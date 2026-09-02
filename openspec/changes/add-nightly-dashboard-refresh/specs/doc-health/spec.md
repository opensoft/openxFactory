# doc-health

## ADDED Requirements

### Requirement: Ideation-dashboard image refresh lane
The nightly doc-health run SHALL include an ideation-dashboard IMAGE REFRESH lane, ordered AFTER the deterministic pass, the existing ideation-dashboard snapshot lane, and the report delivery step, so a refresh can never jeopardise the report it follows. The lane SHALL execute on the Omnigent artifact worker as a dispatched artifact-only child, following the same execution split and bounded-worker pattern as the agentic semantic sweep, the document-cataloger lane, the ideation-readiness lane and the possibles-derivation lane. Its work runs ONLY after the input-revision check of the no-change requirement below has found movement — the check precedes source materialization, so a quiet night costs two revision reads rather than a bundle, build and push. The credentialed hosted parent SHALL then materialize fresh openxFactory `main` (never the aggregation's submodule pin) plus the Omnigent-Install recipe at ITS `main` into a bounded sealed source artifact carrying the source HEAD, source committer timestamp, and both path-scoped input revisions. The credential-free child SHALL verify and download that artifact, generate the snapshot from THAT SAME corpus tree under `--strict` using the manifest-pinned source revision and timestamp, build from the bundled Dockerfile with the assembled workspace shape as context, push to `acropensoftxfactoryqa.azurecr.io` under a date-stamped tag, and capture the resulting digest as its only result. The worker SHALL perform no repository clone, fetch, or push.

`--strict` SHALL be the publication gate and MUST precede the push: a snapshot the validator rejects, or one the validator could not be run against at all, SHALL fail the lane with NOTHING published — no tag, no pushed image, no digest, no pull request. The lane SHALL add no deterministic check family and MUST NOT affect deterministic results.

#### Scenario: The lane runs on a night with corpus movement
- **WHEN** the report has been delivered and the worker is ready
- **THEN** the credentialed parent seals fresh openxFactory `main` plus the current recipe into a bounded source artifact, and the worker verifies it, generates the snapshot under `--strict`, builds the image from that assembled context, pushes it under a date-stamped tag, and records the resulting digest
- **AND** the snapshot's `source_revision` and the baked corpus revision MUST be the same commit

#### Scenario: Strict validation fails
- **WHEN** snapshot generation reports any error or any warning under `--strict`, or the validator cannot be run
- **THEN** the lane MUST publish nothing — no tag, no push, no digest, no pull request — and MUST record the failure with the validator's own output
- **AND** the deterministic results and the delivered report MUST be unaffected

#### Scenario: The sealed source artifact is unavailable or invalid
- **WHEN** the child cannot download the source run's named artifact, its manifest is malformed, a required path is absent, or its recorded revisions do not match the parent decision
- **THEN** the child MUST fail before strict generation and before any registry credential is used
- **AND** no repository fallback, host clone, image push, digest, or pull request MUST occur

#### Scenario: The lane builds from the wrong tree
- **WHEN** any realization would build from the aggregation's `openxFactory` submodule pin, or bake the committed snapshot alongside a freshly checked-out corpus
- **THEN** it MUST be rejected — the snapshot and the baked corpus MUST come from one checkout at one revision, because a snapshot whose `source_revision` names a commit the baked `/source` tree does not carry makes the served plane's freshness header untrue

### Requirement: The refresh lane skips when its worker is unavailable and never falls back to a hosted runner
The refresh lane SHALL be gated by the same fail-closed readiness evaluation the nightly's other worker lanes use — runner-group membership in the restricted artifact-worker group plus a matching authenticated heartbeat within the configured maximum age — and an unready worker SHALL record the lane as SKIPPED while the run continues. There MUST be NO inline fallback on a GitHub-hosted runner for this lane, deliberately and by contrast with the semantic sweep's model-key fallback: the image build and the registry push belong to the worker host that already holds the registry binding, and a hosted fallback would require standing push credentials in a runner the program does not own. A skipped refresh SHALL cost one cycle of served-plane freshness and nothing else, because the next run regenerates from the then-current `main` and catches up in one hop.

#### Scenario: No eligible worker is online
- **WHEN** readiness finds no eligible online runner in the restricted group, or the heartbeat is missing, malformed, or older than the configured maximum age
- **THEN** the lane MUST be recorded as skipped with the reason, and the nightly MUST continue
- **AND** no image is built, no image is pushed, and no pull request is opened

#### Scenario: A hosted fallback is proposed
- **WHEN** any proposal would build or push the dashboard image from a GitHub-hosted runner, or place registry push credentials in a hosted job, so that the refresh survives an unavailable worker
- **THEN** it MUST be rejected — the skip is the designed outcome, and a standing hosted push credential is a permanent cost paid for a one-cycle benefit

#### Scenario: A skipped cycle is followed by a normal one
- **WHEN** the lane skipped on the previous run and the worker is ready on this one
- **THEN** this run MUST regenerate from the current `main` and produce a single up-to-date artifact
- **AND** nothing from the skipped cycle MUST need replaying

### Requirement: A refresh that changes nothing proposes nothing
The refresh lane MUST decide whether to refresh by comparing its INPUT REVISIONS BEFORE it builds anything, and MUST stop when the inputs have not moved: no checkout, no snapshot generation, no image build, no registry push, no branch, no pull request, no approval, no deploy. Every pin the lane produces SHALL therefore RECORD the provenance the next run needs to make that comparison — the revision of the corpus repository the snapshot and baked corpus were generated from, and the revision of the served plane's repository the Dockerfile and build recipe were read from — and the AUTHORITATIVE location for that record SHALL be the pin's own comment block inside the `images:` entry of the overlay, in a stable machine-readable key/value shape rather than prose to be pattern-guessed. The overlay is authoritative because it is in-repo state readable with a plain read of the served plane's default branch, needing no API query and no archaeology through merged pull requests; a pull-request body MAY repeat the provenance for human reviewers but SHALL NOT be the record the lane reads. Recording it in the comment costs no widening of the auto-merge envelope, which already admits comments adjacent to the digest inside that block.

The recorded revisions MUST be the revisions of the last commit touching each repository's BAKED INPUTS, and MUST NOT be those repositories' branch tips. The served plane's repository moves for reasons that have nothing to do with this image — including, inevitably, this lane's OWN merged pin commits — so a tip-versus-tip comparison would make every landed pin guarantee that the next run rebuilds, reintroducing exactly the nightly churn this requirement exists to prevent. Whichever input scoping a realization adopts SHALL be recorded with the pin, so that consecutive runs compare like with like.

Provenance that is ABSENT or unparseable — a hand-pinned bootstrap image, or a pin a human wrote — SHALL be treated as CHANGED: the lane builds once, and the pin it produces establishes the provenance every later run reads. Failing open here is deliberate and bounded, because the cost is one redundant build while failing closed would leave a hand-pinned plane permanently unrefreshed.

Equality of the BUILT IMAGE DIGEST against the pinned digest MUST NOT be the predicate, and no realization may make it one. Container image builds here are not reproducible: a fresh checkout stamps file modification times at checkout time, so the copied layers differ byte-wise even when every file's CONTENT is identical, and the manifest digest moves with them; the base image is additionally referenced by a floating tag, so a fresh pull can move the base layers independently of anything in this program. A digest comparison would therefore never find equality, the short-circuit would never fire, and the lane would pin and deploy content-equivalent images every night. Digest inequality MAY be retained as a defence-in-depth note on a run that built anyway, but it SHALL NEVER be the trigger.

#### Scenario: Nothing moved overnight
- **WHEN** the current corpus-repository input revision equals the pinned image's recorded corpus revision AND the current served-plane build-recipe revision equals its recorded build-recipe revision
- **THEN** the lane MUST stop BEFORE building — no checkout, no snapshot generation, no image build, no push — and MUST open ZERO pull requests and cause ZERO deploys
- **AND** the run MUST be recorded as a no-change outcome, and the absence of a pull request MUST NOT be reported as a failure

#### Scenario: The corpus moved
- **WHEN** the corpus repository's baked inputs have moved since the recorded revision
- **THEN** the lane MUST build and MUST produce exactly one pin proposal for that movement

#### Scenario: The build recipe moved but the corpus did not
- **WHEN** the served plane's Dockerfile or build recipe has moved since the recorded revision while the corpus has not
- **THEN** the lane MUST build and propose, because the image differs even though the corpus did not — this is why the predicate carries two revisions and not one

#### Scenario: The pinned image carries no usable provenance
- **WHEN** the pinned image's provenance record is absent or cannot be parsed
- **THEN** the inputs MUST be treated as changed and the lane MUST build once
- **AND** the pin it opens MUST establish the provenance that later runs read

#### Scenario: An unrelated commit lands on the served plane's repository
- **WHEN** the served plane's repository advances for any reason that does not touch the image's baked inputs — including this lane's own previously merged pin commit
- **THEN** the lane MUST NOT treat that as movement and MUST NOT rebuild
- **AND** a realization comparing branch tips rather than baked-input revisions MUST be rejected, because it makes every landed pin force the next run's rebuild

#### Scenario: Output-digest equality is proposed as the predicate
- **WHEN** any realization would decide the no-change case by comparing the digest it just built against the pinned digest
- **THEN** it MUST be rejected — the build is not reproducible (checkout-time modification stamps move the copied layers; the floating base-image tag moves the base), so that comparison can never find equality and the short-circuit would never fire

### Requirement: The refresh lane proposes its pin as an envelope-shaped pull request
The lane SHALL deliver its result as a pull request authored by the lane's governed App identity on a FIXED head branch, against the served plane's repository default branch, whose ENTIRE diff is the `digest:` value and its adjacent provenance comment on the `ideation-dashboard` entry inside the `images:` block of the ONE overlay file. No other file, no added or removed image entry, no `name:` or `newTag:` change, and no change to any other block of that file MAY be produced by this lane. That comment block is not decoration: it is the AUTHORITATIVE provenance record the next run's no-change check reads, so the lane MUST write both input revisions into it — the corpus revision the snapshot and baked corpus came from, and the build-recipe revision the Dockerfile came from — in the stable machine-readable shape the no-change requirement fixes. The pull-request body SHALL repeat, for the human reviewer who would otherwise reconstruct it, the same two revisions plus the snapshot's `source_revision`, the pushed tag and digest, the digest it replaces, and the strict-validation counts; the body is a courtesy to readers and is NOT the record the lane reads. Naming the build-recipe revision is what keeps a Dockerfile change from altering the image invisibly behind a digest-only diff.

The lane MUST NOT assert its own diff shape as a claim — by a label, a title prefix, or a commit-message convention — because a shape the author asserts is a shape a buggy or compromised lane can widen. The shape MUST be adjudicated by the receiving repository over the actual diff, and the lane's obligation is to PRODUCE a conforming diff, never to certify one.

#### Scenario: A pin proposal is opened
- **WHEN** the lane has a new digest to propose
- **THEN** it MUST open (or advance) exactly one pull request on the fixed head branch whose whole diff is the digest line and its adjacent comment in the overlay's `images:` block
- **AND** the body MUST name the snapshot `source_revision`, the tag, the new and previous digests, the strict-validation counts, and the Dockerfile revision

#### Scenario: The lane would produce a wider diff
- **WHEN** any realization of the lane would touch a second file, another block of the overlay, another image entry, or any non-digest field
- **THEN** it MUST be rejected in review — producing an out-of-envelope diff is a defect of this lane, not a case for widening the envelope

#### Scenario: An out-of-envelope diff nevertheless reaches the repository
- **WHEN** a pull request from this lane carries a diff wider than the envelope for any reason
- **THEN** the receiving repository's shape adjudication MUST refuse it and the pull request MUST park for human review
- **AND** the lane MUST NOT be able to obtain approval by declaring its own diff in scope

### Requirement: The refresh chain is landed by four separate authorities, and no actor holds more than its own rung
The end-to-end refresh SHALL be performed by four distinct actors, each acting only within authority it already holds: the artifact WORKER builds and pushes the image and holds no repository credential; the lane's APP identity opens the pin pull request and holds no registry and no cluster credential; the APPROVER identity — a dedicated merge-master App, distinct from the author because an author cannot approve its own pull request — submits exactly one approving review when a rules-as-code envelope conjunctively holds, and issues no merge call; and GitHub's own auto-merge lands it, after which the served plane's in-cluster reconciler applies the merged state under the companion `dox-gitops-delivery` capability. The approval envelope SHALL be read from the receiving repository's BASE branch together with the approving workflow's own definition, so a pull request can never alter the rules or the logic that govern its own approval, and every condition SHALL be evaluated fail-closed: any failing or unevaluable condition submits no approval and leaves the pull request parked for the human gate. The exception SHALL be revocable by a single configuration change, with no code change and no redeploy.

#### Scenario: A refresh lands end to end
- **WHEN** the lane has pushed an image and opened a conforming pin pull request
- **THEN** the shape adjudication passes, the approver submits one approving review inside the envelope, GitHub's auto-merge lands the pull request, and the in-cluster reconciler applies it
- **AND** at no point does any single actor both produce the artifact and apply it

#### Scenario: A condition of the envelope cannot be evaluated
- **WHEN** the approver cannot evaluate any envelope condition — a check result unavailable, the approving identity unconfigured, the candidate class unresolved
- **THEN** no approval MUST be submitted and the pull request MUST park for the human gate

#### Scenario: The lane is granted apply authority
- **WHEN** any proposal would give the lane, the worker, or the authoring App a cluster credential, a kubeconfig, or authority to merge its own pull request
- **THEN** it MUST be rejected — the separation of the four rungs is the design, not an implementation detail to be optimised away

#### Scenario: The exception must be withdrawn
- **WHEN** the autonomous approval for this candidate class must be stopped
- **THEN** revoking one configuration item MUST return every such pull request to human review, with no code change and no redeploy

### Requirement: The refresh lane's outcome is visible in the nightly reporting surface
The refresh lane SHALL record its outcome as a diagnostic status artifact beside the existing ideation-dashboard lane status, delivered by the run's existing health-artifact delivery, and the dated report SHALL carry that outcome. The recorded outcome SHALL distinguish, at minimum: published-and-proposed, no-change, skipped (with the readiness reason), and strict-validation failure (with the validator's own output, bounded) — and it SHALL carry the two input revisions the no-change decision was made on (each beside the recorded revision it was compared against), the snapshot `source_revision`, the built and previously pinned digests when a build occurred, and the pull-request reference when one exists. A no-change outcome SHALL name the revisions that matched, so that "nothing moved" is auditable rather than merely asserted. Where the artifact can only be delivered on the FOLLOWING run because the delivery step precedes the lane, the report SHALL state which run's outcome it is naming rather than presenting a lagging outcome as the current one. A status-artifact failure MUST NOT fail the run, and a skip MUST NEVER be silent: the run's own annotations SHALL carry it immediately even when the artifact is delivered later. A pin pull request left open across more than one cycle SHALL be reportable as a stuck chain, because an unmerged pin on a fixed branch is the clearest available signal that the refresh is parked.

