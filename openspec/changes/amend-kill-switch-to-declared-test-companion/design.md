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

**AND `<repo-relative path>` IS A NORMALIZED POSIX REPOSITORY-RELATIVE PATH
CONTAINED IN THE CHECKOUT AND TRACKED AT THE CONTROL BASELINE — THE GRAMMAR
ADMITS NOTHING ELSE.** The envelope is a
PULL-REQUEST-EDITABLE file and the procedure below reads the declared path from
disk, so an unconstrained path would let a proposed declaration name a location
outside the repository or be compared in a non-canonical spelling. It cannot, by
construction: the declared path is POSIX (forward slashes only), relative to the
repository root, and ALREADY NORMALIZED. Step 1 REFUSES ANYTHING ELSE AT
CAPTURE, IN TWO STAGES — and THE REFUSAL SET IS THE SPEC'S OWN. The `## MODIFIED`
requirement states that set normatively; this paragraph, task 3.2's step 1 and
the scenarios REPEAT THAT ONE SET VERBATIM rather than each carrying a list of
its own, because a refusal set that drifts between the three sites is a
declaration the checker and the specification disagree about.

- **(a) LEXICAL REFUSAL FIRST, TOUCHING NO FILESYSTEM AT ALL.** The declaration
  is refused where the declared path is AN ABSOLUTE PATH, CARRIES ANY `..`
  SEGMENT, ANY `.` SEGMENT, A BACKSLASH, AN EMPTY SEGMENT, A TRAILING SLASH,
  ANY NON-POSIX SEPARATOR, ANY PATH OR SEGMENT BEGINNING WITH `-`, ANY GLOB OR
  PATHSPEC-MAGIC CHARACTER (`*`, `?`, `[` OR `]`), OR A LEADING `:`. This stage
  is pure string work: it opens nothing,
  stats nothing and resolves nothing, so a hostile spelling is thrown out before
  the filesystem is consulted at all.
- **(b) THEN CONTAINMENT, WHICH MAY CONSULT METADATA BUT READS NOTHING.** Only a
  path that SURVIVES (a) is RESOLVED, following symlinks, and the resolved result
  is required to lie under the repository ROOT'S OWN RESOLVED PATH. Resolution
  necessarily consults metadata — which is why this stage is NOT claimed to
  precede every filesystem access, a claim that would be false of any resolution
  — but IT DOES NOT OPEN OR READ THE ARTEFACT BEFORE CONTAINMENT HOLDS, so no
  read ever follows a declaration out of the checkout and no comparison is ever
  made on a non-canonical spelling.

A refusal at EITHER stage FAILS THE CONFORMANCE CHECK, NAMING THE REFUSAL CLASS
AND THE OFFENDING DECLARATION.

**AND (c) THE PATH IS TRACKED AT THE CONTROL BASELINE, WHICH IS WHY AN IGNORED
OUTPUT IS NOT A DECLARABLE ARTEFACT.** A `# companion-artefact:` names a RECORDED
VALUE — the golden digest is the case in point — and a recorded value lives in
the tree. Step 1 therefore ALSO refuses a declared path that version control does
not TRACK at the control baseline (`git ls-files --error-unmatch -- <path>` in
the hermetic scratch repository, the path passed AFTER `--` and under
`GIT_LITERAL_PATHSPECS=1`, so a pull-request-editable declaration reaches git as
an OPERAND MATCHED LITERALLY — never an option, never a pathspec pattern; the
lexical refusal above already rejects a leading `-`, a leading `:` and every
glob or pathspec-magic character, and this is the second belt behind it), as a
conformance failure against the class. The
consequence is deliberate and is the reason the rule is stated: a tool whose
output the repository IGNORES cannot have that output DECLARED, so the barrier's
`git clean -fdx` can never delete a declared artefact, and an ignored path
appearing in any inventory is an ACCIDENTAL output that fails step 4 — never a
correctly declared one the control run could never pass.

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

