# Core Principle: Decomposition

## 1. Intent

Split a feature into grounded subject-matter/project entities with clear responsibility, change drivers, and forbidden overlaps — so a coding agent cannot "implement the paragraph" in one monolithic class.

Derived from regulation sections 7–11 and generator mapping rules (document decomposition at generation time).

System thinking may produce an internal abstract system map. The document decomposition must be the grounded result of that map: real domain objects, project artifacts, feature objects, integration boundaries, data/config/persistence owners, UI/view objects, workflows, policies, or neutral fallback roles.

Every entity produced by decomposition must be grounded through `grounding.md`: the document must say what the entity is in the current project domain, which project context justifies it, and how its behavior/parameters are represented. A `Grounded as:` line on top of an otherwise abstract subsystem tree is not enough.

---

## 2. Levels of decomposition

| Level | Typical content |
|---|---|
| L0 Feature / module | Root project/domain object boundary (one per `## 4`) |
| L1 Subject area / project object group | Major grounded part inside L0; not an abstract analysis category unless it is a real project/domain object |
| L2 Entity | Concrete project/domain entity, artifact, policy, workflow, model, view, adapter, owner, or neutral fallback role **inside** one L1 parent |
| L3+ Nested | Grounded child objects, fields, hooks, views/config consumers, lifecycle parts, or owned records **inside** one L2 parent |

Go deeper only when shallow split would force a God Object or ambiguous ownership. Simple features may use one or two levels; complex features need more.

### 2.1 Hierarchical tree (mandatory document shape)

`## 4. System Decomposition` must be a **grounded part-whole tree**, not a linear slice per level and not the raw system-thinking map.

The word "System" in the section title means the feature is understood as a connected whole. It does **not** permit abstract final headings such as "Logic subsystem", "State subsystem", "Input subsystem", "Integration subsystem", or "Persistence subsystem" unless those are discovered project/domain objects. If such names only describe the agent's analysis lens, convert them into the real object(s) that own the behavior.

**Required structure:**

1. **L0** — one root block (`### 4.1. Level 0 — <feature/module>`): role, boundary, optional tree overview.
2. **L1** — each grounded subject/project part is its **own** heading nested under L0 (`### 4.x. Level 1 — <grounded part name>`), not only a summary table detached from children and not an abstract analysis category.
3. **L2+** — each grounded entity is a **child heading under its L1 parent** (`#### <entity name>`), not a single flat list “all L2 entities”.
4. **Same-level interactions** — after the entities of that level (subsystem or L0 internal), add `#### Interaction at level <N>` (or regulation numbering `4.x.y`) before moving to the next sibling subsystem.
5. **External neighbors** — actors outside L0 sit under the L0 block (e.g. “Outside L0 boundary”), not as another “L1 subsystem” mixed with internal children.

**Tree overview (recommended at start of §4):**

```text
<Feature> (L0)
├── <Subsystem A> (L1)
│   ├── <Entity A1> (L2)
│   └── <Entity A2> (L2)
└── <Subsystem B> (L1)
    └── <Entity B1> (L2)

Outside L0: <neighbor systems>
```

**Forbidden:**

- `### 4.2` table of L1 parts + `### 4.3` flat list of **all** L2 entities with no parent part;
- every entity as sibling `####` under one “Level 2” section;
- numbering that jumps L0 → flat L2 → “L1 external” after internal entities.
- abstract system-thinking headings kept as final decomposition with only `Grounded as:` fields added below them.

---

## 3. When to add an entity

Add a distinct entity only if it protects at least one boundary:

- separate **reason to change**;
- separates **gameplay decision** from **visual representation**;
- separates **orchestration** from **domain rules**;
- hides **runtime object creation**, pooling, or cleanup;
- owns **config load** vs **runtime state**;
- defines **external integration** surface;
- prevents **formal but wrong** single-class implementation.

If none apply, keep behavior inside an existing entity — do not add classes for completeness.

---

## 4. Deep decomposition triggers

Escalate depth when source material shows any of: spatial/tick models; multi-state objects; scoring/rewards; spawn/pools; win/lose with blocking UI; runtime-created views; multi-step input; analytics handoff; God-Object risk.

---

## 5. Entity description format

