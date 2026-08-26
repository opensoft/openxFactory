# Customer Memory Fill And Maintenance Taxonomy

Status: draft
Kind: architecture
Repository context: openxFactory
Related docs:
[Subject Hermes Memory Model](customer-hermes-memory-model.md),
[xFactory Memory Gateway Architecture](customer-memory-gateway-architecture.md),
[Avatar-First UI Standard](avatar-first-ui-standard.md)
Purpose: classify the general ways Subject Hermes memory is filled and
maintained, and define what each DomainxFactory must specialize locally.

## 1. Core Boundary

Customer memory is built from customer interaction and from ingested
information about the customer subject. The customer UI is not Subject Hermes.

```text
Avatar-first UI or conventional UI
  captures interaction, media, controls, attachments, and transcript refs

Hermes interaction distiller
  turns raw interaction material into candidate source claims, timeline events,
  preferences, follow-ups, current-state changes, and memory items

xFactory Memory Gateway
  runs consent, source authority, privacy, retention, budget, provider route,
  migration, and audit rails before durable memory is written or changed

Subject Hermes
  owns the customer-subject memory model and current truth state
```

Raw transcripts, recordings, uploaded files, telemetry, external records, and
agent summaries are source material. They do not become durable Subject Hermes
memory until the domain's Hermes layer distills them and xFactory gates the
write or update.

## 2. General Versus Domain-Specific

openxFactory owns the general shape:

- canonical fill modes
- canonical maintenance modes
- required source refs, consent refs, authority levels, privacy classes, and
  audit refs
- the rule that Hermes distills and xFactory gates memory writes
- the rule that raw interaction/session artifacts are source material, not
  memory items
- the requirement that DomainxFactories map each mode to their own source
  families, review rules, evidence types, and customer-subject aliases

DomainxFactory repos own the domain mapping:

- domain name for the customer layer, such as Patient Hermes, Managed System
  Hermes, Project Hermes, or Campaign Hermes ("Tenant Hermes" is reserved for
  the tenant/operator layer and must not alias the customer layer)
- domain source families and adapters
- domain claim types, timeline event types, and evidence graph relations
- domain authority thresholds and reviewer roles
- domain retention, privacy, consent, and safety rules
- domain examples for each fill and maintenance mode

## 3. Canonical Fill Pipeline

```text
capture or ingest source material
  -> create source ref and ingestion metadata
  -> Hermes distills candidate claims, events, preferences, obligations, or state
  -> xFactory evaluates consent, purpose, authority, privacy, retention, and route
  -> Subject Hermes appends or updates canonical objects
  -> audit, usage, and provider mapping records are emitted
```

The common outputs are:

```text
identity profile
consent profile
preference profile
source claim
timeline event
evidence graph edge
current state snapshot
memory item
active workflow context
follow-up obligation
promotion candidate
```

## 4. Fill Mode Taxonomy

