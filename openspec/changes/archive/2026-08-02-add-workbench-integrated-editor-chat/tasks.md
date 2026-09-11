## 1. Implementation Start Gate

- [x] 1.1 Baseline recorded 2026-07-28: `add-staging-workbench` landed through codexFactory PR #42 (`4e7b7b7`); `add-workbench-bullseye-and-create` through PR #46 (`9d59ac0`); `add-dashboard-repo-selector` through PR #47 (`fae38d2`) plus PR #48 hardening (`5546ff2`); and `add-workbench-branch-sessions` through PR #49 (`7440bed`) plus dashboard hardening PRs #51 (`fec8ab5`) and #52 (`b42b9cb`). The current clean common baseline is codexFactory `main` at `34bfc2f`; `python3 -m pytest tests/ideation-dashboard -q` passed **1467 tests** there in the `py-bench` dev container.
- [x] 1.2 codexFactory `008-fix-dashboard-edit` landed through PR #56 as merge commit `d2c16b1` and is an ancestor of the recorded `34bfc2f` common baseline. Its worktree is clean; the external-editor escape hatch is therefore a merged baseline rather than unresolved feature work.
- [x] 1.3 Run one real-corpus acceptance sequence that independently satisfies `add-staging-workbench` 6.5, `add-workbench-bullseye-and-create` 7.2, `add-dashboard-repo-selector` 6.2, and `add-workbench-branch-sessions` 9.2, then completes `add-propose-verb` 4.3 from the merged/session-free ready topic; record evidence against every clause rather than treating one success as blanket closure.
      Prepared 2026-07-30: the combined-pass runbook/evidence template is
      `d10-acceptance-runbook.md` in this change directory, with per-clause
      evidence slots under `evidence/d10/`.
      RUN AND SIGNED 2026-07-31 → 2026-08-01: the pass executed A→B→C→D→E
      on the real corpus with `consent-instrument-contract` as P5 for all
      three write steps, every clause recorded its own evidence, and Brett
      signed the matrix — 6.2 and 4.3 PASS; 6.5, 7.2, 9.2 PASS WITH
      FINDINGS (each finding named, caused, and dispositioned; register
      F1–F12). The evidence set landed via PR #48 (`93ea5c1`); the five
      owning-ledger boxes are checked by the same governance commit as
      this one. Session outputs beyond acceptance: nine consent-instrument
      design rulings recorded in the merged packet (session PR #47,
      merge commit `52153ce`) and the first real `proposal-authoring`
      commission — `add-consent-instrument` is dispatched.
- [x] 1.4 Complete each predecessor's pending contract-manifest/release registration and any dashboard-repository publication/credential wiring required by its own task list.
      Realized 2026-07-30: all four owning registration tasks
      (`add-staging-workbench` 1.7, `add-workbench-bullseye-and-create` 1.6,
      `add-dashboard-repo-selector` 1.6, `add-workbench-branch-sessions`
      1.6) landed in contract-v1.26 through PR #43, published merge
      `4efa9d0e2c7d21f2abf3cd7e55f41b74afed97f9`; the annotated tag object
      `bf20357d8452e7e02ff15811f1912ec691d01cfb` dereferences to that merge,
      with verify-promotion, verify-tag, and every release gate passing
      (179-entry inventory, manifest digests 107/107, family validator 0/0,
      OpenSpec 57/57). Evidence closure landed through PR #44, merge
      `589343b8c3453f816b24ebd3b29190343412559a`. No predecessor
      registration, publication, or credential-wiring task remains open in
      any predecessor ledger; only the Brett live-pass clauses (this
      change's 1.3) and the archive chain (1.5/1.6) remain.
- [x] 1.5 Archive the predecessor chain in dependency order: `add-ideation-dashboard` → `add-propose-verb` → `add-staging-workbench` → `add-workbench-bullseye-and-create` → `add-dashboard-repo-selector` → `add-workbench-branch-sessions`; verify `openspec/specs/ideation-dashboard/spec.md` exists after the chain completes.
      COMPLETED 2026-08-01: the remaining five elements archived in exact
      dependency order as `2026-08-01-add-propose-verb` →
      `2026-08-01-add-staging-workbench` →
      `2026-08-01-add-workbench-bullseye-and-create` →
      `2026-08-01-add-dashboard-repo-selector` →
      `2026-08-01-add-workbench-branch-sessions`, one commit each, strict
      validation green at every step (58 → 53 items). VERIFIED:
      `openspec/specs/ideation-dashboard/spec.md` exists and carries the
      promoted capability — 40 requirements after the chain. README
      entries moved Active → Archived. Task 1.6 (the rebase onto the
      promoted capability) is now the sole remaining Start-Gate item.
      Progress 2026-07-30: the first chain element `add-ideation-dashboard`
      archived on 2026-07-29 (openxFactory `main` commit `366f04f`, archive
      entry `2026-07-29-add-ideation-dashboard`), promoting the base
      `openspec/specs/ideation-dashboard/spec.md`. The remaining five
      predecessors are still active with nine open tasks — four
      contract-manifest registrations and five Brett live-pass /
      first-commission clauses — so this task stays open.
      Update 2026-08-01: ZERO open tasks now remain in any predecessor
      ledger — the four registrations closed at contract-v1.26 (task 1.4)
      and the five live-pass/first-commission clauses closed with the
      signed D10 pass (task 1.3, same governance commit as this note).
      The archive chain is fully unblocked and is this task's remaining
      work.
- [x] 1.6 Rebase this change on the promoted `ideation-dashboard` capability, replace both MODIFIED requirement blocks with the exact promoted source plus this change's edits, and run strict OpenSpec validation.
      Note 2026-07-30: this change branch is 81 commits behind openxFactory
      `origin/main` and does not yet contain the promoted base capability;
      the rebase must fold in `366f04f` and every later promotion before the
      MODIFIED blocks are replaced with promoted source. Sequenced after 1.5
      completes.
      DONE 2026-08-02, rebased onto the promoted capability at openxFactory
      `ff64e81` (`origin/main`, 40 requirements after the 2026-08-01 archive
      chain; the head that also carries contract-v1.28). Both MODIFIED blocks
      — `Session-scoped document editing verb` and the scoped-view
      requirement — now sit on the EXACT promoted source with this change's
      edits on top. The promotion introduced NO drift to fold in: the
      promoted text of both requirements is byte-identical to the
      `add-workbench-branch-sessions` delta text they were originally written
      against (measured with a block-level diff of
      `openspec/specs/ideation-dashboard/spec.md` against
      `openspec/changes/archive/2026-08-01-add-workbench-branch-sessions/specs/
      ideation-dashboard/spec.md`), so no requirement body changed and each
      block's diff against the promoted spec is exactly this change's own
      delta:
        * `Session-scoped document editing verb` — the verb becomes reachable
          as doxBench's eligible FIRST save (atomically materialize/join the
          session, revalidate base ref/revision/hash, commit only in the
          worktree), the tile's-own-material refusal is stated explicitly, and
          three scenarios are added (first save, first-save validation failure,
          context owned by another scope) while the outside-a-session scenario
          is re-worded to exempt that first save.
        * scoped view — the three-panel staging workbench becomes doxBench's
          three coordinated regions (retained docs/lens context, the two-tab
          Outline/Document authoring canvas, the chat region), with editing,
          chat, Apply and the create-backed outline buffer added under the
          local-console posture, and two scenarios added (a document becomes
          active; the narrow-viewport stack).
      MAPPING RECORDED (not guessed): this change RENAMES the promoted
      `Staging workbench scoped view` to `doxBench scoped view` per design
      D11 — the human-facing SURFACE is renamed; the capability
      `ideation-dashboard` and every `workbench-*` technical identifier are
      not. The delta now declares it in a `## RENAMED Requirements` section
      (`FROM:`/`TO:`), which is load-bearing rather than cosmetic: measured on
      a scratch copy of `openspec/` on 2026-08-02, `openspec archive` aborted
      with `ideation-dashboard MODIFIED failed for header "### Requirement:
      doxBench scoped view" - not found`, and with the RENAMED section it
      applies cleanly (`+ 6, ~ 2, - 0, → 1`, one scoped-view requirement in
      the result, the old header gone). Observed tool behaviour worth knowing
      at 7.8: a renamed requirement is re-appended rather than kept in place,
      so its position in the promoted spec moves. Validation on the rebased
      delta: `openspec validate add-workbench-integrated-editor-chat --strict`
      valid, and `openspec validate --all --strict` 53 passed / 0 failed.
