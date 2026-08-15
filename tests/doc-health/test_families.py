"""Per-family fixture tests: each family finds exactly its fixture's known
violations — a missed or extra finding fails the test."""

from __future__ import annotations

from datetime import date
import gzip
import hashlib
import io
import json
from pathlib import Path
import tarfile

from conftest import AS_OF, FakeGit, make_ctx

from doc_health import CRITICAL, ERROR, WARNING, INFO
from doc_health import corpus
from doc_health.families import FAMILIES


def keys(findings):
    return sorted((f.severity, f.path, f.rule) for f in findings)


def test_status_validity():
    got = FAMILIES["status-validity"](make_ctx("status-validity"))
    assert keys(got) == [
        (ERROR, "docs/freeform.md", "free-form status 'active'"),
        (ERROR, "docs/missing.md", "missing status header"),
    ]


def test_standard_backing():
    got = FAMILIES["standard-backing"](make_ctx("standard-backing"))
    assert [(f.severity, f.path) for f in got] == [
        (CRITICAL, "docs/unbacked.md")]


def test_ratified_provenance():
    got = FAMILIES["ratified-provenance"](make_ctx("ratified-provenance"))
    assert [(f.severity, f.path) for f in got] == [
        (CRITICAL, "docs/dangling.md")]


def test_succession_integrity():
    got = FAMILIES["succession-integrity"](make_ctx("succession-integrity"))
    assert sorted((f.severity, f.path) for f in got) == [
        (ERROR, "docs/lost.md"),
        (ERROR, "docs/retired-noreason.md"),
    ]


def test_location_conformance():
    got = FAMILIES["location-conformance"](make_ctx("location-conformance"))
    assert [(f.severity, f.path) for f in got] == [(ERROR, "docs/stray.md")]


def test_proposal_support_location_conformance(tmp_path):
    repo = tmp_path / "alpha"
    staged = repo / "ideation/staging/topic-a"
    staged.mkdir(parents=True)
    (staged / "source.md").write_text(
        "# Source\n\nStatus: staged\nKind: architecture\n\n"
        "Exit: change-a\n"
    )
    (staged / "evidence.md").write_text(
        "# Evidence\n\nStatus: staged\nKind: reference\n\n"
        "Source: change-a\n"
    )
    support = repo / "openspec/changes/change-a/supporting-docs"
    support.mkdir(parents=True)
    (support / "source.md").write_text("# Source\n\nStatus: staged\n")
    (support / "manifest.yaml").write_text(json.dumps({
        "format_version": 1,
        "files": [{"path": "source.md", "sha256": "bad"}],
    }))
    misplaced = repo / "openspec/specs/cap"
    misplaced.mkdir(parents=True)
    (misplaced / "supporting-docs.tar.gz").write_bytes(b"x")

    ctx = make_ctx("location-conformance")
    ctx.repo_paths = {"alpha": repo}
    ctx.docs = corpus.load_docs("alpha", repo)
    ctx.change_ids = {"alpha": {"change-a"}}
    got = FAMILIES["location-conformance"](ctx)
    rules = "\n".join(f.rule for f in got)
    assert "already cites proposal change-a" in rules
    assert not any(f.path.endswith("evidence.md") for f in got)
    assert "staged status under active proposal support" in rules
    assert "active proposal support checksum mismatch" in rules
    assert "under canonical specs" in rules


