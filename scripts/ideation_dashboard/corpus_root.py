"""Is this path a corpus checkout at all? — the entrypoint guard on `--repo-root`
/ `--checkout-root` (T092).

T092, minute one of the human acceptance pass: `--repo-root` was handed a path
from a DIFFERENT filesystem namespace (a container path, typed on the host), and
`generator.generate_snapshot` happily projected NOTHING from it. Every scan in the
projection is individually forgiving BY DESIGN — `corpus.iter_doc_paths` skips a
governed root that is not a directory, the change and staged-topic scans return []
for a missing base, the register adapters discover no source — so the snapshot came
back empty, was WRITTEN, the CLI exited 0, and the dashboard rendered its own
empty-state copy ("a sparse funnel is an honest funnel, not a broken one") over a
typo. Nothing downstream can tell an empty corpus from a wrong path.

So the ENTRYPOINTS refuse the wrong path before they generate or write anything,
and this module is the one definition they share: `cli.py`'s `--repo-root` and
`serve.py`'s `--checkout-root` are the same value under two spellings (runbook
§2), and a human who learns the rule on one must not be surprised by the other.

Deliberately NOT inside `generate_snapshot`: the nightly lane must never fail (it
reports SKIPPED instead), and a library caller scanning a tree of its own choosing
is not making the human's mistake. The guard belongs where a human types a path.

Deliberately its own module rather than part of `generator.py`: `serve.py` needs
this predicate on EVERY `build_server` (it is what `_checkout_real` answers), and
importing the generator there would newly require PyYAML in the served image's
startup path, which serves snapshots and scans nothing. This module is stdlib plus
`doc_health.corpus`, which the serving path already uses.
"""

from __future__ import annotations

from pathlib import Path

from doc_health import corpus

# The directories a snapshot is projected FROM: the governed document roots
# `corpus.iter_doc_paths` walks (documents — and with them clusters, the keyword
# index and every edge) plus `openspec/` (`generator._iter_changes`; `ideation/`
# already carries the staging folders). DERIVED from `corpus.GOVERNED_ROOTS`
# rather than restated, so a root added to the doc-health scan is a root this
# predicate accepts. A tree holding NONE of them projects nothing by
# construction, whatever else it holds.
SCANNED_ROOTS: tuple[str, ...] = tuple(sorted({*corpus.GOVERNED_ROOTS, "openspec"}))


def corpus_scan_defect(repo_root: Path | str) -> str | None:
    """Why `repo_root` cannot be scanned as a corpus checkout, or None when it
    can be.

    Structural only: it answers "could this tree project anything at all", never
    "does it". A real corpus that happens to be empty is LEGAL and passes here —
    the entrypoint warns loudly about a zero-document projection instead
    (`cli._warn_on_empty_projection`), because failing on it would make an
    honestly-empty repository unusable."""
    path = Path(repo_root)
    try:
        if not path.exists():
            return "the path does not exist"
        if not path.is_dir():
            return "the path is not a directory"
        if not any((path / root).is_dir() for root in SCANNED_ROOTS):
            return "the directory holds none of the roots a snapshot is projected from"
    except OSError as exc:  # an unreadable path is not a corpus checkout either
        return f"the path could not be read ({exc.strerror or exc})"
    return None


def corpus_root_refusal(repo_root: Path | str, *, flag: str = "--repo-root",
                        shape: str = "") -> str | None:
    """The operator-facing refusal for a `flag` value that is not a corpus
    checkout, or None when it is one.

    It names the RESOLVED ABSOLUTE path it checked and WHAT it looked for, because
    the mistake it exists to catch is a path that looks right and resolves
    somewhere else. `shape` is the CALLER's own correct invocation, appended
    verbatim — placeholders only: a real home directory or a container path in
    this message would be the very confusion the refusal is ending."""
    defect = corpus_scan_defect(repo_root)
    if defect is None:
        return None
    try:
        resolved: Path | str = Path(repo_root).resolve()
    except OSError:  # pragma: no cover - resolve() is non-strict; belt and braces
        resolved = repo_root
    roots = ", ".join(f"{root}/" for root in SCANNED_ROOTS)
    lines = [
        f"{flag} is not a corpus checkout: {defect}",
        f"  checked      {resolved}",
        f"  looked for   a directory holding at least one of {roots}",
        "               (the roots a snapshot is projected from)",
        f"  {flag} must name the SERVED CHECKOUT itself: the corpus tree whose",
        "  documents, staged topics and changes the snapshot projects. It is not",
        "  the aggregation root above that tree, and it is not the same path in",
        "  another filesystem namespace — a path that resolves inside a container",
        "  does not resolve on the host, or the reverse. Resolve it where THIS",
        "  command runs.",
    ]
    if shape:
        lines.append("  a correct invocation has this shape:")
        lines.extend(f"    {line}" for line in shape.strip().splitlines())
    return "\n".join(lines)