| Fill mode | General openxFactory part | DomainxFactory specialization | Typical canonical outputs |
| --- | --- | --- | --- |
| Direct customer interaction | UI session, transcript refs, media refs, interaction event envelope, speaker/actor refs, consent and disclosure refs. Hermes distills; xFactory gates. | Domain persona, allowed questions, safety policy, escalation rules, domain interaction event types. | source claim, timeline event, preference profile update, memory candidate, follow-up obligation |
| Structured customer input | Form/survey/settings/upload envelope, answer quality labels, validation status, consent basis. | Domain fields, answer schemas, required attestations, domain-specific validation. | identity profile, consent profile, preference profile, source claim, active workflow context |
| Customer-attached evidence | Attachment metadata, source ref, custody, hash/location refs, extraction method, privacy class. | Domain evidence types and extractors, such as lab PDF, screenshot, invoice, campaign asset, repo artifact. | source claim, evidence graph node, timeline event, current state candidate |
| External system ingestion | Approved source inventory, adapter route, source family, read scope, timestamp, object refs. | Domain systems and adapters, such as EHR, LIS, CRM, M365, GitHub, accounting ledger, ad platform. | source claim, timeline event, current state snapshot, memory candidate |
| Third-party or provider message | Sender/role identity, relationship to customer, authority level, message/source ref, reply obligations. | Domain trusted party categories, such as clinician, caregiver, vendor, accountant, agency, reviewer. | source claim, timeline event, follow-up obligation, active workflow context |
| Sensor, device, or telemetry feed | Time-series source ref, sampling window, device identity, reliability metadata, anomaly flags. | Domain device classes, such as wearable, endpoint, monitor, CI run, financial feed, campaign metric stream. | observation claim, timeline event, current state signal, follow-up obligation |
| Staff or operator note | Staff actor ref, role authority, note source ref, review status, conflict handling. | Domain staff roles and note types, such as nurse note, technician note, account manager note, bookkeeper note. | source claim, memory candidate, timeline event, follow-up obligation |
| Non-Hermes agent output | External agent identity, model/system provenance, prompt/output refs, authority downgrade, review requirement. | Domain policy for partner agents, customer-owned bots, vendor automations, and imported AI summaries. | low-authority source claim, hypothesis, review task, promotion candidate |
| Omnigent work output | xFactory job ref, worker refs, artifact refs, validation result, reviewer requirement. | Domain Omnigent artifacts, such as clinical hypothesis packet, runbook result, PR admission packet, reconciliation packet, campaign analysis. | evidence graph update, current state candidate, follow-up obligation, promotion candidate |
| Workflow outcome | Workflow state transition, outcome observation, enforcement/handoff refs, comparison to prediction or target. | Domain outcome measures, such as lab received, deployment complete, PR merged, close complete, campaign launched. | timeline event, outcome observation, current state refresh, memory item |
| Migration or backfill | Legacy source inventory, mapping table, migration batch, confidence labels, provenance, rollback/tombstone plan. | Domain legacy systems and cleanup policy, such as legacy EHR, CRM notes, ticket archive, prior ledger, ad history. | backfilled source claims, timeline events, memory candidates, provider mappings |

## 5. Maintenance Mode Taxonomy

| Maintenance mode | General openxFactory part | DomainxFactory specialization | Typical canonical changes |
| --- | --- | --- | --- |
| Refresh | Re-read authoritative or time-sensitive sources and regenerate purpose-bound current state snapshots. | Domain freshness windows and source priority. | new current state snapshot, stale marker, timeline update |
| Reconciliation | Compare conflicting claims and preserve unresolved ambiguity. | Domain conflict rules and reviewer roles. | evidence graph conflict edge, review task, supersession candidate |
| Supersession | Mark older memory replaced by newer source-backed information without silent deletion. | Domain source hierarchy and update policy. | superseded memory item, replacement memory item, audit ref |
| Correction | Apply customer, staff, provider, or system correction with traceable reason. | Domain correction workflows and approval thresholds. | amended claim, corrected timeline event, refreshed snapshot |
| Consent change | Apply revoked, narrowed, expanded, expired, or delegated consent. | Domain consent models, guardian/delegate rules, regulatory policy. | consent profile update, blocked uses, tombstone or degraded packet |
| Retention expiry | Archive, tombstone, de-identify, or delete according to retention policy. | Domain retention classes and legal hold rules. | tombstone, archive ref, de-identification record |
| Promotion review | Move approved customer-scoped learning to client or domain memory. | Domain de-identification, review council, reusable learning policy. | promotion candidate, approval/rejection, target memory write |
| De-identification | Transform customer-derived learning for broader use while preserving traceability. | Domain safe-harbor, masking, aggregation, and minimum cohort rules. | de-identified claim, promotion packet, audit refs |
| Drift monitoring | Detect stale state, missed follow-ups, changed external source state, or workflow regression. | Domain drift signals and monitoring cadence. | follow-up obligation, stale flag, workflow review task |
| Provider migration | Move memory between providers without changing Hermes calls. | Domain provider routes, migration windows, validation criteria. | provider mapping, migration manifest, dual-write/shadow-read audit |

## 6. Domain Mapping Requirement

Every DomainxFactory should include a local customer-memory source and
maintenance mapping that answers:

- What is the customer layer called in this domain?
- What source families can fill memory?
- Which source families may create high-authority claims?
- Which fill modes require human or Hermes review?
- Which maintenance modes are automatic, scheduled, or approval-gated?
- Which external providers or adapters are allowed?
- Which customer UI interactions are source material only?
- Which artifacts are never allowed to become memory items directly?

The local domain mapping should reference this taxonomy and keep the same mode
names so cross-domain tooling can validate coverage.
