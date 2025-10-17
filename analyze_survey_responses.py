#!/usr/bin/env python3
"""
DevOps Maturity Survey Response Analyzer
======================================

This script analyzes responses from the DevOps maturity survey and generates:
- Maturity scores by category
- DORA metrics performance levels
- Radar charts for visualization
- Benchmarking against industry standards
- Excel dashboard with charts

Usage:
    python analyze_survey_responses.py responses.csv [output.xlsx]
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from math import pi
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.chart import RadarChart, Reference, Series
from openpyxl.drawing.image import Image
import seaborn as sns
from datetime import datetime
import sys
import os
from typing import Dict, List, Tuple, Optional

class SurveyAnalyzer:
    """Analyzes DevOps maturity survey responses"""

    def __init__(self):
        # DORA metrics scoring (higher score = better performance)
        self.dora_scoring = {
            "deployment_frequency": {
                "Fewer than once per month": 1,
                "Once per month": 2,
                "Once per week": 3,
                "Multiple times per week": 4,
                "On-demand (multiple times per day)": 5
            },
            "lead_time": {
                "More than 6 months": 1,
                "1-6 months": 2,
                "1 week - 1 month": 3,
                "1 day - 1 week": 4,
                "Less than 1 day": 5
            },
            "mttr": {
                "More than 1 week": 1,
                "1 day - 1 week": 2,
                "1 hour - 1 day": 3,
                "Less than 1 hour": 4,
                "Less than 1 hour (automated)": 5
            },
            "failure_rate": {
                "60%+": 1,
                "45-60%": 2,
                "30-45%": 3,
                "15-30%": 4,
                "0-15%": 5
            }
        }

        # Industry benchmarks (based on DORA research)
        self.benchmarks = {
            "Elite": {"deployment_frequency": 5, "lead_time": 5, "mttr": 5, "failure_rate": 5},
            "High": {"deployment_frequency": 4, "lead_time": 4, "mttr": 4, "failure_rate": 4},
            "Medium": {"deployment_frequency": 3, "lead_time": 3, "mttr": 3, "failure_rate": 3},
            "Low": {"deployment_frequency": 2, "lead_time": 2, "mttr": 2, "failure_rate": 2}
        }

        # Category weights for overall maturity score
        self.category_weights = {
            "culture": 0.25,
            "deployment_frequency": 0.20,
            "lead_time": 0.15,
            "mttr": 0.15,
            "failure_rate": 0.10,
            "monitoring": 0.05,
            "security": 0.05,
            "compliance": 0.05
        }

    def load_responses(self, csv_file: str) -> pd.DataFrame:
        """Load survey responses from CSV file"""
        try:
            df = pd.read_csv(csv_file)
            print(f"Loaded {len(df)} responses from {csv_file}")
            return df
        except Exception as e:
            print(f"Error loading CSV file: {e}")
            sys.exit(1)

    def clean_column_names(self, df: pd.DataFrame) -> pd.DataFrame:
        """Clean and standardize column names"""
        # Remove timestamp column if present
        df = df.drop(columns=[col for col in df.columns if 'timestamp' in col.lower()], errors='ignore')

        # Rename columns to more manageable names
        column_mapping = {}
        for i, col in enumerate(df.columns):
            if 'role' in col.lower():
                column_mapping[col] = 'role'
            elif 'experience' in col.lower():
                column_mapping[col] = 'experience'
            elif 'team size' in col.lower():
                column_mapping[col] = 'team_size'
            elif 'domain' in col.lower():
                column_mapping[col] = 'business_domain'
            elif 'collaboration' in col.lower():
                column_mapping[col] = 'devops_collaboration'
            elif 'fail fast' in col.lower():
                column_mapping[col] = 'fail_fast_culture'
            elif 'cross-functional' in col.lower():
                column_mapping[col] = 'cross_functional_teams'
            elif 'deploy' in col.lower() and 'frequency' in col.lower():
                column_mapping[col] = 'deployment_frequency'
            elif 'lead time' in col.lower():
                column_mapping[col] = 'lead_time'
            elif 'restore' in col.lower():
                column_mapping[col] = 'mttr'
            elif 'failure' in col.lower():
                column_mapping[col] = 'failure_rate'
            elif 'deployment strategy' in col.lower():
                column_mapping[col] = 'deployment_strategy'
            elif 'monitoring' in col.lower():
                column_mapping[col] = 'monitoring_comprehensiveness'
            elif 'alerting' in col.lower():
                column_mapping[col] = 'automated_alerting'
            elif 'performance' in col.lower():
                column_mapping[col] = 'performance_tracking'
            elif 'security' in col.lower() and 'integrated' in col.lower():
                column_mapping[col] = 'security_integration'
            elif 'security testing' in col.lower():
                column_mapping[col] = 'security_testing'
            elif 'compliance' in col.lower() and 'deployment' in col.lower():
                column_mapping[col] = 'compliance_handling'
            elif 'audit' in col.lower():
                column_mapping[col] = 'audit_capabilities'
            else:
                column_mapping[col] = f'q{i+1}'

        df = df.rename(columns=column_mapping)
        return df

    def calculate_maturity_scores(self, df: pd.DataFrame) -> Dict[str, float]:
        """Calculate maturity scores for each category"""
        scores = {}

        # DORA metrics scoring
        for metric, scoring_map in self.dora_scoring.items():
            if metric in df.columns:
                responses = df[metric].map(scoring_map).dropna()
                if len(responses) > 0:
                    scores[metric] = responses.mean()

        # Culture scoring
        culture_questions = ['devops_collaboration', 'fail_fast_culture', 'cross_functional_teams']
        culture_scores = []
        for col in culture_questions:
            if col in df.columns:
                if col == 'devops_collaboration':
                    score_map = {'Poor collaboration': 1, 'Excellent collaboration': 5}
                    responses = df[col].map(score_map).dropna()
                elif col == 'fail_fast_culture':
                    score_map = {'Not at all': 1, 'Fully embraced': 5}
                    responses = df[col].map(score_map).dropna()
                elif col == 'cross_functional_teams':
                    score_map = {'No': 1, 'Planning to implement': 2, 'Partially implemented': 3, 'Fully implemented': 4}
                    responses = df[col].map(score_map).dropna()
                if len(responses) > 0:
                    culture_scores.append(responses.mean())

        if culture_scores:
            scores['culture'] = np.mean(culture_scores)

        # Monitoring scoring
        monitoring_questions = ['monitoring_comprehensiveness', 'automated_alerting', 'performance_tracking']
        monitoring_scores = []
        for col in monitoring_questions:
            if col in df.columns:
                if col == 'monitoring_comprehensiveness':
                    score_map = {'Basic logging only': 1, 'Full observability stack': 5}
                    responses = df[col].map(score_map).dropna()
                elif col == 'automated_alerting':
                    score_map = {'No': 1, 'Basic alerts': 2, 'Comprehensive alerting': 4, 'AI-driven alerting': 5}
                    responses = df[col].map(score_map).dropna()
                elif col == 'performance_tracking':
                    score_map = {'Manual monitoring': 1, 'Basic dashboards': 2, 'Real-time dashboards with alerts': 4, 'AI/ML-based anomaly detection': 5}
                    responses = df[col].map(score_map).dropna()
                if len(responses) > 0:
                    monitoring_scores.append(responses.mean())

        if monitoring_scores:
            scores['monitoring'] = np.mean(monitoring_scores)

        # Security scoring
        if 'security_integration' in df.columns:
            security_map = {
                'Security as an afterthought': 1,
                'Manual security reviews': 2,
                'Automated security scanning': 3,
                'DevSecOps with security champions': 4,
                'Security by design/Shift-left security': 5
            }
            responses = df['security_integration'].map(security_map).dropna()
            if len(responses) > 0:
                scores['security'] = responses.mean()

        # Compliance scoring
        compliance_questions = ['compliance_handling', 'audit_capabilities']
        compliance_scores = []
        for col in compliance_questions:
            if col in df.columns:
                if col == 'compliance_handling':
                    score_map = {
                        'Manual compliance checks': 1,
                        'Automated compliance validation': 3,
                        'Compliance as code': 4,
                        'Integrated compliance monitoring': 5
                    }
                    responses = df[col].map(score_map).dropna()
                elif col == 'audit_capabilities':
                    score_map = {
                        'Basic logging': 1,
                        'Change tracking': 2,
                        'Automated audit trails': 4,
                        'Real-time compliance monitoring': 5
                    }
                    responses = df[col].map(score_map).dropna()
                if len(responses) > 0:
                    compliance_scores.append(responses.mean())

        if compliance_scores:
            scores['compliance'] = np.mean(compliance_scores)

        return scores

    def calculate_overall_maturity(self, scores: Dict[str, float]) -> float:
        """Calculate overall maturity score"""
        weighted_sum = 0
        total_weight = 0

        for category, score in scores.items():
            if category in self.category_weights:
                weighted_sum += score * self.category_weights[category]
                total_weight += self.category_weights[category]

        return weighted_sum / total_weight if total_weight > 0 else 0

    def determine_performance_level(self, score: float) -> str:
        """Determine performance level based on score"""
        if score >= 4.5:
            return "Elite"
        elif score >= 3.5:
            return "High"
        elif score >= 2.5:
            return "Medium"
        elif score >= 1.5:
            return "Low"
        else:
            return "Initial"

    def create_radar_chart(self, scores: Dict[str, float], output_file: str = "radar_chart.png"):
        """Create radar chart visualization"""
        # Prepare data for radar chart
        categories = ['Culture', 'Deployment\nFrequency', 'Lead Time', 'MTTR', 'Failure\nRate', 'Monitoring', 'Security', 'Compliance']
        category_keys = ['culture', 'deployment_frequency', 'lead_time', 'mttr', 'failure_rate', 'monitoring', 'security', 'compliance']

        values = []
        for key in category_keys:
            values.append(scores.get(key, 0))

        # Add first value again to close the radar chart
        values += values[:1]
        categories += categories[:1]

        # Create radar chart
        angles = [n / float(len(categories[:-1])) * 2 * pi for n in range(len(categories[:-1]))]
        angles += angles[:1]

        fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(projection='polar'))

        # Plot data
        ax.plot(angles, values, 'o-', linewidth=2, label='Your Organization', color='#1f77b4')
        ax.fill(angles, values, alpha=0.25, color='#1f77b4')

        # Add benchmark lines
        for level, benchmark_scores in self.benchmarks.items():
            benchmark_values = []
            for key in category_keys:
                benchmark_values.append(benchmark_scores.get(key, 3))
            benchmark_values += benchmark_values[:1]

            color_map = {'Elite': '#2ca02c', 'High': '#ff7f0e', 'Medium': '#7f7f7f', 'Low': '#d62728'}
            ax.plot(angles, benchmark_values, '--', linewidth=1, label=f'{level} Performers', color=color_map.get(level, '#7f7f7f'))

        # Set labels
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(categories[:-1])
        ax.set_ylim(0, 5)
        ax.set_yticks([1, 2, 3, 4, 5])
        ax.set_yticklabels(['1', '2', '3', '4', '5'])
        ax.set_title('DevOps Maturity Assessment\n(Banking Environment)', size=16, fontweight='bold', pad=20)

        # Add legend
        ax.legend(loc='upper right', bbox_to_anchor=(1.2, 1.0))

        plt.tight_layout()
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        plt.close()

        print(f"Radar chart saved to {output_file}")

    def create_excel_dashboard(self, df: pd.DataFrame, scores: Dict[str, float], output_file: str = "devops_maturity_dashboard.xlsx"):
        """Create comprehensive Excel dashboard"""
        workbook = openpyxl.Workbook()

        # Summary sheet
        summary_sheet = workbook.active
        summary_sheet.title = "Summary"

        # Title
        summary_sheet['A1'] = "DevOps Maturity Assessment Dashboard"
        summary_sheet['A1'].font = Font(size=16, bold=True)
        summary_sheet.merge_cells('A1:E1')

        # Metadata
        summary_sheet['A3'] = "Report Generated:"
        summary_sheet['B3'] = datetime.now().strftime("%Y-%m-%d %H:%M")
        summary_sheet['A4'] = "Total Responses:"
        summary_sheet['B4'] = len(df)
        summary_sheet['A5'] = "Overall Maturity Score:"
        summary_sheet['B5'] = f"{self.calculate_overall_maturity(scores):.2f}/5.00"
        summary_sheet['A6'] = "Performance Level:"
        summary_sheet['B6'] = self.determine_performance_level(self.calculate_overall_maturity(scores))

        # Style metadata
        for row in range(3, 7):
            summary_sheet[f'A{row}'].font = Font(bold=True)
            summary_sheet[f'B{row}'].font = Font(bold=True)

        # Scores table
        summary_sheet['A9'] = "Category Scores"
        summary_sheet['A9'].font = Font(size=14, bold=True)
        summary_sheet.merge_cells('A9:B9')

        summary_sheet['A10'] = "Category"
        summary_sheet['B10'] = "Score"
        summary_sheet['C10'] = "Level"
        summary_sheet['D10'] = "Benchmark"

        # Header styling
        header_fill = PatternFill(start_color="CCCCCC", end_color="CCCCCC", fill_type="solid")
        for col in ['A10', 'B10', 'C10', 'D10']:
            summary_sheet[col].fill = header_fill
            summary_sheet[col].font = Font(bold=True)

        # Add scores
        categories_display = {
            'culture': 'Culture & Collaboration',
            'deployment_frequency': 'Deployment Frequency',
            'lead_time': 'Lead Time for Changes',
            'mttr': 'Mean Time to Restore',
            'failure_rate': 'Change Failure Rate',
            'monitoring': 'Monitoring & Observability',
            'security': 'Security Practices',
            'compliance': 'Compliance & Audit'
        }

        row = 11
        for category, display_name in categories_display.items():
            score = scores.get(category, 0)
            level = self.determine_performance_level(score)

            summary_sheet[f'A{row}'] = display_name
            summary_sheet[f'B{row}'] = f"{score:.2f}"
            summary_sheet[f'C{row}'] = level
            summary_sheet[f'D{row}'] = self.get_benchmark_comparison(category, score)

            row += 1

        # Demographics sheet
        demo_sheet = workbook.create_sheet("Demographics")
        self.create_demographics_analysis(demo_sheet, df)

        # DORA Metrics sheet
        dora_sheet = workbook.create_sheet("DORA Metrics")
        self.create_dora_analysis(dora_sheet, df)

        # Recommendations sheet
        rec_sheet = workbook.create_sheet("Recommendations")
        self.create_recommendations(rec_sheet, scores)

        # Save workbook
        workbook.save(output_file)
        print(f"Excel dashboard saved to {output_file}")

    def create_demographics_analysis(self, sheet, df: pd.DataFrame):
        """Create demographics analysis sheet"""
        sheet['A1'] = "Demographics Analysis"
        sheet['A1'].font = Font(size=14, bold=True)

        # Role distribution
        if 'role' in df.columns:
            sheet['A3'] = "Role Distribution"
            sheet['A3'].font = Font(bold=True)

            role_counts = df['role'].value_counts()
            row = 4
            for role, count in role_counts.items():
                sheet[f'A{row}'] = role
                sheet[f'B{row}'] = count
                row += 1

        # Experience distribution
        if 'experience' in df.columns:
            sheet['D3'] = "Experience Distribution"
            sheet['D3'].font = Font(bold=True)

            exp_counts = df['experience'].value_counts()
            row = 4
            for exp, count in exp_counts.items():
                sheet[f'D{row}'] = exp
                sheet[f'E{row}'] = count
                row += 1

    def create_dora_analysis(self, sheet, df: pd.DataFrame):
        """Create DORA metrics analysis sheet"""
        sheet['A1'] = "DORA Metrics Analysis"
        sheet['A1'].font = Font(size=14, bold=True)

        dora_metrics = ['deployment_frequency', 'lead_time', 'mttr', 'failure_rate']
        dora_display = {
            'deployment_frequency': 'Deployment Frequency',
            'lead_time': 'Lead Time for Changes',
            'mttr': 'Mean Time to Restore',
            'failure_rate': 'Change Failure Rate'
        }

        row = 3
        for metric in dora_metrics:
            if metric in df.columns:
                sheet[f'A{row}'] = dora_display[metric]
                sheet[f'A{row}'].font = Font(bold=True)

                responses = df[metric].value_counts()
                sub_row = row + 1
                for response, count in responses.items():
                    sheet[f'A{sub_row}'] = response
                    sheet[f'B{sub_row}'] = count
                    sub_row += 1

                row = sub_row + 1

    def create_recommendations(self, sheet, scores: Dict[str, float]):
        """Create recommendations sheet based on scores"""
        sheet['A1'] = "Improvement Recommendations"
        sheet['A1'].font = Font(size=14, bold=True)

        recommendations = {
            'culture': {
                'low': [
                    "Establish regular cross-functional meetings between dev and ops",
                    "Implement shared goals and metrics",
                    "Create DevOps champions program"
                ],
                'high': ["Continue strengthening collaboration practices"]
            },
            'deployment_frequency': {
                'low': [
                    "Implement CI/CD pipelines",
                    "Adopt trunk-based development",
                    "Automate testing and deployment processes"
                ],
                'high': ["Focus on deployment quality and stability"]
            },
            'lead_time': {
                'low': [
                    "Streamline code review processes",
                    "Implement feature flags",
                    "Automate integration testing"
                ],
                'high': ["Maintain current rapid delivery capabilities"]
            },
            'mttr': {
                'low': [
                    "Implement comprehensive monitoring",
                    "Create incident response playbooks",
                    "Automate rollback procedures"
                ],
                'high': ["Continue improving incident response processes"]
            },
            'failure_rate': {
                'low': [
                    "Enhance automated testing coverage",
                    "Implement canary deployments",
                    "Improve code quality gates"
                ],
                'high': ["Maintain low failure rate through quality practices"]
            }
        }

        row = 3
        for category, score in scores.items():
            if category in recommendations:
                level = 'low' if score < 3.5 else 'high'
                sheet[f'A{row}'] = category.replace('_', ' ').title()
                sheet[f'A{row}'].font = Font(bold=True)

                for rec in recommendations[category][level]:
                    row += 1
                    sheet[f'A{row}'] = f"• {rec}"

                row += 2

    def get_benchmark_comparison(self, category: str, score: float) -> str:
        """Compare score against benchmarks"""
        if category in ['deployment_frequency', 'lead_time', 'mttr', 'failure_rate']:
            benchmark = self.benchmarks
            if score >= 4.5:
                return "Elite Performer"
            elif score >= 3.5:
                return "High Performer"
            elif score >= 2.5:
                return "Medium Performer"
            elif score >= 1.5:
                return "Low Performer"
            else:
                return "Initial Stage"
        return "N/A"

def main():
    if len(sys.argv) < 2:
        print("Usage: python analyze_survey_responses.py <responses.csv> [output.xlsx]")
        sys.exit(1)

    csv_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else "devops_maturity_dashboard.xlsx"

    analyzer = SurveyAnalyzer()

    # Load and clean data
    df = analyzer.load_responses(csv_file)
    df = analyzer.clean_column_names(df)

    # Calculate scores
    scores = analyzer.calculate_maturity_scores(df)
    print(f"Calculated maturity scores: {scores}")

    overall_score = analyzer.calculate_overall_maturity(scores)
    performance_level = analyzer.determine_performance_level(overall_score)

    print(".2f")
    print(f"Performance Level: {performance_level}")

    # Create visualizations
    analyzer.create_radar_chart(scores, "devops_maturity_radar.png")

    # Create Excel dashboard
    analyzer.create_excel_dashboard(df, scores, output_file)

    print("\nAnalysis complete! Generated files:")
    print(f"- {output_file} (Excel dashboard)")
    print("- devops_maturity_radar.png (Radar chart)")

if __name__ == "__main__":
    main()