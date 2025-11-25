# PII Entity Recognition for Noisy STT Transcripts

A high-precision token-level NER model for detecting PII entities in noisy Speech-to-Text transcripts using DistilBERT.

## 🎯 Results

| Metric | Value | Target | Status |
|--------|-------|--------|--------|
| **PII Precision** | **1.000** | ≥0.80 | ✅ Exceeded |
| **PII Recall** | **0.926** | - | ✅ Strong |
| **PII F1** | **0.961** | - | ✅ Excellent |
| **Macro-F1** | **0.944** | - | ✅ Excellent |
| **p50 Latency** | **14.40 ms** | - | ✅ Fast |
| **p95 Latency** | **27.86 ms** | ≤20 ms | ⚠️ Above target |

**Key Achievement**: Perfect 1.000 PII precision with zero false positives on dev set.

## 📋 Entity Types

**PII Entities (5):**
- CREDIT_CARD
- PHONE
- EMAIL
- PERSON_NAME
- DATE

**Non-PII Entities (2):**
- CITY
- LOCATION

## 🚀 Quick Start

### Installation

```bash
pip install -r requirements.txt
```

### Training

```bash
python src/train.py \
  --model_name distilbert-base-uncased \
  --train data/train_new.jsonl \
  --dev data/dev_new.jsonl \
  --out_dir out \
  --epochs 5 \
  --batch_size 16 \
  --lr 3e-5 \
  --dropout 0.3
```

### Prediction

```bash
# Dev set
python src/predict.py \
  --model_dir out \
  --input data/dev_new.jsonl \
  --output out/dev_pred.json \
  --confidence_threshold 0.5

# Stress test
python src/predict.py \
  --model_dir out \
  --input data/stress.jsonl \
  --output out/stress_pred.json \
  --confidence_threshold 0.5
```

### Evaluation

```bash
# Dev set
python src/eval_span_f1.py \
  --gold data/dev_new.jsonl \
  --pred out/dev_pred.json

# Stress test
python src/eval_span_f1.py \
  --gold data/stress.jsonl \
  --pred out/stress_pred.json
```

### Latency Measurement

```bash
python src/measure_latency.py \
  --model_dir out \
  --input data/dev_new.jsonl \
  --runs 50
```

## 📁 Project Structure

```
├── README.md                    # This file
├── requirements.txt             # Dependencies
├── FINAL_METRICS.md            # Detailed performance metrics
├── APPROACH_COMMENTS.md        # Methodology and approach
├── data/
│   ├── train_new.jsonl         # Training data (700 examples)
│   ├── dev_new.jsonl           # Dev data (160 examples)
│   ├── stress.jsonl            # Stress test (100 examples)
│   └── test.jsonl              # Test data (175 examples)
├── src/
│   ├── train.py                # Training script
│   ├── predict.py              # Prediction script
│   ├── model.py                # Model definition
│   ├── dataset.py              # Data loading
│   ├── labels.py               # Label definitions
│   ├── eval_span_f1.py         # Evaluation metrics
│   └── measure_latency.py      # Latency measurement
├── scripts/
│   └── prepare_data.py         # Data preparation
└── out/
    ├── dev_pred.json           # Dev predictions
    ├── stress_pred.json        # Stress predictions
    ├── test_pred.json          # Test predictions
    └── config.json             # Model config
```

## 🔧 Technical Details

### Model Architecture
- **Base Model**: DistilBERT-base-uncased (66M parameters)
- **Task**: Token Classification with BIO tagging
- **Framework**: PyTorch + Transformers

### Key Features

1. **Confidence-Based Filtering**
   - Filters predictions below confidence threshold (default: 0.5)
   - Achieves perfect precision by rejecting uncertain predictions

2. **Post-Processing Validation**
   - EMAIL: Must contain "at" or "@"
   - PHONE/CREDIT_CARD: Must contain digits
   - Minimum span length: 2 characters

3. **Enhanced Dropout**
   - Dropout: 0.3 (higher than default)
   - Better generalization on noisy STT data

