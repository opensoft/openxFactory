---
code_surface: openxFactory (`scripts/doc_health/families.py` — `fam_ratified_provenance` learns the second, record-citing citation spelling and gains the three-way floor check on it, and its `_header_line` read widens from one prefix to two WITHOUT becoming a prefix match on the bare word "Ratified", which would swallow body prose; `tests/doc-health/` — positive and negative cases for both spellings, for the floor, and for the body-prose boundary, mutation-validated. `docs/document-lifecycle.md` § Status Claim Rules is prose rather than runtime code, but it is the text the family implements and it lands in the same slice.)
target_release: implemented — the openxFactory main line. This surface cuts NO contract bundle: no schema under `contracts/schemas/` changes, no digest set moves, and no release tag is owed. The archive gate is therefore merge-plus-green on main, full stop — `python3 -m pytest tests/doc-health` and `-k workbench` green, `OPENSPEC_TELEMETRY=0 openspec validate --all --strict` green, and a doc-health run whose severity counts are unchanged against the pre-change baseline. The bare `implementation_pending` token is deliberately NOT used: `docs/archive-record-discrepancies.md` C1 records that it is a house token the realization axis does not define, and Brett's 2026-08-22 ruling rewrote four archived proposals off it; its legality on the ACTIVE phase was left open by that ruling and this change does not presume an answer.
Status: draft
Proposed: 2026-08-22
---

# Proposal: sanction-ratified-record-spelling

## Why

**The rule names one spelling. The corpus writes two, and the second is the one recent sessions were told to write.**

`docs/document-lifecycle.md` § Status Claim Rules sanctions exactly one
ratification citation:

> A `ratified` header names the approving OpenSpec change
> (`Ratified by: <change>`).

In practice a second spelling has grown up beside it — a bare `Ratified:`
line that cites a RECORD rather than a change, used precisely where no
approving OpenSpec change exists to name: an in-session ruling, a
disposition, an `.openspec.yaml` approval pair, an archive commit.

**Measured in this tree at `ca0b905`, not inherited from the review that
raised the flag.** Every number below was re-derived here.

*Under the governed roots doc-health actually reads*
(`contracts/`, `docs/`, `examples/`, `ideation/`, `templates/` — the roots
`doc_health.corpus` builds `ctx.docs` from):

- **29 documents carry a `Ratified by:` line.** All 29 name a resolvable
  OpenSpec change id, so `fam_ratified_provenance` fires on none of them.
- **22 of those 29** carry `Status: ratified` inside the 15-line header
  window and are the population the family checks. The other seven are not
  checked at all: four carry `Status: draft` (one of those four also places
  its citation past the window) and three carry `Status: record`.
- **13 of the 29 name ONLY the change id** — no approver, no date, no
  record path. They are correct as written, and any rule that demanded
  more of them would convert 13 sound documents into findings overnight.
