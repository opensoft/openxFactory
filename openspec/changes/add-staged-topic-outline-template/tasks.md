# Tasks: add-staged-topic-outline-template

Sequenced in PARALLEL with `doxbench-editing-model` Phase A (Brett, 2026-08-15).
The decision half is done — all five questions accepted as recommended — so what
remains is the contract and the surface.

## 1. The template contract

- [x] 1.1 Write the canonical template into `docs/document-lifecycle.md`: the
      three required sections, the four-sub-field open-question shape, the
      `Added-by:` provenance rule, and the `xspec:` marker wrapping. The fenced
      skeleton already exists in the staging fragment — carry it verbatim rather
      than re-deriving it, so the ratified text and the drafted text cannot drift.
      Landed as `## The Staged-Topic Outline Template`. The 99-line skeleton was
      EXTRACTED programmatically rather than retyped, and the carry is proven
      byte-identical by sha256 rather than asserted. Also superseded the marker
      bullet that said staged fragments "need no inline markers" — true for
      QUEUING, no longer the whole story now that conforming fragments wrap
      proposal-element sections in the same ratified `xspec:` grammar.
- [x] 1.2 State the round-trip-on-demote rule as a testable property, not a
      description: a demoted fragment's proposal-element sections carry the last
      attempted `proposal.md` text, the change id, both dates, and the reason.
      Written as "the load-bearing rule", stating the testable question in the
      prose itself — does a demoted fragment's slot carry the prior change's
      real text — so the reason it is a requirement and not a convention is on
      the page rather than only in the proposal.
- [x] 1.3 Record Q1's ruling where the next reader will meet it — `primaryFragmentPath`
      is unchanged and the one-path rule is preserved, not extended. The function's
      own docstring is the right place; anyone proposing a second candidate file
      will read it there first.
      States that the `outline.md` alternative was PUT AND DECLINED, that a
      future second candidate is a reversal needing its own ruling rather than a
      patch to the list, and that doc-health's `_primary_fragment` mirrors this
      selection — change both together or neither.

## 2. Doc-health conformance nudge

- [x] 2.1 A warning-tier check: a staged topic's primary fragment carries the
      three required sections and every open question carries four sub-fields.
      Landed as doc-health family `staged-topic-template`. `_primary_fragment`
      mirrors `primaryFragmentPath` in wheel-model.js exactly — exact
      `<topic>.md` first, else shallowest markdown, path-only and never
      content-sniffed — so the checker and the wheel can never disagree about
      which file a topic's outline IS.
- [x] 2.2 REQUIRED for topics staged after ratification, OPT-IN before it. The
      discriminator is the topic's own staging date, not the file's mtime — an
      opt-in topic that gets touched for an unrelated reason must not silently
      become required.
      Needed a new git primitive: `first_commit_date`. The existing
      `last_commit_date` is the wrong signal by exactly the failure this task
      names — age uses the last touch, obligation uses the first. An unknown
      date is treated as opt-in, never required.
- [x] 2.3 Never gate-blocking (Q2). A finding here is a nudge; assert that in a
      test, because the default instinct on a new family is to fail the gate.
      Every finding is WARNING even where conformance is REQUIRED — the
      required/opt-in distinction lives in the rule TEXT, which is what a reader
      acts on, rather than in a severity that would fail a run under
      `--fail-on error`. Asserted by
      `test_non_conformance_is_never_gate_blocking`, and proven on the real
      corpus: the full doc-health run exits 0 with 29 new warnings and no new
      errors. Escalating this family needs a new ruling, which the code says.

## 3. The outline tab

- [ ] 3.1 Render identified sections from headings and `xspec:` fences. No
      content-sniffing, no fabricated headings.
- [ ] 3.2 Add-section affordance writing through `edit-apply`, scoped by the
      target section; `Added-by:` provenance stamped on the added section.
- [ ] 3.3 Degrade on non-conforming fragments: render what is present, report
      nothing as broken, rewrite nothing on open.
- [ ] 3.4 Gate-off posture: the affordance is not a live control and no write
      path is reachable.
- [ ] 3.5 Leave the outline buffer's seeding, hashing, dirty-state and Save
      semantics untouched — this is presentation and addressing only. A diff in
      `BUFFER_KINDS` or the save order means the change has overreached into
      `doxbench-editing-model` Phase B's territory.

## 4. Tests

- [ ] 4.1 Template conformance: required sections present; a bare question with
      no recommended answer is non-conforming.
- [ ] 4.2 Round-trip: demote a fragment that reached proposal and assert the
      proposal-element sections carry the real prior text, not the aspirational
      original. This is the requirement's whole point and the one test that must
      not be a shape assertion.
- [ ] 4.3 Opt-in boundary: a pre-ratification topic warns and does not block; a
      post-ratification topic is required.
- [ ] 4.4 Outline tab: sections identified from headings/fences; add-section
      goes through `edit-apply` with provenance; non-conforming fragment renders
      without rewrite; gate-off offers no live control.

## 5. Gates

- [ ] 5.1 `OPENSPEC_TELEMETRY=0 openspec validate add-staged-topic-outline-template
      --strict`, then `--all --strict`, from the `openxFactory/` root.
- [ ] 5.2 `python3 -m pytest tests/ideation-dashboard -q` and
      `tests/doc-health` — exit codes read directly, never through a pipeline.
- [ ] 5.3 doc-health full run: 0 new regressions beyond the new warning family's
      own intended findings, which should be enumerated rather than counted.
- [ ] 5.4 Live proof in a browser: open a conforming topic and a pre-template
      topic in the outline tab, add a section to the conforming one, confirm the
      commit lands through `edit-apply` on the session branch.

## 6. Bookkeeping

- [ ] 6.1 README "OpenSpec Records" active block.
- [ ] 6.2 Tick the staging topic's exit and mark the INDEX row proposed.
- [ ] 6.3 Hand Q4's ruling to `doxbench-editing-model` Phase A — `edit-apply` is
      the verb, so Phase A's chat edits become marker-scoped section patches.
      That upgrade belongs to Phase A, not here; this task is the handoff, not
      the build.
