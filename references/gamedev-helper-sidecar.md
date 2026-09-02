# GameDev helper sidecar

Read this reference only when the caller supplies `GAMEDEV_HELPER_REQUEST_PATH`.
The caller must also supply the exact
`GAMEDEV_SPECIFICATION_CONTROLLER_PATH`; it must match the controller path and
SHA-256 recorded in the immutable request. Do not discover, substitute, or infer
that controller binding.
It adds provenance I/O around the normal specification workflow; it does not
change routing, stages, passes, findings, or `not applicable` policy.

## Before the mode runs

1. Read the request as immutable input. Do not create or normalize it.
2. Verify and retain the paired `GAMEDEV_SPECIFICATION_CONTROLLER_PATH` exact
   resolved path/SHA binding for the post-mode preflight. Do not execute the
   controller during semantic work.
3. Verify that the request's exact route matches the selected mode:
   - `generation` -> `spec-generator` with the request's `new` or `continue`
     target operation;
   - `correction` -> `spec-assistant` -> `fragment-capture` with `continue`.
4. Verify the current specification bytes against the request's exact input
   SHA, or confirm its explicit `absent` marker. Stop on drift.
5. Restrict durable writes to the request's exact `allowed_write_paths`.
   Project source, configuration, tests, and every other path remain forbidden.

## After the mode passes

Only after the normal selected mode and all of its mandatory checks finish with
generic outcome `PASS`:

1. write the helper-owned report and coverage artifacts to the exact paths in
   the request; their internal format remains owned by this skill;
2. run:

```text
python scripts/emit_helper_result.py \
  --controller <GAMEDEV_SPECIFICATION_CONTROLLER_PATH> \
  --request <GAMEDEV_HELPER_REQUEST_PATH>
```

The emitter validates the immutable request, external-skill fingerprints,
output specification, exact durable write set, and report/coverage artifacts.
Before starting a subprocess, it requires the resolved `--controller` path and
current SHA-256 to equal the request's controller binding. It then runs, without
a shell, that exact controller as:

```text
python -B <GAMEDEV_SPECIFICATION_CONTROLLER_PATH> \
  --project-root <project_root from GAMEDEV_HELPER_REQUEST_PATH> \
  preflight-helper-output \
  --request <GAMEDEV_HELPER_REQUEST_PATH>
```

The controller preflight must exit successfully and return its exact schema-1
JSON envelope. It validates canonical PRD trace plus one positive integer
specification revision, `status: draft|approved`, and language equal to the
request-bound approved PRD language. The emitter verifies the request-bound
controller path and SHA-256 again through the envelope, request ID and exact-byte
SHA-256, and output repository-relative path and exact-byte SHA-256. Only after
that binding passes may it atomically create the one canonical result sidecar.
Do not handcraft, reconstruct, normalize, or overwrite that JSON. A
blocked/warning outcome, missing artifact, stale input, unexpected write,
controller rejection, malformed or mismatched preflight envelope, or emitter
failure produces no PASS result sidecar.
