"""Feature `sequenced-after-integrity` (add-sequenced-after-substrate tasks
5.4-5.5): the CORPUS SWEEP as a shipped, RE-RUNNABLE report.

A one-off measurement recorded in prose ages into a stale sentence. The sweep is
what makes the "measured, not assumed" obligation of the "Chain-walk policy
belongs to the consumer, and its bound SHALL be measured" requirement DISCHARGE
OVER TIME: it reports the population, the co-modified / sole-modifier split at
requirement granularity, adoption of the field, and THE DEEPEST DECLARED CHAIN it
resolves.

The reading of the live corpus is asserted here against the AUTHORING measurement
recorded in the ratified proposal, so a drift in either the corpus or the
counting method surfaces as a test failure rather than as a number nobody
re-derives.
"""
from __future__ import annotations

import importlib.util
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MODULE = ROOT / "scripts" / "sequenced_after.py"
VALIDATOR = ROOT / "scripts" / "validate-sequenced-after.py"
CHANGE = ROOT / "openspec" / "changes" / "add-sequenced-after-substrate"


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


def _change(root: Path, change_id: str, declaration: str | None = None,
            archived: str | None = None, requirements: dict | None = None) -> Path:
    base = root / "openspec" / "changes"
    directory = (base / "archive" / f"{archived}-{change_id}"
                 if archived else base / change_id)
    directory.mkdir(parents=True, exist_ok=True)
    front = "code_surface: openxFactory"
    if declaration is not None:
        front += f"\nsequenced_after: {declaration}"
    (directory / "proposal.md").write_text(
        f"---\n{front}\n---\n\n# {change_id}\n", encoding="utf-8")
    for capability, titles in (requirements or {}).items():
        spec_dir = directory / "specs" / capability
        spec_dir.mkdir(parents=True, exist_ok=True)
        body = "\n".join(
            f"### Requirement: {title}\nThe system SHALL do it.\n"
            f"#### Scenario: s\n- **WHEN** a\n- **THEN** b\n" for title in titles)
        (spec_dir / "spec.md").write_text(
            f"# delta\n\n## ADDED Requirements\n\n{body}", encoding="utf-8")
    return directory


# --- requirement-granular co-modification (task 5.4) ------------------------


def test_requirement_titles_are_NORMALIZED_before_comparison():
    # NFC + whitespace-collapsed + case-folded: two changes writing the same
    # requirement under a re-wrapped or re-cased title ARE co-modifiers, and a
    # raw string comparison would report two sole modifiers instead.
    assert (sa.normalize_requirement_title("Ordered   deltas\tand branch")
            == sa.normalize_requirement_title("ordered deltas and branch"))
    assert (sa.normalize_requirement_title("Café rule")
            == sa.normalize_requirement_title("café rule"))


def test_co_modification_is_REQUIREMENT_granular_not_capability_granular(tmp_path):
    _change(tmp_path, "add-a", requirements={"cap": ["First rule"]})
    _change(tmp_path, "add-b", requirements={"cap": ["Second rule"]})
    sweep = sa.corpus_sweep(tmp_path)
    assert sweep.co_modified == 0, (
        "two changes touching one capability but no shared requirement are not "
        "ordered deltas on each other")
    assert sweep.sole_modifiers == 2


def test_a_shared_requirement_title_makes_BOTH_changes_co_modified(tmp_path):
    _change(tmp_path, "add-a", requirements={"cap": ["Shared rule"]})
    _change(tmp_path, "add-b", requirements={"cap": ["shared   RULE"]})
    sweep = sa.corpus_sweep(tmp_path)
    assert sweep.co_modified == 2 and sweep.sole_modifiers == 0


def test_the_same_title_under_two_capabilities_is_not_shared(tmp_path):
    _change(tmp_path, "add-a", requirements={"cap-one": ["Same title"]})
    _change(tmp_path, "add-b", requirements={"cap-two": ["Same title"]})
    assert sa.corpus_sweep(tmp_path).co_modified == 0


# --- the sweep's other measures ---------------------------------------------


def test_the_sweep_counts_the_population_across_BOTH_corpora(tmp_path):
    _change(tmp_path, "add-active")
    _change(tmp_path, "add-archived", archived="2026-08-01")
    sweep = sa.corpus_sweep(tmp_path)
    assert (sweep.change_ids, sweep.active, sweep.archived) == (2, 1, 1)


def test_the_sweep_counts_DECLARATIONS_and_ROOT_CLAIMS_separately(tmp_path):
    _change(tmp_path, "add-silent")
    _change(tmp_path, "add-root", declaration="[]")
    _change(tmp_path, "add-child", declaration="[add-root]")
    sweep = sa.corpus_sweep(tmp_path)
    assert sweep.declaring == 2, "absence is not a declaration"
    assert sweep.root_claims == 1
    assert sweep.declaring_ids == ("add-child", "add-root")


