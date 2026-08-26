"""sanction-ratified-record-spelling: both sanctioned ratification citation
spellings, each pinned to its own rule.

`Ratified by: <change>` is the primary spelling and keeps the change-id
resolution it has always had. `Ratified:` is the record-citing alternative,
legal only where no approving OpenSpec change exists to name, and it is held
to the three-way floor instead — an approver, a date, or a resolvable record
path, any ONE of which suffices.

Four boundaries here are load-bearing rather than incidental, and each has a
test whose only job is to fail if the boundary moves:

- the floor MUST NOT reach `Ratified by:`. Thirteen of the governed
  documents carrying that spelling name their change and nothing else — no
  approver, no date, no path — and applying the floor across both spellings
  would convert all thirteen from correct to CRITICAL in one commit.
- the floor MUST NOT RESCUE `Ratified by:` either — the mirror loosening.
  A primary line naming an approver and a date but no resolvable change is
  still a finding, because the named change IS that spelling's citation.
  The corpus writes that shape eighteen times under `openspec/`, so the day
  those roots become governed is the day a rescue would go quietly live.
- "exactly one citation" is counted as ONE TOTAL across both spellings, so
  the SAME spelling twice is the same violation as one of each. A reader
  that stops at the first match per prefix cannot enforce that, which is
  why `fam_ratified_provenance` reads through `_header_lines`.
- the reader MUST stay two distinct prefixes and MUST NOT collapse to
  `_header_line(doc, "Ratified")`. `_header_line` matches with
  `body.startswith(prefix)`, so the short prefix also matches body prose
  opening with the word — and because every such line in today's corpus sits
  below the header window, the short prefix would pass a test suite written
  against today's corpus and mis-fire on the first document whose HEADER
  window opens with one. The fixtures below put exactly that line inside the
  window, where the difference is observable.

This module builds its `Context`/`Doc` directly rather than through
`conftest.make_ctx`'s fixture-directory mechanism, following
`test_families_real_lines.py`: what is under test is exact header content and
exact line placement, which is far more precisely controlled as a literal
string than as a checked-in fixture tree.
"""

from __future__ import annotations

from datetime import date

import pytest

from doc_health import CRITICAL
from doc_health import corpus
from doc_health.corpus import Doc
from doc_health.families import fam_ratified_provenance
from doc_health.runner import Context

AS_OF = date(2026, 8, 22)
REPO = "openxFactory"
DOC_PATH = "docs/subject.md"

#: A record the citation's record axis can actually resolve to. Deliberately
#: carries NO date in its name — a dated filename would satisfy the date axis
#: too and the record-axis test would stop isolating the record axis.
RECORD_REL = "review/ratification-record.md"


@pytest.fixture
def repo(tmp_path):
    (tmp_path / "docs").mkdir()
    (tmp_path / "review").mkdir()
    (tmp_path / RECORD_REL).write_text("# ratification record\n")
    return tmp_path


def _run(text, repo, change_ids=("real-change",)):
    doc = Doc(REPO, DOC_PATH, text,
              corpus.parse_status(text), corpus.parse_kind(text))
    assert doc.status == "ratified", "fixture is broken: status must be ratified"
    ctx = Context(
        repo_paths={REPO: repo}, docs=[doc], capabilities={},
        change_ids={REPO: set(change_ids)}, git=None, thresholds={},
        as_of=AS_OF, agg_root=None)
    return fam_ratified_provenance(ctx)


def _rules(findings):
    return [(f.severity, f.family, f.rule) for f in findings]


def _only_rule(findings):
    assert len(findings) == 1, f"expected exactly one finding, got {findings}"
    assert findings[0].severity == CRITICAL
    assert findings[0].family == "ratified-provenance"
    return findings[0].rule


# ------------------------------------------------- the record-citing floor


def test_record_citation_naming_only_an_approver_is_clean(repo):
    """Floor axis 1 of 3, alone. No date, no path — an approver is enough."""
    findings = _run(
        "# Subject\n\nStatus: ratified\n"
        "Ratified: by Brett Heap, in-session\n\nBody.\n", repo)
    assert findings == [], _rules(findings)


