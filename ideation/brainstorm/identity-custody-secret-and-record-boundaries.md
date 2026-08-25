# Secret and Record Custody Boundaries — Brainstorm

Status: brainstorm
Kind: architecture
Summary: Credentials, portable identity claims, governed records, sanitized
analysis artifacts, and commodity data should occupy distinct custody tiers
with references rather than copied secrets.
Topics: identity-custody, openxvault, credential-references, encryption-tiers
Repository context: openxFactory neutral custody and record-vault exploration
Captured: 2026-07-28

## Possible feats

- **Custody-tier reference contract** — identify a protected object, provider,
  tenant, purpose, policy class, and retrieval grant without embedding secret
  material.
- **Vault projection builder** — create sanitized, provenance-linked analysis
  artifacts while protected source records remain encrypted and audited.

## Focus

This document isolates where identity material and governed records live.
Convenient file access must not collapse authentication secrets, agent
credentials, PHI, sanitized analysis, and public artifacts into one Git plane.

## Proposed model

Three broad custody planes remain distinct:

- **Vault plane** — encrypted governed records and sensitive credentials under
  KMS-backed policy, audit, retention, and break-glass controls.
- **Sanitized analysis plane** — minimized derivatives with source pins and
  de-identification evidence.
- **Commodity plane** — non-sensitive bulk artifacts with ordinary repository
  or object-storage controls.

Configuration and layer content carry provider and object references only.
Runtime resolution checks identity, tenant, purpose, and current grant.

## Interfaces and boundaries

[openxVault](git-native-record-vault.md) supplies the record-vault
exploration. The
[Principal and Agent Binding](identity-custody-principal-and-agent-binding.md)
supplies the actor and grant being evaluated. This packet does not define a
new cryptographic primitive.

## Alternatives and tensions

- Git-native encrypted records aid provenance but repository replication
  expands ciphertext custody.
- Central vault services simplify policy while offline workflows become
  harder.
- De-identification increases reuse yet remains domain- and attack-dependent.

## Open questions

- Which object classes may be committed as encrypted blobs?
- How are erasure and legal hold represented in immutable history?
- What provenance is safe to retain in sanitized artifacts?

## Relationships

The [trust-plane synthesis](identity-custody-synthesis-trust-plane.md) joins
identity and custody during authorization.
