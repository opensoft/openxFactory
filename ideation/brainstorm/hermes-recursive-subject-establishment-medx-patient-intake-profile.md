# Medx Patient-Intake Profile — Brainstorm

Status: brainstorm
Kind: architecture
Summary: Medx can specialize Hermes recursive establishment to discover record custodians, acquire authorized longitudinal records, process structured and imaging modalities, and assemble a provenance-rich patient model that remains subject to clinical review.
Topics: hermes-recursive-subject-establishment, medx-patient-intake, medx, patient-hermes, medical-records
Repository context: openxFactory neutral packet with MedxFactory as the person-subject and high-assurance proof profile
Captured: 2026-07-30

## Possible feats

- **Recursive patient record-establishment profile** — build a longitudinal
  provider, encounter, source, and gap map from patient, provider, payer, and
  imaging evidence.
- **Patient-authorized record-acquisition coordinator** — turn provider and
  study leads into transparent, consented, trackable acquisition obligations.

## Focus

A new patient's available chart is rarely the complete patient history.
Relevant evidence can be fragmented across prior physicians, clinics,
hospitals, laboratories, pharmacies, insurers, imaging centers, pathology
labs, portals, paper records, and the patient's own recollection.

## Proposed model

Seed source families may include:

- patient and delegate interviews, forms, uploads, and consent records;
- current and outside EHR records, CCD/FHIR exports, notes, and discharge
  packets;
- payer claims, encounters, explanation-of-benefit records, and prior
  authorizations;
- pharmacy and medication history;
- laboratory, pathology, molecular, and genomic reports;
- DICOM imaging studies, radiology reports, and comparison-study references;
- referrals, provider messages, care-management records, and device data.

The first recursive pass can create a provider and encounter map:

```text
patient
  -> insurers and coverage periods
  -> primary care and specialists
  -> hospitals, urgent care, labs, pharmacies, imaging and pathology
  -> encounters, referrals, studies, specimens, and treatments
  -> suspected missing custodians and time intervals
```

Clues then create evidence obligations:

- a payer claim suggests an encounter whose clinical record is absent;
- a note names an earlier specialist or diagnosis source;
- an imaging report references a comparison study not received;
- a pathology result points to slides or an outside reread;
- a medication list suggests a prescriber or pharmacy history;
- a patient recollection supplies a lead that remains unverified.

Authorized acquisition may use patient or representative requests, provider
portals, payer APIs, health-information exchange, direct transfer, or upload.
In a United States profile, the [HHS access guidance](https://www.hhs.gov/hipaa/for-professionals/faq/2042/what-personal-health-information-do-individuals/index.html)
describes broad access to medical, billing, insurance, lab, X-ray, and related
records; [TEFCA](https://healthit.gov/policy/tefca/) includes individual access
services; and the [CMS Patient Access API](https://www.cms.gov/priorities/burden-reduction/overview/interoperability/frequently-asked-questions/patient-access-api)
can supply claims, encounters, and defined clinical data. CMS also notes that
large unstructured PDFs or fax scans may be absent, so no single channel
proves record completeness.

Imaging remains a distinct estate. [DICOMweb](https://www.dicomstandard.org/using/dicomweb/)
supports standard query, retrieval, and storage operations, while the episode
still needs study/series identity, report linkage, pixel access policy,
specialist interpretation, and coverage evidence.

## Interfaces and boundaries

The profile emits patient-reported and source-backed claims, provider and
encounter relationships, evidence gaps, reliability concerns, purpose-bound
current-state candidates, and clinical review tasks.

Claims, payer records, and notes are evidence with different failure modes.
Claims may reveal care activity without supplying clinical detail. Repeated
notes may copy one weak source. Imaging, pathology, labs, medication records,
and patient reports retain separate provenance and operational-versus-
epistemic status.

RLM and specialist models cannot independently create a diagnosis, chart
correction, order, treatment change, or patient-facing clinical conclusion.
Clinicians and authorized care teams retain clinical authority.

## Alternatives and tensions

- Payer-first discovery can reconstruct a broad utilization map but may miss
  self-pay, uncovered, old, or non-billed care.
- Patient-led recollection respects agency but can be incomplete and should
  not be treated as low-value merely because it is not provider-authored.
- Health-information networks and APIs improve reach but do not eliminate
  manual requests, identity matching, imaging exchange, or scanned records.

## Open questions

- Which longitudinal facets are required for provisional patient readiness?
- How are minors, guardians, caregivers, sensitive records, and segmented
  consent represented?
- Who owns follow-up when a provider does not respond or no longer exists?
- Which imaging or pathology gaps block clinical reasoning versus remain
  disclosed limitations?

## Relationships

This profile specializes [authority, consent, and subject rights](hermes-recursive-subject-establishment-authority-consent-and-subject-rights.md),
[multimodal processing](hermes-recursive-subject-establishment-multimodal-processing-and-specialist-routing.md),
[relationship traversal](hermes-recursive-subject-establishment-relationship-graph-and-traversal-scope.md),
[claim reconciliation](hermes-recursive-subject-establishment-claim-lineage-and-reconciliation.md),
and [coverage readiness](hermes-recursive-subject-establishment-coverage-gaps-and-readiness.md).
Domain evidence includes the
[Patient Memory Fill and Maintenance Mapping](../../../xFactories/MedxFactory/docs/patient-memory-fill-maintenance-mapping.md),
[Patient Truth and Simulation Model](../../../xFactories/MedxFactory/docs/patient-truth-and-simulation-model-system.md),
and [Foundational Data Reliability](../../../xFactories/MedxFactory/docs/foundational-data-reliability-and-reverification.md).

