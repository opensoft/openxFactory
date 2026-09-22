# Design — add-neutral-product-standalone-operability

Status: draft

This document carries the decisions behind the ten requirements, the ONE
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
`invert-opendox-consumer-dependency` (names one of ten requirements),
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
requirements with thirty scenarios are a standing property of any neutral
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
steps over **31 of the repository's 53 test modules** (30 + 1 + 6, reproducing
the pinned `MIN_SELECTED: 1114 / MIN_PASSED: 1111 / EXPECT_SKIPPED: 3` exactly);
**22 test modules are collected by no required command at all**. A green required
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
