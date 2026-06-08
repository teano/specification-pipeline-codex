---
description: >-
  Codex invocation reference for $skill-specification-pipeline. Resolves or
  creates the specification markdown file, then routes through the global
  specification pipeline skill.
---

# Codex Specification Pipeline Invocation

Use `$skill-specification-pipeline` as the only process root for specification
requests.

## 1. Parse Arguments Before Routing

The skill does not run router, pass, profile, or mode work until a concrete
specification file path is resolved.

### 1.1 Continue An Existing Specification

```text
$skill-specification-pipeline continue <path-to-specification.md> [-- <free-text user request>]
```

Rules:

1. `<path-to-specification.md>` must be repo-relative or absolute, end with `.md`, and exist on disk.
2. If the file is missing or unreadable, stop and ask the user for a valid path.
3. Set `SPECIFICATION_DIR` to the parent directory of the resolved `SPECIFICATION_PATH`.

### 1.2 Create A New Specification

```text
$skill-specification-pipeline new "<specification-title>" <parent-directory> [-- <free-text user request>]
```

Rules:

1. `<specification-title>` is the human title used for the document `#` heading and filename slug.
2. `<parent-directory>` is the folder that will contain the file. Create the directory if it does not exist.
3. Derive `SPECIFICATION_SLUG` from the title: lowercase; trim; replace spaces/underscores with `-`; keep only `[a-z0-9-]`; collapse repeated `-`; trim leading/trailing `-`.
4. Set `SPECIFICATION_DIR = <parent-directory>`.
5. Set `SPECIFICATION_PATH = <parent-directory>/<SPECIFICATION_SLUG>.md`.
6. If `SPECIFICATION_PATH` already exists, stop and tell the user to use `continue` or pick another directory/title.
7. Create the starter body as UTF-8 without BOM and LF line endings: `# <specification-title>` plus section headings from `../shared/specification-document-regulation.md` section 5. Sections may stay empty; do not invent requirements.

### 1.3 Invalid Or Incomplete Invocation

If the request does not start with `new` or `continue`, or required parameters
are missing, stop and show the formats from
`references/command-specification-help.md`. Do not route the pipeline without
`SPECIFICATION_PATH`.

Optional `--` separator: everything after `--` is `USER_REQUEST`. If `--` is
absent, treat the remainder after structured parameters as `USER_REQUEST` when
unambiguous.

## 2. Determine User Language

Before routing, determine `USER_LANGUAGE` from the user's natural-language
request.

Rules:

1. Use the dominant natural language in `USER_REQUEST`; if empty, use the surrounding user message or the new specification title.
2. For `continue` with no usable request text, inspect the existing specification body and use the dominant non-metadata natural language.
3. Ignore project naming when detecting language: API names, file/folder names, class/method/variable names, Unity/C# terms, IDs, and code snippets do not decide `USER_LANGUAGE`.
4. If the language cannot be determined confidently, stop and ask the user to specify the language.
5. Store a human-readable language name, for example `English`, `Russian`, or `Spanish`.

## 3. Hand Off To The Skill

Pass these bindings into the pipeline:

| Binding | Value |
|---|---|
| `SPECIFICATION_PATH` | resolved markdown file |
| `SPECIFICATION_DIR` | parent directory of `SPECIFICATION_PATH` |
| `SPECIFICATION_TITLE` | `#` title from the file, else `<specification-title>` for `new` |
| `USER_REQUEST` | text after `--` or trailing free text |
| `USER_LANGUAGE` | detected user language |

Then:

1. route via `../router/router-map.md` using `USER_REQUEST` and the spec file as context;
2. enforce guards from `../policies/mode-transition-guards.md`;
3. apply shared policies, principles, and pass-loading policy;
4. run the selected mode workflow.

Specification edits go to `SPECIFICATION_PATH` when the routed mode allows
writes (`spec-generator`, `spec-normalizer`, `fragment-capture`). During `new`,
the skill may create `SPECIFICATION_DIR`. No other filesystem mutations are
allowed: do not create, edit, delete, move, rename, format, or patch source code,
assets, configs, tests, generated project files, project metadata, or any
non-documentation project file. `review-light` and `review-full` are read-only
until the user explicitly asks to apply fixes.
