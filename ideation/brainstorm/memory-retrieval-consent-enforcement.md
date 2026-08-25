# Memory Consent Enforcement at Recall — Brainstorm

Status: brainstorm
Kind: architecture
Summary: Every private-memory recall should re-evaluate subject, purpose,
requester, scope, expiry, revocation, and break-glass policy before evidence
enters a context packet.
Topics: memory-retrieval, consent, subject-hermes, private-memory
Repository context: openxFactory memory-gateway and subject-recall exploration
Captured: 2026-07-28

## Possible feats

- **Per-query recall authorization** — emit allow, minimize, deny, or
  dual-authorized break-glass dispositions with reason and audit evidence.
- **Subject-visible recall log** — expose who requested what category, for
  which purpose, what was disclosed, and which evidence was withheld.

## Focus

This document isolates consent and authorization at retrieval time. Stored
access or a previously valid consent record is not sufficient when purpose,
requester, subject state, or revocation may have changed.

## Proposed model

The gate evaluates:

- tenant, subject, requester, and delegated authority;
- requested evidence classes and minimum necessary scope;
- declared purpose and permitted use;
- consent grant, expiry, withdrawal, and jurisdictional constraints;
- source ACL and retention/deletion state;
- break-glass eligibility, two-person authorization, and notification.

The disposition accompanies the context packet and is recorded in a
subject-visible audit trail where appropriate.

## Interfaces and boundaries

The gate consumes subject consent and memory metadata. It controls admission
to the [Evidence-to-Context Boundary](memory-retrieval-evidence-context-boundary.md).
It does not decide clinical, legal, or project outcomes.

Related source:
[Subject Recall and Consent Path](subject-recall-and-consent-path.md).

## Alternatives and tensions

- Pre-authorized broad consent reduces latency but weakens purpose limitation.
- Detailed denial explanations improve trust yet may reveal sensitive source
  existence.
- Immediate revocation conflicts with replicated indexes and offline caches.

## Open questions

- Which denials may disclose the existence of withheld evidence?
- How is emergency access reconciled with later subject notification?
- What deletion guarantees apply to previously generated context packets?

## Relationships

The [governed recall synthesis](memory-retrieval-synthesis-governed-recall.md)
joins authorization to context construction.
