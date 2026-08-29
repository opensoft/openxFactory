"""Per-family fixture tests: each family finds exactly its fixture's known
violations — a missed or extra finding fails the test."""

from __future__ import annotations

from datetime import date, timedelta
import gzip
import hashlib
import io
import json
import os
from pathlib import Path
import tarfile

from conftest import AS_OF, FakeGit, make_ctx

import doc_health
from doc_health import CRITICAL, ERROR, WARNING, INFO
from doc_health import corpus
from doc_health import families
from doc_health import report
from doc_health.corpus import Doc
from doc_health.families import FAMILIES
from doc_health.runner import Context

from action_pins import assert_actions_pinned, harvest_behavioral, harvest_static


def keys(findings):
    return sorted((f.severity, f.path, f.rule) for f in findings)


def test_status_validity():
    got = FAMILIES["status-validity"](make_ctx("status-validity"))
    assert keys(got) == [
        (ERROR, "docs/freeform.md", "free-form status 'active'"),
        (ERROR, "docs/missing.md", "missing status header"),
    ]
    # PIN (commissioned 2026-08-27, after `promotion_fidelity._ACTION` was
    # mutated and 85 tests stayed green — no doc-health family's action line
    # was pinned anywhere). An action line is operator guidance rendered in
    # every ranked-plan row; nothing else in this repository notices it
    # changing, so each family gets one verbatim pin in its own suite.
    assert {f.path: f.action for f in got} == {
        "docs/freeform.md": "replace with a controlled taxonomy value",
        "docs/missing.md":
            "add a Status: header from the controlled taxonomy",
    }


def test_projection_is_a_controlled_status_and_not_a_record(tmp_path):
    """REGRESSION, 2026-08-28 (`declare-generated-projection-status`).

    `ideation/cross-reference.md` is rewritten in place by
    `scripts/render-ideation-cross-reference.py` on every run, and carried
    `Status: record` — so `record-immutability` reported a CRITICAL for every
    legitimate regeneration, making the correct act a finding. Promoted canon
    in `ideation-cross-reference` already called the index and "its rendered
    twin" generated artifacts that are NOT records; the header contradicted it.

    The ninth standing ends it AT THE ROOT. Both halves are asserted here,
    because either alone would be the wrong fix: `projection` must be a
    CONTROLLED value (so `status-validity` stays silent — the file is not
    merely unrecognised), and it must NOT be a record (so
    `record-immutability` never reaches it). Silencing the family instead
    would have satisfied the second and failed the first.
    """
    from doc_health import TAXONOMY
    assert "projection" in TAXONOMY

    repo = tmp_path / "alpha"
    (repo / "ideation").mkdir(parents=True)
    projected = repo / "ideation/index.md"
    projected.write_text(
        "# Index\n\nStatus: projection\nKind: report\n\n"
        "**GENERATED FILE — do not edit by hand.**\n"
    )

    ctx = make_ctx("status-validity")
    ctx.repo_paths = {"alpha": repo}
    ctx.docs = corpus.load_docs("alpha", repo)
    ctx.lifecycle_docs = []
    assert FAMILIES["status-validity"](ctx) == []

    # A record's capture blob differs from the tree and the family fires; a
    # projection's status makes the family skip before it ever asks git, so
    # the SAME divergence is silent. Asserted against one FakeGit rather than
    # two, so the only difference between the runs is the status value.
    git = FakeGit(captures={
        ("alpha", "ideation/index.md"):
            "# Index\n\nStatus: record\n\nold body\n"})
    ctx.git = git
    assert FAMILIES["record-immutability"](ctx) == []

    # ...and the exemption is not blindness: the same file as a `record`,
    # against the same git, still reports the critical.
    projected.write_text(
        "# Index\n\nStatus: record\nKind: report\n\nnew body\n")
    ctx.docs = corpus.load_docs("alpha", repo)
    got = FAMILIES["record-immutability"](ctx)
    assert [(f.severity, f.path) for f in got] == [
        (CRITICAL, "ideation/index.md")]


def test_standard_backing():
    got = FAMILIES["standard-backing"](make_ctx("standard-backing"))
    assert [(f.severity, f.path) for f in got] == [
        (CRITICAL, "docs/unbacked.md")]
    # PIN, see test_status_validity's docstring comment.
    assert got[0].action == (
        "add a Backed by: line resolving to a promoted spec or canonical "
        "contract, or demote to draft")


def test_ratified_provenance():
    got = FAMILIES["ratified-provenance"](make_ctx("ratified-provenance"))
    assert [(f.severity, f.path) for f in got] == [
        (CRITICAL, "docs/dangling.md")]
    # PIN, see test_status_validity's docstring comment.
    assert got[0].action == (
        "point Ratified by: at an existing active or archived change")


def test_succession_integrity():
    got = FAMILIES["succession-integrity"](make_ctx("succession-integrity"))
    assert sorted((f.severity, f.path) for f in got) == [
        (ERROR, "docs/lost.md"),
        (ERROR, "docs/retired-noreason.md"),
    ]
    # PIN, see test_status_validity's docstring comment.
    assert {f.path: f.action for f in got} == {
        "docs/lost.md":
            "add a Superseded by: line naming the successor document",
        "docs/retired-noreason.md":
            "add a Retired:/Reason: line naming the reason or decision "
            "record",
    }


def test_location_conformance():
    got = FAMILIES["location-conformance"](make_ctx("location-conformance"))
    assert [(f.severity, f.path) for f in got] == [(ERROR, "docs/stray.md")]
    # PIN, see test_status_validity's docstring comment.
    assert got[0].action == (
        "move it under ideation/brainstorm/ or change its status")


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


