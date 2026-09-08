"""ONE TEST PER RATIFIED SCENARIO of
`amend-chain-anchoring-readiness-and-durability` — twenty for requirement 2
(*"Fixed UTC durability batches account for every accepted event exactly
once"*) and fourteen for requirement 3 (*"Witness submission and confirmation
remain distinct evidence states"*), thirty-four in all, each named for the
scenario it pins.

WHY A SECOND MODULE AND NOT MORE OF THE FIRST. `test_anchoring_reader.py`
adjudicates the READER — its corpus, its coverage, its exit codes. This module
adjudicates the RATIFIED DELTA: each test names a scenario, builds the record
set that scenario describes, and asserts the outcome the scenario states. A
scenario with no test is a scenario nobody has seen hold, and a scenario whose
test asserts something else is worse than none.

EVERY TEST RUNS OVER A MINIMAL SCOPE rather than the whole packaged corpus.
The durability records are self-contained — three consecutive windows, their
admissions, manifests, receipts and states, plus the two registers and the
released construction — and the reader's own self-test already adjudicates all
forty-one positives together. Repeating that here would multiply a quadratic
cost for no additional evidence.
"""

from __future__ import annotations

import copy
import importlib.util
import sys
from pathlib import Path

import pytest
import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from scripts.signed_execution_chain import canonical  # noqa: E402

VALIDATOR_PATH = REPO_ROOT / "scripts" / "validate-chain-anchoring.py"
CONTRACT_DIR = REPO_ROOT / "contracts" / "chain-anchoring"
EXAMPLES = CONTRACT_DIR / "examples"
NEGATIVES = EXAMPLES / "negative"

DURABILITY_FILES = (
    "confirmation-profile-1-operational-versions.example.yaml",
    "confirmation-profile-2-durability-and-ordering-only.example.yaml",
    "confirmation-profile-registry-1-append-only.example.yaml",
    "daily-merkle-profile-1-released.example.yaml",
    "durability-eligibility-registry-1-append-only.example.yaml",
    "durability-batch-admission-1-window-and-replay.example.yaml",
    "durability-batch-admission-2-late-source-time.example.yaml",
    "durability-batch-manifest-1-first-day-genesis.example.yaml",
    "durability-batch-manifest-2-empty-day-linked.example.yaml",
    "durability-batch-manifest-3-late-arrival-linked.example.yaml",
    "anchor-receipt-5-daily-item-both-witnesses-confirmed.example.yaml",
    "anchor-receipt-6-daily-empty-window-anchored.example.yaml",
    "anchor-receipt-7-daily-durability-unupgraded.example.yaml",
    "anchor-state-5-daily-both-confirmed.example.yaml",
    "anchor-state-6-daily-durability-submitted-chain-pending.example.yaml",
)

OP = "chain-example-operational"
DUR = "chain-example-durability"


def _load_reader():
    spec = importlib.util.spec_from_file_location(
        "validate_chain_anchoring_scenarios", VALIDATOR_PATH)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


reader = _load_reader()


@pytest.fixture(scope="module")
def registry_and_docs():
    return reader.build_registry()


def _records(paths):
    out = []
    for path in paths:
        out.extend(reader.labelled("scenario", path))
    return copy.deepcopy(out)


@pytest.fixture(scope="module")
def base_records():
    """The durability subset of the packaged corpus, as one coherent scope."""
    return _records([EXAMPLES / name for name in DURABILITY_FILES])


def _validate(records, registry_and_docs):
    findings = reader.Findings()
    registry, docs = registry_and_docs
    reader.validate_scope(findings, records, registry, docs)
    return findings


def _codes(findings):
    return reader.codes_of(findings.errors)


def _fixture(code):
    """The packaged negative named for a refusal code, adjudicated in the
    durability scope rather than the whole corpus."""
    return copy.deepcopy(reader.labelled("negative", NEGATIVES / f"{code}.yaml"))


def _with(base, code):
    return list(base) + _fixture(code)


def _pick(base, key, value):
    return copy.deepcopy(next(doc for _, doc in base
                              if isinstance(doc, dict) and doc.get(key) == value))


def _swap(base, key, value, mutated):
    """The base scope with the record identified by `key`/`value` replaced."""
    out = []
    for label, doc in base:
        if isinstance(doc, dict) and doc.get(key) == value:
            out.append((label, mutated))
        else:
            out.append((label, copy.deepcopy(doc)))
    return out


def _reseal_manifest(doc):
    doc["material_digest"]["value"] = canonical.digest(doc["terms"])
    return doc


def _reseal_receipt(doc):
    doc["anchored_digest"]["value"] = canonical.digest(
        {"material_digest": doc["material_digest"],
         "mint_time_configuration": doc["mint_time_configuration"]})
    for entry in doc["per_chain_anchors"]:
        entry["commitment_derivation"]["source_aggregation_root"]["value"] = \
            doc["anchored_digest"]["value"]
    return doc


# ======================================================================
# Requirement 2 — fixed UTC durability batches account for every accepted
# event exactly once
# ======================================================================

def test_a_non_empty_utc_window_closes(base_records, registry_and_docs):
    """WHEN a fixed UTC window closes with one or more accepted events THEN its
    signed manifest accounts for every eligible accepted sequence exactly once,
    every event has a valid path into `daily_batch_root`, and the recomputed
    configuration-bound `anchored_digest` becomes the one item whose aggregation
    root enters both witnesses."""
    assert not _validate(base_records, registry_and_docs).errors
    manifest = _pick(base_records, "manifest_id", "dbm-example-0001")
    receipt = _pick(base_records, "receipt_id", "rcp-example-daily-0001")
    terms = manifest["terms"]
    assert terms["event_count"] == 2
    assert (terms["first_leaf_sequence"], terms["last_leaf_sequence"]) == (641, 642)
    # the root really reproduces from the window's ordered leaves
    admissions = [doc for _, doc in base_records
                  if doc.get("kind", "").endswith("durability_batch_admission")
                  and doc.get("window_open") == terms["window_open"]
                  and doc.get("admission_kind") == "new_leaf"]
    construction = _pick(base_records, "profile_id",
                         "dmp-example-daily-merkle")["construction"]
    leaves = [a["event_leaf_digest"]["value"]
              for a in sorted(admissions, key=lambda a: a["leaf_sequence"])]
    assert reader._batch_root(construction, leaves) == \
        terms["daily_batch_root"]["value"]
    # and the receipt's anchored digest is the one item both witnesses carry
    assert receipt["material_digest"]["value"] == manifest["material_digest"]["value"]
    assert receipt["aggregation_merkle_path"] == []
    roots = {e["commitment_derivation"]["source_aggregation_root"]["value"]
             for e in receipt["per_chain_anchors"]}
    assert roots == {receipt["anchored_digest"]["value"]}
    assert {e["chain_id"] for e in receipt["per_chain_anchors"]} == {OP, DUR}


