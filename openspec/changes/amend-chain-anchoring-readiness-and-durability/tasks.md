# Tasks: amend-chain-anchoring-readiness-and-durability

## 1. Governance and Single-Feature Handoff

- [ ] 1.1 Ratify this amendment and its three additive `chain-anchoring`
      requirements; record the owner, exact artifact revision, unconditional
      decision, validation evidence, and timestamp before implementation begins.
      > **Note (2026-09-04, owner's ruling — requirement 1 dropped):** this
      > amendment now carries TWO additive requirements (2 and 3), not three.
      > See `proposal.md` "Requirement 1 removed".
- [ ] ~~1.2 Verify the released signed-execution-chain contracts and record
      that `signed-execution-chain-gate` is REQUIRED in the live ruleset and its
      broken-chain canary fails as designed; then record
      operational `trust-anchor`-conformant PKI evidence for issuance,
      verification, revocation handling, and chain custody; refuse the handoff
      while any realization gate is unproven.~~
      > **Note (2026-09-04, owner's ruling — requirement 1 dropped):** this
      > task served requirement 1 alone (the operational-PKI realization gate)
      > and is no longer owed. `add-chain-anchoring` already realized its
      > schemas and validator at PR #629 without this gate, on the owner's
      > explicit ruling. Retained here, struck rather than deleted, per
      > `docs/document-lifecycle.md`.
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
- [ ] ~~1.5 Create exactly one SHARED Speckit feature from the intended
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
- [ ] 1.6 Verify the linked feature specification maps every requirement and
      scenario in this amendment without reopening the ratified witness
      configuration or importing provider/runtime enforcement.
      > **Note (2026-09-04):** "every requirement" now means requirements 2
      > and 3 only.

## 2. Linked Feature Acceptance

- [ ] 2.1 Accept feature evidence that the shared realization creates the
      `chain-anchoring` schemas, examples, and canonical validator from the basis
      plus this amendment, implements the normative realization gate, and rejects
      provisional chain or PKI vocabularies.
      > **Note (2026-09-04, owner's ruling — requirement 1 dropped):** the
      > schema/example/validator creation half is already DONE, via PR #629,
      > against the basis alone (no "plus this amendment" — see
      > `proposal.md` "Realization cost if ratified"). The "implements the
      > normative realization gate" and "rejects provisional chain or PKI
      > vocabularies" clauses were requirement 1's and are no longer owed.
      > What remains owed by this task, if requirements 2 and 3 ratify, is a
      > follow-on pass adding their durability and confirmation-profile
      > machinery on top of the already-realized schemas.
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

- [ ] 3.1 Run strict validation for this change and the complete OpenSpec corpus,
      plus the repository's targeted and full validation gates; retain exact
      command results and resolve every finding before acceptance.
- [ ] 3.2 After the shared feature merges green, archive
      `add-chain-anchoring` FIRST to create canonical `chain-anchoring`, then
      archive this amendment SECOND; verify all twelve promoted requirements
      byte-for-byte against their two deltas.
      > **Note (2026-09-04, owner's ruling — requirement 1 dropped):**
      > `add-chain-anchoring` (nine requirements) plus this amendment's
      > remaining TWO (requirements 2 and 3, not three) makes **eleven**
      > promoted requirements to verify, not twelve. `add-chain-anchoring`
      > itself has not archived yet as of this writing (its realization, PR
      > #629, is merged; its own archive is a separate act).
- [ ] 3.3 Cut one additive new-family contract minor allocated by merge order
      only after both archives are present, register all contract members and
      digests, and publish immutable release evidence before any consumer claims
      released-contract conformance.
