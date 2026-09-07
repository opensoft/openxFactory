# Proposal Ratification: publish-openspec-cli-pin-as-contract-member

Status: record
Kind: report
Decision date: 2026-09-07
Ratifier: Brett Heap (openxFactory operator authority) — in session
Ratified: 2026-09-07 by Brett Heap (openxFactory operator authority) —
in-session, lane `openxfactory-1`, verbatim: *"merge 72 when green, then ratify
the A packet"*, recorded on openxFactory issue
[#754](https://github.com/opensoft/openxFactory/issues/754) at
**2026-09-07T14:27:55Z**. The word has two clauses and BOTH are discharged: the
FIRST landed xFactory-Hermes-Install
[#72](https://github.com/opensoft/xFactory-Hermes-Install/pull/72) as merge
commit `06c9083d` at 14:42:30Z — the estate's first declared consumption copy,
B of #754 — and the SECOND is this act. It was given after a presentation that
carried this packet's veto points BY NAME: `design.md` **D1** — **A-defer**
(register the pin in the two editorial files and cut no bundle) against
**A-cut** (register AND cut `contract-v3.5` in this pull request, with the
annotated tag owed after the merge), with the third option **A-member** (move
the derived membership 283 → 285 by adding the pin to `AUXILIARY_MEMBERS` in
`scripts/hermes_runtime_validation/release.py`) recorded as NOT TAKEN rather
than foreclosed — and `design.md` **D2**, named separately so it could be
vetoed on its own, the manifest row carrying no `sha256`. **NONE WAS VETOED.**
Ratified baseline: this change as committed in the ratification commit carrying
this record — `proposal.md`, `design.md`, `tasks.md`, `.openspec.yaml` and
`specs/neutral-product-pin/spec.md` (**TWO ADDED requirements**, no `## MODIFIED`
and no `## REMOVED`) — together with the REALIZATION this packet's
`code_surface` declares: the ONE new `contracts/manifest.yaml` row
(`id: openspec-cli-pin`, `type: pin`, no `sha256`), `contracts/README.md`'s
matching Native-contract-index row and its new consumer-facing section *Gating
archives on the pinned CLI from a consumer repository*, plus the root
`README.md` OpenSpec Records row and this change's row in
`tests/sequenced_after/corpus-ledger.yaml`, with
`openspec validate publish-openspec-cli-pin-as-contract-member --strict` green
through the pinned 1.12 route and the verification run captured beside this file
at `verification-2026-09-07.md`.

**This record is CAPTURED AT MERGE, not at first push, and it was RE-DERIVED
PRE-CAPTURE.** `record-immutability` forbids editing a `Status: record` document
AFTER capture; capture is the merge of the pull request that establishes it, and
nothing is merged yet. Every number in `verification-2026-09-07.md` was
re-derived on the tree this record sits in, at `origin/main` **`f756a91f`** — the
head this branch's THIRD and last catch-up merge took. **THREE MERGES FROM
`main` STAND ON THIS BRANCH, AND ALL THREE ARE NAMED**: `e318e0e7` (taking
`64aad02e`), `85adc0f3` (taking `5e4d960c`, which landed the Apache-2.0
`LICENSE`, PR #762) and `ee657e30` (taking `f756a91f`, the ratification of
`amend-absent-changelog-is-an-answer`, PR #753 — taken BEFORE this ratification
was encoded, with NO conflict: the 32 paths `main` moved include `README.md`,
where both sides had added a row to the *Active changes* block and git kept
BOTH, and `tests/sequenced_after/corpus-ledger.yaml`, where both sides added a
row and git kept both; nothing else `main` moved is a path this packet edits).
A commit cannot write its own hash into its own tree, so the ratification commit
is named by its subject and its position on the branch rather than by a hash;
the `--archive-gate` runs that take it as `--ratified-ref` are appended to
`verification-2026-09-07.md` in a follow-up commit touching `review/` files
only.

## 1. What was ratified, and what it says

**TWO requirements are ADDED to `neutral-product-pin` and none is modified or
removed.** No file is added under `openspec/specs/`, so **no codexFactory floor
advance is owed**.

**R1 — *A consumption pin that another repository reads is a PUBLISHED contract
member, adopted by pin-sync*, SEVEN scenarios.** A consumption pin SHALL be a
published contract member wherever any repository other than `openxFactory` is
expected to read it: registered in `contracts/manifest.yaml` with an `id`, its
`path`, a `type`, its `intended_consumers`, `adapter_owner: openxFactory` and a
`consumption_rule` stating the checkout-at-the-pinned-ref recipe and forbidding
copying, and indexed in `contracts/README.md`. Registration is what makes
adoption ride the consumer's ORDINARY PIN-SYNC, with no per-repository act
needed to LEARN that the pin exists. Publishing the pin is NOT publishing the
pinned product. A consumer gates by READING from the pinned checkout and NEVER
by copying. ONE fallback is admitted, for a repository with no stack pin, which
must declare the commit it copied from, the digest of what it copied and the
divergence it accepts, and must retire the copy when it adopts a stack pin.
**TWO of the seven scenarios and their clauses came from the three-lens fix
round and are part of what was ratified**: the PRECONDITION on the normal case
— a consumer whose `contract_ref` predates the commit that introduced the
entrypoint (openxFactory `1d8cd54e`, 2026-09-04) cannot perform the read, the
remedy is to ADVANCE the pin and never to copy, and a gate meeting the absence
REFUSES rather than skipping silently (*The consumer's pinned ref predates the
entrypoint*) — and the RECONCILIATION with this capability's promoted
requirement *A required check runs the pinned tool, at the pinned digest*: a
required check wired off a declared consumption copy leaves that requirement's
enforcement claim **UNMET** until the copy is retired, so declaring makes the
copy AUDITABLE and not LAWFUL (*A required check is wired off a declared
consumption copy*). A fifth scenario, *The published instructions name a verb
the entrypoint rejects*, came from Codex's P1 in bench round 2.

**R2 — *Registering a pin in the consumption register is not a bundle cut unless
it moves the release membership*, THREE scenarios.** The mechanical test, its
two outcomes, and an obligation on the REGISTERING AUTHOR: record the derived
membership BEFORE and AFTER, because a membership that is COMPUTED cannot be
eyeballed and silence about it is not evidence that it did not move. This packet
discharges that obligation in the packet that writes it — **283 → 283** — which
is § 3's D1 measurement.

**THE REALIZATION, in the same pull request** under `release-realization`'s
decomposition rule: ONE `contracts/manifest.yaml` row for
`contracts/openspec-cli-pin.yaml`, written on
`domain-factory-conformance-validator`'s precedent
(`contracts/manifest.yaml:184-199`) whose `consumption_rule` already carries the
never-copy rule in the register's own voice; the matching `contracts/README.md`
index row; and the new consumer-facing section carrying the four-step
checkout-at-`contract_ref` recipe, the never-copy rule and the declared copy-in
fallback. **`contracts/openspec-cli-pin.yaml` is NOT edited** — no version, no
digest, no `rollback:`, no `dispositions:` entry — and no script and no workflow
is edited.

## 2. Why the packet exists

**THE PIN GOVERNS A FLEET AND THE FLEET'S OWN CONTRACT REGISTER DOES NOT MENTION
IT.** `contracts/openspec-cli-pin.yaml` is the estate's claim about WHICH TOOL
adjudicates canon — `openspec validate --strict` is the gate every spec delta
passes, and the archive act is what writes a ratified delta into canon. Measured
2026-09-07 on `origin/main`, `git grep -c 'openspec-cli-pin'` returns **0** for
`contracts/manifest.yaml`, **0** for `contracts/README.md` and **0** for
`contracts/releases/contract-v3.4.digests.yaml`. Its two siblings,
`contracts/openxwallet-pin.yaml` and `contracts/openreposhape-pin.yaml`, are in
the same state: **the pin CLASS has never been published.**

**THE SURVEY BEHIND #754 SAYS WHAT THAT COSTS.** Of 26 repositories carrying
`openspec/`, exactly TWO gated on the pin (openxFactory; codexFactory, required
since its #227) and one more consumed it with a shadow-only gate (OpsxFactory);
twenty had zero pin awareness, three of them archiving that week on whatever
`openspec` was on `PATH`. **THE GAP IS PUBLICATION, NOT ENFORCEMENT**: the gate
is already ratified and running — `add-openspec-cli-pin` requirement 2 already
requires a consuming repository to invoke the pinned entrypoint FROM the pinned
openxFactory checkout and to name that version in its `stack.yaml` — and nothing
here restates, weakens or extends it. What was missing is that the pin is
FINDABLE and that adoption rides a pin-sync a consumer already performs.

**AND THE ESTATE HAS BOTH SHAPES IN IT, WHICH IS WHY R1 CARRIES BOTH.**
codexFactory and OpsxFactory resolve `stack.yaml['xfactory']['contract_ref']`,
check openxFactory out at that commit and invoke the entrypoint from that
checkout, copying nothing — the NORMAL case, OpsxFactory in a hardened form that
recomputes per-file SHA-256 digests against the pinned checkout before executing
the entrypoint. xFactory-Hermes-Install #72 is the first DECLARED COPY, and its
shortfall against R1 is named in § 4 rather than counted as met.

## 3. The decisions ratified knowingly

### D1 — A-defer (register, cut nothing), against A-cut; A-member not taken

- **A-defer, TAKEN AND RATIFIED, on a MEASUREMENT rather than a reading.** The
  derived release membership is a CLOSED set computed by
  `scripts/hermes_runtime_validation/release.py::_collect_members` (`:532-745`)
  from the hermes-runtime contract index, the fixture index,
  `scripts/hermes_runtime_validation/**`, four `NAMED_VALIDATORS`, seven
  `AUXILIARY_MEMBERS` and three `NORMATIVE_DOCS` (`:38-103`). **It never walks
  `contracts/manifest.yaml`'s `contracts:` list** — the manifest is read for
  `contract_bundle_version` and the six intent-compliance registrations and for
  nothing else — so a row added there moves NO member. Measured on this tree:
  **283 members before this diff and 283 after**, the pin absent from both, and
  283 is also the entry count of `contracts/releases/contract-v3.4.digests.yaml`,
  so the declared bundle and the derived membership agree. Both edited files are
  EDITORIAL members (`scripts/doc_health/release_inventory.py:57-67`), whose
  drift between cuts `release-surface-integrity` declares *"an EXPECTED, BOUNDED
  state that the next cut re-baselines"* and grades `info`, never `error`.
- **THE COST IS PUT WITH THE DECISION AND IS RESTATED HERE SO RATIFICATION
  CANNOT BE READ AS UNAWARE OF IT.** `docs/contract-versioning-policy.md`
  § *Change Classes* grades *"new contracts"* **Additive (minor)** and
  § *Version Identity* item 5 requires the changelog to carry *"one entry per
  release listing every contract added, changed, or deprecated"*. This packet
  registers a contract and cuts no release, and this repository writes no
  `Unreleased` block by practice, so **the `contracts/CHANGELOG.md` entry naming
  this registered contract is OWED AT THE NEXT CUT** (`tasks.md` § 5.7). That
  cost is ratified with the decision. The atomicity clause — *"the manifest and
  changelog update SHALL be committed atomically with the contract files"* — is
  not breached by the deferral: this diff adds no contract FILE (the pin already
  exists on `main` and is untouched, D7), only its register row.
- **A-cut, REJECTED FOR COST and written out beside A-defer rather than
  strawed**: it buys nothing this packet needs (the pin does not become an
  inventory member by being registered, and consumer adoption is BY COMMIT); it
  spends a version number that cannot be unspent (`contract-v2.6` is the
  standing record of what that costs); it creates a tag obligation this lane
  cannot discharge, which `release-tag-gate`'s `gate-findings` arm turns into a
  refusal of the NEXT pull request touching the release surface — the
  estate-wide red of 2026-09-03; and **it is not this lane's act to take**, a
  cut being a contract act on Brett Heap's word. **A-cut WAS NOT CHOSEN**, so
  its conditional — that a cut, if chosen, becomes a realization task of this
  packet — does not arise. This packet cuts nothing, allocates no version and
  owes no tag.
- **A-member, RECORDED AS NOT TAKEN RATHER THAN FORECLOSED.** Adding
  `contracts/openspec-cli-pin.yaml` to `AUXILIARY_MEMBERS` (and its entrypoint
  to `NAMED_VALIDATORS`) would move the derived membership **283 → 285** and
  would then require the bundle realization order under R2's own second
  scenario. It is a change to the RELEASE MACHINERY rather than to a register,
  and the word leaves it exactly where the packet put it: a different packet
  with a different risk profile. Naming it is what makes *"the pin is not in the
  inventory"* visibly a DECISION rather than an oversight.

**Ratified as designed. The reversal was NOT taken.**

### D2 — the manifest row carries NO `sha256`

- **No digest, TAKEN AND RATIFIED**, matching `domain-factory-conformance-validator`,
  the `type: tool` row this one is modelled on. `scripts/validate-manifest-digests.py`
  walks every entry carrying a `sha256` and fails closed inside the required
  `pytest-suite` — a good property for a file that moves at a cut, and
  `contracts/openspec-cli-pin.yaml` is not that kind of file: it moves on THREE
  distinct events, only one of which is a version bump (a bump; a DISPOSITION
  ADDED; a DISPOSITION RETIRED, which is forced from OUTSIDE — the verifier
  refuses `pin-disposition-stale` the moment a dispositioned finding stops
  occurring, including when the raising change archives in another repository).
  A digest would make each of those a two-file edit whose omission reds the
  required suite on `main`. What a digest would buy is already bought twice: the
  merge-gate floor names the pin a never-clearable path, and a version move is
  human-only with target-version evidence owed in the same change. The
  digest-bearing alternative is written out with its cost, so the veto had
  somewhere to land.
- **AND THE RESIDUAL COUPLING IS RATIFIED AS DISCLOSED.** Declining the digest
  does not make the row coupling-free: the row's `consumption_rule` QUOTES the
  path `scripts/validate-openspec-cli-pin.py`, the pin names that same path in
  its own `consumer_entrypoint:` field, and **nothing compares the two**. A
  rename that moved the pin and not the row would leave the register quoting a
  path that does not exist, silently. That is one string wide instead of one
  file wide, it is real, and it is owed to the checker at `tasks.md` § 5.4
  rather than written here.

**Ratified as designed. The row stands without a digest.**

### D7 — the pin file's own header is not edited, and the defect in it is owed elsewhere

`contracts/openspec-cli-pin.yaml` is NOT this packet's surface: publishing a pin
and moving a pin are different acts with different authorities, the second being
human-only with target-version evidence owed in the same change, and a packet
that did both would ask one word to cover two decisions. **Nothing in this
ratification may be read as approving a bump.** The consequence is carried
openly: the pin's own header still says *"Every repository in the estate runs
STRICT OpenSpec validation and every OpenSpec ARCHIVE through this entrypoint
and through nothing else"*, which R1's own register-names-both-commands clause
reaches by its own terms — the entrypoint has no archive verb. **That defect is
OWED ON THE PIN**, in the pin's own change family, and is recorded at
`tasks.md` § 5.9 rather than fixed from here.

## 4. What is NOT ratified, and the residue this word does not reach

The word ratifies the text and its realization. It does not reach any of the
following, each of which stands in `tasks.md` § 5 exactly as the word was given
over it.

1. **§ 5.1 — B of #754, the three no-lane repositories.** Their copy-in is
   separate work in separate repositories. It is not performed from this lane,
   and R1's fallback is what each copy must satisfy. **One shortfall is named
   rather than smoothed:** xFactory-Hermes-Install #72 (`06c9083d`) carries TWO
   of R1's three fields — the openxFactory commit copied from (`44d8fbaf`, in a
   vendoring header on each copied file) and the divergence accepted — and **the
   digest of what it copied is NOT recorded**; byte-identity is asserted below
   the header with a `diff` recipe in place of a per-file `sha256`. **The digest
   is OWED on xFactory-Hermes-Install**, is that repository's act, and is stated
   here as owed rather than counted as met.
2. **§ 5.2 — every other sibling's adoption belongs to its own lane**, by #754's
   second ruling: OpsxFactory's shadow gate becoming required, MedxFactory /
   AdxFactory / LedgerxFactory, the openDox family. Named so the omission reads
   as SCOPE rather than oversight. Three of those consumers cannot run the
   recipe today at all — MedxFactory and AdxFactory pin `6c03d783`, LedgerxFactory
   pins `af7ac0fa`, and the entrypoint is absent from all three — which is R1's
   ratified precondition and an ADVANCE-THE-PIN act on those repositories.
3. **§ 5.3 — the two sibling pins are unregistered too.**
   `contracts/openxwallet-pin.yaml` and `contracts/openreposhape-pin.yaml` are
   reached by R1's own terms wherever another repository reads them, and neither
   is registered by this packet: each needs its own reading of who reads it and
   on what terms, and one row-block over three pins would assert three
   consumption rules on one word.
4. **§ 5.4 — a registration is not a check.** Nothing in this repository asserts
   that a pin another repository reads IS registered, and nothing compares the
   row's quoted entrypoint against the pin's `consumer_entrypoint:` (D2's
   residual coupling). Both assertions belong in a checker beside
   `release-inventory-drift`, and neither is written here.
5. **§ 5.5 — THE ARCHIVE IS A SEPARATE ACT.** `code_surface` is non-empty, so
   under `release-realization` this packet archives on merged-plus-green
   realization evidence rather than on landing, and on a word distinct from this
   one. **This word ratifies; it does not archive.** openxFactory **#754** is the
   rollout's governing record and stays OPEN — it governs B and the sibling
   lanes as well as this packet — which is why the pull request says `Refs #754`
   and not `Closes`.
6. **§ 5.6 — a change id that no `sequenced_after:` can name.**
   `bump-openspec-cli-pin-to-1.12`'s id contains a `.`, which
   `scripts/validate-sequenced-after.py`'s grammar (`^[a-z0-9][a-z0-9-]*$`)
   admits no spelling of. Found by writing the declaration and reading the
   refusal. Three honest exits are recorded — widen the grammar, rename the
   change, or accept that the ordering is prose no machine reads — and none is
   taken here.
7. **§ 5.7 — the `contracts/CHANGELOG.md` entry is owed at the next cut**, which
   is A-defer's ratified cost (§ 3, D1). The release entry that follows this
   merge must list `contracts/openspec-cli-pin.yaml` among the contracts the
   bundle carries.
8. **§ 5.8 — `neutral-product-pin`'s Purpose will need widening AT ARCHIVE.** The
   promoted Purpose frames the capability in ONE direction, openxFactory as the
   CONSUMER of an external neutral product; R1 adds a third direction —
   openxFactory PUBLISHING its own consumption pin as a contract member others
   read and adopt by pin-sync. The widening belongs in the archive act, where
   the spec file is rewritten, and not in a delta that carries requirements
   rather than a Purpose block.
9. **§ 5.9 — the pin file's own header carries the unexecutable claim**, and
   this packet may not fix it (§ 3, D7). Owed on the pin, in the pin's own
   change family.

**AND ONE CONVENTION IS DISCLOSED RATHER THAN RATIFIED AS AN ENUMERATION.**
`target_release: none` is HOUSE PRACTICE and not an enumerated value:
`release-realization` § *Realization axis declaration* enumerates `implemented`
or a named aggregation-repo release, and eleven active changes in this corpus
spell the no-bundle case `none`. The front matter says so rather than claiming
an enumeration it does not have.

## 5. The bench, and the adversarial review folded before this record

- **THREE ADVERSARIAL LENSES on the pushed head returned MERGEABLE_AFTER_FIXES**
  — TWO MAJORS and eight smaller corrections, plus two NOTEs, nothing that
  breached a hard limit. **All were taken, in `2d195187` (merge tree
  `85adc0f3`) and `8eb5dc8f` (bench round 3), so the ratified baseline is the
  FOLDED text and not the text reviewed.** A re-verification pass over
  `8eb5dc8f` returned **READY_TO_ENCODE**.
  - **MAJOR 1 — the fallback's worked example was the wrong repository.** The
    packet cited OpsxFactory's `contracts/openspec-cli-pin-consumption.yaml` as
    R1's fallback realized, in five carriers. Measured, OpsxFactory HAS an
    `xfactory:` stack pin (`contract_ref: 724a2a4f`), copies NOTHING, records a
    POINTER rather than a copied-from commit, and its *"DECLARED DIVERGENCE"* is
    a divergence from OPSXFACTORY'S OWN ratified design TOWARD this pin. The
    citation was struck from all five carriers and OpsxFactory re-cited under
    the NORMAL case in hardened form; the fallback's first realized instance is
    xFactory-Hermes-Install #72, with its missing digest named as owed.
  - **MAJOR 2 — the normal-case recipe was not executable for three consumers.**
    `scripts/validate-openspec-cli-pin.py` first exists at openxFactory
    `1d8cd54e`; MedxFactory and AdxFactory pin `6c03d783` and LedgerxFactory
    pins `af7ac0fa`, and the entrypoint is absent from all three, so a literal
    reader would get a missing-file error and fall back to the ambient
    `openspec`. Step 1 of the recipe gained the precondition, the three named
    consumers, the advance-your-pin remedy and codexFactory's
    `scripts/validate-docs.sh:162` guard as the shape of a lawful refusal — and
    **R1 gained the matching clause and scenario**, so canon says it rather than
    a README.
  - The eight smaller corrections are re-measurements of the packet's own
    citations (the manifest's zero occurrences; ten files naming the string
    rather than three; seven singleton `type:` values rather than five; R1's
    seven scenarios rather than four; the two consumers' different environment
    variable names; § Ratification naming all three veto points;
    `docs/contract-versioning-policy.md` engaged in D1; D2's residual coupling
    named), each corrected in the direction of the stronger reading.
- **Codex: one round, one P1, TAKEN INTO CANON.** The published instructions
  told a consumer to route the ARCHIVE act through an entrypoint that rejects
  `archive <id>` as an unrecognized argument. Taken as R1's
  register-names-both-commands clause and its scenario, not as a local README
  fix. The thread was replied to and **resolved**.
- **Copilot: FOUR inline threads across the rounds by head, ALL taken and ALL
  resolved.** Bench round 3's two findings were violations of this packet's OWN
  new R1 clause, found in the two register carriers the first taking did not
  reach — the strongest possible reason to take them — and taking them is what
  exposed § 5.9, the same claim standing in a file this packet may not edit.
- **ONE REFUSAL STANDS, RE-MEASURED RATHER THAN RESTATED.** Copilot's
  *"licence" → "license"* nit was refused with counts, and the counts reproduce
  at every head they have been taken at, case-SENSITIVE and lowercase-only (the
  prose spelling; a case-insensitive count folds in machine keys that cannot
  change spelling). Repo-wide `licence`:`license` **203 : 526** when the refusal
  was posted, **204 : 535** at the fix-round head `85adc0f3` and **204 : 547**
  at this ratified head — the `license` side moving only because `main` landed
  the Apache-2.0 `LICENSE` (PR #762) and the #753 ratification records, neither
  of which is prose this packet wrote. `contracts/` **45 : 75** at all three
  heads; root `README.md` `licence` **9**, with one correction to the refusal's
  own text, which had said eight. Both spellings are established in this
  corpus's prose and 2.6:1 is not overwhelming.
- **Sourcery:** the private-repo upsell stub, as on every packet in this arc.
- **ZERO threads are open on this pull request at the ratified head.**

## 6. The landing obligation

**Rule 6 applies.** This pull request touches `openspec/changes/` and carries a
README OpenSpec Records entry, so lane `openxfactory-1` posts
`LANDING — lane openxfactory-1, session <id>, <UTC>, PR #757 into openxFactory
main` on the pull request and in `~/projects/xFactory/LANES.md` before the
merge, and `LANDED — lane openxfactory-1, <UTC>, PR #757 → <merge sha>` after
it. **The landing is the coordinator's act, not this author's.**

**The pull request is self-authored and is merged under the B2 provenance
pattern**: `gh` opens pull requests as `brettheap`, so a code-owner ruleset never
clears on Brett Heap's own click; the merge is an admin merge on his recorded
word — *"merge 72 when green, then ratify the A packet"*, #754 comment of
2026-09-07T14:27:55Z — quoted in the merge provenance. The pinned 1.12
entrypoint is green at the ratified head and the CI rollup is observed rather
than expected.