def test_record_citation_naming_only_a_date_is_clean(repo):
    """Floor axis 2 of 3, alone. No approver named anywhere on the line."""
    findings = _run(
        "# Subject\n\nStatus: ratified\n"
        "Ratified: 2026-08-22 — the in-session ruling round\n\nBody.\n", repo)
    assert findings == [], _rules(findings)


def test_record_citation_naming_only_a_resolvable_record_is_clean(repo):
    """Floor axis 3 of 3, alone — the approver-less, date-less form the
    register's C2 ruling protects, where inventing either would be the
    failure the floor exists to prevent."""
    findings = _run(
        "# Subject\n\nStatus: ratified\n"
        f"Ratified: record: {RECORD_REL}\n\nBody.\n", repo)
    assert findings == [], _rules(findings)
    # The fixture isolates the record axis only if the OTHER two really are
    # absent; assert that rather than trusting the wording.
    line = f"Ratified: record: {RECORD_REL}"
    from doc_health.families import _CITATION_APPROVER, _CITATION_DATE
    assert not _CITATION_APPROVER.search(line), "fixture names an approver"
    assert not _CITATION_DATE.search(line), "fixture names a date"


def test_record_citation_naming_a_path_that_does_not_resolve_is_a_finding(repo):
    """The record axis is RESOLVABLE-path, not path-shaped. A pointer at a
    file the repo does not contain is the decoration the floor rejects."""
    rule = _only_rule(_run(
        "# Subject\n\nStatus: ratified\n"
        "Ratified: record: review/no-such-record.md\n\nBody.\n", repo))
    assert "names none of an approver, a date, or a resolvable record" in rule


def test_record_citation_naming_none_of_the_three_is_critical(repo):
    """The empty line the floor exists to reject."""
    rule = _only_rule(_run(
        "# Subject\n\nStatus: ratified\n"
        "Ratified: yes, it was agreed\n\nBody.\n", repo))
    assert "names none of an approver, a date, or a resolvable record" in rule
    assert "Ratified by:" not in rule, (
        "a Ratified: floor violation must not be reported as a missing "
        "Ratified by: line — the document plainly carries a citation")


# ------------------------------------------- exactly one citation, never two


def test_carrying_both_spellings_is_critical(repo):
    """OQ-4: two lines each claiming to name the ratification say nothing
    about which is current. Reported on the count, not the pair (the
    ratified scenario's own wording) — the exact string is pinned here."""
    rule = _only_rule(_run(
        "# Subject\n\nStatus: ratified\n"
        "Ratified by: real-change\n"
        "Ratified: 2026-08-22 by Brett Heap\n\nBody.\n", repo))
    assert rule == "carries 2 ratification citation lines, not one"


def test_both_spellings_is_a_finding_even_when_each_would_pass_alone(repo):
    """The both-lines finding is structural, not a fallback for two bad
    lines: here the primary resolves AND the record line clears the floor,
    and it is still a finding, reported on the count."""
    findings = _run(
        "# Subject\n\nStatus: ratified\n"
        "Ratified by: real-change\n"
        f"Ratified: 2026-08-22 by Brett Heap — record: {RECORD_REL}\n"
        "\nBody.\n", repo)
    assert len(findings) == 1
    assert findings[0].rule == "carries 2 ratification citation lines, not one", \
        _rules(findings)


def test_both_spellings_in_the_reverse_order_is_the_same_finding(repo):
    """Order-independence: the rule counts citations, it does not privilege
    whichever spelling the author happened to type first."""
    rule = _only_rule(_run(
        "# Subject\n\nStatus: ratified\n"
        "Ratified: 2026-08-22 by Brett Heap\n"
        "Ratified by: real-change\n\nBody.\n", repo))
    assert rule == "carries 2 ratification citation lines, not one"


