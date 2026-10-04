# Feature Specification: openDox standalone operation (release 1)

**Feature Branch**: `034-opendox-standalone-operation`
**Created**: 2026-09-24
Status: draft
**Clarifications**: all 27 clarify questions are answered, in three rounds:
eleven on `#656` comment `5817152735`, fourteen on comment `5850003126`, which
also ruled RN-1 (a), and two on comment `5851950767`. No phase is
provisional.
**Realizes**: RELEASE 1, "standalone operation", phases 1–3, of the
openxFactory OpenSpec change `add-neutral-product-standalone-operability`
(#1144, landed `94b6f7f1`). The phases follow that change's RULED release map
(`#656` `5799646419`, as corrected by `5800995035`). T005's re-plan brought
7.3 into phase 1 by #1155's contingency, and R1Q25 (b) returned it to phase 2,
so the build follows the map. One reading stands beside the map, and T007's
batch F records it: 9.2's whole-suite check lands in phase 1, and the box
closes in phase 3.
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
R1Q6"*. He answered the other fourteen, and RN-1, on comment `5850003126`
(2026-09-26T21:23:03Z), verbatim: *"go with recommendations on all the open
questions"*.

**THE RATIFIED PACKET IS THE AUTHORITY, NOT THIS FILE.** Every requirement
below realizes one of #1144's requirements and names it. Nothing here restates,
narrows or widens the packet. Where this file appears to do so, that is a
defect in this file, and the packet wins. Where the packet contradicts itself
or the live code, the contradiction is put to Brett as a question
([`clarify-questions.md`](./clarify-questions.md), `R1Q1`–`R1Q27`). It is never
settled here by assumption.

**Why the feature lives in openxFactory.** The governing change lives here.
The global protocol hands a change to a Speckit feature under `specs/NNN-*` in
the change's own repository (lifecycle step 3). openDox-spec cannot govern this
work yet: requirement 8's interim arrangement applies, because openDox-spec has
promoted none of the 71 requirements the carve assigned it (#1144 Group 8). The
IMPLEMENTATION lands in five repositories, each by that repository's own pull
request: openDox-code, openXdox-code, openDox, openXdox and openxFactory. A
sixth, openDox-spec, joins through T053, since R1Q11 is answered (a).
openXdox-spec is not touched, since R1Q12 is answered (a).

## Clarifications

### Session 2026-09-24

Round 1 raised 22 questions in [`clarify-questions.md`](./clarify-questions.md),
and one answer raised a 23rd. T005's re-measure raised a 24th on 2026-09-25
([`evidence/remeasure-2026-09-25.md`](./evidence/remeasure-2026-09-25.md)),
and T006's analyze a 25th the same day
([`evidence/analyze-round-1a.md`](./evidence/analyze-round-1a.md)). Round 2's
analyze raised a 26th and a 27th on 2026-09-27
([`evidence/analyze-round-2.md`](./evidence/analyze-round-2.md)), and Brett
answered both the same day.
They are named `R1Q<n>`, because a bare `Q<n>` already names one of #1144's own
rulings (RULING Q1, RULING Q2, Q-R4, DIRECTION Q5).

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
  needed"). RN-1 held phase 1's close (T049), but not T016's landing, until
  it was ruled (a) (§ Session 2026-09-26).
- Q: R1Q4. What does the default profile contribute, given that an empty
  default stays refused? → A: (a). openDox's own verbs and routes: the runtime
  verbs now, and release 2's `submit`, `land` and `health` later. Its display
  words are `NEUTRAL_DISPLAY`'s: it declares no `DISPLAY` facet, so the absent
  facet renders them (holder reading, `#656` `5851560764`). A governed host's
  own start asserts that its profile is the registered one.
- Q: R1Q5. Where do the runtime verbs register without breaking the 31-entry
  golden? → A: (a). Through the default profile's `SUBCOMMAND_EXTENSIONS`
  (`RuntimeSubcommand`), and `opendox-runtime` stays as an alias. A host that
  registers its own profile keeps its 31-entry tree.
  - The count moves at phase 3 (`5970917267`, § Session 2026-10-02 and
    2026-10-03 below). T100 adds `model-binding trust`, so from phase 3's pin
    the host's tree has 32 entries. The answer itself stands: the runtime
    verbs still do not reach a host's tree.
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

### Session 2026-09-26

Brett Heap answered the other fourteen, and RN-1, on `#656`, comment
`5850003126`, 2026-09-26T21:23:03Z, verbatim: *"go with recommendations on all
the open questions"*. Each is answered with the option `clarify-questions.md`
recommended. T019, T009 and T069 encode them.

- Q: R1Q14. Does 7.3's falsifier or lane 4's C3 govern `find_validator`? → A:
  (a), 7.3. The lookup ignores its start and resolves the installed
  distribution's validator, and C3's test is revised in 7.3's landing (T061).
  F5.2's allow-list admits both of F7.1's edits, each with its reason.
  openxFactory's scripts read what T061 leaves unchanged, and T066, a non-arc
  openxFactory act, revises the seal test at both pins. Under R1Q27 (a) it
  moves none of openxFactory's validator callers (T067).
- Q: R1Q24. Where do openXdox-code's files that need openxFactory's
  status-exemption rail or its contracts run? → A: (a). They join the declared
  exclusion, each file with its own reason, as open extractions that the
  direction arc (T008) takes. F7.1's second test still runs by node id.
- Q: R1Q25. Does 7.3 move into phase 1, against the RULED release map? → A:
  (b), no. 7.3 stays in phase 2, beside openDox's own validator. Phase 1's
  openXdox-code check declares `tests/test_snapshot.py` in the exclusion with
  its own reason until 7.3 lands. 9.2's whole-suite check lands in phase 1, and
  the box closes in phase 3.
- Q: R1Q10. Which consumer mechanisms get an openDox-owned default? → A: (a),
  each on release 1's path, in R-G3's pattern. openDox's neutral default is
  registered by the entry points, and openXdox contributes its governed one
  through the same seam. openxFactory's two reaches default to openDox's own
  chat validators and to no status exemption.
- Q: R1Q11. How can a neutral snapshot be schema-valid? → A: (a). openDox-spec
  owns a neutral snapshot schema whose stage values are the six role keys.
  openXdox keeps its governed schema, and its facet carries the governed
  snapshot values. The bundle is cut as a `dox-v1.x` minor.
- Q: R1Q12. Which snapshot schema does openDox's validator own? → A: (a), the
  neutral one, since R1Q11 is (a). The code leg carries digest-checked copies
  of its spec leg's four schemas, and the malformed fixture breaks one of the
  neutral schema's rules.
- Q: R1Q13. How does a plain document land in a station? → A: (a), with (c)
  for documents that declare nothing. A neutral front-matter key names the
  stage role, the default adapter declares a small neutral field set, and a
  document that declares nothing is a source, with groups derived from shared
  topics. The fixture yields at least one group.
- Q: R1Q23. Where do 5.4a's four `doc_health` suites run for F5.2? → A: (a).
  F5.2's environment composes openxFactory's `scripts/` at a named commit.
- Q: R1Q15. Does the documented command serve or refuse with nothing
  configured? → A: (b). It selects local explicitly, with a `--local` flag, and
  F10.1 and 10.3's README carry it.
- Q: R1Q16. What is "one served product"? → A: as recommended. (i) The
  document server owns the bundled PostgreSQL as its child and reports it.
  (ii) Starting and migrating the store is all 13.1 asks. (iii) The standalone
  install is the `opendox[local]` extra. (iv) The bundled server stops with the
  entry point.
- Q: R1Q17. What resolves a credential reference standalone? → A: (b), a
  built-in resolver for `env:` and OS-keyring references, inside
  `doxbench_provider.py` only.
- Q: R1Q18. How does an endpoint declare that it takes no credential? → A: (a),
  a third auth kind, `none`, which forbids the broker and the reference.
- Q: R1Q19. The lens's two openxFactory seed actions, standalone? → A: (a) now,
  (b) later. They are offered only where a binding answers them.
- Q: R1Q21. Release 2: a second feature? → A: (a). Release 2 is its own
  Speckit feature, planned once release 1 lands.
- RN-1 → A: (a). Requirement 3's fourth scenario is amended so that a host
  registration replaces the default only before a parser or server is built
  from it, and a scenario for the refusal after a build is added. The ruling's
  own words send the text through an amendment to the change: T007's batch D,
  which landed as #1170 → `79a720a2`.

The #1144 lines these answers amend are T007's batches F, G and H
([`tasks.md`](./tasks.md) § "Ruled amendments"). This revision edits no file
of #1144.

### Session 2026-09-27

Round 2's analyze found two questions that the answers did not settle, and
[`clarify-questions.md`](./clarify-questions.md) put them to Brett Heap. He
answered both on `#656`, comment `5851950767`, 2026-09-27T02:25:29Z, verbatim
*"(a) Admit the two edits (Recommended)"* and *"(a) Own three, others by tree
(Recommended)"*. T067 encodes them. When the analyze's second pass found a
route R1Q26 had not listed (W2-10), Brett was shown it and kept (a), on
comment `5852513402`, verbatim *"Keep (a) as ruled (Recommended)"*.

- Q: R1Q26. openXdox's facet gains a `values` block (R1Q11 (a)), but one of
  12.5's protected suites pins the facet as it is, and so does openxFactory's
  own facet test. How does the block land? → A: (a). T007's batch I amends
  5.3a to admit the block, and 12.5's falsifier to admit the two edits to
  `tests/test_gate_loop_views.py`, each entered with its reason. T060 makes
  the first and T059 the second. T066 composes `values` into openxFactory's
  profile at both pins.
- Q: R1Q27. 7.3 narrows the consumer's validator to its three schemas, but
  openxFactory's contracts name that validator as the one that checks
  openxFactory's own four kinds. What validates them afterwards? → A: (a).
  The validator checks its own three from its installed distribution, and the
  other kinds only where the tree it runs from supplies their schemas, as
  openxFactory's farm does today. F7.1's second test reads *"every schema this
  install validates is on disk"* (batch I). No contract row changes.

The #1144 lines these answers amend are T007's batch I ([`tasks.md`](./tasks.md)
§ "Ruled amendments").

### Session 2026-10-02 and 2026-10-03

Phase 3's own work raised seven more questions. Brett Heap answered each by
multiple choice, and each answer is the option marked *(Recommended)*. Each is
posted on `#656`, and the time below is the comment's. [`tasks.md`](./tasks.md)
encodes them, in T086, T094, T099–T104 and AT-R1's two halves.

- Q: How does release 1 install, and does the aggregation's pin-sync after
  T064 land? (`5962754358`, 2026-10-02T22:55:22Z) → A: two answers.
  - (1) *"Publish to PyPI at the cut (Recommended)"*. openDox-code publishes
    the wheel to PyPI as `opendox` by trusted publishing (OIDC), so no token
    is stored anywhere, and 10.3's `pip install "opendox[local]"` works as
    written (T101, T099).
  - (2) *"Yes, land when green (Recommended)"*. The opensoft/xFactory
    pin-sync after T064 lands as a merge commit, once its tests pass with the
    submodules initialized. It moves the openxFactory gitlink,
    `.github/clearing/openxfactory/PIN.yaml` and the root openDox and
    openXdox gitlinks in ONE commit.
- Q: Which version does openDox's first PyPI release carry?
  (`5963162921`, 2026-10-02T23:38:05Z) → A: *"0.1.0 (Recommended)"*. The
  version bump is the last phase-3 openDox-code landing, T087 pins that
  commit, and the release workflow publishes only the commit the openDox
  root's `contracts/code-pin.yaml` names (T101, T087, T099).
- Q: A standalone workbench opens read-only, because its editors and chat
  rail wait on a create gate that only openXdox answers. Where should they
  appear? (`5963618568`, 2026-10-03T00:28:27Z) → A: *"Edit and chat by scope
  (Recommended)"*. The editors and the chat rail appear wherever the scope
  lets the document be edited. Only creating documents and Save stay behind
  the gate, so Save is refused by name (T102).
- Q: A standalone openDox serves its console token from `/capabilities` to
  any loopback caller, other OS users of the same machine included. How
  does the page get the token? (`5963851934`, 2026-10-03T00:56:13Z) → A:
  *"Token via the opened URL (Recommended)"*. The server stops handing the
  token out from `/capabilities`. `generate-and-open` opens the page with
  the token in the URL's fragment and keeps a private copy (0600) in the
  state directory (T104). T007's batch N records #1144's side, and T095's
  harness reads the private copy.
- Q: Where does openxFactory stand under T100's per-machine binding trust
  when it hosts openDox? (`5970369724`, 2026-10-03T15:02:16Z) → A:
  *"Governance approval (Recommended)"*. The host's registered policy wins
  over openDox's strict default. openxFactory registers `GovernedBindingTrust`
  as a sixth `seams()` entry, with an undo (T094):
  - a binding the governance flow approved is trusted;
  - a declared binding still pending approval is refused
    (`pending_binding_ids`);
  - a binding with no declaration is trusted;
  - an unreadable declarations document admits nothing;
  - `record()` writes nothing.

  The comment also records the holder's rulings on T094's preparation:
  - E1 (a): the help golden's phase-3 copy lands in a non-arc PR ahead of
    T094, in T066's form, under `tests/domain_profile/fixtures/`. That PR
    opens after T087 and is regenerated from T087's commit.
  - E3 (a): that PR is the golden reader only.
  - E4 (a), verbatim: *"#76 merges main before it lands"*.
  - T086 registers no trust policy in openXdox.

  The holder's later comment `5972924576` (2026-10-03T19:56:30Z) reads E3
  (a). It limits the ahead PR's scope, which carries no host wiring, and
  means that the golden's own reader picks the golden from the pinned
  parser. It does not make the golden the PR's only content. The same
  comment rules E5 (a): the PR also carries `test_cli_column_split`'s usage
  line and the rebound-Host case of `test_doxbench_routes.py`, each in
  both-pins form (T094, T103).
- Q: #1144 and this plan fix the assembled `--help` tree at 31 sections, but
  T100 adds `model-binding trust`. Is the count amended? (`5970917267`,
  2026-10-03T16:09:32Z) → A: *"Amend to 32 (Recommended)"*. From phase 3's
  pin the tree has 32 sections.
  - T007's batch O (#1228) records it in #1144, at 10.1, F9.1 and F9.2.
  - openXdox-code's F9.2 test moves to 32 with T086, at the pin move past
    T100.
  - openxFactory's help golden moves with T094's ahead PR. That golden also
    covers T070's `--local`, T079's and T080's `--model` and auth-kind
    changes, and T084's rename of the program to `opendox`.

  The question came from the plan analyze of 2026-10-03 (finding H2).
- Q: On standalone, T102 refuses Save by name, because Save goes through
  openxFactory's create gate. What does AT-R1's "both editors usable" mean
  then? (`5971834845`, 2026-10-03T17:50:13Z) → A: *"Usable = edits; Save
  refused (Recommended)"*. "Usable" means each editor opens and accepts
  edits. On standalone, create and Save are refused by name. The oracle
  declares that refusal, so it is expected and not an error. AT-R1 step 7
  and `quickstart.md` § 4 step 4 carry it.

Of these, only three amend a line of #1144: `5963851934` (T007's batch N,
at #1144's 12.4a); `5970917267` (batch O, at 10.1, F9.1 and F9.2); and item
1 of `5962754358` with `5963162921` (batch O, at 9.5: the one release tag,
`v0.1.0`, that the publish at the cut owes).

### Session 2026-10-04

The holder's adversarial reviews of T104 (openDox-code#84) and T100
(openDox-code#82, landed as `38d3350e`) raised three more questions, and
batch P's review a fourth. Brett Heap answered each by multiple choice, and
each answer is the option marked *(Recommended)*. The first three are in
one comment on `#656`, `5982436447` (2026-10-04T17:11:29Z), which also
records three of the holder's rulings, and the fourth is `5983805990`.

- Q: Snap and Flatpak browsers, and a Windows browser opened from WSL,
  cannot open the private copy's `file://` URL under the hidden default
  state directory, and the token is never printed. What does release 1 do?
  (item 1, finding B3) → A: *"Hint line, accepted limit (Recommended)"*. The
  start prints one more line, with no token, saying that such a browser
  should be used with `OPENDOX_STATE_DIR` set to a folder that is not
  hidden. The openDox root's README documents it (T076), and release 1
  ships with the limit (T104).
- Q: A trust names a digest of the binding's record, so a trusted binding
  whose broker runs a program inside the served repository stays trusted
  after a pull changes that program. What is the rule? (item 2, finding A2)
  → A: *"Refuse in-repo programs (Recommended)"*. A binding's command may
  not name a file inside the served repository, and the broker lives
  outside it. A T100 follow-on openDox-code PR carries it before T087 (claim
  `5982447319`).
- Q: A shell or interpreter wrapper, such as `["/bin/sh", "-c", "exec
  ./tools/broker.py"]`, names no file as an argv member but still runs an
  in-repo program. How far does item 2 reach? (`5983805990`,
  2026-10-04T19:56:01Z, asked on #1230's Copilot thread `r4179024140`) →
  A: *"Refuse inline scripts (Recommended)"*. A binding whose program is a
  shell or an interpreter given an inline script (`sh -c`, `bash -c`,
  `python -c`, `node -e`) is refused by name. The program must be a real
  file outside the served repository, and every broker also starts with its
  working directory outside it. `sh -c "pass show key"` becomes
  `["pass", "show", "key"]`, or a script kept outside the repository. The
  holder's ruling `5984069416` (2026-10-04T20:27:27Z, on Copilot
  `r4179187252`) implements it for launcher chains: a common launcher such
  as `env` is unwrapped to the program it starts, the broker's environment
  drops `PWD` and `OLDPWD`, and a general program that runs code from its
  own arguments (`awk`, `find -exec`) is an accepted release-1 limit.
- Q: A state directory inside the served repository is refused. What of one
  inside some other git checkout? (item 3, finding A14) → A: *"Served repo
  only, limit (Recommended)"*. The check stays as it is, and the wider case
  is an accepted limit, with no code change. A check for any enclosing
  checkout would refuse a home directory kept in git.

The holder's rulings recorded with them:
- B2: a platform without the POSIX primitives refuses the start by name, as
  openDox-code#69's `bundle.unsupported_platform()` does (T104).
- B7: a browser's persistent history keeps the fragment. It is the same
  user's data as the 0600 copy, and the page's `replaceState` cleans only
  session history, so it is an accepted limit (T104).
- A8: the realization follows F16.1's ratified text. A state directory that
  is itself a symbolic link trusts nothing (the T100 follow-on).

T007's batch P records items 1 to 3, `5983805990`, B7 and A8 in #1144, at
12.4a, 16.3a and F16.1, and item 2 with `5983805990` also in a third dated
note to requirement 17, since they narrow batch M's note there. B2 needs no
line there.

**Nothing is open.** No task in [`tasks.md`](./tasks.md) carries a `Blocked
by:` line, and the answers above settle the choices phase 3's additions
raised, T094's help golden and trust policy among them.

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
runs whole. openXdox-code's runs whole less a declared exclusion, which is
reported as an open extraction. It holds the `doc_health` files (R1Q6 (d)),
the files that reach openxFactory's status-exemption rail or its contracts
(R1Q24 (a)), and `tests/test_snapshot.py` until 7.3 lands (R1Q25 (b)), each
with its own reason. The `opendox` console script exists.

**Why this priority**: nothing else in the release can be exercised until the
product imports and its suite runs. Today openDox-code's suite gives 0 passed
and 1,305 errors (research R2).

**Independent Test**: at the phase-1 tip, F2.1, F3.1 (line 2 as amended, R1Q3
(a)), F9.1 (in both legs; openXdox-code's as amended, R1Q6 (d), R1Q24 (a),
R1Q25 (b), and RULED `5870594693`'s one `--deselect`) and `opendox --help` all
pass. So do 4.3's eight
reaches into openxFactory, under F4.1's scan restricted to the publisher's
packages. F9.2 is run and quoted red, not passed: RULED `5859927858` keeps it
unchanged, so it stays red on the 31-entry help-tree test until T008, and
phase 1 closes with it quoted so (holder decision, 2026-09-29, at T049).
From phase 3's pin that test reads 32 entries, because T100 adds
`model-binding trust` (RULED `5970917267`; T086 moves it).

**Acceptance Scenarios**:

1. **Given** a fresh venv holding only openDox-code with `.[runtime,test]`,
   **When** every module of `opendox` is imported, **Then** each one imports,
   and 2.4's test names the first module that does not (requirement 2).
2. **Given** no host has registered a profile, **When** an entry point builds
   the parser, **Then** it builds on openDox's own default profile, which the
   entry point registered. A profile a host registers before anything is built
   replaces the default, and one registered after a build is refused
   (requirement 3, as RN-1 (a) amends it; R1Q3 (a), R1Q4 (a)).
3. **Given** nothing is registered, **When** a verb needs the home corpus,
   **Then** it refuses with `CorpusRefused` of kind `ADAPTER_NOT_REGISTERED`,
   naming the seam and the remedy. **Given** an entry point was built, **Then**
   the home corpus is openDox's `LocalGitCorpus` (requirement 5).
4. **Given** each leg's own checkout with no sibling present, **When**
   `python -m pytest -q` runs, **Then** it is green. `validate.yml` names no
   file list and no `--noconftest` (requirement 9).
   - openDox-code's whole suite includes `tests_runtime/`, run against the
     required job's database (R1Q8 (a)).
   - openXdox-code's is the whole suite less its declared exclusion, which
     every run reports with its count and each entry's reason. It holds the
     `doc_health` files (R1Q6 (d)), the files that reach openxFactory's
     contracts or rail (R1Q24 (a)), and `tests/test_snapshot.py` until 7.3
     lands in phase 2 (R1Q25 (b)).
5. **Given** openXdox-code with openDox at its pin, **When** the declared
   integration suite runs, **Then** it passes, including the assembled
   `--help` tree (requirement 9, third scenario). The tree has 31 entries
   through phase 2, and 32 from phase 3's pin, where T100 adds
   `model-binding trust` (RULED `5970917267`).

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
that are on disk in the installed package. The snapshot's contract is
openDox-spec's own neutral schema (R1Q11 (a)). A plain document lands in the
station its neutral front matter names, or among the sources when it declares
nothing (R1Q13 (a) with (c)). With openXdox installed, the
governed corpus is projected exactly as it is today.

**Why this priority**: a product that can only serve snapshots it cannot
generate is not standalone (requirement 4, first scenario).

**Independent Test**: at the phase-2 tip, F5.3, F7.2 and F5.1 (5.3a re-run)
pass. F5.2 (5.4a) is run and quoted: it is red on three pre-arc carve-residue
tests of `tests/test_session_snapshot.py` until T086 repairs them, and its box
closes at phase 3's checkpoint, T089 (RULED `5962785556`, item 1; T063). F5.2
is run as T007's batches C, F, G and K amend it,
with openxFactory's `scripts/` composed at a named commit (R1Q23 (a)) and its
last step passing `--chains` (`5916000030`, item 4). F7.1 (7.3)
passes too, since R1Q25 (b) keeps 7.3 in this phase, and its second test
reads as R1Q27 (a) has it.

**Acceptance Scenarios**:

1. **Given** the 5.0 fixture in a fresh repository and neither `openxdox` nor
   `doc_health` importable, **When** `python -m opendox.cli generate` runs,
   **Then** a non-empty snapshot is written. No string value in it carries a
   declared governance word (requirement 4, second scenario; R1Q11 (a), R1Q13
   (a) with (c)).
2. **Given** the 7.0 malformed fixture, **When** `generate --strict` runs,
   **Then** it exits non-zero, naming the fixture's `EXPECTED_RULE`, and it
   does not fail on an unresolvable path (requirement 7; R1Q12 (a): the rule is
   the neutral schema's).
3. **Given** openXdox-code installed, with the realized openDox installed over
   its pinned one, **When** 5.4a's generator suites run (F5.2 takes them by
   glob, and at openXdox-code `e28930bf` it selects seven), **Then** they pass,
   and no arc landing edited them except through R1Q7 (a)'s reviewed
   allow-list (requirement 4, third scenario). The four `doc_health` suites run
   with openxFactory's `scripts/` composed at a named commit (R1Q23 (a)).

7.3's scenario is User Story 4's third, and it closes in this phase (R1Q25
(b)).

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
R1Q15 and R1Q16), F16.1 (as T007's batches M and P amend it) and F4.1 (the whole
package: no deferred reach, and `consumer_reach.py` gone) pass. So does
**AT-R1**, defined under Success Criteria.

**Acceptance Scenarios**:

1. **Given** no database, no broker and a fresh `OPENDOX_STATE_DIR`, **When**
   the documented command runs in local mode, **Then** the served process
   reports `install.mode == local`, a bundled datastore under the state
   directory with no TCP listener, and migrations applied (requirements 12 and
   13). The command is `opendox generate-and-open --local …`, after
   `pip install "opendox[local]"` (R1Q15 (b), R1Q16 (iii)). The bundled server
   is the document server's child, and it stops with the entry point (R1Q16
   (i), (iv)).
2. **Given** a hosted install, or an unset mode, with no issuer, **When** the
   same command runs, **Then** it refuses, naming `OPENDOX_OIDC_ISSUER`, and
   never degrades to local (requirement 13; R1Q15 (b): only `--local` or the
   setting selects local).
3. **Given** a stand-in OpenAI-compatible server on loopback, **When** a chat
   turn is sent, **Then** it reaches that server in the chat-completions
   grammar and names the configured model (requirement 17).
4. **Given** a binding whose endpoint URL or extra field carries a key,
   **When** it is declared, **Then** it is refused, and nothing is stored
   (requirement 17). A reference resolves through the built-in `env:` or
   keyring resolver (R1Q17 (b)), and an endpoint that takes no credential
   declares the auth kind `none` (R1Q18 (a)).
5. **Given** no model configured, **When** the chat pane opens, **Then** it
   shows "no model configured" and how to configure one, before any turn. A
   turn is refused `model_capability_unavailable` before any process starts or
   any endpoint is contacted, and every other surface answers as it does with a
   model configured (requirement 17; R1Q10 (a): the other surfaces answer
   through openDox's own defaults).
6. **Given** a served repository whose bindings document holds a binding this
   machine has not trusted, such as one that arrived with a clone or was
   edited by hand, **When** a turn names it, **Then** it is refused by name,
   naming `opendox model-binding trust <id>`, before any broker runs, any
   credential reference is resolved or any endpoint is contacted. A binding
   declared through `opendox model-binding add` or `edit`, or trusted through
   `opendox model-binding trust <id>`, is reached as scenario 3 says
   (requirement 17 as T007's batch M note reads it; RULED `5962785556`, item
   2: *"Trust per machine (Recommended)"*), unless its command names a file
   inside the served repository. Such a binding is refused by name, naming
   the remedy, a broker installed outside the repository, both when trust
   would be recorded for it and before any process is spawned, even when it
   is trusted, and so is one whose program is a shell or an interpreter
   given an inline script (requirement 17 as T007's batch P note reads it;
   RULED `5982436447`, item 2: *"Refuse in-repo programs (Recommended)"*,
   and `5983805990`: *"Refuse inline scripts (Recommended)"*).

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
T093's procedure. F7.1 (at the phase-2 tip, T061) and 9.3's integration suite
pass, and F5.2 passes at the phase-3 tip, once T086 repairs its three pre-arc
reds (RULED `5962785556`).

**Acceptance Scenarios**:

1. **Given** openxFactory at a pin carrying the removal of 2.1, **When** its
   server is built, **Then** its five lane routes are served through the seam
   and the handler-contribution facet (R1Q1 (a), R1Q2 (a)).
2. **Given** every arc landing on openxFactory `main` since `94b6f7f1`, **When**
   F11.1 runs, **Then** each path touched is one of 11.1's surfaces, as
   widened to named composition tests by R1Q2 (a), and further to the seven
   admitted arc edits closed list RULED on `#656` comment `5890601202`
   ("Named closed list") — proved at T018 (phase 1) with `ARC_TIP`
   `f56c87c6`, both a PASS at that closed list and a FAIL on a planted
   eighth path never in it. The manifest differs only
   in `edits[].note` values, each added where an entry had none or extended,
   and none rewritten (requirement 1; R1Q20 (a), R1Q22 (a)).
3. **Given** openXdox installed in a fresh venv, **When** its validator lookup
   starts inside a planted pre-shed tree, **Then** it resolves the installed
   distribution's own validator, and its schemas are on disk (7.3; R1Q14 (a)).
   It closes in phase 2 (R1Q25 (b)), and every schema that install validates
   is on disk (R1Q27 (a)).

---

### Edge Cases

- A host registers AFTER an entry point registered the default. It replaces
  the default until a parser or server is built from it, and is refused
  `AlreadyRegistered` after that (R1Q3 (ii); RN-1 (a)).
- A governed host FORGETS to register, and gets a working-looking parser
  without its gate verbs. Its own start asserts its registration, so it
  refuses to start (R1Q4 (a)).
- A test file in openXdox-code needs `doc_health`. It is listed in the declared
  exclusion with its reason, and it is never silently skipped (R1Q6 (d)).
- A test file in openXdox-code needs openxFactory's contracts or its
  status-exemption rail, but not `doc_health`. R1Q24 (a) is ruled by class:
  the files of those two classes at T040's pin join the declared exclusion,
  each with its own reason, and the direction arc takes them. At `e28930bf`
  there were seven, and T005's experiment found an eighth behind a residue
  failure (T043).
- `tests/test_snapshot.py` needs no `doc_health`, yet fails in a lone
  checkout until 7.3 locates its schemas. It joins the declared exclusion with
  its own reason until 7.3 lands in phase 2 (R1Q25 (b)), and T061 clears the
  entry.
- The install mode is unset and `--local` is not given, so the install is
  hosted and refuses without its issuer (R1Q15 (b), 13.5). A flag and a
  setting that disagree are refused, naming both. No answer rules that case,
  and the refusal is the plan's fail-closed reading (T070). A local install
  asked to bind beyond loopback is refused with no opt-in (13.4).
- A plain document declares a `stage:` value that is not one of the six role
  keys. The value is not a declaration: the generate verb reports it, naming
  the document, and reads the document as a source, so no other value reaches
  the neutral snapshot (T054 in process and T056 through the verb; R1Q13 (a)
  with (c)).
- A raw key appears inside an endpoint URL, not in a field (16.3).
- A repository someone else wrote carries a committed bindings document whose
  broker runs a command, or whose `env:` reference names one of the user's
  secrets. Nothing runs and nothing is read until the user trusts that exact
  binding on this machine, and an edit, a copy under another root or a clone
  is untrusted again (16.3a, T100).
- The plain repository yields no grouping, candidate or selection tile, so the
  chat pane cannot be opened at all. The fixture declares at least one group,
  and a repository with no front matter still yields one from shared topics
  (R1Q13 (a) with (c)). AT-R1 fails, and does not skip, if it does not.
- The served model-catalog route imports openxFactory's `doxbench_contracts`
  by name today, so it fails closed without them (research R15). From T027,
  in phase 1, it resolves its validators through a seam, and fails closed
  naming that seam when nothing is registered. From T085 on, a standalone
  install validates with openDox's own packaged validators, and the route
  answers (R1Q10 (a), R1Q12 (a)).
- Lane 4's C3 edited 7.3's file and moved openxFactory's openXdox pin, and C4
  wrote the openXdox pin runbook. Both have landed. The arc starts from them
  and never duplicates them (plan.md § "In-flight overlaps").

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
  SHALL build on it when no host has registered, and a profile a host
  registers before anything is built from the default SHALL replace it. Both
  defaults are entry-point registrations (R1Q3 (a)). A registration after a
  build is refused, as RN-1 (a) rules (`5850003126`), and T007's batch D put
  that into the scenario text (#1170 → `79a720a2`). An EMPTY
  default stays refused: the default contributes openDox's own verbs (R1Q4
  (a), R1Q5 (a)). The carve manifest's `deleted_at_carve` row SHALL stay
  byte-identical.
- **FR-003** (requirement 5; 4.1, 4.1a, 4.2, 4.3; F4.1): every deferred reach
  into openxFactory or openXdox SHALL resolve through a seam openDox declares.
  With nothing registered, it SHALL refuse, naming the seam and the remedy. The
  home corpus SHALL be registered by the entry point (openDox's
  `LocalGitCorpus`) unless a host registered its own. `consumer_reach.py` SHALL
  be retired with its last name. Placement: the eight reaches into openxFactory
  in phase 1, and the nineteen into openXdox no later than the phase whose
  surface calls them (R1Q9 (a); R1Q10 (a): each such seam has an openDox
  default that the entry points register, and openXdox contributes its
  governed one).
- **FR-004** (requirement 4; 5.0–5.6; F5.1, F5.2, F5.3): openDox SHALL generate
  its own neutral snapshot over `CorpusAdapter` and `LocalGitCorpus`,
  rendering the six ruled words. It SHALL declare a generator seam. openXdox
  SHALL keep its governed generator and contribute it through that seam, with
  its projection unchanged (R1Q11 (a): the neutral snapshot's contract is
  openDox-spec's own; R1Q13 (a) with (c); R1Q23 (a); R1Q7 (a); R1Q26 (a):
  the governed values go to openXdox's facet, whose two protected tests are
  edited with their reasons).
- **FR-005** (requirement 7; 7.0–7.3; F7.1, F7.2): openDox's validator and the
  schemas it reads SHALL be on disk in one installed checkout. The input set is
  narrowed to openDox's own kinds first, and no intent-plane or governance
  schema is vendored. openXdox's validator lookup SHALL resolve through its
  installed distribution, with no parent walk (R1Q12 (a): openDox's four kinds
  ship as digest-checked package data; for 7.3, R1Q14 (a), in phase 2 by R1Q25
  (b); R1Q27 (a): the other kinds only where the tree it runs from supplies
  their schemas).
- **FR-006** (requirement 9; 9.1–9.5; F9.1, F9.2): each leg's required check
  SHALL run its whole suite green in its own checkout. Where a check runs less
  than the whole suite, it SHALL declare the exclusion with its count and its
  reason, and report it as an open extraction (requirement 9, first scenario).
  - **openDox-code**: the whole suite, `tests_runtime/` included, run against
    the required job's database (R1Q8 (a)). No exclusion is declared.
  - **openXdox-code, for release 1**: the whole suite less the declared
    exclusion (F9.1 as amended by T007's batches B and F, and by batch J's one
    `--deselect` until T008 removes it). It holds the
    `doc_health` files (R1Q6 (d)), the files that reach openxFactory's
    contracts or its status-exemption rail (R1Q24 (a)), and
    `tests/test_snapshot.py` until 7.3 lands in phase 2 (R1Q25 (b)), each
    with its own reason. The exclusion stays an OPEN EXTRACTION until the
    direction arc (T008) lands. It is reported as open, and never as closed,
    including at the archive.
  - Behaviour that needs both legs SHALL be declared integration tests at the
    declared composition.
  - The margins SHALL be restored, with no skip carrying the gap. A skip that
    still defers `doc_health` becomes part of the declared exclusion instead
    (T044).
  - The pins SHALL advance by their owners' ordinary pin-sync acts (9.5).

  FR-006 is met for release 1 when both legs' checks pass as above. Requirement
  9 is fully met only once the exclusion is empty.
- **FR-007** (requirement 10; 10.1–10.3; F10.1): openDox SHALL declare one
  documented entry point, the `opendox` console script, which serves the whole
  browser surface from an openDox-only install; `opendox-runtime` stays as an
  alias (R1Q5 (a)). The openDox root's README SHALL document the single
  command, and the root SHALL NOT host it (R1Q5 (a); R1Q15 (b): the command
  passes `--local`).
- **FR-008** (requirements 12 and 13; 13.1–13.6; F13.1): the standalone install
  SHALL bring its own PostgreSQL, with one dialect and both DSNs. It SHALL
  offer an explicitly selected local single-user mode, loopback-only and with
  no broker, while the hosted mode stays unchanged and refuses without its
  issuer. The serving process SHALL report its own install shape (R1Q15 (b);
  R1Q16: the `opendox[local]` extra brings the bundled server, which the
  document server owns as its child and which stops with the entry point).
- **FR-009** (requirement 17; 16.1–16.6, 16.3a; F16.1): chat SHALL reach any
  OpenAI-compatible endpoint by URL, model name and credential reference, and
  SHALL refuse a raw key when it is declared. A credential SHALL travel only
  over `https://`, or over `http://` to `127.0.0.1`, `[::1]` or `localhost`,
  whether the built-in resolver resolves it (`5880893901`) or a broker mints
  it (`5890601202`). A binding that would send one over `http://` to any
  other host SHALL be refused when it is declared (`ENDPOINT_NOT_PRIVATE`).
  The request that presents a credential SHALL follow no redirect, and over
  plain `http://` it SHALL take no proxy, so the credential keeps that route.
  An endpoint that declares the auth kind `none` presents no credential and
  keeps whatever route it declares. This is #1144's requirement 17 as its
  batch-K note reads it (`5916000030`, item 1). A binding read from the
  served repository SHALL run a broker, or resolve any credential reference,
  only once the operator has trusted that exact binding on this machine. The
  trust SHALL live in the operator's own state (`OPENDOX_STATE_DIR`), never in
  the repository, keyed to the root's resolved path, the binding's id and a
  digest of its full record. `add` and `edit` SHALL record it, `trust <id>`
  SHALL record it after printing what will run and where the credential
  goes, and an untrusted binding SHALL be refused by name before any spawn,
  read or contact. Bindings stay committable. This is requirement 17 as its
  batch-M note reads it (`5962785556`, item 2; 16.3a). A binding whose
  command names a file inside the served repository SHALL be refused by
  name even when it is trusted, naming the remedy, a broker installed
  outside the repository, and so SHALL one whose program is a shell or an
  interpreter given an inline script, directly or through a common
  launcher such as `env` (`5984069416`). The program SHALL be a real file
  outside the served repository, and every path the command names, the
  program and each argument alike, SHALL be judged both as named and as it
  resolves, when trust is recorded and before any spawn, so a link or a
  `PATH` entry that leads inside, or an in-repo link that points outside,
  is refused. Every broker SHALL start with its working directory outside
  the repository and with an environment that points away from it: no
  `PWD` or `OLDPWD`, no variable whose value is a path inside it, and no
  path-list entry inside it. A program that runs code from its own
  arguments is an accepted release-1 limit. This is requirement 17 as its
  batch-P note reads it (`5982436447`, item 2, and `5983805990`; 16.3a). With no model
  configured, it SHALL show a "no model configured" state before any turn,
  and every other surface SHALL work. Exactly one module SHALL contact a provider (R1Q10 (a);
  R1Q17 (b): a built-in `env:` and keyring resolver in that module; R1Q18 (a):
  an auth kind `none`).
- **FR-010** (requirement 1; 11.0, 11.1; F11.1): release 1 SHALL move nothing
  out of openxFactory. Every realization landing SHALL carry `Arc:
  neutral-product-standalone-operability`, and bookkeeping SHALL NOT (R1Q20
  (a)). openxFactory's arc edits SHALL stay within 11.1's surfaces: its three,
  plus the named composition tests of R1Q2 (a) (R1Q22 (a)), plus the seven
  admitted arc edits closed list RULED on `#656` comment `5890601202`
  ("Named closed list") — a later phase extends that list only by a
  further ruling, never by edited guard code alone.
- **FR-011** (acceptance): release 1 SHALL pass AT-R1 (below) before its
  bookkeeping ticks the release-1 boxes.
- **FR-012** (process): no task SHALL start while a question in its
  `Blocked by:` line is open. Every realization PR SHALL name its task ids, the
  boxes it realizes, and the falsifier it ran, with the output quoted.

### Key Entities

- **Default profile**: openDox's own domain profile (documents and ideas), whose
  display words are `NEUTRAL_DISPLAY`'s (it declares no `DISPLAY` facet, so the
  absent facet renders them; `5851560764`), registered by the entry points (R1Q3
  (a)). It contributes openDox's own verbs, the runtime verbs through
  `RuntimeSubcommand` now (R1Q4 (a), R1Q5 (a)).
- **Handler contribution**: the facet R1Q1 (a) rules. A profile or extension
  declares the mixin classes whose methods its bindings name, and
  `build_server` composes them into `BoundDashboardHandler`'s bases.
- **Declared exclusion**: openXdox-code's committed list of the test files that
  cannot run in a lone checkout, with its count and each entry's reason,
  reported as an open extraction. Its reasons are `doc_health` (R1Q6 (d)),
  openxFactory's status-exemption rail and its contracts (R1Q24 (a)), and the
  consumer's schemas until 7.3, for `tests/test_snapshot.py` alone (R1Q25
  (b)).
