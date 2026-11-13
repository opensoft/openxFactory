# Dispatch Bootstrap Candidate Evidence

Status: source candidate; owner acceptance and operation remain separate
Commission: Brett Heap, 2026-11-13; fix through factory/adapter governance and
test in isolation. Setup/dispatch unauthorized; feedback deferred; neither
historical blocked write replayed.

This new change preserves the accepted preparation packet and frozen origin.
The adapter implements the distinct static commitment, independent actual-run
bootstrap and explicit workflow-input migration in feature017 T012B. Its
internal full config digest, signed claims and operation-grant checks retain
their meaning. No neutral contract, consumer pin or runtime deployment changes.

At factory source `d28c33b06604911a6616285ad974d2cbbcaf3220`, the pinned strict
new packet passed. Complete pinned corpus validation had zero undispositioned
failures, with its existing accepted add-chain-attestation scenario exception
explicitly reported; it is not described as an entirely clean corpus. The
dependency DAG passed. The generated ledger added exactly this change's row
with assigned PR #1311 provenance; all other rows are unchanged and the
249-row ledger agrees with the corpus.

An auxiliary broad proposal-support sweep reported missing legacy manifests
in add-workload-factory-binding and prepare-protected-runtime-qualification,
and an absent origin ID in honor-conditional-lane-attribution. Those packets
are byte-identical to this branch's origin/main baseline; this candidate's
strict proposal-support verification passes. No unrelated origin or manifest
is changed or silently dispositioned here. Hosted CI remains an independent
exact-head check.

All nine local expert roles inspected factory `d28c33b` with the paired adapter
`ce8687baa1f6fc703e33be1d41a2e79e3cd4772f`. Initial adapter ordered tests passed
1,348, native network-none matrix 1,046, all zero failures/errors/skips. Security,
reliability and QA independently passed all 161 bootstrap/workflow cases. One
standalone test assertion-scope S5778 finding was fixed at adapter
`38d205c0b6b175afff2b38f2968730a307b74ed9`; corrected standalone analysis reports
zero issues. Fresh complete/native qualification at the corrected test source
is recorded in the adapter's feature017 evidence before publication.

The synthetic authority's locked concurrent claim test models the hosting
contract; it does not provide deployed GitHub authentication, atomic issuance
or administrative separation. Production bindings still refuse before any
environment output or OIDC. T013/T014, protected receipt promotion and human/domain
acceptance remain incomplete. Paired candidate source acceptance is required
before landing; this evidence authorizes no setup, dispatch or release.
