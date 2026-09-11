# Design: amend-kill-switch-to-declared-test-companion

Status: draft

This record exists because the amendment is small in words and consequential in
kind: it corrects a clause of a RATIFIED decision on a MEASUREMENT, and the
obvious cheaper answer — loosen the tests — would destroy the property the tests
exist for. The measurement is set out first so that the decisions can be read
against figures rather than against a preference.

## 1. The measurement

**What was being attempted.** `extend-merge-master-envelope-to-floor-bot-lanes`
box 3.6 owes an OBSERVATION: throw the kill switch, watch an enrolled lane fall
back to the human merge gate, restore it, watch autonomous approval resume. On
2026-09-11 the throw half was measured before being attempted for real.

**What decision N-4 says, verbatim and as ratified** (the parent's `design.md`):

> **The kill switch is the candidate entry.** Deleting it from
> `.github/merge-approval-envelope.yml` returns the lane to human merges, takes
> one edit, is a code-owner-reviewed act by construction, is read from the base
> branch so it takes effect on the next run, and is visible in the diff forever.

N-4 reached that shape by refusing two alternatives, and both refusals stand:

- a boolean `active:` member — refused as a **schema change**, and because a
  disabled entry still **reads as enrolled**;
- a repository variable — refused as **invisible in the diff**.

The envelope file's own banner repeats the one-edit claim, so the false sentence
exists in two places and the realization must correct the one that is machine-adjacent.

**The figures.** Measured in a throwaway clone at codexFactory `main` =
`0ad92bd5`, with `PYTHONPATH=scripts python3 -m pytest tests/merge-master/ -q`:

| tree | result |
| --- | --- |
| clean | **3993 passed, 28 skipped** |
| the one edit — delete envelope lines 173–356, the `openxfactory-floor-regeneration` mapping and nothing else (356 → 172 lines; the YAML still parses) | **29 failed, 3964 passed, 28 skipped** |

| file | failures |
| --- | --- |
| `tests/merge-master/test_floor_regeneration_enrolment.py` | 17 |
| `tests/merge-master/test_enrolled_surface_config.py` | 7 |
| `tests/merge-master/test_behaviour_snapshot.py` | 3 |
| `tests/merge-master/test_caller_workflows.py` | 1 |
| `tests/merge-master/test_class_floor_differential.py` | 1 |
| `specs/018-per-tree-floor-instance/behaviour-snapshot.json` — the golden digest | (the sixth file; it must move for the three snapshot failures) |

**Why that is fatal to the claim rather than merely inconvenient.**
`tests/merge-master/` sits inside codexFactory's REQUIRED `validate` check:
`.github/workflows/validate.yml` runs `bash scripts/validate-docs.sh`, whose
line 217 lists `tests/merge-master/`. The one edit therefore does not produce a
red local run that a reviewer may wave through; it produces a pull request that
**cannot land**. "Takes one edit" describes an act that is not available.

**The two records.** The measurement is the RESULT posted on openxFactory #745 at
2026-09-11T03:08Z
(https://github.com/opensoft/openxFactory/issues/745#issuecomment-5628853801).
The ruling accepting it — Brett Heap's SELECTION "Accept the finding; file a
successor", 2026-09-11 ~03:40Z, in session, multi-choice — is recorded on
openxFactory #745 comment 5632569506 (2026-09-11T09:42:11Z,
https://github.com/opensoft/openxFactory/issues/745#issuecomment-5632569506)
and on codexFactory #232 (2026-09-11T09:42:12Z).

**What the measurement also settles, and it changes the parent's scenario text.**
`_find_surface` matches on repository AND head ref only — **never on author**.
With the entry removed, ANY `floor/bot-regeneration` pull request returns
`is_candidate: false`, exits **11** (`_EXIT_NOT_CANDIDATE`), reports
`decision=skip`, and posts **no sticky comment**, because the "Explain park or
block" step is gated on `decision == 'park'`. The parent scenario's
"parks for a human" is therefore not observable; what is observable is *no
envelope decision at all, and the pull request left at the human merge gate with
no comment*. The amended scenario is written to the observable behaviour, which
is a correction of the same kind as the one this packet is for.

**The second blocker, recorded for completeness and not answered here.** No real
bot cycle exists to observe: hourly floor-regeneration has reported "nothing
owed" since 2026-09-10T17:22Z, and an APPROVE cannot be constructed by hand
because the class pins `expected_author: openxfactory[bot]`. The candidate entry
is INTACT on codexFactory `main` (blob
`fa8773628ef69dceab3a912740850c0432ffbce3`, 356 lines). This packet removes the
FIRST blocker only, which is exactly what consequence (4) of the ruling says.

## 2. Authoring decisions

### D-1 — The switch is one reviewed edit PLUS its declared test companion (alternative (A)), and the suite is NOT made kill-switch-aware (alternative (B) is refused)

**(A) — RECOMMENDED. Declare the companion.** The kill switch is the removal of
the candidate entry TOGETHER WITH a companion set of conformance-assertion edits
that is DECLARED beside the enrolment. Two properties follow, and they are the
whole case:

1. the withdrawing pull request is **landable** against the required checks,
   because the reviewer applying the declared companion is applying a known,
   pre-agreed set rather than discovering twenty-nine failures; and
2. the companion is itself a **reviewed, diff-visible declaration** — the
   property N-4 chose the candidate entry for in the first place is extended to
   cover the thing that actually makes the act take more than one edit.

It also keeps the honest accounting: the act is not smaller than it is, and the
declaration says so where the next reader will be standing.

**(B) — NOT RECOMMENDED, and refused.** Make the pinning suite
kill-switch-aware: teach the tests to read the enrolled set out of the envelope
rather than pinning ids, so the entry may leave without any assertion moving.

**Why (B) is refused.** *A suite that adapts to the entry leaving no longer
notices it leaving.* The one property worth most in a conformance suite over an
autonomous-merge enrolment is that an enrolment cannot depart quietly. Today
`test_the_envelope_enrols_exactly_two_candidate_classes` asserts
`ids == ["codexfactory-routine-code", "openxfactory-floor-regeneration"]`; under
(B) that assertion becomes a tautology over whatever the envelope currently says,
and the same edit that withdraws a class silently withdraws the check on the
withdrawal. The measurement is explicit that **the pinning is not the defect**:
a suite that did not notice would be strictly worse than one that notices
loudly.

**No formulation of (B) was found that keeps the property, and the reason is
structural rather than a failure of imagination.** Any suite that derives the
expected set from the declaration has, by construction, no independent record of
what the set should be; to keep the notice-it-leaving property it must hold a
second, independent statement of the enrolled set — at which point that second
statement IS a declaration, and the design is (A) with the declaration moved to
a worse place (a test file rather than beside the enrolment). A hybrid — derive
the *shape* from the envelope, pin the *ids* independently — is (A) again, with
the companion partly implicit. (B) is therefore refused not as a close call but
as a route that arrives at (A) or at a weaker guarantee.

**What (A) does NOT do:** it does not relax a single assertion, does not remove a
test, and does not make the withdrawal cheaper in edits. It makes the withdrawal
**declared, landable and reviewed**, which is what N-4 was reaching for.

### D-2 — The declaration site is the envelope's own banner/comment block beside the candidate: no schema change

The companion is declared **in the envelope's banner/comment block, immediately
beside the candidate it belongs to**, naming the exact companion assertions and
artefacts that candidate carries — and it is declared for **EVERY enrolled
candidate class, today `codexfactory-routine-code` and
`openxfactory-floor-regeneration`**, because the requirement binds every
enrolment and nothing is grandfathered.

**Why the least-schema site.** N-4 refused an `active:` member because it is a
schema change and because a disabled entry reads as enrolled. Answering N-4's
"one edit" problem by adding a schema member would reverse that refusal while
claiming to honour it. A comment-block declaration:

- adds **no schema member**, so no envelope consumer, parser, validator or
  reader changes behaviour;
- is **in the same reviewed file**, in the same diff, under the same code-owner
  review, next to the thing it describes — so it cannot be found stale by
  someone reading the candidate;
- is the natural place to also **correct the false "one edit" sentence**, which
  lives in that very banner today.

**And the declaration is kept honest by machinery, not by discipline** (D-2b):
one codexFactory conformance test asserts BOTH halves of the DECLARED companion
against measurement — the declared assertions against the set that actually pins
the enrolment, and the declared artefacts against the paths their own allowlisted
regenerations actually rewrite. Without it, the declaration
rots the first time someone adds a pinning assertion, and it rots invisibly —
the failure mode that produced this packet. With it, a stale declaration is a
failing check on the pull request that made it stale.

**The declaration's SITE and GRAMMAR, fixed (D-2c) — and the sibling-file
option is DROPPED.** The companion is declared **IN
`.github/merge-approval-envelope.yml`, beside the candidate it belongs to, as
COMMENT LINES**. Comments are not schema, so this is consistent with N-4's
refusal of a schema change and with the requirement's "named beside the
enrolment in the same reviewed declaration". The earlier "or a sibling declared
file keyed by candidate id" option is **withdrawn**: it fixed no path, no format
and no discovery rule, so no conformance test could deterministically find the
declaration, and it sat against the requirement's own site rule. One site, one
grammar, one discovery rule.

**The grammar, per candidate.** Immediately after that candidate mapping's `id:`
line, or as the mapping's TRAILING comment block — the realizing companion
change picks ONE placement and the checker reads that one — one line per entry:

- `# companion: <pytest node id>` for each assertion that pins the enrolment,
  the node id being `<path>::<Class>::<test>`, or `<path>::<test>` where there
  is no class. FUNCTION grain, which answers Q-3.
- `# companion-artefact: <repo-relative path> regenerate: <identifier>` for
  each golden or snapshot file whose recorded value moves with the withdrawal.
  FILE grain — and the REGENERATION IDENTIFIER is part of the declaration, not
  an afterthought: the artefact's movement is MEASURED by running that
  regeneration and reading the diff, never inferred, so an artefact with NO
  declared identifier CANNOT BE DECLARED and therefore cannot be part of an
  enrolment's companion. Supplying the missing identifier, and the reviewed
  table row that resolves it, is the realizing companion change's work.

**THE `regenerate:` FIELD IS AN ALLOWLISTED IDENTIFIER, NEVER A COMMAND, AND THE
DECLARATION THEREFORE CANNOT INTRODUCE EXECUTION.** The envelope is a
PULL-REQUEST-EDITABLE file and the conformance test (D-2b) runs inside a
REQUIRED CI check, so a declaration carrying shell text would let a proposed
declaration run arbitrary commands in that runner. It does not, by construction:

- `<identifier>` is a BARE TOKEN — a name, not a command, not an argument, not a
  path, and nothing that is evaluated;
- it is RESOLVED ONLY IN TRUSTED TEST CODE — a fixed `identifier -> argv` table
  held in the conformance test module under codexFactory's `tests/merge-master/`,
  which is code-owner-reviewed test code inside the required check;
- the resolved argv is executed as a LIST WITH NO SHELL
  (`subprocess.run(argv, shell=False)` semantics) from a FIXED cwd of the
  repository root, so no byte of the declaration reaches a shell;
- an identifier ABSENT FROM THE TABLE **fails the check** — it is not looked up
  elsewhere, not guessed at, and never executed.

Adding an identifier is therefore a REVIEWED TEST-CODE CHANGE in the trusted
module, not a declaration edit. That is the whole point of the split: the
declaration names WHICH recording tool an artefact belongs to, and only reviewed
test code decides WHAT that name runs.

**The checker's DISCOVERY RULE, stated so the check is deterministic.** Parse
the envelope text; locate the candidate by its `id:` value; collect every
`# companion:` and `# companion-artefact:` line from there up to the next
candidate's `id:` line, or to the end of the candidates list. **Nothing else
counts as a declaration** — not a comment elsewhere in the file, not a separate
file, not a line held in a test.

**And the check is ONE PROCEDURE OF FIVE STEPS IN A FIXED ORDER (D-2b, stated
exactly here; `tasks.md` § 3.2 carries the same five steps as the realizing
task's own statement of them, and every other mention in this packet points at
that one). It is two equalities plus a non-emptiness rule, and THE ORDER IS PART
OF THE DESIGN rather than an incidental sequencing: every later step consumes
what an earlier step captured or committed.**

1. **CAPTURE THE DECLARATIONS, BEFORE ANYTHING IS EDITED.** Parse the envelope
   AS IT STANDS PRE-WITHDRAWAL and retain, for that class and by the discovery
   rule above, the declared `# companion:` PINNING NODE-ID set and the declared
   `# companion-artefact:` set as (path, regeneration-identifier) pairs; and
   resolve every declared identifier against the trusted module's table in this
   same step, so an identifier absent from the table fails HERE rather than
   being looked up elsewhere or executed. The reason this is FIRST is mechanical:
   step 2 removes those very comment lines from the tree being measured, so a
   test that has not already captured them has no declaration left to compare
   against — the expected values are the CAPTURED ones, never re-read from the
   withdrawn tree.
2. **WITHDRAW AND COMMIT THE BASELINE, BECAUSE WITHOUT IT THE ARTEFACT EQUALITY
   CAN NEVER HOLD.** In the scratch tree, APPLY THE WITHDRAWAL — that class's
   candidate mapping and its companion comment lines removed, and nothing else —
   and **COMMIT IT AS THE BASELINE COMMIT**. Every measurement below is taken in
   that committed tree and against that commit. The reason is mechanical too:
   the tree in which the measurement happens already carries the withdrawal
   edit, so a diff taken against the pre-withdrawal state would report
   `.github/merge-approval-envelope.yml` itself, and a set containing the
   envelope could never equal a set of artefact paths, however correct the
   regeneration was.
3. **MEASURE THE ASSERTIONS, OVER THE CAPTURED NODE LIST.** Let **A** be the set
   of failing pytest node ids obtained by running the pinning suite on the
   baseline commit's tree over **EXACTLY THE NODE IDS CAPTURED AT STEP 1** — an
   explicit node list, **never a directory sweep** of `tests/merge-master/` or of
   anything else. The conformance test asserts that **A equals that class's
   CAPTURED `# companion:` set**, in both directions and order-free, **and that A
   is NOT EMPTY** (below). **The conformance module itself lives in
   `tests/merge-master/` but is NEVER a member of any class's pinning node
   list** — the step-3 run is the captured list and nothing else, so the module
   can neither discover nor invoke itself and no unrelated failure contaminates
   **A**; a declared node id naming the conformance module is refused at step 1.
4. **REGENERATE, AND DIFF AGAINST THE BASELINE COMMIT.** THEN, in that same tree
   and with the baseline commit already made, each CAPTURED artefact is
   REGENERATED by ITS OWN declared allowlisted regeneration — the `regenerate:`
   IDENTIFIER of its `# companion-artefact:` line, resolved to fixed argv in the
   trusted test module (D-2c), run as a list with no shell from a fixed cwd of
   the repository root — and the set of paths **`git diff --name-only
   <baseline-commit>`** reports is compared to that class's CAPTURED
   `# companion-artefact:` path set. Because the withdrawal is already IN the
   baseline, that delta contains **ONLY paths the regeneration changed**. The
   test asserts the two sets are **equal — no more, no less** — in both
   directions and order-free.
5. **RECORD THE RESULT.** Both equalities and the non-emptiness result are
   reported per class, and any failure NAMES THE CLASS AND THE STEP, so the red
   check says which enrolment failed and where rather than only that the
   conformance test failed.

**A PATH-SCOPED DIFF IS DELIBERATELY NOT USED, AND THE REASON IS THE FAILURE IT
WOULD HIDE.** Restricting the diff to the declared paths would make the equality
trivially satisfiable in one direction and would conceal exactly the failure most
worth catching — a regeneration that writes a path NOBODY DECLARED. The
whole-tree diff *against the baseline commit* keeps that detection: an unexpected
generated path appears in the delta, is absent from the declared set, and the
check fails. The baseline removes the false positive; the whole-tree grain keeps
the true one.

**AND THE MEASURED ASSERTION SET MAY NOT BE EMPTY.** Both equalities pass
VACUOUSLY on an enrolment that nothing pins: withdraw the class, no assertion
fails, the measured set is empty, and a declared empty set equals it. That is
precisely the enrolment that could leave unnoticed — the property D-1 refused
alternative (B) in order to protect. So the check requires **A to be NON-EMPTY
for every enrolled class**: an empty measured set is a FAILING check, never a
vacuous pass, and the enrolment is recorded as non-conformant for lacking a
pinning assertion until the companion realization adds one.

**Existence is necessary but is NO LONGER THE CHECK, and the inference it stood
on is WITHDRAWN.** The earlier formulation declared the artefacts,
existence-checked their paths, and took their *moved* property to be proved by
**A** itself — a golden or snapshot artefact moving exactly when its recording
test is in **A**. That inference does not hold, and this record says so rather
than carrying it: the existence of a `# companion-artefact:` path does not prove
it is the file whose recorded value moves; a node id in **A** does not identify
the path its run rewrites; a recording test can fail for a reason that has
nothing to do with this withdrawal; and a shared snapshot can change without any
declared node id naming it. So the artefact half is now measured the way the
assertion half always was — by running something and reading what it reports.
The objection that a pytest run "does not report moved paths" is answered by NOT
ASKING IT TO: the allowlisted regenerations rewrite the artefacts and `git diff
--name-only <baseline-commit>` reports the paths.

**The consequence, stated rather than left implicit:** an artefact with NO
declared regeneration identifier — or with one absent from the trusted module's
table — cannot be declared, so a companion that needs such an artefact is not
declarable until the realizing companion change supplies BOTH the identifier and
the reviewed table row that resolves it. That is a constraint ON THE REALIZATION
(tasks 3.1), not a gap in the rule.

**Alternatives considered and not recommended:** a separate companion manifest
file (a second place to forget); a schema member (D-2's whole objection); a
declaration held only in the test suite (invisible at the declaration, and the
reader most in need of it is reading the envelope).

**D-2d — APPLYING THE COMPANION AT THE THROW, which is a different act from
declaring it and happens at a different time.** D-2b's conformance procedure is
a MEASUREMENT: it runs in a throwaway scratch tree, proves each class's
declaration is complete and exact, and EDITS NOTHING. The realization therefore
moves no assertion and no artefact (`tasks.md` § 3.1, § 3.3). What the
declaration buys is that the throw's author knows, before opening the pull
request, exactly which assertions and artefacts the withdrawal will move — and
APPLYING the companion is the separate, later act this section defines. It is
defined once, in `tasks.md` § 3.6; the same content is recorded here because a
reader of the design should not have to reconstruct it:

- **the throw is ONE codexFactory pull request** carrying exactly three kinds of
  change and nothing else — (i) that class's candidate mapping and its companion
  comment lines removed from the envelope; (ii) for EACH declared `# companion:`
  node id, the MINIMAL REVIEWED EDIT to that assertion's EXPECTATION so that it
  holds in the post-withdrawal tree (an enrolled-id list loses the withdrawn id;
  a helper asserting `len(matches) == 1` asserts the post-withdrawal count) — the
  assertion RE-TARGETED, never deleted, skipped or weakened, and still noticing
  the enrolments that remain; (iii) for EACH declared `# companion-artefact:`,
  the file as produced by its own allowlisted regeneration, the golden digest's
  movement recorded in its movement log as the throw (D-3);
- **"and nothing else" is measurable, not an assurance**: the paths `git diff
  --name-only` reports for that pull request lie within the union of the
  envelope, the files holding the declared node ids and the declared artefact
  paths, and no assertion outside the declared set changes;
- **landability follows rather than being hoped for**: every assertion that
  would fail is one the pull request re-targets and every artefact that would
  move is one it regenerates, so the required `validate` check passes on the
  throw's own tree;
- **the restore is the REVERT of that pull request**, so the mapping, the comment
  lines, the assertions' expectations and the artefacts return together.

**And the figures stay in view.** At today's head the companion for
`openxfactory-floor-regeneration` measures 29 assertions across five test files
plus the golden digest (§ 1's table; the RESULT of 2026-09-11T03:08Z), so the
throw carries a six-file companion beside the envelope edit. That is what N-4's
"one edit" hid. This packet does not shrink the act — it makes it declared,
bounded and reviewable instead of discovered at the moment the switch is thrown.

### D-3 — The golden behaviour digest IS part of the declared companion

`specs/018-per-tree-floor-instance/behaviour-snapshot.json` is named in the
companion, and both the throw and the restore are recorded as **movements** of
it.

**Why, and what the alternative costs.** The digest is the one artefact whose
every movement is individually reasoned in `test_behaviour_snapshot.py`, where
this enrolment is recorded as *"the SIXTH movement"*. The alternative —
exempting the digest from the companion, or teaching it to ignore enrolment
changes — is exactly the (B) failure in miniature and on the worst possible
artefact: the digest's entire purpose is that nothing about the approval
behaviour moves unnoticed. Declaring it, and recording the throw and the restore
each as a movement, keeps the ledger complete: an observation of the kill switch
is a real event in the behaviour history, and it should read as one.

**Consequence, stated rather than discovered:** the throw pull request carries a
digest movement and a reasoned entry for it, and the restore (a revert) carries
the mirror movement. That is two entries in the digest's history for one
observation, and it is correct that it be so.

### D-4 — `## MODIFIED`, not `REMOVED` + `ADDED`, and the requirement header is UNCHANGED

The delta is a single `## MODIFIED Requirements` block whose header is
**character-for-character** the parent's:
`### Requirement: An enrolled autonomous lane carries a one-edit kill switch`.

**Why the header does not move even though its words now under-describe the
act.** The requirement's SUBJECT (an enrolled autonomous lane), SCOPE (the
enrolment declaration and its withdrawal) and AUTHORITY are unchanged; only its
account of the act's shape is corrected. A `REMOVED` + `ADDED` pair would sever
the requirement's identity, break the scenario lineage and the conformance
mapping that reads scenarios back to tests, and present a narrow correction as a
new grant. It would also, in this estate, look like the requirement had been
withdrawn — which is precisely the impression an amendment about kill switches
should not give. A renamed header would do the same at half the cost and none of
the benefit. **A `## MODIFIED` must match the parent's header exactly**, so the
header is also a mechanical constraint, not only a judgement.

**And the target is a SIBLING'S ADDITION, not canon.** The parent is ratified
(2026-09-07, PR #746) but **unarchived**, so the requirement is not yet in the
promoted `openspec/specs/roles-authority-model/spec.md`; it lives at the parent's
own delta `specs/roles-authority-model/spec.md` lines 53–65. The pairing is
declared per requirement in the delta, as `govern-sibling-added-modified-deltas`
requires, and the front matter carries
`sequenced_after: [extend-merge-master-envelope-to-floor-bot-lanes]`. The archive
order follows: this packet SHALL NOT archive before the parent promotes. The
form precedent is `amend-mirror-floor-regeneration-merge-authority`, which did
the same thing against its own then-unarchived parent.

### D-5 — The realization surface is a codexFactory COMPANION change, and this lane authors none of it

openxFactory's half of this packet **carries no code**. The realization is two
surfaces in codexFactory — the banner correction plus companion declaration
(D-2), and the conformance test (D-2b) — authored **by that repository's lane,
after ratification**.

**Why the split.** It is the same split
`extend-merge-master-envelope-to-floor-bot-lanes` made, and it is not
bookkeeping: codexFactory owns the envelope, the suite and the digest; a
cross-repository edit by this lane would take an authorship that repository's
own gates are built to require, and would put the load-bearing edit outside the
review that judges it. **NO RULESET IS EDITED BY ANY AGENT and NO BYPASS ACTOR IS
PROPOSED IN ANY FORM.**

### D-6 — What this packet refuses to carry

Stated as refusals so that a later reader can see they were considered:

- **no throw of the kill switch**, in either repository, by anyone, now — this
  packet amends the ACCOUNT of the switch and never operates it;
- **no edit to the envelope's candidate mapping** — the entry stays exactly as it
  is (blob `fa8773628ef69dceab3a912740850c0432ffbce3`, 356 lines);
- **no schema change and no `active:` member** — N-4's refusal is honoured, not
  reversed;
- **no repository or organization variable, secret or environment-held value** —
  N-4's "invisible in the diff" ground is restated as a `SHALL NOT` in the delta;
- **no ruleset edit, no bypass actor, no merge-queue change**;
- **no codexFactory byte authored by this lane**;
- **no relaxation of any conformance assertion**, and no rewrite of the suite to
  read the enrolment from the envelope (D-1 (B));
- **no contract bundle, no `contract_bundle_version`, no tag, no pin, no digest
  movement** in openxFactory;
- **no edit to the parent packet** `extend-merge-master-envelope-to-floor-bot-lanes`
  — its `tasks.md` was moved by PR #957, merged 2026-09-11T10:50:23Z
  (`54c166cf`); this packet takes its merge-from-main rather than re-writing
  that file — and therefore **no tick of its box 3.6 here**.

## 3. What this does to parent box 3.6's procedure

Box 3.6 is an **OBSERVATION** box. It owes a throw, an observation, a restore and
a second observation. It does **not** tick on a successor being named, and this
pull request ticks it nowhere. What changes is that the procedure becomes
performable, because the throw becomes landable:

| step | before this packet | after this packet is ratified and its codexFactory companion realized |
| --- | --- | --- |
| the throw | delete the candidate entry — one edit, per N-4 — which **reds 29 assertions in a required check and cannot land** | ONE codexFactory pull request carrying the entry's removal **together with exactly the declared companion**, which passes the required checks and lands |
| what to observe | the parent's text says the next pull request "parks for a human" | the next real bot pull request reaches **no envelope decision** — `is_candidate: false`, exit 11 (`_EXIT_NOT_CANDIDATE`), `decision=skip`, **no sticky comment** — and stays at the human merge gate |
| the restore | (unstated) | a **revert** of that same pull request, restoring the entry and the companion assertions in one act |
| the second observation | autonomous approval resumes | unchanged: autonomous approval resumes on the following real bot cycle |
| where it is recorded | — | openxFactory #745 and codexFactory #232, with box 3.6 ticked **on the parent's own packet**, never on this one |

**The remaining blocker is not removed by this packet.** A real bot cycle must
exist to observe, and none does today ("nothing owed" since 2026-09-10T17:22Z);
none can be manufactured, because the class pins `expected_author:
openxfactory[bot]`. Consequence (4) of the ruling states the conjunction
exactly: the observation resumes only after this successor lands **and** a real
bot cycle exists.

## 4. Open questions — declared, not answered

**ANSWERED AT FILING, AND THEREFORE NOT OPEN — the former Q-2, "does the
companion rule bind the OTHER enrolled class, and the next one?": YES — EVERY
ENROLLED CLASS; NOTHING IS GRANDFATHERED.** The requirement binds every enrolled
candidate class, so the realizing codexFactory companion change declares a
companion for EVERY class enrolled in `.github/merge-approval-envelope.yml` at
realization time — today TWO, `codexfactory-routine-code` and
`openxfactory-floor-regeneration` — each MEASURED BY THE SAME FIVE-STEP
PROCEDURE, in the order D-2b fixes and `tasks.md` § 3.2 carries (capture the
declarations, commit the withdrawal as the baseline, measure the assertions over
the captured node list — which may not be empty — regenerate and diff against
the baseline, record), and
`openxfactory-review-lane-repin`
likewise if
`admit-review-lane-repin-to-merge-approval-envelope` realizes and enrols it.
This is a **BLOCKING CLOSURE CONDITION, not a sequencing preference**: tasks 3.1
and 3.2 carry it per class, and tasks § 5.1 states that this packet is **not
archivable while ANY enrolled candidate class lacks a declared companion and a
passing conformance test over BOTH equalities**. It is recorded here rather
than below because an open question may not hold a condition on which archival
depends.

- **Q-1. Should the companion declaration be machine-checkable from
  openxFactory's side too?** D-2b puts both equality checks in codexFactory,
  where both the declaration and the assertions live. A second,
  openxFactory-side check would have to read another repository's tree, which
  this estate does at a pin and a digest, not at a live read. Declared, not
  answered.
- **Q-3. Should the declaration name assertions at test-function granularity or
  at file granularity?** Answered: node-id (function) grain for assertions,
  file grain for artefacts (D-2c).
- **Q-4. Is "landable against the required checks" the right bar, or should it be
  "landable with no further human judgement"?** The chosen bar is observable from
  the platform and is what the finding measured. A stronger bar would have to
  define what judgement the declared companion's application requires — which
  Q-3's granularity question largely determines.
- **Q-5. What records the throw for the digest's own ledger?** D-3 puts two
  movements in the behaviour history for one observation. Whether the digest's
  reasoning convention wants those two entries cross-referenced to each other,
  and to #745 / cxF #232, is a codexFactory convention question.
