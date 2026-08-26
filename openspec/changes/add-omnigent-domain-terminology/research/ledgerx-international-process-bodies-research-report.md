# Research report: UN/CEFACT and BIAN — the widening question, answered no

Status: record
Run: 2026-08-26 against live primary sources, answering LedgerxFactory
`openspec/changes/adopt-neutral-omnigent-overlay/supporting-docs/apqc-replacement-candidates-verification-prompt.md`
(`Status: record`, prepared 2026-08-09, never run until now).

The brief is NOT copied here. It is record-class evidence living in its own
repo, and the three sibling rounds pair prompt+report only because those
prompts were authored here. Cite the LedgerxFactory path above.

## The question this run actually answered

The brief was commissioned to fill a **process-layer gap** that APQC's
removal opened over the operational accounting workers. That premise is
gone: task 3b.5k lifted the APQC bar on 2026-08-26 (the 2026-08-09 verdict
had been read off apqc.org's site Terms of Service rather than the licence
printed on page 2 of the PCF itself), and task 3.2 put cross-industry PCF
8.0 back into the ledgerx overlay as a third body. There is no gap to fill.

Brett ruled on 2026-08-26 that the round still runs, against the narrower
surviving question recorded in task 3b.5f:

> Does UN/CEFACT or BIAN add **international process vocabulary BEYOND
> cross-industry PCF 8.0** for the ledgerx operational-accounting workers?

That is a **widening** question, not a gap-filling one. The answer is **no,
for both bodies, on grounds that do not depend on the licence** — which is
why this report leads with category rather than licence, inverting the
brief's own ordering and saying so.

## Executive conclusion

**Adopt neither. Register neither. The registry and the ledgerx overlay are
unchanged by this round, and nothing here is flagged as follow-up.**

1. **UN/CEFACT names data, not work.** The finance module of the current
   UN/CEFACT Web Vocabulary declares exactly five OWL classes —
   `FinanceAgreement`, `Payment`, `Account`, `Insurance`, `PaymentMeans` —
   plus object and datatype properties. The whole seven-domain ontology is
   classes, properties and SKOS code lists. "Buy", "Ship" and "Pay" are
   three narrative phases of a supply chain, not named process elements with
   identifiers. The Cross Industry Invoice is an invoice **document schema**.
   A body naming data artifacts cannot name work, exactly as the brief's
   Question Two anticipated. It adds **zero** process vocabulary, so it
   cannot add process vocabulary *beyond* PCF.
2. **BIAN names a bank's own services, not accounting work for clients.**
   BIAN Service Domains are capability partitions, each with a Functional
   Pattern, Asset Type and Control Record — `services_or_capabilities`, not
   `processes`. And the brief's domain-fit prior is **confirmed, not
   refuted**: BIAN's Financial Accounting Service Domain "lives in the
   accounting world of the bank"; Accounts Receivable handles "invoices
   issue by the bank"; Regulatory Reporting meets "the bank's" obligations.
   ledgerx keeps books **for client companies**. The overlap is nominal.
3. **The licences split in opposite directions, and neither rescues the
   category verdict.** BIAN — which fails category — has a genuinely usable
   Apache-2.0 route. UN/CEFACT — which also fails category — has a licence
   position that is *contradictory at primary source* and could not be
   resolved. Both are recorded below in full, because a licence finding is
   worth keeping even when the adoption question is already closed on other
   grounds, and because both are instructive replays of the APQC lesson.
4. **PCF 8.0 already carries the international reach the brief was chasing.**
   The motivation for these two candidates was that O\*NET is US-only. But
   the process layer is no longer O\*NET's to carry: APQC's own mandatory
   attribution paragraph describes the PCF as intended to work "regardless
   of industry, size, or geography", and the registry records `apqc_pcf`
   with `jurisdiction: international`. The international-reach argument was
   an artefact of the removed premise and does not survive its removal.

## Per-body verdicts

### A. UN/CEFACT

| Field | Finding |
|---|---|
| What was assessed | Buy-Ship-Pay Reference Data Model (BSP-RDM) / UN/CEFACT Web Vocabulary; Cross Industry Invoice (CII) |
| Steward | UN/CEFACT, under UNECE |
| Jurisdiction | international |
| Current version | The resolvable vocabulary publishes JSON-LD contexts **D22A, D22B, D23B**. It is being superseded by the consolidated **UN/CEFACT Web Vocabulary** at `vocab.unece.org`, built from the UN-hosted GitLab repo `un/unece/uncefact/vocab-bsp` (last activity 2026-08-26), which reconciles BSP with UNTP into one ontology across seven domains. **NOT verified:** a current BSP-RDM release designator or the CII version — see "What could not be verified" |
| `names` | `data_artifacts_or_messages` — verified, high confidence |
| Term list availability | public |
| Reuse licence | **CONTRADICTORY AT PRIMARY SOURCE — unresolved** |
| Redistribution in product config | `unclear` |
| Fit against the workers | **None of the 14.** Zero of the nine the brief listed |
| Verdict | **Do not adopt. Do not register.** |

