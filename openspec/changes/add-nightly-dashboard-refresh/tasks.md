# Tasks: add-nightly-dashboard-refresh

Dependency-ordered. Tasks marked "(HUMAN GATE)" stop for a human decision or
execution; nothing after a gate proceeds until it clears. Tasks marked
"(OMNIGENT-INSTALL)" or "(AGGREGATION)" land in that repository — this change's
realization is cross-repo, as this program's earlier lane changes were, because
the artifact-only children live in the aggregation and the receiving overlay,
the shape check and the approval envelope live in Omnigent-Install.

THE APPLY IS NOT A TASK HERE. It belongs to the already-merged companion
`add-dox-gitops-reconciliation` (Omnigent-Install `main`, `7d0370d`), whose
`dox` Flux Kustomization reconciles the merged pin. This change stops at "a
merged digest-only pin PR exists"; §6 is what UNBLOCKS the companion's task 7,
which was deliberately ordered behind this change's ruling on the lane
identity ("a grant whose subject is unresolved must not be created").

Nothing in this change may commit a credential value, place registry push
credentials in a GitHub-hosted job, grant the lane apply authority, or alter
what the served overlay renders beyond the one digest line.

## 1. Preflight — prove every assumption before writing the lane (read-only)

- [ ] 1.1 Confirm openxFactory `main` passes snapshot generation under
      `--strict` TODAY: `PYTHONPATH=scripts python3 -m
      ideation_dashboard.cli generate --repo-root . --repository openxFactory
      --strict --output <tmp>/openxFactory-snapshot.json` from a fresh `main`
      checkout. Record the error/warning counts. If `main` carries a standing
      warning, the lane can never publish — fix that FIRST, because the lane's
      gate is not negotiable and a permanently-failing gate is a silent
      no-refresh.
- [ ] 1.2 Verify the `XFACTORY_APP` installation on
      `opensoft/Omnigent-Install` with a REAL authenticated call (mint a token
      with that repository in scope and attempt a read plus a dry write path),
      not by reading a settings page: installation permissions are
      per-installation, and a missing permission fails at CALL time, not at
      mint time (the aggregation's own 403 on `actions`, live-verified
      2026-07-28, is the precedent). Record which of `contents: write`,
      `pull_requests: write` and `actions: write` the installation actually
      carries.
- [ ] 1.3 If 1.2 shows the installation cannot be extended, record the
      contingency ruling and mint a dedicated refresh-lane App instead. Only
      the `expected_author` value in §6.2's envelope entry changes; nothing
      else in this change depends on which App it is.
- [ ] 1.4 Confirm the worker host's build substrate: `cpc-omni01` docker-ce
      daemon reachable from the runner's service account, disk headroom for an
      ~8 MB context plus the image layers, and the runner
      `xfactory-artifact-cpc-omni01` online in group
      `xfactory-artifact-workers` with its `host-artifact-cpc-omni01` dispatch
      label.
- [ ] 1.5 Read the currently pinned `ideation-dashboard` digest AND its
      provenance comment from
      `deploy/kubernetes/overlays/aks-qa/kustomization.yaml` at
      Omnigent-Install `main`. This is the shape the lane's diff must reproduce,
      and it is the record the no-change check reads. Confirm and record that
      the bootstrap pin's comment is human PROSE carrying no machine-readable
      key/value provenance — so the first lane run is a bootstrap build by
      construction (§4.3), not a bug.
- [ ] 1.6 Confirm the receiving repository's required checks and its default
      branch protection, so §6's envelope entry can be written against real
      check names rather than guessed ones.

## 2. The push credential — the one genuinely new grant (OMNIGENT-INSTALL)

Blocking for §3 and everything after it. The host manifest declares `acr_pull`
only, and that schema block is `additionalProperties: false` with
`required: [registry, token_vaultref]`, so a push credential CANNOT be added as
an extra field — it needs a schema delta.

- [ ] 2.1 (HUMAN GATE) Rule the credential's shape (design Open Question 1):
      a second scoped ACR token escrowed in Key Vault, mirroring `acr_pull`'s
      v1 pattern, or the device-cert Entra credential that block's comment
      calls v2. Recommendation on record: mirror `acr_pull` for v1 and let the
      v2 migration move both together.
- [ ] 2.2 (OMNIGENT-INSTALL) Land the `schemas/worker-host-manifest.schema.yaml`
      delta for the ruled shape, and the `cpc-omni01` manifest entry using it.
      The credential MUST be push-scoped to the single `ideation-dashboard`
      image repository — not registry-wide — and declared as a `vaultref`, the
      way every other credential in that manifest is.
