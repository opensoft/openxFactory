"""Mechanical catalog (US1): deterministic entries, diff classes,
rename-as-delete-plus-add, immutable dated snapshots with effective
taxonomy provenance, byte-identical rendering, atomically claimed run
sequences, stale-overwrite refusal, opaque locators for path-prohibited
documents, recursion exclusion, and the no-source-mutation boundary.

All tests are hermetic: the fixture workspace is read-only (mutation
scenarios copy it into pytest tmp dirs), git facts come from
conftest.FakeGit, and every write lands under a tmp catalog root."""

from __future__ import annotations

import errno
import hashlib
import json
import os
import shutil
import stat
import threading
from datetime import datetime
from pathlib import Path

import pytest

from conftest import AS_OF, FIXTURES, FakeGit, ProbeDenial  # noqa: F401 (sys.path side effect)

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
    persisted = catalog._load_run_bytes(tmp_path, run_dir)
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
        rid, docs, catalog._load_run_bytes(tmp_path, run_dir)) is None
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
        tmp_path / "old", runs_root(tmp_path / "old") / DAY_STR / legacy)
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
                                 catalog._load_run_bytes(tmp_path, run_dir)) \
        == catalog.CONTENT_ADDRESSED


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
                                     tmp_path / "closed",
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
        tmp_path / "partial", runs_root(tmp_path / "partial") / DAY_STR / rid)) \
        == catalog.CONTENT_ADDRESSED


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


def test_write_run_refuses_a_non_snapshot_stranger_anywhere_in_the_run(
        tmp_path):
    # Follow-up to #1175 (opensoft/openxFactory#1186, Copilot's review
    # thread on catalog.py:1161): the preflight above this one compared
    # only the repositories a run records against paths _snapshot_files
    # yields, which filters to *.yaml -- so a plain non-YAML file
    # (notes.txt), a *.yaml.bak-suffixed one, or a stranger subdirectory
    # (empty, or holding only non-YAML content) never surfaced there, and
    # the run-identity hash never saw it. _refuse_foreign_descendants checks
    # EVERY descendant of the run directory against the exact allowed set
    # (run.yaml plus the repository-snapshot paths this run records), so
    # each of these is now refused before the first write or claim, the
    # same way (CatalogError, "does not record") as the existing
    # stranger-snapshot refusal above.
    alpha = alpha_entries(extended_inventory())
    runs = {"alpha": alpha, "xFactories/MedxFactory": [
        dict(e, repo="xFactories/MedxFactory") for e in alpha]}
    rid, _recorded = catalog.write_run(tmp_path / "src", DAY, runs, TAXONOMY)
    cases = {
        "non-yaml-top-level": ("notes.txt",),
        "non-yaml-nested": ("xFactories", "notes.txt"),
        "yaml-bak-suffix": ("run.yaml.bak",),
        "stranger-subdirectory-empty": ("extra",),  # a directory, no file
        "stranger-subdirectory-with-file": ("extra", "junk.txt"),
    }
    for name, rel in cases.items():
        root = tmp_path / name
        shutil.copytree(tmp_path / "src", root)
        run_dir = runs_root(root) / DAY_STR / rid
        stray = run_dir.joinpath(*rel)
        if name == "stranger-subdirectory-empty":
            stray.mkdir()
        else:
            stray.parent.mkdir(parents=True, exist_ok=True)
            stray.write_text("stranger\n", encoding="utf-8")
        before = tree_state(root)
        with pytest.raises(catalog.CatalogError, match="does not record"):
            catalog.write_run(root, DAY, runs, TAXONOMY)
        assert tree_state(root) == before, name  # no claim, no run.yaml


def test_write_run_refuses_a_symlinked_stranger_in_the_run(tmp_path):
    # A stranger planted as a symlink is refused too -- but by the
    # PRE-EXISTING _refuse_links_inside guard (#1175 rounds 6 and 9), which
    # walks every node under the run directory and refuses any symlink
    # outright, before _refuse_foreign_descendants (this follow-up's new
    # check, added above) ever runs. This scenario already raised on main;
    # unlike the five plain file/directory cases in the test above, it is
    # not new coverage. It is kept as an interaction guard: adding the
    # descendant-vs-allowed-set check must not loosen, skip, or reorder the
    # existing no-symlink-anywhere guarantee.
    alpha = alpha_entries(extended_inventory())
    runs = {"alpha": alpha}
    rid, recorded = catalog.write_run(tmp_path / "src", DAY, runs, TAXONOMY)
    root = tmp_path / "linked"
    shutil.copytree(tmp_path / "src", root)
    run_dir = runs_root(root) / DAY_STR / rid
    outside = tmp_path / "outside"
    outside.mkdir()
    target = outside / "evil.yaml"
    target.write_bytes(recorded["alpha"].read_bytes())
    (run_dir / "evil.yaml").symlink_to(target)
    before = tree_state(root)
    with pytest.raises(catalog.CatalogError, match="symlink"):
        catalog.write_run(root, DAY, runs, TAXONOMY)
    assert tree_state(root) == before


def test_write_run_still_passes_a_clean_run(tmp_path):
    # The new descendant preflight (_refuse_foreign_descendants) must not
    # reject a run holding exactly its own allowed set: a fresh run
    # directory (nothing exists yet, so the "if run_dir.exists()" guard is
    # not even entered), and a repeat over one already fully recorded --
    # run.yaml, every legitimate snapshot, including the "xFactories"
    # ancestor directory a slash-separated repository id creates, and
    # nothing else.
    alpha = alpha_entries(extended_inventory())
    runs = {"alpha": alpha, "xFactories/MedxFactory": [
        dict(e, repo="xFactories/MedxFactory") for e in alpha]}
    rid, paths = catalog.write_run(tmp_path / "fresh", DAY, runs, TAXONOMY)
    assert sorted(paths) == ["alpha", "xFactories/MedxFactory"]
    rid_again, paths_again = catalog.write_run(
        tmp_path / "fresh", DAY, runs, TAXONOMY)
    assert rid_again == rid
    assert {r: p.read_bytes() for r, p in paths_again.items()} == \
        {r: p.read_bytes() for r, p in paths.items()}
    assert catalog.load_snapshot(tmp_path / "fresh")["run_id"] == rid


