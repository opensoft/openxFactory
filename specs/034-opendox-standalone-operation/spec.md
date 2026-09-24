# Feature Specification: openDox standalone operation (release 1)

**Feature Branch**: `034-opendox-standalone-operation`
**Created**: 2026-09-24
**Status**: Draft (planning). 11 of the 23 clarify questions are answered,
including every question phase 1 needed. 12 are open, and phases 2–3 are
PROVISIONAL until they are answered.
**Realizes**: RELEASE 1, "standalone operation", phases 1–3, of the
openxFactory OpenSpec change `add-neutral-product-standalone-operability`
(#1144, landed `94b6f7f1`). The phases follow that change's RULED release map
(`#656` `5799646419`, as corrected by `5800995035`).
**Lane**: `openxfactory-4`
**Input**: the lane's planning brief of 2026-09-24. It asks for the Speckit
planning artifacts for release 1, with every task mapped to a #1144 box, a
repository and a falsifier, and with every ambiguity put as a question. No
code is written by this feature's planning.

**AUTHORITY.** Brett Heap ratified #1144 on `#656`, comment `5815412869`
(2026-09-24T13:51:09Z), verbatim: *"ratify #1144, land the follow-ons, (a) on
C1–C5"*. That comment records *"The ratify word authorizes realization of
release 1 (phases 1–3). The realization does not happen by the word itself."*
The ratification record, box 1.8, landed as #1151 → `cd494e4c`
(2026-09-24T14:54:27Z), under its own Rule 6 window, and ticked 1.8 and 3.0.
Brett Heap answered the eleven phase-1 clarify questions on `#656`, comment
`5817152735` (2026-09-24T15:31:46Z), verbatim: *"(a) on all eleven, (d) on
R1Q6"*.

**THE RATIFIED PACKET IS THE AUTHORITY, NOT THIS FILE.** Every requirement
below realizes one of #1144's requirements and names it. Nothing here restates,
narrows or widens the packet. Where this file appears to do so, that is a
defect in this file, and the packet wins. Where the packet contradicts itself
or the live code, the contradiction is put to Brett as a question
([`clarify-questions.md`](./clarify-questions.md), `R1Q1`–`R1Q23`). It is never
settled here by assumption.

**Why the feature lives in openxFactory.** The governing change lives here.
The global protocol hands a change to a Speckit feature under `specs/NNN-*` in
the change's own repository (lifecycle step 3). openDox-spec cannot govern this
work yet: requirement 8's interim arrangement applies, because openDox-spec has
promoted none of the 71 requirements the carve assigned it (#1144 Group 8). The
IMPLEMENTATION lands in five repositories, each by that repository's own pull
request: openDox-code, openXdox-code, openDox, openXdox and openxFactory. A
sixth, openDox-spec, joins only if T053 applies.

## Clarifications

### Session 2026-09-24

Round 1 raised 22 questions in [`clarify-questions.md`](./clarify-questions.md),
and one answer raised a 23rd. They are named `R1Q<n>`, because a bare `Q<n>`
already names one of #1144's own rulings (RULING Q1, RULING Q2, Q-R4,
DIRECTION Q5).

Brett Heap answered eleven of them. The ruling was given on `#656`, comment
`5817152735`, 2026-09-24T15:31:46Z, verbatim: *"(a) on all eleven, (d) on
R1Q6"*.

- Q: R1Q22. Does the carve's declared-edit discipline govern the arc's edits
  to carved files? → A: (a), no. The manifest records the carve as it
  arrived, post-arrival development is ordinary work, and 11.1's notes record
  only each closed reach.
- Q: R1Q1. How is the lanes mixin dropped, when a `RouteBinding` can name only
  a method its handler class already has? → A: (a), a handler-contribution
  facet. A profile or extension declares the mixin classes holding the methods
  its bindings name. `build_server` composes them into
  `BoundDashboardHandler`'s bases, and `resolve_handlers` is unchanged.
- Q: R1Q2. May an arc landing edit openxFactory's tests that pin openDox's
  internals, which 11.1's guard forbids? → A: (a). 11.1's declared surfaces are
  widened to NAMED openxFactory composition tests, which may be edited and are
  never removed. The first is
  `tests/ideation-dashboard/test_extension_point_parity.py`.
- Q: R1Q3. Is the default profile an entry-point registration or a fallback
  inside `current()`? → A: (a). Both defaults, the profile and the adapter,
  are registrations an entry point makes, and F3.1 line 2 is amended to ask
  after `build_parser()`. `ProfileNotRegistered` stays for library callers.
  (i) 3.2's "ambiguous registration" wording is corrected to the case
  `profile_proxy.py` was written for, NOTHING REGISTERED. (ii) A host
  registration replaces the default until a parser or server is built from
  it, and is refused after that. That conflicts with the TEXT of requirement
  3's fourth scenario, so it is RULING NEEDED RN-1 (plan.md § "Ruling
  needed"). RN-1 holds phase 1's close (T049), but not T016's landing.
- Q: R1Q4. What does the default profile contribute, given that an empty
  default stays refused? → A: (a). openDox's own verbs and routes: the runtime
  verbs now, and release 2's `submit`, `land` and `health` later. Its
  `DISPLAY` is `NEUTRAL_DISPLAY`. A governed host's own start asserts that its
  profile is the registered one.
- Q: R1Q5. Where do the runtime verbs register without breaking the 31-entry
  golden? → A: (a). Through the default profile's `SUBCOMMAND_EXTENSIONS`
  (`RuntimeSubcommand`), and `opendox-runtime` stays as an alias. A host that
  registers its own profile keeps its 31-entry tree.
- Q: R1Q6. How does openXdox-code run its whole suite green alone while its
  modules import openxFactory's `doc_health`? → A: (d), for release 1.
  - The `doc_health`-dependent files are a DECLARED exclusion, with their
    count and reason (requirement 9, first scenario), and F9.1 is amended for
    openXdox-code.
  - The direction question becomes its own arc (T008), decided before 12.5
    needs the 16 governed suites. Requirement 9 therefore stays an open
    extraction for openXdox-code until that arc lands.
  - This answer raises R1Q23 for phase 2.
- Q: R1Q7. How do the protected suites of 5.4a and 12.5 survive release 1?
  They already fail, and one introspects a method release 1 moves. → A: (a). A
  reviewed allow-list admits edits that only RESPELL a reference to a moved
  seam, with no assertion weakened, and each edit is recorded.
- Q: R1Q8. Does openDox-code's "whole suite" include `tests_runtime/`? → A:
  (a), yes. `testpaths` widens to both roots, and the required job gets a
  PostgreSQL service. F9.1 is unchanged.
- Q: R1Q9. Does `session_documents` refuse until Group 6? → A: (a), no. It
  resolves through the registered adapter's `list_documents` in phase 1, and
  the hosted membership rule is unchanged.
- Q: R1Q20. Do the arc's bookkeeping commits carry the `Arc:` trailer? → A:
  (a), no. Only realization landings carry it.

Where an answer amends a falsifier or a task line of #1144, T007 records the
amendment there as bookkeeping, and the realization carries it out
([`tasks.md`](./tasks.md) § "Ruled amendments"). The planning PR (#1155)
edits no file of #1144.

**Still OPEN** (phases 2–3, and process): R1Q10–R1Q19, R1Q21, and R1Q23. Every
task one of them blocks carries `Blocked by: R1Qn` in [`tasks.md`](./tasks.md).
None of those tasks may start until its phase's round task has encoded the
answer here: T009 for phase 2, T069 for phase 3.

One box needs no question. **3.0** ("RATIFICATION READ FIRST") is discharged by
the ratification word itself. `5815412869` ratified the change and struck no
requirement, and design.md § D5 names ratification as *"the act that settles
it"*. The ratification record (#1151, `review/ratification-2026-09-24.md` § 2)
ticked it.

## User Scenarios & Testing *(mandatory)*

### User Story 1 — It runs (Priority: P1) · phase 1

A developer who has only openDox-code checks it out and installs it with its
declared extras. Every module imports. The command-line parser builds on
openDox's own default profile. The entry point registers openDox's own default
corpus adapter. Each leg's suite runs green in its own checkout. openDox-code's
runs whole. openXdox-code's runs whole less a declared `doc_health` exclusion,
which is reported as an open extraction (R1Q6 (d)). The `opendox` console
script exists.

**Why this priority**: nothing else in the release can be exercised until the
product imports and its suite runs. Today openDox-code's suite gives 0 passed
and 1,305 errors (research R2).

**Independent Test**: at the phase-1 tip, F2.1, F3.1 (line 2 as amended, R1Q3
(a)), F9.1 (in both legs; openXdox-code's as amended, R1Q6 (d)), F9.2 and
`opendox --help` all pass. So do 4.3's eight
reaches into openxFactory, under F4.1's scan restricted to the publisher's
packages.

**Acceptance Scenarios**:

1. **Given** a fresh venv holding only openDox-code with `.[runtime,test]`,
   **When** every module of `opendox` is imported, **Then** each one imports,
   and 2.4's test names the first module that does not (requirement 2).
2. **Given** no host has registered a profile, **When** an entry point builds
   the parser, **Then** it builds on openDox's own default profile, which the
   entry point registered. A profile a host registers before anything is built
   replaces the default (requirement 3; R1Q3 (a), R1Q4 (a); RN-1).
3. **Given** nothing is registered, **When** a verb needs the home corpus,
   **Then** it refuses with `CorpusRefused` of kind `ADAPTER_NOT_REGISTERED`,
   naming the seam and the remedy. **Given** an entry point was built, **Then**
   the home corpus is openDox's `LocalGitCorpus` (requirement 5).
4. **Given** each leg's own checkout with no sibling present, **When**
   `python -m pytest -q` runs, **Then** it is green. `validate.yml` names no
   file list and no `--noconftest` (requirement 9).
   - openDox-code's whole suite includes `tests_runtime/`, run against the
     required job's database (R1Q8 (a)).
   - openXdox-code's is the whole suite less its declared `doc_health`
     exclusion, which every run reports with its count and its reason (R1Q6
     (d)).
5. **Given** openXdox-code with openDox at its pin, **When** the declared
   integration suite runs, **Then** it passes, including the 31-entry assembled
   `--help` tree (requirement 9, third scenario).

**Phase-1 limit, measured and not chosen**: in phase 1 a standalone
`build_server` still needs an injected snapshot source. With nothing else
installed it is refused at `serve.py:1647` (research R7). The server starting
on its own is phase 2's work (US2).

---

### User Story 2 — It is useful alone (Priority: P2) · phase 2

openDox, with no consumer installed, is pointed at a plain git repository. It
generates its OWN neutral snapshot over its corpus adapter, which it renders in
the six ruled words: sources, groups, candidates, selections, submissions,
completed. It validates that snapshot with its own validator, reading schemas
that are on disk in the installed package. With openXdox installed, the
governed corpus is projected exactly as it is today.

**Why this priority**: a product that can only serve snapshots it cannot
generate is not standalone (requirement 4, first scenario).

**Independent Test**: at the phase-2 tip, F5.3, F7.2, F5.1 (5.3a re-run),
F5.2 (5.4a) and F7.1 (7.3) all pass. F5.2 is run as T007's batch C amends it
and as R1Q23 decides.

**Acceptance Scenarios**:

1. **Given** the 5.0 fixture in a fresh repository and neither `openxdox` nor
   `doc_health` importable, **When** `python -m opendox.cli generate` runs,
   **Then** a non-empty snapshot is written. No string value in it carries a
   declared governance word (requirement 4, second scenario; R1Q11, R1Q13).
2. **Given** the 7.0 malformed fixture, **When** `generate --strict` runs,
   **Then** it exits non-zero, naming the fixture's `EXPECTED_RULE`, and it
   does not fail on an unresolvable path (requirement 7; R1Q12).
3. **Given** openXdox installed over the realized openDox, **When** the six
   generator suites run, **Then** they pass, and no arc landing edited them
   except through R1Q7 (a)'s reviewed allow-list (requirement 4, third
   scenario; R1Q23 decides where the four `doc_health` suites run).
4. **Given** openXdox installed in a fresh venv, **When** its validator lookup
   starts inside a planted pre-shed tree, **Then** it resolves the installed
   distribution's own validator (7.3; R1Q14).

---

### User Story 3 — It installs (Priority: P3) · phase 3

On a clean machine, a single user installs openDox and runs the one command
openDox's README documents. The product starts with its own bundled datastore,
in an explicitly selected local identity mode, bound to loopback, and serves
its browser surface. Chat can be pointed at any OpenAI-compatible endpoint by a
URL, a model name and a credential reference, and never by a raw key. With no
model configured, the chat pane shows "no model configured" and explains how to
configure one, before any turn is attempted, and everything else works.

**Why this priority**: this is the student promise itself (requirements 10, 12,
13 and 17). It depends on US1 and US2.

**Independent Test**: at the phase-3 tip, F13.1 and F10.1 (both as amended per
R1Q15 and R1Q16), F16.1 and F4.1 (the whole package: no deferred reach, and
`consumer_reach.py` gone) pass. So does **AT-R1**, defined under Success
Criteria.

**Acceptance Scenarios**:

1. **Given** no database, no broker and a fresh `OPENDOX_STATE_DIR`, **When**
   the documented command runs in local mode, **Then** the served process
   reports `install.mode == local`, a bundled datastore under the state
   directory with no TCP listener, and migrations applied (requirements 12 and
   13).
2. **Given** a hosted install, or an unset mode, with no issuer, **When** the
   same command runs, **Then** it refuses, naming `OPENDOX_OIDC_ISSUER`, and
   never degrades to local (requirement 13; R1Q15).
3. **Given** a stand-in OpenAI-compatible server on loopback, **When** a chat
   turn is sent, **Then** it reaches that server in the chat-completions
   grammar and names the configured model (requirement 17).
4. **Given** a binding whose endpoint URL or extra field carries a key,
   **When** it is declared, **Then** it is refused, and nothing is stored
   (requirement 17; R1Q17, R1Q18).
5. **Given** no model configured, **When** the chat pane opens, **Then** it
   shows "no model configured" and how to configure one, before any turn. A
   turn is refused `model_capability_unavailable` before any process starts or
   any endpoint is contacted, and every other surface answers as it does with a
   model configured (requirement 17; R1Q10).

---

### User Story 4 — The governed host is unchanged (Priority: P1) · every phase

openxFactory keeps its corpus, its check families, its lanes, its intent-plane
schemas and its governed flow. It keeps them working by registering its
profile, home corpus, lanes column and other contributions through openDox's
declared seams, at pins that advance in lockstep. The guard in 11.1 holds.

**Why this priority**: requirement 1 is the invariant every other requirement
is judged against. A standalone openDox that breaks its governed host is a
regression, not a release.

**Independent Test**: openxFactory's required checks (among them
`pytest-suite`) stay green at every pin advance. An interim F11.1 run after
each phase's openxFactory landings exits 0: T018, T065 and T098, each by
T093's procedure. F5.2 and 9.3's integration suite pass.

**Acceptance Scenarios**:

1. **Given** openxFactory at a pin carrying the removal of 2.1, **When** its
   server is built, **Then** its five lane routes are served through the seam
   and the handler-contribution facet (R1Q1 (a), R1Q2 (a)).
2. **Given** every arc landing on openxFactory `main` since `94b6f7f1`, **When**
   F11.1 runs, **Then** each path touched is one of 11.1's surfaces, as
   widened to named composition tests by R1Q2 (a). The manifest differs only
   by extended notes (requirement 1; R1Q20 (a), R1Q22 (a)).

---

### Edge Cases

- A host registers AFTER an entry point registered the default. It replaces
  the default until a parser or server is built from it, and is refused
  `AlreadyRegistered` after that (R1Q3 (ii); RN-1).
- A governed host FORGETS to register, and gets a working-looking parser
  without its gate verbs. Its own start asserts its registration, so it
  refuses to start (R1Q4 (a)).
- A test file in openXdox-code needs `doc_health`. It is listed in the declared
  exclusion with its reason, and it is never silently skipped (R1Q6 (d)).
- The install mode is unset (R1Q15), or a local install is asked to bind
  beyond loopback, which is refused with no opt-in (13.4).
- A raw key appears inside an endpoint URL, not in a field (16.3).
- The plain repository yields no grouping, candidate or selection tile, so the
  chat pane cannot be opened at all (R1Q13).
- The served model-catalog route validates against openxFactory's
  `doxbench_contracts` until T085 lands, so it fails closed without them
  today (research R15). T027's seam then makes it fail closed naming itself
  when nothing is registered. From T085 on, a standalone install validates
  with openDox's own packaged validators, and the route answers (R1Q10,
  R1Q12).
