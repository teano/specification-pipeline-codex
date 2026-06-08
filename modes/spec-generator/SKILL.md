---
name: spec-generator-mode
description: >-
  Full technical specification generation from design source with grounded
  extraction, subject-matter/project decomposition, and explicit unknowns.
---

# Specification Generator Mode

## 0. Runtime contract

**Inputs:** `SPECIFICATION_PATH` and `USER_LANGUAGE` (required; orchestrator — `../../SKILL.md` §2). Write the generated or updated specification to that path.

Use this mode only when the user wants a **whole** technical specification from GDD, feature brief, game/feature description, or GDD plus project context.

Core principle: the generator **does not retell the GDD** and does not produce marketing-style prose. It transforms design into a **technical specification for a coding agent**.

Before any generation or rebuild:

1. Load `../../shared/specification-document-regulation.md` and follow it for document shape, terminology, decomposition, flows, diagrams, and open questions.
2. Load `../../shared/core-principles/system-thinking.md`, `../../shared/core-principles/decomposition.md`, and `../../shared/core-principles/grounding.md`.
3. Load `../../shared/source-priority-policy.md`, `../../shared/pass-loading-policy.md`, and `../../policies/mode-transition-guards.md`.

**Precedence:** regulation wins on document format; this mode wins on GDD→requirements transformation logic. Unresolvable conflicts → report as a finding; do not guess.

**Hard rules:**

- Extract only requirements grounded in GDD, user words, project context, or confirmed decisions.
- Do not invent gameplay, project APIs, paths, namespaces, services, configs, events, or architecture without basis.
- If project context is insufficient → label `Assumption`, `Limitation`, or `Open Question`; do not close gaps silently.
- Describe mechanics, input, UI/VFX, data, configs, and integrations **inside grounded project/domain owners**, not as detached topical chapters or abstract system categories.
- Ground each owner as a concrete project-domain object using explicit project rules, project analysis, or `grounding.md`; abstract "system" wording is only internal analysis and must not remain as the final decomposition hierarchy.
- Separate gameplay logic from visual/UI/VFX, config from runtime state, orchestration from domain rules, integration boundaries from internal logic.
- Add entities only when decomposition principles require them; do not mechanically copy project-structure patterns into the spec.
- Keep terminology limited to domain vocabulary; Unity/C# API names and confirmed type/method/property signatures belong in decomposition or implementation contract and must be reused exactly, not duplicated as glossary terms.
- Post-generation edits/review → `../spec-assistant/`; normalize-only → `../spec-normalizer/`.
- **Compact output is allowed; skipping mandatory checks is not** — even for “simple” GDDs.

**Depth by source completeness:**

| Situation | Output |
|---|---|
| Sufficient data | Full spec per regulation |
| Partial data | Structured draft + assumptions, limitations, open questions |
| Too little data | Explicit “what can be fixed” vs “what needs user/project context” — do not fake completeness |

---

## 1. When to use

- User provides GDD / brief / feature description and expects a **complete document**, not fragment-by-fragment coaching.
- User asks to convert design into an agent-ready technical specification.
- User supplies GDD + project context report for one-shot generation.

**Not this mode:** fragment dictation, patch edits, review-only, research prompts, normalize-only, or incremental authoring → route per `../../policies/mode-transition-guards.md`.

If the user generates once then edits, **first pass = generator**; **follow-ups = assistant**.

---

## 2. Stage pipeline (mandatory order)

Run stages in order; do not skip a stage without an explicit blocked status and findings.

| # | Stage | Skill |
|---|---|---|
| 1 | Intake gate | `./intake-gate/SKILL.md` |
| 2 | Grounded extraction | `./grounded-extraction/SKILL.md` |
| 3 | System mapping | `./system-mapping/SKILL.md` |
| 4 | Flow and data modeling | `./flow-data-modeling/SKILL.md` |
| 5 | Open questions and risks | `./open-questions-risks/SKILL.md` |
| 6 | Assembly and verdict | `./assembly-verdict/SKILL.md` |

Internal analysis from stage 2 must **surface in the spec quality**, not as a separate dumped checklist unless the user asked for it.

---

## 3. Pass activation

Per `../../shared/pass-loading-policy.md` generator scenario:

- Profile: `../../review-profiles/review-light.md` (pass IDs only in profile file).
- Extra passes: `PASS-004`, `PASS-005`, `PASS-007`, `PASS-010`.

Run passes per profile order; aggregate findings per `../../shared/pass-loading-policy.md` §6. Do **not** copy pass checklists into this file.

---

## 4. Conditional gates

| Condition | Action |
|---|---|
| Incomplete source | Document assumptions / open questions; no silent invention |
| Any mandatory pass `block` | `draft-blocked` + structured findings |
| Targeted patch request | Route to `spec-assistant` |
| Unresolved source conflict | Finding + open question; do not pick a side as requirement |
| `not applicable` for a pass | Stated reason per policy §4 |

---

## 5. Output contract

**Language:** use required `USER_LANGUAGE` for chat and specification body content. **Do not translate** structural metadata or machine/project identifiers (`PASS-*`, `REQ-*`, finding `id`, API names, file/folder names, class/method/variable names, namespaces, config keys, Unity/C# terms, code snippets).

**Chat / handoff structure:**

1. **Status:** `draft-ok` | `draft-warning` | `draft-blocked`
2. **Assembled specification** (body per regulation)
3. **Assumptions / open questions / risks** (explicit registry)
4. **Findings** (structured per policy §6)
5. **Next step** (review-light, review-full, user decisions, or normalizer)

Include a **compact pass result table** (pass ID + status only) when any pass is not `pass`.

`draft-warning` / `draft-blocked` **without findings** → contract error.

---

## 6. Failure handling

1. Wrong scope → `../../policies/mode-transition-guards.md`.
2. Mandatory pass `block` without findings → treat as contract error; force `draft-blocked`.
3. Ambiguous routing → at most one critical clarifying question before starting.

---

## 7. When not applicable

Not for fragment capture, review-only, normalize-only, or repository research prompts.
