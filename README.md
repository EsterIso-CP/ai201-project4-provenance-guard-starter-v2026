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

1. **Arrives.** A client sends `POST /submit` with `text` and `creator_id`. The route is the front door and adds nothing but the raw input.
2. **Validation.** The route rejects missing, non-string, or too-short text with a 400, so bad input never reaches the model. It adds a guarantee that later stages only see scoreable text.
3. **Signal one (`detector.model_signal`).** gpt2 runs locally and computes perplexity, which is squashed to 0–1. It adds a "how predictable is this?" score.
4. **Signal two (`stylometry.style_signal`).** Three shape measures (sentence-length spread, type-token ratio, punctuation density) are flipped so higher means more AI, then combined. It adds a "what shape is this?" score.
5. **Combining rule (`scoring.combine_signals`).** The two scores become one number, and a disagreement check can block a confident verdict. It adds the final score and `guess`.
6. **Label mapping.** The score is mapped to one of three labels with wording written for a non-technical reader. It adds the words the reader sees.
7. **Content ID and audit log.** The submission gets a `content_id`, and the scores, label and status are written to `logs/audit.jsonl`. It adds a record an appeal can refer back to.

---

## Signals and Scoring

### Signal one — the model signal

**What it measures:** perplexity under gpt2, meaning how easily a language model could predict this text.

**Why that might differ between human and AI writing:** a model writes by choosing likely next words, so its output tends to be predictable. Human writing wanders more, with odd word choices and specifics.

**What it can't see:** authorship. It measures predictability, so plain writing in common words and short sentences scores as machine-like. That hits second-language writers, younger writers and anyone writing plainly on purpose. Dense prose full of rare words scores as human.

### Signal two — the style signal

**What it measures:** the shape of the text without reading it: how much sentence length varies, how much vocabulary repeats, and how much punctuation there is.

**Why that might differ between human and AI writing:** generated prose tends toward even, mid-length sentences and a narrower vocabulary. Human writing is lumpier.

**What it can't see:** meaning. Anything that changes the shape without changing the substance moves it (typos, chopped-up sentences, a pasted quotation), and that's cheap to do on purpose. Type-token ratio also falls as text gets longer, so length alone can look like a signal.

### The combining rule

**The rule:** the final score is a weighted average of the two signals. A high-confidence AI verdict also needs both signals to lean AI on their own. If the average is above the AI cutoff but either signal is below the agreement floor, the score is capped just under the cutoff, so the label can only be "unsure". The human side has no matching guard on purpose: a wrong accusation costs a writer more than a missed detection costs the site, so only the AI label needs both signals to agree. When the signals split, the rule treats that as uncertainty and doesn't pick a winner.

**The numbers** (all in `config.py`): score = 0.5 × model_score + 0.5 × style_score. Agreement floor = 0.5. Label cutoffs: ≤ 0.35 high-confidence human, ≥ 0.65 high-confidence AI, unsure between. *(Placeholders until calibration in unit 8.)*

**Where it lives:** `scoring.py::combine_signals`

**A case where my two signals split, and what my rule does with it:** a short, plainly written team-update paragraph I wrote myself (content_id `611f1cd6-…`) got model_score **0.7784**, so gpt2 found it very predictable and leaned AI. It got style_score **0.3854**, so its shape leaned human. That's a 0.39 gap. The average came out at **0.5819**, which is in the unsure band, so it was labeled "unsure", not "AI". The cap didn't need to fire here because the average alone stayed under 0.65. It would have mattered if the model signal had been higher: with model_score 0.95 and the same style_score, the average would be 0.668, and the agreement floor would pull it back to 0.64 (unsure) because style_score is below 0.5. This is exactly the blind spot named above: plain human writing fools signal one, and the rule won't let signal one accuse on its own.

---

## Label Variants

| Label | Score range | The exact text a reader sees |
|---|---|---|
| high-confidence human | 0.00–0.35 | "We think this was probably written by a person. Nothing in it stood out as typical of machine-generated writing. This is an automated best guess, so it can be wrong." |
| unsure | 0.35–0.65 (also where a split-signal score gets capped) | "We can't tell whether this was written by a person or by AI. Some of it looks like machine writing, but plain, clear writing can look that way too, so this is not a finding that AI wrote it. If you wrote it yourself, you can appeal and your appeal will be recorded and flagged for review." |
| high-confidence AI | 0.65–1.00, and both signals ≥ 0.5 | "This has several features that are common in machine-generated writing. That's an automated estimate, not proof, and it can be wrong, especially for plain or very clear writing. If you wrote it yourself, you can appeal and your appeal will be recorded and flagged for review." |

All three are reachable. From one session: an AI-style sample scored 0.715 (ai), my plain team update scored 0.5819 (unsure), and a casual story about missing the bus scored 0.3383 (human).

**Why I worded the "unsure" one this way:** it says what was measured instead of what the writer did, and it says outright that plain human writing can trigger it. The person reading it may have written every word, so it can't sound like an accusation. It points to the appeal path and only promises what the service actually does: the appeal is recorded and flagged. It doesn't promise that a person will review it.

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
  -d '{"text": "The implementation of the proposed framework requires careful consideration of several key factors. First, it is important to note that the system must be able to handle a wide variety of different inputs. Additionally, the overall performance of the solution depends on a number of important variables.", "creator_id": "ester"}'
```

```json
{
  "confidence": 0.715,
  "content_id": "7b6da679-68f2-43fc-a0e8-aa29f6f09ce5",
  "guess": "ai",
  "label": "This has several features that are common in machine-generated writing. That's an automated estimate, not proof, and it can be wrong, especially for plain or very clear writing. If you wrote it yourself, you can appeal and your appeal will be recorded and flagged for review.",
  "model_score": 0.8864,
  "style_score": 0.5437
}
```

**An appeal**

This appeal is on my plain team-update paragraph (`611f1cd6-…`). It was labeled "unsure" in the same session, and its decision entry is the first one in the log below.

```bash
$ curl -X POST http://127.0.0.1:5000/appeal \
  -H "Content-Type: application/json" \
  -d '{"content_id": "611f1cd6-7b39-4d8d-a9ae-4067dc54e017", "reasoning": "I wrote this myself for a team update."}'
