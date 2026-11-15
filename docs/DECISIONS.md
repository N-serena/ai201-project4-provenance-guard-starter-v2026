# Decisions — Provenance Guard

Newest first. Each entry: the decision, the date, and why.

---

## 2026-11-15 — Style signal: what it measures and how it's weighted

`stylometry.py::style_signal` maps three measures onto 0–1 (1 = AI-like) with a clipped
straight line, then takes a weighted average.

| Measure | Raw value | AI end → human end | Weight |
|---|---|---|---|
| Sentence-length spread | stdev / mean of words per sentence | 0.20 → 0.60 | 0.6 |
| Word variety | moving-average TTR, 40-word window | 0.65 → 0.85 | **0.0** |
| Expressive punctuation | `; : ! ? ( ) ' " …` per word (no `. , —`) | 0.00 → 0.05 | 0.4 |

Calibration inputs (both human samples are my own chat messages):

| Input | spread | TTR | punct | **style** | **model** |
|---|---|---|---|---|---|
| clearly AI | 0.258 | 0.878 | 0.000 | 0.913 | 0.926 |
| clearly human | 0.438 | 0.771 | 0.000 | 0.643 | 0.188 |
| plain human | 0.548 | 0.916 | 0.026 | 0.270 | 0.135 |
| lightly-edited AI | 0.415 | 0.738 | 0.035 | 0.397 | 0.688 |

**Why:**
- Spread was the only measure that put the AI text at the AI end, so it gets the most weight.
- TTR pointed the wrong way: the chatbot text had *more* varied vocabulary (0.878) than my
  first sample (0.771). It stays computed but counts for nothing.
- Em dashes are left out of punctuation because current chatbots use them heavily. Plain
  hyphens are left out because AI compounds ("self-expression") would count as expressive.
- Fewer than two sentences: spread scores 0.5 (no evidence either way).

**Known weaknesses:**
- Text with no expressive punctuation scores 1.0 on that part. My own lowercase chat style
  has none, and so does most very short text. A one-sentence input with no punctuation
  scores 0.70.
- Contractions alone pull text toward human, which is how the lightly-edited AI got 0.397.
- The ranges were set from four texts, so they're a starting point.

---

## 2026-11-15 — Endpoint contracts settled

Both endpoints' fields and error cases are in `docs/milestone1.md`, section 4. `/appeal`
confirms with `status: under_review`, returns 404 for an unknown `content_id`, and refuses
blank reasoning with a 400.

**Why:** a writer who appeals should see that something happened. An unknown id has to fail
loudly, because a typo that silently succeeds looks like a working appeal that went nowhere.
An appeal with no reasoning gives a reviewer nothing to act on.

---

## 2026-11-12 — `confidence` is the combined score

The `confidence` field in the `/submit` response holds the combined score, from 0.0
(confidently human) to 1.0 (confidently AI).

**Why:** unit 8's `run_attacks.py` and `run_eval.py` read `confidence` and compare it to the
thresholds. Any other meaning, such as distance from 0.5, would make every row of next
unit's reports wrong.