def test_staged_citation_of_an_archived_proposal_is_silent(tmp_path):
    """REGRESSION, 2026-08-28 (`clean-doc-health-floor` W3). The staged-exit
    arm demanded material "move into the proposal supporting-docs folder"
    even when the cited proposal had ARCHIVED — a closed, immutable packet,
    so the remedy named an act nobody can perform. `corpus.change_ids` unions
    active and archived ids (including the `YYYY-MM-DD-` stripped spelling),
    and the arm read that union, so archived-ness was invisible to it.

    The finding now fires only while the cited proposal is ACTIVE.
    """
    repo = tmp_path / "alpha"
    staged = repo / "ideation/staging/topic-a"
    staged.mkdir(parents=True)
    (staged / "source.md").write_text(
        "# Source\n\nStatus: staged\nKind: architecture\n\n"
        "## Exit\n\nExit: change-a\n"
    )
    # Archived, in the real date-prefixed folder shape `corpus.change_ids`
    # strips — so the id resolves by BOTH spellings and the exemption is
    # proven against the branch that actually matched before this fix.
    archived = repo / "openspec/changes/archive/2026-07-09-change-a"
    archived.mkdir(parents=True)

    ctx = make_ctx("location-conformance")
    ctx.repo_paths = {"alpha": repo}
    ctx.docs = corpus.load_docs("alpha", repo)
    ctx.change_ids = {"alpha": {"change-a", "2026-07-09-change-a"}}
    assert FAMILIES["location-conformance"](ctx) == []
    # The union still carries the id, so this proves the ARM stopped reading
    # it — not that the id stopped resolving.
    assert "change-a" in corpus.change_ids(repo)
    assert corpus.active_change_ids(repo) == set()

    # ...and the exemption is not blindness: give the same citation a live
    # active packet and the finding lands again, unchanged.
    (repo / "openspec/changes/change-a").mkdir(parents=True)
    got = FAMILIES["location-conformance"](ctx)
    assert [(f.severity, f.path, f.rule) for f in got] == [(
        ERROR, "ideation/staging/topic-a/source.md",
        "staged material already cites proposal change-a")]


def test_staged_citation_prefers_the_active_proposal_over_an_archived_one(
        tmp_path):
    """REGRESSION, 2026-08-28 (`clean-doc-health-floor` W3). A staged fragment
    may cite BOTH an archived and an active change — `avatar-pilot-hardening`
    in this repository cites `implement-avatar-client-lab` (archived
    2026-08-04) and `qualify-avatar-live-voice` (active). `_staged_exit_changes`
    returns its ids SORTED and the finding reports `cited[0]`, so the archived
    id won on alphabetical order and hid the performable remedy behind an
    impossible one.

    Narrowing the set to active ids re-points the finding at the change the
    material can actually move into. The row does NOT disappear, and this test
    pins that: the fix is a correction of the named target, not a silencer.
    """
    repo = tmp_path / "alpha"
    staged = repo / "ideation/staging/topic-a"
    staged.mkdir(parents=True)
    # `aaa-change` sorts BEFORE `zzz-change`, so the archived id is the one
    # that would be reported if the union were still read.
    (staged / "source.md").write_text(
        "# Source\n\nStatus: staged\nKind: architecture\n\n"
        "## Exit\n\nBlocked on aaa-change; exits via zzz-change.\n"
    )
    (repo / "openspec/changes/archive/2026-07-09-aaa-change").mkdir(
        parents=True)
    (repo / "openspec/changes/zzz-change").mkdir(parents=True)

    ctx = make_ctx("location-conformance")
    ctx.repo_paths = {"alpha": repo}
    ctx.docs = corpus.load_docs("alpha", repo)
    ctx.change_ids = {"alpha": {"aaa-change", "zzz-change"}}
    got = FAMILIES["location-conformance"](ctx)
    assert [(f.severity, f.path, f.rule) for f in got] == [(
        ERROR, "ideation/staging/topic-a/source.md",
        "staged material already cites proposal zzz-change")]
    # PIN, see test_status_validity's docstring comment.
    assert got[0].action == (
        "move selected material into the proposal supporting-docs folder")


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


def _load_proposal_support():
    """`scripts/proposal-support.py` as a module.

    A hyphenated standalone script, so it is loaded by path rather than
    imported — the reason `doc_health.recorded_rel` is a second copy of that
    module's `manifest_rel` instead of an import of it."""
    import importlib.util

    script = Path(__file__).resolve().parents[2] / "scripts" / "proposal-support.py"
    spec = importlib.util.spec_from_file_location("proposal_support_ref", script)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_the_recorded_path_normalizations_agree(tmp_path):
    """The two readers of one record must not disagree about its alphabet.

    `proposal-support.py verify` and this suite both resolve a support
    manifest's `files[].path` and a proposal's recorded origin path, and a
    record the one called sound while the other called it a checksum mismatch
    (or unresolvable provenance) would be the worst of both. There are exactly
    TWO copies of the rule — one per process boundary: `doc_health.recorded_rel`
    serves the whole package, and the mover keeps its own because a hyphenated
    standalone script cannot be imported. This pins them to each other."""
    reference = _load_proposal_support().manifest_rel
    for value in ("notes/one.md", "notes\\one.md", "source-snapshots\\a\\b.md",
                  "ideation\\staging\\topic-a", "", "a/b", None, 7, ["x"]):
        assert doc_health.recorded_rel(value) == reference(value)


def test_backslash_spelled_manifest_paths_still_resolve(tmp_path):
    """A manifest written by `str(PurePath)` on a Windows checkout spells its
    path fields with backslashes (PR #221's deferred half). Read here they
    become one filename that resolves to nothing, so every entry would report a
    false `checksum mismatch` on files that are present and correct."""
    repo = tmp_path / "alpha"
    support = repo / "openspec/changes/change-a/supporting-docs"
    (support / "notes").mkdir(parents=True)
    (support / "notes/source.md").write_text("# Source\n\nStatus: draft\n")
    (support / "manifest.yaml").write_text(json.dumps({
        "format_version": 1,
        "files": [{
            "path": "notes\\source.md",
            "sha256": hashlib.sha256(
                (support / "notes/source.md").read_bytes()).hexdigest(),
        }],
    }))
    ctx = make_ctx("location-conformance")
    ctx.repo_paths = {"alpha": repo}
    ctx.docs = corpus.load_docs("alpha", repo)
    ctx.change_ids = {"alpha": set()}
    assert FAMILIES["location-conformance"](ctx) == []

    # ...and the tolerance is not blindness: a real mismatch still lands.
    (support / "notes/source.md").write_text("# Source\n\nStatus: draft\n\nx\n")
    ctx.docs = corpus.load_docs("alpha", repo)
    got = FAMILIES["location-conformance"](ctx)
    assert len(got) == 1 and "checksum mismatch" in got[0].rule