def test_write_run_refuses_a_temp_shaped_stranger_in_the_run(tmp_path):
    # opensoft/openxFactory#1196, from Copilot's last round on PR #1189
    # (#1186): the preflight admitted any regular file named like one of
    # _write_rendered's temps, "<final-name>.<random>.tmp", beside an
    # allowed file, because the writer staged its temps there. A concurrent
    # writer's temp in flight and one a crash left behind both sat inside
    # the run, so a stranger merely named that way passed too. Every write
    # is now staged in catalog.STAGING_DIR, outside every run, so no temp of
    # the writer's is ever inside one and the preflight admits none. Each
    # shape the admission let through now refuses before anything is
    # claimed or written, like any other stranger: beside a snapshot,
    # beside a nested repository's snapshot, beside run.yaml, and beside a
    # partial run a crash left behind, which heals once the file is gone.
    # This replaces the test that pinned the admission. The writer's own
    # temps, in flight and left by a crash, are pinned by the staging
    # tests (opensoft/openxFactory#1196) further down.
    alpha = alpha_entries(extended_inventory())
    runs = {"alpha": alpha, "xFactories/MedxFactory": [
        dict(e, repo="xFactories/MedxFactory") for e in alpha]}
    rid, _recorded = catalog.write_run(tmp_path / "src", DAY, runs, TAXONOMY)
    cases = {
        "beside-a-snapshot": ("alpha.yaml.z9k2p7.tmp",),
        "beside-a-nested-snapshot": ("xFactories",
                                     "MedxFactory.yaml.q1w2e3.tmp"),
        "beside-run-yaml": ("run.yaml.a1b2c3.tmp",),
    }
    for name, rel in cases.items():
        root = tmp_path / name
        shutil.copytree(tmp_path / "src", root)
        run_dir = runs_root(root) / DAY_STR / rid
        run_dir.joinpath(*rel).write_bytes(b"partial, in flight")
        before = tree_state(root)
        with pytest.raises(catalog.CatalogError,
                           match="does not record") as exc:
            catalog.write_run(root, DAY, runs, TAXONOMY)
        assert "/".join(rel) in str(exc.value), name  # names the stranger
        assert tree_state(root) == before, name  # no claim, no write

    # A partial run: alpha and run.yaml landed, then a crash left the temp
    # of the snapshot it never published beside that snapshot's path, where
    # the writer once staged it. The retry refuses rather than heal the run
    # around it, and heals once the file is gone.
    crashed = tmp_path / "crashed"
    catalog.write_snapshot(crashed, DAY, rid, "alpha", runs["alpha"],
                           TAXONOMY)  # only alpha landed before the crash
    crashed_run_dir = runs_root(crashed) / DAY_STR / rid
    (crashed_run_dir / "xFactories").mkdir()
    orphaned = (crashed_run_dir / "xFactories" /
                "MedxFactory.yaml.orphaned9z.tmp")
    orphaned.write_bytes(b"never replaced")
    before = tree_state(crashed)
    with pytest.raises(catalog.CatalogError, match="does not record"):
        catalog.write_run(crashed, DAY, runs, TAXONOMY)
    assert tree_state(crashed) == before
    orphaned.unlink()
    rid_healed, paths_healed = catalog.write_run(crashed, DAY, runs,
                                                 TAXONOMY)
    assert rid_healed == rid
    assert sorted(paths_healed) == ["alpha", "xFactories/MedxFactory"]
    assert sorted(catalog.load_snapshot(crashed)["repos"]) == \
        ["alpha", "xFactories/MedxFactory"]


def test_write_run_fails_closed_on_an_unenumerable_run_directory(tmp_path):
    # Review (Copilot, PR #1189 for #1186): os.walk silently skips a
    # directory it cannot enumerate when onerror is omitted, so a foreign
    # descendant hidden inside an unreadable subdirectory of an otherwise
    # legitimate, allowed ancestor ("xFactories/", here) would never be
    # seen at all -- the preflight would complete over a subtree it never
    # actually verified. _refuse_foreign_descendants now fails closed: an
    # enumeration error anywhere in the run directory refuses the run
    # rather than silently letting it through.
    alpha = alpha_entries(extended_inventory())
    runs = {"alpha": alpha, "xFactories/MedxFactory": [
        dict(e, repo="xFactories/MedxFactory") for e in alpha]}
    rid, _recorded = catalog.write_run(tmp_path / "src", DAY, runs, TAXONOMY)
    root = tmp_path / "unreadable"
    shutil.copytree(tmp_path / "src", root)
    run_dir = runs_root(root) / DAY_STR / rid
    blocked = run_dir / "xFactories"
    before = tree_state(root)
    mode = blocked.stat().st_mode
    # Execute-only (no read): a KNOWN child path (the preceding checks'
    # lstat of xFactories/MedxFactory.yaml) still resolves fine, but
    # os.scandir(xFactories) -- what os.walk needs to enumerate its
    # contents -- is denied, which is exactly the enumeration failure
    # under test.
    blocked.chmod(0o100)
    try:
        with pytest.raises(catalog.CatalogError,
                           match="could not be fully enumerated"):
            catalog.write_run(root, DAY, runs, TAXONOMY)
    finally:
        blocked.chmod(mode)  # restore -- tmp_path cleanup needs it readable
    assert tree_state(root) == before  # no claim, no write


def test_refuse_links_inside_fails_closed_on_an_unenumerable_subdirectory(
        tmp_path, monkeypatch):
    # opensoft/openxFactory#1197: _refuse_links_inside's own os.walk passed
    # no onerror at all -- unlike its sibling _refuse_foreign_descendants
    # (PR #1189/#1190), which already failed closed the same way -- so a
    # subdirectory os.walk could not enumerate was silently skipped, and a
    # symlink hiding inside one would never be seen. Monkeypatched, not
    # chmod'd: chmod does not deny a directory to root, so a chmod-based
    # repro would not hold under a root test runner or in CI.
    run_dir = tmp_path / "run"
    blocked = run_dir / "xFactories"
    blocked.mkdir(parents=True)
    (blocked / "MedxFactory.yaml").write_bytes(b"placeholder")
    real_scandir = os.scandir

    def denying_scandir(path="."):
        if Path(path) == blocked:
            raise PermissionError(
                errno.EACCES, os.strerror(errno.EACCES), os.fspath(path))
        return real_scandir(path)

    monkeypatch.setattr(os, "scandir", denying_scandir)
    with pytest.raises(catalog.CatalogError) as excinfo:
        catalog._refuse_links_inside(tmp_path, run_dir)
    message = str(excinfo.value)
    assert "could not be fully enumerated" in message
    # the node the walk could not enter, named relative to run_dir, never
    # the host-absolute path the underlying OSError itself carries
    assert "(xFactories)" in message


def test_refuse_links_inside_fails_closed_on_an_unprobeable_entry(
        tmp_path, monkeypatch):
    # Copilot review (PR #1200): onerror only covers a failed
    # scandir(top), not a failed per-entry classification -- os.walk's own
    # is_dir() catches an OSError from one listed entry and treats it as a
    # plain file rather than aborting (same on 3.12, 3.13, and 3.14), and
    # the entry is still yielded either way. A bare node.is_symlink() would
    # then misclassify it right along with os.walk: not a directory to
    # refuse enumerating, and on Python 3.14 not a symlink either, since
    # is_symlink there swallows the same error. Every listed name is
    # classified by _own_mode's explicit os.lstat instead (the same
    # primitive _link_inside already uses for the read-side scan), so a
    # per-entry probe failure -- injected here on os.lstat itself, not
    # scandir -- still refuses.
    run_dir = tmp_path / "run"
    run_dir.mkdir()
    blocked = run_dir / "MedxFactory.yaml"
    blocked.write_bytes(b"placeholder")
    real_lstat = os.lstat

    def denying_lstat(path, *args, **kwargs):
        if Path(path) == blocked:
            raise PermissionError(
                errno.EACCES, os.strerror(errno.EACCES), os.fspath(path))
        return real_lstat(path, *args, **kwargs)

    monkeypatch.setattr(os, "lstat", denying_lstat)
    with pytest.raises(catalog.CatalogError) as excinfo:
        catalog._refuse_links_inside(tmp_path, run_dir)
    message = str(excinfo.value)
    assert "could not be checked for a symlink" in message
    # opensoft/openxFactory#1201: named under the root, by its errno name,
    # never by the host-absolute path or the strerror the OSError carries.
    assert "(EACCES)" in message and message.endswith("run/MedxFactory.yaml")
    assert str(tmp_path) not in message
    assert os.strerror(errno.EACCES) not in message