def test_two_primary_citations_are_a_finding_even_when_one_resolves(repo):
    """Exactly-one is ONE TOTAL, not one per spelling. Two
    `Ratified by:` lines carry the identical defect as one of each — nothing
    on the page says which is current — and a reader that stopped at the
    first match would call this document clean because the FIRST line happens
    to resolve. Reported on the count: this is the SAME finding, byte for
    byte, as one of each spelling (the ratified scenario's requirement)."""
    findings = _run(
        "# Subject\n\nStatus: ratified\n"
        "Ratified by: real-change\n"
        "Ratified by: ghost-change\n\nBody.\n", repo)
    rule = _only_rule(findings)
    assert rule == "carries 2 ratification citation lines, not one"


def test_two_record_citations_are_a_finding_even_when_one_clears_the_floor(repo):
    """The same one-total rule on the record-citing spelling. The first line
    clears the floor on two axes, so a first-match reader sees a clean
    document; the second line is a competing claim about the same
    ratification — the same count-based finding as the other duplicate
    shapes."""
    findings = _run(
        "# Subject\n\nStatus: ratified\n"
        "Ratified: 2026-08-22 by Brett Heap\n"
        "Ratified: yes, it was agreed\n\nBody.\n", repo)
    rule = _only_rule(findings)
    assert rule == "carries 2 ratification citation lines, not one"


# --------------------------------------- the primary spelling, unchanged


def test_ratified_by_resolving_to_a_change_stays_clean(repo):
    """Regression: the primary path's change-id resolution is untouched."""
    findings = _run(
        "# Subject\n\nStatus: ratified\n"
        "Ratified by: real-change\n\nBody.\n", repo)
    assert findings == [], _rules(findings)


def test_ratified_by_naming_its_change_and_nothing_else_is_complete(repo):
    """THE 13-DOCUMENT REGRESSION GUARD. This line names no approver, no
    date and no path — it would fail the floor outright — and it is correct
    as written, because the named change IS its record. If the floor is ever
    widened to both spellings, this is the test that fails."""
    line = "Ratified by: real-change"
    from doc_health.families import _CITATION_APPROVER, _CITATION_DATE
    from doc_health.families import _link_targets
    assert not _CITATION_APPROVER.search(line)
    assert not _CITATION_DATE.search(line)
    assert _link_targets(line) == []
    findings = _run(f"# Subject\n\nStatus: ratified\n{line}\n\nBody.\n", repo)
    assert findings == [], (
        "the three-way floor reached Ratified by: — this converts every "
        "governed document naming its change and nothing else into a "
        "CRITICAL finding")


def test_ratified_by_dangling_is_still_critical(repo):
    """Regression: the widening must not let an unresolvable change id
    through on its way to learning the second spelling."""
    rule = _only_rule(_run(
        "# Subject\n\nStatus: ratified\n"
        "Ratified by: ghost-change\n\nBody.\n", repo))
    assert rule == (
        "Ratified by: missing or does not resolve to an OpenSpec change")


@pytest.mark.parametrize("line, axis", [
    ("Ratified by: Brett Heap on 2026-08-22, in-session", "date"),
    ("Ratified by: approved by Brett Heap, in-session", "approver"),
])
def test_the_floor_must_not_rescue_a_non_resolving_primary_citation(
        repo, line, axis):
    """THE LOOSENING GUARD, and the mirror of the 13-document one above.

    Each line here names a person and a record-shaped justification, trips
    ONE of the floor's axes, and names no change that resolves. The first is
    the shape the corpus writes eighteen times under `openspec/`, outside
    the governed roots. The requirement is one-directional: the floor is what
    makes the RECORD-CITING spelling checkable, and "the named change IS the
    citation" is what makes the primary one checkable. Letting the floor
    rescue a primary line would silently sanction `Ratified by: <a person>`
    as a substitute for naming the change — dissolving the condition of use
    the two spellings exist to keep apart, and doing it to the eighteen lines
    the corpus already carries the moment `openspec/` joins the governed
    roots.

    Without this the loosening survives every other test: `ghost-change`
    above trips NEITHER axis, so the dangling case alone cannot observe a
    floor rescue. Both axes are parametrized because a rescue could be
    written on either one.
    """
    from doc_health.families import _CITATION_APPROVER, _CITATION_DATE
    body = line.split(":", 1)[1]
    tripped = {"approver": _CITATION_APPROVER, "date": _CITATION_DATE}[axis]
    assert tripped.search(body), (
        f"fixture is broken: it must trip the floor's {axis} axis, or it "
        "cannot observe a floor rescue")
    rule = _only_rule(_run(
        f"# Subject\n\nStatus: ratified\n{line}\n\nBody.\n", repo))
    assert rule == (
        "Ratified by: missing or does not resolve to an OpenSpec change"), (
        "the three-way floor rescued a Ratified by: line that names no "
        "resolvable change — the primary spelling's whole rule is that the "
        "named change is the citation")