def test_backslash_spelled_archive_manifest_paths_still_resolve(tmp_path):
    """The archived half: bundle member names are POSIX on every platform, so a
    backslash-spelled manifest makes the inventory comparison span two
    alphabets and calls a sound bundle corrupt."""
    repo = tmp_path / "alpha"
    directory = repo / "openspec/changes/archive/2026-07-09-change-a"
    directory.mkdir(parents=True)
    content = b"# Source\n\nStatus: draft\n"
    buffer = io.BytesIO()
    with gzip.GzipFile(fileobj=buffer, mode="wb", filename="", mtime=0) as gz:
        with tarfile.open(fileobj=gz, mode="w") as tar:
            info = tarfile.TarInfo("notes/source.md")
            info.size = len(content)
            tar.addfile(info, io.BytesIO(content))
    bundle = buffer.getvalue()
    (directory / "supporting-docs.tar.gz").write_bytes(bundle)
    (directory / "supporting-docs.manifest.yaml").write_text(json.dumps({
        "format_version": 1,
        "bundle": {"sha256": hashlib.sha256(bundle).hexdigest()},
        "files": [{
            "path": "notes\\source.md",
            "sha256": hashlib.sha256(content).hexdigest(),
        }],
    }))
    ctx = make_ctx("location-conformance")
    ctx.repo_paths = {"alpha": repo}
    ctx.docs = []
    ctx.change_ids = {"alpha": {"change-a"}}
    assert FAMILIES["location-conformance"](ctx) == []


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
    # PIN, see test_status_validity's docstring comment.
    assert got[0].action == (
        "revert the content edit or re-issue as a new record")


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
    # PIN, see test_status_validity's docstring comment. `sorted` is stable,
    # so the two (WARNING, "docs/aging.md") ties keep the family's own
    # append order: candidate before draft.
    actions = [f.action for f in sorted(got, key=lambda f: (f.severity, f.path))]
    assert actions == [
        "create the OpenSpec change and add its change= id",
        # MOVED by `settle-aging-staging-topics`. The old line read
        # "progress the topic to a proposal or mark it deferred" and named
        # an act no staged topic could perform: the `document-lifecycle`
        # taxonomy has no `deferred` value for a topic, and this change
        # adds none. The line now names the two records the family honours.
        "progress the topic to a proposal, or record the outcome it "
        "already reached — the primary fragment superseded/retired, or "
        "an Exit taken: line naming the archived change",
        "trend data — no action required",
        "convert the block via an OpenSpec change or drop it",
        "ratify, supersede, or retire the draft",
    ]


# --- staged-topic outcomes (`settle-aging-staging-topics`) ------------------
#
# Six topics, ONE age, one fixture: every topic below is 130 days untouched,
# so each of them fires under the rule as it stood before this change and the
# only thing separating them is the outcome each one records. The three that
# stay is the regression; the three that still fire is the positive control
# that the family did not simply go quiet.
_OUTCOME_TOPICS = ("closed-topic", "exited-topic", "fenced-topic",
                   "inflight-topic", "retired-topic", "stale-topic")


def _outcome_ctx():
    return make_ctx("staged-topic-outcomes", git=FakeGit(last_dates={
        ("alpha", f"ideation/staging/{name}"): date(2026, 3, 1)
        for name in _OUTCOME_TOPICS}))


def test_a_recorded_outcome_stops_a_staged_topic_ageing():
    got = FAMILIES["staged-candidate-aging"](_outcome_ctx())
    assert keys(got) == [
        # `Exit taken:` inside a code fence is an EXAMPLE of the record, so
        # the topic that only shows the grammar keeps ageing.
        (ERROR, "ideation/staging/fenced-topic",
         "staged topic untouched 130 days"),
        # The cited change is ACTIVE: the proposal is in flight, the staged
        # material is `location-conformance`'s move, and the age is half of
        # one live obligation — silencing it would hide the other half.
        (ERROR, "ideation/staging/inflight-topic",
         "staged topic untouched 130 days"),
        # No outcome recorded anywhere: the family's original behaviour,
        # unchanged.
        (ERROR, "ideation/staging/stale-topic",
         "staged topic untouched 130 days"),
    ]


def test_the_three_silenced_topics_are_silenced_for_their_own_reason():
    """Each skip arm alone, so one arm cannot cover another's failure."""
    ctx = _outcome_ctx()
    docs_by_path = {(d.repo, d.path): d for d in ctx.docs}
    archived = families._archived_change_ids(ctx)
    assert "2026-01-05-add-exited-thing" in archived
    assert "add-live-thing" not in archived  # active, and never archived
    staging = ctx.repo_paths["alpha"] / "ideation" / "staging"
    outcome = {
        name: families._topic_outcome(
            ctx, docs_by_path, archived, "alpha",
            ctx.repo_paths["alpha"], staging / name)
        for name in _OUTCOME_TOPICS}
    assert outcome == {
        "closed-topic": "primary fragment is superseded",
        "retired-topic": "primary fragment is retired",
        # read from the staging INDEX's detail section, not from the
        # fragment: the register row is where this corpus records exits.
        "exited-topic": "exit taken: 2026-01-05-add-exited-thing (archived)",
        "fenced-topic": None,
        "inflight-topic": None,
        "stale-topic": None,
    }


def test_an_index_exit_record_binds_to_its_own_topic_section():
    """A neighbouring topic's `Exit taken:` line must not silence this one.

    The index is one document holding every topic's section, so a reader
    that scanned the whole file would silence the entire register the
    moment any one topic recorded an exit.
    """
    ctx = _outcome_ctx()
    index = next(d for d in ctx.docs if d.path == "ideation/staging/INDEX.md")
    assert families._exit_taken_lines(
        families._index_section(index.text, "exited-topic"))
    assert not families._exit_taken_lines(
        families._index_section(index.text, "stale-topic"))


def test_register_lifecycle_consistency():
    got = FAMILIES["register-lifecycle-consistency"](
        make_ctx("register-lifecycle-consistency"))
    rules = sorted(f.rule for f in got)
    assert len(rules) == 2
    assert "DTN-002" in rules[0] and "not a documented alias" in rules[0]
    assert "DTN-003" in rules[1] and "adopted without resolvable" in rules[1]
    # PIN, see test_status_validity's docstring comment.
    by_rule = {f.rule: f.action for f in got}
    dtn002 = next(a for r, a in by_rule.items() if "DTN-002" in r)
    dtn003 = next(a for r, a in by_rule.items() if "DTN-003" in r)
    assert dtn002 == "use a documented lifecycle alias"
    assert dtn003 == "point the adopted entry at its promoted artifact"


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
    # PIN, see test_status_validity's docstring comment.
    record_finding = next(
        f for f in got if f.path == "docs/record-candidate.md")
    assert record_finding.action == (
        "records are excluded from the conversion queue")