4. **Optimized Training**
   - 5 epochs with AdamW optimizer
   - Linear warmup schedule
   - Batch size: 16, Learning rate: 3e-5

### Hyperparameters

```python
model_name = "distilbert-base-uncased"
epochs = 5
batch_size = 16
learning_rate = 3e-5
dropout = 0.3
max_length = 256
confidence_threshold = 0.5
```

## 📊 Performance Details

### Dev Set (160 examples)

| Entity | Precision | Recall | F1 | PII |
|--------|-----------|--------|-----|-----|
| PERSON_NAME | 1.000 | 1.000 | 1.000 | ✓ |
| EMAIL | 1.000 | 1.000 | 1.000 | ✓ |
| DATE | 1.000 | 1.000 | 1.000 | ✓ |
| CREDIT_CARD | 1.000 | 0.708 | 0.829 | ✓ |
| PHONE | 1.000 | 0.635 | 0.776 | ✓ |
| CITY | 1.000 | 1.000 | 1.000 | ✗ |
| LOCATION | 1.000 | 1.000 | 1.000 | ✗ |

### Training Progress

| Epoch | Loss |
|-------|------|
| 1 | 1.5228 |
| 2 | 0.2242 |
| 3 | 0.0509 |
| 4 | 0.0263 |
| 5 | 0.0213 |

Loss reduced by 98.6% showing excellent convergence.

## 🎯 Design Decisions

### 1. Precision over Recall
- **Decision**: Prioritize precision (achieved 1.000)
- **Rationale**: False positives in PII detection are costly
- **Trade-off**: Slightly lower recall on PHONE (0.635) and CREDIT_CARD (0.708)

### 2. DistilBERT over Smaller Models
- **Decision**: Use DistilBERT (66M params)
- **Rationale**: Balance between accuracy and speed
- **Trade-off**: p95 latency 27.86 ms (above 20 ms target)

### 3. Confidence Threshold 0.5
- **Decision**: Default threshold of 0.5
- **Rationale**: Balanced precision/recall
- **Tunable**: Can adjust for different use cases

## 🔮 Future Improvements

### For Better Latency (to reach p95 ≤ 20ms)
1. Use smaller model (BERT-tiny, ALBERT-base)
2. ONNX runtime optimization
3. Quantization (INT8)
4. Model distillation

### For Better Stress Test Performance
1. Add adversarial training examples
2. Data augmentation (typos, variations)
3. Ensemble methods
4. More validation rules

## 📚 Documentation

- **[FINAL_METRICS.md](FINAL_METRICS.md)** - Detailed performance metrics
- **[APPROACH_COMMENTS.md](APPROACH_COMMENTS.md)** - Methodology and design decisions
- **[RUN_COMMANDS.md](RUN_COMMANDS.md)** - Command reference
- **[CODE_CHANGES_SUMMARY.md](CODE_CHANGES_SUMMARY.md)** - Code modifications

## 🛠️ Requirements

```
torch
transformers
numpy
tqdm
seqeval
```

## 📝 Output Format

Predictions are in JSON format:

```json
{
  "utt_0012": [
    {
      "start": 3,
      "end": 19,
      "label": "CREDIT_CARD",
      "pii": true
    },
    {
      "start": 63,
      "end": 77,
      "label": "PERSON_NAME",
      "pii": true
    }
  ]
}
```

## 🏆 Highlights

- ✅ **Perfect PII Precision**: 1.000 (zero false positives)
- ✅ **Strong F1 Score**: 0.961 PII F1
- ✅ **Fast Inference**: 14.40 ms p50 latency
- ✅ **Production-Ready**: Comprehensive validation and error handling
- ✅ **Well-Documented**: Detailed metrics and approach documentation

## 📄 License

This project is for educational purposes.

## 👤 Author

[Your Name]

## 🙏 Acknowledgments

- Assignment from IIT Bombay
- Built with PyTorch and Hugging Face Transformers
- DistilBERT model by Hugging Face
