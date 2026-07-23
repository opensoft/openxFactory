# Tech-Stack Benches as Governed Worker Toolchains — Brainstorm

Status: brainstorm
Kind: architecture
Summary: Adopt the operator's proven tech-stack bench containers (flutterBench,
pythonBench, dotNetBench, cppBench, …) as the governed execution environments
for Omnigent workers — published to ACR with digest pins and machine-readable
bench manifests, declared per domain through the ratified overlay's
`toolchain_bindings` slot, selected per job by the worker harness, advertised
in the worker heartbeat, and pre-pulled onto worker hosts by an Intune-deployed
worker-host agent — replacing both ad-hoc native toolchains and hand-run host
setup.
Topics: tech-benches, toolchain-bindings, omnigent-domain-overlay,
worker-host-agent, intune, worker-heartbeat, bench-manifest, execution-lane,
containment, worker-hosts, cloudpc, omni-001, dtn-candidate
Repository context: openxFactory (neutral bench-manifest + heartbeat delta);
codexFactory `omnigent/` overlay (first `toolchain_bindings` consumer);
Omnigent-Install (harness selection, host manifest, heartbeat publisher);
OpsxFactory (bench build pipeline + Intune deployment)
Captured: 2026-07-23

## The idea

The operator already maintains per-tech-stack bench containers (flutterBench,
pythonBench, dotNetBench, cppBench, m365Bench, cloudBench, …): images
preloaded with every tool an AI agent needs for that stack, each describable
by a manifest that tells the agent its options without exploration. They
demonstrably speed up AI-assisted work. The proposal: make benches the
*governed* execution environment for Omnigent workers — a coding job runs
inside the bench matching its target repo's stack, not natively on the host.

Decision context (2026-07-23, Brett): pursue this, combined with Intune —
bench installation and refresh on worker hosts is managed deployment, not
hand-run setup.

## Why this is stronger than a convenience

1. **Speed** — pre-pulled benches remove per-job toolchain setup; the rider
   host spec (8 vCPU / 32 GB / 500 GB) was sized for local toolchains and
   caches from the start.
2. **The manifest is the prize** — a bench manifest (tools + versions +
   capabilities) gives the agent tool discovery AND gives the lane a
   machine-checkable claim about the environment a job ran in. Enforcement
   evidence and merge councils can cite the bench digest.
3. **Containment improves** — running the job in a bench with only the
   workspace mounted structurally hides the host profile; heartbeats can
   attest bench digests exactly as they attest credential absence today.
4. **Determinism** — digest-pinned benches make runs reproducible against a
   known toolchain.

## Contract fit (the slot already exists)

`contracts/omnigent/omnigent-domain-overlay.schema.yaml` (ratified
`add-omnigent-domain-overlay`) already carries `toolchain_bindings:` as
`payload_ref[]` (id + path). Benches are the concrete payload behind those
refs. What is still missing, in dependency order:

1. **Neutral `bench-manifest` contract** (openxFactory) — `kind:
   xfactory_tech_bench`: bench id, image ref + digest, stack, tool inventory
   (name/version), capabilities, credential statement (benches are
   tools-only, never credentialed), refresh policy. Domain-neutral: Medx
   declares clinical-document benches, Ledgerx ledger tooling — the mechanism
   is identical, making this a DTN-shaped contract from birth.
2. **codexFactory `omnigent/` overlay consumes it** — `toolchain_bindings`
   entries pointing at bench manifests for the engineering stacks
   (dotNet, python, cpp, flutter, ts/node, …), digest-pinned.
3. **Job→bench selection** (Omnigent-Install harness) — the bench resolves
   from the target repo's declared stack or an explicit field on the
   intent/binding; the manifest rides into the worker context as the agent's
   tool catalog.
