## Context

The promoted document lifecycle gives every repository a brainstorm and staging
area and governs domain-to-neutral promotion. It does not define intake when
ownership is unknown or a durable way to split one domain-origin discussion
into neutral, domain, installer/runtime, and aggregation claims. The result is
manual placement, whole-document copying, and weak tag-based ownership.

This change owns ideation intake, claim-level routing, destination acceptance,
and the non-mutating organizer. Document cataloging is a separate capability
and proposal. Current authorized catalog signals may help select organizer
work, but routing remains complete and authoritative without them.

The active semantic-sweep change supplies the bounded worker pattern. The
document-cataloging change adds the thirteenth deterministic family. To avoid
conflicting replacement deltas for the enumerated doc-health family list,
routing implementation follows both and adds the fourteenth family.

Stakeholders are document authors, Domain Hermes authorities retaining domain
meaning, openxFactory ratify authority, destination owners, codexFactory
document-engineering workers, and operators reviewing organizer output.

## Goals / Non-Goals

**Goals:**

- Let authors capture ideas before final ownership is known.
- Keep known-domain thinking in the owning DomainxFactory.
- Route mixed ideas claim-by-claim with one canonical record and durable
  provenance.
- Require destination-owner acceptance before routing is complete.
- Make structural routing defects deterministic and machine-checkable.
- Use semantic analysis only for bounded, non-authoritative recommendations.
- Preserve human and Hermes authority over ownership, extraction, promotion,
  and lifecycle transitions.
- Migrate prospectively without inventing historical IDs.

**Non-Goals:**

- A general idea backlog in the xFactory aggregation repository.
- Requiring routing YAML for ordinary known-owner documents.
- Implementing document catalog storage, taxonomy, classification, or
  cataloger workers.
- Automatically moving, deleting, promoting, accepting, or approving content.
- Letting catalog tags or organizer confidence establish ownership.
- Replacing domain-to-neutral promotion or OpenSpec proposal gates.
- Defining proposal-origin policy or generic infrastructure readiness schemas.
- Making organizer recommendations merge-blocking in v1.

## Decisions

### 1. One canonical routing record per routed idea

An unclassified, mixed, or cross-domain idea receives one durable Idea ID and
one `routing.yaml` record paired with human-readable Markdown:

```text
openxFactory/ideation/brainstorm/inbox/XFI-2026-001/
  idea.md
  routing.yaml
```

Destination artifacts carry only the Idea ID, selected Claim IDs, and a pointer
to the canonical record. Copying the full routing record is invalid because
copies would drift and create competing routing state.

Idea IDs use `XFI-<year>-<three-digit-sequence>` and are allocated centrally in
`openxFactory/ideation/routing-index.yaml`. Claim IDs append
`-C<two-digit-sequence>`. Allocation and index update occur in one reviewed
change; collisions require rebase and reallocation.

### 2. Capture location reflects what is known now

- Known domain: the owning DomainxFactory brainstorm.
- Clearly neutral or cross-domain: openxFactory brainstorm.
- Genuinely unknown: openxFactory's unclassified inbox.

The aggregation repository remains limited to composition, pins, workflow, and
release effects. It cannot become a general ideation backlog.

### 3. Mixed ideas split by claim, not by document copy

Each independently routable statement receives an immutable Claim ID. The
routing record names proposed owner, target capability, destination,
dependencies, exclusions, rationale, blockers, and disposition.

For domain-origin expansion, the domain source remains design history and
authority for local meaning. An openxFactory routing hub references and
summarizes selected claims without copying the full source.

### 4. Routing state is orthogonal to document lifecycle

`Scope` and `Routing status` describe intake and routing; they do not add
document statuses. Document lifecycle remains brainstorm → staged → proposed →
promoted/adopted.

Routing transitions are append-only:

```text
null -> intake
intake -> triaging | deferred | rejected
triaging -> split | routed | deferred | rejected
split -> triaging | routed | deferred | rejected
routed | deferred | rejected -> triaging  (reviewed reopen)
```

Claim dispositions are `unresolved`, `proposed`, `routed`, `deferred`, and
`rejected`. A record reaches `routed` only after every active claim is resolved
and each routed claim records accepted owner, capability, destination,
acceptance actor, time, and evidence.

### 5. Cross-repository provenance uses structured references

Git cannot preserve one rename across repositories. Sources and destinations
therefore retain lightweight references containing canonical repository ID,
POSIX repository-relative path, full committed revision, Idea ID, Claim IDs,
and routing-record revision.

The reserved repository ID `xFactory` denotes the aggregation root; every
other ID is an exact aggregation-relative submodule path from `.gitmodules` and
resolves through its gitlink. Absolute paths and traversal are invalid.
`pending_capture` is allowed only during intake; organize and proposal gates
require committed revisions.

Proposal support manifests add `ideation_provenance` only when selected staged
material actually derives from routed claims. General proposal-origin,
proposal-authored support, and archive-source-state rules remain owned by the
separate staged `proposal-origin-contract` topic.

### 6. The deterministic family enforces routing by reference

After the prerequisite changes archive, `ideation-routing` becomes the
fourteenth deterministic family. It validates schemas and vocabulary, central
ID allocation, unique definitions, paired files, transitions, accepted
destinations, structured references, staged/proposal provenance, explicit
blockers, copied records, aging, and forbidden aggregation placement.

The checker distinguishes definitions from lightweight references and ignores
fenced examples. It may normalize safe mechanical path defects but cannot
choose an owner, split claims, accept destinations, move content, or promote
policy.

Strict organize/proposal mode materializes every referenced pinned repository.
A nightly unavailable external-path check is reported as skipped rather than
passed.

