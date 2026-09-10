# Tasks: amend-modified-block-currency-standing

Status: ratified
Ratified by: amend-modified-block-currency-standing — 2026-09-10, Brett Heap, "Ratify as encoded, all four sites" (record `review/ratification-2026-09-10.md`)
Kind: tasks

`code_surface: none`, `target_release: none`. There is no realization group,
because there is nothing to realize: the delta is requirement prose, the
severities and the resolution row it describes have been the module's real state
since 2026-08-31, and under `release-realization` an empty code surface archives
ON LANDING plus this task list rather than on merged-plus-green realization
evidence. **The "realization" of a wording amendment IS its promotion at
archive.**

**NOTHING IS TICKED THAT DID NOT LAND.** Every ticked box below is a diff in
this pull request or a measurement recorded verbatim in its body. **§ 1
(ratification) IS NOW TICKED AND NAMES THE WORD THAT TICKED IT** — Brett Heap's
*"Ratify as encoded, all four sites"* of 2026-09-10, which is his act and not
the authoring lane's; his earlier *"do 1, then 2"* stays recorded as the ORIGIN
of the authoring, which admitted no text to canon. **§ 5 (archive) STAYS
ENTIRELY OPEN**: promotion is a separate act on a separate word, so openxFactory
#857 and #858 close at the archive and not at this landing. § 6 records what was
measured and deliberately not taken, and stays open where the work is owed.

## 1. Ratification — GIVEN 2026-09-10

