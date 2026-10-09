"""T008: the corpus index, the vector format and coverage at the commit.

The format is contracts/conformance-corpus.md. Every mutation here runs on a
COPY of the family (`family_tree`), so the real corpus is never edited. Where a
mutation would otherwise also break an unrelated rule (a row digest, say), the
test regenerates the index with the generator first, so that the finding under
test is the only one the mutation causes.

The generator's own Phase 1 obligations (T020) are pinned at the bottom: the
deterministic JSON form, `--check`, and the labelled fixture keys.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pytest

from scripts.council_convening import corpus, generate
from scripts.signed_execution_chain import ed25519

from .conftest import CONFORMANCE, FAMILY_REL, INDEX, LEGACY, REPLACEMENT


def _conformance(root: Path) -> Path:
    return root / FAMILY_REL / "conformance"


def _codes(root: Path) -> list[str]:
    return [finding.code for finding in corpus.check_corpus(root).findings]


def _index(root: Path) -> dict:
    return json.loads((_conformance(root) / "index.json").read_text(encoding="utf-8"))


def _write_index(root: Path, index: dict) -> None:
    (_conformance(root) / "index.json").write_bytes(corpus.dump_json(index))


def _vector_path(root: Path, row: dict) -> Path:
    return _conformance(root) / row["path"]


def _load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _rewrite_vector(root: Path, row: dict, vector: dict) -> None:
    """Write a vector in canonical form, then regenerate the index from the
    vectors, so a row digest never moves alone."""
    _vector_path(root, row).write_bytes(corpus.dump_json(vector))
    generate.generate(root)


def _rows(root: Path) -> list[dict]:
    return _index(root)["cases"]


def _first_row(root: Path, **expected) -> dict:
    for row in _rows(root):
        if all(row["expected"].get(k) == v for k, v in expected.items()):
            return row
    raise AssertionError(f"no row expects {expected}")


# --------------------------------------------------------------------------
# The landed corpus is clean.
# --------------------------------------------------------------------------

def test_the_landed_corpus_has_no_findings():
    report = corpus.check_corpus()
    assert [f"{f.code}: {f.message}" for f in report.findings] == []
    assert report.vectors == len(_index_doc()["cases"]) > 0
    assert report.adjudicated == (report.vectors, report.vectors)


def _index_doc() -> dict:
    return json.loads(INDEX.read_text(encoding="utf-8"))


def test_the_index_header():
    index = _index_doc()
    assert index["schema_version"] == 1
    assert index["kind"] == "openxfactory-council-convening-conformance-index"
    assert index["corpus_id"] == "council-convening-conformance"
    assert index["protocol"] == REPLACEMENT
    assert index["coverage_floor"] == ["FR-001", "FR-002", "FR-003", "FR-004",
                                       "FR-011", "SC-001"]


def test_every_row_digest_is_over_the_raw_bytes():
    for row in _index_doc()["cases"]:
        raw = (CONFORMANCE / row["path"]).read_bytes()
        assert row["sha256"] == "sha256:" + hashlib.sha256(raw).hexdigest()


def test_rows_are_in_bytewise_path_order():
    paths = [row["path"] for row in _index_doc()["cases"]]
    assert paths == sorted(paths, key=lambda p: p.encode("utf-8"))


def test_the_totals_recount():
    index = _index_doc()
    rows = index["cases"]
    assert index["totals"]["vectors"] == len(rows)
    assert index["totals"]["both_sides"] == sum(
        1 for r in rows if r["applies_to"] == ["producer", "consumer"])
    by_area: dict[str, int] = {}
    by_outcome: dict[str, int] = {}
    for row in rows:
        by_area[row["area"]] = by_area.get(row["area"], 0) + 1
        outcome = row["expected"]["outcome"]
        by_outcome[outcome] = by_outcome.get(outcome, 0) + 1
    assert index["totals"]["by_area"] == by_area
    assert index["totals"]["by_outcome"] == by_outcome


def test_phase_1_vectors_are_foundation_vectors_for_both_sides():
    for row in _index_doc()["cases"]:
        if row["area"] != "foundation":
            continue
        assert row["boundary"] in ("definition", "classification")
        assert row["applies_to"] == ["producer", "consumer"]
        vector = _load(CONFORMANCE / row["path"])
        assert vector["expected"]["derived_origin"] == "hand"


def test_the_areas_landed_at_this_commit_are_foundation_and_resolution():
    """Phase 2 adds the `resolution` area, at boundaries `commission` and
    `admission`; every resolution vector is hand-authored."""
    rows = _index_doc()["cases"]
    assert {row["area"] for row in rows} == {"foundation", "resolution"}
    for row in rows:
        if row["area"] == "resolution":
            assert row["boundary"] in ("commission", "admission")
            assert _load(CONFORMANCE / row["path"])["expected"]["derived_origin"] == "hand"


# --------------------------------------------------------------------------
# Closure, in both directions.
# --------------------------------------------------------------------------

def test_an_unindexed_vector_is_refused(family_tree):
    row = _rows(family_tree)[0]
    extra = _vector_path(family_tree, row).with_name("zz-unindexed.json")
    vector = _load(_vector_path(family_tree, row))
    vector["case_id"] = "zz-unindexed"
    extra.write_bytes(corpus.dump_json(vector))
    assert "council-convening-index-closure" in _codes(family_tree)


def test_a_stray_file_of_any_kind_is_refused(family_tree):
    (_conformance(family_tree) / "vectors" / "foundation" / "NOTES.txt").write_text(
        "not a vector\n", encoding="utf-8")
    assert "council-convening-index-closure" in _codes(family_tree)


def test_a_missing_indexed_file_is_refused(family_tree):
    _vector_path(family_tree, _rows(family_tree)[0]).unlink()
    assert "council-convening-index-closure" in _codes(family_tree)


def test_a_row_digest_that_does_not_match_the_bytes_is_refused(family_tree):
    index = _index(family_tree)
    index["cases"][0]["sha256"] = "sha256:" + "0" * 64
    _write_index(family_tree, index)
    assert "council-convening-index-digest" in _codes(family_tree)


def test_rows_out_of_bytewise_order_are_refused(family_tree):
    index = _index(family_tree)
    index["cases"][0], index["cases"][1] = index["cases"][1], index["cases"][0]
    _write_index(family_tree, index)
    assert "council-convening-index-closure" in _codes(family_tree)


def test_a_case_id_that_is_not_the_basename_is_refused(family_tree):
    row = _rows(family_tree)[0]
    vector = _load(_vector_path(family_tree, row))
    vector["case_id"] = vector["case_id"] + "-renamed"
    _rewrite_vector(family_tree, row, vector)
    assert "council-convening-index-closure" in _codes(family_tree)


def test_a_row_that_disagrees_with_its_vector_is_refused(family_tree):
    index = _index(family_tree)
    index["cases"][0]["requirement_ids"] = ["FR-012"]
    _write_index(family_tree, index)
    assert "council-convening-index-closure" in _codes(family_tree)


def test_totals_that_do_not_recount_are_refused(family_tree):
    index = _index(family_tree)
    index["totals"]["vectors"] += 1
    _write_index(family_tree, index)
    assert "council-convening-index-closure" in _codes(family_tree)


def test_an_unknown_index_member_is_refused(family_tree):
    index = _index(family_tree)
    index["extra"] = True
    _write_index(family_tree, index)
    assert "council-convening-index-closure" in _codes(family_tree)


def test_an_unknown_row_member_is_refused(family_tree):
    index = _index(family_tree)
    index["cases"][0]["note"] = "x"
    _write_index(family_tree, index)
    assert "council-convening-index-closure" in _codes(family_tree)


# --------------------------------------------------------------------------
# The vector format.
# --------------------------------------------------------------------------

def test_an_unknown_vector_member_is_refused(family_tree):
    row = _rows(family_tree)[0]
    vector = _load(_vector_path(family_tree, row))
    vector["description"] = "a member the format does not have"
    _rewrite_vector(family_tree, row, vector)
    assert "council-convening-schema" in _codes(family_tree)


def test_evaluation_time_is_required(family_tree):
    row = _rows(family_tree)[0]
    vector = _load(_vector_path(family_tree, row))
    del vector["evaluation_time"]
    _rewrite_vector(family_tree, row, vector)
    assert "council-convening-schema" in _codes(family_tree)


def test_evaluation_time_must_be_a_utc_instant(family_tree):
    row = _rows(family_tree)[0]
    vector = _load(_vector_path(family_tree, row))
    vector["evaluation_time"] = "2026-02-30T00:00:00Z"
    _rewrite_vector(family_tree, row, vector)
    assert "council-convening-schema" in _codes(family_tree)


@pytest.mark.parametrize("origin", ["computed", None, ""])
def test_derived_origin_is_hand_or_generated(family_tree, origin):
    row = _rows(family_tree)[0]
    vector = _load(_vector_path(family_tree, row))
    vector["expected"]["derived_origin"] = origin
    _rewrite_vector(family_tree, row, vector)
    assert "council-convening-schema" in _codes(family_tree)


@pytest.mark.parametrize("applies_to", [[], ["consumer", "producer"],
                                        ["producer", "producer"], ["provider"]])
def test_applies_to_is_a_non_empty_ordered_subset(family_tree, applies_to):
    row = _rows(family_tree)[0]
    vector = _load(_vector_path(family_tree, row))
    vector["applies_to"] = applies_to
    _rewrite_vector(family_tree, row, vector)
    assert "council-convening-schema" in _codes(family_tree)


def test_an_expected_refusal_outside_the_vocabulary_is_refused(family_tree):
    row = _first_row(family_tree, outcome="refuse")
    vector = _load(_vector_path(family_tree, row))
    vector["expected"]["refusal"] = "snapshot_malformed"      # a Phase 3 code
    _rewrite_vector(family_tree, row, vector)
    assert "council-convening-schema" in _codes(family_tree)


def test_a_route_without_findings_is_refused(family_tree):
    row = _first_row(family_tree, outcome="route")
    vector = _load(_vector_path(family_tree, row))
    vector["expected"]["findings"] = []
    _rewrite_vector(family_tree, row, vector)
    assert "council-convening-schema" in _codes(family_tree)


def test_an_environment_oracle_the_format_does_not_name_is_refused(family_tree):
    row = _first_row(family_tree, outcome="route")
    vector = _load(_vector_path(family_tree, row))
    vector.setdefault("environment", {})["weather"] = {"sunny": True}
    _rewrite_vector(family_tree, row, vector)
    assert "council-convening-schema" in _codes(family_tree)


@pytest.mark.parametrize("mutate", [
    lambda raw: b"\xef\xbb\xbf" + raw,            # a byte-order mark
    lambda raw: raw.replace(b"\n", b"\r\n"),      # CRLF
    lambda raw: raw.rstrip(b"\n"),                # no trailing newline
    lambda raw: raw + b"\n",                      # two trailing newlines
])
def test_the_json_byte_form(family_tree, mutate):
    row = _rows(family_tree)[0]
    path = _vector_path(family_tree, row)
    path.write_bytes(mutate(path.read_bytes()))
    assert "council-convening-schema" in _codes(family_tree)


def test_an_unhandled_boundary_at_this_commit_is_not_adjudicated(family_tree):
    row = _first_row(family_tree, outcome="accept")
    vector = _load(_vector_path(family_tree, row))
    vector["boundary"] = "commission"                  # Phase 2's
    _rewrite_vector(family_tree, row, vector)
    assert "council-convening-vector-outcome-mismatch" in _codes(family_tree)


def test_an_expectation_the_reference_does_not_reproduce_is_refused(family_tree):
    row = _first_row(family_tree, refusal="legacy_protocol_refused")
    vector = _load(_vector_path(family_tree, row))
    vector["expected"]["refusal"] = "protocol_not_selected"
    _rewrite_vector(family_tree, row, vector)
    assert "council-convening-vector-outcome-mismatch" in _codes(family_tree)


def test_a_derived_value_the_reference_does_not_reproduce_is_refused(family_tree):
    row = _first_row(family_tree, outcome="route")
    vector = _load(_vector_path(family_tree, row))
    vector["expected"]["derived"] = {"classification": "replacement"}
    _rewrite_vector(family_tree, row, vector)
    assert "council-convening-vector-outcome-mismatch" in _codes(family_tree)


# --------------------------------------------------------------------------
# The `$parts` sentinel.
# --------------------------------------------------------------------------

def test_parts_are_joined_before_anything_else():
    assert corpus.join_parts({"a": {"$parts": ["seat-", "alpha"]}, "b": [1, "x"]}) == {
        "a": "seat-alpha", "b": [1, "x"]}
    assert corpus.join_parts([{"$parts": ["x"]}]) == ["x"]


@pytest.mark.parametrize("value", [
    {"$parts": ["a"], "other": 1},
    {"$parts": "ab"},
    {"$parts": []},
    {"$parts": ["a", 1]},
    {"nested": {"$parts": ["a"], "$extra": True}},
])
def test_a_malformed_parts_object_is_refused(value):
    with pytest.raises(corpus.PartsError):
        corpus.join_parts(value)


def test_a_parts_vector_adjudicates_on_the_joined_value():
    rows = [row for row in _index_doc()["cases"]
            if "$parts" in json.dumps(_load(CONFORMANCE / row["path"])["inputs"])]
    assert rows, "the foundation corpus carries at least one $parts vector"


# --------------------------------------------------------------------------
# Coverage at the commit.
# --------------------------------------------------------------------------

def _drop_rows(root: Path, predicate) -> None:
    for row in _rows(root):
        if predicate(row):
            _vector_path(root, row).unlink()
    generate.generate(root)


def test_every_refusal_code_needs_a_probe(family_tree):
    _drop_rows(family_tree, lambda r: r["expected"]["refusal"] == "protocol_not_selected")
    assert "council-convening-refusal-code-without-probe" in _codes(family_tree)


def test_every_finding_code_needs_a_probe(family_tree):
    _drop_rows(family_tree, lambda r: r["expected"]["outcome"] == "route")
    assert "council-convening-finding-code-without-probe" in _codes(family_tree)


def test_every_coverage_floor_requirement_needs_a_probe(family_tree):
    index = _index(family_tree)
    index["coverage_floor"] = ["FR-001", "FR-011", "FR-012"]
    _write_index(family_tree, index)
    assert "council-convening-requirement-without-probe" in _codes(family_tree)


def test_the_landed_coverage_counts():
    report = corpus.check_corpus()
    # Phase 1's five refusal codes plus Phase 2's twenty-nine (T028).
    assert report.refusals_probed == (34, 34)
    assert report.findings_probed == (1, 1)
    assert report.requirements_probed == (6, 6)
    assert report.coverage_floor == ["FR-001", "FR-002", "FR-003", "FR-004",
                                     "FR-011", "SC-001"]


# --------------------------------------------------------------------------
# The registry_status rule (U4).
# --------------------------------------------------------------------------

def test_a_vector_that_reads_a_status_must_carry_the_override(family_tree):
    row = next(r for r in _rows(family_tree)
               if r["boundary"] == "classification"
               and r["expected"]["outcome"] == "route"
               and _load(_vector_path(family_tree, r))["inputs"]["selected_protocol"] == LEGACY)
    vector = _load(_vector_path(family_tree, row))
    del vector["environment"]["registry_status"]
    if not vector["environment"]:
        del vector["environment"]
    _rewrite_vector(family_tree, row, vector)
    assert "council-convening-vector-registry-status-missing" in _codes(family_tree)


def test_every_landed_vector_that_reads_a_status_carries_it():
    for row in _index_doc()["cases"]:
        vector = _load(CONFORMANCE / row["path"])
        if (row["boundary"] == "classification"
                and vector["inputs"]["selected_protocol"] == LEGACY):
            assert LEGACY in vector.get("environment", {}).get("registry_status", {}), (
                row["case_id"])


# --------------------------------------------------------------------------
# The generator's Phase 1 obligations (T020).
# --------------------------------------------------------------------------

def test_dump_json_is_the_deterministic_form():
    data = {"b": [1, {"d": "x", "c": "y"}], "a": "caf" + chr(0xE9)}
    raw = corpus.dump_json(data)
    assert raw == (b'{\n  "a": "caf\\u00e9",\n  "b": [\n    1,\n    {\n'
                   b'      "c": "y",\n      "d": "x"\n    }\n  ]\n}\n')
    assert raw.endswith(b"}\n") and not raw.endswith(b"\n\n")
    assert b"\r" not in raw


def test_generate_check_reproduces_the_landed_corpus():
    assert generate.check() == []


def test_generate_check_reports_a_reformatted_vector(family_tree):
    row = _rows(family_tree)[0]
    path = _vector_path(family_tree, row)
    path.write_text(json.dumps(_load(path), indent=4) + "\n", encoding="utf-8")
    drift = generate.check(family_tree)
    assert drift and any(row["path"] in line for line in drift)


def test_generate_check_reports_a_stale_index(family_tree):
    index = _index(family_tree)
    index["coverage_floor"] = ["FR-001"]
    _write_index(family_tree, index)
    assert any("index.json" in line for line in generate.check(family_tree))


def test_generate_writes_the_coverage_floor():
    assert generate.COVERAGE_FLOOR == ("FR-001", "FR-002", "FR-003", "FR-004",
                                       "FR-011", "SC-001")


def test_labelled_test_keys_are_deterministic_and_distinct():
    first = generate.test_key("seat-alpha")
    again = generate.test_key("seat-alpha")
    other = generate.test_key("seat-beta")
    assert first.public_key == again.public_key
    assert first.public_key != other.public_key
    assert len(first.public_key) == 32
    assert first.fingerprint == "sha256:" + first.public_key.hex()
    message = b'{"signing_context":"probe"}'
    signature = first.sign(message)
    assert len(signature) == 64
    assert ed25519.verify(first.public_key, message, signature)
    assert not ed25519.verify(other.public_key, message, signature)


def test_a_test_key_never_shows_its_seed():
    key = generate.test_key("seat-alpha")
    seed = generate.seed_for_label("seat-alpha")
    assert seed.hex() not in repr(key)
    assert not any(isinstance(value, (bytes, bytearray)) and value == seed
                   for value in vars(key).values())
