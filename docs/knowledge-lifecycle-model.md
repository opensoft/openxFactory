# xFactory Knowledge Lifecycle Model

Status: draft
Kind: architecture
Repository context: openxFactory
Purpose: define how domain knowledge and expert memory enter, are distilled,
are placed across deployment tiers, are kept current, and are promoted or
retired — as a domain-neutral contract that each DomainxFactory specializes.

Related docs: `customer-hermes-memory-model.md` (tier ownership and the
canonical object set, including promotion candidates and the
draft/active/superseded/revoked/archived status lifecycle),
`customer-memory-gateway-architecture.md` (the gateway ports and rails this
lifecycle runs through), `customer-memory-fill-maintenance-taxonomy.md`
(fill and maintenance modes, including reconciliation and correction),
`traceability-model.md` (trace chain for derived artifacts),
`factory-taxonomy-model.md` (profile fields that drive pinning),
`hermes-mixture-of-agents-for-xfactory.md`. Related decision:
`decisions/0002-xfactory-aggregation-repo.md` (the xFactory layer owns memory
promotion and source authority).

This model does not introduce a new memory mechanism. It defines the knowledge
lifecycle that runs through the existing xFactory Memory Gateway ports (read,
write, context packet, promotion, revoke-or-tombstone, audit) and rails. Where
a gate is named below, section 3 maps it to the port that implements it.

## 1. Why This Exists

Every DomainxFactory needs a large, evolving body of expert knowledge, and the
phrase "domain memory" tends to collapse three genuinely different things into
one store with one refresh cadence. That collapse is where knowledge bases rot:
canonical guidance gets mixed with unverified alerts, and slow audit pipelines
block fast-changing facts.

This model separates the kinds of knowledge, defines where each lives, and
makes every transition between states an explicit, governed gate. It is written
in openxFactory because the lifecycle is domain-neutral. MedxFactory,
LedgerxFactory, OpsxFactory, AdxFactory, and codexFactory each supply their own
corpus and taxonomy but inherit the same states, gates, and placement rules.

The design target: **maximize recall and freshness before an answer; maximize
traceability and discipline before that answer is trusted or acted on.**

## 2. Three Knowledge Kinds

Do not model domain knowledge as one store. Model three, because each has a
different owner, refresh cadence, and distillation path.

```text
canonical      slow-changing, source-grounded, must be auditable
               e.g. guidelines, drug interactions, staging criteria,
                    accounting standards, security baselines
               home: Root Truth DBs -> distilled retrieval indexes
                     (Domain Hermes tier; gateway role expert_knowledge_memory)

volatile       fast-changing, latest facts, may be unverified but urgent
               e.g. recalls, new approvals, revised guidance, CVEs, rate changes
               home: Live Knowledge Layer with TTL, fused at query time
                     (Domain Hermes tier)

experiential   emergent from usage, org-local first, sometimes promoted
               e.g. de-identified case patterns, what worked at this org,
                    local standing orders
               home: Tenant Hermes memory -> candidate patterns
                     -> (gates) Root Truth
```

The common failure is forcing volatile and experiential knowledge through the
canonical pipeline. The canonical pipeline optimizes for auditability, which
makes it the slowest path; volatile knowledge optimizes for latency. One
pipeline cannot be good at both.

## 3. Knowledge States and Gates

Knowledge moves through named states. Each arrow is a governed transition, not
an implicit copy.

```text
raw source
  -> [extract gate]      claim + provenance + evidence strength
  -> [validate gate]     Root Truth atom (canonical, versioned)
  -> [distill gate]      Dream / derived index (recipe + seed, traceable)
  -> retrieval
canonical atom
  -> [retire gate]       superseded / archived; derived indexes rebuilt

live fact
  -> [ingest gate]       Live Knowledge entry (TTL, source pointer)
  -> retrieval (fused; see section 5 for flag-versus-override rules)
  -> [promotion gate]    Root Truth atom, when verified; live entry expires
  -> or TTL escalation   forced verification decision near expiry (section 5)

experiential pattern (Tenant Hermes memory)
  -> [de-identify gate]  candidate pattern, stripped to domain criteria
  -> [promotion gate]    Root Truth atom, after domain review
```

Gate contracts the xFactory layer defines; each domain fills in the criteria:

- Extract gate: every claim carries source provenance and an evidence-strength
  rating. No claim without a source.
- Validate gate: promotion into Root Truth requires the domain's validation rule
  (expert review, guideline concordance, or automated concordance check).
- Distill gate: derived indexes record their transformation recipe and random
  seed so any derived object traces back to Root Truth atoms, consistent with
  the trace-chain rule in `traceability-model.md`. Derived objects never become
  truth sources.
- Retire gate: a canonical atom is superseded or archived when a newer atom
  replaces it, a source is retracted, or re-verification fails. Retirement
  triggers rebuild of derived indexes that referenced the atom. Nothing is
  deleted; audit evidence is preserved.