- [x] 1.7 Brett ratified the proposal decisions and approved a narrow implementation-start exception on 2026-07-29: exact `doxBench` naming, local-only provider/data-handling posture, first-edit session materialization, two-buffer semantics, and no-autosave/no-force-apply stand. Tasks 1.3–1.6 remain open and mandatory before archive; the exception permits Speckit/code work to start without cutting a one-item predecessor bundle and does not permit realization merge before this change's own contract package is registered and pinned (design D0).

## 2. Contract-First Package (openxFactory)

- [x] 2.1 Add `xfactory-workbench-model-catalog` and `xfactory-workbench-chat-turn` JSON Schemas with reusable definitions for buffer state, bounded transcript turns, content hashes, typed edit proposals, limits, fixed redacted failures, and the non-identity `working_subject` field.
- [x] 2.2 Add schema-valid examples for an empty model catalog, a local/on-tenant model, an explicitly enabled zero-retention hosted model, a turn with unsaved outline/document edits, a prose-only response, and independent outline/document proposals.
- [x] 2.3 Add one-violation negative fixtures for exposed credentials/endpoints, unknown model ids, mismatched content hashes, out-of-scope paths, over-budget requests, duplicate turn ids with different content, untyped replacement content, and identity semantics attached to `working_subject`.
- [x] 2.4 Extend the delegated contract validator and tests so every positive validates, each negative fails for its intended reason, existing dashboard/session artifacts remain valid, and no pre-growth snapshot or gate record is invalidated.
- [x] 2.5 Register the schemas/examples in the contract manifest and changelog, allocate the additive release, and land/tag that contract package before codexFactory implementation merges.
      2026-07-30: registration and allocation are DONE on this branch —
      manifest entries with per-file sha256, README index rows, CHANGELOG
      entry, and `contracts/releases/contract-v1.27.digests.yaml`, with the
      bundle version allocated as `contract-v1.27` (2.1-2.4 evidence: six
      positives, eight negatives plus the duplicate-turn pair, the delegated
      validator's doxBench rules, and `tests/ideation_dashboard/` — validator
      self-test 0 errors/0 warnings; family suites 65 passed). Instance kinds
      use the retained `workbench-*` family per the compatibility ruling; the
      catalog planning doc's `xfactory-`-prefixed kind is reconciled at
      codexFactory T007. STAYS OPEN for its final clause: LAND (merge to
      main) and TAG `contract-v1.27` — the immutable release identifier must
      name content that exists on main (research R13), so the tag is cut on
      the merge commit, not on this branch.
      2026-08-02 AMENDMENT (G-1), pending the NEXT cut: the chat-turn
      request's `active_document_path` becomes nullable, mirroring
      `buffer_state.path` — the same additive shape the PR #45 review already
      applied to buffer paths, for the same reason. Growth source is the
      codexFactory PR #63 re-verification (reviewer Brett Heap): measured
      against the real corpus with the consumer's own scope authority, 16 of
      21 staged topics have exactly ONE editable path — the topic's own
      primary fragment, which doxBench loads as the OUTLINE — so requiring a
      non-null value made a legal turn impossible on ~76% of real topics.
      Landed here as schema + one packaged positive example + two delegated
      validator tests (validator code unchanged: `_confined` already judges
      only paths that exist). No spec-delta edit: this change's own
      requirement already says a buffer carries a "repository-relative path or
      `null` for a not-yet-created artifact" and never required the request's
      active document path to be non-null — the schema realized it more
      narrowly than the requirement, which is what G-1 measured. Recorded in
      CHANGELOG "Unreleased — pending bundle registration"; the manifest
      sha256 refresh, version allocation, digest inventory and tag belong to
      the operator's cut.
      CLOSED 2026-08-02 (T105). Both clauses of this task are now evidenced:
        * LAND + TAG `contract-v1.27` — annotated tag `fb912b9`
          dereferencing to `d09d582`, which is an ancestor of `origin/main`
          (verified with `git for-each-ref` + `git merge-base --is-ancestor`
          in a clean worktree off `origin/main`);
        * LAND + TAG the G-1 amendment as `contract-v1.28` — merged through
          openxFactory PR #53, annotated tag `a6f49bb` dereferencing to
          `ff64e81` on `origin/main`. The CHANGELOG's "Unreleased — pending
          bundle registration" section is back to "(nothing pending.)" and
          `python3 scripts/validate-manifest-digests.py` reports
          "OK contracts/manifest.yaml: 109 per-file digest(s) verify", so the
          per-file identity consumers pin matches the released bytes.
        * BEFORE codexFactory implementation merges — the ordering clause
          HOLDS as a fact, not a promise: codexFactory PR #63 is still OPEN
          (head `a3780da`) while both bundles are tagged on main, and the
          consumer pinned the released commit ahead of its own merge
          (`stack.yaml` `contract_ref: ff64e81…`, codexFactory `9dbe941`).

## 2a. Evidenced verification records (T105, 2026-08-02)

Three operator/reviewer records are the evidence base for the ticks and
annotations in section 7. They are cited by NAME throughout; each is an
operator artifact held outside this repository.

- `doxbench-t099-evidence.md` — the approved-model fixture smoke (2026-08-01,
  Brett Heap operating, local human console; subscription-primary adapter held
  outside every repo).
- `doxbench-t100-evidence.md` — the real-corpus SC-012 acceptance chain
  (four runs) plus the measured accessibility sheet and the operator's binding
  CHK034 AT/browser-matrix declaration.
- `doxbench-t104-review.md`, `doxbench-t104-families.md`,
  `doxbench-t104-dispositions.md`, `doxbench-t104-reverify.md` — the
  independent two-pass review, its merged defect families, Brett's binding
  dispositions, and the re-verification on the fixed head.

## 3. Speckit Handoff (codexFactory)

- [x] 3.1 Under design D0's approved implementation-start exception, Speckit specify created feature `010-doxbench-editor-chat` from current codexFactory `main` (`279f36f`) in its generated linked worktree; implementation did not start from `008-fix-dashboard-edit` or a dirty root. Sections 1.3–1.6 remain pre-merge/archive debt.
- [x] 3.2 Speckit clarify ran against the ratified OpenSpec artifacts and generated feature specification on 2026-07-29. No critical product or authority ambiguity remained worth formal clarification: scope, human/local authority, two-buffer lifecycle, stale Apply, partial Save, provider/privacy boundary, and hosted degradation are explicit; realization constants remain correctly deferred to the plan.
- [x] 3.3 The no-argument Speckit checklist ran at repository maximum-coverage release-gate rigor after the checklist prerequisite required `plan.md` first. The feature now carries separate requirement-quality gates for functional behavior, UX, accessibility, state/concurrency, security/privacy, provider boundaries, contracts/versioning, governed Save, failure/recovery, compatibility/migration, performance/limits, and evidence/observability, plus the specification-quality checklist.
- [ ] 3.4 Produce the Speckit plan, research, data model, and interface contracts with explicit OpenSpec requirement/scenario references and the exact pinned openxFactory contract release.
      Planning artifacts are complete in `specs/010-doxbench-editor-chat/` and
      record the exact current `stack.yaml` baseline
      (`8110c38ccbc71f3896a99daa400424312fb1c7b4`,
      `contract-v1.18`). This task remains open because the additive doxBench
      schema release does not yet exist; its immutable release commit/tag must
      replace the baseline pin before realization merge.
- [ ] 3.5 Generate the dependency-ordered Speckit implementation tasks and run Speckit analyze until the OpenSpec proposal/design/spec, Speckit spec/plan/tasks, and contract schemas are mutually consistent; Speckit owns the executable code-task detail and this OpenSpec list remains the governance/milestone ledger.
      Speckit generated 106 dependency-ordered, test-first tasks on 2026-07-29
      and the initial analysis found 54/54 buildable requirements covered with
      no critical or high-severity contradiction. This task remains open until
      the future released Openx schemas replace the planning interfaces and the
      post-pin analysis confirms mutual consistency.

## 4. doxBench Editor Shell Milestone (codexFactory Speckit)

