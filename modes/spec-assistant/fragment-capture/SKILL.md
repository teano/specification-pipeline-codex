# Assistant Submode: Fragment Capture

## 1. Purpose

Apply a local spec change without full rewrite; keep related sections consistent with regulation fragment protocol (`../../../shared/specification-document-regulation.md` §6) and open-question closure (`§7`). This submode is not the default for proofreading-only requests.

## 2. Mandatory passes

`PASS-002`, `PASS-003` per `../../../shared/pass-loading-policy.md` §4.

Run pass files in `../../../shared/passes/`; aggregate per §6.

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

## 5. Mini-protocol (after target edit)

1. Map fragment to canonical section(s) and affected entities.
2. Terminology impact → PASS-002: classify new names as domain terminology vs Unity/C# API vs decomposition/contract signatures before editing glossary.
3. Source grounding and conflicts → PASS-003.
4. If the fragment uses system thinking, changes decomposition, adds behavior, or changes an owner, apply `../../../shared/core-principles/grounding.md` so the affected system becomes a project-domain object/role; if data is insufficient, ask for the real project object, boundary, responsibility, behavior, or properties instead of inventing them.
5. If slice touched: ownership/API (PASS-004), data/config (PASS-005) — note in findings or recommend follow-up review.
6. Weakening risk vs baseline → PASS-001 spot-check when prior text exists.
7. List related sections needing user-approved follow-up edits.

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
2. Apply the user change to the target section only (no full-doc rewrite unless requested).
3. Ground changed systems/entities through project context or `../../../shared/core-principles/grounding.md` when ownership/decomposition/behavior is touched.
4. If the fragment introduces or changes a confirmed type, method, property, field, event, config key, namespace, folder, or file signature, update its owning decomposition/contract entry and align exact mentions; do not add a glossary/TERM-* row for the signature.
5. Run mandatory passes; optional spot-check PASS-001 when baseline exists.
6. Record cross-section impact and contradictions.
7. Aggregate findings per `../../../shared/pass-loading-policy.md` §6.

## 7. Conditional Gates

- No full document regeneration.
- Proofreading-only wording is not a write scope; route to `review-light`.
- Implementation wording inside spec work is a write scope only for `SPECIFICATION_PATH`, never for project files.
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
- If the affected entity cannot be grounded → ask targeted clarification questions or record `OQ-xxx` only in the final Open Questions section; do not patch the spec with guessed entities.

## 10. When Not Applicable

Full-document review, generation, or normalization → other submodes.
