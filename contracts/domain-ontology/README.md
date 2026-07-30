# domain-ontology Contract

Status: ratified
Ratified by: add-domain-ontology-layer (approved 2026-07-29; registered in
`contracts/manifest.yaml` + `contracts/CHANGELOG.md` at the next additive
bundle cut, per [Contract Versioning Policy](../../docs/contract-versioning-policy.md)
and the Contracts Pending Realization convention)

The neutral ontology meta-contract: how the xFactory semantic kernel and
every DomainxFactory ontology package are shaped, identified, validated,
published, and consumed — **meaning, never authority**. openxFactory owns
the kernel (`core/`); Domain Hermes owns each domain package in its
DomainxFactory repository; Tenant Hermes binds local terms; Subject Hermes
instantiates and never publishes. The semantic plane describes; the control
plane (grants, consent, approvals, bindings) decides — enforced
structurally by closed shapes and the canonical validator, not by prose.

## The eighteen kinds

| Schema | Kind | Carries |
| --- | --- | --- |
| `ontology-package-manifest.schema.yaml` | `xfactory_ontology_package_manifest` | identity, namespace, stewards, exact kernel import, digest-covered inventory, compatibility line, kernel adoption evidence |
| `ontology-concepts.schema.yaml` | `xfactory_ontology_concepts` | concept registry: immutable IDs, labels/aliases, definitions, acyclic multi-parent specialization |
| `ontology-relations.schema.yaml` | `xfactory_ontology_relations` | relation registry with exact domain/range and deterministic characteristics |
| `ontology-external-mappings.schema.yaml` | `xfactory_ontology_external_mappings` | by-reference external code mappings; no mirrored content, license-gated quoting |
| `ontology-source-inventory.schema.yaml` | `xfactory_ontology_source_inventory` | registered authorities with license class, permitted use, review deadline |
| `ontology-candidate-record.schema.yaml` | `xfactory_ontology_candidate_record` | append-only proposed changes; model extraction carries run identity; steward-decided dispositions |
| `ontology-release-record.schema.yaml` | `xfactory_ontology_release_record` | publication/adoption record naming the accountable steward |
| `ontology-migration-map.schema.yaml` | `xfactory_ontology_migration_map` | breaking/retiring term dispositions across a compatibility line |
| `semantic-context.schema.yaml` | `xfactory_semantic_context` | bounded, closed-or-truncated term subset with exact pins; the Omnigent worker-scope seam |
| `ontology-quality-report.schema.yaml` | `xfactory_ontology_quality_report` | computable per-release quality signals under the privacy aggregation floor |
| `ontology-stewardship-policy.schema.yaml` | `xfactory_ontology_stewardship_policy` | council, source-review cadence, the seven mode workflows, trigger thresholds, quality gate, standing privacy floor (inventoried content) |
| `ontology-maintenance-input.schema.yaml` | `xfactory_ontology_maintenance_input` | governed, floor-respecting maintenance observations; `as_of` is data, never a clock |
| `ontology-maintenance-report.schema.yaml` | `xfactory_ontology_maintenance_report` | append-only record of each trigger evaluation; a clean check is itself evidence |
| `semantic-context-profile.schema.yaml` | `xfactory_semantic_context_profile` | the worker-scoped term subset per archetype/class (inventoried content); compiled per worker by the context compiler — the Omnigent seam |
| `ontology-review-fixtures.schema.yaml` | `xfactory_ontology_review_fixtures` | labeled positive/negative/representative review cases per term (starter-seeded, steward-curated) |
| `ontology-coverage-gap-report.schema.yaml` | `xfactory_ontology_coverage_gap_report` | starter-refreshed inventory of unanswered/unresolved ontology scope |
| `ontology-starter-provenance.schema.yaml` | `xfactory_ontology_starter_provenance` | the STARTER marker: which starter version generated the scaffold, ontology-aware |
| `ontology-consumer-impact-report.schema.yaml` | `xfactory_ontology_consumer_impact_report` | breaking/retiring impact: affected domain-owned terms + consumer pins (never tenant bindings) |

Package layout: `package.yaml` + inventoried CONTENT files (concepts,
relations, mappings, sources, migration maps, profiles, stewardship
policy), digest-closed; RECORD files (candidates, releases, contexts,
quality/maintenance/coverage/consumer-impact reports, review fixtures,
starter provenance) sit BESIDE the inventory — they reference the package
digest, so covering them would be self-referential. Superseded versions
are retained under `retained/<version>/` while referenced; since the
self-retention release flow, each release also snapshots the bytes it
publishes at publication time, so history never depends on later edits.
YAML dates must be quoted strings.

## The kernel

`core/` is the xFactory semantic kernel package (`xf/core`, DRAFT):
24 concepts and 9 relation primitives, each naming the contract that owns
its runtime shape. The ratified bootstrap scenario allows `pending`
adoption while the kernel is draft; every concept AND relation now records
`evidenced` adoption with two independent resolvable adopters (deduped by
identity — two copies of one adopter count once). The inventory
behind every owner pointer is
[docs/domain-ontology-semantic-decisions.md](../../docs/domain-ontology-semantic-decisions.md).

## Canonical validator

