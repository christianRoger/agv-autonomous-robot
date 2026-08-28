# Communication Protocol

## Overview

The AGV communication layer provides a serial communication channel between the **ESP32 real-time controller** and the **Olimex A13 Linux platform**.

The communication interface is based on **UART at 115200 baud** and is designed to provide a foundation for exchanging commands, status information and telemetry between the two processing platforms.

The protocol is intentionally lightweight so it can be implemented on both the microcontroller and the Linux system with minimal overhead.

---

## Communication Architecture

The system uses a distributed architecture:

```text
                    AGV SYSTEM
                         │
          ┌──────────────┴──────────────┐
          │                             │
          ▼                             ▼
     ┌─────────┐                  ┌─────────────┐
     │  ESP32  │◄──── UART ─────►│ Olimex A13  │
     │         │                  │   Linux     │
     │ Real-   │                  │ High-Level  │
     │ Time    │                  │ Processing  │
     │ Control │                  │             │
     └─────────┘                  └─────────────┘
          │                             │
          ▼                             ▼
     Hardware                     Applications
     Control                     & Navigation
```

The ESP32 handles time-sensitive hardware operations, while the Linux platform is intended for higher-level processing.

---

## Serial Interface

The current prototype uses the following serial configuration:

| Parameter     | Value         |
| ------------- | ------------- |
| Interface     | UART          |
| Baud rate     | 115200        |
| Data bits     | 8             |
| Parity        | None          |
| Stop bits     | 1             |
| Format        | 8N1           |
| Communication | Bidirectional |
| Logic level   | 3.3 V         |

The ESP32 hardware UART is used for communication with the Olimex A13.

---

## ESP32 Configuration

The current ESP32 test configuration uses:

```text
UART interface: HardwareSerial(2)
RX: GPIO 16
TX: GPIO 17
Baud rate: 115200
```

Example:

```cpp
HardwareSerial OlimexSerial(2);

constexpr int RX_OLIMEX = 16;
constexpr int TX_OLIMEX = 17;

OlimexSerial.begin(
    115200,
    SERIAL_8N1,
    RX_OLIMEX,
    TX_OLIMEX
);
```

---

## Basic Communication Test

The initial communication test uses a simple heartbeat message.

The ESP32 periodically transmits:

```text
PING
```

The message is transmitted approximately every two seconds.

The purpose of this test is to verify the complete communication path before implementing a more complex protocol.

The test validates:

* UART configuration
* TX/RX wiring
* Baud rate
* Serial device configuration
* Data transmission
* Basic communication reliability

---

## Message Direction

The communication channel is bidirectional.

```text
ESP32                         Olimex A13
─────                         ──────────

PING ───────────────────────►

      ◄────────────────────── COMMAND

STATUS ─────────────────────►

TELEMETRY ──────────────────►
```

The ESP32 can transmit status and telemetry information to Linux, while the Linux platform can send commands to the ESP32.

---

## Protocol Concept

The communication protocol is designed around the concept of **commands and responses**.

A future structured message can follow a simple format such as:

```text
COMMAND|PARAMETER|VALUE
```

Example:

```text
MOTOR|LEFT|100
```

or:

```text
STATUS|READY|1
```

This structure is intentionally simple and human-readable, making it easy to debug through a serial terminal during development.

---

## Command Layer

The Linux platform can act as the higher-level controller for commands such as:

```text
START
STOP
RESET
STATUS
```

Future commands may include:

```text
MOTOR|LEFT|VALUE
MOTOR|RIGHT|VALUE
SENSOR|READ|ID
NAV|TARGET|X,Y
MODE|AUTO
MODE|MANUAL
```

These commands represent the planned communication model and can be expanded as additional AGV functions are implemented.

---

## Telemetry

The ESP32 can provide information about the current state of the robotic platform.

Potential telemetry data includes:

* Motor state
* Sensor readings
* Battery information
* Controller status
* Error conditions
* Current operating mode
* Communication status

A structured telemetry message could use a format such as:

```text
TELEMETRY|MOTOR_L=80|MOTOR_R=82|MODE=AUTO
```

The protocol can later be extended to use a more compact binary representation if required by performance or bandwidth constraints.

---

## Communication Flow

A typical high-level communication sequence is:

```text
        Olimex A13
             │
             │ Command
             ▼
           ESP32
             │
             │ Hardware control
             ▼
        Motors / Sensors
             │
             │ Status / Telemetry
             ▼
        Olimex A13
```

The Linux system can therefore request an operation, while the ESP32 performs the corresponding real-time hardware operation and returns the resulting status.

---

## Error Handling

Communication errors should be detected by both sides of the system.

Potential error conditions include:

* Invalid command
* Unknown command
* Missing parameter
* Invalid parameter value
* UART communication failure
* Timeout
* Unexpected message
* Hardware communication error

The protocol can later include explicit error responses such as:

```text
ERROR|INVALID_COMMAND
```

or:

```text
ERROR|INVALID_PARAMETER
```

---

## Future Protocol Improvements

As the AGV becomes more complex, the communication layer can be extended with:

* Message identifiers
* Sequence numbers
* Checksums
* Message length fields
* Acknowledgement messages
* Timeouts
* Command validation
* Telemetry packets
* Binary communication
* Communication state management

These improvements can increase communication reliability and make the protocol suitable for more complex autonomous robotic operations.

---

## Development Status

**Current status: Prototype communication layer**

The ESP32 ↔ Olimex A13 UART communication has been successfully tested using a basic serial communication test.

The current implementation establishes the foundation for future command, telemetry and autonomous-control communication between the real-time controller and the Linux platform.

The protocol will evolve as additional AGV hardware and autonomous functions are implemented.

