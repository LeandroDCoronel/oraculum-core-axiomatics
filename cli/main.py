import os
import json
import datetime
import csv

# --------------------------
# CONFIGURATION
# --------------------------
DATA_DIR = "data"
HISTORY_DIR = os.path.join(DATA_DIR, "history")
TODAY_FILE = os.path.join(DATA_DIR, "today.json")
END_TIME = datetime.time(21, 0)
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
    """
    Devuelve dict:
    {
        "A.KPI.1": "7 km completed",
        ...
    }
    """
    csv_file = os.path.join("kpi-okrs", DOMAIN_INFO[domain_code]["csv"])
    kpis = {}

    with open(csv_file, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        next(reader, None)  # saltar header ID,KPI,OKR

        for row in reader:
            if len(row) >= 2 and row[0].strip():
                kpis[row[0].strip()] = row[1].strip()

    return kpis

# --------------------------
# PRELOAD KPIs
# --------------------------
for code in DOMAIN_INFO:
    DOMAIN_INFO[code]["kpis"] = list(load_kpis(code).keys())

def load_today():
    today_date = datetime.date.today().isoformat()

    if os.path.exists(TODAY_FILE):
        with open(TODAY_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)

        if data.get("date") != today_date:
            save_history(data)
            fill_missing_days(data["date"])
            return {"date": today_date, **{c: [] for c in DOMAIN_INFO}}

        return data

    return {"date": today_date, **{c: [] for c in DOMAIN_INFO}}

def save_today(today):
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(TODAY_FILE, "w", encoding="utf-8") as f:
        json.dump(today, f, indent=2)

def save_history(day_data):
    os.makedirs(HISTORY_DIR, exist_ok=True)
    path = os.path.join(HISTORY_DIR, f"{day_data['date']}.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(day_data, f, indent=2)

def fill_missing_days(last_date_str):
    last_date = datetime.date.fromisoformat(last_date_str)
    yesterday = datetime.date.today() - datetime.timedelta(days=1)

    d = last_date + datetime.timedelta(days=1)
    while d <= yesterday:
        save_history({
            "date": d.isoformat(),
            **{c: [] for c in DOMAIN_INFO}
        })
        d += datetime.timedelta(days=1)

def fix_history_gaps():
    if not os.path.exists(HISTORY_DIR):
        return

    files = sorted(
        f.replace(".json", "")
        for f in os.listdir(HISTORY_DIR)
        if f.endswith(".json")
    )

    if len(files) < 2:
        return

    dates = [datetime.date.fromisoformat(d) for d in files]

    for i in range(len(dates) - 1):
        d = dates[i] + datetime.timedelta(days=1)
        while d < dates[i + 1]:
            save_history({
                "date": d.isoformat(),
                **{c: [] for c in DOMAIN_INFO}
            })
            d += datetime.timedelta(days=1)

def calculate_progress(day_data):
    domain_progress = {}
    for code in DOMAIN_INFO:
        total = len(load_kpis(code))
        completed = len(day_data.get(code, []))
        domain_progress[code] = completed / total if total else 0.0

    global_p = sum(
        domain_progress[c] * DOMAIN_INFO[c]["weight"]
        for c in DOMAIN_INFO
    )

    return domain_progress, global_p

# --------------------------
# INTERFAZ
# --------------------------
def main_menu():
    today = load_today()
    now = datetime.datetime.now().time()
    day_closed = now > END_TIME

    while True:
        os.system("cls" if os.name == "nt" else "clear")
        print("=" * 40)
        print(" ORACULUM · DAILY KPI INTERFACE")
        print(f" Date: {today['date']}   Time: {datetime.datetime.now().strftime('%H:%M')}")
        print(f" Active window: {START_TIME.strftime('%H:%M')} – {END_TIME.strftime('%H:%M')}")
        print("=" * 40)

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
            print("Invalid choice. Press Enter.")
            input()

def domain_menu(code, today):
    kpis = load_kpis(code)
    kpi_ids = list(kpis.keys())

    while True:
        os.system("cls" if os.name == "nt" else "clear")
        print(f"--- {DOMAIN_INFO[code]['name']} ---")

        for i, kpi_id in enumerate(kpi_ids, 1):
            mark = "[✔]" if kpi_id in today[code] else "[ ]"
            print(f"{i}. {mark} {kpis[kpi_id]}")

        print("[Q] Back")
        choice = input("> ").strip().upper()

        if choice == "Q":
            break
        elif choice.isdigit() and 1 <= int(choice) <= len(kpi_ids):
            kpi_id = kpi_ids[int(choice) - 1]
            if kpi_id in today[code]:
                today[code].remove(kpi_id)
            else:
                today[code].append(kpi_id)
        else:
            print("Invalid choice. Press Enter.")
            input()

# --------------------------
# HISTORIC HELPERS
# --------------------------

def summarize_day(day):
    """
    Returns string: 'A: xx.xx%  B: xx.xx% ...'
    """
    path = os.path.join(HISTORY_DIR, f"{day}.json")

    if not os.path.exists(path):
        return ""

    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    summary = []

    for domain, info in DOMAIN_INFO.items():
        kpis = info["kpis"]
        if not kpis:
            continue

        done = sum(1 for k in kpis if k in data.get(domain, []))
        pct = (done / len(kpis)) * 100
        summary.append(f"{domain}: {pct:5.2f}%")

    return "  ".join(summary)


# --------------------------
# HISTORIC MENU
# --------------------------

def historic_menu():
    fix_history_gaps()

    if not os.path.exists(HISTORY_DIR):
        print("No historic data.")
        input()
        return

    days = sorted(
        f.replace(".json", "")
        for f in os.listdir(HISTORY_DIR)
        if f.endswith(".json")
    )

    while True:
        os.system("cls" if os.name == "nt" else "clear")
        print("=========== HISTORIC ===========")

        for i, d in enumerate(days, 1):
            summary = summarize_day(d)
            print(f"{i}. {d}  {summary}")
        
        print("[Q] Back")

        choice = input("> ").strip().upper()
        if choice == "Q":
            break
        elif choice.isdigit() and 1 <= int(choice) <= len(days):
            view_day(days[int(choice) - 1])
        else:
            print("Select a number or Q.")
            input()

def view_day(day):
    path = os.path.join(HISTORY_DIR, f"{day}.json")
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    domain_progress, global_p = calculate_progress(data)

    os.system("cls" if os.name == "nt" else "clear")
    print(f"------ {day} ------\n")

    for code in DOMAIN_INFO:
        print(f"{DOMAIN_INFO[code]['name']}:")
        kpis = load_kpis(code)

        for kpi_id in data.get(code, []):
            print(f"  - {kpis.get(kpi_id, kpi_id)}")

        print(f"  Progress: {domain_progress[code]*100:.2f}%\n")

    print(f"Global P: {global_p*100:.2f}%")
    input("\n[Enter] Back")

# --------------------------
# EJECUCIÓN
# --------------------------
if __name__ == "__main__":
    now = datetime.datetime.now().time()
    today = load_today()

    if now >= END_TIME:
        save_history(today)
        print("⛔ Day closed (outside active window)")
    else:
        main_menu()