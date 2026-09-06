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
| `workers/` | `cloudpc-worker-pack.yaml`, `profiles/` (14), `prompts/` (4 manager/review prompt sets), `schemas/artifact-worker-heartbeat.schema.json`, `fixtures/artifact-worker-heartbeat/` (8 fixtures + README), `scaleout/` (`worker-lanes.yaml`, `job-assignment-policy.example.yaml`), `external-pool-references.yaml`, `host-readiness.example.json`, `live-factory-worker-lane.yaml`, `live-factory-worker-preflight.example.yaml` | **RULED** — cloudpc worker pack, profiles, schemas incl. the heartbeat schema |
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

**Amended 2026-09-05, at copy time** — three corrections surfaced by copying the
tree, filed here rather than rewriting the tables above:

1. **`schemas/bench-manifest.schema.yaml` and
   `examples/bench-manifests/python-bench.example.yaml` MOVE**, though D2.2
   above lists `bench-manifest.schema.yaml` as staying. Both files MUST move
   because `scripts/validate_worker_host_manifest.py` and
   `tests/test_worker_host_manifest.py` — both D2.1 host material — consume
   them by hard-coded path; leaving them behind would break the copied
   validator and its test the moment it ran anywhere but `Omnigent-Install`.
   Copied in OmniWorker-Install PR #2 (`d617e68e`).
2. **`tests/test_worker_auth_bootstrap.py` STAYS with the orchestrator**,
   though D2.1 above lists it as moving with the eight host-side `tests/`.
   Re-checked against its own content at copy time (the JUDGED-tree
   discipline D2 already calls for): its subject is
   `containers/omnigent-worker/scripts/*`, which is orchestrator material,
   not a host test that travels with `hostapp/` or `workers/`. Not copied.
3. **The dartwing CI workflow was copied to `evidence/omnigent-install-ci/`
   only, not installed as a working workflow.** Five of its steps read
   orchestrator-only paths, so installing it verbatim in the new repository
   would either fail on day one or silently no-op; it is carried as
   reference evidence instead, pending its own follow-on if the new
   repository needs its own CI shape for this class of check.

**Amended 2026-09-05 — RATIFIED 2026-09-05 by Brett Heap, in-session, verbatim "ratify and merge 704, 214 and 18", on openxFactory PR #704 — at retirement measurement** — § D2.1 assigns `workers/`,
the host-side `scripts/` and the JUDGED docs to `OmniWorker-Install`, and § D2.2
assigns the manager-review runtime, the compose and Kubernetes topology and the
`omnigent-install-manifest` realization to `Omnigent-Install`. **Both
assignments stand. What neither table measured is that the second set READS the
first set at run time**, and it does so in thirty-nine places.

PR opensoft/Omnigent-Install#213 measured it by removing the whole copied tree in its
own branch and re-running every validator: **ten of the twelve repository
validators are green on that repository's `main`, and removing all 120
candidate paths broke all ten**, including all three the dartwing workflow runs
by name. The consumers are `manager_review/runner.py`,
`agents/manager-review/seat-*.yaml`, both compose stacks,
`k8s/local/worker-lanes.yaml`, `config/omnigent-install-manifest.yaml` and its
render-verify arm, eleven validators and eight test modules — every one of them
§ D2.2 material. The full path-by-path inventory is `docs/omniworker-split.md` in
PR opensoft/Omnigent-Install#213, which is the requirements source for the remedy.

**Brett Heap RULED it 2026-09-05: "Orchestrator pins OmniWorker-Install."**
`OmniWorker-Install` is CANONICAL for the worker profiles, the schemas
(including `workers/schemas/artifact-worker-heartbeat.schema.json`), the
heartbeat publisher and the other Part 1 material; the orchestrator CONSUMES
them through a **commit-plus-digest pin** — the estate pattern this repository
already runs twice, `contracts/openxwallet-pin.yaml` and
`contracts/openreposhape-pin.yaml`. Nothing is re-homed back across the
boundary; § D2.1 and § D2.2 both stand exactly as written, and the orchestrator
reads the canonical copy at a verified commit instead of carrying a second one.

That single mechanism closes four of the five items `docs/omniworker-split.md`
recorded as owed before Part 1 could be retired — the manager-review seat
material, the lane topology, the host-side scripts the orchestrator executes,
and the `omnigent-install-manifest` render-verify arm. The packet realizing it
is `Omnigent-Install`'s `add-omniworker-install-pin`.


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

