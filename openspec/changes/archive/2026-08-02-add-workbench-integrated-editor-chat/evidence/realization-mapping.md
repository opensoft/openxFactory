# doxBench realization evidence, mapped item by item (task 7.7)

Task 7.7's other three clauses were already evidenced in the ledger (the
independent review, the contract-package-before-realization ordering, and the
ledger revisions themselves). This file closes the clause the task is named
for: **realization evidence mapped to EVERY OpenSpec scenario and Speckit
acceptance criterion**.

## How the item list was built (mechanically, not by eye)

- **Scenarios** — every `#### Scenario:` under
  `openspec/changes/add-workbench-integrated-editor-chat/specs/`, walked with a
  script that tracks the enclosing `## …Requirements` section and
  `### Requirement:` header. Result: **52 scenarios** across 8 requirements
  (6 ADDED, 2 MODIFIED).
- **Speckit criteria** — every `- **FR-nnn**:` and `- **SC-nnn**:` in
  codexFactory `specs/010-doxbench-editor-chat/spec.md`, read from the MERGED
  revision (`git show origin/main:…` at `c80264c`), matched with
  `^- \*\*(FR|SC)-\d+\*\*:`. Result: **45 FRs** (FR-001…FR-045, no gaps, no
  duplicates) and **12 SCs** (SC-001…SC-012).

**Total 109 items; every one has a row below.** Rows are `EVIDENCED`,
`PARTIAL` (evidence exists and a named clause is not met), or `NOT EVIDENCED`
(with the reason). No row is left blank, and nothing is claimed that a named
file, test, commit, or operator record does not support.

## Revisions cited

| Short | What |
|---|---|
| `c80264c` | codexFactory PR #63 merge — the whole feature on `main` |
| `21d408f` `4b71845` `673eb33` `a57f6af` | the T104 fix-first wave: F4 turn-engine concurrency, F3 first-edit integrity, F2 active-document eligibility, F1 post-Save re-key |
| `b8cdf73` / `9dbe941` | G-1: the outline-only turn / the consumer pin advance to contract-v1.28 |
| `d09d582` (`contract-v1.27`), `ff64e81` (`contract-v1.28`) | the released openxFactory wire contracts this feature pins |
| `doxbench-t099-evidence.md` | operator record: approved-model fixture smoke, badge, redaction drill |
| `doxbench-t100-evidence.md` | operator record: the ten SC-012 clauses on the real corpus, plus the measured accessibility sheet and the CHK034 declaration |
| `doxbench-t104-review.md` / `-families.md` / `-dispositions.md` / `-reverify.md` | the independent two-pass review, its families, Brett's dispositions, the re-verification |

Unqualified rows landed across the feature branch and reached `main` in
`c80264c`; a row names a specific commit when that commit is what made the
item true.

---

## Part A — the change's own scenarios (52)

### Requirement: doxBench surface identity (2)

| # | Scenario | State | Code | Test |
|---|---|---|---|---|
| A1 | The integrated authoring surface is presented | EVIDENCED | `web/views/staging-workbench.js` `drawCanvas` builds `canvasLabel = "doxBench" + …` into the region's `aria-label` and visible `h2`; `web/views/doxbench-editor.js` `mountDoxBenchCanvas` heading | `test_doxbench_accessibility.py` (exact casing in visible + accessible names), `test_doxbench_view.py::test_the_shell_really_composes_a_canvas_and_a_rail` |
| A2 | Existing workbench artifacts are loaded | EVIDENCED | no identifier renamed: `workbench-chat-turn` kinds in `doxbench_contracts.py`, `WorkbenchModelPort` in `doxbench_model.py`, unchanged routes/records | `test_doxbench_contracts.py` (kind literals), `test_staging_workbench.py` (pinned mount signature + route constants), `test_session_records.py` |

### Requirement: doxBench editor buffer contract (7)

