# Tasks: Ideation Intent Plane

Governance tasks (sections 1-2, openxFactory contract) come first;
realization tasks (sections 3-5, codexFactory + omnigent-install +
aggregation Speckit work) are marked as such and are NOT done by authoring
this change.

## 1. Origin And Governance (openxFactory)

- [x] 1.1 Organized 2026-07-23: `ideation/staging/ideation-action-plane/`
      (two fragments: intent plane + drive membrane) from the
      dashboard-action-center and cloud-workstation-topology brainstorms
      (both flipped to `staged` with Organized notes); INDEX.md row + detail
      section added in the same commit (maintenance rule).
- [x] 1.2 Decision record: second touch RESOLVED as custody-not-decision
      (design D1, Brett 2026-07-23); intent kernel is its own schema (D3);
      local-first realization order (D5).
- [x] 1.3 Verified 2026-07-23: `--strict` and `--all --strict` green (37
      items); README "OpenSpec Records" entry added in the proposal commit.

## 2. Gate-Intent Kernel (openxFactory contract)

- [x] 2.1 Realized 2026-07-23: `contracts/schemas/gate-intent.schema.yaml`
      — the request artifact (actor inbox-stamped, verb enum in lockstep with
      gate-action-record incl. dispose-possible, per-verb target
      conditionals, args as console-entrypoint kwargs, requested_at,
      snapshot_rev_seen, one-way status with refused->refusal_reason and
      applied->applied_record conditionals, idempotency_key); open/additive
      posture, never a record of an applied act.
- [x] 2.2 Realized 2026-07-23: packaged examples — valid pending + applied
      (with the request->act record chain); negatives
      `intent-refused-without-reason` and `intent-applied-without-record`
      (both schema-layer, each naming its violated rule).
- [x] 2.3 Realized 2026-07-23 (schema registration + per-status field rules;
      one-way TRANSITION-mode pairs ride the apply-lane realization with its
      fixtures): `gate-intent.schema.yaml` registered in the family
      validator's schema list + kind map; applied->record and
      refused->reason enforced at the schema layer; self-test green
      (0 errors, 0 warnings, --strict).
- [x] 2.4 Register the delta in contracts/manifest.yaml / CHANGELOG.md /
      README.md at the realization commit (registration-at-realization
      precedent).
      Realized 2026-08-02 in the release candidate published as
      `contract-v1.29` (renumbered 2026-08-03 after the chat-turn release
      consumed `contract-v1.28`): the gate-intent kernel is registered for
      the first time at its wheel-expanded shape, with raw-byte digest and
      closed release-inventory membership.

## 3. Local Action Center (codexFactory Speckit realization — D5 first)

- [x] 3.1 Realized 2026-07-23 (codexFactory `specs/006-local-action-center`,
      PR #39): `gate_routes.py` + serve.py `POST /actions/gate/<verb>`
      (dispose-possible, ratify executing; demote/edit-apply/kickoff stay
      descriptor this slice) over the gate-console engine; actor = explicit
      `--actor` or the checkout's git user.name (unresolvable identity keeps
      the capability off, fail-closed); the capability verdict gains
      `actions.gate` + `actor`, true only on loopback + real checkout +
      resolved actor — the deployed image never qualifies.
- [x] 3.2 Realized 2026-07-23 (PR #39; wheel — the canvas tray follows the
      same dispose.js module when that view grows a pending surface):
      `views/dispose.js` tray (accept / reject with required reason+citation
      / defer) on the wheel's focused pending_review tile, session-local
      applied overlay (two-plane: the snapshot is never mutated; tiles show
      the verdict + regenerate hint), refusal panel rendering every engine
      refusal textContent-only; gate.js ratify EXECUTES under the capability
      (caps bound by app.js — gate.js stays import-free for its standalone
      node tests).
