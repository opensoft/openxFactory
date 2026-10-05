# Feature Specification: openDox, the document tool and self-maintenance (release 2)

**Feature Branch**: `038-opendox-document-tool-self-maintenance`
**Created**: 2026-10-05
Status: draft
**Clarifications**: 24 questions are OPEN in
[`clarify-questions.md`](./clarify-questions.md), `R2Q1`–`R2Q24`, and each
awaits Brett Heap. The same file defers 35 design-level questions to the plan,
each with a proposed default. No phase is planned until round 1 is answered.
**Realizes**: RELEASE 2, "the document tool and self-maintenance", phases 4–5,
of the openxFactory OpenSpec change `add-neutral-product-standalone-operability`
(#1144, landed `94b6f7f1`). The phases follow that change's RULED release map
(`#656` `5799646419`, as corrected by `5800995035`). Phase 4 is Group 12, phase
5 is Groups 6, 14 and 15, and Group 11 (the guard) and box 9.5 (the pins) run
in every phase.
**Lane**: `openxfactory-4`
**Input**: the lane's brief of 2026-10-05. It asks for the `/speckit.specify`
step alone: a specification written faithfully from #1144 and its four
release-2 rulings, with every genuinely undecided point put as a question. No
code is written until the plan is ruled.

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
`6001702967`, verbatim *"Start release 2 (Recommended)"*. This file specifies
release 2 and realizes none of it.

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
of requirement 1, and names it with its boxes. Nothing here restates, narrows
or widens the packet. Where this file appears to do so, that is a defect in
this file, and the packet wins. Where the packet contradicts itself, its
rulings, or the release-1 code it now has to build on, the contradiction is put
to Brett as a question. It is never settled here by assumption. The questions
are named `R2Q<n>`, because a bare `Q<n>` names one of #1144's own rulings
(RULING Q1, RULING Q2, Q-R4, DIRECTION Q5) and `R1Q<n>` names plan 034's.

**Why the feature lives in openxFactory.** The governing change lives here, as
it did for plan 034. openDox-spec cannot govern this work yet: requirement 8's
interim arrangement still applies, because openDox-spec has promoted none of
the 71 requirements the carve assigned it (#1144 Group 8, outside both
releases). The IMPLEMENTATION lands by each repository's own pull request:

- openDox-code, the bulk: Groups 6, 12, 14 and 15;
- openXdox-code, where 12.5 proves the governed flow unchanged, and whose pin
  on openDox advances (9.5);
- the openDox root, for its `code` pin (9.5) and its README;
- the openXdox root, for its `code` pin (9.5);
- openxFactory, for its two pin pairs (9.5) and any host wiring within 11.1's
  declared surfaces.

Whether openDox-spec joins them, as it did in release 1 through T053, is
R2Q22.

## Clarifications

### Session 2026-10-05 (round 1): OPEN

Twenty-four questions in [`clarify-questions.md`](./clarify-questions.md)
await Brett Heap. They come from two readings:

- this feature's reading of #1144's 37 release-2 boxes and its four rulings,
  against the live trees;
- three read-only inventories by lane openXfactory-3, delegated by this lane
  (#656 `6001723339`, claimed on `6001723764`): R2-INV-12 for Group 12, and
  R2-INV-HEALTH parts A and B for Groups 6, 14 and 15.

Every tree was measured on 2026-10-05 at `main`: openDox-code `a9ac96f9`,
openXdox-code `56e1c238`, the openDox root `d77f8cbf` and openxFactory
`0f2a87f6`.

The three inventories raised 61 candidates, and this feature's own reading
raised seven more. Each went to round 1, or to the file's "Deferred to the
plan, with proposed defaults" section, or was merged into another. The file's
last table maps every one, and nothing was dropped.

Six of round 1's questions are CONTRADICTIONS, not gaps. Two texts cannot both
hold, or a falsifier cannot pass against the code release 1 built:

- **R2Q1.** The release map says phase 4 delivers submission and landing behind
  "one interface for both". 12.1 and 12.6a require two new protocols, separate
  from each other and from the unchanged `PullRequestPort`.
- **R2Q2.** 12.4 both keeps the `PullRequestPort` bindings serving `gate
  open-pr` and says it "repoints its UNSET DEFAULT". A protected openXdox-code
  suite pins today's default, `GhPullRequests`.
- **R2Q6.** 12.6a lands by a `--no-ff` merge commit. Release 1's served-checkout
  rule (feature 007, FR-004 and SC-002) keeps `merge` and `update-ref` off the
  served checkout and pins `HEAD unchanged`.
- **R2Q8.** 12.5's falsifier runs sixteen governed suites. Fifteen of them sit
  in openXdox-code's declared exclusion (`doc_health`), and composed with
  openxFactory's scripts the sixteen read 668 passed and 174 red.
- **R2Q9.** F6.1 runs a bare process that batch G says must refuse. F14.1 and
  F15.1 reach a bundled store that R1Q16 gives only to a running document
  server. Four more of part B's points (OQ-H15-22) change Group 15's text, and
  the new verbs' shapes need `--local`. All seven are put as one set of
  amendments.
- **R2Q10.** F14.1 and F15.1 select findings by literal names, while
  requirement 15 needs an exception to cite one finding stably across resets.

Each answer is encoded here in the same commit that records it. An answer that
changes a falsifier or a task line of #1144 lands there as a bookkeeping
amendment on Brett's word, in plan 034's T007 form. An answer that would change
a requirement's text or a scenario is put to Brett as a ruling first and is not
applied here. Until the answers are in, every part of this file marked
`[NEEDS CLARIFICATION: R2Qn]` is unplanned in the part it names.

## User Scenarios & Testing *(mandatory)*

The falsifiers are #1144's own, cited by the label plan 034 defines:
`F<group>.<n>` is the n-th FALSIFIED BY box of that group in document order.
In Group 12, F12.1 is 12.5's governed-flow proof and F12.2 is the submission and
landing acceptance.

### User Story 1 — Submit work from a plain repository (Priority: P1) · phase 4

A student works in openDox on a plain local git repository, the install RULING
C3 describes, on a machine with no `gh`. They submit a branch through openDox's
OWN `submit` verb, or its own route. Where a remote is attached, the branch is
pushed there, and openDox reports where the work went, with any credential in
the remote's URL redacted. Where none is attached, openDox says plainly that
there is nowhere to submit. A governed host that needs its own platform flow
contributes its implementation through the same binding.

**Why this priority**: it is requirement 11's first gap. Today the only
implementation is `GhPullRequests`, which shells out to `gh` against
`github.com`, and the only act that submits is openXdox's `gate open-pr`. So a
standalone openDox cannot submit at all, `gh` or no `gh` (#1144 12.4a).

**Independent Test**: F12.2's submission half exits 0 in an openDox-code
checkout alone, with `gh` absent. That is the `submit` verb, the CLI binding
asserted neutral, the two `tests/test_submission_default.py` nodes, the five
`tests/test_submit_route.py` nodes and the no-remote refusal.

**Acceptance Scenarios**:

1. **Given** a plain git repository with a remote attached and a branch, and no
   `gh`, **When** `opendox submit --repo-root <repo> --branch <branch>` runs,
   **Then** the branch arrives at the remote, and the verb reports the remote,
   the ref and the URL (requirement 11, third scenario; 12.1a, 12.2, 12.4a).
   [NEEDS CLARIFICATION: R2Q5 — which branches a standalone install may submit]
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

---

### User Story 2 — Land one's own work, by an explicit human act (Priority: P1) · phase 4

A standalone owner lands a branch into their own default branch. Their install
is the explicit local one, and their default branch carries the committed
standalone declaration. They confirm the landing by typing the branch's name at
the controlling terminal, or through the view's confirm control. openDox lands
it as a `--no-ff` merge commit, which `git revert -m 1` undoes. A conflict is
shown with its paths, and the default branch does not move. In a governed
repository, or where governance cannot be established, no lander is bound at
all.

**Why this priority**: *"merge yes"* (`5784155201`). Forbidding a standalone
owner to merge their own repository protects nobody from anybody. The three
guardrails carry the purpose the old absence served: no tool merging behind its
governance's back (`design.md` § D9).

**Independent Test**: F12.2's thirteen named
`tests/test_landing_guardrails.py` nodes exit 0 in an openDox-code checkout
alone [NEEDS CLARIFICATION: R2Q6 — where the merge is made, given release 1's
served-checkout rule].

**Acceptance Scenarios**:

1. **Given** a standalone repository and a local install, **When** `land` runs
   with a confirmation minted at the controlling terminal for that branch and
   its head, **Then** the default branch gains a merge commit, `Landed` returns
   its sha, and `git revert -m 1 <sha>` restores the tree (requirement 11, sixth
   and ninth scenarios; 12.6a).
2. **Given** a confirmation made any way that is not a human act — a flag, a
   configuration key, a stdin that is not a terminal, a token built directly,
   one minted for another branch or head, or one presented twice — **When**
   `land` runs, **Then** it refuses (requirement 11, seventh scenario; 12.6a).
3. **Given** a branch that conflicts with the default branch, **When** `land`
   runs, **Then** it raises `MergeConflict` naming the conflicting paths, and the
   default branch is where it was (requirement 11, eighth scenario).
4. **Given** a registered host that declares an instrument, or a committed
   declaration that says `governed`, **When** a landing is requested, **Then** no
   lander is bound, and the landing is routed to that governance's own
   instrument (requirement 11, fifth scenario; 12.6a)
   [NEEDS CLARIFICATION: R2Q4 — what the instrument is, and what routing does].
5. **Given** no declaration on the default branch, a host profile that fails to
   load, a declaration that disagrees with the install mode, or a branch that
   ADDS a standalone declaration, **When** a landing is requested, **Then**
   governance is `unknown`, no lander is bound, and `land` refuses, naming what
   is missing (12.6a) [NEEDS CLARIFICATION: R2Q7 — which branch is the default
   branch].
6. **Given** any configuration key at all, **When** the configuration surface is
   walked, **Then** none switches a guardrail off (requirement 11, seventh
   scenario: *"a guardrail and not a setting"*; 12.6).

---

### User Story 3 — The governed host is unchanged (Priority: P1) · every phase

openxFactory's GitHub pull-request flow, through openXdox's `gate open-pr`,
behaves exactly as it does today with the host's implementation registered.
openxFactory keeps its corpus, its 23 check families, its adapter column, its
intent-plane schemas and its integration tests. Every realization landing of
release 2 carries the arc's trailer, and openxFactory's arc edits stay on the
guard's declared surfaces.

**Why this priority**: requirement 1 is the invariant every other requirement
is judged against, and 12.5 is the box that proves submission is a
generalization rather than a replacement. A release that breaks its governed
host is a regression, not a release.

**Independent Test**: F12.1, run as R2Q8 rules [NEEDS CLARIFICATION: R2Q8].
An interim F11.1 run after each phase's openxFactory landings.
openxFactory's required checks, green at every pin advance.

**Acceptance Scenarios**:

1. **Given** openXdox-code with the realized openDox installed and
   `FakePullRequests` injected, **When** every openXdox-code suite that drives
   `open-pr` or injects `FakePullRequests` runs (the set is computed, not typed:
   16 at `ab04453d`, and 16 again at `56e1c238`), **Then** each passes, and no
   arc landing edited one except through the reviewed allow-list (requirement
   11, tenth scenario; 12.5; F12.1 as T007 batches C and I amend it, R1Q7 (a),
   R1Q26 (a)).
2. **Given** every arc landing on openxFactory `main` since `94b6f7f1`, **When**
   F11.1 runs, **Then** every path touched is one of its declared surfaces, or a
   change to the carve manifest's `edits[].note` values alone, and nothing is
   deleted (requirement 1; 11.0, 11.1; R1Q2 (a), R1Q20 (a), R1Q22 (a); the
   `ADMITTED_ARC_EDITS` list RULED in `5890601202`, which a later phase extends
   only by a further ruling).
3. **Given** openxFactory's check families, **When** release 2 lands, **Then**
   each is where it was. No family moves into openDox, and the openXdox
   governance pack is follow-on F1 (requirement 1, first scenario; 6.2;
   `design.md` § D12).
4. **Given** the governed hosts' command trees and help goldens, **When**
   release 2 lands, **Then** they move only as R2Q3 rules
   [NEEDS CLARIFICATION: R2Q3].

---

### User Story 4 — See the health of one's own documents (Priority: P2) · phase 5

A user runs openDox's health check over their own documents, from the Health
view or from the command line. It reads documents AS documents: broken internal
links, documents nothing links to, near-duplicates, missing neutral front
matter, a declared stage that disagrees with where the document sits among the
six ruled words, and stale or empty stubs. Its results live in the product's
disposable store. New findings come first, persistent ones stay quiet, and an
uncited disappearance is re-raised.

**Why this priority**: *"a document product that cannot report on its own
documents has not shipped the thing it is named for"* (requirement 6, second
scenario). Today the scoped action answers `not-available` in every
openDox-only process (measured under Assumptions).

**Independent Test**: F6.1, and F14.1's `health run` and `health list` lines,
each as R2Q9 rules [NEEDS CLARIFICATION: R2Q9].

**Acceptance Scenarios**:

1. **Given** an openDox-code checkout alone, **When** the scoped health action
   runs over `README.md`, **Then** it returns `completed`, with a findings list
   and a reference (requirement 6, second scenario; 6.2; F6.1)
   [NEEDS CLARIFICATION: R2Q9, item 1].
2. **Given** a store, **When** results are computed, **Then** they live in the
   store, in a table that an ADDITIVE `0003_` migration brought, and the change
   has declared whether that table joins RULING Q1's closed list or is
   install-owned beside it (requirement 6, fourth and fifth scenarios; 14.1,
   14.2) [NEEDS CLARIFICATION: R2Q13].
3. **Given** results, **When** anything would commit them into the corpus they
   describe, **Then** the write is refused (requirement 6, third scenario;
   14.3).
4. **Given** the store dropped and rebuilt, **When** the check runs again,
   **Then** the results are recomputed and no document is lost (requirement 6,
   fourth scenario; 14.3) [NEEDS CLARIFICATION: R2Q12 — what the baseline is
   anchored to].
5. **Given** no model configured, **When** the check runs, **Then** no
   model-assisted check runs, and every other check does (requirement 6; 14.4).
6. **Given** a family that reads the publisher's `Status:` taxonomy or its
   change/spec/delta nouns, **When** release 2 lands, **Then** that family stays
   with its corpus, and openDox's check reads its own declaration (requirement 6,
   sixth scenario).

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

**Independent Test**: F14.1 over 14.9's `health-corpus` fixture
[NEEDS CLARIFICATION: R2Q9, R2Q10].

**Acceptance Scenarios**:

1. **Given** the fixture in a fresh repository, **When** `health list --json`
   runs, **Then** each planted finding carries its class: `broken-link`,
   `derivable-front-matter` and `stage-location-mismatch` are `auto-fix`,
   `near-duplicate` is `assisted`, and `human-only-finding` is `human-only`
   (requirement 14, second to fourth scenarios; 14.6, 14.9)
   [NEEDS CLARIFICATION: R2Q11 — what "location" means].
2. **Given** each `auto-fix` finding and the `assisted` one, **When** `health fix`
   runs on it, **Then** a branch `health-fix-<finding>` carries a change to that
   finding's own document, and the default branch does not move (requirement 14,
   second, third and fifth scenarios; 14.6, 14.7).
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