# --- opensoft/openxFactory#1201: every catalog probe fails closed -----------
#
# Python 3.14's pathlib answers False from `exists`, `is_dir`, `is_file` and
# `is_symlink` for a node whose `stat` fails for ANY reason. Five writer
# probes asked pathlib (`_refuse_foreign_node`, `_occupied`, `_read_claims`,
# and the run-directory probes in `write_snapshot` and `write_run`), so on
# 3.14 an unreadable node passed the writer's no-follow guard as absent, an
# existing record read as "nothing there", and an unreadable claims directory
# read as holding no claims. Every one now classifies the node by the one
# explicit `lstat` the run scan already used (`_node_mode`), and a node it
# cannot check is a controlled `CatalogError` naming the node under the
# catalog root and the errno by name: never the host-absolute path or the
# strerror text the OSError carries. Each case runs under this interpreter's
# pathlib AND CPython 3.14's (`pathlib_314`), with EACCES and EIO, and the
# tree is compared node for node (directories included) before and after.

UNPROBEABLE_ERRNOS = (errno.EACCES, errno.EIO)


def full_state(base):
    """Every node under `base`, directories and links included, with each
    file's sha256: what "nothing claimed, staged, made or replaced" is
    measured against (`tree_state` sees files only)."""
    state = {}
    for dirpath, dirnames, filenames in os.walk(base):
        for name in sorted(dirnames + filenames):
            node = Path(dirpath) / name
            rel = node.relative_to(base).as_posix()
            mode = os.lstat(node).st_mode
            if stat.S_ISLNK(mode):
                state[rel] = "link:" + os.readlink(node)
            elif stat.S_ISDIR(mode):
                state[rel] = "dir"
            else:
                state[rel] = hashlib.sha256(node.read_bytes()).hexdigest()
    return state


def assert_redacted_refusal(exc, root, node, err, tmp_path):
    """The controlled refusal for an unprobeable node: names the node under
    the catalog root and the errno by name, and carries neither the
    host-absolute path nor the strerror text of the OSError behind it."""
    message = str(exc)
    assert "could not be checked for a symlink" in message, message
    assert f"({errno.errorcode[err]})" in message, message
    rel = Path(node).relative_to(root).as_posix()
    assert message.endswith(f": {rel}"), message
    assert str(tmp_path) not in message, message
    assert os.strerror(err) not in message, message


def _unprobeable_run(tmp_path):
    """(entries by repository, run id) for a one-repository run."""
    runs = {"alpha": alpha_entries(extended_inventory())}
    return runs, catalog.run_id(runs, TAXONOMY)


# The nodes the writer's preflight classifies before anything is claimed:
# every directory from the catalog root down (`_catalog_chain`), the claims
# and staging directories, the day and run directories, `run.yaml` and the
# snapshot (`_refuse_unsafe_run_paths` -> `_refuse_foreign_node`).
PREFLIGHT_NODES = {
    "catalog-root": lambda root, run: root,
    "health": lambda root, run: root / "health",
    "runs": lambda root, run: runs_root(root),
    "claims-directory": lambda root, run: runs_root(root) / ".sequence",
    "staging-directory": lambda root, run: runs_root(root) / ".staging",
    "day-directory": lambda root, run: run.parent,
    "run-directory": lambda root, run: run,
    "run-yaml": lambda root, run: run / "run.yaml",
    "snapshot": lambda root, run: run / "alpha.yaml",
}


@pytest.mark.parametrize("err", UNPROBEABLE_ERRNOS, ids=errno.errorcode.get)
@pytest.mark.parametrize("case", sorted(PREFLIGHT_NODES))
def test_the_writer_refuses_a_node_it_cannot_check_before_anything_lands(
        tmp_path, monkeypatch, pathlib_314, case, err):
    # `_refuse_foreign_node`, the writer's no-follow guard: with pathlib's
    # probes, Python 3.14 passed a node it could not stat -- a symlink
    # included -- as absent (the #1201 survey measured it with a real
    # EACCES), and this interpreter raised a raw OSError carrying the
    # host-absolute path.
    runs, rid = _unprobeable_run(tmp_path)
    root = tmp_path / "catalog"
    root.mkdir()
    node = PREFLIGHT_NODES[case](root, runs_root(root) / DAY_STR / rid)
    before = full_state(root)
    denial = ProbeDenial(monkeypatch, [node], err)
    with pytest.raises(catalog.CatalogError) as caught:
        catalog.write_run(root, DAY, runs, TAXONOMY)
    denial.armed = False
    assert denial.denied, case  # the denial was reached, not bypassed
    assert_redacted_refusal(caught.value, root, node, err, tmp_path)
    assert full_state(root) == before, case  # nothing claimed, staged, made


def _partial_run(tmp_path, name):
    """A copy of a recorded one-repository run whose run.yaml is gone: a
    run that crashed between its snapshot and its record, which a retry
    heals by claiming a sequence and writing run.yaml. So a refusal that
    comes too late shows as a changed tree."""
    runs, rid = _unprobeable_run(tmp_path)
    catalog.write_run(tmp_path / "src", DAY, runs, TAXONOMY)
    root = tmp_path / name
    shutil.copytree(tmp_path / "src", root)
    run_dir = runs_root(root) / DAY_STR / rid
    (run_dir / "run.yaml").unlink()
    return root, runs, rid, run_dir


def _arm_after(monkeypatch, name, denial, *, on_entry=False):
    """Arm `denial` when `catalog.<name>` returns (or is entered): the node
    becomes unreadable after the checks before it vouched for it, so the
    probe under test is the first to meet the denial."""
    real = getattr(catalog, name)

    def armed(*args, **kwargs):
        if on_entry:
            denial.armed = True
        result = real(*args, **kwargs)
        denial.armed = True
        return result

    monkeypatch.setattr(catalog, name, armed)


# (call, node, the catalog function after which the node turns unreadable,
#  whether it turns unreadable on ENTRY to that function instead)
LATE_PROBES = {
    # write_run's own run-directory probe (was `run_dir.exists()`): on 3.14
    # it skipped the link walk and the foreign-descendant walk
    "write_run-run-directory": (
        "write_run", lambda run: run, "_refuse_unsafe_run_paths", False),
    # write_snapshot's run-directory probe (was `run_dir.exists()`): on 3.14
    # it skipped the link walk before a partial run was healed
    "write_snapshot-run-directory": (
        "write_snapshot", lambda run: run, "_refuse_unsafe_run_paths", False),
    # `_occupied` behind `_holds_exactly` (was `exists() or is_symlink()`):
    # on 3.14 an existing snapshot read as "nothing there"
    "write_run-snapshot": (
        "write_run", lambda run: run / "alpha.yaml",
        "_refuse_foreign_descendants", False),
    # `_occupied` behind `_recorded`: on 3.14 an existing run.yaml read as
    # "never recorded"
    "write_run-run-yaml": (
        "write_run", lambda run: run / "run.yaml",
        "_refuse_foreign_descendants", False),
    # `_read_claims` (was `claims_dir.is_dir()`): on 3.14 an unreadable
    # claims directory read as holding no claims
    "write_snapshot-claims-directory": (
        "write_snapshot", lambda run: run.parent.parent / ".sequence",
        "_read_claims", True),
}


@pytest.mark.parametrize("err", UNPROBEABLE_ERRNOS, ids=errno.errorcode.get)
@pytest.mark.parametrize("case", sorted(LATE_PROBES))
def test_a_probe_after_the_preflight_refuses_a_node_it_cannot_check(
        tmp_path, monkeypatch, pathlib_314, case, err):
    call, node_of, after, on_entry = LATE_PROBES[case]
    root, runs, rid, run_dir = _partial_run(tmp_path, "partial")
    if case.endswith("run-yaml"):
        # a recorded run, so run.yaml is there to be read as absent
        catalog.write_run(root, DAY, runs, TAXONOMY)
    node = node_of(run_dir)
    before = full_state(root)
    denial = ProbeDenial(monkeypatch, [node], err, armed=False)
    _arm_after(monkeypatch, after, denial, on_entry=on_entry)
    with pytest.raises(catalog.CatalogError) as caught:
        if call == "write_run":
            catalog.write_run(root, DAY, runs, TAXONOMY)
        else:
            catalog.write_snapshot(root, DAY, rid, "alpha", runs["alpha"],
                                   TAXONOMY)
    denial.armed = False
    assert denial.denied, case  # the probe under test met the denial
    assert_redacted_refusal(caught.value, root, node, err, tmp_path)
    assert full_state(root) == before, case  # nothing claimed or written