def test_submodule_pin_drift(tmp_path):
    ctx = make_ctx("status-validity", agg_root=tmp_path, git=FakeGit(
        pins={"xFactories/alpha": "a" * 40, "openxFactory": "b" * 40},
        remotes={"alpha": "c" * 40, "openxFactory": "b" * 40}))
    (tmp_path / "xFactories/alpha").mkdir(parents=True)
    (tmp_path / "openxFactory").mkdir()
    got = FAMILIES["submodule-pin-drift"](ctx)
    assert [(f.severity, f.path) for f in got] == [
        (WARNING, "xFactories/alpha")]
    # PIN, see test_status_validity's docstring comment.
    assert got[0].action == "sync the submodule pointer or push the submodule"


def _gzip_tar(members: dict) -> bytes:
    """A deterministic `.tar.gz` bundle of `{member_name: content_bytes}`,
    the exact shape `test_clean_and_corrupt_archived_support` builds by hand
    for a single member — factored out here because the table test below
    needs several distinct archived bundles."""
    buffer = io.BytesIO()
    with gzip.GzipFile(fileobj=buffer, mode="wb", filename="", mtime=0) as gz:
        with tarfile.open(fileobj=gz, mode="w") as tar:
            for name, content in members.items():
                info = tarfile.TarInfo(name)
                info.size = len(content)
                tar.addfile(info, io.BytesIO(content))
    return buffer.getvalue()


def test_every_action_string_the_tag_hygiene_family_can_emit_is_pinned_verbatim():
    """`fam_tag_hygiene` raises TWELVE distinct finding classes through its
    local `hit(sev, doc, rule, action)` wrapper — `#448` (`cadc05ec`) pinned
    exactly one of them (`test_tag_hygiene` above, "records are excluded
    from the conversion queue"). Steward follow-up (Brett, 2026-08-28)
    widens that to the whole set, table-driven, in this family's own suite.

    SEVEN are pinned BEHAVIOURALLY: the same read-only
    `fixtures/tag-hygiene/` corpus `test_tag_hygiene` reads already drives
    seven of the twelve through one real run of the family (heading-cross,
    unresolved target=, record-candidate, unmatched close, missing spec=,
    malformed marker, unclosed fence). The remaining FIVE — nested fence,
    missing target=, unresolved supersedes capability, unresolved
    supersedes change=, and the doc-level `spec-candidate` status — have no
    branch in that fixture and are pinned STATICALLY instead: read from
    `families.py`'s own source via `ast`, scoped to `fam_tag_hygiene` (which
    finds its nested `hit` wrapper and every one of its call sites, since
    scoping walks that function's whole subtree rather than filtering a
    flat module walk).
    """
    behavioral = harvest_behavioral(FAMILIES["tag-hygiene"],
                                    make_ctx("tag-hygiene"))
    static = harvest_static(families, functions=frozenset({"fam_tag_hygiene"}))

    EXPECTED_ACTIONS = {
        "close the fence before the heading (document-lifecycle grammar)",
        "candidate blocks cannot nest (document-lifecycle grammar)",
        "add target=<capability> (document-lifecycle grammar)",
        "name a capability under openspec/specs/ or an active change "
        "(document-lifecycle grammar)",
        "records are excluded from the conversion queue",
        "remove or pair the close fence (document-lifecycle grammar)",
        "add the spec= attribute (document-lifecycle grammar)",
        "name an existing capability (document-lifecycle grammar)",
        "name an existing active or archived change (document-lifecycle grammar)",
        "use one of the three canonical marker forms (document-lifecycle grammar)",
        "add the matching /xspec:candidate close fence (document-lifecycle grammar)",
        "candidacy is block-level only; remove the status value",
    }
    assert_actions_pinned(EXPECTED_ACTIONS, behavioral, static,
                          family="tag-hygiene")


def test_every_action_string_the_ratified_provenance_family_can_emit_is_pinned_verbatim():
    """`fam_ratified_provenance` raises FOUR distinct finding classes.
    `#448` pinned one (`test_ratified_provenance` above). All four are
    pinned BEHAVIOURALLY here: three tiny, self-contained `Doc`/`Context`
    scenarios (mirroring `test_ratified_citation_spellings.py`'s own `_run`
    helper, which builds a `Context` directly rather than through
    `conftest.make_ctx` because what is under test is exact header content)
    plus the existing read-only `fixtures/ratified-provenance/` corpus for
    the dangling `Ratified by:` case `test_ratified_provenance` already
    reads. No branch here needs a static fallback.
    """
    def run(text):
        doc = Doc("alpha", "docs/subject.md", text,
                  corpus.parse_status(text), corpus.parse_kind(text))
        ctx = Context(repo_paths={"alpha": Path("/nonexistent")}, docs=[doc],
                      capabilities={}, change_ids={"alpha": {"real-change"}},
                      git=None, thresholds={}, as_of=AS_OF, agg_root=None)
        return families.fam_ratified_provenance(ctx)

    behavioral = harvest_behavioral(FAMILIES["ratified-provenance"],
                                    make_ctx("ratified-provenance"))
    for text in (
            "# Subject\n\nStatus: ratified\n\nNo citation here.\n",
            "# Subject\n\nStatus: ratified\n\nRatified by: some-change\n\n"
            "Ratified: 2026-01-01\n",
            "# Subject\n\nStatus: ratified\n\nRatified: nothing here\n"):
        behavioral |= frozenset(f.action for f in run(text))
    static = harvest_static(families,
                            functions=frozenset({"fam_ratified_provenance"}))

    EXPECTED_ACTIONS = {
        "add Ratified by: <change> where an approving OpenSpec change exists, "
        "otherwise Ratified: naming an approver, a date, or a resolvable "
        "record path",
        "keep exactly one: Ratified by: where an approving OpenSpec change "
        "exists, Ratified: where none does",
        "name at least one of an approver, a date, or a resolvable record "
        "path — or cite the approving change with Ratified by: if one exists",
        "point Ratified by: at an existing active or archived change",
    }
    assert_actions_pinned(EXPECTED_ACTIONS, behavioral, static,
                          family="ratified-provenance")


