# Tasks: implement-omniworker-install-repo

Dependency-ordered, and the order is the whole safety argument. §1 (ratify the
name and the boundary) before §2 (create the repository), §2 before §3 (there
is nothing to copy into until it exists), §3 before §4/§5 (a consumer cannot be
re-pinned at a path that holds nothing), §4 and §5 complete before §6
(retirement is the only destructive step and it is last), and §7 is the archive
gate. §8 is the named work this change deliberately does NOT do.

**Every box below is unchecked. Nothing in this list has been performed.**
This packet is `Status: draft`; it authors a boundary, a naming record and a
plan, and it performs none of them.

Reasoning for every decision is in [design.md](design.md); the obligations are
in [specs/repo-boundary-governance/spec.md](specs/repo-boundary-governance/spec.md).
Structurally parallel to [`implement-keycloak-install-repo`](../implement-keycloak-install-repo/tasks.md)
and [`implement-openxpki-install-repo`](../implement-openxpki-install-repo/tasks.md),
which are the two nearest repository-creation precedents in this corpus.

**Amended 2026-09-08 — THE ARCHIVE TICKS. APPROVED 2026-09-08 ~12:2xZ by Brett
Heap, in-session, verbatim "archive implement-omniworker-install-repo",
recorded on opensoft/openxFactory#591** — every box still open at that word is
closed below, and each one says WHICH KIND of close it is, because the kinds are
not interchangeable:

