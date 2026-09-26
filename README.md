# Automated Production Cell

A small industrial automation project combining Python, Beckhoff TwinCAT,
PLC programming, SQLite, n8n, and Airtable.

A small industrial automation project combining Python, Beckhoff TwinCAT,
PLC programming, SQLite, n8n, and Airtable.

## Project Overview

This project simulates and implements an automated production cell
that detects, inspects, sorts, and records manufactured workpieces.

The project was developed in two stages:

1. A production-cell control sequence was first simulated in Python.
2. The same state-machine logic was then implemented using
   IEC 61131-3 Structured Text in Beckhoff TwinCAT.

The resulting architecture connects real-time PLC control with
Python-based data processing and workflow automation.

## Project Overview

The project simulates and implements an automated production cell
that detects, inspects, sorts, and records manufactured workpieces.

The project was developed in two stages:

1. A production-cell control sequence was first simulated in Python.
2. The same state-machine logic was then implemented using
   IEC 61131-3 Structured Text in Beckhoff TwinCAT.

This creates a bridge between software development, industrial PLC
control, and production-data automation.

## Production Sequence

```text
IDLE
  ↓
STARTING
  ↓
RUNNING
  ↓
WORKPIECE_DETECTED
  ↓
INSPECTING
  ↓
SORTING
  ↓
RECORDING
  ↓
RUNNING

Fault conditions can transition the machine to:

FAULT → RESET → IDLE
 
## Technology Stack

### Industrial Automation

- Beckhoff TwinCAT 3
- IEC 61131-3 Structured Text
- PLC state-machine programming
- Timers
- Fault handling

### Python / Data

- Python
- SQLite
- pyads
- Data processing and analytics

### Automation / Integration

- n8n
- Airtable
- Webhooks

## System Architecture
                    ┌──────────────────────┐
                    │ Beckhoff TwinCAT PLC │
                    │                      │
                    │ State Machine        │
                    │ Sensors              │
                    │ Actuators             │
                    │ Production KPIs       │
                    │ Fault Handling        │
                    └──────────┬───────────┘
                               │
                              ADS
                               │
                               ▼
                    ┌──────────────────────┐
                    │ Python Data Layer     │
                    │                      │
                    │ Data Acquisition      │
                    │ Processing            │
                    │ SQLite                │
                    │ Analytics             │
                    └──────────┬───────────┘
                               │
                              n8n
                               │
                               ▼
                    ┌──────────────────────┐
                    │ Airtable             │
                    │ Production Records   │
                    └──────────────────────┘

## PLC Responsibilities

- Real-time machine control
- State-machine execution
- Sensor processing
- Actuator control
- Production counters
- Fault handling
- Machine status

## Python Responsibilities

- PLC data acquisition via ADS
- Data processing
- Local persistence
- Analytics
- Integration with external automation services

## Automation Layer

n8n receives production data and sends it to Airtable,
where production records and KPIs can be monitored.

## Current PLC Implementation

The TwinCAT PLC currently implements:

- Production state machine
- Start/stop control
- Startup timer
- Workpiece detection
- Position detection
- Inspection timing
- OK/DEFECT sorting
- Production counters
- Defect-rate calculation
- Emergency-stop handling
- Machine-fault handling
- Fault codes
- Machine status

## Project Status

### Completed

- Python production-cell simulation
- SQLite production database
- n8n production webhook
- Airtable production records
- TwinCAT PLC project
- IEC 61131-3 Structured Text implementation
- PLC state machine
- PLC fault handling
- PLC production KPIs
- PLC/Python architecture documentation

### Next

- ADS communication between TwinCAT and Python
- Python `pyads` integration
- Reading PLC production data
- Integrating PLC data with the existing SQLite/n8n/Airtable pipeline

## Learning Objective

The project is designed as a practical bridge between:

**Mechanical Engineering → Industrial Automation → PLC Programming → Python → AI/Data Automation**

The goal is to understand how real-time industrial control systems
can connect with modern software and data-processing workflows.

