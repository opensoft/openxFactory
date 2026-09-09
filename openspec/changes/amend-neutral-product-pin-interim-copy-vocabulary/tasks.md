# Tasks: amend-neutral-product-pin-interim-copy-vocabulary

Status: ratified
Ratified by: amend-neutral-product-pin-interim-copy-vocabulary — 2026-09-09, Brett Heap, "Ratify with TOLERATED" (record `review/ratification-2026-09-09.md`)
Kind: tasks

`code_surface: none`, `target_release: none`. There is no realization group,
because there is nothing to realize: the delta is requirement prose, no script,
test, workflow, contract, schema or example reads the word it reserves, and
under `release-realization` an empty code surface archives ON LANDING plus this
task list rather than on merged-plus-green realization evidence. **The
"realization" of a wording amendment IS its promotion at archive.**

**NOTHING IS TICKED THAT DID NOT LAND.** Every ticked box below is a diff in
this pull request or a measurement recorded verbatim in its body. **§ 1
(ratification) IS NOW TICKED AND NAMES THE WORD THAT TICKED IT** — Brett Heap's
*"Ratify with TOLERATED"* of 2026-09-09, which is his act and not the authoring
lane's. **§ 4 (archive) STAYS ENTIRELY OPEN**: promotion is a separate act on a
separate word, so openxFactory #868 closes at the archive and not at this
landing. § 5 records what was measured and deliberately not taken.

## 1. Ratification — GIVEN 2026-09-09

