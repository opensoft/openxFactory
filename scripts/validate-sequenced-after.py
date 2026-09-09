#!/usr/bin/env python3
"""House validator for the `sequenced_after:` realization-axis front-matter field
(release-realization / add-sequenced-after-substrate).

`openspec validate` is the EXTERNAL OpenSpec CLI and cannot be extended in-tree,
so — exactly as `scripts/validate-scope-globs.py` and the other
`scripts/validate-*.py` contract validators do — this script is the house
realization of the "Parent-declaration validation" requirement, and the pytest
gate (`tests/sequenced_after/test_validate.py::test_corpus_sequenced_after_all_validate`)
runs it over every active change on every pull request, so a malformed, dangling,
ambiguous or cyclic declaration anywhere in the corpus reds the required
`pytest-suite` check.

It imposes NO DEPTH LIMIT and NO FAN-OUT LIMIT: a two-parent declaration and a
chain deeper than any consuming gate would walk both VALIDATE. Depth, fan-out and
composition are the AUTHORIZATION POLICY of the gate that acts on a chain, and a
number baked into the neutral field would bind repositories that never adopt the
consuming axis while drifting from the one gate that enforces it. A CYCLE is
refused, because no consumer's policy can resolve a chain that revisits an id to
a root.

Usage:
    validate-sequenced-after.py [REPO_ROOT]

    REPO_ROOT defaults to the current directory. Scans REPO_ROOT/openspec/changes/
    (active changes only) and validates every proposal that DECLARES
    `sequenced_after`; resolution consults the ACTIVE and ARCHIVED corpora both,
    because a chain's root is its oldest change and therefore the first to
    archive. Exit 0 when all pass; exit 1 (naming the offending change, entry and
    rule) otherwise.

    THE PLAIN RUN ALSO GATES ON ARCHIVE-DATE AGREEMENT: no archived change's
    ledger row may record a `moved_on` EARLIER than the date on its
    `archive/<YYYY-MM-DD>-<id>` directory. A row cannot have last moved before
    the archive that made it archived, and that is the shape a CLI clock
    running AHEAD of UTC produces (issue #790). Measured clean across all 143
    archived rows before it was made a gate; exit 1 with the change named
    otherwise.

    EQUALITY IS NOT REQUIRED, because `release-realization` defines `moved_on`
    as the date the ROW last moved: an archived row moved later by another
    change carries a later date, and 124 of this corpus's 143 do, none of them
    a defect. `--strict-archive-dates` asks for the stronger reading in which
    an archived row's `moved_on` IS its archive date. A missing or unreadable
    ledger is not this arm's finding — `--ledger-diff` owns that class — so the
    arm says it did not run and the verdict is unchanged.

    AND IT GATES ON THE ARCHIVE DATE AGAINST HISTORY (issue #812), which is a
    DIFFERENT FACT and a second arm — it prints and prefixes its findings
    `archive-date-vs-commit`, the one token this help, these docs and the
    output all use, so a log grep finds every line of it. Every directory under
    `openspec/changes/archive/` matching `ARCHIVE_DIR` is measured against the
    UTC committer date of the OLDEST commit that added it — one
    `git log --diff-filter=A --reverse --no-renames --name-only` walk over the
    archive root, so a batch archive act (many directories, one commit)
    attributes correctly and the cost is 83ms rather than the 9.3s of 144
    per-directory calls. A disagreement is reported BY NAME unless
    `tests/sequenced_after/archive-date-dispositions.yaml` disposes of it, and a
    disposition that names a directory which does not disagree, no longer
    exists, or cites a commit history does not carry is reported too — a stale
    disposition silences a finding on a fact nobody can check. The RECORD
    carries the severity dial (`enforcement: warning|error`), so a repository
    can adopt the arm and measure before it gates; `--strict-archive-dates`
    asks for `error` regardless. A missing or unreadable record is CANNOT RUN
    (exit 2) — the arm's whole basis for calling a disagreement dispositioned
    is that file. A checkout that cannot answer the question at all — not a git
    work-tree root, or SHALLOW, where every directory older than the graft
    boundary would be attributed to the boundary commit — says it did not run
    and leaves the verdict unchanged — while git FAILING in a checkout that
    passed those probes (a partial clone with objects unavailable, a corrupt
    object store) is CANNOT RUN, because green-with-the-gate-off is the one
    answer a gate must never give.

    THE ARM MEASURES A NAME AGAINST A COMMIT, AND CANNOT ITSELF JUDGE WHY THEY
    DIFFER. FOUR causes produce the same shape: the clock defect; a
    wrapper-made archive whose commit crossed UTC midnight; a change id that
    arrived carrying its own `YYYY-MM-DD-` prefix (which the pinned CLI
    preserves DELIBERATELY); and a directory RENAMED INSIDE `archive/` after
    its archive act, which `--no-renames` attributes to the RENAME commit and
    which can therefore disagree by any distance, not merely a day — the shape
    of this corpus's two oldest directories, whose dispositions cite the rename
    commit AND the archive act it moved. (Rename detection is not the repair:
    under `-M` the destination never appears as an add and the directory would
    be silently unmeasured.) That judgement is what a disposition's `fact`
    records, and why the record is a record rather than an allow-list.

    BOTH ARMS RUN ON ONE PASS. They read different things and want different
    repairs, so the first one's failure does not return before the second has
    reported.

    --archive-gate CHANGE_DIR --ratified-ref REF
        Parent-declaration retention (freeze) gate. CHANGE_DIR may name either
        the change's ACTIVE or its ARCHIVED directory — the ratified-side
        proposal is always located BY CHANGE ID against REF's own tree (active
        path first, then any archived `<date>-<id>` directory), never by
        reusing CHANGE_DIR's current path, so the gate still runs after the
        change has moved from its active location to
        `openspec/changes/archive/<date>-<id>/` between ratification and
        archive. CHANGE_DIR may be absolute or relative (including `.` from
        inside the change directory itself) and MUST live under
        `openspec/changes/` of its repository, because the ratified-side lookup
        is anchored there.

        A FAILURE TO READ EITHER SIDE is a named finding with exit 2 rather
        than a traceback — EVERY `SequencedAfterError` out of the gate is
        reported that way, not an enumerated few: CHANGE_DIR is not inside a
        git work tree; REF does not name a commit (an unresolvable ref is named
        as such, NOT reported as a change absent at a resolvable one); the id
        has no proposal.md at REF at all; CHANGE_DIR carries no proposal.md IN
        THE WORKING TREE (the CURRENT declaration cannot be read, so the gate
        cannot run, and the absent file is NOT read as `ABSENT` and compared,
        which would report a mutation nobody made or a retention nobody
        earned); or the front matter on EITHER side is malformed or
        unparseable. A declaration MUTATION — the gate running and finding a
        broken freeze — is exit 1.

        THE REFUSAL SET IS NOW THE SIBLING'S. `validate-scope-globs.py`
        --archive-gate refuses the same inputs, in the same order, with the
        same exit codes; `tests/sequenced_after/test_gate_parity.py` runs both
        CLIs over one set of git fixtures and asserts it, so a future divergence
        reds a check rather than being discovered by an operator.

    --sweep
        THE CORPUS SWEEP, re-runnable: the change-id population, the
        co-modified / sole-modifier split at REQUIREMENT granularity, how many
        changes declare the field, how many declare an explicit `[]` root claim,
        the surviving prose `Sequenced-after:` headers, and THE DEEPEST DECLARED
        CHAIN it resolves. Re-running it is what makes the
        "measured, not assumed" obligation discharge over time instead of ageing
        into a stale sentence. Exit 0 — a measurement is not a gate.

    --ledger-diff
        THE PER-CHANGE SWEEP LEDGER, checked against the live corpus. Prints the
        LEDGER-DERIVED reading — or the MEASURED one when the ledger cannot be
        read, so the re-runnable report survives a broken file — and then every
        stale, missing or extra ROW BY NAME. Exit 1 when the ledger disagrees
        with the corpus — unlike `--sweep`, this IS a gate, because a ledger
        that no longer describes the corpus is a stale pin rather than a
        measurement. Exit 2 when the ledger cannot be READ AT ALL, which is a
        different fact from a stale one: a stale ledger is repaired by moving a
        row, an unreadable one by fixing the file, and reporting them under one
        code would send an author to the wrong repair.

    --seed-ledger --moved-by '#PR' [--moved-on YYYY-MM-DD] [--seeded-from SHA]
        REWRITE the ledger from the live corpus, stamping `moved_by`/`moved_on`
        on the rows that actually moved and PRESERVING the provenance of every
        row that did not. This is how an author moves a row: run it, then read
        the diff as the list of rows the change moved. `--moved-by` is REQUIRED
        — a moved row with no moving pull request is provenance nobody can
        follow. `--moved-on` defaults to TODAY IN UTC, never the machine's local
        date.

        A ROW FLIPPING `active` -> `archived` TAKES ITS DIRECTORY'S DATE, not
        the run's: at that one moment the row's move and the archive are the
        same act. EVERY OTHER ROW — including a row created for a change that
        was already archived, and an archived row moved later by some other
        change — takes the run's date, because `release-realization` defines
        `moved_on` as the date THAT MOVE happened. An explicit `--moved-on`
        that disagrees with a FLIPPING row's directory is REFUSED (exit 2,
        naming the rows and their dates) rather than silently overridden, and a
        flipping row whose directory is dated AFTER today in UTC is refused
        too — that directory was named by a clock running ahead of UTC.

        AN EXISTING LEDGER TOO MALFORMED TO READ DOES NOT BLOCK THE REPAIR: the
        seeder says so on stderr and rewrites from the live corpus, stamping
        EVERY row (none of the old provenance could be read, so none of it can
        be preserved) and dropping `seeded_from` unless `--seeded-from` is
        given. Refusing here would leave the only tool that can fix the file
        unusable on the only file that needs fixing.

    --repository NAME
        The declaring repository token, which decides which qualified entries
        normalize to the bare form (default: openxFactory).

    `--archive-gate`, `--sweep`, `--ledger-diff` and `--seed-ledger` are MODES
    and are mutually exclusive: combining two can only mean the caller believed
    both would run, and silently running whichever the dispatch reaches first is
    the answer to a question nobody asked.

    A FLAG OUTSIDE ITS MODE IS REFUSED FOR THE SAME REASON, rather than accepted
    and ignored. `--ratified-ref` belongs to `--archive-gate`;
    `--moved-by`, `--moved-on` and `--seeded-from` belong to `--seed-ledger`;
    `--strict-archive-dates` belongs to the plain run, which is the only place
    the archive-date arm runs. `--ledger-diff --moved-by garbage` exiting 0
    would tell a caller their flag was honoured when nothing read it.
"""
from __future__ import annotations

