# Contract Release Identity Gate — Brainstorm

Status: brainstorm
Kind: process
Summary: A contract release should bind immutable source, package, schema,
conformance, validation, compatibility, and signer identities before a tag or
stack surface may claim the release.
Topics: release-lifecycle, contract-release, release-identity, conformance-gate
Repository context: openxFactory contract and stack-surface release exploration
Captured: 2026-07-28

## Possible feats

- **Contract release manifest** — bind source revision, package digest,
  capability and schema versions, validation evidence, compatibility, and
  signer.
- **Stack-surface admission check** — reject consumers that claim a release
  without matching manifest and conformance evidence.

## Focus

This document isolates the identity of a released contract. A Git tag,
package version, schema value, and deployment surface should not drift into
separate claims about what was released.

## Proposed model

The gate evaluates a release candidate containing:

- owning repository and exact source revision;
- contract/capability identifiers and versions;
- packaged artifact digests and dependency pins;
- schema and validator versions;
- conformance and compatibility evidence;
- release signer and timestamp;
- superseded release and rollback instructions.

Only the resulting manifest may authorize a downstream stack surface to claim
that release identity.

## Interfaces and boundaries

The source gap analysis lives in
[Contract Release and Stack-Surface Gaps](contract-release-and-stack-surface.md).
This gate does not choose semantic versioning policy for every capability or
replace domain acceptance.

## Alternatives and tensions

- One global release manifest improves consistency but couples independent
  contract families.
- Per-capability manifests reduce coupling and make stack-wide compatibility
  harder to understand.
- Signed attestations improve provenance while key custody becomes critical.

## Open questions

- Which versions must advance together?
- What evidence proves compatibility across a stack surface?
- Who signs neutral versus domain contract releases?

## Relationships

The source evidence needed by the gate is pinned through
[Immutable Source Provenance](release-lifecycle-immutable-source-provenance.md).
