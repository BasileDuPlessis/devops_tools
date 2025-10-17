#!/usr/bin/env python3
"""
Google Forms CSV Generator for DevOps Maturity Survey
===================================================

This script generates a CSV file that can be imported directly into Google Forms
for bulk question creation, greatly simplifying the survey setup process.
"""

import csv
import json
from typing import List, Dict

class GoogleFormsCSVGenerator:
    """Generates CSV file for Google Forms bulk import"""

    def __init__(self):
        self.questions_data = []

    def add_question(self, title: str, type: str, description: str = "",
                    options: List[str] = None, required: bool = False,
                    scale_min: int = None, scale_max: int = None,
                    scale_labels: List[str] = None):
        """Add a question to the CSV data"""
        question = {
            'title': title,
            'type': type,
            'description': description,
            'required': 'Yes' if required else 'No'
        }

        if options:
            # Join options with newlines for Google Forms format
            question['options'] = '\n'.join(options)

        if scale_min is not None and scale_max is not None:
            question['scale_min'] = str(scale_min)
            question['scale_max'] = str(scale_max)
            if scale_labels:
                question['scale_labels'] = f"{scale_labels[0]}|{scale_labels[1]}"

        self.questions_data.append(question)

    def generate_demographics_section(self):
        """Generate demographics questions"""
        self.add_question(
            title="What is your role in the organization?",
            type="Multiple Choice",
            options=[
                "Developer/Engineer",
                "DevOps Engineer/SRE",
                "IT Operations/Infrastructure",
                "Security Engineer",
                "Compliance/Risk Management",
                "Project Manager",
                "IT Management",
                "Other"
            ],
            required=True
        )

        self.add_question(
            title="How many years of experience do you have in software development/IT?",
            type="Multiple Choice",
            options=["< 1 year", "1-3 years", "3-5 years", "5-10 years", "10+ years"],
            required=True
        )

        self.add_question(
            title="What is the size of your development team?",
            type="Multiple Choice",
            options=["1-5", "6-20", "21-50", "51-100", "100+"],
            required=True
        )

        self.add_question(
            title="Which business domain does your team primarily support?",
            type="Multiple Choice",
            options=[
                "Retail Banking",
                "Investment Banking",
                "Risk Management",
                "Compliance/Regulatory",
                "Payments/Transactions",
                "Core Banking Systems",
                "Digital Banking/Mobile",
                "Data Analytics/BI",
                "Other"
            ],
            required=True
        )

    def generate_culture_section(self):
        """Generate DevOps culture questions"""
        self.add_question(
            title="How would you rate the collaboration between development and operations teams?",
            type="Linear Scale",
            scale_min=1,
            scale_max=5,
            scale_labels=["Poor collaboration", "Excellent collaboration"],
            required=True
        )

        self.add_question(
            title="To what extent does your organization embrace a 'fail fast, learn fast' culture?",
            type="Linear Scale",
            scale_min=1,
            scale_max=5,
            scale_labels=["Not at all", "Fully embraced"],
            required=True
        )

        self.add_question(
            title="How frequently do development and operations teams work together on projects?",
            type="Multiple Choice",
            options=["Never", "Rarely", "Sometimes", "Often", "Always"],
            required=True
        )

        self.add_question(
            title="Does your organization have cross-functional teams (DevOps/SRE model)?",
            type="Multiple Choice",
            options=["No", "Planning to implement", "Partially implemented", "Fully implemented"],
            required=True
        )

    def generate_deployment_section(self):
        """Generate deployment practices questions"""
        self.add_question(
            title="How frequently does your team deploy code to production?",
            type="Multiple Choice",
            options=[
                "Fewer than once per month",
                "Once per month",
                "Once per week",
                "Multiple times per week",
                "On-demand (multiple times per day)"
            ],
            required=True
        )

        self.add_question(
            title="What is the typical lead time from code commit to production deployment?",
            type="Multiple Choice",
            options=[
                "More than 6 months",
                "1-6 months",
                "1 week - 1 month",
                "1 day - 1 week",
                "Less than 1 day"
            ],
            required=True
        )

        self.add_question(
            title="How long does it typically take to restore service after an incident?",
            type="Multiple Choice",
            options=[
                "More than 1 week",
                "1 day - 1 week",
                "1 hour - 1 day",
                "Less than 1 hour",
                "Less than 1 hour (automated)"
            ],
            required=True
        )

        self.add_question(
            title="What percentage of deployments result in failures requiring rollback?",
            type="Multiple Choice",
            options=["60%+", "45-60%", "30-45%", "15-30%", "0-15%"],
            required=True
        )

        self.add_question(
            title="What deployment strategy does your team primarily use?",
            type="Multiple Choice",
            options=[
                "Manual deployments",
                "Automated deployments with manual approval",
                "Automated deployments with automated testing",
                "Continuous deployment",
                "GitOps/declarative deployments"
            ],
            required=True
        )

    def generate_monitoring_section(self):
        """Generate monitoring questions"""
        self.add_question(
            title="How comprehensive is your application monitoring?",
            type="Linear Scale",
            scale_min=1,
            scale_max=5,
            scale_labels=["Basic logging only", "Full observability stack"],
            required=True
        )

        self.add_question(
            title="Do you have automated alerting for production issues?",
            type="Multiple Choice",
            options=["No", "Basic alerts", "Comprehensive alerting", "AI-driven alerting"],
            required=True
        )

        self.add_question(
            title="How do you track application performance metrics?",
            type="Multiple Choice",
            options=[
                "Manual monitoring",
                "Basic dashboards",
                "Real-time dashboards with alerts",
                "AI/ML-based anomaly detection"
            ],
            required=True
        )

    def generate_security_section(self):
        """Generate security questions"""
        self.add_question(
            title="How is security integrated into your development process?",
            type="Multiple Choice",
            options=[
                "Security as an afterthought",
                "Manual security reviews",
                "Automated security scanning",
                "DevSecOps with security champions",
                "Security by design/Shift-left security"
            ],
            required=True
        )

        self.add_question(
            title="What security testing is performed before deployment?",
            type="Checkboxes",
            options=[
                "Static Application Security Testing (SAST)",
                "Dynamic Application Security Testing (DAST)",
                "Software Composition Analysis (SCA)",
                "Container security scanning",
                "Infrastructure as Code security",
                "None of the above"
            ],
            required=True
        )

    def generate_compliance_section(self):
        """Generate compliance questions"""
        self.add_question(
            title="How does your team handle regulatory compliance in deployments?",
            type="Multiple Choice",
            options=[
                "Manual compliance checks",
                "Automated compliance validation",
                "Compliance as code",
                "Integrated compliance monitoring"
            ],
            required=True
        )

        self.add_question(
            title="What audit capabilities do you have for deployment changes?",
            type="Multiple Choice",
            options=[
                "Basic logging",
                "Change tracking",
                "Automated audit trails",
                "Real-time compliance monitoring"
            ],
            required=True
        )

    def generate_csv(self, filename: str = "devops_survey_questions.csv"):
        """Generate CSV file for Google Forms import"""
        # Build all questions
        self.generate_demographics_section()
        self.generate_culture_section()
        self.generate_deployment_section()
        self.generate_monitoring_section()
        self.generate_security_section()
        self.generate_compliance_section()

        # CSV headers for Google Forms import
        headers = ['Question', 'Type', 'Description', 'Options', 'Required',
                  'Scale Min', 'Scale Max', 'Scale Labels']

        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=headers)
            writer.writeheader()

            for question in self.questions_data:
                row = {
                    'Question': question['title'],
                    'Type': question['type'],
                    'Description': question.get('description', ''),
                    'Options': question.get('options', ''),
                    'Required': question['required'],
                    'Scale Min': question.get('scale_min', ''),
                    'Scale Max': question.get('scale_max', ''),
                    'Scale Labels': question.get('scale_labels', '')
                }
                writer.writerow(row)

        print(f"Google Forms CSV generated: {filename}")
        return filename

    def generate_import_instructions(self, csv_file: str = "devops_survey_questions.csv",
                                   instructions_file: str = "google_forms_import_guide.md"):
        """Generate simplified import instructions"""
        instructions = f"""# 🚀 Quick Google Forms Import Guide

## Method 1: Direct CSV Import (Recommended)

### Step 1: Create Form
1. Go to [Google Forms](https://forms.google.com)
2. Click **"Blank"** to create a new form
3. Title: **"DevOps Maturity Assessment - Banking Environment"**
4. Description: **"This survey assesses your organization's DevOps maturity and DORA metrics implementation."**

### Step 2: Import Questions
1. Click the **⋮ (More options)** menu in the top-right
2. Select **"Import questions"**
3. Upload the file: **`{csv_file}`**
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
"""

        with open(instructions_file, 'w', encoding='utf-8') as f:
            f.write(instructions)

        print(f"Import instructions saved: {instructions_file}")

if __name__ == "__main__":
    generator = GoogleFormsCSVGenerator()
    csv_file = generator.generate_csv()
    generator.generate_import_instructions(csv_file)