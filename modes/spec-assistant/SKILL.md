---
name: spec-assistant-mode
description: >-
  Interactive specification work: fragment capture, targeted edits, and
  findings-first review without duplicating pass logic.
---

# Specification Assistant Mode

## 1. When to use

- fragment capture and targeted edits;
- review-light and review-full;
- resolve ambiguity before generator/normalizer.

**Not this mode:** first full spec from GDD (`spec-generator`); normalize-only (`spec-normalizer`).

## 2. Inputs

- `SPECIFICATION_PATH` (required; from orchestrator / command — see `../../SKILL.md` §2)
- `USER_LANGUAGE` (required; from orchestrator / command — see `../../SKILL.md` §2)
- optional `USER_REQUEST`
- `../../shared/specification-document-regulation.md`
- `../../shared/core-principles/system-thinking.md`
- `../../shared/core-principles/decomposition.md`
- `../../shared/core-principles/grounding.md`
- `../../shared/source-priority-policy.md`
- `../../shared/pass-loading-policy.md`
- `../../policies/mode-transition-guards.md`

## 3. Submodes

| Submode | Skill | Use when |
|---|---|---|
| Router | `./router/SKILL.md` | every assistant turn (select scope) |
| Fragment capture | `./fragment-capture/SKILL.md` | local add/change |
| Review light | `./review-light/SKILL.md` | fast review |
| Review full | `./review-full/SKILL.md` | deep review (§16 blocks) |

## 4. Execution Steps

1. Select submode via `./router/SKILL.md`.
2. Load pass/profile scope from `../../shared/pass-loading-policy.md` §4.
3. Run the selected submode; execute passes via `../../shared/passes/PASS-*.md` only.
4. Aggregate findings per `../../shared/pass-loading-policy.md` §6.
5. Return response per submode output contract (see §6). For **review** submodes: **read-only** on `SPECIFICATION_PATH` unless the user explicitly asks to apply fixes.

## 5. Conditional Gates

| Condition | Action |
|---|---|
| Full generation request | `spec-generator` |
| Normalize-only request | `spec-normalizer` |
| Mandatory pass `block` | `blocked` + findings |
| Pass `not applicable` | stated reason in report |

## 6. Output Contract

- Language: use required `USER_LANGUAGE` for chat and specification body content.
- Do not translate structural metadata or machine/project identifiers (`PASS-*`, `REQ-*`, `F-*`, `AC-*`, finding `id`, API names, file/folder names, class/method/variable names, namespaces, config keys, Unity/C# terms, code snippets).

| Submode | File I/O on `SPECIFICATION_PATH` | Chat structure |
|---|---|---|
| `fragment-capture` | write (local change per fragment protocol) | status → summary → what changed → follow-ups |
| `review-light`, `review-full` | **read-only** until user approves application | status → summary → findings → **proposed fixes (chat only)** → next step |

`warning` / `blocked` without findings are forbidden.

## 7. Failure Handling

1. Submode out of scope → `../../policies/mode-transition-guards.md`.
2. Mandatory pass `block` without findings → contract error.
3. Ambiguous routing → at most one critical question (via router).

## 8. When Not Applicable

First-time full generation from design source or normalize-only without assistant scope.
