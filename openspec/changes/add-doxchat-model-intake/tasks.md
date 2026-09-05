# Tasks: add-doxchat-model-intake

## 0. Ratification and unblocking

These four are RECORDING ACTS, not new decisions. 0.1–0.3 were ruled on
2026-08-21 in an in-session multiple-choice round and the rulings are already in
the proposal's Open Questions; each is ticked here by citing its RULED line
verbatim, so the build's own record names the sentence it was built to.

- [x] 0.1 Brett rules OQ-3. RULED, and quoted from the proposal verbatim:
      **"RULED (2026-08-21, Brett, in-session multiple choice): recommendation
      adopted — split by install. A recorded gate action suffices on the
      single-operator loopback console; a consent instrument is REQUIRED where
      the model is enrolled on a tenant or shared install or where a turn will
      process another party's material, and only that case carries
      `consent_ref` on the approval record."**
      BUILT AS RULED, in both directions: `model_approval.install_posture`
      states which install the approval was made on, and two schema
      conditionals REQUIRE `consent_ref` on `shared` and REFUSE it on
      `single-operator` — "only that case carries" read as the two-sided rule it
      is. `doxbench_intake.ModelDeclaration` refuses the same two constructions
      at the dataclass, so the settings document and the record cannot disagree.
- [x] 0.2 Brett confirms OQ-4. RULED, verbatim: **"RULED (2026-08-21, Brett,
      in-session multiple choice): recommendation adopted — the intake
      affordance IS the empty-catalog default selection, consequence accepted as
      stated; confirm the reading against the live console once the flow
      exists."**
      BUILT AS RULED. The consequence is accepted rather than hidden: with an
      empty catalog the selector shows a selected option that is not a model
      while the rail says no approved model is configured. The
      confirm-against-the-live-console half is 4.1's, and 4.1 is OPEN.
- [x] 0.3 Brett rules OQ-5. RULED, verbatim: **"RULED (2026-08-21, Brett,
      in-session multiple choice): recommendation adopted — the approval act is
      the intake flow's own explicit last step, recorded as an approval."**
      BUILT AS RULED: `swb-model-intake.js` renders the approval as the flow's
      last step, and `POST /actions/workbench/model-approval` records it. No
      route to a separate gate console exists, which is the point — routing a
      human who just authorized a subscription elsewhere to finish would make
      the pending state a trap rather than a safeguard.
