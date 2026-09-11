"""#939: an ARCHIVED ratification record the owner has GRANDFATHERED is
reported at `info` with the ruling quoted, not at CRITICAL.

Eighteen records stood CRITICAL in the report-only nightly with no repair
available to anyone: fifteen openxFactory records grandfathered on #877
(opensoft/xFactory PR #420 -> `5bfa1fe4`) and codexFactory's three (xFactory
PR #412), each carrying a dated, cited entry in the aggregation's
`health/dispositions.yaml` and each ARCHIVED, so `record-immutability` and
`govern-archived-record-edits` put its header beyond a plain fix.
`fam_ratified_provenance` never read that file — only the runner's
`uncited_resolutions` arm did, and that arm silences a DISAPPEARED contested
finding, never a standing one, while this family is `auto-fixable` and so is
never in its contested set at all.

TWO BOUNDARIES ARE UNDER TEST AS HARD AS THE DOWNGRADE ITSELF. A disposition
reaches an ARCHIVED path and nothing else — an active packet's record is one
commit away from correct, and an entry standing in for that commit would turn
"the owner ruled on something nobody can repair" into "the owner ruled on
something nobody got round to repairing". And an entry with no `cite` records
no decision, which is the rule every other reader of this file already applies.

Built like `test_ratification_record_subject.py`: `Doc`/`Context` by hand
rather than through `conftest.make_ctx`, because what is under test is exact
header content at an exact path, plus `tmp_path` for the aggregation root the
dispositions file lives at (the shape `test_promotion_fidelity.py` already
uses).
"""

from __future__ import annotations

from datetime import date

from conftest import NO_SUCH_REPO_ROOT
from doc_health import CRITICAL, INFO
from doc_health import corpus, promotion_fidelity, report
from doc_health.corpus import Doc
from doc_health.families import (_GRANDFATHERED_ACTION,
                                 _GRANDFATHERED_RULE_PREFIX,
                                 _RATIFICATION_RECORD_RULE,
                                 _RATIFIED_PROVENANCE,
                                 _CITE_EXCERPT_CHARS,
                                 _cite_excerpt,
                                 _grandfather_cites,
                                 fam_ratified_provenance)
from doc_health.runner import Context

AS_OF = date(2026, 9, 10)
REPO = "openxFactory"

#: The archived record's path, in the shape the fifteen #877 records carry.
ARCHIVED = ("openspec/changes/archive/2026-09-04-add-per-change-sweep-ledger/"
            "review/ratification-2026-09-04.md")
#: Its ACTIVE twin — the same file name under a packet that has not archived.
ACTIVE = ("openspec/changes/add-per-change-sweep-ledger/review/"
          "ratification-2026-09-04.md")

#: A `record`-status ratification record: the #877/#878 shape, which the
#: family's SUBJECT arm reports.
SUBJECT_TEXT = ("# Proposal Ratification: real-change\n\n"
                "Status: record\n"
                "Ratified: 2026-09-04 by Brett Heap\n")
#: A `ratified` record with no citation in either sanctioned spelling: the
#: shape codexFactory's three carry, which the family's CITATION arm reports.
UNCITED_TEXT = ("# Proposal Ratification: real-change\n\n"
                "Status: ratified\n\nNo citation line.\n")

CITE = ('Brett Heap, first-hand, in session, 2026-09-10, verbatim: '
        '"grandfather 877 via dispositions" (opensoft/openxFactory#877).')


def _doc(path, text):
    return Doc(REPO, path, text, corpus.parse_status(text),
               corpus.parse_kind(text))


def _dispositions(tmp_path, body: str):
    health = tmp_path / "health"
    health.mkdir(parents=True, exist_ok=True)
    (health / "dispositions.yaml").write_text(body, encoding="utf-8")
    return tmp_path


def _entry(path=ARCHIVED, *, family=_RATIFIED_PROVENANCE, repo=REPO,
           cite=CITE, extra=""):
    lines = [f"- family: {family}", f"  repo: {repo}", f"  path: {path}",
             "  date: 2026-09-10"]
    if cite is not None:
        lines.append(f"  cite: {cite!r}")
    if extra:
        lines.append(extra)
    return "\n".join(lines) + "\n"


