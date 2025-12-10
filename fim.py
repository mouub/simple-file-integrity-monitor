import hashlib
import os
import time

# CONFIGURAZIONE
BASELINE_FILE = "baseline.txt"
TARGET_FOLDER = "./Files"
POLLING_INTERVAL = 1  # Secondi di attesa tra i controlli

def calculate_file_hash(filepath):
    """
    Calcola l'hash SHA-256 di un file.
    Legge il file a blocchi di 4096 byte per ottimizzare l'uso della RAM 
    ed evitare crash con file di grandi dimensioni.
    """
    sha256_hash = hashlib.sha256()
    try:
        with open(filepath, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()
    except FileNotFoundError:
        return None
    except Exception as e:
        # Ritorna None se il file è bloccato o temporaneo, evitando crash del monitoraggio
        return None

def load_baseline():
    """
    Carica le firme dei file (hash) dalla baseline salvata in un dizionario.
    Ritorna: dict {percorso_file: hash}
    """
    baseline = {}
    if not os.path.exists(BASELINE_FILE):
        return baseline
    
    with open(BASELINE_FILE, "r") as f:
        for line in f:
            parts = line.strip().split("|")
            if len(parts) == 2:
                baseline[parts[0]] = parts[1]
    return baseline

def create_baseline():
    """
    Scansiona la cartella target, calcola gli hash e crea il file di riferimento (baseline).
    Sovrascrive eventuali baseline precedenti.
    """
    print("\n[INFO] Creazione nuova baseline...")
    
    if os.path.exists(BASELINE_FILE):
        os.remove(BASELINE_FILE)

    count = 0
    with open(BASELINE_FILE, "w") as f:
        for root, dirs, files in os.walk(TARGET_FOLDER):
            for file in files:
                file_path = os.path.join(root, file)
                file_hash = calculate_file_hash(file_path)
                
                if file_hash:
                    f.write(f"{file_path}|{file_hash}\n")
                    print(f"[OK] Indicizzato: {file_path}")
                    count += 1
    
    print(f"\n[SUCCESSO] Baseline creata con {count} file monitorati!")

def start_monitoring():
    """
    Monitora continuamente la cartella confrontando lo stato attuale con la baseline.
    Rileva: Nuovi file, File modificati, File eliminati.
    """
    print("\n[INFO] Caricamento baseline...")
    baseline_db = load_baseline()
    
    if not baseline_db:
        print("[ERRORE] Baseline non trovata. Esegui prima l'opzione A per crearla.")
        return

    print(f"[INFO] Monitoraggio avviato su {len(baseline_db)} file. Premi Ctrl+C per fermare.")
    
    while True:
        time.sleep(POLLING_INTERVAL)
        
        # 1. Rilevamento stato attuale dei file su disco
        current_files_state = {}
        for root, dirs, files in os.walk(TARGET_FOLDER):
            for file in files:
                file_path = os.path.join(root, file)
                file_hash = calculate_file_hash(file_path)
                if file_hash:
                    current_files_state[file_path] = file_hash

        # 2. Controllo file Nuovi o Modificati
        for file_path, current_hash in current_files_state.items():
            if file_path not in baseline_db:
                print(f"[ALLARME] NUOVO FILE RILEVATO: {file_path}")
            elif baseline_db[file_path] != current_hash:
                print(f"[ALLARME] FILE MODIFICATO: {file_path}")

        # 3. Controllo file Eliminati
        for file_path in baseline_db:
            if file_path not in current_files_state:
                print(f"[ALLARME] FILE ELIMINATO: {file_path}")

def main():
    print("\n### FILE INTEGRITY MONITOR (FIM) ###")
    print("A) Crea nuova Baseline")
    print("B) Avvia Monitoraggio")
    
    choice = input("\nScegli un'opzione: ").upper()
    
    if choice == 'A':
        create_baseline()
    elif choice == 'B':
        start_monitoring()
    else:
        print("Scelta non valida.")

if __name__ == "__main__":
    main()