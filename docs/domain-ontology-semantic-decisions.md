# Domain-Ontology Semantic Inventory And Decisions

Status: ratified
Kind: register
Ratified by: [add-domain-ontology-layer](../openspec/changes/add-domain-ontology-layer/proposal.md)
Repository context: openxFactory
Purpose: the realization record of change tasks 1.1–1.6 — the semantic
inventory behind the xFactory kernel (`contracts/domain-ontology/core/`),
the collision/leak/gap registers the kernel must not repeat, the identifier
grammar, the compatibility rubric, the canonical-representation ruling, and
the recorded cross-domain deferral. The kernel's machine truth lives in the
core package; this register records WHY each term points where it points.

## 1. Semantic inventory (task 1.1)

One row per kernel term: the authoritative owner its `owning_contract`
field cites, and the second surface that will serve as adoption evidence at
kernel publication (two resolvable adopters per term; `pending` while the
kernel is draft, resolved by the MedxFactory/codexFactory pilots).

| Term | Owning contract (cited) | Second surface (adoption candidate) |
| --- | --- | --- |
| subject | `contracts/policies/layer-vocabulary.yaml` | promoted `layer-vocabulary` spec; `neutral-job-envelope` `subject_ref` |
| tenant | `contracts/policies/layer-vocabulary.yaml` | `docs/party-ladder.md` rung 1; client-content `tenant_isolated` |
| domain | `contracts/policies/layer-vocabulary.yaml` | `hermes-domain-overlay` / `omnigent-domain-overlay` domain blocks |
| workflow | `contracts/schemas/xfactory-workflow.schema.yaml` | `workflow_ref` across 6 families (job envelopes, memory gateway) |
| activity | `docs/domain-ontology-semantic-decisions.md` (§4 — first definition) | none yet; the kernel definition is the seed |
| state | `docs/xfactory-domain-factory-model.md` | six runtime state machines (see §2) |
| transition | `docs/xfactory-domain-factory-model.md` | lifecycle events (`from_state`/`to_state`); idea-routing transition graphs |
| gate | `contracts/schemas/xfactory-workflow.schema.yaml` | promoted `workflow-gate-contract` spec (DTN-002) |
| artifact | `contracts/hermes-runtime/artifact-record.schema.yaml` | `artifact_refs` in job envelopes; gate-action artifacts |
| focal_item | `docs/xfactory-domain-factory-model.md` | promoted `neutral-job-envelope` `focal_item_ref` |
| interaction | `docs/xfactory-domain-factory-model.md` | memory-gateway fill mode "Direct customer interaction" |
| journey_state | `docs/xfactory-domain-factory-model.md` | promoted `layer-vocabulary` spec names it a Subject Hermes ownership item |
| outcome | `docs/xfactory-domain-factory-model.md` | `outcome_observation` in the fill taxonomy |
| intervention | `docs/xfactory-domain-factory-model.md` | `intervention_class` in the client product-service scaffold |
| source | `contracts/memory-gateway/vocabularies.yaml` | `expert-knowledge-source.schema.yaml`; source-authority rail |
| claim | `contracts/memory-gateway/vocabularies.yaml` (`source_claim` port) | `docs/customer-hermes-memory-model.md` §8 |
| evidence | `contracts/memory-gateway/vocabularies.yaml` (`evidence_graph` port) | `docs/traceability-model.md` edge contract |
| hypothesis | `contracts/schemas/xfactory-derived-model-conformance.schema.yaml` | promoted `governed-derived-model` spec; installation-spine rule |
| observation | `docs/customer-hermes-memory-model.md` (`claim_type: observation`) | fill-taxonomy telemetry row |
| knowledge_atom | `contracts/memory-gateway/vocabularies.yaml` (`memory_item` port) | `docs/knowledge-lifecycle-model.md` Root Truth atom |
| policy | `openspec/specs/roles-authority-model/spec.md` | `contracts/hermes-runtime/approval-decision-policy.schema.yaml` |
| consent | `contracts/memory-gateway/consent-profile.schema.yaml` | avatar-client consent registries; DTN-016 |
| authority | `contracts/hermes-runtime/authority-grant.schema.yaml` | promoted `roles-authority-model` spec |
| approval | `contracts/hermes-runtime/approval-decision.schema.yaml` | overlay `approval_scope_kinds`; job-envelope approval blocks |
| trace_reference | `contracts/hermes-runtime/traceability-edge.schema.yaml` | `trace_refs` (job run v2, required); memory context packets |

## 2. Collision and overload register (task 1.2)

The kernel exists to name ONE meaning per term; these are the recorded
overloads the kernel definitions disambiguate against. Contracts listed
here are REFERENCED, never restated.

