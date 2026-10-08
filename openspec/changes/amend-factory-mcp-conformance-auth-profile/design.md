# Design: amend-factory-mcp-conformance-auth-profile

Status: draft
Kind: design
Authored: 2026-10-08, lane `openxfactory-5` (display `openXfactory-5`).

This design carries out three rulings. It does not reopen them. What it adds is
HOW: the block's shape, the validator's stable codes, the contract version, and
six choices the rulings do not settle, each put as an open question with a
recommended answer for the ratify read. See [the proposal](proposal.md) for the
rulings, quoted verbatim.

## Context

Measured on 2026-10-08 against openxFactory `main` `80f47483`:

- `contracts/factory-mcp/declaration.schema.json` describes a service as either
  `{deployment: not_deployed}` or `{deployment: deployed, installation,
  environment, canonical_resource_uri}`, both closed. Nothing describes the
  tokens a deployed server accepts. A binding's authority comes from
  `authority_source: trusted_host`, and the profile fixes `authority_effect:
  none`.
- `scripts/validate-factory-mcp.py` requires a deployed service's
  `canonical_resource_uri` to be an absolute https URI with a host and without
  userinfo or fragment (`invalid_resource_uri`). Its `check_mapping` classes
  each outcome row by its inventory alone: a value of an error inventory must
  be `execution_failure` with `is_error: true`, and a value of a result
  inventory `completed_evaluation` with `is_error: false`
  (`outcome_classification_mismatch` otherwise).
- The declaration is unbundled: `contracts/manifest.yaml` (bundle
  `contract-v4.0`) has no factory MCP row, and the runbook says the additive
  contract version is allocated "only in the later governed realization".

Measured the same day outside this repository, stated at behaviour level
because those repositories are private:

- The engineering domain's hosted adapter is an OAuth 2.1 resource server. It
  accepts only EdDSA, checks its algorithm allow-list before any key lookup,
  refuses `none` and HMAC by name, requires the token's issuer to equal its
  configured issuer, and requires the token's audience to equal its canonical
  resource URI (codexFactory, private, verified 2026-10-08).
- The estate's identity front door verifies RS256 tokens from its Entra
  issuer (the Entra ID v2.0 endpoint), with an audience that is an
  application's client identifier rather than a URI. It never issues tokens
  (xFactory-Hermes-Install, verified 2026-10-08). Microsoft documents that an
  Entra ID v2.0 access token carries the resource application's client
  identifier as its `aud`.
- The approved hosting plan for the engineering domain's server names its
  token issuer by a runtime name rather than an issuer identifier (OpsxFactory,
  verified at its `main` on 2026-10-08).
- The operations domain's DNS check publishes result statuses `blocked` and
  `eligible` only, and reports an unavailable dependency as an error code
  (OpsxFactory, verified at its `main` on 2026-10-08). The engineering domain's
  published domain-error schema carries an unavailable-dependency code too
  (codexFactory, private, verified 2026-10-08).

## Goals and non-goals

**Goals.** One token profile every hosted domain server declares and the
offline validator checks: issuer, algorithms, audience, metadata location. M5's
scenario says what the validator enforces. The capability states where error
vocabularies live.

**Non-goals.** No server, transport package, token minting, key material or
client registration. No change to any domain's published schema. No contract
cut in this packet. No certification: as everywhere in this profile, a valid
declaration returns `verified_conformance: false`.

## Decisions

### D1. The block lives on the deployed service, and nowhere else

The block is a new property `auth` of the `deployed` branch of `service`. The
`not_deployed` branch stays as it is, closed, so a block there is refused the
way any unknown field there is refused today. The resource URI the block
protects is the existing `canonical_resource_uri`. The block does not carry a
second resource field that could disagree with it.

Proposed shape (field names are the realization's to confirm, and any rename
is recorded in the Speckit feature):

```json
"service": {
  "deployment": "deployed",
  "installation": "…",
  "environment": "…",
  "canonical_resource_uri": "https://mcp.example.dev",
  "auth": {
    "issuer": "https://issuer.example/tenant/v2.0",
    "algorithms": ["RS256", "EdDSA"],
    "audience": {"binding": "resource_uri", "value": "https://mcp.example.dev"},
    "metadata_path": "/.well-known/oauth-protected-resource",
    "evidence_ids": ["…"],
    "gap_ids": []
  }
}
```

The block is closed. `algorithms` is a non-empty list of unique strings.
`audience.binding` is the closed set `resource_uri | issuer_assigned`.
`evidence_ids` and `gap_ids` follow the tools' rules exactly. No field holds a
key, a secret or a token: keys are found from the issuer's published metadata,
which is public material.