def test_an_empty_utc_window_closes(base_records, registry_and_docs):
    """WHEN a fixed UTC window closes with no eligible accepted events THEN a
    signed count-zero manifest binds the deterministic empty `daily_batch_root`
    and the immediately preceding `previous_daily_anchored_digest`, and its
    configuration-bound `anchored_digest` enters both configured witness paths
    as the daily anchored item."""
    manifest = _pick(base_records, "manifest_id", "dbm-example-0002")
    day_one = _pick(base_records, "receipt_id", "rcp-example-daily-0001")
    construction = _pick(base_records, "profile_id",
                         "dmp-example-daily-merkle")["construction"]
    terms = manifest["terms"]
    assert terms["event_count"] == 0
    assert "first_leaf_sequence" not in terms and "last_leaf_sequence" not in terms
    assert terms["daily_batch_root"]["value"] == construction["empty_root"]["value"]
    assert terms["previous_daily_anchored_digest"]["value"] == \
        day_one["anchored_digest"]["value"]
    receipt = _pick(base_records, "receipt_id", "rcp-example-daily-0002")
    assert {e["chain_id"] for e in receipt["per_chain_anchors"]} == {OP, DUR}
    assert not _validate(base_records, registry_and_docs).errors


def test_a_source_time_event_arrives_after_its_earlier_day_closed(
        base_records, registry_and_docs):
    """WHEN an event's source time belongs to a closed prior window but its
    trusted log acceptance belongs to the current open window THEN the prior
    manifest remains unchanged and the event enters the current window exactly
    once with source-time lateness recorded off chain."""
    late = _pick(base_records, "admission_id", "dba-example-0004")
    assert late["owner_source_time"] < late["window_open"]
    assert late["window_open"] <= late["trusted_acceptance_time"] < late["window_close"]
    assert late["late_arrival_rule"]["window_selected_from"] == \
        "trusted_acceptance_time"
    assert late["late_arrival_rule"]["source_time_lateness_recorded"] == "off_chain"
    # exactly once, and in the CURRENT window only
    same_leaf = [doc for _, doc in base_records
                 if doc.get("event_leaf_digest", {}).get("value")
                 == late["event_leaf_digest"]["value"]]
    assert len(same_leaf) == 1
    # the earlier day's manifest is untouched by it
    day_one = _pick(base_records, "manifest_id", "dbm-example-0001")
    assert late["leaf_sequence"] > day_one["terms"]["last_leaf_sequence"]
    assert not _validate(base_records, registry_and_docs).errors


def test_acceptance_occurs_exactly_at_utc_midnight(base_records, registry_and_docs):
    """WHEN the trusted log acceptance timestamp is exactly `00:00:00Z` THEN the
    event enters the new UTC window because the prior window's exclusive
    boundary has passed."""
    midnight = _pick(base_records, "admission_id", "dba-example-0005")
    assert midnight["trusted_acceptance_time"] == "2026-09-01T00:00:00Z"
    assert midnight["window_open"] == "2026-09-01T00:00:00Z"
    # the PRIOR window is the one that closed at that instant, and it does not
    # hold this event
    prior = _pick(base_records, "manifest_id", "dbm-example-0002")
    assert prior["terms"]["window_close"] == midnight["window_open"]
    assert prior["terms"]["event_count"] == 0
    assert not _validate(base_records, registry_and_docs).errors
    # and the same instant declared as the PRIOR window's is refused, because
    # the interval is half-open
    moved = copy.deepcopy(midnight)
    moved["window_open"], moved["window_close"] = prior["terms"]["window_open"], \
        prior["terms"]["window_close"]
    findings = _validate(_swap(base_records, "admission_id", "dba-example-0005",
                               moved), registry_and_docs)
    assert "admission-window-acceptance-mismatch" in _codes(findings)


def test_admission_races_the_midnight_close(base_records, registry_and_docs):
    """WHEN event admission and window closure execute concurrently at the
    exclusive UTC boundary THEN the atomic admission/close order places the
    event in exactly one window, and its sequence cannot appear on both sides or
    invert the acceptance-time partition."""
    # the atomicity is DECLARED, and a realization that declares otherwise is
    # refused for the step it skipped
    findings = _validate(_with(base_records, "durability_admission_not_atomic"),
                         registry_and_docs)
    assert "durability_admission_not_atomic" in _codes(findings)
    # one event on both sides of a boundary is refused
    findings = _validate(
        _with(base_records, "durability_event_assigned_to_two_windows"),
        registry_and_docs)
    assert "durability_event_assigned_to_two_windows" in _codes(findings)
    # and a sequence that inverts the acceptance partition is refused
    findings = _validate(
        _with(base_records, "durability_sequence_inverts_acceptance_partition"),
        registry_and_docs)
    assert "durability_sequence_inverts_acceptance_partition" in _codes(findings)


def test_a_minter_omits_the_final_eligible_admissions(base_records,
                                                      registry_and_docs):
    """WHEN a manifest lowers its last sequence and event count to match a
    retained prefix while the bound signed-log checkpoint covers later eligible
    admissions before `close_sequence_watermark` THEN canonical checkpoint
    reconciliation detects the omitted suffix and REFUSES the batch before
    witness verification."""
    findings = _validate(
        _with(base_records,
              "durability_batch_summary_lowered_below_watermark"),
        registry_and_docs)
    assert "durability_batch_summary_lowered_below_watermark" in _codes(findings)
    # the fixture's own numbers are SELF-CONSISTENT, which is the point
    fixture = [doc for _, doc in _fixture(
        "durability_batch_summary_lowered_below_watermark")]
    manifest = next(d for d in fixture if "terms" in d)
    assert manifest["terms"]["event_count"] == 1
    assert manifest["terms"]["first_leaf_sequence"] == \
        manifest["terms"]["last_leaf_sequence"]


