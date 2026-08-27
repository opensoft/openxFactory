"""`scripts/set-domain-openxfactory-pin.py` must not regenerate away the comment
that tells it not to.

WHY THIS FILE EXISTS. Found by `split-openxwallet-repo` P5a.2 while bumping
LedgerxFactory's `stack.yaml` to the P2.5 minor. `preserved_subblocks` carried a
preserved provenance sub-block's KEY and VALUE lines through a pin rewrite and
dropped every other line in the `xfactory:` block — including the two comment
lines immediately above `promoted_from:`, which read:

    # managed provenance (document-lifecycle promotion process) -- re-pin
    # tooling must preserve this block; regenerating it away is a health finding

A tool that answers an instruction not to delete something by deleting the
instruction is the worst available outcome: the block stays, the reason it stays
does not, and the next reader has no reason to think it is protected. The
protection was never machine-readable, so nothing but this suite can hold it.

THE FIXTURE IS A LITERAL, NOT A READ OF THE SIBLING CHECKOUT. These tests run in
`pytest-suite` over a lone openxFactory clone with no `xFactories/` beside it, so
a test that read LedgerxFactory's real file would skip in CI — which is where it
has to run. The literal is pinned to the real shape by
`test_the_fixture_still_matches_the_live_ledgerx_shape`, which self-skips when no
sibling checkout is reachable (the same instrument the openxwallet-pin suite uses
for its aggregation-dependent assertions), so fixture drift is caught wherever a
real tree is present without making CI depend on one.
"""

from __future__ import annotations

import importlib.util
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPT = REPO_ROOT / "scripts" / "set-domain-openxfactory-pin.py"

spec = importlib.util.spec_from_file_location("set_domain_openxfactory_pin",
                                              SCRIPT)
setter = importlib.util.module_from_spec(spec)
spec.loader.exec_module(setter)

PRESERVE_COMMENT = (
    "  # managed provenance (document-lifecycle promotion process) — re-pin\n"
    "  # tooling must preserve this block; regenerating it away is a health "
    "finding\n")

PROMOTED_FROM = (
    "  promoted_from:\n"
    "    - artifact: contracts/schemas/xfactory-workflow.schema.yaml\n"
    "      candidate_id: DTN-001\n"
    "    - artifact: contracts/schemas/xfactory-workflow.schema.yaml\n"
    "      candidate_id: DTN-002\n"
    "    - artifact: contracts/schemas/"
    "xfactory-credential-contracts.schema.yaml\n"
    "      candidate_id: DTN-004\n")

#: LedgerxFactory's `stack.yaml` shape: the `xfactory:` block with a comment
#: block between the last regenerated key and a preserved sub-block, and a
#: following top-level key whose own comments must not move.
LEDGERX_SHAPE = (
    "schema_version: 1\n"
    "kind: xfactory_domain_stack\n"
    "\n"
    "domain:\n"
    "  id: ledgerx\n"
    "  product_name: LedgerxFactory\n"
    "\n"
    "xfactory:\n"
    "  contract_repo: github.com/opensoft/openxFactory\n"
    "  contract_name: openxFactory\n"
    "  contract_ref_type: commit\n"
    "  contract_ref: 39539fd4fa137614f8ebca2574d373d5b8ecc065\n"
    "  contract_schema_version: 1\n"
    '  contract_declared_at: "2026-08-08"\n'
    "  contract_source: xFactory-submodule-pin\n"
    + PRESERVE_COMMENT
    + PROMOTED_FROM
    + "hermes:\n"
      "  # Canonical layer declaration (contract-v1.1).\n"
      "  layers:\n"
      "    - role: customer\n"
)

NEW_REF = "a" * 40


def _repin(tmp_path: Path, text: str) -> str:
    path = tmp_path / "stack.yaml"
    path.write_text(text, encoding="utf-8")
    setter.update_stack(path, NEW_REF, "commit", "2026-08-27",
                        "xFactory-submodule-pin")
    return path.read_text(encoding="utf-8")


# --- the regression -----------------------------------------------------------

def test_the_preserve_comment_survives_a_repin(tmp_path):
    out = _repin(tmp_path, LEDGERX_SHAPE)
    assert PRESERVE_COMMENT in out, (
        "the comment instructing the tool to preserve the block was itself "
        "regenerated away")


def test_the_comment_still_precedes_the_block_it_annotates(tmp_path):
    """Preserved is not enough — a comment relocated below its block annotates
    the wrong thing."""
    out = _repin(tmp_path, LEDGERX_SHAPE)
    assert out.index(PRESERVE_COMMENT) < out.index("  promoted_from:")
    assert PRESERVE_COMMENT + "  promoted_from:\n" in out


def test_the_preserved_block_itself_still_survives_verbatim(tmp_path):
    out = _repin(tmp_path, LEDGERX_SHAPE)
    assert PROMOTED_FROM in out


