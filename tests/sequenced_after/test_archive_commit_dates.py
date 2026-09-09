"""The ARCHIVE-DATE-vs-ADDING-COMMIT arm (issue #812), and the disposition
record it reads.

#797 made `proposal-support.py archive` own the clock GOING FORWARD and gated
the ledger against the directory name. Neither arm looks at HISTORY, so the ten
directories a local clock one day behind UTC named before either existed were
invisible to both. This arm measures every archived directory against the UTC
date of the commit that added it; the record is where a measured disagreement is
accepted, once, in place, with the ruling that accepted it.

THE FIXTURES ARE REAL GIT REPOSITORIES with controlled commit dates, because the
whole arm is a statement about history and a fixture that faked the walk would
assert only that the fake was read.
"""
from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
MODULE = ROOT / "scripts" / "sequenced_after.py"
VALIDATOR = ROOT / "scripts" / "validate-sequenced-after.py"


def _load():
    # NOT under the name `sequenced_after`: this directory is a package by that
    # name, and registering the script module under it aborts collection of
    # every sibling module. Same route the other modules here take.
    spec = importlib.util.spec_from_file_location("sequenced_after_substrate",
                                                  MODULE)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


sa = _load()

RULED = 'Brett Heap 2026-09-08 "rule 1 + 2a on 812"'
CITED = "opensoft/openxFactory#812"


# --- fixtures: real repositories, real commit dates --------------------------


def _run(args, cwd, env=None):
    result = subprocess.run(args, cwd=str(cwd), capture_output=True, text=True,
                            env=env)
    assert result.returncode == 0, (args, result.stdout, result.stderr)
    return result


def _repo(path: Path) -> Path:
    path.mkdir(parents=True, exist_ok=True)
    _run(["git", "init", "-q", "-b", "main", "."], path)
    _run(["git", "config", "user.email", "arm@example.invalid"], path)
    _run(["git", "config", "user.name", "Arm Fixture"], path)
    _run(["git", "config", "commit.gpgsign", "false"], path)
    return path


def _write(root: Path, directory: str) -> None:
    change = root / "openspec" / "changes" / "archive" / directory
    change.mkdir(parents=True, exist_ok=True)
    (change / "proposal.md").write_text(
        f"---\ncode_surface: openxFactory\n---\n\n# {directory}\n",
        encoding="utf-8")


def _commit(root: Path, when: str, message: str = "archive") -> str:
    """Commit everything staged-or-not at an EXACT instant.

    `when` carries an OFFSET (`2026-08-05T00:30:00+00:00`), which is the whole
    point: the defect this arm measures is a directory named from a local clock
    while the commit's UTC day is the next one, and a fixture without offsets
    could not express it.
    """
    import os
    env = dict(os.environ, GIT_AUTHOR_DATE=when, GIT_COMMITTER_DATE=when)
    _run(["git", "add", "-A"], root)
    _run(["git", "commit", "-q", "-m", message], root, env=env)
    return _run(["git", "rev-parse", "HEAD"], root).stdout.strip()


def _entry(directory: str, dated: str, sha: str, day: str,
           fact: str = "named by a local clock one day behind UTC") -> dict:
    return {"directory": directory, "directory_date": dated,
            "adding_commit": sha, "commit_date_utc": day, "fact": fact,
            "ruled_by": RULED, "cited_to": CITED}


def _record(root: Path, entries: list[dict], enforcement: str = "error") -> Path:
    path = sa.dispositions_path(root)
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = ["schema_version: 1", "kind: archive_date_dispositions", "",
             f"enforcement: {enforcement}", "", "dispositions:"]
    for entry in entries:
        first = True
        for key in sa.DISPOSITION_KEYS:
            lead = "  - " if first else "    "
            first = False
            lines.append(f"{lead}{key}: {json.dumps(entry[key])}")
    if not entries:
        lines[-1] = "dispositions: []"
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return path


def _validate(root: Path, *flags: str) -> subprocess.CompletedProcess:
    return subprocess.run([sys.executable, str(VALIDATOR), str(root), *flags],
                          capture_output=True, text=True)


