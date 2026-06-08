---
name: spec-normalizer-mode
description: >-
  Normalize an existing specification into implementation-ready markdown with
  strict machine addressability, traceability, and readiness gates.
---

# Specification Normalizer Mode

## 1. Inputs

1. `SPECIFICATION_PATH` — existing specification to normalize (required; orchestrator — `../../SKILL.md` §2);
2. `USER_LANGUAGE` — user-facing language and specification body language (required; orchestrator — `../../SKILL.md` §2);
3. request for implementation-ready artifact;
4. shared docs:
   * `../../shared/specification-document-regulation.md`;
   * `../../shared/core-principles/system-thinking.md`;
   * `../../shared/core-principles/decomposition.md`;
   * `../../shared/core-principles/grounding.md`;
   * `../../shared/source-priority-policy.md`;
   * `../../shared/pass-loading-policy.md`;
   * `../../policies/mode-transition-guards.md`.

## 2. Execution Steps

Run stages in order; do not skip gates for compact output.

1. `./pipeline/SKILL.md` — source analysis, classification, deduplication, 20-section draft assembly;
2. `./addressability-traceability/SKILL.md` — machine addressing layer, registry gate, traceability matrix (`PASS-008`);
3. `./anti-weakening-readiness/SKILL.md` — coverage/readiness verdict (`PASS-001`, `PASS-009`);
4. produce final verdict with blocking finding IDs when any gate fails.

## 3. Mandatory Pass Activation

Per `../../shared/pass-loading-policy.md` normalizer scenario:

* profile `../../review-profiles/review-full.md`;
* extra passes `PASS-008`, `PASS-009`, `PASS-010`.

Pass check semantics live only in `../../shared/passes/*`. Stage files add orchestration and artifact contracts, not duplicated checklists.

## 4. Output Artifact Contract

Final normalized markdown must follow the 20-section TOC in `./pipeline/SKILL.md` §3.

Non-negotiable sections (never omitted; use explicit empty-state text when slice absent):

* `## 3. Source Preservation Notes`
* `## 6. Machine-Readable Requirement Address Registry`
* `## 19. Traceability Matrix`
* `## 20. Readiness Verdict`

Compact output is allowed; skipping mandatory sections or internal gates is not. See `./anti-weakening-readiness/SKILL.md` §2.

## 5. Conditional Gates

1. not for first-time generation from source design;
2. not for targeted edits without normalization goal;
3. any `PASS-008` or `PASS-009` block → verdict `Blocked` / `Not Ready`;
4. `Ready` requires confirmed machine addressability + traceability + explicit readiness dimensions;
5. `PASS-010` block or critical deduplication loss → not `Ready`.

## 6. Output Contract

1. normalized artifact + readiness verdict (`## 20. Readiness Verdict`);
2. on block: separate `Blocking Findings IDs` list (structured findings per `../../shared/pass-loading-policy.md` §6);
3. structured findings for `pass-with-warning` / `block` / critical risk;
4. verdict dimensions: source preservation, terminology, machine-readable addressing, orphan blocking elements, unresolved blockers;
5. use required `USER_LANGUAGE` for chat and specification body content; structural metadata and machine/project identifiers stay English where required (`REQ-*`, `AC-*`, `PASS-*`, finding `id`, API names, file/folder names, class/method/variable names, namespaces, config keys, Unity/C# terms, code snippets).

## 7. Failure Handling

1. wrong scope → route via `../../policies/mode-transition-guards.md`;
2. `PASS-008` / `PASS-009` block → no "almost ready" wording;
3. block without finding IDs → contract error, forced `Blocked`;
4. missing machine addressing → self-repair (assign IDs, update registry/matrix/verdict) before returning artifact; do not explain omission as final result.

## 8. Hard Invariant

**No machine addressability and traceability → no `Ready` normalization output.**

Human-readable cleanup alone (pretty structure, deduped prose, tables without stable element IDs, section-title references) is an erroneous result for this mode.

## 9. When Not Applicable

Not for generating a new spec from scratch or local patch/review without normalization output.