| # | Scenario | State | Code | Test |
|---|---|---|---|---|
| A3 | A human edits the outline before chatting | EVIDENCED | `doxbench-state.js` `beginBufferEdit`/`settleBufferHash`; `doxbench-editor.js` `edit()` | `test_doxbench_state.py`, `test_doxbench_view.py` (live-DOM edit path) |
| A4 | A human selects a document | EVIDENCED | `doxbench-editor.js` `selectDocument`/`switchDocument` + the labelled picker | `test_doxbench_view.py::test_the_document_picker_reaches_select_document_and_reverts_when_blocked` |
| A5 | A scope has no outline | EVIDENCED | `doxbench-editor.js` `emptyStatement`/`bufferStatusText` (explicit empty state, never fabricated); `staging-workbench-model.js` `doxbenchScopeProjection` publishes `outline_path: null` | `test_doxbench_view.py` (posture harness `capable`/`outlineOnly`), `test_doxbench_scope.py::test_empty_and_missing_scopes_are_honest` |
| A6 | One dirty buffer is saved | EVIDENCED | `doxbench-save.js` `planRow`/`runSave`; `gate_routes.execute_first_edit` | `test_doxbench_save.py`, `test_session_document_ownership.py::test_the_first_edit_verb_lands_a_first_save_over_the_gate_dispatch` |
| A7 | Both dirty buffers are saved | EVIDENCED | `doxbench-save.js` `saveOrder` (outline-then-document), one gate action per document | `test_doxbench_save.py` (order + one-action-per-document), T100 clause 7 (two commits `efb8d32`, `ddca5ad` in that order) |
| A8 | The second save action fails | EVIDENCED | `doxbench-save.js` partial-success rows; `doxbench-editor.js` `save()` per-buffer verdicts | `test_doxbench_save.py` (partial-success reporting), `test_doxbench_view.py` (per-buffer status region) |
| A9 | A human discards local edits | EVIDENCED | `doxbench-state.js` `discardBuffer`; `doxbench-editor.js` `discard()` | `test_doxbench_state.py`, `test_doxbench_view.py` |

### Requirement: Grounded doxBench chat turn (8)

| # | Scenario | State | Code | Test |
|---|---|---|---|---|
| A10 | A human edit feeds the next turn | EVIDENCED | `doxbench-chat.js` `createTurnDispatcher.submit` reads `editorState()` at submit time, never a cache | `test_doxbench_chat_view.py` (fresh buffers at submit), T100 clause 4 (the planted stray character found by the next turn) |
| A11 | Unsaved edits are discussed | EVIDENCED | `doxbench_turns.build_prompt_envelope` `_buffer_section` labels dirty text as working state | `test_doxbench_turns.py::test_dirty_buffer_carries_the_explicit_dirty_working_state_label` |
| A12 | The route receives a mismatched path or hash | EVIDENCED | `doxbench_turns.revalidate_scope` + `verify_buffer_identity`; `serve.py` steps 5-6 | `test_doxbench_turns.py` (identity + scope refusals), `test_doxbench_routes.py` (`content_identity_mismatch`, `turn_scope_refused`) |
| A13 | A turn exceeds a declared limit | EVIDENCED | `doxbench_turns.validate_request_body_bytes` + the per-model ceiling in `serve.py` | `test_doxbench_turns.py` (bound arithmetic), `test_doxbench_routes.py` (`request_limit_exceeded` with the measured dimension) |
| A14 | A turn completes | EVIDENCED | `serve.py` `_handle_workbench_chat_turn` success envelope with observed hashes | `test_doxbench_routes.py::test_a_valid_turn_with_a_dispatch_capable_port_returns_the_released_success` |
| A15 | A completed turn is retried | EVIDENCED | `doxbench_turns.TurnStore` replay + the route's lease binding (**`21d408f`**) | `test_doxbench_routes.py::test_the_completed_success_is_stored_and_replayed_with_exactly_one_dispatch` and `…test_two_concurrent_turns_on_one_turn_id_dispatch_once_and_replay_verbatim` |
| A16 | A turn id is reused for different content | EVIDENCED | `TurnStore.reserve` digest conflict → `turn_id_conflict` | `test_doxbench_routes.py::test_a_conflicting_digest_against_a_resolved_entry_refuses_turn_id_conflict` |
| A17 | A provider or response validation fails | EVIDENCED | `doxbench_model.dispatch_turn` fixed codes; `doxbench_turns.validate_assistant_response`; `serve.py` failure envelope | `test_doxbench_model.py`, `test_doxbench_routes.py` (`model_failed`, `response_invalid`, `model_timeout`), T099 redaction drill (marker leaked False) |

