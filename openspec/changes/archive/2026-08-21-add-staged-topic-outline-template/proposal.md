---
code_surface: openxFactory (the doxBench outline tab renders the template and gains an add-section affordance; `fragmentSummary()` gains a conforming-topic path; doc-health gains a warning-tier conformance nudge)
target_release: implemented
Status: ratified
Ratified: 2026-08-15 by Brett Heap — in-session, verbatim: "ratify add-staged-topic-outline-template". Follows his acceptance of all five open questions as recommended earlier the same day, which closed the parallel decision track this change was sequenced for.
---

> **REALIZED AND ARCHIVED 2026-08-21.** All 22 tasks are discharged and the code
> is merged on the implemented target across eight pull requests — this change's
> OWN chain, each of which edits a file under this change's folder: #193
> (`93f4241` — doc-health's WARNING-tier `staged-topic-template` family), #195
> (`ea42a43` — the template as contract text in `docs/document-lifecycle.md`),
> #198 (`e0dbcea`, `642dd64` — the outline section model and Amendment 1), #208
> (`26558e7`, `3a1f3aa`, `cd9f683` — the outline tab's section index through the
> `renderViewer` `onText` seam, add-section through `applyProposal`, and Save
> carried by `edit-document` per Amendment 1), #211 (`9dfd59a`, `4c9b46b` — the
> mutation-validated tests for 4.1 and 4.3, plus the honest report that 4.2 was
> blocked by a live demote defect), #217 (`55e8a67`, `7469d1a`, `b84a936` — 4.2
> discharged by DRIVING the real round trip, once the change that defect spawned,
> `align-demote-to-round-trip-rule`, had realized at #215), #224 (`8dde22f`,
> `2f9e876` — bookkeeping 6.1-6.3) and #227 (`5654343`, `8780bf5`, `67ad236`,
> `a70bf01`, `0d4cf16` — gates 5.1-5.3 and the live browser proof 5.4).
>
> SPAWNED CHANGES, REALIZED SEPARATELY and not part of the chain above: task
> 4.2's driven round trip produced `align-demote-to-round-trip-rule` (PR #215 /
> `79ed72e`, archived by this change's #217),
> `refine-demote-round-trip-mechanics` (PR #221 / `6c3d87c`) and
> `align-status-reader-to-real-lines` (PR #222 / `c379a09`), the last two
> archived 2026-08-21 by #225. None of those three PRs touches a file of this
> change; each one's evidence lives in its own archive record. All three are
> closed before this change archived.
>
> The realization proof is task 5.4: headless Chromium through the shipped page,
> the real wheel gesture, the real outline tab, the shipped Save — and the answer
> read out of git. One write route reached (`/actions/gate/first-edit`), one
> verb, and that verb evidenced THREE independent ways: the response body's
> `"verb": "edit-document"`, the commit subject plus its `Gate-Action:` trailer
> on session branch `draft/outline-conformer`, and the committed gate-action
> record's own `action:`. The pre-template topic degraded rather than refused,
> and the served checkout never moved. Task detail, the gate evidence, the 29
> enumerated warning findings and the items left open by ruling are in
> `tasks.md`.
>
> Amendment 1 below is part of the record, not an afterthought: Q4 was ratified
> naming `edit-apply`, which cannot reach a session branch, and the verb the
> code actually uses is `edit-document`.
>
> This block REPLACED the release-realization "APPROVED BUT NOT YET REALIZED"
> banner rather than carrying it through the archive, following
> `align-demote-to-round-trip-rule` (archived 2026-08-19, its task 6.3) and the
> two archives of 2026-08-21 that took the same course: archiving a record whose
> first paragraph says "none of it is built" would state something false about a
> realized change.

# Proposal: add-staged-topic-outline-template

## Why

A staged topic's primary fragment is the one file the wheel selects and the one
document a reader opens first, and today its shape is a convention nobody
checks. Fragments are "conventionally feat-spec-shaped" — which is to say each
one is shaped like whichever fragment its author last read.

That costs three things. A reader cannot extract a topic's live state without
opening the whole folder. A parsing tool has nothing dependable to parse. And
most expensively, a topic that reaches proposal and is then demoted falls back
to its pre-proposal aspirational text, so everything learned while the change
was in flight is discarded exactly when it is most valuable.

Brett's 2026-08-15 direction settled seven claims and left five questions, all
five now dispositioned as recommended. This change carries them.

## What Changes

**A required template for the primary fragment** (`document-lifecycle`). Three
required sections — pre-document idea notes, conflicts, and open questions —
plus the proposal-element sections. Every open question carries four sub-fields
in fixed order: Context, Recommended answer, Explanation, Disposition status.
A question is never left bare: the template forces a recommendation and a reason
for it even while the disposition stays open.

**Round-trip on demote.** A demoted topic's proposal-element sections are
refreshed to the ACTUAL text of the last attempted `proposal.md`, tagged with
the change id, the dates raised and demoted, and the demote reason. They are
never re-blanked to the aspirational original. This is the requirement's whole
point, and it is testable: does a demoted fragment's slot carry the prior
change's real text.

**Provenance on additions.** Sections beyond the required set carry an
`Added-by:` name-or-agent-id and a date, because either a human or an AI may add
one and the document must stay attributable as it accumulates content nobody
commissioned.

**Machine-addressability via the existing marker grammar.** The proposal-element
sections are wrapped in the ratified `xspec:candidate` / `xspec:supersedes`
comment forms rather than a second mechanism invented beside them. That prose is
literally the candidate text an eventual change would carry.

**The outline tab renders it** (`ideation-dashboard`), with an add-section
affordance that writes through the existing `edit-document` path.

### The five dispositions, as ruled

| | Question | Ruling |
|---|---|---|
| Q1 | Fragment or separate `outline.md`? | The primary fragment IS the outline — no new file, no selector change |
| Q2 | Migration of 30+ existing topics | Opt-in when next touched; required for new topics; doc-health nudges, never blocks |
| Q3 | Spec delta or convention? | Spec delta — the round-trip guarantee needs contract force |
| Q4 | Verb for AI section-patching | `edit-document`, scoped by the targeted section (amended 2026-08-15 — ratified as `edit-apply`, see Amendment 1) |
| Q5 | Wheel summary extraction | Read the guaranteed `Summary:` for conformers; keep the fallback for the rest |

## Impact

- **Affected capabilities:** `document-lifecycle` (one ADDED requirement),
  `ideation-dashboard` (one ADDED requirement).
- **Both deltas are ADDED, not MODIFIED as the staging INDEX predicted.** The
  existing `Ideation work area convention` governs where fragments live, and
  `doxBench editor buffer contract` governs buffer mechanics; neither says
  anything about a fragment's internal shape. Folding a template contract into
  either would overload a requirement that answers a different question. Noted
  because the INDEX row will read as a mismatch otherwise.
- **Q1 keeps `primaryFragmentPath()` untouched.** The wheel's one-path rule —
  exactly one deterministically selected file per topic, chosen path-only, never
  content-sniffed — is preserved rather than extended.
- **Q2 means the corpus is deliberately non-uniform for a while.** 30+ existing
  topics stay non-conforming until touched, so every consumer must tolerate both
  shapes. That is why Q5 is additive.
- **Two rulings carry forward rather than landing here.** Q4 makes
  `edit-document` the verb for section-patching (Amendment 1), which upgrades
  `doxbench-editing-model` Phase A's freeform chat rewrites into marker-scoped
  patches — that upgrade is Phase A's to build. Q5 rides Phase B, because Q2's
  opt-in migration means the fallback must stay.
- **Not in scope:** the wheel's 3-line summary extraction change itself (Phase
  B), and any mechanical rewrite of existing topics (Q2 ruled it out).

## Amendment 1 — the section-patching verb (2026-08-15)

**`edit-document`, not `edit-apply`.** Brett's ruling, in session, verbatim:
"amend to edit-document".

Q4 was accepted as recommended on the strength of a stated context —
"the workbench/doxBench branch-session model already exposes an `edit-apply`
intent verb for content changes on a session branch" — that does not hold.
`edit_apply(gate, change_id, document, redline)` is the gate console's
MAIN-RESIDENT redline verb: it requires `--change-id` ("the change owning the
document") and applies to change documents. A staged topic's fragment is not
one. The intent-plane change references the same gate-console verb; there is no
second, session-scoped `edit-apply`.

The two states are mutually exclusive besides. `edit-apply` needs a change id,
but doc-health's `location-conformance` fires the moment a staged fragment cites
a live change and its remedy is to move the material OUT of staging — performed
on this very topic the same day. A fragment whose topic has an owning change is
no longer in staging to patch.

**Q4's intent is unchanged and is what the amendment preserves:** no second
write verb, reuse of the existing session path, and section scoping as a
patch-TARGETING detail rather than a different kind of action. `edit-document`
— the verb the ratified buffer contract already uses for session content —
satisfies all three. Only the verb name was wrong.

Amended here, in the spec delta, and in `docs/document-lifecycle.md`. The
supporting-docs copies are NOT amended: they record the question as it was
asked and ruled, and the `source-snapshots/` copy is checksum-protected by the
bundle manifest — rewriting either would falsify a record to make it agree with
a later correction.
