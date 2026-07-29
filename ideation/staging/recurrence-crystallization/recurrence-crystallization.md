# Staged: Recurrence Crystallization — repeated AI work into governed cheaper paths

Status: staged
Kind: architecture
Summary: Stages the crystallization flywheel as a neutral contract family:
every expensively-solved governed job leaves an episode; episodes cluster
into tenant-scoped recurrence families with volume and stability forecasts;
a budget-consented decision selects a rung on the frozen L0–L6 automation
ladder; Hermes mines the episode corpus into a micro-spec, acceptance
corpus, scope fence, and effect class; codexFactory builds the capability
as an ordinary governed job under authority conservation; and a single
dispatch junction serves future instances behind deterministic fences with
the AI path intact and a sentinel fraction keeping drift detection, corpus
freshness, and savings counterfactuals honest.
Topics: crystallization, pattern-ledger, crystallization-decision,
crystallization-build, crystallization-consent, crystallized-capability-registry,
crystallization-dispatch, capability-health, automation-ladder, self-learning,
memory-gateway, cost-accountability, omnigent-domain-overlay
Repository context: openxFactory (neutral crystallization contract family;
codexFactory is the first conformer and the cross-domain builder)
Staging ID: `openxFactory:staging:recurrence-crystallization`
Source: the 19-doc recurrence-crystallization brainstorm packet, anchored at
[crystallization-overview.md](../../brainstorm/crystallization-overview.md)
(captured 2026-07-28); decision session 2026-07-29 locking D1–D11 and
verifications V1–V2, recorded below.
Target capabilities: `pattern-ledger` (ADDED), `crystallization-decision`
(ADDED), `crystallization-build` (ADDED), `crystallization-consent` (ADDED),
`crystallized-capability-registry` (ADDED), `crystallization-dispatch`
(ADDED), `capability-health` (ADDED), `omnigent-domain-overlay` (MODIFIED:
crystallized-executor profile class + rung-ceiling declarations)

## What this stages

The factory already learns from repeated work (recall-assisted solving via
the memory gateway); this topic stages the missing consolidation stage —
usage becoming *procedure*, not only knowledge. The claims are carried at
full resolution in the source packet (84 claims / 84 open questions, each
individually addressable by per-doc ID prefixes: EL/TF/RF, EC/AL/RQ/BP/AU,
CR/DS/PV/DL/LC/CA, SYA/SYB/SYC); the fragments here restate only the
contract-shaping rulings and the delta surfaces.

## Decision record (2026-07-29)

| # | Decision | Ruling |
| --- | --- | --- |
| D1 | Wave scope | One topic, five fragments; cross-tenant pooling (XT) deliberately out of wave — its brainstorm doc stays active |
| D2 | v1 outcome labels | Define a minimal `outcome_label` event record now: source enum `praise \| gate_outcome \| correction \| adjudication`; praise becomes a record without waiting for a richer reward system |
| D3 | Family scoping | Tenant-scoped families; pooled twins deferred to the cross-tenant wave |
| D4 | Candidate record | Own `crystallization_candidate` kind, suggestion-grammar-shaped (idempotency, suppression, evidence-citing rationale) — no dependency on the unratified practice pipeline |
| D5 | Build topology | codexFactory builds for every domain; the consuming domain owns fitness gates (BP-C2) |
| D6 | Schema residence | Neutral schemas in openxFactory now, codexFactory first conformer (the adoption-profile pattern: schema neutral, content domain) |
| D7 | Rung vocabulary | `automation_rung` frozen as L0–L6 controlled vocabulary, semantics per the automation-ladder brainstorm |
| D8 | MVP family | Packet-capture mechanics at L3 (see MVP slice below); alternates: nightly-sweep triage prep, conformance-fixture regeneration |
| D9 | Dispatch placement | Neutral dispatch contract; hermes-install admission is the first realization |
| D10 | Demotion propagation | Capability *artifacts* are digest-pinned; *authority status* is live-read — a demotion takes effect at the next dispatch decision, never waits for a re-pin |
| D11 | Effect classes | `effect_class` vocabulary `pure \| idempotent \| compensable \| irreversible` declared per capability; v1 fences admit only `pure`/`idempotent` families |
| V1 | memory-gateway delta? | **No MODIFIED delta.** The M1 promotion requirement constrains the promotion *candidate record* (consent, de-identification, source refs, target layer, review metadata), not the promoted artifact's kind — a procedural promotion target is consumption |
| V2 | `family_hint` envelope field? | **Deferred.** Dispatch fingerprints from existing envelope fields; the optional `family_hint` is a later-wave MODIFIED `neutral-job-envelope` candidate |

