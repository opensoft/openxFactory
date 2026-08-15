---
code_surface: openxFactory (the doxBench outline tab renders the template and gains an add-section affordance; `fragmentSummary()` gains a conforming-topic path; doc-health gains a warning-tier conformance nudge)
target_release: implemented
Status: ratified
Ratified: 2026-08-15 by Brett Heap — in-session, verbatim: "ratify add-staged-topic-outline-template". Follows his acceptance of all five open questions as recommended earlier the same day, which closed the parallel decision track this change was sequenced for.
---

> **APPROVED BUT NOT YET REALIZED.** This change has a non-empty code surface and
> none of it is built: the outline tab does not render the template, there is no
> add-section affordance, `fragmentSummary()` has no conforming-topic path, and
> doc-health has no conformance nudge. Under `release-realization`'s archive
> gate it therefore stays ACTIVE as approved intent until its code merges on the
> implemented target with a green run — the invariant being that promoted specs
> describe what the code does. Nothing here should be read as shipped.

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
