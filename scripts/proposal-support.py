#!/usr/bin/env python3
"""Move staged proposal support and preserve it through OpenSpec archive."""

from __future__ import annotations

import argparse
import gzip
import hashlib
import io
import json
import os
from pathlib import Path, PurePosixPath
import re
import shutil
import subprocess
import tarfile
from datetime import date


LINK_RE = re.compile(r"(!?\[[^\]]*\])\(([^)]+)\)")


class SupportError(ValueError):
    pass


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def manifest_text(data: dict) -> str:
    # JSON is valid YAML 1.2 and keeps the command dependency-free.
    return json.dumps(data, indent=2, sort_keys=True) + "\n"


def load_manifest(path: Path) -> dict:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise SupportError(f"invalid manifest {path}: {exc}") from exc
    if not isinstance(data, dict) or data.get("format_version") != 1:
        raise SupportError(f"invalid manifest format: {path}")
    return data


def ensure_inside(path: Path, parent: Path, label: str) -> Path:
    resolved = path.resolve()
    try:
        resolved.relative_to(parent.resolve())
    except ValueError as exc:
        raise SupportError(f"{label} escapes {parent}") from exc
    return resolved


def reject_symlinks(path: Path) -> None:
    current = path
    while True:
        if current.is_symlink():
            raise SupportError(f"symlink not allowed: {current}")
        if current == current.parent:
            break
        current = current.parent


def repo_revision(root: Path) -> str:
    result = subprocess.run(  # NOSONAR: argv is allowlisted; shell is disabled
        ["git", "-C", str(root), "rev-parse", "HEAD"],
        capture_output=True, text=True, check=False,
    )
    return result.stdout.strip() if result.returncode == 0 else "uncommitted"


def git_blob_sha256(root: Path, revision: str, source_path: str) -> str | None:
    if revision == "uncommitted":
        return None
    if not re.fullmatch(r"(?:[0-9a-f]{40}|[0-9a-f]{64})", revision):
        raise SupportError(f"invalid repository revision: {revision}")
    source = PurePosixPath(source_path)
    if (source.is_absolute() or not source.parts
            or ".." in source.parts or "" in source.parts):
        raise SupportError(f"invalid repository source path: {source_path}")
    object_name = f"{revision}:{source.as_posix()}"
    result = subprocess.run(
        ["git", "-C", str(root.resolve()), "show", "--end-of-options",
         object_name],
        capture_output=True, check=False,
    )
    return sha256_bytes(result.stdout) if result.returncode == 0 else None


def active_change_dir(root: Path, change: str) -> Path:
    # Change ids are plain slugs; anything with path syntax would let a
    # caller-supplied name traverse outside openspec/changes/.
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]*", change):
        raise SupportError(f"invalid change name: {change}")
    path = root / "openspec" / "changes" / change
    if not path.is_dir() or change == "archive":
        raise SupportError(f"active OpenSpec change not found: {change}")
    return path


def archived_change_dir(root: Path, change: str) -> Path:
    matches = sorted((root / "openspec" / "changes" / "archive").glob(
        f"????-??-??-{change}"
    ))
    if len(matches) != 1:
        raise SupportError(
            f"expected one archived OpenSpec change for {change}, found {len(matches)}"
        )
    return matches[0]


def change_dir(root: Path, change: str, archived: bool) -> Path:
    return (archived_change_dir if archived else active_change_dir)(root, change)


def markdown_target(raw: str) -> tuple[str, str] | None:
    value = raw.strip()
    if value.startswith("<") and value.endswith(">"):
        value = value[1:-1]
    if not value or value.startswith(("#", "http://", "https://", "mailto:")):
        return None
    path, marker, anchor = value.partition("#")
    return path, marker + anchor if marker else ""


def rewrite_links(text: str, old_file: Path, new_file: Path,
                  mapping: dict[Path, Path], root: Path) -> str:
    def replace(match: re.Match) -> str:
        parsed = markdown_target(match.group(2))
        if parsed is None:
            return match.group(0)
        raw_path, anchor = parsed
        old_target = ensure_inside(old_file.parent / raw_path, root,
                                   "Markdown link")
        target = mapping.get(old_target, old_target)
        if not target.exists() and target not in mapping.values():
            raise SupportError(
                f"broken relative link in {old_file}: {match.group(2)}"
            )
        relative = os.path.relpath(target, new_file.parent).replace(os.sep, "/")
        return f"{match.group(1)}({relative}{anchor})"

    return LINK_RE.sub(replace, text)


