# Generator Stage: Open Questions and Risks

## 1. Purpose

Surface **unknowns, assumptions, conflicts, and formal-execution risks** before assembly so the draft does not pretend certainty.

Passes when in scope per `../../../shared/pass-loading-policy.md` §4:

- `PASS-006` — `../../../shared/passes/PASS-006-edge-cases-and-testability.md`
- `PASS-007` — `../../../shared/passes/PASS-007-forbidden-shortcuts-and-constraints.md`

---

## 2. Classification (do not conflate)

### 2.1 Open Question

A question **without an answer the spec cannot fix precisely**.

Example:

```text
Open Question:
GDD does not state whether progress persists between sessions or resets each launch.
```

Use when: missing owner, missing parameter, unknown API, unknown persistence, unknown win condition.

**Placement:** every unresolved OQ is an `OQ-xxx` row in assembled **`## 11. Open Questions`** only — not under decomposition entities or as inline `TBD` (regulation §7.1, `decomposition.md` §5).

### 2.2 Assumption

A **minimal** default chosen only for document coherence.

Assumption is allowed only if **all** are true:

1. Without it, the document is unreadable or disconnected.
2. It is explicitly labeled `Assumption`.
3. It does **not** add a new gameplay mechanic.
4. The user can confirm or replace it later.

Example:

```text
Assumption:
If GDD defines no win condition, the mode is endless until lose or user exit.
```

**Never** embed assumption text inside requirement bullets.

### 2.3 Conflict

Two or more sources (or sections) disagree; resolution is **not** chosen silently.

Typical conflicts:

- Different win/lose conditions or parameter values.
- Different sources of truth for the same state.
- Instant mechanic vs visual flow requiring wait.
- UI shows data with no defined source.
- Tutorial demands action forbidden by core logic.
- Popup flow vs pause/endgame.
- Scoring described differently in two places.
- One term for two entities, or two terms for one entity.

**Handling:**

| Severity | Action |
|---|---|
| Critical | Finding + open question; do **not** write either side as sole requirement |
| Non-critical | Document both sides in issues; propose user decision |

Conflict formatting in the assembled doc → per `../../../shared/specification-document-regulation.md`.

### 2.4 Risk (finding)

Implementation risk with severity — use structured findings (`critical-risk`, `high`, etc.) per policy §6.

Distinct from Open Question: risk names a **known** failure mode; open question names **missing** information.

---

## 3. Formal execution risks

When a requirement can be satisfied **incorrectly but plausibly**, add implementation constraint or forbidden shortcut blocks per regulation — only when a **concrete** risk exists:

- Multiple valid implementations; easy one breaks architecture.
- Outcome looks correct but violates ownership/lifecycle/config direction.
- Agent may put gameplay checks in view or hardcode tunables.

Example pattern:

```text
Formal execution risk:
Requirement "highlight valid target" can be implemented in view.
Required fix: validity decided by logic system; view only displays result.
```

`PASS-007` owns shortcut/forbidden-solution semantics — reference by ID, do not duplicate checklist.

---

## 4. Edge cases and testability

`PASS-006` when user-facing flows exist. Capture:

- Missing failure/cancel/retry behavior.
- Untestable or placeholder acceptance wording.
- Derived edge cases implied by rules but not stated.

---

## 5. Registry structure (pre-assembly)

Maintain an internal registry (emit in assembled doc per regulation):

| Bucket | Entries |
|---|---|
| Open Questions | ID or bullet, blocking vs non-blocking — **unresolved only** (no “closed” archive; see regulation §7) |
| Assumptions | Labeled, minimal |
| Conflicts | Sources, sides, recommended user action |
| Risks | Linked finding IDs |
| Limitations | Scope or project-context gaps |

---

## 6. Stage execution steps

1. Scan extraction + mapping + flow/data drafts for gaps.
2. Classify each gap (§2) — no default bucket mixing.
3. Run `PASS-006`, `PASS-007` when applicable.
4. Add formal-execution risk blocks only where grounded.
5. Ensure no open question was “answered” by invention.
6. Assembly must not emit subsections such as “Closed decisions” or tables of resolved OQs — answers belong in canonical body sections per `../../../shared/specification-document-regulation.md` §7.

---

## 7. Stage gate

Assembly stage forbidden if:

- Critical conflicts unresolved and written as single-sided requirements, or
- Mandatory pass `block` without findings.

---

## 8. Output

| Field | Content |
|---|---|
| Stage status | `open-items-ok` \| `open-items-warning` \| `open-items-blocked` |
| Deliverable | Registry (open / assumption / conflict / risk) |
| Pass table | `PASS-006`, `PASS-007` when run |
| Findings | Per policy §6 |
| Language | Required `USER_LANGUAGE` |
