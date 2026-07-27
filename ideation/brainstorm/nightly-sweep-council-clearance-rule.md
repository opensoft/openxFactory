# Nightly-Sweep Council Clearance: tier-2 rule for the doc-health rolling PR — Brainstorm

Status: brainstorm
Kind: process
Author: Brett Heap (concept: defaults let the council merge-or-not the nightly
sweep); drafted with Claude (session 2026-07-23)
Origin: human
Summary: Extends the ratified Merge Master autonomous-approval envelope
(`add-merge-master-autonomous-approval`, codexFactory) with a **tier-2
council-clearance path** for the nightly doc-health rolling PR: when the
conjunctive envelope fails on a condition in a declared *council-clearable*
set, the merge-readiness council (LQ/LS/LI) convenes and its unanimous
`ready` verdict — pinned to the exact head SHA — lets the Merge Master
approve; security-touching failures, check failures, and identity mismatches
are **never clearable** and park for the human as today. Includes an
anti-normalization rule (a condition cleared repeatedly stops being clearable
and parks with a fix-the-generator flag) and ships `configured_but_inactive`
behind an activation gate until council orchestration lands in the Omnigent
lane. Widening what auto-clears is a per-repo gate rule, so ratifying this is
the **Gate-Rules Council's first real exercise**.
Topics: codexfactory, merge-master, autonomous-approval, doc-health-sweep,
merge-readiness-council, gate-rules-council, auto-clear-envelope, tier-2,
nightly-sweep, omnigent-lane, activation-gate, cost-accountability
Repository context: codexFactory (envelope rules-as-code + per-repo gate rule); openxFactory (this leaf)
Captured: 2026-07-23
Updated: 2026-07-23 (Q1+Q4 decided; convening packet assembled; CONVENED —
rule ratified as amended, record at codexFactory
`hermes/domain/review-councils/records/2026-07-23-gate-rules-nightly-sweep-clearance.md`)

## Convened (2026-07-23)

The Gate-Rules Council's first exercise ran as a recorded manual rehearsal:
all seat verifications HOLD (LS floor verified against `envelope.py`, CSC
pull-in evaluated and not triggered; LA composition; CPL kill switch +
notices; project seat vacant-symbolic), with one **LQ amendment** — the
docs-class allowlist narrowed from `**/*.md` to
`["health/**", "docs/**/*.md", "README.md"]` (workflow contracts, openspec
records, and `hermes/` governed content are not docs-class). Q2 blessed:
lane-emitted PR check-run transport. **Rule v1 RATIFIED AS AMENDED**,
`configured_but_inactive`; Brett Heap's acknowledgement registered. The
rehearsal satisfies `first_convening_rehearsed_and_recorded`; the remaining
activation-gate requirement is council orchestration in the Omnigent lane.
Exit IMPLEMENTED 2026-07-23: codexFactory change
`add-nightly-sweep-council-clearance` — rule YAML + council_clearance.py
decision core (composes tier 1, envelope.py untouched) + 18 negative-suite
tests, all green, on main 8931ee2. Ships active: false (report-only).
Pending: ratification; archives after its parent
add-merge-master-autonomous-approval. Activation awaits council
orchestration in the Omnigent lane.

## Decided (2026-07-23)

- **Q1 — docs-class is a static allowlist, Lead Quality owns it.**
  Rules-as-code: `**/*.md` plus `health/**`; everything else — workflows,
  scripts, schemas, any YAML outside `health/**` — is NOT docs-class.
  Allowlist changes are Lead-Quality-accepted recorded events. Deterministic,
  auditable, no new code surface, no circularity.
- **Q4 — v1 clears docs-only overflow alone.**
  `dispositioned_regression_finding` is dropped from v1 (riskier, rarer);
  adding it later is a normal rule amendment through the same council. One
  crisp condition for the council's first exercise.

## Decided (2026-07-25)

- **Verdict-emitting identity is a DISTINCT lane identity, `checks: write`
  only** (Brett, 2026-07-25, at the `add-council-clearance-lane-wiring`
  proposal gate). Three-identity separation on the candidate PR: the
  content App authors, the lane identity emits the verdict check-run, the
  Merge Master App approves — no identity both produces evidence and
  consumes it for its own act. Reusing the content App was considered and
  set aside: the PR author emitting the clearance evidence for its own PR
  weakens the separation the envelope is built on.
