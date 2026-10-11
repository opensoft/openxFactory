"""T025: the commission record and its normative evaluation order (data-model E2).

Every committed `resolution` vector is adjudicated here, and the cases T025
names are pinned again in process, most of them by mutating a committed vector,
so that a test never depends on a vector it does not name.

The order is data-model E2's, steps 1 to 13; the admission-only steps A1 to A5
are not Phase 2's (A1 and A4 are Phase 5's binding, A3 is Phase 3's retry
identity, and A2 and A5 are 025's own guards, outside the corpus). Where the
data-model text leaves an order between two checks of one step open, this
module pins the reading the reference implementation takes, and each such
reading is a vector too:

* step 5 runs its per-source checks source by source, in path order, all five
  on one source before the next (an earlier source's `rule_unauthorized` beats
  a later source's `rule_unavailable`);
* step 8 runs per condition, as the text says;
* step 9 runs its three checks over their own lists, in the listed order, and a
  fact source missing for a contract a condition uses, or present for one no
  condition uses, is `fact_source_mismatch`;
* step 10 evaluates each condition over the authoritative facts in order, where
  an incomplete fact set is `condition_unevaluable` and the bare-directory
  evidence rule is `predicate_parameters_malformed`, and only then compares
  the consumed facts (`consumed_facts_mismatch`): pinned by
  `commission-refuse-bare-directory-evidence-only-in-the-authoritative-facts`,
  `...-only-in-the-consumed-facts` and
  `commission-refuse-order-bare-directory-before-a-later-unevaluable`;
* step 11 checks every condition's `held` before any condition's seat
  (`condition_result_mismatch` before `condition_seat_unbound`);
* step 13 reads the live head in order, and the first read that is not the
  candidate's head names the outcome.

Brett Heap's two rulings of 2026-10-09T17:35:34Z, both the recommended option,
are pinned here as well: "Bind it in PR-2 (Recommended)", under which the rule
projection declares the fact source of each input contract and step 9 refuses a
record whose `fact_sources` differ from it, entry for entry and in order
(`fact_source_mismatch`); and "Sorted and unique (Recommended)", under which a
consumed `changed_paths` is bytewise sorted and duplicate-free, checked at
step 2 (`convening_malformed`), a rename contributing both its paths, each at
its own place in the sort.
"""

from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path

import pytest

from scripts.council_convening import corpus, resolution

from .conftest import CONFORMANCE, REPLACEMENT

VECTORS = CONFORMANCE / "vectors" / "resolution"
CASES = sorted(p.stem for p in VECTORS.glob("*.json"))
SHA = "0123456789abcdef0123456789abcdef01234567"


def load(case_id: str) -> dict:
    """A committed vector, joined and copied, so a test may mutate it."""
    raw = json.loads((VECTORS / f"{case_id}.json").read_text(encoding="utf-8"))
    return copy.deepcopy(corpus.join_parts(raw))


def outcome(vector: dict) -> dict:
    return resolution.adjudicate(vector)


def code(vector: dict):
    return outcome(vector)["refusal"]


def record(vector):
    return vector["inputs"]["record"]


def prov(vector):
    return vector["inputs"]["record"]["required_seats_provenance"]


def env(vector):
    return vector["environment"]


def gkey(vector, path):
    g = prov(vector)["governed"]
    return f"{g['repository']}@{g['revision']}:{path}"


def producer_only(vector: dict) -> dict:
    """A shared commission vector narrowed to the producer, for a case that
    changes an input only the producer reads."""
    vector["applies_to"] = ["producer"]
    vector["environment"].pop("resolved_candidate", None)
    return vector


def as_admission(vector: dict) -> dict:
    """A shared commission vector, run as the consumer runs it (conformance-corpus
    § How each side runs a shared vector)."""
    v = copy.deepcopy(vector)
    v["boundary"] = "admission"
    v["applies_to"] = ["consumer"]
    v["inputs"].pop("expected_candidate", None)
    for key, reads in v["environment"]["live_heads"].items():
        v["environment"]["live_heads"][key] = reads[0]
    return v


BASE = "commission-accept-conditional-seat-not-held"          # classed, standard
HELD = "commission-accept-conditional-seat-held"
UNCLASSED = "commission-accept-unclassed-rule-facts-held"      # the gate-rules shape


# --------------------------------------------------------------------------
# The committed corpus adjudicates, and every shared vector agrees both ways.
# --------------------------------------------------------------------------

def test_the_resolution_area_exists_and_is_not_trivial():
    assert len(CASES) >= 100
    boundaries = {load(c)["boundary"] for c in CASES}
    assert boundaries == {"commission", "admission"}


@pytest.mark.parametrize("case_id", CASES)
def test_every_resolution_vector_adjudicates_to_its_expected(case_id):
    vector = load(case_id)
    got = outcome(vector)
    expected = vector["expected"]
    assert (got["outcome"], got["refusal"], list(got["findings"])) == (
        expected["outcome"], expected["refusal"], expected["findings"])
    assert got["derived"] == expected["derived"]


def _shared_commission_cases():
    """Chosen at collection, never by a skip: `pytest-suite` pins its skip count."""
    out = []
    for case_id in CASES:
        raw = json.loads((VECTORS / f"{case_id}.json").read_text(encoding="utf-8"))
        if raw["boundary"] == "commission" and raw["applies_to"] == ["producer", "consumer"]:
            out.append(case_id)
    return out


@pytest.mark.parametrize("case_id", _shared_commission_cases())
def test_every_shared_commission_vector_reaches_the_same_outcome_at_admission(case_id):
    vector = load(case_id)
    got = outcome(as_admission(vector))
    assert (got["outcome"], got["refusal"]) == (
        vector["expected"]["outcome"], vector["expected"]["refusal"])


def test_only_head_drift_vectors_are_producer_only():
    for case_id in CASES:
        vector = load(case_id)
        if vector["applies_to"] == ["producer"]:
            assert len(next(iter(env(vector)["live_heads"].values()))) > 1, case_id


def test_a_shared_vector_inconsistent_for_the_consumer_is_a_harness_error():
    vector = load(BASE)
    env(vector)["resolved_candidate"]["pull_number"] = 7
    with pytest.raises(resolution.HarnessError):
        outcome(vector)


def test_shared_commission_vectors_carry_tip_values_equal_to_the_revision():
    for case_id in CASES:
        vector = load(case_id)
        if vector["boundary"] != "commission" or vector["applies_to"] != ["producer", "consumer"]:
            continue
        for value in env(vector).get("governed", {}).values():
            if "sha256" in value:
                assert value["tip_sha256"] == value["sha256"], case_id
            else:
                assert value["tip_entries"] == value["entries"], case_id


