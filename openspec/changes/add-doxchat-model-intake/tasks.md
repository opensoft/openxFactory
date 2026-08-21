# Tasks: add-doxchat-model-intake

## 0. Ratification and unblocking

- [ ] 0.1 Brett rules OQ-3: does approval require a Hermes consent instrument,
      or is a recorded gate action enough? This decides whether the approval
      record carries a `consent_ref`, so it must settle before 3.2.
- [ ] 0.2 Brett confirms OQ-4: the empty-catalog default selection is the
      intake affordance even though the send control stays refused. Asked for
      explicitly; confirm against the live console once 1.x exists.
- [ ] 0.3 Brett rules OQ-5: the approval act sits in the intake flow's last
      step rather than on the gate console.
- [ ] 0.4 BLOCKING DEPENDENCY: `add-model-provider-broker` lands and a broker
      (openProfiler) declares its CLI surface. Nothing in sections 2 and 3 can
      be built before this, and section 1 must not ship without it (the
      ship-with-the-flow requirement). OQ-1 (first provider) and OQ-2 (OAuth
      flow location) are answered there, not here.

## 1. The selector (small, and deliberately NOT shippable alone)

- [ ] 1.1 The intake affordance renders as the FIRST option in
      `doxbench-chat.js`, ahead of every catalog entry, carrying a value that
      is not a model id and cannot collide with one.
- [ ] 1.2 Empty catalog selects it by default; a non-empty catalog defaults to
      an available model instead.
- [ ] 1.3 The send control's refusal and the rail's no-approved-model sentence
      stay BYTE-IDENTICAL. Pin this with an assertion, not a reading — the
      existing suites already pin that sentence and they must keep passing
      unchanged.
- [ ] 1.4 The affordance is NOT offered on either `catalogFailure` rung in
      `staging-workbench-model.js`, nor on the hosted/read-only plane.
- [ ] 1.5 Route-side: a turn naming the affordance's value refuses through the
      EXISTING absent-model refusal. No new failure code.
- [ ] 1.6 The affordance is not rendered at all when the broker is
      unavailable, and the selector's behaviour is then indistinguishable from
      today's. A test proves the indistinguishability.

## 2. The intake flow

- [ ] 2.1 The flow opens from the affordance, offers the two authentication
      kinds (`api_key`, `oauth`), and refuses with a stated reason when no
      broker is declared — presenting no field that would accept a secret.
- [ ] 2.2 API-key path: the value goes to the broker and only the returned
      reference is retained, in a binding of the shape
      `xfactory_credential_binding_template` owns.
- [ ] 2.3 OAuth path: the dashboard hands off to the broker's authorization
      flow and receives a credential reference. It never receives an access
      token, a refresh token, or an authorization code.
- [ ] 2.4 THE GREP TEST: after a completed intake, the whole checkout, the
      plane state directory, every response body, and every log line are
      searched for the supplied value and it is found nowhere. This is the
      test that makes the requirement real; write it before 2.2.
- [ ] 2.5 No intake surface reaches a provider endpoint. The structural
      provider-boundary check keeps passing unchanged — this change does not
      narrow it, `add-model-provider-broker` does.

## 3. Proposed, then approved

- [ ] 3.1 A completed intake produces a PENDING declaration plus its binding,
      disclosed as pending and contributing NO available catalog entry.
- [ ] 3.2 The approval act: an explicit act by the resolved local human actor,
      persisted as a gate action naming the declaration and carrying issuer,
      approver, expiry, and audit reference (plus `consent_ref` iff 0.1 says
      so). Agent invocation refuses and is reported, like every gate action.
- [ ] 3.3 ADDITIVE contract release: one new `action` enum member on
      `contracts/schemas/gate-action-record.schema.yaml` plus its `allOf`
      conditional. Allocated AT REALIZATION per
      `docs/contract-versioning-policy.md` — reserve no minor number now.
      Do NOT reuse an existing member.
- [ ] 3.4 A turn naming a declared-but-unapproved model refuses before any
      provider call, because the entry is not available.
- [ ] 3.5 The closed seven-field public catalog entry does NOT widen. Assert
      it: proposed-versus-approved stays server-side.

## 4. Evidence

- [ ] 4.1 Live-console proof on the real serve: empty catalog shows intake
      first and selected; the rail sentence is unchanged; a completed intake
      leaves a pending entry; approval makes it selectable; a turn runs.
- [ ] 4.2 Realization evidence recorded per `release-realization`. This change
      has a code surface, so it archives only on merged plus green — never on
      authoring alone.
