# Provenance Guard

> ### 👋 Start here
>
> **New to this repo? Read [RUNNING.md](RUNNING.md) first.**
>
> Once `python test.py` passes, in one terminal:
>
> ```bash
> python app.py
> ```
>
> and in another:
>
> ```bash
> curl -X POST http://127.0.0.1:5000/ping \
>   -H "Content-Type: application/json" \
>   -d '{"message": "hello"}'
> ```
>
> That's a web service. Something sent it text and it sent something back.
> Everything this unit is filling in the middle.
>
> **The rest of this file is your submission.** Fill it in as you go.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     Unit 7 asks for the first five sections. Unit 8 adds the five below.

     Everything is pasted as TEXT. A pasted curl response gets full credit;
     a picture of your terminal gets none.
     ───────────────────────────────────────────────────────────────────────── -->

<!-- ═══════════════════════ UNIT 7 — THE BUILD ═══════════════════════ -->

## What This Does

<!-- The path a submission takes, from arriving to the label a reader sees.
     Six or seven steps — this is the trace you wrote in Milestone 1. -->

A writing site sends a piece of text to Provenance Guard, and gets back a guess about
whether a person or an AI wrote it, a score saying how sure that guess is, and a sentence
the writer can read. If the writer thinks it's wrong, they can appeal.

The path a submission takes (full trace in [docs/milestone1.md](docs/milestone1.md)):

1. **The request arrives** at `POST /submit` with `text` and `creator_id`.
2. **Input checks** (`app.py::submit`) make sure there is usable text to judge. Anything
   broken gets a 4xx error that says what to fix, and is logged as a rejection.
3. **Signal one** (`detector.py::model_signal`) looks at the *words*: how predictable they
   are to a language model. It gives a number from 0 to 1.
4. **Signal two** (`stylometry.py::style_signal`) looks at the *shape*: sentence lengths and
   punctuation. It gives another number from 0 to 1.
5. **Combining** (`scoring.py::combine_signals`) turns the two numbers into one score,
   leaning toward the writer when the signals disagree.
6. **The label** (`scoring.py::score_to_label`) turns that score into one of three sentences
   a person can read.
7. **The log** (`audit.py::log_decision`) records the decision with both signal scores, and
   the response goes back to the writer with a `content_id`. With that id, the writer can
   send `POST /appeal`, which records their reasoning and moves the piece to `under_review`.



---

## Signals and Scoring

<!-- For each signal: what property it measures, why that might differ between
     human and AI writing, and WHAT IT CAN'T SEE.

     The blind spot is not optional. If you can't name it you don't understand
     the signal yet — and unit 8's attack set is built out of blind spots. -->

### Signal one — the model signal

**What it measures:** how predictable the words are to a language model (gpt2, run
locally). The model reads the text and measures its *perplexity*, which is how surprised it
is by each next word. Low surprise becomes a high AI score. I left the starter's mapping
as it was: perplexity 45 scores 0.5 (`detector.py::model_signal`, midpoint 45, steepness 1.6).
It reads only the first 400 tokens, about 300 words.

**Why that might differ between human and AI writing:** AI writing feels *generic*. A
model writes by picking a likely next word, so its text is easy for a model to predict.
People wander more and pick odd, specific words.

**What it can't see:** whether the writing is *personal*. It counts how expected the
words are and never understands what they say. A learner, or someone writing in a second
language, keeps to words they're sure of. That reads as predictable, so this signal is
most likely to accuse the writer with the least ability to argue back.

### Signal two — the style signal

**What it measures:** the *shape* of the text (`stylometry.py::style_signal`):
- **Sentence-length spread:** how much sentence lengths vary (stdev / mean). Weight 0.6.
- **Expressive punctuation:** `; : ! ? ( ) ' " …` per word. Full stops, commas and em
  dashes are left out. Weight 0.4.
- **Word variety:** a moving-average type-token ratio. It's computed and logged, but has
  weight **0**, because on my calibration inputs the chatbot text had *more* varied
  vocabulary than mine, so it pointed the wrong way.

Each measure is mapped onto 0–1 (1 = AI-like) and the weighted average is the score. A
text with only one sentence has no spread, so that part counts as 0.5. Ranges and
calibration results are in [docs/DECISIONS.md](docs/DECISIONS.md).

**Why that might differ between human and AI writing:** AI writing feels *formula-like*.
That shows up as sentences that are all about the same length and tidy, unexpressive
punctuation. Human writing is lumpier.

**What it can't see:** it can't read at all. Anything that changes the shape without
changing the meaning moves it: breaking up sentences, adding contractions, adding typos.
It also reads very short or unpunctuated text as AI-like. My own lowercase chat style has
no expressive punctuation, and scored 0.64 on it.

