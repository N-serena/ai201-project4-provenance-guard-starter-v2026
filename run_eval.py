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

Two scenario keys, added in unit 8, collect what criteria 2 and 3 need:

    "appeal_reasoning"   after each successful submit, appeal its content_id
                         with this reasoning and look for the appeal in /log.
    "check_rejections"   after each trial, count 4xx responses, rejected
                         entries the trial added to /log, and whether /ping
                         still answers.

A "bodies" entry that is a str is sent as raw bytes, for a body that isn't JSON.
"""

import argparse
import datetime as dt
import json
import sys
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


def post_body(requests, url, body, timeout):
    """
    Send one request body to /submit.

    A dict goes out as JSON. A str goes out as raw bytes labelled
    application/json, which is how a scenario sends a body that isn't JSON.
    """
    if isinstance(body, str):
        return requests.post(f"{url}/submit", data=body.encode("utf-8"),
                             headers={"Content-Type": "application/json"},
                             timeout=timeout)
    return requests.post(f"{url}/submit", json=body, timeout=timeout)


def log_entries(requests, args):
    """Every entry in the audit log, oldest first."""
    return requests.get(f"{args.url}/log", timeout=args.timeout).json()["entries"]


def send_appeal(requests, args, content_id, reasoning):
    """Appeal one decision, then look for that appeal in /log."""
    response = requests.post(f"{args.url}/appeal",
                             json={"content_id": content_id, "reasoning": reasoning},
                             timeout=args.timeout)
    payload = response.json() if response.content else {}
    in_log = any(e.get("content_id") == content_id and e.get("event") == "appeal"
                 for e in log_entries(requests, args))
    return {"status": response.status_code, "appeal_status": payload.get("status"),
            "in_log": in_log}


def trial_checks(requests, args, scenario, results, log_start):
    """
    The checks a criterion needs beyond each response.

    Appeals: how many came back under_review and how many reached /log.
    Rejections: how many 4xx and 5xx came back, how many rejected entries this
    trial added to /log, and whether /ping still answers afterwards.
    """
    checks = {}
    if scenario.get("appeal_reasoning"):
        appeals = [r["appeal"] for r in results if "appeal" in r]
        checks["appeals_sent"] = len(appeals)
        checks["under_review"] = sum(a["appeal_status"] == "under_review" for a in appeals)
        checks["in_log"] = sum(a["in_log"] for a in appeals)
    if scenario.get("check_rejections"):
        codes = [r.get("status") or 0 for r in results]
        added = log_entries(requests, args)[log_start:]
        ping = requests.post(f"{args.url}/ping", json={"message": "still there?"},
                             timeout=args.timeout)
        checks["4xx"] = sum(400 <= c < 500 for c in codes)
        checks["not_4xx"] = sum(not 400 <= c < 500 for c in codes)
        checks["with_error_and_message"] = sum(
            bool(r.get("error_code")) and r.get("has_message", False) for r in results)
        checks["rejections_logged"] = sum(e.get("event") == "rejected" for e in added)
        checks["ping_status"] = ping.status_code
    return checks


def describe(body):
    """A short, readable note of what was sent — for the report."""
    if isinstance(body, str):
        return f"raw body: {body[:60]}"
    if set(body) == {"text", "creator_id"} and isinstance(body.get("text"), str):
        text = body["text"]
        return text[:70] if text else "(empty text)"
    return json.dumps(body)[:120]


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
            results = []
            needs_log = scenario.get("check_rejections")
            log_start = len(log_entries(requests, args)) if needs_log else 0
            for i, body in enumerate(bodies_for(scenario), 1):
                preview = describe(body)
                try:
                    response = post_body(requests, args.url, body, args.timeout)
                    payload = response.json() if response.content else {}
                    result = {
                        "status": response.status_code,
                        "guess": payload.get("guess"),
                        "confidence": payload.get("confidence"),
                        "model_score": payload.get("model_score"),
                        "style_score": payload.get("style_score"),
                        "label": payload.get("label"),
                        "error_code": payload.get("error"),
                        "has_message": bool(payload.get("message")),
                        "sent": preview,
                    }
                    if scenario.get("appeal_reasoning") and payload.get("content_id"):
                        result["appeal"] = send_appeal(requests, args, payload["content_id"],
                                                       scenario["appeal_reasoning"])
                    results.append(result)
                except Exception as exc:  # noqa: BLE001
                    results.append({"status": None, "error": f"{type(exc).__name__}: {exc}",
                                    "sent": preview})

            checks = trial_checks(requests, args, scenario, results, log_start)
            trials.append({"results": results, "checks": checks})
            marks = [r.get("guess") or str(r.get("status") or "—") for r in results]
            print(f"  trial {trial}: {', '.join(marks)}")
            if checks:
                print(f"           {checks}")

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
        for trial_number, trial in enumerate(row["trials"], 1):
            lines += [f"**Trial {trial_number}**", ""]
            if trial["checks"]:
                lines += ["Checks: `" + json.dumps(trial["checks"]) + "`", ""]
            lines += ["```json", json.dumps(trial["results"], indent=2), "```", ""]

    path.write_text("\n".join(lines), encoding="utf-8")
    print(f"\nWrote {path.relative_to(config.ROOT)}")
    print("Commit it. It's the evidence the test actually happened.")


if __name__ == "__main__":
    main()