**And the check is ONE PROCEDURE OF FIVE STEPS IN A FIXED ORDER — STEP 2 IN TWO
LETTERED HALVES, THE CONTROL RUN (2a) BEFORE THE WITHDRAWAL (2b) — (D-2b, stated
exactly here; `tasks.md` § 3.2 carries the same five steps as the realizing
task's own statement of them, and every other mention in this packet points at
that one). It is two equalities, a DETERMINISM CONTROL and a non-emptiness rule,
and THE ORDER IS PART OF THE DESIGN rather than an incidental sequencing: every
later step consumes what an earlier step captured or committed.**

1. **CAPTURE THE DECLARATIONS, BEFORE ANYTHING IS EDITED.** Parse the envelope
   AS IT STANDS PRE-WITHDRAWAL and retain, for that class and by the discovery
   rule above, the declared `# companion:` PINNING NODE-ID set and the declared
   `# companion-artefact:` set as (path, regeneration-identifier) pairs; and
   resolve every declared identifier against the trusted module's table in this
   same step, so an identifier absent from the table fails HERE rather than
   being looked up elsewhere or executed; and APPLY D-2c's TWO-STAGE PATH REFUSAL
   to EVERY DECLARED PATH in this same step — first the LEXICAL refusal, which
   touches no filesystem at all, of an ABSOLUTE PATH, ANY `..` SEGMENT, ANY `.`
   SEGMENT, A BACKSLASH, AN EMPTY SEGMENT, A TRAILING SLASH, ANY NON-POSIX
   SEPARATOR, ANY PATH OR SEGMENT BEGINNING WITH `-`, ANY GLOB OR
   PATHSPEC-MAGIC CHARACTER (`*`, `?`, `[` OR `]`), OR A LEADING `:`, and then,
   for a path that survives it, CONTAINMENT: the path
   RESOLVED, following symlinks, and the result required to lie under the
   repository root's OWN RESOLVED PATH, a stage that may consult metadata but
   DOES NOT OPEN OR READ THE ARTEFACT BEFORE CONTAINMENT HOLDS. A refusal at
   either stage happens HERE, naming the refusal class and the offending
   declaration, rather than the declaration being read or existence-checked
   outside the checkout. **AND THE DECLARED PATH MUST BE TRACKED AT THE CONTROL
   BASELINE** — `git ls-files --error-unmatch -- <path>`, the path AFTER `--`
   and under `GIT_LITERAL_PATHSPECS=1` so it is an operand matched literally
   rather than an option or a pattern, in the hermetic scratch
   repository, on the pre-withdrawal tree 2a commits unchanged as that baseline
   — so AN IGNORED OR UNTRACKED PATH IS NEVER DECLARABLE: a recorded value lives
   in the tree by definition, and a declaration naming a path version control
   does not track is a conformance failure against the class, refused here
   rather than discovered at step 4 as an equality that could never hold. The
   reason this is FIRST is mechanical:
   step 2b removes those very comment lines from the tree being measured, so a
   test that has not already captured them has no declaration left to compare
   against — the expected values are the CAPTURED ones, never re-read from the
   withdrawn tree.
