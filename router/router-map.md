# Specification Router Map

## 1. Purpose

This file routes requests by expected output artifact after `../shared/specification-target-resolution.md` resolves the internal `new` / `continue` operation and target.

It does not duplicate mode methodologies.

---

## 2. Mode Index

| Mode | Use when user expects | Mode entrypoint |
|---|---|---|
| `spec-assistant` | fragment capture, targeted edits, review/findings | `../modes/spec-assistant/SKILL.md` |
| `spec-generator` | first full specification from GDD/feature brief | `../modes/spec-generator/SKILL.md` |
| `spec-normalizer` | implementation-ready normalized specification | `../modes/spec-normalizer/SKILL.md` |

---

## 3. Fast Routing Table

| User intent | Route |
|---|---|
| "Add/fix/dictate this fragment or implementation entity in the spec" | `spec-assistant` → `fragment-capture` with pre-write grounding |
| "Full/deep/comprehensive proofreading / полная или глубокая вычитка / pre-implementation audit" | `spec-assistant` + delegated review-full via isolated Codex review subagent (**read-only**) |
| "Proofread / вычитка / редактура / проверь текст" | `spec-assistant` + delegated review-light via isolated Codex review subagent (**read-only**) |
| "Proofread and apply fixes / вычитка и внеси правки" | `spec-assistant`: delegated review-light first, then parent fragment-capture only for explicit write-scoped fixes |
| "Need to implement / надо реализовать / что будем делать / какое решение принять" inside specification work | `spec-assistant` + fragment-capture on `SPECIFICATION_PATH` only |
| "Implement/change project code" inside specification work | block project mutation; capture only the spec decision if requested; require a separate non-pipeline implementation request |
| "Review this spec quickly" | `spec-assistant` + delegated review-light via isolated Codex review subagent |
| "Review this spec deeply/full pass" | `spec-assistant` + delegated review-full via isolated Codex review subagent |
| "Generate a complete technical spec from GDD" | `spec-generator` |
| "Normalize into implementation-ready markdown" | `spec-normalizer` |

If intent is ambiguous, default route is `spec-assistant` with at most one critical clarifying question.

---

## 4. Specification file (orchestrator)

Before routing, the orchestrator must apply `../shared/specification-target-resolution.md` and set `TARGET_OPERATION` plus `SPECIFICATION_PATH` per `../SKILL.md` §2. Users are not required to name the operation.

| Route | File I/O on `SPECIFICATION_PATH` |
|---|---|
| `spec-assistant` → `review-light` / `review-full` | delegated **read-only** worker; parent receives compact bundle; apply only on explicit user request and matching reviewed revision |
| `spec-assistant` → `fragment-capture` | read + write |
| `spec-generator`, `spec-normalizer` | read + write |

Writes are still restricted to `SPECIFICATION_PATH`; during `new`, the
orchestrator may create its parent directory. Do not redirect writes mid-run.
Source code and project files are never write targets for this pipeline.

---

## 5. Mandatory Shared Layers

The selected executor must load:

* `../shared/specification-document-regulation.md`;
* `../shared/core-principles/system-thinking.md`;
* `../shared/core-principles/decomposition.md`;
* `../shared/core-principles/grounding.md`;
* `../shared/source-priority-policy.md`;
* `../shared/pass-loading-policy.md`;
* `../policies/mode-transition-guards.md`.

For delegated review, the parent loads only `../modes/spec-assistant/review-worker/SKILL.md` before dispatch. The isolated Codex worker loads the shared layers/profile/pass files and the complete specification.

---

## 6. Routing Safety Rules

