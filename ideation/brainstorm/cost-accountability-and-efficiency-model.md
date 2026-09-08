# Cost Accountability & Efficiency: clock-in, spend audit, and the accounting chain — Brainstorm

Status: brainstorm
Kind: architecture
Summary: Every agent action burns credits; today nothing judges whether the
spend was worth the outcome. This doc captures a three-layer cost-accountability
model raised during the roster review: Plane-2 workers **clock in/out with
their directing persona** (the manager judges credits-burned vs. action-taken);
the Domain Hermes carries an **efficiency mandate** with an audit-selection
algorithm that picks which recurring tasks to audit for cheaper execution and
feeds process updates back into the practice catalog; the **Client (tenant)
layer** runs a reporting-to-accounting function tracking company-wide costs and
**defines the tracking granularity the subject layer must honor**; and the
**Project/Subject layer** carries a project accountant tracking project and
sub-project task spend. Sibling of `codexfactory-domain-roster-draft.md`
(where the domain slice is captured; moved 2026-09-07 to
`opensoft/codexFactory@83c9c35a`); grandchild of
`hermes-layer-content-seeding.md`.
Topics: practice-adoption, cost-accountability, credits, clock-in, efficiency-audit,
practice-catalog, domain-hermes, client-hermes, project-hermes, accounting,
spend-tracking, granularity-contract, layer-content-seeding
Repository context: openxFactory (spans domain/client/subject content + hermes-install runtime evidence)
Captured: 2026-07-22

## Possible feats

- **Clock-in/out protocol** — worker action reports `(action, credits_burned,
  outcome)` to its directing persona; rides the bidirectional
  persona↔worker references decided in the roster draft.
- **Manager spend judgment** — the directing persona's appropriateness check
  (was this spend right for this outcome?), with park/flag on egregious skew.
- **Efficiency-audit selection algorithm** — which tasks get audited: highest
  total spend, highest variance vs. estimate, most-repeated; owned by the
  domain (owner persona open).
- **Process-update loop** — audit findings become practice-catalog updates /
  policy-position proposals (through the normal ratification paths).
- **Client accounting function** — tenant-level reporting-to-accounting role
  tracking company-wide costs across projects.
- **Project accountant** — project-layer role tracking project and
  sub-project task spend.
- **Granularity contract** — the tenant layer declares the cost-tracking
  granularity the subject layer must honor (per-task? per-job? per-worker-run?);
  a neutral schema so every domain reports costs the same shape.

## The chain, by layer

| Layer | Function | Judges |
| --- | --- | --- |
| Domain (Plane-1 personas) | managers receive clock-ins; efficiency mandate + audit algorithm | is the spend appropriate for the action? is there a cheaper way? |
| Client (tenant) | reporting-to-accounting; company-wide cost tracking; **sets granularity** | are projects within envelope? where does money go across the company? |
| Project/Subject | project accountant; per-task and sub-project tracking at the tenant-set granularity | is this project on budget? which tasks are expensive? |

The wizard's spend ceilings (client-policy-wizard) are the *envelope*; this
model is the *ledger and the judgment* inside it.

## Fit with what exists

- **Budget primitives exist at the bottom:** the runtime already enforces an
  operator-action budget (`lifecycle/budget.py`), and jobs carry envelopes —
  but nothing aggregates spend upward or judges it.
- **Evidence discipline exists:** clock-in records are evidence-shaped
  (redacted, idempotent) — same convention as seeding/lifecycle evidence.
- **Enforceable slice:** spend ceilings and granularity contracts pass the
  store-vs-improvise test (enforceability, our-way choice) and materialize as
  `layer_content` records; the audit algorithm's *parameters* are domain
  policy; per-run judgments are memory (worker proposes, Lead accepts).

## Open questions

- **Audit-algorithm ownership** — Scrum Coordinator (process/flow) vs. Lead
  Engineer (lane throughput) vs. a new persona?
- **Credits unit** — tokens? normalized cost? wall-clock? one unit across all
  layers or per-layer with exchange rates?
- **Clock-in transport** — evidence records through the runtime vs. gateway
  memory entries vs. both (enforceable ledger + learned patterns)?
- **Judgment consequences** — what happens when a manager flags
  inappropriate spend: park the worker class, tighten its envelope, or just
  accumulate signal for the next audit?
- **Granularity floor** — is there a neutral minimum granularity every tenant
  must accept (so cross-client domain learning about efficiency stays
  possible)?
- **Estimate source** — variance-vs-estimate needs estimates; who produces
  them (decomposer worker? the manager persona at approval time?)?
