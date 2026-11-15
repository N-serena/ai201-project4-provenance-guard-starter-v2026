# Milestone 1 — tracing a submission

My answers, worked out in conversation on 2026-11-15, put in order. The words in quotes
are mine as I first said them; the rest connects them to the files in this repo.

---

## 1. The path a poem takes

"When the person submits the poem … the poem is carried in a post request, then [the]
service in charge saves it to [a] datastore."

In this project the result comes back in the response to that same POST. Between arriving
and answering, the service has to *decide* something:

1. **The request arrives** at `POST /submit` with `text` and `creator_id`.
2. **Input checks** (`app.py::submit`) make sure there is usable text to judge.
3. **Signal one** (`detector.py::model_signal`) looks at the words and gives a number.
4. **Signal two** (`stylometry.py::style_signal`) looks at the shape and gives a number.
5. **Combining** (`scoring.py::combine_signals`) turns the two numbers into one score.
6. **The label** (`scoring.py::score_to_label`) turns the score into a sentence a person reads.
7. **The log** (`audit.py::log_decision`) saves the decision, and the response goes back to
   the writer.

---

## 2. What the signals look for, and what they can't see

What I'd look for as a reader: "patterns, because AI writing has a pattern." AI writing
"feels generic, less personal, formula-like."

| What I noticed | Which signal | What it measures |
|---|---|---|
| "generic" | Signal one — `detector.py` | How predictable the words are to a language model (perplexity). Generic writing picks the expected word every time. |
| "formula-like" | Signal two — `stylometry.py` | The shape: sentence-length spread, word variety, punctuation. A formula shows up as evenness. |
| "less personal" | **Neither** | — |

**Blind spot shared by both:** neither signal understands what the text says. They count
things. A personal story told in plain words looks the same to them as a generic one.

**Signal two's extra blind spot:** it only sees shape, so changing the shape without
changing the meaning (breaking up sentences, adding typos) moves its score.

---

## 3. The false positive

Who gets wrongly flagged: "a learner might depict these signals." Someone still learning
to write, or writing in a second language, keeps to words they are sure of and the
structure they were taught. That reads as predictable *and* formula-like, so both
signals point the same wrong way, and the person accused has the least ability to argue back.

What the system should do for them: "it should be gentle, point out the signals or the
reason why, and let them appeal."

- The label must not sound like an accusation.
- It says what the system noticed, in plain words.
- It points to the appeal.

This is the case the thresholds in Milestone 4 and the labels in Milestone 5 have to
protect.

---

## 4. The two endpoints

*Still to confirm.* This is what `/submit` does now (step 3a), plus open questions for
`/appeal`.

### POST /submit

In: `{"text": string, "creator_id": string}`

Out (200):

| Field | Type | Meaning |
|---|---|---|
| `content_id` | string | ID for this submission; `/appeal` needs it |
| `creator_id` | string | Echoed back |
| `guess` | `"ai"` / `"human"` / `"unsure"` | Short machine-readable verdict |
| `confidence` | number 0–1 | Combined score: 0 = confidently human, 1 = confidently AI |
| `label` | string | The sentence the writer reads |
| `model_score` | number 0–1 | Signal one |
| `style_score` | number 0–1 | Signal two |
| `status` | string | `"decided"` |

Errors: each returns `{"error": code, "message": text}` and is logged as a rejection.

| Case | Status | `error` |
|---|---|---|
| Body isn't a JSON object | 400 | `invalid_json` |
| `creator_id` missing or blank | 400 | `missing_creator_id` |
| `text` missing or not a string | 400 | `missing_text` |
| `text` blank | 400 | `empty_text` |
| `text` over 20 000 characters | 413 | `text_too_long` |

### POST /appeal

In: `{"content_id": string, "reasoning": string}`

Open questions for me:
- What does the writer get back when it works?
- What happens if the `content_id` doesn't exist?
- Is empty `reasoning` allowed?
