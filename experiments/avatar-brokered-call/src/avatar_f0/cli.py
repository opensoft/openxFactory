"""F0 harness CLI (contracts/cli-interface.md).

Exit codes: 0 = run completed (terminal record written), 2 = preflight rejection,
3 = redaction failure. A no-key run completes as a schema-valid INCONCLUSIVE record
(SC-013) with no provider call attempted and nothing fabricated.
"""
from __future__ import annotations

import argparse
import asyncio
import subprocess
import sys
from pathlib import Path
from typing import List, Optional

# THE DECLARED SENTINEL VOCABULARY, IMPORTED RATHER THAN RETYPED
# (`fix-pin-value-boundary-and-sentinel-split`, Q3 ruled 2026-08-28). A
# generator writing one of these spellings imports the name, which is the whole
# difference between a vocabulary and a habit: a retyped literal drifts from the
# declaration silently, and the value it writes is read by a verification that
# guards on the exact string.
#
# THE PATH INSERTION IS THE CROSS-PACKAGE PART AND IS STATED RATHER THAN HIDDEN.
# `doc_health.pin_sentinels` lives under `<root>/scripts/` and this harness
# lives under `<root>/experiments/`, so neither is on the other's import path by
# construction. The module depends on nothing outside the standard library,
# which is why it can be reached this way at all — the same reasoning
# `scripts/proposal-support.py` records for its own insertion. Q3 ruled the
# import in for THIS instance and legislated no general rule; if a second
# generator retypes a literal, that is the evidence for one.
_SCRIPTS_DIR = str(Path(__file__).resolve().parents[4] / "scripts")
if _SCRIPTS_DIR not in sys.path:
    sys.path.insert(0, _SCRIPTS_DIR)
from doc_health import pin_sentinels  # noqa: E402

from . import __version__
from .acceptance_map import AcceptanceMapError, load_acceptance_map
from .config import PreflightError, RunConfig, VALID_GROUPS, validate_preflight
from .credential import ENV_VAR, has_credential, load_credential, reject_if_in_arguments
from .evidence import (RedactionFailure, WritePathError, build_interface_impact,
                       finalize_record, write_evidence)
from .redaction import scan_log
from .run import build_inconclusive_record, inconclusive_report_md


def _redacted(text: str) -> str:
    """Never surface raw diagnostic/crash text that trips a redaction rule.

    FR-017 requires prohibited content to be excluded from ALL logs, traces, and
    crash output — including exception messages printed to stderr, which could
    otherwise leak a credential or identifier captured in the raised error.
    """
    return str(text) if not scan_log(str(text)) else "[redacted: prohibited content]"

RUN_TIMESTAMP = "2026-07-11T00:00:00Z"  # deterministic; keeps the committed record stable


def _repo_root() -> Path:
    # cli.py -> avatar_f0 -> src -> experiments/avatar-brokered-call -> experiments -> <root>
    return Path(__file__).resolve().parent.parent.parent.parent.parent


def _git_file_commit(root: Path, relpath: str) -> str:
    """The commit that last modified ``relpath`` — the file's provenance (FR-018).

    WHERE NO COMMIT NAME CAN BE WRITTEN, THE SENTINEL WRITTEN NAMES THE
    CONDITION THAT ACTUALLY HELD (`fix-pin-value-boundary-and-sentinel-split`).
    Until this branch existed, `out.returncode` was never read and a single
    ``"unknown"`` was returned by two different failures: a git run that
    SUCCEEDED and found no commit holding the path, and a git run that FAILED
    and produced nothing because it failed. Those are different facts about the
    repository and the vocabulary declares a different member for each, so the
    return code has to be read before either can be written honestly.
    """
    try:
        out = subprocess.run(
            ["git", "-C", str(root), "log", "-1", "--format=%H", "--", relpath],
            capture_output=True, text=True, timeout=10)
        if out.returncode != 0:
            # The repository's own history could not be read at all — nothing
            # about the content was established (unreadable-repository).
            return pin_sentinels.UNCOMMITTED
        # A SUCCESSFUL run that named no commit: the repository is readable,
        # HEAD resolves, and this content is held by no commit (dirty-worktree
        # — the content is real and no commit name describes it).
        return out.stdout.strip() or pin_sentinels.UNCOMMITTED_WORKTREE
    except Exception:
        # The call itself did not complete (timeout, git absent, not a
        # repository): unreadable-repository, the same condition the non-zero
        # return code names.
        return pin_sentinels.UNCOMMITTED


