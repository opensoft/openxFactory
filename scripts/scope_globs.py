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

from dataclasses import dataclass
from pathlib import Path
from typing import Mapping

try:
    import yaml
except ImportError:  # pragma: no cover - pyyaml is a suite dependency
    yaml = None


class ScopeGlobsError(Exception):
    """Raised when a `scope_globs` declaration is malformed or non-dialect.

    The message names the offending entry and the rule it breaks, so a
    `openspec validate --strict`-equivalent house run can report it directly.
    """


# --- front-matter reading ----------------------------------------------------


_FENCE = "---"


def read_front_matter(source: str | Path) -> dict:
    """Return the YAML front-matter mapping of a `proposal.md`.

    Accepts either the document text or a path to it. The realization-axis block
    (`code_surface:` / `target_release:` / the new `scope_globs:` sibling) lives
    in the leading `---`-fenced YAML block; this is the one place the block is
    parsed for structured (non-flat) fields. Returns an empty dict when the
    document carries no front-matter fence.
    """
    if yaml is None:  # pragma: no cover
        raise ScopeGlobsError("pyyaml is required to read proposal front-matter")
    if isinstance(source, Path):
        text = source.read_text(encoding="utf-8")
    else:
        text = source
    lines = text.splitlines()
    if not lines or lines[0].strip() != _FENCE:
        return {}
    body: list[str] = []
    for line in lines[1:]:
        if line.strip() == _FENCE:
            try:
                doc = yaml.safe_load("\n".join(body))
            except yaml.YAMLError as exc:
                raise ScopeGlobsError(f"proposal front-matter is not valid YAML: {exc}") from exc
            return doc if isinstance(doc, dict) else {}
        body.append(line)
    # No closing fence — not a well-formed front-matter block.
    return {}


def read_scope_globs(proposal: str | Path) -> object | None:
    """Return the RAW `scope_globs` value from a proposal, or None when absent.

    Absence (the field is missing) returns None — the fail-closed default. A
    present-but-malformed value is returned as-is for `validate_shape` to reject;
    this reader does not itself validate the shape.
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