- Lane 4's in-flight C3 edits 7.3's file and moves openxFactory's openXdox pin,
  and C4 writes the openXdox pin runbook. Both must be sequenced around, never
  duplicated (plan.md § "In-flight overlaps").

## Requirements *(mandatory)*

### Functional Requirements

Each FR realizes the named #1144 requirement through the named boxes. Its
falsifier is #1144's own, cited by the label `tasks.md` defines
(`F<group>.<n>`, the n-th FALSIFIED BY box of that group in document order).

- **FR-001** (requirement 2; boxes 2.1–2.6, 9.2a; F2.1): every module of
  openDox SHALL import with no consumer, publisher or host installed. The five
  lane routes SHALL be contributed through a declared seam, with their methods
  through the handler-contribution facet (R1Q1 (a)). A test in
  openDox's own suite SHALL import every module. The openDox → openxFactory
  direction SHALL be watched by a required check.
- **FR-002** (requirement 3; 3.0–3.3; F3.1): openDox SHALL ship a default
  profile for its own domain that carries no publisher vocabulary. Entry points
  SHALL build on it when no host has registered, and a registered profile
  SHALL replace it. Both defaults are entry-point registrations (R1Q3 (a)).
  The after-build case is RN-1, and FR-002 is not reported as realized until
  RN-1 is ruled. An EMPTY default stays refused: the default
  contributes openDox's own verbs (R1Q4 (a), R1Q5 (a)). The carve manifest's
  `deleted_at_carve` row SHALL stay byte-identical.