```
python3 scripts/validate-domain-ontology.py            # self-test: kernel + examples
python3 scripts/validate-domain-ontology.py .          # + repo scan and content-manifest cross-check
python3 scripts/validate-domain-ontology.py --determinism
python3 scripts/validate-domain-ontology.py --readiness <pkg-dir>   # ontology_ready | domain_scaffold_required
```

`scripts/ontology-compile-context.py` compiles bounded semantic contexts
(closure or itemized truncation, tenant-binding fail-closed, no
unrestricted mode, deterministic digests); the memory-gateway packet
contracts carry the block and `validate-memory-gateway.py` preflights it
before provider I/O. Stewardship tooling: `scripts/ontology-maintenance.py` evaluates the policy
triggers over a governed input and opens mode-mapped candidates append-only
(a clean run records the completed check, and an identifier-shaped value
anywhere in the input fails the run closed before any bytes land);
`scripts/ontology-release.py` performs the governed version transition —
accountable-steward gate (worker/agent identities prepare, never publish),
migration AND consumer-impact evidence for breaking/retiring, the policy
quality gate (a report is always required; each `--quality-exception
SIGNAL=REF` releases exactly one signal's threshold with its recorded
review — there is no blanket exception), byte-true self-retention of the
published version at publication, and a new compatibility line on
breaking. Exercised end-to-end by `scripts/test-ontology-stewardship.py`.

Stable finding codes (each with at least one indexed negative fixture):

| Code | Rule |
| --- | --- |
| ONT-DIGEST | inventory/package digest drift or uninventoried content file — fail closed |
| ONT-INVENTORY-FOREIGN | non-ontology-family document inventoried (incl. mirrored terminologies) |
| ONT-NAMESPACE | term outside the package namespace; package_id disagreement |
| ONT-ID-DUP | duplicate identifier |
| ONT-LABEL-COLLISION | label/alias collision within the namespace |
| ONT-PARENT-MISSING / ONT-CYCLE | unresolvable parent; specialization cycle |
| ONT-RELATION-RANGE | unresolvable relation domain/range or mapping concept |
| ONT-KERNEL-IMPORT | missing/mismatched exact kernel import |
| ONT-ADOPTION | published kernel without two resolvable adopters per term |
| ONT-SOURCE-MISSING | unregistered source/steward reference |
| ONT-MAPPING-UNREGISTERED | mapping to an unregistered or non-external system |
| ONT-LICENSE | quoted definition without a `definition_quote` permitted use |
| ONT-COMPAT / ONT-RETENTION | missing previous/migration map; missing retained bytes |
| ONT-PRIVATE | subject-instance URNs or endpoint-shaped values in content |
| ONT-AUTHORITY-FIELD / ONT-AUTHORITY-TARGET | reserved authority field; authority-plane instance reference |
| ONT-CANDIDATE / ONT-RELEASE | run-identity, steward-disposition, and accountable-publication rules |
| ONT-FLOOR / ONT-QUALITY | aggregation-floor and computable-signal rules |
| ONT-CONTEXT-CLOSURE / ONT-CONTEXT-PIN / ONT-BINDING | subset closure, pin agreement, tenant-binding agreement |
| ONT-POLICY / ONT-MAINTENANCE / ONT-PROFILE | council/quorum resolution; fired-trigger completeness; profile term resolution |
| ONT-MANIFEST-PIN | content-manifest `domain_ontology` target missing or invalid |
| ONT-SCHEMA | any other schema conformance failure |

## Fixture index

Positive (`examples/`): `medx-minimal/` (medical specialization with a
restricted-license by-reference mapping and beside-package release,
candidate, worker-scoped context, quality report), `codex-minimal/`
(engineering specialization of the same kernel), `generated-scaffold/`
(starter-shaped draft), `kernel-adoption-pair/` (a PUBLISHED kernel whose
domain_package adopter resolves through the shared package registry —
proving kernel publication satisfiable and keeping the registry live under
fixture coverage), `roster-twin-pair/` (two same-id packages with distinct
digests and rosters — loose records resolve by exact digest, never first
match), plus the retained MedxFactory/codexFactory pilot
packages under `pilots/` (full release history, retained versions, worker
contexts — see `docs/domain-ontology-pilot-report.md`). Negative (`examples/negative/`): 44 fixtures, one
per finding rule — including two paired-revision cases (a parent added on
a published concept and a relation range widened, each declared additive
against retained prior bytes), a prose identifier/endpoint leak, a
duplicated kernel adopter counted once, a domain package squatting the
kernel namespace, and two loose worker-attributed release records whose
packages ARE in the tree (the roster rule, not the orphan rule — one
single-package, one requiring digest disambiguation between the twins) —
each declaring `# expected_failure:` (and, where a code covers several
rules, `# expected_failure_detail:`); the self-test fails closed if a
positive fails, a negative stops failing for its declared reason, or the
corpus drops below its pinned minimum of 44. Repo scans run in their own
registry scope: a consumer's loose records resolve against the consumer's
packages only, never against these fixtures.

## What this family is not

Not a taxonomy (factory/subject kinds), not a record schema, not policy,
not a knowledge graph store, and never an authorization surface: no
ontology field can carry an effect or permission, no term can reference an
authority-plane record instance, and semantic context never widens a
worker's permission matrix.
