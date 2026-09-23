---
code_surface: openxFactory, openDox-code, openXdox-code and openDox — (openDox is the assembly root; its leg repositories are named separately because each carries its own arm of the realization.) THIS PACKET AUTHORS NO CODE BYTE, and it declares a real one. Landing here is corpus text only: this packet's five files (`proposal.md`, `design.md`, `tasks.md`, `.openspec.yaml` and ONE `## ADDED` spec delta), one README *Active changes* bullet, and the machine-seeded per-change row in `tests/sequenced_after/corpus-ledger.yaml` that every filing owes. The REALIZATION the requirements specify runs post-ratification, in FOUR repositories — the three that gain code, plus openxFactory for annotation only — and each arm is a named task with its own claim: in `opensoft/openDox-code`, the removal of the two module-level `ideation_dashboard` imports at `src/opendox/serve.py:199,206` and their replacement by the route-extension seam the carve's `design.md` already specifies, a default domain profile so `build_parser()`/`build_server()` start with no host, the resolution of `src/opendox/authoring.py:318`'s `corpus_adapter_openxfactory` reach through the registered adapter, a document validator and a health check over its own documents, a `[project.scripts]` entry point for the document surface, THE NEUTRAL SUBMISSION DEFAULT that lets a plain git repository get a session's work out (RULED `5783934499`), and the removal of its `validate.yml` exclusions; in `opensoft/openXdox-code`, the consumer half of the RULED G3 shape — openXdox keeps its governed generator and injects it through openDox's declared seam (`#656` `5783335210`) — plus the `OPENDOX_BACK_IMPORTS` ratchet driven down as each reach closes; in `opensoft/openDox` (the assembly root), one documented start target; and in `openxFactory`, NOTHING BUT the carve-manifest annotations that record each closed reach — no check family, no schema, no corpus document and no `scripts/` module moves, per this packet's first requirement. NOT THIS CHANGE'S SURFACE, and named so no reader infers it: the re-promotion of the 71 requirements the carve's map assigns to openDox is openDox-spec's own act and is tracked as a BLOCKED task here, not authored here; the document surface is NOT rewritten, re-architected or re-scoped; and no pin, gitlink, contract bundle or release tag moves.
target_release: implemented — the affected repositories' main lines (openxFactory, openDox-code, openXdox-code, openDox). `implementation_pending` was the honest-looking word and it is NOT in the ratified vocabulary, which admits `implemented`, a release this estate defines, or `deferred-allocation`; the deferral this packet needs is carried by the CODE SURFACE, not by this token. Under `release-realization`'s archive gate a change with a NON-EMPTY code surface "SHALL NOT archive until realization evidence exists: its code merged on the implemented target through the owning domain's engineering gates, and — where the surface is runnable — a green run of that surface", so this packet stays ACTIVE as approved-but-unrealized intent until the arc is built. The evidence is per requirement: the falsification command named in that requirement's `tasks.md` box, run in a checkout holding only the repository under test, quoted with its output. No contract bundle is cut, no bundle number is allocated or reserved, and no release tag is owed — this packet moves no contract byte.
sequenced_after: []
---

# Proposal: add-neutral-product-standalone-operability

Status: draft
Authored: 2026-09-22, in lane `openxfactory-4` (display
`openXfactory-4-openDox_extraction`), actor `buildarc`, as the BUILD ARC the
archived packet `split-opendox-two-layer-product` names as its own unclosed
residue.
Directed by: Brett Heap, asking this lane on 2026-09-22 whether openDox can be
self-contained as a research and document tool, and what it has versus
openxFactory.
Authoring method: hand-authored against a MEASURED state. Every fact in this
proposal was produced by running something in a fresh clone, and the command is
given beside the claim so a reader can refuse it. No `opsx:propose` alignment
review or council debate was run: the design decisions are settled by the
archived packet's own rulings. The ONE that was not settled at filing was put to
Brett as a named question rather than decided here — and it was RULED the same
day, so `design.md` § R-G3 now records a decision, the options as they were put,
and a correction to this packet's own analysis of them.

FILING IS NOT RATIFYING. All three lifecycle documents carry `Status: draft`,
`.openspec.yaml` declares drafting provenance with NO approval pair, and nothing
here admits text to canon. Ratification is a separate act on Brett Heap's word.

## Why

