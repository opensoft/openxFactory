# Tasks: add-per-tenant-app-manifest-provisioning

## 1. The packet (THIS PULL REQUEST)

- [x] 1.1 `.openspec.yaml` declaring `kind: staged`, the fragment's path, the
  exit-precondition measurement (Q1 RULED by `5704187317`; Q2 unruled and not
  needed, with the case-neutrality reason stated), and `approved_by` recording
  that the ruling authorizes AUTHORING and is not ratification.
- [x] 1.2 `proposal.md` with the realization-axis front matter — `code_surface:
  none` with its four measured negatives, `target_release: implemented` with the
  reason NO bundle number is reserved (the two active siblings on this capability
  each owe an additive minor on the same schema file).
- [x] 1.3 `design.md`: D1 why the growth goes ON the requirement, D2 the
  shape/runbook line and its one deliberate exception, D3 case-neutrality against
  the unruled Q2, D4 why the naming convention is a requirement clause, D5 what
  this packet refuses and where each piece went, D6 the per-tenant multiplicity
  and the bill it implies.
- [x] 1.4 `specs/credential-contracts/spec.md`: ONE `## MODIFIED` block on
  *Dispatch-only credential least privilege and serving-tier separation* —
  canon's body paragraph and all three promoted scenarios restated VERBATIM, five
  clauses added (the first carrying an explicit scoping rider), eight
  scenarios added. The delta-currency check is stated in the
  delta's own preamble: two active changes carry a `credential-contracts` delta
  and NEITHER writes this requirement, so the block is over canon and no
  `Modified over` marker is owed. The preamble ALSO states what the block does
  not repeal — canon's *"Both cases SHALL remain legitimate"*
  (`openspec/specs/credential-contracts/spec.md:141`) and the ratified
  operator-hosted Case A of `docs/openxdox-dispatch-credential-binding.md:31-37`
  — and two of the eight added scenarios ASSERT that reconciliation rather than
  leaving it to prose.