def proposed_content(path: Path, target: Path, mapping: dict[Path, Path],
                     root: Path, change: str, historical: bool = False) -> bytes:
    data = path.read_bytes()
    if path.suffix.lower() != ".md":
        return data
    text = data.decode("utf-8")
    status = re.search(r"^Status:\s*([^\s]+)\s*$", text, re.M)
    if status is None:
        raise SupportError(f"governed Markdown lacks Status header: {path}")
    if status.group(1) == "staged":
        text = re.sub(
            r"^Status:\s*staged\s*$",
            f"Status: draft\nProposed by: {change}",
            text,
            count=1,
            flags=re.M,
        )
    elif status.group(1) not in (
            {"draft", "record", "superseded", "retired"}
            if historical else {"draft", "record"}):
        raise SupportError(
            f"supporting Markdown status must be staged, draft, or record: {path}"
        )
    return rewrite_links(text, path, target, mapping, root).encode("utf-8")


def source_files(source: Path) -> list[Path]:
    files = []
    for path in sorted(source.rglob("*")):
        reject_symlinks(path)
        if path.is_file():
            files.append(path.resolve())
    return files


def select_files(source: Path, requested: list[str]) -> tuple[list[Path], list[Path]]:
    all_files = source_files(source)
    if not requested:
        return all_files, []
    selected = []
    for raw in requested:
        candidate = ensure_inside(source / raw, source, "selected file")
        reject_symlinks(candidate)
        if not candidate.is_file():
            raise SupportError(f"selected file not found: {raw}")
        selected.append(candidate)
    selected = sorted(set(selected))
    return selected, [path for path in all_files if path not in selected]


def move_file(source: Path, target: Path) -> None:
    # Git stores snapshots, not rename operations; review/commit still detects
    # the move without mutating the caller's index as an implementation side effect.
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.move(str(source), str(target))


def transition(root: Path, change: str, source_arg: str, requested: list[str],
               workspace: str | None, transition_date: str, archived: bool,
               apply: bool) -> dict:
    root = root.resolve()
    source = ensure_inside(root / source_arg, root, "staging source")
    expected = root / "ideation" / "staging"
    ensure_inside(source, expected, "staging source")
    if source == expected or not source.is_dir():
        raise SupportError("source must be a topic below ideation/staging")
    destination = change_dir(root, change, archived) / "supporting-docs"
    if (destination / "manifest.yaml").exists():
        raise SupportError(f"support manifest already exists: {destination}")

    selected, remaining = select_files(source, requested)
    if not selected:
        raise SupportError("no supporting files selected")
    mapping = {
        path: destination / path.relative_to(source) for path in selected
    }
    snapshots = {
        path: destination / "source-snapshots" / path.relative_to(source)
        for path in selected
    }
    for target in [*mapping.values(), *snapshots.values()]:
        ensure_inside(target, destination, "support destination")
        if target.exists():
            raise SupportError(f"support destination exists: {target}")

    rendered = {
        path: proposed_content(path, mapping[path], mapping, root, change,
                               historical=archived)
        for path in selected
    }
    revision = repo_revision(root)
    entries = [
        {
            "path": str(mapping[path].relative_to(destination)),
            "sha256": sha256_bytes(rendered[path]),
            "source_path": str(path.relative_to(root)),
            "source_sha256": sha256_file(path),
            "source_snapshot_path": str(
                snapshots[path].relative_to(destination)
            ),
        }
        for path in selected
    ]
    if revision != "uncommitted":
        for entry in entries:
            committed = git_blob_sha256(
                root, revision, entry["source_path"])
            if committed != entry["source_sha256"]:
                raise SupportError(
                    "staging source is not committed at source revision: "
                    f"{entry['source_path']}")
    manifest = {
        "change_id": change,
        "files": entries,
        "format_version": 1,
        "notebook_workspace": workspace,
        "origin_path": str(source.relative_to(root)),
        "remaining_paths": [str(path.relative_to(root)) for path in remaining],
        "source_revision": revision,
        "transitioned_at": transition_date,
    }

    action = "MOVE" if apply else "WOULD MOVE"
    for path in selected:
        print(f"{action} {path.relative_to(root)} -> {mapping[path].relative_to(root)}")
    if not apply:
        return manifest

    for path in selected:
        snapshots[path].parent.mkdir(parents=True, exist_ok=True)
        snapshots[path].write_bytes(path.read_bytes())
        move_file(path, mapping[path])
        mapping[path].write_bytes(rendered[path])
    destination.mkdir(parents=True, exist_ok=True)
    (destination / "manifest.yaml").write_text(
        manifest_text(manifest), encoding="utf-8"
    )
    for directory in sorted(source.rglob("*"), reverse=True):
        if directory.is_dir() and not any(directory.iterdir()):
            directory.rmdir()
    if source.exists() and not any(source.iterdir()):
        source.rmdir()
    return manifest


