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

- [x] 1.1 Confirm openxFactory `main` passes snapshot generation under
      `--strict` TODAY: `PYTHONPATH=scripts python3 -m
      ideation_dashboard.cli generate --repo-root . --repository openxFactory
      --strict --output <tmp>/openxFactory-snapshot.json` from a fresh `main`
      checkout. Record the error/warning counts. If `main` carries a standing
      warning, the lane can never publish — fix that FIRST, because the lane's
      gate is not negotiable and a permanently-failing gate is a silent
      no-refresh.
      > DONE 2026-08-31 against fresh `main` `3a6a16e9`: the first literal
      > fresh-checkout attempt correctly exposed that the child had made the
      > reviewed validator unreachable (`validator-unavailable`, exit 1).
      > Aggregation PR #179 fixed the checkout shape and merged as
      > `de9a1d99`; rerunning the exact sparse/blobless child shape then reported
      > `validate-ideation-dashboard-contracts: 0 error(s), 0 warning(s)`.
- [ ] 1.2 Verify the `XFACTORY_APP` installation on
      `opensoft/Omnigent-Install` with a REAL authenticated call (mint a token
      with that repository in scope and attempt a read plus a dry write path),
      not by reading a settings page: installation permissions are
      per-installation, and a missing permission fails at CALL time, not at
      mint time (the aggregation's own 403 on `actions`, live-verified
      2026-07-28, is the precedent). Record which of `contents: write`,
      `pull_requests: write` and `actions: write` the installation actually
      carries.
      > GATE OPEN (human/infra). Until the `XFACTORY_APP` installation includes
      > Omnigent-Install, the delivery step's `repos/<recipe>` probe 403s and the
      > pin PR parks fail-soft — the stage is code-complete behind this gate.
- [x] 1.3 **N/A — the contingency this task guards against is foreclosed,
      and 1.2 stays OPEN on its own separate ground.** 1.2 owes a CALL-TIME
      write proof and is deferred to §7.1; that is not the question this
      task turns on. This one asks whether the installation CANNOT be
      extended, and it demonstrably can be — it is already organization-wide
      (`repository_selection: all`), so Omnigent-Install is in scope without
      any extension act. Nothing here asserts 1.2's proof has been taken.
      If 1.2 shows the installation cannot be extended, record the
      contingency ruling and mint a dedicated refresh-lane App instead. Only
      the `expected_author` value in §6.2's envelope entry changes; nothing
      else in this change depends on which App it is.
      > NOT INVOKED. The existing `openxfactory` App installation 145372182 is
      > organization-wide (`repository_selection: all`) with `contents: write`
      > and `pull_requests: write`; Omnigent-Install is in scope. Task 1.2's
      > call-time write proof remains part of the first real delivery in 7.1.
- [ ] 1.4 Confirm the worker host's build substrate: `cpc-omni01` docker-ce
      daemon reachable from the runner's service account, disk headroom for an
      ~8 MB context plus the image layers, and the runner
      `xfactory-artifact-cpc-omni01` online in group
      `xfactory-artifact-workers` with its `host-artifact-cpc-omni01` dispatch
      label.
- [x] 1.5 Read the currently pinned `ideation-dashboard` digest AND its
      provenance comment from
      `deploy/kubernetes/overlays/aks-qa/kustomization.yaml` at
      Omnigent-Install `main`. This is the shape the lane's diff must reproduce,
      and it is the record the no-change check reads. Confirm and record that
      the bootstrap pin's comment is human PROSE carrying no machine-readable
      key/value provenance — so the first lane run is a bootstrap build by
      construction (§4.3), not a bug.
      > DONE, re-read live 2026-08-31. The current pin is
      > `sha256:ff3c65b55e713ba7f7165aa5f3b2285bcdc8d75e8cb06ee6277b0bc205d13cda`
      > and now carries `xf-refresh-provenance: v1` machine provenance from the
      > 2026-08-27 manual `gate-trust-r1` build. This is no longer a bootstrap
      > pin: current corpus baked inputs have moved, so the first live lane run
      > is still a real build by the ordinary changed-input predicate.
- [x] 1.6 Confirm the receiving repository's required checks and its default
      branch protection, so §6's envelope entry can be written against real
      check names rather than guessed ones.
      > DONE, live GitHub evidence 2026-08-31: default branch `main`; active
      > ruleset 21294850 requires `Digest-only pin scope`; recent
      > `merge-master-approval` check-suite runs are green.

## 2. The push credential — the one genuinely new grant (OMNIGENT-INSTALL)

