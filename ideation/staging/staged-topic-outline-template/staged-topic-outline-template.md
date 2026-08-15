# Staged: a distilled outline template for staged topics

Status: staged
Kind: capability-proposal
Summary: Gives the doxBench outline tab a standard, distilled template for a
staged topic's primary fragment, for both human and AI consumption: the
basic elements of a proposal (Why / What changes / Impact) filled with the
current "possible draft" values, refreshed to the ACTUAL text of the last
attempted proposal on a demote (round-trip semantics), three required
sections (idea notes, conflicts, and open questions carrying a recommended
answer plus explanation), human-or-AI-addable sections carrying provenance,
and the ratified `xspec:` prose-tagging markers so the sections stay
machine-addressable. RECOMMENDS the primary fragment itself as the outline —
no new file, no selector change — flagged as a recommendation rather than a
ratified decision in Open question 1.
Topics: outline-template, primary-fragment, doxbench, wheel-model,
document-lifecycle, ideation-dashboard, round-trip-demote,
prose-tagging-markers, open-questions
Repository context: openxFactory owns both target capabilities —
`document-lifecycle` (the fragment template contract itself: required
sections, the round-trip-on-demote refresh rule, section provenance, marker
usage) and `ideation-dashboard` (the doxBench outline tab that renders the
template and would gain an add-section affordance). The wheel already
deterministically selects a topic's primary fragment
(`primaryFragmentPath()`, `scripts/ideation_dashboard/web/views/wheel-model.js`)
and extracts its controlled header block's `Summary:` field for the expanded
tile's 3-line preview (`fragmentSummary()`, same file) — this template is
written to stay compatible with both mechanisms without a selector change.
Staging ID: openxFactory:staging:staged-topic-outline-template
Captured: 2026-08-15
Source: Brett Heap's direction 2026-08-15 (in-session): the doxBench outline
tab today renders a staged topic's primary fragment, which is only
conventionally "feat-spec-shaped" — Brett wants it to be a distilled TRUE
outline of the staged topic, for both human and AI consumption, with a
standard template.
Target capabilities: MODIFIED `document-lifecycle` (the fragment template
contract: required sections, round-trip-on-demote refresh rule, section
provenance, marker usage) and MODIFIED `ideation-dashboard` (the doxBench
outline tab renders the template; gains an add-section affordance)

## Context

`primaryFragmentPath()` selects one file per staged topic — the markdown
file named `<staging_id>.md` if one exists, else the shallowest markdown
file in the folder — and the wheel's expanded tile renders that file's
`Summary:` header field (or, failing that, its first meaningful paragraph)
as a 3-line preview. Today that primary fragment is only conventionally
feat-spec-shaped: every topic in this folder happens to carry roughly a
Context/Claims/Open-questions/Exit shape because authors have imitated each
other, not because any contract requires it, and nothing requires the three
sections Brett wants most (idea notes, conflicts, structured open
questions) or the round-trip guarantee that a demoted proposal's actual
attempted text survives the trip back to staging. This topic proposes
making that convention a real, machine-checkable template.

## Claims

The following are settled by Brett's 2026-08-15 direction and are NOT
reopened by the open questions below — they are the fixed baseline the
questions iterate against:

1. The outline is for BOTH human and AI consumption. It is not a build log
   and not decorative front-matter: every section exists so a reader, or a
   parsing tool, can extract the topic's live state without opening the
   whole folder.
2. **RECOMMENDED design (not yet ratified — see Open question 1):** the
   primary fragment `<staging_id>.md` — the exact file `primaryFragmentPath`
   already deterministically selects — IS the templated outline. No new
   file, no selector change, no second "true" document competing with the
   primary fragment for authority. Every other file in a topic folder stays
   free-form (source dumps, brainstorm carry-overs, `openspec/` draft
   workspaces per the draft-proposal convention).
3. Three sections are REQUIRED on every conforming topic: (a) pre-document,
   non-documented idea notes; (b) conflicts; (c) open questions. The third
   is where Brett spends the most attention, so it carries more structure
   than anything else in the document.
4. Every open question carries four sub-fields, in this fixed order:
   Context, Recommended answer, Explanation, Disposition status. A question
   is never left as a bare question — the template forces a recommendation
   and a reason for it even while the disposition itself stays open.
5. Sections are extensible by EITHER a human or an AI. Every section added
   beyond the required three plus the proposal-element sections carries
   provenance — an `Added-by:` name-or-agent-id and a date — so the
   document stays attributable as it accumulates content nobody
   commissioned in advance.
