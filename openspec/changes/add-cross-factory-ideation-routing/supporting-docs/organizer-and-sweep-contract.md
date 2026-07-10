# Ideation Organizer And Sweep Contract

Status: draft
Proposed by: add-cross-factory-ideation-routing
Kind: architecture
Repository context: openxFactory
Staging ID: openxFactory:staging:ideation-routing
Target capabilities: `ideation-routing` (ADDED) and `doc-health` (MODIFIED)

## Decision

Document organization and ideation routing use complementary components:

```text
deterministic doc-health sweep
  -> emits one shared inventory
  -> detects structural routing defects

semantic ideation organizer
  -> consumes only current catalog signals
  -> recommends ownership, claim splits, and destinations for eligible ideas

owning Hermes or authorized human
  -> decides and approves routing

lifecycle tooling
  -> performs reviewed moves, extraction, and proposal transitions
```

The organizer remains separate from the deterministic sweep and from the
document cataloger defined by `add-document-cataloging`. Detection,
classification, routing recommendation, authority, and mutation must not
collapse into one autonomous step.

The organizer may consume a catalog signal only when its locator or authorized
opaque resolver, content hash, inventory snapshot, and effective taxonomy
digest are current. It ignores stale and `policy_blocked` classifications.

## Deterministic Sweep

Add an `ideation-routing` check family to the regular doc-health pass. It uses
no model calls and validates:

- unique Idea IDs and Claim IDs;
- routing YAML schema and controlled vocabulary;
- paired `idea.md` and `routing.yaml` agreement;
- resolvable source, routing-record, and destination paths;
- staged artifacts citing existing claims;
- proposal manifests pinning routing provenance;
- routed claims having a destination or explicit blocker;
- duplicate or conflicting routing records;
- unclassified ideas exceeding the configured aging threshold;
- destination documents containing copied routing YAML; and
- general ideation backlogs incorrectly placed in the aggregation repository.

The deterministic pass may automatically correct only safe mechanical defects
already permitted by doc-health policy, such as normalized path separators. It
must not choose an owner, split a claim, move a document, or promote policy.

## Semantic Ideation Organizer

The organizer examines new or materially changed brainstorm content and may
recommend:

- scope classification;
- domains touched and candidate owners;
- independently routable claims;
- likely neutral skeleton and domain-local exclusions;
- dependencies among claims;
- duplicate or related ideas;
- destination brainstorm or staging topics; and
- questions that block confident routing.

Its output is a versioned recommendation artifact, not a doc-health finding or
draft routing-record mutation. Every recommendation includes a committed
source revision, passage hash and section reference, rationale, numeric
confidence from 0 through 1, alternatives, and unresolved ambiguity.

The organizer must not:

- change repository ownership;
- move, delete, supersede, or promote a document;
- create a normative staging claim without review;
- assign approval or execution authority;
- mark a disputed claim resolved;
- copy private domain/customer content into a neutral record; or
- treat model inference as source-backed domain truth.

## Trigger Policy

| Trigger | Component | Default behavior |
|---|---|---|
| Nightly repository health run | deterministic sweep | scan all governed routing records and references |
| New or changed `Scope: unclassified` or `mixed` brainstorm | organizer | enqueue semantic review |
| Manual operator request | organizer | review named idea or topic |
| Cross-domain link added to a known-domain brainstorm | organizer | recommend whether a routing hub is needed |
| Aging threshold exceeded | sweep then organizer | deterministic finding followed by optional semantic recommendation |
| Before organize/proposal gate | both | strict validation and unresolved-claim report |

The semantic organizer should normally run on changed inputs only. A full
repository semantic reorganization is on-demand or scheduled infrequently,
not part of every nightly run.

Recommended initial cadence:

- deterministic routing checks nightly;
- semantic organizer on demand and on qualifying changes;
- optional weekly deduplication/cross-domain review; and
- mandatory strict run before staging or proposal transition.

