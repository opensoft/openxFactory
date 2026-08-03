## Context

Three lines of work now meet in **doxBench**, the product and user-facing name
for the integrated authoring evolution of the dashboard's staging workbench:

1. `add-staging-workbench` shipped a scoped, read-only `docs / lens / outline`
   surface and explicitly deferred editing and chat.
2. `add-workbench-bullseye-and-create` and
   `add-workbench-branch-sessions` added governed creation, branch-confined
   editing, branch-aware reads, and the worktree as the draft source of truth.
3. codexFactory's earlier `ai-spec-doc-editor` brainstorm established the
   product expectation for an editor with inline/side-panel AI and model choice,
   but it remained separate from the ideation dashboard.

The codexFactory realizations of the staging workbench, repository/ref registry,
create flow, branch sessions, and external-editor escape hatch are merged. The
recorded common baseline is codexFactory `main` at `34bfc2f`, where the dashboard
suite passes 1467 tests; `008-fix-dashboard-edit` is present through PR #56
merge `d2c16b1`. Their openxFactory changes are not yet archived, so the
promoted `openspec/specs/ideation-dashboard/` capability does not exist. This
change is deliberately stacked on their latest complete delta. It cannot
archive until that predecessor chain is promoted. Under the governed D0
exception recorded below, Speckit and code realization may start before that
promotion, but the resulting realization cannot merge until its contract and
promotion prerequisites are discharged.

The current renderer is a static ES-module application with no bundler. It may
use same-origin backend routes supplied by the local dashboard server, but the
bundle must contain no external URL, provider credential, or direct model
client. The served checkout never moves. Existing corpus writes happen only
through human-console gate routes, and a branch-session action produces one
commit carrying its document and gate-action record.

The word “subject” is overloaded elsewhere in the family for identity-bearing
customer and domain subjects. The user-facing chat control in this change is a
free-form authoring focus, so the contract and UI call it `working_subject`.

The doxBench name is presentation and project nomenclature. Existing
`workbench-*` schemas, routes, module names, branch-session records, and the
`ideation-dashboard` capability remain stable technical identifiers.

The non-normative
[doxBench brainstorm overview](../../../ideation/brainstorm/doxbench-overview.md)
decomposes this design into atomic mechanisms and relationship syntheses.
This document and its OpenSpec delta remain authoritative for the proposed
decisions and requirements.

## Goals / Non-Goals

**Goals:**

- Put the complete human/AI authoring loop in doxBench: edit outline or
  document, ask the selected model, review/apply a proposal, edit again, and
  have the next turn see exactly those current buffers.
- Preserve the existing `docs` and `lens` material as context without making
  either one the authoring canvas.
- Let unsaved edits participate in a chat turn while keeping persistence
  explicit, branch-confined, and governed.
- Bind every turn and proposal to content hashes so late model output cannot
  overwrite newer human work.
- Keep provider credentials and routing policy server-side and make a
  no-provider deployment degrade to a useful editor rather than a broken chat.
- Preserve the hosted dashboard's read-only posture.

**Non-Goals:**

- Real-time multi-cursor collaboration or a CRDT. A branch session remains
  collaborative at the git/worktree level; simultaneous buffer merging is a
  successor capability.
- Rich DOCX/Google Docs/Word editing, realm add-ins, or the standalone neutral
  editor product from the older brainstorm.
- Autonomous agent writes, silent AI application, autosave commits, deletion,
  direct writes to `main`, or any new lifecycle/gate authority.
- NotebookLM as chat transport or mandatory grounding. Session notebooks remain
  a separate optional tool.
- Hosted chat or hosted editing before hosted identity, model brokerage, and
  governed write application are separately approved.
- A general family-wide model gateway. The provider port is intentionally
  narrow, though it can be extracted later if a second interactive consumer
  proves the abstraction.

## Decisions

### D0 — Stable code baseline required; predecessor governance remains a merge gate

**Original decision**: documentation and ratification could proceed, but
Speckit realization would not start until:

1. the codexFactory `008-fix-dashboard-edit` select-to-edit work is present in
   the common baseline — cleared 2026-07-28 by PR #56 merge `d2c16b1`;
2. the remaining first-real-commission, contract-registration, aggregation
   wiring, and Brett live-pass tasks for `add-propose-verb`,
   `add-staging-workbench`, `add-workbench-bullseye-and-create`,
   `add-dashboard-repo-selector`, and `add-workbench-branch-sessions` close;
3. the OpenSpec changes archive in this order:
   `add-ideation-dashboard` → `add-propose-verb` →
   `add-staging-workbench` → `add-workbench-bullseye-and-create` →
   `add-dashboard-repo-selector` → `add-workbench-branch-sessions`; and