# ------------------------------------------------ no citation at all


def test_ratified_with_no_citation_names_both_spellings(repo):
    """A bare, uncited `Status: ratified` stays illegal — and the message
    must name both sanctioned spellings now that both are legal, rather than
    telling the author to add the one that may not exist."""
    rule = _only_rule(_run("# Subject\n\nStatus: ratified\n\nBody.\n", repo))
    assert rule == (
        "ratified header carries no citation in either sanctioned spelling")


# ---------------------------------------- the body-prose / window boundary


def test_prose_opening_with_the_word_inside_the_window_is_not_a_citation(repo):
    """D2's trap, made observable: `Ratified together with…` sits INSIDE the
    header window here. It is body prose and not a citation, so this document
    is uncited. Collapsing the reader to `_header_line(doc, "Ratified")`
    would match this line and report something else entirely."""
    rule = _only_rule(_run(
        "# Subject\n\nStatus: ratified\n"
        "Ratified together with the two decisions already carried into the\n"
        "design, which is a sentence and not a citation line.\n\nBody.\n",
        repo))
    assert rule == (
        "ratified header carries no citation in either sanctioned spelling")


def test_a_section_label_below_the_window_is_not_a_second_citation(repo):
    """The companion shape: a properly cited document whose BODY carries a
    `Ratified: <prose>` decision label. Reading the whole document instead of
    the header window would see two citations and report the both-lines
    violation on a document that carries exactly one."""
    filler = "".join(f"Filler line {i}.\n" for i in range(20))
    text = ("# Subject\n\nStatus: ratified\n"
            "Ratified by: real-change\n\n" + filler +
            "Ratified: YAML-serialized JSON-Schema contracts under contracts/\n")
    assert len(corpus.split_keepends(text)) > corpus.STATUS_SCAN_LINES, \
        "fixture is broken: the label must sit below the header window"
    findings = _run(text, repo)
    assert findings == [], (
        "a body-prose decision label was read as a ratification citation: "
        f"{_rules(findings)}")


def test_a_citation_past_the_window_is_not_found(repo):
    """The window itself is unchanged by this widening: a citation pushed
    past `STATUS_SCAN_LINES` is not read, in either spelling."""
    filler = "".join(f"Filler line {i}.\n" for i in range(20))
    text = ("# Subject\n\nStatus: ratified\n\n" + filler +
            "Ratified: 2026-08-22 by Brett Heap\n")
    rule = _only_rule(_run(text, repo))
    assert rule == (
        "ratified header carries no citation in either sanctioned spelling")


def test_the_two_prefixes_are_disjoint():
    """The structural fact the two-rule split rests on: a `Ratified by:` line
    does not match the record-citing prefix, so no line is ever read under
    both rules."""
    from doc_health.families import (_RATIFIED_BY_PREFIX,
                                     _RATIFIED_RECORD_PREFIX)
    assert not "Ratified by: some-change".startswith(_RATIFIED_RECORD_PREFIX)
    assert not "Ratified: a record".startswith(_RATIFIED_BY_PREFIX)
    assert _RATIFIED_BY_PREFIX != "Ratified" != _RATIFIED_RECORD_PREFIX
