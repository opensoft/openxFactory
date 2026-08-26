# Source Leads and Evidence-Acquisition Obligations — Brainstorm

Status: brainstorm
Kind: process
Summary: Evidence should be allowed to reveal new custodians and missing artifacts through typed source leads that become reviewable, trackable acquisition obligations rather than silent autonomous outreach.
Topics: hermes-recursive-subject-establishment, source-lead, evidence-acquisition-obligation, subject-establishment, follow-up
Repository context: openxFactory neutral discovery-to-acquisition handoff across subject domains
Captured: 2026-07-30

## Possible feats

- **Source-lead record** — capture a suspected custodian, source, relationship,
  and discovery anchor before access has been established.
- **Evidence-acquisition obligation** — track what is needed, why, from whom,
  under which authority, by when, and whether the gap blocks readiness.

## Focus

The most valuable intake clues often point outside the current corpus:

- an invoice references a master agreement;
- a contract references an amendment or portal schedule;
- a ledger line reveals an unknown counterparty;
- an oncology note references an outside pathology review;
- an imaging report compares against an unavailable earlier study;
- an insurer claim reveals a clinic the patient did not remember.

These clues should not disappear into prose or cause an agent to contact a
third party without authority.

## Proposed model

```yaml
evidence_obligation:
  subject_ref: <pseudonymous-subject>
  question: <fact-or-gap-to-resolve>
  source_class: <agreement | encounter | imaging-study | ...>
  suspected_custodian_ref: <entity-or-unresolved-lead>
  discovery_basis_refs: [<source-anchor>]
  purpose: <episode-purpose>
  materiality: <domain-defined>
  required_authority_refs: []
  acquisition_route_candidates: []
  status: discovered
  blocking_level: non_blocking
  attempts: []
```

Suggested states:

```text
discovered
  -> identity_pending
  -> authorization_pending
  -> ready_to_request
  -> requested
  -> partially_received | received | denied | unavailable | expired
  -> processed
  -> obligation_satisfied | remains_open
```

One received source may satisfy several obligations. One obligation may require
several sources to establish an effective agreement set or a clinically
meaningful longitudinal record.

The obligation should preserve negative evidence: no response, unavailable
archive, destroyed record, denied access, or source known only through
metadata.

## Interfaces and boundaries

RLM discovery may propose a lead or obligation. Entity resolution, consent,
provider binding, and applicable human approval determine whether it becomes
an executable request.

The obligation does not itself authorize:

- messaging a vendor, customer, clinic, insurer, or patient;
- accepting portal terms;
- retrieving protected or confidential data;
- representing that xFactory is the subject or an authorized professional.

Approved acquisition is handed to the normal job and external-action pathway.
The durable episode waits and resumes when evidence or a terminal disposition
arrives.

## Alternatives and tensions

- A general follow-up obligation could represent the need, but an
  evidence-acquisition obligation needs source class, custodian, authority,
  attempt, and coverage semantics.
- Automatic outreach reduces intake latency but can create privacy, legal,
  relationship, and misrepresentation risk.
- Client- or patient-led requests preserve agency but can omit inconvenient or
  forgotten sources.

## Open questions

- Is this a specialization of the existing Subject Hermes follow-up
  obligation or a sibling contract?
- Which acquisition attempts count as reasonable closure?
- How are fees, expected delay, and subject burden represented?
- Who resolves conflicting custodian identity before outreach?

## Relationships

Obligations are created by the [recursive evidence frontier](hermes-recursive-subject-establishment-recursive-evidence-frontier.md),
executed under [authority, consent, and subject rights](hermes-recursive-subject-establishment-authority-consent-and-subject-rights.md),
and reported through [coverage, gap, and readiness](hermes-recursive-subject-establishment-coverage-gaps-and-readiness.md).