**Absence on a deployed service is a semantic refusal** (`hosted_auth_missing`
at `/service`), not a structural one. The schema makes `auth` optional in the
`deployed` branch, and the semantic pass refuses its absence. Making it
structurally required would surface as an undifferentiated `schema_oneOf` at
`/service`, because `service` is a `oneOf`. That is stable, but it names
nothing.

### D2. The algorithm rule

- **RS256 is REQUIRED** in every hosted declaration's list
  (`auth_rs256_missing`). It is the one algorithm the estate's only live
  issuer signs, so a server that omits it refuses every real token.
- **EdDSA is OPTIONAL and additive.** A domain that already verifies EdDSA
  keeps it beside RS256. Codex's check-the-allow-list-first design is kept.
- **`none` and HMAC are refused by name** (`auth_algorithm_forbidden`, located
  at the entry). The names are `none`, `HS256`, `HS384` and `HS512`, compared
  without letter case. A resource server that holds only public verification
  material can never have a reason to accept either: an unsigned token proves
  nothing, and an HMAC token's key is shared with the issuer.
- **Every other value is not admitted** (`auth_algorithm_unadmitted`, located
  at the entry), even a sound one such as ES256 or PS256. A further algorithm
  is a governed change to this capability (open question OQ-2). This mirrors
  the engineering adapter's own record that a second algorithm is an additive
  governed change, never a default.

### D3. The audience binding (RFC 8707 § 2)

The MCP authorization model requires a server to accept only tokens issued
for it as their audience. RFC 8707 lets a client name the resource it wants a
token for, but the issuer chooses what it writes into `aud`. So the block
declares the exact `aud` value the server requires, and how that value is
bound to this server:

- **`resource_uri`.** The value MUST equal `canonical_resource_uri`, compared
  exactly (`auth_audience_unbound` otherwise). This is the engineering
  adapter's model today.
- **`issuer_assigned`.** The value is an identifier the issuer assigned to this
  resource alone, such as an application identifier. This form exists because
  the estate's live issuer is the Entra ID v2.0 endpoint, whose access tokens
  carry the resource application's client identifier rather than a URI. The
  validator cannot prove offline that an identifier belongs to this resource
  alone, so the binding rests on the block's cited evidence or gap (D5) and is
  never certified (OQ-1).
- **Refused for either binding** (`auth_audience_unbound`): a value containing
  `*`, or a value equal to the issuer identifier.

Sharing an issuer never makes tokens interchangeable between domain servers:
each server's audience is its own, which is what the brainstorm atom on
service identity already argued.

### D4. Issuer and metadata path

- **Issuer.** An absolute https URI with a host, and without query, fragment or
  userinfo (`invalid_issuer`). That is the form RFC 8414 § 2 and OpenID
  Connect Discovery require of an issuer identifier, and the form a resource
  server compares the token's `iss` against. A runtime or product name (the
  hosting plan's case) is refused. One issuer per hosted server (OQ-6).
- **Metadata path.** The path at which the server serves its RFC 9728
  protected-resource metadata. It MUST equal the well-known location RFC 9728
  § 3.1 derives from `canonical_resource_uri`: `/.well-known/oauth-protected-resource`,
  followed by the resource URI's path when that path is not empty or `/`
  (`auth_metadata_path_mismatch`). So `https://mcp.example.dev` gives
  `/.well-known/oauth-protected-resource`, and `https://host.example/mcp`
  gives `/.well-known/oauth-protected-resource/mcp`. A client can then find the
  metadata without first receiving a 401. The engineering adapter serves its
  metadata at the canonical resource URI followed by the well-known suffix,
  which agrees with § 3.1 only while that URI has no path (codexFactory,
  private, verified 2026-10-08). That is a note for its slice, not a finding
  here (OQ-3).
- **No query on a hosted resource URI.** A deployed service's
  `canonical_resource_uri` carries no query component (`auth_resource_query`
  at `/service/canonical_resource_uri`). RFC 8707 § 2 says a resource
  indicator should not carry one, and the metadata path above is a path field
  that could not represent it. The existing `invalid_resource_uri` check
  admits a query today, so this is a new refusal, and it applies only to a
  deployed service (OQ-3).

### D5. The block cites its support

The evidence and gap concern vocabulary gains one key, `auth`. The block's
`evidence_ids` and `gap_ids` resolve exactly as a tool's do
(`missing_support_reference`, `duplicate_support_reference`), and the block
must cite at least one evidence or gap record carrying `auth`
(`unsupported_auth` at `/service/auth/evidence_ids`). A block supported only
by a gap is valid-with-gaps. This is the profile's existing rule that a claim
names its evidence or stays an explicit gap (OQ-4).

### D6. Optionality: stdio-only declarations