### Requirement: doxBench model catalog and provider boundary (5)

| # | Scenario | State | Code | Test |
|---|---|---|---|---|
| A18 | The browser loads model choices | EVIDENCED | `doxbench_model.catalog_wire_envelope` public seven-field allowlist; `serve.py` `_handle_workbench_model_catalog` | `test_doxbench_model.py`, `test_doxbench_routes.py` (catalog route) |
| A19 | No model is configured | EVIDENCED | `EMPTY_CATALOG` posture; `staging-workbench-model.js` `presentationPosture` | `test_doxbench_routes.py` (empty catalog is a SUCCESS), `test_doxbench_view.py` (posture note) |
| A20 | An unknown model id is submitted | EVIDENCED | `catalog.selectable_entry_for` → `model_unavailable` | `test_doxbench_routes.py` (unknown-model refusal), delegated validator's `unknown-model` rule |
| A21 | A browser attempts a direct provider call | EVIDENCED | bundle boundary: no fetch outside the declared same-origin sites | `test_renderer.py` (fetch-site arithmetic), `test_staging_workbench.py` (no `fetch(`/`XMLHttpRequest`/`import(` in the view), `test_doxbench_transport.py` |
| A22 | Hosted doxBench is opened | EVIDENCED | `sessionSurfaceHidden`/`createGateLive` gate `canvasOffered` in `staging-workbench.js` | `test_doxbench_view.py::test_gate_off_and_hidden_surfaces_withhold_the_canvas_at_the_shell`, posture harness |

### Requirement: Typed AI proposals and stale-application protection (5)

| # | Scenario | State | Code | Test |
|---|---|---|---|---|
| A23 | An AI proposes a document revision | EVIDENCED | `doxbench_turns.validate_assistant_response` typed proposals; `doxbench-chat.js` `proposalCardModel` | `test_doxbench_proposals.py`, `test_doxbench_routes.py::test_a_validated_proposal_flows_into_the_released_success_envelope` |
| A24 | A proposal targets both buffers | EVIDENCED | independent per-target records in `doxbench-chat-model.js` `settleTurnSuccess` | `test_doxbench_proposals.py` (independent targets), `test_doxbench_chat_view.py` (cards) |
| A25 | Human work makes a proposal stale | EVIDENCED | `refreshProposalCurrency` + `doxbench-editor.js` `applyProposal` identity gate | `test_doxbench_proposals.py` (stale transitions), T100 clause 6 (a card went visibly stale, Apply disabled, Reject terminal) |
| A26 | A provider returns prose that looks like a document | EVIDENCED | prose is never inferred as content — only a typed proposal exposes Apply | `test_doxbench_proposals.py`, `test_doxbench_routes.py::test_a_duplicate_target_proposal_payload_is_refused_at_the_route` |
| A27 | An applied proposal is saved | EVIDENCED | Apply marks the buffer dirty and Save runs the ordinary gate path | T100 clauses 5+7 (apply then two governed commits), `test_doxbench_save.py` |

### Requirement: Browser-local doxBench conversation (4)

