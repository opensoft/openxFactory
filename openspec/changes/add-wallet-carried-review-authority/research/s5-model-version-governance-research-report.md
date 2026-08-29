# S5 Model-Version Governance Research Report

Status: complete research snapshot; no implementation is authorized
Prepared: 2026-08-29; amended 2026-08-29 (fold-in of the parallel research
document, see section 8)
Authority context: `add-wallet-carried-review-authority` S5

## Executive Summary

This report prepares four distinct decision packets. It does not select a
Council model, select an exact provider version or deployment, declare an alias
admissible, claim live tenant availability, record a ratification, or authorize
implementation.

The ratified Q8 baseline is fail-closed: Q8(a) requires a new explicit
human-ratified register act before re-issuance; Q8(b) makes DRIFT revoke derived
grants as CAUSE does; and Q8(d) requires exact model versions only. A provider
alias roll is not transparent continuity. Current Council transport passes
mutable `opus` and `sonnet` aliases directly to Claude Code without a
repository-local exact-ID expansion, so it cannot satisfy Q8(d) as it stands.
[1][2][3]

The decision owners remain separate. The Gate-Rules Council selects which model
or model family represents a seat based on local duty-specific soak evidence;
the Council convener accepts or rejects that output on record, and applying an
accepted selection to the enrolled roster requires recorded Lead acceptance.
The Operator independently selects and evidences the exact published provider
version and live execution or deployment identity. Packet 2 gates issuance and
activation; it does not invalidate a Council seat-selection decision. The S5
Convener alone can rule on a future relaxation of admissible pin form. Human
ratification governs issuance, re-issuance, and any new serialization standard.
[4][8]

Exact provider IDs are artifact targets, not universal cryptographic serving
digests. They do not freeze routing, safety systems, infrastructure, region,
fallback behavior, or outputs. Provider response metadata is execution evidence,
not cryptographic attestation. [5][9][10][11][12][13]

This report was amended on 2026-08-29 to fold in a second, independently
fidelity-reviewed research pass, which adds a screening-evidence and
recommendation annex carrying the binding seat-diversity constraint and a
candidate evidence register (section 2A), verified provider mutation, lifecycle,
and platform facts (section 3), the 2026-08-28 ruling of record that closes
Packet 3 (section 4), verified holder-side and wallet-side composition findings
with the remaining Packet 4 gap evidence (section 5), and a fact-level
unresolved annex (section 7A); it adds evidence and labeled recommendations
only, and selects nothing. [19]

## Decision Boundary

1. Packet 1: Gate-Rules Council seat-to-model or model-family selection.
2. Packet 2: Operator exact provider-version and execution-identity evidence.
3. Packet 3: Convener ruling on admissible pin forms (ruled 2026-08-28; see
   section 4).
4. Packet 4: human ratification of canonical composition and re-issuance
   semantics.

No packet substitutes for another. A Council selection cannot prove live
provider availability. Operator evidence cannot relax Q8(d). Runtime or core
enforcement cannot ratify. A provider response cannot ratify serialization
semantics.

## 1. Governing Baseline

Q8(d) requires exact model versions only. A hosted holder may not pin a family
such as `gpt-5.x`; the current validation failure for a family pin is intended.
Q8(a) requires re-issuance to be an explicit human-ratified register act. Q8(b)
requires DRIFT revocation to cascade to derived grants as CAUSE does. The
agent-profile contract separately requires a declared composition change to end
the agent's certified identity, without a tolerance band or grace period.
[1][6][7]

The current Council roster intends diversity but does not meet exact-version
identity: `lead-security` and `lead-integration` receive `opus`, and
`lead-quality` receives `sonnet`; the workflow passes those aliases to Claude
Code. The workflow requires a recorded roster change and fresh soak before a
later model-map change, and the task ledger expressly divides Council model
choice from Operator exact-version choice. [2][3][4][14]

The folded-in research pass left the transport platform undetermined and
therefore treated the platform half of every candidate pin as unresolved. This
report's workflow evidence resolves the transport: the council-deliberation
worker passes its `SEAT_MODELS` aliases to Claude Code, so the live pinning
hazards for the current path are the Claude Code and direct-Anthropic ones. The
one that must be asserted is Anthropic's opt-in server-side `fallbacks` beta
(`server-side-fallback-2026-07-01` and `-2026-06-01`), which routes a refused
request to a different model and is a deliberate substitution mechanism: a
governed seat must not set it, and the evidence record should assert its
absence. The configured provider surface underneath that transport is still an
Operator execution-identity field, so the partner-plane hazards recorded in
section 3 remain live for any partner-hosted selection. [3][19][20]

## 2. Packet 1: Council Seat-to-Model Selection

### Ratified Minimum And Recommended S5 Template

The ratified minimum is that exact version identity is required for a hosted
holder and that composition drift fails closed. It does not prescribe a Council
shortlist grammar, soak-case schema, or Council record fields. The following
tables are **recommended S5 decision and evidence templates**, proposed to make
the Council decision reproducible. They are not ratified policy.

### Decision Requested

For each required seat, the Gate-Rules Council selects a model or model family
as the seat's representative based on duty-specific soak evidence, or retains
`unresolved - Council`. The Council does not select the Operator's exact
provider version, account, region, profile, or deployment. Those facts are
independently selected and evidenced in Packet 2. Packet 2 completeness gates
issuance and activation after a Council choice; it does not gate the validity of
the Council's selection decision. Aggregate benchmarks may screen candidates but
cannot be final seat-governance evidence. [2][18]

The current codexFactory route adds two operational acceptance acts inside this
packet's boundary. The Council convener accepts or rejects the Council output on
record, and applying an accepted choice to the enrolled workflow roster requires
the separate `lead_accepted_recorded` roster-change route. Neither acceptance is
the human-ratified register act required later for issuance or re-issuance.
[4][8]

### Recommended Seat Duties And Evidence Bar

| Seat | Duty | Recommended pass evidence | Recommended failure evidence | Status |
|---|---|---|---|---|
| `lead-quality` | Detect incomplete rationale, unsupported claims, missing conditions, and evidence gaps. | Local soak cases show grounded rationale, correct `ready` or `blocked` disposition, and all unresolved conditions returned in the required schema. | Hallucinated evidence, omitted material condition, malformed output, or an ungrounded `ready`. | unresolved - Council |
| `lead-security` | Find abuse paths, unsafe assumptions, untrusted-input mistakes, and authority or boundary failures. | Local adversarial soak cases identify the planted issue or block honestly; refusal and uncertainty behavior remain correct. | Missed seeded security defect, candidate text treated as instructions, invented assurance, or bypassed refusal. | unresolved - Council |
| `lead-integration` | Check system facts, CI state, base freshness, contract and workflow compatibility, and operational handoff. | Local soak cases use packet facts correctly, identify integration blockers, and refuse when a required fact is absent. | Missing fact treated as a default, declared interface mismatch overlooked, or unsupported approval. | unresolved - Council |
| `company-policy-lead` | Conditional rules-council-only policy review when a candidate class explicitly pulls it in. | Local policy cases apply only the declared policy packet and escalate ambiguity explicitly. | Policy applied outside the packet, ambiguity silently resolved, or authority overclaimed. | unresolved - Council |

The current enrolled execution surface has three seats. `company-policy-lead`
is conditional, not a fourth default worker. Its inclusion must be recorded for
the applicable candidate class. [4][8]

### Recommended Soak-Test Record

| Field | Recommended content |
|---|---|
| Seat candidate | Seat, model or model-family label, provider plane, research date, and candidate capability assumptions. No exact deployment selection is required. |
| Composition context | Seat ID, rendered prompt-contract digest, tool manifest digest, policy version, parameters, and retrieval reference. |
| Corpus | Versioned local cases for ordinary review, security adversarial input, missing facts, malformed input, and abstention or refusal. |
| Results | Per-case expected and actual disposition, rationale-quality assessment, schema validity, turn and budget observations, and failure classification. |
| Pass rule | Every mandatory case passes, with no critical false `ready`, missing required condition, ungrounded claim, or unexplained schema or invocation failure. |
| Failure rule | Any mandatory-case failure rejects the candidate for that seat until a new candidate and fresh soak are reviewed. |
| Decision evidence | Test date, runner and environment, stable evidence reference, Council signatures, selection or deferral, and scope limitation. |

### Recommended Shortlist And Diversity Analysis

| Field | Recommended treatment |
|---|---|
| Seat | Named seat and duty from this packet. |
| Candidate model or family | `unresolved - Council` unless a dated screening candidate has been verified from first-party provider documentation. A named ID is screening evidence, never an Operator version selection. |
| Provider plane | Direct provider, partner-hosted plane, and API or CLI surface. Do not conflate direct Anthropic, Claude on Vertex, Bedrock, or Foundry. |
| Capability fit | Local duty-specific soak outcome, not a leaderboard rank. |
| Independence and diversity | Model family, provider plane, prompt contract, tool set, retrieval corpus, and likely failure-mode overlap. Different names or hashes alone do not prove sufficient reviewer independence. |
| Constraints | Lifecycle considerations, known substitution behavior, and unresolved evidence. Operator deployment facts belong in Packet 2. |
| Decision | Select, reject, defer, or request evidence, with Council signatures and date. |

The current `opus` and `sonnet` assignments evidence a model-diversity aim, not
proven independence. Security and integration share an alias while quality uses
a different alias. That arrangement needs seat-specific evidence and an explicit
diversity analysis. [3][4]

