"""The `scope_globs:` structured path-scope substrate (release-realization).

Realizes the `release-realization` capability's structured-scope requirements
added by `add-structured-scope-substrate`:

  * "Structured path-scope declaration" — the OPTIONAL front-matter sibling
    field `scope_globs:`, a MAPPING from repository name to a non-empty list of
    repository-relative globs in the merge-gate ENVELOPE DIALECT.
  * "Structured path-scope validation" — well-formedness + dialect conformance,
    FLOOR-AGNOSTIC (this module never rejects a glob because it happens to name a
    floor path; the floor is applied at CHECK time by the downstream verifier).
  * "Scope retention at archive" — the freeze: `scope_globs` bytes may not change
    between ratification and archive.

ABSENCE IS FAIL-CLOSED. A change with no `scope_globs`, or with no entry for a
given repository, is simply NOT provenance-eligible for that repository. Absence
is NEVER interpreted as "all paths".

THE FIELD IS READ THROUGH THE SHARED STRICT LOADER, NOT `yaml.safe_load`.
`scripts/frontmatter_strict.py` is the ONE loader for the realization-axis
front-matter block, over BOTH its structured fields (`scope_globs:` and
`sequenced_after:`). It refuses — rather than silently resolves — duplicate keys
at any level, anchors, aliases, merge keys, non-UTF-8 bytes, YAML directives,
more than one document, and a block over the declared byte ceiling. This module
originally parsed the sub-block with `yaml.safe_load`, whose
LAST-DUPLICATE-KEY-WINS behaviour let a proposal carrying two `scope_globs:`
blocks show a reviewer the FIRST and authorize the LAST. The retrofit was
ratified by convener ruling OQ-1 of `add-sequenced-after-substrate` (2026-09-01)
— fix inside that change, because a strict loader with a documented hole in one
field of a trust-root surface is not a strict loader. **It changes how the field
is LOADED and never what it MEANS:** every shape, dialect, cross-consistency and
retention rule below is untouched, and the shipped corpus validates
byte-identically after the swap (asserted by
`tests/scope_globs/test_strict_loader.py`).

THE GLOB DIALECT IS NOT REDEFINED HERE. The single glob authority is the
codexFactory merge-gate envelope, `scripts/merge_master/envelope.py`
(`_glob_to_regex`, `path_matches`, `_validate_path_allowlist`,
`_UNIVERSAL_PATTERNS`, `_COMPLEMENT_KEYS`). The verifier's containment check and
the never-clearable floor check both use that one engine, so they cannot
disagree. openxFactory cannot import that module (it lives in a sibling submodule
whose pin is stale and which is not vendored into openxFactory's CI tree), so the
dialect is MIRRORED here byte-for-behaviour and pinned in lockstep by
`tests/scope_globs/test_dialect_lockstep.py`. The mirror was transcribed from the
live codexFactory checkout at HEAD `3143f34d` (glob region last changed at
`9ebe805`, `add-regular-pr-council-clearance`). If the envelope engine ever
changes its dialect, this mirror MUST be updated in the same lockstep and its
pinning test refreshed against the new authority.

Deterministic: text/YAML reads only, no model calls, no writes.
"""

from __future__ import annotations

import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Mapping

sys.path.insert(0, str(Path(__file__).resolve().parent))

import frontmatter_strict as fms  # noqa: E402  (self-locating sibling import)


class ScopeGlobsError(Exception):
    """Raised when a `scope_globs` declaration is malformed or non-dialect.

    The message names the offending entry and the rule it breaks, so a
    `openspec validate --strict`-equivalent house run can report it directly.
    """


# --- front-matter reading ----------------------------------------------------
#
# Delegated to the SHARED strict loader (`scripts/frontmatter_strict.py`). The
# fence split, the prose-header/structured-field split and the per-field strict
# parse all live there, so `scope_globs:` and `sequenced_after:` cannot be read
# by two loaders that disagree. This module keeps its own error type: a caller
# catching `ScopeGlobsError` keeps catching every refusal this reader can raise.


