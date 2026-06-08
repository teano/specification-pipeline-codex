# Normalizer Stage: Addressability and Traceability

## 1. Purpose

Assign and verify machine-readable IDs, element records, registry gate, and traceability matrix minimum.

Executes **`PASS-008`** semantics only from `../../../shared/passes/PASS-008-machine-addressability-traceability.md`.

---

## 2. REQ element record format

```md
### REQ-001 — <Short title>

| Field | Value |
|---|---|
| id | REQ-001 |
| title | <Short title> |
| normative | yes |
| owner | <system/entity> |
| source | <GDD § / user / decision id> |
| status | draft | confirmed | deprecated |
| related | AC-..., TERM-..., REQ-... |
| verification | AC-001 / test location |

<Normative statement body — testable, one primary obligation per REQ when possible.>
```

Rules:

- One normative obligation per REQ where feasible; split if actors/triggers differ.
- No anonymous `must` bullets in §8–§14 without ID.

---

## 3. AC element record format

```md
### AC-001 — <Short title>

| Field | Value |
|---|---|
| id | AC-001 |
| verifies | REQ-001, REQ-003 |
| type | happy | negative | edge | non-functional |
| precondition | <state> |
| action | <observable trigger> |
| expected | <observable outcome> |
| blocking | yes | no |

<Optional Gherkin-style steps.>
```

Every **blocking** REQ must have ≥1 AC or explicit `verification: <location>` in REQ record.

---

## 4. TERM element record format

```md
### TERM-001 — <Canonical term>

| Field | Value |
|---|---|
| id | TERM-001 |
| term | <Canonical> |
| definition | <Unambiguous definition> |
| aliases | <optional> |
| not_same_as | TERM-002 |
| used_in | REQ-..., sections |
```

TERM-* records are **not** a registry for code/API names. Do not create TERM-* records for Unity/C# API vocabulary or for concrete signatures already described in decomposition / implementation contract.

Examples that stay out of TERM-*:

- Unity/C# API and language/framework names: `Sprite`, `ScriptableObject`, `EventHandler<T>`, `IReadOnlyList<T>`, `bool`, `out`, `const`;
- confirmed project signatures: concrete type names, method names, property names, fields, events, config keys, and full signatures recorded in decomposition or §14.

For signature-bearing entities, machine addressability comes from their owning `REQ-*`, decomposition entry, contract table, or implementation-contract section. The normalizer must still verify exact spelling/case reuse across body text and flag drift through `PASS-002`; it must not solve drift by adding a TERM-* alias.

---

## 5. Registry gate (§6)

Section **Machine-Readable Requirement Address Registry** must list:

| Column | Description |
|---|---|
| id | REQ-* / AC-* / TERM-* |
| kind | requirement | acceptance | term |
| title | short |
| section | document § |
| status | draft/confirmed/deprecated |

**Gate:** every ID in body appears in registry; no registry orphan rows.

---

## 6. Traceability matrix minimum (§19)

Minimum columns:

| REQ id | AC id(s) | Source ref | Owner | Blocking |
|---|---|---|---|---|

Compact specs may use a short table; **matrix must exist**.

Orphan check: REQ with no AC/verification row → `PASS-008` block if blocking.

---

## 7. Execution steps

1. Scan for anonymous normative statements; assign IDs.
2. Build/update element records in canonical sections.
3. Fill registry; cross-check counts.
4. Build matrix; link blocking paths.
5. Run `PASS-008`; emit findings on failure.

---

## 8. Output

- Updated sections §5–§6, §8–§16, §19;
- `PASS-008` status + findings;
- Hand off to anti-weakening-readiness stage.

---

## 9. Failure handling

Registry/matrix omission is **block**, not warning. Cite finding IDs in final verdict.
