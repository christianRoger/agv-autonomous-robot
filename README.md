# Autonomous AGV Robot – ESP32 & Linux

> **Autonomous Mobile Robot · ESP32 · Linux · Embedded Systems · Robotics · UART**

Prototype of an **autonomous mobile robot (AGV)** developed using an **ESP32 microcontroller** and an **Olimex A13 embedded Linux platform**.

The project combines real-time embedded control, Linux-based processing, serial communication and robotic system integration into a distributed robotic platform.

The system is being developed as an experimental platform for studying **robotics, embedded systems, autonomous navigation, hardware/software integration and distributed control**.

---

## Project Overview

The AGV is designed around a distributed architecture combining **real-time microcontroller control** with **Linux-based higher-level processing**.

The **ESP32** is responsible for real-time interaction with the robotic hardware, while the **Olimex A13** running Linux provides a higher-level computing environment for system management and future autonomous functions.

The two platforms communicate through a **UART serial interface**.

The architecture is designed to support future integration of:

* Motor control
* Sensor acquisition
* Autonomous navigation
* Obstacle detection
* Telemetry
* Remote control
* Path planning
* Higher-level robotic algorithms

---

## System Architecture

The AGV uses a distributed embedded architecture where the **ESP32** and **Olimex A13 Linux platform** perform different roles within the system.

```text
                         AGV SYSTEM
                              │
              ┌───────────────┴───────────────┐
              │                               │
              ▼                               ▼
        ┌─────────────┐                 ┌─────────────┐
        │    ESP32    │◄──── UART ────►│  Olimex A13 │
        │ Real-Time   │                 │    Linux    │
        │ Controller  │                 │ High-Level  │
        └──────┬──────┘                 │ Processing  │
               │                        └──────┬──────┘
               │                               │
        ┌──────┴──────┐                 ┌──────┴──────┐
        │             │                 │             │
        ▼             ▼                 ▼             ▼
     Motors        Sensors          Navigation    System
     Control       / I/O            Algorithms    Management
```

This separation allows time-sensitive hardware operations to remain on the ESP32 while higher-level processing can be performed on the Linux platform.

### ESP32 – Real-Time Controller

The ESP32 acts as the low-level controller of the robotic platform.

Its responsibilities include:

* Real-time hardware control
* GPIO management
* Motor control interface
* Sensor acquisition
* UART communication
* Command processing
* Time-sensitive control tasks
* Serial diagnostics and debugging

### Olimex A13 – Linux Platform

The Olimex A13 operates as the higher-level computing platform.

The board runs **Armbian Linux** and provides an environment for system-level applications and future autonomous functions.

Its role includes:

* Linux-based system management
* Serial communication with the ESP32
* Higher-level application processing
* Data handling
* Telemetry processing
* Future autonomous navigation algorithms
* Future integration of advanced sensors and computer vision

---

## Hardware & Connections

The prototype is built around an **ESP32 development board** and an **Olimex A13 embedded Linux platform**.

### Main Hardware

* ESP32 development board
* Olimex A13 embedded Linux platform
* Robotic chassis
* DC motors
* Motor drive system
* Power supply system
* UART serial communication interface
* Sensors and peripheral interfaces

### ESP32

The ESP32 provides the real-time control layer of the system.

Main interfaces include:

* GPIO
* UART
* Motor control interfaces
* Sensor interfaces
* Serial debugging

### Olimex A13

The Olimex A13 provides the Linux-based processing environment.

The board runs **Armbian Linux** and communicates with the ESP32 through UART.

---

## ESP32 ↔ Olimex UART Communication

Communication between the ESP32 and Olimex A13 is implemented through a **bidirectional UART serial interface**.

### Serial Configuration

The current prototype uses:

* **Baud rate:** 115200
* **Interface:** UART
* **Data format:** 8N1
* **Communication:** Bidirectional
* **Physical connection:** TX / RX / GND

The communication link has been tested between the ESP32 hardware serial interface and the Linux serial interface on the Olimex platform.

### Connection

```text
ESP32                         Olimex A13
─────                         ──────────

TX  ────────────────────────► RX

RX  ◄──────────────────────── TX

GND ───────────────────────── GND
```

### Communication Concept

