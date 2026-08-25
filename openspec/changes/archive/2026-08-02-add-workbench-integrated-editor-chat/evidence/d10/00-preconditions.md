# D10 Preconditions Record

Status: record
Kind: evidence
Repository context: openxFactory
Captured: 2026-07-31 (prep pass; session-start slots marked SESSION-START)
Summary: Prerequisite record P1-P6 for the D10 combined real-corpus
acceptance pass (`d10-acceptance-runbook.md`, task 1.3).

## P1 — codexFactory main serve baseline

- Serving checkout: `xFactories/codexFactory-worktrees/fix-doxbench-hosted-refresh`
  (the worktree that holds `main`)
- 2026-07-31 prep state: clean (`git status -sb` empty), at `279f36f`,
  behind `origin/main` by 6 — fast-forward REQUIRED at session start,
  BEFORE the serve starts; the checkout must not move afterward.
- SESSION-START 2026-07-31T08:06Z: fast-forwarded to
  `c617c31f3a334b301e06e31a4fe1eb5bea7618a4` (= origin/main), clean
  (`## main...origin/main`, no entries) — `p1-serve-baseline.txt`.
- Served corpus: dedicated worktree `openxFactory-worktrees/d10-corpus`,
  branch `d10/corpus-baseline` at
  `d09d5820de5b63b9528f6baea884a6dccde9b158` (= openxFactory origin/main),
  clean — immovable for the session (`a-65-readonly-before.txt`).
- `py-bench` images present (`py-bench:brett`, `py-bench:latest`): verified 2026-07-31.

## P2 — Local human console

- SESSION-START 2026-07-31T08:11Z: loopback serve at
  `http://127.0.0.1:46129/` (pid 1940758), started with the ordinary
  daily-dogfood invocation
  (`cli.py generate-and-open --repo-root <d10-corpus> --repository openxFactory`).
- Console presence: `/capabilities` reports
  `{"actions": {"notebook": true, "gate": true, "refresh": true,
  "session": true, "edit": true}, "actor": "brettheap",
  "refresh": {"binding": "regenerate", "loopback_only": true}}`
  with a console token present (value not recorded).
- Snapshot: 238 documents, 21 staged topics; VALIDATED against the pinned
  `ideation-dashboard-snapshot` schema (0 errors, jsonschema 4.26.0);
  `generation.source_revision` = `d09d5820…` — exactly the served corpus HEAD.

## P3 — Hosted dashboard + publication lane

- Hosted URL: `https://ideation-dashboard.xforge.us`
- Reachability probe 2026-07-31T08:04Z: unauthenticated GET returned
  `HTTP/2 401` with valid TLS — boundary posture correct, endpoint live.
- Last known live image digest (2026-07-30 forward repair, plan §11.11):
  `acropensoftxfactoryqa.azurecr.io/ideation-dashboard@sha256:b602380e6f07ddc7d4eff7a7e1680fc37082e274f2cd947085898329ecdb02c3`
- SESSION-START 2026-07-31T08:16Z: live deployment AND running pod both at
  `sha256:b602380e6f07ddc7d4eff7a7e1680fc37082e274f2cd947085898329ecdb02c3`
  (pod `ideation-dashboard-54b78cbbc7-4f6cc`, 1/1, 0 restarts) — identical
  to the §11.11 digest; recorded in `c-62-image-before.txt`.
- Publication lane: `workflow_dispatch` on the aggregation
  `doc-health-nightly.yml` (same `refetch` binding the green 2026-07-29
  automated pass used).

## P4 — Repository roster

- The 11 registered repositories of the aggregation `project-register.yaml`
  (all served as selector routes in the 2026-07-30 acceptance):
  openxFactory, codexFactory, MedxFactory, AdxFactory, LedgerxFactory,
  OpsxFactory, agenttower, cloudpc-install, hermes-install,
  omnigent-install, xfactory-installer.
- SESSION-START 2026-07-31T08:14Z: published `health/ideation-dashboard/index.json`
  at aggregation origin/main lists exactly 11 entries, all `@ main`
  (openxFactory `bf49c1bc94`, codexFactory `6222ab54fc`, Medx/Adx/Ledgerx/Opsx
  populated, five install repos present).

## P5 — Topics (RULED by Brett 2026-07-31)

- Staged topic for Steps B and D: **`consent-instrument-contract`**
- Ready topic for Step E: **`consent-instrument-contract`** (same topic —
  freed session-free by Step D's merge). Rationale: its exit condition was
  met 2026-07-30 (Medx second instantiation archived); the index marks
  `add-consent-instrument` "unblocked and ready to author", so the Step E
  propose commission is the real authoring kickoff, not ceremony.

## P6 — Evidence directory

- `evidence/d10/` exists beside the runbook (this file inaugurates it) on
  branch `docs/d10-acceptance-evidence` (worktree
  `openxFactory-worktrees/d10-acceptance-evidence`, based on `d09d582`).
