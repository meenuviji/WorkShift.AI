import pandas as pd
import numpy as np
import os

# ------------------------------
# Step 1: Define Input & Output
# ------------------------------
output_path = "data/processed/prophet_ready.csv"

# ------------------------------
# Step 2: Create a Simulated Time Series
# ------------------------------
# Prophet requires a continuous date column (ds) and numeric target (y)
# We'll create a clean monthly trend series from 2015 to 2025

date_range = pd.date_range(start="2015-01-01", end="2025-01-01", freq="M")

# Simulate "job openings" data with a growing trend + seasonality + small noise
np.random.seed(42)
trend = np.linspace(1500, 5000, len(date_range))
seasonality = 200 * np.sin(np.linspace(0, 12 * np.pi, len(date_range)))
noise = np.random.normal(0, 100, len(date_range))

y = trend + seasonality + noise

forecast_df = pd.DataFrame({
    "ds": date_range,
    "y": y
})

# ------------------------------
# Step 3: Save & Confirm
# ------------------------------
os.makedirs(os.path.dirname(output_path), exist_ok=True)
forecast_df.to_csv(output_path, index=False)

print("✅ Prophet-ready data saved successfully!")
print(f"File path: {output_path}")
print("\nSample of the dataset:")
print(forecast_df.head(10))
print("\nTotal rows:", len(forecast_df))
