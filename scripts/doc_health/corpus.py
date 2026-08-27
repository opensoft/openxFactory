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
governed corpus: each OpenSpec change packet's `proposal.md` and EVERY
`review/` record under it — whatever that record's subject — minus any path
carrying a byte-exact-evidence segment (`EVIDENCE_PARTS`). It is read by
exactly four families — status validity,
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

# The root-level NEUTRAL PRODUCTS the aggregation pins as SIBLINGS of
# `openxFactory/` rather than under `xFactories/` — governed repositories whose
# aggregation-relative id is a bare name (DTN-022: a neutral product pins at the
# aggregation's neutral root). AUTHORITY for the allowlist; see
# `split-openxwallet-repo` design D11.
#
# AN ALLOWLIST, NOT A RULE, and the distinction is the whole decision. The rule
# "every root-level `.gitmodules` pin is a governed repository" is one line
# shorter and WRONG: it would enrol all nine `installs/*` runtime repositories as
# governed ideation repositories, each deriving its own `xf-ideation-<name>`
# book and each becoming resolvable-without-materialization for reference
# checking — the exact opposite of the `external` classification those pins are
# supposed to carry. The set of root-level neutral products is small, slow-moving
# and governance-visible, so naming it costs one line per product and buys an
# explicit admission decision every time.
#
# ORDER is alphabetical and load-bearing for nothing; membership is.
#
# `openAvatar` is admitted on the SAME footing as `openXwallet` and not as a
# courtesy: it has been a root-level ratified product for five months, and its
# absence from both widened sites is precisely the empirical proof (council
# `council-systems-architect.md` concern 4) that a root-level repository derives
# nothing automatically.
ROOT_LEVEL_GOVERNED_PRODUCTS = ("openAvatar", "openXwallet")

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
# The RULED PATTERNS ARE UNCHANGED (OQ-2, re-affirmed 2026-08-23 when the
# `review/` half was widened to every review record). The first pattern matches
# a file named `proposal.md` at ANY depth under `openspec/changes/`, so a
# byte-exact snapshot stored as `<packet>/supporting-docs/source-snapshots/
# proposal.md` would otherwise enter the set — which the capability's
# "byte-exact evidence" scenario states as a MUST NOT, not as an observation
# about how many such files happen to exist. The first cut disclosed that gap
# and left it open on the measurement that nothing occupied it; that was the
# wrong reading of a MUST. The membership rule is now enforced by
# `EVIDENCE_PARTS` below, which `iter_lifecycle_paths` applies as a segment
# filter AFTER the ruled globs resolve. The globs stay exactly as ruled; the
# evidence exclusion is a separate, separately-stated rule that the ruling's
# own scenario requires.
LIFECYCLE_SCAN = (
    "openspec/changes/**/proposal.md",
    "openspec/changes/**/review/*.md",
)

# Path segments that mark a document as byte-exact EVIDENCE rather than live
# prose (doc-health capability, "A document is byte-exact evidence rather than
# live prose"). A path carrying any of these is excluded from the lifecycle
# scan set even where it matches a ruled glob: reporting a frozen record for
# the state it preserves is a false finding, and the frozen record's whole
# value is that its bytes do not move to satisfy a checker.
#
# Deliberately NOT folded into `EXCLUDED_PARTS`: that blacklist governs BOTH
# document sets, and a `supporting-docs/` fragment is a legitimate governed
# document when it sits under a governed root. This one governs the lifecycle
# scan set alone.
EVIDENCE_PARTS = frozenset({"supporting-docs", "source-snapshots", "evidence"})

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


def _is_evidence(rel: Path) -> bool:
    """Byte-exact evidence, by path segment (see `EVIDENCE_PARTS`)."""
    return any(part in EVIDENCE_PARTS for part in rel.parts)


