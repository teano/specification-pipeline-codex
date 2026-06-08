# Core Principle: Grounding

## 1. Intent

System thinking is the internal method; grounding is the mandatory document step that turns an abstract system into a concrete project-domain object.

The specification must be useful for an implementer who does not reason in systems. Do not leave "system", "subsystem", or "entity" as a thinking abstraction. In the document, every significant system must become a real feature/module object with a project-shaped role, behavior, parameters, boundaries, and expected artifact placement when known.

Grounding must change the document structure, not only individual entity cards. If the decomposition tree remains an abstract systems-thinking tree and only adds `Grounded as:` fields, grounding has failed.

---

## 2. Grounding source order

Use the strongest available project context before applying generic rules:

1. Explicit user instructions for this specification.
2. Repository rules, skill instructions, or architecture docs loaded for the current project.
3. Existing project structure, naming, local module patterns, and nearby examples.
4. Framework/platform conventions only when they are detected in the target project or explicitly supplied by the user.
5. Generic grounding fallback in §8 when project context is missing, new, inconsistent, or not compatible with any detected conventions.

If the project has clear rules, do not replace them with the fallback. If the rules are unclear or contradictory, use the clarification gate in §3 instead of inventing a fake project architecture.

---

## 3. Clarification gate: no invented grounding

If the agent does not have enough data to correctly ground an entity or its content, it must not invent project entities, class names, folders, APIs, owners, parameters, or behavior.

Before writing the entity as normative spec text, ask targeted clarification questions or record a blocking open question in the final Open Questions section. The question must ask for the missing real-world/project correspondence, not for abstract methodology.

Ask about the missing dimension:

| Missing data | Clarifying question shape |
|---|---|
| System boundary | "What is inside this system, and what is explicitly outside it?" |
| Project object | "Which real project object/module/component does this system correspond to?" |
| Responsibility | "What must this entity decide or own, and what must stay outside it?" |
| Behavior | "Which trigger starts this behavior, what states change, and what happens on invalid/cancel/failure paths?" |
| Properties/parameters | "Which parameters belong to this entity, where are they declared, and are they config, runtime state, persisted state, or view-local state?" |
| Owner/lifecycle | "Who creates, initializes, updates, disposes, clears, or releases this entity?" |
| Placement | "Where should this entity live in the project structure, or which existing slice should it extend?" |

Allowed outputs when grounding is incomplete:

- ask the user one or more focused clarification questions before editing/generating the normative entity;
- add an `OQ-xxx` only in the final Open Questions section when the pipeline mode must continue with a draft;
- add an ISSUE/risk when the missing grounding blocks implementation readiness;
- write only a clearly labeled assumption if the user/project policy allows assumptions and the assumption does not create a new mechanic, API, path, or class.

Forbidden outputs:

- inventing a plausible controller/service/view/config name;
- choosing a folder, module, persistence owner, config owner, or API because it "sounds right";
- filling behavior, parameters, or lifecycle from generic framework habits without source/project evidence;
- hiding missing grounding behind broad wording such as "the system handles this".

---

## 4. Applicability check

Before using any framework, platform, or repository convention, verify the current environment from sources that are available in the target project:

- repository indicators: source roots, package/module layout, build files, application/framework markers, test layout, config locations, generated/vendor boundaries;
- implementation surface: authored code, namespaces/packages, dependency composition, providers/adapters, controllers/services, models, views, configs, storage records;
- project-owned baseline: prefer the authored application/module area and rules named by the project, not vendor, generated, plugin, sample, or legacy trees.

Do not encode a specific repository's folder names, module names, framework objects, or internal architecture into this reusable grounding artifact. If a project convention is not discovered or supplied for the current target, use §8 instead of carrying assumptions from another project.

---

## 5. Entity-level grounding

For every significant L0/L1/L2+ item in `## 4. System Decomposition`, define what the abstract system is in the project domain.

Ground the **heading and parent-child placement** first, then ground the entity description. A heading such as "logic subsystem", "state subsystem", "input subsystem", "integration subsystem", or "configuration subsystem" is valid only when the project/domain really has that named object or boundary. Otherwise, replace it with the real object(s) that own those concerns.

Required grounding decisions:

| Decision | Required answer |
|---|---|
| Project entity kind | Feature, module/bounded context, UI component, application/runtime service, facade/API boundary, controller/orchestrator, provider, model, view, config owner, persistence owner, integration adapter, event/command, external boundary, or another project-recognized kind |
| Project location | Existing module/slice/folder when known; otherwise neutral unresolved wording, with the concrete question recorded only in the final Open Questions section if placement affects implementation |
| Runtime owner | Who creates, initializes, updates, disposes, clears, or releases the entity |
| Responsibility | What this entity decides or performs in domain terms |
| Does not own | Decisions that must stay in another entity |
| Collaborators | Concrete neighboring project entities or external systems |
| Data/config/persistence | Whether it owns runtime state, config interpretation, save data, or none |
| Lifecycle | Relevant initialization, activation, pause, completion, teardown, pool return, async/tween/subscription boundaries |

