# Domain-Ontology Guide

Status: ratified
Kind: process
Ratified by: [add-domain-ontology-layer](../openspec/changes/add-domain-ontology-layer/proposal.md) (task 8.2)
Repository context: openxFactory
Purpose: the one-stop walk through the ratified ontology system — the
semantic/control-plane separation, the generation pipeline, Domain Hermes
stewardship, maintenance triggers, the compatibility rubric, the migration
path, and provider-neutral runtime consumption — with pointers to the
machine surfaces that enforce each part. The contracts are canonical
(`contracts/domain-ontology/`); this guide orients, never overrides.

## 1. The semantic plane never crosses the control plane

Ontology is meaning, not authority:

```text
taxonomy        classifies a domain or template
schema          validates record shape
ontology        defines concepts, relationships, valid specialization
knowledge graph stores scoped instances, claims, evidence
policy          determines what actors may do
```

The separation is STRUCTURAL, not prose: every family shape is closed
(`additionalProperties: false` — an `effect`/`permission`/`grant` field
cannot exist), the canonical validator rejects reserved authority field
names and authority-plane instance references
(`ONT-AUTHORITY-FIELD`/`ONT-AUTHORITY-TARGET`), and the memory gateway
preflights every packet-borne semantic context before provider I/O. No
classification, equivalence, traversal, or inference result grants
access, approves work, promotes data, creates bindings, or authorizes
external action — those continue through the existing grant, consent,
approval, and promotion contracts unchanged.

Ownership (four strata): openxFactory owns the kernel (`xf/core`, 24
concepts + 9 relation primitives, each naming its owning contract);
Domain Hermes owns each domain package and its quality; Tenant Hermes
binds local codes (never redefining the published package); Subject
Hermes instantiates privately and never publishes. The full term-by-term
inventory, collision/leak registers, identifier grammar, and recorded
deferrals: [domain-ontology-semantic-decisions.md](domain-ontology-semantic-decisions.md).

## 2. Generation: the ontology-aware starter (v13)

A new domain's pre-run answers (`ontology:` section — subject/focal-item
kinds, workflows, activities, journey states, outcomes, interventions,
evidence types, external terminologies WITH license classes, governed
sources, boundaries, stewards, reviewers) deterministically seed
`hermes/domain/ontology/`: draft package manifest with digest-true
inventory, concepts specializing their kernel parents, a registered
source inventory, the stewardship policy, a refreshed coverage-gap
report, synthetic labeled review fixtures, the STARTER provenance marker,
and an explicit `content-manifest.yaml` declaring `domain_ontology`.
Placeholders are never seeded — each becomes an Unresolved row keeping
the draft non-publishable. Reruns never overwrite domain-owned content
(differences are Conflicts rows; the manifest digests the PRESERVED
bytes). Model-assisted extraction enters only through
`--ingest-candidates`: registered sources, an extraction-run identity,
append-only candidates, dispositions never resurrected, and a proposal
colliding with a structured import auto-records as a conflicting
candidate that blocks readiness until dispositioned.

## 3. Stewardship: Domain Hermes decides, machines propose

The inventoried stewardship policy carries the council (members resolved
against the manifest roster), source-review cadence, the seven mode
workflows (`seed extend refresh reconcile correct deprecate retire`,
each with required inputs, review evidence, outputs, blocked states),
trigger thresholds, the quality gate, and the standing aggregation
floor. Candidates are append-only; acceptance requires a steward
disposition; publication (`scripts/ontology-release.py`) requires an
ACCOUNTABLE steward whose identity is human or council — a worker/agent
identity can prepare everything and publish nothing (enforced by the
tool AND validator fixtures). MedxFactory's realized instance: the
dedicated ontology-steward persona, MxD-MRR wearing the ontology review
seats, `high_impact_requires: [licensed_human]`.

## 4. Maintenance: triggers open candidates, evidence either way

`scripts/ontology-maintenance.py` evaluates a governed input (`as_of` is
data, never a clock) against the policy: source expiry, unknown-term and
mapping-failure thresholds, repeated low-confidence classification,
workflow drift, sub-domain requests, appeals, and reviewed promotion
candidates each open a mode-mapped candidate append-only; a below-floor
term entry fails the run closed; and a clean evaluation writes the
append-only maintenance report that IS the evidence the check ran while
the active package and pins stayed untouched.

## 5. Compatibility: classified edges, never taste

`initial | additive | clarifying | breaking | retiring`, with the edges
decided: parent add/remove on a published concept — breaking; relation
domain/range change in EITHER direction — breaking; identity reuse —
breaking with a new identifier; alias/label collision — a validation
error, not a class. Breaking/retiring ships a migration map (which joins
the digest-covered inventory), starts a new compatibility line, and
requires explicit consumer re-pins. The validator compares revisions
against retained prior bytes, so a misdeclared edge is caught
(`ONT-COMPAT`). The kernel follows the same rubric; only openxFactory
classifies kernel revisions.

## 6. Migration, retention, rollback

Published bytes stay retrievable at their digest under
`retained/<version>/` while referenced (`ONT-RETENTION` on deletion);
two pins may coexist during a migration window when every artifact
records its exact pin; rollback re-pins new work and never rewrites a
recorded identity. Existing domains migrate additively: the starter's
`--dry-run` is the report-only path; adoption lands through each
consumer's own governed change
([domain-ontology-adoption-handoff.md](domain-ontology-adoption-handoff.md)).
Readiness (`validate-domain-ontology.py --readiness`) keeps a scaffold
`domain_scaffold_required` until the package validates clean, publishes
via an accountable release, carries no placeholders, ships its policy,
and satisfies the quality gate against the CURRENT digest.

## 7. Runtime consumption: bounded, pinned, provider-neutral

No surface issues an unrestricted ontology corpus.
`scripts/ontology-compile-context.py` compiles purpose-bounded semantic
contexts — closed over specialization ancestors and relation endpoints,
or itemized-truncated where the profile allows — with exact kernel and
package pins, tenant bindings failing closed on any mismatch, and
retired packages refusing new compilation. Worker-scoped profiles
(`xfactory_semantic_context_profile`, per archetype or class) are the
Omnigent seam: one small digest-pinned context per worker, permission
matrix untouched. Compiled projections (graph, relational, vector,
JSON-LD/RDF export) are derivative, reproducible from the pinned
package, and unable to change canonical meaning — rebuilding on a
different provider leaves identifiers, conformance results, and context
digests unchanged. The memory gateway carries the context in its packet
contracts and preflights it before provider I/O.

## Proof surfaces

`validate-domain-ontology.py --determinism` (8 positive units incl. the
Medx/codex pilots and the published-kernel adoption pair, 43 indexed
negatives),
`test-domain-starter-ontology.py`, `test-ontology-stewardship.py`,
`test-semantic-context.py`, the overlay validator's generated-domain
completeness rule, and the pilot record
([domain-ontology-pilot-report.md](domain-ontology-pilot-report.md)).
