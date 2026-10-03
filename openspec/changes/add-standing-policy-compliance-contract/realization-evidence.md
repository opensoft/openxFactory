# Standing-policy compliance realization evidence

Status: record
Recorded: 2026-10-03

## Published neutral implementation

[PR #514](https://github.com/opensoft/openxFactory/pull/514) merged on
2026-08-30 at `ec8be5aa62179713f37ee12dab53a948d791e147`. Its final
`pytest-suite`, `wallet-validation` and `merge-master-approval` checks passed.
The consolidated implementation includes `887291027`; the older archival
branch is a pre-integration development snapshot, not an unpublished feature.

The annotated remote tag `contract-v2.3` has tag object
`9fe9a742217ff830d84bb77d1a696589aca311c0` and resolves to the same merge
commit. Remote refs were checked on 2026-10-03, and the current release
validator's `verify-tag --remote origin --tag contract-v2.3` returned no
findings. The tag and its original inventory remain immutable.

## Recovery of a bounded-read check

The archive checked an immutable Git blob's advertised size before reading its
content. The consolidated implementation checked the budget after loading the
blob. Recovery restores an optional pre-read ceiling in `resolve_git_object`
and passes the compliance input budget from both trusted source and family
readers. Existing resolver condition codes and sanitized Git environment are
preserved. The default resolver call retains its original behavior.

Regression cases use a real Git repository, exercise both authority readers,
and prove an over-budget blob invokes no content read. Exactly-at-budget
content remains accepted. The regression failed on both over-budget cases
before the fix and all four cases pass after it. The existing exact-object
resolver tests also pass (24 tests including the new budget cases).

Current recovery verification: 37 focused release-boundary, authority-budget
and exact-object tests passed. The broader compliance/Hermes non-PostgreSQL
suite passed 929 tests with one release-mode CLI timeout. That same test also
timed out with the recovery code removed and identical materialized submodules;
without those submodules it completed in four seconds. The timeout is a
baseline environment failure, not claimed as a passing check.

The family validator and this change's strict OpenSpec validation pass.
Repository-wide strict validation passes 110 items and fails the unchanged
`add-chain-attestation` delta because its modified requirement omits canon's
legacy no-attestation scenario. Publication requires either correction of that
governance failure or an explicit user exception under constitution V.

## Disposition of the remaining archival differences

99 of the archive's 148 changed paths match the consolidated integration
commit. The release allocation advanced from the archived v2.1/v2.2 candidates
to published v2.3. The two old membership/inventory tests are covered by the
current atomic release-boundary tests, which also refuse incomplete
registration and missing members. Release and CLI helper splits were
consolidated into the landed modules; their original source remains in the
verified recovery bundle. PostgreSQL evidence belongs to the immutable
published release, not the discarded candidate inventory.

The pre-read ceiling above is the behavioral gap recovered from this audit.
No old release inventory, registration, or tag is restored by this change.

## Remaining governance obligations

The named codexFactory first-conformer handoff and FEAT-003 runtime evidence
remain outstanding in this change's task list. Cleanup establishes neutral
implementation/release evidence only; the OpenSpec archive gate remains open.
This recovery fix is an implementation correction to the bounded-input
contract and has not allocated a new contract release.
