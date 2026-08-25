# Tasks: add-doxbench-distilled-abstract

RED-FIRST throughout: every behavioural pin is written and seen to FAIL before
the code that satisfies it exists. Pins are behavioural — a test that only
asserts a string is present in a source file is a spelling test, and the one
place a source-text assertion is legitimate here is the purity/import guard the
repo already uses.

Sequencing: **§1 does not start until `ratify-doxbench-landed-context-surfaces`
has archived** (this change's `:863` delta is authored against its landed text),
and §2's provider-boundary delta is authored relative to the outcome of the
ratified `add-doxchat-model-intake`, which modifies the same requirement
(`release-realization/spec.md:64-74`).

## 1. Gate and ground

- [ ] 1.1 Confirm `ratify-doxbench-landed-context-surfaces` is archived and that
      the canonical `doxBench scoped view` text matches the base this change's
      delta was authored against; if it drifted, re-author the delta against what
      landed rather than editing canon.
- [ ] 1.2 Confirm `add-doxchat-model-intake`'s outcome for `doxBench model
      catalog and provider boundary`, and reconcile this change's delta with it.
- [ ] 1.3 `OPENSPEC_TELEMETRY=0 openspec validate add-doxbench-distilled-abstract
      --strict` and `--all --strict` green; README OpenSpec Records entry present.
- [ ] 1.4 Re-read `clarifications.md`. N1–N5 are constraints, not suggestions:
      N1 forbids sharing the chat `TurnStore`, N5 forbids relying on the default
      fake for verifier coverage.

## 2. The adapter is reachable at all (do this FIRST — nothing else is visible)

- [ ] 2.1 RED: a test asserting that a server built by the ENTRYPOINT path
      resolves a non-`None` `WorkbenchModelPort`. It fails today —
      `_workbench_model_port` returns `None` at `serve.py:1546-1547` because no
      entrypoint declares a factory.
- [ ] 2.2 Declare `OmpHarnessBridge` as `model_port_factory` at the entrypoint in
      the `build_kwargs.setdefault` idiom (`serve.py:4850`, `:4857`), so a caller
      passing its own factory keeps it. GREEN 2.1.
- [ ] 2.3 Add `omp` to `tests/hermeticity.py`'s `GUARDED_BINARIES` (`:91`) and
      prove the shim refuses it, OR pin that every abstract test injects `spawn=`.
      Prefer the former.
- [ ] 2.4 Correct the stale banner at `serve.py:2128-2134`, which asserts "no code
      below calls it" of `dispatch`. Land this WITH the first real call site, not
      before.

## 3. Prompt assembly (non-chat), RED-first

- [ ] 3.1 RED: `build_prompt_envelope` refuses an abstract-shaped request —
      demonstrate the chat-shape barrier concretely (no outline buffer, no human
      message) rather than asserting it in prose.
- [ ] 3.2 RED: identical construction input yields byte-identical rendered prompt
      bytes; and the envelope carries EXACTLY ONE subject section — no layer-1
      packet, no second buffer, no transcript. Check through `port.dispatched`.
- [ ] 3.3 Add `PACKET_PURPOSE_DOCUMENT_ABSTRACT` beside
      `doxbench_packet.py:308` and prove a packet issued for one purpose is
      refused for the other.
- [ ] 3.4 Implement `doxbench_turns.build_abstract_envelope` with its own
      section-order constant. GREEN 3.1–3.3.
- [ ] 3.5 RED then GREEN: the output bound is tighter than
      `MAX_ASSISTANT_PROSE_BYTES` (`doxbench_turns.py:80`) and an over-long
      response is refused, not truncated into the region.

## 4. `DocumentAbstract` and its verifier

- [ ] 4.1 RED: constructing a `DocumentAbstract` with any `authority` other than
      non-authoritative, or any `regenerable_from` other than the document,
      refuses at construction — the guarantee is structural, as it is for
      `DocumentThread` (`doxbench_threads.py:619`).
- [ ] 4.2 RED (hand-seeded `dispatch_result`, per N5): an abstract mentioning no
      declared topic and no declared destination is REFUSED, verified against the
      SNAPSHOT'S fields on the FIRST generation with no previous abstract present.
- [ ] 4.3 RED: an abstract naming a repository path absent from its own request is
      refused; an abstract naming the wrong subject is refused; an abstract naming
      the subject's own path passes.
- [ ] 4.4 RED: a verification failure renders NOTHING and states a refusal — it is
      never silently downgraded to rendering unverified text.
- [ ] 4.5 Implement the type and verifier in `doxbench_knowledge.py`. GREEN
      4.1–4.4. Name the check `subject-mention coverage` in the code, and add a
      comment saying why it is not fidelity (`dispatch_turn` returns one opaque
      string, `doxbench_model.py:985`).
- [ ] 4.6 Assert UNCHANGED: `test_doxbench_packet.py:920-921` still passes with
      `layer(2).owner == "doxbench_threads.compact_thread"`, and
      `assert_fidelity(2, FIDELITY_LOSSLESS_BY_REFERENCE)` still raises. The
      sibling class must not have touched layer 2's ownership.

## 5. The route and the store

- [ ] 5.1 RED: the new route is refused on a non-loopback plane, with no gate
      capability, and with no resolved actor — the same three-part verdict the
      catalog and turn routes sit behind.
- [ ] 5.2 RED: the route refuses a subject outside `projection.editable_paths`
      with a stated reason and reaches no provider (ruling 7(a)).
- [ ] 5.3 RED: a separate bounded store, keyed by `(subject path, content
      digest)`; one in-flight per key with attach-and-wait; identical-key replay
      with no second dispatch; a changed digest is a NEW key and not a conflict;
      eviction is deterministic and not clock-ordered.
- [ ] 5.4 RED (N1, explicitly): abstract activity over a scope larger than the
      cache bound MUST NOT evict the chat surface's turn-idempotency records.
      Assert against the chat `TurnStore`'s own contents.
- [ ] 5.5 Implement the route beside `_workbench_model_port` and the store.
      GREEN 5.1–5.4.
- [ ] 5.6 RED then GREEN: the response echoes the subject path and digest it was
      generated for.

## 6. Snapshot non-interference (both directions)

- [ ] 6.1 RED: the generator produces BYTE-IDENTICAL snapshots for one unchanged
      tree, once with abstracts generated in-session and once without.
- [ ] 6.2 RED: no snapshot field carries a model-derived value — assert over the
      emitted document objects, not over the schema.
- [ ] 6.3 RED: with the port absent, raising, and timing out, the snapshot is
      unaffected and no lane or gate action fails.

## 7. Renderer, interaction, accessibility

- [ ] 7.1 RED: spinning the docs wheel across N documents dispatches ZERO model
      calls. This is the pin the whole interaction design exists for —
      `doc-wheel.js:205-212` fires `onSelect` on every notch and `:463` at mount.
- [ ] 7.2 RED: a generation that resolves against a subject the pane no longer has
      selected is DISCARDED UNRENDERED, and the region shows the
      not-yet-generated caption for the current subject.
- [ ] 7.3 RED: the in-flight state is cancellable and states its wait bounded by
      `MAX_ADAPTER_TIMEOUT_SECONDS` (`doxbench_model.py:54`).
- [ ] 7.4 RED: a dirty loaded subject is captioned as describing the SAVED
      version, and no unsaved buffer text appears in the dispatched envelope
      (check `port.dispatched`).
- [ ] 7.5 RED: exactly ONE abstract region renders at a time, the deterministic
      one opens, and the 280px budget rule at
      `test_doxbench_context_panes.py:231-240` still holds.
- [ ] 7.6 RED: an abstract survives leaving and re-entering the tile in-session,
      keyed by (path, digest).
- [ ] 7.7 RED: with no gate capability the generation control is ABSENT, and an
      already-generated abstract stays readable.
- [ ] 7.8 Implement: the pure formatter beside `documentAbstract`
      (`staging-workbench-model.js:1545`), the controls and states in
      `staging-workbench.js`, and ONE fetch call site in `web/app.js`. GREEN
      7.1–7.7.
- [ ] 7.9 Widen `test_renderer.py:152` from 5 to 6 `app.js` fetch sites and
      declare the new route BY NAME in the `:129-133` docstring. Assert
      `staging-workbench.js` gained no fetch and
      `test_staging_workbench.py:798-801`'s import-free guard still passes.
- [ ] 7.10 Two regions, two DISTINCT accessible names, house idiom preserved
      (`test_doxbench_accessibility.py:281-311`); neither announced as "selected
      document".

## 8. The captioning pin, inverted not deleted

- [ ] 8.1 Move the pin off the whole-file sweep at
      `test_doxbench_context_panes.py:144-152` and onto the node harness fixture
      (`:83-94`) as a per-abstract CAPTION FIELD assertion.
- [ ] 8.2 Pin all five captions with their declared carriers: model-derived and
      deterministic as visible text AND part of the region's accessible name;
      stale, ungenerated and hosted-plane as visible text inside a named region.
- [ ] 8.3 Rewrite the module docstring's scope statement (`:26-29`) to RECORD the
      2026-08-03 → 2026-08-25 reversal rather than erase the old ruling. Leave the
      `:31-34` operator-rig note standing.
- [ ] 8.4 Pin that the deterministic abstract is never captioned as a
      distillation — the half of the old guard that stays true.

## 9. Mutation rounds

- [ ] 9.1 Mutate the verifier: invert each refusal in turn (coverage, foreign
      path, wrong subject) and confirm a NAMED test fails for each.
- [ ] 9.2 Mutate the interaction: make generation fire from `onSelect` and confirm
      7.1 fails; remove the subject recheck and confirm 7.2 fails.
- [ ] 9.3 Mutate the store: key on path alone and confirm 5.3 fails; share the
      chat `TurnStore` and confirm 5.4 fails.
- [ ] 9.4 Mutate the boundary: point the abstract at a `context_paths`-only
      subject and confirm 5.2 fails; add a fourth port member and confirm
      `test_doxbench_model.py:482`/`:522` fail.
- [ ] 9.5 Mutate the snapshot: emit the abstract into a document object and
      confirm 6.1 and 6.2 both fail.

## 10. Realization gate

- [ ] 10.1 `pytest tests/ideation-dashboard` green.
- [ ] 10.2 `OPENSPEC_TELEMETRY=0 openspec validate --all --strict` green.
- [ ] 10.3 **ONE OPERATOR RUN on the real corpus through a REAL adapter** — the
      bridge lane (§2.2), or the T100 rig's operator-supplied adapter. Record the
      subject document, the model, the returned abstract, and the verifier's
      verdict. A green suite against `FakeWorkbenchModelPort` alone does NOT close
      this change: the fake returns a constant
      (`doxbench_model.py:1101`).
- [ ] 10.4 Confirm `.openspec.yaml`'s origin is unchanged since ratification — the
      archive gate re-reads it (`release-realization/spec.md:97-103`).
- [ ] 10.5 Archive. `target_release: none` means no bundle is cut; it does NOT
      mean doc-only, and the merge-plus-green gate still applies
      (`release-realization/spec.md:23-32`).

## 11. Speckit handoff

- [ ] 11.1 EXACTLY ONE feature: `specs/014-doxbench-distilled-abstract`.
      `specs/013-*` is claimed by `013-first-wallet`. **Do not create it here** —
      it is created by the Speckit flow when implementation starts.
