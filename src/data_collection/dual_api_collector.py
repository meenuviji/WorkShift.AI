# WorkShift.AI - Dual API Job Collector
# Professional job data collection using Adzuna API and RapidAPI JSearch

import requests
import pandas as pd
import time
import os
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class DualAPIJobCollector:
    """
    Professional job collector using both Adzuna API and RapidAPI JSearch
    """
    
    def __init__(self):
        # Adzuna API credentials
        self.adzuna_app_id = os.getenv('ADZUNA_APP_ID')
        self.adzuna_app_key = os.getenv('ADZUNA_APP_KEY')
        
        # RapidAPI credentials
        self.rapidapi_key = os.getenv('RAPIDAPI_KEY')
        
        # Settings
        self.data_path = os.getenv('DATA_PATH', 'data/raw')
        self.jobs_data = []
        
        # Create data directory
        os.makedirs(self.data_path, exist_ok=True)
        
        print("Dual API Job Collector initialized")
        print(f"Data will be saved to: {self.data_path}")
        
        # Check API keys
        self.check_api_keys()
    
    def check_api_keys(self):
        """Check if all API keys are available"""
        adzuna_available = bool(self.adzuna_app_id and self.adzuna_app_key)
        rapidapi_available = bool(self.rapidapi_key)
        
        print(f"Adzuna API: {'Available' if adzuna_available else 'Not Available'}")
        print(f"RapidAPI: {'Available' if rapidapi_available else 'Not Available'}")
        
        if not adzuna_available and not rapidapi_available:
            print("ERROR: No API keys found! Please check your .env file")
            return False
        
        return True
    
    def search_adzuna_jobs(self, job_title, location, max_results=25):
        """
        Search for jobs using Adzuna API
        """
        if not self.adzuna_app_id or not self.adzuna_app_key:
            print("   Adzuna API not available, skipping...")
            return []
        
        print(f"   Searching Adzuna: {job_title} in {location}")
        
        url = "https://api.adzuna.com/v1/api/jobs/us/search/1"
        
        params = {
            'app_id': self.adzuna_app_id,
            'app_key': self.adzuna_app_key,
            'what': job_title,
            'where': location,
            'results_per_page': max_results,
            'sort_by': 'date',
            'content-type': 'application/json'
        }
        
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            
            data = response.json()
            jobs = data.get('results', [])
            
            print(f"   Adzuna returned {len(jobs)} jobs")
            
            processed_jobs = []
            for job in jobs:
                try:
                    processed_job = {
                        'title': job.get('title', '').strip(),
                        'company': job.get('company', {}).get('display_name', '').strip(),
                        'location': job.get('location', {}).get('display_name', '').strip(),
                        'description': job.get('description', '').strip()[:500],
                        'salary_min': job.get('salary_min'),
                        'salary_max': job.get('salary_max'),
                        'contract_type': job.get('contract_type', ''),
                        'category': job.get('category', {}).get('label', ''),
                        'created_date': job.get('created'),
                        'redirect_url': job.get('redirect_url', ''),
                        'source': 'adzuna',
                        'search_term': job_title,
                        'search_location': location,
                        'collected_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    }
                    
                    processed_jobs.append(processed_job)
                    self.jobs_data.append(processed_job)
                    
                except Exception as e:
                    print(f"   WARNING: Error processing Adzuna job: {e}")
                    continue
            
            print(f"   Processed {len(processed_jobs)} Adzuna jobs")
            time.sleep(1)
            
            return processed_jobs
            
        except requests.exceptions.RequestException as e:
            print(f"   ERROR: Adzuna API request failed: {e}")
            return []
    
    def search_rapidapi_jobs(self, job_title, location, max_results=25):
        """
        Search for jobs using RapidAPI JSearch
        """
        if not self.rapidapi_key:
            print("   RapidAPI not available, skipping...")
            return []
        
        print(f"   Searching RapidAPI: {job_title} in {location}")
        
        url = "https://jsearch.p.rapidapi.com/search"
        
        headers = {
            'X-RapidAPI-Key': self.rapidapi_key,
            'X-RapidAPI-Host': 'jsearch.p.rapidapi.com'
        }
        
        params = {
            'query': f"{job_title} {location}",
            'page': '1',
            'num_pages': '1',
            'date_posted': 'month'
        }
        
        try:
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()
            
            data = response.json()
            jobs = data.get('data', [])
            
            print(f"   RapidAPI returned {len(jobs)} jobs")
            
            processed_jobs = []
            for job in jobs[:max_results]:
                try:
                    processed_job = {
                        'title': job.get('job_title', '').strip(),
                        'company': job.get('employer_name', '').strip(),
                        'location': f"{job.get('job_city', '')}, {job.get('job_state', '')}".strip(', '),
                        'description': job.get('job_description', '').strip()[:500],
                        'salary_min': job.get('job_min_salary'),
                        'salary_max': job.get('job_max_salary'),
                        'contract_type': job.get('job_employment_type', ''),
                        'remote_allowed': job.get('job_is_remote', False),
                        'posted_date': job.get('job_posted_at_datetime_utc', ''),
                        'apply_link': job.get('job_apply_link', ''),
                        'source': 'rapidapi_jsearch',
                        'search_term': job_title,
                        'search_location': location,
                        'collected_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    }
                    
                    processed_jobs.append(processed_job)
                    self.jobs_data.append(processed_job)
                    
                except Exception as e:
                    print(f"   WARNING: Error processing RapidAPI job: {e}")
                    continue
            
            print(f"   Processed {len(processed_jobs)} RapidAPI jobs")
            time.sleep(1)
            
            return processed_jobs
            
        except requests.exceptions.RequestException as e:
            print(f"   ERROR: RapidAPI request failed: {e}")
            return []
    
    def search_all_sources(self, job_title, location, max_per_source=20):
        """
        Search for jobs using all available APIs
        """
        print(f"Searching: {job_title} in {location}")
        
        total_jobs = 0
        
        # Search Adzuna
        adzuna_jobs = self.search_adzuna_jobs(job_title, location, max_per_source)
        total_jobs += len(adzuna_jobs)
        
        # Search RapidAPI
        rapidapi_jobs = self.search_rapidapi_jobs(job_title, location, max_per_source)
        total_jobs += len(rapidapi_jobs)
        
        print(f"   Total jobs found: {total_jobs}")
        return total_jobs
    
    def collect_comprehensive_data(self):
        """
        Collect job data from all sources for multiple roles and locations
        """
        print("Starting job data collection from multiple sources...")
        print("=" * 70)
        
        # Job titles to search for
        job_titles = [
            'Software Engineer',
            'Data Scientist',
            'Product Manager',
            'DevOps Engineer',
            'Machine Learning Engineer',
            'Frontend Developer',
            'Backend Developer',
            'Full Stack Developer',
            'Data Analyst',
            'Software Developer',
            'Cloud Engineer',
            'Security Engineer'
        ]
        
        # Locations to search in
        locations = [
            'San Francisco, CA',
            'New York, NY',
            'Seattle, WA',
            'Austin, TX',
            'Boston, MA',
            'Los Angeles, CA',
            'Chicago, IL',
            'Denver, CO'
        ]
        
        print(f"Searching for {len(job_titles)} job types in {len(locations)} locations")
        print(f"Total searches planned: {len(job_titles) * len(locations)}")
        
        total_jobs = 0
        search_count = 0
        
        # Search for each job title in each location
        for job_title in job_titles:
            for location in locations:
                search_count += 1
                print(f"\nSearch {search_count}/{len(job_titles) * len(locations)}")
                
                jobs_found = self.search_all_sources(job_title, location, max_per_source=15)
                total_jobs += jobs_found
                
                print(f"   Running total: {total_jobs} jobs collected")
                
                # Respectful delay between searches
                time.sleep(3)
        
        print(f"\nCollection complete!")
        print(f"Total jobs collected: {total_jobs}")
        
        return self.jobs_data
    
    def save_to_csv(self, filename=None):
        """
        Save collected jobs to CSV file
        """
        if not self.jobs_data:
            print("ERROR: No jobs to save")
            return None
        
        if filename is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"{self.data_path}/dual_api_jobs_{timestamp}.csv"
        
        df = pd.DataFrame(self.jobs_data)
        df.to_csv(filename, index=False)
        
        print(f"\nData saved successfully!")
        print(f"File: {filename}")
        print(f"Records: {len(df)}")
        
        return filename
    
    def display_summary(self):
        """
        Display comprehensive summary of collected data
        """
        if not self.jobs_data:
            print("ERROR: No data to summarize")
            return
        
        df = pd.DataFrame(self.jobs_data)
        
        print("\n" + "=" * 70)
        print("JOB DATA COLLECTION SUMMARY")
        print("=" * 70)
        
        print(f"Total Jobs Collected: {len(df):,}")
        print(f"Unique Companies: {df['company'].nunique():,}")
        print(f"Unique Locations: {df['location'].nunique():,}")
        print(f"Search Terms Used: {df['search_term'].nunique():,}")
        
        print("\nData Sources:")
        for source, count in df['source'].value_counts().items():
            print(f"   {source}: {count} jobs")
        
        print("\nTop Job Titles:")
        top_titles = df['search_term'].value_counts().head(10)
        for title, count in top_titles.items():
            print(f"   {title}: {count} jobs")
        
        print("\nTop Locations:")
        top_locations = df['location'].value_counts().head(10)
        for location, count in top_locations.items():
            print(f"   {location}: {count} jobs")
        
        print("\nTop Companies:")
        top_companies = df['company'].value_counts().head(10)
        for company, count in top_companies.items():
            if company:
                print(f"   {company}: {count} jobs")
        
        # Salary analysis
        salary_df = df.dropna(subset=['salary_min', 'salary_max'])
        if len(salary_df) > 0:
            print(f"\nSalary Information:")
            print(f"   Jobs with salary data: {len(salary_df)} ({len(salary_df)/len(df)*100:.1f}%)")
            print(f"   Average min salary: ${salary_df['salary_min'].mean():,.0f}")
            print(f"   Average max salary: ${salary_df['salary_max'].mean():,.0f}")
            print(f"   Salary range: ${salary_df['salary_min'].min():,.0f} - ${salary_df['salary_max'].max():,.0f}")
        
        # Remote work analysis
        remote_df = df[df['source'] == 'rapidapi_jsearch']
        if len(remote_df) > 0 and 'remote_allowed' in remote_df.columns:
            remote_count = remote_df['remote_allowed'].sum()
            remote_pct = (remote_count / len(remote_df)) * 100
            print(f"\nRemote Work Analysis:")
            print(f"   Remote-friendly jobs: {remote_count} ({remote_pct:.1f}%)")

def main():
    """
    Main function to execute the dual API job collection
    """
    print("WorkShift.AI - Job Data Collection")
    print("Using Adzuna API + RapidAPI JSearch")
    print("=" * 70)
    
    # Initialize collector
    collector = DualAPIJobCollector()
    
    # Check if at least one API is available
    if not collector.check_api_keys():
        return None
    
    print("\nStarting data collection process...")
    
    # Collect comprehensive job data
    collector.collect_comprehensive_data()
    
    # Display summary
    collector.display_summary()
    
    # Save to CSV
    filename = collector.save_to_csv()
    
    print("\n" + "=" * 70)
    print("JOB DATA COLLECTION COMPLETE")
    print("=" * 70)
    print(f"Data saved to: {filename}")
    print(f"Total records: {len(pd.read_csv(filename)) if filename else 0}")
    
    return filename

if __name__ == "__main__":
    main()