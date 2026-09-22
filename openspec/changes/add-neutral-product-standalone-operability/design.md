# Design — add-neutral-product-standalone-operability

Status: draft

This document carries the decisions behind the sixteen requirements, the ONE
question this packet refuses to decide, and the measurements each rests on.
Every measurement is a command a reader can re-run; where a number is quoted,
the command that produced it is beside it.

## D1 — Why a new capability, and why this id

`neutral-product-standalone-operability` is ADDED rather than folded into an
existing capability, because none of the three candidates can hold it.

- `corpus-adapter-seam` governs the SEAM between openxFactory's corpus and a
  reader of it. It already forbids the reach this arc closes — *"no neutral
  product `openxFactory` pins SHALL import `openxFactory`'s own tooling"* — and
  that is exactly why the new requirements do not belong there: they are not a
  second statement of the prohibition, they are the POSITIVE PROPERTY the
  prohibition leaves unstated. A product can satisfy the seam's rule by having
  no features at all.
- `neutral-product-pin` governs openxFactory CONSUMING an external product: the
  pin, the digests, the fail-closed reader. It is the consumption direction. The
  new capability is its sibling in the other direction — what the product must
  be for the pin to be worth holding.
- `domain-descendant-boundary` governs a descendant of a neutral layer, one level
  further down.

