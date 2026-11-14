# Real GitHub bootstrap authentication proposal

Status: draft; recommended architecture for owner review, not ratified or implemented
Baseline: accepted factory #1312 and adapter #61/#62/#63; feature 017 T013 stays incomplete

## Context

The accepted authority provides durable atomic binding and real local authentication
but uses a fixed isolated-fixture profile. The current CLI is unselected and
refuses before outputs/OIDC. Adapter #63 prepared the missing source decisions;
see its `bootstrap-authentication-plan.md` and `t013-decision-record.md`.

## Goals / Non-Goals

Authenticate a real GitHub admission client and correlate it to one independently
approved dispatch without provisioning a separate persistent bootstrap credential on a runner. Preserve
static/full-config and protected proof semantics. Prepare a bounded source slice
that can be reviewed and tested in isolation before separately authorized use.

No implementation, workflow permission edit, token mint, live API write, App or
federation creation, setup, dispatch, release or human/domain acceptance occurs
now. A provider endpoint response or OIDC token alone is not authority.

## Decisions

### D1 — Explicit admission-identity policy amendment

Recommend a future internal profile `openxfactory-github-bootstrap-internal-v1`.
Its admission job may obtain a short-lived, bootstrap-purpose GitHub OIDC token
before environment approval. This deliberately amends the earlier no-preflight-
OIDC expectation only for the newly source-accepted profile. The reference profile
and default unselected CLI remain unchanged. No current workflow is edited.