### The combining rule

**The rule:** lean toward the writer when the signals disagree. If the two scores are
close, average them. If they're far apart, take the lower (more human) one, so the system
only leans AI when both signals point that way.

**The numbers:** close means within **0.3** of each other (`config.DISAGREEMENT_GAP`).
The average weights each signal **0.5** (`config.WEIGHT_MODEL_SIGNAL`,
`config.WEIGHT_STYLE_SIGNAL`). Labels: below **0.35** is human, **0.35** up to
**0.65** is unsure, **0.65** and above is AI (`config.HUMAN_THRESHOLD`,
`config.AI_THRESHOLD`).

**Where it lives:** `scoring.py::combine_signals`

<!-- ⚠️ The grader checks your code against that line. If your rule lives
     somewhere else, say where. -->

**A case where my two signals split, and what my rule does with it:** a message I wrote
myself, in lowercase with only commas and full stops. Signal one said human (**0.19**);
signal two said AI-ish (**0.64**), because there was no expressive punctuation. They're
0.45 apart, so the rule takes the lower score. Combined **0.19**: "We think this was written
by a human." Plain averaging would have given 0.42, which is "unsure", on something I wrote.

The opposite split nearly happened on lightly-edited AI text: model 0.69, style 0.40, a
gap of 0.29. That's just under the line, so the rule averaged them to 0.54, "unsure". A
slightly heavier edit would push the gap past 0.3, and the rule would let it through at
about 0.40.



---

## Label Variants

<!-- The exact text of all three labels, as a reader would see them, and the
     score range each covers.

     Write them for someone who has never heard the word "threshold". -->

| Label | Score range | The exact text a reader sees |
|---|---|---|
| high-confidence human | 0.00 up to (not including) 0.35 | We think this was written by a human. |
| unsure | 0.35 up to (not including) 0.65 | We're not sure who wrote this, you can appeal. |
| high-confidence AI | 0.65 – 1.00 | We think this might be AI, you can appeal. |

Every score from 0 to 1 maps to exactly one label (checked with a sweep of 0.0000–1.0000).
All three were reached by real text through `/submit`: my own writing → human (0.19,
0.20), lightly-edited AI → unsure (0.54), a chatbot paragraph → AI (0.92). The text lives in
`scoring.py` as `LABEL_HUMAN`, `LABEL_UNSURE` and `LABEL_AI`.

**Why I worded the "unsure" one this way:**
<!-- It's the hardest of the three. It has to admit uncertainty without
     sounding like an accusation, because the person reading it may well have
     written every word themselves. -->

Because a real writer shouldn't feel accused, and they can appeal. Not all AI writing has
patterns: with good prompting and correction, someone can get AI content that is signal
free. So the system can't be sure either way, and the label says so honestly and points
straight to the appeal.



---

## Sample Run

<!-- One submission and one appeal, pasted as text: the request, the response,
     and the log entries. -->

**A submission**

<!-- The response needs content_id, guess, confidence, label, AND both
     signal scores - model_score and style_score. Unit 8's tools read those
     two off the response, so leaving them out costs you next unit's
     diagnostics. -->

```bash
$ curl -X POST http://127.0.0.1:5000/submit \
  -H "Content-Type: application/json" \
  -d '{"text": "Writing is a powerful tool for self-expression and communication. It allows individuals to share their thoughts, ideas, and experiences with others in a meaningful way. Additionally, writing can help people develop critical thinking skills and improve their ability to communicate effectively.", "creator_id": "sample_writer"}'
```

```json
{
  "confidence": 0.938,
  "content_id": "e3a8c193-5425-43e8-8d6a-89c9763fc7b4",
  "creator_id": "sample_writer",
  "guess": "ai",
  "label": "We think this might be AI, you can appeal.",
  "model_score": 0.9471,
  "status": "decided",
  "style_score": 0.9289
}
```

**An appeal**

```bash
$ curl -X POST http://127.0.0.1:5000/appeal \
  -H "Content-Type: application/json" \
  -d '{"content_id": "e3a8c193-5425-43e8-8d6a-89c9763fc7b4", "reasoning": "Sample-run appeal for the README: this is a demonstration of the appeal path on a piece labelled AI."}'
```

```json
{
  "content_id": "e3a8c193-5425-43e8-8d6a-89c9763fc7b4",
  "message": "We've received your appeal and marked this piece as under review.",
  "status": "under_review"
}
```

**What the log shows afterwards**

```bash
$ curl "http://127.0.0.1:5000/log?limit=2"
```