2. **2a — CONTROL: COMMIT THE PRE-WITHDRAWAL TREE AND PROVE EVERY ALLOWLISTED
   TOOL A NO-OP ON IT; THEN 2b — WITHDRAW AND COMMIT THE BASELINE, BECAUSE
   WITHOUT IT THE ARTEFACT EQUALITY CAN NEVER HOLD.**
   **2a — THE CONTROL RUN, AND IT COMES FIRST BECAUSE IT IS WHAT MAKES EVERY
   LATER DELTA ATTRIBUTABLE TO THE WITHDRAWAL AT ALL.** In the hermetic scratch
   repository this step constructs (below), COMMIT THE TREE AS IT STANDS
   PRE-WITHDRAWAL as the **CONTROL BASELINE**; then run **EVERY identifier in the
   allowlist table** against that control baseline through the SAME loop step 4
   fixes — BARRIER, then RUN, then INVENTORY, one tool at a time — and REQUIRE
   **EVERY CONTROL INVENTORY TO BE EMPTY**. An allowlisted recording tool is
   REQUIRED to be DETERMINISTIC AND IDEMPOTENT: run on the tree it was last run
   on, it writes nothing. **A NON-EMPTY CONTROL INVENTORY IS A CONFORMANCE
   FAILURE AGAINST THAT IDENTIFIER**, recorded BEFORE the withdrawal is measured,
   and **ONLY AN IDENTIFIER THAT PASSED THE CONTROL RUN HAS ITS POST-WITHDRAWAL
   DELTA COUNTED**. Without it the artefact equality never establishes that a
   path moved BECAUSE OF the withdrawal: a generator that rewrites its output on
   EVERY run — a recorded timestamp, a nonce, an unordered map — produces its
   delta whatever the tree holds, and step 4 would attribute that delta to the
   class exactly as it attributes a real movement. With it, every attributed path
   is one THE WITHDRAWAL CAUSED. **AND EVERY ALLOWLISTED INVOCATION — HERE AND
   IN STEP 4 — RUNS WITH INTERPRETER CACHES SUPPRESSED**: `PYTHONDONTWRITEBYTECODE=1`
   and `PYTHONPYCACHEPREFIX` pointed OUTSIDE the scratch tree, the companion
   design naming the equivalent for any non-Python runtime it allowlists.
   Determinism is BYTE-IDENTITY OF THE WHOLE TREE, ignored and untracked paths
   included: a tool that leaves a cache or a scratch file behind is
   non-conformant rather than excused, and suppressing the interpreter's own
   caches keeps that demand about THE TOOL rather than about the runtime that
   ran it.
   **2b — THE WITHDRAWAL AND ITS BASELINE.** In the scratch tree, APPLY THE WITHDRAWAL — that class's
   candidate mapping and its companion comment lines removed, and nothing else —
   and **COMMIT IT AS THE BASELINE COMMIT**. Every measurement below is taken in
   that committed tree and against that commit.
   **BOTH COMMITS ARE MADE IN ONE HERMETIC SCRATCH REPOSITORY, NEVER IN AN
   INHERITED GIT ENVIRONMENT.** The scratch tree is a repository OF ITS OWN — `git init`-ed
   there, or a `git worktree` whose PRIVATE git directory is NAMED ON EVERY CALL
   rather than exported into the environment — carrying
   repository-LOCAL `user.name` and `user.email` set to FIXED TEST CONSTANTS,
   with `GIT_CONFIG_GLOBAL=/dev/null` **ALWAYS**, TOGETHER WITH **EITHER**
   `GIT_CONFIG_SYSTEM=/dev/null` **OR** `GIT_CONFIG_NOSYSTEM=1` — those two being
   the alternative spellings of the SYSTEM half ALONE, and
   **`GIT_CONFIG_NOSYSTEM=1` IS NEVER A SUBSTITUTE FOR THE PAIR**: it suppresses
   the SYSTEM file only and leaves the user's GLOBAL configuration fully active,
   which is exactly where a developer's `core.hooksPath` (husky, lefthook,
   `pre-commit`) and `commit.gpgsign` live, so pointing GLOBAL at `/dev/null` is
   the half that cannot be dropped. And `core.hooksPath` pointed at an EMPTY
   DIRECTORY, and `commit.gpgsign=false` and `tag.gpgsign=false`.
   **AND THE ENVIRONMENT IS CLEARED, NOT MERELY ADDED TO: EVERY INHERITED `GIT_*`
   CONTROL VARIABLE IS UNSET** — `GIT_DIR`, `GIT_WORK_TREE`, `GIT_INDEX_FILE`,
   `GIT_COMMON_DIR`, `GIT_OBJECT_DIRECTORY`, `GIT_ALTERNATE_OBJECT_DIRECTORIES`,
   `GIT_NAMESPACE`, `GIT_CEILING_DIRECTORIES`, and every other `GIT_*` name the
   caller happens to export — leaving ONLY the THREE this procedure sets itself:
   `GIT_CONFIG_GLOBAL=/dev/null` ALWAYS, EITHER `GIT_CONFIG_SYSTEM=/dev/null` OR
   `GIT_CONFIG_NOSYSTEM=1` BESIDE IT — never that one in place of the GLOBAL
   setting — and `GIT_LITERAL_PATHSPECS=1`.
   **AND `GIT_LITERAL_PATHSPECS=1` BELONGS HERE BECAUSE A DECLARED PATH IS AN
   OPERAND, NEVER A PATTERN AND NEVER AN OPTION**: every git invocation that
   RECEIVES a declared path passes it AFTER `--` and under literal-pathspec mode
   (equivalently the `:(literal)` magic on each pathspec) — `git ls-files
   --error-unmatch -- <path>` for step 1's tracked-path check, and likewise any
   status or diff call scoped by a declared path — so a filename beginning with
   `-` cannot parse as a flag and a glob or pathspec-magic character cannot
   match some OTHER tracked path. It is the second belt: D-2c's lexical refusal
   already rejects those spellings, and `--` with literal pathspecs means one
   that somehow survived could still not be re-interpreted.
   **And EVERY git call in steps 2 and 4 NAMES ITS REPOSITORY EXPLICITLY** — an
   explicit `--git-dir`/`--work-tree` pair, or `-C <scratch>` after `git init`
   there — so that nothing inherited can redirect a commit or a measurement.
   Setting hermetic VALUES is not enough on its own: an inherited `GIT_DIR`,
   `GIT_WORK_TREE`, `GIT_INDEX_FILE` or `GIT_COMMON_DIR` silently aims the
   scratch commit and the step-4 diffs at ANOTHER repository, and the procedure
   then measures a tree it never withdrew anything from — a green check on the
   wrong tree, which is worse than a red one. THE SAME ENVIRONMENT GOVERNS
   step 4's `git status` inventory and reset calls, and 2a's control loop, which
   is that same loop run against the control baseline.
   This repository already records why, and the precedent is cited rather
   than paraphrased: a CI runner carries no ambient git identity, so an un-pinned
   scratch commit dies there with `Author identity unknown` while passing on a
   developer's machine, and a developer's GLOBAL config can carry `core.hooksPath`
   (husky, lefthook, `pre-commit`) or `commit.gpgsign`, either of which then runs
   or refuses inside the throwaway repository — both directions the same defect,
   that the ambient installation must not change the answer
   (`tests/openxwallet_pin/test_verify_pin.py`, the `_hermetic_git` account at
   lines 32–42). The reason the COMMIT itself belongs here is mechanical too:
   the tree in which the measurement happens already carries the withdrawal
   edit, so a diff taken against the pre-withdrawal state would report
   `.github/merge-approval-envelope.yml` itself, and a set containing the
   envelope could never equal a set of artefact paths, however correct the
   regeneration was.
