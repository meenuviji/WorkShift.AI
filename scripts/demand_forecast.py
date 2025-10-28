import pandas as pd
from prophet import Prophet
import matplotlib.pyplot as plt
import os

# === 1️⃣ Load the cleaned dataset ===
DATA_PATH = "data/processed/clean_job_trends.csv"
df = pd.read_csv(DATA_PATH)

# Ensure consistent column names
df.columns = [c.strip().lower() for c in df.columns]

# Print quick info
print("Columns in dataset:", df.columns.tolist())
print("Sample data:\n", df.head())

# === 2️⃣ Prepare data for forecasting ===
if 'date' not in df.columns or 'postings' not in df.columns or 'avg_salary' not in df.columns:
    raise ValueError("❌ Missing required columns ['date', 'postings', 'avg_salary'] in dataset!")

# Convert date column
df['date'] = pd.to_datetime(df['date'])

# === 3️⃣ Forecast Job Postings ===
print("\n📈 Training Job Postings Forecast Model...")
df_post = df[['date', 'postings']].rename(columns={'date': 'ds', 'postings': 'y'})

model_post = Prophet(daily_seasonality=False, weekly_seasonality=False, yearly_seasonality=True)
model_post.fit(df_post)

future_post = model_post.make_future_dataframe(periods=12, freq='M')  # forecast next 12 months
forecast_post = model_post.predict(future_post)

# Save results
os.makedirs("data/processed", exist_ok=True)
forecast_post.to_csv("data/processed/job_postings_forecast.csv", index=False)

# Plot
model_post.plot(forecast_post)
plt.title("Forecast: Job Postings")
plt.xlabel("Date")
plt.ylabel("Postings")
plt.savefig("data/processed/job_postings_forecast.png", bbox_inches='tight')
plt.close()

print("✅ Job postings forecast saved to data/processed/job_postings_forecast.csv")

# === 4️⃣ Forecast Average Salary ===
print("\n💰 Training Average Salary Forecast Model...")
df_sal = df[['date', 'avg_salary']].rename(columns={'date': 'ds', 'avg_salary': 'y'})

model_sal = Prophet(daily_seasonality=False, weekly_seasonality=False, yearly_seasonality=True)
model_sal.fit(df_sal)

future_sal = model_sal.make_future_dataframe(periods=12, freq='M')
forecast_sal = model_sal.predict(future_sal)

forecast_sal.to_csv("data/processed/salary_forecast.csv", index=False)

# Plot
model_sal.plot(forecast_sal)
plt.title("Forecast: Average Salary")
plt.xlabel("Date")
plt.ylabel("Average Salary ($)")
plt.savefig("data/processed/salary_forecast.png", bbox_inches='tight')
plt.close()

print("✅ Salary forecast saved to data/processed/salary_forecast.csv")

print("\n🎯 Forecasting complete! Check 'data/processed/' for results.")
