# Review Profile: review-full

## Purpose

Deep review for implementation-ready quality and hidden risks.

## Base Profile

Includes all pass IDs from `./review-light.md`.

## Additional Pass IDs

Run after base profile:

5. `PASS-004`
6. `PASS-005`
7. `PASS-007`
8. `PASS-010`

## Activation

Used by:

* `spec-assistant` review-full — `../shared/pass-loading-policy.md` §4 row «Review-full»;
* `spec-normalizer` — baseline profile per §4 row «Normalizer run» (plus `PASS-008`, `PASS-009`, `PASS-010`).

Validated in `../router/scenario-validation.md` (Scenario 3, 5).

## Notes

* this profile is used for full assistant review and as normalizer baseline;
* pass semantics are defined only in `../shared/passes/*`;
* findings escalation: `../shared/pass-loading-policy.md` §6 (mode layer aggregates).
