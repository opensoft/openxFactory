"""The lifecycle sync's workbench orphan-sweep wiring (openxFactory
add-ideation-dashboard task 4.1; the wave-6 note at workbench.orphan_sweep).

Proves, on a fake nlm runner (the real CLI is never invoked):
  * --apply removes `xf-wb-*` notebooks no live manifest binds and keeps
    bound ones;
  * the lifecycle books (xf-ideation-<repo> / xf-drafts / xf-canon) and every other
    non-`xf-wb-*` notebook are NOT sweep candidates — immune by construction;
  * the dry run only prints a plan (no deletions) and its verbs never match
    doc-health's notebook-projection-drift operation pattern;
  * an unavailable nlm and out-of-scope manifests skip gracefully.

unittest-style like the sibling sync tests, so it also collects cleanly under
`tests/hermetic_unittest.py`'s guarded `unittest discover` fallback on this
directory when pytest is absent — retained for any pytest-less host that runs
this tree directly (historically codexFactory's `scripts/validate-docs.sh`,
before the doc-health relocation, adopt-neutral-tooling-home, 2026-08-03; that
script now runs only codexFactory's own test tree)."""

from __future__ import annotations

import contextlib
import importlib.util
import io
import re
import sys
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPT = REPO_ROOT / "scripts" / "sync-notebooklm-books.py"

spec = importlib.util.spec_from_file_location("sync_notebooklm_books_sweep", SCRIPT)
sync = importlib.util.module_from_spec(spec)
assert spec.loader is not None
sys.modules[spec.name] = sync
spec.loader.exec_module(sync)

sys.path.insert(0, str(REPO_ROOT / "scripts"))
# adopt-neutral-tooling-home tranche A: the dashboard runtime (and with it
# `ideation_dashboard.workbench`) arrives with tranche B; until it lands in
# this repo the sweep wiring has nothing to exercise. Probed with find_spec
# because `tests/ideation_dashboard/` forms a same-named NAMESPACE package
# when `tests/` is on sys.path (see tests/hermeticity.py `runner_seams`).
# Self-healing: the skip disappears the moment the real package exists.
if importlib.util.find_spec("ideation_dashboard.workbench") is None:
    raise unittest.SkipTest(
        "ideation_dashboard arrives with adopt-neutral-tooling-home tranche B")
from ideation_dashboard import workbench as wb  # noqa: E402

# doc-health's notebook-projection-drift family counts `[book] ADD|DEL|UPD `
# lines as pending projection operations (scripts/doc_health/families.py).
# Sweep output must never match it.
SYNC_OP = re.compile(r"^\[[^\]]+\]\s+(ADD|DEL|UPD)\s")

LIFECYCLE_BOOKS = [
    {"id": "b1", "title": "xf-ideation"},
    {"id": "b2", "title": "xf-drafts"},
    {"id": "b3", "title": "xf-canon"},
]


class FakeNlm:
    """Records calls; models `notebook list|delete`. Injected as the adapter's
    runner so the real nlm is never reached."""

    def __init__(self, notebooks):
        self.calls = []
        self.notebooks = list(notebooks)

    def __call__(self, *args, parse=True):
        self.calls.append(args)
        if args[:2] == ("notebook", "list"):
            return list(self.notebooks)
        if args[:2] == ("notebook", "delete"):
            nid = args[2]
            self.notebooks = [n for n in self.notebooks if n.get("id") != nid]
            return ""
        return {}

    def deleted_ids(self):
        return [c[2] for c in self.calls if c[:2] == ("notebook", "delete")]


def _boom(*args, **kwargs):
    raise AssertionError("the real nlm runner must never be called in tests")


def _live_manifest(root: Path, name: str, alias: str) -> Path:
    """A live workbench manifest under the v1 scope
    (<root>/openxFactory/ideation/workbench/)."""
    repo = root / "openxFactory"
    boundary_root = repo
    from ideation_dashboard.boundary import OutputBoundary
    w = wb.Workbench.create("openxFactory", name, now="2026-07-14T08:00:00Z")
    w.bind_notebook(alias, now="2026-07-14T08:00:00Z")
    return wb.save(w, OutputBoundary(boundary_root, [wb.WORKBENCH_DIR]))


