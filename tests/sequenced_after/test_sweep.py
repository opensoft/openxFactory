"""Feature `sequenced-after-integrity` (add-sequenced-after-substrate tasks
5.4-5.5): the CORPUS SWEEP as a shipped, RE-RUNNABLE report.

A one-off measurement recorded in prose ages into a stale sentence. The sweep is
what makes the "measured, not assumed" obligation of the "Chain-walk policy
belongs to the consumer, and its bound SHALL be measured" requirement DISCHARGE
OVER TIME: it reports the population, the co-modified / sole-modifier split at
requirement granularity, adoption of the field, and THE DEEPEST DECLARED CHAIN it
resolves.

THE LIVE READING IS PINNED PER CHANGE, not as a handful of totals. The pin is
`corpus-ledger.yaml` beside this file — one row per change id, sorted, each
carrying what the sweep reads about that change — and every total the sweep
reports is DERIVED from those rows and cross-checked, field by field, against
the measurement itself. A drift in either the corpus or the counting method
still surfaces as a test failure rather than as a number nobody re-derives; what
no longer happens is two pull requests colliding on one shared total for
bookkeeping neither of them disagrees about (`add-per-change-sweep-ledger`,
issue #618). The AUTHORING measurement stays where it was recorded — in
`add-sequenced-after-substrate`'s `proposal.md`, `design.md` and the README —
as the dated historical snapshot it always was.
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
            archived: str | None = None, requirements: dict | None = None,
            created: str | None = None) -> Path:
    base = root / "openspec" / "changes"
    directory = (base / "archive" / f"{archived}-{change_id}"
                 if archived else base / change_id)
    directory.mkdir(parents=True, exist_ok=True)
    front = "code_surface: openxFactory"
    if declaration is not None:
        front += f"\nsequenced_after: {declaration}"
    (directory / "proposal.md").write_text(
        f"---\n{front}\n---\n\n# {change_id}\n", encoding="utf-8")
    if created is not None:
        (directory / ".openspec.yaml").write_text(
            f"schema: spec-driven\ncreated: {created}\n", encoding="utf-8")
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


# --- the LIVE corpus reading: THE LEDGER (add-per-change-sweep-ledger) ------


def _ledger(root, rows, schema_version=sa.LEDGER_SCHEMA_VERSION,
            kind=sa.LEDGER_KIND):
    """Write a synthetic ledger under `root`, one `id: {...}` line per row."""
    path = sa.ledger_path(root)
    path.parent.mkdir(parents=True, exist_ok=True)
    body = "".join(f"  {line}\n" for line in rows)
    path.write_text(
        f"schema_version: {schema_version}\nkind: {kind}\n"
        f"seeded_from: ~\n\nrows:\n{body}", encoding="utf-8")
    return path


def _row(change_id, state="active", klass=sa.CLASS_SOLE, declares="absent",
         depth=None, prose=False, moved_by="#1", moved_on="2026-09-03"):
    parts = [f"state: {state}", f"class: {klass}", f"declares: {declares}"]
    if depth is not None:
        parts.append(f"depth: {depth}")
    parts.append("prose: " + ("true" if prose else "false"))
    parts.append(f'moved_by: "{moved_by}"')
    parts.append(f'moved_on: "{moved_on}"')
    return change_id + ": {" + ", ".join(parts) + "}"


def test_the_DERIVED_totals_equal_the_MEASURED_sweep():
    # THE CROSS-CHECK, and the reason `corpus_sweep` was NOT refactored into the
    # classifier: if the fold were the measurement's own implementation this
    # equality would hold by construction and prove nothing, and a classifier
    # bug would silently populate a ledger that agreed with itself.
    readings = sa.classify_corpus(ROOT)
    derived = sa.sweep_from_readings(readings)
    measured = sa.corpus_sweep(ROOT)
    assert sa.sweep_mismatches(derived, measured) == []
    assert derived == measured


def test_the_LIVE_corpus_and_the_LEDGER_agree_row_by_row():
    """The LIVE PIN: the LEDGER and the corpus, row by row.

    The pin is no longer a handful of corpus-wide TOTALS asserted as literals
    here. It is `corpus-ledger.yaml` beside this file — ONE ROW PER CHANGE ID
    over the active and archived corpora both, sorted, each row carrying what
    the sweep reads about that change — and every total the sweep reports is
    DERIVED from those rows. A pull request now moves ITS OWN ROW (and a
    partner's row when its own `## MODIFIED Requirements` block flips that
    partner from sole to co-modifier), so two changes in flight edit two
    non-adjacent lines and merge without a conflict — UNLESS their ids sort
    with no row between them, where they share one insertion point and collide
    like any other adjacent insertion; that residue is the landing window's
    (issue #618 item 1), not something the row shape removes. Ratified by Brett
    Heap 2026-09-04 (*"ratify 623"*), on the convener's ruling of 2026-09-03
    (issue #618): *"do 1 and 3, keep the log in one place"*.

    Move your row with

        python3 scripts/validate-sequenced-after.py . --seed-ledger \
            --moved-by '#<PR>'

    which rewrites the ledger from the live corpus, stamps `moved_by`/`moved_on`
    on the rows that ACTUALLY moved, and leaves every other row's provenance
    alone. The diff is then the list of rows your change moved.
    `--ledger-diff` prints the same findings without writing anything.

    MOVEMENT LOG — THE RULE, RESTATED 2026-09-03. The log stays ONE
    hand-written ledger and it stays HERE — the convener's constraint, not a
    design choice. What changed is when an entry is OWED:

    - AN ENTRY IS OWED when a move is NOT explained by the row diff itself: a
      change to the COUNTING METHOD (what `state`, `class`, `depth` or `prose`
      mean); a PARTNER'S row moving because of someone else's delta, where the
      reason is not legible from the two rows alone; a reading that is not
      per-change moving; or a RE-SEEDING of, or repair to, the ledger.
    - NO ENTRY IS OWED for a move the row diff already states — a row added, a
      row's `state` flipping on archive, a row's `class` flipping on
      ratification. Most changes now append NOTHING.
    - THE NARRATIVE IS NEVER GENERATED FROM THE DIFF. A narrative that restates
      what the diff already says is noise that hides the entries carrying
      judgement. That is why the rule is about what the diff does NOT say.

    - **SEEDED 2026-09-03** from the live corpus, by
      `validate-sequenced-after.py --seed-ledger`, in PR #623
      (`add-per-change-sweep-ledger`). 159 rows: every change id in the active
      and archived corpora both, plus this packet's own directory — which is
      itself a corpus member, an ACTIVE SOLE modifier on its ALL-ADDED delta
      over a novel `release-realization` title, and the only change besides
      `add-sequenced-after-substrate` that declares `sequenced_after:`, taking
      the DEEPEST DECLARED CHAIN from 1 hop to 2 (this change ->
      `add-sequenced-after-substrate` -> `add-structured-scope-substrate`).
      THE SEEDING IS THE LAST ENTRY OWED FOR A MOVE THE DIFF ALSO STATES: the
      whole file is new, so the diff states everything, and the entry exists
      because a seeding is one of the four cases the rule above keeps.
      `seeded_from` in the ledger records `995c0ad5713dc2a22d35a00b083e3445e711b30c`
      as THE COMMIT THE FILE WAS FIRST SEEDED FROM — not the branch's base,
      which has moved twice since (`19d00872`, then `9a773a31`), and NOT a sha
      any record should cite: the ledger is deliberately no longer consistent
      with the corpus at it, and diffing it there reports eleven findings.
      RE-MEASURED AT THE HEAD THIS ENTRY LANDS ON, and EVERY READING CARRIES
      THE SHA IT WAS TAKEN AT, because a reading without one is the staleness
      this packet exists to stop:

        * `origin/main` at `9a773a31` (dated, superseded): `32 active +
          126 archived` = 158 change ids, `109` co-modified, `49` sole
          modifiers, `20 / 12` active co-modified/sole, 1 declaration, 3 prose
          headers (3 archived), deepest chain 1 hop.
        * `origin/main` at `c271caa2` (#615 archived
          `update-standards-body-current-publications`; superseded): `31 active
          + 127 archived` = 158, `109`, `49`, `20 / 11`, 1 declaration, 3 prose
          headers (3 archived), deepest chain 1 hop.
        * `origin/main` at `6a39d2ab` (#617 ratified and archived
          `amend-owner-layer-severity`; superseded): `31 active + 128 archived`
          = 159, `111`, `48`, `20 / 11`, 1 declaration, 3 prose headers (3
          archived), deepest chain 1 hop.
        * `origin/main` at `95c2cf6a` (#622 authored
          `add-consumer-identity-namespace`): `32 active + 128 archived` = 160,
          `112`, `48`, `21 / 11`, 1 declaration, 3 prose headers (3 archived),
          deepest chain 1 hop.
        * THIS BRANCH, merged with `95c2cf6a`: `33 active + 128 archived` =
          161, `112`, `49`, `21 / 12`, 2 declarations, 3 prose headers (3
          archived), deepest chain 2 hops.

      THE DIFFERENCE IS THIS PACKET AND NOTHING ELSE — one more ACTIVE SOLE
      modifier and one more declaration — and every one of those numbers is
      DERIVED from the rows and cross-checked against the measurement rather
      than asserted below.
      TWO EARLIER READINGS IN THIS ENTRY WENT STALE AND BOTH ARE NAMED RATHER
      THAN OVERWRITTEN SILENTLY. The first said `34 active + 125 archived` and
      `21 / 13`, taken before the merge of `main` at `19d00872` (#616 archived
      `add-project-repo-schema`); the second said `33 active + 126 archived`
      and `20 / 13`, taken at `9a773a31` and overtaken by `c271caa2`. Neither
      was wrong when written and both were wrong when read, which is the whole
      argument for pinning per row: the ROWS never needed re-measuring across
      either merge — exactly one row moved each time, and the diff said which.

    - **A PARTNER FLIP, 2026-09-03 — THE FIRST ENTRY THE NEW RULE ACTUALLY
      OWES, and it is owed for the reason the rule names.** Merging `main` at
      `6a39d2ab` (#617, which RATIFIED and ARCHIVED `amend-owner-layer-severity`)
      moved TWO rows:

        * `amend-owner-layer-severity` — a NEW row, `archived` and
          `co-modifier`. It carries TWO `## MODIFIED Requirements` blocks, so it
          enters the corpus already co-modified.
        * `promote-workflow-gate-contract` — `class: sole` -> `co-modifier`,
          and NOTHING ABOUT THIS CHANGE ITSELF MOVED. It was archived on
          2026-07-09 and has not been touched since.

      THE ROW DIFF DOES NOT EXPLAIN THE SECOND ONE, WHICH IS WHY THIS ENTRY
      EXISTS. Read the two rows alone and you can see that a co-modifier
      appeared and that an unrelated archived change flipped, but not WHICH
      requirement key they share, nor that this newcomer is what flipped it
      rather than any other change landing in the same window. That is exactly
      the case the rule reserves: "a PARTNER'S row moving because of someone
      else's delta, where the reason is not legible from the two rows alone".

      THE SHARED KEY, MEASURED RATHER THAN INFERRED. `amend-owner-layer-severity`
      modifies `workflow-gate-contract`'s "Owner layer constraint" and
      `release-surface-integrity`'s "The declared bundle describes the release
      surface". Grepping the corpus for the other writers of each:
      the first key is also written by `promote-workflow-gate-contract`
      (archived 2026-07-09) and by NOTHING else — so that change was SOLE and
      flips; the second is also written by `add-release-inventory-drift-check`
      (archived 2026-08-25), which was ALREADY co-modified — so nothing flips
      there.

      WHICH IS WHY `co_modified` ROSE BY TWO AND NOT BY THREE. Two MODIFIED
      blocks, two earlier writers, but only ONE of those writers was sole: the
      newcomer entering the set (+1) and `promote-workflow-gate-contract`
      leaving `sole` for it (+1), 109 -> 111. `sole_modifiers` falls by exactly
      one with it, 50 -> 49 — the rise-by-two shape is ALWAYS accompanied by the
      sole set falling, and that pairing is the check on the reading rather than
      a second number to remember. `change_ids` rises 159 -> 160 for the new id;
      `active` holds at 32 and `active_co_modified` at 20, both changes being
      ARCHIVED; `declaring`/`root_claims` hold at 2/0 and the prose headers at 3
      (3 archived).

      NO ENTRY WAS OWED FOR EITHER EARLIER MERGE, and the contrast is the point.
      `main` at `19d00872` and at `c271caa2` each moved exactly ONE row's
      `state` between the two corpora, which the diff states in full — so
      neither got an entry, and neither needed one.

    HISTORY, RETAINED VERBATIM. Every entry below is the record of a move that
    really happened under the rule that stood until 2026-09-03 — five scalar
    totals, moved in the same commit as the corpus, narrated here. They are
    kept because they are the evidence for this change: several exist only to
    reconcile two branches' readings of one corpus, and one had to REPLACE an
    earlier entry whose arithmetic went stale between authoring and merge.
    EVERYTHING BELOW IS PAST TENSE, INCLUDING ITS PROSE. The retained preamble
    states the rule THAT STOOD UNTIL 2026-09-03 in the present tense — where
    the live pin lived ("THE LIVE PIN IS THIS TEST, and only this test"), what
    moved with the corpus, and what an author had to re-derive. It is left
    unedited because retaining history verbatim is this packet's own rule, and
    it is read as a record of the old regime rather than as instruction: the
    live pin is now the LEDGER, and the numbers below are asserted nowhere.

    ----------------------------------------------------------------------

    The authoring measurement, re-derived — and MOVED where the corpus moved.

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
    - `active_sole - 1` reads 11. The entry immediately above and the one
      before it both held it at 12 (`active_sole` 13, unmoved by
      `declare-spent-bundle-state`'s archive, which is a co-modified change
      and never touches the sole set); this entry is what drops it, on
      2026-09-03, by archiving `update-standards-body-current-publications` —
      the SAME packet whose ADOPTION raised it to 13 several entries above,
      so this is that packet's other half, written beside the adoption entry
      rather than over it. The archive was earned and not merely taken: the
      packet was ratified 2026-09-03 (Brett Heap, in-session) and realized by
      PR #593 (squash `3c237cd0`) with `pytest-suite` run 33717394896 green
      on `main`, which is what `docs/release-realization-flow.md` § The
      Archive Gate requires of a code-surface change.
      THIS BRANCH TOOK A CATCH-UP MERGE FIRST: `declare-spent-bundle-state`'s
      own archive (PR #611, squash landed on `main` as `7af2725c`) merged
      ahead of this one, so the tree this act works from already carries that
      archive's `active_co_modified` 21 → 20 move. EXACTLY ONE PIN MOVES here
      and it is DISJOINT from that one, for the shape the adoption entry
      already recorded: the packet's delta is `## ADDED Requirements` ONLY
      over the NEW capability `standards-body-registry`, whose four
      requirement titles exist nowhere else in the corpus, so it is a SOLE
      modifier and never a co-modifier. Archiving it therefore removes an
      ACTIVE SOLE modifier — `active_sole` 13 → 12 — and touches nothing
      else: `co_modified` holds at 108, `active_co_modified` holds at 20
      (already moved by the sibling archive, not by this one),
      `sole_modifiers` holds at 50 and `change_ids` at 158 (both count BOTH
      corpora, and an archive moves a change between them rather than out of
      them). THE OPPOSITE HALF OF #571's 2026-09-02 move and the SAME SHAPE
      as the sibling entry immediately above: one archive moves
      `active_co_modified` alone, the other moves `active_sole` alone, and a
      packet moving both would still be a defect in the sweep rather than a
      corpus event.
      MEASURED ON BOTH SIDES rather than inferred from the failure, via
      `python3 scripts/validate-sequenced-after.py . --sweep`: `origin/main`
      at `7af2725c` (`declare-spent-bundle-state` already archived, this
      packet still active) reads `33 active + 125 archived` = 158 change
      ids, `108` co-modified, `50` sole modifiers, `20 / 13` active
      co-modified/sole; this branch after archiving
      `update-standards-body-current-publications` reads
      `32 active + 126 archived` = 158, `108`, `50`, `20 / 12`. The `- 1`
      still subtracts `add-sequenced-after-substrate` alone — an ACTIVE
      change, still sole, and untouched by this act — so the reading falls
      with `active_sole` to 11, which is also the authoring measurement this
      test reproduces. `declaring` holds at 1 and `root_claims` at 0: the
      archived packet declares no `sequenced_after:` field, and prose
      headers hold at 3 (3 archived), this packet carrying no prose
      `Sequenced-after:` header to move into the archived count. The pin
      moves in the SAME COMMIT as the corpus, which is this test's own
      protocol, and the archive PR discloses that it touches this file for
      that reason and for no other: corpus BOOKKEEPING, not realization.
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
    - `active_sole - 1` READS 10 ON THIS MERGE, and the two entries directly
      above are BOTH kept because both are right about their own act and
      neither is right about the total. RE-MEASURED 2026-09-03 by lane
      `openxfactory-f2` on the merge of `main` at `ea117d4e` into this archive
      branch — a catch-up merge taken to advance
      `contracts/review-lane-pin.yaml` onto codexFactory's regenerated
      54-spec floor (codexFactory PR #184, merge `8cb17373`), without which
      this branch's own promoted spec is off the floor and the REQUIRED
      `pytest-suite` is red.
      THE TWO MOVES ABOVE NEITHER CANCEL NOR COINCIDE — THEY COMPOUND. Each
      lowers `active_sole` 13 -> 12, and each removes a DIFFERENT change from
      the same population: `main`'s is `create-medxchart-overlay-boundary`'s
      RATIFICATION leaving the SOLE set (it gained a `## MODIFIED
      Requirements` block, so `sole_modifiers` fell with it), while this
      branch's is `update-standards-body-current-publications`' ARCHIVE
      leaving the ACTIVE corpus (it was always sole, so `sole_modifiers`
      holds). Two different subjects, one population, so on the merge of the
      two the reading falls 13 -> 11 and the `- 1` — still subtracting
      `add-sequenced-after-substrate` alone, an ACTIVE change, still sole, and
      untouched by either act — falls to 10. A cancelling pair would have held
      the pin; a coinciding pair would have moved it once. This is neither,
      which is exactly why the arithmetic had to be re-measured rather than
      carried over from either side.
      MEASURED ON BOTH TREES rather than adjusted by arithmetic, via
      `python3 scripts/validate-sequenced-after.py . --sweep`: `origin/main` at
      `ea117d4e` reads `33 active + 125 archived` = 158 change ids, `109`
      co-modified, `49` sole modifiers, `21 / 12` active co-modified/sole; this
      merge reads `32 active + 126 archived` = 158, `109`, `49`, `21 / 11`.
      AND MEASURED BY EXCLUSION, which is the step that rules out a third
      change having moved in the window this catch-up crosses: undoing ONLY
      the archive on the merged tree — moving the packet back out of
      `openspec/changes/archive/` — reproduces `main`'s reading EXACTLY
      (`33 active + 125 archived` = 158, `109`, `49`, `21 / 12`), so that one
      directory move is the whole of the difference between the two trees and
      no other change's contribution is hiding inside these counts.
      EXACTLY ONE PIN MOVES: `active_sole` 12 -> 11. `co_modified` holds at
      109 and `active_co_modified` at 21 (this packet was never in either
      population, and `main`'s ratification had already set both);
      `sole_modifiers` holds at 49 and `change_ids` at 158, both counting BOTH
      corpora, an archive moving a change between them rather than out of
      them; `archived` rises 125 -> 126; prose headers hold at 3 (3 archived);
      `declaring`/`root_claims` hold at 1/0, the archived packet declaring no
      `sequenced_after:` field and carrying no prose `Sequenced-after:`
      header. The pin moves in the SAME COMMIT as the corpus — here the merge
      commit that resolves this conflict — which is this test's own protocol.
    - MERGE-RESOLVED AGAIN 2026-09-03 by lane `openxfactory-f2`, on the merge
      of `main` at `19d00872` (the realization of `factory-origin-identity`,
      #610, and behind it #616 — the ARCHIVE of `add-project-repo-schema`)
      into this archive branch, and THIS IS THE ENTRY THAT STANDS. The three
      entries above are all kept because each is right about its own act
      against its own baseline, and NONE of them is right about the merged
      total: the pins below take `active_co_modified` from MAIN'S side and
      `active_sole - 1` from THIS BRANCH'S, which is neither side's pair and
      is why the arithmetic was re-measured rather than resolved by taking a
      side.
      WHY EACH SIDE'S OTHER NUMBER IS WRONG HERE, and it is the same cause
      read from two directions. This branch's entry above measured
      `active_co_modified` at 21 against `main` at `ea117d4e`, where
      `add-project-repo-schema` was still an ACTIVE co-modifier; #616 has
      since ARCHIVED it, so that population lost one member and reads 20 on
      the merged tree — main's own value, unmoved by anything this branch
      does, this packet never having been in the co-modified set at all.
      Main's entry above measured `active_sole` at 12, before this branch's
      ARCHIVE of `update-standards-body-current-publications` — an ACTIVE
      change that was always SOLE — moved it out of the active corpus, so
      the reading falls to 11 and the `- 1`, still subtracting
      `add-sequenced-after-substrate` alone (ACTIVE, still sole, untouched by
      either act), falls to 10.
      MEASURED ON BOTH TREES rather than netted by arithmetic, via
      `python3 scripts/validate-sequenced-after.py . --sweep`: `origin/main`
      at `19d00872` reads `32 active + 126 archived` = 158 change ids, `109`
      co-modified, `49` sole modifiers, `20 / 12` active co-modified/sole;
      the merged tree reads `31 active + 127 archived` = 158, `109`, `49`,
      `20 / 11`.
      AND MEASURED BY EXCLUSION, the step that rules out a third change
      having moved inside the window this catch-up merge crosses: the SAME
      sweep on the merged tree with ONLY this branch's archive undone — the
      packet moved back out of `openspec/changes/archive/` — reads
      `32 active + 126 archived` = 158, `109`, `49`, `20 / 12`, MAIN'S
      READING EXACTLY, so that one directory move is the whole of the
      difference between the two trees and no other change's contribution is
      hiding inside these counts.
      EXACTLY ONE PIN MOVES OFF MAIN: `active_sole - 1` 11 -> 10.
      `co_modified` holds at 109 and `active_co_modified` at 20 (an archive
      never un-shares a REQUIREMENT-KEY pairing, and this packet was never in
      either population); `sole_modifiers - 1` holds at 48 and
      `change_ids - 1` at 157, both counting BOTH corpora, an archive moving
      a change between them rather than out of them; `active` falls 32 -> 31
      and `archived` rises 126 -> 127; prose headers hold at 3 (3 archived);
      `declaring`/`root_claims` hold at 1/0, the archived packet declaring no
      `sequenced_after:` field and carrying no prose `Sequenced-after:`
      header. The pin moves in the SAME COMMIT as the corpus — here the merge
      commit that resolves this conflict — which is this test's own protocol.
      WHAT THIS MERGE ALSO DID, disclosed because it moves files this test
      does not read: the FIVE review-lane pin sites and the vendored floor
      snapshot were resolved to MAIN'S side (`605d48ac`), REVERTING this
      branch's own `0d17d1be` advance onto codexFactory `8cb17373`. #616 was
      the FIRST lander of a two-archive floor collision and its pin half is
      already on `main`; codexFactory PR #184's 54-spec floor does not cover
      the merged 55-spec tree, so it cannot be pinned here. Per the pinned
      core's `docs/repository-gate-floor-repair-runbook.md` the SECOND lander
      regenerates the floor once at its own post-merge head, and this
      branch's pin advance is re-authored against that new floor in a
      separate commit. Until it lands, `tests/review_lane_pin`'s coverage
      assertion is EXPECTED RED over
      `openspec/specs/standards-body-registry/spec.md`, which is the guard
      working.
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
    - A SECOND CATCH-UP MERGE, `main` at `c271caa2`, AND THIS TIME THIS BRANCH
      MOVES NOTHING THAT `main` HAD NOT ALREADY MOVED. `main` advanced three
      commits under this branch — #616's `contract-v3.1` cut and its archive of
      `add-project-repo-schema`, #624's `contract-v3.2` superseding cut, and
      #615's archive of `update-standards-body-current-publications` — and the
      last of those is the one that reaches this file: it takes `active_sole`
      13 -> 12 -> 11 together with the entry above it, so `active_sole - 1`
      reads 10. THIS BRANCH'S CONTRIBUTION IS UNCHANGED IN SHAPE A SECOND TIME
      and is entirely in the other four readings: `co_modified` 109 -> 111,
      `sole_modifiers` 49 -> 48, `change_ids` 158 -> 159, and
      `active_co_modified` NOT AT ALL — its authoring and its archive cancel
      inside the one commit, which is what a doc-only landing does to that pin.
      MEASURED ON BOTH TREES AND BY EXCLUSION, never adjusted by arithmetic,
      via `python3 scripts/validate-sequenced-after.py . --sweep`:
      `origin/main` at `c271caa2` reads `31 active + 127 archived` = 158 change
      ids, `109` co-modified, `49` sole modifiers, `20 / 11` active
      co-modified/sole; the merged tree reads `31 active + 128 archived` = 159,
      `111`, `48`, `20 / 11`; and the same sweep on the merged tree with only
      `openspec/changes/archive/2026-09-03-amend-owner-layer-severity/` moved
      aside reads `158`, `109`, `49`, `20 / 11` — `main`'s own reading EXACTLY,
      a second time — so this one archived packet remains the whole of the
      difference and none of `main`'s three new commits interacts with it.
      `archived` rises 127 -> 128; prose headers hold at 3 (3 archived);
      `declaring`/`root_claims` hold at 1/0.
    - **TEN ROWS MOVED FOR ONE CHANGE, AND NINE OF THEM ARE SOMEBODY ELSE'S** —
      which is exactly the case the rule above keeps an entry for. On 2026-09-04
      `split-opendox-two-layer-product` was authored (PR #666): one more ACTIVE
      change, carrying a `## REMOVED Requirements` block over **ALL 102**
      promoted `ideation-dashboard` requirements — the corpus exit of the
      largest promoted specification here. Its own row enters as an ACTIVE
      CO-MODIFIER, and **NINE ARCHIVED ROWS FLIP `sole` -> `co-modifier` in the
      same seeding**: `add-dashboard-account-menu`, `add-lens-gate-verbs`,
      `add-model-capability-vocabulary`, `add-model-provider-broker`,
      `add-register-edit-lane`, `add-repository-lens`,
      `add-shared-identity-seeds`, `add-staged-topic-outline-template` and
      `add-wheel-action-verbs`. THE REASON IS NOT LEGIBLE FROM THE TWO ROWS
      ALONE, which is why this entry exists: each of those nine was the SOLE
      writer of the `ideation-dashboard` requirements it added, and a block that
      names all 102 titles at once shares a requirement key with EVERY ONE OF
      THEM at a stroke. A single delta flipping nine archived partners has not
      happened before in this corpus and it is a property of the SIZE of the
      block, not of anything the nine did.
      THE ARITHMETIC IS THEREFORE +10 AND NOT +1. `co_modified` rises 113 -> 123
      — the new change entering the set (+1) plus the nine partners leaving
      `sole` for it (+9) — and `sole_modifiers` falls 52 -> 43 by the same nine.
      Membership is BOOLEAN, so sharing 102 titles with (among others) four
      ACTIVE siblings flips this change ONCE, and the four active siblings
      (`add-composed-view-authoring`, `add-doxchat-model-intake`,
      `add-nightly-dashboard-refresh`, `retire-doxbench-chat-turn-v1`) were
      ALREADY co-modifiers and do not move at all. `active_co_modified` rises by
      exactly ONE, 19 -> 20 — the new change alone, all nine flipped partners
      being ARCHIVED — and `active_sole` holds at 12. `change_ids` rises
      165 -> 166 and `active` 31 -> 32; `archived` holds at 134; prose headers
      hold at 3 (3 archived); `declaring`/`root_claims` hold at 3/0.
      MEASURED ON BOTH TREES, never adjusted by arithmetic, via
      `python3 scripts/validate-sequenced-after.py . --sweep`: `origin/main` at
      `807a4f47` reads `31 active + 134 archived` = 165 change ids, `113`
      co-modified, `52` sole modifiers, `19 / 12` active co-modified/sole; this
      branch reads `32 active + 134 archived` = 166, `123`, `43`, `20 / 12`.
      The packet is PROPOSAL ONLY (`Status: draft`) and its REMOVED block
      promotes nothing until it archives — so this is a movement of the SWEEP's
      reading of the active corpus, and no `ideation-dashboard` requirement has
      left canon.
    - **A PARTNER FLIP, 2026-09-10 — the second entry the new rule owes, found
      by Copilot review rather than by the authoring pass, and added on
      re-verification.** Authoring `state-header-window-budget` (PR #921, an
      OpenSpec amendment adding one paragraph and one scenario to the
      `release-realization` requirement "Equivalent declaration sites for the
      ordered-delta parent declaration") moves TWO rows:

        * `state-header-window-budget` — a NEW row, `active` and
          `co-modifier`. Its own `## MODIFIED Requirements` block writes the
          same requirement key `accept-sequenced-after-header-line`'s own
          `## ADDED Requirements` block wrote, so it enters the corpus
          already co-modified rather than sole.
        * `accept-sequenced-after-header-line` — `class: sole` ->
          `co-modifier`, and NOTHING ABOUT THAT ARCHIVED CHANGE ITSELF MOVED.
          It archived 2026-09-10 (PR #906) and has not been touched since.

      THE ROW DIFF DOES NOT EXPLAIN THE SECOND ONE, WHICH IS WHY THIS ENTRY
      EXISTS. Read the two rows alone and a co-modifier appears and an
      archived change flips, but not WHICH requirement key they share, nor
      that this newcomer is what flipped it rather than any other change
      landing in the same window — exactly the case the rule reserves: "a
      PARTNER'S row moving because of someone else's delta, where the reason
      is not legible from the two rows alone".

      THE SHARED KEY, MEASURED RATHER THAN INFERRED. Both changes write
      `release-realization` / "Equivalent declaration sites for the
      ordered-delta parent declaration" — `accept-sequenced-after-header-line`
      ADDED it (archived, PR #906) and `state-header-window-budget` MODIFIES
      it (a pure-addition amendment, `code_surface: none`, routed from a
      Copilot review comment on #906 itself). No other active or archived
      change writes this exact requirement key (`proposal.md` § Sibling
      search, corrected twice over this packet's own review rounds), so this
      is a two-party flip and not a wider one.

      WHICH IS WHY `co_modified` ROSE BY TWO AND NOT BY ONE. One MODIFIED
      block, one earlier writer, and that writer was sole: the newcomer
      entering the set (+1) and `accept-sequenced-after-header-line` leaving
      `sole` for it (+1), 143 -> 145. `sole_modifiers` falls by exactly one
      with it, 54 -> 53. `change_ids` rises 197 -> 198 for the new id alone;
      `active` rises 40 -> 41 and `active_co_modified` rises 25 -> 26, both by
      the new row alone, the partner being ARCHIVED; `active_sole` holds at
      15. `declaring` rises 22 -> 23, this change's own
      `sequenced_after: [accept-sequenced-after-header-line]`; the explicit
      `[]` root claims hold at 5, the prose headers at 3 (3 archived), and the
      deepest declared chain at 4 hops — this change's own chain is one hop
      to an archived root, shorter than the standing champion.
      MEASURED ON BOTH TREES, never adjusted by arithmetic, via
      `python3 scripts/validate-sequenced-after.py . --sweep`: `origin/main`
      at `0e76e789` reads `40 active + 157 archived` = 197 change ids, `143`
      co-modified, `54` sole modifiers, `25 / 15` active co-modified/sole,
      `22` declaring; this branch (merged with `0e76e789`) reads `41 active +
      157 archived` = 198, `145`, `53`, `26 / 15`, `23`.
    """
    readings = sa.classify_corpus(ROOT)
    ledger = sa.load_ledger(sa.ledger_path(ROOT))
    assert sa.ledger_problems(readings, ledger) == []


def test_every_corpus_change_has_EXACTLY_ONE_row_and_every_row_a_change():
    readings = sa.classify_corpus(ROOT)
    ledger = sa.load_ledger(sa.ledger_path(ROOT))
    assert set(ledger.rows) == set(readings)
    assert len(ledger.order) == len(set(ledger.order)) == len(readings)


def test_the_live_ledger_is_SORTED_by_change_id():
    # Sorted order is what keeps two changes' insertions apart in the diff. An
    # append-ordered file would put every insertion at one growing tail, which
    # is the collision this change removes.
    ledger = sa.load_ledger(sa.ledger_path(ROOT))
    assert list(ledger.order) == sorted(ledger.order)


def test_the_totals_DERIVED_FROM_THE_LEDGER_equal_the_MEASURED_sweep():
    # THE PIN, stated as the requirement states it: the totals a check asserts
    # are folded from THE ROWS, and they equal the independent measurement. This
    # is the assertion the five scalar literals used to make, with the rows in
    # place of the literals.
    ledger = sa.load_ledger(sa.ledger_path(ROOT))
    derived = sa.sweep_from_readings(sa.readings_from_ledger(ledger))
    measured = sa.corpus_sweep(ROOT)
    assert sa.sweep_mismatches(derived, measured) == []
    assert derived == measured
    assert derived.change_ids == len(ledger.rows)


def test_the_live_ledger_reports_the_SAME_totals_the_sweep_MEASURES():
    # The measurement is still measured and still RE-RUNNABLE — from the rows.
    ledger = sa.load_ledger(sa.ledger_path(ROOT))
    derived = sa.sweep_from_readings(sa.readings_from_ledger(ledger))
    result = subprocess.run(
        [sys.executable, str(VALIDATOR), str(ROOT), "--ledger-diff"],
        capture_output=True, text=True)
    assert result.returncode == 0, result.stdout + result.stderr
    assert "ledger consistent with the corpus" in result.stdout
    assert derived.render() in result.stdout


def test_the_live_sweep_records_a_NON_ZERO_deepest_chain():
    """WHAT THIS TEST PINS, and what it does NOT — stated because the two are
    easy to confuse and an earlier draft of this comment confused them.

    THIS TEST ASSERTS A FLOOR: the reading is `>= 1`, no longer
    "0 hops BY CONSTRUCTION". That is the doctrine at stake, and pinning the
    exact value HERE would re-serialize on every change that declares the
    field — the very cost this packet removes.

    THE EXACT DEPTH IS STILL PINNED, but by the DECLARING CHANGE'S OWN LEDGER
    ROW, checked in `test_the_LIVE_corpus_and_the_LEDGER_agree_row_by_row`:
    setting `depth: 9` on that row fails THAT test, naming the row, the key and
    both values. So the number is not unpinned, it is pinned per change like
    every other reading.

    THE SECOND ASSERTION IS A SELF-CONSISTENCY CHECK ON THE FOLD, NOT A LEDGER
    CHECK. It reads `classify_corpus` and never opens the ledger, so
    `deepest.depth == sweep.deepest_chain` holds by construction of
    `sweep_from_readings`. It is kept for what it does prove — that the fold
    names a row that DECLARES and reports THAT row's depth, rather than a
    non-declaring row or some other row's number — and it is labelled so no
    later reader mistakes it for the pin.
    """
    readings = sa.classify_corpus(ROOT)
    sweep = sa.sweep_from_readings(readings)
    assert sweep.deepest_chain >= 1
    assert sweep.deepest_chain_change is not None
    assert "ZERO EVIDENCE" not in sweep.render()
    deepest = readings[sweep.deepest_chain_change]
    assert deepest.declares is not None and deepest.depth == sweep.deepest_chain


def test_the_sweep_is_RE_RUNNABLE_from_the_validator_CLI():
    result = subprocess.run(
        [sys.executable, str(VALIDATOR), str(ROOT), "--sweep"],
        capture_output=True, text=True)
    assert result.returncode == 0, result.stdout + result.stderr
    assert "DEEPEST DECLARED CHAIN RESOLVED" in result.stdout
    assert "co-modified at requirement granularity" in result.stdout


# --- the ledger's own failure shapes ----------------------------------------


def test_a_MISSING_row_names_the_change_id(tmp_path):
    _change(tmp_path, "add-a")
    _change(tmp_path, "add-b")
    _ledger(tmp_path, [_row("add-a")])
    problems = sa.ledger_problems(sa.classify_corpus(tmp_path),
                                  sa.load_ledger(sa.ledger_path(tmp_path)))
    assert any(p.startswith("missing row: add-b") for p in problems)
    assert not any("add-a" in p for p in problems)


def test_an_EXTRA_row_names_the_change_id(tmp_path):
    _change(tmp_path, "add-a")
    _ledger(tmp_path, [_row("add-a"), _row("add-gone")])
    problems = sa.ledger_problems(sa.classify_corpus(tmp_path),
                                  sa.load_ledger(sa.ledger_path(tmp_path)))
    assert any(p.startswith("extra row: add-gone") for p in problems)


def test_a_STALE_state_names_the_id_the_key_and_BOTH_values(tmp_path):
    _change(tmp_path, "add-a", archived="2026-08-01")
    _ledger(tmp_path, [_row("add-a", state="active")])
    problems = sa.ledger_problems(sa.classify_corpus(tmp_path),
                                  sa.load_ledger(sa.ledger_path(tmp_path)))
    assert problems == ["stale row: add-a: state: ledger 'active', live "
                        "'archived'"]


def test_a_STALE_class_names_the_id_the_key_and_BOTH_values(tmp_path):
    _change(tmp_path, "add-a", requirements={"cap": ["Shared rule"]})
    _change(tmp_path, "add-b", requirements={"cap": ["Shared rule"]})
    _ledger(tmp_path, [_row("add-a", klass=sa.CLASS_CO_MODIFIER),
                       _row("add-b", klass=sa.CLASS_SOLE)])
    problems = sa.ledger_problems(sa.classify_corpus(tmp_path),
                                  sa.load_ledger(sa.ledger_path(tmp_path)))
    assert problems == ["stale row: add-b: class: ledger 'sole', live "
                        "'co-modifier'"]


def test_a_PARTNER_FLIP_names_BOTH_change_ids(tmp_path):
    # THE SHAPE THAT MOTIVATES THE ROW: `add-b` lands carrying a delta over a
    # requirement `add-a` already wrote, so BOTH become co-modifiers and BOTH
    # rows move. The failure must name the partner too, or an author moves one
    # row, re-runs, and discovers the other only on the next red.
    _change(tmp_path, "add-a", requirements={"cap": ["Shared rule"]})
    _change(tmp_path, "add-b", requirements={"cap": ["shared   RULE"]})
    _ledger(tmp_path, [_row("add-a"), _row("add-b")])
    problems = sa.ledger_problems(sa.classify_corpus(tmp_path),
                                  sa.load_ledger(sa.ledger_path(tmp_path)))
    assert len(problems) == 2
    assert any(p.startswith("stale row: add-a: class:") for p in problems)
    assert any(p.startswith("stale row: add-b: class:") for p in problems)


def test_a_STALE_declaration_and_a_STALE_depth_are_each_named(tmp_path):
    _change(tmp_path, "add-root", declaration="[]")
    _change(tmp_path, "add-child", declaration="[add-root]")
    _ledger(tmp_path, [_row("add-child", declares="absent"),
                       _row("add-root", declares="[]", depth=7)])
    problems = sa.ledger_problems(sa.classify_corpus(tmp_path),
                                  sa.load_ledger(sa.ledger_path(tmp_path)))
    assert any(p.startswith("stale row: add-child: declares: ledger 'absent'")
               for p in problems)
    assert any(p.startswith("stale row: add-root: depth: ledger 7, live 0")
               for p in problems)


def test_a_DEPTH_on_a_row_that_declares_NOTHING_is_a_finding(tmp_path):
    # `0` on a non-declaring row would read as a resolved root claim, which is
    # the exact ABSENT/`[]` conflation the substrate refuses.
    _change(tmp_path, "add-a")
    _ledger(tmp_path, [_row("add-a", declares="absent", depth=0)])
    problems = sa.ledger_problems(sa.classify_corpus(tmp_path),
                                  sa.load_ledger(sa.ledger_path(tmp_path)))
    assert any("depth" in p and "not applicable" in p for p in problems)


def test_an_UNSORTED_ledger_is_a_finding(tmp_path):
    _change(tmp_path, "add-a")
    _change(tmp_path, "add-b")
    _ledger(tmp_path, [_row("add-b"), _row("add-a")])
    problems = sa.ledger_problems(sa.classify_corpus(tmp_path),
                                  sa.load_ledger(sa.ledger_path(tmp_path)))
    assert any(p.startswith("unsorted ledger:") for p in problems)


def test_a_MALFORMED_provenance_is_a_finding(tmp_path):
    _change(tmp_path, "add-a")
    _ledger(tmp_path, ['add-a: {state: active, class: sole, declares: absent, '
                       'prose: false, moved_by: "later", moved_on: "soon"}'])
    problems = sa.ledger_problems(sa.classify_corpus(tmp_path),
                                  sa.load_ledger(sa.ledger_path(tmp_path)))
    assert any(p.startswith("malformed provenance: add-a: moved_by")
               for p in problems)
    assert any(p.startswith("malformed provenance: add-a: moved_on")
               for p in problems)


def test_a_DIGIT_SHAPED_date_that_is_not_a_DATE_is_a_finding(tmp_path):
    # `^\d{4}-\d{2}-\d{2}$` accepts 2026-13-45, and a provenance date nobody
    # can place is no provenance.
    _change(tmp_path, "add-a")
    _ledger(tmp_path, [_row("add-a", moved_on="2026-13-45")])
    problems = sa.ledger_problems(sa.classify_corpus(tmp_path),
                                  sa.load_ledger(sa.ledger_path(tmp_path)))
    assert any(p.startswith("malformed provenance: add-a: moved_on")
               for p in problems)


def test_an_UNKNOWN_row_key_is_a_finding(tmp_path):
    _change(tmp_path, "add-a")
    _ledger(tmp_path, ['add-a: {state: active, class: sole, declares: absent, '
                       'prose: false, guess: yes, moved_by: "#1", '
                       'moved_on: "2026-09-03"}'])
    problems = sa.ledger_problems(sa.classify_corpus(tmp_path),
                                  sa.load_ledger(sa.ledger_path(tmp_path)))
    assert any("unknown key 'guess'" in p for p in problems)


def test_a_NON_STRING_row_key_is_REFUSED_never_COERCED(tmp_path):
    # `str()` on the key would collapse two keys YAML holds APART: `123`
    # resolves to an int and `"123"` to a string, so the strict loader's
    # duplicate refusal — which compares keys as YAML typed them — never fires
    # and the SECOND row silently overwrites the first. That is the exact
    # last-duplicate-wins defect this loader exists to refuse, one level down,
    # on the file that IS the pin.
    _change(tmp_path, "add-a")
    header = ("schema_version: 1\nkind: sequenced_after_corpus_ledger\n"
              "seeded_from: ~\n\nrows:\n")
    body = ("{state: active, class: sole, declares: absent, prose: false, "
            'moved_by: "#1", moved_on: "2026-09-03"}')
    path = sa.ledger_path(tmp_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(f'{header}  123: {body}\n  "123": {body}\n',
                    encoding="utf-8")
    try:
        sa.load_ledger(path)
    except sa.SequencedAfterError as exc:
        assert "row key 123" in str(exc) and "not a string" in str(exc), str(exc)
    else:  # pragma: no cover - the refusal is the assertion
        raise AssertionError("an int row key must be refused, never coerced")

    # ...and it refuses ALONE, not only when a quoted twin is present: the
    # danger is the coercion, and a lone unquoted id is the same coercion
    # waiting for a twin.
    path.write_text(f"{header}  123: {body}\n", encoding="utf-8")
    try:
        sa.load_ledger(path)
    except sa.SequencedAfterError as exc:
        assert "not a string" in str(exc), str(exc)
    else:  # pragma: no cover
        raise AssertionError("a lone int row key must be refused too")

    # THE CLI REPORTS IT AS UNREADABLE (exit 2), NOT AS STALE (exit 1): the two
    # want different repairs — a stale ledger is fixed by moving a row, an
    # unreadable one by fixing the file.
    path.write_text(f'{header}  123: {body}\n  "123": {body}\n',
                    encoding="utf-8")
    result = subprocess.run(
        [sys.executable, str(VALIDATOR), str(tmp_path), "--ledger-diff"],
        capture_output=True, text=True)
    assert result.returncode == 2, (result.returncode, result.stdout)
    assert "CANNOT BE READ" in result.stdout, result.stdout


def test_a_PLAIN_STRING_row_key_still_loads(tmp_path):
    # The positive control the refusal above needs: nothing legitimate is lost,
    # quoted or unquoted, because a change id is a string by the grammar.
    _change(tmp_path, "add-a")
    header = ("schema_version: 1\nkind: sequenced_after_corpus_ledger\n"
              "seeded_from: ~\n\nrows:\n")
    body = ("{state: active, class: sole, declares: absent, prose: false, "
            'moved_by: "#1", moved_on: "2026-09-03"}')
    path = sa.ledger_path(tmp_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    for spelling in ("add-a", '"add-a"'):
        path.write_text(f"{header}  {spelling}: {body}\n", encoding="utf-8")
        ledger = sa.load_ledger(path)
        assert list(ledger.rows) == ["add-a"], spelling
        assert ledger.order == ("add-a",), spelling
        assert sa.ledger_problems(sa.classify_corpus(tmp_path), ledger) == []


def test_a_row_TOO_MALFORMED_TO_READ_is_REFUSED_and_never_defaulted(tmp_path):
    # A defaulted row is an INVENTED reading, and the ledger is what every later
    # author reads. Each unreadable field refuses under its own message.
    _change(tmp_path, "add-a")
    for row, expected in (
        (_row("add-a", state="somewhere"), "state is 'somewhere'"),
        (_row("add-a", klass="maybe"), "class is 'maybe'"),
        (_row("add-a", declares="nonsense"), "declares is 'nonsense'"),
        (_row("add-a", declares="[add-b]"), "depth is None"),
        ('add-a: {state: active, class: sole, declares: absent, '
         'prose: perhaps, moved_by: "#1", moved_on: "2026-09-03"}',
         "prose is 'perhaps'"),
    ):
        ledger = sa.load_ledger(_ledger(tmp_path, [row]))
        try:
            sa.readings_from_ledger(ledger)
        except sa.SequencedAfterError as exc:
            assert expected in str(exc), str(exc)
        else:  # pragma: no cover - the refusal is the assertion
            raise AssertionError(f"{row!r} must be refused")


def test_a_WRONG_schema_header_is_a_finding(tmp_path):
    _change(tmp_path, "add-a")
    _ledger(tmp_path, [_row("add-a")], schema_version=99, kind="something-else")
    problems = sa.ledger_problems(sa.classify_corpus(tmp_path),
                                  sa.load_ledger(sa.ledger_path(tmp_path)))
    assert any(p.startswith("malformed ledger: schema_version") for p in problems)
    assert any(p.startswith("malformed ledger: kind") for p in problems)


def test_a_DUPLICATE_row_id_is_REFUSED_by_the_loader(tmp_path):
    # `yaml.safe_load` applies last-duplicate-wins SILENTLY, so a ledger with
    # two rows for one change would show a reviewer the first and check the
    # second. Refused by construction, as the front-matter loader refuses it.
    _change(tmp_path, "add-a")
    _ledger(tmp_path, [_row("add-a"), _row("add-a", state="archived")])
    try:
        sa.load_ledger(sa.ledger_path(tmp_path))
    except sa.SequencedAfterError as exc:
        assert "duplicate" in str(exc).lower()
    else:  # pragma: no cover - the refusal is the assertion
        raise AssertionError("a duplicate change id must be refused")


def test_DERIVED_totals_that_disagree_with_the_MEASUREMENT_name_the_field():
    left = sa.Sweep(
        change_ids=2, active=1, archived=1, co_modified=0, sole_modifiers=2,
        active_co_modified=0, active_sole=1, declaring=0, root_claims=0,
        prose_headers=0, prose_headers_archived=0, deepest_chain=0,
        deepest_chain_change=None, declaring_ids=())
    right = sa.Sweep(**{**left.__dict__, "co_modified": 1, "deepest_chain": 3})
    problems = sa.sweep_mismatches(left, right)
    assert len(problems) == 2
    assert any("co_modified" in p and "0" in p and "1" in p for p in problems)
    assert any("deepest_chain" in p for p in problems)


def test_RE_SEEDING_stamps_ONLY_the_rows_that_MOVED(tmp_path):
    # The authoring tool: a re-seed after a merge must not restamp 158 rows it
    # did not move, or the diff stops being the list of rows the change moved.
    _change(tmp_path, "add-a")
    _change(tmp_path, "add-b")
    path = _ledger(tmp_path, [_row("add-a", moved_by="#1", moved_on="2026-01-01"),
                              _row("add-b", moved_by="#1", moved_on="2026-01-01")])
    _change(tmp_path, "add-b", archived="2026-08-01")
    import shutil
    shutil.rmtree(tmp_path / "openspec" / "changes" / "add-b")
    readings = sa.classify_corpus(tmp_path)
    rendered = sa.render_ledger(
        readings, moved_by="#2", moved_on="2026-09-03",
        previous=sa.load_ledger(path))
    path.write_text(rendered, encoding="utf-8")
    rows = sa.load_ledger(path).rows
    assert rows["add-a"]["moved_by"] == "#1", (
        "an unmoved row keeps the pull request that last moved it")
    assert rows["add-a"]["moved_on"] == "2026-01-01"
    assert rows["add-b"]["moved_by"] == "#2"
    assert rows["add-b"]["state"] == "archived"
    assert sa.ledger_problems(readings, sa.load_ledger(path)) == []


def test_the_SEEDER_refuses_a_provenance_it_cannot_read(tmp_path):
    _change(tmp_path, "add-a")
    readings = sa.classify_corpus(tmp_path)
    for by, on in (("620", "2026-09-03"), ("#620", "September")):
        try:
            sa.render_ledger(readings, moved_by=by, moved_on=on)
        except sa.SequencedAfterError:
            continue
        raise AssertionError(f"({by!r}, {on!r}) must be refused")


def test_the_LEDGER_DIFF_cli_names_the_stale_rows_and_EXITS_NON_ZERO(tmp_path):
    _change(tmp_path, "add-a")
    _change(tmp_path, "add-b")
    _ledger(tmp_path, [_row("add-a")])
    result = subprocess.run(
        [sys.executable, str(VALIDATOR), str(tmp_path), "--ledger-diff"],
        capture_output=True, text=True)
    assert result.returncode == 1, result.stdout + result.stderr
    assert "missing row: add-b" in result.stdout
    assert "--seed-ledger" in result.stdout


def test_the_SEED_LEDGER_cli_writes_a_ledger_the_diff_then_ACCEPTS(tmp_path):
    _change(tmp_path, "add-a", requirements={"cap": ["Shared rule"]})
    _change(tmp_path, "add-b", requirements={"cap": ["Shared rule"]})
    _change(tmp_path, "add-old", archived="2026-08-01")
    seed = subprocess.run(
        [sys.executable, str(VALIDATOR), str(tmp_path), "--seed-ledger",
         "--moved-by", "#623", "--moved-on", "2026-09-03"],
        capture_output=True, text=True)
    assert seed.returncode == 0, seed.stdout + seed.stderr
    diff = subprocess.run(
        [sys.executable, str(VALIDATOR), str(tmp_path), "--ledger-diff"],
        capture_output=True, text=True)
    assert diff.returncode == 0, diff.stdout + diff.stderr
    rows = sa.load_ledger(sa.ledger_path(tmp_path)).rows
    assert rows["add-a"]["class"] == "co-modifier"
    assert rows["add-old"]["state"] == "archived"
    # `add-old` is a NEW row for a change that was ALREADY archived, which is
    # not a flip: its move is its creation, so it records the run's date and
    # `--moved-on` is honoured (#790, narrowed on review).
    assert rows["add-old"]["moved_on"] == "2026-09-03"


def test_MOVED_ROWS_names_exactly_the_rows_a_re_seed_moves(tmp_path):
    # The one place that decides "did this row move?", so the provenance the
    # renderer stamps and the summary the CLI prints cannot disagree.
    _change(tmp_path, "add-a")
    _change(tmp_path, "add-b")
    path = _ledger(tmp_path, [_row("add-a"), _row("add-b")])
    previous = sa.load_ledger(path)
    readings = sa.classify_corpus(tmp_path)
    assert sa.moved_rows(readings, previous) == ()
    assert sa.moved_rows(readings, None) == ("add-a", "add-b"), (
        "with no previous ledger every row is new, so every row moved")
    _change(tmp_path, "add-c")
    assert sa.moved_rows(sa.classify_corpus(tmp_path), previous) == ("add-c",)
    # A row carrying a key the grammar does not know is MOVED, because a
    # re-seed drops it and dropping a key is a move.
    stale = sa.load_ledger(_ledger(tmp_path, [
        'add-a: {state: active, class: sole, declares: absent, prose: false, '
        'guess: 1, moved_by: "#1", moved_on: "2026-09-03"}',
        _row("add-b"), _row("add-c")]))
    assert sa.moved_rows(sa.classify_corpus(tmp_path), stale) == ("add-a",)


def test_the_SEED_summary_counts_ONLY_the_rows_it_MOVED(tmp_path):
    # A row that merely already carried this pull request is NOT one this run
    # moved, and reporting it as moved would misdescribe the diff.
    _change(tmp_path, "add-a")
    first = subprocess.run(
        [sys.executable, str(VALIDATOR), str(tmp_path), "--seed-ledger",
         "--moved-by", "#623", "--moved-on", "2026-09-03"],
        capture_output=True, text=True)
    assert first.returncode == 0, first.stdout + first.stderr
    assert "1 rows, 1 moved by #623" in first.stdout
    again = subprocess.run(
        [sys.executable, str(VALIDATOR), str(tmp_path), "--seed-ledger",
         "--moved-by", "#623", "--moved-on", "2026-09-03"],
        capture_output=True, text=True)
    assert again.returncode == 0, again.stdout + again.stderr
    assert "1 rows, 0 moved by #623" in again.stdout


def test_an_UNSAFE_declares_entry_is_QUOTED_and_reads_back(tmp_path):
    # A MALFORMED DECLARATION IS A REAL INPUT: the sweep reads a shape-refused
    # declaration AS a declaration (only a strict-LOADER refusal reads as
    # absence), so an entry can carry a comma or a bracket. Written raw,
    # `[a, b]` reads back as TWO entries and `[a] b: {c]` does not parse — and
    # the seeder is the documented REPAIR tool.
    directory = _change(tmp_path, "add-bad")
    (directory / "proposal.md").write_text(
        '---\ncode_surface: openxFactory\n'
        'sequenced_after: ["a, b", "c] d: {e"]\n---\n\n# add-bad\n',
        encoding="utf-8")
    result = subprocess.run(
        [sys.executable, str(VALIDATOR), str(tmp_path), "--seed-ledger",
         "--moved-by", "#623", "--moved-on", "2026-09-03"],
        capture_output=True, text=True)
    assert result.returncode == 0, result.stdout + result.stderr
    written = sa.ledger_path(tmp_path).read_text(encoding="utf-8")
    assert '["a, b", "c] d: {e"]' in written, written
    rows = sa.load_ledger(sa.ledger_path(tmp_path)).rows
    assert rows["add-bad"]["declares"] == ["a, b", "c] d: {e"], (
        "the entries must read back as themselves, not split on the comma")
    assert sa.ledger_problems(sa.classify_corpus(tmp_path),
                              sa.load_ledger(sa.ledger_path(tmp_path))) == []


def test_a_WELL_FORMED_entry_is_NOT_quoted_for_show(tmp_path):
    # Both shapes the reference grammar allows stay plain, so the ordinary file
    # keeps its stable one-line format.
    _change(tmp_path, "add-root", declaration="[]")
    _change(tmp_path, "add-child",
            declaration="[add-root, openxFactory:add-root]")
    text = sa.render_ledger(sa.classify_corpus(tmp_path), moved_by="#1",
                            moved_on="2026-09-03")
    assert "declares: [add-root, openxFactory:add-root]" in text, text


def test_a_SEEDED_FROM_carrying_YAML_metacharacters_still_reads_back(tmp_path):
    # `--seeded-from` is caller-supplied and, unlike `moved_by`/`moved_on`, is
    # NOT pattern-validated. Hand-quoted, a value carrying a quote or a
    # backslash produced a header the round-trip then refused — a refusal caused
    # by the renderer rather than by the input. One quoting strategy for every
    # scalar in the file, so there is one thing to keep right.
    _change(tmp_path, "add-a")
    result = subprocess.run(
        [sys.executable, str(VALIDATOR), str(tmp_path), "--seed-ledger",
         "--moved-by", "#1", "--moved-on", "2026-09-03",
         "--seeded-from", 'he said "hi" \\back'],
        capture_output=True, text=True)
    assert result.returncode == 0, result.stdout + result.stderr
    ledger = sa.load_ledger(sa.ledger_path(tmp_path))
    assert ledger.seeded_from == 'he said "hi" \\back'
    assert sa.ledger_problems(sa.classify_corpus(tmp_path), ledger) == []


def test_the_RENDERER_REFUSES_output_that_does_not_READ_BACK(tmp_path, monkeypatch):
    # The guard itself, driven by restoring the unquoted renderer: the seeder
    # must never report "wrote" for a file it cannot read.
    directory = _change(tmp_path, "add-bad")
    (directory / "proposal.md").write_text(
        '---\ncode_surface: openxFactory\n'
        'sequenced_after: ["a] b: {c"]\n---\n\n# add-bad\n',
        encoding="utf-8")
    monkeypatch.setattr(sa, "_render_entry", lambda entry: entry)
    try:
        sa.render_ledger(sa.classify_corpus(tmp_path), moved_by="#1",
                         moved_on="2026-09-03")
    except sa.SequencedAfterError as exc:
        assert "does not read back" in str(exc), str(exc)
    else:  # pragma: no cover - the refusal is the assertion
        raise AssertionError("a ledger that does not read back must refuse")


def test_the_SEEDER_REPAIRS_a_ledger_too_malformed_to_READ(tmp_path):
    # Refusing here would leave the only tool that can rewrite the file
    # unusable on the only file that needs rewriting.
    _change(tmp_path, "add-a")
    path = sa.ledger_path(tmp_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("schema_version: 1\nkind: k\nrows: not-a-mapping\n",
                    encoding="utf-8")
    result = subprocess.run(
        [sys.executable, str(VALIDATOR), str(tmp_path), "--seed-ledger",
         "--moved-by", "#623", "--moved-on", "2026-09-03"],
        capture_output=True, text=True)
    assert result.returncode == 0, result.stdout + result.stderr
    assert "could not be read" in result.stderr
    assert "EVERY row is stamped #623" in result.stderr
    assert "1 rows, 1 moved by #623" in result.stdout
    assert sa.ledger_problems(sa.classify_corpus(tmp_path),
                              sa.load_ledger(path)) == []


def test_the_SEEDER_REFUSES_a_bad_provenance_WITHOUT_a_traceback(tmp_path):
    # A stack trace tells an author where the library gave up, not what to type
    # instead — and this command is the thing they run when something is wrong.
    _change(tmp_path, "add-a")
    for flags, expected in (
        (["--moved-by", "620"], "--moved-by must be a pull request reference"),
        (["--moved-by", "#620", "--moved-on", "soon"],
         "--moved-on must be an ISO date"),
        (["--moved-by", "#620", "--moved-on", "2026-13-45"],
         "--moved-on must be an ISO date"),
        # AN EMPTY STRING IS A VALUE THE OPERATOR TYPED. It was already
        # refused — here, and again inside `render_ledger` — but nothing PINNED
        # that, so a later edit to either guard could have let it through to a
        # `moved_on or today` that stamps today over it. (Copilot round 3.)
        (["--moved-by", "#620", "--moved-on", ""],
         "--moved-on must be an ISO date"),
    ):
        result = subprocess.run(
            [sys.executable, str(VALIDATOR), str(tmp_path), "--seed-ledger",
             *flags], capture_output=True, text=True)
        assert result.returncode != 0, flags
        assert "Traceback" not in result.stderr, result.stderr
        assert expected in result.stderr, result.stderr


def test_the_SEED_LEDGER_help_does_not_call_moved_by_OPTIONAL():
    # The usage text and the refusal must agree: `--moved-by` is required with
    # `--seed-ledger`, and help that brackets it teaches the opposite.
    result = subprocess.run(
        [sys.executable, str(VALIDATOR), "--help"],
        capture_output=True, text=True)
    assert result.returncode == 0, result.stdout + result.stderr
    assert "--seed-ledger --moved-by '#PR'" in " ".join(result.stdout.split())
    assert "REQUIRED with --seed-ledger" in " ".join(result.stdout.split())


def test_the_CLI_MODES_are_MUTUALLY_EXCLUSIVE(tmp_path):
    # Combining two modes can only mean the caller believed both would run;
    # silently running the first is the answer to a question nobody asked.
    for flags in (["--seed-ledger", "--ledger-diff"],
                  ["--sweep", "--ledger-diff"],
                  ["--sweep", "--seed-ledger"],
                  ["--archive-gate", str(tmp_path), "--sweep"]):
        result = subprocess.run(
            [sys.executable, str(VALIDATOR), str(tmp_path), *flags],
            capture_output=True, text=True)
        assert result.returncode != 0, flags
        assert "not allowed with argument" in result.stderr, flags


def test_the_ARCHIVE_GATE_resolves_a_relative_dir_against_REPO_ROOT(tmp_path):
    # Every other mode resolves against `repo_root`; this one resolved against
    # the CWD, so the same relative CHANGE_DIR could name a DIFFERENT
    # repository's change of the same name — and a gate that checks the wrong
    # directory and PASSES is the failure a gate can least afford.
    elsewhere = tmp_path / "elsewhere"
    _change(elsewhere, "add-a")
    decoy = tmp_path / "decoy"
    _change(decoy, "add-a")
    result = subprocess.run(
        [sys.executable, str(VALIDATOR), str(elsewhere), "--archive-gate",
         "openspec/changes/add-a", "--ratified-ref", "HEAD"],
        capture_output=True, text=True, cwd=str(decoy))
    combined = result.stdout + result.stderr
    # It reaches the RETENTION gate on the named repo rather than failing to
    # find the directory: the git call is what refuses next, and it names the
    # tree it was pointed at.
    assert "elsewhere" in combined or "does not exist" not in combined, combined
    assert "decoy" not in combined, (
        "a relative CHANGE_DIR must not resolve into the current directory's "
        "repository: " + combined)


def test_a_FLAG_OUTSIDE_ITS_MODE_is_REFUSED_not_ignored(tmp_path):
    # The same doctrine the mutually exclusive modes rest on: accepting
    # `--ledger-diff --moved-by garbage` and exiting 0 tells a caller their flag
    # was honoured when nothing read it.
    _change(tmp_path, "add-a")
    for flags, expected in (
        (["--ledger-diff", "--moved-by", "garbage"],
         "--moved-by is only meaningful with --seed-ledger"),
        (["--ledger-diff", "--ratified-ref", "HEAD"],
         "--ratified-ref is only meaningful with --archive-gate"),
        (["--sweep", "--seeded-from", "abc"],
         "--seeded-from is only meaningful with --seed-ledger"),
        (["--sweep", "--moved-on", "2026-09-03"],
         "--moved-on is only meaningful with --seed-ledger"),
    ):
        result = subprocess.run(
            [sys.executable, str(VALIDATOR), str(tmp_path), *flags],
            capture_output=True, text=True)
        assert result.returncode == 2, (flags, result.stdout, result.stderr)
        assert expected in result.stderr, result.stderr
    # ...and the legitimate pairings still run.
    for flags in (["--seed-ledger", "--moved-by", "#1", "--moved-on",
                   "2026-09-03", "--seeded-from", "abc"], ["--ledger-diff"],
                  ["--sweep"]):
        result = subprocess.run(
            [sys.executable, str(VALIDATOR), str(tmp_path), *flags],
            capture_output=True, text=True)
        assert result.returncode == 0, (flags, result.stdout, result.stderr)


def test_the_SEED_LEDGER_cli_REQUIRES_a_moving_pull_request(tmp_path):
    _change(tmp_path, "add-a")
    result = subprocess.run(
        [sys.executable, str(VALIDATOR), str(tmp_path), "--seed-ledger"],
        capture_output=True, text=True)
    assert result.returncode != 0
    assert "--moved-by" in result.stderr


def test_the_SWEEP_output_is_UNCHANGED_by_this_change(tmp_path):
    # `--sweep` is the substrate's own shipped report (task 5.4) and this change
    # does not touch what it prints.
    _change(tmp_path, "add-a")
    result = subprocess.run(
        [sys.executable, str(VALIDATOR), str(tmp_path), "--sweep"],
        capture_output=True, text=True)
    assert result.returncode == 0, result.stdout + result.stderr
    assert result.stdout.rstrip("\n") == sa.corpus_sweep(tmp_path).render()


# --- the archive date and `moved_on` are ONE FACT (issue #790) --------------
#
# `--seed-ledger` stamped `moved_on` from `datetime.date.today()` — the
# MACHINE'S LOCAL clock — while the OpenSpec CLI names
# `openspec/changes/archive/<YYYY-MM-DD>-<id>/` from its own, and nothing
# compared them. A 23:35-local archive therefore produced a `2026-09-07-`
# directory on a UTC `2026-09-08` day (PR #780's packet). The seeder now takes
# an archived row's date FROM ITS DIRECTORY, and the plain validator run reports
# every archived row where the two disagree.


def _utc_today() -> str:
    """Today in UTC, the clock `--moved-on` now defaults to."""
    import datetime
    return datetime.datetime.now(datetime.timezone.utc).date().isoformat()


def test_a_NEW_row_for_an_ALREADY_ARCHIVED_change_takes_the_RUN_DATE(tmp_path):
    """NOT A FLIP, so not the archive's date — the narrowing taken from review.

    `release-realization`'s per-subject-row requirement defines the provenance
    pair as the pull request that last moved the row AND THE DATE OF THAT MOVE.
    A row created today for a change archived in August moved today; writing
    August beside today's pull request would make the pair state two different
    moves.
    """
    _change(tmp_path, "add-a")
    _change(tmp_path, "add-old", archived="2026-08-01")
    # BRACKETED, NOT COMPARED TO ONE READING. The seeder runs in a CHILD
    # process, so a run that crossed midnight UTC between these two readings
    # would legitimately observe two different days and an equality assertion
    # would fail for the calendar rather than for the code.
    before = _utc_today()
    result = subprocess.run(
        [sys.executable, str(VALIDATOR), str(tmp_path), "--seed-ledger",
         "--moved-by", "#790"], capture_output=True, text=True)
    after = _utc_today()
    assert result.returncode == 0, result.stdout + result.stderr
    rows = sa.load_ledger(sa.ledger_path(tmp_path)).rows
    assert rows["add-old"]["state"] == "archived"
    assert rows["add-old"]["moved_on"] in {before, after}
    assert rows["add-a"]["moved_on"] in {before, after}
    assert rows["add-old"]["moved_on"] != "2026-08-01", (
        "an already-archived change's NEW row is not a flip and must not take "
        "the archive's date")


def test_the_SEEDER_stamps_the_DIRECTORY_date_when_a_row_FLIPS_to_archived(
        tmp_path):
    """THE FLIP is the moment the two facts become one, and it is the moment
    the old seeder got wrong: the row moves BECAUSE the change archived, so the
    date it records is the archive's, not the re-seed's."""
    _change(tmp_path, "add-a")
    path = _ledger(tmp_path, [_row("add-a", moved_by="#1",
                                   moved_on="2026-01-01")])
    assert sa.load_ledger(path).rows["add-a"]["state"] == "active"
    _change(tmp_path, "add-a", archived="2026-08-14")
    import shutil
    shutil.rmtree(tmp_path / "openspec" / "changes" / "add-a")
    result = subprocess.run(
        [sys.executable, str(VALIDATOR), str(tmp_path), "--seed-ledger",
         "--moved-by", "#790"], capture_output=True, text=True)
    assert result.returncode == 0, result.stdout + result.stderr
    row = sa.load_ledger(path).rows["add-a"]
    assert row["state"] == "archived"
    assert row["moved_by"] == "#790"
    assert row["moved_on"] == "2026-08-14"


def test_an_EXPLICIT_moved_on_that_the_DIRECTORY_CONTRADICTS_is_REFUSED(tmp_path):
    """NEVER SILENTLY OVERRIDDEN. A caller who typed a date and got a different
    one written was told their flag was honoured when it was not — the same
    mistake `--ledger-diff --moved-by garbage` is refused for."""
    _change(tmp_path, "add-old")
    path = _ledger(tmp_path, [_row("add-old", moved_by="#1",
                                   moved_on="2026-01-01")])
    before = path.read_text(encoding="utf-8")
    _change(tmp_path, "add-old", archived="2026-08-01")
    import shutil
    shutil.rmtree(tmp_path / "openspec" / "changes" / "add-old")
    result = subprocess.run(
        [sys.executable, str(VALIDATOR), str(tmp_path), "--seed-ledger",
         "--moved-by", "#790", "--moved-on", "2026-09-08"],
        capture_output=True, text=True)
    assert result.returncode == 2, result.stdout + result.stderr
    assert "add-old (2026-08-01)" in result.stderr
    assert "the same act" in result.stderr
    assert "Traceback" not in result.stderr
    assert path.read_text(encoding="utf-8") == before, (
        "a refused re-seed writes nothing")


def test_an_EXPLICIT_moved_on_that_AGREES_with_every_directory_is_ACCEPTED(
        tmp_path):
    # ANTI-VACUITY for the refusal above: the flag is not simply banned in the
    # presence of an archived row.
    _change(tmp_path, "add-old")
    _ledger(tmp_path, [_row("add-old", moved_by="#1", moved_on="2026-01-01")])
    _change(tmp_path, "add-old", archived="2026-08-01")
    import shutil
    shutil.rmtree(tmp_path / "openspec" / "changes" / "add-old")
    result = subprocess.run(
        [sys.executable, str(VALIDATOR), str(tmp_path), "--seed-ledger",
         "--moved-by", "#790", "--moved-on", "2026-08-01"],
        capture_output=True, text=True)
    assert result.returncode == 0, result.stdout + result.stderr
    assert sa.load_ledger(sa.ledger_path(tmp_path)).rows["add-old"]["moved_on"] \
        == "2026-08-01"


def test_an_UNMOVED_archived_row_is_NOT_RESTAMPED_by_the_new_rule(tmp_path):
    """The seeder's oldest promise still holds: a row that did not move keeps
    the provenance it carried. A seeder that rewrote the 124 archived rows
    whose date is later than their directory would make every re-seed a
    124-row diff — and those rows are not defects: they record later moves,
    which is what `release-realization` says `moved_on` means."""
    _change(tmp_path, "add-old", archived="2026-08-01")
    path = _ledger(tmp_path, [_row("add-old", state="archived", moved_by="#1",
                                   moved_on="2026-09-03")])
    result = subprocess.run(
        [sys.executable, str(VALIDATOR), str(tmp_path), "--seed-ledger",
         "--moved-by", "#790"], capture_output=True, text=True)
    assert result.returncode == 0, result.stdout + result.stderr
    assert sa.load_ledger(path).rows["add-old"]["moved_on"] == "2026-09-03"
    assert sa.load_ledger(path).rows["add-old"]["moved_by"] == "#1"


def test_the_PLAIN_RUN_GATES_on_a_moved_on_that_PREDATES_its_directory(tmp_path):
    """THE CONTRADICTION, which no reading of the provenance pair permits: the
    row says `archived` and claims a move OLDER than the archive that made it
    archived. It is also the shape a CLI clock running AHEAD of UTC produces."""
    _change(tmp_path, "add-old", archived="2026-08-01")
    _ledger(tmp_path, [_row("add-old", state="archived", moved_on="2026-07-31")])
    result = subprocess.run(
        [sys.executable, str(VALIDATOR), str(tmp_path)],
        capture_output=True, text=True)
    assert result.returncode == 1, result.stdout + result.stderr
    assert "archive-date contradiction: add-old" in result.stdout, result.stdout
    assert "'2026-07-31'" in result.stdout and "'2026-08-01'" in result.stdout


def test_a_LATER_moved_on_is_NOT_a_finding_by_default(tmp_path):
    """A LEGITIMATE later move, and the correction taken from review.

    `release-realization` defines `moved_on` as the date the ROW last moved, so
    an archived change whose reading is moved by a later pull request carries a
    later date. 124 of this corpus's 143 archived rows do. Reporting them would
    call a correct ledger stale."""
    _change(tmp_path, "add-old", archived="2026-08-01")
    _ledger(tmp_path, [_row("add-old", state="archived", moved_on="2026-09-03")])
    result = subprocess.run(
        [sys.executable, str(VALIDATOR), str(tmp_path)],
        capture_output=True, text=True)
    assert result.returncode == 0, result.stdout + result.stderr
    assert "contradiction" not in result.stdout
    assert "drift" not in result.stdout


def test_an_UNREADABLE_moved_on_is_left_to_the_LEDGER_DIFF_to_name(tmp_path):
    """Reported once, in one vocabulary. `ledger_problems` already names
    malformed provenance; comparing a value that is not a date would send the
    author to a second, wrong repair."""
    _change(tmp_path, "add-old", archived="2026-08-01")
    _ledger(tmp_path, [_row("add-old", state="archived", moved_on="September")])
    result = subprocess.run(
        [sys.executable, str(VALIDATOR), str(tmp_path)],
        capture_output=True, text=True)
    assert result.returncode == 0, result.stdout + result.stderr
    assert "archive-date contradiction" not in result.stdout


def test_the_SEEDER_REFUSES_a_FLIP_whose_directory_is_dated_AFTER_TODAY(tmp_path):
    """The ahead-clock refusal, at the moment the stamp would be written: a
    directory dated in the future can only have been named by a clock running
    ahead of UTC, and stamping its date would create the contradiction the
    validator gates on."""
    _change(tmp_path, "add-old")
    _ledger(tmp_path, [_row("add-old", moved_by="#1", moved_on="2026-01-01")])
    _change(tmp_path, "add-old", archived="2999-01-01")
    import shutil
    shutil.rmtree(tmp_path / "openspec" / "changes" / "add-old")
    result = subprocess.run(
        [sys.executable, str(VALIDATOR), str(tmp_path), "--seed-ledger",
         "--moved-by", "#790"], capture_output=True, text=True)
    assert result.returncode == 2, result.stdout + result.stderr
    assert "add-old (2999-01-01)" in result.stderr
    assert "ahead of UTC" in result.stderr
    assert "Traceback" not in result.stderr


def test_a_CONSISTENT_corpus_is_SILENT_and_says_the_arm_PASSED(tmp_path):
    _change(tmp_path, "add-old", archived="2026-08-01")
    _ledger(tmp_path, [_row("add-old", state="archived", moved_on="2026-08-01")])
    for flags in ([], ["--strict-archive-dates"]):
        result = subprocess.run(
            [sys.executable, str(VALIDATOR), str(tmp_path), *flags],
            capture_output=True, text=True)
        assert result.returncode == 0, (flags, result.stdout, result.stderr)
        assert "archive-date agreement passed" in result.stdout
        assert "contradiction" not in result.stdout
        assert "drift" not in result.stdout


def test_STRICT_ARCHIVE_DATES_asks_for_the_STRONGER_reading(tmp_path):
    """The reading issue #790 proposed, kept and made OPT-IN rather than
    dropped: an archived row's moved_on IS its archive date. 124 live rows do
    not satisfy it and are not defects, which is why it is not the default."""
    _change(tmp_path, "add-old", archived="2026-08-01")
    _ledger(tmp_path, [_row("add-old", state="archived", moved_on="2026-09-03")])
    result = subprocess.run(
        [sys.executable, str(VALIDATOR), str(tmp_path),
         "--strict-archive-dates"], capture_output=True, text=True)
    assert result.returncode == 1, result.stdout + result.stderr
    assert "archive-date agreement FAILED" in result.stdout
    assert "archive-date drift: add-old" in result.stdout


def test_STRICT_ARCHIVE_DATES_is_REFUSED_OUTSIDE_the_plain_run(tmp_path):
    _change(tmp_path, "add-a")
    for mode in (["--sweep"], ["--ledger-diff"],
                 ["--seed-ledger", "--moved-by", "#1"]):
        result = subprocess.run(
            [sys.executable, str(VALIDATOR), str(tmp_path),
             "--strict-archive-dates", *mode], capture_output=True, text=True)
        assert result.returncode == 2, (mode, result.stdout, result.stderr)
        assert "--strict-archive-dates is only meaningful" in result.stderr


def test_a_MISSING_LEDGER_does_not_make_the_PLAIN_RUN_a_verdict(tmp_path):
    """`--ledger-diff` owns ledger readability, and answers it with exit 2 — a
    status the plain run does not have and must not invent."""
    _change(tmp_path, "add-old", archived="2026-08-01")
    result = subprocess.run(
        [sys.executable, str(VALIDATOR), str(tmp_path)],
        capture_output=True, text=True)
    assert result.returncode == 0, result.stdout + result.stderr
    assert "archive-date arm NOT RUN" in result.stdout
    path = sa.ledger_path(tmp_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("rows: [not, a, mapping]\n", encoding="utf-8")
    result = subprocess.run(
        [sys.executable, str(VALIDATOR), str(tmp_path)],
        capture_output=True, text=True)
    assert result.returncode == 0, result.stdout + result.stderr
    assert "archive-date arm NOT RUN" in result.stdout
    assert "--ledger-diff reports that class" in result.stdout


def test_an_id_in_BOTH_corpora_is_read_as_ACTIVE_and_NOT_date_checked(tmp_path):
    """The classifier reads such an id as ACTIVE, `resolve` reports the
    ambiguity, and this arm must not report the SAME defect in a second
    vocabulary that sends the author to a provenance repair."""
    _change(tmp_path, "add-a")
    _change(tmp_path, "add-a", archived="2026-08-01")
    _ledger(tmp_path, [_row("add-a", state="active", moved_on="2026-07-31")])
    result = subprocess.run(
        [sys.executable, str(VALIDATOR), str(tmp_path)],
        capture_output=True, text=True)
    assert "contradiction" not in result.stdout, result.stdout


def test_TWO_ARCHIVE_DIRECTORIES_for_one_id_are_NOT_date_checked(tmp_path):
    """Two dated directories is an AMBIGUITY `resolve` refuses. Picking one here
    would decide it silently, in the one place that stamps provenance."""
    _change(tmp_path, "add-old", archived="2026-08-01")
    _change(tmp_path, "add-old", archived="2026-08-02")
    assert "add-old" not in sa.archive_dates(tmp_path)
    _ledger(tmp_path, [_row("add-old", state="archived", moved_on="2026-07-31")])
    result = subprocess.run(
        [sys.executable, str(VALIDATOR), str(tmp_path)],
        capture_output=True, text=True)
    assert "contradiction" not in result.stdout, result.stdout



def test_a_STALE_ACTIVE_ROW_for_an_ARCHIVED_id_is_the_LEDGER_DIFFS_finding(
        tmp_path):
    """ONE FACT, ONE VOCABULARY, and this one was named twice.

    The arm's own finding reads "an archived row cannot record a move that
    predates the archive that made it archived" — a sentence about a row that
    CLAIMS to be archived. A row still saying `active` for an id that is
    archived on disk claims no such thing: it is simply out of date, which is
    `--ledger-diff`'s stale-row class and whose repair is a re-seed. Reporting
    it here as an archive-date contradiction sent the author to a second repair
    (go and correct `moved_on`) for a row whose `moved_on` is not the problem.
    """
    _change(tmp_path, "add-old", archived="2026-08-01")
    _ledger(tmp_path, [_row("add-old", state="active", moved_on="2026-07-31")])
    plain = subprocess.run(
        [sys.executable, str(VALIDATOR), str(tmp_path)],
        capture_output=True, text=True)
    assert "archive-date contradiction" not in plain.stdout, plain.stdout
    assert "archive-date drift" not in plain.stdout
    # …and the stale row IS reported, by the mode that owns the class.
    diff = subprocess.run(
        [sys.executable, str(VALIDATOR), str(tmp_path), "--ledger-diff"],
        capture_output=True, text=True)
    assert diff.returncode != 0, diff.stdout + diff.stderr
    assert "add-old" in diff.stdout + diff.stderr
    # The strict reading agrees: it is the same row, and the same non-finding.
    strict = subprocess.run(
        [sys.executable, str(VALIDATOR), str(tmp_path),
         "--strict-archive-dates"], capture_output=True, text=True)
    assert "archive-date drift" not in strict.stdout, strict.stdout
    assert "archive-date contradiction" not in strict.stdout, strict.stdout
    assert "archive-date agreement passed" in strict.stdout


# ---- the seeder's default `moved_on` is UTC, ON A UTC RUNNER TOO -----------
#
# `_utc_today()` replaced `datetime.date.today()`, and every test of it read the
# host's own clock — so on the UTC runner CI uses, the two readings agree and
# the mutation `_utc_today -> date.today` passed the whole suite. The clock is
# therefore FROZEN, in a child process, at an instant where UTC and the
# machine's local day are two different days.

_FROZEN_CLOCK_DRIVER = '''
import datetime, importlib.util, os, sys, time

# A REAL ZONE, SET ON THE PROCESS, because the defect is about what
# `datetime.date.today()` reads: `Pacific/Kiritimati` is UTC+14, the extreme of
# the ahead-of-UTC direction, and `time.tzset()` is what makes the C library
# and therefore `astimezone()` honour it.
os.environ["TZ"] = "Pacific/Kiritimati"
time.tzset()

# 23:35 UTC: the hour PR #780's archive actually ran at, and an hour at which
# UTC+14 is already on the NEXT day.
WHEN = datetime.datetime(2026, 9, 8, 23, 35, tzinfo=datetime.timezone.utc)


# BOUND BEFORE THE CLASS BODY: inside `_FrozenDatetimeModule` the name
# `datetime` is being rebound to the stub, so the real module's own attributes
# have to be read out here or the class body reads its own half-built self.
_REAL_TIMEZONE = datetime.timezone
_REAL_TIMEDELTA = datetime.timedelta


class _Datetime(datetime.datetime):
    @classmethod
    def now(cls, tz=None):
        return WHEN.astimezone(tz) if tz is not None else WHEN.astimezone()


class _Date(datetime.date):
    @classmethod
    def today(cls):
        # THE MACHINE'S LOCAL CLOCK, which is the value the defect wrote.
        return WHEN.astimezone().date()


class _FrozenDatetimeModule:
    datetime = _Datetime
    date = _Date
    timezone = _REAL_TIMEZONE
    timedelta = _REAL_TIMEDELTA


spec = importlib.util.spec_from_file_location("validator_under_test", sys.argv[1])
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
module.datetime = _FrozenDatetimeModule
print(module._utc_today())
print(_Date.today().isoformat())
'''


def test_the_SEEDERS_DEFAULT_DATE_IS_UTC_AND_NOT_THE_LOCAL_DAY(tmp_path):
    """The guard that fails on a UTC runner, which no earlier test could.

    Mutate `_utc_today` back to `datetime.date.today().isoformat()` and this
    test reports `2026-09-09` where UTC says `2026-09-08`. The second assertion
    is its ANTI-VACUITY: at the frozen instant the two days really are two days,
    so the first assertion cannot pass by the distinction being unobservable.
    """
    driver = tmp_path / "frozen_clock_driver.py"
    driver.write_text(_FROZEN_CLOCK_DRIVER, encoding="utf-8")
    result = subprocess.run(
        [sys.executable, str(driver), str(VALIDATOR)],
        capture_output=True, text=True)
    assert result.returncode == 0, result.stdout + result.stderr
    utc_day, local_day = result.stdout.split()
    assert local_day == "2026-09-09", (
        "the fixture's own premise: under Pacific/Kiritimati at 23:35 UTC the "
        "machine's local day is tomorrow")
    assert utc_day == "2026-09-08", (
        "`--moved-on` defaulted to the MACHINE'S day, which is issue #790 on "
        "the ledger side of the same archive")


def test_the_SEEDER_STAMPS_THE_UTC_DAY_UNDER_AN_AHEAD_OF_UTC_TZ(tmp_path):
    """The same property END TO END, through the CLI an operator actually runs.

    BRACKETED rather than compared to one reading: the seeder runs in a child
    process, so a run that crossed midnight UTC between the two readings would
    legitimately observe two different days. This test DISTINGUISHES the two
    clocks only while UTC is past 10:00 (the hours in which UTC+14 is already
    on the next day); the frozen-clock test above is the one that fails
    wherever it is run.
    """
    import datetime as _dt
    import os
    _change(tmp_path, "add-a")

    def utc_now() -> str:
        return _dt.datetime.now(_dt.timezone.utc).date().isoformat()

    before = utc_now()
    result = subprocess.run(
        [sys.executable, str(VALIDATOR), str(tmp_path), "--seed-ledger",
         "--moved-by", "#790"],
        capture_output=True, text=True,
        env={**os.environ, "TZ": "Pacific/Kiritimati"})
    after = utc_now()
    assert result.returncode == 0, result.stdout + result.stderr
    stamped = sa.load_ledger(sa.ledger_path(tmp_path)).rows["add-a"]["moved_on"]
    assert stamped in (before, after), (
        f"{stamped!r} is neither UTC day this run spanned "
        f"({before!r}, {after!r}) — the local Kiritimati day is a day ahead")


# ---- a row cannot move before the change existed (issue #743) --------------
#
# #790 (above) fixed the seeder's DEFAULT `--moved-on` to read UTC rather than
# the machine's local day; #743 was filed against the same paragraph before
# that fix landed and asked, additionally, for a guard this file did not yet
# have: refuse a `moved_on` (defaulted OR explicit, and on a flip too) that
# predates the change's own `.openspec.yaml` `created:` date. The reader that
# gets `created:` (`_created_dates`) lives on `validate-sequenced-after.py`
# itself rather than on the shared `sequenced_after` library module, so these
# are exercised through the CLI subprocess, exactly as every other
# `--seed-ledger` behaviour above is.


def test_the_SEEDER_REFUSES_a_moved_on_EARLIER_than_the_changes_created_date(
        tmp_path):
    _change(tmp_path, "add-a", created="2026-09-15")
    result = subprocess.run(
        [sys.executable, str(VALIDATOR), str(tmp_path), "--seed-ledger",
         "--moved-by", "#743", "--moved-on", "2026-09-10"],
        capture_output=True, text=True)
    assert result.returncode == 2, result.stdout + result.stderr
    assert "add-a" in result.stderr
    assert "created" in result.stderr
    assert not sa.ledger_path(tmp_path).is_file(), (
        "a refused seed must not write a ledger — the ONE-REFUSAL discipline "
        "the directory-ahead-of-UTC guard above already keeps")


def test_the_SEEDER_REFUSES_the_DEFAULTED_UTC_moved_on_TOO(tmp_path):
    """The SAME guard over the `moved_on is None` branch, where `effective`
    is `today` rather than an explicit `--moved-on` or a flip's directory
    date — the one branch an explicit-`--moved-on`-only suite would leave
    unwatched (Copilot round 1, PR #990)."""
    _change(tmp_path, "add-a", created="2099-01-01")
    result = subprocess.run(
        [sys.executable, str(VALIDATOR), str(tmp_path), "--seed-ledger",
         "--moved-by", "#743"],
        capture_output=True, text=True)
    assert result.returncode == 2, result.stdout + result.stderr
    assert "add-a" in result.stderr
    assert "created" in result.stderr
    assert not sa.ledger_path(tmp_path).is_file()


def test_the_SEEDER_ACCEPTS_a_moved_on_EQUAL_TO_the_changes_created_date(
        tmp_path):
    _change(tmp_path, "add-a", created="2026-09-10")
    result = subprocess.run(
        [sys.executable, str(VALIDATOR), str(tmp_path), "--seed-ledger",
         "--moved-by", "#743", "--moved-on", "2026-09-10"],
        capture_output=True, text=True)
    assert result.returncode == 0, result.stdout + result.stderr
    row = sa.load_ledger(sa.ledger_path(tmp_path)).rows["add-a"]
    assert row["moved_on"] == "2026-09-10"


def test_the_SEEDER_ACCEPTS_a_moved_on_LATER_than_the_changes_created_date(
        tmp_path):
    _change(tmp_path, "add-a", created="2026-01-01")
    result = subprocess.run(
        [sys.executable, str(VALIDATOR), str(tmp_path), "--seed-ledger",
         "--moved-by", "#743", "--moved-on", "2026-09-10"],
        capture_output=True, text=True)
    assert result.returncode == 0, result.stdout + result.stderr
    row = sa.load_ledger(sa.ledger_path(tmp_path)).rows["add-a"]
    assert row["moved_on"] == "2026-09-10"


def test_a_change_with_NO_readable_created_date_is_NOT_gated(tmp_path):
    # No `.openspec.yaml` at all — the common case for most of the corpus —
    # is a permissive read, not a refusal waiting to happen.
    _change(tmp_path, "add-a")
    result = subprocess.run(
        [sys.executable, str(VALIDATOR), str(tmp_path), "--seed-ledger",
         "--moved-by", "#743", "--moved-on", "2020-01-01"],
        capture_output=True, text=True)
    assert result.returncode == 0, result.stdout + result.stderr


def test_the_SEEDER_GUARD_APPLIES_TO_A_FLIPS_DIRECTORY_DATE_TOO(tmp_path):
    """A row FLIPPING to archived takes its DIRECTORY'S date, not the run's
    (issue #790) — and that is the stamp this guard has to compare, or a
    change archived (by directory name) before it was created would sail
    through on the run's own, later, date."""
    _change(tmp_path, "add-a")
    _ledger(tmp_path, [_row("add-a", moved_by="#1", moved_on="2026-01-01")])
    _change(tmp_path, "add-a", archived="2026-01-10", created="2026-06-01")
    import shutil
    shutil.rmtree(tmp_path / "openspec" / "changes" / "add-a")
    result = subprocess.run(
        [sys.executable, str(VALIDATOR), str(tmp_path), "--seed-ledger",
         "--moved-by", "#743"],
        capture_output=True, text=True)
    assert result.returncode == 2, result.stdout + result.stderr
    assert "add-a" in result.stderr
    assert "2026-01-10" in result.stderr and "2026-06-01" in result.stderr