- **Backing stack for rehearsal + initial active period** — DECIDED
  (Brett, 2026-07-26, option B): the live opensoft self-client QA stack
  (`hermes-opensoft-qa`) backs both the rehearsal and the initial active
  period. Conditions recorded with the decision: (1) a named migration
  trigger — the lane moves to a production-posture stack at P5 self-host
  landing OR at the first domain-layer reseed of the QA stack, whichever
  comes first; (2) a lane-side duplicate guard — the lane never
  commissions a convening for a head SHA that already carries a verdict
  check-run (protects the convene-at-most-once discipline against a
  reseed wiping the runtime's job ledger). Both conditions ride the
  `council_orchestration_available` attestation packet. Risk basis: the
  clearable set is docs-class overflow on the bot-authored nightly PR
  only — unanimous SHA-pinned verdict, independently re-judged by the
  tier-2 core, anti-normalization at 3, standing kill switch,
  per-clearance notice.

## Adversarial review findings (2026-07-26)

A 4-lens adversarial review of the landed lane wiring
(`add-council-clearance-lane-wiring`) confirmed two defects IN the wiring —
both fixed before any live leg, while the rule still ships `active: false`:

- **Verdict check-run was trusted by NAME only.** Any App with
  `checks: write` — including the content App that authors the candidate —
  could have forged a unanimous `ready` verdict and obtained a real
  approval once flipped, with no council convening; the forgery was
  self-protecting because the lane's convene and emit guards also matched
  on name alone, so a planted check-run made the genuine lane stand down.
  Fixed: the transport binds to the configured lane App id
  (`vars.COUNCIL_LANE_APP_ID`), a blessed name from any other identity
  parks as malformed, and both lane guards carry the same predicate.
- **The `neutral` conclusion self-blocked the clearance it certified.**
  Tier-1 `require_all_checks` demands every non-excluded check-run conclude
  `success`, so a genuine verdict made `_classify` return never-clearable.
  Fixed lane-side (conclusion `success`, verdict value in the title) —
  deliberately NOT by excluding the check in the tier-1 envelope, which the
  ratified rule forbids weakening.

**Flip-order precondition (not a defect — fail-closed by design):** the
consecutive-clearance count derives from the preceding merged nightlies'
approval reviews. Human approvals read as unknown, so today's history
yields `countable: false` → at-threshold → every candidate parks with the
fix-the-generator flag. Tier 2 therefore stays inert until tier-1's
merge-master App has autonomously approved at least one nightly. Verified
against the real module 2026-07-26. **The gate flip must follow tier-1
realization, not merely accompany it.**

Out of scope here, needing their own changes (tier-1 surfaces, pre-existing
since 2026-07-16 unless noted):

1. **Path gate reads a truncated file list** — `gh pr view --json files`
   caps at 100 with no pagination, so a >100-file candidate can have
   out-of-allowlist paths truncated out of `changed_paths` before the gate
   sees them. A health-report tree can plausibly exceed 100. **Fail-open;
   highest priority of these.**
2. **Open-findings gate fails OPEN on query error** (`|| echo '[]'`): an
   API failure reads as "no open regression finding".
3. **Approval token minted org-wide** (no `repositories:` scoping) inside a
   `pull_request_target` job.
4. **Floating `@main` pins**: the rule + decision core are pulled from
   `opensoft/codexFactory@main`, and the convening lane calls the reusable
   at `@main` while passing the lane App key and runtime token — the
   "base-branch pinned" property holds only for the envelope config. Needs
   a pinning policy (`review-lane.yml` SHA-pins as the house pattern).
5. **Rule binding unchecked**: the rule declares
   `repository: opensoft/codexFactory` while the candidate lives in
   `opensoft/xFactory`; `validate_rule` never reads the field. A council
   amendment should correct the text.

## Adversarial review — `add-changed-path-completeness` (2026-07-26)

Review of the landed combined diff (codexFactory `553826b` core precondition
+ aggregation `b0e86ef` gathers) before ratification, because the last review
of this surface found a critical fail-open. **No fail-open found in the
change itself.** Items 1 and 2 of the out-of-scope list above are closed by
it.

Verified by execution, not assertion: aggregation `pytest tests/` 44 passed /
25 subtests and `actionlint` exit 0 on both workflows; codexFactory
`pytest tests/merge-master/` at `c43151e` 128 passed / 5 skipped. The
never-clearable property holds by construction — `_classify` returns early on
`failed_condition != "path_allowlist"` (council_clearance.py:152) and the
precondition sits between the expected-base block and condition 2
(envelope.py:356-400), so an unproven set can never be reported as a path
failure. `changed_paths` has no third consumer: only `envelope.evaluate` and
`_classify`, and `_classify` is unreachable until completeness has passed.
The shipped jq was run directly against edge fixtures the suite does not
cover — zero-file PR, null / empty-string / non-string `previous_filename`,
duplicate filenames, rename cycles, an absent `changed_files`, a string
total — and every case is fail-closed or benign.

What the review DID find, all in the same fail-open class the change exists
to close, none of it introduced by the change. **Findings 1–3 were FIXED
inside this change** (Brett's ruling: fix the gathers now and ratify text and
code together, rather than narrow the requirement) — codexFactory `841ab26`,
aggregation `af5b89d`, pin `bd52fba`, recorded as tasks §4. Findings 4 and 5
remain open. **The change was then ratified and archived on 2026-07-26**
(codexFactory `da10584`,
`openspec/changes/archive/2026-07-26-add-changed-path-completeness`); its
spec delta archived WITH it rather than folding into `openspec/specs/`,
since `merge-master-approval` stays unpromoted while the parent's task 7.4
is blocked.

1. **The commit-statuses gather is unpaginated** —
   `gh api "repos/$REPO/commits/$HEAD_SHA/status"` carries no `--paginate`
   and no `per_page`, two lines below a sibling check-runs call that does
   paginate, inside the block this change rewrote. The combined-status
   endpoint pages at 30. `_checks_green` quantifies universally over
   `facts.statuses` and fails closed only when the considered count is zero,
   so a failing legacy status past entry 30 is invisible and all-checks-green
   reports satisfied. Latent, not live: the candidate head carries zero
   legacy statuses today (the repo uses check-runs). The endpoint returns
   `total_count`, so the exact proof this change invented for changed paths
   is available here for the price of one comparison.
2. **Neither the check-runs nor the statuses gather carries a completeness
   proof.** The change's own principle — a fact set the envelope quantifies
   over must not be accepted without proof that it is whole — is applied to
   changed paths alone. Both responses carry `total_count`. This is also a
   spec/realization mismatch worth settling at ratification: the fourth
   ADDED requirement is titled *"Every gather feeding an approval decision
   proves completeness the same way"*, but its scenarios pin only the two
   workflow SURFACES, so `--strict` passes while the title promises more
   than the code delivers. Either narrow the requirement to "every workflow
   surface" or extend the discipline to these two gathers.
3. **The open-findings window is still a truncating client-side filter.**
   `gh issue list --limit 200` truncates with no total, and the notice
   exclusion runs after the fetch, so the workflow's own per-clearance
   notices — filed as open issues and never closed, and unlabelled on the
   fallback path — consume window slots. An absent finding reads as "no
   blocking finding". Zero exposure today (1 open issue), saturating in
   ~200 clearances once tier 2 is active. Server-side exclusion via
   `--search "-label:<notice>"` plus a count cross-check closes it.
4. **Candidate resolution masks failure with the idiom the change removed**,
   two lines above the gather block and therefore outside the no-masking
   test's window: `mapfile -t HEAD_REFS < <(python3 "$CORE" …)` cannot see a
   core that is absent or throwing (`set -e` does not observe process
   substitution) and `n="$(gh pr list … || true)"` reads an API failure as
   "no open PR". Both yield `decision=skip` on a green run. Not a security
   fail-open — no approval is granted — but the nightly can silently stop
   being evaluated with no operator signal, which matters precisely because
   the core is pulled from a floating `@main` (item 4 above).
5. **Informational.** (a) `echo "reason=$REASON"` puts a string that can
   embed a changed path into `GITHUB_OUTPUT` unescaped; git permits newlines
   in filenames, so a crafted path can inject further `key=value` lines. Not
   exploitable for approval — `decision=` is written after `reason=` and the
   last write wins, and a malformed output file fails the step — and it
   presupposes an already-compromised generator. The heredoc-delimiter form
   is the fix when the file is next touched. (b) The convening lane
   commissions `resolve.outputs.head_sha`, read before the classify step's
   gather and never compared against the SHA that step settles on, so the
   new recheck does not cover the gap between the two jobs' reads; downstream
   SHA binding makes the worst case a wasted convening. (c) The head-SHA
   recheck cannot see base-branch movement, which also changes the diff —
   exploiting it needs push access to `main`.

**Fix as landed (findings 1–3).** Both listings now paginate at
`per_page=100` with `--paginate --slurp` and carry the `total_count` each
endpoint declares for itself; the core requires `check_runs_total` /
`check_runs_entry_count` and `statuses_total` / `statuses_entry_count` and
parks under a new `check_facts_incomplete`. That precondition is ordered
ahead of the PATH condition, not merely ahead of the check condition, because
`_classify` re-runs `_checks_green` and `_open_finding` over the same facts
when it admits a `path_allowlist` park — the identical re-derivation trap the
changed-path ordering exists to prevent, and it is proven by test, not
assumed. The open-findings window is gone rather than widened: exhaustive
pagination of `repos/{repo}/issues?state=open` (no issues endpoint declares a
total, so exhaustion is the proof) with pull requests dropped and the notice
exclusion applied to the complete set. Requirement 4's title, which promised
"every gather" while its scenarios pinned only the two surfaces, is retitled
to what it governs and a new requirement states the per-listing discipline —
so what Brett ratifies says exactly what the code does. Verified live before
designing it: `check-runs?per_page=1 --paginate --slurp` over a real PR head
gave 3 pages, `total_count` 3 on each, 3 entries. No commit in these
repositories carries a legacy status, so the status listing is verified
structurally; that caveat is recorded in-file, and a wrong assumption parks
with both counts named rather than approving. Interop re-verified by
execution: the live nightly still approves, 30-of-137 statuses parks, and a
docs-only overflow with short statuses parks never-clearably instead of
reaching tier 2.

Two deviations beyond brief in `b0e86ef`, both defensible and documented
in-file, flagged for the ratification decision: the `|| echo '[]'` removal
was extended past open-findings to the check-runs and statuses gathers; and
the pull-request resource is read twice (once in full, once for
`-q .user.login`) because the harness asserts that exact literal call.
Relatedly `.head | .sha` is spelled that way deliberately — the harness
asserts the literal `head.sha` is absent — so neither should be "tidied".

## Registered (2026-07-26) — lane identity + federated runtime credential

Brett completed the council-lane registration per codexFactory
`docs/council-lane-app-registration.md` (through v3, `a99567a`): lane GitHub
App installed on `opensoft/xFactory` (`checks: write` only), all six
variables and both secrets set, no `HERMES_RUNTIME_TOKEN` secret (the lane
federates per run, `eddf960`). Brett's admin AI then ran the federation
diagnosis (session artifact
`xFactory/council-lane-federation-diagnosis-prompt.md`) against the Entra
side and reported:

- **All pass**: Hermes resource app emits v2 tokens (issuer/audience match
  the pins); the lane identity holds app roles `hermes.job.execute` AND
  `hermes.job.read`, no client secret/certificate; federated credentials for
  `repo:opensoft/xFactory:ref:refs/heads/main` and a
  `job_workflow_ref`-shaped subject for `council-lane-reusable.yml@main`;
  `id-token: write` granted.
- **One blocking defect, FIXED by the admin AI 2026-07-26**: the Entra
  claims-mapping policy (`hermes-layer-claim`,
  `ef0259cb-6f9e-4dfc-823b-03611dbd39b2`) emitted `JwtClaimType: "layer"`,
  but the aks-qa overlay pins the layer claim name as the flat key
  `extn.layer` — Hermes reads the literal `extn.layer` key, so every token
  would have 401'd despite correct federation and roles. Changed to
  `extn.layer`, value `codexfactory-software-engineering`, policy still
  assigned to the `opensoft-hermes-qa` service principal,
  `acceptMappedClaims` enabled.

**Not yet proven** (this is lane-wiring task 5.1, the recorded rehearsal):
no live dispatch has run, so no federated token has actually been exchanged
and accepted end to end. Two preconditions the diagnosis did NOT cover,
both lane-side facts outside the admin AI's view:

1. The clearability preflight REFUSES a healthy nightly (`tier1_approve` —
   nothing to convene). The rehearsal candidate must park under
   `path_allowlist` with docs-class-only overflow (rule inactive is fine:
   the preflight accepts `report_only` + would-be-clearable).
2. The QA stack's domain layer must carry materialized `review_council`
   content naming `merge_readiness_council` — commission is admitted
   fail-closed against it before any write (runbook §5). Unverified as of
   this record.

**Stage-1 federation test (2026-07-26, runs 30200808815 / 30200918192,
emit-only against PR #29 — read-only by construction, nothing written).**
The `Federate a Hermes runtime token` step succeeded on both runs: assertion
minted, Entra exchange accepted, token issued — the GitHub→Entra path is
PROVEN live. Hermes then answered the job-list read with **HTTP 403
`authz.cross_layer_denied`** (surfaced by the diagnostic patch codexFactory
`9e62a38`, which makes the lane's runtime-read warnings name the runtime's
own error code). That code is precise: 401 would be token validation
(issuer/audience/signature), and `authz.insufficient_scope` would fire
FIRST — `require_scope` is a dependency ahead of the handler's layer check —
so the token validates AND carries `hermes.job.read`. The ONLY remaining
defect is the layer claim: `extn.layer` is absent from the emitted token or
carries the wrong value, despite the claims-mapping policy fix. Back with
Brett's admin AI: verify what the emitted token actually carries (the
out-of-band decode is now justified), checking Entra propagation lag first;
fallbacks if a dotted literal `JwtClaimType` won't emit are the
directory-extension optional-claim route (lands natively as `extn.<name>`)
or, last resort, re-pointing the overlay's `oidc_layer_claim` (config
change + redeploy). `hermes.job.execute` remains unproven until a commission
runs (stage 2).