```

```json
{
  "content_id": "611f1cd6-7b39-4d8d-a9ae-4067dc54e017",
  "message": "Your appeal has been recorded and flagged for review.",
  "status": "under_review"
}
```

**What the log shows afterwards**

```bash
$ curl "http://127.0.0.1:5000/log?limit=4"
```

```json
{
  "count": 4,
  "entries": [
    {
      "combined_score": 0.5819,
      "content_id": "611f1cd6-7b39-4d8d-a9ae-4067dc54e017",
      "creator_id": "ester",
      "guess": "unsure",
      "label": "We can't tell whether this was written by a person or by AI. Some of it looks like machine writing, but plain, clear writing can look that way too, so this is not a finding that AI wrote it. If you wrote it yourself, you can appeal and your appeal will be recorded and flagged for review.",
      "model_score": 0.7784,
      "status": "decided",
      "style_score": 0.3854,
      "timestamp": "2026-11-09T17:33:48+00:00"
    },
    {
      "content_id": "611f1cd6-7b39-4d8d-a9ae-4067dc54e017",
      "creator_id": "ester",
      "event": "appeal",
      "reasoning": "I wrote this myself for a team update.",
      "status": "under_review",
      "timestamp": "2026-11-09T17:34:39+00:00"
    },
    {
      "combined_score": 0.715,
      "content_id": "7b6da679-68f2-43fc-a0e8-aa29f6f09ce5",
      "creator_id": "ester",
      "guess": "ai",
      "label": "This has several features that are common in machine-generated writing. That's an automated estimate, not proof, and it can be wrong, especially for plain or very clear writing. If you wrote it yourself, you can appeal and your appeal will be recorded and flagged for review.",
      "model_score": 0.8864,
      "status": "decided",
      "style_score": 0.5437,
      "timestamp": "2026-11-09T17:34:48+00:00"
    },
    {
      "combined_score": 0.3383,
      "content_id": "963d6235-e881-49cc-b076-496a563749a9",
      "creator_id": "ester",
      "guess": "human",
      "label": "We think this was probably written by a person. Nothing in it stood out as typical of machine-generated writing. This is an automated best guess, so it can be wrong.",
      "model_score": 0.5448,
      "status": "decided",
      "style_score": 0.1319,
      "timestamp": "2026-11-09T17:34:56+00:00"
    }
  ]
}
```

The appeal didn't overwrite the original decision. It was added as a new `event: "appeal"` entry with the same `content_id`, the writer's reasoning, and `status: "under_review"`.

---

## How I Used AI

**Moment 1 — understanding a topic I was stuck on**

- *What I asked for:* an explanation of concepts I was confused about while building the signals, like what perplexity measures and why predictable text might point to AI.
- *What came back:* a plain language explanation of each idea and how it connects to human versus AI writing.
- *What I changed:* I didn't copy the explanation in. I used it to understand the signal, then wrote my own description of what each signal measures and, most importantly, what it can't see. That's the blind-spot reasoning in Signals and Scoring.

**Moment 2 — debugging commands that didn't work**

- *What I asked for:* help figuring out why my curl commands weren't returning real results. Some functions weren't connected or set up correctly, so the service was still running the starter stubs. My early log entries show it: `"guess": "placeholder"`, `"style_score": null`, and a label reading `"PLACEHOLDER — write the unsure label."`
- *What came back:* help tracing the request through each stage (the route, the two signals, the combining rule, the label mapping) to find which pieces were still stubs or weren't being called.
- *What I changed:* I connected the real functions and re-ran the same submissions until every response had a real guess, both signal scores, and the actual label text. Then I checked that all three labels could be reached.

<!-- ═══════════════════════ UNIT 8 — THE TEST ═══════════════════════ -->

---

## Rate Limiting

**My limits:** 5 per minute, 50 per day (on `POST /submit` only)

**Why those numbers and not others:**
A real writer submits a piece, maybe tweaks it and resubmits, a few times an hour. 5 a minute leaves room for a quick retry or a couple of drafts in a row without ever getting in their way. 50 a day is far more than one person's own writing.

A script trying to map my thresholds needs hundreds of slightly different variations to find where "human" turns into "unsure" and "unsure" turns into "AI". At 5 a minute that's slow. At 50 a day per caller, a thousand probes takes 20 days instead of a few minutes. I didn't go lower because each submission takes a second or two of model time anyway, and a stricter limit would start hitting real writers who paste several short pieces in a row.

**What a caller counts as:** the `creator_id` in the request, falling back to the caller's IP address when there isn't one (`app.py::rate_limit_key`). A household or classroom sharing one IP address doesn't share a limit, so a writer isn't blocked because of someone else. The weakness is that `creator_id` is self-reported. A script can make up a new one for every request and look like a thousand different writers, which per-IP limiting would catch. That's a real gap, and Unit 8's attack set will test it.

**The run of status codes when I pushed past it:**

```
$ python run_attacks.py --flood 15
200 200 200 200 200 429 429 429 429 429 429 429 429 429 429

