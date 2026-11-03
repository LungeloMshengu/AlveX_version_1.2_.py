import random
import csv
import os
import time
from datetime import datetime

# ==========================================
# ALVEX TECHNOLOGIES
# MACHINE INTELLIGENCE V1.2
# ==========================================

MAX_TEMPERATURE = 80
MAX_VIBRATION = 8.0
TOTAL_CYCLES = 5

FILENAME = "alvex_v12_data.csv"

# 1. CREATE FACTORY MACHINES

machines = []

for number in range(1, 11):
    machines.append({
        "id": f"MOTOR-{number:03d}",
        "health": 100,
        "temperature_alerts": 0,
        "vibration_alerts": 0,
        "total_temperature": 0,
        "total_vibration": 0,
        "readings": 0
    })


# 2. READ MACHINE TEMPERATURE

def read_machine_temperature():
    return random.randint(35, 100)


# 3. READ MACHINE VIBRATION

def vibration_level():
    return round(random.uniform(1, 12), 2)


# 4. DETECT ABNORMAL READINGS

def abnormal_readings(temperature, vibration):

    problems = []

    if temperature > MAX_TEMPERATURE:
        problems.append("HIGH TEMPERATURE")

    if vibration > MAX_VIBRATION:
        problems.append("EXCESSIVE VIBRATION")

    return problems


# 5. CALCULATE MACHINE HEALTH

def calculate_health(machine):

    penalty = (
        machine["temperature_alerts"] * 5
        + machine["vibration_alerts"] * 5
    )

    health = max(0, 100 - penalty)

    return health


# 6. CLASSIFY MACHINE RISK

def classify_risk(health):

    if health >= 80:
        return "LOW"

    elif health >= 60:
        return "MEDIUM"

    else:
        return "HIGH"


# 7. GENERATE WARNINGS

def generate_warnings(machine_id, problems):

    if problems:

        print("WARNING:", machine_id)

        for problem in problems:
            print("  ALERT:", problem)

    else:
        print("STATUS: NORMAL")


# 8. SAVE MACHINE DATA

def save_readings(machine, temperature,
                  vibration, problems):

    file_exists = os.path.exists(FILENAME)

    needs_header = (
        not file_exists or os.path.getsize(FILENAME) == 0
    )

    with open(FILENAME, "a", newline="") as file:

        writer = csv.writer(file)

        if needs_header:
            writer.writerow([
                "Timestamp",
                "Machine ID",
                "Temperature",
                "Vibration",
                "Health Score",
                "Risk",
                "Problems"
            ])

        writer.writerow([
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            machine["id"],
            temperature,
            vibration,
            machine["health"],
            classify_risk(machine["health"]),
            "; ".join(problems) if problems else "Normal"
        ])


# 9. MONITOR INDIVIDUAL MACHINES

def monitor_machine(machine):

    temperature = read_machine_temperature()
    vibration = vibration_level()

    machine["readings"] += 1

    machine["total_temperature"] += temperature
    machine["total_vibration"] += vibration

    problems = abnormal_readings(
        temperature, vibration
    )

    if "HIGH TEMPERATURE" in problems:
        machine["temperature_alerts"] += 1

    if "EXCESSIVE VIBRATION" in problems:
        machine["vibration_alerts"] += 1

    machine["health"] = calculate_health(machine)

    print("\nMachine:", machine["id"])
    print("Temperature:", temperature, "C")
    print("Vibration:", vibration, "mm/s")

    generate_warnings(machine["id"], problems)

    print("Health:", machine["health"], "/100")
    print("Risk:", classify_risk(machine["health"]))

    save_readings(
        machine, temperature, vibration, problems
    )


# 10. FACTORY DASHBOARD

def factory_dashboard():

    print("\n======================================")
    print("       ALVEX FACTORY DASHBOARD")
    print("======================================")

    print("MACHINE       HEALTH       RISK")

    for machine in machines:

        print(
            machine["id"],
            "     ",
            str(machine["health"]) + "/100",
            "     ",
            classify_risk(machine["health"])
        )


# 11. FACTORY PERFORMANCE REPORT

def factory_report():

    print("\n======================================")
    print("       FACTORY HEALTH REPORT")
    print("======================================")

    total_health = 0
    high_risk = 0
    medium_risk = 0
    low_risk = 0

    for machine in machines:

        health = machine["health"]
        risk = classify_risk(health)

        total_health += health

        if risk == "HIGH":
            high_risk += 1

        elif risk == "MEDIUM":
            medium_risk += 1

        else:
            low_risk += 1

        average_temp = (
            machine["total_temperature"]
            / machine["readings"]
        )

        average_vibration = (
            machine["total_vibration"]
            / machine["readings"]
        )

        print("\n", machine["id"])
        print("Health:", health, "/100")
        print("Risk:", risk)
        print("Average temperature:", round(average_temp, 2))
        print("Average vibration:", round(average_vibration, 2))
        print("Temperature alerts:", machine["temperature_alerts"])
        print("Vibration alerts:", machine["vibration_alerts"])

    print("\n======================================")
    print("TOTAL MACHINES:", len(machines))
    print("AVERAGE FACTORY HEALTH:", round(total_health / len(machines), 2))
    print("LOW RISK:", low_risk)
    print("MEDIUM RISK:", medium_risk)
    print("HIGH RISK:", high_risk)
    print("======================================")

    print("Data saved in:", FILENAME)


# 12. START ALVEX

def start_system():

    print("======================================")
    print("       ALVEX TECHNOLOGIES")
    print("       MACHINE INTELLIGENCE")
    print("       VERSION 1.2")
    print("======================================")

    for cycle in range(1, TOTAL_CYCLES + 1):

        print("\nFACTORY CYCLE:", cycle)

        for machine in machines:
            monitor_machine(machine)

        print("\nCycle completed.")
        time.sleep(1)

    factory_dashboard()
    factory_report()


# RUN PROGRAM

start_system()