import argparse
import datetime
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import sequenced_after as sa  # noqa: E402


def _utc_today() -> str:
    """TODAY IN UTC — what an unspecified `--moved-on` stamps.

    `datetime.date.today()` read the MACHINE'S LOCAL clock, so a row moved at
    23:35 local recorded the previous UTC day (issue #790, the same defect
    `scripts/proposal-support.py` carried on the other side of the same
    archive). Every other date in this estate is UTC, and a provenance date
    whose meaning depends on where the author was sitting is provenance nobody
    can place.
    """
    return datetime.datetime.now(datetime.timezone.utc).date().isoformat()


def _validate_change(repo_root: Path, change_id: str, proposal: Path,
                     repository: str) -> list[str]:
    """Return a list of problem strings for one proposal (empty when clean)."""
    try:
        raw = sa.read_declaration(proposal)
    except sa.SequencedAfterError as exc:
        return [str(exc)]
    if raw is sa.ABSENT:
        # ABSENCE IS NOT AN ERROR AND IS NOT A ROOT CLAIM. The change has made no
        # declaration about its chain position; the prose sequencing obligation
        # remains sufficient for every purpose other than a mechanical walk.
        return []
    try:
        sa.validate_declaration(repo_root, change_id, raw,
                                declaring_repository=repository)
    except sa.SequencedAfterError as exc:
        return [str(exc)]
    return []


