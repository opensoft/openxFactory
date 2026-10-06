# Proposal validation and consistency review — 2026-09-07

Status: record
Kind: report
Lane: mcp-family-contract
Captured: 2026-09-07
Reviewer: authoring Codex session (consistency review, not an independent council)

## Validation scope

Commands ran in the existing py-bench container against this isolated clone.
No implementation, live reader, deployment or runtime test was executed.

- Strict per-change OpenSpec validation: PASS.
- Proposal-support origin verification: PASS. Ad-hoc origin is proposed, not approved.
- Full strict OpenSpec: 97/99 pass. The two errors are pre-existing MODIFIED
  scenario omissions in add-chain-attestation and add-composed-view-authoring.
  Those change directories and their promoted specs are byte-unchanged from
  this clone's HEAD (git diff --exit-code passed).
- Targeted doc-health proposal-origin family: zero findings.
- Targeted status-validity family: three errors, all existing review records in
  add-openspec-cli-pin, bump-openspec-cli-pin-to-1.12 and
  disposition-codexfactory-declared-renames; none is an authored path.
- Brainstorm validator: PASS, fourteen documents (ten atoms, three syntheses,
  one overview), with all packet links and tier coverage valid.

## Consistency checks and dispositions

- The packet is non-normative; proposal Status is draft. The user requested
  documentation and implementation but has not ratified these exact artifacts.
- Each repository declares one new capability, one local code surface and one
  future Speckit feature. OpenSpec records handoff checkpoints without duplicating
  executable feature tasks. No release number is reserved.
- Shared semantics surround domain payloads; structuredContent stays lossless
  and negative findings remain completed evaluations.
- Schema validity, declared behavior, conformance evidence and deployed
  readiness are separate. Missing mappings and runtime support remain gaps.
- DNS complete-absence evidence differs from missing coverage. Staleness,
  unreadability and malformed observations are typed evaluation failures.
- Cancellation cannot be guaranteed for arbitrary synchronous readers; that
  limitation and operational admission requirement are explicit.
- Existing DNS TTL applies to deletion too; the design was corrected to preserve
  it. Domain plan identity uses the existing content projection, while outer
  evidence records actual reader use and timestamped observations separately.
- Neutral semantic checks operate on structured fields and schema enum/const
  projections. A validator cannot infer authorization or exhaustive coverage
  by reading explanatory prose; unsupported mappings are gaps.
- No existing codex schema, DNS planning policy, release manifest, hosting plan
  or consumer pin is modified.

## Disposition

The local draft is ready to present for exact ratification, subject to the
disclosed unrelated baseline findings. This is neither council acceptance nor
a production-readiness claim. Required review and complete repository gates
still apply before publication and realization landing.

See [proposal](../proposal.md), [design](../design.md) and
[governance checkpoints](../tasks.md).
