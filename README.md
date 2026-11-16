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

**My limits:** ___ per minute, ___ per day

**Why those numbers and not others:**
<!-- Think about two people: a real writer submitting their own work a few
     times an hour, and a script sending a thousand variations to map your
     thresholds. Your numbers have to be liveable for the first and hostile to
     the second. -->

**What a caller counts as:** <!-- per address, or per creator_id? They fail
differently — one script can look like a thousand callers, and one household
can look like one. -->

**The run of status codes when I pushed past it:**

<!-- python run_attacks.py --flood 15 -->

```

```

---

## Attack Run — Before

<!-- Every attack with its outcome and a held-or-broke mark.
     `run_attacks.py --label before` produces the table. -->



**Ten audit log entries from the run**

<!-- Choose entries that show the interesting failures, not the ten easiest. -->

```json

```

**The single worst outcome** — the one I'd least want to explain to a writer
whose work got caught by it:



---

## Run Log and Verdicts

<!-- Your five criteria across three trials. `run_eval.py --label before`. -->

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1.  |  |  |  |  |  |
| 2.  |  |  |  |  |  |
| 3.  |  |  |  |  |  |
| 4.  |  |  |  |  |  |
| 5.  |  |  |  |  |  |

**Real output from one trial**, pasted as text, naming the file and function
that produced it:

```json

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



---

## The Improvement

**What I changed:**

**Which diagnosis pointed at it:**

### Attack Run — After

<!-- Same format. `run_attacks.py --label after` -->



**Did it help, and how do I know:**

<!-- Widening the unsure band usually fixes one problem and creates another.
     Reporting that trade honestly is worth full credit. -->



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
