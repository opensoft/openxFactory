# Identity and Custody Overview — Brainstorm

Status: brainstorm
Kind: reference
Summary: The identity and custody packet proposes one explainable trust plane
that links brokered humans, services, qualified agents, scoped grants, and
protected records without storing credentials in governed content.
Topics: identity-custody, identity-brokering, agent-certification, openxvault
Repository context: openxFactory cross-factory identity and custody contracts
Captured: 2026-07-28

## Possible feats

- **xFactory trust-plane kernel** — principal linking, agent qualification,
  scoped delegation, custody references, authorization decisions, and
  revocation evidence.

## Motivation

xFactory spans interactive users, applications, autonomous agents,
repositories, tenant data, and protected records. Treating login identity,
GitHub access, agent configuration, and data possession as the same authority
creates unreviewable delegation and leakage risk.

## Goals

- Link external logins to one durable human persona.
- Keep service and agent identities independently accountable.
- Bind qualifications and grants to explicit scopes and expiry.
- Store credentials and sensitive records in governed custody planes.
- Make every protected access explainable and revocable.

## Non-goals

- Keycloak, DID wallets, or a vault product alone do not define authority.
- Credentials never belong in layer content or repository manifests.
- Agent certification does not eliminate per-action policy.
- This packet does not select one identity or KMS vendor.

## What the system delivers

Operators can identify the actor and delegation behind an action, verify
current qualification and grants, resolve a protected object by reference,
apply custody policy, and audit the resulting access or denial.

## System model

```text
external IdPs → durable persona ─┐
service/agent identity + cert ───┼→ scoped grant + purpose
protected object reference ─────┘
  → authorization and custody policy
  → short-lived access or explained denial
  → audit, revocation, and recertification
```

## Cluster map

- [Identity and Custody Trust Plane](identity-custody-synthesis-trust-plane.md)
  — joins actor/delegation evidence to protected-object handling.

## How it fits

The dashboard uses brokered human identity. Worker enrollment binds service
and agent identities. Hermes retrieval adds subject consent. openxVault
protects records. Individual runtimes consume the neutral trust decision
without receiving raw upstream credentials.

## Key decisions and open questions

Open choices include authoritative identity linking, wallet issuer trust,
behavioral drift thresholds, offline verification, custody-tier placement,
and privacy-preserving correlation.

## Document map

### Synthesis

- [Identity and Custody Trust Plane](identity-custody-synthesis-trust-plane.md)

### Atomic explorations

- [Principal and Agent Identity Binding](identity-custody-principal-and-agent-binding.md)
- [Secret and Record Custody Boundaries](identity-custody-secret-and-record-boundaries.md)

### Related source leaves

- [Keycloak Identity Brokering](keycloak-identity-brokering.md)
- [Agent Certification Wallets](agent-certification-wallets.md)
- [openxVault](git-native-record-vault.md)
