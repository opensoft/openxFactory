"""A branch session's worktree never reaches a lifecycle book: openxFactory's
NotebookLM sync keeps the worktree container out of its scan (FR-005, FR-039;
research R7). Moved here under R1Q2 (a), on F11.1's `HOST_TESTS` surface.

MOVED HERE by plan 034 T035 (opensoft/openDox-code#51, landed `80acead1`).
The cases left `tests/test_session_harness.py` at openDox-code `68be484a`,
whose module failed to COLLECT there: it loaded openxFactory's
`scripts/sync-notebooklm-books.py` at import time (`:37-45`), and openDox-code
carries no such script. The script is this repository's, so the cases run
here, against it, loaded by spec under this file's own module name exactly as
the source module did.

Two of T035's three session cases are here, verbatim:
`test_session_worktrees_never_reach_a_lifecycle_book` (`:279-329`) and
`test_pinned_factory_paths_never_admits_a_worktree_container` (`:332-347`).
Both build their workspace under `tmp_path`.

The third, `test_worktree_container_is_gitignored_in_the_aggregation_repo`
(`:248-260`, with `find_aggregation_root` at `:229-238`), is NOT here. It
reads the xFactory AGGREGATION checkout's ignore file, found by a parent walk,
and skips where there is none. In openxFactory's CI the walk finds none, so the
case would skip in the required gate: `pytest-suite` pins
`EXPECT_SKIPPED: "6"` over `tests/`. A destination for it is a question for
the holder; T047's PR names it.

WHY `tests/domain_profile/`, AND NOT THE PROPOSED `tests/ideation-dashboard/`
PATH. `tests/ideation-dashboard/` is inside the carve surface
(`docs/opendox-carve-manifest.yaml` `moved_paths:`), where
`scripts/validate-carve-manifest.py` refuses a NEW file that no row declares
(`carve-file-undeclared`), and F11.1 forbids adding the row. This directory is
outside that surface, and it is F11.1's own `HOST_TESTS` prefix. The root
`tests/conftest.py` installs the reach and makes the host's one call here too,
so a case that composes the pinned legs composes the same ones it would have
composed there.
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]

# The sync script is a hyphenated path, so it loads by spec like it does in
# tests/notebooklm — under its OWN module name here, so neither suite clobbers
# the other's copy in sys.modules.
_SYNC_SCRIPT = REPO_ROOT / "scripts" / "sync-notebooklm-books.py"
_spec = importlib.util.spec_from_file_location("sync_books_session_scan", _SYNC_SCRIPT)
sync = importlib.util.module_from_spec(_spec)
assert _spec.loader is not None
sys.modules[_spec.name] = sync
_spec.loader.exec_module(sync)


def test_session_worktrees_never_reach_a_lifecycle_book(tmp_path):
    """FR-039 / research R7's second half: the book scan excludes the worktree
    container by name AND anything under a nested `.git`, so a session worktree
    contributes NO source, title, or repository to any of the lifecycle books."""
    doc = "Status: staged\n"
    root = tmp_path / "workspace"
    (root / "openxFactory/ideation/staging/real").mkdir(parents=True)
    (root / "openxFactory/ideation/staging/real/README.md").write_text(
        "# Real\n\n" + doc, encoding="utf-8")
    governed = root / "xFactories/codexFactory"
    (governed / "docs").mkdir(parents=True)
    (governed / ".git").mkdir()
    (governed / "docs/real-doc.md").write_text("# Governed\n\n" + doc, encoding="utf-8")
    (root / ".gitmodules").write_text(
        '[submodule "codexFactory"]\n\tpath = xFactories/codexFactory\n'
        "\turl = https://example.invalid/codexFactory.git\n", encoding="utf-8")

    # a SESSION worktree, exactly where FR-005 puts it
    session = root / "xFactories/codexFactory-worktrees/sessions/draft__demo-topic"
    (session / "ideation/staging/demo-topic").mkdir(parents=True)
    (session / ".git").write_text("gitdir: elsewhere\n", encoding="utf-8")
    (session / "ideation/staging/demo-topic/README.md").write_text(
        "# Session draft\n\n" + doc, encoding="utf-8")

    # `scan` returns (desired, specs) since split-ideation-book-per-repo
    # (2026-08-10) — this test still unpacked the pre-split dict and failed with
    # `'tuple' object has no attribute 'items'` on every run. Repaired here
    # rather than left red; the CLAIM being tested is untouched.
    desired, _specs = sync.scan(root)

    assert desired  # the scan produced books
    for book, entries in desired.items():
        for relpath, title in entries.items():
            assert "-worktrees" not in relpath, (
                f"book {book} projected a worktree source: {relpath}")
            assert "Session draft" not in title
            assert "sessions/" not in relpath
    # the control: the governed and openxFactory documents DID project, so the
    # assertion above is not passing on an empty scan. The ideation family is
    # PER-REPOSITORY since split-ideation-book-per-repo, so the control looks
    # across the whole family instead of one shared `ideation` key — which keeps
    # it proving what it always proved (the scan was not empty) without this
    # test taking a position on how that family is keyed.
    ideation = {relpath
                for key, entries in desired.items()
                if key.startswith(sync.IDEATION_KEY_PREFIX)
                for relpath in entries}
    assert any(r.endswith("openxFactory/ideation/staging/real/README.md")
               for r in ideation), sorted(ideation)
    assert any(r.endswith("xFactories/codexFactory/docs/real-doc.md")
               for r in ideation), sorted(ideation)


def test_pinned_factory_paths_never_admits_a_worktree_container(tmp_path):
    """The other exclusion research R7 names: `pinned_factory_paths` is
    pin-state driven, and its no-.gitmodules fallback drops `*-worktrees` by
    suffix. Both halves asserted, so removing either is a test failure."""
    root = tmp_path / "workspace"
    (root / "xFactories/codexFactory").mkdir(parents=True)
    (root / "xFactories/codexFactory-worktrees/sessions").mkdir(parents=True)

    # fallback (no .gitmodules): suffix heuristic
    assert sync.pinned_factory_paths(root) == ["xFactories/codexFactory"]

    # pin-state (with .gitmodules): only pinned paths
    (root / ".gitmodules").write_text(
        '[submodule "codexFactory"]\n\tpath = xFactories/codexFactory\n'
        "\turl = https://example.invalid/codexFactory.git\n", encoding="utf-8")
    assert sync.pinned_factory_paths(root) == ["xFactories/codexFactory"]
