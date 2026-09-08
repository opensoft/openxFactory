# Synthesis: Governed Source-to-Release Promotion — Brainstorm

Status: brainstorm
Kind: process
Summary: Immutable source pins and a contract release identity gate combine
into a promotion chain that separates evolving brainstorm evidence from
accepted proposal claims and shipped contract artifacts.
Topics: release-lifecycle, contract-release, ideation-lifecycle, provenance, synthesis
Repository context: openxFactory document and contract release exploration
Captured: 2026-07-28

## Possible feats

- **Source-to-release provenance chain** — trace a released capability through
  proposal pins, accepted deltas, promoted specs, package digests, validation,
  and downstream adoption.

## Members and their joints

Atomic members:
[Contract Release Identity Gate](release-lifecycle-contract-identity-gate.md)
and [Immutable Source Provenance](release-lifecycle-immutable-source-provenance.md).

### Capture remains exploratory

Brainstorm leaves preserve alternatives and contradictions. A proposal selects
and pins relevant evidence, then states accepted normative claims explicitly.

### Promotion creates canonical contract state

After implementation and validation, promoted specs and release manifests own
the contract. Supporting brainstorms remain provenance, not shadow standards.

### Adoption verifies the same identity

Stack surfaces and consumers pin the release manifest and prove conformance.
They do not infer compatibility from a branch name or mutable file.

## Emergent behavior

Readers can trace why a contract changed and exactly what shipped without
freezing brainstorm exploration or letting it silently become policy.

## Tensions to hold

- Complete provenance increases archive and tooling complexity.
- Stable leaf paths improve collaboration while accepted source must remain
  reproducible.
- Independent release cadence competes with stack-wide compatibility.

## Recombination opportunities

The packet can supply provenance to the dashboard workbench and to
cross-factory proposal routing without changing their action authority.

## Open questions

- Which provenance links are mandatory at every release?
- When can a generated support snapshot be safely pruned?
- How are emergency releases represented without bypassing the identity gate?