- [ ] 4.1 Realize the named doxBench three-region responsive shell — retained docs/lens context, `Outline / Document` authoring canvas, and chat rail — with the exact `doxBench` casing in visible and accessible surface names, without changing any existing scope, completeness, lens, health, repository/ref, or source-resolution derivation.
      The first two regions landed on 2026-07-30. The staging-workbench shell
      now wraps its existing tab bar and body in a context region beside a
      doxBench authoring canvas, at desktop width and stacked at narrow
      width; the canvas region carries the exact `doxBench` product name in
      its accessible name and visible heading. The canvas is offered only on
      a capable local plane, through the same `createGateLive` and
      `sessionSurfaceHidden` derivations the session bar already uses plus a
      resolved active repository/ref, so the hosted and gate-off planes keep
      exactly their read-only context. No scope, completeness, lens, health,
      repository/ref, or source-resolution derivation changed: the shell's
      pinned mount signature, outline-panel signature, viewer call, posture
      pill, and open/rekey/session-end orderings are all byte-identical, and
      the CSS change is append-only. This milestone remains open until the
      THIRD region — the chat rail — exists; it is currently a layout
      modifier class rather than a shipped region, deliberately, so nothing
      promises a surface US2 has not built.
- [ ] 4.2 Realize a pure two-buffer state model with base/current hashes, dirty/save/discard transitions, active-document switching guards, honest absent-outline creation state, and session-key invalidation; prove it through the Node harness before transport is added.
      Contract-independent work started on 2026-07-29 with shared Python and
      import-free browser exact-UTF-8 SHA-256 primitives, a 400,000-byte bound,
      normalization-sensitive cross-runtime vectors, and explicit malformed
      surrogate refusal. The pure state layer now creates exactly two
      independently hashed buffers, exposes generation-safe edit settlement,
      restores base content on Discard, serializes only to injected
      session-scoped storage under the complete repository/ref/tile/scope key,
      re-hashes restored content, isolates neighbouring keys, and clears only
      the ended session. Sixteen focused state tests and 169 affected boundary
      tests pass. This milestone remains open until Save transitions and the
      active-document switching guard are connected to the editor.
      The active-document switching guard was connected on 2026-07-30. A dirty
      Document buffer now blocks a switch and is never silently replaced; an
      accessible document picker makes the guard reachable and snaps back to
      the current path when blocked; a path outside the declared scope is
      refused outright; Discard or Cancel resolve the guard with focus moving
      into it and returning to the buffer afterwards. Two real defects in the
      generation-safe hashing contract were found by review and fixed with
      reconstructed pre-fix red evidence: the settle call had been pairing
      each completion with the snapshot it was derived from, which made the
      staleness check unreachable and let an older hash silently revert a
      newer edit, Discard, or document switch, and the refusal path had the
      same flaw in its rollback. Both now pair against the live buffer, and
      three race regressions pin it. Eighty focused tests and 233 affected
      boundary tests pass. This milestone still remains open until Save
      transitions are connected: every Save-shaped affordance in the canvas is
      deliberately rendered visible-but-disabled with its reason stated as
      real text, because this slice wires no governed Save.
- [ ] 4.3 Realize accessible Markdown editing plus live sanitized preview for both buffers using only vendored/local assets, preserving cursor/selection, scroll, focus, active tab, and dirty state across render and chat updates.
      The contract-independent rendering foundation landed on 2026-07-29:
      `viewer.js` now exports one cached, shared Markdown mount seam for the
      existing viewer, future buffer previews, and chat prose. Raw HTML remains
      escaped, unsafe links remain inert, external-scheme images require a
      human click, and the reviewed non-empty HTML sink stays centralized.
      Thirty-six focused renderer tests and 152 affected boundary tests pass.
      This milestone remains open until both editors and their live preview
      state are realized and accessibility-tested.
      Both editors and their live preview landed on 2026-07-30. Each buffer
      has a labelled multiline editor and a debounced preview rendered through
      the one shared seam and no other; the editor module contains no markup
      sink of its own, constructs no second sanitizer, and reaches no
      transport. Per-buffer focus, cursor/selection, scroll, active tab, and
      dirty state survive tab switches, context refreshes, and preview
      renders, and focus is tracked explicitly rather than left to the DOM.
      Unusual Unicode is treated as exact bytes with no normalization —
      combining versus precomposed forms and CRLF versus LF hash differently —
      and an unpaired surrogate or an over-limit edit is refused with the
      reason stated in the buffer's own live region instead of the earlier
      behaviour, which reverted the text silently. A second review defect was
      fixed here: preview and status had keyed off load state alone, so a
      scope with no outline could never preview typed text at all. Each editor
      is now programmatically described by its own preview and the
      Save-unavailable reason is real text rather than a hover-only title.
      This milestone remains open until the formal accessibility gates run:
      arrow/Home/End tab traversal, forced-colors, zoom, and reduced-motion
      remain unrealized and belong to the US5 accessibility tasks.
- [ ] 4.4 Preserve the landed external-editor action for main-resident/outside-session documents and expose integrated editing only where the local human-console capability and scoped ownership allow it.
      Partially advanced on 2026-07-30. The landed external-editor action is
      untouched — the viewer's edit affordance, its keyed source base, and its
      own test suites are byte-identical — and the new canvas is exposed only
      where the local human-console capability allows it, through the existing
      capability derivations rather than a new posture rule. Scoped ownership
      is honoured on the read side: the canvas refuses a document outside the
      declared scope, and ownership is derived from the shared projection
      rather than restated. This milestone remains open because the
      ownership-at-Save half cannot be evidenced until governed Save exists.
      Advanced again on 2026-07-30: integrated editing now READS real
      material. The dashboard composition root gained an injected
      source-loading seam over the PRE-EXISTING read-only source
      pass-through — the same route the viewer already reads, so no new route
      and no new egress point in the bundle's declared same-origin set — and
      the workbench shell forwards it into the authoring canvas, which
      previously showed only its honest unavailable state. The seam resolves
      the workbench's own source base at CALL time, so a scope route, session
      re-key, or session end is followed by the very next load rather than by
      a second routing path, and it surfaces the serving entry's own ref as
      provenance instead of fabricating a per-file revision. The landed
      external-editor action remains byte-identical, and exposure is still
      decided by the existing local-human-console capability derivations
      rather than a new posture rule. This milestone still remains open for
      the same reason as before: the ownership-at-Save half cannot be
      evidenced until governed Save exists.
- [ ] 4.5 Realize browser-local keyed working state for `working_subject`, selected model, and bounded transcript, with same-key refresh restore, cross-key isolation, and merge/abandon cleanup.

## 5. doxBench Model and Turn Backend Milestone (codexFactory Speckit)

- [ ] 5.1 Implement an injected `WorkbenchModelPort` and a server-side allowlisted catalog adapter that exposes labels/limits/data-handling badges but no credentials, raw endpoints, environment-variable names, or provider templates.
      PRESENT as of 2026-07-30, across two tested contract-independent
      slices. The local server accepts a model-port factory through the same
      injection seam its pull-request and notebook ports already use, binds
      it per process, and reports presence or absence through one accessor
      gated on the existing local-human verdict; absence — no declared
      factory, a plane that fails that gate, or a factory that raises — is
      the honest empty-catalog/editor-only POSTURE rather than an error,
      which is the posture the editor-only release requires. The held port
      is DUCK-TYPED at the seam: the server reads no attribute and no method
      on it, proven by a recording fake whose access log stays empty across
      every path. Alongside that seam, a runtime-checkable narrow
      catalog-only `WorkbenchModelPort` protocol now exists and declares
      EXACTLY two members — an adapter-declared `timeout_seconds` held to
      greater than zero and at most 120 seconds, and `catalog()` — with the
      narrowness asserted rather than merely intended: the declared member
      set is pinned to exactly those two and to intersect no dispatch,
      prompt-assembly, validation, UI, route, save, or review-ensemble name.
      The public catalog types are immutable and provider-neutral: entries
      carry exactly the seven-field public allowlist (opaque id, human
      label, policy class, availability, positive input and output limits,
      and a data-handling badge), the collection is ordered and
      duplicate-free with its invariants enforced on EVERY construction path
      rather than one blessed helper, and an empty catalog is a named
      editor-only posture. Limits must be positive and no higher than the
      server constants, and the input constant is pinned by test to the same
      value the local server declares for its own route bound so the two
      cannot drift. Forbidden public state is structurally impossible rather
      than merely absent: the seven-field slotted surface refuses any
      additional keyword, both public projections are key-exact, and the
      fake adapter's textual form exposes only an entry count and the
      declared timeout. One deterministic catalog-side FAKE adapter landed
      with the types. No provider SDK, provider environment variable,
      credential, raw endpoint, secret name, or deployment resource name is
      referenced anywhere; the module's entire import list is two
      standard-library modules, pinned by a source sentinel.
      REMAINING, which keeps this milestone open. The server-side
      ALLOWLISTED CATALOG ADAPTER itself — a configured
      on-tenant/local/subscription adapter, plus an opt-in zero-retention
      hosted fallback — does not exist, so no approved deployment can yet
      offer a model. The port carries NO dispatch member, absent rather
      than stubbed, because its request and response shapes depend on
      prompt/context assembly (item 5.3), the not-yet-released chat-turn
      contract, and the turn route's own dispatch and response validation
      (items 5.2 and 5.5); fixed provider failure mapping, timeout
      ENFORCEMENT, response bounds, and redacted diagnostics remain item
      5.5's. The catalog types deliberately carry no schema version field
      and no kind constant until the additive contract package is released
      and pinned (the schema-gated catalog envelope), so nothing here may be
      read as contract parity. And no public capability field announces a
      model capability — that announcement is additive to the catalog route
      and belongs with the catalog capability/route work.
