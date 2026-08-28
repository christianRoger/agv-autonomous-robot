# Hardware & Connections

## Overview

The Autonomous AGV Robot prototype is based on a distributed embedded architecture combining an **ESP32 microcontroller** with an **Olimex A13 embedded Linux platform**.

The hardware is divided into two main processing layers:

* **ESP32** — real-time control, GPIO management and hardware interfaces.
* **Olimex A13** — Linux-based high-level processing and system management.

The two platforms communicate through a **bidirectional UART serial interface**.

---

## System Hardware

### Main Components

The current prototype architecture includes:

* ESP32 development board
* Olimex A13 embedded Linux platform
* Robotic chassis
* DC motor system
* Motor control interface
* Power supply system
* UART communication interface
* GPIO-connected peripherals and sensors

The hardware architecture is designed to allow additional sensors and actuators to be integrated as the AGV evolves.

---

## ESP32

The ESP32 is used as the **real-time controller** of the robotic platform.

Its main responsibilities include:

* GPIO control
* Real-time hardware operations
* Motor control interface
* Sensor interfaces
* UART communication
* Command reception
* Status and telemetry transmission

The ESP32 is responsible for operations where deterministic timing and direct hardware access are important.

---

## Olimex A13

The **Olimex A13** operates as the Linux-based processing platform.

The board runs **Armbian Linux** and provides a higher-level computing environment for the AGV.

Its intended responsibilities include:

* System management
* UART communication
* High-level application processing
* Data handling
* Future autonomous navigation algorithms
* Future sensor processing
* Future computer vision integration

This architecture keeps time-sensitive hardware operations on the ESP32 while allowing more complex processing to be performed on the Linux platform.

---

# UART Connection

The primary communication interface between the ESP32 and Olimex A13 is a **3.3 V UART serial connection**.

The connection uses three signals:

```text
ESP32                         Olimex A13
─────                         ──────────

TX  ────────────────────────► RX

RX  ◄──────────────────────── TX

GND ───────────────────────── GND
```

TX and RX are crossed between the two devices.

A common ground is required for reliable communication.

---

## Serial Configuration

The prototype communication test uses:

| Parameter     | Configuration |
| ------------- | ------------- |
| Interface     | UART          |
| Baud rate     | 115200        |
| Data bits     | 8             |
| Parity        | None          |
| Stop bits     | 1             |
| Communication | Bidirectional |
| Logic level   | 3.3 V         |

The serial configuration corresponds to the standard **115200 8N1** configuration.

---

# ESP32 UART Configuration

The ESP32 test firmware uses a hardware UART interface.

The prototype test configuration uses:

```text
RX = GPIO 16
TX = GPIO 17
Baud rate = 115200
```

Example configuration:

```cpp
HardwareSerial OlimexSerial(2);

constexpr int RX_OLIMEX = 16;
constexpr int TX_OLIMEX = 17;

void setup()
{
    OlimexSerial.begin(
        115200,
        SERIAL_8N1,
        RX_OLIMEX,
        TX_OLIMEX
    );
}
```

The UART interface is used to exchange commands and status information between the ESP32 and the Linux platform.

---

# Olimex A13 Serial Interface

The Olimex A13 runs **Armbian Linux** and exposes multiple serial interfaces through Linux device nodes.

During hardware testing, the following serial devices were identified:

```text
/dev/ttyS0
/dev/ttyS1
/dev/ttyS2
/dev/ttyS3
```

The correct device depends on the physical UART interface and board configuration being used.

Serial interfaces can be inspected from Linux using:

```bash
ls /dev/ttyS*
```

The communication layer was tested by establishing a serial connection between the ESP32 hardware UART and the corresponding Olimex UART interface.

---

# Communication Test

The initial communication test uses a simple heartbeat message from the ESP32.

The ESP32 periodically transmits:

```text
PING
```

The message is sent approximately every two seconds.

Example communication flow:

```text
ESP32
  │
  │  PING
  ▼
Olimex A13
  │
  │  Serial processing
  ▼
Linux application
```

This basic test is used to verify:

* UART electrical connection
* TX/RX configuration
* Baud rate configuration
* Serial device selection
* Data transmission
* Communication reliability

The simple protocol can later be extended to support structured commands, telemetry and control messages.

---

# UART Communication Architecture

The communication architecture is designed as a **distributed control system**.

```text
                    AGV SYSTEM
                         │
          ┌──────────────┴──────────────┐
          │                             │
          ▼                             ▼
     ┌─────────┐                  ┌─────────────┐
     │  ESP32  │◄──── UART ─────►│ Olimex A13  │
     │         │                  │   Armbian   │
     │ Real-   │                  │   Linux     │
     │ Time    │                  │             │
     │ Control │                  │ High-Level  │
     └────┬────┘                  │ Processing  │
          │                       └──────┬──────┘
          │                              │
     ┌────┴────┐                    ┌────┴────┐
     │ Motors  │                    │ Linux   │
     │ Sensors │                    │ Apps    │
     │ GPIO    │                    │ Data    │
     └─────────┘                    └─────────┘
```

The architecture separates low-level hardware control from high-level processing.

---

# Power and Ground

The UART connection requires a common ground reference between the ESP32 and Olimex A13.

```text
ESP32 GND ───────────────── Olimex GND
```

The power supply architecture for motors and other high-current loads is kept separate from the logic-level communication signals.

Care must be taken to ensure that the logic interfaces operate at compatible voltage levels.

---

# Future Hardware Expansion

The hardware architecture is designed to support future expansion.

Potential additions include:

* Motor drivers
* Wheel encoders
* Ultrasonic sensors
* Distance sensors
* IMU
* LiDAR
* Camera modules
* Additional GPIO peripherals
* Wireless communication
* Battery monitoring

These components can be integrated while maintaining the separation between the ESP32 real-time control layer and the Linux processing layer.

---

# Hardware Development Status

**Current status: Prototype**

The ESP32 ↔ Olimex A13 UART communication has been tested as part of the prototype development.

The current hardware architecture establishes the communication foundation required for future AGV functions, including motor control, sensor acquisition, telemetry and autonomous navigation.

The hardware and communication architecture will continue to evolve as additional robotic subsystems are implemented.