---

### User Story 6 — Extend the health check through pinned, sandboxed packs (Priority: P3) · phase 5

A domain adds its own checks without forking openDox. A pack is listed in the
corpus's committed `health/packs.yaml` and pinned by digest, and also by commit
when it is sourced from outside the corpus. It runs in an operating-system-
enforced sandbox, which shows it only a read-only, isolated copy of the corpus,
with no network, no inherited environment and no inherited descriptors. It
returns findings in the neutral shape, and optionally patches. The engine
stamps each finding with the pack's id and version. It validates every patch
before any branch exists. A pack that crashes, hangs, writes, returns garbage,
declares no version or tries to escape is reported as a finding against that
pack, and the other packs still run. No pack can redefine the resolution
classes, the baseline or who may land work.

**Why this priority**: the layering depends on it. openXdox's governance pack
(F1) and each DomainxFactory's own pack (F2) need the interface. A standalone
user's own documents do not, which is why it comes after User Stories 4 and 5.

**Independent Test**: F15.1 over 15.6a's `pack-corpus`, which uses 14.5's verbs
and so closes after them. It runs on a host where the reference sandbox works
(see Risks) [NEEDS CLARIFICATION: R2Q9, R2Q16, R2Q17].

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

---

### Edge Cases

- A branch adds `.opendox/governance.yaml` with `governance: standalone` to a
  repository whose default branch has none. Governance is `unknown` and the
  landing is refused. A branch never decides its own landing (12.6a).
