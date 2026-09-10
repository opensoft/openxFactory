# Design: state-header-window-budget

## 0. CONVENER BRIEF

1. **What.** One paragraph and one scenario added to the promoted requirement
   "Equivalent declaration sites for the ordered-delta parent declaration"
   (`release-realization`), stating that the bounded lifecycle header
   window is counted from a document's own line 1 and that a leading
   `---` fence's lines count toward that budget rather than being excluded
   from it. Nothing existing is reworded, reordered or removed.
2. **Why.** A Copilot review on PR #906 (the archive that promoted the
   requirement) found the gap; Brett Heap agreed on that thread but declined
   to fix it there, because editing an archive's promoted text with no
   ruling behind the edit breaks the sha256 byte-identity that archive's own
   evidence rests on, and named this packet's shape. `proposal.md` § Origin
   quotes both comments in full.
3. **The fact is not in question; only the wording is.** `scripts/frontmatter_strict.py`
   already counts the window this way (docstring at lines 541–545, executable
   arithmetic at lines 565 and 569), the archived packet's own `tasks.md`
   § 2.3 already says so, and this session re-confirmed it empirically on
   the branch (§ D1 below) rather than trusting the docstring's word for it.
   The only decision left to the convener is whether the added sentences say
   it well.
4. **Blast radius: zero, measured, at the level that matters: runtime
   behavior.** No script, test or contract EXECUTES any differently because
   of this requirement's prose; `code_surface: none`. This is narrower than
   "no script reads the prose" — `scripts/doc_health/modified_block_currency.py`'s
   own currency gate mechanically parses every active `## MODIFIED` block,
   this one included, to diff it against canon, and that parse IS Group 2's
   validation gate this packet passes, not a behavioral consumer the zero-blast-radius
   claim is about. No consumer re-vendors; no pin moves. `proposal.md` § Impact.

## Context

- **Basis.** `accept-sequenced-after-header-line` (ratified 2026-09-10,
  archived same day, PR #886 → archive PR #906) added the requirement this
  packet modifies and promoted it into `openspec/specs/release-realization/spec.md`.
  Its `tasks.md` § 2.3, written at authoring time and never disputed, already
  states the fence-counts-toward-the-window design choice in words; this
  packet's only job is moving that sentence from a task record into the
  requirement itself.
- **Precedents.** Brett Heap's own PR #906 reply named
  `amend-marker-reason-boundary` and `amend-neutral-product-pin-interim-copy-vocabulary`
  as the shape a narrow amendment like this one takes in this corpus. The
  second is the closer template: `ad_hoc`, `code_surface: none`, one
  `## MODIFIED` requirement, archives on landing.

## Decisions

### D1 — Verified empirically, not just read from the docstring
The docstring the Copilot comment cites (lines 541–545) already asserts the
fence-counts-toward-the-window rule in prose, but a docstring can drift from
the code beneath it, so this packet is not authored on the docstring's word
alone. On this branch: a `sequenced_after:` header line at the document's
real line 19, behind a four-line fence, reads `NO_HEADER_LINE` — it would be
admitted under the (wrong) reading "the window is fifteen lines counted
after the fence closes," which a fence ending at line 4 would place at
real lines 5–19 inclusive. The same header line at real line 15, behind the
same fence, IS read — line 15 being the window's own absolute edge, fence
included. `proposal.md` § Why quotes both results. This is the fact the
added paragraph states; it is not this lane's reading, it is what the
function returns.

### D2 — A new paragraph, not a reworded sentence
The existing sentence — "outside any leading `---` fence, whose lines are
read by the front-matter reader and MUST NOT be counted a second time as
header lines of the same document" — is TRUE and stays. It answers "is a
fence's line a second declaration site?" (no); it does not answer "does a
fence's line still occupy a slot in the window's count?" (yes). Rewording
that sentence to carry both facts risks losing the first while stating the
second, and would turn a pure addition into an edit needing a `Removed from
canon` marker for no gain. A NEW paragraph, immediately after it, states the
second fact without touching the first. Carried this way, the delta needs no
marker of either kind (`document-lifecycle`'s reserved forms declare
deletions; this packet makes none).

### D3 — The scenario is placed after "The same bytes appear beyond the
header window", not after the positive first scenario
The new scenario, `Fence lines consume the header window budget`, is a
fenced-document special case of the general "beyond the window is prose"
rule the second existing scenario already states, so it reads best
immediately after it rather than after the first scenario (which explicitly
excludes fences: "a proposal carries no `---` front matter"). No scenario
is renumbered; scenarios are unordered `####` headings and the file order is
editorial only.

### D4 — No number is written into the requirement text
Neither the existing text nor this addition states "fifteen" or "fifteen
real lines" — the requirement refers to "the document's BOUNDED LIFECYCLE
HEADER WINDOW … that this corpus already reads a document's `Status:`
header in," by reference rather than by literal. This packet follows the
same convention rather than introducing the first hardcoded window size
into this capability's promoted text: `HEADER_WINDOW_LINES` is held equal
to `doc_health.corpus.STATUS_SCAN_LINES` by an agreement test, not by the
spec, and a number written into the requirement would go stale exactly
where the code does not.

## Risks / trade-offs

- **None found at the behavioural level** — the code, the docstring and the
  archived task record all already agree; this packet changes what the
  requirement SAYS, not what anything DOES.
- **The one thing worth a convener's read is wording, not substance**: does
  the added paragraph read as a clarification of the existing sentence
  (intended) or as if it were correcting it (not intended, and not true —
  the existing sentence was never wrong, only incomplete on an adjacent
  question)?

## Open questions

None carried forward. `proposal.md` § Open questions.