def _archive_date_arm(repo_root: Path,
                      require_equal: bool) -> tuple[list[str], str | None]:
    """The archive-date findings, or the reason the arm could not run.

    The ledger is READ HERE and nowhere else on this path, and a ledger that is
    missing or unparseable is NOT this arm's finding: `--ledger-diff` owns
    ledger readability and answers it with exit 2, a status this run does not
    have and must not invent. So the arm says it could not run, and the plain
    run's own verdict is untouched.
    """
    path = sa.ledger_path(repo_root)
    if not path.is_file():
        return [], f"there is no per-change sweep ledger at {path}"
    try:
        ledger = sa.load_ledger(path)
    except sa.SequencedAfterError as exc:
        return [], (f"the per-change sweep ledger could not be read ({exc}); "
                    "--ledger-diff reports that class")
    return sa.archive_date_problems(repo_root, ledger,
                                    require_equal=require_equal), None


def _archive_commit_arm(
    repo_root: Path,
) -> tuple[list[str], "sa.ArchiveDateDispositions | None",
           tuple[str, str] | None]:
    """The `archive-date-vs-commit` findings, the severity the record
    asks for, or the reason the arm could not run.

    THE ORDER OF THE TWO REFUSALS IS THE POINT. Git is probed FIRST, and a
    checkout that cannot answer the question — not a work-tree root, or shallow
    — is `NOT RUN` and leaves the verdict alone, because that is a property of
    the CHECKOUT and not of the repository: refusing there would red every
    consumer who validates an exported tree, and inventing findings from a
    history that does not describe it would be worse. The RECORD is read second,
    and a missing or unreadable one is `CANNOT RUN` with exit 2, because that IS
    a property of the repository — the arm's whole basis for calling a
    disagreement dispositioned is a file that is part of this diff, and reading
    "no record" as "no dispositions" would turn one bad line into twelve
    findings whose real cause is the file.
    """
    try:
        added = sa.adding_commits(repo_root)
    except sa.ArchiveHistoryUnavailable as exc:
        # THE CHECKOUT DECLINES THE QUESTION — not a work-tree root, nested,
        # shallow, no git at all. Caught FIRST because it is a SUBCLASS.
        return [], None, ("NOT RUN", str(exc))
    except sa.SequencedAfterError as exc:
        # GIT FAILED, in a checkout that claimed it could answer. Reporting
        # that as NOT RUN would leave the run green with a gate the record asks
        # for at `error` silently off (Codex P2, PR #820).
        return [], None, ("CANNOT RUN", str(exc))
    path = sa.dispositions_path(repo_root)
    if not path.is_file():
        return [], None, ("CANNOT RUN",
                          f"there is no archive-date disposition record at "
                          f"{path}")
    try:
        record = sa.load_archive_date_dispositions(path)
    except sa.SequencedAfterError as exc:
        return [], None, ("CANNOT RUN", str(exc))
    return sa.archive_commit_problems(repo_root, added, record), record, None