1. choose by artifact type, not by input file type only;
2. do not switch to generator if the user asks for a targeted update;
3. do not switch to normalizer when the user asks only for review;
4. do not edit `SPECIFICATION_PATH` during review-only routes (`review-light`, `review-full`) unless the user explicitly asks to apply fixes;
5. treat proofreading wording (`вычитка`, `proofread`, `редактура`, `проверь текст`, similar) as review-only unless an explicit write/apply verb is present in the same request; explicit full/deep/comprehensive/readiness depth takes precedence and selects `review-full`, otherwise select `review-light`;
6. treat implementation wording (`сделать`, `реализовать`, `надо сделать`, `нужно добавить`, `нужно изменить`, `что будем делать`, `какое решение принять`, `implement`, `build`, `add`, `change`, similar) inside specification work as a request to capture future implementation requirements/decisions in `SPECIFICATION_PATH`, not as permission to mutate project files;
7. do not create, edit, delete, move, rename, format, patch, or otherwise mutate source code or project files;
8. do not ask the user to choose a mode when the route is obvious;
9. route only to `spec-assistant`, `spec-generator`, or `spec-normalizer`.
10. delegate explicit review/proofreading before the parent reads the complete specification; never simulate the worker in the parent while the Codex multi-agent mechanism is available;
11. apply reviewed findings only when the current exact-byte SHA-256 matches the bundle revision; otherwise re-review.
12. infer `new` for generation when no relevant specification exists; if one exists, require an explicit regenerate-versus-continue choice before writing;
13. reuse the conversation-bound or uniquely relevant specification for dictation; when none exists, preserve the fragment and ask for a target or new-spec confirmation;
14. never reject natural-language intent merely because literal `new` / `continue` syntax is absent.

---

## 7. Scenario-to-Pass Matrix

Canonical source: `../shared/pass-loading-policy.md` §4. Do not redefine pass semantics here.

| Scenario | Mode | Profiles | Extra passes | Effective set |
|---|---|---|---|---|
| Fragment capture | `spec-assistant` | none | `PASS-002`, `PASS-003`, `PASS-011`; conditional `PASS-004` / `PASS-005` by slice | terminology + immediate grounding + boundary/coherence + applicable entity-contract checks |
| Review-light | `spec-assistant` | `review-light` | none | profile set |
| Review-full | `spec-assistant` | `review-full` | none | profile set |
| Generator run | `spec-generator` | `review-light` | `PASS-004`, `PASS-005`, `PASS-007`, `PASS-010` | light + generation safety |
| Normalizer run | `spec-normalizer` | `review-full` | `PASS-008`, `PASS-009`, `PASS-010` | full + hard gate + readiness |

Conditional `not applicable` (reason required): same file §4 table. `PASS-011` is not applicable only for confirmed editorial-only zero-semantic-change work; it is mandatory for semantic fragments and generator extraction/mapping.

Validated scenarios: `./scenario-validation.md` (happy path 1–5; edge 6–9; escalation 10–12).

---

## 8. Cross-Reference Index

After route selection, resolve pass/profile scope from:

| Layer | File | Role |
|---|---|---|
| Scenario matrix | `../shared/pass-loading-policy.md` §4 | mode → profile → extra passes |
| Review profiles | `../review-profiles/review-light.md`, `../review-profiles/review-full.md` | ordered pass IDs only |
| Assistant submodes | `../modes/spec-assistant/router/SKILL.md` | fragment / review-light / review-full |
| Review delegation | `../modes/spec-assistant/review-worker/SKILL.md` | isolated worker dispatch, bundle/revision validation, approved-fix handoff |
| Validated scenarios | `./scenario-validation.md` | coherence checks + edge/escalation cases (incl. 10–12) |
| Pass semantics | `../shared/passes/*` | atomic checks (DRY — not duplicated in modes) |
| Findings escalation | `../shared/pass-loading-policy.md` §6 | structured findings for warning/block |
| Assistant escalation | `../modes/spec-assistant/router/SKILL.md` §4 | review-light → review-full triggers |
| Conditional slices | `../shared/pass-loading-policy.md` §4 | source slice → pass activation table |

User documentation: `../references/command-specification-help.md`.