The id was chosen to be READ correctly by someone who has not read this packet:
"neutral product" names the subject the corpus already uses in two capability
ids, and "standalone operability" names the property without naming openDox, so
that openXwallet and any future neutral product inherit it. Rejected: `add-opendox-build-arc`
(names an actor's work plan, not a property, and dies when the arc closes),
`invert-opendox-consumer-dependency` (names one of sixteen requirements),
`add-standalone-product-contract` ("contract" is already overloaded in this
corpus by `contracts/`).

## D2 — Why this packet is filed in openxFactory, and what ends the arrangement

The argument is in `proposal.md` § "Where this change is authored, and why".
Two points belong here because they are design, not justification.

**The choice was made against a measurement, not a presumption.** The lane's
brief permitted defaulting to openxFactory if openDox-spec's instance were
inoperable. It is not inoperable — `openspec validate --all --strict` exits 0
there over four changes. The instance is EMPTY, not broken, and the distinction
matters: a broken instance would be a defect to fix in openDox-spec, whereas an
empty one is a governance state the carve produced deliberately and has not yet
left.

**"The BUILD arc" names two different things, and this packet is the second.**
RULED OQ-N (`docs/opendox-cutover-runbook.md:2027-2031`) puts "the BUILD arc
(§ 3.5's FastAPI + Postgres runtime, § 3.6's repository-creation act)" in
openDox-spec's instance — and that arc is DONE, landed as openDox-code `#25` →
`aca94ecb` and `#26` → `4f8ae01e` on 2026-09-18, in openDox-code exactly as OQ-N
directed. The OTHER thing the same words name is the one
`src/opendox/consumer_reach.py` files as *"BUILD-arc work"* that *"does not exist
yet"* — the dependency inversion — and it is this packet's subject. The two are
cited by the same section numbers (§ 3.5 / § 3.6) throughout the tree, which is
why `conftest.py:34-39`, `pyproject.toml:150-154`, `runtime/cli.py:34`,
`docs/runtime.md:88` and `README.md:39` all say "the BUILD arc" and do not all
mean the same act. Recording the collision is part of this packet's work.

**The arrangement is designed to end.** Requirement 8's third scenario is the
exit: *"WHEN the extracted product's instance has promoted the requirements the
map assigned it → THEN subsequent work scoped to that product is authored in its
own instance, and the interim arrangement ends."* This packet is therefore
self-limiting by construction — it does not claim openDox's governance
permanently, it records that openDox cannot yet hold it and names the condition
under which it can.

## D3 — Why the gaps are REQUIREMENTS and not merely tasks

A gap list is an actor's inventory; it expires when the actor stops. Ten
requirements with sixty-seven scenarios are a standing property of any neutral
product this repository pins, and they outlive the arc. The concrete openDox
work is in `tasks.md`, one box per requirement, each naming the falsification
command — so the requirement states the property, the task states the act, and
the archive gate reads the command's output.

The requirements are written DOMAIN-NEUTRALLY and openDox is the measured
instance, which is the house form: `corpus-adapter-seam`'s own first requirement
carries *"The measured instance this rule is written from: twelve of
`scripts/ideation_dashboard/`'s forty-eight modules carry twenty-three
`scripts/doc_health/` imports…"*. Nothing in the ten names openDox, so a future
neutral product is bound without an amendment.

## D4 — G1's remedy is the carve's own design, not new design

`src/opendox/serve.py:199` and `:206` import `ideation_dashboard`, which exists
only in openxFactory. The remedy does not need inventing: the archived packet's
`design.md` already specifies it —

> "openDox keeps the server, static and canvas routes, chat and model routes and
> `/capabilities`; openXdox CONTRIBUTES snapshot, `/source` and projection routes
> through an EXTENSION POINT openDox exposes. Without the extension point the
> integration layer forks the server, which is a fork rather than a profile."

The seams exist in the tree today — `serve.build_server(route_extensions=)` and
`cli.build_parser(subcommand_extensions=)`, with openXdox-code already supplying
its half (`serve_gate.routes()`, `serve_projection.routes()`,
`cli_gate.GateSubcommands.register()`). What `serve.py:199` re-exports is neither
leg's: `serve_openxfactory_lanes` is OPENXFACTORY's lanes surface, filed
`stays_openxfactory_adapter`. So the remedy is the narrowest possible one — the
routes are contributed by openxFactory through the seam that already exists, and
openDox stops naming them. **No new mechanism is designed by this packet for G1.**

This is why requirement 2 is first among the gap requirements and why the arc is
not a rewrite. Re-measured at `f8a1ece` (an earlier sweep read 1188/1126; tests
landed since, so quote the head):

```
$ python -m pytest -q          # plain, root conftest active
11 skipped, 1298 errors in 120.52s
$ grep -c "No module named 'ideation_dashboard'" plain-pytest.log
1232
```

Zero passed. Every one of the 1,298 is a SETUP error rather than a collection
error, over 44 files, and one autouse fixture does it —
`tests/session_fixtures.py:413`, whose body is `from opendox import cli as
cli_mod`. CI is green anyway, because `validate.yml` runs three `--noconftest`
steps over a NAMED FILE LIST. **Re-measured for this packet at openDox-code
`f8a1eced`, by extracting the `run:` blocks that invoke pytest and stripping
shell comments** — an earlier reading of 31 of 53 counted only the three
`--noconftest` blocks over `tests/`, and a regex over the whole workflow
over-counted to 47 by matching comments:

```
run: blocks invoking pytest: 4
  block 1: files= 30  --noconftest=True
  block 2: files=  1  --noconftest=True
  block 3: files=  6  --noconftest=True
  block 4: files=  2  --noconftest=False
DISTINCT test modules actually named: 37
tree: tests/test_*.py = 53, tests_runtime/test_*.py = 10, TOTAL = 63
```

**So the figure this packet uses everywhere is 37 of 63**, and the three
`--noconftest` blocks reproduce the pinned `MIN_SELECTED: 1114 /
MIN_PASSED: 1111 / EXPECT_SKIPPED: 3` exactly. **26 test modules are named by no
pytest step at all.** A green required
check is not evidence that the product imports, and requirement 2's second
scenario exists to say so.

All of it is downstream of two import statements.

## D5 — G2's default profile does NOT re-own the composition point

The carve deleted `profile_openxfactory.py` — the manifest's single
`deleted_at_carve` row — on the stated ground that *"a composition point is not a
thing a core or a consumer can own"*, and `profile_proxy.py` deliberately refuses
rather than returning an empty tuple. Requirement 3 must not undo that, and it
does not. The distinction the requirement draws:

- **What the carve forbade** is a CORE carrying ANOTHER domain's profile.
  openxFactory's governance vocabulary in openDox's tree is what RULING C2
  refuses and what DIRECTION Q5 exists to prevent.
- **What requirement 3 asks for** is the core carrying ITS OWN domain's profile —
  documents and ideas, the domain the founding ruling gave openDox — as a
  DEFAULT that any host replaces by registering.

The third scenario is the guard: *"WHEN a host, consumer layer or domain
descendant registers a profile → THEN the registered profile replaces the default
for that process, so the default is a fallback and never a privileged path."*
That is the same shape `corpus-adapter-seam` already requires of openxFactory's
own adapter — one implementation among others, no privileged route.

The measured state requirement 3 closes: `build_parser()`/`build_server()` refuse
with `ProfileNotRegistered` until a host calls
`opendox.domain_profile.register()`, and openxFactory's
`scripts/opendox_host.py` is the only host that exists anywhere — grepping all
five repositories for `domain_profile.register(` finds it, two test harnesses
and nothing else. Worse for the standalone goal, that host's composite subclasses
**`openxdox.domain_profile.DomainProfile`**, so the only real profile in
existence needs BOTH siblings present. A product whose only host lives in the
repository it was extracted from is not extracted.

**Requirement 3 revisits the PREMISE of a ruling, and says so rather than
slipping past it.** The refusal is deliberate and ruled: RULED ASK-2 option (2)
(`#656` comment `5628886636`), and `profile_proxy.py` records the reasoning —
*"An empty tuple was refused by the ruling's own terms and by the failure mode: a
parser whose contributed verbs are silently absent is indistinguishable from a
working one until someone types the missing command."* That reasoning is correct
and requirement 3 does not touch it: **an EMPTY default is still refused.** What
requirement 3 changes is the premise the refusal rests on — the refusal text's
own words, *"openDox is the NEUTRAL product and ships no profile of its own"*.
This packet proposes that it should ship one FOR ITS OWN DOMAIN, which is a
different question from the one ASK-2 answered, and ratifying this packet is the
act that settles it. **If the ratification read takes ASK-2 to foreclose the
question, requirement 3 is the one to strike**, and the other nine stand without
it — openDox would then need a host shipped somewhere, and that is the same gap
under another name.

## D6 — Why G1 and G4 are separate requirements

They look like one gap and they are two, with different failure modes and
different falsification commands. Measured in `opensoft/openDox-code` at
`f8a1ece`, `PYTHONPATH=./src`:

```
$ python3 -c "import opendox.serve"
ModuleNotFoundError: No module named 'ideation_dashboard'     # G1: IMPORT TIME

$ python3 -c "import opendox.authoring"
(exits 0)                                                      # G4: import is CLEAN
```

`authoring.py:318`'s `from corpus_adapter_openxfactory import home_corpus` sits
INSIDE a function body, so the module imports cleanly and the failure waits for
the call:

```
$ python -c "import opendox.authoring as a; a.required_header_fields()"
ModuleNotFoundError: No module named 'corpus_adapter_openxfactory'
```

G4 is the more dangerous class for exactly that reason: it survives any
import-based health check, and it fails in front of a user. Requirement 2 covers
the import-time class and requirement 5 the deferred class, and a fix to either
leaves the other standing.

**G4 is also, precisely, a DECLARED CARVE EDIT THAT DID NOT LAND** — which is
why requirement 5 asks for no new design. `docs/opendox-carve-manifest.yaml`
carries the row already:

```yaml
  - source_path: scripts/ideation_dashboard/authoring.py
    disposition: moved_with_declared_edit
    destination_path: src/opendox/authoring.py
    edits:
      - class: adapter calls
        lines: [317, 318]
        note: "authoring.py:317-318 reaches corpus_adapter/corpus_adapter_openxfactory;
               the required-field vocabulary comes from the adapter's CLASSIFY
               operation (design D2)"
```

The edit class, the line numbers and the operation that answers are all named.
The file moved; the edit did not. And `corpus_adapter_openxfactory` itself has
**zero** rows in that manifest — `grep -c 'source_path: scripts/corpus_adapter_openxfactory'`
returns `0` — so it was never in carve scope, stays wholly at openxFactory, and
openDox names it anyway.

## D7 — What the arc measures itself against

The BUILD arc's progress has a number already in the tree, and this packet uses
it rather than inventing one: openXdox-code's
`tests/test_dependency_direction.py` carries a per-module ratchet
(`OPENDOX_BACK_IMPORTS`). `consumer_reach.py:11-13` quotes the historical figure
and dates it — *"Thirty-two calls survived the carve pointing the wrong way —
13 at import time and 19 deferred, over six modules, measured at `8e9ffa62`"* —
and the ratchet is **already lower**: today it declares `0` import-time and `19`
deferred over five modules, and `pytest tests/test_dependency_direction.py`
passes at the live tree and at the pin alike.

Two consequences this packet is built on:

1. **The consumer inversion is finished and is not re-proposed.** Requirement 2
   is not about `openxdox`; it is about `ideation_dashboard`, which no ratchet
   counts.
2. **No instrument watches the publisher direction.** The ratchet measures
   openDox → openXdox only. That is precisely how two import-time reaches into
   openxFactory survived a completed inversion with a green gate over them, and
   requirement 2's third scenario — a test that imports every module with NO
   sibling installed — is the instrument that would have caught them.

`consumer_reach.py` states the position this packet changes, in its own words:

> "THE REMEDY IS TO INSTALL openXdox — and only that, today … the injection that
> would make this reach disappear does not exist yet and is BUILD-arc work."

## D8 — Where the product entry point may lawfully live

Requirement 10 says a product must declare ONE documented entry point and does
not say where, deliberately — but the realization has exactly one lawful place
and the reason is worth recording, because the obvious place is refused.

`opensoft/openDox` is an openRepoShape assembly root. Its `Makefile` carries a
row in `contracts/shape-pin.yaml` (`:49-50`), and `AGENTS-shape.md` § "Never edit
a file that has a row in `contracts/shape-pin.yaml`" is unambiguous: *"every
sha256 is recomputed on every pull request. An edit in place is reported as DRIFT
and refused."* So a `run` or `serve` target at the root is not a small
convenience — it reds `make pins`, and the lawful route is an upstream change in
`opensoft/openRepoShape` propagated by its `update-shape.py`, which would bind
EVERY project carrying the shape.

The shape's own "What goes where" settles it the other way in one line: *"the
code leg | the implementation and its tests"*. And `README.md`, `AGENTS.md`,
`CLAUDE.md` and `project.yaml` carry NO shape-pin row and are the project's own
to edit. So:

- the entry point is a `[project.scripts]` console script at **openDox-code**,
  beside the existing `opendox-runtime` — and **this is already ruled**, not this
  packet's preference. `runtime/cli.py:40-46` records RULED Q-R4 (`#656` comment
  `5701772032`, Brett Heap, 2026-09-16, by interactive multi-choice): *"the verbs
  are wired into `opendox.cli` in the BUILD-arc act that repairs `opendox.serve`,
  and `opendox-runtime` is the spelling until then."* This packet IS the act that
  repairs `opendox.serve`, so Q-R4's condition is met here;
