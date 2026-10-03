from __future__ import annotations

import argparse
import json
from collections.abc import Callable, Mapping, Sequence
from datetime import datetime, timezone
from pathlib import Path
from typing import Protocol

from .corpus import DesiredState
from .lifecycle_sync import ManifestPayloadError, SyncManifest, parse_sync_manifest
from .models import BookSpec, SessionSync
from .nlm_client import JsonValue, NotebookRow


class ParityReporter(Protocol):
    def __call__(self, root: Path, *, book: str | None = None) -> int: ...


class SessionSyncer(Protocol):
    def __call__(
        self,
        root: Path,
        branch: str,
        apply: bool,
        *,
        repository: str | None = None,
        retire: bool = False,
    ) -> SessionSync: ...


class BookSyncer(Protocol):
    def __call__(
        self,
        root: Path,
        spec: BookSpec,
        desired: dict[str, str],
        manifest: SyncManifest,
        apply: bool,
        *,
        notebooks: Sequence[NotebookRow | Mapping[str, JsonValue]] | None = None,
    ) -> tuple[bool, bool]: ...


class CliArgs(argparse.Namespace):
    root: Path
    apply: bool
    parity: bool
    book: str | None
    session_ref: str | None
    session_repository: str | None
    session_retire: bool
    session_sweep: bool
    import_exports: str | None
    import_new_sources: str | None
    target_path: str | None
    import_date: str

    def __init__(self) -> None:
        super().__init__()
        self.root = Path()
        self.apply = False
        self.parity = False
        self.book = None
        self.session_ref = None
        self.session_repository = None
        self.session_retire = False
        self.session_sweep = False
        self.import_exports = None
        self.import_new_sources = None
        self.target_path = None
        self.import_date = datetime.now(timezone.utc).date().isoformat()


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    _ = parser.add_argument("root", type=Path)
    _ = parser.add_argument("--apply", action="store_true")
    _ = parser.add_argument(
        "--parity",
        action="store_true",
        help="prove live books against the corpus scan; reports, never mutates",
    )
    _ = parser.add_argument("--book", help="sync one scan-derived book key")
    _ = parser.add_argument("--session-ref", metavar="BRANCH")
    _ = parser.add_argument("--session-repository", metavar="REPOSITORY")
    _ = parser.add_argument("--session-retire", action="store_true")
    _ = parser.add_argument("--session-sweep", action="store_true")
    _ = parser.add_argument("--import-exports", metavar="NOTEBOOK")
    _ = parser.add_argument("--import-new-sources", metavar="NOTEBOOK")
    _ = parser.add_argument("--target-path")
    _ = parser.add_argument(
        "--import-date",
        default=datetime.now(timezone.utc).date().isoformat(),
        help="date stamp for imported idea files (YYYY-MM-DD)",
    )
    return parser


def run(
    *,
    enforce_profile: Callable[[Path], Mapping[str, str] | None],
    parity_report: ParityReporter,
    sweep_sessions: Callable[[Path, bool], int],
    sync_session: SessionSyncer,
    import_exports: Callable[[Path, str, bool, str], int],
    import_new: Callable[[Path, str, str, bool, str], int],
    scan: Callable[[Path], tuple[DesiredState, dict[str, BookSpec]]],
    list_notebooks: Callable[[], list[NotebookRow]],
    sync_book: BookSyncer,
    sweep_workbench: Callable[[Path, bool], None],
    operation_errors: tuple[type[Exception], ...],
) -> None:
    parser = _parser()
    args = parser.parse_args(namespace=CliArgs())
    _ = enforce_profile(args.root)
    if args.parity:
        raise SystemExit(parity_report(args.root, book=args.book))
    if args.session_sweep:
        if args.session_ref:
            parser.error(
                "--session-sweep reconciles the whole session namespace and "
                + "--session-ref names one branch; run them separately"
            )
        raise SystemExit(sweep_sessions(args.root, args.apply))
    if args.session_ref:
        _ = sync_session(
            args.root,
            args.session_ref,
            args.apply,
            repository=args.session_repository,
            retire=args.session_retire,
        )
        return
    if args.session_retire or args.session_repository:
        parser.error("--session-retire / --session-repository require --session-ref")
    if args.import_exports:
        imported_on = _import_date(args.import_date, parser)
        _ = import_exports(args.root, args.import_exports, args.apply, imported_on)
        return
    if args.import_new_sources:
        if not args.target_path:
            parser.error("--target-path is required with --import-new-sources")
        imported_on = _import_date(args.import_date, parser)
        _ = import_new(
            args.root,
            args.import_new_sources,
            args.target_path,
            args.apply,
            imported_on,
        )
        return
    _sync_books(
        args,
        parser,
        scan=scan,
        list_notebooks=list_notebooks,
        sync_book=sync_book,
        sweep_workbench=sweep_workbench,
        operation_errors=operation_errors,
    )


