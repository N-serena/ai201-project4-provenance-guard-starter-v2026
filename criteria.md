# Acceptance criteria — Provenance Guard

Five criteria that say what "working" means for this service, written in unit 7
**before** you built it.

**All five are yours.** None are given.

An acceptance criterion names a number or something plainly observable. *"The
detector is accurate"* is an opinion — and perfect AI detection isn't possible
anyway, so it's an opinion about something nobody can deliver. *"Of 10 pieces I
wrote myself, at most 1 is labelled high-confidence AI"* is a criterion.

Under each, write a sentence or two on **why that target**. *"I allow at most 1
false positive in 10 because on a writing site a wrong accusation costs more
than a missed detection"* is a real answer.

> Missing your own targets next unit costs you nothing. Setting a target so
> easy you can't miss it does.

---

## Pick numbers you can defend

**Cover at least three of these five areas.** They're prompts, not a form.

| Area | A question it could answer |
|---|---|
| False positives | How often may a human's writing get called AI? |
| Score spread | How far apart should clearly-AI and clearly-human text score? |
| Label coverage | Is every one of your three labels actually reachable? |
| The appeal path | Does an appeal always change status and always get recorded? |
| Bad input | What happens when `text` is missing, empty, or enormous? |

Two things worth knowing before you pick numbers:

- **The expensive mistake is one-sided.** Missing some AI text costs the site a
  little. Accusing a real writer costs that person a lot. A criterion that
  treats both errors as equally bad is describing a system nobody would ship.
- **Unit 8 tests across three trials, and the target has to hold across all
  three.** Your first signal runs a model, so identical input can score
  differently twice. A target of "at most 1 in 10" against trials of 2, 1, 2 is
  a **miss**.

---
## 1. My own writing is rarely called AI

Of 10 short pieces (under 50 words) that I wrote myself, at most **3** get the
high-confidence AI label (`guess: "ai"`). Of 10 longer pieces (50 words or more) that I
wrote myself, at most **1** gets it. Both limits hold in every one of the three trials.

**Why this target:** a wrong "AI" label on someone's own work is the most expensive mistake
this system can make, and the writer most likely to get it is a learner who writes plainly.
Short pieces give both signals very little to go on, so I allow more room there; longer
pieces give the signals enough text that a wrong accusation is harder to excuse. I chose 3
over 2 for short pieces because the model signal can score the same text differently
between runs, and the limit has to hold in all three.


---

## 2. Every appeal is recorded

Of 10 appeals sent with real `content_id`s from earlier submissions, all **10** return
`status: "under_review"`, and each one appears in `GET /log` as an appeal entry for that
`content_id`. Holds in every one of the three trials.

**Why this target:** the appeal is the only thing standing between a wrong accusation and
nothing at all. A writer who appeals has to be able to trust it worked, so one lost appeal
in ten is not acceptable.


---

## 3. Broken requests get a clear error, never a crash

All **7** kinds of broken request to `POST /submit` get a 4xx response with an `error` code
and a `message`, and none gets a 5xx:

1. body isn't JSON
2. no `creator_id`
3. no `text`
4. `text` isn't a string
5. blank `text`
6. `text` over 20 000 characters
7. text too short to score (for example `"Hi."`)

Each one appears in `GET /log` as a rejected entry, and `POST /ping` still answers afterwards.
Holds in every one of the three trials.

**Why this target:** a crash on malformed input is one of the most common real failures, and
a writer who sends something broken by mistake should be told what to fix. A request that
leaves no trace in the log can't be found later.


---

## 4. All three labels can actually be reached

From a fixed set of 9 texts (3 clearly AI-generated, 3 clearly my own writing, 3 I judge
borderline), each of the three labels (high-confidence human, unsure, high-confidence AI)
is returned for at least **2** texts. Holds in every one of the three trials.

**Why this target:** a label that never appears is a promise the system can't keep, and a
range that produces a label only once could be luck at the edge of a threshold. Two hits
per label shows each range is genuinely reachable.


---

## 5. Clearly-AI and clearly-human text score well apart

Using the same set as criterion 4, the average `confidence` of the 3 clearly AI-generated
texts is at least **0.3** higher than the average `confidence` of the 3 clearly-my-own
texts. Holds in every one of the three trials.

**Why this target:** if the easy cases land close together, every harder case falls into a
narrow middle where one small wobble flips the label. A 0.3 gap leaves room for an "unsure"
band between them without either clear group spilling into it.


---

<!-- ─────────────────────────────────────────────────────────────────────────
     UNIT 8 — read this before you change anything above.

     If a criterion turns out to be BROKEN rather than merely unmet, you can
     revise it, and that earns credit. But never delete or edit the original
     line. Add the revision underneath, like this:

         ## 2. Uncertain cases land in the unsure band

         The system handles uncertain cases well.

         **Why this target:** ...

         > **Revised in unit 8:** Text I judged borderline scores between
         > 0.4 and 0.6 in at least 4 of 5 cases.
         >
         > **Why revised:** "well" gave me nothing to check. I couldn't
         > reach a verdict from it at all.

     That's a revision because the criterion couldn't be MEASURED.

     Lowering a target because you missed it is not a revision, and it costs
     you the point:

         ✗ "At most 1 of 10 of my own pieces flagged as AI" → "at most 3
            of 10", because 1 of 10 turned out to be hard.

     A number you missed stays where it is, gets diagnosed, and gets a fix
     attempted. That's where the points are.
     ───────────────────────────────────────────────────────────────────────── -->
