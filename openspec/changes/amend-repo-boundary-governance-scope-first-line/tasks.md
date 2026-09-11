# Tasks: amend-repo-boundary-governance-scope-first-line

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
Heap's word of 2026-09-11T00:42Z, verbatim *"do 915 and 931, land each when
green"*, commissions this AUTHORING and pre-gives the LANDING word for a
ratified head; it ratifies no wording and resolves none of `design.md`'s three
decisions, so this packet carries no approval pair and no document in it says
`Status: ratified`. **§ 5 (archive) IS ALSO ENTIRELY OPEN**: promotion is a
third act on a third word, so openxFactory #931 closes AT THE ARCHIVE and not
at this landing, and `Closes #931` appears on the archive pull request and on
nothing else. § 6 records what was measured and deliberately not taken.

**AND THE ORDER OF THE DECISIONS IS NOT THE ORDER OF THE SECTIONS.**
`design.md` **D6 IS PUT FIRST** and it can end the packet: the failure this
amendment answers is REAL on the OpenSpec CLI at 1.2.0 and is reported by NO
REQUIRED CHECK, because openxFactory validates through the pinned 1.12.0
artifact and this specification PASSES there. Whether promoted canon should be
amended for a binary no required check runs is the owner's call, § 1.2 is the
box that records it, and **IT IS ASKED FRESH FOR THIS REQUIREMENT** — the
ruling of 2026-09-10 on the sibling requirement is quoted as precedent and is
not read as a standing rule.

## 1. Ratification — OWED, NOT GIVEN

**THIS SECTION IS OPEN BY DESIGN.** The word behind this packet commissions an
authoring and pre-gives a landing word; it admits no text to canon.

