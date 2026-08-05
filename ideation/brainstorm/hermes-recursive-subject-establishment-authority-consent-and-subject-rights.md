# Authority, Consent, and Subject Rights — Brainstorm

Status: brainstorm
Kind: architecture
Summary: Recursive establishment must bind every discovery, acquisition, processing, recall, inference, retention, and promotion step to purpose-specific authority while preserving correction, contest, revocation, and transparency rights.
Topics: hermes-recursive-subject-establishment, authority-consent-subject-rights, consent, subject-hermes, privacy
Repository context: openxFactory neutral governance with stricter person-subject and regulated-domain profiles
Captured: 2026-07-30

## Possible feats

- **Subject-establishment mandate** — declare authorized purposes, facets,
  sources, traversal limits, recipients, retention, budget, reviewers, and
  prohibited processing before recursion begins.
- **Subject-visible establishment ledger** — project what was sought, received,
  inferred, denied, corrected, and recalled into an understandable audit view.

## Focus

Recursive discovery creates a distinctive governance risk: the system may find
information that is accessible but outside the authorized purpose, or discover
a source whose retrieval requires a different grant. Scope discovery must
never silently become permission expansion.

## Proposed model

The episode begins with a mandate containing:

- subject reference and identity anchors;
- explicit establishment purpose and authorized model facets;
- allowed and prohibited source and record classes;
- consent, delegation, legal, contractual, or professional authority refs;
- permitted custodians, recipients, jurisdictions, and locations;
- relationship traversal and sensitive-category constraints;
- model-provider disclosure and retention posture;
- acquisition, recursion, spend, time, and subject-burden limits;
- required human or professional review;
- correction, contest, revocation, erasure, and exit handling.

Authority is evaluated separately at each boundary:

```text
discover metadata
  != retrieve content
  != disclose to a processor or model
  != retain a copy
  != infer a claim
  != admit a current-state item
  != promote learning beyond the subject
  != act on the result
```

For a person-subject, recall remains purpose-bound and minimized per query.
Public accessibility does not bypass the subject mandate, privacy policy, or
domain rules. Sensitive inferences may remain prohibited even when their
underlying sources are admissible.

Revocation stops future access and work, invalidates affected frontier items,
and triggers the declared cache, capsule, derived-data, and provider
disposition path. Corrections and contests preserve the original claim,
subject response, review, and resolution rather than silently rewriting
history.

## Interfaces and boundaries

Subject Hermes owns or references the consent and rights posture. Tenant and
Domain Hermes may narrow the allowed envelope but cannot expand beyond the
subject's valid authority or cross subject isolation.

An emergency or other exceptional path, if a domain permits one, must reuse
the existing break-glass contract and accountable review. The establishment
packet does not invent a generic bypass.

This document describes a system requirement surface, not legal advice. Each
DomainxFactory still owns jurisdictional, professional, contractual, and
records-policy specialization.

## Alternatives and tensions

- One broad onboarding authorization is easy to administer but undermines
  purpose limitation and meaningful subject choice.
- Per-source authorization provides control but can overwhelm the subject and
  stall establishment.
- Tiered standing envelopes plus exception review may offer a workable middle,
  provided denial and revocation remain live and observable.

## Open questions

- Is the mandate an extension of the consent profile, the subject-establishment
  fact set, or a distinct episode artifact?
- Which parts of the establishment ledger are safe and useful to expose to a
  company administrator, patient, caregiver, or delegate?
- How are derived inferences deleted or degraded when a supporting source is
  revoked?
- Can an episode retain proof that a prohibited source was encountered without
  retaining its content or sensitive metadata?

## Relationships

This governance constrains the [Hermes control boundary](hermes-recursive-subject-establishment-hermes-control-and-execution-boundary.md),
[source leads and acquisition obligations](hermes-recursive-subject-establishment-source-leads-and-acquisition-obligations.md),
and [subject-model admission](hermes-recursive-subject-establishment-subject-model-assembly-and-admission.md).
The existing detailed recall path is
[Subject Recall and Consent](subject-recall-and-consent-path.md).

