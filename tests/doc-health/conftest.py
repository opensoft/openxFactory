"""Test harness for the doc-health suite.

Fixture corpora live in fixtures/<family>/<repo>/... — miniature repo
trees with known violations. FakeGit supplies the git-derived facts
(dates, capture blobs, pins) so tests are hermetic and deterministic.

The STRUCTURAL hermeticity guard (`tests/hermeticity.py`) is registered here as
well as in `tests/conftest.py`, because a targeted `pytest tests/doc-health` run
makes this directory the rootdir and pytest's `confcutdir` then excludes the
suite-wide conftest from collection (FR-043, PR #49 finding 17).
"""

from __future__ import annotations

import os
import sys
from datetime import date
from pathlib import Path
from stat import S_ISDIR, S_ISREG

import pytest

HERE = Path(__file__).resolve().parent
TESTS_ROOT = HERE.parent
REPO_ROOT = HERE.parent.parent
sys.path.insert(0, str(REPO_ROOT / "scripts"))
sys.path.insert(0, str(TESTS_ROOT))

# --------------------------------------------------------------------------
# THE § 5.2 SHED REACH, INSTALLED HERE TOO. Same reason as the hermeticity
# guard above it: a targeted `pytest tests/doc-health` makes this directory the
# rootdir, `confcutdir` excludes `tests/conftest.py`, and this suite reaches
# carved modules — `test_status_reader_real_lines.py` imports `openxdox` and
# `test_sentinel_vocabulary.py` reads a moved file's SOURCE through
# `carved_reach.source()` (Copilot, `PRRT_kwDOTAvnrs6hVRyV`). Idempotent.
# --------------------------------------------------------------------------

from carved_reach import install as install_carved_reach  # noqa: E402

install_carved_reach(tests=True)

from doc_health import corpus  # noqa: E402
from doc_health.runner import Context  # noqa: E402
from hermeticity import (  # noqa: E402,F401  (autouse fixture registration)
    claim_conftest_slot,
    hermetic_binary_path,
    hermetic_external_runners,
)

FIXTURES = HERE / "fixtures"
AS_OF = date(2026, 7, 9)

#: A repository root that DOES NOT EXIST, for the `Context`s a test builds by
#: hand when what is under test is exact header content rather than a fixture
#: tree. Resolved at runtime, never written as an absolute literal: the
#: constitution's § IV forbids a committed file to carry a host-absolute path
#: and names runtime resolution as one of its two sanctioned alternatives
#: (Copilot, PR #890).
#:
#: NON-EXISTENCE IS THE POINT, not an accident. A family given this root may
#: not reach the filesystem at all, so a root that cannot resolve is how that
#: is asserted rather than assumed — which is also why `tmp_path` is the wrong
#: tool for these cases: it exists. ONE definition rather than one per file, so
#: a second copy cannot quietly become a real directory.
NO_SUCH_REPO_ROOT = HERE / "no-such-repo-root"