def read_front_matter(source: str | bytes | Path) -> dict:
    """Return the realization-axis front-matter of a `proposal.md` as a dict.

    Accepts document text, bytes, or a path. The STRUCTURED fields
    (`scope_globs`, `sequenced_after`) are read from their own sub-blocks through
    the STRICT loader and returned as their structured values; every other field
    is returned as its raw joined string (prose headers are not YAML). Returns an
    empty dict when there is no well-formed front-matter fence. Raises
    `ScopeGlobsError` for any strict-loader refusal, with the loader's message.
    """
    try:
        return fms.read_front_matter(source)
    except fms.StrictFrontMatterError as exc:
        raise ScopeGlobsError(str(exc)) from exc


def read_scope_globs(proposal: str | Path) -> object | None:
    """Return the RAW `scope_globs` value from a proposal, or None when absent.

    Absence (the field is missing) returns None — the fail-closed default. A
    present-but-shape-malformed value is returned as-is for `validate_shape` to
    reject; only YAML that does not parse at all raises here.
    """
    return read_front_matter(proposal).get("scope_globs")


# --- schema / shape ----------------------------------------------------------


@dataclass(frozen=True)
class ScopeGlobs:
    """A validated `scope_globs` declaration: repository -> tuple of globs."""

    by_repo: Mapping[str, tuple[str, ...]]

    def repositories(self) -> tuple[str, ...]:
        return tuple(self.by_repo)

    def globs_for(self, repository: str) -> tuple[str, ...]:
        """The globs declared for `repository`, or an empty tuple when the
        repository has no entry (not provenance-eligible)."""
        return self.by_repo.get(repository, ())


def validate_shape(scope: object) -> ScopeGlobs:
    """Validate the STRUCTURE of a `scope_globs` value and return a `ScopeGlobs`.

    Shape contract (per the "Structured path-scope declaration" requirement): a
    non-empty MAPPING of non-empty string repository-key to a non-empty list of
    non-empty, UNIQUE strings. Raises `ScopeGlobsError` naming the offending
    entry otherwise. Dialect conformance is a SEPARATE concern (see
    `validate_dialect`); this function checks only the container shape.
    """
    if not isinstance(scope, dict):
        raise ScopeGlobsError(
            "scope_globs must be a mapping of repository name to a list of "
            f"globs, not {type(scope).__name__}")
    if not scope:
        raise ScopeGlobsError(
            "scope_globs is present but empty; omit the field entirely to declare "
            "no structured scope (absence is the fail-closed default)")
    by_repo: dict[str, tuple[str, ...]] = {}
    for repo, globs in scope.items():
        if not isinstance(repo, str) or not repo:
            raise ScopeGlobsError(
                f"scope_globs repository key {repo!r} must be a non-empty string")
        if not isinstance(globs, list) or not globs:
            raise ScopeGlobsError(
                f"scope_globs[{repo}] must be a non-empty list of globs")
        for entry in globs:
            if not isinstance(entry, str) or not entry:
                raise ScopeGlobsError(
                    f"scope_globs[{repo}] entries must be non-empty strings; "
                    f"found {entry!r}")
        if len(set(globs)) != len(globs):
            raise ScopeGlobsError(
                f"scope_globs[{repo}] entries must be unique")
        by_repo[repo] = tuple(globs)
    return ScopeGlobs(by_repo=by_repo)


# --- the MIRRORED envelope glob dialect --------------------------------------
#
# Transcribed byte-for-behaviour from codexFactory
# `scripts/merge_master/envelope.py` and pinned in lockstep by
# `tests/scope_globs/test_dialect_lockstep.py`. See the module docstring for the
# authority's provenance (HEAD 3143f34d, glob region 9ebe805). Keep the names,
# the tuples, and the rejection order identical to the authority.

#: Keys whose very presence declares a surface as the COMPLEMENT of another set
#: ("everything except …"). Refused outright: a complement fails open. Mirror of
#: `envelope._COMPLEMENT_KEYS`.
COMPLEMENT_KEYS = (
    "path_denylist", "path_blocklist", "path_exclusions", "exclude_paths",
    "except_paths", "path_complement", "not_paths", "path_exclude",
    "codeowners_complement",
)

#: Globs that admit every path — the complement of the empty set, which would
#: leave the never-clearable floor the only remaining control. Mirror of
#: `envelope._UNIVERSAL_PATTERNS`.
UNIVERSAL_PATTERNS = ("**", "*", "**/*", "/**", "./**")