**Refined root cause (admin AI, 2026-07-26, decoded real token).** The
emitted token carries `iss`/`aud`/`ver: 2.0` correct and BOTH roles
(`hermes.job.execute` too — so stage 2's scope is already proven present),
but neither `extn.layer` nor `layer`. The claims-mapping policy
(`Source: "application"`, `ExtensionID: extension_9783…_layer`,
`JwtClaimType: "extn.layer"`) reads the client SERVICE PRINCIPAL, while the
extension value sits on the lane APPLICATION object — no source value, claim
omitted. Meanwhile the native path is already fully configured (directory
extension `layer` exists, value on the lane application object, Hermes
resource app requests it as an access-token optional claim, which v2 emits
as `extn.<name>`) — but the ASSIGNED claims-mapping policy supersedes it.
Next test: unassign (not delete) `hermes-layer-claim` from the
`opensoft-hermes-qa` service principal and let the native optional-claim
path emit. Safe by the decode itself: the policy currently contributes zero
claims, so unassigning it cannot remove anything any client receives; and
Hermes-side principals persisted with a DB `layer_id` are unaffected either
way (`security.py` falls back to the persisted row when the token carries no
layer claim). Both temporary decode credentials deleted; lane-app password
count 0.

**Unassign tested (2026-07-26 12:29Z): native path ALSO empty — same
mismatch, second mechanism.** Policy unassigned reversibly (Graph `$ref`
delete; object intact); two decodes (12:30Z, 12:33Z) still carry both roles
and no layer claim in either spelling. Confirmed cause: the directory
extension value sits on application object `b63f2641…` and is ABSENT from
service principal `037eb659…` — and the app-only optional-claims path reads
the SP, which is the very object the token's `sub` names. Next targeted
change (approved): set
`extension_9783ac18e5c74b9dbd762e6d7d89d5be_layer =
codexfactory-software-engineering` on SP `037eb659…`, decode, and only then
re-dispatch the emit-only test. Wrinkle to check if the PATCH is refused:
the extension definition's `targetObjects` must include `ServicePrincipal`
(a definition created for `Application` only rejects SP writes — the fix is
widening the definition, not another mechanism). Policy stays unassigned
(provably contributed nothing, suppressed the native path). Credentials
again at zero.

**Dead end confirmed, design settled (2026-07-26).** Graph does not support
directory extensions on ServicePrincipal objects (SP PATCH refused;
`targetObjects` widening refused as an invalid value) — so an app-only token
for this lane structurally CANNOT carry a per-client `extn.layer` claim by
any of the three mechanisms tried (claims-mapping, native optional claims,
SP extension). A static-value transformation was ruled out deliberately: it
stamps every token the resource issues, and claims take precedence over
persisted rows, so it would mis-scope every other principal. The fix is
Hermes's own designed-in fallback (`claims.layer_id or persisted.layer_id`):
ONE persisted principal row keyed by the token's `sub` (the lane SP object
id `037eb659…`), `layer_id codexfactory-software-engineering`, kind
`service`, scopes empty (scopes always come from the token's `roles`, which
three decodes proved carry BOTH job scopes). Exact SQL now in the runbook
(codexFactory `39f6795`); the row is operational state — survives a domain
reseed, needs re-inserting on a database rebuild, so it rides the
stack-migration checklist. Entra side is FINAL: policy permanently
unassigned, no lane credentials, nothing further for the admin AI. Remaining
for stage 1: Brett inserts the row (psql, phase-1 runbook pattern) and the
emit-only test re-dispatches — no Entra propagation involved, the row is
read live.