- the assembly root **documents** it in `README.md` and points at it;
- the root `Makefile` is not touched.

The measured starting position: `openDox/Makefile` is 23 lines with four targets
(`help`, `bootstrap`, `validate`, `pins`) and is **byte-identical to openXdox's**;
neither code leg has a Makefile at all; and the assembly README's only
instruction is `make bootstrap`, which its own text describes as putting each leg
on its pinned commit and running three validators. Nothing in either repository
starts a document tool, and the only containerized path —
`openDox-code/deploy/compose/`, whose `Dockerfile` ends
`CMD ["opendox-runtime", "runtime", "serve"]` — starts the runtime API on
`/livez`, `/readyz` and `/api/v1`, mounting no static files and serving no
document surface.

## D9 — RULED: the neutral submission step, and why it is not called "publish"

**RULED by Brett Heap, `#656` comment
[`5783934499`](https://github.com/opensoft/openxFactory/issues/656#issuecomment-5783934499),
2026-09-22T20:49:40Z, verbatim: "add a neutral publish step to the build arc".**
It enters the delta as requirement 11 — a NEW requirement, not an amendment to an
existing one, for the reason given under "Why not fold it into 4 or 5" below.

### The gap, re-measured here rather than accepted

RULING **C3** makes a standalone openDox a PLAIN LOCAL GIT REPOSITORY per
project with a remote attachable later, and the runtime honours it:
`src/opendox/runtime/repository_act.py:1131-1138`'s `attach_remote(store, *,
project_id, remote_url, executable="git")` takes ANY git remote and *"writes NO
object and moves NO ref … which is what makes the eventual move 'a push, not a
migration'."*

The document surface does not. `src/opendox/session_pr.py:297` is `class
GhPullRequests`, which shells out at `:367` with `args = ["gh", "pr",
subcommand]` against `_GITHUB_HOST = "github.com"` (`:233`). A pull request is a
hosting-platform artifact; a push is a git one. So the student on the plain local
repository C3 describes has no way to get a session's work out at all.

**One refinement, measured, that makes the requirement narrower and truer than
"there is no declared protocol".** A declared protocol ALREADY EXISTS:
`session_pr.py:98-99` is `@runtime_checkable class PullRequestPort(Protocol)`
with exactly three operations —

```
def push(self, branch: str) -> None: ...
def open_or_update(self, branch, *, base, title, body, ...) -> PullRequest: ...
def find_open(self, branch: str) -> PullRequest | None: ...
```

— and `FakePullRequests` (`:116`) is a second implementation. So three things are
true at once, and the requirement is written to all three:

1. **`push` is already neutral.** It is a git operation and needs no platform.
2. **The protocol is PLATFORM-SHAPED around the other two.** They return a
   `PullRequest` carrying `url` / `number` / `state`, and `number` is a platform's
   concept, not git's.
3. **The DEFAULT BINDING is the hard-wire, not the protocol.** `cli.py:812` and
   `serve.py:933` construct `GhPullRequests` by name, and `serve.py:1507` records
   that an unset injection *"builds the real `GhPullRequests`"*. There is no
   neutral implementation to fall back to — which is the same shape as
   requirement 3's missing default profile, one layer over.

So the arc does not invent a seam here any more than it did for the generator. It
supplies the missing NEUTRAL IMPLEMENTATION and stops the default binding naming
a platform.

### The invariant — RULED 2026-09-22T21:06:01Z, and deliberately REVERSED in part

An earlier draft of requirement 11 carried the absence below as binding text and
refused any merging implementation in a scenario. It was withdrawn while the
question was open, and **RULED on 2026-09-22T21:06:01Z** (`#656` comment
[`5784155201`](https://github.com/opensoft/openxFactory/issues/656#issuecomment-5784155201),
verbatim *"bundled postgres, local identity yes, merge yes, health in db"*):
**merge authority follows whoever governs the repository.** The hold is released
and requirement 11 now carries the rule and its three guardrails.

