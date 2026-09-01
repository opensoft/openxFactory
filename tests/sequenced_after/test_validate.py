"""Feature `sequenced-after-validate` (add-sequenced-after-substrate tasks
4.1-4.7): two-location ANCHORED resolution, cycle refusal, the deliberate ABSENCE
of a depth or fan-out limit, and the house validator wired over the live corpus.

`openspec validate` (the external CLI) cannot be extended, so the house wiring is
`scripts/validate-sequenced-after.py` plus `test_corpus_sequenced_after_all_validate`
below, which runs it over every active change on every PR — the same enforcement
route the other `scripts/validate-*.py` contract validators use.
"""
from __future__ import annotations

import importlib.util
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
MODULE = ROOT / "scripts" / "sequenced_after.py"
VALIDATOR = ROOT / "scripts" / "validate-sequenced-after.py"


def _load():
    # Loaded under a name that is NOT `sequenced_after`: THIS DIRECTORY is a
    # package by that name (see `__init__.py`), and registering the script module
    # under the package's own name would replace the package in `sys.modules` and
    # abort collection of every sibling test module.
    spec = importlib.util.spec_from_file_location("sequenced_after_substrate", MODULE)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


sa = _load()


# --- a synthetic corpus ------------------------------------------------------


def _change(root: Path, change_id: str, declaration: str | None = None,
            archived: str | None = None, under: Path | None = None) -> Path:
    """Write one change directory. `declaration` is the YAML text after
    `sequenced_after:` (None omits the field); `archived` is a `YYYY-MM-DD`
    prefix placing it under `archive/`; `under` overrides the changes root, for
    the NESTED-corpus fixture."""
    base = under if under is not None else root / "openspec" / "changes"
    directory = (base / "archive" / f"{archived}-{change_id}"
                 if archived else base / change_id)
    directory.mkdir(parents=True, exist_ok=True)
    front = "code_surface: openxFactory"
    if declaration is not None:
        front += f"\nsequenced_after: {declaration}"
    (directory / "proposal.md").write_text(
        f"---\n{front}\n---\n\n# {change_id}\n", encoding="utf-8")
    return directory


# --- two-location ANCHORED resolution (tasks 4.1, 4.7) -----------------------


def test_an_active_parent_resolves(tmp_path):
    expected = _change(tmp_path, "add-parent")
    assert sa.resolve(tmp_path, "add-parent") == expected


def test_an_ARCHIVED_parent_still_resolves(tmp_path):
    # A chain's ROOT is its oldest change and therefore the FIRST to archive, so
    # an active-only rule would make every chain self-disable in the worst order.
    expected = _change(tmp_path, "add-parent", archived="2026-08-28")
    assert sa.resolve(tmp_path, "add-parent") == expected


def test_an_id_matching_BOTH_locations_is_AMBIGUOUS(tmp_path):
    _change(tmp_path, "add-parent")
    _change(tmp_path, "add-parent", archived="2026-08-28")
    with pytest.raises(sa.SequencedAfterError) as exc:
        sa.resolve(tmp_path, "add-parent")
    assert "AMBIGUOUS" in str(exc.value)
    assert "MUST NOT prefer either" in str(exc.value)


def test_TWO_ARCHIVE_DATES_for_one_id_are_AMBIGUOUS(tmp_path):
    _change(tmp_path, "add-parent", archived="2026-08-28")
    _change(tmp_path, "add-parent", archived="2026-08-29")
    with pytest.raises(sa.SequencedAfterError) as exc:
        sa.resolve(tmp_path, "add-parent")
    assert "AMBIGUOUS" in str(exc.value)


def test_an_archive_name_that_merely_STARTS_WITH_the_id_does_not_resolve(tmp_path):
    # Anchored and EXACT on both the date and the remainder: a prefix strip or a
    # split on the first hyphen would mis-resolve an id containing digits and
    # hyphens.
    _change(tmp_path, "add-parent-extended", archived="2026-08-28")
    with pytest.raises(sa.SequencedAfterError) as exc:
        sa.resolve(tmp_path, "add-parent")
    assert "resolves to no change directory" in str(exc.value)


