# PASS-004: API, Lifecycle, and Ownership

## Purpose

Verify public API contracts, lifecycle triggers, ownership/async rules, and responsibility boundaries are explicit and non-contradictory. Closes the class of “compiles but wrong owner resumes work” defects at specification time.

Source basis: assistant extended review §15.2–§15.4 (Public API, Lifecycle, Responsibility conflict, Ownership).

## Activation / Not applicable

**Activate when:** slice includes public API, lifecycle side effects, pooling/subscriptions/tweens, or overlapping system roles.

**Not applicable when:** no API/lifecycle/ownership slice (state reason + sections reviewed).

**Required report if N/A:** reason per `../pass-loading-policy.md` conditional activation table.

## Checklist (numbered)

1. **Public API:** operations/commands/events named; inputs/outputs; pre/post conditions; error returns.
2. **Lifecycle:** init, open, pause, resume, save, close, dispose, pool return — each normative path has trigger + actor.
3. **Ownership:** who creates, holds, mutates, releases; async completion and callback unregistration stated where hazardous.
4. **Responsibility conflict:** no two entities own the same decision without split or explicit hierarchy.
5. UI/view does not own domain rules; facades do not accumulate unrelated obligations (God Object pattern).
6. Integration boundaries: which module exposes API vs consumes; version/availability assumptions stated or OQ.
7. Cancellation/teardown: in-flight work behavior when owner destroyed or scope ended.
8. Cross-section consistency: flow diagram actors match Implementation Contract entities.
9. Normalizer: REQ owner field populated for API/lifecycle obligations.
10. Missing trigger for state change described only as “updates” → flag as lifecycle gap.

## Failure signals

- Verb-only API (“handles login”) without contract table or REQ body.
- State changes with no triggering event or calling actor.
- Two owners for same resource lifecycle without DEC-*.
- Pool/subscription mentioned without release/unsubscribe obligation.

## Example finding templates

```text
[Missing API Contract]
Operation: <name>
Location: <section / REQ-id>
Missing: <inputs | errors | caller | thread/context>
Recommended fix: add REQ-* with observable contract
```

```text
[Lifecycle Trigger Loss]
Behavior: <what changes>
Was trigger: <event/phase> (baseline or peer section)
Now: <vague or missing>
Recommended fix: restore trigger + actor; link AC negative path
```

```text
[Responsibility Conflict]
Entities: <A> and <B>
Overlapping duty: <rule/storage/UI>
Recommended fix: split REQ; assign single owner; DEC-* if intentional shared
```

Structured finding: `F-xxx | PASS-004 | high | problem | impact | location | recommended_fix`

## Output (link ../pass-loading-policy.md §6)

Report pass status: `pass` | `pass-with-warning` | `block` | `not applicable`.

- API/lifecycle blocks typically **block** implementation-ready claims until closed or OQ with ISSUE link.

## Mode notes

- **spec-assistant:** extended blocks 10–11 map to this pass; do not duplicate checklist in review SKILL.
- **spec-generator:** system-mapping second pass must feed API/lifecycle slices.
- **spec-normalizer:** §11 Integration + §14 Implementation Contract primary homes.

## Integration with other passes

- **PASS-006:** derive edge cases from API/lifecycle gaps listed here.
- **PASS-001:** dropping failure branches is weakening.
- **PASS-005:** persistence triggers often lifecycle-bound — cross-check save/load owners.
## Mode integration notes

- **spec-assistant:** report pass status in review table; map templates to review-full §16 blocks when applicable.
- **spec-generator:** run when profile/extra passes demand; never skip because GDD seems simple.
- **spec-normalizer:** treat block as hard gate; link findings to element IDs when addresses exist.
- **Escalation:** bare warning/block without §6 findings is a contract execution error for all modes.
- **Cross-pass:** re-run dependent passes after fixes (e.g. dedup → anti-weakening, terminology → readiness).