**What the ruling keeps and what it drops, stated precisely.** The absence was
never really about merging; it was SEPARATION OF DUTIES. That reading is kept
wherever a governance exists outside the tool — a governed host RESERVES landing
and routes it to that governance's own instrument, so openxFactory's flow is
untouched. What is dropped is the LETTER of the prohibition exactly where the
user IS the governance: forbidding a standalone owner to merge their own
repository protects nobody from anybody, and the student the founding ruling
describes would be left unable to finish their own work. The purpose survives —
**no tool merging behind its governance's back** — and the three guardrails are
what carry it once the absolute form is gone: explicit and human, conflicts
shown, and a merge that is a commit and therefore revertible. Each is its own
scenario, in EVERY mode, and none is configurable.

The text the absence is stated in, kept here because the guardrails are what now
does its work (`session_pr.py:17-23`):

> "**The absence is the enforcement.** There is deliberately no `merge`,
> `approve`, `review`, `self_review`, `bypass_protection`, `enable_auto_merge`,
> or any other operation that could land or bless a pull request — not on the
> protocol, not on the fake, not on the real adapter. A refusal message could be
> deleted by a later edit; a method that does not exist cannot be called at all.
> The merge is the Merge Master's action under the EXISTING ritual, enforced
> outside this dashboard by branch protection."

The question the ruling answered was whether that absence is CONSTITUTIONAL (true
of the product) or CONTEXTUAL (true of a governed install that does not own the
branch). **It is contextual**, and the guardrails are the constitutional part.
That is why requirement 11 does not say "openDox may merge" but *"landing
authority follows whoever governs the repository, and the product SHALL ASK the
repository rather than hard-coding either answer"* — hard-coding "always" would
be the same mistake as hard-coding "never", one governance further along.

### The name, chosen deliberately

The ruling says "publish step". **This delta does not use that word for it, and
the ruling's own naming note is why**: *"the proposal already uses 'publisher'
for the upstream that PUBLISHES a contract bundle, so the new step takes a word
that cannot be read as that one."* That collision is real in this packet's own
text — requirement 2 reads *"imports with no consumer, no **publisher** and no
host present"*, where "publisher" is the repository that publishes the corpus and
the contract bundle. A reader meeting "publisher" twice in one capability with two
meanings is a reader the capability has failed.

The word taken is **SUBMISSION**, and it is not a euphemism:

