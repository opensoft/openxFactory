"""Stage-1 pre-filter unit tests (add-neutrality-drift-lane task 1.5).

One planted fixture per signal class under fixtures/neutrality/: a
neutral-shaped schema with zero domain terms (lexicon_absence), a
near-duplicate of a fixture openxFactory file (near_duplicate), an
uninventoried scripts/ tree that another repo references
(uninventoried_tooling + cross_repo_consumer), plus a properly
domain-flavored schema that must NOT trigger, a frozen archived record
that must never be a subject, and a register-cited path that must be
skipped rather than re-filed.
"""

from __future__ import annotations

import json

from conftest import FIXTURES  # noqa: F401  (sys.path side effect)

from doc_health import neutrality

WORKSPACE = FIXTURES / "neutrality"
OPENX = WORKSPACE / "openxFactory"
MEDX = WORKSPACE / "xFactories" / "MedxFactory"
OPSX = WORKSPACE / "xFactories" / "OpsxFactory"

PLANTED_SCHEMA = "schemas/generic-envelope.schema.yaml"
DOMAIN_SCHEMA = "schemas/patient-intake.schema.yaml"
NEAR_DUP = "contracts/copy-of-neutral.yaml"
UNINVENTORIED = "scripts/tools/check-things.py"
CITED = "scripts/legacy/cited-tool.py"


def scan_medx():
    index = neutrality.build_neutral_index(OPENX)
    refs = neutrality.collect_path_references(
        {"openxFactory": OPENX, "MedxFactory": MEDX, "OpsxFactory": OPSX})
    register_text = (OPENX / "docs" /
                     "domain-neutralization-candidate-register.md"
                     ).read_text(encoding="utf-8")
    return neutrality.scan_repo("MedxFactory", MEDX, index,
                                register_text=register_text,
                                consumer_refs=refs)


def by_path(result):
    return {c.path: c for c in result.candidates}


def signal_names(candidate):
    return {s.name for s in candidate.signals}


# --- lexicon derivation --------------------------------------------------------


def test_lexicon_derives_from_name_stack_and_ontology():
    lexicon = neutrality.derive_lexicon("MedxFactory", MEDX)
    assert "medx" in lexicon.stems
    assert "medxfactory" in lexicon.stems
    assert "medical" in lexicon.stems  # stack.yaml domain.category
    assert "patient" in lexicon.terms  # ontology label
    assert "care plan" in lexicon.terms
    assert "ontology" in lexicon.source_note
    assert "hermes/domain/ontology/concepts.yaml" in lexicon.source_note


def test_lexicon_falls_back_to_name_stems_and_says_so():
    lexicon = neutrality.derive_lexicon("OpsxFactory", OPSX)
    assert "opsx" in lexicon.stems
    assert lexicon.terms == ()
    assert "name stems only" in lexicon.source_note
    assert "no domain ontology" in lexicon.source_note


def test_lexicon_matching_stems_substring_terms_word_boundary():
    lexicon = neutrality.Lexicon(stems=("medx",), terms=("care plan",),
                                 source_note="test")
    assert not neutrality.zero_lexicon_hits("uses MedxFactory rules", lexicon)
    assert not neutrality.zero_lexicon_hits("the Care  Plan step", lexicon)
    # 'plan' alone is not the phrase; unrelated text has zero hits
    assert neutrality.zero_lexicon_hits("a plan for queue retries", lexicon)


# --- per-signal detection --------------------------------------------------------


def test_planted_neutral_schema_trips_lexicon_absence():
    candidate = by_path(scan_medx())[PLANTED_SCHEMA]
    assert "lexicon_absence" in signal_names(candidate)
    note = next(s.note for s in candidate.signals
                if s.name == "lexicon_absence")
    assert "lexicon:" in note  # the sourcing note rides every signal


def test_domain_flavored_schema_does_not_trigger():
    assert DOMAIN_SCHEMA not in by_path(scan_medx())