#### Scenario: The lane skips or fails
- **WHEN** the lane is skipped for readiness, or fails strict validation
- **THEN** the outcome and its reason MUST be recorded in the status artifact and annotated on the run immediately
- **AND** the deterministic results and the delivered report MUST be unaffected

#### Scenario: The status artifact itself cannot be written
- **WHEN** writing the refresh status artifact fails
- **THEN** the run MUST continue and MUST NOT fail on the reporting artifact

#### Scenario: A pin pull request is parked
- **WHEN** a pin pull request from this lane remains open at the next run
- **THEN** the run MUST be able to report the chain as stuck, naming that pull request

#### Scenario: The reported outcome lags its run
- **WHEN** the delivered status artifact describes the previous run because delivery precedes the lane
- **THEN** the report MUST say so explicitly rather than presenting it as this run's outcome

### Requirement: The refresh lane conserves the worker and identity authority the nightly already holds
The refresh lane MUST NOT widen any authority boundary this pipeline already draws. The worker's permission matrix is UNCHANGED: `execute_final_action` and `access_secrets` remain constitutionally false, and the lane's worker-side work is artifact production plus a proposal — nothing else. The worker SHALL hold no repository credential, no kubeconfig and no cluster access, and its registry PUSH capability SHALL be a host substrate credential, scoped to the single image repository, delivered to the host BY REFERENCE and reconciled onto it the way every other credential in its host manifest is — never fetched or read by the worker's model loop, never written into the built image, and never emitted to a job log. The lane's App identity SHALL gain, on the served plane's repository, ONLY the contents and pull-request permissions its authoring act requires; it SHALL gain no registry, approval, merge or cluster authority there or anywhere. The approving identity SHALL remain distinct from the authoring identity.

