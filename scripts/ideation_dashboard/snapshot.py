"""Canonical byte-identical snapshot render/write + load + validation (plan
"snapshot.py"; change task 3.1; FR-002 / SC-001 / SC-002).

Serialization is canonical so two runs over an identical tree yield
BYTE-IDENTICAL bytes: sorted keys (recursively), fixed separators, a trailing
newline, and NO wall-clock — this module never reads the clock; any
`generation.generated_at` is derived upstream from `source_revision`'s commit
date by the generator. List ordering is the generator's responsibility.

Writes go through the interactivity boundary (never around it): `write_snapshot`
takes an `OutputBoundary` and writes only under a declared output path.

Validation is DELEGATED to the pinned openxFactory validator
(`scripts/validate-ideation-dashboard-contracts.py`) — the schema is never
restated here. `validate_or_raise` fails loudly on a non-conforming snapshot.
It reports THREE outcomes: validated, not conformant, and validator
unavailable — see the commentary above `VALIDATED` for why the third one exists.
"""

from __future__ import annotations

import json
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

VALIDATOR_RELPATH = Path("openxFactory") / "scripts" / "validate-ideation-dashboard-contracts.py"


class SnapshotInvalid(Exception):
    """A rendered snapshot failed the pinned validator (or it could not run)."""


# --------------------------- canonical serialization ---------------------------

def canonical_json(snapshot: dict[str, Any]) -> str:
    """Deterministic, diffable JSON: sorted keys, 2-space indent, trailing
    newline (the house canonical-render discipline — see doc_health/runner.py,
    execution_lane/bundler.py)."""
    return json.dumps(snapshot, indent=2, sort_keys=True, ensure_ascii=True) + "\n"


def canonical_bytes(snapshot: dict[str, Any]) -> bytes:
    return canonical_json(snapshot).encode("utf-8")


def load_snapshot(path: Path | str) -> dict[str, Any]:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def write_snapshot(snapshot: dict[str, Any], path: Path | str, boundary) -> Path:
    """Render canonically and write through the interactivity boundary. Every
    snapshot write lands under the boundary's declared output allowlist."""
    return boundary.write_output(path, canonical_json(snapshot))


# --------------------------- validator location ---------------------------

def find_validator(start: Path | None = None) -> Path | None:
    """Walk up from `start` (or cwd) to the aggregation checkout and return the
    pinned validator, or None when no openxFactory checkout is reachable. Keeps
    the module path-agnostic — no absolute path is baked in."""
    base = (start or Path.cwd()).resolve()
    for directory in [base, *base.parents]:
        candidate = directory / VALIDATOR_RELPATH
        if candidate.is_file():
            return candidate
    return None


# --------------------------- validation ---------------------------
#
# THREE outcomes, not two. "the snapshot is wrong" and "the check could not be
# performed" are different facts about the world and they deserve different
# consequences, but a bare `ok = (returncode == 0)` collapses them into one — and
# the collapse shipped: on a host whose python lacks the validator's own
# dependencies the validator exits non-zero, `ok` was False, and
# `generate-and-open` returned before starting the server. A human with a
# perfectly good corpus was told, in effect, that his corpus was bad, and got no
# dashboard. (The bug was latent until PR #51 taught the search to find the
# validator via `--repo-root`: before that the validator was simply not reached
# on the documented launch, validation SKIPPED, and the server started.)

VALIDATED = "validated"
NOT_CONFORMANT = "not-conformant"
VALIDATOR_UNAVAILABLE = "validator-unavailable"

# THE SIGNAL for "unavailable", and why it is not a string match. The pinned
# validator publishes an exit-code contract in its own module docstring —
# "Exit codes: 0 ok, 1 findings (or warnings under --strict), 2 harness error" —
# and honours it: `report()` is the ONLY place a verdict on the DATA is turned
# into a status, and it returns 1 (findings, or warnings under --strict) or 0.
# Every other non-zero exit is environmental: PyYAML absent, jsonschema/
# referencing absent, the schema directory missing, the target path unreadable,
# or the catch-all `ERROR harness failure:` around `main()`. So the classifier
# reads the number, not the prose. Matching the English of one dependency
# message would break on the next wording change, would miss the PyYAML variant
# sitting three lines above it, and would say nothing about a validator that
# could not be launched at all.
FINDINGS_EXIT = 1

# One spelling of the remedy, shared by every surface that has to state it.
DEPENDENCY_REMEDY = "pip install 'jsonschema>=4.18' referencing"