| # | Scenario | State | Code | Test |
|---|---|---|---|---|
| A28 | A page refresh restores the same conversation | EVIDENCED | `doxbench-state.js` `persistDoxBenchState`/`restoreDoxBenchState` + the R-1 companion blob, applied unconditionally after `a57f6af` | `test_doxbench_view.py::test_the_restored_chat_state_is_applied_on_a_plane_with_no_approved_models`, `test_doxbench_state.py` |
| A29 | doxBench changes scope | EVIDENCED | `doxbench-chat-model.js` `rekeyChatState` (fresh conversation per scope key) | `test_doxbench_chat_view.py::test_rekey_isolates_browser_session_state_per_scope_fr011` |
| A30 | A session ends | EVIDENCED | `staging-workbench.js` `onSessionEnded` clears the session-keyed record, canvas torn down BEFORE the clear (**`a57f6af`**) | `test_doxbench_view.py` (destroy-before-clear order pin), `test_doxbench_state.py` (`clearDoxBenchSession`) |
| A31 | Working subject resembles an identity | EVIDENCED | type-only field, no identity-bearing sibling; delegated validator's `working_subject` rule | `test_doxbench_privacy.py`, openxFactory negative `workbench-chat-turn-identity-subject.negative.yaml` |

### Requirement: Session-scoped document editing verb (9, MODIFIED)

| # | Scenario | State | Code | Test |
|---|---|---|---|---|
| A32 | A document is edited inside a session | EVIDENCED | `branch_session.commit_gate_action` / `_commit_gate_action_locked` | `test_session_commits.py`, `test_session_transaction.py` |
| A33 | An existing document is the first save | EVIDENCED | `branch_session.commit_first_edit` (open-or-join, revalidate, commit in the worktree) | `test_session_transaction.py::test_a_first_save_with_no_live_session_OPENS_one_and_commits_inside_it` and `…JOINS_it_and_allocates_no_second_branch` |
| A34 | First-save validation fails | EVIDENCED | `_unwind_first_edit`, completed for created documents in **`4b71845`** | `test_session_transaction.py::test_a_failed_create_into_a_JOINED_session_leaves_no_residue_on_any_axis` (+ the retry and tracked-file tripwires) |
| A35 | Editing is attempted without a session by another path | EVIDENCED | `gate_routes._edit_document` session requirement | `test_session_verbs.py` |
| A36 | An edit targets a path outside the worktree | EVIDENCED | `boundary.py` confinement + `_relpath_within` | `test_session_confinement.py`, `test_boundary.py` |
| A37 | An edit targets context owned by another scope | EVIDENCED | `gate_routes.foreign_document_refusal` + `branch_session.first_edit_eligibility` | `test_session_document_ownership.py::test_the_first_edit_verb_refuses_a_foreign_document_cleanly` |
| A38 | A session edit is asked to delete | EVIDENCED | no delete path exists; blank-content Save refused as a delete in disguise | `test_doxbench_mutation_boundary.py`, `test_session_verbs.py` |
| A39 | Creating inside a session | EVIDENCED | `create-document` writes into the session worktree | `test_create_document_cli.py`, `test_session_document_ownership.py` |
| A40 | A non-console path invokes the edit verb | EVIDENCED | `gate_console` presence + loopback checks in `serve.py`/`gate_routes.py` | `test_gate_console.py`, `test_doxbench_routes.py` (console-required refusals) |

### Requirement: doxBench scoped view (12, MODIFIED)