### 7. The organizer is a separate bounded worker lane

The `ideation-organizer` profile has its own prompt, schema, job type, artifact
lane, timeouts, concurrency, and capability advertisement. It reviews new or
materially changed eligible brainstorms and returns passage evidence,
rationale, numeric confidence, alternatives, exclusions, dependencies, and
unresolved ambiguity.

It cannot allocate IDs, mutate routing records, move content, or approve a
decision. An authorized Hermes role or human accepts, edits, or rejects its
recommendations; reviewed lifecycle tooling performs any extraction or move.

Validated recommendations are immutable records under:

```text
health/ideation-organizer/YYYY-MM-DD/<idea-id>-<run-id>.yaml
```

The next report links them. Closed reports are never edited, and temporary
Actions artifacts are not records.

### 8. Catalog signals are optional, current, and non-authoritative

Organizer selection may use a promoted catalog entry only when its locator or
authorized opaque resolver, content hash, inventory snapshot, and taxonomy
digest match current inputs and the entry is not policy-blocked. Stale or
blocked tags are ignored.

Catalog signals may enqueue review. They cannot allocate IDs, create or change
routing records, select owners or destinations, split claims, add `xspec:`
markers, or move content into staging.

### 9. Generic readiness is consumed, not redefined

The staged Client Infrastructure Liaison contract owns the neutral
`infrastructure_readiness_result`, trusted validator, evidence, expiry,
remediation, and outage semantics. Routing adds only organizer-specific
mandatory assertions: eligible runner state, fresh heartbeat, matching profile
and version, tenant/data boundary, handling authorization, and absence of
repository credentials.

Until the neutral readiness contract is promoted, implementation reuses the
existing semantic-sweep preflight shape without introducing a competing generic
schema.

### 10. Handling policy gates input and output

Orchestration checks source handling and domain policy against workload-specific
host authorization before sending content or identifying metadata. Redacted
input is allowed only when source policy explicitly authorizes the derived
view. Unauthorized work fails closed before dispatch.

Output filtering covers paths, inferred tags, owners, destinations, summaries,
and evidence because those values may disclose protected facts. Authorized
opaque references may replace prohibited identifiers.

### 11. Organizer dispatch is asynchronous and failure-isolated

The main deterministic report never depends on a self-hosted organizer job.
After hosted preflight, orchestration dispatches an independent child workflow.
Missing readiness or authorization records a fail-closed skip; worker loss,
invalid output, or timeout cannot hold deterministic finalization open.

A watchdog reports and cancels a child queued beyond ten minutes or running
beyond thirty minutes. Non-default thresholds are disclosed. Organizer output
is report-only and never opens critical/error regression issues in v1.

### 12. Disposition follows content ownership

The originating Domain Hermes approves surrender of domain meaning.
openxFactory ratify authority approves neutral content. Destination Domain
Hermes accepts its claims or overlays. Routing location, tags, and organizer
confidence grant no authority.

Mid-promotion, the domain-local source remains authoritative until neutral
promotion and consumer adoption complete.

### 13. Compatibility is prospective

Existing brainstorms remain valid. They receive Idea IDs only when materially
changed, deliberately routed, or migrated with evidence. Migration does not
invent historical routing decisions.

Source brainstorms carry one `Idea ID:`. A destination consolidating claims
from several ideas uses `Source Idea IDs:`, `Claim IDs:`, and `Routing records:`
without copying canonical records.

### 14. Active routing work ages visibly

An `intake`, `triaging`, or incomplete `split` record whose latest transition
is 30 days old produces a warning and escalates to error at 90 days. Routed,
rejected, and explicitly deferred records do not age as abandoned unresolved
work. Reports disclose non-default thresholds.

### 15. Prerequisite changes archive before implementation

This proposal may be reviewed now, but implementation of its doc-health delta
and archive gate follow `add-doc-health-semantic-sweep` and
`add-document-cataloging`. That sequence produces twelve deterministic
families plus the semantic pass, then catalog as family thirteen, then routing
as family fourteen without simultaneous replacement deltas.

## Risks / Trade-offs

- **Central allocation creates merge conflicts** → allocate IDs and update the
  index atomically; collisions rebase rather than inventing distributed IDs.
- **Routing records become an unauthorized ownership oracle** → require
  destination acceptance and distinguish proposals from accepted dispositions.
- **Protected metadata leaks through recommendations** → authorize before
  dispatch and filter locators, owners, destinations, summaries, and evidence.
- **Organizer outage delays reports** → use hosted preflight, independent child
  workflows, and watchdog cancellation.
- **Historic ideas appear noncompliant** → apply routing prospectively and
  prohibit fabricated IDs or transitions.
- **Catalog and routing recouple** → treat catalog data as optional selection
  signals and keep schemas, workers, persistence, tests, and failure paths
  separate.

## Migration Plan

1. Finish and archive the semantic-sweep and document-cataloging prerequisites.
2. Promote routing schemas, templates, validators, and lifecycle guidance.
3. Add the deterministic routing family and strict reference resolver.
4. Update DomainxFactory scaffolds and guides, then re-pin consumers.
5. Add the bounded organizer profile and workload-specific readiness checks.
6. Enable asynchronous organizer dispatch and report linking.
7. Pilot one unknown-owner idea and one domain-origin mixed idea through
   reviewed destination acceptance without automatic movement.

Rollback disables organizer dispatch while deterministic routing records and
checks remain available. Existing ordinary and historic brainstorm documents
require no rollback because routing is prospective.

## Open Questions

- Catalog-triggered organizer selection remains optional until both promoted
  capabilities have production evidence; manual and changed-idea triggers are
  sufficient for initial routing realization.
