"""Feature `frontmatter-strict-loader` (add-sequenced-after-substrate tasks
2.1-2.5): the ONE strict loader over the realization-axis front-matter block, and
the `scope_globs` retrofit convener ruling OQ-1 (2026-09-01) placed INSIDE that
change.

Realizes the `release-realization` requirement "Strict loading of the
realization-axis front-matter block". The negative fixtures are one per refused
form, because a single collapsed fixture would pass even if the loader named the
wrong construct — the failure mode a per-construct refused set exists to prevent.

The retrofit's own claim is asserted here too: routing `scripts/scope_globs.py`
through the strict loader changes how the field is LOADED and never what it
MEANS, so every proposal in the LIVE corpus must read the same `scope_globs`
value under the strict loader as under the permissive `yaml.safe_load` path it
replaced.
"""
from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import pytest
import yaml

ROOT = Path(__file__).resolve().parents[2]
SCOPE_MODULE = ROOT / "scripts" / "scope_globs.py"
LOADER_MODULE = ROOT / "scripts" / "frontmatter_strict.py"


def _load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module  # dataclass field resolution needs this
    spec.loader.exec_module(module)
    return module


fms = _load(LOADER_MODULE, "frontmatter_strict")
sg = _load(SCOPE_MODULE, "scope_globs")


def _proposal(front_matter: str) -> str:
    return f"---\n{front_matter}\n---\n\n# Proposal\n\nbody\n"


# --- the POSITIVE fixture: an ordinary block loads unchanged (task 2.4) -------


def test_a_wellformed_block_loads_unchanged():
    text = _proposal(
        "code_surface: openxFactory (prose, not YAML)\n"
        "target_release: implemented\n"
        "scope_globs:\n"
        "  openxFactory:\n"
        "    - scripts/**\n"
        "    - openspec/specs/**\n"
        "sequenced_after: [add-structured-scope-substrate]"
    )
    front = fms.read_front_matter(text)
    assert front["scope_globs"] == {
        "openxFactory": ["scripts/**", "openspec/specs/**"]}
    assert front["sequenced_after"] == ["add-structured-scope-substrate"]
    assert front["code_surface"] == "openxFactory (prose, not YAML)"


def test_prose_headers_are_still_prose():
    # The block as a whole is NEVER YAML-parsed: a prose header carrying colons,
    # brackets and parentheses would not survive a YAML load and must not have to.
    front = fms.read_front_matter(_proposal(
        "code_surface: openxFactory: a prose sentence [with brackets] (and parens)\n"
        "scope_globs:\n  R:\n    - a/**"))
    assert front["code_surface"].startswith("openxFactory: a prose sentence")
    assert front["scope_globs"] == {"R": ["a/**"]}


# --- DUPLICATE KEYS, top level and NESTED (tasks 2.2, 2.4) -------------------


@pytest.mark.parametrize("field", ["scope_globs", "sequenced_after"])
def test_a_structured_field_declared_twice_is_refused(field):
    # The hazard in one line: `yaml.safe_load` resolves this last-wins SILENTLY,
    # so a reviewer sees the first block and the machine authorizes from the last.
    blocks = {
        "scope_globs": "scope_globs:\n  R:\n    - narrow/**\n"
                       "scope_globs:\n  R:\n    - wide/**",
        "sequenced_after": "sequenced_after: [shown-to-the-reviewer]\n"
                           "sequenced_after: [walked-by-the-machine]",
    }[field]
    with pytest.raises(fms.StrictFrontMatterError) as exc:
        fms.read_front_matter(_proposal(blocks))
    assert field in str(exc.value)
    assert "duplicate key" in str(exc.value)


def test_the_permissive_loader_would_have_taken_the_last_block():
    # The regression this refusal closes, demonstrated rather than asserted in
    # prose: the loader the retrofit replaced returns the WIDE scope.
    permissive = yaml.safe_load(
        "scope_globs:\n  R:\n    - narrow/**\n"
        "scope_globs:\n  R:\n    - wide/**\n")
    assert permissive == {"scope_globs": {"R": ["wide/**"]}}