def test_an_identical_dedupe_key_and_digest_are_replayed(base_records,
                                                         registry_and_docs):
    """WHEN the log receives a dedupe key and material digest it already
    accepted THEN it returns the existing admission acknowledgement carrying
    leaf sequence and material digest, returns no pre-closure anchor receipt,
    and creates no second batch admission."""
    replay = _pick(base_records, "admission_id", "dba-example-0003")
    original = _pick(base_records, "admission_id", "dba-example-0001")
    assert replay["admission_kind"] == "replay_acknowledgement"
    assert replay["dedupe_key_ref"] == original["dedupe_key_ref"]
    assert replay["material_digest"] == original["material_digest"]
    assert replay["replay_of_leaf_sequence"] == replay["leaf_sequence"] \
        == original["leaf_sequence"]
    assert "pre_closure_anchor_receipt_ref" not in replay
    assert not _validate(base_records, registry_and_docs).errors
    # the replay does NOT enlarge the batch: the manifest still counts two
    manifest = _pick(base_records, "manifest_id", "dbm-example-0001")
    assert manifest["terms"]["event_count"] == 2
    # a replay that consumed a second sequence is refused
    findings = _validate(
        _with(base_records, "dedupe_replay_consumed_a_second_sequence"),
        registry_and_docs)
    assert "dedupe_replay_consumed_a_second_sequence" in _codes(findings)
    # and so is a constituent event holding an anchor receipt of its own
    findings = _validate(
        _with(base_records, "constituent_event_given_separate_receipt"),
        registry_and_docs)
    assert "constituent_event_given_separate_receipt" in _codes(findings)


def test_a_dedupe_key_is_reused_for_different_content(base_records,
                                                      registry_and_docs):
    """WHEN the log receives an accepted dedupe key with a different material
    digest THEN admission is REFUSED and no leaf sequence is assigned."""
    findings = _validate(
        _with(base_records, "dedupe_key_reused_for_different_content"),
        registry_and_docs)
    assert "dedupe_key_reused_for_different_content" in _codes(findings)
    # the same refusal fires on the SET as well as on the declared rule: an
    # accepted key offered again for different material
    clash = _pick(base_records, "admission_id", "dba-example-0004")
    clash["admission_id"] = "dba-scenario-clash"
    clash["dedupe_key_ref"] = _pick(base_records, "admission_id",
                                    "dba-example-0001")["dedupe_key_ref"]
    findings = _validate(list(base_records) + [("scenario/clash", clash)],
                         registry_and_docs)
    assert "dedupe_key_reused_for_different_content" in _codes(findings)
    # and the key stays off public chains
    findings = _validate(_with(base_records, "dedupe_key_reachable_from_anchor"),
                         registry_and_docs)
    assert "dedupe_key_reachable_from_anchor" in _codes(findings)


def test_an_accepted_event_is_omitted_from_the_daily_root(base_records,
                                                          registry_and_docs):
    """WHEN reconciliation finds an accepted sequence in the window with no path
    into the closed batch THEN the batch is REFUSED as incomplete even if its
    root has valid witness evidence."""
    findings = _validate(_with(base_records, "durability_batch_omits_accepted_event"),
                         registry_and_docs)
    assert "durability_batch_omits_accepted_event" in _codes(findings)
    # and a membership path stripped from an admission of a real closed window
    # is refused there too, with the witness proofs left untouched
    stripped = _pick(base_records, "admission_id", "dba-example-0001")
    stripped["membership_path"] = []
    findings = _validate(_swap(base_records, "admission_id", "dba-example-0001",
                               stripped), registry_and_docs)
    assert "durability_batch_omits_accepted_event" in _codes(findings)


def test_eligibility_changes_during_an_open_window(base_records,
                                                   registry_and_docs):
    """WHEN a new eligibility-registry entry activates after the current UTC
    window opened THEN the current window continues using its bound version,
    content digest, activation checkpoint, and standing, and the new entry
    applies only when the next window opens."""
    findings = _validate(
        _with(base_records, "eligibility_activation_applied_to_open_window"),
        registry_and_docs)
    assert "eligibility_activation_applied_to_open_window" in _codes(findings)
    # the packaged windows all bind the entry effective at or before their open
    registry = _pick(base_records, "registry_id", "der-example-0001")
    active = next(e for e in registry["entries"] if e["standing"] == "active")
    for _, doc in base_records:
        snapshot = doc.get("eligibility_snapshot") or \
            (doc.get("terms") or {}).get("eligibility_snapshot")
        if not snapshot:
            continue
        window_open = doc.get("window_open") or doc["terms"]["window_open"]
        assert snapshot["entry_id"] == active["entry_id"]
        assert active["effective_interval"]["from_window_open"] <= window_open


def test_two_eligibility_entries_claim_the_same_boundary(base_records,
                                                         registry_and_docs):
    """WHEN zero entries or more than one entry with `standing == active` has an
    effective interval containing the UTC window boundary THEN window opening is
    REFUSED and no event is admitted under an ambiguous denominator."""
    findings = _validate(
        _with(base_records, "eligibility_boundary_selection_ambiguous"),
        registry_and_docs)
    assert "eligibility_boundary_selection_ambiguous" in _codes(findings)
    # zero is refused by the same code
    registry = _pick(base_records, "registry_id", "der-example-0001")
    for entry in registry["entries"]:
        entry["standing"] = "retired"
        entry["effective_interval"].setdefault("until_window_open",
                                               "2026-08-30T00:00:00Z")
    findings = _validate(_swap(base_records, "registry_id", "der-example-0001",
                               registry), registry_and_docs)
    assert "eligibility_boundary_selection_ambiguous" in _codes(findings)


def test_an_older_eligibility_version_is_offered_after_successor_activation(
        base_records, registry_and_docs):
    """WHEN a successor's activation checkpoint and effective interval cover the
    UTC window boundary but the runtime offers its retired predecessor THEN
    window opening is REFUSED as eligibility rollback."""
    findings = _validate(_with(base_records, "eligibility_snapshot_rolled_back"),
                         registry_and_docs)
    assert "eligibility_snapshot_rolled_back" in _codes(findings)


def test_eligibility_content_is_substituted_under_the_same_version(
        base_records, registry_and_docs):
    """WHEN an admission or manifest supplies registry contents whose digest
    differs from the snapshotted append-only registry entry THEN admission or
    closure is REFUSED before the batch root can be accepted."""
    findings = _validate(
        _with(base_records, "eligibility_terms_substituted_under_version"),
        registry_and_docs)
    assert "eligibility_terms_substituted_under_version" in _codes(findings)
    # closure is refused on the same ground: the manifest's own snapshot
    manifest = _pick(base_records, "manifest_id", "dbm-example-0001")
    manifest["terms"]["eligibility_snapshot"]["canonical_digest"]["value"] = \
        "sha256:" + "0" * 64
    _reseal_manifest(manifest)
    findings = _validate(_swap(base_records, "manifest_id", "dbm-example-0001",
                               manifest), registry_and_docs)
    assert "eligibility_terms_substituted_under_version" in _codes(findings)