Place each significant entity **under its parent grounded part heading** in the tree (see §2.1), never in a detached flat catalog:

```md
### <Entity name>

Type: <role>
Grounded as: <project-domain object kind / artifact, if known>
Signature: <confirmed type/method/property/field/event/config key, if known>
Role: <place in feature>
Responsibility: ...
Does not own: ...
Inputs / outputs: ...
Commands / events: ...
Child entity management: ...
Reporting upward: ...
Boundaries: ...
```

Omit subsections that do not apply. Simple UI elements stay brief; facades, controllers, providers, scenarios, configs deserve fuller treatment.

If the project has known structure, `Grounded as` should identify the concrete project kind (for example module service, controller, provider, view, config owner, persistence owner, integration adapter, or external boundary) and placement when known. If project structure is unknown, use the generic grounding fallback; unresolved placement questions are recorded only in the final Open Questions section when they affect implementation.

`Signature` is optional and only for names confirmed by source/user/project context. Once recorded, it is the canonical mention form across the spec. Do not create a glossary/TERM-* entry for the signature itself; glossary may define the underlying domain concept only when needed. Unity/C# framework API names used by the signature remain API references, not terminology entries.

Do not move these entity fields into a separate "project grounding" table outside decomposition. If a field describes one concrete entity, it belongs on that entity card. §2 may summarize the feature's overall project integration, but it is not a replacement for grounded entity cards.

**Do not** add an `Open questions:` (or equivalent) field on entity cards. **Unresolved** questions belong only in `## 11. Open Questions` (draft) or `## 18. Open Questions` (normalized) with stable IDs (`OQ-001`, …). Do not add `Related OQ`, `OQ-*`, question text, or `TBD` prose inside decomposition. If needed, use neutral unresolved wording such as `Placement unresolved`; the actual question and ID stay in the Open Questions section.

---

## 6. Same-level interactions

After listing entities at a level, describe peer exchange — entity lists alone are insufficient:

```md
### 4.X. Interactions at level <N>
Participants: <A>, <B>
Flow: 1. ... 2. ...
Forbidden: UI must not make gameplay/business decisions.
```

Unconfirmed interaction → register as `OQ-xxx` in Open Questions (§11 / §18), not as stated fact inline in interactions or entity blocks.

---

## 7. Responsibility matrix (generator stage)

During generation, maintain an internal matrix (Behavior / rule → Owning system → Notes). Second pass: every GDD mechanic maps to exactly one primary owner or an open question.

Prefer explicit **responsibility** over fixed class names when project conventions are unknown. Do not mechanically copy domain systems or role names from other specs unless grounded in this task.

---

## 8. Config, data, UI, and visual boundaries

- Config entities live **inside** the grounded entity/part they parameterize.
- Data models section lists cross-cutting records; local fields stay with the entity.
- UI owns presentation and input routing; domain owns validity and outcomes.
- VFX/animation: trigger, blocking vs non-blocking, cleanup owner.

---

## 9. Forbidden decomposition mistakes

| Mistake | Fix |
|---|---|
| One class per GDD bullet | Group by responsibility |
| Copying reference architecture wholesale | Ground in GDD + project context |
| Abstract "system" without project entity kind | Apply `grounding.md` and name the concrete object/role |
| Formal grounding pasted onto the old abstract hierarchy | Rewrite the hierarchy itself into grounded project/domain objects |
| Entity placements/signatures collected in a separate §2 grounding table | Move each concrete detail to the owning entity in §4; keep §2 high-level |
| Entity without "does not own" | Boundaries stay ambiguous |
| Duplicate owners for same rule | `PASS-004` conflict finding |
| Shallow split with heavy flow | Add L2 entities |
| Open question text, `Related OQ`, or `OQ-*` under each entity | Move the question and ID to §11 / §18; keep only neutral unresolved wording in the entity if needed |
| Flat “Level 2 — all entities” section | Nest each entity under its L1 parent; add tree overview (§2.1) |

---

## 10. Handoff to passes and normalizer

Weak decomposition → `PASS-004`, `PASS-006`, `PASS-003`. Normalizer maps stable entities to `REQ-*`. Deduplication → `PASS-010`. Verify via pass IDs only — no checklist duplication here.
