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
python3 -m pytest tests/factory-mcp -q
```

The expected status is `valid-with-gaps` because the synthetic example has no resolving audit sink. Its revision is an explicit synthetic snapshot identifier, not a claimed Git commit. Caller-supplied snapshot roots must be trusted immutable copies; matching file digests establishes supplied-byte integrity, not who produced those bytes or whether a repository actually accepted them.

## Declaration and diagnostics

The root, every nested record, identifiers, modes and authority fields are closed. A tool `id` is one token of ASCII letters, digits, `_`, `.` and `-`, at most 80 characters. Tools name their owning domain; schemas have repository/revision/path/SHA-256 references, and a tool's input, output and error schemas come from the repository and revision that `source` names (`tool_schema_outside_source`). A deployed service's `canonical_resource_uri` is an absolute `https` URI of printable ASCII (an internationalized host is written in its ASCII form) with a host and no userinfo, fragment or backslash. Evidence and gap IDs are unique and concern-tagged; tools must reference support for binding, effects, outcomes, evidence, repetition and limits. Scope gaps, missing revocation and unimplemented audit sinks cannot masquerade as implemented claims.

Effects distinguish external reads, execution, persistence and target mutation. This profile fixes authority to none and target mutation to false. Execution requires a bounded trusted-host declaration. These are checked declarations, not enforcement of the described implementation.

Outcome inventories point to string enum/const nodes, including local references and oneOf/anyOf finite unions. An inventory must be reachable from its schema's root through the subschemas that apply to an instance (`unreachable_inventory` otherwise), so an unused `$defs` entry cannot stand in for the outcome. Under `oneOf` a value counts only when exactly one branch accepts it; a node carrying both `oneOf` and `anyOf`, an `enum` or `const` beside a union, or a `type` that excludes strings is unresolved and needs a gap. When a domain lists its outcomes as a union of object branches, each carrying its code in a property (for example `oneOf` error objects with `properties.code.const`), the inventory points at the union, or at a `$ref` to it, and names that property as its optional `discriminator`. The vocabulary is then the union of every branch's constant or enum for that property, following `$ref`. Each branch must be object-only (`type: object` on the branch or on an enclosing union), list the property in `required`, and constrain it to strings, or the inventory is unresolved. Mapping entries must exhaust each finite inventory without duplicates and preserve the correct completed-evaluation/execution-failure and isError classification. Unsupported narrowing constraints, cycles or unbounded vocabularies require an explicit outcomes gap. Missing pointers are errors, and pointers follow RFC 6901 strictly: an array index is `0` or a digit run with no leading zero, and `~` escapes only `~0` and `~1`.

An inventory inside one member of a union, such as one result variant or one constant of a code union, maps only that member. Every other member of that union must then hold an inventory on the same schema file, or the tool's schema is reported `uncovered_outcome_branch`. Membership is judged by reachability through `$ref`, never through `not` or `if`, so a definition that every variant references covers them all, and a single file cited as both output and error is covered by its result and error inventories together. A `false` member needs no inventory; a `true` member cannot hold one and needs a declared outcomes gap on that schema. A domain output stays verbatim in structuredContent; the declaration never inserts a wrapper into a digested object.

Repetition selects exactly one of reevaluate, lease_replay or fresh_observation. Replay requires persistence, principal-scoped keys, explicit conflict/in-progress handling, coordination and preserved timestamps. Fresh observation requires external reads, observation timestamps, host-controlled age limits and a final age check. Trace IDs are never grants or implicit replay keys.

Reports contain `status`, `exit_code`, `checks`, `diagnostics`, `gaps` and `verified_conformance`. Each diagnostic has a stable code, dimension and JSON-pointer location in the declaration: a reference failure names the citation that failed (for example `/tools/0/input` or `/source/artifacts/0`), and a semantic finding names the field to fix. Identical diagnostics are reported once. Checks that could not run are null, not passed. Diagnostics sort by dimension, location and code. Exit 0 means valid or valid-with-gaps; 1 means an invalid declaration, including malformed or oversized input (`malformed_json`, `duplicate_json_key`, `non_json_number`, `input_size_limit`); 2 means unreadable input or unavailable/unreadable reference roots, and also a command-line usage error such as a malformed `--snapshot`. Human output also prints every explicit gap. Declaration text in human output has control, format and separator characters (and the backslash) escaped, so a declaration cannot add lines or terminal sequences; `--json` output is JSON-escaped.

## Offline reference boundary

Supply one `--snapshot repository@full_revision=root` per immutable snapshot. Every referenced file, including cross-file JSON Schema references, needs a digest-bearing artifact citation. Paths must be normalized relative paths contained under the supplied root. Absolute paths, traversal, URI paths, escaping or looping symlinks, missing artifacts and mismatched digests refuse. The validator never fetches schema resources or executes schema content.

Local fragment pointers and pinned local file references are supported. A subschema carrying its own `$id` is an embedded schema resource, as JSON Schema 2020-12 defines it: a fragment reference inside it resolves against that resource, not the document root, and only a relative non-fragment reference inside it is refused (`relative_reference_in_embedded_resource`). Non-fragment references under a root schema base URI (`unsupported_schema_base_uri`), dynamic/recursive references and named anchors are conservatively refused; ordinary recursive fragment schemas are supported. A root schema ID is metadata for fragment resolution. Every reference, and every inventory pointer, must land on a schema location: annotation data such as `examples`, `required` or an `enum` array, and a map or list of subschemas such as `properties` itself, is refused (`reference_to_non_schema`, or `invalid_inventory_pointer` for an inventory), and a referenced object must pass the metaschema itself (`invalid_referenced_schema`). The reference walk covers every subschema keyword, including `contentSchema`, legacy `dependencies` and `additionalItems`, so no keyword hides a remote reference. Example/default data is not interpreted as schema code. Unknown or unsupported finite-vocabulary constructions require an honest mapping gap instead of an exhaustive claim.

Input is bounded to 256 KiB (`input_size_limit`; the Python entry point measures the compact UTF-8 serialization), each artifact to 1 MiB (`artifact_size_limit`), declaration lists to 256 items, schema graph depth to 128 and schema strings to their published individual bounds. The CLI consumes JSON with duplicate-key/nonfinite-number rejection. The neutral tool `limits` fields describe the domain's host bounds, not limits imposed on that domain by this offline validator.

## Compatibility, release and ownership

[Codex baseline observations](../openspec/changes/add-factory-mcp-conformance/review/codex-baseline-2026-09-07.md) pin revision `4b12ba83add713666a94129fc45552d8989f8488` of `codeXfactory/codexFactory` and the digests of its three published schemas (tool request, tool result, domain error). This profile leaves those schemas, their outputs and client compatibility unchanged. The observation is a compatibility review input, not an executable codex declaration or adoption certificate. codexFactory is private, so this repository carries no codex schema bytes: a reviewer with access validates a codex declaration out of tree, supplying the codex snapshot with `--snapshot`.

DNS behavior remains in OpsxFactory. This repository ships synthetic domain fixtures only.

The profile is unbundled and unreleased. Register manifest/changelog digests, allocate the additive contract version and accept consumer pins only in the later governed realization. This work creates no listener, shared transport, release tag, accepted deployment or production endpoint.

## Implementation records

- [Feature specification](../specs/037-factory-mcp-conformance/spec.md)
- [Plan](../specs/037-factory-mcp-conformance/plan.md), [research](../specs/037-factory-mcp-conformance/research.md), [data model](../specs/037-factory-mcp-conformance/data-model.md), [interface](../specs/037-factory-mcp-conformance/contracts/interface.md), [quickstart](../specs/037-factory-mcp-conformance/quickstart.md), [tasks](../specs/037-factory-mcp-conformance/tasks.md)
- Requirements checklists: [contract](../specs/037-factory-mcp-conformance/checklists/contract.md), [references](../specs/037-factory-mcp-conformance/checklists/references.md), [authority](../specs/037-factory-mcp-conformance/checklists/authority.md), [evidence](../specs/037-factory-mcp-conformance/checklists/evidence.md), [repetition](../specs/037-factory-mcp-conformance/checklists/repetition.md), [compatibility](../specs/037-factory-mcp-conformance/checklists/compatibility.md)
- [Verification record](../specs/037-factory-mcp-conformance/verification.md)