4. this change is rebased on that promoted capability, revalidated, and
   ratified.

`008-fix-dashboard-edit` is not thrown away: its external-editor action remains
the escape hatch for main-resident documents and any unsupported editor mode.

**Alternative considered**: begin on codexFactory `main` because the code is
already merged. Rejected: the governing capability is still an active stack,
and implementation would otherwise choose behavior against contracts that can
still move during their live passes.

**RULING — implementation-start exception (Brett, 2026-07-29)**: Brett
explicitly approved starting the doxBench Speckit/code lane from the clean
merged codexFactory baseline without first cutting a one-item predecessor
contract bundle. Items 2–4 above remain open governance debt and remain
mandatory before archive. The exception MUST NOT be read as completing their
acceptance clauses, promoting `ideation-dashboard`, or authorizing doxBench to
merge without its own registered and pinned contract package. Any divergence
between the stacked delta and the later promoted capability MUST be reconciled
before merge.

### D1 — doxBench is a three-region authoring shell

**Decision**: on desktop doxBench contains:

```text
                              doxBench
┌──────────────┬──────────────────────────────┬───────────────────────┐
│ Context      │ Authoring canvas             │ Chat rail             │
│ docs / lens  │ [ Outline | Document ]       │ Working subject       │
│ + active doc │ editable source + preview    │ transcript            │
│              │ save / discard / dirty state │ model + composer      │
└──────────────┴──────────────────────────────┴───────────────────────┘
```

`docs` and `lens` remain available as a context rail/drawer, preserving all
existing scope derivations and completeness/interconnectedness behavior. They
are no longer peers of the editable outline. The canvas has exactly two primary
tabs: `Outline` and `Document`. Narrow layouts stack the same three regions in
that order and preserve keyboard access and state.

**Alternative considered**: add `document` as a fourth peer beside
`docs / lens / outline`. Rejected: `docs` is a set browser while `document` is
an authoring target, and keeping both at one tab level would preserve the
current conceptual ambiguity instead of creating the requested canvas.

### D2 — Outline and document are separate explicit buffers

**Decision**: the client holds a `BufferState` for each canvas tab:

- `kind`: `outline | document`
- `path`: repository-relative path or `null` for a new artifact
- `base_ref` and `base_revision`
- `base_hash`: hash of the source content when loaded
- `content` and `content_hash`
- `dirty`

The outline buffer is seeded from the workbench scope's declared outline path
when one exists. If none exists, the canvas shows an honest empty state and
offers a create-backed outline buffer; it does not fabricate an outline or
mistake a document heading list for the topic outline. The document buffer is
the active document selected from `docs` or created through the existing
authoring flow.

They remain separate because the existing outline is topic/fragment material,
not merely a table of contents derived from the active document. Chat can
propose changes to one or both, but synchronization is a human-reviewed
authoring decision, not an automatic rewrite.

**Alternative considered**: derive the outline from document headings and make
document content the sole buffer. Rejected because it would silently redefine
the governed staging fragment and lose outline material that is not a heading
projection.

### D3 — Editing is client-side until an explicit Save

**Decision**: keystrokes and AI proposal application mutate browser buffers
only. They do not call a gate route, regenerate a snapshot, or create a commit.
`Save` compares the current hashes with their base hashes and persists each
changed backed buffer using the existing gate action:

- new path → `create-document`;
- existing path → `edit-document`.

If saving an existing document is the tile's first write, the backend
materializes/joins the tile's branch session and performs `edit-document` there
as one operation. This is the minimal change needed to avoid forcing the human
to create an unrelated file before they may edit existing topic material. A
two-buffer Save produces one existing gate-action commit per changed document,
in a deterministic outline-then-document order; it does not invent a
multi-document commit verb.

After each successful action the existing session refresh rekeys/refreshes the
workbench, and the returned content/revision becomes the buffer's new base.
Partial failure stops the sequence, reports which buffer committed, leaves the
other dirty, and never rolls back a committed gate action by rewriting history.

**Alternative considered**: debounce and autosave after typing. Rejected because
commit-per-keypress-batch would flood the evidentiary history, make model turns
race persistence, and violate the user's ability to review before writing.

### D4 — A chat turn is a bounded snapshot of the current authoring state

**Decision**: the browser posts a versioned `workbench-chat-turn` envelope to a
same-origin local route. It carries:

- repository, ref, tile kind/id, and active document path;
- `working_subject` and the new user message;
- bounded prior transcript turns;
- outline and document buffer descriptors, full current content, and hashes;
- the last accepted assistant turn id, when any; and
- selected model id from the server catalog; and
- a client-generated turn id used as the local process's idempotency key.