# --- the measurement ---------------------------------------------------------


def test_a_ONE_DAY_EARLY_directory_is_a_NAMED_FINDING(tmp_path):
    """The exact shape of the ten: the name is 2026-08-04, the commit's UTC day
    is 2026-08-05, and nothing in #797 can see it."""
    root = _repo(tmp_path / "repo")
    _write(root, "2026-08-04-add-thing")
    sha = _commit(root, "2026-08-05T00:30:00+00:00")
    _record(root, [])
    result = _validate(root)
    assert result.returncode == 1, result.stdout + result.stderr
    assert ("archive-date-vs-commit: 2026-08-04-add-thing: dated 2026-08-04, "
            f"added 2026-08-05 by {sha} — undispositioned") in result.stdout


def test_a_DISPOSITIONED_disagreement_is_SILENT(tmp_path):
    root = _repo(tmp_path / "repo")
    _write(root, "2026-08-04-add-thing")
    sha = _commit(root, "2026-08-05T00:30:00+00:00")
    _record(root, [_entry("2026-08-04-add-thing", "2026-08-04", sha,
                          "2026-08-05")])
    result = _validate(root)
    assert result.returncode == 0, result.stdout + result.stderr
    assert "undispositioned" not in result.stdout
    assert "archive-date-vs-commit agreement passed" in result.stdout
    assert "1 disposition(s) in force" in result.stdout


def test_a_DIRECTORY_THAT_AGREES_is_SILENT_and_needs_no_entry(tmp_path):
    root = _repo(tmp_path / "repo")
    _write(root, "2026-08-05-add-thing")
    _commit(root, "2026-08-05T00:30:00+00:00")
    _record(root, [])
    result = _validate(root)
    assert result.returncode == 0, result.stdout + result.stderr
    assert "archive-date-vs-commit agreement passed" in result.stdout
    assert "0 disposition(s) in force" in result.stdout


def test_the_LOCAL_CLOCK_SHAPE_is_what_it_catches_not_merely_a_string_compare(
        tmp_path):
    """23:30 on the 4th in a zone one hour BEHIND UTC is 00:30 on the 5th in
    UTC. The directory was named 2026-08-04 by that local clock, and the arm
    reads the commit in UTC — which is the whole defect, and the reason the
    comparison converts rather than slicing the timestamp string."""
    root = _repo(tmp_path / "repo")
    _write(root, "2026-08-04-add-thing")
    sha = _commit(root, "2026-08-04T23:30:00-01:00")
    added = sa.adding_commits(root)
    assert added["2026-08-04-add-thing"] == (sha, "2026-08-05")
    _record(root, [])
    assert _validate(root).returncode == 1


def test_the_INITIAL_IMPORT_SHAPE_attributes_MANY_directories_to_ONE_commit(
        tmp_path):
    """`746be44f` added this corpus's two oldest directories in one commit, six
    days after the date their names carry. One walk, oldest-first, must give
    both of them that commit — not one of them, and not the commit that
    happened to touch each first afterwards."""
    root = _repo(tmp_path / "repo")
    _write(root, "2026-06-26-enable-live")
    _write(root, "2026-06-26-migrate-policy")
    sha = _commit(root, "2026-07-02T18:18:41+08:00", "initial import")
    # A LATER commit touching one of them must not become its adding commit.
    (root / "openspec" / "changes" / "archive" / "2026-06-26-enable-live"
     / "notes.md").write_text("later\n", encoding="utf-8")
    _commit(root, "2026-07-09T00:00:00+00:00", "later touch")
    added = sa.adding_commits(root)
    assert added["2026-06-26-enable-live"] == (sha, "2026-07-02")
    assert added["2026-06-26-migrate-policy"] == (sha, "2026-07-02")
    _record(root, [])
    result = _validate(root)
    assert result.returncode == 1, result.stdout
    for name in ("2026-06-26-enable-live", "2026-06-26-migrate-policy"):
        assert (f"archive-date-vs-commit: {name}: dated 2026-06-26, added "
                f"2026-07-02 by {sha} — undispositioned") in result.stdout


