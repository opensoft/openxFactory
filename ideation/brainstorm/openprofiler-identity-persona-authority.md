# OpenProfiler Identity, Trust, and Authority Integration — Brainstorm

Status: brainstorm
Kind: architecture
Summary: Use Keycloak for human identity, openXWallet for scoped authority, and OpenXPKI for device or workload trust while openProfiler remains responsible for provider account and credential operations.
Topics: openprofiler-identity-persona, identity-brokering, keycloak, openxwallet, trust-anchor, openxpki, credential-contracts, openprofiler
Repository context: openxFactory cross-factory architecture spanning Keycloak, OpenXPKI, openXWallet, credential contracts, and openProfiler
Captured: 2026-08-24

## Possible feats

- **Profile-operation authorization** — require scoped wallet grants for enrollment, activation, publication, and revocation.
- **Signed profile/persona manifest** — use OpenXPKI-backed trust to attest the device, workload, or manifest issuer.
- **Keycloak-backed openProfiler login** — authenticate one human persona while preserving provider and organization boundaries.

## Focus

This document isolates the integration seams. The systems are related because
they participate in one profile lifecycle, but they answer different security
questions and should not become a single identity or credential store.

## Proposed model

| System | Owns | Explicitly does not own |
| --- | --- | --- |
| Keycloak | Human subject, upstream identity linking, organization membership | Model persona behavior, provider tokens, wallet grants |
| openXWallet | Scoped, expiring, revocable authority grants and holder attribution | Raw provider credentials, human authentication, persona content |
| OpenXPKI | Trust anchors, workload/device certificates, signing and attestation evidence | Human login, provider account ownership, authorization policy |
| openProfiler | Provider accounts, profiles, credential bindings, activation, broker lifecycle | The family identity directory, PKI policy, general authority vocabulary |
| credential-contracts / vault | Credential references, custody declarations, and secret storage | Model persona semantics and human organization membership |

The intended operation flow is:

```text
human -> Keycloak subject and organization
      -> wallet grant for a named profile operation
      -> PKI-authenticated device/workload and optional signed manifest
      -> openProfiler account/profile resolution
      -> short-lived provider capability or controlled credential checkout
      -> provider runtime
```

Keycloak's organization membership is context for authorization; it is not by
itself permission to activate a provider profile. The authorization decision
comes from the governed layer and, where required, an openXWallet grant.

OpenXPKI is most useful at the service boundary: authenticating an openProfiler
client or broker, signing a profile/persona manifest, and proving which trust
anchor issued the certificate. The private provider credential remains under
the credential-custody boundary.

## Interfaces and boundaries

The native openProfiler client should use OIDC Authorization Code with PKCE
against the selected Keycloak environment. Keycloak may federate Entra,
Google, GitHub, or another upstream, but openProfiler should consume the
Keycloak subject rather than independently interpreting every upstream claim.

The operation request should carry references, not secrets:

```text
keycloak_subject_ref
organization_ref
profile_ref
account_ref
persona_ref / persona_version
wallet_grant_ref
client_certificate_ref
audit_ref
```

The profile broker may issue a provider-native short-lived token or authorize a
controlled credential checkout. In either case, tokens remain backend-only,
short-lived, and absent from browser state, logs, and audit records.

## Alternatives and tensions

- **Use Keycloak groups as the complete authority system** — easy to start but
  turns authentication claims into long-lived, poorly scoped permissions.
- **Use OpenXPKI as the human identity system** — certificates prove control of
  a key or workload, not the human's organization membership or login intent.
- **Store provider credentials in openXWallet** — violates the wallet's role as
  authority carrier and mixes key custody with grants.
- **Let openProfiler directly trust every provider and upstream IdP** — reduces
  one hop initially but creates duplicate account linking, claim mapping, and
  revocation logic.

The main tension is that the current openProfiler cloud design sketches Entra
as the user-facing authority, while the xFactory identity-brokering direction
adopts Keycloak as the family broker. A future implementation should choose one
client-facing issuer per environment; Keycloak can retain Entra as an upstream
where that is required.

## Open questions

- Which profile operations require a wallet grant, and what is the minimum
  authority tier for each?
- Is a client certificate required for local-only activation, or only for a
  remote broker and company-owned profiles?
- Does OpenXPKI sign persona manifests, profile manifests, or only authenticate
  the service that resolves them?
- How are Keycloak organizations mapped to personal versus company provider
  authorities without copying the tenancy graph into Keycloak?
- What is the revocation path when a Keycloak subject, wallet grant, profile,
  persona, certificate, or provider credential is revoked first?

## Relationships

- [OpenProfiler Account and Profile Overlay](openprofiler-identity-persona-account-profile.md)
  defines the provider objects these authorities act upon.
- [OpenProfiler Persona Reference and Composition](openprofiler-identity-persona-persona.md)
  defines the model identity that must not be confused with the human subject.
- Existing [Keycloak identity brokering](keycloak-identity-brokering.md)
  defines one durable human persona per broker instance and organization
  membership without mirroring the tenancy graph.
- The neutral [openXWallet contracts](../../contracts/openxwallet/README.md)
  define grants, custody, and holder attribution.
- The neutral [trust-anchor contracts](../../contracts/trust-anchor/README.md)
  define certificate trust and its relationship to wallet custody.

