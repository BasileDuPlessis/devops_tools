# DevOps Maturity Survey Setup Guide

## Step 1: Create Google Form
1. Go to [Google Forms](https://forms.google.com)
2. Create a new form titled: "DevOps Maturity Assessment - Banking Environment"
3. Add the description: "This survey assesses your organization's DevOps maturity and DORA metrics implementation."

## Step 2: Add Questions

Copy the following questions into your Google Form:

### Section 1: About You

### Section: About You

**Question 1:** What is your role in the organization?
Type: Multiple choice
Options:
- Developer/Engineer
- DevOps Engineer/SRE
- IT Operations/Infrastructure
- Security Engineer
- Compliance/Risk Management
- Project Manager
- IT Management
- Other
*Required*


**Question 2:** How many years of experience do you have in software development/IT?
Type: Multiple choice
Options:
- < 1 year
- 1-3 years
- 3-5 years
- 5-10 years
- 10+ years
*Required*


**Question 3:** What is the size of your development team?
Type: Multiple choice
Options:
- 1-5
- 6-20
- 21-50
- 51-100
- 100+
*Required*


**Question 4:** Which business domain does your team primarily support?
Type: Multiple choice
Options:
- Retail Banking
- Investment Banking
- Risk Management
- Compliance/Regulatory
- Payments/Transactions
- Core Banking Systems
- Digital Banking/Mobile
- Data Analytics/BI
- Other
*Required*


### Section: DevOps Culture

**Question 1:** How would you rate the collaboration between development and operations teams?
Type: Linear scale (1 to 5)
Labels: Poor collaboration → Excellent collaboration
*Required*


**Question 2:** To what extent does your organization embrace a 'fail fast, learn fast' culture?
Type: Linear scale (1 to 5)
Labels: Not at all → Fully embraced
*Required*


**Question 3:** How frequently do development and operations teams work together on projects?
Type: Multiple choice
Options:
- Never
- Rarely
- Sometimes
- Often
- Always
*Required*


**Question 4:** Does your organization have cross-functional teams (DevOps/SRE model)?
Type: Multiple choice
Options:
- No
- Planning to implement
- Partially implemented
- Fully implemented
*Required*


### Section: Deployment Practices

**Question 1:** How frequently does your team deploy code to production?
Type: Multiple choice
Options:
- Fewer than once per month
- Once per month
- Once per week
- Multiple times per week
- On-demand (multiple times per day)
*Required*


**Question 2:** What is the typical lead time from code commit to production deployment?
Type: Multiple choice
Options:
- More than 6 months
- 1-6 months
- 1 week - 1 month
- 1 day - 1 week
- Less than 1 day
*Required*


**Question 3:** How long does it typically take to restore service after an incident?
Type: Multiple choice
Options:
- More than 1 week
- 1 day - 1 week
- 1 hour - 1 day
- Less than 1 hour
- Less than 1 hour (automated)
*Required*


**Question 4:** What percentage of deployments result in failures requiring rollback?
Type: Multiple choice
Options:
- 60%+
- 45-60%
- 30-45%
- 15-30%
- 0-15%
*Required*


**Question 5:** What deployment strategy does your team primarily use?
Type: Multiple choice
Options:
- Manual deployments
- Automated deployments with manual approval
- Automated deployments with automated testing
- Continuous deployment
- GitOps/declarative deployments
*Required*


### Section: Monitoring & Observability

**Question 1:** How comprehensive is your application monitoring?
Type: Linear scale (1 to 5)
Labels: Basic logging only → Full observability stack
*Required*


**Question 2:** Do you have automated alerting for production issues?
Type: Multiple choice
Options:
- No
- Basic alerts
- Comprehensive alerting
- AI-driven alerting
*Required*


**Question 3:** How do you track application performance metrics?
Type: Multiple choice
Options:
- Manual monitoring
- Basic dashboards
- Real-time dashboards with alerts
- AI/ML-based anomaly detection
*Required*


### Section: Security Practices

**Question 1:** How is security integrated into your development process?
Type: Multiple choice
Options:
- Security as an afterthought
- Manual security reviews
- Automated security scanning
- DevSecOps with security champions
- Security by design/Shift-left security
*Required*


**Question 2:** What security testing is performed before deployment?
Type: Checkboxes
Options:
- Static Application Security Testing (SAST)
- Dynamic Application Security Testing (DAST)
- Software Composition Analysis (SCA)
- Container security scanning
- Infrastructure as Code security
- None of the above
*Required*


### Section: Compliance & Audit

**Question 1:** How does your team handle regulatory compliance in deployments?
Type: Multiple choice
Options:
- Manual compliance checks
- Automated compliance validation
- Compliance as code
- Integrated compliance monitoring
*Required*


**Question 2:** What audit capabilities do you have for deployment changes?
Type: Multiple choice
Options:
- Basic logging
- Change tracking
- Automated audit trails
- Real-time compliance monitoring
*Required*


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
