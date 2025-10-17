/**
 * Google Apps Script for DevOps Maturity Survey Form Creation
 *
 * This script automatically creates a complete DevOps maturity survey form
 * with all questions, sections, and proper formatting for banking environments.
 *
 * Installation:
 * 1. Go to Google Forms
 * 2. Click "Blank" to create a new form
 * 3. Click the three dots (⋮) → "Script editor"
 * 4. Copy this entire script into the editor
 * 5. Save the script
 * 6. Run the createDevOpsSurveyForm() function
 */

// Survey configuration
const SURVEY_CONFIG = {
  title: "DevOps Maturity Assessment - Banking Environment",
  description: "This survey assesses your organization's DevOps maturity and DORA metrics implementation. Your responses will help identify areas for improvement and benchmark against industry standards.",
  requireSignIn: true,
  collectEmails: true
};

// Question definitions
const QUESTIONS = [
  // Section 1: About You
  {
    section: "About You",
    title: "What is your role in the organization?",
    type: FormApp.ItemType.MULTIPLE_CHOICE,
    required: true,
    choices: [
      "Developer/Engineer",
      "DevOps Engineer/SRE",
      "IT Operations/Infrastructure",
      "Security Engineer",
      "Compliance/Risk Management",
      "Project Manager",
      "IT Management",
      "Other"
    ]
  },
  {
    title: "How many years of experience do you have in software development/IT?",
    type: FormApp.ItemType.MULTIPLE_CHOICE,
    required: true,
    choices: ["< 1 year", "1-3 years", "3-5 years", "5-10 years", "10+ years"]
  },
  {
    title: "What is the size of your development team?",
    type: FormApp.ItemType.MULTIPLE_CHOICE,
    required: true,
    choices: ["1-5", "6-20", "21-50", "51-100", "100+"]
  },
  {
    title: "Which business domain does your team primarily support?",
    type: FormApp.ItemType.MULTIPLE_CHOICE,
    required: true,
    choices: [
      "Retail Banking",
      "Investment Banking",
      "Risk Management",
      "Compliance/Regulatory",
      "Payments/Transactions",
      "Core Banking Systems",
      "Digital Banking/Mobile",
      "Data Analytics/BI",
      "Other"
    ]
  },

  // Section 2: DevOps Culture
  {
    section: "DevOps Culture",
    title: "How would you rate the collaboration between development and operations teams?",
    type: FormApp.ItemType.SCALE,
    required: true,
    scale: { min: 1, max: 5, lowerLabel: "Poor collaboration", upperLabel: "Excellent collaboration" }
  },
  {
    title: "To what extent does your organization embrace a 'fail fast, learn fast' culture?",
    type: FormApp.ItemType.SCALE,
    required: true,
    scale: { min: 1, max: 5, lowerLabel: "Not at all", upperLabel: "Fully embraced" }
  },
  {
    title: "How frequently do development and operations teams work together on projects?",
    type: FormApp.ItemType.MULTIPLE_CHOICE,
    required: true,
    choices: ["Never", "Rarely", "Sometimes", "Often", "Always"]
  },
  {
    title: "Does your organization have cross-functional teams (DevOps/SRE model)?",
    type: FormApp.ItemType.MULTIPLE_CHOICE,
    required: true,
    choices: ["No", "Planning to implement", "Partially implemented", "Fully implemented"]
  },

  // Section 3: Deployment Practices
  {
    section: "Deployment Practices",
    title: "How frequently does your team deploy code to production?",
    type: FormApp.ItemType.MULTIPLE_CHOICE,
    required: true,
    choices: [
      "Fewer than once per month",
      "Once per month",
      "Once per week",
      "Multiple times per week",
      "On-demand (multiple times per day)"
    ]
  },
  {
    title: "What is the typical lead time from code commit to production deployment?",
    type: FormApp.ItemType.MULTIPLE_CHOICE,
    required: true,
    choices: [
      "More than 6 months",
      "1-6 months",
      "1 week - 1 month",
      "1 day - 1 week",
      "Less than 1 day"
    ]
  },
  {
    title: "How long does it typically take to restore service after an incident?",
    type: FormApp.ItemType.MULTIPLE_CHOICE,
    required: true,
    choices: [
      "More than 1 week",
      "1 day - 1 week",
      "1 hour - 1 day",
      "Less than 1 hour",
      "Less than 1 hour (automated)"
    ]
  },
  {
    title: "What percentage of deployments result in failures requiring rollback?",
    type: FormApp.ItemType.MULTIPLE_CHOICE,
    required: true,
    choices: ["60%+", "45-60%", "30-45%", "15-30%", "0-15%"]
  },
  {
    title: "What deployment strategy does your team primarily use?",
    type: FormApp.ItemType.MULTIPLE_CHOICE,
    required: true,
    choices: [
      "Manual deployments",
      "Automated deployments with manual approval",
      "Automated deployments with automated testing",
      "Continuous deployment",
      "GitOps/declarative deployments"
    ]
  },

  // Section 4: Monitoring & Observability
  {
    section: "Monitoring & Observability",
    title: "How comprehensive is your application monitoring?",
    type: FormApp.ItemType.SCALE,
    required: true,
    scale: { min: 1, max: 5, lowerLabel: "Basic logging only", upperLabel: "Full observability stack" }
  },
  {
    title: "Do you have automated alerting for production issues?",
    type: FormApp.ItemType.MULTIPLE_CHOICE,
    required: true,
    choices: ["No", "Basic alerts", "Comprehensive alerting", "AI-driven alerting"]
  },
  {
    title: "How do you track application performance metrics?",
    type: FormApp.ItemType.MULTIPLE_CHOICE,
    required: true,
    choices: [
      "Manual monitoring",
      "Basic dashboards",
      "Real-time dashboards with alerts",
      "AI/ML-based anomaly detection"
    ]
  },

  // Section 5: Security Practices
  {
    section: "Security Practices",
    title: "How is security integrated into your development process?",
    type: FormApp.ItemType.MULTIPLE_CHOICE,
    required: true,
    choices: [
      "Security as an afterthought",
      "Manual security reviews",
      "Automated security scanning",
      "DevSecOps with security champions",
      "Security by design/Shift-left security"
    ]
  },
  {
    title: "What security testing is performed before deployment?",
    type: FormApp.ItemType.CHECKBOX,
    required: true,
    choices: [
      "Static Application Security Testing (SAST)",
      "Dynamic Application Security Testing (DAST)",
      "Software Composition Analysis (SCA)",
      "Container security scanning",
      "Infrastructure as Code security",
      "None of the above"
    ]
  },

  // Section 6: Compliance & Audit
  {
    section: "Compliance & Audit",
    title: "How does your team handle regulatory compliance in deployments?",
    type: FormApp.ItemType.MULTIPLE_CHOICE,
    required: true,
    choices: [
      "Manual compliance checks",
      "Automated compliance validation",
      "Compliance as code",
      "Integrated compliance monitoring"
    ]
  },
  {
    title: "What audit capabilities do you have for deployment changes?",
    type: FormApp.ItemType.MULTIPLE_CHOICE,
    required: true,
    choices: [
      "Basic logging",
      "Change tracking",
      "Automated audit trails",
      "Real-time compliance monitoring"
    ]
  }
];

