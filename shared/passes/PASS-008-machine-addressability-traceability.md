# PASS-008: Machine Addressability and Traceability

## Purpose

Enforce stable element IDs (REQ-*, AC-*, TERM-*), registry gate §6, traceability matrix §19, and orphan checks. **Hard gate for `spec-normalizer` only** — no `Ready` without this pass `pass`.

Source basis: normalizer §10 addressing, registry, completion gate -1.5; `addressability-traceability/SKILL.md`.

## Activation / Not applicable

**Activate when:** running `spec-normalizer` addressability stage (always for that mode).

**Not applicable when:** outside `spec-normalizer` run — report `outside spec-normalizer run` per policy.

**Required report if N/A:** exact policy reason string.

## Checklist (numbered)

1. No anonymous normative MUST/SHALL in §8–§14 without REQ-* (split if multiple obligations).
2. REQ element records include: id, title, normative, owner, source, status, related, verification.
3. AC records include: verifies, type, precondition, action, expected, blocking flag.
4. TERM-* records for domain glossary terms used in normative text; do not create TERM-* records for Unity/C# API names or confirmed decomposition/contract signatures.
5. §6 Registry lists every body ID; no orphan registry rows.
6. §19 Traceability matrix exists with minimum columns (REQ, AC, source, owner, blocking).
7. Every **blocking** REQ has ≥1 AC or explicit verification field.
8. Cross-references use IDs, not “see above” section titles alone.
9. Deprecated IDs marked `deprecated` in registry — not deleted without trail.
10. Run completion gate -1.5: registry count matches body scan; matrix covers blocking set.

## Failure signals

- Pretty prose tables without stable IDs.
- REQ in body missing from §6 registry.
- Blocking REQ with empty `verifies` column.
- Matrix missing while §20 claims Ready.

## Example finding templates

```text
[Orphan REQ]
id: REQ-012
Problem: not listed in §6 registry
Recommended fix: add registry row; rebuild matrix row
```

```text
[Missing Traceability]
REQ: REQ-003 (blocking)
Problem: no AC-* and no verification field
Recommended fix: add AC-* or set verification with location
```

Structured finding: `F-xxx | PASS-008 | high | problem | impact | location | recommended_fix`

## Output (link ../pass-loading-policy.md §6)

Report pass status: `pass` | `pass-with-warning` | `block` | `not applicable`.

- Registry/matrix omission is **block**, not warning.
- Blocks must appear in normalizer `Blocking Findings IDs` list (policy §7–§8).

## Mode notes

- **spec-normalizer:** run in `addressability-traceability` stage before readiness stage.
- **spec-assistant / generator:** not applicable — recommend normalizer instead of partial ID assignment.

## Integration with other passes

- **PASS-002:** TERM-* linkage.
- **PASS-009:** cannot be `Ready` if PASS-008 blocked.
- **PASS-010:** merged REQ must update registry and matrix rows.
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
- End of pass checklist; status must appear in mode output pass table.
