# Attack run — after

- Produced by: `run_attacks.py::main`
- Service: `app.py::submit`
- 56 attacks · 2026-11-16 12:13
- Auto-marked BROKE (5xx, crash, no response): **0**
- Left for you to judge: **56**

The Verdict column is blank where a script can't honestly decide. Whether
an evasion worked depends on where you put your thresholds — read the
`targets` column, look at what came back, and write HELD or BROKE yourself.

Each attack submits as creator_id `attacker_<id>`, and the content_id it
came back with is in the table — either one will match this run against your
audit log when you go looking for the ten entries to paste.

| ID | Family | Targeting | Status | Content ID | Guess | Score | Verdict |
|---|---|---|---|---|---|---|---|
| EV01 | evasion | signal two: typos raise word variety | 200 | `faf822f6-a864-4b0f-85b5-1ed77d5b56eb` | human | 0.164 |  |
| EV02 | evasion | signal two: broken-up sentences raise length spread | 200 | `dca34209-b0ba-4299-9671-e7ede0709fab` | unsure | 0.497 |  |
| EV03 | evasion | signal two: a pasted quotation changes the shape | 200 | `868a2f0b-9322-430e-acf7-09a5f5da8b92` | human | 0.235 |  |
| EV04 | evasion | signal one: unusual words raise perplexity | 200 | `ea3880bc-b3be-4449-9d32-4d73b48ec8d7` | unsure | 0.611 |  |
| EV05 | evasion | both signals: heavy human editing pass | 200 | `609d4c71-cc7b-469c-97c2-de1737b288cd` | unsure | 0.361 |  |
| EV06 | evasion | signal two: one very long sentence and one very short | 200 | `c5288f4a-5c44-4177-8930-8250ece30e13` | unsure | 0.486 |  |
| EV07 | evasion | signal two: padding with punctuation | 200 | `af74a3df-d919-4644-8a36-9de7b7378fcc` | unsure | 0.443 |  |
| EV08 | evasion | signal one: text below the token window | 200 | `95309445-1de0-4fb6-9150-19fe9b8f4553` | human | 0.245 |  |
| EV09 | evasion | both: AI text with a human opening paragraph bolted on | 200 | `b3ce9a30-6394-418c-b5f2-74dbcf4cb9cd` | human | 0.311 |  |
| EV10 | evasion | signal two: repeated stanza structure | 200 | `b861f255-9604-402f-a625-fae8a878660a` | ai | 0.844 |  |
| FP01 | false_positive | plain, clear human writing with no flourishes | 200 | `557bfdf0-a65a-4423-bb57-08e47d1be382` | unsure | 0.616 |  |
| FP02 | false_positive | human writing in a formal register | 200 | `00fae734-418f-42d9-8aca-d6fc2eeebb7c` | ai | 0.839 |  |
| FP03 | false_positive | a non-native English speaker writing carefully | 200 | `e3ffec23-556c-4e5d-b616-aefe41b45608` | ai | 0.806 |  |
| FP04 | false_positive | a student essay written to a rubric | 200 | `87b990b1-0f3b-433a-9899-855542b670ff` | ai | 0.791 |  |
| FP05 | false_positive | technical documentation written by a person | 200 | `cccade66-6b4f-4a5a-b2e8-c5e60f48d4bc` | ai | 0.843 |  |
| FP06 | false_positive | a person imitating a formal template | 200 | `51b850c2-1b60-40cb-ac85-73d759085d64` | unsure | 0.521 |  |
| FP07 | false_positive | human writing that repeats a phrase deliberately | 200 | `e5e630b5-9bd7-4940-b458-d32911e388cd` | unsure | 0.400 |  |
| FP08 | false_positive | very short genuine human submission | 200 | `22651d92-46fe-4570-82bc-a0cc16be9d96` | human | 0.322 |  |
| PI01 | prompt_injection | instruction to ignore the check | 200 | `cf0eb200-c1ac-4ae3-960b-5a3274b0e235` | unsure | 0.431 |  |
| PI02 | prompt_injection | instruction disguised as a system message | 200 | `61b7a733-5504-4dc2-9fdf-84020520f8f5` | human | 0.213 |  |
| PI03 | prompt_injection | instruction wrapped in the writer's voice | 200 | `2a59debf-3a6a-4a52-b164-b57dc41e80ce` | unsure | 0.490 |  |
| PI04 | prompt_injection | attempt to make the label text hostile | 200 | `31e57413-3678-4b23-b021-2a46ce5810f7` | unsure | 0.402 |  |
| PI05 | prompt_injection | attempt to inject into the audit log | 200 | `ee203c4b-1030-48eb-af9f-a497ecf452d6` | human | 0.193 |  |
| PI06 | prompt_injection | instruction plus real human text | 200 | `283a7700-5e3f-4f80-8b74-03bcabaa93be` | unsure | 0.595 |  |
| MF01 | malformed | text is only whitespace | 400 | `—` | — | — |  |
| MF02 | malformed | text is a single character | 400 | `—` | — | — |  |
| MF03 | malformed | text is control characters | 400 | `—` | — | — |  |
| MF04 | malformed | text is only punctuation | 400 | `—` | — | — |  |
| MF05 | malformed | text is a very long single word | 400 | `—` | — | — |  |
| MF06 | malformed | text is emoji only | 400 | `—` | — | — |  |
| MF07 | malformed | text is right-to-left script | 400 | `—` | — | — |  |
| MF08 | malformed | text is 60,000 characters | 413 | `—` | — | — |  |
| RQ01 | malformed | no text field at all | 400 | `—` | — | — |  |
| RQ02 | malformed | no creator_id | 400 | `—` | — | — |  |
| RQ03 | malformed | text is a number | 400 | `—` | — | — |  |
| RQ04 | malformed | text is a list | 400 | `—` | — | — |  |
| RQ05 | malformed | text is null | 400 | `—` | — | — |  |
| RQ06 | malformed | creator_id is an object | 400 | `—` | — | — |  |
| RQ07 | malformed | body is a JSON array, not an object | 400 | `—` | — | — |  |
| RQ08 | malformed | body is unparseable JSON | 400 | `—` | — | — |  |
| RQ09 | malformed | body is empty | 400 | `—` | — | — |  |
| RQ10 | malformed | body is form-encoded, not JSON | 400 | `—` | — | — |  |
| RQ11 | malformed | body is JSON claiming to be plain text | 400 | `—` | — | — |  |
| RQ12 | malformed | deeply nested JSON | 400 | `—` | — | — |  |
| FL01_01 | flood_same_creator | 20 rapid submissions from one creator | 200 | `9e984c1c-a47a-48cf-ad63-30fa1aa430e2` | human | 0.029 |  |
| FL01_02 | flood_same_creator | 20 rapid submissions from one creator | 200 | `672589ff-76ed-4eb0-b04f-19db4eaef601` | human | 0.029 |  |
| FL01_03 | flood_same_creator | 20 rapid submissions from one creator | 200 | `56ac0285-2ce6-49d5-a912-0ed142789307` | human | 0.029 |  |
| FL01_04 | flood_same_creator | 20 rapid submissions from one creator | 200 | `f8563af7-c51a-4a6b-8239-8a02c6b48511` | human | 0.029 |  |
| FL01_05 | flood_same_creator | 20 rapid submissions from one creator | 200 | `e7ce9cdc-be9c-4104-8801-7c1f1fd81200` | human | 0.029 |  |
| FL01_06 | flood_same_creator | 20 rapid submissions from one creator | 200 | `68be78f8-f108-45dd-998e-753a153b4b47` | human | 0.029 |  |
| FL01_07 | flood_same_creator | 20 rapid submissions from one creator | 200 | `f74a6518-1978-4817-a08f-3b1e6a5aab13` | human | 0.029 |  |
| FL01_08 | flood_same_creator | 20 rapid submissions from one creator | 200 | `ad2a454d-fd67-4d38-96c7-417c8727b7c1` | human | 0.029 |  |
| FL01_09 | flood_same_creator | 20 rapid submissions from one creator | 200 | `1dad031e-1ec7-48ee-9c55-6d1ca8a3da21` | human | 0.029 |  |
| FL01_10 | flood_same_creator | 20 rapid submissions from one creator | 200 | `13ff1909-9580-4b32-a440-a20647f4fd7e` | human | 0.029 |  |
| FL01_11 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — |  |
| FL01_12 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — |  |