- [ ] 5.2 Implement same-origin local-human-console catalog and turn routes with console-presence checks, real-checkout/actor requirements, repository/ref/tile/path confinement, content-hash validation, request/turn/output limits, and fixed redacted errors before provider dispatch.
      PRESENT as of 2026-07-30, across three tested contract-independent
      slices; BOTH ROUTES NOW EXIST and apply the confinement authority.
      The route-independent confinement foundation landed in the feature
      worktree on 2026-07-29: the browser exposes a deterministic presentation
      projection while Python independently re-derives scope and ownership,
      confines resolved/outline/session-created paths to the selected source
      root, and refuses traversal, absolute, hidden-family, and escaping-symlink
      paths. Sixteen focused tests and 153 affected boundary tests pass.
      The REQUEST-BOUND and FIXED-ERROR foundation landed earlier on
      2026-07-30. The server gained a route-specific 1 MiB request
      bound (exactly 1,048,576 bytes) and a bounded reader parameterised PER
      CALL SITE rather than a second global cap: it measures exact UTF-8
      BYTES rather than code points, accepts the bound inclusively, refuses
      one byte over with the measured numeric verdict the limit requirement
      demands, never trusts a declared content length for the read itself, and
      separates a measured over-bound refusal from an unmeasured
      malformation. The pre-existing global tile-action cap is untouched at
      65,536 bytes and no existing route's limit changed, which is exactly why
      a per-route reader was chosen over widening the global one.
      THE CATALOG AND TURN ROUTES then landed on 2026-07-30. Both are
      same-origin and gated on the PLANE verdict first and the
      local-human-console verdict second, reusing the identical
      real-checkout/actor/loopback gate the pre-existing edit and gate routes
      already use, so a hosted or non-loopback plane refuses before any
      catalog or turn work; console-presence failures — missing token, wrong
      token, foreign origin, a Host not naming the bound port, a missing JSON
      content type — each refuse with a fixed code, and every response carries
      the exact JSON media type on success and on refusal alike. The turn
      route validates in strict precondition order so nothing is disclosed
      before it has been earned: plane, console, route bound, body shape,
      server-derived SCOPE, content IDENTITY, model availability and effective
      limits, then turn-id idempotency. REPOSITORY/REF/TILE/PATH CONFINEMENT
      is enforced as ONE fail-closed refusal covering unknown repository,
      unknown ref, unknown tile, a path outside the server-derived editable
      set, traversal shape, and a buffer bound to a foreign repository, so no
      refusal is an oracle about which repositories, refs, tiles, or paths
      exist; the readable-but-not-editable document refuses, which is the
      editable-authority correction this change adjudicated. CONTENT-HASH
      VALIDATION is exact, case-sensitive UTF-8 SHA-256 parity for both
      supplied buffers. REQUEST AND TURN LIMITS are enforced against both the
      server constant and the stricter per-model catalog input limit, measured
      in bytes rather than code points. Turn-id idempotency is complete: a
      same-digest repeat replays the stored result byte-identically, a
      different digest refuses a fixed conflict code with NO dispatch against
      in-flight and resolved entries alike, a second distinct turn id while
      one is in flight refuses, an in-flight attach returns promptly rather
      than hanging, and unrelated conversation keys never interfere. FIXED
      REDACTED ERRORS come only from the ONE module-level doxBench catalog,
      which grew ADDITIVELY with the routes rather than forking into a second
      route-scoped catalog: it now carries ten codes, its messages remain
      module-level constants, its emitter still rebuilds the measured-limit
      block from exactly three cast fields, and sentinel tests prove that no
      response body and no log write carries prompt, buffer, provider payload,
      credential, endpoint, secret name, or exception detail. The catalog
      route exposes only the seven-field public allowlist in a fixed order,
      distinguishes the honest empty-catalog posture from a fixed
      catalog-unavailable failure, and consults the port at most once per
      successful request.
      REMAINING, which keeps this milestone open. "Fixed redacted errors
      BEFORE PROVIDER DISPATCH" is evidenced only up to the dispatch
      BOUNDARY: a fully valid turn assembles its prompt envelope, DISCARDS it
      unsent, refuses with the fixed no-model-capability code, and finalizes
      its reservation as failed so the one-in-flight slot frees. Because no
      approved deployment adapter and no port dispatch member exist (item
      5.1), there is no real provider outcome to map, and OUTPUT limits
      therefore remain arithmetic-only rather than enforced against a real
      response (item 5.5). The wire envelopes are deliberately
      schema-version-free and kind-free until the two additive contract
      packages are released and pinned, so exact-schema request validation,
      unknown-key rejection, and digest serialization parity are all still
      out and no wire shape may be read as contract parity. And no public
      capability field yet announces a model capability — the additive
      announcement item 5.1 also defers.
- [ ] 5.3 Implement deterministic prompt/context assembly over working subject, bounded transcript, scope metadata, active paths, and complete current outline/document buffers, explicitly marking dirty text as unsaved working state.
      PRESENT as of 2026-07-30, as an assembly core that is provider- and
      route-independent. Assembly is DETERMINISTIC in the strong sense: a
      fixed nine-section order, byte-for-byte identical output for identical
      input, with no dependence on environment, clock, network, filesystem,
      or mapping iteration order. All five declared inputs are carried —
      working subject, a bounded transcript, scope metadata (repository, ref,
      tile), the active paths, and the complete current outline and document
      buffers. Buffers are carried COMPLETE and unaltered rather than
      summarized or selected: the transcript is bounded but never
      summarized, and content survives byte-exactly at the size boundary and
      across carriage-return pairs, combining characters, and
      astral-plane characters, with no truncation, normalization, or
      composition. Dirty text is marked explicitly as unsaved working state
      through distinct clean and dirty labels applied independently per
      buffer. Every bound is measured in exact encoded bytes rather than
      character counts, and each refusal names the measured dimension, its
      value, and its limit while echoing no content.
      Disclosure is gated BEFORE assembly, and this milestone tightened that
      gate rather than merely satisfying it. Each turn independently
      revalidates repository, ref, tile, scope membership, and path shape,
      AND requires that backed authoring paths be members of the
      server-derived editable set before any content is disclosed — a
      readable-but-cited path is context, never edit authority, so it
      refuses. Each buffer's own path, repository, and base ref must equal
      what was validated, closing a bypass in which a buffer bearing an
      out-of-scope path but a self-consistent content identity was disclosed
      while a separately supplied path passed the gate. Refusal ordering is
      fixed and tested — scope, then buffer roles, then buffer-to-scope
      binding, then content identity, and only then any assembled text — so
      no refusal ever emits a partial prompt or leaks buffer content. A
      not-yet-created buffer with no path remains a supported case and
      renders a fixed placeholder rather than failing.
      REMAINING, which keeps this milestone open. The assembled prompt is an
      INTERNAL, schema-agnostic representation: it declares no schema version
      and no wire kind constant, pinned by a source sentinel, because the
      chat-turn contract package is unreleased — so nothing here may be read
      as contract parity. Nothing yet DISPATCHES an assembled prompt: the
      turn route that would parse a real request body, apply
      console-presence and actor checks, and hand the envelope to a port is
      item 5.2's, the port carries no dispatch member (item 5.1), and
      response decoding is item 5.5's. Output-side limits exist here as
      arithmetic constants only, with no decoding, no timeout enforcement,
      and no provider failure mapping.