@pytest.mark.parametrize("err", (errno.ENOENT, errno.ENOTDIR),
                         ids=errno.errorcode.get)
def test_absence_still_reads_as_absent_at_every_writer_probe(
        tmp_path, monkeypatch, pathlib_314, err):
    # The other side of the same line: FileNotFoundError and
    # NotADirectoryError are absence, so a fresh catalog root still works.
    root = tmp_path / "catalog"
    node = root / "health"
    node.mkdir(parents=True)
    denial = ProbeDenial(monkeypatch, [node], err)
    assert catalog._occupied(root, node) is False
    catalog._refuse_foreign_node(root, node, directory=True)  # passes
    assert catalog._read_claims(root, node) == []
    assert denial.denied
    # and a real ENOTDIR: a path below a regular file
    denial.armed = False
    (root / "file").write_bytes(b"x")
    assert catalog._occupied(root, root / "file" / "child") is False


def test_a_catalog_probe_refuses_a_symlink_loop_that_fs_probe_reads_absent(
        tmp_path, monkeypatch):
    # The catalog's flavour is deliberately stricter than `fs_probe`'s:
    # absence is FileNotFoundError and NotADirectoryError alone, so ELOOP
    # (which pathlib through 3.13, and `fs_probe` on every version, read as
    # absent) is refused here, as every other unexplained failure is.
    root = tmp_path / "catalog"
    node = root / "health"
    node.mkdir(parents=True)
    ProbeDenial(monkeypatch, [node], errno.ELOOP)
    with pytest.raises(catalog.CatalogError) as caught:
        catalog._occupied(root, node)
    assert "(ELOOP)" in str(caught.value)


def test_no_catalog_refusal_carries_the_oserrors_own_text(tmp_path,
                                                          monkeypatch):
    # The issue's second ask: `_own_mode`'s refusal interpolated `str(exc)`,
    # whose filename is the host-absolute path CI's secret sweeper redacts.
    # A sentinel that LOOKS like a runner's home path (assembled here, never
    # written as a literal a sweeper would redact from this file) is put in
    # both the OSError's filename and its strerror: no refusal may carry it.
    sentinel = os.sep.join(["", "home", "runner", "work", "sentinel-1201"])
    root = tmp_path / "catalog"
    node = root / "health" / "document-catalog"
    node.mkdir(parents=True)
    real_lstat = os.lstat

    def lstat(path, *args, **kwargs):
        if isinstance(path, (str, os.PathLike)) and Path(path) == node:
            raise OSError(errno.EACCES, f"denied under {sentinel}", sentinel)
        return real_lstat(path, *args, **kwargs)

    monkeypatch.setattr(os, "lstat", lstat)
    _mode, refusal = catalog._own_mode(root, node)
    refusals = [refusal]
    for probe in (lambda: catalog._occupied(root, node),
                  lambda: catalog._refuse_foreign_node(root, node, True),
                  lambda: list(catalog._iter_runs(root))):
        with pytest.raises(catalog.CatalogError) as caught:
            probe()
        refusals.append(caught.value)
    for refusal in refusals:
        message = str(refusal)
        assert sentinel not in message and "denied under" not in message
        assert message.endswith(": health/document-catalog"), message
        assert "(EACCES)" in message, message


def test_write_run_refuses_a_stranger_merely_shaped_like_a_writer_temp(
        tmp_path):
    # Review round 2 (Copilot, PR #1189 for #1186): the temp admission's
    # first cut accepted "<final-name>.tmp" with NO random component (mkstemp
    # never omits one -- only a stranger deliberately or accidentally named
    # to resemble a temp could be that exact string) and any non-symlink
    # special node sharing a temp-shaped name (mkstemp only ever creates a
    # plain file). Both are foreign descendants and must refuse. Since
    # opensoft/openxFactory#1196 no temp shape is admitted at all, so they
    # refuse as every temp-shaped stranger does.
    alpha = alpha_entries(extended_inventory())
    runs = {"alpha": alpha}
    rid, _recorded = catalog.write_run(tmp_path / "src", DAY, runs, TAXONOMY)
    cases = {
        "no-random-component": lambda run_dir: (
            run_dir / "alpha.yaml.tmp").write_bytes(b"not a real temp"),
        "fifo-shaped-like-a-temp": lambda run_dir: os.mkfifo(
            run_dir / "alpha.yaml.z9k2p7.tmp"),
    }
    for name, plant in cases.items():
        root = tmp_path / name
        shutil.copytree(tmp_path / "src", root)
        run_dir = runs_root(root) / DAY_STR / rid
        plant(run_dir)
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
    # Review round 3 (Copilot, #1190): if the scan asked Path.is_symlink
    # whether a node was a link, a denied lstat reading as "no link" would
    # be a real hazard on any implementation that swallows every OSError
    # the way os.path.islink does -- which is no longer hypothetical:
    # through Python 3.13, is_symlink documents the propagate-vs-absent
    # contract (only "doesn't exist" reads as False; a permission error
    # propagates), but Python 3.14 changes it -- is_symlink there calls
    # os.path.islink directly (verified against the CPython sources and
    # the official docs; see the PR body). The scan still never asks
    # Path.is_symlink at all: every node is checked with an explicit
    # lstat, and whatever it cannot check or list refuses that entry
    # alone; the runs directory itself refuses the whole scan. This
    # monkeypatch pins is_symlink to exactly that -- Python 3.14's real
    # behaviour, not merely a worst case -- to prove the scan is
    # unaffected on 3.12, 3.13, or 3.14.
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


def record_followed_links(patch, under, every=False, fail=None):
    """The paths of every symlink at or below `under` whose target a call
    stats while `patch` holds: ``os.stat`` following links, which
    ``Path.is_dir``, ``Path.is_file``, ``Path.exists`` and ``os.path.isdir``
    all reach, and a ``DirEntry`` classified or stat-ed following links, as
    ``os.walk`` classifies every entry it lists (``DirEntry.is_dir``).
    `every` records every node such a call stats, link or not. A recorded
    ``os.stat`` of a path `fail` accepts then raises ``PermissionError``, as
    a stat that fails where the node's own ``lstat`` succeeded would."""
    followed = []
    real_stat, real_scandir = os.stat, os.scandir
    prefix = os.fspath(under)

    def link_below(path):
        if not isinstance(path, (str, os.PathLike)):
            return False  # a file descriptor: nothing to follow
        path = os.fspath(path)
        return ((path == prefix or path.startswith(prefix + os.sep))
                and (every or os.path.islink(path)))

    def tracked_stat(path, *, dir_fd=None, follow_symlinks=True):
        if follow_symlinks and dir_fd is None and link_below(path):
            followed.append(os.fspath(path))
            if fail is not None and fail(os.fspath(path)):
                raise PermissionError(errno.EACCES, os.strerror(errno.EACCES),
                                      os.fspath(path))
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


