# codexFactory Domain Hermes Content & Roster: what the Software Engineering domain layer stores and decides — Brainstorm

Status: brainstorm
Kind: architecture
Summary: Fills the Domain (Software Engineering) portion of the three-layer
Hermes install for codexFactory — the Plane-1 **authority personas** that
decide, plus the domain policy, memory boundaries, review-council/gate-rule
contributions, and practice catalog they need. The execution **workers**
(Plane 2) stay in the Omnigent install and are deliberately kept out of this
Hermes content; the MoA advisory ensembles (Plane 3) have an unresolved home.
Most of this content already exists but scattered (role docs, the Omnigent
overlay, working scripts, proposed changes) — filling the domain layer is
mostly consolidating and elevating it into the prescribed `hermes/domain/`
shape, plus authoring the genuine voids. Child of `hermes-layer-content-seeding.md`;
the persona-depth question is spun out to `hermes-persona-character-model.md`.
Topics: codexfactory, domain-hermes, three-layer-hermes-runtime, agent-roster,
authority-personas, scrum-coordinator, merge-master, gate-rules-council,
review-council, practice-catalog, omnigent-separation, moa-advisory,
layer-content-seeding
Repository context: openxFactory (targets codexFactory hermes/domain/ + omnigent/)
Captured: 2026-07-21
Updated: 2026-07-22 (Plane-3 / human-step / scrum-boundary decisions; harvest map, practice matrix, exit path)

## Decided (2026-07-22)

- **Plane-3 home: split.** The MoA mix *profile* is governed domain content in
  `hermes/domain/agent-mixes.yaml`; the ensemble *execution* stays in the
  Omnigent install. Same advises/decides seam as the mantra.
- **Gate-Rules Council human step: acknowledgement.** A non-blocking "here are
  the gate rules for your project" notice the human registers — not a formal
  approval. (If a later rule change would *weaken* a gate, escalation semantics
  can be revisited; the default is acknowledgement.)
- **Scrum boundary: the changes-vs-operates test.** Anything that *changes how
  the team works* (cadence, WIP limits, ceremony definitions, process policy)
  is a Scrum Coordinator decision (domain persona); anything that *operates the
  current process* (scheduling, board updates, tracking, reminders) is the
  Scrum Master worker (Omnigent). Edge cases park with the Coordinator.

## Possible feats

- **Harvest roles → `hermes/domain/roles/`** — turn the prose role tables
  (`engineering-roles-and-authority.md`) into domain-persona objects.
- **Consolidate policy → `hermes/domain/policies/`** — fold the draft
  `engineering-*.md` docs into structured domain policy.
- **Author `hermes/domain/memory-boundaries.yaml`** — the domain's cross-client
  learning vs. client-private split, feeding the ratified memory gateway.
