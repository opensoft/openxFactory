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

import sys
from datetime import date
from pathlib import Path

HERE = Path(__file__).resolve().parent
TESTS_ROOT = HERE.parent
REPO_ROOT = HERE.parent.parent
sys.path.insert(0, str(REPO_ROOT / "scripts"))
sys.path.insert(0, str(TESTS_ROOT))

from doc_health import corpus  # noqa: E402
from doc_health.runner import Context  # noqa: E402
from hermeticity import (  # noqa: E402,F401  (autouse fixture registration)
    hermetic_binary_path,
    hermetic_external_runners,
)

FIXTURES = HERE / "fixtures"
AS_OF = date(2026, 7, 9)


class FakeGit:
    def __init__(self, last_dates=None, line_dates=None, captures=None,
                 pins=None, remotes=None, heads=None, first_dates=None,
                 first_stamps=None, refs=None, ref_trees=None):
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
        self.heads = heads or {}
        # add-promotion-fidelity-check task 4.1 (ruled 2026-08-24): the
        # live-main basis. `refs` answers rev-parse ((repo, ref) -> sha) and
        # `ref_trees` is a whole tree at a ref ((repo, ref) -> {path: body}),
        # which serves BOTH ls-tree and show from one declaration — a shim
        # whose listing and whose bodies could disagree would let a test pass
        # over a reader that never reads what it lists.
        self.refs = refs or {}
        self.ref_trees = ref_trees or {}

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

    def remote_main_sha(self, repo: Path):
        return self.remotes.get(repo.name)

    def head_sha(self, repo: Path):
        return self.heads.get(repo.name)


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
