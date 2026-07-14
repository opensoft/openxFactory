# Cross-Factory Ideation Routing Adoption Guide

Status: ratified
Kind: process
Repository context: openxFactory
Ratified by: add-cross-factory-ideation-routing
Purpose: give an adopting DomainxFactory one place to see what the
capture-first cross-factory ideation routing convention means for its own
ideation area, entirely by reference to the requirements that own it.

## Scope

This guide is additive orientation for a DomainxFactory maintainer, not a new
contract of its own. Every rule it points to is owned by the
`add-cross-factory-ideation-routing` change's
[ideation-routing spec](../openspec/changes/add-cross-factory-ideation-routing/specs/ideation-routing/spec.md),
its
[document-lifecycle delta](../openspec/changes/add-cross-factory-ideation-routing/specs/document-lifecycle/spec.md),
and its
[doc-health delta](../openspec/changes/add-cross-factory-ideation-routing/specs/doc-health/spec.md);
this guide only names which requirement to read and which files in your own
repository it applies to. `scripts/apply-domain-starter.py` seeds every new
DomainxFactory's `ideation/README.md` with a compact pointer to this guide so
the convention is inherited, never re-authored (spec requirement *Prospective
compatibility and migration*, scenario "A new DomainxFactory is scaffolded").

## What the capture-and-route convention means for your repository

### 1. Known-domain capture stays with you

An idea already known to be yours stays in your own
`ideation/brainstorm/` — it is never centralized. The spec's *Capture-first
repository routing* requirement is what draws that line: an unknown-owner idea
is captured in the openxFactory unclassified inbox, a clearly neutral or
already cross-domain idea in openxFactory's brainstorm area, and a
known-domain idea in your DomainxFactory. The xFactory aggregation repository
hosts no general ideation backlog. Nothing about this convention forces a
domain idea out of your repository or requires you to guess a neutral owner
before capture.

### 2. Cross-domain and unknown-owner routing lives in openxFactory

When an idea's owner is genuinely unknown, or it spans several domains,
routing is coordinated from openxFactory, not duplicated here. The spec's
*Canonical routing identity and record* and *Structured repository references
and resolvable provenance* requirements own the durable `XFI-<year>-NNN`
Idea-ID grammar, the `-C<NN>` Claim-ID grammar, the single central allocation
ledger at
[`ideation/routing-index.yaml`](../ideation/routing-index.yaml), and the
structured repository/path/full-revision provenance that survives a move
across separate repositories. The machine-readable shapes are the four
schemas under
[`contracts/schemas/`](../contracts/schemas/) —
`xfactory-idea-routing-reference.schema.yaml`,
`xfactory-idea-routing-record.schema.yaml`,
`xfactory-ideation-routing-index.schema.yaml`, and
`xfactory-ideation-organizer-recommendations.schema.yaml` — with worked valid
and invalid instances under
[`examples/ideation-routing/`](../examples/ideation-routing/). A domain-origin
idea that later expands keeps its original brainstorm as design history; the
openxFactory routing record references it without copying it or acquiring its
domain authority (spec requirement *Routing coordinates but does not transfer
authority*).

### 3. Destination-owner acceptance is your authority

When a claim is proposed for your domain, your Domain Hermes is the
destination authority that accepts or declines it. The spec's *Routing and
claim transition integrity* requirement is what forbids a claim from reaching
`routed` without a named accepted owner, target capability, structured
destination, and acceptance actor/time/evidence — and keeps an unaccepted
claim `unresolved` with an explicit blocker rather than silently assigned to a
convenient repository (scenarios "Proposed owner has not accepted" and
"Ownership remains disputed"). A domain tag, candidate-owner field, or
document-catalog classification naming your repository never substitutes for
that acceptance (requirement *Document catalog signals are routing
recommendations only*).

### 4. Only owner-authorized disposition moves a claim

Routing state changes only through reviewed, owner-authorized transitions. The
spec's *Non-mutating semantic ideation organizer* requirement is what confines
the organizer to recommendations carrying committed evidence, numeric
confidence, alternatives, ambiguity, and a `pending_review` disposition — it
may not move, promote, approve, or assign authority, resolve a disputed claim,
or mutate the canonical routing record. An authorized owner accepting,
editing, or rejecting a recommendation is what lets lifecycle tooling record
the decision (scenario "Recommendation is reviewed"). The deterministic
`ideation-routing` doc-health family (the fourteenth family, implemented in
codexFactory per the doc-health delta) reports duplicate IDs, illegal
transitions, unresolved destinations, broken provenance, copied records, and
misplaced backlogs without ever making a routing decision of its own.

## What this guide does not grant

Nothing in this guide, and no routing record, organizer recommendation, domain
tag, or candidate-owner field, replaces the domain-neutral candidate register,
OpenSpec ratification, destination-owner acceptance, Domain Hermes review, or
the consumer re-pin and overlay-replacement adoption gates. A routed
`neutral_candidate` claim still follows the full
[Domain-To-Neutral Promotion Process](domain-to-neutral-promotion-process.md)
before it promotes.

## Prospective compatibility

Existing brainstorms in your repository remain valid with no fabricated
historical Idea IDs, Claim IDs, or transitions. Routing metadata becomes
required only when an existing item is deliberately changed into an
unclassified, mixed, cross-domain, or claim-split state, or when an authorized
migration records current committed evidence (spec requirement *Prospective
compatibility and migration*). Deterministic validation never reports an
ordinary document merely for lacking routing metadata.

## Related Documents

- [ideation-routing spec](../openspec/changes/add-cross-factory-ideation-routing/specs/ideation-routing/spec.md)
  — the owned capture, identity, transition, classification, provenance,
  acceptance, organizer, and compatibility rules this guide only points into.
- [Ideation Work Area](../ideation/README.md) — the captured/organized pipeline
  the routing convention extends.
- [Document Lifecycle](document-lifecycle.md#cross-factory-ideation-routing) —
  the lifecycle spine routing coordinates but never replaces.
- [Doc-Health Contract](doc-health.md) — the deterministic families, including
  the fourteenth `ideation-routing` family.
- [Domain-To-Neutral Promotion Process](domain-to-neutral-promotion-process.md)
  — the candidate-register and adoption gates a routed neutral claim still
  completes.
- [`contracts/schemas/`](../contracts/schemas/) routing schemas,
  [`ideation/routing-index.yaml`](../ideation/routing-index.yaml) central
  ledger, [`scripts/validate-ideation-routing.py`](../scripts/validate-ideation-routing.py)
  validator, and [`examples/ideation-routing/`](../examples/ideation-routing/)
  worked instances.
