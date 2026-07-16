# Design: Possibles Derivation Lane

## Context

`add-ideation-cross-reference-readiness` landed the unified cross-reference
index (`ideation/cross-reference.yaml`, source of truth; `.md` generated), which
embeds a top-level `possibles_register` `$ref`ing the
`ideation-possibles-register` kernel. The bootstrap index deliberately leaves
`possibles_register` ABSENT (task 2.4 note), so the dashboard funnel's possibles
column is empty and the WHEEL renders only synthesized, demo-marked placeholders
under its "possibles honesty rule" (ideation-dashboard brainstorm, THE WHEEL
locked spec, Brett-approved 2026-07-16).

The kernel already anticipated this lane. Its prose fixes the four register
states (`latent`/`picked`/`rejected`/`superseded`), the one-way transition
machine with no resurrection, and — as a SIBLING concern — the `pending_review`
disposition + evidence contract that lands on the index's cluster/recommendation
entry (the human-seen intake), NOT on the register. This change is the
possibles-side analog of that human-seen intake: instead of a human proposing a
cluster, a bounded AI worker proposes candidate possibles, and humans dispose on
the same gate console.

The document-cataloger lane (`add-document-cataloging`, contract-v1.11) is the
worked precedent for a bounded, artifact-only, non-blocking AI worker with
immutable evidence and a next-run merge. Its hard-won invariants reappear here as
requirements.

## Goals / Non-Goals

**Goals:**

- Fill the empty possibles register with AI-proposed candidates so the funnel
  has left-hand supply and the WHEEL shows real (not demo) possibles.
- Keep every derived possible sourced, non-authoritative, and human-disposed:
  `pending_review` until a human accepts/rejects/defers on the gate console.
- Reuse the kernel's existing evidence/provenance fields; add only the smallest
  additive delta the worker-run provenance genuinely needs.
- Carry the cataloger lane's failure containment, model-worker, and
  immutable-evidence/next-run-merge contracts forward verbatim in intent.

**Non-Goals:**

- Readiness scoring (`add-ideation-cross-reference-readiness` owns the tier
  panel and the min>=8 gate; a cluster can be derivation-rich yet unready).
- Any autonomous lifecycle action — the lane creates no proposal, picks no
  possible, and promotes nothing; disposition is a human act.
- Rendering. The dashboard/WHEEL consume the index; this change defines the data
  contract and the distinct-class rule only, not the view.
- A third possibles file. The register stays embedded in the index (kernel R1:
  "no third standalone register file exists").

## Decisions

### 1. Derivation is a separate lane from readiness scoring

The readiness lane JUDGES an existing cluster: three tier reviewers emit 1-10
scores with the organizer evidence contract, and the min>=8 gate flags a
`pending_review` recommendation against the topic entry. Derivation SYNTHESIZES
new material: it reads clusters/staged topics/members and proposes NEW
`possibles_register` entries. These differ in prompt contract (a generative
"what could this become" prompt versus a scoring rubric), output shape (register
entries versus tier assessments), write target (`possibles_register` versus
`topic_entry.readiness`), and failure blast radius. Bundling a generative lane
into a judgment lane would conflate the two prompt contracts, couple their
timeouts and skips, and make one worker's failure suppress the other. So this is
its own lane with its own worker profile and prompt-contract version, running
beside — never inside — the readiness lane.

### 2. Additive kernel delta: `origin` + a `derivation` block

The register `register_entry` currently requires `id`, `title`, `claim`,
`state`, `provenance`; `state` is one of `latent`/`picked`/`rejected`/
`superseded`. An AI-derived, undisposed candidate needs three things the kernel
does not yet express: a mark that it is AI-derived, the worker-run identity, and
the `pending_review` review disposition. The minimal, forward-compatible delta,
modelled ONE-FOR-ONE on the topic entry's `origin` + `human_seen` pair:

- `register_entry.origin`: optional enum `[human-authored, ai-derived]`; absent
  defaults to `human-authored` (exactly as `topic_entry.origin` absent means
  `machine-derived`). Human-authored possibles are unaffected.
- `register_entry.derivation`: optional object, REQUIRED when `origin:
  ai-derived` (an `allOf` conditional mirroring the human-seen conditional). New
  `$defs/derivation`:
  - `worker_run` (required): `correlation_id`, `worker_profile`,
    `prompt_contract_version` — all non-empty strings.
  - `disposition` (required): `const: pending_review` — the machine output, as
    with `human_seen.disposition` and `score_evidence.disposition`.
  - `human_disposition` (optional): a documented structural mirror of the index
    schema's `human_disposition` (`outcome` = accepted|rejected|deferred,
    `authority`, `at`, `note`) — the family's established mirror pattern (as
    `score_evidence` mirrors the organizer recommendation), avoiding a circular
    `$ref` back into the index schema.

Because the delta adds only optional fields and a conditional that never fires on
existing (origin-absent) entries, it is additive and needs NO
`contract_schema_version` bump, per the kernel's own additive-growth rule.

