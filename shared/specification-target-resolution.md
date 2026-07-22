# Specification Target Resolution

## 1. Purpose

Resolve the specification target and internal operation from natural-language intent before mode routing. Literal `new` / `continue` tokens are supported shortcuts, never mandatory user syntax.

This policy may perform read-only discovery before `SPECIFICATION_PATH` is bound. No pass or mode runs until target resolution finishes.

## 2. Internal result

Return:

- `TARGET_OPERATION`: `new` | `continue`;
- `SPECIFICATION_PATH`;
- `SPECIFICATION_DIR`;
- `SPECIFICATION_TITLE` when known;
- `USER_REQUEST`: the original work intent with command/path syntax removed;
- `TARGET_RESOLUTION_SOURCE`: `explicit-path` | `conversation-binding` | `attached-or-open-file` | `unique-project-candidate` | `inferred-new-target` | `user-confirmation`.

The user does not need to say the internal operation name.

## 3. Candidate discovery

Use this precedence:

1. explicit markdown path in the current request;
2. still-valid `SPECIFICATION_PATH` already bound in the current conversation/task;
3. an attached, selected, or currently open markdown specification explicitly available to the agent;
4. one uniquely relevant candidate in the active project/workspace.

For project discovery, search read-only with `rg --files` (or the next available equivalent) inside the active feature/task directory first, then the active workspace. Consider conventional names such as `specification.md`, `spec.md`, `*-specification.md`, and `*.spec.md`. Rank by request terminology, nearby source/design files, current directory, and feature/task name.

Never:

- search the whole user profile or unrelated workspaces unless asked;
- select among multiple plausible files silently;
- treat an arbitrary markdown document as a specification only because it is the sole `.md` file;
- create or overwrite a file during discovery.

Once a path is resolved, keep it as the conversation binding for subsequent dictation until the user changes the target or the file becomes unavailable.

## 4. Intent-to-operation rules

### Explicit shortcuts

- Explicit `new` with a non-existing target → `new`.
- Explicit `continue` with a readable target → `continue`.
- Natural-language equivalents such as “создай новую спеку”, “продолжи эту спеку”, “дополни существующую” have the same force.

### Generate a specification

When the user asks to generate/create/write a specification:

1. no relevant specification exists → infer `new`;
2. a target location and title are explicit or safely inferable from a unique conventional project spec directory → set `TARGET_RESOLUTION_SOURCE=inferred-new-target` when no explicit path was supplied, then create without asking the user to repeat `new`;
3. location/title is not safely inferable → ask one targeted question for the missing location/title, while stating that `new` was inferred;
4. one relevant specification already exists → ask one choice: regenerate/replace it from scratch or continue/complete the existing document;
5. multiple relevant specifications exist → ask which path is intended; include the regenerate-vs-continue choice only when still ambiguous after selection;
6. explicit “continue/complete generation” or “regenerate/rewrite from scratch” resolves rule 4 without another question.

Never overwrite an existing specification merely because the request says “generate”.

### Dictate, add, or change requirements

When the user starts dictating requirements, decisions, entities, flows, constraints, or corrections:

1. a valid conversation-bound or uniquely relevant specification exists → infer `continue` and route to fragment capture;
2. no relevant specification exists → preserve the fragment in conversation state and ask one question offering: provide/select a target path or create a new specification;
3. multiple candidates exist → ask which specification to continue;
4. do not require the user to restate the fragment after target resolution.

### Review or normalize

- Existing unique/bound target → infer `continue`.
- No target → ask for/select the specification path; do not create an empty document for review/normalization.
- Multiple candidates → ask which one.

## 5. Clarification contract

Ask at most one blocking question per turn. Make it about the smallest unresolved decision and include discovered paths or a concrete suggested path when useful.

Clarify explicitly when:

- the request could mean specification work or project implementation;
- target candidates are multiple or semantically weak;
- generation targets an existing file but rewrite vs continuation is not stated;
- a new target's location/title cannot be inferred safely;
- the requested action itself is unclear.

Do not respond with command syntax alone. Explain the inferred action in natural language and offer the minimal choice.

## 6. Creation and collision safety

For `new`, derive the slug and starter document using the pipeline root creation rules. Before creating, re-check that the target does not exist.

If it now exists, stop and ask whether to continue it, regenerate it, or choose another path. Regeneration/replacement is destructive and requires explicit user confirmation; preserve or report any recovery mechanism required by the active environment.

## 7. Binding gate

After resolution, require readable `SPECIFICATION_PATH` for `continue` or a confirmed non-existing target for `new`, plus `USER_LANGUAGE`. Only then enter router, passes, or modes.

If resolution cannot finish, remain in target-resolution state. Do not pretend the pipeline ran and do not discard dictated content.
