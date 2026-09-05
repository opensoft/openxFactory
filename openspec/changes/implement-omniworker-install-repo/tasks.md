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

- [ ] 2.1 Create `opensoft/OmniWorker-Install`. **Visibility per OQ-10**
      (private to match `Keycloak-Install` / `OpenXPKI-Install` unless ruled
      otherwise), default branch `main`, description naming it the worker-host
      install repository for the xFactory fleet. Name spelled exactly
      `OmniWorker-Install` — capitalized on the `<Name>-Install` house form
      that `CloudPC-Install`, `Keycloak-Install` and `OpenXPKI-Install` already
      set, and that OpsxFactory's closed code-surface vocabulary checks against.
- [ ] 2.2 Independently released, like its siblings: its own `main`, its own
      release line, its own validation. It is NOT a subtree of, and not
      released with, `Omnigent-Install`.
- [ ] 2.3 Install the governance plumbing AT CREATION, not later — the `main`
      ruleset requiring one approving review, the repository added to the
      `openxfactory` GitHub App installation so the content App can author
      PRs, the App secrets, and the `session-open-pr.yml` mirror. The
      authorship route works on day one or the first PR is authored by the
      only human who can approve it (the `implement-keycloak-install-repo`
      lesson, learned there).
- [ ] 2.4 Seed the README with the ownership boundary quoted VERBATIM from the
      ratified requirement — `openxFactory` owns factory workflow policy;
      `OmniWorker-Install` owns worker-host install, operations, and DR;
      `Omnigent-Install` remains the orchestrator. Quoted, never paraphrased:
      the "Install repo scope links" requirement wants the link, and the
      Keycloak-Install README is the worked example of quoting rather than
      restating.
- [ ] 2.5 Pin the compatible openxFactory contract bundle tag plus exact
      contract commit and per-file digests for the neutral contracts the host
      consumes, on the `pinned_contract_manifest` shape.

## 3. Copy-first migration (design § D2, § D3 step 2)

**Copy. Do not move.** Nothing is deleted from `Omnigent-Install` in this
group; §6 is where deletion lives, and only after §4 and §5.

- [ ] 3.1 Copy the RULED tree: `hostapp/`, `workers/`,
      `clients/opensoft/worker-hosts/`, `scripts/publish_artifact_worker_heartbeat.py`,
      `docs/runbooks/cloudpc-named-worker-licensing.md`,
      `docs/runbooks/cloudpc-worker-pack.md`,
      `docs/runbooks/doc-health-cloudpc-pilot.md` (with its correction banner
      intact), `docs/worker-deployment-phases.md`.
- [ ] 3.2 Copy the JUDGED tree, each item re-checked against its content at
      copy time and any disagreement raised rather than carried:
      `docs/credential-auth-profiles.md`, the three llm-credential runbooks,
      `docs/worker-hosts.md`, `schemas/worker-host-manifest.schema.yaml`
      (placement per OQ-4), `evidence/worker-host-manifest/`,
      `rendered/effective-profiles/`, the twenty-one host-side `scripts/`, and
      the eight host-side `tests/` including the `pwsh_host.py` harness.
- [ ] 3.3 Re-home `openspec/changes/add-worker-enrollment-broker-integration/`
      by the sequence OQ-7 rules — **(a)** land PR #40 in `Omnigent-Install`
      first and copy the post-merge tree, or **(b)** re-target the change and
      re-open its PR against `OmniWorker-Install` with an amendment to its
      `code_surface:` declaration. Not by default and not by side effect.
- [ ] 3.4 Prove the copied harnesses GREEN in the new repository before
      anything else depends on them: the PowerShell host-app and deploy
      suites, `test_worker_host_manifest.py`,
      `test_publish_artifact_worker_heartbeat.py`,
      `test_rider_heartbeat_contract.py`, `test_worker_auth_bootstrap.py`,
      `test_artifact_lane_contract.py`. The ratified copy-first requirement's
      second scenario makes this the gate, not a courtesy.
- [ ] 3.5 Add the repository's own boundary validator refusing a committed
      credential value — model-provider credential, runner registration token,
      enrollment lease secret, Key Vault secret value, host service-account
      password — reusing the detection classes the estate's existing
      secret-scanners already established rather than inventing a second
      vocabulary for "this is a secret".

## 4. Consumer re-pins — EACH ITS OWN PR, in its own repository

- [ ] 4.1 **xFactory `.gitmodules`** gains `installs/omniworker-install` →
      `git@github.com:opensoft/OmniWorker-Install.git` as a SIBLING entry.
      `installs/omnigent-install` is not renamed and not removed. Records the
      exact validated commit; the governed admission record is §8.1, not this.
