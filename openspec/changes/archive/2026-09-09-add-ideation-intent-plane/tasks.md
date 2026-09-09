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
- [x] 4.2 Per-user Basic Auth entries + ingress actor forwarding (replaces
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
      DONE 2026-08-13: the live v7 apply landed on QA AKS (dashboard + inbox +
      dox-auth Ready on the approved digests) and the readiness walk passed all
      six mandatory checks — anon 401; brett 200 over the Let's Encrypt dox-tls
      cert; auditor 403 with the refusal stamped actor=auditor; dispatch token
      Actions:write on opensoft/xFactory only; three images digest-pinned;
      dashboard pod credential-free. The CIR cir-opensoft-qa-dox-intent-plane
      walked acknowledged -> completed (trusted_validator, hermes-install PR #21)
      against the fresh passing readiness result dox-qa-intent-plane-ready. The
      dispatch-credential ownership hardening (personal PAT -> org-owned App)
      rides add-dispatch-credential-contract.)
- [x] 4.3 Apply-lane workflow + orchestration module (doc-health lane family
      pattern): replay via console engine, stale-view refusal, atomic
      intent+record+artifact commit, rolling intents PR with auto-merge,
      optional on-apply snapshot rebake.
- [x] 4.4 Hosted tray flips from descriptor to intent emission; intent-feed
      overlay (pending/applied/refused chips) + refusal panel against
      GET intents.

      (TICKED ON THE DOING — REALIZED 2026-09-06 -> 2026-09-09 AND THEN
      PROVEN LIVE. Every merge commit named below was read back with
      `gh pr view <n> --json mergeCommit` at this commit rather than copied
      from a note; the live-run evidence is § 5.1's.

      THE BROWSER HALF — openxFactory PR #718 -> `d179cc0d`
      (2026-09-06T15:06:50Z), "Intent plane 4.4 (PR-1): hosted tray emits
      intents; pending/applied/refused chips": the `actions.intent`
      capability so the tray MOUNTS hosted (`compute_capabilities` had
      returned `gate=local_human`, so it never could), the same-origin intent
      transport the credential-free pod (D16) permits, the pending / applied /
      refused chips over `GET /intents`, and the refusal panel rendering every
      engine refusal textContent-only. Before it, NOTHING in the browser
      posted or read an intent.

      THE FEED SOURCE, WHICH WAS A DESIGN DECISION AND NOT TYPING — the
      durable truth is the COMMITTED intents under
      `ideation/dashboard/intents/`, so the chips needed the custody chain
      that lands them: openxFactory #735 -> `6d3237e6` (enrol the
      `intent-rolling-custody` candidate in `.github/merge-approval-envelope.yml`
      — author `openxfactory[bot]`, head `intents/rolling`, base `main`,
      `require_all_checks: true`) with xFactory #304 -> `b2db7e47` (auto-merge
      on the rolling PR + the merge-master approval dispatch) and xFactory
      #313 -> `ddd19650` (a manual custody-only dispatch path).

      EIGHT DEFECTS THE LIVE RUNS FOUND, EACH FIXED BY ITS OWN VERIFIED PULL
      REQUEST ON BRETT HEAP'S SEPARATE WORD, NONE WORKED AROUND — xFactory
      #345 -> `90435875` (run the lane from `main` and write onto
      `intents/rolling`, ending the stale-library checkout); openxFactory #781
      -> `450bb602` (mint the merge-master token with `pull_requests: write`
      only — the App holds no `issues` scope, so the mint would have been
      refused before anything was approved); openxFactory #808 -> `2ef7d8c2`
      (carry the pinned validator's diagnosis on BOTH refusal branches, and
      distinguish a harness error from real findings — an operator-precedence
      slip had discarded the reason); openxFactory #814 -> `c991c0f3`
      (`lane-line` reports SUCCESS with a notice for bot-authored pull
      requests instead of a job-level skip the envelope core reads as
      not-green); openxFactory #816 -> `89242304` (doc-health promotes
      `gate-intent-snapshot-rev` out of the FUTURE block with `reachability:
      HISTORICAL_EVIDENCE` and `population: ROLLING`, so a refusal record
      legitimately citing a rev that no longer resolves — D4's whole point —
      stops reading as a broken pin); xFactory #362 -> `119280a8` (install
      `pyyaml`, `jsonschema>=4.18` and `referencing` explicitly with an import
      check, and `CHECK_WAIT_SECONDS` 900 -> 2400); openxFactory #830 ->
      `202c170d` (the candidate's `path_allowlist` admits the exact file
      `ideation/cross-reference.yaml` — the register every applied
      `dispose-possible` writes by construction — so an APPLIED disposition
      can be approved at all); and xFactory #369 -> `c2313277` (an unreadable
      check-runs gather is NAMED in one rate-limited `::warning::` instead of
      silently normalising to "one pending" and burning the whole wait).

      AND THE FLIP IS OBSERVED, NOT ASSERTED. `intents/rolling` — refreshed
      once by MERGING `main` into it under ruling D-9 (a) (`6da1bd0e`, the
      kept refusal commits preserved) — landed on `main` as openxFactory PR
      #176 -> `7681e409` (2026-09-09T06:37:45Z), carrying the real applied
      intent `e970dfec` and the real refusal `36d07ecf` among five committed
      `*.gate-intent.yaml` records. The chips and the refusal panel now read a
      feed that exists on `main`, which is exactly what "against GET intents"
      asked for and what no descriptor-only tray could have produced.

      NOT DONE HERE, AND SAID PLAINLY: the lane re-adds a three-line
      `possibles_register` header comment absent from `main`'s committed
      register and never regenerates `ideation/cross-reference.md`, so the
      RENDERED projection trails the register by one disposition. It is
      recorded for a docs-projection successor (the #768 family) on
      openxFactory #656, not fixed by this box.)
- [x] 4.5 Flutter verdict-terminal client consumes the same two endpoints
      (own feature; contract fixed here).
      (DEFERRED SUCCESSOR — RULED 2026-09-05T23:38Z by Brett Heap ("rule
      path A, 4.5 is a deferred successor", openxFactory #656
      https://github.com/opensoft/openxFactory/issues/656#issuecomment-5555554097):
      the Flutter verdict-terminal client is outside this change's
      completion bar; the two endpoints' contract is fixed here and
      unchanged; the client is raised as its own successor change when
      wanted.)

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

**DISPOSITION 2026-09-09 — WHAT KIND OF TICK EACH OF THE THREE REMAINING BOXES
IS, AND WHAT IS NOT CLAIMED BY THEM.** § 4.4, § 5.1 and § 5.2 all tick ON THE
DOING: the work exists in merged commits, in green live runs, and in this pull
request's own diff, and each box names them so a reader can check rather than
trust. **NO BOX TICKS ON A WORD THAT HAS NOT BEEN GIVEN.** Path A itself was
ruled by Brett Heap, 2026-09-05T23:38Z, verbatim *"rule path A, 4.5 is a
deferred successor"* (openxFactory #656), and the live exercise by his ruling
D-2; the SEPARATE word to LAND this archive is asked for in the pull request
body and is not claimed anywhere in this file. **§ 4.5 IS NOT RE-DISPOSITIONED
HERE**: it stands exactly as PR #714 -> `3d1b8cce` encoded it under that same
ruling — a DEFERRED SUCCESSOR, raised as its own change when wanted — and this
archive neither ticks it as work performed nor moves its text by a byte.

- [x] 5.1 End-to-end proofs: forged-actor ignored; unauthorized verb refused
      at inbox; stale-view refused at lane; atomic commit shape; hosted and
      local dispositions produce equivalent records; serving pod remains
      credential-free (boundary suite).

      (TICKED ON THE DOING, IN TWO HALVES — THE SUITE AND THE LIVE EXERCISE —
      AND NEITHER HALF IS CLAIMED FROM THE OTHER.

      THE BOUNDARY SUITE — openxFactory PR #727 -> `07624d5e`
      (2026-09-06T23:31:47Z), "Intent plane 5.1 (PR-4): the boundary suite —
      six proofs in one place, with the hosted-equals-local equivalence".
      `tests/ideation-dashboard/test_intent_plane_boundary.py` (598 lines)
      states the six proofs ONE-TO-ONE with the sentence above, each named
      after the clause it discharges: `test_forged_actor_is_ignored`,
      `test_unauthorized_verb_is_refused`, `test_stale_view_is_refused`,
      `test_applied_atomically`, `test_hosted_and_local_equivalent`,
      `test_serving_pod_is_credential_free`. Five of the six already held
      SOMEWHERE — two in Omnigent-Install's inbox and deployment suites, three
      in this repository's lane and route suites — and nowhere as one
      statement; proof 5, the hosted-equals-local equivalence, did not exist
      anywhere and is new here. The file writes every proof from the position
      that the inbox told the truth about NOTHING except which
      ingress-authenticated user it stamped, which is design D2's own reading
      of a compromised inbox, and it names rather than copies the two ingress
      halves that belong to Omnigent-Install.

      THE LIVE EXERCISE — RULED D-2 BY BRETT HEAP AND RUN END TO END ON QA
      AKS, six real dispatches over 2026-09-08/09, recorded run by run on
      openxFactory #656. It is the half the suite cannot give: a suite proves
      the boundary is written, a live run proves it holds against the real
      cluster, the real Apps and the real branch protection.

        * A REAL REFUSAL (act B, the D4 stale view, verbatim the ratified
          scenario): xFactory `intent-apply` run **34229563533**
          (2026-09-08T13:02:35Z, conclusion `success`) refused with "the
          cross-reference index did not exist at 3fd3e33e…" and committed
          `36d07ecf` on `intents/rolling` — ONE `*.gate-intent.yaml` refusal
          record, no gate-action, no register change. Fail-closed, complete,
          and the refusal is the artifact.
        * A REAL APPLY (act A, third dispatch): xFactory `intent-apply` run
          **34306919288** (2026-09-09T03:23:16Z, conclusion `success`) applied
          `dispose-possible` on
          `pos-derived-governed-kill-switch-custody-contract` for actor
          `brett` and committed `e970dfec` (2026-09-09T03:23:42Z,
          `openxfactory[bot]`) — THREE files in ONE commit, which is the
          atomic shape the box names: `ideation/cross-reference.yaml` +10 (the
          target gains `human_disposition: {outcome: deferred, authority:
          brett, …}`), one `*.gate-action.yaml` (provenance `surface:
          intent-plane`, `console_presence: ingress-auth`) and one
          `*.gate-intent.yaml` (`status: applied`).
        * THE AUTONOMOUS APPROVAL AND MERGE, which no test can stand in for:
          the custody-only re-run xFactory `intent-apply` run **34319843472**
          (2026-09-09T06:36:34Z, `workflow_dispatch`, `success`) read #176's
          head `e970dfec` nine settled check-runs within seconds with the
          content App's new `Checks: read`, and dispatched openxFactory
          `merge-master-approval` run **34319868940** (2026-09-09T06:36:53Z,
          `success`): the codeXfactory token was minted with `pull_requests:
          write` only, the envelope evaluated `approve: true`
          (`already_approved: false`), **`codexfactory[bot]` submitted an
          APPROVED review at 2026-09-09T06:37:22Z**, and GitHub's auto-merge
          merged **PR #176 into `main` as `7681e409` at
          2026-09-09T06:37:45Z**. `reviewDecision: APPROVED`; the org rulesets
          (18962101, one approving review; 18834180, code-owner review) were
          satisfied by the App's review alone, as the merge-master spec
          intends.

      WHAT THE EXERCISE ALSO PROVED, BY FAILING FIRST: five earlier runs
      PARKED or REFUSED and every one of them parked with a NAMED reason —
      `required_check_not_green: check-run 'lane-line' concluded 'skipped'`,
      `check-run 'pytest-suite' is in_progress`, `failed_condition:
      path_allowlist — paths outside allowlist … ['ideation/cross-reference.yaml']`
      — and none of them approved anything. A gate that refuses eight times
      for eight different stated reasons before it approves once is better
      evidence for this box than a gate that passed first time. Each of the
      eight is named with its fixing merge commit in § 4.4.

      THE CREDENTIAL-FREE POD, RE-READ AT THE LIVE RUN rather than only in
      the suite: the dashboard pod carries no credential and the tray posts
      same-origin only; the ONE credentialed component is the inbox, and the
      dispatch token it mounts is `Actions: write` on `opensoft/xFactory`
      alone. Task 4.2's readiness walk recorded the same six checks against
      the live ingress under CIR `cir-opensoft-qa-dox-intent-plane`.)
- [x] 5.2 Keep the README "OpenSpec Records" entry current through
      ratification, realization, and archive.

      (TICKED ON THE DOING, AT THE LAST OF THE THREE MOMENTS THE BOX NAMES.
      The row was added in the proposal commit at RATIFICATION (task 1.3
      records it, 2026-07-23) and carried its realization state through the
      change's active life. THIS PULL REQUEST TAKES THE THIRD MOMENT: the
      README "OpenSpec Records" row moves from the `Active changes:` block to
      the head of `Archived changes:`, repointed at
      `openspec/changes/archive/2026-09-09-add-ideation-intent-plane/proposal.md`
      and rewritten to state what archived, on whose word, on what evidence
      and what was promoted. `scripts/proposal-support.py … archive` does NOT
      move that row — it is a hand edit in the archive commit, the shape every
      recent archive in this corpus used (`26c2661b`, `ca4a1558`) and a
      substrate row under the Rule 6 landing window.

      The per-change sweep-ledger row in
      `tests/sequenced_after/corpus-ledger.yaml` flips `state: active` ->
      `state: archived` in its own commit, re-seeded with the tool
      (`scripts/validate-sequenced-after.py . --seed-ledger --moved-by
      '#<this PR>'`) rather than by hand, because the `--moved-by` pull request
      number does not exist until the pull request does. That is the same
      "keep the record current" duty this box names, in the register that
      reads the README's answer back.)