def _run(*docs, agg_root=None, change_ids=("real-change",)):
    ctx = Context(repo_paths={REPO: NO_SUCH_REPO_ROOT}, docs=list(docs),
                  capabilities={}, change_ids={REPO: set(change_ids)},
                  git=None, thresholds={}, as_of=AS_OF, agg_root=agg_root)
    return fam_ratified_provenance(ctx)


# --- the downgrade, on both arms the eighteen records are reported by --------


def test_a_dispositioned_archived_record_is_reported_at_info_with_the_cite(
        tmp_path):
    """The #877 fifteen: the SUBJECT arm's finding, downgraded.

    The row SURVIVES — same family, same repo, same path — so the standing
    population stays countable in the report; only the band moves and the
    action becomes the ruling rather than a repair nobody can perform.
    """
    agg = _dispositions(tmp_path, _entry())
    findings = _run(_doc(ARCHIVED, SUBJECT_TEXT), agg_root=agg)
    assert [(f.severity, f.family, f.repo, f.path) for f in findings] == [
        (INFO, "ratified-provenance", REPO, ARCHIVED)]
    # The defect is still named, in full, behind the prefix: a reader learns
    # WHAT is wrong as well as that nothing is owed.
    assert findings[0].rule == (
        _GRANDFATHERED_RULE_PREFIX + _RATIFICATION_RECORD_RULE)
    assert findings[0].action == _GRANDFATHERED_ACTION + CITE
    assert CITE in findings[0].action


def test_the_citation_arm_is_downgraded_by_the_same_entry(tmp_path):
    """codexFactory's three: `Status: ratified` with no citation in either
    sanctioned spelling. The entry keys on `(family, repo, path)` and not on
    which arm raised the finding, so ONE rule covers every arm — which is why
    the downgrade is a last pass over the findings rather than a branch inside
    each of the five places this family builds one."""
    agg = _dispositions(tmp_path, _entry())
    findings = _run(_doc(ARCHIVED, UNCITED_TEXT), agg_root=agg)
    assert [f.severity for f in findings] == [INFO]
    assert findings[0].rule == (
        _GRANDFATHERED_RULE_PREFIX
        + "ratified header carries no citation in either sanctioned spelling")


def test_an_undispositioned_archived_record_stays_critical(tmp_path):
    """Immutability alone buys nothing. The downgrade rests on a RECORDED
    RULING, so an archived record nobody has ruled on is reported exactly as
    it was before this change."""
    agg = _dispositions(tmp_path, _entry(path="openspec/changes/archive/"
                                              "2026-09-04-other/review/"
                                              "ratification-2026-09-04.md"))
    findings = _run(_doc(ARCHIVED, SUBJECT_TEXT), agg_root=agg)
    assert [(f.severity, f.rule) for f in findings] == [
        (CRITICAL, _RATIFICATION_RECORD_RULE)]


# --- the two boundaries ------------------------------------------------------


def test_an_active_packet_record_is_never_grandfathered(tmp_path):
    """THE BOUNDARY IS THE ARCHIVE PREFIX. The same ruling, the same record
    text, two paths: the archived one is downgraded and the ACTIVE one stands
    at CRITICAL, because an active packet's header is a plain fix and a
    disposition must not become a way of deferring one.

    Both in ONE run, so the assertion is about the paths rather than about two
    differently-configured runs.
    """
    agg = _dispositions(tmp_path, _entry() + _entry(path=ACTIVE))
    findings = _run(_doc(ARCHIVED, SUBJECT_TEXT), _doc(ACTIVE, SUBJECT_TEXT),
                    agg_root=agg)
    assert {f.path: f.severity for f in findings} == {
        ARCHIVED: INFO, ACTIVE: CRITICAL}
    active = next(f for f in findings if f.path == ACTIVE)
    assert active.rule == _RATIFICATION_RECORD_RULE
    assert _GRANDFATHERED_RULE_PREFIX not in active.rule


def test_an_entry_without_a_cite_is_ignored(tmp_path):
    """An entry that records no decision suppresses nothing — the rule every
    other reader of this file already applies, inherited here rather than
    restated, because the admission test is the shared reader's."""
    agg = _dispositions(tmp_path, _entry(cite=None))
    assert [f.severity for f in _run(_doc(ARCHIVED, SUBJECT_TEXT),
                                     agg_root=agg)] == [CRITICAL]


