# Tasks: add-worker-enrollment-broker

Phase 1 is THIS change. Phases 2–4 are named successor realization
changes (each pins the released contract bundle); phase 5 is the
acceptance that closes the staged topic and spans them. Tasks outside
phase 1 are listed so the sequencing and the ownership are agreed here,
and are NOT executed by this change.

## 1. Contract (openxFactory — THIS CHANGE)

- [x] 1.1 NEW `contracts/worker-enrollment/worker-enrollment-request.schema.yaml`
      (`kind: worker_enrollment_request`, `schema_version`): estate
      (`fleet` | `temp`), authentication mode (`host_identity` |
      `device_code`), authenticated subject, host identity facts (host
      id/device, OS, app version observed), requested worker shape, and
      the policy version the requester saw. One shape for both estates —
      the mode is a field, not a second schema (spec R1).
- [x] 1.2 NEW `contracts/worker-enrollment/worker-lease.schema.yaml`
      (`kind: worker_lease`): lease id, worker/host binding, estate,
      issued-at and expiry, renewal cadence and grace, trust tier, runner
      group + labels, floor in force, lease state
      (`active` | `expired` | `revoked` | `refused`), and the
      `policy_version` applied. The lease is the authority record — it
      carries no token field at all (spec R2, R8).
- [x] 1.3 NEW `contracts/worker-enrollment/worker-enrollment-grant.schema.yaml`
      (`kind: worker_enrollment_grant`): the enrollment response — the
      lease, the runner package policy for the estate (pinned version +
      sha256 + self-update disabled for fleet; self-update enabled for
      temp), the manifest reference or inline manifest for the temp
      estate (design D5), and the short-lived registration token declared
      TRANSIENT: single-use, never persisted, never logged, and excluded
      from every derived record by shape (spec R2, R7).
- [x] 1.4 NEW `contracts/worker-enrollment/worker-lease-renewal.schema.yaml`
      (`kind: worker_lease_renewal`): the renewal request (lease id,
      observed app version, observed runner version, heartbeat liveness
      facts) and the renewal response (lease state, new expiry, CURRENT
      FLOOR always present, required action — `none` | `update_required`
      | `stop` — and refusal reason when refusing). The floor is
      REQUIRED on every response, including approvals (spec R4, R5, R6).
- [x] 1.5 NEW `contracts/worker-enrollment/worker-enrollment-policy.schema.yaml`
      (`kind: worker_enrollment_policy`): per-estate minimum app version,
      per-estate runner package policy, eligibility groups + per-engineer
      machine cap, trust-tier definitions and their runner-group/label
      projections, cadence/grace/skew parameters, and `policy_version`.
      Shipping the schema here keeps design D3 to a home-and-review
      decision rather than a contract decision.
- [x] 1.6 NEW `contracts/worker-enrollment/worker-enrollment-audit-record.schema.yaml`
      (`kind: worker_enrollment_audit_record`): event
      (`enroll` | `renew` | `refuse` | `revoke` | `remove_token`),
      subject, host, estate, decision + reason, lease id, trust tier,
      runner group, observed version + floor, `policy_version`, and an
      evidence ref. The redaction rule is expressed IN THE SHAPE — no
      token/secret/key property exists and free-text fields are
      constrained so a token cannot be smuggled into one (spec R9).
- [x] 1.7 `contracts/worker-enrollment/README.md`: the family, the two
      authentication modes, the lease-not-registration inversion, the
      estate policy split, the redaction rule, and the named consumers
      (broker service, Omnigent-Install host app, OpsxFactory policy).
- [x] 1.8 Packaged examples under `contracts/worker-enrollment/examples/`:
      positives — a fleet enrollment request + grant (pinned package), a
      volunteer request + grant (self-update, temp group, temp manifest),
      a renewal approval carrying the floor, a renewal refusal for a
      below-floor worker, a revocation record. Negatives under
      `negative/` — `grant-token-persisted-in-lease`,
      `audit-record-carries-token`, `temp-lease-in-standing-group`,
      `fleet-grant-without-package-pin`, `renewal-response-missing-floor`,
      `lease-without-trust-tier` — each naming the rule it violates.
      Extended by the adversarial review of 2026-07-26 to 9 positives (the
      temp positives renamed `temp-*` for estate parity, plus the missing
      refusal audit record) and 21 negatives, adding one fixture per
      review finding: the mislabelled-estate lease and its corroborating
      audit record, an unrecognized temp runner group, the chunked token
      in `profiles` / in `reason_detail` / in the broker-served manifest,
      the long-lived token, the drifted fleet pin, the temp grant that
      pins, the escrowing renewal, the stale and the zeroed floor, the
      tierless refusal, the over-long lease, the temp-grant pin branch
      that had a rule and no fixture, and the standing lane that accepts
      volunteered hardware. Fixtures whose finding CODE is a coarse anchor
      also declare an `# expected_failure_detail:`, so a fixture cannot be
      mutated into testing nothing while its self-test stays green.
