# Design: add-nightly-dashboard-refresh

Status: draft (authored 2026-08-22)

## Context

**Verified facts, 2026-08-22 (read-only reads of the checked-out trees).**

- **The companion is merged.** `add-dox-gitops-reconciliation` is on
  Omnigent-Install `main` at `7d0370d`. Its Requirement "Digest-only pin PRs
  from the nightly-refresh lane may merge without human review" fixes the SCOPE
  (one file, digest lines and their comments inside the `images:` block, the
  governed lane identity, a repository-side shape check) and leaves the
  MECHANISM and the IDENTITY NAME open, deliberately, to this change. Its
  task 7 is ordered behind that ruling: "a grant whose subject is unresolved
  must not be created."
- **The nightly already mints an App token per run.**
  `.github/workflows/doc-health-reusable.yml` (openxFactory) mints
  `XFACTORY_APP_ID` / `XFACTORY_APP_PRIVATE_KEY` through
  `actions/create-github-app-token@v2` with
  `owner: ${{ github.repository_owner }}` in BOTH the `prepare` and `finalize`
  jobs. An `owner`-scoped mint covers every repository that installation
  includes.
- **The nightly already dispatches five artifact-only children.** Semantic
  analysis, cataloger, organizer, readiness-scorer and derive-possibles each
  run `GROUP="xfactory-artifact-workers"`, resolve the runner group by API,
  fetch an authenticated Hermes heartbeat, and hand both to
  `scripts/check-worker-readiness.py`. `ready=false` skips; it never falls back
  onto the hosted runner for the worker's job.
- **The worker host is capable and registry-bound.**
  `clients/opensoft/worker-hosts/cpc-omni01.worker-host-manifest.yaml`:
  `container_engine: docker-ce`, runner `xfactory-artifact-cpc-omni01` in group
  `xfactory-artifact-workers`, dispatch label `host-artifact-cpc-omni01`, and
  an `acr_pull` block naming `acropensoftxfactoryqa.azurecr.io`.
- **The image bakes DATA, and says so.**
  `containers/ideation-dashboard/Dockerfile` at Omnigent-Install `main` copies
  `openxFactory/scripts/ideation_dashboard/`,
  `openxFactory/scripts/doc_health/`,
  `health/ideation-dashboard/openxFactory-snapshot.json`, and six governed
  corpus roots under `openxFactory/`, then runs `serve.py` with
  `--snapshot /app/snapshot.json --checkout-root /srv/checkout/openxFactory`.
  Its build context is the ASSEMBLED WORKSPACE SHAPE, and it says so:
  "BUILD CONTEXT = the xFactory aggregation WORKSPACE ROOT, because the three
  baked inputs live in three assembled repos."
- **The manual recipe is recorded in the pin's own comment.** The current
  `ideation-dashboard` entry in
  `deploy/kubernetes/overlays/aks-qa/kustomization.yaml` reads: "BAKED SNAPSHOT
  + /source corpus refreshed to openxFactory main @ 7ae4fe9, generated
  --strict from that same checkout so data and corpus share one
  source_revision."
- **`--strict` means zero errors and zero warnings.**
  `scripts/ideation_dashboard/snapshot.py` records the validator's contract as
  "Exit codes: 0 ok, 1 findings (or warnings under --strict), 2 harness error",
  and `cli.py`'s `_validate` additionally FAILS under `--strict` when the
  validator could not RUN at all — "asking for strictness and getting 'we
  skipped the check' would make the flag a lie."
- **Merge Master exists, is reviewed, and is list-shaped.**
  `.github/workflows/merge-master-approval.yml` (aggregation) submits an
  APPROVE review with a DEDICATED merge-master App token when a rules-as-code
  envelope conjunctively holds, and never issues a merge call — GitHub
  auto-merge lands it. `.github/merge-approval-envelope.yml` is a
  `candidates:` LIST, each entry carrying `target_repos`, `expected_author`,
  `expected_head_ref`, `expected_base_ref`, `path_allowlist`,
  `require_all_checks`, `check_exclusions` and `revert_suffices`.

## Goals / Non-Goals

**Goals**

- The hosted plane's baked data is refreshed on a schedule, not on somebody's
  memory.
- The snapshot and the baked corpus share ONE revision by construction.
- Nothing is published that did not pass `--strict`.
- Nothing is proposed when nothing changed.
- Every rung of the chain holds exactly the authority it already held.
- Both of the companion's open questions closed with reasons, not preferences.
- Failure and parking are visible in the morning report.

**Non-Goals**

- The apply. The companion owns it; this lane must claim no apply capability.
- Realizing the promoted RUNTIME snapshot fetch (Decision 7 explains why this
  change names that gap instead of closing it).
- Any change to the deterministic pass, its families, or the existing snapshot
  lane.
- A refresh lane for `dox-auth`, `intent-inbox`, `dispatch-token-minter`, or any
  other surface image.
- Any expansion of the worker permission matrix, or any per-lane exception.

## Decisions

### Decision 1 — RULING (a): the auto-merge mechanism is Merge Master, extended to Omnigent-Install with a second candidate class

The companion left two shapes on the table: an approver-bot grant conditioned
on a repository-side shape check, or a ruleset bypass scoped to the lane
identity. It named the approver-bot shape preferred and gave the reason —
"the exception lives in a revocable grant rather than in the branch
protection." This change rules for that shape, and rules further that it is
**the existing Merge Master capability**, not a new mechanism built to the same
description.