3. **MEASURE THE ASSERTIONS OVER AN INDEPENDENT, COMPLETE PINNING INVENTORY.**
   Let **A** be the set of failing pytest node ids obtained by running, on the
   baseline commit's tree, **THE WHOLE PINNING SUITE (`tests/merge-master/`) WITH
   THE CONFORMANCE MODULE ITSELF EXCLUDED BY PATH** — `pytest --ignore=<the
   conformance module's path>`, that path being a CONSTANT IN TRUSTED TEST CODE
   and never a value read from a declaration. **WHAT IS RUN IS NOT DERIVED FROM
   THE DECLARATION**: the captured `# companion:` set is the EXPECTED value only,
   so a pinning assertion the declaration OMITS is still run and still enters
   **A**. The conformance test asserts that **A equals that class's CAPTURED
   `# companion:` set**, in both directions and order-free, **and that A is NOT
   EMPTY** (below). **The conformance module itself lives in
   `tests/merge-master/` but is EXCLUDED BY ITS OWN PATH FROM EVERY MEASUREMENT
   AND IS NEVER ITSELF MEASURED** — self-invocation is prevented by that
   exclusion, not by narrowing the run; a declared node id naming the conformance
   module is refused at step 1 for the same reason.
4. **REGENERATE EVERY ALLOWLISTED ARTEFACT ONE TOOL AT A TIME, AND ATTRIBUTE
   EACH CHANGED PATH TO THE IDENTIFIER THAT PRODUCED IT.** THEN, in that same
   tree and with the baseline commit already made,
   **EVERY REGENERATION IN THE TRUSTED MODULE'S ALLOWLIST TABLE — the whole
   table, not only the identifiers this class declared** — is run, each resolved
   to fixed argv in that module (D-2c) and run as a list with no shell from a
   fixed cwd of the repository root. **THEY ARE RUN ONE AT A TIME AND EACH RUN IS
   MEASURED ALONE, AND EVERY ITERATION OF THAT LOOP OPENS WITH A RESET BARRIER —
   THE FIRST ITERATION INCLUDED**: per identifier the loop is BARRIER, then RUN,
   then INVENTORY, in that order.
   **THE BARRIER RESETS BOTH THE INDEX AND THE WORKTREE TO THE BASELINE COMMIT** —
   `git reset --hard <baseline-commit>` followed by `git clean -fdx`, the `-x`
   being what removes ignored files — issued in step 2's hermetic environment with
   its explicit `--git-dir`/`--work-tree`, and then VERIFIES THE TREE EMPTY with
   **THE SAME `git status --porcelain=v1 --untracked-files=all
   --ignored=matching` CALL REPORTING NOTHING**, and only then does that
   identifier run. Stating the barrier at the HEAD of the loop is what puts it
   before the FIRST run as well as every later one, and it therefore SUBSUMES the
   reset between consecutive tools: one barrier, stated once, does both jobs.
   **STEP 3'S OWN BY-PRODUCTS ARE THEREFORE NEVER PART OF ANY INVENTORY** — step 3
   runs the whole pinning suite in this same tree and leaves untracked and ignored
   test caches behind it (`__pycache__`, `.pytest_cache`), and the barrier removes
   them before the first regeneration, so no inventory sees them and no identifier
   is charged with them; without it the first full `--ignored` inventory would
   attribute all of them to whichever tool ran first and break the pair equality
   on artefacts no tool produced. A worktree-only restore is
   NOT enough, and the distinction is the whole attribution: `git checkout -- .`
   restores from the INDEX, so a regeneration tool that STAGES what it writes
   leaves that content in the index, where it survives into the NEXT identifier's
   delta and attributes one tool's artefact to another — precisely the mis-binding
   the pair equality exists to catch; and `-fdx` rather than `-fd` because an
   IGNORED file a tool writes is still a difference the next run can trip over.
   **THEN THE RUN, WHICH MUST SUCCEED**: every allowlisted invocation is REQUIRED
   TO EXIT ZERO, and its exit status is checked BEFORE any delta is read — a
   non-zero exit, or a timeout, is a CONFORMANCE FAILURE recorded against that
   identifier, and that identifier's delta is not recorded and forms no pairs.
   Without that check a generator that writes exactly its declared paths and then
   dies still satisfies the pair equality and is reported healthy.
   **THEN THE INVENTORY**: the paths
   THAT IDENTIFIER produced are **THE FULL WORKING-TREE DELTA AGAINST THE BASELINE
   COMMIT — TRACKED MODIFICATIONS AND DELETIONS, UNTRACKED FILES, AND IGNORED
   FILES ALIKE** — read in the same hermetic environment as **`git status
   --porcelain=v1 --untracked-files=all --ignored=matching`**, the path taken
   from EVERY status line, a RENAME counted as BOTH paths, and the call made
   IMMEDIATELY AFTER the run and BEFORE the next iteration's barrier.
   **`git diff --name-only` IS NOT THE INVENTORY**: it reports only changes to
   TRACKED content, so a generator that writes a NEW file — above all one the
   repository IGNORES, which NO DECLARATION MAY NAME (step 1) and which is
   therefore always an accidental output — produces an artefact the equality
   never sees, which is the undeclared output the check exists to catch. **AN
   IGNORED PATH A TOOL PRODUCES COUNTS AS PRODUCED** and fails the equality —
   always, a declared artefact being a tracked path — exactly as an undeclared
   tracked one does: being ignored by `git` says something about version control,
   nothing about whether the tool wrote it.
   The measured value is therefore a set of **`{(identifier, path)}`
   PAIRS**, and the test asserts THAT PAIR SET EQUALS that class's CAPTURED
   `# companion-artefact:` PAIR SET — path AND identifier, exactly as declared —
   **no more, no less**, in both directions and order-free.
   **THE IDENTIFIER IS PART OF THE EQUALITY BECAUSE THE DECLARATION BINDS IT**: a
   DECLARED pair whose identifier did NOT produce that path FAILS, even when some
   OTHER allowlisted tool did produce it, so an artefact bound to the WRONG
   recording tool is caught instead of being absorbed; and an UNDECLARED pair
   produced by ANY allowlisted tool FAILS for the same reason. **The union of the
   changed paths is retained only as a CONSEQUENCE of that pair equality, never
   as the check** — equal pair sets have equal path sets, and it was the
   path-set-only comparison that let a mis-bound identifier pass. **The inventory
   is INDEPENDENT OF THE DECLARATION here too**: an artefact that moves on this
   withdrawal but which no `# companion-artefact:` line names is regenerated
   anyway and appears in ITS OWN identifier's delta, so the omission BREAKS the
   equality instead of hiding inside it. Because the withdrawal is already IN the
   baseline, each delta contains **ONLY paths that identifier's regeneration
   changed**, and an allowlisted regeneration with nothing to do with this
   withdrawal writes nothing and so contributes no pair at all.
