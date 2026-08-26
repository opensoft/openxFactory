"""The keystone's two non-negotiables: the generator is DETERMINISTIC (identical
trees yield byte-identical snapshots, no wall clock) and every generated snapshot
CONFORMS to the pinned schema/validator with referential integrity — and it never
mutates the source tree (SC-001 / SC-002 / SC-003; spec US1 Independent Test)."""

from __future__ import annotations

import hashlib

import pytest

from conftest import (  # noqa: F401  (sys.path side effect)
    BASE_REPO, PINNED_REVISION, FakeGit, find_openxfactory_validator,
)

from ideation_dashboard import snapshot
from ideation_dashboard.boundary import OutputBoundary
from ideation_dashboard.generator import generate_snapshot


def _gen(**over):
    kwargs = dict(source_revision=PINNED_REVISION, git=FakeGit())
    kwargs.update(over)
    return generate_snapshot(BASE_REPO, "fixture-repo", **kwargs)


# ---- determinism: byte-identity, no wall clock ----

def test_two_runs_over_unchanged_tree_are_byte_identical():
    first = snapshot.canonical_bytes(_gen())
    second = snapshot.canonical_bytes(_gen())
    assert first == second


def test_generated_at_derives_from_revision_commit_date_not_wall_clock():
    snap = _gen()
    gen = snap["generation"]
    assert gen["source_revision"] == PINNED_REVISION
    # generated_at is the FakeGit commit date for the revision — a fixed value,
    # never `datetime.now()`.
    assert gen["generated_at"] == "2026-07-12T00:00:00+00:00"


def test_source_revision_falls_back_to_git_head_when_unpinned():
    # With no explicit source_revision, the anchor comes from the git abstraction's
    # HEAD (here FakeGit), never a wall-clock stamp.
    snap = generate_snapshot(BASE_REPO, "fixture-repo", git=FakeGit(head="feedface" * 5))
    assert snap["generation"]["source_revision"] == "feedface" * 5


# ---- conformance: schema + validator + referential integrity ----

def test_generated_snapshot_conforms_to_pinned_validator(tmp_path):
    validator = find_openxfactory_validator()
    if validator is None:
        pytest.skip("no reachable openxFactory checkout")
    boundary = OutputBoundary(tmp_path, ["out/"])
    path = snapshot.write_snapshot(_gen(), tmp_path / "out" / "snapshot.json", boundary)
    result = snapshot.validate_snapshot(path, validator=validator, strict=True)
    assert result.ok, result.summary() + "\n" + result.stdout + result.stderr


def test_generated_snapshot_is_referentially_closed(tmp_path):
    # Every edge/claim/pick/option-set/evidence ref resolves — asserted directly
    # so the invariant holds even where a validator is unreachable.
    snap = _gen()
    doc_ids = {d["id"] for d in snap["documents"]}
    cluster_ids = {c["id"] for c in snap["clusters"]}
    possible_ids = {p["id"] for p in snap["possibles"]}
    for c in snap["clusters"]:
        for edge in c["document_edges"]:
            assert edge["document"] in doc_ids
    for p in snap["possibles"]:
        for ref in p.get("claiming_clusters", []):
            assert ref in cluster_ids
        opt = p.get("option_set")
        if opt:
            for member in opt.get("members", []):
                assert member in possible_ids


# ---- non-mutation: the generator only reads ----

def _tree_digest(root):
    h = hashlib.sha256()
    for path in sorted(p for p in root.rglob("*") if p.is_file()):
        h.update(path.relative_to(root).as_posix().encode())
        h.update(b"\0")
        h.update(path.read_bytes())
        h.update(b"\0")
    return h.hexdigest()


def test_generation_does_not_create_edit_or_delete_any_source_document():
    before = _tree_digest(BASE_REPO)
    _gen()
    assert _tree_digest(BASE_REPO) == before
