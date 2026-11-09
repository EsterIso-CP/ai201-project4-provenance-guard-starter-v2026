# Acceptance criteria — Provenance Guard

Five criteria that say what "working" means for this service, written in unit 7
before building it. Each one names a number or something plainly observable.
Every target has to hold in all three trials in unit 8, not just on average.

Areas covered: false positives, score spread, label coverage, the appeal path,
bad input.

---

## 1. False positives: my own writing is rarely called AI

Of 10 pieces I wrote myself (at least 4 of them plainly written, short
sentences, common words), at most 1 is labeled high-confidence AI, in every one
of the three trials.

**Why this target:** On a writing site a wrong accusation costs the writer far
more than a missed detection costs the site, so this is the tightest target I
set. I include plain writing on purpose, because that is the writing signal one
is most likely to accuse, and a test set of only ornate prose would let me
pass without checking the real risk.

---

## 2. Score spread: clearly-AI and clearly-human text separate

The mean combined score of 5 clearly AI inputs is at least 0.30 higher than the
mean of 5 clearly-human inputs, and no clearly AI input scores below the
lowest clearly-human input.

**Why this target:** If the two groups sit within 0.30 of each other, the
thresholds are doing the work of guessing, not the signals. I chose 0.30
because the unsure band is roughly 0.40 wide, so the gap must be big enough
that the groups can land in different labels. The no-overlap clause matters
because a good average can hide a few inputs that are ranked backwards.

---

## 3. Label coverage: all three labels are reachable, and "unsure" isn't a dump

Across 20 test inputs, each of the three labels is returned at least once, and
"unsure" is returned for no more than 8 of the 20 (40%).

**Why this target:** A label that can never be returned is dead wording. A
service that answers "unsure" to everything also never accuses anyone, but it
tells the reader nothing. Capping unsure at 40% forces the thresholds to commit
on a clear majority of inputs while still leaving room for real uncertainty.

---

## 4. The appeal path: every appeal changes status and is logged

For 10 of 10 appeals on a valid `content_id`, the content's status changes to
under appeal, and a new entry appears in `GET /log` containing the
`content_id` and the `reasoning` text. An appeal on an unknown `content_id`
returns a 404 and changes nothing else.

**Why this target:** The appeal is the only thing a wrongly-accused writer can
do, so it has to work every time, not most of the time. An appeal that quietly
vanishes is worse than not having one, because the writer believes someone will
look. Zero failures is the only target that makes sense here.

---

## 5. Bad input: broken requests get a clear error, never a score

Five bad inputs each return a 4xx JSON error within 10 seconds, with no 500 and
no score in the response: missing `text`, empty `text`, whitespace-only `text`,
non-string `text` (e.g. a number), and a 100,000-character `text`.

**Why this target:** Returning a score for text that was never really read
would be a confident answer with nothing behind it. The 100,000-character case
also checks that an enormous submission can't tie up the model for minutes,
which matters once rate limiting is on. A 500 would mean the failure is
mine, not the caller's.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     UNIT 8 — if a criterion is BROKEN (can't be measured), add a revision
     underneath it. Never delete or edit the original line. Lowering a target
     because I missed it is not a revision.
     ───────────────────────────────────────────────────────────────────────── -->