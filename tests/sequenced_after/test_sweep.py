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
    - `active_co_modified` reads 17, and read 18 above. It moved on 2026-09-02,
      when PR #571 archived `govern-sibling-added-modified-deltas` — an ACTIVE
      change carrying TWO `## MODIFIED Requirements` blocks (over
      `release-realization`'s 'Ordered deltas and branch vocabulary' and
      `doc-health`'s 'A modified-block-currency finding its own class map cannot
      place is itself a finding'), therefore co-modified. THE SAME SHAPE AS
      #563's move and for the same reason: the archive moved the change out of
      the active corpus and into the archived one (active 30 → 29, archived
      123 → 124), so `active_co_modified` fell 18 → 17 while the corpus-wide
      `co_modified` held at 104 — the change is still a co-modifier, it is
      simply no longer an ACTIVE one. MEASURED ON BOTH SIDES rather than
      inferred from the failure: the sweep reads `30 active + 123 archived`,
      `104`, `49`, `18 / 12` at `bbbbeda9` (`origin/main`) and
      `29 active + 124 archived`, `104`, `49`, `17 / 12` at `da5882b4` (this
      branch), so EXACTLY ONE of this test's pins moves and every other
      assertion below is re-derived unchanged. `active_sole` is untouched at 12,
      that archive having removed a CO-modified active and never a sole one, so
      the `- 1` still subtracts `add-sequenced-after-substrate` alone and still
      recovers the authoring 11.
    - MERGING the two branches together COMPOUNDS the two moves rather than
      colliding them: PR #555's own-directory landing (bullet above) moves
      `change_ids - 1`, `sole_modifiers - 1` and `active_sole - 1` by +1 each
      and leaves `active_co_modified` untouched; PR #571's archive (bullet
      above) moves `active_co_modified` alone and leaves the other three
      where PR #555 left them. The two moved pins are DISJOINT, so combining
      them needs no new number: the live sweep on this merge reads
      `30 active + 124 archived` = 154 change ids, `104` co-modified, `50`
      sole modifiers, `17 / 13` active co-modified/sole — exactly
      `153 + 1`, `49 + 1` and `12 + 1` on PR #555's three pins, with
      `active_co_modified` holding at PR #571's own 17 (a sole-modifier
      landing cannot move a co-modified count). Every assertion below is
      therefore RE-DERIVED UNCHANGED from what each side already asserted on
      its own — confirmed against
      `python3 scripts/validate-sequenced-after.py . --sweep` run on the
      merged tree, not assumed from the arithmetic. This is the reading THIS
      TEST pinned at `b32c2fb6`, the commit that closed PR #571's own prior
      merge of `main` — the branch tip this new merge starts from.
    - `co_modified` reads 105, `active_co_modified` reads 19 and
      `change_ids - 1` reads 154 — each one up from the reading the entry above
      left. They moved on 2026-09-02 when `declare-spent-bundle-state` was
      AUTHORED: one more ACTIVE change, and unlike `add-clearing-dispatch-boundary`
      it carries a `## MODIFIED Requirements` block — over `doc-health`'s
      promoted `Release-tag publication` requirement — so it is a CO-modifier
      rather than a sole one, and both co-modified readings rise while
      `sole_modifiers - 1` and `active_sole - 1` hold at 49 and 12. THE TWO
      ENTRIES ABOVE AND THIS ONE ARE THE SAME RULE APPLIED TWICE IN TWO DAYS,
      and the pair is worth reading together: an ADDED-only packet moves the
      sole-modifier readings and leaves the co-modified ones, a packet carrying
      a MODIFIED block does the exact opposite, and a packet that moved BOTH
      would be a defect in the sweep rather than a corpus event. The pin moves
      in the SAME COMMIT as the corpus, which is this test's own protocol, and
      that packet's PR discloses that it touches this file for that reason and
      for no other: it is corpus BOOKKEEPING, not the realization its OD-8
      splits off to a later PR. `declaring` holds at 1 — it declares NO
      `sequenced_after:` field, the field being carried by an ACTIVE, UNPROMOTED
      change, and adopting an unratified surface is not what the "declaring must
      never be worth less than omitting" doctrine asks of a packet written
      before that change lands. `validate-sequenced-after.py` passes over the
      corpus with it in place. THIS IS `main`'S OWN READING, taken against the
      18-baseline `main` shared with this branch before PR #571's archive —
      `main` has no knowledge of that archive, which is why it reads
      `active_co_modified` as 19 rather than the 18 the merge below settles on.
    - MERGING THIS BRANCH'S OWN READING (17 / 13 active co-modified/sole, 104
      co-modified, 154 change ids, above) WITH `main`'S READING (19, 105, 155 —
      above) compounds two DISJOINT-LOOKING but actually OPPOSED moves on one
      pin: both moves are measured from the SAME 18-baseline
      `active_co_modified` the two branches last shared (after #563's archive,
      before either #571's archive or `declare-spent-bundle-state`'s
      authoring), so PR #571's archive (18 → 17, an ACTIVE co-modifier leaving
      the active corpus) and `declare-spent-bundle-state`'s authoring (18 → 19,
      an ACTIVE co-modifier entering it) CANCEL rather than compound:
      `active_co_modified` reads 18 on the merged tree — neither branch's own
      number, and not `17 + 1` or `19 - 1` by coincidence but by the same
      subtraction and addition both landing back on the shared base.
      `co_modified` carries `main`'s move forward unopposed (104 → 105: an
      archive never shrinks the corpus-wide co-modified count, only a newly
      authored MODIFIED-block change grows it, and this merge has exactly one
      of those), and `change_ids` carries both branches' additions (154 → 155:
      `declare-spent-bundle-state` is one more active change stacked on the
      merge that already carried #555's landing and #571's archive).
      `sole_modifiers`, `active_sole` and their `- 1` readings are untouched by
      either move and hold at 50/49 and 13/12. MEASURED ON THE MERGED TREE, not
      inferred from the arithmetic: `31 active + 124 archived` = 155 change
      ids, `105` co-modified, `50` sole modifiers, `18 / 13` active
      co-modified/sole, via
      `python3 scripts/validate-sequenced-after.py . --sweep` run after this
      merge.
    - `co_modified` reads 107, `active_co_modified` reads 20, `change_ids`
      reads 156 and `active` reads 32 — each one up from the reading the entry
      above left. They moved on 2026-09-02 when PR #560
      (`add-cpc-clearing-boundary`) merged: one more ACTIVE change, and it
      carries a `## MODIFIED Requirements` block — THREE requirements over
      `clearing-dispatch-boundary` ("Work crosses the boundary only as a
      sealed bounded request", "Every verifiable field is verified against the
      provider's authoritative API", "Every dispatch is recorded, and the
      single door is attested rather than assumed") — so it is itself a
      CO-modifier. All three of those titles trace to the SAME single earlier
      active change, `add-clearing-dispatch-boundary`, which owned all three
      and, before this PR, shared none of its ten requirement keys with any
      other change in the corpus — it was SOLE. A change's co-modified/sole
      status is BOOLEAN, not a count of its shared titles, so sharing three
      keys with one other change flips it ONCE: `co_modified` rises by exactly
      TWO — the new change entering the set (+1) and
      `add-clearing-dispatch-boundary` leaving `sole` for it (+1) — never by
      three or four. `active_co_modified` rises by the same two, since both
      changes are ACTIVE. `sole_modifiers` and `active_sole` each fall by
      exactly one — the one flipped change leaving the sole set — landing at
      49 and 12. `change_ids` and `active` each rise by one —
      `add-cpc-clearing-boundary` itself entering the corpus as one more
      active change — landing at 156 and 32; `archived` holds at 124, prose
      headers hold at 3 (3 archived), and `declaring`/`root_claims` hold at
      1/0, none of which is this PR's business. MEASURED, not inferred:
      excluding `add-cpc-clearing-boundary` from the corpus reproduces the
      entry above's own reading EXACTLY (155 change ids, 105 co-modified, 50
      sole modifiers, 18 / 13 active co-modified/sole), and
      `add-clearing-dispatch-boundary` is independently confirmed absent from
      the co-modified set on that exclusion — so the entire two-count rise is
      this one PR's contribution and no other change moved in the same window.
      Via `python3 scripts/validate-sequenced-after.py . --sweep` run on this
      branch's own catch-up merge with `main` (commit `f7865ffc`):
      `32 active + 124 archived` = 156 change ids, `107` co-modified, `49`
      sole modifiers, `20 / 12` active co-modified/sole.
    - `co_modified` reads 108, `active_co_modified` reads 21 and `change_ids`
      reads 157 — each up by exactly ONE from the entry above, and the ONE is
      what makes this entry worth writing rather than a repetition of it.
      They moved on 2026-09-02 when `add-project-repo-schema` was authored: one
      more ACTIVE change, carrying a `## MODIFIED Requirements` block over
      `ideation-dashboard`'s "Project grouping hierarchy", so it is itself a
      CO-modifier. **IT RISES BY ONE AND NOT BY TWO, and the difference from
      #560 is the STANDING OF THE EARLIER WRITERS rather than anything about
      this change.** #560 rose by two because the one earlier writer of its
      three keys, `add-clearing-dispatch-boundary`, had shared no key with
      anything and was SOLE — so it flipped, and a flip is a second increment.
      The earlier writers here are TWO ARCHIVED changes,
      `archive/2026-08-06-add-project-scoped-selection` and
      `archive/2026-07-29-add-ideation-dashboard`, which already shared that
      requirement key WITH EACH OTHER and were therefore already co-modified
      before this change existed. Nothing flips; only the newcomer enters. That
      is why `sole_modifiers` and `active_sole` are UNTOUCHED at 49 and 12 —
      the rise-by-two shape is always accompanied by a sole set falling, and
      the rise-by-one shape never is, which makes the two readings a check on
      each other rather than two numbers to remember. `archived` holds at 124,
      prose headers hold at 3 (3 archived), and `declaring`/`root_claims` hold
      at 1/0. MEASURED, not inferred: the same sweep run on this branch's
      merge-base (`origin/main` at `c0270d28`) reproduces the entry above
      EXACTLY — 156 change ids, 107 co-modified, 49 sole modifiers, 20 / 12
      active co-modified/sole — so the entire one-count rise is this one
      change's contribution and no other change moved in the same window. Via
      `python3 scripts/validate-sequenced-after.py . --sweep`:
      `33 active + 124 archived` = 157 change ids, `108` co-modified, `49`
      sole modifiers, `21 / 12` active co-modified/sole.
    """
    sweep = sa.corpus_sweep(ROOT)
    assert sweep.co_modified == 108, (
        "108 since add-project-repo-schema was authored 2026-09-02: it "
        "carries a `## MODIFIED Requirements` block over "
        "ideation-dashboard's \"Project grouping hierarchy\", so it joined the "
        "co-modified population — and it raised this count by exactly ONE, "
        "not two, because the only earlier writers of that key are TWO "
        "ARCHIVED changes that already shared it with each other and were "
        "already co-modified, so nothing flipped and `sole_modifiers` held "
        "at 49. A rise of two always comes with the sole set falling; a rise "
        "of one never does. It read 107 "
        "since add-cpc-clearing-boundary (PR #560, 2026-09-02), which carries "
        "three `## MODIFIED Requirements` blocks over "
        "clearing-dispatch-boundary — all three tracing to the single "
        "earlier active change add-clearing-dispatch-boundary, previously "
        "SOLE, now flipped to CO-modified by sharing those three keys with "
        "#560 (a change's co-modified membership is boolean, so three shared "
        "titles flip it ONCE, not three times: `co_modified` rises by "
        "exactly two — #560 itself entering the set and "
        "add-clearing-dispatch-boundary leaving `sole` for it). It read 105 "
        "since declare-spent-bundle-state was authored 2026-09-02 on "
        "main, which is the change that raised it: it carries a `## MODIFIED "
        "Requirements` block, so it joined the co-modified population. It "
        "read 104 at THIS test's own authoring — add-sequenced-after-substrate's "
        "ADDED requirement titles being NOVEL, so that change is a SOLE "
        "modifier and moved this count not at all — and held at 104 through "
        "#563's archive, #555's ADDED-only landing, and #571's archive (an "
        "archive moves `active_co_modified`, never the corpus-wide "
        "`co_modified`). ANY later change carrying a MODIFIED block raises it "
        "again, which is one of the two EXPECTED causes of this failure")
    assert sweep.active_co_modified == 21, (
        "21 since add-project-repo-schema was authored 2026-09-02 as one "
        "more ACTIVE co-modifier entering the active corpus — by ONE and not "
        "two, because the earlier writers of the requirement key it shares "
        "are both ARCHIVED and were already co-modified, so no ACTIVE change "
        "flipped and `active_sole` held at 12. It read 20 "
        "since add-cpc-clearing-boundary (PR #560, 2026-09-02), which is "
        "itself an ACTIVE co-modifier entering the active corpus AND flips "
        "add-clearing-dispatch-boundary — also ACTIVE — from sole to "
        "co-modified by sharing three requirement keys with it: two ACTIVE "
        "co-modifiers entering the set at once, so `active_co_modified` rises "
        "by two rather than one. It read 18 on the merged tree: PR #571 archived govern-sibling-added-modified-"
        "deltas (an ACTIVE co-modifier leaving the active corpus, 18 → 17 on "
        "this branch alone) the SAME DAY main authored declare-spent-bundle-"
        "state (an ACTIVE co-modifier entering it, 18 → 19 on main alone) — "
        "both measured from the same 18-baseline the two branches last shared "
        "after #563's archive 2026-09-01, so the two moves CANCEL on this "
        "merge rather than compound. Re-derive with "
        "`python3 scripts/validate-sequenced-after.py . --sweep` and move this "
        "pin in the SAME COMMIT, recording in the MOVEMENT LOG above which "
        "subject moved and why — archiving a co-modified ACTIVE change lowers "
        "this count while leaving `co_modified` untouched, and AUTHORING one "
        "raises BOTH, which are two different EXPECTED causes of this failure "
        "and must not be confused")
    assert sweep.change_ids == sweep.active + sweep.archived
    assert sweep.sole_modifiers == sweep.change_ids - sweep.co_modified
    # This change is itself a sole modifier at requirement granularity — which is
    # exactly why it declaring a parent anyway is the doctrine applied to its
    # author: declaring must never be worth less than omitting.
    assert sweep.change_ids - 1 == 156, (
        "the `- 1` subtracts THIS change and nothing else, so the reading is "
        "the corpus without it: 152 at authoring, 153 when "
        "add-clearing-dispatch-boundary landed 2026-09-01, 154 when "
        "declare-spent-bundle-state was authored 2026-09-02, 155 when "
        "add-cpc-clearing-boundary (PR #560) merged 2026-09-02, 156 when "
        "add-project-repo-schema was authored 2026-09-02")
    # MOVED 2026-09-02: `sole_modifiers` fell 50 → 49 for the same reason
    # `active_sole` falls below — add-clearing-dispatch-boundary left the sole
    # set when add-cpc-clearing-boundary (PR #560) began sharing three
    # requirement keys with it. The `- 1` still subtracts only
    # add-sequenced-after-substrate (unaffected, still sole).
    assert sweep.sole_modifiers - 1 == 48
    # STILL INTACT ON ITS MERITS, not by a cancelling pair of errors — checked,
    # because #563's archive landing between the authoring measurement and this
    # reading makes the coincidence worth ruling out explicitly. That archive
    # removed a CO-modified active, never a sole one, so `active_sole` read 11
    # both before it (`518c670b`) and after it (`ded8b9f1`), and moved to 12
    # only at `43cf5933`, when THIS change added itself as an active sole
    # modifier. The `- 1` therefore still subtracts exactly this change and
    # still recovers the authoring 11.
    #
    # MOVED AGAIN 2026-09-02: `active_sole` fell 13 → 12 when
    # add-cpc-clearing-boundary (PR #560) flipped
    # add-clearing-dispatch-boundary — an ACTIVE change, previously sole — to
    # co-modified by sharing three requirement keys with it. UNLIKE #563's
    # archive, this move DOES touch an active sole modifier, which is exactly
    # the failure mode the note above ruled out for that earlier case; here it
    # is the actual cause. The `- 1` still subtracts only
    # add-sequenced-after-substrate (unaffected, still sole), so the reading
    # falls with `active_sole` to 11.
    assert sweep.active_sole - 1 == 11
    assert sweep.prose_headers == 3 and sweep.prose_headers_archived == 3
    assert sweep.declaring == 1
    assert sweep.declaring_ids == ("add-sequenced-after-substrate",)
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