- **Home-corpus registration**: `corpus_adapter.register_home(factory)` and
  `home()`, plus `ADAPTER_NOT_REGISTERED`.
- **Generator seam**: the operation handed over, its registration point beside
  `domain_profile.register()`, and the conformance it requires (5.4).
- **Neutral snapshot**: the artifact openDox's generator writes. Its contract is
  a new openDox-spec schema, with the six role keys as its stage values (R1Q11
  (a), R1Q12 (a)).
- **Install mode**: `OPENDOX_INSTALL_MODE` (`local` | `hosted`, default
  `hosted`), which the documented command's `--local` also selects (R1Q15
  (b)), and its `install` block on `/capabilities`.
- **Model binding**: the doxBench record, which grows from nine fields to ten
  (`model`) and gains the `openai-chat-v1` dialect and the auth kind `none`
  (R1Q18 (a)).
- **Binding trust**: the operator's record, under `OPENDOX_STATE_DIR` and never
  in a repository, that this machine has accepted one exact binding: the
  served root's resolved path, the binding's id and a digest of its full
  record (16.3a; `5962785556`, item 2).
- **Arc landing**: a commit on a repository's `main` first-parent line that
  carries the `Arc:` trailer. It is what 5.4a's, 12.5's and 11.1's guards read.
- **Pin pair**: a gitlink plus its `contracts/*-pin.yaml`, moved in one commit.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001** (phase 1 exit): at the phase-1 tip, F2.1, F3.1 and F9.1 (in both
  legs) exit 0, each as amended where T007 records an amendment. F9.2 is run
  and quoted red until T008, as US1's independent test records (RULED
  `5859927858`).
  `opendox --help` exits 0, and F4.1's scan lists only `openxdox` targets.
  RN-1 (a) is in requirement 3's text (T007's batch D, #1170 → `79a720a2`),
  and T016 matches it.
  - openDox-code's suite goes from 0 passed today to whole and green.
  - openXdox-code's goes from 57 collection errors to green over the whole
    suite less its declared exclusion (R1Q6 (d), R1Q24 (a), R1Q25 (b)). The
    exclusion is reported as an open extraction, as FR-006 says.
