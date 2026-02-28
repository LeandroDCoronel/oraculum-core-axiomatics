import os
import json
import datetime
import csv

# --------------------------
# CONFIGURACIÓN
# --------------------------
DATA_DIR = "data"
HISTORY_DIR = os.path.join(DATA_DIR, "history")
TODAY_FILE = os.path.join(DATA_DIR, "today.json")
END_TIME = datetime.time(21, 0)  # Cierre automático
START_TIME = datetime.time(5, 0)

DOMAIN_INFO = {
    "A": {"name": "Athletics", "weight": 0.20, "csv": "athletics.csv"},
    "B": {"name": "Business", "weight": 0.30, "csv": "business.csv"},
    "T": {"name": "Technology", "weight": 0.30, "csv": "technology.csv"},
    "S": {"name": "Science", "weight": 0.10, "csv": "science.csv"},
    "R": {"name": "Regulation", "weight": 0.10, "csv": "regulation.csv"},
}

# --------------------------
# FUNCIONES DE CARGA
# --------------------------
def load_kpis(domain_code):
    """Carga KPIs desde los CSV de kpi-okrs según el dominio."""
    csv_file = os.path.join("kpi-okrs", DOMAIN_INFO[domain_code]["csv"])
    kpis = []
    with open(csv_file, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        for row in reader:
            if row:
                kpis.append(row[0])
    return kpis

def load_today():
    if os.path.exists(TODAY_FILE):
        with open(TODAY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    else:
        # Inicializar estructura
        today = {code: [] for code in DOMAIN_INFO.keys()}
        today["date"] = datetime.date.today().isoformat()
        return today

def save_today(today):
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(TODAY_FILE, "w", encoding="utf-8") as f:
        json.dump(today, f, indent=2)

def save_history(today):
    os.makedirs(HISTORY_DIR, exist_ok=True)
    history_file = os.path.join(HISTORY_DIR, f"{today['date']}.json")
    with open(history_file, "w", encoding="utf-8") as f:
        json.dump(today, f, indent=2)

def calculate_progress(today):
    domain_progress = {}
    for code in DOMAIN_INFO:
        total = len(load_kpis(code))
        completed = len(today.get(code, []))
        domain_progress[code] = round(completed / total if total else 0, 4)
    # P global ponderado
    P = sum(domain_progress[c] * DOMAIN_INFO[c]["weight"] for c in DOMAIN_INFO)
    return domain_progress, round(P, 4)

# --------------------------
# INTERFAZ
# --------------------------
def main_menu():
    today = load_today()
    now = datetime.datetime.now().time()
    day_closed = now > END_TIME

    while True:
        os.system("cls" if os.name == "nt" else "clear")
        print("="*40)
        print(" ORACULUM · DAILY KPI INTERFACE")
        print(f" Date: {datetime.date.today().isoformat()}   Time: {datetime.datetime.now().strftime('%H:%M')}")
        print(f" Active window: {START_TIME.strftime('%H:%M')} – {END_TIME.strftime('%H:%M')}")
        print("="*40)
        
        # Mostrar resumen de KPIs por dominio
        for code in DOMAIN_INFO:
            total = len(load_kpis(code))
            completed = len(today.get(code, []))
            print(f"[{code}] {DOMAIN_INFO[code]['name']} ({completed}/{total})")
        
        print("\n[H] Historic")
        print("[Q] Quit")
        choice = input("> ").strip().upper()
        
        if choice == "Q":
            break
        elif choice in DOMAIN_INFO and not day_closed:
            domain_menu(choice, today)
            save_today(today)
        elif choice == "H":
            historic_menu()
        else:
            print("Invalid choice or day closed. Press Enter.")
            input()

def domain_menu(code, today):
    kpis = load_kpis(code)
    while True:
        os.system("cls" if os.name == "nt" else "clear")
        print(f"--- {DOMAIN_INFO[code]['name']} ---")
        for idx, kpi in enumerate(kpis, 1):
            mark = "[✔]" if kpi in today.get(code, []) else "[ ]"
            print(f"{idx}. {mark} {kpi}")
        print("[Q] Back")
        choice = input("> ").strip().upper()
        if choice == "Q":
            break
        elif choice.isdigit() and 1 <= int(choice) <= len(kpis):
            kpi_sel = kpis[int(choice)-1]
            if kpi_sel in today.get(code, []):
                today[code].remove(kpi_sel)
            else:
                today[code].append(kpi_sel)
        else:
            print("Invalid choice. Press Enter.")
            input()

def historic_menu():
    files = sorted(os.listdir(HISTORY_DIR))
    days = [f.replace(".json", "") for f in files if f.endswith(".json")]
    while True:
        os.system("cls" if os.name == "nt" else "clear")
        print("=========== HISTORIC ===========")
        for idx, day in enumerate(days, 1):
            print(f"{idx}. {day}")
        print("\n[T] View day")
        print("[Q] Back")
        choice = input("> ").strip().upper()
        if choice == "Q":
            break
        elif choice.isdigit() and 1 <= int(choice) <= len(days):
            view_day(days[int(choice)-1])
        else:
            print("Invalid choice. Press Enter.")
            input()

def view_day(day_filename):
    file_path = os.path.join(HISTORY_DIR, f"{day_filename}.json")
    if not os.path.exists(file_path):
        print("Historic file not found.")
        input("[Enter] Back")
        return
    with open(file_path, "r", encoding="utf-8") as f:
        day_data = json.load(f)
    
    domain_progress, P = calculate_progress(day_data)
    
    os.system("cls" if os.name == "nt" else "clear")
    print(f"------ {day_data['date']} ------")
    for code in DOMAIN_INFO:
        print(f"{DOMAIN_INFO[code]['name']}:")
        completed_kpis = day_data.get(code, [])
        for kpi in completed_kpis:
            print(f"  - {kpi}")
        print(f"  Progress: {domain_progress[code]:.4f}")
    print(f"\nGlobal P: {P:.4f}")
    input("\n[Enter] Back")

# --------------------------
# EJECUCIÓN
# --------------------------
if __name__ == "__main__":
    today = load_today()
    now = datetime.datetime.now().time()
    if now >= END_TIME:
        save_history(today)
        print("⛔ Day closed (outside active window)")
    else:
        main_menu()