# Decisions — Provenance Guard

Newest first. Each entry: the decision, the date, and why.

---

## 2026-11-12 — `confidence` is the combined score

The `confidence` field in the `/submit` response holds the combined score, from 0.0
(confidently human) to 1.0 (confidently AI).

**Why:** unit 8's `run_attacks.py` and `run_eval.py` read `confidence` and compare it to the
thresholds. Any other meaning, such as distance from 0.5, would make every row of next
unit's reports wrong.