def verify_active_support(directory: Path) -> list[str]:
    support = directory / "supporting-docs"
    manifest = load_manifest(support / "manifest.yaml")
    errors = []
    root = directory.parents[2]
    revision = manifest.get("source_revision")
    for entry in manifest.get("files", []):
        path = ensure_inside(support / entry["path"], support, "manifest path")
        if not path.is_file():
            errors.append(f"missing support file: {path}")
        elif sha256_file(path) != entry.get("sha256"):
            errors.append(f"support checksum mismatch: {path}")
        source_sha256 = entry.get("source_sha256")
        snapshot_valid = False
        snapshot_path = entry.get("source_snapshot_path")
        if source_sha256 and snapshot_path:
            snapshot = ensure_inside(
                support / snapshot_path, support, "source snapshot path"
            )
            reject_symlinks(snapshot)
            if not snapshot.is_file():
                errors.append(f"missing source snapshot: {snapshot}")
            elif sha256_file(snapshot) != source_sha256:
                errors.append(f"source snapshot checksum mismatch: {snapshot}")
            else:
                snapshot_valid = True
        if source_sha256 and revision != "uncommitted":
            committed = git_blob_sha256(
                root, revision, entry.get("source_path", ""))
            if committed is None and not snapshot_valid:
                errors.append(
                    "staging source revision unavailable without valid snapshot: "
                    f"{entry.get('source_path', '')}"
                )
            elif committed is not None and committed != source_sha256:
                errors.append(
                    "staging source checksum mismatch: "
                    f"{entry.get('source_path', '')}")
        if path.suffix.lower() == ".md":
            text = path.read_text(encoding="utf-8")
            if re.search(r"^Status:\s*staged\s*$", text, re.M):
                errors.append(f"staged status under active proposal: {path}")
    return errors


def deterministic_bundle(support: Path) -> tuple[bytes, list[dict]]:
    entries = []
    buffer = io.BytesIO()
    with gzip.GzipFile(fileobj=buffer, mode="wb", filename="", mtime=0) as gz:
        with tarfile.open(fileobj=gz, mode="w", format=tarfile.GNU_FORMAT) as tar:
            for path in source_files(support):
                rel = path.relative_to(support).as_posix()
                data = path.read_bytes()
                info = tarfile.TarInfo(rel)
                info.size = len(data)
                info.mtime = 0
                info.mode = 0o644
                info.uid = info.gid = 0
                info.uname = info.gname = ""
                tar.addfile(info, io.BytesIO(data))
                entries.append({"path": rel, "sha256": sha256_bytes(data)})
    return buffer.getvalue(), entries


def package(root: Path, change: str, packaged_at: str, archived: bool,
            final_import_complete: bool, apply: bool) -> dict:
    root = root.resolve()
    directory = change_dir(root, change, archived)
    support = directory / "supporting-docs"
    if not support.is_dir():
        raise SupportError(f"supporting-docs folder not found: {support}")
    active_manifest = load_manifest(support / "manifest.yaml")
    if active_manifest.get("notebook_workspace") and not final_import_complete:
        raise SupportError("final NotebookLM source import is not recorded")
    errors = verify_active_support(directory)
    if errors:
        raise SupportError("; ".join(errors))

    bundle, files = deterministic_bundle(support)
    archive_manifest = {
        "bundle": {
            "path": "supporting-docs.tar.gz",
            "sha256": sha256_bytes(bundle),
        },
        "change_id": change,
        "files": files,
        "final_notebook_import_complete": final_import_complete,
        "format_version": 1,
        "notebook_workspace": active_manifest.get("notebook_workspace"),
        "origin_path": active_manifest.get("origin_path"),
        "packaged_at": packaged_at,
        "source_revision": active_manifest.get("source_revision"),
        "transitioned_at": active_manifest.get("transitioned_at"),
    }
    action = "PACKAGE" if apply else "WOULD PACKAGE"
    print(f"{action} {support} ({len(files)} files)")
    if apply:
        (directory / "supporting-docs.tar.gz").write_bytes(bundle)
        (directory / "supporting-docs.manifest.yaml").write_text(
            manifest_text(archive_manifest), encoding="utf-8"
        )
        shutil.rmtree(support)
    return archive_manifest


def safe_tar_members(bundle: Path) -> dict[str, bytes]:
    members = {}
    with tarfile.open(bundle, "r:gz") as archive:
        for member in archive.getmembers():
            pure = PurePosixPath(member.name)
            if member.issym() or member.islnk() or pure.is_absolute() or ".." in pure.parts:
                raise SupportError(f"unsafe archive member: {member.name}")
            if not member.isfile():
                continue
            stream = archive.extractfile(member)
            if stream is None:
                raise SupportError(f"unreadable archive member: {member.name}")
            members[member.name] = stream.read()
    return members