def test_an_archive_name_with_no_anchored_date_does_not_resolve(tmp_path):
    archive = tmp_path / "openspec" / "changes" / "archive" / "add-parent"
    archive.mkdir(parents=True)
    (archive / "proposal.md").write_text("---\n---\n", encoding="utf-8")
    with pytest.raises(sa.SequencedAfterError):
        sa.resolve(tmp_path, "add-parent")


def test_an_archive_name_with_a_malformed_date_does_not_resolve(tmp_path):
    _change(tmp_path, "add-parent", archived="26-8-2")
    with pytest.raises(sa.SequencedAfterError):
        sa.resolve(tmp_path, "add-parent")


def test_a_NESTED_changes_directory_does_not_resolve(tmp_path):
    # `openspec/changes/<id>/openspec/changes/<id2>/` must not resolve `<id2>`:
    # an unanchored active side would admit it.
    outer = _change(tmp_path, "add-outer")
    _change(tmp_path, "add-inner", under=outer / "openspec" / "changes")
    assert sa.resolve(tmp_path, "add-outer") == outer
    with pytest.raises(sa.SequencedAfterError):
        sa.resolve(tmp_path, "add-inner")


def test_an_archived_hop_is_read_from_the_ARCHIVED_directory(tmp_path):
    # The archived directory carries the FROZEN ratified text; that is where an
    # archived hop's own declarations are read from.
    archived = _change(tmp_path, "add-parent", declaration="[add-grandparent]",
                       archived="2026-08-28")
    _change(tmp_path, "add-grandparent", declaration="[]", archived="2026-08-01")
    assert sa.declaration_of(archived) == ["add-grandparent"]
    assert sa.resolve(tmp_path, "add-parent") == archived


# --- resolvability of BARE vs FOREIGN entries (task 4.2) ---------------------


def test_a_dangling_BARE_entry_FAILS_validation(tmp_path):
    _change(tmp_path, "add-child", declaration="[add-missing]")
    with pytest.raises(sa.SequencedAfterError) as exc:
        sa.validate_declaration(tmp_path, "add-child", ["add-missing"])
    assert "add-missing" in str(exc.value)
    assert "unwalkable" in str(exc.value)


def test_a_FOREIGN_entry_needs_only_to_be_WELL_FORMED(tmp_path):
    # The neutral validator cannot read another repository's corpus and must not
    # pretend to; the DISPOSITION is the consumer's, which refuses it under a
    # named identifier rather than SKIPPING it.
    _change(tmp_path, "add-child", declaration="[codexFactory:add-missing]")
    declaration = sa.validate_declaration(
        tmp_path, "add-child", ["codexFactory:add-missing"])
    assert declaration.foreign_refs()[0].change_id == "add-missing"


def test_a_SELF_QUALIFIED_entry_must_still_resolve(tmp_path):
    _change(tmp_path, "add-child", declaration="[openxFactory:add-missing]")
    with pytest.raises(sa.SequencedAfterError) as exc:
        sa.validate_declaration(tmp_path, "add-child", ["openxFactory:add-missing"])
    assert "add-missing" in str(exc.value)


def test_a_resolvable_chain_validates(tmp_path):
    _change(tmp_path, "add-root", declaration="[]")
    _change(tmp_path, "add-child", declaration="[add-root]")
    assert sa.validate_declaration(
        tmp_path, "add-child", ["add-root"]).local_ids() == ("add-root",)


# --- CYCLE refusal (task 4.3) -----------------------------------------------


def test_a_two_node_CYCLE_is_refused_naming_the_repeated_id(tmp_path):
    _change(tmp_path, "add-a", declaration="[add-b]")
    _change(tmp_path, "add-b", declaration="[add-a]")
    with pytest.raises(sa.SequencedAfterError) as exc:
        sa.validate_declaration(tmp_path, "add-a", ["add-b"])
    assert "CYCLE" in str(exc.value)
    assert "add-a" in str(exc.value) and "add-b" in str(exc.value)