6. **Round-trip semantics.** A topic that reaches proposal, drafts real
   proposal content, and is then demoted back to staging (Brett's demote
   verb, or a failed/reverted push) does NOT reset the proposal-element
   sections to their pre-proposal aspirational text. They are refreshed to
   the ACTUAL text of the last attempted `proposal.md` (Why / What changes /
   Impact), tagged with the change id and the dates raised and demoted, and
   the demote reason — so nothing learned while the change was in flight is
   lost by falling back to staging.
7. **Machine-addressability.** The template uses the document-lifecycle
   spec's ratified `xspec:` prose-tagging marker grammar — the
   `xspec:candidate`/`xspec:supersedes` comment forms cited in
   `docs/document-lifecycle.md` "Prose Tagging Markers" (see the fenced
   skeleton below for the exact marker text) — to wrap the proposal-element
   sections. That prose IS, quite literally, the candidate text an eventual
   OpenSpec change would carry; the marker grammar already exists for
   exactly this content, so the template reuses it rather than inventing a
   second mechanism beside it.

## The draft template itself

The recommended shape for a conforming `<staging_id>.md`, as a copy-pasteable
skeleton. Every bracketed `<…>` is a fill-in slot; the marker comments are
the real, ratified `xspec:` grammar (not illustrative syntax of its own) —
copying this fence into a real topic and filling the slots produces a
document doc-health's tag-hygiene family will accept unchanged.

```markdown
# Staged: <short topic title>

Status: staged
Kind: <capability-proposal | architecture | staging-packet | ...>
Summary: <2-4 sentences, plain prose, no heading directly above it — this is
what the wheel's expanded tile shows verbatim, so write the topic's own
substance here, not a restatement of the title>
Topics: <comma-separated keyword tags>
Repository context: <which repo(s) own the target capability/capabilities;
who realizes the change>
Staging ID: openxFactory:staging:<topic-slug>
Captured: <YYYY-MM-DD>
Source: <who named this topic, when, and from what — a brainstorm doc, a
live session ruling, a cross-repo pointer>
Target capabilities: <ADDED|MODIFIED> `<capability>` (<one-line delta
summary>)[ and <ADDED|MODIFIED> `<capability-2>` (<one-line delta summary>)]

## Last proposal attempt (round-trip provenance)

<!-- Stays "none yet" until this topic first reaches proposal. On DEMOTE,
     replace every field below with the ACTUAL values from the demoted
     change — never re-blank them; that is the whole point of this slot. -->

Change ID: none yet
Raised: n/a
Status at demote: n/a
Demoted: n/a
Demote reason: n/a

## Claims

<!-- Settled context the open questions below should NOT reopen. -->

- <a decided fact or ruling this topic treats as fixed>

## Why

<!-- xspec:candidate target=<target-capability-1> -->
<one paragraph: the problem, in the shape a proposal.md "## Why" section
would state it — the CURRENT possible-draft answer, not a placeholder>
<!-- /xspec:candidate -->

## What changes

<!-- xspec:candidate target=<target-capability-1> -->
<one or more paragraphs: the CURRENT possible-draft shape of the change,
written the way a proposal.md "## What changes" section would read>
<!-- /xspec:candidate -->

## Impact

<!-- xspec:candidate target=<target-capability-1> -->
- Affected specs: `<capability>` (ADDED|MODIFIED — <requirement area>)
- Affected code: <repo(s) / path(s)>
- <other blast-radius notes>
<!-- /xspec:candidate -->

## Idea notes (pre-document, non-documented)

<!-- Free-form thoughts that have not earned a claim, a question, or a
     proposal line yet. Anyone — human or agent — may append. -->

- <idea note text> — Added-by: <name or agent/model id> · <YYYY-MM-DD>

## Conflicts

<!-- Honest tensions this topic has NOT resolved: with another staged
     topic, with a promoted spec, with itself. A conflict names something
     currently INCONSISTENT, even when the reconciliation is "defer,
     noted" — it is not the same thing as an open question. -->

- <conflict text> — Added-by: <name or agent/model id> · <YYYY-MM-DD>

## Open questions

<!-- The section read most closely. Every question gets all four
     sub-fields below, in this order, even when the answer feels
     obvious — "obvious" is exactly when a wrong disposition ships
     silently. -->

### Q1. <question, as a single sentence>

Context: <what makes this undecided; what facts bear on it>
Recommended answer: <a position, stated plainly — not a survey of options>
Explanation: <why this is the recommended answer — the reasoning, not a
restatement of the recommendation>
Disposition status: open
Added-by: <name or agent/model id> · <YYYY-MM-DD>

## Exit

<one or two sentences: what crossing the proposal gate looks like for this
topic, and what must be true first (e.g. "every open question above carries
a disposition other than `open`"). Do not cite an existing change-id here —
doc-health's location-conformance family scans Exit-labeled lines for
exactly that, to catch a topic mistakenly claiming another change's exit as
its own.>
```

