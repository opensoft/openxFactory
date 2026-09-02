# OpenProfiler Identity and Persona Integration Overview — Brainstorm

Status: brainstorm
Kind: reference
Summary: Extend openProfiler from local provider-profile switching toward a typed account/profile and persona model integrated with Keycloak identity, openXWallet authority, and OpenXPKI trust without collapsing their responsibilities.
Topics: openprofiler-identity-persona, openprofiler, provider-profile, profile-account-diff, persona, identity-brokering, keycloak, openxwallet, trust-anchor, credential-contracts
Repository context: openxFactory cross-factory architecture; openProfiler, Keycloak, OpenXPKI, openXWallet, and provider credential services remain separately owned
Captured: 2026-08-24

## Possible feats

- **Profile identity graph** — connect human subject, organization, provider account, profile overlay, persona version, wallet grant, and trust evidence through stable references.
- **Governed persona-bearing model runtime** — activate a reproducible model posture with fail-closed credential, authority, and persona checks.

## Motivation

openProfiler already manages local AI-provider profiles and switches which
provider identity is active. The next useful abstraction is the difference
between the provider account and the profile layered over it. Some profiles may
also select a persona: a stable model role, voice, behavior contract, or agent
composition.

That selection intersects with three existing family capabilities. Keycloak
identifies the human and organization context. openXWallet carries scoped
authority. OpenXPKI establishes trust in a device, workload, certificate, or
manifest issuer. Treating them as one undifferentiated “profile identity” would
make ownership, revocation, and audit ambiguous.

## Goals

- Represent provider account identity separately from profile-specific deltas.
- Allow a profile to reference a versioned persona without storing persona
  content in credential metadata.
- Keep human identity, model behavior, operational authority, and cryptographic
  trust distinct but linkable.
- Support auditable, reproducible model-runtime selection.
- Preserve local-first and low-latency behavior where the provider runtime calls
  the model directly.

## Non-goals

- Making Keycloak the model persona catalog.
- Storing provider secrets or tokens in openXWallet, Keycloak, or persona
  records.
- Making OpenXPKI an authorization or human-account system.
- Requiring a wallet for every local read-only profile.
- Putting openProfiler in the per-turn provider request path.
- Promoting this brainstorm into policy or implementation without a later
  OpenSpec decision.

## What the system delivers

The intended result is a selected-runtime posture composed from references:

```text
Keycloak human subject + organization context
        │
        ▼
wallet grant authorizing a profile operation
        │
        ▼
PKI-authenticated client or signed manifest
        │
        ▼
provider account + explicit profile overlay
        │
        ▼
optional persona reference/version/digest
        │
        ▼
openProfiler credential resolution and activation
        │
        ▼
short-lived provider capability and direct model call
```

The runtime can record the non-secret references and effective digest without
recording provider credentials. A persona change can be treated as a new
version; when the persona also defines an authority-bearing agent composition,
the corresponding wallet grants can be invalidated and re-issued.

## System model

| Layer | Primary question | Proposed owner |
| --- | --- | --- |
| Human identity | Who is the human and which organizations are associated? | Keycloak |
| Provider identity | Which provider account is this? | openProfiler / provider authority |
| Profile selection | What differs from the account defaults? | openProfiler |
| Model behavior | How should this model present and behave? | Persona catalog or domain profile |
| Operational authority | May this subject perform this profile operation? | openXWallet grant / governed layer |
| Cryptographic trust | Is this client, workload, or issuer trusted? | OpenXPKI / trust-anchor |
| Secret custody | Where is the provider credential held and resolved? | Credential broker / vault boundary |

## Cluster map

- [OpenProfiler Account and Profile Overlay](openprofiler-identity-persona-account-profile.md)
  — defines account identity, profile metadata, and deterministic differences.
- [OpenProfiler Persona Reference and Composition](openprofiler-identity-persona-persona.md)
  — defines the optional persona binding and its relationship to agent identity.
- [OpenProfiler Identity, Trust, and Authority Integration](openprofiler-identity-persona-authority.md)
  — separates Keycloak, openXWallet, OpenXPKI, and credential custody.
- [Synthesis: OpenProfiler Identity and Runtime](openprofiler-identity-persona-synthesis-runtime.md)
  — explains the end-to-end flow and cross-system lifecycle.

## How it fits

This packet extends the direction in the existing openProfiler cloud credential
vault design, which already distinguishes `profile_id`, `account_id`, company
authority, credential generations, leases, and account-ID verification. It also
extends the xFactory `add-model-provider-broker` proposal, which currently
treats openProfiler as an external, unbuilt broker and deliberately leaves its
storage and OAuth surface out of scope.

The packet reuses existing xFactory boundaries rather than creating parallel
ones:

- the identity-brokering capability defines Keycloak-style human subjects and
  organization membership;
- the openXWallet capability defines grants, custody, and holder attribution;
- the trust-anchor capability defines certificate trust and custody mapping;
- credential contracts remain the vocabulary for secret references and broker
  custody;
- openProfiler remains the provider-specific account/profile and activation
  realization.

## Key decisions and open questions

The load-bearing design direction is to keep three meanings of persona apart:
human persona, model persona, and agent identity. A default model persona is a
versioned reference plus digest. A persona that carries autonomous authority
may additionally enter the wallet agent-composition hash.

The main unresolved choices are the canonical manifest boundary, the exact
Keycloak-to-provider-authority mapping, wallet-grant requirements by operation,
PKI signing scope, and the revocation behavior for already-running sessions.

## Document map

1. [Account and Profile Overlay](openprofiler-identity-persona-account-profile.md)
2. [Persona Reference and Composition](openprofiler-identity-persona-persona.md)
3. [Identity, Trust, and Authority Integration](openprofiler-identity-persona-authority.md)
4. [Synthesis: Identity and Runtime](openprofiler-identity-persona-synthesis-runtime.md)