def test_the_pin_is_actually_rewritten(tmp_path):
    """The fix must not have been "preserve everything"."""
    out = _repin(tmp_path, LEDGERX_SHAPE)
    assert f"  contract_ref: {NEW_REF}\n" in out
    assert "39539fd4fa137614f8ebca2574d373d5b8ecc065" not in out
    assert '  contract_declared_at: "2026-08-27"\n' in out


def test_nothing_outside_the_xfactory_block_moves(tmp_path):
    out = _repin(tmp_path, LEDGERX_SHAPE)
    head, _, _ = LEDGERX_SHAPE.partition("xfactory:\n")
    assert out.startswith(head)
    tail = "hermes:\n  # Canonical layer declaration (contract-v1.1).\n"
    assert out.endswith(LEDGERX_SHAPE[LEDGERX_SHAPE.index(tail):])


def test_a_repin_is_idempotent(tmp_path):
    once = _repin(tmp_path, LEDGERX_SHAPE)
    twice = _repin(tmp_path, once)
    assert twice == once
    assert setter.update_stack(tmp_path / "stack.yaml", NEW_REF, "commit",
                               "2026-08-27", "xFactory-submodule-pin") is False


# --- the attribution rule -----------------------------------------------------

def test_a_comment_above_a_regenerated_key_is_still_dropped(tmp_path):
    """ATTRIBUTION: a comment run belongs to what FOLLOWS it. A comment
    describing `contract_source:` annotates a line regenerated from arguments on
    every run, so it goes with it — the alternative, preserving every comment in
    the block, would strand stale prose above freshly written values."""
    text = LEDGERX_SHAPE.replace(
        "  contract_source: xFactory-submodule-pin\n",
        "  # this describes the source line below\n"
        "  contract_source: xFactory-submodule-pin\n", 1)
    out = _repin(tmp_path, text)
    assert "this describes the source line below" not in out
    assert PRESERVE_COMMENT in out, "the OTHER comment must be unaffected"


def test_a_comment_between_a_preserved_block_and_the_next_key_is_attributed_forward(
        tmp_path):
    """A comment sitting after `promoted_from:`'s list and before the next
    sub-key annotates that next key, not the list it merely follows."""
    text = LEDGERX_SHAPE.replace(
        PROMOTED_FROM + "hermes:",
        PROMOTED_FROM
        + "  # about specializes\n"
        + "  specializes: openxFactory\n"
        + "hermes:", 1)
    out = _repin(tmp_path, text)
    assert "  # about specializes\n  specializes: openxFactory\n" in out


def test_a_blank_line_travels_with_the_comment_it_separates(tmp_path):
    text = LEDGERX_SHAPE.replace(
        PRESERVE_COMMENT, "\n" + PRESERVE_COMMENT, 1)
    out = _repin(tmp_path, text)
    assert "\n" + PRESERVE_COMMENT + "  promoted_from:\n" in out


def test_a_block_with_no_preserved_subblock_keeps_no_comments(tmp_path):
    text = LEDGERX_SHAPE.replace(PRESERVE_COMMENT + PROMOTED_FROM, "", 1)
    out = _repin(tmp_path, text)
    assert "promoted_from" not in out
    assert "managed provenance" not in out
    assert f"  contract_ref: {NEW_REF}\n" in out


def test_specializes_alone_is_preserved_with_its_comment(tmp_path):
    text = LEDGERX_SHAPE.replace(
        PRESERVE_COMMENT + PROMOTED_FROM,
        "  # a preserved-key comment\n  specializes: openxFactory\n", 1)
    out = _repin(tmp_path, text)
    assert "  # a preserved-key comment\n  specializes: openxFactory\n" in out


# --- fixture-drift guard ------------------------------------------------------

def test_the_fixture_still_matches_the_live_ledgerx_shape():
    """Self-skipping: `pytest-suite` runs over a lone openxFactory clone.

    Where a sibling LedgerxFactory IS reachable, the two facts the fixture
    encodes are checked against the real file — the preserve comment's text and
    that it sits immediately above `promoted_from:`. Byte equality of the whole
    file is deliberately NOT asserted: the pin values change on every bump and
    the shape is what this suite is about.
    """
    for candidate in (REPO_ROOT.parent / "xFactories" / "LedgerxFactory",
                      REPO_ROOT.parent.parent / "xFactories" / "LedgerxFactory"):
        live = candidate / "stack.yaml"
        if live.is_file():
            break
    else:
        pytest.skip("no sibling LedgerxFactory checkout reachable from this tree")
    text = live.read_text(encoding="utf-8")
    assert PRESERVE_COMMENT in text, (
        f"{live} no longer carries the preserve comment this fixture encodes; "
        "update LEDGERX_SHAPE (and check the comment was not lost to a repin)")
    assert PRESERVE_COMMENT + "  promoted_from:\n" in text