## Idea notes (pre-document, non-documented)

- The `demote` verb is gaining CONTENT semantics with this topic: today
  demote reads mostly as a state-machine transition (proposal folder moves
  back to staging, `Status:` flips). Once the proposal-element sections must
  be REFRESHED to the actual last-attempted values on demote, `demote` also
  becomes a content-writing operation — the assumption that it is a
  mechanical move (move files, flip one header field) may not survive first
  contact with a change whose `proposal.md` drifted far from its staging
  draft before it was demoted. — Added-by: Brett Heap (direction) / Claude
  Opus 4.8 (drafting) · 2026-08-15
- The outline buffer in doxBench is already editable inside branch sessions
  (per the ratified branch-session/workbench model this workspace runs on)
  — so "sections addable by AI" is not really a NEW capability to build; it
  is mostly a content and affordance concern (a documented convention for
  where a section goes and what provenance line it needs, maybe a UI button
  that inserts a stub) rather than new plumbing. — Added-by: Brett Heap
  (direction) / Claude Opus 4.8 (drafting) · 2026-08-15
- Meta-note: this topic should become the FIRST template conformer, paired
  with `substantive-review-lane-questions` (the freshest staged topic as of
  this writing) — both are small and live, and would make a legible first
  pair of "does the template actually fit a real topic" test cases before
  any migration decision gets made for the other 30+ staged topics. —
  Added-by: Brett Heap (direction) / Claude Opus 4.8 (drafting) · 2026-08-15

## Conflicts

- The existing 30+ staged topics under `ideation/staging/` do NOT conform to
  this template — no Idea-notes/Conflicts sections, no structured
  open-question sub-fields, no Last-proposal-attempt slot. Some form of
  migration or explicit grandfathering is needed, or every doc-health run
  against the corpus starts from a nonconforming baseline the day this
  ratifies (see Open question 2). — Added-by: Claude Opus 4.8 (drafting) ·
  2026-08-15
- doc-health's fifteen check families are template-UNAWARE today:
  tag-hygiene checks marker grammar wherever `xspec:` appears in ANY
  document, but no family checks whether a staged topic carries the
  required sections at all. If this template ratifies, doc-health likely
  needs a new check (or an extension of an existing family) to report
  non-conforming staged topics — a delta this topic does not itself scope.
  — Added-by: Claude Opus 4.8 (drafting) · 2026-08-15
- `ideation/staging/INDEX.md`'s per-topic detail section duplicates several
  fields the template now ALSO carries in the primary fragment's own header
  (Staging ID, Files, Target capabilities, Source). Two sources of truth for
  the same facts is exactly the shape of drift doc-health's own families
  exist to catch elsewhere in this repo; this topic does not resolve
  whether INDEX.md should shrink to a pointer-only row once the primary
  fragment is templated. — Added-by: Claude Opus 4.8 (drafting) · 2026-08-15

## Open questions

### Q1. Does the primary fragment itself become the outline, or does a separate `outline.md` earn a dedicated file?

Context: `primaryFragmentPath()` already deterministically selects the file
named `<staging_id>.md` first, falling back to the shallowest markdown file
in the topic folder. A dedicated `outline.md` would need either a selector
change (teach the wheel a second, higher-priority filename) or a rename so
`outline.md` itself became the exact-match target — which would break the
`<staging_id>.md` naming convention every other topic in the corpus uses.
Recommended answer: keep the primary fragment AS the outline; no new file,
no selector change.
Explanation: the wheel's one-path rule — exactly one deterministically
selected file per topic, chosen path-only, "never content-sniffed" per the
function's own documentation — is a load-bearing simplicity property.
Introducing a second candidate file re-opens precisely the ambiguity that
rule was built to avoid, in exchange for a separation (outline vs.
everything else) the template's own "other files stay free-form" claim
already delivers without touching the selector at all.
Disposition status: leaning (carried as the RECOMMENDED shape in Claim 2;
not yet ratified)
Added-by: Brett Heap (direction) / Claude Opus 4.8 (drafting) · 2026-08-15

### Q2. How do the 30+ existing staged topics migrate to this template?

