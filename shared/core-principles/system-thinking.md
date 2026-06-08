# Core Principle: System Thinking

## 1. Intent

Treat every feature as a system of interacting parts with ownership, state, behavior over time, and explicit boundaries — not as a flat requirements list.

System thinking is an **internal analysis method**. It tells the agent how to inspect requirements: find boundaries, part-whole relations, ownership, dependencies, state, behavior over time, and failure paths.

System thinking is **not** the final decomposition style. The spec document must not preserve the agent's abstract thinking map as the implementation contract. It shows the analysis result through grounded project-domain entities, structure, owners, flows, and data — not through meta prose ("we apply systems thinking") and not through abstract "logic/input/output/state systems" as final entities.

---

## 2. What counts as a "system" here

Any element that can own state, rules, triggers, or integration boundaries, for example:

- feature / module / subsystem;
- logical layer (domain, application, presentation);
- facade, controller, provider, service, installer;
- UI window, view, content view, widget;
- config entity, data model, event, command;
- external pipeline or integration boundary.

This is not a checklist to paste into every doc. Use only entities that the task actually needs.

---

## 3. Mandatory perspective per requirement

For each normative fragment, determine internally:

| Lens | Question |
|---|---|
| Placement | Which canonical section and subsystem does this refine? |
| Entity | New entity, or responsibility change on an existing one? |
| Data | Does this add/change models, config, or persistence? |
| Flow | Which user/core/behaviour flow step is affected? |
| Time | Triggers, lifecycle moment, async completion? |
| Boundaries | What must this part **not** decide? |
| Terminology | New or changed term → glossary impact? |
| Risk | Shortcut implementation or formal-but-wrong execution? |
| Consistency | Contradiction or weakening vs source/prior spec? |

You do not need to rewrite the whole document each time; you must know where the fragment belongs.

The table below is an internal reasoning lens only. Do not paste these lens names as decomposition headings unless the current project really has such a named object/layer and `grounding.md` confirms it.

When one statement spans multiple areas, trace **all** affected sections. Example:

```text
User: "The claim-reward button must be disabled if the reward was already claimed."

Affects:
- document decomposition: grounded UI component or action owner;
- reward state model;
- claim-reward flow and technical steps;
- edge case: repeated claim attempt.
```

---

## 4. Layering rules

1. **UI/visual layers** must not own gameplay or business rules unless explicitly assigned.
2. **Config** is not runtime state; parameters live with grounded owning entities in decomposition.
3. **Orchestration** (flow, scene, session) is separated from **domain rules** (scoring, validation).
4. Integration boundaries are explicit: what crosses modules, what stays internal.
5. Unresolved ownership becomes an **`OQ-xxx` entry in Open Questions** (`## 11` draft / `## 18` normalized), not an invented class and not a per-entity “open questions” paragraph in decomposition.

---

## 5. Flows and behaviour over time

- **User flow** — player-visible steps and decisions.
- **Core loop** — repeating mechanical cycle.
- **Behaviour flow** — technical sequence inside systems (including failure branches).

Flows must name the **owning system** per step. Triggers and preconditions are part of the contract, not optional color.

---

## 6. System approach rules (continuous)

1. Terminology is fixed **before** document decomposition when terms exist (`PASS-002`).
2. Same-level entity interactions are described explicitly, not only entity lists.
3. Entity descriptions stay inside decomposition — not orphan top-level chapters.
4. Separate data from behavior, UI from logic, config from runtime state, public API from internals.
5. Separate proposals, assumptions, confirmed requirements, and open questions; **unresolved** open questions live only in the Open Questions section (see `../specification-document-regulation.md` §5–§7).

---

## 7. Anti-patterns (internal guardrails)

| Anti-pattern | Why it fails |
|---|---|
| God Object controller | Hidden coupling, untestable rules |
| Business logic in view | Formal UI pass, wrong outcomes |
| Config as mutable runtime store | Save bugs, race conditions |
| Mechanically copied project templates | Wrong boundaries for this feature |
| Invented integration APIs | Ungrounded implementation |
| Silent assumption closure | False "confirmed" requirements |

Flag these via passes (`PASS-003`, `PASS-004`, `PASS-007`) rather than duplicating check text in modes.

---

## 8. Relation to other layers

| Layer | Role |
|---|---|
| `../specification-document-regulation.md` | Document shape, fragment protocol, review focus |
| `decomposition.md` | How to split systems and describe entities |
| `grounding.md` | How to turn abstract systems into concrete project-domain objects |
| `../passes/*` | Testable verification of system quality |
| Mode stages | When to apply extraction, mapping, normalization |

---

## 9. Output discipline

Show system thinking through grounded project-domain objects, named owners, explicit state/data ownership, separated visual vs logic responsibilities, and open questions where boundaries are unclear.

Final decomposition must be a subject-matter/project decomposition, not a systems-thinking worksheet. Do not output methodology essays unless the user asks for process explanation.