- **state** — the most overloaded token: six independent runtime state
  machines (installation/stack, layer, principal, topology projection,
  ideation register, avatar media) plus lease/dispatch/facet/tag/readiness
  state fields and nine-plus `*_state`/`*_status` families in docs. The
  kernel's `state` is the abstract governed lifecycle condition;
  `journey_state` specializes it for the subject journey. Note
  `client_infrastructure_request` deliberately says `status` and pushes
  overdue/escalation into `conditions[]` — the one contract that resisted
  overloading.
- **source** — six senses: authority tier, source claim, expert knowledge
  source, idea source document, trace-edge endpoint, operation origin. The
  kernel's `source` is the knowledge origin; the trace-edge `source`
  endpoint is graph topology and stays with the traceability contract.
  Three L0–L5 authority ladders with drifting labels exist
  (`notebooklm-source-workspaces`, `customer-hermes-memory-model`,
  `xfactory-domain-factory-model`) — a reconciliation candidate.
- **authority** — seven senses (grant, ownership boundary, epistemic tier,
  disposing role, approver identity, layer scope, consent basis). Kernel
  `authority` = the granted, revocable power to act (the grant contract);
  everything epistemic belongs to source-authority.
- **outcome** — five vocabularies: subject outcome (kernel sense), gate
  outcome (`accepted/rejected/deferred`), avatar session outcome (7
  values), child-ack outcome, readiness check outcome. DTN-002's register
  entry still says "gate outcome vocabulary" while the promoted spec
  renamed it "blocking vocabulary" — recorded, not fixed here.
- **gate** — workflow gate record vs human gate console vs dispatch
  handling gate vs speech gate vs structural GitHub gate. Kernel `gate` is
  the workflow checkpoint; the console is a surface over lifecycle
  transitions, not a second meaning.
- **artifact** — content-addressed runtime record vs installation artifact
  families vs governance evidence artifact vs NotebookLM studio artifact.
  Kernel `artifact` is the produced, digest-addressable work product (the
  runtime record is its canonical shape).
- **claim** — source claim vs ideation routed Claim ID vs attestation
  claims vs installation workflow-evidence claim. Kernel `claim` is the
  source-attributed statement; the ideation Claim ID is a work-routing
  object and never enters the semantic plane.
- **domain** — seven senses; the two that matter here: the Hermes layer
  (kernel `domain`) and a relation's `domain/range` (ontology structure).
  The family schemas use `domain` only inside relation definitions, where
  the ontological reading is unambiguous and standard.
- **subject** — five senses including the worker-enrollment actor
  (`subject.class: host|engineer`) and the client-infrastructure managed
  target. Kernel `subject` is the served party; the enrollment sense is a
  record-local actor field.
- **interaction** — subject↔focal-item contact (kernel sense) vs avatar
  `interaction_mode` transport modality vs UI interaction surface.
- **observation ↔ signal** — used interchangeably in the fill taxonomy;
  kernel standardizes on `observation` and treats "signal" as prose.

## 3. Domain-leak register (task 1.2)

Leaks found in supposedly neutral surfaces, recorded so the kernel and the
pilots do not import them (repair rides later changes, not this one):

- `contracts/memory-gateway/vocabularies.yaml` `knowledge_scopes` — five of
  eight values are a per-vertical product list (`clinical_guideline`,
  `ops_runbook`, `accounting_policy`, ...), validator-required.
- `contracts/schemas/xfactory-domain-stack.schema.yaml` isolation scopes
  (`per_patient`, `per_campaign`, `per_ledger`, ...), enforced by
  `scripts/validate-domain-factory.py`.
- The v1 job envelope's engineering nouns (`epic_id`, `feature_id`,
  `repository{...}`) — v2 explicitly repudiates them.
- `docs/customer-hermes-memory-model.md` exemplifies every neutral object
  with clinical values (36 "patient" occurrences outside the labeled Medx
  section).
- Promoted `roles-authority-model` carries a GitHub-named requirement;
  "Merge Master/Council" are version-control nouns as neutral role names.
- The canonical layer vocabulary is enforced NOWHERE: no validator reads
  `layer-vocabulary.yaml`, while three validators hardcode the LEGACY
  `customer|client|domain` roles. Repair candidate for the
  layer-vocabulary machine migration (staged, dormant).
- Enum drift: `guardian_authority_modes` (5 values) vs consent-profile
  `authority_basis` (4).

## 4. Gaps and adjudications (task 1.2)

- **activity** — defined NOWHERE before this register. Kernel definition
  (first definition of record): a bounded step of work inside a workflow,
  performed by an authorized actor and producing artifacts or outcomes.
  Adjudication against near-synonyms: an activity is the semantic work
  step; a `job`/`job_run` is the execution envelope that may realize one;
  an `interaction_event` is the subject-side touchpoint an activity may
  produce; worker archetype verbs are role taxonomy, not activities.