- [x] 1.1 **RATIFIED 2026-09-09 by Brett Heap** (openxFactory operator
      authority), verbatim *"Ratify with TOLERATED"*, given as a
      MULTIPLE-CHOICE ruling and recorded on PR **#870** at
      2026-09-09T23:31:12Z. The earlier word of 2026-09-09, verbatim *"R1
      'lawful' amendment packet"*, stays recorded as the ORIGIN of the
      AUTHORING — it commissioned a lane to write the remedy, ratified no
      wording and took no design decision, and it is not read as an approval.
      `proposal.md`, `design.md` and this file now carry `Status: ratified` with
      **ONE** citation line each (`Ratified:` in `proposal.md`, `Ratified by:`
      here and in `design.md`), which is what `ratified-provenance` counts.
      `.openspec.yaml` gains `approved_by`/`approved_on` **BESIDE** the drafting
      provenance with `kind` and `id` unmoved — the addition-not-rewrite shape
      `add-drafted-proposal-origin` (issue #318) defined for this transition and
      the shape the archive gate's origin-retention arm reads. Records:
      `review/ratification-2026-09-09.md`, with the gate run re-derived on the
      ratified tree beside it at `review/verification-2026-09-09.md`.
- [x] 1.2 **`design.md` D1 IS RULED — TOLERATED, NOT PERMITTED.** The veto point
      was put and the recommendation was TAKEN, so **the encoded wording stands
      UNCHANGED and no substitution was performed**: the seven occurrences
      enumerated below are ratified exactly as written. TOLERATED was
      recommended and written. PERMITTED is the alternative and is
      the word the refusal on PR #780 itself floated (*"say `PERMITTED as a
      declared interim` in the scenario"*), which is why it is put rather than
      simply passed over. D1 records three reasons for TOLERATED — PERMITTED is
      a near-synonym of LAWFUL and the defect is that two statuses shared one
      word; the admission is conditional and terminal and TOLERATED is the word
      for that; and PERMITTED is already spent one capability over
      (`domain-descendant-boundary:113`, *"the placement is permitted"*) on a
      non-deprecated state. **A veto is a case-preserving substitution over an
      ENUMERATED set of SEVEN occurrences inside the `## MODIFIED` block** —
      `specs/neutral-product-pin/spec.md` lines 121, 133, 134 (added body
      paragraph), 170, 171 (the two replaced canon bullets) and 185, 186 (added
      scenario) — listed line by line in `design.md` D1, plus one in the delta's
      own header prose at line 25 and the packet's prose, neither of which is
      ratification surface. **Replacing only some would leave both status words
      live in one requirement**, which is the defect this packet closes, so the
      set is enumerated rather than counted. The marker's reason names no status
      word and does not move; nothing else in the packet moves either. **The
      seven are NOT redundant and are deliberately not reduced** — D1 records
      what each does.
- [x] 1.3 **`design.md` D2 and D4 STOOD — neither was vetoed.** The ruling of
      2026-09-09 reached D1 and left both additions as designed: the body
      paragraph and the added scenario are ratified as encoded. D2 puts the
      reservation in the requirement BODY rather than leaving the two bullets to
      carry it alone (Codex's finding is satisfiable by the bullets alone; the
      refusal on #780 named the gap that leaves). D4 adds ONE scenario at the
      END of the block asserting the record obligation. Each is separately
      vetoable: a veto of D2 leaves the two bullets and the marker; a veto of D4
      leaves the body paragraph unasserted by any scenario.

## 2. The delta — DONE IN THIS PULL REQUEST

- [x] 2.1 **ONE `## MODIFIED` requirement, written OVER CANON**, byte-faithful
      to `openspec/specs/neutral-product-pin/spec.md:264-384` as `main` states
      it except for the units § 2.2 and § 2.3 name. The requirement's first body
      line carries SHALL (*"A consumption pin SHALL be a PUBLISHED contract
      member…"*), and every one of its eight scenarios — the seven canon carries
      plus the one added — has at least one `WHEN`/`THEN` bullet.
- [x] 2.2 **TWO SCENARIO BULLETS REPLACED IN PLACE, one word each**, under
      *A repository with no stack pin adopts the gate anyway*: `lawful` →
      `TOLERATED` in the `THEN`, with the reserved reading named in the same
      bullet; `lawful` → `tolerated` in the `AND`. Declared by ONE
      `Removed from canon by amend-neutral-product-pin-interim-copy-vocabulary
      (2026-09-09):` marker placed after the scenarios it names — the placement
      `refresh-install-repository-enumerations` used for the same edit shape.
      The first named unit is fenced with a doubled backtick run (it contains
      `` `openxFactory` ``); the reason carries **no code span at all**, so the
      second marker-defect ground `amend-marker-defect-reporting` added cannot
      fire on it.
- [x] 2.3 **ONE BODY PARAGRAPH AND ONE SCENARIO ADDED.** The paragraph states
      the reservation in one place, between the fallback paragraph and the
      enforcement paragraph, so the word is defined before it is spent. The
      scenario — *A record describes a declared interim copy as lawful* — sits
      at the END of the block; **no promoted scenario moves, is retitled, or
      loses a bullet.**
- [x] 2.4 **THE RESERVATION IS SCOPED, NOT CAPABILITY-WIDE** (`design.md` D0a).
      The specification's fifth use of `lawful` is at `:555`, in *A
      dispositioned finding is cited, upgrade-coupled, and refused when stale*,
      on a DISPOSITION's acceptance rather than on a consumption's status. The
      added paragraph reads *"WHERE THIS REQUIREMENT SPEAKS OF A CONSUMPTION'S
      STATUS…"* so it does not reach that sentence; a capability-wide claim
      would have put ratified text in another requirement in violation on the
      day this promoted.
- [x] 2.5 **THE TWO CORRECT BODY USES ARE CARRIED UNCHANGED** — `:299-300`
      (*"a copy is not made lawful by being current on the day it is taken"*)
      and `:344-345` (*"Declaring the copy therefore makes it AUDITABLE and does
      not make it LAWFUL"*). Both are right as written under the reserved
      reading; editing them would be churn and would break the byte-faithfulness
      the rest of the block keeps.

## 3. Verification — DONE IN THIS PULL REQUEST

- [x] 3.1 `OPENSPEC_TELEMETRY=0 openspec validate
      amend-neutral-product-pin-interim-copy-vocabulary --strict` — PASSES.
- [x] 3.2 `OPENSPEC_TELEMETRY=0 openspec validate --all --strict` — the failure
      set is **EQUAL TO `main`'s** and no larger:
      `change/disposition-codexfactory-declared-renames`,
      `spec/neutral-product-pin`, `spec/repo-boundary-governance`. The
      `spec/neutral-product-pin` failure is `main`'s own and PRE-EXISTS this
      packet — `requirements.16.text`, on *A pinned artifact that resolves
      dependencies at install time carries a vendored lockfile…* at `:645`,
      whose first body line opens *"Where a pinned external neutral product is
      distributed…"* with no SHALL or MUST. **This block does not inherit it**
      (a different requirement, a different sentence) and **does not fix it**
      (`design.md` D6): fixing it would be a second amendment of ratified canon
      with no word behind it.
- [x] 3.3 `python3 scripts/proposal-support.py . verify
      amend-neutral-product-pin-interim-copy-vocabulary` — PASSES.
- [x] 3.4 `python3 scripts/validate-sequenced-after.py .` and `--ledger-diff` —
      PASS, with this change's ledger row seeded by the sanctioned tool
      (`--seed-ledger --moved-by '#<PR>'`) rather than hand-written. The row
      reads `declares: []` — the positive root claim — and `class:
      co-modifier`, which is NOT a contradiction of § 5.1: the ledger grades
      `class` over the WHOLE corpus, archived changes included, and this
      requirement's key is necessarily also written by the ARCHIVED
      `publish-openspec-cli-pin-as-contract-member`, the change that PROMOTED
      it. Seeding therefore also flips that archived partner's row from `sole`
      to `co-modifier`, which is the ledger's own documented partner-row
      behaviour and is the only other row this pull request moves. The
      ORDERING rule reads active writers only, and among those this change is
      SOLE.
- [x] 3.5 `python3 scripts/validate-scope-globs.py .` — PASSES.
- [x] 3.6 `python3 scripts/doc-health.py --single-repo .` — **no finding names
      this change.**
- [x] 3.7 `python3 -m pytest tests/sequenced_after tests/scope_globs
      tests/doc-health -q` — PASSES.

## 4. Archive — OWED, NOT GIVEN

- [ ] 4.1 **PROMOTE THE BLOCK AND ARCHIVE THE PACKET**, on Brett Heap's word and
      never on this lane's judgment, through `scripts/proposal-support.py`
      rather than through a bare `openspec` call. `code_surface: none`, so under
      `release-realization` the archive follows LANDING plus this task list and
      waits on no realization evidence. The promoted block must be
      **byte-identical** to the delta, which is the property the refusal on
      #780 was protecting when it declined to reword canon in an archive.
- [ ] 4.2 **CLOSE openxFactory issue #868 AT THE ARCHIVE, not at this landing.**
      The pull request body says `refs #868` and carries no closing keyword for
      exactly this reason.

## 5. Measured, and deliberately NOT taken here

- [x] 5.1 **THE SOLE-MODIFIER MEASUREMENT, taken before the claim** (2026-09-09,
      recorded on issue #868). `ls openspec/changes/*/specs/neutral-product-pin/`
      returns exactly one active delta, `split-opendox-two-layer-product`
      (ratified 2026-09-05, another lane's), which modifies *An external neutral
      product is pinned by commit and digest, never by tag* and *The consuming
      repository's pin is authoritative among reachable checkouts* — **neither
      of them this requirement**. No active change writes this requirement's
      key. `modified-block-currency`'s two-writers rule is scoped to two ACTIVE
      writers, so it does not reach the pair, **no ordering declaration is owed
      in either direction**, and
      `sequenced_after: []` is the positive root claim that follows. The two
      blocks share a spec FILE and no requirement key, which is not a collision.
      `gh pr list --state open --search "neutral-product-pin"` returned #865,
      #866 and #867, and `gh pr view --json files` on each showed none touches a
      `neutral-product-pin` path.
- [ ] 5.2 **THE `requirements.16` STRICT FAILURE IS A SUCCESSOR, NOT THIS
      PACKET.** *A pinned artifact that resolves dependencies at install time
      carries a vendored lockfile, and the install runs through it*
      (`:645`) fails `--strict` on `main` because its first body line carries no
      SHALL or MUST. It is one sentence's worth of amendment, on a DIFFERENT
      requirement from this one, and it is named here as available rather than
      taken: it needs its own issue and its own word. **This box is not ticked
      by this packet, and this packet does not owe it** — the successor is named
      so a later reader does not mistake the untouched failure for an oversight.
- [ ] 5.3 **ISSUE #775 IS A DIFFERENT DEFECT ON THE SAME REQUIREMENT** — the two
      sibling consumption pins (`contracts/openxwallet-pin.yaml`,
      `contracts/openreposhape-pin.yaml`) carry no `contracts/manifest.yaml`
      row. That is a live conformance defect fixed by REGISTERING rows, not by
      amending text, and this packet neither answers nor forecloses it.
- [ ] 5.4 **THE ESTATE'S ONE LIVE DECLARED COPY IS UNAFFECTED IN BOTH
      DIRECTIONS** — `xFactory-Hermes-Install` #72 → `06c9083d`, recorded by
      #780's archived `tasks.md` § 5.1 as still owing this requirement's third
      field, the per-file digest. It was not compliant before and is not
      compliant now; the owed digest stays owed. What changes is the word a
      record must use for it, and nothing already written is invalidated:
      #780's record calls the interim's digest *"owed rather than counted as
      met"*, which is correct under both vocabularies.