def test_an_UNCOMMITTED_archive_directory_is_SKIPPED_not_reported(tmp_path):
    """It has no adding commit yet, so there is no date in history to disagree
    with. Its clock is `proposal-support.py archive`'s to own at creation."""
    root = _repo(tmp_path / "repo")
    _write(root, "2026-08-05-add-thing")
    _commit(root, "2026-08-05T00:30:00+00:00")
    _write(root, "1999-01-01-not-committed")
    _record(root, [])
    result = _validate(root)
    assert result.returncode == 0, result.stdout + result.stderr
    assert "1999-01-01-not-committed" not in result.stdout


def test_a_NON_CHANGE_FILE_directly_under_archive_dates_nothing(tmp_path):
    root = _repo(tmp_path / "repo")
    archive = root / "openspec" / "changes" / "archive"
    archive.mkdir(parents=True)
    (archive / "README.md").write_text("index\n", encoding="utf-8")
    _commit(root, "2026-08-05T00:30:00+00:00")
    assert sa.adding_commits(root) == {}


# --- stale dispositions ------------------------------------------------------


def test_a_disposition_for_a_directory_THAT_AGREES_is_STALE(tmp_path):
    root = _repo(tmp_path / "repo")
    _write(root, "2026-08-05-add-thing")
    sha = _commit(root, "2026-08-05T00:30:00+00:00")
    _record(root, [_entry("2026-08-05-add-thing", "2026-08-05", sha,
                          "2026-08-05")])
    result = _validate(root)
    assert result.returncode == 1, result.stdout + result.stderr
    assert ("archive-date-disposition STALE: 2026-08-05-add-thing: the "
            "directory AGREES with the UTC date of its adding commit") \
        in result.stdout


def test_a_disposition_for_a_directory_THAT_NO_LONGER_EXISTS_is_STALE(tmp_path):
    root = _repo(tmp_path / "repo")
    _write(root, "2026-08-05-add-thing")
    _commit(root, "2026-08-05T00:30:00+00:00")
    _record(root, [_entry("2026-08-04-was-renamed-away", "2026-08-04",
                          "0" * 40, "2026-08-05")])
    result = _validate(root)
    assert result.returncode == 1, result.stdout + result.stderr
    assert ("archive-date-disposition STALE: 2026-08-04-was-renamed-away: no "
            "archived directory of that name exists") in result.stdout


def test_a_disposition_CITING_THE_WRONG_COMMIT_OR_DATE_is_STALE(tmp_path):
    """The entry's authority is that it states a fact anyone can re-measure. An
    entry citing a commit history does not carry disposes of nothing."""
    root = _repo(tmp_path / "repo")
    _write(root, "2026-08-04-add-thing")
    sha = _commit(root, "2026-08-05T00:30:00+00:00")
    _record(root, [_entry("2026-08-04-add-thing", "2026-08-04", "a" * 40,
                          "2026-08-09")])
    result = _validate(root)
    assert result.returncode == 1, result.stdout + result.stderr
    assert "archive-date-disposition STALE: 2026-08-04-add-thing" in result.stdout
    assert f"adding_commit '{'a' * 40}' where history says '{sha}'" in result.stdout
    assert "commit_date_utc '2026-08-09' where history says '2026-08-05'" \
        in result.stdout
    # …and the finding it silenced is NOT ALSO reported: one fact, one repair.
    assert "undispositioned" not in result.stdout


# --- the record cannot be read ----------------------------------------------


def test_a_MISSING_RECORD_is_CANNOT_RUN_and_exits_2(tmp_path):
    root = _repo(tmp_path / "repo")
    _write(root, "2026-08-05-add-thing")
    _commit(root, "2026-08-05T00:30:00+00:00")
    result = _validate(root)
    assert result.returncode == 2, result.stdout + result.stderr
    assert "archive-date-vs-commit arm CANNOT RUN" in result.stdout
    assert "there is no archive-date disposition record at" in result.stdout
    assert "Traceback" not in result.stderr


