# Assistant Submode: Fragment Capture

## 1. Purpose

Apply a local or dictated spec change without full rewrite; ground every introduced implementation entity before writing it; keep related sections consistent with regulation fragment protocol (`../../../shared/specification-document-regulation.md` §6) and open-question closure (`§7`). This submode is not the default for proofreading-only requests.

## 2. Mandatory passes

`PASS-002`, `PASS-003`, `PASS-011` per `../../../shared/pass-loading-policy.md` §4.

Run pass files in `../../../shared/passes/`; aggregate per §6.

When the fragment introduces or changes public operations, creation/registration, lifecycle, ownership, async behavior, data, config, or persistence, also run the corresponding conditional `PASS-004` and/or `PASS-005` in the same turn. Do not postpone these checks to a later review.

## 3. Proofreading Guard

Before editing, check the user wording:

1. If `USER_REQUEST` says `вычитка`, `proofread`, `proofreading`, `редактура`, `проверь текст`, `проверь спецификацию`, `найди проблемы`, or similar without an explicit write/apply verb, stop and route to `review-light`; do not edit `SPECIFICATION_PATH`.
2. Explicit write/apply verbs include `внеси правки`, `исправь в файле`, `примени`, `apply`, `patch`, or `rewrite/update this section`.
3. If proofreading and write intent are both present but the write scope is unclear, ask at most one critical clarification question before editing.

## 4. Implementation Intent Guard

When `USER_REQUEST` describes what must be done, implemented, added, changed, or decided for future work, capture it in the specification instead of executing it:

1. Treat phrases such as `сделать`, `реализовать`, `надо сделать`, `нужно добавить`, `нужно изменить`, `что будем делать`, `какое решение принять`, `зафиксируй решение`, `implement`, `build`, `add`, or `change` as specification material when the pipeline is active.
2. Map the intent to the canonical section: what to build → decomposition / flows / mandatory implementation approach; what not to do → constraints / forbidden formal solutions; selected choice → explicit decision or normative requirement; unresolved choice → open question; risk → issue/risk.
3. Do not create, edit, delete, move, rename, format, patch, or otherwise mutate source code, assets, configs, tests, scenes, generated files, project metadata, or any non-documentation project file.
4. If the user explicitly asks to implement project files during this pipeline run, stop before project mutation and state that implementation requires a separate non-pipeline request.

### 4.1 Immediate Grounding Gate For Dictated Entities

Treat wording such as “нужен провайдер для модели данных”, “добавь конфиг”, “нужен контроллер/фасад/репозиторий/адаптер”, or equivalent entity-level intent as a request for a grounded project contract, not permission to write an abstract role.

Before editing `SPECIFICATION_PATH`:

1. Apply `../../../shared/core-principles/grounding.md` §4.1 and inspect relevant project-owned analogues.
2. Resolve the project-shaped name and placement, interface/public contract when local convention requires it, creator/composition root, registration and lifetime, dependencies, ownership boundaries, and entity-specific data/config/lifecycle details.
3. Write the entity and its affected contract/flow/data/config references together in the same fragment.
4. If the project evidence is absent, contradictory, or insufficient for an implementation-critical dimension, add a focused `OQ-xxx` only in the final Open Questions section. Do not add an abstract provider/model/config/controller/facade entry as normative text and do not guess a plausible name or DI pattern.

### 4.2 Immediate System Boundary And Coherence Gate

Run `PASS-011` for every semantic dictated fragment, including statements that name only one system/entity. Perform the pre-write analysis before treating the sentence's grammatical subject as the behavior owner:

1. Supply `PASS-011` with the fragment, affected specification entities/flows/contracts, project rules, and available project-owned analogues.
2. Treat its owner/boundary/coherence result as a write gate: apply the grounded hierarchy and interaction result, or create `OQ-xxx` and omit the misleading ownership statement.

After editing, run `PASS-011` again against the changed entity, neighboring systems, flows, and contracts. Do not allow the fragment to accumulate a hidden boundary or stale ownership error for later generation/normalization.

Atomic boundary/coherence semantics live only in `../../../shared/passes/PASS-011-system-boundary-coherence.md`.

## 5. Mini-protocol (before and after target edit)