- [ ] 4.2 **xFactory workflow comments** — `doc-health-cataloger-worker.yml`,
      `doc-health-readiness-worker.yml`,
      `doc-health-derive-possibles-worker.yml`,
      `ideation-organizer-worker.yml` — re-point the four
      `installs/omnigent-install/workers/profiles/*.yaml` references. Comments,
      not checkouts (design § D4 measured it): a comment naming a path nothing
      contains is worse than no comment.
- [ ] 4.3 **OpsxFactory `models/code-surface-repositories.yaml`** gains one
      entry `- id: OmniWorker-Install / source: aggregation_submodule`, in the
      alphabetical block. **Depends on 4.1**: the
      `code_surface_repository_registry` validator arm re-derives an
      `aggregation_submodule` entry against the aggregation `.gitmodules`, so
      an entry landed before the pin is a finding rather than a claim.
- [ ] 4.4 **CloudPC-Install `packs/service-rider/selftest/check_heartbeat_contract.py`**
      — `OMNIGENT_ROOT` gains `OMNIWORKER_ROOT` and the sibling-directory
      candidates gain `OmniWorker-Install` / `omniworker-install`, with the
      old names kept as a deprecating fallback for one release. **Verify by a
      run that does NOT skip**: the selftest skips when the sibling is absent,
      so a green summary cannot distinguish a correct re-pin from a missing
      one.
- [ ] 4.5 **openxFactory references** to `Omnigent-Install` worker paths.
      Scoped by measurement at re-pin time; `contracts/manifest.yaml`'s nine
      `Omnigent-Install/schemas|policies/...` source paths are NOT in scope
      (those families stay with the orchestrator — design § D4).
- [ ] 4.6 **NotebookLM projection** — one ideation book per governed repo, so
      the new repository gets `xf-ideation-omniworker-install` /
      *"xFactory Ideation — OmniWorker-Install"*, added via
      `python3 openxFactory/scripts/sync-notebooklm-books.py . --apply` per
      `docs/lifecycle-notebook-projection.md`. Books resolve by TITLE; the
      capacity guard applies.
- [ ] 4.7 **The enrollment broker and CloudPC-Install docs** that name
      `omnigent-install` as the host checkout — `docs/worker-host-pack.md`,
      `docs/host-token-broker.md`, `docs/host-broker-provisioning-prompt.md`,
      `docs/doc-analysis-worker-host.md`, `README.md`. **Gated on OQ-3**: if
      the host continues to check out the orchestrator repository for its
      compose stack, most of these are CORRECT as they stand and only the
      moved-path references change.

## 5. Machine reprovision and its consequence (operator acts)

- [ ] 5.1 Set the Windows 365 provisioning policy device-name template to
      `CPC-OXF-%USERNAME:7%`. **New provisions only** — it renames nothing
      existing.
- [ ] 5.2 Reprovision omni001. It is empty: no runner registered, no pilot
      ever run. Confirm that is still true immediately before the act.
- [ ] 5.3 Read back the new Cloud PC name (`CPC-OXF-Omni001` expected) **and
      the new Entra device id**. Device `08829330-2098-461c-a950-0047e163f2b1`
      does not survive the reprovision.
- [ ] 5.4 **OWED, NOT THIS CHANGE — OpsxFactory fleet re-attestation.** The
      registration record and `workflows/endpoint-management.yaml`
      `fleet_scope.registered_endpoints` carry the old device id as the only
      endpoint in live targeting scope. Re-attest with the new id in its own
      governed change against the registration record — OpsxFactory's own rule
      is that a bound value moves by a new OpenSpec change and never by an
      in-place edit. Until it lands, live targeting names a device that does
      not exist.
- [ ] 5.5 Confirm the rendered casing. `CPC-Omni0-P5AJB` and `CPC-brett-TUBV0`
      came from the same default template but differ in case, so the exact
      rendering of `%USERNAME:7%` is an observation to make, not a prediction
      to rely on. If it renders `CPC-OXF-omni001`, that is still fifteen legal
      characters and the record gets an amendment, not a re-provision.

## 6. Retirement — the ONLY destructive step, and it is last

- [ ] 6.1 Delete the §3.1 and §3.2 paths from `Omnigent-Install`, in ONE
      reviewed PR against that repository, **only after every §4 box is
      checked and green**. Before this PR, every step is revertible by a
      single `git revert`; after it, recovery is a restore.
- [ ] 6.2 Update the `Omnigent-Install` README's scope list — remove "Cloud PC
      worker host registration", "worker containers and worker lane setup",
      "native Claude Code / Codex harness setup", "subsystem-specific worker
      profiles and prompt packs" — and add the scope link to
      `OmniWorker-Install` that the "Install repo scope links" requirement
      demands of both sides.
- [ ] 6.3 Re-run the four moved xFactory lanes and the CloudPC-Install
      selftests after retirement, to prove nothing was reaching the old paths
      unmeasured.

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
