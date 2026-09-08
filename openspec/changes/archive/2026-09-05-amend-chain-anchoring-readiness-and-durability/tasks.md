# Tasks: amend-chain-anchoring-readiness-and-durability

> **RATIFIED 2026-09-04 — Brett Heap, repository owner, in session, recorded on
> PR #548, verbatim: "ratify 2 and 3".** Requirements 2 and 3 are ratified AS
> WRITTEN over head `2677cef9`; requirement 1 is WITHDRAWN (not refused) by his
> separate earlier ruling of the same day. Record:
> [`review/ratification-2026-09-04.md`](review/ratification-2026-09-04.md).
>
> **EVERY UNTICKED TASK BELOW BELONGS TO THE NAMED SUCCESSOR, NOT TO THIS
> PACKET.** Ratification promotes the spec delta and realizes nothing. The
> successor is a **new, separate realization PR** against the schemas PR #629
> (squash `11feff75`) already landed, and it owes: (1) a confirmation-profile
> registry contract plus its id/version/content-digest/activation-checkpoint
> binding in the receipt's mint-time configuration block, (2) the widen-or-
> replace of `contracts/chain-anchoring/anchor-state.schema.yaml`'s closed
> per-witness `status` enum `[in_flight, landed, terminally_failed]` to separate
> `submitted` from `confirmed` per network, and (3) requirement 2's fixed-UTC
> durability batch, eligibility-registry and daily-Merkle construction
> machinery. **It MUST land before `contracts/chain-anchoring/` ships in a
> TAGGED bundle** — item 2 is a breaking change to a closed enum, free while
> unpublished and a compatibility break once published — and the window exists
> only because the `contract-v3.3` tag (`16b85614`) predates #629 by twenty
> minutes, leaving the family registered in `contracts/manifest.yaml` (54
> references) but carrying ZERO entries in
> `contracts/releases/contract-v3.3.digests.yaml`. § 2.4 is the successor's
> FIRST act. See `proposal.md` § *Realization cost — ratified, and now owed*.

## 1. Governance and Single-Feature Handoff