Blocking for §3 and everything after it. The host manifest declares `acr_pull`
only, and that schema block is `additionalProperties: false` with
`required: [registry, token_vaultref]`, so a push credential CANNOT be added as
an extra field — it needs a schema delta.

- [x] 2.1 (HUMAN GATE) Rule the credential's shape (design Open Question 1):
      a second scoped ACR token escrowed in Key Vault, mirroring `acr_pull`'s
      v1 pattern, or the device-cert Entra credential that block's comment
      calls v2. Recommendation on record: mirror `acr_pull` for v1 and let the
      v2 migration move both together.
      > DONE in the ratified realization: v1 is the second scoped ACR token,
      > escrowed by Key Vault reference and limited to push+pull on repository
      > `ideation-dashboard` only.
- [x] 2.2 (OMNIGENT-INSTALL) Land the `schemas/worker-host-manifest.schema.yaml`
      delta for the ruled shape, and the `cpc-omni01` manifest entry using it.
      The credential MUST be push-scoped to the single `ideation-dashboard`
      image repository — not registry-wide — and declared as a `vaultref`, the
      way every other credential in that manifest is.
      > GATE OPEN (OMNIGENT-INSTALL infra). The `acr_push` schema delta +
      > `cpc-omni01` manifest entry are Omnigent-Install's to land; the
      > openxFactory stage assumes the host holds the push credential and never
      > reads it. This gate also blocks the §4.2 worker-profile registration.
      > DONE in Omnigent-Install PR #129 (`509b7d65`) for the governed
      > `cpc-omni01` manifest/schema shape. The rider activation being exercised
      > now is not yet host-app-converged; its equivalent scoped token is
      > escrowed as `cpc-brett01-acr-push-token`, and 2.3 stays open until that
      > credential is materialized and proved on the actual host.
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
      > AMENDED 2026-09-01, RE-RATIFIED 2026-09-04. The task body above is
      > retained as ratified 2026-08-25. Under Brett's host ruling the proof to
      > perform is: the credentialed parent materializes a fresh, bounded
      > openxFactory `main` + recipe source artifact; the worker downloads and
      > verifies it; scratch context `<ctx>`; `--strict` generation from the
      > SEALED CORPUS TREE into
      > `<ctx>/health/ideation-dashboard/openxFactory-snapshot.json`; then build,
      > tag, push and capture as above. The three recorded facts and the
      > same-commit assertion are unchanged, and the assertion is the point of
      > the task either way. STILL OPEN — this has not been run.
- [x] 3.2 Keep the context minimal: copy only what the Dockerfile copies. Its
      own comment accounts the governed corpus roots at ~8 MB and deliberately
      omits `experiments/` (169 MB); a whole-checkout context would ship that
      to the daemon for nothing.
      > DONE in aggregation `.github/workflows/dashboard-image-worker.yml`:
      > sparse/blobless checkout over `CORPUS_PATHS`, then an assembled context
      > containing only the Dockerfile COPY roots and generated snapshot.
      > AMENDED 2026-09-01: the credentialed parent now owns the sparse fresh
      > checkouts and seals only those roots plus manifest + recipe into the
      > source artifact; the worker assembles the same minimal Docker context
      > without repository access.
- [x] 3.3 Read the Dockerfile from Omnigent-Install `main`, not from the
      aggregation's submodule pin — the same staleness reason as the corpus —
      and record its revision as a provenance input, because a Dockerfile
      change alters the image with no corpus change and would otherwise be
      invisible in a digest-only diff.
      > DONE: the child clones Omnigent-Install `main`, sparse-checks out
      > `containers/ideation-dashboard`, and the parent records the path-scoped
      > recipe revision in the proposal provenance.
- [x] 3.4 Add the artifact-only child workflow `dashboard-image-worker.yml`,
      modelled on `doc-health-analysis-worker.yml`:
      `runs-on: {group: xfactory-artifact-workers, labels: <dispatch_label>}`,
      the parent-run/correlation/source-revision verification before it acts on
      any parent input, and the digest as its ONLY result artifact. It holds no
      repository write credential.
      > CROSS-REPO (AGGREGATION). This child does NOT belong in openxFactory —
      > every worker child dispatched by `doc-health-reusable.yml`
      > (`doc-health-analysis-worker.yml`, `-cataloger-`, `-readiness-`,
      > `-derive-possibles-`) lives in the aggregation, the caller repo
      > `$GITHUB_REPOSITORY`, not here (openxFactory ships only
      > `doc-health-reusable.yml` and `session-open-pr.yml`). The openxFactory
      > stage now DISPATCHES `dashboard-image-worker.yml` and collects its one
      > `digest.json` artifact (named `dashboard-image-digest-<correlation_id>`);
      > the child itself, running `dashboard-refresh-nightly.py --phase build`
      > (fresh checkout → `--strict` generate → docker build → ACR push), is the
      > aggregation's to author and is NOT created in this repo.
      > DONE: aggregation PR #141 (`c1bba45d`) landed the active child workflow
      > (id 341027124); PR #179 (`de9a1d99`) corrected its canonical
      > aggregation checkout shape so strict validation can actually run.
      > AMENDED 2026-09-01 by Brett's credential-free runner ruling: the child
      > downloads the parent run's sealed source artifact (the same pattern as
      > its sibling workers), validates its manifest, then runs strict
      > generation/build/push. It performs no repository clone or fetch.
