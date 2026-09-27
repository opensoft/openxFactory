"""Mechanical catalog (US1): deterministic entries, diff classes,
rename-as-delete-plus-add, immutable dated snapshots with effective
taxonomy provenance, byte-identical rendering, atomically claimed run
sequences, stale-overwrite refusal, opaque locators for path-prohibited
documents, recursion exclusion, and the no-source-mutation boundary.

All tests are hermetic: the fixture workspace is read-only (mutation
scenarios copy it into pytest tmp dirs), git facts come from
conftest.FakeGit, and every write lands under a tmp catalog root."""

from __future__ import annotations

import hashlib
import json
import os
import shutil
import threading
from datetime import datetime
from pathlib import Path

import pytest

from conftest import AS_OF, FIXTURES, FakeGit  # noqa: F401 (sys.path side effect)

from doc_health import catalog, inventory
from doc_health.corpus import Doc, load_docs

WORKSPACE = FIXTURES / "catalog" / "workspace"
HEADS = {"alpha": "a" * 40, "openxFactory": "b" * 40}
LATER_HEADS = {"alpha": "c" * 40, "openxFactory": "d" * 40}
DAY = AS_OF  # date(2026, 7, 9) — dates are parameters, never wall clock
DAY_STR = AS_OF.isoformat()

ENTRY_KEYS = {
    "repo", "path", "status", "kind", "repository_context", "handling",
    "artifact_type", "revision", "content_hash", "snapshot_id",
}

REGISTRY_PATHS = {
    "alpha": "catalog/document-tag-registry.yaml",
    "openxFactory": "contracts/document-tag-registry.yaml",
}
REGISTRIES = [WORKSPACE / repo / rel
              for repo, rel in sorted(REGISTRY_PATHS.items())]
# Registry-file last-modifying revisions: fixed provenance parameters,
# distinct from the pinned repo HEADs (never derived from wall clock).
REGISTRY_REVISIONS = {"alpha": "1" * 40, "openxFactory": "2" * 40}

PROTECTED = ("alpha", "docs/protected-roster.md")


def registry_inputs(base=WORKSPACE, heads=HEADS):
    """The two fixture registries as contract taxonomy inputs."""
    return [
        catalog.registry_input(
            repo, REGISTRY_PATHS[repo], base / repo / REGISTRY_PATHS[repo],
            repository_revision=heads[repo],
            registry_revision=REGISTRY_REVISIONS[repo])
        for repo in sorted(REGISTRY_PATHS)]


def taxonomy_for(base=WORKSPACE, heads=HEADS):
    return catalog.effective_taxonomy(registry_inputs(base, heads))


TAXONOMY = taxonomy_for()


def prohibit_protected(entry):
    """Stand-in handling-gate policy: path persistence is prohibited for
    source-declared protected handling."""
    return entry.get("handling") == "protected"


def repo_paths_for(base):
    return {p.name: p for p in sorted(base.iterdir()) if p.is_dir()}


def docs_for(repo_paths):
    docs = []
    for name in sorted(repo_paths):
        docs.extend(load_docs(name, repo_paths[name]))
    return docs


def extended_inventory(base=WORKSPACE, heads=HEADS):
    repo_paths = repo_paths_for(base)
    return inventory.build_inventory(
        docs_for(repo_paths), repo_paths, git=FakeGit(heads=heads))


def by_key(entries):
    return {(e["repo"], e["path"]): e for e in entries}


def entries_by_repo(entries):
    """{repo: that repo's entries}, the shape catalog.run_id/write_run take."""
    grouped = {}
    for entry in entries:
        grouped.setdefault(entry["repo"], []).append(entry)
    return grouped


def write_run(root, inv, as_of=DAY, taxonomy=None):
    """One full mechanical pass: entries -> per-repository snapshots,
    recorded through catalog.write_run (the content-addressed id)."""
    taxonomy = TAXONOMY if taxonomy is None else taxonomy
    return catalog.write_run(
        root, as_of, entries_by_repo(catalog.mechanical_entries(inv)),
        taxonomy)


def alpha_entries(inv):
    return [e for e in catalog.mechanical_entries(inv) if e["repo"] == "alpha"]


def runs_root(root):
    return root / "health" / "document-catalog" / "runs"


def tree_state(base):
    """(relative path -> sha256) for every file under base."""
    return {
        p.relative_to(base).as_posix():
            hashlib.sha256(p.read_bytes()).hexdigest()
        for p in sorted(base.rglob("*")) if p.is_file()}


def mutated_workspace(tmp_path):
    ws = tmp_path / "workspace"
    shutil.copytree(WORKSPACE, ws)
    return ws


# --- mechanical entries (T005) ----------------------------------------------

def test_mechanical_entries_cover_every_governed_document():
    inv = extended_inventory()
    entries = catalog.mechanical_entries(inv)
    # Acceptance 1: one entry per governed document, carrying identity,
    # status, kind, repository context, artifact type, revision, hash.
    assert [(e["repo"], e["path"]) for e in entries] == \
        [(e["repo"], e["path"]) for e in inv]
    assert all(set(e) == ENTRY_KEYS for e in entries)
    assert [(e["repo"], e["path"]) for e in entries] == \
        sorted((e["repo"], e["path"]) for e in entries)
    for got, src in zip(entries, inv):
        assert got == {k: src[k] for k in ENTRY_KEYS}
    # New value copies — mutating the catalog view cannot corrupt the
    # inventory.
    entries[0]["status"] = "tampered"
    assert inv[0]["status"] != "tampered"


def test_mechanical_entries_require_a_fresh_extended_inventory(tmp_path):
    docs = [Doc("alpha", "docs/a.md", "body", "draft")]
    legacy = inventory.build_inventory(docs)  # no extended fields
    with pytest.raises(ValueError):
        catalog.mechanical_entries(legacy)
    # Migration-loaded artifacts carry null extended fields — they can
    # feed diffs but never seed the catalog.
    artifact = tmp_path / "inventory.json"
    artifact.write_text(json.dumps(legacy, indent=1, sort_keys=True) + "\n",
                        encoding="utf-8")
    migrated = inventory.load_previous(artifact)
    with pytest.raises(ValueError):
        catalog.mechanical_entries(migrated)


def test_mechanical_entries_exclude_generated_catalog_records():
    inv = extended_inventory()
    generated = dict(inv[0])
    generated["path"] = \
        "health/document-catalog/runs/2026-07-08/deadbeef/alpha.yaml"
    entries = catalog.mechanical_entries(inv + [generated])
    assert not any(
        e["path"].startswith("health/document-catalog/") for e in entries)
    assert len(entries) == len(inv)


# --- opaque locators for path-prohibited documents (contract US1 scope) ------

def test_policy_prohibited_paths_use_opaque_locators():
    # Contract scenario "Path persistence is prohibited": the entry uses
    # an opaque document reference plus path SHA-256 and omits the path.
    inv = extended_inventory()
    entries = catalog.mechanical_entries(
        inv, path_prohibited=prohibit_protected)
    assert len(entries) == len(inv)
    opaque = [e for e in entries if "path" not in e]
    assert len(opaque) == 1
    entry = opaque[0]
    locator = catalog.opaque_locator(*PROTECTED)
    assert entry["repo"] == PROTECTED[0]
    assert entry["document_ref"] == locator["document_ref"]
    assert entry["path_sha256"] == \
        hashlib.sha256(PROTECTED[1].encode()).hexdigest()
    assert entry["document_ref"] != entry["path_sha256"]
    assert set(entry) == \
        (ENTRY_KEYS - {"path"}) | {"document_ref", "path_sha256"}
    # Mechanical fields (including source-declared handling) persist.
    src = by_key(inv)[PROTECTED]
    assert entry["content_hash"] == src["content_hash"]
    assert entry["handling"] == "protected"
    # Every other entry still persists its path.
    assert all("document_ref" not in e for e in entries if "path" in e)
    # The opaque locator is stable: an unchanged corpus diffs empty and
    # a content change is a modification keyed by the reference.
    again = catalog.mechanical_entries(
        extended_inventory(WORKSPACE, LATER_HEADS),
        path_prohibited=prohibit_protected)
    assert catalog.diff(entries, again).empty


def test_opaque_entries_omit_the_path_from_snapshots(tmp_path):
    root = tmp_path / "agg"
    inv = extended_inventory()
    entries = catalog.mechanical_entries(
        inv, path_prohibited=prohibit_protected)
    alpha = [e for e in entries if e["repo"] == "alpha"]
    rid = catalog.run_id({"alpha": alpha}, TAXONOMY)
    alpha_path = catalog.write_snapshot(root, DAY, rid, "alpha", alpha,
                                        TAXONOMY)
    rendered = alpha_path.read_text(encoding="utf-8")
    # FR-012: neither the protected path nor protected content appears
    # in the produced artifact.
    assert "protected-roster" not in rendered
    assert "PROTECTED-ROSTER-ALPHA" not in rendered
    loaded = catalog.load_snapshot(root)
    ref = catalog.opaque_locator(*PROTECTED)["document_ref"]
    found = [e for e in loaded["repos"]["alpha"]["entries"]
             if e.get("document_ref") == ref]
    assert len(found) == 1 and "path" not in found[0]
    # A content change on the protected document still diffs as a
    # modification under the opaque key.
    ws = mutated_workspace(tmp_path)
    doc = ws / "alpha" / "docs" / "protected-roster.md"
    doc.write_text(doc.read_text(encoding="utf-8") + "\nrevised\n",
                   encoding="utf-8")
    curr = catalog.mechanical_entries(
        extended_inventory(ws, LATER_HEADS),
        path_prohibited=prohibit_protected)
    d = catalog.diff(entries, curr)
    assert d.modified_keys == ((PROTECTED[0], ref),)


def test_ambiguous_locators_are_rejected(tmp_path):
    # Contract scenario "Locator is ambiguous": both a persisted path
    # and an opaque reference, or neither, is rejected.
    inv = extended_inventory()
    entries = catalog.mechanical_entries(inv)
    both = dict(entries[0],
                **catalog.opaque_locator(entries[0]["repo"],
                                         entries[0]["path"]))
    with pytest.raises(ValueError, match="ambiguous"):
        catalog.diff([both], [])
    neither = {k: v for k, v in entries[0].items() if k != "path"}
    with pytest.raises(ValueError, match="ambiguous"):
        catalog.diff([neither], [])
    partial = dict(neither, document_ref="0" * 64)  # no path_sha256
    with pytest.raises(ValueError, match="ambiguous"):
        catalog.diff([partial], [])
    # The snapshot writer refuses them too, before anything lands — and so
    # does minting a run id over them, since the id addresses the snapshot
    # the writer would render.
    repo = entries[0]["repo"]
    rid = catalog.run_id({repo: [entries[0]]}, TAXONOMY)
    with pytest.raises(ValueError, match="ambiguous"):
        catalog.write_snapshot(tmp_path / "agg", DAY, rid, repo, [both],
                               TAXONOMY)
    with pytest.raises(ValueError, match="ambiguous"):
        catalog.run_id({repo: [both]}, TAXONOMY)
    with pytest.raises(ValueError, match="ambiguous"):
        catalog.write_run(tmp_path / "agg", DAY, {repo: [both]}, TAXONOMY)
    assert not (tmp_path / "agg").exists()


# --- diff classes and rename semantics (T005) --------------------------------

def test_diff_reports_add_edit_delete_exactly(tmp_path):
    ws = mutated_workspace(tmp_path)
    prev = catalog.mechanical_entries(extended_inventory(ws, HEADS))
    (ws / "alpha" / "docs" / "brand-new.md").write_text(
        "Status: draft\n\nA brand new governed doc.\n", encoding="utf-8")
    edited = ws / "alpha" / "docs" / "widget-overview.md"
    edited.write_text(edited.read_text(encoding="utf-8") + "\nedited\n",
                      encoding="utf-8")
    (ws / "openxFactory" / "docs" / "legacy-catalog-guide.md").unlink()
    curr = catalog.mechanical_entries(extended_inventory(ws, LATER_HEADS))
    d = catalog.diff(prev, curr)
    assert d.added_keys == (("alpha", "docs/brand-new.md"),)
    assert d.modified_keys == (("alpha", "docs/widget-overview.md"),)
    assert d.deleted_keys == (("openxFactory",
                               "docs/legacy-catalog-guide.md"),)
    assert not d.empty


def test_diff_rename_is_delete_plus_add_without_continuity(tmp_path):
    # Acceptance 3: a rename records a deletion plus an addition — no
    # fabricated continuity between the keys.
    ws = mutated_workspace(tmp_path)
    prev = catalog.mechanical_entries(extended_inventory(ws, HEADS))
    old = ws / "alpha" / "docs" / "widget-register.md"
    new = ws / "alpha" / "docs" / "widget-register-v2.md"
    old.rename(new)
    curr = catalog.mechanical_entries(extended_inventory(ws, LATER_HEADS))
    d = catalog.diff(prev, curr)
    assert d.deleted_keys == (("alpha", "docs/widget-register.md"),)
    assert d.added_keys == (("alpha", "docs/widget-register-v2.md"),)
    assert d.modified == ()
    # Same content travelled — but the diff carries two independent
    # entries, not a rename link.
    assert d.deleted[0]["content_hash"] == d.added[0]["content_hash"]