**The owner's goal, in his own words.** The founding ruling on
[`opensoft/openxFactory#656`](https://github.com/opensoft/openxFactory/issues/656)
(Brett Heap, 2026-09-04, recorded verbatim) says what openDox is for:

> "we will make openDox work to just manage documents and ideas. it will keep
> the integration with git and notebook lm etc and have all tools that help for
> document management and ideation."

and what it is:

> "we do not have a place to store projects. If i want to start a new project in
> a new repo, and make some specs, we have no good place to store my projects. I
> think we need to make this an app that installs and is hosted with a db. we
> should have users and projects and can expand the feature set."

Six hours later, **DIRECTION Q5** (`#656` comment `5542993375`,
2026-09-04T15:48Z) gave the standalone test in the owner's own words — and it is
the sentence this packet exists to satisfy:

> "we want to make openDox useful on its own, it shoudl be able to still manage
> docs and do brainstorming and connect to notebook lm. it is domain neutral and
> external from openXfactory. … a student could use openDox or a lab assistant.
> so we want that to still be useful on its own"

Q5's first layer reads it back as a test a module can be held to: *"openDox must
be useful alone to a student or a lab assistant … would someone with no notion
of factories, gates or tenants use it?"* Brett said the same thing again on
2026-09-06, captured in openXdox-spec PR #3's brainstorm set: *"openDox support a
complete standalone editing and collaboration workflow -yes."*

**Half of that is built and works. The other half does not import.** openDox-code
is two products in one repository, and they are in opposite states. Both facts
are one command each, in a checkout of `opensoft/openDox-code` at `f8a1ece` with
`PYTHONPATH=./src`:

```
$ python3 -c "import opendox.runtime.cli"
(exits 0)

$ python3 -c "import opendox.serve"
  File ".../src/opendox/serve.py", line 199, in <module>
    from ideation_dashboard import serve_openxfactory_lanes  # noqa: E402
ModuleNotFoundError: No module named 'ideation_dashboard'
```

`opendox.runtime` is the app the ruling asked for and it is real: one console
script `opendox-runtime`, the verbs `runtime init|migrate|serve|status|reset`
and `project create-repository|attach-remote|push`, six tables (`users`,
`memberships`, `projects`, `project_repositories`, `sessions`, `drafts`),
FastAPI + Postgres + OIDC, compose and Kubernetes manifests, and a
database-backed suite green in CI. The carved DOCUMENT surface — the part the
ruling describes as "manage documents and ideas… all tools that help for
document management and ideation" — cannot be imported at all.

**The failing import is the owner's own named integration, and it is two lines.**
`ideation_dashboard` is a package that exists only in openxFactory; the carve
manifest files it `stays_openxfactory_adapter`, reaching neither leg. An AST
census of `src/` finds exactly **two import-time reaches, both in `serve.py`
(`:199` and `:206`), plus two deferred ones** — every other mention in the
package is prose. The five names `:206` re-exports are plain route strings:

```
COMMITTED_INTENTS_ROUTE            = "/committed-intents.json"
ACTIONS_REFRESH_ROUTE              = "/actions/refresh"
ACTIONS_APPLY_REGISTER_EDITS_ROUTE = "/actions/apply-register-edits"
ACTIONS_DTN_SEED_ROUTE             = "/actions/dtn-seed"
ACTIONS_STAGING_SEED_ROUTE         = "/actions/staging-seed"
```

From those two lines follow: `src/opendox/cli.py` failing through
`serve.py:199`; `src/opendox/notebook_action.py` failing through its own `:52`
`from .serve import resolve_source_path` — so the "Open in NotebookLM" tile
action, one of the two integrations Brett named by name, is unreachable in the
repository that owns it; and **1,232 of the 1,298 errors** a plain
`python -m pytest -q` produces in openDox-code at `f8a1ece`, where the passing
count is zero.

**And openDox cannot simply vendor the module it is missing.**
`scripts/ideation_dashboard/serve_openxfactory_lanes.py` itself does
`from openxdox import snapshot_registry` (`:70`) and
`from openxdox.serve_projection import hosted_ref_refused` (`:77`), so copying it
into openDox would re-create the consumer dependency BUILD slice 2b removed. The
routes have to be CONTRIBUTED through the seam, which is what the carve's own
`design.md` already specifies.

**This is not a new policy question. It is a ratified requirement the carve left
unsatisfied.** `openspec/specs/corpus-adapter-seam/spec.md`, promoted by the
archive of `split-opendox-two-layer-product` on 2026-09-22, already says it:

> "no neutral product `openxFactory` pins SHALL import `openxFactory`'s own
> tooling. The dependency points ONE WAY — a reader depends on the interface it
> implements, and never on the corpus's own check families"

with the scenario *"A neutral product imports the corpus's own tooling → THEN
the import is refused"*. openDox is a neutral product openxFactory pins, and it
imports openxFactory's own tooling in two places.

**Be precise about which direction is unclosed, because one of them IS closed.**
The inversion openDox → openXdox — the reach into its CONSUMER — was driven to
zero at import time by BUILD slices 2 and 2b, and the gate that proves it passes
today. openXdox-code's `tests/test_dependency_direction.py` carries the ratchet:

```
OPENDOX_BACK_IMPORTS: dict[str, tuple[int, int]] = {
    # module                        (import-time, deferred)
    "opendox/branch_session.py":    (0, 7),
    "opendox/cli.py":               (0, 1),
    "opendox/serve.py":             (0, 2),
    "opendox/serve_project.py":     (0, 2),
    "opendox/serve_workbench.py":   (0, 7),
}
```

Thirteen import-time reaches became **zero**; nineteen deferred ones remain. What
is NOT closed is two other things, and this packet is about them:

1. **The reach into the PUBLISHER.** `ideation_dashboard` and
   `corpus_adapter_openxfactory` are openxFactory's, not openXdox's. No ratchet
   counts them and no gate measures them, which is how they survived a completed
   consumer inversion.
2. **The nineteen deferred reaches into the consumer**, which are lawful as
   late-bound calls and are exactly what makes openDox unable to stand alone.
   `src/opendox/consumer_reach.py` says so in its own refusal text — *"THE REMEDY
   IS TO INSTALL openXdox — and only that, today … The injection that would make
   this reach disappear — openDox naming a protocol and being handed an
   implementation — does not exist yet and is BUILD-arc work."*

**Both legs' required checks are green, and that is the problem.** openDox-code's
`validate.yml` names **37 of its 63 test files** and clears its floor with zero
margin (`1114/1111/3`); openXdox-code names **16 of 85** and clears `539/533/6`,
also with zero margin. Both figures were re-measured for this packet at
openDox-code `f8a1eced` and openXdox-code `ab04453d` by extracting the `run:`
blocks that invoke pytest and stripping shell comments — the method, both
measurements, and why an earlier reading said 31 of 53 and 20 of 85, are in
`design.md`. Run whole with `python -m pytest -q`, openDox-code produces **1,298
errors and zero passed** and openXdox-code **1,089 errors and zero passed**, 57 of
its 85 files failing collection.
And every one of openXdox's six skips carries the same reason — *"doc_health
reachability is BUILD-arc work (§ 3.5/3.6) … this test will assert for real once
that lands"* — while two of openDox's three are its mirror image. **The
whole-product assertions are precisely the ones that skip.** A green required
check is not evidence that the product runs, and requirement 9 exists to say so.

**And the structural fact, which is why this cannot be closed by deleting two
import lines.** openDox serves a snapshot it cannot generate. `generate_snapshot`,
`write_snapshot`, `find_validator`, `corpus_root`, `snapshot_registry` and
`completeness` all went to openXdox at the carve, reached back from openDox
late-bound through `consumer_reach.py`, whose docstring states the position in
terms: *"THE REMEDY IS TO INSTALL openXdox — and only that, today."* A user who
installs openDox alone gets a reader with nothing to read. **Where that generator
should live was the one question this packet did not answer, and Brett ruled it
on 2026-09-22: openDox gets its OWN neutral generator and openXdox keeps its
governed one** — see § "The question this packet asked, and the ruling that
answered it" below, and `design.md` § R-G3.

## Where this change is authored, and why — a finding

This packet is filed in **openxFactory's** OpenSpec instance and not in
openDox-spec's. The lane's brief said to default here if openDox-spec's instance
were not operable. **It IS operable**, so the default did not fire and the choice
needed an argument. Measured, in a fresh clone of `opensoft/openDox-spec` at
`8fe8c4c`:

```
$ OPENSPEC_TELEMETRY=0 openspec validate --all --strict
Totals: 4 passed, 0 failed (4 items)          (exit 0)

$ OPENSPEC_TELEMETRY=0 openspec list --specs
No specs found.
```

The instance validates. It has `openspec/project.md`, a `validate` workflow that
runs `--all --strict` on every pull request, and four changes in flight. What it
does not have is a single promoted requirement, and that is what decides this:

1. **openDox-spec can hold no delta this arc needs.** Its `openspec/specs/` is a
   `.gitkeep`; its `openspec/changes/archive/` is a `.gitkeep`; it has ratified
   and archived nothing. The CLI refuses the operation on its own three changes
   already, in terms: *"target spec does not exist; only ADDED requirements are
   allowed for new specs. MODIFIED and RENAMED operations require an existing
   spec."*
2. **The requirements this arc builds on are promoted HERE.** `corpus-adapter-seam`
   (4 requirements), `domain-mapping-declaration` (3) and `release-realization`
   (17) are in openxFactory's `openspec/specs/`. A delta can only be authored
   where its target spec lives.
3. **The arc binds openxFactory-owned artifacts.** `ideation_dashboard`,
   `corpus_adapter_openxfactory`, `scripts/opendox_host.py` and
   `profile_openxfactory.py`'s `deleted_at_carve` row are openxFactory's, and the
   arc discharges against openxFactory's `docs/opendox-carve-manifest.yaml`. A
   change filed in openDox-spec cannot bind openxFactory.
4. **openDox-spec's own charter forbids it.** Its `openspec/project.md`: *"Proposals,
   specs and changes in this instance describe **this leg's** scope only."* A
   dependency inversion spanning four repositories is not this leg's scope only.
5. **The front-matter grammar this packet must carry exists only here.**
   `code_surface:` and `target_release:` are `release-realization`'s, and that
   capability is promoted in openxFactory.
6. **The adjudicated validation gate exists only here.** openDox-spec's CI installs
   `@fission-ai/openspec@1.2.0` directly; openxFactory pins 1.12.0 through
   `contracts/openspec-cli-pin.yaml` and adjudicates findings against ratified
   `dispositions:`. The corpus grammar this packet is validated under is
   adjudicated in openxFactory alone.

**The strongest argument AGAINST this placement, and the answer to it.**
`docs/opendox-cutover-runbook.md:2027-2031` records **RULED OQ-N**, which names a
BUILD arc and puts it elsewhere:

> "the CARVE arc is § 3.2–3.4, § 3.7's arrival and § 3.8's `carved_from`
> bookkeeping; the BUILD arc (§ 3.5's FastAPI + Postgres runtime, § 3.6's
> repository-creation act) follows, **as openDox-code's own changes under
> openDox-spec's own OpenSpec instance.**"

Read it precisely and it does not reach this packet. OQ-N names the arc by its
two boxes — § 3.5 and § 3.6 — and **that arc is finished**: § 3.5 landed as
openDox-code `#25` → `aca94ecb` and § 3.6 as `#26` → `4f8ae01e`, both on
2026-09-18, both as openDox-code's own changes exactly as OQ-N directed. The
runtime it built is the half of openDox that works. **This packet is a different
arc under the same word** — the dependency inversion and the standalone entry
point, spanning four repositories and modifying requirements promoted in
openxFactory's corpus. That the word "BUILD arc" names two things is itself a
finding, recorded here and in `design.md` § D2 so the next reader is not caught
by it.

OQ-N's direction is nonetheless honoured, twice over: the code it governs is
authored in the legs' own repositories, as `tasks.md` groups 2–10 say in terms;
and requirement 8's third scenario hands governance of openDox back to
openDox-spec the moment that instance can hold it.

**And the emptiness is not benign — it has already stalled openDox-spec's own
backlog.** Three of its four active changes carry `## MODIFIED Requirements`
blocks against `ideation-dashboard`, a spec that does not exist in that
repository, so **they can never be archived**. The loop is open at both ends:
nothing can be promoted because nothing has been archived, and nothing can be
archived because nothing has been promoted. Its gate cannot see this — both spec
legs pin `@fission-ai/openspec@1.2.0`, and run against the same tree 1.2.0 emits
NONE of the three *"Archive would refuse this delta"* notices that the 1.12.0
line this repository pins reports.

**That openDox cannot yet govern its own BUILD arc is itself the gap this packet
carries as G7**, and the requirement *"An extracted product's own spec instance
governs its requirements before the product is called standalone"* names the
succession: once openDox-spec has promoted the requirements the carve's map
assigns it — **68 of the 71 appear nowhere in that repository today** — work
scoped to openDox is authored there, and this arrangement ends.

## What is already built, and is not proposed again

An arc that opens on a half-built product must say what is already standing, or
it proposes work someone has done. Measured, not assumed:

- **The runtime is complete and already standalone.** An AST walk over every
  `.py` under `src/opendox/runtime/`, function bodies included, yields no import
  of `ideation_dashboard`, `corpus_adapter_openxfactory` or `openxdox`. All eight
  verbs answer `--help`, and `opendox-runtime runtime status` refuses correctly
  on a missing DSN rather than crashing. Nothing in this packet touches it.
- **The openDox → openXdox import-time inversion is DONE.** Thirteen import-time
  back-reaches became zero under BUILD slices 2 and 2b (openDox-code `#9` →
  `da8aae96`, `#10` → `0f1f2e59`), and openXdox-code `#13` → `01357c8` lowered the
  ratchet to zero. The gate passes today. This packet does not re-propose it.
- **The corpus-adapter INTERFACE already exists in openDox.**
  `src/opendox/corpus_adapter.py` is a `@runtime_checkable` `Protocol` with six
  operations — `resolve`, `list_documents`, `read`, `classify`, `check`,
  `write_back`. Requirement 5 does not design a seam; it asks that a verb USE the
  one that is already there.
- **The two extension seams exist and openXdox already supplies its half.**
  `serve.build_server(route_extensions=)` and
  `cli.build_parser(subcommand_extensions=)`, with `serve_gate.routes()`,
  `serve_projection.routes()` and `cli_gate.GateSubcommands.register()` on the
  consumer side. Requirement 2's remedy uses them.
- **The CORPUS interface is already declared on both sides; the GENERATOR
  handoff is not, and it is new work.** `src/opendox/corpus_adapter.py` is a
  `@runtime_checkable` `Protocol` with six closed members through which a
  projection READS a corpus, and `src/opendox/runtime/local_git_adapter.py`
  (2,796 lines, RULING C3's plain local git repository) is a conformant
  implementation openDox already ships — which is why the ruled projection is
  small. **Neither of them is a generator seam**: `CorpusAdapter` is closed at six
  members and none of them hands a generator over, so task 5.4 declares that seam
  as new work (`design.md` § R-G3). Requirement 4 asks for the projection that
  reads through the corpus interface, not for either of them.
- **A neutral, profile-parameterized corpus reader already exists** at
  openXdox-code `src/openxdox/domain_corpus_adapter.py`, answering the
  conformance corpus 17 of 17 (`#23` → `3ee8cd39`). It is at the consumer leg, so
  openDox reaching it would be a new back-import — but it is evidence that a
  profile-parameterized neutral reader is a shape this estate has already built
  once, and openDox's own projection (requirement 4) is the same shape on its own
  side of the seam.

**One correction this packet owes the record.** openDox-code's `README.md:39-42`
says `validate` is narrowed *"Until the BUILD arc … inverts the openDox →
openXdox dependency"*. That reason is now false — the dependency IS inverted at
import time. What narrows `validate` today is `ideation_dashboard`, a different
name entirely. The correction is task 9.1's, not this packet's.

## What Changes

ONE `## ADDED Requirements` block creating the capability
`neutral-product-standalone-operability` — sixteen requirements, sixty-nine scenarios.
The capability is the sibling of `neutral-product-pin`: that one governs
openxFactory CONSUMING an external neutral product; this one governs the product
being able to STAND UP without its consumer. It is written domain-neutrally and
applies to every neutral product openxFactory pins; openDox is the measured
instance it is written from, exactly as `corpus-adapter-seam` is written from
its own measured instance.

The requirements, with the gap each answers — requirement 1 is the guard and
answers no gap, requirements 2-9 answer G1-G8, requirement 10 answers both G9 and
G10, and requirements 11-16 are the rulings of 2026-09-22 — each separately
satisfiable and each falsifiable by a command named in `tasks.md`:

| # | Requirement | Gap | Falsified by running |
|---|---|---|---|
| 1 | Making a neutral product standalone moves no corpus, no governance instance and no check family | — | the guard: every commit carrying the arc's trailer, diffed across the whole repository against an allow-list |
| 2 | A neutral product imports with no consumer, no publisher and no host present | G1 | `python -c "import opendox.serve"` in an openDox-only checkout |
| 3 | A neutral product ships a default profile for its own domain, and the composition point stays open | G2 | `opendox --help` with no host registered |
| 4 | A neutral product produces its own primary artifact with no consumer installed **(RULED)** | G3 | generate a snapshot with `openxdox` absent |
| 5 | A deferred reach into the publisher or the consumer resolves through the declared seam | G4 | call the authoring verb with no `corpus_adapter_openxfactory` on the path |
| 6 | A neutral product carries a health check over its own documents, and corpus-operations families stay with the corpus | G5 | run openDox's health check in an openDox-only checkout |
| 7 | A neutral product validates its own documents from a single checkout | G6 | run openDox's validator over a document, one checkout |
| 8 | An extracted product's own spec instance governs its requirements before the product is called standalone | G7 | `openspec list --specs` in openDox-spec |
| 9 | Each repository of a split product runs its own suite to green in its own checkout | G8 | each leg's suite, no exclusions, no sibling |
| 10 | A neutral product declares one entry point that starts the whole product | G9, G10 | install, run the one documented command, reach the browser surface |
| 11 | A session's work leaves the local repository through a declared submission protocol with a neutral default **(RULED)** | — | submit a session on a plain git repo with `gh` not installed |
| 12 | A standalone install brings its own datastore, and the product keeps one dialect **(RULED)** | — | install on a machine with no database and start |
| 13 | A standalone install has a named local identity mode, and a hosted install cannot fall into it **(RULED)** | — | start local with no broker; start hosted with no issuer and get a refusal |
| 14 | A health finding carries a resolution path, and every fix lands through the landing rule **(RULED)** | — | repair a finding; the default branch must not move |
| 15 | An exception is a human decision and lives in the corpus, never in the derived store **(RULED)** | — | reset the store; the exception still holds |
| 16 | Health checks extend through pinned packs, and the engine owns what must not vary **(RULED)** | — | run with a crashing pack registered; the others still report |

**What this packet deliberately does NOT propose.** It is not a rewrite. The
document surface is not re-architected, its routes are not re-scoped and its
80K-line inheritance is not revisited — the arc REVERSES A DIRECTION and adds a
front door, and every requirement above is satisfiable without changing what the
surface does. It does not re-home a single doc-health check family. It does not
re-promote the 71 requirements the carve's map assigns to openDox; that is
openDox-spec's own act and is carried here as a BLOCKED task with its
precondition named. It moves no pin, no gitlink, no contract bundle and no
release tag.

## Three more rulings, the same evening — and two of them amend founding rulings

**RULED** [`5784155201`](https://github.com/opensoft/openxFactory/issues/656#issuecomment-5784155201)
(2026-09-22T21:06:01Z, *"bundled postgres, local identity yes, merge yes, health
in db"*) and [`5784247356`](https://github.com/opensoft/openxFactory/issues/656#issuecomment-5784247356)
(21:12:34Z, *"1, add the fix loop to #1144"*). Full measurements in `design.md`
§§ D10–D11.

**Bundled Postgres, one dialect (requirement 12).** The standalone install brings
its own database so a user installs the product and not a database. **No SQLite
dialect** — a second dialect doubles every migration and every schema test
forever, for a store that under RULING Q1 holds no document; bundling buys the
same convenience once. The two DSNs survive: a single-user install is not a
reason to serve from the migrating credential, and `config.py` already names the
silent fallback as the thing not to do. *Consistent with Q2; no amendment.*

**A named local identity mode (requirement 13) — AMENDS RULING Q2.** Q2 fixed
OIDC through the Keycloak broker and `config.py:89-92` enforces it by making the
issuer REQUIRED. A single user cannot run a Keycloak. The amendment is narrow and
the narrowness is the point: local single-user needs no broker, hosted
multi-user is unchanged, and **a hosted install cannot fall into local mode by
omission** — an unset issuer stays a REFUSAL. That scenario is the whole safety
of the amendment, because a mode you can enter by forgetting to configure
something is an unauthenticated multi-user install wearing the word "local".

**Health results in the store (requirement 6, amended) — AMENDS RULING Q1's
CLOSED TABLE LIST.** `migrations/0001` says the six-table list *"is CLOSED"* and
`test_schema_shape.py:77` refuses a seventh *"in the open"*. Health results become
that seventh thing by the only lawful path the file itself names — an ADDITIVE
migration, never an edit to `0001`, which is applied verbatim behind a
fail-closed SHA-256. **Two corrections this packet measured:** it is `0003_`, not
`0002_` (that file exists — the migration ledger), and the closure test is scoped
to the CANONICAL migration, so it moves only if the health table is declared a
DOMAIN table; the `0002` ledger is the precedent for the other answer. The
realization DECLARES which, and why. **Q1's principle is untouched**: the store
holds no document and stays disposable, because results are recomputable from git.

**The fix loop (requirements 14 and 15).** Detection without resolution is a list
that grows. A Health view with **CLI parity**, three resolution classes
(`auto-fix` for the mechanical findings, `assisted`, `human-only` — the ruled
spellings, one per class everywhere), and **every repair written as a draft on a
branch that reaches the default branch only through the landing rule above** —
**nothing auto-merges, not even a one-line fix**, with batching as the pressure
valve. The applier is genuinely new: openxFactory CLASSIFIES findings
(`AUTO_FIXABLE`/`CONTESTED`) and `grep` finds no code anywhere in
`scripts/doc_health/` that applies one.

**And the one thing that must NOT live in the store (requirement 15).** An
exception is a human judgement that exists nowhere else; a finding is derived and
recomputable. The store is disposable by Q1, so an exception kept there is a
judgement scheduled for deletion, and its finding would silently return on the
next reset. Exceptions are committed to the corpus on the pattern of
`health/dispositions.yaml`, whose semantics already match —
`families.py:370` reads *"removing its health/dispositions.yaml entry re-opens"*
the finding.

**The check-pack interface (requirement 16)** — RULED
[`5784295745`](https://github.com/opensoft/openxFactory/issues/656#issuecomment-5784295745)
(21:16:17Z, *"1, add the pack interface to #1144"*). Health checks become
extensible: a PACK supplies check families, findings in the neutral shape and
optional patches, with its labels through the display facet; **the ENGINE owns
the view and its CLI parity, scheduling, the baseline, storage and the fix loop**,
and **a pack cannot redefine the resolution classes, the baseline rules, or who
may land work** — those are the guarantees §§ D9–D11 exist to give, and a pack that
could vary them would make every one conditional on which plugins an install
carries. Guardrails: a pack READS and RETURNS, only the engine writes; a pack is
pinned by commit and digest; and a pack that crashes or times out becomes a
FINDING AGAINST THAT PACK rather than taking the run down.

**This is what finally gives openxFactory's 23 families a home** that is neither
"stay in openxFactory forever" nor "move into the neutral core", which requirement
1 and RULING C2 both forbid: **openXdox ships the xFactory governance pack**, each
DomainxFactory ships its own pinned in `stack.yaml`, and openDox's neutral checks
are always on. Every finding carries a PACK ID and PACK VERSION, landing in the
SAME additive migration as the results table so it is not migrated twice.

### Follow-ons named here and deliberately NOT authored here

- **Porting the 23 families into the openXdox governance pack** — an openXdox
  follow-on with its own claim. Until it lands, requirement 1 keeps them with
  openxFactory.
- **Each DomainxFactory's own pack** — that domain's own work.
- **The view-wiring slice** — claimed by actor `viewwire` and LANDED as
  openDox-code#35 → `3c3a9e31`.
- **The `display_profile.py` docstring alignment to `completed`** — in flight as
  openDox-code#36, prose only.

## What openxFactory keeps, and why this is not a land-grab

Stated plainly, because an arc that makes one repository standalone reads from
the other side like an extraction, and this one is not.

- **The corpus.** Every document under `ideation/`, `docs/`, `contracts/` and
  `openspec/` stays. The founding ruling settles it: *"The seam openxFactory
  keeps is the corpus itself and its governance; what moves to openXdox is the
  code that reads it."*
- **The OpenSpec instance.** 66 promoted capabilities, 180 archived changes, 43
  active. Nothing in this arc touches `openspec/specs/` except to ADD the one
  capability this packet declares.
- **The doc-health check families.** Not one moves, and the measurement says
  there was never much to take: stripping comments and docstrings so only
  executable code counts, exactly ONE of `scripts/doc_health/`'s 37 Python
  modules is free of openxFactory/OpenSpec identifiers — `lines.py`, 133 lines of
  31,437, or 0.4%. About 13 mix a reusable mechanism with hard-coded corpus
  identifiers and about 23 are corpus operations by subject. At the granularity
  that actually matters — the 23 registered check families, each a
  `fam_<id>(ctx)` entry in `families.FAMILIES` — the tally is **0 pure TOOL, 6
  BOTH, 17 CORPUS-OPS: there is no pure-tooling check family at all.** **There is
  no extractable generic doc-health core.** Requirement 6 is therefore satisfied by
  openDox growing its own check over its own declaration, which is new neutral
  code, not a relocated family — and requirement 1 states that as a refusal
  rather than a promise.
- **The adapter column.** `ideation_dashboard`, `corpus_adapter_openxfactory`
  and `scripts/opendox_host.py` stay, and the carve manifest already files them
  `stays_openxfactory_adapter`. The arc does not delete them: it stops openDox
  IMPORTING them. openxFactory continues to call openDox — that direction is
  lawful and is the whole point of the seam.
- **The intent-plane schemas** and **the integration tests**, including the three
  NotebookLM sync tests that RULING OQ-B kept here on the ground that *"NotebookLM
  sync is openxFactory machinery"*. They are openxFactory tests that import
  openDox, which is the correct direction and is not touched.
- **`scripts/sync-notebooklm-books.py`** (150,771 bytes) stays. The owner's
  "integration with notebook lm" that openDox owns is the tile action
  (`src/opendox/notebook_action.py`, already carved across); the corpus-wide
  projection sync is openxFactory's and remains so.

The one openxFactory-side change this arc contemplates is **annotation**: the
carve manifest gains a row note for each closed reach, so the ledger records
that the direction was reversed and when. No behaviour, no family, no schema.

## The question this packet asked, and the ruling that answered it

**G3 was an open question when this packet was filed. It was ruled six hours
later and requirement 4 is written to the ruling.** Brett Heap, openxFactory
`#656` comment
[`5783335210`](https://github.com/opensoft/openxFactory/issues/656#issuecomment-5783335210),
2026-09-22T20:08:59Z, verbatim: **"yes, openDox gets its own neutral
generator."**

openDox does **not** take openXdox's `generator.py`. It grows a small neutral
projection over the `CorpusAdapter` protocol it *already declares* —
`src/opendox/corpus_adapter.py`, a `@runtime_checkable` `Protocol` whose own
docstring says *"This interface travels to openDox"* — with
`runtime/local_git_adapter.py` as the conformant implementation it already has.
openXdox **keeps** its governed generator and hands it in through the same seam,
losing nothing. That is precisely the injection `consumer_reach.py` names as
*"BUILD-arc work"* that *"does not exist yet"*: the protocol exists, the
implementation exists, and what was never built is the projection that uses them.

**The ruling is better than this packet's own recommendation was, and the reason
is a fact this packet had not measured.** It recommended relocating the generator
parameterized by a domain mapping declaration. `src/openxdox/generator.py:66-68`
reads:

```
from doc_health import corpus
from doc_health.corpus import RealGit
from doc_health.lines import split_keepends
```

**The generator imports openxFactory's `doc_health` directly.** Relocating it
would have put `import doc_health` inside the neutral core — the exact thing
`corpus-adapter-seam` forbids — trading one wrong-way dependency for a deeper
one. The correction is recorded in full at `design.md` § R-G3 rather than quietly
fixed, because this packet priced that option wrongly and a reader deciding
something similar later should see how.

**Two constraints arrive with the ruling** and are carried as such, not as
proposals:

- **"keep those six words."** `NEUTRAL_DISPLAY` in
  `src/opendox/display_profile.py` stands unchanged — *sources → groups →
  candidates → selections → submissions → completed* — ratified as the
  standalone product's own vocabulary. This arc designs no workflow and
  re-authors no word; requirement 3's fourth scenario carries the rule
  neutrally. **The sixth word is `completed`, not `completions`**: RULED
  ([`5784654370`](https://github.com/opensoft/openxFactory/issues/656#issuecomment-5784654370), *"2, keep completed"*), correcting this
  packet's earlier spelling, which had quoted the module's docstring rather than
  its declaration. **And the governed host keeps "implemented" through a
  facet**: RULED ([`5784683830`](https://github.com/opensoft/openxFactory/issues/656#issuecomment-5784683830), *"1, keep completed and
  overlay implemented"*) — openXdox declares a PARTIAL `DISPLAY` facet labelling
  the `completion` stage "implemented", openDox fills everything else from
  `NEUTRAL_DISPLAY`, and it is the estate's first `DISPLAY` facet (task 5.3a;
  `design.md` § R-G3).
- **"wire the views and land it."** The view-wiring slice was CLAIMED on
  openDox-code under actor `viewwire` and has since LANDED as openDox-code#35 →
  `3c3a9e31`. **This packet does not own it and does not list it as owed work** —
  it is referenced so group 10 is not authored twice. The ruling is explicit: *"The generator itself (decision 1) is
  NOT in this claim — it is the BUILD-arc proposal's subject."*

## A second ruling, forty minutes later: the neutral submission step

**RULED** by Brett Heap, `#656` comment
[`5783934499`](https://github.com/opensoft/openxFactory/issues/656#issuecomment-5783934499),
2026-09-22T20:49:40Z: **"add a neutral publish step to the build arc"**. It
enters as **requirement 11**, a new requirement rather than an amendment, for the
reasons in `design.md` § D9.

**The gap.** RULING C3 makes a standalone openDox a plain local git repository
per project with a remote attachable later, and the runtime honours it —
`runtime/repository_act.py:1131-1138`'s `attach_remote(..., executable="git")`
takes ANY git remote and writes no object, *"which is what makes the eventual
move 'a push, not a migration'"*. **The document surface does not.**
`session_pr.py:297` is `class GhPullRequests`, shelling out at `:367` with
`["gh", "pr", subcommand]` against `_GITHUB_HOST = "github.com"` (`:233`). A pull
request is a hosting-platform artifact and a push is a git one, so the student on
the plain repository C3 describes **has no way to get a session's work out at
all**.

**One refinement, measured here, that makes the requirement narrower and truer.**
A declared protocol already exists — `session_pr.py:98-99` is
`@runtime_checkable class PullRequestPort(Protocol)` with `push`,
`open_or_update` and `find_open`, and `FakePullRequests` is a second
implementation. So `push` is ALREADY neutral; what is platform-shaped is the
other two operations' `PullRequest` return (`number` is a platform's concept);
and **the hard-wire is the DEFAULT BINDING**, not the protocol — `cli.py:812` and
`serve.py:933` construct `GhPullRequests` by name. The arc therefore supplies the
missing neutral IMPLEMENTATION and stops the default naming a platform. Same
shape as requirement 3's missing default profile, one layer over.

### RULED — merge authority follows whoever governs the repository

An earlier draft of requirement 11 made the absence of `merge`/`approve`/`review`/
`bypass` binding and refused a merging implementation. It was withdrawn while the
question was open and **RULED on 2026-09-22T21:06:01Z** ([`5784155201`](https://github.com/opensoft/openxFactory/issues/656#issuecomment-5784155201),
*"merge yes"*).

The absence was never about merging; it was **separation of duties**, and that is
kept wherever a governance exists outside the tool — a governed host RESERVES
landing and routes it to that governance's instrument, so openxFactory's flow is
untouched. What is dropped is the LETTER of the prohibition exactly where the
user IS the governance: forbidding a standalone owner to merge their own
repository protects nobody from anybody. **Three guardrails hold in every mode
and none is configurable** — a merge is an explicit HUMAN act, a CONFLICT is
shown and never silently resolved, and a merge is a COMMIT and therefore
revertible. They are what carries the purpose once the absolute form is gone:
*no tool merging behind its governance's back.*


**The name is "submission", not "publish", and the ruling asked for that care.**
This capability already uses "publisher" for the repository that publishes the
corpus and the contract bundle — requirement 2 reads *"no consumer, no publisher
and no host present"* — and a reader meeting the word twice with two meanings is
a reader the capability has failed. "Submission" is the **fifth of the six ruled
words** `NEUTRAL_DISPLAY` already carries, so the step is named after the stage
the product already says it reaches. Rejected alternatives and the reasoning are
in `design.md` § D9.

One smaller item remains for the ratification read, and it is not a ruling
request: `design.md` § D5 records that requirement 3 revisits the **premise** of
RULED ASK-2 — not its reasoning, since an EMPTY default stays refused. If ASK-2
is read as foreclosing a default profile for openDox's own domain, requirement 3
is struck and the other fifteen stand.


## Impact

- **Affected specs:** ADDS the capability `neutral-product-standalone-operability`.
  MODIFIES nothing. REMOVES nothing.
- **Affected repositories at realization:** `opensoft/openDox-code` (the bulk),
  `opensoft/openXdox-code` (the consumer half of G3 and the back-import ratchet),
  `opensoft/openDox` (one start target), `openxFactory` (manifest annotations
  only).
- **Affected code at ratification:** none. This packet authors no code byte.
- **Blocked on a ruling:** nothing. Requirement 4's mechanism was RULED on
  2026-09-22 (`#656` `5783335210`) and the requirement is written to it. Every
  requirement is actionable on ratification.
- **Landed or in flight elsewhere, deliberately not owned here:** the
  view-wiring slice on openDox-code, claimed by actor `viewwire` in the same
  ruling comment and LANDED as openDox-code#35 → `3c3a9e31`; and the
  `display_profile.py` docstring alignment to `completed`, in flight as
  openDox-code#36.
- **One constraint the realization must respect, found by measurement:** the
  entry point requirement 10 asks for CANNOT be an assembly-root `Makefile`
  target. `openDox/Makefile` carries a row in `contracts/shape-pin.yaml` and
  `AGENTS-shape.md` is explicit — *"An edit in place is reported as DRIFT and
  refused"* — so such a target would red `make pins`, and the lawful route would
  be an upstream change in `opensoft/openRepoShape` binding every project that
  carries the shape. The entry point belongs at the CODE leg as a
  `[project.scripts]` console script, which is where the shape's own "What goes
  where" puts the implementation; the root's README, which carries no shape-pin
  row, documents it.
- **Related and not duplicated:** `corpus-adapter-seam` and
  `domain-mapping-declaration` (promoted 2026-09-22 by the carve's archive) are
  the requirements this arc discharges against; `neutral-product-pin` governs the
  consumption direction and is untouched; `openxfactory-engineering-adapter`
  holds the 15 requirements RULING DQ-1 kept here and is untouched.

## Capabilities

- `neutral-product-standalone-operability` — ADDED, 16 requirements, 69 scenarios.