def test_an_empty_cite_is_ignored(tmp_path):
    """`cite: ''` is present and records nothing, which is the same thing."""
    agg = _dispositions(tmp_path, _entry(cite=""))
    assert [f.severity for f in _run(_doc(ARCHIVED, SUBJECT_TEXT),
                                     agg_root=agg)] == [CRITICAL]


def test_an_entry_naming_another_family_is_ignored(tmp_path):
    """One family's entry has never disposed another's findings."""
    agg = _dispositions(tmp_path, _entry(family="record-immutability"))
    assert [f.severity for f in _run(_doc(ARCHIVED, SUBJECT_TEXT),
                                     agg_root=agg)] == [CRITICAL]


def test_an_entry_naming_another_repository_is_ignored(tmp_path):
    agg = _dispositions(tmp_path, _entry(repo="codexFactory"))
    assert [f.severity for f in _run(_doc(ARCHIVED, SUBJECT_TEXT),
                                     agg_root=agg)] == [CRITICAL]


def test_a_requirement_narrowing_does_not_stop_the_downgrade(tmp_path):
    """The optional `requirement:` key selects one requirement inside a DELTA
    file. A ratification record has no requirement grain for it to select, so
    an entry that carries one is admitted on its `(repo, path)` like any other
    rather than silently disposing nothing."""
    agg = _dispositions(tmp_path, _entry(extra="  requirement: Anything"))
    assert [f.severity for f in _run(_doc(ARCHIVED, SUBJECT_TEXT),
                                     agg_root=agg)] == [INFO]


# --- the scopes where the mechanism is not available -------------------------


def test_a_single_repo_run_has_no_aggregation_root_and_nothing_moves():
    """`--single-repo` — this repository's own gate run — has
    `Context.agg_root is None`, so no disposition applies and every finding
    stands at CRITICAL. Inherited, not chosen: the file lives at the
    AGGREGATION root and `runner.main` guards its own read the same way."""
    findings = _run(_doc(ARCHIVED, SUBJECT_TEXT), agg_root=None)
    assert [(f.severity, f.rule) for f in findings] == [
        (CRITICAL, _RATIFICATION_RECORD_RULE)]


def test_a_missing_dispositions_file_changes_nothing(tmp_path):
    """An aggregation root that carries no `health/dispositions.yaml` at all."""
    findings = _run(_doc(ARCHIVED, SUBJECT_TEXT), agg_root=tmp_path)
    assert [f.severity for f in findings] == [CRITICAL]


def test_a_run_with_no_findings_reads_no_file(tmp_path):
    """The early return: a clean corpus never opens the dispositions file."""
    agg = _dispositions(tmp_path, _entry())
    clean = _doc(ARCHIVED, "# Proposal Ratification: real-change\n\n"
                           "Status: ratified\nRatified by: real-change\n")
    assert _run(clean, agg_root=agg) == []


# --- nothing else this family reports moves ----------------------------------


def test_every_other_finding_is_returned_as_the_arms_built_it(tmp_path):
    """A mixed population in one run: the dispositioned archived record moves
    and EVERY other finding is the SAME OBJECT the arms above built, not a
    rebuilt copy that happens to compare equal."""
    agg = _dispositions(tmp_path, _entry())
    other_archived = ("openspec/changes/archive/2026-09-04-other/review/"
                      "ratification-2026-09-04.md")
    docs = (_doc(ARCHIVED, SUBJECT_TEXT),
            _doc(other_archived, SUBJECT_TEXT),
            _doc(ACTIVE, SUBJECT_TEXT),
            _doc("docs/subject.md",
                 "# Subject\n\nStatus: ratified\n\nNo citation.\n"))
    plain = {f.path: f for f in _run(*docs, agg_root=None)}
    graded = {f.path: f for f in _run(*docs, agg_root=agg)}
    assert set(plain) == set(graded) == {
        ARCHIVED, other_archived, ACTIVE, "docs/subject.md"}
    assert graded[ARCHIVED].severity == INFO
    for path in (other_archived, ACTIVE, "docs/subject.md"):
        assert graded[path] == plain[path], path
    # The untouched findings are passed through by identity, so a future edit
    # that starts rebuilding them shows up here rather than in a nightly diff.
    again = _run(*docs, agg_root=agg)
    assert all(f.severity == CRITICAL for f in again if f.path != ARCHIVED)


