# Feature Specification: openDox, the document tool and self-maintenance (release 2)

**Feature Branch**: `038-opendox-document-tool-self-maintenance`
**Created**: 2026-10-05
Status: draft
**Clarifications**: round 1 is ANSWERED. Brett Heap took option (a) on all 25
questions, `R2Q1`–`R2Q25`, on 2026-10-05, by interactive multi-choice,
verbatim *"Accept all 25 recommended (Recommended)"* (`#656` `6003486656`). The
answers are encoded below and inline in
[`clarify-questions.md`](./clarify-questions.md). The same file defers 34
design-level questions to the plan, each with a proposed default. Brett Heap
ruled the plan at `6847e99e`, everything as recommended (`#656` `6013547504`);
its one ruling that moves this specification's text, I-2, is encoded below.
**Realizes**: RELEASE 2, "the document tool and self-maintenance", phases 4–5,
of the openxFactory OpenSpec change `add-neutral-product-standalone-operability`
(#1144, landed `94b6f7f1`). The phases follow that change's RULED release map
(`#656` `5799646419`, as corrected by `5800995035`). Phase 4 is Group 12, phase
5 is Groups 6, 14 and 15, and Group 11 (the guard) and box 9.5 (the pins) run
in every phase.
**Lane**: `openxfactory-4`
**Input**: the lane's brief of 2026-10-05, which asked for the
`/speckit.specify` step: a specification written faithfully from #1144 and
its four release-2 rulings, with every genuinely undecided point put as a
question. The questions are now answered. No code is written until the plan is
ruled.

**ONE OPENSPEC CHANGE, TWO SPECKIT FEATURES (R1Q21 (a)).** #1144 is one
OpenSpec change. The global protocol hands a change to a Speckit feature under
`specs/NNN-*` (lifecycle step 3), and openxFactory's constitution (Principle
II) lets a larger change decompose into one or more. R1Q21 (a) made release 2
its own Speckit feature, planned once release 1 lands. Brett Heap answered it
on `#656` comment `5850003126` (2026-09-26T21:23:03Z), verbatim *"go with
recommendations on all the open questions"*, and plan 034 records it at
`plan.md` § Structure Decision and `clarify-questions.md` § R1Q21. So #1144
hands off to two features:

- [`specs/034-opendox-standalone-operation/`](../034-opendox-standalone-operation/spec.md),
  release 1, phases 1–3;
- this feature, release 2, phases 4–5.

The change archives only on merged, green realization evidence for BOTH
releases (`5800995035`, answer 2). Landing either feature archives nothing and
promotes nothing on its own.

**AUTHORITY.** Brett Heap ratified #1144 on `#656`, comment `5815412869`
(2026-09-24T13:51:09Z), verbatim: *"ratify #1144, land the follow-ons, (a) on
C1–C5"*. That word authorized release 1's realization. The ratification record
names release 1 alone, and release 2's rulings stay SEQUENCED after it, not
deferred, reopened or weakened (#1144 `tasks.md` § "The release map";
`design.md` § D13). Brett Heap started release 2 on `#656`, comment
`6001702967`, verbatim *"Start release 2 (Recommended)"*, and answered its
clarify round on comment `6003486656`. This file specifies release 2 and
realizes none of it.

Release 2 carries four rulings, each exactly as #1144 encodes it:

- `5783934499` (2026-09-22T20:49:40Z), *"add a neutral publish step to the
  build arc"*: the neutral submission step, requirement 11. It is named
  "submission", not "publish", for the reasons in `design.md` § D9.
- `5784155201` (21:06:01Z), *"bundled postgres, local identity yes, merge yes,
  health in db"*: merge authority follows whoever governs the repository, under
  three guardrails (requirement 11), and health results live in the store
  (requirement 6 as amended). Its install half was release 1's phase 3.
- `5784247356` (21:12:34Z), *"1, add the fix loop to #1144"*: the fix loop and
  exceptions in git, requirements 14 and 15.
- `5784295745` (21:16:17Z), *"1, add the pack interface to #1144"*: the
  check-pack interface, requirement 16.

**THE RATIFIED PACKET IS THE AUTHORITY, NOT THIS FILE.** Every requirement
below realizes one of #1144's requirements 6, 11, 14, 15 and 16, or the guard
of requirement 1, and names it with its boxes. Where an answer reads #1144's
text, the reading is recorded here and cited to its answer. Where an answer
changes a falsifier or a task line of #1144, the change lands in #1144 as a
bookkeeping amendment, in plan 034's T007 form, under a Rule 6 window (FR-025).
No answer changes a requirement's text or a scenario: R2Q19 and R2Q20, the two
that asked whether to, were answered "keep as ratified". The questions are
named `R2Q<n>`, because a bare `Q<n>` names one of #1144's own rulings
(RULING Q1, RULING Q2, Q-R4, DIRECTION Q5) and `R1Q<n>` names plan 034's.

**Why the feature lives in openxFactory.** The governing change lives here, as
it did for plan 034. openDox-spec cannot govern this work yet: requirement 8's
interim arrangement still applies, because openDox-spec has promoted none of
the 71 requirements the carve assigned it (#1144 Group 8, outside both
releases). The IMPLEMENTATION lands by each repository's own pull request:

- openDox-code, the bulk: Groups 6, 12, 14 and 15;
- openXdox-code, where 12.5 proves the governed flow unchanged, and whose pin
  on openDox advances (9.5);
- the openDox root, for its `code` pin (9.5), its README, and release 2's
  `dox-v1.y` bundle cut (R2Q22 (a));
- the openXdox root, for its `code` pin (9.5);
- openxFactory, for its two pin pairs (9.5) and any host wiring within 11.1's
  declared surfaces;
- openDox-spec, already the arc's sixth repository (batch G at 9.5,
  `tasks.md:1594-1595`), for release 2's three schemas (R2Q22 (a)).

## Clarifications

### Session 2026-10-05

Round 1 was raised from this feature's reading of #1144's 37 release-2 boxes
and its four rulings, and from three read-only inventories by lane
openXfactory-3 (R2-INV-12, and R2-INV-HEALTH parts A and B; #656 `6001723339`).
Every tree was measured on 2026-10-05 at `main`: openDox-code `a9ac96f9`,
openXdox-code `56e1c238`, the openDox root `d77f8cbf` and openxFactory
`0f2a87f6`. Lane openXfactory-3 checked the questions twice before Brett saw
them. Brett Heap answered all 25 by interactive multi-choice, verbatim *"Accept
all 25 recommended (Recommended)"* (`#656` `6003486656`). Every question took
option (a).

- Q: R2Q1. What does the release map's "one interface for both" bind? → A: One user-facing interface. The `submit` and `land` verbs and routes, and the Health view's land action, are the same in every mode. Behind them, `SubmissionPort`, `LandingPort` and `PullRequestPort` stay split as 12.1 and 12.6a require. `submit`'s port comes by injection, and the governance query binds only the lander. The map's phrase is recorded as a non-normative reading.
- Q: R2Q2. Does `pull_request_factory`'s unset default stay `GhPullRequests`? → A: Yes. The new `submission_factory`/`_submission_port` pair defaults to `LocalGitSubmissions`, and `pull_request_factory`/`_pull_request_port` keep `GhPullRequests`, serving `gate open-pr` unchanged. 12.4's repoint sentences (`tasks.md:2513-2519`; `design.md:476-478`, `:1059-1061`) are read as the withdrawn draft's residue, and a bookkeeping note says so. Brett accepts that, with R2Q3 (a), ruling `5783934499`'s third bullet ("contributed by the governed host") and 12.5's "With the host's implementation registered" go unrealized in release 2.
- Q: R2Q3. Does any governed host carry `submit`, `land` or `health` in release 2? → A: No. Both hosts' trees, help goldens and governed flows are unchanged, and F12.2 proves the host-side behaviour against a registered test host.
- Q: R2Q4. What is the governed host's "instrument", and what does routing a landing to it do? → A: The instrument is the host's contributed `SubmissionPort`, declared in its host profile. Under `governed`, no lander is bound. `land`, and the fix loop's land action, submit through that port and report where the work went. The merge stays the governance's act.
- Q: R2Q5. What may a standalone install submit and land? → A: Any local branch except the default branch, including branches made with git and the fix loop's `health-fix-*` drafts. A live session whose branch is landed ends by the existing merge observation. A standalone session opener and Save are a follow-on outside release 2.
- Q: R2Q6. Where does a standalone `land` merge, and how does a landed default branch reach a remote? → A: The lander makes the `--no-ff` merge commit in a landing worktree of its own. Where the served checkout holds the default branch and is clean, it fast-forwards that checkout with `git merge --ff-only <commit>`. Feature 007 gains four named exceptions, by this word: the guard's argument check (`tests/test_session_git.py:523` still refusing `("merge", "other-branch")`, `:563-564`'s pin moving); `session_git.py:93`'s stated rule; SC-002's `HEAD` clause; and SC-002's working-tree clause. `land` pushes nothing. It first checks, with `ls-remote`, that the local default branch contains the remote's tip. A landed default branch leaves the served checkout only by the user's own `git push`, which reaches a plain repository's remote directly, or a project repository from which `project push` carries it on.
- Q: R2Q7. Which branch is "the default branch", and how does a standalone owner's first declaration reach it? → A: `main`, openDox's existing session base. A repository with no `main` is `unknown` and refused naming it. With no declaration, `land` refuses, naming the exact file and content, which the owner commits with git. The openDox root's README documents it.
- Q: R2Q8. Where does 12.5 run, and who repairs the governed suites' reds? → A: F12.1 runs composed, as F5.2 does under R1Q23 (a), until the `doc_health` direction arc's realization lands, by a bookkeeping line. Phase 4 owns a repair slice for the 174 composed reds, editing none of the 16 suites, by four means: a host-registering conftest outside them; the harness copy fixed and the schema placed where they read it; allow-list entries for pure respellings; and each singleton traced. R1Q6 (d)'s "arc DECIDED first" still stands.
- Q: R2Q9. Approve the falsifier amendments that release 1's rules force? → A: All seven are approved, as ONE bookkeeping batch in T007 form, under a Rule 6 window, landing before phase 4's first checkpoint. The seven are:
  - F6.1 builds an entry point first, and its stale "Today" text is struck;
  - F14.1 and F15.1 first start the document server, as F13.1 does;
  - F15.1 asserts its sandbox precondition;
  - the forking pack's child carries its own pack id;
  - the corpus export cannot be steered by `export-subst` or `export-ignore`;
  - the escaping pack's restore attempt is a write;
  - `submit`, `land` and `health` take `--local`.
