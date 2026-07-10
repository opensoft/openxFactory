# Staged: Cross-Factory Ideation Routing

Status: draft
Proposed by: add-cross-factory-ideation-routing
Kind: process
Repository context: openxFactory
Staging ID: openxFactory:staging:ideation-routing
Source: xFactory brainstorming ownership review, 2026-07-09.
Target capabilities: `ideation-routing` (ADDED), `document-lifecycle`
(MODIFIED), and `doc-health` (MODIFIED).
Related process: [Domain-To-Neutral Promotion Process](../../../../docs/domain-to-neutral-promotion-process.md).

## Problem

xFactory ideas often begin before their final owner is known. A conversation
may start in MedxFactory or codexFactory and later reveal:

- a reusable neutral xFactory contract;
- policy or behavior owned by the originating domain;
- implications for one or more additional domains;
- an installer or execution-runtime concern; and
- examples that belong in several thin domain overlays.

Requiring the author to choose the final repository before capturing the idea
creates friction and lost thinking. Keeping every mixed idea in one central
brainstorm with domain tags creates the opposite problem: tags become a weak
substitute for ownership, one document accumulates competing authorities, and
promotion requires copying prose without clear provenance.

The shared lifecycle needs a capture-first, route-later convention.

## Entry Points

```text
Known domain owner
  -> DomainxFactory/ideation/brainstorm/<topic>.md

Clearly neutral or already cross-domain
  -> openxFactory/ideation/brainstorm/<topic>.md

Ownership genuinely unknown
  -> openxFactory/ideation/brainstorm/inbox/<idea-id>/
       idea.md
       routing.yaml
```

The top-level xFactory aggregation repository does not own the ideation
backlog. It owns composition, pins, and release coordination. Unknown and
cross-factory ideation remains in openxFactory until routed.

Each inbox item is a separate document. A single large tagged inbox document
is prohibited because it prevents independent routing, status, provenance,
and lifecycle transitions.

## Minimum Capture Metadata

```text
Status: brainstorm
Kind: idea
Repository context: openxFactory
Idea ID: XFI-2026-001
Scope: unclassified
Origin: MedxFactory discussion
Domains touched: MedxFactory, OpsxFactory
Candidate owners: openxFactory, OpsxFactory
Routing status: intake
```

`Idea ID` is durable across routing and proposal history. Domain tags and
candidate owners aid discovery; they do not grant ownership or authority.
IDs use `XFI-<year>-<three-digit-sequence>` and are allocated centrally from
`openxFactory/ideation/routing-index.yaml`. The index entry and routing record
are created in the same reviewed change; validation rejects collisions, so a concurrent
change must rebase and allocate a new sequence.

Allowed `Scope` values are:

- `unclassified` — ownership has not been determined;
- `domain` — one DomainxFactory owns the idea;
- `cross_domain` — several domains participate but no neutral claim has yet
  been selected;
- `neutral_candidate` — at least one claim may belong in openxFactory; and
- `mixed` — the idea has both neutral and domain-owned claims.

Allowed `Routing status` values are `intake`, `triaging`, `split`, `routed`,
`deferred`, and `rejected`. These are routing metadata, not replacements for
the canonical document `Status:` taxonomy.

Allowed transitions are `null -> intake`, `intake -> triaging | deferred |
rejected`, `triaging -> split | routed | deferred | rejected`, `split ->
triaging | routed | deferred | rejected`, and a reviewed reopen from any
terminal state to `triaging`.

## Domain-Origin Expansion

When an idea begins in a domain and later crosses boundaries, keep the original
domain brainstorm as design history and as the authority for domain-local
meaning. Create an openxFactory routing record that references it.

```text
MedxFactory brainstorm
  original clinical problem and domain context
              |
              v
openxFactory cross-domain routing record
  durable idea ID, claim IDs, owners, targets, dependencies
       |                 |                 |
       v                 v                 v
openxFactory         MedxFactory       OpsxFactory
neutral claims       medical overlay   IT operations claims
```

