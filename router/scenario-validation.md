# Scenario Validation

## Purpose

Validate route and pass activation coherence for key scenarios.

Canonical matrix: `../shared/pass-loading-policy.md` §4.
Routing entry: `./router-map.md`.

---

## Target-Resolution Scenarios

### Scenario 0A: Natural Generation, No Existing Specification

**Sample intent:** "Сгенерируй техническую спецификацию для daily quests."

* discovery: no conversation-bound, attached/open, or uniquely relevant existing specification
* internal result: `TARGET_OPERATION=new`; when the path is derived rather than explicit, `TARGET_RESOLUTION_SOURCE=inferred-new-target`
* explicit target/title safely inferable: create and route to `spec-generator` without requiring the word `new`
* target/title not safely inferable: ask one question for the missing location/title and state that new-spec creation was inferred
* result: valid

### Scenario 0B: Natural Generation, Existing Specification

**Sample intent:** "Сгенерируй спеку для daily quests." One relevant specification already exists.

* do not overwrite or choose generator semantics silently
* ask one choice: regenerate/replace from scratch or continue/complete the existing specification
* explicit "продолжи генерацию" → `continue`; explicit "пересоздай с нуля" → confirmed replacement flow
* result: valid clarification gate

### Scenario 0C: Dictation With Existing Target

**Sample intent:** "Нужен provider для модели данных."

* valid conversation-bound or uniquely relevant specification exists
* internal result: `TARGET_OPERATION=continue`
* preserve the utterance as `USER_REQUEST` and route directly to grounded fragment capture
* do not ask the user to say `continue` or repeat the fragment
* result: valid

### Scenario 0D: Dictation Without Target

**Sample intent:** "После claim награда должна сохраняться."

* no relevant specification exists
* retain the fragment in conversation state
* ask one question offering an explicit path/selection or creation of a new spec, with a concrete suggested path when safe
* after resolution, apply the retained fragment without requesting repetition
* result: valid blocked resolution

### Scenario 0E: Multiple Candidates Or Unclear Action

* multiple relevant specifications → ask which path; never choose silently
* request could mean spec documentation or project implementation → ask which result the user wants
* response must be a natural-language minimal question, not command usage alone
* result: valid clarification gate

### Scenario 0F: Explicit Shortcuts Remain Supported

* explicit `new` and `continue` still bind the same internal operations
* shortcuts bypass only resolved ambiguity, not collision, path, language, or write-safety gates
* result: valid

---

## Happy-Path Scenarios

### Scenario 1: Fragment Capture

**Sample intent:** "Add this new reward rule to the existing spec section."

* route: `spec-assistant` → `../modes/spec-assistant/fragment-capture/SKILL.md`
* profiles: none
* passes: `PASS-002`, `PASS-003`, `PASS-011` (per pass-loading-policy §4)
* expected behavior: pre-write boundary/coherence analysis, local grounded update, post-write verification, no full rewrite, one next step
* result: valid

### Scenario 1A: Dictated Implementation Entity

**Sample intent:** "Нужен провайдер для модели данных."

* route: `spec-assistant` → `../modes/spec-assistant/fragment-capture/SKILL.md`
* passes: `PASS-002`, `PASS-003`, `PASS-011`, plus conditional `PASS-004` and `PASS-005` because interface/composition and model/data slices are affected
* expected behavior: before editing, inspect project rules and same-role authored analogues; resolve the project-shaped provider/model name, interface or concrete contract per local convention, creator/composition root, registration/lifetime, dependencies, ownership, and data behavior
* insufficient evidence: add focused `OQ-xxx` only in the final Open Questions section and do not insert an abstract provider/model entity into normative decomposition or contract text
* forbidden behavior: write “data model provider” as an abstract placeholder and defer naming/interface/registration to generation or normalization
* result: valid

### Scenario 1B: Hidden System Boundary During Dictation

**Sample intent:** "Модуль A выполняет доменную операцию B." The current project may already have a separate owner for capability B.

* route: `spec-assistant` → `../modes/spec-assistant/fragment-capture/SKILL.md`
* passes: mandatory `PASS-002`, `PASS-003`, `PASS-011`; conditional `PASS-004` for the cross-system contract and `PASS-005` when state/data/config/persistence is affected
* pre-write behavior: decompose the statement into actions/capabilities; do not assume Module A owns operation B; search project rules and authored source for an existing capability owner; evaluate the cohesion of both responsibility sets
* grounded existing owner found: retain Module A only as calculator/requester/consumer when supported; assign execution to the existing owner; update hierarchy (`Outside L0 boundary` when external to the feature), interaction, flow, and contract in the same fragment
* owner/boundary unresolved: create focused `OQ-xxx`; do not save the misowned statement or invent a duplicate system
* post-write behavior: re-run `PASS-011` across affected neighboring systems and cross-section references
* forbidden behavior: preserve the one-system wording and defer boundary repair to generation/normalization
* result: valid

