Oraculum-Core-Axiomatics CLI
Version 3.0.0

Overview
Oraculum-Core-Axiomatics is a CLI tool to track daily KPIs across multiple domains:

- Athletics
- Business
- Technology
- Science
- Regulation

It records completed KPIs, computes weighted daily progress (P), and maintains historical records.

Features in v3.0.0
- Daily progress per domain (0-1)
- Weighted overall progress P
- Auto-close day at 21:00
- Historic JSON storage with domain progress and overall P
- Full CLI interface in English
- Toggle KPIs (mark/unmark)
- Backward compatible with v2 JSON files

Usage
1. Run the CLI:
   python cli/main.py
2. Mark KPIs as completed in your active window (05:00–21:00).
3. View historical days using [H] Historic.

File Structure
- cli/main.py — main CLI logic
- kpi-okrs/ — CSV files per domain
- data/ — JSON files for today and historical records
- VERSION — current version
- README.md — project overview
- CHANGELOG.md — version history

License
MIT License