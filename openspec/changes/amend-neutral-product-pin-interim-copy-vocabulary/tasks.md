# Tasks: amend-neutral-product-pin-interim-copy-vocabulary

Status: draft
Kind: tasks

`code_surface: none`, `target_release: none`. There is no realization group,
because there is nothing to realize: the delta is requirement prose, no script,
test, workflow, contract, schema or example reads the word it reserves, and
under `release-realization` an empty code surface archives ON LANDING plus this
task list rather than on merged-plus-green realization evidence. **The
"realization" of a wording amendment IS its promotion at archive.**

**NOTHING IS TICKED THAT DID NOT LAND.** Every ticked box below is a diff in
this pull request or a measurement recorded verbatim in its body. **§ 1
(ratification) IS ENTIRELY OPEN AND STAYS OPEN**: this packet is a DRAFT, no
word ratifies it, and no box in that section may be ticked by the lane that
authored it. § 4 (archive) is likewise open and is a separate act on Brett
Heap's word.

## 1. Ratification — OWED, NOT GIVEN

- [ ] 1.1 **RATIFY THE PACKET.** Brett Heap's word of 2026-09-09, verbatim
      *"R1 'lawful' amendment packet"*, commissioned this AUTHORING and is
      recorded as the packet's origin; it ratifies no wording and takes no
      design decision, so `.openspec.yaml` carries drafting provenance with **no
      approval pair** and every document carries `Status: draft`. On
      ratification: `proposal.md`, `design.md` and this file take `Status:
      ratified` with **ONE** citation line each (`Ratified:` in `proposal.md`'s
      front matter, `Ratified by:` here and in `design.md`), `.openspec.yaml`
      gains `approved_by`/`approved_on` **BESIDE** the drafting provenance with
      `kind` and `id` unmoved — the addition-not-rewrite shape
      `add-drafted-proposal-origin` (issue #318) defined for this transition and
      the shape the archive gate's origin-retention arm reads — and the act is
      recorded at `review/ratification-<YYYY-MM-DD>.md`.
- [ ] 1.2 **RULE `design.md` D1 — THE VETO POINT: TOLERATED against PERMITTED.**
      TOLERATED is recommended and written. PERMITTED is the alternative and is
      the word the refusal on PR #780 itself floated (*"say `PERMITTED as a
      declared interim` in the scenario"*), which is why it is put rather than
      simply passed over. D1 records three reasons for TOLERATED — PERMITTED is
      a near-synonym of LAWFUL and the defect is that two statuses shared one
      word; the admission is conditional and terminal and TOLERATED is the word
      for that; and PERMITTED is already spent one capability over
      (`domain-descendant-boundary:113`, *"the placement is permitted"*) on a
      non-deprecated state. **A veto costs four words** — two scenario bullets,
      the added body paragraph, the added scenario — plus the marker's reason
      sentence, and nothing else in the packet moves.
- [ ] 1.3 **RULE `design.md` D2 and D4 — the two additions.** D2 puts the
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
