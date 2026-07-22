# Assistant Submode Router

## 1. Purpose

Select the correct assistant submode and pass/profile scope from user intent — no pass logic duplication.

## 2. Inputs

- user intent and artifact type (fragment, draft spec, normalized spec);
- `../../../shared/pass-loading-policy.md`;
- `../../../policies/mode-transition-guards.md`;
- `../../../router/router-map.md` (cross-mode intent).

## 3. Routing table

| User intent (examples) | Submode | Profile | Extra passes |
|---|---|---|---|
| Add/change/dictate a paragraph, bullet, section, behavior, or implementation entity | `fragment-capture` | none | PASS-002, PASS-003, PASS-011; conditional PASS-004/PASS-005 by slice |
| Full/deep/comprehensive proofreading / полная или глубокая вычитка / readiness or pre-implementation audit | `review-full` | `review-full.md` | none |
| Proofread / вычитка / редактура / проверь текст / find wording issues | `review-light` | `review-light.md` | none |
| Proofread and apply explicit fixes / вычитка и внеси правки | sequence: `review-light` then `fragment-capture` only for the explicit write scope | `review-light.md` for review step | PASS-002, PASS-003, PASS-011 for write step; conditional PASS-004/PASS-005 by slice |
| Need to implement / надо реализовать / нужен provider/model/config/controller/facade / что будем делать / какое решение принять inside spec work | `fragment-capture` on `SPECIFICATION_PATH` only | none | PASS-002, PASS-003, PASS-011; conditional PASS-004/PASS-005 by slice |
| Explicit implement/change project code inside spec work | blocked for project mutation; capture spec decision only if requested | none | none |
| Quick review, sanity check | `review-light` | `review-light.md` | none |
| Deep review, readiness check, compare versions | `review-full` | `review-full.md` | none |
| Ambiguous “review this” | `review-light` (default) | `review-light.md` | none |

## 4. Execution Steps

1. Classify intent (fragment / dictated-entity capture / implementation-intent-capture / proofreading-light-review / light review / full review / out of scope). Explicit full/deep/comprehensive/readiness wording takes precedence and selects `review-full`; otherwise proofreading selects `review-light`. Apply/write wording adds the later write step without lowering review depth. Treat implementation wording inside specification work as future-work capture in `SPECIFICATION_PATH`, not code implementation. Route named implementation entities through `fragment-capture` and its pre-write grounding gate.
2. If out of scope → `mode-transition-guards.md` (generator, normalizer, project context).
3. Load submode `SKILL.md` and pass scope per policy §4. Every semantic fragment route includes mandatory pre-write and post-write `PASS-011` boundary/coherence checks. Every review route selects a fresh isolated Codex worker through `../review-worker/SKILL.md` before the parent reads the complete specification.
4. Return chosen route: submode path + profile + extra pass IDs.
5. Remind executor: findings per §6; use required `USER_LANGUAGE`; IDs and project/machine identifiers are not translated; **review submodes = delegated read-only** on `SPECIFICATION_PATH` (`../../../policies/mode-transition-guards.md` §4.3). The parent validates/renders the bundle and does not repeat passes.

## 5. Conditional Gates

- Full generation from GDD → `../../spec-generator/SKILL.md`, not assistant.
- Normalize / implementation-ready IDs → `../../spec-normalizer/SKILL.md`.
- `warning`/`block` without findings in prior step → contract error; do not switch submode to hide it.

## 6. Output Contract

Brief routing record:

```text
Submode: <name>
Profile: <path or none>
Extra passes: PASS-00x, ...
Executor: <parent | isolated-codex-review-worker>
Escalation: <none | review-full | generator | normalizer>
```

## 7. Failure Handling

1. Intent conflicts with artifact → one critical clarifying question.
2. Proofreading wording without explicit depth → `review-light`, read-only; explicit full/deep/comprehensive/readiness wording → `review-full`, read-only. Do not route either directly to `fragment-capture` without apply/write intent.
3. Implementation wording inside specification work → `fragment-capture` writes only to `SPECIFICATION_PATH`; never mutate project code/assets/configs/tests/scenes.
4. Explicit code implementation request inside specification work → block project mutation and require a separate non-pipeline implementation request.
5. User wants both fragment edit and full review → sequence: fragment-capture (writes) then review-full (read-only report on updated artifact; state both scopes).
6. User wants proofreading plus explicit application → run/report review scope first, then apply only the explicit write-scoped fixes; ask one clarification question if the write scope is unclear.
7. Codex multi-agent/subagent mechanism unavailable → use the declared local read-only fallback; disclose it and never claim delegation occurred.

## 8. When Not Applicable

Executing the review or edit (delegated to chosen submode skill).
