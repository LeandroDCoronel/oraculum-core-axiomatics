# Oraculum Systems – CLI Core
## Version 4 (2026-03-03)

### Overview
This release stabilizes the daily KPI tracking system:

- Historic data now includes missing days automatically.
- KPI names displayed in historic summaries.
- Progress percentages formatted with 2 decimals.
- Daily menu and KPI marking fully functional.
- Ready for pivoting into future v5 with data analytics.

### How to use
1. Run `python cli/main.py`.
2. Select domain to mark KPIs completed.
3. Access `[H] Historic` to see daily summaries.
4. Progress is shown per domain and globally.

### Notes
- Athletics KPIs are unchanged and verified.
- All historical gaps filled up to the day before today.
- Current system measures KPI as completed/not completed (1/0).