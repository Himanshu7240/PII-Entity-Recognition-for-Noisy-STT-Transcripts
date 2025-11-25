"""
Script to prepare proper train/dev split since dev.jsonl only has 10 examples
"""
import json
import random

random.seed(42)

# Read all training data
with open('data/train.jsonl', 'r', encoding='utf-8') as f:
    train_lines = [line.strip() for line in f if line.strip()]

# Read existing dev data
with open('data/dev.jsonl', 'r', encoding='utf-8') as f:
    dev_lines = [line.strip() for line in f if line.strip()]

print(f"Original train: {len(train_lines)} examples")
print(f"Original dev: {len(dev_lines)} examples")

# Shuffle train data
random.shuffle(train_lines)

# Split: 700 train, 150 dev (keeping original 10 dev + 140 from train)
new_train = train_lines[:700]
additional_dev = train_lines[700:]

# Combine with existing dev
all_dev = dev_lines + additional_dev

# Write new files
with open('data/train_new.jsonl', 'w', encoding='utf-8') as f:
    for line in new_train:
        f.write(line + '\n')

with open('data/dev_new.jsonl', 'w', encoding='utf-8') as f:
    for line in all_dev:
        f.write(line + '\n')

print(f"\nNew train: {len(new_train)} examples")
print(f"New dev: {len(all_dev)} examples")
print("\nCreated: data/train_new.jsonl and data/dev_new.jsonl")