- **knowledge_atom** — the corpus says `memory item` (subject tier,
  defined) and `Root Truth atom` (domain tier, draft, zero adopters).
  Kernel `knowledge_atom` is the layer-neutral abstraction both
  specialize; aliases record both corpus names. The
  memory-item↔root-truth-atom promotion relation is exactly the reviewed
  promotion path the lifecycle spec governs.
- **journey_state vs current_state_snapshot** — two subject-belief
  snapshots in two neutral docs, never reconciled
  (`journey_state_snapshot` in the interaction model,
  `current_state_snapshot` in the memory model). The kernel takes
  `journey_state` as the condition and leaves snapshot records to the
  memory model; reconciling the two record shapes is pilot input.
- **focal_item regression** — the definition lives in a draft doc while
  the promoted field (`focal_item_ref`) lost its carrier in the v2 job
  envelope. Recorded; the ontology package now carries the definition
  durably.
- **trace edge `relation` is unconstrained** — the runtime traceability
  edge takes any `canonical_id` as its relation, and
  `docs/traceability-model.md` §"Core Relations" names eleven relations
  the schema does not enforce. The kernel's relation registry is the
  natural future vocabulary source — a named follow-on candidate, not
  in this change's scope.

## 5. Identifier grammar and label separation (task 1.3)

- **Grammar:** `xf/<namespace>/<term>` with lowercase `[a-z0-9_]`
  segments; deeper segments allowed (`^xf/[a-z0-9_]+(/[a-z0-9_]+)+$`).
  The kernel owns `xf/core/...`; each DomainxFactory owns
  `xf/<domain-slug>/...` (`medx`, `codex`, `ledgerx`, `opsx`, `adx`,
  or the starter-assigned slug). A package's `namespace` equals its
  `package_id`, and every term in the package must live under it.
- **Immutability:** identifiers never change or get reused; labels,
  aliases, and definitions evolve without changing identity. Preferred
  labels and aliases are unique (case-insensitive) within a package
  namespace; a collision is a validation error, never a resolution choice.
- **Positive examples:** `xf/core/subject`; `xf/medx/patient` with label
  "Patient" and alias "pt" added later as `clarifying`.
- **Negative examples:** `xf/other/thing` inside package `xf/negx`
  (namespace escape); two terms with label/alias "Thing" (collision);
  reassigning `xf/medx/patient` to mean a guardian (identity reuse —
  breaking, new identifier + migration required). Each is an indexed
  fixture under `contracts/domain-ontology/examples/negative/`.

## 6. Compatibility rubric, retention, and rollback (task 1.4)

Classes: `initial` (first line), `additive`, `clarifying`, `breaking`,
`retiring`. Edges, classified rather than left to taste: parent add or
remove on a published concept — breaking; relation domain/range change in
either direction — breaking; non-colliding alias — clarifying; alias/label
collision — invalid (not a class); external-mapping refresh — a mapping
revision classified by its effect on valid classification. Breaking and
retiring revisions require a migration map, a new compatibility line, and
explicit consumer re-pins. Every published version's bytes stay
retrievable at their recorded digest while referenced (`retained/<version>/`
in the canonical layout); rollback re-pins new work and never rewrites a
recorded identity; two pins may coexist during a migration window when
every artifact records the exact pin it used. The kernel follows the same
rubric; a breaking kernel revision starts a new kernel line and cascades
only through reviewed domain revisions.

## 7. Canonical representation (task 1.5)

Ratified: YAML-serialized JSON-Schema contracts under
`contracts/domain-ontology/`, digest-pinned per the family conventions,
validated by `scripts/validate-domain-ontology.py`. JSON-LD/RDF export is
optional derivative interoperability — stable IDs and explicit relations
keep it addable without changing canonical meaning — and no first-release
evidence justified including it now. Compiled projections (graph,
relational, vector, in-memory) are derivative and identify their source
package digest.

## 8. Cross-domain shared concepts (task 1.6)

Recorded deferral, per the change's open question: the first release
permits NO cross-domain imports. A shared-but-not-neutral concept (billing
in Medx and Ledgerx; incidents in Opsx and codex) is handled today by
deliberate duplication with external mappings if needed; the pilots record
where the pressure actually appears, and the decision (kernel promotion vs
a governed cross-domain import contract vs standing duplication) is taken
with that evidence. Nothing in the package contract forecloses any of the
three.

## 9. Follow-on candidates surfaced by this inventory

Recorded for the register/staging pipeline; none are this change's scope:

1. Constrain the traceability edge `relation` vocabulary from the kernel
   relation registry (§4).
2. Reconcile the three L0–L5 source-authority ladders (§2).
3. Make a validator read `contracts/policies/layer-vocabulary.yaml` and
   retire the three hardcoded legacy-role lists (§3; rides the staged
   layer-vocabulary machine migration).
4. Reconcile `journey_state_snapshot` and `current_state_snapshot` (§4).
5. De-verticalize `knowledge_scopes` and the isolation-scope enum (§3;
   DTN pressure).