| # | Scenario | State | Code | Test |
|---|---|---|---|---|
| A41 | doxBench opens on a cluster | EVIDENCED | `staging-workbench-model.js` `workbenchScope` cluster arm; `doxbench_scope.resolve_scope` | `test_doxbench_scope.py` (`cluster` fixture case, server/browser parity) |
| A42 | doxBench opens on a possible | EVIDENCED | possible arm with the separately labelled inherited section | `test_doxbench_scope.py::test_possible_keeps_cited_and_inherited_disjoint_and_read_only` |
| A43 | doxBench opens on a staged topic | EVIDENCED | staged arm incl. the cluster-neighbourhood section; outline from the primary fragment | `test_doxbench_scope.py::test_staged_scope_owns_only_resolved_folder_material_and_created_paths` |
| A44 | A document becomes active | EVIDENCED | picker → `selectDocument`; candidates are the guard-accepted intersection after **`673eb33`** | `test_doxbench_view.py` (picker), `test_doxbench_turns.py::test_every_published_candidate_passes_the_real_turn_guard_on_every_fixture` |
| A45 | Cluster-neighbourhood documents stay out of health | EVIDENCED | health/readiness stay folder-scoped in `generator.py`/`workbench.py` | `test_completeness.py`, `test_readiness_gate.py`, `test_staging_workbench.py` |
| A46 | A docs row shows how far a document has come | EVIDENCED | signals rendered verbatim from the snapshot, never recomputed | `test_staging_workbench.py` (verbatim signals), `test_completeness.py` |
| A47 | The source pass-through is absent | EVIDENCED | `doxbench-editor.js` `loadDescriptor` → `load_state: "unavailable"`, stated inline | `test_doxbench_view.py::test_an_unavailable_source_is_reported_inline_with_context_retained` |
| A48 | A scope carries no outline | EVIDENCED | explicit empty/create state; outline-only posture stated after **`b8cdf73`** | `test_doxbench_view.py` (posture harness), `test_doxbench_scope.py` |
| A49 | A human edits before a session exists | EVIDENCED | browser-local editing writes nothing; the next turn sees it | `test_doxbench_mutation_boundary.py` (zero corpus writes), T100 clause 4 |
| A50 | An existing document is saved | EVIDENCED | `execute_first_edit` single commit on the session branch | T100 clause 7 (verified in git), `test_session_document_ownership.py` |
| A51 | doxBench renders without gate or model capability | EVIDENCED | `presentationPosture` + `canvasOffered` | `test_doxbench_view.py` (gate-off/hosted), `test_doxbench_routes.py` (catalog-absent posture) |
| A52 | doxBench is used on a narrow viewport | EVIDENCED | `styles.css` narrow-viewport stacking of the three regions | `doxbench-t100-evidence.md` CHK026 (no page-level horizontal scrolling at 100% / 200% / 200%-narrow, all three regions present), `test_doxbench_accessibility.py` |

---

## Part B — Speckit functional requirements (45)

