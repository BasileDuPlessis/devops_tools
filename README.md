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

### 2. Generate Survey Template

```bash
python3 devops_maturity_survey.py
```

This creates:
- `devops_maturity_survey_template.json` - Survey structure
- `google_forms_setup.md` - Step-by-step Google Forms setup guide

### 3. Create Google Forms Survey

1. Go to [Google Forms](https://forms.google.com)
2. Follow the instructions in `google_forms_setup.md`
3. Distribute survey to your IT teams
4. Export responses as CSV

### 4. Analyze Results

```bash
python3 analyze_survey_responses.py your_responses.csv
```

This generates:
- `devops_maturity_dashboard.xlsx` - Comprehensive Excel dashboard
- `devops_maturity_radar.png` - Radar chart visualization

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