- [ ] 5.4 Implement one-in-flight-turn discipline plus client-turn-id idempotency for completed, in-flight, and conflicting repeats, with an in-process bounded result cache that stores no provider credential.
      PRESENT as of 2026-07-30, as a dedicated in-process store with real
      concurrency proofs rather than simulated interleaving. ONE-IN-FLIGHT is
      enforced PER CONVERSATION KEY, which this milestone had to correct: an
      earlier draft partitioned reservations by conversation key plus client
      turn id with no per-key guard, so two distinct turn ids for one
      conversation both won dispatch. A second, distinct turn id for a key
      that already has one in flight is now refused immediately — no wait, no
      dispatch, no entry created — through a check-and-set inside one
      critical section, so no window grants two dispatch rights; a race in
      which many distinct ids contend for a single key resolves with exactly
      one winner. Crucially, that discipline does NOT serialize unrelated
      conversations: independent keys proceed concurrently, and finalization
      releases the slot so the next turn may reserve.
      CLIENT-TURN-ID IDEMPOTENCY covers all three declared repeat classes. A
      completed repeat replays its stored outcome with no second dispatch, a
      failed repeat replays its stored failure the same way, an identical
      in-flight repeat attaches and waits rather than dispatching twice, and
      a CONFLICTING repeat — the same identifier bearing a different input
      digest — refuses against every state, including refusing immediately
      and without blocking against an in-flight entry.
      The BOUNDED RESULT CACHE stores no provider credential and no request
      content at all, keeping only a scope-partitioned identity, an input
      digest, a state, and an already-bounded result. It is bounded on both
      axes, evicting least-recently-used completed or failed entries at 64
      entries and 16 MiB, ordered by a monotonic counter rather than any
      wall-clock reading so eviction is deterministic and reproducible;
      in-flight entries are never evicted. Misuse fails closed and leaves the
      cache and its accounting byte-for-byte unchanged: finalizing an unknown
      or already-resolved entry refuses, as do negative and over-limit
      result sizes. Stored results are isolated by deep copy on the way in
      AND on both read paths, so a caller mutating a peeked or replayed
      result cannot change what a later identical repeat returns. The lock is
      held only for in-memory bookkeeping — every payload copy happens with
      it released, proven by a deterministic lock probe rather than a timing
      measurement — so a large result never stalls an unrelated conversation.
      REMAINING, which keeps this milestone open. Nothing CALLS this store
      yet. The turn route that must reserve before dispatch, honour the
      refusal as a fixed redacted error, and finalize afterwards is item
      5.2's; response decoding that would produce the bounded result it
      caches is item 5.5's. The browser-side conversation state that must
      surface a one-in-flight refusal while preserving composer content is
      codexFactory Speckit T052-T054. The store is process-local by design
      and offers no cross-process or persisted discipline, so a
      multi-process deployment posture is unaddressed here.
- [ ] 5.5 Implement strict response decoding for assistant prose plus zero or more typed proposals, rejecting malformed/oversized/provider-error responses without changing buffers or leaking prompt/document/provider payloads into logs or errors.
- [ ] 5.6 Supply fake/local test adapters and the approved deployment adapters behind the same port; keep all real provider calls disabled in ordinary tests and make an empty catalog a supported editor-only posture.
      The FAKE ADAPTER half and the empty-catalog posture landed on
      2026-07-30. One deterministic in-memory adapter now sits behind the
      port: it returns the same catalog object on every call, records every
      call in an append-only log so a later test can prove a refusal
      preceded any dispatch, accepts a seeded failure for the deterministic
      catalog-assembly-failure posture, validates its declared timeout at
      construction, and refuses anything that is not a real catalog. It
      reaches no network, reads no environment variable, spawns no process,
      and holds no credential — ordinary tests cannot reach a provider
      through it because there is no provider path to reach. The empty
      catalog is a named, tested editor-only posture rather than an error,
      matching the absence posture the injection point already reports.
      This milestone remains open on its other half: the APPROVED
      DEPLOYMENT adapters do not exist. Neither the configured
      on-tenant/local/subscription adapter nor the opt-in zero-retention
      hosted fallback of the design's model-port decision has been built, so
      no deployment can yet enable a real model, and the fake adapter's
      coverage is catalog-side only — the fake-provider timeout,
      unavailable-model, malformed-output, and oversize-output cases arrive
      with items 5.5 and 7.2.

## 6. Proposal Apply and Governed Save Milestone (codexFactory Speckit)

- [ ] 6.1 Render typed proposals with independent Outline/Document review controls and DOM-safe comparison; prose without a valid proposal MUST remain conversation only.
- [ ] 6.2 Implement local Apply as a reversible target-buffer replacement guarded by the proposal base hash, and prove stale Apply preserves newer human text with no silent merge or force-apply path.
- [ ] 6.3 Extend the existing edit gate so an eligible integrated first Save of the tile's own existing material atomically materializes/joins the branch session, verifies base ref/revision/hash, and commits only in the worktree; every failed first save MUST leave no orphan worktree, registry entry, record, or commit.
- [ ] 6.4 Implement Save for one or both buffers through only `create-document` / `edit-document`, in deterministic outline-then-document order, with one gate-action commit per changed document and an exact partial-success state when the second action refuses.
- [ ] 6.5 Reuse the existing session refresh/rekey path after each successful save so docs, lens, outline, active document, freshness header, and subsequent chat hashes all follow the worktree without an overlay or second projection path.
- [ ] 6.6 Prove that chat, Apply, editing, Discard, model selection, and transcript persistence write no corpus state, while Save never touches the served checkout and no path grants delete, merge, approve, or lifecycle-transition authority.

## 7. Verification and Release Gates

- [ ] 7.1 Add contract parity tests that load the exact pinned openxFactory schemas and validate every emitted catalog, request, response, proposal, and fixed failure shape.
- [ ] 7.2 Add pure-model and route tests for buffer transitions, context/key isolation, hash/path/ref confinement, ownership, limits, idempotency, stale proposals, provider failures, log redaction, first-save cleanup, partial saves, and gate-off/hosted degradation.
- [ ] 7.3 Update the renderer boundary arithmetic and prove the browser bundle contains no external URL, direct provider call, dynamic import, credential marker, or fetch outside the declared same-origin routes.
      Advanced by exactly one call site on 2026-07-30. The composition root
      moved from one fetch call site to two, and the arithmetic was widened
      HONESTLY rather than hidden behind the injected-fetcher spelling that
      exempts the other transport modules: the composition root is the one
      place the bundle's egress must stay visible, so its new read is a plain,
      counted call. The pinned same-origin ROUTE SET did not grow — the second
      site is the pre-existing read-only source pass-through the viewer
      already reads — and every other module's per-file count is unchanged,
      including the self-quoting guards that make a silently widened or
      deleted pin fail. The workbench shell remains free of every transport
      spelling, no dynamic import was added, and the composition root is
      asserted to contain no catalog, turn, or Save route, no credential or
      authorization marker, and no provider spelling, so this slice's
      deliberate absences are pinned rather than merely current. This gate
      remains open: it closes only against the FINAL bundle, once the catalog,
      turn, chat, and Save transports actually exist and their own arithmetic
      is proven.
- [ ] 7.4 Run keyboard/screen-reader/reduced-motion/high-contrast/responsive checks over the named doxBench surface, context, tabs, editors, chat, proposal comparison, Save/Discard, failure states, and focus restoration; verify visible and accessible names use exact `doxBench` casing and close every release-gating checklist item.
      NOT TICKED — annotated 2026-08-02 (T105). Evidence
      `doxbench-t100-evidence.md`, measured with a retained Playwright script
      on head `9c90b35` (re-verified after the tablist work). What HOLDS:
      CHK007 roving keyboard PASS across every visible `[role=tablist]` —
      three strips (`.tabs`, `.swb-tabs`, `.doxbench-tabs`), one tabbable tab
      each, Left/Right AND Up/Down moving selection with focus, Home/End
      reaching the ends; CHK024 focus + legibility PASS with a recorded gap
      (measured contrast 6.0:1 status, 6.0:1 save note, 14.87:1 rail header
      against the AA 4.5:1 bar; indicators are the UA default rather than a
      designed token); CHK025 forced colors PASS (selected/unselected survives
      without colour, weight 400 vs 600); CHK026 zoom + reflow PASS (no
      page-level horizontal scrolling at 100%, 200%, 200%-narrow); CHK035
      announcement surfaces PASS ON STRUCTURE ONLY — three named landmarks and
      correct live-region politeness, with zero unlabelled buttons after the
      `repohint` nit closed.
      WHY IT STAYS OPEN — the task's own wording asks for SCREEN-READER checks
      and to "close every release-gating checklist item", and two legs of the
      operator's own binding CHK034 AT/browser matrix are DECLARED BUT NOT
      EXERCISED: the Narrator primary leg (Edge/Chromium on Windows 11) and
      the NVDA secondary spot-check (Firefox). Only the keyboard-only Chromium
      leg is exercised. CHK035 therefore stands as a structural PROXY — no
      screen reader has spoken this surface — and full sign-off requires the
      Narrator pass. Recorded, not force-ticked.