| FR | State | Realization evidence |
|---|---|---|
| FR-001 | EVIDENCED | exact `doxBench` casing in heading + `aria-label` (`staging-workbench.js` `drawCanvas`, `doxbench-editor.js`); `test_doxbench_accessibility.py` |
| FR-002 | EVIDENCED | no protocol renamed, no migration: `workbench-*` kinds and routes unchanged; `test_doxbench_contracts.py`, `test_staging_workbench.py` |
| FR-003 | EVIDENCED | three regions composed in `staging-workbench.js` (`context`/`canvas`/`rail`); live-DOM `test_doxbench_view.py::test_the_shell_really_composes_a_canvas_and_a_rail` |
| FR-004 | EVIDENCED | `DOXBENCH_BUFFER_TABS`; `test_doxbench_view.py::test_doxbench_buffer_tabs_are_exactly_outline_and_document` |
| FR-005 | EVIDENCED | `doxbench-state.js` `frozenBuffer` field set; `test_doxbench_state.py` |
| FR-006 | EVIDENCED | outline seeded from `projection.outline_path` only, never inferred; `test_doxbench_scope.py`, `test_doxbench_view.py` |
| FR-007 | EVIDENCED | `selectDocument` + the dirty-document guard; `test_doxbench_view.py` (guard blocked/resolved) |
| FR-008 | EVIDENCED | `test_doxbench_mutation_boundary.py` (editing/preview/chat/Apply/Discard write zero corpus state) |
| FR-009 | EVIDENCED | `discardBuffer` restores base without persistence or a model call; `test_doxbench_state.py` |
| FR-010 | **EVIDENCED** | buffer content, dirty state, active tab and focus are preserved and tested (`test_doxbench_view.py` tab/focus restoration; `applyTabVisibility`); the selection/scroll residual closed in the F5–F10 wave (2026-08-05): `applyTabVisibility` captures each pane's view as it goes hidden and writes it back on return — `viewState` gained its production caller — and the test shim now drops `scrollTop` on hide the way a real layout-box loss does, so the tab round-trip pin fails without the write-back (reverse-RED shown) |
| FR-011 | EVIDENCED | `rekeyChatState` per `(repository, ref, tile_kind, tile_id)`; `test_doxbench_chat_view.py` |
| FR-012 | EVIDENCED | free-form string only; `test_doxbench_privacy.py` + the released schema's type-only rule |
| FR-013 | EVIDENCED | `build_prompt_envelope` nine-section assembly with both complete buffers; `test_doxbench_turns.py` (FR-013 field set) |
| FR-014 | EVIDENCED | explicit clean/dirty working-state labels; `test_doxbench_turns.py` |
| FR-015 | EVIDENCED | `revalidate_scope` dual membership, independently re-derived server-side; strengthened by **`673eb33`** (candidates now match the guard) — `test_doxbench_turns.py::test_every_published_candidate_passes_the_real_turn_guard_on_every_fixture` |
| FR-016 | EVIDENCED | buffers read at submit time; `test_doxbench_chat_view.py`, T100 clause 4 |
| FR-017 | EVIDENCED | `doxbench_turns` bounds + measured `limit` block; `test_doxbench_turns.py`, `test_doxbench_routes.py` |
| FR-018 | EVIDENCED | `TurnStore._in_flight_by_key`; `test_doxbench_routes.py` (`turn_in_flight`), `test_doxbench_chat_view.py` (client one-in-flight) |
| FR-019 | EVIDENCED | idempotent replay, and after **`21d408f`** a lost peek/reserve race replays instead of double-dispatching — `test_doxbench_routes.py::test_two_concurrent_turns_on_one_turn_id_dispatch_once_and_replay_verbatim` |
| FR-020 | EVIDENCED | fixed redacted failures in `doxbench_model.dispatch_turn`; `test_doxbench_model.py`, `test_doxbench_privacy.py`, and T099's two-way redaction drill |
| FR-021 | EVIDENCED | `PUBLIC_ENTRY_FIELDS` allowlist; `test_doxbench_model.py`, `test_doxbench_routes.py` |
| FR-022 | EVIDENCED | credential/endpoint spelling scans both sides; `test_doxbench_privacy.py`, the delegated validator's scan, T099 (no credential-shaped value anywhere) |
| FR-023 | EVIDENCED | same-origin only; `test_renderer.py` fetch-site arithmetic, `test_staging_workbench.py` |
| FR-024 | EVIDENCED | console-presence + real checkout + resolved actor; `test_gate_console.py`, `test_doxbench_routes.py` |
| FR-025 | EVIDENCED | empty catalog is a success posture, editors stay usable; `test_doxbench_routes.py`, `test_doxbench_view.py` |
| FR-026 | EVIDENCED | typed proposals validated against observed hashes; `test_doxbench_proposals.py`, `test_doxbench_turns.py` |
| FR-027 | EVIDENCED | Apply exposed only for a valid typed proposal; `test_doxbench_proposals.py` |
| FR-028 | EVIDENCED | `applyProposal` re-checks the settled identity at the swap; `test_doxbench_proposals.py`, `test_doxbench_view.py` |
| FR-029 | EVIDENCED | stale is terminal-until-new-turn, no merge/force path; `test_doxbench_proposals.py`, T100 clause 6 |
| FR-030 | EVIDENCED | Apply is a local reversible edit that marks dirty and calls no gate; `test_doxbench_mutation_boundary.py` |
| FR-031 | EVIDENCED | `planRow` create-vs-edit by path; `test_doxbench_save.py`, `test_session_document_ownership.py` |
| FR-032 | EVIDENCED | `commit_first_edit` atomically opens/joins and revalidates; `test_session_transaction.py` |
| FR-033 | EVIDENCED | rollback completed for created documents in **`4b71845`**; `test_session_transaction.py::test_a_failed_create_into_a_JOINED_session_leaves_no_residue_on_any_axis` asserts file/index/worktree/registry/record |
| FR-034 | EVIDENCED | outline-then-document, one action per document; `test_doxbench_save.py`, T100 clause 7 |
| FR-035 | EVIDENCED | per-buffer verdicts, only landed bases advance; `test_doxbench_save.py` |
| FR-036 | EVIDENCED | `tile_owned_prefix` + `first_edit_eligibility`; `test_session_document_ownership.py` |
| FR-037 | EVIDENCED | no delete/merge/approve path, served checkout never written; `test_doxbench_mutation_boundary.py`, `test_session_confinement.py` |
| FR-038 | **EVIDENCED** | the Save outcome re-keys the shell, session bar and rail (**`a57f6af`**), proven live by `test_doxbench_view.py::test_a_save_that_opens_a_session_rekeys_the_chat_rail_not_only_the_canvas`; the R-12 residual — the post-partial-Save turn refused because unsaved buffers keep the pre-session `base_ref` — is CLOSED by the reviewer's binding ruling (2026-08-02, realized in the F5–F10 wave): `_require_buffer_binding` accepts a buffer based on the session's own recorded base revision and still refuses once the session diverged past it for that document; `base_ref` provenance and the byte-identity pin stand unchanged. Guards: `test_doxbench_routes.py::test_the_post_partial_save_turn_grounds_the_unlanded_buffer_on_the_session_base` (turn succeeds), `::test_a_pre_session_buffer_is_refused_once_the_session_moved_the_document` (divergence), and the re-purposed `test_the_post_save_turn_still_declares_the_pre_session_base_for_unsaved_buffers` (provenance preserved) |
| FR-039 | EVIDENCED | `clearDoxBenchSession` on merge/abandon, with the destroy-before-clear order fixed in **`a57f6af`**; `test_doxbench_view.py`, `test_doxbench_state.py` |
| FR-040 | EVIDENCED | hosted/gate-off/source-unavailable postures retain context and remove controls; `test_doxbench_view.py` posture harness |
| FR-041 | **PARTIAL** | desktop/narrow/keyboard-only/zoom/high-contrast measured PASS (`doxbench-t100-evidence.md`: CHK007 across all three tablists, CHK024 6.0:1/6.0:1/14.87:1, CHK025 forced colors, CHK026 reflow); **screen-reader is unexercised** — CHK034a (Edge+Narrator, primary) and CHK034b (Firefox+NVDA, secondary) are DECLARED BUT NOT RUN, and CHK035 passed as a structural proxy only. Operator-gated; tracked as R-10/CHK034a/CHK034b and as ledger task 7.4 |
| FR-042 | EVIDENCED | inherited derivations byte-identical: pinned mount/outline/viewer signatures and the append-only CSS; `test_staging_workbench.py`, `test_completeness.py`, `test_session_snapshot.py`, `test_renderer.py` |
| FR-043 | EVIDENCED | `doxbench_scope` created-paths enter BOTH sets from a server-held record; `test_doxbench_scope.py::test_session_created_paths_for_scope_lands_in_both_projection_sets`, `test_doxbench_routes.py` forgery pins |
| FR-044 | EVIDENCED | no analytics/telemetry/crash reporting in the bundle; `test_renderer.py` (fetch sites), `test_staging_workbench.py` (no external URL, no dynamic import), `test_hermeticity.py` |
| FR-045 | **EVIDENCED** | byte-exact Unicode round-trip is proven (`doxbench_hash` shared vectors incl. CRLF/combining/astral: `test_doxbench_hash.py`, `test_doxbench_turns.py::test_crlf_content_is_preserved_exactly_no_newline_normalization`) and the F5–F10 wave closed its two residuals: `dir="auto"` on both authoring textareas and previews (F9, `test_authoring_surfaces_disable_autofill_and_derive_text_direction`), and the CRLF round-trip made real end to end — the server's base revalidation reads through the served lens (`served_text`), the governed writes pin `newline=""`, and the editor preserves the document's EOL flavor through the textarea's forced-LF projection (F10, commits c2f432c + ebbcf70) |

