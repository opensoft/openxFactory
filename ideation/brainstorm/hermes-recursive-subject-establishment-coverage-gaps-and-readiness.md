# Coverage, Gaps, and Establishment Readiness — Brainstorm

Status: brainstorm
Kind: architecture
Summary: Subject readiness should be based on declared facet, source, time, processing, reconciliation, and review coverage with explicit gaps rather than document counts or an unsupported claim of complete intake.
Topics: hermes-recursive-subject-establishment, coverage-gaps-readiness, subject-establishment, evidence-coverage, assurance
Repository context: openxFactory neutral readiness and assurance across open and bounded evidence estates
Captured: 2026-07-30

## Possible feats

- **Subject-establishment coverage ledger** — measure discovery, acquisition,
  processing, reconciliation, review, and freshness separately by required
  facet.
- **Readiness-with-gaps decision** — permit bounded workflows to proceed while
  naming blockers, exclusions, stale evidence, and unresolved obligations.

## Focus

Large intake systems often confuse volume with completeness. Thousands of
documents do not prove that the effective vendor amendment, missing fiscal
period, prior pathology, or comparison CT was found. The open web and unknown
record custodians have no finite denominator.

## Proposed model

Coverage has several dimensions:

| Dimension | Question |
| --- | --- |
| Facet | Which required subject questions are answered? |
| Source universe | Which expected custodians and source families were discovered? |
| Acquisition | Which known sources were requested and received? |
| Temporal | Which fiscal, contractual, encounter, or care periods are represented? |
| Processing | Which received bytes were admitted and successfully processed? |
| Claim | Which extracted claims retain exact provenance? |
| Reconciliation | Which material conflicts and duplicates were resolved? |
| Review | Which required client, accountant, clinician, legal, or specialist reviews occurred? |
| Freshness | Which accepted claims or projections remain current for purpose? |

Per-source states should distinguish:

```text
not_discovered
discovered_metadata_only
authorization_pending
requested
partially_received
received_unprocessed
processed_with_limitations
reconciled
reviewed
unavailable
prohibited
stale
```

Open-world discovery can report query portfolios, registries or networks
checked, source classes, languages, time windows, relationship depth,
inaccessible sources, and marginal discovery yield. It cannot prove that the
internet or all unknown custodians were exhausted.

Suggested readiness outcomes:

```text
not_ready
ready_for_limited_workflows
provisionally_established
established_with_declared_gaps
established
degraded_after_change
```

Readiness is purpose-specific. Missing payroll records may not block vendor
setup; missing prior pathology may block a high-risk clinical conclusion while
not blocking appointment coordination.

## Interfaces and boundaries

The coverage ledger consumes the evidence manifest, frontier, acquisition
attempts, processing records, claim graph, reviews, and freshness rules. It
does not assign source authority or approve a consequential action.

The readiness decision is an assurance artifact for Subject Hermes and
accountable reviewers. Each downstream workflow still applies its own
minimum-evidence and professional-authority checks.

## Alternatives and tensions

- A hard "complete/incomplete" intake gate is easy to explain but makes real
  subjects permanently incomplete or encourages false closure.
- Purely workflow-specific readiness can allow useful progress but fragment
  the overall establishment picture.
- One subject-level coverage ledger with workflow-specific readiness views
  preserves both.

## Open questions

- Which neutral coverage metrics are meaningful across all subject types?
- How is marginal discovery yield measured without rewarding shallow queries?
- Who may accept an unresolved material gap?
- When does an unavailable source become a stable limitation rather than an
  endlessly retried obligation?

## Relationships

Readiness closes the [durable establishment episode](hermes-recursive-subject-establishment-durable-establishment-episode.md),
measures the [recursive evidence frontier](hermes-recursive-subject-establishment-recursive-evidence-frontier.md),
and evaluates [subject-model assembly](hermes-recursive-subject-establishment-subject-model-assembly-and-admission.md).
The domain coverage shapes appear in the Ledgerx and Medx profiles, both
MOVED 2026-09-07 to their own repositories at the same
`ideation/brainstorm/` filenames — Ledgerx to `ledgerXfactory/LedgerxFactory@6921aea3`,
Medx to `MedxSoft/MedxFactory@74bed502` (see `../README.md`,
"Moved to a DomainxFactory (2026-09-07)").