def test_diff_ignores_unrelated_commits():
    # Revision/snapshot-id churn without content change is not a
    # modification (design decision 8).
    prev = catalog.mechanical_entries(extended_inventory(WORKSPACE, HEADS))
    curr = catalog.mechanical_entries(
        extended_inventory(WORKSPACE, LATER_HEADS))
    assert prev != curr  # revisions did move
    assert catalog.diff(prev, curr).empty


def test_diff_rejects_duplicate_keys():
    entries = catalog.mechanical_entries(extended_inventory())
    with pytest.raises(ValueError, match="duplicate"):
        catalog.diff(entries + [dict(entries[0])], entries)
    with pytest.raises(ValueError, match="duplicate"):
        catalog.diff(entries, entries + [dict(entries[-1])])


# --- taxonomy digest and run id (T006) ---------------------------------------

def test_taxonomy_digest_uses_the_contract_input_formula(tmp_path):
    # Contract: SHA-256 over the ordered canonical repository, path,
    # registry content hash, and registry-version inputs.
    inputs = registry_inputs()
    digest = catalog.taxonomy_digest(inputs)
    assert len(digest) == 64
    # Caller order never matters — inputs are ordered canonically.
    assert digest == catalog.taxonomy_digest(list(reversed(inputs)))
    # Machine-local file locations never enter the digest: the same
    # canonical inputs read from copies elsewhere digest identically.
    copies = []
    for i, src in enumerate(REGISTRIES):
        dst = tmp_path / str(i) / src.name
        dst.parent.mkdir()
        dst.write_bytes(src.read_bytes())
        copies.append(dst)
    from_copies = [
        catalog.registry_input(
            repo, REGISTRY_PATHS[repo], copies[i],
            repository_revision=HEADS[repo],
            registry_revision=REGISTRY_REVISIONS[repo])
        for i, repo in enumerate(sorted(REGISTRY_PATHS))]
    assert catalog.taxonomy_digest(from_copies) == digest
    # Swapping two registries' contents changes the digest even though
    # both files share the basename document-tag-registry.yaml: the
    # canonical repository and path are digest inputs, so an effective
    # registry change between namespaces always invalidates.
    swapped = [dict(inputs[0], content_sha256=inputs[1]["content_sha256"]),
               dict(inputs[1], content_sha256=inputs[0]["content_sha256"])]
    assert catalog.taxonomy_digest(swapped) != digest
    # registry_version is a distinct digest input.
    bumped = [dict(inputs[0], registry_version="2"), inputs[1]]
    assert catalog.taxonomy_digest(bumped) != digest
    # Registry content change changes the digest.
    changed = tmp_path / "changed" / REGISTRIES[0].name
    changed.parent.mkdir()
    changed.write_bytes(REGISTRIES[0].read_bytes() + b"\n# drift\n")
    drifted = [catalog.registry_input(
        "alpha", REGISTRY_PATHS["alpha"], changed,
        repository_revision=HEADS["alpha"],
        registry_revision=REGISTRY_REVISIONS["alpha"]), inputs[1]]
    assert catalog.taxonomy_digest(drifted) != digest


def test_provenance_revisions_never_alter_the_digest():
    # Contract scenario "Registry repository changes elsewhere": a new
    # pinned revision with unchanged registry content and version keeps
    # the effective digest identical while provenance records the move.
    inputs = registry_inputs()
    moved = [dict(i, repository_revision="f" * 40,
                  registry_revision="e" * 40) for i in inputs]
    assert catalog.taxonomy_digest(moved) == catalog.taxonomy_digest(inputs)
    before = catalog.effective_taxonomy(inputs)
    after = catalog.effective_taxonomy(moved)
    assert after["digest"] == before["digest"]
    assert after["inputs"] != before["inputs"]  # provenance did move
    assert [i["repository_revision"] for i in after["inputs"]] == \
        ["f" * 40, "f" * 40]


def test_taxonomy_inputs_must_be_complete_and_unique():
    # Contract scenario "Taxonomy inputs are incomplete".
    inputs = registry_inputs()
    for field in ("repository", "path", "content_sha256",
                  "registry_version"):
        broken = [dict(inputs[0]), inputs[1]]
        del broken[0][field]
        with pytest.raises(ValueError, match="incomplete"):
            catalog.taxonomy_digest(broken)
    with pytest.raises(ValueError, match="incomplete"):
        catalog.taxonomy_digest([])
    with pytest.raises(ValueError, match="duplicate"):
        catalog.taxonomy_digest([inputs[0], dict(inputs[0])])
    # The effective-taxonomy block additionally requires provenance:
    # the pinned repository revision and the registry file revision.
    for field in ("repository_revision", "registry_revision"):
        broken = [dict(inputs[0]), inputs[1]]
        del broken[0][field]
        with pytest.raises(ValueError, match="incomplete"):
            catalog.effective_taxonomy(broken)
    block = catalog.effective_taxonomy(inputs)
    assert block["digest"] == catalog.taxonomy_digest(inputs)
    # Inputs are stored in canonical (repository, path) order.
    assert [(i["repository"], i["path"]) for i in block["inputs"]] == \
        [("alpha", REGISTRY_PATHS["alpha"]),
         ("openxFactory", REGISTRY_PATHS["openxFactory"])]


def test_registry_input_reads_content_hash_and_version(tmp_path):
    inp = catalog.registry_input(
        "alpha", REGISTRY_PATHS["alpha"], REGISTRIES[0],
        repository_revision=HEADS["alpha"],
        registry_revision=REGISTRY_REVISIONS["alpha"])
    assert inp == {
        "repository": "alpha",
        "path": REGISTRY_PATHS["alpha"],
        "content_sha256":
            hashlib.sha256(REGISTRIES[0].read_bytes()).hexdigest(),
        "registry_version": "1",
        "repository_revision": HEADS["alpha"],
        "registry_revision": REGISTRY_REVISIONS["alpha"],
    }
    unversioned = tmp_path / "registry.yaml"
    unversioned.write_text(
        "schema_version: 1\nkind: xfactory_document_tag_registry\n",
        encoding="utf-8")
    with pytest.raises(ValueError, match="registry_version"):
        catalog.registry_input(
            "alpha", "catalog/registry.yaml", unversioned,
            repository_revision=HEADS["alpha"],
            registry_revision=REGISTRY_REVISIONS["alpha"])


def test_legacy_run_id_is_inventory_and_taxonomy_derived():
    # The pre-#519 key, kept only to recognize the runs recorded under it.
    inv = extended_inventory()
    rid = catalog.legacy_run_id(inv)
    assert rid == catalog.legacy_run_id(extended_inventory())  # no wall clock
    assert rid == inventory.snapshot_id(inv)
    # Any corpus change — content or revision — is a different key.
    assert catalog.legacy_run_id(
        extended_inventory(WORKSPACE, LATER_HEADS)) != rid
    # The effective taxonomy digest folds in, so a taxonomy change over an
    # unchanged corpus is a different key too.
    with_taxonomy = catalog.legacy_run_id(inv, TAXONOMY)
    assert with_taxonomy != rid
    assert with_taxonomy == catalog.legacy_run_id(extended_inventory(),
                                                  TAXONOMY)
    other = catalog.effective_taxonomy(
        [dict(registry_inputs()[0], registry_version="9")])
    assert catalog.legacy_run_id(inv, other) != with_taxonomy


def classified(entries, path, value):
    """`entries` with one document carrying a suggested factory_scope, the
    shape a merged cataloger recommendation leaves on an entry."""
    out = []
    for entry in entries:
        entry = dict(entry)
        if entry["path"] == path:
            entry["facet_assignments"] = [{
                "facet": "factory_scope", "proposed_values": [],
                "review": None, "state": "suggested",
                "state_since": DAY_STR, "transitions": [],
                "values": [value]}]
        out.append(entry)
    return out


def test_run_id_is_a_content_address():
    # opensoft/xFactory#519: the id addresses the recorded CONTENT, not
    # just the inventory and taxonomy that shaped part of it.
    inv = extended_inventory()
    runs = entries_by_repo(catalog.mechanical_entries(inv))
    rid = catalog.run_id(runs, TAXONOMY)
    assert len(rid) == 64 and set(rid) <= set("0123456789abcdef")
    # Deterministic, independent of caller order (repositories or entries).
    assert rid == catalog.run_id(
        entries_by_repo(catalog.mechanical_entries(extended_inventory())),
        TAXONOMY)
    assert rid == catalog.run_id(
        {repo: list(reversed(runs[repo])) for repo in reversed(sorted(runs))},
        TAXONOMY)
    # The SAME inventory and taxonomy with a different classification --
    # the #519 collision -- is a different run.
    reclassified = dict(runs, alpha=classified(
        runs["alpha"], "docs/widget-overview.md", "domain"))
    assert catalog.run_id(reclassified, TAXONOMY) != rid
    assert catalog.run_id(dict(runs, alpha=classified(
        runs["alpha"], "docs/widget-overview.md", "neutral")), TAXONOMY) \
        != catalog.run_id(reclassified, TAXONOMY)
    # A revision-only move and a taxonomy change are still new runs.
    assert catalog.run_id(entries_by_repo(catalog.mechanical_entries(
        extended_inventory(WORKSPACE, LATER_HEADS))), TAXONOMY) != rid
    other = catalog.effective_taxonomy(
        [dict(registry_inputs()[0], registry_version="9")])
    assert catalog.run_id(runs, other) != rid
    # Dropping a repository is a different run: the id covers the whole run.
    assert catalog.run_id({"alpha": runs["alpha"]}, TAXONOMY) != rid
    # It never equals the legacy key for the same inputs.
    assert rid != catalog.legacy_run_id(inv, TAXONOMY)
    with pytest.raises(ValueError, match="at least one"):
        catalog.run_id({}, TAXONOMY)


def test_write_run_records_under_the_content_address(tmp_path):
    root = tmp_path / "agg"
    inv = extended_inventory()
    runs = entries_by_repo(catalog.mechanical_entries(inv))
    rid, paths = catalog.write_run(root, DAY, runs, TAXONOMY)
    assert rid == catalog.run_id(runs, TAXONOMY)
    assert sorted(paths) == ["alpha", "openxFactory"]
    assert all(p.parent == runs_root(root) / DAY_STR / rid
               for p in paths.values())
    recorded = catalog.load_snapshot(root)
    assert recorded["run_id"] == rid
    # The recorded documents themselves hash back to the id.
    assert catalog.content_digest(recorded["repos"]) == rid
    assert catalog.run_id_scheme(rid, recorded["repos"]) == \
        catalog.CONTENT_ADDRESSED


def test_two_trees_recording_one_corpus_share_an_id_only_for_one_content(
        tmp_path):
    # The #519 shape: two producers of the SAME inventory and taxonomy on
    # the same day, in trees that never see each other. Identical content
    # converges on one id and byte-identical files; a different
    # classification can no longer land under the same id.
    inv = extended_inventory()
    runs = entries_by_repo(catalog.mechanical_entries(inv))
    rid_a, paths_a = catalog.write_run(tmp_path / "a", DAY, runs, TAXONOMY)
    rid_b, paths_b = catalog.write_run(tmp_path / "b", DAY, runs, TAXONOMY)
    assert rid_a == rid_b
    assert {r: p.read_bytes() for r, p in paths_a.items()} == \
        {r: p.read_bytes() for r, p in paths_b.items()}
    reclassified = dict(runs, alpha=classified(
        runs["alpha"], "docs/widget-overview.md", "domain"))
    rid_c, _ = catalog.write_run(tmp_path / "c", DAY, reclassified, TAXONOMY)
    assert rid_c != rid_a
    # Under the legacy key all three would have shared ONE id.
    assert catalog.legacy_run_id(inv, TAXONOMY) == \
        catalog.legacy_run_id(extended_inventory(), TAXONOMY)


