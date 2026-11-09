"""
Turning two numbers into one, and one number into something a person can read.
← YOU BUILD THIS IN MILESTONES 4 AND 5

Two functions live here, and both are stubs.

`combine_signals` is where your false-positive decision from Milestone 1
actually gets made. Everything above it — the labels, the appeal path — is
downstream of a number this function produced.

`score_to_label` is where you stop writing for a machine and start writing for
a person. A score of 0.62 means nothing to a writer.

⚠️ Your README's **Signals and Scoring** section has to name the file and
function holding your combining rule. The grader checks your code against what
you claim, so that line should read `scoring.py::combine_signals`.
"""

import config


def combine_signals(model_score: float, style_score: float) -> float:
    """
    Combine two 0–1 signals into one 0–1 score. Milestone 4.

    Both inputs and the output run 0.0 (confidently human) to 1.0 (confidently
    AI).

    THE RULE: a weighted average of the two signals, using the weights in
    config.py. If that average is above AI_THRESHOLD but either signal on its
    own is below AGREEMENT_FLOOR, the score is capped just under AI_THRESHOLD,
    so the label can only be "unsure". There is no matching guard on the human
    side: a wrong accusation costs a writer more than a missed detection costs
    the site, so only the AI label needs both signals to agree. When the two
    signals split, this rule treats that as uncertainty and does not pick a
    winner.

    THE NUMBERS (all in config.py): weights 0.5 / 0.5, AI_THRESHOLD 0.65,
    HUMAN_THRESHOLD 0.35, AGREEMENT_FLOOR 0.5. Placeholders until the four
    calibration inputs have been run.

    Args:
        model_score: from `detector.model_signal` — how predictable the text is.
        style_score: from `stylometry.style_signal` — the shape of the text.

    Returns:
        A float from 0.0 (confidently human) to 1.0 (confidently AI).
    """
    score = (
        config.WEIGHT_MODEL_SIGNAL * model_score
        + config.WEIGHT_STYLE_SIGNAL * style_score
    )

    both_lean_ai = (
        model_score >= config.AGREEMENT_FLOOR
        and style_score >= config.AGREEMENT_FLOOR
    )
    if score > config.AI_THRESHOLD and not both_lean_ai:
        # score_to_label uses >= AI_THRESHOLD, so the cap has to sit just below it.
        score = config.AI_THRESHOLD - 0.01

    return round(min(max(score, 0.0), 1.0), 4)


LABEL_HUMAN = (
    "We think this was probably written by a person. Nothing in it stood out "
    "as typical of machine-generated writing. This is an automated best guess, "
    "so it can be wrong."
)
LABEL_UNSURE = (
    "We can't tell whether this was written by a person or by AI. Some of it "
    "looks like machine writing, but plain, clear writing can look that way "
    "too, so this is not a finding that AI wrote it. If you wrote it yourself, "
    "you can appeal and your appeal will be recorded and flagged for review."
)
LABEL_AI = (
    "This has several features that are common in machine-generated writing. "
    "That's an automated estimate, not proof, and it can be wrong, especially "
    "for plain or very clear writing. If you wrote it yourself, you can appeal "
    "and your appeal will be recorded and flagged for review."
)


def score_to_label(score: float) -> tuple[str, str]:
    """
    Turn a score into (guess, label_text). Thresholds live in config.py.
    The label text only promises what the service does: an appeal is recorded
    and flagged. It doesn't promise a human reviewer.
    """
    if score >= config.AI_THRESHOLD:
        return "ai", LABEL_AI
    if score <= config.HUMAN_THRESHOLD:
        return "human", LABEL_HUMAN
    return "unsure", LABEL_UNSURE


def label_ranges() -> list[tuple[str, str]]:
    """
    The score range each label covers. Your README needs these beside the
    label text — given to you so the numbers can't drift apart from config.py.
    """
    return [
        ("high-confidence human", f"0.00 – {config.HUMAN_THRESHOLD:.2f}"),
        ("unsure", f"{config.HUMAN_THRESHOLD:.2f} – {config.AI_THRESHOLD:.2f}"),
        ("high-confidence AI", f"{config.AI_THRESHOLD:.2f} – 1.00"),
    ]