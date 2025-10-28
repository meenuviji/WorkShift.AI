import pandas as pd
import os

# ---------------------------------------
# Load and clean job demand data
# ---------------------------------------
def load_job_demand_data(path="data/raw/raw_job_demand.csv"):
    if not os.path.exists(path):
        raise FileNotFoundError(f"Could not find file: {path}")
    
    df = pd.read_csv(path)
    print(f"✅ Loaded job demand data with {len(df)} rows and {len(df.columns)} columns.")
    
    # Convert date column to datetime
    df['date'] = pd.to_datetime(df['date'], errors='coerce', infer_datetime_format=True)
    df = df.dropna(subset=['date'])

    
    # Sort by date for forecasting later
    df = df.sort_values(by='date').reset_index(drop=True)
    
    # Remove duplicates just in case
    df = df.drop_duplicates()
    
    return df


# ---------------------------------------
# Load and clean automation risk data
# ---------------------------------------
def load_automation_risk_data(path="data/raw/automation_risk_reference.csv"):
    if not os.path.exists(path):
        raise FileNotFoundError(f"Could not find file: {path}")
    
    df = pd.read_csv(path)
    print(f"✅ Loaded automation risk data with {len(df)} rows and {len(df.columns)} columns.")
    
    # Ensure job_title is string and consistent
    df['job_title'] = df['job_title'].str.strip()
    
    return df


# ---------------------------------------
# Merge both datasets
# ---------------------------------------
def merge_datasets(demand_df, risk_df):
    # Normalize job titles for consistent merging
    demand_df['job_title'] = demand_df['job_title'].astype(str).str.strip().str.lower()
    risk_df['job_title'] = risk_df['job_title'].astype(str).str.strip().str.lower()

    print("🧩 Job titles in demand data:", demand_df['job_title'].unique())
    print("🧩 Job titles in risk data:", risk_df['job_title'].unique())

    # Merge datasets
    merged = pd.merge(demand_df, risk_df, on='job_title', how='left')

    # Fill missing values
    merged['automation_risk_score'] = merged['automation_risk_score'].fillna(0.5)

    print(f"✅ Merged dataset has {len(merged)} rows and {len(merged.columns)} columns.")
    return merged



# ---------------------------------------
# Main function to run all cleaning steps
# ---------------------------------------
def prepare_clean_dataset():
    demand_df = load_job_demand_data()
    risk_df = load_automation_risk_data()
    
    clean_df = merge_datasets(demand_df, risk_df)
    
    # Save to processed folder
    os.makedirs("data/processed", exist_ok=True)
    output_path = os.path.join(os.getcwd(), "data", "processed", "clean_job_trends.csv")
    clean_df.to_csv(output_path, index=False)
    
    print(f"💾 Cleaned data saved to {output_path}")
    return clean_df


# ---------------------------------------
# Run script standalone
# ---------------------------------------
if __name__ == "__main__":
    prepare_clean_dataset()