- Q: R2Q10. What is a finding's `id`? → A: A stable, pack-qualified key, derived by the engine from the pack id, family, document path and a family-supplied locator. It survives a reset, is unique, and maps to a valid ref name. `health list --json` also carries `kind`. F14.1 and F15.1 select planted findings by their fixture document.
- Q: R2Q11. What is a document's "location" for `stage-location-mismatch`, and which way does the repair go? → A: A top-level directory named by one of the six role keys or their declared words. A document outside such a directory is never flagged. The `auto-fix` edits the `stage:` header and never moves the file.
- Q: R2Q12. How does the baseline work in a disposable store? → A: The baseline is the previous default-tip run, held in the store. Each run sorts its findings into three classes: new, arrived with a pack upgrade (D12), and persistent. Disappearance is measured only between default-tip runs. A citation is a landing of the fix loop's draft, or a commit with a `Finding:` trailer, and an uncited disappearance is re-raised once as `human-only`. A reset forgets the baseline, and Brett takes the reading that this narrows "recomputable from git" for pending disappearances.
- Q: R2Q13. Does the health table join RULING Q1's closed list? → A: Yes, DOMAIN. It joins `identity.TABLES`, and the closure test reads `0001` with `0003_`, both in the same change.
- Q: R2Q14. How does 6.1a's "relocate the generic part" square with 11.1's guard and the unruled direction arc? → A: 6.1a is satisfied vacuously in release 2. No family moves, and no shared module is created. Any relocation inside `doc_health` belongs to the direction arc's Q4.
- Q: R2Q15. What does a HOSTED install do with the health engine and with packs? → A: Health runs on the local plane and from the CLI only. On the hosted plane, the view, its routes and the `health` verbs refuse by name, as `submit` does, and record nothing. The schema still migrates.
- Q: R2Q16. What runs in the sandbox, and does macOS get packs? → A: Trusted installed code runs in process on every platform: the product's own checks, and a host's check registered through `register_health_check`, at the scoped seam only and never stored. Only manifest-listed packs are sandboxed. Where there is no sandbox, packs do not run, and one finding against the install says why. Release 2 has no Seatbelt realization.
- Q: R2Q17. Does openDox-code's required check run the sandbox suite? → A: Yes. The required `validate` job pins `ubuntu-24.04`, installs bubblewrap, sets `kernel.apparmor_restrict_unprivileged_userns=0`, and proves the sandbox live before the suite. Under `CI`, the sandbox tests fail rather than skip, so `EXPECT_SKIPPED` stays 11. Moving to 26.04 waits for a measurement on a runner, and there is no macOS job. This required-check change is made by this word.
- Q: R2Q18. What may a pack depend on? → A: The standard library and the engine runner's neutral contract module, nothing else. The pack's digest plus the install's version pin everything that runs.
- Q: R2Q19. Amend requirement 16 and 15.1b so that a pack may see git history? → A: No, keep as ratified: a pack sees only the exported tree.
- Q: R2Q20. Amend requirement 16 and 15.1b so that a pack's check may be model-assisted? → A: No, keep as ratified: pack checks are model-free.
- Q: R2Q21. Is a domain's pack pinned in its `stack.yaml` or in the corpus's `health/packs.yaml`? → A: `health/packs.yaml` is authoritative for what the engine runs. A lockstep check against a domain's `stack.yaml` is owed by F2, not release 2.
- Q: R2Q22. Does openDox-spec own the health contract's schemas, with a bundle cut? → A: Yes. openDox-spec owns three schemas: the exceptions file, `health/packs.yaml` and the finding's neutral shape. The code leg carries digest-checked copies, and the openDox root cuts one more `dox-v1.y` minor under a batch-G style addendum at 9.5. No repository joins.
- Q: R2Q23. Is release 2 published to PyPI? → A: Yes. `opendox` 0.2.0 is published at release 2's cut, tagged `v0.2.0`, through the existing trusted-publishing workflow, under a batch-O style addendum. It is published on Brett's publish word after acceptance passes.
- Q: R2Q24. Does release 2 carry an end-to-end acceptance, AT-R2? → A: Yes, in AT-R1's form, with an HTTP half in CI and a browser half on the host.
- Q: R2Q25. May a finding's `evidence` hold document excerpts? → A: No. It holds locators only, and the view reads the passage from git when it renders.

### Session 2026-10-06 (the plan ruling)

Brett Heap ruled plan 038 at `6847e99e` by interactive multi-choice, every
item as recommended (`#656` `6013547504`). One ruling moves this
specification's text:

- Q: I-2. In a repository with no `main`, which branch's tip holds the health baseline? → A: *"main, else HEAD's branch (Recommended)"*. The baseline branch is `main`, else the branch HEAD names; R2Q7 (a)'s `main` still governs landing alone. User Stories 4 and 5, the edge cases, FR-010, Key Entities and Risks now say "the baseline branch's tip".

## User Scenarios & Testing *(mandatory)*

The falsifiers are #1144's own, cited by the label plan 034 defines:
`F<group>.<n>` is the n-th FALSIFIED BY box of that group in document order.
In Group 12, F12.1 is 12.5's governed-flow proof and F12.2 is the submission and
landing acceptance. A falsifier "as amended" is the one R2Q9 (a)'s bookkeeping
batch, or another answer's bookkeeping line, leaves in #1144 (FR-025).

### User Story 1 — Submit work from a plain repository (Priority: P1) · phase 4

A student works in openDox on a plain local git repository, the install RULING
C3 describes, on a machine with no `gh`. They submit a branch through openDox's
OWN `submit` verb, or its own route. Where a remote is attached, the branch is
pushed there, and openDox reports where the work went, with any credential in
the remote's URL redacted. Where none is attached, openDox says plainly that
there is nowhere to submit. A governed host that needs its own platform flow can
contribute its implementation through the same binding, though no host does in
release 2 (R2Q3 (a)).

**Why this priority**: it is requirement 11's first gap. Today the only
implementation is `GhPullRequests`, which shells out to `gh` against
`github.com`, and the only act that submits is openXdox's `gate open-pr`. So a
standalone openDox cannot submit at all, `gh` or no `gh` (#1144 12.4a).

**Independent Test**: F12.2's submission half exits 0 in an openDox-code
checkout alone, with `gh` absent. That is the `submit` verb, the CLI binding
asserted neutral, the two `tests/test_submission_default.py` nodes, the five
`tests/test_submit_route.py` nodes and the no-remote refusal.

**Acceptance Scenarios**:

1. **Given** a plain git repository with a remote attached, and a local branch
   that is not the default branch, and no `gh`, **When** `opendox submit
   --repo-root <repo> --branch <branch>` runs, **Then** the branch arrives at the
   remote, and the verb reports the remote, the ref and the URL (requirement 11,
   third scenario; 12.1a, 12.2, 12.4a; R2Q5 (a)).
2. **Given** the same repository with no remote, **When** the same verb runs,
   **Then** it exits non-zero with `NoSubmissionTarget`, names what is missing,
   and prints no traceback (requirement 11, fourth scenario; 12.3).
3. **Given** nothing injected, **When** the CLI or the server builds its
   submission binding, **Then** it is `LocalGitSubmissions`, a `SubmissionPort`,
   and not a `PullRequestPort` (requirement 11, first scenario; 12.1, 12.4).
4. **Given** a remote whose URL carries a userinfo credential and a query-string
   token, **When** a submission succeeds, is refused or fails, **Then** neither
   secret appears in the report, the printed output or a refusal, and the report
   still names the remote's host and path (12.1a).
5. **Given** the route `POST /actions/session/submit`, **When** a request comes
   off loopback, without a resolved actor, without the console token, or from a
   foreign origin, **Then** it is refused in that order, before any body byte is
   read, and the remote is unchanged. The route takes no repository from the
   request (12.4a). On a standalone plane, the token reaches the page only
   through the URL it is opened with (12.4a as T007 batch N records
   `5963851934`).
6. **Given** the default branch, **When** `submit` is asked to submit it,
   **Then** it refuses, naming the rule (R2Q5 (a)).

---

### User Story 2 — Land one's own work, by an explicit human act (Priority: P1) · phase 4

A standalone owner lands a branch into their own default branch, `main`. Their
install is the explicit local one, and `main` carries the committed standalone
declaration. They confirm the landing by typing the branch's name at the
controlling terminal, or through the view's confirm control. openDox makes a
`--no-ff` merge commit in a landing worktree of its own, which `git revert -m 1`
undoes. Where their served checkout holds `main` and is clean, it fast-forwards
that checkout to the merge commit. A conflict is shown with its paths, and the
default branch does not move. `land` pushes nothing. In a governed repository,
or where governance cannot be established, no lander is bound at all.

**Why this priority**: *"merge yes"* (`5784155201`). Forbidding a standalone
owner to merge their own repository protects nobody from anybody. The three
guardrails carry the purpose the old absence served: no tool merging behind its
governance's back (`design.md` § D9).

**Independent Test**: F12.2's thirteen named
`tests/test_landing_guardrails.py` nodes exit 0 in an openDox-code checkout
alone. Feature 007's tests pass with their four named exceptions (R2Q6 (a)).

**Acceptance Scenarios**:

1. **Given** a standalone repository and a local install, **When** `land` runs
   with a confirmation minted at the controlling terminal for that branch and
   its head, **Then** `main` gains a merge commit, `Landed` returns its sha, and
   `git revert -m 1 <sha>` restores the tree (requirement 11, sixth and ninth
   scenarios; 12.6a).
2. **Given** a served checkout that holds `main` and is clean, **When** a
   landing succeeds, **Then** the served checkout is fast-forwarded to the merge
   commit by `git merge --ff-only`. It is never switched, reset or stashed. A
   fast-forward that no longer applies refuses, and the default branch is where
   it was (R2Q6 (a)).
3. **Given** a remote attached whose default-branch tip the local `main` does
   not contain, **When** `land` runs, **Then** it refuses, naming the remedy
   (R2Q6 (a)).
4. **Given** a confirmation made any way that is not a human act — a flag, a
   configuration key, a stdin that is not a terminal, a token built directly,
   one minted for another branch or head, or one presented twice — **When**
   `land` runs, **Then** it refuses (requirement 11, seventh scenario; 12.6a).
5. **Given** a branch that conflicts with the default branch, **When** `land`
   runs, **Then** it raises `MergeConflict` naming the conflicting paths, and the
   default branch is where it was (requirement 11, eighth scenario).
6. **Given** a registered host whose profile declares an instrument, **When** a
   landing is requested, **Then** no lander is bound, and the landing is
   submitted through the host's contributed `SubmissionPort`, which reports
   where the work went. The merge stays the governance's act (requirement 11,
   fifth scenario; 12.6a; R2Q4 (a)). In release 2 the host is F12.2's registered
   test host (R2Q3 (a)). Given instead a committed declaration that says
   `governed` and no host, no lander is bound and `land` refuses, naming what
   is missing (12.6a).
7. **Given** no declaration on `main`, no `main` at all, a host profile that
   fails to load, a declaration that disagrees with the install mode, or a
   branch that ADDS a standalone declaration, **When** a landing is requested,
   **Then** governance is `unknown`, no lander is bound, and `land` refuses,
   naming what is missing. Where the declaration is missing, it names the exact
   file and content to commit (12.6a; R2Q7 (a)).
