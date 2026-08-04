"""Canonical snapshot serialization is byte-identical and diffable, writes go
through the boundary, and validation is delegated to the pinned openxFactory
validator (FR-002 / SC-001 / SC-002). Generator-output determinism over the
fixture tree is a wave-2 concern (test_snapshot_determinism.py, T008); here we
pin the serialization/validation substrate itself."""

from __future__ import annotations

import pytest

from conftest import find_openxfactory_validator  # noqa: F401

from ideation_dashboard import snapshot
from ideation_dashboard.boundary import BoundaryViolation, OutputBoundary


def _minimal_snapshot(**over) -> dict:
    base = {
        "schema_version": 1,
        "kind": "ideation-dashboard-snapshot",
        "repository": "fixture-repo",
        "generation": {"source_revision": "0" * 40},
        "documents": [],
        "clusters": [],
        "possibles": [],
        "staged_topics": [],
        "changes": [],
        "keyword_index": [],
    }
    base.update(over)
    return base


# ---- canonical, byte-identical serialization ----

def test_canonical_json_is_key_order_independent():
    a = {"kind": "x", "schema_version": 1, "repository": "r", "nested": {"b": 2, "a": 1}}
    b = {"repository": "r", "nested": {"a": 1, "b": 2}, "schema_version": 1, "kind": "x"}
    assert snapshot.canonical_json(a) == snapshot.canonical_json(b)


def test_canonical_json_is_stable_across_repeated_renders():
    snap = _minimal_snapshot(documents=[{"id": "doc-a", "path": "p", "stage": "staged"}])
    assert snapshot.canonical_bytes(snap) == snapshot.canonical_bytes(snap)


def test_canonical_json_has_trailing_newline_and_sorted_keys():
    out = snapshot.canonical_json({"b": 1, "a": 2})
    assert out.endswith("\n")
    assert out.index('"a"') < out.index('"b"')  # sorted


def test_load_round_trips(tmp_path):
    snap = _minimal_snapshot(repository="round-trip")
    p = tmp_path / "out" / "snapshot.json"
    b = OutputBoundary(tmp_path, ["out/"])
    written = snapshot.write_snapshot(snap, p, b)
    assert snapshot.load_snapshot(written) == snap


# ---- writes go through the boundary ----

def test_write_snapshot_refused_outside_allowlist(tmp_path):
    b = OutputBoundary(tmp_path, ["out/"])
    with pytest.raises(BoundaryViolation):
        snapshot.write_snapshot(_minimal_snapshot(), "ideation/x.json", b)


# ---- validation delegated to the pinned validator ----

def test_find_validator_locates_pinned_checkout():
    # From the repo root the sibling openxFactory checkout is reachable.
    assert snapshot.find_validator(__import__("conftest").REPO_ROOT) is not None


def test_minimal_snapshot_validates_against_pinned_validator(tmp_path):
    validator = find_openxfactory_validator()
    if validator is None:
        pytest.skip("no reachable openxFactory checkout")
    b = OutputBoundary(tmp_path, ["out/"])
    p = snapshot.write_snapshot(_minimal_snapshot(), tmp_path / "out" / "s.json", b)
    result = snapshot.validate_snapshot(p, validator=validator)
    assert result.ok, result.summary() + "\n" + result.stdout + result.stderr


def test_referentially_broken_snapshot_is_rejected(tmp_path):
    validator = find_openxfactory_validator()
    if validator is None:
        pytest.skip("no reachable openxFactory checkout")
    # A cluster edge to a document id that does not exist -> dangling edge error.
    snap = _minimal_snapshot(
        clusters=[{"id": "cl-x", "name": "X", "topics": ["x"],
                   "document_edges": [{"document": "doc-missing", "matched_topics": ["x"]}]}],
    )
    b = OutputBoundary(tmp_path, ["out/"])
    p = snapshot.write_snapshot(snap, tmp_path / "out" / "bad.json", b)
    with pytest.raises(snapshot.SnapshotInvalid, match="dangling|unknown document"):
        snapshot.validate_or_raise(p, validator=validator)


# ---- three outcomes: validated / not conformant / validator unavailable ----
#
# `ok = (returncode == 0)` answered "is this snapshot good?" with "did the check
# succeed?", and those diverge precisely when the tooling is broken. The
# classifier reads the validator's DOCUMENTED exit-code contract (0 ok, 1
# findings, 2 harness error) rather than its prose, so these tests pin the codes.

def _stub(tmp_path, body: str, name: str = "stub.py"):
    p = tmp_path / name
    p.write_text(body, encoding="utf-8")
    return p


def _written(tmp_path):
    b = OutputBoundary(tmp_path, ["out/"])
    return snapshot.write_snapshot(_minimal_snapshot(), tmp_path / "out" / "s.json", b)


