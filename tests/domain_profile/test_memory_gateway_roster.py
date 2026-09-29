"""The doxBench memory gateway's roster is the promoted capability's own: a
composition test moved here under R1Q2 (a), on F11.1's `HOST_TESTS` surface.

MOVED HERE by plan 034 T034 (opensoft/openDox-code#50, landed `71b631bc`).
The three cases left `tests/test_doxbench_memory_gateway.py` at openDox-code
`19370adc`, where they failed on `FileNotFoundError`: they read
`openspec/specs/memory-gateway/spec.md`, the promoted capability that
`doxbench_memory_gateway.CAPABILITY_REQUIREMENTS` is transcribed from. That
spec is openxFactory's, and no openDox repository carries a copy (#50 checked
openDox-spec, openDox, openXdox-spec, openXdox and openXdox-code). T034's own
text names only the outline case; the holder accepted these three under the
same R1Q2 (a), because the spec they read is openxFactory's alone.

They compose the two here: the spec is this repository's own, at `REPO_ROOT`,
and `mg` is the pinned openDox leg's `opendox.doxbench_memory_gateway`, which
the root `tests/conftest.py` puts on the path through `carved_reach`. The cases' bodies are #50's, verbatim.

WHY `tests/domain_profile/`, AND NOT THE PROPOSED `tests/ideation-dashboard/`
PATH. `tests/ideation-dashboard/` is inside the carve surface
(`docs/opendox-carve-manifest.yaml` `moved_paths:`), where
`scripts/validate-carve-manifest.py` refuses a NEW file that no row declares
(`carve-file-undeclared`), and F11.1 forbids adding the row. This directory is
outside that surface, and it is F11.1's own `HOST_TESTS` prefix. The root
`tests/conftest.py` installs the reach and makes the host's one call here too,
so a case that composes the pinned legs composes the same ones it would have
composed there.
"""

from __future__ import annotations

import re
from pathlib import Path

from opendox import doxbench_memory_gateway as mg  # noqa: E402

REPO_ROOT = Path(__file__).resolve().parents[2]

SPEC_PATH = REPO_ROOT / "openspec" / "specs" / "memory-gateway" / "spec.md"


# ===========================================================================
# THE ROSTER — transcribed, and asserted against the capability itself
# ===========================================================================


def test_the_roster_is_exactly_the_promoted_capabilitys_requirements():
    """The declaration is only complete if the roster it is complete OVER is
    the capability's own. Read from the promoted spec, so a requirement added
    upstream fails here rather than becoming a silent gap in the declaration."""
    published = {
        line[len("### Requirement: "):].strip()
        for line in SPEC_PATH.read_text(encoding="utf-8").splitlines()
        if line.startswith("### Requirement: ")
    }
    assert published == set(mg.CAPABILITY_REQUIREMENTS)


def _published_tiers() -> dict[str, str]:
    """The spec's OWN tier block, parsed: requirement name -> the tier line it
    is named on."""
    spec = SPEC_PATH.read_text(encoding="utf-8")
    block = spec.split("```text", 1)[1].split("```", 1)[0]
    published: dict[str, str] = {}
    for match in re.finditer(r"(M\d):((?:.|\n)*?)(?=\nM\d:|\Z)", block):
        tier, body = match.group(1), " ".join(match.group(2).split())
        for name in body.split(";"):
            published[name.strip().rstrip(".")] = tier
    return published


def test_the_tier_column_is_TRANSCRIBED_not_invented():
    """RE-PINNED (adversarial review, F7). The roster test checked NAMES only,
    so two wrong tier values sat in the column unchallenged: one requirement
    carried `M0` although the spec's tier block never tiers it at all, and
    `Expert Memory And Knowledge DBs Are Gateway-Governed` was FLATTENED to
    `M4` although the spec says in as many words that it follows the tier of
    the operation it mirrors. Both are now transcribed, and this test reads the
    spec's own block so neither error can recur silently."""
    published = _published_tiers()
    for requirement, declared in mg.CAPABILITY_REQUIREMENTS.items():
        named = [line for line in published
                 if line.lower().startswith(requirement.lower())]
        if not named:
            # Not tiered by the spec at all -- which the column must SAY.
            assert declared == mg.TIER_UNTIERED, requirement
            continue
        line = named[0]
        if line != requirement:
            # The spec qualifies this row rather than tiering it outright.
            assert declared == mg.TIER_MIRRORS_OPERATION, requirement
            assert "follows the tier of the operation it mirrors" in line
            continue
        assert declared == published[line], requirement


def test_the_untiered_requirement_really_is_absent_from_the_tier_block():
    published = _published_tiers()
    untiered = [name for name, tier in mg.CAPABILITY_REQUIREMENTS.items()
                if tier == mg.TIER_UNTIERED]
    # TWO since 2026-08-22: add-doxbench-editing-phase-b's archive promoted
    # `Subject-Free Local Consumers…` into the capability, and the spec's tier
    # block does not tier it either. The list stays EXACT rather than becoming
    # a membership check — an untiered requirement is a fact about the spec, so
    # a third one appearing should fail here and be looked at.
    assert untiered == [
        "Derived memory bindings validate against the neutral schema",
        "Subject-Free Local Consumers Declare Their Inapplicable Rails"]
    for name in untiered:
        assert not any(line.lower().startswith(name.lower())
                       for line in published)
