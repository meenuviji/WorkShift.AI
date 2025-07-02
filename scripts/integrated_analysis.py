# WorkShift.AI - Integrated Analysis
# Combines job market data with automation risk analysis

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import os
import sys
import warnings
warnings.filterwarnings('ignore')

# Set plotting style
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

class IntegratedWorkShiftAnalysis:
    """
    Integrates job market analysis with automation risk assessment
    to provide comprehensive insights
    """
    
    def __init__(self, job_data_path):
        """Initialize integrated analysis"""
        self.job_data_path = job_data_path
        
        # Check if data file exists
        if not os.path.exists(job_data_path):
            print(f"Error: Data file not found: {job_data_path}")
            print("Please ensure you have job data in the data/raw folder.")
            return
        
        # Initialize analyzers
        print("Initializing analyzers...")
        try:
            # Import the analyzers
            from job_market_analysis import JobMarketAnalyzer
            from automation_risk_analyzer import AutomationRiskAnalyzer
            
            self.market_analyzer = JobMarketAnalyzer(job_data_path)
            self.risk_analyzer = AutomationRiskAnalyzer(job_data_path)
        except ImportError as e:
            print(f"Error importing modules: {e}")
            print("Make sure job_market_analysis.py and automation_risk_analyzer.py are in the scripts folder")
            sys.exit(1)
        
        # Store integrated results
        self.integrated_df = None
    
    def create_integrated_dataset(self):
        """Merge job market data with automation risk scores"""
        print("\nCreating integrated dataset...")
        
        # Get job market data
        market_df = self.market_analyzer.df.copy()
        
        # Create risk_category mapping function
        def map_to_risk_category(job_title):
            """Map job titles to risk categories"""
            if pd.isna(job_title):
                return 'Software Engineer'
                
            title_lower = str(job_title).lower()
            
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
            return 'Software Engineer'  # Default
        
        # Apply the mapping to create risk_category column
        market_df['risk_category'] = market_df['search_term'].apply(map_to_risk_category)
        
        # Get automation risk scores
        risk_scores = {}
        for role in self.risk_analyzer.role_risk_profiles:
            risk_scores[role] = {
                'automation_risk_score': self.risk_analyzer.calculate_automation_risk(role),
                'risk_level': self.risk_analyzer.get_risk_level(
                    self.risk_analyzer.calculate_automation_risk(role)
                )
            }
        
        # Map risk scores to job data
        market_df['automation_risk_score'] = market_df['risk_category'].map(
            lambda x: risk_scores.get(x, {}).get('automation_risk_score', 0.5)
        )
        market_df['risk_level'] = market_df['risk_category'].map(
            lambda x: risk_scores.get(x, {}).get('risk_level', 'Medium')
        )
        
        self.integrated_df = market_df
        print(f"✓ Integrated dataset created with {len(self.integrated_df):,} records")
        
        return self.integrated_df
    
    def analyze_salary_vs_risk(self):
        """Analyze relationship between salary and automation risk"""
        print("\n" + "="*60)
        print("SALARY VS AUTOMATION RISK ANALYSIS")
        print("="*60)
        
        # Filter for jobs with salary data
        salary_risk_df = self.integrated_df.dropna(subset=['salary_avg'])
        
        if len(salary_risk_df) == 0:
            print("No salary data available for risk analysis")
            return
        
        # Group by risk category
        risk_salary = salary_risk_df.groupby('risk_category').agg({
            'salary_avg': 'mean',
            'automation_risk_score': 'first',
            'title': 'count'
        }).round(0)
        
        risk_salary.columns = ['avg_salary', 'risk_score', 'job_count']
        risk_salary = risk_salary.sort_values('risk_score', ascending=False)
        
        print("\nAverage Salary by Automation Risk:")
        print("-" * 60)
        for role, data in risk_salary.iterrows():
            risk_level = self.risk_analyzer.get_risk_level(data['risk_score'])
            print(f"{role:25} | Risk: {data['risk_score']:.2f} ({risk_level:10}) | "
                  f"Avg Salary: ${data['avg_salary']:,.0f} | Jobs: {int(data['job_count'])}")
        
        # Calculate correlation
        if len(salary_risk_df) > 10:
            correlation = salary_risk_df['salary_avg'].corr(salary_risk_df['automation_risk_score'])
            print(f"\nSalary-Risk Correlation: {correlation:.3f}")
            
            if correlation < -0.3:
                print("→ Strong negative correlation: Higher risk jobs tend to pay less")
            elif correlation > 0.3:
                print("→ Strong positive correlation: Higher risk jobs tend to pay more")
            else:
                print("→ Weak correlation between automation risk and salary")
    
    def analyze_market_demand_vs_risk(self):
        """Analyze job market demand vs automation risk"""
        print("\n" + "="*60)
        print("MARKET DEMAND VS AUTOMATION RISK")
        print("="*60)
        
        # Group by risk level
        demand_by_risk = self.integrated_df['risk_level'].value_counts()
        total_jobs = len(self.integrated_df)
        
        print("\nJob Postings by Risk Level:")
        print("-" * 40)
        for risk_level, count in demand_by_risk.items():
            percentage = (count / total_jobs) * 100
            print(f"{risk_level:15} | {count:5,} jobs ({percentage:5.1f}%)")
        
        # Analyze high-risk vs low-risk jobs
        high_risk_jobs = self.integrated_df[
            self.integrated_df['automation_risk_score'] >= 0.5
        ]
        low_risk_jobs = self.integrated_df[
            self.integrated_df['automation_risk_score'] < 0.3
        ]
        
        if len(high_risk_jobs) > 0:
            print("\nMost Posted High-Risk Jobs (Risk ≥ 0.5):")
            for job, count in high_risk_jobs['search_term'].value_counts().head(5).items():
                print(f"  • {job}: {count:,} postings")
        
        if len(low_risk_jobs) > 0:
            print("\nMost Posted Low-Risk Jobs (Risk < 0.3):")
            for job, count in low_risk_jobs['search_term'].value_counts().head(5).items():
                print(f"  • {job}: {count:,} postings")
    
    def analyze_location_risk_patterns(self):
        """Analyze automation risk patterns by location"""
        print("\n" + "="*60)
        print("LOCATION-BASED RISK PATTERNS")
        print("="*60)
        
        # Average risk by location
        location_risk = self.integrated_df.groupby('location').agg({
            'automation_risk_score': 'mean',
            'title': 'count',
            'salary_avg': 'mean'
        }).round(3)
        
        location_risk.columns = ['avg_risk_score', 'job_count', 'avg_salary']
        location_risk = location_risk[location_risk['job_count'] >= 20]
        location_risk = location_risk.sort_values('avg_risk_score', ascending=False)
        
        print("\nAverage Automation Risk by Location (min 20 jobs):")
        print("-" * 80)
        for location, data in location_risk.head(10).iterrows():
            salary_str = f"${data['avg_salary']:,.0f}" if pd.notna(data['avg_salary']) else "N/A"
            print(f"{location:30} | Risk: {data['avg_risk_score']:.3f} | "
                  f"Jobs: {int(data['job_count']):3} | Avg Salary: {salary_str:>12}")
    
    def generate_strategic_insights(self):
        """Generate strategic insights from integrated analysis"""
        print("\n" + "="*60)
        print("STRATEGIC INSIGHTS & RECOMMENDATIONS")
        print("="*60)
        
        # 1. Safe haven analysis
        safe_jobs = self.integrated_df[self.integrated_df['automation_risk_score'] < 0.3]
        
        if len(safe_jobs) > 0:
            print("\n1. SAFE HAVEN CAREERS (Low automation risk + High demand):")
            safe_job_counts = safe_jobs['search_term'].value_counts()
            
            for job, count in safe_job_counts.head(5).items():
                job_data = safe_jobs[safe_jobs['search_term'] == job]
                avg_salary = job_data['salary_avg'].mean()
                salary_str = f"${avg_salary:,.0f}" if pd.notna(avg_salary) else "N/A"
                risk_score = job_data['automation_risk_score'].iloc[0]
                print(f"   • {job}: {count:,} openings | Risk: {risk_score:.2f} | Avg salary: {salary_str}")
        
        # 2. High risk but high demand
        risky_jobs = self.integrated_df[self.integrated_df['automation_risk_score'] >= 0.5]
        
        if len(risky_jobs) > 0:
            print("\n2. TRANSITION WARNING (High risk but still hiring):")
            risky_job_counts = risky_jobs['search_term'].value_counts()
            
            for job, count in risky_job_counts.head(5).items():
                job_data = risky_jobs[risky_jobs['search_term'] == job]
                risk_score = job_data['automation_risk_score'].iloc[0]
                avg_salary = job_data['salary_avg'].mean()
                salary_str = f"${avg_salary:,.0f}" if pd.notna(avg_salary) else "N/A"
                print(f"   • {job}: {count:,} openings | Risk: {risk_score:.2f} | Avg salary: {salary_str}")
        
        # 3. Salary premium analysis
        salary_data = self.integrated_df.dropna(subset=['salary_avg'])
        if len(salary_data) > 0:
            low_risk_salary = salary_data[
                salary_data['automation_risk_score'] < 0.3
            ]['salary_avg'].mean()
            high_risk_salary = salary_data[
                salary_data['automation_risk_score'] >= 0.5
            ]['salary_avg'].mean()
            
            if pd.notna(low_risk_salary) and pd.notna(high_risk_salary):
                premium = ((low_risk_salary - high_risk_salary) / high_risk_salary) * 100
                print(f"\n3. SALARY ANALYSIS:")
                print(f"   • Low-risk roles average: ${low_risk_salary:,.0f}")
                print(f"   • High-risk roles average: ${high_risk_salary:,.0f}")
                print(f"   • Premium for low-risk roles: {premium:+.1f}%")
        
        # 4. Geographic recommendations
        print("\n4. GEOGRAPHIC RECOMMENDATIONS:")
        location_stats = self.integrated_df.groupby('location').agg({
            'automation_risk_score': 'mean',
            'salary_avg': 'mean',
            'title': 'count'
        })
        
        # Filter locations with enough data
        location_stats = location_stats[location_stats['title'] >= 30]
        
        if len(location_stats) > 0:
            # Normalize values for scoring
            location_stats['risk_norm'] = 1 - (location_stats['automation_risk_score'] / location_stats['automation_risk_score'].max())
            location_stats['salary_norm'] = location_stats['salary_avg'] / location_stats['salary_avg'].max()
            location_stats['jobs_norm'] = location_stats['title'] / location_stats['title'].max()
            
            # Calculate composite score
            location_stats['score'] = (
                location_stats['risk_norm'] * 0.4 +
                location_stats['salary_norm'] * 0.4 +
                location_stats['jobs_norm'] * 0.2
            )
            
            best_locations = location_stats.sort_values('score', ascending=False)
            
            print("   Best tech hubs (considering risk, salary, and opportunities):")
            for location, data in best_locations.head(5).iterrows():
                print(f"   • {location}: Score {data['score']:.3f} "
                      f"(Risk: {data['automation_risk_score']:.2f}, "
                      f"Jobs: {int(data['title'])}, "
                      f"Avg Salary: ${data['salary_avg']:,.0f})")
    
    def create_integrated_dashboard(self):
        """Create comprehensive integrated dashboard"""
        print("\n" + "="*60)
        print("CREATING INTEGRATED DASHBOARD")
        print("="*60)
        
        # Create figure
        fig = plt.figure(figsize=(20, 16))
        gs = fig.add_gridspec(3, 3, hspace=0.3, wspace=0.3)
        
        # 1. Salary vs Risk Scatter
        ax1 = fig.add_subplot(gs[0, :2])
        salary_risk_df = self.integrated_df.dropna(subset=['salary_avg'])
        
        if len(salary_risk_df) > 0:
            # Group by role for cleaner visualization
            role_data = salary_risk_df.groupby('risk_category').agg({
                'salary_avg': 'mean',
                'automation_risk_score': 'first',
                'title': 'count'
            }).reset_index()
            
            # Create scatter plot
            scatter = ax1.scatter(
                role_data['automation_risk_score'],
                role_data['salary_avg'],
                s=role_data['title'] * 20,  # Size based on job count
                alpha=0.6,
                c=role_data['automation_risk_score'],
                cmap='RdYlGn_r',
                edgecolors='black',
                linewidth=1
            )
            
            # Add role labels
            for _, row in role_data.iterrows():
                ax1.annotate(
                    row['risk_category'],
                    (row['automation_risk_score'], row['salary_avg']),
                    xytext=(5, 5),
                    textcoords='offset points',
                    fontsize=9,
                    alpha=0.8
                )
            
            ax1.set_xlabel('Automation Risk Score', fontsize=12)
            ax1.set_ylabel('Average Salary ($)', fontsize=12)
            ax1.set_title('Salary vs Automation Risk by Role', fontsize=14, fontweight='bold')
            ax1.grid(True, alpha=0.3)
            
            # Add colorbar
            cbar = plt.colorbar(scatter, ax=ax1)
            cbar.set_label('Risk Score', fontsize=10)
        
        # 2. Risk Distribution Pie Chart
        ax2 = fig.add_subplot(gs[0, 2])
        risk_counts = self.integrated_df['risk_level'].value_counts()
        colors = {
            'Very Low': '#1f77b4',
            'Low': '#2ca02c',
            'Medium': '#ffdb58',
            'High': '#ff7f0e',
            'Very High': '#d62728'
        }
        pie_colors = [colors.get(level, '#gray') for level in risk_counts.index]
        
        wedges, texts, autotexts = ax2.pie(
            risk_counts.values,
            labels=risk_counts.index,
            autopct='%1.1f%%',
            colors=pie_colors,
            startangle=90,
            explode=[0.05 if level in ['Very Low', 'Low'] else 0 for level in risk_counts.index]
        )
        
        # Make percentage text bold
        for autotext in autotexts:
            autotext.set_weight('bold')
            autotext.set_color('white')
        
        ax2.set_title('Job Distribution by Risk Level', fontsize=14, fontweight='bold')
        
        # 3. Job Demand by Risk Level
        ax3 = fig.add_subplot(gs[1, :])
        
        # Get top jobs in each risk category
        risk_categories = ['Very Low', 'Low', 'Medium', 'High', 'Very High']
        job_data_list = []
        
        for risk_cat in risk_categories:
            risk_jobs = self.integrated_df[self.integrated_df['risk_level'] == risk_cat]
            if len(risk_jobs) > 0:
                top_jobs = risk_jobs['search_term'].value_counts().head(3)
                for job, count in top_jobs.items():
                    job_data_list.append({
                        'Risk Level': risk_cat,
                        'Job': job,
                        'Count': count
                    })
        
        if job_data_list:
            job_df = pd.DataFrame(job_data_list)
            job_pivot = job_df.pivot_table(
                index='Job',
                columns='Risk Level',
                values='Count',
                fill_value=0
            )
            
            # Ensure columns are in correct order
            ordered_cols = [col for col in risk_categories if col in job_pivot.columns]
            job_pivot = job_pivot[ordered_cols]
            
            # Create stacked bar chart
            job_pivot.plot(
                kind='barh',
                stacked=True,
                ax=ax3,
                colormap='RdYlGn_r',
                width=0.8
            )
            
            ax3.set_xlabel('Number of Job Postings', fontsize=12)
            ax3.set_ylabel('')
            ax3.set_title('Top Jobs by Risk Level', fontsize=14, fontweight='bold')
            ax3.legend(title='Risk Level', bbox_to_anchor=(1.05, 1), loc='upper left')
            ax3.grid(True, axis='x', alpha=0.3)
        
        # 4. Location Risk Heatmap
        ax4 = fig.add_subplot(gs[2, :2])
        
        # Prepare location-role matrix
        location_role = self.integrated_df.pivot_table(
            index='location',
            columns='risk_category',
            values='title',
            aggfunc='count',
            fill_value=0
        )
        
        # Select top locations by total jobs
        if len(location_role) > 0:
            top_locations = location_role.sum(axis=1).nlargest(10).index
            location_role_top = location_role.loc[top_locations]
            
            # Create heatmap
            sns.heatmap(
                location_role_top,
                cmap='YlOrRd',
                ax=ax4,
                cbar_kws={'label': 'Number of Jobs'},
                fmt='d',
                annot=True,
                annot_kws={'size': 8}
            )
            
            ax4.set_title('Job Distribution by Location and Role', fontsize=14, fontweight='bold')
            ax4.set_xlabel('Job Role', fontsize=12)
            ax4.set_ylabel('Location', fontsize=12)
            plt.setp(ax4.xaxis.get_majorticklabels(), rotation=45, ha='right')
        
        # 5. Strategic Insights Summary
        ax5 = fig.add_subplot(gs[2, 2])
        ax5.axis('off')
        
        # Calculate key metrics
        safe_jobs = self.integrated_df[self.integrated_df['automation_risk_score'] < 0.3]
        risky_jobs = self.integrated_df[self.integrated_df['automation_risk_score'] >= 0.5]
        
        # Create insights text
        insights = [
            "KEY INSIGHTS",
            "=" * 25,
            "",
            f"Total Jobs Analyzed: {len(self.integrated_df):,}",
            f"Safe Jobs (<0.3 risk): {len(safe_jobs):,} ({len(safe_jobs)/len(self.integrated_df)*100:.1f}%)",
            f"At-Risk Jobs (≥0.5 risk): {len(risky_jobs):,} ({len(risky_jobs)/len(self.integrated_df)*100:.1f}%)",
            "",
            "TOP SAFE CAREERS:",
        ]
        
        # Add top safe careers
        if len(safe_jobs) > 0:
            for i, (job, count) in enumerate(safe_jobs['search_term'].value_counts().head(3).items(), 1):
                insights.append(f"{i}. {job} ({count:,} jobs)")
        
        insights.extend([
            "",
            "TRANSITION WARNINGS:",
        ])
        
        # Add risky but popular jobs
        if len(risky_jobs) > 0:
            for job, count in risky_jobs['search_term'].value_counts().head(2).items():
                risk = risky_jobs[risky_jobs['search_term'] == job]['automation_risk_score'].iloc[0]
                insights.append(f"• {job} (Risk: {risk:.2f})")
        
        # Add salary insight
        salary_data = self.integrated_df.dropna(subset=['salary_avg'])
        if len(salary_data) > 0:
            avg_salary = salary_data['salary_avg'].mean()
            insights.extend([
                "",
                f"Avg Salary: ${avg_salary:,.0f}"
            ])
        
        # Display insights
        insights_text = '\n'.join(insights)
        ax5.text(
            0.05, 0.95, insights_text,
            transform=ax5.transAxes,
            fontsize=11,
            verticalalignment='top',
            fontfamily='monospace',
            bbox=dict(boxstyle='round,pad=1', facecolor='lightgray', alpha=0.8)
        )
        
        # Main title
        fig.suptitle(
            'WorkShift.AI - Integrated Job Market & Automation Risk Analysis',
            fontsize=20,
            fontweight='bold',
            y=0.98
        )
        
        # Save dashboard
        os.makedirs('data/processed', exist_ok=True)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"data/processed/integrated_dashboard_{timestamp}.png"
        plt.savefig(filename, dpi=300, bbox_inches='tight', facecolor='white')
        print(f"\n✓ Dashboard saved: {filename}")
        
        # Show plot if running interactively
        plt.show()
        
        return filename
    
    def export_integrated_insights(self):
        """Export integrated insights for further analysis"""
        print("\n" + "="*60)
        print("EXPORTING INTEGRATED INSIGHTS")
        print("="*60)
        
        # Create summary by role
        summary_data = []
        
        for role in self.risk_analyzer.role_risk_profiles.keys():
            role_data = self.integrated_df[self.integrated_df['risk_category'] == role]
            
            if len(role_data) > 0:
                summary_data.append({
                    'Role': role,
                    'Automation_Risk_Score': self.risk_analyzer.calculate_automation_risk(role),
                    'Risk_Level': self.risk_analyzer.get_risk_level(
                        self.risk_analyzer.calculate_automation_risk(role)
                    ),
                    'Job_Count': len(role_data),
                    'Avg_Salary': role_data['salary_avg'].mean() if 'salary_avg' in role_data else np.nan,
                    'Min_Salary': role_data['salary_avg'].min() if 'salary_avg' in role_data else np.nan,
                    'Max_Salary': role_data['salary_avg'].max() if 'salary_avg' in role_data else np.nan,
                    'Top_Location': role_data['location'].value_counts().index[0] if len(role_data) > 0 else 'N/A',
                    'Top_Company': role_data['company'].value_counts().index[0] if len(role_data) > 0 else 'N/A',
                    'Remote_Jobs': role_data['remote_allowed'].sum() if 'remote_allowed' in role_data else 0,
                    'Remote_Percentage': (role_data['remote_allowed'].mean() * 100) if 'remote_allowed' in role_data else 0
                })
        
        summary_df = pd.DataFrame(summary_data)
        summary_df = summary_df.sort_values('Automation_Risk_Score')
        
        # Save summary
        os.makedirs('data/processed', exist_ok=True)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"data/processed/integrated_insights_{timestamp}.csv"
        summary_df.to_csv(filename, index=False)
        print(f"\n✓ Insights exported: {filename}")
        
        # Display summary
        print("\nRole Summary:")
        print("-" * 100)
        print(f"{'Role':<25} {'Risk Score':<12} {'Risk Level':<12} {'Jobs':<8} {'Avg Salary':<12} {'Top Location':<20}")
        print("-" * 100)
        
        for _, row in summary_df.iterrows():
            salary_str = f"${row['Avg_Salary']:,.0f}" if pd.notna(row['Avg_Salary']) else "N/A"
            print(f"{row['Role']:<25} {row['Automation_Risk_Score']:<12.2f} {row['Risk_Level']:<12} "
                  f"{row['Job_Count']:<8} {salary_str:<12} {row['Top_Location']:<20}")
        
        return summary_df
    
    def run_integrated_analysis(self):
        """Run complete integrated analysis"""
        print("\n" + "="*60)
        print("WORKSHIFT.AI - INTEGRATED ANALYSIS")
        print("="*60)
        print(f"Analyzing job market data with automation risk assessment...")
        print(f"Data file: {self.job_data_path}")
        
        try:
            # Create integrated dataset
            self.create_integrated_dataset()
            
            # Run all analyses
            self.analyze_salary_vs_risk()
            self.analyze_market_demand_vs_risk()
            self.analyze_location_risk_patterns()
            self.generate_strategic_insights()
            
            # Create visualizations
            self.create_integrated_dashboard()
            
            # Export insights
            self.export_integrated_insights()
            
            print("\n" + "="*60)
            print("✓ INTEGRATED ANALYSIS COMPLETE!")
            print("="*60)
            print("\nGenerated outputs:")
            print("  • Dashboard visualization (PNG)")
            print("  • Integrated insights (CSV)")
            print("  • Strategic recommendations (console)")
            print("\nCheck the 'data/processed' folder for saved files.")
            
        except Exception as e:
            print(f"\n✗ Error during analysis: {e}")
            import traceback
            traceback.print_exc()