def test_run_id_scheme_tells_content_legacy_and_edited_runs_apart(tmp_path):
    inv = extended_inventory()
    runs = entries_by_repo(catalog.mechanical_entries(inv))
    # A content-addressed run verifies.
    rid, _ = catalog.write_run(tmp_path / "new", DAY, runs, TAXONOMY)
    new_docs = catalog.load_snapshot(tmp_path / "new")["repos"]
    assert catalog.run_id_scheme(rid, new_docs) == catalog.CONTENT_ADDRESSED
    # A run recorded under the pre-#519 key is recognized, not verified.
    legacy = catalog.legacy_run_id(inv, TAXONOMY)
    for repo, entries in sorted(runs.items()):
        catalog.write_snapshot(tmp_path / "old", DAY, legacy, repo, entries,
                               TAXONOMY)
    old_docs = catalog.load_snapshot(tmp_path / "old")["repos"]
    assert catalog.run_id_scheme(legacy, old_docs) == \
        catalog.LEGACY_INPUT_KEY
    # An edited snapshot under a content-addressed id is neither.
    edited = json.loads(json.dumps(new_docs))
    edited["alpha"]["entries"][0]["status"] = "tampered"
    assert catalog.run_id_scheme(rid, edited) is None
    # A lost repository snapshot is neither.
    assert catalog.run_id_scheme(rid, {"alpha": new_docs["alpha"]}) is None
    # A file from another run (its own run_id) mixed in is neither.
    catalog.write_run(tmp_path / "other", DAY, dict(
        runs, alpha=classified(runs["alpha"], "docs/widget-overview.md",
                               "domain")), TAXONOMY)
    other = catalog.load_snapshot(tmp_path / "other")["repos"]
    assert catalog.run_id_scheme(rid, dict(new_docs, alpha=other["alpha"])) \
        is None
    # Retagging that foreign file with this run's id still fails the hash.
    retagged = json.loads(json.dumps(other["alpha"]))
    retagged["run"]["run_id"] = rid
    assert catalog.run_id_scheme(rid, dict(new_docs, alpha=retagged)) is None
    # A run holding no snapshot at all is neither (never vacuously legacy).
    assert catalog.run_id_scheme(rid, {}) is None
    assert catalog.run_id_scheme(legacy, {}) is None


def test_run_id_scheme_verifies_the_persisted_bytes(tmp_path):
    # Review (Codex, #1175): parsing a re-serialized snapshot and rendering
    # it again reproduces the original bytes, so a check over parsed
    # documents alone would call an edited file intact. With the raw
    # persisted bytes, verification is byte for byte -- line endings too
    # (Copilot, #1175: a universal-newline text read would have translated
    # a CRLF edit back to the writer's LF before hashing).
    runs = entries_by_repo(catalog.mechanical_entries(extended_inventory()))
    rid, _ = catalog.write_run(tmp_path, DAY, runs, TAXONOMY)
    run_dir = runs_root(tmp_path) / DAY_STR / rid
    docs = catalog.load_snapshot(tmp_path)["repos"]
    persisted = catalog._load_run_bytes(run_dir)
    assert sorted(persisted) == sorted(docs)
    assert catalog.run_id_scheme(rid, docs, persisted) == \
        catalog.CONTENT_ADDRESSED
    # The byte-exact address equals the parsed one for the writer's files.
    assert catalog._persisted_digest(rid, persisted) == \
        catalog.content_digest(docs) == rid
    # Same content, different bytes: indentation, compact form, a trailing
    # newline, CRLF line endings.
    original = persisted["alpha"]
    for edited in (
            json.dumps(docs["alpha"], indent=4, sort_keys=True).encode(),
            json.dumps(docs["alpha"], sort_keys=True,
                       separators=(",", ":")).encode(),
            original + b"\n",
            original.replace(b"\n", b"\r\n")):
        assert json.loads(edited) == docs["alpha"]
        assert catalog.run_id_scheme(
            rid, docs, dict(persisted, alpha=edited)) is None
    # A CRLF file is exactly what a text-mode read would have hidden.
    (run_dir / "alpha.yaml").write_bytes(original.replace(b"\n", b"\r\n"))
    assert (run_dir / "alpha.yaml").read_text(encoding="utf-8") == \
        original.decode("utf-8")
    assert catalog.run_id_scheme(
        rid, docs, catalog._load_run_bytes(run_dir)) is None
    # The bytes must cover exactly the documents' repositories.
    assert catalog.run_id_scheme(
        rid, docs, {"alpha": persisted["alpha"]}) is None
    # A legacy run stays recognized on its derivation, bytes or not.
    inv = extended_inventory()
    legacy = catalog.legacy_run_id(inv, TAXONOMY)
    for repo, entries in sorted(runs.items()):
        catalog.write_snapshot(tmp_path / "old", DAY, legacy, repo, entries,
                               TAXONOMY)
    old_docs = catalog.load_snapshot(tmp_path / "old")["repos"]
    old_bytes = catalog._load_run_bytes(
        runs_root(tmp_path / "old") / DAY_STR / legacy)
    assert catalog.run_id_scheme(legacy, old_docs, old_bytes) == \
        catalog.LEGACY_INPUT_KEY


def test_write_run_preflights_every_repository_id_before_writing(tmp_path):
    # Review (Copilot, #1175): a valid repository sorted before an invalid
    # one must not be recorded first -- the run would be left partial,
    # holding a run.yaml and only some of its snapshots.
    alpha = alpha_entries(extended_inventory())
    for bad_repo in ("run", "../x", ".hidden", "alpha/../.."):
        runs = {"alpha": alpha, bad_repo: [dict(e, repo=bad_repo)
                                          for e in alpha]}
        with pytest.raises(ValueError, match="invalid repository id"):
            catalog.run_id(runs, TAXONOMY)
        with pytest.raises(ValueError, match="invalid repository id"):
            catalog.write_run(tmp_path / "agg", DAY, runs, TAXONOMY)
    assert not (tmp_path / "agg").exists()  # nothing landed, not even alpha


def test_write_run_refuses_a_conflicting_later_repository_before_any_write(
        tmp_path):
    # Review (Copilot, #1175): a run directory already holding a CONFLICTING
    # file for a later repository (edited by hand, or mixed from another
    # run) must be refused before the earlier repository is written or a
    # sequence claimed -- not after, which would leave a partial recorded
    # run behind.
    runs = entries_by_repo(catalog.mechanical_entries(extended_inventory()))
    rid, source = catalog.write_run(tmp_path / "src", DAY, runs, TAXONOMY)
    run_dir = runs_root(tmp_path / "agg") / DAY_STR / rid
    run_dir.mkdir(parents=True)
    tampered = source["openxFactory"].read_bytes() + b" "
    (run_dir / "openxFactory.yaml").write_bytes(tampered)  # sorts after alpha
    with pytest.raises(catalog.CatalogError, match="immutable"):
        catalog.write_run(tmp_path / "agg", DAY, runs, TAXONOMY)
    assert sorted(p.name for p in run_dir.iterdir()) == ["openxFactory.yaml"]
    assert (run_dir / "openxFactory.yaml").read_bytes() == tampered
    assert not (runs_root(tmp_path / "agg") / ".sequence").exists()
    assert catalog.load_snapshot(tmp_path / "agg") is None


def test_write_run_refuses_occupied_run_paths_before_any_write(tmp_path):
    # Review (Copilot, #1175): a node the run would never write -- a
    # directory at a snapshot or run.yaml path, a file where the run, date,
    # or a slash-separated repository's directory goes, or (round 5) where
    # the claims directory or any catalog directory above the date goes --
    # must be refused as a controlled CatalogError before the first write,
    # never surface as a filesystem error after a sequence was claimed.
    alpha = alpha_entries(extended_inventory())
    runs = {"alpha": alpha, "xFactories/MedxFactory": [
        dict(e, repo="xFactories/MedxFactory") for e in alpha]}
    rid = catalog.run_id(runs, TAXONOMY)

    def as_file(path):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("occupied\n", encoding="utf-8")

    # run.parents: [0] the date directory, [1] runs, [2] document-catalog,
    # [3] health.
    cases = {
        "snapshot-is-a-directory": lambda run: (
            run / "xFactories" / "MedxFactory.yaml").mkdir(parents=True),
        "run-yaml-is-a-directory": lambda run: (
            run / "run.yaml").mkdir(parents=True),
        "repository-subdirectory-is-a-file": lambda run: as_file(
            run / "xFactories"),
        "run-directory-is-a-file": as_file,
        "date-directory-is-a-file": lambda run: as_file(run.parent),
        "sequence-directory-is-a-file": lambda run: as_file(
            run.parents[1] / ".sequence"),
        "runs-directory-is-a-file": lambda run: as_file(run.parents[1]),
        "catalog-directory-is-a-file": lambda run: as_file(run.parents[2]),
        "health-directory-is-a-file": lambda run: as_file(run.parents[3]),
    }
    for name, occupy in cases.items():
        root = tmp_path / name
        run_dir = runs_root(root) / DAY_STR / rid
        occupy(run_dir)
        before = tree_state(root)
        with pytest.raises(catalog.CatalogError, match="occupied"):
            catalog.write_run(root, DAY, runs, TAXONOMY)
        assert tree_state(root) == before, name  # no claim, no snapshot
        assert not (run_dir / "alpha.yaml").exists(), name
        assert catalog.load_snapshot(root) is None, name


def test_write_run_refuses_symlinked_paths_before_any_write(tmp_path):
    # Review round 5 (Copilot, #1175): is_dir() and is_file() follow
    # symlinks. A symlinked catalog directory passed the preflight and
    # carried the run's writes and claims out of health/document-catalog/
    # runs, and a snapshot or run.yaml linked to an outside file holding
    # the recorded bytes was accepted as a completed no-op, leaving the run
    # with records that stay mutable from outside it. The writer never
    # follows a symlink at any depth from the root down, or inside an
    # existing run. That holds for a dangling link and for one pointing
    # back inside the tree, too.
    alpha = alpha_entries(extended_inventory())
    runs = {"alpha": alpha, "xFactories/MedxFactory": [
        dict(e, repo="xFactories/MedxFactory") for e in alpha]}
    rid, recorded = catalog.write_run(tmp_path / "src", DAY, runs, TAXONOMY)
    recorded_meta = (runs_root(tmp_path / "src") / DAY_STR / rid /
                     "run.yaml").read_bytes()

    def link_dir(node, outside):
        node.parent.mkdir(parents=True, exist_ok=True)
        node.symlink_to(outside, target_is_directory=True)

    def link_file(node, outside, content):
        outside_file = outside / node.name
        if content is not None:
            outside_file.write_bytes(content)
        node.unlink()
        node.symlink_to(outside_file)

    # Directory cases start from an empty tree; file cases from a complete
    # copy of the recorded run, so only the link stands between the retry
    # and a completed no-op. The root itself counts (round 6): a symlinked
    # root must not carry the claims and snapshots somewhere else.
    dir_cases = {
        "root": lambda root: root,
        "health": lambda root: root / "health",
        "document-catalog": lambda root: root / "health" / "document-catalog",
        "runs": runs_root,
        "sequence": lambda root: runs_root(root) / ".sequence",
        "date": lambda root: runs_root(root) / DAY_STR,
        "run": lambda root: runs_root(root) / DAY_STR / rid,
        "repository-subdirectory": lambda root: (
            runs_root(root) / DAY_STR / rid / "xFactories"),
    }
    file_cases = {
        "snapshot-to-recorded-bytes": ("alpha.yaml",
                                       recorded["alpha"].read_bytes()),
        "run-yaml-to-recorded-bytes": ("run.yaml", recorded_meta),
        "run-yaml-dangling": ("run.yaml", None),
    }
    cases = [(f"{name}-directory", "directory", node)
             for name, node in dir_cases.items()]
    cases += [(name, "file", spec) for name, spec in file_cases.items()]
    cases += [("date-directory-inside-the-tree", "inside-the-tree", None),
              ("link-inside-a-recorded-run", "inside-the-run", None)]
    for name, kind, spec in cases:
        root, outside = tmp_path / name, tmp_path / f"{name}-outside"
        outside.mkdir()
        run_dir = runs_root(root) / DAY_STR / rid
        if kind == "directory":
            link_dir(spec(root), outside)
        elif kind == "file":
            shutil.copytree(tmp_path / "src", root, symlinks=True)
            link_file(run_dir / spec[0], outside, spec[1])
        elif kind == "inside-the-tree":  # to a real catalog directory
            real = runs_root(root) / "2026-07-01"
            real.mkdir(parents=True)
            link_dir(runs_root(root) / DAY_STR, real)
        else:  # a linked directory inside an otherwise complete run, which
            # Path.rglob would silently skip (round 6)
            shutil.copytree(tmp_path / "src", root, symlinks=True)
            (outside / "stray.yaml").write_bytes(
                recorded["alpha"].read_bytes())
            link_dir(run_dir / "linked", outside)
        before, before_outside = tree_state(root), tree_state(outside)
        with pytest.raises(catalog.CatalogError, match="symlink"):
            catalog.write_run(root, DAY, runs, TAXONOMY)
        if name in ("root-directory", "run-directory",
                    "snapshot-to-recorded-bytes"):
            with pytest.raises(catalog.CatalogError, match="symlink"):
                catalog.write_snapshot(root, DAY, rid, "alpha", alpha,
                                       TAXONOMY)
        assert tree_state(root) == before, name  # no claim, no snapshot
        assert tree_state(outside) == before_outside, name