## Ownership

| Surface | Owner |
|---|---|
| neutral routing and routing-finding contracts | openxFactory |
| deterministic and semantic implementation | codexFactory doc-engineering capability |
| nightly workflow hosting and reports | xFactory aggregation repository |
| ideation execution worker | dedicated `ideation-organizer` Omni/Omnigent profile on the document-analysis host |
| routing disposition | owning Domain Hermes, neutral boundary authority, or authorized human |
| lifecycle mutation | reviewed lifecycle tooling under the owning repository |

Organizer dispatch is an independent follow-up workflow. A hosted preflight
checks both eligible-runner state and an Omni readiness heartbeat no older than
five minutes plus workload-specific tenant/data-boundary and handling
authorization before dispatch, so deterministic report finalization never
waits on the Cloud PC. Orchestration also checks each source's declared handling
and source-domain policy. If readiness or authorization is absent, the report
records a fail-closed skip without sending content or identifying metadata.
Redacted input is allowed only when source policy explicitly permits that
derived view. A watchdog reports and cancels a child queued beyond ten minutes
or running beyond thirty minutes without blocking deterministic results.

## Organizer Output

```yaml
schema_version: 1
kind: ideation_organizer_recommendations
status: record
idea_id: XFI-2026-001
source_revision: <commit>
recommendations:
  - claim_candidate_id: candidate-01
    source_ref:
      repository: openxFactory
      path: ideation/brainstorm/inbox/XFI-2026-001/idea.md
      revision: <full commit>
      section: infrastructure-management
      passage_sha256: <sha256>
    summary: Every Client Hermes needs an infrastructure liaison
    proposed_owner: openxFactory
    proposed_target: ideation/staging/client-infrastructure-liaison
    confidence: 0.86
    alternatives:
      - OpsxFactory
    domain_local_exclusions:
      - Intune execution policy
    rationale: Reusable client coordination behavior across domains
    disposition: pending_review
```

Organizer findings are proposals, not verdicts. Accepted recommendations are
written into the routing record by an authorized transition; rejected and
modified recommendations remain evidence for why routing changed.

After validation, orchestration persists the immutable recommendation at
`health/ideation-organizer/YYYY-MM-DD/<idea-id>-<run-id>.yaml` with
`status: record` and links a
summary from the next dated health report finalized after it lands. An already
closed `Status: record` report is never edited, and a temporary workflow
artifact is not the record. The canonical routing record appends acceptance,
modification, or rejection plus the evidence-record reference; protected domain
values pass through an output-policy filter that may suppress paths, proposed
tags/owners/destinations, summaries, and evidence or replace them with authorized
opaque references and hashes rather than copy them centrally.

## Failure And Safety Posture

- Parser or schema failure creates a deterministic finding.
- Organizer failure records no semantic recommendation and leaves the source
  unchanged.
- Missing worker readiness records a skip before dispatch; stale child runs are
  handled by the independent-workflow watchdog.
- Missing tenant/data-boundary or handling authorization fails closed before
  organizer content or identifying metadata is dispatched; redaction is used
  only when source policy explicitly permits it.
- Conflicting owner recommendations route to review.
- Potential private or regulated content is processed and persisted only under
  source-domain policy; output filtering covers inferred metadata as well as
  passages.
- No organizer output is executable authority.

## Acceptance Tests

- nightly checks find duplicate IDs without a model call;
- ordinary docs without routing metadata pass;
- changed mixed brainstorms enqueue semantic review;
- organizer output includes evidence, confidence, alternatives, and pending
  disposition;
- organizer cannot mutate lifecycle state;
- semantic failure does not suppress deterministic health results;
- unauthorized organizer hosts receive neither protected content nor
  identifying metadata;
- routing approval is attributed to the owning authority; and
- accepted organizer recommendations update one canonical routing record.
- current catalog tags may enqueue routing review but never create routing
  state; and
- organizer failure remains observable and non-blocking.
