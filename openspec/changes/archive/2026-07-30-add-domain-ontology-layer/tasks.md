## 1. Semantic Inventory And Decisions

Sections 1-3 realized 2026-07-29. Evidence for 1.1-1.6:
[docs/domain-ontology-semantic-decisions.md](../../../docs/domain-ontology-semantic-decisions.md)
— the term-by-term inventory with owners and adoption candidates (1.1), the
collision/leak/gap registers (1.2), the identifier grammar with positive and
negative examples (1.3), the edge-classified compatibility rubric with
retention/two-pin/rollback (1.4), the YAML/JSON canonical-representation
ruling with JSON-LD/RDF recorded as optional derivative (1.5), and the
recorded cross-domain deferral with the three candidate mechanisms (1.6).

- [x] 1.1 Inventory the neutral semantic concepts, relation vocabularies, lifecycle terms, and authoritative owners already present across xFactory schemas, policies, validators, and architecture documents.
- [x] 1.2 Record collisions, overloaded terms, domain-specific leaks, duplicate definitions, and contracts that must be referenced rather than restated by the semantic kernel.
- [x] 1.3 Finalize the stable core and domain namespace grammar, identifier immutability rules, the acyclic multi-parent specialization rule, and label/alias separation and in-namespace uniqueness with positive and negative examples.
- [x] 1.4 Finalize the `additive`, `clarifying`, `breaking`, and `retiring` compatibility rubric — including parent addition/removal, relation domain/range widening and narrowing, alias collision as a validation error, and external-mapping refresh — plus migration, retention, two-pin coexistence, and in-flight rollback requirements.
- [x] 1.5 Ratify the provider-neutral YAML/JSON canonical representation and record JSON-LD/RDF export as optional derivative interoperability unless first-release evidence justifies inclusion.
- [x] 1.6 Record the cross-domain shared-concept decision (kernel promotion vs governed cross-domain import vs deliberate duplication with mappings) or its explicit deferral with pilot evidence.

## 2. Ontology Contract Family And Core Kernel

Evidence for 2.1-2.6: `contracts/domain-ontology/` — ten schemas (2.1) with
closed enum vocabularies in-shape and the finding-code vocabulary in the
family README (2.2); inventory digest closure, ontology-family-only
membership, beside-package record kinds, and `retained/<version>/` retention
(2.3); the `core/` kernel package, 24 concepts + 9 relations, every term
naming its authoritative contract, adoption pending-while-draft per the
bootstrap scenario (2.4); registered in the contracts README
Contracts-Pending-Realization table, the family README, and the repo doc
index, with manifest/CHANGELOG registration deferred to the bundle cut per
the documented convention (2.5); by-reference mapping + license-class +
permitted-use contract with refresh-as-mapping-revision (2.6).

- [x] 2.1 Create `contracts/domain-ontology/` with shared definitions and schemas for the ontology package manifest, concepts, relations, external mappings, source/steward references, candidate changes, releases/adoptions, migration maps, and bounded semantic context.
- [x] 2.2 Define closed lifecycle, semantic-kind, mapping-kind, compatibility, fill/maintenance-mode, provenance, and finding-code vocabularies.
- [x] 2.3 Implement package inventory, ontology-family-only inventory membership, raw-content digest, and published-version retention rules consistent with the existing contract release and overlay-manifest conventions.
- [x] 2.4 Build the minimal xFactory core ontology from the approved inventory, with each term pointing to its authoritative contract, recording adoption evidence (two independent resolvable adopters, pending while draft and resolved via the pilot packages before publication), and adding no domain-owned nouns; record that openxFactory alone classifies kernel revisions.
- [x] 2.5 Register the new schemas, core package, validators, and fixture indexes in the canonical contract manifest and documentation indexes without allocating a release number early.
- [x] 2.6 Define the by-reference external-terminology mapping contract with license-class vocabulary, permitted-use recording, and refresh-as-mapping-revision semantics.

## 3. Canonical Semantic Validation

