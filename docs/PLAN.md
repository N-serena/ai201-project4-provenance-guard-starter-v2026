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
| 5a | M5 — three label texts (me), `score_to_label` + thresholds (Claude) | both | done — see DECISIONS |
| 5b | M5 — `/appeal` | Claude | done — README Sample Run filled |
| 6 | M6 — README write-up, checklist, submit fork URL | me (Claude checks claims vs code) | done — commit, push, submit URL |
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

- 2026-11-16, step 5b: `/appeal` follows the Milestone 1 contract. Only a logged decision
  can be appealed; rejections are stored with `requested_content_id`, so a fake id stays a
  404 on every try. Repeat appeals on one id are each recorded. Appeal rejections are
  logged with `endpoint: "appeal"`. The confirmation message text is Claude's draft, so I
  can reword it.

## Fixed contract points

- Response field `confidence` is the combined score on 0 (human) to 1 (AI). Unit 8's
  `run_attacks.py` and `run_eval.py` compare it to the thresholds.
- `/submit` response carries `content_id`, `guess`, `confidence`, `label`, `model_score`,
  `style_score`.
- Bad input returns a 4xx JSON error and is recorded with `audit.log_rejection`.

## Unit 8

The attack set (staff-written) is in `attack_set/`: 32 rows in `attacks.csv` (evasion 10,
false_positive 8, prompt_injection 6, malformed 8) and 24 in
`attacks_malformed_requests.csv` (malformed 12, flood_same_creator 12).

| # | Step | Owner | Status |
|---|---|---|---|
| 1 | Rate limiting: numbers, enable, `--flood 15` → 429s in README | me (numbers, why), Claude (wiring) | done — see DECISIONS |
| 2 | Attack run before: `run_attacks.py --set attack_set --label before`, HELD/BROKE per row | script sends, I judge | done — 34 HELD / 22 BROKE, 0 crashes; worst: EV09 |
| 3 | Own criteria, three trials: fill `scenarios.py`, `run_eval.py --label before` | Claude + my writing | done — `results/run_2026-11-16_1117_before.md`; only criterion 1 (long) missed: 3 of 10 called ai, every trial |
| 4 | Verdicts and diagnoses: stage + mechanism for each miss | me (Claude checks) | done — five patterns A–E in README "Diagnoses" |
| 5 | One improvement, `--label after` | both | done — route word check; 39 HELD / 17 BROKE, criteria unchanged |
| 6 | What's Still Broken + production trade | me | pending |

From the before run (for step 4's diagnoses):
- EV03, EV09 and PI05 passed as human the same way: model said AI (0.64–0.70), style said
  human, the gap was over 0.3, and the combining rule took the lower score.
- FP02–FP05 were called ai with both signals agreeing (0.74–0.94).
- MF03–MF07 got a label: nothing checks that the text is English words before scoring.

From the eval run (before):
- Scores were identical in all three trials: gpt2 on CPU gives the same number each time.
- The model signal put all 10 of my long pieces between 0.67 and 0.80. Style pulled 7 of
  them down; the 3 called ai (long 2, 9, 10) had style 0.54–0.60, inside the 0.3 gap, so
  the average ran and landed just over 0.65 (0.655–0.676).

First things to watch, from unit 7:
- Short or unpunctuated text leans AI on the style signal (criterion 1's short pieces).
- Lightly-edited AI sat 0.01 under the disagreement gap; a heavier edit slips it to ~0.40.
- Criterion 1 needs 20 pieces of my own writing and criterion 4/5 a 9-text set, all in
  `scenarios.py`. See RUNNING.md, "Unit 8 — the test".
