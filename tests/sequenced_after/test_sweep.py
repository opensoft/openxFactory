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
    - SIBLING READING, taken from the SAME merge-base as the entry above
      (`origin/main` at `c0270d28`) and therefore NOT a step after it:
      `change_ids - 1` reads 156, `sole_modifiers - 1` reads 49 and
      `active_sole - 1` reads 12 — each one up from the reading the
      `add-cpc-clearing-boundary` entry left, and `co_modified` and
      `active_co_modified` hold at 107 and 20. They
      moved on 2026-09-03 when `update-standards-body-current-publications` was
      ADOPTED as an ACTIVE change (PR #593, the rescue of work stranded
      uncommitted in a shared checkout, openxFactory issue #591). ITS DELTA IS
      `## ADDED Requirements` ONLY, over a NEW capability `standards-body-registry`
      whose four requirement titles exist nowhere else in the corpus, so it is a
      SOLE modifier and never a co-modifier — the exact shape
      `add-clearing-dispatch-boundary`'s own landing had, and the exact OPPOSITE
      of `declare-spent-bundle-state`'s and `add-cpc-clearing-boundary`'s, which
      carried MODIFIED blocks and moved the two co-modified readings instead. A
      packet moving BOTH would still be a defect in the sweep rather than a
      corpus event.
      THE MOVE IS ONE STEP AND NOT TWO, which is the part specific to a rescue:
      the snapshot placed the packet under `openspec/changes/archive/2026-09-01-...`,
      where it ALREADY counted as one archived change id and one sole modifier,
      so `git mv`-ing it to the active corpus moves the ACTIVE/ARCHIVED SPLIT
      and `active_sole` alone — while `change_ids` and `sole_modifiers` were
      raised by the snapshot's own landing rather than by the move.
      THIS ENTRY WAS RE-DERIVED ONCE, and the first reading is left here as the
      record of why: it was authored against the `main` of 2026-09-03 00:0xZ and
      read `155 / 50 / 13` with `co_modified` 105 and `active_co_modified` 18.
      PR #560 (`add-cpc-clearing-boundary`) then merged and this branch took the
      catch-up merge, which moves FOUR of the five pins under it — the entry
      above says how — so every number was measured again on the merged tree
      rather than adjusted by arithmetic. MEASURED ON BOTH SIDES: `origin/main`
      at `c0270d28` reads `32 active + 124 archived` = 156, `107`, `49`,
      `20 / 12`; this branch after the merge reads `33 active + 124 archived`
      = 157, `107`, `50`, `20 / 13`, via
      `python3 scripts/validate-sequenced-after.py . --sweep` on each tree. The
      pin moves in the SAME COMMIT as the corpus, which is this test's own
      protocol, and that PR discloses that it touches this file for that reason
      and for no other: corpus BOOKKEEPING, not realization. `declaring` holds
      at 1 — the packet declares no `sequenced_after:` field, the field being
      carried by an ACTIVE, UNPROMOTED change.
    - MERGING THE TWO SIBLING ENTRIES ABOVE COMPOUNDS EXACTLY ONE PIN, and the
      reason is the boolean-membership rule both of them already invoke:
      the two packets move DISJOINT sets. `add-project-repo-schema` carries a
      MODIFIED block, so it moved the two CO-modified readings alone
      (`co_modified` 107 → 108, `active_co_modified` 20 → 21) and left the sole
      readings where they were; `update-standards-body-current-publications` is
      ADDED-only over a NEW capability, so it moved the two SOLE readings alone
      (`sole_modifiers - 1` 48 → 49, `active_sole - 1` 11 → 12) and left the
      co-modified readings where they were. Only `change_ids` is moved by BOTH —
      each is one more ACTIVE change — so it alone compounds: `change_ids - 1`
      reads 156 on either branch taken singly and 157 on the merge. NO PIN HERE
      IS THE NET OF TWO OPPOSED MOVES, which is what makes this merge different
      from the 2026-09-02 `active_co_modified` reconciliation four entries above,
      where an archive and an authoring cancelled on one pin; here nothing
      cancels and only the population grows twice.
      MEASURED ON ALL THREE TREES rather than inferred from the arithmetic, via
      `python3 scripts/validate-sequenced-after.py . --sweep`: `origin/main` at
      `ee294f9f` reads `33 active + 124 archived` = 157 change ids, `108`
      co-modified, `49` sole modifiers, `21 / 12` active co-modified/sole; this
      branch at `1d9ae04c` reads `33 active + 124 archived` = 157, `107`, `50`,
      `20 / 13`; the merge of the two reads `34 active + 124 archived` = 158,
      `108`, `50`, `21 / 13`. AND MEASURED BY EXCLUSION, which is the step that
      rules out a THIRD change having moved in the same window: dropping
      `add-project-repo-schema` from the merged corpus reproduces this branch's
      own reading EXACTLY (157, 107, 50, 20 / 13), and dropping
      `update-standards-body-current-publications` reproduces `main`'s EXACTLY
      (157, 108, 49, 21 / 12) — so every count above is the two named packets'
      contribution and no other's. `archived` holds at 124, prose headers hold
      at 3 (3 archived), and `declaring`/`root_claims` hold at 1/0, none of
      which either packet touches. The pin moves in the SAME COMMIT as the
      corpus — here the merge commit itself, PR #593's catch-up with `main` of
      2026-09-03, taken to re-fire the `pull_request` checks GitHub had skipped
      while the test-merge commit could not be built — which is this test's own
      protocol.
    - `active_co_modified` reads 20, and read 21 above. It moved on 2026-09-03,
      when `declare-spent-bundle-state` was ARCHIVED — the change whose
      AUTHORING raised `co_modified` 104 → 105 and `active_co_modified`
      18 → 19 several bullets above. THE SAME SHAPE AS #563's and #571's moves,
      and for the same reason: archiving a co-modified ACTIVE change moves it
      out of the active corpus and into the archived one, so
      `active_co_modified` falls by exactly one while the corpus-wide
      `co_modified` — a count of REQUIREMENT-KEY pairings, which an archive
      never un-shares — holds at 108.
      THIS ENTRY REPLACES THE ONE PR #611 FIRST WROTE, and the two are not both
      kept because they CONTRADICT on the split. #611's reasoning was right and
      its arithmetic went stale: it was authored 2026-09-03T03:55Z against the
      `main` of 2026-09-02 (`ee294f9f`, `33 active + 124 archived`) and recorded
      the after-state as `32 active + 125 archived` = 157. Two commits then
      landed on `main` before this branch could merge — PR #593 (`3c237cd0`),
      which ADOPTED `update-standards-body-current-publications` as an ACTIVE
      change, and PR #589 (`6da1e1f5`), which hardened the SPENT containment
      guard — so the before-state this archive actually acts on is
      `34 active + 124 archived` = 158 and the after-state is
      `33 active + 125 archived` = 158. The TOTAL being unchanged is the
      invariant that entry was making and it survives; both of its addends were
      one lower than the corpus now carries, so the corrected reading is
      recorded here and the stale one is removed rather than left to contradict
      it. Corrected by lane openxfactory-1d, 2026-09-03, while resolving #611's
      conflict with `main`.
      MEASURED ON BOTH TREES rather than adjusted by arithmetic, via
      `python3 scripts/validate-sequenced-after.py . --sweep`: `origin/main` at
      `6da1e1f5` reads `34 active + 124 archived` = 158 change ids, `108`
      co-modified, `50` sole modifiers, `21 / 13` active co-modified/sole; this
      merge reads `33 active + 125 archived` = 158, `108`, `50`, `20 / 13`.
      EXACTLY ONE PIN MOVES — `active_co_modified` 21 → 20 — and `main`'s own
      reading IS the by-exclusion control, this archive being the only
      difference between the two trees. `change_ids - 1` holds at 157 (moving
      one change between buckets cannot change the total), `sole_modifiers - 1`
      holds at 49 (this change was always a co-modifier and never a sole one),
      and `active_sole - 1` holds at 12 (an archive of a co-modified active
      never touches the sole set) — the three #593 last moved, re-derived on the
      merged tree rather than assumed to have survived it. `archived` rises
      124 → 125; prose headers hold at 3 (3 archived); `declaring`/`root_claims`
      hold at 1/0. The promoted `doc-health` requirement this change's
      `## MODIFIED Requirements` block targeted is now CANON rather than an
      active delta, which is what makes the change a FORMER co-modifier rather
      than a present one. The pin moves in the SAME COMMIT as the corpus — here
      the merge commit that resolves this conflict — which is this test's own
      protocol.
    - RE-DERIVED A THIRD TIME 2026-09-03, on the merge of `main` at `2b0615da`
      (after #611 archived `declare-spent-bundle-state`, then #614, #602,
      #604) into the `create-medxchart-overlay-boundary` RATIFICATION branch,
      and this is the entry that stands: `co_modified` reads 109,
      `active_co_modified` reads 21, `sole_modifiers` falls to 49 (`- 1`: 48)
      and `active_sole` to 12 (`- 1`: 11), while `change_ids` HOLDS at 158
      (`- 1`: 157).
      MAIN'S PIN IS ALREADY FULLY ACCOUNTED FOR BY THE ENTRY DIRECTLY ABOVE,
      which is #611's own archive of `declare-spent-bundle-state` and left
      `main` reading `33 active + 125 archived` = 158 change ids, `108`
      co-modified, `50` sole modifiers, `20 / 13` active co-modified/sole —
      the baseline this entry starts from. Three more commits landed on
      `main` in the same window this branch's catch-up merge crosses — #614
      (pins one `--as-of` clock across the self-gate's own two report
      renderings), #602 (a workspace-record re-pointer) and #604 (an
      oversized-upload rename guard) — and NONE moves this pin: a claim
      MEASURED, not assumed, via `git diff --stat 6da1e1f5..2b0615da --
      openspec/changes/`, which is empty over that range once #611's own
      `declare-spent-bundle-state` move is set aside.
      THIS BRANCH'S OWN CONTRIBUTION IS UNCHANGED IN SHAPE A THIRD TIME, only
      restated from main's newer baseline: its `## MODIFIED Requirements`
      block over `domain-descendant-boundary`'s 'A descendant is placed at a
      ratified placement' adds +1 `co_modified` and +1 `active_co_modified`
      and takes -1 `sole_modifiers` and -1 `active_sole` RELATIVE TO MAIN'S
      PIN, and moves `change_ids` and `active` not at all — the same THIRD
      CAUSE the first entry named (RATIFYING an already-active change moves
      four membership readings and no population count), read against a
      baseline that has now moved twice under it without the shape itself
      ever changing.
      MEASURED BY EXCLUSION ON THE MERGED TREE, not inferred and not carried
      over from either earlier measurement:
      `python3 scripts/validate-sequenced-after.py . --sweep` on the merged
      tree reads `33 active + 125 archived` = 158 change ids, `109`
      co-modified, `49` sole modifiers, `21 / 12` active co-modified/sole; the
      SAME sweep on the merged tree with only
      `openspec/changes/create-medxchart-overlay-boundary/specs/domain-descendant-boundary/`
      moved aside reads `33 active + 125 archived` = 158, `108`, `50`,
      `20 / 13` — MAIN'S PIN EXACTLY — and that reading is independently
      confirmed by running the same sweep on `origin/main` at `2b0615da`
      itself, which prints the same 158, `108`, `50`, `20 / 13`. So that one
      delta directory is the whole of the difference between the two trees a
      third time and no fourth change moved in the window. `archived` holds
      at 125 (unmoved by this ratification: #611's archive of
      `declare-spent-bundle-state` already set it there and this packet
      archives nothing), prose headers hold at 3 (3 archived), and
      `declaring`/`root_claims` hold at 1/0, none of which this ratification
      touches. The pin moves in the SAME COMMIT as the corpus — here the
      merge commit itself — which is this test's own protocol.
    - `active_co_modified` reads 19, and read 20 above. It moved on 2026-09-03,
      when `add-project-repo-schema` was ARCHIVED — the change whose AUTHORING
      raised `co_modified` 107 → 108 and `active_co_modified` 20 → 21 several
      bullets above, on the very same `## MODIFIED Requirements` block (over
      `ideation-dashboard`'s "Project grouping hierarchy"). THE SAME SHAPE AS
      #563's, #571's and `declare-spent-bundle-state`'s own archives: archiving
      a co-modified ACTIVE change moves it out of the active corpus and into
      the archived one, so `active_co_modified` falls by exactly one while the
      corpus-wide `co_modified` — a count of REQUIREMENT-KEY pairings, which an
      archive never un-shares — holds at 108. The archive was gated on
      `add-project-repo-schema`'s own `tasks.md` 9.3, the cut of
      `contract-v3.1` carrying `scripts/validate-ideation-dashboard-
      contracts.py`'s new bytes, per `release-realization`'s realization
      archive gate for a code-surface change — this move is therefore dated to
      the CUT landing rather than to the ratification several bullets above.
      MEASURED ON BOTH TREES rather than adjusted by arithmetic, via
      `python3 scripts/validate-sequenced-after.py . --sweep`: `origin/main` at
      `7af2725c` reads `33 active + 125 archived` = 158 change ids, `108`
      co-modified, `50` sole modifiers, `20 / 13` active co-modified/sole; this
      branch after the archive reads `32 active + 126 archived` = 158, `108`,
      `50`, `19 / 13`. EXACTLY ONE PIN MOVES — `active_co_modified` 20 → 19 —
      and `main`'s own reading IS the by-exclusion control, this archive being
      the only difference between the two trees. `change_ids - 1` holds at 157
      (moving one change between buckets cannot change the total),
      `sole_modifiers - 1` holds at 49 (this change was always a co-modifier
      and never a sole one), and `active_sole - 1` holds at 12 (an archive of a
      co-modified active never touches the sole set). `archived` rises
      125 → 126; prose headers hold at 3 (3 archived); `declaring`/`root_claims`
      hold at 1/0. The promoted `project-repo-schema` capability (eleven ADDED
      requirements) and the promoted `ideation-dashboard` requirement this
      change's `## MODIFIED Requirements` block targeted are now CANON rather
      than an active delta, which is what makes the change a FORMER
      co-modifier rather than a present one. **THIS PULL REQUEST WAS AUTHORED
      AGAINST `origin/main` AT `7af2725c` WHILE PRs #608 AND #609 WERE LANDING
      SEPARATELY**, per the coordinating session's instruction not to rebase
      repeatedly — so this pin, like the README OpenSpec Records block, is a
      KNOWN, NAMED conflict point that MUST be re-measured against `main`'s
      post-#608/#609 state before merge rather than resolved by taking either
      side blind. The pin moves in the SAME COMMIT as the corpus — here the
      archive commit — which is this test's own protocol.
    - MERGE-RESOLVED 2026-09-03, on the merge of `main` at `0bf37d14` — the
      ratifications of `create-medxchart-overlay-boundary` (#608) and
      `create-medxpractice-overlay-boundary` (#609), plus #614, #602, #604,
      #601, #599 and #603 — into this `contract-v3.1` CUT branch:
      `active_co_modified` reads 20, WHICH IS NEITHER SIDE'S NUMBER, and that
      is the point. The two bullets directly above are BOTH live and they move
      the SAME pin in OPPOSITE directions from the SAME 20-baseline each
      started from: #608's RATIFICATION made an ALREADY-ACTIVE change a
      co-modifier (20 -> 21), and this branch's ARCHIVE of
      `add-project-repo-schema` moved a co-modified ACTIVE change out of the
      active corpus (20 -> 19). On the merged tree both are true at once and
      the two moves CANCEL at 20. Taking either side wholesale would have been
      wrong, in opposite directions.
      MEASURED ON BOTH TREES rather than netted by arithmetic, via
      `python3 scripts/validate-sequenced-after.py . --sweep`: `origin/main` at
      `0bf37d14` reads `33 active + 125 archived` = 158 change ids, `109`
      co-modified, `49` sole modifiers, `21 / 12` active co-modified/sole; the
      merged tree reads `32 active + 126 archived` = 158, `109`, `49`,
      `20 / 12`. EXACTLY ONE READING DIFFERS — `active_co_modified` 21 -> 20 —
      and `main`'s own reading IS the by-exclusion control, this archive being
      the only difference between the two trees. Every OTHER pin in this test
      therefore keeps MAIN'S post-#608/#609 value, unmoved by the archive:
      `co_modified` holds at 109 (an archive never un-shares a REQUIREMENT-KEY
      pairing), `sole_modifiers - 1` holds at 48 (this change was always a
      co-modifier and never a sole one), `active_sole - 1` holds at 11 (an
      archive of a co-modified active never touches the sole set), and
      `change_ids - 1` holds at 157 (moving one change between buckets cannot
      change the total). `active` falls 33 -> 32 and `archived` rises
      125 -> 126; prose headers hold at 3 (3 archived); `declaring` /
      `root_claims` hold at 1/0. #609 moves NONE of these: its delta is over
      the novel `medxpractice-overlay-boundary` titles and it carries no
      `## MODIFIED Requirements` block, so it was and remains a SOLE modifier.
      The pin moves in the SAME COMMIT as the corpus — here the merge commit
      that resolves this conflict — which is this test's own protocol.
    - `co_modified` reads 111, `active_co_modified` reads 22,
      `change_ids - 1` reads 158 and `sole_modifiers - 1` falls to 47, while
      `active_sole - 1` HOLDS at 11. They moved on 2026-09-03 when
      `amend-owner-layer-severity` was AUTHORED (lane `openxfactory-smalls`,
      openxFactory issues #561 and #339): one more ACTIVE change, carrying TWO
      `## MODIFIED Requirements` blocks — over `workflow-gate-contract`'s
      'Owner layer constraint' and `release-surface-integrity`'s 'The declared
      bundle describes the release surface' — so it is itself a CO-modifier.
      THE RISE IS TWO AND THE SOLE SET FALLS BY ONE, which is the
      `add-cpc-clearing-boundary` shape rather than the `add-project-repo-schema`
      one, and the STANDING OF THE EARLIER WRITERS is again what decides it:
      the earlier writer of the `release-surface-integrity` key,
      `archive/2026-08-25-add-release-inventory-drift-check`, was ALREADY
      co-modified and does not flip; the earlier writer of the
      `workflow-gate-contract` key,
      `archive/2026-07-09-promote-workflow-gate-contract`, was SOLE and DOES —
      so `co_modified` rises by exactly two (the newcomer entering, that one
      change leaving `sole` for it) and `sole_modifiers` falls by exactly one.
      Sharing keys with TWO earlier changes flips membership ONCE for each of
      them and never twice for either, membership being boolean.
      `active_co_modified` rises by ONE and not two, and `active_sole` holds,
      because the change that flipped is ARCHIVED: an archived flip cannot
      enter or leave an ACTIVE population. `change_ids` rises by one
      (`33 active + 125 archived` = 158 becomes `34 active + 125 archived` =
      159), `archived` holds at 125, prose headers hold at 3 (3 archived), and
      `declaring`/`root_claims` hold at 1/0 — the packet declares no
      `sequenced_after:` field, the field being carried by an ACTIVE,
      UNPROMOTED change.
      MEASURED ON BOTH TREES AND BY EXCLUSION rather than inferred from the
      arithmetic, via `python3 scripts/validate-sequenced-after.py . --sweep`:
      `origin/main` at `0bf37d14` reads `33 active + 125 archived` = 158 change
      ids, `109` co-modified, `49` sole modifiers, `21 / 12` active
      co-modified/sole; this branch reads `34 active + 125 archived` = 159,
      `111`, `48`, `22 / 12`; and the SAME sweep on this branch with only
      `openspec/changes/amend-owner-layer-severity/specs/` moved aside reads
      `159`, `109`, `50`, `21 / 13` — the packet still present as one more
      change id but owning no requirement key, which reproduces main's two
      co-modified readings EXACTLY and isolates the entire move to those two
      delta directories. The pin moves in the SAME COMMIT as the corpus, which
      is this test's own protocol, and that PR discloses that it touches this
      file for that reason and for no other: corpus BOOKKEEPING, not a code
      surface — the packet declares `code_surface: none` and names this pin in
      that declaration.
    - `active_co_modified` reads 21, and read 22 in the entry directly above.
      It moved LATER THE SAME DAY AND IN THE SAME PULL REQUEST, when
      `amend-owner-layer-severity` was ARCHIVED — the packet whose AUTHORING
      the entry above records. THE TWO ENTRIES ARE ONE COMMIT'S TWO HALVES,
      which is what a doc-only packet looks like on this pin: `code_surface:
      none` makes the archive gate LANDING rather than merged-plus-green, so
      the authoring and the archive ride one PR and this pin is moved TWICE
      before anything is pushed. Both halves are recorded rather than netted,
      because a reader who sees only the net reading cannot tell an archived
      packet from one that was never authored.
      THE SHAPE IS #563'S, #571'S AND #611'S, and for their reason: archiving
      a co-modified ACTIVE change moves it out of the active corpus and into
      the archived one, so `active_co_modified` falls by exactly one while the
      corpus-wide `co_modified` — a count of REQUIREMENT-KEY pairings, which an
      archive never un-shares — HOLDS at 111. `change_ids - 1` holds at 158
      (moving a change between buckets cannot change the total),
      `sole_modifiers - 1` holds at 47 (this change was always a co-modifier
      and never a sole one, and `promote-workflow-gate-contract`, the change it
      flipped out of `sole`, was already archived), and `active_sole - 1` holds
      at 11 (an archive of a co-modified active never touches the sole set).
      The two promoted requirements this packet's MODIFIED blocks targeted are
      now CANON rather than active deltas, which is what makes the change a
      FORMER active co-modifier rather than a present one.
      MEASURED ON BOTH SIDES OF THE ACT rather than adjusted by arithmetic, via
      `python3 scripts/validate-sequenced-after.py . --sweep`: before the
      archive the branch read `34 active + 125 archived` = 159 change ids,
      `111` co-modified, `48` sole modifiers, `22 / 12` active
      co-modified/sole; after it the branch reads `33 active + 126 archived` =
      159, `111`, `48`, `21 / 12`. EXACTLY ONE PIN MOVES, and the pre-archive
      reading is its own by-exclusion control, the archive act being the only
      difference between the two trees. `archived` rises 125 -> 126; prose
      headers hold at 3 (3 archived); `declaring`/`root_claims` hold at 1/0.
    - MERGING THE TWO ENTRIES ABOVE WITH `main` AT `19d00872` LEAVES FOUR OF
      THE FIVE PINS WHERE THIS BRANCH PUT THEM AND `active_co_modified` WHERE
      NEITHER BRANCH PUT IT, and the asymmetry is the whole content of this
      entry. `main` moved twice in the same window off the same 20-baseline —
      `create-medxchart-overlay-boundary`'s RATIFICATION (#608) 20 -> 21, then
      `add-project-repo-schema`'s ARCHIVE on its `contract-v3.1` cut (#616)
      21 -> 20 — and THIS BRANCH moved twice off that same baseline in one
      commit, the authoring 20 -> 21 and the archive 21 -> 20. FOUR MOVES,
      CANCELLING TWO-FOR-TWO, so the merged tree reads 20: not `20 + 1`, not
      `20 - 1`, and not either branch's intermediate. `co_modified`,
      `change_ids` and `sole_modifiers` compound instead of cancelling,
      because `main`'s two moves were an ACTIVE-membership ratification and an
      archive — neither of which touches a corpus-wide count — while this
      branch's authoring raised `co_modified` by two and lowered
      `sole_modifiers` by one for good.
      MEASURED ON ALL THREE TREES AND BY EXCLUSION, never adjusted by
      arithmetic, via `python3 scripts/validate-sequenced-after.py . --sweep`:
      `origin/main` at `19d00872` reads `32 active + 126 archived` = 158 change
      ids, `109` co-modified, `49` sole modifiers, `20 / 12` active
      co-modified/sole; this branch before the merge read
      `33 active + 126 archived` = 159, `111`, `48`, `21 / 12`; the merged tree
      reads `32 active + 127 archived` = 159, `111`, `48`, `20 / 12`. AND THE
      CONTROL THAT RULES OUT A THIRD MOVER: the same sweep on the merged tree
      with `openspec/changes/archive/2026-09-03-amend-owner-layer-severity/`
      moved aside reads `158`, `109`, `49`, `20 / 12` — `main`'s own reading
      EXACTLY — so this one archived packet is the whole of the difference and
      no other change moved in the window. `archived` rises 126 -> 127, prose
      headers hold at 3 (3 archived), and `declaring`/`root_claims` hold at
      1/0. The pin moves in the SAME COMMIT as the corpus — here the merge
      commit itself — which is this test's own protocol.
    """
    sweep = sa.corpus_sweep(ROOT)
    assert sweep.co_modified == 111, (
        "111 since amend-owner-layer-severity was AUTHORED 2026-09-03 with TWO "
        "`## MODIFIED Requirements` blocks — over workflow-gate-contract's "
        "'Owner layer constraint' and release-surface-integrity's 'The declared "
        "bundle describes the release surface'. It rose by TWO and not one: the "
        "newcomer entering the set, plus the ARCHIVED "
        "promote-workflow-gate-contract leaving `sole` for it, its "
        "owner-layer key having been shared with nothing until now — while the "
        "other earlier writer, the archived add-release-inventory-drift-check, "
        "was already co-modified and did not flip. A rise of two always comes "
        "with the sole set falling, and it did (49 -> 48). It read 109 "
        "since create-medxchart-overlay-boundary was RATIFIED 2026-09-03 "
        "and gained a `## MODIFIED Requirements` block over "
        "domain-descendant-boundary's 'A descendant is placed at a ratified "
        "placement'. THE THIRD EXPECTED CAUSE OF THIS FAILURE, distinct from "
        "the authoring cause and the archiving cause named below: RATIFYING "
        "an already-active change moves this pin while `change_ids` and "
        "`active` do not move at all. The rise is ONE and `sole_modifiers` "
        "FALLS with it — the same change enters co-modified and leaves sole, "
        "its only earlier co-writer being the archived split-openxwallet-repo "
        "that promoted the requirement. THE 108 IT ROSE FROM IS MAIN'S OWN, "
        "measured on the merged tree at 2b0615da: declare-spent-bundle-state's "
        "ARCHIVE (#611) does not move this reading — archiving a co-modified "
        "active change moves `active_co_modified` alone, never the "
        "corpus-wide `co_modified` — nor do #614, #602 or #604, none of which "
        "touch `openspec/changes/**/specs/**`, so the rise to 109 is this "
        "ratification's alone. It read 108 since add-project-repo-schema was authored 2026-09-02: it "
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
    assert sweep.active_co_modified == 20, (
        "20 ON THE MERGED TREE 2026-09-03 — NEITHER BRANCH'S NUMBER, AND THE "
        "SECOND TIME IN ONE DAY THIS PIN IS A NET OF OPPOSED MOVES RATHER "
        "THAN A STEP. FOUR moves off the same 20-baseline land in this merge "
        "and cancel two-for-two. On `main`: create-medxchart-overlay-boundary's "
        "RATIFICATION (#608) raised it 20 -> 21, making an ALREADY-ACTIVE "
        "change a co-modifier with `active_sole` falling 13 -> 12 in the same "
        "move; then add-project-repo-schema's ARCHIVE, on its own `tasks.md` "
        "9.3 cut of `contract-v3.1`, lowered it 21 -> 20. On THIS branch: "
        "amend-owner-layer-severity's AUTHORING raised it 20 -> 21 and its "
        "ARCHIVE, in the same commit (`code_surface: none`, so the archive "
        "gate is LANDING), lowered it 21 -> 20. Every one of the four is an "
        "ACTIVE co-modifier entering or leaving the active corpus, and none "
        "touches the corpus-wide `co_modified`, which an archive never "
        "un-shares. #609 moves it not at all (no `## MODIFIED Requirements` "
        "block; still a sole modifier). "
        "RE-DERIVE ON THE MERGED TREE, never by taking one side. It read 20 "
        "since declare-spent-bundle-state was ARCHIVED 2026-09-03: "
        "archiving a co-modified ACTIVE change lowers this count while "
        "leaving the corpus-wide `co_modified` untouched, the same shape "
        "#563's and #571's archives moved. It read 21 "
        "since add-project-repo-schema was authored 2026-09-02 as one "
        "more ACTIVE co-modifier entering the active corpus — by ONE and not "
        "two, because the earlier writers of the requirement key it shares "
        "are both ARCHIVED and were already co-modified, so no ACTIVE change "
        "flipped and `active_sole` held at 12 as it then stood — PR #593 "
        "raised it to 13 on 2026-09-03, which the MOVEMENT LOG records and "
        "which this pin does not read. It read 20 "
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
    assert sweep.change_ids - 1 == 158, (
        "158 since amend-owner-layer-severity was authored 2026-09-03, one "
        "more change id in the CORPUS — and it stays 158 through that same "
        "commit's ARCHIVE of it, because this pin counts the population and "
        "not the active corpus: the packet moved from active to archived "
        "(34+125 -> 33+126, and 32+127 after the merge with main) and a "
        "bucket move cannot change a total. Do NOT read this row as an "
        "active-count claim; `active_co_modified` and `active_sole` are the "
        "readings that saw the archive. Before that: "
        "the `- 1` subtracts THIS change and nothing else, so the reading is "
        "the corpus without it: 152 at authoring, 153 when "
        "add-clearing-dispatch-boundary landed 2026-09-01, 154 when "
        "declare-spent-bundle-state was authored 2026-09-02, 155 when "
        "add-cpc-clearing-boundary (PR #560) merged 2026-09-02, 156 when "
        "add-project-repo-schema was authored 2026-09-02, 157 when "
        "update-standards-body-current-publications was adopted 2026-09-03 "
        "-- and HELD at 157 through declare-spent-bundle-state's ARCHIVE "
        "2026-09-03 (#611, moves a change between buckets, not the total) "
        "and through create-medxchart-overlay-boundary's RATIFICATION "
        "2026-09-03, which moves four membership readings and no population "
        "count at all")
    # MOVED 2026-09-02: `sole_modifiers` fell 50 → 49 for the same reason
    # `active_sole` falls below — add-clearing-dispatch-boundary left the sole
    # set when add-cpc-clearing-boundary (PR #560) began sharing three
    # requirement keys with it. MOVED AGAIN 2026-09-03: it rose 49 -> 50 when
    # update-standards-body-current-publications was adopted (PR #593), an
    # ADDED-only packet over a new capability with novel requirement titles and
    # therefore a SOLE modifier — the opposite direction and the opposite cause,
    # which is why the two are recorded separately rather than netted. HELD at
    # 50 through declare-spent-bundle-state's ARCHIVE 2026-09-03 (#611): that
    # change was always a co-modifier and never a sole one, so removing it
    # from the active corpus touches `active_co_modified` alone.
    #
    # AND MOVED AGAIN 2026-09-03, on the merge of `main` at `2b0615da` (after
    # #611's archive of declare-spent-bundle-state, and after #614/#602/#604,
    # none of which touch `openspec/changes/**/specs/**`) into the
    # create-medxchart-overlay-boundary RATIFICATION branch: `sole_modifiers`
    # fell 50 -> 49 when that ratification added a `## MODIFIED Requirements`
    # block and took the packet OUT of the sole set — it was sole until then
    # on its NOVEL medxchart-overlay-boundary titles. UNLIKE
    # add-project-repo-schema's authoring, which held this pin, this move DOES
    # touch the sole set, because the change entering co-modified is the same
    # change leaving sole. The `- 1` still subtracts only
    # add-sequenced-after-substrate (unaffected, still sole), so the reading
    # falls with `sole_modifiers` to 48.
    #
    # AND MOVED AGAIN 2026-09-03: `sole_modifiers` fell 49 -> 48 when
    # amend-owner-layer-severity was AUTHORED and its `## MODIFIED
    # Requirements` block over workflow-gate-contract's 'Owner layer
    # constraint' flipped the ARCHIVED promote-workflow-gate-contract — sole
    # until then on that key — into the co-modified set. The newcomer is a
    # co-modifier itself and never joins `sole`, so this pin records the
    # FLIPPED change alone. The `- 1` still subtracts only
    # add-sequenced-after-substrate (unaffected, still sole), so the reading
    # falls with `sole_modifiers` to 47.
    assert sweep.sole_modifiers - 1 == 47
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
    #
    # AND MOVED BACK 2026-09-03: `active_sole` rose 12 -> 13 when
    # update-standards-body-current-publications was adopted as an ACTIVE change
    # (PR #593). An ADDED-only delta over a new capability with novel
    # requirement titles is an ACTIVE SOLE modifier, so it enters exactly the
    # population #560 had just removed one from. The two moves are unrelated and
    # cancel only numerically; the `- 1` still subtracts
    # add-sequenced-after-substrate alone. HELD at 13 through
    # declare-spent-bundle-state's ARCHIVE 2026-09-03 (#611): that change was
    # always a co-modifier and never a sole one, so an archive of it never
    # touches the sole set.
    #
    # AND MOVED AGAIN 2026-09-03, on the merge of `main` at `2b0615da` into
    # the create-medxchart-overlay-boundary RATIFICATION branch: `active_sole`
    # fell 13 -> 12 ALONGSIDE `sole_modifiers` above — that packet is ACTIVE
    # and its ratification moved it out of the sole set, so the two pins move
    # together, as they always do when the change that flips is itself
    # ACTIVE. The `- 1` still subtracts add-sequenced-after-substrate alone,
    # so the reading falls to 11.
    #
    # HELD 2026-09-03 through amend-owner-layer-severity's authoring, and the
    # hold is asserted rather than assumed because the same commit moves the
    # other four readings: that packet is a CO-modifier, so it never enters
    # `sole`, and the one change it flipped OUT of `sole`
    # (promote-workflow-gate-contract) is ARCHIVED, so no ACTIVE sole modifier
    # moved in either direction. This is the same reading the
    # add-project-repo-schema entry relied on and the OPPOSITE of #560's, where
    # the flipped change was itself active.
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