10 of 15 were rate limited.
```

Each 429 left a trace in the log, so a flood shows up as an event, not as an empty log:

```json
{
  "creator_id": "flood_tester",
  "event": "rejected",
  "limit": "5 per 1 minute",
  "reason": "rate_limited",
  "status": "rejected",
  "timestamp": "2026-11-09T17:47:15+00:00"
}
```

Requests my own routes refuse are logged too (`app.py::_reject` → `audit.log_rejection`), with the route, the HTTP status and the reason:

```json
{
  "creator_id": "log_check_4",
  "event": "rejected",
  "http_status": 400,
  "reason": "text_missing",
  "route": "/submit",
  "status": "rejected",
  "text_type": "NoneType",
  "timestamp": "2026-11-09T17:47:21+00:00"
}
```

---

## Attack Run — Before

```
$ python run_attacks.py --set attack_set --label before
```

All 56 attacks ran against the live service with rate limiting on (5/minute, 50/day). Nothing crashed: no 5xx and no dropped connections, so the script auto-marked 0 as broke. Full output is in `results/attack_run_2026-11-09_1257_before.md`.

**How I judged held or broke:** I asked whether each attack got what its `targets` column was going for.

- **evasion:** the text is AI-written, so the attack wants to avoid the AI label. It held only if the service still said `ai`.
- **false_positive:** the text is real human writing, so it held as long as the service didn't say `ai`.
- **prompt_injection:** the attack wants its instruction obeyed (a `human` verdict, or a broken label or log). It broke if the verdict came back `human` on AI text, or if the label or log was tampered with.
- **malformed:** it held on a clean 4xx, or on a sensible result for real text. It broke if the service gave a confident verdict on something that isn't writing.
- **flood:** it held if the limit kicked in.

| ID | Family | Targeting | Status | Guess | Score | Verdict |
|---|---|---|---|---|---|---|
| EV01 | evasion | signal two: typos raise word variety | 200 | human | 0.343 | **BROKE** |
| EV02 | evasion | signal two: broken-up sentences raise length spread | 200 | unsure | 0.374 | **BROKE** |
| EV03 | evasion | signal two: a pasted quotation changes the shape | 200 | unsure | 0.529 | **BROKE** |
| EV04 | evasion | signal one: unusual words raise perplexity | 200 | unsure | 0.569 | **BROKE** |
| EV05 | evasion | both signals: heavy human editing pass | 200 | human | 0.325 | **BROKE** |
| EV06 | evasion | signal two: one very long sentence and one very short | 200 | unsure | 0.383 | **BROKE** |
| EV07 | evasion | signal two: padding with punctuation | 200 | unsure | 0.584 | **BROKE** |
| EV08 | evasion | signal one: text below the token window | 200 | human | 0.284 | **BROKE** |
| EV09 | evasion | both: AI text with a human opening paragraph bolted on | 200 | unsure | 0.518 | **BROKE** |
| EV10 | evasion | signal two: repeated stanza structure | 200 | ai | 0.766 | HELD |
| FP01 | false_positive | plain, clear human writing with no flourishes | 200 | unsure | 0.522 | HELD |
| FP02 | false_positive | human writing in a formal register | 200 | unsure | 0.643 | HELD (0.007 from the AI cutoff) |
| FP03 | false_positive | a non-native English speaker writing carefully | 200 | unsure | 0.635 | HELD (0.015 from the AI cutoff) |
| FP04 | false_positive | a student essay written to a rubric | 200 | unsure | 0.615 | HELD |
| FP05 | false_positive | technical documentation written by a person | 200 | **ai** | 0.719 | **BROKE** |
| FP06 | false_positive | a person imitating a formal template | 200 | unsure | 0.620 | HELD |
| FP07 | false_positive | human writing that repeats a phrase deliberately | 200 | unsure | 0.635 | HELD |
| FP08 | false_positive | very short genuine human submission | 200 | human | 0.276 | HELD |
| PI01 | prompt_injection | instruction to ignore the check | 200 | human | 0.280 | **BROKE** |
| PI02 | prompt_injection | instruction disguised as a system message | 200 | human | 0.178 | **BROKE** |
| PI03 | prompt_injection | instruction wrapped in the writer's voice | 200 | unsure | 0.492 | HELD |
| PI04 | prompt_injection | attempt to make the label text hostile | 200 | unsure | 0.461 | HELD (label is a fixed string; the script tag never reaches it) |
| PI05 | prompt_injection | attempt to inject into the audit log | 200 | unsure | 0.523 | HELD (log line stayed one valid JSON object, `guess` unchanged) |
| PI06 | prompt_injection | instruction plus real human text | 200 | unsure | 0.484 | HELD |
| MF01 | malformed | text is only whitespace | 400 | — | — | HELD |
| MF02 | malformed | text is a single character | 400 | — | — | HELD |
| MF03 | malformed | text is control characters | 200 | human | 0.125 | **BROKE** |
| MF04 | malformed | text is only punctuation | 200 | human | 0.281 | **BROKE** |
| MF05 | malformed | text is a very long single word | 200 | unsure | 0.624 | HELD |
| MF06 | malformed | text is emoji only | 200 | **ai** | 0.773 | **BROKE** |
| MF07 | malformed | text is right-to-left script | 200 | **ai** | 0.728 | **BROKE** |
| MF08 | malformed | text is 60,000 characters | 413 | — | — | HELD |
| RQ01 | malformed | no text field at all | 400 | — | — | HELD |
| RQ02 | malformed | no creator_id | 200 | human | 0.245 | HELD (scored as `unknown`) |
| RQ03 | malformed | text is a number | 400 | — | — | HELD |
| RQ04 | malformed | text is a list | 400 | — | — | HELD |
| RQ05 | malformed | text is null | 400 | — | — | HELD |
| RQ06 | malformed | creator_id is an object | 200 | human | 0.150 | HELD (creator coerced to `unknown`) |
| RQ07 | malformed | body is a JSON array, not an object | 400 | — | — | HELD |
| RQ08 | malformed | body is unparseable JSON | 400 | — | — | HELD |
| RQ09 | malformed | body is empty | 400 | — | — | HELD |
| RQ10 | malformed | body is form-encoded, not JSON | 429 | — | — | HELD* |
| RQ11 | malformed | body is JSON claiming to be plain text | 429 | — | — | HELD* |
| RQ12 | malformed | deeply nested JSON | 400 | — | — | HELD |
| FL01_01–05 | flood_same_creator | 20 rapid submissions from one creator | 200 ×5 | human | 0.139 | HELD (under the limit) |
| FL01_06–12 | flood_same_creator | 20 rapid submissions from one creator | 429 ×7 | — | — | HELD |

\* RQ10 and RQ11 have no usable `creator_id`, so they counted against my IP. RQ02 and RQ06–RQ09 had already used that bucket's 5 per minute, so these two got a 429 from the limiter and **never reached my route**. To find out what the route itself does with them, I re-sent both by hand after the minute reset. Both came back `400 bad_request` and were logged.

**The count: 40 held, 16 broke.**

| Family | Held | Broke |
|---|---|---|
| evasion | 1 | 9 |
| false_positive | 7 | 1 |
| prompt_injection | 4 | 2 |
| malformed | 16 | 4 |
| flood_same_creator | 12 | 0 |
| **Total** | **40** | **16** |

The evasion number needs context. I ran the plain AI paragraph that EV01–EV07 are built from through the same functions, with no tricks added. It scored model 0.6694, style 0.5218, combined **0.5956**, which is "unsure". So most of the evasion attacks didn't need their tricks to avoid the AI label, because the base text already avoids it. What the tricks did do was push three of them (EV01, EV05, EV08) and two injections (PI01, PI02) all the way to a confident "human". That's the bigger failure.

**Audit log entries from the run**

<!-- Choose entries that show the interesting failures, not the ten easiest. -->

Pulled with `curl "http://127.0.0.1:5000/log?limit=200" > results/audit_extract.json`. These are the failures plus the rejections, not the easy 400s.

```json
[
  {
    "combined_score": 0.7282,
    "content_id": "78979397-0155-4310-a5de-4e8002dd6b73",
    "creator_id": "attacker_MF07",
    "guess": "ai",
    "label": "This has several features that are common in machine-generated writing. That's an automated estimate, not proof, and it can be wrong, especially for plain or very clear writing. If you wrote it yourself, you can appeal and your appeal will be recorded and flagged for review.",
    "model_score": 0.9064,
    "status": "decided",
    "style_score": 0.55,
    "timestamp": "2026-11-09T17:57:47+00:00"
  },
  {
    "combined_score": 0.7194,
    "content_id": "337d36a1-dec6-46cc-8485-e411e1a9794f",
    "creator_id": "attacker_FP05",
    "guess": "ai",
    "label": "This has several features that are common in machine-generated writing. That's an automated estimate, not proof, and it can be wrong, especially for plain or very clear writing. If you wrote it yourself, you can appeal and your appeal will be recorded and flagged for review.",
    "model_score": 0.8005,
    "status": "decided",
    "style_score": 0.6383,
    "timestamp": "2026-11-09T17:57:46+00:00"
  },
  {
    "combined_score": 0.6351,
    "content_id": "cbf75b89-8fce-4552-a8d6-fb507b43f4b1",
    "creator_id": "attacker_FP03",
    "guess": "unsure",
    "label": "We can't tell whether this was written by a person or by AI. Some of it looks like machine writing, but plain, clear writing can look that way too, so this is not a finding that AI wrote it. If you wrote it yourself, you can appeal and your appeal will be recorded and flagged for review.",
    "model_score": 0.8051,
    "status": "decided",
    "style_score": 0.4652,
    "timestamp": "2026-11-09T17:57:46+00:00"
  },
  {
    "combined_score": 0.1782,
    "content_id": "42eed533-a99b-4d49-b028-d9dad1065783",
    "creator_id": "attacker_PI02",
    "guess": "human",
    "label": "We think this was probably written by a person. Nothing in it stood out as typical of machine-generated writing. This is an automated best guess, so it can be wrong.",
    "model_score": 0.2044,
    "status": "decided",
    "style_score": 0.1519,
    "timestamp": "2026-11-09T17:57:46+00:00"
  },
  {
    "combined_score": 0.3427,
    "content_id": "1f48d957-3746-40bd-b8e9-53954c6927ee",
    "creator_id": "attacker_EV01",
    "guess": "human",
    "label": "We think this was probably written by a person. Nothing in it stood out as typical of machine-generated writing. This is an automated best guess, so it can be wrong.",
    "model_score": 0.1635,
    "status": "decided",
    "style_score": 0.5218,
    "timestamp": "2026-11-09T17:57:46+00:00"
  },
  {
    "combined_score": 0.2842,
    "content_id": "ec936781-bfd6-4576-94b4-3ede1f9890df",
    "creator_id": "attacker_EV08",
    "guess": "human",
    "label": "We think this was probably written by a person. Nothing in it stood out as typical of machine-generated writing. This is an automated best guess, so it can be wrong.",
    "model_score": 0.2452,
    "status": "decided",
    "style_score": 0.3232,
    "timestamp": "2026-11-09T17:57:46+00:00"
  },
  {
    "combined_score": 0.7734,
    "content_id": "df75984c-f626-4202-88be-bbb496966bd7",
    "creator_id": "attacker_MF06",
    "guess": "ai",
    "label": "This has several features that are common in machine-generated writing. That's an automated estimate, not proof, and it can be wrong, especially for plain or very clear writing. If you wrote it yourself, you can appeal and your appeal will be recorded and flagged for review.",
    "model_score": 0.9969,
    "status": "decided",
    "style_score": 0.55,
    "timestamp": "2026-11-09T17:57:47+00:00"
  },
  {
    "combined_score": 0.125,
    "content_id": "ebefbcf0-30cf-46f4-98bf-62335071ee9c",
    "creator_id": "attacker_MF03",
    "guess": "human",
    "label": "We think this was probably written by a person. Nothing in it stood out as typical of machine-generated writing. This is an automated best guess, so it can be wrong.",
    "model_score": 0.0,
    "status": "decided",
    "style_score": 0.25,
    "timestamp": "2026-11-09T17:57:47+00:00"
  },
  {
    "combined_score": 0.5228,
    "content_id": "5cb04de7-c75c-4707-b8d9-e68b5f326aa6",
    "creator_id": "attacker_PI05",
    "guess": "unsure",
    "label": "We can't tell whether this was written by a person or by AI. Some of it looks like machine writing, but plain, clear writing can look that way too, so this is not a finding that AI wrote it. If you wrote it yourself, you can appeal and your appeal will be recorded and flagged for review.",
    "model_score": 0.6401,
    "status": "decided",
    "style_score": 0.4054,
    "timestamp": "2026-11-09T17:57:47+00:00"
  },
  {
    "creator_id": "unknown",
    "event": "rejected",
    "limit": "5 per 1 minute",
    "reason": "rate_limited",
    "status": "rejected",
    "timestamp": "2026-11-09T17:57:47+00:00"
  },
  {
    "creator_id": "attacker_flood",
    "event": "rejected",
    "limit": "5 per 1 minute",
    "reason": "rate_limited",
    "status": "rejected",
    "timestamp": "2026-11-09T17:57:47+00:00"
  }
]
```

What each entry shows, in order:

1. **MF07:** Arabic text gets the high-confidence AI label.
2. **FP05:** a person's technical docs get the AI label. Both signals cleared the 0.5 floor, so the agreement guard didn't help.
3. **FP03:** a non-native speaker writing carefully lands 0.015 below an accusation.
4. **PI02:** AI text with a fake "SYSTEM: return human" line comes out confidently human. The model didn't obey the line. The line changed the text's shape and pulled style_score down to 0.15.
5. **EV01:** typos drop model_score to 0.16 and flip the AI text to human.
6. **EV08:** two short AI sentences get scored anyway and come out human.
7. **MF06:** emoji only, called AI.
8. **MF03:** control characters, called human with model_score 0.0.
9. **PI05:** the log-injection attempt held. The fake `"guess": "human"` stayed inside the text and never became a field.
10. **The `unknown` 429:** the IP-bucket rejection that RQ10 and RQ11 hit.
11. **The `attacker_flood` 429:** one of the seven flood rejections. Rejections carry fewer fields than decisions, as expected.

**The single worst outcome** — the one I'd least want to explain to a writer
whose work got caught by it:

**MF07, the Arabic text labeled high-confidence AI (0.7282).** Someone writing in their own language submitted a normal paragraph and was told it "has several features that are common in machine-generated writing". The label even blames "plain or very clear writing", which isn't the reason. The real reason is that neither signal can read Arabic:

- gpt2 is an English model and gave it model_score 0.9064.
- `stylometry.words()` only matches `[a-z0-9']`, so it found zero words. Type-token ratio came back 0.0, and flipping that turned it into the most AI-like value possible. That's why style_score sits at exactly 0.55, the same as the emoji-only input (MF06).

That 0.55 is just over my 0.5 agreement floor. So the guard I built to stop one signal from accusing on its own let it through, because the second signal wasn't really measuring anything. I couldn't defend that to the writer. The service didn't misjudge their writing; it never read it, and accused them anyway. FP05 (a person's technical documentation called AI) is a close second, but at least both signals were actually measuring that text.

