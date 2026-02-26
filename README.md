Oraculum Core Axiomatics
=======================

Oraculum Core Axiomatics is a deterministic system for daily self-governance,
based on KPI completion across multiple strategic domains.

This repository contains:
- v1: axiomatic computation core
- v2: interactive CLI for daily execution and historic tracking


Domains
-------

Each domain is accessed using a single-letter shortcut:

A – Athletics  
B – Business  
T – Technology  
S – Science  
R – Regulation  


Daily Usage (v2)
----------------

Run the CLI:

python cli/main.py

Select a domain and toggle KPIs by number.
Progress is saved automatically during the day.

After the daily time window (21:00), the day is archived into:

data/history/YYYY-MM-DD.json


Time Window
-----------

Daily execution is allowed only between:

05:00 – 21:00

Outside this window, the day is considered closed.


Project Structure
-----------------

Oraculum-Core-Axiomatics/
├── core/        # v1 axiomatic computation (preserved)
├── cli/         # v2 interactive CLI
├── kpi-okrs/    # KPI definitions (CSV source of truth)
├── data/
│   ├── today.json
│   └── history/
├── logs/
├── CHANGELOG.md
├── VERSION
└── README.md


Versioning
----------

Semantic versioning is used:

v1.x – Core axiomatic engine  
v2.x – Daily operational CLI  
v3.x – Planned automation and intelligence layers  

Current stable version: v2.0.0