The server resolves the repository/ref and allowed paths independently, verifies
the content hashes, assembles a bounded prompt, and records in the response
which hashes the model saw. Unsaved content is intentionally sent because that
is the feature: the next turn must see human edits before they are saved. The
server never represents unsaved text as governed or committed state.

Transcript, working subject, and selected model are stored in `sessionStorage`
under `(repository, ref, tile kind, tile id)`. They are browser-local working
state, not a branch-session descriptor, snapshot field, corpus artifact, or
shared conversation. They are cleared when the session ends and invalidated
when the active key changes unexpectedly.

The request and response schemas set hard byte, turn-count, and output limits.
The server refuses an over-budget request with the measured limit rather than
silently truncating a document. The UI may offer a deliberate “send bounded
selection” successor, but v1 never lies about what the model saw.

Only one turn may be in flight for one conversation key. Repeating a completed
client turn id in the same server process returns the recorded result without a
second provider dispatch; repeating an in-flight id attaches to or reports that
turn, and reusing the id with different hashes refuses. A provider failure
produces a fixed redacted error, leaves both buffers unchanged, and never creates
an assistant proposal.

**Alternative considered**: have the server re-read only the worktree. Rejected
because it would omit the human's unsaved changes and fail the central turn
loop.

### D5 — AI output is prose plus optional typed proposals, never a write

**Decision**: a successful response contains assistant prose and zero or more
typed proposals:

- target `outline` or `document`;
- complete proposed content;
- `base_hash` equal to the buffer hash supplied for the turn;
- a human-readable summary; and
- response/turn ids for traceability in browser state.

The human can apply a proposal to the corresponding buffer. Apply is a local,
reversible buffer replacement and is distinct from Save. If the current buffer
hash no longer equals `base_hash`, Apply refuses as stale and offers three
honest choices: keep current, inspect current versus proposed, or run a new turn.
There is no automatic merge and no “apply anyway” button that bypasses review;
the human may manually copy from the comparison if they truly want the old
proposal.

**Alternative considered**: return arbitrary Markdown and let the client infer
which artifact to replace. Rejected because inference is exactly how a chat
answer becomes an accidental write.

### D6 — The model selector is a server-declared catalog over an injected port

**Decision**: a same-origin model-catalog response exposes stable UI ids,
labels, provider class, context/output limits, and a data-handling badge. It
contains no credential, raw endpoint, secret environment-variable name, or
provider request template. The turn route accepts only a catalog id and resolves
it server-side through an injected `WorkbenchModelPort`.

The first implementation may provide:

- a configured on-tenant/local/subscription adapter; and
- a hosted fallback only when its policy explicitly requires zero retention and
  the deployment has opted in.

This reuses the family's routing and data-handling posture, not the governed
review lane's ensemble semantics or code path: an interactive authoring turn is
not a three-model formal review. With no allowed model, the catalog is empty,
the chat rail explains why, and both editor tabs remain usable.

**Alternative considered**: let the browser call OpenAI-compatible endpoints
directly with BYO keys. Rejected because it leaks credentials and provider
configuration into an untrusted surface, evades same-origin controls, and makes
data-handling policy unenforceable.

### D7 — Chat is local-plane; persistence keeps all existing authority checks

**Decision**: model catalog and turn routes are available only on the loopback
human console with a real checkout and resolved actor. They require the same
per-serve console-presence token as other sensitive local actions, even though a
turn is non-mutating, because it can disclose corpus and unsaved text to a model.
The route validates repository/ref confinement and the tile's scoped document
membership before any provider call.

Save continues through `create-document` / `edit-document`; the chat route
cannot call those verbs. Hosted and gate-off surfaces render the read-only
workbench and no disabled controls that imply authority they do not have.

**Alternative considered**: allow hosted chat but keep Save disabled. Rejected:
hosted chat still sends internal corpus material to a model and needs identity,
tenant policy, audit, and a model broker even when it does not write.

### D8 — The UI distinguishes working subject from every identity subject

**Decision**: the wire field is `working_subject`; the visible label is
“Working subject.” It defaults from the tile title/summary, remains editable,
and affects prompt focus only. Schema descriptions explicitly prohibit treating
it as `subject_ref`, actor, customer, patient, tenant, authority, or routing
identity.

**Alternative considered**: keep the shorter `subject`. Rejected because the
repository now has a formal customer-subject contract, and an ambiguous field
would eventually be misbound.

### D9 — The editor uses the existing Markdown renderer and adds no remote UI dependency

**Decision**: v1 provides an accessible Markdown editing control plus live
rendered preview for both buffers, reusing the vendored renderer and sanitizing
path already used by the viewer. The implementation may enhance the editing
control behind an interface, but it must not add a CDN, dynamic import, or
browser-to-provider network call. Selection, cursor, scroll, dirty state, and
tab state survive a chat response and context-panel navigation.

