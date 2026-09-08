---
code_surface: openxFactory (`scripts/doc_health/corpus.py` — one added function, `active_change_ids`, a sibling of `change_ids` returning ACTIVE change ids only, with the reason the two sets must stay distinct in its docstring; `scripts/doc_health/families.py` — `fam_location_conformance` computes the per-repo active-id map from `ctx.repo_paths` it already walks and the staged-exit arm reads that map instead of `ctx.change_ids`, three lines plus a comment, no other arm touched; `tests/doc-health/test_families.py` — two added regression tests, one proving an archived-only citation is silent and that the union still resolves the id, one proving a document citing BOTH an archived and an active change is reported against the ACTIVE one, each carrying the negative-then-positive pairing this suite requires and the second pinning the action line; `tests/doc-health/test_modified_block_currency_self_gate.py` — one added row in `_LEDGER_SUBJECTS`, naming this packet's own MODIFIED block as a subject that family reports, because that gate compares its named set with `==` and a new MODIFIED block anywhere in the active set falls it due by design. NO change to `corpus.change_ids` itself, to `Context`, to `runner.py`, to `tests/doc-health/conftest.py`, to the family registry, to the family enumeration or its numerals, to any other family's basis, to the report schema, or to any threshold. Also four GOVERNANCE-TEXT edits carrying no code: `Status: draft` added to `contracts/domain-ontology/examples/pilots/codex/README.md`, `contracts/domain-ontology/examples/pilots/medx/README.md` and `openspec/changes/archive/2026-08-25-fix-abandoned-session-cleanup-terminal-states/proposal.md`, `Status: open (operational)` replaced by `Status: draft` in `docs/notebooklm-sync-open-item.md`, plus one appended addendum section in `docs/archive-record-discrepancies.md` registering the archived-record edit, and one README active-changes entry.)
target_release: implemented — the openxFactory main line. This surface cuts NO contract bundle, measured rather than assumed: every path this change touches was grepped against all 48 `contracts/releases/*.digests.yaml` inventories and NONE is a member — not the two pilot READMEs (no inventory carries any `domain-ontology` path at all), not `docs/notebooklm-sync-open-item.md`, not `scripts/doc_health/corpus.py`, `families.py` or `tests/doc-health/test_families.py` (no inventory carries any `doc_health` path), so no schema moves, no digest set changes, and no release tag is owed. The archive gate is therefore merge-plus-green on main, following `add-duplicate-packet-check` and `govern-openspec-corpus-membership` exactly: `python3 -m pytest tests/doc-health` green, `OPENSPEC_TELEMETRY=0 openspec validate --all --strict` green, and a doc-health single-repo run whose severity counts move by exactly the amount § What was measured predicts and in no other line. THE REALIZATION RIDES IN THE PROPOSING PULL REQUEST, on the `supersede-lost-pin-baseline` precedent: the code is three lines and two tests, the backfills are one line each, and splitting them from the packet that argues for them would put the argument and the act in different reviews. The change therefore ships ACTIVE and archives only after the merge.
Status: ratified
Ratified: 2026-08-28 by Brett — his merge-and-archive ruling of 2026-08-28, put as a multi-choice by the orchestrating session and answered by selection, relayed the same day: OD-5's measured departure from the ruled `draft` APPROVED as taken, and BOTH pull requests directed to merge on green — so the packet archives on merged-plus-green, which is the act this line cites. The selections as relayed are the record; no verbatim wording reached the authoring session, so none is quoted, and the two voices are kept apart rather than merged into one quotation. THE CITATION COVERS THAT ONE ACT AND NOTHING ELSE — OD-2, OD-3 and OD-4 were not put to him, stand as authored, and remain flagged in § Orchestrator decisions. The header moved AT THE ARCHIVE rather than at filing, and § 6.3 is why it could not be left: `promotion_fidelity.PRE_RATIFICATION` is `{brainstorm, staged, draft}`, so an archived proposal reading `draft` has its deltas discounted as design evidence — which would have silently dropped this packet's own MODIFIED block, the very defect § 1.4 measured against somebody else's archived record. No approving OpenSpec change exists to name, so the citation takes the record spelling `sanction-ratified-record-spelling` sanctioned for exactly that case, and clears its three-way floor on all three axes: approver (`by Brett`), date (`2026-08-28`), and a resolvable record path (`tasks.md` § 6.1, which records the selections).
Proposed: 2026-08-28
---

