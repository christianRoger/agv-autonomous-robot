# AGV Robot V1 — System Architecture

## Panoramica

Il **TECH3D AGV Robot V1** è una piattaforma robotica mobile progettata con un'architettura embedded distribuita.

Il sistema combina un **ESP32**, una piattaforma **Olimex A13 con Linux** e un **ESP32-CAM**, assegnando a ciascun dispositivo funzioni specifiche all'interno del sistema.

L'architettura è stata progettata per separare le attività **real-time**, le elaborazioni di livello superiore e le funzioni di acquisizione delle immagini.

```text
                         TECH3D AGV V1
                              │
              ┌───────────────┼────────────────┐
              │               │                │
              ▼               ▼                ▼
        ┌─────────────┐ ┌─────────────┐ ┌─────────────┐
        │    ESP32    │ │ Olimex A13  │ │ ESP32-CAM   │
        │             │ │    Linux    │ │             │
        │ Real-Time   │ │ High-Level  │ │ Vision / QR │
        │ Controller  │ │ Processing  │ │             │
        └──────┬──────┘ └──────┬──────┘ └──────┬──────┘
               │                │               │
               │                │               │
               ▼                ▼               ▼
           Motors           Navigation       QR Codes
           Encoders         Data Processing   Camera
           Sensors          Mission Logic
           Safety
```

---

## Architettura distribuita

Il sistema utilizza un'architettura distribuita nella quale il controllo del veicolo è suddiviso tra più piattaforme.

### ESP32

L'ESP32 rappresenta il **controller real-time principale** del veicolo.

È responsabile delle funzioni che richiedono tempi di risposta deterministici, tra cui:

* controllo dei motori;
* gestione del PWM;
* acquisizione degli encoder;
* controllo PID della trazione;
* gestione dei sensori;
* gestione delle condizioni di sicurezza;
* comunicazione UART;
* gestione dello stato operativo del robot;
* interfaccia Web locale;
* aggiornamento del display OLED.

Il firmware utilizza **FreeRTOS** per distribuire le principali funzioni in task indipendenti.

---

### Olimex A13

L'**Olimex A13** esegue **Armbian Linux** e viene utilizzato come piattaforma di elaborazione di livello superiore.

Le sue funzioni includono:

* gestione del sistema Linux;
* comunicazione seriale con l'ESP32;
* gestione delle missioni;
* elaborazione dei dati;
* gestione delle informazioni relative alle stazioni;
* pianificazione di percorsi;
* funzioni di supervisione;
* future elaborazioni dedicate alla navigazione autonoma.

Questa separazione consente di mantenere le funzioni real-time sul microcontrollore senza caricare l'ESP32 con tutte le elaborazioni di livello superiore.

---

### ESP32-CAM

L'ESP32-CAM viene utilizzata come modulo dedicato all'acquisizione delle immagini e alla gestione della lettura dei **QR Code**.

La comunicazione con il controller principale avviene tramite **UART**.

Il modulo può trasmettere al sistema informazioni relative ai QR rilevati, permettendo all'ESP32 di utilizzarle durante le missioni automatiche.

---

# Comunicazione tra i moduli

I principali dispositivi del sistema comunicano attraverso interfacce seriali dedicate.

```text
             ┌───────────────────────┐
             │       Olimex A13      │
             │       Armbian Linux   │
             └───────────┬───────────┘
                         │
                    UART 115200
                         │
                         ▼
             ┌───────────────────────┐
             │         ESP32         │
             │   Real-Time Control   │
             └───────────┬───────────┘
                         │
                    UART 115200
                         │
                         ▼
             ┌───────────────────────┐
             │       ESP32-CAM       │
             │     Vision / QR       │
             └───────────────────────┘
```

Le interfacce seriali permettono di mantenere separati i diversi livelli del sistema e facilitano il debug e l'espansione della piattaforma.

I dettagli dei messaggi e del protocollo di comunicazione sono descritti nel documento:

**[Communication Protocol.md](Communication%20Protocol.md)**

---

# Controllo della trazione

La trazione del robot utilizza due motori DC indipendenti:

```text
                    ESP32
                      │
             ┌────────┴────────┐
             │                 │
             ▼                 ▼
        Motore SX          Motore DX
             │                 │
             ▼                 ▼
        Encoder SX         Encoder DX
             │                 │
             └────────┬────────┘
                      │
                      ▼
                 Feedback
                      │
                      ▼
                 Controllo PID
```

Gli encoder di quadratura forniscono il feedback della velocità delle ruote.

Il controller ESP32 utilizza queste informazioni per regolare la velocità dei motori attraverso il controllo **PID**.

L'acquisizione degli impulsi degli encoder viene effettuata tramite il periferico hardware **PCNT** dell'ESP32.

---

# Firmware ESP32

Il firmware è organizzato secondo una struttura modulare.

Le principali responsabilità sono suddivise in moduli dedicati:

```text
ESP32 Firmware
│
├── State Management
├── Motor Control
├── Encoder Management
├── OLED Interface
├── Signaling
├── QR Processing
├── UART Communication
├── Navigation
├── NVS Storage
└── Web Server
```