def validate_corpus(repo_root: Path, repository: str,
                    strict_archive_dates: bool = False) -> int:
    problems: list[str] = []
    declared = 0
    active = sa.active_change_dirs(repo_root)
    for change_id, change_dir in active.items():
        proposal = change_dir / "proposal.md"
        if not proposal.is_file():
            continue
        try:
            if sa.read_declaration(proposal) is not sa.ABSENT:
                declared += 1
        except sa.SequencedAfterError:
            pass  # reported by _validate_change below
        for problem in _validate_change(repo_root, change_id, proposal, repository):
            problems.append(f"{change_id}: {problem}")
    if problems:
        print("sequenced_after validation FAILED:")
        for problem in problems:
            print(f"  - {problem}")
        return 1
    print(f"sequenced_after validation passed ({len(active)} active changes, "
          f"{declared} declaring the field).")

    # THE ARCHIVE-DATE ARM. It GATES, in the one direction that is a
    # contradiction under any reading of the provenance pair: an archived row
    # whose `moved_on` PREDATES the directory it describes claims a move older
    # than the archive that made it archived. Measured across this corpus
    # before it was made a gate — 143 archived rows, 0 findings — and it is
    # exactly the shape a CLI clock running AHEAD of UTC produces.
    #
    # IT DOES NOT REQUIRE EQUALITY, and that is a correction taken from review
    # rather than a softening. `release-realization` defines `moved_on` as the
    # date the ROW last moved, so an archived row moved later by another
    # change legitimately carries a later date — 124 of the 143 do, none of
    # them a defect. Requiring equality by default would report a correct
    # ledger as stale and red the required `pytest-suite` check on rows nobody
    # in flight put there. `--strict-archive-dates` asks for that stronger
    # reading, which is the one issue #790 proposed, and is opt-in.
    status = 0
    findings, unavailable = _archive_date_arm(repo_root, strict_archive_dates)
    if unavailable is not None:
        print(f"archive-date arm NOT RUN: {unavailable}.")
    elif findings:
        print(f"archive-date agreement FAILED ({len(findings)} finding(s)):")
        for problem in findings:
            print(f"  - {problem}")
        status = 1
    else:
        print("archive-date agreement passed (no archived row's moved_on "
              "predates its directory"
              + ("; --strict-archive-dates also required equality)."
                 if strict_archive_dates else ")."))

    # THE SECOND ARCHIVE-DATE ARM, and it RUNS EVEN WHEN THE FIRST FAILED
    # (issue #812). The two read different things — the first a ledger row
    # against a directory name, this one a directory name against the UTC date
    # of the commit that added it — so an early `return 1` above would hide a
    # whole class of finding behind an unrelated one, and an author repairing
    # the ledger would then discover the second class only on the next run.
    # `--strict-archive-dates` asks BOTH arms for their stronger reading.
    problems, record, note = _archive_commit_arm(repo_root)
    if note is not None:
        kind, reason = note
        print(f"archive-date-vs-commit arm {kind}: {reason}.")
        if kind == "CANNOT RUN":
            # EXIT 2 WINS OVER THE FIRST ARM'S EXIT 1. "The run could not do
            # its job" and "the corpus disagrees" want different repairs, and
            # the first is the one the author must fix before the second
            # reading means anything.
            return 2
    elif problems:
        # THE RECORD CARRIES THE DIAL, so a repository can adopt this arm and
        # measure before it gates; `--strict-archive-dates` overrides it upward
        # and never downward.
        severe = (strict_archive_dates
                  or record.enforcement == sa.ENFORCEMENT_ERROR)
        print(f"archive-date-vs-commit "
              f"{'FAILED' if severe else 'WARNING'} ({len(problems)} "
              f"finding(s)):")
        for problem in problems:
            print(f"  - {problem}")
        print(f"Disposition each measured disagreement once in "
              f"{sa.DISPOSITIONS_REL}, citing the adding commit, the fact and "
              f"the ruling; remove any entry reported STALE.")
        if severe:
            status = 1
    else:
        print(f"archive-date-vs-commit agreement passed (every archived "
              f"directory is named for the UTC date of the commit that added "
              f"it, or is dispositioned in place; {len(record.order)} "
              f"disposition(s) in force, enforcement {record.enforcement}).")
    return status