- [x] 3.3 Realized 2026-07-23 (PR #39): 8 real-HTTP tests — capability
      advertisement on/off loopback and without actor, accept persists
      register + gate-action record, uncited reject refused on the wire with
      nothing persisted, validator-reject persists nothing, invalid/unknown
      verbs, ratify executes; notebook-suite capability expectations updated
      (actor pinned for determinism); dashboard suite 329 green.

## 4. Hosted Intent Plane (codexFactory + omnigent-install + aggregation)

UNBLOCKED 2026-08-09 — hosting venue DECIDED by Brett (design D7): the QA
AKS cluster behind the dashboard's ingress, per-user Basic Auth as identity
rung 1; realization evidence rides a deployment-handoff request to
OpsxFactory (managed-subject rule).

- [x] 4.1 Intent-inbox service (dispatch-only credential, ingress-actor
      stamping, per-actor verb allowlist config, rate limit + idempotency
      key); deployment via omnigent-install (hosting shape decided at
      realization: sidecar vs own deployment).
      (Service + committed allowlist + 13 real-HTTP tests proposed
      2026-08-09 as Omnigent-Install PR #67 — actor stamped over
      body claims, allowlist fail-closed, one-workflow dispatch with the
      token named-not-carried, refusals and dispatch failures recorded and
      served. Ticks on merge; the k8s/ingress half rides 4.2 with the
      OpsxFactory deployment handoff.
      MERGED 2026-08-10: PR #67 (squashed 3a5b524) landed with a RED
      validate job — the suite was pytest in a unittest-discovery CI — and
      PR #68 repaired it same-day with the 13 scenarios as unittest
      TestCases, checks green before merge.)
- [ ] 4.2 Per-user Basic Auth entries + ingress actor forwarding (replaces
      the shared secret); Keycloak swap stays contract-invisible.
      (Deploy tree MERGED 2026-08-10 as Omnigent-Install PR #69, checks
      green before merge: deploy/kubernetes base + aks-qa overlay — dox
      namespace, credential-free dashboard pod, the inbox in its OWN
      deployment (D2 shape resolved: one credential, one pod), ingress on
      dox-opensoft-qa.xforge.us with per-user htpasswd Basic Auth and
      X-Auth-Request-User forwarded from $remote_user, /intents -> inbox,
      Key Vault CSI for both secrets, unittest shape guards, human-gated
      apply runbook. TICKS when the live apply lands via the OpsxFactory
      deployment handoff — CIR request + intake case + Brett's approval
      record + grant-held apply + read-back checks, the dispatch-junction
      precedent.)
- [x] 4.3 Apply-lane workflow + orchestration module (doc-health lane family
      pattern): replay via console engine, stale-view refusal, atomic
      intent+record+artifact commit, rolling intents PR with auto-merge,
      optional on-apply snapshot rebake.
- [ ] 4.4 Hosted tray flips from descriptor to intent emission; intent-feed
      overlay (pending/applied/refused chips) + refusal panel against
      GET intents.
- [ ] 4.5 Flutter verdict-terminal client consumes the same two endpoints
      (own feature; contract fixed here).

      (REALIZED 2026-08-10: openxFactory PR #157 — intent_apply_lane.py in
      the register-edit lane's family, replaying through run_gate_action
      with the new intent-plane/ingress-auth provenance pair (additive
      schema + manifest growth), full server-side revalidation, D4
      stale-view CAS, atomic intent+record+artifact commits, committed
      refusals, payload-equivalent idempotency, whole-pass rollback;
      40 lane tests. MERGED a6fdb77 after TWELVE Codex rounds closing 26
      findings (25 fixed, 1 disposed: the edit-project register CAS —
      aggregation-owned register, D18 queueing + fulfilment-time member
      checks are the material guard). The aggregation gained
      .github/workflows/intent-apply.yml (5539eb9): content-App token,
      fresh clone on intents/rolling, allowlist fetched from
      Omnigent-Install, env-only intent input, fail-on-rejected-push,
      one custody PR. The rolling PR's auto-merge custody wiring and the
      hosted tray flip ride 4.4.)

## 5. Tests And Records

- [ ] 5.1 End-to-end proofs: forged-actor ignored; unauthorized verb refused
      at inbox; stale-view refused at lane; atomic commit shape; hosted and
      local dispositions produce equivalent records; serving pod remains
      credential-free (boundary suite).
- [ ] 5.2 Keep the README "OpenSpec Records" entry current through
      ratification, realization, and archive.
