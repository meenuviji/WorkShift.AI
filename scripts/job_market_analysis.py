# WorkShift.AI - Job Market Data Analysis
# Professional analysis of collected job market data

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Set plotting style
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

class JobMarketAnalyzer:
    """
    Professional job market data analyzer for WorkShift.AI
    """
    
    def __init__(self, csv_file_path):
        """
        Initialize analyzer with job data
        
        Args:
            csv_file_path (str): Path to the CSV file containing job data
        """
        self.data_path = csv_file_path
        self.df = None
        self.load_data()
    
    def load_data(self):
        """Load and perform initial data cleaning"""
        try:
            self.df = pd.read_csv(self.data_path)
            print(f"Data loaded successfully: {len(self.df)} records")
            print(f"Columns: {list(self.df.columns)}")
            
            # Basic data cleaning
            self.clean_data()
            
        except FileNotFoundError:
            print(f"ERROR: File not found: {self.data_path}")
            return None
        except Exception as e:
            print(f"ERROR loading data: {e}")
            return None
    
    def clean_data(self):
        """Clean and prepare data for analysis"""
        print("\nCleaning data...")
        
        original_count = len(self.df)
        
        # Remove duplicates
        self.df = self.df.drop_duplicates()
        
        # Clean job titles and companies
        self.df['title'] = self.df['title'].str.strip()
        self.df['company'] = self.df['company'].str.strip()
        self.df['location'] = self.df['location'].str.strip()
        
        # Handle salary data
        self.df['salary_min'] = pd.to_numeric(self.df['salary_min'], errors='coerce')
        self.df['salary_max'] = pd.to_numeric(self.df['salary_max'], errors='coerce')
        
        # Calculate average salary where possible
        self.df['salary_avg'] = (self.df['salary_min'] + self.df['salary_max']) / 2
        
        # Extract state from location
        self.df['state'] = self.df['location'].str.extract(r', ([A-Z]{2})')[0]
        
        # Clean search terms for better categorization
        self.df['job_category'] = self.df['search_term'].str.replace(' Engineer', '').str.replace(' Developer', '')
        
        print(f"Data cleaned: {len(self.df)} records (removed {original_count - len(self.df)} duplicates)")

        # Add risk category mapping
        self.df['risk_category'] = self.df['search_term'].apply(self.map_to_risk_category)
    
    def basic_statistics(self):
        """Display basic statistics about the dataset"""
        print("\n" + "="*60)
        print("BASIC DATASET STATISTICS")
        print("="*60)
        
        print(f"Total job postings: {len(self.df):,}")
        print(f"Unique companies: {self.df['company'].nunique():,}")
        print(f"Unique job titles: {self.df['title'].nunique():,}")
        print(f"Unique locations: {self.df['location'].nunique():,}")
        print(f"Date range: {self.df['collected_date'].min()} to {self.df['collected_date'].max()}")
        
        print(f"\nData sources breakdown:")
        for source, count in self.df['source'].value_counts().items():
            print(f"  {source}: {count:,} jobs")
        
        print(f"\nSalary data availability:")
        salary_data = self.df.dropna(subset=['salary_min', 'salary_max'])
        print(f"  Jobs with salary info: {len(salary_data):,} ({len(salary_data)/len(self.df)*100:.1f}%)")
        
        if len(salary_data) > 0:
            print(f"  Average salary range: ${salary_data['salary_min'].mean():,.0f} - ${salary_data['salary_max'].mean():,.0f}")
    
    def analyze_job_demand(self):
        """Analyze job demand by role and location"""
        print("\n" + "="*60)
        print("JOB DEMAND ANALYSIS")
        print("="*60)
        
        # Job demand by search term
        job_demand = self.df['search_term'].value_counts().head(10)
        print("\nTop 10 Most In-Demand Roles:")
        for role, count in job_demand.items():
            print(f"  {role}: {count:,} postings")
        
        # Job demand by location
        location_demand = self.df['location'].value_counts().head(10)
        print("\nTop 10 Job Markets by Volume:")
        for location, count in location_demand.items():
            print(f"  {location}: {count:,} postings")
        
        # State-level analysis
        if 'state' in self.df.columns:
            state_demand = self.df['state'].value_counts().head(10)
            print("\nTop States for Tech Jobs:")
            for state, count in state_demand.items():
                if pd.notna(state):
                    print(f"  {state}: {count:,} postings")
    
    def analyze_salaries(self):
        """Analyze salary trends and patterns"""
        print("\n" + "="*60)
        print("SALARY ANALYSIS")
        print("="*60)
        
        salary_df = self.df.dropna(subset=['salary_avg'])
        
        if len(salary_df) == 0:
            print("No salary data available for analysis")
            return
        
        print(f"Analyzing {len(salary_df):,} jobs with salary data")
        
        # Overall salary statistics
        print(f"\nOverall Salary Statistics:")
        print(f"  Average salary: ${salary_df['salary_avg'].mean():,.0f}")
        print(f"  Median salary: ${salary_df['salary_avg'].median():,.0f}")
        print(f"  Salary range: ${salary_df['salary_avg'].min():,.0f} - ${salary_df['salary_avg'].max():,.0f}")
        
        # Salary by job role
        role_salaries = salary_df.groupby('search_term')['salary_avg'].agg(['mean', 'count']).round(0)
        role_salaries = role_salaries[role_salaries['count'] >= 5].sort_values('mean', ascending=False)
        
        print(f"\nAverage Salary by Role (min 5 jobs):")
        for role, data in role_salaries.head(10).iterrows():
            print(f"  {role}: ${data['mean']:,.0f} (based on {data['count']} jobs)")
        
        # Salary by location
        location_salaries = salary_df.groupby('location')['salary_avg'].agg(['mean', 'count']).round(0)
        location_salaries = location_salaries[location_salaries['count'] >= 10].sort_values('mean', ascending=False)
        
        print(f"\nAverage Salary by Location (min 10 jobs):")
        for location, data in location_salaries.head(10).iterrows():
            print(f"  {location}: ${data['mean']:,.0f} (based on {data['count']} jobs)")
    
    def analyze_companies(self):
        """Analyze top hiring companies"""
        print("\n" + "="*60)
        print("COMPANY HIRING ANALYSIS")
        print("="*60)
        
        # Top hiring companies
        top_companies = self.df['company'].value_counts().head(15)
        print("Top 15 Hiring Companies:")
        for company, count in top_companies.items():
            if company and company.strip():
                print(f"  {company}: {count:,} job postings")
    
    def analyze_remote_work(self):
        """Analyze remote work trends"""
        print("\n" + "="*60)
        print("REMOTE WORK ANALYSIS")
        print("="*60)
        
        # Check if remote data exists
        if 'remote_allowed' in self.df.columns:
            remote_df = self.df.dropna(subset=['remote_allowed'])
            
            if len(remote_df) > 0:
                remote_count = remote_df['remote_allowed'].sum()
                remote_percentage = (remote_count / len(remote_df)) * 100
                
                print(f"Remote work data available for {len(remote_df):,} jobs")
                print(f"Remote-friendly jobs: {remote_count:,} ({remote_percentage:.1f}%)")
                
                # Remote work by role
                remote_by_role = remote_df.groupby('search_term')['remote_allowed'].agg(['sum', 'count'])
                remote_by_role['percentage'] = (remote_by_role['sum'] / remote_by_role['count'] * 100).round(1)
                remote_by_role = remote_by_role[remote_by_role['count'] >= 5].sort_values('percentage', ascending=False)
                
                print(f"\nRemote Work by Role (min 5 jobs):")
                for role, data in remote_by_role.head(10).iterrows():
                    print(f"  {role}: {data['percentage']:.1f}% remote ({int(data['sum'])}/{int(data['count'])} jobs)")
            else:
                print("No remote work data available")
        else:
            print("Remote work data not available in dataset")
    
    def create_visualizations(self):
        """Create key visualizations"""
        print("\n" + "="*60)
        print("CREATING VISUALIZATIONS")
        print("="*60)
        
        # Create figure with subplots
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        fig.suptitle('WorkShift.AI - Job Market Analysis Dashboard', fontsize=16, fontweight='bold')
        
        # 1. Job demand by role
        job_demand = self.df['search_term'].value_counts().head(8)
        axes[0, 0].barh(job_demand.index, job_demand.values, color='skyblue')
        axes[0, 0].set_title('Job Demand by Role')
        axes[0, 0].set_xlabel('Number of Job Postings')
        
        # 2. Job demand by location
        location_demand = self.df['location'].value_counts().head(8)
        axes[0, 1].barh(location_demand.index, location_demand.values, color='lightcoral')
        axes[0, 1].set_title('Job Demand by Location')
        axes[0, 1].set_xlabel('Number of Job Postings')
        
        # 3. Salary distribution
        salary_df = self.df.dropna(subset=['salary_avg'])
        if len(salary_df) > 0:
            axes[1, 0].hist(salary_df['salary_avg'], bins=20, color='lightgreen', alpha=0.7)
            axes[1, 0].set_title('Salary Distribution')
            axes[1, 0].set_xlabel('Average Salary ($)')
            axes[1, 0].set_ylabel('Number of Jobs')
        else:
            axes[1, 0].text(0.5, 0.5, 'No salary data available', ha='center', va='center')
            axes[1, 0].set_title('Salary Distribution')
        
        # 4. Data sources
        source_counts = self.df['source'].value_counts()
        axes[1, 1].pie(source_counts.values, labels=source_counts.index, autopct='%1.1f%%', startangle=90)
        axes[1, 1].set_title('Data Sources Distribution')
        
        plt.tight_layout()
        
        # Save the visualization
        viz_filename = f"data/processed/job_market_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        plt.savefig(viz_filename, dpi=300, bbox_inches='tight')
        
        print(f"Visualization saved: {viz_filename}")
        plt.show()
    
    def generate_insights(self):
        """Generate key business insights"""
        print("\n" + "="*60)
        print("KEY BUSINESS INSIGHTS")
        print("="*60)
        
        # Most in-demand role
        top_role = self.df['search_term'].value_counts().index[0]
        top_role_count = self.df['search_term'].value_counts().iloc[0]
        
        print(f"1. HIGHEST DEMAND ROLE")
        print(f"   {top_role} with {top_role_count:,} job postings")
        
        # Best paying role (if salary data available)
        salary_df = self.df.dropna(subset=['salary_avg'])
        if len(salary_df) > 0:
            role_salaries = salary_df.groupby('search_term')['salary_avg'].agg(['mean', 'count'])
            role_salaries = role_salaries[role_salaries['count'] >= 5]
            
            if len(role_salaries) > 0:
                highest_paid_role = role_salaries['mean'].idxmax()
                highest_salary = role_salaries.loc[highest_paid_role, 'mean']
                
                print(f"\n2. HIGHEST PAYING ROLE")
                print(f"   {highest_paid_role} with average salary ${highest_salary:,.0f}")
        
        # Top job market
        top_market = self.df['location'].value_counts().index[0]
        top_market_count = self.df['location'].value_counts().iloc[0]
        
        print(f"\n3. TOP JOB MARKET")
        print(f"   {top_market} with {top_market_count:,} job postings")
        
        # Top hiring company
        top_company = self.df['company'].value_counts().index[0]
        top_company_count = self.df['company'].value_counts().iloc[0]
        
        print(f"\n4. TOP HIRING COMPANY")
        print(f"   {top_company} with {top_company_count:,} job postings")
        
        # Remote work insights
        if 'remote_allowed' in self.df.columns:
            remote_df = self.df.dropna(subset=['remote_allowed'])
            if len(remote_df) > 0:
                remote_percentage = (remote_df['remote_allowed'].sum() / len(remote_df)) * 100
                print(f"\n5. REMOTE WORK AVAILABILITY")
                print(f"   {remote_percentage:.1f}% of jobs offer remote work")
        
        # Market concentration
        top_5_locations = self.df['location'].value_counts().head(5).sum()
        location_concentration = (top_5_locations / len(self.df)) * 100
        
        print(f"\n6. MARKET CONCENTRATION")
        print(f"   Top 5 locations account for {location_concentration:.1f}% of all jobs")
    
    def generate_report(self):
        """Generate a comprehensive analysis report"""
        print("\n" + "="*60)
        print("GENERATING COMPREHENSIVE REPORT")
        print("="*60)
        
        # Create report filename
        report_filename = f"data/processed/job_market_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        
        # Redirect output to file
        import sys
        original_stdout = sys.stdout
        
        try:
            with open(report_filename, 'w') as f:
                sys.stdout = f
                
                print("WorkShift.AI - Job Market Analysis Report")
                print(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                print("="*60)
                
                # Run all analyses
                self.basic_statistics()
                self.analyze_job_demand()
                self.analyze_salaries()
                self.analyze_companies()
                self.analyze_remote_work()
                self.generate_insights()
                
                print("\n" + "="*60)
                print("END OF REPORT")
                
            sys.stdout = original_stdout
            print(f"Report saved: {report_filename}")
            
        except Exception as e:
            sys.stdout = original_stdout
            print(f"Error generating report: {e}")
    
    def run_complete_analysis(self):
        """Run the complete analysis pipeline"""
        print("\nStarting complete job market analysis...")
        
        # Run all analyses
        self.basic_statistics()
        self.analyze_job_demand()
        self.analyze_salaries()
        self.analyze_companies()
        self.analyze_remote_work()
        self.generate_insights()
        
        # Create visualizations
        self.create_visualizations()
        
        # Generate report
        self.generate_report()
        
        print("\nAnalysis complete!")


# Main execution
if __name__ == "__main__":
    # Initialize the analyzer with your CSV file
    analyzer = JobMarketAnalyzer('data/raw/consolidated_jobs.csv')
    
    # Run complete analysis
    if analyzer.df is not None:
        analyzer.run_complete_analysis()
    else:
        print("Failed to load data. Please check the file path.")