# Tasks: publish-openspec-cli-pin-as-contract-member

Status: draft
Kind: tasks

`code_surface: openxFactory` (two editorial files), `target_release: none`. The
realization group is § 4 and it is IN THIS PULL REQUEST: the tasks are
individually executable, so under `release-realization`'s decomposition rule this
packet realizes through its own task list rather than through a feature DAG.

**NOTHING IS TICKED THAT DID NOT LAND.** Every ticked box below is a diff in this
pull request or a measurement recorded verbatim in the pull request body.

**§ 1 IS NOT TICKED, AND IT NAMES WHY: ratification has not happened.** It is not
a box written never to tick — it ticks on Brett Heap's word, with the verbatim
utterance, one `Ratified`/`Ratified by` citation line added to each document, the
approval pair ADDED beside the drafting provenance in `.openspec.yaml` (`kind`
and `id` never move), and a record at `review/ratification-<date>.md`.

**NO BOX IN § 5 IS WRITTEN TO STAY UNTICKED EITHER.** Under Brett Heap's ruling
of 2026-09-06T23:10Z, verbatim *"Tick on the recording"*, an owed successor's box
ticks once the successor is NAMED — a filed issue — with the box text saying the
tick records the naming and not the doing. Each § 5 box below states the issue it
will name. This matters mechanically: `scripts/proposal-support.py` refuses to
archive any change whose `tasks.md` still matches `^- \[ \]`, and there is no
bypass flag.

## 1. Ratification — OWED, NOT GIVEN

