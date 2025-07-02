# WorkShift.AI - Adzuna Job Collector
# Professional job data collection using Adzuna API

import requests
import pandas as pd
import time
import os
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class AdzunaJobCollector:
    """
    Professional job collector using Adzuna API for WorkShift.AI project
    """
    
    def __init__(self):
        self.app_id = os.getenv('ADZUNA_APP_ID')
        self.app_key = os.getenv('ADZUNA_APP_KEY')
        self.data_path = os.getenv('DATA_PATH', 'data/raw')
        self.jobs_data = []
        
        # Create data directory
        os.makedirs(self.data_path, exist_ok=True)
        
        print("Adzuna API Collector initialized")
        print(f"Data will be saved to: {self.data_path}")
        
        # Check if API keys are loaded
        if not self.app_id or not self.app_key:
            print("ERROR: API keys not found!")
            print("Make sure your .env file has:")
            print("ADZUNA_APP_ID=9c54ed3b")
            print("ADZUNA_APP_KEY=74a6869147ede2c62fe7ea140846ec54")
        else:
            print("API keys loaded successfully")
    
    def search_jobs(self, job_title, location, max_results=25):
        """
        Search for jobs using Adzuna API
        
        Args:
            job_title (str): Job title to search for
            location (str): Location to search in
            max_results (int): Maximum number of results to return
            
        Returns:
            list: List of processed job dictionaries
        """
        print(f"Searching: {job_title} in {location}")
        
        # Adzuna API endpoint
        url = "https://api.adzuna.com/v1/api/jobs/us/search/1"
        
        # API parameters
        params = {
            'app_id': self.app_id,
            'app_key': self.app_key,
            'what': job_title,
            'where': location,
            'results_per_page': max_results,
            'sort_by': 'date',  # Get most recent jobs
            'content-type': 'application/json'
        }
        
        try:
            # Make API request
            response = requests.get(url, params=params)
            response.raise_for_status()  # Raise exception for bad status codes
            
            # Parse JSON response
            data = response.json()
            jobs = data.get('results', [])
            
            print(f"   API returned {len(jobs)} jobs")
            
            # Process each job
            processed_jobs = []
            for job in jobs:
                try:
                    # Extract job information
                    processed_job = {
                        'title': job.get('title', '').strip(),
                        'company': job.get('company', {}).get('display_name', '').strip(),
                        'location': job.get('location', {}).get('display_name', '').strip(),
                        'description': job.get('description', '').strip()[:500],  # Limit description length
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
                    
                    # Add to results
                    processed_jobs.append(processed_job)
                    self.jobs_data.append(processed_job)
                    
                except Exception as e:
                    print(f"   WARNING: Error processing job: {e}")
                    continue
            
            print(f"   Processed {len(processed_jobs)} jobs successfully")
            
            # Be respectful to API - small delay
            time.sleep(1)
            
            return processed_jobs
            
        except requests.exceptions.RequestException as e:
            print(f"   ERROR: API request failed: {e}")
            return []
        except Exception as e:
            print(f"   ERROR: Unexpected error: {e}")
            return []
    
    def collect_comprehensive_data(self):
        """
        Collect job data for multiple roles and locations
        
        Returns:
            list: Complete list of collected job data
        """
        print("Starting comprehensive job data collection...")
        print("=" * 60)
        
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
            'Software Developer'
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
        print(f"Expected total searches: {len(job_titles) * len(locations)}")
        
        total_jobs = 0
        search_count = 0
        
        # Search for each job title in each location
        for job_title in job_titles:
            for location in locations:
                search_count += 1
                print(f"\nSearch {search_count}/{len(job_titles) * len(locations)}")
                
                jobs_found = self.search_jobs(job_title, location, max_results=20)
                total_jobs += len(jobs_found)
                
                print(f"   Running total: {total_jobs} jobs collected")
                
                # Small delay between searches to be respectful
                time.sleep(2)
        
        print(f"\nCollection complete!")
        print(f"Total jobs collected: {total_jobs}")
        
        return self.jobs_data
    
    def save_to_csv(self, filename=None):
        """
        Save collected jobs to CSV file
        
        Args:
            filename (str, optional): Custom filename for the CSV file
            
        Returns:
            str: Path to the saved CSV file
        """
        if not self.jobs_data:
            print("ERROR: No jobs to save")
            return None
        
        # Generate filename if not provided
        if filename is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"{self.data_path}/adzuna_jobs_{timestamp}.csv"
        
        # Create DataFrame and save
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
        
        print("\n" + "=" * 60)
        print("JOB DATA COLLECTION SUMMARY")
        print("=" * 60)
        
        print(f"Total Jobs Collected: {len(df):,}")
        print(f"Unique Companies: {df['company'].nunique():,}")
        print(f"Unique Locations: {df['location'].nunique():,}")
        print(f"Search Terms Used: {df['search_term'].nunique():,}")
        
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
            if company:  # Skip empty company names
                print(f"   {company}: {count} jobs")
        
        # Salary analysis
        salary_df = df.dropna(subset=['salary_min', 'salary_max'])
        if len(salary_df) > 0:
            print(f"\nSalary Information:")
            print(f"   Jobs with salary data: {len(salary_df)} ({len(salary_df)/len(df)*100:.1f}%)")
            print(f"   Average min salary: ${salary_df['salary_min'].mean():,.0f}")
            print(f"   Average max salary: ${salary_df['salary_max'].mean():,.0f}")
            print(f"   Salary range: ${salary_df['salary_min'].min():,.0f} - ${salary_df['salary_max'].max():,.0f}")
        
        print("\nData Sources:")
        for source, count in df['source'].value_counts().items():
            print(f"   {source}: {count} jobs")

def main():
    """
    Main function to execute the job collection process
    
    Returns:
        str: Path to the saved CSV file containing job data
    """
    print("WorkShift.AI - Real Job Data Collection")
    print("Using Adzuna API")
    print("=" * 60)
    
    # Initialize collector
    collector = AdzunaJobCollector()
    
    # Check if initialization was successful
    if not collector.app_id or not collector.app_key:
        print("\nERROR: Setup incomplete!")
        print("Please check your .env file and API keys")
        return None
    
    print("\nStarting data collection process...")
    
    # Collect comprehensive job data
    collector.collect_comprehensive_data()
    
    # Display summary
    collector.display_summary()
    
    # Save to CSV
    filename = collector.save_to_csv()
    
    print("\n" + "=" * 60)
    print("JOB DATA COLLECTION COMPLETE!")
    print("=" * 60)
    print(f"Data saved to: {filename}")
    print("Ready for analysis and visualization!")
    
    
    return filename

if __name__ == "__main__":
    main()