Do not write generic names such as "Logic System" or "UI System" if a project-shaped name is possible. Use domain names that identify the real thing: for example, reward claim rule owner, reward claim action view, reward claim configuration, reward claim persisted state owner, or their project-appropriate equivalents.

Concrete class names are allowed only when grounded by project rules, existing nearby patterns, user instruction, or a normalization decision. If the project convention is unknown, specify the entity kind and responsibility without pretending the final class name is confirmed.

---

## 6. Description-level grounding

Entity text must describe the real object, not the analysis category.

When documenting behavior, state:

- trigger: user action, framework lifecycle callback, command, event, timer/tick, external response, save/load, config load, or lifecycle moment;
- preconditions and invalid states;
- state read/write ownership;
- command/event inputs and outputs;
- visible result, if any, owned by the view/visual entity;
- failure/cancel/retry/unavailable branches;
- cleanup and ownership transfer.

When documenting parameters, state:

- parameter owner: config provider, module/component config, authored asset/inspector/editor setting when the project has such artifacts, local/remote config, persisted data, runtime model, or external system;
- whether the value is static config, mutable runtime state, persisted user state, or transient UI state;
- default/range only if confirmed by source or project config;
- consumers and forbidden consumers.

Do not leave behavior as "the system validates", "the system shows", or "the system saves". Name the grounded owner and describe the domain action.

---

## 7. Project-convention grounding rules

Use these only after §4 confirms that the target project has matching conventions. The rules below describe how to apply discovered conventions; they intentionally do not prescribe any one repository layout.

### 7.1 Project structure

- Place new authored code/config/data under the source root, package, module, feature area, or bounded context used by the target project.
- Choose layer and role names from local project patterns (for example API/facade, controller/service, factory/provider, model/DTO, view/component, adapter, repository, config, initialization/composition), not from this reusable instruction file.
- Do not introduce new build units, metadata files, generated files, framework descriptors, or package boundaries as spec requirements unless the user/project explicitly says so.
- Do not copy layout from vendor, plugin, generated, sample, or legacy folders as the default grounding.

### 7.2 Object and artifact kinds

- UI/view/component artifacts display state and route input; they do not own domain truth unless explicitly assigned.
- Domain/application services, controllers, policies, providers, repositories, models, factories, adapters, or workflows own rules, orchestration, data access, creation, or integration boundaries according to project convention.
- Authored/configured asset types represent parameters only when the target project uses that pattern.
- Runtime-created, pooled, subscribed, or async artifacts need an owner, lifetime, cleanup/release path, and concurrency/limit rules.

### 7.3 Composition and dependencies

- If the entity is a service/facade/controller/provider/adapter, define how it is composed using the target project's established dependency mechanism.
- Do not require hidden runtime lookup, service location, reflection, global state, or ad hoc creation for dependencies when the project expects explicit composition.
- Required externally wired references are setup requirements, not optional runtime branches, unless the design explicitly makes them optional.

### 7.4 Config and persistence

- New persistent feature/module data must use the target project's established persistence flow.
- Configs belong under the subsystem they parameterize, with serving system, parameters, consumers, invalid states, and update/static/runtime ownership.
- Bundled/local/remote config assumptions must align with the infrastructure discovered in the target project.

---

## 8. Generic grounding fallback

Use this when the project is new, lacks rules, has no clear structure, or does not match any detected framework/platform convention.

The fallback is **not** permission to invent a plausible architecture. It is a constrained way to keep the spec implementation-useful while explicitly marking every missing project correspondence.

### 8.1 Source basis under fallback

Under fallback, the only allowed normative basis is:

1. explicit user statements;
2. the source brief/GDD/spec text;
3. decisions already confirmed in the same thread;
4. generic domain decomposition from the source itself.

The fallback must not introduce:

- concrete class/interface/API names;
- folder/package/module paths;
- framework lifecycle methods;
- dependency injection/composition mechanisms;
- persistence technology;
- config file format/location;
- event bus/message bus/library names;
- data schemas beyond fields explicitly present in source or user decisions.

If any of those are needed for implementation readiness, create an `OQ-xxx` entry in the final Open Questions section or a blocking finding instead of filling the gap.

### 8.2 Minimum fallback grounding record

Every significant entity must still be grounded as:

| Field | Meaning |
|---|---|
| Entity kind | One neutral role from §8.3, not a project class name |
| Responsibility | One clear reason to exist and reason to change |
| Owner | Actor or neighboring entity that creates/updates/disposes/calls it; if unknown, write `Owner unresolved` and record the concrete question only in the final Open Questions section |
| State | What data it owns, reads, writes, persists, or must not touch |
| Behavior | Triggered actions, preconditions, transitions, outputs, failures |
| Parameters | Tunables, defaults if known from source, validation, consumers |
| Boundary | What this entity must not decide or know |
| Placement | `Project placement unresolved` unless source/user/project context provides a real location |

### 8.3 Allowed neutral entity roles

Use neutral roles only as placeholders for responsibility, not as final implementation class names:

| Neutral role | Use only when source confirms |
|---|---|
| Domain entity | A domain object with identity/state/rules from source |
| Value/data model | A structured data payload or state snapshot from source |
| Application workflow | A multi-step use case or lifecycle flow |
| Domain policy/rule | A decision rule with explicit inputs and outputs |
| Controller/orchestrator role | Coordination is required, but final project artifact is unknown |
| UI/view role | Display or input routing is required, but final UI artifact is unknown |
| Config role | Tunable/static parameters are confirmed, but storage format/location is unknown |
| Persistence role | Data must survive beyond runtime, but storage mechanism is unknown |
| Integration adapter role | Communication with an external system is confirmed |
| Event/command role | A trigger or notification contract is confirmed |

Do not multiply neutral roles for completeness. Add a role only when it protects a real source-backed boundary. If the source says only "store user progress", do not invent `ProgressRepository`, `ProgressSerializer`, and `ProgressMigrationService`; write one persistence role and mark storage/composition as unresolved.

### 8.4 Naming rules under fallback

Prefer domain names formed from source terminology plus a neutral role:

- `Order eligibility policy` when the source defines order eligibility rules;
- `Daily reward claim workflow` when the source defines a daily reward claim flow;
- `Quest launch model` when the source defines quest launch data.

Forbidden under fallback unless confirmed by project context:

- suffixing every concept with implementation names such as `Service`, `Manager`, `Controller`, `Repository`, `Provider`, `Factory`, `Facade`, `Adapter`, `ViewModel`;
- inventing namespaces, packages, folders, files, method signatures, interfaces, event bus topics, config filenames, or database table names;
- converting a neutral role into a required class name.

If a concrete name is useful but unconfirmed, phrase it as descriptive text, not as a requirement:

```md
Entity kind: domain policy role
Working label: order eligibility policy
Project artifact/name: unresolved; record the concrete question only in the final Open Questions section
```

### 8.5 Fallback placement rules

When no project structure is known, placement must be explicit about uncertainty:

- write `Project placement unresolved`;
- add an `OQ-xxx` entry in the final Open Questions section if placement affects implementation, ownership, dependency direction, or testability;
- do not write speculative paths such as `<guessed source root>/<guessed module>/<guessed role>`;
- do not infer client/server/shared placement unless source says so.

Acceptable:

```md
Placement: Project placement unresolved.
```

Not acceptable:

```md
Placement: <guessed source root>/<guessed module>/<guessed role>
```

### 8.6 Fallback API, event, and lifecycle rules

When public operations or notifications are needed but project conventions are unknown:

- describe operation intent and payload fields, not method signatures;
- describe event/command semantics, not transport/library names;
- describe lifecycle moments in domain terms, not framework callbacks;
- require ownership of subscription/cleanup only if events/subscriptions are source-confirmed;
- record composition mechanism as unresolved unless source/project context supplies it.

Acceptable:

```md
Operation: start quest from a launch model.
Input: quest type, owner id, target, optional duration.
Output: active quest instance or validation failure.
Project API shape: unresolved; record the concrete question only in the final Open Questions section.
```

Not acceptable:

```md
IQuestFacade.StartQuest(QuestStartModel model)
```

unless that signature was confirmed by source/user/project context.

### 8.7 Fallback data, config, and persistence rules

Under fallback:

- list data fields only when source/user supplied them or they are directly required by confirmed behavior;
- label derived fields as `Assumption` or record a corresponding `OQ-xxx` only in the final Open Questions section;
- distinguish runtime state, persisted state, config/static data, and display-only data;
- do not choose storage technology, serialization format, config location, database schema, save key, or migration path;
- if persistence is required but mechanism is unknown, create a persistence role and record one `OQ-xxx` for storage owner/mechanism only in the final Open Questions section.

### 8.8 Required fallback wording pattern

Use this compact pattern for each entity when grounding is incomplete:

