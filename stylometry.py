"""
Signal two: the style signal. ← YOU BUILD THIS IN MILESTONE 4

Signal one reads the text for meaning. This one measures it *as text* — the
shape of it, without understanding a word.

Three measures are stubbed below because the brief names those three. They are
stubs, not implementations: what they compute is yours, and so is how you
combine them.

    sentence_length_spread   do sentences vary in length, or march in step?
    type_token_ratio         how much of the vocabulary repeats?
    punctuation_density      how much punctuation, and how varied?

Why these might differ between human and AI writing: generated prose tends
toward even, mid-length sentences and a narrower band of vocabulary, because
that's what "most likely next word" produces on average. Human writing is
lumpier — a three-word sentence next to a forty-word one.

⚠️ **The blind spot, which you have to name in Milestone 1.**

This signal cannot read. It has no idea what the text says. Anything that
changes the shape without changing the substance moves it — adding typos,
breaking up sentences, pasting in a quotation. That is a very cheap thing for
someone to do on purpose, and unit 8's attack set will do it to you.

Build each function on its own and call it from a terminal before you wire
anything together:

    python stylometry.py "some text to look at"
"""

import re
import statistics


def sentences(text: str) -> list[str]:
    """Split into sentences. Rough and good enough — given to you."""
    parts = re.split(r"(?<=[.!?])\s+", text.strip())
    return [p for p in parts if p.strip()]


def words(text: str) -> list[str]:
    """Split into lowercase words, punctuation stripped. Given to you."""
    return re.findall(r"[a-z0-9']+", text.lower())


# ── The three measures — YOU BUILD THESE ─────────────────────────────────────

TTR_WINDOW = 100  # only look at the first 100 words, so length can't fake a signal


def sentence_length_spread(text: str) -> float:
    """
    Coefficient of variation of sentence length (stdev / mean, in words).
    Scale: 0 upward; typical 0.2 (even) to 0.8 (lumpy). HIGHER = MORE HUMAN.
    Fewer than two sentences has no spread, so it returns NaN, and
    style_signal treats that as neutral (0.5) instead of accusing anyone.
    """
    lengths = [len(words(s)) for s in sentences(text)]
    lengths = [n for n in lengths if n > 0]
    if len(lengths) < 2:
        return float("nan")
    return statistics.stdev(lengths) / statistics.mean(lengths)


def type_token_ratio(text: str) -> float:
    """
    Unique words / total words, over the first TTR_WINDOW words only.
    Scale: 0 to 1. HIGHER = MORE VARIED = MORE HUMAN.
    """
    w = words(text)[:TTR_WINDOW]
    return len(set(w)) / len(w) if w else 0.0


_PUNCT = re.compile(r"[,;:()\u2014\u2013\"?!-]")

def punctuation_density(text: str) -> float:
    """
    Non-period punctuation marks per word (commas, semicolons, colons, dashes,
    parentheses, quotes, ? and !). Scale: 0 upward. Direction is a GUESS:
    here HIGHER = MORE AI-ISH, which is the weakest assumption of the three.
    """
    w = words(text)
    return len(_PUNCT.findall(text)) / len(w) if w else 0.0


def _clamp(x: float) -> float:
    return min(max(x, 0.0), 1.0)



# ── Combining them ───────────────────────────────────────────────────────────

def style_signal(text: str) -> float:
    """0-1, HIGHER = MORE LIKELY AI. Each measure becomes an AI-ness sub-score
    on 0-1 first, so none wins just because its raw numbers are bigger."""
    cv = sentence_length_spread(text)
    spread_ai = 0.5 if cv != cv else _clamp(1.0 - cv / 0.8)         # flipped
    ttr_ai = _clamp(1.0 - (type_token_ratio(text) - 0.55) / 0.40)   # flipped
    punct_ai = _clamp(punctuation_density(text) / 0.15)             # not flipped
    return round(0.5 * spread_ai + 0.3 * ttr_ai + 0.2 * punct_ai, 4)


if __name__ == "__main__":
    import sys

    text = " ".join(sys.argv[1:]) or (
        "The system works well. It handles most cases correctly and provides "
        "good results. Users generally find it easy to use and understand."
    )

    print(f"{len(sentences(text))} sentences, {len(words(text))} words\n")
    print(f"sentence_length_spread   {sentence_length_spread(text)}")
    print(f"type_token_ratio         {type_token_ratio(text)}")
    print(f"punctuation_density      {punctuation_density(text)}")
    print(f"style_signal             {style_signal(text)}   (higher = more likely AI)")
    print("\nAll zeros? These are stubs — Milestone 4 is where you build them.")
