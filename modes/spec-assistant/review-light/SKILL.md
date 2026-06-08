# Assistant Submode: Review Light

## 1. Purpose

Fast findings-first quality check and explicit risks before deeper review or implementation.

**Read-only contract:** do **not** edit `SPECIFICATION_PATH` during this submode. Report findings and proposed fixes in chat; apply changes only after the user explicitly requests (e.g. “apply F-002”, “внеси правки”). See `../../../policies/mode-transition-guards.md` §4.3.

## 2. Inputs

- `../../../review-profiles/review-light.md`
- `../../../shared/pass-loading-policy.md` §4–§6
- Pass files referenced by the light profile only

## 3. Mandatory Pass Activation

Pass set is defined solely by `../../../review-profiles/review-light.md` and matrix `../../../shared/pass-loading-policy.md` §4.

Do not copy pass checklists into this file.

## 4. Execution Steps

1. Establish comparison baseline when PASS-001 or PASS-003 is in profile scope.
2. Run profile pass IDs in order; record status and §6 findings.
3. On `critical` / `high` density or scope-critical gap → recommend `review-full` with same finding IDs.
4. Keep output compact per `../../../shared/pass-loading-policy.md` §5 (findings-first, no checklist dump).

## 5. Conditional Gates

| Condition | Action |
|---|---|
| Local scope, no high-risk slices | Compact format |
| Multiple `high` / `critical` findings | Escalate to `review-full` |
| `not applicable` | Explicit reason only |
| User asked “deep review” | Route to `review-full` |

## 6. Output Contract

1. **Status:** `ok` | `warning` | `blocked`
2. **Summary** (1–2 sentences)
3. **Findings** (by priority, §6 structure)
4. **Proposed fixes** (chat only — suggested wording or minimal patch description per finding ID; **do not** write to the spec file)
5. **At most one** blocking question
6. **Next step** (e.g. offer to apply selected fixes after user approval)

`warning` / `blocked` without findings are forbidden.

## 7. Failure Handling

1. Pass `warning`/`block` without findings → contract error; do not finalize.
2. Light review reveals API/lifecycle/data gaps → cite PASS ID and recommend `review-full` or user decision.

## 8. When Not Applicable

Implementation-ready deep audit → `review-full`. Normalize-only → `spec-normalizer`.