# Proposal: clean-doc-health-floor

## Why

Two of the errors standing on this repository's doc-health floor are not
reports of anything wrong with the repository. One is a set of four documents
whose headers were never written. The other is a check demanding an act that
cannot be performed.

`status-validity` reports FOUR errors, and all four are missing or free-form
`Status:` headers — three documents that predate the convention and one
archived packet that a one-time sweep missed by a day. Nothing is in dispute
about any of them; they were left because the sweep that would have taken them
had already closed.

`location-conformance` reports an error against
`ideation/staging/avatar-pilot-hardening/avatar-pilot-hardening.md` for citing
`implement-avatar-client-lab`, and tells the operator to "move selected
material into the proposal supporting-docs folder". That proposal ARCHIVED on
2026-08-04. An archived packet is closed and immutable — the folder cannot
receive the material, and the remedy names an act nobody can perform. The
finding is not wrong that the document cites a change; it is wrong that
anything can be done about the change it names.

Both are floor, not signal, and floor teaches operators to stop reading the
report.

## What was measured

Every number here was measured on 2026-08-28 in a fresh worktree off
`origin/main` at `6612d323`, and re-measured after each slice rather than
predicted.

**THE BASELINE.** `python3 scripts/doc-health.py --single-repo .` reports
**5 critical, 11 error, 41 warning, 11 info**, 0 new regressions.
`python3 -m pytest tests/doc-health -q` reports **1249 passed, 0 failed**
under `set -o pipefail`.

**W1 — the four documents, and the value each record supports.** The
`status-validity` errors are exactly:

| Document | Reported as | Value backfilled |
| --- | --- | --- |
| `contracts/domain-ontology/examples/pilots/codex/README.md` | missing status header | `draft` |
| `contracts/domain-ontology/examples/pilots/medx/README.md` | missing status header | `draft` |
| `docs/notebooklm-sync-open-item.md` | free-form status `'open (operational)'` | `draft` |
| `openspec/changes/archive/2026-08-25-fix-abandoned-session-cleanup-terminal-states/proposal.md` | missing status header | `ratified` + citation (see OD-5) |

The two pilot READMEs are named — as a directory and a count, "two pilot
`README.md`s" — in `govern-openspec-corpus-membership`'s own read-back
(`tasks.md:2252-2258`), which recorded them together with
`docs/notebooklm-sync-open-item.md` as "governed-corpus documents that predate
this campaign and are outside its scope". They are this packet's scope
precisely because that one declared them out of its own. Both title
themselves `(DRAFT)` and describe themselves as a "Starter-seeded draft
package", so `draft` is read off the document rather than chosen for it.

**THE ARCHIVED RECORD — ALL THREE CANDIDATE VALUES MEASURED, AND THE RULED ONE
DOES NOT WIN.** This is the one W1 edit that touches an archived path. The
commission ruled `draft` for it. Every candidate was run before any was
written, and the ruled value turns out to trade one error for another:

| Header written | `status-validity` | `ratified-provenance` | `promotion-fidelity` |
| --- | --- | --- | --- |
| `Status: draft` (as ruled) | clears | 0 | **NEW ERROR** |
| `Status: ratified`, uncited | clears | **NEW CRITICAL** | 0 |
| `Status: ratified` + citation | **clears** | **0** | **0** |

**The `draft` result is the surprising one and it is the reason this packet
departs from the literal ruling.** `promotion_fidelity.PRE_RATIFICATION` is
`{"brainstorm", "staged", "draft"}`, and a packet declaring one of those
"never claimed the approval that obliges promotion, so its deltas are archived
design evidence". Marking this packet `draft` therefore DISCOUNTS its
`ideation-dashboard` delta as the authority for
`Staged-topic proposal commissioning`, the family falls back to the earlier
`2026-08-01-add-workbench-branch-sessions`, and that packet's 7 ratified
scenarios are then compared against a promoted spec the later packet
legitimately rewrote — producing:

> `[error] openspec/changes/archive/2026-08-01-add-workbench-branch-sessions/specs/ideation-dashboard/spec.md — requirement 'Staged-topic proposal commissioning' reached openspec/specs/ideation-dashboard/spec.md without 1 of its 7 ratified scenarios`