- [ ] 2.3 Reconcile the credential onto the host through the Worker Host App and
      verify a push by hand from the host. The worker AGENT must never fetch or
      read it: it is host substrate, reconciled onto the host, and that is the
      distinction that keeps this consistent with `access_secrets: false`.
      Confirm it is absent from the built image and from job logs.

## 3. The artifact-only child, and the recipe proven by hand (AGGREGATION)

- [ ] 3.1 Prove the fresh-checkout recipe MANUALLY on `cpc-omni01`, end to end,
      producing a real digest and opening NO pull request: scratch context
      `<ctx>`; fresh openxFactory `main` checkout at `<ctx>/openxFactory`;
      `--strict` generation from that checkout into
      `<ctx>/health/ideation-dashboard/openxFactory-snapshot.json`;
      `docker build -f <omnigent-install>/containers/ideation-dashboard/Dockerfile
      <ctx>`; date-stamped tag; push; capture digest. Record the digest, the
      `source_revision`, and the corpus revision, and assert they are the same
      commit.
- [ ] 3.2 Keep the context minimal: copy only what the Dockerfile copies. Its
      own comment accounts the governed corpus roots at ~8 MB and deliberately
      omits `experiments/` (169 MB); a whole-checkout context would ship that
      to the daemon for nothing.
- [ ] 3.3 Read the Dockerfile from Omnigent-Install `main`, not from the
      aggregation's submodule pin — the same staleness reason as the corpus —
      and record its revision as a provenance input, because a Dockerfile
      change alters the image with no corpus change and would otherwise be
      invisible in a digest-only diff.
- [ ] 3.4 Add the artifact-only child workflow `dashboard-image-worker.yml`,
      modelled on `doc-health-analysis-worker.yml`:
      `runs-on: {group: xfactory-artifact-workers, labels: <dispatch_label>}`,
      the parent-run/correlation/source-revision verification before it acts on
      any parent input, and the digest as its ONLY result artifact. It holds no
      repository write credential.
- [ ] 3.5 Confirm the child joins the existing `xfactory-artifact-worker`
      concurrency group so the singleton host is never double-booked by the
      nightly, the review lane and this lane at once.

## 4. The nightly stage (openxFactory)

- [ ] 4.1 Add the refresh stage to `.github/workflows/doc-health-reusable.yml`'s
      `finalize` job, ordered AFTER the "Commit report (deliver via rolling PR)"
      step, so the refresh can never jeopardise the report it follows.
- [ ] 4.2 Gate it with the file's existing readiness idiom — the
      `GROUP="xfactory-artifact-workers"` runner-group resolution plus the
      authenticated Hermes heartbeat, evaluated by
      `scripts/check-worker-readiness.py` — and SKIP fail-closed when unready.
      Add NO inline hosted fallback: the build and push belong to the host that
      holds the registry binding.
- [ ] 4.3 Implement the no-change short-circuit ON INPUTS, BEFORE the build
      (design Decision 10). Read the two recorded revisions out of the pinned
      image's comment block, compute the current pair, and stop with a
      `no_change` outcome — no checkout, no snapshot, no build, no push, no
      branch, no PR — when both match. Scope each side to the BAKED INPUTS, not
      the branch tip:
      `git log -1 --format=%H -- scripts/ideation_dashboard scripts/doc_health
      contracts docs examples ideation openspec templates` on openxFactory, and
      `git log -1 --format=%H -- containers/ideation-dashboard` on
      Omnigent-Install. Tip-versus-tip is WRONG and must not be shipped: the
      lane's own merged pin advances Omnigent-Install `main`, so tip comparison
      would force a rebuild every night forever. Do NOT compare the built digest
      against the pinned digest — the build is not reproducible (fresh-checkout
      mtimes move the copied layers; `FROM python:3.12-slim` floats), so that
      predicate never fires.
- [ ] 4.3a Define the provenance record's shape and make the overlay comment its
      AUTHORITATIVE home: a stable, machine-readable key/value block carrying
      both input revisions and the scoping used to compute them, written into
      the pin's comment inside the `images:` entry. It must parse
      deterministically — no prose regex-guessing. Absent or unparseable ⇒ treat
      as CHANGED (bootstrap build), never as unchanged.
- [ ] 4.4 Implement the pin-PR authoring on the fixed head branch
      `bot/dox-dashboard-pin`, using the force-free rolling-branch mechanics the
      report step already proved: org ruleset 8981805 applies
      `non_fast_forward` to `~ALL` branches with NO bypass, so deliver by branch
      CREATION (deleting a stale ref first) or by a fast-forward merge commit
      whose FIRST parent is the current remote tip. Do not rediscover this — an
      earlier revision of the report step got it wrong and "succeeded solely on
      nights the push happened to CREATE the branch."
