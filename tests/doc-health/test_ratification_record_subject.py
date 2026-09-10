"""#878: `ratified-provenance` reads a review record's SUBJECT, not only its
`Status:` value.

`document-lifecycle`'s scenario *A review record records a ratification* binds
on the SUBJECT — "WHEN a `review/` document under a change packet records that
the change was ratified, THEN it MUST carry `Status: ratified` and one
ratification citation in a sanctioned spelling". `fam_ratified_provenance`
scoped itself on `doc.status != "ratified": continue`, the header's VALUE, so
a ratification record filed `Status: record` was exactly the document the
scenario governs and exactly the document the family never opened. Measured
consequence: fourteen archived ratification records out of contract with zero
findings (#877), and PR #870's first encode reproduced the drift while
doc-health reported clean.

The neighbouring scenario *A review record is not about a ratification* is the
boundary this must not cross: a `record`-status review whose subject is a
finding, a disposition or a captured review round is SOUND, and a family that
fired on it would have traded one silent gap for a loud false population of
seventy-odd.

Built like `test_ratified_citation_spellings.py` and
`test_families_real_lines.py`: `Doc`/`Context` directly rather than through
`conftest.make_ctx`, because what is under test is exact header content at an
exact path.
"""

from __future__ import annotations

from datetime import date
from pathlib import Path

import pytest

from doc_health import CRITICAL
from doc_health import corpus
from doc_health.corpus import Doc
from doc_health.families import (_RATIFICATION_RECORD_ACTION,
                                 _RATIFICATION_RECORD_RULE,
                                 fam_ratified_provenance)
from doc_health.runner import Context

AS_OF = date(2026, 9, 9)
REPO = "openxFactory"
REPO_ROOT = Path(__file__).resolve().parents[2]

#: A ratification record's path in the shape the packet template writes.
PACKET_RECORD = "openspec/changes/real-change/review/ratification-2026-09-09.md"


def _run(*docs, repo=Path("/nonexistent"), change_ids=("real-change",)):
    ctx = Context(repo_paths={REPO: repo}, docs=list(docs), capabilities={},
                  change_ids={REPO: set(change_ids)}, git=None, thresholds={},
                  as_of=AS_OF, agg_root=None)
    return fam_ratified_provenance(ctx)


def _doc(path, text):
    return Doc(REPO, path, text, corpus.parse_status(text),
               corpus.parse_kind(text))


# --- the three branches the scenario pair draws -------------------------------


def test_a_ratification_record_that_follows_canon_draws_nothing():
    """Branch one: `Status: ratified` plus one citation — the shape the
    scenario asks for, and the shape PR #870's re-derived record follows."""
    text = ("# Proposal Ratification: real-change\n\n"
            "Status: ratified\n"
            "Ratified: 2026-09-09 by Brett Heap\n")
    assert _run(_doc(PACKET_RECORD, text)) == []


def test_a_record_status_ratification_record_is_reported():
    """Branch two: the #878 gap itself. The record's subject IS the
    ratification (its path and its title both say so) and its status is not
    `ratified`, so the scenario is violated and the family must say so."""
    text = ("# Proposal Ratification: real-change\n\n"
            "Status: record\n"
            "Ratified: 2026-09-09 by Brett Heap\n")
    findings = _run(_doc(PACKET_RECORD, text))
    assert [(f.severity, f.family, f.path) for f in findings] == [
        (CRITICAL, "ratified-provenance", PACKET_RECORD)]
    # PIN the operator-facing text: the rule quotes the scenario it enforces,
    # because the remedy is a governance act and a reader who cannot find the
    # rule cannot perform it.
    assert findings[0].rule == _RATIFICATION_RECORD_RULE
    assert findings[0].rule == (
        "a review record that records a ratification must carry Status: "
        "ratified and one citation — document-lifecycle, *A review record "
        "records a ratification*")
    assert findings[0].action == _RATIFICATION_RECORD_ACTION


def test_a_record_status_review_that_is_not_about_a_ratification_draws_nothing():
    """Branch three: the neighbouring scenario. A captured review round, a
    finding, a disposition — a `record`-status review whose subject is not the
    ratification is sound, and seventy-odd of them sit in this corpus."""
    text = ("# Codex review round 2 — real-change\n\n"
            "Status: record\n\nThree findings, two taken.\n")
    path = "openspec/changes/real-change/review/codex-round-2.md"
    assert _run(_doc(path, text)) == []


