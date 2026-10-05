# Codex compatibility baseline

Status: record
Kind: report
Lane: mcp-family-contract
Captured: 2026-09-07

Repository: opensoft/codexFactory.
Inspected source revision: 4b12ba83add713666a94129fc45552d8989f8488.
This is a source observation, not artifact acceptance, runtime certification
or a change to the codex contract.

Paths below are relative to that source repository.

| Artifact | SHA-256 |
| --- | --- |
| packages/codexfactory-mcp-contract/schemas/tool-request.schema.json | 2b443f76530de1528359c0d8c9d8ff7a45f82ebaa8c06ffa53c67a59897d5e3b |
| packages/codexfactory-mcp-contract/schemas/tool-result.schema.json | 907352c252dd14e569e5d388bebb6f36152ffe9be5e87b11ce4269f5a079426c |
| packages/codexfactory-mcp-contract/schemas/domain-error.schema.json | 590fb7f9db6a0cf6ad6a5bb15467ff5feae8ac748f99f0c2f78ec590f6854750 |

The source prefix for the following modules is
packages/codexfactory-mcp-contract/src/codexfactory_mcp_contract/.

- wire/tools.py declares exactly inspect and verify in TOOL_ORDER and derives
  descriptors from the published schemas. Its outputSchema includes the
  corresponding result variant and the domain-error schema.
- service.py shows inspection using trusted context and verification acquiring
  an idempotency lease, invoking the trusted runner and committing the outcome.
- wire/outcomes.py supplies the shared domain-to-wire result mapping.

The two compatibility witnesses are codex_qa_inspect_patch and
codex_qa_verify_candidate. The proposed profile must preserve their schemas,
tool order, result objects and replay meaning.

Unresolved before adoption: complete neutral scope-tuple mapping, runtime
revocation freshness, deployment provenance association, audit-sink resolution
and behavioral conformance evidence. The neutral document does not resolve
those by adding caller fields or changing a domain result.

See the [design](../design.md) and [proposal](../proposal.md).