def test_near_duplicate_of_openxfactory_file_trips():
    candidate = by_path(scan_medx())[NEAR_DUP]
    assert signal_names(candidate) == {"near_duplicate"}
    note = candidate.signals[0].note
    assert "contracts/schemas/xfactory-sample-envelope.schema.yaml" in note
    assert str(neutrality.NEAR_DUPLICATE_SIMILARITY) in note


def test_uninventoried_scripts_tree_trips_with_consumer():
    candidate = by_path(scan_medx())[UNINVENTORIED]
    names = signal_names(candidate)
    assert "uninventoried_tooling" in names
    assert "cross_repo_consumer" in names
    assert "lexicon_absence" in names
    consumer_note = next(s.note for s in candidate.signals
                         if s.name == "cross_repo_consumer")
    assert "OpsxFactory" in consumer_note


def test_inventoried_domain_flavored_script_does_not_trigger():
    assert "scripts/inventory-listed.py" not in by_path(scan_medx())


def test_frozen_records_are_excluded_subjects():
    result = scan_medx()
    assert not any(c.path.startswith("openspec/changes/archive/")
                   for c in result.candidates)


def test_register_cited_path_is_skipped_not_refiled():
    result = scan_medx()
    assert CITED not in by_path(result)
    assert result.register_cited_skipped == 1


def test_scan_is_deterministic_and_counts_signals():
    first, second = scan_medx(), scan_medx()
    assert [c.path for c in first.candidates] == \
        [c.path for c in second.candidates]
    assert [c.content_sha256 for c in first.candidates] == \
        [c.content_sha256 for c in second.candidates]
    assert first.signal_counts["near_duplicate"] == 1
    assert first.signal_counts["lexicon_absence"] == 2
    assert first.signal_counts["cross_repo_consumer"] == 1
    assert first.signal_counts["uninventoried_tooling"] == 1
    assert sorted(by_path(first)) == [NEAR_DUP, PLANTED_SCHEMA,
                                      UNINVENTORIED]


# --- incremental state, baseline marker, selection --------------------------------


def test_state_roundtrip_and_missing_state_is_empty(tmp_path):
    assert neutrality.load_state(tmp_path) == {}
    repos = {"MedxFactory": {"last_run_commit": "a" * 40,
                             "judged": {PLANTED_SCHEMA: "b" * 64}}}
    path = neutrality.record_state(tmp_path, repos)
    assert path == tmp_path / "health" / "neutrality-drift" / "state.yaml"
    assert neutrality.load_state(tmp_path) == repos
    document = json.loads(path.read_text(encoding="utf-8"))
    assert document["kind"] == neutrality.STATE_KIND


def test_baseline_marker_is_an_immutable_record(tmp_path):
    assert neutrality.load_baseline(tmp_path, "codexFactory") is None
    path = neutrality.record_baseline(
        tmp_path, "codexFactory", "c" * 40,
        evidence="2026-08-03 manual sweep", as_of="2026-08-03")
    marker = neutrality.load_baseline(tmp_path, "codexFactory")
    assert marker["kind"] == neutrality.BASELINE_KIND
    assert marker["status"] == "record"
    assert marker["commit"] == "c" * 40
    # exclusive write: a recorded baseline is never rewritten
    import pytest
    from doc_health.catalog import CatalogError
    with pytest.raises(CatalogError):
        neutrality.record_baseline(tmp_path, "codexFactory", "d" * 40,
                                   evidence="second", as_of="2026-08-04")
    assert path.is_file()


def test_baseline_path_rejects_traversal():
    import pytest
    with pytest.raises(ValueError):
        neutrality.baseline_path("/tmp", "../escape")


def _selection(**kwargs):
    result = scan_medx()
    defaults = dict(state={}, baselines={}, changed_paths={},
                    suppressions={}, budget=8)
    defaults.update(kwargs)
    return result, neutrality.select_for_review([result], **defaults)


