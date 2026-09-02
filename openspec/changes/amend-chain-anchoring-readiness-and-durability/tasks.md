# Tasks: amend-chain-anchoring-readiness-and-durability

## 1. Governance and Single-Feature Handoff

- [ ] 1.1 Ratify this amendment and its three additive `chain-anchoring`
      requirements; record the owner, exact artifact revision, unconditional
      decision, validation evidence, and timestamp before implementation begins.
- [ ] 1.2 Verify the released signed-execution-chain contracts and record
      that `signed-execution-chain-gate` is REQUIRED in the live ruleset and its
      broken-chain canary fails as designed; then record
      operational `trust-anchor`-conformant PKI evidence for issuance,
      verification, revocation handling, and chain custody; refuse the handoff
      while any realization gate is unproven.
- [ ] 1.3 Before schema or validator authoring, approve and publish append-only
      Kaspa and Bitcoin confirmation-profile registry entries with canonical
      content digests, approval records, activation log checkpoints, effective
      UTC-window boundaries, standing, predecessor links, and positive/refusal
      transition vectors; refuse feature handoff while either active profile is
      unresolved.
- [ ] 1.4 Create exactly one SHARED Speckit feature from the intended
      openxFactory base and record immutable two-way links from that feature to
      both `add-chain-anchoring` and this amendment; neither packet may create a
      competing implementation feature, and executable implementation tasks stay
      in the shared feature's `tasks.md`.
- [ ] 1.5 Verify the linked feature specification maps every requirement and
      scenario in this amendment without reopening the ratified witness
      configuration or importing provider/runtime enforcement.

## 2. Linked Feature Acceptance

- [ ] 2.1 Accept feature evidence that the shared realization creates the
      `chain-anchoring` schemas, examples, and canonical validator from the basis
      plus this amendment, implements the normative realization gate, and rejects
      provisional chain or PKI vocabularies.
- [ ] 2.2 Accept deterministic feature evidence for non-empty, empty,
      midnight-boundary, concurrent close/admission, late-source-time,
      identical-replay, conflicting-dedupe, recursive-control-leaf,
      mid-window eligibility activation, eligibility-content substitution,
      split-witness-root, substituted manifest/configuration/profile, missing
      witness-commitment path, and selectively omitted daily-window cases.
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
- [ ] 2.5 Record contract realization separately from runtime commissioning. If a
      participating runtime is claimed, require its signed-log instance identity,
      signer chain, custody owner, reachable interface, current checkpoint, and
      successful canonical-validator result; otherwise state that no runtime was
      commissioned.

## 3. Validation, Release, and Closure

- [ ] 3.1 Run strict validation for this change and the complete OpenSpec corpus,
      plus the repository's targeted and full validation gates; retain exact
      command results and resolve every finding before acceptance.
- [ ] 3.2 After the shared feature merges green, archive
      `add-chain-anchoring` FIRST to create canonical `chain-anchoring`, then
      archive this amendment SECOND; verify all twelve promoted requirements
      byte-for-byte against their two deltas.
- [ ] 3.3 Cut one additive new-family contract minor allocated by merge order
      only after both archives are present, register all contract members and
      digests, and publish immutable release evidence before any consumer claims
      released-contract conformance.
