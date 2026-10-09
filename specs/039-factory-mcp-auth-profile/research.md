# Research: Factory MCP authorization profile

Status: draft
Kind: reference

**Feature**: [`spec.md`](spec.md) · **Plan**: [`plan.md`](plan.md)

The ratified packet decides what the profile requires. This file records how
the realization meets it, wherever the packet leaves the how open or a standard
it cites settles it. Each entry gives the decision, the line that allows or
decides it, and the alternatives rejected. Nothing here changes a requirement
or scenario.

## Starting point, measured

On `main` `93d13d6c`, the synthetic example probed through
`validate(declaration, snapshots)` in a virtual environment built from CI's
hash-locked requirements:

| Declaration | Report on `main` |
| --- | --- |
| the example as shipped (not deployed) | `valid-with-gaps`, no diagnostic |
| service made `deployed`, synthetic host, no block | `valid-with-gaps`, no diagnostic |
| the same with an `auth` block | `invalid`: `schema_oneOf` at `/service` |
| not deployed, with an `auth` block | `invalid`: `schema_oneOf` at `/service` |
| deployed, canonical resource URI with `?q=1`, no block | `valid-with-gaps`, no diagnostic |
| error code `UNAVAILABLE` mapped as a completed evaluation | `invalid`: `outcome_classification_mismatch` at `/tools/0/outcomes/mapping/2` |

This is the starting point `design.md` D7 and D8 describe.

## Decisions

### R-1. The block's field names are D1's, unchanged

**Decision**: `issuer`, `algorithms`, `audience` (`binding`, `value`),
`metadata_path`, `evidence_ids`, `gap_ids`. **Basis**: D1, "field names are the
realization's to confirm, and any rename is recorded in the Speckit feature".
None is renamed, so there is no rename to record. All six are required within
the block: `evidence_ids` and `gap_ids` "follow the tools' rules exactly" (D5),
and a tool requires both.

### R-2. The block is optional in the schema, and its absence is a semantic refusal

**Decision**: `auth` is a property of the `deployed` branch, not listed in its
`required`. The validator reports `hosted_auth_missing` at `/service`.
**Basis**: D1, "Making it structurally required would surface as an
undifferentiated `schema_oneOf` at `/service` … it names nothing."

### R-3. A structural fault inside the block stays `schema_oneOf` at `/service`

**Decision**: the structure pass is unchanged and does not descend into the
`oneOf` branches. **Basis**: `tasks.md` 2.2 expects exactly that code and
location for every closed-shape fault. D7 says naming the field "is a validator
change the realization may make … This packet does not choose." **Alternatives
rejected**:

- Flattening the selected branch's errors would change the code and location
  of every existing fault under `service` too. That moves behavior the
  packet does not touch, and contradicts task 2.2's text.
- Moving the closed-shape checks into the semantic pass would duplicate the
  schema in code, which feature 037's design keeps out.

### R-4. No JSON Schema `format` on the issuer, the audience or the metadata path

**Decision**: these three are plain bounded strings in the schema. Their rules
are semantic checks written with the standard library, as
`canonical_resource_uri`'s already are (`resource_uri_ok`). **Basis**: D7 places
`invalid_issuer` at `/service/auth/issuer`, in the semantic dimension. A
`format` keyword is checked only when an optional package is installed. With
it, a runtime-name issuer would fail inside the `oneOf` and read `schema_oneOf`
at `/service`. Without it, the same issuer would read `invalid_issuer`.
Measured: on `main`, a system interpreter that carries such a package gives
four false failures in `tests/factory-mcp/` (`invalid_json_schema` where the
test expects `invalid_pointer`), and a virtual environment built from CI's lock
gives none (88 passed, 203 subtests).

### R-5. A query component is a `?` before any `#`, and it is refused on its own

**Decision**: `auth_resource_query` is reported whenever a deployed service's
canonical resource URI has a `?` before any `#`, including an empty query
(`…/mcp?`). It is reported whether or not the block is present, and whether or
not the URI also fails `invalid_resource_uri`. **Basis**: RFC 3986 § 3, "The
query component is indicated by the first question mark ("?") character". The
D7 row's condition, "a deployed service's canonical resource URI carries a query
component", depends on nothing else. The semantic pass reports every condition
it finds; that is the existing rule. **Alternative rejected**:
`urlsplit(uri).query != ""` misses the empty query.

### R-6. The metadata path is derived only from a valid resource URI, and compared exactly

**Decision**: the expected path is `/.well-known/oauth-protected-resource`,
followed by the URI's path (as `urlsplit` returns it, byte for byte) unless that
path is empty or `/`. The block's `metadata_path` must equal it exactly. Port
and query take no part. When the URI already fails `invalid_resource_uri`, the
path is not compared. **Basis**: D4 and OQ-3 (RFC 9728 § 3.1 insertion). An
invalid URI has no RFC 9728 location, and `invalid_resource_uri` already names
the root cause. **Alternatives rejected**: deriving a path from an invalid URI
would report a mismatch against a location that does not exist. Normalizing
percent escapes or trailing slashes would accept paths a client never derives
from the URI it holds.

### R-7. Algorithm names: admitted ones exactly, forbidden ones without letter case

**Decision**: only the exact strings `RS256` and `EdDSA` are admitted. An entry
is `auth_algorithm_forbidden` when it is ASCII and, lowercased, is `none`,
`hs256`, `hs384` or `hs512`. Any other entry is `auth_algorithm_unadmitted`.
A forbidden entry is reported once, as forbidden. `auth_rs256_missing` is
judged separately, on whether the exact string `RS256` is listed. **Basis**: D2
and D7. JWS `alg` values are case-sensitive strings (RFC 7515 § 4.1.1), so
`rs256` is not RS256. D2 compares only the forbidden names "without letter
case". A non-ASCII lookalike is not admitted either, so it is refused under
the general code.