5. **RECORD THE RESULT.** Both equalities and the non-emptiness result are
   reported per class, and any failure NAMES THE CLASS AND THE STEP — a step-1
   refusal naming its refusal class and the offending declaration, a step-2a
   non-empty control inventory naming the NON-DETERMINISTIC identifier and the
   paths it rewrote on an unchanged tree, a step-4
   inequality naming the offending `(identifier, path)` pairs — so the red check
   says which enrolment failed and where rather than only that the conformance
   test failed.

**A PATH-SCOPED DIFF IS DELIBERATELY NOT USED, AND THE REASON IS THE FAILURE IT
WOULD HIDE.** Restricting the diff to the declared paths would make the equality
trivially satisfiable in one direction and would conceal exactly the failure most
worth catching — a regeneration that writes a path NOBODY DECLARED. The
whole-tree diff *against the baseline commit*, taken after EACH identifier's own
run, keeps that detection: an unexpected generated path appears in that
identifier's delta, the `(identifier, path)` pair it forms is absent from the
declared set, and the check fails. The baseline removes the false positive; the
whole-tree grain keeps the true one; the per-identifier grain is what makes the
pair, rather than the bare path, the thing compared.

**AND NEITHER MEASUREMENT IS DERIVED FROM THE DECLARATION IT IS COMPARED
AGAINST, WHICH IS WHAT MAKES THIS A COMPLETENESS CHECK.** An earlier formulation
narrowed step 3 to the captured node list, to stop the conformance module
discovering and invoking itself. That narrowing bought self-containment at the
price of the property the check exists for: a pinning assertion the declaration
OMITS would never be run, never fail and never enter **A**, so an incomplete
declaration would equal its own measurement and the "every assertion" guarantee
would be circular. Self-invocation is instead prevented by EXCLUDING THE MODULE
BY ITS OWN PATH — a constant in trusted test code, not a value read from the
declaration — which leaves the inventory COMPLETE. **The contamination the
narrowing also guarded against is answered by the BASELINE, not by the run:** the
pinning suite is green on the pre-withdrawal tree, because it is a required
check, and the baseline tree differs from that tree BY THE WITHDRAWAL AND NOTHING
ELSE, so every failure in **A** is attributable to the withdrawal — and a failure
that is not is a red suite on `main`, a finding in its own right that must not be
hidden by narrowing the run. The artefact half takes the same treatment for the
same reason: EVERY allowlisted regeneration runs, one at a time, so an artefact
that moves undeclared appears in ITS OWN identifier's delta and breaks the pair
equality rather than being passed over unregenerated.

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
ASKING IT TO: the allowlisted regenerations rewrite the artefacts and the FULL
WORKING-TREE DELTA against the baseline commit — `git status --porcelain=v1
--untracked-files=all --ignored=matching`, taken after each identifier's own run
— reports the paths AND the identifier that produced each of them, a NEW or
IGNORED file among them exactly as a tracked modification is.

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
- **"and nothing else" is measurable, not an assurance, AND IT BINDS AT TWO
  LEVELS**: (a) AT THE PATH LEVEL, the paths `git diff --name-only` reports for
  that pull request lie within the union of the envelope, the files holding the
  declared node ids and the declared artefact paths; and (b) AT THE ASSERTION
  LEVEL, within a declared assertion's OWN FILE nothing moves but the declared
  node ids' EXPECTATIONS — no other assertion, no fixture, no helper and no
  import changes. The path-level bound alone is not the bound: it is satisfied by
  a throw that rewrites an UNDECLARED assertion inside a DECLARED file. Both
  levels are verified by the throw pull request's reviewers reading the diff
  HUNK BY HUNK against the declaration, and a withdrawal that breaches either
  level is refused;