---

## Part C — Speckit success criteria (12)

| SC | State | Realization evidence |
|---|---|---|
| SC-001 | EVIDENCED | `doxbench-t100-evidence.md`: a real topic opened, both buffers edited, discussed, one valid proposal applied, and the result saved without leaving doxBench (clauses 1-7) |
| SC-002 | EVIDENCED | observed hashes echoed per turn and recomputed server-side; `test_doxbench_turns.py`, `test_doxbench_routes.py` success envelope |
| SC-003 | EVIDENCED | `test_doxbench_mutation_boundary.py` (20 tests) plus T100's untouched served checkout |
| SC-004 | EVIDENCED | `test_doxbench_proposals.py` stale matrix; T100 clause 6 on the live surface |
| SC-005 | EVIDENCED | `test_doxbench_save.py` (order, one action per document, partial success); T100 clause 7 verified in git |
| SC-006 | EVIDENCED | `test_session_transaction.py` fault-injection at every step, incl. the F3 create-residue case (**`4b71845`**) |
| SC-007 | EVIDENCED | `test_doxbench_view.py` posture harness + the shell-level withholding pin |
| SC-008 | EVIDENCED | `test_doxbench_routes.py` (empty catalog = success), `test_doxbench_view.py` (editors usable, posture stated) |
| SC-009 | EVIDENCED | `test_doxbench_accessibility.py` casing pins; `test_doxbench_contracts.py` artifact compatibility |
| SC-010 | **PARTIAL** | keyboard-only leg passes at both widths (T100 CHK007/CHK024/CHK026, Playwright-measured); the assistive-technology leg is DECLARED BUT NOT EXERCISED (CHK034a/CHK034b). Same gap as FR-041 |
| SC-011 | EVIDENCED | `test_doxbench_privacy.py`, the delegated validator's credential/endpoint scan, and T099's grep-verified zero-marker serve output |
| SC-012 | EVIDENCED | `doxbench-t100-evidence.md`: all ten clauses PASS on the real corpus across four runs, ending in the real merge-ending cleanup (`torn_down: [worktree, registry-entry]`, branch deleted, index back to `main`) |

