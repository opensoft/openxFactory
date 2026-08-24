# Archived-Change Record Discrepancies — Open Bookkeeping Register

Status: record
Kind: reference
Disposition: RULED — Brett ruled every open class on 2026-08-22 in an
in-session multiple-choice round, and `archive-register-rulings` executed those
rulings the same day. Six of the seven classes are now closed or deliberately
recorded as legacy; one half-item stays open for want of a fact Brett did not
supply (C3's `add-worker-credential-by-reference`), and one C1 item is held on
a scope question named in that entry. Per-item outcomes are recorded under each
class below. This document remains a record of what was found, not an authority
for anything: the rulings are Brett's and the execution is the commit's.
Owner: openxFactory (the `document-lifecycle` and `release-realization`
capabilities, and the archived change directories under
`openspec/changes/archive/`).
Opened: 2026-08-22, re-derived over all 86 archived changes; revised the same
day after an adversarial review lap (see "What this register got wrong first").
Ruled: 2026-08-22 by Brett Heap, in-session, a multiple-choice round over every
open class in which the recommended option was adopted on each. Executed the
same day by `archive-register-rulings`. Editing a `Status: record` document
trips doc-health's `record-immutability` critical by design; that cost was
accepted when this file was written and is measured and dispositioned in
"The record-immutability cost of this revision, measured" below.

## Why this file exists

PR #253 ("Give the sixteen rowless archived changes their README rows",
`d23d690`) found seven record-vs-tree or record-internal discrepancies while
writing each README row from that change's own archived record. It deliberately
did not propagate them into the rows, and said they were "enumerated in the
branch report". That branch, `change/readme-archived-rows`, touched exactly one
file (`README.md`) and is deleted from origin, so the enumeration survived
nowhere: the finding evaporated the moment the PR merged.

This register is the durable form. The set below was re-derived from the tree
rather than inherited, so the counts are this tree's, not that branch's, and
the total is not seven.

This file is itself headed `Status: record`, which means a future edit to it
is a `record-immutability` finding of class `contested` — the same cost the
`docs/support-bundle-scope-open-item.md` register carries. Accepted
deliberately: a register of open items is a captured observation, and the way
to revise it is a citing change or a `health/dispositions.yaml` entry, which is
the discipline this register is asking for elsewhere. The alternative headers
would either understate what the file is or exempt it from the rule it invokes.

**Half of that last sentence turned out to be wrong, and is corrected below
rather than rewritten here.** The 2026-08-22 revision paid the cost and
measured it: a `health/dispositions.yaml` entry does NOT silence a live
`record-immutability` critical. It only keeps that finding's eventual
disappearance from being re-emitted as an `uncited-resolution` ERROR. Both
directions were measured with real runs — see "The record-immutability cost of
this revision, measured".

## Corrected in the same change as this file

### B1 — `add-doxbench-editing-phase-a` read `Status: draft` after archiving

`openspec/changes/archive/2026-08-21-add-doxbench-editing-phase-a/proposal.md`
carried `Status: draft` from proposal through archive. The ratification flip
`document-lifecycle` requires in the same change as the transition was never
made, though the transition is on the change's own record in four places: its
`.openspec.yaml` carries `approved_by: Brett Heap (dispositions and phase
sequencing relayed in-session)` and `approved_on: 2026-08-15`; its `tasks.md`
§10 calls Brett "the ratifying authority" and speaks of "the ratified
requirement"; task 9.1 recorded the archive-gate realization evidence under
`release-realization`, which admits only a ratified change; and the archival
promoted this change's text, +5 ADDED and ~2 MODIFIED, into
`openspec/specs/ideation-dashboard/spec.md`.

Corrected to `Status: ratified` **with a citation line**, because
`docs/document-lifecycle.md` § Status Claim Rules requires a `ratified` header
to name its ratification. Both the ratifier and the date are copied verbatim
out of `.openspec.yaml`; nothing is inferred.

The spelling chosen is `Ratified:`, and the choice is deliberate rather than
free. Both spellings are live in the thirty-eight archived proposals that
already read `Status: ratified`, and both are counted:

- **`Ratified by:` — twenty-nine**, folder-dated 2026-07-23 through 2026-08-15.
  This is the rule's literal spelling (`Ratified by: <change>`), and fifteen of
  the twenty-nine do name their own change id ("Brett's approval of
  `<change-id>` on <date>"). The other fourteen name Brett, a date, and a
  quoted instruction instead ("Brett's direction on 2026-07-30 (\"lets do F18
  term-lifecycle enforcement\")"), so the spelling does not *require* a change
  id — but it does require one of the two, and Phase A has neither.
- **`Ratified:` — nine**, folder-dated 2026-08-10 and later, the corpus's later
  form. Eight read `Ratified: <date> by Brett Heap — in-session, verbatim: "…"`.
  The ninth, `2026-08-22-add-roster-device-admission-surface`, reads
  ``Ratified: 2026-08-19 — record: `review/ratification-2026-08-19.md` (…)``: a
  date plus a pointer to the record that carries the ratification, no change id
  and no quote.

Phase A's ratification is neither an approving OpenSpec change (none exists) nor
a quotable in-session utterance that anyone wrote down. What exists is a record
file — this change's `.openspec.yaml`, carrying approver and date. That is the
ninth's shape exactly, so B1 uses `Ratified:` with a `record:` pointer at
`.openspec.yaml`. Reaching for `Ratified by:` would have meant either naming a
change that does not exist or manufacturing a quotation. The reasoning is
recorded in full in that change's own `tasks.md`.

**The precedent this extends, with the constraint the first draft dropped.**
Brett's 2026-08-10 ruling that a later change may correct an archived ledger is
recorded at `2026-08-13-align-doxbench-contract-pin-to-publisher` task 6.2, and
it carries an operative condition: the correction was done "as an APPEND: the
original open-item sentence is left standing word for word and the resolution
follows it, so the record still says what was true when the tranche closed."
B1 cannot honour that literally. An append on the `Status:` line is
mechanically impossible — `doc_health.corpus.STATUS_RE` is
`^Status:\s*(.+?)\s*$`, so it swallows any trailing annotation into the value
and `Status: draft (corrected to ratified)` would register as a free-form
status. B1 is therefore an **in-place overwrite and an extension of the
2026-08-10 ruling, not an instance of it**, and is named as one. The append's
purpose is served another way: the original value is preserved verbatim ("read
`Status: draft` from proposal through archive") here and again in the change's
own correction note, so a reader still finds what the record said before.
Whether an overwrite on a single-valued header falls inside the ruling is
flagged for Brett; the words he gave do not cover it.

The shape borrowed from `split-ideation-book-per-repo` 4.3 is likewise not
identical, and the first draft of this register overstated the match. That
precedent is an **inline suffix on the task line** ("— Discharged by the archive
commit itself (`e9a4be6`, 2026-08-10); the box was left unchecked in that
commit by oversight and corrected here with this note rather than silently").
B1's note is a separate `##` section at the end of the ledger. Same spirit —
the correction travels with the change it corrects and never lands silently —
different shape.

**On `efa42cf`, in that commit's own words.** `efa42cf` says: "The archived
change is therefore restored **byte-exact to main's version**." Byte-exact is
broader than requirement text, and B1 is not byte-exact: it rewrites one line
of front matter and adds one. Re-scoping that phrase to requirement text, as
the first draft of this register did, silently narrows what the commit said.
What actually distinguishes B1 is `efa42cf`'s stated *reason*, not the scope of
the
restoration it performed: "An archive amended after the fact would have claimed
Phase A ratified a conditional slot while the spec its own archival produced
said otherwise: a falsified record." What that forbids is an amendment putting
the archive into disagreement with the spec its archival promoted. A lifecycle
header cannot create that disagreement — it promotes no requirement, and no
reader consults it (see "What the tooling does and does not enforce"). So the
extension past "byte-exact" is deliberate and named: the requirement text
`efa42cf` was protecting is untouched.

After B1, the archived population read: 39 `Status: ratified`, 1
`Status: draft` (C7), and 46 with no `Status:` header at all (C2).

**After the 2026-08-22 rulings it reads: 42 `Status: ratified`, 0
`Status: draft`, and 44 headerless**, over the same 86 archived proposals.
The three additions are C7's `add-dashboard-account-menu` (which was the last
`draft`) and C2's two backfills, `add-governed-derived-model` and
`add-lens-gate-verbs`. Counted in-tree at the executing commit, not inherited.

## Recorded, deliberate, and correctly left alone

### A1 — `target_release: none` on thirteen archived proposals

`none` is not a legal value on the realization axis: `release-realization`
allows `implemented` or a named release, and `none` belongs to `code_surface`.
The 2026-08-13 archive commit `18a4ffc` found this, counted five siblings at
the time, and chose to record it "in the archived task ledger rather than
corrected under cover of an archive commit". Thirteen archived proposals now
carry it. The disposition stands: a per-change judgement about what the axis
*should* have said is not a bookkeeping act, and the value flows into the
dashboard snapshot (`ideation_dashboard.generator._release_frontmatter`), so
rewriting it silently would move a projected field.

Twelve of the thirteen are the bare token. One is not, and it is a materially
different case: `2026-07-30-add-ontology-term-lifecycle-enforcement` reads
`target_release: none (no contract-bundle bytes change; the canonical
validator, tools, and fixture corpus are content-addressed by commit under the
contract-v1.22 registration)`. An **annotated** `none` carrying its own
justification is an author stating why no release applies, which is a defensible
reading of the axis; the bare token states nothing and is the one that reads as
a mis-set field. Any ruling on A1 should treat the two separately, and should
note that the annotation is what a corrected bare token would have to grow.

### A2 — `add-workbench-integrated-editor-chat`'s two deliberate acts

Twenty-four tasks archived open, annotated rather than force-ticked; and the
proposal's lowercase `status: proposed` front-matter field left untouched. Both
are recorded in that change's `tasks.md` and in its README row. Verified still
true: it is the only change in the repository, active or archived, carrying a
`status:` field.

**SUPERSESSION ADDENDUM, 2026-08-23 — the SECOND act only.** Everything above
stands as written and is not edited: the twenty-four open tasks are still
annotated rather than force-ticked, the lowercase `status: proposed` field is
still untouched, and this change is still the only one in the repository
carrying such a field. What is superseded is the consequence this entry and C2
drew from the second act — that the proposal must therefore stay headerless.
**RULED 2026-08-23 (Brett, in-session), recorded as task 5D.2a of
`govern-openspec-corpus-membership`: backfill it too**, and the change's
`proposal.md` now carries `Status: ratified` plus one `Ratified:` citation
derived from its own tasks.md 1.7. The supersession is ON THE 2026-08-02
DECISION'S OWN TERMS rather than an overturning of it. That decision's stated
reason was that "no vocabulary for a post-archive value is defined in `docs/` or
the `release-realization` capability"; the ratification-citation rule in
`openspec/specs/document-lifecycle/spec.md` is now promoted, it owns the
`Status:` field for proposals, and it requires the header the decision declined
to invent. Nothing that decision asserted about the corpus of 2026-08-02 has
been contradicted, and slice 5C's travelling note in the change's own `tasks.md`
quotes it in full and leaves it standing. The "two status fields on one
proposal" hazard C2 named is measured rather than argued away: `Status:` and
`status:` are two different keys to `doc_health.corpus.STATUS_RE`, which is
case-sensitive, so exactly ONE of the two lines is machine-read and the
proposal carries one status of record, not two. The first act — the
twenty-four open tasks — is untouched by this ruling and remains correctly
recorded above.

### A3 — `add-roster-device-admission-surface`'s realization axis

`8924838` recorded that this change's front matter still read a bare
`target_release: implementation_pending` and handed the correction to "the
archive slice's bookkeeping". The archive slice `d9b80c1` did it: the axis now
reads `implemented — realized on the openxFactory main line and cut as
contract-v1.35 …`. Closed, not open.

### A4 — archived changes with annotated open tasks

`add-governed-derived-model` 1.2, `add-crystallizer-contracts` 3.1,
`add-capability-steward` 3.1, `align-demote-to-round-trip-rule` 7.2,
`add-dashboard-account-menu` 6.2, `add-roster-device-admission-surface` 6.1.
Each open box carries its own reason in the ledger — a downstream consumer,
a deferred live proof, a ruling left open on purpose. Nothing to fix.

**CORRECTED 2026-08-22 by `archive-register-rulings`: two of the six are not
annotated, so "each open box carries its own reason" was wrong.** Re-read box
by box while sourcing the C6 annotation shape. `add-crystallizer-contracts` 3.1
and `add-capability-steward` 3.1 are bare, unannotated open boxes carrying
byte-identical text ("OpenSpec Records entry at raise; doc-index links land
with the promoted specs at archive"), and neither ledger has any trailing note
section. The other four are annotated as described. The corrected claim: four
of the six carry their own reason; two are unannotated open boxes of the same
class as C6 and were simply never counted into it. They are recorded here
rather than annotated, because Brett's 2026-08-22 ruling on C6 named the four
avatar changes and nothing else, and extending a ruling to items it did not
name is the error this register exists to avoid. Two lines, one ruling round
away from closing.

### A5 — the two repairs PR #253 made at its own gate

`split-ideation-book-per-repo`'s unticked 4.3 is ticked with an inline note,
and the lens pair (`add-repository-lens`, `add-project-visible-set`) carry
their `.openspec.yaml` staged-origin declarations. Both confirmed present.

## Ruled 2026-08-22 — the classes that were open, and what closed them

Seven classes are recorded below. Six were OPEN when this register was written
and now carry a **RULED** block stating Brett's ruling, the option adopted, and
what `archive-register-rulings` actually executed against it. The original
entry above each block is left standing word for word — the append discipline
Brett set on 2026-08-10 and this register invokes throughout — so the record
still says what was true when the register was captured. The seventh, C4, was
never OPEN — its own entry says "No action proposed" — and was never part of
the ruling round; it carries no RULED block. That is the split this document's
own `Disposition:` header counts: "Six of the seven classes are now closed or
deliberately recorded as legacy."

### C1 — `target_release: implementation_pending` on six archived proposals

`split-ideation-book-per-repo`, `add-worker-credential-by-reference`,
`add-client-identity-roster`, `align-demote-to-round-trip-rule`,
`align-status-reader-to-real-lines`, `refine-demote-round-trip-mechanics`.

`implementation_pending` is a house token the realization axis does not define
— the axis allows `implemented` or a named release — and, unlike A1's `none`,
it is also self-contradicting on an *archived* change: the archive gate admits
a change only on merge-plus-green evidence, which is exactly the condition
`implementation_pending` says is still owed. `8924838` states that reading
plainly ("the bare token means 'realization is owed'") and A3 shows the
correction shape. Two questions for the ruling: whether the token should be
ratified into the axis as a third legal value for the active phase, and
whether these six are corrected in place or recorded as A1 was.

**RULED 2026-08-22 (Brett, in-session multiple-choice round; recommended option
adopted): one cleanup fixes all six.** Correct in place, deriving each change's
realization evidence from its OWN record — archive commit, tasks.md evidence,
README row, release tags — and rewriting the value to the `implemented —
<evidence>` spelling `d9b80c1` established. The ruling carried an explicit
escape: any of the six whose realization evidence is genuinely ambiguous stays
untouched and is recorded here instead. No forced fixes. The ruling did not
reach the token's legality on the active phase; that half of the question is
still open and is not answered by these six rewrites.

**FOUR FIXED, TWO NOT.** Executed by `archive-register-rulings`:

| change | outcome | evidence the rewritten value names |
| --- | --- | --- |
| `align-demote-to-round-trip-rule` | **FIXED** | PR #215 (`e2c07ef`, `d28d36d`, `1c8b58a`, `79ed72e`, 2026-08-19), 3240 tests / 62-of-62 strict / doc-health baseline-identical — from its own tasks.md §6.2 and banner |
| `align-status-reader-to-real-lines` | **FIXED** | PR #222 (merged 2026-08-20T01:24:14Z, six named shas), re-verified green at `7312c25` — from its own tasks.md §6.2 and banner |
| `refine-demote-round-trip-mechanics` | **FIXED** | PR #221 (merged 2026-08-20T01:23:54Z, five named shas), re-verified green at `7312c25` — from its own tasks.md §7.2 and banner |
| `add-client-identity-roster` | **FIXED**, with its source named | PR #190 / `71674ed`, cut as the `contract-v1.33` bundle 2026-08-15 — sourced from the archive commit `753d02d` and the README row, NOT from tasks.md |
| `split-ideation-book-per-repo` | **LEFT UNTOUCHED — genuinely ambiguous** | see below |
| `add-worker-credential-by-reference` | **LEFT UNTOUCHED — held on a scope question, not on evidence** | see below |

**Three corrections the execution had to make to the ruling's own template, all
of them factual.**

1. **`d9b80c1`'s sentence does not transplant.** Its clause reads "realized on
   the openxFactory main line and cut as contract-v1.35", and that is specific
   to `add-roster-device-admission-surface`. Three of the four fixed changes
   (`align-demote-to-round-trip-rule`, `align-status-reader-to-real-lines`,
   `refine-demote-round-trip-mechanics`) cut **no contract bundle at all** —
   their surfaces are code-only, and their discharge is merge-plus-green on
   main, full stop. Each rewritten value says so explicitly rather than
   borrowing a release it never had. What was actually copied from `d9b80c1` is
   its SHAPE: `implemented — <evidence>`, followed by the original
   `implementation_pending` value preserved verbatim and the statement of what
   discharged it.
2. **`contract-v1.33` is not a git tag, and neither is `contract-v1.35`.**
   `git tag --list 'contract-v*'` returns `contract-v1.7`–`contract-v1.32`,
   then `v1.34`, `v1.36`, `v1.37`, `v1.38`, `v1.40`; `v1.33`, `v1.35` and
   `v1.39` are absent. Both cuts are real as BUNDLES —
   `contracts/releases/contract-v1.33.digests.yaml` and its
   `contracts/CHANGELOG.md` section exist — so `add-client-identity-roster`'s
   rewritten value says "cut as the `contract-v1.33` bundle" and records the
   missing tag rather than implying one. Worth carrying forward: `d9b80c1`'s
   own "cut as contract-v1.35" means the bundle too, not a tag.
3. **`add-client-identity-roster` was fixed against a ledger that never closed
   its own archive gate.** Its tasks.md §5.1 and §5.3 — the strict-validation
   box and the "archive on realization evidence" box — are still unticked, as
   are §2.1–2.5, §3.1–3.4, §4.1–4.3 and §5.2 — every other box outside §1. On
   its own ledger this change reads as never having passed the gate it archived
   through. The realization itself is not in doubt (`71674ed`, PR
   #190, the v1.33 bundle files), and the ruling named the archive commit and
   the README row as parts of "its own record", so the fix stands and its front
   matter says where the evidence came from. But the ledger gap is a C6-shaped
   anomaly that this round did not touch and did not have a ruling for:
   **fifteen-odd unticked boxes on a change whose README row claims
   realization.** Recorded here rather than annotated.

**Why `split-ideation-book-per-repo` was left.** Its record names no pull
request, no merge sha other than the archive commit itself, no contract cut,
and no green-run output. The only realization statement in the change is task
4.3's "Discharged by the archive commit itself (`e9a4be6`, 2026-08-10)" — which
is circular: the archive commit is the act whose admissibility
`implementation_pending` was gating, so it cannot be the evidence that the gate
was satisfied. Task 4.2 speaks of a full post-migration sync recorded "as
realization evidence", but that output is recorded nowhere in the folder.
Writing `implemented — <evidence>` here would mean naming evidence the record
does not carry. This is exactly the case the ruling's escape clause was for.

**Why `add-worker-credential-by-reference` was left, and why that is a
different reason.** Its evidence is not thin. The change wrote its own
archive-gate condition into its front matter — "the change archives on one
worker lane fetching its model-provider credential from the vault per-job with
green live evidence" — and its tasks.md names that condition discharged, dated,
with an operator confirmation and a run id (§2.3 xFactory `0af326a`; §2.4 the
§11.4 smokes, "token source VAULT with SMOKE OK", then a rotation consumed by
the next run; §2.5 final smoke run 31833019258; §3.1 "code surface green: vault
fetch live on all three lanes, rotation scenario proven, host credential-free
end state reached"), corroborated by the README row. That the shas do not
resolve in this repository is by design, not a gap: its declared `code_surface`
is "xFactory aggregation (worker-lane fetch steps + runbook §11) +
operator-executed provisioning …; openxFactory contract-only otherwise". On its
own terms the discharge is named.

It was left untouched anyway, because **the same 2026-08-22 round ruled "do not
touch it" over this change** in closing C3's account-menu half (see C3 below).
That instruction is written under a C3 heading and is most naturally read as
scoped to the ratification-and-origin axis, which is where C3 lives; C1's
ruling, meanwhile, enumerates six changes and this is one of them. Two ruled
sentences point opposite ways over one file, and neither can be honoured
without overriding the other. The conservative reading was taken — nothing was
written to the file — because the cost of that choice is one more sentence from
Brett, while the cost of the other choice is an edit to a change he may have
meant to freeze. **This is the one item in the round that needs a word back:
does C1's cleanup cover `add-worker-credential-by-reference`'s
`target_release`, or does C3's "do not touch it" freeze the whole change?** The
rewritten value is ready either way; only the permission is missing.

**ADDENDUM 2026-08-22 (later the same day) — the word came back; five of six
are now fixed.** Brett ruled, in a separate in-session round held after this
entry and C3 were written, that C3's "do not touch it" was scoped to the
ratification-and-origin axis — where C3 lives — and not to the release axis,
so C1's cleanup does cover `add-worker-credential-by-reference`'s
`target_release` after all. The rewritten value was written:
`implemented — code surface green on the xFactory aggregation main line …`,
naming task 2.3's lane wiring (`0af326a`), task 2.4's live evidence (the
§11.4 smokes, "token source VAULT with SMOKE OK," then a proven rotation),
task 2.5's remaining-lane migration and host cleanup (`6758046`, final smoke
run `31833019258`), and task 3.1's closeout tick — corroborated by this
change's own archive commit `b533a1f` and its README row. Sourced entirely
from this change's own tasks.md §2.3–§2.5 and §3.1, the same record already
quoted above; nothing new was inferred. **FOUR FIXED, TWO NOT** above is
superseded by this addendum only in the count, not in its word-for-word
text: read it as **FIVE FIXED, ONE NOT** from here forward. The one change
still not fixed is `split-ideation-book-per-repo`, for the reason already
given above (its only realization statement is the archive commit itself,
which is circular). The open question this entry posed is answered: C1's
cleanup covers `add-worker-credential-by-reference`; C3's freeze does not
reach the release axis, only the ratification-and-origin axis where C3
itself lives (see C3's own addendum).

### C2 — seven archived proposals were authored after the `Status:` convention began and carry no header

This entry was re-derived on a second axis after the first draft got it wrong.
**Two different dates are in play and they must not be mixed.** A change's
archive-folder date prefix is when it *archived*; its `Status:` header, if it
has one, was written when the proposal was *authored*, typically days or weeks
earlier. Arguing about a header-writing convention from folder dates therefore
measures the wrong thing. Both axes are stated here explicitly.

**Folder-date axis (a fact about the archive, not about the convention).**
Forty-six of the eighty-six archived proposals carry no `Status:` header.
Thirty-two of those forty-six have a folder date earlier than 2026-07-23, the
earliest folder date on which a header-carrying proposal was archived. The
remaining fourteen are folder-dated 2026-07-23 through 2026-08-09 and sit
interleaved with archived changes that do carry a header; every archived change
folder-dated 2026-08-10 or later carries one. The 32-of-46 figure stands as a
folder-date fact and nothing more. Two proposals tie at the earliest header
folder date (`2026-07-23-add-hermes-domain-overlay-contract` and
`2026-07-23-adopt-subject-tenant-domain-vocabulary`), so no single archived
proposal is "the first to carry the header" on this axis.

**Authoring-date axis (the one the convention lives on).** Re-derived with
`git log --diff-filter=A --follow` over each `proposal.md`. The first headers
were authored on **2026-07-22** — three that day
(`add-hermes-domain-overlay-contract`, `adopt-subject-tenant-domain-vocabulary`,
`add-omnigent-domain-overlay`), and no header-carrying proposal was authored
earlier. Measured against that start, thirty-nine of the forty-six headerless
proposals were authored *before* 2026-07-22 and are genuinely pre-convention.
**Seven** were authored on or after it, and those seven are the whole anomaly:

| authored | archived as |
| --- | --- |
| 2026-07-23 | `2026-07-23-add-governed-derived-model` |
| 2026-07-24 | `2026-08-01-add-propose-verb` |
| 2026-07-25 | `2026-08-01-add-staging-workbench` |
| 2026-07-25 | `2026-08-01-add-workbench-bullseye-and-create` |
| 2026-07-25 | `2026-08-05-add-wheel-action-verbs` |
| 2026-07-25 | `2026-08-06-add-lens-gate-verbs` |
| 2026-07-30 | `2026-08-02-add-workbench-integrated-editor-chat` |

The other seven of the fourteen "interleaved" changes were authored between
2026-07-09 and 2026-07-16 and merely archived late
(`add-ideation-dashboard`, `add-ideation-cross-reference-readiness`,
`add-possibles-derivation-lane`, `implement-avatar-client-lab`,
`add-cross-factory-ideation-routing`, `add-proposal-origin-contract`,
`qualify-avatar-brokered-call-feasibility`). They are pre-convention, not
anomalies. No headerless proposal was authored after 2026-07-30 at all.

So the headline count is **seven**, not fourteen, and the class is much smaller
and much more recent than the folder-date reading suggests.

Still deliberately not fixed. B1 corrected a header whose value the record
contradicted; these carry no value at all, so supplying one is authoring, not
correcting — the hazard `add-workbench-integrated-editor-chat`'s own ruling
names ("inventing a value for an unowned field would be worse than leaving the
one the author wrote"). The ruling wanted is one decision for the class:
backfill the seven post-convention proposals from each change's archive
evidence, backfill all forty-six, or record that a missing header on an
archived proposal means what its location means.

**RULED 2026-08-22 (Brett, in-session multiple-choice round; recommended option
adopted): backfill the seven true anomalies where the records allow, and only
there.** For each, hunt the ratification evidence — its `.openspec.yaml`
`approved_by`/`approved_on`, `Ratified`-style lines elsewhere in its record,
the archive and ratification commits, the README row. Where the record names an
approver and/or a date, add `Status: ratified` plus a citation line in whichever
existing spelling honestly fits. Where it does not, leave it headerless and
record why here. No invented provenance anywhere. The forty-six-wide option was
not taken.

**TWO BACKFILLED, FIVE LEFT HEADERLESS.** Executed by
`archive-register-rulings`:

| authored | change | outcome | what the record supplied |
| --- | --- | --- | --- |
| 2026-07-23 | `add-governed-derived-model` | **HEADER ADDED** | date only — `Ratified: 2026-07-23` |
| 2026-07-24 | `add-propose-verb` | left headerless | nothing |
| 2026-07-25 | `add-staging-workbench` | left headerless | origin approval + a task sign-off, neither a ratification |
| 2026-07-25 | `add-workbench-bullseye-and-create` | left headerless | same |
| 2026-07-25 | `add-wheel-action-verbs` | left headerless | same |
| 2026-07-25 | `add-lens-gate-verbs` | **HEADER ADDED** | approver + date — `Ratified: 2026-08-06 by Brett` |
| 2026-07-30 | `add-workbench-integrated-editor-chat` | left headerless, and it must stay that way | a recorded decision AGAINST writing a status value |

**`add-governed-derived-model` — a date with no name, which the corpus already
has a spelling for.** Three independent places in its own record carry
`2026-07-23`: the archive commit `e8c2970`, titled "Ratify and archive
add-governed-derived-model" and opening "Ratified 2026-07-23"; its tasks.md
("Ratified and archived 2026-07-23"); and the README row ("**ratified,
realized, and archived 2026-07-23**"). No prose anywhere names a ratifier. The
commit is authored by `brettheap`, but that is git metadata, not a recorded
attribution, and it is deliberately NOT cited as one. A date plus a record
pointer with no approver is precisely the spelling
`2026-08-22-add-roster-device-admission-surface` already uses, so that is the
spelling used, and the citation line says in as many words that the date only
is recorded. One mechanical note: this proposal has no `---` fences at all —
its `code_surface:` and `target_release:` are bare lines — so the header was
added as bare lines too, matching `split-ideation-book-per-repo`, which carries
`Status:`/`Ratified:` the same fenceless way. No fences were introduced.

**`add-lens-gate-verbs` — an approver and a date, and a caveat written into
the citation itself.** Its tasks.md 3.3 reads "DISCHARGED by disposition, ruled
by Brett 2026-08-06 (decision round)", the archive commit `409e399` is titled
"Archive add-lens-gate-verbs under Brett's 3.3 disposition", and the README row
repeats it. That is a named human and a date attached to a decision about this
change. It is also, read literally, a **realization** disposition — Brett ruled
that the 3.1 route tests, the 3.2 Playwright smoke, and his 4.4 wheel-verbs
human pass were together sufficient realization evidence — and the word
"ratified" appears nowhere in this change. The header was still added, because
it is the only named human decision on the record and it is the decision the
change archived under; but the citation line states the gap plainly and points
a reader at 3.3 for the literal act. This is the weaker of the two backfills
and is flagged as such rather than smoothed over.

**Why the three remaining 2026-07-25 changes were left (the fourth,
`add-lens-gate-verbs`, is the backfill above), though each has an
`approved_by`/`approved_on` pair.** `add-staging-workbench`,
`add-workbench-bullseye-and-create` and `add-wheel-action-verbs` each carry
`approved_by: Brett (openxFactory operator authority)` / `approved_on:
2026-07-25` in `.openspec.yaml`. Those fields are nested under `origin:`, and
`document-lifecycle`'s origin requirement says exactly what they mean: an
ad-hoc origin is "an explicit, approved exception", and the pair records who
approved authoring the change without a staging source and when. The dates are
the changes' `created:` dates and sit six to eleven days before their archives.
Reading them as ratification would date each change's ratification to the day
it was proposed. B1 did cite a `.openspec.yaml` approval pair as a ratification
record for `add-doxbench-editing-phase-a`, but that case differs on both
counts: its `approved_on` coincided with the ratification, and its `reason`
narrates Brett's dispositions on the change's substance rather than permission
to author it. Each of these three also carries a Brett-named task sign-off
(2026-08-01 in the D10 pass) — task acceptance, not ratification either. Two
near-misses on the same record is a reason for care, not a reason to pick one.

**Why `add-propose-verb` was left.** Nothing. Its front matter, its whole
directory, its created and archive commits, and its README row name no
ratifier and no ratification date. Its one Brett-plus-date pair lives in a
DIFFERENT change's evidence directory
(`2026-08-02-add-workbench-integrated-editor-chat/evidence/d10/signoff-matrix.md`)
and is a task-4.3 acceptance.

**Why `add-workbench-integrated-editor-chat` must stay headerless — a stronger
reason than the other four.** Leaving it alone is not merely the absence of
evidence here; adding a header would contradict a recorded decision in its own
archive commit. `354ded9` states: "FRONT MATTER deliberately untouched:
`status: proposed` stands. The archive tool neither reads nor writes it, NO
other change in this repository — active or archived — carries a `status:`
field, and no vocabulary for a post-archive value is defined … The change's
location under `openspec/changes/archive/` is its status of record; inventing a
value for an unowned field would be worse than leaving the one the author
wrote." That is A2 of this register, verified deliberate. Writing
`Status: ratified` beside its existing lowercase `status: proposed` would put
two status fields on one proposal and overturn a ruling nobody revisited. The
only named human decision on its record is a reviewer-of-record MERGE decision
on PR #63 (Brett Heap, 2026-08-02T20:34:22Z), which is a review gate, not a
ratification.

**Net: the class is smaller again.** Of the seven true anomalies, two now carry
headers, one is protected by a recorded decision against ever carrying one, and
four carry no ratification provenance for a header to cite. The thirty-nine
pre-convention headerless proposals were out of scope for this ruling and stay
exactly as they were.

### C3 — two archived changes have no origin declaration and are past the contract date

`archive/2026-08-14-add-worker-credential-by-reference` and
`archive/2026-08-22-add-dashboard-account-menu` have no `.openspec.yaml` at
all. Both are dated after `proposal-origin`'s 2026-08-07 contract date, so the
family reports them at **ERROR** severity, class auto-fixable — the two errors
in a current `--family proposal-origin` single-repo run.

Precedent exists for repairing this at a gate (`18a4ffc` added its own change's
missing file; PR #253 added the lens pair's declarations). It was not taken
here because neither change is staged-derived: both would have to be declared
`ad_hoc`, and the family requires a non-empty `reason`, `approved_by` and
`approved_on` for an ad-hoc origin. Nothing in either record states an approver
or an approval date for the origin, and `proposal_origin.py`'s own contract is
that provenance is never fabricated or inferred. Writing three fields from
inference to clear an auto-fixable error would put invented provenance into a
governed record. Needs Brett to supply the two approvals, or a ruling that a
recorded exemption is the right close. For `add-dashboard-account-menu` this is
the same missing pair of facts as C7, and one ruling closes both.

**RULED 2026-08-22 — ONE HALF CLOSED, ONE HALF STILL OPEN.** Brett supplied the
missing facts for `add-dashboard-account-menu` and supplied nothing for
`add-worker-credential-by-reference`, so the round closed exactly one of the
two errors this entry named.

**`add-dashboard-account-menu` — CLOSED.** Brett declared that he ratified the
change in-session on 2026-08-21, its authoring date, and
`archive-register-rulings` wrote the change's `.openspec.yaml`: an `ad_hoc`
origin — no staging topic exists behind it, the requirement having been read
off the deployed surface — with `approved_by: Brett Heap`, `approved_on:
2026-08-21`, and a `reason` that states in full that the file was written on
2026-08-22 rather than at the transition, and that the approval pair is Brett's
declaration rather than a contemporaneous record. The refusal this entry made
still stands on its own terms: nothing was inferred from the archive gate or
from `c09fe68`'s wording, and re-reading the record will still turn up no
contemporaneous trace. What changed is not the evidence but the authority.
C7 closes on the same pair of facts.

**`add-worker-credential-by-reference` — STILL OPEN.** Brett supplied no
ratification fact for it and ruled that it not be touched. Its record is
unchanged, it still carries no `.openspec.yaml`, and it is now the single
`proposal-origin` ERROR in a single-repo run rather than one of two — measured,
2 error before the round and 1 after. The same instruction is what held C1's
rewrite of this change's `target_release`; the scope question that raises is
stated in full in C1's block.

**ADDENDUM 2026-08-22 (later the same day).** The release-axis half of this
hold was executed 2026-08-22: Brett ruled the freeze scoped to the
ratification-and-origin axis only, and C1's addendum above records the
`target_release` rewrite now written. The origin-and-ratification half
recorded above — no `.openspec.yaml`, no approval pair, still the single
`proposal-origin` ERROR — is unchanged and stays open.

### C4 — twenty-one archived changes are pre-contract-legacy origin warnings

Measured on a live `--family proposal-origin` single-repo run: 2 error, 30
warning. Twenty-one of the thirty warnings are archived changes; the other nine
are active. All are reported at WARNING by design ("never fabricated, never a
regression-gate break"). Listed here only so the ERROR pair in C3 is not
mistaken for the whole population. No action proposed.

**Re-measured 2026-08-22, after C3's account-menu ruling landed.** The same
command — `python3 scripts/doc-health.py --single-repo . --family
proposal-origin` — now reads **1 error, 30 warning**. The `.openspec.yaml` C3
records for `add-dashboard-account-menu` closed one of the two ERROR-severity
findings this entry counted when it was written; the survivor is
`add-worker-credential-by-reference`, held open by the same ruling (see C3's
RULED block). The warning count did not move. So "the ERROR pair in C3" above
is no longer a pair — it is a singleton — and this addendum is the correction
rather than a silent rewrite of the original count.

### C5 — `enable-live-openxfactory` declares four capabilities that were never promoted

`archive/2026-06-26-enable-live-openxfactory/specs/` carries
`## ADDED Requirements` deltas for `live-factory-runtime`,
`hermes-omnigent-integration`, `worker-runtime-admission` and
`github-merge-enforcement`. None of the four exists under
`openspec/specs/`. It is the only archived change in the corpus with an
unpromoted delta — its two 2026-06-26 siblings both promoted
(`canonical-policy-migration`, `repo-boundary-governance`).

The same change also calls itself `enable-live-openxfactory-factory` in its own
`README.md` and throughout `evidence/`, against a folder id of
`enable-live-openxfactory`. Both are bootstrap-era artifacts from before the
archive convention settled. Recorded rather than resolved: promoting four
capabilities is a governance act, and deleting the deltas destroys the record
of what the change intended.

**RULED 2026-08-22 (Brett, in-session multiple-choice round; recommended option
adopted): leave it recorded as legacy.** The four capabilities were
deliberately not promoted and stay unpromoted; the folder-id-versus-self-name
mismatch stays as the bootstrap-era artifact it is. **No file in
`archive/2026-06-26-enable-live-openxfactory/` was changed by this round**, and
none should be by a later one absent a governance act that actually promotes
the capabilities. This entry is closed as RULED — legacy, not as a defect
awaiting repair, so a future sweep that rediscovers the unpromoted deltas
should read this line and stop rather than re-open the question.

**SUPERSESSION ADDENDUM, 2026-08-23 — ONE HEADER LINE ONLY.** Everything above
stands as written and is not edited: the four capabilities were deliberately
not promoted, they stay unpromoted, `openspec/specs/` gains nothing from
them, and the folder-id-versus-self-name mismatch stays exactly the
bootstrap-era artifact this entry called it. What is superseded, narrowly, is
this entry's "no file … was changed by this round, and none should be by a
later one absent a governance act that actually promotes the capabilities" as
applied to the proposal's missing `Status:` header specifically. **RULED
2026-08-23 (Brett, in-session), recorded as task 5C.3 of
`govern-openspec-corpus-membership`: backfill `Status: draft` too**, and the
change's `proposal.md` now carries that one line and nothing else — no
`Ratified:`/`Ratified by:` citation, because `openspec/specs/document-lifecycle/spec.md`
requires a citation only for `Status: ratified`, and "absent such backing the
document MUST carry `draft` or lower status". `draft` records the honest
value this folder has always supported: never ratified, archived by Brett's
own PR #28 with `--skip-specs`, retaining the four spec deltas as archived
design evidence rather than promoting them. Nothing this entry found about
the four capabilities, the archive act, or the `--skip-specs` reasoning is
contradicted, and the change's own `tasks.md` quotes this entry's ruling in
full and leaves it standing. This is C2's successor's amended stop-and-report
(`docs/archive-record-discrepancies.md`'s 2026-08-23 slice-5C section, C5
addendum cross-reference); slice 5C's own STOP AND REPORT on this document is
resolved by this addendum, not by re-opening C2 or C5's class findings.

### C6 — four 2026-07-13 avatar changes archived with unticked ledgers

Counted box by box:

| change | boxes | ticked | open |
| --- | --- | --- | --- |
| `align-avatar-first-ui-standard` | 8 | 0 | 8 |
| `implement-avatar-reference-runtime` | 11 | 0 | 11 |
| `clarify-avatar-revocation-client-enforced` | 4 | 0 | 4 |
| `define-avatar-client-contract-kernel` | 14 | 1 | 13 |
| **total** | **37** | **1** | **36** |

Thirty-six of thirty-seven boxes open, while their README rows and the contract
record report realization (`align-avatar-first-ui-standard`'s row: "realized as
`contract-v1.8`"). Unlike A4's open boxes, none of these carries an annotation
saying why it is open, so the ledgers and the rows disagree with no
reconciliation on the record.

Not fixed: ticking thirty-six boxes from inferred evidence is the same
authoring hazard as C2, one order of magnitude larger.

**RULED 2026-08-22 (Brett, in-session; the prose recommendation, unopposed):
annotate all four ledgers, tick nothing.** `archive-register-rulings` appended
a `## Bookkeeping annotation` section to the end of each of the four
`tasks.md` files, stating what the archive evidence actually shows: how many
boxes archived open, what that change's README row claims about realization,
and where the realization evidence actually lives. **No box was ticked and no
task text was altered in any of the four.** The counts in the table above were
re-verified box by box before writing and all four hold exactly: 8/0, 11/0,
4/0, 14/1, totalling 37 boxes with 36 open.

The shape is the separate trailing `##` section rather than an inline suffix on
a task line. Both are house forms — `add-doxbench-editing-phase-a`'s own
correction note adjudicates the choice in writing ("This is a separate `##`
section appended to the ledger's end. Same spirit … different shape") — and the
trailing section is the right one here because the annotation is about each
ledger as a whole, not about one box. The closest structural precedent is
`add-workbench-branch-sessions`'s "## Realization evidence (2026-07-27) —
sections 2-8 ticked against merged code", which likewise names an execution
ledger living elsewhere and says which boxes stay open and why.

**The finding that made the annotations writable: the ticking happened in a
different ledger.** Three of the four have a Speckit feature that was the real
execution vehicle, and each is complete —
`specs/001-avc-contract-kernel/tasks.md` 54 of 54 done,
`specs/003-avc-reference-runtime/tasks.md` 65 of 65,
`specs/004-avatar-first-ui/tasks.md` 37 of 37, zero open in all three. The work
was tracked there and never mirrored back into the OpenSpec boxes. So the C6
gap is bookkeeping, not evidence: `contract-v1.7` (`ddff475`, 2026-07-12) and
`contract-v1.8` (`81fceae`, 2026-07-13) are both real annotated tags with
matching CHANGELOG sections, the promoted specs exist, and every contract,
runtime, test, example and validator artifact the ledgers name is on disk.

**One of the four does not belong in the class as stated, and its annotation
says so.** This entry's premise is that the ledgers and the README rows
"disagree" about realization. `clarify-avatar-revocation-client-enforced` has
**no realization claim in its README row at all** ("ACR-005 disposition:
revocation is client-enforced within the 5 s bound; archived 2026-07-13") and
declares `target_release: none`. There is nothing for its ledger to disagree
with, and its annotation asserts no realization. What that annotation records
instead is that the clarified requirement text did reach the canon
(`openspec/specs/avatar-client-runtime/spec.md`) and that the ACR-005
disposition is carried in `contracts/avatar-client/kernel-handoff.yaml`
(`revocation_model: client_enforced`) — plus the fact that two of its four
boxes sit under a section its own author headed "Downstream realization
(tracked in sibling changes; not gated by this change)", which makes them
`add-roster-device-admission-surface` 6.1's case: unticked meaning "owned
elsewhere". So the honest count is **three ledgers whose rows claim realization
the boxes do not reflect, and one that never claimed it.**

Two stale evidence pointers were found and flagged in the annotations rather
than rewritten: `define-avatar-client-contract-kernel` 1.2 and
`clarify-avatar-revocation-client-enforced` 1.2 both cite paths under
`openspec/changes/qualify-avatar-brokered-call-feasibility/`, which stopped
resolving when that sibling archived on 2026-08-09. The task text is left as
written and the annotation carries the correction.

### C7 — `add-dashboard-account-menu` reads `Status: draft` with no citable ratifier

`openspec/changes/archive/2026-08-22-add-dashboard-account-menu/proposal.md`
carries `Status: draft` from proposal through archive, and the same defect B1
describes: the ratification flip `document-lifecycle` requires in the same
change as the transition was never made. The transition is implied on the
record three times — the realization commit `c09fe68` opens "Realizes the
ratified add-dashboard-account-menu change"; the archive commit `afd7b33`
archived it under `release-realization`'s gate, which admits only a ratified
change; and the archival promoted four requirements into
`openspec/specs/ideation-dashboard/spec.md`.

**Flipping it was drafted in this change and then withdrawn.** The reason is
the same lifecycle rule that makes B1 correct: § Status Claim Rules requires a
`ratified` header to *name* its ratification, and every one of the thirty-eight
pre-existing `Status: ratified` archived proposals does so in one of the two
spellings. This change's record names no approver and no date. `c09fe68` says
the change was ratified; it does not say by whom or when, and neither does
`afd7b33`, the README row, or any file in the change directory — there is no
`.openspec.yaml` here at all (that absence is C3's other half). A bare flip
would assert provenance the record cannot back; a flip with a citation would
mean inventing a ratifier or a date. That is precisely what C3 refuses to do
with `approved_by`/`approved_on`, and the refusal has to hold on both axes.

The ruling is cheap: name the ratifier and the ratification date for
`add-dashboard-account-menu`, and this entry and C3's account-menu half close
together on the same pair of facts. The consideration and the withdrawal are
recorded in that change's own `tasks.md` so the next reader who spots the
anomaly finds the reasoning rather than re-opening it.

**RULED 2026-08-22 (Brett, in-session multiple-choice round; recommended option
adopted): "I ratified it 2026-08-21."** Brett declared the fact this entry was
waiting for — he ratified `add-dashboard-account-menu` in-session on
2026-08-21, its authoring date. **CLOSED.** Three things were executed by
`archive-register-rulings`, and a fourth deliberately was not.

1. **The header was flipped**, `Status: draft` → `Status: ratified`. The
   original value is preserved verbatim in prose here, on the new citation
   line, and in the change's own tasks.md, because an append on a single-valued
   header is mechanically impossible for the reason B1 states
   (`doc_health.corpus.STATUS_RE` swallows a trailing annotation into the
   value). Like B1, this is an in-place overwrite and an **extension** of
   Brett's 2026-08-10 append ruling, not an instance of it, and is named as one
   in both places.
2. **A `Ratified:` citation line was added**, satisfying § Status Claim Rules.
   It reads `Ratified: 2026-08-21 by Brett Heap — record: the 2026-08-22
   in-session ruling round captured in docs/archive-record-discrepancies.md
   (C7 and C3's account-menu half) …`. The record-citing `Ratified:` spelling
   was kept for the reason this entry already established and the ruling did
   not change: there is still no approving OpenSpec change to name and still no
   contemporaneous quotation. The record it cites is **this register**, not the
   new `.openspec.yaml`. That is a deliberate departure from B1, which cites
   its own origin file: B1's origin file predated the correction and was
   independent evidence, whereas this change's was written in the same act from
   the same declaration, so citing it would be circular.
3. **The `.openspec.yaml` was written**, closing C3's account-menu half — see
   that entry.
4. **Not done: nothing was inferred, and nothing was discovered.** It is worth
   being exact about what this ruling did and did not change, because the
   entry above is careful and would otherwise read as having been overturned.
   It was not. Every sentence of it remains true of the record: `c09fe68` still
   does not say by whom or when, and neither does `afd7b33`, the README row, or
   any file that was in the directory. The ratification fact is a
   **declaration by the ratifier**, not a discovery in the archive, and the
   citation line and the change's tasks.md both say so in as many words. Had
   Brett not stated it, this entry would still be open.

The `tasks.md` note that recorded the withdrawal was NOT overwritten. Its
heading gained a second clause naming the later ruling, a forward pointer was
added above it, and a "Bookkeeping resolution" section was appended after it —
the original decline reasoning stands word for word, including its opening
sentence "Nothing in this change's record is edited", which was true when it
was written and is false now. Preserving that rather than tidying it away is
the whole content of the 2026-08-10 append discipline.

## What this register got wrong first

An adversarial review lap on 2026-08-22, before this change was pushed,
returned FIX FIRST on the first draft of this register. What it corrected,
recorded here because a register that hides its own errata is worth less than
one that shows them:

- **The account-menu flip (now C7) was made and has been reverted.** It failed
  the citation half of § Status Claim Rules, which the first draft did not
  apply to itself.
- **The phase-a flip (B1) kept, and gained the citation line it always
  needed.**
- **C4 read nineteen; the live run says twenty-one archived warnings.**
- **C6 read "13 boxes, 1 ticked" for the kernel and "32 of 36" across the four;
  the boxes count 14/1 and 37/36.**
- **C2 argued from archive-folder dates, which is the wrong axis for a
  header-writing convention.** Re-derived on authoring dates; the headline
  count falls from fourteen to seven, and the "applied unevenly for eighteen
  days" span claim is withdrawn as an artifact of the wrong axis.
- **The 2026-08-10 precedent was paraphrased with its operative APPEND
  constraint dropped**, and the `efa42cf` distinction re-scoped that commit's
  "byte-exact" without quoting it. Both are now quoted and addressed as
  deliberate extensions.
- **A1's annotated `none` was folded in with the twelve bare ones.**
- **The tooling claim read "byte-identical … differing only in the corpus-size
  lines", which contradicts itself.** Split into two separately measured
  claims below, and the numbers re-taken in-tree after the first pair turned
  out to be `git archive` artifacts.

## The record-immutability cost of this revision, measured

This file is `Status: record` under `docs/`, so revising it to record the
2026-08-22 rulings trips doc-health's `record-immutability` critical — the cost
the "Why this file exists" section accepted deliberately. Measured in this git
tree, never from an exported copy, because this family reads git history and a
`git archive` export silently loses it:

- **Before the revision** (`--single-repo . --family record-immutability`, at
  `446291d`): **3 critical**, on `docs/domain-ontology-adoption-handoff.md`,
  `docs/domain-ontology-pilot-report.md`, and `ideation/cross-reference.md`.
  This file was NOT among them — its bytes still matched its capture blob,
  because PR #262's second commit `29e29d5` touched only the account-menu
  tasks.md and left this document alone.
- **After the revision**: **4 critical**, the fourth being
  `docs/archive-record-discrepancies.md — record document changed after
  capture`. Exactly the one predicted, and no others moved.

**The disposition was expected to silence that critical. IT DOES NOT, and this
was measured rather than assumed.** The plan for this revision called for
adding a `health/dispositions.yaml` entry and confirming the critical went
away. It does not go away, and any claim that it would be gate behaviour
nobody demonstrated:

- With the register edited and NO disposition: 4 critical.
- With a `record-immutability` / `openxFactory` /
  `docs/archive-record-discrepancies.md` disposition entry carrying a non-empty
  `cite`: **still 4 critical, and the two reports are byte-identical.**

The reason is in the code, and it is not a bug. `fam_record_immutability`
(`scripts/doc_health/families.py`) emits its findings unconditionally; nothing
in the family, the runner, or the renderer filters a live finding by
disposition. For record-immutability specifically — the family this revision
measured — the dispositions file is loaded once in `runner.main` into a set of
`(family, repo, path)` tuples, and that set is passed to exactly one consumer:
`report.uncited_resolutions`. The file's own header says so in as many words —
"a contested finding present in a previous report that is absent from the
current report is normally re-emitted as an `uncited-resolution` ERROR unless a
disposition here cites its resolution." That does not generalize repo-wide:
`neutrality_dispatch._load_dispositions` is a second loader, and there
`disposition_suppressions`/`is_suppressed` DO suppress live findings, keyed by
`(repo, path, content_sha256)` — a rejected candidate stays suppressed only
while its content digest is unchanged.

**So what a disposition actually buys, also measured end to end.** Against a
previous report carrying the four contested `record-immutability` findings, a
current run in which they are absent:

- with an empty dispositions file: **4 `uncited-resolution` ERRORs**, total
  errors 6 → 10, and 4 new regressions;
- with the four disposition entries present: **0 `uncited-resolution` ERRORs**,
  total errors back to 6, and 0 regressions.

A disposition is therefore a forward-looking receipt, not a mute button. It
does not stop this register's critical from being reported; it stops the
critical's eventual DISAPPEARANCE from being read as an unexplained resolution.
That is the right instrument for what happened here, and it is worth having —
but it belongs to a later run, not this one.

**Two facts about where it has to live, both of which put it outside this
commit.** `health/dispositions.yaml` is resolved as
`ctx.agg_root / "health" / "dispositions.yaml"` — the **aggregation** checkout's
file, not openxFactory's own `health/` directory, which has no such file. And
`ctx.agg_root` is `None` on a `--single-repo` run, so in the self-gate mode a
pull request actually uses, the dispositions file is never loaded at all and
could not suppress anything even in the case where it does apply. Writing the
entry is a change to a different repository, and the shared aggregation
checkout carries the sweep hazard this workspace's rules warn about, so this
commit does not touch it. The entry, ready to append when the aggregation repo
is next touched deliberately:

```yaml
- family: record-immutability
  repo: openxFactory
  path: docs/archive-record-discrepancies.md
  severity: critical
  disposer: openxFactory ratify gate
  adjudicated_by: archive-register-rulings (Claude Fable 5)
  date: 2026-08-22
  cite: >-
    Brett's in-session multiple-choice ruling round of 2026-08-22 over every
    open class in this register, executed the same day by
    `archive-register-rulings`. The edit is the register recording its own
    rulings, which is the revision path the document names for itself; the
    original text of every revised entry is left standing word for word with
    the ruling appended after it, per Brett's 2026-08-10 append discipline.
  rationale: >-
    Recorded for the run in which this finding disappears, not for this one:
    the critical is NOT suppressible and is reported live either way
    (measured — a run with this entry present is byte-identical to a run
    without it). Its purpose is to keep the eventual re-capture of this
    document from being re-emitted as an `uncited-resolution` ERROR.
```

**The honest conclusion for this register's own rule.** The critical is
visible, expected, named, and NOT suppressed. It should stay visible: a record
document that was revised ought to report that it was revised, and this section
is where a reader finds out why. What must never happen is the finding quietly
vanishing later with nobody able to say what resolved it — and that is the one
outcome the disposition above prevents.

## What the tooling does and does not enforce here

Measured rather than assumed, because "the gate forbids it" has been a false
excuse in this repository before.

The doc-health `record-immutability` family does **not** reach any file under
`openspec/`. It iterates `ctx.docs`, which `doc_health.corpus` builds from the
governed roots `contracts/`, `docs/`, `examples/`, `ideation/`, `templates/`
only, and within those it skips every document whose own header is not
`Status: record`. Two separate claims, kept separate because conflating them
produced a self-contradicting sentence in the first draft:

1. **Across the B1 proposal edits alone, the report is byte-identical.** A
   `--family record-immutability` run with the two edited lines present and a
   second run with them reverted produce the same bytes: the same three
   findings, all under `docs/` and `ideation/`. That is the claim about the
   `Status:`/`Ratified:` edits, and it is exact.
2. **Across the whole commit, the corpus-size lines move, because this document
   is new.** Adding a `Status: record` document to `docs/` moves the record
   count from 28 to 29 and the governance word total from 514,788 to 518,465,
   which drops canon share from 30.7% to 30.4% on the same 157,839 canon words.
   That is a corpus-size effect of the register itself, not of any
   archived-change edit, and it is not byte-identical to anything. The
   *severity* counts do not move: the full single-repo run reads 3 critical /
   7 error / 69 warning / 4 info on both sides, 0 new regressions, and the three
   criticals are the same pre-existing `docs/` and `ideation/` ones either way.

   Both baselines above were taken **in this git tree** (the document removed
   from the working tree and the README index line reverted, then restored),
   not from an exported copy. `record-immutability` and `staged-candidate-aging`
   both read git history, and a `git archive` export silently loses it — an
   export baseline reports 0 critical / 59 warning here, which is an artifact of
   the export, not a real before-state. Worth recording: it is the same shape of
   mistake as C2's, a measurement taken on an axis that does not carry the
   thing being measured.

Nor does any reader consult a proposal's `Status:` header.
`ideation_dashboard.generator` derives a change's status from its folder
location, and its ratifier from `.openspec.yaml` `ratified_by`/`ratifier` —
"deliberately NOT the `Ratified by:` proposal header". What the generator *does*
read out of proposal front matter is `code_surface` and `target_release`, by
key and not by position, which is why C1 and A1 are the items with a downstream
projection and B1's header lines are not.

So nothing mechanical blocked B1, and nothing mechanical would block C1–C7
either. What governs is the record-immutability *discipline* — Brett's
2026-08-10 append ruling, quoted with its constraint under B1 — and `efa42cf`'s
rule that an archived change must not be amended into disagreement with the
spec its own archival promoted. B1 satisfies the second and extends the first,
saying so. C1–C7 either require a judgement the record does not supply, or
would put invented content into a governed record.

## Corrected 2026-08-23 — twenty-seven archived ratification citations (`govern-openspec-corpus-membership` slice 5B)

Nothing above this line is edited. This section is an append, in the discipline
the register asks of everyone else.

**The authority.** Brett Heap ruled all six Open Questions of
`govern-openspec-corpus-membership` in an in-session multiple-choice round on
2026-08-23, and extended OQ-4 the same day after that change's slice-5A
adversarial review. The rulings are recorded question by question in
`openspec/changes/govern-openspec-corpus-membership/proposal.md`. Two of them
reach archived records, and slice 5B executes both:

- **OQ-4** — a `Ratified by:` line that names a person and a date rather than
  an approving OpenSpec change is substantively the record-citing form and is
  spelled wrong. The remedy is a **prefix respell**: `Ratified by:` becomes
  `Ratified:` and every byte after the colon is carried VERBATIM. Nothing is
  rephrased, added or dropped. The recommendation to cover the archived block
  with ONE ruling was rejected: each line is justified from its own record.
- **OQ-4's RULED extension** — a `Ratified by:` line whose named change id is
  the DOCUMENT'S OWN id passes `fam_ratified_provenance` only by
  self-reference. A change is not its own approving change. Same class, same
  remedy.
- **OQ-5** — a `review/ratification-*.md` record carrying `Ratifier:` and
  `Decision date:` gains a conforming `Ratified:` line derived from those two
  headers, which stay standing.

**Twenty-seven archived records, on TWO different grounds, kept apart on
purpose.**

| ground | count | what the finding was |
| --- | --- | --- |
| live CRITICAL, respell | 11 | `ratified-provenance`: "Ratified by: missing or does not resolve to an OpenSpec change" |
| live CRITICAL, added line | 1 | `ratified-provenance`: "ratified header carries no citation in either sanctioned spelling" |
| LATENT, respell | 15 | none — the family accepted the line by self-reference |
| **total archived records touched** | **27** | 12 findings cleared |

The fifteen latent ones **cleared no finding**. They emitted nothing before the
edit and they emit nothing after it; the census does not move by one on their
account. They are corrected because the ruling says the spelling is wrong, not
because anything reported them. Saying "27 corrections, 27 discharges" would be
exactly the overstatement `govern-openspec-corpus-membership` exists to make
impossible.

A twenty-eighth document was edited in the same slice and is deliberately NOT a
register entry: `add-hermes-customer-subject-runtime-contract` is an ACTIVE
change, so no archive rule is engaged. It is named here so a reader who counts
28 in the commit knows why 27 appear below.

**The per-record justifications live in each change's own `tasks.md`**, as a
trailing `## Bookkeeping correction (2026-08-23, ...)` section — twenty-seven
of them, one per record, each naming the record that justifies its line. That
placement is deliberate and it is the correction slice 5A had to make to
itself: a consolidated table is a fine index and a poor substitute, because a
reader of one archived change should not have to know that a different
document holds the answer. The table below is the index.

| # | archived change | ground | the record that justifies its line |
| --- | --- | --- | --- |
| 1 | `2026-07-30-add-ontology-stewardship-hardening` | CRITICAL | Brett's 2026-07-30 direction quoted on the line ("yes, fold it into that hardening pass"), written by commit `5667de5` of the same day |
| 2 | `2026-08-04-adopt-neutral-utility-pack` | CRITICAL | Brett's 2026-08-03 approval of the DTN-018/019/021 scope quoted on the line, written by commit `2c53b27` of the same day |
| 3 | `2026-08-06-add-opendox-project-header` | CRITICAL | Brett's 2026-08-06 "ratify both and realize them in order", quoted on the line and again in the body of commit `8121f5f` |
| 4 | `2026-08-06-add-project-scoped-selection` | CRITICAL | Brett's 2026-08-06 "ratify exit 1 and realize it", quoted on the line and again in the body of commit `db3e00c` |
| 5 | `2026-08-07-add-project-merged-projection` | CRITICAL | the same 2026-08-06 instruction, on this change's own line and in the same commit `8121f5f`, which realized it |
| 6 | `2026-08-07-add-register-edit-lane` | CRITICAL | Brett's 2026-08-06 "automate that step 2" directive, quoted on the line and echoed in commit `23c0f6c` |
| 7 | `2026-08-08-add-openxwallet` | CRITICAL | Brett Heap's 2026-08-07 ruling "declared and capping authority", recorded by commit `c5b41ca` |
| 8 | `2026-08-09-add-project-visible-set` | CRITICAL | Brett's 2026-08-07 view-selector ruling (topic `dashboard-project-scoping` D19), recorded by commit `2eca313` |
| 9 | `2026-08-09-add-repository-lens` | CRITICAL | Brett's 2026-08-07 lens observation and instruction (D21), recorded by commit `864bb12` |
| 10 | `2026-08-13-add-session-notebook-reconciliation` | CRITICAL | Brett's 2026-08-10 "fix the session teardown notebook gap", quoted in commit `1b964ba` (PR #163) |
| 11 | `2026-08-15-add-subject-overlay-contract` | CRITICAL | Brett Heap's 2026-08-15 confirmation of the three OQ-1 positions, recorded by commit `9744fbe` |
| 12 | `2026-08-22-add-roster-device-admission-surface` (`review/ratification-2026-08-19.md`) | CRITICAL | the document's own `Decision date: 2026-08-19` and `Ratifier: Brett (repository owner)` — derived, not invented |
| 13 | `2026-07-23-add-hermes-domain-overlay-contract` | latent | the 2026-07-23 user approval named on the line, carried by archive commit `5ad71a7` of the same day |
| 14 | `2026-07-23-adopt-subject-tenant-domain-vocabulary` | latent | the 2026-07-23 user approval named on the line, recorded by commit `7d47b0a` of the same day |
| 15 | `2026-07-24-add-client-layer-tuning-contracts` | latent | the 2026-07-24 user approval named on the line, carried by archive commit `95ac6dd` of the same day |
| 16 | `2026-07-24-add-hermes-domain-content-manifest` | latent | the 2026-07-24 user approval named on the line, carried by archive commit `6785435` of the same day |
| 17 | `2026-07-24-add-omnigent-domain-overlay` | latent | the 2026-07-22 user approval named on the line, recorded by commit `aa636e1` of that same 2026-07-22 |
| 18 | `2026-07-29-add-crystallizer-contracts` | latent | Brett's 2026-07-29 approval, recorded by commit `57b5e70` of the same day |
| 19 | `2026-07-29-add-pattern-ledger` | latent | Brett's 2026-07-29 approval, recorded by commit `1842e1c` of the same day |
| 20 | `2026-07-30-add-capability-steward` | latent | Brett's 2026-07-29 approval, recorded by commit `aa04319` of that same 2026-07-29 |
| 21 | `2026-07-30-add-deployment-handoff-boundary` | latent | Brett's 2026-07-29 approval, recorded by commit `c06dc0f` of that same 2026-07-29 |
| 22 | `2026-07-30-add-domain-ontology-layer` | latent | Brett's 2026-07-28 approval, recorded by commit `e32c690` of that same 2026-07-28 |
| 23 | `2026-08-01-add-dashboard-repo-selector` | latent | Brett's 2026-07-29 approval, recorded by commit `c14cecc` of that same 2026-07-29 |
| 24 | `2026-08-01-add-workbench-branch-sessions` | latent | Brett's 2026-07-26 approval, recorded by commit `6b59614` of that same 2026-07-26 |
| 25 | `2026-08-05-add-neutrality-drift-lane` | latent | Brett's 2026-08-04 approval (PR #64 review), recorded by commit `5a4747c` of the same day |
| 26 | `2026-08-05-adopt-neutral-tooling-home` | latent | Brett's 2026-08-03 approval, recorded by commit `6a90bd6` of the same day |
| 27 | `2026-08-06-add-consent-instrument` | latent | Brett's 2026-08-03 approval, recorded by commit `4ebb742` of the same day |

Every commit named above is dated the day its citation line names. That
agreement was checked commit by commit, not assumed, and it is what makes each
line's approver-and-date a fact of the record rather than a claim on the page.

**How the original line survives, given B1's mechanical problem.** B1 states it
and it applies unchanged here: `doc_health.corpus.STATUS_RE` is
`^Status:\s*(.+?)\s*$` and swallows any trailing annotation, so an append on a
single-valued header is impossible. Each of the twenty-six respells is
therefore an **in-place overwrite and an extension of Brett's 2026-08-10 append
ruling, named as one**, exactly as B1 was. The original line is preserved in a
stronger form than a re-quotation would give: a respell changes only the three
bytes ` by`, so the original reads exactly as the line now on the page with
`Ratified by:` in place of `Ratified:`, and each travelling note says so. That
identity was asserted mechanically at the edit rather than trusted — the bytes
after the prefix were compared before and after on all twenty-six, and
`git diff --word-diff` shows one changed token per file and nothing else. Entry
12 is not a respell but a pure addition of one line, so it honours the
2026-08-10 ruling literally rather than extending it.

**What did NOT change.** No `Status:` value moved. The archived population still
reads 44 `Status: ratified`, 0 `draft` and 44 headerless over 88 archived
proposals, counted in-tree at the executing commit — the same split the
2026-08-22 rulings left, over two more archived changes than existed then. What
moved is the spelling of citation lines: B1's 2026-08-22 count of twenty-nine
`Ratified by:` and nine `Ratified:` among the archived ratified proposals now
reads **3 and 41**. B1's counts are left standing as the measurement they were.

**The three that keep `Ratified by:`, measured and deliberately out of the
ruling.** `2026-07-30-add-omnigent-semantic-wiring`,
`2026-07-30-add-ontology-term-lifecycle-enforcement` and
`2026-07-30-publish-semantic-kernel` each name `add-domain-ontology-layer` —
another change, in passing prose, not themselves — so they are neither
resolution failures nor self-citers. Two ACTIVE proposals sit in the same
position (`add-shared-identity-seeds`, and `add-identity-brokering` whose line
names a record path that resolves). Respelling any of the five is not ruled.
They are named so a later reader who counts by eye knows which set was ruled
and which was measured.

**The record-immutability cost of this append, measured.** Editing this
`Status: record` document trips `record-immutability` — the cost the "Why this
file exists" section accepted. That critical was ALREADY standing before this
append, from the 2026-08-22 revision, and this append does not add a second
one: the whole-repo single-repo run reads **4 critical / 8 error / 68 warning /
4 info** both before and after, 0 new regressions, with
`docs/archive-record-discrepancies.md` among the four on both sides. Measured
in this git tree, not assumed, because the family reads git history. Two lines
of that report DO move, and they are this section's own bulk rather than any
finding: the `record` stage's word total rises 32,260 → 33,994 and canon share
reads 31.4% against 31.5%, on unchanged canon words (169,417). That is the
corpus-size effect the register recorded for itself once before. The
dispositions entry drafted in "The
record-immutability cost of this revision, measured" covers this document and
still applies; as that section proves, it does not silence the live critical
and is not expected to.

**Nothing under `openspec/` is read by doc-health.** The twenty-seven proposal
and review edits and the twenty-seven travelling notes all live under
`openspec/changes/`, outside `corpus.GOVERNED_ROOTS`, so they move no
whole-repo finding at all. The scoped scan set that `govern-openspec-corpus-membership`
defines DOES read them, and there the slice takes `ratified-provenance` from 12
CRITICAL to 0.

## Corrected 2026-08-23 — forty-three archived proposal headers, and C2's successor (`govern-openspec-corpus-membership` slice 5C)

Nothing above this line is edited except entries A2 and C5, each of which
gains a dated supersession addendum under its own text — A2 at the express
direction of task 5D.2a, C5 at the express direction of a same-day ruling
recorded as task 5C.3, both of `govern-openspec-corpus-membership`; both
entries' original text stands word for word. Everything else here is an
append, in the discipline the register asks of everyone else.

**C2's CLASS DECISION IS SUPERSEDED. C2's per-record FINDINGS ARE NOT.** This
is the whole of what changed, and the two halves must not be run together.

C2 closed on 2026-08-22 with "backfill the seven true anomalies where the
records allow, and only there" and, in as many words, "**The forty-six-wide
option was not taken**". On 2026-08-23 Brett ruled OQ-6 of
`govern-openspec-corpus-membership` in an in-session multiple-choice round and
**DEPARTED from that change's own recommendation**: backfill ALL forty-seven
headerless proposals, forty-four archived and three active. No grandfather, no
contract date, no reduced-severity class. The wide option is now taken. The
ruling is recorded question by question in
`openspec/changes/govern-openspec-corpus-membership/proposal.md`, and it names
this supersession itself — "This ruling supersedes the class half of C2's
2026-08-22 ruling, and says so."

C2's execution table is EVIDENCE, NOT A DECISION, and the append discipline
protects it. Every per-record finding it made is re-verified by slice 5C and
stands unaltered:

| C2's finding | still true? | what 5C did with it |
| --- | --- | --- |
| `add-propose-verb`: "Nothing. Its front matter, its whole directory, its created and archive commits, and its README row name no ratifier and no ratification date." | YES, re-verified | not cited; the archive act is cited instead |
| `add-staging-workbench`, `add-workbench-bullseye-and-create`, `add-wheel-action-verbs`: an `origin:`-nested `approved_by`/`approved_on` pair recording permission to author, six to eleven days before archive, plus a Brett-named task sign-off — "Two near-misses on the same record is a reason for care, not a reason to pick one" | YES, re-verified | NEITHER near-miss cited on any of the three; the archive act is cited instead |
| `add-workbench-integrated-editor-chat`: "a recorded decision AGAINST writing a status value", verified deliberate as A2 | YES, re-verified and quoted in full in the change's own note | superseded on its own terms by 5D.2a; see the A2 addendum above |
| the thirty-nine pre-convention headerless proposals "were out of scope for this ruling and stay exactly as they were" | YES — that was true of C2's ruling | they are IN scope for OQ-6's, and thirty-eight of the thirty-nine are backfilled here |

**What C2 did not have, and what makes the wide backfill possible without
inventing anything.** Two things arrived after 2026-08-22. First, OQ-6's
ruling itself. Second, and the load-bearing one, the **archive-act
derivation**: `2026-08-22-add-doxbench-editing-phase-b/proposal.md` cites the
archive act as its ratification on the reasoning `bdd09c2` records — "a change
whose spec deltas have PROMOTED is ratified by construction". That derivation
does not read any packet approval into meaning it never had; it reads the
ARCHIVE, which is a governance act, and the promotion it performed, which is
checkable in `openspec/specs/`. C2 was hunting for provenance on the packet and
correctly found none on five records. The archive act was never on that list.

**Forty-four archived documents in scope, forty-three corrected directly, one
stopped and reported — then resolved the same day by a dedicated ruling.**

| | count |
| --- | ---: |
| archived headerless proposals in the ruled scan set | 44 |
| corrected — `Status: ratified` plus one `Ratified:` citation | **43** |
| of those, derivation route (a): an explicit ratification act on the record | 11 |
| of those, derivation route (b): the archive act and its promotion | 32 |
| STOPPED AND REPORTED — no header written at this pass | 1 |
| of the one stopped, later corrected under a dedicated ruling — `Status: draft`, uncited | **1** |
| left stopped after the dedicated ruling | **0** |

Every one of the 43 clears the three-way floor on axes measured through
`doc_health.families` before the line was written, never assumed: **30** on
date plus a resolvable record path, **10** on approver plus date plus a record
path, **2** on approver plus date, **1** on date alone. Of the twelve that
clear the approver axis by a mechanical regex match, only NINE attribute the
ratifying act to a named ratifier; the other three — `adopt-avatar-client-lab-candidates`,
`implement-avatar-client-lab` and `qualify-avatar-brokered-call-feasibility` —
take derivation route (b) and match "by Brett" only inside quoted prose their
own citation lines disclaim as something else (a PR-merge Tier-1 approval, a
realization-gate disposition, an archive-hold acceptance), not as the
ratifying act itself. Four carry a
ratification date EARLIER than their own archive folder date — by 1, 4, 23 and
25 days — and each says so on its own line rather than smoothing the date to
match the folder.

**THE ONE STOP-AND-REPORT: `enable-live-openxfactory`.** Reported by name, with
what its record does and does not carry, exactly as OQ-6 requires of a document
that cannot support a header.

- What it carries: an archive act that is unambiguously Brett's — he authored
  and merged PR #28, "Archive live factory OpenSpec change", at
  2026-06-26T05:55:09Z, over a merge-readiness report reading "Decision: READY"
  with all six council reviewers Pass, and a phase-9 closeout reading "Decision:
  READY TO ARCHIVE". Also an `.openspec.yaml` origin pair
  (`approved_by: Brett`, `approved_on: 2026-06-26`).
- What it does not carry: any ratification act, in any wording, anywhere on the
  record. The origin pair is permission to author, which C2 ruled is not a
  ratification.
- Why route (b) cannot rescue it, and this is the decisive fact: **its archive
  act promoted nothing.** PR #28's own body records the command as
  `openspec archive enable-live-openworkflow-factory --skip-specs -y`, and its
  merge-readiness report states the reason in words — "The archive is
  intentionally performed with `--skip-specs` because this change recorded
  infrastructure/runtime proof and retained the delta specs as archived design
  evidence rather than promoting them into standing product specs." The single
  leg the by-construction derivation stands on is affirmatively negated by the
  record itself. It is the only archived change in the corpus in that position,
  as **C5 of this register independently found**: "It is the only archived
  change in the corpus with an unpromoted delta — its two 2026-06-26 siblings
  both promoted".
- And C5 already ruled the folder, on 2026-08-22, in terms that reach this
  slice directly: "leave it recorded as legacy … **No file in
  `archive/2026-06-26-enable-live-openxfactory/` was changed by this round, and
  none should be by a later one absent a governance act that actually promotes
  the capabilities.** This entry is closed as RULED — legacy, not as a defect
  awaiting repair, so a future sweep that rediscovers the unpromoted deltas
  should read this line and stop rather than re-open the question." OQ-6
  superseded C2's class decision. It did not reach C5. So this slice read that
  line and stopped, which is what it says to do.
- Consequence, stated rather than left to be discovered at a gate: this
  document is a live `status-validity` ERROR and it is a NON-ZERO result for
  task 5D.2 of `govern-openspec-corpus-membership`. It blocks that merge until
  Brett rules it, and it must not be waved through as a known exception,
  because a known exception is the grandfather OQ-6 refused re-entering by the
  back door.
- **RESOLVED the same day.** RULED 2026-08-23 (Brett, in-session), recorded as
  task 5C.3: backfill `Status: draft` too. C5's no-edit ruling above is
  SUPERSEDED, narrowly and for this one header line only — the freeze on the
  four capabilities otherwise stands, they stay unpromoted, and no other line
  of the folder is touched. `draft` needs no citation: the promoted rule
  requires one only for `Status: ratified`, and "absent such backing the
  document MUST carry `draft` or lower status". C5 gains a dated 2026-08-23
  supersession addendum under its own text, above, with C5's original text
  standing byte-for-byte; the change's own `tasks.md` quotes C5's ruling in
  full and leaves it standing. This document is no longer a live
  `status-validity` ERROR and no longer a NON-ZERO result for 5D.2.

**Where the per-record justifications live.** Not here. Each of the 43 archived
packets carries its own as a trailing "## Bookkeeping correction" section in
its own `tasks.md` — phase-b's and 5B's shape — naming the derivation route,
the record cited, the floor axes measured, and the real line numbers the two
new lines occupy. Nine carry an extra paragraph where the record needed one:
the four C2 re-verifications above; two realization-disposition cautions
(`implement-avatar-client-lab` and `qualify-avatar-brokered-call-feasibility`,
where Brett's named decision is a realization disposition or an archive-hold
lift and the citation says so rather than calling it a ratification — the same
gap C2 flagged for `add-lens-gate-verbs`); two corroboration-not-citation
cautions (`adopt-avatar-client-lab-candidates`' sign-off on the candidate's open
questions, and `add-document-cataloging`'s Brett gate on a different artifact);
and one where promotion and archive fall a day apart
(`reconcile-domain-neutral-and-engineering-spec-ownership`).

**The scan-set census, same helpers, same globs, same four families as 5B.**

| | before 5C | after 5C | delta |
| --- | --- | --- | --- |
| scan set documents | 124 | 124 | 0 |
| `status-validity` | 46 ERROR | **2 ERROR** | −44 |
| `ratified-provenance` | 0 | **0** | 0 |
| `standard-backing` | 0 | 0 | 0 |
| `succession-integrity` | 0 | 0 | 0 |
| **total** | **46** | **2** | **−44** |
| of which on ACTIVE documents | 2 | 2 | 0 |

`ratified-provenance` reads 0 on BOTH sides, and that is the number to watch
rather than to assume: 43 documents newly read `Status: ratified`, so 43
documents newly entered that family's scope, and every one of them carries
exactly one citation clearing the floor. A backfill that wrote statuses without
citations would have moved this row from 0 to 43. The 44th,
`enable-live-openxfactory`, reads `Status: draft`, which `ratified-provenance`
never inspects. The two remaining ERRORs are the two headerless ACTIVE
MedxChart and MedxPractice proposals, which are another session's in-flight
work and are untouched by this change.

**The record-immutability cost of this append, measured.** Editing this
`Status: record` document trips `record-immutability` — the cost the "Why this
file exists" section accepted. That critical was ALREADY standing before this
append, and this append does not add a second one: the whole-repo single-repo
run reads **4 critical / 8 error / 68 warning / 4 info, 0 new regressions**
both before and after, with `docs/archive-record-discrepancies.md` among the
four on both sides. Measured in this git tree rather than assumed, because the
family reads git history. Exactly TWO lines of that report differ between the
two runs, compared line by line rather than summed, and neither is a finding:
the `record` stage's word total rises 33,994 → 36,494 and canon share reads
31.2% against 31.4%, on unchanged canon words (169,417). That is this
section's own bulk (including its C5 addendum and the adversarial spot-check's
corrections, folded into the same commit) and nothing else — the same
corpus-size effect the register recorded for itself at the 2026-08-22
revision and again at 5B. Re-verified a second way: the intermediate
33,994 → 35,916 step this slice's own commit produced, and the further
35,916 → 36,494 the fix-lap corrections added on top of it, were each
measured before being combined — the fix lap moved no finding, only this
one word count, confirmed by comparing the two reports line by line.

**Nothing under `openspec/` is read by doc-health.** All 44 proposal edits
(43 backfilled directly plus `enable-live-openxfactory`'s dedicated-ruling
backfill) and all 44 travelling notes live under `openspec/changes/archive/`,
outside `corpus.GOVERNED_ROOTS`, so they move no whole-repo finding at all —
verified by running the whole-repo report after the proposal-and-note commit
and before this append, and reading the same four numbers. The scoped scan
set that `govern-openspec-corpus-membership` defines DOES read them, and
there the slice takes `status-validity` from 46 to 2.

## Addendum 2026-08-23 — the per-domain lifecycle-header populations the enforcement surfaces (`govern-openspec-corpus-membership` slice 5D, M1)

**Why this addendum exists.** Slice 5D lands the enforcement: the four
lifecycle families read the OpenSpec scan set. openxFactory's own scan set is
discharged and the 5D.2 gate reads zero. The nine DomainxFactory repos the
aggregation pins are a different matter — their own OpenSpec packets carry a
substantial pre-existing lifecycle-header population that the enforcement now
SURFACES, in the aggregation-root (`--repo-root`) scope CI runs. An adversarial
review lap raised that as a reason to hold the change. **Brett ruled the
opposite on 2026-08-23: land it.** The findings are true, surfacing them is the
tool working, and each domain owes its own discharge under its own governance.

The population is therefore **advisory by ruling**, not silenced and not
grandfathered: no contract date, no reduced-severity class, no scan-set
exclusion. What is ruled is only WHO discharges it and WHEN — the owning
domain, under its own change process, not this change. This addendum is the
durable enumeration, written here for the same reason this whole register
exists: the finding must not evaporate when
`govern-openspec-corpus-membership` archives.

### How this was measured, and why the numbers differ from the review's

The review's numbers (~27 CRITICAL / 76 ERROR) came from the LOCAL domain
checkouts, which are ahead of what the aggregation repo pins. The table below
was re-measured **at the aggregation repo's pinned submodule SHAs**
(`git -C <aggregation> ls-tree -r origin/main`, the current canonical pins), by
building a scratch layout of ten clones each detached at its pinned commit and
running `runner.build_context` + the four families over it — the same code path
CI runs, not a replay script. **Every pinned SHA was reachable locally**, so no
row is a substitute state. Only findings whose path is in that repo's own
lifecycle scan set are counted; governed-corpus findings, which the enforcement
does not move, are excluded.

| repo | pinned SHA | scan-set docs | CRITICAL | ERROR | shape |
| --- | --- | --- | --- | --- | --- |
| openxFactory | `ded0826` (this change's base) | 126 | 1 | 3 | the four stragglers slice 5D itself discharges — **0 / 0 at the branch tip** |
| AdxFactory | `45eaf55` | 2 | 0 | 1 | 1 missing status header (archived) |
| HealthLinc | `76008ec` | 1 | 1 | 0 | 1 unresolvable `Ratified by:` (archived) |
| LedgerxFactory | `f9488ae` | 27 | 0 | 26 | 26 missing status headers (24 archived, 2 active) |
| MedxChart | `68d2f1f` | 0 | 0 | 0 | no OpenSpec packets pinned |
| MedxEHR | `9e23424` | 1 | 1 | 0 | 1 unresolvable `Ratified by:` (archived) |
| MedxFactory | `f3d9550` | 25 | 13 | 1 | 13 unresolvable `Ratified by:`, 1 missing header (all archived) |
| MedxPractice | `d8d7319` | 0 | 0 | 0 | no OpenSpec packets pinned |
| OpsxFactory | `7908016` | 76 | 14 | 39 | 8 unresolvable `Ratified by:`, 6 uncited `ratified` review records, 16 missing headers, 23 free-form statuses (45 active, 8 archived) |
| codexFactory | `e61f24d` | 27 | 7 | 8 | 7 unresolvable `Ratified by:`, 8 missing status headers (14 archived, 1 active) |
| **total** | | **285** | **37** | **78** | |

**Domain subtotal, excluding openxFactory: 36 CRITICAL / 75 ERROR over 159
scan-set documents in seven repositories.** Higher than the review's count
because the pinned states differ from the local checkouts, in both directions;
the pinned figure is the one that binds, because the pins are what CI assembles.

### The follow-ups, one per domain, owed to that domain's governance

Each is a named, durable item. None is discharged by
`govern-openspec-corpus-membership`, and none is dispositioned away by it.

- **FU-DOM-ADX — AdxFactory (1 ERROR).** One archived proposal,
  `2026-07-23-add-adx-object-model`, carries no `Status:` header. Derivable
  from its own archive record; a one-header backfill on the archived-record
  route.
- **FU-DOM-HEALTHLINC — HealthLinc (1 CRITICAL).**
  `2026-08-06-add-one-patient-intake-experience` carries a `Ratified by:`
  naming no resolvable OpenSpec change. This is exactly the OQ-4 shape: a
  substantively sound citation in the wrong spelling. The remedy that change
  ruled — rewrite to the sanctioned record-citing `Ratified:` where no
  approving change exists to name — applies unchanged.
- **FU-DOM-LEDGERX — LedgerxFactory (26 ERROR).** The largest
  missing-header block outside openxFactory: 24 archived and 2 active
  proposals with no `Status:` at all. Same shape and same remedy as this
  change's own slice 5C — derive each header from the packet's own record,
  report by name where the record supports none.
  **DISCHARGED 2026-08-24** (LedgerxFactory PR #22, merged `a645858`;
  aggregation pin `4279472`), the OpsxFactory precedent applied: the 26
  turned out to be one shape in two variants — 15 packets carrying a LOCAL
  front-matter vocabulary (`governance_status:`/`ratified_by:`/`ratified_on:`)
  invisible to the checker, each given a conforming `Ratified:` line derived
  from its own front matter with dates kept distinct from folder dates, and
  11 whose act lived only in the archive commit's subject, derived
  archive-act-where-deltas-promoted (all 11 promotion targets verified).
  Zero stop-and-reports. The habit was live (both active packets carried
  it), so the convention is codified in LedgerxFactory's
  `docs/packet-lifecycle-headers.md`. Scan set reads 0/0 at `a645858`.
- **FU-DOM-MEDXEHR — MedxEHR (1 CRITICAL).**
  `2026-08-06-add-patient-reconciliation-overlay`, the OQ-4 spelling shape.
- **FU-DOM-MEDXFACTORY — MedxFactory (13 CRITICAL, 1 ERROR).** Thirteen
  archived proposals with unresolvable `Ratified by:` lines — the root-truth
  and terminology series — plus one missing header
  (`2026-08-11-add-root-truth-index-embedding`). All archived, so all on the
  archived-record route.
- **FU-DOM-OPSX — OpsxFactory (14 CRITICAL, 39 ERROR).** The largest
  population and the only one whose bulk is ACTIVE (45 of 53). Three distinct
  shapes, and they do not share a remedy: eight proposals with unresolvable
  `Ratified by:` lines; six `review/ratification-*.md` records carrying
  `Status: ratified` with no citation in either sanctioned spelling; and
  thirty-nine status defects concentrated in the `add-cloudpc-worker-fleet-
  management`, `add-endpoint-management-workflow` and
  `add-managed-node-inventory` packets, where `review/` records use a local
  vocabulary (`complete`, `RATIFIED FOR IMPLEMENTATION`,
  `**RATIFIED FOR DEPENDENT DETERMINISTIC CONSUMPTION ONLY**`) that no
  taxonomy value covers. That last block is the one worth flagging to
  OpsxFactory first: it is a live authoring convention, not a legacy
  backlog, so it will keep producing findings until the convention changes.
  **DISCHARGED 2026-08-24** (OpsxFactory PR #88, merged `87ca884`;
  aggregation pin `fd60112`), under Brett's in-session adopt-and-discharge
  ruling: OpsxFactory adopted the neutral taxonomy and citation grammar, all
  55 findings at its tip (the population had grown 53 → 55 since this
  entry's pinned measurement, plus a 56th found in the doing — an
  out-of-window `Status:` line, the roster-device shape in a second repo)
  were discharged by the established per-shape mappings with zero
  stop-and-reports, and the convention is codified in OpsxFactory's
  `docs/packet-lifecycle-headers.md` so the live habit stops regenerating
  findings. The four lifecycle families read 0 CRITICAL / 0 ERROR over its
  78-document scan set at `87ca884`.
- **FU-DOM-CODEX — codexFactory (7 CRITICAL, 8 ERROR).** Seven unresolvable
  `Ratified by:` lines and eight missing headers, fourteen of the fifteen
  archived.
- **MedxChart and MedxPractice** pin no OpenSpec packets and owe nothing here.
  Their two ACTIVE headerless proposals, named repeatedly in this change's
  task record, live in the openxFactory tree as
  `create-medxchart-overlay-boundary` and
  `create-medxpractice-overlay-boundary` and were discharged by slice 5D's
  own straggler commit — they are not domain-repo items.

### What this addendum does NOT claim

It does not claim these are new defects: every one predates the enforcement
and was invisible only because `openspec/` was outside the governed corpus.
It does not claim a date by which any domain must discharge its population —
that is the domain's to set. And it does not disposition any of them: a
`health/dispositions.yaml` entry would suppress a neutrality finding, not a
lifecycle one, and suppressing them is precisely what the ruling declined to
do.