def iter_lifecycle_paths(repo_path: Path) -> list[Path]:
    """Resolve `LIFECYCLE_SCAN` against one repo, deduplicated and sorted,
    with byte-exact evidence filtered out.

    Shares `_excluded` with `iter_doc_paths` rather than re-deriving the
    exclusion rule: one path-segment blacklist, read the same way for both
    sets. `_is_evidence` is the SECOND filter and belongs to this set alone —
    the capability's "byte-exact evidence" scenario is a MUST NOT on
    MEMBERSHIP, so it is enforced here, at the point membership is decided,
    rather than left to the observation that no such file exists today.
    A `set` because the two patterns could in principle name the same
    file, and a document counted twice would double every finding it carries.
    """
    paths: set[Path] = set()
    for pattern in LIFECYCLE_SCAN:
        for match in repo_path.glob(pattern):
            if not match.is_file():
                continue
            rel = match.relative_to(repo_path)
            if not _excluded(rel) and not _is_evidence(rel):
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

    def first_commit_timestamp(self, repo: Path, relpath: str,
                               ref: str | None = None) -> int | None:
        """Committer epoch seconds of the commit that first added `relpath`.

        `first_commit_date` answers the same question to DAY resolution,
        which is exactly the resolution that cannot break a tie between two
        packets archived on the same day — the tie the promotion-fidelity
        family has to break (nineteen such tie groups in this repository).
        Same shape as its sibling: None whenever git cannot answer, so the
        caller falls back rather than crashing.

        `ref` walks a named commit instead of `HEAD`. The promotion-fidelity
        family's live-main basis reads a tree the checkout does not carry, and
        a tie broken by HEAD's history while the STATEMENTS came from
        `origin/main` would be two readers of two different trees agreeing by
        accident. Default None keeps every existing caller on HEAD.
        """
        args = ["log", "--reverse", "--format=%ct"]
        if ref:
            args.append(ref)
        out = self._run(repo, *args, "--", relpath)
        if not out:
            return None
        for line in out.splitlines():
            if line.strip():
                return int(line.strip())
        return None

    def resolve_ref(self, repo: Path, ref: str) -> str | None:
        """`ref`'s commit sha, or None where the checkout does not carry it.

        The honest answer to "is this basis available here?". A nightly that
        fetched `origin/main` gets a sha; a developer checkout that never
        fetched gets None, and the caller says so rather than pretending.
        """
        out = self._run(repo, "rev-parse", "--verify", "--quiet",
                        f"{ref}^{{commit}}")
        return out.strip() if out and out.strip() else None

    def ls_tree_paths(self, repo: Path, ref: str,
                      prefix: str) -> list[str] | None:
        """Every blob path under `prefix` in `ref`'s tree, or None on failure.

        NUL-delimited (`-z`) so a path containing a quote or a non-ASCII byte
        arrives whole instead of arriving as git's C-style quoted spelling —
        the reader would otherwise silently miss exactly the documents whose
        names it cannot spell back.

        ROOT-RELATIVE ON BOTH AXES, and neither is git's default. `ls-tree`
        resolves its pathspec against the CURRENT PREFIX and prints paths
        relative to it, while `git show <ref>:<path>` always reads from the
        tree ROOT. Called with a `repo` that is a subdirectory of a checkout,
        the untuned pair therefore lists one subtree and reads another —
        silently, and with plausible-looking output. `--full-name` fixes the
        printing and the `:(top)` pathspec magic fixes the matching, so a
        listing and a read of the same name mean the same file wherever the
        caller points this.
        """
        out = self._run(repo, "ls-tree", "-r", "--full-name", "--name-only",
                        "-z", ref, "--", f":(top){prefix}")
        if out is None:
            return None
        return [p for p in out.split("\0") if p]

    def show_blob(self, repo: Path, ref: str, relpath: str) -> str | None:
        """`relpath`'s content at `ref`, or None where it is not there."""
        return self._run(repo, "show", f"{ref}:{relpath}")

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

    # ---- release-surface readers (add-release-inventory-drift-check) ----
    #
    # BOTH RETURN RAW BYTES OR MODES, NEVER DECODED TEXT. Every reader above
    # runs `_run`, which passes `text=True` and therefore applies universal
    # newlines — a blob committed with CRLF comes back with LF, different bytes
    # and a different SHA-256. The release digest identity is "the SHA-256 of
    # the raw Git blob bytes", and the versioning policy names text
    # canonicalization an INVALID digest source, so a text-mode read here would
    # not merely be imprecise: it would compute a number the contract forbids.
    #
    # Both degrade to None on ANY git failure, which the caller reads as "git
    # could not be consulted" and turns into a skip. A path that is simply
    # ABSENT at the commit is NOT a failure and must not look like one — that
    # is why `tree_modes` returns a mapping (absence is a missing key) rather
    # than raising, and why `blobs_at` reports per-path absence in its result.

    def tree_modes(self, repo: Path, commit: str) -> dict[str, str] | None:
        """`{path: git_mode}` for every regular file at `commit`, or None.

        One `ls-tree -r` rather than a call per member: the inventories this
        serves carry ~190 entries, and per-path process spawning is the
        difference between a family that runs in the nightly and one nobody
        keeps."""
        out = self._run(repo, "ls-tree", "-r", commit)
        if out is None:
            return None
        modes: dict[str, str] = {}
        for line in out.splitlines():
            meta, _, path = line.partition("\t")
            parts = meta.split()
            if path and len(parts) >= 3:
                modes[path] = parts[0]
        return modes

    def blobs_at(self, repo: Path, commit: str,
                 relpaths) -> dict[str, bytes | None] | None:
        """`{path: raw bytes}` at `commit`, with None for a path ABSENT there.

        One `cat-file --batch` process for the whole member set. The batch
        protocol answers a missing object with `<spec> missing`, which is
        exactly the distinction the contract needs: absence is data, and only a
        failure of git itself collapses to None."""
        specs = list(relpaths)
        if not specs:
            return {}
        payload = "\n".join(f"{commit}:{p}" for p in specs) + "\n"
        try:
            proc = subprocess.run(
                ["git", "-C", str(repo), "cat-file", "--batch"],
                input=payload.encode("utf-8"), capture_output=True)
        except OSError:
            return None
        if proc.returncode != 0:
            return None
        out: dict[str, bytes | None] = {}
        buf = proc.stdout
        pos = 0
        for spec in specs:
            nl = buf.find(b"\n", pos)
            if nl < 0:
                return None
            header = buf[pos:nl].decode("utf-8", "replace")
            pos = nl + 1
            if header.endswith(" missing") or header.endswith(" ambiguous"):
                # `ambiguous` FOLDS INTO ABSENCE, and that is a deliberate
                # narrowing rather than an oversight (PR review P3-3). git
                # answers `ambiguous` for a bare name that could be several
                # objects; every spec this reader sends is a fully-qualified
                # `<commit>:<path>`, which cannot be ambiguous. The branch
                # exists so an unexpected answer degrades to "not there" rather
                # than desynchronising the batch parser, and if it ever fires it
                # will surface as drift on a member — loud, in the right place.
                out[spec] = None
                continue
            fields = header.split()
            if len(fields) < 3 or not fields[2].isdigit():
                return None
            size = int(fields[2])
            out[spec] = buf[pos:pos + size]
            pos += size + 1  # the trailing newline the batch protocol adds
        return out

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