Isolated by reverting this single edit and re-running: `promotion-fidelity`
reads **1 error with the `draft` backfill and 0 without it**. So `draft` would
have cleared four `status-validity` errors and manufactured one
`promotion-fidelity` error against an innocent third packet — a net of three,
and a false report about a change that did nothing wrong.

**`ratified` with a citation clears all four families and manufactures
nothing**, and it is not a workaround — it is what the promoted rule says.
`openspec/specs/document-lifecycle/spec.md:39-53` states that a `ratified`
value's citation "SHALL be derived from the packet's own record — **its origin
declaration**, its ratification or archive commit, its own task record, or the
index row that announced it". The origin declaration is named FIRST. This
packet's `.openspec.yaml` carries `approved_by: Brett Heap` and
`approved_on: 2026-08-25`, so the citation is derived rather than invented, and
it clears the record-citing spelling's three-way floor on ALL THREE axes rather
than the one it needs: approver, date, and a resolvable record path.

That is also what the precedent actually did — 43 of the 44 backfills took
`ratified` plus a citation, and Brett himself ruled the same direction on
2026-08-26, correcting an archived packet FROM `draft` TO `ratified`
"to match the header convention used by every sibling ratified archived
packet" (commit `4dc57a4d`). This is the departure recorded as OD-5.

**THE PRECEDENT, VERIFIED RATHER THAN CITED FROM MEMORY — AND THE COMMISSION'S
PREMISE CORRECTED IN THREE PLACES.** The instruction that opened this work
cited "ruling 5C.3 (2026-08-23), which backfilled 46 archived proposals with
exactly this edit". Read at the archive, the packet says something different,
and the differences are recorded here rather than smoothed over:

1. **`5C.3` is not the authorizing ruling.** It is the STOP-AND-REPORT guard
   rail (`tasks.md:1948-1956`): "Where a record genuinely cannot support a
   status, or supports a status but not a citation the floor accepts, the
   campaign leaves that document alone and reports it BY NAME … It does not
   get a plausible-looking header". The authorization was `OQ-6`
   (`proposal.md:511-556`).
2. **The count is 44, not 46.** Forty-four archived `proposal.md` files were
   in scope (`tasks.md:1713-1728`); 46 was the `status-validity` ERROR CENSUS
   before the slice (44 archived + 2 active).
3. **The value was `ratified` for 43 of them, and `draft` for exactly ONE.**
   Forty-three took `Status: ratified` plus a `Ratified:` citation, two lines
   each. One — `enable-live-openxfactory` — took `Status: draft`, alone, on
   line 1, uncited. Confirmed on disk: of 112 archived proposals in this
   repository today, 110 read `ratified`, 1 reads `draft`, and 1 reads nothing,
   and that last one is the file this packet edits.

**So the operative precedent is the one-document ruling, not the 43-document
one**, and it is on all fours with this case. `tasks.md:1768-1791`, verbatim:
"`draft` is the honest value the record has always supported and needs no
citation — the promoted rule requires a citation only for `Status: ratified`,
and 'absent such backing the document MUST carry `draft` or lower status'".
Two more instances took the same shape and value in the same campaign, the
MedxChart and MedxPractice overlay-boundary proposals, each tabulated as
"`Status: draft`, no citation — **The record names no ratification act.**"
(`tasks.md:2164-2166`). The precedent has three instances, and the promoted
scenario `A record cannot support a derived header`
(`openspec/specs/document-lifecycle/spec.md:75-79`) is its canon form.

**AND `record-immutability` CANNOT FIRE ON IT, BY CONSTRUCTION.** The
commission asked this to be confirmed rather than assumed, and it is confirmed
twice. Structurally: `fam_record_immutability` iterates `ctx.docs`, which
`corpus.iter_doc_paths` builds from `GOVERNED_ROOTS = ("contracts", "docs",
"examples", "ideation", "templates")` — `openspec/` is not a governed root, so
no archived proposal can reach the family — and its first statement is
`if doc.status != "record": continue`, which a `draft` header fails a second
time. Empirically: the family reported 5 criticals before this edit and 5
after, the same five paths. That is also why the 44 backfills of 2026-08-23
needed no allowlist, no baseline entry and no disposition — a point
`govern-openspec-corpus-membership` makes in its own words at
`proposal.md:18-22` and proves at `tasks.md:1870-1874`.