- **SC-002** (phase 2 exit): F5.1, F5.3, F7.1 and F7.2 exit 0. F5.2 is run and
  quoted red on three pre-arc tests until T086, and exits 0 at phase 3's exit
  (SC-003; RULED `5962785556`, item 1). F5.2 runs
  as T007's batches C, F, G and K amend it (R1Q23 (a); `5916000030`, item 4:
  its last step passes `--chains`), and F7.1 runs here
  because R1Q25 (b) keeps 7.3 in phase 2, read as batch I records R1Q27
  (a).
- **SC-003** (phase 3 exit): F4.1, F5.2, F10.1, F13.1 and F16.1 (with T007's
  batch M line, whose named file holds batch P's A2 cases too) exit 0, and
  the F4.1 scan prints
  `no deferred reach names the consumer or the publisher`.
- **SC-004**: AT-R1 passes, and its evidence is recorded in this feature's
  `evidence/` directory.
- **SC-005**: after each phase's openxFactory landings, an interim F11.1 run
  (`PACKET_MERGE=94b6f7f1`), with the guard as widened by T007's batch A,
  prints `requirement 1 holds`.
- **SC-006**: at release-1 close, 65 of release 1's 70 boxes are ticked, each
  with its evidence:
  - 63 by T097;
  - 3.0, by the ratification record (#1151);
  - 5.6, which was already `[x]`.

  The other four (9.5, 11.0, 11.1 and F11.1) are performed in every phase, but
  left open for the arc's close after release 2. F9.2 stays open until T008,
  because RULED `5859927858` keeps it red on the help-tree test until then
  (holder decision, 2026-09-29, at T049).
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
2. **Only openDox installed.** openDox-code is installed as `opendox[local]`
   (R1Q16 (iii)), and nothing else.
3. **A plain git repository.** Two repositories are used, each copied into a
   fresh `git init`:
   - (a) 5.0's `plain-documents` fixture;
   - (b) a directory of ordinary `.md` files with no front matter at all.
4. **Opens.** The ONE command the openDox root README documents,
   `opendox generate-and-open --local …` (R1Q15 (b)), serves the bundle on
   loopback. Whether or not `--no-open` is given, the command writes a
   private copy in the state directory, `console/<port>.html`, and prints
   its location as a `file://` URL, never the token. Without `--no-open`
   it hands that copy to the browser. With `--no-open`, as this test runs
   it, the page is opened by loading the printed `file://` URL. Either way
   the copy forwards to the page with the console token in the URL's
   fragment. `/capabilities` carries no console token, so a request that
   needs one reads it from that copy (`5963851934`; T104, as T007's batch N
   records it at #1144's 12.4a).
5. **The wheel works.** `#tab-wheel` renders a tile for every document station
   the snapshot fills, and raises no `pageerror`.
6. **The radar lens works.** `#tab-lens` renders the bullseye with the corpus's
   documents as dots, and not the text "nothing on the radar". Neither of its
   two openxFactory seed actions is offered, since no binding answers them
   (R1Q19 (a)).
7. **The chat pane works.** From a grouping tile's `workbench` verb, the
   staging workbench opens, and its chat rail shows the "no model configured"
   state, naming how to configure a model, BEFORE any turn is attempted. A turn
   is refused `model_capability_unavailable`, and both editors stay usable.
   The rail's catalog and turn routes are guarded, so the page is the one
   step 4 opened through the private copy, carrying the console token.
   "Usable" means that each editor opens and accepts edits. On standalone,
   creating a document and Save are refused by name, since both go through
   openxFactory's create gate, which a standalone install lacks (T102). That
   refusal is declared to `tests/smoke_signals.py`'s oracle, so it is
   expected and not an error (RULED `5971834845`, *"Usable = edits; Save
   refused (Recommended)"*).
8. **No errors.** There are zero `pageerror` events. Every other console error
   or failed request is declared to `tests/smoke_signals.py`'s oracle, or the
   run fails. No route the three panes request answers 5xx.

The HTTP half (steps 1–4, and the route answers behind steps 5–8) runs in CI in
openDox-code (T095). It is a harness in its own `acceptance` job, which has no
database service, so its clean-machine assertions hold. The browser half is a
Playwright run on the host, with its verdict computed by the oracle (T096). CI
carries no browser: the oracle's own header records that *"CI has no `node`"*.
Neither half is a member of a leg's pytest suite: each installs the product and
drives it from outside, so FR-006 is unaffected.

## Assumptions

- Release 2 (Groups 6, 12, 14 and 15), Group 8 and F1–F4 are out of scope. The
  archive needs BOTH releases' evidence (`5800995035` answer 2), so landing
  release 1 archives and promotes nothing.
- The eleven answers of `5817152735` are applied, so phase 1 is planned on
  its answers.
- The fourteen answers of `5850003126`, and RN-1 (a), are applied in this
  revision: R1Q14, R1Q24 and R1Q25 by T019, R1Q10–R1Q13 and R1Q23 by T009, and
  R1Q15–R1Q19 by T069. R1Q21 (a) makes release 2 its own Speckit feature.
- R1Q26 (a) and R1Q27 (a), answered on `5851950767`, are applied by T067, in
  its own bookkeeping PR.
- Phases 2 and 3 are planned on their answers, and no step is conditional on
  an open question.
- Lane 4's own acts C1, C3 and C4 (`#656` `5815604830`, `5815613524`,
  `5815620605`) have all landed (#1152, #1153, openXdox-code#28, #1157 and
  #1154). This feature starts from them and duplicates none of them.