def _import_date(value: str, parser: argparse.ArgumentParser) -> str:
    try:
        return datetime.fromisoformat(value).date().isoformat()
    except ValueError:
        parser.error(f"--import-date must be an ISO date, got {value!r}")


def _sync_books(
    args: CliArgs,
    parser: argparse.ArgumentParser,
    *,
    scan: Callable[[Path], tuple[DesiredState, dict[str, BookSpec]]],
    list_notebooks: Callable[[], list[NotebookRow]],
    sync_book: BookSyncer,
    sweep_workbench: Callable[[Path, bool], None],
    operation_errors: tuple[type[Exception], ...],
) -> None:
    manifest_path = args.root / ".claude/nlm-sync-manifest.json"
    try:
        raw: JsonValue = (
            json.loads(manifest_path.read_text()) if manifest_path.exists() else {}
        )
        manifest: SyncManifest = parse_sync_manifest(raw)
    except (json.JSONDecodeError, ManifestPayloadError) as exc:
        parser.error(f"invalid sync manifest {manifest_path}: {exc}")
    if manifest.pop("ideation", None) is not None:
        print("manifest: dropped the retired shared-ideation key")
    desired, specs = scan(args.root)
    if args.book and args.book not in desired:
        parser.error(
            f"--book {args.book!r} is not a book this scan derives; "
            + f"available: {', '.join(sorted(desired))}"
        )

    def flush_manifest() -> None:
        manifest_path.parent.mkdir(exist_ok=True)
        _ = manifest_path.write_text(json.dumps(manifest, indent=1))

    notebooks: list[NotebookRow] | None = None
    failures: list[str] = []
    overflows: list[str] = []
    for book, items in desired.items():
        if args.book and book != args.book:
            continue
        print(f"== {book}: {len(items)} desired sources ==")
        try:
            if notebooks is None:
                notebooks = list_notebooks()
            ok, overflowed = sync_book(
                args.root, specs[book], items, manifest, args.apply, notebooks=notebooks
            )
        except operation_errors as exc:
            failures.append(book)
            print(f"[{book}] FAILED ({exc}); continuing with the remaining books")
            notebooks = None
            if args.apply:
                flush_manifest()
            continue
        if overflowed:
            overflows.append(book)
        if not ok:
            failures.append(book)
        if args.apply:
            flush_manifest()
    if args.apply:
        flush_manifest()
        print(f"manifest -> {manifest_path}")
    try:
        sweep_workbench(args.root, args.apply)
    except operation_errors as exc:
        print(f"[workbench] orphan sweep SKIPPED (unexpected error: {exc})")
    if failures or overflows:
        parts: list[str] = []
        if overflows:
            parts.append(f"over-cap: {', '.join(overflows)}")
        if failures:
            parts.append(f"failed: {', '.join(failures)}")
        raise SystemExit(
            f"[sync] nonzero — {'; '.join(parts)} (every other book completed)"
        )
