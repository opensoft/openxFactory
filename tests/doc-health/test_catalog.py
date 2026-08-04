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
import shutil
import threading
from datetime import datetime

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


def write_run(root, inv, as_of=DAY, taxonomy=None):
    """One full mechanical pass: entries -> per-repository snapshots."""
    taxonomy = TAXONOMY if taxonomy is None else taxonomy
    rid = catalog.run_id(inv, taxonomy)
    entries = catalog.mechanical_entries(inv)
    paths = {}
    for repo in sorted({e["repo"] for e in entries}):
        paths[repo] = catalog.write_snapshot(
            root, as_of, rid, repo,
            [e for e in entries if e["repo"] == repo], taxonomy)
    return rid, paths


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
    rid = catalog.run_id(inv, TAXONOMY)
    alpha_path = catalog.write_snapshot(
        root, DAY, rid, "alpha",
        [e for e in entries if e["repo"] == "alpha"], TAXONOMY)
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
    # The snapshot writer refuses them too, before anything lands.
    rid = catalog.run_id(inv, TAXONOMY)
    with pytest.raises(ValueError, match="ambiguous"):
        catalog.write_snapshot(tmp_path / "agg", DAY, rid,
                               entries[0]["repo"], [both], TAXONOMY)
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


def test_run_id_is_inventory_and_taxonomy_derived():
    inv = extended_inventory()
    rid = catalog.run_id(inv)
    assert rid == catalog.run_id(extended_inventory())  # no wall clock
    assert rid == inventory.snapshot_id(inv)
    # Any corpus change — content or revision — is a different run.
    assert catalog.run_id(extended_inventory(WORKSPACE, LATER_HEADS)) != rid
    # The effective taxonomy digest folds into run identity, so a
    # taxonomy change over an unchanged corpus is a new run too.
    with_taxonomy = catalog.run_id(inv, TAXONOMY)
    assert with_taxonomy != rid
    assert with_taxonomy == catalog.run_id(extended_inventory(), TAXONOMY)
    other = catalog.effective_taxonomy(
        [dict(registry_inputs()[0], registry_version="9")])
    assert catalog.run_id(inv, other) != with_taxonomy


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
    inv = extended_inventory()
    rid = catalog.run_id(inv, TAXONOMY)
    alpha = [e for e in catalog.mechanical_entries(inv)
             if e["repo"] == "alpha"]
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
    inv = extended_inventory()
    rid = catalog.run_id(inv, TAXONOMY)
    alpha = [e for e in catalog.mechanical_entries(inv)
             if e["repo"] == "alpha"]
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
    rid = catalog.run_id(inv, TAXONOMY)
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
    rid = catalog.run_id(inv, TAXONOMY)
    path = catalog.write_snapshot(root, DAY, rid, "xFactories/MedxFactory",
                                  entries, TAXONOMY)
    assert path == (runs_root(root) / DAY_STR / rid
                    / "xFactories" / "MedxFactory.yaml")
    loaded = catalog.load_snapshot(root)
    assert sorted(loaded["repos"]) == ["xFactories/MedxFactory"]


def test_snapshot_path_boundaries_are_enforced(tmp_path):
    root = tmp_path / "agg"
    inv = extended_inventory()
    rid = catalog.run_id(inv, TAXONOMY)
    alpha = [e for e in catalog.mechanical_entries(inv)
             if e["repo"] == "alpha"]
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
