#!/usr/bin/env python3
"""
DevOps Maturity Survey Tool for Banking Environment
===============================================

This tool creates a comprehensive survey to assess DevOps maturity and DORA metrics
implementation within banking and financial services organizations.

Features:
- Google Forms survey template generation
- Automated response analysis
- Radar chart visualization
- Maturity benchmarking against industry standards
- Bank-compliant reporting format

Usage:
1. Run this script to generate survey questions
2. Create Google Form with generated questions
3. Export responses as CSV
4. Run analysis script to generate reports
"""

import json
import csv
from datetime import datetime
from typing import Dict, List, Any

class DevOpsMaturitySurvey:
    """DevOps Maturity Survey Generator and Analyzer for Banking"""

    def __init__(self):
        self.survey_sections = {
            "demographics": self._get_demographics_questions(),
            "culture": self._get_culture_questions(),
            "deployment": self._get_deployment_questions(),
            "monitoring": self._get_monitoring_questions(),
            "security": self._get_security_questions(),
            "compliance": self._get_compliance_questions()
        }

        # DORA metrics mapping
        self.dora_metrics = {
            "deployment_frequency": "Deployment Frequency",
            "lead_time": "Lead Time for Changes",
            "mttr": "Mean Time to Restore",
            "failure_rate": "Change Failure Rate"
        }

        # Maturity levels (1-5 scale)
        self.maturity_levels = {
            1: "Initial/Ad-hoc",
            2: "Repeatable",
            3: "Defined",
            4: "Managed/Measured",
            5: "Optimized"
        }

    def _get_demographics_questions(self) -> List[Dict]:
        """Demographic and organizational context questions"""
        return [
            {
                "question": "What is your role in the organization?",
                "type": "choice",
                "options": [
                    "Developer/Engineer",
                    "DevOps Engineer/SRE",
                    "IT Operations/Infrastructure",
                    "Security Engineer",
                    "Compliance/Risk Management",
                    "Project Manager",
                    "IT Management",
                    "Other"
                ],
                "required": True
            },
            {
                "question": "How many years of experience do you have in software development/IT?",
                "type": "choice",
                "options": ["< 1 year", "1-3 years", "3-5 years", "5-10 years", "10+ years"],
                "required": True
            },
            {
                "question": "What is the size of your development team?",
                "type": "choice",
                "options": ["1-5", "6-20", "21-50", "51-100", "100+"],
                "required": True
            },
            {
                "question": "Which business domain does your team primarily support?",
                "type": "choice",
                "options": [
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
                "required": True
            }
        ]

    def _get_culture_questions(self) -> List[Dict]:
        """DevOps culture and collaboration questions"""
        return [
            {
                "question": "How would you rate the collaboration between development and operations teams?",
                "type": "scale",
                "scale_min": 1,
                "scale_max": 5,
                "scale_labels": ["Poor collaboration", "Excellent collaboration"],
                "category": "culture",
                "weight": 1.0,
                "required": True
            },
            {
                "question": "To what extent does your organization embrace a 'fail fast, learn fast' culture?",
                "type": "scale",
                "scale_min": 1,
                "scale_max": 5,
                "scale_labels": ["Not at all", "Fully embraced"],
                "category": "culture",
                "weight": 0.8,
                "required": True
            },
            {
                "question": "How frequently do development and operations teams work together on projects?",
                "type": "choice",
                "options": ["Never", "Rarely", "Sometimes", "Often", "Always"],
                "category": "culture",
                "weight": 0.9,
                "required": True
            },
            {
                "question": "Does your organization have cross-functional teams (DevOps/SRE model)?",
                "type": "choice",
                "options": ["No", "Planning to implement", "Partially implemented", "Fully implemented"],
                "category": "culture",
                "weight": 1.0,
                "required": True
            }
        ]

    def _get_deployment_questions(self) -> List[Dict]:
        """Deployment practices and DORA metrics questions"""
        return [
            {
                "question": "How frequently does your team deploy code to production?",
                "type": "choice",
                "options": [
                    "Fewer than once per month",
                    "Once per month",
                    "Once per week",
                    "Multiple times per week",
                    "On-demand (multiple times per day)"
                ],
                "category": "deployment_frequency",
                "weight": 1.0,
                "required": True
            },
            {
                "question": "What is the typical lead time from code commit to production deployment?",
                "type": "choice",
                "options": [
                    "More than 6 months",
                    "1-6 months",
                    "1 week - 1 month",
                    "1 day - 1 week",
                    "Less than 1 day"
                ],
                "category": "lead_time",
                "weight": 1.0,
                "required": True
            },
            {
                "question": "How long does it typically take to restore service after an incident?",
                "type": "choice",
                "options": [
                    "More than 1 week",
                    "1 day - 1 week",
                    "1 hour - 1 day",
                    "Less than 1 hour",
                    "Less than 1 hour (automated)"
                ],
                "category": "mttr",
                "weight": 1.0,
                "required": True
            },
            {
                "question": "What percentage of deployments result in failures requiring rollback?",
                "type": "choice",
                "options": ["60%+", "45-60%", "30-45%", "15-30%", "0-15%"],
                "category": "failure_rate",
                "weight": 1.0,
                "required": True
            },
            {
                "question": "What deployment strategy does your team primarily use?",
                "type": "choice",
                "options": [
                    "Manual deployments",
                    "Automated deployments with manual approval",
                    "Automated deployments with automated testing",
                    "Continuous deployment",
                    "GitOps/declarative deployments"
                ],
                "category": "deployment",
                "weight": 0.9,
                "required": True
            }
        ]

    def _get_monitoring_questions(self) -> List[Dict]:
        """Monitoring and observability questions"""
        return [
            {
                "question": "How comprehensive is your application monitoring?",
                "type": "scale",
                "scale_min": 1,
                "scale_max": 5,
                "scale_labels": ["Basic logging only", "Full observability stack"],
                "category": "monitoring",
                "weight": 1.0,
                "required": True
            },
            {
                "question": "Do you have automated alerting for production issues?",
                "type": "choice",
                "options": ["No", "Basic alerts", "Comprehensive alerting", "AI-driven alerting"],
                "category": "monitoring",
                "weight": 0.9,
                "required": True
            },
            {
                "question": "How do you track application performance metrics?",
                "type": "choice",
                "options": [
                    "Manual monitoring",
                    "Basic dashboards",
                    "Real-time dashboards with alerts",
                    "AI/ML-based anomaly detection"
                ],
                "category": "monitoring",
                "weight": 0.8,
                "required": True
            }
        ]

    def _get_security_questions(self) -> List[Dict]:
        """Security practices in DevOps context"""
        return [
            {
                "question": "How is security integrated into your development process?",
                "type": "choice",
                "options": [
                    "Security as an afterthought",
                    "Manual security reviews",
                    "Automated security scanning",
                    "DevSecOps with security champions",
                    "Security by design/Shift-left security"
                ],
                "category": "security",
                "weight": 1.0,
                "required": True
            },
            {
                "question": "What security testing is performed before deployment?",
                "type": "checkbox",
                "options": [
                    "Static Application Security Testing (SAST)",
                    "Dynamic Application Security Testing (DAST)",
                    "Software Composition Analysis (SCA)",
                    "Container security scanning",
                    "Infrastructure as Code security",
                    "None of the above"
                ],
                "category": "security",
                "weight": 0.9,
                "required": True
            }
        ]

    def _get_compliance_questions(self) -> List[Dict]:
        """Compliance and regulatory questions for banking"""
        return [
            {
                "question": "How does your team handle regulatory compliance in deployments?",
                "type": "choice",
                "options": [
                    "Manual compliance checks",
                    "Automated compliance validation",
                    "Compliance as code",
                    "Integrated compliance monitoring"
                ],
                "category": "compliance",
                "weight": 1.0,
                "required": True
            },
            {
                "question": "What audit capabilities do you have for deployment changes?",
                "type": "choice",
                "options": [
                    "Basic logging",
                    "Change tracking",
                    "Automated audit trails",
                    "Real-time compliance monitoring"
                ],
                "category": "compliance",
                "weight": 0.9,
                "required": True
            }
        ]

    def generate_survey_template(self, output_file: str = "devops_maturity_survey_template.json"):
        """Generate survey template in JSON format for Google Forms"""
        template = {
            "title": "DevOps Maturity Assessment - Banking Environment",
            "description": "This survey assesses your organization's DevOps maturity and DORA metrics implementation. Your responses will help identify areas for improvement and benchmark against industry standards.",
            "sections": self.survey_sections,
            "metadata": {
                "version": "1.0",
                "created": datetime.now().isoformat(),
                "target_audience": "Banking and Financial Services IT Teams",
                "estimated_duration": "15-20 minutes"
            }
        }

        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(template, f, indent=2, ensure_ascii=False)

        print(f"Survey template saved to {output_file}")
        return template

    def generate_google_forms_instructions(self, template_file: str = "google_forms_setup.md"):
        """Generate instructions for setting up Google Forms survey"""
        instructions = f"""# DevOps Maturity Survey Setup Guide

## Step 1: Create Google Form
1. Go to [Google Forms](https://forms.google.com)
2. Create a new form titled: "DevOps Maturity Assessment - Banking Environment"
3. Add the description: "This survey assesses your organization's DevOps maturity and DORA metrics implementation."

## Step 2: Add Questions

Copy the following questions into your Google Form:

### Section 1: About You
"""

        # Add questions by section
        section_names = {
            "demographics": "About You",
            "culture": "DevOps Culture",
            "deployment": "Deployment Practices",
            "monitoring": "Monitoring & Observability",
            "security": "Security Practices",
            "compliance": "Compliance & Audit"
        }

        for section_key, section_name in section_names.items():
            instructions += f"\n### Section: {section_name}\n"
            for i, question in enumerate(self.survey_sections[section_key], 1):
                instructions += f"\n**Question {i}:** {question['question']}\n"

                if question['type'] == 'choice':
                    instructions += "Type: Multiple choice\nOptions:\n"
                    for option in question['options']:
                        instructions += f"- {option}\n"
                elif question['type'] == 'scale':
                    instructions += f"Type: Linear scale ({question['scale_min']} to {question['scale_max']})\n"
                    instructions += f"Labels: {question['scale_labels'][0]} → {question['scale_labels'][1]}\n"
                elif question['type'] == 'checkbox':
                    instructions += "Type: Checkboxes\nOptions:\n"
                    for option in question['options']:
                        instructions += f"- {option}\n"

                if question.get('required', False):
                    instructions += "*Required*\n"
                instructions += "\n"

        instructions += """
## Step 3: Form Settings
- Make the form require sign-in (for banking compliance)
- Enable email collection
- Set up response validation where appropriate

## Step 4: Distribute Survey
- Share with development, operations, and infrastructure teams
- Target 10-20 responses per business domain for statistical significance

## Step 5: Export Responses
1. Open form responses
2. Click the spreadsheet icon to create a Google Sheet
3. Download as CSV for analysis

## Step 6: Run Analysis
Use the analysis script with your CSV file:
```bash
python analyze_survey_responses.py responses.csv
```
"""

        with open(template_file, 'w', encoding='utf-8') as f:
            f.write(instructions)

        print(f"Google Forms setup instructions saved to {template_file}")

if __name__ == "__main__":
    survey = DevOpsMaturitySurvey()
    survey.generate_survey_template()
    survey.generate_google_forms_instructions()