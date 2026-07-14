# Supported-Consumer Audit — legacy host-local source metadata (contract-v1.9)

Status: record

**Change**: add-hermes-customer-subject-runtime-contract
**Feature**: 005-customer-subject-runtime · Task T079
**Bundle**: contract-v1.9 · **Date**: 2026-07-14

## Purpose

FR-042 requires that removal of legacy host-local release metadata (notably
`contracts/manifest.yaml` `source_compatibility_ref.local_source_path`) be
preceded by a recorded supported-consumer audit. This audit is that record for
the contract-v1.9 realization.

## Version allocation

The next available additive bundle version was recomputed at realization after
`git fetch origin --tags`. Tags `contract-v1.7` (avatar-client kernel) and
`contract-v1.8` (avatar-first UI alignment) were published by other changes
while this feature was in flight, so the planning-time baseline `contract-v1.6`
is stale. The next available additive version is **contract-v1.9**; no
`contract-v1.9` tag exists on the remote.

## Host-local metadata disposition

`contracts/manifest.yaml` retains `source_compatibility_ref.local_source_path:
/home/brett/projects/Agents/Omnigent-Install`, unchanged from `contract-v1.7`
and `contract-v1.8`.

- **Decision: RETAIN as-is; remove nothing in this release.** This bundle
  removes no legacy host-local metadata, so the removal precondition is not
  triggered.
- The release digest inventory and its verifier
  (`scripts/validate-contract-release.py`) key on repository-relative member
  paths only; the pre-existing `source_compatibility_ref` field is not a
  release-inventory member path and is not host-absolute *inventory* metadata.
  It therefore does not fail the release host-path gate.
- No supported consumer in the DomainxFactory regression denominator
  (Adx/Ledger/Med/Ops/codexFactory; LegalxFactory excluded) resolves
  `local_source_path`; each pins openxFactory by canonical repository + exact
  commit (`contract_ref`), not by a host path.

## Conclusion

contract-v1.9 realizes additively with no host-local metadata removal. Should a
future release remove `local_source_path`, a fresh audit under this schema is
required first.
