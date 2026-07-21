# Omnigent Lane Activation Path: getting to Hermes-managed autonomous coding — Brainstorm

Status: brainstorm
Kind: plan
Summary: Defines the sequenced path from today (a Hermes governance/record plane
that is live, and an omnigent lane that only scaffolds + reviews) to the goal (an
omnigent execution lane that autonomously codes a change like seed-layer-content,
managed by the Hermes layers). Answers the ordering question: the Hermes runtime
*plane* is already up, but the Hermes layer *content* (seeded and enforceable) is
a hard prerequisite for a *managed* lane — the lane's authorization and clearance
are not real until policy content is seeded and gates enforce it. The omnigent
*execution machinery* can be built in parallel with that content; the two must
converge before the first managed run. The foundations are hand-built (Speckit +
operator) because the lane cannot build the plumbing it depends on; once the path
is live, the factory can self-host. Parent: `hermes-layer-content-seeding.md`.
Topics: omnigent-lane, execution-lane, hermes-managed, autonomous-coding,
job-dispatch, clearance, credentials, review-lane, merge-master, self-hosting,
sequencing, bootstrap
Repository context: openxFactory (roadmap spanning hermes-install runtime + codexFactory omnigent/review/merge)
Captured: 2026-07-21

## Possible feats

- **Seed + enforce Hermes content** (P1) — the authorize/clear prerequisite.
- **Governed job lifecycle** (P2) — approve → clear → authorized job envelope.
- **Omnigent run loop** (P3) — worker claim, scoped credential issuance, bounded execute, report-back.
- **Land merge-master + execution-lane past draft/simulated** (P4).
- **Self-host registration** (P5) — hermes-install/codexFactory as a governed subject.

## The two planes (why the question matters)

- **Hermes = the govern/record/authorize plane.** LIVE. Its runtime records
  jobs/runs/events, gates writes (dispatch *disablement* — a kill-switch, not a
  scheduler), registers workers, and enforces identity + layer isolation. It does
  not execute code — no job pickup, no clone, no run.
- **Omnigent = the execute plane.** Acts under a Hermes-authorized job and reports
  back into Hermes records. Today it is contract + scaffold + a piloted lane
  (`software-team-execution-lane` stops at a **draft PR** on **simulated** manager
  decisions) + the review-lane ensemble (which reviews, does not build).

"Managed by Hermes" = the lane runs a job that Hermes **authorized** (domain
policy) and the client **cleared**, under Hermes **gates**, reporting into Hermes
**records**. That is the lens for the ordering below.

## The ordering answer

- The Hermes runtime **plane** is already up — the necessary primitives exist.
- The Hermes layer **content** (seeded + enforceable) is a **hard prerequisite**
  for a *managed* lane: until the policy/clearance/authority content is seeded and
  the gates enforce it, Hermes can only *record*, not *authorize/clear* — so every
  job parks for a human (safe, but not autonomous).
- The omnigent **execution machinery** does **not** have to wait — it can be built
  in **parallel** with the content. It simply cannot *run a managed job* until the
  two converge (the worker needs an authorized+cleared job to claim).

So: not "all Hermes first" — but the **authorize/clear content (P1) must land
before the lane is managed**, and the execution machinery (P3) is built alongside.

## The path

| Phase | What | Depends on | State |
| --- | --- | --- | --- |
| **P0** | Hermes govern/record plane: jobs/runs/events, gates, worker register, identity, layer isolation | — | ✅ live (foundation) |
| **P1** | **Seed + enforce Hermes content** — seed-layer-content (read-only → materialize enforceable slice), author domain/client/project content so Hermes can *authorize* + *clear* | P0 | ⏳ seed-layer-content proposed; content in brainstorm |
| **P2** | **Governed job lifecycle** — engineering_intent approval → client auto-clear envelope (or human) → compose neutral-job-envelope + conditions | P1 (client clearance content) | ▫ approvals tables exist, flow unwired |
| **P3** | **Omnigent run loop** — worker *claims* an authorized job; scoped short-lived credential issuance (never standing); bounded execute (clone/code/checks per permission flags); content-only App opens the PR; report runs/events back | P0 primitives (parallel w/ P1–P2); converges at first run | ▫ worker register + App-identity-tiers + credential-contracts realized; claim loop + issuance unbuilt |
| **P4** | **Governed close** — governed-review-lane reviews the PR; gate-rules-council rules + Merge Master enforce/merge; evidence recorded | P3 (a PR to review) | ▫ review lane realized; merge-master proposed (not landed) |
| **P5** | **Self-host** — register hermes-install / codexFactory as a Customer/Project subject; route future changes through the lane | P1–P4 | ▫ future |

## Parallelization & convergence

- **Governance track (P1 → P2):** seed content, make it enforceable, wire the
  approve→clear→job flow. This is the track that makes management *real*.
- **Execution track (P3):** the worker claim loop, credential issuance, and the
  execute-and-report machinery — buildable now against P0 primitives.
- **Convergence:** the first *managed run* needs a P2 authorized/cleared job AND a
  P3 worker to claim+execute it. P4's review lane already exists; landing
  Merge Master closes the loop.

## Bootstrap note (why this is hand-built)

P1–P4 are foundations the operator + Claude Code build by hand (via Speckit),
because the omnigent lane cannot build the plumbing its own governance rides on
(seed-layer-content is the content loader; the claim loop is the lane itself).
Only at **P5** does the recursion close — the factory builds its *next* changes
through the lane it just gained (the self-hosting move named in
`hermes-governed-nightly-sweep.md`). seed-layer-content sits in **P1**: a
hand-built foundation, not a lane-built change.

## Open questions

- **Materialization depth for P1** — how much of the enforceable slice must
  materialize before the client auto-clear envelope can evaluate a real job?
- **Credential issuance (P3)** — does the runtime issue/attenuate short-lived
  worker credentials itself, or broker to an external vault (credential-contracts
  says references only)?
- **Claim vs. push dispatch** — does a worker poll/claim authorized jobs, or does
  Hermes push? (Claim fits the disablement-gate model.)
- **Merge Master landing** — is landing the proposed merge-master change part of
  P4, or a precondition?
- **First self-host subject (P5)** — hermes-install, codexFactory, or a low-risk
  sacrificial repo first?