The security reasoning is INHERITED, not re-derived, and it is worth restating
because every clause of it is load-bearing here too. From
`merge-master-approval.yml`'s own header:

- **The rules and the logic both come from the base branch.** The workflow runs
  under `pull_request_target`, which "runs the workflow definition FROM THE BASE
  BRANCH"; the envelope config is read from the base checkout. "A pull request
  can never alter the rules (or the logic) that govern its own approval." A
  plain `pull_request` trigger "would run the workflow file from the PR head —
  letting a PR rewrite its own approval logic."
- **No PR-head content is executed.** The workflow "reads PR metadata, the
  changed-file list, and head-SHA check-runs via the API" and deliberately does
  not check out or run head content, so the classic `pull_request_target`
  head-execution risk does not apply.
- **A non-candidate PR is skipped, never approved.** "A fork/other PR that
  happens to target the default branch triggers this workflow but fails the
  candidate class (author + same-repo head ref) and is skipped."
- **The approval identity is separate from the author identity.** The approval
  is submitted with a DEDICATED merge-master App token, "never the default
  GITHUB_TOKEN (whose approvals do not satisfy the required review)", and the
  envelope's own comment records why: "A distinct identity from the merge-master
  approver (GitHub's author-cannot-approve rule), so its approval counts."
- **The envelope file is self-protecting.** Its header notes that "any diff that
  edits this file lands outside every path_allowlist below, so such a PR is
  never autonomously approved", and that it sits under a CODEOWNERS-gated
  `.github/` path.
- **Approval is not merging.** Merge Master "never issues a merge call";
  GitHub's auto-merge lands the PR under the ordinary ruleset. The org ruleset
  is untouched, which is exactly the property the companion preferred.

**The second candidate class.** `candidates:` is a list and each entry already
carries `target_repos`, so a second class is a list entry, not a redesign:

```yaml
  - id: dox-dashboard-pin
    target_repos: [opensoft/Omnigent-Install]
    expected_author: <the XFACTORY_APP bot login>      # ruling (b)
    expected_head_ref: bot/dox-dashboard-pin
    expected_base_ref: main
    path_allowlist:
      - deploy/kubernetes/overlays/aks-qa/kustomization.yaml
    require_all_checks: true
    check_exclusions: [merge-master-approval]
    revert_suffices: true
```

**Where the line-level predicate lives, and why the envelope cannot hold it.**
`path_allowlist` is a PATH predicate. The companion's requirement is stricter
than any path: "within that file every changed line is a `digest:` value or a
comment inside the `images:` block, with no image entry added or removed, no
`name:` or `newTag:` change, and no change to `resources:`, `patches:`,
`namespace:` or the header." No envelope field expresses that. So the
composition is:

- the **envelope** contributes author + head ref + base ref + the one-file path
  allowlist + all-non-excluded-checks-green;
- an **Omnigent-Install-side required check** contributes the LINE-level shape
  predicate over the actual diff;
- `require_all_checks: true` makes the second a precondition of the first.

This is precisely the companion's condition 4 and its reason: "if the lane
asserts its own diff shape — by a label it sets, a commit-message convention, a
title prefix — then a compromised or buggy lane widens its own exception." The
shape check reads the diff and nothing the author says. Identity is an input to
the predicate; the verdict comes from the repository.

**Fail-closed in both senses.** A wider diff fails the shape check, which fails
`require_all_checks`, which means no approval and the ruleset's 1-approval
requirement stands — the PR parks. And the mechanism is revocable by one
configuration change: delete the candidate entry (or unset
`vars.MERGE_MASTER_APP_ID`) and every PR against that file needs a human again,
with no code change and no redeploy.

**The trigger, and the one wrinkle worth writing down.** Merge Master runs in
the repository it evaluates (`REPO: ${{ github.repository }}`, and the core is
asked `--list-head-refs --repo "$REPO"`), so Omnigent-Install needs the
workflow file, an envelope instance, and the merge-master App installed with
its `MERGE_MASTER_APP_ID` / `MERGE_MASTER_APP_KEY` bindings. The aggregation
learned the hard way (live-verified 2026-07-28) that a head update alone may
not produce an approving run: a GITHUB_TOKEN-authored push is
recursion-suppressed, and "Actions-created check suites never retrigger
check_suite", so the nightly chains the workflow with an explicit
`gh workflow run`. Here the push is APP-authored, so `pull_request_target` DOES
fire — but it fires before the required checks (including the shape check) have
concluded, and that run parks fail-closed. The evaluation must therefore be
re-triggered AFTER the checks finish. Two orderings satisfy that, and the
implementation should prefer the first:

1. **In-repo `workflow_run` on the shape check's completion.** `workflow_run`
   also runs the workflow definition from the default branch, so it keeps the
   base-branch security property intact, and it needs no cross-repo token and
   no extra App permission. This is the cleanest trigger and is the recommended
   one.
2. **Cross-repo `gh workflow run` from the nightly**, mirroring the
   aggregation's proven chain. This requires `actions: write` on the App's
   Omnigent-Install installation, and it is the backstop if (1) proves
   unreliable in practice.

Either way the dispatch is non-fatal: a failed trigger parks the PR for the
human gate and never fails the nightly, exactly as the aggregation's
`|| echo "::warning::approval-workflow dispatch failed — PR parks for the human
gate"` already does.

### Decision 2 — RULING (b): the lane identity is the existing `XFACTORY_APP`, not a new App

The companion's Open Question 2 asked for "the lane identity's concrete name."
The answer is the App the reusable workflow already mints — the same identity
that authors the nightly `doc-health/nightly` rolling PR and whose bot login
the aggregation envelope already names as `expected_author`.

Three reasons, in order of weight.

1. **It is already the factory identity for exactly this act.** `doc-health`'s
   promoted "Sweep execution split" requirement says orchestration runs "under
   the factory identity (a short-lived installation token minted from the
   openxFactory GitHub App)". Opening the pin PR IS orchestration — it is the
   lane's proposal artifact. Minting a second App for the second thing the same
   orchestrator proposes would fragment the identity the contract names.
2. **Fewer standing grants is the whole point.** A new App means a new private
   key to escrow and rotate, a new installation to audit, and a second
   `expected_author` in a security-critical config. The App already exists, its
   key is already escrowed as a repository secret, and its blast radius is
   already reviewed.
3. **The mint is already owner-scoped.** The workflow mints with
   `owner: ${{ github.repository_owner }}`, so a token that reaches
   Omnigent-Install requires an INSTALLATION change, not a workflow change.
   That is the right place for the grant to live: an installation is
   auditable in the org's App settings and revocable there.

**What must actually be verified, as a task and not an assumption.** The App's
installation must include `opensoft/Omnigent-Install` with:

- `contents: write` — to create/advance the `bot/dox-dashboard-pin` branch;
- `pull_requests: write` — to open the pin PR and comment on it;
- `actions: write` — ONLY if Decision 1's fallback trigger (2) is chosen.

Two properties of the mint deserve their own note, because the aggregation has
already been bitten by both. First, the App's installation permissions are
per-installation, so verifying it on the aggregation proves nothing about
Omnigent-Install. Second, a permission the installation lacks fails at CALL
time, not at mint time — the aggregation's own comment records the shape of
that failure: "its installation carries no `actions` permission, so the
approval-workflow dispatch ... must run on the job's GITHUB_TOKEN instead (403
otherwise — live-verified 2026-07-28)". So the verification task must make a
real authenticated call against Omnigent-Install, not read a settings page.

