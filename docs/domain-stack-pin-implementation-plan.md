# Domain Stack Pin Implementation Plan

Status: planned
Repository context: openxFactory
Purpose: define how every DomainxFactory declares the exact `openxFactory`
contract version it consumes, and how the top-level `xFactory` aggregation repo
can generate those pins from submodule state.

## Goal

Every DomainxFactory must know which `openxFactory` version it runs against.
The authoritative declaration belongs in the DomainxFactory `stack.yaml`, not
only in the parent `xFactory` aggregation repo.

The parent `xFactory` repo may pin a workspace snapshot with submodules, but a
DomainxFactory must remain independently auditable after it is cloned,
deployed, packaged, or released.

## Required `stack.yaml` Shape

Add or normalize this block in each DomainxFactory:

```yaml
xfactory:
  contract_repo: github.com/opensoft/openxFactory
  contract_name: openxFactory
  contract_ref_type: commit
  contract_ref: <openxFactory commit sha>
  contract_schema_version: 1
  contract_declared_at: "YYYY-MM-DD"
  contract_source: xFactory-submodule-pin
```

When `openxFactory` starts publishing release tags, prefer tags for stable
domain releases:

```yaml
xfactory:
  contract_repo: github.com/opensoft/openxFactory
  contract_name: openxFactory
  contract_ref_type: tag
  contract_ref: v0.1.0
  contract_schema_version: 1
  contract_declared_at: "YYYY-MM-DD"
  contract_source: release
```

## Current Normalization Needed

The current domain repos are mixed:

| DomainxFactory | Current state | Required action |
| --- | --- | --- |
| `AdxFactory` | references `github.com/opensoft/openWorkflow`; no pin | rename to `openxFactory`, add commit pin |
| `LedgerxFactory` | references `github.com/opensoft/openWorkflow`; no pin | rename to `openxFactory`, add commit pin |
| `MedxFactory` | references `github.com/opensoft/openWorkflow`; no pin | rename to `openxFactory`, add commit pin |
| `OpsxFactory` | references `github.com/opensoft/openxFactory`; no pin | add commit pin |
| `codexFactory` | references `github.com/opensoft/openWorkflow`; compatibility text only | rename to `openxFactory`, add commit pin |

## Pin Source

For workspace-generated pins, read the parent `xFactory` submodule state:

```bash
git -C /path/to/xFactory rev-parse HEAD:openxFactory
```

That returns the `openxFactory` commit the workspace is using. The generator
should write that value into each DomainxFactory `stack.yaml`.

For standalone domain work, a maintainer may provide an explicit ref:

```bash
scripts/set-domain-openxfactory-pin.py \
  --domain /path/to/MedxFactory \
  --openxfactory-ref 36efa8578800354ea3909c3a4681b02df5ec9375
```

## Implementation Tasks

1. Add a stack pin schema section to the domain stack schema.
2. Add a generator script that can update one or more DomainxFactory
   `stack.yaml` files.
3. Add a validator that fails when:
   - `xfactory.contract_repo` is not `github.com/opensoft/openxFactory`
   - `xfactory.contract_name` is not `openxFactory`
   - `xfactory.contract_ref_type` is missing or not `commit` or `tag`
   - `xfactory.contract_ref` is missing
   - `commit` refs are not 40-character Git SHAs
   - `tag` refs do not match the allowed release-tag pattern
4. Run the generator against all current DomainxFactory repos.
5. Commit each DomainxFactory pin update in its own repo.
6. Push the DomainxFactory commits.
7. Update the parent `xFactory` submodule pins to the new DomainxFactory
   commits.
8. Commit and push the parent `xFactory` aggregation repo.

## Upgrade Flow

When `openxFactory` changes:

```text
openxFactory change lands
  -> parent xFactory updates openxFactory submodule pin
  -> generator updates DomainxFactory stack.yaml pins
  -> domain validation runs
  -> each DomainxFactory commits the new compatibility pin
  -> parent xFactory updates DomainxFactory submodule pins
```

This makes upgrades explicit. Domain repos do not silently move to a new
contract just because `openxFactory` changed.

## Release Tags

The first implementation may use commit SHAs. Before external tenant rollout,
`openxFactory` should publish release tags and a short compatibility note for
each tag.

Recommended first tag shape:

```text
v0.1.0
```

After tags exist, DomainxFactory releases should use tag pins unless they are
testing unreleased contract work.

## Open Questions

- Should the parent `xFactory` generator update dirty DomainxFactory repos, or
  refuse until each domain repo is clean?
- Should tenant records inherit the DomainxFactory `stack.yaml` pin by default,
  or repeat the pin for deployment-time audit?
- Should `openxFactory` publish a machine-readable contract manifest per tag?