```md
#### <Domain label>

Entity kind: <neutral role from §8.3>
Grounding status: fallback / project artifact unresolved
Responsibility: <source-backed responsibility>
Does not own: <explicit boundary>
Inputs / outputs: <source-backed fields/events/commands>
State / data: <runtime/config/persisted/display-only, as known>
Lifecycle: <domain lifecycle only, or `Lifecycle unresolved` when project lifecycle matters>
Placement: Project placement unresolved
```

Do not include an `Open question`, `Related OQ`, or `OQ-*` line in the entity. If unresolved placement/API/composition/storage affects implementation, record the question only in the final Open Questions section.

### 8.9 Fallback escalation rules

Create a blocking `OQ-xxx` in the final Open Questions section or a finding when any of these are unknown and required for implementation:

- where authoritative state lives;
- who creates or owns an entity lifecycle;
- how external consumers call or subscribe;
- how data is persisted or restored;
- which side of a boundary owns a rule;
- whether a value is config, runtime state, persisted state, or display-only;
- how many instances can exist or how they are identified;
- failure/cancel/invalid behavior.

Do not downgrade these to generic prose.

---

## 9. Document integration

Apply grounding whenever the pipeline:

- uses system thinking;
- creates or revises `## 4. System Decomposition`;
- adds, splits, merges, or renames an entity;
- writes flows that reference owners;
- writes data/config/persistence requirements;
- normalizes requirements into implementation-ready contracts;
- reviews a spec for weak ownership or implementation ambiguity.

Grounding belongs in canonical spec sections, not in a separate methodology essay or parallel placement catalog. A short entity line such as `Grounded as: UI component in <feature module>` is acceptable when it prevents ambiguity.

### 9.1 Placement of grounding information

Use this placement rule:

| Grounding content | Canonical home |
|---|---|
| Overall project integration context | `## 2. Context and Scope Boundaries` |
| Module/feature boundary and external neighbors | `## 2. Context and Scope Boundaries`, then concrete neighbors under the L0 boundary in `## 4` when they participate in flows |
| Concrete entity kind, path/package/module, signature, composition, lifecycle owner, config owner, persistence owner | The owning entity in `## 4. System Decomposition` or the normalized implementation contract |
| API/method/property/event/config-key signature | The owning decomposition/contract entry; reuse exact spelling elsewhere |
| Open grounding question | Final Open Questions section only |

`## 2` may briefly explain how the feature/module fits into the project as a whole: target module/slice if known, external modules it talks to, major infrastructure patterns it relies on, and what stays outside the boundary. It must not become a long table of all concrete entity placements, filenames, installers, config records, persistence owners, and method signatures.

If the document needs a heading such as "Project grounding", keep it short and high-level under §2. Do not put an entity-by-entity inventory there. Move those details into the matching §4 entity cards.

The following is not acceptable as completed grounding:

```md
### Level 1 — Logic subsystem
#### Rule system
Grounded as: application service
```

The hierarchy itself must be rewritten into grounded domain/project objects:

```md
### Level 1 — <domain process / project object group>
#### <specific policy, workflow, model, view, provider, adapter, or fallback role>
Entity kind: <grounded kind>
```

If grounding cannot be completed, ask clarification questions or create an `OQ-xxx` in the final Open Questions section / ISSUE/risk in the canonical issues section. Do not compensate by keeping abstract wording.

---

## 10. Anti-patterns

| Anti-pattern | Fix |
|---|---|
| "System" used as the final entity name | Replace with project-domain object and role |
| Abstract L1/L2 tree with no project artifacts | Add entity kind, owner, placement, behavior, parameters |
| Abstract hierarchy kept with `Grounded as:` fields added | Rewrite headings and parent-child structure into grounded project/domain objects |
| Separate grounding catalog duplicates §4 entities | Move concrete placement/signature/owner details to the owning §4 entity; leave only high-level integration context in §2 |
| Class names invented without project evidence | Ask which real project object applies, or record an OQ only in the final Open Questions section |
| UI view owns rule validity by wording accident | Move validity to grounded domain/controller/policy owner |
| Config described as a top-level topic | Attach config to the serving entity/subsystem |
| Persistence behavior described without project persistence owner | Ground in the discovered project persistence flow or record an OQ only in the final Open Questions section |
| Framework assumptions used in an incompatible project | Switch to generic fallback |

---

## 11. Handoff to passes

Weak grounding should surface through existing passes:

- `PASS-003` when a requirement, artifact, path, API, or owner is not source/project-grounded;
- `PASS-004` when ownership, lifecycle, API, or responsibility boundaries are ambiguous;
- `PASS-005` when config, data, or persistence ownership is unclear;
- `PASS-008` / `PASS-009` when normalized requirements cannot be addressed or traced to grounded owners.
