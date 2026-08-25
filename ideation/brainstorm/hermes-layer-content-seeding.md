# Three-Layer Hermes Content & Seeding: giving each layer its personality, memory, and policy — Brainstorm

Status: brainstorm
Kind: architecture
Summary: The install stands up the three Hermes layers *structurally*
(role + label + policy_namespace + an inert `overlay_ref` pointer); it does
NOT yet give any layer its *content* — the personality, memory, and policy
that make a Client/Domain/Project Hermes actually behave. This doc frames the
per-layer content model and how it gets seeded at or after install: the
**Domain** layer authored once in the domain repo (same for every codexFactory
install), the **Client** layer scaffolded from a neutral default and tuned by a
policy-loading wizard, and the **Project/Customer** layer scaffolded from a
library of project-type templates. It sits UNDER the practice-adoption pipeline
(`hermes-governed-nightly-sweep.md`, `domain-practice-suggestion-generation.md`,
`practice-clearance-and-project-realization.md`) — those docs assume the layers
already have content; this doc is how the content gets there. Content is
assembled by a pinned overlay stack (`Hermes-Install-Core` ops engine →
xFactory generic → domain → client → project) and the running Hermes seeds
the enforceable slice of it into records — the two axes and the seam below.
Topics: hermes, three-layer-hermes-runtime, layer-content-seeding, domain-hermes,
client-hermes, project-hermes, personality, memory-gateway, practice-catalog,
overlay-ref, provision-project, client-policy-wizard, project-type-templates,
hermes-install-core, composition-overlay-stack, openworkflow-lineage
Repository context: openxFactory (spans codexFactory + installs/hermes-install)
Captured: 2026-07-21

Updated: 2026-07-22 (increment 1 realized; seam/naming/re-pin decisions recorded)

## Decided (2026-07-22)

- **Central seam: HYBRID — decided.** Materialize the *enforceable* slice
  (policy envelopes, boundaries, consent models) into runtime records; keep
  *reference* content (persona text, role prose) behind the pin; memory goes
  through the ratified gateway, never a parallel store. Increment 1 was built
  on this assumption and is realized (below); the §Central seam section keeps
  the full argument.
