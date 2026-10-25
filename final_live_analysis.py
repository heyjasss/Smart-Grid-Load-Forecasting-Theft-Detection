import pandas as pd

# Load fresh live data
df = pd.read_csv("final_live_data.csv")

# Convert numeric columns
numeric_cols = [
    "PZEM1_Power",
    "PZEM2_Power",
    "Power_Difference"
]

for col in numeric_cols:
    df[col] = pd.to_numeric(df[col], errors="coerce")

df = df.dropna(subset=numeric_cols)

# Results
total = len(df)
normal = (df["Status"] == "NORMAL").sum()
theft = (df["Status"] == "THEFT SUSPECTED").sum()

theft_percentage = (
    theft / total * 100
    if total > 0 else 0
)

print("\n======================================")
print("       FINAL LIVE DATA ANALYSIS")
print("======================================")

print(f"Total Valid Readings : {total}")
print(f"Normal Readings      : {normal}")
print(f"Theft Suspected      : {theft}")
print(f"Theft Percentage     : {theft_percentage:.2f}%")

print("\n------ POWER STATISTICS ------")

print(
    f"PZEM1 Mean Power     : "
    f"{df['PZEM1_Power'].mean():.3f} W"
)

print(
    f"PZEM2 Mean Power     : "
    f"{df['PZEM2_Power'].mean():.3f} W"
)

print(
    f"Mean Difference      : "
    f"{df['Power_Difference'].mean():.3f} W"
)

print(
    f"Maximum Difference   : "
    f"{df['Power_Difference'].max():.3f} W"
)

# Save final analysis
df.to_csv(
    "final_live_analysis_result.csv",
    index=False
)

print("\nSaved:")
print("final_live_analysis_result.csv")