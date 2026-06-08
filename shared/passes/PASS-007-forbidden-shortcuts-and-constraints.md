# PASS-007: Forbidden Shortcuts and Constraints

## Purpose

Detect vague shortcut-friendly wording, lost flexibility clauses, and violations of forbidden formal solutions — language that invites wrong but plausible implementations.

Source basis: assistant §15.6 (flexibility clauses, formal execution risk); generator §12 forbidden shortcuts; regulation §9 review focus.

## Activation / Not applicable

**Activate when:** examples, signatures, caveats, CON-* constraints, or formal execution risk appear in scope.

**Not applicable when:** no examples/flexibility/forbidden-solution slice (state reason).

**Required report if N/A:** one-line scope note.

## Checklist (numbered)

1. Ban vague imperatives without expansion: “handle correctly”, “as needed”, “etc.”, “similar to X” without mapping.
2. **Flexibility clause:** source-allowed options remain explicit; narrowing to single implementation needs DEC-*.
3. **Forbidden formal solutions:** listed anti-patterns (singleton abuse, hidden Find, silent auto-create) not contradicted elsewhere.
4. Examples that look normative must be labeled illustrative OR promoted to REQ with MUST.
5. Signature/API examples match PASS-004 contract fields (params, errors).
6. “Optional” feature language not smuggled into blocking REQ without status change.
7. Generator §12: forbidden patterns not reintroduced in Implementation Contract.
8. Cross-section: §9 Mandatory Approach vs §13 Constraints — no contradiction without ISSUE.
9. Normalizer: CON-* or §13 entries linked to REQ they constrain.
10. Formal execution risk called out when two implementations both satisfy vague text.

## Failure signals

- Single paragraph replaces entire failure-matrix with “edge cases handled”.
- Forbidden pattern required by another REQ.
- Example code block is only place failure behavior is defined.
- Flexibility lost after “cleanup” edit (see PASS-001).

## Example finding templates

```text
[Forbidden Shortcut Risk]
Phrase: "<quote>"
Location: <section / REQ-id>
Formal execution risk: <wrong impl A vs B>
Recommended fix: measurable criteria; split REQ; add CON-*
```

```text
[Flexibility Clause Lost]
Was (source): <options/caveat>
Now: <single rigid rule>
Recommended fix: restore options or DEC-* confirming narrowing
```

Structured finding: `F-xxx | PASS-007 | medium | problem | impact | location | recommended_fix`

## Output (link ../pass-loading-policy.md §6)

Report pass status: `pass` | `pass-with-warning` | `block` | `not applicable`.

- Critical formal execution risk on blocking paths → **block**.

## Mode notes

- **spec-generator:** mandatory in `review-light` profile per pass-loading-policy §4.
- **spec-assistant:** review-full block 13 maps here.

## Integration with other passes

- **PASS-001:** narrowing flexibility without decision is weakening.
- **PASS-004:** vague API text overlaps this pass — cite both if needed.
- **PASS-006:** untestable wording often surfaces here first.
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
- End of pass checklist; status must appear in mode output pass table.
