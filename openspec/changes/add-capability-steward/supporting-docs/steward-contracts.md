# Capability Steward Contracts — registry, dispatch, proof, health

Status: staged
Kind: architecture
Summary: Declares the ADDED `crystallized-capability-registry` (git-truth
records with a derived dispatch index, a document-lifecycle-mirrored status
spine, and the D10 rule that artifacts are digest-pinned while authority
status is live-read), the ADDED `crystallization-dispatch` junction (single
entry before planning, deterministic fences with effect-class admission,
post-conditions always, cause-tagged fallbacks, the L2-cache-behind-the-
junction seam rule), and the ADDED `capability-health` surface (proof
stages as gate instances with demotion bundles armed at promotion, the
mandatory sentinel policy, drift response ladder, and sentinel-anchored
accounting).
Topics: crystallized-capability-registry, crystallization-dispatch,
capability-health, scope-fence, post-conditions, sentinel-sampling, parity,
drift, accounting, automation-share, workflow-gate-contract, caching
Repository context: openxFactory (neutral contracts; hermes-install
admission is the first dispatch realization per D9)
Staging ID: `openxFactory:staging:recurrence-crystallization`
Source: brainstorm docs
[capability registry](../../../../ideation/brainstorm/crystallization-capability-registry.md),
[dispatch and fences](../../../../ideation/brainstorm/crystallization-dispatch-and-fences.md),
[parity and cutover](../../../../ideation/brainstorm/crystallization-parity-and-cutover.md),
[drift and lifecycle](../../../../ideation/brainstorm/crystallization-drift-and-lifecycle.md),
[learning loop](../../../../ideation/brainstorm/crystallization-learning-loop.md),
[accounting](../../../../ideation/brainstorm/crystallization-accounting.md),
[Steward synthesis](../../../../ideation/brainstorm/crystallization-synthesis-steward.md);
rulings D6, D9, D10, D11, V2 (primary doc, 2026-07-29).
Target capabilities: `crystallized-capability-registry` (ADDED),
`crystallization-dispatch` (ADDED), `capability-health` (ADDED)

## Registry (`crystallized-capability-registry`, ADDED)

One record per capability: identity, family refs, fence ref, rung, version
+ artifact digest, provenance ref, permission binding, consent scope,
measured cost profile, health snapshot, owner, dry-run declaration; status
spine `candidate → building → shadow → canary → active → degraded →
retired`, deliberately mirroring the document lifecycle (CR-C4). Rules:

- **Git truth, derived speed** (CR-C1): reviewable YAML with validators is
  the source of truth; the hot-path dispatch index is a governed derived
  projection, regenerated on change, never hand-edited.
- **Sole source** (CR-C2): dispatch reads only the registry; a capability
  absent from it does not exist operationally.
- **Digests, not payloads** (CR-C3): records reference evidence by digest;
  a registry leak leaks no tenant data.
- **D10 — pins vs authority**: capability *artifacts* are digest-pinned
  with deliberate re-pin (runtime-manifest style); *authority status* is
  live-read at the junction — a demotion or retirement takes effect at the
  next dispatch decision and never waits for a consumer re-pin.
- **D6 — residence**: neutral schema in openxFactory now; codexFactory is
  the first conformer (adoption-profile pattern). Field writes follow a
  declared authority matrix (build writes identity once; gates advance
  status; the steward writes health; accounting writes cost).

## Dispatch (`crystallization-dispatch`, ADDED)

The junction sits at job admission, **before planning**, and is the single
entry to every crystallized capability (DS-C1 — side-door invocation is a
conformance violation). Sequence: fingerprint → registry lookup → fence
check → instance risk check → execute at rung → post-conditions → emit with
provenance. Rules:

- **Fences are deterministic** (DS-C2); ambiguity resolves to the AI path;
  a classifier may veto toward fallback, never extend past the fence.
- **Effect-class admission (D11)**: v1 fences admit only families with
  `effect_class` ∈ {`pure`, `idempotent`}; `compensable`/`irreversible`
  are fenced out until compensation contracts exist — this is the packet's
  answer to partial-side-effect fallback.
- **Post-conditions always** (DS-C3): breaches fall back to AI *and* file
  drift signals.
- **Fallbacks are recorded** with a cause taxonomy (`no-family-match |
  fence-miss | execution-error | postcondition-fail | risk-override |
  sentinel`) and accumulate in the family's frontier queue (DS-C4).
- **Overhead is budgeted and metered** (DS-C5).
- **The L2 seam rule**: the result cache (ontology packet) is the L2 rung
  executed *behind* this junction; a cache reachable outside dispatch is a
  conformance violation.
- **D9**: the contract is neutral; hermes-install admission is the first
  realization. **V2**: no envelope delta this wave — fingerprints derive
  from existing fields; optional `family_hint` is a later MODIFIED
  `neutral-job-envelope` candidate.

## Proof, sentinels, health, accounting (`capability-health`, ADDED)

- **Proof ladder**: replay → shadow → canary, each a
  `workflow-gate-contract` instance with rung-scaled profiles (PV-C1);
  shadow requires the build's dry-run mode; demotion trigger bundles are
  armed at promotion (PV-C4); equivalence disagreements are bidirectionally
  adjudicated — capability, historical episode, or spec may be the one
  corrected — with one adjudication record kind shared with sentinels
  (PV-C3; LC-Q5 lean adopted).
- **Sentinels are mandatory** while a capability holds authority: adaptive
  ε with a nonzero floor, mode per family (dual-run / async replay /
  takeover), declared as exploration expense (LC-C2/C3; SYC-C3 — ε is the
  packet's most load-bearing policy number, staged in the dials register).
- **Drift** responds up a cost-ordered ladder with hysteresis — observe →
  shrink fence → regenerate → demote → retire (DL-C2/C3); capability-health
  findings split auto-actionable vs contested, doc-health style (DL-C4);
  dormant capabilities auto-propose retirement, lineage preserved (DL-C5).
- **Accounting**: savings credit only against sentinel-anchored
  counterfactuals — stale anchors report "unverifiable" (CA-C1); every
  ex-ante number is scored on maturity and feeds priors (CA-C2);
  automation share is the headline metric (CA-C3); the ledger rides the
  cost-accountability chain (CA-C5).
- **Renewal write-backs are contractual** (SYC-C2): fallbacks,
  adjudications, sentinel episodes, and scores flow back to the Pattern
  Ledger; a deployment without them is nonconformant.

## Open questions carried

Sync-path latency budget for interactive jobs (DS-Q3); subject-visible
provenance default vs tenant policy (DS-Q5); shadow-window statistics —
fixed N vs sequential tests (PV-Q1); long-horizon job shadowing (PV-Q3);
replay-only promotion for low-risk L3 (PV-Q4); `degraded` as status vs
health annotation (CR-Q3); version semantics on regeneration (CR-Q4);
Steward as role vs contract, and per domain vs per install (SYC-Q1);
capability-health surfacing on the dashboard/gate-console family (SYC-Q3).