@pytest.mark.parametrize("text,fragment", [
    ("schema_version: 1\nkind: archive_date_dispositions\n"
     "enforcement: error\ndispositions: {}\n",
     "the `dispositions:` sequence is missing"),
    ("schema_version: 1\nkind: archive_date_dispositions\n"
     "enforcement: maybe\ndispositions: []\n",
     "`enforcement:` must be one of warning, error"),
    ("schema_version: 1\nkind: something_else\n"
     "enforcement: error\ndispositions: []\n",
     "must declare `schema_version: 1` and `kind: archive_date_dispositions`"),
    # The record's own header says the three FILE keys are deliberately not
    # quoted; quoting `schema_version` makes it the string "1" and the loader
    # refuses. Asserted so the comment's claim is checked, not merely written
    # (Copilot round 1).
    ('schema_version: "1"\nkind: archive_date_dispositions\n'
     "enforcement: error\ndispositions: []\n",
     "must declare `schema_version: 1` and `kind: archive_date_dispositions`"),
    ("schema_version: 1\nkind: archive_date_dispositions\n"
     "enforcement: error\ndispositions:\n  - directory: x\n",
     "is missing or empties"),
    ("schema_version: 1\nkind: archive_date_dispositions\n"
     "enforcement: error\ndispositions: [[not, a, mapping]]\n",
     "entry 1 is not a mapping"),
    ("schema_version: 1\nkind: archive_date_dispositions\nenforcement: error\n"
     "enforcement: error\ndispositions: []\n",
     "malformed archive-date disposition record"),
])
def test_an_UNREADABLE_RECORD_is_CANNOT_RUN_and_exits_2(tmp_path, text,
                                                        fragment):
    root = _repo(tmp_path / "repo")
    _write(root, "2026-08-05-add-thing")
    _commit(root, "2026-08-05T00:30:00+00:00")
    path = sa.dispositions_path(root)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    result = _validate(root)
    assert result.returncode == 2, (text, result.stdout, result.stderr)
    assert "archive-date-vs-commit arm CANNOT RUN" in result.stdout
    assert fragment in result.stdout, result.stdout
    assert "Traceback" not in result.stderr


def test_TWO_ENTRIES_FOR_ONE_DIRECTORY_are_refused_by_name(tmp_path):
    """The entries are a SEQUENCE, so the strict loader's duplicate-KEY refusal
    does not cover them. Last-one-wins would silently apply whichever decision
    the file ends with."""
    root = _repo(tmp_path / "repo")
    _write(root, "2026-08-04-add-thing")
    sha = _commit(root, "2026-08-05T00:30:00+00:00")
    _record(root, [_entry("2026-08-04-add-thing", "2026-08-04", sha,
                          "2026-08-05"),
                   _entry("2026-08-04-add-thing", "2026-08-04", sha,
                          "2026-08-05")])
    result = _validate(root)
    assert result.returncode == 2, result.stdout + result.stderr
    assert "is dispositioned twice (entries 1 and 2)" in result.stdout


def test_an_ABBREVIATED_SHA_is_REFUSED_because_the_record_is_a_citation(
        tmp_path):
    root = _repo(tmp_path / "repo")
    _write(root, "2026-08-04-add-thing")
    sha = _commit(root, "2026-08-05T00:30:00+00:00")
    _record(root, [_entry("2026-08-04-add-thing", "2026-08-04", sha[:8],
                          "2026-08-05")])
    result = _validate(root)
    assert result.returncode == 2, result.stdout + result.stderr
    assert "not a FULL 40-character object name" in result.stdout


# --- the checkout cannot answer ---------------------------------------------


def test_a_NON_GIT_TREE_is_NOT_RUN_and_leaves_the_verdict_ALONE(tmp_path):
    """A property of the CHECKOUT, not of the repository. Refusing here would
    red every consumer validating an exported tree, and every existing
    tmp_path corpus test in this suite."""
    _write(tmp_path, "2026-08-04-add-thing")
    result = _validate(tmp_path)
    assert result.returncode == 0, result.stdout + result.stderr
    assert "archive-date-vs-commit arm NOT RUN" in result.stdout
    assert "is not inside a git work tree" in result.stdout