def test_every_phase_2_refusal_code_has_a_vector():
    phase_2 = {
        "convening_malformed", "council_unknown", "class_unresolved", "class_mismatch",
        "rule_projection_mismatch", "mutable_rule_reference", "rule_revision_ungoverned",
        "governed_sources_mismatch", "rule_path_malformed", "rule_unavailable",
        "rule_unauthorized", "rule_digest_mismatch", "rule_superseded", "predicate_unknown",
        "predicate_parameters_malformed", "condition_unevaluable",
        "condition_result_mismatch", "condition_seat_unbound", "opaque_conclusion",
        "facts_unused", "consumed_facts_mismatch", "fact_source_mismatch",
        "secret_bearing_fact", "candidate_mismatch", "candidate_head_moved",
        "candidate_head_unavailable", "roster_empty", "roster_duplicate_seat",
        "roster_mismatch"}
    assert len(phase_2) == 29
    probed = {load(c)["expected"]["refusal"] for c in CASES}
    assert phase_2 <= probed


def test_no_shared_commission_vector_carries_a_rule_superseded_case():
    for case_id in CASES:
        vector = load(case_id)
        if vector["expected"]["refusal"] == "rule_superseded":
            assert vector["boundary"] == "admission" and vector["applies_to"] == ["consumer"]


# --------------------------------------------------------------------------
# Step 1 before step 2: classification before shape.
# --------------------------------------------------------------------------

def test_classification_runs_before_shape():
    vector = load(BASE)
    record(vector)["protocol"] = "xfc-resolved-council-2"
    record(vector)["notes"] = "malformed as well"
    assert code(vector) == "protocol_unknown"


def test_a_legacy_block_under_the_replacement_selection_is_refused_not_malformed():
    vector = load(BASE)
    vector["inputs"]["record"] = {"council_convening": {
        "council_id": "review-council", "subject_pin": SHA, "packet_refs": ["x#1"]}}
    assert code(vector) == "legacy_protocol_refused"


def test_a_replacement_selection_is_required_and_read():
    vector = load(BASE)
    assert vector["inputs"]["selected_protocol"] == REPLACEMENT


# --------------------------------------------------------------------------
# Step 2: the closed E2 shape, at every depth.
# --------------------------------------------------------------------------

def _shape_targets(vector):
    p = prov(vector)
    return {
        "record": record(vector),
        "provenance": p,
        "candidate": p["candidate"],
        "governed": p["governed"],
        "file source": next(s for s in p["governed"]["sources"] if s["kind"] == "file"),
        "listing source": next(s for s in p["governed"]["sources"] if s["kind"] == "listing"),
        "class_inputs": p["class_inputs"],
        "condition": p["conditions"][0],
        "fact source": p["fact_sources"][0],
        "consumed_facts": p["consumed_facts"],
        "pr_facts": p["consumed_facts"]["pr_facts"],
    }


@pytest.mark.parametrize("where", [
    "record", "provenance", "candidate", "governed", "file source", "listing source",
    "class_inputs", "condition", "fact source", "consumed_facts", "pr_facts"])
def test_an_unknown_member_at_any_depth_is_malformed(where):
    vector = load(BASE)
    _shape_targets(vector)[where]["unexpected_member"] = "x"
    assert code(vector) == "convening_malformed"


@pytest.mark.parametrize("member", ["schema_version", "kind", "protocol", "council_id",
                                    "subject_pin", "packet_refs", "required_seats",
                                    "required_seats_provenance"])
def test_every_required_top_level_member(member):
    vector = load(BASE)
    del record(vector)[member]
    expected = "protocol_unknown" if member == "protocol" else "convening_malformed"
    assert code(vector) == expected


@pytest.mark.parametrize("mutate", [
    pytest.param(lambda r: r.update(packet_refs=[]), id="no-packet-refs"),
    pytest.param(lambda r: r.update(packet_refs=["x"] * 65), id="65-packet-refs"),
    pytest.param(lambda r: r.update(packet_refs=["bad\nref"]), id="control-in-packet-ref"),
    pytest.param(lambda r: r.update(packet_refs="x#1"), id="bare-string-packet-refs"),
    pytest.param(lambda r: r.update(required_seats=["seat-a"] * 65), id="65-seats"),
    pytest.param(lambda r: r.update(required_seats=["seat a"]), id="seat-id-grammar"),
    pytest.param(lambda r: r.update(subject_pin=SHA[:12]), id="abbreviated-pin"),
    pytest.param(lambda r: r.update(mix_id=""), id="empty-mix-id"),
    pytest.param(lambda r: r.update(schema_version=2), id="schema-version"),
])
def test_top_level_shape_refusals(mutate):
    vector = load(BASE)
    mutate(record(vector))
    assert code(vector) == "convening_malformed"


def test_a_record_carrying_only_matched_class_is_malformed():
    vector = load(BASE)
    del prov(vector)["class_inputs"]
    assert code(vector) == "convening_malformed"


def test_a_record_carrying_only_class_inputs_is_malformed():
    vector = load(BASE)
    del prov(vector)["matched_class"]
    assert code(vector) == "convening_malformed"


def test_sources_must_be_in_bytewise_path_order_and_unique():
    vector = load(BASE)
    sources = prov(vector)["governed"]["sources"]
    sources.append(copy.deepcopy(sources[-1]))
    assert code(vector) == "convening_malformed"


def test_a_listing_entry_that_is_not_a_file_source_is_malformed():
    vector = load(BASE)
    for s in prov(vector)["governed"]["sources"]:
        if s["kind"] == "listing":
            s["entries"] = s["entries"] + ["rules/conditions/zz.yaml"]
    assert code(vector) == "convening_malformed"


def test_a_repeated_fact_source_contract_is_malformed():
    vector = load(BASE)
    prov(vector)["fact_sources"].append(copy.deepcopy(prov(vector)["fact_sources"][0]))
    assert code(vector) == "convening_malformed"


