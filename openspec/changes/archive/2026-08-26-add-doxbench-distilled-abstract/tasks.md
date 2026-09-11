# Tasks: add-doxbench-distilled-abstract

RED-FIRST throughout, with ONE declared exception: every behavioural pin is
written and seen to FAIL before the code that satisfies it exists, EXCEPT §6,
whose items are labelled GUARD because ruling 2(b) makes them green on the first
run by construction and their teeth come from mutation 9.5 instead. Pins are
behavioural — a test that only asserts a string is present in a source file is a
spelling test, and the one place a source-text assertion is legitimate here is
the purity/import guard the repo already uses.

Sequencing: **§1 does not start until `ratify-doxbench-landed-context-surfaces`
has archived** (this change's `:863` delta is authored against its landed text).
The provider-boundary delta was originally authored relative to the outcome of
the ratified `add-doxchat-model-intake`, which modifies the same requirement; on
2026-08-26 that ordering was REVERSED (1.2/1.2a) — this change archives FIRST and
intake now declares relative to THIS change's outcome
(`release-realization/spec.md:64-74`).

## 1. Gate and ground

- [x] 1.1 Confirm `ratify-doxbench-landed-context-surfaces` is archived and that
      the canonical `doxBench scoped view` text matches the base this change's
      delta was authored against; if it drifted, re-author the delta against what
      landed rather than editing canon.
      2026-08-25 — BOTH HALVES ALREADY VERIFIED by that change's own §3.4 at
      archive time: it is archived at
      `openspec/changes/archive/2026-08-25-ratify-doxbench-landed-context-surfaces/`,
      and this change's MODIFIED `doxBench scoped view` block was compared line
      by line against the canon it promoted — every canon line and all SIXTEEN
      canon scenarios are present here, and this block diverges ONLY by its own
      declared additions (it strikes "a new analysis," from the closing sentence,
      appends the paragraph narrowing the no-new-ANALYSIS clause to the
      bullseye's geometry and the completeness signals, and adds the two
      scenarios that take it to 18). NO DRIFT, no re-authoring owed. Re-confirm
      and tick when §1 actually starts.
- [x] 1.2 Confirm the INTAKE FOLD still matches `add-doxchat-model-intake`'s
      delta at archive time. This change's `:1045` text is canon PLUS intake's
      additions (the one-non-model-INTAKE-affordance paragraph, the widened
      "browser loads model choices" bullet, the "The intake affordance is
      submitted as a model" scenario, and the "Hosted doxBench is opened"
      intake-affordance-absence bullet) PLUS this change's own widening. The
      fold is ASYMMETRIC, not mutual: archive replaces canon's block with the
      archiving delta's raw markdown, no merge. This change's delta already
      carries intake's text, so this change archiving second is safe; intake's
      delta does NOT carry this change's EVERY-MODEL-CONSUMER widening or its
      four added scenarios, so intake archiving second would revert them.
      ORDERING CONSTRAINT: `add-doxchat-model-intake` MUST archive BEFORE
      `add-doxbench-distilled-abstract`.
      2026-08-25 — intake's hosted-plane bullet folded per #351.
      **2026-08-26 — THE FOLD DIRECTION IS REVERSED, and the ordering constraint
      above is WITHDRAWN.** The asymmetry analysis holds; the ordering it
      concluded does not. `add-doxchat-model-intake` stands at 0/22 tasks with a
      real code surface (selector, intake flow, broker hand-off, an additive
      gate-action enum member) and a BLOCKING dependency on
      `add-model-provider-broker`, so its archive gate — merged plus green
      (`release-realization/spec.md:23-32`) — cannot be met for a long time. This
      change is realized NOW (#365 `02477d40`, #386 `d4740415`, pytest-suite green
      on main, operator run recorded at §10.3), so waiting on intake would hold a
      realized change open indefinitely; and archiving THIS change with intake's
      text folded in would promote into canon an intake affordance that DOES NOT
      EXIST in the code — a promoted spec describing what the code does not do,
      which is the exact invariant `release-realization` protects. So: this
      change's block is re-authored as canon PLUS ITS OWN additions only (the
      three intake sentences, the widened selector bullet, the intake scenario
      and the hosted-plane intake bullet all REMOVED from it), and intake — the
      LATER archiver — is re-authored as (canon + this change's widening + this
      change's four scenarios) + intake's four additions. That is the direction
      `release-realization/spec.md:64-74` asks for in the first place: the later
      proposal declares its deltas relative to the earlier change's OUTCOME.
      Verified mechanically the same day: this change's block minus canon is
      exactly its own two widened sentences, its three added sentences and its
      four added scenarios (34 → 52 lines); intake's block carries every line of
      this change's block except the one selector bullet it deliberately widens,
      plus exactly its four additions (52 → 60 lines).
- [x] 1.2a 2026-08-25 — intake's delta re-authored against canon (#351, landed on main via PR #358, 87d0b95a); the remaining hazard is ORDER: intake archives first (see 1.2).
      2026-08-26 — SUPERSEDED with 1.2: the order is flipped, THIS change archives
      first, and intake's delta is re-authored a second time — no longer against
      bare canon but against this change's landed outcome. Its own tasks carry the
      matching Amendment Record entry and its delta header now states the base it
      is authored against, so nothing about the flip depends on reading this file.
- [x] 1.3 (2026-08-25 — valid; --all --strict 78/78; README entry present.) `OPENSPEC_TELEMETRY=0 openspec validate add-doxbench-distilled-abstract
      --strict` and `--all --strict` green; README OpenSpec Records entry present.
- [x] 1.4 (2026-08-25 — N1–N5 carried verbatim into every apply-wave agent brief.) Re-read `clarifications.md`. N1–N5 are constraints, not suggestions:
      N1 forbids sharing the chat `TurnStore`, N5 forbids relying on the default
      fake for verifier coverage.

## 2. The adapter is reachable at all (do this FIRST — nothing else is visible)

- [x] 2.1 RED: a server built by the ENTRYPOINT path resolves a port whose
      `catalog()` discloses AT LEAST ONE AVAILABLE ENTRY. Non-`None` is not the
      bar: `OmpHarnessBridge`'s `catalog` defaults to `EMPTY_CATALOG`
      (`doxbench_model.py:719`), so a bare declaration would resolve, disclose
      nothing, and look like a working install. Fails today —
      `_workbench_model_port` returns `None` at `serve.py:1546-1547`.
- [x] 2.2 Declare `model_port_factory` at the REAL entrypoint: `cli.py:298`'s
      `serve_mod.build_server(...)`, beside `adapter_factory` (`:304`) and
      `knowledge_declaration` (`:311-312`). `serve()` (`serve.py:4833`) has NO
      CALLERS, so its `setdefault` block gets the same declaration only as the
      standalone secondary path. Supply all three install-time inputs the
      constructor needs — the CATALOG as a declaration constant beside the
      knowledge declaration, `session_root` as an entrypoint CLI flag, and a
      `LaunchConfig` carrying `provider_id` and `command` (the shape at
      `tests/ideation-dashboard/test_doxbench_bridge_live.py:145-146`). NOTHING
      becomes a per-request or per-turn parameter: `_workbench_model_port` calls
      the factory with NO arguments (`serve.py:1549`). GREEN 2.1.
- [x] 2.2a RED then GREEN: the factory returns ONE PROCESS-LIFETIME INSTANCE —
      two requests resolve the SAME object (identity, not equality), and no
      adapter child is started twice. `_workbench_model_port` is called per
      request (`serve.py:2162`, `:2700`) and the bridge is stateful
      (`_sessions`/`_selected`, `doxbench_bridge.py:900-901`), so a per-request
      construction would break `spec.md:1991`'s one-session-per-document-thread
      rule by construction.
- [x] 2.2b Confirm the two absence pins still pass unchanged —
      `test_doxbench_request_handling.py:696` and `:727` inject
      `model_port_factory` into `build_server` directly, so an entrypoint
      declaration leaves them `None`.
- [x] 2.3 Add `omp` to `tests/hermeticity.py`'s `GUARDED_BINARIES` (`:91`) and
      prove the shim refuses it. THREE places iterate that tuple and must be
      updated in the same commit:
      `tests/ideation-dashboard/test_hermeticity.py:63` and `:75` (both
      `@pytest.mark.parametrize` over `GUARDED_BINARIES`) and
      `tests/notebooklm/test_hermeticity_guard.py:43`. The refusal is stamped
      `MARKER = "FR-043"` (`tests/hermeticity.py:95`), a NotebookLM requirement
      id that would MISLABEL an `omp` refusal: either generalize the marker or
      document the mislabel in that module. Alternative if this proves too
      wide: pin instead that every abstract test injects its own `spawn=`.
- [x] 2.4 Correct BOTH stale statements now — not "with the first call site",
      because a real `dispatch` call site already exists at `serve.py:3422`, so
      both are false today: the banner at `serve.py:2128-2134` ("no code below
      calls it") and `_workbench_model_port`'s docstring at `:1542-1544` ("no
      route below calls it ... the dispatch arm is T051's").
- [x] 2.5 Handed over from `ratify-doxbench-landed-context-surfaces` (§2.7):
      write the missing PIN for the lens tablist's arrows/Home/End
      reachability. `test_doxbench_context_panes.py:166-175` checks `role`,
      `aria-selected` and `tabIndex` only; the behaviour lives at
      `staging-workbench.js:491-503`. Also correct the stale comment at
      `staging-workbench.js:508` ("ABOVE the always-present matrix") and the two
      stale wheel-is-deferred assertions that change recorded
      (`test_doxbench_context_panes.py:19-25` docstring and `:217-229`
      `test_the_deferred_wheel_is_recorded_where_the_selector_stands`).

## 3. Prompt assembly (non-chat), RED-first

- [x] 3.1 RED: `build_prompt_envelope` refuses an abstract-shaped request —
      demonstrate the chat-shape barrier concretely (no outline buffer, no human
      message) rather than asserting it in prose.
- [x] 3.2 RED: identical construction input yields byte-identical rendered prompt
      bytes; and the envelope carries EXACTLY ONE subject section — no layer-1
      packet, no second buffer, no transcript. Check through `port.dispatched`.
- [x] 3.3 RED then GREEN: `build_abstract_envelope` REFUSES a `ContextPacket`
      handed to it, of ANY declared purpose. Do NOT add a new
      `PACKET_PURPOSE_*`: an abstract request carries no packet, so
      `require_valid` would never run and the constant would be dead code. The
      refusal to pin is "this request carries no packet", not "this packet has
      the wrong label".
- [x] 3.4 Implement `doxbench_turns.build_abstract_envelope` with its own
      section-order constant. GREEN 3.1–3.3.
- [x] 3.5 RED then GREEN: the output bound is tighter than
      `MAX_ASSISTANT_PROSE_BYTES` (`doxbench_turns.py:80`) and an over-long
      response is refused, not truncated into the region.

## 4. `DocumentAbstract` and its verifier

- [x] 4.1 RED: constructing a `DocumentAbstract` with any `authority` other than
      non-authoritative, or any `regenerable_from` other than the document,
      refuses at construction — the guarantee is structural, as it is for
      `DocumentThread` (`doxbench_threads.py:619`).
- [x] 4.2 RED (hand-seeded `dispatch_result`, per N5): an abstract mentioning no
      declared topic and no declared destination is REFUSED, verified against the
      SNAPSHOT'S fields on the FIRST generation with no previous abstract present.
- [x] 4.3 RED: an abstract naming a repository path absent from its own request is
      refused; an abstract naming the wrong subject is refused; an abstract naming
      the subject's own path passes.
- [x] 4.4 RED: a verification failure renders NOTHING and states a refusal — it is
      never silently downgraded to rendering unverified text.
- [x] 4.5 Implement the type and verifier in `doxbench_knowledge.py`. GREEN
      4.1–4.4. Name the check `subject-mention coverage` in the code, and add a
      comment saying why it is not fidelity (`dispatch_turn` returns one opaque
      string, `doxbench_model.py:985`).
- [x] 4.6 Assert UNCHANGED: `test_doxbench_packet.py:920-921` still passes with
      `layer(2).owner == "doxbench_threads.compact_thread"`, and
      `assert_fidelity(2, FIDELITY_LOSSLESS_BY_REFERENCE)` still raises. The
      sibling class must not have touched layer 2's ownership.

## 5. The route and the store

- [x] 5.1 RED: the new route is refused on a non-loopback plane, with no gate
      capability, and with no resolved actor — the same three-part verdict the
      catalog and turn routes sit behind.
- [x] 5.2 RED: the route refuses a subject outside `projection.editable_paths`
      with a stated reason and reaches no provider (ruling 7(a)).
- [x] 5.3 RED: a separate bounded store, keyed by `(scope, subject path,
      content digest, resolved model id)`; one in-flight per key with
      attach-and-wait; identical-key replay with no second dispatch FOR A
      REQUEST CARRYING NO REFRESH INTENT; a changed digest is a NEW key and not
      a conflict; eviction is deterministic and not clock-ordered. (The SCOPE is
      in the key per the 2026-08-25 adversarial review's S3; the RESOLVED MODEL
      ID per the same day's packet review, task 5.3a. Both corrections land in
      one five-field `AbstractKey` — see design D5.)
- [x] 5.3a RED then GREEN (2026-08-25): the MODEL is in the key. Same subject,
      same digest, DIFFERENT resolved model id → a second dispatch against the
      newly resolved model, and the first model's prose is NOT replayed under
      the second model's recorded id. Asserted on `port.dispatched` and on the
      returned `DocumentAbstract.model_id`, not on the store's internal dict.
      The routing-rule case is pinned too: `auto` and the model it resolves to
      are ONE key, so the second request REPLAYS — key on the rule's id instead
      and every routed abstract collides in one bucket while sharing none with
      the plain model's. `AbstractKey` is now five fields, `(repository, ref,
      subject_path, content_digest, resolved_model_id)`; the route resolves
      through `doxbench_selected_model` — the same one function the chat wire
      record and thread sidecar read — ONCE, and keys AND records by that value,
      so the key and the recorded provenance are the same facts. THE CLIENT
      HALF LANDED WITH IT: `staging-workbench.js`'s session cache is keyed by
      the model too (else a browser replaying its own prose after a switch never
      asks the server at all and the server's correct key is never consulted),
      and the rail's model choice now repaints the docs region — without that
      the DOM kept the previous model's prose under the model-derived caption.
      The client keys on the REQUESTED id, which is the only one it can know
      before asking; the entry still carries the RESOLVED id the answer echoed.
      Where NO model is selectable at all (ruling 7.7's ungated console) the
      lookup falls back to this document's most recent answer under any model,
      because "any already-generated abstract SHALL remain readable" outranks a
      qualification that has nothing to disambiguate.
- [x] 5.3b RED then GREEN (2026-08-25): an EXPLICIT REFRESH bypasses completed
      replay — realized as one OPTIONAL boolean `refresh` inside the same CLOSED
      request shape (an unknown key is still refused, and `1`/`"true"` are
      MALFORMED rather than truthy; both halves pinned). Only the RE-GENERATE
      control sends it; GENERATE, the mount, a selection change and a tile
      re-entry send nothing, and a re-entry does not reach the route at all.
      `AbstractStore.reserve(key, refresh=True)` invalidates the completed
      entry, takes the in-flight slot and dispatches, and the answer replaces
      the entry. The invalidated `DocumentAbstract` rides back on the lease as
      that generation's PREVIOUS verification base: the ratified rule makes a
      previous abstract an ADDITIONAL base "where one exists", and RE-GENERATE
      is the one path where one always does, so dropping it at the moment of
      invalidation would have made the refresh path verify against a strictly
      weaker base than every other path. The ATTACH path is deliberately not a
      refresh path — a caller that WAITED replays the holder's answer rather
      than invalidating what it just waited for. The original obligation, in
      full: same subject,
      same digest, same model, RE-GENERATE invoked → the completed entry is
      invalidated, a second dispatch occurs, and the new result replaces the
      entry. Then the negative half, which is what stops the bypass becoming a
      free-for-all: a second refresh while the first is still in flight ATTACHES
      (one dispatch, not two), and re-entering the tile replays with NO dispatch
      because a re-entry carries no refresh intent. Without 5.3b the RE-GENERATE
      control the spec requires is inert whenever content and model are
      unchanged, which is the ordinary case it exists for.
- [x] 5.4 RED (N1, explicitly): abstract activity over a scope larger than the
      cache bound MUST NOT evict the chat surface's turn-idempotency records.
      Assert against the chat `TurnStore`'s own contents.
- [x] 5.5 (2026-08-25 review: the route dispatched the bridge UNBOUND — first call of every
      process was model_failed and later calls landed in the chat document's harness session
      (canon :2026). Fixed: the abstract binds ITS OWN JSON-composed conversation key
      ("doxbench-abstract", scope, subject_path) via for_conversation before dispatch; a bind
      failure refuses and releases the store key. Proven against the real OmpHarnessBridge with
      the fake child. request_paths ∩ (editable ∪ context); AbstractKey scope-qualified.)
      Implement the route beside `_workbench_model_port` and the store.
      GREEN 5.1–5.4.
- [x] 5.6 RED then GREEN: the response echoes the subject path and digest it was
      generated for.

## 6. Snapshot non-interference (both directions)

**These pass on the first run under ruling 2(b), and that is the point.** They
are REGRESSION GUARDS, not RED-first pins: with generation session-local there is
nothing to make them fail today, so every item below is labelled GUARD and NOT
RED — a reviewer who saw RED here would rightly expect a baseline failure that
cannot exist. What proves they have teeth is the mutation round: 9.5 (a CONSTANT
abstract emitted into a document object) breaks 6.2 — and only 6.2, since a
constant emission is byte-identical in both arms of 6.1 by construction; 9.5b (a
document field derived from whether a session generation happened) is what 6.1's
genuine without-generation arm catches. Measured 2026-08-25: 9.5b survived all
five guards until that arm was added. Do not mark this section done without
running both.

- [x] 6.1 GUARD (green on the first run): the generator produces BYTE-IDENTICAL
      snapshots for one unchanged tree, once with abstracts generated in-session
      and once without.
- [x] 6.2 GUARD (green on the first run): no snapshot field carries a
      model-derived value — assert over the emitted document objects, not over
      the schema.
- [x] 6.3 GUARD (green on the first run): with the port absent, raising, and
      timing out, the snapshot is unaffected and no lane or gate action fails.

## 7. Renderer, interaction, accessibility

- [x] 7.1 RED: spinning the docs wheel across N documents dispatches ZERO model
      calls. This is the pin the whole interaction design exists for —
      `doc-wheel.js:205-212` fires `onSelect` on every notch and `:463` at mount.
- [x] 7.2 RED: a generation that resolves against a subject the pane no longer has
      selected is DISCARDED UNRENDERED, and the region shows the
      not-yet-generated caption for the current subject.
      (2026-08-26 — REFINED by the operator run. DISCARDED is a rule about a
      SUCCESS: it carries prose, and prose painted under the wrong caption is
      the defect. A REFUSAL or ERROR answering the subject the request was
      DISPATCHED for is RECORDED against that subject and renders on it when it
      is next shown — never on another — because it carries no prose to paint
      wrongly, and dropping it was what made a refused generation look like a
      control that did nothing. An answer NAMING A DIFFERENT subject than the
      dispatched one is discarded whole and recorded against neither. The echo
      is tested against the DISPATCH, so the recheck and the store key ask one
      question.)
- [x] 7.3 RED: the in-flight state is cancellable and states its wait bounded by
      the ADAPTER'S OWN `port.timeout_seconds` — the value the chat path reads
      through `validated_timeout_seconds` (`serve.py:3416-3417`), which the bridge
      defaults to `60.0` (`doxbench_bridge.py:881`) — and NOT by
      `MAX_ADAPTER_TIMEOUT_SECONDS = 120` (`doxbench_model.py:54`), which is the
      validated ceiling. Pin an adapter declaring 60 and assert the region does
      not state 120.
- [x] 7.4 RED: a dirty loaded subject is captioned as describing the SAVED
      version, and no unsaved buffer text appears in the dispatched envelope
      (check `port.dispatched`).
- [x] 7.5 RED: exactly ONE abstract REGION exists and one abstract STATE renders
      at a time, the deterministic one opens, and the 280px budget rule at
      `test_doxbench_context_panes.py:231-240` still holds.
- [x] 7.6 RED then GREEN: an abstract survives leaving and re-entering the tile
      in-session, keyed by (path, digest, resolved model id), and the re-entry
      issues NO refresh intent — the replay path and the bypass path are pinned
      as two different things here and at 5.3b. (The (path, digest) half was
      GREEN on 2026-08-25; #364 widened it, and the model-id and no-refresh
      halves landed the same day: a model switch shows NOT-YET-GENERATED and
      switching back replays the first model's abstract with no new request,
      while a tile re-entry sends no request at all — so there is nothing for an
      inferred intent to ride on.)
- [x] 7.6a RED (ruling 3): when the subject's content has moved past the digest
      an abstract was generated from, the abstract is SHOWN and LABELLED STALE
      with its source digest stated — not discarded, not silently refreshed, not
      presented as current.
- [x] 7.6b RED (ruling 3): for an UNLOADED subject the source digest is the
      digest of the SERVED SAVED CONTENT, and the per-buffer settled-identity
      guard is not required of it. Pin both an unloaded subject and a loaded one,
      because the escalation rule is the difference between them.
- [x] 7.7 RED: with no gate capability the generation control is ABSENT, and an
      already-generated abstract stays readable.
- [x] 7.8 **§8.1 and §8.3 must land BEFORE this task.** The relocated captioning
      pin has to exist before any caption containing "Distilled" is written, or
      this task knowingly reds the old whole-file sweep at
      `test_doxbench_context_panes.py:144-152` and leaves the section boundary
      broken on purpose. Then implement: the pure formatter beside
      `documentAbstract`
      (`staging-workbench-model.js:1545`), the controls and states in
      `staging-workbench.js`, and ONE fetch call site in `web/app.js`. GREEN
      7.1–7.7. (STATED ADJUSTMENT, second instance, 2026-08-25: task 5.3a's
      client half made the docs abstract follow the rail's MODEL choice, which
      grew the rail mount call's `onState` by ten lines and pushed
      `selectBuffer:` off the far edge of the flat 5000-character window at
      `test_doxbench_tile_verbs.py:747` — a pin whose claim was perfectly
      intact. Re-anchored at BOTH ends, from the mount call's opening to the
      line past its close, exactly as the sibling pin in the same file was
      re-anchored by this change. Teeth re-proved: renaming `selectBuffer:` to
      `unloadBuffer:` inside the call still fails it.)
- [x] 7.9 Widen `test_renderer.py:152` from 5 to 6 `app.js` fetch sites and
      declare the new route BY NAME in the `:129-133` docstring. Then confirm the
      view's THREE transport asserts still pass —
      `test_staging_workbench.py:795` (`"fetch(" not in view`), `:796`
      (`"POST" not in view`, modulo the prose escape) and `:797`
      (`"XMLHttpRequest" not in view`) — plus the model module's own
      fetch-and-import guard at `:798-801`. The transport stays in `app.js`.
- [x] 7.10 ONE region whose accessible name COMPOSES the subject's title/path
      with the provenance caption of the state shown, so the deterministic and
      model-derived states are distinguishable BY NAME; the name changes when the
      state switches. House idiom preserved
      (`test_doxbench_accessibility.py:281-311`). Replace the static
      `aria-label` `"selected document"` at `staging-workbench.js:250` — this
      change owns that line; the split change cut the rename because it needs
      code — and assert the region is never announced as the selected document.

## 8. The captioning pin, inverted not deleted

**Ordering:** 8.1 and 8.3 run BEFORE §7.8. Everything else in this section can
follow the captions it describes, but the pin relocation cannot — see 7.8.

- [x] 8.1 Move the pin off the whole-file sweep at
      `test_doxbench_context_panes.py:144-152` and onto the node harness fixture
      (`:83-94`) as a per-abstract CAPTION FIELD assertion.
- [x] 8.2 Pin all five captions with their declared carriers: model-derived and
      deterministic as visible text AND part of the region's accessible name;
      stale, ungenerated and hosted-plane as visible text inside a named region.
- [x] 8.3 Rewrite the module docstring's scope statement (`:26-29`) to RECORD the
      2026-08-03 → 2026-08-25 reversal rather than erase the old ruling. Leave the
      `:31-34` operator-rig note standing.
- [x] 8.4 Pin that the deterministic abstract is never captioned as a
      distillation — the half of the old guard that stays true.

## 9. Mutation rounds

- [x] 9.1 Mutate the verifier: invert each refusal in turn (coverage, foreign
      path, wrong subject) and confirm a NAMED test fails for each.
- [x] 9.2 Mutate the interaction: make generation fire from `onSelect` and confirm
      7.1 fails; remove the subject recheck and confirm 7.2 fails.
- [x] 9.3 (2026-08-25 — SEVEN mutants, all caught, all reverted; md5 verified
      clean afterwards.) Key on path and digest alone → 4 fail, including the
      whole-scope pin and all three model pins. DROP THE MODEL (a constant in
      its place) → the three 5.3a route pins fail. Key on the REQUESTED id
      rather than the RESOLVED one → the routing-rule pin and the key-readback
      pin fail, and only those, which is the discrimination that clause is for.
      Refresh a NO-OP (fall through to completed replay) → 3 store pins and the
      5.3b route pin fail. Refresh SKIPS the one-in-flight arm → both
      attach-and-wait pins and the route's one-model-call pin fail. Two CLIENT
      mutants beside them: drop the model from `abstractEntryKey` → the two
      model-switch pane pins fail; make RE-GENERATE issue no intent →
      the refresh-intent pane pin fails. Share the chat `TurnStore` (one
      instance bound to both handler attributes) → 5.4's churn pin and the
      own-store pin fail. A shared records dict across store instances also
      fails `test_two_stores_share_no_state`.
- [x] 9.4 Mutate the boundary: point the abstract at a `context_paths`-only
      subject and confirm 5.2 fails; add a fourth port member and confirm
      `test_doxbench_model.py:482`/`:522` fail.
- [x] 9.5 (2026-08-25 — REVIEW ROUND added four more mutants, all caught: dispatch the RAW
      unbound port (4 route pins incl. the real-bridge leak pin and the bind-failure store-key pin); bind-failure leaving the store
      key held (attach-and-hang pin); ctx.dirtyFor→false (mounted dirty-buffer pin);
      MAX_ABSTRACT_PROSE_BYTES 1500→2000 (absolute budget pin). a CONSTANT emission is caught by 6.2 only, byte-identical in both arms by
      construction; the session-derived emission 9.5b survived until 6.1 gained a genuine
      without-generation arm — pin added. 7.2 likewise gained the not-cached assertion after
      9.2b survived it.) Mutate the snapshot: emit the abstract into a document object and
      confirm 6.1 and 6.2 both fail.
      (2026-08-26 — FIX-ROUND MUTANTS on the visible-refusal path, all caught:
      key the error recording on the CURRENT subject (`session.subject.path`)
      instead of the DISPATCHED `path` → the refusal-renders-where-it-was-asked
      pin and the foreign-answer pin both fail; drop `!foreign` from the
      recording guard (`if (!succeeded)`) → the dropped-whole pin fails; move
      the recording ABOVE the token check → the cancelled-wait pin fails; drift
      `ABSTRACT_PROSE_WORDS_APPROX_BYTES` to 1_400 → the word-cap/byte-gloss
      coherence pin fails. The N3 defect was found by writing its pin first: a
      SUCCESS echoing a foreign path that equals the CURRENT subject passed the
      old recheck and was then cached under the DISPATCHED path — one document's
      prose filed under another's name — and the pin was RED until the recheck
      took `foreign` into account.)

## 10. Realization gate

- [x] 10.1 `pytest tests/ideation-dashboard` green. 2026-08-25 — 4390 passed / 13 skipped; after the review fix round 4412 / 13; 4442 / 13 after the #364 catch-up; 4447 / 13 after the final polish round.
      Whole-repo `pytest tests/ -m "not postgres"`: 6416 passed, 2 pre-existing failures
      unrelated to this branch (doc-health bootstrap-cluster drift; hermes release
      inventory merge-base in a worktree) — CI on the PR is the authority.
- [x] 10.2 `OPENSPEC_TELEMETRY=0 openspec validate --all --strict` green. 2026-08-25 — 78/78; 77/77 after merging main (one change archived there).
- [x] 10.3 **ONE OPERATOR RUN on the real corpus through a REAL adapter** — the
      bridge lane (§2.2), or the T100 rig's operator-supplied adapter. Record the
      subject document, the model, the returned abstract, and the verifier's
      verdict. **Record it at
      `openspec/changes/add-doxbench-distilled-abstract/realization-evidence.md`**
      — one paragraph carrying subject, model, abstract, verdict, date and
      operator. A green suite against `FakeWorkbenchModelPort` alone does NOT
      close this change: the fake returns a constant
      (`doxbench_model.py:1101`).
      2026-08-26 — **CLOSED by Attempt 2.** Operator Brett, at the local console
      served by `~/doxbench-operator/t100_serve.py` (the T100 subscription
      adapter over the `claude` CLI — the second of the two adapters this item
      allows; `omp` is not installed on that host, so the bridge lane was not
      reachable and this run evidences none of it). Corpus checkout at main
      `d4740415`, i.e. AFTER the #386 fix. Subject
      `ideation/staging/avatar-pilot-hardening/avatar-pilot-hardening.md`,
      content digest `20b36eb3…be505a`; model as evidenced by the adapter's
      dispatch record `claude-haiku-subscription.low`; answer 1119 bytes, inside
      the 1_500-byte bound. The pane rendered it under the ruled model-derived
      caption beside both controls — `caption_state: model-derived`, verifier
      ACCEPTED, no refusal class. `generation` and `wait_bound_seconds` were not
      captured and are recorded as not captured, not invented. Attempt 1
      (2026-08-26, four failed presses) is kept in the file: it closed nothing
      and found the two defects `change/abstract-length-cap-and-visible-refusal`
      fixed.
- [x] 10.4 Confirm `.openspec.yaml`'s origin is unchanged since ratification — the
      archive gate re-reads it (`release-realization/spec.md:97-103`).
      2026-08-26 — RE-CONFIRMED at archive time: the blob is byte-identical to
      the one at ratification commit `1ccb2ae0` (`428e06ed` both sides), and the
      file's whole history is its single creation commit `5c547610`.
- [x] 10.5 Archive. `target_release: none` means no bundle is cut; it does NOT
      mean doc-only, and the merge-plus-green gate still applies
      (`release-realization/spec.md:23-32`).
      2026-08-26 — ARCHIVED as
      `openspec/changes/archive/2026-08-26-add-doxbench-distilled-abstract/`.
      Gate, each arm checked rather than asserted: code MERGED on main (#365
      `02477d40`, #386 `d4740415`, both contained in `origin/main`); CI GREEN on
      main — `pytest-suite` concluded `success` at `d4740415`; the OPERATOR RUN
      recorded at §10.3 and in `realization-evidence.md`; origin UNCHANGED
      (§10.4 — blob `428e06ed` identical to ratification commit `1ccb2ae0`);
      `openspec validate --all --strict` green before and after. Promotion:
      three requirements MODIFIED and seven ADDED — canon went 88 → 95
      requirements and 404 → 444 scenarios, matching this delta exactly (+3/+4/+2
      on the modified blocks, +31 across the seven added), with 85 requirements
      byte-identical and none removed. The provider-boundary block promoted is
      this change's own and carries NO intake text: grep for `INTAKE affordance`
      and `intake affordance is submitted` over promoted canon returns 0, which
      is the point of the 1.2 reversal.

## 11. Speckit handoff

- [ ] 11.1 EXACTLY ONE feature: `specs/015-doxbench-distilled-abstract` (RENUMBERED
      2026-08-25: `specs/014-register-and-reader` landed on main via 9374b16b while this
      change was in apply; 015 is the next free number).
      `specs/013-*` is claimed by `013-first-wallet`. **Do not create it here** —
      it is created by the Speckit flow when implementation starts.

## Bookkeeping correction (2026-09-11, `split-opendox-two-layer-product` § 5.9) — carry-forward

Edited (bookkeeping): 2026-09-11 by split-opendox-two-layer-product — carry-forward annotation

This packet's `specs/ideation-dashboard/spec.md` delta stays the record, unedited and unaugmented by anything below. The `ideation-dashboard` capability's artifacts — the `scripts/ideation_dashboard/` tree, `web/`, `tests/ideation-dashboard/`, the packaged examples under `examples/ideation-dashboard/`, the five dashboard governance docs, and the five dashboard contract schemas — were SHED from `openxFactory` by `split-opendox-two-layer-product` § 5.2, `opensoft/openxFactory` PR #940 → `cc4ae9d35b2dbd56743c8c19699fd685d4e49343` (merged 2026-09-11). They are now consumed at a pin from the `openDox`/`openXdox` legs per `docs/opendox-carve-manifest.yaml` (destinations `opendox_spec`, `opendox_code`, `openxdox_spec`, `openxdox_code`; `contracts/opendox-pin.yaml`, `contracts/openxdox-pin.yaml`). The five contract schemas associated with the `ideation-dashboard` capability — `gate-action-record`, `ideation-dashboard-snapshot-index`, `ideation-dashboard-snapshot`, `xfactory-workbench-chat-turn`, `xfactory-workbench-model-catalog` — were DEPRECATED at `contract-v3.7` (`opensoft/openxFactory` PR #970 → `45bd9ee250ad1125f9227ad511bee0fec2b16306`, tag `ec3c17292c6dc2ca6004d158d6cc26bf5e6523e2`, merged 2026-09-11) and are slated for removal from the bundle at `contract-v4.0` (§ 5.7; cut PR `TBD-CUT-PR`, a placeholder the landing lane fills in when the cut lands). Ruled by Brett Heap, 2026-09-11 20:27Z, session `openXfactory-4 (5)`, on `opensoft/openxFactory`#656 comment `5640246046` (§ 5.9), realizing `split-opendox-two-layer-product` `tasks.md` § 5.9 — "ANNOTATE the 30 archived changes carrying an `ideation-dashboard` delta with the carry-forward." Nothing this packet asserts is changed by this annotation; immutable records are annotated, never edited into agreement.
