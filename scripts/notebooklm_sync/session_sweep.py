from __future__ import annotations

from collections.abc import Callable, Collection, Iterable, Mapping
from pathlib import Path

from .models import (
    SESSION_ALIAS_PREFIX,
    SESSION_DEAD,
    SESSION_FOREIGN,
    SESSION_LIVE,
)
from .nlm_client import JsonValue
from .session_sync import SessionAdapter
from .session_targets import LiveSessionBranches, SessionGitFactory


def classify_session_notebooks(
    titles: Iterable[JsonValue], live_aliases: Collection[str], slugs: Iterable[str]
) -> list[tuple[str, str]]:
    prefixes = [f"{SESSION_ALIAS_PREFIX}{slug}-" for slug in slugs]
    classified: list[tuple[str, str]] = []
    for title in titles:
        name = str(title or "")
        if not name.startswith(SESSION_ALIAS_PREFIX):
            continue
        if name in live_aliases:
            verdict = SESSION_LIVE
        elif any(name.startswith(prefix) for prefix in prefixes):
            verdict = SESSION_DEAD
        else:
            verdict = SESSION_FOREIGN
        classified.append((name, verdict))
    return classified


def session_source_count(
    row: JsonValue | Mapping[str, JsonValue],
) -> int | None:
    if not isinstance(row, Mapping):
        return None
    for key in ("source_count", "sources", "sourceCount"):
        value = row.get(key)
        if isinstance(value, int):
            return value
    return None


def live_session_aliases(
    repositories: Iterable[tuple[str, Path]],
    *,
    git_factory: SessionGitFactory,
    live_branches: LiveSessionBranches,
    notebook_alias: Callable[[str, str], str],
) -> tuple[set[str], list[str]]:
    aliases: set[str] = set()
    errors: list[str] = []
    for name, checkout in repositories:
        roots = [checkout]
        try:
            for record in git_factory(checkout).worktree_records():
                path = Path(record.path)
                if path not in roots:
                    roots.append(path)
        except (AttributeError, OSError, RuntimeError, TypeError, ValueError) as exc:
            errors.append(f"{name}: could not enumerate worktrees: {exc}")
            continue
        for checkout_root in roots:
            try:
                branches, listing_errors = live_branches(
                    git_factory(checkout_root), checkout_root
                )
            except (
                AttributeError,
                OSError,
                RuntimeError,
                TypeError,
                ValueError,
            ) as exc:
                errors.append(f"{name} [{checkout_root}]: {exc}")
                continue
            errors.extend(
                f"{name} [{checkout_root}]: {detail}" for detail in listing_errors
            )
            for branch in branches:
                try:
                    aliases.add(notebook_alias(name, branch))
                except (
                    AttributeError,
                    OSError,
                    RuntimeError,
                    TypeError,
                    ValueError,
                ) as exc:
                    errors.append(f"{name} {branch}: {exc}")
    return aliases, errors


def session_notebook_sweep(
    pairs: list[tuple[str, Path]],
    aliases: set[str],
    errors: list[str],
    apply: bool,
    *,
    adapter: SessionAdapter,
    notebook_title: Callable[[Mapping[str, JsonValue]], str | None],
) -> int:
    if errors:
        print(
            "[session-sweep] REFUSED: this run could not account for every "
            + "session repository, and a repository it cannot enumerate looks "
            + "exactly like one whose sessions have ended. Nothing was retired."
        )
        for detail in errors:
            print(f"[session-sweep]   unaccounted: {detail}")
        return 1
    listing = adapter.list_sessions_result()
    if not listing.ok:
        print(
            "[session-sweep] REFUSED: the notebook list could not be read, so "
            + "nothing is known about session notebooks — this is NOT an empty "
            + f"account: {listing.detail}"
        )
        return 1
    rows: dict[str, Mapping[str, JsonValue]] = {}
    for notebook in listing.rows:
        title = notebook_title(notebook)
        if title:
            rows[title] = notebook
    slugs = [name.lower() for name, _checkout in pairs]
    verdicts = classify_session_notebooks(rows, aliases, slugs)
    dead = [title for title, verdict in verdicts if verdict == SESSION_DEAD]
    for title, verdict in verdicts:
        if verdict == SESSION_LIVE:
            print(f"[session-sweep] KEEP   {title} (a live session claims it)")
        elif verdict == SESSION_FOREIGN:
            print(
                f"[session-sweep] SKIP   {title} (names a repository this "
                + "workspace does not carry)"
            )
        else:
            count = session_source_count(rows[title])
            discards = "" if count is None else f"; retiring discards {count} source(s)"
            action = "RETIRE" if apply else "DEAD  "
            print(
                f"[session-sweep] {action} {title} "
                + f"(no live session claims it{discards})"
            )
    if not dead:
        print(f"[session-sweep] {len(aliases)} live session(s); no orphans")
        return 0
    if not apply:
        print(
            f"[session-sweep] dry-run: {len(dead)} orphan(s) pending; "
            + "re-run with --apply to retire"
        )
        return 0
    failures = 0
    for title in dead:
        result = adapter.retire(title)
        print(
            f"[session-sweep] {'retired' if result.ok else 'FAILED '} {title}: "
            + f"{result.detail}"
        )
        if not result.ok:
            failures += 1
    return 1 if failures else 0