def _with_listed_file(vector, path):
    """`path` carried as a governed file and a `rules/conditions` entry by the
    record, the projection and the oracle alike."""
    digest = "sha256:" + "1" * 64
    sources = prov(vector)["governed"]["sources"]
    sources.append({"kind": "file", "path": path, "sha256": digest})
    sources.sort(key=lambda s: s["path"].encode("utf-8"))
    for s in sources:
        if s["kind"] == "listing":
            s["entries"] = sorted(s["entries"] + [path], key=lambda p: p.encode("utf-8"))
    for projection in env(vector)["rules"].values():
        projection["sources"] = sorted(projection["sources"] + [path],
                                       key=lambda p: p.encode("utf-8"))
    env(vector)["governed"][gkey(vector, path)] = {
        "available": True, "governed": True, "sha256": digest, "tip_sha256": digest}
    listing = env(vector)["governed"][gkey(vector, "rules/conditions")]
    listing["entries"] = sorted(listing["entries"] + [path], key=lambda p: p.encode("utf-8"))
    listing["tip_entries"] = list(listing["entries"])
    return vector


def test_a_listed_file_carried_everywhere_is_accepted():
    """The control for the two listing rules below: nothing else refuses."""
    vector = _with_listed_file(load(BASE), "rules/conditions/zz.yaml")
    assert outcome(vector)["outcome"] == "accept"


@pytest.mark.parametrize("path", [
    "rules/conditions/notes.txt",          # no suffix the listing reads
    "rules/conditions/zz.yaml.bak",        # a suffix that is not the last one
    "rules/conditions/nested/deep.yaml",   # not directly inside
    "rules/conditionsx/zz.yaml",           # a sibling directory sharing a prefix
])
def test_a_listing_entry_must_be_directly_inside_with_a_listed_suffix(path):
    """Pre-review L1 (2026-10-09): the entries are the files directly inside the
    listing's path with one of its suffixes, as E2 states, checked at step 2."""
    vector = _with_listed_file(load(BASE), path)
    assert code(vector) == "convening_malformed"


# Brett Heap, 2026-10-09T17:35:34Z, "Sorted and unique (Recommended)" (M3).

def test_consumed_changed_paths_must_be_bytewise_sorted():
    vector = load(BASE)
    prov(vector)["consumed_facts"]["pr_facts"]["changed_paths"].reverse()
    assert code(vector) == "convening_malformed"


def test_consumed_changed_paths_must_be_unique():
    vector = load(BASE)
    paths = prov(vector)["consumed_facts"]["pr_facts"]["changed_paths"]
    paths.insert(0, paths[0])
    assert code(vector) == "convening_malformed"


def test_the_sort_is_bytewise_not_case_folded():
    """`README.md` (0x52) sorts before `docs/a.md` (0x64); the reverse refuses."""
    for paths, expected in ((["README.md", "docs/a.md"], "accept"),
                            (["docs/a.md", "README.md"], "refuse")):
        vector = load(BASE)
        for facts in (prov(vector)["consumed_facts"]["pr_facts"],
                      *env(vector)["facts"].values()):
            facts.update({"changed_paths": list(paths), "changed_files_total": 2,
                          "changed_paths_entry_count": 2})
        assert outcome(vector)["outcome"] == expected, paths


def test_the_order_rule_runs_before_secrets():
    vector = load(BASE)
    paths = prov(vector)["consumed_facts"]["pr_facts"]["changed_paths"]
    paths.append(SECRET_PATH)   # "notes/..." after "src/...": out of order
    assert code(vector) == "convening_malformed"


def test_the_schema_types_what_has_a_semantic_code_and_no_more():
    """data-model: one failing check names one code."""
    vector = load(BASE)
    prov(vector)["governed"]["revision"] = "main"                 # step 5, not shape
    assert code(vector) == "mutable_rule_reference"
    vector = load(BASE)
    prov(vector)["conditions"][0]["predicate"] = "not-a-predicate"
    assert code(vector) == "rule_projection_mismatch"             # step 7 sees it first
    vector = load(BASE)
    record(vector)["required_seats"] = []                         # step 12, not shape
    assert code(vector) == "roster_empty"
    vector = load(BASE)
    prov(vector)["consumed_facts"]["pr_facts"]["changed_files_total"] = 5000
    env(vector)["facts"] = {k: dict(v, changed_files_total=5000)
                            for k, v in env(vector)["facts"].items()}
    assert code(vector) == "condition_unevaluable"                # step 10, not shape


def test_a_non_canonicalizable_value_is_refused_after_the_schema():
    vector = load(BASE)
    prov(vector)["conditions"][0]["parameters"]["weight"] = 0.5
    assert code(vector) == "value_not_canonicalizable"
    vector = load(BASE)
    prov(vector)["conditions"][0]["parameters"]["weight"] = 0.5
    record(vector)["unexpected_member"] = 1
    assert code(vector) == "convening_malformed"


# --------------------------------------------------------------------------
# Step 3: secrets, before any oracle is queried with a free-text value.
# --------------------------------------------------------------------------

SECRET_PATH = "notes/gh" + "p_" + "A1b2C3d4E5f6G7h8I9j0K1l2"
SECRET_REF = "tok" + "en=" + "abcdefghijklmnopqrstu"
SECRET_KEY_ID = "AK" + "IA" + "ABCDEFGHIJKLMNOP"


def insert_sorted(paths: list, path: str) -> None:
    """Add a path where the bytewise sort puts it, so that a record mutated to
    carry it still passes step 2's order rule for `changed_paths`."""
    paths.append(path)
    paths.sort(key=lambda p: p.encode("utf-8"))


@pytest.mark.parametrize("place", ["packet_refs", "class_inputs", "parameters",
                                   "consumed_facts"])
def test_a_secret_in_each_scanned_member_is_refused(place):
    vector = load(BASE)
    p = prov(vector)
    if place == "packet_refs":
        record(vector)["packet_refs"].append(SECRET_REF)
    elif place == "class_inputs":
        p["class_inputs"]["head_ref"] = "topic/" + SECRET_KEY_ID
    elif place == "parameters":
        p["conditions"][0]["parameters"]["protected_paths"].append(SECRET_KEY_ID)
    else:
        insert_sorted(p["consumed_facts"]["pr_facts"]["changed_paths"], SECRET_PATH)
    assert code(vector) == "secret_bearing_fact"


def test_a_secret_is_refused_before_any_oracle_is_read():
    vector = load(BASE)
    insert_sorted(prov(vector)["consumed_facts"]["pr_facts"]["changed_paths"], SECRET_PATH)
    oracles = resolution.VectorOracles(vector["environment"])
    with pytest.raises(resolution.Refused) as caught:
        resolution.resolve(record(vector), boundary="commission",
                           selected_protocol=REPLACEMENT, oracles=oracles,
                           expected_candidate=vector["inputs"]["expected_candidate"])
    assert caught.value.code == "secret_bearing_fact"
    assert oracles.reads == []