def test_a_NESTED_duplicate_key_is_refused():
    # Nesting depth must not smuggle a duplicate past a top-level check: a nested
    # duplicate authorizes exactly as well as a top-level one.
    with pytest.raises(fms.StrictFrontMatterError) as exc:
        fms.read_front_matter(_proposal(
            "scope_globs:\n"
            "  R:\n    - narrow/**\n"
            "  R:\n    - wide/**"))
    assert "duplicate key" in str(exc.value)
    assert "'R'" in str(exc.value)


def test_a_deeply_nested_duplicate_key_is_refused():
    with pytest.raises(fms.StrictFrontMatterError) as exc:
        fms.read_front_matter(_proposal(
            "scope_globs:\n"
            "  R:\n"
            "    nested:\n"
            "      a: 1\n"
            "      a: 2"))
    assert "duplicate key" in str(exc.value)


def test_an_NFC_equivalent_duplicate_key_is_refused():
    # `café` composed and `café` decomposed are ONE key to every human reading
    # the file and two to the machine.
    with pytest.raises(fms.StrictFrontMatterError) as exc:
        fms.read_front_matter(_proposal(
            "scope_globs:\n"
            "  caf\u00e9:\n    - a/**\n"
            "  cafe\u0301:\n    - b/**"))
    assert "duplicate key" in str(exc.value)


# --- ANCHOR, ALIAS, MERGE KEY — each named separately (task 2.4) -------------


def test_an_anchor_is_refused_and_named():
    with pytest.raises(fms.StrictFrontMatterError) as exc:
        fms.read_front_matter(_proposal(
            "scope_globs:\n"
            "  R: &wide\n    - wide/**"))
    assert "anchor" in str(exc.value)
    assert "&wide" in str(exc.value)


def test_an_alias_is_refused_and_named_as_an_alias_not_an_anchor():
    # Composition reaches the ANCHOR first, so a loader-order refusal would call
    # this "an anchor" and the two fixtures would collapse onto one message.
    with pytest.raises(fms.StrictFrontMatterError) as exc:
        fms.read_front_matter(_proposal(
            "scope_globs:\n"
            "  R: &wide\n    - wide/**\n"
            "  S: *wide"))
    assert "alias" in str(exc.value)
    assert "*wide" in str(exc.value)


def test_a_merge_key_is_refused_and_named_as_a_merge_key():
    with pytest.raises(fms.StrictFrontMatterError) as exc:
        fms.read_front_matter(_proposal(
            "scope_globs:\n"
            "  base: &base\n    a: 1\n"
            "  R:\n    <<: *base\n    b: 2"))
    assert "merge key" in str(exc.value)


# --- NON-UTF-8 and the BYTE CEILING (task 2.1, 2.4) --------------------------


def test_a_non_utf8_byte_is_refused_rather_than_replaced(tmp_path):
    p = tmp_path / "proposal.md"
    p.write_bytes(
        b"---\nscope_globs:\n  R:\n    - a\xff/**\n---\n\n# Proposal\n")
    with pytest.raises(fms.StrictFrontMatterError) as exc:
        fms.read_front_matter(p)
    assert "not valid UTF-8" in str(exc.value)


def test_a_non_utf8_byte_is_refused_from_bytes_too():
    with pytest.raises(fms.StrictFrontMatterError) as exc:
        fms.read_front_matter(b"---\nscope_globs:\n  R:\n    - a\xff\n---\n")
    assert "not valid UTF-8" in str(exc.value)