```json
{
  "count": 2,
  "entries": [
    {
      "combined_score": 0.938,
      "content_id": "e3a8c193-5425-43e8-8d6a-89c9763fc7b4",
      "creator_id": "sample_writer",
      "guess": "ai",
      "label": "We think this might be AI, you can appeal.",
      "model_score": 0.9471,
      "signals_disagree": false,
      "status": "decided",
      "style_score": 0.9289,
      "timestamp": "2026-11-16T00:11:42+00:00",
      "word_count": 41
    },
    {
      "content_id": "e3a8c193-5425-43e8-8d6a-89c9763fc7b4",
      "creator_id": "sample_writer",
      "event": "appeal",
      "reasoning": "Sample-run appeal for the README: this is a demonstration of the appeal path on a piece labelled AI.",
      "status": "under_review",
      "timestamp": "2026-11-16T00:11:42+00:00"
    }
  ]
}
```

The original decision stays in the log unchanged; the appeal is a new entry after it with
`status: under_review`. An unknown `content_id` returns `404 content_not_found`, and blank
reasoning returns `400 empty_reasoning`.

---

## How I Used AI

I used Claude (Claude Code) through the whole build. It asked me questions one at a time
for the parts that had to be mine (the trace, the criteria, the combining rule, the
labels), wrote the code around my answers, and ran the curl tests.

**Moment 1: the false-positive number in criterion 1**

- *What I asked for:* help writing my criteria. I'd chosen "at most 2 of 10 short pieces
  labelled AI", and said I picked 2 "to leave room for the three runs".
- *What came back:* my reasoning was backwards. A lower number is *stricter*, so it leaves
  less room. If any one of the three runs produced a third wrong label, the criterion
  would fail. Both 2 and 3 were defensible; the choice was mine.
- *What I changed:* I raised it to 3, because short pieces give the signals very little to
  go on and the model can score the same text differently between runs. The reason under
  criterion 1 now says that.

**Moment 2: word variety pointed the wrong way**

- *What I asked for:* build the style signal from the three measures in the brief:
  sentence-length spread, word variety, punctuation.
- *What came back:* before scaling anything, Claude printed the raw measures on my four
  calibration inputs. Word variety had the chatbot text at 0.88 and my own writing at 0.77,
  so the AI text had *more* varied vocabulary. That's the opposite of what the brief
  expected.
- *What I changed:* word variety stays in the code and is still computed, but it counts
  for nothing (weight 0). Spread and punctuation carry the signal. I wrote the finding in
  Signals and Scoring instead of leaving a measure in that quietly made the score worse.

<!-- ═══════════════════════ UNIT 8 — THE TEST ═══════════════════════ -->

---

## Rate Limiting

**My limits:** 10 per minute, 200 per day (`config.RATE_LIMIT_PER_MINUTE`,
`config.RATE_LIMIT_PER_DAY`), on `POST /submit` only

**Why those numbers and not others:** a real writer working without AI is unlikely
to submit 10 pieces in a minute or 200 in a day, unless they prepared them in advance.

**What a caller counts as:** per `creator_id`, because a writer should have their own
limit. A request with no `creator_id` counts against its address.

**The run of status codes when I pushed past it:**

<!-- python run_attacks.py --flood 15 -->

`python run_attacks.py --flood 15`: 15 submissions in a burst as `flood_tester`
(`results/flood_2026-11-15_2008.md`):

```
200 200 200 200 200 200 200 200 200 200 429 429 429 429 429
```

The 429 response:

```json
{"error":"rate_limited","limit":"10 per 1 minute","message":"Too many submissions. Try again shortly."}
```

Each 429 is also in the audit log as a rejection, so a flood leaves a trace:

```json
{"creator_id": "flood_tester", "event": "rejected", "status": "rejected", "reason": "rate_limited", "limit": "10 per 1 minute"}
```

A different `creator_id` submitting straight after the flood still got a 200.

---

## Attack Run — Before

<!-- Every attack with its outcome and a held-or-broke mark.
     `run_attacks.py --label before` produces the table. -->

Full run: `results/attack_run_2026-11-15_2240_before.md` (56 attacks, 0 crashes).

**How I judged**
- Human writing labelled **unsure** is HELD, because the writer isn't accused and can appeal.
- AI text labelled **unsure** is BROKE, because the AI text isn't caught.
- A prompt injection is judged by whether the AI text was still caught, not by whether the
  instruction was obeyed, because the AI text still gets through.
- Something that isn't really writing getting a label at all is BROKE, because it
  shouldn't be judged as writing.

**False positives (genuine human writing)**