def test_the_secret_floor_is_the_providers_own_patterns_loaded_by_import():
    import importlib.util

    from .conftest import REPO_ROOT

    spec = importlib.util.spec_from_file_location(
        "floor_probe", REPO_ROOT / "scripts" / "validate-domain-factory.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    assert [p.pattern for p in resolution.secret_patterns()] == [
        p.pattern for p in module.SECRET_PATTERNS]


def test_a_refusal_never_echoes_the_secret():
    vector = load(BASE)
    insert_sorted(prov(vector)["consumed_facts"]["pr_facts"]["changed_paths"], SECRET_PATH)
    oracles = resolution.VectorOracles(vector["environment"])
    with pytest.raises(resolution.Refused) as caught:
        resolution.resolve(record(vector), boundary="commission",
                           selected_protocol=REPLACEMENT, oracles=oracles,
                           expected_candidate=vector["inputs"]["expected_candidate"])
    assert SECRET_PATH not in str(caught.value)
    assert "A1b2C3d4" not in str(caught.value)


def test_shape_runs_before_secrets():
    vector = load(BASE)
    record(vector)["packet_refs"].append(SECRET_REF)
    record(vector)["unexpected_member"] = 1
    assert code(vector) == "convening_malformed"


# --------------------------------------------------------------------------
# Step 4: candidate identity.
# --------------------------------------------------------------------------

def test_the_subject_pin_is_the_candidate_head():
    vector = load(BASE)
    record(vector)["subject_pin"] = "f" * 40
    assert code(vector) == "candidate_mismatch"


@pytest.mark.parametrize("member, value", [("repository", "example-org/other-app"),
                                           ("pull_number", 43)])
def test_the_candidate_agrees_with_the_trusted_trigger_at_commission(member, value):
    vector = producer_only(load(BASE))
    vector["inputs"]["expected_candidate"][member] = value
    assert code(vector) == "candidate_mismatch"


def test_only_the_members_the_trigger_names_are_compared_at_commission():
    """The merge-readiness trigger names repository and pull_number only."""
    vector = load(BASE)
    assert set(vector["inputs"]["expected_candidate"]) == {"repository", "pull_number"}
    assert code(vector) is None


def test_the_gate_rules_trigger_names_the_subject_path_and_head():
    vector = producer_only(load(UNCLASSED))
    assert set(vector["inputs"]["expected_candidate"]) == {
        "repository", "pull_number", "subject_path", "head_sha"}
    vector["inputs"]["expected_candidate"]["head_sha"] = "f" * 40
    assert code(vector) == "candidate_mismatch"


def test_the_candidate_equals_the_consumers_own_resolution_at_admission():
    vector = as_admission(load(BASE))
    assert code(vector) is None
    env(vector)["resolved_candidate"]["head_sha"] = "f" * 40
    assert code(vector) == "candidate_mismatch"
    vector = as_admission(load(UNCLASSED))
    del env(vector)["resolved_candidate"]["subject_path"]
    assert code(vector) == "candidate_mismatch"


def test_class_inputs_head_ref_must_be_the_authoritative_head_ref():
    """N1."""
    vector = load(BASE)
    env(vector)["head_refs"] = {k: "topic/other" for k in env(vector)["head_refs"]}
    assert code(vector) == "candidate_mismatch"


def test_class_inputs_repository_must_be_the_candidate_repository():
    vector = load(BASE)
    prov(vector)["class_inputs"]["repository"] = "example-org/other-app"
    assert code(vector) == "candidate_mismatch"


# --------------------------------------------------------------------------
# Step 5: governed sources, under OPEN-3 and follow-up 1.
# --------------------------------------------------------------------------

def test_a_mutable_revision_is_refused():
    for revision in ("main", SHA[:12], SHA.upper(), SHA + "\n", "refs/heads/main"):
        vector = load(BASE)
        prov(vector)["governed"]["revision"] = revision
        assert code(vector) == "mutable_rule_reference", revision


def test_an_unlisted_governed_repository_is_refused_before_any_history_read():
    vector = load(BASE)
    prov(vector)["governed"]["repository"] = "former-org/governed-rules"
    oracles = resolution.VectorOracles(vector["environment"])
    with pytest.raises(resolution.Refused) as caught:
        resolution.resolve(record(vector), boundary="commission",
                           selected_protocol=REPLACEMENT, oracles=oracles,
                           expected_candidate=vector["inputs"]["expected_candidate"])
    assert caught.value.code == "rule_unauthorized"
    assert not [r for r in oracles.reads if r[0] == "governed_history"]


def test_a_case_variant_of_the_allowlisted_repository_is_unauthorized():
    vector = load(BASE)
    prov(vector)["governed"]["repository"] = "Example-Org/Governed-Rules"
    assert code(vector) == "rule_unauthorized"


def test_a_revision_off_the_first_parent_history_is_ungoverned():
    vector = load(BASE)
    for value in env(vector)["governed_history"].values():
        value["on_first_parent"] = False
    assert code(vector) == "rule_revision_ungoverned"


def test_an_omitted_source_and_an_extra_source_are_refused():
    vector = load(BASE)
    prov(vector)["governed"]["sources"] = [
        s for s in prov(vector)["governed"]["sources"] if s["path"] != "rules/envelope.yml"]
    assert code(vector) == "governed_sources_mismatch"
    vector = load(BASE)
    for projection in env(vector)["rules"].values():
        projection["sources"] = sorted(projection["sources"] + ["rules/zz.yaml"])
    assert code(vector) == "governed_sources_mismatch"


@pytest.mark.parametrize("change, expected", [
    ({"available": False}, "rule_unavailable"),
    ({"governed": False}, "rule_unauthorized"),
    ({"sha256": "sha256:" + "0" * 64}, "rule_digest_mismatch"),
])
def test_each_per_source_refusal(change, expected):
    vector = load(BASE)
    env(vector)["governed"][gkey(vector, "rules/envelope.yml")].update(change)
    assert code(vector) == expected