- **landability follows rather than being hoped for**: every assertion that
  would fail is one the pull request re-targets and every artefact that would
  move is one it regenerates, so the required `validate` check passes on the
  throw's own tree;
- **the restore is a FORWARD CHANGE produced by this same procedure — NEVER A
  REVERT**: one pull request carrying the same three kinds of change in the
  opposite direction and nothing else — the candidate mapping and its companion
  comment lines re-added BYTE-IDENTICAL to the pre-throw declaration, each
  declared assertion's expectation re-targeted BACK to the enrolled tree, and
  each declared artefact REGENERATED by its allowlisted tool in the restored
  tree, which APPENDS the restore movement to the golden digest's history (D-3)
  as the throw appended the throw's. The bound and the landability consequence
  are identical to the throw's. A `git revert` is refused as the restore: it
  would delete the throw's recorded movement instead of recording a restore.

**And the figures stay in view.** At today's head the companion for
`openxfactory-floor-regeneration` measures 29 assertions across five test files
plus the golden digest (§ 1's table; the RESULT of 2026-09-11T03:08Z), so the
throw carries a six-file companion beside the envelope edit. That is what N-4's
"one edit" hid. This packet does not shrink the act — it makes it declared,
bounded and reviewable instead of discovered at the moment the switch is thrown.

**D-2e — WHAT THIS PACKET FIXES, AND WHAT THE COMPANION CHANGE'S DESIGN OWNS.**
This packet fixes THE INVARIANTS of the conformance procedure, and only those:
capture before withdrawal; a committed hermetic baseline; a complete INDEPENDENT
inventory with the conformance module excluded BY PATH; per-identifier
attribution as (identifier, path) PAIRS over the FULL working-tree delta, ignored
and untracked paths included; allowlisted identifiers resolved ONLY in
trusted test code; artefact paths refused LEXICALLY and then CONTAINED; DECLARED
ARTEFACTS ARE TRACKED PATHS at the control baseline, an ignored or untracked path
never being declarable; index AND
worktree reset between tools; THE DETERMINISM AND IDEMPOTENCE OF EVERY
ALLOWLISTED RECORDING TOOL — A BYTE-IDENTICAL NO-OP, IGNORED AND UNTRACKED PATHS
INCLUDED, WITH INTERPRETER CACHES SUPPRESSED — PROVED BY A CONTROL RUN ON THE
COMMITTED PRE-WITHDRAWAL TREE WHOSE INVENTORIES MUST BE EMPTY — **AN INVARIANT, NOT A
MECHANIC**: what the control run must ESTABLISH is fixed here, while HOW it is
issued is the companion's to specify, and without it no post-withdrawal delta is
attributable to the withdrawal at all; NON-EMPTINESS; and the two equalities with
their failure classes. **THE EXACT COMMANDS, FLAGS AND HELPER LAYOUT ARE THE
codexFactory COMPANION CHANGE'S DESIGN TO SPECIFY AND ITS REVIEWERS TO JUDGE.** A
later mechanic that leaves every invariant above INTACT belongs THERE, not here:
this is a specification packet, and a procedure written to the byte into a spec
delta is a procedure that must be RE-RATIFIED to change a flag. The invariants
are stated at the grain at which a reviewer can tell whether the check still
measures what it claims to; below that grain the companion's own design and its
own reviewers hold the pen.

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

**Consequence, stated rather than discovered — TWO FORWARD MOVEMENTS, THROW AND
RESTORE, EACH RECORDED BY REGENERATION; NEVER A REVERT.** The throw pull request
carries a digest movement and a reasoned entry for it; the RESTORE is a FORWARD
change produced by the same procedure as the throw (D-2d, `tasks.md` § 3.6 and
§ 4.3), and because it REGENERATES the digest in the restored tree it APPENDS the
mirror movement. That is two entries in the digest's history for one observation,
and it is correct that it be so. **A `git revert` of the throw cannot deliver
this and is therefore refused as the restore:** reverting the patch REMOVES the
throw's appended entry rather than adding a second one, so the behaviour history
would end with no record that the switch was ever thrown — the opposite of the
ledger this observation exists to produce, and the reason the restore is defined
as a forward change rather than as an undo.

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
| the restore | (unstated) | a **FORWARD change by the throw's own procedure, never a revert** — the entry and its companion comment lines re-added byte-identical, the declared assertions re-targeted back, the declared artefacts regenerated, so the digest records the RESTORE movement beside the throw's (D-3) |
| the second observation | autonomous approval resumes | unchanged: autonomous approval resumes on the following real bot cycle |
| where it is recorded | — | openxFactory #745 and codexFactory #232, with box 3.6 ticked **on the parent's own packet**, never on this one |

**The remaining blocker is not removed by this packet.** A real bot cycle must
exist to observe, and none does today ("nothing owed" since 2026-09-10T17:22Z);
none can be manufactured, because the class pins `expected_author:
openxfactory[bot]`. Consequence (4) of the ruling states the conjunction
exactly: the observation resumes only after this successor lands **and** a real
bot cycle exists.

## 4. Open questions — declared, not answered

**REVISIONS AT FILING, so the record says what review moved and what it did
not.** Review rounds 7–9 changed the CONFORMANCE PROCEDURE (step 3 now measures
the whole pinning suite with the conformance module excluded by its own path, and
step 4 regenerates every allowlisted artefact, so a declaration that OMITS a
companion is DETECTED rather than equalling its own narrowed measurement) and the
DEFINITION OF THE RESTORE (a forward change produced by the throw's own
procedure, never a revert, so the golden digest records BOTH movements). They did
NOT change the mechanism this packet asks to ratify: the declared companion, the
in-envelope comment grammar, the allowlisted regeneration identifiers resolved
only in trusted test code, the committed post-withdrawal baseline and the
non-emptiness clause all stand as filed.

**ANSWERED AT FILING, AND THEREFORE NOT OPEN — the former Q-2, "does the
companion rule bind the OTHER enrolled class, and the next one?": YES — EVERY
ENROLLED CLASS; NOTHING IS GRANDFATHERED.** The requirement binds every enrolled
candidate class, so the realizing codexFactory companion change declares a
companion for EVERY class enrolled in `.github/merge-approval-envelope.yml` at
realization time — today TWO, `codexfactory-routine-code` and
`openxfactory-floor-regeneration` — each MEASURED BY THE SAME FIVE-STEP
PROCEDURE, in the order D-2b fixes and `tasks.md` § 3.2 carries (capture the
declarations, commit the withdrawal as the baseline, measure the assertions over
the whole pinning suite with the conformance module excluded by its own path —
a measured set that may not be empty — regenerate every allowlisted artefact and
diff against the baseline, record), and
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
