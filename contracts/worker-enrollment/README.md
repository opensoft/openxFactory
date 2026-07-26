# worker-enrollment Contract

Status: ratified
Ratified by: add-worker-enrollment-broker (approved 2026-07-26; registered in
`contracts/manifest.yaml` + `contracts/CHANGELOG.md` at the next additive bundle
cut, per [Contract Versioning Policy](../../docs/contract-versioning-policy.md))

The neutral contract for **how a machine becomes a governed worker and stays
one** — and the one place that grants permission to become one.

Today nothing grants it. The Worker Host App can build a worker host but cannot
register one: its `runner_services` step refuses fail-closed, because the only
way to hand a host a runner registration token is to put an administration-tier
GitHub App key on the host, which the ratified `roles-authority-model` App
identity tiers forbid and the per-domain App convention narrows further. This
family is the resolution, ratified as a contract before three separate
repositories try to implement it.

## The inversion this family exists for

**Enrollment grants a LEASE, not a registration.**

A registration is a fact on a machine: it exists until someone reaches the
machine and removes it. A lease is a decision the platform re-takes on a
cadence: it lapses unless the platform re-grants it. On managed metal the
difference is bookkeeping. On a laptop that spends weekends off-network and may
quit the company on a Friday, the difference is whether control exists at all.

Every other control here is expressed as a property of the renewal decision —
the version floor, revocation, the trust tier, the audit trail — which is
exactly why they all work on hardware nobody manages.

## Two authentication modes, one enrollment point

The request and response shapes are IDENTICAL across the estates. The estate
difference is who authenticates and where the host manifest comes from, never a
second protocol; `estate` and `authentication.mode` are FIELDS of one shape.

| | **fleet** | **temp** (volunteer workstation) |
|---|---|---|
| Authenticates as | the HOST, with a per-host identity in the managed-platform key vault | the ENGINEER, through an interactive device-code flow |
| Standing secret on the machine | one, and only broker ACCESS — never minting authority (`standing_secret_on_host: broker_access_only`) | **none, ever** — declared as `standing_secret_on_host: none` on every renewal request, so escrow is a contract violation and not an unrecorded choice |
| Runner package | hard pin: version + sha256 + self-update disabled; bumps ride manifest rollouts | self-update enabled; observed version informational only |
| Host manifest | arrives in the managed delivery package | **broker-served at enrollment** — the volunteer has no delivery plane |
| Runner group | the standing execution lanes | a dedicated temp group with temp labels |
| Trust tier | `managed_fleet` | `volunteered_hardware` |
| Fail-closed control | the app-version floor (and the delivery plane) | the app-version floor, and nothing else |

The estate policy split lives in the POLICY and the manifest source, not in the
exchange — so if the estates diverge further it is a policy fork, never a
protocol fork.

## Files

- `worker-enrollment-request.schema.yaml` — the one enrollment request both
  estates send: estate, authentication mode + authenticated subject (by
  reference), host identity facts including the observed app version, the
  requested worker shape, and the policy version the requester saw.
- `worker-lease.schema.yaml` — **the authority record.** Lease id, worker/host
  binding, estate, issue and expiry, renewal cadence and grace, trust tier,
  runner group + labels, the floor in force, lease state
  (`active` | `expired` | `revoked` | `refused`), and the `policy_version`
  applied. **It carries no token field at all** (see the redaction rule).
- `worker-enrollment-grant.schema.yaml` — the approved enrollment response: the
  lease embedded whole, the runner package policy for the estate, the temp
  estate's broker-served manifest, and the registration token declared
  TRANSIENT. A refused enrollment produces no grant at all — only an audit
  record — which is why the grant has no `decision` field.
- `worker-lease-renewal.schema.yaml` — the renewal exchange. The request names
  the identity that authenticated it (the same identity that enrolled, by
  reference) and declares whether any standing secret on the host made the call,
  then carries the observed app and runner versions and heartbeat liveness; the
  response carries the lease state, the new expiry, the required action
  (`none` | `update_required` | `stop`), a coded refusal reason — and **the
  current floor, always, including on approvals**, with its provenance
  (`source: policy` | `last_known`), so the one refusal that could not read a
  policy still carries a floor without inventing a policy version.
