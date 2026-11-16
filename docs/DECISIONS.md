# Decisions — Provenance Guard

Newest first. Each entry: the decision, the date, and why.

---

## 2026-11-16 — Criteria 2 and 3 are tested by an extended `run_eval.py`

`scenarios.py` gained two keys and `run_eval.py` reads them:
- `appeal_reasoning`: after each successful submit, appeal its `content_id` and check
  `/log` for the appeal entry.
- `check_rejections`: after each trial, count 4xx responses, responses carrying
  `error` and `message`, rejected entries the trial added to `/log`, and the `/ping`
  status.

A `bodies` entry that is a str is sent as raw bytes, for criterion 3's "body isn't JSON".

**Why:** criterion 2 and 3 have to hold in all three trials, and checking 30 appeals and
21 bad requests by hand is slow and easy to get wrong. The checks land in the same report
as the other criteria.

---

## 2026-11-15 — Rate limits: 10 per minute, 200 per day, per creator

Rate limiting is on by default (`config.RATE_LIMITING_ENABLED`; `AI201_RATE_LIMITS=0`
turns it off). `/submit` allows 10 a minute and 200 a day per `creator_id`, falling back
to the caller's address when there is none (starter's `rate_limit_key`). Storage is
in-memory, so a restart resets every count.

`--flood 15` gave 10 × 200 then 5 × 429, each logged as `rate_limited`. A different
creator straight after still got 200.

**Why:** a real writer working without AI is unlikely to submit 10 pieces in a minute or
200 in a day unless they prepared them in advance. Counting per creator gives each writer
their own limit.

**Known weakness:** a script can send a new `creator_id` on every request and get a fresh
limit each time.

---

## 2026-11-15 — Labels and thresholds

| Label | Score range | Text |
|---|---|---|
| high-confidence human | 0.00 up to (not including) 0.35 | We think this was written by a human. |
| unsure | 0.35 up to (not including) 0.65 | We're not sure who wrote this, you can appeal. |
| high-confidence AI | 0.65 – 1.00 | We think this might be AI, you can appeal. |

The text lives in `scoring.py` (`LABEL_HUMAN`, `LABEL_UNSURE`, `LABEL_AI`); thresholds in
`config.py`. A sweep of 0.0000–1.0000 found no gaps. Through `/submit` all three are
reached: my writing → human (0.19, 0.20), edited AI → unsure (0.54), chatbot → AI (0.92).

**Why:** the labels are my own words. I read them back as the writer would (the unsure and
AI labels don't say why, and both end in "you can appeal", so they sound alike) and chose
to keep them as written. Thresholds stay at the starter 0.35 / 0.65: on my four inputs they
put every text where I'd expect it.

---

## 2026-11-15 — Combining rule: lean toward the writer when the signals disagree

`scoring.py::combine_signals`:
- If `model_score` and `style_score` are within **0.3** of each other (`DISAGREEMENT_GAP`),
  the combined score is their average (weights **0.5 / 0.5**).
- If they are more than 0.3 apart, the combined score is the **lower** of the two.

Each log entry records `signals_disagree` so unit 8 can see which branch ran.

Through `/submit`:

| Input | model | style | combined | branch |
|---|---|---|---|---|
| clearly AI | 0.926 | 0.913 | 0.919 | average |
| clearly human (mine) | 0.188 | 0.643 | 0.188 | lower |
| plain human (mine) | 0.135 | 0.270 | 0.202 | average |
| lightly-edited AI | 0.688 | 0.397 | 0.543 | average |

**Why:** a wrong "AI" label on a real writer is the expensive mistake, so a big
disagreement goes the writer's way. I picked averaging-when-close (version B) over
always-take-the-lower (version A) so that lightly-edited AI lands near the middle (0.54)
instead of passing as human (0.40).

**Known weakness:** the edited AI's gap was 0.29, just under the line. A slightly heavier
edit pushes the gap past 0.3, the rule takes the lower score, and it scores about 0.40.

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