The routing record summarizes and identifies claims; it does not copy the full
source conversation. The originating document adds an `Extracted to:` or
`Routing record:` reference so the transition is visible and reviewable.

## Claim-Level Routing

Mixed ideas are split by claims rather than by entire documents. Each selected
claim receives a durable ID:

```text
<idea-id>-C<sequence>
```

Example:

| Claim ID | Claim | Owner and destination |
|---|---|---|
| `XFI-2026-001-C01` | Every Client Hermes coordinates required external infrastructure | openxFactory staging |
| `XFI-2026-001-C02` | Care Hermes uses the liaison for Medx dependencies | MedxFactory staging |
| `XFI-2026-001-C03` | Intune and Cloud PC execution follow Ops policy | OpsxFactory staging |
| `XFI-2026-001-C04` | Omni host packaging and recovery behavior | CloudPC-Install planning/change surface |
| `XFI-2026-001-C05` | Protected medical data cannot use an unapproved fallback | MedxFactory staging |

Each claim record declares:

- summary and source passage reference;
- proposed owner and destination;
- classification rationale;
- dependencies on other claim IDs;
- domain-local exclusions;
- routing disposition; and
- destination artifact or unresolved blocker; and
- destination-owner acceptance actor, time, and evidence before `routed`.

Claim disposition values are `unresolved`, `proposed`, `routed`, `deferred`,
and `rejected`. A routed claim requires an accepted owner, target capability,
structured destination, and acceptance evidence. A record reaches `routed`
only when no active claim remains unresolved or proposed.

## Classification Rules

| Claim shape | Owner |
|---|---|
| reusable workflow, authority, lifecycle, schema, or template used across domains | openxFactory |
| professional, regulatory, domain evidence, terminology, threshold, or approval rule | owning DomainxFactory |
| domain specialization of a neutral hook | DomainxFactory thin overlay |
| IT operations policy or privileged system execution | OpsxFactory |
| software-engineering-specific execution | codexFactory |
| installer, host, or runtime implementation | owning install/runtime repository |
| root composition, submodule pin, or release assembly only | xFactory aggregation repository |

When ownership remains contested, the claim stays in the routing record with
`disposition: unresolved`; it is not silently assigned to the most convenient
repository.

## Organize Gate

At the organize gate:

1. deduplicate claims and assign claim IDs;
2. classify neutral, domain, installation, runtime, and aggregation concerns;
3. select an owner and target capability for each routed claim;
4. create or update the destination staging artifact;
5. record `Source Idea IDs`, Claim IDs, and routing-record pointers in each
   destination;
6. update the source brainstorm with every extraction destination; and
7. leave unresolved claims in the routing record.

Neutral claims enter `openxFactory/ideation/staging/<topic>/`. Domain claims
enter the owning `DomainxFactory/ideation/staging/<topic>/`. Claims do not need
to enter staging at the same time.

## Cross-Repository Provenance

Git cannot preserve a single file move across separate repositories. The
routing contract therefore preserves provenance explicitly:

```yaml
source:
  repository: xFactories/MedxFactory
  path: ideation/brainstorm/omni-clinic-hosting.md
  revision: <full commit>
routing_record:
  repository: openxFactory
  path: ideation/brainstorm/cross-domain/XFI-2026-001/routing.yaml
  revision: <full commit>
```

Repository ID `xFactory` denotes the aggregation root; every other repository
ID is the exact aggregation-relative `.gitmodules` path and resolves through
its gitlink. Paths are POSIX repository-relative paths; absolute paths and
traversal are invalid.
`pending_capture` is permitted only for an intake source. Organize and proposal
gates require committed, resolvable revisions, including referenced pinned
install/runtime repositories.

The source brainstorm is retained as design history. If all active thinking is
superseded, it may move to the appropriate terminal document status with links
to its successors; it is never deleted while another artifact cites it.

