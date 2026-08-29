# GameDev helper sidecar

Read this reference only when the caller supplies `GAMEDEV_HELPER_REQUEST_PATH`.
It adds provenance I/O around the normal specification workflow; it does not
change routing, stages, passes, findings, or `not applicable` policy.

## Before the mode runs

1. Read the request as immutable input. Do not create or normalize it.
2. Verify that its exact route matches the selected mode:
   - `generation` -> `spec-generator` with the request's `new` or `continue`
     target operation;
   - `correction` -> `spec-assistant` -> `fragment-capture` with `continue`.
3. Verify the current specification bytes against the request's exact input
   SHA, or confirm its explicit `absent` marker. Stop on drift.
4. Restrict durable writes to the request's exact `allowed_write_paths`.
   Project source, configuration, tests, and every other path remain forbidden.

## After the mode passes

Only after the normal selected mode and all of its mandatory checks finish with
generic outcome `PASS`:

1. write the helper-owned report and coverage artifacts to the exact paths in
   the request; their internal format remains owned by this skill;
2. run:

```text
python scripts/emit_helper_result.py --request <GAMEDEV_HELPER_REQUEST_PATH>
```

The emitter validates the immutable request, external-skill fingerprints,
output specification, exact durable write set, and report/coverage artifacts,
then atomically creates the one canonical result sidecar. Do not handcraft,
reconstruct, normalize, or overwrite that JSON. A blocked/warning outcome,
missing artifact, stale input, unexpected write, or emitter failure produces no
PASS result sidecar.
