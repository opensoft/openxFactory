# Public interface: what this feature changes

Status: draft
Kind: reference

The interface is feature 037's ([`../../037-factory-mcp-conformance/contracts/interface.md`](../../037-factory-mcp-conformance/contracts/interface.md)):
the schema `contracts/factory-mcp/declaration.schema.json`, and the validator
`scripts/validate-factory-mcp.py` as a CLI and as the callable
`validate(declaration, snapshots)`. This feature changes it only as below.

## Declaration (input)

- **Added**: `service.auth`, optional in the `deployed` branch and closed, as
  [`data-model.md`](../data-model.md) gives it.
- **Added**: the concern key `auth` in `evidence[].concerns` and
  `gaps[].concerns`.
- **Unchanged**: `schema_version: 1`, `kind`, `profile: advisory-v1` (OQ-5), and
  every other field.

## Diagnostics (output)

New stable codes, all in the `semantics` dimension (`design.md` D7):

| Code | Location |
| --- | --- |
| `hosted_auth_missing` | `/service` |
| `invalid_issuer` | `/service/auth/issuer` |
| `auth_rs256_missing` | `/service/auth/algorithms` |
| `auth_algorithm_forbidden` | `/service/auth/algorithms/<k>` |
| `auth_algorithm_unadmitted` | `/service/auth/algorithms/<k>` |
| `auth_audience_unbound` | `/service/auth/audience/value` |
| `auth_metadata_path_mismatch` | `/service/auth/metadata_path` |
| `auth_resource_query` | `/service/canonical_resource_uri` |
| `unsupported_auth` | `/service/auth/evidence_ids` |

Existing codes at new locations: `duplicate_support_reference` at
`/service/auth/evidence_ids` or `/service/auth/gap_ids`, and
`missing_support_reference` at `/service/auth/evidence_ids/<k>` or
`/service/auth/gap_ids/<k>`.

Existing code, new trigger: `schema_oneOf` at `/service` (dimension
`structure`) also reports a block on a not-deployed service and any break of
the block's closed shape.

## Compatibility of the interface

- A not-deployed declaration validates exactly as before.
- A deployed declaration with no block, which `main` accepts, is now `invalid`
  (`hosted_auth_missing`). So is a deployed one whose canonical resource URI
  carries a query (`auth_resource_query`). That is the change's intent. The
  declaration is unreleased, so no pinned consumer breaks (`design.md` D10).
- The report's shape, its ordering and de-duplication rules, its exit codes
  (0 valid or valid-with-gaps, 1 invalid, 2 operational) and its input and
  output bounds are unchanged.
- At the cut (task 2.6), the declaration is registered in
  `contracts/manifest.yaml` for the first time, at the additive minor the cut
  allocates.
