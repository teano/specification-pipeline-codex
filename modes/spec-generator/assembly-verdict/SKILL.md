# Generator Stage: Assembly and Verdict

## 1. Purpose

Assemble the full specification draft per `../../../shared/specification-document-regulation.md`, attach assumptions/open questions/risks, and emit generator readiness with pass aggregate.

## 2. Pre-assembly gate

All prior stages complete or explicitly `*-blocked` with findings:

| Stage | Skill |
|---|---|
| Intake | `./intake-gate/SKILL.md` |
| Extraction | `./grounded-extraction/SKILL.md` |
| Mapping | `./system-mapping/SKILL.md` |
| Flow/data | `./flow-data-modeling/SKILL.md` |
| Open items | `./open-questions-risks/SKILL.md` |

No silent skip of mandatory passes. Critical conflicts remain ISSUE/OQ — not single-sided requirements.

## 3. Assembly rules

1. Document structure follows regulation canonical sections (omit empty; no invented filler).
2. Mechanics live under grounded project/domain owners — no detached topical-only chapters and no abstract systems-thinking hierarchy with only formal `Grounded as` annotations.
3. §2 contains high-level project integration and boundaries only; concrete entity grounding belongs in §4/contract, not a separate grounding catalog.
4. Open Questions, Assumptions, Conflicts, Forbidden shortcuts per regulation and stage 5 output.
5. Run generator pass set per `../../../shared/pass-loading-policy.md` §4: `review-light` profile + `PASS-004`, `PASS-005`, `PASS-007`, `PASS-010`.
6. Compact pass table in chat when any pass ≠ `pass`.

## 4. Readiness labels

| Label | Meaning |
|---|---|
| `draft-ok` | All mandatory passes `pass`; no blocking OQ/conflict |
| `draft-warning` | Warnings with §6 findings; user review before build |
| `draft-blocked` | Any mandatory `block` or critical unresolved conflict |

Bare `draft-warning` / `draft-blocked` without findings → contract error.

## 5. Stage execution steps

1. Merge stage artifacts into one coherent draft.
2. Run profile + extra passes; collect findings.
3. Assign readiness label from pass aggregate (policy §8).
4. List blocking user decisions (OQ/ISSUE) at top of handoff.
5. Recommend next step: `review-light`, `review-full`, user decisions, or `spec-normalizer`.

## 6. Output Contract

| Field | Content |
|---|---|
| Status | `draft-ok` \| `draft-warning` \| `draft-blocked` |
| Body | Assembled specification (regulation shape) |
| Registry | Assumptions / open questions / conflicts / risks |
| Findings | §6 structured list |
| Pass table | ID + status (+ finding count) when not all `pass` |
| Next step | One clear recommendation |

Use required `USER_LANGUAGE`; structural metadata and machine/project identifiers remain unchanged.

## 7. Failure Handling

- Stage `extraction-blocked` or `mapping-blocked` → do not claim `draft-ok`; assemble partial only if user asked, with explicit gaps.
- PASS-003 `block` → `draft-blocked`.

## 8. When Not Applicable

Fragment edits or normalize-only (other modes).
