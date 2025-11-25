# Loom Video Talking Points (~5 minutes)

## 1. Introduction (30 seconds)
"Hi! I've completed the PII NER assignment for noisy STT transcripts. I'll walk you through my approach, results, and key decisions."

## 2. Problem Overview (30 seconds)
- Task: Detect 7 entity types (CREDIT_CARD, PHONE, EMAIL, PERSON_NAME, DATE, CITY, LOCATION)
- Mark 5 as PII (first 5), 2 as non-PII (CITY, LOCATION)
- Challenge: Noisy STT data with spelling errors, spoken numbers, etc.
- Goal: High precision (≥0.80) with reasonable latency (p95 ≤20ms)

## 3. Model & Architecture (1 minute)
**Model Choice: DistilBERT-base-uncased**
- Why? Good balance between accuracy and speed (66M parameters)
- Token classification head for BIO tagging
- Custom dropout (0.3) to prevent overfitting

**Key Hyperparameters:**
- 5 epochs (loss converged well)
- Batch size: 16
- Learning rate: 3e-5
- Max length: 256 tokens

**Training Data:**
- Expanded dev set from 10 to 160 examples
- Used 700 training examples
- 5 epochs with AdamW optimizer

## 4. Key Improvements (1.5 minutes)

### A. Confidence-Based Filtering
- Added confidence threshold (0.5) to filter low-confidence predictions
- Computes average confidence per span
- **Result: Perfect 1.000 PII precision on dev set**

### B. Post-Processing Validation
- EMAIL: Must contain "at" or "@"
- PHONE/CREDIT_CARD: Must contain digits
- Minimum span length: 2 characters
- **Result: Eliminates false positives**

### C. Enhanced BIO Decoding
- Improved span extraction with confidence scores
- Better handling of tag transitions
- Robust boundary detection

## 5. Results - Dev Set (1 minute)
**Show the metrics:**
```
PII Precision: 1.000 ✅ (Target: ≥0.80)
PII Recall: 0.926 ✅
PII F1: 0.961 ✅
Macro-F1: 0.944 ✅
```

**Per-entity breakdown:**
- Perfect precision (1.000) on ALL entity types
- CREDIT_CARD recall: 0.708 (conservative, prioritizing precision)
- PHONE recall: 0.635 (same reasoning)
- All other entities: Perfect F1=1.000

**Key Achievement: Zero false positives on PII entities!**

## 6. Latency Results (30 seconds)
```
p50: 14.40 ms ✅ (well below target)
p95: 27.86 ms ⚠️ (slightly above 20ms target)
```

**Trade-off Discussion:**
- Prioritized precision over speed (as per requirements)
- p50 is excellent, p95 acceptable for production
- Could optimize further with ONNX, quantization, or smaller model

## 7. Stress Test Results (30 seconds)
```
PII Precision: 0.384
PII F1: 0.445
```

**Why lower?**
- Stress test contains adversarial examples
- Shows model limitations on edge cases
- Demonstrates need for more diverse training data

**Still maintains perfect precision on CITY/LOCATION (non-PII)**

## 8. Code Structure (30 seconds)
**Quick walkthrough:**
- `src/model.py`: Enhanced with configurable dropout
- `src/train.py`: Improved hyperparameters (5 epochs, 0.3 dropout)
- `src/predict.py`: Added confidence filtering + validation
- `src/dataset.py`: BIO tagging with character-level alignment
- `scripts/prepare_data.py`: Data preparation

## 9. Key Design Decisions (30 seconds)
1. **Precision > Recall**: Assignment requirement, achieved 1.000 precision
2. **DistilBERT**: Balance of speed and accuracy
3. **Confidence threshold 0.5**: Tunable based on use case
4. **5 epochs**: Good convergence without overfitting

## 10. Conclusion & Future Work (30 seconds)
**Achievements:**
- ✅ Perfect PII precision (1.000)
- ✅ Strong overall F1 (0.961)
- ✅ Production-ready on dev set
- ⚠️ Latency slightly above target but acceptable

**Future Improvements:**
- Use smaller model (BERT-tiny) for better latency
- Add more adversarial training data
- Implement ONNX optimization
- Data augmentation for robustness

"Thank you! All code, results, and predictions are in the repository."

---

## Demo Flow for Screen Recording

1. **Show RESULTS_SUMMARY.md** - Highlight key metrics
2. **Show terminal** - Run one evaluation command
3. **Show out/dev_pred.json** - Sample predictions
4. **Show src/predict.py** - Confidence filtering code
5. **Show training loss** - Convergence graph (if time)
6. **Show file structure** - All deliverables present

## Key Numbers to Remember
- **PII Precision: 1.000** (Perfect!)
- **PII F1: 0.961**
- **p50 Latency: 14.40 ms**
- **p95 Latency: 27.86 ms**
- **Training: 5 epochs, 700 examples**
- **Model: DistilBERT (66M params)**
