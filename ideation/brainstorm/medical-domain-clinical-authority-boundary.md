# Clinical Authority Boundary — Brainstorm

Status: brainstorm
Kind: architecture
Summary: A MedxFactory domain overlay should define clinical reasoning and
review authorities while reserving order signing, chart writing, consent,
and final care decisions for explicitly human or external systems.
Topics: medical-domain, clinical-authority, domain-hermes, external-enforcement
Repository context: openxFactory neutral boundary informed by MedxFactory
Captured: 2026-07-28

## Possible feats

- **Clinical authority map** — bind domain personas, worker classes,
  escalation targets, and never-assignable human acts.
- **Medical decision-boundary validator** — reject overlays that grant order,
  chart, consent, or truth-model write authority to an autonomous worker.

## Focus

This document isolates what a medical Domain Hermes persona may decide and
what must remain with clinicians, patients, care organizations, or regulated
systems.

## Proposed model

MedxFactory Domain Hermes may govern evidence curation, reasoning standards,
verification, safety review, draft documentation, and escalation. It may
direct bounded workers and assemble decision foundations.

The overlay must represent `order_sign`, `chart_write`, and
`truth_model_write` as external-enforcement acts. Patient consent and
care-organization data stewardship remain cross-layer authorities, not
domain personas.

## Interfaces and boundaries

The candidate roster in
[MedxFactory Domain Roster](medxfactory-domain-roster-draft.md) supplies
decider roles. Worker capabilities arrive through the
[Medical Harness Adaptation](medical-omnigent-harness-adaptation.md).
This brainstorm is not clinical guidance.

## Alternatives and tensions

- More detailed domain personas improve routing but can imply clinical
  authority they do not possess.
- A strict never-assignable list is auditable but needs jurisdiction and
  workflow-specific extension.
- Draft documentation helps clinicians while creating automation-bias risk.

## Open questions

- Which review conclusions may Domain Hermes issue without clinician sign-off?
- How are jurisdictional and care-organization constraints layered?
- What display language prevents a decision foundation from appearing final?

## Relationships

The [Specialized Worker Envelope](medical-domain-specialized-worker-envelope.md)
binds worker execution beneath this authority.