def test_a_source_of_the_wrong_kind_is_a_digest_mismatch():
    """Pre-review L4 (2026-10-09): a `file` source where the path holds a listing,
    or a `listing` where it holds a file, differs from the record as a wrong
    digest does, `rule_digest_mismatch`, never a harness error."""
    vector = load(BASE)
    entry = env(vector)["governed"][gkey(vector, "rules/envelope.yml")]
    del entry["sha256"], entry["tip_sha256"]
    entry.update({"entries": [], "tip_entries": []})
    assert code(vector) == "rule_digest_mismatch"
    vector = load(BASE)
    entry = env(vector)["governed"][gkey(vector, "rules/conditions")]
    del entry["entries"], entry["tip_entries"]
    entry.update({"sha256": "sha256:" + "2" * 64, "tip_sha256": "sha256:" + "2" * 64})
    assert code(vector) == "rule_digest_mismatch"


def test_a_governed_entry_holding_neither_kind_is_a_harness_error():
    vector = load(BASE)
    entry = env(vector)["governed"][gkey(vector, "rules/envelope.yml")]
    del entry["sha256"], entry["tip_sha256"]
    with pytest.raises(resolution.HarnessError):
        outcome(vector)


def test_a_listing_whose_entries_differ_at_the_revision_is_a_digest_mismatch():
    vector = load(BASE)
    env(vector)["governed"][gkey(vector, "rules/conditions")]["entries"] = [
        "rules/conditions/paths.yaml"]
    assert code(vector) == "rule_digest_mismatch"


def test_per_source_checks_run_source_by_source():
    vector = load(BASE)
    env(vector)["governed"][gkey(vector, "rules/conditions")]["governed"] = False
    env(vector)["governed"][gkey(vector, "rules/envelope.yml")]["available"] = False
    assert code(vector) == "rule_unauthorized"


@pytest.mark.parametrize("path", ["rules/conditions/paths.yaml", "rules/council-profile.yaml",
                                  "rules/councils/review-council.yaml", "rules/envelope.yml"])
def test_every_governed_source_changed_at_the_tip_is_superseded_at_admission(path):
    """Follow-up 1, "Every governed source (Recommended)": not only the rule file."""
    vector = as_admission(load(BASE))
    env(vector)["governed"][gkey(vector, path)]["tip_sha256"] = "sha256:" + "1" * 64
    assert code(vector) == "rule_superseded"


def test_a_listing_whose_entry_set_changed_at_the_tip_is_superseded_at_admission():
    vector = as_admission(load(BASE))
    entry = env(vector)["governed"][gkey(vector, "rules/conditions")]
    entry["tip_entries"] = entry["entries"] + ["rules/conditions/zz.yaml"]
    assert code(vector) == "rule_superseded"


def test_an_unrelated_unlisted_file_changed_at_the_tip_is_accepted():
    vector = as_admission(load(BASE))
    env(vector)["governed"][gkey(vector, "rules/README.md")] = {
        "available": True, "governed": False,
        "sha256": "sha256:" + "2" * 64, "tip_sha256": "sha256:" + "3" * 64}
    assert outcome(vector)["outcome"] == "accept"


def test_there_is_no_rule_superseded_outcome_at_commission():
    """The commission-time comparison is a non-normative producer pre-check."""
    vector = load(BASE)
    vector["applies_to"] = ["producer"]
    env(vector).pop("resolved_candidate")
    env(vector)["governed"][gkey(vector, "rules/envelope.yml")]["tip_sha256"] = (
        "sha256:" + "1" * 64)
    assert outcome(vector)["outcome"] == "accept"


def test_commission_never_reads_a_tip_value():
    vector = load(BASE)
    vector["applies_to"] = ["producer"]
    env(vector).pop("resolved_candidate")
    for value in env(vector)["governed"].values():
        value.pop("tip_sha256", None)
        value.pop("tip_entries", None)
    assert outcome(vector)["outcome"] == "accept"


def test_admission_without_a_tip_value_is_a_harness_error_not_a_skip():
    vector = as_admission(load(BASE))
    del env(vector)["governed"][gkey(vector, "rules/envelope.yml")]["tip_sha256"]
    with pytest.raises(resolution.HarnessError):
        outcome(vector)


def test_a_digest_mismatch_is_named_before_supersession_on_one_source():
    vector = as_admission(load(BASE))
    entry = env(vector)["governed"][gkey(vector, "rules/envelope.yml")]
    entry["tip_sha256"] = "sha256:" + "1" * 64
    entry["sha256"] = "sha256:" + "4" * 64
    assert code(vector) == "rule_digest_mismatch"


# --------------------------------------------------------------------------
# Step 6: council and class, including the class selector's grammar.
# --------------------------------------------------------------------------

@pytest.mark.parametrize("pattern, head_ref, matched", [
    ("release/*", "release/2026.10", True),
    ("release/*", "release/a/b", False),             # `*` never crosses `/`
    ("release/?", "release/x", True),
    ("release/?", "release/xy", False),
    ("release/?", "release//", False),               # `?` never matches `/`
    ("**/hotfix", "hotfix", True),                   # `**/` matches zero segments
    ("**/hotfix", "a/b/hotfix", True),
    ("**/hotfix", "a/bhotfix", False),
    ("topic/**", "topic/a/b/c", True),               # trailing `**` matches anything
    ("topic/**", "topic/", True),
    ("topic/**", "topics/a", False),
    ("**", "anything/at/all", True),
    ("feature.x", "featureXx", False),               # `.` is literal
    ("feature.x", "feature.x", True),
    ("a+b", "a+b", True),                            # every other character is literal
    ("[ab]", "a", False),
    ("[ab]", "[ab]", True),
    ("main", "main2", False),                        # anchored at the end
    ("main", "xmain", False),                        # anchored at the start
])
def test_the_head_ref_glob_grammar(pattern, head_ref, matched):
    assert resolution.head_ref_matches({"glob": pattern}, head_ref) is matched


def test_an_exact_head_ref_matches_only_itself():
    assert resolution.head_ref_matches({"exact": "release/*"}, "release/*") is True
    assert resolution.head_ref_matches({"exact": "release/*"}, "release/1") is False


def test_the_first_matching_selector_entry_wins():
    selector = [
        {"class": "sensitive", "repositories": ["o/r"], "head_ref": {"exact": "release/1"}},
        {"class": "standard", "repositories": ["o/r"], "head_ref": {"glob": "release/*"}},
    ]
    assert resolution.select_class(selector, {"repository": "o/r", "head_ref": "release/1"}) == "sensitive"
    assert resolution.select_class(selector, {"repository": "o/r", "head_ref": "release/2"}) == "standard"
    assert resolution.select_class(selector, {"repository": "o/x", "head_ref": "release/1"}) is None


