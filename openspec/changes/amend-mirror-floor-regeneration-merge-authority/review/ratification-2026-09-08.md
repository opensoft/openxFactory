# Proposal Ratification: amend-mirror-floor-regeneration-merge-authority

Status: record
Kind: decision record

Decision date: 2026-09-08

Ratifier: Brett Heap (openxFactory repository owner) — in session, recorded on
openxFactory issue [#745](https://github.com/opensoft/openxFactory/issues/745),
comment 5586895152

Recorded by: lane `openxfactory-2` (display `openXfactory-2`), session
`78b27179`, on PR [#807](https://github.com/opensoft/openxFactory/pull/807)

**The header shape is the parent's** (`mirror-floor-regeneration-automation/review/ratification-2026-09-06.md`),
because this is an openxFactory record; **the content follows the twin's**
(codexFactory `amend-floor-regeneration-merge-authority/review/ratification-2026-09-08.md`),
because this packet is that packet's lockstep mirror and the two records are
meant to be read side by side.

## The word

Brett Heap (openxFactory repository owner), in session, **2026-09-08T14:39:02Z**,
verbatim:

> **"merge 292 when green, then ratify 807"**

Recorded on openxFactory issue
[#745](https://github.com/opensoft/openxFactory/issues/745), comment
**5586895152**, created **2026-09-08T14:39:04Z**.

**IT IS A TWO-ACT WORD AND THIS IS ITS SECOND ACT.** The first — *"merge 292 when
green"* — was performed by the landing lane: codexFactory
[#292](https://github.com/opensoft/codexFactory/pull/292), the finding-2
REALIZATION (the lane arms the platform's auto-merge, never merges), merged into
codexFactory `main` at **2026-09-08T15:26:33Z**, merge commit
**`406a2afb8cce758ed645a5f9217a395fb9452246`**, over head `59de5d0c`. This record
belongs to the second act.

**IT IS A DIFFERENT WORD FROM THE ONE THAT COMMISSIONED THE AUTHORING.** That
one — 2026-09-08T13:22:40Z, *"rule on finding 3, do the mirror packet too"*
(#745 comment 5585824802; codexFactory #232 comment 5585824548) — ruled a finding
in the OTHER repository and commissioned this authoring. It ratified no text
here, and the packet said so in its own header. **This word ratifies the text.**

## The head it was given over, and the condition it names

*"when green"* attaches to the FIRST act by its grammar. The landing lane's own
statement of the word applies the same condition to this one — *"then
openxFactory #807 … receives its ratifying commit … and lands under its own
Rule 6 window … once green with every thread resolved"* — and it was met before
this record was written. Measured on pull request
[#807](https://github.com/opensoft/openxFactory/pull/807) at head
**`b910e97d86a979f12b814b8c4953a8e9201a0358`**:

* required and advisory checks: `pytest-suite` **pass**; `clearing-dispatch-gate`,
  `lane-line`, `merge-master-approval`, `openreposhape-pin`, `openspec-cli-pin`,
  `wallet-validation`, `release-tag-gate`, `signed-execution-chain-gate` **all
  pass**;
* review threads: **2 raised — one by Codex (P1) and one by Copilot — both fixed,
  replied to and RESOLVED; 0 unresolved**;
* `closingIssuesReferences`: **empty** — #745 and codexFactory #232 are
  referenced with `Refs`, never with a closing keyword;
* the pull request was a DRAFT throughout authoring and is taken out of draft by
  the same act this record belongs to.

**`pytest-suite` WAS RED ONCE, ON `70eac2d7`, AND THE FAULT WAS THIS PACKET'S.**
`tests/doc-health/test_modified_block_currency_self_gate.py`'s two sibling-pairing
assertions reported this packet's MODIFIED block as `undeclared`: the requirement
it restates is not in canon, because `mirror-floor-regeneration-automation` is
ratified but not yet archived, so the basis is an ACTIVE SIBLING'S ADDITION and
`govern-sibling-added-modified-deltas` requires a `Modified over` marker in the
requirement body. The marker was added rather than the test adjusted, and the
family's `sibling-pairing declaration` arm went **1 → 0**.

## What it ratifies

**The PROPOSAL, and one `## MODIFIED` requirement in it.**
`specs/review-lane-floor-mirror/spec.md` restates
`mirror-floor-regeneration-automation`'s requirement *"An automated pin advance
only ever proposes"* in full, narrowing "SHALL NOT merge" to "SHALL NOT merge
**by its own act**" and admitting that the lane **MAY arm the platform's
auto-merge** on its own pull request, so that the merge completes only when (a)
the merge-master envelope approval for that exact head stands and (b) every
required check has succeeded. *"SHALL NOT approve"* is untouched, and so is the
default-branch bar, restated as a bar on the LANE'S OWN WRITES.

**Ten scenarios in the block: seven added, one carried with narrowed bullets, two
carried verbatim.** The seventh added scenario is not in codexFactory's twin and
exists because Codex's P1 on this pull request found a real contradiction: the
block's *"no second act after the arming"* forbade the single-flight UPDATE the
parent's *The automated advance lane is triggered by the pinned core's own
movement and every firing is idempotent* REQUIRES. The prohibition is now *"no
second act TOWARD THE MERGE"*, the delivery/disposal boundary is stated in the
requirement, and the armed state's fate on an update is measured rather than
assumed (GitHub disables auto-merge only on a push by an actor WITHOUT write
permission; this lane's declared identity holds `contents: write`).

## Which decisions stand — M-A through M-G, one line each

**NONE VETOED. ALL SEVEN STAND AS RECOMMENDED**, which is the same shape
`mirror-floor-regeneration-automation`'s M-1..M-7,
`extend-merge-master-envelope-to-floor-bot-lanes`'s N-1..N-5 and codexFactory's
D-1..D-7 were ratified in. Each remains one edit away from a veto.

* **M-A — where the arming happens.** STANDS: arm immediately after the pull
  request is opened OR updated, inside the existing "Open or update the single
  automated advance" step, on the same App token, idempotently on both paths —
  and, as amended in review, an already-armed pull request stays UPDATABLE and is
  re-armed on the update.
* **M-B — the merge method.** STANDS: `--squash`, platform-default message. A real
  choice here and not in codexFactory, which permits only a merge commit; squash
  is recommended on PR #732's observed precedent.
* **M-C — what remains forbidden, and how the tests say so.** STANDS: narrow
  exactly two of the ten swept terms for the workflow only, assert the admitted
  form by EQUALITY, and ADD the driver-side control this repository does not have.
* **M-D — the realization gate.** STANDS in all three parts: name the enrolment
  successor `admit-review-lane-repin-to-merge-approval-envelope` and do NOT author
  it here; recommend **NO bypass actor on any ruleset**, here or in the org; and
  leave the COMPLETION PATH open for a word, with the cheap precondition measured
  first.
* **M-E — observability.** STANDS: one notice and one summary line on arming, and
  one line on the next firing saying what became of the armed pull request.
* **M-F — scope.** STANDS: ONE `## MODIFIED` block, over ONE requirement, in ONE
  capability, and no second delta of any kind.
* **M-G — the live proof.** STANDS: the realization evidence is SPLIT, and the
  second half — one real unattended cycle — is not this packet's to produce.

## What it does NOT decide, and this was checked rather than assumed

* **BOX 1.3 IS NOT RULED BY THIS WORD.** Whether the realization lands INERT (the
  recommendation) or waits for the enrolment successor is a sequencing choice the
  word does not touch, and the word says as much in its own recording: *"Its
  realization stays gated on the enrolment successor … and on the shape-1
  measurement — not part of this word."* **Both answers are conforming** — the
  requirement admits the inert state by name — so the box stays open and names
  the act that ticks it.
* **NOTHING IS REALIZED BY THE RATIFICATION.** No workflow is edited, no test is
  flipped, no envelope byte moves, no ruleset is touched, and
  `contracts/review-lane-pin.yaml`, `contracts/review-lane-floor-snapshot.yaml`,
  `merge-master-approval.yml`'s `PINNED_CORE_COMMIT` and both checkout refs are
  byte-unchanged.
* **NO SUCCESSOR IS FILED.** `admit-review-lane-repin-to-merge-approval-envelope`
  is NAMED in `proposal.md` and `design.md` M-D and is not authored; box 3.1 says
  what files it.
* **NO OTHER PACKET'S TEXT MOVES.** `mirror-floor-regeneration-automation`,
  `extend-merge-master-envelope-to-floor-bot-lanes` and the archived
  `mirror-floor-addition-grace` are untouched by this act.
* **THE ARCHIVE IS A SEPARATE, LATER WORD**, and it is held twice over: by
  `release-realization` (a code surface archives on merged-plus-green realization
  evidence) and by the `Modified over` pairing, which holds this packet until
  `mirror-floor-regeneration-automation` promotes.

## Which boxes this ratification ticks, and why only that one

**ONE — box 1.1 — on the landing lane's instruction, and the deviation from the
packet's own preamble is disclosed rather than taken quietly.**

* **1.1 — ratify or refuse.** Discharged by the word above, by this record, and by
  `proposal.md`, `design.md` and `tasks.md` moving to `Status: ratified` with
  their citation lines, which is exactly the box's own stated tick condition.
* **1.2 — veto or let stand M-A through M-G.** Its stated tick condition is *"the
  ratification record naming which decisions stand and which are vetoed — one
  line each, including 'none vetoed' if that is the answer"*, and the section
  above answers precisely that, one line each, none vetoed. **THE BOX IS
  NEVERTHELESS LEFT OPEN**, on the landing lane's explicit instruction to tick
  only the box the packet's own rule says ratification ticks. The tension is
  stated rather than resolved by an unauthorised tick: **say the word and 1.2
  ticks in one edit**, citing this section. (codexFactory's twin ticked both and
  disclosed the deviation the other way; the two records are consistent in
  disclosing, not in the count.)
* **1.3 stays open** because the word does not rule it, as recorded above.
* **§ 2 stays open**: its boxes describe the canon text, and what PROVES them is
  the realization landing green against it — the preamble says so in terms.
* **§ 3, § 4 and § 5 stay open**, each naming its own act.

**THE PACKET'S TICK-DISCIPLINE PREAMBLE IS CORRECTED IN THE SAME COMMIT RATHER
THAN LEFT TO CONTRADICT THE TREE.** It read that this pull request "performs
nothing but the proposing" with "EVERY BOX UNTICKED", and cited the parent and
the twin as ratifying with everything unticked. That was true of the parent and
NOT of the twin, which ticked 1.1 and 1.2; and it stopped being true of this pull
request the moment the ratification landed inside it. The sentence is amended to
say what actually happened.

## ADDENDUM 2026-09-09 — THE TWO BOXES THIS RECORD LEFT OPEN ARE RULED

**APPENDED, NOT A REWRITE.** Every word above is the record of 2026-09-08 and is
left standing exactly as it was written, including the two passages this
addendum supersedes — a record that is edited to agree with a later word stops
being evidence of what was decided when. What changed is a second and a third
word from the same ratifier, one day later, and they are recorded here beside
the first.

**BOX 1.3 — RULED: THE REALIZATION LANDS INERT.** Brett Heap, in session,
**2026-09-09T11:48:21Z**, verbatim:

> **"rule land inert, this lane realizes it"**

Recorded on openxFactory issue
[#745](https://github.com/opensoft/openxFactory/issues/745#issuecomment-5601338925),
comment **5601338925**. The recommendation of `design.md` M-A's last alternative
is taken: the arming lands NOW rather than waiting for
`admit-review-lane-repin-to-merge-approval-envelope`, **with the inertness
DECLARED in the workflow's own witness line and reported in the run summary** —
`NO CANDIDATE CLASS ADMITS THIS LANE TODAY, so the arming is inert: the pull
request waits for the same human merge word a hand-authored advance needs, until
admit-review-lane-repin-to-merge-approval-envelope lands.` **The section *What it
does NOT decide* above, at its first bullet — "BOX 1.3 IS NOT RULED BY THIS
WORD" — is TRUE OF THE 2026-09-08 WORD and superseded by this one.** Box 4.3
(filing the successor) is NOT ruled by it and stays open.

**BOX 1.2 — RULED: NONE VETOED.** Brett Heap, in session, **2026-09-09**,
verbatim:

> **"none vetoed, merge it when green, then report the next sweep"**

Recorded on openxFactory issue
[#745](https://github.com/opensoft/openxFactory/issues/745#issuecomment-5601413264),
comment **5601413264**. **M-A THROUGH M-G ALL STAND AS RECOMMENDED, none
vetoed** — the answer this record's § *Which decisions stand* already carried
one line each, now given the word that ticks the box. **The passage above at
*1.2 — veto or let stand*, which held the box open on the landing lane's
instruction and said "say the word and 1.2 ticks in one edit", is superseded by
this ruling; that one edit is made in `tasks.md` in the realizing pull request.**
The word's second and third clauses — the merge and the next-sweep report — are
the LANDING lane's acts and are claimed by no box here.

**THE CODEX P1 RESIDUAL — RULED: ACCEPTED, AND RECORDED RATHER THAN CLOSED.**
Brett Heap, in session, **2026-09-09T13:57:49Z**, verbatim:

> **"accept the residual, record it"**

Recorded on openxFactory issue
[#745](https://github.com/opensoft/openxFactory/issues/745#issuecomment-5603082637),
comment **5603082637**. **THE RESIDUAL, STATED EXACTLY.** The arming lives
inside the delivery step *Open or update the single automated advance*, which is
gated `steps.repin.outputs.action == 'advance'`, so a firing on which the pinned
core has not moved never reaches it: **a refused arming is re-attempted only on
the next firing that DELIVERS an advance, and that firing moves the head
first.** **IT IS ACCEPTED AS THE CONFORMING SHAPE.** No third
`gh pr merge --auto` occurrence is added — decision **M-C's ratified
exactly-twice equality stands untouched**, and the named negative control still
reds at three; no amendment is opened; and the residual is **DISCLOSED WHERE THE
RUN IS READ** rather than closed, on both surfaces and in the same words: the
delivery step's refusal witness and the no-op firing's outcome report, commit
**`d368b07b`** on PR
[#844](https://github.com/opensoft/openxFactory/pull/844), measured by
`test_a_refused_arming_is_a_recorded_outcome_not_a_failed_advance` and
`test_the_not_armed_branch_states_the_retry_condition_when_rendered`. **WHAT
WOULD LET AN ARMED STATE COMPLETE ANYTHING IS UNCHANGED BY THIS WORD:**
`admit-review-lane-repin-to-merge-approval-envelope` (box 4.3, unfiled, needs
its own word), and until it lands the armed state is inert by box 1.3's ruling
above. **THIS WORD TICKS NO BOX.** It answers a finding raised on the REALIZING
pull request, not on the packet's text; box 3.5's evidence carries it, and the
packet's decisions are where the 2026-09-08 word and the two rulings above left
them.

**WHAT THIS ADDENDUM DOES NOT DO.** It ratifies nothing new: the proposal was
ratified on 2026-09-08 and its text has not moved. It performs no merge, files
no successor, touches no ruleset and enrols no candidate. The realization it
authorizes is a separate pull request whose own diff is the evidence for § 3,
and which, by box 1.3's ruling, is observably INERT until the enrolment
successor lands.

## Scope

This record ratifies the PROPOSAL. **The realization is a later word and a
separate pull request**, and it is gated on the enrolment successor existing —
today openxFactory's merge-approval envelope enrols only `intent-rolling-custody`,
so no candidate class admits `bot/review-lane-repin` and an armed auto-merge here
would have no approver. `tasks.md` § 5 says what the archive waits on.