| ID | Targeting | Guess | Score | model | style | Verdict |
|---|---|---|---|---|---|---|
| FP01 | plain, clear human writing | unsure | 0.616 | 0.618 | 0.614 | HELD |
| FP02 | formal register | ai | 0.839 | 0.739 | 0.940 | BROKE |
| FP03 | non-native speaker writing carefully | ai | 0.806 | 0.805 | 0.808 | BROKE |
| FP04 | student essay written to a rubric | ai | 0.791 | 0.833 | 0.750 | BROKE |
| FP05 | technical documentation | ai | 0.843 | 0.800 | 0.885 | BROKE |
| FP06 | imitating a formal template | unsure | 0.521 | 0.881 | 0.521 | HELD |
| FP07 | deliberate repetition | unsure | 0.400 | 0.882 | 0.400 | HELD |
| FP08 | very short genuine submission | human | 0.322 | 0.322 | 0.650 | HELD |

**Evasion (AI text disguised)**

| ID | Targeting | Guess | Score | model | style | Verdict |
|---|---|---|---|---|---|---|
| EV01 | signal two: typos raise word variety | human | 0.164 | 0.164 | 1.000 | BROKE |
| EV02 | signal two: broken-up sentences | unsure | 0.497 | 0.594 | 0.400 | BROKE |
| EV03 | signal two: a pasted quotation | human | 0.235 | 0.666 | 0.235 | BROKE |
| EV04 | signal one: unusual words | unsure | 0.611 | 0.611 | 1.000 | BROKE |
| EV05 | both: heavy human editing pass | unsure | 0.361 | 0.321 | 0.400 | BROKE |
| EV06 | signal two: one very long and one very short sentence | unsure | 0.486 | 0.573 | 0.400 | BROKE |
| EV07 | signal two: padding with punctuation | unsure | 0.443 | 0.586 | 0.300 | BROKE |
| EV08 | signal one: text below the token window | human | 0.245 | 0.245 | 0.876 | BROKE |
| EV09 | both: human opening paragraph bolted on | human | 0.311 | 0.704 | 0.311 | BROKE |
| EV10 | signal two: repeated stanza structure | ai | 0.844 | 0.979 | 0.709 | HELD |

**Prompt injection.** No instruction was obeyed: every label is the fixed text from
`scoring.py`, and PI05's fake JSON did not add fields to its log entry. PI01–03 and PI05
wrap an AI paragraph; PI04 and PI06 wrap human writing.

| ID | Targeting | Under it | Guess | Score | model | style | Verdict |
|---|---|---|---|---|---|---|---|
| PI01 | instruction to ignore the check | AI | unsure | 0.431 | 0.463 | 0.400 | BROKE |
| PI02 | instruction disguised as a system message | AI | human | 0.213 | 0.204 | 0.222 | BROKE |
| PI03 | instruction in the writer's voice | AI | unsure | 0.490 | 0.594 | 0.385 | BROKE |
| PI04 | make the label text hostile | human | unsure | 0.402 | 0.500 | 0.305 | HELD |
| PI05 | inject into the audit log | AI | human | 0.193 | 0.640 | 0.193 | BROKE |
| PI06 | instruction plus real human text | human | unsure | 0.595 | 0.558 | 0.632 | HELD |

**Malformed.** A refusal is HELD when it is a 4xx with `error` and `message` and shows up
in `/log` as rejected (criterion 3). All 15 refusals below did.

| ID | Targeting | Status | Result | Verdict |
|---|---|---|---|---|
| MF01 | text is only whitespace | 400 | `empty_text` | HELD |
| MF02 | text is a single character | 400 | `text_too_short` | HELD |
| MF03 | control characters plus "test red" | 200 | human, 0.000 (model 0.000, style 0.700) | BROKE |
| MF04 | only punctuation | 200 | human, 0.011 (model 0.011, style 1.000) | BROKE |
| MF05 | one 4,000-character word | 200 | ai, 0.849 (model 0.998, style 0.700) | BROKE |
| MF06 | emoji only | 200 | ai, 0.848 (model 0.997, style 0.700) | BROKE |
| MF07 | a real Arabic sentence | 200 | ai, 0.803 (model 0.906, style 0.700) | BROKE |
| MF08 | 57,640 characters | 413 | `text_too_long` | HELD |
| RQ01 | no text field | 400 | `missing_text` | HELD |
| RQ02 | no creator_id | 400 | `missing_creator_id` | HELD |
| RQ03 | text is a number | 400 | `missing_text` | HELD |
| RQ04 | text is a list | 400 | `missing_text` | HELD |
| RQ05 | text is null | 400 | `missing_text` | HELD |
| RQ06 | creator_id is an object | 400 | `missing_creator_id` | HELD |
| RQ07 | body is a JSON array | 400 | `invalid_json` | HELD |
| RQ08 | unparseable JSON | 400 | `invalid_json` | HELD |
| RQ09 | empty body | 400 | `invalid_json` | HELD |
| RQ10 | form-encoded body | 400 | `invalid_json` | HELD |
| RQ11 | JSON sent as `text/plain` | 400 | `invalid_json` | HELD |
| RQ12 | deeply nested JSON | 400 | `missing_text` | HELD |

