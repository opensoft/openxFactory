# S5 Model-Version Governance Research Report

Status: complete research snapshot; no implementation is authorized
Prepared: 2026-08-29
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

## Decision Boundary

1. Packet 1: Gate-Rules Council seat-to-model or model-family selection.
2. Packet 2: Operator exact provider-version and execution-identity evidence.
3. Packet 3: Convener ruling on admissible pin forms.
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

## 4. Packet 3: Convener Admissible-Pin Ruling

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

### Proposed Canonicalization And Attestation Design

This is a proposal for ratification, not a final standard. Every unresolved
choice below must be ratified before implementation or activation.

1. **Value-domain normalization.** Convert each component to typed values before
   serialization. Require explicit null handling, explicit defaults, canonical
   provider and component identifiers, lowercase digest hex, RFC 3339 UTC times
   where time is permitted, and no implicit environment-derived values.
   Unresolved: parameter vocabulary, defaulting rules, and exact provider
   identity grammar.
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

## 6. Contradictions And Counter-Evidence

| Observation | Consequence | Disposition |
|---|---|---|
| Current roster is model-diverse in intent but uses mutable aliases. | Diversity intent does not meet exact-version identity. | Council selection remains independent and unresolved; Operator evidence is separately required before issuance or activation. [2][3][4] |
| Exact provider IDs exist, but no reviewed provider supplies a universal cryptographic serving digest. | Exact ID cannot mean complete serving immutability. | Limit claim to artifact targeting and pair it with Packet 2 execution evidence. [5][9][10][11][12][13] |
| A Foundry deployment name can remain while model configuration changes. | Deployment name cannot be the model pin alone. | Bind configured model/version and deployment read-back in Packet 2. [13] |
| Direct Anthropic and partner-hosted surfaces can share model names. | Lifecycle and execution identity cannot be inherited across planes. | Require separate direct, Vertex, Bedrock, or Foundry evidence. [9][11][12][13] |
| Agent-profile authority defines components and binding modes but not canonical serialization. | A hash can be structurally required while byte semantics are undefined. | Ratify proposed serialization or keep activation fail-closed. [6][7] |
| Canonical codexFactory state declares a six-component holder source map, but its `model_version` source resolves to mutable aliases and no ratified canonical serialization exists. | Source mapping is verified, while Q8(d) identity and deterministic composition bytes remain unresolved. | Operator supplies exact-ID evidence; human authority ratifies serialization and attestation semantics before activation. [2][4][8] |

## 7. Unresolved Decisions Matrix

| Unresolved fact or decision | Owner | Closure evidence | Blocking effect |
|---|---|---|---|
| Seat model or model-family selection | Gate-Rules Council | Signed selection record, duty-specific soak pass, rejected alternatives, diversity analysis, and recorded Council-convener disposition. | Blocks an accepted selection from existing when unresolved; does not itself issue or activate a grant. |
| Application of an accepted selection to the enrolled roster | Designated roster-change Lead | `lead_accepted_recorded` evidence, the reviewed roster change, and fresh soak evidence for the applied roster. | Blocks live roster application; does not substitute for human-ratified issuance. |
| Exact published version and live execution identity | Operator | Packet 2 record with provider documentation, lifecycle, console or API read-back, authorization or eligibility evidence, and execution evidence. | Blocks governed issuance and activation, not the Council's model-family selection. |
| Exact execution identity for the current Claude Code alias invocation | Operator | Documented exact resolution or replacement configuration, recorded evidence, and no undocumented substitution. | Blocks use of `opus` or `sonnet` for a governed holder. |
| Admissibility of attested alias resolution | Convener | Explicit ruling plus ratified and implemented core and contract delta meeting Packet 3 controls. | Exact published version only remains mandatory. |
| Exact-version replacement for the current holder's alias-valued model source | Operator | Packet 2 exact-ID record plus a codexFactory holder-profile update referencing the Council selection and stable repository revision. | Blocks Q8(d)-conformant issuance and activation; the six-component source map itself is already identified. |
| Canonical serialization profile and value-domain rules | Human ratification authority | Ratified grammar for normalization, ordering, encoding, duplicate handling, digest, and examples. | Blocks trusted composition digest comparison and activation. |
| Attestation envelope and signer trust model | Human ratification authority and Operator | Ratified envelope, signer authorization, key and revocation model, and evidence-retention location. | Blocks signed composition attestation. |
| Re-issuance runbook walk | Operator with human ratifier | Recorded deliberate composition bump, cascade, new human-ratified register act, and parked or refused old authority. | Blocks S5 completion and normal recovery from a provider roll. |
| In-flight content-provenance treatment | Hermes runtime ruling owner | Explicit ruling and implementation evidence after ratification. | Limits the runtime revalidation claim; does not relax drift refusal. |

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

## 10. Final Disposition

Packet research is complete. S5 itself remains incomplete pending applicable
section 7 and 8.1 rulings and core deltas, their merges and green realization
evidence, the re-issuance runbook walk, Council seat selection, Operator exact
provider and execution evidence, exact-version replacement of the current
holder aliases, and ratification of serialization semantics. No implementation,
model selection, exact provider version, deployment, alias admission, or grant
re-issuance is authorized by this report.
