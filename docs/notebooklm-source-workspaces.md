# NotebookLM Source Workspaces

Status: draft
Kind: reference
Repository context: openxFactory
Purpose: define how NotebookLM notebooks may be used as source workspaces for
Hermes layers and domain agents without confusing notebook synthesis with
ground truth.

Related: lifecycle-derived notebooks over the governance corpus itself are
governed by [Lifecycle Notebook Projection](lifecycle-notebook-projection.md).

## 1. Role In xFactory

NotebookLM is a mediated source workspace.

It may help a Hermes layer or domain agent collect, search, summarize, compare,
and discuss source material. It is not itself a ground-truth authority, policy
source, medical source, legal source, customer memory, or workflow gate.

The generic chain is:

```text
ground truth source
  -> NotebookLM notebook
  -> NotebookLM output or note
  -> xFactory source trace
  -> Hermes review, approval, rejection, or memory update
  -> domain workflow or agent context
```

NotebookLM outputs may inform work. They may not decide regulated, high-risk,
customer-affecting, or policy-setting work unless the relevant ground sources
are traced and the correct Hermes layer accepts the claim.

## 2. Allowed Uses

NotebookLM workspaces may be attached to any Hermes layer or to a domain agent
task.

Customer Hermes may use a NotebookLM workspace for:

- customer-specific context packets
- patient, buyer, project, matter, or account source collections
- private summaries used inside the customer boundary
- customer-facing explanations after review

Client Hermes may use a NotebookLM workspace for:

- client policy binders
- tenant operating manuals
- client-specific SOPs
- client integrations and vendor docs
- staff credential, privilege, or coverage source packets

Domain Hermes may use a NotebookLM workspace for:

- domain literature review
- regulations and standards review
- domain playbook drafting
- root truth corpus exploration
- reusable lifecycle, journey, outcome, and intervention research

Domain Omnigent or domain agents may use a NotebookLM workspace for:

- task-specific context bundles
- source-guided synthesis
- claim extraction
- draft review packets
- comparison tables
- domain research briefs

## 3. Authority Rule

NotebookLM can be a source of context, synthesis, and leads. It is not the final
source of truth.

Use this rule:

```text
NotebookLM output may raise a claim.
Ground sources must support the claim.
Hermes must decide whether the claim may enter memory, policy, workflow, or
customer-facing output.
```

For low-risk internal exploration, a NotebookLM synthesis may remain a draft.
For any domain memory update, customer intervention, policy update, regulated
decision, or external-facing output, the trace must reach the original ground
source.

## 4. Source Authority Levels

Every NotebookLM-derived artifact should carry a source authority level.

| Level | Name | Meaning | May drive workflow gates? |
| --- | --- | --- | --- |
| `L0` | `unverified_note` | Human or AI note with no checked source trail | No |
| `L1` | `notebook_synthesis` | NotebookLM answer, summary, guide, table, or note | No |
| `L2` | `notebook_cited_source` | Claim is tied to a NotebookLM source or citation | No, except low-risk draft gates |
| `L3` | `ground_source_verified` | Claim has been checked against the original article, paper, regulation, chart, policy, or document | Sometimes, if the domain allows it |
| `L4` | `hermes_reviewed_truth` | Relevant Hermes layer accepted the claim for customer, client, or domain use | Yes, within scope |
| `L5` | `operational_policy` | Claim has been approved as a policy, gate, routing rule, or workflow requirement | Yes |

NotebookLM output should default to `L1`. A cited NotebookLM answer may support
`L2`. It reaches `L3` only after the original source is inspected and recorded.
It reaches `L4` or `L5` only after Hermes review.

## 5. Traceability Chain

Every NotebookLM-derived claim used outside exploration must preserve this
chain:

```text
claim
  -> NotebookLM output or note
  -> notebook record
  -> notebook source record
  -> original ground source
  -> cited passage, page, section, timestamp, or document-level citation
  -> verification record
  -> Hermes review decision
  -> workflow, memory, policy, or agent artifact that consumed it
```

NotebookLM citations are useful, but xFactory must not assume they are complete.
If the notebook cites only an entire source, the verifier must record the
document-level citation and decide whether that is enough for the use case. If
the use case requires exact support, the verifier must add page, section,
paragraph, timestamp, quote-limited excerpt, or other source location metadata.

## 6. Required Records

Domain factories that use NotebookLM should support these record families.

```yaml
kind: external_source_workspace
schema_version: 1
id: workspace-medx-oncology-review
provider: notebooklm
owner_layer: domain_hermes
scope:
  domain_id: medx
  client_id: null
  customer_id: null
purpose: oncology literature and scope review
default_authority_level: L1_notebook_synthesis
created_at: "2026-06-30T00:00:00Z"
source_inventory_ref: source-inventory-medx-oncology-review
```

