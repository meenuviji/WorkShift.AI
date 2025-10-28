import pandas as pd
from prophet import Prophet
import matplotlib.pyplot as plt
import os

# ---------- CONFIG ----------
data_path = "data/processed/prophet_ready.csv"
output_path = "data/processed/forecast_results.csv"

# ---------- LOAD DATA ----------
if not os.path.exists(data_path):
    raise FileNotFoundError(f"❌ Data file not found: {data_path}")

df = pd.read_csv(data_path)
print("✅ Data loaded for Prophet training")
print(df.head())

# Prophet expects columns: ds (date) and y (target)
if "ds" not in df.columns or "y" not in df.columns:
    raise ValueError("❌ Columns 'ds' and 'y' are required for Prophet training!")

# ---------- TRAIN MODEL ----------
print("\n🚀 Training Prophet model (optimized for Windows)...")

model = Prophet(
    daily_seasonality=False,
    weekly_seasonality=False,
    yearly_seasonality=True,
    changepoint_prior_scale=0.05
)

# Fit the model (light optimization)
model.fit(df[["ds", "y"]])

# ---------- FORECAST ----------
future = model.make_future_dataframe(periods=5 * 365, freq="D")
forecast = model.predict(future)

# Save results
forecast.to_csv(output_path, index=False)
print(f"\n✅ Forecast completed successfully and saved to {output_path}")

# ---------- VISUALIZE ----------
try:
    fig1 = model.plot(forecast)
    plt.title("Job Trend Forecast (WorkShift.AI)")
    plt.xlabel("Date")
    plt.ylabel("Predicted Value")
    plt.show()

    fig2 = model.plot_components(forecast)
    plt.show()
except Exception as e:
    print(f"⚠️ Visualization skipped due to: {e}")