---

## Part D — the honest gaps

Five of 109 rows were PARTIAL at archive time. None was unknown; each had a
named carrier. The F5–F10 wave (2026-08-04/05) closed the FR-038 row per the
R-12 ruling and the FR-010 and FR-045 rows with the F6/F9/F10 fixes — see
their Part C entries — leaving only the screen-reader legs below.

| Item | Gap | Why it is not closed here | Carrier |
|---|---|---|---|
| FR-041, SC-010, and the CHK035 leg of the AT sheet | no screen reader has spoken this surface | operator-gated: the declared primary (Edge+Narrator) and secondary (Firefox+NVDA) legs need a human at a Windows AT plane | ledger task 7.4; `CHK034a`/`CHK034b`; R-10 |

Everything else — 107 of 109 rows — has an implementing code path and a test or
an operator record that proves it.

## Coverage statement

- 52 delta scenarios: 52 rows, 52 EVIDENCED.
- 45 Speckit FRs: 45 rows, 44 EVIDENCED, 1 PARTIAL (FR-041) — FR-038 moved
  PARTIAL → EVIDENCED with the R-12 closure, FR-010 and FR-045 with the
  F6/F9/F10 fixes (F5–F10 wave, 2026-08-04/05).
- 12 Speckit SCs: 12 rows, 11 EVIDENCED, 1 PARTIAL (SC-010).
- **109 of 109 items mapped.**
