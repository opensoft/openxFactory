"""Shared inventory module: extraction parity with the semantic sweep,
the prior list-format migration read path, and extended-field determinism
over the catalog fixture workspace. All tests are hermetic — the fixture
workspace is read-only and git facts come from conftest.FakeGit."""

from __future__ import annotations

import hashlib
import json

import pytest

from conftest import FIXTURES, FakeGit  # noqa: F401  (sys.path side effect)

from doc_health import inventory, semantic
from doc_health.corpus import Doc, load_docs

WORKSPACE = FIXTURES / "catalog" / "workspace"
HEADS = {"alpha": "a" * 40, "openxFactory": "b" * 40}

EXTENDED_KEYS = {
    "repo", "path", "status", "kind", "repository_context", "handling",
    "artifact_type", "revision", "content_hash", "snapshot_id",
}


def make_docs():
    return [
        Doc("alpha", "docs/a.md", "alpha doc body", "draft"),
        Doc("alpha", "docs/b.md", "beta doc body", "ratified"),
        Doc("openxFactory", "docs/n.md", "neutral doc body", "standard"),
    ]


def legacy_entry(d):
    """The pre-extraction semantic.build_inventory entry, copied verbatim
    as the parity reference."""
    return {"repo": d.repo, "path": d.path,
            "status": d.status or "(none)",
            "content_hash": hashlib.sha256(d.text.encode()).hexdigest()}


def workspace_repo_paths():
    return {p.name: p for p in sorted(WORKSPACE.iterdir()) if p.is_dir()}


def workspace_docs(repo_paths):
    docs = []
    for name in sorted(repo_paths):
        docs.extend(load_docs(name, repo_paths[name]))
    return docs


def extended_inventory():
    repo_paths = workspace_repo_paths()
    return inventory.build_inventory(
        workspace_docs(repo_paths), repo_paths, git=FakeGit(heads=HEADS))


def by_key(entries):
    return {(e["repo"], e["path"]): e for e in entries}


# --- extraction parity (T002) ------------------------------------------------

def test_semantic_reexports_the_shared_inventory_functions():
    assert semantic.build_inventory is inventory.build_inventory
    assert semantic.changed_paths is inventory.changed_paths


def test_legacy_shape_is_byte_identical_to_pre_extraction_output():
    docs = make_docs()
    expected = sorted((legacy_entry(d) for d in docs),
                      key=lambda e: (e["repo"], e["path"]))
    got = inventory.build_inventory(docs)
    assert got == expected
    # The exact artifact rendering prepare_bundle / --emit-inventory use.
    assert (json.dumps(got, indent=1, sort_keys=True) + "\n"
            == json.dumps(expected, indent=1, sort_keys=True) + "\n")
    assert all(set(e) == {"repo", "path", "status", "content_hash"}
               for e in got)


def test_changed_paths_matches_pre_extraction_semantics():
    old = inventory.build_inventory(make_docs())
    docs = make_docs()
    docs[0] = Doc("alpha", "docs/a.md", "EDITED body", "draft")
    docs.append(Doc("alpha", "docs/new.md", "brand new", "draft"))
    changed = inventory.changed_paths(inventory.build_inventory(docs), old)
    assert changed == {("alpha", "docs/a.md"), ("alpha", "docs/new.md")}


def test_changed_paths_bridges_legacy_previous_and_extended_current():
    repo_paths = workspace_repo_paths()
    docs = workspace_docs(repo_paths)
    legacy_previous = inventory.build_inventory(docs)
    current = extended_inventory()
    changed = inventory.changed_paths(current, legacy_previous)
    # Only the promoted specs are new to the extended view; identical
    # content never reads as changed across the format migration.
    assert changed == {
        ("alpha", "openspec/specs/widget/spec.md"),
        ("openxFactory", "openspec/specs/document-lifecycle/spec.md"),
    }


# --- migration read path (T002) ------------------------------------------------

def test_load_previous_migrates_prior_list_format(tmp_path):
    prior = inventory.build_inventory(make_docs())  # sweep v1 artifact
    artifact = tmp_path / "inventory.json"
    artifact.write_text(json.dumps(prior, indent=1, sort_keys=True) + "\n",
                        encoding="utf-8")
    loaded = inventory.load_previous(artifact)
    assert [(e["repo"], e["path"]) for e in loaded] == \
        [(e["repo"], e["path"]) for e in prior]
    for old, new in zip(prior, loaded):
        assert set(new) == EXTENDED_KEYS
        for key in ("repo", "path", "status", "content_hash"):
            assert new[key] == old[key]
        for key in inventory.EXTENDED_FIELDS:
            assert new[key] is None


def test_load_previous_reads_extended_format_unchanged(tmp_path):
    entries = extended_inventory()
    artifact = tmp_path / "inventory.json"
    artifact.write_text(json.dumps(entries, indent=1, sort_keys=True) + "\n",
                        encoding="utf-8")
    assert inventory.load_previous(artifact) == entries


def test_load_previous_missing_file_is_none(tmp_path):
    assert inventory.load_previous(tmp_path / "absent.json") is None


def test_load_previous_rejects_unrecognized_shapes(tmp_path):
    not_a_list = tmp_path / "bad-shape.json"
    not_a_list.write_text('{"entries": []}', encoding="utf-8")
    with pytest.raises(ValueError):
        inventory.load_previous(not_a_list)
    bad_entry = tmp_path / "bad-entry.json"
    bad_entry.write_text('[{"repo": "alpha"}]', encoding="utf-8")
    with pytest.raises(ValueError):
        inventory.load_previous(bad_entry)