- [ ] 4.5 Write the PR body provenance — the two input revisions, snapshot
      `source_revision`, pushed tag, new and previous digests,
      strict-validation counts, and the run URL — and mark it explicitly as a
      COURTESY restatement: the record the lane reads is the overlay comment
      (4.3a), never the PR body. Assert no label, title prefix or
      commit-message convention is used to CLAIM the diff shape — the receiving
      repository adjudicates it.
- [ ] 4.6 Confirm the produced diff is exactly the `digest:` line plus its
      adjacent provenance comment on the `ideation-dashboard` entry, and touches
      no other line, block or file. Keep the human-readable facts the existing
      comment carries (see 1.5) and add the 4.3a key/value block beside them —
      the comment must serve both a reader and the parser.
- [ ] 4.7 Write `health/ideation-dashboard/refresh-status.json` beside the
      existing `lane-status.json`, following `nightly_lane.py`'s status idiom
      (diagnostic, not a projection; its own failure must never take the run
      down). Fields: result (`ok` / `no_change` / `skipped` / `strict_failed`),
      reason, bounded detail, the two input revisions each beside the recorded
      revision compared against, `source_revision`, built and pinned digests
      (when a build occurred), tag, PR reference, `generated_at`, `run_id`. A
      `no_change` outcome MUST name the revisions that matched, so "nothing
      moved" is auditable rather than asserted.
- [ ] 4.8 (HUMAN GATE) Resolve the reporting-lag choice (design Open Question 3):
      accept the one-run lag and have the report SAY which run's outcome it
      names, or add a second narrowly-scoped delivery for the status artifact
      after the stage. Record the choice.
- [ ] 4.9 Add the report section for the refresh outcome, and the stuck-chain
      signal: a `bot/dox-dashboard-pin` PR still open at the next run is
      reported, naming it.
- [ ] 4.10 Emit `::notice::` / `::warning::` annotations for every outcome so a
      skip is never silent in the run itself, whatever the artifact-delivery
      lag turns out to be.

## 5. Tests (openxFactory)

- [ ] 5.1 Tests under `tests/ideation-dashboard/` for the refresh status
      artifact: every outcome class, the bounded detail, and the invariant that
      a status-write failure does not fail the lane.
- [ ] 5.2 Tests for the no-change short-circuit, pinning the ORDERING and not
      just the outcome: (a) same-input night ⇒ the lane stops BEFORE the docker
      build — assert structurally that no checkout, no snapshot generation, no
      build and no push were invoked, not merely that no PR was opened, because
      an outcome-only assertion passes even if the build ran; (b) a pin whose
      provenance is absent or unparseable ⇒ the lane BUILDS (bootstrap), and the
      pin it produces carries a parseable record; (c) recipe moved / corpus
      static ⇒ builds; (d) an unrelated commit on the served plane's repository,
      including a simulated previously-merged pin, ⇒ does NOT rebuild, which is
      the guard against a tip-versus-tip regression.
- [ ] 5.2a A round-trip test over the REAL overlay file: the provenance block the
      lane writes is parsed back to the same two revisions, and the surrounding
      human prose is preserved. This is the guard on the one comment that is now
      load-bearing state.
- [ ] 5.3 A test that the produced diff is envelope-shaped: exactly the digest
      line and its adjacent comment in the `images:` block of the one overlay
      file, over a fixture of the real file. This is the guard that keeps a
      future edit from quietly widening what the lane can produce.
- [ ] 5.4 A test that the snapshot `source_revision` and the recorded corpus
      revision are asserted EQUAL by the lane, so the two-revision trap is
      detectable rather than merely avoidable.
- [ ] 5.5 Run the full suites and report the real exit status. Do not pipe the
      run through `tail` or any filter that can mask a failure.

## 6. The receiving side — shape check and approval (OMNIGENT-INSTALL)

This is the companion's task 7, unblocked by rulings (a) and (b). Ordered after
§4 so the identity the grant names is real.

- [ ] 6.1 Implement the repository-side shape check as a REQUIRED status check
      over the ACTUAL diff: exactly one file
      (`deploy/kubernetes/overlays/aks-qa/kustomization.yaml`), every changed
      line a `digest:` value or a comment inside the `images:` block, no image
      entry added or removed, no `name:`/`newTag:` change, no change to
      `resources:`, `patches:`, `namespace:` or the header. It MUST ignore
      everything the author asserts — label, title, commit message: identity is
      an input to the predicate, never the verdict.
