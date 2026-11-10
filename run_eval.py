#!/usr/bin/env python3
"""
Run your five criteria three times each.  <- UNIT 8, MILESTONE 3

    python app.py                              # in one terminal
    python run_eval.py --label before          # in another
    python run_eval.py --label after

The attack set tests what staff thought to test. This tests what *you* thought
to test, and the two rarely overlap much. Both count.

Fill in `scenarios.py` first — that's where you say what each criterion needs
run against it. A criterion about false positives needs your own writing. One
about label coverage needs inputs across the score range.

!! Three trials, and **your first signal runs a model, so identical input can
score differently twice.** That's exactly why repeats matter here.

This does the sending and the recording. It does not decide whether a trial
passed — that depends on the criterion you wrote, so the Verdict column comes
back blank.
"""

import argparse
import datetime as dt
import json
import sys
import time
import uuid
from pathlib import Path

import config

# Windows consoles often run a codepage that can't print every character in
# this file's help text. Without this, `--help` ends in a UnicodeEncodeError
# traceback instead of the help — which is a miserable first thing to hit.
for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(errors="replace")
    except (AttributeError, ValueError):  # not a normal text stream
        pass


DEFAULT_URL = f"http://{config.HOST}:{config.PORT}"


def bodies_for(scenario):
    """
    The request bodies one scenario sends.

    A "texts" scenario gets a creator_id made up for it. A "bodies" scenario is
    sent exactly as written, which is how a bad-input criterion says things a
    string can't — no `text` field, a null, something enormous.
    """
    if scenario.get("bodies"):
        return list(scenario["bodies"])
    return [
        {"text": text, "creator_id": f"eval_{scenario['name'][:12]}_{i}"}
        for i, text in enumerate(scenario["texts"], 1)
    ]


def describe(body):
    """A short, readable note of what was sent — for the report."""
    if set(body) == {"text", "creator_id"} and isinstance(body.get("text"), str):
        text = body["text"]
        return text[:70] if text else "(empty text)"
    return json.dumps(body)[:120]


def run_appeal_trial(requests, url, scenario, timeout):
    """
    One trial of an "appeals" scenario (criterion 4).

    For each text: submit it, appeal the content_id that came back, then read
    GET /log and check the appeal is there with that content_id, the reasoning,
    and status under_review. Last, appeal a content_id that was never issued:
    that should be a 404 and leave no appeal entry behind.
    """
    results = []
    for i, text in enumerate(scenario["appeals"], 1):
        creator = f"eval_{scenario['name'][:12]}_{i}"
        reasoning = f"I wrote this myself (eval appeal {i})."
        row = {"sent": describe({"text": text, "creator_id": creator})}
        try:
            sub = requests.post(f"{url}/submit", json={"text": text, "creator_id": creator},
                                timeout=timeout)
            content_id = sub.json().get("content_id")
            row["submit_status"] = sub.status_code
            row["content_id"] = content_id
            app = requests.post(f"{url}/appeal",
                                json={"content_id": content_id, "reasoning": reasoning},
                                timeout=timeout)
            row["status"] = app.status_code
            row["appeal_response"] = app.json()
            entries = requests.get(f"{url}/log", timeout=timeout).json()["entries"]
            mine = [e for e in entries if e.get("content_id") == content_id]
            appeal_entries = [e for e in mine if e.get("event") == "appeal"
                              and e.get("reasoning") == reasoning]
            row["log_entries_for_id"] = len(mine)
            row["appeal_logged"] = bool(appeal_entries)
            row["logged_status"] = appeal_entries[-1].get("status") if appeal_entries else None
            row["passed"] = (app.status_code == 200
                             and row["appeal_response"].get("status") == "under_review"
                             and row["logged_status"] == "under_review")
        except Exception as exc:  # noqa: BLE001
            row.update({"status": None, "error": f"{type(exc).__name__}: {exc}",
                        "passed": False})
        results.append(row)

    fake = str(uuid.uuid4())
    row = {"sent": f"appeal on unknown content_id {fake}"}
    try:
        app = requests.post(f"{url}/appeal",
                            json={"content_id": fake, "reasoning": "This was mine."},
                            timeout=timeout)
        entries = requests.get(f"{url}/log", timeout=timeout).json()["entries"]
        stray = [e for e in entries
                 if e.get("content_id") == fake and e.get("event") == "appeal"]
        row.update({"status": app.status_code, "appeal_response": app.json(),
                    "appeal_entries_created": len(stray),
                    "passed": app.status_code == 404 and not stray})
    except Exception as exc:  # noqa: BLE001
        row.update({"status": None, "error": f"{type(exc).__name__}: {exc}",
                    "passed": False})
    results.append(row)
    return results