- **FR-003** (requirement 5; 4.1, 4.1a, 4.2, 4.3; F4.1): every deferred reach
  into openxFactory or openXdox SHALL resolve through a seam openDox declares.
  With nothing registered, it SHALL refuse, naming the seam and the remedy. The
  home corpus SHALL be registered by the entry point (openDox's
  `LocalGitCorpus`) unless a host registered its own. `consumer_reach.py` SHALL
  be retired with its last name. Placement: the eight reaches into openxFactory
  in phase 1, and the nineteen into openXdox no later than the phase whose
  surface calls them (R1Q9 (a); R1Q10, still open).
- **FR-004** (requirement 4; 5.0–5.6; F5.1, F5.2, F5.3): openDox SHALL generate
  its own neutral snapshot over `CorpusAdapter` and `LocalGitCorpus`,
  rendering the six ruled words. It SHALL declare a generator seam. openXdox
  SHALL keep its governed generator and contribute it through that seam, with
  its projection unchanged (R1Q11, R1Q13 and R1Q23, open; R1Q7 (a)).
- **FR-005** (requirement 7; 7.0–7.3; F7.1, F7.2): openDox's validator and the
  schemas it reads SHALL be on disk in one installed checkout. The input set is
  narrowed to openDox's own kinds first, and no intent-plane or governance
  schema is vendored. openXdox's validator lookup SHALL resolve through its
  installed distribution, with no parent walk (R1Q12, R1Q14).