- `worker-enrollment-policy.schema.yaml` — the OpsxFactory-owned policy the
  broker CONSUMES (never broker-local config): per-estate floor and runner
  package, eligibility groups + per-engineer machine cap, trust-tier definitions
  and their runner-group/label projections, the per-lane declaration of which
  tiers a lane accepts (the LANE side of the exclusion, which a repo-wide boolean
  per tier could not express), cadence/grace/skew, the registration-token
  lifetime ceiling, the standing execution-lane groups a temp lease must never
  bind, and `policy_version`.
  Raising a floor denies work estate-wide, so `review.floor_raise_path` is part
  of the contract.
- `worker-enrollment-audit-record.schema.yaml` — one record per `enroll`,
  `renew`, `refuse`, `revoke`, and `remove_token`: subject, host, estate,
  decision + coded reason, lease id, trust tier, runner group, observed version
  and the floor in force, `policy_version`, and an evidence reference. ONE
  encoding per outcome, pinned by shape — a refused renewal is
  `renew` + `refused`, and `refuse` is reserved for a refused ENROLLMENT before
  any lease exists — because a compliance query filtering the other spelling
  returns silence and reads it as "no refusals occurred". The tier and the group
  travel on refusals and revocations too, since those are the records R9
  scenario 3 makes the sole evidence.