**STAGE 1 CLOSED (2026-07-26, run 30206131600).** The principal row was
inserted on the QA stack by Brett's admin AI (preflights all PASS,
transaction-verified, count 5→6, via the managed AKS command channel, no
DSN displayed, nothing else touched). The immediate emit-only re-dispatch
concluded `success` with the single clean notice "no
merge_readiness_council convening found — nothing to emit": NO 403, no
warning. A federated token now clears every gate live — GitHub assertion,
Entra exchange, Hermes issuer/audience validation, both job scopes from
`roles`, and the layer from the persisted row. The credential path for the
lane is DONE end to end. Remaining before the recorded rehearsal (task
5.1): verify the QA stack's materialized `review_council` content names
`merge_readiness_council`, and stage a candidate that parks under
`path_allowlist` with docs-class-only overflow (a healthy nightly refuses
as `tier1_approve`). Stage 2 also gives `hermes.job.execute` its first live
exercise (already proven present in the token by decode).

**Stage 2 commissioned (2026-07-26, run 30207122387).** Candidate staged:
README one-liner on `doc-health/nightly` (docs-class overflow), pin
`27c3221`. En route, TWO findings fixed/observed: (a) SonarCloud's automatic
analysis attaches NO check-run to a diff without analyzable code, so a
docs-only head reads fail-closed "absent" forever — closed by adding the
repo's first PR CI (`validate.yml`, aggregation `6d8d99f`: the same
pytest+actionlint gates the discipline runs locally, job id `validate`,
non-excluded); (b) the auto-triggered tier-1 evaluation on the staged head
parked with the classifier ADMITTING the docs-only overflow and refusing
only on checks-absent — the ordering evidence, free. With `validate` green,
the lane preflight classified clearable and the runtime ADMITTED THE FIRST
LIVE CONVENING: `CONVENE-27c32213aced-30207122387`, HTTP 201. Observed fact
to chase later: the job landed `queued`, NOT `awaiting_authorization` — the
tenant auto-clear envelope gate (governed-job P2) did not engage, meaning
`tenant_auto_clear_envelope` found no materialized `policy_override` on the
client layer (phase-3a reseeded the client layer with "3 kinds"; whether
policy_override is among them needs checking — recorded as an open question,
not a rehearsal blocker; it removes the authorize step). Emit half correctly
emitted nothing on a queued convening. Next: the operator-relayed worker leg
(claim → run → conforming verdict), prompt prepared at
`xFactory/council-lane-rehearsal-worker-prompt.md` — the rehearsal worker is
the lane identity with a temporary `hermes.worker.write` role + temporary
secret (its tokens inherit the persisted-row layer binding), both removed in
cleanup. Then emit-only re-dispatch, tier-2 report-only evidence, dated
record, attestation packet.

