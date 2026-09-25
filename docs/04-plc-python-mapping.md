# PLC ↔ Python State Mapping

The Python production-cell simulation and the Beckhoff TwinCAT PLC
implementation use the same state-machine architecture.

## State Mapping

| PLC State | Python State | Function |
|---|---|---|
| IDLE | State.IDLE | Machine waiting for start |
| STARTING | State.STARTING | Startup sequence |
| RUNNING | State.RUNNING | Conveyor running |
| WORKPIECE_DETECTED | State.WORKPIECE_DETECTED | Workpiece detected |
| INSPECTING | State.INSPECTING | Quality inspection |
| SORTING | State.SORTING | OK/DEFECT sorting |
| RECORDING | State.RECORDING | Production data recorded |
| FAULT | State.FAULT | Machine stopped because of fault |
| RESET | State.RESET | Return to idle |

## Inputs

The PLC inputs correspond to conditions previously simulated in Python:

| PLC Input | Python Equivalent |
|---|---|
| StartButton | `start` |
| StopButton | `stop` |
| EmergencyStop | `emergency_stop` |
| WorkpieceSensor | `workpiece_detected()` |
| PositionSensor | `position_reached()` |
| InspectionOK | `inspect_workpiece()` |
| MachineFault | `fault_detected()` |

## Outputs

| PLC Output | Python Equivalent |
|---|---|
| ConveyorMotor | Conveyor control |
| OKSorter | OK sorting |
| DefectSorter | Defect sorting |
| GreenIndicator | Normal operation |
| RedIndicator | Fault condition |

## Data Flow

```text
Python Simulation
       │
       │ State-machine logic
       ▼
Beckhoff TwinCAT PLC
       │
       │ ADS
       ▼
Python Data Layer
       │
       ├── SQLite
       │
       └── n8n
             │
             ▼
          Airtable

## Architecture Principle

The PLC is responsible for deterministic real-time machine control.

Python is used for data acquisition, processing, persistence,
analytics, and integration with external automation services.

The same production sequence is therefore represented at both
the industrial-control and software/data-processing levels.