MF07 is real writing called ai, so it is BROKE under the first rule as well.

**Flood (one creator, 12 in a burst).** FL01_01–10 got 200; FL01_11 and FL01_12 got 429
`rate_limited` ("10 per 1 minute"), both logged. The limit stopped the 11th: HELD.

**Totals:** 56 attacks · HELD 34 · BROKE 22 (false positive 4, evasion 9, injection 4,
malformed 5, flood 0). No crashes.



**Ten audit log entries from the run**

<!-- Choose entries that show the interesting failures, not the ten easiest. -->

From `results/audit_extract_before.json`. In order: four AI texts that passed as human
(EV09, EV03, EV08, PI05), two human writers called ai (FP03, FP02), two non-writing inputs
that got a label (MF07, MF04), and two refusals (MF08, the flood).

```json
{"combined_score": 0.3107, "content_id": "2a4ad9bd-07da-4cb5-bfae-abf69e6cc785", "creator_id": "attacker_EV09", "guess": "human", "label": "We think this was written by a human.", "model_score": 0.7042, "signals_disagree": true, "status": "decided", "style_score": 0.3107, "timestamp": "2026-11-16T03:39:57+00:00", "word_count": 110}
{"combined_score": 0.2349, "content_id": "f4d42683-6da1-4de7-a70d-218e15e69084", "creator_id": "attacker_EV03", "guess": "human", "label": "We think this was written by a human.", "model_score": 0.6662, "signals_disagree": true, "status": "decided", "style_score": 0.2349, "timestamp": "2026-11-16T03:39:56+00:00", "word_count": 105}
{"combined_score": 0.2452, "content_id": "75e5b268-56f6-49a1-a289-a4fbea829711", "creator_id": "attacker_EV08", "guess": "human", "label": "We think this was written by a human.", "model_score": 0.2452, "signals_disagree": true, "status": "decided", "style_score": 0.8758, "timestamp": "2026-11-16T03:39:57+00:00", "word_count": 10}
{"combined_score": 0.1929, "content_id": "f2ef5dc1-6bad-42bc-890b-6581eaaca1a4", "creator_id": "attacker_PI05", "guess": "human", "label": "We think this was written by a human.", "model_score": 0.6401, "signals_disagree": true, "status": "decided", "style_score": 0.1929, "timestamp": "2026-11-16T03:40:00+00:00", "word_count": 28}
{"combined_score": 0.8064, "content_id": "ea9565db-6042-4afd-bc7e-874b79fdd36a", "creator_id": "attacker_FP03", "guess": "ai", "label": "We think this might be AI, you can appeal.", "model_score": 0.8051, "signals_disagree": false, "status": "decided", "style_score": 0.8077, "timestamp": "2026-11-16T03:39:58+00:00", "word_count": 83}
{"combined_score": 0.8391, "content_id": "2455ac3d-04ff-4b21-810e-08fe43bf17d7", "creator_id": "attacker_FP02", "guess": "ai", "label": "We think this might be AI, you can appeal.", "model_score": 0.7387, "signals_disagree": false, "status": "decided", "style_score": 0.9395, "timestamp": "2026-11-16T03:39:58+00:00", "word_count": 76}
{"combined_score": 0.8032, "content_id": "df556ce1-739b-4dc9-91d0-63bab729f4ad", "creator_id": "attacker_MF07", "guess": "ai", "label": "We think this might be AI, you can appeal.", "model_score": 0.9064, "signals_disagree": false, "status": "decided", "style_score": 0.7, "timestamp": "2026-11-16T03:40:01+00:00", "word_count": 17}
{"combined_score": 0.0112, "content_id": "c012f88c-b852-42a7-ae9c-8ce35c4e4c4a", "creator_id": "attacker_MF04", "guess": "human", "label": "We think this was written by a human.", "model_score": 0.0112, "signals_disagree": true, "status": "decided", "style_score": 1.0, "timestamp": "2026-11-16T03:40:00+00:00", "word_count": 8}
{"creator_id": "attacker_MF08", "event": "rejected", "length": 57640, "reason": "text_too_long", "status": "rejected", "timestamp": "2026-11-16T03:40:01+00:00"}
{"creator_id": "attacker_flood", "event": "rejected", "limit": "10 per 1 minute", "reason": "rate_limited", "status": "rejected", "timestamp": "2026-11-16T03:40:02+00:00"}
```

