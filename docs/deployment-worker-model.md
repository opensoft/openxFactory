# Deployment and Worker Model

This document describes the intended deployment shape for the AI software development factory.

The core decision is that the Hermes server is the control plane. It may run Hermes, Omnigent/Polly coordination, VPN access, project registries, job queues, worker registries, traceability views, and lightweight status services. It should not become the main machine for concurrent builds, full test suites, browser tests, or heavy repository execution.

Real engineering execution runs on separate worker hosts. For the current plan, those worker hosts are Cloud PCs with 8 vCPU, 32 GB RAM, and 500 GB disks.

## High-Level Layout

```text
Hermes control server
  +-- Hermes
  |     +-- portfolio governance
  |     +-- OpenSpec change management
  |     +-- policy and approval control
  |     +-- project memory
  |     +-- cross-project dashboard
  |
  +-- Omnigent / Polly control
  |     +-- repo-level orchestration
  |     +-- job dispatch
  |     +-- branch/session control
  |     +-- worker coordination
  |
  +-- VPN / private access
  |     +-- private dashboard and admin access
  |
  +-- light control services
        +-- repo/project registry
        +-- worker registry
        +-- job queue
        +-- traceability store
        +-- branch admission records
        +-- status dashboard

Cloud PC worker hosts
  +-- Omnigent host / runner
  +-- repo clones and worktrees
  +-- coder sessions
  +-- tester sessions
  +-- integrator sessions
  +-- local toolchains
  +-- dependency caches
  +-- generated artifacts and reports
```

## Control Plane Boundary

The Hermes server is allowed to run control and orchestration services:

- Hermes dashboard and project control UI
- OpenSpec governance and change state
- Omnigent server and Polly coordination
- VPN or private ingress
- job queue
- worker registry
- repo/project registry
- traceability documents and indexes
- branch admission records
- merge council records
- lightweight status dashboards

The Hermes server should not be used as the main execution host for:

- many concurrent coder sessions
- full repository builds
- full test suites
- browser end-to-end tests
- Docker-heavy integration tests
- database integration suites
- broad static analysis across large repos
- repeated dependency installation
- multi-project branch integration work

The practical rule is:

```text
Hermes server = decisions, memory, policy, approvals, routing, dashboards
Cloud PCs = coding, testing, integration, branch work, repo execution
```

## Cloud PC Worker Hardware

The planned Cloud PC worker profile is:

```yaml
cloud_pc_worker:
  cpu: 8 vCPU
  memory: 32 GB
  disk: 500 GB
```

This size is useful because coder sessions are usually light, while tester and integrator sessions are heavier. The 500 GB disk matters because worker hosts accumulate:

- repo clones
- git worktrees
- dependency caches
- package manager caches
- Docker images and layers
- browser test binaries
- build outputs
- test artifacts
- review packets
- logs

Disk cleanup should be part of worker maintenance, but the larger disk gives enough room for multiple active projects and repeated test/build cycles.

## Worker Roles

Workers should be described by role and capability, not only by machine name.

The initial roles are:

- coder
- tester
- integrator
- reviewer

One Cloud PC may advertise multiple roles, but each role should have its own capacity limits.

### Coder Workers

Coder sessions are lightweight because most reasoning happens in remote LLMs and subagent harnesses. Local work usually consists of:

- reading files
- editing files
- using git
- running small targeted commands
- running focused unit tests
- generating Spec Kit artifacts
- producing implementation diffs

An 8 vCPU / 32 GB Cloud PC can plausibly run 10 to 20 coder sessions when those sessions are mostly using remote model APIs and are not all building or testing at the same time.

Recommended starting capacity:

```yaml
coder_worker_capacity:
  cloud_pc_size: 8_vcpu_32gb_500gb
  recommended_sessions: 10
  optimistic_sessions: 20
  scheduling_note: "Allow 20 only when sessions are mostly LLM-bound and heavy local commands are restricted."
```

Coder sessions should generally be allowed to run:

- git commands
- file edits
- formatters on changed files
- lint on changed files
- targeted unit tests
- lightweight type checks when cheap
- Spec Kit specify, clarify, checklist, plan, tasks, analyze, and implement for small features

Coder sessions should generally avoid:

- full monorepo builds
- full test suites
- Docker Compose stacks
- browser end-to-end suites
- broad dependency audits
- long-running integration tests

When a coder needs heavy validation, Polly should hand the branch to a tester worker.

### Tester Workers

Tester sessions are heavier because they run local execution. They consume CPU, memory, disk IO, and sometimes containers or browsers.

Tester sessions may run:

- full test suites
- full builds
- lint
- typecheck
- integration tests
- database-backed tests
- Docker Compose validation
- browser end-to-end tests
- dependency audits
- migration dry-runs
- changed-area regression tests

An 8 vCPU / 32 GB Cloud PC should normally run only 1 to 2 tester sessions.

Recommended starting capacity:

```yaml
tester_worker_capacity:
  cloud_pc_size: 8_vcpu_32gb_500gb
  recommended_sessions: 1
  optimistic_sessions: 2
  scheduling_note: "Treat tester sessions as scarce. They are the main local resource bottleneck."
```

Tester sessions should prefer clean or disposable workspaces. A tester should check out the branch, run validation, upload reports, and leave the workspace in a known state or discard it.

### Integrator Workers

Integrator sessions sit between coding and final GitHub merge enforcement. They are responsible for cross-feature and cross-branch work after individual feature branches exist.

Integrator sessions may run:

- merge or rebase checks
- conflict detection
- dependency-layer validation
- integration branch creation
- cross-feature regression checks
- contract compatibility checks
- migration ordering checks
- branch readiness checks against latest main

Integrator sessions are heavier than coders but usually lighter than full tester sessions. The recommended starting capacity is 1 to 3 integrator sessions per Cloud PC, depending on how much validation the integrator is allowed to run locally.

Recommended starting capacity:

```yaml
integrator_worker_capacity:
  cloud_pc_size: 8_vcpu_32gb_500gb
  recommended_sessions: 1
  optimistic_sessions: 3
  scheduling_note: "Raise capacity only if integrators are mostly doing git and review work rather than full builds."
```

Integrator sessions should not casually rewrite feature work. They should reconcile dependency layers, detect conflicts, and send focused repair requests back to Polly/coder sessions when feature branches need changes.

### Reviewer Workers

Reviewer sessions may be mostly API/model-bound, similar to coder sessions, but they need consistent review packets and clear scope.

Reviewer sessions may run:

- local branch review
- diff review
- Spec Kit traceability review
- architecture review
- security review
- maintainability review
- test coverage review

Reviewers should receive structured packets from Polly, including:

- epic, phase, and feature IDs
- OpenSpec references
- Spec Kit artifacts
- changed file list
- git diff
- deterministic check output
- known project constraints
- branch admission policy

Reviewer sessions can share Cloud PCs with coders as long as local build/test execution is restricted.

## Worker Registry

Hermes and Polly need a shared view of worker capacity.

A worker should advertise:

- host name
- network address or Omnigent host identity
- hardware profile
- allowed roles
- current load
- supported languages/toolchains
- supported project labels
- available disk
- whether Docker is allowed
- whether browser tests are allowed
- whether secrets are mounted
- maximum concurrent sessions by role

Example:

```yaml
host: cloudpc-eng-01
profile:
  cpu: 8
  memory_gb: 32
  disk_gb: 500
roles:
  coder:
    capacity: 16
  tester:
    capacity: 2
  integrator:
    capacity: 2
  reviewer:
    capacity: 8
capabilities:
  languages:
    - node
    - python
    - dotnet
  docker: true
  browser_tests: true
  databases:
    - postgres
    - sqlite
current_load:
  coder: 7
  tester: 1
  integrator: 0
  reviewer: 2
constraints:
  max_heavy_jobs: 2
  reserve_disk_gb: 80
```

Polly should schedule work against these advertised capabilities instead of assuming every worker can do every job.

## Scheduling Model

The scheduling model should separate LLM-bound work from local execution work.

```text
LLM-bound work
  - decomposition
  - coding
  - local branch review
  - Spec Kit artifact generation
  - explanation and summarization

Local execution work
  - build
  - test
  - typecheck
  - lint at full scale
  - integration tests
  - browser tests
  - Docker validation
```

Many LLM-bound sessions can coexist on one Cloud PC. Fewer local execution jobs can run safely at the same time.

The scheduler should reserve capacity for heavy jobs. For example, a Cloud PC with 16 coder slots should not start 16 sessions that are all allowed to run builds. The worker policy should distinguish between:

```yaml
session_type:
  coder_light:
    consumes:
      coder: 1
      heavy_job: 0

  tester_heavy:
    consumes:
      tester: 1
      heavy_job: 1

  integrator_medium:
    consumes:
      integrator: 1
      heavy_job: 0.5
```

## Workspace Isolation

Do not let 10 to 20 coder sessions share one mutable checkout.

Each feature branch should use an isolated worktree or clone:

```text
D:\factory\
  repos\
    <project>\
      main\
  worktrees\
    <project>\
      <feature-id>\
  artifacts\
    <job-id>\
  caches\
    npm\
    pip\
    nuget\
    docker\
```