Evidence for 3.1-3.8: `scripts/validate-domain-ontology.py` — 25 stable
finding codes covering 3.1/3.2 structure+semantics, 3.3 privacy and
control-plane rules (subject-URN and endpoint scans, aggregation floor,
reserved authority fields aligned with the runtime's protected-word list,
authority-plane instance references), and 3.4 cross-contract checks
(semantic-context closure/pin/tenant-binding agreement plus the
`domain_ontology` content-manifest cross-check; the memory context-packet
leg activates when section 6 adds the packet fields). Fixtures: 3 positive
packages (medical + engineering specializations of the same kernel + a
generated scaffold, 3.5), 34 indexed negatives incl. mirrored-terminology,
licensed-content, and paired-revision parent-add/range-widening
misclassification cases against retained prior bytes (3.6, 3.8), each asserting its declared finding;
`--determinism` proves identical findings on repeat (3.7).

- [x] 3.1 Implement a canonical domain-ontology validator for schema conformance, package/import closure, exact digests, namespace ownership, identifier uniqueness, label/alias uniqueness, foreign-kind inventory exclusion, retention of referenced superseded versions, and stable-ID reuse.
- [x] 3.2 Add semantic checks for missing or circular specialization, multi-parent acyclicity, relation domain/range, lifecycle and supersession, mapping validity and mapping-target registration, kernel adoption evidence, steward/source completeness, and compatibility/migration evidence.
- [x] 3.3 Add privacy and control-plane checks that reject subject or tenant instance material in packages, candidates, reports, fixtures, and quality signals; enforce the term-signal aggregation floor; and reject any ontology record carrying a field outside the closed vocabulary or naming a grant, credential, consent record, approval decision, cross-layer binding, provider binding, or route, without depending on label or definition prose.
- [x] 3.4 Add cross-contract checks for ontology package, Domain Hermes content manifest, installation overlay, compiled semantic context (subset closure or recorded truncation, tenant-binding resolution), and memory context-packet pin agreement.
- [x] 3.5 Create indexed positive fixtures for at least one medical and one software-engineering specialization of the same core plus a generated new-domain scaffold.
- [x] 3.6 Create negative fixtures for digest drift, namespace collision, label/alias collision, ID reuse, invalid cycles, parent addition on a published concept, relation domain/range widening and mismatch, undeclared mappings, unregistered mapping targets, a foreign document inventoried as ontology content, missing sources/stewards, a deleted but still referenced superseded version, private-instance leakage, a below-floor term signal, an unclosed context subset, and semantic-authority bypass.
- [x] 3.7 Add deterministic automated tests that reproduce every indexed finding and prove repeated validation produces identical results.
- [x] 3.8 Add negative fixtures and validator findings for mirrored external terminologies and licensed source content beyond the recorded permitted use.

## 4. Domain Ontology Generation