def _archive_gate(change_dir: Path, ratified_ref: str) -> int:
    try:
        problem = sa.retention_at_archive(change_dir, ratified_ref)
    except (sa.SequencedAfterError, subprocess.CalledProcessError) as exc:
        # UNRUNNABLE IS NOT A MUTATION FINDING (exit 1) AND NOT A TRACEBACK.
        # THE CATCH IS DELIBERATELY ON THE WHOLE ERROR CLASS, not on an
        # enumerated few: the id names no proposal.md at `ratified_ref`,
        # CHANGE_DIR carries no proposal.md in the working tree so the
        # current-side declaration cannot be read, the front matter on either
        # side does not parse — every one of them is the same distinct fact,
        # that the gate could not READ what it compares, and every one is
        # reported the way every other refusal in this CLI is: a named finding
        # and exit 2, the same shape `validate-scope-globs.py` uses for its own
        # gate. A new refusal added to the substrate lands here correctly
        # without this comment having to be revised.
        #
        # `CalledProcessError` is caught BESIDE it as a backstop, the same way
        # `validate-scope-globs.py` does: no git call on this path is expected
        # to reach the caller unhandled any more — the work-tree probe and the
        # ref-commit probe are the two that used to — and if one ever does, it
        # is still reported rather than traced.
        print("sequenced_after PARENT-DECLARATION-RETENTION gate CANNOT RUN:")
        print(f"  - {exc}")
        return 2
    if problem is not None:
        print("sequenced_after PARENT-DECLARATION-RETENTION gate FAILED (contested):")
        print(f"  - {problem}")
        return 1
    print("sequenced_after retention gate passed (declaration unchanged since "
          "ratification).")
    return 0