Linux workers can use the same structure under `/factory`:

```text
/factory/
  repos/<project>/main/
  worktrees/<project>/<feature-id>/
  artifacts/<job-id>/
  caches/
```

The important rule is that each agent session writes to its own branch workspace. Shared caches are allowed, but shared working directories are not.

## Tester Workspace Rules

Tester sessions should prefer repeatable workspaces:

```text
1. Receive branch and test plan from Polly.
2. Create or reset a clean workspace.
3. Check out the branch.
4. Install or restore dependencies from cache.
5. Run assigned checks.
6. Upload logs, reports, and status.
7. Clean or mark workspace disposable.
```

This keeps test results trustworthy and avoids hidden state from prior agent sessions.

## Integrator Workspace Rules

Integrator sessions should operate on integration workspaces, not coder workspaces.

An integrator may:

- pull latest main
- fetch candidate branches
- test merge order
- detect conflicts
- validate shared contracts
- create an integration branch when explicitly requested

An integrator should not silently change the scope of a feature branch. If the integration pass finds a problem, Polly should send a focused repair job to the responsible feature branch.

## Branch Admission Flow

The worker model supports branch admission before PR creation.

```text
Sonnet coder session
  -> implements feature branch

Polly
  -> runs deterministic checks on worker
  -> creates local branch review packet
  -> runs local multi-model review
  -> sends blockers back to coder if needed
  -> produces branch admission packet

Hermes
  -> evaluates admission packet
  -> approves or blocks PR creation

Polly
  -> opens PR only after Hermes approval

GitHub
  -> runs PR checks, reviews, branch protection, and merge queue
```

This prevents low-quality branches from immediately triggering expensive GitHub PR systems.

## Capacity Guidance

Initial per-Cloud-PC guidance:

```yaml
cloud_pc_capacity_guidance:
  hardware:
    cpu: 8
    memory_gb: 32
    disk_gb: 500

  coder:
    normal: 10
    upper_bound: 20
    notes:
      - "Good when work is mostly remote-model-bound."
      - "Restrict full builds and full test suites."

  tester:
    normal: 1
    upper_bound: 2
    notes:
      - "Treat as scarce because tests/builds consume local resources."
      - "Use clean or disposable workspaces."

  integrator:
    normal: 1
    upper_bound: 3
    notes:
      - "Depends on whether integration jobs run full validation."
      - "Good for merge, conflict, and dependency-layer checks."

  reviewer:
    normal: 4
    upper_bound: 10
    notes:
      - "Works well when review is model/API-bound."
      - "Give reviewers structured packets and avoid heavy execution."
```

These are starting numbers, not permanent guarantees. Actual capacity should be adjusted from observed CPU, memory, disk IO, test duration, model latency, and queue wait time.

## Scaling Pattern

The factory should scale by adding worker hosts, not by making the Hermes server larger first.

Recommended growth path:

```text
Stage 1
  One small Hermes control server
  One Cloud PC worker

Stage 2
  One small Hermes control server
  One coder-heavy Cloud PC
  One tester-heavy Cloud PC

Stage 3
  One small Hermes control server
  Multiple labeled worker pools:
    - coder-light
    - tester-heavy
    - integrator-medium
    - reviewer-api

Stage 4
  Same control-plane pattern
  Add elastic or ephemeral workers for bursts
```

The control plane can remain small as long as it only coordinates. The expensive part of the system is branch execution, and that belongs on workers.

## Security Model

Hermes dashboard and admin tools should not be exposed publicly.

Access should be through VPN or equivalent private access.

Worker security should include:

- per-worker credentials
- per-project credentials where possible
- least-privilege GitHub tokens
- no broad shared secrets across all workers
- separate secrets for coders and testers when possible
- clear policy for which workers may run Docker
- clear policy for which workers may access production-like data
- artifact upload without exposing local worker filesystems broadly

Workers should be considered semi-trusted execution environments. Coding agents can run commands and modify files, so secrets and network access must be intentionally scoped.

## Operational Rules

1. Keep Hermes and Omnigent control services private.
2. Register Cloud PCs as Omnigent worker hosts.
3. Label workers by role and capability.
4. Keep coder work in isolated worktrees.
5. Reserve tester capacity for heavy local validation.
6. Use integrators for cross-feature dependency and merge-layer work.
7. Upload reports and artifacts back to the control plane.
8. Require Hermes approval before PR creation.
9. Let GitHub enforce final PR and merge rules.
10. Scale by adding worker Cloud PCs before enlarging the Hermes control server.
