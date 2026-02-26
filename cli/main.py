import json
import csv
from datetime import datetime, time
from pathlib import Path

# ---------------- CONFIG ---------------- #

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
HISTORY = DATA / "history"
TODAY_FILE = DATA / "today.json"
KPI_PATH = ROOT / "kpi-okrs"

DOMAINS = {
    "A": "athletics.csv",
    "B": "business.csv",
    "T": "technology.csv",
    "S": "science.csv",
    "R": "regulation.csv",
}

DOMAIN_NAMES = {
    "A": "Athletics",
    "B": "Business",
    "T": "Technology",
    "S": "Science",
    "R": "Regulation",
}

START_TIME = time(5, 0)
END_TIME = time(21, 0)

# ---------------- UTILS ---------------- #

def now():
    return datetime.now()

def today_str():
    return now().strftime("%Y-%m-%d")

def within_time_window():
    return START_TIME <= now().time() <= END_TIME

def load_kpis(domain):
    filename = DOMAINS[domain]
    path = KPI_PATH / filename

    with open(path, newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        return [
            {
                "id": row["ID"],
                "label": row["KPI"]
            }
            for row in reader
        ]

# ---------------- TODAY ---------------- #

def load_today():
    if TODAY_FILE.exists():
        with open(TODAY_FILE, "r") as f:
            return json.load(f)
    return {"date": today_str()}

def save_today(data):
    with open(TODAY_FILE, "w") as f:
        json.dump(data, f, indent=2)

# ---------------- HISTORY ---------------- #

def close_day():
    data = load_today()
    if data.get("date") != today_str():
        return

    HISTORY.mkdir(exist_ok=True)
    target = HISTORY / f"{today_str()}.json"
    with open(target, "w") as f:
        json.dump(data, f, indent=2)

    TODAY_FILE.unlink(missing_ok=True)

def list_history():
    files = sorted(HISTORY.glob("*.json"))
    result = []
    for i, f in enumerate(files, start=1):
        with open(f) as fh:
            data = json.load(fh)
        result.append((i, f.name.replace(".json", ""), data))
    return result

# ---------------- UI ---------------- #

def print_header():
    print("=" * 40)
    print(" ORACULUM · DAILY KPI INTERFACE")
    print(f" Date: {today_str()}   Time: {now().strftime('%H:%M')}")
    print(" Active window: 05:00 – 21:00")
    print("=" * 40)

def main_menu(today):
    for d in DOMAINS:
        count = len(today.get(d, []))
        total = len(load_kpis(d))
        name = DOMAIN_NAMES.get(d, d)
        print(f"[{d}] {name} ({count}/{total})")

    print("\n[H] Historic")
    print("[Q] Quit")

# ---------------- FLOWS ---------------- #

def domain_flow(domain):
    today = load_today()
    kpis = load_kpis(domain)
    done = set(today.get(domain, []))

    while True:
        print(f"\n--- {DOMAIN_NAMES[domain]} ---")
        for i, kpi in enumerate(kpis, start=1):
            mark = "✔" if kpi["id"] in done else " "
            print(f"[{i}] [{mark}] {kpi['id']} · {kpi['label']}")

        print("[Q] Back")
        choice = input("> ").strip().upper()

        if choice == "Q":
            break

        if choice.isdigit():
            idx = int(choice) - 1
            if 0 <= idx < len(kpis):
                kpi_id = kpis[idx]["id"]
                if kpi_id in done:
                    done.remove(kpi_id)
                else:
                    done.add(kpi_id)

                today[domain] = sorted(done)
                save_today(today)

# ---------------- HISTORY FLOW ---------------- #

def history_flow():
    history = list_history()
    print("\n=========== HISTORIC ===========")
    for i, date, _ in history:
        print(f"{i}. {date}")

    print("\n[T] View day")
    print("[Q] Back")

    choice = input("> ").strip().upper()
    if choice == "T":
        num = int(input("Day number: "))
        for i, date, data in history:
            if i == num:
                print(f"\n------ {date} ------")
                for d in data:
                    if d != "date":
                        print(f"{DOMAIN_NAMES.get(d, d)}:")
                        for k in data[d]:
                            print(f"  - {k}")
                input("\n[Enter] Back")

# ---------------- MAIN ---------------- #

def main():
    if not within_time_window():
        close_day()
        print("⛔ Day closed (outside active window)")
        return

    while True:
        today = load_today()
        print_header()
        main_menu(today)

        choice = input("> ").strip().upper()

        if choice in DOMAINS:
            domain_flow(choice)
        elif choice == "H":
            history_flow()
        elif choice == "Q":
            break

if __name__ == "__main__":
    main()