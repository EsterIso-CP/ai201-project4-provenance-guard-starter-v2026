# Attack run — before

- Produced by: `run_attacks.py::main`
- Service: `app.py::submit`
- 56 attacks · 2026-11-09 12:57
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
| EV01 | evasion | signal two: typos raise word variety | 200 | `1f48d957-3746-40bd-b8e9-53954c6927ee` | human | 0.343 |  |
| EV02 | evasion | signal two: broken-up sentences raise length spread | 200 | `936bb5f6-f452-4af3-a9d5-49c03e9b3796` | unsure | 0.374 |  |
| EV03 | evasion | signal two: a pasted quotation changes the shape | 200 | `8f042da8-9712-47a4-903b-98fbdda278f9` | unsure | 0.529 |  |
| EV04 | evasion | signal one: unusual words raise perplexity | 200 | `80b7a9ee-5368-44b3-a751-fdb07dfdca3b` | unsure | 0.569 |  |
| EV05 | evasion | both signals: heavy human editing pass | 200 | `8aa1dd53-24b9-4e0f-b38f-33632e0f2910` | human | 0.325 |  |
| EV06 | evasion | signal two: one very long sentence and one very short | 200 | `2c3aec38-2ca9-48d0-ac50-71bac7489b65` | unsure | 0.383 |  |
| EV07 | evasion | signal two: padding with punctuation | 200 | `693ce871-3e59-4ce7-989e-970ea9cf8f63` | unsure | 0.584 |  |
| EV08 | evasion | signal one: text below the token window | 200 | `ec936781-bfd6-4576-94b4-3ede1f9890df` | human | 0.284 |  |
| EV09 | evasion | both: AI text with a human opening paragraph bolted on | 200 | `6f408ae0-f8a2-4f24-a5f4-99109d596790` | unsure | 0.518 |  |
| EV10 | evasion | signal two: repeated stanza structure | 200 | `0c68508e-057f-46a0-82ef-5808578ebaca` | ai | 0.766 |  |
| FP01 | false_positive | plain, clear human writing with no flourishes | 200 | `44a26b06-a144-4cff-9d11-8363c2e7d6b2` | unsure | 0.522 |  |
| FP02 | false_positive | human writing in a formal register | 200 | `b1481e36-45d2-445c-ab89-3e195311dc24` | unsure | 0.643 |  |
| FP03 | false_positive | a non-native English speaker writing carefully | 200 | `cbf75b89-8fce-4552-a8d6-fb507b43f4b1` | unsure | 0.635 |  |
| FP04 | false_positive | a student essay written to a rubric | 200 | `88ac7942-7ecd-4c04-b682-6178f20b55c6` | unsure | 0.615 |  |
| FP05 | false_positive | technical documentation written by a person | 200 | `337d36a1-dec6-46cc-8485-e411e1a9794f` | ai | 0.719 |  |
| FP06 | false_positive | a person imitating a formal template | 200 | `174b72b4-50ee-48de-bba3-ce7a5bcc5b9f` | unsure | 0.620 |  |
| FP07 | false_positive | human writing that repeats a phrase deliberately | 200 | `17429c04-9d2c-4d75-8d64-9e10f117e935` | unsure | 0.635 |  |
| FP08 | false_positive | very short genuine human submission | 200 | `7438f1cf-4d29-4fea-bb13-e79ff3be6583` | human | 0.276 |  |
| PI01 | prompt_injection | instruction to ignore the check | 200 | `70dc1577-b141-497a-b5d9-67fb96afe0cc` | human | 0.280 |  |
| PI02 | prompt_injection | instruction disguised as a system message | 200 | `42eed533-a99b-4d49-b028-d9dad1065783` | human | 0.178 |  |
| PI03 | prompt_injection | instruction wrapped in the writer's voice | 200 | `8a47562d-7003-43f9-8880-de7c29bc84a4` | unsure | 0.492 |  |
| PI04 | prompt_injection | attempt to make the label text hostile | 200 | `45bf2be1-3061-46fd-93e8-77a216181001` | unsure | 0.461 |  |
| PI05 | prompt_injection | attempt to inject into the audit log | 200 | `5cb04de7-c75c-4707-b8d9-e68b5f326aa6` | unsure | 0.523 |  |
| PI06 | prompt_injection | instruction plus real human text | 200 | `0a4ed6b5-619b-47de-89f3-9c866a64bab4` | unsure | 0.484 |  |
| MF01 | malformed | text is only whitespace | 400 | `—` | — | — |  |
| MF02 | malformed | text is a single character | 400 | `—` | — | — |  |
| MF03 | malformed | text is control characters | 200 | `ebefbcf0-30cf-46f4-98bf-62335071ee9c` | human | 0.125 |  |
| MF04 | malformed | text is only punctuation | 200 | `0d41efec-4d3a-4bc6-a867-66cd5c026a17` | human | 0.281 |  |
| MF05 | malformed | text is a very long single word | 200 | `82f25c90-67ca-4454-ba5e-f78213e0ac14` | unsure | 0.624 |  |
| MF06 | malformed | text is emoji only | 200 | `df75984c-f626-4202-88be-bbb496966bd7` | ai | 0.773 |  |
| MF07 | malformed | text is right-to-left script | 200 | `78979397-0155-4310-a5de-4e8002dd6b73` | ai | 0.728 |  |
| MF08 | malformed | text is 60,000 characters | 413 | `—` | — | — |  |
| RQ01 | malformed | no text field at all | 400 | `—` | — | — |  |
| RQ02 | malformed | no creator_id | 200 | `854c34e5-d9b4-464a-8aca-f948b0caeda3` | human | 0.245 |  |
| RQ03 | malformed | text is a number | 400 | `—` | — | — |  |
| RQ04 | malformed | text is a list | 400 | `—` | — | — |  |
| RQ05 | malformed | text is null | 400 | `—` | — | — |  |
| RQ06 | malformed | creator_id is an object | 200 | `61eec67e-0c1a-41b8-8920-9d9ac9d388a2` | human | 0.150 |  |
| RQ07 | malformed | body is a JSON array, not an object | 400 | `—` | — | — |  |
| RQ08 | malformed | body is unparseable JSON | 400 | `—` | — | — |  |
| RQ09 | malformed | body is empty | 400 | `—` | — | — |  |
| RQ10 | malformed | body is form-encoded, not JSON | 429 | `—` | — | — |  |
| RQ11 | malformed | body is JSON claiming to be plain text | 429 | `—` | — | — |  |
| RQ12 | malformed | deeply nested JSON | 400 | `—` | — | — |  |
| FL01_01 | flood_same_creator | 20 rapid submissions from one creator | 200 | `7f13b22d-423f-4bfa-89e0-2573dfa1f34a` | human | 0.139 |  |
| FL01_02 | flood_same_creator | 20 rapid submissions from one creator | 200 | `95bca439-d39e-4122-bec4-ac7c55f7d89f` | human | 0.139 |  |
| FL01_03 | flood_same_creator | 20 rapid submissions from one creator | 200 | `b9cd8695-1cb7-40ba-be2f-a1b71a4b3177` | human | 0.139 |  |
| FL01_04 | flood_same_creator | 20 rapid submissions from one creator | 200 | `acb228d6-1568-4b1f-b99d-e7e614c6f547` | human | 0.139 |  |
| FL01_05 | flood_same_creator | 20 rapid submissions from one creator | 200 | `2e8fc024-f976-4fdc-8bdd-9cb5e0fd5265` | human | 0.139 |  |
| FL01_06 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — |  |
| FL01_07 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — |  |
| FL01_08 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — |  |
| FL01_09 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — |  |
| FL01_10 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — |  |
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
  "content_id": "1f48d957-3746-40bd-b8e9-53954c6927ee",
  "creator_id": "attacker_EV01",
  "guess": "human",
  "confidence": 0.3427,
  "model_score": 0.1635,
  "style_score": 0.5218,
  "label": "We think this was probably written by a person. Nothing in it stood out as typical of machine-generated writing. This is an automated best guess, so it can be wrong.",
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
  "content_id": "936bb5f6-f452-4af3-a9d5-49c03e9b3796",
  "creator_id": "attacker_EV02",
  "guess": "unsure",
  "confidence": 0.3737,
  "model_score": 0.5943,
  "style_score": 0.153,
  "label": "We can't tell whether this was written by a person or by AI. Some of it looks like machine writing, but plain, clear writing can look that way too, so this is not a finding that AI wrote it. If you wrote it yourself, you can appeal and your appeal will be recorded and flagged for review.",
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
  "content_id": "8f042da8-9712-47a4-903b-98fbdda278f9",
  "creator_id": "attacker_EV03",
  "guess": "unsure",
  "confidence": 0.5286,
  "model_score": 0.6662,
  "style_score": 0.391,
  "label": "We can't tell whether this was written by a person or by AI. Some of it looks like machine writing, but plain, clear writing can look that way too, so this is not a finding that AI wrote it. If you wrote it yourself, you can appeal and your appeal will be recorded and flagged for review.",
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
  "content_id": "80b7a9ee-5368-44b3-a751-fdb07dfdca3b",
  "creator_id": "attacker_EV04",
  "guess": "unsure",
  "confidence": 0.5693,
  "model_score": 0.6114,
  "style_score": 0.5272,
  "label": "We can't tell whether this was written by a person or by AI. Some of it looks like machine writing, but plain, clear writing can look that way too, so this is not a finding that AI wrote it. If you wrote it yourself, you can appeal and your appeal will be recorded and flagged for review.",
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
  "content_id": "8aa1dd53-24b9-4e0f-b38f-33632e0f2910",
  "creator_id": "attacker_EV05",
  "guess": "human",
  "confidence": 0.3246,
  "model_score": 0.3212,
  "style_score": 0.3281,
  "label": "We think this was probably written by a person. Nothing in it stood out as typical of machine-generated writing. This is an automated best guess, so it can be wrong.",
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
  "content_id": "2c3aec38-2ca9-48d0-ac50-71bac7489b65",
  "creator_id": "attacker_EV06",
  "guess": "unsure",
  "confidence": 0.3831,
  "model_score": 0.5727,
  "style_score": 0.1935,
  "label": "We can't tell whether this was written by a person or by AI. Some of it looks like machine writing, but plain, clear writing can look that way too, so this is not a finding that AI wrote it. If you wrote it yourself, you can appeal and your appeal will be recorded and flagged for review.",
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
  "content_id": "693ce871-3e59-4ce7-989e-970ea9cf8f63",
  "creator_id": "attacker_EV07",
  "guess": "unsure",
  "confidence": 0.5844,
  "model_score": 0.5862,
  "style_score": 0.5826,
  "label": "We can't tell whether this was written by a person or by AI. Some of it looks like machine writing, but plain, clear writing can look that way too, so this is not a finding that AI wrote it. If you wrote it yourself, you can appeal and your appeal will be recorded and flagged for review.",
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
  "content_id": "ec936781-bfd6-4576-94b4-3ede1f9890df",
  "creator_id": "attacker_EV08",
  "guess": "human",
  "confidence": 0.2842,
  "model_score": 0.2452,
  "style_score": 0.3232,
  "label": "We think this was probably written by a person. Nothing in it stood out as typical of machine-generated writing. This is an automated best guess, so it can be wrong.",
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
  "content_id": "6f408ae0-f8a2-4f24-a5f4-99109d596790",
  "creator_id": "attacker_EV09",
  "guess": "unsure",
  "confidence": 0.5183,
  "model_score": 0.7042,
  "style_score": 0.3324,
  "label": "We can't tell whether this was written by a person or by AI. Some of it looks like machine writing, but plain, clear writing can look that way too, so this is not a finding that AI wrote it. If you wrote it yourself, you can appeal and your appeal will be recorded and flagged for review.",
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
  "content_id": "0c68508e-057f-46a0-82ef-5808578ebaca",
  "creator_id": "attacker_EV10",
  "guess": "ai",
  "confidence": 0.7665,
  "model_score": 0.9792,
  "style_score": 0.5538,
  "label": "This has several features that are common in machine-generated writing. That's an automated estimate, not proof, and it can be wrong, especially for plain or very clear writing. If you wrote it yourself, you can appeal and your appeal will be recorded and flagged for review.",
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
  "content_id": "44a26b06-a144-4cff-9d11-8363c2e7d6b2",
  "creator_id": "attacker_FP01",
  "guess": "unsure",
  "confidence": 0.5225,
  "model_score": 0.6175,
  "style_score": 0.4274,
  "label": "We can't tell whether this was written by a person or by AI. Some of it looks like machine writing, but plain, clear writing can look that way too, so this is not a finding that AI wrote it. If you wrote it yourself, you can appeal and your appeal will be recorded and flagged for review.",
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
  "content_id": "b1481e36-45d2-445c-ab89-3e195311dc24",
  "creator_id": "attacker_FP02",
  "guess": "unsure",
  "confidence": 0.6428,
  "model_score": 0.7387,
  "style_score": 0.5469,
  "label": "We can't tell whether this was written by a person or by AI. Some of it looks like machine writing, but plain, clear writing can look that way too, so this is not a finding that AI wrote it. If you wrote it yourself, you can appeal and your appeal will be recorded and flagged for review.",
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
  "content_id": "cbf75b89-8fce-4552-a8d6-fb507b43f4b1",
  "creator_id": "attacker_FP03",
  "guess": "unsure",
  "confidence": 0.6351,
  "model_score": 0.8051,
  "style_score": 0.4652,
  "label": "We can't tell whether this was written by a person or by AI. Some of it looks like machine writing, but plain, clear writing can look that way too, so this is not a finding that AI wrote it. If you wrote it yourself, you can appeal and your appeal will be recorded and flagged for review.",
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
  "content_id": "88ac7942-7ecd-4c04-b682-6178f20b55c6",
  "creator_id": "attacker_FP04",
  "guess": "unsure",
  "confidence": 0.6146,
  "model_score": 0.8329,
  "style_score": 0.3963,
  "label": "We can't tell whether this was written by a person or by AI. Some of it looks like machine writing, but plain, clear writing can look that way too, so this is not a finding that AI wrote it. If you wrote it yourself, you can appeal and your appeal will be recorded and flagged for review.",
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
  "content_id": "337d36a1-dec6-46cc-8485-e411e1a9794f",
  "creator_id": "attacker_FP05",
  "guess": "ai",
  "confidence": 0.7194,
  "model_score": 0.8005,
  "style_score": 0.6383,
  "label": "This has several features that are common in machine-generated writing. That's an automated estimate, not proof, and it can be wrong, especially for plain or very clear writing. If you wrote it yourself, you can appeal and your appeal will be recorded and flagged for review.",
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
  "content_id": "174b72b4-50ee-48de-bba3-ce7a5bcc5b9f",
  "creator_id": "attacker_FP06",
  "guess": "unsure",
  "confidence": 0.6198,
  "model_score": 0.8814,
  "style_score": 0.3581,
  "label": "We can't tell whether this was written by a person or by AI. Some of it looks like machine writing, but plain, clear writing can look that way too, so this is not a finding that AI wrote it. If you wrote it yourself, you can appeal and your appeal will be recorded and flagged for review.",
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
  "content_id": "17429c04-9d2c-4d75-8d64-9e10f117e935",
  "creator_id": "attacker_FP07",
  "guess": "unsure",
  "confidence": 0.635,
  "model_score": 0.8816,
  "style_score": 0.3884,
  "label": "We can't tell whether this was written by a person or by AI. Some of it looks like machine writing, but plain, clear writing can look that way too, so this is not a finding that AI wrote it. If you wrote it yourself, you can appeal and your appeal will be recorded and flagged for review.",
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
  "content_id": "7438f1cf-4d29-4fea-bb13-e79ff3be6583",
  "creator_id": "attacker_FP08",
  "guess": "human",
  "confidence": 0.2758,
  "model_score": 0.3223,
  "style_score": 0.2294,
  "label": "We think this was probably written by a person. Nothing in it stood out as typical of machine-generated writing. This is an automated best guess, so it can be wrong.",
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
  "content_id": "70dc1577-b141-497a-b5d9-67fb96afe0cc",
  "creator_id": "attacker_PI01",
  "guess": "human",
  "confidence": 0.2804,
  "model_score": 0.4625,
  "style_score": 0.0983,
  "label": "We think this was probably written by a person. Nothing in it stood out as typical of machine-generated writing. This is an automated best guess, so it can be wrong.",
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
  "content_id": "42eed533-a99b-4d49-b028-d9dad1065783",
  "creator_id": "attacker_PI02",
  "guess": "human",
  "confidence": 0.1782,
  "model_score": 0.2044,
  "style_score": 0.1519,
  "label": "We think this was probably written by a person. Nothing in it stood out as typical of machine-generated writing. This is an automated best guess, so it can be wrong.",
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
  "content_id": "8a47562d-7003-43f9-8880-de7c29bc84a4",
  "creator_id": "attacker_PI03",
  "guess": "unsure",
  "confidence": 0.4917,
  "model_score": 0.5943,
  "style_score": 0.389,
  "label": "We can't tell whether this was written by a person or by AI. Some of it looks like machine writing, but plain, clear writing can look that way too, so this is not a finding that AI wrote it. If you wrote it yourself, you can appeal and your appeal will be recorded and flagged for review.",
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
  "content_id": "45bf2be1-3061-46fd-93e8-77a216181001",
  "creator_id": "attacker_PI04",
  "guess": "unsure",
  "confidence": 0.4609,
  "model_score": 0.4998,
  "style_score": 0.4221,
  "label": "We can't tell whether this was written by a person or by AI. Some of it looks like machine writing, but plain, clear writing can look that way too, so this is not a finding that AI wrote it. If you wrote it yourself, you can appeal and your appeal will be recorded and flagged for review.",
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
  "content_id": "5cb04de7-c75c-4707-b8d9-e68b5f326aa6",
  "creator_id": "attacker_PI05",
  "guess": "unsure",
  "confidence": 0.5228,
  "model_score": 0.6401,
  "style_score": 0.4054,
  "label": "We can't tell whether this was written by a person or by AI. Some of it looks like machine writing, but plain, clear writing can look that way too, so this is not a finding that AI wrote it. If you wrote it yourself, you can appeal and your appeal will be recorded and flagged for review.",
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
  "content_id": "0a4ed6b5-619b-47de-89f3-9c866a64bab4",
  "creator_id": "attacker_PI06",
  "guess": "unsure",
  "confidence": 0.4843,
  "model_score": 0.5583,
  "style_score": 0.4102,
  "label": "We can't tell whether this was written by a person or by AI. Some of it looks like machine writing, but plain, clear writing can look that way too, so this is not a finding that AI wrote it. If you wrote it yourself, you can appeal and your appeal will be recorded and flagged for review.",
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
  "content_id": "ebefbcf0-30cf-46f4-98bf-62335071ee9c",
  "creator_id": "attacker_MF03",
  "guess": "human",
  "confidence": 0.125,
  "model_score": 0.0,
  "style_score": 0.25,
  "label": "We think this was probably written by a person. Nothing in it stood out as typical of machine-generated writing. This is an automated best guess, so it can be wrong.",
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
  "content_id": "0d41efec-4d3a-4bc6-a867-66cd5c026a17",
  "creator_id": "attacker_MF04",
  "guess": "human",
  "confidence": 0.2806,
  "model_score": 0.0112,
  "style_score": 0.55,
  "label": "We think this was probably written by a person. Nothing in it stood out as typical of machine-generated writing. This is an automated best guess, so it can be wrong.",
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
  "content_id": "82f25c90-67ca-4454-ba5e-f78213e0ac14",
  "creator_id": "attacker_MF05",
  "guess": "unsure",
  "confidence": 0.6238,
  "model_score": 0.9976,
  "style_score": 0.25,
  "label": "We can't tell whether this was written by a person or by AI. Some of it looks like machine writing, but plain, clear writing can look that way too, so this is not a finding that AI wrote it. If you wrote it yourself, you can appeal and your appeal will be recorded and flagged for review.",
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
  "content_id": "df75984c-f626-4202-88be-bbb496966bd7",
  "creator_id": "attacker_MF06",
  "guess": "ai",
  "confidence": 0.7734,
  "model_score": 0.9969,
  "style_score": 0.55,
  "label": "This has several features that are common in machine-generated writing. That's an automated estimate, not proof, and it can be wrong, especially for plain or very clear writing. If you wrote it yourself, you can appeal and your appeal will be recorded and flagged for review.",
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
  "content_id": "78979397-0155-4310-a5de-4e8002dd6b73",
  "creator_id": "attacker_MF07",
  "guess": "ai",
  "confidence": 0.7282,
  "model_score": 0.9064,
  "style_score": 0.55,
  "label": "This has several features that are common in machine-generated writing. That's an automated estimate, not proof, and it can be wrong, especially for plain or very clear writing. If you wrote it yourself, you can appeal and your appeal will be recorded and flagged for review.",
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
  "status": 200,
  "content_id": "854c34e5-d9b4-464a-8aca-f948b0caeda3",
  "creator_id": null,
  "guess": "human",
  "confidence": 0.2447,
  "model_score": 0.2395,
  "style_score": 0.25,
  "label": "We think this was probably written by a person. Nothing in it stood out as typical of machine-generated writing. This is an automated best guess, so it can be wrong.",
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
  "status": 200,
  "content_id": "61eec67e-0c1a-41b8-8920-9d9ac9d388a2",
  "creator_id": {
    "id": "x"
  },
  "guess": "human",
  "confidence": 0.1496,
  "model_score": 0.0492,
  "style_score": 0.25,
  "label": "We think this was probably written by a person. Nothing in it stood out as typical of machine-generated writing. This is an automated best guess, so it can be wrong.",
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
  "status": 429,
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
  "status": 429,
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
  "content_id": "7f13b22d-423f-4bfa-89e0-2573dfa1f34a",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.1394,
  "model_score": 0.0287,
  "style_score": 0.25,
  "label": "We think this was probably written by a person. Nothing in it stood out as typical of machine-generated writing. This is an automated best guess, so it can be wrong.",
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
  "content_id": "95bca439-d39e-4122-bec4-ac7c55f7d89f",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.1394,
  "model_score": 0.0287,
  "style_score": 0.25,
  "label": "We think this was probably written by a person. Nothing in it stood out as typical of machine-generated writing. This is an automated best guess, so it can be wrong.",
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
  "content_id": "b9cd8695-1cb7-40ba-be2f-a1b71a4b3177",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.1394,
  "model_score": 0.0287,
  "style_score": 0.25,
  "label": "We think this was probably written by a person. Nothing in it stood out as typical of machine-generated writing. This is an automated best guess, so it can be wrong.",
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
  "content_id": "acb228d6-1568-4b1f-b99d-e7e614c6f547",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.1394,
  "model_score": 0.0287,
  "style_score": 0.25,
  "label": "We think this was probably written by a person. Nothing in it stood out as typical of machine-generated writing. This is an automated best guess, so it can be wrong.",
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
  "content_id": "2e8fc024-f976-4fdc-8bdd-9cb5e0fd5265",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.1394,
  "model_score": 0.0287,
  "style_score": 0.25,
  "label": "We think this was probably written by a person. Nothing in it stood out as typical of machine-generated writing. This is an automated best guess, so it can be wrong.",
  "error": null,
  "verdict": ""
}
```

### FL01_06 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_06",
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

### FL01_07 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_07",
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

### FL01_08 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_08",
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

### FL01_09 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_09",
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

### FL01_10 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_10",
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
