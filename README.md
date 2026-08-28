# Autonomous AGV Robot – ESP32 & Linux

> **Autonomous Mobile Robot · ESP32 · Linux · Embedded Systems · Robotics · UART**

Prototipo di **veicolo a guida autonoma (AGV)** sviluppato su piattaforma **ESP32**, **Olimex A13 con Armbian Linux** ed **ESP32-CAM**.

Il progetto integra controllo embedded real-time, comunicazione seriale, gestione dei motori, acquisizione dei sensori e funzioni di navigazione autonoma all'interno di un'architettura robotica distribuita.

L'obiettivo è sviluppare una piattaforma sperimentale per lo studio e l'integrazione di **robotica, sistemi embedded, firmware, controllo real-time, comunicazione tra sistemi e navigazione autonoma**.

---

## Project Overview

Il sistema utilizza un'architettura distribuita nella quale ogni piattaforma svolge funzioni specifiche.

```text
                         TECH3D AGV V1
                              │
              ┌───────────────┼────────────────┐
              │               │                │
              ▼               ▼                ▼
        ┌─────────────┐ ┌─────────────┐ ┌─────────────┐
        │    ESP32    │ │ Olimex A13  │ │ ESP32-CAM   │
        │ Real-Time   │ │    Linux    │ │ Vision / QR │
        │ Controller  │ │ High-Level  │ │             │
        └──────┬──────┘ └──────┬──────┘ └─────────────┘
               │                │
        ┌──────┴──────┐         │
        ▼             ▼         ▼
     Motors        Sensors   Navigation
     + Encoders      / I/O   / Missions
```

L'**ESP32** gestisce le funzioni real-time e l'interazione diretta con l'hardware del robot.

L'**Olimex A13** esegue **Armbian Linux** e fornisce l'ambiente per le funzioni di livello superiore.

L'**ESP32-CAM** è dedicata alle funzioni di acquisizione immagini e lettura dei QR Code.

---

## System Architecture

L'architettura separa il controllo real-time dalle elaborazioni di livello superiore.

### ESP32 – Real-Time Controller

L'ESP32 rappresenta il controller principale del veicolo.

Le sue responsabilità comprendono:

* Controllo dei motori
* PWM e gestione degli attuatori
* Acquisizione degli encoder
* Controllo PID della trazione
* Gestione dei sensori
* Comunicazione UART
* Gestione dello stato del robot
* Funzioni di sicurezza
* Interfaccia OLED
* Web Dashboard
* Elaborazione dei dati provenienti dalla ESP32-CAM

Il firmware utilizza **FreeRTOS** per distribuire le principali attività in task indipendenti.

### Olimex A13 – Linux Platform

L'Olimex A13 esegue **Armbian Linux** e rappresenta il livello di elaborazione superiore.

Le sue funzioni comprendono:

* Comunicazione seriale con l'ESP32
* Gestione delle missioni
* Elaborazione dei dati
* Gestione delle informazioni sulle stazioni
* Pianificazione dei percorsi
* Supervisione del sistema
* Sviluppo di future funzioni di navigazione autonoma

### ESP32-CAM

L'ESP32-CAM viene utilizzata come modulo dedicato alla visione e alla lettura dei **QR Code**.

I dati rilevati possono essere trasferiti all'ESP32 tramite UART e utilizzati dal sistema durante le missioni automatiche.

---

## Hardware

Il prototipo è basato sui seguenti componenti principali:

* ESP32 development board
* Olimex A13
* Armbian Linux
* ESP32-CAM
* Motori DC
* Encoder di quadratura
* Motor driver
* Display OLED SSD1306
* Sensore ultrasonico HC-SR04
* Buzzer
* Segnalazione luminosa
* Interfacce UART
* Alimentazione e cablaggi del prototipo

La configurazione dettagliata dell'hardware e del pinout è disponibile in:

**[Hardware & Connections](docs/Hardware%20%26%20Connections.md)**

---

## Motor Control

La trazione utilizza due motori DC indipendenti con feedback tramite encoder di quadratura.

```text
                 ESP32
                   │
          ┌────────┴────────┐
          ▼                 ▼
      Motor SX          Motor DX
          │                 │
          ▼                 ▼
      Encoder SX        Encoder DX
          │                 │
          └────────┬────────┘
                   ▼
             Feedback Speed
                   │
                   ▼
              PID Control
```

Gli encoder vengono acquisiti tramite il periferico hardware **PCNT** dell'ESP32.

Il feedback viene utilizzato dal controllo PID per regolare la velocità dei motori.

---

## Autonomous Navigation

Il sistema è progettato per supportare modalità di navigazione automatica basate su missioni e stazioni.

Il flusso concettuale è:

```text
Mission / Destination
        │
        ▼
   Olimex A13
 Mission Processing
        │
       UART
        │
        ▼
      ESP32
 Vehicle Control
        │
   ┌────┴────┐
   ▼         ▼
Motors    Sensors
   │         │
   └────┬────┘
        ▼
   Robot State
```

I **QR Code** possono essere utilizzati come riferimenti per identificare stazioni o punti della missione.

---

## UART Communication

La comunicazione tra ESP32 e Olimex A13 utilizza una connessione UART bidirezionale.

Configurazione del prototipo:

* **Baud rate:** 115200
* **Formato:** 8N1
* **Comunicazione:** bidirezionale
* **Connessione:** TX / RX / GND

```text
ESP32                         Olimex A13
─────                         ──────────

TX  ────────────────────────► RX

RX  ◄──────────────────────── TX

GND ───────────────────────── GND
```

