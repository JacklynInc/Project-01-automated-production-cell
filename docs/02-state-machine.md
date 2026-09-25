# Automated Production Cell — State Machine

## Purpose

The production cell is controlled using a state machine.
Each state represents a defined operating condition of the machine.

## States

### IDLE
- Machine is stopped.
- Conveyor is OFF.
- Sorter actuators are in their home position.
- System waits for START.

### STARTING
- Safety conditions are checked.
- Sensors are initialized.
- Actuators are confirmed to be in their home position.
- If all conditions are valid, move to RUNNING.

### RUNNING
- Conveyor is ON.
- System monitors the workpiece sensor.
- When a workpiece is detected, move to WORKPIECE_DETECTED.

### WORKPIECE_DETECTED
- Conveyor movement is controlled.
- System waits for the position sensor.
- When the correct position is confirmed, move to INSPECTING.

### INSPECTING
- The workpiece is inspected.
- Inspection result is determined:
  - OK
  - DEFECT
- Move to SORTING.

### SORTING
- The appropriate actuator is activated.
- OK workpieces are sent to the OK output.
- Defective workpieces are sent to the DEFECT output.
- Move to RECORDING.

### RECORDING
- Production result is recorded.
- Production counter is updated.
- Return to RUNNING.

### FAULT
- Conveyor is stopped.
- Actuators are placed in a safe state.
- Fault information is recorded.
- System waits for RESET.

### RESET
- Fault condition is cleared.
- Sensors and actuators are checked.
- If the system is safe, return to IDLE.

## State Flow

```text
IDLE
  |
  v
STARTING
  |
  v
RUNNING
  |
  v
WORKPIECE_DETECTED
  |
  v
INSPECTING
  |
  v
SORTING
  |
  v
RECORDING
  |
  +--------> RUNNING


Any State
    |
    v
  FAULT
    |
    v
  RESET
    |
    v
  IDLE

  INPUTS
I0.0  Start
I0.1  Stop
I0.2  Emergency Stop
I0.3  Workpiece Sensor
I0.4  Position Sensor

OUTPUTS
Q0.0  Conveyor Motor
Q0.1  OK Sorter
Q0.2  Defect Sorter
Q0.3  Green Indicator
Q0.4  Red Indicator