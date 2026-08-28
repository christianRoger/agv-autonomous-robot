```python
#!/usr/bin/env python3

"""
TECH3D AGV Robot
Olimex A13 <-> ESP32 UART Communication Example

Demonstrates:
- Linux serial communication
- UART communication with ESP32
- Command transmission
- Response reception
- Periodic heartbeat
- Simple communication protocol

This is a simplified public example extracted from the
communication concepts used in the AGV platform.

The complete AGV Linux software and navigation logic are
not included in this repository.
"""

import serial
import time


# ============================================================================
# UART CONFIGURATION
# ============================================================================

UART_DEVICE = "/dev/ttyS1"
UART_BAUDRATE = 115200

SERIAL_TIMEOUT = 1.0


# ============================================================================
# UART INTERFACE
# ============================================================================

class AGVUart:
    """UART interface between Olimex A13 Linux and ESP32."""

    def __init__(self, device: str, baudrate: int):
        self.device = device
        self.baudrate = baudrate
        self.serial = None

    def connect(self):
        """Open the serial interface."""

        try:
            self.serial = serial.Serial(
                port=self.device,
                baudrate=self.baudrate,
                bytesize=serial.EIGHTBITS,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
                timeout=SERIAL_TIMEOUT
            )

            print(f"[UART] Connected to {self.device}")
            print(f"[UART] Baud rate: {self.baudrate}")

            return True

        except serial.SerialException as error:
            print(f"[UART] Connection error: {error}")
            return False

    def send(self, message: str):
        """Send a newline-terminated command to the ESP32."""

        if self.serial is None:
            print("[UART] Interface not connected")
            return False

        try:
            packet = f"{message}\n".encode("utf-8")

            self.serial.write(packet)
            self.serial.flush()

            print(f"[UART] TX: {message}")

            return True

        except serial.SerialException as error:
            print(f"[UART] TX error: {error}")
            return False

    def receive(self):
        """Read one line from the ESP32."""

        if self.serial is None:
            return None

        try:
            line = self.serial.readline()

            if line:
                message = line.decode(
                    "utf-8",
                    errors="replace"
                ).strip()

                if message:
                    print(f"[UART] RX: {message}")

                return message

        except serial.SerialException as error:
            print(f"[UART] RX error: {error}")

        return None

    def close(self):
        """Close the serial interface."""

        if self.serial is not None:
            self.serial.close()
            print("[UART] Interface closed")


# ============================================================================
# COMMAND TESTS
# ============================================================================

def test_ping(uart: AGVUart):
    """Test ESP32 communication using PING/PONG."""

    print("\n--- PING TEST ---")

    uart.send("PING")

    response = uart.receive()

    if response == "PONG":
        print("[TEST] PING successful")
        return True

    print("[TEST] No valid PONG response")
    return False


def test_status(uart: AGVUart):
    """Request ESP32 status."""

    print("\n--- STATUS TEST ---")

    uart.send("STATUS")

    response = uart.receive()

    if response:
        print("[TEST] STATUS response received")
        return True

    print("[TEST] No STATUS response")
    return False


def test_stop(uart: AGVUart):
    """Test the safety STOP command."""

    print("\n--- STOP TEST ---")

    uart.send("STOP")

    response = uart.receive()

    if response == "ACK:STOP":
        print("[TEST] STOP command acknowledged")
        return True

    print("[TEST] STOP acknowledgement not received")
    return False


# ============================================================================
# HEARTBEAT
# ============================================================================

def send_heartbeat(uart: AGVUart):
    """Send a periodic heartbeat to the ESP32."""

    uart.send("HEARTBEAT")


# ============================================================================
# MAIN
# ============================================================================

def main():

    print()
    print("======================================")
    print(" TECH3D AGV - OLIMEX UART TEST")
    print(" Olimex A13 <-> ESP32")
    print("======================================")

    uart = AGVUart(
        UART_DEVICE,
        UART_BAUDRATE
    )

    if not uart.connect():
        print("\n[ERROR] Unable to open UART interface")
        print(f"[INFO] Check device: {UART_DEVICE}")
        return

    try:

        # Basic communication tests
        test_ping(uart)

        time.sleep(1)

        test_status(uart)

        time.sleep(1)

        test_stop(uart)

        print("\n--- HEARTBEAT TEST ---")

        # Periodic heartbeat demonstration
        for _ in range(5):

            send_heartbeat(uart)

            time.sleep(2)

    except KeyboardInterrupt:

        print("\n[INFO] Test interrupted by user")

    finally:

        uart.close()

        print("[INFO] UART test finished")


if __name__ == "__main__":
    main()
```

