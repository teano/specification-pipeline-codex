# Pass Loading Policy

## 1. Purpose and scope

Deterministic loading of `PASS-*` by mode/scenario without duplicating pass logic in mode files.

Atomic pass semantics live only in `./passes/*`.


---

## 2. Pass Registry

| Pass ID | File |
|---|---|
| `PASS-001` | `./passes/PASS-001-anti-weakening.md` |
| `PASS-002` | `./passes/PASS-002-terminology-consistency.md` |
| `PASS-003` | `./passes/PASS-003-source-grounding-and-conflicts.md` |
| `PASS-004` | `./passes/PASS-004-api-lifecycle-ownership.md` |
| `PASS-005` | `./passes/PASS-005-data-config-integrity.md` |
| `PASS-006` | `./passes/PASS-006-edge-cases-and-testability.md` |
| `PASS-007` | `./passes/PASS-007-forbidden-shortcuts-and-constraints.md` |
| `PASS-008` | `./passes/PASS-008-machine-addressability-traceability.md` |
| `PASS-009` | `./passes/PASS-009-readiness-verdict-gate.md` |
| `PASS-010` | `./passes/PASS-010-deduplication-safety.md` |

---

## 3. Profile Mapping

Profiles:

* `../review-profiles/review-light.md`
* `../review-profiles/review-full.md`

Intent → mode routing: `../router/router-map.md`.
Scenario validation (happy path, edge, escalation): `../router/scenario-validation.md`.

Rules:

1. profile files reference pass IDs only;
2. mode files add orchestration/gate/output;
3. mode files do not copy pass check text.

---

## 4. Scenario-to-Pass Matrix

| Scenario | Mode | Profiles | Extra passes | Effective set |
|---|---|---|---|---|
| Fragment capture | `spec-assistant` | none | `PASS-002`, `PASS-003` | terminology + grounding |
| Review-light | `spec-assistant` | `review-light` | none | profile set |
| Review-full | `spec-assistant` | `review-full` | none | profile set |
| Generator run | `spec-generator` | `review-light` | `PASS-004`, `PASS-005`, `PASS-007`, `PASS-010` | light + generation safety |
| Normalizer run | `spec-normalizer` | `review-full` | `PASS-008`, `PASS-009`, `PASS-010` | full + hard gate + readiness |

### Conditional activation (not applicable)

Profile passes are **mandatory** for the scenario unless a row below applies. When a source slice is present, the mapped pass is **mandatory** even in compact output (see §5). Slice names align with normalizer §7.3; semantics live only in `./passes/PASS-*.md`.

| Slice in source | Pass ID | Pass file | Not applicable when | Required report |
|---|---|---|---|---|
| Anti-weakening (baseline compare) | `PASS-001` | `./passes/PASS-001-anti-weakening.md` | no prior/source baseline | reason + scope |
| Terminology / glossary / drift | `PASS-002` | `./passes/PASS-002-terminology-consistency.md` | no domain terminology in scope | reason |
| Grounding / source conflicts | `PASS-003` | `./passes/PASS-003-source-grounding-and-conflicts.md` | editorial-only, zero semantic change | confirm editorial-only |
| **Public API** / operations / commands | `PASS-004` | `./passes/PASS-004-api-lifecycle-ownership.md` | no public API slice | reason + sections reviewed |
| **Lifecycle** / init / close / save / cleanup / continuation | `PASS-004` | same | no lifecycle side effects | reason + sections reviewed |
| **Ownership/async** / pooling / subscriptions / tweens | `PASS-004` | same | no ownership/async rules | reason |
| **Responsibility conflict** / overlapping roles | `PASS-004` | same | no conflicting ownership statements | reason |
| **Persistence** / storage / files / metadata | `PASS-005` | `./passes/PASS-005-data-config-integrity.md` | no data/config/persistence | reason |
| **Placeholder/testability** / MVP enum / test-only values | `PASS-006` | `./passes/PASS-006-edge-cases-and-testability.md` | no testable MVP data or flows | reason |
| **Derived edge cases** / validation / failure paths | `PASS-006` | same | no derivable edge cases from API/lifecycle/data | reason |
| **Flexibility clause** / examples / signatures / caveats | `PASS-007` | `./passes/PASS-007-forbidden-shortcuts-and-constraints.md` | no examples or flexibility caveats | reason |
| **Forbidden shortcuts** / formal execution risk | `PASS-007` | same | no shortcut or CON risk in scope | reason |
| Machine addressing / registry / traceability | `PASS-008` | `./passes/PASS-008-machine-addressability-traceability.md` | outside `spec-normalizer` | `outside spec-normalizer run` |
| Readiness verdict / completion gate | `PASS-009` | `./passes/PASS-009-readiness-verdict-gate.md` | outside `spec-normalizer` | `outside spec-normalizer run` |
| Deduplication / merge / canonical placement | `PASS-010` | `./passes/PASS-010-deduplication-safety.md` | no deduplication this run | `no deduplication performed` |

