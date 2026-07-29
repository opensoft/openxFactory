# Domain Practice Suggestion Generation: how the Domain Hermes proposes autonomously — Brainstorm

Status: brainstorm
Kind: architecture
Summary: Mechanics for the Domain Hermes (e.g. codexFactory = Software
Engineering) to autonomously generate "this subject should adopt this
practice" suggestions: a practice catalog bound to capability maturity,
a read-only gap scan over governed subjects, a structured suggestion
record with idempotency and suppression, and a hard autonomy boundary —
the domain may only ever SUGGEST. Umbrella:
`hermes-governed-nightly-sweep.md`.
Topics: practice-adoption, practice-catalog, adoption-profile, gap-scan, suggestion-record,
domain-autonomy, domain-hermes, practice-adoption
Repository context: openxFactory (adoption-profile schema neutral; catalog content codexFactory)
Captured: 2026-07-20

## Possible feats

- **Neutral `adoption_profile` schema** (openxFactory) carried by capabilities.
- **Read-only gap-scan worker** enumerating registered governed subjects.
- **`practice_adoption_suggestion` record kind** with idempotency + suppression.

## Where best practice lives: the practice catalog

A domain's expertise is already partially reified: promoted capabilities
(doc-health-checker, workflow-gate-contract, ...) with lifecycle
statuses. What is missing is the ADOPTION claim: "subjects of kind K
in state S should realize capability C via realization R."

Sketch: each capability MAY carry an `adoption_profile`:

- `subject_kind`: what this applies to (a repo, a cluster, an install —
  reuse the subject-kind vocabulary from the client-infrastructure
  records: subjects are class-only, never actors).
- `applicability`: predicates over observable subject state ("holds
  documents with governance Status headers", "has a default branch with
  protection", "is registered in the install's stack.yaml").
- `realization`: what adoption concretely looks like (for the nightly
  sweep: the thin caller workflow present, pinned to the reusable
  workflow at a released ref, runs green within the last N days).
- `maturity_gate`: the capability's lifecycle status required before
  the domain may SUGGEST it (`standard` seems right: ratified = exists,
  standard = the domain stakes its name on recommending it).
- `risk_class`: input to the policy layer's auto-clear envelope
  (does adoption add credentials? external calls? spend?).

The catalog is domain-owned content in the domain repo, but the SCHEMA
for adoption profiles is neutral (openxFactory) so every domain's
suggestions look the same to every client's policy layer.

## The gap scan: how generation actually happens

A periodic, READ-ONLY sweep by the Domain Hermes (yes — a meta-nightly;
the recursion is a feature, not a bug, because suggestion generation is
side-effect-free):

1. Enumerate governed subjects for each client install (from the
   install's stack/registry records — the domain does not discover
   subjects by scanning the world; it reads what the client has
   registered, which keeps tenant boundaries clean).
2. For each (subject, adoption_profile) pair where `applicability`
   holds: observe realization state. Observation must be cheap,
   unprivileged, and evidence-producing (the workflow file exists at
   HEAD; the last scheduled run's conclusion; the report artifact's
   age). If observation needs credentials the domain does not hold,
   the OBSERVATION ITSELF is the first suggestion ("grant read access
   so adoption can be assessed").
3. Gap → emit `practice_adoption_suggestion`; adopted → emit/refresh
   adoption evidence; drift (was adopted, now broken) → emit a
   suggestion flagged as REGRESSION, which policy layers likely
   fast-track.

Trigger options for the scan (not mutually exclusive): scheduled
(meta-nightly), event-driven (capability reaches `standard`; new
subject registered; client onboards), and on-demand (liaison asks
"what does the domain recommend for this repo?").

## The suggestion record

Follows the client-infrastructure-request family's grammar (six
identity classes, opaque refs, no secrets, explicit transitions), even
if it becomes its own kind:

- `suggestion_id` + `idempotency_key` (subject + practice + catalog
  version → regeneration is a no-op while one is open).
- `practice_ref` (capability + adoption_profile version) and
  `subject_ref`.
- `rationale`: the domain's evidence — WHY this practice, citing the
  capability's spec and the observed gap. Suggestions without evidence
  are noise; the record should make thin rationales embarrassing.
- `proposed_realization`: concrete enough for the project layer to
  execute (file paths, pinned refs, expected green signal) without the
  domain doing anything itself.
- `risk_class` + `credential_implications` (feeds auto-clearance).
- `disposition` lifecycle: suggested → cleared | rejected |
  deferred(until) → realized → adopted(evidence) — with rejection
  suppression honored on regeneration (a rejected suggestion does NOT
  reappear until the practice's catalog version or the subject's state
  materially changes; mirror doc-health's contested-finding
  dispositions).

## The autonomy boundary (the load-bearing rule)

The Domain Hermes may autonomously: read registered subject state,
evaluate applicability, emit/refresh/close suggestions, and publish its
catalog. It may NOT: touch the subject, open PRs, request credentials
for itself, or escalate its own suggestions past the policy layer.
Autonomy is safe because the entire generation path is
side-effect-free; the first side effect anywhere in the pipeline
belongs to the CLIENT's cleared decision. This is the same fail-closed
instinct as the reference avatar runtime's fixture adapters: the
boundary is structural, not behavioral.

## Open questions

- Catalog versioning: does a new adoption_profile version reopen
  previously rejected suggestions? (Leaning: yes — rejection binds to
  the version rejected.)
- Who signs the catalog? A practice entering the catalog is the domain
  staking its reputation; is that a domain-internal OpenSpec change
  (leaning yes — catalog changes are contract changes)?
- Observation authority for private subjects: read tokens are
  themselves credentials; is "observability grant" a standing item in
  the client-infrastructure vocabulary?
- One suggestion per subject or batched per client? (Policy layers
  probably want batch review UX; records should stay per-subject for
  traceability either way.)
- Does the gap scan run inside the deployed Hermes runtime (a CronJob
  in the hermes namespace — inheriting the corebackup spot-eviction
  pause, acceptable) or as a factory workflow (GitHub-scheduled, like
  the sweep it governs)? Dogfooding argues for the former once the
  runtime grows job scheduling.