8. **Given** any configuration key at all, **When** the configuration surface is
   walked, **Then** none switches a guardrail off (requirement 11, seventh
   scenario: *"a guardrail and not a setting"*; 12.6).

---

### User Story 3 — The governed host is unchanged (Priority: P1) · every phase

openxFactory's GitHub pull-request flow, through openXdox's `gate open-pr`,
behaves exactly as it does today, on `pull_request_factory`'s unset default,
`GhPullRequests` (R2Q2 (a)). openxFactory keeps its corpus, its 23 check
families, its adapter column, its intent-plane schemas, its integration tests,
its command tree and its help goldens (R2Q3 (a)). Every realization landing of
release 2 carries the arc's trailer, and openxFactory's arc edits stay on the
guard's declared surfaces.

**Why this priority**: requirement 1 is the invariant every other requirement
is judged against, and 12.5 is the box that proves submission is a
generalization rather than a replacement. A release that breaks its governed
host is a regression, not a release.

**Independent Test**:
- F12.1, run composed, as F5.2 runs under R1Q23 (a), PERMANENTLY: ARC-Q2 (a)
  and the plan ruling's CF-5 (`6013547504`) supersede R2Q8 (a)'s "until the
  `doc_health` direction arc's realization lands" (FR-005).
- An interim F11.1 run after each phase's openxFactory landings.
- openxFactory's required checks, green at every pin advance.

**Acceptance Scenarios**:

1. **Given** openXdox-code with the realized openDox installed,
   `FakePullRequests` injected, and openxFactory's `scripts/` composed, **When**
   every openXdox-code suite that drives `open-pr` or injects `FakePullRequests`
   runs (the set is computed, not typed: 16 at `ab04453d`, and 16 again at
   `56e1c238`), **Then** each passes. No arc landing edited one except through
   the reviewed allow-list (requirement 11, tenth scenario; 12.5; F12.1 as T007
   batches C and I amend it and as R2Q8 (a) amends it; R1Q7 (a), R1Q26 (a)).
2. **Given** every arc landing on openxFactory `main` since `94b6f7f1`, **When**
   F11.1 runs, **Then** every path touched is one of its declared surfaces, or a
   change to the carve manifest's `edits[].note` values alone, and nothing is
   deleted (requirement 1; 11.0, 11.1; R1Q2 (a), R1Q20 (a), R1Q22 (a); the
   `ADMITTED_ARC_EDITS` list RULED in `5890601202`, which a later phase extends
   only by a further ruling).
3. **Given** openxFactory's check families, **When** release 2 lands, **Then**
   each is where it was. No family moves into openDox, and the openXdox
   governance pack is follow-on F1 (requirement 1, first scenario; 6.2;
   `design.md` § D12). openxFactory's scoped check keeps running in process at
   the scoped seam, and its results are never stored (R2Q16 (a)).
4. **Given** the governed hosts' command trees and help goldens, **When**
   release 2 lands, **Then** they are unchanged. No host contributes `submit`,
   `land` or `health` in release 2 (R2Q3 (a)).

---

### User Story 4 — See the health of one's own documents (Priority: P2) · phase 5

A user runs openDox's health check over their own documents, from the Health
view or from the command line, on a local install. It reads documents AS
documents: broken internal links, documents nothing links to, near-duplicates,
missing neutral front matter, a declared stage that disagrees with the
top-level stage directory the document sits in, and stale or empty stubs. Its
results live in the product's disposable store, as a domain table. Against the
previous run at the baseline branch's tip (`main`, else the branch HEAD names;
I-2 (a)):
- new findings come first;
- findings that arrived with a pack upgrade are shown apart from them;
- persistent ones stay quiet;
- an uncited disappearance between two runs at the baseline branch's tip is
  re-raised.

**Why this priority**: *"a document product that cannot report on its own
documents has not shipped the thing it is named for"* (requirement 6, second
scenario). Today the scoped action answers `not-available` in every
openDox-only process (measured under Assumptions).

