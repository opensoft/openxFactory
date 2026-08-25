# Synthesis: Discovery and Acquisition — Brainstorm

Status: brainstorm
Kind: architecture
Summary: A typed recursive frontier can inspect a versioned evidence estate, turn source clues into governed acquisition obligations, and expand knowledge without expanding permission.
Topics: hermes-recursive-subject-establishment, discovery-acquisition, recursive-evidence-frontier, evidence-estate-manifest, evidence-acquisition-obligation, synthesis
Repository context: openxFactory neutral subject evidence discovery and acquisition coordination
Captured: 2026-07-30

## Possible feats

- **Recursive evidence-estate closure loop** — alternate discovery, authorized
  acquisition, manifest update, and frontier reprioritization while preserving
  negative and unavailable-source evidence.

## Members and their joints

Atomic members:
[Recursive Evidence Frontier](hermes-recursive-subject-establishment-recursive-evidence-frontier.md),
[Subject Evidence-Estate Manifest](hermes-recursive-subject-establishment-evidence-estate-manifest.md),
[Source Leads and Evidence-Acquisition Obligations](hermes-recursive-subject-establishment-source-leads-and-acquisition-obligations.md),
and
[Authority, Consent, and Subject Rights](hermes-recursive-subject-establishment-authority-consent-and-subject-rights.md).

```text
known evidence estate
        |
        v
select frontier question
        |
        v
inspect authorized representations
        |
        +--> claim or relationship candidate
        |
        +--> source lead
                  |
                  v
         authority and identity checks
                  |
                  v
         acquisition obligation
                  |
                  v
         approved request / retrieval
                  |
                  v
         manifest version advances
                  |
                  +------> frontier repeats
```

### Discovery is not acquisition

Metadata or a cited reference can establish that a source may exist. It does
not establish that xFactory may retrieve, retain, process, or disclose the
source. The source lead preserves that intermediate state so the controller
does not either forget the clue or overreach.

### The manifest supplies denominators

The evidence-estate manifest provides the known source universe and exact
representations selected for a bounded pass. It can represent
`discovered_metadata_only`, unavailable, prohibited, or partially received
sources rather than forcing everything into a binary ingested/not-ingested
view.

This supports honest coverage over the known estate while acknowledging that
open-world discovery can never prove a universal denominator.

### Obligations make missing evidence operable

An evidence obligation attaches the missing question to a suspected custodian,
discovery basis, acquisition route, authority requirement, materiality, and
attempt history. It converts "we should get the old CT" or "find the vendor
amendment" into a durable, reviewable handoff.

Several obligations may collapse when one source arrives; one obligation may
remain open after a partial response. Negative outcomes remain evidence for
readiness and future follow-up.

### Recursive expansion stays narrower than authority

The frontier may discover a new provider, counterparty, portal, or record
class. The mandate decides whether that descendant is in scope. The system may
record a minimized prohibited-source encounter without reading or retaining
its content.

## Emergent behavior

The cluster turns intake from a bulk upload into an adaptive evidence-closure
process. The partial model guides acquisition, and acquisition reshapes the
model, while each step retains a stable source, authority, and attempt trail.

## Tensions to hold

- Client- or patient-selected records reduce access but may omit contradictory
  evidence.
- Automated acquisition improves speed but increases relationship, privacy,
  identity, and records risk.
- Rich manifest metadata supports reasoning but can itself reveal sensitive
  relationships.

## Recombination opportunities

The loop can feed the staged neutral
[Subject Establishment](../staging/subject-establishment/subject-establishment.md)
fact-set step and reuse domain document, mailbox, EHR, ledger, and public-source
bindings rather than standardizing their provider details.

## Open questions

- Is evidence acquisition a neutral subject-establishment sub-capability or a
  composition of existing follow-up and job contracts?
- What minimum metadata may survive for a prohibited or erased source lead?
- How are duplicate requests prevented across concurrent episode passes?