- Ingest gate (volatile): entry records source, timestamp, verification level,
  and a TTL. Marked unverified until it passes the promotion gate.
- De-identify gate (experiential): an org-local pattern becomes a candidate
  pattern only after passing the domain's de-identification criteria (for
  MedxFactory, the applicable safe-harbor or expert-determination standard).
  This is the privacy boundary and is a named gate, not an assumed property.
- Promotion gate: the single shared entry point into Root Truth for both
  volatile and experiential knowledge — one gate, two feeders, and **two
  distinct rubrics**. A verified volatile fact (e.g. a confirmed regulatory
  action) and an org-sourced experiential pattern carry different evidence
  types, so each domain defines a per-feeder promotion rubric under the one
  gate contract.

These gates are not a parallel mechanism to the xFactory Memory Gateway; they
are the knowledge-lifecycle uses of its ports and rails:

```text
extract / validate / ingest  -> write port (source authority rail)
distill                      -> write port for derived artifacts (trace refs)
de-identify                  -> privacy and redaction rail
promotion                    -> promotion port + promotion rail
                                ("nothing silently crosses" scope boundaries)
retire                       -> revoke-or-tombstone port
all of the above             -> audit port
```

Root Truth is append-only with supersession and retraction: corrections and
supersessions append via the revoke-or-tombstone port, and every atom carries
the shared status lifecycle (`draft -> active -> superseded / revoked /
archived`) from `customer-hermes-memory-model.md`. Corrections do not silently
rewrite.

## 4. Tier Placement — Thin Local, Cloud First

Knowledge is placed across the three Hermes tiers defined in
`customer-hermes-memory-model.md` as a cache hierarchy, not a binary of local
versus source.

```text
Domain Hermes (global / cloud)
  canonical Root Truth + derived indexes + Live Knowledge Layer
  the source of record; consistent and auditable across all deployments

Tenant Hermes (org-local, thin cache)
  a pinned subset of derived indexes for the specialties this org practices,
  plus org-local experiential memory; rare queries hit the cloud on demand

Subject Hermes (subject edge)
  subject projections and consented retrieval scope only
```

Default placement rule:

> Keep local only what changes the answer for this org's population or must
> survive offline. Keep global everything that must stay consistent and
> auditable across deployments.

The default deployment posture is **thin local / cloud first**. An org pins a
minimal working set and queries the domain layer on demand for the long tail.

Pinned indexes are stale by definition, so pinning carries a staleness
contract: every pinned derived index declares a `max_staleness` and a sync
cadence, and a pinned index past its bound must either refresh or mark its
results as stale-degraded in retrieval. Pinning is driven by the org's factory
taxonomy profile (see `factory-taxonomy-model.md`): `target_domain_subtype`
and the org's practiced specialties determine the pinned working set. An org
with no oncology service does not carry oncology indexes locally.

The volatile layer is cloud-side and always queried live, so a connected thin
deployment never serves an expired alert. The honest corollary: a
*disconnected* edge carries no live alerts at all. Safety-critical volatile
classes (each domain designates them; recalls and withdrawal alerts in
MedxFactory) therefore require a push path to offline-capable deployments —
they cannot rely on pull-through query fusion. Offline-capable ("fat local")
deployments are an opt-in profile, not the default, selected by org type when
connectivity or latency demands it; their sync and staleness contract,
including the safety push path, is an open question in section 10.

## 5. The Volatile Layer — Recorded Decision

Decision: model latest / volatile knowledge as a **separate Live Knowledge
Layer**, not as fast-tracked entries inside Root Truth.

Retrieval fuses Live Knowledge with derived-index results at query time. Fusion
follows a flag-versus-override rule:

- An **unverified** live entry may *flag* a canonical answer (surface the
  alert, annotate uncertainty, cite the source) but never silently *overrides*
  it.
- A live entry may **override** a canonical answer only at or above a
  verification level the domain defines (e.g. confirmed regulatory action from
  an authoritative source), and the override is recorded in the audit trail.

Entries carry a TTL, but expiry is not always silent. An alert that never
gathers relevance lapses. A live entry that is near expiry and still being
retrieved above a domain-set relevance threshold forces a verification
decision: promote it, extend with an explicit re-verification note, or expire
it with a recorded rationale. A true safety fact must not vanish because
nobody happened to review it before its TTL.

Why not fold volatile knowledge into Root Truth versioning: Root Truth's
append-only, expert-validated path is deliberately the slowest, so breaking
updates would wait on distillation; TTL / auto-expiry is awkward in an
append-only store; and propagating a fast-changing fact into every pinned
local cache fights the thin-local posture. A separate layer that is always
queried live avoids all three.

Cost of the decision: retrieval must implement fusion and conflict resolution
across two stores, and a verified volatile fact must migrate cleanly into Root
Truth so it does not live in both places. That migration is the promotion gate
in section 3 — when a live fact is confirmed, it graduates to a Root Truth atom
and its live entry expires.