**Amended 2026-09-05 — RATIFIED 2026-09-05 by Brett Heap, in-session, verbatim "ratify and merge 704, 214 and 18", on openxFactory PR #704 — on Brett Heap's ruling "Orchestrator pins
OmniWorker-Install"** — the sequence above has nine steps and the retirement is
step 9. It is now TEN, with a new step between the copy and the retirement:

```text
8b PIN        Omnigent-Install declares contracts/omniworker-install-pin.yaml —
              commit d617e68e plus a sha256 for each of the 39 Part 1 paths it
              reads — writes the resolver and the drift-refusing verifier, and
              RE-POINTS every one of the 52 staying consumers to the resolved
              pinned checkout, one consumer class per PR, each green as it lands.
              Its packet is Omnigent-Install `add-omniworker-install-pin`.
```

**Step 9 now depends on 8b, and the dependency is the whole reason 8b exists.**
The order the ratified "Copy-first migration" requirement already imposes —
*"the source path MUST NOT be deleted from `Omnigent-Install` until every
declared consumer has been re-pinned and verified"* — was read in § D4 as a
statement about consumers OUTSIDE that repository, and all five of those were
re-pinned and merged (tasks § 4). It binds the consumers INSIDE it in exactly
the same words, and thirty-nine paths have them. So: **pin lands → consumers
re-pointed → validators green against the pinned checkout → THEN retirement.**

Step 9 also splits in two by consequence, because PR opensoft/Omnigent-Install#213
performed the half that was already lawful: the 50 Worker Host App paths whose
consumers had all left with them (Part 2, plus two orphaned evidence records).
The 70 Part 1 paths that remain are step 9's whole content, and they wait on 8b.

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

**Amended 2026-09-05, at task 4.6 measurement** — the NotebookLM row above and
D3 step 8 both assume `Omnigent-Install` already carries a sibling ideation
book, `xf-ideation-omnigent-install`, for `OmniWorker-Install` to gain a
sibling of. **That premise does not hold, and it never has.** Read against
`scripts/sync-notebooklm-books.py` and `docs/lifecycle-notebook-projection.md`
in this clone: `installs/*` repositories are OUT OF SCOPE for the
ideation-book projection BY DESIGN, not by omission — the script's own
`ROOT_LEVEL_GOVERNED_PRODUCTS` comment says the allowlist (`openAvatar`,
`openXwallet`) exists "never `every root-level `.gitmodules` pin`, which
would enrol the nine `installs/*` runtime repositories as governed ideation
repositories" (citing `split-openxwallet-repo` design D11), its `SKIP_PARTS`
set explicitly skips `installs`, and the projection doc states its scope as
"`openxFactory/` and `xFactories/*/`, skipping `.git`, `installs/`". Confirmed
live via `nlm notebook list`: no "xFactory Ideation — Omnigent-Install" book
exists today. Step 8 and this row are therefore not a task owed by this
change or its successor — there is nothing for `OmniWorker-Install` to gain a
sibling of, and running the sync would not create one, because the mechanism
does not reach `installs/*` at all.

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

**Amended 2026-09-05, ruled and executed** — Brett Heap ruled OQ-7 sequence
**(a)**, "yes, land it and then move it". `Omnigent-Install` PR #40 LANDED,
merge commit `f585eb2b`; `openspec/changes/add-worker-enrollment-broker-integration/`
was then copied AS LANDED into `OmniWorker-Install` PR #2 (`d617e68e`),
alongside `hostapp/` (task 3.1/3.3). **The copy's `code_surface:` declaration
still names `Omnigent-Install` paths** — sequence (a)'s cost, named above,
was paid but not yet discharged: the amendment of that declaration to name
`OmniWorker-Install` is owed in the COPY's own packet, in the
`OmniWorker-Install` repository, not in this one. This design does not
perform that amendment; it only records that it is owed and where.

**Amended 2026-09-05 — RATIFIED 2026-09-05 by Brett Heap, in-session, verbatim "ratify and merge 704, 214 and 18", on openxFactory PR #704 — OQ-6 ruled** — Brett Heap ruled § D6's OQ-6 the same day
he ruled the pin, and in the same shape as OQ-7: **"Land it in Omnigent-Install
first, then copy."** That is sequence **(a)** above, now this repository's rule
for BOTH in-flight changes rather than a one-off.

