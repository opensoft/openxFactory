# Claim Lineage and Reconciliation — Brainstorm

Status: brainstorm
Kind: architecture
Summary: Recursive establishment should preserve atomic claims, source lineage, operational versus epistemic status, conflicts, and supersession instead of treating repeated or recent statements as automatically corroborated truth.
Topics: hermes-recursive-subject-establishment, claim-lineage, evidence-reconciliation, source-claim, provenance
Repository context: openxFactory neutral evidence graph with accounting and clinical reliability specialization
Captured: 2026-07-30

## Possible feats

- **Lineage-aware source claim** — record exact source anchor, issuer, parties,
  effective period, extraction path, purpose fit, and upstream copied source.
- **Recursive reconciliation pass** — cluster competing claims, identify
  lineage dependence, and propose support, conflict, supersession, or review
  edges without deleting disagreement.

## Focus

Large estates create false confidence easily. Ten notes may repeat one
unverified diagnosis. Several forms may copy one old business address. An
invoice, email, and ledger entry may all derive from the same disputed vendor
term. Agreement among dependent sources is not independent corroboration.

## Proposed model

Every claim should be small enough to verify, conflict-check, and supersede. It
records:

- source and exact location;
- subject, relationship, account, location, and period applicability;
- issuer, author, interested party, or recorder role;
- extraction or observation method;
- upstream lineage and suspected copy-forward;
- source lifecycle such as draft, executed, final, amended, or superseded;
- operational authority and epistemic reliability separately;
- confidence rationale, uncertainty, and review status;
- supporting, contradicting, or superseding claim refs.

Reconciliation asks:

1. Do the claims concern the same entity, account, specimen, encounter, or
   period?
2. Does each source have authority for this claim type?
3. Are apparently agreeing sources independent?
4. Is there a later amendment, correction, reread, or result?
5. Does behavior or cross-modality evidence contradict the stated record?
6. Is professional review required before an accepted interpretation exists?

The output is an evidence graph update and candidate resolution:

```text
accepted_for_purpose
qualified
contested
superseded
unresolved
requires_professional_review
```

The original claims remain addressable after resolution.

## Interfaces and boundaries

Source claim creation is not a memory write. Reconciliation proposes evidence
relations and purpose-specific interpretations for Subject Hermes admission.

Operational truth and epistemic reliability must remain distinct. A signed
chart result or executed agreement may be operationally authoritative while
still requiring identity, applicability, completeness, or professional
challenge before a high-risk decision depends on it.

No universal source-class ranking should claim that documents always outrank
self-report, that newer always means correct, or that AI extraction creates
source authority.

## Alternatives and tensions

- A single accepted-value table is easy for downstream workflows but hides
  disagreement and historical applicability.
- A full evidence graph preserves nuance but can make every downstream query
  expensive and difficult to explain.
- Purpose-bound current-state projections can offer a usable view while the
  evidence graph retains the full conflict surface.

## Open questions

- Which reconciliation operations can be deterministic?
- How is lineage dependence inferred and later corrected?
- Which unresolved conflicts block subject readiness versus one workflow only?
- How are professional interpretations calibrated against later outcomes?

## Relationships

Claims originate from the [evidence-estate manifest](hermes-recursive-subject-establishment-evidence-estate-manifest.md)
and [multimodal processing](hermes-recursive-subject-establishment-multimodal-processing-and-specialist-routing.md),
ground the [relationship graph](hermes-recursive-subject-establishment-relationship-graph-and-traversal-scope.md),
and feed [subject-model admission](hermes-recursive-subject-establishment-subject-model-assembly-and-admission.md).