def test_overlapping_identical_runs_both_complete(tmp_path, monkeypatch):
    # Review round 7 (Copilot, #1175): two identical write_run calls that
    # overlap after the preflight each claim a sequence, and the writer that
    # reaches its run.yaml step second finds the other one's record.
    # _recorded holds that record to its OWN sequence and that sequence's
    # claim, both of which name this run. It never compares them with the
    # caller's sequence, so the later writer completes as a no-op instead of
    # refusing. Its claim stays orphaned and keeps its number, exactly as a
    # crashed run's claim does.
    runs = entries_by_repo(catalog.mechanical_entries(extended_inventory()))
    real_claim = catalog._claim_sequence
    interleaved = []

    def claim_then_let_the_other_writer_finish(root, day, rid):
        sequence = real_claim(root, day, rid)
        if not interleaved:  # the first writer, just past its claim
            interleaved.append(sequence)
            catalog.write_run(root, day, runs, TAXONOMY)  # start to finish
        return sequence

    monkeypatch.setattr(catalog, "_claim_sequence",
                        claim_then_let_the_other_writer_finish)
    rid, paths = catalog.write_run(tmp_path, DAY, runs, TAXONOMY)
    assert interleaved == [1]
    run_dir = runs_root(tmp_path) / DAY_STR / rid
    meta = json.loads((run_dir / "run.yaml").read_text(encoding="utf-8"))
    assert meta["sequence"] == 2  # the other writer recorded first
    claims = runs_root(tmp_path) / ".sequence"
    assert [json.loads(p.read_text(encoding="utf-8"))["run_id"]
            for p in sorted(claims.iterdir())] == [rid, rid]  # 1 orphaned
    latest = catalog.load_snapshot(tmp_path)
    assert (latest["run_id"], latest["sequence"]) == (rid, 2)
    assert catalog.run_id_scheme(rid, latest["repos"],
                                 catalog._load_run_bytes(run_dir)) == \
        catalog.CONTENT_ADDRESSED


def test_write_snapshot_never_adds_to_a_complete_run(tmp_path):
    # Review round 8 (Copilot, #1175): once run.yaml existed, write_snapshot
    # wrote any missing target. A caller could record a content-addressed id
    # for one repository and then append another under the same id,
    # mutating a closed run into mixed content. A run whose recorded
    # snapshots already make up the content its id addresses is complete,
    # and it refuses additions. A partial run (crashed between its first
    # snapshot and its last) is still completed by a retry.
    runs = entries_by_repo(catalog.mechanical_entries(extended_inventory()))
    rid_one, _ = catalog.write_run(tmp_path / "closed", DAY,
                                   {"alpha": runs["alpha"]}, TAXONOMY)
    before = tree_state(tmp_path / "closed")
    with pytest.raises(catalog.CatalogError, match="complete"):
        catalog.write_snapshot(tmp_path / "closed", DAY, rid_one,
                               "openxFactory", runs["openxFactory"],
                               TAXONOMY)
    assert tree_state(tmp_path / "closed") == before
    closed = catalog.load_snapshot(tmp_path / "closed")
    assert catalog.run_id_scheme(rid_one, closed["repos"],
                                 catalog._load_run_bytes(
                                     runs_root(tmp_path / "closed") /
                                     DAY_STR / rid_one)) == \
        catalog.CONTENT_ADDRESSED
    # The crash window: the full run's first snapshot and run.yaml landed,
    # the second never did. The same content's retry completes it.
    rid = catalog.run_id(runs, TAXONOMY)
    catalog.write_snapshot(tmp_path / "partial", DAY, rid, "alpha",
                           runs["alpha"], TAXONOMY)
    assert catalog.load_snapshot(tmp_path / "partial")["repos"].keys() == \
        {"alpha"}
    assert catalog.write_run(tmp_path / "partial", DAY, runs, TAXONOMY)[0] \
        == rid
    healed = catalog.load_snapshot(tmp_path / "partial")
    assert healed["repos"].keys() == {"alpha", "openxFactory"}
    assert catalog.run_id_scheme(rid, healed["repos"], catalog._load_run_bytes(
        runs_root(tmp_path / "partial") / DAY_STR / rid)) == \
        catalog.CONTENT_ADDRESSED


def test_write_snapshot_never_heals_a_partial_run_around_a_link(tmp_path):
    # Review round 9 (Copilot, #1175): write_snapshot checked only its own
    # target's path. A partial run holding an unrelated symlink was still
    # completed and closed: its missing snapshot was written, and an
    # unrecorded run was also claimed and given its run.yaml. That left a
    # closed run holding a link, which a linked directory can use to hide
    # files from _snapshot_files. Healing refuses a run with a link anywhere
    # inside it, as write_run does.
    runs = entries_by_repo(catalog.mechanical_entries(extended_inventory()))
    rid = catalog.run_id(runs, TAXONOMY)
    for recorded in (False, True):
        root = tmp_path / f"recorded-{recorded}"
        catalog.write_snapshot(root, DAY, rid, "alpha", runs["alpha"],
                               TAXONOMY)  # the crash window: alpha only
        run_dir = runs_root(root) / DAY_STR / rid
        if not recorded:
            (run_dir / "run.yaml").unlink()
        outside = tmp_path / f"outside-{recorded}"
        outside.mkdir()
        (run_dir / "linked").symlink_to(outside, target_is_directory=True)
        before = tree_state(root)
        with pytest.raises(catalog.CatalogError, match="symlink"):
            catalog.write_snapshot(root, DAY, rid, "openxFactory",
                                   runs["openxFactory"], TAXONOMY)
        assert tree_state(root) == before, recorded  # no claim, no write
        assert not (run_dir / "openxFactory.yaml").exists(), recorded
        assert tree_state(outside) == {}, recorded


def test_a_foreign_sequence_claim_node_is_refused_before_claiming(tmp_path):
    # Review round 7 (Copilot, #1175): the claim scan skipped a claim-named
    # node that was not a regular file. The O_EXCL open then collided with a
    # directory or a dangling link at that number forever, and the scan
    # followed a symlinked claim to import an outside sequence and date.
    # Each is now refused before anything is claimed or written.
    runs = entries_by_repo(catalog.mechanical_entries(extended_inventory()))
    outside = tmp_path / "outside"
    outside.mkdir()
    (outside / "claim.yaml").write_text(catalog.render(
        catalog._claim_document(1, "2026-07-01", "f" * 64)),
        encoding="utf-8")
    cases = {
        "directory": lambda claim: claim.mkdir(),
        "dangling-symlink": lambda claim: claim.symlink_to(
            outside / "missing.yaml"),
        "symlink-to-a-claim": lambda claim: claim.symlink_to(
            outside / "claim.yaml"),
    }
    for name, plant in cases.items():
        root = tmp_path / name
        claims = runs_root(root) / ".sequence"
        claims.mkdir(parents=True)
        plant(claims / "000001.yaml")
        before = tree_state(root)
        outcome = []

        def attempt():
            try:
                catalog.write_run(root, DAY, runs, TAXONOMY)
                outcome.append("recorded")
            except catalog.CatalogError as exc:
                outcome.append(str(exc))

        writer = threading.Thread(target=attempt, daemon=True)
        writer.start()
        writer.join(10)
        assert not writer.is_alive(), f"{name}: the claim loop never ended"
        assert outcome and "000001.yaml" in outcome[0], (name, outcome)
        assert "symlink" in outcome[0] or "occupied" in outcome[0], name
        assert tree_state(root) == before, name  # nothing claimed
        assert not (runs_root(root) / DAY_STR).exists(), name


def test_write_run_refuses_a_snapshot_the_run_does_not_record(tmp_path):
    # Review round 6 (Copilot, #1175): the preflight compared only the
    # repositories this call records. A run directory also holding a
    # stranger's snapshot, for another repository or mixed in from another
    # run, passed as a completed no-op. Crashed before its run.yaml, the run
    # was even completed around the stranger. Either way the closed run
    # held a file the run-identity check reads as mixed content.
    alpha = alpha_entries(extended_inventory())
    runs = {"alpha": alpha, "xFactories/MedxFactory": [
        dict(e, repo="xFactories/MedxFactory") for e in alpha]}
    rid, recorded = catalog.write_run(tmp_path / "src", DAY, runs, TAXONOMY)
    stranger = recorded["alpha"].read_bytes()
    cases = {
        "top-level": ("zeta.yaml",),
        "nested": ("xFactories", "Extra.yaml"),
        "crashed-run": ("zeta.yaml",),  # run.yaml removed below
    }
    for name, rel in cases.items():
        root = tmp_path / name
        shutil.copytree(tmp_path / "src", root)
        run_dir = runs_root(root) / DAY_STR / rid
        run_dir.joinpath(*rel).write_bytes(stranger)
        if name == "crashed-run":
            (run_dir / "run.yaml").unlink()
        before = tree_state(root)
        with pytest.raises(catalog.CatalogError, match="does not record"):
            catalog.write_run(root, DAY, runs, TAXONOMY)
        assert tree_state(root) == before, name  # no claim, no run.yaml


def test_write_run_refuses_edited_run_metadata_before_any_write(tmp_path):
    # Review round 5 (Copilot, #1175): a regular but edited run.yaml passed
    # as a completed run. A retry over a run whose snapshots all matched
    # returned without reading it, and a retry over a run missing a
    # snapshot wrote that snapshot under the edited record without
    # claiming. load_snapshot then ordered the run by whatever sequence the
    # file stated. An existing run.yaml must be exactly this run's record
    # (its id, its date, a positive integer sequence, byte for byte), and
    # its sequence must be a claim this run made.
    runs = entries_by_repo(catalog.mechanical_entries(extended_inventory()))
    rid, recorded = catalog.write_run(tmp_path / "src", DAY, runs, TAXONOMY)
    meta_rel = ("health", "document-catalog", "runs", DAY_STR, rid,
                "run.yaml")
    claim_rel = ("health", "document-catalog", "runs", ".sequence",
                 "000001.yaml")
    meta = json.loads((tmp_path / "src").joinpath(*meta_rel)
                      .read_text(encoding="utf-8"))
    assert meta == {"schema_version": 1,
                    "kind": "xfactory_document_catalog_run",
                    "status": "record", "run_id": rid, "as_of": DAY_STR,
                    "sequence": 1}

    def canonical(**changes):
        return catalog.render(dict(meta, **changes)).encode("utf-8")

    claim = json.loads((tmp_path / "src").joinpath(*claim_rel)
                       .read_text(encoding="utf-8"))
    edits = {
        "wrong-run-id": (meta_rel, canonical(run_id="f" * 64)),
        "wrong-date": (meta_rel, canonical(as_of="2026-07-10")),
        "string-sequence": (meta_rel, canonical(sequence="1")),
        "boolean-sequence": (meta_rel, canonical(sequence=True)),
        "zero-sequence": (meta_rel, canonical(sequence=0)),
        "unclaimed-sequence": (meta_rel, canonical(sequence=7)),
        "extra-field": (meta_rel, canonical(note="edited")),
        "compact-reserialization": (
            meta_rel, json.dumps(meta, sort_keys=True).encode("utf-8")),
        "crlf-line-endings": (meta_rel,
                              canonical().replace(b"\n", b"\r\n")),
        "not-json": (meta_rel, b"sequence: 1\n"),
        "not-an-object": (meta_rel, b"[]\n"),
        "claim-names-another-run": (claim_rel, catalog.render(
            dict(claim, run_id="f" * 64)).encode("utf-8")),
        "claim-missing": (claim_rel, None),
    }
    # The untouched copy is a completed no-op, so each refusal below is the
    # edit's doing.
    shutil.copytree(tmp_path / "src", tmp_path / "control")
    before = tree_state(tmp_path / "control")
    assert catalog.write_run(tmp_path / "control", DAY, runs, TAXONOMY)[0] \
        == rid
    assert tree_state(tmp_path / "control") == before
    for name, (rel, content) in edits.items():
        for missing_snapshot in (False, True):
            root = tmp_path / f"{name}-{missing_snapshot}"
            shutil.copytree(tmp_path / "src", root)
            if content is None:
                root.joinpath(*rel).unlink()
            else:
                root.joinpath(*rel).write_bytes(content)
            if missing_snapshot:
                (runs_root(root) / DAY_STR / rid / "openxFactory.yaml") \
                    .unlink()
            before = tree_state(root)
            with pytest.raises(catalog.CatalogError,
                               match="catalog run metadata"):
                catalog.write_run(root, DAY, runs, TAXONOMY)
            with pytest.raises(catalog.CatalogError,
                               match="catalog run metadata"):
                catalog.write_snapshot(root, DAY, rid, "alpha",
                                       runs["alpha"], TAXONOMY)
            assert tree_state(root) == before, (name, missing_snapshot)


def test_a_line_ending_edit_is_never_a_completed_noop(tmp_path):
    # Review (Copilot, #1175): the existing-file checks compare RAW bytes.
    # A text-mode read translates CRLF back to LF, so a retry over a
    # CRLF-edited snapshot used to return as a completed no-op.
    runs = entries_by_repo(catalog.mechanical_entries(extended_inventory()))
    rid, paths = catalog.write_run(tmp_path, DAY, runs, TAXONOMY)
    for path in paths.values():  # the writer lands exactly render()'s bytes
        raw = path.read_bytes()
        assert raw == catalog.render(json.loads(raw)).encode("utf-8")
        assert b"\r" not in raw
    edited = paths["alpha"].read_bytes().replace(b"\n", b"\r\n")
    paths["alpha"].write_bytes(edited)
    with pytest.raises(catalog.CatalogError, match="immutable"):
        catalog.write_run(tmp_path, DAY, runs, TAXONOMY)
    with pytest.raises(catalog.CatalogError, match="immutable"):
        catalog.write_snapshot(tmp_path, DAY, rid, "alpha", runs["alpha"],
                               TAXONOMY)
    assert paths["alpha"].read_bytes() == edited  # refused, never rewritten