def _ledger_diff(repo_root: Path, repository: str) -> int:
    """Report the ledger against the live corpus. Exit 1 when it is stale.

    Prints the LEDGER-DERIVED reading where the ledger can be read, and the
    MEASURED one otherwise, so the re-runnable report survives a stale file.
    """
    readings = sa.classify_corpus(repo_root, declaring_repository=repository)
    measured = sa.corpus_sweep(repo_root, declaring_repository=repository)
    problems: list[str] = []
    path = sa.ledger_path(repo_root)
    ledger = None
    if not path.is_file():
        problems.append(f"malformed ledger: {path} does not exist")
    else:
        try:
            ledger = sa.load_ledger(path)
        except sa.SequencedAfterError as exc:
            # UNREADABLE IS NOT STALE. Exit 2 rather than 1, because the two
            # want different repairs: a stale ledger is fixed by re-seeding a
            # row, an unreadable one by fixing the file it could not parse.
            print(measured.render())
            print()
            print(f"per-change sweep ledger CANNOT BE READ:\n  - {exc}")
            print("Fix the file, or rewrite it with: python3 "
                  "scripts/validate-sequenced-after.py . --seed-ledger "
                  "--moved-by '#<PR>'")
            return 2
    if ledger is not None:
        problems.extend(sa.ledger_problems(readings, ledger))
        try:
            derived = sa.sweep_from_readings(sa.readings_from_ledger(ledger))
        except sa.SequencedAfterError as exc:
            problems.append(str(exc))
            derived = None
    else:
        derived = None
    if derived is not None:
        print(derived.render())
        problems.extend(sa.sweep_mismatches(derived, measured))
    else:
        print(measured.render())
    print()
    if problems:
        print(f"per-change sweep ledger STALE ({len(problems)} finding(s)):")
        for problem in problems:
            print(f"  - {problem}")
        print("Re-seed with: python3 scripts/validate-sequenced-after.py . "
              "--seed-ledger --moved-by '#<PR>'")
        return 1
    print(f"per-change sweep ledger consistent with the corpus "
          f"({len(readings)} rows).")
    return 0


def _seed_ledger(repo_root: Path, repository: str, moved_by: str,
                 moved_on: str | None, seeded_from: str | None) -> int:
    """Rewrite the ledger from the live corpus, preserving unmoved provenance.

    EVERY refusal below the CLI arrives as a MESSAGE AND AN EXIT CODE, never as
    a traceback: a stack trace tells an author where the library gave up and
    not what they should type instead, and this command's whole purpose is to
    be the thing an author runs when something is wrong with the ledger.
    """
    try:
        return _seed_ledger_inner(repo_root, repository, moved_by, moved_on,
                                  seeded_from)
    except sa.SequencedAfterError as exc:
        print(f"--seed-ledger refused: {exc}", file=sys.stderr)
        return 2


