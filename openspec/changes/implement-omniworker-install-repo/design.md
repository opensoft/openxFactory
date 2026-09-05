# Design: implement-omniworker-install-repo

Status: draft

Every assignment below is tagged **RULED** (Brett Heap, 2026-09-05),
**JUDGED** (this packet, from the file's own content — contestable), or
**OPEN** (§ D6 — put to Brett, not decided here). Measurements are against
`opensoft/Omnigent-Install` at `9e4fe4e9`, `opensoft/xFactory` at `56cda29c`,
and `opensoft/openxFactory` at `ceb6dc9e`, all read 2026-09-05.

## D1 — The boundary, in one sentence each

**Omnigent orchestrates. omniWorker hosts.**

`Omnigent-Install` owns the thing that DECIDES: the control-plane services,
the container and compose topology it schedules, the agent and pilot flows,
the Hermes and memory services, the intent inbox, and the
`omnigent-install-manifest` realization.

`OmniWorker-Install` owns the thing that EXECUTES: the Worker Host App that
converges a Cloud PC into a worker host, the worker pack that describes what
a host runs, the profiles and prompt sets a host materializes, the host
manifests, the heartbeat the host publishes, and the runbooks an operator
follows to stand one up.

The test for a disputed file: *does it describe a decision the control plane
makes, or a state a machine is converged into?* Where that test does not
answer cleanly, the file is in § D6 and not in § D2.

## D2 — The split, directory by directory

### D2.1 — Moves to `OmniWorker-Install`

| Path | Contents (measured) | Basis |
|---|---|---|
| `hostapp/` | `XFactoryWorkerHost/` (`.psm1` + `.psd1`), `deploy/` (`Install.ps1`, `Uninstall.ps1`, `Invoke-Supervisor.ps1`, `XFDeployCommon.ps1`, `Detect-AppVersion.ps1`, `Detect-ManifestDigest.ps1`, `README.md`), `tests/` (`Invoke-HostAppTests.ps1`, `Invoke-DeployTests.ps1`), `render_manifest.py`, `README.md` | **RULED** — the worker host app + deploy + tests |
| `workers/` | `cloudpc-worker-pack.yaml`, `profiles/` (14), `prompts/` (4 manager/review prompt sets), `schemas/artifact-worker-heartbeat.schema.json`, `fixtures/artifact-worker-heartbeat/` (9 fixtures + README), `scaleout/` (`worker-lanes.yaml`, `job-assignment-policy.example.yaml`), `external-pool-references.yaml`, `host-readiness.example.json`, `live-factory-worker-lane.yaml`, `live-factory-worker-preflight.example.yaml` | **RULED** — cloudpc worker pack, profiles, schemas incl. the heartbeat schema |
| `clients/opensoft/worker-hosts/` | `cpc-omni01.worker-host-manifest.yaml` | **RULED** |
| `scripts/publish_artifact_worker_heartbeat.py` | the reference heartbeat publisher CloudPC-Install's selftest loads by path | **RULED** |
| `docs/runbooks/cloudpc-named-worker-licensing.md` | Omni identity + Windows 365 licensing, both host classes | **RULED** |
| `docs/runbooks/cloudpc-worker-pack.md` | the production-shaped worker install, phases 1–4 | **RULED** |
| `docs/runbooks/doc-health-cloudpc-pilot.md` | the CloudPC pilot runbook (carries a live correction banner; it travels with the banner) | **RULED** |
| `docs/worker-deployment-phases.md` | Cloud PC as durable host, containers as runtime boundary, Omni identity mapping | **RULED** |
| `openspec/changes/add-worker-enrollment-broker-integration/` | the ACTIVE host-app change (PR #40): `worker_enrollment` reconcile step, broker client, lease store, `schemas/worker-host-manifest.schema.yaml` edits, `hostapp/tests/` fake-broker suites | **RULED** — with the *sequencing* left OPEN, § D5 |
| `docs/credential-auth-profiles.md` | prepared model-CLI homes (`.claude/`, `.codex/`, `.gitconfig`) mounted into a worker lane's container | **JUDGED** host-side: it describes a state a machine is converged into. Brett's list said "IF they are host-side (judge from content)" |
| `docs/runbooks/llm-credential-onboarding.md`, `llm-credential-portability-research.md`, `plan-a-llm-credential-install.md` | Claude/Codex CLI credential onboarding for *CloudPC worker personas*; the working install plan targets `omni001 / omni002 / omni003 → CloudPC Persona Agent → worker container writable HOME` | **JUDGED** host-side. Caveat: `plan-a-llm-credential-install.md` opens on `master provider Key Vault → Hermes credential ACL database`, which is control-plane. The runbook moves; the Hermes-side half stays a pointer, and if that split is wrong it is cheaper to correct in the copy than to leave the operator procedure in the wrong repository |
| `docs/worker-hosts.md` | "Worker hosts are Cloud PCs registered with Omnigent" — host registration, one container per Cloud PC | **JUDGED** host-side, and it is the doc `worker-deployment-phases.md` (RULED to move) links to |
| `schemas/worker-host-manifest.schema.yaml` | the host manifest schema | **JUDGED**. Measured consumers: `hostapp/{XFactoryWorkerHost.psm1,render_manifest.py}`, `hostapp/deploy/{Install.ps1,XFDeployCommon.ps1,Detect-ManifestDigest.ps1}`, `hostapp/tests/Invoke-DeployTests.ps1`, `scripts/validate_worker_host_manifest.py`, `tests/{test_hostapp_deploy,test_hostapp_module,test_worker_host_manifest}.py`, `clients/opensoft/worker-hosts/cpc-omni01.*`. **Every one of them moves.** One consumer stays: `clients/opensoft/k8s/azure/.../helmrelease.yaml`, which is a reference, not a validation |
| `evidence/worker-host-manifest/` | `cpc-omni01.worker-host-manifest.json`, `python-bench.example.json` | **JUDGED** — evidence for the manifest that moves |
| `rendered/effective-profiles/` | `coding-patch-worker.yaml` + its `.provenance.yaml` | **JUDGED** — generated output of `render_effective_profiles.py` over `workers/profiles/` |
| host-side `scripts/` | `register-worker.sh`, `resolve-worker-pool.sh`, `worker_pool_binding.py`, `render_effective_profiles.py`, `validate_worker_host_manifest.py`, `validate_worker_pools.py`, `validate_worker_preflight.py`, `validate_worker_lane_config.py`, `smoke-worker-lane-config.sh`, `validate_artifact_lane_contract.py`, `validate_cloudpc_deployment_plan.py`, `smoke-cloudpc-deployment-plan.sh`, `validate-worker-auth.sh`, `ops-worker-rebuild-check.sh`, `prewarm-omnigent-runtime.sh`, `claude-subscription-auth.sh`, `create-dev-auth-profile.sh`, `ops-rotate-auth-profile.sh`, `plan-a-login-tui.py`, `smoke-plan-a-credential-install.sh`, `validate_plan_a_credential_install.py` | **JUDGED** — "other worker-host scripts" per Brett's list, enumerated by measurement rather than by pattern. Each one either converges a host, validates a host artifact, or prepares a host credential home |
| host-side `tests/` | `test_hostapp_deploy.py`, `test_hostapp_module.py`, `test_worker_host_manifest.py`, `test_publish_artifact_worker_heartbeat.py`, `test_rider_heartbeat_contract.py`, `test_worker_auth_bootstrap.py`, `test_artifact_lane_contract.py`, `pwsh_host.py` (the PowerShell harness the first two need) | **JUDGED** — a test travels with the thing it tests; "Existing proof harness depends on current files" is a stop condition in the ratified copy-first requirement, so these move WITH their subjects and in the same PR |

### D2.2 — Stays in `Omnigent-Install`

| Path | Basis |
|---|---|
| `compose/`, `containers/`, `k8s/`, `deploy/` | **RULED** |
| `hermes_service/`, `memory_service/` | **RULED** |
| `agents/`, `pilot-flows/`, `live-pilot/`, `speckit/` | **RULED** |
| the Omnigent server / Polly install docs — `docs/omnigent-implementation-plan.md`, `deployment-topology.md`, `hermes-*.md` (6), `memory-*.md` (2), `clarification-*.md` (2), `context-compression-pilot.md`, `phase1-*.md`, `project-*.md`, `qa-environment-naming.md` | **RULED** |
| the `omnigent-install-manifest` realization — `config/omnigent-install-manifest.yaml`, `schemas/omnigent-install-manifest.schema.yaml`, `scripts/validate_omnigent_manifest.py` | **RULED** |
| `intent_inbox/`, `dox_auth/`, `dispatch_token_minter/`, `manager_review/`, `manager_token_supplier/` | **JUDGED** — control-plane services. `config/intent-inbox-allowlist.json` stays with them, which is why `intent-apply.yml` does not move (§ D4) |
| `config/`, `contracts/openxfactory-contract-ref.yaml`, `policies/`, `ops/`, `examples/` | **JUDGED** — orchestrator configuration, the contract pin, and the pilot examples |
| `schemas/` minus `worker-host-manifest.schema.yaml` — the clarification family (3), the Hermes job family (3), `hermes-operational-postgres.sql`, `omnigent-domain-overlay.schema.yaml`, `omnigent-install-manifest.schema.yaml`, `bench-manifest.schema.yaml` | **JUDGED**, and the two `omnigent-*` ones are **RULED** untouched by the ruling's own words |
| `clients/opensoft/` minus `worker-hosts/` — `scripts/`, `k8s/`, `hermes/`, `docs/`, `iac/` | **JUDGED** — tenant deployment and QA estate |
| the remaining `docs/runbooks/` — `hermes-*.md` (3), `phase1`–`phase9` (9), `merge-master-implementation-plan.md`, `live-*.md` (3), `project-alfa-structured-clarify-test.md`, `pilot-flow-checklist.md`, `reusable-pilot-flow.md` | **JUDGED** |
| the remaining `scripts/` (~80) and `tests/` (~30) — the `smoke-*`/`validate_*` pilot, Hermes, merge-council, PR-admission, dartwing, openchart/openemr, dox-auth, intent-inbox and minter families | **JUDGED** |
| the remaining `openspec/changes/` — `add-dox-gitops-reconciliation`, `add-manager-lane-claim-loop`, `add-manager-review-agent`, `add-manager-seat-persistence`, `add-qa-subscription-environment`, `admit-keycloak-db-to-core-failover`, `generalize-lane-claim-loop`, `migrate-dartwing-to-platform-qa`, `qa-workcore-request-rightsizing`, and the whole `archive/` | **JUDGED** — with `add-worker-acr-push` OPEN (§ D6 OQ-6) |

## D3 — Pin choreography

**Copy-first, and retirement LAST.** The ratified "Copy-first migration"
requirement already binds this: *"the policy MUST be copied or summarized
into `openxFactory` before the install repo copy is deleted or marked
legacy"*, and *"a proposed move [that] could break an existing proof harness
or smoke test ... MUST be deferred until a replacement location and validation
path exist."* The sequence below is that rule applied to a repository split.

```text
1  CREATE      opensoft/OmniWorker-Install     (Brett's act; private; main; ruleset; App install)
2  COPY        the D2.1 tree into it, WITH its tests, and prove them green there
3  PIN         xFactory .gitmodules gains installs/omniworker-install  (a SIBLING entry;
               installs/omnigent-install is NOT removed and NOT renamed at this step)
4  RE-POINT    the four xFactory workflow comments naming
               installs/omnigent-install/workers/profiles/*.yaml
5  ADMIT       OpsxFactory models/code-surface-repositories.yaml — one entry,
               id: OmniWorker-Install, source: aggregation_submodule
               (the validator re-derives it against the aggregation .gitmodules,
               so step 3 must land first or the entry is a finding)
6  RE-POINT    openxFactory's own references to Omnigent-Install worker paths
7  RE-POINT    CloudPC-Install packs/service-rider/selftest/check_heartbeat_contract.py
               OMNIGENT_ROOT -> OMNIWORKER_ROOT (with a deprecating fallback), and the
               sibling-directory candidates OmniWorker-Install / omniworker-install
8  PROJECT     a NotebookLM ideation book for the new repository
               (xf-ideation-omniworker-install), per docs/lifecycle-notebook-projection.md
9  RETIRE      delete the D2.1 paths from Omnigent-Install — ONLY after 3-7 are landed
               and green, and only in its own reviewed PR
```

**Each numbered step is its own PR** (tasks §4/§5/§6). Steps 3–7 have no
required order among themselves EXCEPT that 5 depends on 3, because
OpsxFactory's `code_surface_repository_registry` validator arm re-derives an
`aggregation_submodule` entry against the aggregation's `.gitmodules` and a
`.gitmodules` that does not yet carry the path makes the entry a finding
rather than a claim.

**Step 9 is the only destructive step and it is last**, which is what makes
every step before it revertible by a single `git revert`.

Two things this sequence deliberately does NOT do:

- **It does not rename `installs/omnigent-install`.** The orchestrator keeps
  its submodule path because it keeps its name. Step 3 ADDS a sibling.
- **It does not admit the new repository to the aggregation as a governed
  act.** Step 3's gitlink is the mechanical pin; the *record* of path,
  remote, visibility, exact validated commit, checkout, compatibility, update
  and rollback is a separate reviewed change, which the ADDED requirement's
  own scenario demands and which this change MUST NOT be accepted as.

## D4 — The consumer measurement, including two that do NOT move

Measured on `opensoft/xFactory` at `56cda29c` with
`grep -rn "omnigent\|Omnigent" .github/workflows/`:

| Consumer | Reference | Moves? |
|---|---|---|
| `.gitmodules` | `installs/omnigent-install` → `git@github.com:opensoft/Omnigent-Install.git` | **Gains a sibling** at step 3; the entry itself stays |
| `doc-health-cataloger-worker.yml` | comment: `installs/omnigent-install/workers/profiles/document-cataloger.yaml` | **Yes** — the profile moves |
| `doc-health-readiness-worker.yml` | comment: `installs/omnigent-install/workers/profiles/…` | **Yes** |
| `doc-health-derive-possibles-worker.yml` | comment: `installs/omnigent-install/workers/profiles/derive-possibles.yaml` | **Yes** |
| `ideation-organizer-worker.yml` | comment: `installs/omnigent-install/workers/profiles/ideation-organizer.yaml` | **Yes** |
| `intent-apply.yml` | `repositories: openxFactory,Omnigent-Install` and a `gh api` read of `repos/<owner>/Omnigent-Install/contents/config/intent-inbox-allowlist.json` | **NO.** `config/` is orchestrator material and stays. The App scope and the allowlist read are both correct after the split |
| `dashboard-image-worker.yml` | prose: the image pin PR is delivered *to* Omnigent-Install; and `self-hosted/omnigent/artifact-only` runner labels | **NO** for the pin; the LABEL is OQ-5 |
| `council-deliberation-worker.yml` | prose: "the EIGHTH Omnigent worker lane" | **NO** — prose about the orchestrator |

**No xFactory workflow checks out the submodule.** `grep -rn "submodules:"
.github/workflows/*.yml` returns nothing. All four moving references are
documentary comments that tell a reader which profile declares the label the
lane dispatches to — which is exactly why they must be re-pointed: a comment
that names a path nothing contains is worse than no comment.

Outside the aggregation:

| Consumer | Reference | Moves? |
|---|---|---|
| OpsxFactory `models/code-surface-repositories.yaml` | `- id: Omnigent-Install / source: aggregation_submodule` | **Gains one entry**; the existing one stays |
| CloudPC-Install `packs/service-rider/selftest/check_heartbeat_contract.py` | `OMNIGENT_ROOT`, sibling candidates `Omnigent-Install` / `omnigent-install`, then `workers/schemas/artifact-worker-heartbeat.schema.json` and `scripts/publish_artifact_worker_heartbeat.py` | **Yes** — both target files move. The selftest SKIPS rather than fails when the sibling is absent, so it will go quietly green-with-skips at the moment of the move; the re-point must therefore be verified by an explicit non-skip run, not by a green summary |
| openxFactory `contracts/manifest.yaml` (`repo: opensoft/Omnigent-Install`, `source_path: Omnigent-Install/schemas/…` ×7, `Omnigent-Install/policies/…` ×2) | the adapter-owner and source-path declarations for the clarification and Hermes-job families | **NO** — those schemas stay with the orchestrator |
| openxFactory `openspec/specs/{shared-contract-ownership,canonical-contract-migration,repo-boundary-governance,omnigent-install-manifest}/spec.md` | canonical text naming `Omnigent-Install` | **NO text change by this packet.** The ADDED requirement names the new repository; whether the older enumerations are refreshed is a separate act (§ D6 OQ-9) |
| NotebookLM `xf-ideation-omnigent-install` | one ideation book per governed repo | **Gains a sibling book** at step 8 |

## D5 — The in-flight change, stated as a rule and NOT decided

`Omnigent-Install`'s `add-worker-enrollment-broker-integration` is ACTIVE and
its PR #40 is open. Its declared `code_surface` is
`hostapp/XFactoryWorkerHost/XFactoryWorkerHost.psm1`, `hostapp/deploy/`,
`schemas/worker-host-manifest.schema.yaml`, `hostapp/tests/`,
`hostapp/README.md` — **every one of which is D2.1 material.** It cannot be
ignored and it must not be silently rebased into a repository its proposal
does not name.

**The two lawful sequences, with their costs:**

**(a) LAND FIRST, THEN MOVE.** #40 merges into `Omnigent-Install`; the split
copies the post-merge tree. *Cost:* the split waits on a change whose
`target_release` is explicitly gated on acceptance evidence from a volunteer
end-to-end run against a DEPLOYED broker — which does not exist yet — so
"lands" here means the code merges while the change stays active and
unarchived. *Benefit:* one tree, one history, no cross-repository rebase, and
the change directory moves in step 2 like any other file.

**(b) MOVE WITH ITS PR.** The change directory and the open PR both re-target
`OmniWorker-Install`. *Cost:* a PR cannot be transferred between repositories
— it is re-opened, losing its review thread and its bot rounds — and the
proposal's `code_surface: omnigent-install` line becomes false the moment the
tree moves, so the packet needs an amendment naming the new repository.
*Benefit:* the change lands in the repository that will still own the code
when it is archived, and no reviewer ever reads a merged diff against a path
that no longer exists.

**This packet does not choose.** The rule it does assert, and the ADDED
requirement encodes, is the weaker and safer one: **an active change whose
declared `code_surface` is entirely D2.1 material MUST be re-homed by an
explicit act — either sequence (a) or sequence (b) named in the migration
change — and MUST NOT be left to arrive in the new repository as an untracked
side effect of a file copy.** Whichever Brett rules, the packet's amendment or
the re-target is a task, not a discovery.

## D6 — Open questions

**OQ-1 — `docs/runbooks/codexfactory-execution-lane-enablement.md`.** It says
of itself: *"the worker-side procedure required by openxFactory repo-boundary
governance (worker procedure lives in Omnigent-Install; lane policy lives in
codexFactory)"*. Under the split, "worker procedure" is `OmniWorker-Install`
— but the runbook's topology is three GitHub workflows dispatching a rider,
which is lane plumbing. Host runbook, or orchestrator runbook?

**OQ-2 — `workers/scaleout/` vs `docs/runbooks/phase8-scaleout.md` and
`compose/phase8-worker-stack/`.** `workers/scaleout/worker-lanes.yaml` and
`job-assignment-policy.example.yaml` move with `workers/` (RULED). The phase-8
runbook and the compose stack they describe stay with the orchestrator
(RULED). That splits one operator procedure across two repositories. Accept
the seam, or move the phase-8 runbook with the lanes?

**OQ-3 — `compose/phase8-worker-stack/` and `containers/omnigent-worker/`
after the split.** Brett RULED `compose/` and `containers/` stay. But
CloudPC-Install's `docs/worker-host-pack.md` converges *"a dedicated-Omni
worker host's omnigent-install checkout"* and brings up exactly three compose
services from `compose/phase8-worker-stack/`, and `docs/host-token-broker.md`
locates the vault token at `<omnigent-install checkout>/.local/vault-token`.
**After the split, a worker HOST still checks out the ORCHESTRATOR
repository.** That is a coherent answer — the host runs the orchestrator's
container stack — but it should be a ruled answer, because it means
`OmniWorker-Install` is not sufficient to stand up a host on its own.

**OQ-4 — the root `schemas/` directory.** § D2.1 moves exactly ONE file out of
it (`worker-host-manifest.schema.yaml`) on measured consumers. Is a single
file worth a `schemas/` directory in the new repository, or should it live at
`workers/schemas/` beside the heartbeat schema that is already there?

**OQ-5 — the GitHub runner label `omnigent`.** Every runner registers
`self-hosted, omnigent, cloudpc, omni001` (and the rider variant
`self-hosted, omnigent, artifact-only, doc-analysis, rider, host-<id>`), and
at least seven xFactory lanes select on it. Under "Omnigent orchestrates;
omniWorker hosts" the label means the machine, and the machine is now
`omniWorker` — but it is a live machine key whose change is a coordinated
runner re-registration plus a workflow sweep, with a window in which no lane
can dispatch. **Change it, keep it, or add `omniworker` as a second label and
retire `omnigent` later?** This packet recommends the third, and does not
assume it.

**OQ-6 — `openspec/changes/add-worker-acr-push/`.** It carries a spec delta
for a capability named `worker-host-registry-credentials` and edits
`schemas/worker-host-manifest.schema.yaml` — host material — but ACR push is
an orchestrator image concern. Which repository owns it?

**OQ-7 — `add-worker-enrollment-broker-integration` sequencing.** § D5,
sequence (a) or (b).

**OQ-8 — the archived `openspec/changes/archive/` history.** The moved active
change takes its own directory. Do the ARCHIVED changes that created the
moving code travel too (so the new repository's history explains its tree), or
does the archive stay whole in `Omnigent-Install` (so no archive is ever split)?
This packet leans to leaving `archive/` whole and having the new repository's
first change cite the old archive by URL.

**OQ-9 — the older openxFactory enumerations.** `shared-contract-ownership`
and `canonical-contract-migration` name `Hermes-Install` and `Omnigent-Install`
by hand, and `repo-boundary-governance`'s own "Install repository scope"
enumerates four install repositories. All three become incomplete when a fifth
exists. Refresh them in a follow-on (this packet's recommendation, on the
`implement-keycloak-install-repo` precedent that left the enumeration alone),
or widen them here?

**OQ-10 — visibility.** `Keycloak-Install` and `OpenXPKI-Install` were created
PRIVATE. `OmniWorker-Install` is assumed private to match. Confirm — the
sibling `openDox` ruling went PUBLIC, so private is no longer automatic in
this estate.

## D7 — What this packet refuses to do

- **It does not create the repository.** That is Brett's act.
- **It does not touch `Omnigent-Install`.** Not one file, not the README, not
  the boundary link. Its half of the split is a task in §6, performed by a PR
  authored against that repository after every consumer is re-pinned.
- **It does not edit OpsxFactory.** The fleet re-attestation needs the NEW
  Entra device id, which does not exist until omni001 is reprovisioned, and
  OpsxFactory's own rule says a bound value moves by a new change and never
  by an in-place edit.
- **It does not rename anything in `contracts/omnigent/`.** The ruling
  excludes it in terms.
- **It does not decide any of OQ-1 through OQ-10.**