def test_run_scan_classifies_every_node_by_its_own_lstat(tmp_path):
    # Review round 5 (Copilot, #1190: two findings its review counted but
    # never posted): after its lstat check the scan still asked is_dir() and
    # is_file() whether a node was a directory or a recorded run.yaml. Each
    # stats the node a second time, following links, and on any
    # implementation that swallows every OSError the way os.path.isdir and
    # os.path.isfile do, a failed second stat would read as absent: the
    # scan would report no catalog, or pass over a day or a recorded run,
    # instead of failing closed -- which is no longer hypothetical: through
    # Python 3.13, is_dir/is_file document the propagate-vs-absent contract
    # (only "doesn't exist" reads as False; a permission error propagates
    # -- verified against the CPython sources and the official docs, see
    # the PR body), but Python 3.14 changes it -- both call os.path.isdir/
    # isfile directly there. The scan does not lean on either version's
    # contract: every node is now classified by the mode its own lstat
    # returned, so the scan makes no following stat at all -- one explicit
    # primitive doing the whole job on 3.12, 3.13, or 3.14 alike. With
    # is_dir() and is_file() pinned to that real 3.14 behaviour below, a
    # following stat that fails changes nothing it yields.
    root = tmp_path / "agg"
    rid_one, _ = write_run(root, extended_inventory())
    alpha = alpha_entries(extended_inventory())
    rid_two, _ = catalog.write_run(root, LATER_DAY_STR, {
        "xFactories/MedxFactory": [dict(e, repo="xFactories/MedxFactory")
                                   for e in alpha]}, TAXONOMY)
    (runs_root(root) / LATER_DAY_STR / ("e" * 64)).mkdir()  # crashed run
    (runs_root(root) / "notes.yaml").write_text("stray\n", encoding="utf-8")
    expected = list(catalog._iter_runs(root))
    assert [tuple(e[:3]) for e in expected] == [
        (DAY_STR, 1, rid_one), (LATER_DAY_STR, 2, rid_two)]  # none refused
    chain = {os.fspath(node) for node in catalog._catalog_chain(root)}
    days = {os.fspath(runs_root(root) / DAY_STR),
            os.fspath(runs_root(root) / LATER_DAY_STR)}
    run_dirs = {os.fspath(e[3]) for e in expected}

    with pytest.MonkeyPatch.context() as patch:
        followed = record_followed_links(patch, root, every=True)
        assert list(catalog._iter_runs(root)) == expected
    assert followed == []

    for name, denied in (
            ("a-catalog-directory", lambda path: path in chain),
            ("a-day-directory", lambda path: path in days),
            ("a-run-directory", lambda path: path in run_dirs),
            ("a-run-yaml", lambda path: os.path.basename(path) == "run.yaml"),
            ("every-node", lambda path: True)):
        with pytest.MonkeyPatch.context() as patch:
            patch.setattr(Path, "is_dir", lambda self: os.path.isdir(self))
            patch.setattr(Path, "is_file", lambda self: os.path.isfile(self))
            record_followed_links(patch, root, every=True, fail=denied)
            assert list(catalog._iter_runs(root)) == expected, name


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


# --- writes staged outside the run tree (opensoft/openxFactory#1196) ---------

def test_the_writers_staged_temp_is_never_inside_the_scanned_tree(tmp_path):
    # opensoft/openxFactory#1196: a write in flight has its temp on disk,
    # and _write_rendered stages it in catalog.STAGING_DIR: beside the day
    # directories, on the run tree's own filesystem, named for its target,
    # and never inside a day or run directory. So neither the run scan nor
    # the writer's preflight ever meets it. This pins Codex's P1 on PR #1189
    # at the moment that finding named: an identical writer that starts
    # while another is between its mkstemp and its os.replace completes,
    # although the preflight now admits no temp-shaped file at all. Each
    # publish is checked at its rename, with the temp still staged.
    alpha = alpha_entries(extended_inventory())
    runs = {"alpha": alpha, "xFactories/MedxFactory": [
        dict(e, repo="xFactories/MedxFactory") for e in alpha]}
    rid = catalog.run_id(runs, TAXONOMY)
    run_dir = runs_root(tmp_path) / DAY_STR / rid
    staging = tmp_path / catalog.STAGING_DIR
    allowed = [run_dir / "run.yaml", run_dir / "alpha.yaml",
               run_dir / "xFactories" / "MedxFactory.yaml"]
    real_replace = os.replace
    published = []

    def publish(src, dst):
        src, dst = Path(src), Path(dst)
        staged = src.read_bytes()
        # Staged, not beside its target: in the staging directory, on the
        # target directory's filesystem, holding the complete rendering.
        assert src.parent == staging, src
        assert src.name.startswith(dst.name + ".") and \
            src.name.endswith(".tmp"), src
        assert os.lstat(staging).st_dev == os.lstat(dst.parent).st_dev
        assert staged == catalog.render(json.loads(staged)).encode("utf-8")
        # The scan lists nothing for the staging directory, and the
        # preflight's walk over the run finds nothing the run does not
        # record.
        assert all(entry.as_of != staging.name
                   for entry in catalog._iter_runs(tmp_path))
        catalog._refuse_foreign_descendants(run_dir, allowed)
        published.append((dst.relative_to(run_dir).as_posix(),
                          sorted(p.name for p in staging.iterdir())))
        if len(published) == 1:  # the first write is in flight: an
            catalog.write_run(tmp_path, DAY, runs, TAXONOMY)  # identical one
        return real_replace(src, dst)

    with pytest.MonkeyPatch.context() as patch:
        patch.setattr(os, "replace", publish)
        assert catalog.write_run(tmp_path, DAY, runs, TAXONOMY)[0] == rid
    # The first writer's alpha.yaml temp stayed staged while the second
    # writer's preflight, claim and three publishes ran, and the second
    # recorded the run. The first then published an identical alpha.yaml
    # and found the rest recorded.
    assert [dst for dst, _staged in published] == [
        "alpha.yaml", "alpha.yaml", "run.yaml", "xFactories/MedxFactory.yaml"]
    assert [len(staged) for _dst, staged in published] == [1, 2, 2, 2]
    assert list(staging.iterdir()) == []  # every temp consumed by its rename
    meta = json.loads((run_dir / "run.yaml").read_text(encoding="utf-8"))
    assert meta["sequence"] == 2  # the second writer recorded first
    claims = runs_root(tmp_path) / ".sequence"
    assert [json.loads(p.read_text(encoding="utf-8"))["run_id"]
            for p in sorted(claims.iterdir())] == [rid, rid]  # 1 orphaned
    latest = catalog.load_snapshot(tmp_path)
    assert (latest["run_id"], latest["sequence"]) == (rid, 2)
    assert catalog.run_id_scheme(rid, latest["repos"],
                                 catalog._load_run_bytes(tmp_path, run_dir)) \
        == catalog.CONTENT_ADDRESSED