def test_a_block_over_the_ceiling_is_refused_before_the_parse():
    assert fms.CEILING_BYTES == 65_536  # the OPERATIVE number, not a gesture
    filler = "\n".join(f"    - path{n}/**" for n in range(9000))
    text = _proposal("scope_globs:\n  R:\n" + filler)
    with pytest.raises(fms.StrictFrontMatterError) as exc:
        fms.read_front_matter(text)
    assert str(fms.CEILING_BYTES) in str(exc.value)
    assert "before the parse" in str(exc.value)


def test_the_largest_real_front_matter_is_far_under_the_ceiling():
    # The ceiling must bound the parser without ever binding an honest proposal.
    largest = 0
    for proposal in (ROOT / "openspec" / "changes").rglob("proposal.md"):
        lines = fms.fenced_lines(proposal.read_bytes())
        if lines is None:
            continue
        largest = max(largest, len("\n".join(lines).encode("utf-8")))
    assert 0 < largest < fms.CEILING_BYTES // 4, largest


# --- the two PARITY extras the consuming verifier also refuses ---------------


def test_a_yaml_directive_is_refused():
    with pytest.raises(fms.StrictFrontMatterError) as exc:
        fms.strict_load("%YAML 1.2\n---\nscope_globs:\n  R:\n    - a/**\n")
    assert "directive" in str(exc.value)


def test_more_than_one_document_is_refused():
    with pytest.raises(fms.StrictFrontMatterError) as exc:
        fms.strict_load("scope_globs:\n  R:\n    - a/**\n---\nscope_globs: {}\n")
    assert "documents where exactly one is required" in str(exc.value)


def test_unparseable_yaml_refuses_with_the_field_named():
    with pytest.raises(fms.StrictFrontMatterError) as exc:
        fms.read_front_matter(
            "---\nscope_globs:\n  - : :bad\n  nested: [unterminated\n---\nbody")
    assert "scope_globs" in str(exc.value)


# --- the retrofit: same MEANING, stricter LOADING (task 2.3) -----------------


def _permissive_scope_globs(proposal: Path):
    """The loader the retrofit REPLACED, re-implemented here so the equality is
    measured against the real thing rather than remembered."""
    text = proposal.read_text(encoding="utf-8", errors="strict")
    lines = fms.fenced_lines(text)
    if lines is None:
        return None
    for field, block in fms.field_blocks(lines).items():
        if field != "scope_globs":
            continue
        parsed = yaml.safe_load("\n".join(block))
        return parsed.get("scope_globs") if isinstance(parsed, dict) else parsed
    return None


def test_the_live_corpus_reads_identically_under_the_strict_loader():
    proposals = sorted((ROOT / "openspec" / "changes").rglob("proposal.md"))
    assert proposals, "the corpus scan found no proposals"
    for proposal in proposals:
        assert sg.read_scope_globs(proposal) == _permissive_scope_globs(proposal), \
            f"{proposal} reads differently under the strict loader"


def test_scope_globs_still_raises_its_own_error_type():
    # API-honouring: a caller catching `ScopeGlobsError` keeps catching every
    # refusal this reader can raise, strict-loader refusals included.
    with pytest.raises(sg.ScopeGlobsError) as exc:
        sg.read_front_matter(_proposal(
            "scope_globs:\n  R:\n    - a/**\nscope_globs:\n  R:\n    - b/**"))
    assert "duplicate key" in str(exc.value)


def test_scope_globs_reads_through_the_shared_loader():
    assert sg.fms is fms or sg.fms.__file__ == fms.__file__


# --- the PARITY NOTE is a build obligation (task 2.5) ------------------------


def test_the_module_docstring_records_the_lockstep_parity_obligation():
    doc = fms.__doc__ or ""
    flat = " ".join(doc.split())
    assert "change_digest.py" in flat, "the authority module must be named"
    assert "MUST be made in lockstep" in flat
    for construct in ("DUPLICATE KEYS", "ANCHORS", "ALIASES", "MERGE KEYS",
                      "NON-UTF-8 BYTES", "BYTE CEILING"):
        assert construct in flat, construct