# --- the two recognizers, and what bounds them --------------------------------


def test_the_title_alone_is_enough_when_the_file_is_named_otherwise():
    """The H1 arm. A ratification record whose author named the file something
    else still declares its subject in its title, and the scenario binds on the
    subject rather than on a naming convention."""
    text = ("# Proposal Ratification: real-change\n\n"
            "Status: record\n\nRatified 2026-09-09.\n")
    path = "openspec/changes/real-change/review/decision.md"
    findings = _run(_doc(path, text))
    assert [f.path for f in findings] == [path]


def test_the_path_alone_is_enough_when_the_title_is_spelled_otherwise():
    """The path arm, and why the title arm cannot stand alone: five of the
    records measured on #877 open `# Ratification — <date>` or `# Ratification
    record — <change>`, so a title-only test would miss a third of the standing
    population."""
    for title in ("# Ratification — 2026-09-09",
                  "# Ratification record — real-change"):
        text = f"{title}\n\nStatus: record\n\nRatified 2026-09-09.\n"
        findings = _run(_doc(PACKET_RECORD, text))
        assert [f.path for f in findings] == [PACKET_RECORD], title


def test_a_ratification_named_document_outside_a_packet_review_dir_is_out_of_scope():
    """`_lifecycle_scope` concatenates the scan set with the GOVERNED CORPUS,
    so a `docs/` document is in this family's scope too. The scenario reaches
    `review/` documents under a change packet, and a policy document about
    ratification is not one."""
    text = ("# Proposal Ratification: how we do it\n\n"
            "Status: record\n\nProse about ratification records.\n")
    assert _run(_doc("docs/ratification-policy.md", text)) == []
    assert _run(_doc("openspec/changes/real-change/review.md", text)) == []


def test_a_title_line_below_the_header_window_is_not_this_document_s_title():
    """The window bound. A `# Proposal Ratification:` line quoted in prose far
    below the header is not the document's H1, and a family that read it as one
    would fire on a record ABOUT ratification records."""
    filler = "".join(f"Filler line {i}.\n" for i in range(20))
    text = ("# Review round\n\nStatus: record\n\n" + filler +
            "# Proposal Ratification: quoted-in-prose\n")
    path = "openspec/changes/real-change/review/notes.md"
    assert len(corpus.split_keepends(text)) > corpus.STATUS_SCAN_LINES, \
        "fixture is broken: the quoted title must sit below the window"
    assert _run(_doc(path, text)) == []


def test_a_ratification_record_with_no_status_header_is_reported():
    """`doc.status is None` is not `"ratified"`, and the scenario's THEN is
    "MUST carry `Status: ratified`" — which an absent header fails as squarely
    as a wrong value. Such a document also draws a `status-validity` finding;
    the two say different things (that family asks for A taxonomy value, this
    one names WHICH), and this corpus holds exactly one such record today."""
    text = "# Ratification — 2026-09-09\n\nRatified 2026-09-09.\n"
    doc = _doc(PACKET_RECORD, text)
    assert doc.status is None, "fixture is broken: the header must be absent"
    assert [f.rule for f in _run(doc)] == [_RATIFICATION_RECORD_RULE]


def test_the_existing_status_value_logic_is_untouched():
    """Everything the family did before #878 it still does: a `ratified`
    document with no citation, with two, and with an unresolvable change all
    keep their own rules, and a `ratified` ratification RECORD is checked by
    those rules rather than by the subject arm."""
    uncited = _doc("docs/subject.md",
                   "# Subject\n\nStatus: ratified\n\nNo citation.\n")
    doubled = _doc("docs/two.md",
                   "# Subject\n\nStatus: ratified\nRatified by: real-change\n"
                   "Ratified: 2026-09-09\n")
    dangling = _doc("docs/dangling.md",
                    "# Subject\n\nStatus: ratified\nRatified by: no-such\n")
    rules = {f.path: f.rule for f in _run(uncited, doubled, dangling)}
    assert rules == {
        "docs/subject.md":
            "ratified header carries no citation in either sanctioned "
            "spelling",
        "docs/two.md": "carries 2 ratification citation lines, not one",
        "docs/dangling.md":
            "Ratified by: missing or does not resolve to an OpenSpec change",
    }
    # A `ratified` ratification record takes the citation path, not the
    # subject arm — the subject arm exists for the records that are NOT
    # `ratified`.
    ok = _doc(PACKET_RECORD,
              "# Proposal Ratification: real-change\n\nStatus: ratified\n"
              "Ratified by: real-change\n")
    assert _run(ok) == []


