"""T010: the canonical validator's CLI, per contracts/validator-cli.md.

Exit codes: 0 is no ERROR and no routed record; 1 is findings; 2 is a harness or
dependency failure; 3 is `check` only, at least one record ROUTED to the legacy
verifier and nothing an ERROR. Exit 3 is never a pass. The self-test never
exits 3: a route vector whose route matches its `expected` is a correct
adjudication, and the self-test exits 0.

Most cases run the validator as CI does, as a separate process. The cases that
need a broken tree call `main(argv, root=...)` in process on a copy of the
family, so the real tree is never edited and the CLI keeps no hidden `--root`
flag.
"""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

import pytest
import yaml

from .conftest import (
    FAMILY_REL,
    INDEX,
    LEGACY,
    PROTOCOL_REGISTRY,
    REPLACEMENT,
    load_validator,
    run_validator,
)

LINE = re.compile(
    r"^(ERROR \[council-convening-[a-z0-9-]+\] \S.*"
    r"|WARN  \[council-convening-[a-z0-9-]+\] \S.*"
    r"|note  \S.*)$")

PHASE_1_NOTES = [
    r"^note  schemas loaded: 2 \(family\) \+ digest-construction$",
    r"^note  protocol registry closed: 2 entries$",
    r"^note  corpus index: ([0-9]+) vectors, ([0-9]+) both-sides, sha256:[0-9a-f]{64}$",
    r"^note  vectors adjudicated: ([0-9]+)/\1$",
    r"^note  refusal codes probed: 5/5$",
    r"^note  finding codes probed: 1/1$",
    r"^note  requirements probed: 2/2 \(FR-001, FR-011\)$",
    r"^note  generator reproduced corpus byte-for-byte$",
]

SHA = "0123456789abcdef0123456789abcdef01234567"
FPR = "sha256:" + "ab" * 32


@pytest.fixture(scope="module")
def self_test():
    return run_validator()


def _write(tmp_path: Path, name: str, document) -> Path:
    path = tmp_path / name
    if name.endswith(".json"):
        path.write_text(json.dumps(document) + "\n", encoding="utf-8")
    else:
        path.write_text(yaml.safe_dump(document, sort_keys=False), encoding="utf-8")
    return path


# --------------------------------------------------------------------------
# The self-test.
# --------------------------------------------------------------------------

def test_the_self_test_exits_0(self_test):
    assert self_test.returncode == 0, self_test.stdout + self_test.stderr


@pytest.mark.parametrize("pattern", PHASE_1_NOTES)
def test_the_self_test_prints_every_phase_1_proof_of_work_note(self_test, pattern):
    assert re.search(pattern, self_test.stdout, re.M), (
        f"missing note {pattern!r} in:\n{self_test.stdout}")


def test_the_corpus_note_names_the_real_index(self_test):
    index = json.loads(INDEX.read_text(encoding="utf-8"))
    digest = hashlib.sha256(INDEX.read_bytes()).hexdigest()
    expected = (f"note  corpus index: {len(index['cases'])} vectors, "
                f"{index['totals']['both_sides']} both-sides, sha256:{digest}")
    assert expected in self_test.stdout.splitlines()


def test_route_vectors_are_adjudicated_and_the_self_test_still_exits_0(self_test):
    index = json.loads(INDEX.read_text(encoding="utf-8"))
    assert any(row["expected"]["outcome"] == "route" for row in index["cases"])
    assert self_test.returncode == 0


def test_every_output_line_is_a_finding_or_a_note(self_test):
    for line in self_test.stdout.splitlines():
        assert LINE.match(line), f"malformed output line: {line!r}"


def test_a_self_test_over_a_broken_corpus_exits_1(family_tree, capsys):
    from scripts.council_convening import corpus, generate

    root = family_tree
    conformance = root / FAMILY_REL / "conformance"
    index = json.loads((conformance / "index.json").read_text(encoding="utf-8"))
    row = next(r for r in index["cases"] if r["expected"]["outcome"] == "route")
    vector_path = conformance / row["path"]
    vector = json.loads(vector_path.read_text(encoding="utf-8"))
    vector["expected"] = {"outcome": "accept", "refusal": None, "findings": [],
                          "derived": {"classification": "legacy"},
                          "derived_origin": "hand"}
    vector_path.write_bytes(corpus.dump_json(vector))
    generate.generate(root)
    assert load_validator().main([], root=root) == 1
    out = capsys.readouterr().out
    assert "ERROR [council-convening-vector-outcome-mismatch]" in out


def test_a_self_test_whose_schema_does_not_load_exits_2(family_tree, capsys):
    (family_tree / FAMILY_REL / "shared-definitions.schema.yaml").write_text(
        "schema_version: [unclosed\n", encoding="utf-8")
    assert load_validator().main([], root=family_tree) == 2
    out = capsys.readouterr()
    assert "ERROR [" not in out.out, "a harness failure is never reported as a finding"


