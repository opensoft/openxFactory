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

import copy
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

#: The Phase 1 notes, at the counts landed by Phase 6: six family schemas (Phase
#: 2's predicate registry and commission record, and Phase 6's protocol selection
#: and activation evidence), 43 refusal codes, both findings and the
#: seven-requirement floor (T026, T028, T029; T058, T060).
PHASE_1_NOTES = [
    r"^note  schemas loaded: 6 \(family\) \+ digest-construction$",
    r"^note  protocol registry closed: 2 entries$",
    r"^note  corpus index: ([0-9]+) vectors, ([0-9]+) both-sides, sha256:[0-9a-f]{64}$",
    r"^note  vectors adjudicated: ([0-9]+)/\1$",
    r"^note  refusal codes probed: 43/43$",
    r"^note  finding codes probed: 2/2$",
    r"^note  requirements probed: 7/7 \(FR-001, FR-002, FR-003, FR-004, FR-011, FR-012, SC-001\)$",
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


def test_check_routes_the_real_legacy_seat_result_with_exit_3(tmp_path):
    """The legacy seat result as codexFactory signs it and Hermes reads it: no
    `protocol` member, the context string at `signature.protocol`."""
    path = _write(tmp_path, "seat-result.json", {
        "seat": "security", "result": "approve", "rationale": "no finding",
        "undispositioned_conditions": 0,
        "signature": {"protocol": LEGACY, "key_fingerprint": FPR,
                      "signature": "A" * 85 + "Q"}})
    result = run_validator("check", str(path))
    assert result.returncode == 3, result.stdout + result.stderr
    assert "council-convening-legacy-protocol-routed" in result.stdout


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
    extra = dict(json.loads(json.dumps(doc["protocols"][0])),
                 protocol_id="xfc-resolved-council-2")  # a deep copy: no YAML alias
    doc["protocols"].append(extra)
    path = _write(tmp_path, "registry.yaml", doc)
    result = run_validator("check", str(path))
    assert result.returncode == 1
    assert "ERROR [council-convening-registry-closure]" in result.stdout


def test_check_refuses_a_registry_tag_with_a_trailing_newline(tmp_path):
    doc = yaml.safe_load(PROTOCOL_REGISTRY.read_text(encoding="utf-8"))
    doc["protocols"][1]["introduced_in"] = "contract-v4.0\n"
    path = _write(tmp_path, "registry.yaml", doc)
    result = run_validator("check", str(path))
    assert result.returncode == 1, result.stdout + result.stderr
    assert "ERROR [council-convening-schema]" in result.stdout
    assert "protocols/1/introduced_in" in result.stdout


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
# An unknown subcommand is argparse's exit 2. Every mode has landed by Phase 6.
# --------------------------------------------------------------------------

@pytest.mark.parametrize("argv", [
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
    # A deep copy: a shared sub-object would be dumped as a YAML alias, which the
    # strict loader refuses before closure is ever judged (M2).
    doc["predicates"].append(dict(copy.deepcopy(doc["predicates"][0]), predicate="paths_touch_any"))
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


# --------------------------------------------------------------------------
# B2: the non-record family kinds are judged, never waved through.
# --------------------------------------------------------------------------

INDEX_KIND = "openxfactory-council-convening-conformance-index"
VECTOR_KIND = "openxfactory-council-convening-conformance-vector"
SCHEMA_KIND = "openxfactory-council-convening-contract-schema"
DIALECT = "https://json-schema.org/draft/2020-12/schema"
ID_BASE = "https://xforge.us/schemas/openxfactory/council-convening/v1/"


@pytest.mark.parametrize("document", [
    {"protocol": LEGACY, "kind": INDEX_KIND, "seat": "security",
     "signature": {"protocol": LEGACY, "key_fingerprint": FPR, "signature": "A" * 85 + "Q"}},
    {"kind": INDEX_KIND, "protocol": "nope"},
])
def test_check_judges_a_document_labelled_as_a_corpus_index(tmp_path, document):
    path = _write(tmp_path, "index.json", document)
    result = run_validator("check", str(path))
    assert result.returncode == 1, result.stdout + result.stderr
    assert "ERROR [council-convening-index-closure]" in result.stdout


def test_check_accepts_the_landed_index_structure_and_says_what_it_did_not_check():
    result = run_validator("check", str(INDEX))
    assert result.returncode == 0, result.stdout + result.stderr
    assert "closure against its tree is the self-test's" in result.stdout


def _route_vector() -> dict:
    index = json.loads(INDEX.read_text(encoding="utf-8"))
    row = next(r for r in index["cases"] if r["expected"]["outcome"] == "route")
    return json.loads((INDEX.parent / row["path"]).read_text(encoding="utf-8"))


def test_check_adjudicates_a_vector(tmp_path):
    path = _write(tmp_path, "vector.json", _route_vector())
    result = run_validator("check", str(path))
    assert result.returncode == 0, result.stdout + result.stderr
    assert "vector adjudicated to its expected outcome" in result.stdout
    assert "the self-test adjudicates it" not in result.stdout


def test_check_refuses_a_vector_whose_expectation_the_reference_contradicts(tmp_path):
    vector = _route_vector()
    vector["expected"] = {"outcome": "accept", "refusal": None, "findings": [],
                          "derived": {"classification": "legacy"}, "derived_origin": "hand"}
    path = _write(tmp_path, "vector.json", vector)
    result = run_validator("check", str(path))
    assert result.returncode == 1, result.stdout + result.stderr
    assert "ERROR [council-convening-vector-outcome-mismatch]" in result.stdout


def _schema_doc(**changes) -> dict:
    document = {"schema_version": 1, "kind": SCHEMA_KIND, "name": "xfactory_probe",
                "$schema": DIALECT, "$id": ID_BASE + "probe.schema.yaml", "type": "object"}
    document.update(changes)
    return {key: value for key, value in document.items() if value is not None}


def test_check_accepts_a_family_schema_with_the_house_header(tmp_path):
    result = run_validator("check", str(_write(tmp_path, "probe.yaml", _schema_doc())))
    assert result.returncode == 0, result.stdout + result.stderr


@pytest.mark.parametrize("changes", [
    {"$id": None},
    {"$id": "https://example.invalid/probe.schema.yaml"},
    {"$id": ID_BASE + "probe.json"},
    {"$schema": None},
    {"$schema": "http://json-schema.org/draft-07/schema#"},
    {"schema_version": 2},
    {"protocol": LEGACY},
    {"signature": {"protocol": LEGACY}},
])
def test_check_refuses_a_schema_kind_document_without_the_house_header(tmp_path, changes):
    path = _write(tmp_path, "probe.yaml", _schema_doc(**changes))
    result = run_validator("check", str(path))
    assert result.returncode == 1, result.stdout + result.stderr
    assert "ERROR [council-convening-schema]" in result.stdout


# --------------------------------------------------------------------------
# L4: a `kind` that is not a string is malformed, never a crash.
# --------------------------------------------------------------------------

@pytest.mark.parametrize("kind", [["xfactory_council_seat_return"], {"a": 1}, 7])
def test_check_refuses_a_kind_that_is_not_a_string(tmp_path, kind):
    path = _write(tmp_path, "record.json", {"kind": kind, "protocol": LEGACY})
    result = run_validator("check", str(path))
    assert result.returncode == 1, result.stdout + result.stderr
    assert "Traceback" not in result.stderr
    assert "ERROR [council-convening-schema]" in result.stdout


# --------------------------------------------------------------------------
# L9: nothing is classified against a registry that is not closed.
# --------------------------------------------------------------------------

def _unclose_the_registry(root: Path) -> None:
    path = root / FAMILY_REL / "protocol.registry.yaml"
    doc = yaml.safe_load(path.read_text(encoding="utf-8"))
    for rule in doc["protocols"][1]["recognition"]:
        if rule["rule"] == "legacy_signing_context":
            rule["member_paths"] = [["somewhere", "else"]]
    path.write_text(yaml.safe_dump(doc, sort_keys=False), encoding="utf-8")


def test_check_refuses_to_classify_against_an_unclosed_registry(family_tree, tmp_path, capsys):
    _unclose_the_registry(family_tree)
    record = _write(tmp_path, "record.json", {"protocol": LEGACY})
    assert load_validator().main(["check", str(record)], root=family_tree) == 1
    out = capsys.readouterr().out
    assert "ERROR [council-convening-registry-closure]" in out
    assert "legacy-protocol-routed" not in out


def test_corpus_refuses_to_summarize_against_an_unclosed_registry(family_tree, capsys):
    _unclose_the_registry(family_tree)
    assert load_validator().main(["corpus"], root=family_tree) == 1
    assert "ERROR [council-convening-registry-closure]" in capsys.readouterr().out


def test_the_generator_refuses_an_unclosed_registry(family_tree):
    from scripts.council_convening import generate

    _unclose_the_registry(family_tree)
    with pytest.raises(ValueError, match="registry"):
        generate.render(family_tree)
    assert any("registry" in line for line in generate.check(family_tree))


# --------------------------------------------------------------------------
# M1: one malformed vector is a finding, and the findings are printed first.
# --------------------------------------------------------------------------

def test_a_vector_that_breaks_the_format_is_a_finding_not_a_traceback(family_tree, capsys):
    """An INDEXED vector missing `requirement_ids` (its row digest moved, as a
    hand edit would leave it) once crashed the generator's `build_index` with a
    `KeyError`, after the self-test had collected its findings and before it
    printed any."""
    from scripts.council_convening import corpus, generate

    conformance = family_tree / FAMILY_REL / "conformance"
    index = json.loads((conformance / "index.json").read_text(encoding="utf-8"))
    row = next(r for r in index["cases"] if r["expected"]["outcome"] == "route")
    target = conformance / row["path"]
    vector = json.loads(target.read_text(encoding="utf-8"))
    del vector["requirement_ids"]
    target.write_bytes(corpus.dump_json(vector))
    row["sha256"] = corpus.raw_sha256(target.read_bytes())
    (conformance / "index.json").write_bytes(corpus.dump_json(index))
    with pytest.raises(ValueError, match="requirement_ids"):
        generate.render(family_tree)
    assert load_validator().main([], root=family_tree) == 1
    lines = capsys.readouterr().out.splitlines()
    schema = next(i for i, line in enumerate(lines)
                  if line.startswith("ERROR [council-convening-schema]")
                  and row["case_id"] in line and "requirement_ids" in line)
    drift = next(i for i, line in enumerate(lines)
                 if line.startswith("ERROR [council-convening-generator-drift]"))
    assert schema < drift, "the collected findings print before the generator check"


# --------------------------------------------------------------------------
# M2: a repeated YAML key is refused, never resolved.
# --------------------------------------------------------------------------

def test_check_refuses_a_yaml_record_with_a_repeated_key(tmp_path):
    path = tmp_path / "record.yaml"
    path.write_text(f"protocol: {LEGACY}\nprotocol: {REPLACEMENT}\nkind: xfactory_council_convening\n",
                    encoding="utf-8")
    result = run_validator("check", str(path))
    assert result.returncode == 1, result.stdout + result.stderr
    assert "ERROR [council-convening-schema]" in result.stdout
    assert "strict YAML" in result.stdout


# --------------------------------------------------------------------------
# Phase 6 (T059): `select`, `check --historical`, E11/E12 records, full coverage.
# --------------------------------------------------------------------------

INDEX_SHA = "sha256:" + "cd" * 32
BUNDLE = "contract-v5.0"


def _selection(side, mode="rehearsal", protocol=REPLACEMENT, bundle=None, commit=SHA,
               index=INDEX_SHA):
    return {"schema_version": 1, "kind": "xfactory_council_protocol_selection",
            "side": side, "mode": mode, "protocol": protocol, "provider_commit": commit,
            "provider_bundle": bundle, "corpus_index_sha256": index}


def _select(tmp_path, producer, consumer):
    p = _write(tmp_path, "producer.json", producer)
    c = _write(tmp_path, "consumer.json", consumer)
    return run_validator("select", "--producer", str(p), "--consumer", str(c))


def test_select_accepts_a_matched_rehearsal_pair(tmp_path):
    result = _select(tmp_path, _selection("producer"), _selection("consumer"))
    assert result.returncode == 0, result.stdout + result.stderr
    assert "note  select: pair matched on mode, protocol, provider_commit, " \
           "provider_bundle, corpus_index_sha256" in result.stdout
    assert "ERROR [" not in result.stdout


def test_select_reads_yaml_selections_too(tmp_path):
    p = _write(tmp_path, "producer.yaml", _selection("producer", bundle=BUNDLE))
    c = _write(tmp_path, "consumer.yaml", _selection("consumer", bundle=BUNDLE))
    result = run_validator("select", "--producer", str(p), "--consumer", str(c))
    assert result.returncode == 0, result.stdout + result.stderr


@pytest.mark.parametrize("member, value", [
    ("mode", "active"), ("protocol", LEGACY), ("provider_commit", "f" * 40),
    ("provider_bundle", "contract-v4.2"), ("corpus_index_sha256", "sha256:" + "ef" * 32)])
def test_select_refuses_a_pair_that_differs_on_any_matched_value(tmp_path, member, value):
    consumer = _selection("consumer", bundle=BUNDLE)
    consumer[member] = value
    result = _select(tmp_path, _selection("producer", bundle=BUNDLE), consumer)
    assert result.returncode == 1, result.stdout + result.stderr
    # An active replacement selection is refused for eligibility first at this
    # commit, where the replacement is `available`.
    code = ("replacement-not-admission-eligible" if member == "mode"
            else "pair-mismatched")
    assert f"ERROR [council-convening-{code}]" in result.stdout


def test_select_refuses_an_active_replacement_before_the_major(tmp_path):
    """The live registry holds the replacement `available` at this commit."""
    result = _select(tmp_path, _selection("producer", mode="active", bundle=BUNDLE),
                     _selection("consumer", mode="active", bundle=BUNDLE))
    assert result.returncode == 1
    assert "ERROR [council-convening-replacement-not-admission-eligible]" in result.stdout


def test_select_accepts_an_active_legacy_pair_while_in_use(tmp_path):
    result = _select(tmp_path,
                     _selection("producer", mode="active", protocol=LEGACY, bundle=BUNDLE),
                     _selection("consumer", mode="active", protocol=LEGACY, bundle=BUNDLE))
    assert result.returncode == 0, result.stdout + result.stderr


@pytest.mark.parametrize("producer, code", [
    (_selection("producer", mode="active"), "selection-malformed"),
    (_selection("consumer"), "selection-malformed"),
    (_selection("producer", protocol="xfc-resolved-council-2"), "protocol-unknown"),
])
def test_select_names_the_first_failing_check(tmp_path, producer, code):
    result = _select(tmp_path, producer, _selection("consumer"))
    assert result.returncode == 1
    assert f"ERROR [council-convening-{code}]" in result.stdout


def test_select_refuses_a_legacy_selection_once_historical_only(family_tree, tmp_path, capsys):
    path = family_tree / FAMILY_REL / "protocol.registry.yaml"
    doc = yaml.safe_load(path.read_text(encoding="utf-8"))
    doc["protocols"][1]["status"] = "historical_only"
    doc["protocols"][0]["status"] = "admission_eligible"
    path.write_text(yaml.safe_dump(doc, sort_keys=False), encoding="utf-8")
    p = _write(tmp_path, "p.json", _selection("producer", protocol=LEGACY, bundle=BUNDLE))
    c = _write(tmp_path, "c.json", _selection("consumer", protocol=LEGACY, bundle=BUNDLE))
    assert load_validator().main(["select", "--producer", str(p), "--consumer", str(c)],
                                 root=family_tree) == 1
    assert "ERROR [council-convening-legacy-protocol-refused]" in capsys.readouterr().out


def test_select_on_an_unreadable_file_exits_2(tmp_path):
    c = _write(tmp_path, "c.json", _selection("consumer"))
    result = run_validator("select", "--producer", str(tmp_path / "absent.json"),
                           "--consumer", str(c))
    assert result.returncode == 2
    assert "ERROR [" not in result.stdout


def test_select_needs_both_sides():
    assert run_validator("select", "--producer", "p.json").returncode == 2


def test_select_never_echoes_a_value(tmp_path):
    value = "xfc-" + "Q" * 60 + "-distinctive"
    result = _select(tmp_path, _selection("producer", protocol=value),
                     _selection("consumer", protocol=value))
    assert result.returncode == 1
    assert value not in result.stdout + result.stderr


# `check --historical`.

def test_check_historical_exits_3_on_a_legacy_record(tmp_path):
    path = _write(tmp_path, "legacy.json", {"protocol": LEGACY, "key_fingerprint": FPR})
    result = run_validator("check", "--historical", str(path))
    assert result.returncode == 3, result.stdout + result.stderr
    assert "council-convening-legacy-protocol-routed" in result.stdout


def test_check_historical_exits_0_on_a_valid_replacement_record(tmp_path):
    path = _write(tmp_path, "replacement.json", VALID_REPLACEMENT_RECORD)
    result = run_validator("check", "--historical", str(path))
    assert result.returncode == 0, result.stdout + result.stderr
    assert "ERROR [" not in result.stdout


def test_check_historical_still_refuses_a_malformed_replacement_record(tmp_path):
    broken = dict(VALID_REPLACEMENT_RECORD)
    broken["unexpected"] = "member"
    path = _write(tmp_path, "broken.json", broken)
    result = run_validator("check", "--historical", str(path))
    assert result.returncode == 1


# `check` on the two Phase 6 kinds, judged by kind and never classified.

def test_check_validates_a_selection_record(tmp_path):
    path = _write(tmp_path, "selection.json", _selection("producer"))
    result = run_validator("check", str(path))
    assert result.returncode == 0, result.stdout + result.stderr
    assert "protocol-unknown" not in result.stdout
    assert "not checkable offline" in result.stdout  # the pair needs `select`


def test_check_refuses_a_malformed_selection_record(tmp_path):
    path = _write(tmp_path, "selection.json", _selection("producer", mode="active"))
    result = run_validator("check", str(path))
    assert result.returncode == 1
    assert "ERROR [council-convening-selection-malformed]" in result.stdout


def test_check_validates_an_activation_record_offline_and_says_what_it_could_not(tmp_path):
    record = {"schema_version": 1, "kind": "xfactory_council_activation_evidence",
              "act": "pause", "recorded_at": "2026-10-09T00:00:00Z",
              "provider": {"commit": SHA, "bundle": BUNDLE, "corpus_index_sha256": INDEX_SHA},
              "owner_word": {"author": "Example Owner", "date": "2026-10-09T00:00:00Z",
                             "verbatim": "an example owner word", "cite": "example"}}
    path = _write(tmp_path, "pause.json", record)
    result = run_validator("check", str(path))
    assert result.returncode == 0, result.stdout + result.stderr


def test_check_reports_the_activation_rules_it_cannot_run_offline(tmp_path):
    record = json.loads(ACTIVATION_VECTOR.read_text(encoding="utf-8"))["inputs"]["record"]
    path = _write(tmp_path, "activation.json", record)
    result = run_validator("check", str(path))
    assert result.returncode == 0, result.stdout + result.stderr
    assert "not checkable offline" in result.stdout
    assert "rehearsal_ref" in result.stdout and "binding_refs" in result.stdout


def test_check_refuses_an_incomplete_activation_record(tmp_path):
    record = json.loads(ACTIVATION_VECTOR.read_text(encoding="utf-8"))["inputs"]["record"]
    del record["owner_word"]
    path = _write(tmp_path, "activation.json", record)
    result = run_validator("check", str(path))
    assert result.returncode == 1
    assert "ERROR [council-convening-activation-evidence-incomplete]" in result.stdout


#: A landed replacement record: Phase 2's commission record, from a positive
#: resolution vector.
VALID_REPLACEMENT_RECORD = _commission_record()
#: An activation record from the migration corpus, with its per-seat bindings.
ACTIVATION_VECTOR = (INDEX.parent / "vectors" / "migration"
                     / "mig-act-activation-per-seat-merge-readiness-accept.json")
