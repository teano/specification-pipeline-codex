# Review Profile: review-light

## Purpose

Fast structural and safety review for iterative drafting.

## Pass IDs

Run in order:

1. `PASS-003`
2. `PASS-002`
3. `PASS-001`
4. `PASS-006`

## Activation

Used by:

* `spec-assistant` review-light — `../shared/pass-loading-policy.md` §4 row «Review-light»;
* `spec-generator` — same profile as baseline per §4 row «Generator run».

Validated in `../router/scenario-validation.md` (Scenario 2, 4).

## Notes

* this profile is default for light review and generator baseline checks;
* pass semantics are defined only in `../shared/passes/*`;
* findings escalation: `../shared/pass-loading-policy.md` §6 (mode layer aggregates).