def test_source_snapshots_keep_their_staged_status(tmp_path):
    """REGRESSION, 2026-08-15. `source-snapshots/` holds BYTE-EXACT copies of
    the staged files as they were at the move, and the manifest proves that
    with a per-file sha256. Their `Status: staged` is therefore CORRECT, and
    the usual remedy — rewrite it to `draft` — would falsify the snapshot and
    break the checksum it exists to support.

    Nothing exercised this until the first mover-produced bundle landed, at
    which point a correct snapshot became a standing ERROR on the change that
    produced it. Proposal prose beside the snapshots is still checked."""
    repo = tmp_path / "alpha"
    support = repo / "openspec/changes/change-a/supporting-docs"
    (support / "source-snapshots").mkdir(parents=True)
    # the immutable record: staged, and legitimately so
    (support / "source-snapshots/source.md").write_text(
        "# Source\n\nStatus: staged\nKind: architecture\n")
    # live proposal prose beside it, correctly transitioned
    (support / "source.md").write_text("# Source\n\nStatus: draft\n")
    (support / "manifest.yaml").write_text(json.dumps({
        "format_version": 1,
        "files": [{
            "path": "source.md",
            "sha256": hashlib.sha256(
                (support / "source.md").read_bytes()).hexdigest(),
        }],
    }))

    ctx = make_ctx("location-conformance")
    ctx.repo_paths = {"alpha": repo}
    ctx.docs = corpus.load_docs("alpha", repo)
    ctx.change_ids = {"alpha": set()}
    got = FAMILIES["location-conformance"](ctx)

    assert not any("source-snapshots" in f.path for f in got), (
        "a byte-exact snapshot must not be reported for the status it records")
    assert not any(
        "staged status under active proposal support" in f.rule for f in got)

    # ...and the exemption is scoped to snapshots: prose that really is still
    # staged is caught.
    (support / "source.md").write_text("# Source\n\nStatus: staged\n")
    ctx.docs = corpus.load_docs("alpha", repo)
    got = FAMILIES["location-conformance"](ctx)
    assert any(
        "staged status under active proposal support" in f.rule for f in got)


def test_clean_and_corrupt_archived_support(tmp_path):
    repo = tmp_path / "alpha"
    directory = repo / "openspec/changes/archive/2026-07-09-change-a"
    directory.mkdir(parents=True)
    content = b"# Source\n\nStatus: draft\n"
    buffer = io.BytesIO()
    with gzip.GzipFile(fileobj=buffer, mode="wb", filename="", mtime=0) as gz:
        with tarfile.open(fileobj=gz, mode="w") as tar:
            info = tarfile.TarInfo("source.md")
            info.size = len(content)
            tar.addfile(info, io.BytesIO(content))
    bundle = buffer.getvalue()
    (directory / "supporting-docs.tar.gz").write_bytes(bundle)
    (directory / "supporting-docs.manifest.yaml").write_text(json.dumps({
        "format_version": 1,
        "bundle": {"sha256": hashlib.sha256(bundle).hexdigest()},
        "files": [{
            "path": "source.md",
            "sha256": hashlib.sha256(content).hexdigest(),
        }],
    }))
    ctx = make_ctx("location-conformance")
    ctx.repo_paths = {"alpha": repo}
    ctx.docs = []
    ctx.change_ids = {"alpha": {"change-a"}}
    assert FAMILIES["location-conformance"](ctx) == []
    (directory / "supporting-docs.tar.gz").write_bytes(bundle + b"x")
    got = FAMILIES["location-conformance"](ctx)
    assert len(got) == 1 and "bundle checksum mismatch" in got[0].rule


def test_record_immutability():
    fixture = Path(__file__).parent / "fixtures/record-immutability/alpha"
    git = FakeGit(captures={
        ("alpha", "docs/mutated.md"):
            "# Mutated\n\nStatus: record\n\nOriginal body.\n",
        ("alpha", "docs/linkfix.md"):
            (fixture / "docs/linkfix.md").read_text()
            .replace("new-target.md", "old-target.md"),
    })
    got = FAMILIES["record-immutability"](make_ctx("record-immutability",
                                                   git=git))
    assert [(f.severity, f.path) for f in got] == [
        (CRITICAL, "docs/mutated.md")]