def test_every_action_string_the_location_conformance_family_can_emit_is_pinned_verbatim(
        tmp_path):
    """`fam_location_conformance` raises TEN distinct finding classes across
    three passes: doc-level brainstorm/staged placement, ACTIVE proposal
    support (`_active_support_findings`), and ARCHIVED proposal support
    (`_archive_support_findings`). `#448` pinned one
    (`test_location_conformance` above). All TEN are pinned BEHAVIOURALLY:
    one consolidated `tmp_path` corpus, modeled on the separate scenarios
    `test_proposal_support_location_conformance` and
    `test_clean_and_corrupt_archived_support` already exercise, packs a
    brainstorm doc, a staged-outside-ideation doc, a staged doc citing an
    active proposal, two active supporting-docs changes (one with no
    manifest plus staged prose, one with a checksum mismatch), three
    archived changes (incomplete, bundle checksum mismatch, member
    inventory mismatch), and a misplaced `specs/` bundle into one run. No
    branch here needs a static fallback.
    """
    repo = tmp_path / "alpha"

    # --- doc-level findings -------------------------------------------
    (repo / "docs").mkdir(parents=True)
    (repo / "docs/stray-brainstorm.md").write_text(
        "# Stray\n\nStatus: brainstorm\n")
    (repo / "docs/stray-staged.md").write_text(
        "# Stray\n\nStatus: staged\nKind: architecture\n")
    staged = repo / "ideation/staging/topic-a"
    staged.mkdir(parents=True)
    (staged / "source.md").write_text(
        "# Source\n\nStatus: staged\nKind: architecture\n\n"
        "## Exit\n\nExit: change-cite\n")
    (repo / "openspec/changes/change-cite").mkdir(parents=True)

    # --- active support: change-a has no manifest + staged prose ------
    support_a = repo / "openspec/changes/change-a/supporting-docs"
    support_a.mkdir(parents=True)
    (support_a / "prose.md").write_text("# Prose\n\nStatus: staged\n")

    # --- active support: change-b has a valid manifest, wrong checksum
    support_b = repo / "openspec/changes/change-b/supporting-docs"
    support_b.mkdir(parents=True)
    (support_b / "prose.md").write_text("# Prose\n\nStatus: draft\n")
    (support_b / "manifest.yaml").write_text(json.dumps({
        "format_version": 1,
        "files": [{"path": "prose.md", "sha256": "0" * 64}],
    }))

    # --- archive: change-c incomplete (bundle, no manifest) -----------
    archive_c = repo / "openspec/changes/archive/change-c"
    archive_c.mkdir(parents=True)
    (archive_c / "supporting-docs.tar.gz").write_bytes(b"x")

    # --- archive: change-d bundle checksum mismatch -------------------
    archive_d = repo / "openspec/changes/archive/change-d"
    archive_d.mkdir(parents=True)
    content_d = b"# D\n\nStatus: draft\n"
    bundle_d = _gzip_tar({"d.md": content_d})
    (archive_d / "supporting-docs.tar.gz").write_bytes(bundle_d + b"corrupt")
    (archive_d / "supporting-docs.manifest.yaml").write_text(json.dumps({
        "format_version": 1,
        "bundle": {"sha256": hashlib.sha256(bundle_d).hexdigest()},
        "files": [{"path": "d.md",
                   "sha256": hashlib.sha256(content_d).hexdigest()}],
    }))

    # --- archive: change-e member inventory mismatch ------------------
    archive_e = repo / "openspec/changes/archive/change-e"
    archive_e.mkdir(parents=True)
    content_e = b"# E\n\nStatus: draft\n"
    bundle_e = _gzip_tar({"e.md": content_e})
    (archive_e / "supporting-docs.tar.gz").write_bytes(bundle_e)
    (archive_e / "supporting-docs.manifest.yaml").write_text(json.dumps({
        "format_version": 1,
        "bundle": {"sha256": hashlib.sha256(bundle_e).hexdigest()},
        "files": [{"path": "WRONG.md",
                   "sha256": hashlib.sha256(content_e).hexdigest()}],
    }))

    # --- misplaced bundle under canonical specs -----------------------
    misplaced = repo / "openspec/specs/cap"
    misplaced.mkdir(parents=True)
    (misplaced / "supporting-docs.tar.gz").write_bytes(b"x")

    ctx = make_ctx("location-conformance")
    ctx.repo_paths = {"alpha": repo}
    ctx.docs = corpus.load_docs("alpha", repo)
    ctx.change_ids = {"alpha": {"change-cite"}}

    behavioral = harvest_behavioral(FAMILIES["location-conformance"], ctx)
    behavioral |= harvest_behavioral(FAMILIES["location-conformance"],
                                     make_ctx("location-conformance"))
    static = harvest_static(
        families,
        functions=frozenset({"fam_location_conformance",
                             "_active_support_findings",
                             "_archive_support_findings"}))

    EXPECTED_ACTIONS = {
        "move it under ideation/brainstorm/ or change its status",
        "move it under ideation/staging/ or change its status",
        "move selected material into the proposal supporting-docs folder",
        "create the proposal supporting-document manifest",
        "change proposed prose to draft or immutable evidence to record",
        "refresh or correct the supporting-document manifest",
        "restore both the readable manifest and compressed bundle",
        "rebuild the deterministic bundle and manifest",
        "restore or rebuild the archive from verified proposal support",
        "move the bundle beside its archived OpenSpec change",
    }
    assert_actions_pinned(EXPECTED_ACTIONS, behavioral, static,
                          family="location-conformance")


