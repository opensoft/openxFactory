---
code_surface: openxFactory
target_release: deferred-allocation
sequenced_after: [qualify-private-connectivity-production, implement-private-connectivity-binding]
---

# Proposal: Publish the supported private connectivity binding contract

Status: ratified
Ratified: 2026-11-14 by Brett Heap. [Ratification record](review/ratification.md)
Kind: proposal
Proposed: 2026-11-13

## Why

The neutral binding schema and reader used by feature 040 still reference a feature-local draft outside the published contract bundle. Feature 043 needs a supported, compatible neutral release and verified consumer handoff before customer qualification can rely on it.

## What Changes

- Propose publication of the domain-neutral optional binding contract, documentation and conformance corpus under contracts/private-connectivity, preserving the ratified binding/endpoint/access/route/lifecycle semantics and unbound compatibility.
- Propose moving the existing neutral reader to the supported schema and adding conformance/publication regressions within the exact [design scope](design.md). Preserve feature 040 schema and evidence as historical records.
- Require the existing atomic contract cut: schema/contract files, manifest, changelog and generated release inventory, with version allocation at the approved realization cut, reviewed landing and annotated-tag publication/readback.
- Require exact commit/content compatibility evidence before separately authorized owners accept consumer pins. Neither a feature-local draft, mutable branch/tag alone nor a passed fixture qualifies a supported customer release.
- Hand scope acceptance to feature 043 T016 and publication/readback to T018–T019 in its sole executable task list. E owner acceptance at T006 does not grant this separate neutral publication scope.

## Capabilities

### New Capabilities

- private-connectivity-contract-publication: supported neutral binding publication, preserved conformance, normal atomic release identity and verified consumer handoff.

### Modified Capabilities

None. Existing private-connectivity semantics, versioning, release realization and managed-subject requirements remain in force. A behavior change or a required edit outside the proposed exact scope returns to its owning decision.

## Impact

The accepted owner is Brett Heap as opensoft/openXfactory's neutral publication/release maintainer; see the ratification record. Proposed surfaces are the binding schema/documentation/corpus, current reader and directly affected tests, manifest/changelog, the one generated release inventory selected at the actual cut and T018/T019 publication/readback receipts.

No version is reserved, file is published, tag is created, consumer pin is advanced or release gate is passed by this draft. No provider, identity, installer, product, domain or operational runtime scope is granted. Actual neutral scope/release authority is required at T016 and the cut. Runtime owners retain their own source, release and target approvals; Q0 remains unaccepted and Q1–Q5 unentered.

Draft publication: [PR #1310](https://github.com/opensoft/openXfactory/pull/1310). See [production policy](../qualify-private-connectivity-production/proposal.md), [design](design.md), [requirements](specs/private-connectivity-contract-publication/spec.md) and [governance handoff](tasks.md).