class FakeGit:
    def __init__(self, last_dates=None, line_dates=None, captures=None,
                 pins=None, remotes=None, heads=None, first_dates=None,
                 first_stamps=None, refs=None, ref_trees=None,
                 blobs=None, modes=None, git_unavailable=False,
                 tag_refs=None, first_parents=None,
                 present_commits=None, fetchable=None):
        self.last_dates = last_dates or {}
        self.first_dates = first_dates or {}
        # add-promotion-fidelity-check: archive-commit order to SECOND
        # resolution, which is what breaks a tie between two packets
        # archived on the same DAY. Absent an entry the shim answers None,
        # exactly as RealGit does when git cannot answer — which is the
        # fallback path the tie-break tests exercise deliberately.
        self.first_stamps = first_stamps or {}
        self.line_dates = line_dates or {}
        self.captures = captures or {}
        self.pins = pins
        self.remotes = remotes or {}
        # add-release-tag-publication-check: (repo, tag) -> (objecttype, sha),
        # and (repo, ref) -> [sha, ...] newest first. A MISSING declaration
        # answers None from both shims — "the refs could not be listed" and
        # "the walk could not be performed" — because that is the state
        # RealGit reports when git cannot answer, and it is the skip path the
        # family's scenarios exercise. An EXPLICIT (None, None) is the other
        # thing entirely: the remote listed no such tag, which is an ANSWER.
        self.tag_refs = tag_refs
        self.first_parents = first_parents
        self.heads = heads or {}
        # add-promotion-fidelity-check task 4.1 (ruled 2026-08-24): the
        # live-main basis. `refs` answers rev-parse ((repo, ref) -> sha) and
        # `ref_trees` is a whole tree at a ref ((repo, ref) -> {path: body}),
        # which serves BOTH ls-tree and show from one declaration — a shim
        # whose listing and whose bodies could disagree would let a test pass
        # over a reader that never reads what it lists.
        self.refs = refs or {}
        self.ref_trees = ref_trees or {}
        # add-release-inventory-drift-check: the release-surface readers.
        # `blobs` is {(repo, path): bytes} and a path ABSENT from it answers
        # None for that path while the CALL succeeds — the distinction the
        # family's taxonomy turns on. `git_unavailable` collapses both readers
        # to None, which is the only way to reach the skip arm.
        self.blobs = blobs or {}
        self.modes = modes or {}
        self.git_unavailable = git_unavailable
        # openxFactory #612: the local object store, and what `origin` would
        # serve if asked for it. Sets rather than dicts because the only
        # question either seam answers is membership.
        self.present_commits = set(present_commits or ())
        self.fetchable = set(fetchable or ())
        self.fetch_calls: list[tuple[str, str, object]] = []

    def last_commit_date(self, repo: Path, relpath: str):
        return self.last_dates.get((repo.name, relpath))

    def first_commit_date(self, repo: Path, relpath: str):
        return self.first_dates.get((repo.name, relpath))

    def first_commit_timestamp(self, repo: Path, relpath: str, ref=None):
        if ref:
            return self.first_stamps.get((repo.name, ref, relpath))
        return self.first_stamps.get((repo.name, relpath))

    def resolve_ref(self, repo: Path, ref: str):
        return self.refs.get((repo.name, ref))

    def ls_tree_paths(self, repo: Path, ref: str, prefix: str):
        tree = self.ref_trees.get((repo.name, ref))
        if tree is None:
            return None
        return sorted(p for p in tree if p.startswith(prefix))

    def show_blob(self, repo: Path, ref: str, relpath: str):
        return (self.ref_trees.get((repo.name, ref)) or {}).get(relpath)

    def line_commit_date(self, repo: Path, relpath: str, line: int):
        return self.line_dates.get((repo.name, relpath, line))

    def capture_blob(self, repo: Path, relpath: str, predicate):
        blob = self.captures.get((repo.name, relpath))
        return blob if blob is not None and predicate(blob) else None

    def gitlink_pins(self, agg_root: Path):
        return self.pins

    def tag_ref(self, repo: Path, name: str):
        if self.tag_refs is None:
            return None
        return self.tag_refs.get((str(repo), name), (None, None))

    def first_parent_shas(self, repo: Path, ref: str, limit: int):
        if self.first_parents is None:
            return None
        shas = self.first_parents.get((str(repo), ref))
        return None if shas is None else list(shas)[:max(1, limit)]

    def remote_main_sha(self, repo: Path):
        return self.remotes.get(repo.name)

    def head_sha(self, repo: Path):
        return self.heads.get(repo.name)

    # openxFactory #612: the object-store seam. `blobs_at` above answers a
    # per-path None for TWO facts — the path is absent at a commit we hold, and
    # the commit is not here at all — so a caller that has to tell them apart
    # asks these instead of guessing. The default is the pessimistic one:
    # NOTHING is present and NOTHING is fetchable, so an existing test that
    # declares no object store still reaches the fail-closed skip it was
    # written for. `fetch_calls` records every attempt, which is how a test
    # proves the fetch was NOT made.
    def commit_present(self, repo: Path, sha: str) -> bool:
        return sha in self.present_commits

    def fetch_commit(self, repo: Path, sha: str, depth=None) -> bool:
        self.fetch_calls.append((repo.name, sha, depth))
        if sha in self.fetchable:
            self.present_commits.add(sha)
            return True
        return False

    # add-release-inventory-drift-check: the release-surface readers.
    #
    # `blobs` is `{(repo, path): bytes}` and a path ABSENT from it answers
    # None for that path while the call itself succeeds — which is exactly the
    # distinction the family's taxonomy turns on (a deleted member is drift; a
    # broken git is a skip). `git_unavailable=True` collapses BOTH readers to
    # None, which is the only way to get the skip arm.

    def blobs_at(self, repo: Path, commit: str, relpaths):
        if self.git_unavailable:
            return None
        return {p: self.blobs.get((repo.name, p)) for p in relpaths}

    def tree_modes(self, repo: Path, commit: str):
        if self.git_unavailable:
            return None
        return {path: mode for (name, path), mode in self.modes.items()
                if name == repo.name}


# --------------------------------------------------------------------------
# PYTHON 3.14's PATHLIB, ON EVERY INTERPRETER (opensoft/openxFactory#1201).
#
# Through 3.13, `Path.exists`/`is_dir`/`is_file`/`is_symlink` raise any
# `OSError` that does not name the node's absence; 3.14 answers False for all
# of them. CI's required suite runs 3.12, so a test that relies on the native
# behaviour proves nothing about 3.14. `pathlib_314` runs a test twice: once
# natively, and once with the four methods replaced by CPython 3.14's own
# bodies (`Lib/pathlib/__init__.py` at python/cpython@c66df4e7, lines 663-707,
# transcribed below). They delegate to `os.path`, whose `genericpath` bodies
# are identical in 3.12, 3.13 and 3.14, so the swap reproduces 3.14 exactly.
# A test under it proves the code under test refuses because it no longer
# asks pathlib, not because this interpreter's pathlib happens to raise.
# --------------------------------------------------------------------------