- [x] 3.5 Confirm the child joins the existing `xfactory-artifact-worker`
      concurrency group so the singleton host is never double-booked by the
      nightly, the review lane and this lane at once.
      > CROSS-REPO (AGGREGATION). The concurrency group is declared on the
      > aggregation's nightly caller and the child workflow, alongside 3.4.
      > DONE: the child uses the shared `xfactory-artifact-worker` concurrency
      > group with `cancel-in-progress: false`, and runner group id 5 now allows
      > this child workflow explicitly.
- [x] 3.6 (ADDED 2026-09-04 BY THE AMENDMENT, openxFactory) Expose the
      generation timestamp anchor on the `generate` CLI, because the sealed
      source artifact is not a git checkout and the amended lane cannot derive
      it. MEASURED, not assumed: `ideation_dashboard.cli generate` accepts
      `--repo-root`, `--repository`, `--source-revision`, `--project-register`,
      `--possibles`, `--strict`, `--no-validate` and nothing else
      (`scripts/ideation_dashboard/cli.py`, `_add_generate_args`), so the
      `--generated-at <manifest source committer timestamp>` that `design.md`
      Decision 3's amended step 3 and the amended spec delta's "using the
      manifest-pinned source revision and timestamp" both call for DOES NOT
      EXIST. The Python entry point `generate_snapshot` already takes
      `generated_at`; `_generation_stamp` in
      `scripts/ideation_dashboard/generator.py` otherwise derives it by
      running `git show -s --format=%cI`
      inside the scanned tree, and `RealGitDates` degrades "to None … outside a
      git checkout" — which is exactly what the child now has. So without this
      task the amended lane publishes a snapshot with NO `generated_at`, and
      the served plane's freshness header loses its stamp. This is realization
      work the amendment creates; the amendment was RE-RATIFIED 2026-09-04 by
      Brett Heap (see `proposal.md` § AMENDED AFTER RATIFICATION), so this
      task is now REQUIRED realization work on this change's code surface —
      it is not yet done (still unticked above), and it remains NOT part of
      what makes the archive gate close (§4.8).
      > DONE 2026-09-04, openxFactory PR #PRNUM. `ideation_dashboard.cli`
      > `generate` and `generate-and-open` now accept `--generated-at
      > <RFC 3339>` beside `--source-revision`: the value is validated at the
      > CLI boundary (`generator.is_rfc3339_datetime`, the shape the snapshot
      > schema's `generation.generated_at` declares), passed to
      > `generate_snapshot(generated_at=...)`, recorded VERBATIM, and it
      > overrides the git derivation. A malformed value is REFUSED
      > (`cli.GeneratedAtRefused` — stderr, exit 1, no snapshot written)
      > rather than degraded to an absent stamp, which is the defect this task
      > names. Absence changes nothing: the `git show -s --format=%cI`
      > derivation still runs and an unresolvable stamp is still omitted.
      > Pinned by `tests/ideation-dashboard/test_generated_at_anchor.py` (16
      > cases: the amended recipe's own argv parses, verbatim, override,
      > absence, seven malformed spellings refused with no file left behind,
      > and the pinned value passing a real `--strict` validation run). The
      > "not yet done" clause above states the position at authoring; this
      > note supersedes it. The task remains NOT part of what closes the
      > archive gate (§4.8) — that is unchanged.

## 4. The nightly stage (openxFactory)

- [x] 4.1 Add the refresh stage to `.github/workflows/doc-health-reusable.yml`'s
      `finalize` job, ordered AFTER the "Commit report (deliver via rolling PR)"
      step, so the refresh can never jeopardise the report it follows.
      > DONE. The "Ideation-dashboard IMAGE REFRESH stage" block sits
      > immediately after the "Commit report (deliver via rolling PR — ruleset
      > 18962101)" step and before "Open regression issue" in `finalize`.
