# File Integrity Monitor (FIM)

Un tool di sicurezza scritto in Python che monitora l'integrità dei file in tempo reale.
Il software calcola l'impronta digitale (Hash SHA-256) dei file in una cartella target e avvisa l'utente se avvengono modifiche non autorizzate.

## Funzionalità

* **Creazione Baseline:** Calcola e memorizza gli hash SHA-256 dei file target.
* **Monitoraggio Real-Time:** Scansiona continuamente la cartella per rilevare cambiamenti.
* **Avvisi di Sicurezza:** Notifica immediata in caso di:
    * Creazione di nuovi file.
    * Modifica del contenuto di un file (alterazione dell'hash).
    * Eliminazione di file.
* **Ottimizzazione Risorse:** Lettura dei file a blocchi (4KB) per evitare sovraccarico della memoria su file di grandi dimensioni.

## 🛠️ Tecnologie Utilizzate

* **Linguaggio:** Python 3
* **Librerie:** `hashlib` (per crittografia/hashing), `os`, `time`.
* **Algoritmo:** SHA-256 (Secure Hash Algorithm 256-bit).

## ⚙️ Come usare il tool

1.  Clona la repository:
    ```bash
    git clone https://github.com/mouub/simple-file-integrity-monitor.git
    ```
2.  Entra nella cartella:
    ```bash
    cd simple-file-integrity-monitor
    ```
3.  Esegui lo script:
    ```bash
    python3 fim.py
    ```
4.  Segui le istruzioni a schermo:
    * Seleziona **A** per creare una nuova Baseline.
    * Seleziona **B** per avviare il monitoraggio.

## Disclaimer

Questo progetto è stato creato a scopo didattico per approfondire concetti di Cybersecurity (Hashing, Integrity Checks) e automazione in Python.