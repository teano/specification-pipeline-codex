# Normalizer Stage: Anti-Weakening and Readiness

## 1. Purpose

Final anti-weakening confirmation and **readiness verdict** after all passes.

Executes **`PASS-001`** (comparison to source) and **`PASS-009`** per pass files.

---

## 2. Readiness verdict dimensions

Score each before labeling §20:

| Dimension | Pass / source |
|---|---|
| Source coverage | Preservation notes §3 |
| Anti-weakening | PASS-001 |
| Addressability | PASS-008 |
| AC coverage | PASS-008 + §16 |
| Conflicts resolved | PASS-003 + §17 |
| Open questions | §18 — blocking vs non-blocking |
| Terminology | PASS-002 |
| Pass aggregate | All mandatory passes |
| Dedup safety | PASS-010 |

---

## 3. Verdict labels (§20 template)

```md
## 20. Readiness Verdict

### Verdict
`Ready` | `Not Ready` | `Blocked`

### Summary
<1–3 sentences>

### Blocking finding IDs
- F-... (PASS-008)
- ...

### Pass summary
| Pass | Status | Findings |
|---|---|---|
| PASS-001 | pass | 0 |
| ... | ... | ... |

### Conditions for Ready (if Not Ready)
- ...
```

**`Ready` forbidden when:**

- any mandatory pass is `block`;
- `PASS-008` or `PASS-009` not `pass`;
- unresolved blocking conflict or blocking OQ on critical path.

---

## 4. Compact ≠ skip mandatory checks

Re-read `../../../shared/pass-loading-policy.md` §5:

- Verdict text may be short;
- checks on slices present in source still run;
- blocking source details must appear in spec, AC, or preservation notes.

---

## 5. Execution steps

1. Reconcile source vs output using §3 preservation scaffold.
2. Run `PASS-001` with source baseline.
3. Aggregate all pass statuses from pipeline + addressability.
4. Run `PASS-009` checklist; assign verdict.
5. Emit final mode package: document + findings + verdict.

---

## 6. Output contract

| Status | User message |
|---|---|
| `Ready` | Normalized spec is implementation-ready |
| `Not Ready` | Gaps listed with finding IDs |
| `Blocked` | Critical gate failure; do not implement yet |

---

## 7. Failure handling

Declaring `Ready` with failed gate → contract violation.

`warning` aggregate → `Not Ready` unless user explicitly accepts risks (record in §15 Explicit Decisions).