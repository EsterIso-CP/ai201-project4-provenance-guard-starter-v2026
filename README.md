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