def test_a_NESTED_TREE_is_NOT_RUN_because_history_does_not_describe_it(tmp_path):
    """A corpus written UNDER a checkout is untracked in it: every directory
    would read as having no adding commit, and every disposition as stale."""
    outer = _repo(tmp_path / "outer")
    (outer / "seed.txt").write_text("x\n", encoding="utf-8")
    _commit(outer, "2026-08-05T00:00:00+00:00", "seed")
    inner = outer / "nested"
    _write(inner, "2026-08-04-add-thing")
    result = _validate(inner)
    assert result.returncode == 0, result.stdout + result.stderr
    assert "archive-date-vs-commit arm NOT RUN" in result.stdout
    assert "is not the ROOT of a git work tree" in result.stdout


def test_a_SHALLOW_CLONE_is_NOT_RUN_rather_than_reporting_the_GRAFT_BOUNDARY(
        tmp_path):
    """THE GUARD THAT MATTERS MOST. In a depth-1 clone the boundary commit
    appears to have added every archived directory, so all but the newest would
    be reported as disagreements nobody made — a hundred findings with no cause
    an author could act on. `pytest-suite.yml` already checks out at
    `fetch-depth: 0`; a checkout that did not must say so, not invent."""
    origin = _repo(tmp_path / "origin")
    _write(origin, "2026-08-04-add-thing")
    _commit(origin, "2026-08-05T00:30:00+00:00", "one")
    (origin / "later.txt").write_text("x\n", encoding="utf-8")
    _commit(origin, "2026-08-30T00:00:00+00:00", "two")
    shallow = tmp_path / "shallow"
    _run(["git", "clone", "-q", "--depth", "1", origin.as_uri(), str(shallow)],
         tmp_path)
    assert _run(["git", "rev-parse", "--is-shallow-repository"],
                shallow).stdout.strip() == "true"
    _record(shallow, [])
    result = _validate(shallow)
    assert result.returncode == 0, result.stdout + result.stderr
    assert "archive-date-vs-commit arm NOT RUN" in result.stdout
    assert "this checkout is SHALLOW" in result.stdout
    assert "undispositioned" not in result.stdout


# --- severity ----------------------------------------------------------------


def test_ENFORCEMENT_WARNING_prints_the_findings_and_leaves_the_verdict(tmp_path):
    root = _repo(tmp_path / "repo")
    _write(root, "2026-08-04-add-thing")
    _commit(root, "2026-08-05T00:30:00+00:00")
    _record(root, [], enforcement="warning")
    result = _validate(root)
    assert result.returncode == 0, result.stdout + result.stderr
    assert "archive-date-vs-commit WARNING (1 finding(s))" in result.stdout
    assert "undispositioned" in result.stdout


def test_STRICT_ARCHIVE_DATES_overrides_the_dial_UPWARD_and_never_DOWNWARD(
        tmp_path):
    root = _repo(tmp_path / "repo")
    _write(root, "2026-08-04-add-thing")
    _commit(root, "2026-08-05T00:30:00+00:00")
    _record(root, [], enforcement="warning")
    strict = _validate(root, "--strict-archive-dates")
    assert strict.returncode == 1, strict.stdout + strict.stderr
    assert "archive-date-vs-commit FAILED (1 finding(s))" in strict.stdout


def test_THE_LIVE_RECORD_IS_ENFORCED_not_merely_warned(tmp_path):
    """The ruling asks for ERROR once every disagreement carries a disposition,
    and the live corpus is green with the twelve, so `error` is what ships."""
    record = sa.load_archive_date_dispositions(sa.dispositions_path(ROOT))
    assert record.enforcement == sa.ENFORCEMENT_ERROR


# --- the second arm does not hide behind the first --------------------------