- A registered governing host and a committed standalone declaration are both
  present. The host wins (12.6a).
- A standalone owner's first landing, before any declaration exists. It is
  refused as `unknown`. Which branch is the default, and how the first
  declaration reaches it, is R2Q7.
- A remote URL carries a credential. It is redacted from `Submission.url`, from
  the printed report and from every refusal (12.1a). Whether such a remote is
  pushed at all is a plan default (OQ-12-11: refused, as `attach_remote` refuses
  one).
- A submit request reaches the hosted multi-user plane. It is refused before
  anything else, because that plane carries no `session` capability, and a push
  spends a personal git credential a hosted plane must never hold (12.4a).
- A browser tab kept an earlier serve's console token. The next serve refuses
  it until the page is opened again through the new private copy, an accepted
  limit (12.4a, T007 batch N). A persistent browser history can keep the
  fragment, also accepted (batch P, B7).
- A finding names no document. It carries no patch (requirement 16; 15.2a).
- A corpus-relative pack entry carries a `commit`, or an entry claims the id
  `opendox`. Each is refused (15.1a, 15.7).
- The platform offers no kernel-enforced sandbox. Packs do not run, and `health
  run` reports that as a finding against the install (15.1b). Whether the
  product's own checks still run there is R2Q16. Today this is every target the
  estate runs (see Risks).
