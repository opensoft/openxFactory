## 1. Ratification and predecessor gate

- [ ] 1.1 Obtain and record explicit ratification of this successor's proposal, design, capability delta, ownership boundary, and one-feature handoff.
- [ ] 1.2 Verify `add-signed-execution-chain` realization from durable evidence: released tranche-one contracts, append-only signed transparency log, canonical validator, live required-check ruleset state, and realization verification.
- [ ] 1.3 Verify the PKI plane is real from durable `trust-anchor`-conformant issuance, verification, revocation, and declared chain-custody evidence; do not accept an install-repository seed, contract pin, planned topology, or workflow as sufficient.
- [ ] 1.4 Record the exact realized tranche-one and PKI artifact versions and digests this successor consumes; do not accept proposal text or workflow presence as realization evidence.
- [ ] 1.5 Reconcile this packet against the realized tranche-one contracts and PKI evidence and update the OpenSpec artifacts before handoff if any leaf, digest, checkpoint, verifier, or signer-trust assumption differs.
- [ ] 1.6 Run strict OpenSpec validation after the reconciliation and leave the handoff blocked if either predecessor gate or validation is incomplete.

## 2. Single Speckit feature handoff

- [ ] 2.1 Commission exactly one Speckit feature for the entire anchoring realization after Section 1 is complete; create no parallel feature for Kaspa, Bitcoin/OpenTimestamps, receipts, or validators.
- [ ] 2.2 Carry this proposal, design, and `signed-execution-chain-anchoring` delta into that feature as its governance source without duplicating an executable implementation task list here.
- [ ] 2.3 Obtain and record versioned operator approval for Kaspa and Bitcoin confirmation profiles, including submitted/confirmed evidence rules and transition test vectors; leave schema and validator authoring blocked rather than allowing the feature to choose unresolved thresholds.
- [ ] 2.4 Require the feature plan to fix canonical byte encodings, keyed-commitment construction, deterministic empty root, retained-proof vectors, deterministic acceptance-time/dedupe/sequence rules, permissioned consent-checkpoint vectors, and adapter conformance vectors against the approved profiles before schema authoring.
- [ ] 2.5 Confirm the feature scope contains only openxFactory-owned contracts, examples, adapter ports, consistency rules, and reference validators, with no deployable gateway or anchoring runtime and no medical policy.

## 3. Governed realization acceptance

- [ ] 3.1 Accept the feature only when its evidence covers the provider-neutral off-chain gateway boundary, the neutral permissioned consent-checkpoint/state-root seam, asynchronous `anchor_pending`, and distinct submitted and confirmed states without treating network publication as authorization.
- [ ] 3.2 Accept the public-artifact contracts only with positive and refusal evidence for opaque keyed commitments, PHI, encrypted PHI, plain hashes, stable public identifiers, weak or reused secret inputs, and payload-shaped records.
- [ ] 3.3 Accept the Kaspa profile only with direct L1 operational witnessing and independently replayable retained transaction, DAG inclusion, header, version, and confirmation-policy proof after ordinary-node pruning.
- [ ] 3.4 Accept the durability profile only with complete fixed-UTC 24-hour reconciliation driven by trusted log acceptance time and monotonic leaf sequence, stable dedupe, exact-once paths, closed-window immutability, prior-window lateness recording, and a signed empty continuity checkpoint through the same OpenTimestamps/Bitcoin path.
- [ ] 3.5 Accept confirmation and receipt verification only when the operator-approved profile versions and their transition vectors pass, pending, submitted, confirmed, invalid, and unevaluable results remain distinct, and long-horizon durability requires confirmed Bitcoin evidence.
- [ ] 3.6 Verify Toccata has no v1 production role beyond isolated experiments and Kasplex and Igra remain outside v1; record no future adoption trigger, because a future governed change decides contract code on then-current merits and evidence.
- [ ] 3.7 Register and release the additive contract surface under the bundle version allocated at realization, using the repository's release-realization and independent verification rules.
- [ ] 3.8 Record the landed Speckit feature and verification evidence in this change, and archive the change only after that single feature and its pull request have landed.