def _exists_314(self, *, follow_symlinks=True):
    if follow_symlinks:
        return os.path.exists(self)
    return os.path.lexists(self)


def _is_dir_314(self, *, follow_symlinks=True):
    if follow_symlinks:
        return os.path.isdir(self)
    try:
        return S_ISDIR(self.stat(follow_symlinks=follow_symlinks).st_mode)
    except (OSError, ValueError):
        return False


def _is_file_314(self, *, follow_symlinks=True):
    if follow_symlinks:
        return os.path.isfile(self)
    try:
        return S_ISREG(self.stat(follow_symlinks=follow_symlinks).st_mode)
    except (OSError, ValueError):
        return False


def _is_symlink_314(self):
    return os.path.islink(self)


def emulate_pathlib_314(monkeypatch) -> None:
    """Replace `Path`'s four query methods with CPython 3.14's bodies."""
    monkeypatch.setattr(Path, "exists", _exists_314)
    monkeypatch.setattr(Path, "is_dir", _is_dir_314)
    monkeypatch.setattr(Path, "is_file", _is_file_314)
    monkeypatch.setattr(Path, "is_symlink", _is_symlink_314)


@pytest.fixture(params=("native", "cpython-3.14"))
def pathlib_314(request, monkeypatch):
    """Run the test under this interpreter's pathlib, then under 3.14's.
    Yields the model's name."""
    if request.param == "cpython-3.14":
        emulate_pathlib_314(monkeypatch)
    yield request.param


class ProbeDenial:
    """`os.stat` and `os.lstat` of exactly `nodes` raise
    `OSError(err, os.strerror(err), <path>)` while `armed` -- both, because a
    node whose parent denies search can be neither stat-ed nor lstat-ed, and
    because pathlib reaches `os.stat` (`follow_symlinks=False` for its
    `lstat` through 3.13) where the explicit probes reach `os.lstat`.
    Monkeypatched rather than `chmod`-ed: `chmod` denies nothing to root, so
    a mode-based repro would not hold under a root runner. `denied` records
    every call that was refused, so a test can prove the denial was reached.
    """

    def __init__(self, monkeypatch, nodes, err, *, armed=True):
        self.targets = {os.path.normpath(os.fspath(n)) for n in nodes}
        self.err = err
        self.armed = armed
        self.denied = []
        real_stat, real_lstat = os.stat, os.lstat

        def hit(name, path):
            if not (self.armed and isinstance(path, (str, os.PathLike))):
                return False
            path = os.fspath(path)
            if not isinstance(path, str) or \
                    os.path.normpath(path) not in self.targets:
                return False
            self.denied.append((name, path))
            return True

        def denying_stat(path, *args, **kwargs):
            if hit("stat", path):
                raise OSError(err, os.strerror(err), os.fspath(path))
            return real_stat(path, *args, **kwargs)

        def denying_lstat(path, *args, **kwargs):
            if hit("lstat", path):
                raise OSError(err, os.strerror(err), os.fspath(path))
            return real_lstat(path, *args, **kwargs)

        monkeypatch.setattr(os, "stat", denying_stat)
        monkeypatch.setattr(os, "lstat", denying_lstat)


def make_ctx(family: str, git=None, agg_root=None, notebook=lambda: None,
             thresholds=None):
    from doc_health import DEFAULT_THRESHOLDS
    fixture = FIXTURES / family
    repo_paths = {p.name: p for p in sorted(fixture.iterdir()) if p.is_dir()}
    docs, capabilities, change_ids = [], {}, {}
    for name, path in repo_paths.items():
        docs.extend(corpus.load_docs(name, path))
        capabilities[name] = corpus.spec_capabilities(path)
        change_ids[name] = corpus.change_ids(path)
    return Context(
        repo_paths=repo_paths, docs=docs, capabilities=capabilities,
        change_ids=change_ids, git=git or FakeGit(),
        thresholds=thresholds or dict(DEFAULT_THRESHOLDS),
        as_of=AS_OF, agg_root=agg_root, notebook_dryrun=notebook)


# `claim_conftest_slot` re-installs THIS module as the ambient `conftest` for
# nodes under this directory only, so a multi-directory invocation
# (`pytest tests/doc-health tests/ideation-dashboard`) no longer depends on
# argument order — see its docstring in `tests/hermeticity.py` for the
# mechanism, and never add the call to `tests/conftest.py` (issue #305).
claim_conftest_slot(globals())