**The licence contradiction, both sides quoted.** This is the APQC discipline
applied and, this time, coming back unresolved rather than corrected.

*Against.* `vocabulary.uncefact.org` is the site that actually serves BSP
element names and their URIs, and its own `/terms` page is the standard UN
site Terms and Conditions:

> The United Nations grants permission to Users to visit the Site and to
> download and copy the information, documents and materials (collectively,
> "Materials") from the Site for the User's personal, non-commercial use,
> without any right to resell or redistribute them or to compile or create
> derivative works therefrom, subject to the terms and conditions outlined
> below, and also subject to more specific restrictions that may apply to
> specific Material within this Site.

Personal, non-commercial, no redistribution, no derivative works. That is a
flat bar on precisely what a shipped overlay does.

*For.* The newer UNECE-operated deliverable sites carry, in the page footer
beneath "© 2026 United Nations Economic Commission for Europe":

> All UN/CEFACT standards are free to use under CC By 4.0 license

Verified byte-identical on **five** UNECE-operated hosts — `vocab.unece.org`,
`untp.unece.org`, `unlocode.unece.org`, `grid.unece.org`, `unvtd.unece.org`
— so it is a deliberate UN/CEFACT-wide assertion, not one site's typo.

*Why it stays unresolved.* The footer is a one-line claim, not a licence: it
links to no CC BY deed, states no attribution formula, and names no
licensor. There is **no `LICENSE`, `LICENCE` or `COPYING` file anywhere** in
the UN-hosted source repository the site is generated from. The two
statements are on different UNECE hosts, and the restrictive one is the
licence page of the artefact — the same relationship that made APQC's site
ToS the wrong document to read there, but with the roles reversed, because
here the restrictive text *is* on the publishing artefact's own terms page
and the permissive text is the incidental footer. Resolving it needs the
UN/CEFACT IPR Policy (ECE/TRADE/C/CEFACT/2010/20/Rev.2), which is
unreachable: `unece.org` answers **HTTP 403 to every automated fetch**
attempted, across the main site, `service.unece.org`, `tfig.unece.org`, and
direct PDF paths. Recorded as a gap rather than guessed.

**Nothing turns on it here.** Category already decides the case. Were
UN/CEFACT ever wanted for a data-layer purpose, this contradiction must be
resolved first — by a human reading the IPR Policy in a browser, the way
Brett read PCF 8.0's page 2.

### B. BIAN

| Field | Finding |
|---|---|
| What was assessed | BIAN Service Landscape / Service Domain names and identifiers |
| Steward | BIAN (Banking Industry Architecture Network), a not-for-profit association |
| Jurisdiction | international |
| Current version | **Service Landscape 14.0, released February 2026.** Confirmed independently: the deliverables page names 14.0, and every release-14 API artefact carries `version: 14.0.0` |
| `names` | `services_or_capabilities` — verified, high confidence |
| Term list availability | **Split.** Membership/registration-gated on bian.org; **public** for Service Domain names via the Apache-2.0 GitHub repository |
| Reuse licence | **Apache-2.0 for the repository artefacts**; "© 2026 BIAN. All rights reserved." on bian.org |
| Redistribution in product config | `yes_with_conditions` — for Service Domain names/identifiers as published in the Apache-2.0 repo only |
| Fit against the workers | **None of the 14 honestly.** Nearest is Account Reconciliation, and it is a bank's own internal reconciliation service |
| Verdict | **Do not adopt. Do not register.** Category and industry scope both fail |

**Membership gating: what is actually public today.** The brief asked
specifically, and the answer is a genuine split.

*Gated.* The Service Landscape deliverable page requires a registration form
(name, email, company, country, GDPR consent) for both 14.0 and 13.0. The
BIAN Intellectual Property Policy is a membership document obtainable only
by emailing `info@bian.org`. bian.org's own footer reads "© 2026 BIAN. All
rights reserved." — no reuse permission is published anywhere on the site,
and the IP-portfolio and imprint pages carry none either.

*Not gated.* `github.com/bian-official/public` carries a root `LICENSE` file
containing the **verbatim Apache License 2.0** (added in the initial commit,
2021-03-03) over a repository BIAN describes as "This is a repository of
BIAN artefacts, currently the BIAN Semantic APIs". It holds `release9.1`
through `release14.0.0`. Its README states plainly: **"Each API
Specification represents a BIAN Service Domain."** Release 14.0.0 contains
**259** such specifications. Each names its Service Domain in the clear:

```yaml
info:
  title: Financial Accounting
  description: 'The Financial Accounting Service Domain takes in financial
    facts and based on these, creates accounting instructions that will
    update the general ledger and sub ledger accounts'
  version: 14.0.0
```

No file carries an internal copyright notice contradicting the repo licence,
and there is no `NOTICE` file. A second repo, `bian-official/artefacts`, is
also Apache-2.0 and holds per-Service-Domain CSVs that **do** carry the
Service Landscape placement.

**The specification/data split, and which way it cuts.** The brief's
Question One item 5 asked whether the licence differs between the
specification document and the element data. It does, and — unlike APQC —
it cuts *in our favour on the data*:

- **Service Domain names and descriptions at 14.0: Apache-2.0, usable.**
- **The Service Landscape hierarchy at 14.0: not in any Apache-2.0 artefact.**
  The current hierarchy ships through the registration-gated portal under
  "all rights reserved". The Apache-2.0 `artefacts` repo does hold the
  hierarchy — `"Business Area" Operations` → `"Business Domain" Accounting
  Services` → `"Service Domain" Financial Accounting` — but it was last
  committed **2021-10-06** ("Upload of Artefacts") and carries no version
  stamp. It is a ~2021-vintage snapshot, five years and roughly six releases
  behind 14.0. Citing hierarchy positions from it as current would be a
  wrong citation of exactly the kind this programme has twice corrected.

So the honest statement is: the Apache-2.0 grant reaches Service Domain
names at the current release, and reaches the Service Landscape hierarchy
only at a stale one. Recorded because it is a real finding, not because it
changes the outcome.

**Domain fit — the brief's prior confirmed.** The brief offered its prior
"for you to confirm or refute". Confirmed, on BIAN's own words from the
Apache-2.0 artefacts:

| BIAN Service Domain | BIAN's own text | Why it is not our work |
|---|---|---|
| Financial Accounting | "It **lives in the accounting world of the bank** … It knows and maintains the chart of accounts and it can create accounting instructions that will update the general ledger and sub ledger accounts" | A bank's internal posting engine over the bank's own GL |
| Accounts Receivable | "handles accounts receivable for **invoices issue by the bank** to customers and partners" | The bank as creditor, not a bookkeeper for a client |
| Account Reconciliation | "This Service Domain handles account reconciliation tasks" | The bank's own internal reconciliation |
| Regulatory Reporting | "the tasks required to meet **the bank's** regulatory reporting obligations" | The bank's own obligations |
| Compliance Reporting | "apply and report on internal audit control and reporting activity" | The bank's internal audit function |
| Customer Tax Handling | "consumer tax reporting obligations including the consolidation and reporting of customer tax related financial activity" | A bank's tax-reporting duty toward its account holders, not tax workpaper preparation |
| Corporate Tax Advisory | "A **fee or commission based product** providing tax specific assessments, advice and guidance" | A banking product; and advisory authority these workers do not hold |

There is a second, sharper objection. BIAN's finance Service Domains are
**automated execution services** — Financial Accounting *creates accounting
instructions that update* the general ledger. Every ledgerx worker is
artifact-only under a constitutional `execute_final_action: false`. Naming
one of these workers with a Service Domain whose defining act is updating
the GL would be precisely the authority-implying mislabel the brief told us
to flag. Even the nearest candidate is not merely a weak fit; it is a
dishonest one.

## Per-worker fit table

The brief listed nine workers; the shipped overlay declares fourteen. All
fourteen are assessed, since a widening question has to be asked of the
whole set.

| Worker | UN/CEFACT | BIAN |
|---|---|---|
| document_intake_processor | none — names documents, not the framing of them | none |
| document_fact_reader | none — an ontology of facts is not a fact-sourcing role | none |
| invoice_coder | none — `Invoice` is a document class, not the act of coding one | none |
| bookkeeper | none | none — nearest names posting, which this worker cannot do |
| reconciliation_specialist | none | Account Reconciliation is nominal only; a bank's own reconciliation, and the worker already carries PCF 9.3.2.6 (10824) and a COSO component |
| close_accountant | none | none — BIAN has no period-close Service Domain for a client's books |
| tax_preparation_assistant | none | none — Customer Tax Handling and Corporate Tax Advisory are both bank-side |
| counterparty_analyst | none — `Party` classes name parties, not profiling work | none |
| scenario_modeler | none | none |
| books_designer | none — no chart-of-accounts design concept | none — Financial Accounting *maintains* a bank's chart of accounts; it does not draft a client's |
| ledger_platform_specialist | none | none |
| controller_reviewer | none | none |
| compliance_reviewer | none | none — Compliance Reporting is the bank's internal audit function |
| posting_admission_agent | none | none — every near neighbour names the terminal act this worker is barred from |

Fourteen of fourteen, twice over. "Fits none of them" was named an
acceptable answer in the brief; it is the answer.

## No crosswalk-candidate table