def test_BOTH_ARCHIVE_DATE_ARMS_REPORT_on_one_run(tmp_path):
    """They read different things — a ledger row against a directory name, and
    a directory name against history — so an early return on the first would
    hide a whole class of finding behind an unrelated one."""
    root = _repo(tmp_path / "repo")
    _write(root, "2026-08-04-add-thing")
    _commit(root, "2026-08-05T00:30:00+00:00")
    ledger = sa.ledger_path(root)
    ledger.parent.mkdir(parents=True, exist_ok=True)
    ledger.write_text(
        "schema_version: 1\nkind: sequenced_after_corpus_ledger\nrows:\n"
        '  add-thing: {state: archived, class: sole, declares: absent, '
        'prose: false, moved_by: "#1", moved_on: "2026-08-01"}\n',
        encoding="utf-8")
    _record(root, [])
    result = _validate(root)
    assert result.returncode == 1, result.stdout + result.stderr
    assert "archive-date contradiction: add-thing" in result.stdout
    assert "archive-date-vs-commit: 2026-08-04-add-thing" in result.stdout


def test_CANNOT_RUN_WINS_OVER_the_first_arms_FAILURE(tmp_path):
    """"The run could not do its job" and "the corpus disagrees" want different
    repairs, and the first is the one to fix before the second means anything."""
    root = _repo(tmp_path / "repo")
    _write(root, "2026-08-04-add-thing")
    _commit(root, "2026-08-05T00:30:00+00:00")
    ledger = sa.ledger_path(root)
    ledger.parent.mkdir(parents=True, exist_ok=True)
    ledger.write_text(
        "schema_version: 1\nkind: sequenced_after_corpus_ledger\nrows:\n"
        '  add-thing: {state: archived, class: sole, declares: absent, '
        'prose: false, moved_by: "#1", moved_on: "2026-08-01"}\n',
        encoding="utf-8")
    result = _validate(root)
    assert result.returncode == 2, result.stdout + result.stderr
    assert "archive-date contradiction: add-thing" in result.stdout
    assert "archive-date-vs-commit arm CANNOT RUN" in result.stdout


# --- the live corpus ---------------------------------------------------------


def test_THE_BATCH_WALK_AGREES_WITH_A_PER_DIRECTORY_LOG_on_every_DISPOSITION():
    """The batch walk is an optimisation (83ms against 9.3s for 144
    per-directory `git log` calls), and an optimisation that attributed a
    directory to the wrong commit would make every sha in the record a
    fiction. Each dispositioned directory is therefore re-derived by the
    INDEPENDENT method the issue measured with."""
    record = sa.load_archive_date_dispositions(sa.dispositions_path(ROOT))
    added = sa.adding_commits(ROOT)
    for name in record.order:
        out = subprocess.run(
            ["git", "-C", str(ROOT), "log", "--diff-filter=A", "--reverse",
             "--no-renames", "--format=%H%x09%cI", "--",
             f"openspec/changes/archive/{name}"],
            capture_output=True, text=True, check=True).stdout.strip()
        sha, _, when = out.splitlines()[0].partition("\t")
        import datetime as _dt
        day = _dt.datetime.fromisoformat(when).astimezone(
            _dt.timezone.utc).date().isoformat()
        assert added[name] == (sha, day), name
        entry = record.entries[name]
        assert entry["adding_commit"] == sha, name
        assert entry["commit_date_utc"] == day, name


