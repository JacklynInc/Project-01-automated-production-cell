# PLC Architecture

## Controller

The production cell is implemented as a Beckhoff TwinCAT PLC project
using IEC 61131-3 Structured Text.

The PLC contains the real-time machine-control logic, while Python
handles data processing and external automation.

## State Machine

The production sequence uses the following states:

IDLE
STARTING
RUNNING
WORKPIECE_DETECTED
INSPECTING
SORTING
RECORDING
FAULT
RESET

## Inputs

| Input | Type | Description |
|---|---|---|
| StartButton | BOOL | Starts production |
| StopButton | BOOL | Stops normal production |
| EmergencyStop | BOOL | Safety-related stop |
| WorkpieceSensor | BOOL | Detects a workpiece |
| PositionSensor | BOOL | Confirms inspection position |
| InspectionOK | BOOL | Inspection result |
| MachineFault | BOOL | Technical machine fault |

## Outputs

| Output | Type | Description |
|---|---|---|
| ConveyorMotor | BOOL | Conveyor control |
| OKSorter | BOOL | Sorts accepted workpieces |
| DefectSorter | BOOL | Sorts rejected workpieces |
| GreenIndicator | BOOL | Normal operation indication |
| RedIndicator | BOOL | Fault indication |

## Timers

| Timer | Duration | Purpose |
|---|---:|---|
| StartTimer | 2 s | Startup delay |
| InspectionTimer | 1 s | Inspection duration |
| SortingTimer | 500 ms | Sorting duration |

## Production KPIs

The PLC calculates:

- Total Parts
- OK Parts
- Defect Parts
- Defect Rate

## Fault Handling

| Fault Code | Meaning |
|---:|---|
| 0 | No fault |
| 1 | Emergency Stop |
| 2 | Machine Fault |

When a fault occurs, the conveyor and sorters are stopped and
the machine enters the FAULT state.

## Machine Status

The PLC exposes a human-readable `MachineStatus` variable for
monitoring and future HMI/Python integration.

## Communication Architecture

```text
Beckhoff TwinCAT PLC
        │
        │ ADS
        ▼
     Python
        │
        ├── SQLite
        │
        └── n8n
              │
              ▼
           Airtable

## Responsibilities

### PLC

- Real-time machine control
- State machine execution
- Sensor processing
- Actuator control
- Production counters
- Fault handling
- Machine status

### Python

- PLC data acquisition
- Data processing
- Local persistence
- Analytics
- Integration with external automation services

### n8n / Airtable

- Workflow automation
- Production data integration
- Cloud-based production records