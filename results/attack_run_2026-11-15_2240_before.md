# Attack run — before

- Produced by: `run_attacks.py::main`
- Service: `app.py::submit`
- 56 attacks · 2026-11-15 22:40
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
| EV01 | evasion | signal two: typos raise word variety | 200 | `b9536b75-d44d-4bf3-887e-770f0f6d82b7` | human | 0.164 |  |
| EV02 | evasion | signal two: broken-up sentences raise length spread | 200 | `807fa102-31ed-4233-b7ba-b3eb65769d42` | unsure | 0.497 |  |
| EV03 | evasion | signal two: a pasted quotation changes the shape | 200 | `f4d42683-6da1-4de7-a70d-218e15e69084` | human | 0.235 |  |
| EV04 | evasion | signal one: unusual words raise perplexity | 200 | `55c1c9b3-88f3-4cee-b71f-8c6f38363208` | unsure | 0.611 |  |
| EV05 | evasion | both signals: heavy human editing pass | 200 | `69515bfc-9342-403f-acaf-3a68eebbb8c7` | unsure | 0.361 |  |
| EV06 | evasion | signal two: one very long sentence and one very short | 200 | `818ba838-c981-4a84-9994-edfb91b3579b` | unsure | 0.486 |  |
| EV07 | evasion | signal two: padding with punctuation | 200 | `d04080f2-5a98-4e4a-ae0d-1e2bb26eb779` | unsure | 0.443 |  |
| EV08 | evasion | signal one: text below the token window | 200 | `75e5b268-56f6-49a1-a289-a4fbea829711` | human | 0.245 |  |
| EV09 | evasion | both: AI text with a human opening paragraph bolted on | 200 | `2a4ad9bd-07da-4cb5-bfae-abf69e6cc785` | human | 0.311 |  |
| EV10 | evasion | signal two: repeated stanza structure | 200 | `ba9002ad-3f41-48c0-bf45-fde03eda8e68` | ai | 0.844 |  |
| FP01 | false_positive | plain, clear human writing with no flourishes | 200 | `0834afa1-df3c-4528-83ef-43bb5dd3cf81` | unsure | 0.616 |  |
| FP02 | false_positive | human writing in a formal register | 200 | `2455ac3d-04ff-4b21-810e-08fe43bf17d7` | ai | 0.839 |  |
| FP03 | false_positive | a non-native English speaker writing carefully | 200 | `ea9565db-6042-4afd-bc7e-874b79fdd36a` | ai | 0.806 |  |
| FP04 | false_positive | a student essay written to a rubric | 200 | `37f49ea1-9057-4362-a3b1-e9d6f27baba5` | ai | 0.791 |  |
| FP05 | false_positive | technical documentation written by a person | 200 | `350b995e-945b-4743-9b7f-e44780430333` | ai | 0.843 |  |
| FP06 | false_positive | a person imitating a formal template | 200 | `9537271a-704d-4c2b-aac4-e83c707e4844` | unsure | 0.521 |  |
| FP07 | false_positive | human writing that repeats a phrase deliberately | 200 | `a4549210-ae0c-4222-9cff-448c1db4587f` | unsure | 0.400 |  |
| FP08 | false_positive | very short genuine human submission | 200 | `f1c08b44-1bed-4039-9b57-47a0fef5756b` | human | 0.322 |  |
| PI01 | prompt_injection | instruction to ignore the check | 200 | `2e65a3b2-3060-4978-a41a-f93721424c5e` | unsure | 0.431 |  |
| PI02 | prompt_injection | instruction disguised as a system message | 200 | `c491a59e-ea74-4015-a2b3-02ca70944a6a` | human | 0.213 |  |
| PI03 | prompt_injection | instruction wrapped in the writer's voice | 200 | `5cad98c6-4f1f-4be6-a2e8-42efa8cc34f5` | unsure | 0.490 |  |
| PI04 | prompt_injection | attempt to make the label text hostile | 200 | `f254da98-dadd-4582-b8dc-6b1590f68644` | unsure | 0.402 |  |
| PI05 | prompt_injection | attempt to inject into the audit log | 200 | `f2ef5dc1-6bad-42bc-890b-6581eaaca1a4` | human | 0.193 |  |
| PI06 | prompt_injection | instruction plus real human text | 200 | `3be7b676-cd69-443e-ae35-25b0570ff53e` | unsure | 0.595 |  |
| MF01 | malformed | text is only whitespace | 400 | `—` | — | — |  |
| MF02 | malformed | text is a single character | 400 | `—` | — | — |  |
| MF03 | malformed | text is control characters | 200 | `fdff36e7-3770-4441-8b9a-71633f30f34d` | human | 0.000 |  |
| MF04 | malformed | text is only punctuation | 200 | `c012f88c-b852-42a7-ae9c-8ce35c4e4c4a` | human | 0.011 |  |
| MF05 | malformed | text is a very long single word | 200 | `e9c50fde-571d-4064-8af2-bcc7bb0adcb3` | ai | 0.849 |  |
| MF06 | malformed | text is emoji only | 200 | `f310a92e-4fc0-4592-bb89-df7bcb27b6a2` | ai | 0.848 |  |
| MF07 | malformed | text is right-to-left script | 200 | `df556ce1-739b-4dc9-91d0-63bab729f4ad` | ai | 0.803 |  |
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
| FL01_01 | flood_same_creator | 20 rapid submissions from one creator | 200 | `f1621ea5-146f-4d0b-b7fe-9ee93e25bb25` | human | 0.029 |  |
| FL01_02 | flood_same_creator | 20 rapid submissions from one creator | 200 | `0012d27c-0516-4e63-8b4c-e10d32f73e79` | human | 0.029 |  |
| FL01_03 | flood_same_creator | 20 rapid submissions from one creator | 200 | `2886e4be-64af-47bb-b2c9-862223b900d1` | human | 0.029 |  |
| FL01_04 | flood_same_creator | 20 rapid submissions from one creator | 200 | `fd5ced92-7199-444c-97c9-1ce8de5234c9` | human | 0.029 |  |
| FL01_05 | flood_same_creator | 20 rapid submissions from one creator | 200 | `4dd73b16-1815-4db6-9d6b-018152604061` | human | 0.029 |  |
| FL01_06 | flood_same_creator | 20 rapid submissions from one creator | 200 | `c4609ff3-198c-474d-b332-5400a5294f6f` | human | 0.029 |  |
| FL01_07 | flood_same_creator | 20 rapid submissions from one creator | 200 | `bf0025e8-78de-4ffd-9255-031c3887fd7c` | human | 0.029 |  |
| FL01_08 | flood_same_creator | 20 rapid submissions from one creator | 200 | `e5568f72-137d-4c29-a8db-30f0e0188623` | human | 0.029 |  |
| FL01_09 | flood_same_creator | 20 rapid submissions from one creator | 200 | `a40bf29f-4fbd-4e8e-969c-2f1013baeff6` | human | 0.029 |  |
| FL01_10 | flood_same_creator | 20 rapid submissions from one creator | 200 | `06afd59a-879e-4d47-8652-e5c08ce9030d` | human | 0.029 |  |
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
  "content_id": "b9536b75-d44d-4bf3-887e-770f0f6d82b7",
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
  "content_id": "807fa102-31ed-4233-b7ba-b3eb65769d42",
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
  "content_id": "f4d42683-6da1-4de7-a70d-218e15e69084",
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
  "content_id": "55c1c9b3-88f3-4cee-b71f-8c6f38363208",
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
  "content_id": "69515bfc-9342-403f-acaf-3a68eebbb8c7",
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
  "content_id": "818ba838-c981-4a84-9994-edfb91b3579b",
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
  "content_id": "d04080f2-5a98-4e4a-ae0d-1e2bb26eb779",
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
  "content_id": "75e5b268-56f6-49a1-a289-a4fbea829711",
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
  "content_id": "2a4ad9bd-07da-4cb5-bfae-abf69e6cc785",
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
  "content_id": "ba9002ad-3f41-48c0-bf45-fde03eda8e68",
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
  "content_id": "0834afa1-df3c-4528-83ef-43bb5dd3cf81",
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
  "content_id": "2455ac3d-04ff-4b21-810e-08fe43bf17d7",
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
  "content_id": "ea9565db-6042-4afd-bc7e-874b79fdd36a",
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
  "content_id": "37f49ea1-9057-4362-a3b1-e9d6f27baba5",
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
  "content_id": "350b995e-945b-4743-9b7f-e44780430333",
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
  "content_id": "9537271a-704d-4c2b-aac4-e83c707e4844",
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
  "content_id": "a4549210-ae0c-4222-9cff-448c1db4587f",
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
  "content_id": "f1c08b44-1bed-4039-9b57-47a0fef5756b",
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
  "content_id": "2e65a3b2-3060-4978-a41a-f93721424c5e",
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
  "content_id": "c491a59e-ea74-4015-a2b3-02ca70944a6a",
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
  "content_id": "5cad98c6-4f1f-4be6-a2e8-42efa8cc34f5",
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
  "content_id": "f254da98-dadd-4582-b8dc-6b1590f68644",
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
  "content_id": "f2ef5dc1-6bad-42bc-890b-6581eaaca1a4",
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
  "content_id": "3be7b676-cd69-443e-ae35-25b0570ff53e",
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
  "status": 200,
  "content_id": "fdff36e7-3770-4441-8b9a-71633f30f34d",
  "creator_id": "attacker_MF03",
  "guess": "human",
  "confidence": 0.0,
  "model_score": 0.0,
  "style_score": 0.7,
  "label": "We think this was written by a human.",
  "error": null,
  "verdict": ""
}
```

### MF04 — `malformed`

*Targeting:* text is only punctuation

```json
{
  "id": "MF04",
  "status": 200,
  "content_id": "c012f88c-b852-42a7-ae9c-8ce35c4e4c4a",
  "creator_id": "attacker_MF04",
  "guess": "human",
  "confidence": 0.0112,
  "model_score": 0.0112,
  "style_score": 1.0,
  "label": "We think this was written by a human.",
  "error": null,
  "verdict": ""
}
```

### MF05 — `malformed`

*Targeting:* text is a very long single word

```json
{
  "id": "MF05",
  "status": 200,
  "content_id": "e9c50fde-571d-4064-8af2-bcc7bb0adcb3",
  "creator_id": "attacker_MF05",
  "guess": "ai",
  "confidence": 0.8488,
  "model_score": 0.9976,
  "style_score": 0.7,
  "label": "We think this might be AI, you can appeal.",
  "error": null,
  "verdict": ""
}
```

### MF06 — `malformed`

*Targeting:* text is emoji only

```json
{
  "id": "MF06",
  "status": 200,
  "content_id": "f310a92e-4fc0-4592-bb89-df7bcb27b6a2",
  "creator_id": "attacker_MF06",
  "guess": "ai",
  "confidence": 0.8484,
  "model_score": 0.9969,
  "style_score": 0.7,
  "label": "We think this might be AI, you can appeal.",
  "error": null,
  "verdict": ""
}
```

### MF07 — `malformed`

*Targeting:* text is right-to-left script

```json
{
  "id": "MF07",
  "status": 200,
  "content_id": "df556ce1-739b-4dc9-91d0-63bab729f4ad",
  "creator_id": "attacker_MF07",
  "guess": "ai",
  "confidence": 0.8032,
  "model_score": 0.9064,
  "style_score": 0.7,
  "label": "We think this might be AI, you can appeal.",
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
  "content_id": "f1621ea5-146f-4d0b-b7fe-9ee93e25bb25",
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
  "content_id": "0012d27c-0516-4e63-8b4c-e10d32f73e79",
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
  "content_id": "2886e4be-64af-47bb-b2c9-862223b900d1",
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
  "content_id": "fd5ced92-7199-444c-97c9-1ce8de5234c9",
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
  "content_id": "4dd73b16-1815-4db6-9d6b-018152604061",
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
  "content_id": "c4609ff3-198c-474d-b332-5400a5294f6f",
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
  "content_id": "bf0025e8-78de-4ffd-9255-031c3887fd7c",
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
  "content_id": "e5568f72-137d-4c29-a8db-30f0e0188623",
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
  "content_id": "a40bf29f-4fbd-4e8e-969c-2f1013baeff6",
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
  "content_id": "06afd59a-879e-4d47-8652-e5c08ce9030d",
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