**Pass ↔ slice quick map**

| Pass | Primary slices |
|---|---|
| `PASS-001` | Anti-weakening (when baseline exists) |
| `PASS-002` | Terminology |
| `PASS-003` | Source grounding, conflicts |
| `PASS-004` | Public API, Lifecycle, Ownership/async, Responsibility conflict |
| `PASS-005` | Persistence, data/config |
| `PASS-006` | Placeholder/testability, Derived edge cases |
| `PASS-007` | Flexibility clause, Forbidden shortcuts |
| `PASS-008` | Machine addressability (`spec-normalizer` only) |
| `PASS-009` | Readiness / completion gate (`spec-normalizer` only) |
| `PASS-010` | Deduplication safety |

If slice absent: do not fabricate a large section; note: `No explicit <slice> requirements found.`

Skipping a mandatory pass without `not applicable` is forbidden.

---

## 5. Output Depth Policy

Goal: **compact output without skipping mandatory checks**.

| May shorten | Must not shorten |
|---|---|
| repetitive explanations | coverage of mandatory passes |
| long source quotes | explicit result per mandatory pass |
| full doc dump in chat | findings on `warning`/`block` |
| summary instead of full registry in chat | registry/traceability in normalizer report (minimum) |

By mode:

* **assistant / review-light:** concise text; findings-first order required; **read-only** on `SPECIFICATION_PATH` (proposed fixes in chat only).
* **review-full / normalizer:** expanded diagnostics for blocking areas; blocking IDs required; **review-full** is read-only on the spec file until the user requests application (`../policies/mode-transition-guards.md` §4.3).
* **generator:** full spec artifact allowed; pass results — compact table + findings.

See also `../policies/mode-transition-guards.md` §5.

---

## 6. Pass Escalation Contract

Pass status (`pass` | `pass-with-warning` | `block` | `not applicable`) is not sufficient for the user.

### Structured finding (required fields)

* `id` — stable finding ID (e.g. `F-001`);
* `pass_id` — `PASS-*`;
* `severity` — `critical` | `high` | `medium` | `warning` | `critical-risk`;
* `problem`;
* `impact`;
* `location` — section / element ID / fragment;
* `recommended_fix`.

### Escalation rules

1. `pass-with-warning` without findings → **contract violation**;
2. `block` without findings → **violation**; mode-level outcome forced to `blocked`;
3. critical-risk must not be reduced to a generic comment without a finding;
4. mode output must include aggregated findings + final status.

Mode files reference this §, not duplicate fields.

---

## 7. Hard Rules

1. `spec-normalizer` always loads `PASS-008` and `PASS-009`;
2. skipping a mandatory pass is forbidden;
3. `not applicable` requires a stated reason, not silence;
4. any pass `block` → final readiness is not `Ready`;
5. `PASS-008`/`PASS-009` blocks must link to specific finding IDs in mode output.

---

## 8. Mode Output Status Mapping

| Pass aggregate | Assistant | Generator | Normalizer |
|---|---|---|---|
| all pass | `ok` | `draft-ok` | eligible for `Ready` after gates |
| any warning | `warning` | `draft-warning` | `Not Ready` |
| any block | `blocked` | `draft-blocked` | `Blocked` / `Not Ready` |

Bare status without findings on `warning`/`block` is a contract execution error.

See negative case: ../router/scenario-validation.md Scenario 12; positive — Scenarios 10–11.