def _git_head(root: Path) -> str:
    """The current HEAD commit — the F0 source commit this evidence is produced at.

    ONE CONDITION WEARING THREE SPELLINGS OF THE SAME FAILURE. There is no
    success that answers empty, so the empty-output return and the exception
    return name the identical unreadable-repository condition and write the
    identical member.

    THE THIRD SPELLING WAS MEASURED AT REALIZATION AND IS WHY THE RETURN CODE
    IS READ HERE TOO. `fix-pin-value-boundary-and-sentinel-split` § 3.3 reasoned
    that a failed `rev-parse HEAD` always produces nothing and that no return
    code branch was therefore needed. Measured against git rather than assumed,
    that is false in one case: on an UNBORN `HEAD` the command prints the
    literal string `HEAD` on stdout and exits non-zero, so the unguarded form
    returned `"HEAD"` — a value that is neither a commit name nor a declared
    sentinel, written as though it were the repository's revision. The
    vocabulary already assigns that case to this member by name
    (`unreadable-repository`: "`rev-parse HEAD` failed, `HEAD` is unborn, or the
    path is not a repository"), so reading the return code changes no ruled
    member; it only stops a third failure being spelled as a pin.
    """
    try:
        out = subprocess.run(
            ["git", "-C", str(root), "rev-parse", "HEAD"],
            capture_output=True, text=True, timeout=10)
        if out.returncode != 0:
            return pin_sentinels.UNCOMMITTED
        return out.stdout.strip() or pin_sentinels.UNCOMMITTED
    except Exception:
        return pin_sentinels.UNCOMMITTED


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
    run.add_argument("--acceptance-map-sha256",
                     default=RunConfig.__dataclass_fields__["acceptance_map_expected_sha256"].default)
    run.add_argument("--lab-project-ref", default="lab:f0-brokered-call")
    run.add_argument("--offline-selftest", action="store_true",
                     help="make no provider call; emit the INCONCLUSIVE terminal record")
    run.add_argument("--live", action="store_true",
                     help="execute the REAL provider matrix (billed). Requires OPENAI_API_KEY; "
                          "without --live a run stays offline/INCONCLUSIVE even with a key present.")
    p.add_argument("--version", action="version", version=f"avatar-f0 {__version__}")
    return p


def _run_live(root, cfg):
    """Drive the real provider matrix and return (record_body, report_md)."""
    from .candidate import CandidateProfile, dependency_lock_digest
    from .fixture import generate_fixture
    from .live_runner import (LiveEnv, build_session_config, live_report_md,
                              real_live_components, run_live_matrix)

    key = load_credential()
    lock_path = root / "experiments/avatar-brokered-call/requirements.lock"
    lock_text = lock_path.read_text() if lock_path.is_file() else ""
    fixture = generate_fixture()
    harness_rev = _git_file_commit(root, "experiments/avatar-brokered-call/src/avatar_f0")[:12]
    # Full HEAD is recorded in the evidence as source_commit so the kernel publication gate's
    # commit_match can succeed; the kernel owner pins this same commit as f0_source_commit.
    source_commit = _git_head(root)
    candidate = CandidateProfile(
        harness_revision=harness_rev,
        dependency_lock_sha256=dependency_lock_digest(lock_text),
        fixture_bytes_sha256=fixture.sha256,
        fixture_params=fixture.params,
    )
    env = LiveEnv(components=real_live_components(key, fixture.pcm16),
                  session_config=build_session_config(candidate),
                  deadline_ms=cfg.readiness_deadline_ms)
    record_body = asyncio.run(run_live_matrix(
        env, candidate, groups=list(cfg.selected_groups),
        lab_project_ref=cfg.lab_project_ref,
        dependency_versions=_dependency_versions(root),
        started_at=RUN_TIMESTAMP, completed_at=RUN_TIMESTAMP,
        source_commit=source_commit,
    ))
    return record_body, live_report_md(record_body)


