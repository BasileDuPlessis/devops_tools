# DevOps Maturity Survey Tool for Banking

A comprehensive tool for assessing DevOps maturity and DORA metrics implementation in banking and financial services environments.

## Features

- **Google Forms Survey Template**: Pre-built survey covering DORA metrics, DevOps culture, security, and compliance
- **Automated Analysis**: Process survey responses and calculate maturity scores
- **Radar Charts**: Visual maturity assessment against industry benchmarks
- **Excel Dashboard**: Professional reporting with charts and recommendations
- **Bank-Compliant**: Designed for financial services regulatory requirements

## Quick Start

### 1. Install Dependencies

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install required packages
pip install openpyxl pandas matplotlib seaborn
```

### 2. Generate Survey Files

```bash
python3 generate_google_forms_csv.py  # Optional: generates documentation
```

This creates:
- `google_apps_script.js` - Direct form creation script
- `google_apps_script_setup.md` - Quick setup instructions
- `devops_maturity_survey_template.json` - Survey structure (legacy)
- `google_forms_setup.md` - Detailed manual setup guide (alternative)

### 3. Create Google Forms Survey (3 Methods)

#### 🚀 **Method A: Google Apps Script (Recommended - 1 minute)**
1. Go to [Google Forms](https://forms.google.com)
2. Create blank form → ⋮ (More options) → "Script editor"
3. Copy `google_apps_script.js` content → Save → Run `createDevOpsSurveyForm()`
4. **Done!** Complete survey created automatically with all questions and settings.

#### 📋 **Method B: Template Copy (2 minutes)**
1. Use the Apps Script method once to create a master template
2. For future surveys: Make a copy of the template form
3. Customize as needed

#### 📝 **Method C: Manual Setup (30 minutes)**
Follow the detailed guide in `google_forms_setup.md`

### 4. Configure Form Settings
- **Require sign-in**: Form settings → Responses → Require sign-in
- **Collect emails**: Form settings → Responses → Collect email addresses
- **Add sections**: Use the import guide for section organization

### 5. Distribute & Collect Responses
- Share with development, operations, security, and compliance teams
- Target 10-20 responses per business domain

### 6. Analyze Results

```bash
python3 analyze_survey_responses.py your_responses.csv
```

This generates:
- `devops_maturity_dashboard.xlsx` - Comprehensive Excel dashboard
- `devops_maturity_radar.png` - Radar chart visualization

## Google Forms Creation Methods

### 🚀 **Google Apps Script (Recommended)**
Google Forms can be created programmatically using Google Apps Script. This method takes ~1 minute:

1. **Create Form**: Go to Google Forms → New blank form
2. **Open Script Editor**: ⋮ (More options) → "Script editor"
3. **Copy Code**: Paste `google_apps_script.js` content
4. **Run Script**: Click run button next to `createDevOpsSurveyForm()`
5. **Complete**: Full survey with all questions and settings created automatically

**Benefits:**
- ⚡ **60x faster** than manual creation
- 🎯 **Zero errors** in setup
- 🔄 **Reproducible** for multiple surveys
- �️ **Bank-compliant** settings pre-configured

### 📋 **Template Method (2 minutes)**
1. Create one master form using Apps Script
2. For additional surveys: Click "Make a copy"
3. Modify questions as needed

### 📝 **Manual Setup (30 minutes)**
For organizations requiring full manual control:
- Follow `google_forms_setup.md` for step-by-step instructions
- Copy-paste each question individually
- Configure sections and validation manually

## Survey Structure

The survey covers 6 key areas:

### 1. Demographics
- Role, experience, team size, business domain

### 2. DevOps Culture
- Collaboration between teams
- Failure culture adoption
- Cross-functional team implementation

### 3. Deployment Practices (DORA Metrics)
- Deployment frequency
- Lead time for changes
- Mean time to restore (MTTR)
- Change failure rate
- Deployment strategies

### 4. Monitoring & Observability
- Monitoring comprehensiveness
- Automated alerting
- Performance tracking

### 5. Security Practices
- Security integration in development
- Security testing coverage

### 6. Compliance & Audit
- Regulatory compliance handling
- Audit capabilities

## Maturity Scoring

### Performance Levels
- **Elite (4.5-5.0)**: Industry-leading practices
- **High (3.5-4.4)**: Advanced implementation
- **Medium (2.5-3.4)**: Developing capabilities
- **Low (1.5-2.4)**: Basic implementation
- **Initial (1.0-1.4)**: Starting out

### DORA Benchmarks
Based on industry research from the DORA (DevOps Research and Assessment) team:

| Metric | Elite | High | Medium | Low |
|--------|-------|------|--------|-----|
| Deployment Frequency | Multiple/day | Multiple/week | Weekly | Monthly |
| Lead Time | <1 day | <1 week | <1 month | <6 months |
| MTTR | <1 hour | <1 day | <1 week | <1 week |
| Failure Rate | 0-15% | 0-15% | 0-15% | 0-15% |

## Output Files

### Excel Dashboard (`devops_maturity_dashboard.xlsx`)

**Summary Sheet:**
- Overall maturity score and performance level
- Category-wise scores and benchmarks
- Key metrics overview

**Demographics Sheet:**
- Response distribution by role, experience, team size
- Business domain coverage

**DORA Metrics Sheet:**
- Detailed breakdown of DORA metric responses
- Performance distribution analysis

**Recommendations Sheet:**
- Prioritized improvement suggestions
- Actionable next steps

### Radar Chart (`devops_maturity_radar.png`)
- Visual comparison against industry benchmarks
- 8-dimensional maturity assessment
- Easy-to-understand performance visualization

## Usage in Banking Context

### Target Audience
- Development teams
- Infrastructure/operations teams
- Security teams
- Compliance officers
- IT management

### Regulatory Compliance
- Survey responses can be anonymized
- Excel outputs suitable for audit trails
- Professional formatting for executive reporting

### Implementation Roadmap
1. **Assessment Phase**: Run survey across teams
2. **Analysis Phase**: Generate reports and identify gaps
3. **Planning Phase**: Create improvement roadmap
4. **Implementation Phase**: Execute prioritized initiatives
5. **Monitoring Phase**: Track progress with follow-up surveys

## Customization

### Adding Questions
Edit `devops_maturity_survey.py` to add banking-specific questions:
```python
def _get_custom_questions(self) -> List[Dict]:
    return [
        {
            "question": "Your custom banking question",
            "type": "choice",
            "options": ["Option 1", "Option 2", "Option 3"],
            "category": "custom",
            "weight": 0.5,
            "required": True
        }
    ]
```

### Modifying Scoring
Update scoring logic in `SurveyAnalyzer` class for custom metrics.

### Branding
Customize colors, logos, and formatting in the Excel dashboard generation.

## Troubleshooting

### Common Issues

**"Module not found" errors:**
```bash
pip install --upgrade openpyxl pandas matplotlib seaborn
```

**CSV import issues:**
- Ensure CSV is exported from Google Forms with proper encoding
- Check for special characters in responses
- Verify column headers match expected format

**Apps Script issues:**
- Grant permissions when prompted during first run
- Ensure you have edit access to the form
- Check script execution logs for error details
- Script timeout: Try running again (should complete in <30 seconds)

**Chart generation fails:**
- Install matplotlib with backend support
- Check file permissions for output directory

### Data Quality
- Aim for 10-20 responses per business domain
- Ensure representative sampling across teams
- Follow up on incomplete responses

## Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For questions or support:
- Create an issue in the repository
- Contact the DevOps team
- Refer to the troubleshooting section above

## Version History

- **v1.0**: Initial release with core DORA metrics and banking compliance features
- Comprehensive survey template and analysis tools
- Excel dashboard and radar chart generation