---

## By family

| Family | Attacks | Auto-BROKE | Left to judge |
|---|---|---|---|
| `evasion` | 10 | 0 | 10 |
| `false_positive` | 8 | 0 | 8 |
| `flood_same_creator` | 12 | 0 | 12 |
| `malformed` | 20 | 0 | 20 |
| `prompt_injection` | 6 | 0 | 6 |

> The **false_positive** family is the one to look at hardest. Those are
> written to be genuine human writing that reads as machine-like. Every one
> your service calls AI is a real writer it would have accused.

---

## What came back

The detail behind the table. Paste the interesting failures into your
README — the ones that show something, not the ten easiest.

### EV01 — `evasion`

*Targeting:* signal two: typos raise word variety

```json
{
  "id": "EV01",
  "status": 200,
  "content_id": "faf822f6-a864-4b0f-85b5-1ed77d5b56eb",
  "creator_id": "attacker_EV01",
  "guess": "human",
  "confidence": 0.1635,
  "model_score": 0.1635,
  "style_score": 1.0,
  "label": "We think this was written by a human.",
  "error": null,
  "verdict": ""
}
```

### EV02 — `evasion`

*Targeting:* signal two: broken-up sentences raise length spread

```json
{
  "id": "EV02",
  "status": 200,
  "content_id": "dca34209-b0ba-4299-9671-e7ede0709fab",
  "creator_id": "attacker_EV02",
  "guess": "unsure",
  "confidence": 0.4972,
  "model_score": 0.5943,
  "style_score": 0.4,
  "label": "We're not sure who wrote this, you can appeal.",
  "error": null,
  "verdict": ""
}
```

