# PASS-001: Anti-Weakening

## Purpose

Detect semantic weakening of the specification versus a prior version, source material, or already confirmed decisions. This pass is an early review guard — not full normalization and not a traceability audit. It protects requirement strength, concrete contracts, and confirmed decisions from being diluted into vague prose, open questions, or optional suggestions.

Source basis: assistant extended review §15.1; normalizer anti-weakening gate §15; source preservation expectations.

## Activation / Not applicable

**Activate when:**

- comparing a draft to a previous spec version, GDD excerpt, brief, chat-confirmed fragment, or prior normalized output;
- reviewing edits that merge, shorten, or rephrase requirements;
- running `spec-normalizer` (always compare output to source);
- any mode claims “preserved” or “normalized” strength versus a baseline.

**Not applicable when:**

- there is no prior or source baseline for comparison (state reason explicitly, e.g. “new fragment only, no baseline”);
- the task is purely additive and does not alter existing normative text (name scope).

**Required report if N/A:** one-line reason naming what baseline is missing.

## Checklist (numbered)

1. Scan for removed requirement-level statements (MUST/SHOULD obligations, imperative behavior, forbidden actions).
2. Compare concrete behavior against baseline: are specific actions, thresholds, or sequences replaced by generic wording (“handle correctly”, “as usual”, “by analogy”)?
3. Verify actors, owners, triggers, and lifecycle moments are still present where the baseline named them.
4. Verify negative paths, validation failures, error behavior, and cancellation branches were not dropped.
5. Verify data integrity: fields, enum values, storage keys/paths, API operations, integration boundaries still appear with the same strength.
6. Flag moves of mandatory requirements into non-verifiable sections (notes, suggestions, open questions without ISSUE/OQ linkage in normalizer output).
7. Detect strength inversion: confirmed decision → open question; strict source contract → flexible recommendation; flexible caveat → rigid implementation contract without user confirmation.
8. Detect loss of normative examples: if an example defined mandatory format or contract, confirm it was not removed or weakened without replacement.
9. When deduplicating or merging (coordinate with PASS-010), confirm no extra condition from the duplicate was lost.
10. If uncertain whether a lost detail was mandatory, record `[Possible Weakening]` rather than asserting fact.

## Failure signals

- Mandatory statements disappear with no ISSUE/OQ/decision trail in normalizer mode.
- “Should” / “may” / “preferably” replaces a former MUST without documented user decision.
- Lifecycle/API/data sections shrink while feature scope unchanged.
- Open Questions grow after an edit that was meant to “clean up” the doc.
- Normalizer or assistant claims `pass` on preservation while Source Preservation Notes list weakening risks.

## Example finding templates

```text
[Weakening]
Was in source / previous version:
<quote or paraphrase>

Now in current version:
<quote or paraphrase>

Why this is weaker:
<lost actor | trigger | failure path | field | contract strength>

Recommended fix:
Restore normative wording or record explicit user-approved change as DEC-*.
```

```text
[Possible Weakening]
Detail that may have been lost: <detail>
Need user confirmation: was this mandatory in source or illustrative only?
```

Structured finding (policy §6): `F-xxx | PASS-001 | high | problem | impact | location | recommended_fix`

## Output (link ../pass-loading-policy.md §6)

Report pass status: `pass` | `pass-with-warning` | `block` | `not applicable`.

- `pass-with-warning` and `block` **require** structured findings per `../pass-loading-policy.md` §6 (`id`, `pass_id`, `severity`, `problem`, `impact`, `location`, `recommended_fix`).
- Any `block` on this pass forces mode-level `blocked` / `Not Ready` / `draft-blocked` per policy §8.
- Do not emit bare status without findings when warnings or blocks exist.
- In normalizer output, tie blocking weakening to specific element IDs when addresses exist.

## Mode notes

- **spec-assistant:** run on version compare and after substantive fragment merges; never claim `ok` if §9 weakening block has open items.
- **spec-generator:** compare draft sections to grounded extraction notes before assembly verdict.
- **spec-normalizer:** mandatory comparison to source snapshot; blocks feed §20 and Blocking Findings IDs.

## Integration with other passes

- Pair with **PASS-003** when weakening might be explained as unresolved source conflict.
- Pair with **PASS-010** when merge/dedup is the suspected cause of lost conditions.
- **PASS-009** must not declare `Ready` while PASS-001 is `block`.

11. Coordinate with Source Preservation Notes in normalizer §3.3 when recording weakening risks.
12. Document [Possible Weakening] items in findings even when overall pass is pass-with-warning.