- The store is reset between an exception's commit and the next run. The
  exception still holds, because it was never in the store (requirement 15,
  first scenario).
- `health accept` has written an exception that is not yet committed. F14.1
  commits it before the next run. Whether an uncommitted entry already
  suppresses is not ruled, and the plan states its reading.
- A file already sits at `health/dispositions.yaml` or `health/packs.yaml` but
  is not of the product's own kind. The aggregation repository of this estate,
  for example, keeps its governance dispositions under that name. No answer
  rules this case, and the plan's proposed default is fail-closed (OQ-H-13):
  the file is refused by name and never read as exceptions or packs.
- A run meets a pack whose output cannot be parsed as the neutral shape. None of
  that output is stored, and the finding says why (15.6).
- Landing meets a conflict. The paths are shown, and the default branch does not
  move. The plan's proposed default names the remedy in the refusal and adds no
  conflict verb (OQ-038-1).
- A corpus repository that openDox's runtime created is BARE (Q-R1), so there is
  no working tree for `accept` to write into. The plan's proposed default writes
  a draft on a branch there (OQ-H-14).

## Requirements *(mandatory)*

### Functional Requirements

Each FR realizes the named #1144 requirement through the named boxes. Its
falsifier is #1144's own.

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
- **FR-003** (requirement 11; 12.4): the product's own submission binding SHALL
  name no platform. `submission_factory` (beside `pull_request_factory` in
  `serve.py`) and `_submission_port` (beside `_pull_request_port` in `cli.py`)
  SHALL default to `LocalGitSubmissions` when nothing is injected, and a
  governed host MAY contribute its own `SubmissionPort` through them. The
  submission seam SHALL stay separate from the generator seam: the same pattern,
  a different registration point.
  [NEEDS CLARIFICATION: R2Q2 — whether `pull_request_factory`'s unset default
  stays `GhPullRequests`]