**W3 — THE FIX RE-POINTS THE FINDING; IT DOES NOT CLEAR IT. This corrects the
commission's stated expectation and is the single most important number in
this packet.** The forcing document cites TWO changes, not one:

```
implement-avatar-client-lab      ARCHIVED  (archive/2026-08-04-implement-avatar-client-lab)
qualify-avatar-live-voice        ACTIVE    (openspec/changes/qualify-avatar-live-voice)
```

`_staged_exit_changes` returns its ids SORTED and the finding reports
`cited[0]`, so the archived id won on alphabetical order — and in doing so
HID the performable remedy behind an impossible one. After the fix the row is
still an error, re-pointed:

- before: `staged material already cites proposal implement-avatar-client-lab`
- after:  `staged material already cites proposal qualify-avatar-live-voice`

**So `location-conformance` reads 3 errors before and 3 errors after, and the
error count of this repository does not move for W3 at all.** That is the
correct outcome and the fix working, not the fix failing: the material genuinely
can move into `qualify-avatar-live-voice`, and the operator is now told the one
thing they can actually do. The regression proof therefore lives in the
fixtures rather than in a corpus delta, which is what the two added tests are
for.

It also matters for what does NOT happen. `Finding.match_key()` is
`(family, repo, path)` — rule text is not part of it — so the row keeps its
identity across the change, no CONTESTED finding vanishes, and no
`uncited-resolution` error is manufactured. **No disposition is owed by this
packet**, and none is added.

**THE OTHER TWO ROWS ARE UNTOUCHED, AND BOTH ARE CORRECT AS THEY STAND.**
`ideation/staging/openxwallet-neutral-home/openxwallet-neutral-home.md` cites
`create-ledgerxwallet-overlay-boundary`, which is ACTIVE; that row is another
session's in-flight work and is byte-identical before and after this change.
`ideation/staging/worker-enrollment-broker/worker-enrollment-broker.md` cites
`add-worker-enrollment-broker`, also ACTIVE, and is likewise unmoved. Neither
was touched, and the fix leaving them firing is the live-corpus half of the
"the exemption is not blindness" proof.

**THE FLOOR, BEFORE AND AFTER.**

| Family | Before | After | Why |
| --- | --- | --- | --- |
| `status-validity` | 4 error | **0 error** | W1's four backfills |
| `ratified-provenance` | 0 | **0** | the one `ratified` header written carries a derived citation clearing all three floor axes |
| `promotion-fidelity` | 0 | **0** | the value chosen in OD-5 is the one that does not discount an innocent packet's delta |
| `record-immutability` | 5 critical | **5 critical** | out of reach of `openspec/`; untouched by this packet |
| `location-conformance` | 3 error | **3 error** | one row re-pointed from an impossible remedy to a performable one |
| **whole run** | **5 critical / 11 error / 41 warning / 11 info** | **5 critical / 7 error / 41 warning / 12 info** | |

The whole-run numbers are the ones to check: **four errors cleared, none
introduced, criticals and warnings unmoved.** The single added INFO is
`modified-block-currency` observing that this packet's own MODIFIED block
diverges from promoted canon in exactly 2 of 10 units — which are exactly the
two "active or archived" phrases OD-4 narrows on purpose. That family cannot
distinguish a deliberate rewording from drift and does not claim to; the info
line is the check working, and it is the audit trail for the narrowing.

## The mechanism, stated exactly

`corpus.change_ids` unions THREE vocabularies into one flat set: active folder
names, archived folder names, and archived names stripped of their
`YYYY-MM-DD-` prefix. That union is right for the question most callers ask —
"does this id name a change that ever existed" — and `ratified-provenance`
depends on it, because a ratification citation may name an archived change and
must. It is the wrong set for the question the staged-exit arm asks, which is
"can an act still be performed against this change".

1. `corpus.active_change_ids(repo_path)` answers the second question. It is a
   SIBLING, not a narrowing: `change_ids` is not touched, and its callers keep
   the union they need.
2. `fam_location_conformance` builds the per-repo active-id map from
   `ctx.repo_paths` — the same tree its other two arms already walk — rather
   than from a new `Context` field. No `Context`, `runner.py` or `conftest.py`
   change is owed, and the set cannot drift from the tree the family measures.
3. Only the staged-exit arm reads it. The brainstorm arm, the stray-staged arm,
   the active-support walk, the archive-support walk and the canonical-specs
   bundle check are untouched.