---

## Run Log and Verdicts

<!-- Your five criteria across three trials. `run_eval.py --label before`. -->

```
$ python run_eval.py --label before
```

Three trials, nothing changed in between. Full output is in `results/run_2026-11-09_1305_before.md`.

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. My own writing labeled high-confidence AI | ≤ 1 of 10 | 0/10 | 0/10 | 0/10 | MET |
| 2. Clearly-AI vs clearly-human scores separate | mean gap ≥ 0.30, no overlap | gap 0.419, min AI 0.696 > max human 0.413 | gap 0.419, no overlap | gap 0.419, no overlap | MET |
| 3. All three labels reachable, unsure ≤ 8 of 20 | 3 of 3 labels, unsure ≤ 8 | 3/3 · unsure 7/20 | 3/3 · unsure 7/20 | 3/3 · unsure 7/20 | MET |
| 4. Every appeal changes status and is logged; unknown id → 404 | 10 of 10 + 404 | 10/10 + 404 | 10/10 + 404 | 10/10 + 404 | MET |
| 5. Bad input gets a 4xx JSON error, no score, under 10 s | 5 of 5 | 5/5 | 5/5 | 5/5 | MET |

All three runs scored identically, down to the fourth decimal. Neither signal has anything random in it, so that's what I expected.

