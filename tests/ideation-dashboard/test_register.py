"""The cross-reference index adapter reads the landed `ideation-cross-reference`
index (topic entries + embedded possibles register) READ-ONLY, and the project
register adapter reads the workspace hierarchy — both from the fixture corpus
(plan "register.py")."""

from __future__ import annotations

import textwrap

from conftest import BASE_REPO  # noqa: F401  (sys.path side effect)

from ideation_dashboard.register import (
    POSSIBLES_REGISTER_KEY, TOPIC_ENTRIES_KEY,
    CrossReferenceIndexAdapter, ProjectRegisterAdapter,
)


# ---- possibles register (embedded in the cross-reference index) ----

def test_possibles_discovered_from_repo_root():
    ids = [e["id"] for e in CrossReferenceIndexAdapter.discover(BASE_REPO).possibles()]
    # The five worked-example possibles, nothing fabricated for legacy docs.
    assert set(ids) == {
        "pos-health-sweep", "pos-ideation-governance",
        "pos-avatar-lab", "pos-avatar-inline", "pos-dtn-autopromote",
    }


def test_possibles_preserve_states_and_edges():
    by_id = CrossReferenceIndexAdapter.discover(BASE_REPO).possibles_by_id()
    # multi-cluster possible
    assert by_id["pos-health-sweep"]["claiming_clusters"] == \
        ["cl-doc-health", "cl-ideation-governance"]
    # pick-edge inheritance
    assert by_id["pos-ideation-governance"]["pick"] == \
        {"staging_id": "ideation-governance", "change_id": "add-ideation-governance"}
    # cited rejection carries reason + citation
    rej = by_id["pos-dtn-autopromote"]
    assert rej["state"] == "rejected" and rej["reason"] and rej["citation"]
    # option set
    assert by_id["pos-avatar-inline"]["option_set"]["id"] == "os-avatar-shape"


# ---- topic entries (the landed index shape: names + readiness) ----

def test_topic_entries_carry_names_and_readiness():
    by_id = CrossReferenceIndexAdapter.discover(BASE_REPO).topic_entry_by_id()
    assert by_id["cl-avatar"]["name"] == "Avatar Client Lab"
    assert by_id["cl-doc-health"]["name"] == "Doc Health"
    # a scored panel carries integer tier scores...
    scored = {t["tier"]: t.get("score") for t in by_id["cl-doc-health"]["readiness"]["tiers"]}
    assert scored == {"domain": 9, "company": 8, "project": 8}
    # ...an unscored panel carries no score, only an unscored_reason
    unscored = by_id["cl-ideation-governance"]["readiness"]["tiers"]
    assert all("score" not in t and t["unscored_reason"] for t in unscored)


def test_landed_keys_are_the_read_seam():
    # The seam is closed: both top-level fields are read directly under their
    # realized names (no key override).
    assert TOPIC_ENTRIES_KEY == "topic_entries"
    assert POSSIBLES_REGISTER_KEY == "possibles_register"


def test_bootstrap_index_without_possibles_register_yields_empty(tmp_path):
    # An index that carries topic_entries but NO possibles_register is the
    # documented BOOTSTRAP state — empty possibles, not an error.
    index = tmp_path / "ideation" / "cross-reference.yaml"
    index.parent.mkdir(parents=True)
    index.write_text(textwrap.dedent("""\
        schema_version: 1
        kind: ideation-cross-reference
        generation: {source_revision: deadbeef}
        topic_entries:
          - id: cl-alpha
            name: Alpha
            topics: [alpha]
            tag_sources: [topics-header]
            members: []
            extension_fit: {has_promoted_fit: false, statement: none}
    """), encoding="utf-8")
    adapter = CrossReferenceIndexAdapter.discover(tmp_path)
    assert adapter.possibles() == []                      # bootstrap: empty
    assert [e["id"] for e in adapter.topic_entries()] == ["cl-alpha"]  # names still read


def test_missing_cross_reference_source_yields_empty(tmp_path):
    assert CrossReferenceIndexAdapter.discover(tmp_path).possibles() == []
    assert CrossReferenceIndexAdapter.discover(tmp_path).topic_entries() == []
    assert CrossReferenceIndexAdapter(None).possibles() == []
    assert CrossReferenceIndexAdapter(None).topic_entries() == []


# ---- project register ----

def test_project_resolution_repo_project_group():
    adapter = ProjectRegisterAdapter.discover(BASE_REPO)
    assert adapter.resolve("fixture-repo") == ("fixture-core", "fixture-family")
    assert adapter.resolve("fixture-repo-b") == ("fixture-siblings", "fixture-family")


def test_absent_repository_resolves_ungrouped():
    adapter = ProjectRegisterAdapter.discover(BASE_REPO)
    assert adapter.resolve("not-registered") == (None, None)


def test_missing_project_register_resolves_ungrouped(tmp_path):
    adapter = ProjectRegisterAdapter.discover(tmp_path)
    assert adapter.resolve("anything") == (None, None)
    assert adapter.projects() == []
