"""Focused behavioral tests extracted from the NotebookLM sync suite."""

from __future__ import annotations

import contextlib
import io
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Protocol, TypedDict
from unittest.mock import patch

from tests.notebooklm._sync_world_support import HarnessFailure
from tests.notebooklm.typed_sync_contracts import (
    load_typed_sync,
    no_sleep,
)


class _FakeState(TypedDict):
    notebooks: list[dict[str, str]]
    sources: dict[str, list[dict[str, str]]]


_FakeResult = str | list[dict[str, str]]


class _Runner(Protocol):
    def __call__(self, *args: str, parse: bool = True) -> _FakeResult: ...


sync = load_typed_sync()


class SplitIdeationBookTests(unittest.TestCase):
    """split-ideation-book-per-repo: per-repo routing, seeds-never-create,
    title resolution with alias re-registration, apply-gated lazy creation,
    and the capacity guard's occupancy math. All against a stubbed nlm —
    nothing here may touch the real CLI (FR-043)."""

    def _fake(
        self,
        notebooks: list[dict[str, str]],
        sources: dict[str, list[dict[str, str]]] | None = None,
        create_ok: bool = True,
        rename_ok: bool = True,
    ) -> tuple[_Runner, list[tuple[str, ...]], _FakeState]:
        calls: list[tuple[str, ...]] = []
        state: _FakeState = {
            "notebooks": [dict(notebook) for notebook in notebooks],
            "sources": {
                key: [dict(source) for source in values]
                for key, values in (sources or {}).items()
            },
        }

        def fake(*args: str, parse: bool = True) -> _FakeResult:
            del parse
            calls.append(args)
            head = args[:2]
            if head == ("notebook", "list"):
                return list(state["notebooks"])
            if head == ("notebook", "create"):
                if not create_ok:
                    raise HarnessFailure("notebook quota exhausted")
                nb = {"id": f"nb{len(state['notebooks']) + 1}", "title": args[2]}
                state["notebooks"].append(nb)
                _ = state["sources"].setdefault(nb["id"], [])
                return ""
            if head in {("alias", "set"), ("tag", "add"), ("chat", "configure"),
                        ("source", "delete")}:
                return ""
            if head == ("source", "rename"):
                if rename_ok:
                    for rows in state["sources"].values():
                        for row in rows:
                            if row["id"] == args[2]:
                                row["title"] = args[3]
                return ""
            if head == ("source", "list"):
                return list(state["sources"].get(args[2], []))
            if head == ("source", "add"):
                nid = args[2]
                sid = f"s{len(state['sources'].setdefault(nid, [])) + 1}"
                if "--file" in args:
                    # the CLI titles a --file source by FILENAME and echoes the id
                    state["sources"][nid].append({"id": sid, "title": "upload.md"})
                    return f"Added source: upload.md\nSource ID: {sid}\n"
                state["sources"][nid].append({"id": sid, "title": args[6]})
                return ""
            raise AssertionError(f"unexpected nlm call: {args}")

        return fake, calls, state

    @staticmethod
    def _world(root: Path, brainstorms: int = 1) -> None:
        (root / "openxFactory/examples").mkdir(parents=True, exist_ok=True)
        _ = (root / "openxFactory/examples/lifecycle-notebook-workspaces.yaml").write_text(
            "workspaces:\n", encoding="utf-8"
        )
        for g in sync.GROUNDING:
            p = root / g
            p.parent.mkdir(parents=True, exist_ok=True)
            _ = p.write_text("# Grounding\n", encoding="utf-8")
        base = root / "openxFactory/ideation/brainstorm"
        base.mkdir(parents=True, exist_ok=True)
        for i in range(brainstorms):
            _ = (base / f"idea-{i:02d}.md").write_text(
                f"# Idea {i}\n\nStatus: brainstorm\n", encoding="utf-8")

    def test_seeds_never_create_a_book(self):
        with TemporaryDirectory() as td:
            root = Path(td)
            (root / "openxFactory/docs").mkdir(parents=True)
            _ = (root / "openxFactory/docs/x.md").write_text(
                "# X\n\nStatus: draft\n", encoding="utf-8")
            desired, _specs = sync.scan(root)
            # grounding/charter seeding must not conjure an ideation book for
            # a repo with zero brainstorm/staged documents
            self.assertNotIn("ideation-openxfactory", desired)
            self.assertIn("drafts", desired)

    def test_dry_run_reports_pending_creation_and_mutates_nothing(self):
        with TemporaryDirectory() as td:
            root = Path(td)
            self._world(root)
            desired, specs = sync.scan(root)
            spec = specs["ideation-openxfactory"]
            fake, calls, _state = self._fake([])
            out = io.StringIO()
            with patch.object(sync, "nlm", fake), contextlib.redirect_stdout(out):
                ok, over = sync.sync_book(root, spec, desired[spec.key], {}, False)
            self.assertTrue(ok)
            self.assertFalse(over)
            self.assertIn("CREATE", out.getvalue())
            self.assertNotIn(("notebook", "create"), [c[:2] for c in calls])
            # the pending adds stay visible drift for doc-health
            self.assertIn("ADD", out.getvalue())

    def test_apply_creates_seeds_and_writes_the_workspace_record(self):
        with TemporaryDirectory() as td:
            root = Path(td)
            self._world(root)
            desired, specs = sync.scan(root)
            spec = specs["ideation-openxfactory"]
            fake, calls, state = self._fake([])
            out = io.StringIO()
            with patch.object(sync, "nlm", fake), \
                    patch.object(sync.time, "sleep", no_sleep), \
                    contextlib.redirect_stdout(out):
                ok, over = sync.sync_book(root, spec, desired[spec.key], {}, True)
            self.assertTrue(ok)
            self.assertFalse(over)
            heads = [c[:2] for c in calls]
            for required in (("notebook", "create"), ("alias", "set"),
                             ("tag", "add"), ("chat", "configure")):
                self.assertIn(required, heads)
            record = (
                root
                / "openxFactory/examples/lifecycle-notebook-workspaces.yaml"
            ).read_text()
            self.assertIn("workspace-xfactory-lifecycle-ideation-openxfactory",
                          record)
            self.assertIn(state["notebooks"][0]["id"], record)

    def test_missing_alias_resolves_by_title_and_reregisters(self):
        with TemporaryDirectory() as td:
            root = Path(td)
            self._world(root)
            desired, specs = sync.scan(root)
            spec = specs["ideation-openxfactory"]
            fake, calls, _state = self._fake([{"id": "nbX", "title": spec.title}])
            with patch.object(sync, "nlm", fake), \
                    patch.object(sync.time, "sleep", no_sleep), \
                    contextlib.redirect_stdout(io.StringIO()):
                _ = sync.sync_book(root, spec, desired[spec.key], {}, True)
            self.assertIn(("alias", "set", spec.alias, "nbX"), calls)
            self.assertNotIn(("notebook", "create"), [c[:2] for c in calls])
            adds = [c for c in calls if c[:2] == ("source", "add")]
            self.assertTrue(adds)
            # addressed by notebook id, never by alias
            self.assertTrue(all(c[2] == "nbX" for c in adds))

    def test_over_cap_projects_the_prefix_and_reports_the_exact_excess(self):
        with TemporaryDirectory() as td:
            root = Path(td)
            self._world(root, brainstorms=7)   # 7 members + 3 grounding = 10
            desired, specs = sync.scan(root)
            spec = specs["ideation-openxfactory"]
            unmanaged = [{"id": "hand1", "title": "my hand-added PDF"}]
            fake, calls, _state = self._fake(
                [{"id": "nbX", "title": spec.title}], sources={"nbX": unmanaged})
            out = io.StringIO()
            with patch.object(sync, "NOTEBOOK_SOURCE_CAP", 8), \
                    patch.object(sync, "nlm", fake), \
                    patch.object(sync.time, "sleep", no_sleep), \
                    contextlib.redirect_stdout(out):
                _ok, over = sync.sync_book(root, spec, desired[spec.key], {}, True)
            text = out.getvalue()
            self.assertTrue(over)
            # occupancy 10 members + 1 charter + 1 unmanaged = 12 over cap 8:
            # in-cap prefix is 8 - 1 charter - 1 unmanaged = 6 members
            self.assertEqual(text.count("EXCESS"), 4)
            adds = [c for c in calls if c[:2] == ("source", "add")
                    and c[6] != sync.CHARTER_TITLE]
            self.assertEqual(len(adds), 6)

    def test_oversized_source_rides_a_file_and_is_renamed_to_its_title(self):
        # Linux MAX_ARG_STRLEN killed the canon book live 2026-08-10: a doc
        # too large for one argv string must upload as a file and then be
        # renamed to the contract title (--title is ignored on --file).
        with TemporaryDirectory() as td:
            root = Path(td)
            self._world(root)
            big = root / "openxFactory/ideation/brainstorm/huge.md"
            _ = big.write_text(
                "# Huge\n\nStatus: brainstorm\n" + "x" * 500, encoding="utf-8"
            )
            desired, specs = sync.scan(root)
            spec = specs["ideation-openxfactory"]
            fake, calls, _state = self._fake([{"id": "nbX", "title": spec.title}])
            with patch.object(sync, "MAX_TEXT_ARG_BYTES", 200), \
                    patch.object(sync, "nlm", fake), \
                    contextlib.redirect_stdout(io.StringIO()):
                ok, _over = sync.sync_book(root, spec, desired[spec.key], {}, True)
            self.assertTrue(ok)
            file_adds = [c for c in calls
                         if c[:2] == ("source", "add") and "--file" in c]
            renames = [c for c in calls if c[:2] == ("source", "rename")]
            self.assertEqual(len(file_adds), 1)
            self.assertIn("--wait", file_adds[0])
            self.assertEqual(len(renames), 1)
            self.assertEqual(renames[0][3],
                             "[brainstorm] openxFactory: huge")
            # the small docs still ride --text
            text_adds = [c for c in calls
                         if c[:2] == ("source", "add") and "--text" in c]
            self.assertTrue(text_adds)

    def test_oversized_source_refuses_a_silent_rename_failure(self):
        with TemporaryDirectory() as td:
            root = Path(td)
            self._world(root)
            big = root / "openxFactory/ideation/brainstorm/huge.md"
            _ = big.write_text(
                "# Huge\n\nStatus: brainstorm\n" + "x" * 500, encoding="utf-8"
            )
            desired, specs = sync.scan(root)
            spec = specs["ideation-openxfactory"]
            fake, _calls, _state = self._fake(
                [{"id": "nbX", "title": spec.title}], rename_ok=False)
            with patch.object(sync, "MAX_TEXT_ARG_BYTES", 200), \
                    patch.object(sync, "nlm", fake), \
                    contextlib.redirect_stdout(io.StringIO()), \
                    self.assertRaisesRegex(RuntimeError, "rename was not visible"):
                _ = sync.sync_book(root, spec, desired[spec.key], {}, True)

    def test_low_headroom_warns_and_names_the_owed_delta(self):
        with TemporaryDirectory() as td:
            root = Path(td)
            self._world(root, brainstorms=7)   # 10 members + charter = 11
            desired, specs = sync.scan(root)
            spec = specs["ideation-openxfactory"]
            fake, _calls, _state = self._fake([{"id": "nbX", "title": spec.title}])
            out = io.StringIO()
            with patch.object(sync, "NOTEBOOK_SOURCE_CAP", 20), \
                    patch.object(sync, "nlm", fake), \
                    contextlib.redirect_stdout(out):
                _ok, over = sync.sync_book(root, spec, desired[spec.key], {}, False)
            text = out.getvalue()
            self.assertFalse(over)
            self.assertIn("WARN headroom", text)
            self.assertIn("OpenSpec delta", text)