def test_stale_staging_content_is_ignored_and_never_admitted(tmp_path):
    # opensoft/openxFactory#1196: a writer that crashes between its mkstemp
    # and its os.replace leaves its temp in catalog.STAGING_DIR. Stale
    # staging content is IGNORED, never swept: nothing tells it apart from a
    # concurrent writer's temp in flight, whose rename a sweep would break,
    # and an age test would read the wall clock. It is never read either,
    # so it is never admitted as a snapshot: only the rename of the writer
    # that staged it could carry it into a run, and the crash never made
    # that rename. Stale content shaped as a complete snapshot of this very
    # run, a conflicting one, a run.yaml naming another sequence, or a whole
    # recorded run leaves the scan, the latest-run lookup, the first write,
    # its retry and the run's identity exactly as a clean tree has them,
    # and is itself left exactly as it was.
    runs = entries_by_repo(catalog.mechanical_entries(extended_inventory()))
    clean = tmp_path / "clean"
    rid, clean_paths = catalog.write_run(clean, DAY, runs, TAXONOMY)
    snapshot = clean_paths["alpha"].read_bytes()
    conflicting = catalog.render(
        dict(json.loads(snapshot), status="tampered")).encode("utf-8")
    root = tmp_path / "stale"
    staging = root / catalog.STAGING_DIR
    stale = {
        ("alpha.yaml.x1y2z3.tmp",): snapshot,  # complete, never renamed
        ("openxFactory.yaml.k9m8n7.tmp",): conflicting,
        ("run.yaml.p0q9r8.tmp",): catalog.render(
            catalog._run_meta_document(rid, DAY_STR, 7)).encode("utf-8"),
        # A whole run's layout: read as a run, it would claim sequence 7.
        ("f" * 64, "alpha.yaml"): conflicting,
        ("f" * 64, "run.yaml"): catalog.render(
            catalog._run_meta_document("f" * 64, DAY_STR, 7)).encode("utf-8"),
    }
    for rel, content in stale.items():
        node = staging.joinpath(*rel)
        node.parent.mkdir(parents=True, exist_ok=True)
        node.write_bytes(content)
    left = tree_state(staging)

    assert list(catalog._iter_runs(root)) == []
    assert catalog.load_snapshot(root) is None
    assert catalog.write_run(root, DAY, runs, TAXONOMY)[0] == rid
    run_dir = runs_root(root) / DAY_STR / rid
    meta = json.loads((run_dir / "run.yaml").read_text(encoding="utf-8"))
    assert meta["sequence"] == 1  # no stale sequence was ever read
    assert tree_state(runs_root(root) / DAY_STR) == \
        tree_state(runs_root(clean) / DAY_STR)  # the clean tree's run
    assert [(e.as_of, e.sequence, e.run_id, e.refusal)
            for e in catalog._iter_runs(root)] == [(DAY_STR, 1, rid, None)]
    latest = catalog.load_snapshot(root)
    assert latest["repos"] == catalog.load_snapshot(clean)["repos"]
    assert catalog.run_id_scheme(rid, latest["repos"],
                                 catalog._load_run_bytes(root, run_dir)) == \
        catalog.CONTENT_ADDRESSED
    before = tree_state(root)
    assert catalog.write_run(root, DAY, runs, TAXONOMY)[0] == rid  # a no-op
    assert tree_state(root) == before
    assert tree_state(staging) == left  # ignored, never swept


def test_write_run_refuses_a_foreign_staging_directory_before_any_write(
        tmp_path):
    # opensoft/openxFactory#1196: every write passes through the staging
    # directory, so the writer holds it to what it holds every catalog
    # directory it writes through. A symlink there (escaping the catalog
    # root, into a day directory of the tree, or dangling) or a node that
    # is not a directory is refused before anything is claimed, staged or
    # written. A temp staged through such a link would be written outside
    # the catalog tree, or inside a day directory the run scan reads.
    runs = entries_by_repo(catalog.mechanical_entries(extended_inventory()))
    rid = catalog.run_id(runs, TAXONOMY)

    def staging_of(root):
        return root / catalog.STAGING_DIR

    def into_a_day_directory(root, out):
        day = runs_root(root) / "2026-07-01"
        day.mkdir(parents=True)
        plant_link(staging_of(root), day)

    def not_a_directory(root, out):
        staging_of(root).parent.mkdir(parents=True)
        staging_of(root).write_text("occupied\n", encoding="utf-8")

    cases = {
        "symlink-escaping-the-root": (
            lambda root, out: plant_link(staging_of(root), out), "symlink"),
        "symlink-into-a-day-directory": (into_a_day_directory, "symlink"),
        "symlink-dangling": (
            lambda root, out: plant_link(staging_of(root), out / "missing"),
            "symlink"),
        "not-a-directory": (not_a_directory, "occupied"),
    }
    for name, (plant, reason) in cases.items():
        root, outside = tmp_path / name, tmp_path / f"{name}-outside"
        outside.mkdir()
        plant(root, outside)
        before, before_outside = tree_state(root), tree_state(outside)
        with pytest.raises(catalog.CatalogError, match=reason):
            catalog.write_run(root, DAY, runs, TAXONOMY)
        with pytest.raises(catalog.CatalogError, match=reason):
            catalog.write_snapshot(root, DAY, rid, "alpha", runs["alpha"],
                                   TAXONOMY)
        assert tree_state(root) == before, name  # no claim, no snapshot
        assert tree_state(outside) == before_outside, name  # nothing staged
        assert not (runs_root(root) / ".sequence").exists(), name
        assert not (runs_root(root) / DAY_STR).exists(), name


def test_write_run_refuses_a_cross_mount_run_before_any_claim(tmp_path):
    # PR #1199 review (Copilot, two rounds): the atomic-rename check ran
    # only when a write was staged, after the sequence was claimed and the
    # run's directories made, so a staging directory an atomic rename could
    # not publish from left an orphaned claim and a partial run behind,
    # although that refusal depends on the layout alone. And an st_dev match
    # alone passed two bind mounts of one filesystem, between which
    # rename(2) still fails with EXDEV. The preflight now checks every
    # directory the run publishes into against the staging directory, its
    # filesystem AND its mount, before anything is claimed, counting a
    # directory not made yet as its nearest existing ancestor's, where it
    # would be made. A mount is simulated by shifting one id of every node
    # at or below one directory: the device id for another filesystem, the
    # mount id alone for a bind mount of the same filesystem.
    runs = entries_by_repo(catalog.mechanical_entries(extended_inventory()))
    rid = catalog.run_id(runs, TAXONOMY)
    real = {"_device_id": catalog._device_id, "_mount_id": catalog._mount_id}

    def mounted_at(seam, mount):
        def shifted_id(node):
            node = Path(node)
            shift = 1 if node == mount or mount in node.parents else 0
            return (real[seam](node) or 0) + shift
        return shifted_id

    def made(node):
        node.mkdir(parents=True)
        return node

    mounts = {
        "the-staging-directory": lambda root: made(
            root / catalog.STAGING_DIR),
        "a-day-directory": lambda root: made(runs_root(root) / DAY_STR),
        "a-crashed-run-directory": lambda root: made(
            runs_root(root) / DAY_STR / rid),
    }
    for seam in ("_device_id", "_mount_id"):
        for name, mount_of in mounts.items():
            root = tmp_path / seam / name
            mount = mount_of(root)
            before = tree_state(root)
            with pytest.MonkeyPatch.context() as patch:
                patch.setattr(catalog, seam, mounted_at(seam, mount))
                with pytest.raises(catalog.CatalogError,
                                   match="same filesystem and mount") as exc:
                    catalog.write_run(root, DAY, runs, TAXONOMY)
                with pytest.raises(catalog.CatalogError,
                                   match="same filesystem and mount"):
                    catalog.write_snapshot(root, DAY, rid, "alpha",
                                           runs["alpha"], TAXONOMY)
            case = (seam, name)
            assert str(tmp_path) not in str(exc.value), case  # tree-relative
            assert tree_state(root) == before, case
            assert not (runs_root(root) / ".sequence").exists(), case
            assert not (runs_root(root) / DAY_STR / rid / "run.yaml") \
                .exists(), case

        # A run tree mounted whole is one filesystem and one mount: a fresh
        # run records, the directories it has not made yet counted as the
        # mounted one's.
        root = tmp_path / seam / "mounted-whole"
        runs_root(root).mkdir(parents=True)
        with pytest.MonkeyPatch.context() as patch:
            patch.setattr(catalog, seam, mounted_at(seam, runs_root(root)))
            assert catalog.write_run(root, DAY, runs, TAXONOMY)[0] == rid
        assert catalog.load_snapshot(root)["run_id"] == rid, seam
        assert list((root / catalog.STAGING_DIR).iterdir()) == [], seam


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
    # precisely this. Since opensoft/openxFactory#1196 every temp is staged
    # in the catalog's staging directory, never beside its target, so the
    # call names the catalog root and no temp may be left in either place.
    target = tmp_path / "sub" / "run.yaml"
    target.parent.mkdir(parents=True)
    (tmp_path / catalog.RUNS_DIR).mkdir(parents=True)  # the staging parent
    # Distinct AND different-length payloads so any torn interleaving of
    # two writes is detectable as "not equal to any single input".
    inputs = [f"sequence: {i}\n" + "x" * (i * 37) + "\n" for i in range(24)]
    errors = []
    barrier = threading.Barrier(len(inputs))

    def writer(text):
        try:
            barrier.wait()
            catalog._write_rendered(tmp_path, target, text)
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
    # No shared/leaked temp remains beside the published file, or staged.
    leftovers = [p.name for p in target.parent.iterdir()
                 if p.name != "run.yaml"]
    assert leftovers == []
    assert list((tmp_path / catalog.STAGING_DIR).iterdir()) == []