A declaration whose service is `not_deployed` needs no block, and carries
none. Such a server is reached over stdio by a host that launches it. It has no
network resource to protect and no canonical resource URI. The MCP
authorization model applies to HTTP transports, and says a stdio
implementation should take its credentials from its environment instead. The
promoted scenario *Undeployed contract* already says such a declaration makes
no operational URI claim, and an issuer, audience or metadata path would be
one. The engineering domain's stdio adapter is therefore unaffected by this
change.

### D7. Validation

All authorization checks run in the semantic pass, after structure and
references, in the existing `check_catalog` position for service-level checks.
They report in the existing dimensions and stable-ordering rules.

| Code | Dimension | Location | Condition |
| --- | --- | --- | --- |
| `hosted_auth_missing` | semantics | `/service` | a deployed service has no `auth` |
| `schema_oneOf` (existing) | structure | `/service` | a not-deployed service carries `auth` |
| `invalid_issuer` | semantics | `/service/auth/issuer` | not an absolute https URI with a host, or it carries a query, fragment or userinfo |
| `auth_rs256_missing` | semantics | `/service/auth/algorithms` | RS256 is not listed |
| `auth_algorithm_forbidden` | semantics | `/service/auth/algorithms/<k>` | `none`, `HS256`, `HS384` or `HS512`, in any letter case |
| `auth_algorithm_unadmitted` | semantics | `/service/auth/algorithms/<k>` | any other value than `RS256` or `EdDSA` |
| `schema_uniqueItems` (existing) | structure | `/service/auth/algorithms` | an algorithm is repeated |
| `auth_audience_unbound` | semantics | `/service/auth/audience/value` | a `resource_uri` binding names anything but `canonical_resource_uri`, or any audience contains `*` or equals the issuer |
| `auth_metadata_path_mismatch` | semantics | `/service/auth/metadata_path` | not the RFC 9728 § 3.1 location for `canonical_resource_uri` |
| `auth_resource_query` | semantics | `/service/canonical_resource_uri` | a deployed service's canonical resource URI carries a query component |
| `unsupported_auth` | semantics | `/service/auth/evidence_ids` | no cited evidence or gap carries `auth` |

Every row has a red-first test, written before the validator change and shown
failing against the validator on `main` (`tasks.md` 2.2). Probed at `main`
`80f47483`, the starting point is the expected one: the synthetic example with
its service made `deployed` (synthetic host, no block) is `valid-with-gaps`
with no diagnostic, and the same declaration with an `auth` field is `invalid`,
`schema_oneOf` at `/service`. The synthetic example stays `not_deployed`. A
second, deployed synthetic example exercises the block over synthetic
identifiers only: no real issuer, tenant or host.

### D8. The M5 narrowing

**What is enforced.** `check_mapping` already refuses an error-inventory code
classed as a completed evaluation, or marked `is_error: false`, and a
result-inventory value classed as an execution failure. Probed at `main`
`80f47483` with the synthetic example and a synthetic snapshot:

- the error code `UNAVAILABLE` mapped as a completed evaluation is `invalid`,
  `outcome_classification_mismatch` at `/tools/0/outcomes/mapping/2`;
- a result status `dependency_unavailable` added to the result inventory and
  mapped as a completed evaluation is `valid-with-gaps`, with no diagnostic;
- the same status mapped as the scenario demands, as an execution failure, is
  `invalid`, `outcome_classification_mismatch` at `/tools/0/outcomes/mapping/2`.

So the scenario as promoted cannot be enforced, and the error-inventory route
already is.

**Why narrow rather than add a per-row meaning.** A per-row label such as
`meaning: indeterminate` would rest on the author's own assertion and enforce
consistency, not truth. Both real domains already report an unavailable
dependency as an error code. So the scenario is narrowed to the route the
validator can see: inability reported through the error inventory is an
execution failure. The body states the other half outright: result-schema
statuses are completed evaluations. What a result status MEANS stays the
domain's, as the promoted *Honest validation and domain ownership* already
keeps it.

**The narrowed words.** In the body, one sentence is inserted after the first,
and *"inability to evaluate"* gains *"that the domain reports through its
error inventory"*. In *Unavailable dependency*, the WHEN gains *"reports through
its error inventory that it"*. The requirement title, the other sentences, the
scenario's THEN and title, and the other two scenarios are carried byte for
byte (`tasks.md` 1.2 records the diff).

**Red first.** The enforcement already exists, so M5's tests cannot fail
against `main`. They are shown red against a mutant of `main`'s validator whose
classification comparison is removed, and green against `main`'s own. The
feature's verification record keeps both runs. One test refuses an
error-inventory dependency code mapped as a completed evaluation. The other
refuses a result status mapped as an execution failure.

### D9. Per-domain error vocabularies