def test_a_self_test_without_the_digest_construction_exits_2(family_tree, capsys):
    (family_tree / "contracts" / "signed-execution-chain"
     / "digest-construction.schema.yaml").unlink()
    assert load_validator().main([], root=family_tree) == 2


def test_strict_is_accepted_and_changes_nothing_at_phase_1():
    result = run_validator("--strict")
    assert result.returncode == 0, result.stdout + result.stderr


# --------------------------------------------------------------------------
# `check`: classification first, then the kind.
# --------------------------------------------------------------------------

def test_check_routes_a_legacy_record_with_exit_3(tmp_path):
    path = _write(tmp_path, "legacy.json",
                  {"protocol": LEGACY, "key_fingerprint": FPR, "signature": "sig"})
    result = run_validator("check", str(path))
    assert result.returncode == 3, result.stdout + result.stderr
    assert "council-convening-legacy-protocol-routed" in result.stdout
    assert "ERROR [" not in result.stdout


def test_check_routes_a_roster_less_envelope_in_yaml(tmp_path):
    path = _write(tmp_path, "envelope.yaml", {"council_convening": {
        "council_id": "merge-readiness", "subject_pin": SHA,
        "packet_refs": ["opensoft/openxFactory#1268"]}})
    result = run_validator("check", str(path))
    assert result.returncode == 3, result.stdout + result.stderr


def test_check_refuses_a_replacement_record_of_a_kind_not_landed(tmp_path):
    path = _write(tmp_path, "convening.json", {
        "schema_version": 1, "kind": "xfactory_council_convening",
        "protocol": REPLACEMENT, "council_id": "merge-readiness"})
    result = run_validator("check", str(path))
    assert result.returncode == 1, result.stdout + result.stderr
    assert "ERROR [council-convening-kind-unknown]" in result.stdout


def test_check_refuses_a_kind_less_replacement_record(tmp_path):
    path = _write(tmp_path, "bare.json", {"protocol": REPLACEMENT})
    result = run_validator("check", str(path))
    assert result.returncode == 1
    assert "ERROR [council-convening-kind-unknown]" in result.stdout


def test_check_refuses_an_unknown_protocol(tmp_path):
    path = _write(tmp_path, "unknown.json", {"protocol": "xfc-resolved-council-2"})
    result = run_validator("check", str(path))
    assert result.returncode == 1
    assert "ERROR [council-convening-protocol-unknown]" in result.stdout


def test_check_judges_the_registry_by_kind_and_never_classifies_it():
    """N7: the registry carries no `protocol` member and matches no recognition
    rule, so classifying it would refuse it as `protocol_unknown`."""
    result = run_validator("check", str(PROTOCOL_REGISTRY))
    assert result.returncode == 0, result.stdout + result.stderr
    assert "protocol-unknown" not in result.stdout
    assert "ERROR [" not in result.stdout


def test_check_refuses_a_registry_that_gained_an_entry(tmp_path):
    doc = yaml.safe_load(PROTOCOL_REGISTRY.read_text(encoding="utf-8"))
    extra = dict(doc["protocols"][0], protocol_id="xfc-resolved-council-2")
    doc["protocols"].append(extra)
    path = _write(tmp_path, "registry.yaml", doc)
    result = run_validator("check", str(path))
    assert result.returncode == 1
    assert "ERROR [council-convening-registry-closure]" in result.stdout


def test_check_refuses_a_judged_by_kind_record_whose_schema_has_not_landed(tmp_path):
    path = _write(tmp_path, "binding.json", {
        "schema_version": 1, "kind": "xfactory_council_producer_binding",
        "binding_id": "commission"})
    result = run_validator("check", str(path))
    assert result.returncode == 1
    assert "ERROR [council-convening-kind-unknown]" in result.stdout
    assert "protocol-unknown" not in result.stdout


def test_check_with_a_route_and_an_error_exits_1(tmp_path):
    legacy = _write(tmp_path, "legacy.json", {"protocol": LEGACY})
    unknown = _write(tmp_path, "unknown.json", {"protocol": "nope"})
    result = run_validator("check", str(legacy), str(unknown))
    assert result.returncode == 1
    assert "council-convening-legacy-protocol-routed" in result.stdout
    assert "ERROR [council-convening-protocol-unknown]" in result.stdout


def test_check_on_an_unparseable_record_is_a_schema_finding(tmp_path):
    path = tmp_path / "broken.json"
    path.write_text("{not json\n", encoding="utf-8")
    result = run_validator("check", str(path))
    assert result.returncode == 1
    assert "ERROR [council-convening-schema]" in result.stdout


def test_check_on_an_unreadable_path_exits_2(tmp_path):
    result = run_validator("check", str(tmp_path / "absent.json"))
    assert result.returncode == 2
    assert "ERROR [" not in result.stdout


def test_check_says_exit_0_covers_the_offline_rules_only():
    result = run_validator("check", str(PROTOCOL_REGISTRY))
    assert "offline-checkable rules only" in result.stdout