- **on the evidence** — the act was performed and the record cites the landed
  commit that performed it (1.2, 7.1, 7.2, 7.4, 8.1, 8.2, and 6.1/7.3/8.5 on
  opensoft/Omnigent-Install#213's merge);
- **answered by the act** — an open question the packet refused to guess was
  settled by what was actually done, and the record cites the artefact that
  settles it (1.3/7.5's OQ-2, OQ-3, OQ-4, OQ-8, OQ-10);
- **on a NAMED SUCCESSOR** — the act is NOT done, is owed elsewhere, and an
  issue now names it with a date, under Brett Heap's ruling of 2026-09-06,
  verbatim **"Tick on the recording"** (6.3, 8.3, 8.4, and 1.3/7.5's OQ-1,
  OQ-5, OQ-9). Five issues were filed at this archive, all UNCLAIMED:
  opensoft/openxFactory#794 (OQ-1), opensoft/openxFactory#795 (OQ-5 / § 8.3),
  opensoft/openxFactory#796 (OQ-9 / § 8.4), opensoft/xFactory#346 and
  opensoft/CloudPC-Install#19 (the two halves of § 6.3);
- **the archive's own statement** — 7.6, which ticks at the archive with the
  evidence summary because that is what the box is.

*No tick claims work that was not done*, and no box's ratified requirement
sentence is rewritten — the state changes, the note is appended, and the
original text stays readable against it, which is the in-place amendment
convention this packet already used for its 2026-09-05 amendments (PR #704) and
its § 5 dispositions (PR #773). **The opening line "Every box below is unchecked.
Nothing in this list has been performed." was true of the ratified draft and is
superseded by this amendment and its four predecessors.**

## 1. Naming ratification and boundary (openxFactory; this change's own PR)

- [x] 1.1 Ratify this packet. Brett Heap's word on the PR or on the governing
      issue; the packet is `Status: draft` until then, and the four rulings it
      quotes (name, scope, template, reprovision) are the authority for those
      four facts only — not for the boundary, the split table, or the
      choreography, which are this packet's proposals.
      Recorded 2026-09-05: Brett Heap, "ratify 680 and merge 16", on PR #680 at head
      `91866619`; proposal `Status: ratified` + `Ratified:` line; naming record `Status: ratified`.
- [x] 1.2 On landing, flip `docs/omniworker-naming.md` from `Status: draft` to
      `Status: ratified`. `Ratified by: implement-omniworker-install-repo`
      already names this change; the lifecycle ratification IS this change
      landing, on the `docs/openxdox-naming.md` precedent.
      **Recorded 2026-09-08 — DISCHARGED AT LANDING; ticks on the evidence, and
      the evidence is read rather than asserted.** `git show
      76434aac:docs/omniworker-naming.md` reads `Status: ratified` on line 3 and
      `Ratified by: implement-omniworker-install-repo` on line 4 — `76434aac` is
      this change's own landing squash ("Name the worker host omniWorker, and
      split it out rather than rename Omnigent (#680)",
      2026-09-05T18:18:01Z), so the flip happened IN the landing commit rather
      than in a follow-on, which is exactly what this box asked for. The record
      still reads `Status: ratified` at `main` `9581ed9b`: neither Amendment A1
      (opensoft/openxFactory#784 → squash `6c9e3627`) nor the precision pass
      (opensoft/openxFactory#789 → squash `9581ed9b`) touched either header
      line, and A1 says so in terms.
- [x] 1.3 Answer OQ-1 through OQ-10 (design § D6). Each answer is recorded as a
      dated amendment to this tasks file or to `design.md`, naming Brett's
      words, before the task it gates runs. **OQ-7 (the in-flight change) and
      OQ-10 (visibility) gate §2 and §3 and cannot be deferred past them.**
      **Recorded 2026-09-08 — ALL TEN DISPOSED, and each one names its own
      kind: THREE ruled by Brett Heap, FOUR answered by the act with the
      settling artefact cited, THREE explicitly deferred to a named successor
      issue.** Nothing below is asserted from memory; every "verified" is a
      2026-09-08 read of the live repository or of git.
      - **OQ-1** — `docs/runbooks/codexfactory-execution-lane-enablement.md`,
        host runbook or orchestrator runbook? **DEFERRED, holder Brett Heap:
        opensoft/openxFactory#794.** Verified 2026-09-08: the file is STILL
        PRESENT in `Omnigent-Install` (blob `a0bcc2b8`, after the Part 1
        retirement) and ABSENT from `OmniWorker-Install` (404) — so it stayed
        with the orchestrator BY DEFAULT, not by decision, and the runbook's own
        self-description still reads *"worker procedure lives in
        Omnigent-Install"*, a sentence the split made false whichever way OQ-1
        is answered. The issue carries both exits and the doc edit each entails.
      - **OQ-2** — `workers/scaleout/` versus `docs/runbooks/phase8-scaleout.md`
        and `compose/phase8-worker-stack/`; accept the seam or move the runbook?
        **ANSWERED BY THE ACT: the seam is ACCEPTED and MECHANIZED, so it is no
        longer a seam across two truths.** `workers/scaleout/` moved (§ D2.1);
        `compose/`, `k8s/` and the phase-8 runbook stayed (verified 2026-09-08:
        `docs/runbooks/phase8-scaleout.md` blob `45f038b5` at
        `Omnigent-Install@main`); and both compose stacks plus
        `k8s/local/worker-lanes.yaml` now reach the moved topology through
        `${OMNIWORKER_ROOT}`, where a missing value is `required variable
        OMNIWORKER_ROOT is missing a value` and never a relative fallback.
        Realized opensoft/Omnigent-Install#217 `4f82cbd8`; recorded as row 2 of
        that repository's `docs/omniworker-split.md` § "The five owed rulings —
        all closed", landed opensoft/Omnigent-Install#235 `bbba916d`.
      - **OQ-3** — after the split, does a worker HOST still check out the
        ORCHESTRATOR repository for its compose stack? **ANSWERED BY THE ACT:
        YES, deliberately.** opensoft/CloudPC-Install#17 → squash `bba9da8a`
        re-pointed only the moved-path references and KEPT the
        orchestrator/compose-checkout wording, per the gate task 4.7 names;
        recorded in 4.7's dated note of 2026-09-05. `OmniWorker-Install` is
        therefore not sufficient to stand up a host on its own, which is the
        consequence § D6 asked to have made explicit rather than implicit.
      - **OQ-4** — the root `schemas/` directory: one file's worth of directory,
        or move it to `workers/schemas/`? **ANSWERED BY THE ACT: root
        `schemas/`, and by measurement rather than taste.**
        `scripts/validate_worker_host_manifest.py` and
        `tests/test_worker_host_manifest.py` consume BOTH
        `worker-host-manifest.schema.yaml` and `bench-manifest.schema.yaml` by
        hard-coded path, so the pair moved together (task 3.2's `Amended:`
        note). Verified 2026-09-08 through the contents API:
        `OmniWorker-Install/schemas/` holds exactly those two files, and
        `workers/schemas/` holds only `artifact-worker-heartbeat.schema.json`.
      - **OQ-5** — the GitHub runner label `omnigent`. **DEFERRED, holder Brett
        Heap: opensoft/openxFactory#795**, which is also task 8.3's named
        successor. The measurement that makes the ruling cheap stands and is
        carried into the issue: nothing in the aggregation SELECTS on the label;
        all ten self-hosted lanes dispatch by runner GROUP plus a per-host or
        per-lane label.
      - **OQ-6** — which repository owns
        `openspec/changes/add-worker-acr-push/`? **RULED 2026-09-05 by Brett
        Heap, verbatim "Land it in Omnigent-Install first, then copy"**
        (opensoft/openxFactory#591 ~22:20Z), recorded as `design.md` § D5's
        dated amendment and RATIFIED 2026-09-05 in-session, verbatim "ratify
        and merge 704, 214 and 18", on opensoft/openxFactory#704.
      - **OQ-7** — `add-worker-enrollment-broker-integration` sequencing, (a) or
        (b)? **RULED 2026-09-05 by Brett Heap, sequence (a), verbatim "yes, land
        it and then move it"** — and PERFORMED:
        opensoft/Omnigent-Install#40 landed first (merge commit `f585eb2b`) and
        the change directory was copied AS LANDED into
        opensoft/OmniWorker-Install#2 `d617e68e` (tasks 3.1/3.3, design § D5).
        Sequence (a)'s named cost is carried, not hidden: the copy's
        `code_surface:` still names `Omnigent-Install` paths and its amendment
        is owed in the COPY's own packet, there.
      - **OQ-8** — does the archived `openspec/changes/archive/` history travel
        with the moved code? **ANSWERED: NO — the archive stays whole**, which
        was this packet's own lean, adopted by the retirement act and recorded
        in `Omnigent-Install`'s `docs/omniworker-split.md`, verbatim:
        *"`openspec/changes/archive/` is untouched by design (OQ-8): an archive
        is a record of what happened, not an index of what is present, and the
        archived changes that describe how the moved code was built are still
        true."* Landed opensoft/Omnigent-Install#235 `bbba916d`.
      - **OQ-9** — the older openxFactory enumerations. **DEFERRED:
        opensoft/openxFactory#796**, which is also task 8.4's named successor,
        unclaimed. The deferral is the packet's own recommendation on the
        `implement-keycloak-install-repo` precedent, and the issue records the
        collision the refresh must check for first: both
        `implement-keycloak-install-repo` and `implement-openxpki-install-repo`
        are STILL ACTIVE in this repository at `main` `9581ed9b`.
      - **OQ-10** — visibility. **ANSWERED BY THE ACT: PRIVATE.** Verified
        2026-09-08 by `gh repo view opensoft/OmniWorker-Install`:
        `visibility: PRIVATE`, default branch `main`, created
        2026-09-05T16:15:48Z — matching `Keycloak-Install` /
        `OpenXPKI-Install` exactly as task 2.1 specified, so the assumption this
        box guarded was confirmed rather than overridden.
      **THE TWO GATING QUESTIONS WERE NOT DEFERRED PAST WHAT THEY GATE**, which
      is this box's last sentence and the only clause in it that could have been
      violated silently: OQ-7 was ruled 2026-09-05 before the § 3.3 copy ran,
      and OQ-10 was settled at the § 2.1 creation act itself.

## 2. Repository creation — Brett Heap's act, not this session's

- [x] 2.1 Create `opensoft/OmniWorker-Install`. **Visibility per OQ-10**
      (private to match `Keycloak-Install` / `OpenXPKI-Install` unless ruled
      otherwise), default branch `main`, description naming it the worker-host
      install repository for the xFactory fleet. Name spelled exactly
      `OmniWorker-Install` — capitalized on the `<Name>-Install` house form
      that `CloudPC-Install`, `Keycloak-Install` and `OpenXPKI-Install` already
      set, and that OpsxFactory's closed code-surface vocabulary checks against.
      Recorded 2026-09-05: `opensoft/OmniWorker-Install` created, private,
      default branch `main`, seed commit `c5d0f1f6`.
- [x] 2.2 Independently released, like its siblings: its own `main`, its own
      release line, its own validation. It is NOT a subtree of, and not
      released with, `Omnigent-Install`.
      Recorded 2026-09-05: own `main`, own ruleset, own harnesses (§3.4) —
      no subtree relationship to `Omnigent-Install` at any point in the copy.
- [x] 2.3 Install the governance plumbing AT CREATION, not later — the `main`
      ruleset requiring one approving review, the repository added to the
      `openxfactory` GitHub App installation so the content App can author
      PRs, the App secrets, and the `session-open-pr.yml` mirror. The
      authorship route works on day one or the first PR is authored by the
      only human who can approve it (the `implement-keycloak-install-repo`
      lesson, learned there).
      Recorded 2026-09-05 — HALF DONE: ruleset 22342039 "main review gate"
      (OrganizationAdmin bypass) and App secrets `OPENXFACTORY_APP_ID` /
      `OPENXFACTORY_APP_PRIVATE_KEY` are set. **OWED to Brett**: adding the
      repository to the `openxfactory` GitHub App installation (a web act
      only an org admin can perform) — until then the content App cannot
      author PRs there and the `implement-keycloak-install-repo` day-one
      lesson applies (the first PR is authored by the only human who can
      approve it).
      Confirmed 2026-09-05: still OWED — the App-repository-access half
      remains Brett Heap's web act, unchanged by the §4 re-pins below.
      **Recorded 2026-09-08 — SUCCESSOR NAMED: opensoft/openxFactory#800**,
      filed at this archive and holding the one clause of four that is still
      owed. Ticks on the recording under Brett Heap's ruling of 2026-09-06,
      verbatim "Tick on the recording". **The two OWED notes above are left
      exactly as they stand — this note names their successor, it does not
      claim their work was done**, and the box moves from `[~]` to `[x]` as a
      RECORDING, not as a discharge.
      *Three clauses of four discharged, unchanged from the notes above*: the
      `main` ruleset **22342039** "main review gate", the App secrets
      `OPENXFACTORY_APP_ID` / `OPENXFACTORY_APP_PRIVATE_KEY`, and the
      `session-open-pr.yml` mirror — which is, measured 2026-09-08, that
      repository's ONLY workflow file.
      *The fourth, measured in both directions and neither direction hidden.*
      TOWARD DISCHARGED: the `openxfactory` App's installation is
      `repository_selection: all`, so `OmniWorker-Install` sits inside it
      without a per-repository add, and a down-scoped token for that repository
      WAS actually minted in CI — `Omnigent-Install`'s
      `dartwing-activation-validation.yml` ran `actions/create-github-app-token`
      with `repositories: OmniWorker-Install`, `permission-contents: read`, log
      reading `creating token for repositories "OmniWorker-Install"` and the
      token revoked at cleanup (run 34041914618, re-proved on 34042785728).
      STILL OWED: that mint proves `contents: read`, while AUTHORING a pull
      request needs `contents: write` PLUS `pull_requests: write`, which no run
      has requested against this repository — and **all six pull requests in
      `OmniWorker-Install` are authored by `brettheap`** (#1, #2, #3, #5, #6,
      #7), none by the App. Six pull requests in, the authorship route has never
      been exercised, which is exactly the failure mode this box's last sentence
      names. #800 records what would prove it (one authoring attempt with both
      write permissions, the resulting `author.login`, then close and delete)
      and that the permission grant, if one is needed, is Brett Heap's.
- [x] 2.4 Seed the README with the ownership boundary quoted VERBATIM from the
      ratified requirement — `openxFactory` owns factory workflow policy;
      `OmniWorker-Install` owns worker-host install, operations, and DR;
      `Omnigent-Install` remains the orchestrator. Quoted, never paraphrased:
      the "Install repo scope links" requirement wants the link, and the
      Keycloak-Install README is the worked example of quoting rather than
      restating.
      Recorded 2026-09-05: README seeded at repository creation (seed
      `c5d0f1f6`) quoting the ownership boundary verbatim.
- [x] 2.5 Pin the compatible openxFactory contract bundle tag plus exact
      contract commit and per-file digests for the neutral contracts the host
      consumes, on the `pinned_contract_manifest` shape.
      Recorded 2026-09-05: `contract-pin.yaml` at contract-v3.4, contract
      commit `807a4f47`, per-file digests for the seven worker-enrollment
      schemas, pinned at `190f5dc`.

## 3. Copy-first migration (design § D2, § D3 step 2)

**Copy. Do not move.** Nothing is deleted from `Omnigent-Install` in this
group; §6 is where deletion lives, and only after §4 and §5.

- [x] 3.1 Copy the RULED tree: `hostapp/`, `workers/`,
      `clients/opensoft/worker-hosts/`, `scripts/publish_artifact_worker_heartbeat.py`,
      `docs/runbooks/cloudpc-named-worker-licensing.md`,
      `docs/runbooks/cloudpc-worker-pack.md`,
      `docs/runbooks/doc-health-cloudpc-pilot.md` (with its correction banner
      intact), `docs/worker-deployment-phases.md`.
      Recorded 2026-09-05: `workers/`, `clients/opensoft/worker-hosts/`,
      `scripts/publish_artifact_worker_heartbeat.py`, and the four runbooks
      copied in OmniWorker-Install PR #1 → `eb0c9675` (72 files). `hostapp/`
      copied separately in PR #2 → `d617e68e`, sequenced behind Omnigent-Install
      PR #40 landing (see 3.3) per the OQ-7 ruling.
- [x] 3.2 Copy the JUDGED tree, each item re-checked against its content at
      copy time and any disagreement raised rather than carried:
      `docs/credential-auth-profiles.md`, the three llm-credential runbooks,
      `docs/worker-hosts.md`, `schemas/worker-host-manifest.schema.yaml`
      (placement per OQ-4), `evidence/worker-host-manifest/`,
      `rendered/effective-profiles/`, the twenty-one host-side `scripts/`, and
      the eight host-side `tests/` including the `pwsh_host.py` harness.
      Recorded 2026-09-05: bulk of the JUDGED tree copied in PR #1 →
      `eb0c9675`; the manifest schema and its five dependent tests copied in
      PR #2 → `d617e68e` alongside `hostapp/`. Two disagreements surfaced and
      are recorded as `Amended:` notes in design.md § D2 rather than carried
      silently: `schemas/bench-manifest.schema.yaml` and
      `examples/bench-manifests/python-bench.example.yaml` MOVED (design §
      D2.2 said stay) because `scripts/validate_worker_host_manifest.py` and
      `tests/test_worker_host_manifest.py` consume them by hard-coded path;
      `tests/test_worker_auth_bootstrap.py` STAYED with the orchestrator
      (design § D2.1 listed it as moving) because its subject is
      `containers/omnigent-worker/scripts/*`, not host material.
- [x] 3.3 Re-home `openspec/changes/add-worker-enrollment-broker-integration/`
      by the sequence OQ-7 rules — **(a)** land PR #40 in `Omnigent-Install`
      first and copy the post-merge tree, or **(b)** re-target the change and
      re-open its PR against `OmniWorker-Install` with an amendment to its
      `code_surface:` declaration. Not by default and not by side effect.
      Recorded 2026-09-05: sequence **(a)** — Brett Heap's ruling on OQ-7,
      "yes, land it and then move it". Omnigent-Install PR #40 LANDED,
      merge commit `f585eb2b`; the change directory was then copied AS
      LANDED into OmniWorker-Install PR #2 → `d617e68e`. Its `code_surface:`
      declaration still names Omnigent-Install paths — the amendment of that
      declaration is owed in the COPY's own packet (in OmniWorker-Install),
      recorded here and in design.md § D5, not performed by this PR.
- [x] 3.4 Prove the copied harnesses GREEN in the new repository before
      anything else depends on them: the PowerShell host-app and deploy
      suites, `test_worker_host_manifest.py`,
      `test_publish_artifact_worker_heartbeat.py`,
      `test_rider_heartbeat_contract.py`, `test_worker_auth_bootstrap.py`,
      `test_artifact_lane_contract.py`. The ratified copy-first requirement's
      second scenario makes this the gate, not a courtesy.
      Recorded 2026-09-05: every suite green at the new location — HostApp
      1027 tests, Deploy 256 tests, unittest 76 tests, the manifest validator,
      and the canonical worker-enrollment validator at 0/0 findings (from
      pin `190f5dc`); the boundary validator (3.5) reports 0 findings.
- [x] 3.5 Add the repository's own boundary validator refusing a committed
      credential value — model-provider credential, runner registration token,
      enrollment lease secret, Key Vault secret value, host service-account
      password — reusing the detection classes the estate's existing
      secret-scanners already established rather than inventing a second
      vocabulary for "this is a secret".
      Recorded 2026-09-05: boundary validator added and run at the new
      location — 0 findings.

## 4. Consumer re-pins — EACH ITS OWN PR, in its own repository

- [x] 4.1 **xFactory `.gitmodules`** gains `installs/omniworker-install` →
      `git@github.com:opensoft/OmniWorker-Install.git` as a SIBLING entry.
      `installs/omnigent-install` is not renamed and not removed. Records the
      exact validated commit; the governed admission record is §8.1, not this.
      Recorded 2026-09-05: xFactory PR #268, "Add installs/omniworker-install
      sibling submodule + re-point worker-profile comments" → squash
      `2f767ac8` — gitlink `160000` at OmniWorker-Install `d617e68e`, verified
      `git cat-file -t` = commit; covers this task and 4.2 together. Substrate
      row 5 on xFactory #227 claimed and released.
- [x] 4.2 **xFactory workflow comments** — `doc-health-cataloger-worker.yml`,
      `doc-health-readiness-worker.yml`,
      `doc-health-derive-possibles-worker.yml`,
      `ideation-organizer-worker.yml` — re-point the four
      `installs/omnigent-install/workers/profiles/*.yaml` references. Comments,
      not checkouts (design § D4 measured it): a comment naming a path nothing
      contains is worse than no comment.
      Recorded 2026-09-05: xFactory PR #268 → squash `2f767ac8` (see 4.1) —
      four workflow comments re-pointed.
- [x] 4.3 **OpsxFactory `models/code-surface-repositories.yaml`** gains one
      entry `- id: OmniWorker-Install / source: aggregation_submodule`, in the
      alphabetical block. **Depends on 4.1**: the
      `code_surface_repository_registry` validator arm re-derives an
      `aggregation_submodule` entry against the aggregation `.gitmodules`, so
      an entry landed before the pin is a finding rather than a claim.
      Recorded 2026-09-05: OpsxFactory PR #228 → merge commit `6a0d9467` —
      entry `- id: OmniWorker-Install / source: aggregation_submodule` added;
      landed AFTER xFactory PR #268 because
      `scripts/release_realization_axis.py::_aggregation_gitmodules`
      re-derives from the workspace `.gitmodules` (a standalone clone/CI
      recorded a skip before then); proven in a simulated workspace — before
      #268 a finding, after #268 "21 declared, 21 present, exact match".
- [x] 4.4 **CloudPC-Install `packs/service-rider/selftest/check_heartbeat_contract.py`**
      — `OMNIGENT_ROOT` gains `OMNIWORKER_ROOT` and the sibling-directory
      candidates gain `OmniWorker-Install` / `omniworker-install`, with the
      old names kept as a deprecating fallback for one release. **Verify by a
      run that does NOT skip**: the selftest skips when the sibling is absent,
      so a green summary cannot distinguish a correct re-pin from a missing
      one.
      Recorded 2026-09-05: CloudPC-Install PR #17 → squash `bba9da8a` —
      `find_worker_root()`: `OMNIWORKER_ROOT` / `OmniWorker-Install` /
      `omniworker-install` primary; `OMNIGENT_ROOT` and the old siblings kept
      one release as a DEPRECATED fallback with a notice. Three-run proof:
      new root RUNS PASS 31/0/0 skips; fallback RUNS PASS 31 with the notice;
      neither present → SKIPPED, exit 1.
- [x] 4.5 **openxFactory references** to `Omnigent-Install` worker paths.
      Scoped by measurement at re-pin time; `contracts/manifest.yaml`'s nine
      `Omnigent-Install/schemas|policies/...` source paths are NOT in scope
      (those families stay with the orchestrator — design § D4).
      Recorded 2026-09-05 — measured by `grep -rn "Omnigent-Install"
      contracts/ openspec/specs/` in this clone: every reference to
      `Omnigent-Install` under `contracts/` and `openspec/specs/` (7 files:
      `contracts/manifest.yaml`, `contracts/README.md`, `contracts/CHANGELOG.md`,
      `contracts/worker-enrollment/README.md`,
      `openspec/specs/shared-contract-ownership/spec.md`,
      `openspec/specs/canonical-contract-migration/spec.md`,
      `openspec/specs/repo-boundary-governance/spec.md`) names either an
      ORCHESTRATOR schema/policy family (the Hermes job envelope/event/run
      schemas, the three clarification schemas, `hermes-operational-postgres`,
      `hermes-governance-agents`, `merge-risk-policy` — `contracts/manifest.yaml`
      and `contracts/README.md`), a historical changelog entry
      (`contracts/CHANGELOG.md`), prose naming Omnigent-Install as the actor
      that consumes the worker-enrollment broker
      (`contracts/worker-enrollment/README.md`, not a source-path
      declaration), or canonical text establishing the general
      `repo-boundary-governance` capability (the three `openspec/specs/`
      files, already flagged incomplete by design § D6 OQ-9). **Zero
      references to worker/host material paths** (`hostapp/`, `workers/`,
      `schemas/worker-host-manifest.schema.yaml`, etc.) exist under
      `contracts/` or `openspec/specs/` — nothing in scope for this task.
      Nothing changed in `contracts/` or `openspec/specs/` by this PR.
- [x] 4.6 **NotebookLM projection** — one ideation book per governed repo, so
      the new repository gets `xf-ideation-omniworker-install` /
      *"xFactory Ideation — OmniWorker-Install"*, added via
      `python3 openxFactory/scripts/sync-notebooklm-books.py . --apply` per
      `docs/lifecycle-notebook-projection.md`. Books resolve by TITLE; the
      capacity guard applies.
      Recorded 2026-09-05 — DISCHARGED by finding, sync NOT run: `installs/*` repositories
      are OUT OF SCOPE for the ideation-book projection BY DESIGN, not merely
      by omission. `scripts/sync-notebooklm-books.py`'s own comment on
      `ROOT_LEVEL_GOVERNED_PRODUCTS` (only `openAvatar`, `openXwallet`) says
      an allowlist is used "never `every root-level `.gitmodules` pin`, which
      would enrol the nine `installs/*` runtime repositories as governed
      ideation repositories (`split-openxwallet-repo` design D11)"; its
      `SKIP_PARTS` set explicitly skips `installs`; and
      `docs/lifecycle-notebook-projection.md` states the scope as
      "`openxFactory/` and `xFactories/*/`, skipping `.git`, `installs/`".
      Confirmed live: `nlm notebook list` carries no
      "xFactory Ideation — Omnigent-Install" book today, and none will be
      created for `OmniWorker-Install` either — the D3 step 8 / D4 table
      premise (that Omnigent-Install already has a sibling ideation book to
      gain a sibling of) does not hold. Recorded as an `Amended:` note in
      design.md § D3/D4. No list needs to gain `OmniWorker-Install`; there is
      no automatic discovery to rely on either — the mechanism does not
      reach `installs/*` at all.
- [x] 4.7 **The enrollment broker and CloudPC-Install docs** that name
      `omnigent-install` as the host checkout — `docs/worker-host-pack.md`,
      `docs/host-token-broker.md`, `docs/host-broker-provisioning-prompt.md`,
      `docs/doc-analysis-worker-host.md`, `README.md`. **Gated on OQ-3**: if
      the host continues to check out the orchestrator repository for its
      compose stack, most of these are CORRECT as they stand and only the
      moved-path references change.
      Recorded 2026-09-05: CloudPC-Install PR #17 (see 4.4) — moved-path
      references re-pointed in `README.md`, `docs/worker-host-pack.md`,
      `docs/host-token-broker.md`, `docs/doc-analysis-worker-host.md` (7
      refs total); an orientation note added to
      `docs/host-broker-provisioning-prompt.md`; orchestrator/compose-checkout
      wording kept per the OQ-3 gate this task names.

## 5. Machine reprovision and its consequence (operator acts)

**Amended 2026-09-07 — Amendment: § 5 dispositions — APPROVED 2026-09-07 ~22:55Z by Brett Heap, in-session, verbatim "do all 4, they are all approved", recorded on opensoft/openxFactory#591** — the three
boxes this section left open now close on the record: **5.1 and 5.5 as
SUPERSEDED BY RULING**, **5.2 by a recorded DISPOSITION**. The ruling those two
are superseded by is Brett Heap's of 2026-09-05 ~22:50Z on
opensoft/openxFactory#591, verbatim: **"Accept Omni001-XEAON"**.

*No ratified REQUIREMENT TEXT is rewritten — and that is not the same claim as
"no lines changed".* Two things do change, deliberately: the **task state** of
5.1, 5.2 and 5.5 (`[ ]` → `[x]`), which is what recording a disposition means;
and the **amendment notes appended** below each box. What is left untouched is
the ratified prose — every box's original requirement sentence and the dated
note it already carried — so the supersession stays readable against exactly
what it supersedes. This is the in-place amendment convention this packet
already used for its four amendments of 2026-09-05 (openxFactory PR #704).

*Why an amendment and not a discharge.* opensoft/openxFactory#756 → squash
`73bb088e` (2026-09-07T16:55Z) ticked 5.3 and 5.4 on evidence and wrote honest
notes under 5.1, 5.2 and 5.5 leaving them OPEN, because no evidence discharges
them **as written**. Its landing note said the honest close was a packet
amendment for 5.1/5.5 and a recorded disposition for 5.2, on Brett's word. That
word is the approval quoted above.

*Consequence for § 6 — stated precisely, because it was contested and because
imprecision here would hide a real gap.* Three things have to be kept apart,
and this amendment claims only the first two.

1. **The ACTS were in order.** § 5's operator acts were performed 2026-09-05
   (reprovision ~22:24Z, read-back the same evening) with the OpsxFactory
   re-attestation landing 2026-09-06 (`83a91c58`); § 6's Part 1 retirement act
   landed 2026-09-07T12:12Z (opensoft/Omnigent-Install#235 `bbba916d`). The
   opening rule — "§4 and §5 complete before §6" — governs the acts, and the
   acts did not violate it.

2. **The RECORD lagged, and closing that lag is what this amendment does.**
   § 5's boxes were not ticked in this packet until
   opensoft/openxFactory#756 (5.3, 5.4) and this amendment (5.1, 5.2, 5.5), so
   when #756 recorded the § 6 retirement at 16:55Z on 2026-09-07 the packet
   still SHOWED § 5 open. That is exactly the Codex P2 raised against #756
   ("Satisfy the prerequisites before recording retirement"), and it was a fair
   reading of the packet as it then stood. § 5 is closed on the record from
   here.

3. **One clause of § 5 was never performed at all, and this amendment does not
   pretend otherwise.** 5.2's second imperative — confirm omni001's emptiness
   immediately before the act — did not happen, and it can no longer be
   evidenced. § 5 therefore closes with that clause DISPOSED, not discharged.
   Read strictly, "§5 complete before §6" was never satisfied for that one
   clause and cannot be made true retroactively; this amendment RECORDS that
   gap rather than curing it. What it asserts is only that the act the clause
   gated (the reprovision) was performed before § 6's retirement, and that the
   consequence the confirmation existed to prevent did not occur (5.2's
   disposition). **Nothing here waives the ordering rule, and nothing here
   makes the missing confirmation retroactively true.**
   Raised as a Codex P2 on opensoft/openxFactory#773 ("Do not mark the
   prerequisite as retroactively satisfied") against an earlier draft of this
   paragraph, which did claim the ordering "is satisfied"; the finding was
   taken and the claim narrowed to what is true.

- [x] 5.1 Set the Windows 365 provisioning policy device-name template to
      `CPC-OXF-%USERNAME:7%`. **New provisions only** — it renames nothing
      existing.
      NOT discharged as specified: Windows 365 requires `%RAND:5%` in every
      device-name template, so the literal `CPC-OXF-%USERNAME:7%` (no random
      suffix) could not be applied — the provisioning that ran used
      `%USERNAME:7%-%RAND:5%` and rendered `Omni001-XEAON`, not
      `CPC-OXF-Omni001`. [Precision note 2026-09-08 (opensoft/openxFactory#787
      → squash `7fa12108`): a random `%RAND:y%` segment is required in the
      device-name template; `%RAND:5%` is what was observed to be accepted,
      not the required token itself — `%RAND:2%` was tried and rejected as
      too short, and lengths 3, 4, and above 5 were never tried, so read
      "requires `%RAND:5%`" above as "requires a random segment; `%RAND:5%`
      is what was observed to be accepted."] Brett ruled
      "Accept Omni001-XEAON" (~22:50Z,
      openxFactory issue #591) — box superseded by ruling, not discharged.
      **Amended 2026-09-07 — SUPERSEDED BY RULING; box closed.** The template
      this box names is not reachable by supported means: Windows 365 refuses a
      device-name template without `%RAND:5%` and refuses a post-provision
      rename, so `CPC-OXF-%USERNAME:7%` could not be set and `CPC-OXF-Omni001`
      was never an attainable name. [Precision note 2026-09-08
      (opensoft/openxFactory#787 → squash `7fa12108`): "without `%RAND:5%`"
      over-states the evidence — what was measured is that a template with no
      random segment at all is refused and that `%RAND:2%` was rejected as
      too short; lengths 3, 4, and above 5 were never tried, so read this as
      "refuses a device-name template without a random `%RAND:y%` segment;
      `%RAND:5%` is what was observed to be accepted."] The template actually
      applied was
      `%USERNAME:7%-%RAND:5%`, which rendered `Omni001-XEAON` — Entra device
      `cf287ce7-7f73-4da7-adfb-c501bd7dd670`, the key by which the fleet now
      identifies the machine. Brett Heap ruled the outcome 2026-09-05 ~22:50Z
      on opensoft/openxFactory#591, verbatim: **"Accept Omni001-XEAON"**. That
      ruling IS the accepted outcome of this box, and it is what closes it: the
      box is ticked as SUPERSEDED, not as discharged as specified. The original
      requirement sentence is left standing above, unedited — the box's STATE
      changes, its ratified text does not — so the supersession can be read
      against it.
- [x] 5.2 Reprovision omni001. It is empty: no runner registered, no pilot
      ever run. Confirm that is still true immediately before the act.
      The box's substance is two imperatives, not one: reprovision, AND
      confirm the emptiness immediately before doing it. Only the first is
      evidenced. Recorded 2026-09-05 ~22:24Z: omni001 REPROVISIONED (Brett's
      ruling, executed as Graph by Brett; recorded on openxFactory issue
      #591) — new Cloud PC `Omni001-XEAON`; no runner or pilot was reported
      recovered or lost by the act. The second clause — a distinct,
      immediately-pre-act confirmation that omni001 was still empty — is NOT
      separately evidenced anywhere in the record. Left OPEN pending that
      confirmation being recorded; not superseded by any ruling.
      **Amended 2026-09-07 — DISPOSITION RECORDED; box closed. This is a
      disposition, not evidence that the confirmation happened**, and it must
      never be read as one.
      *Evidenced.* The reprovision: 2026-09-05 ~22:24Z, executed as Graph by
      Brett Heap and recorded on opensoft/openxFactory#591 — new Cloud PC
      `Omni001-XEAON`, new Entra device
      `cf287ce7-7f73-4da7-adfb-c501bd7dd670` (5.3).
      *Not evidenced, and now unrecoverable.* The second clause — a distinct,
      immediately-pre-act confirmation that omni001 was still empty — was never
      separately recorded, and the old device
      `08829330-2098-461c-a950-0047e163f2b1` is GONE from Entra (5.3), so the
      state that confirmation would have observed can no longer be observed. No
      later act can produce this evidence; leaving the box open would leave it
      open forever.
      *What stands as the record instead.* The observable consequence of the
      act. No runner and no pilot was reported lost by it, and the only
      registered endpoint in `fleet_scope` live targeting was REBOUND — not
      recovered — to the new device by opensoft/OpsxFactory#233 → merge commit
      `83a91c58` (5.4). Had omni001 carried a runner or a pilot, the loss would
      have surfaced in exactly that act.
      *Disposed* on Brett Heap's approval of this § 5 amendment, 2026-09-07
      ~22:55Z, in-session, verbatim "do all 4, they are all approved", recorded
      on opensoft/openxFactory#591.
- [x] 5.3 Read back the new Cloud PC name (`CPC-OXF-Omni001` expected) **and
      the new Entra device id**. Device `08829330-2098-461c-a950-0047e163f2b1`
      does not survive the reprovision.
      Recorded 2026-09-05: read back as new Cloud PC `Omni001-XEAON` (differs
      from the `CPC-OXF-Omni001` expectation — see 5.5's note), new Entra
      device `cf287ce7-7f73-4da7-adfb-c501bd7dd670` (registered 22:01:56Z,
      managed, compliant), Intune device `ff367aaf-3d42-429a-a939-42f1f5d6d327`;
      old device `08829330-2098-461c-a950-0047e163f2b1` confirmed GONE from
      Entra.
- [x] 5.4 **OWED, NOT THIS CHANGE — OpsxFactory fleet re-attestation.** The
      registration record and `workflows/endpoint-management.yaml`
      `fleet_scope.registered_endpoints` carry the old device id as the only
      endpoint in live targeting scope. Re-attest with the new id in its own
      governed change against the registration record — OpsxFactory's own rule
      is that a bound value moves by a new OpenSpec change and never by an
      in-place edit. Until it lands, live targeting names a device that does
      not exist.
      Recorded 2026-09-06: `reattest-omni001-fleet-registration` landed as
      opensoft/OpsxFactory#233 → merge commit `83a91c58` (01:18Z;
      `registered_endpoints[0]` rebound to
      `cf287ce7-7f73-4da7-adfb-c501bd7dd670` / `Omni001-XEAON`, digest
      `ece6d6c7…` pinned into `workflows/endpoint-management.yaml` in the same
      commit, retired id kept as dated history), ratified via
      opensoft/OpsxFactory#235 → merge commit `3e4cd248` (03:55Z).
- [x] 5.5 Confirm the rendered casing. `CPC-Omni0-P5AJB` and `CPC-brett-TUBV0`
      came from the same default template but differ in case, so the exact
      rendering of `%USERNAME:7%` is an observation to make, not a prediction
      to rely on. If it renders `CPC-OXF-omni001`, that is still fifteen legal
      characters and the record gets an amendment, not a re-provision.
      NOT discharged: the actual render (`Omni001-XEAON`) is not a casing
      variant of `CPC-OXF-...` at all — the `CPC-OXF-` prefix never applied
      (5.1's note) — so this box's anticipated remedy (a casing amendment)
      does not apply either. Superseded by Brett's "Accept Omni001-XEAON"
      ruling (~22:50Z, openxFactory issue #591); the CloudPC-Install
      fleet-identity doc correction landed as opensoft/CloudPC-Install#18 →
      squash `349d539d` (2026-09-05T23:39:33Z) recording the actual name and
      the mandatory `%RAND:5%` constraint, but that documents the outcome, it
      does not discharge this box's casing-of-the-ruled-template premise.
      [Precision note 2026-09-08 (opensoft/openxFactory#787 → squash
      `7fa12108`): "the mandatory `%RAND:5%` constraint" over-states what is
      established — a random `%RAND:y%` segment is mandatory; `%RAND:5%` is
      what was observed to be accepted, not proven as the exact required
      value.]
      **Amended 2026-09-07 — SUPERSEDED BY RULING; box closed**, for exactly
      the reason the note above already gives: the casing question never arose,
      because the `CPC-OXF-` prefix never applied (5.1's amendment). Brett
      Heap's "Accept Omni001-XEAON" (2026-09-05 ~22:50Z,
      opensoft/openxFactory#591) accepts the rendered name as it stands, so
      there is no casing to confirm and no casing amendment to make — the
      remedy this box anticipated has no premise left. The document that
      records the actual name and the mandatory `%RAND:5%` constraint is
      opensoft/CloudPC-Install#18 → squash `349d539d` (2026-09-05T23:39:33Z);
      it is cited as the record of the name, not as the discharge of this box.
      [Precision note 2026-09-08 (opensoft/openxFactory#787 → squash
      `7fa12108`): same over-claim as this box's earlier note above — "the
      mandatory `%RAND:5%` constraint" states a random `%RAND:y%` segment is
      mandatory; `%RAND:5%` is what was observed to be accepted, not proven
      as the exact required value.]
      The supersession is what closes the box.

## 6. Retirement — the ONLY destructive step, and it is last

**Amended 2026-09-05 — RATIFIED 2026-09-05 by Brett Heap, in-session, verbatim "ratify and merge 704, 214 and 18", on openxFactory PR #704 — on Brett Heap's two rulings of that day** — one box is
inserted BEFORE 6.1, and 6.1's remaining scope narrows by consequence. Neither
existing box is rewritten.

*Why.* PR opensoft/Omnigent-Install#213 attempted 6.1 and measured that it could not
finish: thirty-nine of the seventy-two §3.1 Part 1 paths are still read at run
time by § D2.2 material that STAYS in that repository — `manager_review/runner.py`,
`agents/manager-review/seat-*.yaml`, both compose stacks,
`k8s/local/worker-lanes.yaml`, `config/omnigent-install-manifest.yaml` and its
render-verify arm, eleven validators and eight test modules. Removing the whole
copied tree in that branch broke all ten repository validators that are green on
its `main`. The inventory is `docs/omniworker-split.md` in that PR. Brett ruled
the remedy: **"Orchestrator pins OmniWorker-Install."** See design § D2 and
§ D3's amendments.

*What opensoft/Omnigent-Install#213 did land, and what it did not.* It retired the 50 paths whose
consumers had all left with them — the §3.2 Worker Host App tree plus two
orphaned `evidence/worker-host-manifest/` records — and deferred the 70 Part 1
paths that remain. Those 70 are 6.1's whole remaining content, and they wait on
6.0.

*The hold on opensoft/Omnigent-Install#213.* Brett also ruled OQ-6 (design § D5's amendment): **"Land it
in Omnigent-Install first, then copy."** `Omnigent-Install`'s
`add-worker-acr-push` declares `schemas/worker-host-manifest.schema.yaml` and
`tests/test_worker_host_manifest.py` as part of its `code_surface`, and
opensoft/Omnigent-Install#213 retires both, so **opensoft/Omnigent-Install#213 is HELD until that change lands** — otherwise the
retirement re-homes an active change by side effect, which the ADDED
requirement forbids. Its repository work is already merged
(PR opensoft/Omnigent-Install#129 `509b7d65`, PR opensoft/Omnigent-Install#143 `5b5592e4`); what remains is a HUMAN/VAULT gate, a
live-host confirmation and its archive.

- [x] 6.0 **Realize the `Omnigent-Install` → `OmniWorker-Install` pin**, design
      § D3 step 8b: `contracts/omniworker-install-pin.yaml` declaring `commit`
      plus a `sha256` for each of the 39 Part 1 paths that repository reads (and
      the remaining 31 declared by commit, so the surface is complete), the
      resolver and the drift-refusing verifier, and the re-point of all 52
      staying consumers to the resolved pinned checkout — one consumer class per
      PR, each green as it lands — plus the CI step that materializes the pinned
      commit. Its packet is `Omnigent-Install` `add-omniworker-install-pin`
      (PR opensoft/Omnigent-Install#214, authored 2026-09-05 by this change's lane; Brett ratifies).
      **6.1 depends on this box**, on the ratified "Copy-first migration"
      requirement's own words — *"the source path MUST NOT be deleted from
      `Omnigent-Install` until every declared consumer has been re-pinned and
      verified"* — which § D4 read as a statement about consumers OUTSIDE that
      repository and which binds the ones inside it identically. Order: pin
      lands → consumers re-pointed → every validator green against the pinned
      checkout, proved with the pin RESOLVED and not skipped → THEN 6.1.
      Also depends on opensoft/Omnigent-Install#213 landing, which depends in turn on
      `add-worker-acr-push` landing (the OQ-6 hold above).
      Recorded 2026-09-07: `add-omniworker-install-pin` ratified
      (opensoft/Omnigent-Install#214 → `544c6319`), realized in twelve groups
      (opensoft/Omnigent-Install#215 `9760e060`,
      opensoft/Omnigent-Install#221 `2e0cb543`,
      opensoft/Omnigent-Install#217 `4f82cbd8`,
      opensoft/Omnigent-Install#216 `61db51bb`,
      opensoft/Omnigent-Install#223 `2a166115`,
      opensoft/Omnigent-Install#219 `e31251ed`,
      opensoft/Omnigent-Install#230 `02fb3fed`,
      opensoft/Omnigent-Install#218 `57b16077` +
      opensoft/Omnigent-Install#222 `e5732aa1`,
      opensoft/Omnigent-Install#220 `fb611deb`,
      opensoft/Omnigent-Install#227 `3ff2da69`,
      opensoft/Omnigent-Install#232 `72989c1d`,
      opensoft/Omnigent-Install#235 `bbba916d`), archived
      (opensoft/Omnigent-Install#237 `07bdc9c3`, 2026-09-07; capability
      `omniworker-install-pin` promoted).

- [x] 6.1 Delete the §3.1 and §3.2 paths from `Omnigent-Install`, in ONE
      reviewed PR against that repository, **only after every §4 box is
      checked and green**. Before this PR, every step is revertible by a
      single `git revert`; after it, recovery is a restore.
      Part 1 (the 70 pin-declared paths) RETIRED by
      opensoft/Omnigent-Install#235 `bbba916d` on 2026-09-07 after
      byte-identity 70/70 and CI green with the paths gone; Part 2 (the 50
      Worker Host App paths) is opensoft/Omnigent-Install#213, HELD on OQ-6
      until `add-worker-acr-push` lands — closes then. § 5 is not yet fully
      closed either: 5.3 and 5.4 are ticked with evidence above; 5.1 and 5.5
      remain open (superseded by Brett's "Accept Omni001-XEAON" ruling, not
      discharged); 5.2 remains open too (its reprovision half is evidenced,
      its pre-act empty-confirmation half is not).
      **Amended 2026-09-07 — the § 5 sentence immediately above is
      superseded.** § 5 is now CLOSED on the record: 5.3 and 5.4 ticked on
      evidence by opensoft/openxFactory#756 → squash `73bb088e`, and 5.1, 5.5
      and 5.2 closed by the § 5 amendment of 2026-09-07 (SUPERSEDED BY RULING /
      DISPOSITION RECORDED — 5.2 by disposition, NOT by discharge; § 5's
      amendment header records what that leaves unsatisfied). 6.1's only
      remaining dependency is Part 2 —
      opensoft/Omnigent-Install#213, HELD on OQ-6 until `add-worker-acr-push`
      lands there.
      **Recorded 2026-09-08 — CLOSED; ticks on the evidence, both parts.**
      Part 1 (the 70 pin-declared paths) was retired by
      opensoft/Omnigent-Install#235 `bbba916d` (2026-09-07T12:12:15Z) after
      byte-identity 70/70 and CI green with the paths gone. **Part 2 (the 50
      Worker Host App paths) LANDED as opensoft/Omnigent-Install#213 → merge
      commit `9c9c9355` (2026-09-08T13:05:48Z, from head `6feafc2d`)**, under a
      Rule 6 landing window because it re-homed
      `openspec/changes/add-worker-enrollment-broker-integration/` out of that
      repository — OQ-7 sequence (a) completing there. Its head was
      MERGEABLE/CLEAN with all four checks green (`validate`,
      `merge-master-approval`, `Digest-only pin scope`, `openspec-cli-pin`) and
      0 open review threads.
      *The OQ-6 hold recorded above was SUPERSEDED, and the supersession is
      stated rather than glossed.* The hold said #213 waits until
      `add-worker-acr-push` lands, because #213 retires two of the four paths
      that change declares as its `code_surface`. Brett Heap's word of
      2026-09-08 ~12:10Z, verbatim **"merge 213"** (recorded on
      opensoft/openxFactory#591), supersedes it. `add-worker-acr-push` was
      byte-identical to `main` at the merge (tree `7bb94b12`), so the
      retirement re-homed nothing by side effect in that directory — but the
      consequence is real and is recorded on the pull request and in that
      repository's `docs/omniworker-split.md`: two of its declared paths no
      longer exist in the repository that hosts it, and the `code_surface:`
      amendment naming `OmniWorker-Install` is owed in the COPY's own packet,
      there. **Brett's word is the authority for that outcome; this packet
      neither performs nor discharges that amendment**, which is design § D5's
      named cost of sequence (a), paid here rather than hidden.
      *The ordering rule holds for the acts.* § 4 is fully checked and § 5 is
      CLOSED on the record (amended 2026-09-07), so "§4 and §5 complete before
      §6" is satisfied — with the single clause § 5.2 records as DISPOSED, not
      discharged, and § 5's amendment header says exactly what that leaves
      unsatisfied.
- [x] 6.2 Update the `Omnigent-Install` README's scope list — remove "Cloud PC
      worker host registration", "worker containers and worker lane setup",
      "native Claude Code / Codex harness setup", "subsystem-specific worker
      profiles and prompt packs" — and add the scope link to
      `OmniWorker-Install` that the "Install repo scope links" requirement
      demands of both sides.
      Recorded 2026-09-07: done in opensoft/Omnigent-Install#235 `bbba916d`
      (README scope + doc index; `workers/`/`rendered/` gone).
- [x] 6.3 Re-run the four moved xFactory lanes and the CloudPC-Install
      selftests after retirement, to prove nothing was reaching the old paths
      unmeasured.
      Runs after 6.1 Part 2 closes.
      **Recorded 2026-09-08 — SUCCESSORS NAMED, NOT PERFORMED, and this note
      does not pretend otherwise.** This box's own last sentence is "Runs after
      6.1 Part 2 closes", and Part 2 (opensoft/Omnigent-Install#213) lands in
      the same window as this archive, so the re-run cannot have happened yet.
      Under Brett Heap's ruling of 2026-09-06, verbatim **"Tick on the
      recording"**, the box closes on NAMED successors — one per repository,
      because neither can perform the other's act:
      **opensoft/xFactory#346** (the four moved worker lanes) and
      **opensoft/CloudPC-Install#19** (the service-rider selftests). Both are
      UNCLAIMED and both are gated on #213 landing.
      *The measurement that made them necessary, taken 2026-09-08 and carried
      into both issues.* There is NO post-retirement run of any of the four
      lanes: `doc-health-cataloger-worker.yml` last ran 33830578322 (2026-09-04,
      **failure**), `doc-health-readiness-worker.yml` 33831413294 (2026-09-04,
      success), `doc-health-derive-possibles-worker.yml` 33831449410
      (2026-09-04, success), and `ideation-organizer-worker.yml` **has never
      run at all** — every one of those predates the Part 1 retirement of
      2026-09-07T12:12Z. `CloudPC-Install` has had no run since
      2026-09-05T23:14Z. Two facts are recorded so the re-run cannot be
      misread: the cataloger's red is **PRE-EXISTING** (its four most recent
      runs, 2026-09-02 through -04, are all `failure`) and must not be read as
      retirement damage; and a run that SKIPS is not evidence —
      opensoft/CloudPC-Install#17 already proved that trap, and its three-run
      proof (new root RUNS PASS / deprecated root RUNS PASS with the notice /
      neither present SKIPPED exit 1) is the shape the CloudPC half must
      repeat.

## 7. Archive conditions

- [x] 7.1 `opensoft/OmniWorker-Install` exists, is seeded, its harnesses are
      green on its own `main`, and its boundary validator refuses a planted
      credential.
      **Recorded 2026-09-08 — MET; ticks on the evidence, clause by clause.**
      *Exists and is seeded.* `opensoft/OmniWorker-Install` created
      2026-09-05T16:15:48Z, `visibility: PRIVATE`, default branch `main`, seed
      commit `c5d0f1f6` whose README quotes the ownership boundary verbatim from
      the ratified requirement (tasks 2.1/2.4; re-verified 2026-09-08 by
      `gh repo view`).
      *Harnesses green on its own `main`.* opensoft/OmniWorker-Install#1 →
      `eb0c9675` recorded, at the new location and with no import-path fixes:
      `test_publish_artifact_worker_heartbeat` 9 passed,
      `test_rider_heartbeat_contract` 11, `test_artifact_lane_contract` 9,
      `test_validate_boundary` 16, plus 12/12 JSON and 26/26 YAML files parsing.
      opensoft/OmniWorker-Install#2 → `d617e68e` added the Worker Host App
      suites (HostApp 1027 tests, Deploy 256, unittest 76) and the manifest
      validator, with the canonical worker-enrollment validator at 0/0
      findings. `main` has stayed green through four later merges —
      opensoft/OmniWorker-Install#3 `33eed467`, #5 `54daeb3c`, #6 `322ee4da`,
      #7 `187d75b6` (`main` tip 2026-09-08T03:51Z, the archive of that
      repository's own `add-manifests-root-parameter`).
      *Measured honestly rather than overstated.* `OmniWorker-Install` carries
      no CI workflow but `session-open-pr.yml`, so "green on its own `main`"
      rests on the suite runs recorded in those pull requests and NOT on a
      required status check — there is no required check in that repository to
      cite (confirmed on #5 and #6: the only reporting app is non-required).
      *Boundary validator refuses a planted credential.*
      `scripts/validate-boundary.py` reports 0 findings on the tree, and its
      unit suite contains planted-secret cases that are all CAUGHT — a
      GitHub-token-shaped value, a PEM header, a `.claude/` runtime path and an
      assigned credential env var (#1, 16 tests). #2 took the suite to 24 and
      added the control that matters for the two exact-path, class-scoped
      exemptions it introduced for the hostapp fixtures' by-design token-shaped
      negative controls: **the same bytes outside an exempt path are still
      flagged**, so the exemptions cannot be read as a weakened pattern. The
      validator also records a measured refusal to import a vocabulary that
      does not transfer — the enrollment broker's KEY-name check produced 68
      false positives against legitimate credential-NAMING fields, so only the
      VALUE-shape checks were carried forward, matching the ratified
      requirement's own VALUE-scoped wording.
- [x] 7.2 Every §4 consumer re-pin is MERGED and green in its own repository —
      not authored, merged.
      **Recorded 2026-09-08 — MET; ticks on the evidence, and every merge state
      below was re-read with `gh pr view` on 2026-09-08 rather than copied from
      the § 4 notes.**
      *Merged, all five acts.* 4.1 + 4.2 (the aggregation `.gitmodules` sibling
      and the four workflow comments) — opensoft/xFactory#268, MERGED, squash
      `2f767ac8`, 2026-09-05T19:53:48Z. 4.3 (OpsxFactory's closed code-surface
      vocabulary) — opensoft/OpsxFactory#228, MERGED, merge commit `6a0d9467`,
      2026-09-05T19:53:58Z, landed AFTER #268 on purpose so the registry arm
      re-derives against a `.gitmodules` that already carries the pin. 4.4 + 4.7
      (the CloudPC-Install `OMNIWORKER_ROOT` seam and the five docs) —
      opensoft/CloudPC-Install#17, MERGED, squash `bba9da8a`,
      2026-09-05T19:54:04Z.
      *Two boxes discharged WITHOUT an edit, called out rather than counted
      silently* — "merged and green" cannot honestly be claimed of an act that
      correctly did nothing. 4.5 (openxFactory references) was discharged BY
      MEASUREMENT: zero references to worker/host material paths exist under
      `contracts/` or `openspec/specs/`, so nothing was in scope and nothing
      changed. 4.6 (the NotebookLM projection) was discharged BY FINDING:
      `installs/*` repositories are out of scope for the ideation-book
      projection by design, so no book is owed and the sync was not run.
      *Green — and where the greenness actually lives, measured per repository
      rather than assumed uniform.* opensoft/xFactory#268 shows four successful
      checks at its head `b161eea0` (`lane-line`, `merge-master-approval`,
      `validate`, SonarCloud). opensoft/OpsxFactory#228 and
      opensoft/CloudPC-Install#17 show ONE check run each at their heads
      (`95ef9d97`, `9675e3dc`) — `copilot-pull-request-reviewer`, success — and
      no validation check ran on either head, so their greenness rests on the
      proofs recorded in their own pull requests: for #228, the simulated
      workspace in which the registry arm read "21 declared, 21 present, exact
      match" after #268 and a finding before it; for #17, the three-run proof in
      which the discharging run does NOT skip (31 checks, 0 failures, 0 skips).
      *The consumer that had to stay green through all of it is
      `Omnigent-Install`*, which reads the moved tree through
      `contracts/omniworker-install-pin.yaml`: green across the whole
      twelve-group realization, its archive (opensoft/Omnigent-Install#237 →
      `07bdc9c3`) and the routine re-pin that followed
      (opensoft/Omnigent-Install#246 → `16963099`).
- [x] 7.3 §6 retirement is merged and the post-retirement re-run (6.3) is green.
      **Recorded 2026-09-08 — MET ON THE RETIREMENT HALF, SUCCESSOR-NAMED ON
      THE RE-RUN HALF, and the two are not conflated.**
      *Retirement merged, in full.* Part 1 — opensoft/Omnigent-Install#235
      `bbba916d` (2026-09-07T12:12:15Z). Part 2 —
      opensoft/Omnigent-Install#213 → merge commit `9c9c9355`
      (2026-09-08T13:05:48Z), on Brett Heap's word "merge 213". § 6.2's README
      scope edit landed inside #235. § 6 is therefore merged in full, and § 6.1
      above carries the OQ-6 supersession this required.
      *The post-retirement re-run is NOT green, because it has not run — and
      this box does not claim otherwise.* § 6.3's own text sequences it after
      Part 2, which landed today, so no run could precede it; measured
      2026-09-08 there is no post-retirement run of any of the four lanes and
      none in CloudPC-Install since 2026-09-05. The obligation closes on the two
      NAMED successors § 6.3 records — **opensoft/xFactory#346** (the four moved
      worker lanes) and **opensoft/CloudPC-Install#19** (the service-rider
      selftests), both unclaimed — under Brett Heap's "Tick on the recording"
      ruling of 2026-09-06. What this box asserts is that the retirement is
      merged and that the proof obligation the re-run carries is owed to two
      dated issues rather than to nobody.
- [x] 7.4 `docs/omniworker-naming.md` reads `Status: ratified`.
      **Recorded 2026-09-08 — MET; ticks on the evidence.** Verified by reading
      the file at `main` `9581ed9b`: line 3 is `Status: ratified`, line 4 is
      `Ratified by: implement-omniworker-install-repo`. It has read that since
      the file first existed, at this change's landing squash `76434aac` (task
      1.2), and the two 2026-09-08 amendment passes
      (opensoft/openxFactory#784 → `6c9e3627`, #789 → `9581ed9b`) left both
      lines untouched — A1's own header says so: *"`Status: ratified` and
      `Ratified by:` above are unchanged."*
- [x] 7.5 OQ-1 through OQ-10 are each ruled and recorded, or explicitly
      deferred with the deferral naming who holds it.
      **Recorded 2026-09-08 — MET, and it is the same record as task 1.3's:
      read that box's ten bullets, which are not repeated here.** The count
      against this box's own two exits: **THREE ruled and recorded** (OQ-6 and
      OQ-7 by Brett Heap 2026-09-05, both carried as dated `design.md` § D5
      amendments and ratified on opensoft/openxFactory#704; OQ-10 settled at the
      creation act and verified live), **FOUR answered by the act with the
      settling artefact cited** (OQ-2, OQ-3, OQ-4, OQ-8), and **THREE
      explicitly deferred, each naming its holder and its issue** — OQ-1
      (opensoft/openxFactory#794, holder Brett Heap), OQ-5
      (opensoft/openxFactory#795, holder Brett Heap, also § 8.3's successor) and
      OQ-9 (opensoft/openxFactory#796, unclaimed, also § 8.4's successor). No OQ
      is left silent, and no OQ is recorded as ruled that was not.
- [x] 7.6 **Do not archive before then.** `release-realization` gates a change
      with a code surface on merged plus green realization evidence; this
      change's code surface spans five repositories and two of them are
      operator estates.
      **Recorded 2026-09-08 — THE GATE IS MET AND THIS IS THE SUMMARY IT TICKS
      ON.** `target_release: repository-bootstrap`, on the archived
      `add-xfactory-installer-repository` (2026-07-10) and
      `admit-install-repos-to-aggregation` (2026-08-25) precedents for a
      repository-creation act: **no contract bundle is cut, no contract schema
      moves, no version is allocated or reserved**, and realization lands on the
      new repository's own `main` plus one pull request per consumer. The code
      surface is NON-EMPTY, so this packet archives on **merged-plus-green
      realization evidence, never on landing** — and the evidence, per
      repository:
      1. **opensoft/OmniWorker-Install** — created, seeded, suites and boundary
         validator proved at the new location; six merged pull requests, `main`
         tip `187d75b6` (§ 7.1).
      2. **opensoft/Omnigent-Install** — the pin realized across twelve groups
         and archived (#214 `544c6319` → … → #237 `07bdc9c3`), re-pinned
         routinely (#246 `16963099`), Part 1 retired (#235 `bbba916d`) and
         Part 2 recorded at § 6.1 / § 7.3 below.
      3. **opensoft/xFactory** — the sibling submodule and the four workflow
         comments (#268 `2f767ac8`, four checks green) and the governed
         aggregation admission record (#274 `648c8bd3`, § 8.1).
      4. **opensoft/OpsxFactory** — the code-surface registry entry (#228
         `6a0d9467`) and the fleet re-attestation with the new Entra device id
         (#233 `83a91c58`, ratified #235 `3e4cd248`, § 8.2).
      5. **opensoft/CloudPC-Install** — the `OMNIWORKER_ROOT` seam and the five
         docs (#17 `bba9da8a`), and the fleet-identity correction (#18
         `349d539d`).
      **What the gate does NOT claim, stated here rather than left to be
      discovered.** Two operator-estate acts are closed on NAMED SUCCESSORS and
      not on evidence — the post-retirement re-run (§ 6.3 →
      opensoft/xFactory#346, opensoft/CloudPC-Install#19) and the runner-label
      ruling (§ 8.3 → opensoft/openxFactory#795) — and one ratified clause was
      DISPOSED rather than discharged (§ 5.2's immediately-pre-act emptiness
      confirmation, which can no longer be evidenced; § 5's amendment header
      records exactly what that leaves unsatisfied). None of the three is a
      code-surface gap: every byte this packet's `code_surface:` declares is
      merged and green.

## 8. Named follow-ups — NOT this change

- [x] 8.1 **Aggregation admission record.** A dedicated reviewed change
      recording path, remote, visibility, exact validated commit, checkout,
      compatibility, update and rollback for `installs/omniworker-install`.
      The ADDED requirement's own scenario says this change MUST NOT be
      accepted as that record. §4.1's gitlink is the mechanical pin, not the
      governed admission.
      **Recorded 2026-09-08 — PERFORMED; ticks on the evidence.**
      opensoft/xFactory#274, *"Record the governed aggregation admission for
      installs/omniworker-install (tasks § 8.1)"* → squash `648c8bd3`
      (2026-09-05T23:26:48Z, four checks green). It lands
      `docs/2026-09-05-omniworker-install-admission-record.md` carrying the
      EIGHT fields under the eight labels the ratified requirement enumerates,
      on the shape the archived `admit-install-repos-to-aggregation`
      (2026-08-25) set for `Keycloak-Install` and `OpenXPKI-Install` under the
      identically worded clause. **It is a SEPARATE act from the pin, which is
      what the requirement demands**: #274's own body quotes the scenario
      (*"the repository's own creation change MUST NOT be accepted as that
      record"*), and it moves no gitlink and changes no pin — #268 `2f767ac8`
      did that, and task 4.1 calls that "the mechanical pin, not the governed
      admission".
- [x] 8.2 **OpsxFactory fleet re-attestation** with the new Entra device id
      (§5.4). Its own change, against the registration record.
      **Recorded 2026-09-08 — PERFORMED; ticks on the evidence, and this is the
      same act § 5.4 already records.** `reattest-omni001-fleet-registration`
      landed as opensoft/OpsxFactory#233 → merge commit `83a91c58`
      (2026-09-06T01:18:40Z): `registered_endpoints[0]` rebound from Entra
      device `08829330-2098-461c-a950-0047e163f2b1` / `CPC-Omni0-P5AJB` to
      `cf287ce7-7f73-4da7-adfb-c501bd7dd670` / `Omni001-XEAON`, the retired id
      kept as dated history, and the digest `ece6d6c7…` pinned into
      `workflows/endpoint-management.yaml` in the same commit. Ratified by
      opensoft/OpsxFactory#235 → merge commit `3e4cd248`
      (2026-09-06T03:55:22Z), `opsx-validation` SUCCESS.
      *It is its own change against the registration record, which is what this
      box asked for* — OpsxFactory's own rule is that a bound value moves by a
      new OpenSpec change and never by an in-place edit, and #233 was
      deliberately opened as a DRAFT because merging it IS the re-attestation,
      an act only Brett Heap can perform.
      *One measured caveat, recorded rather than smoothed over.* #233's
      `opsx-validation` check reads **failure** at its head `0df91a37`. Read at
      2026-09-08, the failure is the end-of-run freshness gate refusing to speak
      for the wrong commit — verbatim: *"merge_sha: captured
      '5cd31ff8…', current '83a91c58…'. The pull request moved under the run"* —
      i.e. the pull request MERGED while its own run was in flight, so the run
      had validated a now-stale test-merge commit. It is a staleness refusal
      about WHICH commit the result speaks for, not a finding against the
      registration record; the ratification #235, on the same record, is
      `opsx-validation` SUCCESS.
- [x] 8.3 **The runner-label question (OQ-5).** If `omnigent` becomes
      `omniworker` on the runners, that is a coordinated runner
      re-registration plus a sweep of at least seven xFactory lanes, with a
      window in which no lane can dispatch. Its own change, and not a
      side effect of this one.
      **Recorded 2026-09-08 — SUCCESSOR NAMED, holder Brett Heap:
      opensoft/openxFactory#795**, filed at this archive and UNCLAIMED. Ticks
      on the recording under Brett Heap's ruling of 2026-09-06, verbatim "Tick
      on the recording"; **nothing has been done to any runner label and this
      note claims nothing has.**
      The issue carries the three exits the packet put (change it, keep it, or
      add `omniworker` as a second label and retire `omnigent` later — the
      packet's recommendation, because a runner may hold both), the ratified
      naming record's three casings, and the measurement that makes the ruling
      cheap: **nothing in the aggregation SELECTS on the label** — all ten
      self-hosted xFactory lanes dispatch by runner GROUP plus a per-host or
      per-lane label. It also carries the correction that measurement went
      through: the earlier claim that the label was *"selected on by at least
      seven lanes"* was WRONG, inferred from runbook label lists rather than
      read off the workflows, and corrected on opensoft/openxFactory#591
      (2026-09-05T14:57Z) — in the direction that makes the act cheaper, so the
      cost is a runner re-registration plus a doc sweep and **no lane loses its
      dispatch path** while it happens. The sentence in this box's ratified text
      about *"a sweep of at least seven xFactory lanes"* is the claim that
      correction narrows.
- [x] 8.4 **The older openxFactory enumerations (OQ-9)** —
      `shared-contract-ownership`, `canonical-contract-migration`, and this
      capability's own "Install repository scope" — become incomplete when a
      fifth install repository exists. Refreshed in a follow-on, on the
      `implement-keycloak-install-repo` precedent that left the enumeration
      alone rather than colliding with the change that owned it.
      **Recorded 2026-09-08 — SUCCESSOR NAMED: opensoft/openxFactory#796**,
      filed at this archive and UNCLAIMED. Ticks on the recording under Brett
      Heap's ruling of 2026-09-06, verbatim "Tick on the recording"; **no
      enumeration has been widened and this note claims none has.** The fifth
      install repository now exists (created 2026-09-05, admitted by
      opensoft/xFactory#274 `648c8bd3`), so all three enumerations are
      incomplete as this box predicted.
      The issue records the collision the refresh must check for BEFORE it is
      authored, measured 2026-09-08 at `main` `9581ed9b`: both
      `implement-keycloak-install-repo` and `implement-openxpki-install-repo`
      are **STILL ACTIVE** in this repository, so a change that MODIFIES
      *"Install repository scope"* may collide with whichever of them archives
      first — which is exactly the reason this packet added a SIBLING
      requirement instead of widening a shared one. It also puts the authoring
      question the box's own wording leaves open: widen the three hand-written
      lists, or stop enumerating and derive the list (the aggregation
      `.gitmodules`, which OpsxFactory's `code_surface_repository_registry`
      already re-derives), so the sixth repository does not reopen this box.
- [x] 8.5 **The `Omnigent-Install` scope-link half.** §6.2 performs it as part
      of retirement; if retirement is deferred, the scope link is still owed
      the moment the new repository exists, because "Install repo scope links"
      binds both repositories and not only the new one.
      **Recorded 2026-09-08 — PERFORMED; ticks on the evidence, and the evidence
      is the live file rather than a pull request's promise.** Read at
      `opensoft/Omnigent-Install@main` on 2026-09-08, that repository's
      `README.md` carries BOTH halves this box binds: the four scope items are
      gone from its scope list, and in their place a paragraph names
      `opensoft/OmniWorker-Install` as owning "worker-host install, operations
      and disaster recovery", links it, and quotes Brett Heap's boundary ruling
      of 2026-09-05 — with the doc index carrying the same link for the three
      moved docs. That is the scope link the ratified "Install repo scope links"
      requirement demands of BOTH repositories; openxFactory's own half has been
      in place since the packet landed.
      *Which act performed it, stated precisely because this box's own wording
      guesses differently.* § 6.2's, in opensoft/Omnigent-Install#235
      `bbba916d` (2026-09-07T12:12:15Z) — **not** the Part 2 retirement. So the
      contingency this box was written for ("if retirement is deferred, the
      scope link is still owed the moment the new repository exists") never had
      to fire: the link landed with Part 1, a day before
      opensoft/Omnigent-Install#213 → `9c9c9355` completed the retirement.

**Amended 2026-09-07 — one further follow-up is NAMED here and is NOT performed
by the § 5 amendment, because it falls outside what that amendment was approved
to touch.** `docs/omniworker-naming.md` — the ratified canonical naming record
this packet authored — still declares the machine-name template
`CPC-OXF-%USERNAME:7%`, still renders `CPC-OXF-Omni001` as the worked example,
still reasons explicitly from the template carrying — in that record's own
words — **no `%RAND%` segment**, which is the premise Windows 365 refuses: it
refuses by requiring the specific token `%RAND:5%` in every device-name
template, not merely some random segment of any length. It still reads
`Amendments: None`. openxFactory's
own `README.md` repeats the template in its doc-index line and in its records
block. An operator following the canonical record is therefore still instructed
to configure a template that cannot be applied. **Owed: a dated amendment
appended to `docs/omniworker-naming.md`'s Amendments section recording the
mandatory `%RAND:5%` constraint, the applied template `%USERNAME:7%-%RAND:5%`,
the rendered name `Omni001-XEAON`, and Brett Heap's "Accept Omni001-XEAON"
ruling — plus the two `README.md` references — as its own reviewed act on
Brett's word.** Raised as a Codex P2 on opensoft/openxFactory#773 ("Amend the
canonical machine-naming record"); the finding is accepted as correct and is
recorded here rather than performed, because the § 5 amendment's approval
covers this packet's own § 5 dispositions and neither a ratified `docs/` record
nor the README substrate.

[Narrowed 2026-09-08 by `docs/omniworker-naming.md` A1
(opensoft/openxFactory#784 → squash `6c9e3627`): the sentence above, "it
refuses by requiring the specific token `%RAND:5%` in every device-name
template, not merely some random segment of any length", overstates what was
measured. A template with no random segment at all is rejected (the
established premise); beyond that, `%RAND:2%` was rejected as too short and
`%RAND:5%` was accepted — lengths 3, 4, and above 5 were never tested, so
`%RAND:5%` is the only width established as accepted: neither an exact-token
requirement nor any alternative accepted width is established by the
evidence.]

**Amended 2026-09-08 — DISCHARGED; box closed.** Recorded 2026-09-08: landed
as opensoft/openxFactory#784 → squash `6c9e3627` (05:51:36Z),
`docs/omniworker-naming.md` Amendment A1 + README entries; on Brett Heap's
word 2026-09-08T03:23Z "archive add-manifests-root-parameter and fix the
naming record." A1 also narrowed the exact-token phrasing this owed item
itself carried above (`%RAND:5%` as the only width established as accepted —
lengths 3, 4, and above 5 were never tested, so neither a minimum nor any
alternative accepted width is established) — see the bracketed note
immediately above and the
matching note at `proposal.md`'s § "Origin" (after the ruled-template
paragraph). Raised on opensoft/openxFactory#784 ("Propagate the narrowing
into the authoritative packet") by chatgpt-codex-connector; declined to
perform inside #784 as outside that act's authority, named there as owed to
this packet, and performed here.
