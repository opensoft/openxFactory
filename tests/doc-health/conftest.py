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
                 pins=None, remotes=None, heads=None, first_dates=None):
        self.last_dates = last_dates or {}
        self.first_dates = first_dates or {}
        self.line_dates = line_dates or {}
        self.captures = captures or {}
        self.pins = pins
        self.remotes = remotes or {}
        self.heads = heads or {}

    def last_commit_date(self, repo: Path, relpath: str):
        return self.last_dates.get((repo.name, relpath))

    def first_commit_date(self, repo: Path, relpath: str):
        return self.first_dates.get((repo.name, relpath))

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
