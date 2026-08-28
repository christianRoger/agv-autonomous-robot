# Robot AGV V1 — TECH3D (ESP32)

Veicolo a guida autonoma (AGV) basato su **ESP32**, con controllo di motori DC tramite **PID + encoder in quadratura (PCNT)**, navigazione autonoma tramite **QR code**, dashboard Web e comunicazione con **Olimex A13** (Linux) e **ESP32-CAM**.

> Documentazione tecnica completa disponibile nel repository.

---

## Panoramica

* **Trazione:** 2 motori DC con controllo PID e feedback degli encoder hardware tramite PCNT.
* **Modalità:** Manuale (joystick Web), Automatica (missioni verso le stazioni) e Apprendimento (mappatura automatica delle stazioni tramite QR).
* **Interfaccia:** display OLED 128×64 + dashboard Web responsive (browser/smartphone).
* **Sicurezza:** sensore a ultrasuoni HC-SR04 (arresto a 30 cm), heartbeat dell'Olimex A13 e Task Watchdog (TWDT, 10 s).

---

## Hardware / Pinout

| Componente                 | Funzione              | GPIO ESP32       |
| -------------------------- | --------------------- | ---------------- |
| Display OLED SSD1306 (I2C) | Telemetria locale     | SDA 21 / SCL 4   |
| Motore SX (PWM / DIR)      | Trazione sinistra     | PWM 18 / DIR 19  |
| Motore DX (PWM / DIR)      | Trazione destra       | PWM 22 / DIR 23  |
| Encoder SX (A / B)         | Feedback velocità SX  | 25 / 26 (PCNT)   |
| Encoder DX (A / B)         | Feedback velocità DX  | 32 / 33 (PCNT)   |
| UART2 → Olimex A13         | Navigazione (Linux)   | RX 16 / TX 17    |
| UART1 → ESP32-CAM          | Lettura QR            | RX 35 / TX 15    |
| Pulsante Reset Wi-Fi       | Ripristino rete       | 13 (pull-up)     |
| Girofaro (LED)             | Segnalazione visiva   | 12               |
| Buzzer                     | Segnalazione acustica | 27               |
| Ultrasuoni HC-SR04         | Sicurezza ostacoli    | TRIG 5 / ECHO 14 |

> Il GPIO **34** è unicamente di ingresso (input-only) sull'ESP32 e non è adatto come RX seriale; per questo motivo il segnale RX dell'ESP32-CAM è stato spostato sul GPIO **35**.

---

## Struttura modulare (cartella `src/`)

Il firmware è stato refactoring da un singolo file monolitico a una struttura modulare composta da file `.cpp/.h` organizzati nella cartella `src/`.

Lo sketch principale `Robot_AGV_V1.ino`, nella directory principale del progetto, contiene solamente `setup()` e `loop()` e si occupa dell'inizializzazione e del collegamento dei vari moduli.

```text
Robot_AGV_V1/

├── Robot_AGV_V1.ino          # setup()/loop() + collegamento dei moduli
├── config.h                  # pinout, parametri PID, stack/task, struct
├── web_dashboard.h           # HTML + JS della dashboard (PROGMEM)
└── src/

    ├── globals.h / .cpp          # oggetti globali condivisi + prototipi
    ├── state_manager.h / .cpp    # accesso thread-safe al RobotState (mutex)
    ├── encoders.h / .cpp         # inizializzazione PCNT (encoder in quadratura)
    ├── motors.h / .cpp           # TaskMotors + pararMotores (PID 50 Hz)
    ├── oled_display.h / .cpp     # TaskOLED (rendering del display)
    ├── signaling.h / .cpp        # TaskSignaling (girofaro + buzzer)
    ├── qr_processing.h / .cpp    # TaskQRProcessing + elaboraCodiceQR
    ├── uart_comm.h / .cpp        # TaskUARTParser + applyCameraEnabled
    ├── nvs_storage.h / .cpp      # initNVSAndDefaults
    ├── web_server.h / .cpp       # setupWebDashboard + isAuthenticated
    └── navigation.h / .cpp       # avviaNavigazioneAutomatica + lerDistancia
```

La cartella `src/` viene compilata automaticamente da Arduino IDE, arduino-cli o PlatformIO.

Gli header dei moduli vengono inclusi tramite `#include "globals.h"` e gli altri file di intestazione necessari.

---

## Task FreeRTOS

