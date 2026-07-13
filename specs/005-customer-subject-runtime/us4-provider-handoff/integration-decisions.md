# US4 Integration Decisions

Status: record

Coordinator decisions resolving ambiguities the US4 SIC surfaced. Numbering
continues conceptually from the US3 series (D1–D11 in
`us3-swarm-handoff/integration-decisions.md`); these are the US4 series.

- **U1 — Frozen-evidence discipline.** No US4 file is added to, and no edit
  touches, the 78-member PostgreSQL evidence source inventory. Consequences:
  `shared-definitions.schema.yaml` is reused by `$ref` only (its
  `content_resource_type` already enumerates `job`/`job_run`/`job_event` —
  jobs were pre-provisioned); new fixture families use `phase:
  semantic|structural`, never `database`; `loader.py`/`fixtures.py`/
  `semantics/{authority,evidence}.py` are import-only. The PG matrix is NOT
  re-run for US4; the gate instead proves the inventory intersection of the
  US4 diff is empty.
- **U2 — Release inventory schema is self-contained.** It lives at
  `contracts/releases/` (outside the hermes-runtime family root), cannot be a
  catalog member, cannot `$ref` across directories (`..` segments are
  hard-rejected), and is validated by the release verifier + its own tests,
  not the offline registry. Header kind:
  `openxfactory-contract-release-digest-inventory-schema`.
- **U3 — Domain-regression pins.** The realized inventory uses the ratified
  research-Decision-12 table verbatim. Verified 2026-07-13 against the local
  submodule gitdirs: all five commits present, all five `stack.yaml` blob
  digests match, all five pinned commits carry `contract_ref: 3d51c3ed…`.
  Local HEAD drift (codexFactory `1e4179b…`, OpsxFactory `56dd900…`, dirty
  OpsxFactory worktree) is IRRELEVANT — the resolver reads exact
  `commit:path` Git objects only. LegalxFactory exclusion recorded with the
  research-decision reason.
- **U4 — Finding-code namespaces.** `HGR-JOB-*` (jobs semantics),
  `HGR-RELEASE-*` (release verifier), `HGR-REGRESSION-*` (domain
  regression), `HGR-HANDOFF-*` (consumer receipt; wrong-product code is the
  planning-pinned `HGR-HANDOFF-CONSUMER-REPOSITORY`). `HRC-*` stays reserved
  for CLI/harness dependency findings. Rationale: HGR- is the
  governed-runtime slice; the planning docs already seeded
  `HGR-HANDOFF-…`.
- **U5 — Release-verifier exit codes.** Planning gap (no pinned table)
  resolved as 0 = pass, 1 = findings, 2 = dependency/harness — mirroring
  `validate-hermes-runtime-contracts.py::classify_exit_code`. Dependency
  errors carry `exit_code = 2` exception classes like
  `ContentResolutionError`.
- **U6 — Catalog registration is coordinator-only (T077).** Lanes return
  structured registration payloads (SIC §7); the coordinator applies all
  contract-index entries, fixture-index cases, and evidence-register flips
  in ONE pass. Prevents four-way merge conflicts on the catalogs and keeps
  the count-pin updates (`== 79` → new total) atomic with the registrations.
- **U7 — Mode semantics for the wired CLI.** `standard` mode never requires
  domain/consumer mirrors (the pre-US4 gate stays runnable offline);
  the regression inventory gets schema+semantic validation always, but live
  `commit:path` resolution runs only when `--domain-repo/--domain-repo-root`
  is supplied or the mode is `candidate`/`realization` (where absence of the
  resolver input is a dependency error, exit 2). `--handoff-receipt` implies
  consumer resolution; without a resolvable consumer repo it is exit 2.
  On the real repository TODAY, `--require-candidate` correctly FAILS with
  finding `HGR-RELEASE-INVENTORY-MISSING` (exit 1): no
  `contracts/releases/<tag>.digests.yaml` exists until T079 allocates the
  version — that failure is the specified pre-realization behavior, proven
  by a test against the real repo and a passing test against a synthetic
  candidate snapshot.
- **U8 — v1 job surface stays byte-frozen.** The additive bridge is proven by
  Lane J asserting the three `contracts/schemas/hermes-job-*.schema.yaml`
  files and their pinned `examples/**` fixtures validate unchanged
  (NJE-004-S05 / SC-003). v2 schemas are separate new files; no edit, move,
  or deprecation of v1 paths in this feature.
- **U9 — Scenario double-claims.** Where release and handoff tests both
  exercise a SCO-002 scenario, the evidence entry lists BOTH lanes' node IDs
  (parity allows multiple nodes per scenario). Coordinator reconciles final
  bindings; a scenario with zero surviving bindings is a T077 stop-ship.
- **U10 — T078 provider-gate evidence scope.** `provider-verification.yaml`
  records: strict validator (standard mode, and with `--domain-repo-root`
  against offline mirrors built from the local submodule gitdirs), the
  candidate-mode pre-realization expected failure (U7), non-PG pytest, the
  UNCHANGED PG evidence identity (`sha256:b2ef44a9…`, inventory-intersection
  proof), hygiene gates, and exact repo revision — with `schema_version` +
  `kind`, no credentials, no host-absolute paths. Realization-time entries
  (version, tag, remote evidence) are explicitly `pending: T079+`.
