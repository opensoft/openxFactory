# Clarify questions — 038-opendox-document-tool-self-maintenance (round 1)

Status: draft

**Feature**: `038-opendox-document-tool-self-maintenance`, release 2 ("the
document tool and self-maintenance", phases 4–5) of the ratified OpenSpec
change `add-neutral-product-standalone-operability` (#1144).
**Lane**: `openxfactory-4`. **Raised**: 2026-10-05, at `/speckit.specify`,
before any plan or code. **Answer state**: OPEN. All 25 await Brett Heap.
Nothing here is decided by this feature. Each question puts its recommended
option first, marked **(Recommended)**, and that is a recommendation only.

**Naming.** These are `R2Q1`…`R2Q25`. A bare `Q<n>` names one of #1144's own
rulings (RULING Q1, RULING Q2, Q-R4, DIRECTION Q5), and `R1Q<n>` names plan
034's, so this round uses neither.

**Measured at**: openDox-code `a9ac96f9`, openXdox-code `56e1c238`, the openDox
root `d77f8cbf` and openxFactory `0f2a87f6`, all `main` on 2026-10-05. Box
numbers (`12.6a`, `14.5`, …) are #1144 `tasks.md`'s. Falsifier labels are plan
034's: `F<group>.<n>` is the n-th FALSIFIED BY box of that group, so F12.1 is
12.5's governed-flow proof and F12.2 is the submission and landing acceptance.

**What is NOT asked.** Nothing that #1144 or a ruling already decides is asked
here. That covers the rulings `5783934499`, `5784155201`, `5784247356` and
`5784295745` as #1144 encodes them, the migration number (`0003_`), the three
class spellings, the guardrails, the sandbox's shape, the patch rules, and the
shapes of the `submit`, `land` and `health` verbs. R2Q6 asks only whether
those verbs gain one option. Where a question touches one of these, it asks
how two decided texts fit together, never whether to keep one.

**How to answer.** One line per question is enough, for example `R2Q1 a`.
Each answer is written inline under its question, and encoded into `spec.md`
in the same commit. An answer that changes a falsifier or a task line of
#1144's `tasks.md` lands there as a bookkeeping amendment on your word, in plan
034's T007 form, under a Rule 6 window. An answer that would change a
requirement's text or a scenario is put to you as a ruling first, and is not
applied here.

**What each phase waits on.**

| phase | cannot be planned without |
|---|---|
| 4 (Group 12) | R2Q1, R2Q2, R2Q3, R2Q4, R2Q6, R2Q7, R2Q8, R2Q9 |
| 5 (Groups 6, 14, 15) | R2Q5, R2Q6, R2Q10–R2Q21, R2Q25 |
| release 2's close | R2Q22, R2Q23 |
| process only | R2Q24 |

**Five are contradictions, not gaps**: R2Q1, R2Q3, R2Q5, R2Q11 and R2Q14.

---

## R2Q1 — What does "one interface for both" bind? *(blocks FR-004; phase 4)* — CONTRADICTION

**What #1144 says, twice.** The release map's phase-4 row reads *"local merge
and the governed pull-request path, the neutral submission step, one interface
for both"*. The proposal and `design.md` § D13 say *"behind one interface"*.
But 12.1 says *"SPLIT THE PROTOCOL; do not bend the platform's one"*. It makes
`SubmissionPort` new and leaves `PullRequestPort` unchanged. 12.6a then makes
landing *"a SEPARATE protocol, `session_pr.LandingPort`"*. That is three
protocols, and `design.md` § D9 rejects folding them.

**Options.**
- **(a) (Recommended)** One USER-FACING interface. The `submit` and `land`
  verbs and routes, and the Health view's land action, are the same in every
  mode. Behind them, the three protocols stay split as 12.1 and 12.6a require,
  and the governance query picks the binding. *Consequence:* no box text moves.
  The map's phrase is recorded as a non-normative reading.
- **(b)** One PROTOCOL for submission and landing. *Consequence:* this reverses
  12.1 and 12.6a, which § D9 argued against. It needs a bookkeeping amendment to
  both boxes, and a ruling if their text moves.
- **(c)** Strike the phrase from the map as an editorial slip. *Consequence:* a
  bookkeeping amendment to the map's one cell and to § D13's line.

**ANSWER:** _awaiting Brett Heap_

---

## R2Q2 — Under `governed`, what does routing the landing to the instrument do? *(blocks FR-007, US2 scenario 4; phase 4)*

**What is decided.** Requirement 11 says that the governed host *"RESERVES
landing and routes it to that governance's own instrument, and the product
itself lands nothing"*. 12.6a says that *"a registered host profile that
declares an instrument makes the repository `governed`"*, and that under
`governed` *"a land request … is routed to the host's own instrument"*, with
NO `LandingPort` bound (F12.2's `test_a_governed_repository_binds_no_lander`).
The fix-loop ruling `5784247356` adds: *"A governed repository gets a pull
request instead."*

**What is not.** What a host declares as its "instrument", and what `land`, or
the fix loop's land action, DOES under `governed`.

**Options.**
- **(a) (Recommended)** The instrument is the host's contributed
  `SubmissionPort` (12.4). Under `governed`, `land` binds no lander, and instead
  submits through the host's port: for openXdox, push, then open or update the
  pull request. It then reports where the work went, and the merge stays the
  governance's act. *Consequence:* one host contribution serves both acts, and
  the fix loop's "gets a pull request" holds with no second step. `gate open-pr`
  is untouched.
- **(b)** `land` refuses under `governed`, naming the host's declared
  instrument. The human then runs `submit`, or the host's own verb.
  *Consequence:* simplest. A governed user takes two acts, and the fix loop's
  pull request needs the second.
- **(c)** The host declares a separate instrument callable, distinct from its
  `SubmissionPort`. *Consequence:* a fourth seam to declare and test.

**ANSWER:** _awaiting Brett Heap_

---

## R2Q3 — How does F12.1 run, while 15 of its 16 suites sit in the declared exclusion? *(blocks FR-005, US3; phase 4)* — CONTRADICTION

**Measured** at openXdox-code `56e1c238`. F12.1's own selection, `git grep -l
-e open-pr -e open_pr -e FakePullRequests -- 'tests/test_*.py'`, selects 16
files. Fifteen are entries of `tests/declared_exclusion.yaml`, each with the
reason `doc_health`. Only `tests/test_gate_loop_views.py` runs in a lone
checkout. F12.1 installs `".[test]"` and runs each file with plain `pytest`, so
15 of the 16 fail to import `doc_health`. Plan 034's research R11 measured the
same on 2026-09-24.

**What is decided.** R1Q6 (d) (`5817152735`) made the `doc_health` direction
its own arc, *"decided before 12.5 needs the 16 governed suites"* (plan 034
T008). The arc's record is the staged topic
`ideation/staging/doc-health-direction-arc/`, and its Q1–Q4 and Q6 await your
ruling. That ruling is owed before 12.5 whatever is answered here. This
question asks only how F12.1 runs. For F5.2, R1Q23 (a) (`5850003126`) composed
openxFactory's `scripts/` at a named commit.

**Options.**
- **(a) (Recommended)** Rule the direction arc before phase 4's 12.5, as R1Q6
  (d) requires. Then run F12.1 as R1Q23 (a) runs F5.2, with openxFactory's
  `scripts/` composed at a named commit, until the arc's realization lands.
  F12.1 gains that environment line by a bookkeeping amendment.
  *Consequence:* phase 4 waits on the ruling but not on the arc's realization.
  The exclusion stays an open extraction, reported as open.
- **(b)** 12.5 waits for the arc's REALIZATION to land, so that F12.1 runs
  standalone as written. *Consequence:* phase 4's close is gated on an arc that
  has no owner yet (the topic's Q6).
- **(c)** 12.5 closes on `test_gate_loop_views.py` alone, and reports the other
  15 as open. *Consequence:* requirement 11's tenth scenario rests on 1 suite of
  16.

**ANSWER:** _awaiting Brett Heap_

---

## R2Q4 — Does any governed host carry `submit`, `land` or `health` in release 2? *(blocks FR-004, FR-007; phases 4–5)*

**What is decided.** R1Q4 (a) (`5817152735`): openDox's default profile
contributes *"openDox's own verbs and routes: the runtime verbs now, and
release 2's `submit`, `land` and `health` later"*. Under R1Q5 (a), a host that
registers its own profile keeps its own tree, which has 32 entries since phase
3 (`5970917267`). Measured at openDox-code `a9ac96f9`: `default_profile.py`'s
`SUBCOMMAND_EXTENSIONS` is `(RuntimeSubcommand(),)`.

**What is not.** 12.4 lets a governed host contribute its own
`SubmissionPort`, and 12.6a lets it declare an instrument. Both act on verbs
that a host's own profile does not carry unless it contributes them. So: do
openXdox and openxFactory contribute any of the three in release 2?

**Options.**
- **(a) (Recommended)** Neither contributes in release 2. Their trees and
  their help goldens do not move, and their governed flows (`gate open-pr`, and
  openxFactory's own doc-health) are unchanged. F12.2 proves the host-side
  behaviour against a registered test host. *Consequence:* the smallest
  governed-side change, and 12.5 proves nothing moved. A host's opt-in is a
  later act.
- **(b)** openXdox contributes `submit` (with its `GhPullRequests`-backed
  `SubmissionPort`) and `land`, routed to its instrument. *Consequence:* the
  32-entry tree and goldens move in openXdox-code and openxFactory, by a batch-O
  style amendment, and the governed console gains the neutral verbs.
- **(c)** Both hosts contribute all three, `health` included, running
  openDox's neutral checks over openxFactory's corpus. *Consequence:* broadest.
  It puts neutral findings beside openxFactory's governance findings, and it
  needs a store in the composed host, which has none today.

**ANSWER:** _awaiting Brett Heap_

---

## R2Q5 — Which process owns the bundled store while a `health` verb runs? *(blocks FR-011, FR-015, US4–US6; phase 5)* — CONTRADICTION

**Measured** at openDox-code `a9ac96f9`. R1Q16 (i) and (iv) made the bundled
PostgreSQL the DOCUMENT SERVER's child, which stops with the entry point.
`runtime status` reports the bundle and never starts it. A local `runtime
migrate` or `reset` refuses unless a live server of this data directory runs,
in `runtime/bundle.py`'s `refusal_before_connecting`, verbatim: *"no bundled
server is running on … A local install's server is started by `opendox
generate-and-open --local`, which owns it"*.

**The collision.** F14.1 and F15.1 run `opendox health run|list|fix|accept` in
local mode with no document server started. F14.1 also runs `opendox-runtime
runtime reset --confirm …` and `runtime migrate`. As built, the runtime verbs
refuse, and the `health` verbs have no store to reach.

**Options.**
- **(a) (Recommended)** A local verb that needs the store uses a live bundled
  server of THIS data directory when one is running. Otherwise it starts one as
  its own child for the verb's duration, and stops it on exit. That reads R1Q16
  (i) and (iv) as *"the process that starts the server owns it, and it stops
  with that process"*. `runtime migrate` and `reset` take the same rule.
  *Consequence:* F14.1 and F15.1 run as written, a CLI-only install works (the
  requirement 14 scenario that names an install without a browser), and each
  cold verb pays a server start.
- **(b)** The verbs refuse without a running document server, naming
  `generate-and-open --local`. F14.1 and F15.1 are amended to start one first.
  *Consequence:* the CLI-only use always needs a server running beside it.
- **(c)** A long-lived background store, started once and shared.
  *Consequence:* this reverses R1Q16 (i) and (iv), and needs your ruling on
  that.

**ANSWER:** _awaiting Brett Heap_

---

## R2Q6 — How do `submit`, `land` and `health` learn the install mode? *(blocks FR-004, FR-007, FR-011; phases 4–5)*

**What is decided.** `standalone` requires `OPENDOX_INSTALL_MODE=local` (12.6a),
and the `health` store is the local bundle (Group 13). R1Q15 (b) gave
`generate-and-open` a `--local` flag that selects local as the setting does,
and plan 034's T070 refuses a flag and a setting that disagree. F14.1 and F15.1
export the setting.

**Options.**
- **(a) (Recommended)** Each new verb takes the same `--local` flag, equivalent
  to the setting, and a flag and a setting that disagree are refused, naming
  both. *Consequence:* a student who started with `--local` uses the same word
  everywhere, and an unset install stays hosted (13.5). The shapes that 12.4a,
  12.6a and 14.5 declare each gain one option, by a bookkeeping amendment, as
  T007 batch H gave `generate-and-open` its `--local`. F14.1 and F15.1, which
  export the setting, stand as written.
- **(b)** The setting alone. *Consequence:* the declared shapes stand
  verbatim. But a `land` typed in a fresh shell reads `hosted`, governance
  becomes `unknown`, and the landing is refused, a confusing first experience.
- **(c)** The mode is persisted in the state directory by the first local
  start. *Consequence:* the mode can be entered by state rather than by an
  explicit choice, which edges toward the "by omission" that 13.5 forbids.

**ANSWER:** _awaiting Brett Heap_

---

## R2Q7 — How does a standalone owner's first governance declaration reach the default branch? *(blocks FR-007, US2; phase 4)*

**What is decided.** 12.6a reads `governance: standalone` only from
`.opendox/governance.yaml` at the DEFAULT branch's tip. A branch that adds it is
`unknown`. *"Because the declaration is a committed file, changing it is a
landing like any other."* Until it exists, no lander is bound, so the product
cannot land the declaration itself.

**Options.**
- **(a) (Recommended)** The product never writes the default branch outside
  `land`. With no declaration, `land` refuses as `unknown`, naming the exact
  file and content, and that the owner commits it to the default branch
  themselves. The openDox root's README documents it. *Consequence:* no new
  writer of the default branch, and one documented git step for a new owner.
- **(b)** As (a). In addition, a local install's `project create-repository`
  seeds the declaration in a NEW repository's first commit, since its creator
  is its owner. *Consequence:* new repositories need no manual step, and the
  runtime's repository act gains a write.
- **(c)** A `governance declare standalone` verb commits the declaration to the
  default branch after a terminal confirmation. *Consequence:* a second path
  onto the default branch, with its own guardrail tests.

**ANSWER:** _awaiting Brett Heap_

---

## R2Q8 — Does a standalone landing ever reach the remote? *(blocks FR-007; phase 4)*

**What is decided.** `land` merges a session branch into the LOCAL default
branch (12.6a). `submit` pushes a session branch to the attached remote (12.2).
Neither box says whether the default branch is pushed after a landing.

**Options.**
- **(a) (Recommended)** `land` is local only. The default branch reaches a
  remote only by an explicit `submit --branch <default-branch>`, or by the
  user's own git. *Consequence:* landing and submission stay two acts, each with
  its own report.
- **(b)** After a successful landing, `land` pushes the default branch to the
  attached remote and reports where. *Consequence:* one act, and a landing now
  also spends the user's push credential.
- **(c)** `land`'s prompt asks whether to push. *Consequence:* a second
  interactive answer, which needs a guardrail test of its own.

**ANSWER:** _awaiting Brett Heap_

---

## R2Q9 — Once a conflict is shown, what remedy does the product name? *(blocks FR-007, US2 scenario 3; phase 4)*

**What is decided.** Requirement 11: a conflict *"SHALL BE SHOWN to the human
and never silently resolved"*. 12.6a: *"A conflict raises `MergeConflict`
carrying the conflicting paths and leaves the default branch where it was."*

**Options.**
- **(a) (Recommended)** The refusal names the remedy: bring the default branch
  into the session branch and resolve there, by git or by editing in openDox.
  Release 2 adds no conflict editor. *Consequence:* the smallest surface. A
  student without git experience gets instructions, not a tool.
- **(b)** A product verb merges the default branch INTO the session branch, and
  leaves the conflict markers in the session's checkout for the human to edit
  and commit, never on the default branch. *Consequence:* a guided path, and
  one more verb with tests.
- **(c)** An in-view conflict editor. *Consequence:* the largest. It is a UI
  feature that #1144 does not name.

**ANSWER:** _awaiting Brett Heap_

---

## R2Q10 — Does the hosted multi-user plane run the health engine? *(blocks FR-009; phase 5)*

**What is decided.** The hosted plane carries no `session` capability, so
`submit` refuses there (12.4a), and the view's confirm control needs a
loopback nonce (12.6a). The `0003_` migration applies to every install,
because there is one migration set (requirement 12). F14.1 and F15.1 run local
mode only. Health results are per corpus, and a hosted plane serves many users'
projects.

**Options.**
- **(a) (Recommended)** Release 2 serves the health engine on the LOCAL plane
  and from the CLI. On the hosted plane, the Health view and its routes refuse
  by name, as `submit` does, while the schema still migrates. *Consequence:* no
  per-tenant results design in release 2, and the hosted schema is ready for a
  later act.
- **(b)** The hosted plane runs and lists health per project, read-only, and
  refuses `fix`, `accept` and `land`. *Consequence:* the results need a project
  key and membership checks, which the plan must design.
- **(c)** Full parity on the hosted plane. *Consequence:* the fix loop writes
  branches in checkouts a hosted plane does not hold. That conflicts with 12.4a's
  reasoning on personal credentials.

**ANSWER:** _awaiting Brett Heap_

---

## R2Q11 — F6.1 against release 1's seam: what makes it pass? *(blocks FR-008, US4 scenario 1; phase 5)* — CONTRADICTION

**Measured** at openDox-code `a9ac96f9`, in a bare process with `PYTHONPATH=src`.
`workbench.run_scoped_doc_health(".", ["README.md"])` answers `not-available`:
*"no health check is registered at openDox's health-check seam"*.
`DEFAULT_SCOPED_FAMILIES` is `("status-validity", "tag-hygiene")`, two of
openxFactory's corpus-operations families. A registered check *"refuses a
family it does not carry"*. Release 1's 4.3 made this a seam that a host
registers (`register_health_check`), with *"REFUSAL, NOT A DEFAULT"*. R1Q3 (a)
makes openDox's own defaults registrations that an ENTRY POINT makes, never a
fallback inside a seam.

**The collision.** F6.1 calls the action in a bare process, with the default
families, and asserts `status == "completed"`. With nothing registered it
cannot pass. If openDox's check were registered but carried only neutral
families, it would refuse the two defaults. Requirement 6's sixth scenario
keeps a `Status:`-taxonomy family with its corpus.

**Options.**
- **(a) (Recommended)** The entry points register openDox's own check (R1Q3 (a)
  and R1Q10 (a)'s pattern), and the check answers its OWN family names. The
  registered check declares its default scoped families, and the action asks
  for those when a caller names none, so a host's registration keeps asking for
  its own. F6.1 is amended by a bookkeeping batch to build an entry point
  before the call, as F3.1 line 2 was. *Consequence:* no fallback inside the
  seam, no publisher family names in openDox, and one line of F6.1 changes.
- **(b)** The seam falls back to openDox's own check when nothing is
  registered, and that check accepts the two host family names as aliases.
  *Consequence:* F6.1 stands verbatim, but this reverses 4.3's "refusal, not a
  default" and brings the publisher's family names into the neutral product
  (RULING C2).
- **(c)** `opendox.workbench` registers openDox's check when it is imported,
  and the defaults change to neutral names. *Consequence:* an import side
  effect, which R1Q3 (a) chose against, and F6.1 stands only with the changed
  defaults.

**ANSWER:** _awaiting Brett Heap_

---

## R2Q12 — Is Group 6's check the engine's built-in families, or a second check? *(blocks FR-008, FR-010; phase 5)*

**What is decided.** Group 6 gives the scoped action (`run_scoped_doc_health`,
per-document, over a set's documents) *"something to call"*. Group 14.4 runs the
six neutral families from the view and the CLI, baseline-relative, with results
in the store. Requirement 16 attributes the product's own checks to `opendox`,
*"the one pack no manifest lists"*.

**Options.**
- **(a) (Recommended)** ONE neutral check. The engine's built-in families
  (14.4), attributed to `opendox` (15.7), are what openDox registers at the
  scoped seam (6.2), and the scoped action runs their per-document subset over
  the named documents. *Consequence:* one implementation, and one set of family
  names on every surface.
- **(b)** Two checks: a scoped per-document check for Group 6, and the engine's
  families for 14.4. *Consequence:* two neutral implementations to keep
  aligned, and two answers to "what is wrong with this document".

**ANSWER:** _awaiting Brett Heap_

---

## R2Q13 — Does the health table join RULING Q1's closed list? *(blocks FR-009, US4 scenario 2; phase 5)*

**Two texts.** The ruling `5784155201`, item 4: *"health results become a
seventh table … this lands as an ADDITIVE `0002` migration with the closure test
moved in the SAME change"*. #1144 kept that, corrected the number to `0003_`,
and then left the boundary claim to the realization (14.2; `design.md` §
D10.4): the closure test reads `0001` alone, which is why `0002`'s ledger table
never tripped it. So the realization *"DECLARES"* domain or install-owned, and
says why.

**Options.**
- **(a) (Recommended)** DOMAIN. The results table joins Q1's list in
  `identity.TABLES`, and `tests_runtime/test_schema_shape.py`'s closure text
  moves in the same change, as the ruling's own words have it. Q1's principle
  stands: no document, and a disposable store. *Consequence:* the boundary is
  re-drawn in the open, and `0001`'s digest is untouched.
- **(b)** INSTALL-OWNED, beside the ledger, on the `0002` precedent. No closure
  text moves, and the change says why. *Consequence:* the ruling's "seventh
  table" is read as not joining the list.

**ANSWER:** _awaiting Brett Heap_

---

## R2Q14 — What is a finding's `id`? *(blocks FR-011, FR-015, US5, US6; phase 5)* — CONTRADICTION

**The texts.** F14.1 selects and repairs findings by literal ids:
`broken-link`, `derivable-front-matter`, `stage-location-mismatch`,
`near-duplicate`, `human-only-finding` and `accepted-finding`. It names branches
`health-fix-<id>`, and it reads `{x["id"]: x["resolution_class"]}`. F15.1 uses
`x['id'] == 'broken-link'` and `patch-ok`, `patch-traversal`, …. Requirement 15
needs an exception that *"SHALL cite what it is accepting"*, so that removing it
re-opens that finding, across store resets. A real corpus can carry two
findings of one family. openxFactory's own uncited-resolution rule keys a
finding on `(family, repository, path)` (`openspec/specs/doc-health/spec.md`).

**Options.**
- **(a) (Recommended)** A finding's `id` is a STABLE key that the engine
  derives from the raising pack's id, the family, the document's path and a
  family-supplied locator. It survives a reset, and no two findings share it.
  F14.1 and F15.1 are amended by a bookkeeping batch to look up each planted
  finding by its document, which the fixtures name after its label, instead of
  by a literal id. *Consequence:* exceptions cite something durable. Two
  falsifiers' selection lines change, and branch names are derived from the key.
- **(b)** The `id` is the family's kind name. *Consequence:* the falsifiers
  stand verbatim, but two findings of one family share an id, so neither
  `--finding` nor an exception can tell them apart (requirement 15).
- **(c)** The `id` is the kind name with a numeric suffix (`broken-link-2`).
  *Consequence:* the falsifiers stand, but ids shift when an earlier finding
  disappears, so an exception can attach to the wrong finding after an edit.

**ANSWER:** _awaiting Brett Heap_

---

## R2Q15 — Which class do the unplaced families take? *(blocks FR-012; phase 5)*

**What is decided** (requirement 14; `5784247356`):
- `auto-fix`: a moved link target, front matter derivable from the adapter, a
  stage/location mismatch;
- `assisted`: a near-duplicate, an empty stub;
- `human-only`: *"a decision the product cannot make"*.

**Not placed:** an orphan (a document nothing links to), a stale stub that is
not empty, a broken link whose target did not move, and missing front matter
that the adapter cannot derive.

**Options.**
- **(a) (Recommended)** All four are `human-only`: the product shows the
  evidence and proposes nothing it cannot justify, so `auto-fix` and `assisted`
  stay exactly the ruled lists. *Consequence:* the most conservative reading,
  and the fixture's `human-only-finding` can be any of them.
- **(b)** An orphan and a stale stub are `assisted` (the product proposes a link
  from the nearest neighbour, or proposes deletion). The other two are
  `human-only`. *Consequence:* more help, and two more proposal generators.
- **(c)** The plan decides family by family. *Consequence:* no ruling now, and
  the classes are settled in planning, in the open.

**ANSWER:** _awaiting Brett Heap_

---

## R2Q16 — What is the baseline anchored to? *(blocks FR-010, US4 scenario 4; phase 5)*

**What is decided.** Requirement 6: *"BASELINE-RELATIVE so that new findings get
attention while persistent ones stay quiet and an uncited disappearance is
re-raised"*. Results live in a DISPOSABLE store, whose loss *"SHALL cost a
recomputation rather than a document"*. The engine owns the baseline
(requirement 16).

**Options.**
- **(a) (Recommended)** The baseline is DERIVED, relative to the default
  branch. A finding is "persistent" when a run at the default branch's tip has
  it, and "new" when the working state or a session branch has it and the tip
  does not. After a reset, the next run recomputes it from git. *Consequence:* a
  reset costs only recomputation, as requirement 6 says.
- **(b)** The baseline is the previous stored run. *Consequence:* simple, but a
  reset makes every finding "new" once, and loses the history of what had
  disappeared.
- **(c)** The baseline is committed to the corpus. *Consequence:* this
  contradicts *"results are DERIVED DATA and SHALL NOT BE COMMITTED"*, and needs
  a ruling.

**ANSWER:** _awaiting Brett Heap_

---

## R2Q17 — In a neutral corpus, what cites a disappearance? *(blocks FR-010; phase 5)*

**What is decided.** An *"uncited disappearance is re-raised"* (requirement 6,
from the doc-health pattern `5784155201` names). In openxFactory, a citation is
a governance act: a cited change, or a disposition. A neutral corpus has no such
acts, but it has the fix loop's landings and git history.

**Options.**
- **(a) (Recommended)** A disappearance is cited when the commits that removed
  it, on the default branch, include a landing of the fix loop's draft for that
  finding, or a commit whose message names the finding's id in a `Finding:`
  trailer. An uncited one is re-raised once, as a `human-only` finding naming
  the original, which the human can accept. *Consequence:* hand repairs can be
  cited with one trailer, and nothing vanishes unseen.
- **(b)** Only the fix loop's own landings cite, and every other disappearance
  is re-raised. *Consequence:* strict. Every hand edit that fixes a finding
  raises a follow-up.
- **(c)** The neutral product does not track disappearances. *Consequence:*
  this contradicts requirement 6's text, and needs a ruling.

**ANSWER:** _awaiting Brett Heap_

---

## R2Q18 — What does "optionally on commit" mean? *(blocks FR-010; phase 5)*

**What is decided.** 14.4 and `5784155201`: the check runs *"on demand from the
dashboard and the command line and optionally on commit"*. The engine owns
scheduling (requirement 16). No falsifier exercises the on-commit run.

**Options.**
- **(a) (Recommended)** Release 2 runs on demand only. "Optionally on commit"
  is met by a documented one-line hook, `opendox health run --repo-root .`,
  which the user may add, and the product writes nothing under `.git/`.
  *Consequence:* no hook management, and nothing in a user's repository metadata
  that the user did not put there.
- **(b)** An opt-in verb installs a `post-commit` hook. *Consequence:* the
  convenience costs a writer into `.git/hooks`, with tests of its own.
- **(c)** The engine runs after each commit the product itself makes: session
  commits, fix drafts and landings. *Consequence:* automatic within openDox's
  own acts, and blind to commits made outside it.

**ANSWER:** _awaiting Brett Heap_

---

## R2Q19 — Do the product's own checks run in the sandbox? *(blocks FR-017, US6; phase 5)*

**What is decided.** Requirement 16: *"A PACK SHALL RUN IN A SEPARATE PROCESS
INSIDE AN OPERATING-SYSTEM-ENFORCED SANDBOX … Where the platform offers no such
sandbox, packs SHALL NOT RUN."* The product's own checks are attributed *"as the
one pack no manifest lists"*. Requirement 6's second scenario says a document
product that cannot report on its own documents is undelivered.

**Options.**
- **(a) (Recommended)** The product's own neutral checks run IN PROCESS, as
  product code that is always on, on every platform the product supports. Only
  manifest-listed packs run in the sandbox. "The one pack no manifest lists" is
  read as an attribution rule. *Consequence:* without a sandbox, packs do not
  run, but openDox still reports on its own documents.
- **(b)** The built-in checks run in the sandbox too. *Consequence:* uniform,
  but a machine without a sandbox has no health check at all, against
  requirement 6's second scenario.

**ANSWER:** _awaiting Brett Heap_

---

## R2Q20 — What may a pack depend on? *(blocks FR-016, US6; phase 5)*

**What is decided.** A pack is pinned by a source-tree digest (and by a commit
when it is not in the corpus). It runs with *"read-only binds of only the
interpreter paths the pack's runtime needs"*, `PYTHONNOUSERSITE=1`, and nothing
of `$HOME` (15.1b). The fixture packs are Python packages. The contract follows
the `corpus_adapter` protocol pattern (15.1).

**Options.**
- **(a) (Recommended)** A pack is Python source implementing openDox's pack
  protocol. An engine-provided runner runs it inside the sandbox, with the
  install's own interpreter and standard library mounted read-only. It may
  import only the standard library and the neutral contract module the runner
  provides, and no third-party dependency in release 2. *Consequence:* the
  digest pins everything that runs. F1's governance pack must vendor or drop
  what it needs.
- **(b)** A pack may declare third-party dependencies, installed into a
  per-pack environment that the engine manages and pins by hash.
  *Consequence:* richer packs, and a dependency installer and its pins in the
  engine.
- **(c)** A pack is any executable that speaks a JSON protocol on stdout.
  *Consequence:* language-neutral, and the "protocol pattern" of 15.1 becomes a
  wire format instead.

**ANSWER:** _awaiting Brett Heap_

---

## R2Q21 — Does openDox-spec own the health contract's schemas, with a bundle cut? *(blocks FR-016, FR-023; phase 5)*

**Precedent.** R1Q11 (a) and R1Q12 (a): openDox-spec owns the neutral snapshot
schema, and the code leg carries digest-checked copies. Release 1 cut a
`dox-v1.x` minor at the openDox root (T053; T007 batch G at 9.5), and
openDox-spec joined the arc's repositories. Release 2 adds three serialized
artifacts:
- the exceptions file;
- `health/packs.yaml`;
- a finding's neutral shape, on a pack's stdout and in `health list --json`.

Requirement 16 says the contract is one *"the product itself owns"*.

**Options.**
- **(a) (Recommended)** openDox-spec owns a schema for each of the three, and
  the code leg carries digest-checked copies. Release 2 cuts ONE `dox-v1.y`
  minor at the openDox root, under a batch-G style addendum at 9.5, and
  openDox-spec's landings carry 11.0's trailer. *Consequence:* the same shape as
  release 1. A sixth repository joins, and the root owes a tag for the bundle.
- **(b)** The contract is the code leg's protocol and constants only: no
  spec-leg schema, and no bundle. *Consequence:* fewer acts, but a pack author
  reads Python, not a schema.
- **(c)** The schemas live in the code leg, and the bundle is deferred.
  *Consequence:* schemas exist, but outside the leg that owns contracts.

**ANSWER:** _awaiting Brett Heap_

---

## R2Q22 — Is release 2 published to PyPI? *(blocks FR-023; release 2's close)*

**Precedent.** T007 batch O (`5962754358`, `5963162921`) published `opendox`
0.1.0 to PyPI at release 1's cut, by trusted publishing, with one tag `v0.1.0`
at the commit the openDox root's `contracts/code-pin.yaml` names, on your
publish word after AT-R1. 9.5 otherwise owes no tag. Measured:
openDox-code's `pyproject.toml` reads `version = "0.1.0"` at `a9ac96f9`.

**Options.**
- **(a) (Recommended)** Publish `opendox` 0.2.0 to PyPI at release 2's cut, by
  the existing workflow, with one tag `v0.2.0`, on your publish word after
  release 2's acceptance passes, and under a batch-O style addendum at 9.5.
  *Consequence:* `pip install "opendox[local]"` brings the document tool's
  release-2 surface.
- **(b)** No publish. Release 2 is reachable only at the pinned commit.
  *Consequence:* PyPI users stay on 0.1.0.
- **(c)** A publish per phase (0.2.0 at phase 4, 0.3.0 at phase 5).
  *Consequence:* two cuts, two tags and two publish words.

**ANSWER:** _awaiting Brett Heap_

---

## R2Q23 — Does release 2 carry its own end-to-end acceptance, AT-R2? *(blocks FR-024; release 2's close)*

**Precedent.** Release 1 closed on AT-R1, which runs a clean machine and the
browser surface, as an HTTP half in CI (T095) and a browser half on the host
(T096). #1144's release-2 falsifiers are command-line acceptances and named
tests. 14.5's three parity tests prove that the view is served and that its
action list matches the CLI's. They do not prove that a human can complete a
repair from the view.

**Options.**
- **(a) (Recommended)** Define AT-R2 in AT-R1's form, on a clean machine with
  only `opendox[local]` and a plain repository. The Health view lists findings,
  new first. A mechanical repair is drafted from the view, and landed through
  the view's confirm control as a revertible merge commit. An exception accepted
  from the CLI survives `runtime reset`. A session is submitted to a bare
  remote with `gh` absent. It runs as an HTTP half in CI and a browser half on
  the host. *Consequence:* the release is proved as a user meets it, and the
  plan carries two more tasks.
- **(b)** Release 2 closes on #1144's falsifiers (F6.1, F12.1, F12.2, F14.1 and
  F15.1) and the named tests alone. *Consequence:* faster, and the view's own
  flows are proved only by parity.

**ANSWER:** _awaiting Brett Heap_

---

## R2Q24 — Who closes the arc? *(process; no release-2 FR waits on it)*

**Measured.** Plan 034 reads 92 of 96. Its open tasks are T090–T093:
- 9.5, the pins;
- 11.0, the trailer;
- 11.1, the notes;
- F11.1, the guard at the arc's close.

They are performed in every phase and *"left open for the arc's close after
release 2"* (034 SC-006). F9.2 stays open until the `doc_health` direction arc
lands (RULED `5859927858`). The archive needs both releases' evidence
(`5800995035`).

**Options.**
- **(a) (Recommended)** Feature 038 performs 9.5, 11.0, 11.1 and F11.1 in phases
  4–5, and ticks the four boxes at the arc's close. Plan 034's T090–T093 are
  then closed by reference to 038's evidence. The archive act follows as the
  holder's, and is named as blocked until F9.2 closes on the direction arc's
  landing. *Consequence:* one feature owns the close. 034's four tasks close
  without new work there.
- **(b)** Plan 034 keeps T090–T093 and ticks them at the arc's close, and 038
  only runs the per-phase checks and references them. *Consequence:* the close
  is split across two features' bookkeeping.
- **(c)** A separate bookkeeping PR closes the arc after both features.
  *Consequence:* a third record of the same boxes.

**ANSWER:** _awaiting Brett Heap_

---

## R2Q25 — How does openDox-code's required check run the sandbox tests? *(blocks FR-017, US6; phase 5)*

**Measured** at openDox-code `a9ac96f9`. `validate.yml`'s `validate` and
`acceptance` jobs run on `ubuntu-latest`, and no workflow under
`.github/workflows/` installs `bubblewrap` or names `bwrap`. Release 1's FR-006
keeps openDox-code's whole suite running, with no declared exclusion, and 9.4
lets no skip carry a gap. F15.1 names nine sandbox tests, among them
`test_a_pack_has_no_network` and `test_no_descendant_of_a_pack_outlives_its_budget`.
They need a working sandbox. **Not measured:** whether the hosted runner image
lets `bwrap` create the namespaces 15.1b requires.

**Options.**
- **(a) (Recommended)** The required job installs `bubblewrap` and enables what
  the runner needs, so every sandbox test runs in CI, and a step proves that the
  sandbox is live before the suite runs. *Consequence:* the guarantee is
  measured on every PR. If the runner cannot be made to sandbox, the plan
  returns here with that finding.
- **(b)** The sandbox tests run in their own declared job, as AT-R1's
  acceptance job does, reported by name and never skipped silently.
  *Consequence:* the main suite stays as it is, and the sandbox is still proved
  per PR.
- **(c)** The sandbox tests skip in CI with a declared reason, and run on the
  host. *Consequence:* against 9.4's rule, and needs your ruling.

**ANSWER:** _awaiting Brett Heap_