- it is the **fifth of the six ruled words** `NEUTRAL_DISPLAY` carries
  (`sources → groups → candidates → selections → submissions → completions`), so
  the arc names the step after the stage the product already says it reaches,
  rather than importing a new noun;
- it says what the act IS on a plain repository — the work is submitted somewhere
  — without claiming what the destination does with it, which "publish" (already
  taken) and "pull request" (platform-shaped) both do;
- and it stays accurate under the ruled answer: one SUBMITS work somewhere, and
  who may then land it is settled by who governs the repository. A word
  that implied the work had landed would prejudge the open item.

Rejected: `publish` (collides, as the ruling notes), `propose` (collides with
OpenSpec's proposal noun, which this corpus uses constantly), `share` (says
nothing about direction), `push` (names one implementation's mechanism as the
protocol, the exact error the requirement exists to correct).

### Why not fold it into requirement 4 or 5

Requirement 4 is the READ path — the product generating the artifact it serves.
Requirement 5 is about reaches that resolve through a declared seam. This is the
WRITE path leaving the repository, it has its own constitutional invariant that
neither of those carries, and it is separately satisfiable: openDox could
generate its own snapshot and still have no way to submit, or submit and still
serve nothing. The other ten requirements were already "ordered and separately
satisfiable"; folding this into one of them would break that and hide the open
merge question inside a requirement about something else. It shares requirement 4's
INJECTION SEAM, and says so rather than restating it.

## D10 — RULED: the standalone install's shape (four decisions, two of which AMEND founding rulings)

