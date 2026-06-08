# PASS-002: Terminology Consistency

## Purpose

Keep the specification language stable and machine-usable across sections. Terms are part of the implementation contract: drift, hidden synonyms, and ambiguous verbs cause wrong bindings, duplicate entities, and silent merges during normalization.

Source basis: `specification-document-regulation.md` terminology rules; assistant review §14.3; normalizer glossary and TERM-* records §9.

## Activation / Not applicable

**Activate when:** domain terms, states, resources, UI labels, config keys, or project/domain roles appear in any touched section; generator/normalizer/assistant review runs on narrative requirements.

**Not applicable when:** no domain vocabulary in scope (state reason, e.g. meta-only edit).

**Required report if N/A:** one-line scope note.

## Checklist (numbered)

1. Confirm glossary/terminology section exists when the feature has domain entities, resources, states, actions, or UI concepts.
2. For each critical term: canonical name, type/role, allowed synonyms (if confirmed), status (Confirmed / Proposed / Open Question).
3. Hunt drift: different names for the same object across flow, data, UI without confirmed synonym.
4. Hunt overload: one label for two entities without distinct definitions.
5. Flag vague phrasing: “normally”, “as usual”, “handle correctly”, “by analogy” without expansion.
6. Verify ownership language: creator, holder, releaser, lifecycle boundary, facade vs controller vs view vs storage.
7. Separate requirement vs proposal vs open question in phrasing.
8. Check action verb consistency for the same behavior (open vs show vs display vs launch).
9. Normalizer: TERM-* or glossary entries link to REQ/DATA/UI addresses that use the term.
10. Do not silently merge similar terms without user decision or DEC-* record.
11. Exclude Unity/C# API vocabulary from glossary/TERM-* records: framework/library types, methods, properties, events, attributes, namespaces, interfaces, and language keywords are referenced as code/API, not defined as product terminology.
12. Exclude concrete decomposition signatures from glossary/TERM-* records. If a decomposition/implementation-contract entity has a confirmed type, method, property, field, event, or signature name, use that exact signature everywhere instead of creating a duplicate terminology entry.

## Boundary: terminology vs signatures

Glossary/TERM-* is for project/domain vocabulary that needs semantic disambiguation: feature nouns, domain states, resources, player/UI concepts, config concepts, and role names that are not already defined by a concrete signature.

Do **not** add glossary rows for:

- Unity/C# API and framework vocabulary, e.g. `Sprite`, `ScriptableObject`, `EventHandler<T>`, `[SerializeField]`, `IReadOnlyList<T>`, `MonoBehaviour`, `DateTime`;
- language/API mechanics, e.g. `bool`, `out`, `const`, property, method, interface, event, enum, namespace;
- decomposition entities already described by a concrete signature, e.g. `QuestLifecycleOrchestrator`, `IQuestsModuleFacade`, `TryStartQuest`, `durationSeconds`, `MementoChanged`.

When such a signature is confirmed in decomposition or implementation contract:

1. keep its definition, role, owner, parameters, side effects, and lifecycle in decomposition / implementation contract;
2. reference the entity everywhere by the exact recorded signature (case, generic arity, property/method name, and parameters when the full signature is relevant);
3. do not introduce a glossary alias to "normalize" the signature;
4. treat spelling/case drift as a PASS-002 finding even though no TERM-* row exists.

## Failure signals

- Glossary missing while Implementation Contract uses product nouns.
- Two unqualified names for one object in AC vs flows.
- REQ references undefined term with no TERM-* or inline definition.
- Synonym used in one section only without glossary alias row.
- Unity/C# API or confirmed decomposition signatures appear as glossary/TERM-* records.
- A confirmed signature appears under multiple spellings/cases or with a glossary alias instead of exact reuse.

## Example finding templates

```text
[Terminology Conflict]
Terms: <A> vs <B>
Location: <section / REQ-id>
Why it matters: <ambiguous binding | duplicate entity risk>
Recommended fix: pick canonical term; add TERM-*; mark other as alias or OQ
```

```text
[Terminology Drift]
Canonical (glossary): <term>
Drift instances: <list of sections/phrases>
Recommended fix: align wording or record confirmed synonym in glossary
```

Structured finding: `F-xxx | PASS-002 | medium | problem | impact | location | recommended_fix`

## Output (link ../pass-loading-policy.md §6)

Report pass status: `pass` | `pass-with-warning` | `block` | `not applicable`.

- Warning/block require structured findings per `../pass-loading-policy.md` §6.
- Terminology blocks in normalizer prevent `Ready` when canonical IDs cannot be assigned safely.

## Mode notes

- **spec-assistant:** after every fragment that introduces a new noun or renames an entity.
- **spec-generator:** before system-mapping second pass; block assembly if domain vocabulary exists but glossary is empty. Dense decomposition made only of confirmed signatures does not require glossary rows for those signatures.
- **spec-normalizer:** TERM-* records must back §3 terminology and §6 registry rows.

## Integration with other passes

- **PASS-003:** term conflicts from two sources → Issues, not silent merge.
- **PASS-004:** ownership terms must match lifecycle/API actor names.
- **PASS-008:** every TERM-* in body must appear in registry and matrix `used_in` links.
- **PASS-010:** dedup must not collapse distinct terms without DEC-*.
## Mode integration notes

- **spec-assistant:** report pass status in review table; map templates to review-full §16 blocks when applicable.
- **spec-generator:** run when profile/extra passes demand; never skip because GDD seems simple.
- **spec-normalizer:** treat block as hard gate; link findings to element IDs when addresses exist.
- **Escalation:** bare warning/block without §6 findings is a contract execution error for all modes.
- **Cross-pass:** re-run dependent passes after fixes (e.g. dedup → anti-weakening, terminology → readiness).
## Reference triggers (quick scan)

- Re-read affected spec sections after any merge, rename, or ID reassignment.
- Quote the smallest source fragment that proves the finding (avoid long dumps).
- If the user asked for a short answer, still run mandatory passes; compress findings, not checks.
- Record 
ot applicable with scope, not silence.
- Prefer restoring source strength over adding new requirements when fixing PASS-001 findings.
- When two passes conflict, report both findings and let the user decide (PASS-003).
- Normalizer: never return Ready while PASS-008 or PASS-009 is block.
- Generator: unresolved PASS-003 block → draft-blocked with findings before assembly.
