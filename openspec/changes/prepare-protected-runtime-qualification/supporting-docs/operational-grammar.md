# Internal operational grammar realization

Status: source candidate; owner review required before runtime use

This is the factory-owned realization of D1/D3 and the categories in
[launch inputs](launch-inputs.md). It supplements the ratified preparation
baseline (factory #1307 at `04fad0559`, adapter #49 at `0a2dda9`) under Brett
Heap's subsequent commissioning of feature 017 T002, after adapter #50 landed.
It changes no accepted possession/observation contract, source-only consumer
lock or frozen origin field. Implementation and its sole task list remain in
`opensoft/openXwallet`, feature `017-protected-runtime-qualification`.

## Closed input

The internal JSON object is bounded to 16 KiB, UTF-8, with duplicate members,
unknown/missing fields and non-finite numbers refused. Canonical SHA-256 uses
the existing RFC 8785 implementation. Versioning is the exact internal profile
`openxfactory-protected-runtime-internal-v1`; this is not a promoted standard.
The implementation defines no public server, consumer execution lock or CLI.

| Field | Required interpretation |
| --- | --- |
| `profile`, `revision` | Exact internal profile and positive safe integer revision |
| `not_before`, `expires_at` | Safe integer UTC epoch interval, active before and after readback |
| `case_ref` | Non-secret operator-selected case handle |
| `sources` | Exactly `factory_profile`, `adapter`, `wallet_contracts`, `wallet_code`, `worker`, `supervisor`, `caller_workflow`, `reusable_workflow`; each has exact `repository`, full lowercase 40-hex nonzero `commit`, safe repository-relative `path` and `digest` of selected content |
| `dependency_digest`, `composition_digest` | Existing SHA-256 notation for exact dependencies and approved composition |
| `issuer` | Exactly `issuer`, `discovery`, `jwks`, `audience`; endpoints are D2's fixed strings, audience explicitly selected |
| `launch` | Exactly the existing twelve expected workload claims plus `run_id` and `run_attempt`; no claim normalization |
| `protection` | Exactly `repository_id`, immutable `environment_id`, exact `environment`, `reviewer_ids`, `prevent_self_review`, `can_admins_bypass`, `deployment_refs` |
| `authority` | Exactly `policy_ref`, `policy_revision`, `policy_digest`, `subject_ref`, `wallet_ref`, `key_ref`, `custody_ref`, `grant_ref`; current canonical authority remains T004/T005 work |
| `services` | Exactly `records`, `challenge`, `registry`, `custody`, `supervisor`, `worker_channel`, `janitor`; each has `service_ref`, `principal_ref`, `credential_ref`, `trust_digest` |
| `state` | Exactly `store_ref`, `initialization_ref`, `retention_ref`, `recovery_ref`; actual private initialized-state enforcement remains T008 work |
| `lifecycle` | Exactly `lease_ref`, `cleanup_ref`, `receipt_retention_ref`; actual leases/finalization/readback remain T009 work |

Handles are bounded namespace identifiers, not URLs, filesystem paths, credentials
or executable resolvers. Missing/null/pending/latest/head/wildcard placeholders
refuse. Numeric GitHub identifiers are canonical positive decimal strings.
Source refs cannot float: an exact workflow branch/tag ref is accompanied by
its separate immutable commit and content digest, and compared with fresh readback.
A workflow ref may instead name that exact commit. Worker source repo/commit match
the expected repository and `sha`; caller/reusable source paths, repositories and
commits match their respective workflow refs and SHA claims.

The initial narrow protection profile requires 1–6 distinct User/Team reviewer
IDs, self-review prevented, administrator bypass disabled, and 1–32 distinct exact
deployment refs including the selected source ref. Environment/repository identity
must match the launch. A broader protection model needs a reviewed grammar change;
an unsupported or unrepresented provider rule cannot be silently dropped by a
readback implementation. Human environment review is not the independent domain
human authentication/consent gate.

## Independent approval and readback

The trusted embedding separately supplies an approved canonical configuration
digest, independently selected readback principal, authenticated bounded readback
callback and trusted clock. These are constructor dependencies, never fields
deserialized from a worker request. The principal differs from the worker-channel
principal. A class instance, identifier or boolean does not prove administrative
isolation/authentication; hosting must enforce that boundary, and deployment
acceptance stays blocked until independently qualified.

Readback JSON has exactly `profile`, `principal_ref`, `case_ref`, `config_digest`,
`launch`, `sources`, `dependency_digest`, `composition_digest`, `protection`,
`services`, `state`, `lifecycle`, `observed_at`, `expires_at`. It is obtained
independently of candidate input and reports measured source and actual effective
protection/selected service context. The callback must not echo the candidate,
omit provider rules or infer protection from a signed environment claim.
Authenticated provider/service acquisition is later hosting work, not something
a synthetic readback proves.

All projection fields match exactly, including canonical types. Readback is current
after blocking I/O, with at most 60 seconds of validity; config expiry may shorten
it further. Clock regression or invalid values refuse. The deeply immutable result
is short-lived. Each later trusted composition must rerun preflight and respect
the earliest deadline; a saved result cannot authorize later use. No daemon or
persistent acceptance cache is supplied.

Approval of an exact candidate is external to it; self-hashes or `approved: true`
cannot establish approval. Service references are resolved only by the trusted
embedding, never dereferenced/imported by the parser. No signer, socket, provider
operation, workflow dispatch or human approval results from validation. The
60-second readback and initial protection profile are candidate realization
choices requiring source review before runtime use. Synthetic tests establish
structural/integrity behavior, not deployed P01/G02/G03 acceptance.