- [x] 1.9 Implement `scripts/validate-worker-enrollment.py` (canonical
      validator, repo-path argument like the other canonical validators):
      schema checks plus the four rules the shapes cannot express —
      (a) no token/secret value in any record or lease, (b) a temp-estate
      lease never names a standing execution-lane runner group, (c) a
      fleet grant always carries version + sha256 + self-update disabled
      while a temp grant never carries a pin, (d) every renewal response
      carries a floor. Extended by the 2026-07-26 adversarial review with
      the four rules the review proved were needed, and with value checks
      where the original rules only checked presence: (e) estate, subject
      class, host management and trust tier agree (both directions, on the
      lease AND the audit record), (f) a device-code renewal declares no
      standing secret on the host, (g) lease expiry matches the cadence
      and the registration token is genuinely short-lived, (h) no standing
      execution lane accepts volunteered hardware; the fleet pin is
      checked against the policy's declared package, the floor against the
      floors declared by the policy version it cites (and never zero), the
      denylist is applied by CLASS so realistic identifiers do not read as
      secrets, chunked tokens are de-chunked, and rule (b)'s no-policy
      fallback became a fail-closed allow-list that says when it runs.
- [x] 1.10 Validate: `OPENSPEC_TELEMETRY=0 openspec validate
      add-worker-enrollment-broker --strict` and `--all --strict` green;
      `python3 scripts/validate-worker-enrollment.py . --strict` green
      (0 errors, 0 warnings) over the packaged examples;
      `python3 scripts/validate-ideation-cross-reference.py` still 0
      errors.
- [x] 1.11 Register in `contracts/manifest.yaml` + `contracts/CHANGELOG.md`
      + the README contract index at the next additive bundle cut, per
      `docs/contract-versioning-policy.md`
      (registration-at-realization precedent).
      Realized 2026-08-02 in the release candidate published as
      `contract-v1.29` (renumbered 2026-08-03 after the chat-turn release
      consumed `contract-v1.28`): all seven schemas carry manifest digests
      and closed release-inventory membership; the canonical validator and
      11-positive/27-negative fixture corpus are pinned by the exact release
      commit.
- [x] 1.12 Close-out: README OpenSpec Records entry; staging INDEX +
      topic file readiness updated to "Proposed as
      add-worker-enrollment-broker (exit 1)"; the parked
      registration-credential decision on the worker-host-app topic
      annotated as resolved by this contract.

## 2. Broker service (FOLLOW-ON CHANGE — home decision D1 already taken)

- [x] 2.1 **Design D1 — DECIDED 2026-07-26** with the change's approval
      (proposal.md: "D1-D10 recommendations adopted as decided"). The
      broker lands in a NEW dedicated repository owned by OpsxFactory's
      domain, deployed as a container app on the existing platform
      subscription and deliberately NOT into the QA AKS cluster — it is a
      production control-plane dependency of every worker host, and
      hanging it off a QA cluster would inherit QA's blast radius and
      lifecycle. Do NOT re-escalate this: it is recorded in design.md D1
      and in the family README's consumer note.
- [ ] 2.2 Custody the opsxfactory administration-tier App key under the
      ratified `credential-contracts` shapes (vaulted binding,
      short-lived workflow-scoped grants, approval before issuance,
      rotation cadence). No other component holds it (spec R3).
- [ ] 2.3 Enrollment endpoint: both authentication modes, eligibility
      evaluation against the policy, grant issuance with a short-lived
      single-use registration token, temp-estate manifest rendering
      (design D5).
- [ ] 2.4 Lease store and renewal endpoint: TTL/grace/skew per policy,
      floor on every response, refusal reasons, revocation as a lease
      state that refuses the next renewal (spec R4–R6).