## Fragment map

- [pattern-ledger-contracts.md](pattern-ledger-contracts.md) — the sensing
  contract family: episode, outcome-label, family, forecast, and candidate
  records (ADDED `pattern-ledger`).
- [crystallizer-contracts.md](crystallizer-contracts.md) — decision, spec
  mining, and governed build (ADDED `crystallization-decision`,
  `crystallization-build`).
- [authority-and-consent.md](authority-and-consent.md) — authority
  conservation and consent tiers (MODIFIED `omnigent-domain-overlay`, ADDED
  `crystallization-consent`).
- [steward-contracts.md](steward-contracts.md) — registry, dispatch, proof,
  health, accounting (ADDED `crystallized-capability-registry`,
  `crystallization-dispatch`, `capability-health`).
- [dials-and-defaults.md](dials-and-defaults.md) — the declared-dials
  register (defaults now, tenant/domain tuning later; no deltas).

## MVP slice (D8)

**Family: packet-capture mechanics, target rung L3 (frozen playbook).**
Evidence: two independent sessions performed the same job shape on
2026-07-28 alone — the ontology packet (12 docs) and the crystallization
packet (19 docs) — each running: author header-conformant brainstorm docs →
README anchor entry → index surfaces → explicit-path commit → push → parent
pointer sync. The *mechanics* are the family (a fragment family per TF-C4);
the authoring judgment stays L0/L1 and is out of the fence. Header
conformance is a mechanically checkable post-condition — a working checker
already exists as session scratch, i.e. the fence/post-condition prototype
predates the contract. The MVP runs under the first two exit changes with
manual steward stand-ins: episodes reconstructed retrospectively for this
family only, nomination by count threshold, human decision, replay parity
plus a human-compared shadow week, sentinel ε per the dials register.

## Out of wave

- **Cross-tenant pooling, platform capabilities, DTN promotion** —
  [crystallization-cross-tenant.md](../../brainstorm/crystallization-cross-tenant.md)
  stays active brainstorm; the T3 consent tier is defined now (so the enum
  never migrates) but unused this wave.
- **L2 result cache** — owned by the ontology packet's result-cache
  brainstorm; this topic consumes it as a rung behind the dispatch junction
  (seam rule in [steward-contracts.md](steward-contracts.md)).
- **Platform-actor naming** in the Subject/Tenant/Domain vocabulary (XT-Q2).

## Exit path

Three ordered OpenSpec changes: `add-pattern-ledger` (sensing contracts —
no spend, lowest risk) → `add-crystallizer-contracts` (decision + build +
authority) → `add-capability-steward` (registry, dispatch, proof, health).
A fourth, cross-tenant, follows in a later wave after a first domain proof.
The dials register feeds all three as declared dials
(governed-derived-model pattern).

## Spanning open questions (carried, non-blocking)

Dial tuning beyond staged defaults; adjudicator assignment by rung/risk
(PV-Q2); shadow-window statistics (PV-Q1); long-horizon job shadowing
(PV-Q3); replay-only promotion for low-risk L3 (PV-Q4); Steward as role vs
contract (SYC-Q1); dashboard/gate-console surfacing of capability-health
(SYC-Q3); praise vocabulary maturation beyond the v1 label enum (LC-Q3);
per-instance mixed-rung dispatch (AL-Q4); distillation as an L4 refinement
(AL-Q5); chargeback and the k-threshold (cross-tenant wave).