The consequence worth stating: **the finding does not disappear when a cited
change archives — it re-points to whichever cited change is still active, and
only goes silent when NO cited change is active.** A staged fragment whose
every exit has archived is genuinely finished with staging by a route this
family cannot remedy, and that is the one case it now stays quiet for.

## What this changes

- **Four documents carry a controlled status**, and `status-validity` reads 0.
- **The archived-record edit is registered**, in the append discipline
  `docs/archive-record-discrepancies.md` has used for every prior
  archived-record correction.
- **`location-conformance` stops demanding impossible acts**, and starts naming
  the performable one when a document cites both kinds of change.
- **Canon says so**, so the next reader does not restore the union by
  tidying — the promoted text currently PINS the defect in two places.

## What this deliberately does not change

- **`corpus.change_ids`.** Not one line. `ratified-provenance` reads the union
  on purpose and its pinned action line says so verbatim.
- **The other two `location-conformance` rows.** Both cite ACTIVE changes, both
  are correct as they stand, and one belongs to another session's in-flight
  work.
- **`record-immutability`, in any way.** Its five criticals are pre-existing,
  recorded as such by three prior packets, and stand untouched at five. The one
  of them this session was also commissioned to end —
  `ideation/cross-reference.md` — is filed separately; see OD-1.
- **The controlled taxonomy.** `open (operational)` maps INTO the existing
  vocabulary rather than the vocabulary widening to admit it. No value is added
  by this packet.
- **`health/dispositions.yaml`.** No finding vanishes without keeping its
  match key, so nothing is owed there and nothing is added.
- **The family registry, the enumeration, the numerals, the report schema, any
  threshold.**

## Orchestrator decisions, cleared 2026-08-28 (authored: flagged for veto)

**CLEARED 2026-08-28**, by a multi-choice put to Brett by the orchestrating
session and relayed to this session the same day. The selections that reach
this packet: **OD-5 KEEP `ratified` plus the derived citation** — the measured
deviation from the ruled `draft` is APPROVED as taken — and **both pull
requests merge on green**. On OD-5 he took the packet's own recommendation, so
**the clearance moves nothing**: not one byte of the archived record's header
changes, and the three-way measurement stands as the reason. OD-1's split is
confirmed by the same act in the form that matters — the sibling packet is
merged on its own gate rather than folded back in — and **the aggregation
disposition entry that split turned on is assigned to the ORCHESTRATING
SESSION as part of the merge sequence, not to this one.** OD-2, OD-3 and OD-4
were not put to him and are NOT covered; they stand as authored, still flagged.
No verbatim wording of the ruling reached this session, so none is quoted —
the approver, the date, the mechanism and the selections are recorded instead,
which is what the origin requirement asks for. **THE ORIGINAL FLAGGED TEXT IS
KEPT BELOW AS MARKED HISTORY** rather than rewritten, because what was flagged
and why is the part a later reader needs. This act is DISTINCT from the
commission recorded in `.openspec.yaml`: that one admitted the packet, this one
closed the veto window on the decision that departed from a ruling.



**OD-1 — THE THIRD RULED WORKSTREAM IS FILED SEPARATELY, NOT IN THIS PACKET.**
**CONFIRMED 2026-08-28 in the form that matters, and ONE CLAUSE OF IT
REASSIGNED.** The same ruling directs that BOTH pull requests merge on green —
so the split stands and the sibling lands on its own gate rather than being
folded back in. **The aggregation disposition entry this decision turned on is
now the ORCHESTRATING SESSION's to write, as part of the merge sequence, and is
NOT owed by either packet's authoring session.** That reassignment does not
weaken the argument below — the entry is still owed, still in another
repository, and still the reason these two workstreams were not coupled to the
third — it changes only WHO performs it. The text below is kept as authored.
Brett commissioned three workstreams together ("lets do all 3 in order"), and
this packet carries two. The third — generated projections take a NON-RECORD
status, ending the `record-immutability` critical on `ideation/cross-reference.md`
at its root — is filed as `declare-generated-projection-status`. **The reason is
archive-gate coupling, measured rather than felt.** That workstream extends the
controlled status taxonomy to a NINTH value, which touches `doc_health.TAXONOMY`,
`promotion_fidelity`'s two exhaustive standing sets, a closed regex alternation in
the NotebookLM sync, a `lifecycle_status` enum in a `contracts/` schema, the
lifecycle table in `docs/document-lifecycle.md` and a MODIFIED block restating
eight scenarios — **and it owes a disposition entry in the AGGREGATION
repository**, because `health/dispositions.yaml` does not exist in openxFactory
and the `record-immutability` finding it clears is CONTESTED, so its
disappearance becomes an `uncited-resolution` ERROR on the nightly without one.
Coupling W1 and W3 to that would put four cleared errors and a three-line
predicate fix behind a taxonomy debate and an act in another repository, neither
of which they need. **Alternative not taken:** one packet, on the
`govern-openspec-corpus-membership` precedent — a multi-slice floor campaign
carrying mechanical backfills, code, and deltas on two capabilities in a single
change. That precedent is real and was weighed; it is declined because none of
its slices had a cross-repository dependency, and the coupling here is
gratuitous rather than inherent. **If Brett would rather see all three in one
change, this is the decision to veto** and the remedy is cheap: the two packets
have no file in common except `README.md`.