def test_merkle_construction_profile_is_missing_or_substituted(
        base_records, registry_and_docs):
    """WHEN an admission or manifest omits the daily-Merkle profile id, version,
    or content digest, or the resolved profile bytes do not match that digest
    THEN admission or closure is REFUSED before any membership or completeness
    claim is accepted."""
    findings = _validate(_with(base_records, "merkle_profile_absent_or_substituted"),
                         registry_and_docs)
    assert "merkle_profile_absent_or_substituted" in _codes(findings)
    # substituted on the MANIFEST, which is the closure side of the same rule
    manifest = _pick(base_records, "manifest_id", "dbm-example-0003")
    manifest["terms"]["merkle_profile"]["canonical_digest"]["value"] = \
        "sha256:" + "1" * 64
    _reseal_manifest(manifest)
    findings = _validate(_swap(base_records, "manifest_id", "dbm-example-0003",
                               manifest), registry_and_docs)
    assert "merkle_profile_absent_or_substituted" in _codes(findings)


def test_independent_validator_recomputes_a_non_empty_root(base_records,
                                                           registry_and_docs):
    """WHEN a validator receives accepted event bytes, sequences, membership
    paths, and a manifest naming the released daily-Merkle profile THEN
    canonical leaf encoding, domain separation, ordering, tree shape, odd-node
    handling, and SHA-256 deterministically reproduce the manifest's
    `daily_batch_root` or verification is REFUSED."""
    construction = _pick(base_records, "profile_id",
                         "dmp-example-daily-merkle")["construction"]
    # the released construction really is resolvable and really reproduces
    assert construction["leaf_domain_separator"] != \
        construction["node_domain_separator"]
    assert construction["hash_algorithm"] == "sha256"
    manifest = _pick(base_records, "manifest_id", "dbm-example-0003")
    admissions = sorted(
        (doc for _, doc in base_records
         if doc.get("window_open") == manifest["terms"]["window_open"]
         and doc.get("admission_kind") == "new_leaf"),
        key=lambda a: a["leaf_sequence"])
    leaves = [a["event_leaf_digest"]["value"] for a in admissions]
    assert len(leaves) == 2
    assert reader._batch_root(construction, leaves) == \
        manifest["terms"]["daily_batch_root"]["value"]
    for index, admission in enumerate(admissions):
        recomputed = reader._membership_path(construction, leaves, index)
        supplied = [(e["position"], e["sibling_digest"]["value"])
                    for e in admission["membership_path"]]
        assert supplied == [(s["position"], s["value"]) for s in recomputed]
    # a root that does not reproduce is refused
    broken = copy.deepcopy(manifest)
    broken["terms"]["daily_batch_root"]["value"] = "sha256:" + "2" * 64
    _reseal_manifest(broken)
    findings = _validate(_swap(base_records, "manifest_id", "dbm-example-0003",
                               broken), registry_and_docs)
    assert "daily_batch_root_not_reproducible" in _codes(findings)


def test_an_intermediate_empty_day_is_omitted(base_records, registry_and_docs):
    """WHEN two or more consecutive empty windows share the deterministic empty
    `daily_batch_root` but an intermediate daily manifest is omitted THEN the
    later manifest's `previous_daily_anchored_digest` does not resolve to the
    immediately preceding item and continuity verification is REFUSED."""
    # drop the empty day entirely: the third day's link no longer resolves
    without_empty = [(label, copy.deepcopy(doc)) for label, doc in base_records
                     if not (isinstance(doc, dict)
                             and doc.get("manifest_id") == "dbm-example-0002")]
    findings = _validate(without_empty, registry_and_docs)
    assert "daily_continuity_link_unresolved" in _codes(findings)
    # and the gap between the surviving windows is refused in its own right
    findings = _validate(_with(base_records,
                               "empty_window_without_linked_checkpoint"),
                         registry_and_docs)
    assert "empty_window_without_linked_checkpoint" in _codes(findings)
    # the link is over the previous item's ANCHORED DIGEST and never its root
    findings = _validate(_with(base_records, "daily_continuity_link_over_batch_root"),
                         registry_and_docs)
    assert "daily_continuity_link_over_batch_root" in _codes(findings)
    # and the first manifest binds the contract-defined sentinel
    findings = _validate(
        _with(base_records, "first_daily_manifest_without_genesis_sentinel"),
        registry_and_docs)
    assert "first_daily_manifest_without_genesis_sentinel" in _codes(findings)


def test_an_anchoring_control_leaf_is_offered_as_a_source_event_in_its_own_batch(
        base_records, registry_and_docs):
    """WHEN a witness submission, confirmation, batch manifest, continuity
    checkpoint, or other anchoring-control leaf is offered as a
    durability-eligible event in the batch it produces THEN admission to that
    batch is REFUSED as recursive while the control leaf remains retained in the
    signed log/checkpoint path."""
    findings = _validate(
        _with(base_records, "anchoring_control_leaf_admitted_as_event"),
        registry_and_docs)
    assert "anchoring_control_leaf_admitted_as_event" in _codes(findings)
    # the control leaf is still RETAINED: the manifest keeps its continuity leaf
    manifest = _pick(base_records, "manifest_id", "dbm-example-0001")
    assert manifest["continuity_leaf_ref"]
    # and every conforming eligibility entry excludes the class from the count
    registry = _pick(base_records, "registry_id", "der-example-0001")
    for entry in registry["entries"]:
        assert "anchoring_control" in entry["terms"]["excluded_leaf_classes"]


def test_different_roots_are_proposed_for_the_two_configured_witnesses(
        base_records, registry_and_docs):
    """WHEN a realization proposes a rapid Kaspa aggregation root and a
    different OpenTimestamps aggregation root for the same configuration-bound
    daily item THEN the profile REFUSES the split and requires both witness
    commitment paths to begin at the same `aggregation_root ==
    anchored_digest`."""
    findings = _validate(_with(base_records, "daily_item_witness_roots_differ"),
                         registry_and_docs)
    assert "daily_item_witness_roots_differ" in _codes(findings)
    split = _pick(base_records, "receipt_id", "rcp-example-daily-0001")
    split["per_chain_anchors"][1]["commitment_derivation"][
        "source_aggregation_root"]["value"] = "sha256:" + "3" * 64
    findings = _validate(_swap(base_records, "receipt_id",
                               "rcp-example-daily-0001", split),
                         registry_and_docs)
    assert "daily_item_witness_roots_differ" in _codes(findings)
    assert "aggregation_root_not_identity_for_daily_item" in _codes(findings)


