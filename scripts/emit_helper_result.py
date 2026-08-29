#!/usr/bin/env python3
"""Emit one immutable GameDev integration result for a controller request."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
from pathlib import Path
from typing import Any


REQUEST_SCHEMA = 1
RESULT_SCHEMA = 1
REQUEST_KEYS = {
    "schema",
    "request_id",
    "operation",
    "project_root",
    "route",
    "approved_prd",
    "specification",
    "expected_user_language",
    "allowed_write_paths",
    "artifacts",
    "helper_identity",
    "correction_ids",
}
ROUTE_KEYS = {"mode", "submode", "target_operation"}
PRD_KEYS = {"path", "revision", "sha256"}
SPECIFICATION_KEYS = {"path", "input"}
INPUT_ABSENT_KEYS = {"kind"}
INPUT_SHA_KEYS = {"kind", "sha256"}
ARTIFACT_PATH_KEYS = {"helper_report_path", "coverage_path", "result_path"}
IDENTITY_KEYS = {
    "entrypoint_path",
    "entrypoint_sha256",
    "result_emitter_path",
    "result_emitter_sha256",
}


class EmitterError(RuntimeError):
    pass


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def exact_sha(value: Any) -> bool:
    return isinstance(value, str) and re.fullmatch(r"[0-9a-f]{64}", value) is not None


def load_object(path: Path, label: str) -> tuple[bytes, dict[str, Any]]:
    try:
        raw = path.read_bytes()
        value = json.loads(raw.decode("utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as error:
        raise EmitterError(f"{label} must be readable UTF-8 JSON") from error
    if not isinstance(value, dict):
        raise EmitterError(f"{label} must contain one JSON object")
    return raw, value


def project_path(root: Path, relative: Any, label: str) -> Path:
    if not isinstance(relative, str) or not relative or Path(relative).is_absolute():
        raise EmitterError(f"{label} must be one non-empty project-relative path")
    resolved = (root / relative).resolve()
    try:
        canonical = resolved.relative_to(root).as_posix()
    except ValueError as error:
        raise EmitterError(f"{label} escapes the project root") from error
    if canonical != relative:
        raise EmitterError(f"{label} is not canonical")
    return resolved


def validate_request(request_path: Path) -> tuple[bytes, dict[str, Any], dict[str, Path]]:
    request_bytes, request = load_object(request_path, "helper request")
    if set(request) != REQUEST_KEYS or type(request.get("schema")) is not int:
        raise EmitterError("helper request schema is invalid")
    if request["schema"] != REQUEST_SCHEMA:
        raise EmitterError("helper request version is invalid")
    request_id = request.get("request_id")
    if not isinstance(request_id, str) or re.fullmatch(r"HREQ-[0-9]{6}", request_id) is None:
        raise EmitterError("helper request id is invalid")

    root_value = request.get("project_root")
    if not isinstance(root_value, str) or not Path(root_value).is_absolute():
        raise EmitterError("helper request project root is invalid")
    root = Path(root_value).resolve()
    if not root.is_dir():
        raise EmitterError("helper request project root does not exist")
    try:
        request_relative = request_path.resolve().relative_to(root).as_posix()
    except ValueError as error:
        raise EmitterError("helper request must be inside the project root") from error
    if request_relative != f".agentic-pipeline/helper-requests/{request_id}.json":
        raise EmitterError("helper request path is non-canonical")

    route = request.get("route")
    if not isinstance(route, dict) or set(route) != ROUTE_KEYS:
        raise EmitterError("helper request route is invalid")
    operation = request.get("operation")
    correction_ids = request.get("correction_ids")
    if operation == "generation":
        valid_route = (
            route.get("mode") == "spec-generator"
            and route.get("submode") is None
            and route.get("target_operation") in {"new", "continue"}
            and correction_ids == []
        )
    elif operation == "correction":
        valid_route = (
            route
            == {
                "mode": "spec-assistant",
                "submode": "fragment-capture",
                "target_operation": "continue",
            }
            and isinstance(correction_ids, list)
            and bool(correction_ids)
            and all(isinstance(item, str) and item.strip() for item in correction_ids)
            and len(correction_ids) == len(set(correction_ids))
        )
    else:
        valid_route = False
    if not valid_route:
        raise EmitterError("helper request operation/route is invalid")

    prd = request.get("approved_prd")
    if not isinstance(prd, dict) or set(prd) != PRD_KEYS or not exact_sha(prd.get("sha256")):
        raise EmitterError("helper request PRD authority is invalid")
    prd_path = project_path(root, prd.get("path"), "approved PRD path")
    if not prd_path.is_file() or sha256(prd_path) != prd["sha256"]:
        raise EmitterError("helper request PRD bytes are stale")

    specification = request.get("specification")
    if not isinstance(specification, dict) or set(specification) != SPECIFICATION_KEYS:
        raise EmitterError("helper request specification binding is invalid")
    spec_path = project_path(root, specification.get("path"), "specification path")
    input_binding = specification.get("input")
    if not isinstance(input_binding, dict):
        raise EmitterError("helper request specification input is invalid")
    if set(input_binding) == INPUT_ABSENT_KEYS and input_binding.get("kind") == "absent":
        if route.get("target_operation") != "new":
            raise EmitterError("absent specification input requires target operation new")
        input_sha = None
    elif (
        set(input_binding) == INPUT_SHA_KEYS
        and input_binding.get("kind") == "sha256"
        and exact_sha(input_binding.get("sha256"))
    ):
        if route.get("target_operation") != "continue":
            raise EmitterError("SHA-bound specification input requires continue")
        input_sha = input_binding["sha256"]
    else:
        raise EmitterError("helper request specification input is invalid")

    language = request.get("expected_user_language")
    if not isinstance(language, str) or not language.strip():
        raise EmitterError("helper request language is invalid")

    artifact_paths = request.get("artifacts")
    if not isinstance(artifact_paths, dict) or set(artifact_paths) != ARTIFACT_PATH_KEYS:
        raise EmitterError("helper request artifact paths are invalid")
    report_path = project_path(root, artifact_paths["helper_report_path"], "helper report path")
    coverage_path = project_path(root, artifact_paths["coverage_path"], "coverage path")
    result_path = project_path(root, artifact_paths["result_path"], "result path")
    allowed = request.get("allowed_write_paths")
    expected_allowed = [
        specification["path"],
        artifact_paths["helper_report_path"],
        artifact_paths["coverage_path"],
        artifact_paths["result_path"],
    ]
    if allowed != expected_allowed or len(allowed) != len(set(allowed)):
        raise EmitterError("helper request allowed write set is invalid")

    identity = request.get("helper_identity")
    if not isinstance(identity, dict) or set(identity) != IDENTITY_KEYS:
        raise EmitterError("helper request external identity is invalid")
    skill_root = Path(__file__).resolve().parents[1]
    entrypoint = skill_root / "SKILL.md"
    emitter = Path(__file__).resolve()
    expected_identity = {
        "entrypoint_path": str(entrypoint.resolve()),
        "entrypoint_sha256": sha256(entrypoint),
        "result_emitter_path": str(emitter),
        "result_emitter_sha256": sha256(emitter),
    }
    if identity != expected_identity:
        raise EmitterError("helper request external identity fingerprint is stale or foreign")

    if not spec_path.is_file():
        raise EmitterError("helper output specification does not exist")
    output_sha = sha256(spec_path)
    if input_sha is not None and output_sha == input_sha:
        raise EmitterError("helper output specification did not change")
    for path, label in ((report_path, "helper report"), (coverage_path, "coverage")):
        if not path.is_file() or path.stat().st_size == 0:
            raise EmitterError(f"{label} artifact is missing or empty")
    if result_path.exists():
        raise EmitterError("helper result sidecar already exists")

    return request_bytes, request, {
        "root": root,
        "specification": spec_path,
        "report": report_path,
        "coverage": coverage_path,
        "result": result_path,
    }


def emit(request_path: Path) -> Path:
    request_bytes, request, paths = validate_request(request_path.resolve())
    artifacts = request["artifacts"]
    result = {
        "schema": RESULT_SCHEMA,
        "request": {
            "id": request["request_id"],
            "sha256": hashlib.sha256(request_bytes).hexdigest(),
        },
        "operation": request["operation"],
        "route": request["route"],
        "output_specification": {
            "path": request["specification"]["path"],
            "sha256": sha256(paths["specification"]),
        },
        "outcome": "PASS",
        "write_paths": request["allowed_write_paths"],
        "artifacts": [
            {
                "kind": "helper_report",
                "path": artifacts["helper_report_path"],
                "sha256": sha256(paths["report"]),
            },
            {
                "kind": "coverage",
                "path": artifacts["coverage_path"],
                "sha256": sha256(paths["coverage"]),
            },
        ],
        "helper_identity": request["helper_identity"],
    }
    result_path = paths["result"]
    result_path.parent.mkdir(parents=True, exist_ok=True)
    temporary = result_path.with_suffix(result_path.suffix + ".tmp")
    if temporary.exists():
        raise EmitterError("helper result temporary path already exists")
    payload = (json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode(
        "utf-8"
    )
    try:
        with temporary.open("xb") as stream:
            stream.write(payload)
            stream.flush()
            os.fsync(stream.fileno())
        if result_path.exists():
            raise EmitterError("helper result sidecar already exists")
        os.replace(temporary, result_path)
    finally:
        if temporary.exists():
            temporary.unlink()
    return result_path


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--request", required=True)
    args = parser.parse_args(argv)
    try:
        result = emit(Path(args.request))
    except EmitterError as error:
        print(f"error: {error}", file=sys.stderr)
        return 2
    print(str(result))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
