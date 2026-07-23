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
- [ ] 1.3 `OPENSPEC_TELEMETRY=0 openspec validate add-ideation-intent-plane
      --strict` and `--all --strict` green before commit; README "OpenSpec
      Records" entry added.

## 2. Gate-Intent Kernel (openxFactory contract)

- [ ] 2.1 `contracts/schemas/gate-intent.schema.yaml`: the request artifact
      (actor, verb enum incl. dispose-possible, target, args, requested_at,
      snapshot_rev_seen, status pending|applied|refused + refusal reason,
      applied_record ref) — open/additive posture, gate-action-record's
      sibling, never a record of an applied act.
- [ ] 2.2 Packaged examples (valid pending/applied/refused; negatives:
      forged-status, missing snapshot_rev_seen, refused-without-reason).
- [ ] 2.3 Delegated validator rules in
      `validate-ideation-dashboard-contracts.py` (status transitions one-way
      pending->applied|refused; applied requires record ref; kind/family
      registration) + self-test fixtures green.
- [ ] 2.4 Register the delta in contracts/manifest.yaml / CHANGELOG.md /
      README.md at the realization commit (registration-at-realization
      precedent).

## 3. Local Action Center (codexFactory Speckit realization — D5 first)

- [ ] 3.1 Loopback-gated executing gate routes in serve.py
      (`POST /actions/gate/<verb>`) calling the console engine; actor from
      local identity; capability probe advertises them only on loopback.
- [ ] 3.2 Dispose tray UI on pending_review possible tiles (wheel + canvas):
      accept / reject(reason+citation) / defer; refusal panel rendering
      GateRefused/boundary refusals; gate bar upgraded from descriptor to
      executing when the routes are live.
- [ ] 3.3 Tests: route gating (403 off-loopback), tray -> engine -> register
      lifecycle outcomes, refusal surfacing, boundary intact.

## 4. Hosted Intent Plane (codexFactory + omnigent-install + aggregation)

- [ ] 4.1 Intent-inbox service (dispatch-only credential, ingress-actor
      stamping, per-actor verb allowlist config, rate limit + idempotency
      key); deployment via omnigent-install (hosting shape decided at
      realization: sidecar vs own deployment).
- [ ] 4.2 Per-user Basic Auth entries + ingress actor forwarding (replaces
      the shared secret); Keycloak swap stays contract-invisible.
- [ ] 4.3 Apply-lane workflow + orchestration module (doc-health lane family
      pattern): replay via console engine, stale-view refusal, atomic
      intent+record+artifact commit, rolling intents PR with auto-merge,
      optional on-apply snapshot rebake.
- [ ] 4.4 Hosted tray flips from descriptor to intent emission; intent-feed
      overlay (pending/applied/refused chips) + refusal panel against
      GET intents.
- [ ] 4.5 Flutter verdict-terminal client consumes the same two endpoints
      (own feature; contract fixed here).

## 5. Tests And Records

- [ ] 5.1 End-to-end proofs: forged-actor ignored; unauthorized verb refused
      at inbox; stale-view refused at lane; atomic commit shape; hosted and
      local dispositions produce equivalent records; serving pod remains
      credential-free (boundary suite).
- [ ] 5.2 Keep the README "OpenSpec Records" entry current through
      ratification, realization, and archive.
