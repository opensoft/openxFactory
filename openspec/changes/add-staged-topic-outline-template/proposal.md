---
code_surface: openxFactory (the doxBench outline tab renders the template and gains an add-section affordance; `fragmentSummary()` gains a conforming-topic path; doc-health gains a warning-tier conformance nudge)
target_release: implemented
Status: draft
---

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
affordance that writes through the existing `edit-apply` path.

### The five dispositions, as ruled

| | Question | Ruling |
|---|---|---|
| Q1 | Fragment or separate `outline.md`? | The primary fragment IS the outline — no new file, no selector change |
| Q2 | Migration of 30+ existing topics | Opt-in when next touched; required for new topics; doc-health nudges, never blocks |
| Q3 | Spec delta or convention? | Spec delta — the round-trip guarantee needs contract force |
| Q4 | Verb for AI section-patching | `edit-apply`, scoped by the targeted section |
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
- **Two rulings carry forward rather than landing here.** Q4 makes `edit-apply`
  the verb for section-patching, which upgrades `doxbench-editing-model` Phase
  A's freeform chat rewrites into marker-scoped patches — that upgrade is Phase
  A's to build. Q5 rides Phase B, because Q2's opt-in migration means the
  fallback must stay.
- **Not in scope:** the wheel's 3-line summary extraction change itself (Phase
  B), and any mechanical rewrite of existing topics (Q2 ruled it out).