Questa struttura permette di isolare le diverse funzionalità e semplifica manutenzione, debugging e sviluppo futuro.

La struttura dettagliata del firmware è descritta in:

**[ESP32 Firmware Architecture.md](ESP32%20Firmware%20Architecture.md)**

---

# FreeRTOS e task concorrenti

Il firmware ESP32 utilizza **FreeRTOS** per gestire attività concorrenti.

Le principali attività sono organizzate in task dedicati, tra cui:

* controllo motori;
* comunicazione UART;
* aggiornamento OLED;
* segnalazione;
* elaborazione QR.

Alcuni task sono associati a core specifici dell'ESP32 per distribuire il carico di elaborazione.

L'accesso allo stato condiviso del robot viene protetto tramite meccanismi di sincronizzazione, evitando condizioni di race tra task differenti.

---

# Navigazione autonoma

La navigazione autonoma è progettata come un sistema multilivello.

```text
          Mission / Destination
                    │
                    ▼
             Olimex A13
           Mission Processing
                    │
                    │ UART
                    ▼
                 ESP32
            Vehicle Control
                    │
          ┌─────────┴─────────┐
          ▼                   ▼
       Motors              Sensors
          │                   │
          ▼                   ▼
      Movement            Feedback
          │                   │
          └─────────┬─────────┘
                    ▼
              Robot State
```

L'Olimex A13 può gestire le informazioni di missione e di navigazione, mentre l'ESP32 esegue il controllo diretto del veicolo.

I QR Code possono essere utilizzati come riferimenti per identificare stazioni o punti della missione.

---

# Sistema di sicurezza

La sicurezza viene gestita principalmente dall'ESP32, in quanto il microcontrollore mantiene il controllo diretto degli attuatori.

Il sistema integra diversi livelli di protezione:

### Rilevamento ostacoli

Il sensore ultrasonico viene utilizzato per rilevare ostacoli davanti al veicolo.

Quando la distanza rilevata raggiunge la soglia di sicurezza configurata, il sistema può arrestare i motori.

### Heartbeat

La comunicazione con l'Olimex A13 utilizza un meccanismo di **heartbeat**.

La perdita della comunicazione oltre il timeout configurato può causare l'attivazione della logica **fail-safe**.

### Watchdog

Il firmware utilizza il **Task Watchdog Timer (TWDT)** per monitorare l'esecuzione delle attività principali.

In caso di blocco o mancata risposta di un task, il watchdog può provocare il riavvio del sistema.

---

# Interfaccia utente

L'ESP32 integra due livelli principali di interazione:

```text
                   ESP32
                     │
          ┌──────────┴──────────┐
          │                     │
          ▼                     ▼
     OLED Display          Web Dashboard
      128 × 64             Browser / Wi-Fi
```

Il display OLED fornisce informazioni essenziali direttamente sul robot.

La Web Interface permette invece di accedere a funzioni di supervisione e configurazione attraverso un browser.

Tra le funzioni disponibili:

* monitoraggio dello stato del robot;
* controllo manuale;
* selezione della modalità operativa;
* gestione delle stazioni;
* configurazione;
* informazioni diagnostiche;
* monitoraggio della comunicazione.

---

# Modalità operative

Il sistema è progettato per supportare differenti modalità operative.

### Modalità Manuale

Il robot può essere controllato attraverso l'interfaccia Web.

### Modalità Automatica

Il sistema utilizza una missione e una destinazione configurata per eseguire il movimento autonomo.

### Modalità Apprendimento

La piattaforma può essere utilizzata per acquisire informazioni relative alle stazioni e alla struttura dell'ambiente utilizzando i QR Code e gli altri dati disponibili.

---

# Filosofia progettuale

L'architettura segue alcuni principi fondamentali:

**Separazione delle responsabilità**

Ogni piattaforma esegue le funzioni per le quali è più adatta.

**Controllo real-time locale**

Le funzioni critiche di movimento e sicurezza rimangono sul microcontrollore ESP32.

**Elaborazione distribuita**

Le elaborazioni più complesse possono essere trasferite alla piattaforma Linux.

**Modularità**

Il firmware è suddiviso in moduli indipendenti per facilitare manutenzione ed evoluzione.

**Fail-safe**

La perdita di comunicazione o il rilevamento di condizioni pericolose può portare il sistema in uno stato sicuro.

---

# Stato dell'architettura

L'architettura descritta rappresenta la struttura del **prototipo AGV V1** e costituisce la base per future evoluzioni del sistema.

Possibili sviluppi includono:

* algoritmi di navigazione più avanzati;
* integrazione di sensori aggiuntivi;
* localizzazione del robot;
* mappatura dell'ambiente;
* computer vision;
* pianificazione dinamica dei percorsi;
* comunicazione wireless tra robot e sistema di supervisione;
* gestione di flotte di AGV.

---

## Documentazione correlata

* **Hardware & Connections** — configurazione hardware e pinout.
* **ESP32 Firmware Architecture** — struttura interna del firmware.
* **Communication Protocol** — protocollo di comunicazione tra i moduli.

---

**TECH3D — Robot AGV V1**

**Embedded Systems · Robotics · ESP32 · Linux · Autonomous Navigation**