def test_both_the_repository_and_the_head_ref_must_match():
    selector = [{"class": "c", "repositories": ["o/a"], "head_ref": {"glob": "**"}}]
    assert resolution.select_class(selector, {"repository": "o/b", "head_ref": "x"}) is None


def test_an_unknown_council():
    vector = load(BASE)
    record(vector)["council_id"] = "unknown-council"
    assert code(vector) == "council_unknown"


def test_a_declared_but_unselected_class_is_refused():
    """U1: a class is never accepted because it exists."""
    vector = load(BASE)
    prov(vector)["matched_class"] = "hotfix"
    assert code(vector) == "class_mismatch"


def test_a_lighter_class_than_the_selector_picks_is_refused():
    vector = load("commission-accept-class-first-match-wins")
    prov(vector)["matched_class"] = "standard"
    assert code(vector) == "class_mismatch"


def test_an_unclassed_council_without_class_inputs_is_accepted():
    """N4: the gate-rules shape."""
    vector = load(UNCLASSED)
    assert "class_inputs" not in prov(vector) and "matched_class" not in prov(vector)
    assert outcome(vector)["outcome"] == "accept"


def test_class_inputs_on_an_unclassed_council_are_refused():
    vector = load(UNCLASSED)
    prov(vector)["class_inputs"] = {"repository": prov(vector)["candidate"]["repository"],
                                    "head_ref": "feature/login"}
    prov(vector)["matched_class"] = "standard"
    env(vector)["head_refs"] = {f"{prov(vector)['candidate']['repository']}#42": "feature/login"}
    assert code(vector) == "class_mismatch"


def test_no_class_inputs_on_a_classed_council_are_refused():
    vector = load(BASE)
    del prov(vector)["class_inputs"]
    del prov(vector)["matched_class"]
    assert code(vector) == "class_mismatch"


def test_a_selector_that_matches_nothing_is_unresolved():
    vector = load(BASE)
    prov(vector)["class_inputs"]["head_ref"] = "unmatched/branch"
    env(vector)["head_refs"] = {k: "unmatched/branch" for k in env(vector)["head_refs"]}
    assert code(vector) == "class_unresolved"


# --------------------------------------------------------------------------
# Step 7: the projection.
# --------------------------------------------------------------------------

def test_standing_seats_and_conditions_must_equal_the_projection():
    vector = load(BASE)
    prov(vector)["standing_seats"] = ["seat-b", "seat-a"]
    record(vector)["required_seats"] = ["seat-b", "seat-a"]
    assert code(vector) == "rule_projection_mismatch"
    vector = load(BASE)
    prov(vector)["conditions"][0]["seat"] = "seat-d"
    assert code(vector) == "rule_projection_mismatch"
    vector = load(BASE)
    prov(vector)["conditions"] = []
    prov(vector)["fact_sources"] = []
    prov(vector)["consumed_facts"] = {}
    assert code(vector) == "rule_projection_mismatch"


def test_held_is_not_part_of_the_projection():
    vector = load(HELD)
    assert prov(vector)["conditions"][0]["held"] is True
    assert outcome(vector)["outcome"] == "accept"


# --------------------------------------------------------------------------
# Steps 9 to 11: facts and held.
# --------------------------------------------------------------------------

def test_the_gate_rules_rule_facts_come_from_the_subject_path_at_the_head():
    """I1: `candidate_subject` reads `rule_facts` at `candidate.subject_path`,
    `candidate.head_sha`."""
    vector = load(UNCLASSED)
    c = prov(vector)["candidate"]
    key = f"rule_facts:{c['repository']}@{c['head_sha']}:{c['subject_path']}"
    assert set(env(vector)["facts"]) == {key}
    env(vector)["facts"] = {key + ".elsewhere": env(vector)["facts"][key]}
    with pytest.raises(resolution.HarnessError):
        outcome(vector)


def test_a_governed_fact_source_reads_at_the_governed_revision():
    vector = load("commission-accept-governed-source-rule-facts")
    g = prov(vector)["governed"]
    assert set(env(vector)["facts"]) == {
        f"rule_facts:{g['repository']}@{g['revision']}:rules/conditions/posture.yml"}
    assert outcome(vector)["outcome"] == "accept"


def test_a_pr_facts_source_must_be_the_candidate_pull():
    vector = load(BASE)
    prov(vector)["fact_sources"][0]["source"] = {"governed_path": "rules/envelope.yml"}
    assert code(vector) == "fact_source_mismatch"


def test_a_fact_source_for_each_contract_in_use_and_no_other():
    vector = load(BASE)
    prov(vector)["fact_sources"] = []
    assert code(vector) == "fact_source_mismatch"
    vector = load(BASE)
    prov(vector)["fact_sources"].append(
        {"input_contract": "rule_facts", "source": "candidate_subject"})
    assert code(vector) == "fact_source_mismatch"


def test_an_absent_consumed_fact_is_an_opaque_conclusion():
    for fact in ("changed_paths", "changed_files_total", "changed_paths_entry_count"):
        vector = load(BASE)
        del prov(vector)["consumed_facts"]["pr_facts"][fact]
        assert code(vector) == "opaque_conclusion", fact


def test_an_unused_consumed_fact_is_refused():
    vector = load(BASE)
    prov(vector)["consumed_facts"]["rule_facts"] = {"rule_touched_paths": []}
    assert code(vector) == "facts_unused"


def test_an_empty_object_for_an_unused_contract_is_unused():
    """Pre-review L2 (2026-10-09): `{"rule_facts": {}}` beside no `rule_facts`
    condition is `facts_unused`, so one resolution has one encoding and Phase 3's
    retry identity never sees two."""
    vector = load("commission-accept-standing-only")
    prov(vector)["consumed_facts"] = {"rule_facts": {}}
    assert code(vector) == "facts_unused"


def test_consumed_facts_must_equal_the_authoritative_facts():
    vector = load(BASE)
    prov(vector)["consumed_facts"]["pr_facts"]["changed_paths"] = ["README.md"]
    assert code(vector) == "consumed_facts_mismatch"


def test_rule_touched_paths_compare_in_order():
    """Reading 6, which the M3 ruling leaves standing for `rule_facts`: no order is
    specified for `rule_touched_paths`, so none is normalized."""
    vector = load(UNCLASSED)
    touched = prov(vector)["consumed_facts"]["rule_facts"]["rule_touched_paths"]
    assert len(touched) == 2
    touched.reverse()
    assert code(vector) == "consumed_facts_mismatch"


# Brett Heap, 2026-10-09T17:35:34Z, "Bind it in PR-2 (Recommended)" (H1).