**The single worst outcome** — the one I'd least want to explain to a writer
whose work got caught by it:

**EV09**, AI text with a human opening paragraph bolted on, labelled "We think this was
written by a human." (0.311). I don't think the human intervention will be meaningful, yet
it was enough to pass the whole piece. The model signal read it as AI (0.704), the style
signal read it as human (0.311), the gap was over 0.3, and my combining rule took the lower
score.


---

## Run Log and Verdicts

<!-- Your five criteria across three trials. `run_eval.py --label before`. -->

Full run: `results/run_2026-11-16_1117_before.md`. Inputs are in `scenarios.py`.
Criteria 2 and 3 are checked by `run_eval.py` itself (`appeal_reasoning` and
`check_rejections`, see `docs/DECISIONS.md`); their counts are under "Checks" in the report.

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. My own writing is rarely called AI | short: ≤3 of 10 `ai`; long: ≤1 of 10 `ai` | short 0, long **3** | short 0, long **3** | short 0, long **3** | **MISSED** (long) |
| 2. Every appeal is recorded | 10 of 10 `under_review` and in `/log` | 10 / 10 | 10 / 10 | 10 / 10 | MET |
| 3. Broken requests get a clear error | 7 of 7: 4xx with `error` + `message`, logged, `/ping` 200 | 7, 7 logged, ping 200 | 7, 7 logged, ping 200 | 7, 7 logged, ping 200 | MET |
| 4. All three labels reachable | each label on ≥2 of 9 | ai 5, unsure 2, human 2 | ai 5, unsure 2, human 2 | ai 5, unsure 2, human 2 | MET |
| 5. AI and human score apart | AI mean − my mean ≥ 0.30 | 0.843 − 0.293 = 0.550 | 0.550 | 0.550 | MET |

Every score was identical across the three trials: gpt2 on CPU returns the same number
for the same text.

**Real output from one trial**, pasted as text, naming the file and function
that produced it: `run_eval.py::main`, trial 1 of "long pieces of mine", the three pieces
labelled ai.

```json
[
  {
    "status": 200,
    "guess": "ai",
    "confidence": 0.6683,
    "model_score": 0.7899,
    "style_score": 0.5466,
    "label": "We think this might be AI, you can appeal.",
    "error_code": null,
    "has_message": false,
    "sent": "I don't know why, but lately I've been thinking a lot about how quickl"
  },
  {
    "status": 200,
    "guess": "ai",
    "confidence": 0.6759,
    "model_score": 0.7522,
    "style_score": 0.5995,
    "label": "We think this might be AI, you can appeal.",
    "error_code": null,
    "has_message": false,
    "sent": "I've started writing this message a few times and deleted it every tim"
  },
  {
    "status": 200,
    "guess": "ai",
    "confidence": 0.6555,
    "model_score": 0.7757,
    "style_score": 0.5353,
    "label": "We think this might be AI, you can appeal.",
    "error_code": null,
    "has_message": false,
    "sent": "Went here with two friends on Friday night. The food was actually pret"
  }
]
```

Trial 1 checks for criteria 2 and 3, from the same report:

```
appeals:    {"appeals_sent": 10, "under_review": 10, "in_log": 10}
bad input:  {"4xx": 7, "not_4xx": 0, "with_error_and_message": 7, "rejections_logged": 7, "ping_status": 200}
```

**Diagnoses**

<!-- For each miss AND each broken attack: the stage and the mechanism.

     Your service has five stages: the route, signal one, signal two, the
     combining rule, and the label mapping.

     Not a diagnosis:  "The evasion attacks got through."
     A diagnosis:      "Four evasion inputs got through. All four had typos
                        added to AI-generated text. My second signal measures
                        word variety, and typos raise word variety — so it read
                        them as more human. My combining rule weights that
                        signal at 0.6, so it dragged the whole score down."

     Look for a pattern. Five failures on one signal is one problem, not five. -->

The 22 broken attacks and the criterion 1 miss fall into five patterns.

**A. Human writing called ai, with both signals high.** FP02, FP03, FP04, FP05, and three
of my own long pieces (the criterion 1 miss).

What they share: they're clean and predictable, or casual in tone, and non-relational.

- **Stage:** signal one and signal two together. Then the combining rule, which averaged
  them, and the label mapping, which put the average at or over 0.65.
