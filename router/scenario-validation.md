# Scenario Validation

## Purpose

Validate route and pass activation coherence for key scenarios.

Canonical matrix: `../shared/pass-loading-policy.md` §4.
Routing entry: `./router-map.md`.

---

## Happy-Path Scenarios

### Scenario 1: Fragment Capture

**Sample intent:** "Add this new reward rule to the existing spec section."

* route: `spec-assistant` → `../modes/spec-assistant/fragment-capture/SKILL.md`
* profiles: none
* passes: `PASS-002`, `PASS-003` (per pass-loading-policy §4)
* expected behavior: local update, no full rewrite, one next step
* result: valid

---

### Scenario 2: Review-Light

**Sample intent:** "Quickly check this draft for obvious problems."

* route: `spec-assistant` → `../modes/spec-assistant/review-light/SKILL.md`
* profiles: `../review-profiles/review-light.md`
* passes from profile: `PASS-003`, `PASS-002`, `PASS-001`, `PASS-006`
* expected behavior: concise findings-first report; escalation contract §6 applies; **no edits** to `SPECIFICATION_PATH` unless user explicitly requests application afterward
* result: valid

---

### Scenario 3: Review-Full

**Sample intent:** "Do a full deep review before implementation."

* route: `spec-assistant` → `../modes/spec-assistant/review-full/SKILL.md`
* profiles: `../review-profiles/review-full.md` (includes light + extended)
* effective passes: `PASS-003`, `PASS-002`, `PASS-001`, `PASS-006`, `PASS-004`, `PASS-005`, `PASS-007`, `PASS-010`
* expected behavior: deep findings-first report with risks and proposed fixes (chat only); **no edits** to `SPECIFICATION_PATH` unless user explicitly requests application afterward
* result: valid

---

### Scenario 4: Generator

**Sample intent:** "Generate a complete technical spec from this GDD."

* route: `spec-generator` → `../modes/spec-generator/SKILL.md`
* profiles: `../review-profiles/review-light.md`
* extra passes: `PASS-004`, `PASS-005`, `PASS-007`, `PASS-010`
* expected behavior: grounded full draft with explicit assumptions/open questions
* result: valid

---

### Scenario 5: Normalizer

**Sample intent:** "Normalize this specification into implementation-ready markdown."

* route: `spec-normalizer` → `../modes/spec-normalizer/SKILL.md`
* profiles: `../review-profiles/review-full.md`
* extra passes: `PASS-008`, `PASS-009`, `PASS-010`
* hard gate: if `PASS-008` or `PASS-009` fails, readiness is blocked with blocking finding IDs
* expected behavior: machine-addressable normalized artifact with traceability/readiness verdict
* result: valid

---

## Edge Scenarios

### Scenario 6: Ambiguous Intent

**Sample intent:** "Look at this spec" (no artifact: patch vs review vs generate).

* route: `spec-assistant` (default per `router-map.md` §3)
* clarifying questions: at most one critical question before execution
* do not route to `spec-generator` or `spec-normalizer` until intent is clear
* result: valid

---

### Scenario 7: Partial Source

**Sample intent:** "Generate the full spec" with incomplete GDD / missing sections.

* route: `spec-generator`
* passes: generator set (review-light + extras per §4)
* expected behavior: `block` or explicit assumptions/open questions; no silent invention
* `PASS-003` must surface grounding gaps as findings
* result: valid (blocked draft acceptable with findings)

---

### Scenario 8: Conflicting Source

**Sample intent:** Two design sources contradict on ownership or data contract.

* route: depends on task — review → `spec-assistant` + appropriate profile; generate → `spec-generator`
* `PASS-003` (and `PASS-004`/`PASS-005` when in scope) must emit conflict findings
* must not: auto-pick a winner without a user-visible finding
* result: valid

---

### Scenario 9: Not-Applicable Passes

**Sample intent:** Review a UI copy fragment with no API/data/lifecycle in scope.

* route: `spec-assistant` + `review-light`
* conditional passes (`PASS-004`, `PASS-005`, `PASS-006` when out of scope): `not applicable` with stated reason per `pass-loading-policy.md` §4
* must not: skip mandatory profile passes silently
* result: valid

---

## Pass Escalation Contract Scenarios

Reference: `../shared/pass-loading-policy.md` §6. Mode wrappers aggregate; pass files do not duplicate escalation fields.

### Scenario 10: Warning With Findings

**Setup:** A mandatory pass returns `pass-with-warning` with at least one structured finding (`id`, `pass_id`, `severity`, `problem`, `impact`, `location`, `recommended_fix`).

* mode-layer status: `warning` (assistant) / `draft-warning` (generator) per §8 mapping
* user report: includes aggregated findings list — not status-only
* result: **valid contract**

---

### Scenario 11: Block With Findings

**Setup:** Any mandatory pass returns `block` with one or more structured findings (blocking IDs for `PASS-008`/`PASS-009` in normalizer).

* mode-layer status: `blocked` / `Blocked` / `Not Ready` as applicable
* normalizer: `Ready` forbidden; blocking finding IDs required in verdict
* user report: findings-first; targeted fixes where applicable
* result: **valid contract**

---

### Scenario 12: Block Without Findings (Contract Error)

**Setup:** Pass or mode layer emits `block` or `pass-with-warning` **without** structured findings.

* expected executor behavior: treat as **contract violation** — rebuild findings before final user output; do not ship bare status
* mode wrappers (`spec-assistant`, `spec-generator`, `spec-normalizer`) and `mode-transition-guards.md` §6: forced `blocked` / no `Ready`
* negative test: this scenario must **fail** validation if presented as a finished user deliverable
* result: **invalid** — contract error

---

## Coherence Checklist

1. all scenarios use only `spec-assistant`, `spec-generator`, or `spec-normalizer`;
2. pass activation matches `../shared/pass-loading-policy.md` §4 for each scenario row;
3. review profiles list only pass IDs; semantics stay in `../shared/passes/*`;
4. normalizer hard gate (`PASS-008`, `PASS-009`) explicitly blocks `Ready` on failure;
5. escalation scenarios 10–11 satisfy §6; scenario 12 must never pass as final output.
