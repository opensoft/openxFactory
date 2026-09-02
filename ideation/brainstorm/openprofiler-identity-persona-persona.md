# OpenProfiler Persona Reference and Composition — Brainstorm

Status: brainstorm
Kind: architecture
Summary: Represent a model profile's persona as an optional versioned behavior reference, keeping it distinct from human authentication and from wallet authority.
Topics: openprofiler-identity-persona, persona, behavioral-identity, agent-identity, openxwallet-agent-profile, openprofiler
Repository context: openxFactory cross-factory architecture; persona content may be domain-owned while openProfiler carries the profile binding
Captured: 2026-08-24

## Possible feats

- **Versioned persona binding** — attach a stable persona reference and digest to a provider profile.
- **Composition-aware activation** — activate a model profile only when its persona, policy, and tool references resolve consistently.

## Focus

This document isolates what it means for a provider profile to “contain” a
persona. The word persona currently spans several existing concepts: a human
persona asserted by Keycloak, a presentation persona used by avatar clients,
and an agent identity derived from model composition. They must not collapse
into one identifier.

## Proposed model

Use a persona manifest or catalog record with a stable reference:

```yaml
persona_ref: research-analyst
persona_version: 3
role: research_assistant
disclosure_ref: disclosure.research-analyst
behavior_contract_ref: prompt-contract.research-analyst.v3
tool_manifest_ref: tools.research-readonly.v2
policy_ref: policy.research-safe.v4
persona_digest: sha256:...
```

A provider profile carries an optional binding:

```yaml
profile_ref: codex-work-001
persona:
  ref: research-analyst
  version: 3
  digest: sha256:...
```

The profile binding is a selection and provenance record. The persona catalog
or domain layer owns the actual behavior content. The runtime resolves the
references, verifies the digest, and records the selected persona version for
the session.

Three identity classes remain distinct:

- **Human persona** — the durable human subject asserted by Keycloak's
  identity-brokering layer.
- **Model persona** — the role, voice, behavioral constraints, disclosure, and
  policy selected for a model runtime.
- **Agent identity** — the composed identity of a model version, prompt
  contract, tools, policy, parameters, and governed retrieval references.

If the model persona is only presentation or behavior, the profile needs the
reference and digest. If it is also an authority-bearing agent identity, its
composition should participate in the openxWallet agent-profile composition
hash. A change then invalidates the relevant agent grants and requires
re-issuance.

## Interfaces and boundaries

The persona source owns authoring, catalog lifecycle, disclosure content, and
domain-specific policy. openProfiler owns selection, association with a
provider profile, resolution status, and the non-secret digest.

Keycloak must not be used as the persona catalog. Its human subject is an
authentication identity, not a model character. openXWallet must not be used
as the persona store; it may carry authority over an agent whose composition
includes the persona. OpenXPKI may attest or sign the manifest but does not
define its meaning.

Raw system prompts, private memory, provider credentials, and bearer tokens do
not belong in the profile inventory or wallet grant.

## Alternatives and tensions

- **Embed persona text in every profile** — simple locally, but duplicates
  content and makes version, approval, and revocation ambiguous.
- **Use the Keycloak human persona as the model persona** — gives one name but
  conflates who is authenticated with how a model behaves.
- **Require wallet composition for every persona** — provides strong identity
  but overburdens low-risk local display profiles that need no autonomous
  authority.
- **Use only free-form system prompts** — flexible but difficult to compare,
  digest, certify, or safely reuse across providers.

The recommended direction is a reference-plus-digest by default, with wallet
composition only when the persona is also an authority-bearing agent identity.

## Open questions

- Is a persona reusable across providers, or must each provider profile bind a
  provider-specific realization?
- Which persona fields are tenant-controlled, domain-controlled, or user-
  tunable?
- Is a behavioral battery required before a persona-bearing profile can receive
  autonomous authority?
- Does changing a persona always revoke a profile's grants, or only grants
  whose scope includes agent execution?

## Relationships

- [OpenProfiler Account and Profile Overlay](openprofiler-identity-persona-account-profile.md)
  defines the profile that carries this optional binding.
- [Identity, Trust, and Authority Integration](openprofiler-identity-persona-authority.md)
  separates persona content from authentication, grants, and attestations.
- Existing [Hermes persona character model](hermes-persona-character-model.md)
  explores authored character and the guardrail that character shapes how, not
  whether, an authority decides.
- Existing [openxWallet agent certification](agent-certification-wallets.md)
  explores composition hashes, certification, and drift-triggered revocation.

