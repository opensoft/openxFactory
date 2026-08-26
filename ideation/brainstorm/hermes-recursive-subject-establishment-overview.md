# Hermes Recursive Subject Establishment Overview — Brainstorm

Status: brainstorm
Kind: reference
Summary: Subject Hermes can use bounded recursive inference to discover, acquire, digest, reconcile, and maintain a massive heterogeneous subject evidence estate while preserving durable gaps, non-authoritative models, domain review, and strict action boundaries.
Topics: hermes-recursive-subject-establishment, subject-establishment, subject-hermes, rlm, evidence-estate, ledgerx, medx
Repository context: openxFactory neutral architecture with LedgerxFactory company-intake and MedxFactory patient-intake proof profiles
Captured: 2026-07-30

## Possible feats

- **Hermes recursive subject-establishment controller** — make adaptive
  evidence discovery and model assembly a capability of each scoped Subject
  Hermes rather than a global research agent.
- **Durable subject-establishment episode** — coordinate bounded inference,
  external waits, consent changes, acquisition, review, and readiness over days
  or weeks.
- **Subject evidence-estate and acquisition contracts** — preserve sources,
  representations, leads, obligations, attempts, processing, gaps, and
  coverage across heterogeneous providers.
- **Purpose-bound derived subject model** — assemble useful company, patient,
  project, or managed-estate views without turning inference into authoritative
  truth or action.
- **Ledgerx and Medx adoption profiles** — prove the same neutral closure loop
  against materially different accounting and clinical evidence estates.

## Motivation

xFactory subjects can arrive with far more evidence than one model context can
hold or one intake form can capture.

A Ledgerx client company may bring years of ledgers, bank and card data,
corporate records, contracts, invoices, statements, correspondence, and
relationships with many vendors and customers. Understanding a counterparty
may require assembling an effective agreement set across master terms,
amendments, schedules, emails, invoices, and observed payment behavior, then
checking selected public sources.

A Medx patient may have a fragmented longitudinal history across clinicians,
clinics, hospitals, insurers, pharmacies, laboratories, imaging centers,
pathology labs, portals, scanned charts, radiology studies, and the patient's
own memory. Finding the record custodians is itself part of understanding the
patient.

This is not merely online research, document ingestion, or retrieval over an
already complete corpus. The subject model tells Hermes what evidence is
missing; newly acquired evidence changes the model and reveals the next
sources, relationships, contradictions, and questions.

Recursive Language Models provide a useful context-computation pattern:
externalize the large estate, let a root model inspect and partition it
programmatically, call bounded models over selected slices, and synthesize.
xFactory must add durable episode state, governed acquisition, modality
routing, source authority, subject isolation, coverage, and admission.

## Goals

- Establish a provenance-rich, purpose-qualified understanding of a new
  subject across evidence estates larger than one reliable context.
- Discover missing sources, custodians, time periods, relationships, and
  contradictory evidence adaptively.
- Keep long-running establishment resumable without keeping a model or
  credential live across external waits.
- Preserve raw sources, representations, claims, interpretations, and current
  state as distinct linked objects.
- Measure discovery, acquisition, processing, reconciliation, review, and
  freshness coverage separately.
- Allow useful workflows to proceed with explicit gaps when their own evidence
  threshold is satisfied.
- Reuse existing Hermes, memory-gateway, Omnigent, derived-model, job, consent,
  credential, trace, and review boundaries.

## Non-goals

- No single authoritative, all-purpose dossier of a company or person.
- No claim that the open web, all unknown custodians, or every possible record
  has been exhausted.
- No unrestricted scraping, mailbox, filesystem, provider, EHR, imaging,
  ledger, or records access.
- No autonomous outreach merely because a model discovers a lead.
- No direct model write to a ledger, chart, vendor card, diagnosis, order,
  treatment, payment instruction, or other external truth store.
- No automatic cross-subject or cross-tenant correlation.
- No replacement of deterministic parsers, specialist tools, accountants,
  clinicians, legal review, radiologists, pathologists, or accountable subject
  authorities.
- No new Omnigent worker archetype or global "Research Hermes" with standing
  subject access.
- No silent promotion of this brainstorm into the staged
  subject-establishment capability or an OpenSpec contract.

## What the system delivers

If qualified and selected through governance, the system would provide:

- a purpose- and authority-bound subject-establishment mandate;
- a durable episode composed of finite, replayable Hermes RLM passes;
- a typed frontier of unresolved facets, relationships, periods,
  contradictions, missing artifacts, and review questions;
- a versioned evidence-estate manifest spanning documents, correspondence,
  transactions, structured records, media, and public sources;
- source leads and evidence-acquisition obligations with attempt history;
- modality-aware deterministic, model, and specialist processing;
- a subject-scoped relationship graph with identity quarantine and traversal
  limits;
- atomic source claims with lineage, conflict, supersession, authority, and
  epistemic-reliability evidence;
- immutable, non-authoritative, purpose-bound derived subject models;
- admission packets for evidence, timeline, current state, memory, and
  follow-up;