@dataclass
class ValidationResult:
    ok: bool
    returncode: int
    stdout: str
    stderr: str
    validator: Path | None
    # Additive: `outcome` refines `ok` without displacing it, so every existing
    # `if not result.ok` caller keeps its exact behaviour. Left unset it is
    # derived from `ok` under the old two-outcome reading.
    outcome: str | None = None
    unavailable_reason: str | None = None

    def __post_init__(self) -> None:
        if self.outcome is None:
            self.outcome = VALIDATED if self.ok else NOT_CONFORMANT

    @property
    def available(self) -> bool:
        """Did the validator actually reach a verdict? False means NOTHING is
        known about this snapshot's conformance — not that it is bad."""
        return self.outcome != VALIDATOR_UNAVAILABLE

    def summary(self) -> str:
        if self.validator is None:
            return "validator not found (no reachable openxFactory checkout)"
        tail = (self.stdout or self.stderr).strip().splitlines()
        return tail[-1] if tail else f"returncode={self.returncode}"


def _is_readable_json(path: Path) -> bool:
    """Can WE read the file we just handed the validator? This is the one
    attribution the exit code cannot make for us: the validator also exits with
    a harness code when the target file will not parse, and that failure is the
    DATA's, not the environment's. Asking locally keeps a truncated or corrupt
    snapshot classified as non-conformant — so this fix cannot turn a real
    blocking failure into a warning."""
    try:
        json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, ValueError):
        return False
    return True


def validate_snapshot(
    path: Path | str, *, validator: Path | None = None, strict: bool = False,
    search_from: Path | None = None,
) -> ValidationResult:
    """Validate a rendered snapshot file with the pinned validator (single-file
    mode auto-detects `kind`). Returns a result; never raises for a mere
    validation failure — use `validate_or_raise` for loud failure.

    `result.outcome` is one of `VALIDATED`, `NOT_CONFORMANT`, or
    `VALIDATOR_UNAVAILABLE`; `result.ok` stays True only for `VALIDATED`."""
    path = Path(path).resolve()
    validator = validator or find_validator(search_from or path.parent)
    if validator is None:
        return ValidationResult(
            False, -1, "", "validator not found", None, VALIDATOR_UNAVAILABLE,
            f"no {VALIDATOR_RELPATH} is reachable from this run")
    if not Path(validator).is_file():
        # Checked BEFORE launching, because the exit code cannot carry this one:
        # `python3 <a directory>` exits 1 — the validator's own findings code —
        # so a bogus explicitly-passed path would otherwise be read as a verdict
        # against the snapshot. `find_validator` can never produce it (it tests
        # `is_file`), but a caller supplying `validator=` can.
        return ValidationResult(
            False, -1, "", f"not a file: {validator}", Path(validator),
            VALIDATOR_UNAVAILABLE,
            f"the validator path is not a readable file ({validator})")
    cmd = [sys.executable, str(validator), str(path)]
    if strict:
        cmd.append("--strict")
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True)
    except OSError as exc:      # not executable, interpreter gone, ENOMEM, ...
        return ValidationResult(
            False, -1, "", f"{type(exc).__name__}: {exc}", validator,
            VALIDATOR_UNAVAILABLE,
            f"the validator could not be launched with {sys.executable}")
    if proc.returncode == 0:
        return ValidationResult(True, 0, proc.stdout, proc.stderr, validator,
                                VALIDATED)
    if proc.returncode == FINDINGS_EXIT:
        return ValidationResult(False, proc.returncode, proc.stdout, proc.stderr,
                                validator, NOT_CONFORMANT)
    if not _is_readable_json(path):
        return ValidationResult(False, proc.returncode, proc.stdout, proc.stderr,
                                validator, NOT_CONFORMANT)
    return ValidationResult(
        False, proc.returncode, proc.stdout, proc.stderr, validator,
        VALIDATOR_UNAVAILABLE,
        f"the validator exited {proc.returncode}, which is a HARNESS error in its "
        f"own documented contract (0 ok, {FINDINGS_EXIT} findings, 2 harness "
        f"error) — it never reached a verdict on this snapshot")


def validate_or_raise(
    path: Path | str, *, validator: Path | None = None, strict: bool = False,
    search_from: Path | None = None,
) -> ValidationResult:
    """Validate and raise `SnapshotInvalid` on non-conformance (or on an
    unrunnable validator) — the generator's fail-loud path (SC-002).

    An UNAVAILABLE validator still raises here, deliberately, and that is not an
    oversight left over from the three-outcome split. This is the path a caller
    chooses when it wants a guarantee rather than a report, and "I could not
    check" is not the guarantee it asked for. The warn-and-continue judgement
    belongs to the CLI, which knows a human is standing there and that a
    dashboard he cannot start helps him less than an unchecked one he can."""
    result = validate_snapshot(path, validator=validator, strict=strict,
                               search_from=search_from)
    if not result.ok:
        raise SnapshotInvalid(
            f"{path}: {result.summary()}\n{result.stdout}{result.stderr}".rstrip())
    return result
