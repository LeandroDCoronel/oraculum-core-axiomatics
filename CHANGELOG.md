# Changelog

## [3.0.0] - 2026-02-27
### Added
- Daily progress calculation per domain (0-1) with weighted overall P
- Auto-close of day at 21:00, disallow marking KPIs after closing
- Historic JSON files now store progress per domain and overall P
- CLI fully in English
- Toggle KPIs (mark/unmark) in domain menu
- Historic menu displays domain progress and overall P
- Maintains compatibility with v2 JSON structure

---

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