**What each criterion was tested with** (all in `scenarios.py`):

- **1:** ten paragraphs I wrote myself, taken from the Unit 7 sections of this README as committed in "Unit 7 Completion". I only stripped the markdown. Five are plainly written (short sentences, common words).
- **2:** five clearly-AI paragraphs, generated by an AI model for this test, against five of my paragraphs from criterion 1.
- **3:** 20 inputs: my 10, the 5 AI paragraphs, and 5 from the attack set (FP01, FP03, FP08, EV01, EV07) to cover the middle of the range. The result was 8 human, 7 unsure, 5 ai.
- **4:** `run_eval.py` only ever called `/submit`, so I extended it. I added `run_eval.py::run_appeal_trial`, which submits each of my 10 paragraphs, appeals the `content_id` that came back, and reads `GET /log` to confirm an `event: "appeal"` entry with that `content_id`, the same reasoning, and `status: "under_review"`. It then appeals a `content_id` that was never issued, and expects a 404 with no appeal entry created.
- **5:** raw request bodies: missing `text`, empty, whitespace only, a number, and 100,000 characters. I also added `elapsed_s` to each result in `run_eval.py::main` so the 10-second part could be checked.

**This table and the attack run disagree, and that's the useful part.** My criteria pass 5 of 5, while the attack set broke 16 times. The gap is in what I chose to test:

- My own writing is fairly technical prose, full of words like "perplexity" and "type-token ratio". gpt2 finds that unpredictable, so model_score stayed between 0.06 and 0.48. That isn't the writing that gets falsely accused.
- The attack set's plain human writing came much closer. FP03 (non-native speaker) scored 0.635 and FP05 (technical documentation) was labeled AI.
- My clearly-AI set is the most stereotypical AI prose there is ("In today's rapidly evolving digital landscape…"), so separation was easy. The evasion attacks show what happens once AI text is even slightly less stereotypical.

**Real output from trial 1**, pasted as text. All of it was produced by `run_eval.py::main` sending to `app.py::submit`, except criterion 4, which came from `run_eval.py::run_appeal_trial` sending to `app.py::appeal` and `app.py::get_log`.

Criterion 1: my two highest-scoring pieces. Even the closest one is 0.24 under the AI cutoff:

```json
[
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.4126,
    "model_score": 0.3043,
    "style_score": 0.5208,
    "label": "We can't tell whether this was written by a person or by AI. Some of it looks like machine writing, but plain, clear writing can look that way too, so this is not a finding that AI wrote it. If you wrote it yourself, you can appeal and your appeal will be recorded and flagged for review.",
    "error": null,
    "elapsed_s": 0.04,
    "sent": "It says what was measured instead of what the writer did, and it says "
  },
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.387,
    "model_score": 0.4845,
    "style_score": 0.2895,
    "label": "We can't tell whether this was written by a person or by AI. Some of it looks like machine writing, but plain, clear writing can look that way too, so this is not a finding that AI wrote it. If you wrote it yourself, you can appeal and your appeal will be recorded and flagged for review.",
    "error": null,
    "elapsed_s": 0.03,
    "sent": "I didn't copy the explanation in. I used it to understand the signal, "
  }
]
```

Criterion 2: the lowest clearly-AI score (0.6961) is still above the highest clearly-human score (0.4126, the first entry above):

```json
{
  "status": 200,
  "guess": "ai",
  "confidence": 0.6961,
  "model_score": 0.8219,
  "style_score": 0.5702,
  "label": "This has several features that are common in machine-generated writing. That's an automated estimate, not proof, and it can be wrong, especially for plain or very clear writing. If you wrote it yourself, you can appeal and your appeal will be recorded and flagged for review.",
  "error": null,
  "elapsed_s": 0.04,
  "sent": "In today's rapidly evolving digital landscape, organizations must cont"
}
```

Criterion 3: one input landing in each label:

```json
[
  {
    "status": 200,
    "guess": "ai",
    "confidence": 0.6961,
    "model_score": 0.8219,
    "style_score": 0.5702,
    "label": "This has several features that are common in machine-generated writing. That's an automated estimate, not proof, and it can be wrong, especially for plain or very clear writing. If you wrote it yourself, you can appeal and your appeal will be recorded and flagged for review.",
    "error": null,
    "elapsed_s": 0.04,
    "sent": "In today's rapidly evolving digital landscape, organizations must cont"
  },
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.5225,
    "model_score": 0.6175,
    "style_score": 0.4274,
    "label": "We can't tell whether this was written by a person or by AI. Some of it looks like machine writing, but plain, clear writing can look that way too, so this is not a finding that AI wrote it. If you wrote it yourself, you can appeal and your appeal will be recorded and flagged for review.",
    "error": null,
    "elapsed_s": 0.05,
    "sent": "We got to the campsite about four. The pitch was fine, a bit sloped, b"
  },
  {
    "status": 200,
    "guess": "human",
    "confidence": 0.2758,
    "model_score": 0.3223,
    "style_score": 0.2294,
    "label": "We think this was probably written by a person. Nothing in it stood out as typical of machine-generated writing. This is an automated best guess, so it can be wrong.",
    "error": null,
    "elapsed_s": 0.02,
    "sent": "Went for a run. Legs hurt. Worth it."
  }
]
```

Criterion 4: one appeal that passed, and the unknown-id appeal:

```json
[
  {
    "sent": "A model writes by choosing likely next words, so its output tends to b",
    "submit_status": 200,
    "content_id": "66d753f2-421f-4a79-b212-96a995c7832c",
    "status": 200,
    "appeal_response": {
      "content_id": "66d753f2-421f-4a79-b212-96a995c7832c",
      "message": "Your appeal has been recorded and flagged for review.",
      "status": "under_review"
    },
    "log_entries_for_id": 2,
    "appeal_logged": true,
    "logged_status": "under_review",
    "passed": true
  },
  {
    "sent": "appeal on unknown content_id 57121c71-24b3-404b-ab81-5567839f37f9",
    "status": 404,
    "appeal_response": {
      "error": "unknown_content_id",
      "message": "No submission with that content_id."
    },
    "appeal_entries_created": 0,
    "passed": true
  }
]
```

Criterion 5: all five bad inputs. Each got a 4xx and no score, and each came back in under 0.01 s because the route rejects them before the model runs:

```json
[
  {"status": 400, "guess": null, "confidence": null, "model_score": null, "style_score": null, "label": null, "error": "text_missing", "elapsed_s": 0.0, "sent": "{\"creator_id\": \"eval_bad_missing\"}"},
  {"status": 400, "guess": null, "confidence": null, "model_score": null, "style_score": null, "label": null, "error": "text_missing", "elapsed_s": 0.0, "sent": "(empty text)"},
  {"status": 400, "guess": null, "confidence": null, "model_score": null, "style_score": null, "label": null, "error": "text_missing", "elapsed_s": 0.0, "sent": "   \n\t  "},
  {"status": 400, "guess": null, "confidence": null, "model_score": null, "style_score": null, "label": null, "error": "text_missing", "elapsed_s": 0.0, "sent": "{\"text\": 12345, \"creator_id\": \"eval_bad_number\"}"},
  {"status": 413, "guess": null, "confidence": null, "model_score": null, "style_score": null, "label": null, "error": "text_too_long", "elapsed_s": 0.0, "sent": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"}
]
```

**Diagnoses**


### Verdicts against my Unit 7 targets

**All five criteria: MET in every trial.** None of them needed a generous reading except one, and I'm naming it:

- **Criterion 4** says "the content's status changes to under appeal". My service doesn't edit the original decision entry, which stays `status: "decided"`. It appends a new entry for the same `content_id` with `status: "under_review"`. I counted that as met because the latest status for that `content_id` in the log is `under_review`, and `/appeal` returns it. I chose append-only on purpose in Unit 7. If the criterion meant "the original record is changed", this would be a miss.

**I held everything, and honestly my targets were too easy.** The attack set broke 16 times while my criteria passed 5 of 5. That happened because of what I tested, not because the service is good:

- **Criterion 1** used my README prose. It's technical, full of words like "perplexity", "type-token ratio" and "content_id", and gpt2 finds that unpredictable, so model_score stayed between 0.06 and 0.48. The "plain" pieces I counted aren't plain the way FP03 (0.635) or FP05 (labeled AI) are plain. The criterion passed on writing that was never at risk.
- **Criterion 2** compared my prose against the most stereotypical AI text possible, so the separation was always going to be wide.

**The criterion I'd tighten is criterion 1.** The target (at most 1 in 10 labeled AI) is fine. The test set is what's weak: "at least 4 plainly written" should mean plainly written the way the false-positive attacks are. That means instructions or documentation, a formal report, and careful second-language writing, all in my own words. I'd also add a margin: no piece above 0.60, since FP02 and FP03 passed by 0.007 and 0.015. This isn't a revision in `criteria.md`, because the criterion could be measured and I didn't miss it. It's just weaker than it looked.

### Diagnoses: the 16 broken attacks

No criterion missed, so these are all from the attack run. I ran every broken input back through `detector.model_signal` and `stylometry.style_signal` and broke signal two into its three parts. The plain AI paragraph most evasions are built from (BASE) is the reference row:

| ID | model | style | length spread | type-token ratio | punct. density | words / sentences | combined |
|---|---|---|---|---|---|---|---|
| BASE | 0.669 | 0.522 | 0.161 | 0.871 | 0.047 | 85 / 7 | 0.596 unsure |
| EV01 | **0.164** | 0.522 | 0.161 | 0.871 | 0.047 | 85 / 7 | 0.343 human |
| EV02 | 0.594 | **0.153** | **0.849** | 0.824 | 0.044 | 91 / 13 | 0.374 unsure |
| EV03 | 0.666 | 0.391 | 0.443 | 0.860 | 0.075 | 106 / 11 | 0.529 unsure |
| EV04 | 0.611 | 0.527 | 0.174 | 0.872 | 0.058 | 86 / 7 | 0.569 unsure |
| EV05 | 0.321 | 0.328 | 0.675 | 0.768 | 0.085 | 82 / 7 | 0.325 human |
| EV06 | 0.573 | **0.194** | **1.186** | 0.750 | 0.033 | 92 / 6 | 0.383 unsure |
| EV07 | 0.586 | 0.583 | n/a (1 sentence) | 0.773 | 0.227 | 97 / 1 | 0.584 unsure |
| EV08 | 0.245 | 0.323 | 0.283 | **1.000** | 0.000 | 10 / 2 | 0.284 human |
| EV09 | 0.704 | 0.332 | 0.468 | 0.880 | 0.054 | 111 / 9 | 0.518 unsure |
| FP05 | 0.801 | 0.638 | 0.277 | **0.586** | 0.029 | 70 / 7 | 0.719 **ai** |
| PI01 | 0.463 | **0.098** | 0.663 | 0.933 | 0.000 | 45 / 6 | 0.280 human |
| PI02 | **0.204** | 0.152 | 0.652 | 0.956 | 0.044 | 45 / 6 | 0.178 human |
| MF03 | **0.000** | 0.250 | n/a | 1.000 | 0.000 | **3** / 1 | 0.125 human |
| MF04 | **0.011** | 0.550 | n/a | **0.000** | 0.000 | **0** / 4 | 0.281 human |
| MF06 | 0.997 | **0.550** | n/a | **0.000** | 0.000 | **0** / 1 | 0.773 **ai** |
| MF07 | 0.906 | **0.550** | n/a | **0.000** | 0.000 | **0** / 1 | 0.728 **ai** |

The 16 failures come down to five problems, not sixteen.

