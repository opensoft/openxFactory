# Proposal Ratification: add-standing-policy-compliance-contract

Status: ratified
Decision date: 2026-08-26
Ratifier: Brett Heap (repository owner)
Ratified: 2026-08-26 by Brett Heap — in-session, verbatim: "the 1 is approved
as ratified by Brett".
Ratified baseline: PR #349 as merged at
`e95de149cdabb94fcd9938670df82c8af94ef419`, including the final review-hardening
commit `0b9359fd6ae6a246aba9705e6089c6a984600760`.

## Decision

Brett ratified the complete neutral `intent-compliance` requirement set and
authorized its realization. The ratification covers the five-record family,
the deterministic floor, bounded classifier escalation, loud redacted evidence,
current-state allowance resolution, authenticated revocation authority,
registry-lifetime allowance identifiers, cross-enforcement reference lockstep,
and dispatch serialization against a racing registry-head update.

This record authorizes the implementation tasks; it does not claim that any
schema, validator, bundle release, codexFactory conformer, or FEAT-003 evidence
already exists.

## Required realization sequence

1. Realize and release the neutral openxFactory contract family.
2. Raise the named codexFactory successor against that released bundle.
3. Prove the FEAT-003 no-allowance, valid-allowance, and revoked-allowance paths.
4. Archive only after both the release and first-conformer evidence are merged
   and green.

## Implementation-boundary clarification — 2026-08-26

The phrase “dispatch serialization” above records the ratified security goal,
not a claim that this neutral contract performs runtime linearization. The
openxFactory realization validates caller-trusted snapshots and static
registry-head-conditioned dispatch evidence. Token issuance, single-use or
replay prevention, atomic consumption, worker invocation, and revocation-race
enforcement remain obligations of the consuming domain runtime and its own
realization evidence. This clarification preserves the decision and narrows no
ratified requirement; it prevents implementation evidence from overstating the
neutral layer's operational authority.