def test_write_rendered_publishes_only_by_an_atomic_rename(tmp_path):
    # opensoft/openxFactory#1196: a staged write is published only by an
    # atomic rename, out of a staging directory the write re-checks at the
    # moment it stages: a symlinked staging directory is refused there too,
    # with nothing written through it. The rename needs the staging and
    # target directories on one filesystem and one mount. The layout keeps
    # them there; were they not, the write is refused, naming tree-relative
    # paths, before anything is staged. A rename that fails anyway
    # (os.replace fails across mounts, never copies) leaves neither the
    # target nor the temp behind. On Linux the mount id is really read.
    target = runs_root(tmp_path) / DAY_STR / ("e" * 64) / "alpha.yaml"
    target.parent.mkdir(parents=True)
    staging = tmp_path / catalog.STAGING_DIR
    outside = tmp_path / "outside"
    outside.mkdir()
    staging.symlink_to(outside, target_is_directory=True)
    with pytest.raises(catalog.CatalogError, match="symlink"):
        catalog._write_rendered(tmp_path, target, "{}\n")
    assert not target.exists() and list(outside.iterdir()) == []
    staging.unlink()

    with pytest.MonkeyPatch.context() as patch:
        patch.setattr(catalog, "_rename_compatible", lambda a, b: False)
        with pytest.raises(catalog.CatalogError,
                           match="same filesystem and mount") as exc:
            catalog._write_rendered(tmp_path, target, "{}\n")
    assert str(tmp_path) not in str(exc.value)  # tree-relative paths only
    assert not target.exists() and list(staging.iterdir()) == []

    def cross_device(src, dst):
        raise OSError(errno.EXDEV, os.strerror(errno.EXDEV))

    with pytest.MonkeyPatch.context() as patch:
        patch.setattr(os, "replace", cross_device)
        with pytest.raises(OSError) as failed:
            catalog._write_rendered(tmp_path, target, "{}\n")
    assert failed.value.errno == errno.EXDEV
    assert not target.exists() and list(staging.iterdir()) == []

    assert catalog._rename_compatible(staging, target.parent)
    assert catalog._mount_id(staging) == catalog._mount_id(target.parent)
    assert catalog._mount_id(staging) is not None or \
        not hasattr(os, "O_PATH") or not Path("/proc/self/fdinfo").is_dir()
    catalog._write_rendered(tmp_path, target, "{}\n")
    assert target.read_bytes() == b"{}\n"
    assert list(staging.iterdir()) == []


def test_every_publish_is_durable_before_the_next_is_staged(tmp_path):
    # PR #1199 review (Copilot, rounds 3 and 4), and the fsync-then-rename
    # order opensoft/openxFactory#1196 keeps. Closing a temp flushes
    # Python's buffer but makes nothing durable, and a rename is a directory
    # entry the disk can still lose: a power loss could undo a snapshot's
    # rename and keep the run.yaml published after it, leaving a recorded
    # run holding no snapshot. Each write of a run now fsyncs its own temp,
    # complete, renames it, and fsyncs the directory it landed in and every
    # directory from that one up to the runs directory, all before the
    # run's next file is staged. A slash-separated repository's snapshot
    # lands in a directory the writer made inside the run, so its chain is
    # one directory longer. The run's sequence claim is made durable the
    # same way before anything of the run is written, so no durable run.yaml
    # names a claim a power loss took.
    alpha = alpha_entries(extended_inventory())
    runs = {"alpha": alpha, "xFactories/MedxFactory": [
        dict(e, repo="xFactories/MedxFactory") for e in alpha]}
    rid = catalog.run_id(runs, TAXONOMY)
    staging = tmp_path / catalog.STAGING_DIR
    real_fsync, real_replace = os.fsync, os.replace
    events = []

    def label(node):
        return Path(node).relative_to(runs_root(tmp_path)).as_posix()

    def fsync(fd):
        inode = os.fstat(fd).st_ino
        claims = runs_root(tmp_path) / ".sequence"
        temps = [p for p in staging.iterdir() if os.lstat(p).st_ino == inode] \
            if staging.is_dir() else []
        claimed = [p for p in claims.iterdir() if p.is_file()
                   and os.lstat(p).st_ino == inode]
        if temps:  # the temp itself, holding what it is about to publish
            events.append(("sync temp", temps[0].name.split(".")[0],
                           temps[0].read_bytes()))
        elif claimed:
            events.append(("sync claim", claimed[0].name,
                           claimed[0].read_bytes()))
        else:
            tree = [runs_root(tmp_path), *(
                p for p in runs_root(tmp_path).rglob("*") if p.is_dir())]
            events.append(("sync directory", [
                label(p) for p in tree if os.lstat(p).st_ino == inode]))
        return real_fsync(fd)

    def replace(src, dst):
        assert Path(src).parent == staging, src
        events.append(("replace", label(dst)))
        return real_replace(src, dst)

    with pytest.MonkeyPatch.context() as patch:
        patch.setattr(os, "fsync", fsync)
        patch.setattr(os, "replace", replace)
        assert catalog.write_run(tmp_path, DAY, runs, TAXONOMY)[0] == rid
    run = f"{DAY_STR}/{rid}"
    published = (("alpha", f"{run}/alpha.yaml", [run, DAY_STR, "."]),
                 ("run", f"{run}/run.yaml", [run, DAY_STR, "."]),
                 ("MedxFactory", f"{run}/xFactories/MedxFactory.yaml",
                  [f"{run}/xFactories", run, DAY_STR, "."]))
    claim = runs_root(tmp_path) / ".sequence" / "000001.yaml"
    expected = [("sync claim", claim.name, claim.read_bytes()),
                ("sync directory", [".sequence"]), ("sync directory", ["."])]
    for name, path, chain in published:
        body = (runs_root(tmp_path) / path).read_bytes()
        expected += [("sync temp", name, body), ("replace", path)]
        expected += [("sync directory", [directory]) for directory in chain]
    assert events == expected
    assert list(staging.iterdir()) == []


class Died(Exception):
    """A writer stopped dead at the moment a test chose."""


