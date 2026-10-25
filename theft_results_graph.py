import pandas as pd
import matplotlib.pyplot as plt

# Load advanced theft detection results
df = pd.read_csv("advanced_theft_result.csv")

# Count Normal and Theft Suspected
status_counts = df["Status"].value_counts()

# -------------------------------
# Graph 1: Normal vs Theft
# -------------------------------

plt.figure(figsize=(8, 5))

status_counts.plot(
    kind="bar"
)

plt.title("Advanced Theft Detection Results")
plt.xlabel("Status")
plt.ylabel("Number of Readings")

plt.xticks(rotation=0)
plt.grid(axis="y")

plt.tight_layout()
plt.show()


# -------------------------------
# Graph 2: Power Difference
# -------------------------------

plt.figure(figsize=(10, 5))

plt.plot(
    df["Power_Difference"],
    linewidth=1.5
)

plt.axhline(
    df["Power_Difference"].mean(),
    linestyle="--",
    label="Average Power Difference"
)

plt.title("Power Difference Analysis")
plt.xlabel("Reading Number")
plt.ylabel("Power Difference (W)")

plt.legend()
plt.grid()

plt.tight_layout()
plt.show()


print("\n------ FINAL VISUALIZATION ------")
print("Total Readings:", len(df))
print("Normal:", status_counts.get("Normal", 0))
print(
    "Theft Suspected:",
    status_counts.get("Theft Suspected", 0)
)

print("\nGraphs generated successfully.")