code_surface: openxFactory, codexFactory, xFactory, DomainxFactories, omnigent-install, cloudpc-install
target_release: implemented

## Why

The document lifecycle assumes authors know an idea's final repository before
capturing it, but xFactory ideas frequently begin unclassified or expand from
one domain into neutral, cross-domain, installer, and runtime concerns. Without
a governed routing contract, teams either lose early thinking or copy mixed
brainstorms across repositories with ambiguous ownership and provenance.

## What Changes

- Add a capture-first, route-later ideation model with a neutral unclassified
  inbox in openxFactory and domain-local capture when ownership is known.
- Add durable Idea IDs and Claim IDs plus one canonical routing YAML sidecar for
  each unclassified, mixed, or cross-domain idea; ordinary documents keep their
  current lightweight lifecycle headers.
- Route mixed discussions claim-by-claim so neutral contracts, domain policy,
  installer behavior, runtime implementation, and aggregation effects retain
  distinct owners and provenance.
- Preserve domain-origin authority while neutral candidates progress through
  staging, proposal, promotion, and consumer adoption.
- Allocate routing IDs centrally in openxFactory and require destination-owner
  acceptance before a claim becomes routed.
- Add a deterministic `ideation-routing` doc-health family for schema,
  identifier, reference, destination, transition, aging, and provenance checks.
- Add a semantic ideation organizer that reviews qualifying brainstorms and
  produces non-authoritative ownership, claim-split, dependency, and
  destination recommendations; it cannot move, promote, delete, or approve
  content.
- Permit the organizer to consume current, authorized catalog entries from the
  separately promoted `document-cataloging` capability as optional selection
  signals; tags cannot create routing state or authority.
- Apply source handling policy and workload-specific host authorization before
  organizer dispatch and filter protected paths, inferred owners/destinations,
  summaries, and evidence on return.
- Update the shared ideation scaffold and every DomainxFactory guide with
  capture, routing, destination acceptance, disposition, and adoption rules.
- Reuse the neutral infrastructure-readiness result when that staged contract
  is promoted; this change defines only organizer-specific profile and
  capability assertions, not generic Cloud PC or outage policy.
- Keep `add-doc-health-semantic-sweep` and `add-document-cataloging` unchanged;
  implement this change after both archive so the organizer reuses the bounded
  worker pattern and doc-health adds routing as the fourteenth family without
  conflicting deltas.

## Capabilities

### New Capabilities

- `ideation-routing`: Defines unknown-owner intake, routing records, Idea and
  Claim IDs, claim-level ownership, cross-repository provenance, destination
  acceptance, organizer recommendations, and routing disposition authority.

### Modified Capabilities

- `document-lifecycle`: Adds the unknown-owner inbox and claim-level
  cross-domain routing transition before staging, including source retention,
  extraction records, and routed-claim provenance at proposal gates.
- `doc-health`: Adds deterministic ideation-routing validation as the
  fourteenth deterministic check family after document cataloging is promoted.
  Semantic organization remains a separate worker lane, not another semantic
  finding family.

## Impact

- **openxFactory:** routing requirements, schemas, templates, examples,
  lifecycle guidance, and doc-health delta.
- **codexFactory:** routing-record parser, deterministic checks, organizer
  selection, versioned prompt/output contracts, tests, and report integration.
- **xFactory aggregation:** nightly routing checks and conditional independent
  organizer dispatch; reports retain skips and recommendation evidence without
  treating recommendations as verdicts.
- **DomainxFactories:** known-domain capture, routing pointers, claim
  provenance, destination acceptance, and owner-authorized disposition;
  existing brainstorms receive no fabricated historical IDs.
- **omnigent-install and cloudpc-install:** one bounded `ideation-organizer`
  profile and workload-specific readiness assertions on the existing document
  analysis host; no additional Entra user or Cloud PC.
- **Compatibility:** ordinary documents need no routing sidecar; routing is
  prospective, and catalog signals remain optional inputs rather than routing
  authority.
