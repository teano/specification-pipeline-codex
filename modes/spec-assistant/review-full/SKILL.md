# Assistant Submode: Review Full

## 1. Purpose

Deep findings-first review before implementation. Uses profile `../../../review-profiles/review-full.md` plus extended review lenses migrated from assistant §16 and §15.

**Read-only contract:** do **not** edit `SPECIFICATION_PATH` during this submode. Report findings and proposed fixes in chat; apply changes only after the user explicitly requests (e.g. “apply block 7 / F-003”, “внеси правки”). See `../../../policies/mode-transition-guards.md` §4.3.

## 2. Inputs

- `../../../review-profiles/review-full.md`
- `../../../shared/pass-loading-policy.md` §4–§6
- Pass files under `../../../shared/passes/` (semantics only — do not copy checklists here)

## 3. Mandatory Pass Activation

Load every pass ID listed in `review-full.md` per `../../../shared/pass-loading-policy.md` §4.

Typical full profile adds: `PASS-004`, `PASS-005`, `PASS-006`, `PASS-007`, `PASS-010` after light-profile passes.

For each pass: run checklist in pass file → aggregate status → emit §6 findings for any `pass-with-warning` or `block`.

## 4. Execution Steps

1. Confirm baseline: prior spec, source excerpt, or user-confirmed fragments for PASS-001/PASS-003.
2. Run passes in profile order; record `pass` | `pass-with-warning` | `block` | `not applicable` + reason.
3. Map findings to §16 blocks below (omit empty blocks).
4. Group by severity: critical → high → medium → risks → missing → duplicate.
5. Propose targeted fixes per finding in chat only (not generic rewrite; **do not** patch the spec file).
6. Emit output contract (§5) with pass summary table when any pass is not `pass`.

## 5. Output Contract (template)

1. **Status:** `ok` | `warning` | `blocked`
2. **Summary** (1–3 sentences)
3. **Pass summary** (compact table: pass ID, status, finding count)
4. **Findings** (structured list per `../../../shared/pass-loading-policy.md` §6)
5. **Review sections** (§16 blocks — findings-first within each)
6. **Proposed fixes** (chat only — per finding ID; no file mutation)
7. **Next step** (e.g. offer to apply selected fixes after user approval)

Use required `USER_LANGUAGE`. Do not translate machine IDs or project identifiers (`PASS-*`, `REQ-*`, `F-*`, API names, file/folder names, class/method/variable names, namespaces, config keys, Unity/C# terms, code snippets).

`warning` / `blocked` without findings are forbidden.

## 6. §16 Review skeleton (blocks 1–13)

Use these headings when findings exist. **Omit** a block if there are no items of that type. For short user requests, group by priority but still run all mandatory passes.

### Block 1 — Critical problems

```text
[Critical] <title>
Location: <section / element ID>
Why: ...
Recommended fix: ...
```

### Block 2 — Architectural risks

```text
[Risk] ...
Formal execution risk: ...
How to close: mandatory approach / forbidden solution / AC
```

### Block 3 — Imprecision and weak wording

```text
[Medium] ...
Current wording: ...
Suggested wording: ...
```

### Block 4 — Missing items

```text
[Missing] ...
Why clarification is needed: ...
Question for user: ...
```

### Block 5 — Duplicates and structure

```text
[Duplicate] ...
Occurs in: ...
Canonical source of truth: ...
(PASS-010 if merge risk)
```

### Block 6 — Safe to leave unchanged

Brief list of areas reviewed and found acceptable (no filler).

### Block 7 — Proposed fixes (chat only)

Ordered, minimal edit proposals tied to finding IDs. **Do not** apply to `SPECIFICATION_PATH` until the user explicitly requests.

### Block 8 — Anti-weakening (PASS-001)

```text
[Weakening] / [Possible Weakening]
Was: ...
Now: ...
Why weaker: ...
Fix: ...
```

### Block 9 — API / lifecycle contract gaps (PASS-004)

```text
[Missing API Contract] ...
[Lifecycle Trigger Loss] ...
[Missing Lifecycle Trigger] ...
```

### Block 10 — Responsibility / ownership conflicts (PASS-004)

```text
[Responsibility Conflict]
Entity: ...
Side A: ...
Side B: ...
Fix: single owner or explicit split
```

### Block 11 — Testability gaps (PASS-006)

```text
[Testability Gap]
Problem: ...
Why it matters: ...
Fix: test strategy / user-approved values
```

### Block 12 — Flexibility clause issues (PASS-007)

```text
[Flexibility Clause Lost]
Was: ...
Now: ...
Fix: label semantic vs exact contract
```

### Block 13 — Derived edge cases (PASS-006)

```text
[Derived Edge Case]
Scenario: ...
Why it arises: ...
Undefined: ...
Question: ...
```

## 7. Failure Handling

- Contract error if any mandatory pass reports `warning`/`block` without §6 findings.
- If scope exceeds assistant (full normalize, traceability build), route per `../../../policies/mode-transition-guards.md` — do not impersonate normalizer.
- Multiple critical findings → recommend user decisions before implementation.

## 8. When Not Applicable

Quick scan or single-section touch → `review-light`. Normalize-only → `spec-normalizer`.