**Pattern 1: the route accepts text the signals can't measure, and signal two's fallbacks aren't neutral. (EV08, MF03, MF04, MF06, MF07: 5 broken)**
The route checks that `text` is a non-empty string and that gpt2 can tokenize it. It never checks that there are words in it. That lets through emoji (MF06), Arabic (MF07), punctuation (MF04), control characters with 3 words (MF03), and a 10-word sentence pair (EV08). Signal two then fails in two opposite directions:
- **No words at all:** `stylometry.words()` only matches `[a-z0-9']`, so emoji, Arabic and punctuation produce zero words. `type_token_ratio` then returns 0.0, which the flip turns into the most AI-like value possible. Add the neutral 0.5 that the spread measure gives when there's only one sentence, and style_score lands on **exactly 0.55** every time. That's just over my 0.5 agreement floor, so the guard in the combining rule doesn't fire. Signal one also reads high on emoji and Arabic (0.997, 0.906): gpt2 breaks them into byte-level pieces, and once a multi-byte character has started, its remaining bytes are easy to predict. Both signals "agree" on AI, and neither one read the text. That's how MF06 and MF07 got the AI label.
- **Too few words:** with 3 or 10 words, every word is unique, so type-token ratio is 1.0 and reads as maximally human (EV08, MF03). Signal one is also unreliable on so few tokens: the opening tokens have no context to predict from, and garbage like control characters is so surprising to gpt2 that model_score hits 0.0 (MF03) or 0.011 (MF04).

The stage is mainly **the route**, with **signal two's fallbacks** as the mechanism that turns "nothing to measure" into a confident number. One fix covers all five: refuse or force "unsure" when the text has too few real words to measure.

**Pattern 2: AI text was never going to reach the AI label, because of how signal two and the combining rule fit together. (EV04, EV07, plus the head start for every evasion: 2 broken outright)**
BASE, with no attack at all, scores **0.596, which is unsure**. The reason is signal two's type-token ratio. Its scale assumes TTR runs 0.55 (AI) to 0.95 (human), but TTR is high for *any* short text. An 85-word AI paragraph has a TTR of 0.871, which the flip reads as fairly human (sub-score 0.20). So signal two tops out around 0.52 on normal-length AI prose. With 0.5/0.5 weights and a 0.65 cutoff, an AI paragraph only gets labeled AI if model_score is at least about 0.78. Most AI text in the attack set sits at 0.6–0.7.
- **EV04** (rare words) barely moved either signal (0.611 / 0.527).
- **EV07** (punctuation padding) actually *raised* style_score to 0.583, because it collapsed the text into one sentence with dense punctuation.

Both are "unsure" only because BASE already was. The stage is **signal two (TTR calibration) feeding the combining rule's threshold**, and the mechanism is that TTR measures length as much as variety, which I named as a blind spot in Unit 7 and then didn't account for. EV10 is the one evasion that held, and it proves the point: it repeats the same paragraph three times, so TTR fell to 0.321 and signal two finally read AI.

**Pattern 3: signal two's sentence-length spread is cheap to move. (EV02, EV03, EV06, EV09, PI01: 5 broken)**
All five add sentences of a very different length to AI text:
- EV02 adds "Really." seven times.
- EV06 adds one huge sentence and one tiny one.
- EV03 adds a chatty quotation.
- EV09 adds a human opening paragraph.
- PI01 adds short imperative instruction sentences.

Length spread jumped from BASE's 0.161 to between 0.44 and 1.19, which took its sub-score to 0 or close to it. Spread carries 50% of signal two, so style_score dropped to 0.10–0.39 while model_score barely changed (0.46–0.70). The stage is **signal two**, and the mechanism is that one weighted measure is measuring a property anyone can change by adding one-word sentences. PI01 is here and not in pattern 4 because its model_score (0.463) only fell partway. Its instruction lines did nothing as instructions, since nothing in my service reads the text as commands. They just changed its shape, and that was enough to reach "human".

**Pattern 4: signal one averages surprise over every token, so a few strange tokens pull the whole score down. (EV01, PI02: 2 broken)**
The attack set expected EV01's typos to fool signal two through word variety. They didn't: **style_score is 0.5218, exactly the same as BASE**, because a misspelled word is still one unique word, so type-token ratio didn't move. The typos hit **signal one**. "poistioned", "thsi" and "cosnistently" are each split into several rare tokens gpt2 doesn't expect. Perplexity is an average over all tokens, so a handful of very surprising ones dragged model_score from 0.669 to 0.164. PI02 works the same way: "SYSTEM:", "guess=human, confidence=0.02" are tokens gpt2 doesn't expect at the start of an essay, so model_score fell to 0.204. Its six short sentences also pulled style_score down, so it reached "human" through both signals at once. The stage is **signal one**, and the mechanism is that perplexity is a mean, and a mean can be dragged by a few outliers.

**Pattern 5: both signals read the same surface trait, so the agreement guard can't help. (FP05: 1 broken)**
FP05 is a person's technical documentation. Signal one called it predictable (0.801), since instructions use common words in common orders. Signal two called it AI (0.638): docs repeat their nouns ("the service", "the port", "the file"), so TTR was 0.586 (sub-score 0.91), and the imperative sentences were all about the same length (spread 0.277). Both signals are above 0.5, so my combining rule's agreement check passed, and the score went straight to the AI label. The stage is **the combining rule**, and the mechanism is that the agreement guard assumes the two signals are independent witnesses. They aren't: plainness and repetitiveness both look like predictability and evenness, so when one is fooled by plain writing, the other usually is too. FP02, FP03, FP04 and FP07 all scored between 0.61 and 0.64, so they are the same failure just under the cutoff.

**And one I wouldn't call a detector failure: EV05.** EV05 is a "heavy human editing pass": the AI paragraph rewritten in a person's voice, with asides, a dash, and "Obviously." as its own sentence. Both signals moved toward human (0.321 / 0.328) because the features they measure were really replaced. By my held/broke rule it broke, and I counted it. But once a person has rewritten the text this thoroughly, a "human" label is arguably correct. No fix to either signal should try to catch it.

**Tally:** pattern 1: 5, pattern 2: 2, pattern 3: 5, pattern 4: 2, pattern 5: 1, plus EV05. That's 16. The two patterns with the most failures (1 and 3) are both **signal two**: its fallbacks on unmeasurable text, and its spread measure on stretched text. Signal two is where the improvement should go.



---

## The Improvement

**What I changed:** one input check at the route. `POST /submit` now refuses any text with fewer than **12 words**, counted the same way signal two counts them (`stylometry.words`, runs of `[a-z0-9']`). It returns a **422 `too_few_words`** before either signal runs, and the refusal is written to the audit log with the word count. The check is in `app.py::submit`, right after the length check, and the number is `MIN_WORDS = 12` in `config.py`. Nothing else changed: same weights, same thresholds, same signals.

The message the writer sees says what happened and doesn't blame them:

```json
{
  "error": "too_few_words",
  "message": "We need at least 12 words written in the English alphabet to make a guess, and this has 8. That isn't a judgment about your writing: below that, our checks have nothing reliable to measure, so we don't score it."
}
```