# --- snapshots: immutable dated run paths (T007) -----------------------------

def test_write_snapshot_creates_immutable_dated_run(tmp_path):
    root = tmp_path / "agg"
    inv = extended_inventory()
    rid, paths = write_run(root, inv)
    run_dir = runs_root(root) / DAY_STR / rid
    assert sorted(paths) == ["alpha", "openxFactory"]
    for repo, path in paths.items():
        assert path == run_dir / f"{repo}.yaml"
        doc = json.loads(path.read_text(encoding="utf-8"))
        assert set(doc) == {"schema_version", "kind", "status", "run",
                            "taxonomy", "entries"}
        assert doc["status"] == "record"
        assert doc["kind"] == "xfactory_document_catalog"
        assert doc["run"]["run_id"] == rid
        assert doc["run"]["repository"] == repo
        assert doc["run"]["repository_revision"] == HEADS[repo]
        assert doc["run"]["inventory_snapshot_id"] == \
            inventory.snapshot_id(inv)
        # Contract: every snapshot records the effective taxonomy digest
        # plus the ordered pinned-registry inputs with provenance.
        assert doc["taxonomy"] == TAXONOMY
        assert [tuple(sorted(i)) for i in doc["taxonomy"]["inputs"]] == \
            [tuple(sorted(catalog.TAXONOMY_INPUT_FIELDS))] * 2
        assert all(set(e) == ENTRY_KEYS for e in doc["entries"])
    # Acceptance 1: one entry per governed document across the run.
    written = [e for repo in sorted(paths)
               for e in json.loads(
                   paths[repo].read_text(encoding="utf-8"))["entries"]]
    assert by_key(written).keys() == by_key(inv).keys()
    meta = json.loads((run_dir / "run.yaml").read_text(encoding="utf-8"))
    assert meta == {"schema_version": 1,
                    "kind": "xfactory_document_catalog_run",
                    "status": "record", "run_id": rid,
                    "as_of": DAY_STR, "sequence": 1}
    # The claimed sequence record exists and matches the run.
    claim = json.loads((runs_root(root) / ".sequence" / "000001.yaml")
                       .read_text(encoding="utf-8"))
    assert (claim["run_id"], claim["as_of"], claim["sequence"]) == \
        (rid, DAY_STR, 1)


def test_as_of_rejects_datetime_instances(tmp_path):
    # datetime is a date subclass; a naive isinstance(as_of, date) check
    # would accept it and emit a run directory outside YYYY-MM-DD
    # (isoformat() on a datetime includes a time component).
    root = tmp_path / "agg"
    alpha = alpha_entries(extended_inventory())
    rid = catalog.run_id({"alpha": alpha}, TAXONOMY)
    bad_as_of = datetime(2026, 7, 9, 12, 30)
    with pytest.raises(ValueError, match="datetime"):
        catalog.write_snapshot(root, bad_as_of, rid, "alpha", alpha, TAXONOMY)
    with pytest.raises(ValueError, match="datetime"):
        catalog.load_snapshot(root, as_of=bad_as_of)
    assert not runs_root(root).exists()


def test_snapshots_require_complete_taxonomy_provenance(tmp_path):
    # Contract scenario "Taxonomy inputs are incomplete": a snapshot
    # lacking the digest or an ordered pinned-registry input is refused.
    root = tmp_path / "agg"
    alpha = alpha_entries(extended_inventory())
    rid = catalog.run_id({"alpha": alpha}, TAXONOMY)
    for bad in (None, {}, {"digest": TAXONOMY["digest"]},
                {"digest": TAXONOMY["digest"], "inputs": []},
                {"inputs": TAXONOMY["inputs"]}):
        with pytest.raises(ValueError):
            catalog.write_snapshot(root, DAY, rid, "alpha", alpha, bad)
    stripped = [{k: v for k, v in i.items() if k != "registry_revision"}
                for i in TAXONOMY["inputs"]]
    with pytest.raises(ValueError, match="incomplete"):
        catalog.write_snapshot(root, DAY, rid, "alpha", alpha,
                               {"digest": TAXONOMY["digest"],
                                "inputs": stripped})
    # A digest that does not match its inputs is refused too.
    with pytest.raises(ValueError, match="digest"):
        catalog.write_snapshot(root, DAY, rid, "alpha", alpha,
                               {"digest": "0" * 64,
                                "inputs": TAXONOMY["inputs"]})
    assert not (root / "health").exists()  # nothing landed


def test_snapshot_rendering_is_byte_identical_for_identical_corpus(tmp_path):
    # Acceptance 2: unchanged corpus -> byte-identical rendered
    # snapshots (D3: sorted keys, fixed indent, trailing newline).
    inv = extended_inventory()
    _, first = write_run(tmp_path / "one", inv)
    _, second = write_run(tmp_path / "two", extended_inventory())
    for repo in first:
        one, two = first[repo].read_bytes(), second[repo].read_bytes()
        assert one == two
        assert one.endswith(b"\n") and b"\r" not in one
        text = one.decode("utf-8")
        assert text == json.dumps(json.loads(text), indent=2,
                                  sort_keys=True) + "\n"


def test_identical_content_rerun_is_a_completed_noop(tmp_path):
    # Acceptance 5: a second run over identical content collapses into
    # the same immutable run directory without rewriting anything.
    root = tmp_path / "agg"
    inv = extended_inventory()
    rid, paths = write_run(root, inv)
    before = {repo: p.read_bytes() for repo, p in paths.items()}
    rid_again, paths_again = write_run(root, extended_inventory())
    assert rid_again == rid
    assert paths_again == paths
    assert {repo: p.read_bytes() for repo, p in paths_again.items()} == before
    # The completed no-op claimed no second sequence.
    assert catalog.load_snapshot(root)["sequence"] == 1
    assert sorted(p.name for p in (runs_root(root) / ".sequence")
                  .iterdir()) == ["000001.yaml"]
    # An interrupted run completes idempotently: a missing repo file is
    # rewritten with the identical bytes.
    paths["alpha"].unlink()
    _, completed = write_run(root, extended_inventory())
    assert completed["alpha"].read_bytes() == before["alpha"]


def test_conflicting_rewrite_of_an_existing_snapshot_is_refused(tmp_path):
    root = tmp_path / "agg"
    inv = extended_inventory()
    rid, _ = write_run(root, inv)
    entries = catalog.mechanical_entries(inv)
    alpha = [dict(e) for e in entries if e["repo"] == "alpha"]
    alpha[0]["status"] = "tampered"
    with pytest.raises(catalog.CatalogError, match="immutable"):
        catalog.write_snapshot(root, DAY, rid, "alpha", alpha, TAXONOMY)


def test_taxonomy_change_is_a_new_run_not_a_conflict(tmp_path):
    # A registry change over an unchanged corpus lands as a new
    # immutable run — never a conflicting rewrite, and reclassification
    # invalidation keys to the new digest.
    root = tmp_path / "agg"
    ws = mutated_workspace(tmp_path)
    inv = extended_inventory(ws, HEADS)
    rid_one, _ = write_run(root, inv, taxonomy=taxonomy_for(ws, HEADS))
    registry = ws / "alpha" / REGISTRY_PATHS["alpha"]
    registry.write_text(
        registry.read_text(encoding="utf-8").replace(
            "registry_version: 1", "registry_version: 2"),
        encoding="utf-8")
    assert extended_inventory(ws, HEADS) == inv  # corpus unchanged
    changed = taxonomy_for(ws, HEADS)
    assert changed["digest"] != TAXONOMY["digest"]
    rid_two, _ = write_run(root, inv, taxonomy=changed)
    assert rid_two != rid_one
    day_dir = runs_root(root) / DAY_STR
    assert sorted(p.name for p in day_dir.iterdir()) == \
        sorted([rid_one, rid_two])
    latest = catalog.load_snapshot(root)
    assert (latest["run_id"], latest["sequence"]) == (rid_two, 2)
    assert latest["repos"]["alpha"]["taxonomy"]["digest"] == \
        changed["digest"]


def test_stale_run_cannot_land_after_a_newer_one(tmp_path):
    # Acceptance 5: a snapshot derived from an older corpus date is
    # refused once a newer run is recorded — before anything lands.
    root = tmp_path / "agg"
    write_run(root, extended_inventory())
    stale_inv = extended_inventory(WORKSPACE, LATER_HEADS)
    with pytest.raises(catalog.CatalogError, match="stale"):
        write_run(root, stale_inv, as_of="2026-07-08")
    assert not (runs_root(root) / "2026-07-08").exists()
    # No stale sequence claim was created either.
    assert sorted(p.name for p in (runs_root(root) / ".sequence")
                  .iterdir()) == ["000001.yaml"]


def test_sequence_numbers_are_claimed_atomically_and_uniquely(tmp_path):
    # A racing run owns its number the instant its claim file exists —
    # even before the claim content or its run.yaml lands — so two
    # concurrent runs can never record the same sequence and "latest"
    # is never a lexicographic tie-break.
    root = tmp_path / "agg"
    claims = runs_root(root) / ".sequence"
    claims.mkdir(parents=True)
    (claims / "000001.yaml").write_text("", encoding="utf-8")  # in flight
    rid, _ = write_run(root, extended_inventory())
    meta = json.loads((runs_root(root) / DAY_STR / rid / "run.yaml")
                      .read_text(encoding="utf-8"))
    assert meta["sequence"] == 2
    assert catalog.load_snapshot(root)["sequence"] == 2


def test_claimed_newer_run_blocks_stale_dated_writes(tmp_path):
    # The stale refusal sees claimed runs whose run.yaml has not landed
    # yet: a newer-dated claim alone is enough to refuse an older date.
    root = tmp_path / "agg"
    claims = runs_root(root) / ".sequence"
    claims.mkdir(parents=True)
    (claims / "000001.yaml").write_text(json.dumps({
        "schema_version": 1,
        "kind": "xfactory_document_catalog_sequence_claim",
        "status": "record", "sequence": 1, "as_of": "2026-07-10",
        "run_id": "f" * 64}, indent=2, sort_keys=True) + "\n",
        encoding="utf-8")
    with pytest.raises(catalog.CatalogError, match="stale"):
        write_run(root, extended_inventory())  # DAY < claimed 2026-07-10
    assert not (runs_root(root) / DAY_STR).exists()


def test_crashed_run_directories_are_not_recorded_runs(tmp_path):
    # A run that crashed after creating its directory but before
    # recording run.yaml is invisible: it is never "latest" (no empty
    # repos == {} result), never blocks newer work, and heals on retry.
    root = tmp_path / "agg"
    rid_one, _ = write_run(root, extended_inventory())
    ghost = runs_root(root) / "2026-07-10" / ("e" * 64)
    ghost.mkdir(parents=True)
    latest = catalog.load_snapshot(root)
    assert (latest["run_id"], latest["sequence"]) == (rid_one, 1)
    assert latest["repos"]  # never an empty ghost result
    assert catalog.load_snapshot(root, run_id="e" * 64) is None
    # The unrecorded directory does not stale-block a run dated before
    # its directory name.
    ws = mutated_workspace(tmp_path)
    (ws / "alpha" / "docs" / "late-addition.md").write_text(
        "Status: draft\n\nLanded after the crash.\n", encoding="utf-8")
    rid_two, _ = write_run(root, extended_inventory(ws, LATER_HEADS))
    assert catalog.load_snapshot(root)["run_id"] == rid_two