- [ ] 6.2 Install the merge-master App on Omnigent-Install, add the
      `merge-master-approval` workflow and an envelope INSTANCE with ONE
      candidate class: `target_repos: [opensoft/Omnigent-Install]`,
      `expected_author` = the §1.2/§1.3 App's bot login,
      `expected_head_ref: bot/dox-dashboard-pin`, `expected_base_ref: main`,
      `path_allowlist: [deploy/kubernetes/overlays/aks-qa/kustomization.yaml]`,
      `require_all_checks: true`,
      `check_exclusions: [merge-master-approval]`, `revert_suffices: true`.
      Set the `MERGE_MASTER_APP_ID` / `MERGE_MASTER_APP_KEY` bindings.
- [ ] 6.3 Keep the base-branch security properties intact: the envelope config
      AND the workflow definition are read from the BASE branch, no PR-head
      content is checked out or executed, the approving identity is distinct
      from the authoring identity, and the envelope file's own path sits outside
      every `path_allowlist` so a PR editing the rules can never be
      autonomously approved. Pin the shared decision core by SHA, as the
      aggregation does, rather than tracking a moving branch.
- [ ] 6.4 (HUMAN GATE) Choose the approval trigger (design Open Question 2):
      in-repo `workflow_run` on the shape check's completion — recommended,
      base-branch semantics preserved, no extra App permission — or the
      cross-repo `gh workflow run` chain, which needs `actions: write` on the
      App's installation here. Either way the trigger is NON-FATAL: a failed
      trigger parks the PR for the human gate and never fails the nightly.
- [ ] 6.5 Verify the parked path and the revocation path: a wider diff from the
      SAME identity is refused by 6.1 and waits for human review; deleting the
      candidate entry (or unsetting the approver binding) returns every PR
      against that file to human review with no code change and no redeploy.
      Restore afterwards.

## 7. End-to-end proof (HUMAN GATE)

- [ ] 7.1 (HUMAN GATE) Enable PR authoring and watch ONE real nightly cycle end
      to end: worker builds and pushes; the App opens the digest-only pin PR;
      the shape check passes; merge-master approves inside the envelope; GitHub
      auto-merge lands it; the companion's `dox` Kustomization reconciles; the
      `dox-dashboard` Deployment rolls onto the new digest.
- [ ] 7.2 Verify the served result, not just the pipeline: the freshness header
      names the new `source_revision`, and a document that landed on `main`
      since the PREVIOUS image resolves through `/source` — the check that
      actually proves the corpus was rebaked and not just the snapshot.
- [ ] 7.3 Prove the negative direction: a deliberately wider diff from the same
      lane identity is refused by the shape check and parks for human review,
      with no approval submitted.
- [ ] 7.4 Prove the no-change night ON A LIVE RUN, and prove it at the right
      point: a cycle with no input movement stops BEFORE the build — the run's
      own log shows no checkout, no snapshot generation, no docker build and no
      ACR push — and produces zero PRs and zero deploys, reporting `no_change`
      rather than a failure. Then prove the sequence that matters most: the
      night AFTER a landed pin, with no further corpus movement, must ALSO be
      `no_change`. That is the regression the old digest predicate would have
      failed, and a single quiet night does not demonstrate it.
- [ ] 7.5 Prove the skip: with the worker offline or its heartbeat stale, the
      lane records a skip, the nightly completes, the report is unaffected, and
      the next cycle catches up in one hop.
- [ ] 7.6 Record the staleness bound actually observed (generation to served
      rollout) against the design's ~24 h + one reconcile interval + one
      rollout, and state it wherever the served plane is documented, as the
      MODIFIED requirement demands.

## 8. Docs and close

- [ ] 8.1 Add this change to the openxFactory README "OpenSpec Records" block,
      in that list's existing format.
- [ ] 8.2 Record the conformance gap explicitly where the served plane is
      documented: the hosted image today passes only `--snapshot` and
      `--checkout-root` and performs no runtime fetch, so its baked artifacts
      ARE its data and this lane's cadence IS its data cadence. Name the rebake
      bound as the mitigation, and do NOT present it as the intended design.
- [ ] 8.3 Confirm `OPENSPEC_TELEMETRY=0 openspec validate
      add-nightly-dashboard-refresh --strict` and `--all --strict` are clean.
- [ ] 8.4 Notify the companion `add-dox-gitops-reconciliation` that legs 1–2 are
      live and its Open Questions are closed: the mechanism is Merge Master
      extended with a second candidate class (ruling a), the lane identity is
      the existing `XFACTORY_APP` on the fixed head branch
      `bot/dox-dashboard-pin` (ruling b), and this lane claims no apply
      capability of its own. Its task 8.3 is the counterpart of this one.
- [ ] 8.5 Archive per the `target_release` gate: `implementation_pending`, and
      the evidence is §7's real cycle in BOTH directions. A lane proven only by
      a dry run does not close this change.