- coverage and readiness decisions that expose declared gaps and limitations;
- domain profiles defining required facets, sources, risks, reviewers, and
  forbidden actions.

## System model

```text
subject admission + establishment mandate
  purpose | identity | consent | source classes | traversal | budget | review
                                 |
                                 v
                   durable Subject Hermes episode
                                 |
                                 v
                    bounded Hermes RLM pass
                  inspect -> decompose -> select
                                 |
              +------------------+------------------+
              |                                     |
              v                                     v
     tool-less reference calls              governed work requests
                                            Omnigent / adapters /
                                            specialists / humans
              |                                     |
              +------------------+------------------+
                                 |
                                 v
                     evidence-estate manifest
          sources | representations | custody | access | processing
                                 |
                                 v
                   claims + relationship graph
             identity | lineage | conflict | effective time
                                 |
                                 v
                 governed derived subject model
                       non-authoritative
                                 |
                                 v
                    Subject Hermes admission
          evidence | timeline | current state | memory | follow-up
                                 |
                                 v
                     coverage + readiness
                                 |
          +----------------------+-----------------------+
          |                      |                       |
          v                      v                       v
        wait               proceed with gaps          establish
          |                                              |
          +-------------- new evidence/change -----------+
```

The governing feedback loop is:

```text
partial model
  -> identify the highest-value authorized gap
  -> discover or acquire evidence
  -> process and reconcile
  -> update the model and coverage
  -> repeat, wait, escalate, or stop
```

## Cluster map

- [Runtime and Authority](hermes-recursive-subject-establishment-synthesis-runtime-and-authority.md)
  — joins durable episodes, bounded Hermes reasoning, delegated execution, live
  authority, consent, and subject rights.
- [Discovery and Acquisition](hermes-recursive-subject-establishment-synthesis-discovery-and-acquisition.md)
  — connects the recursive frontier, evidence manifest, source leads,
  acquisition obligations, and the rule that discovery never widens
  permission.
- [Evidence and Subject-Model Assembly](hermes-recursive-subject-establishment-synthesis-evidence-and-model.md)
  — relates multimodal processing, entity resolution, lineage-aware
  reconciliation, non-authoritative projections, and Subject Hermes admission.
- [Closure and Domain Profiles](hermes-recursive-subject-establishment-synthesis-closure-and-domain-profiles.md)
  — applies honest readiness to Ledgerx company intake and Medx patient intake
  while preserving domain-specific facets and professional authority.

## How it fits

### Companion to governed recursive inference

The existing
[Governed Recursive Inference Overview](governed-recursive-inference-overview.md)
places task-local recursive computation inside a bounded Omnigent worker. This
packet adds a distinct root placement:

```text
Omnigent RLM
  recursively completes one bounded execution task

Hermes recursive establishment
  recursively maintains what xFactory knows and still needs to learn
  about one governed subject
```

Both can reuse typed context operations, immutable capsules, finite family
budgets, subordinate calls, trajectories, provider-disclosure evidence,
coverage ledgers, assurance packets, and routing against simpler baselines.

### Extension of subject establishment

The staged neutral
[Subject Establishment](../staging/subject-establishment/subject-establishment.md)
starts with a provenance-graded subject fact set and continues through neutral
design, platform realization, review, apply, and verification. This packet
deepens how a difficult fact set and subject model could be discovered and
assembled. It does not replace neutral design or external-system realization.

### Reuse of Subject Hermes and the memory gateway

The
[Subject Hermes Memory Model](../../docs/customer-hermes-memory-model.md)
already owns identity, consent, preferences, timeline, source claims, evidence
graph, current state, memory, active workflow context, follow-up, and promotion
candidates. The
[Memory Fill and Maintenance Taxonomy](../../docs/customer-memory-fill-maintenance-taxonomy.md)
already separates source material from gated memory writes.

Recursive establishment should emit candidates into those objects instead of
creating a parallel truth or memory store.

### Reuse of governed derived models

Any inferred subject model should use the
[Governed Derived Model](../../docs/governed-derived-model.md) invariants:
immutable non-authoritative status, full provenance, read-only truth-store
access, zero action authority, declared subject isolation, and reviewed
promotion into another object kind.

### Respect for subject-runtime isolation

One client company, patient, project, or other customer subject has its own
pseudonymous Subject Hermes runtime instance. A related counterparty or
provider graph remains scoped to that subject. Serving the same real-world
entity as another subject does not authorize memory merge or transitive
visibility.

### Domain proof profiles

Ledgerx contributes document-estate, corporate fact-source, counterparty,
agreement-set, transaction, correspondence, and professional-review cases.
Medx contributes fragmented record discovery, person-subject consent,
longitudinal evidence, claims-versus-clinical-content, DICOM-scale media,
operational-versus-epistemic truth, and clinician-authority cases.

## Leading design positions

These are the strongest current brainstorm positions:

1. The durable unit is a subject-establishment episode, not one RLM session.
2. The episode consists of bounded passes and event-driven resumes.
3. Hermes owns the recursive evidence frontier because the output changes
   subject understanding.
4. Omnigent, adapters, specialists, and external systems retain bounded
   execution roles.
5. The recursive frontier ranges over facets, relationships, time, sources,
   contradictions, and reviews—not files alone.
6. Evidence identity, byte custody, representations, claims, and memory remain
   distinct.
7. A discovered source creates a lead, not permission.
8. Acquisition is a governed action with identity, authority, attempt, and
   subject-burden evidence.
9. Relationship traversal is one hop by default and cannot create a general
   dossier of related parties.
10. Repeated dependent sources do not count as independent corroboration.
11. Derived subject models remain non-authoritative and purpose-bound.
12. Readiness is qualified by workflow and explicit gaps; "many documents"
    never proves completeness.
13. Establishment naturally becomes continuing refresh, reconciliation, and
    drift monitoring after the initial readiness decision.

## Key decisions and open questions

### Capability boundary

- Is the neutral name `hermes-recursive-subject-establishment`,
  `recursive-evidence-establishment`, or a subject-establishment extension
  that avoids naming one model technique?
- Which runtime and evidence contracts can be shared unchanged with the
  Omnigent-focused recursive-inference packet?
- Does maintenance reuse the establishment episode or begin a distinct
  long-lived episode family?

### Evidence and acquisition

- Is the evidence-estate manifest one neutral family or a coordinated view
  over domain catalogs?
- Is an evidence-acquisition obligation a specialized follow-up obligation or
  a sibling object?
- Which acquisition actions can operate under standing envelopes, and which
  always require contemporaneous subject or professional approval?

### Models and rights

- Which purpose projections must declare governed-derived-model conformance?
- How can a subject inspect, correct, or contest a model while respecting
  confidential third-party sources?
- What derived artifacts must be erased, tombstoned, or access-degraded after
  consent revocation or source withdrawal?

### Coverage and readiness

- Which coverage dimensions and readiness states are truly neutral?
- What constitutes reasonable closure for an unavailable custodian?
- Who may accept a material unresolved gap, and for which downstream workflow?

### Domain adoption

- Should Ledgerx prove the first low-action company-establishment profile before
  Medx enters a high-assurance qualification lane?
- Is a third profile such as codexFactory project adoption or Opsx managed
  estate needed before neutral proposal?
- Which stable recursive patterns should later crystallize into deterministic
  intake capabilities?

## Document map

### Synthesis documents

- [Runtime and Authority](hermes-recursive-subject-establishment-synthesis-runtime-and-authority.md)
- [Discovery and Acquisition](hermes-recursive-subject-establishment-synthesis-discovery-and-acquisition.md)
- [Evidence and Subject-Model Assembly](hermes-recursive-subject-establishment-synthesis-evidence-and-model.md)
- [Closure and Domain Profiles](hermes-recursive-subject-establishment-synthesis-closure-and-domain-profiles.md)

### Atomic documents: runtime and authority

- [Durable Subject-Establishment Episode](hermes-recursive-subject-establishment-durable-establishment-episode.md)
- [Hermes Control and Execution Boundary](hermes-recursive-subject-establishment-hermes-control-and-execution-boundary.md)
- [Authority, Consent, and Subject Rights](hermes-recursive-subject-establishment-authority-consent-and-subject-rights.md)

### Atomic documents: discovery and acquisition

- [Recursive Evidence Frontier](hermes-recursive-subject-establishment-recursive-evidence-frontier.md)
- [Subject Evidence-Estate Manifest](hermes-recursive-subject-establishment-evidence-estate-manifest.md)
- [Source Leads and Evidence-Acquisition Obligations](hermes-recursive-subject-establishment-source-leads-and-acquisition-obligations.md)

### Atomic documents: evidence and model assembly

- [Multimodal Processing and Specialist Routing](hermes-recursive-subject-establishment-multimodal-processing-and-specialist-routing.md)
- [Subject Relationship Graph and Traversal Scope](hermes-recursive-subject-establishment-relationship-graph-and-traversal-scope.md)
- [Claim Lineage and Reconciliation](hermes-recursive-subject-establishment-claim-lineage-and-reconciliation.md)
- [Subject-Model Assembly and Admission](hermes-recursive-subject-establishment-subject-model-assembly-and-admission.md)

### Atomic documents: closure and domain profiles

- [Coverage, Gaps, and Establishment Readiness](hermes-recursive-subject-establishment-coverage-gaps-and-readiness.md)
- [Ledgerx Company-Intake Profile](hermes-recursive-subject-establishment-ledgerx-company-intake-profile.md)
- [Medx Patient-Intake Profile](hermes-recursive-subject-establishment-medx-patient-intake-profile.md)

## Validation posture

This packet is non-normative brainstorm material. Contradiction is legal,
alternatives remain reversible, and no source access, records request, subject
model, memory write, domain action, or contract promotion follows without a
separate governed decision and execution path.