def test_exit_zero_is_validated(tmp_path):
    v = _stub(tmp_path, "print('0 error(s), 0 warning(s)')\n")
    result = snapshot.validate_snapshot(_written(tmp_path), validator=v)
    assert result.outcome == snapshot.VALIDATED
    assert result.ok and result.available


def test_the_findings_exit_code_is_a_verdict_on_the_data(tmp_path):
    v = _stub(tmp_path, "import sys\nprint('1 error(s)')\nsys.exit(1)\n")
    result = snapshot.validate_snapshot(_written(tmp_path), validator=v)
    assert result.outcome == snapshot.NOT_CONFORMANT
    assert not result.ok
    # the validator DID reach a verdict — the data is what failed
    assert result.available


def test_the_harness_exit_code_means_no_verdict_was_reached(tmp_path):
    v = _stub(tmp_path, "import sys\nprint('ERROR deps', file=sys.stderr)\nsys.exit(2)\n")
    result = snapshot.validate_snapshot(_written(tmp_path), validator=v)
    assert result.outcome == snapshot.VALIDATOR_UNAVAILABLE
    assert not result.available
    assert not result.ok           # `ok` still means VALIDATED, and nothing was
    assert "harness" in result.unavailable_reason


def test_a_missing_validator_is_unavailable_not_a_verdict(tmp_path):
    result = snapshot.validate_snapshot(_written(tmp_path),
                                        search_from=tmp_path / "out")
    assert result.outcome == snapshot.VALIDATOR_UNAVAILABLE
    assert result.validator is None


def test_a_validator_path_that_is_not_a_file_is_unavailable(tmp_path):
    """Not found is not the only way to have nothing to run — and this one is
    checked before launching precisely BECAUSE the exit code cannot express it:
    `python3 <a directory>` exits 1, which is the validator's findings code, so
    the snapshot would have been blamed for a bad tooling path."""
    d = tmp_path / "not-a-script"
    d.mkdir()
    result = snapshot.validate_snapshot(_written(tmp_path), validator=d)
    assert result.outcome == snapshot.VALIDATOR_UNAVAILABLE
    assert result.validator == d


def test_a_validator_that_will_not_launch_at_all_is_unavailable(tmp_path,
                                                                monkeypatch):
    """The exec-time failures no pre-check can anticipate — a dead interpreter,
    EACCES, ENOMEM. `subprocess.run` raises instead of returning a code, and an
    unhandled OSError here would surface as a crash rather than a diagnosis."""
    v = _stub(tmp_path, "import sys\nsys.exit(0)\n")

    def boom(*_a, **_k):
        raise OSError(12, "Cannot allocate memory")

    monkeypatch.setattr(snapshot.subprocess, "run", boom)
    result = snapshot.validate_snapshot(_written(tmp_path), validator=v)
    assert result.outcome == snapshot.VALIDATOR_UNAVAILABLE
    assert "could not be launched" in result.unavailable_reason


def test_an_unparseable_snapshot_is_the_data_even_on_a_harness_exit(tmp_path):
    """The one attribution the exit code cannot make. The validator ALSO exits 2
    when the file it was handed will not parse — and that is the snapshot's
    fault, not the environment's. Left unguarded, this fix would have converted
    a corrupt or truncated snapshot from a hard stop into a warning, which is
    the very trade it exists to refuse."""
    corrupt = tmp_path / "corrupt.json"
    corrupt.write_text('{"kind": "ideation-dashboard-snap', encoding="utf-8")
    v = _stub(tmp_path, "import sys\nprint('ERROR unparseable', file=sys.stderr)\n"
                        "sys.exit(2)\n")
    result = snapshot.validate_snapshot(corrupt, validator=v)
    assert result.outcome == snapshot.NOT_CONFORMANT
    assert not result.ok


def test_validate_or_raise_still_raises_when_the_validator_cannot_run(tmp_path):
    """The generator's fail-loud path is NOT relaxed. It exists so code that
    wants a guarantee gets an exception instead of a report, and "I could not
    check" is not the guarantee it asked for. The warn-and-continue judgement is
    the CLI's alone, because only the CLI knows a human is waiting."""
    v = _stub(tmp_path, "import sys\nsys.exit(2)\n")
    with pytest.raises(snapshot.SnapshotInvalid):
        snapshot.validate_or_raise(_written(tmp_path), validator=v)


def test_result_defaults_keep_the_old_two_outcome_reading(tmp_path):
    """`outcome` is additive: a five-argument construction — every one that
    predates this split — still means what it always did."""
    assert snapshot.ValidationResult(True, 0, "", "", None).outcome == snapshot.VALIDATED
    legacy = snapshot.ValidationResult(False, 1, "", "", None)
    assert legacy.outcome == snapshot.NOT_CONFORMANT and legacy.available
