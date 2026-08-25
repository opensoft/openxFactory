from __future__ import annotations

import re
from pathlib import Path
from typing import TypeAlias

from .models import (
    GROUNDING,
    IDEATION_STATUSES,
    SESSION_CONTAINER_SUFFIX,
    SKIP_PARTS,
    STATIC_BOOKS,
    STATUS_RE,
    BookSpec,
    ideation_spec,
    static_spec,
)

DesiredState: TypeAlias = dict[str, dict[str, str]]


def in_nested_checkout(document: Path, repository_root: Path) -> bool:
    for parent in document.parents:
        if parent == repository_root:
            return False
        if (parent / ".git").exists():
            return True
    return False


def pinned_factory_paths(root: Path) -> list[str]:
    gitmodules = root / ".gitmodules"
    if gitmodules.is_file():
        pins = re.findall(
            r"^\s*path\s*=\s*(xFactories/\S+)\s*$",
            gitmodules.read_text(),
            re.MULTILINE,
        )
        if pins:
            return sorted(path for path in pins if (root / path).is_dir())
    factories = root / "xFactories"
    if not factories.is_dir():
        return []
    return [
        str(path.relative_to(root))
        for path in sorted(factories.iterdir())
        if path.is_dir() and not path.name.endswith(SESSION_CONTAINER_SUFFIX)
    ]


def scan(root: Path) -> tuple[DesiredState, dict[str, BookSpec]]:
    desired: DesiredState = {book: {} for book in STATIC_BOOKS}
    specs = {book: static_spec(book) for book in STATIC_BOOKS}
    for base in ["openxFactory", *pinned_factory_paths(root)]:
        repository_root = root / base
        for document in sorted(repository_root.rglob("*.md")):
            relative = document.relative_to(root)
            if SKIP_PARTS.intersection(relative.parts) or "openspec" in relative.parts:
                continue
            if in_nested_checkout(document, repository_root):
                continue
            match = STATUS_RE.search(document.read_text(errors="replace")[:2000])
            if match is None:
                continue
            status = match.group(1)
            repository = (
                relative.parts[0]
                if relative.parts[0] != "xFactories"
                else relative.parts[1]
            )
            stem = (
                f"{document.parent.name}/{document.stem}"
                if document.stem.lower() == "readme"
                else document.stem
            )
            title = f"[{status}] {repository}: {stem}"
            if status in IDEATION_STATUSES:
                spec = ideation_spec(repository)
                specs.setdefault(spec.key, spec)
                desired.setdefault(spec.key, {})[str(relative)] = title
            for book, config in STATIC_BOOKS.items():
                if status in config["statuses"]:
                    desired[book][str(relative)] = title
    specs_root = root / "openxFactory/openspec/specs"
    for document in sorted(specs_root.glob("*/spec.md")):
        relative = document.relative_to(root)
        desired["canon"][str(relative)] = (
            f"[spec] openxFactory: {document.parent.name}"
        )
    for grounding in GROUNDING:
        stem = Path(grounding).stem
        for book in desired:
            desired[book][grounding] = f"[grounding] openxFactory: {stem}"
    return desired, specs