def test_a_witness_specific_commitment_path_is_omitted(base_records,
                                                       registry_and_docs):
    """WHEN a per-chain entry carries transaction and chain inclusion evidence
    but no proof that its transaction commitment derives from the same
    configuration-bound `aggregation_root` named by the receipt THEN that
    witness entry is REFUSED even when the transaction itself is canonically
    accepted."""
    findings = _validate(_with(base_records, "witness_commitment_path_absent"),
                         registry_and_docs)
    assert "witness_commitment_path_absent" in _codes(findings)
    # the fixture's transaction evidence is COMPLETE, which is the point
    entry = [doc for _, doc in _fixture("witness_commitment_path_absent")
             ][0]["per_chain_anchors"][0]
    assert entry["anchor_transaction_bytes"] and entry["inclusion_proof"] \
        and entry["block_header"] and entry["chain_acceptance_evidence"]
    # and a proof taken over the raw batch root is refused on its own ground
    findings = _validate(
        _with(base_records, "durability_witness_proof_over_raw_batch_root"),
        registry_and_docs)
    assert "durability_witness_proof_over_raw_batch_root" in _codes(findings)


def test_batch_root_or_mint_time_configuration_is_substituted(base_records,
                                                              registry_and_docs):
    """WHEN event membership proves one `daily_batch_root` but the manifest,
    previous daily anchored digest, close watermark, resolving log checkpoint,
    Merkle profile, material digest, witness set, horizon, timing input,
    confirmation-profile version, profile digest, activation checkpoint, or
    standing evidence differs from the values committed by `anchored_digest`
    THEN receipt verification REFUSES the item before evaluating either witness
    proof."""
    findings = _validate(
        _with(base_records, "daily_manifest_configuration_substituted"),
        registry_and_docs)
    assert "daily_manifest_configuration_substituted" in _codes(findings)
    # the receipt side: any edit inside the committed block breaks the digest
    edited = _pick(base_records, "receipt_id", "rcp-example-daily-0001")
    edited["mint_time_configuration"]["configured_witnesses"][0][
        "completion_horizon_seconds"] = 99999
    findings = _validate(_swap(base_records, "receipt_id",
                               "rcp-example-daily-0001", edited),
                         registry_and_docs)
    assert "receipt_configuration_block_edited" in _codes(findings)
    # including the confirmation-profile version, which lives in that block
    edited = _pick(base_records, "receipt_id", "rcp-example-daily-0001")
    edited["mint_time_configuration"]["configured_witnesses"][0][
        "confirmation_profile"]["version"] = 1
    findings = _validate(_swap(base_records, "receipt_id",
                               "rcp-example-daily-0001", edited),
                         registry_and_docs)
    assert "receipt_configuration_block_edited" in _codes(findings)
    # a close watermark no checkpoint covers is refused before the witnesses
    findings = _validate(_with(base_records, "durability_close_watermark_unproven"),
                         registry_and_docs)
    assert "durability_close_watermark_unproven" in _codes(findings)
    # and so are a reopened window, a selective batch and an open window
    # presented as anchored
    for code in ("durability_window_reopened_after_close",
                 "durability_event_selectivity_applied",
                 "open_window_presented_as_anchored",
                 "durability_window_not_fixed_utc_midnight",
                 "durability_window_selected_from_source_time",
                 "source_time_lateness_recorded_on_chain"):
        findings = _validate(_with(base_records, code), registry_and_docs)
        assert code in _codes(findings), code


# ======================================================================
# Requirement 3 — witness submission and confirmation remain distinct
# evidence states
# ======================================================================

def test_the_operational_interface_accepts_a_transaction_for_processing(
        base_records, registry_and_docs):
    """WHEN the declared interface accepts the serialized commitment transaction
    but configured chain acceptance or proof capture is incomplete THEN the
    per-witness state deterministically reports submitted while the overall item
    remains `anchor_pending`, and the receipt gains no confirmed entry.

    (The delta names Kaspa; this family names no chain, so the packaged records
    carry the OPERATIONAL and DURABILITY roles and the test reads them.)"""
    state = _pick(base_records, "state_id", "as-example-daily-0003")
    assert state["state"] == "anchor_pending"
    row = next(r for r in state["per_witness"] if r["chain_id"] == DUR)
    assert row["status"] == "submitted"
    assert row["submission_evidence"]["accepted_by_interface"] is True
    assert "confirmation_evidence" not in row
    receipt = _pick(base_records, "receipt_id", "rcp-example-daily-0003")
    assert {e["chain_id"] for e in receipt["per_chain_anchors"]} == {OP}
    assert not _validate(base_records, registry_and_docs).errors


def test_operational_confirmation_evidence_becomes_complete(base_records,
                                                            registry_and_docs):
    """WHEN the configured acceptance rule passes and transaction bytes,
    inclusion proof, block header, and chain-acceptance evidence are captured
    whole THEN the completed entry is appended to the receipt without replacing
    its prior submitted state."""
    state = _pick(base_records, "state_id", "as-example-daily-0001")
    row = next(r for r in state["per_witness"] if r["chain_id"] == OP)
    assert row["status"] == "confirmed"
    assert row["confirmation_evidence"]["chain_acceptance_rule_passed"] is True
    assert set(row["confirmation_evidence"]["retained_proof_material"]) == {
        "transaction_bytes", "inclusion_proof", "block_header",
        "chain_acceptance_evidence"}
    # the SUBMITTED transition is still on the record beside the confirmation
    kinds = [t["transition"] for t in state["transitions"]]
    assert kinds.count("witness_submission") == 2
    assert kinds.count("witness_confirmation") == 2
    receipt = _pick(base_records, "receipt_id", "rcp-example-daily-0001")
    entry = next(e for e in receipt["per_chain_anchors"] if e["chain_id"] == OP)
    assert entry["anchor_transaction_bytes"] and entry["inclusion_proof"] \
        and entry["block_header"] and entry["chain_acceptance_evidence"]
    assert not _validate(base_records, registry_and_docs).errors


def test_schema_authoring_starts_without_approved_confirmation_profiles(
        base_records, registry_and_docs):
    """WHEN either configured network lacks a versioned operator-approved
    profile, approval record, transition vectors, or objective confirmation
    evidence THEN chain-anchoring schema and validator authoring is BLOCKED and
    no implementation-selected threshold is accepted.

    THE BLOCK IS MECHANICAL RATHER THAN A PROMISE. This realization builds the
    VESSEL an operator's approval is published into; what it refuses is a
    register that reports a configured network with no active entry, a profile
    approved by anyone but the operator, a profile with only one transition
    direction, and a numeric depth with nothing cited behind it."""
    for code in ("confirmation_profile_unresolved",
                 "confirmation_profile_not_operator_approved",
                 "confirmation_profile_numeric_depth_uncited",
                 "profile-transition-vectors-incomplete"):
        findings = _validate(_with(base_records, code), registry_and_docs)
        assert code in _codes(findings), code
    # the packaged profiles name no depth at all, which is the delta's own line
    for _, doc in base_records:
        confirmed = (doc.get("terms") or {}).get("confirmed_condition")
        if confirmed:
            assert "numeric_depth" not in confirmed
            assert confirmed["chain_acceptance_rule_citation"]