def test_a_SELF_LOOP_is_refused(tmp_path):
    _change(tmp_path, "add-a", declaration="[add-a]")
    with pytest.raises(sa.SequencedAfterError) as exc:
        sa.validate_declaration(tmp_path, "add-a", ["add-a"])
    assert "CYCLE" in str(exc.value)


def test_a_three_node_CYCLE_is_refused(tmp_path):
    _change(tmp_path, "add-a", declaration="[add-b]")
    _change(tmp_path, "add-b", declaration="[add-c]")
    _change(tmp_path, "add-c", declaration="[add-a]")
    with pytest.raises(sa.SequencedAfterError) as exc:
        sa.validate_declaration(tmp_path, "add-a", ["add-b"])
    assert "CYCLE" in str(exc.value)


def test_a_cycle_reached_THROUGH_AN_ARCHIVED_hop_is_refused(tmp_path):
    _change(tmp_path, "add-a", declaration="[add-b]")
    _change(tmp_path, "add-b", declaration="[add-a]", archived="2026-08-28")
    with pytest.raises(sa.SequencedAfterError) as exc:
        sa.validate_declaration(tmp_path, "add-a", ["add-b"])
    assert "CYCLE" in str(exc.value)


def test_a_DIAMOND_is_not_a_cycle(tmp_path):
    # Two parents sharing a grandparent re-visits a node without revisiting it
    # ON THE PATH. A global seen-set would refuse this honest fan-in.
    _change(tmp_path, "add-root", declaration="[]")
    _change(tmp_path, "add-left", declaration="[add-root]")
    _change(tmp_path, "add-right", declaration="[add-root]")
    _change(tmp_path, "add-child", declaration="[add-left, add-right]")
    declaration = sa.validate_declaration(
        tmp_path, "add-child", ["add-left", "add-right"])
    assert declaration.local_ids() == ("add-left", "add-right")


# --- NO depth limit and NO fan-out limit (task 4.4) -------------------------


def test_a_TWO_PARENT_declaration_validates(tmp_path):
    _change(tmp_path, "add-p1", declaration="[]")
    _change(tmp_path, "add-p2", declaration="[]")
    _change(tmp_path, "add-child", declaration="[add-p1, add-p2]")
    declaration = sa.validate_declaration(
        tmp_path, "add-child", ["add-p1", "add-p2"])
    assert len(declaration.entries) == 2


def test_a_chain_DEEPER_than_any_gates_ceiling_validates(tmp_path):
    # The consuming gate's ceiling is FOUR hops inclusive of the terminal
    # change; a nine-hop chain must VALIDATE here, because the ceiling belongs to
    # the gate and not to the field.
    ids = [f"add-hop{n}" for n in range(10)]
    _change(tmp_path, ids[-1], declaration="[]")
    for child, parent in zip(ids, ids[1:]):
        _change(tmp_path, child, declaration=f"[{parent}]")
    sa.validate_declaration(tmp_path, ids[0], [ids[1]])
    assert sa.chain_depth(tmp_path, ids[0]) == 9


def test_chain_depth_measures_and_never_enforces(tmp_path):
    _change(tmp_path, "add-root", declaration="[]")
    _change(tmp_path, "add-child", declaration="[add-root]")
    assert sa.chain_depth(tmp_path, "add-root") == 0
    assert sa.chain_depth(tmp_path, "add-child") == 1


def test_chain_depth_of_a_declared_ROOT_and_of_an_UNDECLARED_change(tmp_path):
    _change(tmp_path, "add-root", declaration="[]")
    _change(tmp_path, "add-silent")
    assert sa.chain_depth(tmp_path, "add-root") == 0
    assert sa.chain_depth(tmp_path, "add-silent") == 0
    # ...and the two zeros mean different things, which is why root status is
    # never inferred from a depth reading.
    assert sa.declaration_of(
        sa.resolve(tmp_path, "add-root")) == []
    assert sa.declaration_of(
        sa.resolve(tmp_path, "add-silent")) is sa.ABSENT