def glob_to_regex(pattern: str) -> re.Pattern[str]:
    """Translate a repository-relative path glob to an anchored full-match regex.

    Mirror of `envelope._glob_to_regex`: `**` matches any number of path
    segments including zero, `*` a run of non-separator characters within a
    segment, `?` one non-separator. Byte-for-behaviour identical, pinned by the
    lockstep test.
    """
    i = 0
    out: list[str] = ["^"]
    n = len(pattern)
    while i < n:
        c = pattern[i]
        if c == "*":
            if i + 1 < n and pattern[i + 1] == "*":
                i += 2
                if i < n and pattern[i] == "/":
                    i += 1
                    out.append("(?:[^/]+/)*")
                else:
                    out.append(".*")
            else:
                out.append("[^/]*")
                i += 1
        elif c == "?":
            out.append("[^/]")
            i += 1
        else:
            out.append(re.escape(c))
            i += 1
    out.append("$")
    return re.compile("".join(out))


def path_matches(path: str, patterns: Iterable[str]) -> bool:
    """True when `path` matches at least one glob. Mirror of
    `envelope.path_matches`."""
    return any(glob_to_regex(p).match(path) is not None for p in patterns)


def validate_glob(where: str, pattern: str) -> None:
    """Reject the envelope-forbidden forms for a single glob, in the authority's
    order (negation, universal, leading-slash), then require it compiles under
    the shared engine. Mirror of the per-pattern arm of
    `envelope._validate_path_allowlist`."""
    if pattern.startswith("!"):
        raise ScopeGlobsError(
            f"{where} entry {pattern!r} is a negation; the envelope glob dialect "
            f"has none, and a surface expressed by subtraction is a complement "
            f"that fails open")
    if pattern in UNIVERSAL_PATTERNS:
        raise ScopeGlobsError(
            f"{where} entry {pattern!r} admits every path, which is the "
            f"complement of the empty set — declare the paths the scope admits")
    if pattern.startswith("/"):
        raise ScopeGlobsError(
            f"{where} entry {pattern!r} starts with '/'; changed paths are "
            f"repository-relative and never do, so the pattern is unreachable "
            f"(the CODEOWNERS dialect is not this one)")
    try:
        glob_to_regex(pattern)
    except re.error as exc:  # pragma: no cover - the dialect cannot produce this
        raise ScopeGlobsError(
            f"{where} entry {pattern!r} does not compile under the envelope "
            f"dialect: {exc}") from exc


def validate_dialect(scope: ScopeGlobs) -> None:
    """Reject complement/denylist-shaped repository keys, then dialect-check
    every glob. FLOOR-AGNOSTIC: a glob that happens to name a floor path is NOT
    rejected here (the floor override is a check-time concern of the verifier)."""
    for repo in scope.by_repo:
        if repo in COMPLEMENT_KEYS:
            raise ScopeGlobsError(
                f"scope_globs key {repo!r} is a complement/denylist-shaped key; "
                f"a scope is an explicit allowlist, never the complement of "
                f"another set — a complement fails open")
    for repo, globs in scope.by_repo.items():
        for pattern in globs:
            validate_glob(f"scope_globs[{repo}]", pattern)


def validate_cross_consistency(
    scope: ScopeGlobs, code_surface_repos: Iterable[str]
) -> None:
    """Every `scope_globs` repository key MUST be named in `code_surface`; the
    reverse is NOT required (a code_surface repo may carry no scope and is then
    simply not provenance-eligible)."""
    declared = set(code_surface_repos)
    for repo in scope.by_repo:
        if repo not in declared:
            raise ScopeGlobsError(
                f"scope_globs names repository {repo!r} which is not in "
                f"code_surface; a scope may not authorize a repository the change "
                f"declares no realization surface for")


def validate_scope_globs(
    scope: object, code_surface_repos: Iterable[str] | None = None
) -> ScopeGlobs:
    """Full validation of a raw `scope_globs` value: shape, dialect conformance,
    and (when `code_surface_repos` is given) cross-consistency. Returns the
    validated `ScopeGlobs`. FLOOR-AGNOSTIC throughout."""
    validated = validate_shape(scope)
    validate_dialect(validated)
    if code_surface_repos is not None:
        validate_cross_consistency(validated, code_surface_repos)
    return validated


