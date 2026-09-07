# Add Factory MCP Conformance

Status: ratified
Ratified: 2026-09-07 by Brett Heap; record review/ratification-2026-09-07.md
Kind: architecture
Proposed: 2026-09-07
Lane: mcp-family-contract
code_surface: contracts/factory-mcp/, scripts/validate-factory-mcp.py, tests/factory-mcp/
target_release: next additive contract minor, allocated at realization; no release cut in this change

## Why

Agents need to interpret capabilities across domain factories without confusing
a tool's meaning, its operational effects and the authority of its result.
Existing codex tools and a proposed Ops DNS check provide concrete comparison
points before sharing transport implementation.

## What Changes

- Add an advisory conformance declaration describing service/catalog identity,
  authoritative schema references, trusted scope mappings, operational effects,
  outcome/error mappings, evidence disclosure and repetition/limits.
- Deliver an offline schema/semantic validator and domain-independent fixtures.
  Separate declaration validity from behavioral verification and deployment readiness.
- Document source-pinned observations of the existing codex inspect/verify
  boundary, including unresolved mappings, without changing those tools.
- Hand realization to one Speckit feature after ratification. The companion
  OpsxFactory change owns DNS behavior and its domain mapping.

## Capabilities

### New Capabilities

- `factory-mcp-conformance`: a versioned advisory conformance declaration and
  offline validation requirements, preserving domain contracts and ownership.

### Modified Capabilities

None. Existing credential, scope, job, release and domain contracts are consumed
by reference and are not restated as new authority.

## Impact

Neutral schema, semantic validator, synthetic positive/negative fixtures and
mapping guidance live here. DNS request/result/error schemas, policy reuse and
observation interfaces live in OpsxFactory. Actual codex adoption stays with
codexFactory; this change adds no codex field, wrapper or dependency.

No shared transport package, MCP listener, central router, provider reader,
medical tool, host deployment, token minting, release acceptance, tag or pin
advance is included. Future hosted integrations require their own reviewed
authority. The initial profile admits only advisory authority effects.

## Origin and paired handoff

Direct proposal from Brett's 2026-09-07 design conversation; the
[factory-mcp packet](../../../ideation/brainstorm/factory-mcp-overview.md)
preserves the non-normative design history. No staged source existed.
The ad-hoc origin exception is proposed for approval with this packet.

Evidence: [codex baseline](review/codex-baseline-2026-09-07.md) and
[validation/consistency review](review/validation-2026-09-07.md).

Companion: opensoft/OpsxFactory change `add-dns-check-mcp`. Each repository
ratifies its own change and owns one Speckit realization. A shared contract
release and consumer adoption must use the existing release process and
separately reviewed pins; no moving checkout becomes a production dependency.

## Ratification boundary

This packet requests approval of the bounded schema/validator slice and its
proposed origin. It records no approval. Runtime code remains gated by the
repository constitution; the task list records the ratification and handoff.