- [x] 4.2 Gate it with the file's existing readiness idiom — the
      `GROUP="xfactory-artifact-workers"` runner-group resolution plus the
      authenticated Hermes heartbeat, evaluated by
      `scripts/check-worker-readiness.py` — and SKIP fail-closed when unready.
      Add NO inline hosted fallback: the build and push belong to the host that
      holds the registry binding.
      > DONE. "Evaluate dashboard-refresh worker readiness" (id `dfr-readiness`)
      > is a verbatim clone of the readiness-scorer idiom (runner-group + Hermes
      > heartbeat → `check-worker-readiness.py`); `ready != 'true'` runs the
      > "record skip (worker unavailable)" step and nothing else. No hosted
      > fallback exists in the stage. The `--required-label dashboard-image` /
      > `--required-profile dashboard-image-refresh` values and the matching
      > worker-profile registration are the AGGREGATION/host gate (§1.4, §2);
      > until they resolve, readiness is false and the stage skips fail-closed —
      > the designed default.
- [x] 4.3 Implement the no-change short-circuit ON INPUTS, BEFORE the build
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
      > DONE. `decide_refresh` is a pure path-scoped two-revision predicate
      > (`CORPUS_BAKED_PATHS` / `RECIPE_BAKED_PATHS`); output-digest equality is
      > banned and unspellable (`digest_note` is a note, never a trigger). The
      > `dfr-decide` workflow step runs it BEFORE dispatch, so a quiet night
      > dispatches no child and builds nothing.
- [x] 4.3a Define the provenance record's shape and make the overlay comment its
      AUTHORITATIVE home: a stable, machine-readable key/value block carrying
      both input revisions and the scoping used to compute them, written into
      the pin's comment inside the `images:` entry. It must parse
      deterministically — no prose regex-guessing. Absent or unparseable ⇒ treat
      as CHANGED (bootstrap build), never as unchanged.
- [x] 4.4 Implement the pin-PR authoring on the fixed head branch
      `bot/dox-dashboard-pin`, using the force-free rolling-branch mechanics the
      report step already proved: org ruleset 8981805 applies
      `non_fast_forward` to `~ALL` branches with NO bypass, so deliver by branch
      CREATION (deleting a stale ref first) or by a fast-forward merge commit
      whose FIRST parent is the current remote tip. Do not rediscover this — an
      earlier revision of the report step got it wrong and "succeeded solely on
      nights the push happened to CREATE the branch."
      > DONE. The "deliver pin PR to Omnigent-Install (force-free, fail-soft)"
      > step reuses the report step's exact mechanics against `RECIPE_REPO`:
      > branch CREATION (delete stale ref first) when no PR is open, else a
      > fast-forward merge commit whose first parent is the remote tip; never
      > `--force`. FAIL-SOFT: a `repos/<recipe>` read that 403s, a failed clone,
      > or a rejected push logs `::warning::` and exits 0 — the App lacking
      > Omnigent-Install scope (installation gate 1.2) never hard-fails the
      > nightly; the refresh parks for the human gate.
- [x] 4.5 Write the PR body provenance — the two input revisions, snapshot
      `source_revision`, pushed tag, new and previous digests,
      strict-validation counts, and the run URL — and mark it explicitly as a
      COURTESY restatement: the record the lane reads is the overlay comment
      (4.3a), never the PR body. Assert no label, title prefix or
      commit-message convention is used to CLAIM the diff shape — the receiving
      repository adjudicates it.
      > DONE. `render_pr_body` (module) writes exactly these fields, states it
      > is a courtesy restatement, and the delivery step sets no shape-claiming
      > label/title-prefix/commit convention.
- [x] 4.6 Confirm the produced diff is exactly the `digest:` line plus its
      adjacent provenance comment on the `ideation-dashboard` entry, and touches
      no other line, block or file. Keep the human-readable facts the existing
      comment carries (see 1.5) and add the 4.3a key/value block beside them —
      the comment must serve both a reader and the parser.
      > DONE. `rewrite_pin` replaces only the digest value + machine-provenance
      > comment lines and preserves the human prose; the delivery step's
      > `git diff --cached --quiet` envelope guard confirms the overlay is the
      > only file touched. Pinned by tests 5.3 / 5.2a.