def _seed_ledger_inner(repo_root: Path, repository: str, moved_by: str,
                       moved_on: str | None, seeded_from: str | None) -> int:
    readings = sa.classify_corpus(repo_root, declaring_repository=repository)
    path = sa.ledger_path(repo_root)
    previous = None
    if path.is_file():
        try:
            previous = sa.load_ledger(path)
        except sa.SequencedAfterError as exc:
            # THE SEEDER IS THE REPAIR. Refusing to read a broken ledger would
            # leave the only tool that can rewrite it unusable on the only file
            # that needs rewriting, so it says what it could not read and
            # re-seeds from the corpus instead.
            print(f"the existing ledger could not be read ({exc}); re-seeding "
                  f"from the live corpus, so EVERY row is stamped "
                  f"{moved_by} and `seeded_from` is dropped unless "
                  f"--seeded-from is given", file=sys.stderr)
    # THE ROWS THIS RUN MOVES, from the same helper the renderer stamps by, so
    # the summary cannot overcount: a row that merely already carried this pull
    # request is NOT one this run moved.
    moved = sa.moved_rows(readings, previous)
    dates = sa.archive_dates(repo_root)
    # AN EXPLICIT `--moved-on` THAT THE ARCHIVE DIRECTORIES CONTRADICT IS
    # REFUSED, never quietly overridden. An archived row's `moved_on` and its
    # `archive/<YYYY-MM-DD>-<id>` directory are ONE FACT (issue #790), so the
    # directory wins — but a caller who typed a date and got a different one
    # written was told their flag was honoured when it was not, which is the
    # same mistake `_mode_only` refuses one level up.
    flipping = [change_id for change_id in moved
                if sa.flips_to_archived(change_id, readings[change_id],
                                        previous) and change_id in dates]
    # A DIRECTORY DATED AFTER TODAY IN UTC IS REFUSED BEFORE IT IS STAMPED.
    # `moved_on` would then predate the archive it describes, which is the one
    # thing the validator's archive-date arm calls a contradiction — and it is
    # the shape a CLI clock running AHEAD of UTC produces (issue #790). Writing
    # it and then failing the corpus check on the next run is two acts where
    # one refusal will do.
    today = _utc_today()
    ahead = [(cid, dates[cid]) for cid in flipping if dates[cid] > today]
    if ahead:
        listed = ", ".join(f"{cid} ({on})" for cid, on in ahead[:5])
        raise sa.SequencedAfterError(
            f"{len(ahead)} row(s) flipping to archived carry a directory "
            f"dated AFTER today in UTC ({today}): {listed}. That directory was "
            f"named by a clock running ahead of UTC, and stamping its date as "
            f"`moved_on` would record a move older than the archive it "
            f"describes. Repair the directory name first — "
            f"`proposal-support.py archive` now refuses to create one")
    if moved_on is not None:
        disagreeing = [(change_id, dates[change_id]) for change_id in flipping
                       if dates[change_id] != moved_on]
        if disagreeing:
            listed = ", ".join(f"{cid} ({on})" for cid, on in disagreeing[:5])
            more = ("" if len(disagreeing) <= 5
                    else f", … and {len(disagreeing) - 5} more")
            raise sa.SequencedAfterError(
                f"--moved-on {moved_on!r} disagrees with the archived "
                f"directory of {len(disagreeing)} row(s) this re-seed FLIPS to "
                f"archived: {listed}{more}. At the flip the row's move and the "
                f"archive are the same act, so its moved_on IS the date its "
                f"archive/<YYYY-MM-DD>-<id> directory carries and a re-seed "
                f"cannot stamp another day on it. Drop --moved-on (a flipping "
                f"row then takes its directory's date and every other row "
                f"takes today in UTC), or pass the date those directories "
                f"carry")
    text = sa.render_ledger(
        readings, moved_by=moved_by,
        # `today`, READ ONCE ABOVE, not a second reading: two calls straddling
        # midnight UTC would refuse against one date and stamp another.
        #
        # `is None`, NOT `or`, and for the reason the archive half states: `or`
        # cannot tell "the caller named nothing" from "the caller named
        # something falsy", and silently substituting today for a value someone
        # passed would report a flag as honoured when nothing read it.
        #
        # THIS ONE WAS ALREADY UNREACHABLE, and the record should say so rather
        # than claim a fix it did not make: an empty `--moved-on` is refused by
        # `main` (`--moved-on must be an ISO date (YYYY-MM-DD), not ''`) and
        # AGAIN by `render_ledger` itself, which runs `is_moved_on` over the
        # value before it writes a line — remove either guard and the other
        # still refuses. Unlike `archive`'s `args.date or today`, which was a
        # live defect, this is a predicate that says what it means where it
        # previously only happened to be right. (Copilot round 3, taken as
        # clarity; the finding's premise that the value reaches here was wrong.)
        moved_on=today if moved_on is None else moved_on,
        previous=previous, seeded_from=seeded_from, archive_dates=dates)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    print(f"wrote {path} ({len(readings)} rows, {len(moved)} moved by "
          f"{moved_by}).")
    for change_id in moved[:20]:
        print(f"  - {change_id}")
    if len(moved) > 20:
        print(f"  … and {len(moved) - 20} more; read the diff.")
    return 0