- [ ] 1.1 **RATIFY THE PACKET**, on Brett Heap's word and never on this lane's
      judgment. At ratification `proposal.md`, `design.md` and this file flip
      to `Status: ratified` with ONE citation line each, a
      `review/ratification-<date>.md` record is written carrying
      `Status: ratified`, and `.openspec.yaml` GAINS `approved_by`/`approved_on`
      **BESIDE** the drafting provenance with `kind`, `id`, `reason` and
      `proposed_by` unmoved — the addition-not-rewrite shape
      `add-drafted-proposal-origin` (issue #318) defined and the shape the
      archive gate's origin-retention arm reads, which is why the status flip
      and the approval pair move in ONE commit. The word of 2026-09-11T00:42Z,
      verbatim *"do 915 and 931, land each when green"*, recorded in this
      lane's CLAIMED comment on openxFactory
      [#931](https://github.com/opensoft/openxFactory/issues/931), stays the
      ORIGIN of the AUTHORING and the pre-given LANDING word, and is NOT read
      as an approval.
- [ ] 1.2 **RULE `design.md` D6 — AMEND, or CLOSE #931 ON THE MEASUREMENT.**
      Put FIRST because it can end the packet. The failure is real on the 1.2.0
      binary on PATH (`✗ [ERROR] requirements.1.text: Requirement must contain
      SHALL or MUST keyword`, exit 1) and ABSENT from the pinned 1.12.0 the
      required gate runs (exit 0, `spec/repo-boundary-governance` among the
      passes, six INFO notes). D6 recommends AMENDING ANYWAY on three grounds
      that are not the red gate — a ten-to-one convention inside this one file
      in which all ten compliant first lines are 79 characters or fewer, an
      unfinished 1.12 migration in which every engineer and agent who types the
      command this repository's own notes tell them to type meets a red
      specification, and the fact that this is the corpus's LAST instance so
      taking it empties the class — and writes the alternative out beside it.
      **A VETO HERE WITHDRAWS THE PACKET**, it does not re-wire it.
      **THE 2026-09-10 RULING ON #882 IS PRECEDENT, NOT ENTAILMENT**, and the
      difference is measured: two of its three grounds read differently here
      (ten to one, not seventeen; four words added, not two case flips).
- [ ] 1.3 **RULE `design.md` D1 — THE WORDING.** Three options are written out
      with their costs and the recommended one is ENCODED.
      **Option 1 (RECOMMENDED and written)** re-orders with a closed subject
      phrase: *"The following install repositories SHALL be scoped to subsystem
      install, operations, backup, restore, upgrade, verification, and disaster
      recovery: `Hermes-Install`, …"* — four words added, none removed, the
      five names in canon's order, spelling and serial comma, first body line
      72 characters with `SHALL` at word five.
      **Option 2** changes NOT ONE WORD and moves only the line breaks, which
      owes no marker at all — proven, not argued — and costs a 108-character
      first line in a file whose ten compliant first lines are all 79 or fewer,
      and a compliance that rests on a line break the currency family is
      contractually blind to.
      **Option 3** is the counted subject issue #931 itself floats, REFUSED
      because it copies the count FIVE into a second requirement when the
      sibling *Install-repository enumerations are an index with a named
      authority* already states it and exists because these enumerations drift.
      A veto to option 2 replaces the block with the re-flow-only block,
      DELETES the marker and re-runs the gates; a veto to option 3 is a wording
      swap plus a note about the count's second home.
- [ ] 1.4 **RULE `design.md` D2 — THE TWO MARKER DECISIONS**, and carry or veto
      D0, D3, D4, D5 and D7 beside them. **D2a:** ONE `Removed from canon`
      marker, ONE name, no code span in its reason, is owed under option 1 and
      is written; under option 2 none would be owed. **D2b:** the marker this
      requirement INHERITS from `refresh-install-repository-enumerations`
      (2026-09-08, promoted at `:66`) is NOT carried forward, on canon's own
      rule at `openspec/specs/doc-health/spec.md:1801-1805` and on a
      four-times-repeated precedent; the cost is that the promoted file stops
      showing the 2026-09-08 widening and the reader is sent to the archived
      delta canon names as the durable record. Both branches are proven with
      the family's own `derive_units` and `suppression` in § 3.3.

## 2. The measurement — TAKEN BEFORE THE DESIGN, DONE IN THIS PULL REQUEST

- [x] 2.1 **THE CORPUS WAS MEASURED, NOT SAMPLED.** Across all **62** promoted
      spec files under `openspec/specs/` and all **641** `### Requirement:`
      headings in them, **exactly 1** has a first body line carrying neither
      `SHALL` nor `MUST`: `openspec/specs/repo-boundary-governance/spec.md`
      index **1** (heading `:34`, body `:35`). Its predecessor's § 2.1 measured
      TWO on the same corpus and the same predicate; the archive of
      `amend-neutral-product-pin-lockfile-first-line` cleared the other, so
      **this is the corpus's LAST instance**.
- [x] 2.2 **TEN TO ONE INSIDE THIS ONE FILE, AND ALL TEN INSIDE 80
      CHARACTERS.** `repo-boundary-governance` carries **11** requirements;
      **10** open their body with `SHALL` on line one, at 63, 67, 70, 71, 73,
      74, 75, 75, 76 and 79 characters — **none of them 80 or more**. That is
      the REVERSE of what the predecessor found in `neutral-product-pin` (seven
      of seventeen at 80 to 397 characters), so a long first line is NOT house
      style here and that is a real cost against `design.md` D1's option 2
      rather than a borrowed argument. Index 1 is the only one that opens with
      an enumeration.
- [x] 2.3 **THE REQUIREMENT IS NOT SHORT OF OBLIGATION**, which is why this is
      an amendment of EXPRESSION and not of rule: `SHALL` stands at `:36`, one
      line below the first, and `MUST` **3** times below that, once in each
      scenario.
- [x] 2.4 **BOTH BINARIES WERE MEASURED, AND THE PINNED ONE DOES NOT REPORT
      THIS AT ALL** (`design.md` D6). `contracts/openspec-cli-pin.yaml:255`
      pins `version: "1.12.0"`; `.github/workflows/openspec-cli-pin-gate.yml`
      runs `python3 scripts/validate-openspec-cli-pin.py --all --no-cache`
      through the content-verified artifact; and on that binary this
      specification PASSES, `Specification 'repo-boundary-governance' is
      valid`, exit 0, six INFO notes. The runs and their exit codes are in § 4.
- [x] 2.5 **THE MECHANISM IS CITED, NOT RE-CLAIMED.** The controlled
      three-requirement fixture that proves 1.2.0 reads one line and 1.12.0
      reads the whole body lives in the ARCHIVED
      `amend-neutral-product-pin-lockfile-first-line`'s `design.md` D6. This
      packet cites it and does not re-run or re-claim it.
- [x] 2.6 **THE ARCHIVE WRITES THE DELTA BLOCK VERBATIM, PROVEN ON THIS VERY
      FILE.** The promoted block at `:34-66` is BYTE-IDENTICAL to
      `openspec/changes/archive/2026-09-09-refresh-install-repository-enumerations/specs/repo-boundary-governance/spec.md:5-37`
      — sha256 `24f6479c03641027e791c46d6a1bc29ac6b5af6f37b6ca3c1f4781bdd3c069ee`,
      2,885 bytes, on both sides. That is what makes `design.md` D2b a real
      decision rather than a formality: a marker this block omits does not
      survive promotion.
- [x] 2.7 **THE MARKER-CARRIAGE PRECEDENT WAS MEASURED ACROSS THE WHOLE
      CORPUS.** 23 promoted requirements have been modified by two or more
      archived changes; only **one** accumulates markers from more than one
      change. `doc-health`'s *Currency of an active change's MODIFIED
      requirement* was amended **four** times in five days and each block
      carried exactly ONE marker, its own, the promoted text today carrying
      only the last. Five apparent counter-examples were checked and are
      FENCED EXAMPLES inside the `doc-health` spec rather than live markers —
      `fenced_regions` says so — so they are not precedent in either direction.
- [x] 2.8 **`kind: ad_hoc` WAS CHECKED RATHER THAN ASSUMED.**
      `ideation/staging/` was enumerated (**30** topic folders) and `INDEX.md`
      read: no topic folder and no INDEX row names this requirement, the
      first-body-line shape or the strict keyword rule, and
      `grep -rliE "install repository scope|first body line|first-body-line|SHALL or MUST" ideation/staging/`
      returns nothing (exit 1). The one hit for the capability NAME is a
      passing citation in `wallet-carried-work-authority`, an unrelated topic.
      `kind: staged` would claim a staging source that does not resolve. The
      organized source is issue #931 and the three passages of its
      predecessor's packet that named it.

## 3. The delta — DONE IN THIS PULL REQUEST

- [x] 3.1 **ONE `## MODIFIED` REQUIREMENT, WRITTEN OVER CANON, BYTE-FAITHFUL BY
      CONSTRUCTION RATHER THAN BY TRANSCRIPTION** — the method
      `amend-modified-block-currency-standing`'s `tasks.md` § 2.1 established
      and `amend-neutral-product-pin-lockfile-first-line` repeated. The block
      was generated by SLICING
      `openspec/specs/repo-boundary-governance/spec.md` lines **34–66** (the
      `### Requirement:` heading at `:34` through `:66`, the last non-blank line
      before the next heading at `:68` — 33 lines, sha256
      `24f6479c03641027e791c46d6a1bc29ac6b5af6f37b6ca3c1f4781bdd3c069ee`, 2,885
      bytes), applying the ONE change as an exact SINGLE-OCCURRENCE
      substitution over the first sentence — **the generator refuses on any
      other occurrence count**, and it asserts that the paragraph's text
      OUTSIDE the substituted sentence is identical on both sides — and
      re-wrapping ONLY the paragraph that substitution touched, at the file's
      own width of 79.
- [x] 3.2 **THE GENERATOR'S OUTPUT AND THE COMMITTED BLOCK ARE ONE STRING**:
      34 lines, sha256
      `50ced1fa72901a62ea0add5401b9a8511297d04c612d4985fe13aa8dd9d5b0b4`, 3,404
      bytes, on both sides. The requirement HEADING is byte-identical, and the
      **27** lines from `:38` to `:64` — the whole second body paragraph, all
      three scenario headings and all six scenario bullets — are canon's own
      bytes, compared line by line and hashed: sha256
      `8d30b74e26f014d2076627f6b8763f54b563f6249ae7f5cd8c375a2ed6444904` on both
      sides.
- [x] 3.3 **THE ACCOUNTING IS DERIVED BY THE FAMILY'S OWN CODE, AND EVERY
      BRANCH OF BOTH MARKER DECISIONS IS PROVEN.**
      `scripts/doc_health/modified_block_currency.py`'s `derive_units` over
      canon's requirement returns **13 units** — 4 body, 3 scenario titles, 6
      scenario bullets — and over this block **13 units** in the same
      three-way split. `carried()` reports **1 uncarried** canon unit (the
      retired first sentence) and **1 added** block unit (its replacement);
      `suppression()` reports **1 suppressed** and **0 marker defects**. The
      three canon scenario titles are carried in canon's order and the block
      adds none. **FOUR BLOCKS WERE GENERATED ON THIS TREE AND ALL FOUR
      MEASURED**, so both decisions were read off numbers rather than argued:
      option 1 with the inherited marker carried (1 uncarried, 1 added, **1**
      marker defect on ground three); option 2 with it carried (0, 0, **1**);
      option 1 with it dropped — the committed block — (1, 1, **0**); option 2
      with it dropped (0, 0, **0**). The counterfactual confirms canon's own
      normalization rule (*"a re-wrapped paragraph compares equal to the same
      paragraph wrapped differently"*,
      `openspec/specs/doc-health/spec.md:1668-1672`): **option 2 would owe no
      marker and none would be written.**
- [x] 3.4 **FOUR WORDS ADDED, NONE REMOVED**, measured whitespace-split and
      CASE-SENSITIVE rather than described: the new sentence's 24 tokens minus
      the retired sentence's 20 are `The`, `following`, `install`,
      `repositories`, `recovery:` and `` `OmniWorker-Install`. ``; the retired
      sentence's minus the new one's are `recovery.` and
      `` `OmniWorker-Install` ``. Four words and two punctuation moves. 215
      characters become 251. **THIS IS LARGER THAN THE PREDECESSOR'S EDIT AND
      THE PACKET SAYS SO**: that sentence already carried a subject to promote
      and this one does not, so no zero-word re-order of it exists.
- [x] 3.5 **THE OBLIGATION LANDS ON LINE ONE, WHICH IS THE WHOLE POINT.** The
      block's first body line is `The following install repositories SHALL be
      scoped to subsystem install,` — **72 characters**, `SHALL` at word five,
      inside the file's own observed range of 63 to 79. Canon's is
      `` `Hermes-Install`, `Omnigent-Install`, `Keycloak-Install`,
      `OpenXPKI-Install`, `` — 77 characters, no keyword.
- [x] 3.6 **ONE `Removed from canon` MARKER, ONE NAME, NO CODE SPAN IN ITS
      REASON**, placed at the END of the block and ASSEMBLED FROM
      `derive_units`' OWN OUTPUT rather than retyped. The retired sentence
      carries five code spans, so the name is fenced with a DOUBLE backtick and
      one space of padding on each side — the same fence
      `refresh-install-repository-enumerations` used in this file for the same
      reason — and the ` — ` reason boundary stands outside every code span.
      Re-parsed by `parse_marker` on the committed file it yields form
      `removed`, change id `amend-repo-boundary-governance-scope-first-line`,
      date `2026-09-11`, **exactly one name EQUAL to the single uncarried canon
      unit**, an **EMPTY `quoted` list**, no destination, and a 1,152-character
      reason carrying **0 code spans** — so none of the marker-defect class's
      five grounds can fire on it.
- [x] 3.7 **THE INHERITED MARKER IS NOT CARRIED, AND THE DECISION IS CITED
      RATHER THAN PREFERRED** (`design.md` D2b). Canon:
      *"**A marker is NOT a carriage unit, in either direction** … The durable
      record of a deletion is the archived delta"*
      (`openspec/specs/doc-health/spec.md:1801-1805`). The durable record is
      named in the delta header and in § 2.6:
      `openspec/changes/archive/2026-09-09-refresh-install-repository-enumerations/specs/repo-boundary-governance/spec.md:37`.
      The alternative is costed in § 3.3: carrying it yields one `info`-band
      marker-defect finding on ground three, on either wording.
- [x] 3.8 **NOTHING UNDER `openspec/specs/` IS EDITED BY THIS PULL REQUEST**,
      and no script, test, contract, schema, workflow or example is touched
      either. The promoted specification still states the sentence as ratified;
      the ARCHIVE act is what would write this block into it.
- [x] 3.9 **README `## OpenSpec Records` CARRIES THE ACTIVE ROW**, in house
      style, at the head of the active list, lane `openxfactory-1`, written as
      **`Status: draft`** (NOT RATIFIED) and naming the origin issue, the
      accounting, both marker decisions, the three questions put for the owner
      and what this pull request does not do.
- [x] 3.10 **THE PER-CHANGE SWEEP LEDGER ROW IS SEEDED BY THE SANCTIONED
      TOOL**, never hand-written:
      `python3 scripts/validate-sequenced-after.py . --seed-ledger --moved-by '#<PR>'`.
      The row reads `declares: []` — the positive root claim — and
      `class: co-modifier`, which is NOT a contradiction of § 4.5: the ledger
      grades `class` over the WHOLE corpus, archived changes included, and this
      requirement's key is necessarily also written by the ARCHIVED changes
      that promoted and last wrote it. Any partner row the seed flips is
      recorded in § 4.5 rather than left to be found.

## 4. Gates — RUN IN FULL, WITH EXIT CODES, ON THIS PULL REQUEST'S TREE

**EVERY FIGURE BELOW IS A RUN, NOT A RECOLLECTION**, and where a figure only
means something against `main` the CONTROL is a second worktree rather than a
remembered number. **§ 4.1–4.9 WERE TAKEN AGAINST `origin/main` `114d6e3d`**,
the base this branch was cut from, checked out detached in its own worktree.

- [x] 4.1 `OPENSPEC_TELEMETRY=0 openspec validate
      amend-repo-boundary-governance-scope-first-line --strict` — **`Change
      'amend-repo-boundary-governance-scope-first-line' is valid`, exit 0.**
- [x] 4.2 `OPENSPEC_TELEMETRY=0 openspec validate --all --strict` (1.2.0 on
      `PATH`) — **exit 1** on both trees, and **THE FAILURE SET IS
      IDENTICAL**: `change/disposition-codexfactory-declared-renames`,
      `change/disposition-codexfactory-floor-relocation-retitle`,
      `spec/repo-boundary-governance`. `diff` over the sorted `✗` lines of the
      two runs is EMPTY. Totals move by exactly one PASSING item — this
      packet's own change: control `Totals: 97 passed, 3 failed (100 items)`,
      this branch `Totals: 98 passed, 3 failed (101 items)`, with
      `✓ change/amend-repo-boundary-governance-scope-first-line` in the branch
      run. **`spec/repo-boundary-governance` STILL FAILS AND THAT IS CORRECT**:
      a delta does not edit the promoted specification, so the failure this
      packet answers is still there at this head, with the same error text
      issue #931 quotes — `openspec validate repo-boundary-governance --strict
      --type spec` gives `Specification 'repo-boundary-governance' has issues`
      / `✗ [ERROR] requirements.1.text: Requirement must contain SHALL or MUST
      keyword`, exit 1. **THE ARCHIVE ACT IS WHAT CLEARS IT**, and the archive
      is § 5.
- [x] 4.3 `python3 scripts/validate-openspec-cli-pin.py --all` (the pinned
      1.12.0, content-verified) — **exit 0** on both trees. The exact
      invocations differ in ONE flag and it is named rather than glossed: the
      CONTROL ran `--all --no-cache` (a temporary prefix discarded at the end)
      and the BRANCH ran `--all --cache-dir <path>` reusing that same verified
      install; both verify the artifact's content address before invoking it,
      and both print the same integrity line. Totals: control
      `Totals: 98 passed, 2 failed (100 items)`, this branch `Totals: 99
      passed, 2 failed (101 items)`. The two failures are the two
      DISPOSITIONED scenario-omission findings accepted on Brett Heap's word of
      2026-09-05 *"take exit 2"* (`add-chain-attestation` /
      `signed-execution-chain`, `add-composed-view-authoring` /
      `ideation-dashboard`), and `spec/repo-boundary-governance` carries INFO
      notes only — six of them, and it is among the PASSES. Both runs report
      `@fission-ai/openspec@1.12.0 verified against its content address` and
      the 80-package dependency closure installed with `npm ci
      --ignore-scripts`, closing with `every target validated --strict with 0
      UNDISPOSITIONED failures`. The named-spec run on the same binary gives
      `Specification 'repo-boundary-governance' is valid`, exit 0.
- [x] 4.4 `python3 scripts/proposal-support.py . verify
      amend-repo-boundary-governance-scope-first-line` — **`proposal support
      verification ok`, exit 0.**
- [x] 4.5 `python3 scripts/validate-sequenced-after.py .` — **exit 0**:
      `sequenced_after validation passed (39 active changes, 9 declaring the
      field)`, plus `archive-date agreement passed` and
      `archive-date-vs-commit agreement passed`. And
      `python3 scripts/validate-sequenced-after.py . --ledger-diff` — **exit
      0**, `per-change sweep ledger consistent with the corpus (198 rows)`,
      after § 3.10's seed. **BEFORE the seed it exited 1 and named exactly what
      the seed then moved**, which is recorded rather than hidden: `missing
      row: amend-repo-boundary-governance-scope-first-line` and seven derived
      total mismatches (`change_ids` 197 != 198, `active` 38 != 39,
      `co_modified` 143 != 144, `active_co_modified` 23 != 24, `declaring`
      22 != 23, `root_claims` 5 != 6, and the `declaring_ids` tuple). The seed
      wrote `198 rows, 1 moved by #937` and named it. **NO PARTNER ROW FLIPPED
      AND THAT IS MEASURED, NOT ASSUMED**: `git diff` over
      `tests/sequenced_after/corpus-ledger.yaml` is **ONE INSERTED LINE**, this
      change's own row — unlike the predecessor packet, whose seed also flipped
      its archived promoter from `sole` to `co-modifier`, because both of this
      requirement's archived writers already graded `co-modifier`.
- [x] 4.6 `python3 scripts/validate-scope-globs.py .` — **`scope_globs
      validation passed (all active changes conform).`, exit 0.**
- [x] 4.7 `python3 scripts/doc-health.py --single-repo .` — **exit 0** on both
      trees, `Findings: 32 critical, 5 error, 47 warning, 15 info. New
      regressions vs previous report: 0` on BOTH — and **NO FINDING NAMES THIS
      CHANGE** (`grep -c amend-repo-boundary-governance-scope-first-line` over
      the branch report = **0**). **THE TWO REPORTS ARE BYTE-IDENTICAL ONCE THE
      REPOSITORY LABEL IS NORMALIZED**: 348 lines and 99 finding lines each,
      `md5` `177901498123ce6c02ba6188792e6312` on both, the only raw difference
      being the worktree name in the `Repo-Identity:` header and in each
      finding's repository prefix. In particular the
      `modified-block-currency` family — which reads every active block by
      construction and reports **11** findings across other active changes in
      this same run — reports NOTHING about this block, which is both marker
      decisions working in the real gate rather than only in § 3.3's
      derivation.
- [x] 4.8 `python3 -m pytest tests/sequenced_after tests/scope_globs
      tests/proposal-support -q` — **`489 passed, 66 subtests passed`, exit
      0.** Before § 3.10's seed the same set exited 1 with exactly four
      failures, all four the ledger's staleness and none of them about this
      packet's content
      (`test_the_LIVE_corpus_and_the_LEDGER_agree_row_by_row`,
      `test_every_corpus_change_has_EXACTLY_ONE_row_and_every_row_a_change`,
      `test_the_totals_DERIVED_FROM_THE_LEDGER_equal_the_MEASURED_sweep`,
      `test_the_live_ledger_reports_the_SAME_totals_the_sweep_MEASURES`) —
      measured by stashing the seeded ledger and re-running, then restoring it.
      The seed clears all four.
- [x] 4.9 **BOTH PROOFS ARE RE-RUNNABLE AND ARE RE-RUN ON EVERY MERGE FROM
      `main`**: the generator reports slice `34..66`, 33 lines, sha256
      `24f6479c…`, and generator output identical to the committed block at
      sha256 `50ced1fa…`, 3,404 bytes; `derive_units` reports 13/13 units, 1
      uncarried, 1 added, 1 suppressed, 0 marker defects and the three scenario
      titles equal in order. The carried tail — `:38` to `:64`, 27 lines —
      hashes `8d30b74e…` on both sides.

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
      amend-repo-boundary-governance-scope-first-line --date <YYYY-MM-DD>
      --yes` and never a bare `openspec archive`. The promoted block must be
      **BYTE-IDENTICAL** to the delta, measured and recorded in the archive
      pull request's body rather than asserted — the property the refusal on
      PR #780 was protecting when it declined to reword canon in an archive.
      **AND THE ARCHIVE IS WHAT CLEARS § 4.2's `spec/repo-boundary-governance`
      FAILURE ON THE 1.2.0 BINARY**, which is the one gate figure this packet
      changes and it changes it THERE and not here — measured before and after
      and pasted, never claimed. **THE ARCHIVE ALSO REMOVES THE INHERITED
      MARKER FROM THE PROMOTED FILE** (`design.md` D2b), which the archive pull
      request must state in its body rather than let a reader discover in the
      diff.
- [ ] 5.2 **CLOSE openxFactory issue #931 AT THE ARCHIVE, not at this
      landing.** This pull request's body says `refs #931` and carries **no
      closing keyword**, and no commit message on this branch carries one
      either — not `Closes`, not `Fixes`, not `Resolves`, in any case or tense,
      quoted or unquoted — so `closingIssuesReferences` on this pull request is
      `[]`, verified through GraphQL and recorded in the body. `Closes #931`
      belongs on the archive pull request and on nothing else.

## 6. Measured, and deliberately NOT taken here

- [ ] 6.1 **THE MARKER-CARRIAGE QUESTION AS A GENERAL RULE IS NAMED AS RESIDUE
      AND IS NOT TAKEN.** `design.md` D2b decides it for THIS block on canon's
      own sentence and on the corpus's four-times-repeated practice, and the
      measurement it rests on exposes something more general: **any later
      amendment of a requirement whose promoted text already carries a marker
      must either drop that marker or accept a ground-three marker-defect
      finding** — there is no third option today. That may be the right
      behaviour or it may be a gap in `modified-block-currency`. **THIS PACKET
      NEITHER TAKES IT NOR FORECLOSES IT**: it is a `doc-health` amendment, a
      different capability, and under the ruling of 2026-09-06T23:10Z
      (*"Tick on the recording"*) this box ticks once a successor is NAMED —
      which means filing its issue, and that is not this lane's act on this
      word. A search of `gh issue list --state all` before this box was written
      found no open issue reporting it.
- [x] 6.2 **THE REQUIREMENT'S HEADING IS NOT EDITED.** *"Install repository
      scope"* is a noun phrase and is correct; editing a ratified heading
      changes the requirement KEY every consumer, marker and currency check
      matches on, which is a far larger act than this word commissions. This
      box is a MEASUREMENT and ticks on the measurement being taken and
      recorded.
- [x] 6.3 **THE SIBLING REQUIREMENT'S COUNT IS NOT TOUCHED, AND IS THE REASON
      D1's OPTION 3 IS REFUSED.** *Install-repository enumerations are an index
      with a named authority* (`:308`) states *"the install repositories …
      number FIVE"*. Writing that count into the scope requirement as well
      would create a second copy of one declaration in the one capability whose
      own prose records that enumerations drift. The count is left where it is
      and is not duplicated.
- [x] 6.4 **THE OTHER THREE ENUMERATIONS `refresh-install-repository-enumerations`
      TOUCHED ARE NOT SWEPT.** Its markers also stand in *Canonical workflow
      authority* (`:32`), *Copy-first migration* and
      `shared-contract-ownership`'s *Contract version pinning*. None of those
      requirements has a first-line defect, none is edited here, and D2b's
      reasoning is deliberately NOT applied to them: this packet drops one
      inherited marker because it is amending that one requirement for another
      reason, never as a tidy-up.
- [x] 6.5 **THE TWO DISPOSITIONED FINDINGS ARE UNTOUCHED.** The pinned run in
      § 4.3 names two accepted exceptions (`add-chain-attestation` /
      `signed-execution-chain`, `add-composed-view-authoring` /
      `ideation-dashboard`), granted on Brett Heap's word of 2026-09-05
      *"take exit 2"*. Neither is related to this requirement, no entry of
      `contracts/openspec-cli-pin.yaml` moves, and this packet neither renews
      nor retires either one.
- [x] 6.6 **`prepare-openspec-1-12-readiness` IS NOT AMENDED.** The controlled
      two-binary fixture that proves the mechanism lives in the ARCHIVED
      predecessor's `design.md` D6 and is CITED here rather than re-run or
      re-claimed. This packet writes no readiness evidence and claims no part
      of that migration.
- [x] 6.7 **THE SIBLING SEARCH WAS TAKEN BEFORE THE CLAIM AND RE-TAKEN AT THE
      BRANCH CUT** (`design.md` D5). `ls -d
      openspec/changes/*/specs/repo-boundary-governance` returns FIVE active
      deltas — `add-identity-brokering`, `add-trust-anchor`,
      `implement-keycloak-install-repo`, `implement-openxpki-install-repo`,
      `qualify-avatar-live-voice` — and each was read BY NAME: they write
      *Keycloak install repository boundary*, *OpenXPKI install repository
      boundary* and *Neutral avatar-client repository boundary*, **not one of
      them this requirement**. The corpus search is pasted in a form that
      REPRODUCES, the archive exclusion being a PIPE rather than prose —
      Copilot's finding on this pull request, taken:
      `grep -rln "Install repository scope" openspec/changes/ --include=spec.md
      | grep -v '/archive/'` returns THIS CHANGE AND NOTHING ELSE (exit 0, one
      line), and the PRE-ADDITION result is re-derivable against the branch
      point with `git grep -l "Install repository scope" 114d6e3d --
      'openspec/changes/*/specs/*/spec.md' | grep -v '/archive/'` — nothing,
      exit 1. Unfiltered the search returns three ARCHIVED deltas as well, so
      the filter belongs in the command. All **six** pull requests open at the branch cut
      — #934, #932, #921, #888, #594, #518 — were read with `gh pr view <n>
      --json files` and **not one touches any `repo-boundary-governance`
      path** (six zeroes). So this change is the **SOLE ACTIVE MODIFIER** of
      the requirement key, `modified-block-currency`'s two-writers rule does
      not reach any of the five, and no ordering declaration is owed in either
      direction.