# --- the standing population, measured on this repository ---------------------


def _packet_ratification_records_not_ratified():
    """Every `review/` ratification record under a change packet on THIS tree —
    ACTIVE AND ARCHIVED ALIKE — whose status is not `ratified`, derived
    independently of the family under test.

    The scenario reaches "a `review/` document under a change packet" and draws
    no line at the archive boundary, so neither does this walk. It restates the
    subject rule in its own code rather than calling the family's
    `_records_a_ratification`, which is the independence that matters; the
    fifteen-line header window is not an implementation detail it could
    honestly vary — `_h1`'s docstring makes the window part of the rule, on
    `align-status-reader-to-real-lines`' wide ruling — so it is mirrored
    exactly, splitting on the same real-line rule the status beside it is read
    with.
    """
    out = {}
    base = REPO_ROOT / "openspec" / "changes"
    for path in sorted(base.glob("*/review/*.md")) + sorted(
            base.glob("archive/*/review/*.md")):
        rel = path.relative_to(REPO_ROOT).as_posix()
        text = path.read_text(encoding="utf-8", errors="replace")
        title = next((body for body, _ending
                      in corpus.split_keepends(text)[:corpus.STATUS_SCAN_LINES]
                      if body.startswith("# ")), "")
        subject = (path.name.startswith("ratification-")
                   or title.startswith("# Proposal Ratification:"))
        if subject and corpus.parse_status(text) != "ratified":
            out[rel] = corpus.parse_status(text)
    return out


#: The fourteen archived records #877 measured on `main` at 2026-09-10T00:26Z,
#: every one titled *Proposal Ratification: <change>* or *Ratification — …* and
#: carrying a `Ratified:` line while filed `Status: record`. Pinned here as the
#: measurement this change was authored against, NOT as the whole population:
#: the population moves (a change archived after that measurement with the same
#: drifted spelling joins it; #877's discharge removes one), so the assertion
#: below is a biconditional against each record's own status rather than an
#: equality against a frozen list that would red `main` either way.
ISSUE_877_FOURTEEN = (
    "openspec/changes/archive/2026-09-04-add-per-change-sweep-ledger/review/ratification-2026-09-04.md",
    "openspec/changes/archive/2026-09-04-create-medxchart-overlay-boundary/review/ratification-2026-09-03.md",
    "openspec/changes/archive/2026-09-04-create-medxpractice-overlay-boundary/review/ratification-2026-09-03.md",
    "openspec/changes/archive/2026-09-05-add-release-tag-gate/review/ratification-2026-09-05.md",
    "openspec/changes/archive/2026-09-05-amend-published-tip-unreadable-scenario/review/ratification-2026-09-05.md",
    "openspec/changes/archive/2026-09-05-amend-unreadable-read-sibling-scenarios/review/ratification-2026-09-05.md",
    "openspec/changes/archive/2026-09-06-amend-marker-reason-boundary/review/ratification-2026-09-06.md",
    "openspec/changes/archive/2026-09-07-amend-absent-changelog-is-an-answer/review/ratification-2026-09-07.md",
    "openspec/changes/archive/2026-09-08-publish-openspec-cli-pin-as-contract-member/review/ratification-2026-09-07.md",
    "openspec/changes/archive/2026-09-09-add-openspec-cli-pin/review/ratification-2026-09-04.md",
    "openspec/changes/archive/2026-09-09-amend-marker-defect-reporting/review/ratification-2026-09-09.md",
    "openspec/changes/archive/2026-09-09-bump-openspec-cli-pin-to-1.12/review/ratification-2026-09-05.md",
    "openspec/changes/archive/2026-09-09-pin-openspec-cli-dependency-closure/review/ratification-2026-09-09.md",
    "openspec/changes/archive/2026-09-09-refresh-install-repository-enumerations/review/ratification-2026-09-09.md",
)