There is no neutral error-code vocabulary, and the capability now says so.
Each domain keeps its own codes and envelope in its own published schemas. The
profile's lossless mapping (each code's class and isError semantics, with the
domain object unchanged in structuredContent) is the only layer the domains
share. A code name two domains both use carries no shared meaning through the
profile. Nothing in the validator changes: it already reads each domain's codes
from that domain's pinned schema and never compares them across declarations.
The ruled consequence, "No published schema changes", is the requirement's
second sentence.

### D10. Contract versioning

The declaration has never been released. The schema's own title says
"Unreleased", and the manifest has no row for it. So adding a block to the
deployed branch breaks no released shape and no consumer pin. The realization
registers the declaration in the contract bundle for the first time, with its
digest. That is an additive minor under `docs/contract-versioning-policy.md`
§ Change Classes ("new contracts"). It is the next minor after `contract-v4.0`,
`contract-v4.1` if no other cut lands first. The number is allocated AT THE
CUT under § Bundle Realization Order, which forbids reserving it now. Hence
`target_release: deferred-allocation`.

**The cut is realization work, and needs its own claim.** Contract cuts are
substrate row 4 on #630. The realization claims the version number there
before it touches `contracts/manifest.yaml`, `contracts/CHANGELOG.md` or
`contracts/releases/`, lands the cut atomically with the schema, and publishes
the annotated tag after landing. This packet claims nothing in row 4 (OQ-5).

## Compatibility

- **Engineering domain.** Its hosted declaration will fail `auth_rs256_missing`
  until its own RS256 slice lands. That is the intended signal. RS256 alone may
  not be enough. Its audience check compares `aud` with its canonical resource
  URI, while the estate issuer's v2.0 tokens carry a client identifier. Either
  the slice adopts the `issuer_assigned` binding or the issuer is configured to
  emit the resource URI as the audience. That choice is the domain's and the
  host's, not this profile's. Its stdio adapter is unaffected (D6).
- **Operations domain.** The DNS check landed callable-only, with no hosted
  declaration, so nothing of it changes. The gateway's intake design consumes
  this profile at its own task (lane `opsXfactory-4`).
- **Existing declarations.** A not-deployed declaration validates exactly as
  before; the new `auth` concern key only adds an admitted value. A deployed
  declaration without the block, which is valid today, becomes invalid
  (`hosted_auth_missing`), and so does a deployed one whose canonical resource
  URI carries a query (`auth_resource_query`). That is the point of the
  change, and the declaration is unreleased, so no pinned consumer breaks
  (D10).

## Risks and trade-offs

- **An issuer-assigned audience is not mechanically checkable.** Mitigation:
  it rests on cited evidence or an explicit gap, and validity never certifies
  it (D3, D5).
- **A closed algorithm set may lag a domain's needs.** Mitigation: a governed
  addition is cheap. An open set would let each domain drift, which is the
  failure this ruling answers.
- **The metadata-path rule may disagree with an adapter that appends the
  suffix.** The two agree whenever the canonical resource URI has no path. The
  difference is named for the engineering slice (D4).

## Open questions

Each has a recommended answer. A ratify word "as recommended" adopts all six.

| # | Question | Recommended answer |
| --- | --- | --- |
| OQ-1 | Admit the `issuer_assigned` audience binding beside `resource_uri`? | **Yes.** The estate's only live issuer puts a client identifier in `aud`. A resource-URI-only profile would refuse its tokens on audience after admitting them on algorithm. The binding rests on cited support and is never certified. |
| OQ-2 | Keep the admitted algorithms closed at RS256 (required) and EdDSA (optional)? | **Yes.** ES256, PS256 or any other algorithm is a governed change to this capability, matching the ruling's "EdDSA optional" and the engineering adapter's own allow-list discipline. |
| OQ-3 | How is the metadata path derived for a canonical resource URI with a path, and is a query refused? | **RFC 9728 § 3.1 insertion** (`/.well-known/oauth-protected-resource` + the resource path), and **yes, refuse the query**: the requirement, D4 and D7 already carry `auth_resource_query`, because RFC 8707 § 2 says a resource indicator should not carry a query and a path field cannot represent one. The alternative is a metadata URL field in place of the path, which would admit a query. |
| OQ-4 | Must the block cite evidence or a gap under a new `auth` concern? | **Yes**, exactly as tools do for their six concerns. A gap-only block is valid-with-gaps. |
| OQ-5 | Keep `schema_version: 1` and `profile: advisory-v1`, and first-bundle the declaration at the next additive minor? | **Yes.** The declaration was never released, so no consumer pins the shape without the block. A version bump would describe a break no one can observe. |
| OQ-6 | One issuer per hosted server, or a list? | **Exactly one.** Under one server per domain every server faces the same estate issuer. A second issuer is a governed addition when a real need appears. |
