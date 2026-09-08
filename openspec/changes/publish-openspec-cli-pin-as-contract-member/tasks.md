# Tasks: publish-openspec-cli-pin-as-contract-member

Status: ratified
Ratified by: publish-openspec-cli-pin-as-contract-member — 2026-09-07, Brett Heap, "merge 72 when green, then ratify the A packet" (record `review/ratification-2026-09-07.md`)
Kind: tasks

`code_surface: openxFactory` (two editorial files), `target_release: none`. The
realization group is § 4 and it is IN THIS PULL REQUEST: the tasks are
individually executable, so under `release-realization`'s decomposition rule this
packet realizes through its own task list rather than through a feature DAG.

**NOTHING IS TICKED THAT DID NOT LAND.** Every ticked box below is a diff in this
pull request or a measurement recorded verbatim in the pull request body.

**DISPOSITION 2026-09-08, AT THE ARCHIVE — THE SENTENCE ABOVE IS EXTENDED, NOT
SUPERSEDED, AND IT IS QUOTED IN PLACE RATHER THAN REWRITTEN.** *"Every ticked
box below is a diff in this pull request or a measurement recorded verbatim in
the pull request body"* was written of the RATIFICATION pull request
([#757](https://github.com/opensoft/openxFactory/pull/757)), where every box
then ticked was exactly that. **§ 5's nine ticks are added by the ARCHIVE pull
request**, and each is a diff in it, a measurement recorded verbatim in ITS
body, or the naming of a successor — which is what the next paragraph but one
already provides for. The first sentence, *"NOTHING IS TICKED THAT DID NOT
LAND"*, is **NOT** extended and needs no disposition: it still holds without
qualification, and the archive-time clauses in § 5 are what make it hold.

**§ 1 IS TICKED, AND IT NAMES WHAT DISCHARGED IT: ratification was GIVEN on
2026-09-07.** It ticked on Brett Heap's word, with the verbatim utterance, one
`Ratified`/`Ratified by` citation line added to each document, the approval pair
ADDED beside the drafting provenance in `.openspec.yaml` (`kind`, `id` and
`reason` never move), and the record at `review/ratification-2026-09-07.md` with
the verification run beside it at `review/verification-2026-09-07.md`.

**NO BOX IN § 5 IS WRITTEN TO STAY UNTICKED EITHER.** Under Brett Heap's ruling
of 2026-09-06T23:10Z, verbatim *"Tick on the recording"*, an owed successor's box
ticks once the successor is NAMED — a filed issue — with the box text saying the
tick records the naming and not the doing. Each § 5 box below states the issue it
will name. This matters mechanically: `scripts/proposal-support.py` refuses to
archive any change whose `tasks.md` still matches `^- \[ \]`, and there is no
bypass flag.

## 1. Ratification — GIVEN 2026-09-07

- [x] 1.1 **RATIFIED 2026-09-07 by Brett Heap** (openxFactory operator
      authority), in session, verbatim: *"merge 72 when green, then ratify the A
      packet"* — recorded on openxFactory issue
      [#754](https://github.com/opensoft/openxFactory/issues/754) at
      2026-09-07T14:27:55Z. The word's FIRST clause landed
      xFactory-Hermes-Install
      [#72](https://github.com/opensoft/xFactory-Hermes-Install/pull/72) as
      merge commit `06c9083d` at 14:42:30Z; its SECOND clause is this act.
      Brett Heap's two earlier rulings of 2026-09-07 on #754 — rollout *"Hybrid
      A+B"* and lane scope *"openxFactory only; siblings via their lanes"* —
      remain the ORIGIN and are still recorded as one: they admit this work and
      fix its scope, and they decide no wording here. **WHAT WAS DONE:**
      `proposal.md`, `design.md` and this file carry `Status: ratified` with
      **ONE** citation line each — `Ratified:` in `proposal.md`'s front matter,
      `Ratified by:` here and in `design.md` — which is what
      `ratified-provenance` counts; `.openspec.yaml` gains the approval pair
      (`approved_by`, `approved_on`) **BESIDE** the drafting provenance it was
      authored with, `kind`, `id` and `reason` unmoved, which is the
      addition-not-rewrite shape `add-drafted-proposal-origin` defined for this
      transition and the shape the archive gate's origin-retention arm reads.
      Record: `review/ratification-2026-09-07.md`, with the verification run
      captured beside it at `review/verification-2026-09-07.md`.
- [x] 1.2 **THE VETO POINTS WERE PUT AND NONE WAS TAKEN.** `design.md` **D1** —
      **A-defer** (register in the two editorial files, cut no bundle) against
      **A-cut** (register AND cut `contract-v3.5` here, with the annotated tag
      owed after the merge) — was carried in the pull request body, in this
      file, in `proposal.md` § Ratification and in the README row, with A-cut
      written out beside A-defer with its four costs and a third option,
      A-member, recorded as not taken rather than foreclosed. **A-defer is
      RATIFIED AS DESIGNED**, on the measurement in § 2: the derived release
      membership does not move (283 → 283), and both edited files are editorial
      members whose movement between cuts `release-surface-integrity` declares
      expected. **A-defer's COST is ratified with it**: the
      `contracts/CHANGELOG.md` entry naming this registered contract is OWED AT
      THE NEXT CUT (§ 5.7), this repository writing no `Unreleased` block by
      practice. **A-CUT WAS NOT CHOSEN**, so its conditional — that a cut, if
      chosen, becomes a realization task of this packet — does not arise: this
      pull request cuts nothing, allocates no version and owes no tag, and a cut
      remains an act on a word of Brett Heap's that has not been given.
      **A-member stands recorded as not taken**, unforeclosed. And `design.md`
      **D2** — the manifest row carrying no `sha256`, with the digest-bearing
      alternative and its cost written beside it — was carried separately so it
      could be vetoed on its own, and **was NOT vetoed either**: the row stands
      without a digest, and D2's residual coupling (the `consumption_rule`
      quotes the entrypoint path and nothing compares it with the pin's own
      `consumer_entrypoint:`) is ratified as DISCLOSED, owed at § 5.4.

## 2. The measurement, taken before the design

- [x] 2.1 **THE PIN IS REGISTERED NOWHERE, IN ANY OF THE THREE REGISTERS — ZERO
      OCCURRENCES IN EACH.** `git grep -c 'openspec-cli-pin' origin/main --`
      returns `0` for `contracts/README.md`, `0` for `contracts/manifest.yaml`
      and `0` for `contracts/releases/contract-v3.4.digests.yaml`, re-measured
      2026-09-07. **CORRECTED:** an earlier reading of this box said the string
      appeared in the manifest *"only inside prose comments belonging to the
      `openxwallet-pin` rows"* — it does not; that prose carries
      `openxwallet-pin.yaml`. The gap is total in all three registers rather than
      partial in one. Its two siblings, `contracts/openxwallet-pin.yaml` and
      `contracts/openreposhape-pin.yaml`, are in the same state — the pin CLASS
      has never been published.
- [x] 2.2 **RELEASE MEMBERSHIP IS A CLOSED SET AND THE MANIFEST'S `contracts:`
      LIST IS NOT ONE OF ITS SOURCES.**
      `scripts/hermes_runtime_validation/release.py::_collect_members` (`:532-745`)
      reads the hermes-runtime contract index, the fixture index,
      `scripts/hermes_runtime_validation/**`, four `NAMED_VALIDATORS`, seven
      `AUXILIARY_MEMBERS` and three `NORMATIVE_DOCS` (`:38-103`). The manifest is
      consulted for `contract_bundle_version` (`:587`) and the six
      intent-compliance registrations (`:601-616`) and for nothing else.
- [x] 2.3 **283 MEMBERS BEFORE, 283 AFTER; THE PIN IS IN NEITHER READING.**
      `release_membership(.)` run on this branch before and after the diff. The
      manifest and `contracts/README.md` ARE members, and are two of the exactly
      three editorial ones (`scripts/doc_health/release_inventory.py:57-67`). 283
      is also the entry count of `contracts/releases/contract-v3.4.digests.yaml`,
      so the declared bundle and the derived membership agree at this commit. The
      numbers are in the pull request body.
- [x] 2.4 **`contract-v3.4` IS PUBLISHED**, an annotated tag object peeling to
      commit `807a4f47` — the fact `release-tag-gate`'s `gate-findings` arm turns
      on, checked rather than assumed, because this diff touches
      `contracts/manifest.yaml` and therefore triggers that gate.
- [x] 2.5 **THE TWO LIVE CONSUMERS BOTH READ, NEITHER COPIES — AND OPSXFACTORY IS
      THE NORMAL CASE, NOT THE FALLBACK.** codexFactory
      `.github/workflows/validate.yml` resolves
      `stack.yaml['xfactory']['contract_ref']`, checks openxFactory out at that
      ref into `.openxfactory-pin`, and runs `scripts/validate-docs.sh` with
      `OPENXFACTORY_ROOT` pointing at it; that script invokes
      `$OPENX/scripts/validate-openspec-cli-pin.py`. OpsxFactory
      `.github/workflows/opsx-validation.yml` does the same into
      `scratchpad/openxfactory-pin-<sha12>` and invokes
      `"$OPSX_OPENSPEC_CLI_PIN_ENTRYPOINT" --repo . --all --strict`.
      **CORRECTED, AGAINST THE TREE.** An earlier reading of this box cited
      OpsxFactory's `contracts/openspec-cli-pin-consumption.yaml` as R1's
      FALLBACK realized. It is not, on four measured counts: OpsxFactory HAS an
      `xfactory:` stack pin (`contract_ref: 724a2a4f`); it copies NOTHING
      (`contracts/openspec-cli-pin.yaml` and `scripts/validate-openspec-cli-pin.py`
      both 404 in that repository); the consumption file records
      `commit_source: stack.yaml xfactory.contract_ref`, a POINTER rather than a
      copied-from commit, and `scripts/opsx_validation_gate.py` asserts
      statically that it declares no commit of its own; and its *"DECLARED
      DIVERGENCE"* is a divergence from OPSXFACTORY'S OWN ratified `design.md`
      § 4/§ 6 — an `npm ci` install of `@fission-ai/openspec@1.2.0` — TOWARD this
      pin, its governing change `advance-openxfactory-pin-and-fold-cli-pin`
      having gone in the RETIRE-THE-COPY direction. What that file actually is,
      and why it is worth citing under the NORMAL case instead: per-file SHA-256
      digests recomputed against the PINNED CHECKOUT before the entrypoint is
      executed, so the entrypoint that RAN is provably the entrypoint that was
      REVIEWED — a hardened read, and a precedent for others. The re-citation
      lands in `contracts/README.md`, `proposal.md`, this box and the pull
      request body.

## 3. The delta

- [x] 3.1 `specs/neutral-product-pin/spec.md`: **R1**, *A consumption pin that
      another repository reads is a PUBLISHED contract member, adopted by
      pin-sync* — registration in both registers; adoption riding the consumer's
      ordinary pin-sync; publishing the pin is not publishing the pinned product;
      read-from-the-pinned-checkout and never copy; and ONE admitted fallback for
      a repository with no stack pin, which must declare the commit it copied
      from, the digest of what it copied and the divergence it accepts, and must
      retire the copy on adopting a stack pin. **Plus the two clauses added in
      the three-lens fix round:** the PRECONDITION on the normal case — a
      consumer whose `contract_ref` predates the commit introducing the
      entrypoint cannot perform the read, published instructions name that
      commit, the remedy is to ADVANCE the pin and never to copy, and a gate
      meeting the absence REFUSES rather than skipping silently; and the
      RECONCILIATION with this capability's promoted requirement *A required
      check runs the pinned tool, at the pinned digest*, which forbids invoking
      an in-tree copy or a vendored duplicate — a required check wired off a
      declared copy leaves that enforcement claim UNMET until the copy is
      retired, so declaring makes the copy auditable and not lawful. **SEVEN
      scenarios** — four as first authored, a fifth (*The published instructions
      name a verb the entrypoint rejects*) added in bench round 2 on Codex's P1,
      and two added in the fix round (*The consumer's pinned ref predates the
      entrypoint*, *A required check is wired off a declared consumption copy*).
      This box previously read *"four scenarios"* and had not been re-counted
      after round 2; it is re-counted against the file here.
- [x] 3.2 `specs/neutral-product-pin/spec.md`: **R2**, *Registering a pin in the
      consumption register is not a bundle cut unless it moves the release
      membership* — the mechanical test, the two outcomes, and the obligation on
      the registering author to RECORD the derived membership before and after,
      so that "no cut is owed" is measured rather than asserted. Three scenarios.
- [x] 3.3 **NO `## MODIFIED` AND NO `## REMOVED`** (`design.md` D4). The
      requirement a modification would land on is under an ACTIVE `## MODIFIED`
      block held by `add-openspec-cli-pin`, which has not archived; a second
      block over that title would have to restate either promoted text that
      contradicts the pending one or pending text this repository does not yet
      hold. Both new titles are new, so no partner row flips in the corpus
      ledger.
- [x] 3.4 `sequenced_after: [add-openspec-cli-pin]` declared in `proposal.md`'s
      front matter — the ordering claim stated rather than left to reading order:
      R1 and R2 stand on the pin file that change lands. **THE SECOND ENTRY WAS
      ATTEMPTED AND IS UNWRITEABLE**, which is § 5.6's finding:
      `scripts/validate-sequenced-after.py` refuses any entry whose change-id
      half does not match `^[a-z0-9][a-z0-9-]*$`, and
      `bump-openspec-cli-pin-to-1.12`'s own id carries a `.`, so no change in
      this repository can be sequenced behind it by any spelling. Measured by
      writing the entry and reading the refusal, not inferred.

## 4. The realization — in this pull request

- [x] 4.1 `contracts/manifest.yaml`: ONE row, `id: openspec-cli-pin`,
      `path: contracts/openspec-cli-pin.yaml`, `type: pin` (`design.md` D3),
      `adapter_owner: openxFactory`,
      `compatibility: canonical_openxfactory_contract`, `intended_consumers`, and
      a `consumption_rule` written on `domain-factory-conformance-validator`'s
      precedent (`contracts/manifest.yaml:184-199`): invoke the entrypoint from
      the checkout at `stack.yaml`'s `xfactory.contract_ref`; copying is a
      conformance violation. **No `sha256`** (`design.md` D2). No other row is
      touched and `contract_bundle_version` does not move.
- [x] 4.2 `contracts/README.md`: the matching row in *Native openxFactory
      contracts*, naming what the pin is, what it is NOT (openxFactory does not
      own the CLI), and the entrypoint it names.
- [x] 4.3 `contracts/README.md`: the new consumer-facing section **Gating
      archives on the pinned CLI from a consumer repository** — the FOUR-step
      checkout-at-`contract_ref` recipe (steps 1-3 are the shape codexFactory and
      OpsxFactory already run), the never-copy rule, and the declared copy-in
      fallback for a repository with no stack pin (B of #754), citing #754.
      **STEP 4 EXISTS BECAUSE THE FIRST DRAFT'S ARCHIVE INSTRUCTION WAS NOT
      EXECUTABLE**, found by Codex's P1 on this pull request and verified against
      the tools: `validate-openspec-cli-pin.py --help` offers `--all`/`--change`
      and rejects `archive <id>` as an unrecognized argument, and the archive act
      runs through `scripts/proposal-support.py <root> archive <change>`, which
      imports that entrypoint's resolver and invokes the resolved binary. The
      section now names BOTH commands and says which act each performs; R1 gains
      the clause and the scenario that make it canon rather than a local fix.
      **AND THE FIX ROUND MADE STEP 1 EXECUTABLE, which it was not.** The recipe
      as first written could not run where the consumer's `contract_ref`
      PREDATES `1d8cd54e` (2026-09-04), the commit that first carries
      `scripts/validate-openspec-cli-pin.py`: measured 2026-09-07, MedxFactory
      and AdxFactory pin `6c03d783` (2026-08-06) and LedgerxFactory pins
      `af7ac0fa` (2026-08-27), and the entrypoint is absent from all three, so a
      literal reader gets a missing-file error and falls back to the ambient
      `openspec` — the Codex-P1 failure class in a second guise. Step 1 now
      carries the precondition, the three named consumers behind it, the
      advance-your-pin remedy, and codexFactory's
      `scripts/validate-docs.sh:162` guard as the shape of a lawful refusal;
      step 2's *"both live consumers use exactly this name"* is corrected —
      codexFactory uses `OPENXFACTORY_ROOT`, OpsxFactory uses
      `OPSX_PINNED_OPENXFACTORY_CHECKOUT` / `OPSX_OPENSPEC_CLI_PIN_ENTRYPOINT`,
      and the name is the consumer's while the seam is the checkout; and the
      fallback subsection is re-cited (§ 2.5) with the promoted-requirement
      price stated.
- [x] 4.4 **`contracts/openspec-cli-pin.yaml` IS NOT EDITED** (`design.md` D7) —
      no version, no digest, no `rollback:`, no `dispositions:` entry — and no
      script and no workflow is edited. Publishing a pin and moving a pin are
      different acts with different authorities, and nothing here may be read as
      approving a bump.
- [x] 4.5 `README.md`: the OpenSpec Records row for this active change, carrying
      the D1 veto point in the same words as § 1.2.
- [x] 4.6 `tests/sequenced_after/corpus-ledger.yaml`: this change's row seeded
      with `--seed-ledger --moved-by '#<PR>'` after the pull request exists, and
      the diff read to confirm it is this row and no other.

## 5. Owed, and deliberately not taken here

**DISPOSITION 2026-09-08 — WHAT THIS ARCHIVE ADDED TO THIS SECTION, AND WHAT IT
DID NOT.** Every box below is ticked, and **the ruling used is the one the
header of this file already named**: Brett Heap, 2026-09-06T23:10Z, in session,
by multiple choice, the option labelled verbatim *"Tick on the recording"* — an
owed successor's box ticks once the successor is NAMED, with the box text saying
the tick records the naming and not the doing. Nothing in that ruling is
superseded and nothing in this section's ratified text is deleted: **the
ratified text of every box is carried VERBATIM beneath its archive-time
clause.**

**THE NINE TICKS ARE OF FOUR KINDS, AND EACH BOX SAYS WHICH IT IS.** § 5.1 and
§ 5.5 tick **ON THE EVIDENCE** — landed merge commits, and the ratification plus
two green `pytest-suite` runs on `main` commits MEASURED to contain it. § 5.2
ticks on a record that **already exists**, openxFactory
[#754](https://github.com/opensoft/openxFactory/issues/754), which stays OPEN as
the rollout's governing tracker; no second issue is filed for it, a second
tracker forking the record it would be filed to carry. § 5.3, § 5.4, § 5.6,
§ 5.7 and § 5.9 tick on **FIVE ISSUES FILED AT THIS ARCHIVE, ALL UNCLAIMED** —
openxFactory [#775](https://github.com/opensoft/openxFactory/issues/775),
[#776](https://github.com/opensoft/openxFactory/issues/776),
[#777](https://github.com/opensoft/openxFactory/issues/777),
[#778](https://github.com/opensoft/openxFactory/issues/778) and
[#779](https://github.com/opensoft/openxFactory/issues/779). And § 5.8 ticks
**ON THE DOING**: the `neutral-product-pin` Purpose widening it declared owed AT
THE ARCHIVE is taken here, as one disclosed sentence in a hunk separate from the
promotion.

**NO TICK IN THIS SECTION CLAIMS WORK THAT WAS NOT DONE.** No sibling repository
is adopted from this lane; no checker is written; no grammar is widened and no
change is renamed; no release is cut and no version is allocated or reserved;
`contracts/openspec-cli-pin.yaml` is not edited; and the per-file digest owed on
xFactory-Hermes-Install is named as owed rather than counted as met. All five
issues above are **open and unclaimed at this commit**.

**THE RATIFICATION RECORD IS NOT EDITED.** `review/ratification-2026-09-07.md`
is `Status: record` — immutable, untouched, standing exactly as written,
including its § 4 enumeration of this whole residue. Its § 4 item 5 anticipated
this act in terms: *"THE ARCHIVE IS A SEPARATE ACT … This word ratifies; it does
not archive."* Its § 4 item 8 anticipated § 5.8's edit in the same way: the
Purpose widening *"belongs in the archive act, where the spec file is
rewritten"*.

- [x] 5.1 **TICKED ON THE EVIDENCE, NOT ON A NAMING — ROLLOUT B IS COMPLETE,
      THREE OF THREE, AND ITS ONE SHORTFALL IS NAMED RATHER THAN COUNTED AS
      MET.** All three no-lane repositories landed their copy-in on 2026-09-07,
      each on a word of Brett Heap's, and each is cited by MERGE COMMIT:
      xFactory-Hermes-Install **#72** -> `06c9083d` (14:42:30Z); openXwallet
      **#21** -> `b7c6e0b8` (16:37:10Z), preceded by its 1.12 readiness **#23**
      -> `5f36486c` (16:31Z) and carrying the vendored tarball on the ruling
      *"Vendor the tarball into the repo"*; Omnigent-Install **#241** ->
      `47454e0a` (16:57:14Z), preceded by its readiness **#245** -> `8c42bdfe`
      (16:23:24Z). Recorded on
      [#754](https://github.com/opensoft/openxFactory/issues/754) at
      2026-09-07T16:57:43Z, where the rollout is called COMPLETE, 3 of 3, every
      gate green on its own repository's corpus under the pinned 1.12.0. **WHAT
      THIS TICK DOES NOT CLAIM, and the ratified text below already said it:**
      the Hermes copy's per-file `sha256` — R1's THIRD field — is **STILL OWED
      on xFactory-Hermes-Install**, is that repository's act and not this
      lane's, and stands on #754's record of 19:22:36Z as owed and unclaimed.
      Making `openspec-cli-pin` a REQUIRED check in each of the three is Brett
      Heap's console act and is likewise not done here. The ratified text
      follows unchanged:
      **B OF #754 — THE THREE NO-LANE REPOSITORIES.** Omnigent-Install,
      openXwallet and xFactory-Hermes-Install carry no `xfactory:` stack pin and
      archive on whatever `openspec` is on PATH; R1's fallback scenario is what
      their copy-in must satisfy. It is separate work, in separate repositories,
      with its own claims on their governing issues, and this packet performs
      none of it. **This box ticks on the recording** — when the three pull
      requests (or the issue that tracks them) are named here — per the
      *"Tick on the recording"* ruling; the tick will record the naming, not the
      doing. **ONE OF THE THREE LANDED WHILE THIS PACKET WAS IN REVIEW, and its
      shortfall is named rather than smoothed:** xFactory-Hermes-Install PR
      [#72](https://github.com/opensoft/xFactory-Hermes-Install/pull/72), merged
      `06c9083d` on 2026-09-07, is the estate's FIRST declared copy. It carries
      two of R1's three fields — the openxFactory commit copied from
      (`44d8fbaf`, in a vendoring header on each of the three copied files) and
      the divergence accepted (three `uses:` commit-SHA pins in the adapted
      workflow; governed archive routing deferred, `scripts/proposal-support.py`
      not being vendored). **The digest of what it copied is NOT recorded** — it
      asserts byte-identity below the header and ships a `diff` recipe against
      the named commit in place of a per-file `sha256`. That is a real check and
      it is not the field R1 names, so **the digest is OWED on
      xFactory-Hermes-Install**, is that repository's act and not this lane's,
      and is stated here as owed rather than counted as met.

- [x] 5.2 **TICKED ON THE RECORDING — THE ESTATE-WIDE ADOPTION TRACKER IS
      [#754](https://github.com/opensoft/openxFactory/issues/754) ITSELF, WHICH
      STAYS OPEN, AND NO NEW ISSUE IS FILED BECAUSE A SECOND TRACKER WOULD FORK
      THE RECORD.** Per Brett Heap's ruling of 2026-09-06, verbatim *"Tick on
      the recording"*: the box ticks once the successor is NAMED, and this
      clause is the box text saying the tick records the naming and not the
      doing. #754's comment of 2026-09-07T19:22:36Z is that record and it
      ENUMERATES what is owed and unclaimed — the three stack-pin consumers
      standing BEHIND the entrypoint commit `1d8cd54e`, **MedxFactory and
      AdxFactory at `6c03d783`, LedgerxFactory at `af7ac0fa`**, which advance
      their pins through their own lanes and which is R1's ratified
      PRECONDITION rather than a defect in those repositories; **OpsxFactory's
      shadow gate** becoming required; **the Hermes copy's per-file digest**;
      and the openxFactory tooling follow-ons. **NO SIBLING ADOPTION IS
      PERFORMED FROM THIS LANE**, by Brett Heap's ruling of 2026-09-07,
      verbatim *"openxFactory only; siblings via their lanes"*. The ratified
      text follows unchanged:
      **EVERY OTHER SIBLING'S ADOPTION BELONGS TO ITS OWN LANE**, by #754's
      second ruling: OpsxFactory's shadow gate becoming required (four live
      lanes), MedxFactory / AdxFactory / LedgerxFactory (their owners), the
      openDox family (lane `openXfactory-4`). Named so the omission reads as
      scope rather than oversight. **This box ticks on the recording** of the
      issue that carries the estate-wide adoption tracker, and the tick will
      record the naming.

- [x] 5.3 **TICKED ON THE RECORDING — THE SUCCESSOR IS openxFactory
      [#775](https://github.com/opensoft/openxFactory/issues/775), FILED AT
      THIS ARCHIVE AND UNCLAIMED, AND NEITHER SIBLING PIN IS REGISTERED BY THIS
      ACT.** Per Brett Heap's ruling of 2026-09-06, verbatim *"Tick on the
      recording"*: the box ticks once the successor is NAMED, and this clause
      is the box text saying the tick records the naming and not the doing.
      #775 carries the measurement RE-TAKEN at this archive's base `bd263dca` —
      `contracts/manifest.yaml` holds **206 rows and exactly ONE of `type:
      pin`**, `openspec-cli-pin`; **neither** `contracts/openxwallet-pin.yaml`
      **nor** `contracts/openreposhape-pin.yaml` has a `contracts:` row; the
      wallet pin's two `contracts/README.md` occurrences are a HISTORICAL row
      recording its REMOVAL from the manifest at `contract-v2.0` rather than a
      registration, and the openRepoShape pin has **zero** occurrences there —
      and it carries the reason a sweep was refused: R1's predicate is per pin
      and unmeasured for these two, one pinning a MOUNTED product and the other
      a CITED one that its own header says openxFactory *"does not MOUNT"*.
      **#775 picks no wording and no shape**, and asks each pin's reading
      first. The ratified text follows unchanged:
      **THE TWO SIBLING PINS ARE UNREGISTERED TOO** —
      `contracts/openxwallet-pin.yaml` and `contracts/openreposhape-pin.yaml`,
      measured in § 2.1. R1 reaches them by its own terms wherever another
      repository reads them, and neither is registered by this packet: each needs
      its own reading of who reads it and on what terms, and a packet that swept
      three pins into one row-block would be asserting three consumption rules on
      one word. **This box ticks on the recording** of the successor issue that
      names them, and the tick will record the naming.

- [x] 5.4 **TICKED ON THE RECORDING — THE SUCCESSOR IS openxFactory
      [#776](https://github.com/opensoft/openxFactory/issues/776), FILED AT
      THIS ARCHIVE AND UNCLAIMED, AND NO CHECKER IS WRITTEN HERE.** Per Brett
      Heap's ruling of 2026-09-06, verbatim *"Tick on the recording"*: the box
      ticks once the successor is NAMED, and this clause is the box text saying
      the tick records the naming and not the doing. #776 carries BOTH owed
      assertions and **re-verifies the second against the tree at this
      archive's base** rather than restating it: the ONLY comparison of
      `consumer_entrypoint:` against anything in this repository is
      `tests/proposal-support/test_pinned_openspec_cli.py:275`, which asserts
      `support.PIN_VERIFIER == ROOT / real_pin["consumer_entrypoint"]` —
      **`proposal-support`'s own constant against the PIN, not the MANIFEST ROW
      against the pin** — so that test stays green through exactly the failure
      this assertion exists to catch. #776 leaves the finding class, how *"is
      read"* is decided, and whether the second assertion compares a string or
      resolves a path **deliberately unpicked**, each needing its own reading.
      The ratified text follows unchanged:
      **A REGISTRATION IS NOT A CHECK, AND THE ROW'S ONE RESIDUAL COUPLING IS
      UNVERIFIED.** Nothing in this repository asserts that a pin another
      repository reads IS registered — R1 states the obligation, and `doc-health`
      has no family that reads it. **AND THE SAME CHECKER OWES A SECOND
      ASSERTION**, which is D2's residual coupling stated plainly: the manifest
      row's `consumption_rule` QUOTES the path
      `scripts/validate-openspec-cli-pin.py`, the pin file names that same path
      in its own `consumer_entrypoint:` field, and **nothing compares the two** —
      a rename that moved the pin and not the row would leave the register
      quoting a path that does not exist, silently. Declining the per-file
      digest (D2) does not remove that coupling; it makes it one string wide
      instead of one file wide. Both assertions belong in a checker beside
      `release-inventory-drift` rather than inside it, and neither is written
      here. **This box ticks on the recording** of the successor issue that
      proposes it, and the tick will record the naming.

- [x] 5.5 **TICKED ON THE ARCHIVE EVIDENCE, BOTH HALVES CITED RATHER THAN
      ASSERTED, AND ON A WORD DISTINCT FROM THE RATIFICATION.** **RATIFIED AND
      LANDED:** PR [#757](https://github.com/opensoft/openxFactory/pull/757) ->
      merge commit **`a5940811`**, 2026-09-07T19:22:23Z; ratifying commit
      **`05a9db8b`**; records `review/ratification-2026-09-07.md` and
      `review/verification-2026-09-07.md`, both `Status: record` and both
      untouched by this archive. **GREEN ON MAIN, TWICE, WITH CONTAINMENT
      MEASURED RATHER THAN ASSUMED:** `pytest-suite` run **34159620759**,
      conclusion **`success`**, `headSha` **`7992b87a`**; and run
      **34173088424**, conclusion **`success`**, `headSha` **`bd263dca`**,
      which is this branch's base. `gh api
      repos/opensoft/openxFactory/compare/a5940811...<sha>` answers `ahead`
      with **`behind_by: 0`** for both (7 and 12 commits ahead), so each is a
      `main` commit CONTAINING the merge rather than merely later than it.
      **THE SEPARATE WORD IS BRETT HEAP'S**, 2026-09-07, in session, verbatim
      **"archive the A packet when green"**, recorded and claimed on
      [#754](https://github.com/opensoft/openxFactory/issues/754) — and **this
      is that act**. The ratified text follows unchanged:
      **ARCHIVE — NOT TAKEN, AND ON A SEPARATE WORD.** `code_surface` is
      non-empty, so under `release-realization` this packet archives on
      merged-plus-green realization evidence rather than on landing, and on a
      word distinct from the ratification. This box ticks when both halves exist
      and are CITED rather than asserted — the merge commit on `main` and the
      workflow run id of a green required suite at that commit.

- [x] 5.6 **TICKED ON THE RECORDING — THE SUCCESSOR IS openxFactory
      [#777](https://github.com/opensoft/openxFactory/issues/777), FILED AT
      THIS ARCHIVE AND UNCLAIMED, AND NONE OF THE THREE EXITS IS TAKEN.** Per
      Brett Heap's ruling of 2026-09-06, verbatim *"Tick on the recording"*:
      the box ticks once the successor is NAMED, and this clause is the box
      text saying the tick records the naming and not the doing. #777
      re-measures the grammar at this archive's base —
      `scripts/sequenced_after.py:174`, `CHANGE_ID =
      re.compile(r"^[a-z0-9][a-z0-9-]*$")` — and finds the class is **TWO
      active changes rather than one**: `bump-openspec-cli-pin-to-1.12`, which
      this box names, **and `prepare-openspec-1.12-readiness` beside it**. It
      records all three exits with their costs — the widening reaching a second
      grammar (`scripts/doc_health/modified_block_currency.py:588`) and the
      recorded decision O7 behind it, the rename moving a ratified change's
      identity, and the prose status quo made explicit — and **picks none**,
      exactly as the ratifying word did. The ratified text follows unchanged:
      **A CHANGE ID THAT NO `sequenced_after:` CAN NAME.**
      `bump-openspec-cli-pin-to-1.12` is an ACTIVE change whose id contains a
      `.`, and the substrate's grammar (`^[a-z0-9][a-z0-9-]*$`, enforced by
      `scripts/validate-sequenced-after.py`) admits no such id — so no change in
      this repository, or in any repository declaring a cross-repository entry,
      can order itself behind it. Found by attempting the declaration in this
      packet. The honest exits are three and none is taken here: widen the
      grammar, rename the change (a directory move with its own archive
      consequences), or record the ordering in prose and accept that no machine
      reads it. **This box ticks on the recording** of the successor issue that
      names the choice, and the tick will record the naming.

- [x] 5.7 **TICKED ON THE RECORDING — THE OBLIGATION IS CARRIED FORWARD AS
      openxFactory [#778](https://github.com/opensoft/openxFactory/issues/778),
      FILED AT THIS ARCHIVE AND UNCLAIMED, AND NO RELEASE IS CUT AND NO VERSION
      IS ALLOCATED OR RESERVED HERE.** Per Brett Heap's ruling of 2026-09-06,
      verbatim *"Tick on the recording"*: the box ticks once the successor is
      NAMED, and this clause is the box text saying the tick records the naming
      and not the doing. #778 is addressed to **whoever takes the NEXT CUT** —
      the obligation is the cutter's, not this lane's — and it carries what
      that session would otherwise re-derive: the registered row's identity,
      the fact that it bears **no per-file `sha256`** (`design.md` **D2**) and
      is therefore a register row rather than a digest member, R2 as the rule
      governing the reading, and the atomicity clause's discharge, the diff
      having added no contract FILE because the pin file already existed on
      `main` and is untouched per **D7**. The ratified text follows unchanged:
      **THE `contracts/CHANGELOG.md` ENTRY IS OWED AT THE NEXT CUT.**
      `docs/contract-versioning-policy.md` § *Change Classes* grades *"new
      contracts"* as **Additive (minor)**, and § *Version Identity* item 5
      requires the changelog to carry *"one entry per release listing every
      contract added, changed, or deprecated"*. This packet registers a contract
      and cuts no release, so the entry has no release to be written into today:
      this repository writes no `Unreleased` block by practice (the changelog is
      headed at `contract-v3.4`, and its cut records state that no `Unreleased`
      block is pending), and allocating a version to create one IS A-cut, which
      is not this lane's act. **So the entry is owed at the NEXT CUT**, whoever
      takes it, and it is recorded here rather than left for that session to
      re-derive: the release entry that follows this merge must list
      `contracts/openspec-cli-pin.yaml` among the contracts the bundle carries.
      The § *Version Identity* atomicity clause — *"the manifest and changelog
      update SHALL be committed atomically with the contract files"* — is not
      breached by the deferral: this diff adds no contract FILE (the pin file
      already exists on `main` and is untouched, `design.md` D7), only its
      register row, and the membership/digest accounting of D1 is unmoved by a
      changelog line. **This box ticks on the recording** of the cut, or of the
      issue that carries it, and the tick will record the naming.

- [x] 5.8 **TICKED ON THE DOING — AND THIS IS THE ONE BOX IN THIS SECTION WHOSE
      TICK RECORDS WORK PERFORMED HERE RATHER THAN A NAMING.** The widening is
      TAKEN IN THIS ARCHIVE, as **ONE SENTENCE** appended to
      `openspec/specs/neutral-product-pin/spec.md`'s `## Purpose`, written from
      R1's and R2's own words and **mirroring the file's own precedent
      construction** — *"It also carries the reverse direction — …"*, which is
      how that Purpose already names its second direction. The sentence is
      quoted here in full so the edit is on the record and not merely in a
      diff: *"And it carries a THIRD direction, in which openxFactory is the
      PUBLISHER of its own consumption claim: a consumption pin that another
      repository reads is a PUBLISHED contract member — registered in
      `contracts/manifest.yaml`, indexed in `contracts/README.md`, adopted by
      the consumer's ordinary pin-sync and read from the pinned checkout rather
      than copied — together with the accounting of what such a registration
      does and does not move, an act on the consumption register and not a
      bundle cut unless it moves the closed release membership."* **IT IS A
      SEPARATE HUNK FROM THE PROMOTION**, taken AFTER
      `scripts/proposal-support.py … archive` had written the two ADDED
      requirements into canon, so the serializer's output and this editorial
      sentence are visibly distinct in the diff. **NOTHING ELSE IN THE `##
      Purpose` BLOCK IS TOUCHED** — no existing clause is reworded, reordered
      or removed — and **no promoted requirement's text is edited by it**. The
      ratified text follows unchanged:
      **`neutral-product-pin`'s PURPOSE WILL NEED WIDENING AT ARCHIVE.** The
      promoted Purpose frames the capability in ONE direction — *"Govern
      openxFactory's consumption of an EXTERNAL neutral product, the direction in
      which it is the consumer rather than the publisher"* — with one reverse
      clause for a neutral product vendoring an openxFactory contract. R1 adds a
      third direction the Purpose does not describe: openxFactory PUBLISHING its
      own consumption pin as a contract member that other repositories read and
      adopt by pin-sync. A promoted spec whose Purpose does not name a
      requirement it carries is a Purpose that has fallen behind its own
      requirements, so the widening belongs in the ARCHIVE act (§ 5.5) — where
      the deltas promote and the spec file is rewritten — and not in the delta,
      which carries requirements rather than the Purpose block. **This box ticks
      on the recording** of that obligation in the archive act, and the tick will
      record the naming, not the doing.

- [x] 5.9 **TICKED ON THE RECORDING — THE SUCCESSOR IS openxFactory
      [#779](https://github.com/opensoft/openxFactory/issues/779), FILED AT
      THIS ARCHIVE AND UNCLAIMED, AND `contracts/openspec-cli-pin.yaml` IS NOT
      EDITED BY THIS ARCHIVE ANY MORE THAN IT WAS BY THE RATIFICATION.** Per
      Brett Heap's ruling of 2026-09-06, verbatim *"Tick on the recording"*:
      the box ticks once the successor is NAMED, and this clause is the box
      text saying the tick records the naming and not the doing. #779 quotes
      the header claim VERBATIM from the comment block above
      `consumer_entrypoint:` (`:248`), records that the packet corrected the
      identical claim in its four carriers while `design.md` **D7** forbade
      touching the fifth, states R1's promoted clause that reaches it — *"WHERE
      THE TWO GOVERNED ACTS ARE REACHED BY TWO DIFFERENT COMMANDS, THE REGISTER
      SHALL NAME BOTH"* — and **bounds the remedy**: the text at issue is a
      COMMENT above the field, no key, digest, version or disposition moves,
      and nothing in it proposes moving the pin. Whether the correction rides
      an existing change of the pin's family or needs its own is **that
      family's call and is not decided here**. The ratified text follows
      unchanged:
      **THE PIN FILE'S OWN HEADER CARRIES THE UNEXECUTABLE CLAIM TOO, AND
      THIS PACKET MAY NOT FIX IT.** Codex's P1 and Copilot's two follow-ups found
      the "route archive through the entrypoint" claim in this packet's four
      carriers, and all four are corrected. The SAME claim stands in
      `contracts/openspec-cli-pin.yaml` itself, above `consumer_entrypoint:`
      (*"Every repository in the estate runs STRICT OpenSpec validation and every
      OpenSpec ARCHIVE through this entrypoint and through nothing else"*), and
      that file is NOT this packet's surface — `design.md` D7 refuses to edit it,
      and nothing here may be read as approving any edit to it. R1's
      register-names-both-commands clause reaches it by its own terms, so it is a
      DEFECT OWED on the pin, belonging to a successor in the pin's own change
      family (`add-openspec-cli-pin` / `bump-openspec-cli-pin-to-1.12`), not to
      this one. **This box ticks on the recording** of the successor issue that
      names it, and the tick will record the naming.