| Task               | Core | Priorità | Stack | Funzione                      |
| ------------------ | ---: | -------: | ----: | ----------------------------- |
| `TaskMotors`       |    1 | 5 (alta) | 12 KB | PID + lettura encoder PCNT    |
| `TaskUARTParser`   |    0 |        4 | 16 KB | Comandi A13 e QR dalla CAM    |
| `TaskOLED`         |    0 |        2 |  6 KB | Aggiornamento OLED            |
| `TaskSignaling`    |    0 |        2 |  4 KB | Girofaro + Buzzer             |
| `TaskQRProcessing` |    1 |        1 | 12 KB | Elaborazione QR non bloccante |

Tutti i task utilizzano il **TWDT (Task Watchdog Timer)** con timeout di 10 secondi.

L'accesso alla struttura `RobotState` è protetto da un **mutex** (`state_mutex`) per evitare condizioni di race in ambiente dual-core.

---

## Comunicazione seriale (UART)

### Olimex A13 — UART2, 115200 baud

I comandi vengono terminati dal carattere `\n`.

| Comando           | Effetto                                |
| ----------------- | -------------------------------------- |
| `CMD:QR:<codice>` | Elabora un QR ricevuto                 |
| `CMD:GOTO:<dest>` | Imposta la destinazione della missione |
| `CMD:POS:<x>,<y>` | Aggiorna le coordinate X,Y             |
| `CMD:STOP`        | Arresto di emergenza                   |

Quando viene configurata una missione tramite dashboard, l'ESP32 risponde con:

```text
SET:DEST:<dest>
```

### ESP32-CAM — UART1, 115200 baud

L'ESP32-CAM può inviare i codici QR tramite:

```text
QR:<codice>
```

oppure tramite HTTP attraverso:

```text
/api/cam/qr
```

Entrambi i metodi utilizzano un buffer di caratteri fisso, evitando allocazioni dinamiche dell'heap durante il ciclo di elaborazione.

---

## Dashboard Web e autenticazione

Il sistema utilizza **ESPAsyncWebServer** sulla porta 80.

La dashboard comprende:

* Pagina principale `/`
* API REST per telemetria, controllo e configurazione
* Autenticazione server-side
* Gestione delle sessioni tramite token
* Telemetria del sistema
* Mappa 2D delle stazioni
* Joystick per il controllo manuale
* Selettore della modalità operativa
* Limitatore di velocità (50 / 75 / 100%)
* Gestione delle stazioni
* Scanner Wi-Fi
* Configurazione della camera
* Esportazione dei log in formato CSV

### Autenticazione

L'endpoint:

```text
/api/login
```

genera un token di sessione casuale di 32 caratteri esadecimali.

Il token viene memorizzato in:

```text
g_auth_token
```

e inviato al client tramite un cookie `HttpOnly`.

Gli endpoint che modificano lo stato del sistema verificano la validità del cookie e restituiscono HTTP `401` in caso di autenticazione non valida.

Le credenziali iniziali sono:

```text
Username: admin
Password: admin123
```

Le credenziali possono essere modificate.

> **Nota di sicurezza:** le credenziali di default devono essere modificate prima dell'utilizzo in un ambiente reale.

---

## Archiviazione NVS

Le configurazioni persistenti vengono gestite tramite **Preferences / NVS** dell'ESP32.

I dati memorizzati includono:

* Credenziali
* Stazioni di lavoro
* Configurazione della camera
* Parametri di sistema

Al primo avvio vengono create 8 stazioni industriali predefinite.

Gli aggiornamenti successivi della configurazione vengono gestiti senza eliminare le stazioni già presenti.

---

## Sicurezza e Fail-Safe

Il sistema integra diversi meccanismi di sicurezza.

### Rilevamento ostacoli

Il sensore a ultrasuoni **HC-SR04** viene utilizzato per il rilevamento degli ostacoli.

Quando viene rilevato un ostacolo a una distanza inferiore a **30 cm**, il robot esegue:

1. Arresto dei motori
2. Attivazione della segnalazione
3. Gestione dell'evento tramite il sistema di controllo

Il rilevamento utilizza un **filtro mediano** per ridurre i falsi positivi.

### Heartbeat Olimex A13

L'ESP32 monitora la comunicazione con l'Olimex A13.

Se il segnale heartbeat viene perso per più di **3 secondi**, al di fuori della modalità automatica, il robot esegue un arresto di sicurezza.

### Watchdog

Ogni task deve mantenere attivo il **TWDT**.

Se una task non risponde entro il timeout di **10 secondi**, il sistema può essere riavviato dal watchdog.

---

## Controllo motori

La trazione utilizza due motori DC:

* Motore sinistro
* Motore destro

Il controllo della velocità utilizza un algoritmo **PID** con feedback proveniente dagli encoder in quadratura.