def verify_archive(directory: Path) -> list[str]:
    manifest_path = directory / "supporting-docs.manifest.yaml"
    bundle = directory / "supporting-docs.tar.gz"
    manifest = load_manifest(manifest_path)
    errors = []
    if not bundle.is_file():
        return [f"missing support bundle: {bundle}"]
    if sha256_file(bundle) != manifest.get("bundle", {}).get("sha256"):
        errors.append(f"bundle checksum mismatch: {bundle}")
    try:
        members = safe_tar_members(bundle)
    except (SupportError, tarfile.TarError, OSError) as exc:
        return errors + [str(exc)]
    expected = {entry["path"]: entry["sha256"] for entry in manifest.get("files", [])}
    if set(members) != set(expected):
        errors.append(f"bundle member inventory mismatch: {bundle}")
    for path, data in members.items():
        if path in expected and sha256_bytes(data) != expected[path]:
            errors.append(f"bundled file checksum mismatch: {path}")
    return errors


def verify(root: Path, change: str | None) -> list[str]:
    root = root.resolve()
    errors = []
    active_root = root / "openspec" / "changes"
    for directory in sorted(active_root.iterdir()):
        if not directory.is_dir() or directory.name == "archive":
            continue
        if change and directory.name != change:
            continue
        if (directory / "supporting-docs").exists():
            try:
                errors.extend(verify_active_support(directory))
            except SupportError as exc:
                errors.append(str(exc))
    for directory in sorted((active_root / "archive").iterdir()):
        if not directory.is_dir():
            continue
        change_id = re.sub(r"^\d{4}-\d{2}-\d{2}-", "", directory.name)
        if change and change_id != change:
            continue
        has_manifest = (directory / "supporting-docs.manifest.yaml").exists()
        has_bundle = (directory / "supporting-docs.tar.gz").exists()
        if has_manifest or has_bundle:
            if not (has_manifest and has_bundle):
                errors.append(f"incomplete archived support: {directory}")
            else:
                try:
                    errors.extend(verify_archive(directory))
                except SupportError as exc:
                    errors.append(str(exc))
    misplaced = list((root / "openspec" / "specs").rglob("supporting-docs.tar.gz"))
    errors.extend(f"support bundle under canonical specs: {path}" for path in misplaced)
    return errors


def archive_change(root: Path, change: str, packaged_at: str,
                   final_import_complete: bool, yes: bool) -> None:
    directory = active_change_dir(root, change)
    tasks = directory / "tasks.md"
    if tasks.is_file() and re.search(r"^- \[ \]", tasks.read_text(), re.M):
        raise SupportError("change has incomplete tasks")
    subprocess.run(
        ["openspec", "validate", change, "--strict"], cwd=root, check=True
    )
    package(root, change, packaged_at, archived=False,
            final_import_complete=final_import_complete, apply=True)
    command = ["openspec", "archive", change]
    if yes:
        command.append("--yes")
    subprocess.run(command, cwd=root, check=True)


def parser() -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser()
    ap.add_argument("root", type=Path, help="OpenSpec repository root")
    sub = ap.add_subparsers(dest="command", required=True)

    move = sub.add_parser("transition")
    move.add_argument("change")
    move.add_argument("source", help="path below ideation/staging")
    move.add_argument("--file", action="append", default=[])
    move.add_argument("--workspace")
    move.add_argument("--date", default=date.today().isoformat())
    move.add_argument("--archived", action="store_true")
    move.add_argument("--apply", action="store_true")

    pack = sub.add_parser("package")
    pack.add_argument("change")
    pack.add_argument("--date", default=date.today().isoformat())
    pack.add_argument("--archived", action="store_true")
    pack.add_argument("--final-import-complete", action="store_true")
    pack.add_argument("--apply", action="store_true")

    check = sub.add_parser("verify")
    check.add_argument("change", nargs="?")

    archive = sub.add_parser("archive")
    archive.add_argument("change")
    archive.add_argument("--date", default=date.today().isoformat())
    archive.add_argument("--final-import-complete", action="store_true")
    archive.add_argument("--yes", action="store_true")
    return ap


def main() -> None:
    args = parser().parse_args()
    try:
        if args.command == "transition":
            transition(args.root, args.change, args.source, args.file,
                       args.workspace, args.date, args.archived, args.apply)
        elif args.command == "package":
            package(args.root, args.change, args.date, args.archived,
                    args.final_import_complete, args.apply)
        elif args.command == "verify":
            errors = verify(args.root, args.change)
            if errors:
                raise SupportError("\n".join(errors))
            print("proposal support verification ok")
        else:
            archive_change(args.root.resolve(), args.change, args.date,
                           args.final_import_complete, args.yes)
    except (SupportError, subprocess.CalledProcessError) as exc:
        raise SystemExit(str(exc)) from exc


if __name__ == "__main__":
    main()