def test_a_submitted_proof_is_below_its_approved_confirmation_condition(
        base_records, registry_and_docs):
    """WHEN network submission evidence exists but the referenced profile's
    objective confirmation condition or retained-proof requirement is not
    satisfied THEN the witness deterministically remains `submitted`; `pending`
    is reserved for a witness with no accepted submission evidence, and the
    validator REFUSES confirmed state."""
    findings = _validate(
        _with(base_records, "witness_confirmed_without_profile_condition"),
        registry_and_docs)
    assert "witness_confirmed_without_profile_condition" in _codes(findings)
    # the retained-proof half of the same condition
    state = _pick(base_records, "state_id", "as-example-daily-0001")
    row = next(r for r in state["per_witness"] if r["chain_id"] == DUR)
    row["confirmation_evidence"]["retained_proof_material"] = ["transaction_bytes"]
    findings = _validate(_swap(base_records, "state_id",
                               "as-example-daily-0001", state),
                         registry_and_docs)
    assert "witness_confirmed_without_profile_condition" in _codes(findings)
    # and `pending` is RESERVED
    findings = _validate(_with(base_records,
                               "witness_pending_with_submission_evidence"),
                         registry_and_docs)
    assert "witness_pending_with_submission_evidence" in _codes(findings)


def test_a_profile_handles_a_reorganization_or_replacement(base_records,
                                                           registry_and_docs):
    """WHEN a previously observed transaction or block is reorganized, replaced,
    or no longer satisfies the referenced profile THEN the profile's declared
    transition rule determines the witness state, the change is written as
    evidence, and a stale confirmed label is not retained by assertion."""
    # both rules are declared, in the direction that writes evidence
    for _, doc in base_records:
        terms = doc.get("terms") or {}
        if "reorganization_rule" not in terms:
            continue
        for key in ("reorganization_rule", "replacement_rule"):
            assert terms[key]["on_change"] == "rewrite_state_as_evidence"
            assert terms[key]["evidence_written"] is True
    # a state that keeps the label anyway is refused
    findings = _validate(
        _with(base_records, "reorganized_witness_retains_confirmed_label"),
        registry_and_docs)
    assert "reorganized_witness_retains_confirmed_label" in _codes(findings)
    # the honest record — the state moved and the move was written — validates
    state = _pick(base_records, "state_id", "as-example-daily-0001")
    row = next(r for r in state["per_witness"] if r["chain_id"] == OP)
    row["status"] = "invalid"
    row.pop("confirmation_evidence")
    row["observation_change"] = {
        "change_kind": "reorganization", "evidence_written": True,
        "state_after": "invalid",
        "leaf_ref": "leaf-scenario-reorg-0001",
        "observed_at": "2026-09-01T00:00:00Z"}
    state["state"] = "anchor_pending"
    state["transitions"] = [t for t in state["transitions"]
                            if t["transition"] != "completion"]
    state.pop("receipt_ref", None)
    state["long_horizon_claim_admitted"] = False
    findings = _validate(_swap(base_records, "state_id",
                               "as-example-daily-0001", state),
                         registry_and_docs)
    assert "reorganized_witness_retains_confirmed_label" not in _codes(findings)


def test_an_operator_approves_a_new_profile_version(base_records,
                                                    registry_and_docs):
    """WHEN confirmation policy changes after receipts already exist THEN the
    registry appends the new content digest and a future UTC-window activation
    checkpoint, the current open window retains its snapshot, later windows use
    the new version, and prior receipts retain their immutable as-of result
    while current verification reports current standing."""
    registry = _pick(base_records, "registry_id", "cpr-example-0001")
    entries = [e for e in registry["entries"] if e["chain_id"] == OP]
    assert [e["version"] for e in entries] == [1, 2]
    older, newer = entries
    # appended, not edited: the predecessor stands, retired, with its interval
    # closed in the same act
    assert older["standing"] == "retired"
    assert older["effective_interval"]["until_window_open"] == \
        newer["effective_interval"]["from_window_open"]
    assert newer["predecessor_entry_id"] == older["entry_id"]
    assert newer["activation"]["log_sequence"] > older["activation"]["log_sequence"]
    assert older["canonical_digest"]["value"] != newer["canonical_digest"]["value"]
    # exactly one active entry per configured network at the boundary
    for chain in registry["configured_networks"]:
        active = [e for e in registry["entries"]
                  if e["chain_id"] == chain and e["standing"] == "active"]
        assert len(active) == 1
    assert not _validate(base_records, registry_and_docs).errors


def test_a_minter_rolls_back_after_a_newer_profile_activates(base_records,
                                                             registry_and_docs):
    """WHEN a UTC window opens after a new profile activation checkpoint but its
    snapshot selects an older profile version THEN minting is REFUSED before
    witness submission even if the older version was once approved."""
    findings = _validate(_with(base_records,
                               "confirmation_profile_snapshot_rolled_back"),
                         registry_and_docs)
    assert "confirmation_profile_snapshot_rolled_back" in _codes(findings)


def test_a_profile_activates_during_an_open_window(base_records,
                                                   registry_and_docs):
    """WHEN a new confirmation-profile version activates after a UTC window has
    opened and before its daily item closes THEN every event and the final item
    retain the window-open profile snapshot, and the new version applies only to
    the next window."""
    findings = _validate(
        _with(base_records,
              "confirmation_profile_activation_applied_to_open_window"),
        registry_and_docs)
    assert "confirmation_profile_activation_applied_to_open_window" in \
        _codes(findings)
    # every packaged daily item's snapshot is effective at or before its own
    # window open, which is the rule holding rather than being asserted
    registry = _pick(base_records, "registry_id", "cpr-example-0001")
    by_key = {(e["chain_id"], e["profile_id"], e["version"]): e
              for e in registry["entries"]}
    manifests = {doc["manifest_id"]: doc for _, doc in base_records
                 if isinstance(doc, dict) and "manifest_id" in doc}
    for _, doc in base_records:
        ref = (doc.get("daily_item") or {}).get("manifest_ref")
        if ref is None or ref not in manifests:
            continue
        window_open = manifests[ref]["terms"]["window_open"]
        for witness in doc["mint_time_configuration"]["configured_witnesses"]:
            snap = witness["confirmation_profile"]
            entry = by_key[(snap["chain_id"], snap["profile_id"], snap["version"])]
            assert entry["effective_interval"]["from_window_open"] <= window_open