- **FR-004** (requirement 11, first and second scenarios; 12.4a): openDox SHALL
  own the act of submitting: the CLI verb `submit --repo-root <repo> --branch
  <branch>` and the route `POST /actions/session/submit`, in its own surface and
  not under `gate`. Their engine SHALL take its `SubmissionPort` from FR-003's
  bindings, and it SHALL return and print the `Submission`.
  - The route SHALL refuse, in this order and before reading any body byte, a
    request off loopback, one without the `session` capability or a resolved
    human actor, and one that is not the human console. It SHALL take no
    repository from the request.
  - On a standalone plane, the console token SHALL reach the page only through
    the URL the page is opened with (12.4a as T007 batch N records
    `5963851934`, with batch P's printed hint line and accepted limits).
  - The CLI verb runs as the invoking user, in that user's checkout. F12.2 runs
    it non-interactively with no actor (plan default OQ-12-9).

  [NEEDS CLARIFICATION: R2Q1 — what "one interface for both" binds; R2Q3 —
  whether any governed host carries the verb in release 2; R2Q5 — which
  branches a standalone install may submit; R2Q9, item 7 — whether the verb
  takes `--local`]
- **FR-005** (requirement 11, tenth scenario; 12.5; F12.1): with the host's
  implementation registered, openxFactory's GitHub pull-request flow SHALL
  behave exactly as today. The computed set of openXdox-code suites that drive
  `open-pr` or inject `FakePullRequests` SHALL pass, and no arc landing SHALL
  edit them except through the reviewed allow-list (T007 batches C and I; R1Q7
  (a), R1Q26 (a)). R1Q6 (d) requires the `doc_health` direction arc to be
  DECIDED before 12.5 needs these suites (plan 034 T008).
  [NEEDS CLARIFICATION: R2Q8 — where F12.1 runs, and who repairs the 174 reds]
- **FR-006** (requirement 11, fifth to ninth scenarios; 12.6): landing
  authority SHALL follow whoever governs the repository, and openDox SHALL ASK
  the repository rather than hard-code either answer. Three guardrails SHALL
  hold in EVERY mode, and none SHALL be configurable: a merge is an explicit
  human act, a conflict is shown and never silently resolved, and a merge is a
  commit that can be reverted. Each SHALL be a test, not prose. A governed
  host's implementation SHALL still declare no merge.
- **FR-007** (requirement 11; 12.6a; F12.2): openDox SHALL declare
  `session_pr.LandingPort`, with ONE operation, `land(branch, *, confirmation)
  -> Landed`, and the governance query
  `session_pr.repository_governance(checkout_root)`, which answers
  `standalone`, `governed` or `unknown` and FAILS CLOSED.
  - `standalone` SHALL require BOTH the explicit local install
    (`OPENDOX_INSTALL_MODE=local`, 13.4) AND a committed
    `.opendox/governance.yaml` reading `governance: standalone`, read from the
    tip of the DEFAULT branch at the moment of landing. It is never read from
    the branch being landed or from the working tree.
  - A registered host profile that declares an instrument SHALL make the
    repository `governed`, whatever any file says.
  - Everything else SHALL be `unknown`, treated as governed without an
    instrument: no lander is bound, and `land` refuses, naming what is missing.
  - Under `standalone`, the neutral lander SHALL be bound through
    `landing_factory`, declared beside `pull_request_factory`. Under
    `governed`, the landing SHALL be routed to the host's own instrument.
  - `confirmation` SHALL be an opaque, single-use capability that only two
    issuers mint: the `land` verb's prompt, reading the typed branch name from
    the controlling terminal and refusing where there is none, and the view's
    confirm control, given a nonce the loopback server issued for that branch.
    Each token is bound to the branch and its head sha. A static check SHALL
    prove that no module outside those two interactive layers calls an issuer.
  - A conflict SHALL raise `MergeConflict` with the conflicting paths and leave
    the default branch where it was. A landing SHALL be a `--no-ff` merge
    commit whose sha `Landed` returns. The CLI verb is `land --repo-root <repo>
    --branch <branch>`.

  [NEEDS CLARIFICATION: R2Q3 — whether a governed host contributes `land` in
  release 2; R2Q4 — the instrument and what routing does; R2Q5 — which
  branches may be landed; R2Q6 — where the merge is made, and the remote;
  R2Q7 — which branch is the default branch]

**Phase 5 — the health engine, the fix loop, exceptions and packs (Groups 6, 14 and 15; requirements 6, 14, 15 and 16).**

- **FR-008** (requirement 6; 6.1, 6.1a, 6.2; F6.1): openDox SHALL carry a
  health check that it runs over ITS OWN documents from its own checkout,
  reading its own declaration, and the scoped health action SHALL give it
  something to call. No openxFactory check family SHALL move (requirement 1).
  Where a module genuinely mixes a generic traversal with corpus-specific
  classification, the generic part SHALL be relocated into a module both sides
  depend on BEFORE either side moves. The packet's measurement (6.1) found ONE
  of `scripts/doc_health/`'s 37 modules free of corpus identifiers, and
  R2-INV-HEALTH part A finds two of 38 today (`lines.py`, and `fs_probe.py`,
  added since). So the check is new neutral code, not a relocated family. The plan's proposed default
  makes it the engine's built-in families, attributed `opendox` (OQ-H-3).
  [NEEDS CLARIFICATION: R2Q9, item 1 — how F6.1 reaches it; R2Q14 — how 6.1a
  squares with 11.1's guard]
- **FR-009** (requirement 6 as amended; 14.1, 14.2, 14.3): health results SHALL
  be DERIVED DATA kept in the product's disposable store and never committed
  into the corpus they describe. Their table SHALL arrive as an ADDITIVE
  `0003_` migration, never an edit to `0001`. The change SHALL DECLARE whether
  the table joins RULING Q1's closed list or is install-owned beside it, and
  say why. Where it joins, `identity.TABLES` and the closure test's text SHALL
  move in the same change. The store SHALL hold no document and stay
  disposable, so its loss costs a recomputation.
  [NEEDS CLARIFICATION: R2Q13 — which of the two; R2Q15 — what a hosted install
  does]
- **FR-010** (requirement 6; 14.4): the neutral families SHALL be the ruled
  six: broken internal links, documents nothing links to, near-duplicates,
  missing neutral front matter from the adapter's fields, a declared stage that
  disagrees with the document's location among the six ruled words, and stale
  or empty stubs. They SHALL run on demand from the view and the CLI, and
  optionally on commit. They SHALL be BASELINE-RELATIVE: new findings get
  attention, persistent ones stay quiet, and an uncited disappearance is
  re-raised. They SHALL report where the human is already working, never by
  filing into an external tracker, and they SHALL run any model-assisted check
  only where a model is configured. openxFactory's 23 governance families SHALL
  stay with openxFactory.
  [NEEDS CLARIFICATION: R2Q11 — what "location" means; R2Q12 — the baseline, its
  citations, and pack upgrades]
- **FR-011** (requirement 14, first and seventh scenarios; 14.5): the Health
  view SHALL be served by the entry point, and every resolution action in the
  view SHALL have a CLI verb with the same action. The verbs are:

  | verb | shape |
  |---|---|
  | `health run` | `health run --repo-root <corpus> [--pack ID] [--timeout SECONDS]` |
  | `health list` | `health list --repo-root <corpus> [--json]` |
  | `health fix` | `health fix --repo-root <corpus> --finding ID [--batch]` |
  | `health accept` | `health accept --repo-root <corpus> --finding ID --reason TEXT` |

  Options SHALL follow the verb. `health list --json` SHALL emit one object per
  finding with `id`, `resolution_class`, `path`, `severity`, `evidence`,
  `pack_id` and `pack_version`. The `/capabilities` payload's health block
  SHALL list every action the view offers, so parity is a comparison, made by
  three named tests.
  [NEEDS CLARIFICATION: R2Q9, items 2 and 7 — the store the verbs reach, and
  `--local`; R2Q10 — what a finding's `id` is]
- **FR-012** (requirement 14, second to fourth scenarios; 14.6): findings SHALL
  be resolved in three declared classes, spelled `auto-fix`, `assisted` and
  `human-only` in the store, the CLI, the view and the pack contract alike.
  `auto-fix` covers the mechanical findings, written by the product. `assisted`
  covers proposals the human edits, model-written only where a model is
  configured. `human-only` shows the evidence. The applier SHALL be new work,
  since nothing in the estate applies a fix today. The classes of the families
  the ruling did not place are a plan default (OQ-H-8: `human-only`).
  [NEEDS CLARIFICATION: R2Q11 — which way the stage repair goes]
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
- **FR-015** (requirements 14 and 15; 14.9; F14.1): openDox-code SHALL ship
  `tests/fixtures/health-corpus`, a small corpus carrying ONE finding of every
  kind requirement 14 names and nothing else a neutral family would flag:
  `broken-link`, `derivable-front-matter` and `stage-location-mismatch`
  (`auto-fix`), `near-duplicate` (`assisted`), `human-only-finding`
  (`human-only`), and `accepted-finding`. F14.1 SHALL exit 0 over it.
  [NEEDS CLARIFICATION: R2Q9, item 2; R2Q10]
- **FR-016** (requirement 16; 15.1, 15.1a): openDox SHALL declare a NEUTRAL
  CHECK-PACK CONTRACT on the `corpus_adapter` protocol pattern, a
  `@runtime_checkable` protocol with a closed member set.
  - The engine SHALL load packs ONLY from the corpus's committed
    `health/packs.yaml`, whose entries carry `id`, `version`, `source` and a
    REQUIRED source-tree `digest`, as `neutral-product-pin` defines it.
  - A git-URL source SHALL carry a `commit`. A corpus-relative source SHALL NOT,
    and one that does is refused.
  - The engine SHALL verify the pin before importing any line of the pack. A
    listed pack whose source no longer matches its digest SHALL be refused as a
    finding carrying both digests.
  - There SHALL be no entry-point scanning and no import-path discovery.

  [NEEDS CLARIFICATION: R2Q18 — what a pack may depend on; R2Q21 — `stack.yaml`
  against `health/packs.yaml`; R2Q22 — whether openDox-spec owns the contract's
  schemas]
- **FR-017** (requirement 16; 15.1b): every pack SHALL run in a separate process
  inside an OPERATING-SYSTEM-ENFORCED sandbox, never by convention.
  - The engine SHALL export the corpus commit into a directory it owns, and
    mount it read-only as the pack's only view of the user's data.
  - Beside it, the pack sees only:
    - its own pinned code;
    - the interpreter paths its runtime needs, read-only;
    - a private scratch space, discarded with the sandbox;
    - the sandbox's own process and device filesystems.
  - The pack SHALL have no network, a cleared environment with an explicit
    allowlist, and no inherited descriptor. Its whole process tree SHALL end with
    the sandbox.
  - Where the platform offers no such sandbox, packs SHALL NOT run, and `health
    run` SHALL report that as a finding against the install.
  - `bwrap` is the Linux reference.

  [NEEDS CLARIFICATION: R2Q9, items 3 and 5 — F15.1's platform precondition,
  and the export's git attributes; R2Q15 — hosted pods; R2Q16 — whether the
  product's own checks run where no sandbox exists; R2Q17 — whether CI runs the
  sandbox suite; R2Q18 — the libraries a pack's runtime reads; R2Q19 — git
  history in the sandbox; R2Q20 — model access for packs]
- **FR-018** (requirement 16; 15.2, 15.2a): a pack SHALL declare its own version,
  equal to its manifest entry's, and its check families with an id, a version
  and the documents each applies to. It SHALL return findings in the neutral
  shape (severity, one of the three classes, evidence), and it MAY return
  proposed fixes as unified-diff patches only. The engine SHALL validate every
  patch BEFORE any branch exists, and refuse one that:
  - edits a path other than its own finding's document;
  - names an absolute path, or one with a `..` or `.git` component in any
    letter case;
  - targets, or lies below, a symbolic link;
  - creates, deletes, renames, copies or re-modes a file, or is binary;
  - exceeds the engine's bound, 65,536 bytes by default, which no pack can
    raise.

  Each refusal SHALL be a finding against the pack, naming the refused finding
  and the failed check, and SHALL create no branch.
- **FR-019** (requirement 16; 15.3, 15.4): a pack's labels SHALL resolve through
  the display facet and never be spelled into the neutral surface. The ENGINE
  SHALL own, identically for every pack, the view and its CLI parity,
  scheduling, the baseline, storage (results in the store, exceptions in the
  corpus) and the fix loop with its landing rule. No pack SHALL redefine the
  resolution classes, the baseline rules or who may land work.
  [NEEDS CLARIFICATION: R2Q12 — the baseline the engine owns, across a pack
  upgrade]
- **FR-020** (requirement 16; 15.5, 15.6, 15.6a): each refusal SHALL be a test,
  not prose.
  - A pack that crashes, overruns its per-pack time budget (`health run
    --timeout`, a default declared by 15.6 and enforced by the engine), or
    returns output the engine cannot parse SHALL be reported as a finding
    against that pack, and the other packs SHALL still run.
  - openDox-code SHALL ship `tests/fixtures/pack-corpus`: 14.9's corpus plus the
    eight fixture packs 15.6a names, registered by corpus-relative source,
    pinned by digest and carrying no `commit`, with a test that keeps their
    digests current.

  [NEEDS CLARIFICATION: R2Q9, items 3–6 — part B's amendments to 15.1b, 15.6a
  and F15.1; R2Q17 — whether the required check runs the refusal tests]
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
- **FR-023** (9.5): the pins that compose the legs SHALL advance by their
  owners' ordinary pin-sync acts, each in the landing that needs release 2's
  code. Each of openxFactory's two pairs SHALL move in ONE commit. A bundle cut
  or a release tag SHALL be owed only where a recorded addendum at 9.5 says so.
  [NEEDS CLARIFICATION: R2Q22 — a `dox-v1.y` bundle; R2Q23 — a PyPI release and
  its tag]
- **FR-024** (acceptance): release 2 SHALL pass its own acceptance before its
  bookkeeping ticks the release-2 boxes.
  [NEEDS CLARIFICATION: R2Q24 — whether that is an end-to-end AT-R2 or the
  packet's falsifiers alone]
- **FR-025** (process): no task SHALL start while a question in its `Blocked
  by:` line is open. Every realization PR SHALL name its task ids, the boxes it
  realizes and the falsifier it ran, with the output quoted. The plan's proposed
  default for the arc's close is that this feature performs and ticks 9.5, 11.0,
  11.1 and F11.1, and plan 034's T090–T093 close by reference (OQ-038-2).

### Key Entities

- **Submission port** (`SubmissionPort`): the neutral act of moving work out of
  the local repository. Its one operation returns a **Submission** (`remote`,
  `ref`, a redacted `url`). The neutral default is `LocalGitSubmissions`, and
  its refusal is `NoSubmissionTarget`.
- **Pull-request port** (`PullRequestPort`): the governed host's platform
  protocol, unchanged, served by `GhPullRequests` and `FakePullRequests`.
- **Landing port** (`LandingPort`): the act of landing a branch into the default
  branch. It returns **Landed** (the merge commit's sha) or raises
  **MergeConflict** (the conflicting paths).
- **Repository governance**: `standalone`, `governed` or `unknown`, answered by
  `repository_governance` and failing closed. The **governance declaration** is
  `.opendox/governance.yaml`, read from the default branch's tip.
- **Confirmation**: an opaque, single-use capability bound to a branch and its
  head sha, minted only by the `land` prompt or the view's confirm control.
- **Finding**: one health result, with `id`, `resolution_class`, `path`,
  `severity`, `evidence`, `pack_id` and `pack_version`. It is derived data, kept
  in the store. Its identity is R2Q10.
- **Resolution class**: exactly `auto-fix`, `assisted` or `human-only`.
- **Baseline**: what makes a finding new, persistent or disappeared. It is owned
  by the engine, and no pack may vary it. Its anchor is R2Q12.
- **Fix draft**: a repair written as a commit on a branch (`health-fix-<finding>`
  in F14.1). It is distinct from the runtime's `drafts` table, which RULING Q1
  keeps for unsaved document bodies.
- **Exception**: a human's decision that a finding is accepted. It is committed
  in the corpus at `health/dispositions.yaml` and never kept in the store.
- **Check pack**: arbitrary code that supplies check families. It is listed and
  pinned in the corpus's committed `health/packs.yaml`, run in a sandbox, and
  attributed by its manifest entry. The product's own checks are the pack
  `opendox`, which no manifest lists.
- **Proposed patch**: data a pack returns, validated by the engine before any
  branch exists.
- **Arc landing**: a commit on a repository's `main` first-parent line that
  carries the `Arc:` trailer. 12.5's and 11.1's guards read it.
- **Pin pair**: a gitlink plus its `contracts/*-pin.yaml`, moved in one commit.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001** (phase 4 exit): F12.2 exits 0 in an openDox-code checkout alone with
  `gh` absent. That includes its thirteen named guardrail tests, its five named
  route tests and its two named submission-default tests. F12.1 exits 0, run as
  R2Q8 rules.
- **SC-002** (phase 5 exit): F6.1, F14.1 and F15.1 exit 0, each as amended where
  a bookkeeping batch records an answer (R2Q9, R2Q10). F15.1 runs on a host
  where the reference sandbox works.
- **SC-003**: after each phase's openxFactory landings, an interim F11.1 run
  (`PACKET_MERGE=94b6f7f1`) prints `requirement 1 holds`.
- **SC-004**: at release 2's close, all 37 release-2 boxes are ticked, each with
  its evidence: Group 6's 4, Group 12's 11, Group 14's 10 and Group 15's 12.
  The every-phase boxes 9.5, 11.0, 11.1 and F11.1 are ticked at the arc's close.
- **SC-005**: openxFactory's required checks are green at every pin advance
  release 2 makes. openDox-code's required check keeps running its whole suite,
  with no declared exclusion, and release 2's named tests run in it, the sandbox
  tests as R2Q17 rules.
- **SC-006** (the user's outcomes):
  - a student on a machine without `gh` gets a branch's work to an attached
    remote with ONE command, and is told plainly when there is no remote;
  - a standalone owner lands with ONE confirmed act, which ONE
    `git revert -m 1` undoes;
  - the view offers zero resolution actions that the CLI lacks, and the CLI
    offers zero the view lacks;
  - the store holds zero findings without a pack id and a pack version;
  - a store reset loses zero exceptions.
- **SC-007**: zero landings of release 2 merge automatically. Every landing on a
  default branch traces to a human confirmation or to the governance's own
  instrument.

## Assumptions

- **Release 1 is complete.** Plan 034 reads 92 of 96 tasks. The four open ones,
  T090–T093, are the every-phase tasks for 9.5, 11.0, 11.1 and F11.1, which
  were left open for the arc's close after release 2. `opendox` 0.1.0 is on
  PyPI (T099). F9.2 stays open until the `doc_health` direction arc lands (plan
  034 T008; RULED `5859927858`). Since the archive needs both releases'
  evidence, the archive also waits on that arc.
- **The rulings stand as encoded.** `5783934499`, `5784155201`, `5784247356` and
  `5784295745` are sequenced, not reopened. Requirements 6, 11, 14, 15 and 16
  are #1144's as written. The two corrections #1144 already records stand: the
  migration is `0003_`, not `0002_`, and the closure test is scoped to the
  canonical migration (`design.md` § D10.4).
- **`0003_` is still the next number.** openDox-code `a9ac96f9` carries
  `migrations/0001_identity_and_coordination.sql` and
  `migrations/0002_migration_state.sql`, and nothing else. About twenty
  assertions move with `0003_` whichever way R2Q13 is answered (R2-INV-HEALTH
  part A § 1).
- **The seam the scoped health action calls exists, and is empty.** Release 1's
  4.3 routed `run_scoped_doc_health` through
  `opendox.workbench.register_health_check`. The scoped action no longer
  catches the `ImportError` that 6.2 describes. Measured in a bare process at
  `a9ac96f9`, `run_scoped_doc_health(".", ["README.md"])` answers
  `not-available`, *"no health check is registered at openDox's health-check
  seam"*, and `DEFAULT_SCOPED_FAMILIES` is `("status-validity",
  "tag-hygiene")` (R2Q9, item 1).
- **The bundled store's ownership is release 1's.** At `a9ac96f9`, a local-mode
  `runtime status`, `migrate` or `reset` refuses unless a live bundled server of
  this data directory is running: *"A local install's server is started by
  `opendox generate-and-open --local`, which owns it"*
  (`runtime/bundle.py`, `refusal_before_connecting`; R2Q9, item 2).
- **12.5's governed set at `56e1c238`.** `git grep -l -e open-pr -e open_pr -e
  FakePullRequests -- 'tests/test_*.py'` selects 16 files. Fifteen are entries
  of openXdox-code's `tests/declared_exclusion.yaml`, each with the reason
  `doc_health`. `tests/test_gate_loop_views.py` is the one that runs alone.
  Composed with openxFactory's `scripts/`, the 16 read 668 passed and 174 red,
  the same 174 that plan 034's T086 recorded (R2-INV-12 M3; R2Q8).
- **Release 1's served checkout does not move.** Feature 007's FR-004 and SC-002
  leave `merge`, `update-ref` and `revert` out of the served checkout's
  allowlist, and refuse `fetch` and `pull` everywhere (`session_git.py`;
  `merge` and `update-ref` pinned by `tests/test_session_git.py:563-570`;
  R2Q6).
- **A standalone install has no session opener of its own.** Every
  session-opening verb is a gate verb, and release 1 RULED Save refused by name
  on standalone (`5971834845`; R2Q5).
- **Release 2's verbs are new surface.** At `a9ac96f9`, `opendox.cli` declares
  no `submit`, `land` or `health` verb. R1Q4 (a) has openDox's default profile
  contribute them, and `default_profile.py` records the same (R2Q3).
- **The line numbers #1144's boxes cite have moved.** This is non-normative,
  and the plan cites live lines. At `a9ac96f9`:
  - `cli.py:800`'s `_pull_request_port` and `:812-814`'s construction are at
    `:1292-1306`;
  - `serve.py:766`'s `pull_request_factory` is at `:1062`, and its unset
    default at `:1227-1230`.

  R2-INV-12's line-drift table has the rest.
- **Platforms.** Release 2 targets the platforms release 1 targets (plan 034,
  round 13 and ruling B2), and 15.1b already decides that packs do not run where
  no kernel-enforced sandbox exists. The Risks below are why that clause is now
  the common case.
- **"Near-duplicates via the existing engine"** (`5784155201`) is read, as a
  plan default, as openDox's own similarity backend, `doxbench_knowledge.py`'s
  hashed n-gram projection (OQ-H-21).
- **Out of scope:** release 1's groups, and Group 8 (openDox-spec's
  re-promotion). The follow-ons are out of scope too:
  - F1, the openXdox governance pack, which is what gives openxFactory's 23
    families a pack;
  - F2, each domain's own pack;
  - F3, the wording overlays;
  - F4, the direct-arrow revisit.
- **Lane discipline:**
  - Rule 6 windows cover any PR that touches `openspec/changes/`. This
    feature's spec PR touches none.
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
  is made capable. Developers cannot run the sandbox suite in the estate's own
  containers. CI must change to run it (R2Q17), and `ubuntu-latest` moves to
  26.04 between 2026-10-19 and 2026-11-19. Whether the product's own checks
  depend on the sandbox decides whether any target has a health check at all
  (R2Q16).
- **12.5 cannot pass in any environment measured** (R2-INV-12). Its repair is a
  slice of its own, whose size R2Q8 decides.
- **Release 1's own invariants stand in the way of three boxes.** Feature 007's
  served checkout blocks 12.6a's merge (R2Q6). Batch G's empty seam blocks F6.1,
  and R1Q16's bundle ownership blocks F14.1 and F15.1 (R2Q9). None is
  resolved here by assumption.
