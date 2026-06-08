# PASS-009: Readiness Verdict Gate

## Purpose

Aggregate mandatory pass results, readiness dimensions, and completion rules into §20 Readiness Verdict. Prevents premature `Ready` labels when structural or semantic gates still fail.

Source basis: normalizer §3.20 readiness, §7.2 gates; `anti-weakening-readiness/SKILL.md`.

## Activation / Not applicable

**Activate when:** `spec-normalizer` final readiness stage emits §20.

**Not applicable when:** outside `spec-normalizer` — report `outside spec-normalizer run`.

**Required report if N/A:** policy reason string.

## Checklist (numbered)

1. Collect per-pass status for all profile-mandatory passes (see `../pass-loading-policy.md` §4).
2. Score dimensions: source preservation, terminology, machine addressing, orphan blocking elements, unresolved blockers.
3. Any mandatory pass `block` → verdict **Not Ready** / **Blocked** (no exception).
4. `PASS-008` or `PASS-009` block → cite specific finding IDs in §20 and mode output list.
5. PASS-001 comparison to source complete or marked N/A with reason in preservation notes.
6. PASS-010 dedup log reviewed — no critical condition loss.
7. Open Questions: blocking OQ/ISSUE listed in verdict; non-blocking listed separately.
8. §20 includes explicit **Verdict** line and dimension table — not prose-only.
9. Assistant/generator must not emit normalizer `Ready` (forbidden in review SKILL §7).
10. Completion gate -1.5: pass table + findings + artifact path hint present in mode output.

## Failure signals

- §20 says Ready while pass table shows block.
- Missing Blocking Findings IDs when blocks exist.
- Silent skip of mandatory pass without `not applicable`.
- Dimensions all “ok” but PASS-008 findings open.

## Example finding templates

```text
[Readiness Gate Failure]
Verdict attempted: Ready
Blocking passes: PASS-008, PASS-003
Finding IDs: F-014, F-015
Recommended fix: resolve findings; re-run addressability then readiness
```

```text
[Incomplete Verdict Section]
Missing: <dimension row | Blocking Findings IDs | pass aggregate>
Recommended fix: complete §20 template per anti-weakening-readiness SKILL
```

Structured finding: `F-xxx | PASS-009 | high | problem | impact | location | recommended_fix`

## Output (link ../pass-loading-policy.md §6)

Report pass status: `pass` | `pass-with-warning` | `block` | `not applicable`.

- This pass **is** the readiness gate — `block` means deliver `Not Ready` artifact state.

## Mode notes

- **spec-normalizer:** only mode that may declare implementation-ready `Ready`.
- **spec-assistant:** may assess “implementability” in review status — not §20 Ready.

## Integration with other passes

- **PASS-001** and **PASS-008** are common blocking upstream passes.
- **PASS-010** critical loss forces Not Ready per normalizer SKILL §5.
- Policy §8 maps aggregate pass status to mode output enums.
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
- Verdict section is mandatory in normalizer §20 output.
