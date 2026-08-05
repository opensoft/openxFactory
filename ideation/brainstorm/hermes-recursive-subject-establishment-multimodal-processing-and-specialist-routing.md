# Multimodal Processing and Specialist Routing — Brainstorm

Status: brainstorm
Kind: architecture
Summary: Hermes RLM should orchestrate modality-specific deterministic tools, bounded models, and accountable specialists while preserving raw evidence, representations, and interpretations as separate linked artifacts.
Topics: hermes-recursive-subject-establishment, multimodal-processing, specialist-routing, document-intake, medical-imaging
Repository context: openxFactory neutral evidence processing with Ledgerx and Medx specialization
Captured: 2026-07-30

## Possible feats

- **Modality-processing record** — link a source representation to the exact
  parser, OCR, vision, table, thread, code, or specialist result that processed
  it.
- **Specialist routing profile** — select domain tools and reviewers by record
  class, sensitivity, materiality, failure mode, and decision dependency.

## Focus

Massive subject estates are heterogeneous. Email threads, spreadsheets,
contracts, ledger exports, scanned charts, FHIR resources, radiology studies,
pathology slides, audio, and portal exports fail in different ways. "Put it in
a vector store" is not an evidence-processing architecture.

## Proposed model

```text
admitted source
  -> classify modality and record class
  -> select approved processing profile
  -> create derived representations
  -> run deterministic checks and bounded extraction
  -> route material ambiguity to a specialist
  -> emit source-anchored claims and processing evidence
```

Example profiles:

| Source | Processing concerns | Candidate routing |
| --- | --- | --- |
| Contract PDF | layout, tables, signatures, amendments, effective dates | OCR/layout tools, agreement-set assembler, legal/accounting review |
| Mailbox thread | participants, threading, quoted text, attachments, chronology | mail parser, entity matcher, correspondence analyst |
| Ledger export | schema, account/vendor normalization, period and currency | deterministic accounting transforms, accountant review |
| Scanned chart | OCR quality, page order, patient identity, copy-forward | document tools, clinical data-quality review |
| FHIR/CCD | profiles, codes, versions, provenance, missing classes | health-data adapter, terminology mapping |
| DICOM study | study/series identity, metadata, pixels, report linkage | DICOM tooling, imaging model, radiologist review |
| Whole-slide pathology | extreme scale, staining, specimen identity | pathology pipeline and pathologist review |

RLM supplies adaptive decomposition and synthesis. It should not impersonate a
licensed reviewer or use a generic language-model interpretation where a
domain-specific tool, deterministic parser, or specialist is required.

Raw sources, derived renditions, machine observations, professional
interpretations, and Hermes synthesis remain separate nodes. Later correction
of an OCR result, report, or specialist interpretation can then propagate
without rewriting the source.

## Interfaces and boundaries

The evidence-estate manifest supplies stable source and representation
identity. The processing record supplies tool/model version, inputs, outputs,
quality metrics, provider disclosure, cost, and failure disposition.

Unsafe, encrypted, malformed, oversized, active-content, out-of-purpose, or
identity-ambiguous sources enter quarantine or authorized exception review
before normal processing.

Medical image reasoning cannot directly create a diagnosis, chart correction,
order, or patient-facing conclusion. Accounting or contract extraction cannot
directly update a ledger, vendor card, or legal position.

## Alternatives and tensions

- One general multimodal model reduces pipeline complexity but weakens
  reproducibility, domain controls, and modality-specific quality evidence.
- Dedicated pipelines improve assurance but create integration cost and may
  miss cross-modal relationships.
- RLM orchestration can join specialized results, but routing mistakes become
  a new source of error that must itself be visible.

## Open questions

- Which modality classifications and quality signals belong in the neutral
  kernel?
- When can a low-quality rendition support discovery but not claims?
- How are very large images sampled without creating false coverage claims?
- Which specialist review results are reusable across purposes?

## Relationships

Processing consumes the [evidence-estate manifest](hermes-recursive-subject-establishment-evidence-estate-manifest.md),
emits evidence for [claim lineage and reconciliation](hermes-recursive-subject-establishment-claim-lineage-and-reconciliation.md),
and is specialized by the [Ledgerx](hermes-recursive-subject-establishment-ledgerx-company-intake-profile.md)
and [Medx](hermes-recursive-subject-establishment-medx-patient-intake-profile.md)
profiles.