---

### Scenario 2: Review-Light

**Sample intent:** "Quickly check this draft for obvious problems."

* route: `spec-assistant` → `../modes/spec-assistant/review-light/SKILL.md`
* profiles: `../review-profiles/review-light.md`
* passes from profile: `PASS-003`, `PASS-011`, `PASS-002`, `PASS-001`, `PASS-006`
* executor: fresh isolated Codex subagent through `../modes/spec-assistant/review-worker/SKILL.md`
* parent behavior: resolve route, verify path, compute exact-byte SHA-256, and dispatch paths/bindings without reading the complete specification or pass files
* worker behavior: read the complete specification and required context in isolation, run the profile, return one compact review bundle, perform no writes
* expected behavior: parent validates revision/schema and renders a concise findings-first report; escalation contract §6 applies; **no edits** to `SPECIFICATION_PATH` unless user explicitly requests application afterward
* result: valid

### Scenario 2A: Stale Delegated Review Before Apply

**Setup:** A valid review bundle exists, then `SPECIFICATION_PATH` changes before the user asks to apply `F-*`.

* parent recomputes exact-byte SHA-256 before editing
* hash mismatch: do not apply proposed fixes from the old bundle; delegate a new review against the current file
* forbidden behavior: apply findings by ID to a different revision or silently rebase guessed edits
* result: valid

### Scenario 2B: Review Subagent Unavailable

**Setup:** Codex does not expose the multi-agent/subagent mechanism for this run.

* do not fail the review request
* run the selected profile locally under the same read-only contract
* tell the user briefly that isolated review was unavailable and parent-context fallback was used
* forbidden behavior: claim that a worker ran, skip passes, or edit the specification
* result: valid fallback

### Scenario 2C: Apply Approved Findings And Verify

**Setup:** User explicitly asks to apply selected findings from the latest bundle; current hash matches.

* parent routes selected `F-*` through `fragment-capture`; worker never writes
* apply selected fixes as one coherent operation with mandatory fragment passes
* compute new hash and delegate post-fix verification with selected finding IDs and affected sections
* report findings as closed, remaining, or replaced; preserve IDs when the same problem remains
* result: valid

---

### Scenario 3: Review-Full

**Sample intent:** "Do a full deep review before implementation" / "Сделай полную вычитку."

* route: `spec-assistant` → `../modes/spec-assistant/review-full/SKILL.md`
* profiles: `../review-profiles/review-full.md` (includes light + extended)
* effective passes: `PASS-003`, `PASS-011`, `PASS-002`, `PASS-001`, `PASS-006`, `PASS-004`, `PASS-005`, `PASS-007`, `PASS-010`
* executor: fresh isolated Codex review subagent; parent receives a validated compact bundle and does not repeat passes
* routing precedence: explicit full/deep wording wins over the generic `вычитка` → review-light default
* expected behavior: deep findings-first report with risks and proposed fixes (chat only); **no edits** to `SPECIFICATION_PATH` unless user explicitly requests application afterward
* result: valid

---

### Scenario 4: Generator

**Sample intent:** "Generate a complete technical spec from this GDD."

* route: `spec-generator` → `../modes/spec-generator/SKILL.md`
* profiles: `../review-profiles/review-light.md`
* extra passes: `PASS-004`, `PASS-005`, `PASS-007`, `PASS-010`
* expected behavior: grounded full draft with explicit assumptions/open questions
* result: valid

### Scenario 4A: Generator Source With Blurred System Boundaries

**Sample source:** Several actions from different domain capabilities are attributed to one named module, while the project may already contain owners for some capabilities.

* route: `spec-generator` → grounded extraction → system mapping
* grounded extraction: run `PASS-011` action/capability analysis before prose; surface hidden owner candidates and existing-owner lookup requirements
* system mapping: build cohesive candidate systems, ground them in project context, then re-run `PASS-011` against the final hierarchy/interactions/flows/contracts
* expected hierarchy: distinct internal responsibilities become correct sibling branches; existing external owners appear under the L0 outside boundary with explicit interaction; no duplicate capability system is invented
* unresolved owner: `OQ-xxx` / finding; `mapping-ok` and `draft-ok` forbidden while `PASS-011` blocks
* result: valid

---

### Scenario 5: Normalizer

**Sample intent:** "Normalize this specification into implementation-ready markdown."

