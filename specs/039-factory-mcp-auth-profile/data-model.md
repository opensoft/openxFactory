# Data model: Factory MCP authorization profile

Status: draft
Kind: reference

**Feature**: [`spec.md`](spec.md) · **Decisions**: [`research.md`](research.md)

## `service` (existing, a `oneOf` of two closed branches)

| Branch | Fields | Change |
| --- | --- | --- |
| not deployed | `deployment: not_deployed` | none. Still closed, so an `auth` field here is refused as `schema_oneOf` at `/service` (FR-002) |
| deployed | `deployment: deployed`, `installation`, `environment`, `canonical_resource_uri`, **`auth`** | `auth` added as an optional property. Its absence is the semantic refusal `hosted_auth_missing` (FR-001, R-2) |

`canonical_resource_uri` is the protected resource the block describes. The
block carries no second resource field (D1).

## `service.auth` (new, closed)

| Field | Shape | Semantic rule (code at its location) |
| --- | --- | --- |
| `issuer` | string, 1–2048 | absolute https, a host, no userinfo, fragment or query, and RFC 3986 characters: else `invalid_issuer` at `/service/auth/issuer` (FR-004, R-8) |
| `algorithms` | unique array of strings (1–256 items, each 1–256) | `RS256` listed, else `auth_rs256_missing` at `/service/auth/algorithms`. Each entry is `RS256` or `EdDSA`. `none`/`HS256`/`HS384`/`HS512` in any case give `auth_algorithm_forbidden`, anything else `auth_algorithm_unadmitted`, both at `/service/auth/algorithms/<k>` (FR-008 to FR-010, R-7) |
| `audience` | closed object `{binding, value}`. `binding` ∈ {`resource_uri`, `issuer_assigned`}; `value` a string, 1–2048 | `auth_audience_unbound` at `/service/auth/audience/value` if `value` contains `*`, equals `issuer`, or, under `resource_uri`, is not exactly `canonical_resource_uri` (FR-011 to FR-013, R-9) |
| `metadata_path` | string, 1–2048 | equals `/.well-known/oauth-protected-resource` plus the URI's path (unless empty or `/`), else `auth_metadata_path_mismatch` at `/service/auth/metadata_path`. Not compared while the URI is `invalid_resource_uri` (FR-005, R-6) |
| `evidence_ids` | array of ids (0–256, each 1–80) | each id resolves to an evidence record, else `missing_support_reference` at `/service/auth/evidence_ids/<k>`. A repeat gives `duplicate_support_reference` at `/service/auth/evidence_ids` (FR-007, R-10) |
| `gap_ids` | array of ids (0–256, each 1–80) | the same rules at `/service/auth/gap_ids[/<k>]` |
| (block) | — | at least one resolved record carries `auth`, else `unsupported_auth` at `/service/auth/evidence_ids` (FR-007) |

All six fields are required, and any other field is refused. A fault in this
shape reads `schema_oneOf` at `/service` (FR-003, R-3).

**Service-level rule beside the block**: a deployed service whose
`canonical_resource_uri` has a `?` before any `#` gives `auth_resource_query`
at `/service/canonical_resource_uri`, with or without a block (FR-006, R-5). The
existing `invalid_resource_uri` rule is unchanged.

## Concern vocabulary (existing, extended)

`evidence[].concerns` and `gaps[].concerns` admit one more key, `auth`, beside
`binding`, `effects`, `outcomes`, `evidence`, `repetition`, `limits`, `scope`,
`audit` and `revocation`. A tool still needs its six concerns. The block needs
only `auth`.

## Outcome mapping (existing, unchanged; M5 narrowed)

Each mapping row's `class` and `is_error` follow its inventory alone. A value of
an `error` inventory is `execution_failure` with `is_error: true`. A value of a
`result` inventory is `completed_evaluation` with `is_error: false`. Anything
else is `outcome_classification_mismatch` at `/tools/<i>/outcomes/mapping/<k>`
(FR-014). A dependency failure is an execution failure only when the domain
reports it through its error inventory. What a result status means stays the
domain's (D8).

## Error vocabularies (no new entity)

There is no neutral error-code list. Each declaration's codes are read from
that declaration's own pinned error schema, and no two declarations are ever
compared (FR-015, D9).

## Report (existing, unchanged)

`status`, `exit_code`, `checks` (`structure`, `references`, `semantics`),
`diagnostics` (`dimension`, `code`, `location`, sorted and de-duplicated),
`gaps`, and `verified_conformance: false`. The new codes are all `semantics`,
except the closed-shape faults, which are `structure` (`schema_oneOf`).