- [x] 4.7 Write `health/ideation-dashboard/refresh-status.json` beside the
      existing `lane-status.json`, following `nightly_lane.py`'s status idiom
      (diagnostic, not a projection; its own failure must never take the run
      down). Fields: result (`ok` / `no_change` / `skipped` / `strict_failed`),
      reason, bounded detail, the two input revisions each beside the recorded
      revision compared against, `source_revision`, built and pinned digests
      (when a build occurred), tag, PR reference, `generated_at`, `run_id`. A
      `no_change` outcome MUST name the revisions that matched, so "nothing
      moved" is auditable rather than asserted.
      > DONE. `refresh_status_payload` / `write_refresh_status` carry every
      > field; the PR-reference field is patched post-delivery by a new
      > `--phase record-pr` CLI seam — the SMALLEST wrapper needed, wiring the
      > module's already-tested `record_pull_request()` to the CLI so the
      > delivery step can call it once the cross-repo push knows the URL
      > (covered by `test_the_record_pr_cli_phase_patches_the_delivered_status`).
- [x] 4.8 (HUMAN GATE) Resolve the reporting-lag choice (design Open Question 3):
      accept the one-run lag and have the report SAY which run's outcome it
      names, or add a second narrowly-scoped delivery for the status artifact
      after the stage. Record the choice.
      > GATE OPEN (awaiting ratification). The implementation REALIZES the
      > design's preferred resolution — the one-run lag, with the report section
      > naming whose outcome it is ("this run" vs "the PREVIOUS run") — so no
      > second delivery is wired. A reviewer may still fix the choice at
      > ratification; switching to same-run delivery would be an added step.
      **RESOLVED AT RATIFICATION, 2026-08-25 — Brett, in-session, verbatim:
      "ratify add-nightly-dashboard-refresh against its realized system".** The
      reporting-lag choice is settled AS IMPLEMENTED: the one-run lag stands,
      with the report section naming whose outcome it is, and no second delivery
      is wired. A reviewer did not fix it the other way, so the note above
      describes the ratified state rather than a pending option.
      **THE REALIZATION EVIDENCE, verified at this gate against GitHub and git
      rather than read out of any handoff — every sha below is the sha the MERGE
      produced.** openxFactory: PR #260 `de638933` (2026-08-22T13:54:03Z, the
      packet) and PR #261 `446291d4` (2026-08-22T15:54:20Z, the lane
      implementation). Aggregation opensoft/xFactory: PR #141 `c1bba45d`
      (2026-08-24T07:30:53Z, `dashboard-image-worker.yml`, the artifact-only
      build+push child — confirmed present on `main` at 19281 bytes and
      registered as an ACTIVE workflow, id 341027124). Omnigent-Install: PR #123
      `7d0370d5`, #126 `7365eb36` (the Flux delivery companion), #129
      `509b7d65` (the `acr_push` worker-host credential), #143 `5b5592e4`
      (token materialization into the runner env), #146 `575bc26f` (merge-master
      auto-approval for the pin PRs) and #153 `da0bdeba` (the pin shape check
      hardened to take its adjudicator from the base-branch tip). The
      receiving-side gate is live: ruleset **21294850** on Omnigent-Install,
      name "dox digest-only pin scope — required check", target `branch`,
      enforcement `active`, requiring the context `Digest-only pin scope`.
      **THE ARCHIVE GATE STAYS OPEN, and this is the honest half of the tick.**
      This packet's own `target_release` sets the bar in its own words: "one
      real nightly producing a digest-only pin PR against Omnigent-Install that
      merge-master approves, GitHub auto-merges and Flux reconciles, PLUS one
      deliberately wider diff from the same lane identity refused and parked. A
      lane proven only by a dry run is exactly the evidence this program has
      learned not to accept." NEITHER HALF IS MET, measured rather than
      assumed:
      1. The build+push child has **never run**: the GitHub API reports
         `total_count: 0` for workflow 341027124's runs.
      2. **No pin PR has ever existed** — a search of Omnigent-Install for
         `head:bot/dox-dashboard-pin` across all states returns nothing, so
         nothing was approved, auto-merged or reconciled.
      3. The two nightly cycles since the chain landed both **FAILED** before
         the lane could act — `doc-health-nightly` run `32683853055`
         (2026-08-24T02:40:44Z) and `32802204594` (2026-08-25T02:39:01Z), both
         `completed/failure` in `prepare` and `finalize`. On both runs EVERY
         refresh step is `skipped`, including "Evaluate dashboard-refresh worker
         readiness", "decide (no-change short-circuit, before any build)",
         "Dispatch artifact-only dashboard-image child" and "render pin
         proposal". The lane has therefore not been exercised in either
         direction — not a pin, and not a clean no-change short-circuit. Note
         the last SUCCESSFUL nightly, `32613445675` (2026-08-23T02:40:27Z),
         predates the chain going live.
      4. The negative direction (§7.3's wider-diff refusal) is likewise
         unproven, having no lane run to be refused.
      So the code is MERGED AND WIRED but NOT EXERCISED, which is exactly the
      state `target_release` declines to archive on. §7 and §8.5 stay open, and
      §8.5's gate is discharged by the FIRST REAL NIGHTLY, in either
      direction, not by this ratification.
- [x] 4.9 Add the report section for the refresh outcome, and the stuck-chain
      signal: a `bot/dox-dashboard-pin` PR still open at the next run is
      reported, naming it.
      > DONE. The "report previous outcome (one-run lag; Decision 6)" step
      > (before delivery, gated on a fresh dated report) runs `--phase report`;
      > `render_report_section` names the run and, given `--stuck-pull-request`
      > (resolved fail-soft via `gh pr list` on Omnigent-Install), flags a STUCK
      > CHAIN.
- [x] 4.10 Emit `::notice::` / `::warning::` annotations for every outcome so a
      skip is never silent in the run itself, whatever the artifact-delivery
      lag turns out to be.
      > DONE. `RefreshOutcome.annotation()` emits `::notice::` for ok/no_change
      > and `::warning::` for skipped/strict_failed on every CLI run; the
      > workflow adds explicit `::warning::` for dispatch/pin/delivery
      > park-points and `::notice::` on a delivered pin PR.

## 5. Tests (openxFactory)

- [x] 5.1 Tests under `tests/ideation-dashboard/` for the refresh status
      artifact: every outcome class, the bounded detail, and the invariant that
      a status-write failure does not fail the lane.
      > DONE. `test_dashboard_refresh_lane.py` — status per outcome class, the
      > status-write-failure invariant, plus a new
      > `test_the_record_pr_cli_phase_patches_the_delivered_status` for the
      > record-pr CLI seam. 40 tests pass (was 39; +1 for the seam).
- [x] 5.2 Tests for the no-change short-circuit, pinning the ORDERING and not
      just the outcome: (a) same-input night ⇒ the lane stops BEFORE the docker
      build — assert structurally that no checkout, no snapshot generation, no
      build and no push were invoked, not merely that no PR was opened, because
      an outcome-only assertion passes even if the build ran; (b) a pin whose
      provenance is absent or unparseable ⇒ the lane BUILDS (bootstrap), and the
      pin it produces carries a parseable record; (c) recipe moved / corpus
      static ⇒ builds; (d) an unrelated commit on the served plane's repository,
      including a simulated previously-merged pin, ⇒ does NOT rebuild, which is
      the guard against a tip-versus-tip regression.
      > DONE. Ordering asserted structurally via `RecordingBuild` (the build
      > callable is never invoked on a no-change night); bootstrap, recipe-moved,
      > and the unrelated-commit / simulated-merged-pin cases each pinned, with
      > path-scoping asserted on the recipe-side query.
- [x] 5.2a A round-trip test over the REAL overlay file: the provenance block the
      lane writes is parsed back to the same two revisions, and the surrounding
      human prose is preserved. This is the guard on the one comment that is now
      load-bearing state.
      > DONE. `test_provenance_round_trips_through_the_real_overlay` over the
      > `dox-aks-qa-kustomization.yaml` fixture.
- [x] 5.3 A test that the produced diff is envelope-shaped: exactly the digest
      line and its adjacent comment in the `images:` block of the one overlay
      file, over a fixture of the real file. This is the guard that keeps a
      future edit from quietly widening what the lane can produce.
      > DONE. `test_the_produced_diff_is_the_digest_line_and_its_adjacent_comment`
      > + `test_the_other_image_entries_keep_their_digests`.
- [x] 5.4 A test that the snapshot `source_revision` and the recorded corpus
      revision are asserted EQUAL by the lane, so the two-revision trap is
      detectable rather than merely avoidable.
      > DONE. `test_verify_one_revision_rejects_a_two_revision_image` +
      > `test_the_build_asserts_one_revision_before_it_builds`.
- [x] 5.5 Run the full suites and report the real exit status. Do not pipe the
      run through `tail` or any filter that can mask a failure.
      > DONE. `python3 -m pytest tests/ideation-dashboard/test_dashboard_refresh_lane.py -q`
      > → 40 passed (full output, unfiltered). See the realization report.

## 6. The receiving side — shape check and approval (OMNIGENT-INSTALL)

This is the companion's task 7, unblocked by rulings (a) and (b). Ordered after
§4 so the identity the grant names is real.

- [x] 6.1 Implement the repository-side shape check as a REQUIRED status check
      over the ACTUAL diff: exactly one file
      (`deploy/kubernetes/overlays/aks-qa/kustomization.yaml`), every changed
      line a `digest:` value or a comment inside the `images:` block, no image
      entry added or removed, no `name:`/`newTag:` change, no change to
      `resources:`, `patches:`, `namespace:` or the header. It MUST ignore
      everything the author asserts — label, title, commit message: identity is
      an input to the predicate, never the verdict.
      > GATE OPEN (OMNIGENT-INSTALL). The line-level shape check is the receiving
      > repository's to author; the openxFactory lane's job is only to PRODUCE a
      > conforming diff (rewrite_pin, envelope-guarded delivery), never certify it.
      > DONE in Omnigent-Install PR #153 (`da0bdeba`). The base-branch
      > `dox-pin-shape-check.yml` adjudicates the actual PR diff; active ruleset
      > 21294850 requires its `Digest-only pin scope` context on `main`.
- [x] 6.2 Install the merge-master App on Omnigent-Install, add the
      `merge-master-approval` workflow and an envelope INSTANCE with ONE
      candidate class: `target_repos: [opensoft/Omnigent-Install]`,
      `expected_author` = the §1.2/§1.3 App's bot login,
      `expected_head_ref: bot/dox-dashboard-pin`, `expected_base_ref: main`,
      `path_allowlist: [deploy/kubernetes/overlays/aks-qa/kustomization.yaml]`,
      `require_all_checks: true`,
      `check_exclusions: [merge-master-approval]`, `revert_suffices: true`.
      Set the `MERGE_MASTER_APP_ID` / `MERGE_MASTER_APP_KEY` bindings.
      > GATE OPEN (OMNIGENT-INSTALL). The merge-master candidate class + workflow
      > + required-check config land on Omnigent-Install; the openxFactory stage
      > already delivers on the exact `bot/dox-dashboard-pin` head the envelope
      > names. `expected_author` follows the §1.2/§1.3 App-identity ruling.
      > DONE in Omnigent-Install PR #146 (`575bc26f`). The live candidate names
      > `openxfactory[bot]`, fixed head `bot/dox-dashboard-pin`, base `main`, the
      > one overlay path, all-checks-green, and excludes only its own
      > `merge-master-approval` check. Org-level `MERGE_MASTER_APP_ID` and
      > `MERGE_MASTER_APP_KEY` are selected for Omnigent-Install.
- [x] 6.3 Keep the base-branch security properties intact: the envelope config
      AND the workflow definition are read from the BASE branch, no PR-head
      content is checked out or executed, the approving identity is distinct
      from the authoring identity, and the envelope file's own path sits outside
      every `path_allowlist` so a PR editing the rules can never be
      autonomously approved. Pin the shared decision core by SHA, as the
      aggregation does, rather than tracking a moving branch.
      > DONE: the live workflow is `pull_request_target`/`check_suite` plus
      > explicit `workflow_dispatch`, reads workflow + envelope from the base,
      > executes no PR-head content, and pins the codexFactory decision core.
- [x] 6.4 (HUMAN GATE) Choose the approval trigger (design Open Question 2):
      in-repo `workflow_run` on the shape check's completion — recommended,
      base-branch semantics preserved, no extra App permission — or the
      cross-repo `gh workflow run` chain, which needs `actions: write` on the
      App's installation here. Either way the trigger is NON-FATAL: a failed
      trigger parks the PR for the human gate and never fails the nightly.
      > RESOLVED AS REALIZED: the App-authored PR raises
      > `pull_request_target`; completed check suites re-trigger evaluation, and
      > `workflow_dispatch` remains the fail-soft explicit backstop. Recent live
      > `check_suite` evaluations are green.
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

- [x] 8.1 Add this change to the openxFactory README "OpenSpec Records" block,
      in that list's existing format.
      > DONE at `README.md`'s active-change record, including ratification,
      > merged realization, open archive gate, authority split, staleness
      > model, and the runtime-fetch conformance gap.
- [x] 8.2 Record the conformance gap explicitly where the served plane is
      documented: the hosted image today passes only `--snapshot` and
      `--checkout-root` and performs no runtime fetch, so its baked artifacts
      ARE its data and this lane's cadence IS its data cadence. Name the rebake
      bound as the mitigation, and do NOT present it as the intended design.
      > DONE in the active README record and the change's modified
      > `ideation-dashboard` requirement: the current hosted plane has no
      > runtime fetch, baked artifacts are its data, the rebake cadence is only
      > a mitigation, and runtime fetch remains the intended contract.
- [x] 8.3 Confirm `OPENSPEC_TELEMETRY=0 openspec validate
      add-nightly-dashboard-refresh --strict` and `--all --strict` are clean.
      > DONE 2026-08-31: change strict validation passed; repository-wide strict
      > validation passed 76/76 artifacts with 0 failures.
- [ ] 8.4 Notify the companion `add-dox-gitops-reconciliation` that legs 1–2 are
      live and its Open Questions are closed: the mechanism is Merge Master
      extended with a second candidate class (ruling a), the lane identity is
      the existing `XFACTORY_APP` on the fixed head branch
      `bot/dox-dashboard-pin` (ruling b), and this lane claims no apply
      capability of its own. Its task 8.3 is the counterpart of this one.
- [ ] 8.5 Archive per the `target_release` gate: `implementation_pending`, and
      the evidence is §7's real cycle in BOTH directions. A lane proven only by
      a dry run does not close this change.

## 9. Adoption record — the 2026-09-01 amendment's gate pass (lane `openxfactory-f2`)

**RECORD, 2026-09-04.** The seventeen `[x]` flips in §§1, 2, 3, 6 and 8 above,
and their completion prose, were authored 2026-09-01 by the lane
`openxfactory-nightly` and stranded uncommitted in the shared aggregation
checkout at `6612d323`. They were rescued byte-identical as PR #595 (issue
#591) and adopted on Brett's word 2026-09-04, verbatim: "go on 595". This
repository's own rule is that a cross-repository claim is verified at the gate
rather than read out of a handoff, so the adopting lane re-verified every claim
those flips make that is checkable from outside the host. **Not one flip was
altered**; this section records what was and was not confirmed.

**VERIFIED against the provider API, 2026-09-04 — every merge sha the flips
name is real, merged, and is the sha named:**

| task | claim | verified |
| --- | --- | --- |
| 2.2 | Omnigent-Install PR #129 `509b7d65` | MERGED 2026-08-22, `509b7d6541967f44a1fc96f0b7dd047820f5f7ed` |
| 3.4 | aggregation PR #141 `c1bba45d` | MERGED 2026-08-24, `c1bba45de43586cdd84df8465433b8b3d7bc518a` |
| 3.4 | aggregation PR #179 `de9a1d99` | MERGED 2026-08-31, `de9a1d99d4c7bb5d85f37a66e6b93834df1e7421` |
| 6.1 | Omnigent-Install PR #153 `da0bdeba` | MERGED 2026-08-24, `da0bdeba2292a6127a45ecacbf15aacdfd4f3453` |
| 6.2 | Omnigent-Install PR #146 `575bc26f` | MERGED 2026-08-24, `575bc26f43174e444467c185976ea4181888fa30` |
| 8.1 | the README "OpenSpec Records" entry | present on `main`, `README.md`, naming the ratification and the open archive gate |
| 8.3 | strict validation clean | re-run at this branch's head; output in the adopting PR |

**NOT RE-VERIFIED BY THE ADOPTING LANE — host- and org-admin facts that cannot
be checked from outside the host, and outside this repository; the ticks above
stand on the originating lane's own evidence and are not withdrawn.** Recorded
as unconfirmed rather than doubted: the
`XFACTORY_APP` installation `145372182` being organization-wide with
`contents: write` + `pull_requests: write` (1.3); the runner label
`dashboard-image` on runner id 23 and runner group id 5's allowed-workflow
entry (3.5); active ruleset `21294850` on Omnigent-Install `main` (1.6); the
current overlay pin digest and its `xf-refresh-provenance: v1` comment (1.5);
and the escrowed `cpc-brett01-acr-push-token` (2.2's rider note). Every one of
these is re-checked in §7's real cycle, which is the evidence gate that
actually closes this change — so none of them is load-bearing for the flip
being honest, and none is taken on trust by anything that has landed.

**§4.8 AND THE ARCHIVE GATE ARE UNMOVED.** No task in §7 was flipped by the
amendment, `target_release` stays `implementation_pending`, and the lane has
still never run. Whatever is ruled on the amendment, the archive gate stays
open.

**2026-09-04 — RULED (Brett Heap, verbatim "delete the debug tool"):
`playwright-smoke-debug.py` deleted in PR #595; its ~15 lines of DOM capture
are recoverable from the rescue commit 2ffe1807 if ever needed.
Re-ratification of the amended delta recorded in proposal.md § AMENDED AFTER
RATIFICATION.**