**OD-2 — THE ARCHIVED-RECORD EDIT IS REGISTERED IN
`docs/archive-record-discrepancies.md`, BY APPENDING.** Every prior
archived-record correction in this repository is recorded there —
two "Corrected 2026-08-23" sections from the 44-document campaign, and three
dated addenda since — and each appends rather than editing what stands. This
follows that exactly. **The cost is stated rather than discovered:** that file
carries `Status: record`, so editing it trips `record-immutability` — and that
critical is ALREADY STANDING and unchanged by this entry, verified by running
the family either side of the edit rather than assumed, which is the same
verification `govern-openspec-corpus-membership` performed for the same file
(`tasks.md:1700-1712`). **Alternative not taken:** leaving the edit unregistered
because it is one line. Declined — the register exists so that the next
differential audit of archived records finds the reason a header appeared,
and a one-line edit is exactly the kind that looks like drift later.

**OD-3 — THE ACTIVE/ARCHIVED PREDICATE IS DERIVED FROM `ctx.repo_paths`, NOT
THREADED THROUGH `Context`.** The reviewed alternative was a new
`ctx.active_change_ids` field populated in `runner.py` beside `change_ids`.
Declined for a measured reason: `tests/doc-health/conftest.py`'s `make_ctx`
would then also need to populate it, and the five existing
`location-conformance` tests hand-set `ctx.change_ids` while building a real
tree under `tmp_path` — so a threaded field would have made those five tests
depend on a fixture seam rather than on the tree they construct, and a sixth
test written later that forgot the new field would silently never fire.
Reading `ctx.repo_paths`, which every one of those tests already sets, keeps
the family's answer derived from the same tree its other two arms walk. The
trade: one directory listing per repository per run, in a family that already
performs two full `openspec/changes` walks.

**OD-4 — A SPEC DELTA RIDES, ON `doc-health`, AS `MODIFIED`.** Not optional and
not a choice between shapes: the promoted requirement PINS the defect in two
places — "It SHALL report staged material that already cites an active or
archived proposal" in the body, and "**WHEN** a staged document names an active
or archived OpenSpec change" in the scenario. An `ADDED` clarification would
have left canon contradicting the code. The block restates the requirement in
full, per the `A MODIFIED requirement block restates the requirement as canon
currently states it` rule, keeps all four original scenarios, and adds two that
pin the new behaviour on both sides. **In-idiom rather than novel:** this same
family already carries an explicit MUST-NOT-emit carve-out in canon (the
`Kind: register` organized-state home), which `govern-openspec-corpus-membership`
§ design.md:73 cites as "an explicit carve-out" precedent.

**OD-5 — THE ARCHIVED PROPOSAL TAKES `Status: ratified` PLUS A DERIVED
CITATION, NOT THE RULED `Status: draft`. THIS IS A DEPARTURE FROM A RULING AND
IS FLAGGED AS ONE.**
**RULED 2026-08-28: KEEP `ratified` plus the derived citation — the deviation
is APPROVED as taken.** Brett was given the departure, its three-way
measurement and the one-line-revert remedy, and selected the packet's own
recommendation, so **nothing in the file or in this decision moves.** The
paragraphs below are kept EXACTLY as authored, because the argument they make
is the standard the ruling approved rather than a case now closed: the next
session backfilling an archived header needs the measurement, not the verdict.
The veto branch this decision named for itself was NOT taken.
AS AUTHORED, kept: it is the only decision in this packet that contradicts an
instruction rather than filling a gap in one, and it is taken for a measured
reason, not a preferred one.

