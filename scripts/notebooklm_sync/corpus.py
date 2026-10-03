from __future__ import annotations

import re
from collections.abc import Callable, Sequence
from pathlib import Path
from typing import TypeAlias

from .corpus_titles import derive_stems, title_segments
from .models import (
    GROUNDING,
    IDEATION_STATUSES,
    PROJECTED_STATUSES,
    ROOT_LEVEL_GOVERNED_PRODUCTS,
    SESSION_CONTAINER_SUFFIX,
    SKIP_PARTS,
    STATIC_BOOKS,
    STATUS_RE,
    BookSpec,
    ideation_spec,
    static_spec,
)

DesiredState: TypeAlias = dict[str, dict[str, str]]
PINNED_FACTORY_PATH_RE = re.compile(
    r"^\s*path\s*=\s*(xFactories/\S+)\s*$", re.MULTILINE
)


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
        pins = [
            match.group(1)
            for match in PINNED_FACTORY_PATH_RE.finditer(gitmodules.read_text())
        ]
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


def pinned_root_product_paths(root: Path) -> list[str]:
    gm = root / ".gitmodules"
    if not gm.is_file():
        return []
    declared = set(
        re.findall("^\\s*path\\s*=\\s*(\\S+)\\s*$", gm.read_text(), re.MULTILINE)
    )
    found: list[str] = []
    for name in ROOT_LEVEL_GOVERNED_PRODUCTS:
        if name not in declared or not (root / name).is_dir():
            continue
        if not any((root / name).iterdir()):
            print(
                f"WARN {name} is pinned at the aggregation root but its checkout is empty (uninitialized submodule); its ideation documents cannot be swept. Remediation: run `git submodule update --init {name}`."
            )
        found.append(name)
    return found


def governed_repo_paths(root: Path) -> list[str]:
    return [*pinned_root_product_paths(root), *pinned_factory_paths(root)]


def scan(
    root: Path,
    *,
    derive: Callable[
        [Sequence[tuple[str, str, tuple[str, ...]]]], dict[str, str]
    ] = derive_stems,
) -> tuple[dict[str, dict[str, str]], dict[str, BookSpec]]:
    desired: dict[str, dict[str, str]] = {b: {} for b in STATIC_BOOKS}
    specs: dict[str, BookSpec] = {b: static_spec(b) for b in STATIC_BOOKS}
    found: list[tuple[str, str, str, tuple[str, ...]]] = []
    for base in ["openxFactory", *governed_repo_paths(root)]:
        basep = root / base
        for f in sorted(basep.rglob("*.md")):
            rel = f.relative_to(root)
            if SKIP_PARTS.intersection(rel.parts) or "openspec" in rel.parts:
                continue
            if in_nested_checkout(f, basep):
                continue
            m = STATUS_RE.search(f.read_text(errors="replace")[:2000])
            if not m:
                continue
            status = m.group(1)
            if status not in PROJECTED_STATUSES:
                continue
            repo = rel.parts[0] if rel.parts[0] != "xFactories" else rel.parts[1]
            found.append((str(rel), repo, status, title_segments(rel)))
    stems = derive([(rel, repo, segs) for rel, repo, _st, segs in found])
    for rel, repo, status, _segs in found:
        title = f"[{status}] {repo}: {stems[rel]}"
        if status in IDEATION_STATUSES:
            spec = ideation_spec(repo)
            _ = specs.setdefault(spec.key, spec)
            desired.setdefault(spec.key, {})[rel] = title
        for book, cfg in STATIC_BOOKS.items():
            if status in cfg["statuses"]:
                desired[book][rel] = title
    for f in sorted((root / "openxFactory/openspec/specs").glob("*/spec.md")):
        rel = f.relative_to(root)
        desired["canon"][str(rel)] = f"[spec] openxFactory: {f.parent.name}"
    for g in GROUNDING:
        stem = Path(g).stem
        for items in desired.values():
            items[g] = f"[grounding] openxFactory: {stem}"
    return (desired, specs)