# --- the admission rule is the shared reader's -------------------------------


def test_the_admission_rule_is_delegated_to_the_shared_reader(tmp_path):
    """`_grandfather_cites` decides NOTHING about which entries are live: its
    key set is exactly `promotion_fidelity.load_dispositions`' over the same
    file, which is the one reader promotion fidelity, duplicate packet and
    modified-block currency already share. A second admission rule written
    here is how two readers of one file come to disagree."""
    agg = _dispositions(tmp_path, "".join((
        _entry(),
        _entry(path=ACTIVE),
        _entry(path="openspec/changes/archive/x/review/r.md", cite=None),
        _entry(family="record-immutability",
               path="openspec/changes/archive/y/review/r.md"),
        _entry(repo="codexFactory",
               path="openspec/changes/archive/z/review/r.md"),
    )))
    ctx = Context(repo_paths={REPO: NO_SUCH_REPO_ROOT}, docs=[],
                  capabilities={}, change_ids={}, git=None, thresholds={},
                  as_of=AS_OF, agg_root=agg)
    shared = {(repo, path) for repo, path, _requirement
              in promotion_fidelity.load_dispositions(
                  ctx, _RATIFIED_PROVENANCE)}
    assert set(_grandfather_cites(ctx)) == shared
    assert shared == {(REPO, ARCHIVED), (REPO, ACTIVE),
                      ("codexFactory", "openspec/changes/archive/z/review/r.md")}


# --- the excerpt, and the one-line grammar it has to survive -----------------


def test_a_literal_block_cite_is_collapsed_to_one_line():
    """`report.PLAN_RE` is anchored and read back one line at a time, so a
    newline inside a field splits the row into two that match no parser — a
    finding written into the report and read by NOTHING (issue #474's shape at
    a different field). Every entry standing today is a FOLDED scalar and
    already folds to one line; one written as a LITERAL block does not."""
    assert _cite_excerpt("first line\nsecond line\n") == "first line second line"
    assert "\n" not in _cite_excerpt("a\nb\tc\r\nd")


def test_a_long_cite_is_bounded_and_says_it_was_cut():
    long_cite = " ".join(f"word{i}" for i in range(200))
    excerpt = _cite_excerpt(long_cite)
    assert len(excerpt) <= _CITE_EXCERPT_CHARS + 2      # the " …" it appends
    assert excerpt.endswith(" …")
    assert long_cite.startswith(excerpt[:-2])
    # a short one is quoted whole, with no ellipsis to suggest otherwise
    assert _cite_excerpt("short cite") == "short cite"


def test_the_downgraded_row_is_a_readable_ranked_plan_row(tmp_path):
    """The row's own grammar, end to end: a real entry whose cite carries the
    quotes, dashes and newlines the standing eighteen carry, rendered by
    `report.plan_line` in STRICT mode and read back by the parser the nightly
    comparison uses."""
    messy = ('Brett Heap, first-hand, 2026-09-10, verbatim:\n'
             '"grandfather 877 via dispositions" — a backslash \\ and a '
             'quote " in one line. ' + "tail " * 80)
    agg = _dispositions(tmp_path, _entry(cite=messy))
    finding, = _run(_doc(ARCHIVED, SUBJECT_TEXT), agg_root=agg)
    line = report.plan_line(finding, strict=True)
    assert "\n" not in line
    match = report.PLAN_RE.match(line)
    assert match, line
    assert match.group(1) == INFO
    assert match.group(2) == _RATIFIED_PROVENANCE
    assert match.group(4) == ARCHIVED
    text = "## Ranked plan\n\n" + line + "\n"
    assert report.unparsed_plan_rows(text) == []
    # an `info` row is not a regression key and not a contested key, so the
    # downgrade takes these eighteen out of BOTH comparisons rather than
    # manufacturing an uncited resolution on the next nightly
    keys, contested = report.parse_previous(text)
    assert keys == set() and contested == set()