- [x] 1.5 README **OpenSpec Records** row.
- [x] 1.6 The per-change sweep-ledger row, written by
  `python3 scripts/validate-sequenced-after.py . --seed-ledger --moved-by '#<PR>'`
  and never hand-edited; the diff read to confirm WHICH rows it moved. It moved
  TWO, both of them this change's to move: this change's own new `active` row,
  and the archived `add-dispatch-credential-contract` row flipped `sole` →
  `co-modifier` with this pull request's provenance. The partner flip is the
  generator's documented behaviour, not a stray edit — *"a pull request moves ITS
  OWN ROW (and a partner's row when its `## MODIFIED Requirements` block flips
  that partner from sole to co-modifier)"* (`scripts/sequenced_after.py:2244`) —
  and the September `moved_on` on an August-archived row is likewise the
  documented form (`:2386-2392`: *"A September pull request that flips an
  already-archived row from sole to co-modifier moved it in September"*). No
  third row moved.
- [ ] 1.7 Gates MEASURED at the pull request head — *measured* rather than
  *green*, because two of the three do not read zero on `main` either and that
  distinction is the whole content of this box.
  **(a)** `openspec validate add-per-tenant-app-manifest-provisioning --strict`
  → **valid**. That is the packet-local gate and it is the one that must be
  clean.
  **(b)** `openspec validate --all --strict` → **108 passed, 2 failed**, and the
  two are `add-chain-attestation` (its MODIFIED block omits the canon scenario
  *"a tranche-two link does not exist yet"*) and `add-composed-view-authoring`
  (omits *"Gate verbs hide on a composed view"*) — both PRE-EXISTING on `main`
  at the base commit, neither of them this change. This change's ABSENCE from
  that list is not a silence to read past: it is the tool confirming that this
  MODIFIED block carries every promoted scenario of the requirement it restates.
  **(c)** `python3 -m pytest tests/doc-health tests/sequenced_after -q` → ONE
  inherited failure, `tests/doc-health/test_modified_block_currency_self_gate.py`,
  RED on `main` itself over two carriage-ledger subjects opened by another lane,
  with a fix in flight. This packet must not add a THIRD subject, and does not —
  `python3 scripts/doc-health.py --single-repo . --family modified-block-currency`
  finds this change id ZERO times across the whole family report, and the two
  ordering warnings it does raise name the other lane's two subjects.
  All three read at the head rather than argued.

## 2. Ratification

- [ ] 2.1 Ratification read by Brett Heap over the block as it stands, the two
  open questions put with recommendations, and the ruling recorded at
  `review/ratification-<date>.md` with `Status: ratified` and `Ratified by:` on
  `proposal.md` and `design.md`.
- [ ] 2.2 **OQ-1 (the staged topic's Q2 — the managed flow).** Put with the
  recommendation the proposal carries; it blocks nothing here and its answer is
  the installer's sequence.
- [ ] 2.3 **OQ-2 (the apply-workflow repository's provenance).** Put with the
  recommendation the proposal carries; the requirement binds the property, not the
  provenance.

## 3. Realization — OWED ELSEWHERE, AUTHORED NOWHERE HERE

The staged topic's exit path names two halves and this packet is the first; it
does not close the topic (`proposal.md`, the lifecycle paragraph). The second
half is named here so it is a debt with an address rather than an assumption.

- [~] 3.1 **DEFERRED — `opensoft/Omnigent-Install`, the installer change.
  Owner: whoever opens that repository's change.** The flow that drives the
  manifest, exchanges the temporary code inside the provider's window, lands the
  material in the DECLARED custody by reference — whose operator is that
  install's own execution binding, not a party this contract names — and wires
  the two bindings, under that repository's own change, its own code surface and
  its own realization evidence. NOT this packet's surface, and NOT authorable here: that
  repository's README states it *"should not contain … canonical shared contracts
  that belong in `openxFactory/contracts`"*, which is CLAUDE.md working rule 1
  from the other side.
- [~] 3.2 **DEFERRED — the first consuming domain repository: the manifest
  files and the install-doc pointer. Owner: that repository's own lane.** The
  staged topic names `codexFactory` as the first case.
- [~] 3.3 **DEFERRED, CONDITIONAL — a validator arm IF and WHEN a provisioning
  manifest becomes a record this repository carries. Owner: whoever gives the
  record a shape at 3.1.** Deliberately not authored now: the record shape does
  not exist in any corpus `openxFactory` validates, so an arm authored today would
  be an arm with only invented fixtures. Whoever gives the record a shape at 3.1
  owns the question of whether it comes home here.

## 4. Archive gate

- [ ] 4.1 Under `release-realization` an empty code surface archives ON LANDING
  plus this task list — and the mechanism is stated here exactly rather than
  approximately, because it was got wrong once. `archive_change()` scans the
  WHOLE task file and refuses on any literal `- [ ]` with no section-level
  exception (`scripts/proposal-support.py:4609`, *"change has incomplete
  tasks"*). **§ 1 and § 2 are therefore the gate in the operative sense: they are
  this repository's surface and they must be TICKED.** § 3 and § 5 are not this
  repository's surface and cannot be ticked from here, so each carries the
  house's reserved DEFERRED marker `- [~]` with its holder named in the box —
  the form this repository already uses for open-but-not-ours work
  (`README.md:4790`, and `openspec/changes/archive/2026-09-09-pin-openspec-cli-dependency-closure/tasks.md:353`
  and `.../2026-09-10-adopt-codexfactory-repository-identity/tasks.md:466`).
  That marker is what makes the archive executable while the debt stays open and
  addressed, and it is why § 3 is named-and-owed rather than gating — the same
  reason the `code_surface:` head reads `none`.
- [ ] 4.2 The staged fragment STAYS staged and its `ideation/staging/INDEX.md`
  row records the exit (the fold into `opendox-two-layer-product` is recorded
  there and deleting the folder would delete the fold's provenance).

## 5. Not this change's business, recorded so nobody re-derives it

- [~] 5.1 **NOT THIS CHANGE'S. Owner: lane opsXfactory-4.** The `openxdox` DNS
  record's governance — RULED `5704187317` (B), discharged by NAMING; the act is lane opsXfactory-4's inside
  `opensoft/OpsxFactory`'s active `add-governed-dns-administration`, on Brett's
  OQ-E word (`opensoft/OpsxFactory` issue #207 comment `5649809425`). **Nothing
  here waits on it and nothing here performs it.**
- [~] 5.2 **NOT THIS CHANGE'S. Owner: lane opsXfactory-3, at § 3.5's
  realization.** The `dox` workload set becoming per-tenant — RULED
  `5704187317` (D), left to `split-opendox-two-layer-product` § 3.5's realization; its requirement
  stands under lane opsXfactory-3's claim `5638511222`.
- [~] 5.3 **NOT THIS CHANGE'S. Owner: this lane's bookkeeper, amendment #5.**
  `split-opendox-two-layer-product`'s own `tasks.md` § 7.4 tick and the
  RECORDED second delta-text defect (`design.md:133-134` *"beyond naming them"*
  against `tasks.md:1979` *"is governed here"*, in the class of ruling
  `5700622683`) — the bookkeeper's amendment #5. **This packet edits that packet
  by not one byte.**
