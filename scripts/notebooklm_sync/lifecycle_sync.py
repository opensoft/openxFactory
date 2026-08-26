from __future__ import annotations

import hashlib
from collections.abc import Callable, Mapping, Sequence
from pathlib import Path
from typing import TypeAlias

from .models import CHARTER, CHARTER_TITLE, BookSpec
from .nlm_client import JsonValue, NotebookRow, SourceRow

ManifestEntry: TypeAlias = dict[str, str]
BookManifest: TypeAlias = dict[str, ManifestEntry]
SyncManifest: TypeAlias = dict[str, BookManifest]


class ManifestPayloadError(RuntimeError):
    pass


def parse_sync_manifest(payload: JsonValue) -> SyncManifest:
    if not isinstance(payload, dict):
        raise ManifestPayloadError("sync manifest must contain a JSON object")
    manifest: SyncManifest = {}
    for book, raw_entries in payload.items():
        if not isinstance(raw_entries, dict):
            raise ManifestPayloadError(
                f"sync manifest book {book!r} must contain a JSON object"
            )
        entries: BookManifest = {}
        for relative, raw_entry in raw_entries.items():
            if not isinstance(raw_entry, dict):
                raise ManifestPayloadError(
                    f"sync manifest entry {book!r}/{relative!r} must be an object"
                )
            digest = raw_entry.get("hash")
            title = raw_entry.get("title")
            if not isinstance(digest, str) or not isinstance(title, str):
                raise ManifestPayloadError(
                    f"sync manifest entry {book!r}/{relative!r} requires text "
                    + "hash and title fields"
                )
            entries[relative] = {"hash": digest, "title": title}
        manifest[book] = entries
    return manifest


def sync_book(
    root: Path,
    spec: BookSpec,
    desired: dict[str, str],
    manifest: SyncManifest,
    apply: bool,
    notebooks: Sequence[NotebookRow | Mapping[str, JsonValue]] | None,
    *,
    resolve_book: Callable[
        [Path, BookSpec, bool, Sequence[NotebookRow | Mapping[str, JsonValue]] | None],
        tuple[str | None, bool],
    ],
    list_sources: Callable[[str], list[SourceRow]],
    run_text: Callable[..., str],
    sleep: Callable[[float], None],
    add_source: Callable[[str, str, str], None],
    source_cap: int,
    warn_headroom: int,
) -> tuple[bool, bool]:
    key = spec.key
    notebook_id, ok = resolve_book(root, spec, apply, notebooks)
    handle = notebook_id or spec.title
    existing = list_sources(notebook_id) if notebook_id else []
    by_title: dict[str, list[str]] = {}
    unmanaged = 0
    for source in existing:
        by_title.setdefault(source.title, []).append(source.source_id)
        if not (source.title.startswith("[") or source.title == CHARTER_TITLE):
            unmanaged += 1
    book_manifest = manifest.setdefault(key, {})

    overflowed = False
    projected = len(desired) + 1 + unmanaged
    headroom = source_cap - projected
    if projected > source_cap:
        overflowed = True
        allowed = max(0, source_cap - 1 - unmanaged)
        items = sorted(desired.items())
        for _relative, title in items[allowed:]:
            print(
                f"[{key}] EXCESS {title} (occupancy {projected} exceeds "
                + f"cap {source_cap}; cannot project)"
            )
        desired = dict(items[:allowed])
        print(
            f"[{key}] OVER CAP: projecting the deterministic in-cap prefix "
            + f"({allowed} of {len(items)} members; charter + {unmanaged} "
            + "unmanaged occupy the rest)"
        )
    elif headroom <= warn_headroom:
        print(
            f"[{key}] WARN headroom {headroom}: occupancy {projected} of "
            + f"cap {source_cap}. No successor split is defined for this book — "
            + "the owed remedy is an OpenSpec delta to lifecycle-notebook-projection "
            + "defining its split"
        )

    if CHARTER_TITLE not in by_title:
        print(f"[{key}] ADD  {CHARTER_TITLE}")
        if apply and notebook_id:
            _ = run_text(
                "source",
                "add",
                handle,
                "--text",
                CHARTER,
                "--title",
                CHARTER_TITLE,
            )
            sleep(2)

    wanted_titles = set(desired.values()) | {CHARTER_TITLE}
    for title, source_ids in by_title.items():
        if not (title.startswith("[") or title == CHARTER_TITLE):
            continue
        doomed = source_ids if title not in wanted_titles else source_ids[1:]
        for source_id in doomed:
            print(f"[{key}] DEL  {title}")
            if apply:
                _ = run_text("source", "delete", source_id, "--confirm")
                sleep(2)

    for relative, title in sorted(desired.items()):
        text = (root / relative).read_text(errors="replace")
        digest = hashlib.sha256(text.encode()).hexdigest()[:16]
        previous = book_manifest.get(relative)
        unchanged = previous is not None and previous.get("hash") == digest
        if title in by_title and unchanged:
            continue
        if title in by_title:
            print(f"[{key}] UPD  {title}")
            if apply:
                _ = run_text("source", "delete", by_title[title][0], "--confirm")
                sleep(2)
        else:
            print(f"[{key}] ADD  {title}")
        if apply:
            add_source(handle, text, title)
            sleep(2)
        book_manifest[relative] = {"hash": digest, "title": title}
    return ok, overflowed