- **FR-006** (requirement 9; 9.1–9.5; F9.1, F9.2): each leg's required check
  SHALL run its whole suite green in its own checkout. Where a check runs less
  than the whole suite, it SHALL declare the exclusion with its count and its
  reason, and report it as an open extraction (requirement 9, first scenario).
  - **openDox-code**: the whole suite, `tests_runtime/` included, run against
    the required job's database (R1Q8 (a)). No exclusion is declared.
  - **openXdox-code, for release 1**: the whole suite less the declared
    `doc_health` exclusion (R1Q6 (d); F9.1 as amended by T007 batch B). The
    exclusion stays an OPEN EXTRACTION until the direction arc (T008) lands.
    It is reported as open, and never as closed, including at the archive.
  - Behaviour that needs both legs SHALL be declared integration tests at the
    declared composition.
  - The margins SHALL be restored, with no skip carrying the gap. A skip that
    defers `doc_health` becomes part of the declared exclusion instead (T044).
  - The pins SHALL advance by their owners' ordinary pin-sync acts (R1Q7 (a)).

  FR-006 is met for release 1 when both legs' checks pass as above. Requirement
  9 is fully met only once the exclusion is empty.
- **FR-007** (requirement 10; 10.1–10.3; F10.1): openDox SHALL declare one
  console script, `opendox`, that serves the whole browser surface from an
  openDox-only install. The openDox root's README SHALL document the single
  command, and the root SHALL NOT host it (R1Q5 (a); R1Q15, still open).