def test_every_action_string_the_register_lifecycle_consistency_family_can_emit_is_pinned_verbatim(
        tmp_path):
    """`fam_register_lifecycle_consistency` raises THREE distinct finding
    classes. `#448` pinned two of them
    (`test_register_lifecycle_consistency` above, DTN-002/DTN-003). The
    third — a malformed (fewer than six-column) register row — has no
    branch in the read-only `fixtures/register-lifecycle-consistency/`
    corpus, so this table adds ONE `tmp_path` register carrying all three
    row shapes at once; all three are pinned BEHAVIOURALLY and no static
    fallback is needed.
    """
    repo = tmp_path / "openxFactory"
    (repo / "docs").mkdir(parents=True)
    reg = repo / families.REGISTER_PATH
    reg.write_text(
        "# Register\n\nStatus: staged\n\n"
        "| ID | Topic | Decision | Priority | Status | Likely artifact |\n"
        "| --- | --- | --- | --- | --- | --- |\n"
        "| DTN-001 | Malformed |\n"
        "| DTN-002 | BadAlias | `promote` | P0 | `pending` | `docs/x.md` |\n"
        "| DTN-003 | GhostAdopted | `promote` | P1 | `adopted` | "
        "`contracts/ghost.yaml` |\n")
    ctx = Context(repo_paths={"openxFactory": repo}, docs=[], capabilities={},
                  change_ids={}, git=FakeGit(), thresholds={}, as_of=AS_OF,
                  agg_root=None)

    behavioral = harvest_behavioral(
        FAMILIES["register-lifecycle-consistency"], ctx)
    behavioral |= harvest_behavioral(
        FAMILIES["register-lifecycle-consistency"],
        make_ctx("register-lifecycle-consistency"))
    static = harvest_static(
        families, functions=frozenset({"fam_register_lifecycle_consistency"}))

    EXPECTED_ACTIONS = {
        "restore the six-column register row shape",
        "use a documented lifecycle alias",
        "point the adopted entry at its promoted artifact",
    }
    assert_actions_pinned(EXPECTED_ACTIONS, behavioral, static,
                          family="register-lifecycle-consistency")


def test_every_action_string_the_submodule_pin_drift_family_can_emit_is_pinned_verbatim(
        tmp_path):
    """`fam_submodule_pin_drift` raises TWO distinct finding classes.
    `#448` pinned one (`test_submodule_pin_drift` above, the drift case).
    The other — an unreachable remote — is pinned here BEHAVIOURALLY by
    widening that same scenario with a second pinned submodule whose remote
    the `FakeGit` stub simply has no entry for; no static fallback is
    needed.
    """
    ctx = make_ctx("status-validity", agg_root=tmp_path, git=FakeGit(
        pins={"xFactories/alpha": "a" * 40, "xFactories/beta": "d" * 40,
             "openxFactory": "b" * 40},
        remotes={"alpha": "c" * 40, "openxFactory": "b" * 40}))
    (tmp_path / "xFactories/alpha").mkdir(parents=True)
    (tmp_path / "xFactories/beta").mkdir(parents=True)
    (tmp_path / "openxFactory").mkdir()

    behavioral = harvest_behavioral(FAMILIES["submodule-pin-drift"], ctx)
    static = harvest_static(families,
                            functions=frozenset({"fam_submodule_pin_drift"}))

    EXPECTED_ACTIONS = {
        "sync the submodule pointer or push the submodule",
        "re-run with network access to the submodule remote",
    }
    assert_actions_pinned(EXPECTED_ACTIONS, behavioral, static,
                          family="submodule-pin-drift")


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
    # PIN, see test_status_validity's docstring comment.
    assert got[0].action == "review upstream contract changes and re-pin"


def test_notebook_projection_drift():
    drift = FAMILIES["notebook-projection-drift"]
    ctx = make_ctx("status-validity",
                   notebook=lambda: "[xf-canon] ADD  t\n[xf-drafts] UPD  u\n")
    got = drift(ctx)
    assert len(got) == 1 and got[0].severity == WARNING
    assert "2 pending operations" in got[0].rule
    # PIN, see test_status_validity's docstring comment.
    assert got[0].action == "run the lifecycle notebook sync with --apply"
    # PIN (issue #474): the path slot names a REAL artifact, aggregation-root
    # relative like every other `repo=xFactory` finding, and carries no
    # whitespace. It used to read `(lifecycle notebooks)` — a synthetic label
    # whose space made `PLAN_RE`'s `path=(\S+)` unable to read the row back,
    # so the finding was silently dropped from every `--previous-report`
    # comparison (live at health/reports/2026-07-09.md:188).
    assert got[0].path == "openxFactory/docs/lifecycle-notebook-projection.md"
    assert report.PLAN_RE.match(report.plan_line(got[0])), \
        "the family's own row must round-trip through the ranked plan"

    ctx_clean = make_ctx("status-validity", notebook=lambda: "scan only\n")
    assert drift(ctx_clean) == []

    from doc_health import Skip
    ctx_unauth = make_ctx("status-validity", notebook=lambda: None)
    assert isinstance(drift(ctx_unauth), Skip)


# --------------------------------------------------------------------------
# staged-topic-template (add-staged-topic-outline-template, ratified 2026-08-15)
# --------------------------------------------------------------------------

CONFORMING = """# Staged: a topic

Status: staged
Kind: architecture

## Idea notes (pre-document, non-documented)

Something.

## Conflicts

None.

## Open questions

### Q1. Does it work?

Context: it might not.
Recommended answer: yes.
Explanation: because.
Disposition status: open
"""


def _topic(repo, name, text):
    topic = repo / "ideation/staging" / name
    topic.mkdir(parents=True)
    (topic / f"{name}.md").write_text(text)
    return f"ideation/staging/{name}/{name}.md"


def _ctx_for(tmp_path, topics, first_dates, last_dates=None):
    """`last_dates` is ADDITIVE (task 4.3): the family must read the topic's
    FIRST commit date and nothing else, so proving that needs a context where a
    contradictory LAST commit date is available to be read by mistake."""
    repo = tmp_path / "alpha"
    (repo / "ideation/staging").mkdir(parents=True)
    rels = {name: _topic(repo, name, text) for name, text in topics.items()}
    ctx = make_ctx("location-conformance",
                   git=FakeGit(
                       first_dates={("alpha", rels[name]): d
                                    for name, d in first_dates.items()},
                       last_dates={("alpha", rels[name]): d
                                   for name, d in (last_dates or {}).items()}))
    ctx.repo_paths = {"alpha": repo}
    ctx.docs = corpus.load_docs("alpha", repo)
    return ctx, rels


def test_a_conforming_fragment_produces_no_finding(tmp_path):
    ctx, _ = _ctx_for(tmp_path, {"good": CONFORMING},
                      {"good": date(2026, 9, 1)})
    assert FAMILIES["staged-topic-template"](ctx) == []


