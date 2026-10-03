from __future__ import annotations

from collections.abc import Sequence
from pathlib import Path

README_FLOOR_SEGMENTS = 2


def title_segments(rel: Path) -> tuple[str, ...]:
    parts = rel.parts[1:] if rel.parts[0] == "xFactories" else rel.parts
    return (*parts[:-1], Path(parts[-1]).stem)


def derive_stems(
    documents: Sequence[tuple[str, str, tuple[str, ...]]],
) -> dict[str, str]:
    by_repo: dict[str, list[tuple[str, tuple[str, ...]]]] = {}
    for rel, repo, segs in documents:
        by_repo.setdefault(repo, []).append((rel, segs))
    stems: dict[str, str] = {}
    for docs in by_repo.values():
        counts: dict[int, dict[str, int]] = {}
        for _rel, segs in docs:
            for k in range(1, len(segs) + 1):
                level = counts.setdefault(k, {})
                suffix = "/".join(segs[-k:])
                level[suffix] = level.get(suffix, 0) + 1
        for rel, segs in docs:
            floor = README_FLOOR_SEGMENTS if segs[-1].lower() == "readme" else 1
            stems[rel] = "/".join(segs)
            for k in range(min(floor, len(segs)), len(segs) + 1):
                suffix = "/".join(segs[-k:])
                if counts[k][suffix] == 1:
                    stems[rel] = suffix
                    break
    return stems
