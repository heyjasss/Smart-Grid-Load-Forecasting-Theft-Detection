import serial
import csv
from datetime import datetime

# ESP32 COM PORT
ser = serial.Serial("COM4", 9600, timeout=1)

print("======================================")
print("      FINAL LIVE DATA LOGGER")
print("======================================")
print("ESP32 connected...")
print("Fresh logging started...")
print("Saving to: final_live_data.csv")
print("Press Ctrl+C to stop.\n")

# "w" = fresh file every time
with open("final_live_data.csv", "w", newline="") as file:

    writer = csv.writer(file)

    # Fresh header
    writer.writerow([
        "Time",
        "PZEM1_Voltage",
        "PZEM1_Current",
        "PZEM1_Power",
        "PZEM2_Voltage",
        "PZEM2_Current",
        "PZEM2_Power",
        "Power_Difference",
        "Status"
    ])

    try:

        while True:

            line = ser.readline().decode(
                "utf-8",
                errors="ignore"
            ).strip()

            if not line:
                continue

            # Ignore ESP32 text messages
            if (
                "SMART GRID" in line
                or "Threshold" in line
                or "NORMAL" == line
                or "THEFT SUSPECTED" in line
                or line.startswith("PZEM1")
                or line.startswith("!!!")
            ):
                continue

            parts = line.split(",")

            # We need:
            # V1,C1,P1,V2,C2,P2,Difference,Status
            if len(parts) >= 8:

                try:
                    v1 = float(parts[0])
                    c1 = float(parts[1])
                    p1 = float(parts[2])

                    v2 = float(parts[3])
                    c2 = float(parts[4])
                    p2 = float(parts[5])

                    difference = float(parts[6])
                    status = parts[7].strip()

                except ValueError:
                    continue

                timestamp = datetime.now().strftime(
                    "%Y-%m-%d %H:%M:%S"
                )

                writer.writerow([
                    timestamp,
                    v1,
                    c1,
                    p1,
                    v2,
                    c2,
                    p2,
                    difference,
                    status
                ])

                file.flush()

                print(
                    f"{timestamp} | "
                    f"P1={p1:.2f} W | "
                    f"P2={p2:.2f} W | "
                    f"Diff={difference:.3f} W | "
                    f"{status}"
                )

    except KeyboardInterrupt:

        print("\n\nLogging stopped by user.")

    finally:

        ser.close()

        print("ESP32 disconnected.")
        print("Fresh data saved to final_live_data.csv")