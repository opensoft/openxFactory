# Supported-Consumer Audit — legacy host-local source metadata (contract-v1.10)

Status: record

**Change**: add-hermes-customer-subject-runtime-contract
**Feature**: 005-customer-subject-runtime · Task T079
**Bundle**: contract-v1.10 · **Date**: 2026-07-14

## Purpose

FR-042 (and the ratified `hermes-governed-record-integrity` scenario "Legacy
local source path is removed") require that removal of legacy host-local
release metadata — specifically `contracts/manifest.yaml`
`source_compatibility_ref.local_source_path` — be preceded by a recorded
repository-wide consumer audit proving no supported consumer requires it, with
canonical source repository and commit provenance retained. This document is
that audit for the contract-v1.10 realization.

## Version allocation

The next available additive bundle version was recomputed at realization after
the final rebase and release lock, trusting the tree rather than planning
memory:

- Local annotated tags present: `contract-v1.7`, `contract-v1.8`,
  `contract-v1.9`.
- Remote (`origin`, read-only `git ls-remote`): `refs/heads/main` =
  `c6f5d6d`; `contract-v1.9` published (`refs/tags/contract-v1.9` ->
  `a16cf39`, peeled `64cc000`); `refs/tags/contract-v1.10*` absent.
- Manifest and changelog baseline before this task: `contract-v1.9`.

`contract-v1.9` was already realized (`64cc000`) and published (evidence
`51a5549`); it is an ancestor of both `origin/main` and this branch. After it
was tagged, two governed review findings hardened release-surface members
(F-U3 `c6f5d6d`: release membership closure + release fixtures + release.py;
F-4/F-7..F-9 `0c1e1b6`: `hermes-operational-postgres-v2.sql`), so the frozen
`contract-v1.9` digest inventory no longer reproduces the current tree. Under
the Immutable Tag Correction policy the `contract-v1.9` tag is never moved;
the corrected bytes ship under the next available additive version.

**The next available additive version is `contract-v1.10`** (minor increment;
additive, non-breaking — `contract_schema_version` unchanged, all v1 contract
paths untouched). No `contract-v1.10` tag exists locally or on the remote.

## Repository-wide consumer audit

`git grep` over the tracked tree for `local_source_path` and
`source_compatibility_ref` yields exactly the following references. Each is
classified; none is a runtime/consumer read of the manifest field as input.

| Reference | Classification |
|---|---|
| `contracts/manifest.yaml` (`source_compatibility_ref.local_source_path`) | The field itself — the removal target. |
| `contracts/hermes-runtime/evidence-register.yaml` (x2) | Evidence bindings naming the test node `test_inventory_never_encodes_a_host_local_source_path` — a *negative* assertion that the release inventory excludes host-local paths, not a consumer of the field. |
| `tests/hermes_runtime_contracts/test_release_inventory.py` (`test_inventory_never_encodes_a_host_local_source_path`) | Test asserting the built inventory encodes no host-local/absolute path; operates on a synthetic repo and never reads the real manifest field. |
| `docs/contract-versioning-policy.md` | Policy prose stating the removal precondition (this audit). |
| `openspec/changes/.../design.md` | Design prose describing the removal process. |
| `openspec/changes/.../specs/hermes-governed-record-integrity/spec.md` | The ratified scenario authorizing the removal. |
| `specs/005-customer-subject-runtime/spec.md` (FR-042) | The requirement. |
| `specs/005-customer-subject-runtime/research.md` | Planning note. |
| `openspec/changes/.../evidence/legacy-source-path-consumer-audit.md` | This audit record. |

No validator (`scripts/validate-*.py`, including the avatar validators that
read `contract_bundle_version`), no `scripts/hermes_runtime_validation/*`
module, and no DomainxFactory `stack.yaml` reads `local_source_path`. Every
supported consumer in the release regression denominator —
`opensoft/AdxFactory`, `opensoft/LedgerxFactory`, `opensoft/MedxFactory`,
`opensoft/OpsxFactory`, `opensoft/codexFactory` (with `opensoft/LegalxFactory`
recorded as an explicit exclusion) — pins openxFactory by canonical repository
plus exact `contract_ref` commit (`3d51c3ed…`), never by a host path.

**Finding: no supported consumer requires
`source_compatibility_ref.local_source_path`.**

## Host-local metadata disposition

`source_compatibility_ref.local_source_path:
/home/brett/projects/Agents/Omnigent-Install` is a host-absolute developer
path. It is unsupported host-local metadata (audit above) and its presence in
a canonical published release-surface member conflicts with the FR-042 rule
that release metadata reject host-absolute paths.

- **Decision: REMOVE `source_compatibility_ref.local_source_path` in the
  contract-v1.10 additive bundle.** The audit licenses and justifies exactly
  this removal and nothing else.
- **Provenance retained** (required by the ratified scenario): the canonical
  source repository (`repo: opensoft/Omnigent-Install`) and the exact
  `source_commit: e254c22ce14e585e909b05c44aed21fd07beba84` remain in
  `contracts/manifest.yaml`. A manifest comment records the audited removal
  and points to this record.
- No other manifest field, and no file outside the five T079-owned files, is
  changed by this removal; it breaks no gate, test, or consumer.

## Conclusion

`contract-v1.10` realizes additively, supersedes the hardened `contract-v1.9`
(whose immutable tag and digest inventory remain as provenance), and removes
exactly one audited unsupported host-local metadata field
(`source_compatibility_ref.local_source_path`) while retaining canonical
repository and source-commit provenance. The removal is governed by this
recorded audit and satisfies FR-042 and the ratified "Legacy local source path
is removed" scenario.
