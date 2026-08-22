# Archived-Change Record Discrepancies — Open Bookkeeping Register

Status: record
Kind: reference
Disposition: MIXED — one item is corrected and named as such; the remaining
seven are recorded OPEN and none of them is authorized by this document. Each
needs either a Brett ruling or an OpenSpec change to close it.
Owner: openxFactory (the `document-lifecycle` and `release-realization`
capabilities, and the archived change directories under
`openspec/changes/archive/`).
Opened: 2026-08-22, re-derived over all 86 archived changes; revised the same
day after an adversarial review lap (see "What this register got wrong first").

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

After B1, the archived population reads: 39 `Status: ratified`, 1
`Status: draft` (C7), and 46 with no `Status:` header at all (C2).

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

### A5 — the two repairs PR #253 made at its own gate

`split-ideation-book-per-repo`'s unticked 4.3 is ticked with an inline note,
and the lens pair (`add-repository-lens`, `add-project-visible-set`) carry
their `.openspec.yaml` staged-origin declarations. Both confirmed present.

## Open — enumerated, untouched, needing a ruling

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

### C4 — twenty-one archived changes are pre-contract-legacy origin warnings

Measured on a live `--family proposal-origin` single-repo run: 2 error, 30
warning. Twenty-one of the thirty warnings are archived changes; the other nine
are active. All are reported at WARNING by design ("never fabricated, never a
regression-gate break"). Listed here only so the ERROR pair in C3 is not
mistaken for the whole population. No action proposed.

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
