import pandas as pd
from sklearn.ensemble import IsolationForest

# Dataset load
df = pd.read_csv("smart_grid_data.csv")

# Clean column names
df.columns = df.columns.str.strip()

# Convert numerical columns
numeric_columns = [
    "PZEM1_Voltage",
    "PZEM1_Current",
    "PZEM1_Power",
    "PZEM2_Voltage",
    "PZEM2_Current",
    "PZEM2_Power"
]

for col in numeric_columns:
    df[col] = pd.to_numeric(df[col], errors="coerce")

# Remove rows with missing values
df = df.dropna(subset=numeric_columns).reset_index(drop=True)

# Create power difference
df["Power_Difference"] = (
    df["PZEM1_Power"] - df["PZEM2_Power"]
).abs()

# Features for Isolation Forest
X = df[
    [
        "PZEM1_Voltage",
        "PZEM1_Current",
        "PZEM1_Power",
        "PZEM2_Voltage",
        "PZEM2_Current",
        "PZEM2_Power",
        "Power_Difference"
    ]
]

# Isolation Forest
model = IsolationForest(
    contamination=0.05,
    random_state=42
)

model.fit(X)

# Prediction
prediction = model.predict(X)

# Convert prediction to status
df["Status"] = prediction

df["Status"] = df["Status"].replace({
    1: "Normal",
    -1: "Theft Suspected"
})

# Show results
print("\n------ ADVANCED THEFT DETECTION ------")

print(
    df[
        [
            "PZEM1_Power",
            "PZEM2_Power",
            "Power_Difference",
            "Status"
        ]
    ].head(20)
)

# Save result
df.to_csv("advanced_theft_result.csv", index=False)

print("\nAdvanced theft detection completed.")
print("File saved as advanced_theft_result.csv")
# Advanced Theft Detection Graph

import matplotlib.pyplot as plt

plt.figure(figsize=(10, 5))

# Power comparison
plt.plot(
    df.index,
    df["PZEM1_Power"],
    label="PZEM 1 Power"
)

plt.plot(
    df.index,
    df["PZEM2_Power"],
    label="PZEM 2 Power"
)

# Theft points
theft = df[df["Status"] == "Theft Suspected"]

plt.scatter(
    theft.index,
    theft["PZEM1_Power"],
    label="Theft Suspected",
    s=80
)

plt.title("Advanced Smart Grid Theft Detection")
plt.xlabel("Reading Number")
plt.ylabel("Power (W)")

plt.legend()
plt.grid()

plt.show()