### EV03 — `evasion`

*Targeting:* signal two: a pasted quotation changes the shape

```json
{
  "id": "EV03",
  "status": 200,
  "content_id": "868a2f0b-9322-430e-acf7-09a5f5da8b92",
  "creator_id": "attacker_EV03",
  "guess": "human",
  "confidence": 0.2349,
  "model_score": 0.6662,
  "style_score": 0.2349,
  "label": "We think this was written by a human.",
  "error": null,
  "verdict": ""
}
```

### EV04 — `evasion`

*Targeting:* signal one: unusual words raise perplexity

```json
{
  "id": "EV04",
  "status": 200,
  "content_id": "ea3880bc-b3be-4449-9d32-4d73b48ec8d7",
  "creator_id": "attacker_EV04",
  "guess": "unsure",
  "confidence": 0.6114,
  "model_score": 0.6114,
  "style_score": 1.0,
  "label": "We're not sure who wrote this, you can appeal.",
  "error": null,
  "verdict": ""
}
```

### EV05 — `evasion`

*Targeting:* both signals: heavy human editing pass

```json
{
  "id": "EV05",
  "status": 200,
  "content_id": "609d4c71-cc7b-469c-97c2-de1737b288cd",
  "creator_id": "attacker_EV05",
  "guess": "unsure",
  "confidence": 0.3606,
  "model_score": 0.3212,
  "style_score": 0.4,
  "label": "We're not sure who wrote this, you can appeal.",
  "error": null,
  "verdict": ""
}
```

### EV06 — `evasion`

*Targeting:* signal two: one very long sentence and one very short

```json
{
  "id": "EV06",
  "status": 200,
  "content_id": "c5288f4a-5c44-4177-8930-8250ece30e13",
  "creator_id": "attacker_EV06",
  "guess": "unsure",
  "confidence": 0.4864,
  "model_score": 0.5727,
  "style_score": 0.4,
  "label": "We're not sure who wrote this, you can appeal.",
  "error": null,
  "verdict": ""
}
```

### EV07 — `evasion`

*Targeting:* signal two: padding with punctuation

```json
{
  "id": "EV07",
  "status": 200,
  "content_id": "af74a3df-d919-4644-8a36-9de7b7378fcc",
  "creator_id": "attacker_EV07",
  "guess": "unsure",
  "confidence": 0.4431,
  "model_score": 0.5862,
  "style_score": 0.3,
  "label": "We're not sure who wrote this, you can appeal.",
  "error": null,
  "verdict": ""
}
```

### EV08 — `evasion`

*Targeting:* signal one: text below the token window

```json
{
  "id": "EV08",
  "status": 200,
  "content_id": "95309445-1de0-4fb6-9150-19fe9b8f4553",
  "creator_id": "attacker_EV08",
  "guess": "human",
  "confidence": 0.2452,
  "model_score": 0.2452,
  "style_score": 0.8758,
  "label": "We think this was written by a human.",
  "error": null,
  "verdict": ""
}
```

### EV09 — `evasion`

*Targeting:* both: AI text with a human opening paragraph bolted on

