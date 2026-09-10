# Tasks: amend-neutral-product-pin-lockfile-first-line

Status: draft
Kind: tasks

`code_surface: none`, `target_release: none`. There is no realization group,
because there is nothing to realize: the delta is requirement prose, no script,
test, workflow, contract, schema or example quotes any part of the sentence it
re-orders, and under `release-realization` an empty code surface archives ON
LANDING plus this task list rather than on merged-plus-green realization
evidence. **The "realization" of a wording amendment IS its promotion at
archive.**

**NOTHING IS TICKED THAT DID NOT LAND.** Every ticked box below is a diff in
this pull request or a measurement recorded verbatim in its body, with the
command and the exit code. **§ 1 (ratification) IS ENTIRELY OPEN**: Brett
Heap's word of 2026-09-10, verbatim *"do 882 packet"*, commissioned the
AUTHORING and ratified no wording — so every document in this packet reads
`Status: draft`, `.openspec.yaml` carries drafting provenance with NO
`approved_by` and NO `approved_on`, and nothing here is admitted to canon.
**§ 5 (archive) IS ENTIRELY OPEN**: promotion is a separate act on a separate
word, so openxFactory #882 closes AT THE ARCHIVE and not at this landing, and
`Closes #882` appears on the archive pull request and on nothing else. § 6
records what was measured and deliberately not taken.

**AND THE ORDER OF THE DECISIONS IS NOT THE ORDER OF THE SECTIONS.**
`design.md` **D6 is put FIRST** and it can end the packet: the failure this
amendment answers is REAL on the OpenSpec CLI at 1.2.0 and is reported by NO
REQUIRED CHECK, because openxFactory validates through the pinned 1.12.0
artifact and this specification PASSES there. Whether promoted canon should be
amended for a binary no required check runs is the owner's call, and § 1.2
is the box that records it.

## 1. Ratification — OWED, NOT GIVEN

