"""Focused behavioral tests extracted from the NotebookLM sync suite."""

from __future__ import annotations

import unittest
from pathlib import Path
from typing import Protocol, TypedDict, override
from unittest.mock import patch

from tests.notebooklm._sync_world_support import HarnessFailure
from tests.notebooklm.typed_sync_contracts import load_typed_sync, no_sleep


class FakeState(TypedDict):
    notebooks: list[dict[str, str]]
    sources: dict[str, list[dict[str, str]]]


FakeResult = str | list[dict[str, str]]


class FakeRunner(Protocol):
    def __call__(self, *args: str, parse: bool = True) -> FakeResult: ...


sync = load_typed_sync()


class LifecycleFixture(unittest.TestCase):
    @override
    def setUp(self) -> None:
        timing = patch.object(sync.time, "sleep", no_sleep)
        _ = timing.start()
        self.addCleanup(timing.stop)

    def _fake(
        self,
        notebooks: list[dict[str, str]],
        sources: dict[str, list[dict[str, str]]] | None = None,
        create_ok: bool = True,
        rename_ok: bool = True,
    ) -> tuple[FakeRunner, list[tuple[str, ...]], FakeState]:
        calls: list[tuple[str, ...]] = []
        state: FakeState = {
            "notebooks": [dict(notebook) for notebook in notebooks],
            "sources": {
                key: [dict(source) for source in values]
                for key, values in (sources or {}).items()
            },
        }

        def fake(*args: str, parse: bool = True) -> FakeResult:
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
            if head in {
                ("alias", "set"),
                ("tag", "add"),
                ("chat", "configure"),
                ("source", "delete"),
            }:
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
                    state["sources"][nid].append({"id": sid, "title": "upload.md"})
                    return f"Added source: upload.md\nSource ID: {sid}\n"
                state["sources"][nid].append({"id": sid, "title": args[6]})
                return ""
            raise AssertionError(f"unexpected nlm call: {args}")

        return (fake, calls, state)

    @staticmethod
    def _world(root: Path, brainstorms: int = 1) -> None:
        (root / "openxFactory/examples").mkdir(parents=True, exist_ok=True)
        _ = (
            root / "openxFactory/examples/lifecycle-notebook-workspaces.yaml"
        ).write_text("workspaces:\n", encoding="utf-8")
        for g in sync.GROUNDING:
            p = root / g
            p.parent.mkdir(parents=True, exist_ok=True)
            _ = p.write_text("# Grounding\n", encoding="utf-8")
        base = root / "openxFactory/ideation/brainstorm"
        base.mkdir(parents=True, exist_ok=True)
        for i in range(brainstorms):
            _ = (base / f"idea-{i:02d}.md").write_text(
                f"# Idea {i}\n\nStatus: brainstorm\n", encoding="utf-8"
            )