### R-8. The issuer reuses the resource URI's rules, plus no query

**Decision**: `invalid_issuer` unless `resource_uri_ok(issuer)` holds and the
issuer carries no query (R-5's test). **Basis**: D4 requires "an absolute https
URI with a host, and without query, fragment or userinfo". The existing check
already enforces https, a host, a valid port, no userinfo, no fragment and RFC
3986's character set, so issuers and resource URIs meet one rule.

### R-9. Audience faults share one code and one location

**Decision**: `auth_audience_unbound` at `/service/auth/audience/value` when the
value contains `*`, equals the issuer, or (for a `resource_uri` binding) is not
exactly `canonical_resource_uri`. Several faults at once report once (the
existing de-duplication). An `issuer_assigned` value is any string within its
bounds that these rules accept. **Basis**: D3 and D7.

### R-10. The block's support reuses the tools' citation resolution

**Decision**: the loop that resolves a tool's `evidence_ids` and `gap_ids` is
shared with the block. A repeated id is `duplicate_support_reference` at the
list, and a dangling id is `missing_support_reference` at its entry. The block
needs only the `auth` concern, never a tool's six. Its absence from every
resolved record is `unsupported_auth` at `/service/auth/evidence_ids`. **Basis**:
D5 ("resolve exactly as a tool's do") and the D7 rows. The `auth` key is added
to both the evidence and the gap concern vocabularies. On a not-deployed
declaration it is merely admitted.

### R-11. Tests run in a virtual environment built from CI's lock

**Decision**: every local run uses an interpreter whose packages come from
`requirements/hermes-runtime-contracts.lock` with `--require-hashes`, the
command `pytest-suite` runs. **Basis**: R-4's measurement. A system interpreter
carries format-checker packages CI does not, and fails four `main` tests that CI
passes.

### R-12. Bounds

**Decision**: `issuer`, `audience.value` and `metadata_path` are strings of 1 to
2048 characters, the bound `canonical_resource_uri` already has. `algorithms`
is a unique list of 1 to 256 strings of 1 to 256 characters. `evidence_ids` and
`gap_ids` take a tool's bounds (0 to 256 ids of 1 to 80 characters). **Basis**:
feature 037's plan, "Numeric bounds and file organization are implementation
choices below the stated host limit", and its collection bound of 256 items.

### R-13. No secret scanning: the closed shape is the enforcement

**Decision**: "The block SHALL carry no key material, client secret or token"
is met by the closed block. No field can hold one, and an unknown field (`jwks`,
`client_secret`, `token`) is refused as `schema_oneOf`. No heuristic scans
string values. **Basis**: D1, "No field holds a key, a secret or a token". D7
defines no code for a secret-shaped value, and adding one would add a refusal
the packet does not name.

### R-14. M5's mutant run

**Decision**: the two classification tests are run against a mutant of `main`'s
validator. The tree comes from `git archive` of `main` into a scratch
directory, and the mutant removes the comparison in `check_mapping`: the
`if row["is_error"] != error or row["class"] != expected:` line and its `bad(…)`
call. The new test module is copied in and the two tests run. The same two run
against `main`'s own validator. The verification record keeps the diff, the
commands and both results. **Basis**: D8, "shown red against a mutant of
`main`'s validator whose classification comparison is removed, and green
against `main`'s own. The feature's verification record keeps both runs."

### R-15. Two existing tests are amended, because the ratified change reverses their premise

**Decision**: `test_resource_identity_without_optional_format_checker` and
`test_resource_uri_is_https_without_fragment_or_userinfo` build a deployed
service with no block and expect URIs to be judged alone. `design.md`
*Compatibility* reverses that premise: "A deployed declaration without the
block, which is valid today, becomes invalid (`hosted_auth_missing`)". Both are
amended in the red-first commit. They give the deployed service a valid block
with an `issuer_assigned` audience, so they still test the resource URI alone,
and they add `auth_resource_query` where a URI in their list carries a query.
**Alternative rejected**: expecting `hosted_auth_missing` beside each URI
verdict would make every case test two things.

### R-16. The deployed example uses reserved names only

**Decision**: `contracts/factory-mcp/examples/declaration-deployed.example.json`
uses the canonical resource URI `https://mcp.example.test/mcp`, the issuer
`https://issuer.example.test/synthetic`, a `resource_uri` audience, RS256 and
EdDSA, the metadata path `/.well-known/oauth-protected-resource/mcp`, and an
`auth` gap. **Basis**: task 2.2, "Synthetic identifiers only: no real issuer,
tenant, host or domain schema". The `.test` top-level domain is reserved by RFC
6761. A gap, not evidence, supports the block, because no server's token
verification was observed. It shows the scenario "a block supported only by a
gap is reported valid-with-gaps".

### R-17. The version is allocated at the cut

**Decision**: nothing in this feature names a bundle version as decided. At the
stop before task 2.6, the seat computes the next available additive minor
(manifest `contract_bundle_version`, published tags, `contracts/releases/`, #630
row 4 and the open pull requests that touch the release surface) and reports
it. The coordinator claims it on #630, and the cut commit follows. **Basis**:
D10, OQ-5, and `docs/contract-versioning-policy.md` § Bundle Realization Order.

## Out of scope

The change's `tasks.md` § 5: codexFactory's RS256 slice (with its two notes on
the audience binding and the metadata location), OpsxFactory's hosting-plan
issuer correction, the Ops gateway's intake alignment, and any transport
package, server, token minting or client registration.
