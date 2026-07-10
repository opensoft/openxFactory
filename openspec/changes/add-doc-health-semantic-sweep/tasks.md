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
      doc-analysis-worker profile is added to omnigent-install
- [ ] 4.4 Register the Omnigent cloud workstation in organization runner group
      `xfactory-artifact-workers` with artifact/profile/host/unique labels,
      sealed local service account, Claude subscription login, and Python 3;
      publish a fresh external heartbeat, prove hosted readiness, then set
      `OMNIGENT_WORKER=true`

## 5. Realization and archive

- [ ] 5.1 Obtain a green nightly run whose report contains the semantic
      sweep section (realization evidence for the code surface)
- [ ] 5.2 Archive the change, promote the delta into
      `openspec/specs/doc-health/spec.md`, close the staged topic, and
      re-pin domain stack files if the contract ref moves