def test_staged_candidate_aging():
    git = FakeGit(
        last_dates={
            ("alpha", "ideation/staging/old-topic"): date(2026, 3, 1),
            ("alpha", "docs/aging.md"): date(2026, 4, 1),
            ("alpha", "ideation/staging/old-topic/fragment.md"):
                date(2026, 3, 1),
        },
        line_dates={
            ("alpha", "docs/aging.md", 5): date(2026, 6, 1),   # candidate
            ("alpha", "docs/aging.md", 9): date(2026, 5, 1),   # supersedes
        })
    got = FAMILIES["staged-candidate-aging"](
        make_ctx("staged-candidate-aging", git=git))
    by_sev = sorted((f.severity, f.path) for f in got)
    assert by_sev == [
        (ERROR, "docs/aging.md"),                 # supersedes 69d >= 45
        (ERROR, "ideation/staging/old-topic"),    # topic 130d >= 90
        (INFO, "(drafts)"),                       # age distribution
        (WARNING, "docs/aging.md"),               # candidate 38d >= 30
        (WARNING, "docs/aging.md"),               # draft 99d >= 60
    ]


def test_register_lifecycle_consistency():
    got = FAMILIES["register-lifecycle-consistency"](
        make_ctx("register-lifecycle-consistency"))
    rules = sorted(f.rule for f in got)
    assert len(rules) == 2
    assert "DTN-002" in rules[0] and "not a documented alias" in rules[0]
    assert "DTN-003" in rules[1] and "adopted without resolvable" in rules[1]


def test_tag_hygiene():
    got = FAMILIES["tag-hygiene"](make_ctx("tag-hygiene"))
    by_path = {}
    for f in got:
        by_path.setdefault(f.path, []).append(f.rule)
    assert set(by_path) == {"docs/violations.md", "docs/record-candidate.md"}
    assert len(by_path["docs/violations.md"]) == 7
    assert len(by_path["docs/record-candidate.md"]) == 1
    rules = "\n".join(by_path["docs/violations.md"])
    for expected in ("malformed", "unresolved target=ghost-capability",
                     "crosses heading", "unmatched candidate close",
                     "without spec=<capability>/<requirement>",
                     "unclosed candidate fence"):
        assert expected in rules, expected
    assert "record document" in by_path["docs/record-candidate.md"][0]


def test_submodule_pin_drift(tmp_path):
    ctx = make_ctx("status-validity", agg_root=tmp_path, git=FakeGit(
        pins={"xFactories/alpha": "a" * 40, "openxFactory": "b" * 40},
        remotes={"alpha": "c" * 40, "openxFactory": "b" * 40}))
    (tmp_path / "xFactories/alpha").mkdir(parents=True)
    (tmp_path / "openxFactory").mkdir()
    got = FAMILIES["submodule-pin-drift"](ctx)
    assert [(f.severity, f.path) for f in got] == [
        (WARNING, "xFactories/alpha")]


def test_contract_copy_drift(tmp_path):
    ctx = make_ctx("status-validity", git=FakeGit(heads={
        "openxFactory": "e" * 40}))
    openx = tmp_path / "openxFactory"
    beta = tmp_path / "beta"
    openx.mkdir(), beta.mkdir()
    (beta / "stack.yaml").write_text(
        "xfactory:\n  contract_ref: " + "f" * 40 + "\n")
    ctx.repo_paths = {"openxFactory": openx, "beta": beta}
    got = FAMILIES["contract-copy-drift"](ctx)
    assert [(f.severity, f.repo, f.path) for f in got] == [
        (WARNING, "beta", "stack.yaml")]


def test_notebook_projection_drift():
    drift = FAMILIES["notebook-projection-drift"]
    ctx = make_ctx("status-validity",
                   notebook=lambda: "[xf-canon] ADD  t\n[xf-drafts] UPD  u\n")
    got = drift(ctx)
    assert len(got) == 1 and got[0].severity == WARNING
    assert "2 pending operations" in got[0].rule

    ctx_clean = make_ctx("status-validity", notebook=lambda: "scan only\n")
    assert drift(ctx_clean) == []

    from doc_health import Skip
    ctx_unauth = make_ctx("status-validity", notebook=lambda: None)
    assert isinstance(drift(ctx_unauth), Skip)
