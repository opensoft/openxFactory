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