1. Map fragment to canonical section(s) and affected entities before writing.
2. Run the `PASS-011` pre-write analysis from §4.2 for every semantic fragment; identify hidden boundaries and existing capability owners even when only one entity is named.
3. If an implementation entity/signature is introduced or changed, run the immediate grounding gate in §4.1 before writing normative text.
4. Terminology impact → PASS-002: classify new names as domain terminology vs Unity/C# API vs decomposition/contract signatures before editing glossary.
5. Source grounding and conflicts → PASS-003.
6. If the fragment uses system thinking, changes decomposition, adds behavior, changes an owner, or names an implementation entity, apply `../../../shared/core-principles/grounding.md` so the affected system becomes a concrete project-domain artifact/role before the edit. If data is insufficient, create the focused `OQ-xxx` instead of the abstract entity.
7. If the fragment touches ownership/API/creation/registration/lifecycle, run conditional PASS-004. If it touches model/data/config/persistence, run conditional PASS-005. These checks are part of the current fragment, not a deferred recommendation.
8. After writing, run `PASS-011` post-write verification and re-read the entity plus neighboring decomposition, interaction, contract, flow, data, and config references; remove abstract, incoherent, duplicate-owner, or contradictory remnants.
9. Weakening risk vs baseline → PASS-001 spot-check when prior text exists.
10. List related sections needing user-approved follow-up edits.

### 5.1 When the user answers an open question

Per `../../../shared/specification-document-regulation.md` §7:

0. New unknown from a fragment → add `OQ-xxx` to Open Questions only; do not add entity-level “Open questions”, `Related OQ`, body-level `OQ-*`, or flow `TBD` instead of §11.
1. Locate the OQ by ID or text in Open Questions (`## 11` draft / `## 18` normalized).
2. Edit the **canonical section(s)** so the answer is normative inline text (constraints, flows, decomposition, data, integration, or `REQ-*` after normalization).
3. **Remove** the OQ from the open-questions section; do not add “Closed decisions”, “Resolved OQ”, or duplicate tables.
4. Do not leave `Related OQ`, `Linked decision`, or `Связанные решения: OQ-...` cross-references in canonical sections after the question is closed; the answer must stand as normal spec text.
5. If normalization IDs exist, add one line under Source Preservation Notes (`§3`) only when traceability needs it (`OQ-00x → REQ-… / §8`).
6. In chat output, report **which sections changed** — not a parallel list of closed OQs.

## 6. Execution Steps

1. Load `../../../shared/source-priority-policy.md` and fragment scope.
2. Map affected canonical sections and identify every action/capability and introduced/changed implementation entity.
3. Run `PASS-011` pre-write analysis. Detect hidden boundaries, search existing project capability owners, and decide the hierarchy/interaction impact before accepting the user's grammatical subject as owner.
4. Run the immediate grounding gate. Inspect project rules and analogous authored entities; resolve the concrete artifact contract or create `OQ-xxx` and omit the abstract/misowned entity.
5. Before writing, run `PASS-002` and `PASS-003`, plus conditional `PASS-004`/`PASS-005` for the affected slices. Resolve blocking terminology, source, ownership/API/lifecycle, and data/config issues now; optional `PASS-001` spot-check applies when a baseline exists.
6. Apply the grounded, cohesive user change to the target section and directly affected hierarchy/interaction/contract/flow/data/config sections only (no full-doc rewrite unless requested).
7. If the fragment introduces or changes a confirmed type, method, property, field, event, config key, namespace, folder, or file signature, update its owning decomposition/contract entry and align exact mentions; do not add a glossary/TERM-* row for the signature.
8. After writing, re-run the mandatory passes plus conditional `PASS-004`/`PASS-005` against the resulting text, then run `PASS-011` post-write verification across affected owners and neighboring systems. Record cross-section impact and contradictions; a pre-write pass does not substitute for this post-write verification.
9. Aggregate findings per `../../../shared/pass-loading-policy.md` §6.

## 7. Conditional Gates

- No full document regeneration.
- Proofreading-only wording is not a write scope; route to `review-light`.
- Implementation wording inside spec work is a write scope only for `SPECIFICATION_PATH`, never for project files.
- A dictated implementation entity must be grounded before normative insertion; “add abstract now, ground later” is forbidden.
- Every semantic dictated fragment must pass `PASS-011` before and after writing; “record one sentence now, repair boundaries later” is forbidden.
- Unresolved source conflict → finding + open question; never silent merge.
- User asks for full spec from one phrase → route to `spec-generator` per mode guards.

## 8. Output Contract

Compact operational response in required `USER_LANGUAGE`:

1. **Status:** `ok` | `warning` | `blocked`
2. **What changed** (section + intent)
3. **Findings** (structured if any)
4. **Related sections to update**
5. **One next step**

`warning` / `blocked` without findings → contract error.

## 9. Failure Handling

- Mandatory pass `block` → `blocked` + findings; do not claim fragment is “done”.
- If fragment implies architecture not in source → Open Question, not invented types.
- If the affected entity cannot be grounded → record `OQ-xxx` only in the final Open Questions section (or ask a targeted clarification question when execution cannot continue); do not patch the spec with an abstract or guessed entity.
- If `PASS-011` detects a hidden boundary or existing project owner → split/reassign the responsibility and update the hierarchy/interaction in the same fragment; never save the misowned formulation for later cleanup.

## 10. When Not Applicable

Full-document review, generation, or normalization → other submodes.