`Omnigent-Install`'s `add-worker-acr-push` therefore finishes and lands there.
Measured 2026-09-05: its repository work is already merged — PR opensoft/Omnigent-Install#129
(`509b7d65`, 2026-08-22) landed the schema, the `cpc-omni01` manifest block and
the four test cases, and PR opensoft/Omnigent-Install#143 (`5b5592e4`, 2026-08-24) landed the `hostapp/`
delta that consumes them. Nine of its thirteen tasks are ticked and the four
that remain are not code: a HUMAN/VAULT gate (mint the scoped `AcrPush` token
into `kv-opensoft-xfactory-qa`), a live-host confirmation, one notification, and
the archive its `gated-realization` target permits only after those. Its landed
packet and that `hostapp/` delta are then copied to `OmniWorker-Install` exactly
as PR opensoft/Omnigent-Install#40 was, with the `code_surface:` amendment owed **in the copy**, there —
the same debt sequence (a) already left on
`add-worker-enrollment-broker-integration`.

**Consequence: PR opensoft/Omnigent-Install#213 is HELD until `add-worker-acr-push`
lands.** That PR retires `schemas/worker-host-manifest.schema.yaml` and
`tests/test_worker_host_manifest.py`, two of the four paths
`add-worker-acr-push` declares as its `code_surface`. Retiring them while that
change is still active there would re-home it as a side effect of a file
deletion — precisely what this section's rule, and the ADDED requirement that
encodes it, forbid. The hold is sequencing, not a defect in opensoft/Omnigent-Install#213; its Part 2
retirement is sound on its merits.


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
`self-hosted, omnigent, artifact-only, doc-analysis, rider, host-<id>`). Under
"Omnigent orchestrates; omniWorker hosts" the label means the machine, and the
machine is now `omniWorker`.

**Measured, and the measurement is the useful part: NOTHING IN THE AGGREGATION
SELECTS ON IT.** All ten self-hosted xFactory lanes dispatch by runner GROUP
plus a per-host or per-lane label, never by `omnigent`:

| Workflow | `runs-on` group | `runs-on` labels |
|---|---|---|
| `clearing-dispatch.yml` (execution job) | `xfactory-execution-lane-workers` | `host-coding-cpc-brett01` |
| `clearing-dispatch.yml` (artifact job) | `xfactory-artifact-workers` | `host-rider-cpc-brett01` |
| `council-deliberation-worker.yml` (×2) | `xfactory-artifact-workers` | — |
| `execution-lane-coding-worker.yml` | `xfactory-execution-lane-workers` | `${{ inputs.dispatch_label }}` |
| `doc-health-analysis-worker.yml` | `xfactory-artifact-workers` | `${{ inputs.dispatch_label }}` |
| `doc-health-cataloger-worker.yml` | `xfactory-artifact-workers` | `${{ inputs.dispatch_label }}` |
| `doc-health-derive-possibles-worker.yml` | `xfactory-artifact-workers` | `${{ inputs.dispatch_label }}` |
| `doc-health-readiness-worker.yml` | `xfactory-artifact-workers` | `${{ inputs.dispatch_label }}` |
| `dashboard-image-worker.yml` | `xfactory-artifact-workers` | `${{ inputs.dispatch_label }}` |
| `review-lane-worker.yml` | `xfactory-artifact-workers` | `${{ inputs.dispatch_label }}` |
| `ideation-organizer-worker.yml` | `xfactory-artifact-workers` | `${{ inputs.dispatch_label }}` |

`omnigent` is a label the runners REGISTER and nothing here SELECTS. So the
cost is a runner re-registration plus a doc sweep — **not** a workflow sweep,
and **no lane loses its dispatch path while it happens.** That is materially
cheaper than the label lists in the runbooks suggest, and it is why this
question is worth putting rather than deferring.

**Change it, keep it, or add `omniworker` as a second label and retire
`omnigent` later?** This packet recommends the third — a runner may hold both,
so the retirement is free once nothing names the old one — and does not assume
it. The measurement above is scoped to the xFactory aggregation; a consumer
outside it (a codexFactory lane, an operator's ad-hoc dispatch) would have to
be swept before the retirement half.

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
