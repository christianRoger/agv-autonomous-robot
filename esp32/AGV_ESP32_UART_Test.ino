/*
 * TECH3D AGV Robot
 * ESP32 <-> Olimex A13 UART Communication Example
 *
 * Demonstrates:
 * - ESP32 HardwareSerial
 * - UART communication with a Linux platform
 * - Bidirectional communication
 * - Simple command/status protocol
 * - Periodic heartbeat
 *
 * This is a simplified public example extracted from the
 * communication concepts used in the AGV platform.
 *
 * The complete AGV firmware is not included in this repository.
 */

#include <Arduino.h>

// ============================================================================
// UART CONFIGURATION
// ============================================================================

constexpr int UART_RX_PIN = 16;
constexpr int UART_TX_PIN = 17;

constexpr uint32_t UART_BAUDRATE = 115200;

// UART2 used for communication with the Olimex A13
HardwareSerial OlimexSerial(2);


// ============================================================================
// COMMUNICATION
// ============================================================================

void sendHeartbeat()
{
    OlimexSerial.println("HEARTBEAT");

    Serial.println("[UART] HEARTBEAT sent");
}


void sendStatus()
{
    OlimexSerial.println("STATUS:ESP32_READY");

    Serial.println("[UART] STATUS sent");
}


void processCommand(const String& command)
{
    Serial.print("[UART] RX: ");
    Serial.println(command);

    if (command == "PING")
    {
        OlimexSerial.println("PONG");
        Serial.println("[UART] PONG sent");
    }
    else if (command == "STATUS")
    {
        sendStatus();
    }
    else if (command == "STOP")
    {
        Serial.println("[UART] STOP command received");

        // In the complete AGV firmware this command
        // triggers the motor safety/stop logic.
        OlimexSerial.println("ACK:STOP");
    }
    else
    {
        OlimexSerial.println("ERROR:UNKNOWN_COMMAND");
    }
}


// ============================================================================
// UART RECEIVE
// ============================================================================

void readUART()
{
    static String buffer;

    while (OlimexSerial.available())
    {
        char c = OlimexSerial.read();

        if (c == '\n')
        {
            buffer.trim();

            if (!buffer.isEmpty())
            {
                processCommand(buffer);
            }

            buffer = "";
        }
        else
        {
            buffer += c;

            // Prevent uncontrolled buffer growth
            if (buffer.length() > 128)
            {
                buffer = "";
                Serial.println("[UART] RX buffer overflow");
            }
        }
    }
}


// ============================================================================
// SETUP
// ============================================================================

void setup()
{
    Serial.begin(115200);

    delay(1000);

    Serial.println();
    Serial.println("======================================");
    Serial.println(" TECH3D AGV - ESP32 UART TEST");
    Serial.println(" ESP32 <-> Olimex A13");
    Serial.println("======================================");

    OlimexSerial.begin(
        UART_BAUDRATE,
        SERIAL_8N1,
        UART_RX_PIN,
        UART_TX_PIN
    );

    Serial.println("[UART] Olimex A13 interface initialized");

    sendStatus();
}


// ============================================================================
// MAIN LOOP
// ============================================================================

void loop()
{
    static uint32_t lastHeartbeat = 0;

    // Process incoming UART commands
    readUART();

    // Periodic heartbeat
    if (millis() - lastHeartbeat >= 2000)
    {
        lastHeartbeat = millis();

        sendHeartbeat();
    }

    delay(10);
}
