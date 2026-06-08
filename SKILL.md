---
name: skill-specification-pipeline
description: >-
  Global Codex specification workflow for creating, continuing, reviewing,
  generating, and normalizing markdown technical specifications. Use when the
  user invokes $skill-specification-pipeline, asks to run command-specification,
  creates a new specification, continues an existing specification.md file,
  adds requirement fragments, requests light or full specification review,
  generates a complete technical spec from source material, or normalizes a spec
  into implementation-ready markdown. Requires a resolved SPECIFICATION_PATH and
  detected USER_LANGUAGE before routing. Strict documentation-only write scope:
  never mutates source code or project files.
---

# Skill: Specification Pipeline

## 1. Purpose

Own the full specification workflow in Codex:

1. resolve or create one markdown specification file;
2. detect the user's natural language;
3. route the request across assistant, generator, and normalizer modes;
4. load only the relevant regulation, principles, profiles, and passes;
5. edit only the resolved specification file when the routed mode allows writes;
6. never create, edit, delete, move, rename, format, or patch source code or project files.

This is the Codex-global variant of the Cursor command + skill package. Do not
invoke Cursor slash commands. Treat this skill folder as the process root.

## 2. Invocation Formats

Prefer these explicit forms:

```text
$skill-specification-pipeline continue <path-to-specification.md> [-- <work request>]
$skill-specification-pipeline new "<specification-title>" <parent-directory> [-- <work request>]
```

Also trigger this skill implicitly when the user asks for specification creation,
spec continuation, requirement capture, spec review, spec generation, or spec
normalization and the task matches the description.

## 3. Parse The Request Before Routing

Do not run router, pass, profile, or mode work until `SPECIFICATION_PATH` and
`USER_LANGUAGE` are resolved.

### Continue Existing Specification

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

### Create New Specification

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
7. If `SPECIFICATION_PATH` already exists, stop and tell the user to use `continue` or choose another title/directory.
8. Create the file as UTF-8 without BOM and LF line endings. Starter body: `# <specification-title>` plus the section headings from `shared/specification-document-regulation.md` section 5. Leave sections empty unless the user supplied grounded source material.

### Invalid Or Incomplete Invocation

If the request does not provide enough information to resolve a concrete
specification file, stop and show the two invocation formats above. Do not invent
a target path.

If `--` is present, everything after it is `USER_REQUEST`. If `--` is absent,
treat the trailing natural-language text as `USER_REQUEST` when unambiguous.

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
| `SPECIFICATION_PATH` | resolved readable `.md` file; newly created only via `new` |
| `SPECIFICATION_DIR` | parent directory of `SPECIFICATION_PATH`; may be created only by `new` |
| `SPECIFICATION_TITLE` | first `#` title from the file, else the `new` title |
| `USER_REQUEST` | text after `--` or trailing free-text work intent |
| `USER_LANGUAGE` | detected user language |

Hard rules:

1. If `SPECIFICATION_PATH` is missing, not a `.md` file, or unreadable, stop.
2. If `USER_LANGUAGE` is missing or ambiguous, stop and ask for the language.
3. Filesystem writes are limited to creating `SPECIFICATION_DIR` during `new` and creating/editing `SPECIFICATION_PATH` when the routed mode allows writes.
4. Do not create, edit, delete, move, rename, format, patch, or otherwise mutate source code, assets, configs, tests, generated project files, project metadata, or any non-documentation project file.
5. If the user requests implementation/code/project changes inside a pipeline request, stop and state that those changes require a separate non-pipeline request.
6. Another documentation target requires a separate pipeline invocation with its own `SPECIFICATION_PATH`; do not redirect writes mid-run.
7. Review routes (`review-light`, `review-full`) are read-only on `SPECIFICATION_PATH` until the user explicitly asks to apply fixes.

## 6. Package Layout

Use only this skill package as the process root:

```text
skill-specification-pipeline/
  SKILL.md
  router/router-map.md
  router/scenario-validation.md
  shared/
    specification-document-regulation.md
    source-priority-policy.md
    pass-loading-policy.md
    core-principles/
      system-thinking.md
      decomposition.md
      grounding.md
    passes/
  review-profiles/
  modes/
    spec-assistant/...
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

1. Resolve or create `SPECIFICATION_PATH`; detect `USER_LANGUAGE`; read the specification file for context.
2. Classify intent via `router/router-map.md` using `USER_REQUEST` and the specification file.
3. Apply `policies/mode-transition-guards.md`.
4. Apply `shared/source-priority-policy.md`.
5. Always load `shared/specification-document-regulation.md` and core principles: `system-thinking.md`, `decomposition.md`, `grounding.md`.
6. Load pass/profile scope via `shared/pass-loading-policy.md`.
7. Run the selected mode wrapper:
   - `modes/spec-assistant/SKILL.md`
   - `modes/spec-generator/SKILL.md`
   - `modes/spec-normalizer/SKILL.md`
8. Aggregate findings per `shared/pass-loading-policy.md` section 6. Bare block/warning output is forbidden.

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