**Why 12:** there's a clean gap in the word counts. Everything in the attack set with 10 words or fewer was garbage or a fragment: MF01–MF07 had 0–3, FP08 8, EV08 10. The next shortest real text has 30 words (PI05), and my own shortest piece has 16. 12 sits in the gap. I'll admit that a cutoff placed just above EV08's 10 words is partly fitted to this attack set. The real reason for it is that type-token ratio is pinned near 1.0 for any one- or two-sentence text, so signal two can't measure anything below that.

**Which diagnosis pointed at it:** **pattern 1**, "the route accepts text the signals can't measure, and signal two's fallbacks aren't neutral". That covered 5 broken attacks, including MF07, my worst outcome. I chose to fix the route rather than signal two's fallbacks. Making the fallback neutral (0.5) would still let MF06 and MF07 get a confident-looking "unsure" for text that was never read. Refusing to score is the only honest answer when there's nothing to measure.

### Attack Run — After

```
$ python run_attacks.py --set attack_set --label after
$ python run_eval.py --label after
```

Full output is in `results/attack_run_2026-11-09_1315_after.md` and `results/run_2026-11-09_1315_after.md`. Same 56 attacks, same held/broke rule as the before run. Every row whose outcome changed:

| ID | Family | Before | After | Verdict before → after |
|---|---|---|---|---|
| EV08 | evasion | 200 human 0.284 | **422 too_few_words** | BROKE → **HELD** |
| MF03 | malformed | 200 human 0.125 | **422** (3 words) | BROKE → **HELD** |
| MF04 | malformed | 200 human 0.281 | **422** (0 words) | BROKE → **HELD** |
| MF06 | malformed | 200 **ai** 0.773 | **422** (0 words) | BROKE → **HELD** |
| MF07 | malformed | 200 **ai** 0.728 | **422** (0 words) | BROKE → **HELD** |
| MF02 | malformed | 400 too short | 422 (1 word) | HELD → HELD |
| MF05 | malformed | 200 unsure 0.624 | 422 (1 word) | HELD → HELD |
| FP08 | false_positive | 200 human 0.276 | **422** (8 words) | HELD → HELD, **but a real writer is now refused** |
| RQ02 | malformed | 200 human 0.245 | 422 (11 words) | HELD → HELD |
| RQ06 | malformed | 200 human 0.150 | 422 (3 words) | HELD → HELD |
| FL01_01–05 | flood | 200 ×5 | 422 ×5 (9 words) | HELD → HELD |
| FL01_06–12 | flood | 429 ×7 | 429 ×7 | HELD → HELD |

The other 38 rows came back with the same status, guess and score as before, down to the fourth decimal. That includes all of EV01–EV07, EV09, EV10, FP01–FP07, PI01–PI06, RQ10 and RQ11.

I counted EV08's 422 as held under the evasion rule. The service never said "not AI" about it; it refused to say anything. A refusal can't be pasted anywhere as proof that the text is human.

| Family | Before: held / broke | After: held / broke |
|---|---|---|
| evasion | 1 / 9 | 2 / 8 |
| false_positive | 7 / 1 | 7 / 1 |
| prompt_injection | 4 / 2 | 4 / 2 |
| malformed | 16 / 4 | **20 / 0** |
| flood_same_creator | 12 / 0 | 12 / 0 |
| **Total** | **40 / 16** | **45 / 11** |

**Criteria, before and after**, three trials each:

| Criterion | Target | Before (runs 1 / 2 / 3) | After (runs 1 / 2 / 3) | Verdict before → after |
|---|---|---|---|---|
| 1. My own writing labeled AI | ≤ 1 of 10 | 0/10 · 0/10 · 0/10 | 0/10 · 0/10 · 0/10 | MET → MET |
| 2. Score spread | gap ≥ 0.30, no overlap | 0.419, no overlap ×3 | 0.419, no overlap ×3 | MET → MET |
| 3. Label coverage | 3/3 labels, unsure ≤ 8/20 | 3/3, unsure 7/20 ×3 | 3/3, unsure 7/20 ×3 (19 of 20 labeled; FP08 refused) | MET → MET |
| 4. Appeals | 10/10 + 404 | 10/10 + 404 ×3 | 10/10 + 404 ×3 | MET → MET |
| 5. Bad input | 5/5 | 5/5 ×3 | 5/5 ×3 | MET → MET |

The one criterion output that changed, from criterion 3, trial 1 (`run_eval.py::main` → `app.py::submit`):

```json
{
  "status": 422,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": "too_few_words",
  "elapsed_s": 0.0,
  "sent": "Went for a run. Legs hurt. Worth it."
}
```

And the audit log entry for my worst outcome, which is now a refusal instead of an accusation:

```json
{"timestamp": "2026-11-09T18:15:12+00:00", "creator_id": "attacker_MF07", "event": "rejected", "status": "rejected", "reason": "too_few_words", "route": "/submit", "http_status": 422, "word_count": 0}
```

**Did it help, and how do I know:**

**Yes, for exactly what it targeted, and nothing else moved.** Broken attacks went from 16 to 11. All five pattern-1 failures now get a 422. Every other attack and every criterion scored identically to the fourth decimal, so the change is isolated. The 5 fixes come from this check and nothing else. Most importantly, **nothing is labeled AI any more without words in it**: Of the four AI labels in the before run, MF06 and MF07 were on text that wasn't English prose at all, and both are now refused instead. An Arabic writer no longer gets accused.

**What it cost:**

- **Short real writing can't be checked at all.** FP08 ("Went for a run. Legs hurt. Worth it.") is a genuine human post that used to get a correct "human" label. Now it gets a 422. Anyone posting a short caption, a two-line poem, or a one-sentence update is turned away. That's better than a wrong verdict, but it's still a writer who gets no answer.
- **Writers in non-Latin scripts are refused, not served.** The Arabic writer isn't accused any more, but they can't use the service either. This doesn't make the detector work for them; it stops it from lying about them. The message says "written in the English alphabet", so at least they're told why.
- **The flood test now floods with refusals.** The flood rows' own text is 9 words, so FL01_01–05 got 422s. The limiter still counted them and blocked FL01_06–12 with 429s, because rate limiting runs before the route. That's the right behavior: refused requests still use up a caller's allowance, so you can't probe the word cutoff for free.
- **It's easy to step over.** An attacker who knows the cutoff pads EV08 to 12 words. The check stops the service from scoring text it can't measure; it doesn't make short AI text detectable.

**What it didn't touch:** patterns 2–5 (8 evasions, FP05, PI01, PI02). This fix doesn't affect the core weakness, which is that the plain AI paragraph scores 0.596 (unsure), and it wasn't meant to.




---

📖 **How to run this project: [RUNNING.md](RUNNING.md)**