- **Naming: `subject/` wins.** codexFactory's `hermes/subject/` is the truer
  word (the subject ranges from a patient to a repo); the prescribed model in
  `openxFactory/docs/xfactory-domain-factory-model.md` is to be updated from
  `customer/` → `subject/`, not the other way around. Paths in this doc are
  written `subject/` accordingly. (The runtime's Customer *layer role* label is
  a separate, already-canonical concept — this decision is about the domain
  repo's content directory name.)
- **Domain re-pin consent: pin-range model — decided.** The client consents to
  a *pin range* for the Domain overlay; the domain re-pins freely within it;
  changing the range itself is a client-consented event. Where ranges are
  recorded is still open (seeding-mechanism doc).
- **Increment 1 (read-only load) is DONE, not proposed.** Realized as
  hermes-install change `add-seed-layer-content` + Speckit `002-seed-layer-content`,
  merged (PR #5), gates green, archived
  `openspec/changes/archive/2026-07-22-add-seed-layer-content`; capability spec
  at `openspec/specs/layer-content-seeding/spec.md`.

## Possible feats

- **Layer content loader** — a `seed-layer-content` runtime verb that fetches,
  validates, and (per the seam decision) materializes the pinned `overlay_ref`
  content into the live stack after `register-stack`. Detailed in
  `hermes-layer-seeding-mechanism.md`; increment 1 (read-only load) is
  **realized and archived 2026-07-22** (hermes-install `add-seed-layer-content`
  + Speckit `002-seed-layer-content`); increments 2+ in §Increment roadmap.
- **Domain Hermes content authoring (codexFactory)** — fill `hermes/domain/`
  (persona/system-frame, `roles/`, `policies/`, `review-councils/`,
  `memory-boundaries.yaml`, `escalation-rules.yaml`, `agent-mixes.yaml`) and the
  practice catalog, ratified in codexFactory. Detailed in
  `codexfactory-domain-hermes-content.md`; the persona-depth question is
  `hermes-persona-character-model.md`.
- **Client policy wizard** — guided elicitation that tunes the neutral client
  scaffold into a real per-client policy set + the auto-clear envelope, written
  to `config/clients/<client>/`.
- **Project-type template library** — codexFactory-owned archetypes
  (`hermes/subject/templates/<type>.yaml`) selected at `provision-project`, with
  a neutral schema in openxFactory.
- **Neutral layer-content + project-template schemas** — the openxFactory
  contract shapes that keep every domain's layer content legible to the client
  policy layer.
- **Core ops-engine reconciliation** — wire this repo to consume
  `opensoft/Hermes-Install-Core`'s single-Hermes operational engine (deploy,
  backup/restore, DR, secret materialization, migration validation) instead of
  re-implementing it, and reconcile the `openWorkflow`↔`openxFactory` lineage.

## The gap this closes

`register-stack` today builds a `LayerSpec(layer_id, display_name,
policy_namespace, overlay_ref)` per layer and persists it into `hermes_layers`
(`installs/hermes-install/migrations/0003_logical_layers_and_topology.sql`).
`overlay_ref` is a `git+<repo>@<rev>` string — a pinned pointer at per-layer
content — but **the runtime never fetches, parses, or materializes what it
points at.** A registered Domain layer knows it is "codexFactory / Software
Engineering pinned at `5c6f81b9`"; it does not know a single thing codexFactory
*believes* about software engineering. Governed records attach to a layer only
through the `layer_id` FK added in `0004`. So the layers are real containers
with correct isolation and no contents.

"Personality and memory" is the contents: what each layer knows, how it
reasons, what it is allowed to decide, and what it remembers across jobs. The
seam already exists (`overlay_ref` + the stack's `template_revision` /
`parameter_digest` pins). The open work is (a) a content model for what lives
behind that pointer per layer, and (b) a **seeding** step that loads it into
the running Hermes.

Two pin facts worth stating precisely (they shape the loader): the archive
digests (`source_archive_sha256`) live in the install's **compatibility
manifest** — recorded today only for the domain overlay and the contract repo
(client/customer `overlay_ref`s point at the openxFactory contract pin's
neutral templates); and `overlay_ref` names a **repo+rev, not a file**, so the
loader needs a role→overlay-path convention (domain:
`hermes/domain/overlay.yaml`). Consequence: the Domain layer is the only role
with first-class seedable overlay content today; client and project content
arrive by the wizard and archetype paths below.

## Seeding readiness by layer (as of 2026-07-22)

What each layer role has and lacks before it can seed — the entry criteria the
staging split inherits:

| Readiness | Domain (codexFactory) | Client | Project/Subject |
| --- | --- | --- | --- |
| Seedable `overlay_ref` | ✅ `git+codexFactory@<rev>` | ❌ points at the neutral contract pin, not a seedable overlay | ❌ same |
| Digest pin recorded | ✅ compatibility manifest `domain_overlays[]` | ✅ `contract_repository` (but nothing seedable behind it) | ✅ same |
| Role→overlay-path rule | ✅ `hermes/domain/overlay.yaml` | ❌ none — seeding REFUSEs by design | ❌ none |
| Schema / validator | ⚠️ runtime minimal structural check only; no neutral `hermes_domain_overlay` contract | ❌ wizard output shapes have no validators | ❌ no archetype schema |
| Content | ⚠️ 32-line structural stub; `roles/` `policies/` `review-councils/` etc. empty | ⚠️ scaffold labels, no policy text; arrives via wizard | ⚠️ `subject/template.yaml` stub; arrives via archetype at `provision-project` |
| Runtime load path | ✅ increment 1 (read-only) live | ❌ arrival path is the wizard, not the seeder — see open question | ❌ arrival path is `provision-project` + archetype |

Reading: the Domain column is plumbing-complete and content-empty — authoring
`hermes/domain/` is the highest-leverage next act. The Client and Subject
columns fail at the first row: whether they ever get a seedable `overlay_ref`
(vs. their content arriving only by wizard/provisioning writes) is an open
question in `hermes-layer-seeding-mechanism.md`.

## Two axes: composition vs. runtime content loading

Two independent questions hide inside "set up the layers," and keeping them
apart is what makes the seam decision tractable:

- **Axis A — composition (build/install time):** how the install config is
  *assembled* from stacked, pinned sources. A Kustomize-style overlay chain;
  this repo already works this way for deployment (`deploy/kubernetes/base` +
  `overlays/aks-qa`, rendered deterministically and digest-pinned).
- **Axis B — runtime content loading:** what the *running* Hermes does with the
  assembled content — materialize it into records, or hold a pointer. This is
  the § Central seam.

They are orthogonal, but Axis A constrains Axis B (see the seam recommendation).

### The composition stack (Axis A)

| Tier | Repo | Owns | Status today |
| --- | --- | --- | --- |
| Ops engine | `opensoft/Hermes-Install-Core` | infra (Bicep), k8s foundation templates, deploy/cutover, backup/restore/DR, secret materialization, migration *validation* — for a **single** Hermes | Exists; **not referenced** by this repo |
| 3-layer runtime + generic config | `xFactory-Hermes-Install` (this repo) | FastAPI runtime, layer model, migrations `0001–0008`, lifecycle CLI, xFactory-common config | Exists; carries its **own** deploy + backup/restore/DR, **duplicating** Core |
| Domain overlay (content) | codexFactory `hermes/` | codex personality / policy / memory / practice catalog | Stubs only |
| Client + Project (content) | `config/clients/<client>/` + project-type templates | per-client policy, per-project-type scaffolds | Structural only |

`Hermes-Install-Core` is the generic single-Hermes **operational** engine — its
own description: "Shared Hermes prod/nextest install + migration engine consumed
by tenant Hermes-Install repos." It is deploy/backup/restore/DR plumbing (Bash +
Bicep + k8s templates: `deploy-prod-dark.sh`, `restore-prod-from-blob.sh`,
`materialize-prod-secrets.sh`, `validate-prod-migration.sh`, …), **not** a
runtime app or schema. It is distinct from the `FarHeap/Hermes-Install`
single-layer *product* the README warnings name — but two seams must be
reconciled before wiring: its README is still FarHeap-flavored, and it points at
**`openWorkflow`** for canonical policy, a different governance universe than
`openxFactory`.

