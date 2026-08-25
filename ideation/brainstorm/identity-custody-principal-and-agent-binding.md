# Principal and Agent Identity Binding — Brainstorm

Status: brainstorm
Kind: architecture
Summary: Human personas, organizations, service identities, and certified
agent identities should bind through explicit grants without treating login,
wallet possession, or model configuration as interchangeable authority.
Topics: identity-custody, identity-brokering, agent-certification, grants
Repository context: openxFactory neutral identity and autonomous-authority exploration
Captured: 2026-07-28

## Possible feats

- **Principal binding record** — connect a brokered human persona, tenant
  membership, service identity, agent identity, qualifications, and scoped
  grants with independent lifecycles.
- **Agent drift recertification trigger** — invalidate qualification when the
  measured agent identity changes beyond its certified tolerance.

## Focus

This document isolates identity linkage. Authentication proves control of a
login or credential; certification and grants determine what a human or agent
may do in one governed scope.

## Proposed model

The trust graph separates:

- one durable human persona linked to one or more external IdPs;
- tenant and organization memberships;
- service or application identities used by automation;
- a quantified agent identity bound to configuration and behavior evidence;
- qualification claims issued for a revision and test battery;
- explicit grants naming actions, subjects, expiry, and delegator.

No edge is inferred from email similarity, shared workstation, repository
access, or possession of a wallet file.

## Interfaces and boundaries

Identity brokering may establish the durable persona described in
[Keycloak Identity Brokering](keycloak-identity-brokering.md).
[Agent Certification Wallets](agent-certification-wallets.md) may carry
portable claims and grants. Runtime policy still validates issuer, scope,
revocation, current agent identity, and requested action.

## Alternatives and tensions

- Centralized identities simplify revocation but reduce portability.
- Portable credentials improve cross-factory use while issuer trust and
  correlation privacy become harder.
- Behavioral identity strengthens drift detection but can be expensive and
  probabilistic.

## Open questions

- Which claims may be self-presented versus resolved from an authority?
- How are agent identity tolerances calibrated by action risk?
- Can a human delegate through an agent without exposing unrelated tenant
  memberships?

## Relationships

Secret and record material used by these identities is bounded by
[Secret and Record Custody](identity-custody-secret-and-record-boundaries.md).
