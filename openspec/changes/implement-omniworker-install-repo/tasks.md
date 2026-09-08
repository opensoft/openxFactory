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

## 1. Naming ratification and boundary (openxFactory; this change's own PR)

- [x] 1.1 Ratify this packet. Brett Heap's word on the PR or on the governing
      issue; the packet is `Status: draft` until then, and the four rulings it
      quotes (name, scope, template, reprovision) are the authority for those
      four facts only — not for the boundary, the split table, or the
      choreography, which are this packet's proposals.
      Recorded 2026-09-05: Brett Heap, "ratify 680 and merge 16", on PR #680 at head
      `91866619`; proposal `Status: ratified` + `Ratified:` line; naming record `Status: ratified`.
- [ ] 1.2 On landing, flip `docs/omniworker-naming.md` from `Status: draft` to
      `Status: ratified`. `Ratified by: implement-omniworker-install-repo`
      already names this change; the lifecycle ratification IS this change
      landing, on the `docs/openxdox-naming.md` precedent.
- [ ] 1.3 Answer OQ-1 through OQ-10 (design § D6). Each answer is recorded as a
      dated amendment to this tasks file or to `design.md`, naming Brett's
      words, before the task it gates runs. **OQ-7 (the in-flight change) and
      OQ-10 (visibility) gate §2 and §3 and cannot be deferred past them.**

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
- [~] 2.3 Install the governance plumbing AT CREATION, not later — the `main`
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

- [ ] 6.1 Delete the §3.1 and §3.2 paths from `Omnigent-Install`, in ONE
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
- [x] 6.2 Update the `Omnigent-Install` README's scope list — remove "Cloud PC
      worker host registration", "worker containers and worker lane setup",
      "native Claude Code / Codex harness setup", "subsystem-specific worker
      profiles and prompt packs" — and add the scope link to
      `OmniWorker-Install` that the "Install repo scope links" requirement
      demands of both sides.
      Recorded 2026-09-07: done in opensoft/Omnigent-Install#235 `bbba916d`
      (README scope + doc index; `workers/`/`rendered/` gone).
- [ ] 6.3 Re-run the four moved xFactory lanes and the CloudPC-Install
      selftests after retirement, to prove nothing was reaching the old paths
      unmeasured.
      Runs after 6.1 Part 2 closes.

## 7. Archive conditions

- [ ] 7.1 `opensoft/OmniWorker-Install` exists, is seeded, its harnesses are
      green on its own `main`, and its boundary validator refuses a planted
      credential.
- [ ] 7.2 Every §4 consumer re-pin is MERGED and green in its own repository —
      not authored, merged.
- [ ] 7.3 §6 retirement is merged and the post-retirement re-run (6.3) is green.
- [ ] 7.4 `docs/omniworker-naming.md` reads `Status: ratified`.
- [ ] 7.5 OQ-1 through OQ-10 are each ruled and recorded, or explicitly
      deferred with the deferral naming who holds it.
- [ ] 7.6 **Do not archive before then.** `release-realization` gates a change
      with a code surface on merged plus green realization evidence; this
      change's code surface spans five repositories and two of them are
      operator estates.

## 8. Named follow-ups — NOT this change

- [ ] 8.1 **Aggregation admission record.** A dedicated reviewed change
      recording path, remote, visibility, exact validated commit, checkout,
      compatibility, update and rollback for `installs/omniworker-install`.
      The ADDED requirement's own scenario says this change MUST NOT be
      accepted as that record. §4.1's gitlink is the mechanical pin, not the
      governed admission.
- [ ] 8.2 **OpsxFactory fleet re-attestation** with the new Entra device id
      (§5.4). Its own change, against the registration record.
- [ ] 8.3 **The runner-label question (OQ-5).** If `omnigent` becomes
      `omniworker` on the runners, that is a coordinated runner
      re-registration plus a sweep of at least seven xFactory lanes, with a
      window in which no lane can dispatch. Its own change, and not a
      side effect of this one.
- [ ] 8.4 **The older openxFactory enumerations (OQ-9)** —
      `shared-contract-ownership`, `canonical-contract-migration`, and this
      capability's own "Install repository scope" — become incomplete when a
      fifth install repository exists. Refreshed in a follow-on, on the
      `implement-keycloak-install-repo` precedent that left the enumeration
      alone rather than colliding with the change that owned it.
- [ ] 8.5 **The `Omnigent-Install` scope-link half.** §6.2 performs it as part
      of retirement; if retirement is deferred, the scope link is still owed
      the moment the new repository exists, because "Install repo scope links"
      binds both repositories and not only the new one.

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
