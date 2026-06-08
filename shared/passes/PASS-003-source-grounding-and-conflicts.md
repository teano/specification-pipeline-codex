# PASS-003: Source Grounding and Conflicts

## Purpose

Ensure normative statements are grounded in identified sources and contradictions are surfaced — never merged silently. Supports generator extraction and assistant/normalizer when external inputs exist.

Source basis: generator grounded extraction and internal analysis; assistant fragment capture; normalizer source priority.

## Activation / Not applicable

**Activate when:**

- GDD, brief, chat fragments, prior spec, or project context report is used;
- `spec-generator` grounded extraction stage runs;
- `fragment-capture` or review compares new text to earlier sources;
- normalizer reconciles source vs output.

**Not applicable when:** structure-only internal edit (state reason).

**Required report if N/A:** e.g. “internal reformat only; no external source slice.”

## Checklist (numbered)

1. Apply `../source-priority-policy.md` ordering.
2. Each requirement-level statement has source location, user confirmation, or labeled `Assumption`.
3. Reject invented gameplay, APIs, paths, namespaces, services, configs, integrations without basis.
4. Tie each mechanic to an owning grounded system/entity from source or project context — not invented controller names. Use `../core-principles/grounding.md` when project context is incomplete.
5. Detect contradictions: dual source of truth; entity owns and disowns same concern; flow vs constraints; platform branch mismatch; path/name drift.
6. Record both conflict sides; do not pick a winner without user or higher-priority source.
7. If later evidence closes an Open Question, integrate the answer **inline** in the canonical requirement/contract section; remove it from Open Questions; trace once in Normalization / Preservation Notes if an ID existed (`../../../shared/specification-document-regulation.md` §7). Do **not** add “closed decisions” or resolved-OQ archive lists.
8. Project context vs project rules → ISSUE/risk/OQ; do not override silently.
9. Grounding gaps → targeted clarification question, Open Question, or minimal labeled Assumption only when allowed — never undifferentiated MUST.
10. Generator: run mandatory internal analysis before prose; surface analysis conflicts in issues/OQ.
11. Assumptions: minimal, labeled, must not add new mechanics.
12. Project rules are implementation-risk checks only — not product requirement sources.
13. A decomposition hierarchy is not grounded if the headings remain abstract analysis categories and only entity cards contain `Grounded as`.
14. A separate project/repository grounding catalog is not a substitute for grounded decomposition; concrete entity placement/signature/owner details must live on the owning decomposition/contract entry.

## Failure signals

- Requirements without source anchor or Assumption label.
- Conflicting parameters or win conditions written as single truth.
- GDD retelling without extractable owned requirements.
- Abstract system/entity wording left ungrounded when project context or `grounding.md` can identify a concrete object/role.
- Formal grounding where `Grounded as` is added but the decomposition hierarchy remains an abstract systems-thinking map.
- Separate "project grounding" / "repository grounding" section duplicates entity placements, signatures, composition, config, persistence, or lifecycle instead of placing them on owning decomposition entries.
- Agent-invented entity/class/path/API/property/behavior used instead of asking what real project object or boundary applies.
- Silent “resolution” of conflict in prose without ISSUE/DEC.
- Closed open question left in §11/§18 plus a duplicate “resolved / closed decisions” section.
- Unresolved OQ or `TBD` scattered in decomposition/flows while §11/§18 is empty or claims “none”.

## Example finding templates

```text
[Source Conflict]
Side A: ... Side B: ...
Impact: ...
Recommended fix: user decision → ISSUE-* / DEC-*.
```

```text
[Ungrounded Requirement]
Statement: ...
Recommended fix: cite source, ask a targeted clarification question, label allowed Assumption, or remove.
```

Structured finding: `F-xxx | PASS-003 | critical | problem | impact | location | recommended_fix`

## Output (link ../pass-loading-policy.md §6)

Unresolved critical conflicts → `block` with §6 findings. Generator must not report `draft-ok` while blocking conflicts remain. Normalizer: ISSUE-* and Readiness not `Ready`.
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
- Record not applicable with scope, not silence.
- Prefer restoring source strength over adding new requirements when fixing PASS-001 findings.
- When two passes conflict, report both findings and let the user decide (PASS-003).
- Normalizer: never return Ready while PASS-008 or PASS-009 is block.
- Generator: unresolved PASS-003 block → draft-blocked with findings before assembly.
