# Feature Specification: openDox standalone operation (release 1)

**Feature Branch**: `034-opendox-standalone-operation`
**Created**: 2026-09-24
**Status**: Draft (planning; 22 clarify questions open)
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

**THE RATIFIED PACKET IS THE AUTHORITY, NOT THIS FILE.** Every requirement
below realizes one of #1144's requirements and names it. Nothing here restates,
narrows or widens the packet. Where this file appears to do so, that is a
defect in this file, and the packet wins. Where the packet contradicts itself
or the live code, the contradiction is put to Brett as a question
([`clarify-questions.md`](./clarify-questions.md), `R1Q1`–`R1Q22`). It is never
settled here by assumption.

**Why the feature lives in openxFactory.** The governing change lives here.
The global protocol hands a change to a Speckit feature under `specs/NNN-*` in
the change's own repository (lifecycle step 3). openDox-spec cannot govern this
work yet: requirement 8's interim arrangement applies, because openDox-spec has
promoted none of the 71 requirements the carve assigned it (#1144 Group 8). The
IMPLEMENTATION lands in five repositories, each by that repository's own pull
request: openDox-code, openXdox-code, openDox, openXdox and openxFactory.

## Clarifications

### Session 2026-09-24 (round 1): OPEN

Twenty-two questions are raised in [`clarify-questions.md`](./clarify-questions.md)
and are awaiting Brett Heap. Each answer is encoded here by T004, in the same
commit that records it. Until then, every task a question blocks carries
`Blocked by: R1Qn` in [`tasks.md`](./tasks.md), and none of those tasks may
start. The questions are named `R1Q<n>` because a bare `Q<n>` already names one
of #1144's own rulings (RULING Q1, RULING Q2, Q-R4, DIRECTION Q5).

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
corpus adapter. Each leg's suite runs whole and green in its own checkout. The
`opendox` console script exists.

**Why this priority**: nothing else in the release can be exercised until the
product imports and its suite runs. Today openDox-code's suite gives 0 passed
and 1,305 errors (research R2).

**Independent Test**: at the phase-1 tip, F2.1, F3.1 (as amended per R1Q3),
F9.1 (in both legs), F9.2 and `opendox --help` all pass. So do 4.3's eight
reaches into openxFactory, under F4.1's scan restricted to the publisher's
packages.

**Acceptance Scenarios**:

1. **Given** a fresh venv holding only openDox-code with `.[runtime,test]`,
   **When** every module of `opendox` is imported, **Then** each one imports,
   and 2.4's test names the first module that does not (requirement 2).
2. **Given** no host has registered a profile, **When** an entry point builds
   the parser, **Then** it builds on openDox's own default profile. A profile a
   host registers replaces the default (requirement 3; R1Q3, R1Q4).
3. **Given** nothing is registered, **When** a verb needs the home corpus,
   **Then** it refuses with `CorpusRefused` of kind `ADAPTER_NOT_REGISTERED`,
   naming the seam and the remedy. **Given** an entry point was built, **Then**
   the home corpus is openDox's `LocalGitCorpus` (requirement 5).
4. **Given** each leg's own checkout with no sibling present, **When**
   `python -m pytest -q` runs, **Then** it is green. `validate.yml` names no
   file list and no `--noconftest` (requirement 9; R1Q6, R1Q8).
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
F5.2 (5.4a) and F7.1 (7.3) all pass.

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
   (requirement 4, third scenario; R1Q7).
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
each phase's openxFactory landings exits 0 (T093). F5.2 and 9.3's integration
suite pass.

**Acceptance Scenarios**:

1. **Given** openxFactory at a pin carrying the removal of 2.1, **When** its
   server is built, **Then** its five lane routes are served through the seam
   (R1Q1, R1Q2).
2. **Given** every arc landing on openxFactory `main` since `94b6f7f1`, **When**
   F11.1 runs, **Then** each path touched is one of 11.1's surfaces, and the
   manifest differs only by extended notes (requirement 1; R1Q20, R1Q22).

---

### Edge Cases

- A host registers AFTER an entry point registered the default (R1Q3 (ii)).
- A governed host FORGETS to register, and gets a working-looking parser
  without its gate verbs (R1Q4).
- The install mode is unset (R1Q15), or a local install is asked to bind
  beyond loopback, which is refused with no opt-in (13.4).
- A raw key appears inside an endpoint URL, not in a field (16.3).
- The plain repository yields no grouping, candidate or selection tile, so the
  chat pane cannot be opened at all (R1Q13).
- The served model-catalog route validates against openxFactory's
  `doxbench_contracts`, so it fails closed without them (R1Q10, R1Q12).
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
  lane routes SHALL be contributed through a declared seam (R1Q1). A test in
  openDox's own suite SHALL import every module. The openDox → openxFactory
  direction SHALL be watched by a required check.
- **FR-002** (requirement 3; 3.0–3.3; F3.1): openDox SHALL ship a default
  profile for its own domain that carries no publisher vocabulary. Entry points
  SHALL build on it when no host has registered, and a registered profile
  SHALL replace it. An EMPTY default stays refused (R1Q3, R1Q4). The carve
  manifest's `deleted_at_carve` row SHALL stay byte-identical.
- **FR-003** (requirement 5; 4.1, 4.1a, 4.2, 4.3; F4.1): every deferred reach
  into openxFactory or openXdox SHALL resolve through a seam openDox declares.
  With nothing registered, it SHALL refuse, naming the seam and the remedy. The
  home corpus SHALL be registered by the entry point (openDox's
  `LocalGitCorpus`) unless a host registered its own. `consumer_reach.py` SHALL
  be retired with its last name. Placement: the eight reaches into openxFactory
  in phase 1, and the nineteen into openXdox no later than the phase whose
  surface calls them (R1Q9, R1Q10).
- **FR-004** (requirement 4; 5.0–5.6; F5.1, F5.2, F5.3): openDox SHALL generate
  its own neutral snapshot over `CorpusAdapter` and `LocalGitCorpus`,
  rendering the six ruled words. It SHALL declare a generator seam. openXdox
  SHALL keep its governed generator and contribute it through that seam, with
  its projection unchanged (R1Q11, R1Q13, R1Q7).
- **FR-005** (requirement 7; 7.0–7.3; F7.1, F7.2): openDox's validator and the
  schemas it reads SHALL be on disk in one installed checkout. The input set is
  narrowed to openDox's own kinds first, and no intent-plane or governance
  schema is vendored. openXdox's validator lookup SHALL resolve through its
  installed distribution, with no parent walk (R1Q12, R1Q14).
- **FR-006** (requirement 9; 9.1–9.5; F9.1, F9.2): each leg's required check
  SHALL run its whole suite green in its own checkout. Behaviour that needs
  both legs SHALL be declared integration tests at the declared composition.
  The margins SHALL be restored, with no skip carrying the gap. The pins SHALL
  advance by their owners' ordinary pin-sync acts (R1Q6, R1Q7, R1Q8).
- **FR-007** (requirement 10; 10.1–10.3; F10.1): openDox SHALL declare one
  console script, `opendox`, that serves the whole browser surface from an
  openDox-only install. The openDox root's README SHALL document the single
  command, and the root SHALL NOT host it (R1Q5, R1Q15).
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
  neutral-product-standalone-operability`. openxFactory's arc edits SHALL stay
  within 11.1's three surfaces (R1Q2, R1Q20, R1Q22).
- **FR-011** (acceptance): release 1 SHALL pass AT-R1 (below) before its
  bookkeeping ticks the release-1 boxes.
- **FR-012** (process): no task SHALL start while a question in its
  `Blocked by:` line is open. Every realization PR SHALL name its task ids, the
  boxes it realizes, and the falsifier it ran, with the output quoted.

### Key Entities

- **Default profile**: openDox's own domain profile (documents and ideas), with
  `DISPLAY` as `NEUTRAL_DISPLAY`. Its extension contents are set by R1Q4 and
  R1Q5.
- **Handler contribution**: whatever R1Q1 selects to let a host's routes name
  methods that only the host's mixin carries.
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
  legs) and F9.2 exit 0, and `opendox --help` exits 0. openDox-code's suite
  goes from 0 passed today to whole and green, and openXdox-code's from 57
  collection errors to whole and green (or to the declared exclusion that
  R1Q6 (d) admits).
- **SC-002** (phase 2 exit): F5.1, F5.2, F5.3, F7.1 and F7.2 exit 0.
- **SC-003** (phase 3 exit): F4.1, F10.1, F13.1 and F16.1 exit 0, and the F4.1
  scan prints `no deferred reach names the consumer or the publisher`.
- **SC-004**: AT-R1 passes, and its evidence is recorded in this feature's
  `evidence/` directory.
- **SC-005**: after each phase's openxFactory landings, an interim F11.1 run
  (`PACKET_MERGE=94b6f7f1`) prints `requirement 1 holds`.
- **SC-006**: at release-1 close, 63 of release 1's 69 boxes are ticked, each
  with its evidence.
  - 3.0 is ticked by the ratification.
  - 5.6 was already `[x]`.
  - 9.5, 11.0, 11.1 and F11.1 are performed, but left open for the arc's close
    after release 2.
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

The HTTP half (steps 1–4, and the route answers behind steps 5–8) is a CI test
in openDox-code (T095). The browser half is a Playwright run on the host, with
its verdict computed by the oracle (T096). CI carries no browser, as the
oracle's own header records.

## Assumptions

- Release 2 (Groups 6, 12, 14 and 15), Group 8 and F1–F4 are out of scope. The
  archive needs BOTH releases' evidence (`5800995035` answer 2), so landing
  release 1 archives and promotes nothing.
- The answers to R1Q1–R1Q22 are applied (T004) before any task they block. The
  plan and the tasks are written CONDITIONALLY on the recommended options, and
  each conditional step names its question.
- Lane 4's own acts C1, C3 and C4 (`#656` `5815604830`, `5815613524`,
  `5815620605`) are in flight, and this feature neither duplicates nor
  pre-empts them.
