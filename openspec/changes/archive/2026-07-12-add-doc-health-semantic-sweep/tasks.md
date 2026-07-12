# Tasks: Add Doc-Health Semantic Sweep

## 1. Contract (openxFactory)

- [x] 1.1 Validate the change strictly (`openspec validate
      add-doc-health-semantic-sweep --strict` and `--all --strict`) and list
      it in the README "OpenSpec Records" block
- [x] 1.2 Move the staged topic into
      `supporting-docs/agentic-pass.md` with proposal provenance

## 2. Inventory emission (codexFactory)

- [x] 2.1 Extend the deterministic checker to emit its doc inventory (repo,
      path, status, content hash) as a machine-readable artifact per run
- [x] 2.2 Add tests: inventory content matches the corpus walked, hash diff
      against a previous inventory yields the changed-docs set

## 3. Sweep implementation (codexFactory)

- [x] 3.1 Add the versioned prompt contract under `scripts/doc_health/`
      (instructions, finding schema with confidence note, the two semantic
      families)
- [x] 3.2 Implement scope resolution: read `doc_health.sweep_scope` from
      the customer/client/domain Hermes overlays across pinned repos, take
      the deepest declaration, default `incremental`; tests for default,
      deepest-wins, and no-lowering cases
- [x] 3.3 Implement the sweep orchestration: consume the inventory, apply
      the resolved scope, invoke the credential-less analysis worker with
      pinned model id and a neutral job envelope, parse findings, assign
      stable ids (path + passage hash)
- [x] 3.4 Enforce the finding contract in code: always `contested`, severity
      capped at `warning`, required fields present, disposer assigned by
      content ownership (owning factory vs neutral ratify gate); drop and
      log anything malformed
- [x] 3.5 Merge sweep findings into the dated report: semantic family
      sections, ranked-plan items naming their disposer, effective scope +
      declaring layer + model id + prompt version + envelope reference,
      skipped marker on failure
- [x] 3.6 Tests: finding contract enforcement, disposer assignment, dedupe
      against previous report, skipped-sweep report path

## 4. Runner integration (xFactory aggregation repo)

- [x] 4.1 Add the sweep step to the nightly workflow after the deterministic
      pass: non-fatal, orchestration under the existing app-token identity,
      analysis worker with a local read-only checkout and the model API key
      as its only secret, scope resolved from Hermes overlays (no workflow
      knob)
- [x] 4.2 Verify a nightly run with the sweep skipped-on-failure path leaves
      deterministic results intact
- [x] 4.3 Restructure the nightly into the dispatch pipeline: hosted prepare
      builds the self-contained bundle and performs readiness; an independent
      artifact-only child performs analysis under subscription auth; hosted
      finalize polls for a bounded interval and never depends on a self-hosted
      job; inline sweep remains the disabled-dispatch fallback; the
      doc-analysis-worker profile is added to omnigent-install. Remediation
      review completed 2026-07-09: readiness state is authenticated and
      isolated, heartbeats are complete/monotonic, inputs are shell-safe,
      runner labels are unique, deterministic inventory precedes dispatch,
      finalization is failure-isolated, and queue/run budgets align.
- [x] 4.4 Add a manual hosted readiness-only mode that queries the real runner
      group and authenticated Hermes endpoint through the production
      fail-closed evaluator while forcing analysis dispatch and inline fallback
      off; test that it can report ready with `OMNIGENT_WORKER=false` and cannot
      create an analysis child
- [x] 4.5 Follow the omnigent-install
      `docs/runbooks/doc-health-cloudpc-pilot.md` gates: deploy the readiness
      boundary; register the Omnigent cloud workstation in organization runner group
      `xfactory-artifact-workers` with artifact/profile/host/unique labels,
      sealed local service account, Claude subscription login, and Python 3;
      publish a fresh external heartbeat, prove hosted readiness while dispatch
      remains disabled, then set `OMNIGENT_WORKER=true` only for the bounded
      manual test unless recurring heartbeat publication is proven.
      Completed via the CloudPC worker pilot: runner
      `xfactory-artifact-cpc-brett01` serves the `host-rider-cpc-brett01`
      dispatch label in `xfactory-artifact-workers` and executes nightly
      analysis children (runs 29137978776, 29178226880 green).

## 5. Realization and archive

- [x] 5.1 Obtain a green nightly run whose report contains the semantic
      sweep section (realization evidence for the code surface):
      nightly run 29178217833 (2026-07-12, success) produced
      `health/reports/2026-07-12.md` with the Semantic Sweep section
      (claude-sonnet-5, prompt contract v2, envelope SEMSWEEP-21cd3ce31acd)
      and findings in both semantic families; analysis child 29178226880
      ran green on the self-hosted worker
- [x] 5.2 Archive the change, promote the delta into
      `openspec/specs/doc-health/spec.md`, close the staged topic, and
      re-pin domain stack files if the contract ref moves (archived
      2026-07-12; support manifest checksum for omnigent-worker-dispatch.md
      refreshed to its committed a8da029 content as part of this archive —
      the cited resolution for the 2026-07-12 report's contested finding)
