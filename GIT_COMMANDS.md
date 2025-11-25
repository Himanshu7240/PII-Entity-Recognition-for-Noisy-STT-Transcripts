# Git Commands for Submission

## Step-by-Step Git Setup and Push

### Step 1: Initialize Git Repository

```bash
# Make sure you're in the project directory
cd C:\Users\HP\Dropbox\PC\Desktop\assignment\pii_ner_assignment_IITB\pii_ner_assignment_IITB

# Initialize git
git init

# Configure git (if first time)
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

### Step 2: Add Files

```bash
# Check what files will be added
git status

# Add all files (respects .gitignore)
git add .

# Check what's staged
git status
```

### Step 3: Commit

```bash
# Create first commit
git commit -m "Initial commit: PII NER Assignment with DistilBERT

- Achieved 1.000 PII precision on dev set
- DistilBERT-base-uncased with confidence filtering
- Complete documentation and metrics
- Dev, stress, and test predictions included"
```

### Step 4: Create GitHub Repository

1. Go to https://github.com/new
2. Repository name: `pii-ner-assignment`
3. Description: `PII Entity Recognition for Noisy STT Transcripts using DistilBERT`
4. **Public** (not private)
5. **Don't** initialize with README (we already have one)
6. Click "Create repository"

### Step 5: Push to GitHub

```bash
# Add remote (replace YOUR_USERNAME with your GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/pii-ner-assignment.git

# Rename branch to main
git branch -M main

# Push to GitHub
git push -u origin main
```

**Note**: If you get authentication error, you'll need a Personal Access Token:
1. Go to GitHub Settings → Developer settings → Personal access tokens → Tokens (classic)
2. Generate new token with "repo" scope
3. Copy the token
4. Use it as password when prompted

### Step 6: Verify on GitHub

Go to: `https://github.com/YOUR_USERNAME/pii-ner-assignment`

Check that you can see:
- ✅ README.md (displays nicely)
- ✅ All source files in `src/`
- ✅ Data files in `data/`
- ✅ Prediction files in `out/`
- ✅ Documentation files (FINAL_METRICS.md, APPROACH_COMMENTS.md)

---

## Alternative: If You Already Have a Git Repo

If you already initialized git earlier:

```bash
# Check current status
git status

# Add any new/modified files
git add .

# Commit changes
git commit -m "Final submission: Complete PII NER assignment"

# Push to GitHub
git push
```

---

## Troubleshooting

### Problem: "fatal: not a git repository"

**Solution**: You need to initialize git first
```bash
git init
```

### Problem: "remote origin already exists"

**Solution**: Update the remote URL
```bash
git remote set-url origin https://github.com/YOUR_USERNAME/pii-ner-assignment.git
```

### Problem: "failed to push some refs"

**Solution**: Pull first, then push
```bash
git pull origin main --allow-unrelated-histories
git push -u origin main
```

### Problem: Authentication failed

**Solution**: Use Personal Access Token
1. Generate token at: https://github.com/settings/tokens
2. Use token as password when pushing

### Problem: Files too large

**Solution**: Already handled by .gitignore
- Model files (*.safetensors, *.bin) are excluded
- Only code and predictions are pushed

---

## What Gets Pushed to GitHub

### ✅ Included (will be pushed)
- All Python source code (`src/*.py`)
- Data files (`data/*.jsonl`)
- Prediction files (`out/*.json`)
- Configuration files (`out/config.json`, `out/tokenizer*.json`)
- Documentation (`*.md` files)
- Requirements (`requirements.txt`)

### ❌ Excluded (in .gitignore)
- Model weights (`out/model.safetensors`, `out/*.bin`)
- Python cache (`__pycache__/`, `*.pyc`)
- IDE files (`.vscode/`, `.idea/`)
- PDF files (`*.pdf`)
- Virtual environments (`venv/`, `env/`)

---

## Quick Reference

```bash
# Full workflow
git init
git add .
git commit -m "Initial commit: PII NER Assignment"
git remote add origin https://github.com/YOUR_USERNAME/pii-ner-assignment.git
git branch -M main
git push -u origin main
```

---

## After Pushing

### Verify Your Repository

1. Go to: `https://github.com/YOUR_USERNAME/pii-ner-assignment`
2. Check README displays correctly
3. Navigate to `out/dev_pred.json` - should be viewable
4. Navigate to `FINAL_METRICS.md` - should be viewable
5. Navigate to `APPROACH_COMMENTS.md` - should be viewable

### Get Your Submission URLs

Once pushed, your submission URLs will be:

**Repository:**
```
https://github.com/YOUR_USERNAME/pii-ner-assignment
```

**Dev Predictions:**
```
https://github.com/YOUR_USERNAME/pii-ner-assignment/blob/main/out/dev_pred.json
```

**Stress Predictions:**
```
https://github.com/YOUR_USERNAME/pii-ner-assignment/blob/main/out/stress_pred.json
```

**Final Metrics:**
```
https://github.com/YOUR_USERNAME/pii-ner-assignment/blob/main/FINAL_METRICS.md
```

**Approach/Comments:**
```
https://github.com/YOUR_USERNAME/pii-ner-assignment/blob/main/APPROACH_COMMENTS.md
```

---

## You're Done! 🎉

Your code is now on GitHub and ready for submission!
