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

unittest-style like the sibling sync tests: validate-docs.sh falls back to
`unittest discover` on this directory when pytest is absent."""

from __future__ import annotations

import contextlib
import io
import re
import unittest
from collections.abc import Iterable, Mapping
from pathlib import Path
from tempfile import TemporaryDirectory
from types import ModuleType
from typing import NoReturn, Protocol, final, runtime_checkable
from unittest.mock import patch

from notebooklm_sync.compat_projection import ProjectionFacade
from notebooklm_sync.nlm_client import JsonValue, ProviderResult
from opendox import workbench as wb
from output_boundary import OutputBoundary

from tests.notebooklm._sync_test_support import sync


@runtime_checkable
class WorkbenchSaver(Protocol):
    def save(self, workbench: wb.Workbench, boundary: OutputBoundary) -> Path: ...


class WorkbenchSaveUnavailable(RuntimeError):
    """The optional workbench module does not expose its save interface."""


def _save_workbench(module: ModuleType, workbench: wb.Workbench, boundary: OutputBoundary) -> Path:
    if not isinstance(module, WorkbenchSaver):
        raise WorkbenchSaveUnavailable("workbench save interface unavailable")
    return module.save(workbench, boundary)

# The sweep is exercised against the currently pinned openDox package.
# doc-health's notebook-projection-drift family counts `[book] ADD|DEL|UPD `
# lines as pending projection operations (scripts/doc_health/families.py).
# Sweep output must never match it.
SYNC_OP = re.compile(r"^\[[^\]]+\]\s+(ADD|DEL|UPD)\s")

LIFECYCLE_BOOKS: list[dict[str, str]] = [
    {"id": "b1", "title": "xf-ideation"},
    {"id": "b2", "title": "xf-drafts"},
    {"id": "b3", "title": "xf-canon"},
]


@final
class FakeNlm:
    """Records calls; models `notebook list|delete`. Injected as the adapter's
    runner so the real nlm is never reached."""

    def __init__(self, notebooks: Iterable[Mapping[str, JsonValue]]) -> None:
        self.calls: list[tuple[str, ...]] = []
        self.notebooks: list[dict[str, str]] = [
            {"id": str(row["id"]), "title": str(row["title"])} for row in notebooks
        ]

    def __call__(self, *args: str, parse: bool = True) -> ProviderResult:
        del parse
        self.calls.append(args)
        if args[:2] == ("notebook", "list"):
            rows: list[JsonValue] = [dict(row) for row in self.notebooks]
            return rows
        if args[:2] == ("notebook", "delete"):
            nid = args[2]
            self.notebooks = [n for n in self.notebooks if n.get("id") != nid]
            return ""
        return {}

    def deleted_ids(self) -> list[str]:
        return [c[2] for c in self.calls if c[:2] == ("notebook", "delete")]


def _boom(*args: str, parse: bool = True) -> NoReturn:
    del args, parse
    raise AssertionError("the real nlm runner must never be called in tests")


def _live_manifest(root: Path, name: str, alias: str) -> Path:
    """A live workbench manifest under the v1 scope
    (<root>/openxFactory/ideation/workbench/)."""
    repo = root / "openxFactory"
    boundary_root = repo
    from output_boundary import OutputBoundary

    w = wb.Workbench(
        {
            "schema_version": wb.SCHEMA_VERSION,
            "kind": wb.KIND,
            "repository": "openxFactory",
            "name": name,
            "created": "2026-07-14T08:00:00Z",
            "updated": "2026-07-14T08:00:00Z",
            "members": [],
            "seed": {"kind": wb.SEED_ADHOC},
        }
    )
    _ = w.bind_notebook(alias, now="2026-07-14T08:00:00Z")
    return _save_workbench(wb, w, OutputBoundary(boundary_root, [wb.WORKBENCH_DIR]))


def _run(root: Path, apply: bool, adapter: wb.NotebookAdapter | None) -> str:
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        sync.workbench_orphan_sweep(root, apply, adapter=adapter)
    return buf.getvalue()


class WorkbenchSweepWiringTests(unittest.TestCase):
    def test_apply_sweeps_orphans_and_keeps_bound(self) -> None:
        with TemporaryDirectory() as td:
            root = Path(td)
            _ = _live_manifest(root, "Alpha", "xf-wb-alpha")
            fake = FakeNlm(
                LIFECYCLE_BOOKS
                + [
                    {"id": "w1", "title": "xf-wb-alpha"},
                    {"id": "w2", "title": "xf-wb-orphan"},
                ]
            )
            adapter = wb.NotebookAdapter(fake, available=True)
            out = _run(root, True, adapter)
            self.assertIn("deleted=['xf-wb-orphan']", out)
            self.assertEqual(fake.deleted_ids(), ["w2"])
            titles = sorted(n["title"] for n in fake.notebooks)
            self.assertEqual(
                titles, ["xf-canon", "xf-drafts", "xf-ideation", "xf-wb-alpha"]
            )

    def test_lifecycle_books_are_never_sweep_candidates(self) -> None:
        # Zero live manifests: every xf-wb-* is an orphan — yet the three
        # lifecycle books and a plain notebook survive untouched because
        # list_scratch() only ever surfaces xf-wb-* titles.
        with TemporaryDirectory() as td:
            fake = FakeNlm(
                LIFECYCLE_BOOKS
                + [
                    {"id": "n1", "title": "meeting notes"},
                    {"id": "w1", "title": "xf-wb-stale"},
                ]
            )
            adapter = wb.NotebookAdapter(fake, available=True)
            _ = _run(Path(td), True, adapter)
            self.assertEqual(fake.deleted_ids(), ["w1"])
            survivors = sorted(n["title"] for n in fake.notebooks)
            self.assertEqual(
                survivors, ["meeting notes", "xf-canon", "xf-drafts", "xf-ideation"]
            )

    def test_book_aliases_are_structurally_outside_the_sweep_prefix(self) -> None:
        # The managed lifecycle books can never collide with the scratch
        # prefix that defines sweep candidacy.
        for cfg in sync.BOOKS.values():
            self.assertFalse(cfg["alias"].startswith(wb.NOTEBOOK_PREFIX))

    def test_dry_run_prints_a_plan_and_deletes_nothing(self) -> None:
        with TemporaryDirectory() as td:
            root = Path(td)
            _ = _live_manifest(root, "Alpha", "xf-wb-alpha")
            fake = FakeNlm(
                LIFECYCLE_BOOKS
                + [
                    {"id": "w1", "title": "xf-wb-alpha"},
                    {"id": "w2", "title": "xf-wb-orphan"},
                ]
            )
            adapter = wb.NotebookAdapter(fake, available=True)
            out = _run(root, False, adapter)
            self.assertEqual(fake.deleted_ids(), [])
            self.assertIn("KEEP  xf-wb-alpha", out)
            self.assertIn("SWEEP xf-wb-orphan", out)
            # never counted as projection drift by doc-health
            for line in out.splitlines():
                self.assertIsNone(SYNC_OP.match(line), line)

    def test_skips_gracefully_when_nlm_unavailable(self) -> None:
        with TemporaryDirectory() as td:
            adapter = wb.NotebookAdapter(_boom, available=False)
            out = _run(Path(td), True, adapter)
            self.assertIn("SKIPPED", out)
            self.assertIn("nlm unavailable", out)

    def test_skips_gracefully_when_optional_dashboard_adapter_is_incomplete(
        self,
    ) -> None:
        with TemporaryDirectory() as td:
            incomplete = ModuleType("incomplete_workbench")
            with patch.object(ProjectionFacade, "_workbench", return_value=incomplete):
                out = _run(Path(td), True, adapter=None)
        self.assertIn("SKIPPED", out)
        self.assertIn("unavailable", out)

    def test_out_of_scope_manifest_skips_the_sweep(self) -> None:
        # A manifest outside the v1 openxFactory scope could bind a notebook
        # the sweep cannot see as live — the sweep must refuse to run.
        with TemporaryDirectory() as td:
            root = Path(td)
            stray = root / "xFactories" / "codexFactory" / "ideation" / "workbench"
            stray.mkdir(parents=True)
            _ = (stray / "stray.workbench.yaml").write_text(
                "kind: ideation-workbench\n", encoding="utf-8"
            )
            fake = FakeNlm([{"id": "w1", "title": "xf-wb-orphan"}])
            adapter = wb.NotebookAdapter(fake, available=True)
            out = _run(root, True, adapter)
            self.assertIn("SKIPPED", out)
            self.assertIn("outside the v1 openxFactory scope", out)
            self.assertEqual(fake.deleted_ids(), [])


if __name__ == "__main__":
    _ = unittest.main()
