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
- [ ] 1.3 Before schema or validator authoring, approve and publish append-only
      Kaspa and Bitcoin confirmation-profile registry entries with canonical
      content digests, approval records, activation log checkpoints, effective
      UTC-window boundaries, standing, predecessor links, and positive/refusal
      transition vectors; refuse feature handoff while either active profile is
      unresolved.
- [ ] 1.4 Before schema or validator authoring, approve and release one immutable
      daily-Merkle construction profile that fixes canonical leaf encoding,
      SHA-256, leaf/internal domain separators, sequence ordering, tree shape,
      odd-node handling, deterministic empty root, id, version, content digest,
      and positive/refusal vectors.
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
- [ ] 1.6 Verify the linked feature specification maps every requirement and
      scenario in this amendment without reopening the ratified witness
      configuration or importing provider/runtime enforcement.
      > **Note (2026-09-04):** "every requirement" now means requirements 2
      > and 3 only.

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
- [ ] 2.2 Accept deterministic feature evidence for non-empty, empty,
      midnight-boundary, concurrent close/admission, late-source-time,
      identical-replay, conflicting-dedupe, recursive-control-leaf,
      mid-window eligibility activation, eligibility-content substitution,
      zero/multiple eligibility matches, eligibility rollback, omitted eligible
      suffix under a lowered summary, close-watermark/checkpoint substitution,
      Merkle-profile substitution, independent root recomputation, omitted
      intermediate empty day, split-witness-root, substituted manifest/
      configuration/profile, missing witness-commitment path, and selectively
      omitted daily-window cases.
- [ ] 2.3 Accept feature evidence distinguishing Kaspa submitted from confirmed
      and OpenTimestamps submitted from Bitcoin confirmed under immutable
      versioned approved profiles, including activation, rollback, retirement,
      compromise, mid-window activation, content-substitution, reorganization/
      replacement, and profile-revision vectors, while preserving the receipt/
      state split and same-digest proof upgrade.
- [ ] 2.4 Verify immediately before implementation that `chain-anchoring` has not
      released independently. If it has, stop and govern the compatibility and
      version class before changing any schema; otherwise prove the shared first
      release reinterprets no prior artifact because no prior artifact exists.
      > **Note (2026-09-04):** re-stated in current terms — `chain-anchoring`
      > has REALIZED (PR #629) but not RELEASED (`contract-v3.3` unspent, no
      > bundle cut). This task remains live: verify at follow-on realization
      > time that no bundle cut the family in between, per `proposal.md`
      > "Compatibility".
- [ ] 2.5 Record contract realization separately from runtime commissioning. If a
      participating runtime is claimed, require its signed-log instance identity,
      signer chain, custody owner, reachable interface, current checkpoint, and
      successful canonical-validator result; otherwise state that no runtime was
      commissioned.
      > **Note (2026-09-04, owner's ruling — requirement 1 dropped):** this
      > task served requirement 1's realization-versus-commissioning split.
      > PR #629 already reports this split independently for the basis's own
      > realization (its "OPEN, for the owner" items 2-3); no runtime is
      > commissioned by this amendment either.

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