def code_surface_repositories(front_matter: Mapping[str, object]) -> set[str]:
    """Best-effort set of repository tokens named in the `code_surface` header.

    `code_surface` is prose (ratified as repository-granularity free text), so
    this extracts bare repository-name tokens for the cross-consistency check:
    every whitespace/comma/parenthesis-separated word that looks like a repo
    name. `none` yields the empty set. It is intentionally permissive — the
    cross-consistency check only needs to confirm a scope key APPEARS in the
    prose, and a false accept here is caught by the human ratification read, while
    a false reject would wrongly gate a valid scope."""
    raw = front_matter.get("code_surface")
    if not isinstance(raw, str):
        return set()
    tokens = re.split(r"[\s,()/]+", raw)
    return {t for t in tokens if t and t != "none"}


# --- scope retention at archive (the FREEZE) ---------------------------------
#
# Mirrors the "Origin retention at archive" gate (release-realization): a
# ratified declaration is auditable and immutable, so a change cannot silently
# widen the paths its realization was authorized to touch between ratification and
# archive. Realizes the FROZEN-AFTER-RATIFICATION property of the trust-root
# integrity requirement. Contested class: reversing this reverses a gate decision.


def _canonical(scope: object) -> object:
    """A comparable, order-insensitive-over-repos canonical form of a raw
    `scope_globs` value. None stays None; a well-formed value becomes a sorted
    tuple of (repo, glob-tuple) pairs; an unparseable value becomes a sentinel so
    that a mutation INTO malformed shape still registers as a change rather than
    crashing the gate."""
    if scope is None:
        return None
    try:
        by_repo = validate_shape(scope).by_repo
    except ScopeGlobsError:
        return ("__unparseable__", repr(scope))
    return tuple(sorted((repo, by_repo[repo]) for repo in by_repo))


def scope_retention_problem(ratified: object, current: object) -> str | None:
    """Return a contested-class problem string when `current` differs from the
    `ratified` `scope_globs` declaration, or None when unchanged.

    Both may be None (no scope declared — the common case, trivially retained).
    Adding, removing, widening, or reordering the declaration after ratification
    all register as mutations. Glob-list ORDER is significant (the frozen
    declaration is compared as authored); repository-key order is not."""
    if _canonical(ratified) == _canonical(current):
        return None
    return (
        f"scope_globs was mutated after ratification (ratified: {ratified!r}; "
        f"current: {current!r}); a ratified scope is frozen — restoring or "
        f"accepting the mutation is a contested-class act requiring an explicit "
        f"disposition"
    )


def _git_toplevel(path: Path) -> Path:
    out = subprocess.run(
        ["git", "-C", str(path if path.is_dir() else path.parent),
         "rev-parse", "--show-toplevel"],
        capture_output=True, text=True, check=True,
    )
    return Path(out.stdout.strip())


def scope_globs_at_ref(repo_root: Path, ref: str, proposal_rel: str) -> object | None:
    """Read the `scope_globs` value from `proposal_rel` as it stood at git `ref`
    (the ratified snapshot). Returns None when the field is absent at that ref."""
    out = subprocess.run(
        ["git", "-C", str(repo_root), "show", f"{ref}:{proposal_rel}"],
        capture_output=True, text=True, check=True,
    )
    return read_scope_globs(out.stdout)


def scope_retention_at_archive(change_dir: str | Path, ratified_ref: str) -> str | None:
    """Archive-gate freeze check for one change directory.

    Reads `scope_globs` from the change's `proposal.md` at `ratified_ref` (the
    ratified snapshot) and from the current working tree, and returns a
    contested-class problem string if they differ (None when retained). Mirrors
    the origin-retention gate's compare-recorded-vs-live mechanism via git object
    reads."""
    change_path = Path(change_dir)
    proposal = change_path / "proposal.md"
    repo_root = _git_toplevel(change_path)
    proposal_rel = proposal.resolve().relative_to(repo_root.resolve()).as_posix()
    ratified = scope_globs_at_ref(repo_root, ratified_ref, proposal_rel)
    current = read_scope_globs(proposal) if proposal.is_file() else None
    return scope_retention_problem(ratified, current)