- [x] 0.4 BLOCKING DEPENDENCY — DISCHARGED 2026-08-26, with evidence on both
      sides of the seam:
      * `add-model-provider-broker` MERGED (openxFactory PR #392, main
        `bb7d7ae8`), which is this build's base commit. It landed
        `doxbench_binding.py`, `doxbench_provider.py`, the settings verbs in
        `cli.py`, `declared_model_port_factory`, and the
        `test_model_provider_broker.py` / `test_provider_boundary.py` /
        `test_openprofiler_broker_e2e.py` suites this change builds on and
        leaves passing unmodified;
      * the BROKER declared its CLI surface: openProfiler PR #18, main
        `d0538c31`, `docs/broker-cli.md` — the `intake`/`mint`/`revoke`/`list`
        subcommand vocabulary, the flag names, and the answer shapes
        `doxbench_provider` is reconciled against.
      OQ-1 (provider-agnostic; the binding's `provider` field carries the
      answer) and OQ-2 (the broker's own surface is the OAuth redirect target)
      were answered there and are honoured here rather than re-decided: no
      provider is named in any code path, and the OAuth kind reaches the
      broker's own `intake` rather than any authorization flow of this
      dashboard's invention.

## 1. The selector (small, and deliberately NOT shippable alone)

- [x] 1.1 `INTAKE_OPTION_VALUE` (`__doxchat_intake__`) renders as the FIRST
      option, ahead of every catalog entry AND ahead of the placeholder. It
      belongs to no provider's namespace, so it cannot collide with a
      provider-declared `model_id`.
- [x] 1.2 Empty catalog selects it by default (`defaultSelectorValue`); a
      non-empty catalog defaults to an available MODEL, performed by the rail as
      a real selection (`withDefaultModel`) rather than as a rendered value the
      send gate would disagree with.
- [x] 1.3 PINNED WITH AN ASSERTION. The rail's sentence is compared against the
      view's own constant, and both the offered and the not-offered rungs are
      asserted to carry it with Send disabled. The existing chat-view, privacy,
      transport, renderer and staging-workbench suites all pass UNMODIFIED.
- [x] 1.4 Not offered on either `catalogFailure` rung — asserted over the
      ladder's source, rung by rung — nor on the hosted/read-only plane, where
      the rail is not mounted at all and the surface route refuses on the same
      `session` verdict the catalog route uses.
- [x] 1.5 No new failure code exists, and the server does not know the
      affordance's value: a test asserts the literal is ABSENT from `serve.py`,
      so a turn naming it can only reach the existing unknown-model refusal.
- [x] 1.6 Not rendered at all when the flow is unavailable, and a test proves
      the indistinguishability on the RENDERED control: no intake option in the
      list, the placeholder selected, and the selector disabled exactly as
      before this change.

## 2. The intake flow

- [x] 2.1 The flow opens from the affordance through the shell's `openIntake`
      seam into `swb-model-intake.js`. Both kinds are offered, READ FROM
      `doxbench_binding.AUTH_KINDS` and served rather than spelled in the page —
      a test sweeps every browser module for the api-key spelling and finds
      none, because the absolute views clause forbids exactly that vocabulary.
      With no broker declared the surface answers `offered: false` with
      `NO_BROKER_NOTICE` and discloses NO kinds at all, so the page has nothing
      to build a secret-accepting field from.
- [x] 2.2 The value reaches `doxbench_provider.hand_off_credential` — the
      existing enrolment path, unchanged — and only the returned `reference` is
      retained, on the nine-field binding record that has no field a secret
      could occupy. Proven against a REAL broker program the test writes and
      invokes exactly as an operator's declaration would.
- [x] 2.3 OAuth reaches the broker's own `intake` with an EMPTY source and
      receives a reference where a broker implements the flow. Today's declared
      broker refuses before reading standard input at all, and this console
      surfaces that honestly through `OAUTH_UNAVAILABLE_NOTICE`: no redirect is
      invented, no field for token material is presented, and nothing is stored.
      The dashboard receives no token of any kind and no authorization code —
      structurally, because it never becomes the redirect target.
- [x] 2.4 THE GREP TEST is written and passing: after a completed intake AND a
      completed approval, the whole checkout tree, both response bodies, and
      this process's own stdout and stderr are searched for the supplied value
      and it is found NOWHERE. The broker's own record IS checked to contain it,
      because a sweep that found it nowhere at all would be proving the hand-off
      never happened.
- [x] 2.5 `test_provider_boundary.py` passes UNMODIFIED (99 assertions across it
      and the broker suite). No intake module names a provider endpoint, and the
      one-module exemption is untouched — this change does not narrow the
      boundary and did not need to.

## 3. Proposed, then approved

- [x] 3.1 A completed intake writes the binding AND a PENDING
      `model-declaration` (`ideation/dashboard/model-declarations.yaml`),
      disclosed with `PENDING_NOTICE`. `declared_model_port_factory` passes over
      a pending binding exactly as if it were not declared, so it contributes NO
      available catalog entry. A binding the declarations document says nothing
      about is UNAFFECTED — the hand-declared operator path is byte-identical,
      and inverting that rule would have retroactively unapproved every install
      that already works.
- [x] 3.2 `POST /actions/workbench/model-approval`, under the reused `session`
      local-human verdict beside `_workbench_model_port`. It writes the
      gate-action record BEFORE the settings document moves — a crash between
      the two leaves an audit record for an approval that did not take effect,
      which is recoverable, rather than an available model no record accounts
      for. The record carries `model_approval` with issuer, approver, expiry and
      audit reference, plus `install_posture`; `consent_ref` exactly as 0.1
      rules. Agent invocation refuses with the fixed `console_required` sentence
      and is REPORTED on stderr, asserted on all three routes.
- [x] 3.3 ADDITIVE contract release **contract-v1.45**, allocated AT
      REALIZATION on the merge order this build found (v1.44 was the tip).
      `action` gains `approve-model` — a NEW member, never a reused one — plus
      its `allOf` conditional, and the two optional properties that conditional
      requires (`target.model_declaration`, `model_approval`). Manifest bundle
      version bumped, both changed rows' `sha256` recomputed, both
      `consumption_rule`s extended, one CHANGELOG entry cut, and
      `contracts/releases/contract-v1.45.digests.yaml` built by
      `validate-contract-release.py build` and shipped inside the cut.
- [x] 3.4 Structurally, and at the ONE seam where availability is decided: a
      pending binding never becomes a catalog entry, so `selectable_entry_for`
      cannot vouch for it and the turn route's existing unknown-model refusal is
      the only arm reachable — before any provider call, because the catalog is
      consulted before dispatch.
- [x] 3.5 ASSERTED: after a completed intake and approval, every entry the wire
      projection carries has exactly the seven `PUBLIC_ENTRY_FIELDS`, and the
      count is asserted to be seven. Proposed-versus-approved lives in a SECOND
      record beside the binding, never as a tenth field on it.
- [x] 3.6 THE MID-TURN RE-MINT IS VISIBLE IN THE TURN RECORD. Brett ruled
      2026-08-26 that when a minted token expires part-way through a turn the
      dashboard re-mints and retries ONCE, "with the re-mint and the paid retry
      VISIBLY RECORDED in the turn record" — a second paid call the human cannot
      see is exactly the decision that ruling was made to avoid. HANDED HERE BY
      `add-model-provider-broker` (its task 2.4, PR #392 review note c) because
      THIS change owns the released turn-record surface and carries a
      `target_release` that can pay for a schema act.

      BUILT AS THE TASK'S OWN BODY SPECIFIED: an ADDITIVE OPTIONAL fact on the
      v2 success envelope ONLY — `provider_retry`, in contract-v1.45's cut
      alongside 3.3, so ONE release act pays for both. The v1 envelope is
      untouched, because it is deprecated and its promise is byte-identical
      stability. The block carries the REDACTED fact and nothing more:
      `retried` and `at_most_once` (both `const: true`, so no `retried: false`
      spelling exists and an absent object is the only way to say "nothing to
      report") plus the mint's `audit_ref`, which the broker's declaration
      guarantees carries no token material. `additionalProperties: false`, with
      a packaged negative proving a fourth key is refused.

      HOW THE FACT REACHES THE ENVELOPE WITHOUT WIDENING ANYTHING ELSE, which
      was the hard half: `dispatch_turn` still refuses any adapter answer whose
      key set is not exactly `{assistant_prose, proposals}`, and the port's
      member surface is still exactly the declared three. The turn route reads
      the port's already-existing content-free `ledger` — DUCK-TYPED through
      `mint_ledger_snapshot`, so an adapter without one contributes nothing and
      nothing about its turns changes — before and after the dispatch, and
      `provider_retry_fact` derives the fact from the delta.

      WHAT THE DELTA HONESTLY MEASURES, stated rather than over-claimed: the
      ledger is one object shared by every turn a process dispatches, so what
      the record says is that a re-mint and one further paid provider call
      happened WHILE THIS TURN WAS DISPATCHED. On the single-operator loopback
      console this surface is gated to, with at most one turn in flight per
      conversation, that coincides with "this turn's own". The contract's
      description says so in those words, because a record that over-claimed
      would be worse than one that measures something slightly wider.

      AND IT REACHES THE HUMAN, which is the whole point of the ruling: the
      browser adopts it in `settleTurnSuccess` (fail-closed — absent, malformed
      or `retried !== true` adopts as null) and the rail renders
      `PROVIDER_RETRY_NOTE` on a polite live region beside the context-posture
      note, so a screen-reader user hears it too. The console also logs a line
      naming the client turn id, so an operator can join the paid retry to the
      conversation that bought it without opening a browser at all.

## 4. Still owed — the live console, and the realization evidence

- [ ] 4.1 Live-console proof on the real serve — OPEN, and open honestly. This
      build had no browser available, so it was discharged as far as a headless
      run can discharge it and no further.

      PROVEN HEADLESSLY, over a REAL ephemeral serve against a REAL scratch
      corpus with a REAL broker program
      (`tests/ideation-dashboard/test_doxchat_model_intake.py`):
      * `GET /workbench/model-intake` answers `offered: false` with the stated
        reason and NO authentication kinds where no broker is declared, and
        `offered: true` with both kinds and the dialect vocabulary where one is;
      * every one of the three routes refuses an agent invocation with the fixed
        `console_required` sentence AND reports it on stderr;
      * a completed intake hands the value to the broker (asserted on what the
        broker RECEIVED), keeps only the reference, and leaves a PENDING
        declaration that contributes no available catalog entry;
      * the approval writes the gate-action record, the record validates against
        the released schema, and only then does the model appear in the catalog
        as available;
      * the grep test finds the supplied value nowhere in the checkout, in
        either response body, or in this process's own output;
      * the RENDERED selector, against the same minimal DOM stub the chat-view
        suite uses: the affordance is the first option and the selected one on
        an empty catalog, the rail's sentence and Send's refusal are unchanged,
        a populated catalog defaults to a model, choosing the affordance opens
        the flow and moves no selection, and with no flow the control is
        indistinguishable from today's.

      A NOTE ON WHAT "REAL SERVE" MEANS ABOVE, because the distinction matters
      to whoever finishes this task: the routes were driven over real HTTP
      against the server object `build_server` returns — the same object
      `serve()` builds — and NOT through `python3 -m ideation_dashboard.serve`
      with a browser attached. Everything a request can prove is proven; nothing
      a human's eyes can prove is.

      STILL OWED, and it needs a human at a screen: `scripts/reserve-dashboard.sh`,
      a real browser, and the five-step walk this task names end to end —
      including OQ-4's own follow-up ("confirm the reading against the live
      console once the flow exists"), which is a JUDGEMENT about how the
      selected-non-model option READS beside the rail's sentence and cannot be
      asserted by any test. A live turn through an approved brokered model also
      needs a real provider subscription, which no test environment has.
- [ ] 4.2 Realization evidence recorded per `release-realization`. OPEN BY
      DESIGN: this change has a code surface, so it archives only on merged plus
      green — never on authoring alone, and never on this build alone. The
      evidence this task will record is the merge commit, the green CI run, the
      published `contract-v1.45` annotated tag on that merge commit, and the
      aggregation-repo submodule-pin sync. 4.1's live-console pass belongs in
      the same evidence block.

## Amendment Record

- 2026-08-25 — delta re-authored against canon per #351; the block previously
  restated a pre-2026-08-22 version and would have reverted six clauses and
  two scenarios on archive.
- 2026-08-26 — delta re-authored a SECOND time, now against the outcome of
  `add-doxbench-distilled-abstract` rather than against bare canon, because the
  ARCHIVE ORDER of the two changes was reversed. Both modify
  `doxBench model catalog and provider boundary`, and archive replaces canon's
  block with the archiving delta's raw markdown — no merge — so whichever
  archives LAST must already carry the other's text. The earlier plan had that
  change carry THIS one's four additions and archive second. That is no longer
  workable, and was never the safe direction: this change stands at 0/22 tasks
  with a real code surface and a blocking dependency on
  `add-model-provider-broker`, so its merged-plus-green archive gate
  (`release-realization/spec.md:23-32`) is far off, while
  `add-doxbench-distilled-abstract` is realized now (#365 `02477d40`, #386
  `d4740415`, green on main, operator run on record) — and archiving it with an
  intake affordance NOBODY HAS BUILT written into canon would have promoted spec
  text that describes what the code does not do. So that change archived first
  carrying only its own additions, and this change, as the later archiver, now
  declares relative to its outcome, per `release-realization/spec.md:64-74`. What
  changed here is only the BASE, not this change's own content: the block still
  adds exactly the four things it always added — the
  one-non-model-INTAKE-affordance paragraph, the widened
  `The browser loads model choices` bullet, the
  `The intake affordance is submitted as a model` scenario, and the hosted-plane
  intake-affordance-absence bullet — and it now sits on top of that change's
  EVERY-MODEL-CONSUMER widening, its entrypoint-declaration and stateful-adapter
  clauses, and its four added scenarios. Task 4.2 stands unchanged: this change
  still archives only on merged plus green. **Re-verify the block against canon
  before archiving** — canon has moved once already and will move again.
- 2026-08-26 — task 3.6 added: the mid-turn re-mint's visibility in the
  browser's turn record, handed over by `add-model-provider-broker` task 2.4
  (PR #392 review note c). That change cannot carry it — the envelopes are
  released and closed and it declares `target_release: none` — and this one
  already owns the turn-record surface and an additive contract release.
- 2026-08-26 — BUILT. Sections 1, 2 and 3 are complete, including 3.6, and
  `target_release` moves from `implementation_pending` to the bundle this build
  actually cut, `contract-v1.45` — allocated at realization on the merge order
  found (v1.44 was the tip), exactly as the versioning policy requires and as
  tasks 3.3 and 3.6 both said they would be. The proposal's
  APPROVED-BUT-NOT-YET-REALIZED banner is amended to say what is now true; the
  Why, the What Changes, the Open Questions and their rulings are untouched,
  because none of them changed. 4.1 and 4.2 stay OPEN: this change still
  archives only on merged plus green, and 4.1 additionally owes a human at a
  live console. **Re-verify the delta block against canon before archiving** —
  the standing warning above, unchanged and still live.
- 2026-09-05 — the missing `## 4.` group header supplied, by
  `prepare-openspec-1.12-readiness`. Tasks 4.1 and 4.2 had always been a group
  of their own — the two acts this change still owes — but no header was ever
  written for them, so they sat physically under `## 3. Proposed, then
  approved` while their leading number said 4. OpenSpec 1.12.0's task-grouping
  check reads that as two warnings. **NOTHING IS RENUMBERED AND NOTHING MOVES:**
  the pair is cited as "4.1" and "4.2" in five places already written down —
  `proposal.md` twice, task 0.3, and this record twice above — and one of those
  places is a dated amendment, which renumbering would have falsified. The
  header is the lossless repair; the tasks, their text and their unticked state
  are untouched.
