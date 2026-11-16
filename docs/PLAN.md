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
| 1 | M1 — trace, signals + blind spots, false-positive walkthrough, endpoint contract | me (Claude reviews) | done — `docs/milestone1.md` |
| 2 | M2 — `criteria.md`, five criteria with targets and reasons | me (Claude reviews) | done — commit before 3b |
| 3a | M3 — `/submit` answers: placeholder response, payload parsing, bad-input handling | Claude | done (no scores produced) |
| 3b | M3 — signal one wired in, `content_id`, audit log entry, `text_too_short` 400 | Claude | done |
| 4a | M4 — `stylometry.py` measures + `style_signal`, four calibration inputs | Claude | done — see DECISIONS |
| 4b | M4 — combining rule (I write it in words; Claude codes it), both scores logged | both | done — see DECISIONS |
| 5a | M5 — three label texts (me), `score_to_label` + thresholds (Claude) | both | next |
| 5b | M5 — `/appeal` | Claude | pending |
| 6 | M6 — README write-up, checklist, submit fork URL | me (Claude checks claims vs code) | pending |
| — | Stretch: `GET /content/<id>` (decide after 5b; declare in README first) | — | undecided |

## Session notes

- 2026-11-12, step 0: `test.py` 9/9 pass (the first run straight after install failed to
  import torch once, then passed). `detector.py` sample: perplexity 12.5, model_signal 0.8864.

- 2026-11-14, step 3a (built ahead of M1/M2 by choice; no signal wired, no scores exist):
  `/submit` validates the body and returns the full response shape with placeholders.
  Bad input: 400 `invalid_json` / `missing_creator_id` / `missing_text` / `empty_text`,
  413 `text_too_long` (over `config.MAX_TEXT_CHARS` = 20 000, a placeholder until
  criteria.md sets the bad-input target). Every rejection goes to `audit.log_rejection`.

- 2026-11-15, step 3b: signal one alone — chatbot paragraph 0.94, my own chat text 0.17,
  roughed-up AI 0.57. Through `/submit`: first call 5.9 s (model load), second 0.12 s;
  `detector_loaded` stays true. `"Hi."` → 400 `text_too_short`; detector missing → 503
  `detector_unavailable`. Each decision is logged with `word_count` as an extra field (for
  criterion 1's short/long split). README Sample Run is filled in at 5b, once the response
  is final.

## Fixed contract points

- Response field `confidence` is the combined score on 0 (human) to 1 (AI). Unit 8's
  `run_attacks.py` and `run_eval.py` compare it to the thresholds.
- `/submit` response carries `content_id`, `guess`, `confidence`, `label`, `model_score`,
  `style_score`.
- Bad input returns a 4xx JSON error and is recorded with `audit.log_rejection`.

## Unit 8

Not started. See RUNNING.md, "Unit 8 — the test".