### Recommended Council Decision Record

For each seat, record the selected model or model family, or `unresolved -
Council`; rejected alternatives and reasons; soak evidence reference;
independence and diversity finding; decision scope; effective time; re-review
trigger; and Council signatures. The Council owns selection, while the current
operational route separately records the Council convener's acceptance or
rejection and, before an enrolled roster change is applied, the designated
Lead's acceptance. Those records operationalize the selection but do not issue
or re-issue a grant. Only the later explicit human-ratified register act does
that. [4][8]

## 2A. Screening Evidence And Recommendation Annex (not a selection)

This annex recommends; it does not select. Selection is the Council's act under
section 2; nothing here fills a Packet 2 field. Everything below is screening
evidence or a labeled recommendation, folded in from the parallel research pass
and carrying that pass's citations. [19]

### Binding Diversity Constraint (verified ratified text)

Section 2's recommended diversity analysis is a template. The constraint it must
satisfy already exists and is binding. The Gate-Rules Council's Q3 liaison
disposition of 2026-08-22 reads, in part and verbatim:

> Disposition: MODEL-DIVERSE SEATS FOR THE ENROLLED SURFACE, FIXED BEFORE THE
> FIRST SOAK ROW - the four convergent seat rulings adopted as returned: at
> least two distinct models across the three enrolled-surface seats; no fourth
> seat (that would amend `merge-readiness.yaml`'s ratified membership); the
> nightly surface stays as ratified; the roster change is a workflow edit on a
> CODEOWNERS-gated, floored path, routed through `roster_change:
> lead_accepted_recorded`

The 2026-08-26 classification-intent disposition extended the rule to the
fourth, conditional seat by declaring `sonnet` for `company-policy-lead`,
"preserving the 2:2 diversity the 2026-08-22 Q3 ruling sought rather than making
the bench 3:1 on opus", restated tenant-side as "opus: lead-security,
lead-integration; sonnet: lead-quality, company-policy-lead". The standing
constraint is therefore at least two distinct models across the three
enrolled-surface seats, realized as a 2:2 split across all four. [27]

There are two diversity axes and only one is ruled. The floor counts distinct
MODELS; it does not require distinct PROVIDERS. The substantive argument
recorded for it was made about one model, not one vendor: "Three seats on one
model with three prompts are not three independent tests; they are one test run
three times with different framings. Unanimity across correlated seats is worse
than a single seat evidentially, because it converts three correlated draws into
one verdict presenting as 3/3 agreement." Whether that argument reaches a
one-vendor bench is a Council ruling, not a reading of the existing one. [27]

Two cautions travel with this evidence base:

- The seeded adversarial corpus is not evidence that seat diversity is
  unnecessary, and says so in its own words: "Anyone citing this record for the
  proposition that seat diversity is unnecessary is citing it wrongly." Nothing
  was missed by anybody in that corpus, so the instrument has no resolution on
  the question in either direction. This change's own proposal already quotes
  that warning rather than omitting it. [28][31]
- A composition digest is not a diversity or independence measure. The recorded
  finding is that a digest-disjointness test "rejects the right case and admits
  the wrong one": different weights under a shared prompt contract fail it,
  while two seats on the same base model with independently authored prompts,
  tools, and corpora pass it while being maximally correlated. Pinning model
  versions does not discharge the diversity constraint. [31]

Two leads bear on whether an alias-to-exact-version flip re-opens the soak, and
neither settles it. The re-open-soak clause is attached to the diversity
disposition itself ("any later roster change re-opens the soak"), not only to
the roster record, so it travels with the constraint. And the one recorded
instance of the clause being reasoned about and found not triggered turns on an
identity test on the recorded roster ("The roster of the roster record 2.1 is
unchanged"), applied to a case in which nothing was edited at all. The
recommendation below is that the Council rule the point explicitly in the same
act rather than let it be settled by default. [27][28]

### Candidate Evidence Register (screening evidence)

Identifiers are spelled exactly as the surveyed first-party documentation spells
them. Classification is alias versus snapshot per that documentation: string
shape is not a reliable test of mutability, and a spelling not verified against
a provider catalog does not appear here. Lifecycle floors are published
earliest-retirement dates, not commitments about behavior. [9][20][21]

| Candidate exact identifier | Class | Alias that must not be recorded as the pin | Published mutation semantics | Retirement floor | Pinnability note |
|---|---|---|---|---|---|
| `claude-opus-5` | Snapshot (dateless but pinned) | none published; never record the transport selector `opus` | "Anthropic does not update the weights or configuration of an existing model ID. When an updated version is available, it ships under a new model ID." | Not sooner than 2027-07-24; at least 60 days of notice | Strongest published guarantee in the survey, and the longest horizon; the guarantee covers weights, while serving infrastructure "can change over time". |
| `claude-sonnet-5` | Snapshot (dateless but pinned) | none published; never record the transport selector `sonnet` | As above. | Not sooner than 2027-06-30 | As above. |
| `claude-opus-4-8` | Snapshot (dateless but pinned) | none published | As above. | Not sooner than 2027-05-28 | Per-platform spellings unverified outside the direct Claude API; a spelling derived from a format rule is not a verified identifier. |
| `claude-fable-5` | Snapshot (dateless but pinned) | none published | As above. | Not sooner than 2027-06-09 | Surveyed and pinnable; not proposed for any seat below. |
| `claude-haiku-4-5-20251001` | Snapshot (dated) | `claude-haiku-4-5` | As above. | Not sooner than 2026-10-15, the earliest floor in this register | On Foundry and Claude Platform on AWS the published spelling is the alias form, an independent second reason it is a poor pin. |
| `gpt-5.5-2026-04-23` | Snapshot (dated, unambiguous) | `gpt-5.5` | "Sometimes, determinism may be impacted due to necessary changes OpenAI makes to model configurations on our end. To help you keep track of these changes, we expose the `system_fingerprint` field." No weights guarantee is published either way. | No shutdown announced; at least 6 months of notice for generally available models | Usable; the provider reserves configuration change under a stable string. |
| `gpt-5.6-sol` | Snapshot today (identifier equals its only snapshot); reclassification risk | `gpt-5.6` | As above. | No shutdown announced | Whether a future dated snapshot will be published, turning today's pin into an alias, is undocumented. |
| `gpt-5.6-terra` | Snapshot today; same risk | none published; avoid the bare family name | As above. | No shutdown announced | As above. |

No Gemini spelling is fit for a governed seat under the exact-version rule, on
structural grounds rather than capability ones: the current flagship is a
preview model documented at two weeks of deprecation notice; preview identifiers
and `latest` aliases are the class Google's own changelog records as repeatedly
and silently redirected; the generally available spellings are auto-updated
aliases; the only true pinned form exists on generations already retired
2026-06-01; and no minimum notice commitment is published for retirement of a
generally available model. [22]

No capability evidence was gathered in the folded-in pass, deliberately: every
capability descriptor in the surveyed provider documentation is the vendor's own
marketing copy from its own product page and is not independent evidence. What
is screened here is pinnability and lifecycle. Capability judgment stays with
the Council on local duty-specific soak evidence, as section 2 requires. [18][19]

### Recommended Picks (recommendation, not selection)

| Seat | Recommended pick | Rejected alternatives, with reasons | Review trigger |
|---|---|---|---|
| `lead-quality` | `claude-sonnet-5` | `claude-haiku-4-5-20251001`: a valid dated snapshot, but the earliest retirement floor in the register (2026-10-15). `gpt-5.6-terra`: a cross-provider mid tier, but it carries the reclassification risk and OpenAI's configuration-change reservation. | Anthropic's 60-day retirement notice; the 2027-06-30 floor; any declared composition change; and the substantive-return degeneracy measured on the sonnet cell, which travels with any sonnet-class pin. |
| `lead-security` | `claude-opus-5` | `claude-opus-4-8`: a valid snapshot on a shorter floor (2027-05-28) with no offsetting reason on this seat. `gpt-5.5-2026-04-23`: the least ambiguous OpenAI pin, but the provider reserves configuration change under a stable identifier, which is the weakest fit on the seat that most needs stability. | As above; floor 2027-07-24. |
| `lead-integration` | `claude-opus-5` | `claude-opus-4-8`: would create a third distinct model, exceeding the ruled floor, and is a genuinely different bench rather than a precision edit, so it re-opens the soak unambiguously. `gpt-5.6-sol`: a snapshot today with documented reclassification risk. | As above; plus the soak question if the Council prefers the `claude-opus-4-8` variant. |
| `company-policy-lead` (tenant-authoritative) | The tenant's act, not this annex's. For the domain profile to mirror it without breaking the ruled 2:2, the corresponding exact spelling is `claude-sonnet-5`; recorded here as what the domain would mirror, never as a selection. | None. This annex has no standing to reject on the tenant's behalf. | As `lead-quality`; plus any tenant re-declaration. |

The last row is tenant-authoritative on ratified grounds: the tenant declares
who represents the tenant, the domain lane is a consumer bound to that
declaration and a test enforces the binding, and the promoted requirement states
that "the domain profile does not claim authority to choose the tenant
representative". [27][29]

### Diversity Options And The Named Council Question

The four options costed in the provider survey, with that survey's own
assessments as the folded-in pass quoted them (internal cross-references
trimmed, wording otherwise unchanged):

| Option | Composition | Assessment, as recorded |
|---|---|---|
| A: two-provider split, 2+2 | 2 seats on Anthropic snapshots (for example `claude-opus-5`, `claude-opus-4-8`), 2 seats on OpenAI snapshots (for example `gpt-5.5-2026-04-23`, `gpt-5.6-sol`) | "Best available. Achieves genuine cross-provider diversity with every seat on a compliant pin. Both providers publish retirement dates and notice commitments." |
| B: 3+1 | 3 Anthropic seats and 1 OpenAI seat | "Acceptable; less diversity benefit, but reduces exposure to OpenAI's weaker mutation-semantics posture." |
| C: three-provider | Anthropic, OpenAI, and Google | "Not currently constructible without violating the standing ruling." |
| D: single-provider | 4 Anthropic seats | "Compliant and operationally simplest, and Anthropic has the strongest published immutability guarantee - but forfeits the diversity objective and concentrates correlated failure." |

Correction on lifecycle evidence: Anthropic publishes retirement dates for the
surveyed snapshots; for the surveyed OpenAI snapshots only the six-month notice
commitment is published and no retirement date is announced (register rows
above; lifecycle summary in section 3). The two-provider option's "best
available" standing rests on pin compliance and independence, not on symmetric
lifecycle evidence. [9][20][21]

The recommended picks above are Option D, and its price is stated rather than
hidden: Option D forfeits cross-provider diversity, which the ratified floor does
not require. The reason given for it is that moving all four seats to Anthropic
snapshots while preserving the ruled 2:2 is the only option arguable as making
the SAME roster precise, which is the only reading under which the soak question
is even arguable; Option A and Option B are a different bench by any reading and
re-open the soak from zero. That is a price to be paid or declined knowingly,
not a bar. The folded-in pass names Option B as "the intermediate the Council
may prefer: it buys one genuinely independent provider while keeping three seats
on the strongest published pin semantics", and this annex tilts no further than
that. [19][20][21]

The Council question this annex names and does not answer: does the recorded
correlation argument, made about one model, reach a one-vendor bench, so that
two distinct models from a single vendor are the independence the floor was
buying rather than only its measurable proxy? The two providers are not
equivalent on the dimension the decision turns on, and the surveyed documents
state the tension directly: "If the council wants the strongest pin semantics,
that argues for weighting Anthropic seats; if it wants independence, that argues
for the split. These pull in opposite directions and the tradeoff should be
ruled on explicitly rather than settled by default." [20][21][27]

### Cost Baseline (screening evidence, measured under the aliases)

| Measure | Measured value |
|---|---|
| Opus judgment | mean $0.149, median $0.129, max $0.226 |
| Sonnet judgment | mean $0.097, median $0.076 |
| Per-seat ceiling | $12; the most expensive judgment used 1.9 percent of it |
| Cost per three-seat convening | $0.22 to $0.64; modelled worst case about $36 |
| Wall clock | mean 49 s (opus) and 58 s (sonnet) per judgment |
| Diverse roster | cheaper on every candidate: C0a $0.61 to $0.43, C1 $0.64 to $0.46, C2 $0.54 to $0.26 |

Every figure was measured with the mutable `opus` and `sonnet` selectors in
force. No cost, latency, or quality measurement exists for any exact snapshot
identifier named above. This is a starting expectation, not evidence about a
pinned bench. [28]

### Existing Measured Evidence The Soak Template Asks For

Section 2's recommended soak record asks for per-case results and failure
classification. Some already exist, from the 2026-08-22 seeded adversarial
corpus, and belong in front of the Council rather than being re-gathered:

- The sonnet seat returned three defect judgments and named the defect in two of
  three. The miss is a runtime degeneracy rather than a capability miss: a
  schema-valid, substantively empty return at about one in four on that cell,
  11,208 output tokens, $0.215; three re-draws of the same cell named the defect
  three of three. Its five substantive returns "are not visibly weaker than the
  opus returns on the same candidates", and "Diversity did not cost detection."
- The opus security seat named three of three defects on both rosters, and is
  the seat that parked the diversity question rather than rule on absent
  evidence.
- The opus integration seat produced the corpus's only reason-level
  disagreement: on one candidate the uniform roster's `lead-integration`
  accepted a quoted transcript as a legitimate illustration and blocked only on
  the closing directive, "a defensible narrower reading, and the only
  substantive difference of reasoning anywhere in the corpus."
- `company-policy-lead` has no corpus row at all; that corpus ran three seats
  against two rosters.

The substantive-return floor the same corpus recommends is recorded there as a
recommendation it "has no authority to impose", and it remains unruled. It
belongs beside any selection that keeps a sonnet-class model on a seat, because
the degeneracy was measured on the sonnet cell. [28]

## 3. Packet 2: Operator Exact Provider, Model, And Deployment Identity

### Ratified Minimum And Recommended S5 Template

The ratified minimum is exact model versions for a hosted holder, explicit
human-ratified issuance or re-issuance, and fail-closed drift handling. It does
not define a cross-provider identity-record grammar. The following tables are
**recommended S5 evidence templates**. They define proposed closure criteria;
they are not ratified policy.

### Identity Model

Every record separates two layers:

1. **Semantic model identity**: provider, published exact model or version ID,
   documentation source, lifecycle state, and intended model artifact.
2. **Execution or deployment identity**: tenant or account, project or
   subscription, region or location, endpoint, deployment or inference profile,
   API version, configuration, and authentication binding that route the call.

The Operator independently selects and evidences both layers after the Council
has selected the model or model family for the seat. Account, project, region,
and live availability are unknown until Operator verification. The execution
layer gates issuance and activation but does not reopen or invalidate the
Council's model-family choice. [5][9][10][11][12][13]

Within Packet 2, the Operator identifies the provider-published exact ID from
first-party documentation, selects the live account, project, region, endpoint,
deployment, or profile tuple, captures configuration read-back and execution
evidence, and signs the record. The Council may nominate a model family but may
not fill an exact-ID field. A composition attester may serialize the
Operator-approved value but does not choose or reinterpret it.

### Recommended Normalized Identity Record Template

| Field | Recommended content |
|---|---|
| Record identity | Immutable record ID, seat, Operator, decision date, and review expiry. |
| Semantic identity | Provider, exact published model or version ID, source URL or document, source access date, lifecycle status, and deprecation evidence. |
| Execution identity | Provider surface, account or tenant reference, project or subscription reference, region or location, endpoint, deployment or profile identifier, API version, and authentication binding reference. |
| Linkage | Council selection reference, proposed composition digest, and proposed issuance or grant reference. This is a reference relationship, not a claim that the execution tuple is composition-bound. |
| Ratification-time evidence | Provider documentation capture, console or API read-back of configured execution identity, lifecycle check, authorization and eligibility check, and Operator signature. |
| Execution-time evidence | Request time, documented declared and observed model fields, documented deployment or profile fields, response or job ID, available endpoint or region evidence, and substitution or failure result. |
| Limits | Exact ID is not a cryptographic digest of served behavior and does not freeze routing, safety, infrastructure, fallback, region, or output. |
| Fail-closed proposal | Missing exact ID, missing required execution field, stale lifecycle evidence, undocumented substitution, fallback, alias expansion, or mismatched evidence refuses governed issuance or activation. |

### Proposed S5 Evidence Fields By Provider

The following requirements are S5 template fields. The cited first-party
documents support provider facts and identity surfaces, not the proposed
governance template.

| Provider surface | Semantic model evidence | Execution or deployment evidence | Proposed fail-closed criterion |
|---|---|---|---|
| Direct Anthropic and Claude Code | Published exact Anthropic model/version ID, source, and lifecycle evidence. | Claude Code version, configured provider surface, credential-binding reference, endpoint if configurable, and documented observed model field. | `opus` or `sonnet` alone is insufficient. No documented recorded exact resolution, or undocumented fallback or substitution, refuses. Direct Anthropic lifecycle evidence cannot stand in for partner-hosted evidence. [9] |
| OpenAI | Published exact snapshot or exact model ID, source, and deprecation evidence. | Organization or project reference, endpoint, region if applicable, API version, deployment or routing configuration if used, and credential binding. | Unknown account, project, region, or eligibility blocks issuance and activation. Response fields do not prove complete serving immutability. [10] |
| Gemini Developer API | Published exact Gemini API model name and lifecycle evidence. | Google project, endpoint, location if applicable, API version, credential binding, and documented response model field. | Do not infer Vertex eligibility or lifecycle. Missing project or live eligibility evidence refuses issuance and activation. [11] |
| Vertex AI | Published model version and publisher model path. | Project, location, publisher, model path, API contract or version, endpoint, credential binding, and response evidence. | A model-path-looking value alone, or direct-Anthropic evidence, is insufficient. [11] |
| Claude on Vertex | Exact provider and Vertex-compatible model identity verified on the Vertex plane. | Vertex project, location, publisher, model path, API contract, endpoint, credential binding, and response evidence. | Treat as Vertex execution with separate partner lifecycle verification. Anthropic direct identity or lifecycle alone refuses. [9][11] |
| AWS Bedrock | Foundation model ID and provider-published lifecycle evidence. | AWS account, region, invocation API, inference profile, provisioned model or deployment identity where used, endpoint, and credential binding. | Semantic model and profile or deployment identity are separately required; unverified regional access refuses. [12] |
| Microsoft Foundry | Exact configured model and version, source, and retirement evidence. | Azure tenant, subscription, resource, project where applicable, region, account, deployment name, deployment configuration read-back, endpoint, API version, and credential binding. | Deployment name alone is mutable. Configured model/version and deployment must both be rechecked; mismatch or unavailable deployment refuses. [13] |

No reviewed provider documentation supplies a universal cryptographic digest for
the served model artifact. Provider response fields may strengthen execution
records but are not cryptographic attestations. [5][9][10][11][12][13]

### Provider Mutation, Lifecycle, And Platform Facts (verified 2026-08-29)

The following are verified provider facts from the folded-in research pass. They
enrich the template above and the fail-closed criteria it proposes; they are
evidence, not governance, and they amend no field of it. All were read from
first-party documentation on 2026-08-29, with no live API catalog call or test
invocation, so live resolution evidence for any identifier remains the
Operator's to produce. [19]

**Classification.** Anthropic states that it "does not update the weights or
configuration of an existing model ID" and that an updated version "ships under
a new model ID", and that from the 4.6 generation on every published model ID is
a pinned snapshot including the dateless ones. So `claude-opus-5` and
`claude-sonnet-5` are snapshots, while `opus` and `sonnet` are not identifiers in
the published catalog at all. Pre-4.6 spellings such as `claude-haiku-4-5` are
aliases resolving to the most recent dated snapshot, so the alias and the
snapshot differ only by a date suffix while the newer generation deliberately
looks like the alias form. OpenAI publishes its resolution explicitly: each
model page carries a "Current snapshot" field, and a family name such as
`gpt-5.6` routes to `gpt-5.6-sol`. The governing caution is that undated does
not mean mutable and dated does not mean immutable: a pin must be validated
against the provider's catalog, never pattern-matched. [9][20][21]

**Mutation reservation.** OpenAI publishes the opposite of Anthropic's
guarantee: "Sometimes, determinism may be impacted due to necessary changes
OpenAI makes to model configurations on our end. To help you keep track of these
changes, we expose the `system_fingerprint` field." Whether OpenAI weights, as
distinct from model configuration, can change under a fixed dated snapshot is
undocumented in either direction. Google states only that stable models "usually
don't change", which is neither a promise nor a warning. And at every provider a
pin binds weights rather than behavior: serving infrastructure, including the
request router, safety classifiers, and sampling logic, "can change over time",
and infrastructure updates can "produce minor differences in observable behavior
even when the model ID and weights have not changed". A council that needs
reproducible verdicts cannot obtain that from a model pin alone at any provider.
[9][21][22]

**Lifecycle floors.** Published earliest-retirement dates for the surveyed
Anthropic snapshots are 2027-07-24 (`claude-opus-5`), 2027-06-30
(`claude-sonnet-5`), 2027-06-09 (`claude-fable-5`), 2027-05-28
(`claude-opus-4-8`), and 2026-10-15 (`claude-haiku-4-5-20251001`), with at least
60 days of notice and a hard failure after the date. OpenAI commits to at least
six months of notice for generally available models and announces no shutdown
for the surveyed snapshots. Google publishes no minimum notice commitment for
retirement of a generally available model; a six-month figure circulating
through third-party coverage was not found on any Google property and must not
be relied on. [9][21][22]

**Platform hazards.** These are execution-identity facts, and they belong in the
Packet 2 record for whichever plane the Operator selects.

- Microsoft Foundry and Azure OpenAI. Selecting a specific model version does
  not pin it. The published rule is that a null version update policy "is
  equivalent to `OnceCurrentVersionExpired`", which upgrades the deployment when
  the version retires; only an explicit `NoAutoUpgrade` refuses, and it refuses
  hard, so that the deployment "stops working" and "All inference requests
  return `410 Gone`". A record asserting a pinned version on this plane without
  asserting `versionUpgradeOption` records something the platform does not do.
  Inference responses can return the family name rather than the serving
  version, so the bound version is a management-plane read
  (`properties.model.version`), a separate call from inference. Partner models
  on Foundry, Anthropic's included, follow a 12-month lifecycle rather than the
  standard 18-month one, and retirement extensions are refused. [23]
- AWS Bedrock. Fail-closed by design and by default, needing no additional
  configuration; regional inference profiles change region only, with the dated
  model ID embedded unchanged. Bedrock publishes its OWN lifecycle dates, which
  differ from the model provider's: "Model lifecycle dates on this page are
  specific to Amazon Bedrock and may differ from dates published by model
  providers (such as Anthropic or Cohere). For Amazon Bedrock usage, only the
  dates on this page apply." Anthropic states the same in the other direction,
  that partner-operated platforms set their own retirement schedules. A Bedrock
  record must therefore carry Bedrock's dates, never the direct-provider ones.
  [24][9]
- Google Vertex AI. The routing layer is safe but the alias layer moves, and
  this is the weakest evidence base in the survey: the relevant documentation
  pages render client-side and would not yield body text across roughly eight
  fetch attempts, so those rows are provisional and must be re-verified against
  the live API before any Vertex-hosted seat is approved. Always pin the fully
  dated snapshot form. [22]
- Direct Anthropic. The plane is safe by default, with one exception that must
  be asserted rather than assumed: the opt-in server-side `fallbacks` parameter
  described in section 1. [20]

**The pin is a pair.** The same immutable model does not carry the same string
across planes, so a governance pin records the plane and the exact identifier
together, never the identifier alone. Per-platform spellings for
`claude-opus-4-8` are unverified outside the direct Claude API, and for
`claude-haiku-4-5-20251001` the published Foundry and Claude-Platform-on-AWS
spellings are the alias form. A spelling derived from a format rule is not a
verified identifier and must not be recorded as one. [20][23][24]

## 4. Packet 3: Convener Admissible-Pin Ruling

### Ruling Of Record (2026-08-28)

No Convener decision is pending on this packet. The question, whether a family
pin carrying an attested resolved-version record is admissible, was ruled on
2026-08-28, and the change that carried it records the ruling twice, verbatim
and identically, in its proposal and in its design:

> Resolved 2026-08-28 by ratification as proposed: the delta's exact-version
> rule stands - a declared model component names an exact version, and a family
> pin is a validation failure. Admitting a family pin would now be a new change.

The ratified requirement text goes further than Q8(d). Q8(d) forbids the family
pin; the ratified scenario additionally refuses the attested-resolution
workaround by name:

> Scenario: a model family is not a pin
>
> - WHEN a declared model component names a family or an alias rather than an
>   exact version
> - THEN the declaration is a validation failure
> - AND no resolution of that family at declaration time is accepted in place of
>   the exact version

That change carries `Status: ratified` (2026-08-28, Brett Heap, operator
authority) and its ratification commit (`f3f72c6`) is on openXwallet `main`,
observed at `2d66850`.
Its own tasks ledger still shows the ratify and rule-the-carried-question boxes
unticked; that is stale bookkeeping against a ratified record, not a pending
decision. The box beside them, the shape of the re-issuance act, is genuinely
unruled and belongs to Packet 4 rather than here. [26]

Reopening is therefore a new-change act, not an open ruling. Exactly two escape
hatches are recorded: "Family pinning may be revisited only through a future
core delta that can police it", and "Admitting a family pin would now be a new
change." The Options table and the completeness checklist below are retained as
the constructibility bar such a new change would have to clear. The ruling
closed the question; recording it here does not reopen it. The authoritative
task ledger records the same outcome as a dated addendum under task 8.1
(tasks.md), so the ledger and this report no longer state different Packet 3
postures. [1][2][26]

### Options

| Option | Standing | Required controls | Decision effect |
|---|---|---|---|
| Exact published version only | Governing default under Q8(d). | Published exact version ID, Operator Packet 2 evidence, explicit human-ratified re-issuance after composition change, and fail-closed drift. | No Q8(d) relaxation. An alias roll is a new composition state, not continuity. |
| Attested alias resolution | Future policy alternative only. | A ratified contract delta defining signer, signed binding tuple, freshness, resolution method, lifecycle, revocation, drift, fallback and substitution behavior, and failure windows. | Not admissible unless the Convener rules it and the explicit contract delta is ratified and implemented. |

This report does not recommend the second option. Exact published version only
remains the governing default. [1][2]

### Future Attested-Alias Completeness Checklist

This is a future-policy checklist, not adopted design.

| Control | Required future policy content |
|---|---|
| Signer | Accountable issuer, credential and trust chain, key rotation and revocation rules, and proof of authority to attest provider resolution. |
| Binding tuple | Alias, resolved exact provider ID, provider plane, account or project, region, endpoint, deployment or profile, API version, composition hash, issued time, expiry, and attestation ID. |
| Freshness | Maximum age, clock basis, re-attestation trigger, and refusal for missing, expired, unreadable, or stale records. |
| Resolution | Documented provider resolution method, evidence capture, and prohibition on inference from display name or a prior run. |
| Fallback and substitution | Explicitly named permitted behavior, if any. Undocumented fallback, substitution, migration, alias roll, or cross-region routing refuses. |
| Lifecycle | Provider retirement, account or project loss, deployment edit, region withdrawal, and credential rotation trigger re-evaluation under a named owner. |
| Drift and revocation | Any binding-tuple difference is DRIFT, revokes the affected grant and descendants, and requires new human-ratified issuance. |
| Failure window | Define the provider-change-to-detection interval. If valid evidence does not cover it, governed exercise refuses. |

An alias attestation would attest a stated resolution record, not every provider
routing, safety, infrastructure, or output property. The Convener must decide
whether that narrower claim is adequate before a core delta is ratified.
[6][9][10][11][12][13]

### Provider-Side Attestation Evidence (verified 2026-08-29)

The ruling above stands on its own record. The provider evidence gathered
independently on 2026-08-29 closes the same question on the merits for today,
and is recorded so that any future new change starts from it rather than
re-gathering it. [19]

No first-party provider surveyed, Anthropic, OpenAI, or Google, offers any
cryptographic attestation binding a specific inference response to a specific
model version in a third-party-verifiable way as of 2026-08-29. Every version
echo is asserted metadata: Anthropic's `model` field, OpenAI's
`system_fingerprint` (Chat Completions only) alongside `model`, and Google's
`modelVersion` and `responseId`. None is signed. Anthropic's strongest claim is
documentation-level rather than cryptographic, and `system_fingerprint` is a
change-detection signal rather than an identity proof. On that evidence an
attested alias resolution is not currently constructible. [20][21][22]

Cryptographic attestation exists only at the hardware and trusted-execution
layer, and it binds the code image, firmware, or environment, explicitly not the
model weights. The cleanest demonstration is a published GPU attestation claim
set: hardware model, driver and VBIOS versions, reference-measurement
availability, secure-boot and debug status, and report-signature verification.
Every claim is about the chip and its firmware, and none identifies the running
workload, process, or model. A signed claim set of that shape structurally
cannot carry model identity. [25]

Two adjacent capabilities must not be mistaken for it. Webhook signing at both
OpenAI and Anthropic authenticates transport origin and says nothing about which
model weights produced any inference content. Azure's model-provenance language
describes a platform capability for scenarios a customer builds, not a statement
that a live inference response carries a signed model-weight claim. [20][21][23]

One claim is named here so that it cannot re-enter the record as research: a
social-media post asserting that Anthropic had shipped cryptographic model
fingerprinting tying each output to API key, model version, and timestamp. It
has no corroboration on any Anthropic property and is explicitly not a finding.
[19]

Read against the checklist above, this means the signer and binding-tuple rows
are not constructible today; the freshness row is the very fail-open window the
ratifying change weighed and declined; and no ratified vocabulary exists for an
attested model-version resolution, as distinct from the attested composition
HASH the schema already defines. [7][19][26]

## 5. Packet 4: Six-Component Canonical Composition And Re-Issuance

### Ratified Profile Reference And Current Holder Mapping

The agent-profile specification ratifies the six components and requires a
declared component set. Its schema permits both `content` and `reference`
binding modes for every component. The descriptive profile text presents
`content` as the expected mapping for model version, prompt contract, tool
manifest, policy version, and parameters, and `reference` for retrieval corpus.
At codexFactory `origin/main` commit
`0c7b69ae9695fca371b92294bc327249d7bb3c46`, the current
`agent:merge-readiness-council` holder states exactly those six bindings in
`council.composition_source_map` and links them to the holder profile. The map
is therefore verified current repository state. Its model-version source still
contains mutable aliases, so the map does not satisfy Q8(d). [4][6][7][8]

| Component | Current holder source mapping | Proposed canonical value domain | Drift effect |
|---|---|---|---|
| Model version | `content` from `review_council_profiles.merge_readiness_council.model_assignments`; currently mutable `opus` and `sonnet` aliases. | Provider plane and exact published provider model/version identity only. | Any value change invalidates. |
| Prompt contract | `content` from `review_council_profiles.merge_readiness_council.prompt_contract`; current profile records rendered-set and per-seat digests. | Prompt source identity, rendered or declared prompt digest, and version. | Any value change invalidates. |
| Tool manifest | `content` from `review_council_profiles.merge_readiness_council.tool_manifest`. | Tool names, versions, permissions, invocation policy, and manifest digest. | Any value change invalidates. |
| Policy version | `content` from `council.policy_version`. | Policy identity, version, and policy content digest. | Any value change invalidates. |
| Parameters | `content` from `review_council_profiles.merge_readiness_council.parameters`. | Declared generation and execution parameters with explicit defaults and types. | Any value change invalidates. |
| Retrieval corpus | `reference` from `review_council_profiles.merge_readiness_council.retrieval_corpus`; current profile excludes candidate HEAD and pins the ontology package digest. | Corpus identity and governing configuration digest covering scope, selection configuration, and admission policy. | Corpus identity or governing configuration change invalidates. Row-level content changes in the same governed corpus do not by themselves invalidate. |

Packet 2 deployment fields remain outside `model_version` composition by default.
Binding region, deployment, profile, endpoint, or authentication identity into
composition would be a separate, unratified policy choice with a larger DRIFT
blast radius. A signed composition envelope may reference the Packet 2 evidence
record instead. [1][6][7]

### Current Holder Record And Remaining Gap

The canonical codexFactory `origin/main` at
`0c7b69ae9695fca371b92294bc327249d7bb3c46` identifies the holder and its
six-component source map across
`hermes/domain/review-councils/merge-readiness.yaml` and
`hermes/domain/agent-mixes.yaml`. The latter records the prompt digests, tool
manifest, parameters, retrieval binding, ontology digest, candidate-HEAD
exclusion, and seat model assignments. This corroborates the task ledger's
section 4.4 claim that the composition source map was realized. [2][4][8]

A detached sibling checkout at
`ceb04f2f3ffecf8307bff13b6f29b2a16363da93` predates that declaration and is
not evidence of canonical current state. The remaining holder-specific defect
is narrower: `model_version` points to mutable `opus` and `sonnet` aliases, and
no ratified canonical six-component serialization, composition digest, or
signed attestation envelope closes the later stages proposed below.

Two objects must not be conflated here, and both findings are verified. The
HOLDER-side source map EXISTS: at codexFactory
`0c7b69ae9695fca371b92294bc327249d7bb3c46`,
`hermes/domain/review-councils/merge-readiness.yaml` lines 26-48 carry the
six-component `composition_source_map`, with a binding mode and a source for
each component. The WALLET-side composition record DOES NOT: in openxFactory,
`governance/review-authority/register.yaml` row `row-mrc-0001` (lines 62-70)
carries the nine authority-row fields only, `row_id`, `holder_ref`,
`wallet_ref`, `target_repo`, `act`, `authority_tier`, `grant_ref`, `expires_at`,
and `state`, with no composition record and no `declared_hash`; the whole
`governance/review-authority/` directory contains four files and zero
occurrences of the string "composition". A source map naming where each
component's value lives is not a declared component set with digests, and the
distance between the two is precisely Packet 4's subject. [8][19][32]

Three further gap facts, verified in the folded-in pass, sharpen what remains:

1. Nothing verifies that `declared_hash` is correct. The neutral validator
   touches the field at exactly two places, neither a verification: a hash
   without a component set is an error, and an attested hash differing from the
   declared hash must carry `grants_state: revoked_on_composition_change`. This
   change's own proposal states it in as many words: "The hash is over a
   DECLARED set; `check_agent_composition` never checks that a digest is correct
   and cannot check that the set is complete." The same validator dispatches
   that check only when a composition record is present, so its absence is
   currently unrefused. [30][31]
2. Five of the six components carry no content digest today. Only
   `prompt_contract` does, through the rendered-set digest pinned 2026-08-27.
   `model_version`, `tool_manifest`, `policy_version`, and `parameters` are
   declared as SOURCES rather than digests, and the archived declaration design
   says so: "`content` means that S5 will content-bind the resolved value, not
   that task 4.4 authors a digest." [4][29]
3. The re-issuance ruling box carried beside the 2026-08-28 ruling is unticked
   and has no ruling text anywhere. Unlike the two stale bookkeeping boxes
   described in section 4, it is genuinely unruled, and it belongs to this
   packet. [26]

### Proposed Canonicalization And Attestation Design

This is a proposal for ratification, not a final standard. Every unresolved
choice below must be ratified before implementation or activation.

1. **Value-domain normalization.** Convert each component to typed values before
   serialization. Require explicit null handling, explicit defaults, canonical
   provider and component identifiers, lowercase digest hex, RFC 3339 UTC times
   where time is permitted, and no implicit environment-derived values.
   Unresolved: parameter vocabulary, defaulting rules, and exact provider
   identity grammar.

   *Residual question narrowed from the parallel document (D5).* The folded-in
   pass raised the full tuple, plane, exact identifier, effort and reasoning
   settings, thinking configuration, tool set, prompt bytes, and API version
   header, as an open ratification question about what `model_version` digests.
   Against the decomposition above it narrows to a single residual: whether the
   provider PLANE sits inside `model_version`'s digest, since the per-provider
   evidence table in section 3 already treats semantic identity as
   plane-scoped. Execution and deployment identity stays outside composition by
   this report's default and is carried by reference to the Packet 2 evidence
   record; effort, reasoning, and thinking settings are generation parameters
   and belong under the Parameters component. The narrowed question is
   unresolved and is Packet 4 ratification work. [19]
2. **Canonical serialization.** Serialize one object containing
   `schema_version`, holder reference, ordered component set, binding mode,
   normalized value, and declared coverage. Require UTF-8, a fixed profile,
   lexicographic component order, deterministic object-key order, fixed number
   representation, no insignificant whitespace, and a specified escaping rule.
   Unresolved: JSON Canonicalization Scheme, canonical CBOR, or another named
   profile; decimal form; and duplicate-key rejection.
3. **Digest.** Calculate `sha256` over canonical bytes and encode as
   `sha256:<lowercase-hex>`. Record algorithm and profile version. The digest
   asserts equality of the defined composition only; it does not attest provider
   serving behavior. Unresolved: digest agility and dual-digest transition.
4. **Signed attestation envelope.** Sign a separate envelope containing the
   composition digest, canonicalization profile, holder and grant references,
   issuer identity, issue and expiry times, Packet 2 evidence-record reference,
   and revocation status. Unresolved: envelope standard, signer class, key
   distribution, signature algorithm, and evidence-retention location.
5. **Provider execution evidence.** Reference Packet 2 execution-time evidence.
   It is provider-reported evidence, not cryptographic provider attestation, and
   cannot substitute for the signed composition envelope.

### Lifecycle Roles

`propose -> approve -> attest -> register -> activate -> revoke`

| Transition | Decision owner | Evidence producer | Enforcer | Minimum evidence and failure behavior |
|---|---|---|---|---|
| Propose | Council or authorized proposer | Proposer | None | Candidate, seat duty, Packet 1 draft, Packet 2 draft, and proposed six-component values. Proposal has no authority. |
| Approve | Gate-Rules Council for seat choice; Convener for a pin-policy change; human ratifier for issuance semantics. | Council, Convener, or proposer as applicable | None | Signed decision record, completed soak evidence, and resolved required policy choices. A missing decision blocks the next transition. |
| Attest | No ratification occurs here. | Operator supplies Packet 2 facts; designated composition attester supplies canonical bytes, digest, and signed composition attestation. | Runtime or core later verifies matching evidence. | Missing, invalid, stale, or unverifiable evidence refuses. |
| Register | Human ratifier only. | Operator and designated composition attester provide evidence; register writer records the ratified act. | Register reader and runtime or core enforce only matching active state. | Only an explicit human-ratified register act may issue or re-issue. No automatic or standing re-issue. |
| Activate | No new decision. | Operator and attester evidence referenced by the ratified record. | Runtime or core checks matching, freshness, and active state. | Mismatch or unreadable state refuses activation. |
| Revoke | No new ratification. Human ratification is needed only for later re-issuance. | Runtime or core records DRIFT or CAUSE evidence and affected-chain evidence. | Runtime or core cascades and refuses stale authority. | Derived grants revoke with the parent; no stale authority survives. |

### In-Flight Behavior And Re-Issuance

The ratified minimum is that an exercise detecting a composition mismatch
refuses rather than honors an earlier admission stamp, and that issuance or
re-issuance requires an explicit human-ratified register act. The final treatment
of content provenance at verdict consumption remains an open runtime ruling.
[1][2]

The S5 implementer proposed a richer re-issuance grammar: superseding and
superseded grant references, composition hash, ratifying human, and effective
time. Those fields are proposed for ratification; they are not the ratified
minimum and must not be described as an already-required record format. [2]

Two sequencing constraints are recorded in the S5 ledger and bound whatever
follows. The first is a one-act constraint, verbatim from task 7.6:

> STAYS OPEN, and it is now the load-bearing operator item of S5. 7.5's model
> half is blocked ON it: the seat model is a Gate-Rules Council decision
> (`council-deliberation-worker.yml:710-723`, ruled 2026-08-22 - "this lane
> will not choose one"), so the alias-to-exact-version flip IS the deliberate
> composition bump this runbook is supposed to be walked against. The runbook
> and that flip are one act, not two.

The second is the ordering the same ledger forces. The Council rules the
seat-to-model roster first, because which model represents a seat is a
Gate-Rules Council matter and the deliberation lane declines the choice in its
own text. The Operator then records the exact published version and the
execution identity, which depends entirely on the Council's output: the choice
between two candidates from different providers is the roster choice, not a
version choice. The flip and the runbook walk land last, as the single act
quoted above. `company-policy-lead` runs in a parallel tenant lane, because the
tenant declares its own representative and that declaration must land before or
with the domain mirror. Recording this order neither performs a step in it nor
schedules one. [2][14][27]

## 6. Contradictions And Counter-Evidence

| Observation | Consequence | Disposition |
|---|---|---|
| Current roster is model-diverse in intent but uses mutable aliases. | Diversity intent does not meet exact-version identity. | Council selection remains independent and unresolved; Operator evidence is separately required before issuance or activation. [2][3][4] |
| Exact provider IDs exist, but no reviewed provider supplies a universal cryptographic serving digest. | Exact ID cannot mean complete serving immutability. | Limit claim to artifact targeting and pair it with Packet 2 execution evidence. [5][9][10][11][12][13] |
| A Foundry deployment name can remain while model configuration changes. | Deployment name cannot be the model pin alone. | Bind configured model/version and deployment read-back in Packet 2. [13] |
| Direct Anthropic and partner-hosted surfaces can share model names. | Lifecycle and execution identity cannot be inherited across planes. | Require separate direct, Vertex, Bedrock, or Foundry evidence. [9][11][12][13] |
| Agent-profile authority defines components and binding modes but not canonical serialization. | A hash can be structurally required while byte semantics are undefined. | Ratify proposed serialization or keep activation fail-closed. [6][7] |
| Canonical codexFactory state declares a six-component holder source map, but its `model_version` source resolves to mutable aliases and no ratified canonical serialization exists. | Source mapping is verified, while Q8(d) identity and deterministic composition bytes remain unresolved. | Operator supplies exact-ID evidence; human authority ratifies serialization and attestation semantics before activation. [2][4][8] |
| The S5 ledger header states four pull requests, NONE MERGED, but codexFactory #123's commit `61a6811085d69b4db2480dcb2368172fdf9f0e86` is on codexFactory `main` and is an ancestor of the canonical `0c7b69ae` this report pins. | A reader inheriting the header mis-scopes the prompt-contract half of task 7.5, which is landed repository state. | Verify pull-request state directly rather than from the ledger. This report's holder-map findings already rest on a commit that contains it, so no finding above changes. [2][4][19] |
| openXwallet #3 carries `Status: ratified` (2026-08-28) and its ratification commit is on that repository's `main`, while its own tasks ledger still shows boxes 2.1 and 2.2 unticked. | Ledger state and ratification state disagree about a change this report cites as governing. | Stale bookkeeping, not a pending decision, and marked [INFERENCE] in the folded-in evidence, which found no ruling text for box 2.3 and treats only that box as genuinely open. [19][26] |

## 7. Unresolved Decisions Matrix

| Unresolved fact or decision | Owner | Closure evidence | Blocking effect |
|---|---|---|---|
| Seat model or model-family selection | Gate-Rules Council | Signed selection record, duty-specific soak pass, rejected alternatives, diversity analysis, and recorded Council-convener disposition. | Blocks an accepted selection from existing when unresolved; does not itself issue or activate a grant. |
| Application of an accepted selection to the enrolled roster | Designated roster-change Lead | `lead_accepted_recorded` evidence, the reviewed roster change, and fresh soak evidence for the applied roster. | Blocks live roster application; does not substitute for human-ratified issuance. |
| Exact published version and live execution identity | Operator | Packet 2 record with provider documentation, lifecycle, console or API read-back, authorization or eligibility evidence, and execution evidence. | Blocks governed issuance and activation, not the Council's model-family selection. |
| Exact execution identity for the current Claude Code alias invocation | Operator | Documented exact resolution or replacement configuration, recorded evidence, and no undocumented substitution. | Blocks use of `opus` or `sonnet` for a governed holder. |
| Admissibility of attested alias resolution | Convener (RULED 2026-08-28) | Ruling of record cited in section 4; reopening requires a new change. | None pending. Exact published version only is mandatory. |
| Exact-version replacement for the current holder's alias-valued model source | Operator | Packet 2 exact-ID record plus a codexFactory holder-profile update referencing the Council selection and stable repository revision. | Blocks Q8(d)-conformant issuance and activation; the six-component source map itself is already identified. |
| Canonical serialization profile and value-domain rules | Human ratification authority | Ratified grammar for normalization, ordering, encoding, duplicate handling, digest, and examples. | Blocks trusted composition digest comparison and activation. |
| Attestation envelope and signer trust model | Human ratification authority and Operator | Ratified envelope, signer authorization, key and revocation model, and evidence-retention location. | Blocks signed composition attestation. |
| Re-issuance runbook walk | Operator with human ratifier | Recorded deliberate composition bump, cascade, new human-ratified register act, and parked or refused old authority. | Blocks S5 completion and normal recovery from a provider roll. |
| In-flight content-provenance treatment | Hermes runtime ruling owner | Explicit ruling and implementation evidence after ratification. | Limits the runtime revalidation claim; does not relax drift refusal. |

## 7A. Fact-Level Unresolved Annex

The matrix above is decision-level. This annex is fact-level: the register
carried by the folded-in research pass, deduplicated against that matrix, with
each item's resolution route preserved. Nothing here is a decision, and no item
blocks anything the matrix does not already block. Two of the source register's
items are not carried, because section 7 already holds them at decision level:
whether council-content provenance is re-derived at verdict consumption (the
in-flight row), and the Operator's live resolution evidence for a chosen version
(the exact-version row). [19]

### Repository-Side

| Item | Unresolved fact | Resolution route |
|---|---|---|
| R1 | Whether an alias-to-exact-version flip re-opens the soak. The soak-gate clause reads as covering a value edit, while the S5 framing treats the flip as making the same roster precise; no text disposes of the collision, and the two further leads in section 2A do not settle it. | The Council, ruled explicitly in the Packet 1 act rather than by default. |
| R2 | The shape of the re-issuance act is unruled: no ruling text exists anywhere, and the proposed recorded fields are the implementer's. | Convener ruling; Packet 4. |
| R3 | Nothing verifies that `declared_hash` is correct, and nothing requires the record to exist. Section 7 carries the serialization profile; the verification point is a separate gap. | A future change; Packet 4, alongside the serialization ruling. |
| R4 | No live composition record exists for the live agent wallet, and no validator rule refuses its absence. | A future change; Packet 4. |
| R5 | `propose`, `approve`, and `activate` have no wallet-family definition; the nearest surfaces are a posture field and a different object's gate state. | A future change; Packet 4. |
| R7 | The retrieval corpus has no `governing_configuration_digest`; the live declaration uses domain-shaped keys rather than the neutral reference shape. | A future change; Packet 4. |
| R8 | The Gate-Rules Council's own seats carry no declared models, recorded as inherited, and its bench has been hand-assembled at each convening. | Operational, for the Council or the operator; not blocking. |
| R9 | `company-policy-lead` has no measured bench evidence. | A future corpus run. |
| R10 | The substantive-return floor recommended by the seeded corpus is recorded there as a recommendation it has no authority to impose, and is unruled. | The Gate-Rules Council or the operator, beside Packet 1. |
| R11 | No repository text states that the earlier exact-ID implementation is non-authority; the repositories treat it as realization evidence. | Handoff-only; a future change if it matters. |
| R12 | openXwallet's tasks ledger is stale against its own ratification record. | Bookkeeping, by that change's owner. |
| R13 | The S5 ledger's four-pull-requests-NONE-MERGED header is stale. | Bookkeeping; verify pull-request state directly. |
| R14 | RESOLVED. Which transport the council-deliberation worker calls was undetermined in the folded-in pass; this report's workflow evidence resolves it, since the workflow passes `SEAT_MODELS` aliases to Claude Code. The configured provider surface underneath remains a Packet 2 execution-identity field. | Resolved by [3] for the transport; the plane is Operator evidence. |

### Provider-Side

| Item | Unresolved fact | Resolution route |
|---|---|---|
| P1 | Whether Anthropic's response `model` field echoes the alias or the resolved snapshot when a pre-4.6 alias is sent. Material: it determines whether a response can detect alias drift at all. | Operator test call. |
| P2 | Confirmation that no seed-equivalent exists on any Anthropic endpoint; absence is not conclusively provable by search. | Operator test call or provider ticket. |
| P3 | Whether OpenAI weights, as distinct from model configuration, can change under a fixed dated snapshot. No policy statement was found either way. | Provider ticket. Material: it is the central OpenAI mutation-semantics question. |
| P4 | Whether the Responses API exposes `system_fingerprint` at all; it is confirmed only on Chat Completions and legacy Completions. | Operator test call. |
| P5 | Whether OpenAI's response `model` field returns the resolved snapshot or the alias as sent; not confirmed from a primary source. | Operator test call. |
| P6 | Whether `seed` is accepted on the GPT-5.6 family via the Responses API, given that reasoning models are documented as unsupported. | Operator test call. |
| P7 | The exact HTTP status and error for a retired versus a never-existing OpenAI model identifier. | Operator test call. |
| P8 | Whether a future dated `gpt-5.6-sol` snapshot will be published, retroactively reclassifying today's pin as an alias. Not documented. | Provider ticket and time; bears on any `gpt-5.6` pin. |
| P9 | Whether a pinned Gemini version's weights, quantization, or serving stack can change under a fixed identifier. | Provider ticket; Google is silent in both directions. |
| P10 | Any primary-source Google minimum-notice commitment for retirement of a generally available model. | Provider ticket; the circulating third-party figure must not be relied on. |
| P11 | Whether a pinned identifier resolves to an identical serving artifact on the Gemini API and on Vertex AI. | Provider ticket. |
| P12 | Verbatim Google text for the seed description and the temperature-zero non-guarantee; search-index confidence only. | Re-fetch or provider ticket. |
| P13 | Verbatim primary source for sampling parameters being deprecated and ignored, rather than rejected, on the newest Flash models. | Re-fetch. |
| P14 | Vertex's verbatim preview and experimental category definitions; the page did not render. | Re-fetch via a live API client. |
| P15 | Whether Gemini is available on any non-Google platform; negative evidence only. | Open. |
| P16 | Vertex's verbatim lifecycle and partner-model retirement text; the pages render client-side and would not yield body text across roughly eight fetch attempts. | Re-verify against the live API before any Vertex-hosted seat is approved. |
| P17 | Whether Azure's Responses API and Chat Completions differ in returning deployment name versus canonical model name. | Operator test call. |
| P18 | Any customer-facing Bedrock or Vertex feature that cryptographically attests which model version served a request, as opposed to infrastructure identity. None was found. | Open; bears on the section 4 checklist. |
| P19 | Verbatim scope language from the providers' trust portals for their SOC 2 and ISO reports. | Re-fetch. |
| P20 | Primary-source description of Private AI Compute's attestation claims; search summary only. | Re-fetch. |
| P21 | Google's verbatim `modelVersion` field description on the Vertex response reference; existence confirmed, field-level prose did not render. | Re-fetch. |
| P22 | Per-platform spellings for `claude-opus-4-8`. Format rules exist, but a spelling derived from a format rule is not a verified identifier. | Operator test call, before any pin on that model. |

Two items are recorded as rejected rather than unresolved, so that they cannot
re-enter as research: the social-media model-fingerprinting claim named in
section 4, and the six-month Google retirement-notice figure named above. [19]

## 8. Research Method And Evidence Quality

This snapshot uses the Q8 ruling and S5 task ledger as local governing sources,
the openXwallet agent-profile specification and schema for existing composition
semantics, and current codexFactory declarations for the present Council path.
The Wave 2 journal is **supporting, reconciled research evidence**, not
authoritative governance. It records the 2026-08-29 provider-documentation
review. [1][2][3][4][5][9][10][11][12][13]

Evidence is tiered. Local rulings establish governance. Live repository files
establish current repository facts. First-party provider documents establish
published identity and lifecycle surfaces. None proves live tenant availability.
Benchmark and literature results are screening evidence only; local,
duty-specific soak tests remain necessary for Council selection. [18]

Sibling-workspace paths and `.omo` paths are point-in-time workspace evidence.
The codexFactory holder-map findings are fixed to canonical `origin/main` commit
`0c7b69ae9695fca371b92294bc327249d7bb3c46`; any later ratification must capture
stable revisions for every other relied-on repository record.

The claim graph, observation manifest, and expansion log describe research
coverage and retained gaps; they do not ratify decisions. [5][15][16][17]

This report was amended on 2026-08-29 to fold in a second research pass, run
independently and fidelity-reviewed before folding. That pass rested on two
verified inputs: a repository-side extraction across openxFactory, codexFactory,
and openXwallet at recorded HEADs (`3ffd6a8f`, `0c7b69a`, `2d66850`), and a
first-party provider documentation survey covering Anthropic, OpenAI, Google,
Microsoft, Amazon Web Services, NVIDIA, and Apple, all accessed 2026-08-29. Like
the Wave 2 journal, it is **supporting research evidence, not authoritative
governance**. Its limits carry with it: it gathered no benchmark evidence by
design, and it made no live API catalog call or test invocation, so its provider
facts are documentation-catalog evidence as of the access date and live
resolution evidence remains the Operator's to produce. Where its two inputs
required reasoning across them, or where the repository extraction had itself
marked a conclusion an inference, the folded material carries that marking.
Model identifiers are reproduced exactly as the surveyed documentation spells
them, never normalized or reconstructed. Quoted text throughout this report is
reproduced with non-ASCII characters transliterated (em dash as " - ", the
section sign dropped); no word is changed. [19]

## 9. Evidence And Sources

1. Brett Heap, **Operator Rulings - Q8, Q9, Q10 (section 8), recorded 2026-08-26**,
   `openspec/changes/add-wallet-carried-review-authority/rulings-2026-08-26.md`,
   section "Q8 - composition drift for hosted-model holders: FAIL-CLOSED BUNDLE".
2. **Tasks: add-wallet-carried-review-authority**,
   `openspec/changes/add-wallet-carried-review-authority/tasks.md`, sections 4.4,
   7, 7.5-7.7, and 8.1.
3. **Council-deliberation worker**,
   `xFactories/codexFactory/.github/workflows/council-deliberation-worker.yml`
   at codexFactory `0c7b69ae9695fca371b92294bc327249d7bb3c46`, comments and
   `SEAT_MODELS` in the "Run the three seats" step.
4. **Hermes domain agent mixes**,
   `xFactories/codexFactory/hermes/domain/agent-mixes.yaml` at codexFactory
   `0c7b69ae9695fca371b92294bc327249d7bb3c46`, especially
   `review_council_profiles.merge_readiness_council`, `guardrails`, and
   `failure_semantics`.
5. **Wave 2 - Provider and Model Evidence Reconciliation**,
   `.omo/ulw-research/20260829-033311/wave-2-provider-model-evidence.md`,
   sections 1-9. Supporting reconciled research evidence, not governance.
6. **openxwallet-agent-profile Specification**,
   `openXwallet/openspec/specs/openxwallet-agent-profile/spec.md`, requirements
   "An agent holder declares its composition" and "A composition change revokes
   the agent's grants immediately".
7. **openxWallet agent composition declaration schema**,
   `openXwallet/contracts/openxwallet-agent-profile/openxwallet-agent-composition.schema.yaml`,
   description, `component_set`, `binding_mode`, and `attestation`.
8. **Council declarations**,
   `xFactories/codexFactory/hermes/domain/review-councils/merge-readiness.yaml`
   and `xFactories/codexFactory/hermes/domain/review-councils/gate-rules.yaml`
   at codexFactory `0c7b69ae9695fca371b92294bc327249d7bb3c46`, especially
   `council.composition_source_map`, `members`, `conditional_members`, and
   `failure_semantics.output_disposition`.
9. Anthropic, **Claude Code model configuration**
   (`https://code.claude.com/docs/en/model-config`), **Model IDs and versions**
   (`https://platform.claude.com/docs/en/about-claude/models/model-ids-and-versions`),
   and **Model deprecations**
   (`https://docs.anthropic.com/en/docs/about-claude/model-deprecations`).
10. OpenAI, **Models** (`https://platform.openai.com/docs/models`),
    **Deprecations** (`https://platform.openai.com/docs/deprecations`), and
    **Responses API** (`https://platform.openai.com/docs/api-reference/responses`).
11. Google, **Gemini API models** (`https://ai.google.dev/gemini-api/docs/models`),
    **Vertex AI model versions**
    (`https://cloud.google.com/vertex-ai/generative-ai/docs/learn/model-versions`),
    and **Vertex AI REST reference**
    (`https://cloud.google.com/vertex-ai/generative-ai/docs/reference/rest`).
12. Amazon Web Services, **GetFoundationModel API**
    (`https://docs.aws.amazon.com/bedrock/latest/APIReference/API_GetFoundationModel.html`),
    **Inference profiles**
    (`https://docs.aws.amazon.com/bedrock/latest/userguide/inference-profiles.html`),
    and **Model invocation**
    (`https://docs.aws.amazon.com/bedrock/latest/userguide/model-parameters.html`).
13. Microsoft, **Working with models in Microsoft Foundry**
    (`https://learn.microsoft.com/en-us/azure/foundry/openai/how-to/working-with-models`),
    **Model lifecycle and retirements**
    (`https://learn.microsoft.com/en-us/azure/foundry/openai/concepts/model-retirements`),
    and **Microsoft.CognitiveServices/accounts/deployments ARM schema**
    (`https://learn.microsoft.com/en-us/azure/templates/microsoft.cognitiveservices/accounts/deployments`).
14. **Tasks: add-wallet-carried-review-authority**,
    `openspec/changes/add-wallet-carried-review-authority/tasks.md`, section 7.5.
15. **Claim Graph**, `.omo/ulw-research/20260829-033311/claim-graph.md`,
    claims C-05 through C-15.
16. **Observation Manifest**,
    `.omo/ulw-research/20260829-033311/observation-manifest.md`, observations
    O-001 through O-013.
17. **Expansion Log**, `.omo/ulw-research/20260829-033311/expansion-log.md`,
    Wave 2.
18. SWE-bench (`https://www.swebench.com/`); OpenHands
    (`https://arxiv.org/abs/2407.16741`); AgentCanary
    (`https://arxiv.org/abs/2606.10484`); and Agent3Sigma-Canary
    (`https://github.com/antgroup/Agent3Sigma-Canary`).
19. **S5 Model-Version Research And Decision Preparation (parallel pass)**,
    `s5-model-version-research-2026-08-29.md`, sections 0-6. Workspace
    point-in-time evidence held outside the repository beside the session
    handoffs, not a committed file; fidelity-reviewed, folded into this report
    on 2026-08-29. It rests on two verified facts files compiled 2026-08-29, a
    repository-side extraction and a first-party provider survey; the citations
    in sources 20-32 are its underlying sources, reproduced here.
20. Anthropic, **Models overview**
    (`https://platform.claude.com/docs/en/about-claude/models/overview`),
    **Deprecation commitments**
    (`https://www.anthropic.com/research/deprecation-commitments`),
    **Working with messages**
    (`https://platform.claude.com/docs/en/build-with-claude/working-with-messages`),
    **Webhooks**
    (`https://platform.claude.com/docs/en/managed-agents/webhooks`), and the
    `claude-api` skill reference set (`shared/models.md`,
    `shared/platform-availability.md`, `shared/error-codes.md`). Accessed
    2026-08-29.
21. OpenAI, **Models** (`https://developers.openai.com/api/docs/models`) and the
    per-model pages beneath it, **Deprecations**
    (`https://developers.openai.com/api/docs/deprecations`), **Using the latest
    model** (`https://developers.openai.com/api/docs/guides/latest-model`),
    **Reproducible outputs**
    (`https://developers.openai.com/api/docs/guides/advanced-usage#reproducible-outputs`),
    and **Verifying webhook signatures**
    (`https://developers.openai.com/api/docs/guides/webhooks#verifying-webhook-signatures`).
    Accessed 2026-08-29.
22. Google, **Gemini API models**
    (`https://ai.google.dev/gemini-api/docs/models`), **Gemini API changelog**
    (`https://ai.google.dev/gemini-api/docs/changelog`), **Vertex AI model
    versions**
    (`https://docs.cloud.google.com/vertex-ai/generative-ai/docs/learn/model-versions`),
    and **Global endpoint for Claude models on Vertex AI**
    (`https://cloud.google.com/blog/products/ai-machine-learning/global-endpoint-for-claude-models-generally-available-on-vertex-ai`).
    Accessed 2026-08-29.
23. Microsoft, **Model versions**
    (`https://learn.microsoft.com/en-us/azure/foundry-classic/foundry-models/concepts/model-versions`),
    **Working with models**
    (`https://learn.microsoft.com/en-us/azure/foundry/openai/how-to/working-with-models`),
    **Model retirement schedule**
    (`https://learn.microsoft.com/en-us/azure/foundry/openai/concepts/model-retirement-schedule`),
    and **Confidential AI**
    (`https://learn.microsoft.com/en-us/azure/confidential-computing/confidential-ai`).
    Accessed 2026-08-29.
24. Amazon Web Services, **Model lifecycle**
    (`https://docs.aws.amazon.com/bedrock/latest/userguide/model-lifecycle.html`),
    **Inference profiles**
    (`https://docs.aws.amazon.com/bedrock/latest/userguide/inference-profiles.html`),
    and **Model invocation logging**
    (`https://docs.aws.amazon.com/bedrock/latest/userguide/model-invocation-logging.html`).
    Accessed 2026-08-29.
25. NVIDIA, **Attestation examples, single Hopper GPU**
    (`https://docs.nvidia.com/attestation/quick-start-guide/latest/attestation-examples/hopper_single_gpu.html`).
    Accessed 2026-08-29.
26. **openXwallet change `add-composition-drift-cascade`**, at openXwallet
    `main` `2d66850`: `openspec/changes/add-composition-drift-cascade/`
    `proposal.md` front matter and lines 115-117 and 145-151, `design.md` lines
    198-206 and 227-229,
    `specs/openxwallet-agent-profile/spec.md` lines 35-38 and 70-74, and
    `tasks.md` lines 44-60.
27. **codexFactory Gate-Rules and roster records**, at codexFactory
    `0c7b69ae9695fca371b92294bc327249d7bb3c46`:
    `hermes/domain/review-councils/records/2026-08-22-gate-rules-regular-pr-council-clearance.md`
    lines 383-387 and 553-578;
    `hermes/domain/review-councils/records/2026-08-26-gate-rules-classification-intent.md`
    lines 360-368;
    `hermes/domain/review-councils/records/2026-08-22-enrolled-roster-and-advisory-flip.md`
    lines 136-146; and `hermes/client/role-overrides.yaml` lines 22-44.
28. **codexFactory seeded adversarial corpus record**,
    `hermes/domain/review-councils/records/2026-08-22-seeded-adversarial-corpus.md`
    at codexFactory `0c7b69ae9695fca371b92294bc327249d7bb3c46`, especially the
    results summary, the per-seat rows, the diversity section, the cost table,
    and the record's own statement of what it does not establish.
29. **codexFactory composition-declaration authority**,
    `openspec/specs/domain-hermes-content/spec.md` (the declaration-only
    requirement, its scenarios, and the tenant-representation scenario) and
    `openspec/changes/archive/2026-08-28-declare-review-holder-composition/design.md`
    lines 84-86, at codexFactory
    `0c7b69ae9695fca371b92294bc327249d7bb3c46`.
30. **openXwallet neutral validator**, `openXwallet/scripts/validate-openxwallet.py`
    at openXwallet `main` `2d66850`: `check_agent_composition` and its two
    `declared_hash` sites, and the dispatch that runs it only when a composition
    record is present.
31. **Proposal: add-wallet-carried-review-authority**,
    `openspec/changes/add-wallet-carried-review-authority/proposal.md`, the
    distinctness-floor discussion (the anti-correlation finding, the
    declared-set completeness limit, and the quoted seeded-corpus warning).
32. **Review-authority register**,
    `governance/review-authority/register.yaml`, `rows` entry `row-mrc-0001`
    and the enumerated top-level keys.

## 10. Final Disposition

Packet research is complete. Packet 3 is ruled, not pending: the 2026-08-28
ruling of record stands, and reopening it would be a new change (section 4).
S5 itself remains incomplete pending applicable section 7 and 8.1 rulings and
core deltas, their merges and green realization evidence, the re-issuance
runbook walk, Council seat selection, Operator exact provider and execution
evidence, exact-version replacement of the current holder aliases, and
ratification of serialization semantics. No implementation,
model selection, exact provider version, deployment, alias admission, or grant
re-issuance is authorized by this report. The 2026-08-29 amendment adds evidence
and labeled recommendations only and changes none of that.
