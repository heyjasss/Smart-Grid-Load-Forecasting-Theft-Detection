import pandas as pd
import matplotlib.pyplot as plt

# ==========================================
# FINAL SMART GRID THEFT DETECTION
# ==========================================

print("\n======================================")
print("       FINAL THEFT DETECTION")
print("======================================")

# ------------------------------------------
# 1. Load normal baseline threshold
# ------------------------------------------

with open("theft_threshold.txt", "r") as file:
    THRESHOLD = float(file.read().strip())

print(f"\nUsing calculated threshold: {THRESHOLD:.3f} W")


# ------------------------------------------
# 2. Load data
# ------------------------------------------

df = pd.read_csv("normal_baseline_data.csv")


# ------------------------------------------
# 3. Convert power columns to numbers
# ------------------------------------------

df["PZEM1_Power"] = pd.to_numeric(
    df["PZEM1_Power"],
    errors="coerce"
)

df["PZEM2_Power"] = pd.to_numeric(
    df["PZEM2_Power"],
    errors="coerce"
)


# ------------------------------------------
# 4. Remove invalid readings
# ------------------------------------------

df = df.dropna(
    subset=[
        "PZEM1_Power",
        "PZEM2_Power"
    ]
).copy()


# ------------------------------------------
# 5. Calculate power difference
# ------------------------------------------

df["Power_Difference"] = (
    df["PZEM1_Power"] -
    df["PZEM2_Power"]
).abs()


# ------------------------------------------
# 6. Theft detection
# ------------------------------------------

df["Status"] = df["Power_Difference"].apply(
    lambda x:
        "THEFT SUSPECTED"
        if x > THRESHOLD
        else "NORMAL"
)


# ------------------------------------------
# 7. Statistics
# ------------------------------------------

total = len(df)

normal_count = (
    df["Status"] == "NORMAL"
).sum()

theft_count = (
    df["Status"] == "THEFT SUSPECTED"
).sum()

if total > 0:
    theft_percentage = (
        theft_count / total
    ) * 100
else:
    theft_percentage = 0


# ------------------------------------------
# 8. Display results
# ------------------------------------------

print("\n------ FINAL RESULTS ------")

print(f"Total Readings       : {total}")
print(f"Normal Readings      : {normal_count}")
print(f"Theft Suspected      : {theft_count}")
print(f"Theft Percentage     : {theft_percentage:.2f} %")

print("\n------ POWER DIFFERENCE ------")

print(
    f"Mean Difference      : "
    f"{df['Power_Difference'].mean():.3f} W"
)

print(
    f"Maximum Difference   : "
    f"{df['Power_Difference'].max():.3f} W"
)

print(
    f"Minimum Difference   : "
    f"{df['Power_Difference'].min():.3f} W"
)


# ------------------------------------------
# 9. Show last 20 readings
# ------------------------------------------

print("\n------ LAST 20 READINGS ------")

print(
    df[
        [
            "PZEM1_Power",
            "PZEM2_Power",
            "Power_Difference",
            "Status"
        ]
    ].tail(20).to_string(index=False)
)


# ------------------------------------------
# 10. Save final result
# ------------------------------------------

df.to_csv(
    "final_theft_detection_result.csv",
    index=False
)

print(
    "\nResult saved to "
    "final_theft_detection_result.csv"
)


# ------------------------------------------
# 11. Create graph
# ------------------------------------------

plt.figure(figsize=(12, 6))

plt.plot(
    df.index,
    df["PZEM1_Power"],
    label="PZEM1 Power",
    linewidth=2
)

plt.plot(
    df.index,
    df["PZEM2_Power"],
    label="PZEM2 Power",
    linewidth=2
)

plt.plot(
    df.index,
    df["Power_Difference"],
    label="Power Difference",
    linestyle="--",
    linewidth=2
)

plt.axhline(
    THRESHOLD,
    linestyle=":",
    linewidth=2,
    label=f"Theft Threshold ({THRESHOLD:.3f} W)"
)

plt.title(
    "Smart Grid Power Monitoring & Theft Detection"
)

plt.xlabel("Reading Number")
plt.ylabel("Power (W)")

plt.legend()

plt.grid(True)

plt.tight_layout()

plt.savefig(
    "final_theft_detection_graph.png",
    dpi=300
)

plt.show()


print("\n======================================")
print("       ANALYSIS COMPLETED")
print("======================================")