def record_durability(patch, root, events, rules=()):
    """Append to `events`, while `patch` holds, every ``os.replace`` as
    ``("replace", <path under the runs directory>)`` and every ``os.fsync``
    of a directory as ``("sync", <path under the runs directory>)``, each
    right after the real call. `rules` pairs an event with a callable run
    once, at that moment: that is how a test pauses a writer immediately
    after one of its renames or syncs, runs another writer there, or stops
    one dead."""
    runs = runs_root(root)
    real_replace, real_fsync = os.replace, os.fsync
    pending = list(rules)

    def label(node):
        return Path(node).relative_to(runs).as_posix()

    def happened(event):
        events.append(event)
        for rule in pending:
            if rule[0] == event:
                pending.remove(rule)
                rule[1]()
                return

    def replace(src, dst):
        real_replace(src, dst)
        happened(("replace", label(dst)))

    def fsync(fd):
        real_fsync(fd)
        found = os.fstat(fd)
        if stat.S_ISDIR(found.st_mode):
            names = [label(p) for p in [runs, *runs.rglob("*")]
                     if p.is_dir() and (os.lstat(p).st_dev, os.lstat(p).st_ino)
                     == (found.st_dev, found.st_ino)]
            happened(("sync", names[0] if names else "?"))

    patch.setattr(os, "replace", replace)
    patch.setattr(os, "fsync", fsync)


def test_a_writer_accepts_another_writers_publish_only_once_durable(tmp_path):
    # PR #1199 review (Copilot, at caf0c029): os.replace makes a file
    # visible before its writer's directory sync runs, and an identical
    # writer running in that window accepted the file as published -- as a
    # completed no-op, by skipping its own write, or by finding the run
    # recorded or complete -- without syncing it, then published a run.yaml
    # over it or reported success. Were the first writer to die before its
    # sync, a power loss could still take what the second had reported
    # recorded. That is sharpest for a slash-separated repository, whose
    # directory no run.yaml sync covers. Every path that accepts a file
    # another writer published now makes it durable itself first. Each case
    # pauses one writer immediately after a rename (in case 3, after its
    # snapshot's last sync), runs the other there, and stops a writer dead
    # before its own sync.
    nested = [dict(e, repo="xFactories/MedxFactory")
              for e in alpha_entries(extended_inventory())]
    runs = {"xFactories/MedxFactory": nested}
    rid = catalog.run_id(runs, TAXONOMY)
    run = f"{DAY_STR}/{rid}"
    snapshot = f"{run}/xFactories/MedxFactory.yaml"
    chain = [f"{run}/xFactories", run, DAY_STR, "."]  # up to the runs dir

    def between(events, start, end):
        return events[events.index(start) + 1:events.index(end)]

    def first_writer(root, rules):
        events = []
        with pytest.MonkeyPatch.context() as patch:
            record_durability(patch, root, events, rules(root, events))
            try:
                assert catalog.write_run(root, DAY, runs, TAXONOMY)[0] == rid
                events.append(("first returns",))
            except Died:
                events.append(("first dies",))
        return events

    def second_runs_then_first_dies(root, events):
        events.append(("second starts",))
        assert catalog.write_run(root, DAY, runs, TAXONOMY)[0] == rid
        events.append(("second returns",))
        raise Died

    def recorded(root, sequence, name=rid):
        latest = catalog.load_snapshot(root)
        assert (latest["run_id"], latest["sequence"]) == (name, sequence)
        assert catalog.run_id_scheme(name, latest["repos"],
                                     catalog._load_run_bytes(
                                         root,
                                         runs_root(root) / DAY_STR / name)) \
            == catalog.CONTENT_ADDRESSED

    # 1. The first writer is paused right after its snapshot's rename, and
    #    dies there. The second finds the snapshot published, so it writes
    #    none: it syncs that snapshot's directory chain, after its own claim,
    #    before its run.yaml names the snapshot.
    root = tmp_path / "after-the-snapshot-rename"
    events = first_writer(root, lambda root, events: [
        (("replace", snapshot),
         lambda: second_runs_then_first_dies(root, events))])
    second = between(events, ("second starts",), ("second returns",))
    published = second.index(("replace", f"{run}/run.yaml"))
    assert [name for _kind, name in second[:published]] == \
        [".sequence", "."] + chain
    assert ("replace", snapshot) not in second and \
        events[-1] == ("first dies",)
    recorded(root, 2)

    # 2. Paused right after its run.yaml's rename, the first writer dies. The
    #    second is a completed no-op: it writes nothing, and syncs the
    #    snapshot's chain, run.yaml's directory included, before it returns.
    root = tmp_path / "after-the-run-yaml-rename"
    events = first_writer(root, lambda root, events: [
        (("replace", f"{run}/run.yaml"),
         lambda: second_runs_then_first_dies(root, events))])
    assert between(events, ("second starts",), ("second returns",)) == \
        [("sync", directory) for directory in chain]
    assert events[-1] == ("first dies",)
    recorded(root, 1)

    # 3. Paused after its snapshot's sync, before it checks for run.yaml, the
    #    first writer lets the second claim, publish run.yaml, and die right
    #    after that rename. The first then finds the run recorded, and syncs
    #    run.yaml's directory chain before it returns. (The "." that follows
    #    "second dies" is the rest of the first writer's own snapshot chain.)
    root = tmp_path / "a-run-yaml-found-after-the-claim"

    def second_publishes_run_yaml_and_dies(root, events):
        events.append(("second starts",))
        with pytest.raises(Died):
            catalog.write_run(root, DAY, runs, TAXONOMY)
        events.append(("second dies",))

    def die():
        raise Died

    events = first_writer(root, lambda root, events: [
        (("sync", DAY_STR),
         lambda: second_publishes_run_yaml_and_dies(root, events)),
        (("replace", f"{run}/run.yaml"), die)])
    assert between(events, ("second dies",), ("first returns",)) == \
        [("sync", "."), ("sync", run), ("sync", DAY_STR), ("sync", ".")]
    recorded(root, 2)

    # 4. A recorded partial run lacks one snapshot, which another writer
    #    renames into place, and dies, just as this call finds the run
    #    complete. The call returns the completed no-op only after syncing
    #    that snapshot's directory chain.
    both = {"alpha": alpha_entries(extended_inventory()),
            "xFactories/MedxFactory": nested}
    both_rid = catalog.run_id(both, TAXONOMY)
    _rid, source = catalog.write_run(tmp_path / "source", DAY, both, TAXONOMY)
    landed_bytes = source["xFactories/MedxFactory"].read_bytes()
    root = tmp_path / "a-complete-run-found-mid-call"
    catalog.write_snapshot(root, DAY, both_rid, "alpha", both["alpha"],
                           TAXONOMY)  # recorded, partial
    both_run = f"{DAY_STR}/{both_rid}"
    real_addresses_itself = catalog._addresses_itself
    events = []

    def addresses_itself(root, run_dir, name):
        if ("another writer renames",) not in events:
            events.append(("another writer renames",))
            (run_dir / "xFactories").mkdir()
            landed = tmp_path / "landed.tmp"
            landed.write_bytes(landed_bytes)
            os.replace(landed, run_dir / "xFactories" / "MedxFactory.yaml")
        return real_addresses_itself(root, run_dir, name)

    with pytest.MonkeyPatch.context() as patch:
        record_durability(patch, root, events)
        patch.setattr(catalog, "_addresses_itself", addresses_itself)
        catalog.write_snapshot(root, DAY, both_rid, "xFactories/MedxFactory",
                               nested, TAXONOMY)
        events.append(("call returns",))
    assert between(events, ("replace",
                            f"{both_run}/xFactories/MedxFactory.yaml"),
                   ("call returns",)) == [
        ("sync", f"{both_run}/xFactories"), ("sync", both_run),
        ("sync", DAY_STR), ("sync", ".")]
    recorded(root, 1, both_rid)
