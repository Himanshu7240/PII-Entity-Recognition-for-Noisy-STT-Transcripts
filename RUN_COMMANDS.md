# Quick Command Reference

## Complete Workflow Commands

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Prepare Data (Already Done)
```bash
python scripts/prepare_data.py
```

### 3. Train Model
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

### 4. Predict on Dev Set
```bash
python src/predict.py \
  --model_dir out \
  --input data/dev_new.jsonl \
  --output out/dev_pred.json \
  --confidence_threshold 0.5
```

### 5. Evaluate Dev Set
```bash
python src/eval_span_f1.py \
  --gold data/dev_new.jsonl \
  --pred out/dev_pred.json
```

### 6. Predict on Stress Test
```bash
python src/predict.py \
  --model_dir out \
  --input data/stress.jsonl \
  --output out/stress_pred.json \
  --confidence_threshold 0.5
```

### 7. Evaluate Stress Test
```bash
python src/eval_span_f1.py \
  --gold data/stress.jsonl \
  --pred out/stress_pred.json
```

### 8. Measure Latency
```bash
python src/measure_latency.py \
  --model_dir out \
  --input data/dev_new.jsonl \
  --runs 50
```

### 9. Predict on Test Set (Optional)
```bash
python src/predict.py \
  --model_dir out \
  --input data/test.jsonl \
  --output out/test_pred.json \
  --confidence_threshold 0.5
```

## Quick Test (All in One)
```bash
# Train
python src/train.py --model_name distilbert-base-uncased --train data/train_new.jsonl --dev data/dev_new.jsonl --out_dir out --epochs 5 --batch_size 16 --lr 3e-5 --dropout 0.3

# Evaluate Dev
python src/predict.py --model_dir out --input data/dev_new.jsonl --output out/dev_pred.json --confidence_threshold 0.5
python src/eval_span_f1.py --gold data/dev_new.jsonl --pred out/dev_pred.json

# Evaluate Stress
python src/predict.py --model_dir out --input data/stress.jsonl --output out/stress_pred.json --confidence_threshold 0.5
python src/eval_span_f1.py --gold data/stress.jsonl --pred out/stress_pred.json

# Measure Latency
python src/measure_latency.py --model_dir out --input data/dev_new.jsonl --runs 50
```

## Adjustable Parameters

### Confidence Threshold
- **Higher (0.7-0.9)**: Better precision, lower recall
- **Lower (0.3-0.5)**: Better recall, lower precision
- **Default: 0.5** (balanced)

### Training Hyperparameters
- `--epochs`: Number of training epochs (default: 5)
- `--batch_size`: Batch size (default: 16)
- `--lr`: Learning rate (default: 3e-5)
- `--dropout`: Dropout rate (default: 0.3)
- `--max_length`: Max sequence length (default: 256)

## Output Files
- `out/config.json` - Model configuration
- `out/pytorch_model.bin` - Trained weights
- `out/tokenizer_config.json` - Tokenizer config
- `out/dev_pred.json` - Dev predictions
- `out/stress_pred.json` - Stress predictions
- `out/test_pred.json` - Test predictions