- [x] 1.1 Ratify this amendment and its two additive `chain-anchoring`
      requirements; record the owner, exact artifact revision, unconditional
      decision, validation evidence, and timestamp before implementation begins.
      > **Note (2026-09-04, owner's ruling — requirement 1 dropped):** originally
      > worded "three additive requirements"; requirement 1 is removed (see
      > `proposal.md` "Requirement 1 removed"), leaving two (2 and 3).
      > **DONE 2026-09-04** — [`review/ratification-2026-09-04.md`](review/ratification-2026-09-04.md)
      > carries every element this task names: the owner (Brett Heap, repository
      > owner, in session, recorded on PR #548), the exact artifact revision
      > (head `2677cef9`, with the catch-up merge proven not to move a line of
      > the delta), the UNCONDITIONAL decision ("ratify 2 and 3" — both AS
      > WRITTEN, unamended), the validation evidence (the § *Gates at the
      > ratification commit* block plus the seven green required checks), and the
      > timestamp (2026-09-04 ~05:10Z). It also records requirement 1's
      > disposition as WITHDRAWN rather than refused, which no other artifact
      > states.
- [x] ~~1.2 Verify the released signed-execution-chain contracts and record
      that `signed-execution-chain-gate` is REQUIRED in the live ruleset and its
      broken-chain canary fails as designed; then record
      operational `trust-anchor`-conformant PKI evidence for issuance,
      verification, revocation handling, and chain custody; refuse the handoff
      while any realization gate is unproven.~~
      > **Note (2026-09-04, owner's ruling — requirement 1 dropped):** this
      > task served requirement 1 alone (the operational-PKI realization gate)
      > and is no longer owed. `add-chain-anchoring` already realized its
      > schemas and validator at PR #629 without this gate, on the owner's
      > explicit ruling. Struck text kept per `docs/document-lifecycle.md`;
      > checked off (not left `- [ ]`) so a dropped, no-longer-owed task does
      > not trip `proposal-support.py`'s incomplete-tasks archive gate, which
      > matches on the leading marker regardless of the strikethrough.
- [ ] 1.3 **[OPERATOR]** Before schema or validator authoring, approve and
      publish append-only
      Kaspa and Bitcoin confirmation-profile registry entries with canonical
      content digests, approval records, activation log checkpoints, effective
      UTC-window boundaries, standing, predecessor links, and positive/refusal
      transition vectors; refuse feature handoff while either active profile is
      unresolved.
      > **STILL OWED, AND IT IS AN OPERATOR ACT — NOT ticked. What the
      > successor realization built is the VESSEL, and the REFUSAL that makes
      > the block mechanical.** `contracts/chain-anchoring/confirmation-profile.schema.yaml`
      > and `confirmation-profile-registry.schema.yaml` are the shapes an
      > approval is published into, carrying every binding this task
      > enumerates; `scripts/validate-chain-anchoring.py` REFUSES a register
      > whose declared configured network has no `active` entry
      > (`confirmation_profile_unresolved`), one approved by anyone but the
      > operator (`confirmation_profile_not_operator_approved`), one naming a
      > numeric depth with nothing cited behind it
      > (`confirmation_profile_numeric_depth_uncited`), and one whose terms
      > carry only a single transition direction
      > (`profile-transition-vectors-incomplete`) — each red-proven by a
      > packaged negative. **The packaged register carries EXAMPLE entries and
      > NO operator's act**, the packaged conformance declaration records
      > `operator_approval_outstanding` in the present tense, and the family
      > README says so where a consumer will read it. The owner's ruling of
      > 2026-09-04 (*"build the successor realization on 629's schemas"*)
      > authorized the contract; it did not perform this approval, and this
      > realization does not report it performed.
- [ ] 1.4 **[OPERATOR]** Before schema or validator authoring, approve and
      release one immutable
      daily-Merkle construction profile that fixes canonical leaf encoding,
      SHA-256, leaf/internal domain separators, sequence ordering, tree shape,
      odd-node handling, deterministic empty root, id, version, content digest,
      and positive/refusal vectors.
      > **STILL OWED, SAME SPLIT AS 1.3 — NOT ticked.**
      > `contracts/chain-anchoring/daily-merkle-profile.schema.yaml` fixes every
      > element this task names, `SHA-256` as a `const` and the rest as closed
      > enumerations, with the deterministic empty root DECLARED rather than
      > left to convention. The canonical reader RESOLVES a bound profile and
      > mechanically recomputes every leaf, membership path and batch root under
      > it, refuses a substituted construction
      > (`merkle_profile_absent_or_substituted`), refuses equal domain
      > separators (`merkle-domain-separators-equal`), and refuses a declared
      > ordering or shape it cannot reproduce deterministically
      > (`daily_batch_root_not_reproducible`). **The packaged profile is an
      > EXAMPLE release and not the operator's**, which is why this box stays
      > open.
- [x] ~~1.5 Create exactly one SHARED Speckit feature from the intended
      openxFactory base and record immutable two-way links from that feature to
      both `add-chain-anchoring` and this amendment; neither packet may create a
      competing implementation feature, and executable implementation tasks stay
      in the shared feature's `tasks.md`.~~
      > **Note (2026-09-04, owner's ruling — requirement 1 dropped):** this
      > task's premise ("Because `add-chain-anchoring` is ratified but
      > unrealized...") was requirement 1's own text, now removed. The basis
      > realized at PR #629 through an adopted branch, with no shared Speckit
      > feature and no two-way link to this amendment. A follow-on realization
      > for requirements 2 and 3 (see `proposal.md` "Realization cost if
      > ratified") may reuse or skip this shared-feature mechanism as its own
      > owner rules; it is no longer mandatory by this amendment's own text.
      > Checked off (not left `- [ ]`) for the same mechanical reason as 1.2.
- [x] 1.6 Verify the linked feature specification maps every requirement and
      scenario in this amendment without reopening the ratified witness
      configuration or importing provider/runtime enforcement.
      > **Note (2026-09-04):** "every requirement" now means requirements 2
      > and 3 only.
      > **DONE 2026-09-04** — the Speckit feature is
      > [`specs/029-chain-anchoring-durability-confirmation/`](../../../specs/029-chain-anchoring-durability-confirmation/),
      > whose `spec.md` maps ALL THIRTY-FOUR scenarios (20 + 14) to the record
      > shape, the reader rule and the test that holds each, and whose
      > `data-model.md` carries the shape-by-shape design. The mapping is
      > MECHANICAL rather than asserted:
      > `tests/chain_anchoring/test_durability_and_confirmation_scenarios.py`
      > carries **one test per scenario, 34 of them, each named for its
      > scenario and quoting its WHEN/THEN in its own docstring** — 34 passed.
      > NOTHING REOPENED: the two-witness configuration is untouched (the
      > `third_anchor_target` refusal and its fixture stand unchanged), no
      > provider or runtime enforcement is imported, no chain is named, and the
      > `witness_role` enumeration is still exactly `[operational,
      > durability]`.

## 2. Linked Feature Acceptance

- [x] 2.1 Accept that `chain-anchoring`'s schemas, examples, and canonical
      validator are already realized (PR #629, against the basis alone). The
      normative-realization-gate and provisional-chain/PKI-vocabulary clauses
      this task originally named were requirement 1's and are dropped with it.
      > **Note (2026-09-04, owner's ruling — requirement 1 dropped):** checked
      > off because the schema/example/validator creation this task asked to
      > accept is DONE (see `proposal.md` "Realization cost if ratified" for
      > the measurement). What remains owed, if requirements 2 and 3 ratify,
      > is a separate follow-on realization pass adding their durability and
      > confirmation-profile machinery on top of these already-realized
      > schemas — tracked as new work, not as this task's completion.
- [x] 2.2 Accept deterministic feature evidence for non-empty, empty,
      midnight-boundary, concurrent close/admission, late-source-time,
      identical-replay, conflicting-dedupe, recursive-control-leaf,
      mid-window eligibility activation, eligibility-content substitution,
      zero/multiple eligibility matches, eligibility rollback, omitted eligible
      suffix under a lowered summary, close-watermark/checkpoint substitution,
      Merkle-profile substitution, independent root recomputation, omitted
      intermediate empty day, split-witness-root, substituted manifest/
      configuration/profile, missing witness-commitment path, and selectively
      omitted daily-window cases.
      > **DONE 2026-09-04.** Every case this task names is a NAMED REFUSAL with
      > a single-fault packaged negative whose filename IS the code, plus a test
      > that names the scenario: the non-empty and empty closes and the
      > midnight-boundary and late-source-time admissions are POSITIVE packaged
      > records (three consecutive fixed-UTC windows, with the empty day
      > load-bearing in the third day's continuity proof); the concurrent
      > close/admission race is held by the declared-atomicity refusal plus the
      > two-windows and sequence-inversion refusals; and the remainder —
      > identical replay, conflicting dedupe, recursive control leaf, mid-window
      > eligibility activation, eligibility-content substitution,
      > zero/multiple eligibility matches, eligibility rollback, the omitted
      > eligible suffix under a lowered summary, the unproven close watermark,
      > Merkle-profile substitution, independent root recomputation, the omitted
      > intermediate empty day, the split witness root, the substituted
      > manifest/configuration/profile, the absent witness-commitment path and
      > the selective batch — are each red-proven. **THE EVIDENCE IS
      > DETERMINISTIC BY CONSTRUCTION:** every batch root and membership path in
      > the corpus is COMPUTED under the released construction rather than
      > written by hand, and the reader recomputes them rather than reading a
      > declared value. Self-test: 41 positive records as one coherent scope,
      > 126 negatives invalid for their intended reason, **118/118 closed
      > refusal codes red-proven**, 8 further finding codes probed, 0 errors.
- [x] 2.3 Accept feature evidence distinguishing Kaspa submitted from confirmed
      and OpenTimestamps submitted from Bitcoin confirmed under immutable
      versioned approved profiles, including activation, rollback, retirement,
      compromise, mid-window activation, content-substitution, reorganization/
      replacement, and profile-revision vectors, while preserving the receipt/
      state split and same-digest proof upgrade.
      > **DONE 2026-09-04.** The per-witness enumeration is REPLACED — `pending`
      > and `submitted` split the old `in_flight`, `landed` becomes `confirmed`
      > bound to a named profile's objective condition, and `invalid` and
      > `unevaluable` are added because this amendment's own refusal scenario
      > obliges a verifier to report them. The durability witness reports TWO
      > LAYERS separately (`upgrade_stage.aggregation_submission` and
      > `.chain_confirmation`), which is what makes *"OpenTimestamps submitted
      > and Bitcoin pending"* expressible at all; a packaged positive record
      > carries exactly that state with `long_horizon_claim_admitted: false`.
      > Activation, rollback, retirement, compromise, mid-window activation,
      > content substitution, reorganization/replacement and profile revision
      > each have a named refusal and a packaged negative, and the register's
      > two immutable operational versions with the RETIRED PREDECESSOR KEPT IN
      > PLACE are a packaged positive. **THE RECEIPT/STATE SPLIT IS PRESERVED
      > RATHER THAN ASSERTED:** the day-three receipt carries ONE per-chain
      > entry while its state record carries the submitted durability row, and
      > the reader still refuses a receipt entry for a witness the state says
      > is not confirmed. **THE UPGRADE IS SAME-DIGEST:** the completed entry's
      > `commitment_derivation.source_aggregation_root` equals the receipt's own
      > `anchored_digest`, re-anchoring is refused
      > (`durability_proof_reanchored_rather_than_upgraded`, unchanged from the
      > basis) and so is an upgrade that erased its prior transitions
      > (`state_transition_history_erased_on_upgrade`, new).
- [x] 2.4 Verify immediately before implementation that `chain-anchoring` has not
      released independently. If it has, stop and govern the compatibility and
      version class before changing any schema; otherwise prove the shared first
      release reinterprets no prior artifact because no prior artifact exists.
      > **Note (2026-09-04):** re-stated in current terms — `chain-anchoring`
      > has REALIZED (PR #629) but not RELEASED (`contract-v3.3` unspent, no
      > bundle cut). This task remains live: verify at follow-on realization
      > time that no bundle cut the family in between, per `proposal.md`
      > "Compatibility".
      > **DONE 2026-09-04, AND IT WAS THIS REALIZATION'S FIRST ACT.** Measured
      > rather than assumed, twice — at the branch point and again before the
      > PR opened:
      >
      > * `git tag --contains 11feff75` → **EMPTY**. No published tag contains
      >   the basis realization, so nothing in `contracts/chain-anchoring/` has
      >   shipped in a bundle.
      > * `grep -c chain-anchoring contracts/releases/contract-v3.3.digests.yaml`
      >   → **0**. The most recent cut inventory carries no row for any path in
      >   this family, because the `contract-v3.3` tag (`16b85614`) predates
      >   `11feff75` by twenty minutes.
      > * `gh pr list --state open` → **no open cut PR** (`cut/*`, a
      >   "Cut contract-v3.x" title, or a release-inventory change) and **no
      >   sibling realization touching `contracts/chain-anchoring/`** at the
      >   time this branch was cut.
      >
      > **THEREFORE THE SHARED FIRST RELEASE REINTERPRETS NO PRIOR ARTIFACT,
      > BECAUSE NO PRIOR ARTIFACT EXISTS** — which is exactly the alternative
      > this task's own text asks for. It follows that replacing
      > `anchor-state.schema.yaml`'s closed per-witness `status` enumeration is
      > ADDITIVE to every bundle that has ever shipped, and that this
      > realization MUST land before the next cut; a cut taken from a tip that
      > lacks it would have to be re-derived. The measurement and its
      > consequence are recorded where a consumer reads them: the family README,
      > the `witness_evidence_state` `$def` itself, and the manifest's own row
      > block.
- [x] 2.5 Record contract realization separately from runtime commissioning. If a
      participating runtime is claimed, require its signed-log instance identity,
      signer chain, custody owner, reachable interface, current checkpoint, and
      successful canonical-validator result; otherwise state that no runtime was
      commissioned.
      > **Note (2026-09-04, owner's ruling — requirement 1 dropped):** this
      > task served requirement 1's realization-versus-commissioning split.
      > PR #629 already reports this split independently for the basis's own
      > realization (its "OPEN, for the owner" items 2-3); no runtime is
      > commissioned by this amendment either.
      > **DONE 2026-09-04, AND THE STATEMENT IS THE NEGATIVE ONE.** **NO RUNTIME
      > IS COMMISSIONED BY THIS REALIZATION.** No signed-log instance identity,
      > signer chain, custody owner, reachable interface or current checkpoint
      > is claimed anywhere in it, and none is required, because no claim rests
      > on one: what landed is CONTRACT TEXT plus a refusing reader plus a
      > packaged corpus. The reader's own docstring says the same thing at
      > equal length — it reaches no chain, approves no profile, and **cannot
      > see a signed log**: the checkpoint reconciliation walks the ADMISSION
      > RECORDS it is handed and warns
      > (`manifest-admissions-not-in-scope`) where a closed window's
      > admissions do not travel with it, rather than passing the claim. The
      > repo scan reports **0 real artifacts**, which is the expected state
      > until an anchoring subsystem runs.

## 3. Validation, Release, and Closure

- [x] 3.1 Run strict validation for this change and the complete OpenSpec corpus,
      plus the repository's targeted and full validation gates; retain exact
      command results and resolve every finding before acceptance.
      > **DONE 2026-09-04 FOR THE RATIFICATION COMMIT, and scoped to it.** The
      > exact command results are retained in
      > [`review/ratification-2026-09-04.md`](review/ratification-2026-09-04.md)
      > § *Gates at the ratification commit*: `openspec validate
      > amend-chain-anchoring-readiness-and-durability --strict` VALID and
      > `--all --strict` 90 passed / 0 failed; `proposal-support.py . verify`
      > ok; `pytest tests/sequenced_after -q` 162 passed;
      > `validate-sequenced-after.py . --ledger-diff` ledger consistent with the
      > corpus (164 rows); `pytest tests/doc-health -q -p no:cacheprovider`
      > 1542 passed / 0 failed; and all seven required CI checks SUCCESS. Zero
      > findings outstanding. **The SUCCESSOR realization owes its own run of
      > this gate against the schemas it changes** — this tick covers the
      > ratification commit and claims nothing about a tree that edits
      > `contracts/chain-anchoring/`.
      > **AND THE SUCCESSOR RAN IT AGAINST THE TREE IT EDITS, 2026-09-04.**
      > `openspec validate --all --strict` 89 passed / 0 failed (the corpus is
      > 89 items rather than the ratification commit's 90 because
      > `add-subject-establishment` archived in between);
      > `proposal-support.py . verify amend-chain-anchoring-readiness-and-durability`
      > ok; `validate-chain-anchoring.py .` **0 errors, 2 warnings** (both
      > standing and both honest: `reader-not-required` and
      > `archival-node-undeclared`), self-test 41 positives / 126 negatives /
      > 118 of 118 closed codes red-proven; `validate-signed-execution-chain.py
      > . --require-pinned-wallet-vocabulary` 0/0;
      > `validate-manifest-digests.py .` 187 of 187 verify;
      > `pytest tests/chain_anchoring` 59 passed;
      > `pytest tests/doc-health -q -p no:cacheprovider` 1552 passed;
      > `validate-sequenced-after.py . --ledger-diff` ledger consistent (164
      > rows); and `doc-health.py --single-repo` taken at `origin/main`
      > (`e4ff4fb3`, detached worktree) and at this branch's head gives an
      > IDENTICAL finding set — 6 critical / 4 error / 27 warning / 16 info on
      > both sides, zero delta. Full transcript:
      > [`specs/029-chain-anchoring-durability-confirmation/evidence/gates.md`](../../../specs/029-chain-anchoring-durability-confirmation/evidence/gates.md).
- [ ] 3.2 Archive `add-chain-anchoring` FIRST to create canonical
      `chain-anchoring`, then archive this amendment SECOND; verify all eleven
      promoted requirements byte-for-byte against their two deltas. (Originally
      gated on "the shared feature merges green" and "twelve promoted
      requirements" — requirement 1's shared-Speckit-feature mandate is
      dropped along with requirement 1 itself; nine from `add-chain-anchoring`
      plus this amendment's remaining two make eleven. `add-chain-anchoring`
      itself has not archived yet as of this writing — its realization, PR
      #629, is merged; its own archive is a separate act.)
- [ ] 3.3 Cut one additive new-family contract minor allocated by merge order
      only after both archives are present, register all contract members and
      digests, and publish immutable release evidence before any consumer claims
      released-contract conformance.

## Archive — the recorded escape, and the four boxes that made it necessary

**ARCHIVED 2026-09-05 VIA THE RECORDED ESCAPE, SECOND OF AN ORDERED PAIR.**
Brett Heap ordered it in session on 2026-09-04, verbatim *"archive
chain-anchoring"* — one word covering BOTH archives, because the pair is one
act in two commits. `add-chain-anchoring` archived FIRST, on 2026-09-04 (PR
#669, squash `66d11a24`), and CREATED `openspec/specs/chain-anchoring/spec.md`
with its nine requirements; **this amendment archives SECOND, on 2026-09-05,
into that same file**, which is the order **task 3.2 below fixes in its own
first words** — the reverse writes a capability holding only this amendment's
two requirements and loses the basis it amends. The dates differ because the
pair straddles a UTC midnight, not because the acts do.

The evidence chain is read off `main` and none of it is assumed:

* **RATIFIED** 2026-09-04, PR #548, squash `471d3361` — Brett Heap, repository
  owner, in session, verbatim *"ratify 2 and 3"*, both requirements AS WRITTEN
  and unamended over head `2677cef9`. Requirement 1 was **WITHDRAWN — not
  refused** — by his separate and earlier ruling of the same day. Record
  [`review/ratification-2026-09-04.md`](review/ratification-2026-09-04.md),
  archived with the packet.
* **REALIZED** PR #657, squash `e65dcc48`, merged 2026-09-04T18:25:33Z — the
  successor realization built on the schemas PR #629 had already landed: SIX
  new schemas under `contracts/chain-anchoring/`
  (`confirmation-profile`, `confirmation-profile-registry`,
  `daily-merkle-profile`, `durability-eligibility-registry`,
  `durability-batch-admission`, `durability-batch-manifest`), each carrying a
  registered row in `contracts/manifest.yaml`, plus the widen-or-replace of
  `anchor-state.schema.yaml`'s closed per-witness enumeration.
* **PUBLISHED** at `contract-v3.4`, PR #653, squash `807a4f47`, annotated tag
  object `a3309921` — verified by `git rev-list -n1 contract-v3.4` peeling to
  `807a4f47` rather than by reading a release note. **AND THE WORD
  "PUBLISHED" IS USED PRECISELY**: `contracts/releases/contract-v3.4.digests.yaml`
  is a SELECTIVE inventory of 283 entries carrying **ZERO** rows under
  `contracts/chain-anchoring/`, so what publication means here is the six
  manifest rows, the `contracts/CHANGELOG.md` v3.4 entry that names this change
  four times, and the `contracts/README.md` contract-index row — never "its
  digests are in the inventory", which the inventory itself refutes.

`python3 scripts/proposal-support.py . archive amend-chain-anchoring-readiness-and-durability`
was tried FIRST and REFUSED — exit 1, `"change has incomplete tasks"`. Its gate
is

    tasks = directory / "tasks.md"
    if tasks.is_file() and re.search(r"^- \[ \]", tasks.read_text(), re.M):
        raise SupportError("change has incomplete tasks")
    (scripts/proposal-support.py:1079-1081)

— read off those three lines in this tree rather than remembered, and
**UNCONDITIONAL on WHICH box**: it matches the leading marker and can tell
nothing else about the task it refuses on.
`OPENSPEC_TELEMETRY=0 openspec archive amend-chain-anchoring-readiness-and-durability --yes`
was run instead. It reported `Task status: 10/14 tasks` and
`Warning: 4 incomplete task(s) found. Continuing due to --yes flag.`, updated
`openspec/specs/chain-anchoring/spec.md` (`+ 2 added`, `~ 0`, `- 0`), and moved
the packet to
`openspec/changes/archive/2026-09-05-amend-chain-anchoring-readiness-and-durability/`.

**PRECEDENT, cited rather than invented**: `declare-spent-bundle-state` § 5.1
(PR #611, squash `7af2725c`, 2026-09-03), itself following
`govern-sibling-added-modified-deltas` (PR #571, squash `3bcde7e2`); applied by
`add-subject-establishment` (PR #647, squash `e4ff4fb3`, 2026-09-04); and
**immediately preceding this act, `add-chain-anchoring` itself** (PR #669,
squash `66d11a24`, 2026-09-04) — the same lane, the same word, the other half
of this pair, whose sixteen open boxes were disclosed the same way one section
from the end of its own `tasks.md`.

**NOT ONE OF THE FOUR IS UNDONE REALIZATION OF THIS CHANGE**, and ticking any of
them to satisfy the wrapper would be writing a false completion past a gate that
cannot tell "open by omission" from "open by design" apart. **NO BOX IS TICKED
BY THIS ARCHIVE.** They fall in three classes:

**(a) OPERATOR INFRASTRUCTURE — 1.3 and 1.4.** Both carry **`[OPERATOR]`** in
their own first words, and both already carry the realization's own note saying
why they stay open: 1.3's reads *"STILL OWED, AND IT IS AN OPERATOR ACT — NOT
ticked. What the successor realization built is the VESSEL, and the REFUSAL that
makes the block mechanical"*; 1.4's reads *"STILL OWED, SAME SPLIT AS 1.3 — NOT
ticked"*. The split is exact and it is not a hedge: `confirmation-profile.schema.yaml`,
`confirmation-profile-registry.schema.yaml` and `daily-merkle-profile.schema.yaml`
fix **every element these two tasks enumerate**, and
`scripts/validate-chain-anchoring.py` REFUSES a register whose configured
network has no `active` entry, one approved by anyone but the operator, one
naming an uncited numeric depth, and one carrying a single transition
direction — each red-proven by a packaged single-fault negative. What is
missing is **the operator's approval itself**, which no contract can perform:
the packaged register carries EXAMPLE entries and no operator's act, and the
packaged conformance declaration records `operator_approval_outstanding` in the
present tense. `proposal.md`'s `code_surface` says the same thing from the other
side — *"no deployable gateway, chain client, scheduler, or credential
surface"*.

**(b) THIS ACT — 3.2.** The box reads *"Archive `add-chain-anchoring` FIRST to
create canonical `chain-anchoring`, then archive this amendment SECOND; verify
all eleven promoted requirements byte-for-byte against their two deltas."*
**That is exactly what the ordered pair did, and it is completed by this very
commit**: PR #669 archived the basis on 2026-09-04 and created the capability
at nine requirements / 89 scenarios; this act archives the amendment on
2026-09-05 and brings it to **ELEVEN requirements / 123 SCENARIOS**, byte-checked
below rather than trusted. **THE BOX IS STILL NOT TICKED**, and that is
deliberate: **an archive act does not close its own box.** Ticking it would mean
editing the packet's task list in the same commit that freezes the packet as a
record, to make a claim the commit has not finished making — and it moves the
wrapper's gate not at all, since three boxes would remain. #669 set the
precedent one day earlier and one lane over, leaving its own 3.2 and 4.12 open
and **recording the facts one section away instead**, which is what a record is
for. This section is that record.

**(c) DISCHARGED BY THE CUTTING SESSION, IN ANOTHER LANE — 3.3.** The box asks
for *"one additive new-family contract minor allocated by merge order only after
both archives are present"*, and the cut has run: **`contract-v3.4`** (PR #653,
squash `807a4f47`, annotated tag `a3309921`, 2026-09-04) registered all contract
members, carries the `contracts/CHANGELOG.md` entry, the
`contract_bundle_version` bump, the `contracts/README.md` index row and the
rebuilt inventory. **ITS ONE DEPARTURE FROM THIS BOX'S OWN TEXT IS RECORDED
RATHER THAN GLOSSED**: the cut was taken BEFORE either archive was present, on
the repository owner's explicit order that #657 land before these schemas
shipped in a tagged bundle — *"or the enum change becomes a breaking change on a
published bundle"* — because replacing `anchor-state.schema.yaml`'s closed
per-witness enumeration is free while unpublished and a compatibility break once
published. The owner's order governs the box's sequencing preference; the box's
SUBSTANCE — an additive minor allocated by merge order, with the family
registered and its release evidence published — is discharged. Ticking another
session's box in this lane is the same refusal as (b), on the same reasoning
#669 gave for its 4.12.

**THE PROMOTION WAS BYTE-CHECKED, NOT TRUSTED**, and in BOTH directions, because
this act writes into a file another act created and an archive that only checks
what it appended has checked half of what it could break.
`openspec/specs/chain-anchoring/spec.md` went from **95 655 bytes to 119 467**.

* **THE NINE REQUIREMENTS PR #669 PROMOTED ARE UNTOUCHED, BYTE FOR BYTE.**
  Extracted from the first `### Requirement:` line on both sides — from
  `git show origin/main:openspec/specs/chain-anchoring/spec.md` and from this
  tree's file up to the first appended heading — **95 510 bytes against 95 510,
  `diff` exit 0, not one character**. NINE requirements / 89 SCENARIOS on both
  sides.
* **THE TWO APPENDED REQUIREMENTS ARE THE ARCHIVED DELTA'S OWN TEXT.** Extracted
  the same way from
  `specs/chain-anchoring/spec.md` in this archive directory and from the tail of
  the canonical file: **IDENTICAL but for the one trailing blank line the
  archiver emits** — 23 811 bytes against 23 812 — which is the same one-byte
  signature #669 recorded for its own promotion. TWO requirements / 34 SCENARIOS
  on both sides, and no `## MODIFIED Requirements` block existed anywhere in the
  delta to widen a requirement the basis had already fixed.

The capability therefore holds **ELEVEN REQUIREMENTS OVER 123 SCENARIOS** — 9 + 2
and 89 + 34 — the two counts `add-chain-anchoring`'s archived record and this
packet's `review/ratification-2026-09-04.md` each declared separately, now met by
measurement rather than by addition. Neither of the two appended titles collides
with any of the nine. `git status --porcelain -uall openspec/specs/` names that
ONE file and nothing else, so no promoted requirement in any other capability
moved a word.

**THE ORDERED PAIR IS COMPLETE.** `add-chain-anchoring` archived 2026-09-04 at
`openspec/changes/archive/2026-09-04-add-chain-anchoring/`; this packet archived
2026-09-05 at
`openspec/changes/archive/2026-09-05-amend-chain-anchoring-readiness-and-durability/`.
Both dates are the real UTC dates of their acts.
