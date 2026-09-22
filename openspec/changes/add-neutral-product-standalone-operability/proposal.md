---
code_surface: openxFactory, openDox-code, openXdox-code and the openDox assembly root — THIS PACKET AUTHORS NO CODE BYTE, and it declares a real one. Landing here is corpus text only: this packet's five files (`proposal.md`, `design.md`, `tasks.md`, `.openspec.yaml` and ONE `## ADDED` spec delta), one README *Active changes* bullet, and the machine-seeded per-change row in `tests/sequenced_after/corpus-ledger.yaml` that every filing owes. The REALIZATION the requirements specify runs post-ratification, in three repositories, and each arm is a named task with its own claim: in `opensoft/openDox-code`, the removal of the two module-level `ideation_dashboard` imports at `src/opendox/serve.py:199,206` and their replacement by the route-extension seam the carve's `design.md` already specifies, a default domain profile so `build_parser()`/`build_server()` start with no host, the resolution of `src/opendox/authoring.py:318`'s `corpus_adapter_openxfactory` reach through the registered adapter, a document validator and a health check over its own documents, a `[project.scripts]` entry point for the document surface, and the removal of its `validate.yml` exclusions; in `opensoft/openXdox-code`, the consumer half of whichever G3 mechanism is ruled plus the `OPENDOX_BACK_IMPORTS` ratchet driven down as each reach closes; in `opensoft/openDox` (the assembly root), one documented start target; and in `openxFactory`, NOTHING BUT the carve-manifest annotations that record each closed reach — no check family, no schema, no corpus document and no `scripts/` module moves, per this packet's first requirement. NOT THIS CHANGE'S SURFACE, and named so no reader infers it: the re-promotion of the 71 requirements the carve's map assigns to openDox is openDox-spec's own act and is tracked as a BLOCKED task here, not authored here; the document surface is NOT rewritten, re-architected or re-scoped; and no pin, gitlink, contract bundle or release tag moves.
target_release: implementation_pending — the requirements land now and realization runs post-ratification, on the main lines of the four repositories named above, because this packet's whole content is a DIRECTION to reverse and a product entry point to declare, neither of which ratification performs. The archive gate is merged-plus-green realization evidence per `release-realization`: for each requirement, the falsification command named in its `tasks.md` box, run in a checkout holding only the repository under test, quoted with its output. No contract bundle is cut, no bundle number is allocated or reserved, and no release tag is owed — this packet moves no contract byte.
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
archived packet's own rulings, and the ONE that is not settled is put to Brett
as a named question in `design.md` § Q-G3 rather than decided here.

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

**And the structural fact, which is why this cannot be closed by deleting two
import lines.** openDox serves a snapshot it cannot generate. `generate_snapshot`,
`write_snapshot`, `find_validator`, `corpus_root`, `snapshot_registry` and
`completeness` all went to openXdox at the carve, reached back from openDox
late-bound through `consumer_reach.py`, whose docstring states the position in
terms: *"THE REMEDY IS TO INSTALL openXdox — and only that, today."* A user who
installs openDox alone gets a reader with nothing to read. **Where that generator
should live is the one question this packet does not answer** — see
§ "The one question this packet puts to Brett" below, and `design.md` § Q-G3.

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

**That openDox cannot yet govern its own BUILD arc is itself the gap this packet
carries as G7**, and the requirement *"An extracted product's own spec instance
governs its requirements before the product is called standalone"* names the
succession: once openDox-spec has promoted the requirements the carve's map
assigns it, work scoped to openDox is authored there, and this arrangement ends.

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
- **A neutral, profile-parameterized corpus reader already exists** at
  openXdox-code `src/openxdox/domain_corpus_adapter.py`, answering the
  conformance corpus 17 of 17 (`#23` → `3ee8cd39`). It is at the consumer leg, so
  openDox reaching it would be a new back-import — but it is evidence that the
  parameterized shape Q-G3 recommends is a shape this estate has already built
  once.

**One correction this packet owes the record.** openDox-code's `README.md:39-42`
says `validate` is narrowed *"Until the BUILD arc … inverts the openDox →
openXdox dependency"*. That reason is now false — the dependency IS inverted at
import time. What narrows `validate` today is `ideation_dashboard`, a different
name entirely. The correction is task 9.1's, not this packet's.

## What Changes

ONE `## ADDED Requirements` block creating the capability
`neutral-product-standalone-operability` — ten requirements, thirty scenarios.
The capability is the sibling of `neutral-product-pin`: that one governs
openxFactory CONSUMING an external neutral product; this one governs the product
being able to STAND UP without its consumer. It is written domain-neutrally and
applies to every neutral product openxFactory pins; openDox is the measured
instance it is written from, exactly as `corpus-adapter-seam` is written from
its own measured instance.