- **Zero governed documents carry a `Ratified:` header.** One governed
  document carries the literal string in BODY prose —
  `docs/domain-ontology-semantic-decisions.md:201`, a section-level
  decision label ("Ratified: YAML-serialized JSON-Schema contracts
  under…"), 186 lines below the header window and read by nothing.

*Under `openspec/`, which is NOT a governed root today:*

- **86 archived proposals; 42 carry `Status: ratified` in the header
  window.** Of those, **29 cite with `Ratified by:`** and **13 cite with
  `Ratified:`** (12 inside the header window; one, at
  `2026-08-22-add-roster-device-admission-surface`, at line 42, pushed out
  by very long front matter). **One — `2026-08-22-add-doxbench-editing-phase-b`
  — carries `Status: ratified` and NO ratification citation anywhere in
  the file.**
- **11 active proposals** carry `Status: ratified`: 9 `Ratified by:`,
  2 `Ratified:`.
- Across all 38 `Ratified by:` lines in `openspec/changes/` (29 archived +
  9 active), **only 20 name a resolvable change id.** The other 18 name
  Brett or "user approval", a date, and usually a verbatim instruction
  ("Brett's direction on 2026-07-30 (\"lets do F18 term-lifecycle
  enforcement\")"). The primary spelling is therefore ALREADY being used
  free-form for record citation in half the proposal corpus — the
  divergence is not only that a second spelling exists, but that the rule's
  literal reading ("names the approving OpenSpec change") describes a
  minority of the lines written under its own spelling.
- All 15 `Ratified:` lines in `openspec/changes/` name a date; all 15 name
  an approver, a record, or both. **Not one of the 53 citation lines in
  `openspec/changes/` fails a three-way approver-or-date-or-record test.**
  The convention the corpus settled into is already the rule this change
  proposes to write down.

**The tooling trap is latent, not live.** `fam_ratified_provenance`
(`scripts/doc_health/families.py`) reads exactly one prefix —
`_header_line(doc, "Ratified by:")` — and `_header_line` matches with
`body.startswith(prefix)`. A `Ratified:` line therefore returns `None`, and
the family emits a CRITICAL `ratified-provenance` finding, "Ratified by:
missing or does not resolve to an OpenSpec change". Nothing fires today for
one reason only: the 15 `Ratified:` lines all live under `openspec/`, which
`GOVERNED_ROOTS` excludes. Two ordinary events make them live — `openspec/`
entering the governed roots, or one `Ratified:` header appearing in
`docs/` — and either would report as CRITICAL a line that a session wrote
deliberately, on instruction, because the alternative was to invent a
change id.

**This is the flag the 2026-08-22 adversarial review recorded, and the
divergence Brett's own ruling widened.** `docs/archive-record-discrepancies.md`
B1 counts both spellings and argues the choice between them at length,
concluding that Phase A's ratification "is neither an approving OpenSpec
change (none exists) nor a quotable in-session utterance"; C7 makes the same
argument again and keeps `Ratified:` "for the reason this entry already
established and the ruling did not change: there is still no approving
OpenSpec change to name". The C2 ruling then made the two-spelling practice
an INSTRUCTION — as the register renders Brett's adopted option, backfill
"a citation line in whichever existing spelling honestly fits". A promoted
rule that names one spelling while the ratifier's own ruling directs authors
to choose between two is the gap this change closes.

## What Changes

**One design intent, stated once and then encoded in two places.**

`Ratified by: <change>` stays the PRIMARY spelling and is required wherever
an approving OpenSpec change exists to name. `Ratified:` is sanctioned as
the RECORD-CITING alternative, legal ONLY where no approving change exists,
and it must name at least one of an approver, a date, or a resolvable record
path. Both spellings remain subject to the existing rule that a bare,
uncited `Status: ratified` is illegal.

1. **`document-lifecycle` — MODIFIED `Controlled document status taxonomy`.**
   The ratification-citation rule is promoted for the FIRST time. It lives
   today only in `docs/document-lifecycle.md` prose: the promoted
   requirement carries scenarios for the standard claim, the generated
   record, and the succession pointer — three of § Status Claim Rules'
   four bullets — and none for the ratified citation. The delta restates
   the requirement in full with the citation rule, the two-spelling
   condition of use, and the three-way floor folded in; all three existing
   scenarios are restated unchanged, and four are added (an approving
   change exists; no approving change exists; a record-citing line names
   nothing checkable; a ratified header carries no citation at all).

2. **`doc-health` — MODIFIED `Deterministic check families`.** The
   `Lifecycle conformance checks fire` scenario enumerates the lifecycle
   violations the run reports, and its list names only "a dangling
   `Ratified by:` reference". Widening the family adds two violation kinds
   the enumeration does not carry: a `ratified` header with no citation in
   either spelling, and a `Ratified:` line failing the floor. The delta
   restates the requirement body and all eight scenarios verbatim and
   changes exactly that one bullet. Without it the realization in §3 would
   emit findings the promoted contract does not authorize. Whether this
   second delta belongs in this change or in a follow-up is Open Question 1.

3. **Realization — `docs/document-lifecycle.md` § Status Claim Rules.** The
   one-line bullet becomes the two-spelling rule plus the floor, matching
   the promoted text.

4. **Realization — `fam_ratified_provenance`.** It learns to read either
   prefix, applies the existing change-id / link-target resolution to the
   `Ratified by:` form unchanged, and applies the three-way floor to the
   `Ratified:` form. Two boundaries are load-bearing and are pinned by
   tests: the reader MUST NOT become `startswith("Ratified")`, which would
   match body prose such as `add-openxwallet`'s "Ratified together with…"
   line and the section label at
   `docs/domain-ontology-semantic-decisions.md:201`; and the floor MUST NOT
   be applied to `Ratified by:`, which would turn 13 sound governed
   documents into CRITICAL findings in one commit.

**Deliberately NOT in scope.** Whether `openspec/` joins `GOVERNED_ROOTS`
(that is the event that makes the 15 latent lines live, and it is a separate
decision with a much larger blast radius); the missing citation on
`add-doxbench-editing-phase-b` and the out-of-window one on
`add-roster-device-admission-surface` (archived-record edits, which the
register's discipline routes through a citing change and a ruling, not
through this proposal); and any rewrite of existing citation lines. **No
existing line in the corpus is edited by this change.** The rule is written
to fit what the corpus already does.

## Impact

- **Governed corpus:** no document is edited except
  `docs/document-lifecycle.md` itself. Measured: 0 of the 29 governed
  `Ratified by:` documents change classification under the widened rule,
  because the floor does not reach them.
- **Findings:** the realization must be baseline-identical on severity
  counts. If it is not, the widening is wrong, not the corpus.
- **Promoted specs:** `document-lifecycle` keeps its 13 requirements and
  gains 4 scenarios on an existing one (52 → 56); `doc-health` gains no
  requirement and no scenario, only one widened WHEN bullet.
- **Downstream readers:** none. `ideation_dashboard.generator` derives a
  change's ratifier from `.openspec.yaml` `ratified_by`/`ratifier`,
  "deliberately NOT the `Ratified by:` proposal header"
  (`docs/archive-record-discrepancies.md`, "What the tooling does and does
  not enforce here"), so no projection moves.

## Open Questions

Each carries a recommended answer, per the repo's own standard for an
undecided question.

**OQ-1 — Does the `doc-health` delta belong in this change?**
*Context:* the promoted `Lifecycle conformance checks fire` scenario
enumerates violation kinds, and the §3 realization adds two. *Recommended:*
YES, keep it here — a change that widens a check while leaving the
enforcement contract naming only the old spelling ships a known
inconsistency, and the delta is one bullet inside an otherwise verbatim
restatement. *Alternative:* read the enumeration as illustrative and let the
widening ride under "a dangling `Ratified by:` reference" as a shorthand for
"a ratification citation that does not resolve", deferring the doc-health
text.

**OQ-2 — Is `Ratified:` the right spelling to sanction, or should the
corpus converge on one?**
*Context:* a third option exists — keep ONE spelling, `Ratified by:`, and
redefine what may follow it (a change, a record, or an approver plus date),
then rewrite the 15 `Ratified:` lines. *Recommended:* sanction both, as
proposed. The two spellings carry a real distinction the corpus discovered
rather than invented — "an approving change exists" versus "it does not" —
and the convergence option would rewrite 13 archived records, which the
register's own discipline treats as a contested act requiring a ruling per
record. *Alternative:* converge, and pay that cost once.

**OQ-3 — Should the floor require MORE than one of the three?**
*Context:* every one of the 15 live `Ratified:` lines names a date, and 14
name an approver too; a "date AND one other" floor would pass all 15 today.
*Recommended:* keep the three-way floor at one. A stricter floor buys
nothing on the current corpus and would, on the next honest citation that
carries only a record pointer, force the invention of a date — the exact
failure the register refused twice (C2's "no invented provenance anywhere",
C7's "nothing was inferred"). *Alternative:* require a date unconditionally.

**OQ-4 — Should a `ratified` document be allowed to carry BOTH lines?**
*Context:* the delta says exactly one citation, no document carries both
today, and a change that ratifies a document already ratified by a ruling is
imaginable. *Recommended:* exactly one, as proposed — two lines each
claiming to name the ratification say nothing about which is current, which
is the identical defect the promoted "records its authorship once per
document, not once per attempt" requirement already rules on for a
neighbouring header. *Alternative:* permit both and define precedence.

**OQ-5 — Severity of a floor violation.**
*Context:* `fam_ratified_provenance` emits CRITICAL today. A `Ratified:`
line naming nothing checkable is a weaker defect than a dangling change
reference — it is under-specified rather than false. *Recommended:*
CRITICAL, same tier, because the header's claim is unbacked either way and
a second tier for the same rule invites arguing the tier instead of fixing
the line. *Alternative:* ERROR for the floor, CRITICAL reserved for a
dangling reference.