Justification for touching the kernel at all (the brief's explicit ask): the
worker-run provenance and the review disposition have no home on the existing
`register_entry`. The `state` machine is about the PICK lifecycle, not about
AI-review status; overloading `state` with a fifth `pending_review` value would
rewrite the documented four-state machine and conflate "unpicked backlog" with
"unvetted proposal". A parallel `origin` + `derivation` pair keeps the pick
lifecycle intact and matches the precedent the kernel itself points to.

### 3. Evidence reuses existing kernel fields; provenance stays honest

"Evidence citing the source cluster/topic/doc members" needs NO new field: the
source topic clusters are `claiming_clusters` edges and the source member
passages are `supporting_evidence` pins (`evidence_pin`: document + section +
passage hash). A derived entry MUST carry at least one of each, so it is never
an unsourced assertion. The required `provenance` (`ingestion_provenance`)
retains its `Possible feats:` meaning; a derived entry cites the primary source
member document in `provenance.document` and the derivation cluster context in
`provenance.section`. The worker-run identity lives in `derivation.worker_run`,
NOT in `ingestion_provenance`, so `ingestion_provenance` is not stretched and
its `required: [document, section]` is not loosened (loosening would be a
breaking change, not additive).

### 4. Orchestration-authoritative identifiers (model-worker contract)

The tool-less LLM worker proposes titles, claims, and rationale prose only. It
MUST NOT compute, invent, or transcribe any machine-precision value — register
ids, correlation ids, content/passage hashes, revisions, counts. Orchestration
computes every such value and treats its own values as authoritative; a
worker-supplied precision value that disagrees voids the affected proposals
rather than persisting a corrupted entry. This is the document-cataloger lesson
verbatim: a worker that mis-copied one hex character of a content hash voided
twenty-five classifications.

### 5. One-way disposition on the gate console; accepted retains provenance

A derived possible stays `pending_review` until a human disposes it on the gate
console (accepted/rejected/deferred), one-way and never auto-promoted. On
ACCEPT it becomes a first-class `latent` register possible retaining
`origin: ai-derived` (exactly as an accepted human-seen cluster retains
`origin: human-seen`), then follows the normal pick lifecycle. On REJECT it is
recorded `rejected` with the required reason + citation drawn from the
disposition, preserving the audit trail so the same candidate is not silently
re-derived; a later revival is a NEW entry with a new id (no resurrection). The
lane itself moves no document and changes no lifecycle state.

### 6. Bounded worker, immutable evidence, concurrency-protected next-run merge

The worker is a distinct bounded artifact-in/artifact-out Omnigent job with its
own profile, no repository credentials, and no write authority. Its output never
blocks deterministic work; offline/unauthorized/partial/invalid/timed-out/failed
runs leave the deterministic pass, the report, and the register unchanged. A
watchdog reports and cancels a child queued beyond ten minutes or running beyond
thirty minutes. Validated output is immutable evidence under the factory
identity and merges into `possibles_register` only through a later main run,
under concurrency protection that refuses to overwrite a register a concurrent
run has advanced (the 669d60a stale-overwrite class). The merge preserves
register id uniqueness and never edits a disposed entry.

### 7. Distinct class until disposed (WHEEL data-contract consistency)

THE WHEEL's realization data contract carries a per-edge class field
`indexed | inferred | synthesized` that drives thread styling (solid teal =
indexed, dashed teal = inferred, dashed brass = synthesized/demo). Undisposed
derived possibles MUST be distinct from human-picked ones: their cross-class
edges carry a non-`indexed` class (`inferred`/`synthesized`), and no consumer
renders or counts an undisposed derived possible as human-picked indexed data.
Real derived possibles populating the register replace the WHEEL's
synthesized-demo placeholders (the "possibles honesty rule"). This change fixes
the contract; the codexFactory realization drives the styling.

## Risks / Trade-offs

- **A generative worker fabricates ungrounded possibles** → require at least one
  `claiming_clusters` edge and one `supporting_evidence` pin per derived entry;
  reject unsourced proposals before persistence; keep everything `pending_review`
  and human-disposed.
- **Undisposed AI proposals pollute the "latent backlog" view** → `origin:
  ai-derived` + `disposition: pending_review` make them contractually distinct;
  consumers exclude them from human-picked totals and from any Ranked Plan.
- **Worker corrupts identity/evidence** → orchestration-authoritative identifiers
  (Decision 4); worker precision values are discarded.
- **Two lanes couple** → separate worker profile, prompt-contract version,
  evidence artifact, and failure isolation (Decision 1).
- **Merge clobbers a concurrent run** → next-run merge under stale-overwrite
  concurrency protection (Decision 6).

## Migration Plan

1. Land the additive kernel delta (`origin` + `derivation`) and packaged
   example; extend `validate-ideation-dashboard-contracts.py` to enforce the new
   shape and the one-way disposition; note the delegation in the index validator.
2. Register the delta in `contracts/manifest.yaml`/`CHANGELOG.md`/`README.md` at
   realization (avatar-client precedent: registration at the realization commit).
3. Realize the codexFactory derive-possibles worker + prompt contract + output
   validation, and the next-run merge, following the ideation-readiness split.
4. Add the omnigent-install worker profile and the aggregation nightly child +
   watchdog + submodule commit-back.
5. Enable the lane; it reports SKIPPED until a host advertises the profile (the
   readiness-lane precedent for a valid landed state).

Rollback disables the lane and leaves the register untouched; the kernel delta
is additive so nothing regresses.

## Open Questions

- Derivation budget/selection (how many candidates per cluster per run, and
  which clusters to prioritize) is a scorer-side tuning decision confirmed at
  realization, not a contract question — mirroring how the readiness scorer
  confirmed its spread threshold and fit-resolution set at realization.
- Whether an accepted derived possible's edges become `indexed` (versus staying
  a distinct accepted class) is a WHEEL styling choice for the codexFactory
  realization; the contract only requires undisposed ones to be non-`indexed`.
