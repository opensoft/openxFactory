# Proposal Ratification: scope-pinned-arm-root-naming

Status: ratified
Kind: report
Decision date: 2026-09-16
Ratifier: Brett Heap (openxFactory repository owner)
Ratified: 2026-09-16T13:43:18Z by Brett Heap (openxFactory repository
owner), first-hand, in session to lane `openxfactory-2` (display
`openXfactory-2`, session c0d09b6d) — A TYPED SENTENCE, NOT A SELECTION,
verbatim: "ratify 1052 when green, then 1050". THE ONE CITATION: openxFactory
issue #1047, comment
https://github.com/opensoft/openxFactory/issues/1047#issuecomment-5698480379.

## Decision

**RATIFIED — AS FILED, at the head the word met (`92d3e0e2`)**, by Brett Heap.

## The word, and what it ratifies

Brett Heap's instruction was ONE TYPED SENTENCE, not a selection over a
multiple choice — first-hand, in session to lane `openxfactory-2` (display
`openXfactory-2`, session c0d09b6d), 2026-09-16T13:43:18Z:

> **"ratify 1052 when green, then 1050"**

— posted as openxFactory issue #1047 comment
[5698480379](https://github.com/opensoft/openxFactory/issues/1047#issuecomment-5698480379),
which is THE ONE CITATION for this record. The comment's own gloss on the
word, posted in the same breath by the same authority, is what fixes its
scope: it ratifies `scope-pinned-arm-root-naming` (PR #1052) "as its packet
stands at the head the word met, every review round folded, on the
ratification order the word gives (#1052 first, then #1050)". `#1050` names
a separate pull request and packet; it is recorded here only because the
word names it, and it is ratified by no part of this packet's own origin
declaration.

**THE HEAD THE WORD WAS GIVEN OVER.** PR #1052, commit
`92d3e0e2a5a3fddacf02f460277c2b90eb846421` ("Fix round 4: narrow the Status:
-draft claim; drop host-absolute /tmp paths"), with every required check
reporting SUCCESS at that head — the "when green" the word conditions on. No text this packet carries at that head is excepted from the
ratification: `proposal.md`'s account of the two pre-root-selection findings
and why the sentence must be scoped rather than deleted or the arm widened,
`design.md`'s D-1/D-2/D-3, and the one `## MODIFIED` spec delta against
`document-lifecycle` *Prose tagging marker hygiene*.

**AMENDED SINCE — PRE-LANDING CONFORMING CORRECTIONS UNDER THE SAME WORD.**
The baseline stated above is the baseline AS RATIFIED at `92d3e0e2` and is
left exactly as measured; it is not a description of the branch tip. This
differs from a landed ratification amended by its ratifier after the merge:
no merge of this packet exists yet, and the word itself — "ratify 1052 WHEN
GREEN, then 1050" — conditions on green and leaves the lane to land the
corrected head, not the `92d3e0e2` head the word was first given over. FOUR
commits have moved packet text since: see "Addendum, 2026-09-16" at the
foot of this record. **ALL FOUR LEAVE NO LASTING NORMATIVE CHANGE — they are
not all non-normative.** ONE OF THEM, FIX ROUND 5, WAS THE TEMPORARY
NORMATIVE EDIT: it applied a narrower reading of a ratified scenario's WHEN;
that was WRONG (ratified normative text is the ratifier's act to amend, not
the lane's) and fix round 6 REVERTED IT IN FULL, so at the close of round 6
the block carried its normative content BYTE-IDENTICAL to what was ratified
at `92d3e0e2`. The other three moved no normative text at any point. No
decision, scope or `tasks.md` § 1 box is reopened by any of the four. The
gap round 5 surfaced is real and is put to Brett Heap directly, by a RULING
NEEDED comment on openxFactory #1047 posted 2026-09-16.

**AMENDED SINCE — ONCE MORE, AND THIS TIME BY THE RATIFIER HIMSELF, ON
2026-09-17. See § "Addendum, 2026-09-17 — THE RATIFIER'S AMENDMENT OF THE
NO-RECORD SCENARIO'S WHEN" at the foot of this record.** The RULING NEEDED
the paragraph above describes was ANSWERED: Brett Heap ruled *"Apply the
narrowing"* on 2026-09-17, and the sibling scenario *A pinned target names a
pin no resolution root carries*'s WHEN moved from the text ratified at
`92d3e0e2` to the narrower text fix round 5 had measured — this time as the
ratifier's own act, with the contradiction before him, which is the only
authority under which ratified normative text moves. **THAT SUPERSEDES THE
PRECEDING PARAGRAPH'S FORWARD CLAIM** that the block lands with its normative
content byte-identical to `92d3e0e2`: true of every state this packet held up
to 2026-09-17, and no longer true of the text promoted at the archive. The
preceding paragraph and the 2026-09-16 addendum are left EXACTLY as written,
as the evidence of what was true before the word came.

## What is ratified

The proposal as written at `92d3e0e2a5a3fddacf02f460277c2b90eb846421`,
`proposal.md` § *The decision, put for a veto* (OQ-1), option (a) —
RECOMMENDED, AND WHAT THE DELTA ENCODES — AS FILED, with no tightening and no
alternative taken:

- **D-1 — THE READING, AS FILED.** The root-naming obligation is scoped to
  findings that reach root selection; the two findings emitted before it —
  the lexically malformed pinned value, and the document whose repository has
  no resolution root in the run — name what they judged instead of a root.
  One clause of the sibling scenario *A pinned target names a pin no
  resolution root carries*'s WHEN is narrowed to exclude the empty-root-set
  case, and one scenario is added.
- **D-2 — WIDEN THE ARM INSTEAD.** NOT TAKEN, exactly as filed.
- **D-3 — DELETE THE SENTENCE.** NOT TAKEN, exactly as filed.

**BOX TICKED BY THIS RATIFICATION: 1.1 — AND NO OTHER.** `tasks.md` § 2's
seven filing boxes stand exactly as the filing pull request left them; § 3
stays entirely open — it is a separate act on a separate word.

## What this ratification does NOT do

- **NO REALIZATION BEYOND WHAT THE FILING ALREADY MEASURED.** `code_surface:
  none` — no byte of `scripts/doc_health/families.py` moves by this act; the
  realized arm already matched the clarified reading before this word was
  given, which is the filing's own measurement (`proposal.md`, `design.md`
  § Measurement) and not a claim this ratification adds.
- **NO ARCHIVE.** Under `release-realization`, `code_surface: none` archives
  ON LANDING plus `tasks.md` § 3's own task list — a separate act on a
  separate word, not this ratifying commit. `tasks.md` § 3 stays entirely
  open and openxFactory #1047 stays OPEN, closing only at the archive.
- **NO RULING ON `#1050`.** The word's ordering clause ("then 1050") is
  recorded above because the word names it; it approves no text of that
  separate packet, and that packet's own ratification is its own record.
- **NO MERGE.** This record ratifies text at one head. Landing PR #1052 is a
  separate act under this repository's Rule 6 landing-window protocol,
  because this change touches `openspec/changes/`.

## Records

- Governing issue, and the finding this packet answers: openxFactory
  [#1047](https://github.com/opensoft/openxFactory/issues/1047) — THE ONE
  CITATION for this ratification is its comment
  [5698480379](https://github.com/opensoft/openxFactory/issues/1047#issuecomment-5698480379),
  2026-09-16T13:43:18Z.
- The packet this ratifies: openxFactory pull request
  [#1052](https://github.com/opensoft/openxFactory/pull/1052), at
  `92d3e0e2a5a3fddacf02f460277c2b90eb846421`.
- The cause: `openspec/changes/archive/2026-09-15-extend-prose-tagging-target-to-pinned-capabilities/`
  — its design D-2 root paragraph wrote the sentence this packet scopes, and
  its archive pull request [#1042](https://github.com/opensoft/openxFactory/pull/1042)
  is where the defect was surfaced and ruled STANDS, naming this packet as
  the successor.

## Addendum, 2026-09-16 — pre-landing conforming corrections under the same word

**WHY AN ADDENDUM AND NOT A SILENT REWRITE OF THE RECORD ABOVE.** The body of
this record freezes the ratification at `92d3e0e2` and states that no text
this packet carries at that head is excepted. Four commits have moved packet
text since that head. Rewriting the freeze paragraph to chase them would
destroy the evidence of what the word was actually given over; recording the
movement here instead keeps both facts visible.

**THIS DIFFERS FROM A LANDED RATIFICATION LATER AMENDED BY ITS RATIFIER**
(compare `add-requirement-ref-resolution-integrity`'s
`review/ratification-2026-09-01.md`, whose own "Addendum, 2026-09-01" records
a POST-MERGE scope amendment the ratifying owner RULED ON DIRECTLY, IN
SESSION, WITH THE CONTRADICTION BEFORE HIM, before any text moved). No merge
of this packet exists yet. The word — "ratify 1052 WHEN GREEN, then 1050" —
is conditioned on green and instructs the lane to land the corrected head;
these are the corrections made getting that head to green, under the same
word, before any landing.

**THE FOUR COMMITS, AND WHAT EACH MOVED.**

1. `db03f283` — pinned `design.md`'s reproduction-command placeholder
   `--as-of <today>` to the literal date it was actually run with,
   `2026-09-16` (Copilot at `376313b9`, RULED ACCEPT by the lane): the
   committed command was uncopyable, since `runner.py` passes `--as-of`
   straight to `date.fromisoformat`. NON-NORMATIVE — no decision, no scope,
   no `tasks.md` § 1 box moved.
2. `2a613e88` — added the sanctioned `Ratified by:` header line to
   `design.md` and `tasks.md`, directly after `Status: ratified` in each
   (Copilot at `db03f283`, RULED ACCEPT by the lane): `Status: ratified`
   carried no header-line citation the lifecycle citation parser reads, only
   lower prose. NON-NORMATIVE — no decision, no scope, no `tasks.md` § 1 box
   moved.
3. `7055e475` (fix round 5; Copilot at `2a613e88`, three findings, all RULED
   ACCEPT by the lane) — TWO corrections, ONE of them WRONG:
   - **Kept — mechanical: refreshed a stale source-citation pointer.** The
     restated body sentence cited `scripts/doc_health/families.py:1317-1321`
     for where capability resolution reads the root precedence. THAT
     POINTER IS STALE IN CANON ITSELF — `:1317-1321` is `_topic_outcome` on
     `main` today; the logic now lives in `_resolve_capability` (~:1490) and
     `_pin_roots` (~:1548). Corrected to name the two functions directly, no
     line numbers to drift again. NON-NORMATIVE — no SHALL, obligation,
     scenario or precedence claim moves; see `proposal.md`'s "CORRECTED"
     bullet under § What Changes. KEPT by this commit.
   - **Reverted — the lane narrowed ratified normative scenario text on its
     own authority, which it does not have.** Fix round 5 narrowed the
     sibling scenario *A pinned target names a pin no resolution root
     carries*'s WHEN from its ratified text ("…and at least one resolution
     root was selected for the run") to "…and at least one selected root
     whose boundary was successfully searched", on a real finding: a root
     whose `contracts/` directory fails `boundary_dir` is never added to
     `_pinned_arm`'s `searched` list, so where EVERY returned root fails
     that check the function's trailing `if searched:` guard never fires
     and no aggregate "unresolved pinned target: no record under root(s)"
     finding is emitted — the ratified WHEN describes a finding the
     implementation does not emit on that one path. **THE FINDING STANDS;
     THE FIX WAS THE WRONG ACTOR'S.** Ratified normative text is the
     ratifier's to amend, not the lane's — precisely the shape
     `add-requirement-ref-resolution-integrity`'s 2026-09-01 amendment
     observed: that packet's ratifier RULED on the contradiction, IN
     SESSION, BEFORE its scenario text changed, and only then did the text
     move. Fix round 5 moved the text FIRST and framed asking Brett Heap
     as a follow-up "veto" — backwards, and REVERTED here in full.
4. **This commit (fix round 6; Copilot review thread `PRRT_kwDOTAvnrs6jB5Uc`
   on `7055e475`, RULED by the lane) — reverts item 3's WHEN narrowing and
   re-measures:**
   - The WHEN of *A pinned target names a pin no resolution root carries* is
     restored to its text AS RATIFIED at `92d3e0e2`
     (`git show 92d3e0e2:openspec/changes/scope-pinned-arm-root-naming/specs/document-lifecycle/spec.md`),
     BYTE-IDENTICAL. Every paraphrase of it in `proposal.md` and `design.md`
     that fix round 5 changed is restored to describe that ratified text and
     no more.
   - The pointer refresh (item 3, first bullet) is KEPT, as is the `Ratified
     by:` header convention (`2a613e88`) and the `--as-of` pin (`db03f283`).
   - The committed block is RE-MEASURED after the revert: `derive_units`
     reads canon 209 units, block 215, **THREE uncarried units** — the
     root-naming sentence, the pointer-bearing sentence (kept from round 5),
     and the sibling scenario's WHEN bullet (its wording as ratified; this
     bullet has been uncarried against canon since round 1 regardless of
     which wording it holds, canon carrying no such clause at all) — and
     NINE new units. The canon-diff is FOUR hunks, 21 added / 8 removed,
     UNCHANGED from round 5's own figures — a `git diff --numstat`
     line-count property, the WHEN clause being one physical line under
     either wording. README, `tasks.md` § 2.2 and the self-gate's own
     narrative (`tests/doc-health/test_modified_block_currency_self_gate.py`)
     are updated to match.
   - **THE RULING NEEDED comment on openxFactory #1047, posted 2026-09-16,**
     asks Brett Heap directly for the word this text needs: whether to
     ratify the round-5 narrowing (or an equivalent), leave the WHEN exactly
     as ratified, or something else. Until that word comes, the block lands
     with its normative content EXACTLY as ratified at `92d3e0e2`.
     **THE WORD CAME ON 2026-09-17 — *"Apply the narrowing"* — so the block
     does NOT land with that content: see § Addendum, 2026-09-17 at the foot
     of this record. This bullet is left as written, as the record of what
     round 6 decided with the question still open.**

**WHAT DID NOT MOVE, ACROSS ALL FOUR COMMITS.** No `tasks.md` § 1 box (still
1.1, and only 1.1). No OQ-1 disposition — option (a) stands exactly as
ratified, D-2 and D-3 remain refused. No `.openspec.yaml` origin field. No
README ratified-bullet claim. The `code_surface: none` /
`target_release: implemented` declaration. The scenario count (still
twenty-four, one added over canon's twenty-three) and every scenario title.
And, after item 4's revert, every normative SHALL, WHEN, THEN and AND bullet
of the block — the block's normative content is EXACTLY what `92d3e0e2` was
ratified with, the citation refresh being the one non-normative exception.

**GATES AT EACH COMMIT ABOVE**, recorded in that commit rather than
pre-asserted here: `OPENSPEC_TELEMETRY=0 openspec validate
scope-pinned-arm-root-naming --strict` and `--all --strict` (the two
pre-existing `origin/main` failures, `add-chain-attestation` and
`add-composed-view-authoring`, and no other); `python3
scripts/proposal-support.py . verify`; `pytest -q tests/proposal-support
tests/doc-health/test_modified_block_currency_self_gate.py`; and a same-clock
`doc-health.py --single-repo . --family ratified-provenance` comparison
against an `origin/main` baseline showing the SAME pre-existing findings and
none naming this packet.

## Addendum, 2026-09-17 — THE RATIFIER'S AMENDMENT OF THE NO-RECORD SCENARIO'S WHEN

**A SECOND ACT OF THE SAME RATIFIER, ON THE ONE QUESTION THE FIRST LEFT OPEN.**
Recorded as an addendum rather than folded into the body or into the
2026-09-16 addendum above, because a record that quietly rewrites itself to
match a later ruling destroys the evidence that the ruling was needed. This is
the shape `add-requirement-ref-resolution-integrity`'s own
`review/ratification-2026-09-01.md` § "Addendum, 2026-09-01" set, and the shape
fix round 5 got backwards: **the ratifier rules first, with the contradiction
before him, and only then does the text move.**

**THE WORD.** Brett Heap (openxFactory repository owner), first-hand, in
session to lane `openxfactory-2` (display `openXfactory-2`, session c0d09b6d),
2026-09-17 — an INTERACTIVE MULTIPLE-CHOICE SELECTION over the RULING NEEDED
this record's 2026-09-16 addendum posted, verbatim:

> **"Apply the narrowing"**

**THE ONE CITATION:** openxFactory issue #1047, comment
[5714432684](https://github.com/opensoft/openxFactory/issues/1047#issuecomment-5714432684).

**WHAT WAS PUT, AND WITH WHAT IN FRONT OF HIM.** The RULING NEEDED comment of
2026-09-16 carried the contradiction whole, measured rather than argued:

- The scenario *A pinned target names a pin no resolution root carries*, AS
  RATIFIED at `92d3e0e2`, fires on a WHEN satisfied by ROOT SELECTION ALONE —
  "…and at least one resolution root was selected for the run".
- `_pinned_arm` (`scripts/doc_health/families.py`) appends a root to
  `searched` only AFTER that root's `contracts/` directory clears
  `boundary_dir` (`:1604-1613`); a root whose boundary check fails draws its
  OWN finding instead (*A root's contracts directory is itself a symlink*) and
  never reaches `searched`.
- So where EVERY root `_pin_roots` returns fails that boundary check,
  `searched` stays empty, the trailing `if searched:` guard (`:1633`) never
  fires, and NO "unresolved pinned target: no record under root(s)" finding is
  emitted at all — the as-ratified WHEN describes, on that one path, a hygiene
  finding the realized arm does not emit.
- The packet already carried `Status: ratified`, so narrowing the WHEN was an
  amendment to ratified text and **only the ratifying owner could consent to
  one** — which is why fix round 6 reverted the lane's own narrowing and
  posted the question instead of answering it.
- The choices put were: ratify the round-5 narrowing (or an equivalent), leave
  the WHEN exactly as ratified, or something else.

**WHAT MOVED — ONE BULLET, AND ONLY ITS WHEN.** In
`specs/document-lifecycle/spec.md`, the scenario *A pinned target names a pin
no resolution root carries*:

**BEFORE** — as ratified at `92d3e0e2`, the bullet's tail read:

> …and no pin record for `<pin-id>` exists under any root of the run's
> precedence, **and at least one resolution root was selected for the run**

**AFTER** — as amended 2026-09-17, and as promoted at the archive, it reads:

> …and no pin record for `<pin-id>` exists under any root of the run's
> precedence, **and at least one selected root whose boundary was successfully
> searched**

It is byte-for-byte the text fix round 5 applied at `7055e475` and fix round 6
reverted at `d138a99d` — now applied under the authority that was missing then.

**WHY.** The amended WHEN excludes the all-roots-boundary-refused case, so the
scenario's subject is exactly what the arm emits: a `<pin-id>` absent from
every root the run ACTUALLY SEARCHED. The excluded case is not left uncovered —
the independent scenario *A root's contracts directory is itself a symlink*
already requires the per-root boundary finding for each refused root. Canon
therefore stops requiring a finding the arm does not emit, which is precisely
the defect `design.md` D-1 exists to prevent and the defect this whole packet
was filed to repair one instance of.

**WHAT DID NOT MOVE, stated so no reader has to diff for it.** OQ-1's
disposition — option (a), D-2 and D-3 still refused. `tasks.md` § 1, still 1.1
and only 1.1. The `code_surface: none` / `target_release: implemented`
declaration. `.openspec.yaml`'s origin block, drafting and approval pairs alike
(ORIGIN RETAINED, unchanged since the ratifying commit `f8eba345`). The
scenario COUNT, still twenty-four (one added over canon's twenty-three), and
every scenario TITLE, this one included — the bullet was NARROWED, never struck
or retitled, so no `Merged into` or `Removed from canon` marker is owed. The
body sentence this packet was filed for, the pointer refresh beside it, and the
added scenario *A finding emitted before root selection names what it judged*
are all untouched by this amendment.

**RE-MEASURED AFTER THE AMENDMENT**, through the modified-block-currency
family's own `derive_units` and `git diff --numstat`, over the amended block
and canon alike: canon 209 units, block 215 units, **THREE uncarried units**
and **NINE new**, canon-diff **FOUR hunks, 21 added / 8 removed** — every
figure UNCHANGED from round 6's, because the WHEN bullet is ONE PHYSICAL LINE
under either wording and has been uncarried against canon since fix round 1
regardless of which wording it holds, canon carrying no such clause at all.
The amendment changes WHICH TEXT canon receives, not how much.

**WHERE THE CONSENT IS RECORDED.** This addendum; the "AMENDED SINCE — ONCE
MORE, AND THIS TIME BY THE RATIFIER HIMSELF" pointer near the head of this
record; `proposal.md` § What Changes' WHEN bullet and its scope sentence;
`design.md` D-2's round paragraph and its reproduction commands;
`tasks.md` § 2.2's round history and § 3.1's ARCHIVED annotation; the README
archived-ledger entry; and the archive pull request's body. **No site states
the WHEN as ratified-and-unamended after this date.**

**AND THE CARRIED COPY MOVES WITH IT.** PR
[#1075](https://github.com/opensoft/openxFactory/pull/1075) → `a93d2682`
ordered `adopt-entry-grain-dispositions-form` AFTER this packet and carried
this scenario's WHEN into that packet's own `## MODIFIED` block VERBATIM. That
carried copy is re-based to the amended WHEN in the same commit as this
amendment, under this same ruling — recorded by a one-line addendum entry in
`openspec/changes/adopt-entry-grain-dispositions-form/review/ratification-2026-09-16.md`.
A carried copy left at the superseded wording would be the very drift the
carriage was performed to prevent.
