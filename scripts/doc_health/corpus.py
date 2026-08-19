"""Corpus discovery and document metadata for the doc-health suite.

Governed roots follow the staged status-check rules (openxFactory
ideation/staging/doc-health-checks/status-check-rules.md): governance
Markdown lives under docs/, templates/, contracts/, examples/, and
ideation/. Promoted specs (openspec/specs/*/spec.md) are counted toward
canon but checked only by the families that name them. `tests/` and
`installs/` (nested submodules) are never scanned.
"""

from __future__ import annotations

import re
import subprocess
from dataclasses import dataclass
from datetime import date
from pathlib import Path

from .lines import split_keepends

GOVERNED_ROOTS = ("contracts", "docs", "examples", "ideation", "templates")
EXCLUDED_PARTS = {".git", "installs", "node_modules", "tests", "__pycache__"}
STATUS_RE = re.compile(r"^Status:\s*(.+?)\s*$")
STATUS_SCAN_LINES = 15


@dataclass
class Doc:
    repo: str
    path: str          # repo-relative, posix
    text: str
    status: str | None  # raw header value, None if absent
    kind: str | None = None  # Kind: header value, None if absent

    @property
    def words(self) -> int:
        return len(self.text.split())


def discover_repos(repo_root: Path) -> list[tuple[str, Path]]:
    """Family repos inside an aggregation checkout: openxFactory plus every
    xFactories/* the aggregation repo pins."""
    repos: list[tuple[str, Path]] = []
    openx = repo_root / "openxFactory"
    if openx.is_dir():
        repos.append(("openxFactory", openx))
    factories = repo_root / "xFactories"
    if factories.is_dir():
        for child in sorted(factories.iterdir()):
            if child.is_dir() and (child / ".git").exists():
                repos.append((child.name, child))
    return repos


def _excluded(rel: Path) -> bool:
    return any(part in EXCLUDED_PARTS for part in rel.parts)


def iter_doc_paths(repo_path: Path) -> list[Path]:
    paths: list[Path] = []
    for root in GOVERNED_ROOTS:
        base = repo_path / root
        if not base.is_dir():
            continue
        for md in base.rglob("*.md"):
            rel = md.relative_to(repo_path)
            if not _excluded(rel):
                paths.append(rel)
    return sorted(paths)


def parse_status(text: str) -> str | None:
    """Locate the `Status:` header within the first REAL lines of `text`.

    Scans real lines (CR/LF/CRLF only — see `doc_health.lines`) rather than
    `str.splitlines()` fragments, so a header carrying an exotic separator
    (form feed, U+2028, ...) does not inflate the scan window and hide a
    `Status:` line that is plainly there. A reader more aggressive than the
    writer can otherwise report a correct document as lacking a status it
    carries — a false finding (`align-status-reader-to-real-lines`).
    """
    for body, _ending in split_keepends(text)[:STATUS_SCAN_LINES]:
        m = STATUS_RE.match(body)
        if m:
            return m.group(1)
    return None


def parse_kind(text: str) -> str | None:
    """`Kind:` header, scanned the same real-line way as `parse_status`.

    Shares the blindness `parse_status` used to have (both scanned
    `text.splitlines()[:STATUS_SCAN_LINES]`), so it shares the fix.
    """
    for body, _ending in split_keepends(text)[:STATUS_SCAN_LINES]:
        if body.startswith("Kind: "):
            return body[len("Kind: "):].strip() or None
    return None


# SWEEP RECORD (align-status-reader-to-real-lines, task 2.3), UPDATED under
# the wide ruling. `grep -rn "splitlines()\[:" scripts/` was run against this
# fix so the next reader does not have to re-run it to know whether
# `parse_status`/`parse_kind` were the whole set. They were not: the same
# `text.splitlines()[:N]` idiom was also carried, independently, by:
#   scripts/ideation_dashboard/doxbench_packet.py  lifecycle_status()
#   scripts/ideation_dashboard/authoring.py        missing_required_headers()
#   scripts/ideation_dashboard/generator.py        _header_value()
#   scripts/doc_health/inventory.py                _header_value()
#   scripts/doc_health/families.py                 _header_line()
#   scripts/doc_health/organizer_dispatch.py       _header_value()
# plus one UNBOUNDED sibling defect the `splitlines()[:` grep pattern does not
# match: `scripts/doc_health/families.py`'s `_scan_lines()`, a live second
# Python line rule (design Decision 2's fence-scanning hazard's line-splitting
# half) disagreeing with `round_trip.py` on any exotic-boundary heading
# fixture.
#
# First cut of this change scoped its ratified `proposal.md` code surface to
# `lines.py` + `parse_status`/`parse_kind` + `round_trip.py`'s import alone,
# and left the six sites above untouched, reasoning that widening would mean
# presenting an unmeasured baseline diff. Brett's same-day ruling (in-session
# multiple choice, recommended option adopted, 2026-08-19) found that
# reasoning was the drafting error, not the delta: the delta's "SHALL hold for
# every reader of that header" and the proposal's "reduces the Python side to
# one" already governed every reader, and the narrow front-matter enumeration
# was corrected to match. The measurement the narrow cut said it lacked was
# then taken — 1227 governed aggregation files, zero exotic separators, zero
# window differences, zero value changes — so ALL SIX sites plus `_scan_lines`
# convert in THIS change, on a demonstrated zero baseline cost. See
# `proposal.md`'s amended `code_surface:` and `Ratified:` lines for the ruling
# in full.