- `worker-removal-grant.schema.yaml` — **the remove-token issuance response.**
  It exists because R3 scenario 2 ("it requests a remove token from the broker
  against its lease, receives a short-lived single-use token") had no shape:
  `worker_enrollment_grant` requires a grant id, a request ref, an embedded lease
  and a runner package, so it cannot represent a removal, and without this the
  drift-repair call would be the one part of the protocol the broker and the host
  app agreed on privately in code where this validator cannot see a divergence.
  Shipped as the contract half of task 2.5, which pre-sanctioned it. Carries the
  lease it was requested against (by reference), the requesting subject, estate
  and trust tier, the worker/host binding, `binding.runner_group` as the token's
  declared blast radius, the reason class
  (`drift_repair` | `revocation` | `teardown` — design D7's three outcomes), the
  remove token on the enrollment grant's transient discipline exactly, and the
  audit linkage as a REFERENCE to the existing `remove_token` record. It carries
  NO registration token and NO runner package by shape: a repair removes a
  registration and never re-enrols a host, because returning a worker to service
  is a fresh lease decision.
- `examples/` — positive reference examples (both estates end to end — named
  `fleet-*` and `temp-*` after the estate VALUES the contract uses, so the two
  estates' fixtures sort together — a renewal carrying the floor, a below-floor
  refusal, the refusal audit record, a revocation record, a fleet drift-repair
  removal grant and the revocation-driven removal that follows that same
  revocation record, and the policy
  instance) plus self-testing negatives under `examples/negative/`, each
  declaring its `# expected_failure:` reason and, where a finding code alone is
  too coarse an anchor (`schema` is satisfied by any schema error at all), an
  `# expected_failure_detail:` substring that pins the fixture to the invariant
  it is named for.

## The redaction rule

**No token value exists in any stored artifact of this family, because no shape
can hold one.** Redaction here is a property of the record shapes, not of a
logging convention:

1. The **lease** — the document the host actually persists — has no token
   property, at any depth, and `additionalProperties: false` everywhere so none
   can be added.
2. The **grant's** `registration_token` is a DECLARATION: `transient: true`,
   `single_use: true`, an expiry, and an explicit handling block
   (`persist: forbidden`, `log: forbidden`, `derived_records: excluded`). Its
   `value` is `writeOnly` — present in the live response body only. The
   canonical validator treats a `registration_token.value` in any stored,
   committed, or scanned artifact as a finding, so "the token is never retained"
   is testable rather than asserted. The **removal grant's** `remove_token` is
   the same declaration, character for character, because it is the same
   administration-tier authority pointed the other way — and the family has
   exactly these two token-shaped property names, both of them declarations
   ABOUT a token rather than places one can sit.
3. The **audit record** has no token/secret/key property, and every free-text
   field is bounded — 200 characters, a closed character set, and no unbroken
   run of 25 or more token-alphabet characters — so a token cannot be smuggled
   into prose. Everything else on the record is a coded, closed vocabulary.
4. **Every open channel is bounded, and chunking is treated as smuggling.** A
   shape rule is only as good as its narrowest hole, and this family had three:
   separators were excluded from the run class (so `AAAA…….BBBB` reassembled
   with one `replace`), `requested_worker.profiles` was an open map with
   64-character values (so two entries carried the halves of a runner token), and
   `host_manifest.inline` was `{type: object, minProperties: 1}` — an unbounded
   channel in the ONE artifact a volunteer host writes to disk. Now: separators
   count toward a run, the profiles map is bounded on both sides (label-shaped
   keys, 8-character flag values), the inline manifest rides a bounded payload
   channel (closed key vocabulary, bounded scalars, bounded breadth and depth),
   and the canonical validator de-chunks — it strips separators per word and
   tests the CONCATENATION of arrays and bounded maps before deciding.
5. **"Short-lived" is a bound, not an adjective.** The grant declares a
   `lifetime` its pattern caps at fifteen minutes, the policy declares
   `registration_token.max_lifetime` as the estate ceiling, and the validator
   checks the actual `granted_at` → `expires_at` span against both — so R2
   scenario 3 (an expired token cannot register) is testable rather than
   assumed, and a 73-year "single-use" token is a finding. The removal grant's
   remove token gets the same clock check against `issued_at`, capped by the
   contract's fifteen-minute pattern (the policy's registration ceiling is
   deliberately NOT reused: it is the ceiling on ENROLLMENT tokens, and reading
   it here would let a policy edit widen an authority it never mentions).

Minting authority follows the same logic: the administration-tier App key that
mints registration AND remove tokens is held only by the broker, under the
ratified `credential-contracts` custody shapes. No host, installer, manifest,
escrow, or scheduled task holds or can derive it.

## Rules the canonical validator enforces beyond the schema shape

`scripts/validate-worker-enrollment.py [REPO_PATH] [--strict]` (run from the
pinned openxFactory checkout, never copied):

1. **No token or secret anywhere** — no token/secret/key-shaped property in any
   record or lease at any depth, and no secret-shaped value, scanned against the
   shared `contracts/avatar-client/redaction/` denylist plus a
   registration-token entropy heuristic, with chunking treated as smuggling (see
   the redaction rule, point 4). The denylist is applied BY CLASS: credential
   classes are errors, while its identifier-class patterns are advisory in
   reference fields, because an Intune device GUID really is a fleet `host_id`
   and an engineer UPN really is a subject `ref` — both legal by shape, and
   flagging them would have failed the first real record in the broker's own CI.
   The exemptions are four exact (kind, path) declarations ABOUT tokens: a
   grant's transient `registration_token` block, a removal grant's transient
   `remove_token` block, the policy's lifetime ceiling for the registration
   token, and a renewal's `standing_secret_on_host` assertion. Because the
   exemption is an exact pair, a `registration_token` on a REMOVAL grant is a
   finding — which is the shape of the mistake that would let drift repair
   re-enrol a host silently.
2. **Temp leases are segregated, and so are temp removal grants** — a temp-estate
   lease never names a standing execution-lane runner group, and neither does a
   temp-estate removal grant, whose `binding.runner_group` is the remove token's
   blast radius: a standing-group scope there is authority to deregister FLEET
   workers, a larger hazard than the temp lease the rule was written for. The
   removal grant names the field exactly as the lease does so the rule reads both
   without a special case. The check is armed by ANY temp-shaped fact
   (estate, tier, engineer subject, unmanaged host) rather than by the estate
   label alone. With a policy in scope it reads
   `standing_execution_lane_runner_groups` and `estates.temp.runner_group` from
   it. With none in scope — the normal case in the broker and host-app
   checkouts, since the policy instance lives in the managed-platform repo — the
   fallback is an ALLOW-list (the group must read as a temp/volunteer group),
   never a deny-list of today's standing group names, and it always says so in a
   note. `Default` and `xfactory-omnigent-workers` are both real standing lanes
   and neither reads as one.
3. **The estate package split holds** — a fleet grant carries version + sha256 +
   self-update disabled and MATCHES the package the policy declares (presence
   alone does not make an artifact known and digest-verified); a temp grant
   carries no pin at all.
4. **Every renewal response carries a meaningful floor** — approvals included,
   because the renewal response is the only channel that reaches unmanaged
   hardware. A zero floor is a finding, and a floor claiming `source: policy` is
   checked against the floors declared by the policy version it cites.
5. **Estate, subject, host management and trust tier agree** — on all three
   shapes that carry the four facts (the lease, the audit record, the removal
   grant), in both directions. Relabelling one enum used to turn a
   volunteered laptop into a managed-fleet worker in the standing execution lane
   with the audit trail corroborating it; on a removal grant the same relabelling
   would additionally disarm rule (2), which keys off the estate.
6. **A device-code renewal holds no standing secret** — the renewal exchange
   names the identity that authenticated it and declares
   `standing_secret_on_host: none`, so escrowing a refresh credential beside the
   lease is a contract violation rather than an unrecorded implementation choice.
7. **Lease expiry matches the cadence, and the registration token is
   short-lived** — `expires_at` is `issued_at` + `cadence.ttl` within the
   declared clock skew (the bound R4 and R6 compute with), and a token lifetime
   is positive and within both its own declaration and the policy ceiling.
8. **No standing execution lane accepts volunteered hardware** — the policy's
   lane declarations and tier projections must agree with its own standing-group
   list.
9. **The remove token is short-lived too** — a removal grant's `issued_at` →
   `expires_at` span is positive, within its own declared `lifetime`, and within
   the contract's fifteen-minute ceiling. A remove token is the same
   administration-tier authority as a registration token, and a stale REMOVAL
   authority takes workers out of the standing lane rather than adding one to it.

The validator self-tests the packaged examples first (every positive valid,
every negative invalid for its declared reason and, where the code is a coarse
anchor, for its declared detail) and fails closed if that degrades. Rule (2)'s
no-policy fallback gets its own pass over the fixtures of that class, because it
is the path a broker or host-app checkout actually runs.

## Consumers

- **The worker-enrollment broker service** — the standalone deployment holding
  the opsxfactory administration-tier App key, serving both authentication
  modes, owning the lease store, and emitting the audit records. Its repository
  and hosting are decided (design D1, adopted with the change's approval on
  2026-07-26): a dedicated Opsx-owned repository, deployed as a container app on
  the existing platform subscription and deliberately NOT into the QA AKS
  cluster — the broker is a production control-plane dependency of every worker
  host, and hanging it off a QA cluster would inherit QA's blast radius and
  lifecycle. The build itself is a successor change.
- **Omnigent-Install / the Worker Host App** — replaces the fail-closed
  `runner_services` refusal with the broker enrollment call, persists only the
  lease, renews on the declared cadence from the existing hourly supervisor, and
  stops runner services on `update_required`, refusal, expiry, or revocation.
- **OpsxFactory** — custodies the App key, owns the
  `worker_enrollment_policy` instance through the governed review lane, creates
  the dedicated temp runner group and label convention, and provisions the
  per-host broker-access secret at managed-enrollment time.

Each realization PINS the released bundle and runs this validator in its own CI
rather than copying a shape.

## What this family deliberately does not do

**The remove-token exchange now HAS its issuance shape** —
`worker_removal_grant`, added by the 2026-07-26 amendment to the active
`add-worker-enrollment-broker` change, which is the contract half of task 2.5 and
the reason this section no longer records that gap. What it does not add is a
separate REQUEST shape, and that is a decision rather than an omission: R3
scenario 2 makes the request one "against its lease", so its whole content is a
lease id, the authenticated subject, and the reason class — all three echoed on
the issuance, so the exchange is fully determined by one shape plus the
`remove_token` audit record rather than by three repositories each inventing a
request body. The BROKER-SIDE implementation of the exchange remains phase 2
(task 2.5b), as does the host app's teardown use of it (task 3.5).

The heartbeat/readiness contract does not grow here. Lease state and
`update_required` reaching the readiness evaluator must land in publisher,
service, and evaluator together (the three-places rule), so it is a separate
coordinated delta. What this family does is make the states that delta will need
well-defined and named, so it is a projection rather than a design.

Provenance: staged topic `openxFactory:staging:worker-enrollment-broker` (exit
1), which records the seven binding rulings taken with Brett on 2026-07-26;
parent topic `openxFactory:staging:worker-host-app`, whose parked
registration-credential decision this contract resolves. Design decisions D1-D10
(cadence, policy home, approval flow, manifest serving, eligibility, teardown,
trust-tier mechanics, per-host secret provisioning, heartbeat sequencing) are
recorded in
`openspec/changes/add-worker-enrollment-broker/design.md`.
