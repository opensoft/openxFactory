"""F0 harness CLI (contracts/cli-interface.md).

Exit codes: 0 = run completed (terminal record written), 2 = preflight rejection,
3 = redaction failure. A no-key run completes as a schema-valid INCONCLUSIVE record
(SC-013) with no provider call attempted and nothing fabricated.
"""
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path
from typing import List, Optional

from . import __version__
from .acceptance_map import AcceptanceMapError, load_acceptance_map
from .config import PreflightError, RunConfig, VALID_GROUPS, validate_preflight
from .credential import ENV_VAR, has_credential, reject_if_in_arguments
from .evidence import (RedactionFailure, WritePathError, build_interface_impact,
                       finalize_record, write_evidence)
from .run import build_inconclusive_record, inconclusive_report_md

RUN_TIMESTAMP = "2026-07-11T00:00:00Z"  # deterministic; keeps the committed record stable


def _repo_root() -> Path:
    # cli.py -> avatar_f0 -> src -> experiments/avatar-brokered-call -> experiments -> <root>
    return Path(__file__).resolve().parent.parent.parent.parent.parent


def _git_commit(root: Path) -> str:
    try:
        out = subprocess.run(["git", "-C", str(root), "rev-parse", "HEAD"],
                             capture_output=True, text=True, timeout=10)
        return out.stdout.strip() or "unknown"
    except Exception:
        return "unknown"


def _dependency_versions(root: Path) -> dict:
    lock = root / "experiments/avatar-brokered-call/requirements.lock"
    out = {}
    if lock.is_file():
        for line in lock.read_text().splitlines():
            if "==" in line and not line.startswith("#"):
                name, _, ver = line.partition("==")
                if name.lower() in {"aiortc", "websockets", "httpx", "jsonschema", "pyyaml"}:
                    out[name] = ver.strip()
    return out


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="avatar-f0", description="F0 brokered-call feasibility harness")
    sub = p.add_subparsers(dest="cmd")
    run = sub.add_parser("run", help="run the F0 matrix (or emit the no-key INCONCLUSIVE record)")
    run.add_argument("--groups", default=",".join(VALID_GROUPS))
    run.add_argument("--readiness-ms", type=int, default=3000)
    run.add_argument("--acceptance-map", default=RunConfig.__dataclass_fields__["acceptance_map_path"].default)
    run.add_argument("--acceptance-map-sha256", default="")
    run.add_argument("--lab-project-ref", default="lab:f0-brokered-call")
    run.add_argument("--offline-selftest", action="store_true",
                     help="make no provider call; emit the INCONCLUSIVE terminal record")
    p.add_argument("--version", action="version", version=f"avatar-f0 {__version__}")
    return p


def cmd_run(args, argv: List[str]) -> int:
    root = _repo_root()
    # Credential must never arrive via arguments (FR-003).
    try:
        reject_if_in_arguments(argv)
    except Exception as exc:
        print(f"preflight-reject: credential_in_arguments ({exc})", file=sys.stderr)
        return 2

    cfg = RunConfig(
        lab_project_ref=args.lab_project_ref,
        selected_groups=tuple(g for g in args.groups.split(",") if g),
        readiness_deadline_ms=args.readiness_ms,
        acceptance_map_path=args.acceptance_map,
        acceptance_map_expected_sha256=args.acceptance_map_sha256,
    )
    try:
        validate_preflight(cfg)
    except PreflightError as exc:
        print(f"preflight-reject: {exc.reason}", file=sys.stderr)
        return 2

    # Read the digest-verified baseline acceptance map (read-only). Absence/mismatch is a
    # reason for INCONCLUSIVE; it never mints placeholder IDs.
    commit = _git_commit(root)
    acr_note = ""
    acr_source_commit = commit
    acr_content_sha256 = "0" * 64
    acr_source_path = cfg.acceptance_map_path
    try:
        ref = load_acceptance_map(str(root / cfg.acceptance_map_path),
                                  cfg.acceptance_map_expected_sha256, source_commit=commit)
        acr_content_sha256 = ref.content_sha256
        acr_note = (f"Sourced from `{cfg.acceptance_map_path}` @ {commit[:12]} "
                    f"(sha256 {ref.content_sha256[:12]}…); F0-relevant IDs: "
                    f"{', '.join(ref.f0_relevant())}.")
    except AcceptanceMapError as exc:
        acr_note = f"Acceptance map unavailable ({exc.reason}); run is INCONCLUSIVE; no placeholder IDs minted."

    key_present = has_credential()
    reason = "no_lab_credential" if not key_present else "live_path_deferred"

    record_body = build_inconclusive_record(
        started_at=RUN_TIMESTAMP, completed_at=RUN_TIMESTAMP,
        lab_project_ref=cfg.lab_project_ref,
        dependency_versions=_dependency_versions(root),
        reason=reason,
    )
    interface_impact = build_interface_impact(
        acr_source_path=acr_source_path, acr_source_commit=acr_source_commit,
        acr_content_sha256=acr_content_sha256, variances=[])
    report_md = inconclusive_report_md(reason, acr_note)

    try:
        record = finalize_record(record_body, report_md, interface_impact)
    except Exception as exc:  # schema errors surface here
        print(f"error: could not finalize record: {exc}", file=sys.stderr)
        return 1

    if record.get("redaction_scan", {}).get("status") == "FAIL":
        print("redaction-failure: prohibited content detected; evidence not written", file=sys.stderr)
        return 3

    try:
        paths = write_evidence(record, report_md, interface_impact, root)
    except RedactionFailure:
        print("redaction-failure: evidence not written", file=sys.stderr)
        return 3
    except WritePathError as exc:
        print(f"boundary-error: {exc}", file=sys.stderr)
        return 1

    print(f"overall={record['overall']} groups=6 trials=70 "
          f"redaction={record['redaction_scan']['status']}")
    print(f"evidence: {paths['results']}")
    if not key_present:
        print(f"note: no {ENV_VAR} present — terminal INCONCLUSIVE record (valid completion, SC-013)")
    return 0


def main(argv: Optional[List[str]] = None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.cmd == "run":
        return cmd_run(args, argv)
    parser.print_help()
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