def test_check_never_echoes_a_record_value(tmp_path):
    value = "xfc-" + "Q" * 60 + "-distinctive"
    path = _write(tmp_path, "echo.json", {"protocol": value})
    result = run_validator("check", str(path))
    assert result.returncode == 1
    assert value not in result.stdout + result.stderr


# --------------------------------------------------------------------------
# `corpus`.
# --------------------------------------------------------------------------

def test_corpus_json_shape():
    result = run_validator("corpus", "--json")
    assert result.returncode == 0, result.stdout + result.stderr
    summary = json.loads(result.stdout)
    index = json.loads(INDEX.read_text(encoding="utf-8"))
    assert set(summary) == {"corpus_id", "protocol", "index_sha256", "vectors",
                            "agreement_set", "totals", "coverage_floor"}
    assert summary["corpus_id"] == "council-convening-conformance"
    assert summary["protocol"] == REPLACEMENT
    assert summary["index_sha256"] == "sha256:" + hashlib.sha256(INDEX.read_bytes()).hexdigest()
    assert summary["vectors"] == len(index["cases"])
    assert summary["agreement_set"] == index["totals"]["both_sides"]
    assert summary["totals"] == index["totals"]
    assert summary["coverage_floor"] == index["coverage_floor"]


def test_corpus_plain_prints_notes():
    result = run_validator("corpus")
    assert result.returncode == 0
    lines = result.stdout.splitlines()
    assert lines and all(LINE.match(line) for line in lines)
    assert any("agreement set" in line for line in lines)


# --------------------------------------------------------------------------
# Subcommands that land later are argparse's exit 2 now.
# --------------------------------------------------------------------------

@pytest.mark.parametrize("argv", [
    ["select", "--producer", "p.json", "--consumer", "c.json"],
    ["check", "--historical", "x.json"],
    ["no-such-mode"],
])
def test_modes_that_have_not_landed_are_exit_2(argv):
    assert run_validator(*argv).returncode == 2


# --------------------------------------------------------------------------
# `check` on a snapshot and an assignment (T037, Phase 3).
# --------------------------------------------------------------------------

def _snapshot_file(tmp_path: Path, mutate=None) -> Path:
    from .assignment_fixtures import snapshot

    document = snapshot()
    if mutate is not None:
        mutate(document)
    return _write(tmp_path, "snapshot.json", document)


def test_check_on_a_snapshot_recomputes_its_digest_and_its_assignment_set(tmp_path):
    result = run_validator("check", str(_snapshot_file(tmp_path)))
    assert result.returncode == 0, result.stdout + result.stderr
    assert "ERROR [" not in result.stdout
    assert re.search(
        r"^note  .*snapshot\.json: convening_digest recomputed; "
        r"assignment set matches required_seats \(2 seats\)$", result.stdout, re.M), (
        result.stdout)


def test_check_refuses_a_snapshot_whose_digest_does_not_recompute(tmp_path):
    def mutate(document):
        document["convening"]["packet_refs"] = ["packet/alpha-2"]

    result = run_validator("check", str(_snapshot_file(tmp_path, mutate)))
    assert result.returncode == 1, result.stdout + result.stderr
    assert "ERROR [council-convening-digest-construction-mismatch]" in result.stdout


def test_check_refuses_a_snapshot_whose_assignment_set_is_reordered(tmp_path):
    def mutate(document):
        document["assignments"].reverse()

    result = run_validator("check", str(_snapshot_file(tmp_path, mutate)))
    assert result.returncode == 1, result.stdout + result.stderr
    assert "ERROR [council-convening-assignment-set-mismatch]" in result.stdout


def test_check_refuses_a_snapshot_with_an_assignment_above_the_ceiling(tmp_path):
    def mutate(document):
        document["assignments"][0]["expires_at"] = "2026-10-09T06:00:01Z"

    result = run_validator("check", str(_snapshot_file(tmp_path, mutate)))
    assert result.returncode == 1, result.stdout + result.stderr
    assert "ERROR [council-convening-assignment-malformed]" in result.stdout


def test_check_on_a_lone_assignment_checks_its_shape_and_says_what_needs_its_snapshot(
        tmp_path):
    from .assignment_fixtures import assignment, convening_record

    path = _write(tmp_path, "assignment.json",
                  assignment(convening_record(), "convening-0001", "seat-a"))
    result = run_validator("check", str(path))
    assert result.returncode == 0, result.stdout + result.stderr
    assert "note  not checkable offline: " in result.stdout
    assert "assignment set" in result.stdout


def test_check_on_a_commission_record_reports_retry_identity_as_not_offline_checkable(
        tmp_path):
    from .assignment_fixtures import convening_record

    path = _write(tmp_path, "convening.json", convening_record())
    result = run_validator("check", str(path))
    assert re.search(r"^note  not checkable offline: .*retry identity and once-per-pin",
                     result.stdout, re.M), result.stdout