- **FR-008** (requirements 12 and 13; 13.1–13.6; F13.1): the standalone install
  SHALL bring its own PostgreSQL, with one dialect and both DSNs. It SHALL
  offer an explicitly selected local single-user mode, loopback-only and with
  no broker, while the hosted mode stays unchanged and refuses without its
  issuer. The serving process SHALL report its own install shape (R1Q15,
  R1Q16).
- **FR-009** (requirement 17; 16.1–16.6; F16.1): chat SHALL reach any
  OpenAI-compatible endpoint by URL, model name and credential reference, and
  SHALL refuse a raw key when it is declared. With no model configured, it
  SHALL show a "no model configured" state before any turn, and every other
  surface SHALL work. Exactly one module SHALL contact a provider (R1Q10,
  R1Q17, R1Q18).
- **FR-010** (requirement 1; 11.0, 11.1; F11.1): release 1 SHALL move nothing
  out of openxFactory. Every realization landing SHALL carry `Arc:
  neutral-product-standalone-operability`, and bookkeeping SHALL NOT (R1Q20
  (a)). openxFactory's arc edits SHALL stay within 11.1's surfaces: its three,
  plus the named composition tests of R1Q2 (a) (R1Q22 (a)).
- **FR-011** (acceptance): release 1 SHALL pass AT-R1 (below) before its
  bookkeeping ticks the release-1 boxes.
