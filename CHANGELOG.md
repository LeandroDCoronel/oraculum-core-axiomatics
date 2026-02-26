# Changelog

## [2.0.0] – 2026-02-26

### Added
- Interactive CLI for daily KPI tracking (`cli/main.py`)
- Domain-based navigation using single-letter shortcuts (A, B, T, S, R)
- KPI selection by numeric index
- Human-readable KPI labels loaded from CSV files
- Daily working time window enforcement (05:00–21:00)
- Automatic daily persistence into `data/history/YYYY-MM-DD.json`
- Historic viewer for completed days

### Changed
- Migrated from log-based daily tracking (`daily_log.jsonl`) to structured daily files
- KPI semantics fully decoupled from core logic (CSV as source of truth)
- Improved project directory structure for versioned evolution (v1 core preserved)

### Preserved
- `core/compute_index.py` (v1 logic) remains intact and untouched

### Known Limitations
- Daily closure requires CLI execution after time window (manual trigger)
- Historic interface minimal (UI improvements planned for v2.1.0)

---

## [1.0.0] – Initial Release
- Core axiomatic computation engine
- Log-based daily KPI recording