GitHub documents job-scoped `id-token: write` as permission to request an identity
token, not a grant to write other resources. A job without an environment can
have a ref-scoped subject, while reusable workflows carry called-workflow identity.
These facts make the option technically possible; they do not make it safe without
an exact relying-party policy. GitHub's job permission is not restricted to our
chosen audience: that job can request other audiences too. A client constant does
not cryptographically narrow issuer capability. Owner acceptance must cover this
mint capability and relevant owned relying-party trusts, not only a token with our
preferred audience. Unprotected identity must not satisfy any selected signing or
provider trust; applicable existing owned trusts require separate operator review. Sources: [OIDC permissions](https://docs.github.com/en/actions/how-tos/secure-your-work/security-harden-deployments/oidc-in-cloud-providers),
[OIDC reference](https://docs.github.com/en/actions/reference/security/oidc),
[reusable workflows](https://docs.github.com/en/actions/how-tos/secure-your-work/security-harden-deployments/oidc-with-reusable-workflows).

Proposed bootstrap audience: `urn:opensoft:openxfactory:bootstrap-admission:v1`.
It is a proposed constant, not a registered or approved relying party. Final
bootstrap/proof audiences and complete immutable-ID subjects are independent
operator selections, must differ by purpose, and require later corroboration.
Never infer an approved subject from the observed repository prefix alone.

The trusted orchestration jobs contain only accepted control code; no agent/model
worker runs there or receives the token-request capability/token. Deployed worker
exclusion is still a T013/P01 gate. If the worker can read a control token or
request its own acceptable one, the hosting boundary is ineligible. No malicious-
runner/host or trusted-admin compromise resistance is claimed.

Alternative: retain strict no-preflight-OIDC and use an independently issued client
identity on a separately administered admission host. That requires a selected
issuance/delivery/OS boundary and is not supplied by the portable fixture. A new
self-hosted runner or repository bootstrap secret is not selected by this proposal.

### D2 — Purpose- and phase-separated verification

Reuse the accepted fixed issuer/JWKS transport and crypto rules, not the proof
verifier's environment-dependent policy. A separate bootstrap verifier must never
relax the existing proof verifier or make its environment claim optional.
Trust roots/endpoints/audiences/expected claims come from operator selection, not
worker/dispatch fields or token headers. Server TLS identity is independently
selected; HTTPS validates CA/hostname and refuses redirects or token-directed URLs.

Before any readiness, verify RS256/key compatibility, bounded canonical token,
issuer, exact scalar audience, current iat/nbf/exp/jti and exact immutable repo/
owner IDs, event, ref, source/caller/reusable refs and SHAs, run and attempt.
Unprotected preflight requires the selected ref-scoped subject and absence of an
environment claim. Post-approval repeat requires the separately selected complete
protected subject/environment plus fresh provider protection/approval readback.
The phase is selected by trusted policy, never a worker flag. Missing/ambiguous
required claims refuse; do not synthesize signed claims from environment variables.

The accepted same-source reusable definition must have exactly the allowlisted
OIDC-capable orchestration jobs, with unambiguous environment class per phase.
GitHub identity does not assert our role name. If signed/API facts cannot distinguish
a permitted phase, refuse and require a source-policy change; audience alone is
not a job-role discriminator. Qualification worker code cannot be a third eligible
orchestration job. Post-environment token identity does not itself prove approval
or a policy/operation grant.

Bootstrap authority permits only fresh readiness binding/operation readback for
its already-approved case/run. It cannot authorize/revoke selections, dispatch,
access provider resources, fetch signing credentials, request a proof, or satisfy
human approval. Do not configure cloud federation or any signing relying party
to trust the bootstrap audience/ref identity. A signature-valid bootstrap token
must fail unchanged protected-proof verification before custody is called. Isolate
both barriers from a successful signed proof-token control: change only audience
to bootstrap while keeping all protected claims, then separately remove only the
environment while keeping proof audience and other claims. Both must refuse with
zero custody calls. Also test a provider-shaped unprotected token requested with
proof audience; the isolated single-claim controls prevent another mismatch from
masking removal of either policy check. Fixture token shapes are not asserted to
be real provider output.
OIDC acquisition must distinguish the fixed verification issuer from GitHub's
job-provided request endpoint. A separately reviewed trusted hosting policy must
validate allowed HTTPS origin/path/context before sending the request credential;
never forward it to a worker-selected URL, redirect or diagnostic endpoint. These
request-environment values are available only to accepted orchestration code.
Tokens and token-request credentials are never persisted, logged, output or put
in artifacts. Repeated readiness reads may use a still-valid identity only after
fresh current authority checks; identity reuse cannot rebind a run, extend expiry
or bypass existing one-use proof reservation.

### D3 — Durable dispatch-attempt journal outside the job

A separate trusted operator approves a closed static selection/case/window and
one preauthorization. A trusted broker with a separately selected GitHub App
Actions-write capability owns the future dispatch attempt. The reader/controller/
worker do not receive that credential. Repository Actions write is broader than
one workflow; owner acceptance must cover its actual provider capability and
broker restrictions, expiry/revocation and repository-only installation scope.

Before external I/O, atomically compare-and-set the selected approval to consumed/
dispatch-pending in expected initialized retained state. Only the winner may make
at most one external request attempt. Persist the exact three workflow inputs,
repository/workflow/main source, originating human operator, broker actor, window
and immutable selection digest. Disable automatic transport retries and redirects.
Require fresh approved status, exact scope, revocation state and a non-regressing
trusted clock/window before reservation and again after every blocking operation
before request transmission, including credential acquisition and TLS connection.
A reserved winner paused beyond expiry or revoked before send makes zero dispatch
requests and retains consumed/indeterminate scope. The final checkpoint must be
adjacent to the bounded send, with no intervening unbounded I/O or automatic retry.
This checks our request-start authority, not an atomic provider execute-by or
instantaneous distributed revocation guarantee; later drift/expiry still refuses
wallet authority. Stricter provider timing guarantees need an upstream decision.
A crash before I/O may create zero runs and still consumes the attempt. A timeout,
lost response or malformed reply stays indeterminate; no automatic retry, unbind,
reset or newest-run search may manufacture success. Reconciliation/cancellation
requires separately granted scope and a named owner.

Pin the proposed dispatch API contract to `X-GitHub-Api-Version: 2026-03-10`.
Its documented request body has only `ref` and `inputs`; the response is 200
including numeric `workflow_run_id` and run URLs. Do not send
`return_run_details`: that flag and 200/204 switching belong to the older
2022-11-28 schema. A legacy/unexpected 204 is insufficient and stays indeterminate.
Construct later API paths from selected origin/repository and validated numeric
IDs, never returned URLs. The three workflow inputs do not change. See the
[version-pinned workflow dispatch API](https://docs.github.com/en/rest/actions/workflows?apiVersion=2026-03-10#create-a-workflow-dispatch-event).
This corrects the earlier preparation's mixed-version flag assumption without
calling or operationally qualifying the write endpoint.
No call to that write endpoint is made to prepare or validate this proposal.

### D4 — Independent corroboration and field provenance

The controller independently authenticates the broker journal and performs fixed
GitHub API reads with a separately selected Actions-read identity. A public run
record alone is neither a client authenticator nor proof of operator approval.
The JWT run/attempt must match the broker-correlated ID and independently read
current attempt; reruns need new authority and never inherit the old grant.
See [run API](https://docs.github.com/en/rest/actions/workflow-runs#get-a-workflow-run)
and [job API](https://docs.github.com/en/rest/actions/workflow-jobs#list-jobs-for-a-workflow-run-attempt).

| Fact | Independent provenance / refusal rule |
| --- | --- |
| Approval, case, static digest, expiry, originating operator | Operator approval + retained broker journal; never claims invented in a JWT |
| Assigned run | Provider-returned numeric ID bound to the consumed attempt; no worker-selected/newest ID |
| Repo/owner IDs and event/source/ref | Signed GitHub identity and selected provider run/repository facts must match operator source policy |
| Caller and called workflow identity | Exact signed refs/SHAs plus selected workflow ID/path and approved same-source definition; unavailable required provenance refuses |
| Attempt/status/actor | Actual provider run/attempt/job facts plus approved broker actor; no actor-name-only fallback |
| Phase/subject | Signed claims + trusted phase policy + accepted job graph; prefix or audience alone is insufficient |
| Environment/protection/approval | Independent current provider configuration and review history, exact environment ID, self-review/admin-bypass/main restrictions |
| Full config/grant/lease | Approved static projection plus actual run fields, fresh independent operation/scheduler/source readbacks; not token authorization |

API observations are not signed token claims. The implementation must map the
versioned response fields and refusal for each missing/ambiguous fact; do not infer
workflow SHA merely from a matching job title or copy a worker value into a signed
controller observation. The same-source expectation must be corroborated by the
selected actual workflow/source facts and, after protection, by proof identity.

GitHub's main ref is mutable, not an atomic expected-SHA dispatch parameter.
Recheck source before any authorized request and corroborate the actual returned
run afterward. Drift refuses wallet authority and qualification but cannot undo
a provider-created run or guarantee that changed workflow code never started.
Default live state stays blocked while the owner has not accepted a reviewed
source-update coordination policy or explicitly bounded residual-start exposure
and credential controls. Atomic prevention of all unaccepted workflow execution
requires a different upstream design; there is no silent tag fallback, repository
freeze, rule change or relaxed main restriction.

The broker must retain the originating human operator independently of its App
actor. A GitHub App actor must not mask the human initiator for environment
self-review: independently verify eligible reviewer identity differs from the
originating operator. Environment review remains distinct from domain human
consent, and every machine result still reports no human approval.

### D5 — Bounds, durable authority and safe failure

Proposed source bounds: fixed GitHub API origin/version; 5-second connect and
10-second overall decision I/O budget; 1 MiB decoded API response; no redirects
or automatic retries; at most two 100-job pages and four API requests per decision.
Missing relevant job in that bounded set refuses. Require a newly obtained identity
within the selected at-most-60-second admission freshness window, with no new
clock leeway; recheck after blocking work and clip readiness to token/observation/
grant/lease expiry. A provider-cached or stale identity that fails these bounds
refuses rather than gaining an availability exception. Reuse the existing 64-key issuer
snapshot limits and earliest deadlines; no stale response/key fallback on outage.
New operational JSON envelopes are closed and at most 64 KiB, nested runtime
config at most 16 KiB. Responses contain only selected fields/digests, never raw
JWTs, credentials or provider payloads. These are proposed policy bounds, not
provider guarantees, and require owner source acceptance.

Retain explicit store initialization, pinned identity, atomic one-context binding,
revocation, monotonic observed-clock high-water and no active-scope reset/restore.
Keep attempt consumption separate from subsequent actual-run/full-config binding.
Ambiguity consumes authority rather than reissuing it. No distributed exactly-once
dispatch/signature or hostile-host/valid-backup rollback guarantee is claimed.

Fresh bootstrap and operation reads remain mandatory before environment output
and again after environment approval; earliest expiry wins. Signing still requires
the unchanged protected proof identity, policy/challenge, measured launch, confined
custody, retained replay state and independent lifecycle checks. Missing clients
or any required selection retain the default refusal before outputs/proof use.

### D6 — Source-only work and migration

The future source slice may add a separate internal bootstrap verifier/client,
controller/journal adapter and explicitly opt-in workflow admission identity.
Feature 017 T012G-M is the sole executable implementation list. Frozen fixture
profiles, their tests, offline validators, neutral pins and proof verifier policy
remain unchanged. No self-hosted-runner, long-lived bootstrap secret, cloud-login
step or provider credential is introduced on the orchestration runner.

After profile acceptance and explicit implementation commissioning, build isolated
controls first, including signature-valid cross-purpose refusals and actual TLS
client/server identity. Keep operational host/profile selection absent by default.
No source test mints a real GitHub token or dispatches. Later T013 selects/authorizes
hosting, subjects, identities and source-update policy; setup and one dispatch are
separate subsequent decisions. T014/T015 and consumer/human/domain gates stay open.

Rollback disables the new opt-in client, revokes temporary operational capability
under separately authorized scope, and preserves every consumed journal/replay row.
It does not silently enable a stored-secret alternative or reset consumed attempts.

## Risks / Trade-offs

- Bootstrap-only OIDC is a deliberate owner-gated policy amendment, not proof identity or operational authority; audience/phase separation and negative controls are mandatory.
- A bearer token or token-request capability leaked to the worker defeats that client boundary; keep workers outside trusted orchestration and qualify actual exclusion later.
- Actions-write broker credentials have coarse provider scope; explicit owner acceptance and independent administration are required.
- Mutable main can start changed code before detection; default refusal and explicit residual-exposure/coordination acceptance remain mandatory.
- Dispatch ambiguity may consume an attempt with no run; preserve indeterminate state and require separate reconciliation authority.
- Real subject values, target/admin/credential references and deployed secrecy cannot be established by fixture success or these documents.

## Owner decisions before implementation

Accept or reject D1's bootstrap-only OIDC amendment, D2's purpose/phase model and
D3-D5's trust/failure bounds; commission a bounded source slice explicitly. None
is ratified by requesting this proposal. Deployment/resource selections, actual
subject/audience corroboration, source-update policy and every operative stage
remain T013 owner/operator gates even after later source acceptance.