def main():
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--trials", type=int, default=3)
    parser.add_argument("--label", default="")
    parser.add_argument("--url", default=DEFAULT_URL)
    parser.add_argument("--timeout", type=float, default=90.0)
    args = parser.parse_args()

    try:
        import requests
    except ImportError:
        print("The `requests` package isn't installed.\n"
              "Run: pip install -r requirements.txt", file=sys.stderr)
        sys.exit(1)

    try:
        import scenarios
    except ImportError:
        print("No scenarios.py found. Milestone 3 starts by filling it in.",
              file=sys.stderr)
        sys.exit(1)

    problems = scenarios.validate()
    if problems:
        print("scenarios.py has problems:\n", file=sys.stderr)
        for problem in problems:
            print(f"  - {problem}", file=sys.stderr)
        sys.exit(1)

    try:
        requests.get(f"{args.url}/health", timeout=5)
    except Exception:  # noqa: BLE001
        print(f"Nothing answering at {args.url}. Start it:  python app.py",
              file=sys.stderr)
        sys.exit(1)

    if args.trials < 3:
        print(f"!! {args.trials} trial(s). The submission asks for three.\n")

    rows = []
    for scenario in scenarios.SCENARIOS:
        print(f"\n{scenario['name']}  (criterion {scenario.get('criterion') or '—'})")

        trials = []
        for trial in range(1, args.trials + 1):
            if scenario.get("appeals"):
                results = run_appeal_trial(requests, args.url, scenario, args.timeout)
                trials.append(results)
                passed = sum(1 for r in results if r.get("passed"))
                print(f"  trial {trial}: {passed}/{len(results)} appeal checks passed")
                continue
            results = []
            for i, body in enumerate(bodies_for(scenario), 1):
                preview = describe(body)
                started = time.monotonic()
                try:
                    response = requests.post(f"{args.url}/submit", json=body,
                                             timeout=args.timeout)
                    elapsed = round(time.monotonic() - started, 2)
                    payload = response.json() if response.content else {}
                    results.append({
                        "status": response.status_code,
                        "guess": payload.get("guess"),
                        "confidence": payload.get("confidence"),
                        "model_score": payload.get("model_score"),
                        "style_score": payload.get("style_score"),
                        "label": payload.get("label"),
                        "error": payload.get("error"),
                        "elapsed_s": elapsed,
                        "sent": preview,
                    })
                except Exception as exc:  # noqa: BLE001
                    results.append({"status": None, "error": f"{type(exc).__name__}: {exc}",
                                    "sent": preview})

            trials.append(results)
            guesses = [r.get("guess") or "—" for r in results]
            print(f"  trial {trial}: {', '.join(guesses)}")

        rows.append({"scenario": scenario, "trials": trials})

    write_report(rows, args)


def write_report(rows, args):
    config.RESULTS_DIR.mkdir(exist_ok=True)
    stamp = dt.datetime.now().strftime("%Y-%m-%d_%H%M")
    label = f"_{args.label}" if args.label else ""
    path = config.RESULTS_DIR / f"run_{stamp}{label}.md"

    n = args.trials
    headers = " | ".join(f"Run {i}" for i in range(1, n + 1))
    divider = "|".join(["---"] * n)

    lines = [
        f"# Run log{f' — {args.label}' if args.label else ''}",
        "",
        "- Produced by: `run_eval.py::main`",
        "- Service: `app.py::submit` · scoring: `scoring.py::combine_signals`",
        f"- {n} trials per criterion · {dt.datetime.now().strftime('%Y-%m-%d %H:%M')}",
        "",
        "Fill in Target from `criteria.md`, and Run and Verdict from the output",
        "underneath. Whether a trial passed depends on the criterion you wrote.",
        "",
        f"| Criterion | Target | {headers} | Verdict |",
        f"|---|---|{divider}|---|",
    ]

    for row in rows:
        scenario = row["scenario"]
        number = scenario.get("criterion")
        name = f"{number}. {scenario['name']}" if number else scenario["name"]
        lines.append(f"| {name} |  | {' | '.join([' '] * n)} |  |")

    lines += ["", "---", "", "## What actually came back", "",
              "Real output. Paste the relevant parts into your README — the rubric",
              "asks for the actual JSON, not a description of it.", ""]

    for row in rows:
        scenario = row["scenario"]
        lines += [f"### {scenario['name']}", ""]
        for trial_number, results in enumerate(row["trials"], 1):
            lines += [f"**Trial {trial_number}**", "", "```json",
                      json.dumps(results, indent=2), "```", ""]

    path.write_text("\n".join(lines), encoding="utf-8")
    print(f"\nWrote {path.relative_to(config.ROOT)}")
    print("Commit it. It's the evidence the test actually happened.")


if __name__ == "__main__":
    main()
