# Decisions — Provenance Guard

Newest first. Each entry: the decision, the date, and why.

---

## 2026-11-15 — Endpoint contracts settled

Both endpoints' fields and error cases are in `docs/milestone1.md`, section 4. `/appeal`
confirms with `status: under_review`, returns 404 for an unknown `content_id`, and refuses
blank reasoning with a 400.

**Why:** a writer who appeals should see that something happened. An unknown id has to fail
loudly, because a typo that silently succeeds looks like a working appeal that went nowhere.
An appeal with no reasoning gives a reviewer nothing to act on.

---

## 2026-11-12 — `confidence` is the combined score

The `confidence` field in the `/submit` response holds the combined score, from 0.0
(confidently human) to 1.0 (confidently AI).

**Why:** unit 8's `run_attacks.py` and `run_eval.py` read `confidence` and compare it to the
thresholds. Any other meaning, such as distance from 0.5, would make every row of next
unit's reports wrong.
