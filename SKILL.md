---
name: skill-specification-pipeline
description: >-
  Global Codex specification workflow for creating, continuing, reviewing,
  proofreading, capturing implementation intent as spec text, generating, and
  normalizing markdown technical specifications. Use when the user invokes
  $skill-specification-pipeline, asks to run
  command-specification, creates a new specification, continues an existing
  specification.md file, adds requirement fragments, requests proofreading, light
  or full specification review, generates a complete technical spec from source
  material, or normalizes a spec into implementation-ready markdown. Infers new
  versus continue from natural language, resolves SPECIFICATION_PATH, and
  requires USER_LANGUAGE before mode routing. Strict
  documentation-only write scope: never mutates source code or project files.
---

# Skill: Specification Pipeline

## 1. Purpose

Own the full specification workflow in Codex:

1. resolve or create one markdown specification file;
2. detect the user's natural language;
3. route the request across assistant, generator, and normalizer modes;
4. load only the relevant regulation, principles, profiles, and passes;
5. edit only the resolved specification file when the routed mode allows writes;
6. enforce `USER_LANGUAGE` compliance for every user-facing response;
7. never create, edit, delete, move, rename, format, or patch source code or project files.
8. isolate read-only review/proofreading so complete-document analysis does not consume the parent conversation context.

This is the Codex-global variant of the Cursor command + skill package. Do not
invoke Cursor slash commands. Treat this skill folder as the process root.

## 2. Flexible invocation

Accept natural-language requests as the default interface. Infer the internal operation and target through `shared/specification-target-resolution.md`.

These explicit forms remain optional shortcuts:

```text
$skill-specification-pipeline continue <path-to-specification.md> [-- <work request>]
$skill-specification-pipeline new "<specification-title>" <parent-directory> [-- <work request>]
```

Also trigger this skill implicitly when the user asks for specification creation,
spec continuation, requirement capture, spec review, spec generation, or spec
normalization and the task matches the description.

## 3. Resolve the request before routing

Apply `shared/specification-target-resolution.md`. Read-only target discovery may run before bindings exist; do not run router, pass, profile, or mode work until `TARGET_OPERATION`, `SPECIFICATION_PATH`, and `USER_LANGUAGE` are resolved.

### Optional explicit continue shortcut

For:

```text
continue <path-to-specification.md> [-- <work request>]
```

Rules:

1. `<path-to-specification.md>` must be repo-relative or absolute, end with `.md`, and exist on disk.
2. If the file is missing or unreadable, stop and ask the user for a valid path.
3. Set `SPECIFICATION_PATH` to the resolved path.
4. Set `SPECIFICATION_DIR` to the parent directory of `SPECIFICATION_PATH`.
5. Set `SPECIFICATION_TITLE` from the first document `#` heading when present.

### Optional explicit new shortcut

For:

```text
new "<specification-title>" <parent-directory> [-- <work request>]
```

Rules:

1. `<specification-title>` is the human title for the document `#` heading and filename slug.
2. `<parent-directory>` is the folder that will contain the new file; create it when it does not exist.
3. Derive `SPECIFICATION_SLUG` from the title: lowercase; trim; replace spaces/underscores with `-`; keep only `[a-z0-9-]`; collapse repeated `-`; trim leading/trailing `-`.
4. If the slug is empty, stop and ask for a valid title.
5. Set `SPECIFICATION_DIR = <parent-directory>`.
6. Set `SPECIFICATION_PATH = <parent-directory>/<SPECIFICATION_SLUG>.md`.
7. If `SPECIFICATION_PATH` already exists, never overwrite silently. Ask whether to regenerate/replace it or continue/complete it unless the user already chose explicitly.
8. Create the file as UTF-8 without BOM and LF line endings. Starter body: `# <specification-title>` plus the section headings from `shared/specification-document-regulation.md` section 5. Leave sections empty unless the user supplied grounded source material.

### Natural-language resolution

Do not reject a request because it lacks `new` / `continue`. Apply these rules:

1. generate + no relevant spec → infer `new`; ask only for a location/title that cannot be inferred safely;
2. generate + existing relevant spec → ask whether to regenerate from scratch or continue/complete it;
3. dictation + valid bound/unique relevant spec → infer `continue`;
4. dictation + no spec → preserve the fragment and ask for a path or permission to create a new spec;
5. review/normalize + existing target → infer `continue`; without one, ask for the path;
6. multiple candidates or unclear action → ask one minimal blocking question with concrete candidates/options.

Never invent a weak target, select among multiple plausible specs silently, overwrite an existing specification, or discard dictated content.

If `--` is present, everything after it is `USER_REQUEST`. If `--` is absent,
treat the trailing natural-language text as `USER_REQUEST` when unambiguous.

### Proofreading And Edit Intent Terms

Before choosing a write-capable route, classify proofreading wording explicitly.

Rules:

1. Treat `вычитка`, `proofread`, `proofreading`, `редактура`, `проверь текст`, `проверь спецификацию`, `найди проблемы`, and similar wording as review intent by default.
2. A proofreading-only request routes to `spec-assistant` → `review-light` by default and is read-only on `SPECIFICATION_PATH`. Explicit depth wording such as `полная вычитка`, `глубокая вычитка`, `комплексная проверка`, `full/deep/comprehensive review`, or readiness/pre-implementation audit takes precedence and routes to `review-full`.
3. Route to a write-capable assistant edit only when the same request contains an explicit write/apply verb such as `внеси правки`, `исправь в файле`, `примени`, `apply`, `patch`, or `rewrite/update this section`. This adds a later write step and does not lower the selected review depth.
4. If the request combines proofreading and write intent, run/plan the review scope first and apply only the explicitly requested fixes. If the write scope is unclear, ask at most one critical clarification question before editing.
5. Do not infer permission to patch from “сделай вычитку” alone.

### Implementation Intent During Specification Work

When this pipeline is active, implementation wording describes future work for an implementer agent and must be captured in the specification. It is not permission to edit project code or assets.

Rules:

1. Treat wording such as `сделать`, `реализовать`, `надо сделать`, `нужно добавить`, `нужно изменить`, `что будем делать`, `какое решение принять`, `зафиксируй решение`, `implement`, `build`, `add`, or `change` as specification intent when it appears inside a specification request.
2. Capture that intent in `SPECIFICATION_PATH` as the appropriate artifact: confirmed requirement, implementation constraint, mandatory approach, forbidden formal solution, explicit decision, proposal/assumption, open question, or risk/issue.
3. Do not create, edit, delete, move, rename, format, patch, or otherwise mutate source code, assets, configs, tests, scenes, generated files, project metadata, or any non-documentation project file during specification work.
4. If the user explicitly asks to implement code while the specification pipeline is active, stop before project mutation and state that implementation requires a separate non-pipeline request after the spec decision is captured or approved.
5. Do not infer permission to touch project files from “надо реализовать”, “что будем делать”, or “какое решение принять” alone.
6. Ground every named implementation entity during fragment capture. For providers, models, configs, controllers, facades, repositories, adapters, and similar roles, inspect project rules and analogues to resolve the project-shaped name, interface/contract, placement, creation/composition, registration/lifetime, dependencies, and ownership before normative insertion. If critical evidence is missing or contradictory, add a focused `OQ-xxx` and omit the abstract entity.
7. Run `PASS-011` before and after each semantic fragment to detect hidden system boundaries, incoherent responsibilities, duplicate capability owners, and existing project systems that must be reused.

## 4. Determine User Language

Before routing, determine `USER_LANGUAGE`.

Rules:

1. Use the dominant natural language in `USER_REQUEST`; if empty, use the surrounding user message or the new specification title.
2. For `continue` with no usable request text, inspect the existing specification body and use the dominant non-metadata natural language.
3. Ignore project naming when detecting language: API names, file/folder names, class/method/variable names, Unity/C# terms, IDs, and code snippets do not decide `USER_LANGUAGE`.
4. If language cannot be determined confidently, stop and ask the user to specify it.
5. Store a human-readable language name, for example `English`, `Russian`, or `Spanish`.

