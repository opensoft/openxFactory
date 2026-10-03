from __future__ import annotations

import re
from collections.abc import Sequence
from pathlib import Path

from .models import (
    EXPORT_RE,
    SESSION_CONTAINER_SUFFIX,
    SOURCE_ID_RE,
    ExportTarget,
    ImportPathError,
    ImportTarget,
)


def slug_part(value: str) -> str:
    value = value.strip().lower()
    value = re.sub(r"[^a-z0-9-]+", "-", value)
    value = re.sub(r"-{2,}", "-", value).strip("-")
    return value or "untitled"


def parse_export_title(
    title: str, default_repo: str = "openxFactory"
) -> ExportTarget | None:
    match = EXPORT_RE.match(title)
    if match is None:
        return None
    status, remainder = match.groups()
    repository = default_repo
    if ":" in remainder:
        maybe_repository, remainder = remainder.split(":", 1)
        repository = maybe_repository.strip() or default_repo
        remainder = remainder.strip()
    if re.fullmatch(r"[A-Za-z0-9-]+", repository) is None:
        return None
    if " - " in remainder:
        topic, idea_title = remainder.split(" - ", 1)
    else:
        topic = remainder
        idea_title = remainder
    topic = slug_part(topic)
    idea_title = idea_title.strip() or topic
    return ExportTarget(
        status=status,
        repo=repository,
        topic=topic,
        title=idea_title,
        source_title=title,
    )


def repo_path(root: Path, repository: str) -> Path:
    direct = root / repository
    if direct.exists() or repository == "openxFactory":
        return direct
    return root / "xFactories" / repository


def session_repository_of(parts: tuple[str, ...]) -> str | None:
    head = list(parts[1:] if parts and parts[0] == "xFactories" else parts)
    if len(head) < 2 or not head[0].endswith(SESSION_CONTAINER_SUFFIX):
        return None
    if head[1] != "sessions":
        return None
    return head[0][: -len(SESSION_CONTAINER_SUFFIX)] or None


def target_from_path(root: Path, target_path: str) -> ImportTarget:
    raw = Path(target_path)
    path = raw if raw.is_absolute() else root / raw
    try:
        relative = path.resolve().relative_to(root.resolve())
    except ValueError as exc:
        raise ImportPathError("--target-path must stay inside the workspace") from exc
    parts = relative.parts
    repository = parts[0] if parts[0] != "xFactories" else parts[1]
    repository = session_repository_of(parts) or repository
    if "ideation" in parts:
        index = parts.index("ideation")
        if index + 2 >= len(parts) or parts[index + 1] not in {"brainstorm", "staging"}:
            raise ImportPathError(
                "--target-path must name an ideation brainstorm/staging topic"
            )
        status = "brainstorm" if parts[index + 1] == "brainstorm" else "staged"
        return ImportTarget(
            status=status,
            repo=repository,
            topic=parts[index + 2],
            path=path.resolve(),
        )
    try:
        index = parts.index("openspec")
    except ValueError as exc:
        raise ImportPathError(
            "--target-path must name ideation or active proposal support"
        ) from exc
    tail = parts[index:]
    if (
        len(tail) != 4
        or tail[1] != "changes"
        or tail[2] == "archive"
        or tail[3] != "supporting-docs"
    ):
        raise ImportPathError(
            "--target-path must name openspec/changes/<change>/supporting-docs"
        )
    change = root.joinpath(*parts[: index + 3])
    if not (change / "proposal.md").is_file():
        raise ImportPathError("--target-path must belong to an active OpenSpec change")
    if not (path / "manifest.yaml").is_file():
        raise ImportPathError("proposal supporting-docs target must have manifest.yaml")
    return ImportTarget(
        status="draft",
        repo=repository,
        topic=tail[2],
        path=path.resolve(),
    )


def export_destination(root: Path, target: ExportTarget, imported_on: str) -> Path:
    base = repo_path(root, target.repo)
    area = "brainstorm" if target.status == "brainstorm" else "staging"
    return (
        base / "ideation" / area / target.topic / f"notebooklm-ideas-{imported_on}.md"
    )


def imported_source_ids(root: Path, extra_roots: Sequence[Path] = ()) -> set[str]:
    source_ids: set[str] = set()
    bases = [root / relative for relative in ("openxFactory", "xFactories")]
    bases.extend(Path(extra) for extra in extra_roots)
    for base in bases:
        if not base.exists():
            continue
        for path in base.rglob("*.md"):
            if "ideation" not in path.parts and "supporting-docs" not in path.parts:
                continue
            source_ids.update(SOURCE_ID_RE.findall(path.read_text(errors="replace")))
    return source_ids
