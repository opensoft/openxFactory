"""Focused behavioral tests extracted from the NotebookLM sync suite."""

from __future__ import annotations

import contextlib
import io
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from tests.notebooklm.typed_sync_contracts import load_typed_sync, no_sleep

sync = load_typed_sync()
from tests.notebooklm._lifecycle_test_support import LifecycleFixture


class SplitIdeationBookTests(LifecycleFixture):
    def scenario_seeds_never_create_a_book(self) -> None:
        with TemporaryDirectory() as td:
            root = Path(td)
            (root / "openxFactory/docs").mkdir(parents=True)
            _ = (root / "openxFactory/docs/x.md").write_text(
                "# X\n\nStatus: draft\n", encoding="utf-8"
            )
            desired, _specs = sync.scan(root)
            self.assertNotIn("ideation-openxfactory", desired)
            self.assertIn("drafts", desired)

    def scenario_dry_run_reports_pending_creation_and_mutates_nothing(self) -> None:
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
            self.assertIn("ADD", out.getvalue())

    def scenario_apply_creates_seeds_and_writes_the_workspace_record(self) -> None:
        with TemporaryDirectory() as td:
            root = Path(td)
            self._world(root)
            desired, specs = sync.scan(root)
            spec = specs["ideation-openxfactory"]
            fake, calls, state = self._fake([])
            out = io.StringIO()
            with (
                patch.object(sync, "nlm", fake),
                patch.object(sync.time, "sleep", no_sleep),
                contextlib.redirect_stdout(out),
            ):
                ok, over = sync.sync_book(root, spec, desired[spec.key], {}, True)
            self.assertTrue(ok)
            self.assertFalse(over)
            heads = [c[:2] for c in calls]
            for required in (
                ("notebook", "create"),
                ("alias", "set"),
                ("tag", "add"),
                ("chat", "configure"),
            ):
                self.assertIn(required, heads)
            record = (
                root / "openxFactory/examples/lifecycle-notebook-workspaces.yaml"
            ).read_text()
            self.assertIn("workspace-xfactory-lifecycle-ideation-openxfactory", record)
            self.assertIn(state["notebooks"][0]["id"], record)

    def scenario_missing_alias_resolves_by_title_and_reregisters(self) -> None:
        with TemporaryDirectory() as td:
            root = Path(td)
            self._world(root)
            desired, specs = sync.scan(root)
            spec = specs["ideation-openxfactory"]
            fake, calls, _state = self._fake([{"id": "nbX", "title": spec.title}])
            with (
                patch.object(sync, "nlm", fake),
                patch.object(sync.time, "sleep", no_sleep),
                contextlib.redirect_stdout(io.StringIO()),
            ):
                _ = sync.sync_book(root, spec, desired[spec.key], {}, True)
            self.assertIn(("alias", "set", spec.alias, "nbX"), calls)
            self.assertNotIn(("notebook", "create"), [c[:2] for c in calls])
            adds = [c for c in calls if c[:2] == ("source", "add")]
            self.assertTrue(adds)
            self.assertTrue(all(c[2] == "nbX" for c in adds))

    def scenario_over_cap_projects_the_prefix_and_reports_the_exact_excess(self) -> None:
        with TemporaryDirectory() as td:
            root = Path(td)
            self._world(root, brainstorms=7)
            desired, specs = sync.scan(root)
            spec = specs["ideation-openxfactory"]
            unmanaged = [{"id": "hand1", "title": "my hand-added PDF"}]
            fake, calls, _state = self._fake(
                [{"id": "nbX", "title": spec.title}], sources={"nbX": unmanaged}
            )
            out = io.StringIO()
            with (
                patch.object(sync, "NOTEBOOK_SOURCE_CAP", 8),
                patch.object(sync, "nlm", fake),
                patch.object(sync.time, "sleep", no_sleep),
                contextlib.redirect_stdout(out),
            ):
                _ok, over = sync.sync_book(root, spec, desired[spec.key], {}, True)
            text = out.getvalue()
            self.assertTrue(over)
            self.assertEqual(text.count("EXCESS"), 4)
            adds = [
                c
                for c in calls
                if c[:2] == ("source", "add") and c[6] != sync.CHARTER_TITLE
            ]
            self.assertEqual(len(adds), 6)

    def scenario_oversized_source_rides_a_file_and_is_renamed_to_its_title(self) -> None:
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
            with (
                patch.object(sync, "MAX_TEXT_ARG_BYTES", 200),
                patch.object(sync, "nlm", fake),
                contextlib.redirect_stdout(io.StringIO()),
            ):
                ok, _over = sync.sync_book(root, spec, desired[spec.key], {}, True)
            self.assertTrue(ok)
            file_adds = [
                c for c in calls if c[:2] == ("source", "add") and "--file" in c
            ]
            renames = [c for c in calls if c[:2] == ("source", "rename")]
            self.assertEqual(len(file_adds), 1)
            self.assertNotIn("--wait", file_adds[0])
            self.assertEqual(len(renames), 1)
            self.assertEqual(renames[0][3], "[brainstorm] openxFactory: huge")
            text_adds = [
                c for c in calls if c[:2] == ("source", "add") and "--text" in c
            ]
            self.assertTrue(text_adds)

    def scenario_oversized_source_refuses_a_silent_rename_failure(self) -> None:
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
                [{"id": "nbX", "title": spec.title}], rename_ok=False
            )
            with (
                patch.object(sync, "MAX_TEXT_ARG_BYTES", 200),
                patch.object(sync, "nlm", fake),
                contextlib.redirect_stdout(io.StringIO()),
                self.assertRaisesRegex(RuntimeError, "rename never took"),
            ):
                _ = sync.sync_book(root, spec, desired[spec.key], {}, True)

    def scenario_low_headroom_warns_and_names_the_owed_delta(self) -> None:
        with TemporaryDirectory() as td:
            root = Path(td)
            self._world(root, brainstorms=7)
            desired, specs = sync.scan(root)
            spec = specs["ideation-openxfactory"]
            fake, _calls, _state = self._fake([{"id": "nbX", "title": spec.title}])
            out = io.StringIO()
            with (
                patch.object(sync, "NOTEBOOK_SOURCE_CAP", 20),
                patch.object(sync, "nlm", fake),
                contextlib.redirect_stdout(out),
            ):
                _ok, over = sync.sync_book(root, spec, desired[spec.key], {}, False)
            text = out.getvalue()
            self.assertFalse(over)
            self.assertIn("WARN headroom", text)
            self.assertIn("OpenSpec delta", text)