## 5. Mandatory Runtime Bindings

| Binding | Requirement |
|---|---|
| `TARGET_OPERATION` | inferred or explicit `new` / `continue` |
| `TARGET_RESOLUTION_SOURCE` | source defined by `shared/specification-target-resolution.md` |
| `SPECIFICATION_PATH` | resolved readable `.md` file, or confirmed non-existing target when `TARGET_OPERATION=new` |
| `SPECIFICATION_DIR` | parent directory of `SPECIFICATION_PATH`; may be created only for inferred/explicit `new` |
| `SPECIFICATION_TITLE` | first `#` title from the file, else the `new` title |
| `USER_REQUEST` | text after `--` or trailing free-text work intent |
| `USER_LANGUAGE` | detected user language |
| `GAMEDEV_HELPER_REQUEST_PATH` | controller-issued immutable request; required only for a GameDev helper run |
| `GAMEDEV_SPECIFICATION_CONTROLLER_PATH` | exact resolved GameDev specification controller entrypoint; required with `GAMEDEV_HELPER_REQUEST_PATH`, must match that request's path/SHA binding, and is never inferred by this skill |

Hard rules:

1. If `SPECIFICATION_PATH` is initially missing, run target resolution. If it remains ambiguous/unavailable, ask one minimal blocking question and do not run modes.
2. If `USER_LANGUAGE` is missing or ambiguous, stop and ask for the language.
3. Filesystem writes are limited to creating `SPECIFICATION_DIR` during `new` and creating/editing `SPECIFICATION_PATH` when the routed mode allows writes.
4. Do not create, edit, delete, move, rename, format, patch, or otherwise mutate source code, assets, configs, tests, generated project files, project metadata, or any non-documentation project file.
5. If the user requests implementation/code/project changes inside a pipeline request, stop and state that those changes require a separate non-pipeline request.
6. Another documentation target requires a separate pipeline invocation with its own `SPECIFICATION_PATH`; do not redirect writes mid-run.
7. Review routes (`review-light`, `review-full`) are read-only on `SPECIFICATION_PATH` until the user explicitly asks to apply fixes.
8. Proofreading-only wording is a review route, not a fragment-capture route.
9. Implementation wording inside specification work is a request to update the spec, not to implement code or mutate project files.
10. In the parent executor, delegate `review-light`, `review-full`, proofreading, and post-fix verification through `modes/spec-assistant/review-worker/SKILL.md` to a fresh Codex subagent with clean context. An executor marked `REVIEW_EXECUTOR_ROLE=worker` executes locally and never delegates again.
11. On explicit review routes, the parent must not read the complete specification, core principles, profiles, or pass files before delegation. It may verify readability, compute exact-byte SHA-256, and pass concise bindings/paths only.
12. The review worker is strictly read-only and returns a compact validated bundle. The parent remains the only writer after explicit user approval of findings.
13. Never apply findings when the current SHA-256 differs from the reviewed revision. Re-review first. If subagent execution is unavailable, use the declared local fallback and disclose its parent-context cost.
14. For generation, infer `new` when no relevant spec exists. If a relevant spec exists and rewrite versus continuation is unstated, ask before writing; never overwrite silently.
15. For dictation, reuse the current conversation-bound or unique relevant spec. If none exists, preserve the fragment and ask for a path or new-spec confirmation; do not require repetition.

### GameDev helper request

When the caller supplies `GAMEDEV_HELPER_REQUEST_PATH`, require the paired
`GAMEDEV_SPECIFICATION_CONTROLLER_PATH` to match the request's exact resolved
controller path and SHA-256 binding and read
[`references/gamedev-helper-sidecar.md`](references/gamedev-helper-sidecar.md)
before the selected write-capable mode. This is the sole exception that permits
the helper-owned report, coverage, and result-sidecar paths named by a valid
request in addition to `SPECIFICATION_PATH`. It does not change mode routing,
stage/pass execution, pass applicability, or semantic findings. The controller
binding is used only for the mandatory read-only output preflight that must pass
before the immutable PASS result sidecar is created. The emitter rejects a
missing or mismatched request binding before launching any controller.

