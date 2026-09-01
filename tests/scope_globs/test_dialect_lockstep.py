"""LOCKSTEP pin: the `scope_globs` glob dialect must not drift from the single
authority, codexFactory `scripts/merge_master/envelope.py`
(add-structured-scope-substrate task 3.5).

WHY A MIRROR, NOT AN IMPORT. `envelope.py` is the ONE glob engine the verifier's
containment check and the never-clearable floor both use, so `scope_globs`
validation must accept and reject EXACTLY what it does. openxFactory cannot import
that module — it lives in a sibling submodule whose openxFactory pin is stale and
which is not vendored into openxFactory's CI tree — and importing it only when a
sibling checkout happens to be present would make this pin SKIP on the CI runner,
which the `pytest-suite` gate pins to an exact skip count. So the dialect is
MIRRORED in `scripts/scope_globs.py` and pinned here against literals and
behaviour transcribed from the authority.

PROVENANCE OF THE TRANSCRIPTION. Read from the live codexFactory checkout at HEAD
`3143f34d` (glob region last changed at `9ebe805`,
`add-regular-pr-council-clearance`):

  * `envelope._COMPLEMENT_KEYS` and `envelope._UNIVERSAL_PATTERNS` (verbatim
    tuples, below).
  * The accept/reject fixtures of codexFactory's own
    `tests/merge-master/test_generalized_core.py`
    (`test_a_complement_shaped_surface_declaration_is_refused`,
    `test_a_universal_or_negated_allowlist_entry_is_refused`) and
    `tests/merge-master/test_envelope.py`
    (`test_glob_double_star_matches_nested_and_top`,
    `test_glob_double_star_does_not_leak_to_siblings`).

IF THE AUTHORITY'S DIALECT EVER CHANGES, this file and the mirror in
`scripts/scope_globs.py` MUST be updated in the same lockstep and the SHA above
refreshed.
"""
from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
MODULE = ROOT / "scripts" / "scope_globs.py"

# --- verbatim transcription of the authority's dialect constants --------------
AUTHORITY_COMPLEMENT_KEYS = (
    "path_denylist", "path_blocklist", "path_exclusions", "exclude_paths",
    "except_paths", "path_complement", "not_paths", "path_exclude",
    "codeowners_complement",
)
AUTHORITY_UNIVERSAL_PATTERNS = ("**", "*", "**/*", "/**", "./**")


def _load():
    spec = importlib.util.spec_from_file_location("scope_globs", MODULE)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


sg = _load()


def test_complement_keys_are_byte_identical_to_the_authority():
    assert sg.COMPLEMENT_KEYS == AUTHORITY_COMPLEMENT_KEYS


def test_universal_patterns_are_byte_identical_to_the_authority():
    assert sg.UNIVERSAL_PATTERNS == AUTHORITY_UNIVERSAL_PATTERNS


# --- the authority's accept/reject fixtures, replayed against the mirror -------


@pytest.mark.parametrize("entry", ["**", "*", "!scripts/**", "/catalog/**"])
def test_authority_rejected_allowlist_entries_are_rejected_here(entry):
    # codexFactory test_a_universal_or_negated_allowlist_entry_is_refused
    with pytest.raises(sg.ScopeGlobsError):
        sg.validate_scope_globs({"R": ["catalog/**", entry]}, code_surface_repos={"R"})


@pytest.mark.parametrize("key", ["path_denylist", "except_paths", "codeowners_complement"])
def test_authority_rejected_complement_keys_are_rejected_here(key):
    # codexFactory test_a_complement_shaped_surface_declaration_is_refused
    with pytest.raises(sg.ScopeGlobsError):
        sg.validate_scope_globs({key: ["scripts/**"]}, code_surface_repos={key})


def test_glob_double_star_matches_nested_and_top():
    # codexFactory test_glob_double_star_matches_nested_and_top
    assert sg.path_matches("health/reports/2026-07-16.md", ["health/**"])
    assert sg.path_matches("health/corpus.json", ["health/**"])
    assert sg.path_matches("health/a/b/c/d.md", ["health/**"])


def test_glob_double_star_does_not_leak_to_siblings():
    # codexFactory test_glob_double_star_does_not_leak_to_siblings
    assert not sg.path_matches("healthcheck/x.md", ["health/**"])
    assert not sg.path_matches("docs/health/x.md", ["health/**"])
    assert not sg.path_matches(".github/merge-approval-envelope.yml", ["health/**"])


def test_single_star_and_question_are_segment_scoped():
    # `*` and `?` never cross a path separator (envelope._glob_to_regex).
    assert sg.path_matches("docs/a1.md", ["docs/a?.md"])
    assert not sg.path_matches("docs/a12.md", ["docs/a?.md"])
    assert sg.path_matches("docs/anything.md", ["docs/*.md"])
    assert not sg.path_matches("docs/sub/x.md", ["docs/*.md"])
