"""Corpus discovery and document metadata for the doc-health suite.

TWO document sets, declared here and deliberately kept distinct
(`govern-openspec-corpus-membership`, ruled 2026-08-23):

The **governed corpus** (`GOVERNED_ROOTS`, `load_docs`) follows the staged
status-check rules (openxFactory
ideation/staging/doc-health-checks/status-check-rules.md): governance
Markdown lives under docs/, templates/, contracts/, examples/, and
ideation/. Promoted specs (openspec/specs/*/spec.md) are counted toward
canon but checked only by the families that name them. `tests/` and
`installs/` (nested submodules) are never scanned. It is the SOLE input to
the per-stage census, the governance and canon word totals, the canon-share
headline, the shared inventory, and the document catalog.

The **lifecycle scan set** (`LIFECYCLE_SCAN`, `load_lifecycle_docs`) is a
separately declared set of paths that carry lifecycle headers OUTSIDE the
governed corpus: each OpenSpec change packet's `proposal.md` and each
`review/` record. It is read by exactly four families — status validity,
standard backing, ratified provenance, succession integrity — and by nothing
else. It never enters `load_docs`, so no census, word total, canon-share
figure, inventory entry, or catalog record moves because it exists. That
invariance is the claim the ruled option rests on, and it is measured by
test rather than asserted here.
"""

from __future__ import annotations

import re
import subprocess
from dataclasses import dataclass
from datetime import date
from pathlib import Path

from .lines import split_keepends

GOVERNED_ROOTS = ("contracts", "docs", "examples", "ideation", "templates")

# The lifecycle scan set, declared as an EXPLICIT PATTERN SET rather than as a
# directory (`govern-openspec-corpus-membership`, OQ-2 ruled these two globs).
# A directory would have swept in `tasks.md`, `design.md`, the spec deltas,
# `supporting-docs/` and `evidence/` — 488 of the 536 `status-validity` fires
# the full-membership option measured — and whether those are governance
# documents is a question the ruling explicitly left open (§6.1).
#
# `**` matches zero or more directories, so the first pattern reaches both an
# active packet (`openspec/changes/<id>/proposal.md`) and an archived one
# (`openspec/changes/archive/<dated-id>/proposal.md`); the second reaches both
# packets' `review/` records.
#
# DISCLOSED BOUNDARY, measured rather than assumed: the first pattern matches a
# file named `proposal.md` at ANY depth under `openspec/changes/`, so a
# byte-exact snapshot stored as `<packet>/supporting-docs/source-snapshots/
# proposal.md` would enter the set, which the capability's "byte-exact
# evidence" scenario says it must not. Zero such files exist in this corpus
# (measured at the enforcement commit: 124 scan-set documents, none under
# `supporting-docs/`, `source-snapshots/` or `evidence/` — snapshots are named
# after the fragment they preserve, never `proposal.md`). Narrowing the ruled
# pattern to close a gap nothing occupies would be re-ruling OQ-2 in code, so
# the boundary is stated here instead: if a snapshot ever takes that name, this
# tuple is the line to change, under a governed change that measures the effect.
LIFECYCLE_SCAN = (
    "openspec/changes/**/proposal.md",
    "openspec/changes/**/review/*.md",
)

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
# plus an UNBOUNDED sibling defect the `splitlines()[:` grep pattern does not
# match: `scripts/doc_health/families.py`'s `_scan_lines()`, a live second
# Python line rule (design Decision 2's fence-scanning hazard's line-splitting
# half) disagreeing with `round_trip.py` on any exotic-boundary heading
# fixture. `_scan_lines` is not the only such sibling in this corpus — see the
# SECOND SWEEP GAP note below for `families.py`'s OTHER unbounded scanner,
# `_template_gaps`, which remains open (tasks.md §7).
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
#
# SECOND SWEEP GAP (finding F4, focused re-verify, 2026-08-19). The
# `splitlines()\[:` grep above STILL missed
# `scripts/ideation_dashboard/completeness.py`'s `_has_header`: it reads the
# window through `_Prepared.lines[:HEADER_WINDOW]`, where `_Prepared.lines`
# is assigned `text.splitlines()` in `__init__` — the split call and the
# window slice sit on DIFFERENT lines of source, so a grep for the two
# tokens adjacent (`splitlines()\[:`) cannot match either one. Demonstrated:
# `authoring.missing_required_headers` (already converted) said a header
# block was COMPLETE while `completeness`'s `governance_header_block` check
# (not yet converted) said ABSENT, on the SAME exotic-separator document.
# Converted now (`_Prepared.lines` itself, coherently — every consumer of
# `.lines` already treated it as an opaque `Sequence[str]`, so nothing else
# in that module needed to change). THE NEXT SWEEP should grep bare
# `splitlines()` over document text generally, not just the `[:N]`-windowed
# idiom — an assignment-then-slice split defeats the narrower pattern, and
# `families.py`'s `_template_gaps` (deferred, see tasks.md §7 — NOT a
# lifecycle-header reader, so outside this change's every-reader clause) is
# a further instance of exactly that same blind spot, left for its own
# scope.


def load_docs(repo_name: str, repo_path: Path) -> list[Doc]:
    docs = []
    for rel in iter_doc_paths(repo_path):
        text = (repo_path / rel).read_text(encoding="utf-8", errors="replace")
        docs.append(Doc(repo_name, rel.as_posix(), text, parse_status(text),
                        parse_kind(text)))
    return docs


def iter_lifecycle_paths(repo_path: Path) -> list[Path]:
    """Resolve `LIFECYCLE_SCAN` against one repo, deduplicated and sorted.

    Shares `_excluded` with `iter_doc_paths` rather than re-deriving the
    exclusion rule: one path-segment blacklist, read the same way for both
    sets. A `set` because the two patterns could in principle name the same
    file, and a document counted twice would double every finding it carries.
    """
    paths: set[Path] = set()
    for pattern in LIFECYCLE_SCAN:
        for match in repo_path.glob(pattern):
            if not match.is_file():
                continue
            rel = match.relative_to(repo_path)
            if not _excluded(rel):
                paths.add(rel)
    return sorted(paths)


def load_lifecycle_docs(repo_name: str, repo_path: Path) -> list[Doc]:
    """The lifecycle scan set as `Doc`s, built exactly as `load_docs` builds
    the governed corpus.

    Same `Doc` shape, same `parse_status`/`parse_kind` readers — NOT a second
    header reader. `align-status-reader-to-real-lines` exists because this
    corpus grew seven of those and they disagreed with each other; a scan set
    read by an eighth would report defects the corpus does not have, or miss
    the ones it does. The only thing that differs from `load_docs` is which
    paths are collected.
    """
    docs = []
    for rel in iter_lifecycle_paths(repo_path):
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
