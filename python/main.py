from enum import Enum
import time
from inspection import inspect_workpiece
import sqlite3
from datetime import datetime
from statistics import get_production_statistics

import requests
from ads_client import connect_to_plc, read_production_data, disconnect_from_plc


# n8n Webhook
N8N_WEBHOOK_URL = "https://j01.app.n8n.cloud/webhook/Production-result"


# Database
connection = sqlite3.connect("data/production.db")
cursor = connection.cursor()

# Beckhoff PLC
plc = connect_to_plc()
print("Connected to TwinCAT PLC via ADS")
production_data = read_production_data(plc)
print("PLC production data:")
print(production_data)

disconnect_from_plc(plc)


# State machine
class State(Enum):
    IDLE = 1
    STARTING = 2
    RUNNING = 3
    WORKPIECE_DETECTED = 4
    INSPECTING = 5
    SORTING = 6
    RECORDING = 7
    FAULT = 8
    RESET = 9


# Inputs
start = True
stop = False
emergency_stop = False
reset = False

from sensors import workpiece_detected, position_reached, fault_detected

# Inspection
inspection_result = None


# Production counters
total_parts = 0
ok_parts = 0
defect_parts = 0


# Outputs
conveyor_motor = False
ok_sorter = False
defect_sorter = False


# Initial state
state = State.IDLE


# State machine
while False:

    # Emergency stop
    if emergency_stop:
        state = State.FAULT

    # Simulated machine fault
    elif fault_detected():
        state = State.FAULT

    # IDLE
    elif state == State.IDLE:
        if start:
            state = State.STARTING

    # STARTING
    elif state == State.STARTING:
        state = State.RUNNING

    # RUNNING
    elif state == State.RUNNING:
        conveyor_motor = True

        if stop:
            conveyor_motor = False
            state = State.IDLE

        elif workpiece_detected():
            state = State.WORKPIECE_DETECTED

    # WORKPIECE DETECTED
    elif state == State.WORKPIECE_DETECTED:
        if position_reached():
            state = State.INSPECTING

    # INSPECTING
    elif state == State.INSPECTING:
        inspection_result = inspect_workpiece()
        state = State.SORTING

    # SORTING
    elif state == State.SORTING:

        if inspection_result == "OK":
            ok_sorter = True
            print("Sorting: OK")

        else:
            defect_sorter = True
            print("Sorting: DEFECT")

        state = State.RECORDING

    # RECORDING
    elif state == State.RECORDING:

        # Create one timestamp for both database and n8n
        timestamp = datetime.now().isoformat()

        # Update counters
        total_parts += 1

        if inspection_result == "OK":
            ok_parts += 1
        else:
            defect_parts += 1

        # Save production result to SQLite
        cursor.execute(
            """
            INSERT INTO production (result, timestamp)
            VALUES (?, ?)
            """,
            (inspection_result, timestamp)
        )

        connection.commit()

        total, ok, defect, defect_rate = get_production_statistics(connection)

        print(
            f"Database statistics: "
            f"Total: {total} | OK: {ok} | "
            f"DEFECT: {defect} | Defect rate: {defect_rate:.2f}%"
)

        # Get the actual SQLite production ID
        production_id = cursor.lastrowid

        # Send production result to n8n
        try:
            response = requests.post(
                N8N_WEBHOOK_URL,
                json={
                    "production_id": production_id,
                    "result": inspection_result,
                    "timestamp": timestamp,
                    "total_parts": total,
                    "ok_parts": ok,
                    "defect_parts": defect,
                    "defect_rate": defect_rate
                },
                timeout=10
            )

            print(f"n8n response: {response.status_code}")

        except requests.RequestException as error:
            print(f"n8n connection failed: {error}")

        # Production status
        print(f"Production ID: {production_id}")
        print(f"Production result: {inspection_result}")
        print(f"Total: {total_parts} | OK: {ok_parts} | DEFECT: {defect_parts}")

        # Reset sorters
        ok_sorter = False
        defect_sorter = False

        # Continue production
        state = State.RUNNING

    # FAULT
    elif state == State.FAULT:

        conveyor_motor = False
        ok_sorter = False
        defect_sorter = False

        print("FAULT: Machine stopped")

        if not emergency_stop:
            input("Fault: Press Enter to reset the machine...")
            reset = True

            if reset:
                state = State.RESET
                reset = False
    # RESET
    elif state == State.RESET:
        state = State.IDLE

    # Cycle delay
    time.sleep(0.25)