def test_THE_LIVE_RECORD_DISPOSITIONS_ONLY_REAL_DISAGREEMENTS_and_names_two_facts():
    record = sa.load_archive_date_dispositions(sa.dispositions_path(ROOT))
    added = sa.adding_commits(ROOT)
    assert sa.archive_commit_problems(ROOT, added, record) == []
    for name in record.order:
        entry = record.entries[name]
        directory = (ROOT / "openspec" / "changes" / "archive" / name)
        assert directory.is_dir(), name
        assert entry["directory_date"] == name[:10], name
        assert entry["commit_date_utc"] != entry["directory_date"], name
        assert entry["ruled_by"] == RULED, name
        assert entry["cited_to"] == CITED, name
    facts = {record.entries[name]["fact"] for name in record.order}
    assert facts == {
        "named by a local clock one day behind UTC; #780's defect, unnoticed",
        "repository initial import, not an archive act"}
    imported = [n for n in record.order
                if record.entries[n]["fact"].startswith("repository initial")]
    assert len(imported) == 2 and len(record.order) == 12
    # The ten are EXACTLY ONE DAY EARLY — the local-clock shape, not a range.
    import datetime as _dt
    for name in record.order:
        if name in imported:
            continue
        entry = record.entries[name]
        assert (_dt.date.fromisoformat(entry["commit_date_utc"])
                - _dt.date.fromisoformat(entry["directory_date"])
                == _dt.timedelta(days=1)), name


def test_THE_LIVE_PLAIN_RUN_IS_GREEN_WITH_ZERO_UNDISPOSITIONED():
    result = _validate(ROOT)
    assert result.returncode == 0, result.stdout + result.stderr
    assert "archive-date-vs-commit agreement passed" in result.stdout
    assert "12 disposition(s) in force, enforcement error" in result.stdout
    assert "undispositioned" not in result.stdout


def test_NO_GIT_ON_PATH_is_NOT_RUN_rather_than_a_TRACEBACK(tmp_path,
                                                           monkeypatch):
    """The plain run did not shell out to git before this arm — every other git
    caller in the module sits behind `--archive-gate`, which an operator asks
    for. So a machine without git would have gone from a working validator to a
    `FileNotFoundError` out of the middle of a corpus check."""
    import os
    root = _repo(tmp_path / "repo")
    _write(root, "2026-08-04-add-thing")
    _commit(root, "2026-08-05T00:30:00+00:00")
    _record(root, [])
    empty = tmp_path / "no-git-here"
    empty.mkdir()
    env = dict(os.environ, PATH=str(empty))
    result = subprocess.run([sys.executable, str(VALIDATOR), str(root)],
                            capture_output=True, text=True, env=env)
    assert result.returncode == 0, result.stdout + result.stderr
    assert "archive-date-vs-commit arm NOT RUN" in result.stdout
    assert "git could not be run" in result.stdout
    assert "Traceback" not in result.stderr


# --- git FAILING is not the same fact as a checkout that declines -----------
#
# Codex P2 on PR #820: `adding_commits` raised ONE error class for "this
# checkout is not one I serve" and for "git just failed", and the CLI mapped
# both to NOT RUN — so a partial clone with objects unavailable would leave the
# run GREEN with a gate the record asks for at `error` silently off. The split
# is now a TYPE (`ArchiveHistoryUnavailable`), and these two assert the halves.


def _git_shim(tmp_path: Path, failing_arg: str) -> Path:
    """A directory holding a `git` that delegates to the real one EXCEPT when
    `failing_arg` is among its arguments, where it fails the way git fails."""
    import shutil
    real = shutil.which("git")
    assert real, "the real git is needed to build the shim"
    shim_dir = tmp_path / f"shim-{failing_arg.strip('-')}"
    shim_dir.mkdir()
    shim = shim_dir / "git"
    shim.write_text(
        "#!/bin/sh\n"
        "for arg in \"$@\"; do\n"
        f"  if [ \"$arg\" = \"{failing_arg}\" ]; then\n"
        "    echo 'fatal: could not read object store' >&2\n"
        "    exit 128\n"
        "  fi\n"
        "done\n"
        f"exec {real} \"$@\"\n", encoding="utf-8")
    shim.chmod(0o755)
    return shim_dir


