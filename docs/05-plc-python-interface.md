# PLC ↔ Python Interface

## Purpose

Define the production data exchanged between the Beckhoff TwinCAT PLC
and the Python application through ADS.

## PLC → Python

| Variable | PLC Type | Description |
|---|---|---|
| TotalParts | UDINT | Total number of produced parts |
| OKParts | UDINT | Number of accepted parts |
| DefectParts | UDINT | Number of defective parts |
| DefectRate | LREAL | Percentage of defective parts |
| FaultCode | UINT | Current machine fault code |
| MachineStatus | STRING(30) | Current machine state |
| InspectionOK | BOOL | Result of the latest inspection |

## Python → PLC

The Python layer can later provide control or simulation inputs such as:

| Variable | PLC Type | Description |
|---|---|---|
| StartButton | BOOL | Start production |
| StopButton | BOOL | Stop production |
| EmergencyStop | BOOL | Emergency stop |
| WorkpieceSensor | BOOL | Workpiece detection |
| PositionSensor | BOOL | Inspection position |
| InspectionOK | BOOL | Inspection result |
| MachineFault | BOOL | Simulated machine fault |

## Fault Codes

| Code | Meaning |
|---:|---|
| 0 | No fault |
| 1 | Emergency Stop |
| 2 | Machine Fault |

## ADS Communication

ADS provides the communication layer between TwinCAT and Python.

The Python application will use the `pyads` library to access PLC
variables through the TwinCAT ADS interface.

Conceptual example:

```python
total_parts = plc.read_by_name("MAIN.TotalParts")
machine_status = plc.read_by_name("MAIN.MachineStatus")
defect_rate = plc.read_by_name("MAIN.DefectRate")
fault_code = plc.read_by_name("MAIN.FaultCode")

##Data Architecture
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

 ##Responsibilities
PLC
Real-time machine control
State machine execution
Production counters
Fault handling
Machine status
Python
ADS data acquisition
Data processing
Local persistence
Analytics
External automation integration