**RULED by Brett Heap, `#656` comment
[`5784155201`](https://github.com/opensoft/openxFactory/issues/656#issuecomment-5784155201),
2026-09-22T21:06:01Z, verbatim: "bundled postgres, local identity yes, merge yes,
health in db".** Two of the four AMEND founding rulings, and that is recorded
here rather than left for someone to discover.

### D10.1 — Bundled Postgres, one dialect. Consistent with Q2; no amendment.

Measured: `pyproject.toml:134` pins `psycopg[binary,pool]>=3.2`,
`deploy/compose/docker-compose.yaml:25` is already `image: postgres:16`, the
runtime refuses to start without `OPENDOX_DATABASE_URL`, and it keeps TWO DSNs —
`OPENDOX_MIGRATION_DATABASE_URL` for migrating and `OPENDOX_DATABASE_URL` for
serving, with `config.py` refusing to default one from the other (*"Silently
falling back to `OPENDOX_DATABASE_URL`"* is named as the thing not to do).
`grep -rli sqlite src/ migrations/` returns nothing.

The standalone install BRINGS the database rather than asking for one, and **no
SQLite dialect is added**. The reasoning is worth keeping: a second dialect
doubles every migration and every schema test forever, for a database that under
RULING Q1 holds no document. Bundling buys the same convenience once. Requirement
12's third scenario keeps the two DSNs from collapsing — a single-user install is
not a reason to serve from the migrating credential.

### D10.2 — A named local identity mode. THIS AMENDS RULING Q2.

**Q2 fixed OIDC through the Keycloak broker, and the code enforces it:**
`src/opendox/runtime/config.py:89-92` declares `OPENDOX_OIDC_ISSUER` REQUIRED —
*"the Keycloak broker's issuer, pinned: a token from any other issuer is refused
rather than trusted (RULING Q2)"*. A single user installing openDox for their own
documents cannot run a Keycloak.

The amendment is narrow and its narrowness is the point: a LOCAL SINGLE-USER MODE
needs no broker; the HOSTED MULTI-USER MODE keeps OIDC and the pinned issuer
exactly as today. **The mode must be selected explicitly and must not be
reachable by omission** — requirement 13's second scenario makes an unset issuer
in a hosted install a REFUSAL, not a downgrade. That scenario is the whole
safety of the amendment: a mode you can enter by forgetting to configure
something is not a mode, it is an unauthenticated multi-user install wearing the
word "local".

### D10.3 — Merge: see § D9, which the ruling released and rewrote.

### D10.4 — Health results in the database. THIS AMENDS RULING Q1's CLOSED LIST.

`migrations/0001_identity_and_coordination.sql:14` states: *"the table list below
IS the ruling's own list, and it is CLOSED"* — `users`, `memberships`,
`projects`, `project_repositories`, `sessions`, `drafts` — and
`tests_runtime/test_schema_shape.py:77` refuses a seventh with *"RULING Q1 names
six things the database owns; a seventh table is a claim about that boundary and
has to be made in the open."*

Health results become that seventh thing, and **the file itself names the only
lawful path** (`:22-28`): `0001` is applied verbatim behind a fail-closed
`CANONICAL_MIGRATION_SHA256`, so *"Changing the schema is therefore an ADDITIVE
`0002_…`/`0003_…` file, never an edit here"*.

**TWO CORRECTIONS TO THE INSTRUCTION, measured here, so the realization does not
trip on them:**

1. **It is `0003_`, not `0002_`.** `migrations/0002_migration_state.sql` ALREADY
   EXISTS — it declares the `opendox_schema_migrations` ledger. The next additive
   file is `0003_`.
2. **The closure test is scoped to the CANONICAL migration, and there is already
   a precedent for an additive table that does not disturb it.**
   `test_the_canonical_schema_declares_exactly_rulings_six_tables` reads
   `_declared_tables()` over `0001` only, which is why `0002`'s ledger table did
   not trip it (the test file notes at `:179` that it is *"bootstrapped by the
   runner and declared additively in 0002"*). So the closure test moves in the
   same change **only if the health table is declared a DOMAIN table** — one that
   enters `identity.TABLES`, which
   `test_the_store_declares_exactly_the_tables_the_ruling_names` separately holds
   to the ruling's six. If instead it is install-owned like the ledger, the
   precedent already exists and no closure text changes. **The realization must
   DECLARE which of the two it is and say why**, because that choice is the
   boundary claim the test exists to force into the open — and requirement 6's
   third new scenario is written to either answer.

**Q1's principle is untouched, and that is why the amendment is lawful rather
than merely permitted:** the database still holds NO DOCUMENT and stays
DISPOSABLE relative to the corpus, because health results are recomputable from
git. Requirement 6 says so directly, and requirement 15 protects the one thing
that is NOT recomputable.

### D10.5 — The neutral health check's families

Recorded as ruled: broken internal links, documents nothing links to,
near-duplicates, missing neutral front matter from the adapter's fields, a
declared stage that disagrees with where the document sits among the six ruled
words, and stale or empty stubs. On demand from the dashboard and the command
line, optionally on commit; reported where the human is working rather than filed
into an external tracker; baseline-relative; model-assisted checks only where a
model is configured. **openxFactory's 23 governance check families stay with
openxFactory**, which requirement 1 already states as a refusal.

## D11 — RULED: the fix loop, and the one thing that must not live in the database

**RULED by Brett Heap, `#656` comment
[`5784247356`](https://github.com/opensoft/openxFactory/issues/656#issuecomment-5784247356),
2026-09-22T21:12:34Z, verbatim: "1, add the fix loop to #1144"**, extending the
four decisions above. Requirements 14 and 15.

**The applier is genuinely new work, and the ruling measured that before ruling
it.** openxFactory's checker CLASSIFIES findings — `scripts/doc_health/__init__.py:17-18`
is `AUTO_FIXABLE = "auto-fixable"` and `CONTESTED = "contested"` — and
`grep -rln "def apply_fix\|def autofix\|def fix("` over `scripts/doc_health/`
returns NOTHING. Nothing in this estate applies a fix today. So requirement 14 is
not a generalization of an existing applier; it is the first one, and it is
openDox's rather than openxFactory's because openxFactory's findings are
governance findings whose repair is a governed act.

**Why the fix loop is two requirements and not one.** Requirement 14 is the LOOP
— where the human acts, the three resolution classes, and the rule that every
repair is a draft on a branch that lands only through the landing rule. Requirement
15 is the EXCEPTION, and it is separate because it is the only part that
contradicts D10.4: everything else about health belongs in the disposable store,
and an exception must not. Folding it into 14 would bury a rule that reverses the
one immediately above it.

**The distinction requirement 15 turns on.** A finding is DERIVED and recomputable
from the documents; an exception is a JUDGEMENT that exists nowhere else. The
database is disposable by Q1, so an exception stored there is *"a judgement
scheduled for deletion"* — and its finding would silently come back on the next
reset, which is the worst failure mode available: a decision that was made,
recorded, and then quietly unmade by an operational act. The committed
exceptions file follows the pattern of openxFactory's `health/dispositions.yaml`,
whose own semantics already match: `scripts/doc_health/families.py:370` reads
*"removing its health/dispositions.yaml entry re-opens"* the finding — which is
requirement 15's third scenario, in the estate's own words.

**Nothing auto-merges, and that is stated at its sharpest for the smallest case.**
The guardrails from § D9 apply to every repair of every class. Requirement 14's
fifth scenario refuses an automatic landing *"however small"*, with the reason:
a fix small enough to seem safe is exactly the one that gets applied unread. The
batching allowance is the pressure valve — many repairs, ONE draft, ONE human
review — so that "never automatic" does not become "never practical".

## D12 — RULED: the check-pack interface, and the layering it makes possible

**RULED by Brett Heap, `#656` comment
[`5784295745`](https://github.com/opensoft/openxFactory/issues/656#issuecomment-5784295745),
2026-09-22T21:16:17Z, verbatim: "1, add the pack interface to #1144"**, extending
`5784155201` and `5784247356`. Requirement 16.

### The layering this exists for

- **openDox** ships the NEUTRAL checks (§ D10.5's families) and they are ALWAYS
  ON. They are the ones that treat a document as a document.
- **openXdox** ships the xFactory GOVERNANCE pack — openxFactory's 23 families.
  This is what finally gives those families a home that is neither "stay in
  openxFactory forever" nor "move into the neutral core", which requirement 1 and
  RULING C2 both forbid.
- **Each DomainxFactory** ships its own pack, pinned in its `stack.yaml`, so
  MedxDox's clinical checks and codexDox's engineering checks are additions
  rather than forks.

That is the same shape RULING C2 gave the domain-mapping core — *"parameterized
by a domain profile that a descendant supplies"* — applied to checks instead of
vocabulary, and it is why the pack contract lives in openDox on the
`corpus_adapter` Protocol pattern rather than being invented somewhere new.

### Why the engine/pack split falls where it does

A pack supplies WHAT IS CHECKED. The engine owns WHAT THE USER RELIES ON: the
resolution surface and its CLI parity, scheduling, the baseline, storage
(results derived, exceptions committed), and the fix loop with its landing rule.

The hard line is the one requirement 16 states as a refusal: **a pack cannot
redefine the resolution classes, the baseline rules, or who may land work.** Those
three are exactly the guarantees §§ D9–D11 spent their arguments on. If a pack
could vary them, every one of those guarantees would become conditional on which
packs an install happens to carry — and a user could not reason about their own
tool without auditing its plugins. The guardrails follow from the same principle:
**a pack reads and returns; only the engine writes.** A pack that writes has
escaped the draft-on-a-branch rule, the explicit-human-act rule and the
revertible-commit rule in one step.

Two more, each measured against a failure this estate has already had. **A pack is
pinned by commit and digest** — the `neutral-product-pin` discipline, because an
unpinned pack silently changes what a corpus is judged against, which is the same
hazard as an unpinned validator. And **a pack that crashes or times out becomes a
finding against that pack** rather than taking the run down: the doc-health
nightly's analysis child failed silently every night from 2026-08-30 (openxFactory
`add-worker-input-budget`'s own origin note), and a health check whose failure
mode is silence is worse than one that reports itself broken.

### The pack id and version go in NOW, and why that is a schema decision

Requirement 16 puts a PACK ID and PACK VERSION on every finding, and the ruling is
explicit that this lands in **the same additive migration as the results table**
so the table is not migrated twice. Beyond avoiding a second migration it earns
its place three ways: a finding can be ATTRIBUTED to the pack that raised it; a
pack can be UPGRADED without its history becoming ambiguous; and the BASELINE can
tell a genuinely new finding from one that merely arrived with a new pack version
— which is the case that would otherwise make every pack upgrade look like a
regression.

**The migration number, restated because the instruction said `0002`:** that file
exists already (`migrations/0002_migration_state.sql`, the
`opendox_schema_migrations` ledger), so the additive file is **`0003_`**, and the
pack columns go in THAT one beside the results table. The instruction's substance
— one migration, not two — is honoured exactly; only the number moves. See
§ D10.4 for the measurement.

### Scope, stated so nobody builds the wrong half here

**IN this packet:** the interface, its guardrails, and the pack id/version on
every finding. **NOT in this packet, and named in the proposal's follow-ons:**
porting openxFactory's 23 families into the openXdox governance pack is an
openXdox FOLLOW-ON with its own claim, and each domain's pack is that domain's
own work. This packet authors neither, and requirement 1 still keeps the 23
families with openxFactory until that follow-on lands.

## R-G3 — RULED: openDox gets its own neutral generator

**This section asked a question until 2026-09-22T20:08:59Z. It now records an
answer.** RULED by Brett Heap, openxFactory `#656` comment
[`5783335210`](https://github.com/opensoft/openxFactory/issues/656#issuecomment-5783335210),
interactive in the lane session, verbatim:

> **"yes, openDox gets its own neutral generator"**

Requirement 4 is written to that ruling. What follows is the position the
question was asked from, the three options as they were put, what was ruled, and
**one correction to this packet's own earlier analysis**, recorded because the
analysis was wrong in a way that mattered.

### The position the question was asked from

openDox serves a snapshot it cannot generate. The generating half is in
openXdox-code: `generator.py` (974 lines, `generate_snapshot`), `snapshot.py`
(223, `write_snapshot`, `find_validator`), `snapshot_registry.py` (1,318),
`completeness.py` (548) and `corpus_root.py` (101) — **3,164 lines over five
modules**, reached back from openDox late-bound through `consumer_reach.py`,
whose refusal text names the remedy as *"BUILD-arc work"* that *"does not exist
yet"*.

It was placed there by a ratified DESIGN READING, not by a ruling naming it.
DIRECTION Q5 says so in its own last paragraph: *"The per-module assignment is
therefore design work under this test … **not ruled here module by module**."*
The reading was then settled in three agreeing places — the carve proposal's
`code_surface`, its `design.md` module assignment, and the 102-row map, where all
eight requirements of the *projection and snapshot* cluster read as openXdox.

What RULING C2 binds is the vocabulary, and it binds it in both directions
(`#656` comment `5544370242`, 2026-09-04T17:47Z), verbatim:

> "**openXdox is the domain-mapping core, parameterized.** … **parameterized by
> a domain profile that a descendant supplies.** Engineering vocabulary
> ("requirement", "OpenSpec change", the doc-health check families) belongs to
> the engineering descendant `codexDox`, or stays in openxFactory as its own
> adapter over the corpus-adapter interface; a clinician using `MedxDox` never
> sees the word "requirement"."

### The three options, as they were put

**(a) Move the generator into openDox as it stands.** Fastest; openDox generates
immediately. Contradicts C2's principle and accepts Q5's named failure — every
descendant inherits a core speaking openxFactory's nouns and forks it.

**(b) The protocol injection AND a small neutral-side generator openDox writes
for itself.** Direction reversed lawfully, every ruling intact, but two
generators over the same kind of artifact and a standing drift liability.

**(c) Move the generator into openDox parameterized by a domain mapping
declaration.** One generator, every ruling intact, the parameterized core C2
describes — at the cost of auditing and re-expressing ~30 corpus-shaped literal
sites across 3,164 lines. **This packet recommended (c).**

### THE CORRECTION — (a) and (c) were both worse than this packet said

The recommendation was right and **its stated reason was incomplete, in a way
that would have misled the ruling had it gone the other way.** This packet
measured the corpus-shaped PATH LITERALS in `generator.py` and priced (a) as
*"low engineering, high governance"*. It did not measure the imports. They are at
`src/openxdox/generator.py:66-68`:

```
from doc_health import corpus
from doc_health.corpus import RealGit
from doc_health.lines import split_keepends
```

**`generator.py` imports openxFactory's `doc_health` package directly.** So
option (a) was never merely a governance cost: relocating that file into openDox
would have put `import doc_health` inside the neutral core, which is the exact
thing `corpus-adapter-seam`'s first requirement forbids — *"no neutral product
`openxFactory` pins SHALL import `openxFactory`'s own tooling"* — and would have
traded one wrong-way dependency for a deeper one. Option (c) carries the same
defect in smaller print: parameterizing the path literals does not remove the
`doc_health` imports, so (c)'s audit was larger than this packet priced it at.

The governance vocabulary is heavier than the ruling's own figures too. The
ruling records `staging` ×63, `proposal` ×17, `openspec` ×12, `ratified` ×5,
`ideation/` and `Status:` ×4. Re-measured independently at openXdox-code
`ab04453`, case-insensitively over the whole file: **`staging` 72, `proposal` 19,
`openspec` 18, `ratified` 6, `ideation/` 4, `Status:` 4.** The direction is
identical and the magnitude is larger. Nothing in the ruling is contradicted;
this packet's own pricing is.

### What was ruled, and what it means mechanically

openDox does **not** take `generator.py`. Instead:

**One precision the review forced, and it is worth keeping.** "Through the same
seam" is true of the PATTERN and false of the REGISTRATION POINT. The submission
seam already exists — `serve.py:766`'s `pull_request_factory`, called at
`:931-932`, described at `:1505` as *"the same kind of seam"* — so requirement 11
repoints its unset DEFAULT rather than inventing anything. The generator seam
requirement 4 needs does NOT exist and § 5.4 declares it. They are two interfaces
built the same way, not one interface serving both, and saying otherwise would
leave neither implementable.

- **openDox grows a SMALL NEUTRAL PROJECTION** over the `CorpusAdapter` protocol
  it *already declares* — `src/opendox/corpus_adapter.py`, a
  `@runtime_checkable` `Protocol` (`:280`) with six closed members (`resolve`,
  `list_documents`, `read`, `classify`, `check`, `write_back`), whose own
  docstring at `:27` says *"This interface travels to openDox"*. The seam is not
  designed by this arc; it is used by it.
- **`runtime/local_git_adapter.py`** (2,796 lines, RULING C3's plain local git
  repository) is the conformant implementation openDox already has, so the
  neutral projection has something real to read on day one.
- **openXdox KEEPS its governed generator** and hands it in through the same
  seam. It loses nothing; the publisher's corpus is projected exactly as today.

That is the injection `consumer_reach.py` describes and says does not exist:
*"openDox naming a protocol and being handed an implementation."* The protocol
exists. The implementation exists. What has never been built is the projection
that uses them, and that is requirement 4's subject.

**Why this is better than the option this packet recommended.** (c) would have
re-expressed 3,164 lines of someone else's governed code and still had to sever
three `doc_health` imports. The ruled path writes a small amount of new neutral
code against an interface that already exists, and leaves the governed generator
where its vocabulary belongs. It is (b)'s shape without (b)'s duplication
complaint, because openXdox's generator is not a second copy of openDox's — the
two read different corpora by construction.

### The constraint that comes with it

**RULED, same comment, decision 2, verbatim: "keep those six words".**
`NEUTRAL_DISPLAY` in `src/opendox/display_profile.py` stands unchanged —
**`sources → groups → candidates → selections → submissions → completions`** —
ratified as the standalone product's own vocabulary. The neutral projection
renders these and no others; this arc designs no new workflow and re-authors no
word. `display_profile.py:72-80` already argues why they are the right ones: a
shell rendering them is *"VISIBLY not rendering a domain's"*, and a student who
installs openDox alone *"gets a working funnel"*. Requirement 3's fourth scenario
carries this as a general rule so a future neutral product inherits it.

### The sibling slice, in flight — do not duplicate it

**RULED, same comment, decision 3, verbatim: "wire the views and land it"**, and
CLAIMED in the same comment on `opensoft/openDox-code` by actor `viewwire`: the
hardcoded governance spellings in `src/opendox/web/views/` become role lookups
through the display facet, and `views/lens.js` joins it. Measured in that claim:
six of seven views already import `views/display.js` but still carry literal
`stage-brainstorm` / `stage-staged` / `stage-realized` names; `lens.js` imports
it not at all. Both halves of the facet — `display_profile.py` on the server and
`views/display.js` on the client — are already built and need no design.

**This packet does not own that slice and does not list it as owed work.** It is
referenced so that whoever takes group 10 does not author it twice. The ruling is
explicit that the generator is not in that claim: *"The generator itself
(decision 1) is NOT in this claim — it is the BUILD-arc proposal's subject and
comes back for its own word."*

### What is still open after the ruling

Nothing in requirement 4. The arc's remaining open question is the smaller one
this packet already flags at § D5: whether requirement 3's default domain profile
is foreclosed by RULED ASK-2, which answered a different question about an EMPTY
default. That is a ratification read, not a separate ruling request.