- [ ] 1.1 **RATIFICATION IS OWED AND NOTHING HERE PERFORMS IT.** Brett Heap's two
      rulings of 2026-09-07 on openxFactory issue
      [#754](https://github.com/opensoft/openxFactory/issues/754) — rollout
      *"Hybrid A+B"* and lane scope *"openxFactory only; siblings via their
      lanes"* — admit this work and fix its scope. They decide no wording, take
      no design decision and ratify no requirement. `.openspec.yaml` carries
      drafting provenance ONLY, with no `approved_by` and no `approved_on`, the
      lawful unapproved shape `add-drafted-proposal-origin` defined; every
      document in this packet carries `Status: draft` to match.
- [ ] 1.2 **THE VETO POINT IS `design.md` D1** — **A-defer** (register in the two
      editorial files, cut no bundle) against **A-cut** (register AND cut
      `contract-v3.5` here, with the annotated tag owed after the merge).
      A-defer is designed, on the measurement in § 2: the derived release
      membership does not move, and both edited files are editorial members whose
      movement between cuts `release-surface-integrity` declares expected.
      A-cut is written out beside it with four costs and a third option, A-member,
      is recorded as not taken rather than foreclosed. **A CUT IS NOT THIS
      LANE'S ACT.** If A-cut is chosen, the cut becomes a realization task of this
      packet — ticked when it is done, by whoever is told to do it — and this
      pull request performs none of it. A second, smaller veto point is
      `design.md` **D2**: the manifest row carries no `sha256`, with the
      digest-bearing alternative and its cost written beside it.

## 2. The measurement, taken before the design

- [x] 2.1 **THE PIN IS REGISTERED NOWHERE, IN ANY OF THE THREE REGISTERS.**
      `contracts/README.md`: zero occurrences. `contracts/manifest.yaml`: the
      string appears only inside prose comments belonging to the `openxwallet-pin`
      rows. `contracts/releases/contract-v3.4.digests.yaml`: absent. Its two
      siblings, `contracts/openxwallet-pin.yaml` and
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
- [x] 2.5 **THE TWO LIVE CONSUMERS BOTH READ, NEITHER COPIES.** codexFactory
      `.github/workflows/validate.yml` resolves
      `stack.yaml['xfactory']['contract_ref']`, checks openxFactory out at that
      ref into `.openxfactory-pin`, and runs `scripts/validate-docs.sh` with
      `OPENXFACTORY_ROOT` pointing at it; that script invokes
      `$OPENX/scripts/validate-openspec-cli-pin.py`. OpsxFactory
      `.github/workflows/opsx-validation.yml` does the same into
      `scratchpad/openxfactory-pin-<sha12>` and invokes
      `"$OPSX_OPENSPEC_CLI_PIN_ENTRYPOINT" --repo . --all --strict`. OpsxFactory
      additionally carries `contracts/openspec-cli-pin-consumption.yaml`, a
      DECLARED DIVERGENCE — which is the shape R1's fallback scenario
      generalizes, taken from a realized precedent rather than invented.

## 3. The delta

- [x] 3.1 `specs/neutral-product-pin/spec.md`: **R1**, *A consumption pin that
      another repository reads is a PUBLISHED contract member, adopted by
      pin-sync* — registration in both registers; adoption riding the consumer's
      ordinary pin-sync; publishing the pin is not publishing the pinned product;
      read-from-the-pinned-checkout and never copy; and ONE admitted fallback for
      a repository with no stack pin, which must declare the commit it copied
      from, the digest of what it copied and the divergence it accepts, and must
      retire the copy on adopting a stack pin. Four scenarios.
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
      archives on the pinned CLI from a consumer repository** — the three-step
      checkout-at-`contract_ref` recipe as codexFactory and OpsxFactory already
      run it, the never-copy rule, and the declared copy-in fallback for a
      repository with no stack pin (B of #754), citing #754.
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

- [ ] 5.1 **B OF #754 — THE THREE NO-LANE REPOSITORIES.** Omnigent-Install,
      openXwallet and xFactory-Hermes-Install carry no `xfactory:` stack pin and
      archive on whatever `openspec` is on PATH; R1's fallback scenario is what
      their copy-in must satisfy. It is separate work, in separate repositories,
      with its own claims on their governing issues, and this packet performs
      none of it. **This box ticks on the recording** — when the three pull
      requests (or the issue that tracks them) are named here — per the
      *"Tick on the recording"* ruling; the tick will record the naming, not the
      doing.
- [ ] 5.2 **EVERY OTHER SIBLING'S ADOPTION BELONGS TO ITS OWN LANE**, by #754's
      second ruling: OpsxFactory's shadow gate becoming required (four live
      lanes), MedxFactory / AdxFactory / LedgerxFactory (their owners), the
      openDox family (lane `openXfactory-4`). Named so the omission reads as
      scope rather than oversight. **This box ticks on the recording** of the
      issue that carries the estate-wide adoption tracker, and the tick will
      record the naming.
- [ ] 5.3 **THE TWO SIBLING PINS ARE UNREGISTERED TOO** —
      `contracts/openxwallet-pin.yaml` and `contracts/openreposhape-pin.yaml`,
      measured in § 2.1. R1 reaches them by its own terms wherever another
      repository reads them, and neither is registered by this packet: each needs
      its own reading of who reads it and on what terms, and a packet that swept
      three pins into one row-block would be asserting three consumption rules on
      one word. **This box ticks on the recording** of the successor issue that
      names them, and the tick will record the naming.
- [ ] 5.4 **A REGISTRATION IS NOT A CHECK.** Nothing in this repository asserts
      that a pin another repository reads IS registered — R1 states the
      obligation, and `doc-health` has no family that reads it. A checker would
      belong beside `release-inventory-drift` rather than inside it, and it is
      not written here. **This box ticks on the recording** of the successor
      issue that proposes it, and the tick will record the naming.
- [ ] 5.5 **ARCHIVE — NOT TAKEN, AND ON A SEPARATE WORD.** `code_surface` is
      non-empty, so under `release-realization` this packet archives on
      merged-plus-green realization evidence rather than on landing, and on a
      word distinct from the ratification. This box ticks when both halves exist
      and are CITED rather than asserted — the merge commit on `main` and the
      workflow run id of a green required suite at that commit.
- [ ] 5.6 **A CHANGE ID THAT NO `sequenced_after:` CAN NAME.**
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