**The ruling rested on a premise that verification disproved.** The commission
directed `Status: draft` on the ground that "ruling 5C.3 (2026-08-23) backfilled
46 archived proposals with exactly this edit", and instructed this session to
verify that precedent at the archive BEFORE editing an archive path. Verified,
it is wrong in three ways (§ What was measured): `5C.3` is the stop-and-report
guard rail rather than the authorization; the count is 44, not 46; and **43 of
those 44 took `ratified` plus a citation, while exactly ONE took `draft`.** The
instruction described the minority case as if it were the rule.

**And the ruled value does not merely fail to match the precedent — it
manufactures a new error.** Measured by reverting the single edit and
re-running: `Status: draft` puts the packet in
`promotion_fidelity.PRE_RATIFICATION`, which discounts its `ideation-dashboard`
delta as archived design evidence, which makes an innocent third packet
(`2026-08-01-add-workbench-branch-sessions`) report as having failed to promote
one of its seven scenarios. Four errors cleared and one false error created, in
a packet whose entire purpose is to clear floor.

**The value written is derived, not invented.** The promoted rule names "its
origin declaration" as the FIRST source a ratification citation may be derived
from, and this packet's `.openspec.yaml` carries `approved_by: Brett Heap` and
`approved_on: 2026-08-25`. The citation clears the record-citing spelling's
three-way floor on all three axes. Brett's own ruling of 2026-08-26 (commit
`4dc57a4d`) corrected a different archived packet in exactly this direction —
`draft` to `ratified` — "to match the header convention used by every sibling
ratified archived packet". Of 112 archived proposals here, 110 read `ratified`.

**THIS IS THE DECISION TO VETO IF THE READING IS WRONG** — *and it was not
vetoed; see the ruling marker at the head of this decision* — and the veto is
cheap: the remedy is a one-line revert to `Status: draft`, at the cost of the
`promotion-fidelity` error above, which would then itself need a disposition or
its own change. The alternative this packet declined — obey the ruling
literally and file the manufactured `promotion-fidelity` error as a named
follow-up — was rejected because it would knowingly leave a false report about
a packet that did nothing wrong, in order to satisfy a ruling whose stated
grounds do not survive the verification that same ruling ordered.

## Open Questions

**Q1 — Should the staged-exit arm report EVERY active cited change rather than
just `cited[0]`?** The alphabetical-first rule is what hid the performable
remedy behind the archived one, and narrowing the set fixes this instance
without fixing the rule. A document citing two ACTIVE changes still reports
only the alphabetically first, and the operator is told about one of two
possible destinations. **RECOMMENDATION: not in this packet.** It changes the
finding COUNT rather than its content, which moves the floor for reasons
unrelated to the defect this change was commissioned to end, and it needs its
own before/after measurement across every repository the nightly reads. Named
as a follow-up rather than folded in.

**Q2 — Should a staged fragment whose every cited exit has archived be reported
by some OTHER family?** After this change such a document goes silent here, and
silence is the right answer for THIS family — no move is possible. But the
document is still `Status: staged` while the work it was staged for has
completed, which is a real lifecycle condition (`staged-candidate-aging` is the
plausible owner) and is no longer reported anywhere.
**RECOMMENDATION: leave it, and record the gap rather than close it.** The
condition is not a location defect and inventing a home for it inside a
location-conformance fix would be the same category error this change is
removing. The two added tests make the silence deliberate and visible; a future
packet can decide whether aging should speak.

## Impact

- **Affected specs:** `doc-health` (one MODIFIED requirement; no ADDED, no
  REMOVED, no family enumeration change, no numerals moved).
- **Affected code:** `scripts/doc_health/corpus.py`,
  `scripts/doc_health/families.py`, `tests/doc-health/test_families.py`.
- **Affected documents:** four status backfills, one appended register
  addendum, one README entry.
- **Contract bundle:** none owed, measured against all 48 inventories.
- **Dispositions:** none owed, measured — no finding loses its match key.
- **Sibling:** `declare-generated-projection-status` carries the third ruled
  workstream (OD-1). The two packets share no file but `README.md`.
