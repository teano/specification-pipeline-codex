# Mode Transition Guards

## 1. Default route

If the artifact is unclear, use `spec-assistant`.

## 2. Clarification limit

Before starting a mode, allow at most one critical clarifying question.

## 3. Allowed transitions

| From | To | When |
|---|---|---|
| `spec-assistant` | `spec-generator` | user requests full generation |
| `spec-assistant` | `spec-normalizer` | explicit normalize-only request |
| `spec-generator` | `spec-assistant` | post-generation edits/review |
| `spec-generator` | `spec-normalizer` | request to normalize draft |
| `spec-normalizer` | `spec-assistant` | targeted fixes after normalize |

## 4. Transition Blocking Rules

1. generator is forbidden for targeted patch;
2. normalizer is forbidden for review-only;
3. **review-only is read-only on `SPECIFICATION_PATH`:** `review-light` and `review-full` must deliver findings and proposed fixes in chat only; forbidden to edit, patch, or rewrite the spec file unless the user explicitly requests application in the same or a follow-up message;
4. full rewrite is forbidden during fragment capture;
5. **no code/project mutations:** this pipeline is forbidden to create, edit, delete, move, rename, format, patch, or otherwise mutate source code, assets, configs, tests, generated project files, project metadata, or any non-documentation project file;
6. on unresolved source conflict, stay in current mode and raise an open question.

## 5. Depth policy

Wording may be shortened, but mandatory pass checks must not be skipped.

Activation matrix: `../shared/pass-loading-policy.md` §4.

## 6. Findings Escalation Guard

1. `warning`/`block` must include structured findings (see `../shared/pass-loading-policy.md` §6);
2. the mode layer must aggregate findings and show them to the user (status-only is forbidden);
3. `block` without findings is a contract error and forces outcome `blocked`;
4. when switching modes, unresolved findings keep the same `id`.

## 7. Normalizer Hard Gate

1. `spec-normalizer` cannot return `Ready` if `PASS-008` or `PASS-009` blocked a stage;
2. `Ready` is forbidden without confirmed machine addressability and traceability;
3. normalizer verdict must include `Blocking Findings IDs` when blocked.

See `../modes/spec-normalizer/SKILL.md`, `../modes/spec-normalizer/addressability-traceability/SKILL.md`, `../modes/spec-normalizer/anti-weakening-readiness/SKILL.md`.
