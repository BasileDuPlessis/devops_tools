# 🚀 Quick Google Forms Import Guide

## Method 1: Direct CSV Import (Recommended)

### Step 1: Create Form
1. Go to [Google Forms](https://forms.google.com)
2. Click **"Blank"** to create a new form
3. Title: **"DevOps Maturity Assessment - Banking Environment"**
4. Description: **"This survey assesses your organization's DevOps maturity and DORA metrics implementation."**

### Step 2: Import Questions
1. Click the **⋮ (More options)** menu in the top-right
2. Select **"Import questions"**
3. Upload the file: **`devops_survey_questions.csv`**
4. All questions will be imported automatically!

### Step 3: Final Setup
1. **Require sign-in**: Form settings → Responses → "Limit to 1 response" → "Require sign-in"
2. **Enable email collection**: Form settings → Responses → "Collect email addresses"
3. **Add sections**: Right-click questions to add section breaks with titles:
   - About You
   - DevOps Culture
   - Deployment Practices
   - Monitoring & Observability
   - Security Practices
   - Compliance & Audit

## Method 2: Manual Copy-Paste (Alternative)

If CSV import doesn't work, use the detailed guide in `google_forms_setup.md`

## Step 4: Test & Distribute

1. **Test the form**: Click "Preview" to ensure all questions work
2. **Share**: Click "Send" and share with your IT teams
3. **Monitor responses**: View responses in real-time

## Step 5: Export & Analyze

Once you have responses:
```bash
python3 analyze_survey_responses.py responses.csv
```

This will generate your maturity assessment dashboard and radar charts!

---

**Note**: The CSV import method saves ~30 minutes of manual question creation!
