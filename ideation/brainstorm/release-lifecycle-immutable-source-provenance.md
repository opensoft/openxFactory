# Immutable Source Provenance for Ideation and Release — Brainstorm

Status: brainstorm
Kind: architecture
Summary: Brainstorm leaves may remain at stable live paths while proposals
and releases consume pinned path, revision, and digest identities plus
generated evidence snapshots.
Topics: release-lifecycle, ideation-lifecycle, pin-manifest, provenance
Repository context: openxFactory document-lifecycle evolution exploration
Captured: 2026-07-28

## Possible feats

- **Leaf pin manifest** — cite a source path, Git revision, content digest,
  capture identity, and selected passages at a proposal or release gate.
- **Generated support snapshot** — materialize a reviewable bundle from pins
  without making the snapshot a new canonical source.

## Focus

This document isolates source identity across a lifecycle where brainstorm
documents continue evolving. Consumers of an accepted proposal or release
need the exact evidence reviewed at the gate, not whatever the live file says
later.

## Proposed model

A pin contains repository identity, path, source revision, digest, capture
metadata, and optional passage selectors. The proposal records its pins; an
archive or release process may generate a deterministic snapshot and checksum
manifest from them.

The live brainstorm remains non-normative and may gain new contradictions.
Accepted claims must already be expressed in the proposal and promoted spec;
the pinned source remains provenance.

## Interfaces and boundaries

The immovable-leaf alternative is explored in
[Immovable-Leaf Ideation Lifecycle](immovable-leaf-ideation-lifecycle.md).
The current ratified lifecycle remains authoritative until changed through an
explicit OpenSpec delta.

## Alternatives and tensions

- Moving source material gives a clear filesystem state but breaks stable leaf
  identity and backlinks.
- Pinning preserves source identity while tooling must resolve and snapshot
  historical revisions.
- Generated snapshots aid archive portability yet can be mistaken for
  canonical policy.

## Open questions

- Are passage selectors stable enough, or should every pin bind the full file?
- How are rewritten Git histories or repository transfers handled?
- Which lifecycle index owns current disposition?

## Relationships

The [governed promotion synthesis](release-lifecycle-synthesis-governed-promotion.md)
joins source pins to contract release evidence.
