import pandas as pd

# Load 2-PZEM data
df = pd.read_csv("smart_grid_data.csv")

# Convert power columns to numeric
df["PZEM1_Power"] = pd.to_numeric(df["PZEM1_Power"], errors="coerce")
df["PZEM2_Power"] = pd.to_numeric(df["PZEM2_Power"], errors="coerce")

# Calculate power difference
df["Power_Difference"] = (
    df["PZEM1_Power"] - df["PZEM2_Power"]
).abs()

# Theft detection threshold
THRESHOLD = 5.0

# Detect abnormal difference
df["Status"] = df["Power_Difference"].apply(
    lambda x: "THEFT SUSPECTED" if x > THRESHOLD else "NORMAL"
)

# Show results
print("\n------ THEFT DETECTION RESULTS ------")

print(
    df[
        [
            "PZEM1_Power",
            "PZEM2_Power",
            "Power_Difference",
            "Status"
        ]
    ].tail(20)
)

# Save result
df.to_csv("theft_detection_result.csv", index=False)

print("\nDone!")
print("Result saved to theft_detection_result.csv")