def test_non_conformance_is_never_gate_blocking(tmp_path):
    """Q2's ruling: doc-health treats non-conformance as a nudge, NEVER a
    gate-blocking finding — so even a REQUIRED topic warns rather than errors.
    Asserted explicitly because the instinct on a new family is to fail the
    gate, and `--fail-on error` is what would make this block a run."""
    bare = "# Staged: x\n\nStatus: staged\n\n## Claims\n\nNothing.\n"
    ctx, _ = _ctx_for(tmp_path, {"newtopic": bare},
                      {"newtopic": date(2026, 9, 1)})  # after ratification
    got = FAMILIES["staged-topic-template"](ctx)
    assert len(got) == 1
    assert got[0].severity == WARNING
    assert "REQUIRED" in got[0].rule
    # PIN, see test_status_validity's docstring comment. Every finding this
    # family raises carries this one action string, regardless of gap shape
    # or the required/opt-in posture.
    assert got[0].action == (
        "add the missing sections, or give every open question its "
        "Context / Recommended answer / Explanation / Disposition "
        "status sub-fields")


def test_obligation_follows_the_staging_date_not_the_last_touch(tmp_path):
    """A topic staged before the template is opt-in, and editing it for an
    unrelated reason must not silently make it required — which is why the
    family reads first_commit_date, never last_commit_date."""
    bare = "# Staged: x\n\nStatus: staged\n\n## Claims\n\nNothing.\n"
    ctx, _ = _ctx_for(tmp_path, {"oldtopic": bare},
                      {"oldtopic": date(2026, 7, 1)})  # before ratification
    got = FAMILIES["staged-topic-template"](ctx)
    assert len(got) == 1
    assert "opt-in" in got[0].rule and "REQUIRED" not in got[0].rule


def test_an_unknown_staging_date_is_treated_as_opt_in(tmp_path):
    bare = "# Staged: x\n\nStatus: staged\n\n## Claims\n\nNothing.\n"
    ctx, _ = _ctx_for(tmp_path, {"nodate": bare}, {})
    got = FAMILIES["staged-topic-template"](ctx)
    assert len(got) == 1 and "opt-in" in got[0].rule


def test_a_question_missing_sub_fields_is_reported(tmp_path):
    partial = CONFORMING.replace("Explanation: because.\n", "")
    ctx, _ = _ctx_for(tmp_path, {"partial": partial},
                      {"partial": date(2026, 9, 1)})
    got = FAMILIES["staged-topic-template"](ctx)
    assert len(got) == 1
    assert "Explanation" in got[0].rule and "lacks" in got[0].rule


def test_a_fenced_skeleton_does_not_count_as_real_sections(tmp_path):
    """The canonical template ships as a copy-pasteable FENCED skeleton. A
    fragment that merely quotes it has not adopted it."""
    quoting = (
        "# Staged: x\n\nStatus: staged\n\n"
        "Copy this:\n\n```markdown\n"
        "## Idea notes (pre-document, non-documented)\n\n"
        "## Conflicts\n\n## Open questions\n```\n"
    )
    ctx, _ = _ctx_for(tmp_path, {"quoter": quoting},
                      {"quoter": date(2026, 9, 1)})
    got = FAMILIES["staged-topic-template"](ctx)
    assert len(got) == 1
    for label in ("idea notes", "conflicts", "open questions"):
        assert label in got[0].rule


# ---- task 4.1: the conformance rules the existing cases above do not reach ----
#
# What is already proven and deliberately NOT re-proven here: the three required
# sections (`test_a_conforming_fragment_produces_no_finding` +
# `test_a_fenced_skeleton_does_not_count_as_real_sections`), that a missing
# sub-field is named (`test_a_question_missing_sub_fields_is_reported`), and the
# WARNING severity (`test_non_conformance_is_never_gate_blocking`).
#
# What those do not reach is the contract's own emphasis: "A question is never
# recorded bare. The template forces a recommendation and the reasoning for it
# even while the disposition itself stays `open`." The existing case drops
# `Explanation:` from an otherwise complete question — which is a missing field,
# but not the shape the contract is about.


def test_a_bare_question_is_non_conforming_and_names_every_missing_sub_field(tmp_path):
    """"A question is never recorded bare" — the rule task 4.1 names. A heading
    with nothing under it must not pass merely because nothing contradicts the
    four fields; all four are reported, so the human is told what to write rather
    than that something is wrong."""
    bare_question = CONFORMING.split("### Q1.")[0] + "### Q1. Does it work?\n"
    ctx, _ = _ctx_for(tmp_path, {"bare": bare_question},
                      {"bare": date(2026, 9, 1)})
    got = FAMILIES["staged-topic-template"](ctx)
    assert len(got) == 1
    # the three sections are present, so the ONLY gap is the question itself
    assert "no pre-document idea notes section" not in got[0].rule
    # THE FOUR NAMES, LITERALLY — never looped from
    # `families._QUESTION_SUBFIELDS`. Iterating the constant makes the assertion
    # shrink with it: drop a field from the tuple and a loop-driven check simply
    # tests less and still passes. That is the same DIRECTION blindness the two
    # agreement tests have (both assert checker-subset-of-contract and
    # checker-subset-of-model, neither the reverse), and it is why dropping
    # `Recommended answer` from the tuple passed the whole pre-existing suite on
    # both sides.
    for field in ("Context", "Recommended answer", "Explanation",
                  "Disposition status"):
        assert field in got[0].rule, f"{field} not named in: {got[0].rule}"
    # …and the checker still requires exactly those four and no others, so this
    # test and the family cannot drift apart in the other direction either
    assert list(families._QUESTION_SUBFIELDS) == [
        "Context", "Recommended answer", "Explanation", "Disposition status"]
    assert "Q1. Does it work?" in got[0].rule


def test_a_question_with_a_disposition_but_no_recommendation_is_non_conforming(tmp_path):
    """The contract's own named failure, and the one task 4.1 spells out: the
    disposition may stay `open`, but the recommendation and its reasoning are
    still owed. A question carrying only Context and a status is exactly the
    "bare question" the template exists to prevent — an undecided question that
    gives a reader nothing to disagree with."""
    no_recommendation = CONFORMING.replace(
        "Recommended answer: yes.\nExplanation: because.\n", "")
    ctx, _ = _ctx_for(tmp_path, {"norec": no_recommendation},
                      {"norec": date(2026, 9, 1)})
    got = FAMILIES["staged-topic-template"](ctx)
    assert len(got) == 1
    assert "Recommended answer" in got[0].rule
    assert "Explanation" in got[0].rule
    # …and it does NOT claim the fields that ARE there are missing
    assert "Context" not in got[0].rule
    assert "Disposition status" not in got[0].rule