def _declared(vector):
    """The projection's entry for the convened council or its selected class."""
    for projection in env(vector)["rules"].values():
        council = projection["councils"][record(vector)["council_id"]]
        if "classes" in council:
            return council["classes"][prov(vector)["matched_class"]]
        return council
    raise AssertionError("no projection")


def test_the_projection_declares_each_contracts_fact_source():
    for case_id in (BASE, UNCLASSED, "commission-accept-governed-source-rule-facts",
                    "commission-accept-two-input-contracts-in-projection-order"):
        vector = load(case_id)
        assert _declared(vector)["fact_sources"] == prov(vector)["fact_sources"], case_id


def test_fact_sources_that_differ_from_the_projection_are_refused():
    vector = load(UNCLASSED)
    _declared(vector)["fact_sources"] = [
        {"input_contract": "rule_facts", "source": {"governed_path": "rules/envelope.yml"}}]
    assert code(vector) == "fact_source_mismatch"


def test_the_pre_reviews_probe_is_refused():
    """The gate-rules shape pointed at the council profile, both `held` false: it
    passed every check before the binding, and dropped seat-r2."""
    vector = load("commission-refuse-fact-source-swapped-to-a-governed-file")
    assert record(vector)["required_seats"] == ["seat-r1"]
    assert all(c["held"] is False for c in prov(vector)["conditions"])
    assert code(vector) == "fact_source_mismatch"
    _declared(vector)["fact_sources"] = copy.deepcopy(prov(vector)["fact_sources"])
    assert outcome(vector)["outcome"] == "accept"   # the binding is what refuses it


def test_fact_sources_follow_the_projections_order():
    vector = load("commission-refuse-fact-sources-out-of-projection-order")
    assert code(vector) == "fact_source_mismatch"
    prov(vector)["fact_sources"].reverse()
    assert outcome(vector)["outcome"] == "accept"


def test_the_structural_fact_source_rules_still_run_first():
    """A source no contract allows is refused by the structural rule, before the
    projection is compared; the code is the same."""
    vector = load(BASE)
    prov(vector)["fact_sources"][0]["source"] = "candidate_subject"
    _declared(vector)["fact_sources"] = copy.deepcopy(prov(vector)["fact_sources"])
    assert code(vector) == "fact_source_mismatch"


@pytest.mark.parametrize("damage", ["absent", "not_a_list"])
def test_a_projection_without_declared_fact_sources_is_a_harness_error(damage):
    vector = load(BASE)
    if damage == "absent":
        del _declared(vector)["fact_sources"]
    else:
        _declared(vector)["fact_sources"] = {"pr_facts": "candidate_pull"}
    with pytest.raises(resolution.HarnessError):
        outcome(vector)


def test_held_must_equal_the_reference_evaluation():
    vector = load(BASE)
    prov(vector)["conditions"][0]["held"] = True
    record(vector)["required_seats"] = ["seat-a", "seat-b", "seat-c"]
    assert code(vector) == "condition_result_mismatch"


def test_every_held_is_checked_before_any_seat():
    vector = load("commission-refuse-order-result-before-seat-unbound")
    assert code(vector) == "condition_result_mismatch"


def test_a_held_condition_with_no_seat_is_unbound():
    vector = load("commission-refuse-condition-seat-unbound")
    assert code(vector) == "condition_seat_unbound"


def test_an_unseated_condition_that_does_not_hold_is_accepted():
    vector = load(UNCLASSED)
    assert prov(vector)["conditions"][0]["seat"] is None
    assert prov(vector)["conditions"][0]["held"] is False
    assert outcome(vector)["outcome"] == "accept"


# --------------------------------------------------------------------------
# Step 12: roster composition (R6).
# --------------------------------------------------------------------------

def test_the_expected_roster_is_standing_then_held_seats_appended_if_absent():
    conditions = [
        {"seat": "c", "held": True}, {"seat": "a", "held": True},
        {"seat": "d", "held": False}, {"seat": None, "held": False},
        {"seat": "e", "held": True}, {"seat": "c", "held": True}]
    assert resolution.expected_roster(["a", "b"], conditions) == ["a", "b", "c", "e"]


@pytest.mark.parametrize("seats, expected", [
    ([], "roster_empty"),
    (["seat-a", "seat-a", "seat-b"], "roster_duplicate_seat"),
    (["seat-b", "seat-a"], "roster_mismatch"),           # reordered
    (["seat-a", "seat-c"], "roster_mismatch"),           # same-count substitution
    (["seat-a"], "roster_mismatch"),                     # missing
    (["seat-a", "seat-b", "seat-c"], "roster_mismatch"),  # extra
])
def test_roster_refusals(seats, expected):
    vector = load(BASE)
    record(vector)["required_seats"] = seats
    assert code(vector) == expected


def test_a_conditional_seat_already_standing_appears_once():
    vector = load("commission-accept-conditional-seat-already-standing")
    assert record(vector)["required_seats"] == ["seat-a", "seat-b", "seat-c", "seat-d"]
    assert outcome(vector)["outcome"] == "accept"
    record(vector)["required_seats"] = ["seat-a", "seat-b", "seat-c", "seat-c", "seat-d"]
    assert code(vector) == "roster_duplicate_seat"


def test_an_empty_expected_roster_is_never_accepted():
    vector = load("commission-refuse-roster-empty")
    assert record(vector)["required_seats"] == []
    assert code(vector) == "roster_empty"


# --------------------------------------------------------------------------
# Step 13: the live head, the last read of the candidate's head.
# --------------------------------------------------------------------------

MOVED = "f" * 40


def _heads(vector, reads):
    key = next(iter(env(vector)["live_heads"]))
    env(vector)["live_heads"][key] = reads


def test_head_moved_before_the_recheck():
    vector = load(BASE)
    _heads(vector, [MOVED])
    assert code(vector) == "candidate_head_moved"


def test_head_moved_after_the_recheck_refuses_at_commission():
    vector = load(BASE)
    vector["applies_to"] = ["producer"]
    env(vector).pop("resolved_candidate")
    head = record(vector)["subject_pin"]
    _heads(vector, [head, MOVED])
    assert code(vector) == "candidate_head_moved"


def test_head_moved_and_restored_still_refuses():
    vector = load(BASE)
    vector["applies_to"] = ["producer"]
    env(vector).pop("resolved_candidate")
    head = record(vector)["subject_pin"]
    _heads(vector, [MOVED, head])
    assert code(vector) == "candidate_head_moved"


