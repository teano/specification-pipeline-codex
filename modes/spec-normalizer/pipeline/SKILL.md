# Normalizer Stage: Pipeline

## 1. Purpose

Orchestrate structural normalization: mandatory TOC, preservation scaffold, internal gates, handoff to addressability and readiness stages.

**Does not duplicate pass check text** — runs `review-full` profile + `PASS-008`, `PASS-009`, `PASS-010` per `../../../shared/pass-loading-policy.md` §4.

---

## 2. Inputs

- Draft specification (any shape);
- Allowed sources per `../../../shared/source-priority-policy.md`;
- `../../../shared/specification-document-regulation.md`;
- Core principles, including `../../../shared/core-principles/grounding.md`.

---

## 3. Mandatory 20-section TOC

Final document **must** include these headings in order (empty subsections allowed only when truly N/A with note):

```md
## 1. Source and Working Context
## 2. Normalization Notes
## 3. Source Preservation Notes
## 4. Summary
## 5. Glossary / Terminology
## 6. Machine-Readable Requirement Address Registry
## 7. Product Goals
## 8. Functional Requirements
## 9. UI/UX Requirements
## 10. Data Requirements
## 11. Integration Requirements
## 12. Non-Functional Requirements
## 13. Technical Constraints
## 14. Implementation Contract
## 15. Explicit Decisions
## 16. Acceptance Criteria
## 17. Conflicts and Issues
## 18. Open Questions
## 19. Traceability Matrix
## 20. Readiness Verdict
```

**Never skip:** §3 Preservation Notes, §6 Registry, §19 Matrix, §20 Verdict.

### §15 Explicit Decisions vs §18 Open Questions

Per `../../../shared/specification-document-regulation.md` §7:

| Section | Holds |
|---|---|
| **§18 Open Questions** | Only **unresolved** OQs (blocking or non-blocking). Empty or explicit “none” when all closed. |
| **§15 Explicit Decisions** | Product/meta decisions with **no** single natural home in §8–§14 (accepted risk, scope cut). **Not** a log of closed OQs. |

When an OQ is answered during normalization: weave the answer into §8–§14 (and registry `REQ-*` as needed), remove from §18, optionally note `OQ-00x → REQ-…` under §3 — never duplicate the full answer in §15.

---

## 4. Source Preservation Notes scaffold (§3)

```md
### Preserved
- <source element> → <REQ-id / section>

### Normalized / Merged
- <duplicate or rewrite> → canonical <REQ-id>

### Moved to Issues / Open Questions
- <item> → §17 / §18 reference (still **open**)

### Closed open questions (inline only)
- OQ-00x → <REQ-id / §8–§14>; removed from §18; no “closed decisions” table

### Not Preserved
- <item> + rationale (only with explicit reason)

### Weakening Risks
- <PASS-001 findings or "none in scope">
```

---

## 5. Execution steps

1. Load regulation, principles (including grounding), pass-loading policy, full profile + hard passes.
2. Map source slices → conditional passes (policy §4 slice table).
3. Ground abstract systems/entities into project-domain objects/roles before assigning implementation contract IDs; rewrite abstract decomposition headings when needed, because formal `Grounded as` annotations alone are not enough. Move concrete grounding catalogs into owning decomposition/contract entries; §1/§2-style context stays high-level only. Unresolved grounding becomes §17 issue or §18 open question.
4. Restructure content into TOC; assign provisional IDs. Build §5 Glossary from domain vocabulary only: filter out Unity/C# API names and confirmed decomposition/contract signatures, and keep those signatures in their owning decomposition/§14 records.
5. Run dedup with `PASS-010`; log merges in §3.
6. Run profile passes in order; record per-pass status + findings (policy §6).
7. Hand off to `../addressability-traceability/SKILL.md` for registry/matrix completion.
8. Hand off to `../anti-weakening-readiness/SKILL.md` for final verdict.
9. Emit mode output: status, pass table, aggregated findings, artifact path hint.

---

## 6. Output depth (compact ≠ skip checks)

Per `../../../shared/pass-loading-policy.md` §5:

- **May shorten:** empty matrices, repetitive quotes, chat summary.
- **Must not shorten:** mandatory passes, §3/§6/§19/§20, findings on warning/block, blocking detail from source.

---

## 7. Conditional gates

- Do **not** emit `Ready` at this stage alone.
- Any `PASS-008`/`PASS-009` `block` → final `Blocked` / `Not Ready`.
- `not applicable` passes require stated reason in pass summary table.

---

## 8. Output contract

| Field | Content |
|---|---|
| Status | `in-progress` → final from readiness stage |
| Normalized document | Full 20-section markdown |
| Pass summary | ID, status, finding count |
| Findings | Aggregated per policy §6 |

---

## 9. Failure handling

- `block`/`warning` without findings → contract error; rebuild before delivery.
- Missing TOC section → `PASS-008` block.
- Weakening without preservation note → `PASS-001` warning minimum.

---

## 10. When N/A

Whole normalizer mode N/A when user only wants light review — route to `spec-assistant` per `../../../router/router-map.md`.
