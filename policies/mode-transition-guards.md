# Mode Transition Guards

## 1. Default route

Apply `../shared/specification-target-resolution.md` before mode selection. If the action remains unclear after target resolution, use `spec-assistant` only after asking the one blocking question needed to distinguish specification work from implementation or another artifact.

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
5. **no code/project mutations:** this pipeline is forbidden to create, edit, delete, move, rename, format, patch, or otherwise mutate source code, assets, configs, tests, scenes, generated project files, project metadata, or any non-documentation project file;
6. **implementation intent is spec intent:** while this pipeline is active, wording such as `сделать`, `реализовать`, `надо сделать`, `нужно добавить`, `нужно изменить`, `что будем делать`, `какое решение принять`, `implement`, `build`, `add`, or `change` describes future implementer work and must be captured in `SPECIFICATION_PATH`; it never grants permission to touch project code/assets/configs/tests/scenes;
7. explicit requests to implement code inside a specification run must stop before project mutation and require a separate non-pipeline implementation request; the current run may only capture the spec decision/requirement if requested;
8. on unresolved source conflict, stay in current mode and raise an open question.
9. **review delegation:** explicit `review-light`, `review-full`, and proofreading routes must delegate to a fresh isolated Codex review subagent before the parent reads the complete specification whenever the multi-agent mechanism is available;
10. **review worker is read-only:** the worker may not mutate any file; only the parent may apply user-approved fixes through `fragment-capture`;
11. **revision guard:** finding application is forbidden when the current exact-byte SHA-256 differs from the reviewed bundle; re-review the current file first;
12. **honest fallback:** when subagent delegation is unavailable, run the same review locally under the read-only contract and disclose that the parent-context fallback was used.
13. **natural-language operation inference:** do not require literal `new` / `continue`; bind the inferred operation before entering a mode;
14. **existing-generation collision:** a generic generation request against an existing relevant spec must stop for regenerate-versus-continue choice unless the user already stated it;
15. **dictation continuity:** reuse a valid conversation-bound/unique spec; when absent, keep the dictated fragment pending and ask for a path or new-spec confirmation.

## 5. Depth policy

Wording may be shortened, but mandatory pass checks must not be skipped.

Activation matrix: `../shared/pass-loading-policy.md` §4.

## 6. Findings Escalation Guard

1. `warning`/`block` must include structured findings (see `../shared/pass-loading-policy.md` §6);
2. the mode layer must aggregate findings and show them to the user (status-only is forbidden);
3. `block` without findings is a contract error and forces outcome `blocked`;
4. when switching modes, unresolved findings keep the same `id`.
5. delegated findings must come from a validated review bundle; the parent must not rerun passes after accepting the bundle.

## 7. Normalizer Hard Gate

1. `spec-normalizer` cannot return `Ready` if `PASS-008` or `PASS-009` blocked a stage;
2. `Ready` is forbidden without confirmed machine addressability and traceability;
3. normalizer verdict must include `Blocking Findings IDs` when blocked.

See `../modes/spec-normalizer/SKILL.md`, `../modes/spec-normalizer/addressability-traceability/SKILL.md`, `../modes/spec-normalizer/anti-weakening-readiness/SKILL.md`.