4. **Heartbeat bench inventory** (neutral heartbeat contract delta +
   publisher + readiness evaluators) — workers advertise installed bench ids
   + digests; readiness gates dispatch on "required bench present and
   current". Same pattern as profiles/labels; note the 2026-07-23 lesson
   (execution_lane): heartbeat contract deltas must land in the publisher,
   the readiness service field spec/view, and the evaluator together.
5. **Host pre-pull via the worker-host agent + Intune** — bench pull/refresh
   is a reconciled entry in the `worker_host_manifest`, not a hand-run pull.

## The Intune / worker-host-agent coupling

This capture also records the worker-host direction discussed 2026-07-22/23
(motivated by the CPC incident: session-loop publishers dead since 7-19,
unescrowed local service-account passwords, no declarative host state):

- **xFactory Worker Agent**: a signed package deployed by Intune (OpsxFactory
  owns managed platforms — same precedent as the GitHub administration
  plane), running as an auto-start supervisor service. It reconciles a
  declarative `worker_host_manifest`: runner registration, per-worker sealed
  identities (prefer passwordless virtual service accounts; any
  password-bearing account is escrowed — see client-credential-escrow-registry),
  heartbeat publishing from within each worker context, credential-profile
  materialization, **and bench image pre-pull/refresh by digest**.
- Enrollment is a governed handshake: Intune deploys → agent authenticates
  with a device-bound credential → registers with the Hermes runtime
  (worker primitives already live) → human/tenant approval admits the host to
  a pool → config + credential references flow.
- **Linux benches on Windows hosts** need Docker/WSL2 or Podman on the Cloud
  PC — a real new layer; it lands via the agent/Intune, never hand-installed.
- **First bench-enabled host: the Omni-001 Cloud PC** (`CPC-Omni0-P5AJB`,
  provisioned 2026-07-10, idle) — cleanly installed from the agent + benches
  from day one, becoming the migration target off the operator's personal
  CPC (`CPC-brett-TUBV0`, the pilot rider).

## Anti-goals

- No informal `docker pull` of benches onto hosts with workers pointed at
  them by convention — works immediately, unexplainable in a month (the
  exact pattern the 2026-07-22/23 heartbeat recovery dug out of).
- No `:latest`/mutable tags in overlay bindings — digests only.
- No credentials baked into bench images; auth profiles mount at runtime.

## Possible feats

- **`bench-manifest` neutral contract** (openxFactory, ADDED) + examples.
- **Heartbeat bench-inventory delta** (neutral heartbeat contract +
  omnigent-install publisher/service + codexFactory readiness evaluator, one
  coordinated change).
- **codexFactory overlay toolchain_bindings** — first real entries, one per
  engineering bench.
- **Bench build/publish pipeline** (OpsxFactory or codexFactory CI → ACR,
  digest + manifest emission per build).
- **Worker-host agent + Intune packaging** (OpsxFactory realization; agent
  behavior owned by Omnigent-Install) with `worker_host_manifest` including
  bench entries — supersedes the hand-run CPC setup.
- **Omni-001 bench-enabled host install** — first consumer proof; rider
  migration off the personal CPC.

## Open questions

- Bench granularity: one bench per stack vs. composed layers (base bench +
  stack layer) — image size/refresh tradeoff on 500 GB hosts.
- Where bench manifests live: alongside each bench's Dockerfile in the bench
  source repo(s), mirrored into the overlay by pin? Where do bench sources
  live today (operator-local) and which repo owns them going forward?
- Container substrate on Windows 365: Docker Desktop licensing vs Podman;
  WSL2 enablement via Intune policy — OpsxFactory to qualify.
- Does the sealed-account model change inside containers — does the worker
  account run the container runtime, or does the agent own the runtime and
  inject per-job workspaces?
- Heartbeat attestation semantics for benches: advertise all pulled benches
  vs. only benches verified against their pinned digests this cycle.
- Selection authority: may the coding agent choose among multiple eligible
  benches, or does the binding fix exactly one (determinism vs. flexibility)?
