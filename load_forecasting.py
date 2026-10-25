import pandas as pd
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt

# ===============================
# LOAD FINAL DATA
# ===============================

df = pd.read_csv("final_live_data.csv")

df.columns = df.columns.str.strip()

# Convert power to numeric
df["PZEM1_Power"] = pd.to_numeric(
    df["PZEM1_Power"],
    errors="coerce"
)

# Remove invalid readings
df = df.dropna(
    subset=["PZEM1_Power"]
).reset_index(drop=True)

# ===============================
# CREATE TIME/READING INDEX
# ===============================

df["Index"] = range(len(df))

X = df[["Index"]]
y = df["PZEM1_Power"]

# ===============================
# TRAIN MODEL
# ===============================

model = LinearRegression()
model.fit(X, y)

# Existing predictions
df["PredictedPower"] = model.predict(X)

# ===============================
# NEXT POWER FORECAST
# ===============================

next_input = pd.DataFrame({
    "Index": [len(df)]
})

next_power = model.predict(next_input)[0]

# ===============================
# RESULTS
# ===============================

print("\n===================================")
print("       SMART GRID LOAD FORECAST")
print("===================================")

print("Total Readings       :", len(df))
print("Average Actual Power :", round(y.mean(), 3), "W")
print("Minimum Power        :", round(y.min(), 3), "W")
print("Maximum Power        :", round(y.max(), 3), "W")
print("Next Predicted Power :", round(next_power, 3), "W")

# ===============================
# SAVE FORECAST RESULT
# ===============================

forecast_result = pd.DataFrame({
    "Next_Reading_Index": [len(df)],
    "Predicted_Power_W": [round(next_power, 3)]
})

forecast_result.to_csv(
    "load_forecasting_result.csv",
    index=False
)

# ===============================
# GRAPH
# ===============================

plt.figure(figsize=(10, 5))

plt.plot(
    df["Index"],
    df["PZEM1_Power"],
    label="Actual Power"
)

plt.plot(
    df["Index"],
    df["PredictedPower"],
    label="Predicted Trend"
)

plt.scatter(
    len(df),
    next_power,
    s=100,
    label="Next Prediction"
)

plt.title("Smart Grid Load Forecasting")
plt.xlabel("Reading Number")
plt.ylabel("Power (W)")

plt.legend()
plt.grid()
plt.tight_layout()

# Save graph
plt.savefig(
    "load_forecasting_graph.png",
    dpi=160
)

plt.show()