**Contingency, recorded rather than waved away.** If the installation cannot be
extended (an org policy, or a decision that the content App must not hold write
on an install repo), a dedicated refresh-lane App is minted instead. Everything
else in this design is unchanged except the `expected_author` value in the one
envelope entry — which is the property that made naming the identity ONCE, in
configuration, the right shape in the first place.

**The head branch is fixed, and that is deliberate.**
`bot/dox-dashboard-pin`, one branch, reused nightly, mirroring
`doc-health/nightly`. A fixed ref is what lets the envelope pin
`expected_head_ref` to a literal instead of a pattern, and it means at most one
open pin PR at a time. It also inherits the rolling-PR mechanics the report
step already proved: because org ruleset 8981805 applies `non_fast_forward` to
`~ALL` branches with NO bypass, no token can force-push any branch in this org,
so the lane must deliver by branch CREATION (delete the stale ref first) or by
a FAST-FORWARD merge commit whose first parent is the current remote tip. The
implementation should reuse that exact idiom rather than rediscover it — the
aggregation's comment records an earlier revision that got this wrong and
"succeeded solely on nights the push happened to CREATE the branch."

### Decision 3 — The build context problem, and the fresh-checkout recipe

**AMENDED 2026-09-01 (PENDING RE-RATIFICATION — see `proposal.md`
§ AMENDED AFTER RATIFICATION, 2026-09-04) — fresh inputs cross the host
boundary as a sealed parent artifact, never as worker-side repository
clones.** Brett's host ruling is
explicit: "The runner design intentionally requires
`repository_credentials_absent`; source is delivered as sealed job artifacts and
the runners do not clone or push repositories." Both input repositories are
private, and the first real child runs proved the contradiction empirically: an
artifact rider with no repository credential cannot perform the raw clones this
decision originally placed there. Deploying repository keys through Intune would
weaken the host contract to rescue an implementation detail. The authority-
preserving correction moves ONLY the repository-read act to the credentialed
hosted parent; strict generation, Docker build, ACR push, and digest production
remain on the artifact rider.

This is the part that is easy to get subtly wrong, so it is written out.

The Dockerfile's build context is the ASSEMBLED WORKSPACE SHAPE — a directory
containing `openxFactory/` (scripts plus six governed corpus roots) and
`health/ideation-dashboard/openxFactory-snapshot.json`. In a developer's
workspace that shape is just the aggregation checkout. In CI it is not, and
naively building from the aggregation checkout produces a **two-revision
image**:

- `openxFactory/` in the aggregation is a SUBMODULE at its PIN, which lags
  `main` by however long since the last pointer-sync commit;
- `health/ideation-dashboard/openxFactory-snapshot.json` is the committed
  snapshot the existing nightly lane generated — from that same pinned
  submodule.

Both would be self-consistent and both would be STALE, which is the defect the
whole change exists to remove. Worse, a half-corrected version — fresh corpus,
committed snapshot — bakes a snapshot whose `source_revision` names a commit
that is NOT the corpus in the same image, and the freshness header would then
truthfully report a revision the `/source` viewer cannot serve.

So the recipe is the one the two manual builds used, and it is the recipe
because of that property:

1. Make a scratch context directory `<ctx>`.
2. Clone/checkout openxFactory `main` into `<ctx>/openxFactory` — a FRESH
   checkout, not the submodule pin.
3. Generate the snapshot FROM THAT CHECKOUT into the context:
   `PYTHONPATH=scripts python3 -m ideation_dashboard.cli generate
   --repo-root . --repository openxFactory --strict
   --output <ctx>/health/ideation-dashboard/openxFactory-snapshot.json`,
   run from `<ctx>/openxFactory`. `--repo-root .` is what makes
   `source_revision` the checkout's own git HEAD; `--strict` is the gate.
4. `docker build -f <omnigent-install-checkout>/containers/ideation-dashboard/Dockerfile <ctx>`
   — the Dockerfile comes from Omnigent-Install `main`, the CONTEXT is
   `<ctx>`.
5. Tag date-stamped, push, capture the digest.

**THE RECIPE AS AMENDED 2026-09-01 (pending re-ratification).** The five steps
above are the text as ratified 2026-08-25 and are retained unedited. Under
Brett's host ruling the repository-read act moves to the parent and the recipe
reads as follows; step 5 is unchanged and is not repeated.

1. AFTER the no-change decision finds movement, the credentialed hosted parent
   checks out openxFactory `main` and the Omnigent-Install recipe at `main`, with
   credentials not persisted, and records each path-scoped baked-input revision.
2. The parent copies only the Dockerfile COPY roots plus the recipe directory
   into a bounded source artifact and writes a manifest carrying the source HEAD,
   its committer timestamp, the path-scoped corpus revision, and the path-scoped
   recipe revision. It uploads that directory as the source run's sealed job
   artifact.
3. The artifact-only child verifies the source-run provenance, downloads that
   exact artifact with its read-only Actions token, validates the manifest and
   required paths, and generates the snapshot FROM THAT CORPUS TREE into the
   context:
   `PYTHONPATH=scripts python3 -m ideation_dashboard.cli generate
   --repo-root . --repository openxFactory --strict
   --source-revision <manifest source HEAD>
   --generated-at <manifest source committer timestamp>
   --output <ctx>/health/ideation-dashboard/openxFactory-snapshot.json`,
   run from `<ctx>/openxFactory`. The two explicit generation anchors preserve
   the deterministic stamp the fresh checkout supplied; `--strict` is the gate.
4. `docker build -f <bundle>/omnigent-install/containers/ideation-dashboard/Dockerfile <ctx>`
   — the Dockerfile comes from Omnigent-Install `main`, the CONTEXT is
   `<ctx>`.

> **REALIZATION OWED, MEASURED BY THE ADOPTING LANE 2026-09-04 — step 3 above
> names a flag that does not exist.** `--source-revision` IS a real argument of
> `ideation_dashboard.cli generate` (`scripts/ideation_dashboard/cli.py`,
> `_add_generate_args`). **`--generated-at` IS NOT**: that subcommand accepts
> only `--repo-root`, `--repository`, `--source-revision`, `--project-register`,
> `--possibles`, `--strict` and `--no-validate`. The PYTHON entry point
> `generate_snapshot` does take `generated_at`, and `_generation_stamp`
> (`generator.py`) derives it from the revision's committer date when it is not
> passed — but that derivation runs `git show -s --format=%cI` INSIDE the
> scanned tree, and `RealGitDates` is documented to degrade "to None … outside
> a git checkout", which a sealed source artifact is. So on the amended lane the
> snapshot would carry NO `generated_at` at all unless the value is passed in.
> The requirement is therefore right and the interface is missing: exposing the
> anchor on the CLI is realization work this amendment creates. Filed as
> `tasks.md` § 3.6.

Step 3's `--strict` is a real gate and not decoration: it means zero errors AND
zero warnings, and it also fails when the validator could not RUN, so a
missing-validator environment cannot silently produce an unvalidated snapshot.
A non-zero exit at step 3 means steps 4–5 do not happen — no tag exists, no
digest exists, and there is nothing to propose. That ordering is why the
requirement says "publishes nothing" rather than "publishes and reports": the
strict failure precedes the push, so there is no artifact to retract.

Two notes for the implementation. The Dockerfile is read from Omnigent-Install
`main` rather than from the aggregation's submodule pin, for the same
staleness reason as the corpus — and it should be recorded as an input in the
provenance, because a Dockerfile change alters the image without any corpus
change. And the context should carry ONLY what the Dockerfile copies: the
corpus roots are ~8 MB by the Dockerfile's own accounting, and it deliberately
omits `experiments/` (169 MB), so a lazy `cp -a` of a full checkout would send
a needlessly enormous context to the daemon.

**Whether this recipe runs at all** is not decided here. It is decided by the
input-revision predicate in Decision 10, which runs BEFORE step 1 — so on a
quiet night none of the five steps above happens.

### Decision 4 — The stage lives in `doc-health-reusable.yml`, not in a new workflow

A new top-level scheduled workflow would be the obvious alternative. Four
reasons against it.

1. **It needs the readiness machinery that already exists there.** The
   fail-closed runner-group + heartbeat evaluation, the `GROUP=` convention,
   `scripts/check-worker-readiness.py`, and the dispatch-label plumbing are all
   in that file, five times over. A second workflow would either duplicate them
   or drift from them.