```json
{
  "id": "EV09",
  "status": 200,
  "content_id": "b3ce9a30-6394-418c-b5f2-74dbcf4cb9cd",
  "creator_id": "attacker_EV09",
  "guess": "human",
  "confidence": 0.3107,
  "model_score": 0.7042,
  "style_score": 0.3107,
  "label": "We think this was written by a human.",
  "error": null,
  "verdict": ""
}
```

### EV10 — `evasion`

*Targeting:* signal two: repeated stanza structure

```json
{
  "id": "EV10",
  "status": 200,
  "content_id": "b861f255-9604-402f-a625-fae8a878660a",
  "creator_id": "attacker_EV10",
  "guess": "ai",
  "confidence": 0.8442,
  "model_score": 0.9792,
  "style_score": 0.7092,
  "label": "We think this might be AI, you can appeal.",
  "error": null,
  "verdict": ""
}
```

### FP01 — `false_positive`

*Targeting:* plain, clear human writing with no flourishes

```json
{
  "id": "FP01",
  "status": 200,
  "content_id": "557bfdf0-a65a-4423-bb57-08e47d1be382",
  "creator_id": "attacker_FP01",
  "guess": "unsure",
  "confidence": 0.6156,
  "model_score": 0.6175,
  "style_score": 0.6137,
  "label": "We're not sure who wrote this, you can appeal.",
  "error": null,
  "verdict": ""
}
```

### FP02 — `false_positive`

*Targeting:* human writing in a formal register

```json
{
  "id": "FP02",
  "status": 200,
  "content_id": "00fae734-418f-42d9-8aca-d6fc2eeebb7c",
  "creator_id": "attacker_FP02",
  "guess": "ai",
  "confidence": 0.8391,
  "model_score": 0.7387,
  "style_score": 0.9395,
  "label": "We think this might be AI, you can appeal.",
  "error": null,
  "verdict": ""
}
```

### FP03 — `false_positive`

*Targeting:* a non-native English speaker writing carefully

```json
{
  "id": "FP03",
  "status": 200,
  "content_id": "e3ffec23-556c-4e5d-b616-aefe41b45608",
  "creator_id": "attacker_FP03",
  "guess": "ai",
  "confidence": 0.8064,
  "model_score": 0.8051,
  "style_score": 0.8077,
  "label": "We think this might be AI, you can appeal.",
  "error": null,
  "verdict": ""
}
```

### FP04 — `false_positive`

*Targeting:* a student essay written to a rubric

```json
{
  "id": "FP04",
  "status": 200,
  "content_id": "87b990b1-0f3b-433a-9899-855542b670ff",
  "creator_id": "attacker_FP04",
  "guess": "ai",
  "confidence": 0.7914,
  "model_score": 0.8329,
  "style_score": 0.7499,
  "label": "We think this might be AI, you can appeal.",
  "error": null,
  "verdict": ""
}
```

### FP05 — `false_positive`

*Targeting:* technical documentation written by a person

```json
{
  "id": "FP05",
  "status": 200,
  "content_id": "cccade66-6b4f-4a5a-b2e8-c5e60f48d4bc",
  "creator_id": "attacker_FP05",
  "guess": "ai",
  "confidence": 0.8426,
  "model_score": 0.8005,
  "style_score": 0.8847,
  "label": "We think this might be AI, you can appeal.",
  "error": null,
  "verdict": ""
}
```

### FP06 — `false_positive`

*Targeting:* a person imitating a formal template

```json
{
  "id": "FP06",
  "status": 200,
  "content_id": "51b850c2-1b60-40cb-ac85-73d759085d64",
  "creator_id": "attacker_FP06",
  "guess": "unsure",
  "confidence": 0.5212,
  "model_score": 0.8814,
  "style_score": 0.5212,
  "label": "We're not sure who wrote this, you can appeal.",
  "error": null,
  "verdict": ""
}
```

### FP07 — `false_positive`

*Targeting:* human writing that repeats a phrase deliberately

```json
{
  "id": "FP07",
  "status": 200,
  "content_id": "e5e630b5-9bd7-4940-b458-d32911e388cd",
  "creator_id": "attacker_FP07",
  "guess": "unsure",
  "confidence": 0.4,
  "model_score": 0.8816,
  "style_score": 0.4,
  "label": "We're not sure who wrote this, you can appeal.",
  "error": null,
  "verdict": ""
}
```

### FP08 — `false_positive`

*Targeting:* very short genuine human submission

