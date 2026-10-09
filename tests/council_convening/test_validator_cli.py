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

#: The Phase 1 notes, at the counts landed by Phase 2: four family schemas (the
#: predicate registry's and the commission record's join), 34 refusal codes and
#: the six-requirement floor (T026, T028, T029).
PHASE_1_NOTES = [
    r"^note  schemas loaded: 4 \(family\) \+ digest-construction$",
    r"^note  protocol registry closed: 2 entries$",
    r"^note  corpus index: ([0-9]+) vectors, ([0-9]+) both-sides, sha256:[0-9a-f]{64}$",
    r"^note  vectors adjudicated: ([0-9]+)/\1$",
    r"^note  refusal codes probed: 34/34$",
    r"^note  finding codes probed: 1/1$",
    r"^note  requirements probed: 6/6 \(FR-001, FR-002, FR-003, FR-004, FR-011, SC-001\)$",
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
    # The commission record lands in Phase 2, so the snapshot (Phase 3) is the
    # protocol-carrying kind whose schema has not landed at this commit.
    path = _write(tmp_path, "snapshot.json", {
        "schema_version": 1, "kind": "xfactory_council_convening_snapshot",
        "protocol": REPLACEMENT, "convening_id": "convening-1"})
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
# Phase 2 (T027): `check` runs the offline E2 rules on a commission record and
# names each oracle-dependent rule as not offline-checkable; the self-test
# prints the predicate-registry note.
# --------------------------------------------------------------------------

PREDICATE_NOTE = r"^note  predicate registry closed: 2 predicates, 2 input contracts$"
RESOLUTION = INDEX.parent / "vectors" / "resolution"
PREDICATE_REGISTRY = PROTOCOL_REGISTRY.parent / "predicate.registry.yaml"

#: Every E2 rule a classed commission record reaches that needs an environment
#: oracle, as `check` names it. None of them is ever reported as passed.
ORACLE_RULES = [
    "candidate_mismatch (expected candidate)",
    "candidate_mismatch (resolved candidate)",
    "candidate_mismatch (authoritative head ref)",
    "rule_unauthorized (governed repository)",
    "rule_revision_ungoverned",
    "governed_sources_mismatch",
    "rule_unavailable",
    "rule_unauthorized (governed source)",
    "rule_digest_mismatch",
    "rule_superseded",
    "council_unknown",
    "class_mismatch",
    "class_unresolved",
    "rule_projection_mismatch",
    "condition_unevaluable",
    "consumed_facts_mismatch",
    "condition_result_mismatch",
    "candidate_head_unavailable",
    "candidate_head_moved",
]


def _commission_record(case_id: str = "commission-accept-conditional-seat-held") -> dict:
    vector = json.loads((RESOLUTION / f"{case_id}.json").read_text(encoding="utf-8"))
    return vector["inputs"]["record"]


@pytest.fixture(scope="module")
def checked_commission_record(tmp_path_factory):
    path = _write(tmp_path_factory.mktemp("e2"), "convening.json", _commission_record())
    return run_validator("check", str(path))


def test_the_self_test_prints_the_predicate_registry_note(self_test):
    assert re.search(PREDICATE_NOTE, self_test.stdout, re.M), self_test.stdout


def test_check_passes_a_well_formed_commission_record_on_the_offline_rules(
        checked_commission_record):
    result = checked_commission_record
    assert result.returncode == 0, result.stdout + result.stderr
    assert "ERROR [" not in result.stdout
    assert "passes every offline-checkable E2 rule" in result.stdout
    assert "offline-checkable rules only" in result.stdout


@pytest.mark.parametrize("rule", ORACLE_RULES)
def test_check_names_each_oracle_dependent_rule_as_not_offline_checkable(
        checked_commission_record, rule):
    notes = [line for line in checked_commission_record.stdout.splitlines()
             if line.startswith("note  [council-convening-not-offline-checkable] ")]
    assert any(line.endswith(f": not checkable offline: {rule}") for line in notes), (
        checked_commission_record.stdout)


def test_check_names_no_offline_rule_as_not_checkable(checked_commission_record):
    """The offline-checkable rules run; they are never listed as skipped."""
    for rule in ("mutable_rule_reference", "rule_path_malformed", "predicate_unknown",
                 "fact_source_mismatch", "opaque_conclusion", "facts_unused",
                 "condition_seat_unbound", "roster_empty", "roster_mismatch",
                 "secret_bearing_fact", "convening_malformed"):
        assert f"not checkable offline: {rule}" not in checked_commission_record.stdout


@pytest.mark.parametrize("mutate, finding", [
    pytest.param(lambda r: r["required_seats"].reverse(),
                 "council-convening-roster-mismatch", id="roster-reordered"),
    pytest.param(lambda r: r.update(required_seats=[]),
                 "council-convening-roster-empty", id="roster-empty"),
    pytest.param(lambda r: r["required_seats_provenance"]["governed"].update(revision="main"),
                 "council-convening-mutable-rule-reference", id="mutable-revision"),
    pytest.param(lambda r: r["required_seats_provenance"]["conditions"][0].update(
        predicate="paths_touch_any"), "council-convening-predicate-unknown",
        id="unknown-predicate"),
    pytest.param(lambda r: r["required_seats_provenance"].update(fact_sources=[]),
                 "council-convening-fact-source-mismatch", id="no-fact-source"),
    pytest.param(lambda r: r.update(subject_pin="f" * 40),
                 "council-convening-candidate-mismatch", id="pin-not-head"),
    pytest.param(lambda r: r.update(notes="x"),
                 "council-convening-convening-malformed", id="unknown-member"),
])
def test_check_refuses_an_offline_checkable_defect(tmp_path, mutate, finding):
    record = _commission_record()
    mutate(record)
    path = _write(tmp_path, "convening.json", record)
    result = run_validator("check", str(path))
    assert result.returncode == 1, result.stdout + result.stderr
    assert f"ERROR [{finding}]" in result.stdout


def test_a_malformed_commission_record_also_names_the_schema_finding(tmp_path):
    record = _commission_record()
    record["notes"] = "x"
    result = run_validator("check", str(_write(tmp_path, "convening.json", record)))
    assert "ERROR [council-convening-schema]" in result.stdout


def test_check_refuses_a_secret_without_echoing_it(tmp_path):
    record = _commission_record()
    secret = "notes/gh" + "p_" + "A1b2C3d4E5f6G7h8I9j0K1l2"
    record["required_seats_provenance"]["consumed_facts"]["pr_facts"]["changed_paths"].append(
        secret)
    result = run_validator("check", str(_write(tmp_path, "convening.json", record)))
    assert result.returncode == 1
    assert "ERROR [council-convening-secret-bearing-fact]" in result.stdout
    assert secret not in result.stdout + result.stderr


def test_check_judges_the_predicate_registry_by_kind_and_never_classifies_it():
    result = run_validator("check", str(PREDICATE_REGISTRY))
    assert result.returncode == 0, result.stdout + result.stderr
    assert "protocol-unknown" not in result.stdout
    assert re.search(r"predicate registry closed: 2 predicates, 2 input contracts",
                     result.stdout)


def test_check_refuses_a_predicate_registry_that_gained_a_predicate(tmp_path):
    doc = yaml.safe_load(PREDICATE_REGISTRY.read_text(encoding="utf-8"))
    doc["predicates"].append(dict(doc["predicates"][0], predicate="paths_touch_any"))
    result = run_validator("check", str(_write(tmp_path, "predicates.yaml", doc)))
    assert result.returncode == 1
    assert "ERROR [council-convening-registry-closure]" in result.stdout


def test_a_self_test_over_a_widened_predicate_registry_exits_1(family_tree, capsys):
    path = family_tree / FAMILY_REL / "predicate.registry.yaml"
    doc = yaml.safe_load(path.read_text(encoding="utf-8"))
    doc["predicates"][0]["patterns"]["max_items"] = 512
    path.write_text(yaml.safe_dump(doc, sort_keys=False), encoding="utf-8")
    assert load_validator().main([], root=family_tree) == 1
    out = capsys.readouterr().out
    assert "ERROR [council-convening-registry-closure]" in out
    assert "predicate registry closed" not in out