```text
                UART @ 115200
        ┌─────────────────────────┐
        │                         │
        ▼                         ▼
   ┌─────────┐              ┌─────────────┐
   │  ESP32  │              │ Olimex A13  │
   │         │              │   Linux     │
   │ TX ────────────────► RX│             │
   │ RX ◄──────────────── TX│             │
   │ GND ───────────────── GND            │
   └─────────┘              └─────────────┘
```

The serial communication layer provides the foundation for exchanging commands, status information and telemetry between the real-time controller and the Linux platform.

---

## Software & Firmware

The software architecture is divided between the **ESP32 embedded firmware** and the **Linux environment running on the Olimex A13**.

### ESP32 Firmware

The ESP32 firmware is developed using **C/C++** and is responsible for low-level hardware interaction.

Main software concepts include:

* Embedded C/C++
* Hardware control
* GPIO management
* UART communication
* Command processing
* Real-time control
* Sensor interface management
* Motor control interface
* Serial logging
* Firmware debugging

### Linux Software

The Olimex A13 provides a Linux environment for higher-level applications.

The Linux layer is intended to handle:

* System-level applications
* Communication with the ESP32
* Data processing
* Telemetry
* High-level control logic
* Autonomous navigation
* Future robotics software integration

---

## Communication Protocol

The communication protocol is designed around a simple command-and-response model between the Linux platform and the ESP32.

The initial communication tests use basic messages to verify the UART connection and the correct operation of both platforms.

Example:

```text
Olimex A13  ──────►  ESP32
                    PING

Olimex A13  ◄──────  ESP32
                    PONG / STATUS
```

The protocol can be extended to support additional commands and telemetry information as the robotic platform evolves.

Potential future message types include:

* Motor commands
* Sensor data
* Robot status
* Battery information
* Navigation commands
* Telemetry
* Error/status messages

---

## Linux Environment

The Olimex A13 runs **Armbian Linux** as the operating system for the high-level computing layer.

The Linux environment provides access to standard serial interfaces and system tools required for development and debugging.

The platform is intended to provide the computational environment for future AGV functions such as:

* Autonomous navigation
* Path planning
* Sensor processing
* Telemetry
* Computer vision
* Remote control
* High-level decision making

---

## Development & Testing

Development is performed incrementally by validating individual hardware and software layers before integrating them into the complete robotic platform.

Current development activities include:

* ESP32 firmware development
* Olimex A13 Linux configuration
* UART communication testing
* Serial communication debugging
* Hardware interface validation
* ESP32 ↔ Linux integration
* Robotic platform development

The UART communication between the ESP32 and Olimex A13 has been successfully tested as part of the integration process.

---

## Project Status

**Status: Experimental Prototype**

The project is currently under active development.

The current platform establishes the foundation for communication between the **ESP32 real-time controller** and the **Olimex A13 Linux system**.

Future development will focus on integrating additional robotic functions, including:

* Motor control
* Sensor integration
* Autonomous navigation
* Obstacle detection
* Telemetry
* Path planning
* Higher-level robotic algorithms

---

## Future Development

Planned development areas include:

### Motion Control

Integration of the motor control system with the ESP32 firmware.

### Sensor Integration

Integration of sensors for environmental perception and robot state monitoring.

### Autonomous Navigation

Development of navigation and path-planning algorithms running on the Linux platform.

### Obstacle Detection

Integration of distance and environmental sensors for obstacle detection and avoidance.

### Telemetry

Implementation of a structured telemetry system between the ESP32 and Linux platform.

### Computer Vision

Future experimentation with computer vision and image-processing techniques on the Linux platform.

---

## Technologies

**ESP32 · C/C++ · Embedded Systems · Firmware · Armbian Linux · Olimex A13 · UART · Robotics · AGV · Real-Time Control · Distributed Systems**

---

## Repository Structure

The repository is organized to separate documentation, firmware examples and supporting resources.

```text
agv-autonomous-robot/
│
├── README.md
│
├── docs/
│   ├── Hardware & Connections.md
│   └── Software Architecture.md
│
├── examples/
│   └── ...
│
└── images/
    └── ...
```

Additional documentation and technical examples will be added as the project evolves.

---

## Author

**Christian Roger Scarparo**

Embedded Systems · Electronics · Firmware · Robotics · ESP32 · Linux
