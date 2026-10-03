from __future__ import annotations

from collections.abc import Callable, Mapping, Sequence
from pathlib import Path
from typing import Protocol

from .corpus import DesiredState
from .models import BookSpec
from .nlm_client import JsonValue, NotebookRow, SourceRow


class BookResolver(Protocol):
    def __call__(
        self,
        root: Path,
        spec: BookSpec,
        apply: bool,
        notebooks: Sequence[NotebookRow | Mapping[str, JsonValue]] | None,
        *,
        bind_alias: bool,
    ) -> tuple[str | None, bool]: ...


def parity_report(
    root: Path,
    *,
    book: str | None,
    notebooks: Sequence[NotebookRow | Mapping[str, JsonValue]] | None,
    scan: Callable[[Path], tuple[DesiredState, dict[str, BookSpec]]],
    list_notebooks: Callable[[], list[NotebookRow]],
    resolve_book: BookResolver,
    list_sources: Callable[[str], list[SourceRow]],
) -> int:
    desired, specs = scan(root)
    if book and book not in desired:
        print(
            f"parity: {book!r} is not a book this scan derives; available: "
            + f"{', '.join(sorted(desired))}"
        )
        return 1
    rows = notebooks if notebooks is not None else list_notebooks()
    derived_union: set[str] = set()
    live_union: set[str] = set()
    mismatched: list[str] = []
    for key, items in sorted(desired.items()):
        if book and key != book:
            continue
        derived = set(items.values())
        derived_union |= derived
        carried: dict[str, list[str]] = {}
        for relative, title in items.items():
            carried.setdefault(title, []).append(relative)
        collapsed = {
            title: sorted(paths) for title, paths in carried.items() if len(paths) > 1
        }
        if collapsed:
            displaced = sum(len(paths) - 1 for paths in collapsed.values())
            print(
                f"[{key}] PARITY FAIL: {len(collapsed)} derived title(s) carry more than one document — {len(items)} documents derive only {len(derived)} titles, so {displaced} cannot hold a source of their own"
            )
            for title, paths in sorted(collapsed.items())[:5]:
                print(f"[{key}]   COLLAPSED {title}")
                for relative in paths:
                    print(f"[{key}]     {relative}")
        notebook_id, _ok = resolve_book(root, specs[key], False, rows, bind_alias=False)
        if notebook_id is None:
            print(
                f"[{key}] PARITY FAIL: no live notebook titled "
                + f"{specs[key].title!r} ({len(derived)} derived members)"
            )
            mismatched.append(key)
            continue
        live = {
            source.title
            for source in list_sources(notebook_id)
            if source.title.startswith("[")
        }
        live_union |= live
        missing = sorted(derived - live)
        extra = sorted(live - derived)
        if not missing and not extra and not collapsed:
            print(
                f"[{key}] PARITY OK: {len(items)} documents in {len(derived)} titles match"
            )
            continue
        mismatched.append(key)
        print(
            f"[{key}] PARITY FAIL: {len(missing)} missing, {len(extra)} extra "
            + f"(derived {len(derived)}, live {len(live)})"
        )
        for title in missing[:5]:
            print(f"[{key}]   MISSING {title}")
        for title in extra[:5]:
            print(f"[{key}]   EXTRA   {title}")
    print(
        f"parity union: {len(derived_union)} derived titles, "
        + f"{len(live_union)} live managed titles, "
        + f"{len(derived_union - live_union)} unprojected, "
        + f"{len(live_union - derived_union)} unaccounted"
    )
    if mismatched:
        print(
            f"parity: FAILED for {len(mismatched)} book(s): "
            + f"{', '.join(mismatched)} — pending changes remain"
        )
        return 1
    print(
        "parity: PROVEN — every book in scope matches the corpus scan, "
        + "0 pending ADD/DEL/UPD"
    )
    return 0