- **Declare `hermes/domain/agent-mixes.yaml`** — make the review-lane ensemble
  a declared MoA profile (resolves Plane 3's Hermes-side home).
- **Scrum Coordinator persona (domain) + Scrum Master worker (omnigent)** — the
  process-facilitation split.
- **Cross-layer Gate-Rules Council + human-acknowledgement flow** — how per-repo
  merge/gate rules get defined and noticed to a human.
- **Practice catalog** — `adoption_profile`s over the promoted capabilities.

## Three planes, and where each lives (the separation)

"Personalities/agents for the domain" is three different things, and the
boundary between them is load-bearing (the MoA mantra: *Mixture of Agents
advises, Hermes roles decide, openxFactory enforces the workflow rail*):

| Plane | What it is | Home | This doc |
| --- | --- | --- | --- |
| **1 — Deciders** | Hermes authority personas that decide/approve/escalate | **`hermes/domain/`** (Domain Hermes content) | **focus** |
| **2 — Workers** | bounded execution agents that do the work | **Omnigent install** (`omnigent/domain-overlay.yaml`) | out of scope; kept separate |
| **3 — Advisors** | MoA ensembles that advise a decider | **unresolved** — see open questions | flagged |

Plane 2 already exists as the 9 Omnigent agent classes (`engineering_decomposer`,
`coding_agent`, `test_agent`, …) with responsibilities + permissions in
`codexFactory/omnigent/domain-overlay.yaml` and `profiles/software-team.yaml`.
**We do not move those into the Hermes layer.** The domain Hermes *references*
them (routing, capability requirements), but the workers are Omnigent-owned. Any
worker discussion in this cluster is explicitly about the Omnigent install, not
this content.

## What the Domain Hermes stores (Plane-1 content map)

Prescribed shape (`xfactory-domain-factory-model.md`, "a domain Hermes overlay
owns"); today only `overlay.yaml` exists.

| File | Content | Source |
| --- | --- | --- |
| `overlay.yaml` *(exists)* | domain identity, approval scopes, authority boundaries | keep — note: its `hermes_domain_overlay` kind has **no neutral schema** in openxFactory contracts yet; the seeding verb validates it by a minimal structural check until one lands |
| `roles/` *(new)* | the Plane-1 persona roster (below) | harvest `engineering-roles-and-authority.md` |
| `policies/` *(new)* | the stored *delta* — binding choices, enforceable rules, fail-closed boundaries, staked positions (not generic best practice) | `codexfactory-domain-policy-model.md` |
| `review-councils/` *(new)* | per-PR merge-readiness council + the Gate-Rules Council seat | `codexfactory-domain-deliberation.md` |
| `agent-mixes.yaml` *(new)* | MoA mix profiles (Plane 3 Hermes side) | `codexfactory-domain-deliberation.md` |
| `memory-boundaries.yaml` *(new)* | domain cross-client learning vs. client-private | `codexfactory-domain-memory-and-practices.md` |
| `escalation-rules.yaml` *(new)* | elevate the `routing:` + `stop_conditions:` | `codexfactory-domain-deliberation.md` |
| practice catalog *(new)* | `adoption_profile`s over promoted capabilities | `codexfactory-domain-memory-and-practices.md` |

## Harvest map (source → target, verified 2026-07-22)

The "exists but scattered" claim, made checkable — each target file, its actual
source artifacts in the codexFactory tree, and how the content moves:

| Target (`hermes/domain/`) | Source artifact(s) | Move |
| --- | --- | --- |
| `overlay.yaml` | itself (32 lines, live) | **keep**; tighten once the neutral schema lands |
| `roles/*.yaml` | `docs/engineering-roles-and-authority.md` (prose authority tables) + `codexfactory-domain-roster-draft.md` (persona objects) + Option E character model | **transform** — prose → persona objects; authority block is the enforceable slice |
| `policies/` | `docs/engineering-xfactory-domain.md`, `docs/engineering-omnigent-constitution.md`, `docs/engineering-worker-model.md`, `docs/spec-kit-engineering-flow.md` + the filled position table in `codexfactory-domain-policy-model.md` | **transform** — store-the-delta filter: only the binding positions move; the textbook prose stays behind |
| `review-councils/merge-readiness.yaml` | `docs/pr-admission-merge-readiness.md` (NOT a `merge-council.md` — none exists) | **transform** |
| `review-councils/gate-rules-seat.yaml` | none — the Gate-Rules Council is new (§Merge Master reframe); `scripts/merge_master/envelope.py` is the enforcement artifact the council's output feeds | **author new** |
| `agent-mixes.yaml` | `profiles/software-team.yaml` (ensemble shape) + the review-lane ensemble config | **transform** — declare as MoA profiles; execution stays Omnigent (§Decided) |
| `escalation-rules.yaml` | `omnigent/domain-overlay.yaml` `routing:` (~L157) + `stop_conditions:` (~L165) | **transform** — remap onto roster personas |
| `memory-boundaries.yaml` | none (gateway vocabulary exists; no domain instance) | **author new** |
| practice catalog | promoted openxFactory capabilities (below) + adoption-profile shape from `codexfactory-domain-memory-and-practices.md` | **author new** (structure), harvesting capability names |

Rows with no source are the genuine voids: the Gate-Rules Council seat, domain
memory boundaries, and the practice catalog structure. Everything else is
consolidation.

## Per-Lead practice ownership (draft answer to the ownership question)

Each Lead owns the adoption profiles in their area — drafted against the
capabilities promoted in openxFactory as of 2026-07-22:

| Capability (promoted) | Owning Lead |
| --- | --- |
| doc-health | Lead Quality |
| document-lifecycle, document-cataloging | Lead Quality |
| workflow-gate-contract | Lead Integration |
| release-realization | Lead Release |
| credential-contracts | Lead Security |
| repo-boundary-governance | Lead Security |
| neutral-job-envelope | Lead Engineer |
| roles-authority-model | Lead / Chief Architect |
| shared-contract-ownership | Lead / Chief Architect |
| memory-gateway (consumption practices) | Scrum Coordinator? — no natural Lead; candidate roster-gap signal |

Rule this table encodes: **a promoted capability with no natural owning Lead is
a roster-gap test**, not something to force-fit. The catalog is signed
per-profile by its owning Lead; the catalog *as a whole* is a domain
ratification (the "who signs" question in the memory-and-practices doc).

## The Plane-1 roster (domain deciders + coordinator)

The seven engineering Leads from `engineering-roles-and-authority.md`, plus a
Scrum Coordinator, with authority scoped by `overlay.yaml`'s `codex_owns`:

| Persona | Owns / decides | Notes |
| --- | --- | --- |
| Lead / Chief Architect | architecture decisions; resolves architecture ambiguity | consistency over speed |
| Lead Engineer | execution lane; feature-decomposition acceptance | throughput within scope |
| Lead Coder (Coding-Agent Manager) | bounds and manages the coding workers | small, reversible changes |
| Lead Quality | quality gates; review standards | evidence before trust |
| Lead Security | security posture; resolves security ambiguity | fail-closed, skeptical |
| Lead Integration | integration; merge-readiness summary | no side-channel writes |
| Lead Release | release readiness; versioning; release notes | ship-but-safe; recommendation only, deploy stays repository/external |
| **Scrum Coordinator** *(new)* | cadence, ceremonies, flow/WIP, cross-persona coordination | domain-level *facilitation*, not authority over engineering decisions — see scrum split |

**Excluded from the domain roster (per steer):**
- **Product Owner → Customer/Project layer.** Owns the *what/why*, not the domain's *how*.
- **Project Manager → Project layer** specifically.
- **Scrum Master / Agile Master → Omnigent (Plane 2 worker).** The coordinator *decides* process; the scrum-master *worker* runs the mechanics (board updates, ceremony scheduling, tracking). Coordinator = domain Hermes; master = omnigent execution.

## Merge Master and the Gate-Rules Council (reframed)

Correcting the earlier framing: **Merge Master is not a decider persona.** It is
a **mechanical, technical gate-driven merge operator** living in a GitHub App —
it enforces the per-repo merge/gate rules and performs the merge. It belongs to
**external enforcement / the Omnigent-and-infra tier**, not the Hermes roster.
(Its autonomous-approval envelope, `scripts/merge_master/envelope.py`, is the
rules-as-code it executes.)

The *authority* is elsewhere: the **per-repo merge/gate rules** are the governed
artifact, and they are **defined by a cross-layer council (Domain + Client +
Customer/Project) plus a human**. The human step is likely **acknowledgement of
a notice** rather than formal approval — a "here are the gate rules for your
project" notice the human on the project registers, not a blocking sign-off.

So the domain's Plane-1 contribution to merging is: **hold a seat on the
Gate-Rules Council** (bring engineering review standards + security posture to
rule definition) and run the **per-PR merge-readiness council** — distinct from
the rule-setting council. Merge Master then mechanically enforces whatever the
council + human-ack produced.

Distinguish two councils, currently blurred in the docs:
- **Gate-Rules Council** — cross-layer + human-ack; *sets* the per-repo rules. (New; the user's model.)
- **Merge-Readiness Council** — domain per-PR readiness review body (the existing `merge-council.md` concept).

## Persona character — its own question

How much *personality* each Plane-1 persona carries (technical disposition only,
vs. full character that makes human collaboration pleasant and lifts quality) is
brainstormed in **`hermes-persona-character-model.md`** — resolved to Option E
(trait-framework + authored prose + client-tunable voice), no house style at the
domain layer. The seven personas are drafted under that model in
**`codexfactory-domain-roster-draft.md`**.

## Open questions

- ~~**Plane 3 (MoA advisory) home**~~ — DECIDED 2026-07-22: split — profile in
  `hermes/domain/agent-mixes.yaml`, execution in Omnigent (§Decided).
- **Gate-Rules Council composition.** The human step is DECIDED
  (acknowledgement, §Decided); still open: exactly who sits from each layer.
- ~~**Scrum Coordinator vs. Scrum Master boundary**~~ — DECIDED 2026-07-22:
  the changes-vs-operates test (§Decided).
- **Roster completeness.** The domain decider set is now seven Leads (incl. Lead
  Release) + Scrum Coordinator. A project-layer **documentation help/manual
  writer** was raised — captured as a project-roster item (likely a Plane-2
  worker), separate from this domain workstream. The §practice-ownership table
  adds one signal: memory-gateway consumption practices have no natural owning
  Lead.
- **Practice-catalog ownership vs. the roster.** Structurally answered by the
  §Per-Lead practice ownership draft (each Lead owns their area; unowned
  capability = roster-gap test); the table itself still needs domain
  ratification.
- **Neutral `hermes_domain_overlay` schema.** Author it in openxFactory (with a
  machine-readable `overlay_path`) so every domain's overlay validates the same
  way — the seeding increment currently ships only a structural check.

## Exit path (concrete changes this cluster becomes)

1. **codexFactory OpenSpec increment A — `roles/` + `policies/`.** The
   enforceable-slice sources (persona authority blocks, binding policy
   positions). This is what the runtime's seeding increment 2 is starved for —
   highest leverage, propose first. Harvest per the §Harvest map.
2. **codexFactory OpenSpec increment B — councils + mixes + escalation +
   memory boundaries.** `review-councils/`, `agent-mixes.yaml`,
   `escalation-rules.yaml`, `memory-boundaries.yaml`, and the practice catalog
   skeleton with the §ownership table.
3. **openxFactory change — neutral `hermes_domain_overlay` schema** + a
   machine-readable per-pin `overlay_path`, replacing the runtime's minimal
   structural check. Independent of A/B; unblocks every other domain.

Sequencing: A → (B ∥ 3); the hermes-install materialization increment
(seeding increment 2) proposes against A's landed content.