- [ ] 1.1 **RATIFY OR REFUSE THE PACKET, on Brett Heap's word** (openxFactory
      operator authority). The word behind this authoring — 2026-09-10,
      verbatim *"do 882 packet"*, recorded in this lane's CLAIMED comment on
      openxFactory [#882](https://github.com/opensoft/openxFactory/issues/882#issuecomment-5623510674)
      at 2026-09-10T18:29:31Z — commissioned a lane to write the remedy issue
      #882 proposes. **IT DECIDES NO WORDING AND IS NOT READ AS AN APPROVAL.**
      On ratification, and only then: `proposal.md`, `design.md` and this file
      go `Status: ratified` with **ONE** citation line each (`Ratified:` in
      `proposal.md`, `Ratified by:` here and in `design.md`), which is what
      `ratified-provenance` counts; `.openspec.yaml` GAINS
      `approved_by`/`approved_on` **BESIDE** the drafting provenance with
      `kind`, `id`, `reason` and `proposed_by` unmoved — the
      addition-not-rewrite shape `add-drafted-proposal-origin` (issue #318)
      defined for this transition and the shape the archive gate's
      origin-retention arm reads; and a `review/ratification-<date>.md` record
      carries `Status: ratified` with its own citation, while any gate capture
      beside it stays `Status: record` because its subject is the RUN and not
      the ratification.
- [ ] 1.2 **RULE `design.md` D6 FIRST — AMEND, OR CLOSE #882 ON THE
      MEASUREMENT.** This is put before the wording because it can end the
      packet. The failure is real on the 1.2.0 binary on PATH
      (`✗ [ERROR] requirements.16.text: Requirement must contain SHALL or MUST
      keyword`, exit 1) and ABSENT from the pinned 1.12.0 the required gate
      runs (exit 0, `spec/neutral-product-pin` among the passes). D6
      recommends AMENDING ANYWAY on three grounds that are not the red gate —
      seventeen-to-one convention inside this one file, an unfinished 1.12
      migration in which every engineer and agent who types the command this
      repository's own notes tell them to type meets a red specification, and a
      cost of two case flips and one comma — and writes the alternative out
      beside it: publish the two runs, leave ratified text alone, close #882
      with the measurement. **A veto here withdraws the packet rather than
      re-wiring it.**
- [ ] 1.3 **RULE `design.md` D1 — THE WORDING, three options, one encoded.**
      Option 1 (RECOMMENDED and written) re-orders canon's own words so the
      subject and the modal open the sentence: *"The pin SHALL carry a VENDORED
      RESOLUTION where a pinned external neutral product is distributed as a
      published artifact whose installation RESOLVES dependency ranges — …"*,
      adding no word and removing none. Option 2 changes NOT ONE WORD and moves
      only the line breaks, which owes no marker at all — proven, not argued —
      and rests the requirement's compliance on a line break in a corpus whose
      one checker is contractually blind to line breaks. Option 3 is the wording
      issue #882 itself floats, and it is REFUSED because it moves the
      obligation's bearer from the pin to the product, which four sites this
      packet does not touch contradict. A veto to option 2 replaces the block
      with the re-flow-only block, DELETES the marker and re-runs the gates; a
      veto to option 3 is a larger amendment than this word commissions, because
      the honest form of it also re-words the heading and those four sites.
- [ ] 1.4 **RULE `design.md` D2 — the marker.** ONE `Removed from canon`
      marker, ONE name, no code span in its reason, is owed under option 1 and
      is written; under option 2 NONE is owed. Both branches are proven with the
      family's own `derive_units` in § 3.3, so the decision is read off a
      measurement rather than argued. D3 (why an OpenSpec change and not a
      patch), D4 (`code_surface: none`) and D5 (sequencing) are carried beside
      them and are separately vetoable; D7 records what is deliberately not
      taken.

## 2. The measurement — TAKEN BEFORE THE DESIGN, DONE IN THIS PULL REQUEST

- [x] 2.1 **THE CORPUS WAS MEASURED, NOT SAMPLED.** Across all **62** promoted
      spec files under `openspec/specs/` and all **641** `### Requirement:`
      headings in them, **exactly 2** have a first body line carrying neither
      `SHALL` nor `MUST`: `openspec/specs/neutral-product-pin/spec.md` index
      **16** (heading `:668`, body `:669`) and
      `openspec/specs/repo-boundary-governance/spec.md` index **1** (heading
      `:34`, body `:35`, a list of repository names in code spans). The second
      is NOT taken here and is named as residue in § 6.1.
- [x] 2.2 **SEVENTEEN TO ONE INSIDE THIS ONE FILE.** `neutral-product-pin`
      carries **18** requirements; **17** open their body with `SHALL` or
      `MUST` on line one — **10** of them inside 80 characters and **7** on a
      line of 80 characters or more (80, 156, 183, 201, 221, 284 and 397
      characters), so a long first line is house style here too and is not a
      style objection to `design.md` D1's option 2. Index 16 is the only one
      that opens with a condition.
- [x] 2.3 **THE REQUIREMENT IS NOT SHORT OF OBLIGATION**, which is why this is
      an amendment of EXPRESSION and not of rule: `SHALL` occurs **8** times in
      the block, all 8 of them BELOW `:669`, the first at `:670`.
- [x] 2.4 **THE ISSUE'S OWN SCENARIO COUNT IS CORRECTED ON THE MEASUREMENT**
      (`design.md` D0a). Issue #882 says *"all nine scenarios and both trailing
      body paragraphs unchanged"*. The requirement carries **FOUR** scenarios —
      *A pinned artifact declares dependency ranges*, *The committed resolution
      and the pin disagree*, *The install re-resolves a range*, *A reuse cache
      serves a tree it was not built for* — and two trailing body paragraphs,
      which is right. The correction is recorded here and in `design.md` rather
      than by editing the issue's prose, and it changes nothing about the
      remedy: all four are carried, byte for byte.
- [x] 2.5 **BOTH BINARIES WERE MEASURED, ON TWO TREES, AND THE PINNED ONE DOES
      NOT REPORT THIS AT ALL** (`design.md` D6). `contracts/openspec-cli-pin.yaml:255`
      pins `version: "1.12.0"`; `.github/workflows/openspec-cli-pin-gate.yml`
      runs `python3 scripts/validate-openspec-cli-pin.py --all --no-cache`
      through the content-verified artifact; and on that binary this
      specification PASSES. The four runs and their exit codes are in § 4.
- [x] 2.6 **THE MECHANISM WAS MEASURED ON A CONTROLLED FIXTURE RATHER THAN
      INFERRED.** A three-requirement probe specification — keyword on line
      one, keyword on line TWO only, no keyword anywhere — was validated by
      both binaries. 1.2.0 errors on the second and the third
      (`requirements.1.text`, `requirements.2.text`); 1.12.0 says NOTHING about
      the second and emits a WARNING on the third
      (*"should contain SHALL or MUST (RFC 2119 best practice for English
      specs)"*). D6 also records the one thing the table would hide: on 1.12.0
      the probe SPEC is still reported invalid, on the warning — so 1.12.0 is
      not indifferent to a missing keyword, only to a keyword on line two.
- [x] 2.7 **`kind: ad_hoc` WAS CHECKED RATHER THAN ASSUMED.**
      `ideation/staging/` was enumerated (**30** topic folders) and `INDEX.md`
      read: no topic folder and no INDEX row names the vendored lockfile, this
      requirement, the first-body-line shape or the strict keyword rule, and
      `grep -rliE "vendored lockfile|first body line|SHALL or MUST"
      ideation/staging/` returns nothing (exit 1). `kind: staged` would claim a
      staging source that does not resolve. The organized source is issue #882
      and the two passages of its predecessor's packet that named it.

## 3. The delta — DONE IN THIS PULL REQUEST

- [x] 3.1 **ONE `## MODIFIED` REQUIREMENT, WRITTEN OVER CANON, BYTE-FAITHFUL BY
      CONSTRUCTION RATHER THAN BY TRANSCRIPTION** — the method
      `amend-modified-block-currency-standing`'s `tasks.md` § 2.1 established.
      The block was generated by SLICING
      `openspec/specs/neutral-product-pin/spec.md` lines **668–721** (the
      `### Requirement:` heading at `:668` through `:721`, the last non-blank
      line before the next heading at `:723` — 54 lines, sha256
      `a33ceb1087095040e56f5e9e3c7e912b55c99bba0aa0af87cb8e7de10eec58f7`, 4,319
      bytes), applying the ONE change as an exact SINGLE-OCCURRENCE
      substitution over the first sentence — **the generator refuses on any
      other occurrence count**, and it asserts that the paragraph's text
      OUTSIDE the substituted sentence is identical on both sides — and
      re-wrapping ONLY the paragraph that substitution touched, at the file's
      own width of 79.
- [x] 3.2 **THE GENERATOR'S OUTPUT AND THE COMMITTED BLOCK ARE ONE STRING**:
      55 lines, sha256
      `bb8a1937c8bc26d41ebf91a50cde7881f2ca07ec15684cd0a27590ac242c1740`, 4,318
      bytes, on both sides. The requirement HEADING is byte-identical, and the
      38 lines from `:684` to `:721` — the second and third body paragraphs,
      all four scenario headings and all twelve scenario bullets — are canon's
      own bytes, compared line by line and asserted.
- [x] 3.3 **THE ACCOUNTING IS DERIVED BY THE FAMILY'S OWN CODE, AND BOTH
      BRANCHES OF THE MARKER DECISION ARE PROVEN.**
      `scripts/doc_health/modified_block_currency.py`'s `derive_units` over
      canon's requirement returns **25 units** — 9 body, 4 scenario titles, 12
      scenario bullets — and over this block **25 units** in the same
      three-way split. `carried()` reports **1 uncarried** canon unit (the
      retired first sentence) and **1 added** block unit (its replacement);
      `suppression()` reports **1 suppressed** and **0 marker defects**, so the
      ledger arm's undeclared-unit set is **EMPTY**. The four canon scenario
      titles are carried in canon's order and the block adds none.
      **COUNTERFACTUAL, GENERATED ON THE SAME TREE:** a block that moves only
      the LINE BREAKS returns **25 units, 0 uncarried, 0 added** — canon's own
      normalization rule (*"a re-wrapped paragraph compares equal to the same
      paragraph wrapped differently"*, `openspec/specs/doc-health/spec.md:1668-1672`)
      means the family sees no change at all, so **option 2 would owe no marker
      and none would be written**. This block changes the sentence's WORD ORDER,
      so the sentence is a REPLACED unit, one marker is owed, and one is
      written.
- [x] 3.4 **NOT ONE WORD ADDED AND NOT ONE WORD REMOVED**, measured
      whitespace-split and CASE-SENSITIVE rather than described: the retired
      sentence's 61 tokens minus the new sentence's 61 are `Where`, `ranges,`
      and `the`; the new sentence's minus the retired one's are `The`, `where`
      and `ranges`. **Two case flips and one comma.** Casefolded, the two
      multisets differ by `ranges,` against `ranges` and by nothing else. 374
      characters become 373.
- [x] 3.5 **THE OBLIGATION LANDS ON LINE ONE, WHICH IS THE WHOLE POINT.** The
      block's first body line is `The pin SHALL carry a VENDORED RESOLUTION
      where a pinned external neutral` — 73 characters, `SHALL` at word four.
      Canon's is `Where a pinned external neutral product is distributed as a
      published artifact` — 78 characters, no keyword.
- [x] 3.6 **ONE `Removed from canon` MARKER, ONE NAME, NO CODE SPAN IN ITS
      REASON**, placed at the END of the block and ASSEMBLED FROM
      `derive_units`' OWN OUTPUT rather than retyped — the method PR #908's
      packet used, so the marker cannot name a fragment or a unit as its author
      remembers it. Re-parsed by `parse_marker` on the committed file it yields
      form `removed`, change id `amend-neutral-product-pin-lockfile-first-line`,
      date `2026-09-10`, **exactly one name equal to the single uncarried canon
      unit**, an **EMPTY `quoted` list**, no destination, and a 1,167-character
      reason carrying **0 code spans** — so neither the existing second
      marker-defect ground nor either ground the ACTIVE draft
      `amend-marker-declaring-nothing` (PR #908) adds can fire on it. That is
      checked against the draft as well as against promoted canon, because that
      packet may land first.
- [x] 3.7 **NOTHING UNDER `openspec/specs/` IS EDITED BY THIS PULL REQUEST**,
      and no script, test, contract, schema, workflow or example is touched
      either. The promoted specification still states the sentence as ratified;
      the ARCHIVE act is what would write this block into it.
- [x] 3.8 **README `## OpenSpec Records` CARRIES THE ACTIVE ROW**, in house
      style, at the head of the active list: authored 2026-09-10,
      **`Status: draft`** (NOT RATIFIED), lane `openxfactory-1`, naming the
      origin issue, the two-question veto shape (D6 before D1), the accounting,
      the marker decision and what the pull request does not do.
- [x] 3.9 **THE PER-CHANGE SWEEP LEDGER ROW IS SEEDED BY THE SANCTIONED TOOL**,
      never hand-written: `python3 scripts/validate-sequenced-after.py .
      --seed-ledger --moved-by '#<PR>'`. The row reads `declares: []` — the
      positive root claim — and `class: co-modifier`, which is NOT a
      contradiction of § 4.5: the ledger grades `class` over the WHOLE corpus,
      archived changes included, and this requirement's key is necessarily also
      written by the ARCHIVED `pin-openspec-cli-dependency-closure`, the change
      that PROMOTED it. Seeding therefore also flips that archived partner's row
      from `sole` to `co-modifier` — the ledger's own documented partner-row
      behaviour, and the only other row this pull request moves.

## 4. Gates — RUN IN FULL, WITH EXIT CODES, ON THIS PULL REQUEST'S TREE

**EVERY FIGURE BELOW IS A RUN, NOT A RECOLLECTION**, and where a figure only
means something against `main` the CONTROL is a second worktree at
`origin/main` `ea34f22a` rather than a remembered number.

- [x] 4.1 `OPENSPEC_TELEMETRY=0 openspec validate
      amend-neutral-product-pin-lockfile-first-line --strict` — **`Change
      'amend-neutral-product-pin-lockfile-first-line' is valid`, exit 0.**
- [x] 4.2 `OPENSPEC_TELEMETRY=0 openspec validate --all --strict` (1.2.0 on
      `PATH`) — **exit 1** on both trees, and **THE FAILURE SET IS
      IDENTICAL**: `change/disposition-codexfactory-declared-renames`,
      `change/disposition-codexfactory-floor-relocation-retitle`,
      `spec/neutral-product-pin`, `spec/repo-boundary-governance`. `diff` over
      the sorted `✗` lines of the two runs is EMPTY. Totals move by exactly one
      PASSING item — this packet's own change: control `96 passed, 4 failed
      (100 items)`, this branch `97 passed, 4 failed (101 items)`, with
      `✓ change/amend-neutral-product-pin-lockfile-first-line` in the branch
      run. **`spec/neutral-product-pin` STILL FAILS AND THAT IS CORRECT**: a
      delta does not edit the promoted specification, so the failure this
      packet answers is still there at this head. **THE ARCHIVE ACT IS WHAT
      CLEARS IT**, and the archive is § 5.
- [x] 4.3 `python3 scripts/validate-openspec-cli-pin.py --all --strict` (the
      pinned 1.12.0, content-verified) — **exit 0** on both trees: control
      `Totals: 98 passed, 2 failed (100 items)`, this branch `Totals: 99
      passed, 2 failed (101 items)`. The two failures are the two DISPOSITIONED
      scenario-omission findings accepted on Brett Heap's word of 2026-09-05
      *"take exit 2"* (`add-chain-attestation` / `signed-execution-chain`,
      `add-composed-view-authoring` / `ideation-dashboard`), and
      `spec/neutral-product-pin` carries INFO notes only. The run reports
      `@fission-ai/openspec@1.12.0 verified against its content address` and
      the 80-package dependency closure installed with `npm ci
      --ignore-scripts`.
- [x] 4.4 `python3 scripts/proposal-support.py . verify
      amend-neutral-product-pin-lockfile-first-line` — **`proposal support
      verification ok`, exit 0.**
- [x] 4.5 `python3 scripts/validate-sequenced-after.py .` — **exit 0**:
      `sequenced_after validation passed (39 active changes, 9 declaring the
      field)`, plus both archive-date arms passing. And
      `python3 scripts/validate-sequenced-after.py . --ledger-diff` — **exit
      0** after § 3.9's seed. **BEFORE the seed it exited 1 and named exactly
      what the seed then moved**, which is recorded rather than hidden:
      `missing row: amend-neutral-product-pin-lockfile-first-line`, `stale row:
      pin-openspec-cli-dependency-closure: class: ledger 'sole', live
      'co-modifier'`, and eight derived-total mismatches — the archived
      promoter's flip that § 3.9 predicts, observed.
- [x] 4.6 `python3 scripts/validate-scope-globs.py .` — **`scope_globs
      validation passed (all active changes conform).`, exit 0.**
- [x] 4.7 `python3 scripts/doc-health.py --single-repo .` — **exit 1** on both
      trees (its ordinary state on this corpus, which reports findings rather
      than gating on zero), `Findings: 32 critical, 5 error, 47 warning, 16
      info. New regressions vs previous report: 0` on BOTH, canon share 39.7%
      on BOTH — and **NO FINDING NAMES THIS CHANGE** (`grep -c
      amend-neutral-product-pin-lockfile-first-line` over the report = **0**).
      The finding-line diff between the control tree and this branch is
      **EMPTY**: 100 findings each, byte-identical once the repository label is
      normalized. In particular the `modified-block-currency` family — which
      reads every active block by construction and reports nine other active
      changes in this same run — reports NOTHING about this block, which is the
      marker working in the real gate rather than only in § 3.3's derivation.
- [x] 4.8 `python3 -m pytest tests/sequenced_after tests/scope_globs
      tests/proposal-support -q` — **PASSES, exit 0.** Before § 3.9's seed the
      same command exited 1 with exactly four failures, all four the ledger's
      staleness and none of them about this packet's content
      (`test_the_LIVE_corpus_and_the_LEDGER_agree_row_by_row`,
      `test_every_corpus_change_has_EXACTLY_ONE_row_and_every_row_a_change`,
      `test_the_totals_DERIVED_FROM_THE_LEDGER_equal_the_MEASURED_sweep`,
      `test_the_live_ledger_reports_the_SAME_totals_the_sweep_MEASURES`); the
      seed cleared all four.

## 5. Archive — OWED, NOT GIVEN

**THIS SECTION IS OPEN BY DESIGN AND STAYS OPEN THROUGH THIS LANDING.**
`code_surface: none` means the packet archives ON LANDING plus this task list
under `release-realization` rather than on merged-plus-green realization
evidence — but the archive is a SEPARATE ACT ON A SEPARATE WORD, and that word
has not been given. **AND THE SANCTIONED ARCHIVE PATH REFUSES AN OPEN BOX**,
with no bypass flag: `scripts/proposal-support.py` refuses any change whose
`tasks.md` still matches `^- \[ \]` (*"change has incomplete tasks"*), which is
why every box in this file must be ticked in the commit BEFORE the move rather
than after it.

- [ ] 5.1 **PROMOTE THE BLOCK AND ARCHIVE THE PACKET**, on Brett Heap's word
      and never on this lane's judgment, through `python3
      scripts/proposal-support.py . archive
      amend-neutral-product-pin-lockfile-first-line --date <YYYY-MM-DD> --yes`
      and never a bare `openspec archive`. The promoted block must be
      **BYTE-IDENTICAL** to the delta, measured and recorded in the archive
      pull request's body rather than asserted — the property the refusal on
      PR #780 was protecting when it declined to reword canon in an archive.
      **AND THE ARCHIVE IS WHAT CLEARS § 4.2's `spec/neutral-product-pin`
      FAILURE ON THE 1.2.0 BINARY**, which is the one gate figure this packet
      changes and it changes it THERE and not here.
- [ ] 5.2 **CLOSE openxFactory issue #882 AT THE ARCHIVE, not at this
      landing.** This pull request's body says `refs #882` and carries **no
      closing keyword**, and no commit message on this branch carries one
      either, so `closingIssuesReferences` on this pull request is `[]` —
      verified through GraphQL and recorded in the body. `Closes #882` belongs
      on the archive pull request and on nothing else.

## 6. Measured, and deliberately NOT taken here

- [ ] 6.1 **THE CORPUS'S ONE OTHER FIRST-LINE INSTANCE IS NAMED AS RESIDUE AND
      IS NOT TAKEN.** `openspec/specs/repo-boundary-governance/spec.md:34`
      (*Install repository scope*), whose first body line `:35` is a list of
      repository names in code spans, fails the 1.2.0 check on the identical
      ground (`requirements.1.text`) and appears in § 4.2's failure set on BOTH
      trees as `spec/repo-boundary-governance`. It is the ONLY other instance —
      measured across 62 files and 641 requirements (§ 2.1) — and it is a
      different capability, a different requirement and a different sentence.
      Taking it here would be a second amendment of ratified canon with no word
      behind it, which is precisely the act the refusal on PR #780 refused.
      **THIS BOX IS OPEN BECAUSE NO SUCCESSOR IS NAMED YET**: under the ruling
      of 2026-09-06T23:10Z, verbatim *"Tick on the recording"*, an owed
      successor's box ticks once the successor is NAMED, and naming it means
      filing its issue — which is not this lane's act on this word. A search of
      `gh issue list --state all` before this box was written found no open
      issue reporting that requirement's first-line shape.
- [x] 6.2 **THE REQUIREMENT'S HEADING IS NOT EDITED, AND THE LOOSENESS IN IT IS
      RECORDED RATHER THAN FIXED** (`design.md` D7). *"A pinned artifact …
      carries a vendored lockfile"* attributes the carrying to the ARTIFACT
      where the body attributes it to the PIN. Editing a ratified heading
      changes the requirement KEY every consumer, marker and currency check
      matches on, which is a far larger act than this word commissions. This
      box is a MEASUREMENT and ticks on the measurement being taken and
      recorded.
- [x] 6.3 **`prepare-openspec-1-12-readiness` IS OFFERED THE FIXTURE
      MEASUREMENT AND IS NOT AMENDED BY IT.** § 2.6's controlled two-binary
      probe is directly relevant to that ACTIVE change's subject — it records a
      real behaviour difference between 1.2.0 and 1.12.0 that the readiness
      evidence does not name — and it is offered to that change rather than
      folded into this one. This packet writes no readiness evidence, edits
      nothing of that change, and claims no part of that migration.
- [x] 6.4 **THE TWO DISPOSITIONED FINDINGS ARE UNTOUCHED.** The pinned run in
      § 4.3 names two accepted exceptions (`add-chain-attestation` /
      `signed-execution-chain`, `add-composed-view-authoring` /
      `ideation-dashboard`), granted on Brett Heap's word of 2026-09-05
      *"take exit 2"*. Neither is related to this requirement, no entry of
      `contracts/openspec-cli-pin.yaml` moves, and this packet neither renews
      nor retires either one.
- [x] 6.5 **THE SIBLING SEARCH WAS TAKEN BEFORE THE CLAIM AND RE-TAKEN AT THE
      BRANCH CUT** (`design.md` D5). `ls -d openspec/changes/*/specs/neutral-product-pin`
      returns this change and exactly one other active delta,
      `split-opendox-two-layer-product` (ratified 2026-09-05, another lane's),
      which modifies *An external neutral product is pinned by commit and
      digest, never by tag* (`:86`) and *The consuming repository's pin is
      authoritative among reachable checkouts* (`:186`) — **neither of them
      this requirement**. `grep -rln "A pinned artifact that resolves
      dependencies at install time" openspec/changes/ --include=spec.md`
      excluding `archive/` returns THIS CHANGE AND NOTHING ELSE. All **nine**
      pull requests open at the branch cut — #917, #916, #913, #912, #910,
      #908, #888, #594, #518 — were read with `gh pr view <n> --json files` and
      **not one touches any `neutral-product-pin` path**. So this change is the
      **SOLE ACTIVE MODIFIER** of the requirement key, `modified-block-currency`'s
      two-writers rule does not reach the pair, and no ordering declaration is
      owed in either direction.
