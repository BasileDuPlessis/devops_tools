# 🚀 Google Apps Script Setup Guide

## Method 1: Direct Google Apps Script (Recommended - 1 minute setup)

Google Forms supports programmatic creation via Google Apps Script. This creates your entire survey automatically!

### Step-by-Step Setup:

1. **Go to Google Forms**
   - Visit [forms.google.com](https://forms.google.com)

2. **Create New Form**
   - Click "Blank" to create a new form

3. **Open Script Editor**
   - Click the ⋮ (three dots) menu in the top-right
   - Select "Script editor"

4. **Copy the Code**
   - Copy the entire contents of `google_apps_script.js`
   - Paste it into the script editor

5. **Save & Run**
   - Click the save icon (💾)
   - Click the run button (▶️) next to `createDevOpsSurveyForm`
   - Grant permissions when prompted

6. **Done! ✅**
   - Your complete survey is created automatically
   - All 23 questions, sections, and settings configured

### What Gets Created:

- ✅ **Complete survey** with all DORA metrics questions
- ✅ **6 sections** properly organized
- ✅ **Required sign-in** for banking compliance
- ✅ **Email collection** enabled
- ✅ **All question types** (multiple choice, scales, checkboxes)
- ✅ **Proper validation** and required fields

### Form URLs:

After running the script, check the logs for:
- **Edit URL**: Customize the form further
- **Published URL**: Share with respondents
- **Response Summary**: Monitor responses

## Method 2: Manual Copy-Paste (Alternative)

If you prefer manual control:

1. Create a new Google Form
2. Copy questions from `google_forms_setup.md`
3. Set up sections and validation manually

## Method 3: Template Copy

For multiple surveys:

1. Create one form using Method 1
2. Use "Make a copy" to duplicate
3. Modify as needed

## Troubleshooting

### "Script authorization required"
- Click "Authorize access"
- Choose your Google account
- Allow permissions

### "Form not created"
- Check the execution logs
- Ensure you have Forms API access
- Try refreshing the page

### "Script timeout"
- The script should complete in < 30 seconds
- If it times out, try again

## Advanced Usage

### Customize Questions
Edit the `QUESTIONS` array in the script to:
- Add banking-specific questions
- Modify existing questions
- Change scoring scales

### Add Logic
Extend the script to include:
- Conditional questions
- Dynamic sections
- Custom validation

### Automate Distribution
Add code to:
- Share with specific users
- Set response limits
- Schedule form availability

---

**Result**: Professional DevOps maturity survey ready in 1 minute! 🎉