# Omnigent Worker Dispatch for the Semantic Sweep

Status: draft
Proposed by: add-doc-health-semantic-sweep
Kind: architecture
Repository context: openxFactory

Ratify-gate discussion record (2026-07-09): how the semantic sweep's
analysis executes on the Omnigent worker host, and how the credential
story landed. Normative claims live in this change's design.md and spec
delta; this document is provenance for the reasoning.

## The two parts of the sweep

- **Orchestration** — inventory consumption, Hermes-layer scope
  resolution, worker invocation, findings-contract enforcement, report
  merge and commit. Deterministic runner code in the reusable workflow,
  executing under the factory identity (short-lived installation token
  minted from the openxFactory GitHub App). This is xFactory-layer
  plumbing, not Omnigent work.
- **Analysis** — the model-driven judgment step. The only
  non-deterministic part, and the only part that runs as a bounded
  Omnigent worker (omnigent-install profile `doc-analysis-worker`).

## Hosting decision trail

1. Original design: analysis as a headless `claude -p` subprocess inside
   the nightly CI job, with AgentTower hosting deferred.
2. Ratifier direction: run it in Omnigent now — a worker Omnigent stack
   on a cloud workstation — and adopt the AgentTower runtime later.
3. Landed architecture: three-job dispatch pipeline in the nightly.
   - `prepare` (hosted runner): builds a self-contained corpus bundle —
     prompt, scope-selected docs, promoted specs for contradiction
     grounding, `meta.json` — uploaded as a build artifact.
   - `analysis` (self-hosted runner, labels `self-hosted, omnigent`, on
     the cloud workstation): downloads only the bundle. No repository
     checkout, no tokens, scrubbed process environment. Uploads one
     findings artifact. Non-fatal; gated on the aggregation repo
     variable `OMNIGENT_WORKER=true` so nothing queues against an
     unregistered runner.
   - `finalize` (hosted runner): deterministic suite, findings merge
     through contract enforcement, report/inventory/envelope commit,
     regression issue.
4. AgentTower later: replaces the workstation hosting only — the bundle
   in / findings out contract, the worker profile, and the spec are
   unchanged by that migration.

## Credential story

- A GitHub App cannot vault third-party secrets; its private key only
  mints GitHub installation tokens. "Serve the model key from the app"
  is not a thing GitHub offers.
- The dispatch path needs no model secret in GitHub at all: the
  workstation's own claude persona login is the credential
  (`auth_mode: subscription` per the omnigent-install cloudpc worker
  pack, which disallows API keys for worker lanes).
- The `ANTHROPIC_API_KEY` Actions secret remains only as the inline
  fallback while no worker host is registered; absent both, the sweep
  records itself skipped and the deterministic run stays green.
- The two identities never cross: the factory identity never reaches the
  worker host; the model credential never appears in jobs that push.

## Workstation registration runbook (task 4.4)

1. Provision the cloud workstation per the omnigent-install cloudpc
   worker pack; install python3.
2. Install and log in the `claude` CLI under the worker persona
   (subscription auth; no API key on the host).
3. Register a GitHub Actions runner agent on `opensoft/xFactory` with
   labels `self-hosted` and `omnigent`.
4. `gh variable set OMNIGENT_WORKER --repo opensoft/xFactory --body true`
5. The next nightly produces the live sweep section — the realization
   evidence this change archives on.