Gli encoder vengono acquisiti tramite il periferico hardware **PCNT** dell'ESP32.

La `TaskMotors` esegue il controllo PID con una frequenza di:

```text
50 Hz
```

Questa architettura consente di regolare la velocità dei motori sulla base del feedback reale degli encoder.

---

## Navigazione autonoma

La navigazione automatica utilizza le informazioni provenienti dal sistema di gestione delle stazioni e dai codici QR.

Il modulo:

```text
navigation.*
```

gestisce le principali funzioni di navigazione automatica.

Tra le funzioni principali:

```text
avviaNavigazioneAutomatica()
lerDistancia()
```

La comunicazione con l'Olimex A13 consente di utilizzare il sistema Linux per attività di elaborazione e gestione delle missioni.

---

## Sistema QR

Il sistema integra un **ESP32-CAM** per la lettura dei codici QR.

I dati ricevuti vengono elaborati dal modulo:

```text
qr_processing.*
```

attraverso:

```text
TaskQRProcessing
elaboraCodiceQR
```

Il processamento è progettato per essere non bloccante, evitando di interferire con le attività critiche del controllo del robot.

I codici QR possono essere utilizzati per identificare stazioni e supportare la logica di navigazione.

---

## Modalità operative

Il robot supporta tre modalità operative principali:

### Manuale

Il robot viene controllato tramite un **joystick Web**.

La dashboard consente di controllare il movimento e limitare la velocità.

### Automatica

Il robot esegue missioni verso stazioni configurate nel sistema.

La destinazione può essere impostata tramite la dashboard e comunicata all'ESP32 attraverso il livello di comunicazione previsto dal sistema.

### Apprendimento

La modalità di apprendimento consente di utilizzare i codici QR per supportare la mappatura delle stazioni.

Questa modalità costituisce una base per lo sviluppo di funzioni autonome più avanzate.

---

## Compilazione e utilizzo

### Librerie necessarie

Il progetto utilizza le seguenti librerie:

* `ArduinoJson` (v6 o v7)
* `WiFiManager`
* `ESPAsyncWebServer`
* `Adafruit SSD1306`
* `Adafruit GFX`
* `Preferences` (integrata nel framework ESP32)

### Scheda

Configurazione consigliata:

```text
ESP32 Dev Module
```

o una scheda compatibile.

La velocità di upload utilizzata è:

```text
115200 baud
```

---

## Primo avvio

Durante il primo avvio, il sistema:

1. Crea la rete Wi-Fi `TECH3D_AGV_AP` con password `12345678` se non è disponibile una rete Wi-Fi precedentemente configurata.
2. Oppure si connette alla rete Wi-Fi già salvata.
3. Mostra l'indirizzo IP sul display OLED.
4. Permette di accedere alla dashboard Web tramite browser.
5. Richiede l'autenticazione tramite le credenziali configurate.

Credenziali iniziali:

```text
admin / admin123
```

---

## Software complementare — Olimex A13

Il sistema prevede un software complementare sviluppato in **Python** per l'Olimex A13.

I principali componenti software includono:

```text
robot.py
menu_principale.py
database.py
```

Il software viene eseguito su **Armbian Linux** e fornisce funzioni di elaborazione di livello superiore, gestione del database, pianificazione delle rotte e comunicazione con l'ESP32 tramite UART2.

---

## Limitazioni note

### Batteria e corrente

I valori relativi a batteria e corrente sono attualmente dei **placeholder**, poiché non è presente un sensore analogico collegato al pinout attuale.

Per ottenere misure reali è prevista l'integrazione di:

* Divisore di tensione per la misura della batteria
* Sensore di corrente, ad esempio INA219
* Collegamento a un ingresso ADC appropriato

### Direzione degli encoder

Se un motore ruota nella direzione opposta rispetto a quella prevista, è possibile:

* invertire il cablaggio A/B dell'encoder;
* oppure modificare la configurazione PCNT nella funzione `initEncodersPCNT()`.

---

## Stato del progetto

**Stato: Prototipo AGV funzionale in sviluppo**

Il progetto integra:

* Controllo motori
* PID
* Encoder hardware PCNT
* FreeRTOS
* Comunicazione UART
* ESP32-CAM
* Lettura QR
* Navigazione automatica
* Dashboard Web
* OLED
* NVS
* Sistema di sicurezza
* Comunicazione con piattaforma Linux

L'architettura è stata progettata in modo modulare per consentire l'estensione futura delle funzionalità di navigazione autonoma, sensoristica e controllo del veicolo.

---

*Progetto TECH3D — Robot AGV Enterprise V1*

*Progettato e sviluppato da Christian R. Scarparo*