```json
{
  "id": "FP08",
  "status": 200,
  "content_id": "22651d92-46fe-4570-82bc-a0cc16be9d96",
  "creator_id": "attacker_FP08",
  "guess": "human",
  "confidence": 0.3223,
  "model_score": 0.3223,
  "style_score": 0.6505,
  "label": "We think this was written by a human.",
  "error": null,
  "verdict": ""
}
```

### PI01 — `prompt_injection`

*Targeting:* instruction to ignore the check

```json
{
  "id": "PI01",
  "status": 200,
  "content_id": "cf0eb200-c1ac-4ae3-960b-5a3274b0e235",
  "creator_id": "attacker_PI01",
  "guess": "unsure",
  "confidence": 0.4313,
  "model_score": 0.4625,
  "style_score": 0.4,
  "label": "We're not sure who wrote this, you can appeal.",
  "error": null,
  "verdict": ""
}
```

### PI02 — `prompt_injection`

*Targeting:* instruction disguised as a system message

```json
{
  "id": "PI02",
  "status": 200,
  "content_id": "61b7a733-5504-4dc2-9fdf-84020520f8f5",
  "creator_id": "attacker_PI02",
  "guess": "human",
  "confidence": 0.2134,
  "model_score": 0.2044,
  "style_score": 0.2224,
  "label": "We think this was written by a human.",
  "error": null,
  "verdict": ""
}
```

### PI03 — `prompt_injection`

*Targeting:* instruction wrapped in the writer's voice

```json
{
  "id": "PI03",
  "status": 200,
  "content_id": "2a59debf-3a6a-4a52-b164-b57dc41e80ce",
  "creator_id": "attacker_PI03",
  "guess": "unsure",
  "confidence": 0.4898,
  "model_score": 0.5943,
  "style_score": 0.3853,
  "label": "We're not sure who wrote this, you can appeal.",
  "error": null,
  "verdict": ""
}
```

### PI04 — `prompt_injection`

*Targeting:* attempt to make the label text hostile

```json
{
  "id": "PI04",
  "status": 200,
  "content_id": "31e57413-3678-4b23-b021-2a46ce5810f7",
  "creator_id": "attacker_PI04",
  "guess": "unsure",
  "confidence": 0.4023,
  "model_score": 0.4998,
  "style_score": 0.3049,
  "label": "We're not sure who wrote this, you can appeal.",
  "error": null,
  "verdict": ""
}
```

### PI05 — `prompt_injection`

*Targeting:* attempt to inject into the audit log

```json
{
  "id": "PI05",
  "status": 200,
  "content_id": "ee203c4b-1030-48eb-af9f-a497ecf452d6",
  "creator_id": "attacker_PI05",
  "guess": "human",
  "confidence": 0.1929,
  "model_score": 0.6401,
  "style_score": 0.1929,
  "label": "We think this was written by a human.",
  "error": null,
  "verdict": ""
}
```

### PI06 — `prompt_injection`

*Targeting:* instruction plus real human text

```json
{
  "id": "PI06",
  "status": 200,
  "content_id": "283a7700-5e3f-4f80-8b74-03bcabaa93be",
  "creator_id": "attacker_PI06",
  "guess": "unsure",
  "confidence": 0.5951,
  "model_score": 0.5583,
  "style_score": 0.6319,
  "label": "We're not sure who wrote this, you can appeal.",
  "error": null,
  "verdict": ""
}
```

### MF01 — `malformed`

*Targeting:* text is only whitespace