- [x] 1.1 **RATIFIED 2026-09-10 by Brett Heap** (openxFactory operator
      authority), verbatim *"Ratify as encoded, all four sites"*, given in
      session as a MULTIPLE-CHOICE ruling (~04:5xZ) and recorded on PR **#887**
      at 2026-09-10T11:35:59Z. The earlier word of 2026-09-10, verbatim *"do 1,
      then 2"*, stays recorded as the ORIGIN of the AUTHORING — it commissioned
      a packet against two named issues, decided no wording, and is not read as
      an approval. `proposal.md`, `design.md`, this file AND
      `review/ratification-2026-09-10.md` now carry `Status: ratified` with
      **ONE** citation line each (`Ratified:` in `proposal.md` and in the
      ratification record, `Ratified by:` here and in `design.md`), which is
      what `ratified-provenance` counts — one total across both sanctioned
      spellings, and now also under that family's SUBJECT arm, which since
      `804a9170` (#878) reads a `review/ratification-*` record whatever status
      it carries. `review/verification-2026-09-10.md` keeps `Status: record`:
      its subject is the GATE RUN and not the ratification, so the sibling
      scenario *A review record is not about a ratification* governs it.
      `.openspec.yaml` gains `approved_by`/`approved_on` **BESIDE** the
      drafting provenance, with `kind`, `id`, `reason` and `proposed_by`
      unmoved — the addition-not-rewrite shape `add-drafted-proposal-origin`
      (issue #318) defined for this transition and the shape the archive gate's
      origin-retention arm reads, which is why the status flip and the approval
      pair move in ONE commit. Records: `review/ratification-2026-09-10.md`,
      with the gate run captured beside it at
      `review/verification-2026-09-10.md`.
- [x] 1.2 **`design.md` D1 IS RULED — ALL FOUR SITES, NOT THE ONE PARAGRAPH
      #857 QUOTES.** The veto point was put and the recommendation was TAKEN,
      so **the encoded delta stands UNCHANGED and nothing is restored**: the
      five units retired at the four sites stay retired, the marker keeps its
      five names, and the added scenario stays. A veto would have removed three
      names from the marker, restored three canon units verbatim, deleted the
      added scenario, and left the first scenario asserting a `warning` the
      checker has not emitted since 2026-08-31 — a promoted requirement
      contradicting itself about a gate, and a third successor owed for the same
      flip. **IT DID NOT LAND**, and the alternative stays written out in
      `design.md` D1 as the record of what was put and declined.
- [x] 1.3 **`design.md` D0 STANDS AND D2–D7 WERE CARRIED — none was vetoed.**
      The ruling reached D1 and left the rest as designed, and the recording
      names them one by one: the arm-by-arm severity reading that corrects
      #857's own proposed wording STANDS (D0 — the title-resolution arm is
      `warning`, not `error`); the ledger sentence is carried unchanged (D3);
      the one added scenario stands, at the `(family, repository, path)` grain
      (D4); the marker's shape and the deliberate non-restatement of the
      predecessor's marker stand (D5); and #858's `specs/019` FR-018
      restatement rides this pull request as the severable commit `2f384fd1`
      rather than a second pull request (D6). D2 (the replacement wording
      copied from promoted canon) and D7 (what is measured and deliberately not
      taken) were carried beside them and neither was vetoed.

## 2. The delta — DONE IN THIS PULL REQUEST

- [x] 2.1 **ONE `## MODIFIED` REQUIREMENT, WRITTEN OVER CANON**, byte-faithful
      by CONSTRUCTION rather than by transcription: the block was generated by
      slicing `openspec/specs/doc-health/spec.md` lines 1588–2009 and applying
      each replacement as an exact single-occurrence substitution, so every unit
      not named below is canon's own bytes. Verified after the fact by the
      family's own derivation — 143 canon units, 5 uncarried, all 5 named by the
      marker and suppressed, 0 marker defects, 0 missing scenario titles.
- [x] 2.2 **FIVE UNITS RETIRED AND REPLACED IN PLACE**, at the four sites
      `design.md` D1 tabulates: the lifecycle-standing sentence carrying *"the
      arms below are advisory"*; the *advisory at launch* paragraph's first two
      sentences; and the first scenario's `THEN` and `AND` bullets. Each is
      REPLACED, none is dropped without replacement.
- [x] 2.3 **THE PARAGRAPH'S THIRD SENTENCE IS CARRIED UNCHANGED** — *"No flip is
      proposed for the carriage ledger in this change"* — because it is true
      (`design.md` D3). The `AMENDED BY` note records which change its *"this
      change"* names, rather than editing a true sentence.
- [x] 2.4 **THE REPLACEMENT WORDING IS COPIED FROM PROMOTED CANON** (`design.md`
      D2): the `promotion-fidelity` and `duplicate-packet` post-flip paragraphs
      at `openspec/specs/doc-health/spec.md:1080-1100` and `:1233-1254`, and
      their scenarios' three bullets, with the one structural difference the
      facts force — this family is enforcing in ONE arm and advisory in the
      rest, so the standing paragraph is arm-by-arm.
- [x] 2.5 **ONE SCENARIO ADDED, AT THE END OF THE BLOCK** (`design.md` D4), for
      the reach of the resolution row across every class the family emits —
      written at the `(family, repository, path)` grain the uncited-resolution
      rule keys on, and carrying the negative case in its own bullet, so canon
      promises only the disappearance the checker detects (bench round 1, PR
      #887 thread T2).
- [x] 2.6 **ONE `Removed from canon` MARKER, FIVE NAMES, NO CODE SPAN IN ITS
      REASON** (`design.md` D5), and `amend-marker-defect-reporting`'s own
      marker deliberately NOT restated, on this requirement's rule that a marker
      is not a carriage unit in either direction.
- [x] 2.7 **THE `AMENDED BY` NOTE STATES THE WHOLE ACCOUNTING** — what moved,
      what did not, that no severity moves and no row is added, and why the
      predecessor's marker is absent.
- [x] 2.8 **README `## OpenSpec Records` CARRIES THE ACTIVE ROW**, in house
      style, naming the veto point and the draft standing.
- [x] 2.9 **THE PER-CHANGE SWEEP LEDGER ROW IS SEEDED BY THE SANCTIONED TOOL**,
      never hand-written: `python3 scripts/validate-sequenced-after.py .
      --seed-ledger --moved-by '#<PR>'`.

## 3. openxFactory #858 — `specs/019` FR-018, DONE IN THIS PULL REQUEST

- [x] 3.1 **FR-018 RESTATED TO CANON'S THREE GROUNDS**, quoting the promoted
      sentence byte-exactly with its line range and adding the narrow-reading
      clause beside it, in the form PR #827 established for the predecessor's
      identical residue (#730): a dated amendment note — *"(Amended 2026-09-10
      to match canon after `amend-marker-defect-reporting` (#850); this bullet
      previously stated the ONE-ground rule ...)"* — and nothing else in the
      file changed.
- [x] 3.2 **THE QUOTE IS VERIFIED BYTE-EXACT** against
      `openspec/specs/doc-health/spec.md:1744-1751` after whitespace
      normalization, the terminal period included — the exact nit a review
      raised on PR #827.
- [x] 3.3 **ASSUMPTION A1 CHECKED AND LEFT ALONE**, as issue #858 asks. A1
      (`specs/019-modified-block-currency-family/spec.md:606`) states that a
      marker's REASON is optional and was already restated to the amended
      reason-boundary rule by PR #827. The three grounds do not touch it.
- [x] 3.4 **THE COMMIT IS SEVERABLE AND IS RECORDED AS SUCH** (`design.md` D6):
      it depends on no part of this delta, catches up with canon promoted at
      `250d93d7`, and can be cherry-picked and landed alone if this packet's
      ratification is delayed or its delta vetoed.

## 4. Verification — DONE IN THIS PULL REQUEST

- [x] 4.1 `OPENSPEC_TELEMETRY=0 openspec validate
      amend-modified-block-currency-standing --strict` — PASSES.
- [x] 4.2 `OPENSPEC_TELEMETRY=0 openspec validate --all --strict` — the failure
      set is byte-identical to `main`'s: this change appears in NEITHER, and no
      pre-existing failure is added, removed or changed by it.
- [x] 4.3 `python3 scripts/proposal-support.py . verify
      amend-modified-block-currency-standing` — PASSES.
- [x] 4.4 `python3 scripts/validate-sequenced-after.py .` and `--ledger-diff` —
      both PASS, the ledger clean after the seed.
- [x] 4.5 `python3 scripts/validate-scope-globs.py .` — PASSES.
- [x] 4.6 `python3 scripts/doc-health.py --single-repo .` — **NO finding names
      this change**, and the modified-block-currency family reports NOTHING on
      this block: the arm that would have caught a stale restatement is the one
      this packet is written under, and it is silent because the block carries
      canon and declares its five removals.
- [x] 4.7 `python3 -m pytest tests/sequenced_after tests/scope_globs
      tests/doc-health -q` — PASSES.
- [x] 4.8 **EVERY GATE RE-RUN IN FULL ON THE RATIFIED TREE**, 2026-09-10, after
      the ratification encode — capture at `review/verification-2026-09-10.md`.
      `--all --strict` is measured there against an `origin/main` `804a9170`
      control run in a separate worktree, and `doc-health`'s finding-line diff
      against the PRE-RATIFICATION tree `ab8247fa` is recorded beside it.
- [x] 4.9 **AND RE-RUN A SECOND TIME AFTER THE MERGE FROM `main`**, because
      `origin/main` moved `804a9170` → `b91af6ea` while the encode was being
      verified and the pull request went CONFLICTING on the README
      `## OpenSpec Records` block. The merge is `2e84325a` and it moves NO byte
      of this packet; the second capture is
      `review/verification-2026-09-10-post-merge.md`, **at its own path because
      a dated run report is a one-shot `record` and a second run of such a
      generator writes a different path rather than rewriting the first** — the
      2026-09-10 capture is preserved unedited, keeps `Status: record`, and is
      NOT superseded. The re-measure was not a formality: `b91af6ea` brought
      #890's `ratified-provenance` SUBJECT arm (#878), which the first capture's
      tree did not have, plus #886's rewritten `scripts/proposal-support.py`,
      `scripts/sequenced_after.py` and `scripts/frontmatter_strict.py`. Every
      gate is green on the merged tree, the `--all --strict` failure set is
      still IDENTICAL to `main`'s, and `doc-health`'s finding-line diff against
      the DRAFT packet on the SAME `main` is IDENTICAL at 98 lines — this
      packet's ratification record clearing the new subject arm that
      twenty-one other records fail.

## 5. Archive — OWED, NOT GIVEN

- [ ] 5.1 **PROMOTE THE BLOCK AND ARCHIVE THE PACKET**, on Brett Heap's word and
      through `scripts/proposal-support.py` rather than a bare `openspec`
      command. Under `release-realization` an empty code surface archives on
      landing plus this task list; that archive is NOT performed at this
      landing, and nothing under `openspec/specs/` is edited by it.
- [ ] 5.2 **CLOSE openxFactory #857 AND #858 AT THE ARCHIVE**, not at this
      landing. The pull request body carries `refs`, never a closing keyword,
      for exactly that reason.
- [ ] 5.3 **THE PER-CLASS DISAPPEARANCE GAP IS NAMED AS RESIDUE AND IS
      DELIBERATELY NOT TAKEN HERE.** `report.uncited_resolutions` keys a
      resolution on `(family, repository, path)` — `Finding.match_key()`,
      `scripts/doc_health/__init__.py:187` — and skips a prior contested key
      whenever ANY current finding carries it, so a finding of ONE class of this
      family that stops being reported while another finding of the family is
      still emitted at that path owes no citation and raises nothing. That is the
      SHIPPED behaviour and promoted canon already records it — *A
      modified-block-currency finding its own class map cannot place is itself a
      finding*, `openspec/specs/doc-health/spec.md:2334-2341`, and its scenario at
      `:2379` — so the delta's standing paragraph and its added scenario are
      written to it rather than past it (bench round 1, PR #887 thread T2).
      **WHETHER THE CHECKER SHOULD TRACK DISAPPEARANCE AT FINDING-CLASS GRAIN IS
      A CODE DECISION, NOT A WORDING ONE**: it would move `match_key`, the
      ranked-plan grammar `parse_previous` reads and writes, and every family
      keyed on it, and this packet is `code_surface: none` by measurement. It is
      REFUSED as a widening and owed as a successor. **THE BOX TICKS ON THE
      RECORDING** (ruling of 2026-09-06T23:10Z): at the archive act it ticks by
      NAMING a filed successor issue, or by the owner's word that the grain is
      correct as it stands and nothing is owed. It is NOT ticked here.

## 6. Measured, and deliberately NOT taken here

- [ ] 6.1 **`specs/019` FR-024 AND FR-026 STILL STATE THE LAUNCH SEVERITIES AND
      THE FAMILY'S ABSENCE FROM `FAMILY_RESOLUTION`, AND ARE NOT EDITED**
      (`design.md` D7). Unlike FR-018 they FORESEE the flip in their own words —
      FR-024 asks for the arm's severity to be a distinct constant *"so that the
      later flip ... is one line beside one row"*, and the feature's
      out-of-scope list at `:679` names *"any flip of severity or
      `FAMILY_RESOLUTION` membership (packet § 7.2 — a later ruling)"* — so they
      read as a record of what was built rather than as a statement of current
      behaviour. This is residue of the FLIP (#357), not of either issue this
      packet takes. **THE BOX TICKS ON THE RECORDING**, per the ruling of
      2026-09-06T23:10Z (*"Tick on the recording"*): at the archive act it ticks
      by NAMING a filed successor issue, or by the owner's word that a build
      record needs no annotation. It is NOT ticked here and the work is not
      done.
- [ ] 6.2 **NO FLIP OF ANY REMAINING ARM IS PROPOSED.** The title-resolution and
      ordering arm keeps `warning`, the drift, pairing and collision classes
      keep `warning`, and the carriage ledger keeps `info`. A later flip of any
      of them is one ruling after a measurement, exactly as the delta's sequence
      paragraph keeps in force. The box ticks at the archive act, on the
      recording, if a successor is ever named; nothing is owed by this packet.
- [x] 6.3 **THE SOLE-ACTIVE-MODIFIER MEASUREMENT, TAKEN BEFORE THE CLAIM**
      (2026-09-10, over every active `openspec/changes/*/specs/*/spec.md`): two
      other active changes carry a `doc-health` delta —
      `add-nightly-dashboard-refresh` (`## ADDED` only, seven refresh-lane
      requirements) and `settle-aging-staging-topics` (`## MODIFIED` over *Aging
      threshold defaults*) — and NEITHER writes this requirement's key. The
      two-writers rule stated inside the very requirement being modified is
      scoped to two ACTIVE writers, so it does not reach this pair and no
      ordering declaration is owed in either direction. `sequenced_after: []` is
      the positive root claim that follows.
- [x] 6.4 **THE SIX SEVERITY CONSTANTS AND THE RESOLUTION ROW WERE READ OUT OF
      THE MODULE BEFORE ANY WORDING WAS WRITTEN** (`design.md` D0), which is
      what caught the error in issue #857's own proposed remedy: the
      title-resolution arm is `warning`, not `error`, and was deliberately not
      dragged by the flip.
