# Synthesis: Identity and Custody Trust Plane — Brainstorm

Status: brainstorm
Kind: architecture
Summary: Explicit principal and agent bindings combine with tiered custody so
every protected access can prove who acts, under which grant, on which object,
for which purpose, and with which audit trail.
Topics: identity-custody, identity-brokering, agent-certification, openxvault, synthesis
Repository context: openxFactory neutral trust-plane exploration
Captured: 2026-07-28

## Possible feats

- **Trust-plane authorization decision** — evaluate persona, service or agent
  identity, qualification, tenant, grant, object custody, purpose, and
  revocation in one explainable record.

## Members and their joints

Atomic members:
[Principal and Agent Identity Binding](identity-custody-principal-and-agent-binding.md)
and [Secret and Record Custody Boundaries](identity-custody-secret-and-record-boundaries.md).

### Identity names the accountable actor

Brokered persona links, service identities, agent fingerprints,
qualifications, and grants establish who is asking and what delegation chain
applies.

### Custody names the protected object and handling rules

The referenced object declares its tenant, sensitivity, provider, permitted
purposes, retention, and audit obligations. Possession of a reference does
not imply access.

### Authorization binds both at request time

The runtime evaluates the current actor, grant, object, purpose, and
revocation state. It returns a scoped lease or denial and records the
decision without leaking secret material.

## Emergent behavior

The same trust decision can govern dashboard users, autonomous workers,
memory retrieval, repository actions, and vault access while their credentials
and records stay in appropriate stores.

## Tensions to hold

- Unified policy improves consistency but risks centralizing sensitive
  correlation data.
- Short-lived leases improve revocation while increasing runtime dependency.
- Portable credentials need clear issuer and tenant trust boundaries.

## Recombination opportunities

Worker enrollment and execution can consume this trust plane through the
[worker-execution packet](worker-execution-overview.md).

## Open questions

- Which decisions must be online versus verifiable offline?
- How are delegation chains displayed to operators?
- Can qualification and access revocation use the same distribution channel?