```yaml
kind: notebook_source
schema_version: 1
id: notebook-source-003
workspace_id: workspace-medx-oncology-review
source_title: State nursing board procedure guidance
source_type: web_url
ground_source_ref: ground-source-003
imported_at: "2026-06-30T00:00:00Z"
authority_level: L2_notebook_cited_source
```

```yaml
kind: ground_source
schema_version: 1
id: ground-source-003
source_type: regulation
title: State nursing board procedure guidance
uri: https://example.invalid/state-nursing-board/procedure-guidance
publisher: Example State Nursing Board
retrieved_at: "2026-06-30T00:00:00Z"
content_hash: sha256:<hash-if-available>
source_location:
  section: "Scope of Practice"
  page: null
  timestamp: null
```

```yaml
kind: notebooklm_claim_trace
schema_version: 1
id: claim-trace-001
claim:
  id: claim-001
  summary: LVN cannot perform the procedure unless a domain exception applies.
  authority_level: L2_notebook_cited_source
workspace_ref: workspace-medx-oncology-review
notebook_source_refs:
  - notebook-source-003
ground_source_refs:
  - ground-source-003
verification:
  status: pending_domain_review
  required_next_level: L4_hermes_reviewed_truth
  reviewer_layer: domain_hermes
consumers:
  - medx-domain-policy-draft
```

## 7. Layer Ownership

Customer Hermes owns NotebookLM workspaces that contain customer-specific data.
Those workspaces inherit the customer consent, privacy, memory, and sharing
boundaries.

Client Hermes owns NotebookLM workspaces that contain client-specific operating
data, staff data, client policies, local procedures, vendor docs, and tenant
records.

Domain Hermes owns NotebookLM workspaces that contain reusable domain knowledge,
domain regulations, standards, research, playbooks, and policy source material.

Domain agents may create or consume task workspaces only inside an approved job
or standing approval envelope. Agent workspaces must declare which Hermes layer
owns the source truth and where review must happen.

## 8. Promotion Rules

NotebookLM-derived information may move between layers only through explicit
promotion.

Customer to client:

```text
customer-specific notebook finding
  -> customer Hermes consent and privacy check
  -> client Hermes relevance and authorization review
  -> client memory update or rejection
```

Customer or client to domain:

```text
customer/client finding
  -> de-identification when required
  -> ground source verification when required
  -> domain Hermes review
  -> domain memory, policy, model, or workflow update
```

Domain to client or customer:

```text
domain-reviewed knowledge
  -> client policy fit check
  -> customer consent and applicability check
  -> customer-facing or client-facing output
```

No NotebookLM output may silently update shared domain experts or customer
memory.

## 9. Required Domain Policy

Each domain factory that uses NotebookLM must define:

- allowed NotebookLM workspace scopes
- which Hermes layer may create each scope
- allowed source types
- prohibited source types
- default source authority level
- verification requirements by use case
- review requirements by authority level
- retention and export expectations
- customer data restrictions
- client data restrictions
- domain memory promotion rules
- traceability fields required before use

Example policy:

```yaml
notebooklm:
  allowed_as:
    - customer_context_workspace
    - client_policy_workspace
    - domain_research_workspace
    - agent_task_workspace
  default_authority_level: L1_notebook_synthesis
  requires_ground_source_trace_for:
    - domain_memory_update
    - policy_update
    - regulated_decision
    - customer_intervention
    - external_facing_output
  requires_hermes_review_for:
    - L4_hermes_reviewed_truth
    - L5_operational_policy
```

## 10. Validation Requirements

Validation should fail when:

- a NotebookLM-derived claim lacks a workspace reference
- a claim above `L1` lacks a notebook source reference
- a claim above `L2` lacks a ground source reference
- a claim above `L3` lacks a Hermes review record
- a regulated workflow consumes `L1` or `L2` synthesis as if it were ground truth
- customer-specific NotebookLM content is referenced by client or domain memory without promotion evidence
- a domain policy or workflow gate points directly to NotebookLM output instead of reviewed truth or operational policy

## 11. Official Product Notes

NotebookLM is a Google AI research and source-analysis tool. Google describes
it as able to analyze user-provided sources, and NotebookLM Help documents web
or Drive source discovery through Fast Research and Deep Research. Google also
notes that citations may sometimes reference an entire document rather than an
individual cited text when source content is short.

References:

- [NotebookLM](https://notebooklm.google/)
- [NotebookLM Help: Add or discover new sources](https://support.google.com/notebooklm/answer/16215270)
- [NotebookLM Help: Frequently asked questions](https://support.google.com/notebooklm/answer/16269187)
