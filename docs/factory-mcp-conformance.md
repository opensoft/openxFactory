# Factory MCP advisory conformance

Status: draft
Kind: runbook
Governed by: [add-factory-mcp-conformance](../openspec/changes/add-factory-mcp-conformance/proposal.md), ratified 2026-09-07

The unreleased [declaration schema](../contracts/factory-mcp/declaration.schema.json) and [validator](../scripts/validate-factory-mcp.py) check a domain's declared contract offline. They report structural validity, reference integrity, semantic consistency and unresolved gaps separately. Even a valid declaration returns `verified_conformance: false`: source citations still require behavioral review and deployment acceptance.

## Run the synthetic example

From the repository root inside py-bench (Python 3.12 and jsonschema 4.25.1 were used):

```sh
python3 scripts/validate-factory-mcp.py \
  contracts/factory-mcp/examples/declaration.example.json \
  --snapshot synthetic@aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa=contracts/factory-mcp/examples \
  --json
python3 -m unittest discover -s tests/factory-mcp -v
```

The expected status is `valid-with-gaps` because the synthetic example has no resolving audit sink. Its revision is an explicit synthetic snapshot identifier, not a claimed Git commit. Caller-supplied snapshot roots must be trusted immutable copies; matching file digests establishes supplied-byte integrity, not who produced those bytes or whether a repository actually accepted them.

## Declaration and diagnostics

The root, every nested record, identifiers, modes and authority fields are closed. Tools name their owning domain; schemas have repository/revision/path/SHA-256 references. Evidence and gap IDs are unique and concern-tagged; tools must reference support for binding, effects, outcomes, evidence, repetition and limits. Scope gaps, missing revocation and unimplemented audit sinks cannot masquerade as implemented claims.

Effects distinguish external reads, execution, persistence and target mutation. This profile fixes authority to none and target mutation to false. Execution requires a bounded trusted-host declaration. These are checked declarations, not enforcement of the described implementation.

Outcome inventories point to string enum/const nodes, including local references and oneOf/anyOf finite unions. Mapping entries must exhaust each finite inventory without duplicates and preserve the correct completed-evaluation/execution-failure and isError classification. Unsupported narrowing constraints, cycles or unbounded vocabularies require an explicit outcomes gap. Missing pointers are errors. A domain output stays verbatim in structuredContent; the declaration never inserts a wrapper into a digested object.

Repetition selects exactly one of reevaluate, lease_replay or fresh_observation. Replay requires persistence, principal-scoped keys, explicit conflict/in-progress handling, coordination and preserved timestamps. Fresh observation requires external reads, observation timestamps, host-controlled age limits and a final age check. Trace IDs are never grants or implicit replay keys.

Reports contain `status`, `exit_code`, `checks`, `diagnostics`, `gaps` and `verified_conformance`. Each diagnostic has a stable code, dimension and JSON-pointer location. Checks that could not run are null, not passed. Diagnostics sort by dimension, location and code. Exit 0 means valid or valid-with-gaps; 1 means invalid input/declaration; 2 means unreadable input or unavailable/unreadable reference roots. Human output also prints every explicit gap.

## Offline reference boundary

Supply one `--snapshot repository@full_revision=root` per immutable snapshot. Every referenced file, including cross-file JSON Schema references, needs a digest-bearing artifact citation. Paths must be normalized relative paths contained under the supplied root. Absolute paths, traversal, URI paths, escaping symlinks, missing artifacts and mismatched digests refuse. The validator never fetches schema resources or executes schema content.

Local fragment pointers and pinned local file references are supported. Nested schema IDs, non-fragment references under a schema base URI, dynamic/recursive references and named anchors are conservatively refused; ordinary recursive fragment schemas are supported. A root schema ID is metadata for fragment resolution. Example/default data is not interpreted as schema code. Unknown or unsupported finite-vocabulary constructions require an honest mapping gap instead of an exhaustive claim.

Input is bounded to 256 KiB, each artifact to 1 MiB, declaration lists to 256 items, schema graph depth to 128 and schema strings to their published individual bounds. The CLI consumes JSON with duplicate-key/nonfinite-number rejection. The neutral tool `limits` fields describe the domain's host bounds, not limits imposed on that domain by this offline validator.

## Compatibility, release and ownership

[Codex baseline observations](../openspec/changes/add-factory-mcp-conformance/review/codex-baseline-2026-09-07.md) pin repository revision `4b12ba83add713666a94129fc45552d8989f8488` and all three published schema digests. Existing `codex_qa_inspect_patch` reevaluates fixed input/context without ports; `codex_qa_verify_candidate` executes trusted checks and persists principal-scoped lease/replay state. The wire mapping preserves the domain object and maps DomainError to isError true. Their schema shapes and output digests remain unchanged.

Those observations do not resolve the neutral scope tuple, revocation freshness, protected deployment provenance or audit sink. They are a compatibility review input, not an executable codex declaration or adoption certificate. DNS behavior remains in OpsxFactory. This repository ships synthetic domain fixtures only.

The profile is unbundled and unreleased. Register manifest/changelog digests, allocate the additive contract version and accept consumer pins only in the later governed realization. This work creates no listener, shared transport, release tag, accepted deployment or production endpoint.

## Implementation records

- [Feature specification](../specs/037-factory-mcp-conformance/spec.md)
- [Plan](../specs/037-factory-mcp-conformance/plan.md), [research](../specs/037-factory-mcp-conformance/research.md), [data model](../specs/037-factory-mcp-conformance/data-model.md), [interface](../specs/037-factory-mcp-conformance/contracts/interface.md), [quickstart](../specs/037-factory-mcp-conformance/quickstart.md), [tasks](../specs/037-factory-mcp-conformance/tasks.md)
- Requirements checklists: [contract](../specs/037-factory-mcp-conformance/checklists/contract.md), [references](../specs/037-factory-mcp-conformance/checklists/references.md), [authority](../specs/037-factory-mcp-conformance/checklists/authority.md), [evidence](../specs/037-factory-mcp-conformance/checklists/evidence.md), [repetition](../specs/037-factory-mcp-conformance/checklists/repetition.md), [compatibility](../specs/037-factory-mcp-conformance/checklists/compatibility.md)
- [Verification record](../specs/037-factory-mcp-conformance/verification.md)