def test_the_sweep_reports_the_DEEPEST_DECLARED_CHAIN_and_names_it(tmp_path):
    ids = [f"add-hop{n}" for n in range(5)]
    _change(tmp_path, ids[-1], declaration="[]")
    for child, parent in zip(ids, ids[1:]):
        _change(tmp_path, child, declaration=f"[{parent}]")
    sweep = sa.corpus_sweep(tmp_path)
    assert sweep.deepest_chain == 4
    assert sweep.deepest_chain_change == ids[0]


def test_a_chain_whose_ROOT_HAS_ARCHIVED_is_still_measured(tmp_path):
    _change(tmp_path, "add-root", declaration="[]", archived="2026-08-01")
    _change(tmp_path, "add-child", declaration="[add-root]")
    assert sa.corpus_sweep(tmp_path).deepest_chain == 1


def test_a_ZERO_deepest_chain_is_reported_as_ZERO_EVIDENCE(tmp_path):
    _change(tmp_path, "add-root", declaration="[]")
    rendered = sa.corpus_sweep(tmp_path).render()
    assert "DEEPEST DECLARED CHAIN RESOLVED: 0 hop(s)" in rendered
    assert "ZERO EVIDENCE" in rendered
    assert "not evidence that a ceiling is sufficient" in rendered


def test_the_sweep_counts_the_surviving_PROSE_headers(tmp_path):
    # The header is counted WHEREVER it sits, because a free-text header no
    # schema validates has no defined location either — which is part of why it
    # was measured to be unwalkable rather than adopted as the link.
    directory = _change(tmp_path, "add-prose")
    (directory / "proposal.md").write_text(
        "---\ncode_surface: openxFactory\n---\n\n# add-prose\n\n"
        "Sequenced-after: add-parent (free text no schema validates)\n",
        encoding="utf-8")
    _change(tmp_path, "add-archived-prose", archived="2026-08-01")
    archived = (tmp_path / "openspec" / "changes" / "archive"
                / "2026-08-01-add-archived-prose" / "proposal.md")
    archived.write_text(
        "---\ncode_surface: openxFactory\n---\n\n# a\n\nSequenced-after: x\n",
        encoding="utf-8")
    sweep = sa.corpus_sweep(tmp_path)
    assert sweep.prose_headers == 2
    assert sweep.prose_headers_archived == 1
    assert sweep.declaring == 0, (
        "a prose header is NOT a machine-readable declaration and must never be "
        "counted as one")


def test_the_sweep_never_gates(tmp_path):
    # A measurement is not a gate: a corpus full of dangling references still
    # SWEEPS (and still FAILS validation, which is a different run).
    _change(tmp_path, "add-child", declaration="[add-missing]")
    sweep = sa.corpus_sweep(tmp_path)
    assert sweep.declaring == 1 and sweep.deepest_chain == 0
    result = subprocess.run(
        [sys.executable, str(VALIDATOR), str(tmp_path), "--sweep"],
        capture_output=True, text=True)
    assert result.returncode == 0, result.stdout + result.stderr
    assert "corpus sweep" in result.stdout


# --- the LIVE corpus reading (task 5.5) -------------------------------------


