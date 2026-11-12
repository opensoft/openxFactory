# Proposed internal operational projection and qualification inputs

Status: draft; not a published contract or runtime configuration

The trusted embedding selects all groups below. This document defines required
input categories for implementation planning; it supplies no executable JSON,
secret, approved endpoint deployment or domain dependency lock. Field grammar,
validator and protection binding must be owner-reviewed before runtime use.

The subsequent T002 source realization is specified in
[internal operational grammar](operational-grammar.md). It is a review candidate,
not an approved live selection or operational grant. This appendix does not
rewrite the original preparation's recorded selection state below.

| Group | Required binding / independent evidence | Present selection |
| --- | --- | --- |
| Source | Accepted factory profile commit/content hash, adapter source/dependencies, neutral owner source/contracts, supervisor/worker source and configuration measurements | Source baselines recorded below; new runtime sources unimplemented |
| GitHub issuer | Exact issuer `https://token.actions.githubusercontent.com`, discovery `https://token.actions.githubusercontent.com/.well-known/openid-configuration`, JWKS `https://token.actions.githubusercontent.com/.well-known/jwks`; explicit audience and configured subject | Endpoints proposed; audience/subject not selected |
| Launch | Immutable repository/owner IDs; caller and reusable workflow refs/SHAs; environment protection/readback; source ref/SHA; case-bound run/attempt | No approved workflow/environment/source/run selection |
| Authority | Current canonical actor/wallet/key/custody/grant chain and conservative existing act/object scope | No runtime authority grant selected |
| Challenge | Authenticated configured service identity, current canonical challenge, request/subject/run binding and source of trusted time | No service/client selected |
| Supervisor | Separate administrative plane/principal/key; protected observation policy and actual launch measurement; worker denial evidence | Not deployed or qualified |
| Gate/custody | Gate deployment/credential bound to approved source/launch, opaque owning signer, transport trust and strict subject/sign-only policy; direct worker sign denial on a valid preimage | Reference behavior only; deployed credential/confinement absent |
| Replay | Protected store identity, existing initialized state, restart continuity and no active-scope restore; retention and recovery authority | No live state selected |
| Lifecycle | Run-owned leases, cancellation behavior, independent janitor/readback identity, deadlines and redacted receipt retention | No operational selection |

Source baselines: factory binding merge `a3e1471f5ea0ec536d4b6b2f82af9c3cc2939b58`;
adapter merge `336055fde62e45b49c5ff45cee36e1152ca695f1`, tree
`2de0fdcdc7c392033fc51c0b84ca2ed9babc2344`; accepted owning wallet code
`bb0e9dae89a771b05f6c235d0a77237288b95c85`. These are source evidence, not a
selected execution stack. Each domain records its own identity readback and
separate tooling/runtime selections in its owning repository. No domain-specific
repository ID, workflow, subject or policy is selected by this neutral packet.

Credential/private-key material is supplied only to trusted deployment handles,
never committed or retained in receipts. Untrusted requests cannot override any
input above. A human environment reviewer is not the separate domain human
authentication/consent gate. No input category is filled with an invented service.