## 6. Sub-Domain Scaffolding — Template, Don't Hand-Build

Domains have internal structure (specialties, subfields). That structure should
come from a reusable **sub-domain scaffold generator**, not be hand-built per
specialty.

The generator takes a specialty taxonomy and emits the field hierarchy, the set
of internal truth views per leaf, and the derived-index recipe manifests. New
specialties become configurations of the template rather than new
architectures.

```text
sub-domain scaffold (openxFactory contract)
  input:  specialty taxonomy (supergroups -> parent fields -> leaf subfields)
  output: field hierarchy IDs
          per-leaf internal truth views
          derived-index recipe manifests
```

The scaffold keeps field IDs stable ("constancy before expansion"): start
coarse, then add finer microfields under existing IDs rather than renaming.

## 7. Cross-Domain Concepts — Shared Atoms, Not Copies

Some concepts belong to several fields at once (a lab abnormality that appears
in multiple specialties, a control that spans several compliance regimes).
Model these as **shared atoms with multiple parents**, not duplicated entries.
A single Root Truth atom is referenced by every field that needs it, so a
correction propagates once. Duplication is the second common source of rot.

Shared atoms need an ownership rule, or corrections stall between parents:
every shared atom designates exactly one **steward field** whose reviewers own
validate, correction, and retire decisions for the atom. Co-parent fields are
notified on every change and may escalate a disputed change to Domain Hermes
review, but they do not hold a veto that can leave the atom unowned.

## 8. Feedback Without Training on Live Subject Data

Usage should improve retrieval without training models on identifiable
subject data. The path is: usage produces org-local patterns in Tenant Hermes
memory; the de-identify gate (section 3) strips them to candidate patterns
under domain criteria; the promotion gate reviews them; approved patterns
become Root Truth atoms that improve future retrieval for everyone. Retrieval
quality improves through curated, promoted knowledge, not through implicit
learning on live records. The consent rail constrains which Root Truth
partitions a given subject's retrieval may touch, per the subject's consent
profile in `customer-hermes-memory-model.md`.

## 9. Domain Specialization Example — MedxFactory

MedxFactory implements this contract with its tier aliases: Subject Hermes is
**Patient Hermes**, Tenant Hermes is **Clinic Hermes** (the care organization),
Domain Hermes is **Medical Domain Hermes**.

```text
canonical      Root Truth DBs over the medical corpus (papers, guidelines,
               teaching cases), distilled into Dream DBs / retrieval indexes
volatile       Live Knowledge Layer: drug recalls, FDA approvals, revised
               guidance, safety alerts, with TTL and source pointer; recalls
               and withdrawal alerts are the designated safety-push class
experiential   Clinic Hermes: case patterns and standing orders, through the
               de-identify gate (HIPAA safe-harbor or expert-determination
               criteria), promoted via specialist reviewer pods under Medical
               Domain Hermes review standards

tiers          Medical Domain Hermes (global medical truth + live layer)
               Clinic Hermes (clinic pins its practiced specialties)
               Patient Hermes (patient projections, consented scope)

sub-domains    oncology 10 x 10 x 10 scaffold (supergroups -> parent fields ->
               leaf subfields) is the first instance of the section 6 generator;
               pharmacy, radiology, dermatology follow as configurations
cross-domain   a finding shared across oncology, endocrine, and neurology is
               one shared atom with three parents; one of them is designated
               steward (section 7)
```

Other DomainxFactories specialize the same contract with their own corpus and
aliases: LedgerxFactory (accounting standards / rate changes), OpsxFactory
(baselines / CVEs), AdxFactory, codexFactory.

## 10. Open Questions

Carried forward for design and pilot validation:

- Fusion ranking: given the flag-versus-override rule in section 5, how does
  retrieval *rank* a flagged canonical answer against the live entry flagging
  it, and how is the combined result presented?
- Promotion rubrics: the precise per-domain, per-feeder bar (volatile versus
  experiential) for entry into Root Truth.
- Re-verification cadence: the default review interval for a canonical atom,
  beyond the event-driven retire triggers in section 3.
- Pin sizing: how the working set for an org is computed from its taxonomy
  profile, the eviction policy for the local cache, and default
  `max_staleness` values per index class.
- Retrieval-noise ceiling: how many derived indexes before noise outweighs
  recall gains.
- Score calibration: keeping retrieval scores comparable across sub-domains.
- Offline profile: the sync and staleness contract for opt-in fat-local
  deployments, including the safety-critical push path in section 4.

## 11. Ratification Path

Repo precedent (the canonical-policy migration under `openspec/changes/`)
routes layer contracts through OpenSpec governance. Before implementation:

1. an OpenSpec change proposal adopting this model as a shared xFactory
   standard, reconciling it with `customer-memory-gateway-architecture.md`
   port semantics where implementation details diverge; and
2. a numbered ADR under `docs/decisions/` ratifying the section 5 volatile-
   layer decision, which is separable and load-bearing.