def load_docs(repo_name: str, repo_path: Path) -> list[Doc]:
    docs = []
    for rel in iter_doc_paths(repo_path):
        text = (repo_path / rel).read_text(encoding="utf-8", errors="replace")
        docs.append(Doc(repo_name, rel.as_posix(), text, parse_status(text),
                        parse_kind(text)))
    return docs


def promoted_spec_paths(repo_path: Path) -> list[Path]:
    base = repo_path / "openspec" / "specs"
    if not base.is_dir():
        return []
    return sorted(base.glob("*/spec.md"))


def spec_capabilities(repo_path: Path) -> set[str]:
    caps = {p.parent.name for p in promoted_spec_paths(repo_path)}
    changes = repo_path / "openspec" / "changes"
    if changes.is_dir():
        for change in changes.iterdir():
            if change.name == "archive" or not change.is_dir():
                continue
            for spec in change.glob("specs/*/spec.md"):
                caps.add(spec.parent.name)
    return caps


def change_ids(repo_path: Path) -> set[str]:
    ids: set[str] = set()
    changes = repo_path / "openspec" / "changes"
    if not changes.is_dir():
        return ids
    for child in changes.iterdir():
        if child.is_dir() and child.name != "archive":
            ids.add(child.name)
    archive = changes / "archive"
    if archive.is_dir():
        for child in archive.iterdir():
            if child.is_dir():
                ids.add(child.name)
                # archived folders are date-prefixed: YYYY-MM-DD-<id>
                m = re.match(r"\d{4}-\d{2}-\d{2}-(.+)", child.name)
                if m:
                    ids.add(m.group(1))
    return ids


class RealGit:
    """Git-derived facts. Every method degrades to None on failure so
    families can skip-with-notice instead of crashing."""

    def _run(self, repo: Path, *args: str) -> str | None:
        proc = subprocess.run(["git", "-C", str(repo), *args],
                              capture_output=True, text=True)
        return proc.stdout if proc.returncode == 0 else None

    def last_commit_date(self, repo: Path, relpath: str) -> date | None:
        out = self._run(repo, "log", "-1", "--format=%cs", "--", relpath)
        return date.fromisoformat(out.strip()) if out and out.strip() else None

    def first_commit_date(self, repo: Path, relpath: str) -> date | None:
        """When `relpath` first appeared — its staging date, not its last touch.

        The template-conformance family needs this and NOT `last_commit_date`:
        a topic staged before the template ratified is opt-in, and editing it
        for an unrelated reason must not silently make it required. Age uses
        the last touch; obligation uses the first.
        """
        out = self._run(repo, "log", "--reverse", "--format=%cs", "--", relpath)
        if not out:
            return None
        for line in out.splitlines():
            if line.strip():
                return date.fromisoformat(line.strip())
        return None

    def line_commit_date(self, repo: Path, relpath: str, line: int) -> date | None:
        out = self._run(repo, "blame", "--porcelain",
                        f"-L{line},{line}", "--", relpath)
        if not out:
            return None
        for row in out.splitlines():
            if row.startswith("committer-time "):
                from datetime import datetime, timezone
                ts = int(row.split()[1])
                return datetime.fromtimestamp(ts, tz=timezone.utc).date()
        return None

    def capture_blob(self, repo: Path, relpath: str, predicate) -> str | None:
        """Earliest blob of relpath whose text satisfies predicate."""
        out = self._run(repo, "log", "--reverse", "--format=%H", "--", relpath)
        if not out:
            return None
        for sha in out.split():
            blob = self._run(repo, "show", f"{sha}:{relpath}")
            if blob is not None and predicate(blob):
                return blob
        return None

    def gitlink_pins(self, agg_root: Path) -> dict[str, str] | None:
        out = self._run(agg_root, "ls-tree", "-r", "HEAD")
        if out is None:
            return None
        pins = {}
        for row in out.splitlines():
            meta, _, path = row.partition("\t")
            parts = meta.split()
            if len(parts) == 3 and parts[1] == "commit":
                pins[path] = parts[2]
        return pins

    def remote_main_sha(self, repo: Path) -> str | None:
        out = self._run(repo, "ls-remote", "origin", "refs/heads/main")
        if out and out.strip():
            return out.split()[0]
        return None

    def head_sha(self, repo: Path) -> str | None:
        out = self._run(repo, "rev-parse", "HEAD")
        return out.strip() if out else None
