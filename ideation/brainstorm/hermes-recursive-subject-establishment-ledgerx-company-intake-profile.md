# Ledgerx Company-Intake Profile — Brainstorm

Status: brainstorm
Kind: architecture
Summary: Ledgerx can specialize Hermes recursive establishment to reconstruct a client company's accounting, entity, counterparty, agreement, correspondence, and operational evidence estate without allowing extraction to mutate the ledger.
Topics: hermes-recursive-subject-establishment, ledgerx-company-intake, ledgerx, counterparty-model, document-estate
Repository context: openxFactory neutral packet with LedgerxFactory as a domain proof profile
Captured: 2026-07-30

## Possible feats

- **Recursive company evidence-establishment profile** — inventory and
  reconcile books, records, agreements, communications, and public evidence
  into a company-scoped model.
- **Counterparty agreement-set assembler** — discover and relate master
  agreements, amendments, schedules, invoices, statements, correspondence, and
  observed payment behavior.

## Focus

A new Ledgerx subject company cannot be understood from a setup wizard or
general ledger alone. The accounting structure is embedded across transaction
systems, files, mail, company records, vendor and customer relationships, and
the difference between documented and actual operating practice.

## Proposed model

Seed source families may include:

- formation, ownership, licensing, tax, premises, and banking records;
- chart of accounts, general ledger, AP/AR, inventory, payroll, fixed-asset,
  bank, and card exports when authorized;
- invoices, purchase orders, receipts, statements, credits, and remittances;
- vendor and customer master data;
- contracts, amendments, schedules, leases, portal terms, and policies;
- correspondence, attachments, meeting notes, disputes, and confirmations;
- public registries, official filings, websites, and purpose-approved research.

The recursive company graph can cover:

```text
subject company
  -> legal entities, owners, locations, registrations
  -> systems, accounts, books, policies, and fiscal periods
  -> banks, cards, processors, and payment paths
  -> vendors and customers
       -> legal and operational identities
       -> account and location relationships
       -> effective agreement sets
       -> invoices, credits, disputes, and correspondence
       -> contractual terms versus observed behavior
  -> missing periods, records, confirmations, and reviews
```

RLM is useful because each source changes the search:

- an invoice reveals an unregistered vendor account;
- a ledger payment reveals a counterparty absent from the DMS;
- a contract reveals amendments and volume schedules;
- email reveals a disputed or temporary term;
- transaction history challenges the apparent policy;
- a public registry helps resolve legal identity but does not establish
  accounting treatment.

Outputs remain candidates: source claims, relationship edges, effective-period
term candidates, accounting-state projections, evidence obligations, and
review packets.

## Interfaces and boundaries

The profile reuses Ledgerx's subject document estate rather than inventing a
second document binding. It expands the recursive controller across document,
mail, transaction, system, and public-source estates.

No extraction or inferred term directly changes Business Central, another
ledger, a vendor card, payment instruction, tax treatment, or legal position.
Accountants, client authorities, and other required professionals review
material interpretations before realization.

Counterparty traversal remains relationship-scoped. Ledgerx may model what a
vendor relationship means to the subject company; it does not build a general
dossier of the vendor or traverse the vendor's unrelated supply chain.

## Alternatives and tensions

- Starting from the ledger gives a deterministic counterparty inventory but
  misses unposted, disputed, prospective, and contractual relationships.
- Starting from mail and documents finds rich context but can overrepresent
  noisy or inactive relationships.
- A graph joined across transactions, agreements, communications, and reviewed
  facts is more complete but requires strong entity and effective-period
  reconciliation.

## Open questions

- Which accounting and corporate-record facets form the minimum establishment
  matrix?
- How are customer correspondence, legal privilege, payroll, tax, and banking
  data segregated?
- Which counterparty materiality rules govern recursive depth and review?
- When can recurring stable extraction patterns crystallize into deterministic
  Ledgerx capabilities?

## Relationships

This profile specializes the [evidence-estate manifest](hermes-recursive-subject-establishment-evidence-estate-manifest.md),
[relationship graph](hermes-recursive-subject-establishment-relationship-graph-and-traversal-scope.md),
[claim reconciliation](hermes-recursive-subject-establishment-claim-lineage-and-reconciliation.md),
and [coverage ledger](hermes-recursive-subject-establishment-coverage-gaps-and-readiness.md).
Domain evidence includes the
[Ledgerx Subject Document Estate](../../../xFactories/LedgerxFactory/ideation/brainstorm/subject-document-estate-overview.md),
[fact-sourcing synthesis](../../../xFactories/LedgerxFactory/ideation/brainstorm/subject-document-estate-synthesis-fact-sourcing.md),
and [vendor-contract terms](../../../xFactories/LedgerxFactory/ideation/brainstorm/subject-document-estate-vendor-contract-terms.md).