2. **The singleton host must not be double-booked.** The aggregation's nightly
   caller already declares
   `concurrency: {group: xfactory-artifact-worker, cancel-in-progress: false}`
   with the comment "Shared with review-lane.yml because both dispatch the
   singleton artifact worker." A separate schedule would race the nightly for
   `cpc-omni01` unless it joined that group anyway — at which point it is the
   nightly's schedule with extra steps.
3. **It is downstream of the report delivery, and the ordering matters.** The
   refresh must not be able to jeopardise the report: the report is the
   program's daily record and the refresh is an optimisation of a serving
   surface. Ordering the stage after the delivery step inside the same job
   makes the dependency explicit and unbreakable. In a separate workflow the
   ordering would be a coincidence of two cron expressions.
4. **The reporting idiom is already there.** `git add health/` in the delivery
   step is what carries `lane-status.json` to the rolling PR today. A status
   artifact written by a stage in the same job rides that same commit —
   ALMOST. See Decision 6 for the one ordering subtlety this creates.

The counter-argument — that a long docker build lengthens the nightly's
critical path — is answered by the dispatch shape: the child runs on the worker
and the parent polls with a bounded wait, exactly as the five existing lanes
do. The nightly does not hold a docker build open.

### Decision 5 — Skip, never fall back

Worker absent, offline, busy, or heartbeat stale ⇒ the stage records a SKIP and
the nightly continues. There is no GitHub-hosted fallback path, and that is a
deliberate asymmetry with the semantic sweep, which DOES have an inline
fallback (`ANTHROPIC_API_KEY`, "used only when no omnigent worker host is
registered").

The asymmetry has a reason: what the fallback would need. The sweep's inline
fallback needs a model key. This lane's would need **registry push credentials
in a GitHub-hosted job** — a standing secret, in a runner nobody owns, able to
push to the registry the live QA cluster pulls from. That is a materially
different grant from a model key, and the whole shape of this change is that
artifact production stays on the host that already holds the registry binding.
A skipped refresh costs one day of snapshot freshness. A hosted push path costs
a standing credential forever.

The skip is also cheap by construction: tomorrow's run regenerates from
tomorrow's `main` and catches up in one hop. Nothing accumulates.

### Decision 6 — Observability, and the ordering wrinkle it creates

The lane writes `health/ideation-dashboard/refresh-status.json` — a sibling of
the existing `lane-status.json`, whose module already documents the pattern
("The lane-status artifact is diagnostic, not a projection") and whose failure
handling is the right precedent ("Its own failure must never take the [run]
down"). Fields: result (`ok` / `skipped` / `no_change` / `strict_failed`),
reason, the two Decision 10 input revisions each beside the recorded revision
it was compared against (so a `no_change` outcome names the revisions that
matched rather than merely asserting that nothing moved), the
`source_revision` the snapshot was generated at, the strict-validation counts,
the pushed tag and digest when a build occurred, and the PR reference when one
was opened.

**The wrinkle.** The delivery step that carries `health/` to the rolling PR runs
BEFORE this stage (Decision 4 puts the refresh after it, on purpose). So a
status file written after delivery lands in TOMORROW's report PR, one day late
— which is exactly the kind of quiet off-by-one that makes an observability
artifact worse than none.

Two acceptable resolutions, and the implementation must choose one explicitly
rather than let the ordering decide by accident:

- **(preferred) Write the status artifact and let it ride the NEXT delivery,
  and make the report section read the artifact that is present** — i.e. the
  report names the refresh outcome of the PREVIOUS run and says so in those
  words, the way a lane whose evidence lands on a one-run lag must. Honest, and
  needs no second delivery.
- **(alternative) Add a second, narrowly-scoped delivery** for
  `health/ideation-dashboard/refresh-status.json` only, after the stage. This
  costs a second rolling-PR interaction per night and must reuse the same
  force-free branch mechanics; it buys same-run reporting.

Either way the GitHub Actions run annotations (`::warning::` / `::notice::`)
carry the outcome in the run itself immediately, so nothing is invisible until
the report lands. What must never happen is a silent skip.

**A parked PR is also an observable.** If the shape check fails, or merge-master
declines, the PR sits open on a fixed branch — which the next night's run will
find and can report. That is a stronger signal than the status file: an open
`bot/dox-dashboard-pin` PR older than one day means the chain is stuck.

### Decision 7 — The rebake is the FALLBACK path, and the runtime-fetch gap is named, not hidden

The `ideation-dashboard` capability's promoted contract already rules against
using image rebuilds as the data path. "Delivery and regeneration": the served
plane "SHALL bake the APPLICATION — the renderer and its assets — and fetch its
DATA at runtime from that source, keeping a baked snapshot only as a first-boot
and offline fallback", with a scenario stating "an image rebuild MUST NOT be
required — rebuilds are for application changes." "Runtime snapshot fetch with
baked fallback and displayed freshness" says the same thing again and adds the
stale-banner rule.

A change that automates nightly rebuilds to refresh data must therefore say
carefully what it is and is not.

**What it is not:** a ruling that rebuilds are how published data reaches the
served plane. That rule stands, verbatim, in this change's MODIFIED delta.

**What it is:** a staleness bound on the artifacts the capability already
permits to be baked. Two of them, and the second is the one that makes this
lane permanently necessary rather than a stopgap:

- the baked SNAPSHOT, which the contract allows "as a FIRST-BOOT and OFFLINE
  fallback ONLY" — a fallback that is six weeks old is a bad fallback, and
  nothing in the promoted contract bounded its age;
- the baked `/source` CORPUS at `/srv/checkout/openxFactory`, which the runtime
  fetch does not cover at all. The runtime-fetch requirement is about the index
  and the snapshot. The document viewer reads a baked tree, so `/source` goes
  stale on the image's cadence no matter how fresh the fetched snapshot is —
  and a fresh snapshot over a stale corpus is the worse of the two failure
  modes, because every document that landed since the bake 404s.

**And the honest part.** The hosted image today does not do the runtime fetch at
all: its `CMD` passes `--snapshot /app/snapshot.json --checkout-root
/srv/checkout/openxFactory` and no data-source URL. So on the live plane the
baked artifacts ARE the data, and this lane's cadence IS the data cadence. That
is a conformance gap against a promoted requirement. This change does not close
it (that is a serving-side change to `serve.py` and the overlay, with its own
gate) and it must not paper over it either — the MODIFIED requirement states
the gap in the spec, so the next reader of the capability finds it recorded
rather than inferring from the Dockerfile that baking data is the design.

The corollary for the freshness header is worth stating: whatever the header
names, it must remain TRUE. Baking the snapshot and the corpus at one revision
(Decision 3) is what keeps it true — a header naming `source_revision` X while
`/source` serves revision Y would be a lie the viewer cannot detect.

### Decision 8 — Authority conservation, rung by rung

The end-to-end chain, and what each actor may do. The point is that no rung
gains anything.

| Actor | Act | Authority held | Authority NOT held |
| --- | --- | --- | --- |
| `cpc-omni01` worker | generate snapshot, build image, push to ACR | `write_artifacts`; a host-local push-scoped registry credential | no repository credential, no kubeconfig, no cluster access |
| `XFACTORY_APP` (lane identity) | open the digest-only pin PR | `contents: write` + `pull_requests: write` on Omnigent-Install | no registry access, no approval authority, no merge authority, no cluster access |
| merge-master App | submit ONE approving review inside the envelope | review-approval on the candidate class only | no merge call — it "never issues a merge call" |
| GitHub auto-merge | land the PR | the repository's own merge machinery | nothing outside the ruleset |
| in-cluster Flux | apply the merged overlay | the pre-existing `cluster-reconciler` binding | nothing new; the companion's own premise |

`execute_final_action` and `access_secrets` remain `const: false` in
`schemas/omnigent-domain-overlay.schema.yaml`. The worker's part of this lane is
artifact production — `write_artifacts` — which the matrix grants freely, and a
proposal, which is `propose_admission`. The companion's requirement "The worker
lane gains no apply authority and Flux gains no new authority" is a constraint
this change must satisfy, and the table is how it satisfies it.

**The one real new grant, and it is host-local.** The worker needs to PUSH to
`acropensoftxfactoryqa.azurecr.io`. Its manifest declares `acr_pull` only, and
the schema block is `additionalProperties: false` with
`required: [registry, token_vaultref]` — so a push credential cannot be
smuggled in as an extra field; it requires an Omnigent-Install schema delta
(an `acr_push` sibling block, or a scope field on the existing one). That delta
is Omnigent-Install's to author and is a blocking task here, not an assumption.

Two properties the credential must have regardless of which shape is chosen:
it is **push-scoped to the one repository** `ideation-dashboard` (not registry-
wide), and it is **delivered to the host by reference** the way every other
credential in that manifest is (`vaultref://kv-opensoft-xfactory-qa/...`,
reconciled by the Worker Host App), never handed to the model loop and never
written into the image or the job log. The distinction that keeps this
consistent with `access_secrets: false` is the one the manifest already
embodies: host substrate credentials are reconciled ONTO the host by the Worker
Host App; the worker AGENT does not fetch or read them. A push token in the
docker credential helper is the same class of fact as the `acr_pull` token that
is already there.

### Decision 9 — Staleness math

Under normal operation, with the nightly at `17 2 * * *` and the companion's
`dox` Kustomization on a 10-minute interval:

- corpus commits land on openxFactory `main` continuously;
- the lane reads `main` once per night, so the snapshot is at most **~24 h**
  behind `main` at generation time;
- the pin PR opens minutes later; merge-master evaluates once the shape check
  and the repository's other required checks conclude; auto-merge lands it;
- Flux reconciles within **≤ 10 min** of the merge (or immediately under an
  explicit `flux reconcile`);
- the Deployment rolls; the new pod serves the new baked artifacts.

So the served plane's baked data is **at most about one day plus one reconcile
interval plus one rollout** behind `main`. The bound degrades gracefully and
predictably: a skipped night makes it ~48 h; a parked PR holds it at whatever
the last landed pin was until a human looks. Neither failure mode serves WRONG
data — it serves OLD data, with a freshness header that says so, which is the
property the `ideation-dashboard` capability's stale-banner rule was written
for.

### Decision 10 — The no-change predicate is INPUT REVISIONS, evaluated before the build

An earlier draft of this design decided the no-change case by comparing the
digest the lane just built against the digest already pinned. That predicate is
**behaviorally defective and must not be built**, for a reason that only shows
up in production: the comparison can never find equality, so the short-circuit
would never fire, and the lane would pin and deploy content-equivalent images
every single night — precisely the churn the requirement's own rationale
forbids.

Two independent reasons, both on the IMAGE side:

1. **The build is not reproducible.** Every step of the recipe starts with a
   FRESH checkout (Decision 3 requires it), which stamps every file's
   modification time at checkout time.
   *(AMENDED 2026-09-01, pending re-ratification: read "a freshly materialized
   source tree" — under the sealed-artifact recipe the fresh tree is
   materialized by the parent and unpacked on the worker rather than cloned
   there. The mtime property the argument turns on is unchanged, and so is the
   conclusion.)* The `COPY` layers are tars of those
   files, so the layer bytes differ even when every file's CONTENT is
   identical, and the manifest digest moves with them.
2. **The base image floats.** The Dockerfile says `FROM python:3.12-slim` — a
   tag, not a digest — so a fresh pull can move the base layers independently
   of anything in this program.

**One correction worth recording, so nobody "fixes" this the wrong way later.**
The SNAPSHOT is not a source of this drift. `scripts/ideation_dashboard/`
`generator.py` derives `generation.generated_at` from the source revision's
committer date and says so in as many words — "the ONLY source of
`generated_at` — never the wall clock" — and the capability's determinism
property is that the same working tree yields a byte-identical snapshot. So
hashing the snapshot's CONTENT would be a sound comparand; it is simply
INSUFFICIENT, because it cannot see the second input. A Dockerfile change
alters the image with the corpus untouched, and a snapshot hash is blind to it.
That is the reason the predicate carries two revisions rather than one content
hash.

**The predicate.** The lane compares two INPUT revisions against the two
revisions recorded with the currently pinned image, and stops before doing
anything when both match:

- the **corpus input revision** — openxFactory, the revision the snapshot and
  the baked corpus roots would be generated from;
- the **build-recipe input revision** — Omnigent-Install, the revision the
  Dockerfile and build recipe would be read from.

**The scoping subtlety, which is the same defect wearing a different hat.**
These must be the revisions of the last commit touching each repository's BAKED
INPUTS, **not** the repositories' branch tips. Omnigent-Install `main` advances
for reasons that have nothing to do with this image — and, unavoidably, one of
those reasons is this lane's OWN merged pin commits. A tip-versus-tip
comparison would therefore make every landed pin guarantee that the next night
rebuilds, which reintroduces nightly churn through the other half of the
conjunction. The path-scoped form is cheap:

- corpus: `git log -1 --format=%H -- scripts/ideation_dashboard scripts/doc_health contracts docs examples ideation openspec templates`
  (exactly the paths the Dockerfile copies — which correctly ignores `tests/`
  and `experiments/`);
- recipe: `git log -1 --format=%H -- containers/ideation-dashboard`.

Whichever scoping a realization adopts must be RECORDED with the pin, so
consecutive runs compare like with like rather than silently changing the
question.

**Where the provenance lives: the overlay comment, authoritatively.** The pin's
own comment block inside the `images:` entry is the record; the PR body repeats
it for reviewers and is explicitly not the record the lane reads. Three
reasons:

1. **Precedent.** The current pin already carries exactly this fact in prose —
   "BAKED SNAPSHOT + /source corpus refreshed to openxFactory main @ 7ae4fe9,
   generated --strict from that same checkout" — written by hand, twice. This
   decision makes an existing habit machine-readable rather than inventing a
   store.
2. **It is in-repo state.** Reading it is a plain read of Omnigent-Install
   `main`. A merged pull request's body is not a queryable state store, and
   making the lane search merged PRs for its own last provenance would be
   archaeology where a `git show` suffices.
3. **It costs no envelope widening.** The companion's auto-merge scope already
   admits "digest line(s) and their comments" inside that block, so the
   provenance rides inside the shape that is already approved. Putting it
   anywhere else in the file would push the diff out of the envelope.

The one obligation this places on the implementation is a STABLE, parseable
key/value shape — not prose to be regex-guessed. Prose is what the humans
wrote; a lane that has to guess at its own provenance format will eventually
guess wrong and rebuild forever (or, worse, never).

**Bootstrap, stated explicitly.** Absent or unparseable provenance — today's
hand-pinned image, or any pin a human writes — is treated as CHANGED. The lane
builds once, and the pin it produces establishes the provenance every later run
reads. Failing OPEN here is deliberate: the cost is one redundant build, while
failing closed would leave a hand-pinned plane permanently unrefreshed, which
is the defect this whole change exists to remove.

**Digest comparison, demoted.** Retained at most as a defence-in-depth note on
a run that built anyway (a forced or manual run): an unchanged digest there is
a curiosity worth logging, never a trigger. Nothing in the contract may assert
built-digest equality as the predicate.

**And it is cheaper.** The check runs before the checkout, so a quiet night
costs two `git log` reads instead of a fresh clone, a snapshot generation, a
docker build and an ACR push. The correctness argument came first, but the cost
argument points the same way.

## Risks / Trade-offs

- **An automated write path into a live cluster's image supply.** Narrowed to
  one image repository, one overlay file, one digest line, one head branch, one
  author, gated by a repository-side line-level check, approved inside a
  reviewed envelope, revocable in one configuration edit. The residual risk is
  a well-formed digest of a bad image, whose blast radius is the companion's
  Decision 8: a stalled rollout with the old ReplicaSet still serving, undone by
  reverting the pin commit.
- **A nightly-churning `images:` block.** One digest commit per changed night.
  Accepted by the companion as "the audit trail", and mitigated here by the
  no-change short-circuit: quiet nights produce nothing.
- **`--strict` may be too strict to ever pass.** If `main` carries a standing
  snapshot WARNING, the lane never publishes and the plane silently stops being
  refreshed. Mitigated by Decision 6's visibility — a strict failure is a
  reported skip with the validator's own output in the status detail, not a
  silent no-op — and it is arguably the correct outcome: publishing a snapshot
  the validator objects to is how a bad projection reaches a shared surface.
  The realization must confirm `main` currently passes `--strict` before the
  lane is switched on.
- **The App gains write on an install repo.** `contents: write` +
  `pull_requests: write` on Omnigent-Install is a real widening of the content
  App's reach. Bounded by the fact that write on a branch is not write on
  `main` (the org ruleset still requires a PR), by the envelope confining what
  can auto-merge, and by Decision 2's recorded contingency if the widening is
  refused.
- **Merge Master must now be maintained in two repositories.** A second copy of
  the workflow and a second envelope instance is duplication, and duplication
  drifts. Mitigated by the decision core being a pinned shared checkout from
  codexFactory rather than copied logic — only the thin workflow wrapper and
  the config instance are duplicated. Worth revisiting if a third repository
  ever needs it.
- **The provenance record is now load-bearing, and it lives in a comment.**
  Decision 10 makes a YAML comment the state the lane reads, which is unusual
  and worth naming as a risk: a reformat, a hand-edit, or a comment rewritten
  in prose breaks the predicate. The failure mode is bounded in the safe
  direction — unparseable provenance means "changed", so the lane rebuilds
  rather than going silent — and it is mitigated by a stable key/value shape
  and by a test over the real overlay file. The alternative homes are worse:
  a merged PR body is not queryable, and a separate state file would sit
  outside the auto-merge envelope.
- **The two-revision trap is easy to reintroduce.** Any future edit that builds
  from the aggregation checkout instead of the fresh clone silently restores
  the stale-corpus bug, and the resulting image LOOKS fine. Mitigated by
  requiring the provenance to record both the snapshot's `source_revision` and
  the corpus revision, and by the requirement that they be equal — which makes
  the defect assertable rather than merely avoidable.
- **The status artifact's one-run lag** (Decision 6). Accepted as the preferred
  resolution, on condition the report says which run's outcome it is naming.

## Migration Plan

Ordered; `tasks.md` carries the executable form. Steps marked HUMAN GATE stop
for a human decision or execution.

1. Preflight, read-only: confirm `main` passes `--strict` today; confirm the
   `XFACTORY_APP` installation on Omnigent-Install with a real authenticated
   call; confirm `cpc-omni01`'s docker daemon and its registry binding; read
   the currently pinned `ideation-dashboard` digest AND its comment block, and
   record that the bootstrap pin carries no machine-readable provenance — so
   the first run is a Decision 10 bootstrap build by construction.
2. HUMAN GATE — the `acr_push` credential: rule the shape (Decision 8), land
   the Omnigent-Install schema + manifest delta, and reconcile the credential
   onto the host.
3. Build the artifact-only child workflow in the aggregation and prove the
   fresh-checkout recipe end-to-end by hand ON the worker, producing a real
   digest without opening any PR.
   *(AMENDED 2026-09-01, pending re-ratification: build the parent
   source-artifact step as well, and prove the SEALED-SOURCE recipe end to end
   on the worker — a real digest, no worker repository access, no PR.)*
4. Add the refresh stage to `doc-health-reusable.yml` behind the readiness gate,
   with the no-change short-circuit, in a mode that opens no PR (dry-run):
   prove the skip path, the strict-failure path, and the no-change path.
5. Land the Omnigent-Install side: the shape check, the merge-master workflow +
   envelope instance with the one candidate class, and the App bindings. This
   is the companion's task 7, now unblocked.
6. HUMAN GATE — enable PR authoring. First real pin PR is watched end to end.
7. Prove BOTH directions: a digest-only PR approved, auto-merged and reconciled;
   a deliberately wider diff from the same identity refused by the shape check
   and parked.
8. Close: report section, README records, strict validation, notify the
   companion that legs 1–2 are live.

## Open Questions

1. **The `acr_push` credential's shape.** A second scoped ACR token escrowed in
   Key Vault (the pattern `acr_pull` already uses, and what the schema comment
   calls the v1 decision), or the device-cert Entra credential that same comment
   calls v2. Recommendation: mirror `acr_pull` for v1 — a push-scoped token on
   the one image repository — and let the v2 migration move both together.
   Owned by Omnigent-Install; blocking for realization, not for this change's
   requirements.
2. **The approval trigger in Omnigent-Install.** In-repo `workflow_run` on the
   shape check (Decision 1's recommendation, no extra App permission) versus the
   cross-repo `gh workflow run` chain the aggregation proved (needs
   `actions: write`). Decidable only against observed behaviour on the first
   real PR; either satisfies the requirements.
3. **Same-run versus next-run refresh reporting** (Decision 6). The preferred
   resolution accepts a one-run lag with the report saying so; the alternative
   adds a second narrow delivery. A reviewer may fix the choice at
   ratification.
4. **Whether the other three surface images want the same lane.** `dox-auth`,
   `intent-inbox` and `dispatch-token-minter` bake no governed corpus and go
   stale only when their own code changes, so probably not — noted so the
   pattern is not copied by reflex, exactly as the companion noted the mirror
   question for its Kustomizations.