The requirements, in the order of the gap sweep that measured them, each
separately satisfiable and each falsifiable by a command named in `tasks.md`:

| # | Requirement | Gap | Falsified by running |
|---|---|---|---|
| 1 | Making a neutral product standalone moves no corpus, no governance instance and no check family | — | the guard: a diff of `openxFactory/scripts/` and `openspec/` across the arc |
| 2 | A neutral product imports with no consumer, no publisher and no host present | G1 | `python -c "import opendox.serve"` in an openDox-only checkout |
| 3 | A neutral product ships a default profile for its own domain, and the composition point stays open | G2 | `opendox --help` with no host registered |
| 4 | A neutral product produces its own primary artifact with no consumer installed | G3 | generate a snapshot with `openxdox` absent |
| 5 | A deferred reach into the publisher or the consumer resolves through the declared seam | G4 | call the authoring verb with no `corpus_adapter_openxfactory` on the path |
| 6 | A neutral product carries a health check over its own documents, and corpus-operations families stay with the corpus | G5 | run openDox's health check in an openDox-only checkout |
| 7 | A neutral product validates its own documents from a single checkout | G6 | run openDox's validator over a document, one checkout |
| 8 | An extracted product's own spec instance governs its requirements before the product is called standalone | G7 | `openspec list --specs` in openDox-spec |
| 9 | Each repository of a split product runs its own suite to green in its own checkout | G8 | each leg's suite, no exclusions, no sibling |
| 10 | A neutral product declares one entry point that starts the whole product | G9, G10 | install, run the one documented command, reach the browser surface |

**What this packet deliberately does NOT propose.** It is not a rewrite. The
document surface is not re-architected, its routes are not re-scoped and its
80K-line inheritance is not revisited — the arc REVERSES A DIRECTION and adds a
front door, and every requirement above is satisfiable without changing what the
surface does. It does not re-home a single doc-health check family. It does not
re-promote the 71 requirements the carve's map assigns to openDox; that is
openDox-spec's own act and is carried here as a BLOCKED task with its
precondition named. It moves no pin, no gitlink, no contract bundle and no
release tag.

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
- **The doc-health check families.** Not one moves. Requirement 6 says so as a
  refusal, not as a promise: a family that reads openxFactory's `Status:`
  taxonomy or its change/spec/delta nouns stays with the corpus under RULING C2.
  What openDox gains is a health check over ITS OWN documents — new generic code
  on the neutral side, not a relocated family.
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

## The one question this packet puts to Brett

**G3 — where does the snapshot generator live?** This packet does not decide it
and must not. The generator sits in openXdox by RULING C2 and DIRECTION Q5, which
are about vocabulary, not about convenience: C2 refuses placing openxFactory's
status taxonomy, its change/spec/delta nouns and its doc-health families in the
neutral layer, *"because a clinician using a descendant would then see the word
'requirement'"*; Q5 exists to stop the neutral layer shipping one domain's words
so that every other descendant forks it. Moving the generator naively would
violate both. Leaving it where it is means openDox is never standalone.

The options, the recommendation and the consequences of each are in `design.md`
§ Q-G3. Requirement 4 above is deliberately written to the OUTCOME — "produces
its own primary artifact with no consumer installed" — so that it is satisfied
by whichever mechanism Brett rules, and no mechanism is smuggled in by the
requirement's wording.

## Impact

- **Affected specs:** ADDS the capability `neutral-product-standalone-operability`.
  MODIFIES nothing. REMOVES nothing.
- **Affected repositories at realization:** `opensoft/openDox-code` (the bulk),
  `opensoft/openXdox-code` (the consumer half of G3 and the back-import ratchet),
  `opensoft/openDox` (one start target), `openxFactory` (manifest annotations
  only).
- **Affected code at ratification:** none. This packet authors no code byte.
- **Blocked on a ruling:** requirement 4's mechanism (§ Q-G3). Every other
  requirement is actionable on ratification.
- **Related and not duplicated:** `corpus-adapter-seam` and
  `domain-mapping-declaration` (promoted 2026-09-22 by the carve's archive) are
  the requirements this arc discharges against; `neutral-product-pin` governs the
  consumption direction and is untouched; `openxfactory-engineering-adapter`
  holds the 15 requirements RULING DQ-1 kept here and is untouched.

## Capabilities

- `neutral-product-standalone-operability` — ADDED, 10 requirements, 30 scenarios.
