# Generator Stage: Flow and Data Modeling

## 1. Purpose

Model **behavior over time** and **data/config contracts** so implementation agents know states, transitions, persistence boundaries, and config touchpoints — without a class-diagram retelling.

Mandatory passes (per `../../../shared/pass-loading-policy.md` §4):

- `PASS-004` — `../../../shared/passes/PASS-004-api-lifecycle-ownership.md`
- `PASS-005` — `../../../shared/passes/PASS-005-data-config-integrity.md`

If a pass is `not applicable`, state reason per policy §4.

---

## 2. Behaviour flows

Flows describe **feature behavior in time**, per `../../../shared/specification-document-regulation.md`.

Each significant flow must answer:

1. What happens first?
2. What does the player or external system do?
3. Which grounded **system/entity** reacts (not only which class)?
4. Which states change?
5. What does the player see?
6. What branches exist?
7. What happens on error, cancel, retry, or unavailable state?

Rules:

- Do not create a standalone “runtime flow” top-level chapter if regulation places flows in canonical sections.
- Multiple distinct GDD flows → separate behavior scenarios.
- Flow steps must reference grounded owners from system-mapping; no orphan steps.

---

## 3. Data models

Per regulation `## 5. Data Models`:

- Describe **data**, not system behavior prose.
- Entities, fields, ownership, persistence scope, validation boundaries.
- Distinguish runtime state vs config vs transient UI state.
- If GDD omits fields → open question or explicit optional field, not invented gameplay numbers.

---

## 4. Config modeling

Configs are **entities inside grounded decomposition**, not a fake top-level doc chapter and not an abstract "config subsystem" unless that subsystem is a real project/domain object.

For each config entity define:

| Field | Content |
|---|---|
| Serving system | Who loads/owns interpretation |
| Parameters | Names and meaning |
| Defaults | Only if confirmed in source |
| Valid ranges / invalid states | If known |
| Consumers | Who reads; what must not be runtime state |

Missing numeric values → Open Question or “tuning area” only if user confirmed tuning is in scope.

---

## 5. API, lifecycle, and ownership slice

When in scope, `PASS-004` covers:

- Public contracts between systems/modules.
- Lifecycle triggers (init, tick, pause, destroy, pool return).
- Ownership of subscriptions, async completion, visual handoff.

Document outcomes in flow steps and decomposition — pass semantics live only in the pass file.

---

## 6. Integration with prior stages

| Prior stage | This stage uses |
|---|---|
| Grounded extraction | REQ list, edge cases, forbidden shortcuts |
| System mapping | Owners for each flow step and data entity |
| Open questions (draft) | Unresolved transitions or persistence |

---

## 7. Stage gate

Do not proceed to `./open-questions-risks/SKILL.md` if:

- Mandatory `PASS-004` or `PASS-005` is `block` without findings and remediation plan, or
- Major flows lack an owning system.

---

## 8. Stage execution steps

1. List main user/core/behavior flows from GDD.
2. For each flow, write state/transition narrative with grounded project/domain owners.
3. Build data model section entries linked to grounded owners.
4. Attach config entities to grounded owning entities.
5. Check grounding for flow/data/config owners against `../../../shared/core-principles/grounding.md`.
6. Run `PASS-004` and `PASS-005`; aggregate findings per policy §6.
7. Cross-check: no gameplay truth stored in view; no config values invented.

---

## 9. Output

| Field | Content |
|---|---|
| Stage status | `flow-data-ok` \| `flow-data-warning` \| `flow-data-blocked` |
| Deliverable | Flow scenarios + data model + config entities (draft sections) |
| Pass table | `PASS-004`, `PASS-005` (+ profile passes if concurrent) |
| Findings | Structured per policy §6 |
| Language | Required `USER_LANGUAGE` |
