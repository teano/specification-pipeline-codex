# PASS-011: System Boundary and Coherence

## Purpose

Detect hidden system boundaries, verify internal system cohesion, assign each capability to its natural grounded owner, and prevent a specification from accumulating cross-domain responsibility errors or duplicate project systems.

This pass treats system discovery as semantic analysis. The grammatical subject of a requirement is not automatically the owner of every action in that sentence.

Source basis: `../core-principles/system-thinking.md`, `../core-principles/decomposition.md`, `../core-principles/grounding.md`, project rules and authored project analogues, source requirements, and confirmed user decisions.

## Activation / Not applicable

**Activate when:**

- `fragment-capture` receives any semantic requirement, behavior, flow, entity, responsibility, state, config, data, integration, or ownership change;
- generator runs grounded extraction or system mapping;
- review or normalization evaluates behavioral requirements, decomposition, flows, owners, or interactions;
- one sentence assigns an action to a module/system/entity, even when no second system is named explicitly.

**Not applicable only when:** the change is editorial/formatting-only with zero semantic, ownership, flow, hierarchy, or entity impact.

**Required report if N/A:** identify the reviewed fragment/sections and confirm zero semantic change.

## Checklist (numbered)

1. **Action decomposition:** split each normative statement into grammatical subject, trigger, action/capability, target/object, state read/write, result/external effect, and failure/invalid behavior when present.
2. **Capability ownership:** do not equate the grammatical subject with the natural owner. Determine which domain capability each action belongs to and which entity should decide, calculate, request, execute, persist, or display it.
3. **Existing-owner lookup:** before creating or assigning a system, inspect project rules and project-owned source for an existing module, facade, service, provider, repository, controller, policy, adapter, model owner, config owner, persistence owner, or public boundary that already owns the capability. Reuse/extend the grounded owner; do not specify a duplicate parallel system.
4. **Boundary signals:** split responsibilities when they have different domain vocabulary, reasons to change, authoritative state, invariants, lifecycle, configuration, persistence, external consumers, integration boundary, or natural project owner. Sequential use in one flow is not evidence that responsibilities belong to one system.
5. **Internal cohesion:** for every system/entity, verify that its members support one domain purpose and a compatible responsibility set, state/invariants, lifecycle, and change driver. Flag unrelated capabilities grouped only for convenience, call order, screen proximity, or because one controller/module can technically call them.
6. **Single primary owner:** assign each decision, rule, authoritative state mutation, lifecycle obligation, and external effect to exactly one primary owner or a focused `OQ-xxx`. Callers may prepare inputs or request an operation without becoming the execution owner.
7. **Responsibility verbs:** distinguish at least `decides/validates`, `calculates/prepares`, `requests`, `executes/applies`, `persists`, and `displays/notifies`. Do not collapse them into an ambiguous verb such as “handles”, “processes”, or “issues”.
8. **Grounding:** use `grounding.md` to confirm project-shaped names, artifact kinds, placement, interfaces/contracts, composition/registration, dependencies, and lifecycle. If the project owner or boundary cannot be proven, create `OQ-xxx`; do not invent a new system or leave the wrong owner as normative text.
9. **Hierarchy reflection:** represent distinct internal systems as separate sibling branches under their correct parent. Represent an existing owner outside the feature L0 under `Outside L0 boundary`, not as an internal child. Add same-level or boundary interaction text instead of hiding the dependency inside one entity description.
10. **Interaction contract:** for every split boundary, identify caller/consumer, operation intent, inputs, outputs/result, failure behavior, ownership transfer, and forbidden direct dependencies when confirmed. Delegate API/lifecycle detail validation to `PASS-004`.
11. **Cross-section propagation:** in the same turn, align the owning decomposition entries, affected flows, data/config/persistence sections, implementation contract, constraints, and Open Questions. Do not update only the dictated sentence while leaving contradictory ownership elsewhere.
12. **No error accumulation:** after a fragment edit or generated hierarchy is assembled, re-read the affected owner and neighboring systems. A newly introduced hidden boundary, incoherent responsibility set, duplicate owner, or stale hierarchy must not survive into the saved specification as a passing result.

## Pass conditions

`pass` requires all of the following:

- every affected action/capability has one coherent grounded primary owner;
- each affected entity has an internally compatible responsibility set;
- distinct systems are represented at the correct hierarchy/boundary level;
- existing project owners are reused rather than duplicated;
- affected interactions and cross-section references agree.

Use `pass-with-warning` only when uncertainty is explicitly captured as `OQ-xxx`, no false owner remains normative, and the remaining gap does not make the saved fragment misleading.

Use `block` when the text assigns a capability to an incompatible owner, collapses multiple natural systems, duplicates an existing project owner, leaves an incoherent system as normative text, or cannot be safely written without an unresolved boundary decision.

`not applicable` is forbidden for semantic `fragment-capture`, grounded extraction, or system mapping.

## Failure signals

- One module/entity is said to perform a capability owned by another project system.
- One system contains members with unrelated domain purposes, invariants, state, lifecycle, or reasons to change.
- Multiple systems are described as one because their operations occur consecutively in a flow.
- A new service/provider/controller/facade duplicates an existing project capability owner.
- A caller is described as executing an effect when it only calculates inputs or requests the real owner.
- The decomposition lists one system while flows/contracts reveal multiple natural owners.
- A discovered external owner is nested inside feature L0 instead of represented as an external neighbor and interaction boundary.
- An unresolved boundary is hidden in generic prose instead of `OQ-xxx`.

## Example finding templates

```text
[Hidden System Boundary]
Statement: <normative fragment>
Capabilities: <capability A>, <capability B>
Natural/project owners: <owner A>, <owner B or unresolved>
Impact: <wrong hierarchy, coupling, duplicate system, incorrect implementation>
Recommended fix: split responsibility; update hierarchy and interaction; add OQ if owner is unresolved
```

```text
[Incoherent System]
Entity: <name>
Incompatible responsibilities: <A>, <B>
Different change drivers/state/invariants/lifecycle: <evidence>
Recommended fix: retain one cohesive responsibility; move the other to its grounded owner or create a separate boundary only when project evidence supports it
```

```text
[Existing Owner Bypassed]
Capability: <name>
Existing grounded owner: <project entity/source location>
Conflicting proposed owner: <spec entity>
Recommended fix: reuse/extend the existing owner and document the caller-to-owner contract
```

Structured finding: `F-xxx | PASS-011 | high | problem | impact | location | recommended_fix`

## Output

Report `pass` | `pass-with-warning` | `block` | `not applicable` and aggregate findings per `../pass-loading-policy.md` §6.

For `fragment-capture`, run a pre-write boundary analysis and a post-write verification. Do not save a formulation that would make `PASS-011` block; write the grounded split/interaction or record the blocking `OQ-xxx` instead.

For generator, run during grounded extraction to expose candidate boundaries and after system mapping to validate the final grounded hierarchy. `mapping-ok` / `draft-ok` is forbidden while `PASS-011` blocks.

For normalizer, any `PASS-011` block makes readiness not `Ready` through the aggregate readiness rules.

## Integration with other passes

- `PASS-003`: verify source/project grounding and conflicts for the selected owners.
- `PASS-004`: validate the API, lifecycle, composition, and ownership contract after boundaries are selected.
- `PASS-005`: validate data/config/persistence ownership across the boundary.
- `PASS-006`: derive negative paths and testability from cross-system interactions.
- `PASS-010`: prevent deduplication from merging distinct systems or duplicating one owner.