def _mode_only(parser: argparse.ArgumentParser, args: argparse.Namespace,
               flag: str, given: bool, mode: str, mode_selected: object) -> None:
    """Refuse `flag` unless `mode` is the selected mode."""
    if given and not mode_selected:
        parser.error(f"{flag} is only meaningful with {mode}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("repo_root", nargs="?", default=".",
                        help="repository root to scan (default: cwd)")
    # THE MODES ARE MUTUALLY EXCLUSIVE, declared rather than resolved by the
    # order of the dispatch below: combining two of them can only mean the
    # caller believed both would run, and silently running the first is the
    # answer to a question nobody asked.
    modes = parser.add_mutually_exclusive_group()
    modes.add_argument("--archive-gate", metavar="CHANGE_DIR",
                       help="run the parent-declaration retention freeze gate "
                            "on one change dir")
    parser.add_argument("--ratified-ref", metavar="REF",
                        help="git ref carrying the ratified proposal (with "
                             "--archive-gate)")
    modes.add_argument("--sweep", action="store_true",
                       help="print the re-runnable corpus sweep (a measurement, "
                            "not a gate) and exit 0")
    modes.add_argument("--ledger-diff", action="store_true",
                       help="check the per-change sweep ledger against the "
                            "live corpus, naming every stale row; exit 1 when "
                            "it is stale")
    modes.add_argument("--seed-ledger", action="store_true",
                       help="rewrite the per-change sweep ledger from the live "
                            "corpus, preserving the provenance of unmoved rows")
    parser.add_argument("--moved-by", metavar="#PR",
                        help="the pull request stamped on the rows this "
                             "re-seed moves; REQUIRED with --seed-ledger")
    parser.add_argument("--moved-on", metavar="YYYY-MM-DD",
                        help="the date stamped on the rows this re-seed moves "
                             "(default: TODAY IN UTC, never the machine's "
                             "local date). A row FLIPPING to archived takes "
                             "its directory's date instead, and a --moved-on "
                             "that contradicts one is REFUSED")
    parser.add_argument("--seeded-from", metavar="SHA",
                        help="record the commit the ledger was first seeded "
                             "from; omitted, the existing value is preserved")
    parser.add_argument("--strict-archive-dates", action="store_true",
                        help="ALSO require every archived row's moved_on to "
                             "EQUAL its directory's date, not merely not to "
                             "predate it (124 rows legitimately carry a later "
                             "move date, so this is opt-in), AND read the "
                             "`archive-date-vs-commit` arm at `error` "
                             "whatever dial its record carries")
    parser.add_argument("--repository", default=sa.DECLARING_REPOSITORY,
                        help="declaring repository token (default: "
                             f"{sa.DECLARING_REPOSITORY})")
    args = parser.parse_args(argv)

    # A FLAG OUTSIDE ITS MODE IS REFUSED, NOT SILENTLY IGNORED. The modes
    # already refuse to combine on the reasoning that "combining two can only
    # mean the caller believed both would run"; accepting `--ledger-diff
    # --moved-by garbage` and exiting 0 is the same mistake wearing a different
    # hat — the caller believed the flag did something, and it did nothing.
    _mode_only(parser, args, "--ratified-ref", args.ratified_ref is not None,
               "--archive-gate", args.archive_gate)
    if args.strict_archive_dates and (args.archive_gate or args.sweep
                                      or args.ledger_diff or args.seed_ledger):
        parser.error("--strict-archive-dates is only meaningful on the plain "
                     "validation run, which is where the archive-date arm runs")
    for flag, given in (("--moved-by", args.moved_by is not None),
                        ("--moved-on", args.moved_on is not None),
                        ("--seeded-from", args.seeded_from is not None)):
        _mode_only(parser, args, flag, given, "--seed-ledger", args.seed_ledger)

    if args.archive_gate:
        if not args.ratified_ref:
            parser.error("--archive-gate requires --ratified-ref")
        # A RELATIVE CHANGE_DIR RESOLVES AGAINST `repo_root`, like every other
        # mode's paths, not against the current directory. Absolute paths are
        # unaffected, and so is the ordinary `--archive-gate openspec/changes/x`
        # run from the repo root, `repo_root` defaulting to `.`. What changes is
        # `validate-sequenced-after.py path/to/repo --archive-gate
        # openspec/changes/x`, which resolved against the CWD: at best it failed
        # to find the directory, and at worst it found a DIFFERENT repository's
        # change of the same name and gated THAT — the failure mode a gate can
        # least afford, because it passes.
        change_dir = Path(args.archive_gate)
        if not change_dir.is_absolute():
            change_dir = Path(args.repo_root) / change_dir
        return _archive_gate(change_dir, args.ratified_ref)

    if args.ledger_diff:
        return _ledger_diff(Path(args.repo_root), args.repository)

    if args.seed_ledger:
        # ARGUMENT SHAPE IS ARGPARSE'S TO REFUSE, at the boundary and in its own
        # voice, rather than a library exception surfacing as a stack trace six
        # frames down.
        if not args.moved_by:
            parser.error("--seed-ledger requires --moved-by '#<PR>'")
        if not sa.MOVED_BY.match(args.moved_by):
            parser.error(f"--moved-by must be a pull request reference like "
                         f"'#620', not {args.moved_by!r}")
        if args.moved_on is not None and not sa.is_moved_on(args.moved_on):
            parser.error(f"--moved-on must be an ISO date (YYYY-MM-DD), not "
                         f"{args.moved_on!r}")
        return _seed_ledger(Path(args.repo_root), args.repository,
                            args.moved_by, args.moved_on, args.seeded_from)

    if args.sweep:
        print(sa.corpus_sweep(Path(args.repo_root),
                              declaring_repository=args.repository).render())
        return 0

    return validate_corpus(Path(args.repo_root), args.repository,
                           strict_archive_dates=args.strict_archive_dates)


if __name__ == "__main__":
    raise SystemExit(main())