- **Mechanism:** signal one scores how predictable the text is to gpt2. Clean, correct
  prose in common words is easy to predict, so all seven scored 0.74–0.83. Signal two
  scores sentence-length spread and expressive punctuation. These texts have evenly sized
  sentences and few `; : ! ? ( )`, so style scored 0.54–0.94. The two signals were within
  0.3 of each other, so my rule took their average, and every average was 0.65 or more.
  My own three pieces only just crossed (0.655, 0.668, 0.676).

**B. AI text passed as human because the rule took the style score.** EV03 (a pasted
quotation), EV09 (a human opening paragraph), PI05 (fake JSON).

Why style believed them: the added parts have quotes, and I treat quoted text as human,
because AI doesn't own anything (at least under today's regulations).

- **Stage:** signal two, then the combining rule.
- **Mechanism:** signal two counts `"` and `'` as expressive punctuation, and at 0.05 marks
  per word or more that part scores fully human. EV03 (0.057 per word) and PI05 (0.433,
  every JSON key is quoted) both hit it and scored 0 on punctuation. EV09's marks are
  apostrophes in the added paragraph's contractions ("I've", "don't", "here's"), 0.036 per
  word. The added parts also change sentence lengths, so spread moved toward human
  (0.33–0.39). Style came out 0.19–0.31 while the model read all three as AI (0.64–0.70).
  The gap was over 0.3, so my rule took the lower score, and the label was human.

**C. The model signal read AI text as human.** EV01 (typos), EV05 (heavy human edit),
EV08 (10 words), PI02 (a "SYSTEM:" line on top).

Why: the model never saw those odd words together before, and it is trained on clean
output with no errors.

- **Stage:** signal one, and for EV01 and EV08 the combining rule as well.
- **Mechanism:** signal one turns gpt2's perplexity into a score; text the model finds
  hard to predict scores human. Typos (EV01, model 0.164), a heavy edit (EV05, 0.321) and
  an instruction line full of `guess=human, confidence=0.02` (PI02, 0.204) are all
  word sequences gpt2 rarely saw, so perplexity went up. EV08 has a different cause:
  with 10 words the model has almost no context, so each word is hard to predict
  (0.245). In EV01 and EV08 the style signal did read AI (1.000 and 0.876), but the gap
  was over 0.3, so my rule took the lower model score.

**D. AI text landed in unsure.** EV02, EV04, EV06, EV07, PI01, PI03 (final scores
0.431–0.611).

Why: both. The signals are easy to fool, and the band is wide.

- **Stage:** signal one and signal two, then the label mapping.
- **Mechanism:** each attack pushed one style part fully to the human end.
  - EV02 (broken-up sentences, spread 0.85), EV06 (one long and one short sentence, 1.19)
    and PI01 (short instruction sentences before long AI ones, 0.66) maxed out sentence-length
    spread. Style fell to 0.40.
  - EV07 (punctuation padding, 0.062 per word) and PI03 (a note in parentheses, 0.054)
    maxed out expressive punctuation. Style fell to 0.30 and 0.39.
  - EV04 (unusual words) left style at 1.00 but raised perplexity, so the model gave 0.611.
    The gap was over 0.3, so my rule took that lower score.

  The model signal itself scored all six between 0.46 and 0.61, never reaching 0.65, so
  neither signal pulled the result into the AI band. My unsure band is 0.30 wide (0.35 up
  to 0.65), and every final score landed inside it.

**E. Something that isn't writing got a label.** MF03 (control characters), MF04 (only
punctuation), MF05 (one 4,000-character word), MF06 (emoji), MF07 (Arabic).

Where it should have stopped: the route, which should check the text is real words.

- **Stage:** the route.
- **Mechanism:** `/submit` refuses text that is missing, blank, over 20,000 characters, or
  under 3 tokens. Nothing checks that the text is words in a language gpt2 knows, so all
  five reached the signals, and the signals score any characters at all.
  - **Called ai.** `aaaa…`, repeated emoji and Arabic broken into byte pieces are easy
    for gpt2 to predict once the pattern starts (model 0.906–0.998). Each counts as one
    sentence with no expressive punctuation, so style gave 0.70 on all three. The scores
    agreed, and the average was 0.80–0.85.
  - **Called human.** Control characters and punctuation runs are unlike anything gpt2
    saw (model 0.000 and 0.011). Style said AI (0.70 and 1.00), so the gap was over 0.3,
    and my rule took the lower model score.



---

## The Improvement

**What I changed:** the route now checks that `text` is English writing before either
signal scores it (`app.py::_writing_problem`, called from `submit`). Text that fails gets a
400 `not_writing`, and the log entry records which check it failed:

| Check | Refuses | Setting |
|---|---|---|
| `control_characters` | any control character except newline, carriage return and tab | — |
| `too_few_english_letters` | under 60% of non-space characters are Latin letters | `config.MIN_LETTER_SHARE = 0.6` |
| `word_too_long` | a run of more than 45 letters | `config.MAX_WORD_LETTERS = 45` |

Before choosing 0.6, I ran the check on every input I had. My own 20 pieces and the 9-text
set sat at 0.86 or above, and so did every real-text attack (lowest: PI05 at 0.88). MF04,
MF06 and MF07 sat at 0.00.

**Which diagnosis pointed at it:** pattern E. The route should check the text is real
words.

### Attack Run — After

<!-- Same format. `run_attacks.py --label after` -->

Full run: `results/attack_run_2026-11-16_1213_after.md` (56 attacks, 0 crashes). I
compared every row with the before run: exactly five changed, and the other 51 came back
with the same status, guess and score.

| ID | Targeting | Before | After | Verdict before → after |
|---|---|---|---|---|
| MF03 | control characters | 200 human 0.000 | 400 `not_writing` (`control_characters`) | BROKE → HELD |
| MF04 | only punctuation | 200 human 0.011 | 400 `not_writing` (`too_few_english_letters`) | BROKE → HELD |
| MF05 | one 4,000-character word | 200 ai 0.849 | 400 `not_writing` (`word_too_long`) | BROKE → HELD |
| MF06 | emoji only | 200 ai 0.848 | 400 `not_writing` (`too_few_english_letters`) | BROKE → HELD |
| MF07 | an Arabic sentence | 200 ai 0.803 | 400 `not_writing` (`too_few_english_letters`) | BROKE → HELD |

**Totals:** HELD 39 · BROKE 17 (before: 34 · 22). Malformed is now 20 of 20 HELD.

Two of the new log entries:

```json
{"check": "control_characters", "creator_id": "attacker_MF03", "event": "rejected", "reason": "not_writing", "status": "rejected", "timestamp": "2026-11-16T17:13:05+00:00"}
{"check": "too_few_english_letters", "creator_id": "attacker_MF07", "event": "rejected", "reason": "not_writing", "status": "rejected", "timestamp": "2026-11-16T17:13:05+00:00"}
```

**Did it help, and how do I know:** yes, for pattern E. All five inputs that got a label
before are now refused with a reason, and nothing else in the attack run moved. My five
criteria came out the same as before (`results/run_2026-11-16_1213_after.md`): 2–5 still
MET, criterion 1 still MISSED on long pieces (3 of 10 called ai). None of my own writing
was refused.

The cost: a writer who writes in Arabic, or any other non-Latin script, used to get a
wrong "AI" label and now gets "Only English writing can be checked." That is better than
a false accusation, but those writers are still not served. This change does nothing for
patterns A–D, so 17 attacks still break and criterion 1 is still missed.



---

## What's Still Broken

<!-- For each attack still getting through and each criterion still missed:
     what you'd do, and why you stopped. -->



**The trade I'd make if this ran for real:**

<!-- Two sentences. Fewer wrong accusations means more AI text getting through.
     Say which way you'd go and WHO PAYS FOR IT. -->



<!-- ═════════════════════════════════════════════════════════════════════

     SUBMISSION CHECKLIST — unit 7

       [ ] criteria.md has five numbered criteria, each naming a target
       [ ] Each has a reason underneath
       [ ] POST /submit returns content_id, guess, confidence, label,
           model_score and style_score
       [ ] Two signals that measure DIFFERENT things, each with a named blind spot
       [ ] Three label variants, all reachable, written out in full
       [ ] POST /appeal changes status and writes to the log
       [ ] Signals and Scoring names scoring.py::combine_signals
       [ ] Sample Run: a submission AND an appeal, as pasted text
       [ ] At least four new commits
       [ ] Repository URL submitted — WRITE IT DOWN

     SUBMISSION CHECKLIST — unit 8

       [ ] Rate limiting on /submit, with your numbers justified
       [ ] The pasted run of status codes showing 429
       [ ] Audit log with all nine fields, recording rejections too
       [ ] The attack set run IN FULL, every input with an outcome
       [ ] Ten audit log entries pasted as text
       [ ] Five criteria across three trials
       [ ] A diagnosis for every miss and every broken attack — stage AND mechanism
       [ ] One improvement, with Attack Run — After
       [ ] What's Still Broken, including the production trade
       [ ] At least four new commits
       [ ] The SAME repository URL as last unit

     Do not delete and recreate this repository.
     ═════════════════════════════════════════════════════════════════════ -->

---

📖 **How to run this project: [RUNNING.md](RUNNING.md)**
