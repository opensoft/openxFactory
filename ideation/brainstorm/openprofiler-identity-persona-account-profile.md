# OpenProfiler Account and Profile Overlay — Brainstorm

Status: brainstorm
Kind: architecture
Summary: Treat a provider account as verified base identity and a provider profile as an explicit non-secret overlay whose differences can be inspected and reproduced.
Topics: openprofiler-identity-persona, provider-profile, profile-account-diff, openprofiler, credential-contracts
Repository context: openxFactory cross-factory architecture; openProfiler owns provider account and profile behavior
Captured: 2026-08-24

## Possible feats

- **Typed account/profile inventory** — expose verified provider account identity separately from profile metadata.
- **Deterministic profile diff** — show account defaults, profile overrides, and the effective profile without exposing credentials.

## Focus

This document isolates the relationship between a provider account and one or
more profiles that use it. The current openProfiler implementation discovers
and activates local Codex and Claude profiles. It already reads profile names,
families, aliases, and declared identities, and it verifies Codex account IDs
in credential-handling paths, but it does not yet expose a durable account
object or a first-class account-to-profile diff.

The proposed extension makes that relationship explicit without turning
openProfiler into a second provider account system.

## Proposed model

```text
ProviderAccount
  account_ref
  provider
  provider_account_id
  workspace_ref (optional)
  authority_ref
  verification_state
  observed_at

ProviderProfile
  profile_ref
  account_ref
  name / family / aliases
  profile_path
  credential_binding_ref
  persona_binding (optional)
  lifecycle_state

ProfileOverlay
  account_ref
  profile_ref
  changed_fields
  effective_digest
```

The account is the provider's identity and subscription boundary. The profile
is a named operating context over that account. The effective profile is
computed from account defaults plus the profile overlay; it is not a second
copy of the account.

The diff should classify fields rather than compare arbitrary serialized
objects:

- **Provider identity** — provider, immutable account ID, workspace, and other
  provider-confirmed facts.
- **Profile configuration** — name, family, aliases, selected model or
  endpoint, local runtime path, and credential binding reference.
- **Persona binding** — optional persona reference, version, and digest.
- **Lifecycle and observation** — active, ready, revoked, conflicted, last
  observed, and source metadata.

Credential values, access tokens, refresh tokens, and private-key material are
never members of the diff. A credential generation may change while the
account/profile relationship remains unchanged.

## Interfaces and boundaries

openProfiler consumes provider discovery, local manifests, provider account
observations, and eventually authorized account/profile registry data. It emits
sanitized inventory, effective profile projections, credential-binding
references, and runtime activation or broker requests.

Keycloak identity references, wallet grants, and PKI evidence may authorize or
attest an operation, but they are not provider profile fields. The provider
persona catalog owns persona content; openProfiler stores only the binding and
the version/digest needed to reproduce what was selected.

The existing provider account-ID check remains load-bearing. Email is useful
display metadata but is not a safe account identity key.

## Alternatives and tensions

- **Full profile snapshots** are easy to display but duplicate account state,
  obscure ownership, and create noisy diffs when provider metadata changes.
- **A free-form JSON diff** is flexible but makes secrets, volatile state, and
  authority claims easy to smuggle into the wrong layer.
- **Email-based account matching** is convenient but fails for aliases,
  guests, changed addresses, and multiple organizations.
- **Provider-native profile identity only** preserves compatibility but leaves
  no stable cross-provider reference for persona or authority integration.

The smallest useful model is therefore a typed account reference, a typed
profile overlay, and an effective-profile digest.

## Open questions

- Which provider fields are stable enough to become part of the neutral account
  vocabulary, versus remaining provider-specific observations?
- Does one profile always belong to one account, or can a profile represent a
  deliberate multi-account routing set?
- Should the effective digest include persona content, or only the persona
  reference and version while the persona has its own digest?
- Which account/profile operations require a wallet grant, and which are safe
  as local read-only discovery?

## Relationships

- [Persona Reference and Composition](openprofiler-identity-persona-persona.md)
  defines the optional persona binding carried by a profile.
- [Identity, Trust, and Authority Integration](openprofiler-identity-persona-authority.md)
  defines the external identities and grants that may authorize profile
  operations.
- [Synthesis: Identity and Runtime](openprofiler-identity-persona-synthesis-runtime.md)
  joins the account/profile overlay to persona and authority flows.