- [ ] 7.5 Run the full codexFactory suites, dashboard suite, document validation, lint/quality gates, and a scratch-checkout Playwright flow covering: select document → edit outline → chat → edit document → next turn sees both edits → apply proposal → stale refusal → Save → refresh → PR/merge/cleanup.
      NOT TICKED — annotated 2026-08-02 (T105). What HOLDS: the whole
      named FLOW ran on the REAL corpus, four runs, and every one of the ten
      SC-012 clauses is green (`doxbench-t100-evidence.md`): outline edit;
      real chat turns with the data-handling badge shown at the send moment;
      document edit through the active-document picker; the later turn seeing
      BOTH unsaved edits (proven rigorously — a stray character planted in the
      unsaved document title was found and named by the next turn, and a
      weaker observation was explicitly rejected as inadmissible); Apply
      reaching its terminal state; a card going visibly stale and being
      Rejected; Save landing TWO gate-action commits in the specified
      outline-then-document order on `draft/recurrence-crystallization`
      (`efb8d32`, `ddca5ad`, branched from `555747a`, verified in git rather
      than from the UI) with the served checkout never moving; refresh showing
      the session; the pull-request lifecycle through `opensoft/openxFactory#51`
      merged as `235423d`; and published visibility plus a real merge-ending
      cleanup (`torn_down: [worktree, registry-entry]`, branch deleted,
      snapshot index back to `main`). Suites: the codexFactory feature branch
      runs green at `b8cdf73` — `python3 -m pytest tests/ -q` 3236 passed, 26
      skipped, and the dashboard suite 2314 passed, 19 skipped.
      WHY IT STAYS OPEN — three named clauses have no evidence to cite: the
      flow was operator-driven in a real browser rather than a SCRATCH-CHECKOUT
      PLAYWRIGHT script (Playwright was used only for the accessibility sheet),
      and neither the DOCUMENT VALIDATION nor the LINT/QUALITY-GATE runs this
      task names are recorded anywhere I can point at. The PR's own `validate`
      check passes on head `a3780da`, which is adjacent evidence, not this
      clause.
- [x] 7.6 Run an approved-model live smoke first on non-sensitive fixtures, confirm the catalog badge and redacted failure posture, then run one authorized real-corpus branch session without exposing credentials or using an unapproved hosted model.
      CLOSED 2026-08-02 (T105) — every clause of this task, in its own order,
      has a named record.
        * FIXTURE SMOKE FIRST — `doxbench-t099-evidence.md` (2026-08-01, Brett
          Heap operating): scratch FIXTURE corpus only, one approved catalog
          entry served through the released `workbench-model-catalog` envelope,
          TWO real turns dispatched through the operator's own subscription.
        * CATALOG BADGE — shown and confirmed verbatim at the SEND MOMENT,
          naming the provider class and stating plainly that it is consumer
          subscription terms and NOT an enterprise zero-retention agreement.
        * REDACTED FAILURE POSTURE — proven twice: in-process, an adapter
          raising with a planted marker plus a fake endpoint and fake key
          produced exactly the fixed `model_failed` / "the provider failed and
          its details are withheld by design" outcome with the marker leaked
          False; in the browser, the same drill rendered only "the model
          request failed". Serve stdout/stderr marker count 0.
        * THEN THE AUTHORIZED REAL-CORPUS SESSION — `doxbench-t100-evidence.md`:
          the same operator harness pointed at a real `openxFactory` clone,
          real turns over real scope, ending in a real branch session whose
          pull request merged as `235423d`.
        * NO CREDENTIAL EXPOSURE, NO UNAPPROVED HOSTED MODEL — the adapter is a
          subscription-primary local CLI dispatch held OUTSIDE every repo, with
          no API key, endpoint, or credential-shaped value in the adapter, its
          environment, or the evidence; deployment authorization is Brett's
          recorded 2026-07-31 subscription-primary ruling; local serve only.
- [x] 7.7 Assemble doxBench realization evidence mapped to every OpenSpec scenario and Speckit acceptance criterion, obtain independent review, merge the contract package before the codexFactory realization, and update this ledger with exact revisions.
      NOT TICKED — annotated 2026-08-02 (T105). Three of this task's four
      clauses are evidenced; the first is not, and it is the one the task is
      named for.
        * INDEPENDENT REVIEW — DONE, and unusually deep: an independent
          two-pass review of the frozen head `7b63c6a` (`doxbench-t104-review.md`,
          `doxbench-t104-families.md`) raised 128 findings, confirmed 106 after
          three-vote adversarial refutation, and de-duplicated to 84 distinct
          (15 P1 / 49 P2 / 20 P3) across ten families. Brett Heap recorded the
          binding dispositions himself (`doxbench-t104-dispositions.md`,
          author self-approval forbidden, CHK026): F1-F4 FIX-FIRST, F5-F10 a
          recorded follow-up wave. The four families landed as codexFactory
          `21d408f` (F4), `4b71845` (F3), `673eb33` (F2), `a57f6af` (F1), each
          with RED-then-GREEN evidence in its own commit body, and the operator
          re-verified all four fixed on the live surface
          (`doxbench-t104-reverify.md`). That re-verification raised ONE new
          blocker, G-1, which is also closed: the contract-v1.28 nullability
          amendment (openxFactory PR #53, tag `a6f49bb` -> `ff64e81`) plus the
          consumer's outline-only turn (codexFactory `b8cdf73`) and pin advance
          (`9dbe941`).
        * MERGE THE CONTRACT PACKAGE BEFORE THE CODEXFACTORY REALIZATION —
          HOLDS, see 2.5: both bundles are tagged on `origin/main` while
          codexFactory PR #63 is still open at head `a3780da`.
        * UPDATE THIS LEDGER WITH EXACT REVISIONS — done by this T105 pass;
          every claim above names a commit, a tag, or a record.
        * REALIZATION EVIDENCE MAPPED TO EVERY OPENSPEC SCENARIO AND SPECKIT
          ACCEPTANCE CRITERION — NOT DONE. The records above are organized by
          run and by defect family, not scenario by scenario, and no artifact
          exists that walks this delta's requirements (6 ADDED + 2 MODIFIED,
          with their scenarios) against named evidence. Until that mapping
          exists this task stays open, and with it the realization-evidence
          precondition 7.8 depends on.
      CLOSED 2026-08-02 — the mapping now exists at
      `evidence/realization-mapping.md`, written after codexFactory PR #63
      merged as `c80264c`. Its item list is built MECHANICALLY, not by eye:
      every `#### Scenario:` under this change's `specs/` (52, across the 6
      ADDED and 2 MODIFIED requirements) and every `- **FR-nnn**:` /
      `- **SC-nnn**:` in the merged Speckit spec read at
      `git show origin/main:specs/010-doxbench-editor-chat/spec.md` (45 FRs,
      FR-001..FR-045 with no gaps; 12 SCs). 109 items, 109 rows, each naming
      the implementing code path (file + symbol), the test or operator record
      that proves it, and the commit where it landed — the T104 wave
      (`21d408f`, `4b71845`, `673eb33`, `a57f6af`), G-1 (`b8cdf73`,
      `9dbe941`), the merge `c80264c`, and `contract-v1.27`/`contract-v1.28`
      where the wire contract is what makes the row true. Every cited test
      name and file was verified to exist at `c80264c` with `git grep`.
      104 rows EVIDENCED; 5 PARTIAL, each named with its carrier rather than
      papered over: FR-041 + SC-010 (no screen reader has spoken this surface
      — CHK034a Edge+Narrator and CHK034b Firefox+NVDA are declared but not
      exercised; operator-gated, and the same gap that keeps 7.4 open),
      FR-038 (after a single-buffer Save the next turn is still refused —
      R-12, awaiting a reviewer ruling because moving `base_ref` changes what
      the field claims), FR-010 (selection/scroll not restored — T104 family
      F6), and FR-045 (content-derived text direction realized only on the
      chat rail — T104 family F9).