La comunicazione viene utilizzata per scambiare comandi, informazioni di stato e dati di sistema.

La documentazione del protocollo è disponibile in:

**[Communication Protocol](docs/Communication%20Protocol.md)**

---

## Safety & Fail-Safe

Il sistema integra diversi meccanismi dedicati alla sicurezza del veicolo.

### Obstacle Detection

Il sensore ultrasonico viene utilizzato per rilevare ostacoli davanti al robot.

Il rilevamento di una distanza inferiore alla soglia configurata può provocare l'arresto dei motori.

### Communication Heartbeat

La comunicazione con l'Olimex A13 utilizza un meccanismo di **heartbeat** per verificare la disponibilità del collegamento.

In caso di perdita della comunicazione oltre il timeout configurato, il sistema può attivare una condizione di fail-safe.

### Watchdog

Il firmware ESP32 utilizza il **Task Watchdog Timer (TWDT)** per monitorare le attività principali.

---

## Firmware Architecture

Il firmware ESP32 è organizzato in moduli indipendenti e utilizza **FreeRTOS** per la gestione delle attività concorrenti.

La struttura comprende moduli dedicati a:

* State management
* Motor control
* Encoder management
* OLED display
* Signaling
* QR processing
* UART communication
* Navigation
* NVS storage
* Web server

La documentazione completa dell'architettura firmware è disponibile in:

**[ESP32 Firmware Architecture](docs/ESP32%20Firmware%20Architecture.md)**

---

## Web Dashboard

L'ESP32 integra una Web Interface accessibile tramite rete Wi-Fi.

La dashboard è progettata per fornire funzioni di:

* Monitoraggio dello stato del robot
* Controllo manuale
* Selezione della modalità operativa
* Gestione delle stazioni
* Configurazione
* Visualizzazione dei dati
* Monitoraggio del sistema

---

## Development & Testing

Lo sviluppo è stato effettuato progressivamente attraverso la validazione dei singoli sottosistemi.

Le attività comprendono:

* Sviluppo firmware ESP32
* Configurazione Armbian Linux
* Test UART
* Debug della comunicazione seriale
* Test delle interfacce hardware
* Integrazione ESP32 ↔ Olimex A13
* Sviluppo del controllo motori
* Test degli encoder
* Sviluppo delle funzioni di navigazione
* Integrazione del modulo ESP32-CAM

La comunicazione UART tra ESP32 e Olimex A13 è stata verificata attraverso test dedicati.

---

## Public Technical Examples

Il repository contiene alcuni esempi tecnici semplificati per documentare i principali concetti utilizzati nel progetto.

### ESP32 UART Example

**[AGV_ESP32_UART_Test.ino](examples/AGV_ESP32_UART_Test.ino)**

Dimostra:

* HardwareSerial
* UART2
* Comunicazione bidirezionale
* Gestione dei comandi
* Heartbeat
* Comunicazione ESP32 ↔ Linux

### Olimex A13 UART Example

**[Olimex_UART_Test.py](examples/Olimex_UART_Test.py)**

Dimostra:

* Comunicazione seriale Linux
* Python
* UART
* Invio di comandi
* Ricezione di risposte
* Comunicazione Olimex A13 ↔ ESP32

> Gli esempi sono versioni semplificate pubblicate esclusivamente per documentare alcuni concetti tecnici. Il firmware completo e la logica applicativa del progetto non sono inclusi nel repository pubblico.

---

## Documentation

La documentazione tecnica è organizzata nella cartella `docs/`.

* **[System Architecture](docs/System%20Architecture.md)** — architettura generale del sistema
* **[Hardware & Connections](docs/Hardware%20%26%20Connections.md)** — hardware e collegamenti
* **[ESP32 Firmware Architecture](docs/ESP32%20Firmware%20Architecture.md)** — struttura del firmware
* **[Communication Protocol](docs/Communication%20Protocol.md)** — comunicazione tra i moduli

---

## Repository Structure

```text
agv-autonomous-robot/
│
├── README.md
├── LICENSE
│
├── docs/
│   ├── System Architecture.md
│   ├── Hardware & Connections.md
│   ├── ESP32 Firmware Architecture.md
│   └── Communication Protocol.md
│
└── examples/
    ├── AGV_ESP32_UART_Test.ino
    └── Olimex_UART_Test.py
```

Il firmware completo del sistema non è pubblicato. Il repository contiene documentazione tecnica ed esempi selezionati per illustrare l'architettura e alcuni aspetti dell'implementazione.

---

## Project Status

**Status: Functional Prototype / Active Development**

Il progetto è attualmente sviluppato come piattaforma sperimentale e prototipo funzionale.

L'architettura hardware/software e la comunicazione tra i principali moduli sono state implementate e testate progressivamente.

Lo sviluppo futuro è orientato all'estensione delle funzionalità di:

* Navigazione autonoma
* Controllo della trazione
* Integrazione sensori
* Computer vision
* Localizzazione
* Path planning
* Telemetria
* Gestione avanzata delle missioni

---

## Technologies

**ESP32 · C/C++ · FreeRTOS · Embedded Systems · Firmware · Armbian Linux · Olimex A13 · Python · UART · Robotics · AGV · PID Control · Encoders · PCNT · QR Code · ESP32-CAM · Web Interface**

---

## Author

**Christian Roger Scarparo**

Embedded Systems · Electronics · Firmware · Robotics · ESP32 · Linux