- **FR-012** (process): no task SHALL start while a question in its
  `Blocked by:` line is open. Every realization PR SHALL name its task ids, the
  boxes it realizes, and the falsifier it ran, with the output quoted.

### Key Entities

- **Default profile**: openDox's own domain profile (documents and ideas), with
  `DISPLAY` as `NEUTRAL_DISPLAY`, registered by the entry points (R1Q3 (a)). It
  contributes openDox's own verbs, the runtime verbs through
  `RuntimeSubcommand` now (R1Q4 (a), R1Q5 (a)).
- **Handler contribution**: the facet R1Q1 (a) rules. A profile or extension
  declares the mixin classes whose methods its bindings name, and
  `build_server` composes them into `BoundDashboardHandler`'s bases.
- **Declared exclusion**: openXdox-code's committed list of the test files that
  need openxFactory's `doc_health`, with its count and reason, reported as an
  open extraction (R1Q6 (d)).
- **Home-corpus registration**: `corpus_adapter.register_home(factory)` and
  `home()`, plus `ADAPTER_NOT_REGISTERED`.
- **Generator seam**: the operation handed over, its registration point beside
  `domain_profile.register()`, and the conformance it requires (5.4).
- **Neutral snapshot**: the artifact openDox's generator writes, whose contract
  is set by R1Q11 and R1Q12.
- **Install mode**: `OPENDOX_INSTALL_MODE` (`local` | `hosted`, default
  `hosted`), and its `install` block on `/capabilities`.
- **Model binding**: the doxBench record, which grows from nine fields to ten
  (`model`) and gains the `openai-chat-v1` dialect.
- **Arc landing**: a commit on a repository's `main` first-parent line that
  carries the `Arc:` trailer. It is what 5.4a's, 12.5's and 11.1's guards read.
- **Pin pair**: a gitlink plus its `contracts/*-pin.yaml`, moved in one commit.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001** (phase 1 exit): at the phase-1 tip, F2.1, F3.1, F9.1 (in both
  legs) and F9.2 exit 0, each as amended where T007 records an amendment, and
  `opendox --help` exits 0. RN-1 is ruled, and T016 matches the ruling.
  - openDox-code's suite goes from 0 passed today to whole and green.
  - openXdox-code's goes from 57 collection errors to green over the whole
    suite less its declared `doc_health` exclusion (R1Q6 (d)). The exclusion
    is reported as an open extraction, as FR-006 says.
- **SC-002** (phase 2 exit): F5.1, F5.2, F5.3, F7.1 and F7.2 exit 0, with F5.2
  as T007's batch C amends it and as R1Q23 decides.