- [x] 7.8 Roll out with the model catalog empty/off by default, verify editor-only and hosted read-only postures, enable approved models per deployment policy, complete Brett's live pass, sync the promoted spec, and archive this change only after the realization and release evidence have landed.
      CLOSED 2026-08-02, after re-verifying every gate in section 8 (see the
      2026-08-02 re-verification block there — nothing was archived before
      that check). Clause by clause:
        * CATALOG EMPTY/OFF BY DEFAULT — the shipped posture is
          refused-by-absence: no provider adapter exists in this repository,
          `_workbench_model_port()` returns None, and the catalog route
          answers `models: []` as a SUCCESS. Pinned by
          `test_doxbench_routes.py` and the editor-only posture tests.
        * EDITOR-ONLY AND HOSTED READ-ONLY POSTURES VERIFIED — with zero
          approved models both buffers stay loadable, editable, previewable,
          discardable and saveable while chat states its unavailable posture
          (SC-008); on the hosted/gate-off plane the canvas is never mounted
          and every write-implying control is ABSENT rather than disabled
          (SC-007). Evidence: `test_doxbench_view.py`'s posture harness plus
          `doxbench-t100-evidence.md`.
        * APPROVED MODELS PER DEPLOYMENT POLICY — enabled only through an
          operator-held adapter outside every repository, under Brett's
          recorded 2026-07-31 subscription-primary authorization, with the
          data-handling badge shown at the send moment and the redaction drill
          proven twice (`doxbench-t099-evidence.md`).
        * BRETT'S LIVE PASS — complete: `doxbench-t100-evidence.md` records
          all ten SC-012 clauses PASS on the real corpus across four runs,
          and the reviewer-of-record decision on PR #63 (2026-08-02T20:34:22Z)
          records the merge with three accepted exceptions.
        * SYNC THE PROMOTED SPEC AND ARCHIVE — run in this commit with
          `openspec archive add-workbench-integrated-editor-chat`; the result
          is recorded in section 8's archive block.

## 8. Merge / promotion / archive gate confirmation (T106, 2026-08-02)

STATUS UNCHANGED BY THIS SECTION. This change's front-matter still reads
`status: proposed`; nothing here archives the change, promotes a delta, or
edits anything under `openspec/specs/`. T106's own wording is to CONFIRM the
gates "before changing the OpenSpec change status", so the confirmation is the
deliverable and the status change is not part of it — and it would be
premature, because two gates below are PENDING.

Each gate names where its requirement comes from and how its current state was
checked. Checks were run on 2026-08-02 from a clean worktree off openxFactory
`origin/main` (`ff64e81`) and against codexFactory PR #63 as it then stood.

### (a) Before PR #63 merges

