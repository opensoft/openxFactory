# Synthesis: OpenProfiler Identity and Runtime — Brainstorm

Status: brainstorm
Kind: architecture
Summary: A typed profile overlay, versioned persona reference, and separated identity stack can produce an auditable model-runtime selection without making any one system own every credential or authority concern.
Topics: openprofiler-identity-persona, openprofiler, profile-account-diff, persona, identity-brokering, keycloak, openxwallet, trust-anchor, synthesis
Repository context: openxFactory cross-factory architecture joining openProfiler with Keycloak, OpenXPKI, openXWallet, and credential contracts
Captured: 2026-08-24

## Possible feats

- **Auditable model-runtime selection** — reproduce which provider account, profile overlay, persona version, authority grant, and trust evidence were active for a run.
- **Cross-system revocation cascade** — stop profile use when the relevant human identity, grant, certificate, persona composition, or provider credential is no longer valid.

## Members and their joints

Atomic members:

- [OpenProfiler Account and Profile Overlay](openprofiler-identity-persona-account-profile.md)
- [OpenProfiler Persona Reference and Composition](openprofiler-identity-persona-persona.md)
- [OpenProfiler Identity, Trust, and Authority Integration](openprofiler-identity-persona-authority.md)

```text
Keycloak subject
    │ authenticates human and organization context
    ▼
OpenXWallet grant ──────┐
    │ authorizes action  │
    ▼                    │
OpenXPKI evidence        │
    │ authenticates       │
    │ device/workload     │
    ▼                    ▼
Profile manifest = account observation + profile overlay + persona reference
    │
    ▼
openProfiler resolves provider credential binding
    │
    ▼
short-lived provider capability -> direct model runtime
```

### Identity and provenance seam

The account/profile document supplies the object being acted upon. The
authority document supplies who may act and which device or workload is trusted.
The persona document supplies what behavior was selected. Their references can
be recorded together without turning a Keycloak subject into a model persona
or a wallet address into proof of human identity.

### Artifact and information flow

The effective profile is derived from provider account facts and explicit
profile overrides. The persona is resolved by reference and verified by its
version/digest. The operation request carries references to both, plus the
wallet grant and PKI evidence. The provider credential or short-lived token is
resolved only inside the protected backend path.

### Authority and lifecycle seam

Read-only discovery can remain local and low-risk. Enrollment, activation,
credential publication, and revocation can require increasingly strong wallet
grants and PKI evidence. If an agent-bearing persona changes composition, its
wallet grants may be revoked immediately; if the provider account credential is
rotated, the profile relationship need not change; if the Keycloak subject is
disabled, future operations must fail closed.

### Latency and operating seam

The provider broker should not be inserted into every interactive model turn.
openProfiler can mint or authorize a short-lived provider capability before the
runtime call, then the provider client calls the model directly. This preserves
the existing `add-model-provider-broker` latency decision while allowing the
profile/persona/authority references to be audited around the turn.

## Emergent behavior

Together, the three ideas create a portable “selected model identity” record:

```text
human subject + authorized operation + trusted client
  + provider account + explicit profile delta
  + persona version + effective digest
  = reproducible runtime posture
```

None of the individual systems can provide this posture alone. Keycloak knows
the human but not the provider credential. openXWallet can authorize an action
but does not define the profile. OpenXPKI can establish trust in a client or
issuer but does not decide which model should run. openProfiler can activate the
provider profile but should not invent the family identity or authority model.

## Tensions to hold

- The current openProfiler application is local-first, while the proposed
  credential-broker design introduces a remote account/profile authority.
- The current cloud design sketches Entra directly; the family direction uses
  Keycloak as the client-facing identity broker.
- A persona can be a harmless presentation reference or an authority-bearing
  agent composition; the security treatment must differ accordingly.
- Wallets and PKI should be available for high-assurance operations without
  making every local read-only profile unusable.

## Recombination opportunities

- Combine the profile overlay with the existing Codex identity/history runtime
  binding so a selected persona is recorded alongside selected history.
- Use the wallet agent composition digest as the persona-bearing profile's
  effective runtime digest when autonomous authority is requested.
- Use a signed profile manifest as the handoff artifact between openProfiler,
  a remote credential broker, and a provider runtime.

## Open questions

- What is the canonical manifest and digest boundary: profile only, persona
  only, or a composed profile-plus-persona artifact?
- Which system owns the durable audit ledger for cross-system operations?
- Can a profile overlay be shared across organizations, or must its authority
  and persona bindings always remain organization-scoped?
- Which revocation events must interrupt an already-running model session?

