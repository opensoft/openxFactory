# Subject Evidence-Estate Manifest — Brainstorm

Status: brainstorm
Kind: architecture
Summary: Recursive establishment needs a versioned manifest of known subject evidence, representations, locators, custody, admissibility, processing state, and gaps without treating storage location as evidence identity.
Topics: hermes-recursive-subject-establishment, evidence-estate-manifest, provenance, document-estate, source-authority
Repository context: openxFactory neutral evidence identity spanning document, correspondence, transaction, clinical, media, and public-source estates
Captured: 2026-07-30

## Possible feats

- **Subject evidence-estate manifest** — inventory every known source and
  representation with stable identity, lineage, access posture, and processing
  state.
- **Working corpus capsule** — freeze the authorized subset selected for one
  bounded RLM pass with digests and exact disclosure evidence.

## Focus

A subject's evidence is not one folder or vector database. It may span email,
documents, ledgers, APIs, claims, images, external registries, and sources that
are known but not yet accessible. The system needs to distinguish evidence
identity from current storage and to distinguish discovery from acquisition,
parsing, and admission.

## Proposed model

Each manifest entry records:

- stable source and representation IDs;
- subject and relationship scope;
- source family and record class;
- original custodian, issuer, author, and parties when known;
- locator history and current accessible locators;
- content digest, version, effective period, and retrieval time;
- source-original, copy, rendition, extraction, or generated-summary relation;
- byte custody and records-preservation declaration;
- consent, purpose, privacy, sensitivity, and retention references;
- safety/admission disposition;
- processing state and available derived artifacts;
- authority, reliability, freshness, and review metadata;
- whether only discovery metadata is available.

Example representation chain:

```text
vendor email attachment
  -> source-original PDF
  -> DMS-preserved copy
  -> OCR/layout rendition
  -> atomic claim set

radiology study
  -> DICOM study and series
  -> radiology report
  -> approved thumbnails or derived measurements
  -> reviewed imaging claims
```

The manifest can state that a source exists even when the episode cannot
lawfully retrieve, retain, parse, or disclose it. That distinction is part of
the coverage evidence.

## Interfaces and boundaries

The manifest catalogs source material; it does not make the material a Subject
Hermes memory item or a trusted fact. Raw bytes remain in their approved
provider, object store, document system, imaging archive, or quarantine.

A working corpus capsule references an immutable authorized slice of the
manifest for one run. It does not grant standing provider access or imply that
every listed source was disclosed to a model.

This neutral idea can reuse Ledgerx's client-evidence identity and locator
thinking while expanding beyond documents. It should not repurpose the
governance-document catalog as a client-content evidence store.

## Alternatives and tensions

- One central evidence vault simplifies retrieval but creates custody,
  retention, migration, and breach concentration.
- Pure federation preserves source custody but makes reproducibility and
  availability difficult.
- A catalog-plus-referenced-bytes design supports both, but only if backing,
  fallback, and expiry are explicit.

## Open questions

- Is this one neutral manifest family or a coordination view over document,
  mail, ledger, clinical, and imaging catalogs?
- Which representations require independent stable identity?
- When may a lawful snapshot be retained for replay after source access is
  revoked?
- How is manifest completeness established for provider APIs that expose only
  partial record classes?

## Relationships

The manifest bounds the [recursive evidence frontier](hermes-recursive-subject-establishment-recursive-evidence-frontier.md),
feeds [multimodal processing](hermes-recursive-subject-establishment-multimodal-processing-and-specialist-routing.md),
and anchors [claim lineage and reconciliation](hermes-recursive-subject-establishment-claim-lineage-and-reconciliation.md).
Ledgerx evidence overlap is described in the
[Subject Document Estate Overview](../../../xFactories/LedgerxFactory/ideation/brainstorm/subject-document-estate-overview.md).