def test_head_moved_at_admission_after_a_clean_commission():
    vector = load(BASE)
    assert outcome(vector)["outcome"] == "accept"
    admitted = as_admission(vector)
    _heads(admitted, MOVED)
    assert code(admitted) == "candidate_head_moved"


@pytest.mark.parametrize("boundary", ["commission", "admission"])
def test_head_unavailable(boundary):
    vector = load(BASE)
    if boundary == "admission":
        vector = as_admission(vector)
        _heads(vector, "unavailable")
    else:
        _heads(vector, ["unavailable"])
    assert code(vector) == "candidate_head_unavailable"


def test_the_first_read_that_is_not_the_head_names_the_outcome():
    vector = load(BASE)
    vector["applies_to"] = ["producer"]
    env(vector).pop("resolved_candidate")
    _heads(vector, [MOVED, "unavailable"])
    assert code(vector) == "candidate_head_moved"
    _heads(vector, ["unavailable", MOVED])
    assert code(vector) == "candidate_head_unavailable"


def test_the_live_head_is_read_last():
    vector = load(BASE)
    oracles = resolution.VectorOracles(vector["environment"])
    resolution.resolve(record(vector), boundary="commission", selected_protocol=REPLACEMENT,
                       oracles=oracles, expected_candidate=vector["inputs"]["expected_candidate"])
    assert oracles.reads[-1][0] == "live_heads"
    assert [r[0] for r in oracles.reads].count("live_heads") == 1


# --------------------------------------------------------------------------
# The adjacent pairs of steps, each pinned by one two-defect record.
# --------------------------------------------------------------------------

def _defect(step, vector):
    p = prov(vector)
    if step == 1:
        record(vector)["protocol"] = "xfc-resolved-council-2"
    elif step == 2:
        record(vector)["unexpected_member"] = 1
    elif step == 3:
        record(vector)["packet_refs"].append(SECRET_REF)
    elif step == 4:
        record(vector)["subject_pin"] = MOVED
    elif step == 5:
        p["governed"]["revision"] = "main"
    elif step == 6:
        record(vector)["council_id"] = "unknown-council"
    elif step == 7:
        p["standing_seats"] = ["seat-a"]
    elif step == 8:
        p["conditions"][0]["parameters"] = {"protected_paths": ["/bad"]}
        for projection in env(vector)["rules"].values():
            klass = projection["councils"]["review-council"]["classes"]["standard"]
            klass["conditions"][0]["parameters"] = {"protected_paths": ["/bad"]}
    elif step == 9:
        p["consumed_facts"]["rule_facts"] = {"rule_touched_paths": []}
    elif step == 10:
        for facts in env(vector)["facts"].values():
            facts["changed_files_total"] += 1
    elif step == 11:
        p["conditions"][0]["held"] = True
    elif step == 12:
        record(vector)["required_seats"] = list(reversed(record(vector)["required_seats"]))
    elif step == 13:
        _heads(vector, [MOVED])


FIRST_CODE = {1: "protocol_unknown", 2: "convening_malformed", 3: "secret_bearing_fact",
              4: "candidate_mismatch", 5: "mutable_rule_reference", 6: "council_unknown",
              7: "rule_projection_mismatch", 8: "predicate_parameters_malformed",
              9: "facts_unused", 10: "condition_unevaluable",
              11: "condition_result_mismatch", 12: "roster_mismatch",
              13: "candidate_head_moved"}


@pytest.mark.parametrize("step", range(1, 14))
def test_each_single_defect_names_its_step(step):
    vector = load(BASE)
    _defect(step, vector)
    assert code(vector) == FIRST_CODE[step]


@pytest.mark.parametrize("earlier", range(1, 13))
def test_each_adjacent_pair_of_steps_yields_the_earlier_code(earlier):
    vector = load(BASE)
    _defect(earlier + 1, vector)
    _defect(earlier, vector)
    assert code(vector) == FIRST_CODE[earlier]


# --------------------------------------------------------------------------
# convening_digest: known answers from outside this code.
# --------------------------------------------------------------------------

def test_convening_digest_is_the_construction_over_the_whole_record():
    vector = load(HELD)
    digest = resolution.convening_digest(record(vector))
    assert set(digest) == {"construction", "subject", "value"}
    assert digest["construction"] == "xfc-jcs-sha256-1"
    assert digest["subject"] == "council_convening"
    assert digest == vector["expected"]["derived"]["convening_digest"]


def test_convening_digest_known_answer_with_hand_written_canonical_bytes():
    """The canonical bytes are written here by hand, following RFC 8785: members
    sorted by UTF-16 code units, so U+1F600 (a surrogate pair, D83D DE00) sorts
    before U+E000, and both after ASCII; no insignificant whitespace."""
    value = {"": 1, "\U0001F600": 2, "z": [True, None, "x"], "a": {"b": -3}}
    canonical_bytes = '{"a":{"b":-3},"z":[true,null,"x"],"\U0001F600":2,"":1}'.encode("utf-8")
    assert resolution.convening_digest(value)["value"] == (
        "sha256:" + hashlib.sha256(canonical_bytes).hexdigest())


def test_convening_digest_ignores_transport_member_order():
    vector = load(HELD)
    reordered = dict(reversed(list(record(vector).items())))
    assert resolution.convening_digest(reordered) == resolution.convening_digest(record(vector))


def test_an_accepted_resolution_returns_the_roster_and_the_digest():
    vector = load(HELD)
    result = resolution.resolve(record(vector), boundary="commission",
                                selected_protocol=REPLACEMENT,
                                oracles=resolution.VectorOracles(vector["environment"]),
                                expected_candidate=vector["inputs"]["expected_candidate"])
    assert result.required_seats == ["seat-a", "seat-b", "seat-c"]
    assert result.convening_digest == vector["expected"]["derived"]["convening_digest"]


# --------------------------------------------------------------------------
# Oracle data the vector does not carry is a harness error, never a pass.
# --------------------------------------------------------------------------

@pytest.mark.parametrize("oracle", ["governed_history", "governed", "rules", "facts",
                                    "live_heads", "head_refs", "governed_repositories"])
def test_a_missing_oracle_is_a_harness_error(oracle):
    vector = load(BASE)
    del env(vector)[oracle]
    with pytest.raises(resolution.HarnessError):
        outcome(vector)


def test_an_unknown_boundary_is_a_harness_error():
    vector = load(BASE)
    vector["boundary"] = "registration"
    with pytest.raises(resolution.HarnessError):
        outcome(vector)