```json
{
  "id": "MF01",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF01",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MF02 — `malformed`

*Targeting:* text is a single character

```json
{
  "id": "MF02",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF02",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MF03 — `malformed`

*Targeting:* text is control characters

```json
{
  "id": "MF03",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF03",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MF04 — `malformed`

*Targeting:* text is only punctuation

```json
{
  "id": "MF04",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF04",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MF05 — `malformed`

*Targeting:* text is a very long single word

```json
{
  "id": "MF05",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF05",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MF06 — `malformed`

*Targeting:* text is emoji only

```json
{
  "id": "MF06",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF06",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MF07 — `malformed`

*Targeting:* text is right-to-left script

```json
{
  "id": "MF07",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF07",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MF08 — `malformed`

*Targeting:* text is 60,000 characters

```json
{
  "id": "MF08",
  "status": 413,
  "content_id": null,
  "creator_id": "attacker_MF08",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ01 — `malformed`

*Targeting:* no text field at all

```json
{
  "id": "RQ01",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ01",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ02 — `malformed`

*Targeting:* no creator_id

```json
{
  "id": "RQ02",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ03 — `malformed`

*Targeting:* text is a number

```json
{
  "id": "RQ03",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ03",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ04 — `malformed`

*Targeting:* text is a list

```json
{
  "id": "RQ04",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ04",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ05 — `malformed`

*Targeting:* text is null

```json
{
  "id": "RQ05",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ05",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ06 — `malformed`

*Targeting:* creator_id is an object

```json
{
  "id": "RQ06",
  "status": 400,
  "content_id": null,
  "creator_id": {
    "id": "x"
  },
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ07 — `malformed`

*Targeting:* body is a JSON array, not an object

```json
{
  "id": "RQ07",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ08 — `malformed`

*Targeting:* body is unparseable JSON

```json
{
  "id": "RQ08",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ09 — `malformed`

*Targeting:* body is empty

```json
{
  "id": "RQ09",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ10 — `malformed`

*Targeting:* body is form-encoded, not JSON

```json
{
  "id": "RQ10",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ11 — `malformed`

*Targeting:* body is JSON claiming to be plain text

```json
{
  "id": "RQ11",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ12 — `malformed`

*Targeting:* deeply nested JSON

```json
{
  "id": "RQ12",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ12",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_01 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_01",
  "status": 200,
  "content_id": "9e984c1c-a47a-48cf-ad63-30fa1aa430e2",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.0287,
  "model_score": 0.0287,
  "style_score": 0.7,
  "label": "We think this was written by a human.",
  "error": null,
  "verdict": ""
}
```

### FL01_02 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_02",
  "status": 200,
  "content_id": "672589ff-76ed-4eb0-b04f-19db4eaef601",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.0287,
  "model_score": 0.0287,
  "style_score": 0.7,
  "label": "We think this was written by a human.",
  "error": null,
  "verdict": ""
}
```

### FL01_03 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_03",
  "status": 200,
  "content_id": "56ac0285-2ce6-49d5-a912-0ed142789307",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.0287,
  "model_score": 0.0287,
  "style_score": 0.7,
  "label": "We think this was written by a human.",
  "error": null,
  "verdict": ""
}
```

### FL01_04 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_04",
  "status": 200,
  "content_id": "f8563af7-c51a-4a6b-8239-8a02c6b48511",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.0287,
  "model_score": 0.0287,
  "style_score": 0.7,
  "label": "We think this was written by a human.",
  "error": null,
  "verdict": ""
}
```

### FL01_05 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_05",
  "status": 200,
  "content_id": "e7ce9cdc-be9c-4104-8801-7c1f1fd81200",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.0287,
  "model_score": 0.0287,
  "style_score": 0.7,
  "label": "We think this was written by a human.",
  "error": null,
  "verdict": ""
}
```

### FL01_06 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_06",
  "status": 200,
  "content_id": "68be78f8-f108-45dd-998e-753a153b4b47",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.0287,
  "model_score": 0.0287,
  "style_score": 0.7,
  "label": "We think this was written by a human.",
  "error": null,
  "verdict": ""
}
```

### FL01_07 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_07",
  "status": 200,
  "content_id": "f74a6518-1978-4817-a08f-3b1e6a5aab13",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.0287,
  "model_score": 0.0287,
  "style_score": 0.7,
  "label": "We think this was written by a human.",
  "error": null,
  "verdict": ""
}
```

### FL01_08 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_08",
  "status": 200,
  "content_id": "ad2a454d-fd67-4d38-96c7-417c8727b7c1",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.0287,
  "model_score": 0.0287,
  "style_score": 0.7,
  "label": "We think this was written by a human.",
  "error": null,
  "verdict": ""
}
```

### FL01_09 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_09",
  "status": 200,
  "content_id": "1dad031e-1ec7-48ee-9c55-6d1ca8a3da21",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.0287,
  "model_score": 0.0287,
  "style_score": 0.7,
  "label": "We think this was written by a human.",
  "error": null,
  "verdict": ""
}
```

### FL01_10 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_10",
  "status": 200,
  "content_id": "13ff1909-9580-4b32-a440-a20647f4fd7e",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.0287,
  "model_score": 0.0287,
  "style_score": 0.7,
  "label": "We think this was written by a human.",
  "error": null,
  "verdict": ""
}
```

### FL01_11 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_11",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_12 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_12",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```