## Mid-Promotion Authority

Until neutral adoption completes:

- the originating domain remains authoritative for its domain-local meaning;
- openxFactory staging or a proposal owns only the proposed neutral skeleton;
- other domains treat routed claims as candidates, not adopted policy;
- the candidate register or routing record states promotion progress; and
- no consumer replaces its local behavior until the neutral artifact is
  promoted and the consumer re-pins and adopts it.

This follows the existing Domain-To-Neutral Promotion Process.

## Routing Record Shape

The machine-readable draft is
[idea-routing-record.template.yaml](idea-routing-record.template.yaml). The
YAML sidecar is canonical for routing state. The paired brainstorm document
and all destination artifacts reference it rather than copying its fields.

See [Metadata Application Matrix](metadata-application-matrix.md) for which
documents receive full routing records versus lightweight provenance headers.
See [Organizer And Sweep Contract](organizer-and-sweep-contract.md) for how
deterministic validation and semantic routing recommendations interact.

## Repository Responsibilities

| Repository | Responsibility |
|---|---|
| openxFactory | unclassified inbox, cross-domain routing records, neutral claims, routing contract and validation |
| DomainxFactory | domain-origin brainstorms, domain-owned claims, thin overlays, approval to surrender meaning |
| codexFactory | optional doc-engineering assistance for neutralization drafts |
| install/runtime repo | implementation-specific ideas and changes within its boundary |
| xFactory aggregation | composition and release effects only; no general idea backlog |

## Required Proposal Deltas

The proposal for this topic should:

1. add the `ideation-routing` capability;
2. extend `document-lifecycle` with the unclassified inbox and cross-domain
   routing hub;
3. define Idea ID, claim ID, scope, routing status, provenance, and disposition
   fields;
4. add the routing-record template and validator;
5. update every DomainxFactory ideation README and the shared domain starter
   with the capture-and-route rule;
6. bind routing to the Domain-To-Neutral Promotion Process and candidate
   register;
7. add doc-health checks for duplicate IDs, unresolved destinations, broken
   provenance, copied full routing records, and invalid aggregation placement;
8. add a distinct non-mutating ideation-organizer lane; and
9. define prospective mixed-domain routing migration without fabricating
   source metadata or historical records.

## Required Tests

- an unclassified idea can be captured without selecting a final owner;
- a known domain idea remains in its DomainxFactory;
- a domain-origin idea can create a cross-domain routing record without losing
  source authority;
- one idea can route different claims to neutral, domain, installer, and
  aggregation owners;
- duplicate Idea IDs and claim IDs are rejected;
- every routed claim resolves to a destination or explicit unresolved blocker;
- domain tags do not override repository ownership;
- cross-repository provenance resolves to source repo, path, and revision;
- staging artifacts identify their source claim IDs; and
- ordinary documents are not burdened with routing sidecars;
- current tags may enqueue routing review while stale tags are ignored;
- the semantic organizer cannot move, promote, or assign authority; and
- the aggregation repository rejects a general ideation backlog.

## Exit

Create an OpenSpec change, recommended ID `add-cross-factory-ideation-routing`,
that ratifies the inbox, routing record, claim splitting, provenance,
validation, and DomainxFactory adoption rules. At the proposal gate, move this
staged packet into:

```text
openspec/changes/add-cross-factory-ideation-routing/supporting-docs/
```

The proposal must preserve:

```yaml
origin:
  kind: staged
  id: openxFactory:staging:ideation-routing
  path: ideation/staging/ideation-routing
```

## Staging Packet

- [Metadata Application Matrix](metadata-application-matrix.md)
- [Organizer And Sweep Contract](organizer-and-sweep-contract.md)
- [Idea Routing Record Template](idea-routing-record.template.yaml)

Catalog-specific source material moved to the sibling
[`add-document-cataloging`](../../add-document-cataloging/) change during the
user-approved proposal split.