Context: every topic staged before this one predates the template and
carries none of its required sections. A hard migration (rewriting all of
them at once) would touch topics that are near-complete, blocked on an
external gate, or dormant by design for reasons that have nothing to do
with this template.
Recommended answer: opt-in conformance for existing topics — rewritten only
when a topic is next actively touched — with REQUIRED conformance for any
topic staged after this one ratifies; doc-health treats non-conformance as
a nudge, never a gate-blocking finding.
Explanation: this matches how every other retroactive staging convention in
this repo has landed — the draft-proposal `openspec/` workspace convention
(adopted 2026-07-13) was never back-applied to topics staged before it
either. Forcing a mechanical rewrite of 30+ documents, several of which are
COMPLETE-and-archival or blocked on an unrelated external gate, produces
busywork without advancing any live decision, while a WARNING-tier doc-health
finding keeps the incentive to convert visible without stalling unrelated
work.
Disposition status: open
Added-by: Brett Heap (direction) / Claude Opus 4.8 (drafting) · 2026-08-15

### Q3. Does this template become a `document-lifecycle` spec delta, or
stay a staging convention?

Context: the template could stay a pure convention documented in
`docs/document-lifecycle.md` prose (the same status the draft-proposal
`openspec/` workspace convention currently holds), or become a formal
MODIFIED requirement with a scenario, strict-validated at the proposal gate.
The round-trip-on-demote guarantee — "nothing learned in a failed push is
lost" — only has teeth if something actually checks it.
Recommended answer: a spec delta.
Explanation: a convention with no validator is exactly the shape of drift
doc-health's fifteen families exist to catch elsewhere (frozen-identifier
drift, marker malformation, register-lifecycle inconsistency); the
round-trip guarantee is a testable property — does a demoted fragment's
Last-proposal-attempt slot actually carry the prior change's real text — and
a testable property belongs in a spec requirement with a scenario, not in
prose nobody re-checks.
Disposition status: open
Added-by: Brett Heap (direction) / Claude Opus 4.8 (drafting) · 2026-08-15

### Q4. Which intent verb authorizes an AI patching one template section?

Context: the template's extensibility claim (either a human or an AI may
add a section, with provenance) needs an authorized WRITE path, not just a
convention an agent might or might not follow. The workbench/doxBench
branch-session model already exposes an `edit-apply` intent verb for
content changes on a session branch.
Recommended answer: `edit-apply` covers it — an AI adding or patching a
template section is an ordinary content edit on the topic's branch session,
scoped by the section it targets (its heading, or its `xspec:candidate`
fence when the section is a proposal-element block) as the patch's
addressing key.
Explanation: a separate intent verb for "add a template section" would
duplicate machinery `edit-apply` already provides (branch-scoped, committed,
reviewable) to express a distinction — this edit happens to be scoped to
one named section — that is a patch-TARGETING detail, not a different KIND
of action. The marker grammar supplies the addressing precision without a
new verb.
Disposition status: open
Added-by: Brett Heap (direction) / Claude Opus 4.8 (drafting) · 2026-08-15

### Q5. Should the wheel's 3-line summary extraction read the template's `Summary:` section explicitly, rather than falling through its current heuristic?

Context: `fragmentSummary()` today extracts the controlled header block's
`Summary:` field when present, falling back to the first meaningful
paragraph — a heuristic chain that predates any guarantee a primary
fragment carries a template-shaped `Summary:` field at all.
Recommended answer: yes — once this template ratifies (every conforming
primary fragment guaranteed to carry a `Summary:` header field), the wheel
should read that field as the templated Summary directly, for conforming
topics, rather than always running the full fallback chain.
Explanation: the fallback (header Summary, else first paragraph) exists
precisely because nothing today guarantees a topic carries a proper Summary
field; once the template makes that guarantee for conforming topics, the
fallback becomes unnecessary defensive code for a case the template has
already closed. Non-conforming topics (Q2's opt-in remainder) still need
the fallback, so this is additive to `fragmentSummary()`, never a removal.
Disposition status: open (gated on Q2's migration ruling and this topic's
own ratification)
Added-by: Brett Heap (direction) / Claude Opus 4.8 (drafting) · 2026-08-15

## Exit

Iterate this fragment in doxBench — itself editable inside a branch session
per the model Q4 leans on — until all five open questions above carry a
disposition other than `open`. The likely landing is a single OpenSpec
change (something like `add-staged-topic-outline-template`, named for real
only when actually raised) carrying a `document-lifecycle` delta for the
template contract and an `ideation-dashboard` delta for the outline tab's
rendering and its add-section affordance.