"Should reference Core" concretely means: this repo currently **re-implements**
Core's operational surface (its own `deploy/compose` + `deploy/kubernetes`, and
backup/restore/rollback/DR/upgrade runbooks). Wiring to Core = reconciling those
two parallel ops implementations so the generic single-Hermes plumbing comes
from Core and this repo keeps only the 3-layer-specific additions — an ops-tier
refactor, independent of the content work.

Keep two "cores" distinct: **Hermes-Install-Core** (the ops engine, exists) is
NOT a shared **runtime-app core** (a future extraction of `src/hermes_install`
that both a single-layer and the 3-layer install could consume — does not exist;
see Open questions). The content axis (domain → client → project) sits entirely
*above* Core: Core deploys a Hermes, it does not govern one.

## Two senses of "memory" — keep them separate

There is a **ratified** neutral memory model already: the customer memory
gateway (`openxFactory/docs/customer-memory-gateway-architecture.md`, ratified;
contracts under `openxFactory/contracts/memory-gateway/`, standard). That is an
**access/routing gateway** — ports, consent, promotion, provider bindings — to
memory that lives in external providers. It is NOT layer-seed content, and this
brainstorm must feed INTO it, never around it.

"Seeding memory" here means the *initial* contents a layer starts with — the
priors, boundaries, and standing knowledge — expressed as the gateway's own
bucket/promotion vocabulary, not a parallel store. The client scaffold already
names the buckets (`client_private_memory`, `customer_relationship_memory`,
`domain_learning_candidates`, `current_state_evidence`) in
`openxFactory/templates/client-layer/product-service-scaffold.yaml`. Note the
runtime gap: `installs/hermes-install` has **no memory table at all** yet, so
"where seeded memory persists" is an open decision (§ Central seam) that must
land compatibly with the gateway.