def test_selection_takes_everything_on_first_run_bounded_by_budget():
    result, selection = _selection()
    assert selection.selected == 3
    assert [c.path for c in selection.subjects] == \
        sorted(c.path for c in result.candidates)
    assert selection.carried_over == 0
    _, bounded = _selection(budget=2)
    assert len(bounded.subjects) == 2
    assert bounded.carried_over == 1


def test_selection_skips_judged_unchanged_and_requeues_changed():
    result = scan_medx()
    digests = {c.path: c.content_sha256 for c in result.candidates}
    state = {"MedxFactory": {"judged": dict(digests)}}
    selection = neutrality.select_for_review(
        [result], state=state, baselines={}, changed_paths={},
        suppressions={}, budget=8)
    assert selection.subjects == [] and selection.selected == 0
    # a changed digest re-queues exactly that path
    state["MedxFactory"]["judged"][PLANTED_SCHEMA] = "0" * 64
    selection = neutrality.select_for_review(
        [result], state=state, baselines={}, changed_paths={},
        suppressions={}, budget=8)
    assert [c.path for c in selection.subjects] == [PLANTED_SCHEMA]


def test_baseline_marker_skips_unchanged_paths_only():
    result = scan_medx()
    baselines = {"MedxFactory": {"commit": "c" * 40}}
    changed = {"MedxFactory": frozenset({PLANTED_SCHEMA})}
    selection = neutrality.select_for_review(
        [result], state={}, baselines=baselines, changed_paths=changed,
        suppressions={}, budget=8)
    assert [c.path for c in selection.subjects] == [PLANTED_SCHEMA]
    assert selection.baseline_skipped == 2
    # unknown change window (git unavailable): fail open into review
    selection = neutrality.select_for_review(
        [result], state={}, baselines=baselines,
        changed_paths={"MedxFactory": None}, suppressions={}, budget=8)
    assert selection.selected == 3


def test_baseline_repo_full_sweep_ignores_the_marker():
    result = scan_medx()
    baselines = {"MedxFactory": {"commit": "c" * 40}}
    selection = neutrality.select_for_review(
        [result], state={}, baselines=baselines,
        changed_paths={"MedxFactory": frozenset()}, suppressions={},
        budget=8, baseline_repo="MedxFactory")
    assert selection.selected == 3


# --- disposition suppression keyed (repo, path, content digest) ---------------------


def test_disposition_suppression_holds_only_while_content_unchanged():
    result = scan_medx()
    planted = by_path(result)[PLANTED_SCHEMA]
    entries = [
        {"family": "neutrality-drift", "repo": "MedxFactory",
         "path": PLANTED_SCHEMA,
         "content_sha256": planted.content_sha256,
         "cite": "Brett 2026-08-04: not-now"},
        {"family": "location-conformance", "repo": "MedxFactory",
         "path": "other.md", "cite": "unrelated family entry"},
        {"family": "neutrality-drift", "repo": "MedxFactory",
         "path": NEAR_DUP, "content_sha256": "f" * 64},  # no cite: inert
    ]
    suppressions = neutrality.disposition_suppressions(entries)
    assert neutrality.is_suppressed(planted, suppressions)
    selection = neutrality.select_for_review(
        [result], state={}, baselines={}, changed_paths={},
        suppressions=suppressions, budget=8)
    assert PLANTED_SCHEMA not in [c.path for c in selection.subjects]
    assert selection.suppressed == 1
    # changed content: same path, new digest -> re-filed
    changed = neutrality.Candidate(
        repo="MedxFactory", path=PLANTED_SCHEMA,
        content_sha256="1" * 64, signals=planted.signals)
    assert not neutrality.is_suppressed(changed, suppressions)


def test_changed_paths_since_returns_none_without_git(tmp_path):
    assert neutrality.changed_paths_since(tmp_path, "a" * 40) is None
