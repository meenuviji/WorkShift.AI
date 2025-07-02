# WorkShift.AI - Automation Risk Analyzer
# Analyzes AI/automation risk for tech jobs based on multiple factors

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import os
import warnings
warnings.filterwarnings('ignore')

class AutomationRiskAnalyzer:
    """
    Analyzes automation risk for tech jobs based on:
    - Task composition (routine vs creative)
    - Technical complexity
    - Human interaction requirements
    - Current AI capabilities
    """
    
    def __init__(self, job_data_path=None):
        """Initialize the automation risk analyzer"""
        self.job_data_path = job_data_path
        self.df = None
        
        # Define risk factors and weights
        self.risk_factors = {
            'routine_tasks': 0.30,
            'data_processing': 0.20,
            'human_interaction': -0.25,
            'creative_problem_solving': -0.30,
            'technical_complexity': -0.15,
            'physical_presence': -0.10
        }
        
        # Initialize risk profiles
        self._initialize_risk_profiles()
        
        # AI capability timeline
        self.ai_timeline = {
            'current': ['Data entry', 'Basic testing', 'Simple analysis'],
            '2025-2027': ['Complex testing', 'Report generation', 'Code review'],
            '2028-2030': ['Basic coding', 'Data pipeline creation', 'Architecture design'],
            '2030+': ['Complex problem solving', 'Strategic planning', 'Innovation']
        }
        
        # Create necessary directories
        os.makedirs('data/processed', exist_ok=True)
        
        if job_data_path:
            self.load_job_data()
    
    def _initialize_risk_profiles(self):
        """Initialize role-specific risk profiles"""
        self.role_risk_profiles = {
            'Data Entry': {
                'routine_tasks': 0.95, 'data_processing': 0.90, 'human_interaction': 0.10,
                'creative_problem_solving': 0.05, 'technical_complexity': 0.20,
                'physical_presence': 0.05, 'base_risk': 0.85
            },
            'QA Tester': {
                'routine_tasks': 0.70, 'data_processing': 0.60, 'human_interaction': 0.30,
                'creative_problem_solving': 0.30, 'technical_complexity': 0.40,
                'physical_presence': 0.10, 'base_risk': 0.65
            },
            'Data Analyst': {
                'routine_tasks': 0.60, 'data_processing': 0.85, 'human_interaction': 0.40,
                'creative_problem_solving': 0.50, 'technical_complexity': 0.60,
                'physical_presence': 0.05, 'base_risk': 0.55
            },
            'Frontend Developer': {
                'routine_tasks': 0.50, 'data_processing': 0.40, 'human_interaction': 0.50,
                'creative_problem_solving': 0.70, 'technical_complexity': 0.70,
                'physical_presence': 0.05, 'base_risk': 0.35
            },
            'Backend Developer': {
                'routine_tasks': 0.55, 'data_processing': 0.60, 'human_interaction': 0.35,
                'creative_problem_solving': 0.65, 'technical_complexity': 0.80,
                'physical_presence': 0.05, 'base_risk': 0.40
            },
            'Full Stack Developer': {
                'routine_tasks': 0.45, 'data_processing': 0.50, 'human_interaction': 0.45,
                'creative_problem_solving': 0.75, 'technical_complexity': 0.85,
                'physical_presence': 0.05, 'base_risk': 0.30
            },
            'DevOps Engineer': {
                'routine_tasks': 0.65, 'data_processing': 0.55, 'human_interaction': 0.40,
                'creative_problem_solving': 0.60, 'technical_complexity': 0.90,
                'physical_presence': 0.10, 'base_risk': 0.45
            },
            'Machine Learning Engineer': {
                'routine_tasks': 0.40, 'data_processing': 0.80, 'human_interaction': 0.35,
                'creative_problem_solving': 0.85, 'technical_complexity': 0.95,
                'physical_presence': 0.05, 'base_risk': 0.25
            },
            'Data Scientist': {
                'routine_tasks': 0.35, 'data_processing': 0.85, 'human_interaction': 0.45,
                'creative_problem_solving': 0.90, 'technical_complexity': 0.90,
                'physical_presence': 0.05, 'base_risk': 0.20
            },
            'Software Engineer': {
                'routine_tasks': 0.40, 'data_processing': 0.50, 'human_interaction': 0.50,
                'creative_problem_solving': 0.80, 'technical_complexity': 0.85,
                'physical_presence': 0.05, 'base_risk': 0.25
            },
            'Cloud Engineer': {
                'routine_tasks': 0.55, 'data_processing': 0.50, 'human_interaction': 0.35,
                'creative_problem_solving': 0.65, 'technical_complexity': 0.85,
                'physical_presence': 0.05, 'base_risk': 0.40
            },
            'Security Engineer': {
                'routine_tasks': 0.45, 'data_processing': 0.60, 'human_interaction': 0.40,
                'creative_problem_solving': 0.80, 'technical_complexity': 0.90,
                'physical_presence': 0.10, 'base_risk': 0.30
            },
            'Product Manager': {
                'routine_tasks': 0.30, 'data_processing': 0.40, 'human_interaction': 0.90,
                'creative_problem_solving': 0.85, 'technical_complexity': 0.50,
                'physical_presence': 0.40, 'base_risk': 0.15
            },
            'Engineering Manager': {
                'routine_tasks': 0.25, 'data_processing': 0.30, 'human_interaction': 0.95,
                'creative_problem_solving': 0.80, 'technical_complexity': 0.60,
                'physical_presence': 0.50, 'base_risk': 0.10
            }
        }
    
    def load_job_data(self):
        """Load job data from CSV"""
        try:
            self.df = pd.read_csv(self.job_data_path)
            print(f"✓ Loaded {len(self.df):,} job records")
            self.df['risk_category'] = self.df['search_term'].map(self.map_to_risk_category)
        except FileNotFoundError:
            print(f"✗ File not found: {self.job_data_path}")
        except Exception as e:
            print(f"✗ Error loading data: {e}")
    
    def map_to_risk_category(self, job_title):
        """Map job titles to risk categories"""
        title_lower = job_title.lower()
        
        mappings = {
            'data scientist': 'Data Scientist',
            'machine learning': 'Machine Learning Engineer',
            'product manager': 'Product Manager',
            'devops': 'DevOps Engineer',
            'frontend': 'Frontend Developer',
            'backend': 'Backend Developer',
            'full stack': 'Full Stack Developer',
            'software engineer': 'Software Engineer',
            'software developer': 'Software Engineer',
            'cloud engineer': 'Cloud Engineer',
            'security engineer': 'Security Engineer',
            'data analyst': 'Data Analyst'
        }
        
        for keyword, category in mappings.items():
            if keyword in title_lower:
                return category
        return 'Software Engineer'
    
    def calculate_automation_risk(self, role):
        """Calculate automation risk score for a role"""
        if role not in self.role_risk_profiles:
            return 0.5
        
        profile = self.role_risk_profiles[role]
        risk_score = profile['base_risk']
        
        # Apply weighted factors
        for factor, weight in self.risk_factors.items():
            if factor in profile:
                risk_score += weight * (profile[factor] - 0.5)
        
        return max(0, min(1, risk_score))
    
    def get_risk_level(self, score):
        """Convert risk score to risk level"""
        if score >= 0.7: return "Very High"
        elif score >= 0.5: return "High"
        elif score >= 0.3: return "Medium"
        elif score >= 0.15: return "Low"
        else: return "Very Low"
    
    def analyze_risk_by_role(self):
        """Analyze automation risk for all roles"""
        print("\n" + "="*60)
        print("AUTOMATION RISK ANALYSIS BY ROLE")
        print("="*60)
        
        risk_data = []
        for role, profile in self.role_risk_profiles.items():
            risk_score = self.calculate_automation_risk(role)
            risk_data.append({
                'Role': role,
                'Risk Score': risk_score,
                'Risk Level': self.get_risk_level(risk_score),
                'Routine Tasks': profile['routine_tasks'],
                'Human Interaction': profile['human_interaction'],
                'Creative Problem Solving': profile['creative_problem_solving']
            })
        
        risk_df = pd.DataFrame(risk_data).sort_values('Risk Score', ascending=False)
        
        print("\nAutomation Risk Rankings:")
        print("-" * 60)
        for _, row in risk_df.iterrows():
            print(f"{row['Role']:25} | Risk: {row['Risk Score']:.2f} ({row['Risk Level']})")
        
        return risk_df
    
    def analyze_risk_factors(self):
        """Analyze which factors contribute most to automation risk"""
        print("\n" + "="*60)
        print("KEY AUTOMATION RISK FACTORS")
        print("="*60)
        
        print("\nFactors that INCREASE automation risk:")
        print("• Routine, repetitive tasks (30% weight)")
        print("• Heavy data processing work (20% weight)")
        
        print("\nFactors that DECREASE automation risk:")
        print("• High human interaction needs (-25% weight)")
        print("• Creative problem solving (-30% weight)")
        print("• Technical complexity (-15% weight)")
        print("• Physical presence requirements (-10% weight)")
    
    def analyze_timeline_impact(self):
        """Analyze automation impact over time"""
        print("\n" + "="*60)
        print("AI AUTOMATION TIMELINE")
        print("="*60)
        
        for period, capabilities in self.ai_timeline.items():
            print(f"\n{period}:")
            for capability in capabilities:
                print(f"  • {capability}")
        
        print("\n" + "="*60)
        print("ESTIMATED JOB IMPACT BY PERIOD")
        print("="*60)
        
        impact_timeline = {
            'Current (2024)': ['Data Entry', 'QA Tester'],
            '2025-2027': ['Data Analyst', 'DevOps Engineer (partial)'],
            '2028-2030': ['Backend Developer (partial)', 'Frontend Developer (partial)'],
            '2030+': ['Limited impact on creative/leadership roles']
        }
        
        for period, roles in impact_timeline.items():
            print(f"\n{period}:")
            for role in roles:
                print(f"  • {role}")
    
    def analyze_mitigation_strategies(self):
        """Suggest mitigation strategies for different risk levels"""
        print("\n" + "="*60)
        print("RISK MITIGATION STRATEGIES")
        print("="*60)
        
        strategies = {
            'Very High Risk': [
                'Immediate upskilling to more complex roles',
                'Focus on creative and strategic aspects',
                'Develop strong human interaction skills',
                'Consider role transition within 1-2 years'
            ],
            'High Risk': [
                'Start learning AI/ML to work alongside automation',
                'Develop expertise in system design and architecture',
                'Focus on complex problem-solving skills',
                'Build domain expertise that AI cannot easily replicate'
            ],
            'Medium Risk': [
                'Enhance creative and strategic thinking abilities',
                'Develop leadership and communication skills',
                'Learn to manage and optimize AI systems',
                'Focus on cross-functional collaboration'
            ],
            'Low Risk': [
                'Stay updated with AI developments in your field',
                'Learn to leverage AI tools for productivity',
                'Focus on innovation and creative solutions',
                'Develop unique expertise and specializations'
            ]
        }
        
        for risk_level, strategy_list in strategies.items():
            print(f"\n{risk_level} Roles:")
            for strategy in strategy_list:
                print(f"  • {strategy}")
    
    def create_risk_visualizations(self):
        """Create comprehensive risk visualization dashboard"""
        print("\n" + "="*60)
        print("CREATING RISK VISUALIZATIONS")
        print("="*60)
        
        risk_df = pd.DataFrame([
            {
                'Role': role,
                'Risk Score': self.calculate_automation_risk(role),
                'Risk Level': self.get_risk_level(self.calculate_automation_risk(role))
            }
            for role in self.role_risk_profiles
        ]).sort_values('Risk Score', ascending=False)
        
        # Create visualization
        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        fig.suptitle('WorkShift.AI - Automation Risk Analysis Dashboard', fontsize=18, fontweight='bold')
        
        # 1. Risk Score by Role
        ax1 = axes[0, 0]
        colors = ['#d62728' if s >= 0.7 else '#ff7f0e' if s >= 0.5 else '#ffdb58' if s >= 0.3 else '#2ca02c' 
                  for s in risk_df['Risk Score']]
        
        bars = ax1.barh(risk_df['Role'], risk_df['Risk Score'], color=colors)
        ax1.set_xlabel('Automation Risk Score')
        ax1.set_title('Automation Risk by Role', fontsize=14, fontweight='bold')
        ax1.set_xlim(0, 1)
        ax1.grid(axis='x', alpha=0.3)
        
        # Add value labels
        for i, (idx, row) in enumerate(risk_df.iterrows()):
            ax1.text(row['Risk Score'] + 0.01, i, f'{row["Risk Score"]:.2f}', va='center')
        
        # 2. Risk Distribution
        ax2 = axes[0, 1]
        risk_levels = risk_df['Risk Level'].value_counts()
        colors_pie = {'Very High': '#d62728', 'High': '#ff7f0e', 'Medium': '#ffdb58', 
                     'Low': '#2ca02c', 'Very Low': '#1f77b4'}
        pie_colors = [colors_pie.get(level, '#gray') for level in risk_levels.index]
        
        ax2.pie(risk_levels.values, labels=risk_levels.index, autopct='%1.1f%%', 
                colors=pie_colors, startangle=90)
        ax2.set_title('Distribution of Risk Levels', fontsize=14, fontweight='bold')
        
        # 3. Risk Factors Comparison
        ax3 = axes[1, 0]
        sample_roles = ['Data Entry', 'Data Analyst', 'Software Engineer', 'Product Manager']
        factors = ['Routine Tasks', 'Human Interaction', 'Creative Problem Solving']
        
        x = np.arange(len(sample_roles))
        width = 0.25
        
        for i, factor in enumerate(factors):
            values = [self.role_risk_profiles[role][factor.lower().replace(' ', '_')] 
                     for role in sample_roles]
            ax3.bar(x + i*width, values, width, label=factor)
        
        ax3.set_xlabel('Role')
        ax3.set_ylabel('Factor Score')
        ax3.set_title('Key Risk Factors by Role', fontsize=14, fontweight='bold')
        ax3.set_xticks(x + width)
        ax3.set_xticklabels(sample_roles, rotation=45, ha='right')
        ax3.legend()
        ax3.grid(axis='y', alpha=0.3)
        
        # 4. Timeline Impact
        ax4 = axes[1, 1]
        timeline_data = {
            'Current': 15,
            '2025-2027': 35,
            '2028-2030': 25,
            '2030+': 25
        }
        
        bars = ax4.bar(timeline_data.keys(), timeline_data.values(), 
                       color=['#1f77b4', '#ff7f0e', '#ffdb58', '#2ca02c'])
        ax4.set_ylabel('Estimated % of Roles Affected')
        ax4.set_title('Automation Impact Timeline', fontsize=14, fontweight='bold')
        ax4.set_ylim(0, 50)
        ax4.grid(axis='y', alpha=0.3)
        
        # Add value labels
        for bar in bars:
            height = bar.get_height()
            ax4.text(bar.get_x() + bar.get_width()/2., height + 1,
                    f'{height}%', ha='center', va='bottom')
        
        plt.tight_layout()
        
        # Save visualization
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        viz_filename = f"data/processed/automation_risk_analysis_{timestamp}.png"
        plt.savefig(viz_filename, dpi=300, bbox_inches='tight')
        print(f"\n✓ Visualization saved: {viz_filename}")
        
        return viz_filename
    
    def generate_risk_report(self):
        """Generate comprehensive automation risk report"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        report_filename = f"data/processed/automation_risk_report_{timestamp}.txt"
        
        with open(report_filename, 'w') as f:
            f.write("WorkShift.AI - Automation Risk Analysis Report\n")
            f.write(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("="*60 + "\n\n")
            
            # Risk rankings
            risk_df = pd.DataFrame([
                {
                    'Role': role,
                    'Risk Score': self.calculate_automation_risk(role),
                    'Risk Level': self.get_risk_level(self.calculate_automation_risk(role))
                }
                for role in self.role_risk_profiles
            ]).sort_values('Risk Score', ascending=False)
            
            f.write("AUTOMATION RISK RANKINGS\n")
            f.write("-"*60 + "\n")
            for _, row in risk_df.iterrows():
                f.write(f"{row['Role']:25} | Risk: {row['Risk Score']:.2f} ({row['Risk Level']})\n")
            
            f.write("\n" + "="*60 + "\n")
            f.write("END OF REPORT\n")
        
        print(f"\n✓ Report saved: {report_filename}")
        return report_filename
    
    def export_risk_data(self):
        """Export risk data for integration with main analysis"""
        risk_data = []
        
        for role, profile in self.role_risk_profiles.items():
            risk_score = self.calculate_automation_risk(role)
            risk_data.append({
                'role': role,
                'automation_risk_score': risk_score,
                'risk_level': self.get_risk_level(risk_score),
                'routine_tasks': profile['routine_tasks'],
                'human_interaction': profile['human_interaction'],
                'creative_problem_solving': profile['creative_problem_solving'],
                'technical_complexity': profile['technical_complexity']
            })
        
        risk_df = pd.DataFrame(risk_data)
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        export_filename = f"data/processed/automation_risk_scores_{timestamp}.csv"
        risk_df.to_csv(export_filename, index=False)
        
        print(f"\n✓ Risk data exported: {export_filename}")
        return risk_df
    
    def run_complete_analysis(self):
        """Run complete automation risk analysis"""
        print("\n" + "="*60)
        print("WORKSHIFT.AI - AUTOMATION RISK ANALYSIS")
        print("="*60)
        print("Analyzing AI/automation risk for tech jobs...")
        
        # Run all analyses
        self.analyze_risk_by_role()
        self.analyze_risk_factors()
        self.analyze_timeline_impact()
        self.analyze_mitigation_strategies()
        
        # Create visualizations
        self.create_risk_visualizations()
        
        # Generate outputs
        self.generate_risk_report()
        self.export_risk_data()
        
        print("\n" + "="*60)
        print("✓ Automation Risk Analysis Complete!")
        print("="*60)


if __name__ == "__main__":
    # Run with job data if available
    if os.path.exists('data/raw/consolidated_jobs.csv'):
        analyzer = AutomationRiskAnalyzer('data/raw/consolidated_jobs.csv')
    else:
        # Run standalone analysis
        analyzer = AutomationRiskAnalyzer()
    
    analyzer.run_complete_analysis()