def test_every_incomplete_question_is_reported_not_only_the_first(tmp_path):
    """Open questions is "where the most attention is spent", so a fragment
    carrying several is the normal case. Reporting only the first would send a
    human back for a second round on a fragment they had just fixed."""
    two = CONFORMING + (
        "\n### Q2. And this one?\n\nContext: also unclear.\n"
        "Disposition status: open\n")
    ctx, _ = _ctx_for(tmp_path, {"two": two}, {"two": date(2026, 9, 1)})
    got = FAMILIES["staged-topic-template"](ctx)
    assert len(got) == 1          # one finding per FRAGMENT…
    assert "Q2. And this one?" in got[0].rule
    assert "Recommended answer" in got[0].rule
    # …and Q1, which is complete, is not accused
    assert "Q1" not in got[0].rule


def test_a_third_level_heading_outside_open_questions_is_not_a_question(tmp_path):
    """The four sub-fields are owed by OPEN QUESTIONS, not by every `### `
    heading a fragment happens to carry. Without this the rule would fire on any
    sub-heading anywhere — a spurious finding on much of the corpus, and the kind
    a human learns to ignore, which costs the family its whole value."""
    with_subheading = CONFORMING.replace(
        "## Conflicts\n\nNone.\n",
        "## Conflicts\n\n### With the promoted spec\n\nStated, not resolved.\n")
    ctx, _ = _ctx_for(tmp_path, {"sub": with_subheading},
                      {"sub": date(2026, 9, 1)})
    assert FAMILIES["staged-topic-template"](ctx) == []


# ---- task 4.3: the opt-in boundary, driven from both sides --------------------
#
# Already proven above: a pre-ratification topic is opt-in
# (`test_obligation_follows_the_staging_date_not_the_last_touch`), a
# post-ratification topic is REQUIRED (`test_non_conformance_is_never_gate_blocking`),
# and an unknown date is opt-in (`test_an_unknown_staging_date_is_treated_as_opt_in`).
#
# What those leave open is the BOUNDARY itself and the trap task 2.2 names. The
# discriminator is `staged_on >= TEMPLATE_RATIFIED`, and nothing pinned either
# side of that comparison or proved the family ignores a later touch.

BARE = "# Staged: x\n\nStatus: staged\n\n## Claims\n\nNothing.\n"


def test_the_ratification_day_itself_is_required(tmp_path):
    """`>=`, not `>`. A topic staged ON the day the template ratified was staged
    after it ratified; an off-by-one here would let a whole day of topics claim
    the opt-in posture forever, since obligation never re-derives."""
    ctx, _ = _ctx_for(tmp_path, {"onday": BARE},
                      {"onday": families.TEMPLATE_RATIFIED})
    got = FAMILIES["staged-topic-template"](ctx)
    assert len(got) == 1
    assert "REQUIRED" in got[0].rule and "opt-in" not in got[0].rule


def test_the_day_before_ratification_is_opt_in(tmp_path):
    """The other side of the same comparison, one day away, so the pair fails
    for a `>` and for a `>` written as `>=` on the wrong operand alike."""
    ctx, _ = _ctx_for(tmp_path, {"daybefore": BARE},
                      {"daybefore": families.TEMPLATE_RATIFIED - timedelta(days=1)})
    got = FAMILIES["staged-topic-template"](ctx)
    assert len(got) == 1
    assert "opt-in" in got[0].rule and "REQUIRED" not in got[0].rule


def test_a_topic_touched_long_after_ratification_stays_opt_in(tmp_path):
    """THE TRAP task 2.2 was built to avoid, now driven rather than described.
    An opt-in topic edited for an unrelated reason must not silently become
    required — so the context here offers a contradictory LAST commit date well
    after ratification, and a filesystem mtime of now, and the verdict must still
    be opt-in.

    Swapping `first_commit_date` for `last_commit_date` in the family is noticed
    by four tests, not by this one alone — but this is the only one that ISOLATES
    the trap. The other three notice by accident of an unset fixture: they supply
    no `last_dates` at all, so the swapped call returns None and their expected
    REQUIRED collapses to opt-in. Only here does a topic carry BOTH dates, so only
    here does the failure mean "the family read the wrong one" rather than "the
    fixture had nothing to read"."""
    ctx, rels = _ctx_for(
        tmp_path, {"old": BARE},
        first_dates={"old": date(2026, 7, 1)},     # staged before ratification
        last_dates={"old": date(2026, 9, 30)})     # …and touched long after
    touched = tmp_path / "alpha" / rels["old"]
    os.utime(touched, None)                        # a fresh mtime too
    got = FAMILIES["staged-topic-template"](ctx)
    assert len(got) == 1
    assert "opt-in" in got[0].rule and "REQUIRED" not in got[0].rule


def test_the_boundary_is_judged_per_topic_not_per_run(tmp_path):
    """Q2 means the corpus is deliberately non-uniform for a while, so both
    postures coexist in one run and each topic gets its own verdict — a family
    that decided once per run would mislabel every topic on one side of it."""
    ctx, _ = _ctx_for(tmp_path, {"before": BARE, "after": BARE},
                      {"before": date(2026, 7, 1), "after": date(2026, 9, 1)})
    got = {f.path.split("/")[2]: f.rule
           for f in FAMILIES["staged-topic-template"](ctx)}
    assert set(got) == {"before", "after"}
    assert "opt-in" in got["before"] and "REQUIRED" not in got["before"]
    assert "REQUIRED" in got["after"] and "opt-in" not in got["after"]


def test_the_checker_and_the_contract_text_agree():
    """The template contract lives in `docs/document-lifecycle.md`; the family
    that enforces it reads section names from code constants. Nothing makes
    those two follow each other, so this pins them: every section and sub-field
    the checker requires must actually be named in the ratified prose.

    Without this, editing the doc silently leaves the validator enforcing the
    old contract — the exact drift shape doc-health exists to catch elsewhere.
    """
    repo_root = Path(__file__).resolve().parents[2]
    doc = (repo_root / "docs" / "document-lifecycle.md").read_text()
    section = doc.split("## The Staged-Topic Outline Template", 1)[1]
    section = section.split("\n## Gates In Practice", 1)[0]

    for _needle, label in families._TEMPLATE_SECTIONS:
        assert label.split()[-1] in section.lower(), (
            f"the checker requires a '{label}' section the contract text "
            f"does not name")
    for field in families._QUESTION_SUBFIELDS:
        assert field in section, (
            f"the checker requires the '{field}' sub-field the contract text "
            f"does not name")
