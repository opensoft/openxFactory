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

## Q-G3 — THE ONE QUESTION FOR BRETT: where does the snapshot generator live?

**This packet does not decide this and requirement 4 is deliberately written to
the outcome so that it is satisfied by whichever answer is ruled.**

### The position today, and why it is not an oversight

openDox serves a snapshot it cannot generate. The generating half is in
openXdox-code: `generator.py` (974 lines, `generate_snapshot`), `snapshot.py`
(223, `write_snapshot`, `find_validator`), `snapshot_registry.py` (1,318),
`completeness.py` (548) and `corpus_root.py` (101) — **3,164 lines over five
modules**, reached back from openDox late-bound through `consumer_reach.py`.

It is there by ruling, not by accident. **RULING C2** refuses placing
openxFactory's vocabulary in the neutral layer; the promoted
`domain-mapping-declaration` spec states the refusal and its reason:

> "**WHEN** `openxFactory`'s nine-word `Status:` taxonomy, its change/spec/delta
> nouns or its doc-health families are placed in the neutral layer rather than in
> the engineering descendant's declaration — **THEN** the placement is refused
> under RULING C2, because a clinician using a descendant would then see the word
> 'requirement'."

**DIRECTION Q5** is the same rule stated as a failure mode: a neutral layer that
hardcodes one domain's status words, artifact nouns or act verbs *"SHALL be
reported, because every other descendant then forks it — which is the failure
DIRECTION Q5 was given to prevent."*

And the generator does carry that vocabulary. Measured in openXdox-code at
`ab04453` — the corpus-shaped literals are real code, not comments:

```
$ grep -nE 'openspec|ideation/|proposal\.md|tasks\.md|spec\.md' src/openxdox/generator.py
240:    base = repo_root / "openspec" / "changes"
264:    tasks = folder / "tasks.md"
278:    path = folder / ".openspec.yaml"
443:    proposal = folder / "proposal.md"
   … 311-316: the `ideation/staging/` topic rule
```

Roughly thirty such sites across the five modules, plus one `Status:`-taxonomy
literal in `generator.py`. So moving the generator AS IT STANDS into openDox
would place openxFactory's artifact model in the neutral layer, which is what C2
refuses and Q5 was given to prevent.

### The options

**(a) Move the generator into openDox as it stands.**
openDox generates immediately and the arc closes fastest. But openxFactory's
artifact model — `openspec/changes/`, `proposal.md`, `tasks.md`,
`.openspec.yaml`, `ideation/staging/` — lands in the neutral core, which is
precisely the placement RULING C2 refuses. It requires AMENDING C2 and accepting
Q5's named failure: MedxDox and codexDox inherit a core that speaks
openxFactory's nouns, and each forks it. **Cost: low engineering, high
governance — a ratified ruling is amended and the descendant story is the one Q5
exists to prevent.**

**(b) Build the protocol injection: openDox declares a generator protocol,
openXdox implements it.**
The direction is reversed lawfully; no ruling is amended; the consumer keeps its
vocabulary. **But this does NOT by itself make openDox standalone**, and that
should be said plainly: a seam with no neutral-side implementation leaves openDox
still unable to generate anything when installed alone. It converts a
`ModuleNotFoundError` into a well-worded refusal. It satisfies
`corpus-adapter-seam`; it does not satisfy requirement 4 or the owner's goal
unless openDox ALSO ships a default generator — at which point the real question
is what that default generator is, which is option (c). **Cost: moderate
engineering, NO governance cost — and it leaves the owner's question unanswered.**

**(c) [RECOMMENDED] Move the generator into openDox PARAMETERIZED BY A DOMAIN
MAPPING DECLARATION, and leave openxFactory's vocabulary in openXdox's
declaration.**
The generator's corpus-shaped literals become reads of the declaration's ARTIFACT
KINDS and LIFECYCLE axes; openXdox supplies openxFactory's declaration and keeps
its corpus adapter; openDox ships a declaration for its own domain — documents
and ideas — and generates over it with no consumer installed.

This is not a new mechanism. It is the mechanism `domain-mapping-declaration`
was promoted to provide, in its own words: *"the neutral layer SHALL be
parameterized by it rather than shipping any one domain's words"*, with the five
axes named — artifact kinds, lifecycle vocabulary, acts and gates, evidence
classes, promoting authorities. A generator's `proposal.md` / `tasks.md` /
`spec.md` / `.openspec.yaml` / `ideation/staging/` literals ARE artifact kinds,
and the declaration's first axis is where they belong.

It is also a technique this estate has already executed and ruled on. Carve
slice **S7** (RULED Q1/Q2/Q7, `#656` comment `5648049748`, Brett Heap
2026-09-12) did exactly this to the front end: *"parameterize class C — every
governance word in the fourteen class-C files and the four declared class-A tails
becomes a read of the registered domain's DISPLAY facet BY ROLE"*. The generator
is the same job on the server side, against a declaration axis instead of a
display facet.

**Cost: the largest engineering item of the arc — five modules, 3,164 lines, ~30
literal sites to audit and re-express — but ZERO governance cost: C2 and Q5 are
SATISFIED rather than amended, and every descendant gets the parameterized core
Q5 was written to guarantee.** It also subsumes (b): the seams stay, openXdox
keeps contributing its routes and subcommands, and the declaration is what
travels instead of the vocabulary.

### The recommendation, and what makes it refutable

**(c).** It is the only option that answers the owner's question — *can openDox be
self-contained as a research and document tool?* — with YES, without amending a
ratified ruling. (a) answers YES by amending C2. (b) answers NO while making the
failure polite.

What would change the recommendation: if the ~30 literal sites turn out on audit
to be load-bearing on openxFactory's SEMANTICS rather than its PATHS — that is,
if the generator does not merely walk `openspec/changes/` but reasons about what
a change MEANS — then the parameterization is authoring a second product rather
than re-expressing a first, and (b) plus a smaller purpose-built neutral
generator becomes the cheaper honest answer. The audit is the first task of the
G3 box and its result is recorded there BEFORE any code moves.

### What this packet does without the ruling

Requirement 4 stands and is falsifiable under any option: *"a snapshot is
generated over a corpus of plain documents carrying none of the publishing
repository's governance vocabulary, with no consumer installed."* Every other
requirement is actionable on ratification and none of them waits on Q-G3.
