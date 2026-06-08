# PASS-006: Edge Cases and Testability

## Purpose

Ensure derived edge cases, validation/failure paths, and acceptance testability are explicit — including MVP placeholders that must not ship as silent production contracts.

Source basis: assistant §15.5 (derived edge cases) and §15.7 (testability / placeholders).

## Activation / Not applicable

**Activate when:** testable MVP data, flows, AC, or derivable edge cases from API/lifecycle/data exist.

**Not applicable when:** no testable flows or derivable edges (state reason).

**Required report if N/A:** one-line scope note.

## Checklist (numbered)

1. For each blocking REQ: ≥1 observable AC or explicit verification location in REQ record.
2. Happy path plus material negative paths (validation fail, timeout, cancel, deny, empty input).
3. Edge cases derived from rules: min/max, concurrency, duplicate action, stale state, offline, permission denied.
4. Placeholder values (“TBD enum”, “mock id”) flagged — must be OQ or DEC, not normative production value.
5. Acceptance criteria use observable outcomes, not implementation internals.
6. Non-functional reqs (performance, memory) measurable or marked OQ with ISSUE when blocking.
7. Test-only hooks called out separately from production REQ or forbidden in §13/§14.
8. Cross-check flows §7 against AC §16 — no orphan critical step.
9. Normalizer: AC `type` includes negative/edge where applicable; `blocking` aligned with REQ.
10. If edge case is intentionally undefined, record OQ with risk — do not omit silently.

## Failure signals

- Blocking AC uses subjective wording (“feels responsive”, “works well”).
- Critical failure path described only in narrative footnote.
- Placeholder enum in MUST sentence without OQ.
- REQ with no AC row in matrix (PASS-008 coordination).

## Example finding templates

```text
[Testability Gap]
REQ/AC: <ids>
Problem: <unobservable | missing negative path>
Recommended fix: rewrite expected outcome; add AC-negative
```

```text
[Derived Edge Case]
Source rule: <REQ quote>
Missing case: <scenario>
Recommended fix: add AC-edge or OQ with ISSUE if product decision needed
```

Structured finding: `F-xxx | PASS-006 | medium | problem | impact | location | recommended_fix`

## Output (link ../pass-loading-policy.md §6)

Report pass status: `pass` | `pass-with-warning` | `block` | `not applicable`.

- Untestable blocking AC typically **block** for normalizer readiness.

## Mode notes

- **spec-assistant:** review-full block 12 maps here.
- **spec-generator:** assembly-verdict must not pass with placeholder AC on blocking paths.

## Integration with other passes

- **PASS-004:** lifecycle gaps spawn edge cases.
- **PASS-008:** matrix orphan REQ → block.
- **PASS-009:** testability dimension in §20 verdict.
## Mode integration notes

- **spec-assistant:** report pass status in review table; map templates to review-full §16 blocks when applicable.
- **spec-generator:** run when profile/extra passes demand; never skip because GDD seems simple.
- **spec-normalizer:** treat block as hard gate; link findings to element IDs when addresses exist.
- **Escalation:** bare warning/block without §6 findings is a contract execution error for all modes.
- **Cross-pass:** re-run dependent passes after fixes (e.g. dedup → anti-weakening, terminology → readiness).
## Reference triggers (quick scan)

- Re-read affected spec sections after any merge, rename, or ID reassignment.
- Quote the smallest source fragment that proves the finding (avoid long dumps).
- If the user asked for a short answer, still run mandatory passes; compress findings, not checks.
- Record 
ot applicable with scope, not silence.
- Prefer restoring source strength over adding new requirements when fixing PASS-001 findings.
- When two passes conflict, report both findings and let the user decide (PASS-003).
- Normalizer: never return Ready while PASS-008 or PASS-009 is block.
- Generator: unresolved PASS-003 block → draft-blocked with findings before assembly.