def cmd_run(args, argv: List[str]) -> int:
    root = _repo_root()
    # Credential must never arrive via arguments (FR-003).
    try:
        reject_if_in_arguments(argv)
    except Exception as exc:
        print(f"preflight-reject: credential_in_arguments ({_redacted(str(exc))})", file=sys.stderr)
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
    # reason for INCONCLUSIVE; it never mints placeholder IDs. Provenance is the commit
    # that last modified the map file (FR-018 "that map's source commit"), not harness HEAD.
    map_commit = _git_file_commit(root, cfg.acceptance_map_path)
    acr_note = ""
    acr_source_commit = map_commit
    acr_content_sha256 = "0" * 64
    acr_source_path = cfg.acceptance_map_path
    try:
        ref = load_acceptance_map(str(root / cfg.acceptance_map_path),
                                  cfg.acceptance_map_expected_sha256, source_commit=map_commit)
        acr_content_sha256 = ref.content_sha256
        acr_note = (f"Sourced from `{cfg.acceptance_map_path}` @ {map_commit[:12]} "
                    f"(sha256 {ref.content_sha256[:12]}…); F0-relevant IDs: "
                    f"{', '.join(ref.f0_relevant())}.")
    except AcceptanceMapError as exc:
        acr_note = f"Acceptance map unavailable ({exc.reason}); run is INCONCLUSIVE; no placeholder IDs minted."

    key_present = has_credential()
    live_requested = bool(getattr(args, "live", False))
    interface_impact = build_interface_impact(
        acr_source_path=acr_source_path, acr_source_commit=acr_source_commit,
        acr_content_sha256=acr_content_sha256, variances=[])

    if key_present and live_requested:
        # Supervised live run: drive the REAL provider matrix (billed). Any provider/network
        # failure surfaces as INCONCLUSIVE (never a fabricated PASS). A raw traceback could
        # carry SDP/provider text, so any escaping error is redacted and degraded to a
        # terminal INCONCLUSIVE record here (FR-017 / FR-004) — never printed verbatim.
        try:
            record_body, report_md = _run_live(root, cfg)
            reason = "live_run"
        except Exception as exc:
            print(f"live-run-error: {_redacted(str(exc))}", file=sys.stderr)
            reason = "offline_inconclusive"
            record_body = build_inconclusive_record(
                started_at=RUN_TIMESTAMP, completed_at=RUN_TIMESTAMP,
                lab_project_ref=cfg.lab_project_ref,
                dependency_versions=_dependency_versions(root), reason=reason)
            report_md = inconclusive_report_md(reason, acr_note)
    else:
        # Offline INCONCLUSIVE. The persisted artifact is reason-invariant (byte-identical
        # whether or not a key is present); key presence only affects the stderr note.
        reason = "offline_inconclusive"
        record_body = build_inconclusive_record(
            started_at=RUN_TIMESTAMP, completed_at=RUN_TIMESTAMP,
            lab_project_ref=cfg.lab_project_ref,
            dependency_versions=_dependency_versions(root),
            reason=reason,
        )
        report_md = inconclusive_report_md(reason, acr_note)

    # Feed the run's own diagnostic text through the redaction log-scan so FR-017's
    # "all logs/traces/crash output" coverage is active on the live path, not latent.
    emitted_logs = "\n".join([
        f"reason={reason}",
        acr_note,
        f"lab_project_ref={cfg.lab_project_ref}",
    ])
    try:
        record = finalize_record(record_body, report_md, interface_impact,
                                 emitted_logs=emitted_logs)
    except Exception as exc:  # schema errors surface here
        print(f"error: could not finalize record: {_redacted(str(exc))}", file=sys.stderr)
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
        print(f"boundary-error: {_redacted(str(exc))}", file=sys.stderr)
        return 1

    print(f"overall={record['overall']} groups=6 trials=70 "
          f"redaction={record['redaction_scan']['status']}")
    print(f"evidence: {paths['results']}")
    if reason == "live_run":
        print(f"note: supervised LIVE provider run — terminal {record['overall']} record")
    elif not key_present:
        print(f"note: no {ENV_VAR} present — terminal INCONCLUSIVE record (valid completion, SC-013)")
    else:
        print(f"note: {ENV_VAR} present but --live not passed — offline INCONCLUSIVE (safe default)")
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
