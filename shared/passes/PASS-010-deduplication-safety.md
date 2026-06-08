# PASS-010: Deduplication Safety

## Purpose

Ensure merge and deduplication preserve normative strength, extra conditions, and canonical section placement. Logs merges transparently so reviewers can audit what was collapsed.

Source basis: normalizer §8 dedup; pipeline SKILL step 4; regulation core rule 3.

## Activation / Not applicable

**Activate when:** deduplication, merge, or canonical placement runs this session.

**Not applicable when:** `no deduplication performed` (exact policy phrase).

**Required report if N/A:** `no deduplication performed` or stated merge scope empty.

## Checklist (numbered)

1. Identify duplicate clusters: same obligation, same actor/trigger, same data field across sections.
2. Choose canonical home section per regulation — do not leave shadow copies with different strength.
3. When merging REQ text, union all conditions — do not drop conjunctive clauses from either duplicate.
4. Record merge in §3 Source Analysis / preservation notes or dedup log (ids merged → survivor).
5. Cross-check PASS-001: merged result not weaker than strongest source duplicate.
6. Update REQ/AC/TERM IDs: deprecate merged-away ids in registry; survivor `related` lists sources.
7. Refresh §19 matrix rows — no duplicate blocking paths for same behavior without ISSUE.
8. Do not merge terms (PASS-002) or conflicting sources (PASS-003) without DEC-/ISSUE.
9. Generator light profile: run when assembly collapses bullets.
10. If unsure whether duplicates differ materially, keep separate REQ + ISSUE rather than merge.

## Failure signals

- Shorter doc after dedup with fewer MUST lines and no merge log.
- Two AC for same behavior deleted without consolidating verification.
- Survivor REQ missing condition present only in removed duplicate.
- Dedup across Conflicts without ISSUE resolution.

## Example finding templates

```text
[Dedup Condition Loss]
Survivor: REQ-007
Removed duplicate: REQ-021 (deprecated)
Lost condition: <quote>
Recommended fix: restore clause in REQ-007; update merge log
```

```text
[Unsafe Merge]
Items merged: <REQ-003, REQ-018>
Problem: different actors / conflicting triggers
Recommended fix: unmerge; ISSUE-*; assign distinct owners
```

Structured finding: `F-xxx | PASS-010 | high | problem | impact | location | recommended_fix`

## Output (link ../pass-loading-policy.md §6)

Report pass status: `pass` | `pass-with-warning` | `block` | `not applicable`.

- Critical deduplication loss → **block**; normalizer §5 forbids `Ready`.

## Mode notes

- **spec-normalizer:** pipeline step 4 before profile passes; re-run PASS-008 after id changes.
- **spec-generator:** avoid aggressive paraphrase merge in assembly.

## Integration with other passes

- **PASS-001:** primary weakening detector after dedup.
- **PASS-008:** registry/matrix must reflect deprecated ids.
- **PASS-009:** dedup safety dimension in readiness table.
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