## The prescribed shape already exists (draft) — fill it, don't invent it

`openxFactory/docs/xfactory-domain-factory-model.md` (Status: draft) already
prescribes the per-layer content directory a domain repo should carry:

```text
hermes/
  domain/    overlay.yaml  roles/  policies/  review-councils/
             memory-boundaries.yaml  escalation-rules.yaml
  client/    template.yaml  memory-boundaries.yaml
             policy-overrides.yaml  integration-boundaries.yaml
  customer/  template.yaml  memory-boundaries.yaml  consent-model.yaml
```

codexFactory ships only the stubs: `hermes/domain/overlay.yaml`,
`hermes/client/template.yaml`, `hermes/subject/template.yaml` (naming skew
resolved 2026-07-22: `subject/` wins; the prescribed model doc is to be updated
from `customer/` — see §Decided). The `roles/`, `policies/`, `review-councils/`,
`memory-boundaries.yaml`, `escalation-rules.yaml`, `agent-mixes.yaml`, and the
whole `customer/` tree are **empty**. This brainstorm is largely "fill those
files with real content and wire a loader," aligned with the draft model rather
than competing with it.

## Layer 1 — Domain (codexFactory): authored once, identical for every install

The Domain Hermes is the expert. For codexFactory it is "how a Software
Engineering organization thinks": review standards, what a good PR is, the
agent roster and their reasoning mixes, the escalation rules, and the
**practice catalog** (`domain-practice-suggestion-generation.md`). This content
is *domain-owned and install-invariant* — every codexFactory install, for every
client, gets byte-identical domain content; it changes only by re-pinning to a
newer codexFactory revision.

- **Home:** the codexFactory repo, `hermes/domain/` per the prescribed shape.
  Authored through codexFactory's own OpenSpec/ratification — a domain staking
  its reputation is a contract change (echoes the "who signs the catalog"
  question in `domain-practice-suggestion-generation.md`).
- **Distribution:** already solved by the pin. The install's Domain-layer
  `overlay_ref` points at `git+codexFactory@<rev>`; seeding = loading that
  overlay's content into the runtime after `register-stack`. This is exactly
  the "codexFactory overlay applied after the install" the request anticipated.
- **Contents (personality):** a domain persona/system-frame (the genuine void —
  no persona text exists anywhere today except the unrelated avatar UI persona
  schema), role definitions with reasoning-mix profiles (`agent-mixes.yaml`),
  policy priors, review-council composition, escalation rules.
- **Contents (memory):** domain memory boundaries — what the domain remembers
  across all clients (e.g. practice-effectiveness signal) vs. what stays
  client-private. Feeds the gateway's `domain_learning_candidates` promotion
  path; the domain may *learn* only through the promotion gate, never by
  reaching into a client's private memory.

## Layer 2 — Client (Company Policy): neutral scaffold + defaults + policy wizard

The Client Hermes answers "is this allowed *here*?" (the clearance role in
`practice-clearance-and-project-realization.md`). It is client-specific, but
every client starts from the same neutral default and is then *tuned* by
loading that client's actual policies.

- **Scaffold (exists, draft):**
  `openxFactory/templates/client-layer/product-service-scaffold.yaml`
  (`kind: xfactory_client_hermes_product_service_scaffold`) already provides
  offer shapes, ~18 agent roles (incl. `client_memory_steward`,
  `practice_gap_auditor`), skill/interaction scaffolds, the liaison profile
  (`default_state: configured_but_inactive` + activation gate), and the memory
  buckets. It carries structure and role *labels* but no policy *text* — the
  defaults are governance-shaped blanks.
- **Domain specialization:** codexFactory refines the neutral scaffold via
  `hermes/client/{template,policy-overrides,integration-boundaries}.yaml`
  (prescribed, unfilled) — e.g. an engineering-org client cares about repo
  boundaries and runner spend.