Neither body passes, so none is offered. This section exists to say the
omission is the finding.

## Is there a better process-layer candidate?

The brief's Question Four asked. The honest answer is that the question is
**moot as posed**: it assumed an empty process layer, and cross-industry PCF
8.0 now occupies that slot with a licence that grants "a perpetual,
worldwide, royalty-free license to use, copy, publish, modify, and create
derivative works of the PCF", conditional only on one verbatim attribution
paragraph, and with a stated scope that is already geography-neutral.

This run **did not** survey beyond the two named bodies, and does not claim
that no other candidate exists. It claims that the two bodies actually named
do not displace or widen PCF 8.0, and that no further search was authorised
by 3b.5f's narrowed question.

## What could not be verified

Recorded rather than guessed, per the brief's ground rules:

- **A current BSP-RDM release designator and the CII version.** `unece.org`
  answers HTTP 403 to every automated fetch. The three JSON-LD contexts
  D22A/D22B/D23B are what the resolvable vocabulary itself publishes and are
  reported as such, not as "the current version".
- **The UN/CEFACT IPR Policy text** (ECE/TRADE/C/CEFACT/2010/20/Rev.2).
  Same 403. It is the document that would settle the CC BY contradiction.
- **BIAN's Intellectual Property Policy.** A membership document, released
  only on request to `info@bian.org`. The Apache-2.0 LICENSE file was read
  in full instead; whether the IP Policy says anything that qualifies it is
  unknown.
- **Acronym-collision check performed, per the brief's warning:** the "BIAN"
  assessed is the Banking Industry Architecture Network at `bian.org` and
  `github.com/bian-official`, confirmed by the org README's link to
  `https://bian.org/`. No collision found.

## Registry-shaped YAML

None. Neither body is recommended for registration, so no entry is proposed.
Reproducing entries for bodies we decline would put terms into the tree that
nothing may cite.

## Recommendation

Do not adopt UN/CEFACT. Do not adopt BIAN. Do not register either. Leave
`contracts/policies/standards-bodies.yaml` and the ledgerx
`omnigent/domain-overlay.yaml` untouched by this round.

Keep for the record, because they are true and were expensive to establish:
BIAN Service Domain names at 14.0 are Apache-2.0 and would be lawfully
embeddable if a banking domain ever needed them; UN/CEFACT's reuse position
is contradictory at primary source and must be resolved by a human before
any UN/CEFACT term is embedded for any purpose.

Task 3b.5f closes on this report. It was the last of the five briefs it
tracked.

## Sources

Primary sources only. Where a page is quoted, the quote is verbatim.

UN/CEFACT:

- UN/CEFACT Web Vocabulary (consolidated): https://vocab.unece.org/
- Resolvable BSP vocabulary, About: https://vocabulary.uncefact.org/about
- Resolvable BSP vocabulary, Terms and Conditions of Use: https://vocabulary.uncefact.org/terms
- UN-hosted source repository (UNICC GitLab): https://opensource.unicc.org/un/unece/uncefact/vocab-bsp
- Finance ontology module (five classes, verified): `ontology/finance/finance.ttl` in the repository above
- UN/CEFACT GitHub organisation (retiring; spec repos carry no licence): https://github.com/uncefact
- Footer licence assertion verified identically on: https://untp.unece.org/ , https://unlocode.unece.org/ , https://grid.unece.org/ , https://unvtd.unece.org/
- Unreachable to automation (HTTP 403), recorded: https://unece.org/trade/uncefact/rdm , https://unece.org/trade/uncefact/mainstandards , https://unece.org/terms-use

BIAN:

- Service Landscape deliverable (registration-gated): https://bian.org/deliverables/service-landscape/
- Service Landscape 14.0 portal: https://bian.org/servicelandscape-14-0-0/
- V14.0.0 Release Notes: https://bian.org/wp-content/uploads/2026/02/BIAN-v14.0-Release-Notes-v1.0_-Final-Version.pdf
- Imprint (© 2026 BIAN. All rights reserved.): https://bian.org/bian-imprint/
- Intellectual property portfolio page (publishes no licence text): https://bian.org/semantic-apis/intellectual-property-portfolio
- Apache-2.0 artefact repository and its LICENSE: https://github.com/bian-official/public and https://github.com/bian-official/public/blob/main/LICENSE
- Release 14.0.0 Service Domain specifications (259 files): https://github.com/bian-official/public/tree/main/release14.0.0/semantic-apis
- Apache-2.0 Service Landscape CSVs (2021 vintage): https://github.com/bian-official/artefacts

Internal, for the premise change:

- APQC verdict correction: task 3b.5k of `add-omnigent-domain-terminology`
- The brief being answered: LedgerxFactory `openspec/changes/adopt-neutral-omnigent-overlay/supporting-docs/apqc-replacement-candidates-verification-prompt.md`