- **SC-003** (phase 3 exit): F4.1, F10.1, F13.1 and F16.1 exit 0, and the F4.1
  scan prints `no deferred reach names the consumer or the publisher`.
- **SC-004**: AT-R1 passes, and its evidence is recorded in this feature's
  `evidence/` directory.
- **SC-005**: after each phase's openxFactory landings, an interim F11.1 run
  (`PACKET_MERGE=94b6f7f1`), with the guard as widened by T007's batch A,
  prints `requirement 1 holds`.
- **SC-006**: at release-1 close, 65 of release 1's 69 boxes are ticked, each
  with its evidence:
  - 63 by T097;
  - 3.0, by the ratification record (#1151);
  - 5.6, which was already `[x]`.

  The other four (9.5, 11.0, 11.1 and F11.1) are performed in every phase, but
  left open for the arc's close after release 2.
- **SC-007**: openxFactory's required checks are green at every pin advance
  this release makes.

### AT-R1 — the release-1 acceptance test

The brief states it this way: *"on a clean machine with only openDox installed,
a plain git repo opens, and the wheel, radar lens and chat panes work, with
chat's 'no model configured' state."* Each term is made checkable below.
[`quickstart.md`](./quickstart.md) gives the procedure.

1. **Clean machine.** The run uses a fresh venv and a fresh
   `OPENDOX_STATE_DIR`, and each of the following is ASSERTED to be absent, not
   assumed absent:
   - `openxdox`, `ideation_dashboard`, `doc_health` and
     `corpus_adapter_openxfactory`, none importable;
   - `omp` on the PATH;
   - any database or identity broker the user provided;
   - any model binding.
2. **Only openDox installed.** openDox-code is installed as R1Q16 decides, and
   nothing else.
3. **A plain git repository.** Two repositories are used, each copied into a
   fresh `git init`:
   - (a) 5.0's `plain-documents` fixture;
   - (b) a directory of ordinary `.md` files with no front matter at all.
4. **Opens.** The ONE command the openDox root README documents (R1Q15) serves
   the bundle on loopback.
5. **The wheel works.** `#tab-wheel` renders a tile for every document station
   the snapshot fills, and raises no `pageerror`.
6. **The radar lens works.** `#tab-lens` renders the bullseye with the corpus's
   documents as dots, and not the text "nothing on the radar". Its two
   openxFactory seed actions behave as R1Q19 decides.
7. **The chat pane works.** From a grouping tile's `workbench` verb, the
   staging workbench opens, and its chat rail shows the "no model configured"
   state, naming how to configure a model, BEFORE any turn is attempted. A turn
   is refused `model_capability_unavailable`, and both editors stay usable.
8. **No errors.** There are zero `pageerror` events. Every other console error
   or failed request is declared to `tests/smoke_signals.py`'s oracle, or the
   run fails. No route the three panes request answers 5xx.

The HTTP half (steps 1–4, and the route answers behind steps 5–8) runs in CI in
openDox-code (T095). It is a harness in its own `acceptance` job, which has no
database service, so its clean-machine assertions hold. The browser half is a
Playwright run on the host, with its verdict computed by the oracle (T096). CI
carries no browser, as the oracle's own header records. Neither half is a
member of a leg's pytest suite: each installs the product and drives it from
outside, so FR-006 is unaffected.

## Assumptions

- Release 2 (Groups 6, 12, 14 and 15), Group 8 and F1–F4 are out of scope. The
  archive needs BOTH releases' evidence (`5800995035` answer 2), so landing
  release 1 archives and promotes nothing.
- The eleven answers of `5817152735` are applied in this revision, so phase 1
  is planned on its answers.
- The open questions (R1Q10–R1Q19, R1Q21, R1Q23) are applied by each
  provisional phase's round task (T009, T069) before any task they block.
- Phases 2 and 3 are PROVISIONAL. They are drafted on the recommended
  options, and each conditional step names its question. They authorize no
  implementation until their round task has re-planned them on their answers
  and re-run analyze.
- Lane 4's own acts C1, C3 and C4 (`#656` `5815604830`, `5815613524`,
  `5815620605`) are in flight, and this feature neither duplicates nor
  pre-empts them.