def test_the_live_sweep_reproduces_the_AUTHORING_measurement():
    """The authoring measurement, re-derived — and MOVED where the corpus moved.

    The ratified proposal recorded, over the corpus as it stood BEFORE this
    change's own directory existed: 152 change ids, 104 co-modified, 48 sole
    modifiers, 19/11 among the active, 3 prose headers (all archived), 0
    declarations. The live sweep now includes THIS change, so every count that
    the change itself moves is asserted with it added — and the counts it does
    NOT move are asserted unchanged, which is what makes the two readings
    comparable rather than merely both true.

    WHEN THE CORPUS MOVES, THIS PIN MOVES WITH IT — and the move is RECORDED
    below rather than silently re-typed. The authoring numbers in the paragraph
    above are a HISTORICAL RECORD of what was measured then, and stay as written
    in `proposal.md`, `design.md` and the README OpenSpec Records block, which
    all report that one coherent pre-adoption snapshot. THE LIVE PIN IS THIS
    TEST, and only this test.

    MOVEMENT LOG — the sibling carriage ledger's dated-narrative practice
    (`tests/doc-health/test_modified_block_currency_self_gate.py`), applied here:

    - `active_co_modified` reads 18, and was measured 19 at authoring. It moved
      at `ded8b9f1` on 2026-09-01, when PR #563 archived
      `add-release-tag-publication-check` — an ACTIVE change carrying a
      `## MODIFIED Requirements` block, therefore co-modified. The archive moved
      it out of the active corpus and into the archived one (active 30 → 29,
      archived 122 → 123), so `active_co_modified` fell 19 → 18 while the
      corpus-wide `co_modified` held at 104: the change is still a co-modifier,
      it is simply no longer an ACTIVE one. This test was authored three minutes
      BEFORE that archive and landed at `43cf5933` (PR #567) carrying the
      pre-archive reading, so `main` went red on `6856f502`, the first pytest
      run that the concurrency group did not cancel.
    - NOTHING ELSE MOVED. Re-derived at `6856f502` against every commit since
      main's last green: `co_modified` 104, `change_ids - 1` 152,
      `sole_modifiers - 1` 48, `active_sole - 1` 11, 3 prose headers (3
      archived), 1 declaration, 0 root claims — each identical at `518c670b`,
      `ded8b9f1`, `43cf5933`, `a951be76` and `6856f502`.
    - `change_ids - 1`, `sole_modifiers - 1` and `active_sole - 1` move again
      when THIS PACKET's own directory lands: `add-clearing-dispatch-boundary`
      is itself one more ACTIVE change, and its spec delta is ADDED-only (no
      `## MODIFIED Requirements` block) with novel requirement titles, so it
      is a SOLE modifier, never a co-modifier — `co_modified` and
      `active_co_modified` hold at 104 and 18. `change_ids - 1` moves
      152 → 153, `sole_modifiers - 1` moves 48 → 49, and `active_sole - 1`
      moves 11 → 12, bumped in the branch's own landing commit per this rule,
      2026-09-01 (PR #555).
    - PR #548 then adds `amend-chain-anchoring-readiness-and-durability`, one
      more ACTIVE sole modifier with novel ADDED requirement titles. Against
      current main `ab0bb2dd`, change ids move 154 → 155, sole modifiers
      50 → 51, active changes 31 → 32 and active sole modifiers 13 → 14;
      both co-modified counts remain 104/18. Its machine-readable parent
      `[add-chain-anchoring]` moves declarations 1 → 2 without increasing the
      one-hop deepest chain, and root claims remain zero.
    - PR #548 then adds `amend-chain-anchoring-readiness-and-durability`, one
      more ACTIVE sole modifier with novel ADDED requirement titles. Against
      current main `ab0bb2dd`, change ids move 154 → 155, sole modifiers
      50 → 51, active changes 31 → 32 and active sole modifiers 13 → 14;
      both co-modified counts remain 104/18. Its machine-readable parent
      `[add-chain-anchoring]` moves declarations 1 → 2 without increasing the
      one-hop deepest chain, and root claims remain zero.
    """
    sweep = sa.corpus_sweep(ROOT)
    assert sweep.co_modified == 104, (
        "the co-modified population is unchanged by this change, whose ADDED "
        "requirement titles are NOVEL")
    assert sweep.active_co_modified == 18, (
        "18 since add-release-tag-publication-check archived 2026-09-01 by "
        "#563 (measured 19 at authoring, before that archive). Re-derive with "
        "`python3 scripts/validate-sequenced-after.py . --sweep` and move this "
        "pin in the SAME COMMIT, recording in the MOVEMENT LOG above which "
        "subject moved and why — archiving a co-modified ACTIVE change lowers "
        "this count while leaving `co_modified` untouched, and that is the "
        "EXPECTED cause of this failure")
    assert sweep.change_ids == sweep.active + sweep.archived
    assert sweep.sole_modifiers == sweep.change_ids - sweep.co_modified
    # This change is itself a sole modifier at requirement granularity — which is
    # exactly why it declaring a parent anyway is the doctrine applied to its
    # author: declaring must never be worth less than omitting.
    assert sweep.change_ids - 2 == 153
    assert sweep.sole_modifiers - 2 == 49
    # STILL INTACT ON ITS MERITS, not by a cancelling pair of errors — checked,
    # because #563's archive landing between the authoring measurement and this
    # reading makes the coincidence worth ruling out explicitly. That archive
    # removed a CO-modified active, never a sole one, so `active_sole` read 11
    # both before it (`518c670b`) and after it (`ded8b9f1`), and moved to 12
    # only at `43cf5933`, when THIS change added itself as an active sole
    # modifier. PR #548 adds the second post-authoring active sole modifier, so
    # `- 2` subtracts both while preserving the clearing-dispatch live baseline.
    assert sweep.active_sole - 2 == 12
    assert sweep.prose_headers == 3 and sweep.prose_headers_archived == 3
    assert sweep.declaring == 2
    assert sweep.declaring_ids == (
        "add-sequenced-after-substrate",
        "amend-chain-anchoring-readiness-and-durability",
    )
    assert sweep.root_claims == 0


def test_the_live_sweep_records_a_NON_ZERO_deepest_chain():
    # The first post-adoption reading: no longer "0 hops BY CONSTRUCTION".
    sweep = sa.corpus_sweep(ROOT)
    assert sweep.deepest_chain == 1
    assert sweep.deepest_chain_change == "add-sequenced-after-substrate"
    assert "ZERO EVIDENCE" not in sweep.render()


def test_the_sweep_is_RE_RUNNABLE_from_the_validator_CLI():
    result = subprocess.run(
        [sys.executable, str(VALIDATOR), str(ROOT), "--sweep"],
        capture_output=True, text=True)
    assert result.returncode == 0, result.stdout + result.stderr
    assert "DEEPEST DECLARED CHAIN RESOLVED" in result.stdout
    assert "co-modified at requirement granularity" in result.stdout
