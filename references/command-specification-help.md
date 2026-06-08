---
description: >-
  Help for $skill-specification-pipeline: create or continue a specification
  file, then run the global specification pipeline skill on it.
---

# Specification Pipeline Help

Entry skill: `$skill-specification-pipeline`

Process root: this global Codex skill package (`skill-specification-pipeline/SKILL.md`)

The skill always resolves a single markdown specification file before routing.
Review routes (`review-light`, `review-full`) are read-only on that file:
findings and proposed fixes go to chat. The skill edits the document only when
you ask to apply fixes or when the route is `fragment-capture`, `spec-generator`,
or `spec-normalizer`.

Hard write boundary: the skill may create the specification parent directory
during `new` and may edit only the resolved markdown specification file.
It must not create, edit, delete, move, rename, format, or patch source code,
assets, configs, tests, generated project files, project metadata, or any
non-documentation project file.

The skill detects `USER_LANGUAGE` from your natural-language request and uses
that language for chat and specification body content.

## Invocation Formats

### Continue An Existing Specification

```text
$skill-specification-pipeline continue <path-to-specification.md> [-- <work request>]
```

Examples:

```text
$skill-specification-pipeline continue .cursor/tasks/reward-v2/specification.md -- add fragment: daily cap in section 3.2
$skill-specification-pipeline continue .cursor/specs/shop-checkout.md -- full pre-implementation review
```

### Create A New Specification

```text
$skill-specification-pipeline new "<specification-title>" <parent-directory> [-- <work request>]
```

The skill creates `<parent-directory>/<slug-from-title>.md` with a regulation
section skeleton: empty sections, no invented requirements.

Examples:

```text
$skill-specification-pipeline new "Shop checkout flow" .cursor/specs/shop
$skill-specification-pipeline new "Daily rewards" .cursor/tasks/daily-rewards -- generate complete technical spec from the GDD below: ...
```

If the target file already exists, use `continue` instead of `new`.

## What To Pass As `<work request>`

Optional text after `--` or trailing free text is routed by the skill:

| You might say | Typical route |
|---|---|
| "Add this rule to section 3.2" | `spec-assistant` -> fragment-capture |
| "Quick sanity check" | `spec-assistant` -> review-light |
| "Full pre-implementation review" | `spec-assistant` -> review-full |
| "Generate complete technical spec from GDD" | `spec-generator` |
| "Normalize into implementation-ready markdown" | `spec-normalizer` |

Ambiguous intent routes to `spec-assistant`, with at most one critical
clarifying question. Details: `../router/router-map.md`.

## Direct Skill Contract

The same contract is required even when the user invokes the skill naturally
without writing the full command format:

* `SPECIFICATION_PATH` - required, existing `.md`, unless the request uses `new`;
* `SPECIFICATION_DIR` - parent directory of `SPECIFICATION_PATH`; created only by `new`;
* `USER_LANGUAGE` - required, human-readable language name such as `English`, `Russian`, or `Spanish`;
* `USER_REQUEST` - optional work intent.

## Related Docs

* router: `../router/router-map.md`;
* document shape: `../shared/specification-document-regulation.md`;
* open questions: regulation section 7.1 - unresolved `OQ-xxx` only in section 11; section 7.2 - closed answers inline in body, not a closed-decisions archive;
* system decomposition: regulation section 5 + `../shared/core-principles/decomposition.md` section 2.1 - tree (L0 -> L1 subsystems -> nested L2 entities), not a flat entity list;
* file I/O: active repo `AGENTS.md` / encoding guidance; fallback UTF-8 without BOM and LF line endings for markdown.

User-facing pipeline output and specification body content use `USER_LANGUAGE`.
Keep structural metadata and machine/project identifiers in English where
required for navigation or implementation: `PASS-*`, `REQ-*`, `AC-*`, finding
`id`, API names, file/folder names, class/method/variable names, namespaces,
config keys, Unity/C# terms, and code snippets.
