# ICS Honeynet

An Industrial Control System (ICS) honeynet for simulating PLC-controlled industrial processes, exposing industrial protocols, and later integrating attack detection, routing, and deception.

## Project Goals

The long-term objective is to build a realistic ICS environment that can:

* Simulate industrial processes and PLC behaviour.
* Expose industrial protocols such as Modbus TCP.
* Detect suspicious client activity.
* Route attackers to simulated honeypots while legitimate users interact with the real process.
* Provide monitoring through CLI, REST APIs, and eventually a web dashboard.

---

## Current Features

### Plant Simulation

A simulated water distribution plant consisting of three interconnected tanks.

Each tank maintains:

* Water level
* Pump state
* Pump operating mode (Automatic / Manual)
* Manual pump command

The plant continuously updates its state according to predefined flow logic.

---

### Modbus TCP Server

The simulator exposes each tank as an individual Modbus device.

Each PLC currently exposes four holding registers:

| Address | Register    | Description             |
| ------: | ----------- | ----------------------- |
|       0 | LEVEL       | Tank level              |
|       1 | PUMP        | Current pump state      |
|       2 | PUMP_MODE   | Automatic / Manual mode |
|       3 | PUMP_MANUAL | Manual pump command     |

The server continuously synchronizes the simulated process with the Modbus datastore while also applying client commands back into the simulation.

---

### SCADA CLI

A terminal-based SCADA client allows an operator to:

* Monitor all PLCs
* Switch pumps between Automatic and Manual mode
* Send manual pump commands
* Receive connection failure notifications if the PLC server becomes unavailable

The CLI intentionally contains no Modbus logic and communicates only through the service layer.

---

## Architecture

```
                 +----------------+
                 |   CLI (SCADA)  |
                 +-------+--------+
                         |
                         |
                  PLCService API
                         |
                         |
                 Modbus TCP Client
                         |
========================= Network =========================
                         |
                 Modbus TCP Server
                         |
                         |
                 Plant Simulation
                 (Plant / Tank)
```

---

## Project Structure

```
honeynet/

├── client/
│   └── client.py
│
├── plc/
│   ├── plc.py
│   └── registers.py
│
├── services/
│   ├── PLC_service.py
│   └── Modbus_service.py
│
└── test/
```

---

## Design Principles

### Separation of Responsibilities

The project is structured into independent layers.

### Plant

Responsible for:

* Process simulation
* Tank logic
* Flow calculations
* Pump control

The plant has no knowledge of Modbus clients or user interfaces.

---

### Modbus Server

Responsible for:

* Running the Modbus TCP server
* Reading and writing Modbus registers
* Exposing the simulated PLC devices

It contains no plant logic.

---

### PLC Service

Acts as the application's communication layer.

Responsibilities include:

* Reading PLC data
* Writing PLC commands
* Translating Modbus registers into Python objects
* Hiding Pymodbus implementation details from higher layers

The CLI never communicates with Pymodbus directly.

---

### CLI

Responsible only for:

* Displaying menus
* Reading user input
* Presenting plant information

The CLI has no knowledge of:

* Register addresses
* Modbus function codes
* Network communication

---

## Technologies

* Python 3.12
* Pymodbus 4.x
* asyncio

---

## Planned Features

### Phase 1

* Improve project structure
* Additional PLC simulations
* Configuration files
* Logging

### Phase 2

* FastAPI interface
* REST endpoints for plant monitoring
* JSON responses

### Phase 3

* Network routing layer
* Legitimate client routing
* Honeypot routing
* Attack detection

### Phase 4

* SSH honeypot
* Event logging
* Alert generation
* Email notifications

### Phase 5

* Web dashboard
* Live plant visualization
* Multiple simulated industrial processes
* Docker deployment

---

## Current Status

The project currently provides a working industrial process simulator with Modbus TCP communication and a terminal-based SCADA client. The architecture has been separated into simulation, communication, and presentation layers to support future protocol expansion and honeynet functionality.