Section 4 realized 2026-07-29. Evidence: `scripts/apply-domain-starter.py`
v13 (ontology-aware). The pre-run questionnaire (openxFactory doc §3.4.5,
the generated questionnaire's Ontology Intake section, the answer schema's
`ontology.*` required paths, and the answer example's `ontology:` section)
carries the full intake model (4.1). Generation renders the
`hermes/domain/ontology/` templates — package manifest, concepts, source
inventory, coverage-gap report, review fixtures, STARTER provenance marker,
and tree README (4.2) — declares `domain_ontology` in the content manifest
(created or merged additively; `domain_ontology` added to the
content-manifest schema and overlay-validator vocabulary as ratified), and
records the ontology-aware starter version in `STARTER.yaml` (4.3). Seeding
is a pure function of the answer set, domain context, and the pinned
openxFactory kernel (no timestamps or randomness); byte-reproducibility is
proven by test scenario 3 (4.4). `--ingest-candidates` is the bounded
model-extraction interface: registered-source approval, extraction-run
identity, confidence, declared conflicts, open review state; writes only
candidate records and never deletes, replaces, or resurrects one or its
disposition (4.5). Dedup/conflict, placeholder-skip, unsupported-list, and
coverage-gap reporting never silently resolve conflicts (4.6); review
fixtures are synthetic labeled positive/negative/representative cases
(4.7). Reruns preserve domain-owned content — a differing file is a
Conflicts-table row and its preserved bytes are what the manifest digests —
and the rerun report gains the Unresolved Semantic Inputs table beside
created/updated/skipped/conflicts (4.8).
`scripts/test-domain-starter-ontology.py` covers empty repo (with the
canonical validator passing the generated package end-to-end), partial
answers, idempotent rerun, model-ingest rerun with
new/duplicate/conflicting classification and disposition preservation plus
unapproved-source fail-closed, legacy repo additivity, conflicting domain
content, and attempted overwrite (4.9) — all green.

- [x] 4.1 Extend the domain pre-run questionnaire and its machine-readable answer model with subject/focal-item kinds, activities, states, outcomes, interventions, external terminologies, ontology sources, boundaries, stewards, reviewers, and unresolved semantic assumptions.
- [x] 4.2 Add starter templates for `hermes/domain/ontology/`, including manifest, concepts, relations, mappings, source inventory, candidate register, coverage-gap report, review fixtures, and Domain Hermes stewardship metadata.
- [x] 4.3 Extend `scripts/apply-domain-starter.py` to generate the ontology-aware draft scaffold for a new domain, record the ontology-aware starter version in the generated repository, and declare the package in the Domain Hermes content manifest.
- [x] 4.4 Implement deterministic seeding from the taxonomy tuple, layer aliases, existing domain models, workflow catalogs, evidence types, and approved structured vocabulary imports, and prove the seeded scaffold is byte-reproducible from the same answer set and pinned sources.
- [x] 4.5 Define a bounded candidate-ingest interface for model-assisted extraction that requires approved sources, provenance, confidence, ambiguity, conflicts, extraction-run identity, and draft review state; writes only to the candidate register; and never deletes, replaces, or resurrects an existing candidate or its recorded disposition.
- [x] 4.6 Implement entity-resolution, deduplication, core-specialization mapping, unsupported-term, and coverage-gap reports without silently resolving conflicts.
- [x] 4.7 Generate positive, negative, and representative labeled classification fixtures from the draft package for Domain Hermes review, carrying only de-identified or synthetic cases with their expected classification recorded.
- [x] 4.8 Preserve active or domain-owned ontology content on starter rerun and extend the rerun report with conflicting and unresolved categories beside created, updated, and skipped artifacts.
- [x] 4.9 Add starter tests for empty repositories, partial answer sets, idempotent reruns, a model-assisted rerun that proposes a different candidate set over unchanged sources, legacy repositories, conflicting domain content, and attempted active-package overwrite.

## 5. Domain Hermes Stewardship And Maintenance

Section 5 realized 2026-07-29. Evidence: the `domain_ontology` content kind
is in the content-manifest schema and overlay-validator vocabulary (section
4) and the generated-domain completeness rule is live —
`validate-hermes-domain-overlay.py` fails a repo whose ontology-aware
STARTER marker lacks a `domain_ontology` declaration, keyed on the recorded
marker, with a repo-shaped negative fixture (5.1).
`templates/domain-hermes-ontology/` carries the stewardship-policy,
candidate-disposition, release-approval, consumer-adoption, and
maintenance-input templates, and the starter seeds a live
`stewardship.yaml` as inventoried package content (5.2). The
`xfactory_ontology_stewardship_policy` contract makes the seven modes
machine-readable — required inputs, review evidence, outputs, blocked
states — plus council/quorum/high-impact reservations, source-review
cadence, trigger thresholds, quality gate, and the standing aggregation
floor, validated by ONT-POLICY/ONT-FLOOR rules (5.3).
`scripts/ontology-maintenance.py` evaluates all nine trigger families over
a governed `xfactory_ontology_maintenance_input` (`as_of` is data, never a
clock), opens mode-mapped candidates append-only, fails closed on
below-floor term entries, and records every evaluation as an append-only
`xfactory_ontology_maintenance_report` — a clean check is itself evidence
(5.4). Publication is mechanized by `scripts/ontology-release.py`:
byte-identical retention of the superseded version, previous/supersedes
pins, a new compatibility line on breaking, a shipped migration map joins
the inventory, and the release record names the accountable steward —
in-place mutation is structurally impossible and worker/agent-attributed
publication fails both the tool and the validator (5.5). Readiness is
`validate-domain-ontology.py --readiness`: `domain_scaffold_required`
until the package validates clean, publishes via an accountable release,
carries no placeholder stewards/concepts, ships its policy, and satisfies
the quality gate (5.6). The 5.7 proof: the stewardship test suite shows an
agent accountable identity refused at release while the same identities
prepare candidates, diffs, and reports freely; validator fixtures
release-agent-published and candidate-agent-accepted pin the rule.
Quality wiring (5.8): policy-declared required signals with thresholds
block release absent a recorded `quality_exception_ref` (recorded on the
release record), readiness recomputes signals against the CURRENT digest,
maintenance triggers consume the same policy, and the
distinct-subject/distinct-tenant floor binds quality reports AND
maintenance inputs (report floors may not be weaker than the policy's).
All proven by `scripts/test-ontology-stewardship.py` (22 checks green).

- [x] 5.1 Extend the Hermes domain content-manifest schema and canonical validator with the additive `domain_ontology` content kind and generated-domain completeness rules.
- [x] 5.2 Add Domain Hermes templates for ontology steward assignments, review-council policy, source review cadence, candidate disposition, compatibility decision, release approval, and consumer adoption.
- [x] 5.3 Define machine-readable workflows for `seed`, `extend`, `refresh`, `reconcile`, `correct`, `deprecate`, and `retire`, including required inputs, review evidence, outputs, and blocked states.
- [x] 5.4 Implement candidate triggers and reports for source change/expiry, unknown terms, mapping failures, repeated low-confidence classification, conflicts, workflow drift, sub-domain expansion, appeals, and reviewed promotion candidates.
- [x] 5.5 Implement append-only ontology candidate, decision, publication, supersession, deprecation, retirement, and adoption evidence with no in-place mutation of active packages, each publication naming the accountable steward identity and any worker-attributed publication failing validation.
- [x] 5.6 Add generated-domain readiness checks that keep incomplete ontology scaffolds non-operational until sources, stewards, fixtures, ratification, publication, and exact pins pass.
- [x] 5.7 Prove agents and Omnigent workers can prepare diffs, impact reports, and fixtures but cannot promote or publish a package under any worker profile.
- [x] 5.8 Define the per-release quality report and governed quality-signal telemetry (intake-scope coverage, unknown-term rate, mapping resolution, classification fixture accuracy, open-candidate age), each declaring numerator, denominator, observation window, recorded procedure, and pinned fixture-set identity; keep pass/fail validator conformance separate from the accuracy ratio; wire domain thresholds into the maintenance triggers, the readiness baseline, and a publication block that only a recorded reviewed exception releases; and enforce the distinct-subject/distinct-tenant aggregation floor on term-level signals.

## 6. Semantic Context And Memory Gateway Integration

Section 6 realized 2026-07-29. Evidence:
`scripts/ontology-compile-context.py` deterministically compiles a bounded
`xfactory_semantic_context` from exact kernel + package pins, CLOSING the
subset over specialization ancestors and relation endpoints or emitting an
itemized truncation only where the profile allows it, and failing closed
on unrestricted requests, unresolvable terms, retired/superseded packages,
and wrong-package or dangling tenant bindings (6.1). Both memory-gateway
packet contracts carry an optional additive `semantic_context` block —
exact context id/digest, kernel/domain pins, worker scope, bounded term
subset, lifecycle/freshness — and `validate-memory-gateway.py` preflights
it BEFORE provider I/O: digest and pin formats, published/deprecated
lifecycle only (retired rejected), purpose agreement with the packet, and
rejection of any authority-named key inside the block; eight new
conformance-fixture scenarios registered (6.2/6.3, and the section-3.4
memory-packet leg now active). The canonical validator enforces 6.4
generically: any document carrying an embedded `semantic_context` without
its exact identity and pins fails ONT-CONTEXT-PIN (fixture
embedded-context-missing-pins). `scripts/test-semantic-context.py` (18
checks) covers context/package mismatch, retired-package and
digest/format failure, unrestricted-request refusal, tenant-binding
mismatch and dangling targets, truncation rules, deterministic
recompilation (provider-replacement stability), and cross-purpose reuse
(6.5), plus the adversarial floor: an authority field on a worker profile
fails ONT-AUTHORITY-FIELD and the compiled artifact carries no
authority-named field at any depth — classification can describe and never
authorize (6.6). The neutral `xfactory_semantic_context_profile` kind
(family now fourteen) is inventoried package content with ONT-PROFILE
resolution checks; the medx reference package ships `profile-verify.yaml`
whose compilation yields exactly the closed verify-worker subset with the
permission matrix untouched; omnigent overlay declaration and worker
runtime wiring remain the named follow-up omnigent change (6.7).

- [x] 6.1 Implement deterministic compilation of a purpose-bounded semantic-context artifact from exact kernel, domain package, and approved tenant-binding pins, closing the term subset over specialization ancestors and relation domain/range concepts or emitting an itemized truncation record, and failing closed on an unresolvable or wrong-package tenant binding.
- [x] 6.2 Extend customer and expert context-packet contracts to carry semantic-context ID/digest, exact ontology identities, lifecycle/freshness metadata, and the bounded term subset when semantics are included.
- [x] 6.3 Integrate semantic-context validation into memory gateway preflight before provider I/O while retaining all existing consent, privacy, purpose, authority, redaction, promotion, and audit rails.
- [x] 6.4 Require typed claims, workflow hypotheses, jobs, or derived artifacts that use domain semantics to retain their exact semantic-context or ontology package identity.
- [x] 6.5 Add tests for context/package mismatch, stale, expired, or retired-package context, digest-verification failure, unrestricted ontology requests, tenant-binding mismatch, unclosed subsets, provider replacement, and cross-purpose reuse.
- [x] 6.6 Add adversarial tests proving classification, equivalence, specialization, graph traversal, and inferred relations cannot grant access, approve work, promote data, create bindings, or authorize external action.
- [x] 6.7 Define the neutral worker-archetype/worker-class semantic-context profile artifact inside this change's contract family and prove by fixture that compilation yields only the declared closed term subset per worker with the permission matrix unchanged; record omnigent overlay declaration and worker runtime wiring as the follow-up omnigent change.

## 7. Existing-Domain Migration And Cross-Domain Pilots

Section 7 realized 2026-07-29 — full record in
[docs/domain-ontology-pilot-report.md](../../../docs/domain-ontology-pilot-report.md),
pilot packages retained as validator-covered fixtures under
`contracts/domain-ontology/examples/pilots/`. The starter's `--dry-run` is
the explicit migration/report path: full report, zero writes, content
manifest and pins untouched (7.1). Two contrasting approved domain
fixtures — the clinical journey model and the engineering admission model —
ran the whole arc (generate → conflict → disposition → publish → breaking
reparent on `xf/medx@2` / retiring release on `xf/codex@2` → maintenance →
`ontology_ready` → worker-context compilation); no pilot needed a kernel
term, none went unused, and the kernel's per-term adoption evidence is now
recorded (two resolvable adopters each, relations included; kernel digest
`9d4ea5fa…` after the adoption restamp, still DRAFT pending the governed
bundle-cut publication) (7.2). The colliding
model proposal was auto-recorded as a conflicting candidate against the
structured import and blocked readiness until the accountable steward
dispositioned it (7.3). Additive, breaking, retiring, explicit adoption
pins, retained superseded bytes, and the structural two-pin/rollback story
are recorded with historical digests intact (7.4). Downstream handoff
packets for MedxFactory, codexFactory, hermes-install, and the follow-up
omnigent change:
[docs/domain-ontology-adoption-handoff.md](../../../docs/domain-ontology-adoption-handoff.md)
— their pin updates stay in their owning governed changes (7.5).

- [x] 7.1 Build an explicit dry-run migration/report path that scaffolds ontology candidates beside an existing DomainxFactory without changing its content manifest or active runtime pin.
- [x] 7.2 Pilot the generator and validator against MedxFactory and codexFactory, or two equivalently contrasting approved domain fixtures, and use the comparison to remove domain leakage from the core kernel.
- [x] 7.3 Prove structured authoritative imports take precedence over model candidates and that unresolved conflicts remain review blockers in both pilots.
- [x] 7.4 Record additive, clarifying, breaking, retiring, explicit adoption, two-pin coexistence, and rollback-with-in-flight-work exercises with historical interpretation preserved under the original ontology pin and superseded package bytes retained at their digests.
- [x] 7.5 Produce downstream handoff packets for DomainxFactory and Hermes Install consumers; keep their implementation and pin updates in their owning governed changes.

## 8. Documentation, Verification, And Release

Docs (8.1, commit c2943ef): `docs/architecture.md` (Semantic Plane
section), `docs/xfactory-domain-factory-model.md` (Domain Ontology
Ownership), `docs/openxfactory-installation-spine.md`
(domain_ontology_seeding row), `docs/knowledge-lifecycle-model.md`
(knowledge_atom kernel alignment), `docs/customer-memory-gateway-architecture.md`
(rails preflight), `contracts/policies/layer-vocabulary.yaml` (role TEXT
only — Domain Hermes ontology stewardship, Tenant Hermes semantic
bindings; frozen keys untouched), the starter/pre-run surfaces in
`scripts/apply-domain-starter.py` v13, and the family README
(`contracts/domain-ontology/README.md`, rewritten again at the fix wave:
eighteen kinds, self-retention, per-signal exceptions). Consolidated
walk-through (8.2): [docs/domain-ontology-guide.md](../../../docs/domain-ontology-guide.md)
(seven parts: plane separation, generation, stewardship, maintenance,
compatibility, migration/retention/rollback, runtime consumption), linked
from the repo README doc index.

Verification battery (8.3, re-run after the registry fix waves):
`validate-domain-ontology.py` self-test 10 positive units + 44 indexed
negatives, repo scan + content-manifest cross-check, `--determinism`
identical findings on repeat, `--readiness` ontology_ready on both pilot
packages; `test-domain-starter-ontology.py`,
`test-ontology-stewardship.py` (incl. blanket-exception refusal,
exception-without-measurement refusal, per-signal release, self-retention,
consumer-impact refusal), `test-semantic-context.py` (privacy/isolation
negatives incl. authority-field rejection and cross-purpose/retired
preflights); `validate-hermes-domain-overlay.py` self-test (11 fixtures) +
MedxFactory `make validate` green against the re-pinned kernel (Medx
613591f); `validate-memory-gateway.py` green (closed packet schemas
applied, pins resolved against the ontology tree);
`validate-domain-openxfactory-pins.py` green;
`OPENSPEC_TELEMETRY=0 openspec validate --all --strict` 56/56. The
`referencing`-dependent validators (avatar-client, document-catalog,
hermes-runtime, ideation-*, worker-enrollment) fail in this jsonschema-4.10
environment identically before and after the change — environmental, not
regression.

- [x] 8.1 Update the architecture, domain-factory model, installation spine, knowledge lifecycle, memory gateway, domain starter, pre-run questionnaire, and contract README documents with the ratified ontology ownership and lifecycle, and update the machine-readable `contracts/policies/layer-vocabulary.yaml` role text so Domain Hermes ontology stewardship and Tenant Hermes semantic bindings do not drift from the promoted layer-vocabulary spec.
- [x] 8.2 Document the semantic-plane/control-plane separation, generation pipeline, Domain Hermes stewardship model, maintenance triggers, compatibility rubric, migration path, and provider-neutral runtime consumption.
- [x] 8.3 Run strict OpenSpec validation, schema and semantic fixture suites, domain-starter tests, domain-overlay validation, memory-gateway tests, privacy/isolation negatives, and existing repository regression checks.

Independent review (8.4): a dedicated six-lens reviewer (architecture,
security, privacy, domain-stewardship, migration, adversarial) ran four
rounds, each re-running the ORIGINAL attack against the actual bytes
rather than reading the fixes. Round 2 returned BLOCKED with 16 blocking
findings (root cause: "rules attached to a location or shape rather than
to the artifact"); the fix wave (7fafc90 + cd4105b) resolved 15/16 and
introduced N1 (the shared package registry was read but never populated —
three rules dead code, kernel publication unsatisfiable); the N1 wave
(e4b047c) resolved N1/N2/N3 with order-independent registration and two
sentinel fixtures the reviewer independently confirmed fail iff the
mechanism breaks; round 4 raised N4 (loose-record roster resolved by
first entry — a roster-confusion bypass and an honest-record
misjudgment); the N4 wave (5d39bb4) closed both directions by exact-digest
resolution AND repo-scoped registries, with the roster-twin sentinel pair.
Final verdict: **APPROVED against release candidate 5d39bb4** — all 16
original + N1–N4 resolved; independent battery reproduced (10 positives /
44 negatives, zero rot, determinism across three hash seeds). Recorded
for the bundle cut, per the reviewer: the kernel stays `draft` (flipping
to `published` now validates clean — publication is unblocked but remains
a governed Domain-Hermes/bundle decision not taken here), and eight
non-blocking findings (F18–F21, F24–F27) carry to the follow-up omnigent/
stewardship changes — F18 (term-level lifecycle enforcement) first before
term retirement becomes load-bearing in a live domain.

- [x] 8.4 Obtain independent architecture, security, privacy, domain-stewardship, migration, and adversarial review and resolve every blocking finding against the exact release candidate.
Bundle cut (8.5): contract-v1.21 was claimed mid-flight by
add-capability-steward, so this change allocated **contract-v1.22**
(integration order known before allocation). Cut commit 099e788 registers
the eighteen family schemas + three kernel content files in
`contracts/manifest.yaml` with per-file sha256 (and refreshes the
layer-vocabulary entry digest for the 8.1 role-text edit), bumps
`contract_bundle_version`, and records the CHANGELOG entry; 641296c adds
`contracts/releases/contract-v1.22.digests.yaml` (179 entries, raw git
blobs); the annotated tag `contract-v1.22` points at 641296c and is
pushed. Independent verification against the REMOTE:
`validate-contract-release.py verify-tag --remote origin --tag
contract-v1.22` → pass; `verify-commit --commit 641296c` → pass. The
xf/core kernel package ships DRAFT in this bundle by explicit decision:
publication now validates clean (proven in 8.4) and remains a governed
Domain-Hermes bundle decision for a future cut.

Adoption evidence (8.6): **MedxFactory — ADOPTED**: draft `xf/medx`
package at `hermes/domain/ontology/` generated by the v13 starter,
kernel_import digest-pinned to the restamped kernel (`9d4ea5fa…`, Medx
commit 613591f), dedicated ontology-steward persona + MxD-MRR review
council realized via its archived domain-hermes-content changes, `make
validate` green against the workspace kernel. **codexFactory —
DEFERRED**: its pilot package is retained as a validator-covered fixture
(`contracts/domain-ontology/examples/pilots/codex/`); in-repo adoption
lands through its own governed change per the handoff packet.
**hermes-install — DEFERRED**: consumes semantic contexts only through
the memory-gateway packet contracts (this bundle); no repo change until
its runtime carries packet-borne semantic context. **Omnigent runtime
wiring — DEFERRED to the named follow-up omnigent change** (recorded at
6.7): worker profiles + compiled per-worker contexts are the ratified
seam; overlay declaration and runtime wiring stay in the omnigent
contract family's owning change. Handoff packet:
[docs/domain-ontology-adoption-handoff.md](../../../docs/domain-ontology-adoption-handoff.md).
Non-blocking review findings F18–F21/F24–F27 carry to those follow-ups
(F18 first). Archived on release proof: bundle tag verified remotely +
review APPROVED at 5d39bb4 + MedxFactory pin landed.

- [x] 8.5 Allocate the next available additive contract bundle only after integration order is known, generate the exact digest inventory, publish the immutable reviewed commit/tag, and independently verify remote bytes and provenance.
- [x] 8.6 Record consumer adoption or explicit deferral evidence and archive the change only after the implementation feature, release proof, and required downstream pins have landed.