def test_a_FAILING_HISTORY_WALK_is_CANNOT_RUN_not_a_silent_pass(tmp_path):
    """The gate must not report green because the walk it is built on did not
    happen. The checkout passed the work-tree and shallow probes and then git
    failed — that is git failing, not a context this arm declines to serve."""
    import os
    root = _repo(tmp_path / "repo")
    _write(root, "2026-08-04-add-thing")
    _commit(root, "2026-08-05T00:30:00+00:00")
    _record(root, [])
    env = dict(os.environ,
               PATH=f"{_git_shim(tmp_path, 'log')}{os.pathsep}{os.environ['PATH']}")
    result = subprocess.run([sys.executable, str(VALIDATOR), str(root)],
                            capture_output=True, text=True, env=env)
    assert result.returncode == 2, result.stdout + result.stderr
    assert "archive-date-vs-commit arm CANNOT RUN" in result.stdout
    assert "the archive history walk failed in a checkout that passed the" \
        in result.stdout
    # Specifically NOT this arm's decline line — the LEDGER arm legitimately
    # prints its own "NOT RUN" here, there being no ledger in the fixture.
    assert "archive-date-vs-commit arm NOT RUN" not in result.stdout
    assert "Traceback" not in result.stderr


def test_an_UNANSWERABLE_SHALLOW_PROBE_FAILS_CLOSED(tmp_path):
    """The probe answers the question that decides whether the walk can be
    believed at all; a probe that cannot answer it in a tree that just claimed
    to be a work-tree root is git failing, and skipping would leave the run
    green with the gate off."""
    import os
    root = _repo(tmp_path / "repo")
    _write(root, "2026-08-04-add-thing")
    _commit(root, "2026-08-05T00:30:00+00:00")
    _record(root, [])
    shim = _git_shim(tmp_path, "--is-shallow-repository")
    env = dict(os.environ, PATH=f"{shim}{os.pathsep}{os.environ['PATH']}")
    result = subprocess.run([sys.executable, str(VALIDATOR), str(root)],
                            capture_output=True, text=True, env=env)
    assert result.returncode == 2, result.stdout + result.stderr
    assert "archive-date-vs-commit arm CANNOT RUN" in result.stdout
    assert "could not say whether this checkout is shallow" in result.stdout
    assert "refuses rather than skipping" in result.stdout


def test_THE_DECLINE_CASES_ARE_A_SUBCLASS_so_the_CLI_can_tell_them_apart():
    assert issubclass(sa.ArchiveHistoryUnavailable, sa.SequencedAfterError)


def test_THE_RECORD_NAMES_THE_THREE_CAUSES_and_forbids_only_UNMEASURED_entries():
    """Codex P2 on PR #820. The arm compares a NAME to a COMMIT and cannot say
    WHY they differ; a correct archive whose commit crossed UTC midnight, and a
    change id that arrived carrying its own `YYYY-MM-DD-` prefix (which the
    pinned CLI preserves deliberately), produce the same shape as the defect.
    The header's earlier wording forbade EVERY future entry, which left both of
    those with no lawful repair at `enforcement: error`."""
    text = sa.dispositions_path(ROOT).read_text(encoding="utf-8")
    # The leading `# ` of every comment line is stripped BEFORE flattening, so
    # an assertion may span the file's line wrapping. Flattening the raw text
    # would leave a `#` sitting inside every wrapped phrase.
    flat = " ".join(
        line.lstrip().removeprefix("#").strip()
        for line in text.splitlines()).replace("  ", " ")
    flat = " ".join(flat.split())
    assert "A LOCAL CLOCK BEHIND UTC named the directory" in flat
    assert "THE ARCHIVE ACT AND ITS COMMIT FELL ON DIFFERENT UTC DAYS" in flat
    assert "THE CHANGE ID ARRIVED CARRYING ITS OWN `YYYY-MM-DD-` PREFIX" in flat
    assert "CAUSES 2 AND 3 ARE LAWFUL ENTRIES when they are actually measured" \
        in flat
    assert "What is forbidden is writing either one BEFORE it is measured." \
        in flat
    # …and the doc paragraph carries the same limitation, so a reader of the
    # lifecycle doc is not told the arm judges a cause it cannot judge.
    lifecycle = " ".join((ROOT / "docs" / "document-lifecycle.md")
                         .read_text(encoding="utf-8").split())
    assert ("THE ARM COMPARES A NAME TO A COMMIT AND CANNOT ITSELF SAY WHY THEY "
            "DIFFER") in lifecycle