- [ ] 2.5 Remove-token brokering for drift repair, on the same authority
      and the same audit path as registration (spec R3). **Carries a
      contract delta**: the phase-1 family shipped the AUDIT half only
      (`event: remove_token`), and R3 scenario 2's request/response shape
      had no schema — `worker_enrollment_grant` requires a lease and a
      runner package, so it cannot represent a remove-token issuance. Add
      that shape to the bundle in this phase rather than letting the
      broker and the host app agree on it in code, where the canonical
      validator cannot see a divergence (paired with task 3.5).
      **The two halves are tracked separately below: the CONTRACT DELTA IS
      DONE, the broker implementation is not, which is why this checkbox
      stays open.**
  - [x] 2.5a **Contract delta LANDED** by the amendment of 2026-07-26 to this
        ACTIVE change (the shape this task pre-sanctioned):
        `contracts/worker-enrollment/worker-removal-grant.schema.yaml`
        (`kind: worker_removal_grant`) — the remove-token issuance response,
        carrying the enrollment grant's transient discipline for the remove
        token (single-use, a pattern-capped `lifetime`, a `writeOnly` value,
        `persist`/`log` forbidden, `derived_records: excluded`), NO
        registration token and NO runner package by shape, `binding.runner_group`
        as the token's declared blast radius, and the audit linkage as a
        REFERENCE to the existing `remove_token` record rather than a second
        copy of its facts. Spec R3 gains the shape reference plus a
        `worker_removal_grant` requirement with four scenarios, and R10's
        bundle enumeration includes it. Two positives (a drift repair, a
        revocation-driven removal) and six negatives are wired into the
        canonical validator's self-test, which extends rule (a) (the
        `remove_token` declaration exemption and the `.value` finding) and
        rules (b) and (e) to the new kind, and adds rule (i): the remove token
        is short-lived on the clock, not by adjective. Bundle registration
        still rides task 1.11.
  - [ ] 2.5b Broker-side implementation of the exchange against that shape —
        the endpoint, the lease and eligibility checks, minting through the
        custodied administration-tier key, and the `remove_token` audit
        emission. Phase 2, unchanged.
- [ ] 2.6 Audit emission for every decision, validated against the
      audit-record schema with the redaction rule enforced in code and in
      test (spec R9).
- [ ] 2.7 Pin the released contract bundle and run the canonical
      validator in the broker's own CI.

## 3. Omnigent-Install / Worker Host App (FOLLOW-ON CHANGE)

- [ ] 3.1 `runner_services`: replace the fail-closed refusal with the
      broker enrollment call (the seam already exists — nothing needs
      un-building), verify the package per the grant's estate policy, and
      register with the short-lived token without persisting it.
- [ ] 3.2 Supervisor task: lease renewal on the declared cadence,
      persisting only the lease, tolerating clock skew, and treating an
      unreachable broker as "not yet lapsed" until TTL + grace.
- [ ] 3.3 Fail-closed stop path: stop runner services on
      `update_required`, refusal, expiry, or revocation; restart cleanly
      when a renewal returns to active; never allow a local override
      (spec R5).
- [ ] 3.4 Heartbeat reports lease state and `update_required` (delta
      lands in publisher + service + evaluator TOGETHER — design D10,
      three-places rule; may ride the bench-inventory heartbeat delta).
- [ ] 3.5 Teardown semantics per design D7: full cleanup on volunteer
      uninstall (brokered remove token, services, tasks, local state,
      materialized profiles), stop-only on expiry, immediate stop +
      best-effort cleanup on revocation.
- [ ] 3.6 Installer path for volunteer workstations: download → install →
      device-code enroll, with no standing secret written at any step.

## 4. OpsxFactory (FOLLOW-ON CHANGE)

- [ ] 4.1 Custody arrangements for the opsxfactory administration-tier App
      key the broker holds (key vault, rotation, grant approval path).
- [ ] 4.2 The `worker_enrollment_policy` instance: floors per estate,
      runner package pins, cadence/grace, trust tiers — reviewed through
      the governed lane, since raising a floor denies work estate-wide
      (design D3).
- [ ] 4.3 Create the dedicated temp runner group + label convention and
      the trust-tier → runner-group projection (design D8, spec R8).
- [ ] 4.4 Engineer eligibility: the Entra group and the per-engineer
      machine cap (design D6).
- [ ] 4.5 Per-host broker-access secret provisioning at Intune enrollment
      time, escrow-at-birth, with a rotation cadence that does not
      require re-enrollment (design D9).
- [ ] 4.6 Fleet runner package bumps ride manifest rollouts, not broker
      instructions (spec R7).

## 5. Acceptance (spans phases 2–4; closes the staged topic)

- [ ] 5.1 **The volunteer-workstation end-to-end on Brett's machine**
      (first volunteer, and the NT SERVICE fact-check host from the
      worker-host-app topic): download → install → device-code enroll →
      lands in the segregated runner group with temp labels → executes a
      lane job → survives lease renewals → fails closed when the floor is
      raised past its version (`update_required` in the heartbeat, runner
      services stopped) → recovers by reinstall.
- [ ] 5.2 Fleet parity: an Intune-managed host enrolls with its per-host
      identity, receives the pinned package, and registers — proving one
      protocol served both estates.
- [ ] 5.3 Revocation drill: revoke a lease with the machine offline;
      confirm work stops at the refused renewal within cadence + grace
      and that the audit trail alone establishes when and why.
- [ ] 5.4 Evidence: audit records for every step of 5.1–5.3, verified to
      contain no token values; realization evidence recorded on the
      successor changes; staged topic archived.