def _run(root, apply, adapter):
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        sync.workbench_orphan_sweep(root, apply, adapter=adapter)
    return buf.getvalue()


class WorkbenchSweepWiringTests(unittest.TestCase):
    def test_apply_sweeps_orphans_and_keeps_bound(self):
        with TemporaryDirectory() as td:
            root = Path(td)
            _live_manifest(root, "Alpha", "xf-wb-alpha")
            fake = FakeNlm(LIFECYCLE_BOOKS + [
                {"id": "w1", "title": "xf-wb-alpha"},
                {"id": "w2", "title": "xf-wb-orphan"},
            ])
            adapter = wb.NotebookAdapter(fake, available=True)
            out = _run(root, True, adapter)
            self.assertIn("deleted=['xf-wb-orphan']", out)
            self.assertEqual(fake.deleted_ids(), ["w2"])
            titles = sorted(n["title"] for n in fake.notebooks)
            self.assertEqual(
                titles, ["xf-canon", "xf-drafts", "xf-ideation", "xf-wb-alpha"])

    def test_lifecycle_books_are_never_sweep_candidates(self):
        # Zero live manifests: every xf-wb-* is an orphan — yet the three
        # lifecycle books and a plain notebook survive untouched because
        # list_scratch() only ever surfaces xf-wb-* titles.
        with TemporaryDirectory() as td:
            fake = FakeNlm(LIFECYCLE_BOOKS + [
                {"id": "n1", "title": "meeting notes"},
                {"id": "w1", "title": "xf-wb-stale"},
            ])
            adapter = wb.NotebookAdapter(fake, available=True)
            _run(Path(td), True, adapter)
            self.assertEqual(fake.deleted_ids(), ["w1"])
            survivors = sorted(n["title"] for n in fake.notebooks)
            self.assertEqual(
                survivors,
                ["meeting notes", "xf-canon", "xf-drafts", "xf-ideation"])

    def test_book_aliases_are_structurally_outside_the_sweep_prefix(self):
        # The managed lifecycle books can never collide with the scratch
        # prefix that defines sweep candidacy.
        for cfg in sync.BOOKS.values():
            self.assertFalse(cfg["alias"].startswith(wb.NOTEBOOK_PREFIX))

    def test_dry_run_prints_a_plan_and_deletes_nothing(self):
        with TemporaryDirectory() as td:
            root = Path(td)
            _live_manifest(root, "Alpha", "xf-wb-alpha")
            fake = FakeNlm(LIFECYCLE_BOOKS + [
                {"id": "w1", "title": "xf-wb-alpha"},
                {"id": "w2", "title": "xf-wb-orphan"},
            ])
            adapter = wb.NotebookAdapter(fake, available=True)
            out = _run(root, False, adapter)
            self.assertEqual(fake.deleted_ids(), [])
            self.assertIn("KEEP  xf-wb-alpha", out)
            self.assertIn("SWEEP xf-wb-orphan", out)
            # never counted as projection drift by doc-health
            for line in out.splitlines():
                self.assertIsNone(SYNC_OP.match(line), line)

    def test_skips_gracefully_when_nlm_unavailable(self):
        with TemporaryDirectory() as td:
            adapter = wb.NotebookAdapter(_boom, available=False)
            out = _run(Path(td), True, adapter)
            self.assertIn("SKIPPED", out)
            self.assertIn("nlm unavailable", out)

    def test_out_of_scope_manifest_skips_the_sweep(self):
        # A manifest outside the v1 openxFactory scope could bind a notebook
        # the sweep cannot see as live — the sweep must refuse to run.
        with TemporaryDirectory() as td:
            root = Path(td)
            stray = root / "xFactories" / "codexFactory" / "ideation" / "workbench"
            stray.mkdir(parents=True)
            (stray / "stray.workbench.yaml").write_text(
                "kind: ideation-workbench\n", encoding="utf-8")
            fake = FakeNlm([{"id": "w1", "title": "xf-wb-orphan"}])
            adapter = wb.NotebookAdapter(fake, available=True)
            out = _run(root, True, adapter)
            self.assertIn("SKIPPED", out)
            self.assertIn("outside the v1 openxFactory scope", out)
            self.assertEqual(fake.deleted_ids(), [])


if __name__ == "__main__":
    unittest.main()
