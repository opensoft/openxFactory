"""Focused behavioral tests extracted from the NotebookLM sync suite."""

from __future__ import annotations

import contextlib
import io
from unittest.mock import patch

from tests.notebooklm.typed_sync_contracts import load_typed_sync, no_sleep

sync = load_typed_sync()
import json

from tests.notebooklm._lifecycle_test_support import (
    FakeResult,
    FakeRunner,
    FakeState,
    LifecycleFixture,
)


class UploadReadinessTests(LifecycleFixture):
    def _slow_rename_fake(
        self, notebooks: list[dict[str, str]], ready_after: int
    ) -> tuple[FakeRunner, list[tuple[str, ...]], FakeState, dict[str, int]]:
        """A provider whose rename only takes on the `ready_after`-th attempt."""
        calls: list[tuple[str, ...]] = []
        attempts = {"n": 0}
        state: FakeState = {"notebooks": [dict(n) for n in notebooks], "sources": {}}

        def fake(*args: str, parse: bool = True) -> FakeResult:
            del parse
            calls.append(args)
            head = args[:2]
            if head == ("notebook", "list"):
                return list(state["notebooks"])
            if head == ("source", "list"):
                return list(state["sources"].get(args[2], []))
            if head == ("source", "add"):
                nid = args[2]
                sid = f"s{len(state['sources'].setdefault(nid, [])) + 1}"
                state["sources"][nid].append({"id": sid, "title": "xf-sync-abc123.md"})
                return f"Added source: xf-sync-abc123.md\nSource ID: {sid}\n"
            if head == ("source", "rename"):
                attempts["n"] += 1
                if attempts["n"] < ready_after:
                    return ""
                for rows in state["sources"].values():
                    for row in rows:
                        if row.get("id") == args[2]:
                            row["title"] = args[3]
                return ""
            if head in {
                ("alias", "set"),
                ("tag", "add"),
                ("chat", "configure"),
                ("source", "delete"),
            }:
                return ""
            raise AssertionError(f"unexpected nlm call: {args}")

        return (fake, calls, state, attempts)

    def scenario_a_slow_rename_is_polled_until_it_takes(self) -> None:
        fake, calls, state, attempts = self._slow_rename_fake(
            [{"id": "nbX", "title": "T"}], ready_after=4
        )
        with (
            patch.object(sync, "nlm", fake),
            patch.object(sync, "MAX_TEXT_ARG_BYTES", 200),
            patch.object(sync.time, "sleep", no_sleep),
            contextlib.redirect_stdout(io.StringIO()),
        ):
            sync.add_text_source("nbX", "x" * 5000, "[spec] openxFactory: big")
        self.assertEqual(attempts["n"], 4, "should have kept trying")
        titles = [r["title"] for r in state["sources"]["nbX"]]
        self.assertEqual(titles, ["[spec] openxFactory: big"])
        self.assertEqual(len([c for c in calls if c[:2] == ("source", "add")]), 1)

    def scenario_a_rename_that_never_takes_fails_LOUDLY(self) -> None:
        fake, _calls, state, _a = self._slow_rename_fake(
            [{"id": "nbX", "title": "T"}], ready_after=10**6
        )
        with (
            patch.object(sync, "nlm", fake),
            patch.object(sync, "MAX_TEXT_ARG_BYTES", 200),
            patch.object(sync.time, "sleep", no_sleep),
            patch.object(sync, "RENAME_READY_TIMEOUT_S", 9),
            patch.object(sync, "RENAME_POLL_INTERVAL_S", 3),
            contextlib.redirect_stdout(io.StringIO()),
            self.assertRaises(RuntimeError) as caught,
        ):
            sync.add_text_source("nbX", "x" * 5000, "[spec] openxFactory: big")
        msg = str(caught.exception)
        self.assertIn("rename never took", msg)
        self.assertIn("do NOT re-run the sync to fix it", msg)
        self.assertIn("nlm source rename", msg)
        self.assertEqual(
            [r["title"] for r in state["sources"]["nbX"]], ["xf-sync-abc123.md"]
        )

    def scenario_a_rerun_ADOPTS_the_stray_instead_of_adding_a_duplicate(self) -> None:
        text = "x" * 5000
        digest_body = text
        calls: list[tuple[str, ...]] = []
        state = {"sources": {"nbX": [{"id": "stray1", "title": "xf-sync-deadbeef.md"}]}}

        def fake(*args: str, parse: bool = True) -> FakeResult:
            del parse
            calls.append(args)
            head = args[:2]
            if head == ("source", "list"):
                return list(state["sources"].get(args[2], []))
            if head == ("source", "content"):
                return digest_body
            if head == ("source", "rename"):
                for rows in state["sources"].values():
                    for row in rows:
                        if row.get("id") == args[2]:
                            row["title"] = args[3]
                return ""
            raise AssertionError(f"unexpected nlm call: {args}")

        with (
            patch.object(sync, "nlm", fake),
            patch.object(sync, "MAX_TEXT_ARG_BYTES", 200),
            patch.object(sync.time, "sleep", no_sleep),
            contextlib.redirect_stdout(io.StringIO()),
        ):
            sync.add_text_source("nbX", text, "[spec] openxFactory: big")
        self.assertEqual(
            [c for c in calls if c[:2] == ("source", "add")],
            [],
            "the stray was this document; adding again duplicates it",
        )
        self.assertEqual(
            [r["title"] for r in state["sources"]["nbX"]], ["[spec] openxFactory: big"]
        )

    def scenario_a_stray_whose_CONTENT_differs_is_left_alone(self) -> None:
        state = {"sources": {"nbX": [{"id": "other", "title": "xf-sync-deadbeef.md"}]}}
        calls: list[tuple[str, ...]] = []

        def fake(*args: str, parse: bool = True) -> FakeResult:
            del parse
            calls.append(args)
            head = args[:2]
            if head == ("source", "list"):
                return list(state["sources"].get(args[2], []))
            if head == ("source", "content"):
                return "a completely different document"
            if head == ("source", "add"):
                sid = f"s{len(state['sources']['nbX']) + 1}"
                state["sources"]["nbX"].append({"id": sid, "title": "xf-sync-new.md"})
                return f"Source ID: {sid}\n"
            if head == ("source", "rename"):
                for row in state["sources"]["nbX"]:
                    if row.get("id") == args[2]:
                        row["title"] = args[3]
                return ""
            raise AssertionError(f"unexpected nlm call: {args}")

        with (
            patch.object(sync, "nlm", fake),
            patch.object(sync, "MAX_TEXT_ARG_BYTES", 200),
            patch.object(sync.time, "sleep", no_sleep),
            contextlib.redirect_stdout(io.StringIO()),
        ):
            sync.add_text_source("nbX", "x" * 5000, "[spec] openxFactory: big")
        self.assertEqual(
            len([c for c in calls if c[:2] == ("source", "add")]),
            1,
            "an unrelated stray must not be adopted",
        )
        self.assertIn(
            "xf-sync-deadbeef.md", [r["title"] for r in state["sources"]["nbX"]]
        )

    def scenario_a_DUPLICATE_TITLE_does_not_satisfy_the_rename_verifier(self) -> None:
        title = "[spec] openxFactory: big"
        state = {"sources": {"nbX": [{"id": "OLD", "title": title}]}}

        def fake(*args: str, parse: bool = True) -> FakeResult:
            del parse
            head = args[:2]
            if head == ("source", "list"):
                return list(state["sources"]["nbX"])
            if head == ("source", "rename"):
                return ""
            raise AssertionError(f"unexpected nlm call: {args}")

        with (
            patch.object(sync, "nlm", fake),
            patch.object(sync.time, "sleep", no_sleep),
            patch.object(sync, "RENAME_READY_TIMEOUT_S", 9),
            patch.object(sync, "RENAME_POLL_INTERVAL_S", 3),
            contextlib.redirect_stdout(io.StringIO()),
            self.assertRaises(RuntimeError),
        ):
            sync.rename_source_when_ready("nbX", "NEW", title)

    def scenario_adoption_UNWRAPS_a_json_wrapped_body_before_hashing(self) -> None:
        text = "x" * 5000
        state = {"sources": {"nbX": [{"id": "stray1", "title": "xf-sync-deadbeef.md"}]}}
        calls: list[tuple[str, ...]] = []

        def fake(*args: str, parse: bool = True) -> FakeResult:
            del parse
            calls.append(args)
            head = args[:2]
            if head == ("source", "list"):
                return list(state["sources"]["nbX"])
            if head == ("source", "content"):
                return json.dumps({"value": {"content": text}})
            if head == ("source", "rename"):
                for row in state["sources"]["nbX"]:
                    if row.get("id") == args[2]:
                        row["title"] = args[3]
                return ""
            raise AssertionError(f"unexpected nlm call: {args}")

        with (
            patch.object(sync, "nlm", fake),
            patch.object(sync, "MAX_TEXT_ARG_BYTES", 200),
            patch.object(sync.time, "sleep", no_sleep),
            contextlib.redirect_stdout(io.StringIO()),
        ):
            sync.add_text_source("nbX", text, "[spec] openxFactory: big")
        self.assertEqual(
            [c for c in calls if c[:2] == ("source", "add")],
            [],
            "the wrapped stray matched; adding again duplicates it",
        )
        self.assertEqual(
            [r["title"] for r in state["sources"]["nbX"]], ["[spec] openxFactory: big"]
        )

    def scenario_the_content_digest_is_one_mechanism_for_both_sides(self) -> None:
        text = "hello body"
        self.assertEqual(
            sync.content_digest(text),
            sync.content_digest(json.dumps({"value": {"content": text}})),
        )
        self.assertEqual(
            sync.content_digest(text),
            sync.content_digest(json.dumps({"content": text})),
        )
        self.assertNotEqual(
            sync.content_digest(text), sync.content_digest("a different body")
        )