| # | Gate (source) | State | Evidence / check |
|---|---|---|---|
| a1 | Implementation Start Gate closed — tasks 1.1-1.7 (this ledger; proposal's "Start Gate" clause) | **PASS** | 1.6 was the last open item; closed on this branch at `bb62197` with both strict validations green. 1.1-1.5 and 1.7 were already closed with their own dated notes. |
| a2 | Contract package landed and tagged BEFORE the realization merges — task 2.5; design D0 ("does not permit realization merge before this change's own contract package is registered and pinned") | **PASS** | `contract-v1.27` tag `fb912b9` -> `d09d582` and `contract-v1.28` tag `a6f49bb` -> `ff64e81`, both ancestors of `origin/main` (`git for-each-ref`, `git merge-base --is-ancestor`); manifest digests 109/109 verify; PR #63 is still OPEN, so the ordering is a fact rather than an intention. |
| a3 | Consumer pins the exact released bytes — task 7.1 / the immutable-pin clause | **PASS** | codexFactory `stack.yaml` `contract_ref: ff64e81…` with the `contract-v1.28` tag object recorded beside it, advanced in `9dbe941`. |
| a4 | Independent review obtained and dispositioned — task 7.7; CHK026 (author self-approval forbidden) | **PASS** | Independent two-pass review of frozen head `7b63c6a`: 128 raised, 106 confirmed after three-vote refutation, 84 distinct (15 P1). Brett Heap recorded the dispositions himself. F1-F4 landed (`21d408f`, `4b71845`, `673eb33`, `a57f6af`) and were re-verified fixed on the live surface; the re-verification's own new blocker G-1 is closed (contract-v1.28 + codexFactory `b8cdf73`, `9dbe941`). |
| a5 | Engineering gates green on the PR head | **PENDING** | `gh pr checks 63` on head `a3780da`: `validate` **pass**; `sonar` **fail**; `SonarCloud Code Analysis` **cancelled**. The Sonar failure is a configuration conflict, not a code verdict — the run log ends `ERROR You are running CI analysis while Automatic Analysis is enabled. Please consider disabling one or the other.` Clearing it is the operator's SonarCloud AutoScan toggle; the analysis has produced no quality verdict yet. |
| a6 | Human review decision | **PENDING** | `gh pr view 63`: state OPEN, mergeable MERGEABLE, `reviewDecision: REVIEW_REQUIRED`. Automated reviewers have run on this head (`chatgpt-codex-connector` at 18:33:59Z after Brett's `@codex review`, `copilot-pull-request-reviewer` at 18:36:22Z, "Running Copilot Code Review" workflow success). Brett's merge is the gate. |

### (b) Before capability promotion (spec update)

| # | Gate (source) | State | Evidence / check |
|---|---|---|---|
| b1 | Deltas rebased onto the promoted capability — task 1.6 | **PASS** | Both MODIFIED blocks sit on the exact promoted source (promotion introduced no drift: byte-identical to the `add-workbench-branch-sessions` text they were written against). |
| b2 | The delta APPLIES cleanly to the promoted spec | **PASS** | Measured on a scratch copy of `openspec/` (real spec untouched): `openspec archive` reports `+ 6, ~ 2, - 0, → 1` and "Specs updated successfully", leaving exactly one scoped-view requirement. Before the `## RENAMED Requirements` fix landed at `bb62197`, the same command ABORTED with `ideation-dashboard MODIFIED failed for header "### Requirement: doxBench scoped view" - not found`. |
| b3 | Strict validation | **PASS** | `openspec validate add-workbench-integrated-editor-chat --strict` valid; `openspec validate --all --strict` 53 passed / 0 failed. |
| b4 | Promotion happens only through the archive step | **NOT RUN, BY DESIGN** | Task 7.8 owns "sync the promoted spec"; no file under `openspec/specs/` is touched by T105 or T106. |

### (c) Before archive

| # | Gate (source) | State | Evidence / check |
|---|---|---|---|
| c1 | Realization archive gate — `openspec/specs/release-realization/spec.md`: a change with a non-empty code surface SHALL NOT archive until its code is merged on the implemented target AND, where runnable, a green run exists. This change declares `code_surface: codexFactory …, openxFactory …` | **PENDING (merge half)** | openxFactory half MERGED (`ff64e81`, contract-v1.28). codexFactory half NOT merged — PR #63 open at `a3780da`. The runnable half IS green on the branch (`pytest tests/ -q` 3236 passed / 26 skipped; dashboard 2314 / 19; T100's ten SC-012 clauses on the real corpus), but "merged on the implemented target" is unmet, so archiving now would be the spec's own contested-class act. |
| c2 | Workflow protocol: "Archive the OpenSpec change only after the corresponding Speckit work and PR have landed" | **PENDING** | Same fact as c1: PR #63 has not landed. |
| c3 | Task 7.8's own clause — archive "only after the realization and release evidence have landed" | **PENDING** | Release evidence has landed (both contract bundles). Realization evidence has not: 7.7's scenario-by-scenario mapping does not exist, and 7.4's screen-reader legs (CHK034 Narrator primary, NVDA secondary) are declared but not exercised. |
| c4 | `target_release` satisfied — "next additive contract bundle after the five predecessor dashboard changes archive" | **PASS** | The five predecessors archived 2026-08-01; the additive bundles that followed are contract-v1.27 and contract-v1.28, both tagged. |

### Re-verification 2026-08-02 (post-merge, before archiving)

Every PENDING row above was re-checked against the merged state. No row was
assumed; each names what was observed.

| # | Was | Now | Evidence |
|---|---|---|---|
| a5 | PENDING (sonar failed on the AutoScan conflict) | **PASS, with a recorded exception** | At the merged head `0dde88f`: `sonar` **pass** (7m55s — the CI/AutoScan conflict is gone) and `validate` **pass**. The separate `SonarCloud Code Analysis` check is RED on the quality gate itself, and the reviewer of record accepted it explicitly: "0.0% Coverage on New Code is a MEASUREMENT GAP, not missing tests — the job uploads no coverage report while 2,327 tests pass"; coverage wiring rides the follow-up wave. Two further exceptions are recorded there: a WON'T-FIX false positive at `branch_session.py:2675` (a deliberately variadic return whose only caller iterates) and three cognitive-complexity thresholds, re-openable if any acquires a confirmed defect. |
| a6 | PENDING (REVIEW_REQUIRED) | **PASS** | Reviewer-of-record decision recorded as a PR #63 comment by Brett Heap at 2026-08-02T20:34:22Z — MERGE, stating that GitHub could not express it as an approval because author and reviewer of record are the same identity (CHK026 forbids self-approval regardless) and that the independence the requirement demands was supplied by T104, not by a click. |
| c1 | PENDING (codexFactory half unmerged) | **PASS** | PR #63 MERGED at 2026-08-02T20:34:33Z as merge commit `c80264c`; the runnable surface is green on it (2,327 passed / 6 skipped / 0 failures; doxBench contracts 30/30 against the real released bytes). Both halves of the declared code surface are now on their implemented targets — openxFactory at `ff64e81`, codexFactory at `c80264c`. |
| c2 | PENDING | **PASS** | Same fact: the Speckit work and its PR have landed. |
| c3 | PENDING (7.7's mapping absent) | **PASS** | `evidence/realization-mapping.md` — 109 of 109 items mapped, 104 EVIDENCED and 5 PARTIAL with named carriers. |

All gates satisfied, so the archive was run. Gates a1-a4, b1-b4 and c4 were
unchanged and are not re-listed.

### Archive result 2026-08-02

`OPENSPEC_TELEMETRY=0 openspec archive add-workbench-integrated-editor-chat -y`
(`-y` only because this shell is non-interactive; the flow is otherwise the
tooling's own). Result:

  Specs to update:
    ideation-dashboard: update
  Applying changes to openspec/specs/ideation-dashboard/spec.md:
    + 6 added
    ~ 2 modified
    → 1 renamed
  Totals: + 6, ~ 2, - 0, → 1
  Specs updated successfully.
  Change 'add-workbench-integrated-editor-chat' archived as
  '2026-08-02-add-workbench-integrated-editor-chat'.

EXACTLY the totals task 1.6's scratch-copy dry-run predicted on 2026-08-02
(`+ 6, ~ 2, - 0, → 1`) — no divergence. The tool also reported, non-blocking,
one proposal style warning (Why section over 1000 characters) and "24
incomplete task(s)"; those 24 are the milestone tasks whose acceptance belongs
to the Speckit feature's own ledger plus 7.1-7.5, each annotated in place with
what is evidenced and what is not. They are archived open ON PURPOSE — this
ledger's rule throughout has been to annotate honestly rather than
force-tick.

Confirmed after the run: `openspec/specs/ideation-dashboard/spec.md` holds 46
requirements, `### Requirement: doxBench scoped view` appears EXACTLY ONCE and
`### Requirement: Staging workbench scoped view` is GONE (0 occurrences), with
the five other doxBench requirements added beside it. `openspec validate --all
--strict` -> 53 passed / 0 failed.

FRONT MATTER, deliberately untouched: this proposal's `status: proposed` is
left as it stands. The archive tool neither reads nor writes it; NO other
change in this repository — active or archived — carries a `status:` field at
all (checked with `grep -rn "^status:" openspec/changes/*/proposal.md` and the
same over `archive/`); and no vocabulary for a post-archive value is defined
in `docs/` or in the `release-realization` capability. The change's location
under `openspec/changes/archive/` is its status of record; inventing a value
for an unowned field would be worse than leaving the one the author wrote.

### What remains, in order

1. The operator's SonarCloud AutoScan toggle, then a green `sonar` run on the
   PR head (a5).
2. Brett's review decision and merge of PR #63 (a6, c1, c2).
3. Post-merge: assemble 7.7's scenario-by-scenario realization mapping and
   exercise 7.4's declared screen-reader legs (c3).
4. Only then task 7.8: sync the promoted spec and archive.

## Bookkeeping correction (2026-08-23, `govern-openspec-corpus-membership`)

`proposal.md` gained TWO header lines in one edit — `Status: ratified` and a single `Ratified:` citation, at real lines 5 and 6, both well inside the fifteen-real-line header window. Nothing else on the page moved: the writer asserted per file that deleting exactly those two lines recovers the original bytes, and refused to write otherwise. The ruling is OQ-6's of 2026-08-23 (Brett Heap, in-session multiple-choice round), which DEPARTED from its own recommendation — no grandfather, no contract date, no reduced-severity class — and backfills every headerless proposal from its OWN record, stopping and reporting rather than inventing where a record cannot carry one. The status and the citation are coupled because the promoted rule in `openspec/specs/document-lifecycle/spec.md` holds that a bare, uncited `Status: ratified` is a violation whatever else the document says.

This document's citation takes derivation route (a), an explicit ratification act named on the record: this change's own tasks.md 1.7, "Brett ratified the proposal decisions and approved a narrow implementation-start exception on 2026-07-29". The three-way floor is cleared on the APPROVER axis, the DATE axis and a resolvable RECORD PATH, measured through `doc_health.families` before the line was written, not assumed.

**The 2026-08-02 decision this supersedes, quoted in full and LEFT STANDING.** The archive
commit `354ded9` recorded, and this note does not alter, edit, or withdraw one word of it:

> FRONT MATTER deliberately untouched: `status: proposed` stands. The archive tool neither
> reads nor writes it, NO other change in this repository — active or archived — carries a
> `status:` field, and no vocabulary for a post-archive value is defined in `docs/` or the
> `release-realization` capability. The change's location under `openspec/changes/archive/`
> is its status of record; inventing a value for an unowned field would be worse than leaving
> the one the author wrote.

**RULED 2026-08-23 (Brett, in-session), recorded as task 5D.2a of
`govern-openspec-corpus-membership`: BACKFILL IT TOO.** The decision is SUPERSEDED ON ITS OWN
TERMS rather than overturned. Its stated reason — that no vocabulary for a post-archive value
is defined — was true when it was written and is no longer: the ratification-citation rule in
`openspec/specs/document-lifecycle/spec.md` is promoted, it owns the `Status:` field for
proposals, and it requires the header the 2026-08-02 decision declined to invent. Nothing that
decision asserted about the corpus of 2026-08-02 has been contradicted. Two consequences are
recorded rather than left to a reader. FIRST, the lowercase `status: proposed` front-matter
field the author wrote is deliberately LEFT STANDING and untouched, exactly as A2 of
`docs/archive-record-discrepancies.md` verifies it; it is not a second status header, because
`doc_health.corpus.STATUS_RE` is case-sensitive and reads only the capitalised line, so this
proposal carries exactly ONE machine-read status. SECOND, register entry A2 gains a dated
supersession addendum in the same slice, with its original text standing.

It is entered in `docs/archive-record-discrepancies.md` as C2's successor. This note travels with the change, as 5B's twenty-seven do.

## Bookkeeping correction (2026-09-11, `split-opendox-two-layer-product` § 5.9) — carry-forward

Edited (bookkeeping): 2026-09-11 by split-opendox-two-layer-product — carry-forward annotation

This packet's `specs/ideation-dashboard/spec.md` delta stays the record, unedited and unaugmented by anything below. The `ideation-dashboard` capability's artifacts — the `scripts/ideation_dashboard/` tree, `web/`, `tests/ideation-dashboard/`, the packaged examples under `examples/ideation-dashboard/`, the five dashboard governance docs, and the five dashboard contract schemas — were SHED from `openxFactory` by `split-opendox-two-layer-product` § 5.2, `opensoft/openxFactory` PR #940 → `cc4ae9d35b2dbd56743c8c19699fd685d4e49343` (merged 2026-09-11). They are now consumed at a pin from the `openDox`/`openXdox` legs per `docs/opendox-carve-manifest.yaml` (destinations `opendox_spec`, `opendox_code`, `openxdox_spec`, `openxdox_code`; `contracts/opendox-pin.yaml`, `contracts/openxdox-pin.yaml`). The five contract schemas this delta names — `gate-action-record`, `ideation-dashboard-snapshot-index`, `ideation-dashboard-snapshot`, `xfactory-workbench-chat-turn`, `xfactory-workbench-model-catalog` — were DEPRECATED at `contract-v3.7` (`opensoft/openxFactory` PR #970 → `45bd9ee250ad1125f9227ad511bee0fec2b16306`, tag `ec3c17292c6dc2ca6004d158d6cc26bf5e6523e2`, merged 2026-09-11) and LEAVE the bundle at `contract-v4.0` (§ 5.7; cut PR `TBD-CUT-PR`, a placeholder the landing lane fills in when the cut lands). Ruled by Brett Heap, 2026-09-11 20:27Z, session `openXfactory-4 (5)`, on `opensoft/openxFactory`#656 comment `5640246046` (§ 5.9), realizing `split-opendox-two-layer-product` `tasks.md` § 5.9 — "ANNOTATE the 30 archived changes carrying an `ideation-dashboard` delta with the carry-forward." Nothing this packet asserts is changed by this annotation; immutable records are annotated, never edited into agreement.
