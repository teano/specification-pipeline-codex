# Generator Stage: System Mapping

## 1. Purpose

Map **subsystems, boundaries, and responsibilities** as an internal analysis step, then output a grounded subject-matter/project decomposition — so a coding agent cannot collapse everything into one God Object or mix logic with view/state.

Inputs: grounded extraction output from `./grounded-extraction/SKILL.md`, regulation decomposition rules, and `../../../shared/core-principles/grounding.md`.

---

## 2. Architecture intent

Decomposition exists to:

- Split responsibility; avoid God Objects.
- Keep logic separate from visual state; keep view from gameplay decisions.
- Separate config from runtime state.
- Support testability of key rules.
- Fit existing runtime; block shortcut implementations.
- Fit project context: map abstract systems to real project-domain objects, roles, folders, artifacts, and syntax when known.
- Make ownership explicit for runtime-created objects, pools, subscriptions, callbacks, tweens, async work when present.

**Do not** turn every mechanic into a class. Add an entity only when it protects a real boundary (see §4), then ground that entity in project terms. The final `## 4` tree must not remain the abstract candidate-system map.

---

## 3. System signals (from GDD)

Reuse extraction signals; at mapping stage, cluster candidates into systems:

| Signal type | Mapping action |
|---|---|
| Stateful process | Candidate system or entity with explicit state owner |
| Decision rule | Rule owner distinct from visual/input |
| Configurable parameters | Config entity under serving system |
| Visual-only feedback | UI/visual system; no gameplay truth |
| External touchpoint | Integration boundary entity |
| Variant / mode / policy | Strategy/policy owner |
| Spatial model (grid, slots, zones) | Often needs dedicated model + view interpolation split |

---

## 3.1 Grounding pass

After selecting candidate systems, apply `grounding.md` before writing `## 4. System Decomposition`:

1. Load project rules and inspect nearby project structure when available.
2. Decide which discovered project/framework conventions apply to the current project.
3. Rewrite the candidate system map into a grounded subject-matter/project tree; do not keep abstract L1/L2 headings and merely add `Grounded as`.
4. For each L0/L1/L2+ item, state the project entity kind and placement when known.
5. Replace abstract labels such as "Logic System" with domain/project names where possible.
6. If boundary, responsibility, behavior, properties, placement, artifact kind, or owner cannot be grounded, ask targeted clarification questions or add an `OQ-xxx` only in the final Open Questions section / ISSUE-risk in the canonical issues section instead of inventing a class/API/path.
7. Do not emit a separate entity-by-entity project grounding table in §2. Put concrete placements, signatures, composition, config, persistence, and lifecycle details on the owning §4 entity; §2 receives only high-level integration context.

Grounding does not force concrete class names. It forces concrete project-domain meaning.
If that meaning is unknown, the correct output is a question or blocker, not a guessed entity.

If grounding confirms a concrete signature for a decomposition item (type, method, property, field, event, config key, namespace, folder, or file), record that signature on the owning decomposition/contract entry and use it exactly everywhere. Do not add a glossary entry just to define the signature name; glossary stays for the domain concept, while decomposition/contract owns the signature semantics.

---

## 4. When deep decomposition is required

Deep decomposition is **mandatory** if GDD has any of:

- Discrete tick/update flow.
- Spatial model: field, grid, lines, slots, zones.
- Multiple object states; move/swap/merge/match/collision/placement rules.
- Scoring, combo, multiplier, streak, rewards.
- Waves, spawn, RNG, weighted generation, pools.
- Progression, stages, milestones, difficulty scaling.
- Win/lose/endgame.
- Blocking states: pause, tutorial, modal, animation lock, spawn lock.
- Runtime-created visuals; pool return / cleanup.
- View interpolating a discrete model.
- Multi-modal input (drag, tap, swipe, hold, multi-step).
- Analytics/events/result flow.
- High risk of single controller becoming God Object.

If present → document systems **below** the top layer with explicit responsibility.

---

## 5. System selection criteria

**Split out** when:

- Independent reason to change.
- Hides strategy/policy/mode variability.
- Shields logic from framework/UI/VFX/storage/config loading.
- Separates orchestration from domain rules.
- Reduces central `switch`/`if`/enum growth.
- Narrow contract for external consumers.
- Makes lifecycle ownership explicit.

**Do not split** when:

- Would be a single method with no change driver.
- Exists only “for the future”.
- Single caller and no complexity reduction.
- Boundaries cannot be grounded in GDD/project context or `grounding.md` fallback.

---

## 6. Responsibility matrix (internal tool)

For each complex mechanic or flow, fill mentally (include in doc only if user asked):

```text
Mechanic / flow:

- State owner:
- Rule owner:
- Input owner:
- Config owner:
- Visual owner:
- Lifecycle owner:
- Integration owner:
- Events / payloads:
- Forbidden dependencies:
- Open questions: (internal scratch — emit only in `## 11. Open Questions` as `OQ-xxx`, not in entity blocks)
```

If multiple rows need **different natural owners** → decomposition required.

If one owner is credible for a simple mechanic → extra system may be unnecessary.

---

## 7. Mandatory second GDD pass

After primary mapping, for **each significant mechanic** ask:

```text
What systems are required so this mechanic does not live inside a God Object?
```

Per mechanic, confirm:

- Logical state owner.
- Rule owner.
- Config owner.
- Visual display owner.
- Input gesture owner.
- Runtime-created object owner.
- Cleanup owner.
- Events between owners.
- Forbidden direct dependencies.

Complex mechanics → specialized, grounded systems; **concrete class names optional** when project conventions should decide shape.

---

## 8. Mandatory system vs implementation detail

Describe a system **explicitly** when omission would likely cause the agent to:

- Mix logic and view.
- Build a God Object.
- Hardcode tunables.
- Drop edge cases.
- Violate lifecycle ownership.
- Couple domain to external APIs.
- Fail verification or choose shortcuts.

Do **not** list reference roles, folder patterns, or generic technical entities mechanically from project structure.

---

## 9. Domain and role copy prohibition

Do not transplant project-structure labels or generic “manager/service/controller” names from context **unless** GDD or confirmed decisions require them.

---

## 10. Stage execution steps

1. Consume grounded extraction; trace each REQ to a system candidate.
2. Apply deep-decomposition triggers (§4).
3. Run responsibility matrix on complex flows (§6).
4. Execute second GDD pass (§7).
5. Apply grounding pass (§3.1) to convert the abstract system map into a project-domain object tree.
6. Record mapping as a **hierarchical tree** in `## 4. System Decomposition` (`decomposition.md` §2.1): L0 block → one heading per grounded L1 project/domain part → grounded entities nested under that part → interaction subsections per level; optional ASCII tree at L0; external neighbors under L0 “outside boundary”, not as internal L1 after a flat entity list.
7. For each confirmed signature-bearing item, keep the signature in the decomposition/contract entry and align all later mentions to that exact spelling/case; do not create a terminology alias row for it.
8. Keep §2 project context high-level; move entity-specific placement/signature/composition/config/persistence details into the owning §4 entity, not a separate grounding catalog.
9. Register unresolved owners and gaps as `OQ-xxx` in **`## 11. Open Questions` only** (per regulation §5–§7 and `decomposition.md` §5); do not scatter `TBD` or “open questions” subsections under entities in `## 4. System Decomposition`.

---

## 11. Quality criteria

- Traceable to extracted requirements.
- No anonymous “the system does X” without owner.
- No ungrounded system/entity when project context or `grounding.md` can identify a concrete domain object/role.
- No abstract systems-thinking hierarchy remains with only formal `Grounded as` annotations.
- No separate grounding catalog duplicates the §4 decomposition entries.
- Cross-cutting concerns (save, config, analytics) attributed when in scope.
- External dependencies named at boundary level only.

---

## 12. Output

| Field | Content |
|---|---|
| Stage status | `mapping-ok` \| `mapping-warning` \| `mapping-blocked` |
| Deliverable | Grounded hierarchical decomposition (tree-shaped §4) + optional responsibility matrix |
| Findings | Gaps, God Object risks, ownership conflicts |
| Language | Required `USER_LANGUAGE` |