@pytest.fixture(scope="module")
def real_repo_subject_findings():
    """The family, run over THIS repository's own lifecycle scan set."""
    docs = corpus.load_lifecycle_docs(REPO, REPO_ROOT)
    ctx = Context(repo_paths={REPO: REPO_ROOT}, docs=docs, capabilities={},
                  change_ids={REPO: corpus.change_ids(REPO_ROOT)}, git=None,
                  thresholds={}, as_of=AS_OF, agg_root=None)
    return [f for f in fam_ratified_provenance(ctx)
            if f.rule == _RATIFICATION_RECORD_RULE]


def test_the_subject_arm_reports_exactly_the_packet_population_this_tree_carries(
        real_repo_subject_findings):
    """The family's reach over the real packet corpus — active packets and the
    archive together — equals an independent walk of it, so the arm is measured
    against the tree rather than against a number somebody typed.

    A BICONDITIONAL AGAINST THE TREE, never an equality against a frozen list,
    for the reason `ISSUE_877_FOURTEEN` states below: the population moves
    under this test on somebody else's merge (a packet archived, a record
    repaired, a new record written), and `pytest-suite` is a REQUIRED check on
    every pull request in this repository. A measurement that has to be edited
    whenever the corpus moves is a measurement that reds `main` for a reason
    the person who reads the failure did not cause.
    """
    reported = {f.path for f in real_repo_subject_findings}
    assert reported == set(_packet_ratification_records_not_ratified())


def test_every_record_issue_877_named_is_reported_while_it_still_carries_its_status(
        real_repo_subject_findings):
    """#877's fourteen, each pinned to its own status: reported exactly while
    it is not `ratified`, silent the moment it is. All fourteen were
    `Status: record` when this test was written, so all fourteen fire today;
    when #877 is discharged by whichever mechanism the lifecycle owner chooses,
    this test follows the discharge instead of blocking it."""
    reported = {f.path for f in real_repo_subject_findings}
    for rel in ISSUE_877_FOURTEEN:
        path = REPO_ROOT / rel
        assert path.is_file(), f"#877 named a record this tree does not carry: {rel}"
        status = corpus.parse_status(
            path.read_text(encoding="utf-8", errors="replace"))
        assert (rel in reported) == (status != "ratified"), (
            f"{rel} carries Status: {status!r} and is "
            f"{'reported' if rel in reported else 'not reported'}")


def test_the_subject_arm_draws_no_line_at_the_archive_boundary():
    """The scenario says "a `review/` document under a change packet" and draws
    no line at the archive boundary, so neither does the family.

    PINNED SYNTHETICALLY — one record's exact text at an active packet path and
    at an archived one, both reported — because the POPULATION IS NOT THE CLAIM.
    An assertion that the real tree still carries an unrepaired ACTIVE record
    would pass today (six do) and red `main` on the day that population is
    discharged, which is the whole trap `ISSUE_877_FOURTEEN`'s biconditional
    exists to avoid, sprung on a REQUIRED check by the test standing beside it.
    The real-tree reach over both halves is measured by the equality above; the
    rule itself is pinned here, where no merge can move it.

    The distinction the boundary DOES draw is the remedy, not the rule: an
    active packet's record is repaired by editing it, while an archived one
    takes the archived-record edit route (`record-immutability`,
    `govern-archived-record-edits`) — which is why one shared action string
    names both routes rather than two findings splitting them.
    """
    text = ("# Proposal Ratification: real-change\n\n"
            "Status: record\n"
            "Ratified: 2026-09-09 by Brett Heap\n")
    archived = ("openspec/changes/archive/2026-09-09-real-change/review/"
                "ratification-2026-09-09.md")
    assert not PACKET_RECORD.startswith("openspec/changes/archive/"), \
        "fixture is broken: PACKET_RECORD must be an ACTIVE packet path"
    assert [f.path for f in _run(_doc(PACKET_RECORD, text))] == [PACKET_RECORD]
    assert [f.path for f in _run(_doc(archived, text))] == [archived]