def test_a_foreign_hop_terminates_the_local_walk_without_claiming_a_root(tmp_path):
    _change(tmp_path, "add-child", declaration="[codexFactory:add-foreign]")
    assert sa.chain_depth(tmp_path, "add-child") == 0
    declaration = sa.validate_declaration(
        tmp_path, "add-child", ["codexFactory:add-foreign"])
    assert declaration.is_root_claim is False, (
        "a foreign-only declaration is NOT a root claim; only an explicit [] is")


# --- the house validator (tasks 4.5, 4.6) -----------------------------------


def test_corpus_sequenced_after_all_validate():
    result = subprocess.run(
        [sys.executable, str(VALIDATOR), str(ROOT)],
        capture_output=True, text=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr


def test_THIS_CHANGE_declares_and_validates_its_own_parent():
    # The substrate's first instance is the corpus gate's first live subject.
    change = ROOT / "openspec" / "changes" / "add-sequenced-after-substrate"
    raw = sa.read_declaration(change / "proposal.md")
    assert raw == ["add-structured-scope-substrate"]
    declaration = sa.validate_declaration(
        ROOT, "add-sequenced-after-substrate", raw)
    assert declaration.local_ids() == ("add-structured-scope-substrate",)
    assert sa.chain_depth(ROOT, "add-sequenced-after-substrate") == 1


def test_the_validator_names_the_change_the_entry_and_the_rule(tmp_path):
    _change(tmp_path, "bad-change", declaration="[add-missing]")
    result = subprocess.run(
        [sys.executable, str(VALIDATOR), str(tmp_path)],
        capture_output=True, text=True,
    )
    assert result.returncode != 0
    assert "bad-change" in result.stdout
    assert "add-missing" in result.stdout
    assert "unwalkable" in result.stdout


def test_the_validator_flags_an_ungrammatical_entry(tmp_path):
    _change(tmp_path, "bad-change", declaration="[Nested/Path]")
    result = subprocess.run(
        [sys.executable, str(VALIDATOR), str(tmp_path)],
        capture_output=True, text=True,
    )
    assert result.returncode != 0
    assert "bad-change" in result.stdout


def test_the_validator_flags_a_cycle(tmp_path):
    _change(tmp_path, "add-a", declaration="[add-b]")
    _change(tmp_path, "add-b", declaration="[add-a]")
    result = subprocess.run(
        [sys.executable, str(VALIDATOR), str(tmp_path)],
        capture_output=True, text=True,
    )
    assert result.returncode != 0
    assert "CYCLE" in result.stdout


def test_the_validator_flags_a_strict_loader_refusal(tmp_path):
    change = tmp_path / "openspec" / "changes" / "bad-change"
    change.mkdir(parents=True)
    (change / "proposal.md").write_text(
        "---\nsequenced_after: [first]\nsequenced_after: [second]\n---\n\n# bad\n",
        encoding="utf-8")
    result = subprocess.run(
        [sys.executable, str(VALIDATOR), str(tmp_path)],
        capture_output=True, text=True,
    )
    assert result.returncode != 0
    assert "duplicate key" in result.stdout


def test_the_validator_accepts_absence_and_an_empty_root_claim(tmp_path):
    _change(tmp_path, "add-silent")
    _change(tmp_path, "add-root", declaration="[]")
    result = subprocess.run(
        [sys.executable, str(VALIDATOR), str(tmp_path)],
        capture_output=True, text=True,
    )
    assert result.returncode == 0, result.stdout
    assert "1 declaring the field" in result.stdout


def test_the_validator_accepts_a_multi_parent_and_a_deep_chain(tmp_path):
    ids = [f"add-hop{n}" for n in range(6)]
    _change(tmp_path, ids[-1], declaration="[]")
    for child, parent in zip(ids, ids[1:]):
        _change(tmp_path, child, declaration=f"[{parent}]")
    _change(tmp_path, "add-fork", declaration=f"[{ids[0]}, {ids[1]}]")
    result = subprocess.run(
        [sys.executable, str(VALIDATOR), str(tmp_path)],
        capture_output=True, text=True,
    )
    assert result.returncode == 0, result.stdout
