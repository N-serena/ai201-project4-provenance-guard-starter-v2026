# Plan — Provenance Guard

Unit 7 builds the service; unit 8 attacks it. Same repo both units.

Split of work: I write the judgment pieces (trace, blind spots, criteria, combining rule,
label text, How I Used AI). Claude builds the code and reviews the writing. One step at a time.

**Ordering constraint:** `criteria.md` is committed before any scoring results exist (step 2
before step 3b).

## Unit 7

| # | Step | Owner | Status |
|---|---|---|---|
| 0 | Setup: install requirements, `test.py`, `detector.py`, these docs | Claude | done |
| 1 | M1 — trace, signals + blind spots, false-positive walkthrough, endpoint contract | me (Claude reviews) | next |
| 2 | M2 — `criteria.md`, five criteria with targets and reasons | me (Claude reviews) | pending |
| 3a | M3 — `/submit` answers: hardcoded response, payload parsing, bad-input handling | Claude | pending |
| 3b | M3 — signal one wired in, `content_id`, audit log entry | Claude | pending |
| 4a | M4 — `stylometry.py` measures + `style_signal`, four calibration inputs | Claude | pending |
| 4b | M4 — combining rule (I write it in words; Claude codes it), both scores logged | both | pending |
| 5a | M5 — three label texts (me), `score_to_label` + thresholds (Claude) | both | pending |
| 5b | M5 — `/appeal` | Claude | pending |
| 6 | M6 — README write-up, checklist, submit fork URL | me (Claude checks claims vs code) | pending |
| — | Stretch: `GET /content/<id>` (decide after 5b; declare in README first) | — | undecided |

## Session notes

- 2026-11-12, step 0: `test.py` 9/9 pass (the first run straight after install failed to
  import torch once, then passed). `detector.py` sample: perplexity 12.5, model_signal 0.8864.

## Fixed contract points

- Response field `confidence` is the combined score on 0 (human) to 1 (AI). Unit 8's
  `run_attacks.py` and `run_eval.py` compare it to the thresholds.
- `/submit` response carries `content_id`, `guess`, `confidence`, `label`, `model_score`,
  `style_score`.
- Bad input returns a 4xx JSON error and is recorded with `audit.log_rejection`.

## Unit 8

Not started. See RUNNING.md, "Unit 8 — the test".