**CORRECTION + BLOCKED (2026-07-27, worker-leg attempt).** The "first live
convening" claim above is WITHDRAWN: the admin AI's worker leg reached the
claim step and got route-level 404s, and its Step-1 read shows the job's
envelope carries NO runtime `convening` stamp and no provenance — the
deployed QA image (`ghcr.io/opensoft/xfactory-hermes-install:0.1.0`)
predates BOTH `add-worker-claim-loop` (claim route, 2026-07-24) and
`add-council-orchestration` (admission/stamping/verdict conformance,
2026-07-25). Yesterday's HTTP 201 was an ORDINARY job insert with the
`council_convening` block riding along unvalidated, and the `queued`-not-
`awaiting_authorization` observation is likewise just the old image
predating the governed-job P2 gate — that open question is RESOLVED
(no missing tenant content implied). Rehearsal state: worker
`council-rehearsal-worker-2026-07-26` registered (kept, audit trail);
no claim, no run, no verdict, no GitHub dispatch; Entra temporaries
cleaned to zero both attempts. En route the QA upstream also threw a
~5-minute nginx 503 (00:23–00:28Z, recovered alone — spot-pool posture).

**REHEARSAL COMPLETE (2026-07-27) — task 5.1 + 5.2 DONE.** The upgrade
unblocked it the same night: QA moved to image `6faa15d9` (built from
hermes-install `a9bc7b3`; backup + zero migrations + health gate, no
rollback), the recommission produced `CONVENE-27c32213aced-30232705131`
(admitted + provenance-stamped, `awaiting_authorization` — the P2 gate
engaged, retro-confirming the tenant envelope was materialized all along),
the operator-relayed worker leg auto-cleared/claimed/resolved it with a
unanimous-ready verdict through the runtime's conformance checks, the lane
emitted `council-verdict/merge-readiness` `success` on pin `27c3221` under
App 4397053 (== the configured identity), and the tier-2 report-only run
parked "would be council-clearable" byte-identical to tier 1. Dated record +
attestation packet: codexFactory
`hermes/domain/review-councils/records/2026-07-27-merge-readiness-lane-rehearsal.md`
(`9d6876c`). Lane-wiring tasks now open: 6.2 only (archive ordering). The
flip-order precondition STANDS: tier 2 stays inert until the merge-master
App bot-approves ≥1 nightly — the flip and the attestation are Brett's
recorded events. Historical note below kept as written:

**Was blocked on: upgrading the QA stack to a current hermes-install image**
(`docs/runbooks/upgrade.md`, `hermes-lifecycle upgrade`: correlated backup →
compatibility → migrations → health gate; 30-min operator budget; needs a
new image digest built from hermes-install main and a target runtime
manifest — Brett's operator leg, same surface as phases 1–3). After the
upgrade: the stale convening job does NOT block recommission
(`find_convening` matches the runtime `convening` stamp, which the stale job
lacks); the nightly will have moved the head, but the README overflow
persists in the branch so every future head of PR #29 remains a
docs-class-overflow candidate — recommission against the then-current pin
with a green non-excluded check on it (`validate` fires only on
human/App-authored pushes; SonarCloud covers nightly heads).

## The two tiers

- **Tier 1 (exists, ratified 2026-07-16):** the rules-as-code envelope
  auto-approves when ALL hold — content-App author, `doc-health/nightly`
  head ref, paths ⊆ `health/**`, all required checks green, no open
  regression finding. No council; deliberation on the happy path would fail
  the efficiency audit.
- **Tier 2 (this rule):** envelope fails → classify the failing conditions;
  if every failure is in the council-clearable set, convene the
  merge-readiness council instead of parking straight to the human.

## Draft rule (the ratifiable artifact)

```yaml
schema_version: 1
kind: per_repo_gate_rule
rule:
  id: nightly-sweep-council-clearance
  repository: opensoft/codexFactory
  applies_to:
    pr_class: doc-health-nightly-rolling      # tier-1 envelope's subject, unchanged
  default_state: configured_but_inactive      # activation gate below
  tier_1: merge_master_autonomous_envelope    # unchanged; this rule NEVER weakens it

  council_clearable:                          # closed, declared list — nothing else (v1)
    - id: docs_only_path_overflow
      condition: paths exceed health/** but every changed path is docs-class
      docs_class:                             # DECIDED: static allowlist, no classifier
        allowlist: ["health/**", "docs/**/*.md", "README.md"]   # as amended at the convening
        everything_else: not_docs_class       # workflows, scripts, schemas, YAML outside health/**
        owner: lead-quality                   # allowlist changes = Lead-accepted recorded
      council_verifies: no behavioral or config surface touched

  deferred_amendments:                        # NOT in v1; normal rule amendment later
    - id: dispositioned_regression_finding
      note: riskier and rarer; propose through the same council when wanted

  never_clearable:                            # always park for the human
    - author_or_app_identity_mismatch         # identity stays hard — spoofing surface
    - head_ref_mismatch
    - any_required_check_failed               # checks are the enforceability floor
    - secret_scan_finding
    - security_touching_path                  # CI config, workflows, dependency
                                              # manifests, scripts/ — CSC/LS territory
    - gate_weakening_change                   # council_large territory, never tier-2

  council:
    body: merge_readiness_council             # LQ / LS / LI (change B object)
    quorum: all_seats                         # missing seat => REFUSED => park
    verdict_required: ready_unanimous         # split => park (council semantics)
    undispositioned_conditions: zero
    pinned_to: head_sha                       # any new push invalidates the verdict
    convene_at_most: once_per_head_sha        # spend discipline; convening clocks in

  anti_normalization:                         # deviance must not become the default
    same_condition_cleared_consecutively: 3   # nights
    then: park_with_fix_the_generator_flag    # stop clearing; fix the sweep instead;
                                              # efficiency-audit signal recorded

  human:
    step: acknowledgement_of_notice           # non-blocking notice per tier-2 clearance
    kill_switch: standing                     # the human can disable tier-2 at any time

  activation_gate:                            # inert until the lane can convene councils
    requires:
      - council_orchestration_available       # Omnigent-lane execution of council mixes
      - first_convening_rehearsed_and_recorded
    until_then: envelope_failure_parks_for_human   # exactly today's behavior
```

## Why this shape

- **Councils advise; the lever stays mechanical.** The council's `ready` is a
  recommendation record; the Merge Master still executes approval, checking
  the record's SHA pin and TTL like any other envelope condition. No persona
  and no council ever holds the merge lever (repository_owns:
  final_merge_enforcement).
- **Never-clearable is the security floor.** Identity, checks, secrets, and
  security-touching paths stay hard — so the CSC conjunction pull-in is not
  triggered by this rule (it widens nothing security-posture-shaped); noted
  explicitly so the gate-rules convening can verify that claim rather than
  assume it.
- **Anti-normalization** is the piece rules-as-code alone can't express: a
  clearance that recurs is not an exception, it's a defect in the sweep — the
  third consecutive clearance of the same condition parks the PR and flags
  the generator for a fix (feeds `efficiency_finding` in domain memory).
- **configured_but_inactive** mirrors the liaison pattern: ratify the rule
  now, activate when the Omnigent lane can actually convene the council;
  until then behavior is byte-identical to today.

## Governance path (exit)

1. **Gate-Rules Council first exercise:** domain seats LA/LS/LQ, client seat
   company-policy-lead (CSC pull-in explicitly evaluated and — per the
   never-clearable floor — not triggered), project seat = intent-owner slot
   (symbolic), **Brett's acknowledgement** as the human step. The convening
   itself can be run as a manual/rehearsed exercise before orchestration
   exists — its output is this rule ratified.
2. **codexFactory OpenSpec change** extending the merge-master capability:
   the rule record + the envelope.py rules-as-code for tier-2 classification
   and the recommendation-record check, tests mirroring the envelope's
   existing negative suite, `default_state: configured_but_inactive`.
3. **Activation** rides the Omnigent-lane council-orchestration increment;
   flipping the gate is a Lead-accepted recorded event once its two
   requirements hold.

## Convening packet (Gate-Rules Council first exercise — rehearsal)

Everything the seats need in one sitting; the human step is Brett's
acknowledgement.

1. **The rule** — the v1 YAML above (docs-only overflow, static allowlist,
   never-clearable floor, unanimous SHA-pinned verdict, once-per-SHA,
   anti-normalization at 3, kill switch, configured_but_inactive).
2. **Verification claims for the seats to check, not assume:**
   - *Lead Security:* the never-clearable floor covers every security
     surface (identity, checks, secrets, security-touching paths, gate
     weakening) — therefore the rule widens nothing security-posture-shaped
     and the **CSC conjunction pull-in is not triggered** (evaluated on the
     record, not waved through).
   - *Lead Quality:* the docs-class allowlist is deterministic and owned;
     the anti-normalization threshold turns recurring clearances into
     generator fixes (evidence before trust holds).
   - *Lead Architect:* tier-2 composes with tier-1 without weakening it;
     the council output is a recommendation, the Merge Master remains the
     only approver, repository enforcement stays final.
   - *Company Policy Lead:* "is this allowed here" — the tenant accepts an
     agent council clearing a docs-maintenance exception class with a
     standing kill switch and per-clearance notices.
   - *Project seat (intent-owner, symbolic):* recorded as vacant-symbolic;
     binds when the subject-layer roster lands.
3. **Q2 recommendation carried into the convening:** verdict transport as a
   **PR check-run emitted by the lane** — already SHA-bound, visible in the
   PR, and the Merge Master App already reads check state; the alternative
   (governed record the App queries) adds an API surface. Council blesses
   or redirects.
4. **Output:** the ratified `per_repo_gate_rules` record + Brett's
   acknowledgement notice → then the codexFactory OpenSpec change
   (envelope.py tier-2 classification + recommendation-record check +
   negative tests, shipped configured_but_inactive).

## Open questions

- ~~docs-class definition~~ — DECIDED 2026-07-23: static allowlist, Lead
  Quality owns (§Decided).
- **Recommendation-record transport** — recommendation in the convening
  packet (check-run emitted by the lane); the council blesses or redirects.
- **Notice fatigue** — deferred to activation-gate time, informed by real
  clearance counts (anti-normalization bounds the worst case anyway).
- ~~v1 scope~~ — DECIDED 2026-07-23: docs-only overflow alone;
  `dispositioned_regression_finding` is a deferred amendment (§Decided).