* route: `spec-normalizer` → `../modes/spec-normalizer/SKILL.md`
* profiles: `../review-profiles/review-full.md`
* extra passes: `PASS-008`, `PASS-009`, `PASS-010`
* hard gate: if `PASS-008` or `PASS-009` fails, readiness is blocked with blocking finding IDs
* expected behavior: machine-addressable normalized artifact with traceability/readiness verdict; inherited `PASS-011` prevents `Ready` for incoherent or duplicate capability ownership
* result: valid

---

## Edge Scenarios

### Scenario 6: Ambiguous Intent

**Sample intent:** "Look at this spec" (no artifact: patch vs review vs generate).

* route: `spec-assistant` (default per `router-map.md` §3)
* clarifying questions: at most one critical question before execution
* do not route to `spec-generator` or `spec-normalizer` until intent is clear
* result: valid

---

### Scenario 7: Partial Source

**Sample intent:** "Generate the full spec" with incomplete GDD / missing sections.

* route: `spec-generator`
* passes: generator set (review-light + extras per §4)
* expected behavior: `block` or explicit assumptions/open questions; no silent invention
* `PASS-003` must surface grounding gaps as findings; `PASS-011` must surface hidden boundaries, incoherent candidate systems, and unresolved capability owners
* result: valid (blocked draft acceptable with findings)

---

### Scenario 8: Conflicting Source

**Sample intent:** Two design sources contradict on ownership or data contract.

* route: depends on task — review → `spec-assistant` + appropriate profile; generate → `spec-generator`
* `PASS-003` and `PASS-011` (plus `PASS-004`/`PASS-005` when in scope) must emit conflict/boundary findings
* must not: auto-pick a winner without a user-visible finding
* result: valid

---

### Scenario 9: Not-Applicable Passes

**Sample intent:** Review a UI copy fragment with no API/data/lifecycle in scope.

* route: `spec-assistant` + `review-light`
* conditional passes (`PASS-004`, `PASS-005`, `PASS-006` when out of scope): `not applicable` with stated reason per `pass-loading-policy.md` §4
* `PASS-011`: `not applicable` only if the reviewed fragment is confirmed editorial-only with zero semantic/ownership/flow/hierarchy impact; otherwise run it
* must not: skip mandatory profile passes silently
* result: valid

---

## Pass Escalation Contract Scenarios

Reference: `../shared/pass-loading-policy.md` §6. Mode wrappers aggregate; pass files do not duplicate escalation fields.

### Scenario 10: Warning With Findings

**Setup:** A mandatory pass returns `pass-with-warning` with at least one structured finding (`id`, `pass_id`, `severity`, `problem`, `impact`, `location`, `recommended_fix`).

* mode-layer status: `warning` (assistant) / `draft-warning` (generator) per §8 mapping
* delegated review: worker bundle includes aggregated findings; parent validates and renders them — not status-only
* local/generator report: includes aggregated findings list — not status-only
* result: **valid contract**

---

### Scenario 11: Block With Findings

**Setup:** Any mandatory pass returns `block` with one or more structured findings (blocking IDs for `PASS-008`/`PASS-009` in normalizer).

* mode-layer status: `blocked` / `Blocked` / `Not Ready` as applicable
* normalizer: `Ready` forbidden; blocking finding IDs required in verdict
* user report: findings-first; targeted fixes where applicable
* result: **valid contract**

---

### Scenario 12: Block Without Findings (Contract Error)

**Setup:** Pass or mode layer emits `block` or `pass-with-warning` **without** structured findings.

* expected executor behavior: treat as **contract violation** — rebuild findings before final user output; do not ship bare status
* mode wrappers (`spec-assistant`, `spec-generator`, `spec-normalizer`) and `mode-transition-guards.md` §6: forced `blocked` / no `Ready`
* negative test: this scenario must **fail** validation if presented as a finished user deliverable
* result: **invalid** — contract error

---

## Coherence Checklist

1. all scenarios use only `spec-assistant`, `spec-generator`, or `spec-normalizer`;
2. pass activation matches `../shared/pass-loading-policy.md` §4 for each scenario row;
3. review profiles list only pass IDs; semantics stay in `../shared/passes/*`;
4. normalizer hard gate (`PASS-008`, `PASS-009`) explicitly blocks `Ready` on failure;
5. escalation scenarios 10–11 satisfy §6; scenario 12 must never pass as final output.
6. every semantic fragment scenario and generator extraction/mapping scenario includes `PASS-011`; grammar alone never determines capability ownership.
7. review-light/full use one isolated read-only worker per profile; parent does not preload the complete document or rerun passes after a valid bundle.
8. stale review bundles never authorize writes; worker unavailability uses an honest local read-only fallback.
9. target-resolution scenarios infer `new` / `continue` from natural language, preserve pending dictation, and never overwrite or select among candidates silently.