**Independent Test**: F6.1 as amended, and F14.1's `health run` and `health
list` lines as amended (R2Q9 (a), items 1 and 2).

**Acceptance Scenarios**:

1. **Given** an openDox-code checkout alone, and an entry point that registers
   openDox's own check, **When** the scoped health action runs over
   `README.md`, **Then** it returns `completed`, with a findings list and a
   reference (requirement 6, second scenario; 6.2; F6.1 as amended by R2Q9 (a),
   item 1).
2. **Given** a store, **When** results are computed, **Then** they live in the
   store, in a table that an ADDITIVE `0003_` migration brought and that joins
   RULING Q1's closed list. `identity.TABLES` and the closure test move in the
   same change (requirement 6, fourth and fifth scenarios; 14.1, 14.2; R2Q13
   (a)).
3. **Given** results, **When** anything would commit them into the corpus they
   describe, **Then** the write is refused (requirement 6, third scenario;
   14.3).
4. **Given** the store dropped and rebuilt, **When** the check runs again,
   **Then** the results are recomputed and no document is lost. With no
   baseline, the first run sees every finding once as new, and a pending
   uncited disappearance is forgotten (requirement 6, fourth scenario; 14.3;
   R2Q12 (a)).
5. **Given** no model configured, **When** the check runs, **Then** no
   model-assisted check runs, and every other check does (requirement 6; 14.4).
6. **Given** a family that reads the publisher's `Status:` taxonomy or its
   change/spec/delta nouns, **When** release 2 lands, **Then** that family stays
   with its corpus, and openDox's check reads its own declaration (requirement 6,
   sixth scenario).
7. **Given** a hosted install, **When** the Health view, a health route or a
   `health` verb is used, **Then** it refuses by name, saying that the health
   engine and its packs run only on a local install, and records nothing
   (R2Q15 (a)).
8. **Given** any finding, **When** its `evidence` is read, **Then** it holds
   locators only (a path, a line, a link-target string or a family-defined key)
   and no text of a document (R2Q25 (a)).

---

### User Story 5 — Repair findings through the fix loop, and keep exceptions in git (Priority: P2) · phase 5

Every finding has a resolution path, in the Health view and on the command line
with the same actions. An `auto-fix` finding is repaired by openDox itself, as a
draft on a branch. An `assisted` finding gets a proposed repair that the human
edits. A `human-only` finding shows its evidence, and the human repairs the
document, removes it, or records an exception. Every repair reaches the default
branch only through User Story 2's landing rule. Nothing lands automatically,
not even a one-line repair, and several repairs may be batched into one draft.
An exception is committed to the corpus. It survives a store reset, and
removing it re-opens its finding.

**Why this priority**: *"Detection without resolution is a list that grows"*
(requirement 14).

**Independent Test**: F14.1 as amended, over 14.9's `health-corpus` fixture
(R2Q9 (a), item 2; R2Q10 (a)).

**Acceptance Scenarios**:

1. **Given** the fixture in a fresh repository, **When** `health list --json`
   runs, **Then** each planted finding, selected by its fixture document,
   carries its class and its `kind`:
   - `broken-link`, `derivable-front-matter` and `stage-location-mismatch` are
     `auto-fix`;
   - `near-duplicate` is `assisted`;
   - the human-only finding is `human-only`.

   (Requirement 14, second to fourth scenarios; 14.6, 14.9; R2Q10 (a).)
2. **Given** each `auto-fix` finding and the `assisted` one, **When** `health fix`
   runs on it, **Then** a branch `health-fix-<finding>` carries a change to that
   finding's own document, and the default branch does not move. The
   stage-location repair edits the `stage:` header and never moves the file
   (requirement 14, second, third and fifth scenarios; 14.6, 14.7; R2Q11 (a)).
3. **Given** the `human-only` finding, **When** `health fix` runs on it, **Then**
   it is refused and no branch is made: the product proposes nothing it cannot
   justify (requirement 14, fourth scenario).
4. **Given** many findings repaired in one sitting, **When** they are batched,
   **Then** they form one draft for one review, which lands under the same rule
   a single repair would (requirement 14, sixth scenario; 14.7).
5. **Given** a finding, **When** `health accept --finding <id> --reason <text>`
   runs, **Then** `health/dispositions.yaml` changes in the corpus's working
   tree, and once that change is committed the finding is suppressed on the next
   run. After `runtime reset` and `runtime migrate`, the finding is still
   suppressed while the other findings return (requirement 15, first and second
   scenarios; 14.8).
6. **Given** a committed exception, **When** it is removed, **Then** its finding
   is raised again on the next run (requirement 15, third scenario).
7. **Given** the Health view and the CLI, **When** their actions are compared,
   **Then** every view action has a CLI verb and every CLI verb is offered by the
   view (requirement 14, seventh scenario; 14.5; the three
   `tests/test_health_parity.py` nodes).
8. **Given** a fix-loop draft on its branch, **When** a run on that branch no
   longer finds the repaired finding, **Then** no disappearance is raised.
   Disappearance is measured only between two runs at the baseline branch's
   tip, and the draft's landing cites it (R2Q12 (a); I-2 (a)).

---

### User Story 6 — Extend the health check through pinned, sandboxed packs (Priority: P3) · phase 5

A domain adds its own checks without forking openDox. A pack is listed in the
corpus's committed `health/packs.yaml` and pinned by digest, and also by commit
when it is sourced from outside the corpus. It uses only the standard library
and the engine's contract module. It runs in an operating-system-enforced
sandbox, which shows it only a read-only, isolated copy of the corpus's tree,
with no history, no network, no model, no inherited environment and no
inherited descriptors. It returns findings in the neutral shape, and optionally
patches. The engine stamps each finding with the pack's id and version. It
validates every patch before any branch exists. A pack that crashes, hangs,
writes, returns garbage, declares no version or tries to escape is reported as a
finding against that pack, and the other packs still run. No pack can redefine
the resolution classes, the baseline or who may land work. Where no sandbox
exists, packs do not run and the install says why, while the product's own
checks still run in process.

**Why this priority**: the layering depends on it. openXdox's governance pack
(F1) and each DomainxFactory's own pack (F2) need the interface. A standalone
user's own documents do not, which is why it comes after User Stories 4 and 5.

**Independent Test**: F15.1 as amended, over 15.6a's `pack-corpus`. It uses
14.5's verbs, so it closes after them. It asserts its own sandbox precondition,
and runs in openDox-code's required `validate` job on `ubuntu-24.04` with
bubblewrap and the AppArmor sysctl (R2Q9 (a), items 2–6; R2Q17 (a)).

**Acceptance Scenarios**:

1. **Given** the eight fixture packs registered, **When** `health run --timeout
   5` runs under an outer `timeout 120`, **Then** the user's checkout is clean
   and at the fixture's commit, and no descendant of the forking pack outlives
   its budget. The neutral checks still produce `broken-link`. The crashing,
   slow, writing, garbage-emitting and unversioned packs each appear as a finding
   attributed to that pack (requirement 16, first and fifth scenarios; 15.1b,
   15.6, 15.6a).
2. **Given** the escaping pack, **When** it tries each escape, **Then** none
   succeeds. Each attempt fails at the operating system's boundary, and one the
   pack swallows is still contained (requirement 16, third scenario; 15.1b).
3. **Given** any finding in the store, **When** it is listed, **Then** it carries
   a pack id and a pack version, and a built-in `broken-link` is attributed to
   `opendox` itself (requirement 16, seventh scenario; 15.7).
4. **Given** the patching pack's five out-of-bounds patches, **When** `health fix`
   runs on each, **Then** each is refused before any branch exists, as a finding
   against that pack naming the refused finding and the check it failed, and
   `patch-ok` becomes a draft on a branch while the default branch stays put
   (requirement 16, fourth scenario; 15.2a).
5. **Given** a pinned pack edited after pinning, **When** the next run starts,
   **Then** the pack is refused as a finding carrying the expected and the actual
   digest, and it is never skipped silently (requirement 16, second scenario;
   15.1a).
6. **Given** a pack that returns a class the engine does not declare, or declares
   its own baseline or landing rule, **When** it runs, **Then** it is refused
   (requirement 16, sixth scenario; 15.5).
7. **Given** a pack's finding titles and family names, **When** they are shown,
   **Then** they resolve through the display facet, never as the pack spells
   them in the neutral surface (requirement 16, eighth scenario; 15.3).
8. **Given** F15.1's twenty-four named refusal tests, **When** they run, **Then**
   each passes, and a missing node fails the command (15.5).
9. **Given** a platform with no kernel-enforced sandbox, **When** `health run`
   runs, **Then** no pack runs, one finding against the install says why, and
   the product's own checks still run in process (15.1b; R2Q16 (a)).

---

### Edge Cases

- A branch adds `.opendox/governance.yaml` with `governance: standalone` to a
  repository whose `main` has none. Governance is `unknown` and the landing is
  refused. A branch never decides its own landing (12.6a).
- A registered governing host and a committed standalone declaration are both
  present. The host wins (12.6a).
- A standalone owner's first landing, before any declaration exists. It is
  refused as `unknown`, naming the exact file and content to commit to `main`
  with git (R2Q7 (a)).
- A repository with no `main` (one the product created on another branch, or
  one served on `master`). Governance is `unknown`, and `land` refuses, naming
  the missing branch, until the owner creates or renames `main` (R2Q7 (a)). Its
  health baseline is the branch HEAD names (I-2 (a)); with a detached HEAD there
  is no baseline branch, so every finding reads as new.
- A remote URL carries a credential. The remote is PUSHED, and the credential
  is redacted from `Submission.url`, from the printed report and from every
  message, a refusal's included (12.1a; the plan's OQ-12-11, ruled
  `6013547504`). The first plan's refusal, as `attach_remote` refuses one,
  narrowed 12.1a and was withdrawn (ADV-09).
- A submit request reaches the hosted multi-user plane. It is refused before
  anything else, because that plane carries no `session` capability, and a push
  spends a personal git credential a hosted plane must never hold (12.4a). The
  `health` surfaces refuse there by name too (R2Q15 (a)).
- A browser tab kept an earlier serve's console token. The next serve refuses
  it until the page is opened again through the new private copy, an accepted
  limit (12.4a, T007 batch N). A persistent browser history can keep the
  fragment, also accepted (batch P, B7).
- A `--local` flag disagrees with the install-mode setting. The verb refuses,
  naming both (R2Q9 (a), item 7).
- A finding names no document. It carries no patch (requirement 16; 15.2a).
- A corpus-relative pack entry carries a `commit`, or an entry claims the id
  `opendox`. Each is refused (15.1a, 15.7).
- The platform offers no kernel-enforced sandbox (today: this lane's container,
  a default `ubuntu-24.04`, a hosted pod, and macOS). Packs do not run, `health
  run` reports that as a finding against the install, and the product's own
  checks still run in process (15.1b; R2Q16 (a)).
- A pack upgrade brings a finding that was absent from the baseline. It is
  reported as "arrived with a pack upgrade", apart from new. A finding whose id
  persists across the upgrade stays persistent (D12; R2Q12 (a)).
- The store is reset between an exception's commit and the next run. The
  exception still holds, because it was never in the store (requirement 15,
  first scenario).
- The store is reset while an uncited disappearance is pending. The re-raise is
  forgotten, as Brett ruled (R2Q12 (a)).
- `health accept` has written an exception that is not yet committed. F14.1
  commits it before the next run. An uncommitted entry suppresses only in a
  working-state run; a run over a commit reads the committed file (the plan's
  N-14, ruled `6013547504`).
- A file already sits at `health/dispositions.yaml` or `health/packs.yaml` but
  is not of the product's own kind. The aggregation repository of this estate,
  for example, keeps its governance dispositions under that name. The plan's
  ruled default is fail-closed (OQ-H-13; `6013547504`): the file is refused by
  name and never read as exceptions or packs.
- A run meets a pack whose output cannot be parsed as the neutral shape. None of
  that output is stored, and the finding says why (15.6).
- Landing meets a conflict. The paths are shown, and the default branch does not
  move. The plan's ruled default names the remedy in the refusal and adds no
  conflict verb (OQ-038-1).
- A corpus repository that openDox's runtime created is BARE (Q-R1), so there is
  no working tree for `accept` to write into. The plan's ruled default writes a
  draft on a branch there (OQ-H-14).

## Requirements *(mandatory)*

### Functional Requirements

Each FR realizes the named #1144 requirement through the named boxes, as round
1's answers settle it. Its falsifier is #1144's own, as amended where FR-025's
bookkeeping records an answer.

**Phase 4 — the neutral submission step, and landing (Group 12; requirement 11).**

- **FR-001** (requirement 11; 12.1, 12.1a): openDox SHALL declare
  `session_pr.SubmissionPort`, a `@runtime_checkable` protocol with ONE
  operation, `submit(branch) -> Submission`. `PullRequestPort` SHALL stay
  unchanged: its three operations, the absence of every other one, and its role
  as the governed host's platform protocol. `Submission` SHALL name the
  destination the work reached — `remote`, `ref`, and the remote's `url` as git
  resolves it — with any credential that URL carries redacted, and a refused or
  failed push's message SHALL be redacted the same way.
- **FR-002** (requirement 11; 12.2, 12.3): openDox SHALL ship
  `session_pr.LocalGitSubmissions`, implementing `SubmissionPort` and
  constructed as `GhPullRequests` is, with one positional checkout root. With a
  remote attached it SHALL push the branch there and return the `Submission`.
  With none it SHALL raise `session_pr.NoSubmissionTarget`, whose message names
  what is missing: never an opaque failure, and never a reported success.
- **FR-003** (requirement 11; 12.4; R2Q2 (a)): the product's own submission
  binding SHALL name no platform.
  - It SHALL be a NEW pair: `submission_factory`, beside `pull_request_factory`
    in `serve.py`, and `_submission_port`, beside `_pull_request_port` in
    `cli.py`. Each SHALL default to `LocalGitSubmissions` when nothing is
    injected. A governed host MAY contribute its own `SubmissionPort` through
    them.
  - `pull_request_factory` and `_pull_request_port` SHALL keep `GhPullRequests`
    as their unset default, serving `gate open-pr` unchanged. openXdox-code's
    protected `tests/test_session_snapshot.py:893-916` therefore stands.
  - 12.4's "repoints its UNSET DEFAULT" sentences (`tasks.md:2513-2519`) and
    their echoes (`design.md:476-478`, `:1059-1061`) are read as the withdrawn
    draft's residue, and a bookkeeping note in #1144 says so (FR-025).
  - The submission seam SHALL stay separate from the generator seam: the same
    pattern, a different registration point.
  - No governed host contributes a `SubmissionPort` in release 2 (R2Q2 (a) with
    R2Q3 (a)). Brett accepted that ruling `5783934499`'s third bullet
    (*"contributed by the governed host"*) therefore goes unrealized in release
    2.
- **FR-004** (requirement 11, first and second scenarios; 12.4a; R2Q1 (a), R2Q3
  (a), R2Q5 (a), R2Q9 (a) item 7): openDox SHALL own the act of submitting.
  - **The verb and the route.** The CLI verb is `submit --repo-root <repo>
    --branch <branch> [--local]`, and the route is
    `POST /actions/session/submit`. Both live in openDox's own surface, not
    under `gate`.
  - **One user-facing interface.** The verbs and routes, and the Health view's
    land action, SHALL be the same in every mode (R2Q1 (a)): every GOVERNANCE
    mode (`standalone`, `governed`, `unknown`) under openDox's own profile, on
    either install plane, so the hosted plane's refusals (R2Q15 (a)) are
    reachable there (the plan's CF-1, confirmed `6013547504`). No governed host's
    profile SHALL carry `submit`, `land` or `health` in release 2 (R2Q3 (a)): a
    host profile that replaces openDox's own carries none of them.
  - **The engine.** It SHALL take its `SubmissionPort` from FR-003's bindings,
    and return and print the `Submission`.
  - **The branch.** It SHALL accept any local branch except the default branch
    (FR-007's `main`), and refuse the default branch, naming the rule (R2Q5
    (a)).
  - **`--local`.** It SHALL take the same `--local` flag as
    `generate-and-open` (batch H). A flag and an install-mode setting that
    disagree SHALL be refused, naming both (R2Q9 (a), item 7).
  - **The route's gate.** The route SHALL refuse, in this order and before
    reading any body byte, a request off loopback, one without the `session`
    capability or a resolved human actor, and one that is not the human
    console. It SHALL take no repository from the request.
  - **The token.** On a standalone plane, the console token SHALL reach the
    page only through the URL the page is opened with (12.4a as T007 batch N
    records `5963851934`, with batch P's printed hint line and accepted
    limits).
  - **The CLI's actor.** The CLI verb runs as the invoking user, in that user's
    checkout. F12.2 runs it non-interactively with no actor (the plan's ruled
    default OQ-12-9).
- **FR-005** (requirement 11, tenth scenario; 12.5; F12.1; R2Q2 (a), R2Q8 (a)):
  openxFactory's GitHub pull-request flow SHALL behave exactly as today.
  - **It runs on `GhPullRequests`.** The flow runs on `pull_request_factory`'s
    unset default, `GhPullRequests`. 12.5's *"With the host's implementation
    registered"* goes unrealized in release 2, as Brett accepted with R2Q2 (a)
    and R2Q3 (a).
  - **The governed suites pass.** The computed set of openXdox-code suites that
    drive `open-pr` or inject `FakePullRequests` SHALL pass, and no arc landing
    SHALL edit them except through the reviewed allow-list (T007 batches C and
    I; R1Q7 (a), R1Q26 (a)).
  - **F12.1 runs composed, permanently.** It runs composed with openxFactory's
    `scripts/`, as F5.2 does under R1Q23 (a), by a bookkeeping line in #1144
    (FR-025). R2Q8 (a) said "until the `doc_health` direction arc's realization
    lands"; ARC-Q2 (a), the later ruling, makes the composed workflow permanent,
    and the plan ruling confirmed the reading that the composition is F12.1's
    permanent home (CF-5, `6013547504`). The composition is never removed when
    the arc lands.
  - **Phase 4 repairs the 174 reds.** It SHALL repair the 174 composed reds
    measured at `56e1c238` without editing any of the 16 suites, by four
    means:
    - a host-registering conftest outside them, as T104's `HOST_PLANE_SUITES`
      does;
    - the `display.js` harness copy fixed, and the gate console's two schemas
      (openXdox-spec's gate-action record and openxFactory's demotion
      execution receipt) placed where the suites read them;
    - an allow-list entry for each pure respelling (batch C);
    - each singleton traced, and repaired by one of these means or by an
      entry.
  - **The direction arc is decided first.** R1Q6 (d) still requires the
    `doc_health` direction arc to be DECIDED before 12.5 needs these suites
    (plan 034 T008).
- **FR-006** (requirement 11, fifth to ninth scenarios; 12.6): landing
  authority SHALL follow whoever governs the repository, and openDox SHALL ASK
  the repository rather than hard-code either answer. Three guardrails SHALL
  hold in EVERY mode, and none SHALL be configurable: a merge is an explicit
  human act, a conflict is shown and never silently resolved, and a merge is a
  commit that can be reverted. Each SHALL be a test, not prose. A governed
  host's implementation SHALL still declare no merge.
- **FR-007** (requirement 11; 12.6a; F12.2; R2Q3 (a), R2Q4 (a), R2Q5 (a), R2Q6
  (a), R2Q7 (a), R2Q9 (a) item 7): openDox SHALL declare
  `session_pr.LandingPort`, with ONE operation, `land(branch, *, confirmation)
  -> Landed`. It SHALL also declare the governance query
  `session_pr.repository_governance(checkout_root)`, which answers
  `standalone`, `governed` or `unknown` and FAILS CLOSED.
  - **The default branch is `main`**, openDox's existing session base. A
    repository with no `main` SHALL be `unknown`, refused naming it (R2Q7
    (a)).
  - **`standalone`** SHALL require BOTH the explicit local install
    (`OPENDOX_INSTALL_MODE=local`, or `--local`, which selects local exactly
    as the setting does, 13.4; R2Q9 (a) item 7) AND a committed
    `.opendox/governance.yaml` reading `governance: standalone`. The
    declaration is read from the tip of `main` at the moment of landing, never
    from the branch being landed or from the working tree. With no declaration,
    `land` SHALL refuse, naming the exact file and content for the owner to
    commit with git. The product SHALL never write `main` outside `land`
    (R2Q7 (a)).
  - **`governed`.** A registered host profile that declares an instrument SHALL
    make the repository `governed`, whatever any file says. A committed
    declaration that says `governed` makes it `governed` too, in the absence of
    such a host (12.6a). Precedence runs one way: the host, then `main`'s
    declaration, and never a branch's contents.
    - **The instrument** is the host's contributed `SubmissionPort`, declared in
      the host profile (R2Q4 (a)).
    - **Under `governed`,** no lander SHALL be bound. `land`, and the fix loop's
      land action, SHALL submit through the instrument and report where the
      work went. The merge stays the governance's act (R2Q4 (a)).
    - **With no instrument,** as under a declaration with no host registered,
      the repository is governed-without-an-instrument, 12.6a's own phrase:
      `land` refuses, naming what is missing.
    - **In release 2,** no production host declares an instrument (R2Q2 (a)
      with R2Q3 (a)). F12.2 proves the routing against a registered test
      host.
  - **`unknown`.** Everything else SHALL be `unknown`, treated as governed
    without an instrument: no lander is bound, and `land` refuses, naming what
    is missing.
  - **The lander.** Under `standalone`, the neutral lander SHALL be bound
    through `landing_factory`, declared beside `pull_request_factory`.
  - **The branch.** `land` SHALL take any local branch except `main` (R2Q5
    (a)). The CLI verb is `land --repo-root <repo> --branch <branch> [--local]`,
    and a flag and setting that disagree are refused, naming both (R2Q9 (a),
    item 7).
  - **The confirmation.** `confirmation` SHALL be an opaque, single-use
    capability that only two issuers mint:
    - the `land` verb's prompt, reading the typed branch name from the
      controlling terminal and refusing where there is none;
    - the view's confirm control, given a nonce the loopback server issued for
      that branch.

    Each token is bound to the branch and its head sha. A static check SHALL
    prove that no module outside those two interactive layers calls an issuer.
  - **Where the merge is made** (R2Q6 (a)). The lander SHALL make the `--no-ff`
    merge commit in a landing worktree of its own, outside the served checkout,
    and `Landed` returns its sha. Where the served checkout holds `main`, the
    lander SHALL then fast-forward it to the merge commit with
    `git merge --ff-only <commit>`, only when that checkout is clean, never
    switching, resetting or stashing it. A fast-forward that no longer applies
    SHALL refuse, leaving `main` where it was. Where the served checkout holds
    another branch, the lander advances `main` without touching it.
  - **Feature 007's four exceptions.** By Brett's word (R2Q6 (a)), feature
    007's served-checkout rule gains FOUR named exceptions, each scoped to a
    confirmed landing onto the branch the served checkout holds, and no other:
    1. `session_git.py`'s name-only guard (`:99`) gains an argument check that
       admits `merge --ff-only <commit>` alone at the served root.
       `tests/test_session_git.py:523`'s `("merge", "other-branch")` keeps
       refusing, and `:563-564`'s pin that `merge` is absent moves.
    2. `session_git.py:93`'s stated rule admits that fast-forward for the
       served working tree, its index and its `HEAD`.
    3. SC-002's "`HEAD` unchanged" admits it.
    4. SC-002's "working tree changes only inside the gate-records path" admits
       the files it brings.

    FR-004 of feature 007, and the scenario *"The served checkout is asked to
    move"*, hold unchanged.
  - **The remote** (R2Q6 (a)). `land` SHALL push nothing. Where a remote is
    attached, it SHALL first read the remote's default-branch tip with
    `ls-remote`, and refuse, naming the remedy, if `main` does not contain it.
    A landed `main` leaves the served checkout only by the user's own
    `git push`. For a plain repository, that reaches its remote directly. For
    a clone of a project's bare repository, it reaches the project repository,
    from which `project push` (RULING C3) carries it on. The openDox root's
    README documents both.
  - **A conflict** SHALL raise `MergeConflict` with the conflicting paths and
    leave `main` where it was.

**Phase 5 — the health engine, the fix loop, exceptions and packs (Groups 6, 14 and 15; requirements 6, 14, 15 and 16).**

- **FR-008** (requirement 6; 6.1, 6.1a, 6.2; F6.1; R2Q9 (a) item 1, R2Q14 (a),
  R2Q16 (a)): openDox SHALL carry a health check, over ITS OWN documents and
  reading its own declaration.
  - **It runs in process.** It runs from openDox's own checkout and in process,
    as trusted installed code, on every platform (R2Q16 (a)).
  - **The scoped action calls it.** openDox SHALL register it at the scoped
    seam through an entry point, so the scoped health action has something to
    call. A bare process with no registration still refuses, naming the seam
    (batch G). F6.1 is amended to build that entry point before its call, and
    its stale "Today" sentence is struck (R2Q9 (a), item 1).
  - **No family moves.** No openxFactory check family SHALL move
    (requirement 1). 6.1a is satisfied vacuously in release 2: no family moves,
    no module both sides depend on is created, and any relocation inside
    `doc_health` belongs to the direction arc's own Q4 (R2Q14 (a)).
  - **It is new code.** The packet's measurement (6.1) found ONE of
    `scripts/doc_health/`'s 37 modules free of corpus identifiers, and
    R2-INV-HEALTH part A finds two of 38 today (`lines.py`, and `fs_probe.py`,
    added since). So the check is new neutral code, not a relocated family. The
    plan's ruled default makes it the engine's built-in families, attributed
    `opendox` (OQ-H-3's plan half).
  - **A host's check.** A host's check registered through
    `register_health_check` (openxFactory's `scripts/opendox_host.py:524`)
    SHALL keep running in process at the scoped seam only, as release 1 left
    it. Its results SHALL NEVER be stored (R2Q16 (a)).
- **FR-009** (requirement 6 as amended; 14.1, 14.2, 14.3; R2Q13 (a), R2Q15
  (a), R2Q25 (a)): health results SHALL be DERIVED DATA, kept in the product's
  disposable store and never committed into the corpus they describe.
  - **The migration.** Their table SHALL arrive as an ADDITIVE `0003_`
    migration, never an edit to `0001`.
  - **A domain table.** The table is a DOMAIN table. It SHALL join RULING Q1's
    closed list in `identity.TABLES`, and the closure test SHALL read `0001`
    together with `0003_`, both in the same change. The served role's access is
    verified like the other six tables' (R2Q13 (a)).
  - **No document.** The store SHALL hold no document and stay disposable, so
    its loss costs a recomputation. A finding's `evidence` SHALL hold locators
    only: a path, a line, a link-target string or a family-defined key, and no
    text of a document (R2Q25 (a)).
  - **The local plane only.** The health engine SHALL run on the local plane
    and from the CLI only. On the hosted plane, the Health view, its routes and
    the `health` verbs SHALL refuse by name before anything runs, as `submit`
    does, and record nothing. The schema still migrates there, because there is
    one migration set (R2Q15 (a)).
- **FR-010** (requirement 6; 14.4; R2Q11 (a), R2Q12 (a)): the neutral families
  SHALL be the ruled six:
  - broken internal links;
  - documents nothing links to;
  - near-duplicates;
  - missing neutral front matter from the adapter's fields;
  - a declared stage that disagrees with the document's location;
  - stale or empty stubs.

  A document's **location** is a top-level directory whose name is one of the
  six role keys or their declared words. A document outside such a directory
  has no location and is never flagged (R2Q11 (a)).

  The families SHALL run on demand from the view and the CLI, and optionally on
  commit. They SHALL report where the human is already working, never by filing
  into an external tracker, and SHALL run any model-assisted check only where a
  model is configured. openxFactory's 23 governance families SHALL stay with
  openxFactory.

  They SHALL be BASELINE-RELATIVE, as follows (R2Q12 (a)):
  - **The baseline** is the previous COMPLETE, FULL run at the baseline
    branch's tip OF THE SAME CORPUS (its resolved root), held in the store; a
    run of another repository in the same store is never a baseline, and
    neither is a run restricted by `--pack` or one where a pack failed, so a
    partial run never advances it. The baseline branch is `main`, else the
    branch HEAD names (I-2 (a), `6013547504`); R2Q7 (a)'s `main` still governs
    landing alone.
    Every run is classed against it, whether at the tip, on a branch or over
    the working state.
  - **The pack inventory.** Every run SHALL record the `pack_version` of every
    pack it ran, zero-finding packs and openDox's own included. "The
    baseline's `pack_version` for its pack" is read from the baseline run's
    inventory, never from its findings.
  - **New:** absent from the baseline, at the baseline's `pack_version` for its
    pack.
  - **Arrived with a pack upgrade:** absent from the baseline, at a different
    stamped `pack_version` (15.7). It is reported apart from new (D12). A pack
    the baseline run did not run (one newly added) has no baseline version, so
    its first findings arrive this way: they came with a pack change, not a
    document change, which is D12's reason for the class.
  - **Persistent:** present in the baseline. A finding whose id persists across
    a pack upgrade stays persistent.
  - **Disappeared:** measured ONLY between two complete, full runs at the
    baseline branch's tip. A branch, working-state, `--pack`-restricted or
    incomplete run never raises one. An id the later run suppresses as
    accepted is not a disappearance: it is accepted, not gone (Copilot's
    review of `2076f24b`).
  - **Cited:** a disappearance is cited by a landing of the fix loop's draft for
    it, or by a commit that names its id in a `Finding:` trailer. The fix loop
    writes that trailer on every repair commit, a batch draft's included, so
    both are read the same way: from the trailers of the commits between the
    baseline run's commit and the run's own (`git rev-list B..R`), never from a
    branch name. An uncited one
    SHALL be re-raised once, as a `human-only` finding naming the original.
    The re-raise is one engine-authored finding with its own id, in the run
    that measured the disappearance; it is never itself measured as a
    disappearance, so the next run raises nothing for either id
    (contracts/health-finding.md; Copilot's review of `67d6f28b`).
  - **A reset** forgets the baseline. The first run after it sees every finding
    once as new, and pending uncited disappearances are forgotten. This narrows
    14.3's and ruling `5784155201` item 4's *"recomputable from git"* for
    pending disappearances, a reading Brett took.
- **FR-011** (requirement 14, first and seventh scenarios; 14.5; R2Q9 (a) items
  2 and 7, R2Q10 (a), R2Q15 (a)): the Health view SHALL be served by the entry
  point on a local install, and every resolution action in the view SHALL have
  a CLI verb with the same action. The verbs are:

  | verb | shape |
  |---|---|
  | `health run` | `health run --repo-root <corpus> [--pack ID] [--timeout SECONDS] [--local]` |
  | `health list` | `health list --repo-root <corpus> [--json] [--local]` |
  | `health fix` | `health fix --repo-root <corpus> --finding ID [--batch] [--local]` |
  | `health accept` | `health accept --repo-root <corpus> --finding ID --reason TEXT [--local]` |

  - **Options follow the verb.** A `--local` flag and an install-mode setting
    that disagree SHALL be refused, naming both (R2Q9 (a), item 7).
  - **The verbs need the bundle.** Like the runtime verbs, they reach the
    running bundled store that the document server owns (R1Q16), and refuse by
    name without one (R2Q9 (a), item 2).
  - **On a hosted install** they refuse by name (R2Q15 (a)).
  - **The JSON shape.** `health list --json` SHALL emit one object per finding
    with `id`, `kind`, `resolution_class`, `path`, `severity`, `evidence`,
    `pack_id` and `pack_version`.
  - **A finding's `id`** is a STABLE, pack-qualified key. The engine derives it
    from the pack id, the family, the document's path and a locator the family
    supplies. It survives a store reset, is unique, and is mapped into a valid
    ref name for `health-fix-*` (R2Q10 (a)).
  - **Parity.** The `/capabilities` payload's health block SHALL list every
    action the view offers, so parity is a comparison, made by three named
    tests.
- **FR-012** (requirement 14, second to fourth scenarios; 14.6; R2Q11 (a)):
  findings SHALL be resolved in three declared classes, spelled `auto-fix`,
  `assisted` and `human-only` in the store, the CLI, the view and the pack
  contract alike.
  - `auto-fix` covers the mechanical findings, written by the product. The
    `stage-location-mismatch` repair SHALL edit the document's `stage:` header
    to match its directory, and SHALL never move the file (R2Q11 (a)).
  - `assisted` covers proposals the human edits, model-written only where a
    model is configured.
  - `human-only` shows the evidence.

  The applier SHALL be new work, since nothing in the estate applies a fix
  today. The classes of the families the ruling did not place are a plan
  default (OQ-H-8: `human-only`).
- **FR-013** (requirement 14, second, fifth and sixth scenarios; 14.7): every
  repair of every class SHALL be written as a DRAFT ON A BRANCH and never onto
  the default branch, and it SHALL reach the default branch only through
  FR-006's and FR-007's landing rule. NOTHING SHALL land automatically, not even
  a one-line mechanical repair. Several repairs MAY be batched into one draft
  for one review, which lands under the same rule.
- **FR-014** (requirement 15; 14.8): an exception SHALL be recorded IN THE
  CORPUS as a committed artifact, on the pattern of `health/dispositions.yaml`,
  and never in the store. It SHALL survive a store reset, be reviewable as an
  ordinary change to the corpus, and cite what it accepts, so that removing it
  re-opens its finding on the next run.
- **FR-015** (requirements 14 and 15; 14.9; F14.1; R2Q9 (a) item 2, R2Q10 (a)):
  openDox-code SHALL ship `tests/fixtures/health-corpus`, a small corpus. It
  carries ONE finding of every kind requirement 14 names, and nothing else a
  neutral family would flag:
  - `auto-fix`: `broken-link`, `derivable-front-matter` and
    `stage-location-mismatch`;
  - `assisted`: `near-duplicate`, and ONE EMPTY STUB, which requirement 14's
    third scenario and 14.6 class as `assisted` though 14.9's list omits it
    (the plan's T043; ADV-17). F14.1 asserts 14.9's list and no more, so the
    empty stub's class is proved by T044's and T053's tests;
  - `human-only`: one human-only finding;
  - one finding to be accepted.

  F14.1, as amended, SHALL exit 0 over it. The amendment has two parts:
  - It first starts `opendox generate-and-open --repo-root $C --repository
    fixture --no-open --port <port>` in the background, with the setting
    already exported, as F13.1 does. It waits for readiness, and kills the
    server on exit (R2Q9 (a), item 2).
  - It selects each planted finding by its fixture document, not by a literal
    id (R2Q10 (a)).
- **FR-016** (requirement 16; 15.1, 15.1a; R2Q18 (a), R2Q21 (a), R2Q22 (a)):
  openDox SHALL declare a NEUTRAL CHECK-PACK CONTRACT on the `corpus_adapter`
  protocol pattern, a `@runtime_checkable` protocol with a closed member set.
  - **The manifest.** The engine SHALL load packs ONLY from the corpus's
    committed `health/packs.yaml`, which is authoritative for what the engine
    runs. Its entries carry `id`, `version`, `source` and a REQUIRED
    source-tree `digest`, as `neutral-product-pin` defines it. A lockstep check
    against a domain's `stack.yaml` is owed by F2, not by release 2 (R2Q21
    (a)).
  - **The commit field.** A git-URL source SHALL carry a `commit`. A
    corpus-relative source SHALL NOT, and one that does is refused.
  - **The pin.** The engine SHALL verify the pin before importing any line of
    the pack. A listed pack whose source no longer matches its digest SHALL be
    refused as a finding carrying both digests.
  - **No discovery.** There SHALL be no entry-point scanning and no import-path
    discovery.
  - **What a pack may import.** A pack is Python source that uses only the
    standard library and the neutral contract module the engine's runner
    provides. The pack's digest plus the install's version
    (`importlib.metadata.version("opendox")`) pin everything that runs
    (R2Q18 (a)).
  - **The schemas.** openDox-spec SHALL own a schema for each of the contract's
    three serialized artifacts: the exceptions file, `health/packs.yaml`, and
    the finding's neutral shape. openDox-code carries digest-checked copies
    (R2Q22 (a)).
- **FR-017** (requirement 16; 15.1b; R2Q9 (a) items 3 and 5, R2Q15 (a), R2Q16
  (a), R2Q17 (a), R2Q19 (a), R2Q20 (a)): every manifest-listed pack SHALL run in
  a separate process, inside an OPERATING-SYSTEM-ENFORCED sandbox, never by
  convention.
  - **The export.** The engine SHALL export the corpus commit into a directory
    it owns, and mount it read-only as the pack's only view of the user's data.
    The export SHALL NOT be steered by `export-subst` or `export-ignore`: either
    it is not a plain `git archive`, or those attributes are refused (R2Q9 (a),
    item 5).
  - **What the pack sees.** Beside the export, the pack sees only:
    - its own pinned code;
    - the interpreter paths its runtime needs, read-only;
    - a private scratch space, discarded with the sandbox;
    - the sandbox's own process and device filesystems.

    It sees no git history (R2Q19 (a): requirement 16 and 15.1b kept as
    ratified).
  - **Isolation.** The pack SHALL have no network and no model channel (R2Q20
    (a): kept as ratified). It SHALL have a cleared environment with an
    explicit allowlist, and no inherited descriptor. Its whole process tree
    SHALL end with the sandbox.
  - **No sandbox.** Where the platform offers no such sandbox, packs SHALL NOT
    run, and `health run` SHALL report that as one finding against the install.
    `bwrap` is the Linux reference. Release 2 has no Seatbelt realization, so
    macOS runs no packs (R2Q16 (a)). A hosted install runs none either, because
    its health surfaces refuse by name (R2Q15 (a)).
  - **Trusted code runs in process.** The product's own checks, and a host's
    scoped check (FR-008), SHALL run in process on every platform. They are not
    sandboxed. Requirement 16's sandbox clause (`spec.md:544-545`) is recorded
    as governing manifest-listed packs, and its attribution clause
    (`:585-587`) as attribution only (R2Q16 (a)).
  - **CI** (R2Q17 (a)). openDox-code's required `validate` job SHALL:
    - pin `ubuntu-24.04`;
    - install `bubblewrap`;
    - set `kernel.apparmor_restrict_unprivileged_userns=0`;
    - prove the sandbox live before the suite.

    Under `CI`, the sandbox tests SHALL FAIL rather than skip, mirroring
    `tests_runtime/conftest.py:130-147`, so `EXPECT_SKIPPED` stays at 11. A move
    to 26.04 waits until its bwrap profile is measured on a runner, and there is
    no macOS job. Brett made this required-check change by his word.
  - **F15.1's precondition.** F15.1 SHALL assert its precondition, a working
    kernel sandbox, and exit 1 naming it otherwise (R2Q9 (a), item 3).
- **FR-018** (requirement 16; 15.2, 15.2a; R2Q25 (a)): a pack SHALL declare its
  own version, equal to its manifest entry's, and its check families with an
  id, a version and the documents each applies to.
  - **What it returns.** It SHALL return findings in the neutral shape:
    severity, one of the three classes, and evidence. Evidence holds locators
    only and no text of a document (R2Q25 (a)). It MAY return proposed fixes as
    unified-diff patches only.
  - **Patch validation.** The engine SHALL validate every patch BEFORE any
    branch exists, and refuse one that:
    - edits a path other than its own finding's document;
    - names an absolute path, or one with a `..` or `.git` component in any
      letter case;
    - targets, or lies below, a symbolic link;
    - creates, deletes, renames, copies or re-modes a file, or is binary;
    - exceeds the engine's bound, 65,536 bytes by default, which no pack can
      raise.
  - **A refusal** SHALL be a finding against the pack, naming the refused
    finding and the failed check, and SHALL create no branch.
- **FR-019** (requirement 16; 15.3, 15.4; R2Q12 (a)): a pack's labels SHALL
  resolve through the display facet and never be spelled into the neutral
  surface. The ENGINE SHALL own, identically for every pack:
  - the view and its CLI parity;
  - scheduling;
  - the baseline, with its three classes and its default-tip disappearance rule
    (FR-010);
  - storage: results in the store, exceptions in the corpus;
  - the fix loop, with its landing rule.

  No pack SHALL redefine the resolution classes, the baseline rules or who may
  land work.
- **FR-020** (requirement 16; 15.5, 15.6, 15.6a; R2Q9 (a) items 2–6, R2Q17 (a)):
  each refusal SHALL be a test, not prose, and SHALL run in openDox-code's
  required check under FR-017's CI terms.
  - **A failing pack.** A pack that crashes, overruns its per-pack time budget,
    or returns output the engine cannot parse SHALL be reported as a finding
    against that pack, and the other packs SHALL still run. The budget is
    `health run --timeout`, a default declared by 15.6 and enforced by the
    engine.
  - **The pack corpus.** openDox-code SHALL ship `tests/fixtures/pack-corpus`:
    14.9's corpus plus the eight fixture packs 15.6a names. They are registered
    by corpus-relative source, pinned by digest and carry no `commit`, with a
    test that keeps their digests current.
  - **The forking pack** gives its child its own pack id in argv, so F15.1's
    `ps` check cannot pass vacuously (R2Q9 (a), item 4).
  - **The escaping pack** counts a WRITE as its "restores write permission"
    success, never a chmod (R2Q9 (a), item 6).
  - **F15.1, as amended,** first starts the document server for its `health`
    verbs, as F14.1 does, and selects planted findings by their fixture
    document (R2Q9 (a), item 2; R2Q10 (a)).
- **FR-021** (requirement 16, seventh scenario; 15.7): every finding SHALL carry
  `pack_id` and `pack_version`, stamped by the ENGINE from the manifest entry
  that launched the run, never read from what the pack returns. Both SHALL be
  `NOT NULL` columns in the same `0003_` migration as the results table. The
  product's own checks SHALL be attributed to `opendox` and the installed
  version (`importlib.metadata.version("opendox")`), as the one pack no manifest
  lists, and no manifest entry SHALL claim that id.

**Every phase.**

- **FR-022** (requirement 1; 11.0, 11.1, F11.1): release 2 SHALL move nothing out
  of openxFactory. Every realization landing, in every repository the arc
  touches, SHALL carry `Arc: neutral-product-standalone-operability`, and
  bookkeeping SHALL NOT (R1Q20 (a)). openxFactory's arc edits SHALL stay on
  F11.1's declared surfaces, and the `ADMITTED_ARC_EDITS` list SHALL grow only
  by a further ruling, never by edited guard code alone (`5890601202`).
- **FR-023** (9.5; R2Q22 (a), R2Q23 (a)): the pins that compose the legs SHALL
  advance by their owners' ordinary pin-sync acts, each in the landing that
  needs release 2's code. Each of openxFactory's two pairs SHALL move in ONE
  commit. Two cuts are owed, each under a recorded addendum at 9.5:
  - **The bundle.** The openDox root SHALL cut ONE more `dox-v1.y` minor,
    carrying FR-016's three schemas, under a batch-G style addendum. No
    repository joins the arc (R2Q22 (a)).
  - **PyPI.** `opendox` 0.2.0 SHALL be published at release 2's cut, through
    the existing trusted-publishing workflow, with one tag, `v0.2.0`, under a
    batch-O style addendum. It is published on Brett's publish word, after
    FR-024's acceptance passes (R2Q23 (a)).
- **FR-024** (acceptance; R2Q24 (a)): release 2 SHALL pass AT-R2 before its
  bookkeeping ticks the release-2 boxes. AT-R2 is defined in AT-R1's form, on a
  clean machine with only `opendox[local]` and a plain repository:
  - the Health view lists findings, new first;
  - a mechanical repair is drafted from the view, and landed through the view's
    confirm control as a revertible merge commit;
  - an exception survives `runtime reset`;
  - a branch is submitted to a bare remote with `gh` absent.

  It runs as an HTTP half in CI and a browser half on the host, beside #1144's
  falsifiers and named tests.
- **FR-025** (process; R2Q2 (a), R2Q8 (a), R2Q9 (a), R2Q10 (a)): no task SHALL
  start while a question in its `Blocked by:` line is open. Every realization
  PR SHALL name its task ids, the boxes it realizes and the falsifier it ran,
  with the output quoted.
  - **The answers' amendments.** The answers' changes to #1144 SHALL land as
    bookkeeping in T007's form, under a Rule 6 window, with no `Arc:` trailer:
    - R2Q9 (a)'s seven amendments, as ONE batch, before phase 4's first
      checkpoint;
    - R2Q2 (a)'s note on 12.4's repoint sentences;
    - R2Q8 (a)'s F12.1 composed-run line;
    - R2Q10 (a)'s selection lines in F14.1 and F15.1.

    Whether the last three ride in R2Q9 (a)'s batch is the plan's to state.
  - **The arc's close.** The plan's ruled default is that this feature
    performs and ticks 9.5, 11.0, 11.1 and F11.1, and plan 034's T090–T093
    close by reference (OQ-038-2). 11.0, 11.1 and F11.1 tick at the arc's
    close (T082); 9.5 ticks LAST, at T084, after the cut's pin syncs (T083) and
    the 0.2.0 publish (ARC-5 (a)).

### Key Entities

- **Submission port** (`SubmissionPort`): the neutral act of moving work out of
  the local repository. Its one operation returns a **Submission** (`remote`,
  `ref`, a redacted `url`). The neutral default is `LocalGitSubmissions`, and
  its refusal is `NoSubmissionTarget`. A governed host's contributed port is
  also its **instrument** for landing (R2Q4 (a)).
- **Pull-request port** (`PullRequestPort`): the governed host's platform
  protocol, unchanged, served by `GhPullRequests` (the unset default) and
  `FakePullRequests`.
- **Landing port** (`LandingPort`): the act of landing a branch into `main`. It
  returns **Landed** (the merge commit's sha) or raises **MergeConflict** (the
  conflicting paths). Its merge is made in a landing worktree.
- **Repository governance**: `standalone`, `governed` or `unknown`, answered by
  `repository_governance` and failing closed. The **governance declaration** is
  `.opendox/governance.yaml`, read from `main`'s tip.
- **Confirmation**: an opaque, single-use capability bound to a branch and its
  head sha, minted only by the `land` prompt or the view's confirm control.
- **Finding**: one health result, with `id`, `kind`, `resolution_class`,
  `path`, `severity`, `evidence`, `pack_id` and `pack_version`. It is derived
  data, kept in the store. Its `id` is a stable, pack-qualified key (R2Q10
  (a)), and its `evidence` holds locators only (R2Q25 (a)).
- **Resolution class**: exactly `auto-fix`, `assisted` or `human-only`.
- **Baseline**: the previous complete, full run at the baseline branch's tip
  (`main`, else the branch HEAD names; I-2 (a)) of the same corpus, held in the
  store. Against it,
  a finding is new, persistent, or arrived with a pack upgrade (D12). Between
  two such runs, a finding can have disappeared. It is owned by the engine, no
  pack may vary it, and a store reset forgets it (R2Q12 (a)).
- **Fix draft**: a repair written as a commit on a branch (`health-fix-<finding>`
  in F14.1). It is distinct from the runtime's `drafts` table, which RULING Q1
  keeps for unsaved document bodies.
- **Exception**: a human's decision that a finding is accepted. It is committed
  in the corpus at `health/dispositions.yaml` and never kept in the store.
- **Check pack**: arbitrary code that supplies check families. It is listed and
  pinned in the corpus's committed `health/packs.yaml`, run in a sandbox, and
  attributed by its manifest entry. It uses only the standard library and the
  engine's contract module. The product's own checks are the pack `opendox`,
  which no manifest lists and which runs in process.
- **Proposed patch**: data a pack returns, validated by the engine before any
  branch exists.
- **Arc landing**: a commit on a repository's `main` first-parent line that
  carries the `Arc:` trailer. 12.5's and 11.1's guards read it.
- **Pin pair**: a gitlink plus its `contracts/*-pin.yaml`, moved in one commit.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001** (phase 4 exit):
  - F12.2 exits 0 in an openDox-code checkout alone with `gh` absent. That
    includes its thirteen named guardrail tests, its five named route tests and
    its two named submission-default tests.
  - F12.1 exits 0, run composed, with all 174 measured reds repaired and none
    of the 16 suites edited except through the allow-list (R2Q8 (a)).
- **SC-002** (phase 5 exit): F6.1, F14.1 and F15.1 exit 0, each as amended
  (R2Q9 (a), R2Q10 (a)). F15.1 runs in openDox-code's required `validate` job,
  where the reference sandbox is proved live.
- **SC-003**: after each phase's openxFactory landings, an interim F11.1 run
  (`PACKET_MERGE=94b6f7f1`) prints `requirement 1 holds`.
- **SC-004**: at release 2's close, all 37 release-2 boxes are ticked, each with
  its evidence: Group 6's 4, Group 12's 11, Group 14's 10 and Group 15's 12.
  The every-phase boxes 11.0, 11.1 and F11.1 are ticked at the arc's close, and
  9.5 last, after the cut's pin sync and the 0.2.0 publish that still realize
  it.
- **SC-005**: openxFactory's required checks are green at every pin advance
  release 2 makes. openDox-code's required check keeps running its whole suite,
  with no declared exclusion. Release 2's named tests run in it, the sandbox
  tests included, and `EXPECT_SKIPPED` stays at 11 (R2Q17 (a)).
- **SC-006** (the user's outcomes):
  - a student on a machine without `gh` gets a branch's work to an attached
    remote with ONE command, and is told plainly when there is no remote;
  - a standalone owner lands with ONE confirmed act, which ONE
    `git revert -m 1` undoes;
  - the view offers zero resolution actions that the CLI lacks, and the CLI
    offers zero the view lacks;
  - the store holds zero findings without a pack id and a pack version, and
    zero findings whose evidence quotes a document;
  - a store reset loses zero exceptions;
  - every local install, sandbox or none, gets health over its own documents.
- **SC-007**: zero landings of release 2 merge automatically. Every landing on a
  default branch traces to a human confirmation or to the governance's own
  instrument.
- **SC-008**: AT-R2 passes both halves, the HTTP half in CI and the browser half
  on the host, before the release-2 boxes are ticked (R2Q24 (a)).

## Assumptions

- **Release 1 is complete.** Plan 034 reads 92 of 96 tasks. The four open ones,
  T090–T093, are the every-phase tasks for 9.5, 11.0, 11.1 and F11.1, which
  were left open for the arc's close after release 2. `opendox` 0.1.0 is on
  PyPI (T099). F9.2 stays open until the `doc_health` direction arc lands (plan
  034 T008; RULED `5859927858`). Since the archive needs both releases'
  evidence, the archive also waits on that arc.
- **The rulings stand as encoded.** `5783934499`, `5784155201`, `5784247356` and
  `5784295745` are sequenced, not reopened. Requirements 6, 11, 14, 15 and 16
  are #1144's as written, and no round-1 answer changes their text (R2Q19 (a),
  R2Q20 (a)). The two corrections #1144 already records stand: the migration
  is `0003_`, not `0002_`, and the closure test is scoped to the canonical
  migration (`design.md` § D10.4).
- **Readings Brett took.** Round 1 records four readings of #1144's text, each
  on his word. None changes a requirement or a scenario.
  - "one interface for both" is one user-facing interface (R2Q1 (a));
  - 12.4's repoint sentences are residue (R2Q2 (a));
  - the baseline's reset narrows "recomputable from git" for pending
    disappearances (R2Q12 (a));
  - requirement 16's sandbox clause governs manifest-listed packs (R2Q16 (a)).
- **`0003_` is still the next number.** openDox-code `a9ac96f9` carries
  `migrations/0001_identity_and_coordination.sql` and
  `migrations/0002_migration_state.sql`, and nothing else. With R2Q13 (a), the
  table joins Q1's list, and about twenty assertions move with `0003_`
  (R2-INV-HEALTH part A § 1).
- **The seam the scoped health action calls exists, and is empty.** Release 1's
  4.3 routed `run_scoped_doc_health` through
  `opendox.workbench.register_health_check`. The scoped action no longer
  catches the `ImportError` that 6.2 describes. Measured in a bare process at
  `a9ac96f9`, `run_scoped_doc_health(".", ["README.md"])` answers
  `not-available`, *"no health check is registered at openDox's health-check
  seam"*, and `DEFAULT_SCOPED_FAMILIES` is `("status-validity",
  "tag-hygiene")`. F6.1, as R2Q9 (a) item 1 amends it, registers openDox's own
  check through an entry point first.
- **The bundled store's ownership is release 1's.** At `a9ac96f9`, a local-mode
  `runtime status`, `migrate` or `reset` refuses unless a live bundled server of
  this data directory is running: *"A local install's server is started by
  `opendox generate-and-open --local`, which owns it"*
  (`runtime/bundle.py`, `refusal_before_connecting`). R2Q9 (a) item 2 keeps
  that ownership. The `health` verbs reach the running bundle, and F14.1 and
  F15.1 start the document server first.
- **12.5's governed set at `56e1c238`.** `git grep -l -e open-pr -e open_pr -e
  FakePullRequests -- 'tests/test_*.py'` selects 16 files. Fifteen are entries
  of openXdox-code's `tests/declared_exclusion.yaml`, each with the reason
  `doc_health`. `tests/test_gate_loop_views.py` is the one that runs alone.
  Composed with openxFactory's `scripts/`, the 16 read 668 passed, 170 failed
  and 4 errors: 174 red across 11 files, the same 174 that plan 034's T086
  recorded (R2-INV-12 M3, re-measured by this feature on 2026-10-05). The
  other 5 suites pass composed, 210 cases (R2-INV-P4F § "Passing composed
  today"; corrected from "10 files" in plan 038's review round 1).
  - By first cause: 62 need a registered host, 55 are the `display.js` harness
    copy, 16 read moved names or paths, 16 cannot load the gate console's
    schemas (`gate_console.py:642-643` reads a `contracts/schemas/` the code
    leg does not have, for the gate-action record and the demotion execution
    receipt), 3 reach a moved `hosted_index`, and 22 are singletons.
  - Lane openXfactory-3 confirmed this split, and appended an erratum to its
    inventory.
  - R2Q8 (a) puts their repair in phase 4.
- **The served checkout does not move, but for four named exceptions
  (feature 007).**
  - **The spec.** codexFactory's `specs/007-workbench-branch-sessions/spec.md`,
    at `main` `1a32f399`, refuses any session operation that would switch,
    reset or stash the served checkout (FR-004, `:517-519`). It holds that
    checkout's branch and `HEAD` unchanged across every session operation
    (SC-002, `:811-816`).
  - **The realization.** openDox-code's `session_git.py` realizes this:
    - its guard is an allowlist of subcommand NAMES (`:99`), under the stated
      rule that nothing on it touches the served working tree, its index or
      its `HEAD` (`:93`);
    - `merge`, `revert` and `update-ref` are absent from it (`:93-97`);
    - `tests/test_session_git.py` pins `merge` twice: it refuses
      `("merge", "other-branch")` at `:523`, and asserts `merge`'s absence,
      with `update-ref`'s, at `:563-564`;
    - `fetch` and `pull` are refused everywhere (`:125`).
  - **The exceptions.** R2Q6 (a)'s four exceptions (FR-007) apply by Brett's
    word, scoped to a confirmed landing alone.
- **openDox already ships one push, and it is not the served checkout's.**
  - `project push` (RULING C3; `runtime/cli.py:114`, `:1213`) pushes the
    branch that a project repository's HEAD names
    (`runtime/repository_act.py:1266-1298`, `push_to_remote`).
  - That repository is the BARE one `project create-repository` makes
    (`:982`; Q-R1, `5701772032`).
  - The document server serves the working tree of the checkout named by
    `--repo-root` (`serve.py:2107`), and reads no project row.

  R2Q6 (a) keeps `land` push-free, so a landed `main` leaves a served checkout
  only by the user's own `git push`, onward by `project push` where the checkout
  is a clone of a project repository.
- **A standalone install has no session opener of its own.** Every
  session-opening verb is a gate verb, and release 1 RULED Save refused by name
  on standalone (`5971834845`). R2Q5 (a) makes a standalone session opener and
  Save a follow-on outside release 2. Until then, a standalone user edits with
  git or through the fix loop.
- **Release 2's verbs are new surface.** At `a9ac96f9`, `opendox.cli` declares
  no `submit`, `land` or `health` verb. R1Q4 (a) has openDox's default profile
  contribute them, and `default_profile.py:41` records the same. By R2Q3 (a),
  no host's profile contributes them in release 2.
- **The line numbers #1144's boxes cite have moved.** This is non-normative,
  and the plan cites live lines. At `a9ac96f9`:
  - `cli.py:800`'s `_pull_request_port` and `:812-814`'s construction are at
    `:1292-1306`;
  - `serve.py:766`'s `pull_request_factory` is at `:1062`, and its unset
    default at `:1227-1230`.

  R2-INV-12's line-drift table has the rest.
- **Platforms.** Release 2 targets the platforms release 1 targets (plan 034,
  round 13 and ruling B2). The product's own checks run in process on all of
  them. Packs run only where a kernel-enforced sandbox exists, so in practice
  on a capable Linux host (R2Q16 (a)).
- **"Near-duplicates via the existing engine"** (`5784155201`) is read, as the
  plan's ruled default, as openDox's own similarity backend, `doxbench_knowledge.py`'s
  hashed n-gram projection (OQ-H-21).
- **Out of scope:**
  - release 1's groups, and Group 8 (openDox-spec's re-promotion);
  - a standalone session opener and Save (R2Q5 (a));
  - a Seatbelt realization, and a macOS CI job (R2Q16 (a), R2Q17 (a));
  - the follow-ons:
    - F1, the openXdox governance pack, which is what gives openxFactory's 23
      families a pack;
    - F2, each domain's own pack, with its `stack.yaml` lockstep check
      (R2Q21 (a));
    - F3, the wording overlays;
    - F4, the direct-arrow revisit.
- **Lane discipline:**
  - Rule 6 windows cover any PR that touches `openspec/changes/`. This
    feature's spec PR touches none; FR-025's bookkeeping does.
  - Bookkeeping carries no `Arc:` trailer (R1Q20 (a)).
  - Every `gh` call names its repository.

## Risks

- **The reference sandbox is unavailable by default on every target the estate
  runs today** (R2-INV-HEALTH part B § 1 and § 4.4):
  - in this lane's container, `bwrap` exits 1, *"No permissions to create new
    namespace"*;
  - GitHub's `ubuntu-24.04` restricts unprivileged user namespaces through
    AppArmor;
  - the hosted pod is inferred to be the same, and its masked `/proc` defeats
    `--proc`;
  - macOS Seatbelt cannot give an own `/proc` or a PID namespace, so it cannot
    meet requirement 16 as written.

  So 15.1b's "packs do not run" is the default outcome everywhere until a host
  is made capable. R2Q16 (a) keeps every install's own health check, which runs
  in process. R2Q17 (a) makes openDox-code's required `validate` job capable:
  it pins `ubuntu-24.04` with bubblewrap and the AppArmor sysctl, and the
  sandbox tests fail rather than skip there.
  - **The runner image.** If the image or its kernel changes, the required check
    reds rather than silently skipping. `ubuntu-latest` moves to 26.04 between
    2026-10-19 and 2026-11-19, and the pin holds release 2 on 24.04 until 26.04
    is measured.
  - **Local runs.** Developers still cannot run the sandbox suite in the
    estate's own containers.
- **12.5 cannot pass in any environment measured** (R2-INV-12, re-measured).
  R2Q8 (a) puts a repair slice in phase 4: 174 reds, repaired without editing
  the 16 suites. It starts on the plan ruling (`6013547504`). R1Q6 (d)'s
  direction-arc decision was ruled on `6003918488`, and the composed run is
  F12.1's permanent home (ARC-Q2 (a), read with R2Q8 (a) as the plan's CF-5).
- **Three standing invariants stood in the way of four boxes, and the answers
  meet each by a named act, not by assumption:**
  - feature 007's served checkout, against 12.6a's merge: four exceptions, by
    Brett's word (R2Q6 (a));
  - batch G's empty seam, against F6.1: F6.1's amendment (R2Q9 (a), item 1);
  - R1Q16's bundle ownership, against F14.1 and F15.1: their amendment (R2Q9
    (a), item 2).

  Each lands only if FR-025's bookkeeping batch lands under its Rule 6 window
  before phase 4's first checkpoint.
- **Two texts of #1144 go unrealized in release 2, by Brett's acceptance**
  (R2Q2 (a) with R2Q3 (a)): ruling `5783934499`'s *"contributed by the governed
  host"*, and 12.5's *"With the host's implementation registered"*. A later act
  that registers a host's `GhPullRequests` realizes them.
- **A repository with no `main` cannot land** (R2Q7 (a)), until its owner
  creates or renames `main`. That includes a repository the product itself
  created on another branch. Its health baseline still holds: the baseline
  branch is the branch HEAD names (I-2 (a), ruled `6013547504`), so R2Q12 (a)'s
  classes and disappearances apply there too. Only a detached HEAD has no
  baseline branch, and there every finding reads as new.