def main():
    """Main function to run integrated analysis"""
    # Check for data files
    data_files = []
    data_dir = 'data/raw'
    
    if os.path.exists(data_dir):
        data_files = [f for f in os.listdir(data_dir) if f.endswith('.csv')]
    
    if not data_files:
        print("✗ No CSV files found in data/raw folder!")
        print("\nPlease either:")
        print("  1. Run the data collector first (dual_api_collector.py)")
        print("  2. Add CSV files to the data/raw folder")
        sys.exit(1)
    
    # Select data file
    if len(data_files) == 1:
        selected_file = data_files[0]
        print(f"\nUsing data file: {selected_file}")
    else:
        print("\nAvailable data files:")
        for i, file in enumerate(data_files, 1):
            file_path = os.path.join(data_dir, file)
            size = os.path.getsize(file_path) / 1024  # Size in KB
            print(f"  {i}. {file} ({size:.1f} KB)")
        
        while True:
            choice = input("\nSelect file number (or press Enter for most recent): ").strip()
            
            if not choice:
                # Use most recent file
                selected_file = max(data_files, key=lambda f: os.path.getmtime(os.path.join(data_dir, f)))
                break
            elif choice.isdigit() and 1 <= int(choice) <= len(data_files):
                selected_file = data_files[int(choice) - 1]
                break
            else:
                print("Invalid choice. Please try again.")
    
    data_path = os.path.join(data_dir, selected_file)
    
    # Run integrated analysis
    try:
        analyzer = IntegratedWorkShiftAnalysis(data_path)
        analyzer.run_integrated_analysis()
    except Exception as e:
        print(f"\n✗ Failed to run analysis: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()