def test_profile_content_is_substituted_under_an_approved_id_and_version(
        base_records, registry_and_docs):
    """WHEN the supplied profile content digest differs from the append-only
    registry entry committed by the anchored digest THEN verification REFUSES
    the receipt and does not evaluate the substituted confirmation rule."""
    findings = _validate(
        _with(base_records, "confirmation_profile_terms_substituted_under_version"),
        registry_and_docs)
    assert "confirmation_profile_terms_substituted_under_version" in _codes(findings)
    # substituted on the RECEIPT's committed snapshot
    receipt = _pick(base_records, "receipt_id", "rcp-example-daily-0001")
    receipt["mint_time_configuration"]["configured_witnesses"][0][
        "confirmation_profile"]["canonical_digest"]["value"] = "sha256:" + "4" * 64
    _reseal_receipt(receipt)
    findings = _validate(_swap(base_records, "receipt_id",
                               "rcp-example-daily-0001", receipt),
                         registry_and_docs)
    assert "confirmation_profile_terms_substituted_under_version" in _codes(findings)


def test_a_profile_is_retired_or_compromised_after_historical_confirmation(
        base_records, registry_and_docs):
    """WHEN a historical receipt proved confirmation under its then-active
    profile but current registry standing is `retired` or `compromised` THEN the
    historical as-of evidence remains immutable, current verification reports
    `profile_retired` or `profile_compromised`, and no new long-horizon claim is
    admitted from that profile."""
    # minting a NEW receipt under a withdrawn version is refused
    findings = _validate(
        _with(base_records,
              "confirmation_profile_retired_or_compromised_mints_receipt"),
        registry_and_docs)
    assert "confirmation_profile_retired_or_compromised_mints_receipt" in \
        _codes(findings)
    # and the historical as-of token may not be rewritten by current standing
    findings = _validate(
        _with(base_records,
              "confirmation_profile_standing_rewrites_historical_receipt"),
        registry_and_docs)
    assert "confirmation_profile_standing_rewrites_historical_receipt" in \
        _codes(findings)
    # a CURRENT verification over a retired profile reports it and admits no
    # new claim — the accepting half of the same rule
    registry = _pick(base_records, "registry_id", "cpr-example-0001")
    entry = next(e for e in registry["entries"] if e["chain_id"] == DUR)
    result = {
        "schema_version": 1,
        "kind": "xfactory_chain_anchoring_verification_result",
        "result_id": "vr-scenario-retired-0001",
        "subject_ref": "dbm-example-0001",
        "verification_mode": "receipt_only",
        "status": "anchor_complete",
        "receipt_ref": "rcp-example-daily-0001",
        "confirmation_profiles_evaluated_under": [{
            "witness_id": "w-example-dur-0001",
            "chain_id": DUR,
            "profile_id": entry["profile_id"],
            "version": entry["version"],
            "canonical_digest": entry["canonical_digest"],
            "as_of_token": (f"confirmed_under_v{entry['version']}_at_"
                            f"{entry['activation']['checkpoint_ref']}"),
            "current_standing": "profile_retired",
            "new_claim_admitted": False,
        }],
    }
    entry["standing"] = "retired"
    entry["effective_interval"]["until_window_open"] = "2026-09-10T00:00:00Z"
    entry["standing_changed_at"] = "2026-09-10T00:00:00Z"
    scope = _swap(base_records, "registry_id", "cpr-example-0001", registry)
    findings = _validate(scope + [("scenario/result", result)], registry_and_docs)
    assert "confirmation_profile_standing_rewrites_historical_receipt" not in \
        _codes(findings)
    # while a NEW claim from the same retired profile is refused
    claimed = copy.deepcopy(result)
    claimed["result_id"] = "vr-scenario-retired-0002"
    claimed["confirmation_profiles_evaluated_under"][0]["new_claim_admitted"] = True
    findings = _validate(scope + [("scenario/claim", claimed)], registry_and_docs)
    assert "confirmation_profile_retired_or_compromised_mints_receipt" in \
        _codes(findings)
    # AND THE ROW IS KEYED BY WITNESS, NOT BY CHAIN (Copilot round 1). The
    # committed set carries no uniqueness constraint on `chain_id`, so a row
    # naming a witness the referenced receipt does not configure names a rule
    # nobody applied — and it is refused rather than resolved by guessing.
    stranger = copy.deepcopy(result)
    stranger["result_id"] = "vr-scenario-retired-0003"
    stranger["confirmation_profiles_evaluated_under"][0]["witness_id"] = \
        "w-example-not-configured-0001"
    findings = _validate(scope + [("scenario/stranger", stranger)],
                         registry_and_docs)
    assert "witness_confirmed_without_named_profile" in _codes(findings)


def test_two_witnesses_are_configured_against_one_chain(registry_and_docs):
    """Copilot round 2: the SAME anti-pattern round 1 fixed on the
    verification-result side lived one section earlier, on the receipt's own
    committed snapshot. `check_confirmation_bindings` indexed each receipt's
    `configured_witnesses` snapshots by `chain_id`
    (`snapshots[chain] = snapshot`) — but `configured_witnesses` carries no
    uniqueness constraint on `chain_id`, and the per-chain entry's own
    `witness_id` exists for exactly that reason, so a realization running two
    DIFFERENT witnesses against ONE chain silently let the second witness's
    snapshot overwrite the first's. A `per_chain_anchors` entry that named the
    profile it was ACTUALLY confirmed under, for its OWN witness, was then
    compared against the WRONG witness's snapshot and refused for a defect
    that never happened."""
    receipt = copy.deepcopy(reader.labelled(
        "scenario",
        EXAMPLES / "anchor-receipt-1-both-witnesses-landed.example.yaml")[0][1])
    witnesses = receipt["mint_time_configuration"]["configured_witnesses"]
    # collapse the operational witness onto the durability witness's chain:
    # two different witnesses, two different committed profiles, one chain
    witnesses[0]["chain_id"] = DUR
    witnesses[0]["confirmation_profile"]["chain_id"] = DUR
    receipt["per_chain_anchors"][0]["chain_id"] = DUR
    receipt["anchored_digest"]["value"] = canonical.digest(
        {"material_digest": receipt["material_digest"],
         "mint_time_configuration": receipt["mint_time_configuration"]})
    findings = _validate([("scenario/two-witnesses-one-chain", receipt)],
                         registry_and_docs)
    # a chain-keyed index compares per_chain_anchors[0] (witness
    # w-example-op-0001) against witness w-example-dur-0001's snapshot and
    # refuses a receipt that committed nothing wrong; keyed by witness, both
    # entries match their OWN witness's snapshot and nothing is refused
    assert not findings.errors