**Alternative considered**: adopt TipTap/BlockNote immediately. Rejected for
this change because the dashboard has no bundler and the dependency/license
surface would dominate the authoring-loop work. The older standalone editor
product may still choose one under its own change.

### D10 — One combined real-corpus pass closes the predecessor experience gates

**Decision**: before implementation starts, run one scripted/manual dogfood pass
that exercises the real corpus end to end and records evidence once while
checking each predecessor's remaining live criteria:

- workbench completeness/readiness credibility;
- bullseye-driven document creation and source provenance;
- repository publication/refresh across the configured roster; and
- branch-session create, edit, notebook refresh, PR, merge, and published
  visibility; followed by the first real `propose` commission from the now
  session-free ready topic, with its descriptor and gate-action record.

Each predecessor task is checked only if its own acceptance clauses pass; the
combined run is a scheduling optimization, not evidence laundering.

### D11 — doxBench is the surface name, not a protocol rename

**Decision**: the integrated dashboard authoring surface is named
**doxBench**. Product copy, headings, navigation labels, accessibility names,
documentation, tests, and realization evidence use that exact casing.

The inherited capability remains `ideation-dashboard`; the architectural
foundation remains the staging workbench; technical identifiers such as
`xfactory-workbench-model-catalog`, `xfactory-workbench-chat-turn`,
`workbench-chat-turn`, `WorkbenchModelPort`, existing route paths, and
branch-session records remain unchanged. No persisted artifact is rewritten
solely to adopt the name.

**Alternative considered**: rename every `workbench-*` identifier together
with the surface. Rejected because those names are stable contract vocabulary
shared with predecessor changes, while doxBench names the human-facing
experience assembled over them.

## Risks / Trade-offs

- **[Unsaved content leaves the browser during a model turn]** → show the
  selected model's data-handling badge at send time, keep routes local-console
  only, require explicit provider enablement, and never send to an unlisted
  model.
- **[Large documents exceed a model or request budget]** → enforce catalog and
  schema limits before dispatch, report the exact excess, and never silently
  truncate.
- **[A delayed response overwrites newer human edits]** → bind proposals to
  per-buffer hashes and refuse stale Apply.
- **[Two collaborators edit the same tile concurrently]** → branch session
  collaboration remains git/worktree-level in v1; hash/ref checks refuse stale
  saves. Real-time merge/presence is explicitly deferred.
- **[Saving both buffers partly succeeds]** → deterministic sequential actions,
  precise partial-success UI, no history rewrite or hidden rollback.
- **[Chat language is mistaken for an accepted edit]** → only typed proposals
  get Apply controls; Apply changes a buffer only; Save is separately explicit.
- **[Provider abstraction becomes a premature platform]** → keep one narrow
  injected port and extract only after another interactive consumer exists.
- **[The new layout hides existing docs/lens capabilities]** → preserve them as
  a labelled context rail/drawer with state retained across canvas/chat use.
- **[The landed external-editor action conflicts in the viewer]** → preserve
  PR #56's action outside integrated session authoring and verify it explicitly
  when this feature rebases before Speckit planning.

## Migration Plan

1. Retain the landed codexFactory PR #56 external-editor baseline and record
   the D0 implementation-start exception without closing predecessor debt.
2. Create one codexFactory Speckit feature/worktree for realization from the
   clean merged baseline.
3. In parallel with realization, close and archive the D0 predecessor chain;
   then rebase this change on the promoted `ideation-dashboard` capability,
   replace any stacked source text with the promoted requirement text, and run
   OpenSpec validation before merge.
4. Land schemas/examples first, then model port and same-origin routes behind
   an off-by-default capability.
5. Land editor buffers and layout with chat disabled; verify existing
   docs/lens/viewer/session flows unchanged.
6. Land bounded turn assembly, catalog/model adapter, typed proposals, and
   stale-apply protection.
7. Land save integration, first-edit session materialization, browser
   acceptance, and real-corpus dogfood evidence.
8. Roll out locally with no configured model by default; enable an allowed
   model per deployment after the data-handling badge and request audit pass.

Rollback disables the model catalog/turn capability and returns doxBench to
read-only/context plus the external-editor escape hatch. Because chat and buffer
application write no corpus state, and saved state uses ordinary branch-session
commits, rollback needs no data migration.

## Open Questions

None required before proposal review. Model allowlist entries, byte/turn limits,
and exact UI breakpoints are realization constants to be calibrated and pinned
in the Speckit plan; changing their security or data-handling meaning requires a
contract amendment rather than an implementation preference.
