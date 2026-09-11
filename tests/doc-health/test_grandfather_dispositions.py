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

AND THE ENTRY THAT IS READ IS THIS FAMILY'S, DATED. A finding carries `(repo,
path)` and no third coordinate, so the citation lookup re-applies the family
test itself or a NEIGHBOURING family's entry at the same path supplies the
text — a shape the standing file HAS, `location-conformance` and
`document-catalog` disposing one `ideation/staging/` path between them. The
`date` the added scenario asks for is checked in the same place, the shared
reader never having tested one: a narrowing of what a recorded entry may
reach, and never a widening of what counts as recorded.

Built like `test_ratification_record_subject.py`: `Doc`/`Context` by hand
rather than through `conftest.make_ctx`, because what is under test is exact
header content at an exact path, plus `tmp_path` for the aggregation root the
dispositions file lives at (the shape `test_promotion_fidelity.py` already
uses).
"""

from __future__ import annotations

from datetime import date

import pytest

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
                                 _honour_grandfather_dispositions,
                                 fam_ratified_provenance)
from doc_health.runner import Context          # built once, in `_ctx` below

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

#: A citation belonging to ANOTHER family at the SAME path. The standing file
#: already carries such a pair — `location-conformance` and `document-catalog`
#: both dispose one `ideation/staging/` path — so this is a shape the file HAS
#: rather than one it might one day acquire.
FOREIGN_CITE = ('A record-immutability ruling about the same file, on a '
                'different defect, which says nothing whatever about this '
                "family's finding.")


def _doc(path, text):
    return Doc(REPO, path, text, corpus.parse_status(text),
               corpus.parse_kind(text))


def _dispositions(tmp_path, body: str):
    health = tmp_path / "health"
    health.mkdir(parents=True, exist_ok=True)
    (health / "dispositions.yaml").write_text(body, encoding="utf-8")
    return tmp_path


def _entry(path=ARCHIVED, *, family=_RATIFIED_PROVENANCE, repo=REPO,
           cite=CITE, date="2026-09-10", extra=""):
    lines = [f"- family: {family}", f"  repo: {repo}", f"  path: {path}"]
    if date is not None:
        lines.append(f"  date: {date}")
    if cite is not None:
        lines.append(f"  cite: {cite!r}")
    if extra:
        lines.append(extra)
    return "\n".join(lines) + "\n"


def _ctx(*docs, agg_root=None, change_ids=("real-change",)):
    return Context(repo_paths={REPO: NO_SUCH_REPO_ROOT}, docs=list(docs),
                   capabilities={}, change_ids={REPO: set(change_ids)},
                   git=None, thresholds={}, as_of=AS_OF, agg_root=agg_root)


def _run(*docs, agg_root=None, change_ids=("real-change",)):
    return fam_ratified_provenance(
        _ctx(*docs, agg_root=agg_root, change_ids=change_ids))


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
    """`cite: ''` is present and records nothing, which is the same thing.

    AND SO IS A CITE THAT IS PRESENT, TRUTHY AND STILL SAYS NOTHING. `cite:
    '   '` passes a bare truthiness test and passes the shared reader, and the
    row it would produce reads `Cite: ` with no ruling after it — an `info`
    row asserting that an owner ruled while carrying no word of the ruling,
    which is the defect this arm exists to close rather than a lesser form of
    it. A non-string `cite` is refused for the same reason rather than coerced:
    `str(5)` is not a citation. Each is a NARROWING — strictly fewer entries
    honoured than the shared reader admits, never one more — which is asserted
    on the reader's own admitted set for the whitespace case.
    """
    agg = _dispositions(tmp_path, _entry(cite=""))
    assert [f.severity for f in _run(_doc(ARCHIVED, SUBJECT_TEXT),
                                     agg_root=agg)] == [CRITICAL]
    blank = _dispositions(tmp_path / "blank", _entry(cite="   "))
    ctx = _ctx(agg_root=blank)
    assert {(repo, path) for repo, path, _requirement
            in promotion_fidelity.load_dispositions(
                ctx, _RATIFIED_PROVENANCE)} == {(REPO, ARCHIVED)}
    assert _grandfather_cites(ctx) == {}
    assert [f.severity for f in _run(_doc(ARCHIVED, SUBJECT_TEXT),
                                     agg_root=blank)] == [CRITICAL]
    numeric = _dispositions(tmp_path / "numeric", _entry(cite=5))
    assert _grandfather_cites(_ctx(agg_root=numeric)) == {}
    assert [f.severity for f in _run(_doc(ARCHIVED, SUBJECT_TEXT),
                                     agg_root=numeric)] == [CRITICAL]


def test_an_entry_naming_another_family_is_ignored(tmp_path):
    """One family's entry has never disposed another's findings."""
    agg = _dispositions(tmp_path, _entry(family="record-immutability"))
    assert [f.severity for f in _run(_doc(ARCHIVED, SUBJECT_TEXT),
                                     agg_root=agg)] == [CRITICAL]


def test_an_entry_naming_another_repository_is_ignored(tmp_path):
    agg = _dispositions(tmp_path, _entry(repo="codexFactory"))
    assert [f.severity for f in _run(_doc(ARCHIVED, SUBJECT_TEXT),
                                     agg_root=agg)] == [CRITICAL]


def test_a_cross_family_entry_at_the_same_path_does_not_supply_the_cite(
        tmp_path):
    """THE QUOTED RULING IS THIS FAMILY'S, NOT WHICHEVER ENTRY SHARES THE PATH.

    A finding is keyed `(repo, path)` — it has no third coordinate to match an
    entry's `family` on — so the citation lookup has to re-apply the family
    test itself or a NEIGHBOURING family's entry at the same path supplies the
    text. The row would then be downgraded correctly and quote a ruling that
    was never about this defect.

    The foreign entry is written FIRST on purpose: first-match-wins is what a
    `(repo, path)`-only lookup does, so this fixture is the regression and not
    a decoration. The file this reads in production already carries a
    same-path, two-family pair.
    """
    agg = _dispositions(tmp_path, _entry(family="record-immutability",
                                         cite=FOREIGN_CITE) + _entry())
    assert _grandfather_cites(_ctx(agg_root=agg)) == {(REPO, ARCHIVED): CITE}
    findings = _run(_doc(ARCHIVED, SUBJECT_TEXT), agg_root=agg)
    assert [f.severity for f in findings] == [INFO]
    assert findings[0].action == _GRANDFATHERED_ACTION + CITE
    assert FOREIGN_CITE not in findings[0].action


def test_an_undated_entry_is_ignored(tmp_path):
    """THE SCENARIO ASKS FOR A DATE AND THIS ARM IS WHERE THAT IS CHECKED.

    *"an entry ... carrying this family, that repository, that path, A DATE,
    and a non-empty `cite`"*. The shared reader tests family, repo, path and
    `cite` and has never tested a date, so an undated entry is RECORDED as far
    as it is concerned — which is asserted here rather than assumed, so that
    the narrowing is visible as this arm's own act. It is a narrowing and only
    ever a narrowing: no entry is honoured here that the shared reader would
    refuse.
    """
    agg = _dispositions(tmp_path, _entry(date=None))
    ctx = _ctx(agg_root=agg)
    assert {(repo, path) for repo, path, _requirement
            in promotion_fidelity.load_dispositions(
                ctx, _RATIFIED_PROVENANCE)} == {(REPO, ARCHIVED)}
    assert _grandfather_cites(ctx) == {}
    assert [f.severity for f in _run(_doc(ARCHIVED, SUBJECT_TEXT),
                                     agg_root=agg)] == [CRITICAL]
    # `date:` written with no value is present and records nothing, which is
    # the same thing — the treatment `cite` already gets two tests above.
    empty = _dispositions(tmp_path, _entry(date="''"))
    assert [f.severity for f in _run(_doc(ARCHIVED, SUBJECT_TEXT),
                                     agg_root=empty)] == [CRITICAL]


def test_a_malformed_entry_is_ignored_rather_than_aborting_the_run(tmp_path):
    """A LIST- OR DICT-VALUED `repo` MUST NOT TAKE THE NIGHTLY DOWN WITH IT.

    The shared reader refuses an entry whose `repo` or `path` is not a string
    (`load_dispositions` tests both with `isinstance`), so such an entry is
    never in `admitted` and this arm honours nothing either way. But the
    citation pass builds its lookup key from the RAW entry, and a list or a
    dict there makes `(repo, path)` UNHASHABLE: `key in admitted` raised
    `TypeError` out of `fam_ratified_provenance`, out of the runner and out of
    the whole nightly, over one malformed hand-edit of a file the estate's one
    reader silently ignores. The guard is that same reader's refusal taken
    early rather than a new predicate, which is asserted here both ways: the
    malformed entries are absent from the shared reader's admitted set, AND
    the valid entry beside them is still honoured exactly as it is alone.

    Both malformed entries carry this family AND a date, because a pass that
    gave up earlier would never have reached the key at all; and they are
    written FIRST, because the crash is order-dependent — it happens the
    moment the malformed key is tested, so an entry after the valid one would
    still have crashed but would not have proved the ordering irrelevant.
    """
    malformed = (
        f"- family: {_RATIFIED_PROVENANCE}\n"
        f"  repo:\n    - {REPO}\n    - codexFactory\n"
        f"  path: {ARCHIVED}\n"
        "  date: '2026-09-10'\n"
        f"  cite: {FOREIGN_CITE!r}\n"
        f"- family: {_RATIFIED_PROVENANCE}\n"
        f"  repo: {REPO}\n"
        "  path:\n    glob: 'openspec/changes/archive/**'\n"
        "  date: '2026-09-10'\n"
        f"  cite: {FOREIGN_CITE!r}\n")
    agg = _dispositions(tmp_path, malformed + _entry())
    ctx = _ctx(agg_root=agg)
    # The shared reader already drops both, so the admitted set is the valid
    # entry alone and this guard changes WHICH ENTRIES ARE HONOURED not at all.
    assert {(repo, path) for repo, path, _requirement
            in promotion_fidelity.load_dispositions(
                ctx, _RATIFIED_PROVENANCE)} == {(REPO, ARCHIVED)}
    assert _grandfather_cites(ctx) == {(REPO, ARCHIVED): CITE}
    findings = _run(_doc(ARCHIVED, SUBJECT_TEXT), agg_root=agg)
    assert [f.severity for f in findings] == [INFO]
    assert findings[0].action == _GRANDFATHERED_ACTION + CITE
    assert FOREIGN_CITE not in findings[0].action
    # And a malformed entry ALONE — no valid entry to make `admitted`
    # non-empty — is the short-circuit path, which must also not raise.
    alone = _dispositions(tmp_path / "alone", malformed)
    assert _grandfather_cites(_ctx(agg_root=alone)) == {}
    assert [f.severity for f in _run(_doc(ARCHIVED, SUBJECT_TEXT),
                                     agg_root=alone)] == [CRITICAL]


def test_a_malformed_dispositions_FILE_is_ignored_rather_than_aborting_the_run(
        tmp_path):
    """A SCALAR-ROOT FILE MUST NOT TAKE THE NIGHTLY DOWN EITHER, AND THE
    ABORT IT CAUSES IS OLDER THAN THIS PACKET.

    `yaml.safe_load` returns whatever the document holds. A file reading `42`
    is well-formed YAML, so `load_dispositions` reached `for entry in entries`
    and raised `TypeError` out of the estate's ONE reader of this file — out of
    promotion fidelity and duplicate packet since that reader was written, and
    out of this arm from #939. Measured both ways on an aggregation carrying a
    `42`-rooted file: `doc-health.py --repo-root <agg>` exits 1 on
    `origin/main` at `runner.py`'s own unconditional read of the same file, and
    exited 1 on this branch one frame earlier at `families.py`. So the guard is
    in BOTH readers or it buys nothing: fixing the shared one alone would have
    moved the abort back to the runner's line rather than removed it.

    IT NARROWS NOTHING. Every non-list root the guard now refuses already
    yielded an EMPTY disposition set by iteration — a mapping root iterates
    keys and a string root iterates characters, neither of which is a mapping —
    so the honoured set is identical and only the exception is gone. That is
    asserted here shape by shape rather than argued.
    """
    agg = _dispositions(tmp_path, "42\n")
    ctx = _ctx(agg_root=agg)
    assert promotion_fidelity.load_dispositions(
        ctx, _RATIFIED_PROVENANCE) == set()
    assert _grandfather_cites(ctx) == {}
    assert [f.severity for f in _run(_doc(ARCHIVED, SUBJECT_TEXT),
                                     agg_root=agg)] == [CRITICAL]
    # The two families that have read this file since the reader was written
    # are un-aborted by the same guard, which is why it belongs there and not
    # at this arm's call site.
    for family in ("promotion-fidelity", "duplicate-packet"):
        assert promotion_fidelity.load_dispositions(ctx, family) == set()
    # The other non-list roots never yielded a disposition either, so the
    # guard changes the ANSWER for none of them.
    for name, body in (("mapping", "family: ratified-provenance\n"),
                       ("string", "'a note somebody left here'\n"),
                       ("true", "true\n"),
                       ("empty", "\n")):
        other = _ctx(agg_root=_dispositions(tmp_path / name, body))
        assert promotion_fidelity.load_dispositions(
            other, _RATIFIED_PROVENANCE) == set()
        assert _grandfather_cites(other) == {}
        assert [f.severity for f in _run(_doc(ARCHIVED, SUBJECT_TEXT),
                                         agg_root=other.agg_root)] == [CRITICAL]
    # And a LIST root still reads exactly as it did.
    good = _dispositions(tmp_path / "good", _entry())
    assert [f.severity for f in _run(_doc(ARCHIVED, SUBJECT_TEXT),
                                     agg_root=good)] == [INFO]


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


def test_a_run_with_no_findings_reads_no_file(tmp_path, monkeypatch):
    """The early return: a clean corpus never opens the dispositions file.

    THE NO-READ IS MADE OBSERVABLE RATHER THAN INFERRED. A valid file plus an
    empty result proves only the result: an implementation that opened the
    file and then returned `[]` would pass that assertion unchanged. So the
    shared reader is monkeypatched to RAISE, and the clean run must still
    return `[]` — which it can only do by never reaching the read. The same
    probe over a DIRTY corpus is asserted to raise, so the fixture is known to
    be live rather than silently bypassed (PR #945, Copilot's third round).
    """
    agg = _dispositions(tmp_path, _entry())
    clean = _doc(ARCHIVED, "# Proposal Ratification: real-change\n\n"
                           "Status: ratified\nRatified by: real-change\n")
    assert _run(clean, agg_root=agg) == []

    def _explode(*_args, **_kwargs):
        raise AssertionError("the dispositions file was read")

    monkeypatch.setattr(promotion_fidelity, "load_dispositions", _explode)
    assert _run(clean, agg_root=agg) == []
    with pytest.raises(AssertionError, match="the dispositions file was read"):
        _run(_doc(ARCHIVED, SUBJECT_TEXT), agg_root=agg)


# --- nothing else this family reports moves ----------------------------------


def test_every_other_finding_is_returned_as_the_arms_built_it(tmp_path):
    """A mixed population, ONE invocation of the arms: the dispositioned
    archived record moves and every other finding is the SAME OBJECT the arms
    above built — asserted with `is`, never with `==`.

    THE LAST PASS IS HANDED THE ARMS' OWN LIST, AND THAT IS THE WHOLE POINT.
    Findings taken from two separate runs can only be compared by VALUE, and a
    pass that rebuilt every finding it was given would satisfy such a
    comparison exactly as well as one that let them through — so the documented
    pass-through-BY-IDENTITY invariant would go uncovered. Here the arms run
    once, under `agg_root=None` (the scope in which the pass returns its
    argument untouched, pinned by its own test above), and
    `_honour_grandfather_dispositions` is then called on that very list under a
    context that HAS an aggregation root.
    """
    agg = _dispositions(tmp_path, _entry())
    other_archived = ("openspec/changes/archive/2026-09-04-other/review/"
                      "ratification-2026-09-04.md")
    docs = (_doc(ARCHIVED, SUBJECT_TEXT),
            _doc(other_archived, SUBJECT_TEXT),
            _doc(ACTIVE, SUBJECT_TEXT),
            _doc("docs/subject.md",
                 "# Subject\n\nStatus: ratified\n\nNo citation.\n"))
    built = _run(*docs, agg_root=None)
    graded = _honour_grandfather_dispositions(_ctx(*docs, agg_root=agg), built)

    assert [f.path for f in graded] == [f.path for f in built]
    assert {f.path for f in built} == {
        ARCHIVED, other_archived, ACTIVE, "docs/subject.md"}
    built_by_path = {f.path: f for f in built}
    for finding in graded:
        if finding.path == ARCHIVED:
            assert finding.severity == INFO
            assert finding is not built_by_path[ARCHIVED]   # the one rebuilt
            continue
        # IDENTITY: a future edit that starts rebuilding untouched findings
        # fails here rather than showing up as a nightly diff.
        assert finding is built_by_path[finding.path], finding.path
        assert finding.severity == CRITICAL
    # and the same population through the family's own entry point
    assert {f.path: f.severity for f in _run(*docs, agg_root=agg)} == {
        ARCHIVED: INFO, other_archived: CRITICAL, ACTIVE: CRITICAL,
        "docs/subject.md": CRITICAL}


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
    ctx = _ctx(agg_root=agg)
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
