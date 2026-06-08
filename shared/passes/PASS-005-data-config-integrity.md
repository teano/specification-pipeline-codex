# PASS-005: Data and Config Integrity

## Purpose

Ensure data models, persistence, config keys, and repository-shaped requirements are complete, consistent, and implementation-bindable. Covers assistant data review and normalizer DATA slice (§10 Data Requirements, configs in decomposition).

Source basis: assistant data/config review; normalizer persistence and DATA slice; regulation §8 pointer.

## Activation / Not applicable

**Activate when:** persistence, storage, files, metadata, bundled config, or structured user state appears.

**Not applicable when:** no data/config/persistence slice (state reason).

**Required report if N/A:** one-line scope note.

## Checklist (numbered)

1. Entities list fields with types, cardinality, optional/required, and validation rules.
2. Persistence path named: what is saved, when, key/namespace, migration/compatibility note or OQ.
3. Config sources: bundled vs server vs local — match project external-config patterns or label Assumption.
4. No duplicate models for same logical record under different names (coordinate PASS-002).
5. Enum/value sets complete or explicit OQ for unknown values.
6. Read/write ownership matches PASS-004 (who may mutate persisted state).
7. Serialization shape described at requirement level (not code dump): nested objects, arrays, versioning.
8. Defaults and empty states: first-run behavior stated or OQ.
9. Normalizer: DATA reqs use REQ-* with `owner` and link to AC verification where blocking.
10. Sensitive fields (PII, tokens) called out with handling constraint or ISSUE.

## Failure signals

- “Saves progress” without what, where, or failure behavior.
- Config key referenced in UI but absent from data section.
- Two schemas for same player state without ISSUE.
- Repository key names drift between §5 and §10.

## Example finding templates

```text
[Data Model Gap]
Entity: <name>
Missing: <field | validation | relation>
Location: <section>
Recommended fix: extend §5/§10; add REQ-* + AC
```

```text
[Persistence Gap]
Trigger: <when save/load>
Missing: <storage target | conflict resolution | corrupt file>
Recommended fix: normative REQ + negative AC
```

Structured finding: `F-xxx | PASS-005 | high | problem | impact | location | recommended_fix`

## Output (link ../pass-loading-policy.md §6)

Report pass status: `pass` | `pass-with-warning` | `block` | `not applicable`.

- Data integrity **block** when blocking REQ lacks verifiable persistence contract.

## Mode notes

- **spec-generator:** flow-data-modeling stage owns first draft; PASS-005 validates before verdict.
- **spec-normalizer:** §10 mandatory when feature touches user state — do not fabricate large §10 if slice absent (policy note).

## Integration with other passes

- **PASS-003:** config claims need source or Assumption.
- **PASS-004:** save/load lifecycle triggers.
- **PASS-006:** placeholder enums break testability.
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