Repository source SHALL cross into the worker only as the parent run's sealed,
bounded Actions artifact. Repository credentials, deploy keys, Git credential
helpers, raw repository clones, and repository network access on the worker are
prohibited; the credentialed hosted parent owns those reads and persists no
credential into the artifact.

#### Scenario: The lane completes a cycle
- **WHEN** the worker has generated the snapshot, built and pushed the image, and the App has opened the pin pull request
- **THEN** the lane's work is finished, and the apply is performed by the receiving plane's in-cluster reconciler on merged state
- **AND** no part of the lane has held a cluster credential at any point

#### Scenario: A permission-matrix exception is proposed for this lane
- **WHEN** any proposal would set `execute_final_action` or `access_secrets` true for this or any lane, or grant the worker a repository credential to open its own pull request
- **THEN** it MUST be rejected as a contradiction of the contract the worker class is defined by, not weighed as a trade-off

#### Scenario: The worker is asked to fetch repository source
- **WHEN** any realization would place a repository token, deploy key, credential helper, or raw repository clone on the artifact worker
- **THEN** it MUST be rejected — the credentialed parent seals the bounded source artifact and the worker consumes only that artifact

#### Scenario: The push credential's scope is widened
- **WHEN** a realization would give the worker host a registry-wide push credential, or hand the push credential to the model loop, or bake it into the image
- **THEN** it MUST be rejected — the credential is push-scoped to one image repository, host-local, and delivered by reference
