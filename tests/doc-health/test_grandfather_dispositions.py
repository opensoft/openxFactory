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
from doc_health import CRITICAL, INFO, WARNING
from doc_health import corpus, promotion_fidelity, report
from doc_health.corpus import Doc
from doc_health.families import (_AGGREGATION_REPO,
                                 _DISPOSITIONS_REL,
                                 _GRANDFATHERED_ACTION,
                                 _GRANDFATHERED_RULE_PREFIX,
                                 _RATIFICATION_RECORD_RULE,
                                 _RATIFIED_PROVENANCE,
                                 _STALE_ACTION,
                                 _STALE_RULE_PREFIX,
                                 _CITE_EXCERPT_CHARS,
                                 _cite_excerpt,
                                 _grandfather_cites,
                                 _lifecycle_scope,
                                 _honour_grandfather_dispositions,
                                 _stale_grandfather_dispositions,
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


def _doc(path, text, repo=REPO):
    return Doc(repo, path, text, corpus.parse_status(text),
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
    it was before this change.

    THE ASSERTION IS NARROWED TO THE RECORD'S OWN ROW BY #965, AND THE SECOND
    HALF IS ADDED RATHER THAN THE FIRST RELAXED. This fixture's entry names a
    DIFFERENT archived path from the document under test, so it matches no
    finding — which is precisely the stale class `_stale_grandfather_
    dispositions` now reports, at `warning`, against the dispositions file
    itself. The subject of this test (an archived record nobody ruled on is
    still `critical`, under its own rule) is untouched; what moved is that the
    run now also says out loud that the entry beside it disposes nothing.
    """
    agg = _dispositions(tmp_path, _entry(path="openspec/changes/archive/"
                                              "2026-09-04-other/review/"
                                              "ratification-2026-09-04.md"))
    findings = _run(_doc(ARCHIVED, SUBJECT_TEXT), agg_root=agg)
    assert [(f.severity, f.rule) for f in findings if f.path == ARCHIVED] == [
        (CRITICAL, _RATIFICATION_RECORD_RULE)]
    assert [(f.severity, f.repo, f.path) for f in findings
            if f.path == _DISPOSITIONS_REL] == [
        (WARNING, _AGGREGATION_REPO, _DISPOSITIONS_REL)]


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


def test_the_runners_own_read_survives_a_malformed_entry_end_to_end(tmp_path):
    """AND THE NIGHTLY'S OWN READ OF THE SAME FILE MUST SURVIVE IT TOO.

    `runner.main` loads `health/dispositions.yaml` unconditionally on every
    aggregation run, for `report.uncited_resolutions`, and builds a
    `(family, repo, path)` key from the RAW entry. A list- or dict-valued
    `family`, `repo` or `path` in an otherwise well-formed list file makes
    that tuple unhashable, so `set.add` raised `TypeError` out of the whole
    nightly — a crash that predates #939's arm and that the other malformed
    tests in this file could not have caught, because they call the family
    directly and never reach the runner.

    Measured END TO END here, through `runner.main` over a real aggregation
    root, which is the only path that executes that read. It NARROWS NOTHING:
    a key that cannot be hashed could never have entered the set and could
    never have matched a real finding's three string fields, so the
    dispositioned set is identical either way and only the exception is gone
    (PR #945, Copilot's fifth round).
    """
    from doc_health import runner as _runner
    agg = _dispositions(
        tmp_path,
        _entry(repo=None) .replace("  repo: None\n",
                                   "  repo:\n    - a list\n")
        + _entry(path=None).replace("  path: None\n",
                                    "  path:\n    k: a mapping\n")
        + _entry())
    (agg / "openxFactory").mkdir(parents=True, exist_ok=True)
    out = tmp_path / "report.md"
    rc = _runner.main(["--repo-root", str(agg),
                       "--family", _RATIFIED_PROVENANCE,
                       "--as-of", AS_OF.isoformat(),
                       "--report-out", str(out)])
    assert rc == 0
    assert out.is_file()


def test_the_runners_own_read_survives_a_scalar_rooted_dispositions_FILE_end_to_end(
        tmp_path):
    """AND THE NIGHTLY'S OWN READ MUST SURVIVE A SCALAR-ROOTED FILE TOO —
    THE ONE SHAPE NEITHER EXISTING `runner.main` TEST SENDS THROUGH IT.

    `runner.main` loads `health/dispositions.yaml` unconditionally on every
    aggregation run, for `report.uncited_resolutions`, behind its OWN
    `isinstance(_entries, list)` guard (round 4 of PR #945's bench, commit
    `5a8bba3e`) — the same refusal `promotion_fidelity.load_dispositions`
    applies, needed here too because this read happens whatever any family
    does. A file whose ROOT is a scalar (an int, a bool, a string, a bare
    mapping) is well-formed YAML, so `yaml.safe_load` returns it unchanged
    and `for d in _entries` would raise `TypeError: 'int' object is not
    iterable` (or the mapping/string equivalent) out of the whole nightly —
    the abort this guard removed, restored the moment the branch is deleted
    (issue #964, filed at #939's archive).

    NEITHER EXISTING MALFORMED-FILE TEST REACHES THIS LINE. The runner.main
    test just above sends a LIST root carrying malformed ENTRIES through
    `runner.main` — the round-5 unhashable-key guard, a different branch and
    a different crash. And the family-level scalar-root test,
    `test_a_malformed_dispositions_FILE_is_ignored_rather_than_aborting_the_run`,
    reaches a scalar root but through `promotion_fidelity.load_dispositions`
    and the family directly, never through `runner.main` — so deleting the
    round-4 branch alone left the suite green while the abort still fires on
    every real aggregation run.

    Measured END TO END here, through `runner.main` over a real aggregation
    root, which is the only path that executes that read. It NARROWS
    NOTHING: a scalar root never yielded a disposition either way (a mapping
    iterates keys, a string iterates characters, neither of which is a
    dict), so the honoured set is identical either way and only the
    exception is gone.
    """
    from doc_health import runner as _runner
    agg = _dispositions(tmp_path, "7\n")
    (agg / "openxFactory").mkdir(parents=True, exist_ok=True)
    out = tmp_path / "report.md"
    rc = _runner.main(["--repo-root", str(agg),
                       "--family", _RATIFIED_PROVENANCE,
                       "--as-of", AS_OF.isoformat(),
                       "--report-out", str(out)])
    assert rc == 0
    assert out.is_file()


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


def test_the_downgrade_pass_still_returns_early_on_an_empty_finding_list(
        tmp_path, monkeypatch):
    """The early return of `_honour_grandfather_dispositions`, unmoved.

    ORIGINALLY `test_a_run_with_no_findings_reads_no_file`, AND #965
    DELIBERATELY OVERTURNS THE HALF OF IT THAT WAS ABOUT THE FAMILY. That
    version asserted that a CLEAN corpus never opened the dispositions file at
    all, which was true only while nothing read the entries that match
    NOTHING. An entry matching nothing is now the whole subject of the stale
    class, and a clean corpus is the extreme case of it — every honoured entry
    matches nothing — so a run with no findings reads the file and reports
    every in-scope entry, which
    `test_a_clean_corpus_makes_every_in_scope_entry_stale` pins.

    WHAT SURVIVES UNCHANGED IS THE DOWNGRADE PASS'S OWN EARLY RETURN, and it
    is now asserted where it lives rather than through the family, so the two
    passes' costs stay separable: handed an empty finding list, that pass still
    opens nothing. The probe is the same one — the shared reader monkeypatched
    to RAISE, so the no-read is observable rather than inferred — and the same
    probe over a NON-EMPTY list is asserted to raise, so the fixture is known
    to be live rather than silently bypassed (PR #945, Copilot's third round).
    """
    agg = _dispositions(tmp_path, _entry())
    ctx = _ctx(agg_root=agg)
    built = _run(_doc(ARCHIVED, SUBJECT_TEXT), agg_root=None)
    assert [f.severity for f in built] == [CRITICAL]

    def _explode(*_args, **_kwargs):
        raise AssertionError("the dispositions file was read")

    monkeypatch.setattr(promotion_fidelity, "load_dispositions", _explode)
    assert _honour_grandfather_dispositions(ctx, []) == []
    with pytest.raises(AssertionError, match="the dispositions file was read"):
        _honour_grandfather_dispositions(ctx, built)


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


# --- #965: the entries that match NOTHING -----------------------------------
#
# The converse of everything above. `_honour_grandfather_dispositions` reads
# the file and downgrades what it MATCHES; until #965 nothing read what it
# matched nothing, so an entry whose record had been REPAIRED or whose path had
# VANISHED stopped disposing anything in silence and the file kept it. The
# population was ZERO when the parent packet measured it at its § 2.1 rig and
# THREE at its § 5.13 rig, all three by repair.


CLEAN_TEXT = ("# Proposal Ratification: real-change\n\n"
              "Status: ratified\nRatified by: real-change\n")

#: A second archived record, always dirty, so that a run under test is known to
#: be LIVE — a family that reported nothing at all would satisfy several of the
#: assertions below without running.
OTHER_ARCHIVED = ("openspec/changes/archive/2026-09-04-other/review/"
                  "ratification-2026-09-04.md")
#: A path no document carries: the VANISHED half of the class.
VANISHED = ("openspec/changes/archive/2026-08-01-deleted-packet/review/"
            "ratification-2026-08-01.md")


def _stale(findings):
    """The stale rows of a family run, in report order."""
    return [f for f in findings if f.path == _DISPOSITIONS_REL]


def _ctx_repos(*docs, agg_root=None, repos=(REPO,)):
    """`_ctx` with the repository SET spelled out — the scope narrowing under
    test in `test_an_entry_naming_a_repository_out_of_scope_is_never_stale`."""
    return Context(repo_paths={r: NO_SUCH_REPO_ROOT for r in repos},
                   docs=list(docs), capabilities={},
                   change_ids={r: {"real-change"} for r in repos},
                   git=None, thresholds={}, as_of=AS_OF, agg_root=agg_root)


def test_a_repaired_record_leaves_its_entry_reported_stale(tmp_path):
    """THE LIVE SHAPE, AND THE ONE THE MEASUREMENT FOUND. The record still
    exists and is now CONFORMANT — a ratification record carrying its citation
    — so no arm of this family raises a finding against it and the entry that
    grandfathered it disposes nothing. The row lands on the dispositions FILE,
    not on the record: there is nothing wrong with the record.

    A second, dirty archived record is in the corpus so the run is known to be
    live: a family that reported nothing at all would satisfy the stale
    assertion for the wrong reason.
    """
    agg = _dispositions(tmp_path, _entry())
    findings = _run(_doc(ARCHIVED, CLEAN_TEXT),
                    _doc(OTHER_ARCHIVED, SUBJECT_TEXT), agg_root=agg)
    assert [(f.severity, f.path) for f in findings if f.path != _DISPOSITIONS_REL] == [
        (CRITICAL, OTHER_ARCHIVED)]
    stale, = _stale(findings)
    assert (stale.severity, stale.family, stale.repo, stale.path) == (
        WARNING, "ratified-provenance", _AGGREGATION_REPO, _DISPOSITIONS_REL)
    assert stale.rule.startswith(_STALE_RULE_PREFIX)
    assert f"{REPO} {ARCHIVED}" in stale.rule
    assert stale.action == _STALE_ACTION + CITE
    assert stale.resolution == "auto-fixable"


def test_a_vanished_path_leaves_its_entry_reported_stale(tmp_path):
    """THE OTHER HALF OF THE CLASS, and the one the measurement has not seen
    yet. The record is GONE — no document in the corpus carries that path — so
    the entry names a file nobody can read, let alone repair. It is reported
    exactly as the repaired case is: the two are one class, because the arm
    cannot tell them apart and does not need to. Its whole predicate is that
    the entry matched no finding this run raised."""
    agg = _dispositions(tmp_path, _entry(path=VANISHED))
    findings = _run(_doc(OTHER_ARCHIVED, SUBJECT_TEXT), agg_root=agg)
    stale, = _stale(findings)
    assert stale.severity == WARNING
    assert f"{REPO} {VANISHED}" in stale.rule


def test_an_entry_that_matched_reports_no_stale_row(tmp_path):
    """THE NEGATIVE CASE, which is the one the standing fifteen are in. An
    entry whose record still carries the defect downgrades a finding and is
    therefore NOT stale — the downgrade is the match. Asserted in the same run
    as the `info` row it produces, so the two halves of the equality are read
    off one population rather than two."""
    agg = _dispositions(tmp_path, _entry())
    findings = _run(_doc(ARCHIVED, SUBJECT_TEXT), agg_root=agg)
    assert _stale(findings) == []
    assert [(f.severity, f.path) for f in findings] == [(INFO, ARCHIVED)]


def test_a_clean_corpus_makes_every_in_scope_entry_stale(tmp_path):
    """THE EXTREME OF THE CLASS, AND THE BEHAVIOUR #965 DELIBERATELY BUYS. When
    every grandfathered record has been repaired the family reports nothing,
    and the file's entire population is then residue. This is the half of
    `test_a_run_with_no_findings_reads_no_file` that #965 overturns: a run with
    no findings now reads the file, because the entries that match nothing are
    exactly this arm's subject and a clean corpus is the case where they all
    do.

    ONE ROW PER ENTRY, at one path, ordered by the entry's target — the rows
    are distinguished by their rule, which is what a reader prunes by.
    """
    agg = _dispositions(tmp_path, "".join((
        _entry(),
        _entry(path=VANISHED),
        _entry(path=OTHER_ARCHIVED),
    )))
    findings = _run(_doc(ARCHIVED, CLEAN_TEXT), agg_root=agg)
    assert _stale(findings) == findings
    assert [f.severity for f in findings] == [WARNING] * 3
    assert {f.match_key() for f in findings} == {
        ("ratified-provenance", _AGGREGATION_REPO, _DISPOSITIONS_REL)}
    targets = [f.rule[len(_STALE_RULE_PREFIX):].split() for f in findings]
    assert [t[3] for t in targets] == [REPO] * 3
    assert [t[4] for t in targets] == sorted(
        [ARCHIVED, VANISHED, OTHER_ARCHIVED])


def test_an_entry_naming_a_repository_out_of_scope_is_never_stale(tmp_path):
    """A REPOSITORY THIS RUN DID NOT READ IS NOT EVIDENCE OF ANYTHING, and this
    is the narrowing that keeps the class honest. An aggregation checkout with
    a submodule unmaterialized reports no finding for that repository, so every
    entry naming it would fall out of the difference and be reported stale on
    the strength of a measurement nobody took.

    The SAME file is read under two scopes, so what moves is the scope and not
    the fixture: with `codexFactory` contributing no document its entry is
    passed over in silence, and with a `codexFactory` document in the scan set
    — a CLEAN one, so the entry still matches no finding — the same entry is
    reported.
    """
    agg = _dispositions(tmp_path, _entry(repo="codexFactory"))
    without = fam_ratified_provenance(
        _ctx_repos(_doc(OTHER_ARCHIVED, SUBJECT_TEXT), agg_root=agg))
    assert _stale(without) == []
    within = fam_ratified_provenance(
        _ctx_repos(_doc(OTHER_ARCHIVED, SUBJECT_TEXT),
                   _doc(ARCHIVED, CLEAN_TEXT, repo="codexFactory"),
                   agg_root=agg, repos=(REPO, "codexFactory")))
    stale, = _stale(within)
    assert stale.severity == WARNING
    assert "codexFactory" in stale.rule


def test_a_single_repo_run_reports_no_stale_entry():
    """INHERITED, NOT CHOSEN, exactly as the downgrade inherits it. The
    dispositions file lives at the AGGREGATION root and a `--single-repo`
    self-gate run has `Context.agg_root is None`, so `_grandfather_cites`
    returns `{}` and there are no entries to be stale. openxFactory #968 is the
    open sibling that would change that, and it is not changed here."""
    findings = _run(_doc(ARCHIVED, CLEAN_TEXT), agg_root=None)
    assert findings == []
    assert _stale_grandfather_dispositions(_ctx(agg_root=None), []) == []


def test_a_malformed_dispositions_file_reports_no_stale_entry(tmp_path):
    """UNCHANGED BEHAVIOUR, ASSERTED RATHER THAN ASSUMED. A scalar-root file
    and an entry whose `repo` or `path` cannot be hashed are refused one level
    up, in the shared reader and in `_grandfather_cites`, so this pass is
    handed an empty citation map and reports nothing — the same answer it gives
    for a file that carries no entry for this family at all. A new pass over a
    file two guards already refuse must not be the place a malformed hand-edit
    starts aborting the nightly again."""
    scalar = _dispositions(tmp_path / "scalar", "42\n")
    assert _stale(_run(_doc(OTHER_ARCHIVED, SUBJECT_TEXT),
                       agg_root=scalar)) == []
    unhashable = _dispositions(tmp_path / "unhashable", (
        f"- family: {_RATIFIED_PROVENANCE}\n"
        f"  repo:\n    - {REPO}\n    - codexFactory\n"
        f"  path: {VANISHED}\n"
        "  date: '2026-09-10'\n"
        f"  cite: {CITE!r}\n"
        f"- family: {_RATIFIED_PROVENANCE}\n"
        f"  repo: {REPO}\n"
        "  path:\n    glob: 'openspec/changes/archive/**'\n"
        "  date: '2026-09-10'\n"
        f"  cite: {CITE!r}\n"))
    assert _stale(_run(_doc(OTHER_ARCHIVED, SUBJECT_TEXT),
                       agg_root=unhashable)) == []
    missing = _run(_doc(OTHER_ARCHIVED, SUBJECT_TEXT), agg_root=tmp_path)
    assert _stale(missing) == []


def test_an_entry_the_downgrade_would_not_honour_is_not_stale_either(tmp_path):
    """ONE ADMISSION RULE, READ ONCE, FOR BOTH HALVES OF THE EQUALITY. An
    undated entry, an uncited one, and an entry naming another family are all
    refused by `_grandfather_cites` — so none of them downgrades a finding, and
    none of them is reported stale either. A second set of entries counted as
    residue but never honoured would make the file converge on a set no reader
    of it agrees with.

    Each is asserted through the family with a corpus that draws a finding
    elsewhere, so "no stale row" is a fact about the entry rather than about an
    empty run.
    """
    live = _doc(OTHER_ARCHIVED, SUBJECT_TEXT)
    for name, body in (("undated", _entry(path=VANISHED, date=None)),
                       ("uncited", _entry(path=VANISHED, cite=None)),
                       ("blank-cite", _entry(path=VANISHED, cite="   ")),
                       ("other-family", _entry(path=VANISHED,
                                               family="record-immutability"))):
        agg = _dispositions(tmp_path / name, body)
        assert _grandfather_cites(_ctx(agg_root=agg)) == {}, name
        assert _stale(_run(live, agg_root=agg)) == [], name


def test_an_active_path_entry_whose_finding_stands_is_not_stale(tmp_path):
    """THE D2 BOUNDARY AND THIS CLASS DO NOT OVERLAP, which is measured here
    rather than argued. An entry naming an ACTIVE packet's record is admitted
    by the shared reader and is deliberately NOT honoured by the downgrade
    (the record is one commit away from correct), but it still MATCHES a
    finding — the `critical` row that stands — so it is not residue and draws
    no stale row. The predicate is "the entry matched no finding", never "the
    entry changed no severity"."""
    agg = _dispositions(tmp_path, _entry(path=ACTIVE))
    findings = _run(_doc(ACTIVE, SUBJECT_TEXT), agg_root=agg)
    assert [(f.severity, f.path) for f in findings] == [(CRITICAL, ACTIVE)]
    assert _stale(findings) == []


def test_the_second_pass_returns_only_its_own_rows(tmp_path):
    """THE TWO PASSES COMPOSE AND THE SECOND REBUILDS NOTHING. Handed the list
    the downgrade returned, `_stale_grandfather_dispositions` returns ONLY the
    rows it built — never an echo of a finding it was given — so the family's
    tail is a concatenation and every graded row reaches the report as the
    downgrade left it. Asserted over the real list, by identity on the rows
    that pass through and by subject on the rows that are added.

    AND THE DIFFERENCE IS WELL-DEFINED AFTER THE DOWNGRADE because of what the
    downgrade preserves: canon requires a grandfathered finding to keep its
    family, repository and path, so the key set is identical on both sides of
    it — asserted by taking the difference over the UNGRADED list too and
    getting the same row.
    """
    agg = _dispositions(tmp_path, _entry() + _entry(path=VANISHED))
    docs = (_doc(ARCHIVED, SUBJECT_TEXT), _doc(OTHER_ARCHIVED, SUBJECT_TEXT))
    ctx = _ctx(*docs, agg_root=agg)
    ungraded = _run(*docs, agg_root=None)
    graded = _honour_grandfather_dispositions(ctx, ungraded)
    added = _stale_grandfather_dispositions(ctx, graded)

    assert [f.path for f in added] == [_DISPOSITIONS_REL]
    for row, built in zip(graded + added, graded):
        assert row is built
    assert added[0].severity == WARNING and VANISHED in added[0].rule
    # the same difference taken over the UNGRADED list yields the same row
    assert [f.rule for f in _stale_grandfather_dispositions(ctx, ungraded)] == [
        added[0].rule]
    # and the family itself returns the two passes, in that order
    findings = fam_ratified_provenance(ctx)
    assert [(f.severity, f.path) for f in findings] == (
        [(f.severity, f.path) for f in graded]
        + [(WARNING, _DISPOSITIONS_REL)])


def test_the_stale_row_is_a_readable_ranked_plan_row(tmp_path):
    """The row's own grammar, end to end, and the two comparisons it must stay
    out of. A `warning` is neither a regression key (only `critical`/`error`
    rows enter `keys`) nor a contested key (this family carries no `contested`
    class), so a stale entry can neither open an issue nor be adjudicated as an
    uncited resolution — which is the whole reason the class is not
    `contested`: the moment the owner PRUNES the entry the row disappears, and
    a contested row that disappears without a citation is emitted as an
    `error`."""
    messy = ('Brett Heap, first-hand, 2026-09-10, verbatim:\n'
             '"grandfather 877 via dispositions" — a backslash \\ and a '
             'quote " in one line. ' + "tail " * 80)
    agg = _dispositions(tmp_path, _entry(path=VANISHED, cite=messy))
    stale, = _stale(_run(_doc(OTHER_ARCHIVED, SUBJECT_TEXT), agg_root=agg))
    line = report.plan_line(stale, strict=True)
    assert "\n" not in line
    match = report.PLAN_RE.match(line)
    assert match, line
    assert match.group(1) == WARNING
    assert match.group(2) == _RATIFIED_PROVENANCE
    assert match.group(3) == _AGGREGATION_REPO
    assert match.group(4) == _DISPOSITIONS_REL
    text = "## Ranked plan\n\n" + line + "\n"
    assert report.unparsed_plan_rows(text) == []
    keys, contested = report.parse_previous(text)
    assert keys == set() and contested == set()


def test_a_target_spelled_across_two_lines_still_reads_back(tmp_path):
    """`escape_field` quotes a `"` and a `\\` and does not touch a NEWLINE, and
    the entry's `repo` and `path` are whatever a hand-edited YAML string holds
    — a double-quoted scalar carrying `\\n` is admitted by the shared reader as
    a string like any other. The rule collapses it, so the row stays one line
    that `report.PLAN_RE` reads back anchored, instead of two that match no
    parser (issue #474's shape at a third field)."""
    agg = _dispositions(tmp_path, (
        f"- family: {_RATIFIED_PROVENANCE}\n"
        f"  repo: {REPO}\n"
        '  path: "openspec/changes/archive/x/review/\\nratification.md"\n'
        "  date: '2026-09-10'\n"
        f"  cite: {CITE!r}\n"))
    stale, = _stale(_run(_doc(OTHER_ARCHIVED, SUBJECT_TEXT), agg_root=agg))
    assert "\n" not in stale.rule
    line = report.plan_line(stale, strict=True)
    assert report.PLAN_RE.match(line), line


# --- #981 bench: the three shapes Copilot's suppressed comments named --------


def test_the_stale_rows_operator_text_is_pinned_to_its_literal_wording(
        tmp_path):
    """THE ACTION A READER IS TOLD TO TAKE IS PINNED AS TEXT, NOT AS A SYMBOL.

    Every other assertion in this file compares an emitted action against
    `_STALE_ACTION` imported from the module that builds it, so a rewrite of
    the production wording moves both sides at once and stays green — the row
    could come to say anything at all and no test would notice. This one holds
    the SENTENCE, character for character, in the place a reader of the test
    can read it: an operator instruction is an interface, and the packet's D1
    puts that exact instruction to the owner as the thing option 1 buys
    (*"prune the entry or re-point it"*). If Brett Heap rules option 2, this
    assertion is the one that must be re-authored, deliberately and visibly,
    along with the constant it pins (`tasks.md` § 1.1).

    Copilot's suppressed comment on PR #981 (`families.py:370`), TAKEN.
    """
    agg = _dispositions(tmp_path, _entry(path=VANISHED))
    stale, = _stale(_run(_doc(OTHER_ARCHIVED, SUBJECT_TEXT), agg_root=agg))
    assert stale.action == (
        "prune the entry, or re-point it at the record that still carries "
        "the defect: the grandfather it records reaches no finding this run "
        "raises, so it disposes nothing and cannot be read back from the "
        "report. Cite: " + CITE)
    assert stale.rule == (
        "STALE grandfather disposition — the entry naming "
        f"{REPO} {VANISHED} matches no finding this family raises")
    # and the two constants are those literals, so the production text cannot
    # drift behind a symbol either
    assert _STALE_ACTION.startswith("prune the entry, or re-point it at the ")
    assert _STALE_RULE_PREFIX == "STALE grandfather disposition — "


def test_two_entries_at_one_target_report_the_one_row_the_reader_admits(
        tmp_path):
    """ONE ROW PER HONOURED TARGET — WHICH IS NOT THE SAME AS ONE ROW PER LINE
    OF THE FILE, AND THE DIFFERENCE IS PINNED HERE RATHER THAN LEFT TO BE
    DISCOVERED.

    `_grandfather_cites` is a `(repo, path) -> cite` MAP and takes the FIRST
    entry where one target carries two — `cites.setdefault(key, cite)`, the
    parent packet's landed line, BYTE-UNMOVED by this change. So two entries
    at one target downgrade one finding between them and are reported stale as
    one row between them. That is the shared admission rule's answer, not this
    pass's: making the stale half a multimap would report a residue the
    downgrade half cannot honour, and the whole ground of `design.md` D2 is
    that ONE reading of the file serves both halves.

    MEASURED, at `opensoft/xFactory` `0ecb370e`: the file carries 49 entries
    and 49 DISTINCT `(family, repo, path)` triples — the duplicate-target
    shape does not exist today, in this family or in any other. Whether a
    duplicate should be reported per LINE is a question about the shared
    reader, and it belongs to whoever changes that reader (`tasks.md` § 7.7).

    Copilot's suppressed comment on PR #981 (`families.py:621`), TAKEN AS A
    TEST AND REFUSED AS A CODE CHANGE, for the reason above.
    """
    second = ("A SECOND ruling at the same target, recorded later, which the "
              "shared reader does not reach because the first one wins.")
    agg = _dispositions(tmp_path, _entry(path=VANISHED)
                        + _entry(path=VANISHED, cite=second))
    stale = _stale(_run(_doc(OTHER_ARCHIVED, SUBJECT_TEXT), agg_root=agg))
    assert len(stale) == 1
    assert CITE in stale[0].action and second not in stale[0].action
    # the map itself is the reason, and it is the map the DOWNGRADE reads
    assert _grandfather_cites(
        _ctx(_doc(OTHER_ARCHIVED, SUBJECT_TEXT), agg_root=agg)) == {
        (REPO, VANISHED): CITE}


def test_an_entry_naming_a_clean_active_path_is_reported_stale(tmp_path):
    """THE ARCHIVED-PATH BOUNDARY IS A PROPERTY OF THE FINDING, NOT OF THE
    ENTRY, AND THIS PASS TAKES ITS COMPLEMENT OVER ENTRIES — SO AN ENTRY OVER
    A CLEAN ACTIVE PATH IS REPORTED.

    `_honour_grandfather_dispositions` applies `_ARCHIVED_PACKET_PREFIX` to the
    FINDING it is about to move (the parent's D2: an active record's header is
    a plain fix, never a ruling's subject). `_grandfather_cites` admits an
    entry at any path, and this pass asks only whether the entry named a
    finding this run raised. The two cases therefore differ, deliberately:

    * an entry over an active path whose record STILL DRAWS a finding is NOT
      stale — it matched — and `test_an_active_path_entry_whose_finding_stands_
      is_not_stale` pins that;
    * an entry over an active path whose record is CLEAN is reported stale,
      because it reaches nothing and never will.

    THE ALTERNATIVE WAS CONSIDERED AND IS NAMED IN `design.md` D2a: filter the
    complement by the same archive prefix, so an active-path entry is never
    reported. Its cost is silence — an entry that can never dispose anything is
    the STRONGEST case of an entry that disposes nothing, and suppressing it
    re-opens, one level down, exactly the hole this packet exists to close.
    MEASURED at `opensoft/xFactory` `0ecb370e`: ZERO of the 18 entries name a
    path outside `openspec/changes/archive/`, so the population of the
    difference is empty today and the two readings cost the same report.

    Copilot's suppressed comment on PR #981 (`families.py:619`), TAKEN AS A
    NAMED DECISION AND A TEST rather than as a silent filter.
    """
    agg = _dispositions(tmp_path, _entry(path=ACTIVE))
    findings = _run(_doc(ACTIVE, CLEAN_TEXT),
                    _doc(OTHER_ARCHIVED, SUBJECT_TEXT), agg_root=agg)
    # the active record itself draws nothing: it is conformant
    assert [(f.severity, f.path) for f in findings
            if f.path not in (_DISPOSITIONS_REL,)] == [
        (CRITICAL, OTHER_ARCHIVED)]
    stale, = _stale(findings)
    assert stale.severity == WARNING
    assert f"{REPO} {ACTIVE}" in stale.rule


def test_an_unmaterialized_anchor_reports_no_entry_of_its_own_as_stale(
        tmp_path):
    """THE ANCHOR IS ADMITTED ON `is_dir()` ALONE, SO AN EMPTY DIRECTORY IS A
    REPOSITORY IN `ctx.repo_paths` THAT CONTRIBUTED NOTHING — AND THAT IS THE
    SHAPE THE SCOPE NARROWING HAS TO SURVIVE.

    `corpus.discover_repos` requires `_is_materialized_repo` of every pinned
    repository EXCEPT `openxFactory`, which it admits on `is_dir()` because it
    is "the aggregation's anchor rather than one repository among many" and
    every fixture aggregation in this suite is a plain directory. An
    aggregation checkout whose `openxFactory` pin is unmaterialized therefore
    leaves an empty directory that enumerates as a repository and yields no
    document, and a scope read off `ctx.repo_paths` would call every entry
    naming it stale on a checkout nobody measured.

    MEASURED, on the standing file at `opensoft/xFactory` `0ecb370e` with the
    anchor emptied: FIFTEEN false `warning` rows before the narrowing moved to
    the document set, ZERO after, and the fully materialized aggregation
    reports the SAME three stale entries either way. Reading the scope off
    `_lifecycle_scope(ctx)` — the exact document set the five arms above read —
    is what makes "this run did not read that repository" the predicate rather
    than "this run listed a directory of that name".

    Copilot's suppressed comment on PR #981 (`families.py:618`), TAKEN.
    `corpus.discover_repos` is NOT moved: its laxer anchor admission is every
    fixture aggregation's route in, and narrowing it would be a change to what
    EVERY family measures rather than to what this one reports.
    """
    agg = _dispositions(tmp_path, _entry() + _entry(repo="codexFactory"))
    ctx = _ctx_repos(agg_root=agg, repos=(REPO, "codexFactory"))
    assert set(ctx.repo_paths) == {REPO, "codexFactory"}
    assert _lifecycle_scope(ctx) == []
    assert _grandfather_cites(ctx) == {(REPO, ARCHIVED): CITE,
                                       ("codexFactory", ARCHIVED): CITE}
    assert _stale(fam_ratified_provenance(ctx)) == []


def test_either_document_set_alone_puts_a_repository_in_scope(tmp_path):
    """THE SCOPE IS THE UNION `_lifecycle_scope` RETURNS, AND THAT IS A CHOICE
    RATHER THAN AN ACCIDENT OF WHICH ACCESSOR WAS TO HAND.

    `govern-openspec-corpus-membership` keeps the two document sets DISJOINT:
    `ctx.docs` is the governed corpus and `ctx.lifecycle_docs` is the lifecycle
    scan set (each packet's `proposal.md` and every `review/` record under it),
    and `LIFECYCLE_SCAN` "never enters `load_docs`". This family reads BOTH,
    through `_lifecycle_scope`, so its evidence about a repository is whatever
    either set contributed — and the stale pass's scope is that same union.

    NARROWING THE SCOPE TO `ctx.lifecycle_docs` ALONE WAS CONSIDERED AND IS
    REFUSED. A repository that contributed governed documents and no lifecycle
    document WAS read; an entry naming a `review/` record in it names a path
    this run looked for and did not find, which is stale BY A VANISHED TARGET —
    half the class this packet exists to report. Silencing that would hide the
    very shape `design.md` D0 says the measurement has not seen yet, on the one
    checkout where it is most likely to appear.

    BOTH HALVES ARE ASSERTED AGAINST ONE FIXTURE, so what moves between them is
    which set carries the document and nothing else.

    Copilot's suppressed comment on PR #981 (`families.py:633`), TAKEN AS A
    NAMED BOUNDARY AND A TEST, REFUSED AS A NARROWING.
    """
    agg = _dispositions(tmp_path, _entry(path=VANISHED))
    live = _doc(OTHER_ARCHIVED, SUBJECT_TEXT)

    # (a) the repository reaches the run through the LIFECYCLE SCAN SET only
    by_lifecycle = Context(
        repo_paths={REPO: NO_SUCH_REPO_ROOT}, docs=[], capabilities={},
        change_ids={REPO: {"real-change"}}, git=None, thresholds={},
        as_of=AS_OF, agg_root=agg, lifecycle_docs=[live])
    assert by_lifecycle.docs == []
    stale, = _stale(fam_ratified_provenance(by_lifecycle))
    assert f"{REPO} {VANISHED}" in stale.rule

    # (b) and through the GOVERNED CORPUS only — the same entry, the same row
    by_corpus = Context(
        repo_paths={REPO: NO_SUCH_REPO_ROOT}, docs=[live], capabilities={},
        change_ids={REPO: {"real-change"}}, git=None, thresholds={},
        as_of=AS_OF, agg_root=agg, lifecycle_docs=[])
    assert by_corpus.lifecycle_docs == []
    stale_too, = _stale(fam_ratified_provenance(by_corpus))
    assert stale_too.rule == stale.rule and stale_too.action == stale.action