def test_a_durability_proof_is_submitted_but_not_upgraded(base_records,
                                                          registry_and_docs):
    """WHEN the daily item has a retained detached timestamp proof from its
    configuration-bound `aggregation_root == anchored_digest` but no
    independently verified inclusion evidence THEN the anchor-state record
    reports the aggregation submission and the chain layer pending, and no
    long-horizon durability claim is admitted."""
    state = _pick(base_records, "state_id", "as-example-daily-0003")
    row = next(r for r in state["per_witness"] if r["chain_id"] == DUR)
    assert row["status"] == "submitted"
    assert row["upgrade_stage"] == {"aggregation_submission": "submitted",
                                    "chain_confirmation": "pending"}
    assert row["submission_evidence"]["evidence_kinds"] == \
        ["retained_detached_timestamp_proof"]
    assert row["pending_durability_proof"]["awaiting_upgrade"] is True
    assert row["pending_durability_proof"]["reanchored"] is False
    assert state["long_horizon_claim_admitted"] is False
    assert not _validate(base_records, registry_and_docs).errors
    # the receipt carries NO entry for it, rather than a half-filled one
    receipt = _pick(base_records, "receipt_id", "rcp-example-daily-0003")
    assert DUR not in {e["chain_id"] for e in receipt["per_chain_anchors"]}


def test_the_durability_upgrade_verifies(base_records, registry_and_docs):
    """WHEN the detached proof is upgraded with complete transaction, inclusion,
    header, and chain-acceptance evidence that satisfies the configured rules
    THEN the completed durability entry is appended to the same receipt and
    confirmed becomes available without re-anchoring the item."""
    state = _pick(base_records, "state_id", "as-example-daily-0001")
    row = next(r for r in state["per_witness"] if r["chain_id"] == DUR)
    assert row["upgrade_stage"]["chain_confirmation"] == "confirmed"
    assert "upgraded_timestamp_proof" in \
        row["confirmation_evidence"]["retained_proof_material"]
    receipt = _pick(base_records, "receipt_id", "rcp-example-daily-0001")
    entry = next(e for e in receipt["per_chain_anchors"] if e["chain_id"] == DUR)
    # appended against the SAME anchored digest, not a second anchor
    assert entry["commitment_derivation"]["source_aggregation_root"]["value"] == \
        receipt["anchored_digest"]["value"]
    assert not _validate(base_records, registry_and_docs).errors
    # re-anchoring instead of upgrading is refused, and so is erasing the
    # transitions the upgrade came through
    findings = _validate(
        _with(base_records, "state_transition_history_erased_on_upgrade"),
        registry_and_docs)
    assert "state_transition_history_erased_on_upgrade" in _codes(findings)
    reanchored = _pick(base_records, "state_id", "as-example-daily-0003")
    row = next(r for r in reanchored["per_witness"] if r["chain_id"] == DUR)
    row["pending_durability_proof"]["reanchored"] = True
    findings = _validate(_swap(base_records, "state_id",
                               "as-example-daily-0003", reanchored),
                         registry_and_docs)
    assert "durability_proof_reanchored_rather_than_upgraded" in _codes(findings)


def test_pending_evidence_is_offered_as_confirmed(base_records,
                                                  registry_and_docs):
    """WHEN a consumer presents interface acceptance, a detached timestamp
    proof, a transaction identifier, or a prior status label as confirmed
    witness evidence THEN verification REFUSES confirmation and reports the
    actual submitted, pending, invalid, or unevaluable state."""
    findings = _validate(_with(base_records,
                               "submission_evidence_offered_as_confirmed"),
                         registry_and_docs)
    assert "submission_evidence_offered_as_confirmed" in _codes(findings)
    # the vocabulary really carries all four reportable answers
    definitions = yaml.safe_load(
        (CONTRACT_DIR / "anchoring-definitions.schema.yaml").read_text())
    assert definitions["$defs"]["witness_evidence_state"]["enum"] == [
        "pending", "submitted", "confirmed", "invalid", "unevaluable",
        "terminally_failed"]
    # a completeness answer that names no profile is refused too
    findings = _validate(_with(base_records, "witness_confirmed_without_named_profile"),
                         registry_and_docs)
    assert "witness_confirmed_without_named_profile" in _codes(findings)
    unnamed = {
        "schema_version": 1,
        "kind": "xfactory_chain_anchoring_verification_result",
        "result_id": "vr-scenario-unnamed-0001",
        "subject_ref": "dbm-example-0001",
        "verification_mode": "receipt_only",
        "status": "anchor_complete",
    }
    # and a row that names a profile the committed block did not snapshot FOR
    # THAT WITNESS is refused too, which is the other half of "named"
    registry = _pick(base_records, "registry_id", "cpr-example-0001")
    older = next(e for e in registry["entries"]
                 if e["chain_id"] == OP and e["version"] == 1)
    mismatched = {
        "schema_version": 1,
        "kind": "xfactory_chain_anchoring_verification_result",
        "result_id": "vr-scenario-mismatched-0001",
        "subject_ref": "dbm-example-0001",
        "verification_mode": "receipt_only",
        "status": "anchor_complete",
        "receipt_ref": "rcp-example-daily-0001",
        "confirmation_profiles_evaluated_under": [{
            "witness_id": "w-example-op-0001",
            "chain_id": OP,
            "profile_id": older["profile_id"],
            "version": older["version"],
            "canonical_digest": older["canonical_digest"],
            "as_of_token": (f"confirmed_under_v{older['version']}_at_"
                            f"{older['activation']['checkpoint_ref']}"),
            "current_standing": "profile_retired",
        }],
    }
    findings = _validate(list(base_records) + [("scenario/mismatched", mismatched)],
                         registry_and_docs)
    assert "witness_confirmed_without_named_profile" in _codes(findings)
    findings = _validate(list(base_records) + [("scenario/unnamed", unnamed)],
                         registry_and_docs)
    assert "witness_confirmed_without_named_profile" in _codes(findings)


def test_the_operational_witness_alone_is_offered_for_a_long_horizon_claim(
        base_records, registry_and_docs):
    """WHEN a consumer makes a long-horizon durability claim from valid
    operational evidence while the durability witness remains pending or
    unevaluable THEN the claim is REFUSED while the valid operational witness
    result remains independently reportable."""
    findings = _validate(
        _with(base_records, "long_horizon_claim_on_unupgraded_durability_proof"),
        registry_and_docs)
    assert "long_horizon_claim_on_unupgraded_durability_proof" in _codes(findings)
    # the operational result stays reportable: the same record keeps its
    # confirmed operational row and its receipt entry
    fixture = [doc for _, doc in
               _fixture("long_horizon_claim_on_unupgraded_durability_proof")][0]
    operational = next(r for r in fixture["per_witness"] if r["chain_id"] == OP)
    assert operational["status"] == "confirmed"
    # and the claim IS admitted where the chain layer is confirmed
    assert _pick(base_records, "state_id",
                 "as-example-daily-0001")["long_horizon_claim_admitted"] is True
