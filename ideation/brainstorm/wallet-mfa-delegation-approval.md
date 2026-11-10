# Delegation and Separate Human Approval — Brainstorm

Status: brainstorm
Kind: architecture
Summary: Bind a distinct human approval to an agent's exact delegated operation and recheck authority at execution.
Topics: wallet-mfa, delegation, approval-policy, segregation-of-duties, agent-composition
Repository context: opensoft/openxFactory with cross-product integration references
Captured: 2026-11-10

## Possible feats

- Define a single-use approval bound to one immutable operation.
- Qualify invalidation after request, grant, approver, or composition change.

## Actors and authority

An agent has its own subject, wallet, composition, and narrow delegated grant. A delegating subject remains identifiable. Child grants monotonically narrow parent scope and lifetime. The agent signs as itself when exercising authority.

The domain decides when approval is required. Authentication establishes the human and verified assurance. Approval separately records that human's consent to an exact operation.

## Approval binding

Sign a canonical request digest covering tenant, application, agent actor/key and composition, delegating subject, applicable grant, operation, target, expected version, parameters digest, and expiry. Code operations include repository, branch, and full commit SHA where relevant. Sensitive content uses a private reference and digest.

Compare agent and approver at the domain-subject layer. Another key for the same subject cannot satisfy a distinct-holder constraint. Check current approver standing and eligibility.

## Execution and recovery

Recheck all current grants, composition, signer state, policy, approver standing, target version, digest, and expiry immediately before execution. Atomically consume approval with an idempotency record. A remote effect needs a durable intent/outcome or outbox/reconciliation protocol so a crash cannot cause a second effect.

A changed request requires new approval. Denial and expiry refuse the effect. Revocation between approval and execution invalidates the pending use. Approval remains constrained by the grant.

## First pilot

Use a synthetic disposable QA resource. Agent authentication allows a read and pending request. A separate human approval permits exactly one effect. Production merges and deployments require future domain-governed implementation.

## Relationships

[Shared records](wallet-mfa-shared-contracts.md) and [assurance](wallet-mfa-independent-assurance.md) feed the [authentication synthesis](wallet-mfa-synthesis-authentication.md).
