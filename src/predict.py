import json
import argparse
import torch
import torch.nn.functional as F
from transformers import AutoTokenizer, AutoModelForTokenClassification
from labels import ID2LABEL, label_is_pii
import os
import re


def bio_to_spans_with_confidence(text, offsets, label_ids, logits, confidence_threshold=0.5):
    """
    Improved BIO to span conversion with confidence filtering for higher precision
    """
    spans = []
    current_label = None
    current_start = None
    current_end = None
    current_confidences = []

    for idx, ((start, end), lid) in enumerate(zip(offsets, label_ids)):
        if start == 0 and end == 0:
            continue
        
        label = ID2LABEL.get(int(lid), "O")
        
        # Get confidence score
        if idx < len(logits):
            probs = F.softmax(logits[idx], dim=-1)
            confidence = probs[lid].item()
        else:
            confidence = 1.0
        
        if label == "O":
            if current_label is not None:
                avg_conf = sum(current_confidences) / len(current_confidences) if current_confidences else 0
                if avg_conf >= confidence_threshold:
                    spans.append((current_start, current_end, current_label, avg_conf))
                current_label = None
                current_confidences = []
            continue

        prefix, ent_type = label.split("-", 1)
        if prefix == "B":
            if current_label is not None:
                avg_conf = sum(current_confidences) / len(current_confidences) if current_confidences else 0
                if avg_conf >= confidence_threshold:
                    spans.append((current_start, current_end, current_label, avg_conf))
            current_label = ent_type
            current_start = start
            current_end = end
            current_confidences = [confidence]
        elif prefix == "I":
            if current_label == ent_type:
                current_end = end
                current_confidences.append(confidence)
            else:
                if current_label is not None:
                    avg_conf = sum(current_confidences) / len(current_confidences) if current_confidences else 0
                    if avg_conf >= confidence_threshold:
                        spans.append((current_start, current_end, current_label, avg_conf))
                current_label = ent_type
                current_start = start
                current_end = end
                current_confidences = [confidence]

    if current_label is not None:
        avg_conf = sum(current_confidences) / len(current_confidences) if current_confidences else 0
        if avg_conf >= confidence_threshold:
            spans.append((current_start, current_end, current_label, avg_conf))

    return spans


def validate_span(text, start, end, label):
    """
    Post-process validation to improve precision
    """
    span_text = text[start:end].strip()
    
    # Basic validation rules
    if len(span_text) < 2:
        return False
    
    # Email validation
    if label == "EMAIL":
        if "at" not in span_text.lower() and "@" not in span_text:
            return False
    
    # Phone validation - should have digits
    if label == "PHONE":
        if not any(c.isdigit() for c in span_text):
            return False
    
    # Credit card - should have digits
    if label == "CREDIT_CARD":
        if not any(c.isdigit() for c in span_text):
            return False
    
    return True


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model_dir", default="out")
    ap.add_argument("--model_name", default=None)
    ap.add_argument("--input", default="data/dev_new.jsonl")
    ap.add_argument("--output", default="out/dev_pred.json")
    ap.add_argument("--max_length", type=int, default=256)
    ap.add_argument("--confidence_threshold", type=float, default=0.5)
    ap.add_argument(
        "--device", default="cuda" if torch.cuda.is_available() else "cpu")
    args = ap.parse_args()

    tokenizer = AutoTokenizer.from_pretrained(
        args.model_dir if args.model_name is None else args.model_name)
    model = AutoModelForTokenClassification.from_pretrained(args.model_dir)
    model.to(args.device)
    model.eval()

    results = {}

    with open(args.input, "r", encoding="utf-8") as f:
        for line in f:
            obj = json.loads(line)
            text = obj["text"]
            uid = obj["id"]

            enc = tokenizer(
                text,
                return_offsets_mapping=True,
                truncation=True,
                max_length=args.max_length,
                return_tensors="pt",
            )
            offsets = enc["offset_mapping"][0].tolist()
            input_ids = enc["input_ids"].to(args.device)
            attention_mask = enc["attention_mask"].to(args.device)

            with torch.no_grad():
                out = model(input_ids=input_ids, attention_mask=attention_mask)
                logits = out.logits[0].cpu()
                pred_ids = logits.argmax(dim=-1).tolist()

            # Use improved span extraction with confidence filtering
            spans = bio_to_spans_with_confidence(
                text, offsets, pred_ids, logits, 
                confidence_threshold=args.confidence_threshold
            )
            
            ents = []
            for s, e, lab, conf in spans:
                # Additional validation for higher precision
                if validate_span(text, s, e, lab):
                    ents.append(
                        {
                            "start": int(s),
                            "end": int(e),
                            "label": lab,
                            "pii": bool(label_is_pii(lab)),
                        }
                    )
            results[uid] = ents

    os.makedirs(os.path.dirname(args.output) or ".", exist_ok=True)
    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    print(f"Wrote predictions for {len(results)} utterances to {args.output}")


if __name__ == "__main__":
    main()
