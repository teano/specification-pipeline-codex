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
| Add/change a paragraph, bullet, section | `fragment-capture` | none | PASS-002, PASS-003 |
| Quick review, sanity check | `review-light` | `review-light.md` | none |
| Deep review, readiness check, compare versions | `review-full` | `review-full.md` | none |
| Ambiguous “review this” | `review-light` (default) | `review-light.md` | none |

## 4. Execution Steps

1. Classify intent (fragment / light review / full review / out of scope).
2. If out of scope → `mode-transition-guards.md` (generator, normalizer, project context).
3. Load submode `SKILL.md` and pass scope per policy §4.
4. Return chosen route: submode path + profile + extra pass IDs.
5. Remind executor: findings per §6; use required `USER_LANGUAGE`; IDs and project/machine identifiers are not translated; **review submodes = read-only** on `SPECIFICATION_PATH` (`../../../policies/mode-transition-guards.md` §4.3).

## 5. Conditional Gates

- Full generation from GDD → `../spec-generator/SKILL.md`, not assistant.
- Normalize / implementation-ready IDs → `../spec-normalizer/SKILL.md`.
- `warning`/`block` without findings in prior step → contract error; do not switch submode to hide it.

## 6. Output Contract

Brief routing record:

```text
Submode: <name>
Profile: <path or none>
Extra passes: PASS-00x, ...
Escalation: <none | review-full | generator | normalizer>
```

## 7. Failure Handling

1. Intent conflicts with artifact → one critical clarifying question.
2. User wants both fragment edit and full review → sequence: fragment-capture (writes) then review-full (read-only report on updated artifact; state both scopes).

## 8. When Not Applicable

Executing the review or edit (delegated to chosen submode skill).