## 6. Package Layout

Use only this skill package as the process root:

```text
skill-specification-pipeline/
  SKILL.md
  router/router-map.md
  router/scenario-validation.md
  shared/
    specification-document-regulation.md
    specification-target-resolution.md
    source-priority-policy.md
    pass-loading-policy.md
    core-principles/
      system-thinking.md
      decomposition.md
      grounding.md
    passes/
  review-profiles/
  modes/
    spec-assistant/
      review-worker/SKILL.md
      ...
    spec-generator/...
    spec-normalizer/...
  policies/mode-transition-guards.md
  references/
    command-specification.md
    command-specification-help.md
```

Rules:

1. Resolve package references relative to this `SKILL.md`.
2. Do not use `.cursor/skills/skill-specification-pipeline/...` paths unless the user explicitly asks to inspect the original Cursor source package.
3. Load `references/command-specification-help.md` only when the user asks for command help or gives an invalid/incomplete invocation.

## 7. Runtime Flow

For each request:

1. Apply `shared/specification-target-resolution.md`: infer `TARGET_OPERATION`, discover/reuse the target, and ask at most one blocking question only when necessary. Then resolve/create `SPECIFICATION_PATH` and detect `USER_LANGUAGE`. For explicit review, verify readability and compute SHA-256 without reading the complete file in the parent.
2. Classify intent via `router/router-map.md` using `USER_REQUEST`. Route explicit review intent before full-file loading.
3. Apply `policies/mode-transition-guards.md`.
4. Apply `shared/source-priority-policy.md` in the selected executor. For delegated review, the parent passes only source paths and concise decision delta; the worker loads the policy.
5. For local work, load regulation and all core principles. For delegated review, the parent loads only `modes/spec-assistant/review-worker/SKILL.md`; the worker loads regulation, principles, profile, and passes.
6. Load pass/profile scope via `shared/pass-loading-policy.md` in the selected executor.
7. Run the selected mode wrapper:
   - `modes/spec-assistant/SKILL.md`
   - `modes/spec-generator/SKILL.md`
   - `modes/spec-normalizer/SKILL.md`
8. Delegated review returns a validated compact bundle; the parent must not repeat pass execution. Aggregate findings per `shared/pass-loading-policy.md` section 6. Bare block/warning output is forbidden.
9. Before any user-facing response, run the final language compliance gate from `shared/pass-loading-policy.md` section 9.

## 8. File I/O And Encoding

Follow the active repository instructions first (`AGENTS.md`, nested guidance,
and project encoding rules). If no stricter local rule exists, all markdown
created or edited by this skill must be UTF-8 without BOM and LF line endings.

Documentation boundary: this skill may write only `SPECIFICATION_PATH`; during
`new`, it may also create the parent directory that contains that file. It must
not mutate code or project files outside that documentation boundary.

If the encoding of an existing specification file is uncertain, stop and ask
before rewriting it. Preserve existing line endings when editing an existing
file unless the active repo guidance explicitly requires LF for workflow docs.

## 9. Final Instruction

Route all specification requests only through this package. Never run without
`SPECIFICATION_PATH` and `USER_LANGUAGE`.

Use `USER_LANGUAGE` for user-facing chat and for specification body content. Do
not translate structural specification metadata or machine/project identifiers:
section structure required for navigation, front matter keys, `PASS-*`, `REQ-*`,
`AC-*`, finding `id`, API names, file/folder names, class/method/variable names,
namespaces, config keys, Unity/C# terms, and code snippets.

Before every final response, run the language compliance gate in
`shared/pass-loading-policy.md` section 9. Human-facing headings, table headers,
finding field labels, review block names, status captions, and next-step labels
must be written in `USER_LANGUAGE`. English labels in mode templates are semantic
placeholders, not literal output text.