def test_interrupted_run_heals_with_a_fresh_sequence(tmp_path):
    # Crash window: sequence claimed and run dir created, but neither
    # run.yaml nor a snapshot landed. A retry re-claims and records.
    root = tmp_path / "agg"
    inv = extended_inventory()
    rid = catalog.run_id(entries_by_repo(catalog.mechanical_entries(inv)),
                         TAXONOMY)
    claims = runs_root(root) / ".sequence"
    claims.mkdir(parents=True)
    (claims / "000001.yaml").write_text(json.dumps({
        "schema_version": 1,
        "kind": "xfactory_document_catalog_sequence_claim",
        "status": "record", "sequence": 1, "as_of": DAY_STR,
        "run_id": rid}, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    (runs_root(root) / DAY_STR / rid).mkdir(parents=True)
    assert catalog.load_snapshot(root) is None  # not recorded yet
    rid_again, paths = write_run(root, inv)
    assert rid_again == rid
    latest = catalog.load_snapshot(root)
    assert latest["sequence"] == 2  # fresh claim; orphan stays orphaned
    assert sorted(latest["repos"]) == ["alpha", "openxFactory"]
    assert {r: p.read_bytes() for r, p in paths.items()}  # snapshots landed


def test_same_day_runs_keep_run_scoped_paths(tmp_path):
    root = tmp_path / "agg"
    ws = mutated_workspace(tmp_path)
    rid_one, _ = write_run(root, extended_inventory(ws, HEADS))
    (ws / "alpha" / "docs" / "late-addition.md").write_text(
        "Status: draft\n\nLanded between runs.\n", encoding="utf-8")
    rid_two, _ = write_run(root, extended_inventory(ws, LATER_HEADS))
    assert rid_one != rid_two
    day_dir = runs_root(root) / DAY_STR
    assert sorted(p.name for p in day_dir.iterdir()) == \
        sorted([rid_one, rid_two])
    # The later run is the latest by recorded sequence, and the earlier
    # run's snapshots survive untouched.
    latest = catalog.load_snapshot(root)
    assert latest["run_id"] == rid_two and latest["sequence"] == 2
    assert catalog.load_snapshot(root, run_id=rid_one)["sequence"] == 1


def test_load_snapshot_latest_and_specific(tmp_path):
    root = tmp_path / "agg"
    assert catalog.load_snapshot(root) is None
    ws = mutated_workspace(tmp_path)
    rid_one, _ = write_run(root, extended_inventory(ws, HEADS))
    (ws / "alpha" / "docs" / "day-two.md").write_text(
        "Status: draft\n\nNext-day doc.\n", encoding="utf-8")
    rid_two, _ = write_run(root, extended_inventory(ws, LATER_HEADS),
                           as_of="2026-07-10")
    latest = catalog.load_snapshot(root)
    assert (latest["run_id"], latest["as_of"]) == (rid_two, "2026-07-10")
    assert sorted(latest["repos"]) == ["alpha", "openxFactory"]
    assert ("alpha", "docs/day-two.md") in by_key(
        latest["repos"]["alpha"]["entries"])
    specific = catalog.load_snapshot(root, as_of=DAY, run_id=rid_one)
    assert specific["run_id"] == rid_one
    assert ("alpha", "docs/day-two.md") not in by_key(
        specific["repos"]["alpha"]["entries"])
    assert catalog.load_snapshot(root, as_of=DAY)["run_id"] == rid_one
    assert catalog.load_snapshot(root, run_id="0" * 64) is None
    # Loaded latest entries diff cleanly against the prior run.
    d = catalog.diff(specific["repos"]["alpha"]["entries"],
                     latest["repos"]["alpha"]["entries"])
    assert d.added_keys == (("alpha", "docs/day-two.md"),)


def test_slash_separated_repo_ids_become_subdirectories(tmp_path):
    root = tmp_path / "agg"
    inv = extended_inventory()
    entries = [dict(e, repo="xFactories/MedxFactory")
               for e in catalog.mechanical_entries(inv)
               if e["repo"] == "alpha"]
    rid = catalog.run_id({"xFactories/MedxFactory": entries}, TAXONOMY)
    path = catalog.write_snapshot(root, DAY, rid, "xFactories/MedxFactory",
                                  entries, TAXONOMY)
    assert path == (runs_root(root) / DAY_STR / rid
                    / "xFactories" / "MedxFactory.yaml")
    loaded = catalog.load_snapshot(root)
    assert sorted(loaded["repos"]) == ["xFactories/MedxFactory"]


def test_snapshot_path_boundaries_are_enforced(tmp_path):
    root = tmp_path / "agg"
    alpha = alpha_entries(extended_inventory())
    rid = catalog.run_id({"alpha": alpha}, TAXONOMY)
    for bad_repo in ("", "run", "../alpha", "alpha/../..", ".hidden"):
        with pytest.raises(ValueError):
            catalog.write_snapshot(
                root, DAY, rid, bad_repo,
                [dict(e, repo=bad_repo) for e in alpha], TAXONOMY)
    with pytest.raises(ValueError):
        catalog.write_snapshot(root, DAY, "../escape", "alpha", alpha,
                               TAXONOMY)
    with pytest.raises(ValueError):  # entries must belong to the repo
        catalog.write_snapshot(root, DAY, rid, "openxFactory", alpha,
                               TAXONOMY)


# --- link-safe run scan (opensoft/openxFactory#1187) -------------------------

LATER_DAY_STR = "2026-07-10"


def legacy_iter_runs(root):
    """`catalog._iter_runs` as it stood before opensoft/openxFactory#1187: the
    reference every caller's view of a clean tree must still match."""
    runs = runs_root(root)
    if not runs.is_dir():
        return
    for date_dir in sorted(runs.iterdir()):
        if not date_dir.is_dir() or date_dir.name.startswith("."):
            continue
        for run_dir in sorted(date_dir.iterdir()):
            if not run_dir.is_dir() or run_dir.name.startswith("."):
                continue
            meta_path = run_dir / "run.yaml"
            if not meta_path.is_file():
                continue
            sequence = json.loads(
                meta_path.read_text(encoding="utf-8")).get("sequence", 0)
            yield date_dir.name, sequence, run_dir.name, run_dir


def later_runs():
    """{repo: entries} for the corpus at LATER_HEADS: a content no other run
    in these tests records, so it mints a run id of its own."""
    return entries_by_repo(catalog.mechanical_entries(
        extended_inventory(WORKSPACE, LATER_HEADS)))


def foreign_run(base, as_of=LATER_DAY_STR):
    """The directory of a run recorded in a catalog tree of its own at
    `base`: content that lives outside the tree a link is planted in."""
    rid, _paths = catalog.write_run(base, as_of, later_runs(), TAXONOMY)
    return runs_root(base) / as_of / rid


def plant_link(node, target, directory=True):
    node.parent.mkdir(parents=True, exist_ok=True)
    node.symlink_to(target, target_is_directory=directory)
    return node


def relink_file(node, target):
    """Replace the regular file at `node` with a symlink to `target`."""
    node.unlink()
    return plant_link(node, target, directory=False)


def copy_run(source, run_dir, meta=True):
    """A real run directory holding a copy of `source`'s snapshots, and of
    its run.yaml unless `meta` is False (a test then plants its own)."""
    shutil.copytree(source, run_dir)
    if not meta:
        (run_dir / "run.yaml").unlink()
    return run_dir


def refused(scan):
    return [entry for entry in scan if entry.refusal is not None]


def test_run_scan_matches_the_legacy_scan_on_a_clean_tree(tmp_path):
    # opensoft/openxFactory#1187: making the shared scan link-safe must not
    # change what any caller sees in a tree without links: several days,
    # several runs a day, a slash-separated repository, a crashed run, stray
    # files and a hidden directory. The scan yields exactly the runs, in
    # exactly the order, the scan before #1187 did, and refuses none. The
    # latest-run lookup, the date and id lookups, the next claimed sequence
    # and the stale refusal all follow from those same runs.
    root = tmp_path / "agg"
    rid_one, _ = write_run(root, extended_inventory())
    rid_two, _ = write_run(root, extended_inventory(WORKSPACE, LATER_HEADS))
    alpha = alpha_entries(extended_inventory())
    rid_three, _ = catalog.write_run(root, LATER_DAY_STR, {
        "xFactories/MedxFactory": [dict(e, repo="xFactories/MedxFactory")
                                   for e in alpha]}, TAXONOMY)
    crashed = runs_root(root) / LATER_DAY_STR / ("e" * 64)
    crashed.mkdir()
    (crashed / "alpha.yaml").write_text("{}\n", encoding="utf-8")
    (runs_root(root) / "notes.yaml").write_text("stray\n", encoding="utf-8")
    (runs_root(root) / DAY_STR / "loose.yaml").write_text(
        "stray\n", encoding="utf-8")
    hidden = runs_root(root) / DAY_STR / ".partial"
    hidden.mkdir()
    (hidden / "run.yaml").write_text(catalog.render(
        catalog._run_meta_document(".partial", DAY_STR, 99)),
        encoding="utf-8")

    legacy = list(legacy_iter_runs(root))
    scan = list(catalog._iter_runs(root))
    assert [tuple(entry[:4]) for entry in scan] == legacy
    assert refused(scan) == []
    assert sorted((d, seq, r) for d, seq, r, _dir in legacy) == [
        (DAY_STR, 1, rid_one), (DAY_STR, 2, rid_two),
        (LATER_DAY_STR, 3, rid_three)]

    def latest_of(runs):
        d, seq, r, _dir = max(runs, key=lambda run: (run[0], run[1]))
        return d, seq, r

    latest = catalog.load_snapshot(root)
    assert (latest["as_of"], latest["sequence"], latest["run_id"]) == \
        latest_of(legacy)
    on_day = catalog.load_snapshot(root, as_of=DAY)
    assert (on_day["as_of"], on_day["sequence"], on_day["run_id"]) == \
        latest_of([run for run in legacy if run[0] == DAY_STR])
    assert catalog.load_snapshot(root, run_id=rid_one)["sequence"] == 1
    assert catalog.load_snapshot(root, run_id="e" * 64) is None

    # The writer claims one past every number those runs and their claims
    # hold, and still refuses a run dated before the latest of them.
    claimed = [int(p.stem) for p in (runs_root(root) / ".sequence").iterdir()]
    expected = max([seq for _d, seq, _r, _dir in legacy] + claimed) + 1
    rid_four, paths = catalog.write_run(root, LATER_DAY_STR, {
        "alpha": classified(alpha, "docs/widget-overview.md", "domain")},
        TAXONOMY)
    meta = json.loads((paths["alpha"].parent / "run.yaml")
                      .read_text(encoding="utf-8"))
    assert meta["sequence"] == expected == 4
    assert catalog.load_snapshot(root)["run_id"] == rid_four
    with pytest.raises(catalog.CatalogError, match="stale"):
        write_run(root, extended_inventory(), as_of="2026-07-08")


def test_run_scan_refuses_every_symlink_position_for_that_entry_alone(
        tmp_path):
    # opensoft/openxFactory#1187 (Copilot, round 8 of #1175): the shared scan
    # followed links, because is_dir(), is_file() and the run.yaml read all
    # do. A symlinked day directory, run directory or run.yaml was enumerated,
    # and its run.yaml read, as though it were a recorded run, and a malformed
    # linked run.yaml aborted the scan for every caller. Each is now yielded
    # as a refused entry for that entry alone, and nothing behind the link is
    # read: the foreign run.yaml below is not even JSON. That holds for a link
    # escaping the catalog root, one pointing back inside the tree, and a
    # dangling one. A recorded run holding a link inside it is refused the
    # same way, since a reader of that run would read its snapshots through
    # the link. Every other entry, and the scan's order, is the clean tree's.
    clean = tmp_path / "clean"
    rid, _ = write_run(clean, extended_inventory())
    clean_scan = list(catalog._iter_runs(clean))
    foreign = foreign_run(tmp_path / "foreign")
    (foreign / "run.yaml").write_text("<<not json>>", encoding="utf-8")
    recorded = foreign_run(tmp_path / "foreign-recorded")  # valid run.yaml
    frid = foreign.name

    def day(root):
        return runs_root(root) / DAY_STR

    def day_escaping(root, out):
        return (plant_link(runs_root(root) / LATER_DAY_STR, foreign.parent),
                LATER_DAY_STR, None)

    def day_inside(root, out):
        return (plant_link(runs_root(root) / LATER_DAY_STR, day(root)),
                LATER_DAY_STR, None)

    def day_dangling(root, out):
        return (plant_link(runs_root(root) / LATER_DAY_STR, out / "missing"),
                LATER_DAY_STR, None)

    def run_escaping(root, out):
        return plant_link(day(root) / frid, foreign), DAY_STR, frid

    def run_inside(root, out):
        alias = "f" * 64
        return plant_link(day(root) / alias, day(root) / rid), DAY_STR, alias

    def run_dangling(root, out):
        return plant_link(day(root) / frid, out / "missing"), DAY_STR, frid

    def run_yaml_to(target_of):
        def plant(root, out):
            run = copy_run(recorded, day(root) / frid, meta=False)
            return (plant_link(run / "run.yaml", target_of(root, out),
                               directory=False), DAY_STR, frid)
        return plant

    def snapshot_inside(root, out):
        run = copy_run(recorded, day(root) / frid)
        return (relink_file(run / "alpha.yaml", recorded / "alpha.yaml"),
                DAY_STR, frid)

    def directory_inside(root, out):
        run = copy_run(recorded, day(root) / frid)
        return plant_link(run / "linked", foreign), DAY_STR, frid

    cases = {
        "day-escaping-the-root": day_escaping,
        "day-inside-the-tree": day_inside,
        "day-dangling": day_dangling,
        "run-escaping-the-root": run_escaping,
        "run-inside-the-tree": run_inside,
        "run-dangling": run_dangling,
        "run-yaml-escaping-the-root": run_yaml_to(
            lambda root, out: foreign / "run.yaml"),
        "run-yaml-inside-the-tree": run_yaml_to(
            lambda root, out: day(root) / rid / "run.yaml"),
        "run-yaml-dangling": run_yaml_to(
            lambda root, out: out / "missing.yaml"),
        "snapshot-inside-a-recorded-run": snapshot_inside,
        "directory-inside-a-recorded-run": directory_inside,
    }
    for name, plant in cases.items():
        root, outside = tmp_path / name, tmp_path / f"{name}-outside"
        shutil.copytree(clean, root)
        outside.mkdir()
        node, as_of, run_id = plant(root, outside)
        entry = (as_of, None, run_id,
                 None if run_id is None else runs_root(root) / as_of / run_id)
        # The clean tree's runs, untouched, plus the one refused entry in its
        # sorted place. It carries no sequence: nothing behind it was read.
        expected = sorted(
            [(d, seq, r, root / run_dir.relative_to(clean))
             for d, seq, r, run_dir in (e[:4] for e in clean_scan)] + [entry],
            key=lambda e: (e[0], e[2] or ""))
        scan = list(catalog._iter_runs(root))
        assert [tuple(e[:4]) for e in scan] == expected, name
        bad = refused(scan)
        assert [tuple(e[:4]) for e in bad] == [entry], name
        assert "symlink" in str(bad[0].refusal), name
        assert str(node) in str(bad[0].refusal), name  # names the link itself


def test_run_scan_fails_closed_on_a_directory_it_cannot_list(tmp_path):
    # Review round 2 (Copilot, #1190): the walk inside a recorded run passed
    # no onerror, so os.walk skipped a directory it could not list in
    # silence, and the run was yielded as link-free over a subtree nobody
    # saw: a link below it would evade the refusal. The scan's own walk now
    # fails closed. A directory it cannot list, or an entry it cannot check,
    # refuses that run alone: load_snapshot never selects it, and no
    # sequence is claimed beside it. Readable again, the run is whole.
    alpha = alpha_entries(extended_inventory())
    runs = {"alpha": alpha, "xFactories/MedxFactory": [
        dict(e, repo="xFactories/MedxFactory") for e in alpha]}
    cases = (
        # No read: os.scandir of the directory is denied.
        ("unlistable", 0o100, "could not be listed"),
        # No search: it lists, but what it lists cannot be lstat-ed.
        ("unsearchable", 0o400, "could not be checked"),
    )
    for name, mode, reason in cases:
        root = tmp_path / name
        rid, _ = catalog.write_run(root, DAY, runs, TAXONOMY)
        run_dir = runs_root(root) / DAY_STR / rid
        blocked = run_dir / "xFactories"
        original = blocked.stat().st_mode
        blocked.chmod(mode)
        try:
            scan = list(catalog._iter_runs(root))
            assert [tuple(e[:4]) for e in scan] == [
                (DAY_STR, None, rid, run_dir)], name
            assert reason in str(scan[0].refusal), name
            assert catalog.load_snapshot(root) is None, name
            with pytest.raises(catalog.CatalogError,
                               match="no run sequence is claimed beside"):
                catalog.write_run(root, LATER_DAY_STR, later_runs(),
                                  TAXONOMY)
            assert sorted(p.name for p in (runs_root(root) / ".sequence")
                          .iterdir()) == ["000001.yaml"], name
            assert not (runs_root(root) / LATER_DAY_STR).exists(), name
        finally:
            blocked.chmod(original)  # restore: tmp_path cleanup needs it
        assert catalog.load_snapshot(root)["run_id"] == rid, name


def test_run_scan_never_takes_an_unchecked_node_for_link_free(tmp_path,
                                                               monkeypatch):
    # Review round 3 (Copilot, #1190): from Python 3.13 Path.is_symlink is
    # os.path.islink, which reports a node whose lstat is denied as no link,
    # so a scan built on it passes a child of a listable but unsearchable
    # directory, a link included, as link-free. Python 3.12 raises instead,
    # so it is pinned to the 3.13 behaviour here: the scan must not depend on
    # it. The same holds where the scan meets a day or run directory it
    # cannot list or search. Every node is checked with an explicit lstat,
    # and whatever the scan cannot check or list refuses that entry alone;
    # the runs directory itself refuses the whole scan.
    monkeypatch.setattr(Path, "is_symlink", lambda self: os.path.islink(self))
    alpha = alpha_entries(extended_inventory())
    runs = {"alpha": alpha, "xFactories/MedxFactory": [
        dict(e, repo="xFactories/MedxFactory") for e in alpha]}
    cases = (
        # (name, node to block from the run directory, mode, whether the
        # refused entry is the run or its day, reason)
        ("subdirectory-unsearchable", lambda run: run / "xFactories", 0o400,
         "run", "could not be checked"),
        ("run-directory-unsearchable", lambda run: run, 0o600, "run",
         "could not be checked"),
        ("day-directory-unsearchable", lambda run: run.parent, 0o400, "run",
         "could not be checked"),
        ("day-directory-unlistable", lambda run: run.parent, 0o100, "day",
         "could not be listed"),
    )
    for name, blocked_of, mode, entry, reason in cases:
        root = tmp_path / name
        rid, _ = catalog.write_run(root, DAY, runs, TAXONOMY)
        run_dir = runs_root(root) / DAY_STR / rid
        blocked = blocked_of(run_dir)
        original = blocked.stat().st_mode
        blocked.chmod(mode)
        try:
            scan = list(catalog._iter_runs(root))
            assert [tuple(e[:4]) for e in scan] == [
                (DAY_STR, None, rid, run_dir) if entry == "run"
                else (DAY_STR, None, None, None)], name
            assert reason in str(scan[0].refusal), name
            assert catalog.load_snapshot(root) is None, name
            with pytest.raises(catalog.CatalogError,
                               match="no run sequence is claimed beside"):
                catalog.write_run(root, LATER_DAY_STR, later_runs(),
                                  TAXONOMY)
            assert not (runs_root(root) / LATER_DAY_STR).exists(), name
        finally:
            blocked.chmod(original)  # restore: tmp_path cleanup needs it
        assert catalog.load_snapshot(root)["run_id"] == rid, name
        assert sorted(p.name for p in (runs_root(root) / ".sequence")
                      .iterdir()) == ["000001.yaml"], name  # nothing claimed
    root = tmp_path / "runs-directory-unlistable"
    catalog.write_run(root, DAY, runs, TAXONOMY)
    blocked = runs_root(root)
    original = blocked.stat().st_mode
    blocked.chmod(0o100)
    try:
        with pytest.raises(catalog.CatalogError, match="could not be listed"):
            list(catalog._iter_runs(root))
        with pytest.raises(catalog.CatalogError, match="could not be listed"):
            catalog.load_snapshot(root)
    finally:
        blocked.chmod(original)


def record_followed_links(patch, under):
    """The paths of every symlink at or below `under` whose target a call
    stats while `patch` holds: ``os.stat`` following links, which
    ``Path.is_dir``, ``Path.is_file``, ``Path.exists`` and ``os.path.isdir``
    all reach, and a ``DirEntry`` classified or stat-ed following links, as
    ``os.walk`` classifies every entry it lists (``DirEntry.is_dir``)."""
    followed = []
    real_stat, real_scandir = os.stat, os.scandir
    prefix = os.fspath(under)

    def link_below(path):
        if not isinstance(path, (str, os.PathLike)):
            return False  # a file descriptor: nothing to follow
        path = os.fspath(path)
        return ((path == prefix or path.startswith(prefix + os.sep))
                and os.path.islink(path))

    def tracked_stat(path, *, dir_fd=None, follow_symlinks=True):
        if follow_symlinks and dir_fd is None and link_below(path):
            followed.append(os.fspath(path))
        return real_stat(path, dir_fd=dir_fd, follow_symlinks=follow_symlinks)

    class Entry:
        """A listed entry that records a classification following a link."""

        def __init__(self, entry):
            self._entry, self.name, self.path = entry, entry.name, entry.path

        def __fspath__(self):
            return self.path

        def _record(self, follow_symlinks):
            if follow_symlinks and link_below(self.path):
                followed.append(self.path)

        def is_dir(self, *, follow_symlinks=True):
            self._record(follow_symlinks)
            return self._entry.is_dir(follow_symlinks=follow_symlinks)

        def is_file(self, *, follow_symlinks=True):
            self._record(follow_symlinks)
            return self._entry.is_file(follow_symlinks=follow_symlinks)

        def stat(self, *, follow_symlinks=True):
            self._record(follow_symlinks)
            return self._entry.stat(follow_symlinks=follow_symlinks)

        def is_symlink(self):
            return self._entry.is_symlink()

        def inode(self):
            return self._entry.inode()

    class Listing:
        """An ``os.scandir`` iterator that yields recording entries."""

        def __init__(self, listing):
            self._listing = listing

        def __enter__(self):
            return self

        def __exit__(self, *exc_info):
            self._listing.close()

        def __iter__(self):
            return self

        def __next__(self):
            return Entry(next(self._listing))

        def close(self):
            self._listing.close()

    patch.setattr(os, "stat", tracked_stat)
    patch.setattr(os, "scandir", lambda path=".": Listing(real_scandir(path)))
    return followed


def test_run_scan_never_stats_a_link_target(tmp_path):
    # Review round 4 (Copilot, #1190): the walk inside a recorded run was
    # os.walk, which classifies every entry it lists with DirEntry.is_dir(),
    # and that follows a link to stat its target before the scan's own lstat
    # check sees the link. The walk is now driven by each node's own lstat
    # and descends only into a real directory, so no caller of the scan
    # stats a link's target, wherever the link sits and wherever it points:
    # outside the catalog root, back inside the tree, or nowhere. Each such
    # entry is still refused for that entry alone.
    probe = tmp_path / "probe"
    link = plant_link(probe / "linked", tmp_path)
    with pytest.MonkeyPatch.context() as patch:
        followed = record_followed_links(patch, probe)
        list(os.walk(probe))
        link.is_dir()
    # The recorder sees both ways the old walk stats a link's target.
    assert followed == [str(link), str(link)]

    clean = tmp_path / "clean"
    rid, _ = write_run(clean, extended_inventory())
    recorded = foreign_run(tmp_path / "foreign")
    frid = recorded.name

    def day(root):
        return runs_root(root) / DAY_STR

    def linked_day(root, out):
        return (plant_link(runs_root(root) / LATER_DAY_STR, recorded.parent),
                LATER_DAY_STR, None)

    def linked_run(root, out):
        return plant_link(day(root) / frid, recorded), DAY_STR, frid

    def linked_run_yaml(root, out):
        run = copy_run(recorded, day(root) / frid, meta=False)
        return (plant_link(run / "run.yaml", recorded / "run.yaml",
                           directory=False), DAY_STR, frid)

    def inside(link_at, target_of, directory):
        def plant(root, out):
            run = copy_run(recorded, day(root) / frid)
            node = run / link_at
            if node.is_file():
                node.unlink()  # a snapshot the run records, now a link
            return (plant_link(node, target_of(root, out), directory),
                    DAY_STR, frid)
        return plant

    cases = {
        "day-directory": linked_day,
        "run-directory": linked_run,
        "run-yaml": linked_run_yaml,
        "file-escaping-the-root": inside(
            "alpha.yaml", lambda root, out: recorded / "alpha.yaml", False),
        "file-inside-the-tree": inside(
            "alpha.yaml", lambda root, out: day(root) / rid / "alpha.yaml",
            False),
        "file-dangling": inside(
            "alpha.yaml", lambda root, out: out / "missing.yaml", False),
        "directory-escaping-the-root": inside(
            "linked", lambda root, out: recorded, True),
        "directory-inside-the-tree": inside(
            "linked", lambda root, out: day(root) / rid, True),
        "directory-dangling": inside(
            "linked", lambda root, out: out / "missing", True),
        "below-real-subdirectories": inside(
            "deep/er/linked", lambda root, out: recorded, True),
    }
    for name, plant in cases.items():
        root, outside = tmp_path / name, tmp_path / f"{name}-outside"
        shutil.copytree(clean, root)
        outside.mkdir()
        node, as_of, run_id = plant(root, outside)
        with pytest.MonkeyPatch.context() as patch:
            followed = record_followed_links(patch, root)
            scan = list(catalog._iter_runs(root))
            latest = catalog.load_snapshot(root)
            by_id = catalog.load_snapshot(root, run_id=frid)
            with pytest.raises(catalog.CatalogError,
                               match="no run sequence is claimed beside"):
                catalog._claim_sequence(root, "2026-07-12", frid)
        assert followed == [], name
        bad = refused(scan)
        assert [(e.as_of, e.run_id) for e in bad] == [(as_of, run_id)], name
        assert str(node) in str(bad[0].refusal), name  # names the link itself
        assert (latest["run_id"], by_id) == (rid, None), name


def test_latest_run_is_never_a_symlinked_entry(tmp_path):
    # opensoft/openxFactory#1187: a link dated after every recorded run was
    # the "latest" run load_snapshot returned, read through the link. A day
    # directory aliasing a real one even made a run the latest under a date
    # it was never recorded on. The lookup never selects a refused entry, as
    # latest, by date or by id, and returns the latest run it can read
    # without a link.
    clean = tmp_path / "clean"
    rid, _ = write_run(clean, extended_inventory())
    expected = catalog.load_snapshot(clean)
    recorded = foreign_run(tmp_path / "foreign")
    frid = recorded.name

    def later(root):
        return runs_root(root) / LATER_DAY_STR

    def day_alias(root):
        plant_link(later(root), runs_root(root) / DAY_STR)

    def run_directory(root):
        plant_link(later(root) / frid, recorded)

    def run_yaml(root):
        run = copy_run(recorded, later(root) / frid, meta=False)
        plant_link(run / "run.yaml", recorded / "run.yaml", directory=False)

    def link_inside_the_run(root):
        run = copy_run(recorded, later(root) / frid)
        relink_file(run / "alpha.yaml", recorded / "alpha.yaml")

    for plant in (day_alias, run_directory, run_yaml, link_inside_the_run):
        root = tmp_path / plant.__name__
        shutil.copytree(clean, root)
        plant(root)
        latest = catalog.load_snapshot(root)
        assert (latest["as_of"], latest["run_id"], latest["sequence"]) == \
            (DAY_STR, rid, 1), plant.__name__
        assert latest["repos"] == expected["repos"], plant.__name__
        assert catalog.load_snapshot(root, as_of=LATER_DAY_STR) is None, \
            plant.__name__
        assert catalog.load_snapshot(root, run_id=frid) is None, \
            plant.__name__


def test_no_sequence_is_claimed_beside_a_symlinked_entry(tmp_path):
    # opensoft/openxFactory#1187: the claim step took its highest sequence and
    # newest date from the shared scan, which read them through links: a
    # linked run's number and date came from wherever the link pointed, and a
    # dangling link was passed over as if nothing were there. An entry the
    # scan refuses has neither a sequence nor a date the claim can trust, so
    # no sequence is claimed beside it: a claim could reuse the number it
    # records, or land a run dated before it. Nothing is claimed or written.
    # Once the entry is repaired, the writer claims one past every number the
    # catalog holds, so the number a linked run occupies is never reused.
    base = tmp_path / "base"
    write_run(base, extended_inventory())
    rid_two, _ = write_run(base, extended_inventory(WORKSPACE, LATER_HEADS),
                           as_of=LATER_DAY_STR)
    new_runs = {"alpha": classified(alpha_entries(extended_inventory()),
                                    "docs/widget-overview.md", "domain")}
    new_day = "2026-07-12"
    far_later = foreign_run(tmp_path / "foreign", as_of="2026-07-20")

    def run_two(root):
        return runs_root(root) / LATER_DAY_STR / rid_two

    def recorded_run_replaced_by_a_link(root, out):
        shutil.move(run_two(root), out / rid_two)
        plant_link(run_two(root), out / rid_two)

        def repair():
            run_two(root).unlink()
            shutil.move(out / rid_two, run_two(root))
        return repair

    def foreign_day_dated_later(root, out):
        # Read through, its run.yaml would stale-refuse the claim instead.
        return plant_link(runs_root(root) / "2026-07-20",
                          far_later.parent).unlink

    def dangling_run_yaml(root, out):
        # Read through, it would be passed over as a crashed run.
        run = copy_run(run_two(base), runs_root(root) / DAY_STR / ("d" * 64),
                       meta=False)
        plant_link(run / "run.yaml", out / "missing.yaml", directory=False)
        return lambda: shutil.rmtree(run)

    def link_inside_a_recorded_run(root, out):
        return plant_link(run_two(root) / "linked", out).unlink

    for plant in (recorded_run_replaced_by_a_link, foreign_day_dated_later,
                  dangling_run_yaml, link_inside_a_recorded_run):
        name = plant.__name__
        root, outside = tmp_path / name, tmp_path / f"{name}-outside"
        shutil.copytree(base, root)
        outside.mkdir()
        repair = plant(root, outside)
        before, before_outside = tree_state(root), tree_state(outside)
        with pytest.raises(catalog.CatalogError,
                           match="no run sequence is claimed beside") as exc:
            catalog.write_run(root, new_day, new_runs, TAXONOMY)
        assert "symlink" in str(exc.value), name
        assert tree_state(root) == before, name  # no claim, no snapshot
        assert tree_state(outside) == before_outside, name
        assert not (runs_root(root) / new_day).exists(), name
        repair()
        rid, paths = catalog.write_run(root, new_day, new_runs, TAXONOMY)
        meta = json.loads((paths["alpha"].parent / "run.yaml")
                          .read_text(encoding="utf-8"))
        assert meta["sequence"] == 3, name  # past 1 and the linked run's 2
        assert sorted(p.name for p in (runs_root(root) / ".sequence")
                      .iterdir()) == \
            ["000001.yaml", "000002.yaml", "000003.yaml"], name
        assert catalog.load_snapshot(root)["run_id"] == rid, name


def test_a_refused_claim_creates_nothing(tmp_path):
    # Review (Copilot and Codex, #1190): the claim step created the claims
    # directory before the run scan could refuse. A write_run refused beside
    # a linked entry, or as stale, still left runs/.sequence behind, and a
    # direct claim through a linked root or runs directory created it inside
    # the link's target before the scan raised. A linked claims directory was
    # read, and claimed into, through the link. Every refusal now comes
    # before anything is created or read through a link.
    base = tmp_path / "base"
    write_run(base, extended_inventory(), as_of=LATER_DAY_STR)
    shutil.rmtree(runs_root(base) / ".sequence")  # no claims ledger yet
    new_runs = {"alpha": classified(alpha_entries(extended_inventory()),
                                    "docs/widget-overview.md", "domain")}
    rid = catalog.run_id(new_runs, TAXONOMY)

    def beside_a_refused_entry(root, out):
        plant_link(runs_root(root) / "2026-07-11", out)
        return (root, lambda: catalog.write_run(root, "2026-07-12", new_runs,
                                                TAXONOMY),
                "no run sequence is claimed beside")

    def stale(root, out):
        return (root, lambda: catalog.write_run(root, DAY, new_runs,
                                                TAXONOMY), "stale")

    def through_a_linked_root(root, out):
        link = plant_link(out / "linked-root", root)
        return (root, lambda: catalog._claim_sequence(link, "2026-07-12",
                                                      rid), "symlink")

    def through_a_linked_runs_directory(root, out):
        target = out / "runs"
        shutil.move(runs_root(root), target)
        plant_link(runs_root(root), target)
        return (target, lambda: catalog._claim_sequence(root, "2026-07-12",
                                                        rid), "symlink")

    def through_a_linked_claims_directory(root, out):
        claims = out / "claims"
        claims.mkdir()
        (claims / "000001.yaml").write_text(catalog.render(
            catalog._claim_document(1, LATER_DAY_STR, "f" * 64)),
            encoding="utf-8")
        plant_link(runs_root(root) / ".sequence", claims)
        return (claims, lambda: catalog._claim_sequence(root, "2026-07-12",
                                                        rid), "symlink")

    for plant in (beside_a_refused_entry, stale, through_a_linked_root,
                  through_a_linked_runs_directory,
                  through_a_linked_claims_directory):
        name = plant.__name__
        root, outside = tmp_path / name, tmp_path / f"{name}-outside"
        shutil.copytree(base, root)
        outside.mkdir()
        watched, claim, match = plant(root, outside)
        before, before_outside = tree_state(watched), tree_state(outside)
        with pytest.raises(catalog.CatalogError, match=match):
            claim()
        assert tree_state(watched) == before, name  # no claim anywhere
        assert tree_state(outside) == before_outside, name
        if name != "through_a_linked_claims_directory":
            claims_dir = (watched / ".sequence" if watched.name == "runs"
                          else runs_root(watched) / ".sequence")
            assert not claims_dir.exists(), name  # not even the directory


def test_a_symlinked_catalog_directory_refuses_the_whole_scan(tmp_path):
    # opensoft/openxFactory#1187: a link at the catalog root, or at a catalog
    # directory above the day directories, puts every run behind it, so there
    # is no single entry to report. The scan raises, naming the link, and so
    # does every caller that walks it. A node there that is not a directory
    # still means no catalog at all.
    clean = tmp_path / "clean"
    write_run(clean, extended_inventory())
    chain = {
        "root": lambda root: root,
        "health": lambda root: root / "health",
        "document-catalog": lambda root: root / "health" / "document-catalog",
        "runs": runs_root,
    }
    for name, node_of in chain.items():
        root, outside = tmp_path / name, tmp_path / f"{name}-outside"
        shutil.copytree(clean, outside)
        node = plant_link(node_of(root), node_of(outside))
        with pytest.raises(catalog.CatalogError, match="symlink") as exc:
            list(catalog._iter_runs(root))
        assert str(node) in str(exc.value), name
        with pytest.raises(catalog.CatalogError, match="symlink"):
            catalog.load_snapshot(root)
    not_a_directory = tmp_path / "not-a-directory"
    runs_root(not_a_directory).parent.mkdir(parents=True)
    runs_root(not_a_directory).write_text("occupied\n", encoding="utf-8")
    assert list(catalog._iter_runs(not_a_directory)) == []
    assert catalog.load_snapshot(not_a_directory) is None

# --- recursion exclusion (T008) ----------------------------------------------

def test_generated_catalog_paths_are_excluded_from_discovery():
    generated = Doc(
        "alpha",
        "health/document-catalog/runs/2026-07-08/deadbeef/alpha.yaml",
        '{"status": "record"}', None)
    legacy = inventory.build_inventory(
        [Doc("alpha", "docs/a.md", "body", "draft"), generated])
    assert [(e["repo"], e["path"]) for e in legacy] == \
        [("alpha", "docs/a.md")]
    repo_paths = repo_paths_for(WORKSPACE)
    extended = inventory.build_inventory(
        docs_for(repo_paths) + [generated], repo_paths,
        git=FakeGit(heads=HEADS))
    assert not any(e["path"].startswith("health/document-catalog/")
                   for e in extended)
    assert extended == extended_inventory()  # the injection was inert
    assert inventory.is_generated_catalog_path("health/document-catalog")
    assert inventory.is_generated_catalog_path(
        "health/document-catalog/recommendations/2026-07-09/j1.yaml")
    assert not inventory.is_generated_catalog_path("docs/health.md")
    assert not inventory.is_generated_catalog_path(
        "health/document-catalog-notes.md")


# --- no source mutation (SC-003) ---------------------------------------------

def test_full_pass_never_mutates_the_source_corpus(tmp_path):
    # Acceptance 4: no source document is created, edited, or deleted;
    # every write lands under health/document-catalog/.
    ws = mutated_workspace(tmp_path)
    root = tmp_path / "agg"
    before = tree_state(ws)
    inv = extended_inventory(ws, HEADS)
    entries = catalog.mechanical_entries(inv)
    catalog.diff(entries, entries)
    taxonomy = taxonomy_for(ws, HEADS)  # reads the ws registries
    write_run(root, inv, taxonomy=taxonomy)
    write_run(root, extended_inventory(ws, HEADS),
              taxonomy=taxonomy_for(ws, HEADS))  # no-op rerun
    catalog.load_snapshot(root)
    assert tree_state(ws) == before
    created = tree_state(root)
    assert created  # snapshots landed...
    assert all(p.startswith("health/document-catalog/runs/")
               for p in created)  # ...and only there


# --- concurrency-safe rendered write (Copilot #1 / review finding 4) ----------

def test_write_rendered_is_concurrency_safe_across_distinct_content(tmp_path):
    # Copilot #1: _write_rendered must use a UNIQUE per-invocation temp,
    # so racing writers of the SAME target with DIFFERENT bytes (exactly
    # run.yaml under two runs of one run-id that each claimed a distinct
    # sequence) never share/truncate/unlink each other's temp — no torn
    # destination file, and no stray FileNotFoundError from a winner
    # consuming a shared temp. The old fixed `path.name + ".tmp"` failed
    # precisely this.
    target = tmp_path / "sub" / "run.yaml"
    target.parent.mkdir(parents=True)
    # Distinct AND different-length payloads so any torn interleaving of
    # two writes is detectable as "not equal to any single input".
    inputs = [f"sequence: {i}\n" + "x" * (i * 37) + "\n" for i in range(24)]
    errors = []
    barrier = threading.Barrier(len(inputs))

    def writer(text):
        try:
            barrier.wait()
            catalog._write_rendered(target, text)
        except BaseException as exc:  # noqa: BLE001 - recorded, asserted below
            errors.append(exc)

    threads = [threading.Thread(target=writer, args=(t,)) for t in inputs]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    assert errors == []  # no FileNotFoundError from a shared temp
    # The published file is exactly ONE writer's complete bytes — never a
    # torn blend of two different-length writes.
    assert target.read_text(encoding="utf-8") in inputs
    # No shared/leaked temp remains beside the published file.
    leftovers = [p.name for p in target.parent.iterdir()
                 if p.name != "run.yaml"]
    assert leftovers == []
