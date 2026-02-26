import json

WEIGHTS = {
    "A": 0.2,
    "B": 0.3,
    "T": 0.3,
    "S": 0.1,
    "R": 0.1
}

def compute_P(entry):
    return round(sum(entry[d] * WEIGHTS[d] for d in WEIGHTS), 4)

def load_logs(path):
    with open(path, "r") as f:
        for line in f:
            yield json.loads(line)

if __name__ == "__main__":
    logs = list(load_logs("logs/daily_log.jsonl"))

    for day in logs:
        P = compute_P(day)
        print(f"{day['date']} → P = {P}")