- **The wizard (new):** a guided elicitation that turns the scaffold's blanks
  into a real client policy set — repo-boundary policy, credential posture,
  spend ceilings, security posture, named approvers, escalation path — and
  writes them into the per-client tree (`config/clients/<client>/`, the same
  tree the self-client already uses). Its most load-bearing output is the
  **auto-clear envelope** the clearance brainstorm needs: the wizard is how a
  client's "likely-yes" middle gets defined without hand-authoring rules-as-code
  from scratch. Defaults are conservative (everything parks for the human
  liaison until a policy is set), so an un-tuned client is safe, just manual.
- **Re-tuning:** loading updated policies is idempotent re-seeding — the same
  verb, re-run; the liaison's accreted dispositions (from the clearance
  brainstorm) are candidate inputs a later wizard pass can absorb.

## Layer 3 — Project/Customer: a library of project-type templates

The weakest area today — only `hermes/subject/template.yaml` naming
`subject_kinds: [project, repository, product, feature_initiative]` and
required fields; `provision_project.py` scaffolds structure only. The request
is right that projects are not uniform: a microservice repo, a shared library,
a CLI, an infra/monorepo, a spike — each wants different default policy,
default practices, workflow selection, and memory/consent posture.

- **Project-type template library (new):** a set of archetypes, each a content
  bundle: default project policy, default practice-adoption expectations
  (which domain practices a project of this type is expected to realize),
  workflow selections, memory boundaries, consent model.
- **Ownership:** project *types* are domain knowledge (a "microservice repo" is
  a Software-Engineering concept), so the library is **codexFactory-owned**
  under `hermes/subject/templates/<type>.yaml`, with the neutral *schema* in
  openxFactory (same split the practice brainstorm uses: domain owns the
  catalog, openxFactory owns the shape). This keeps every domain's project
  templates legible to the client policy layer.
- **Provisioning flow:** `provision-project` gains a `template` selection →
  materializes the Customer layer from the archetype → tuned by project
  specifics (the repo, its branch-protection state, its team). Today's
  `*.params.yaml` project entries (`layer_id`, `display_name`, `project_ref`,
  `policy_namespace`, `overlay`) are the thin structural half; the archetype is
  the content half.
- **Project-layer agents (captured):** projects also carry their own agents — the
  first raised is a **documentation help/manual writer** (produces the project's
  user-facing manuals/help). Likely a **Plane-2 worker**, distinct from the
  domain's `documentation_agent` (which verifies doc/traceability changes). A
  project roster is a separate workstream from the domain roster
  (`codexfactory-domain-roster-draft.md`); resolve the persona-vs-worker call
  when it's drafted.

## The neutralization gradient (how much of each layer is neutral)

The three layers neutralize to very different degrees, and getting this right
decides where each layer's roster lives:

- **Client layer — highly neutral.** Operating organizations are structurally
  alike (all have policy, approvals, legal, reputation, liability, security,
  delivery, customer functions), so the client house-team roster is neutral
  (openxFactory scaffold), domain-*specialized*, client-*tuned*.
- **Domain layer — not neutral (domain-owned).** Expertise does not generalize —
  a Software Engineering roster is codex-specific by definition.
- **Customer/Subject layer — least neutral.** The subject is what most defines a
  domain, ranging from a person with rights (a patient) to an inert artifact (a
  repo), so the roster is domain-specific; only a *loose* functional skeleton
  (intent-owner / journey-coordinator / rights-consent-advocate) is neutral, and
  even its slot prominence varies (a Patient Advocate is central in Medx, near-
  absent in codex). Detailed in `project-layer-scaffold.md`.

## The central seam: does Hermes load `overlay_ref`, or stay a pointer?

This is the one decision everything else hangs on. Three options:

1. **Interpret-at-load (materialize):** a new `seed-layer-content` lifecycle
   step fetches the pinned overlay, validates it, and writes content-bearing
   records into the runtime (new tables, or the gateway's memory store). Pro:
   content is queryable, auditable, and enforced in-runtime. Con: new schema;
   must reconcile persistence with the ratified gateway.
2. **Pointer-only (interpret-at-use):** content stays in git behind
   `overlay_ref`; agents read it at job time via the pin. Pro: no new
   persistence, zero drift from source. Con: no in-runtime enforcement of
   policy/memory boundaries; the DB stays content-blind.
3. **Hybrid:** materialize the *enforceable* slice (policy envelopes, boundaries,
   consent models — the things gates must check) into records; leave *reference*
   content (persona text, role prose) behind the pin. Mirrors how the practice
   brainstorm already earmarks the empty
   `hermes_approval_requests`/`hermes_approvals` tables for the enforceable
   clearance output while keeping rationale as reference.

**Recommendation: hybrid — and Axis A forces it.** Because content is composed
by a deterministic, digest-pinned overlay stack (Axis A) and the whole reason
for the three layers is governance *gates* (cross-layer isolation, clearance,
dispatch disablement) enforced at write time, the other two options break:

- **Pointer-only fails on enforcement.** Policy that lives only in git behind an
  `overlay_ref` cannot be gated by the runtime — the `layer_id` FK and
  `hermes_cross_layer_bindings` have nothing to check against. Governance that
  is not in the runtime is not enforced.
- **Full-materialize fails on the ratified gateway.** Dumping persona prose and
  role descriptions into the DB duplicates content the memory gateway says lives
  in external providers, and none of it needs write-time enforcement.
- **Hybrid fits both** the overlay-composition model and the existing
  render/pin discipline: compose the full bundle at build time, seed only the
  enforceable slice into records, keep reference content behind the pin. It is
  the only option consistent with Axis A — Core or no Core, since the content
  axis sits entirely above the Core ops tier.

The *authoring* counterpart of this seam — what to write into stored policy at
all versus leaving it to the model on the fly — is worked out in
`codexfactory-domain-policy-model.md`: store the delta (choices, bindings,
boundaries, staked positions, learning), improvise the textbook. Same line,
drawn once.

## Increment roadmap (the seam, sequenced)

The hybrid decision decomposes into increments; each is gated on a decision,
not just on the previous increment's code:

| # | Increment | Gated on | Status |
| --- | --- | --- | --- |
| 1 | **Read-only load path** — `seed-layer-content` verb: resolve pin → fetch → fail-closed digest verify → validate → evidence | — | **DONE 2026-07-22** (`archive/2026-07-22-add-seed-layer-content`) |
| 2 | **Materialize the enforceable slice** into runtime records | record-shape decision (generic content table vs. per-kind tables); *which* fields are enforceable (policy envelopes, boundaries, consent models) — and real domain content to materialize | next |
| 3 | **Memory-gateway binding** — seed initial memory boundaries/priors via gateway vocabulary | the runtime has no memory table; must land as gateway bindings, never a parallel store | after 2 |
| 4 | **Overlay-stack composition** — compose Core → xFactory → domain → client → project instead of single-layer load | compose-at-build vs. compose-at-seed; whether Client/Subject ever get a seedable `overlay_ref` | after 2 |
| 5 | **Re-pin / pin-range consent flow** | model decided (pin range, above); where ranges are recorded is open | after 2 |
| 6 | **Job-time loading of the reference slice** — agents read persona/prose at job time via the pin | role→path conventions beyond `overlay.yaml`; retrieval surface | parallel to 3–5 |

Increment 2 is the critical path — and it is content-starved, not
code-starved: with only a 32-line domain stub there is nothing enforceable to
materialize. Author `hermes/domain/` first (the domain-content-authoring
staging topic), then cut increment 2 against real content.

## Where it lives (answering "hermes-install or a codexFactory overlay?")

Both — split by ownership, which the layer model already dictates:

| Piece | Home | Why |
| --- | --- | --- |
| Domain content (persona, roles, policies, practice catalog) | codexFactory `hermes/domain/` | install-invariant, domain-owned; shipped by pin |
| Neutral client scaffold + schemas | openxFactory `templates/client-layer/` + contracts | domain-neutral defaults; one shape for all |
| Client policy wizard + resulting client tree | hermes-install (runtime) + `config/clients/<client>/` | install-time act; per-client instantiation |
| Project-type template library | codexFactory `hermes/subject/templates/` (schema in openxFactory) | domain knowledge; neutral shape |
| The seeding/loading mechanism | hermes-install (runtime) | the runtime is what materializes content into the live stack |
| Ops/deploy/backup/DR plumbing | `Hermes-Install-Core` (once wired) | generic single-Hermes operational engine, shared by all tenant installs (Axis A base tier) |

So "a codexFactory overlay applied after install" is exactly right for the
Domain layer; the Client wizard and Project library are install-runtime acts
consuming domain-authored and neutral scaffolds; and the operational base they
all deploy onto belongs in `Hermes-Install-Core` (see the composition stack).

## Pilot sketch (opensoft self-client, cheapest honest first run)

1. **Fill one domain slice:** author codexFactory `hermes/domain/policies/` +
   a minimal persona for the Software Engineering domain; nothing loaded yet —
   pure content, ratified in codexFactory.
2. **Seed it read-only:** teach the runtime to fetch + validate the Domain
   `overlay_ref` and expose it (option 2 first — no new tables), proving the
   load path against the already-live opensoft QA stack. *(DONE 2026-07-22:
   `add-seed-layer-content` + Speckit 002, merged and archived.)* Note steps
   are intentionally out of order: step 2 landed before step 1's content
   exists — the loader is proven against the 32-line stub.
3. **Wizard the client on one policy:** run the client wizard for just the
   repo-boundary + PR-only realization policy, write it to
   `config/clients/opensoft/`, and let it define the first auto-clear envelope
   the clearance brainstorm consumes.
4. **One project archetype:** define a single "governed-docs repo" project type,
   provision `project-alfa` from it, and confirm its default practice-adoption
   expectations line up with the existing doc-health sweep.

## Open questions

- ~~**Persistence of seeded content**~~ — DECIDED 2026-07-22: hybrid (§Decided).
  Still open within it: the record shapes for increment 2 (generic vs.
  per-kind tables) and exactly which fields count as the enforceable slice.
- **Persona representation:** is a Hermes-layer "personality" a system-prompt
  document, a structured trait/policy set, or both? Substantially answered by
  `hermes-persona-character-model.md` Option E (trait-axis spine + authored
  prose for flagships); what remains is the on-disk file shape in `roles/`.
- ~~**Naming**~~ — DECIDED 2026-07-22: `subject/` wins; update
  `xfactory-domain-factory-model.md` from `customer/` (§Decided).
- **Neutral overlay contract:** no `hermes_domain_overlay` schema (or
  machine-readable role→overlay-path declaration) exists in openxFactory
  contracts — the seeding verb ships a minimal structural check until one lands.
  Should the neutral layer-content schemas feat above cover both?
- **Wizard authority:** who may run the client wizard and ratify its output —
  the company-policy liaison (Brett in the self-client)? Does a policy change
  need the same thin-independent-approval floor the install already recorded?
- ~~**Domain content upgrade**~~ — DECIDED 2026-07-22: pin-range consent
  (§Decided). Still open: where pin ranges are recorded and enforced
  (compatibility manifest vs. a consent record) — increment 5.
- **Project template drift:** if the archetype changes after a project is
  provisioned, does the project re-seed, or is the archetype a one-time stamp?
- **Core integration + lineage:** how does this repo consume
  `Hermes-Install-Core`'s ops engine (submodule? pinned script package? extracted
  shared library?), and how is the `openWorkflow`↔`openxFactory` governance
  lineage reconciled — Core evolved in the FarHeap/openWorkflow universe, this
  repo in openxFactory. Which deploy/backup/DR surface is authoritative when the
  two currently overlap?
- **Runtime-app core extraction:** should the generic runtime
  (`src/hermes_install` engine + base schema/migrations) *also* be extracted into
  a shared runtime-app core that both a single-layer and the 3-layer install
  consume, or stay in this repo while only the ops tier (Hermes-Install-Core) is
  shared? Distinct from Core-as-it-exists today (ops only).
- ~~**Split at staging**~~ — DONE 2026-07-22: staged as three exit-oriented
  topics — `codexfactory-domain-hermes-content`,
  `layer-content-materialization`, `client-layer-tuning`
  (`ideation/staging/INDEX.md`). The project-template-library remains
  brainstorm-only (`project-type-template-library-draft.md`) and stages when
  the subject-layer work firms up.