def test_loaded_previous_feeds_changed_paths(tmp_path):
    artifact = tmp_path / "inventory.json"
    artifact.write_text(
        json.dumps(inventory.build_inventory(make_docs()),
                   indent=1, sort_keys=True) + "\n", encoding="utf-8")
    previous = inventory.load_previous(artifact)
    docs = make_docs()
    docs[1] = Doc("alpha", "docs/b.md", "EDITED beta", "ratified")
    changed = inventory.changed_paths(
        inventory.build_inventory(docs), previous)
    assert changed == {("alpha", "docs/b.md")}


# --- extended entries over the fixture workspace (T003) -------------------------

def test_extended_inventory_is_deterministic_and_byte_stable():
    first, second = extended_inventory(), extended_inventory()
    assert first == second
    assert (json.dumps(first, indent=1, sort_keys=True) + "\n"
            == json.dumps(second, indent=1, sort_keys=True) + "\n")
    # Input doc order must not leak into the output ordering.
    repo_paths = workspace_repo_paths()
    shuffled = list(reversed(workspace_docs(repo_paths)))
    assert inventory.build_inventory(
        shuffled, repo_paths, git=FakeGit(heads=HEADS)) == first
    assert [(e["repo"], e["path"]) for e in first] == \
        sorted((e["repo"], e["path"]) for e in first)


def test_extended_entries_carry_the_data_model_fields():
    entries = by_key(extended_inventory())
    protected = entries[("alpha", "docs/protected-roster.md")]
    assert set(protected) == EXTENDED_KEYS
    assert protected["status"] == "draft"
    assert protected["kind"] == "reference"
    assert protected["repository_context"] == "alpha"
    assert protected["handling"] == "protected"
    assert protected["artifact_type"] == "governance_markdown"
    assert len(protected["content_hash"]) == 64
    bare = entries[("alpha", "examples/widget-walkthrough.md")]
    assert bare["kind"] is None
    assert bare["repository_context"] is None
    assert bare["handling"] is None


def test_promoted_specs_join_without_expanding_the_governed_corpus():
    repo_paths = workspace_repo_paths()
    docs = workspace_docs(repo_paths)
    assert not any(d.path.startswith("openspec/") for d in docs)
    entries = extended_inventory()
    specs = {(e["repo"], e["path"]): e for e in entries
             if e["artifact_type"] == "promoted_spec"}
    assert set(specs) == {
        ("alpha", "openspec/specs/widget/spec.md"),
        ("openxFactory", "openspec/specs/document-lifecycle/spec.md"),
    }
    assert len(entries) == len(docs) + len(specs)
    assert all(e["artifact_type"] == "governance_markdown"
               for e in entries
               if (e["repo"], e["path"]) not in specs)
    assert specs[("alpha", "openspec/specs/widget/spec.md")]["status"] \
        == "(none)"  # specs carry no lifecycle header


def test_deliberate_violation_and_generated_fixtures_stay_excluded():
    keys = {(e["repo"], e["path"]) for e in extended_inventory()}
    assert not any("deliberate-violations" in path for _, path in keys)
    assert ("openxFactory",
            "openspec/changes/add-widget-catalog/proposal.md") not in keys
    assert not any(path.endswith(".yaml") for _, path in keys)


def test_revision_comes_from_the_owning_repo_head(monkeypatch):
    entries = extended_inventory()
    assert all(e["revision"] == HEADS[e["repo"]] for e in entries)
    # The documented two-argument call (contracts/module-interfaces.md)
    # resolves revisions through the default git implementation
    # (corpus.RealGit) — never null; null `revision` exists only on the
    # load_previous migration path (data-model.md types it `str`).
    monkeypatch.setattr(inventory.corpus, "RealGit",
                        lambda: FakeGit(heads=HEADS))
    repo_paths = workspace_repo_paths()
    documented = inventory.build_inventory(
        workspace_docs(repo_paths), repo_paths)
    assert documented == entries
    assert all(e["revision"] == HEADS[e["repo"]] for e in documented)


def test_doc_repo_absent_from_repo_paths_fails_loudly():
    repo_paths = workspace_repo_paths()
    docs = workspace_docs(repo_paths) + [
        Doc("ghost", "docs/orphan.md", "orphan body", "draft")]
    with pytest.raises(ValueError, match="ghost"):
        inventory.build_inventory(docs, repo_paths,
                                  git=FakeGit(heads=HEADS))


def test_unresolvable_head_revision_fails_loudly():
    repo_paths = workspace_repo_paths()
    docs = workspace_docs(repo_paths)
    partial_heads = {"openxFactory": HEADS["openxFactory"]}
    with pytest.raises(ValueError, match="alpha"):
        inventory.build_inventory(docs, repo_paths,
                                  git=FakeGit(heads=partial_heads))


def test_snapshot_id_is_shared_content_derived_and_stable():
    entries = extended_inventory()
    ids = {e["snapshot_id"] for e in entries}
    assert len(ids) == 1
    sid = ids.pop()
    assert sid == inventory.snapshot_id(entries)  # self-consistent
    assert {e["snapshot_id"] for e in extended_inventory()} == {sid}
    # Any content change produces a different snapshot id.
    repo_paths = workspace_repo_paths()
    docs = workspace_docs(repo_paths)
    edited = [Doc(d.repo, d.path, d.text + "\nedited\n", d.status, d.kind)
              if d.path == "docs/widget-overview.md" else d for d in docs]
    changed = inventory.build_inventory(
        edited, repo_paths, git=FakeGit(heads=HEADS))
    assert {e["snapshot_id"] for e in changed} != {sid}