/**
 * Main function to create the DevOps maturity survey form
 */
function createDevOpsSurveyForm() {
  try {
    // Create the form
    const form = FormApp.create(SURVEY_CONFIG.title);
    form.setDescription(SURVEY_CONFIG.description);

    // Configure form settings
    form.setRequireLogin(SURVEY_CONFIG.requireSignIn);
    form.setCollectEmail(SURVEY_CONFIG.collectEmails);

    // Add questions
    let currentSection = null;
    let sectionBreak = null;

    for (const question of QUESTIONS) {
      // Add section break if needed
      if (question.section && question.section !== currentSection) {
        if (sectionBreak) {
          // Add some spacing after previous section
          form.addTextItem().setTitle(" ").setRequired(false);
        }

        sectionBreak = form.addPageBreakItem();
        sectionBreak.setTitle(question.section);
        currentSection = question.section;
      }

      // Create the appropriate question type
      let formItem;

      switch (question.type) {
        case FormApp.ItemType.MULTIPLE_CHOICE:
          formItem = form.addMultipleChoiceItem();
          const choiceItem = formItem.setChoiceValues(question.choices);
          break;

        case FormApp.ItemType.CHECKBOX:
          formItem = form.addCheckboxItem();
          formItem.setChoiceValues(question.choices);
          break;

        case FormApp.ItemType.SCALE:
          formItem = form.addScaleItem();
          formItem.setBounds(question.scale.min, question.scale.max);
          if (question.scale.lowerLabel) {
            formItem.setLabels(question.scale.lowerLabel, question.scale.upperLabel);
          }
          break;

        default:
          Logger.log(`Unsupported question type: ${question.type}`);
          continue;
      }

      // Set common properties
      formItem.setTitle(question.title);
      formItem.setRequired(question.required);
    }

    // Log completion
    Logger.log(`✅ DevOps Maturity Survey Form created successfully!`);
    Logger.log(`📋 Form URL: ${form.getPublishedUrl()}`);
    Logger.log(`🔗 Edit URL: ${form.getEditUrl()}`);
    Logger.log(`📊 Response URL: ${form.getSummaryUrl()}`);

    // Return form information
    return {
      formId: form.getId(),
      editUrl: form.getEditUrl(),
      publishedUrl: form.getPublishedUrl(),
      summaryUrl: form.getSummaryUrl()
    };

  } catch (error) {
    Logger.log(`❌ Error creating form: ${error.toString()}`);
    throw error;
  }
}

/**
 * Test function to verify the script works
 */
function testFormCreation() {
  Logger.log("🧪 Testing DevOps survey form creation...");
  const result = createDevOpsSurveyForm();
  Logger.log("✅ Test completed successfully!");
  return result;
}

/**
 * Function to delete the current form (for testing)
 */
function deleteCurrentForm() {
  const form = FormApp.getActiveForm();
  if (form) {
    DriveApp.getFileById(form.getId()).setTrashed(true);
    Logger.log("🗑️ Form deleted");
  }
}

/**
 * Get form information
 */
function getFormInfo() {
  const form = FormApp.getActiveForm();
  if (!form) {
    Logger.log("❌ No active form found. Run createDevOpsSurveyForm() first.");
    return;
  }

  Logger.log("📋 Form Information:");
  Logger.log(`Title: ${form.getTitle()}`);
  Logger.log(`ID: ${form.getId()}`);
  Logger.log(`Edit URL: ${form.getEditUrl()}`);
  Logger.log(`Published URL: ${form.getPublishedUrl()}`);
  Logger.log(`Responses: ${form.getResponses().length}`);
}