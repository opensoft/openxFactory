# The Project Repository Schema

Status: ratified
Kind: standard
Ratified by: add-project-repo-schema
Amended by: prefer-triad-project-shape (ratified 2026-10-06T16:02:16Z,
  openxFactory PR #1249) — the Triad named the PREFERRED project shape, with
  the posture restated beside it unchanged: still elective, still the `PA`
  decision, still conferring NOTHING; advised once where a person starts work,
  never blocking and never converting; never a review input; silent in an
  elected Triad, a leg clone, a family holder, a `<user>-wip` workspace
  repository and a repository carrying the optional `single-repository.yaml`.
  Added as § The Triad is PREFERRED, and it still confers NOTHING. Realized per
  `openspec/changes/prefer-triad-project-shape/tasks.md` task 5.1. This
  document's own status line and ratifying citation are unchanged by it.
Amended by: correct-naming-families-count (ratified 2026-10-07,
  openxFactory PR #1266) — the naming section made count-free: the families are
  the ones the pinned standard's naming policy declares, governed there as DATA,
  and this document states neither how many there are nor which. The section's
  heading, the sentence placing the leg suffixes in a different visual class,
  and the sentence naming where the families are governed are restated to say
  so, and one INFORMATIVE note, dated to the pin, lists what that pin declares
  and governs nothing. Realized per
  `openspec/changes/correct-naming-families-count/tasks.md` task 5.1. This
  document's own status line and ratifying citation are unchanged by it.

GitHub has no folder that groups repositories, so a project spanning several of
them is held together by convention or by nothing. This document is openxFactory's
DOCTRINE for that convention: what the shape is, what electing it means, and —
most of all — what it does not mean. The MECHANICS are not here. They live in
`opensoft/openRepoShape`, a public Apache-2.0 standard this repository pins by
commit and digest at [`contracts/openreposhape-pin.yaml`](../contracts/openreposhape-pin.yaml),
verified by [`scripts/validate-openreposhape-pin.py`](../scripts/validate-openreposhape-pin.py).

> **RATIFIED 2026-09-02 by Brett Heap, the convener** — the act is recorded in
> [`add-project-repo-schema`](../openspec/changes/add-project-repo-schema/proposal.md)
> and its `review/ratification-2026-09-02.md`. `Status: standard` is NOT claimed
> here and is not owed: that status requires a PROMOTED spec, and this change
> stays active until its realization evidence completes. A project that elected
> the shape BEFORE this date recorded the staged fragment's path as its
> reference; one electing it now records this document — see § A project may
> start before this is ratified.

## The one sentence that governs everything else

**The shape is ELECTIVE and it confers NOTHING.**

Electing it changes no gate, no floor, no grant and no clearance eligibility. A
one-repository project and a three-repository project are reviewed IDENTICALLY,
because the authority travels in the grants rather than in the layout. A project
that DECLINES the shape is not less governed and is not reviewed more
suspiciously; a project that ADOPTS it earns no additional clearance.

That is not this document's invention — it is the ratified doctrine of
`add-wallet-carried-review-authority` (2026-08-23), on the convener's ruling of
2026-08-22: *"For our own internal projects, we can have codeXfactory recommend
and run a 3 repo project schema. But let the human project manager decide."* The
election is a `PA` decision, `CA`-constrained and `PM`-sequenced
([roles-and-authority](roles-and-authority.md)), taken per project by a human.

**A consumer that derives any permission from a naming family, a leg role, a
register field or a manifest field is DEFECTIVE.** The defect is the consumer's,
not the declaration's. This sentence appears in four places on purpose — here,
in the capability's first requirement, in the project register's schema
description, and in the assembly-root manifest template — because a posture
stated once is a posture the second reader does not meet.

**Every authority question is deferred**, by name, to the sibling work on
wallet-carried work authority. This document declares no grant, no clearance and
no gate standing.

## The Triad is PREFERRED, and it still confers NOTHING

Ratified 2026-10-06 by `prefer-triad-project-shape`, on Brett Heap's direction
of that day: *"the triad should be the prefered structure and should prompt or
warn the user if working on a non Triad repo."* That change keeps every sentence
of the section above and adds this one beside it, so the preference is never
stated without the posture.

**The Triad is the PREFERRED project shape, and preferred is NOT required.**
"Triad" is the human-facing name for the three-repository shape this document
defines — an assembly root with a spec leg and a code leg, described in § The
three legs below — and "three-leg project" and "three-repository project" remain
accepted synonyms. The name is vocabulary only: no machine key, `kind`, field,
file name or naming family is renamed by it, so `project-manifest`,
`project-repo-schema`, `legs[].role` and every other key a reader parses stay
exactly as they are.

The Triad is the recommended default for a new project and the recommended
migration target for an existing single-repository project. The recommendation
is made TO the person deciding and never in their place. Electing is still the
`PA` decision above, `CA`-constrained and `PM`-sequenced, taken per project by a
human. Converting an existing repository is still openRepoShape's
`adopt-project.py`, run by a person deciding for that project, and nothing
converts a repository automatically.

**The preference confers NOTHING, so every sentence of the section above holds
unchanged.** It adds no gate, no floor, no grant, no clearance eligibility, no
lifecycle state and no review difference. A project that keeps all of its work in
one repository is reviewed identically to a Triad, is not less governed, is not
reviewed more suspiciously, and owes no declaration. Wherever the preference is
stated, this posture is stated with it — here, in the project register's schema
description, and in openRepoShape's assembly-root manifest template — so that no
reader meets "preferred" without also meeting "confers nothing".

### Where it is said: once, where a person starts work

The preference reaches a person as an ADVISORY, and only where that person
starts work on a repository that has not elected the Triad:

- **An agent session addressing a person** says it once per session and then
  carries on with the work it was asked to do. A subagent, a delegated worker and
  an unattended run address no person and say nothing.
- **The workstation bootstrap** that installs a repository's agent-workflow
  pointers prints it as a warning in a non-interactive run, with its exit status
  unchanged. In an interactive terminal it asks before continuing, with
  continuing as the default answer, so a person who takes the default gets
  exactly the run they would have had without the advisory.
- **openRepoShape's scaffold, adopt and doctor** may report it beside what they
  already report, and change no exit status on its account.

Where a person creates a new project, the creating tool or agent offers the
Triad first, as the recommended default, and creates no repository the person
has not confirmed. A single repository chosen instead is accepted without a
reason being asked.

The advisory names two exits and takes neither: how to convert (openRepoShape's
`adopt-project.py`, run by a person deciding for that project) and how to stop
meeting it (the optional record below). It converts nothing, creates nothing,
writes no manifest and no record, and records nothing about having been given,
so no later act can read "was advised" as a fact about a project. Its meaning,
which each surface adapts to its own form, is:

> This is a single repository. The Triad — an assembly root with a spec leg and a
> code leg — is the preferred project shape: openRepoShape's `adopt-project.py`
> converts a repository in place, and a project that stays single can say so in
> `single-repository.yaml`. Nothing here changes; work continues.

**It is never a blocking prompt.** A repository that is not a Triad is neither a
decision a person must make before working nor a containment failure, so under
the interrupt bar in [roles-and-authority](roles-and-authority.md) § Human
Escalation Contract the default is always to continue.

### Where it is never said: review

**A project's shape is never a review input.** No review lane, required check,
validator, floor, merge gate, clearance, council or other review surface reads
whether a project elected the Triad, whether it recorded staying single, or
whether the advisory was given, in order to pass, fail, warn in review output or
change any eligibility. That is what keeps a one-repository project and a Triad
reviewed IDENTICALLY now that one of them is preferred.

An electing project's own conformance gate is not such a reading. The naming,
lockstep-pin and manifest validators this document gives an assembly root, and
the doctor run over that root, check the shape the project ELECTED against what
it declared, and none of them reaches a repository that did not elect.
openRepoShape's doctor answers a person's question about one repository, and its
`NOT A SHAPE ROOT` verdict is an answer to that person. A required check, review
lane or merge gate built on that verdict, or on any other reading of whether a
repository is a Triad, is DEFECTIVE, exactly as a consumer deriving a permission
from layout is.

A shape warning placed inside review — a required check, a review comment, a
council finding — is therefore not a realization of the preference. It would
amend the one sentence above, and it must be proposed as such an amendment if it
is ever wanted.

### Where it is silent

The advisory is not given where the shape question is already answered or does
not arise. Each case is read from a declared fact — the repository's own tree,
the pinned naming policy, or the person's own configuration — and never inferred:

1. **An elected Triad assembly root**: `project.yaml` carrying
   `kind: project-manifest`, `schema: project-repo-schema` and `legs:` naming a
   `spec` and a `code` leg.
2. **A leg clone**, where the existing instruction to move to the assembly root
   applies instead.
3. **A family holder**: `family.yaml` carrying `kind: family-manifest` and no
   `project.yaml`, which pins member projects and is not itself a project that
   could elect.
4. **A `<user>-wip` workspace repository**, which holds no code and elects
   nothing, identified by the naming family openRepoShape's naming policy
   declares for it or because the person's own workspace configuration names it.
5. **A repository that has recorded staying single**: `single-repository.yaml` at
   its root, below.

**That list is the whole list.** Every other repository — an aggregation, a
configuration or dotfile repository, a vendored fork, or any class a tool might
infer — receives the advisory until it migrates or records staying single. No
surface exempts a repository by guessing its class. A class that should be
exempt is first given a declared fact, as `<user>-wip` has a naming family, and
then added to this list by a change to the `project-repo-schema` capability.

### The optional staying-single record

A project that has decided to stay a single repository MAY say so once, in
`single-repository.yaml` at its repository root. The record is OPTIONAL and never
owed. A project that declines the Triad and records nothing owes nothing, is
reviewed identically, and meets only the advisory, once per session wherever a
person starts work in it.

The record carries `schema_version: 1`, `kind: single-repository-record`,
`decided_by` (the person who decided for the project, as for an election),
`decided_on` (an ISO date), `reason`, and an optional `revisit_on`. Its schema
and template are openRepoShape's, as mechanics, like the rest of this schema's
mechanics. Its ONLY reader is the advisory: a record whose `kind` is
`single-repository-record` silences it. It confers nothing — no gate, no floor,
no grant, no clearance eligibility, no lifecycle state and no review difference —
and it restates that wherever it is recorded. A file that cannot be read, or
that carries another `kind`, declares nothing and so silences nothing; a surface
may report it, and reporting it fails nothing.

It is deliberately NOT `project.yaml` or a field of it. `project.yaml` with
`kind: project-manifest` and a spec and a code leg is how every surface detects
a Triad, and the doctor's `NOT A SHAPE ROOT` verdict keys on that file's
absence. The project register gains no field for it either: the register is
navigation, and a staying-single marker there would be a second reader.

### Who says it

The advisory restates THIS document's preference where work starts. It is not
codexFactory's act of RECOMMENDING the shape (§ Who owns what, below), which
codexFactory keeps in full: that act is made to a project, and the election
stays the project's human decision. Ruled on 2026-10-06 as that change's third
open question (OQ-3), so the ownership split is unchanged and nothing is
re-concentrated.

## The three legs

| role | repository | holds |
|---|---|---|
| assembly | `<Project>` | the project manifest, the two legs as submodules, the pins, the gate |
| spec | `<Project>-spec` | requirements, decisions, acceptance criteria |
| code | `<Project>-code` | the implementation and its tests |

**The ASSEMBLY leg is the per-project ROOT repository** — the one an engineer
clones. Ruled by Brett Heap, 2026-09-02: *"yes, assembly is per project."* It MAY
additionally pin shared review-team assembly code as an OVERLAY, at a sha, the
way the xFactory aggregation already consumes its review lane at
`review-lane-reusable.yml@<sha>`. That reading and the ratified sentence
*"ASSEMBLY (the code that assembles a review team, shared across the family)"*
then both hold: the per-project root is the LEG, and the shared code is CONTENT
that root may pin.

## Naming, and the naming families

`<Project>` bare for the assembly root, `<Project>-spec` and `<Project>-code` for
the legs. `<Project>` is one CamelCase token with no hyphen, underscore, dot or
space; the suffixes are fixed lowercase and hyphenated, precisely so they sit in a
different visual class from every family the pinned standard's naming policy spells
as a CamelCase word. The assembly root is bare because the thing you clone has no
suffix — the precedent the aggregation root already sets.

Every repository of a project also carries the GitHub topic `xf-project-<id>`,
where `<id>` is the project's lowercase id.

The naming families are the ones the pinned standard's
`contracts/repository-naming.yaml` declares, and they are governed there as DATA,
not by this prose, which therefore states neither how many there are nor which.
Among them are `open<Product>` neutral products, `<X>-Install` installs,
`<Domainx><Product>` domain descendants, and the project legs above, which are
the families the rules in this section reach.

> Informative, dated 2026-10-07 to the pin. At the commit
> [`contracts/openreposhape-pin.yaml`](../contracts/openreposhape-pin.yaml)
> names, `1a9fc537bcce…`, the naming policy declares six families:
> `neutral-product` (`open<Product>`), `install` (`<X>-Install`),
> `domain-descendant` (`<Domainx><Product>`, a claim answered by a declared
> pin), `project-leg` (`<Project>`, `<Project>-spec`, `<Project>-code`),
> `family` (a holder, reported only where its `family.yaml` declares it), and
> `workspace` (`<user>-wip`, one person's private index of unfinished work).
> This list is a reading of the data at that pin and governs nothing. The policy
> at the pin in force is where the families are read, and a later pin may
> declare more or fewer without this doctrine moving.

### A descendant form is a claim, and a claim needs a referent

Ruled by Brett Heap, 2026-09-02: ***"Descendant only if it pins
open&lt;Product&gt;."***

`open<Product>` and `<X>-Install` say what they are in their own characters and
win outright. `<Domainx><Product>` does not. A name of that shape classifies as a
domain descendant ONLY where the project DECLARES a pin on the matching
`open<Product>`. `MedxChart` is a descendant BECAUSE MedxChart pins `openChart`;
a name in the same shape that descends from nothing is an ordinary assembly root,
its DECLARED ROLE wins, and the project's manifest RECORDS that the name also
matches the descendant form so a resolved overlap stays visible rather than being
silently discarded.

The check stays OFFLINE: the referent is a pin the project declares, a fact in its
own tree, so classification never asks any host whether `open<Product>` exists. A
rule that needed the network would be unrunnable in exactly the fork-and-run case
this standard is built for.

**This narrows nothing in `domain-descendant-boundary`.** A descendant is still a
descendant because it pins the product — which is what that capability already
requires.

> Amended 2026-09-05. **The rule above is unchanged: a descendant form is a
> CLAIM, and the claim is answered only by a PIN the project declares — never by
> the spelling, and never by asking a host anything.** What this note adds is one
> thing and only one: **HOW FAR that pin may reach.** The 2026-09-02 sentence
> ratified in this section, ***"Descendant only if it pins open&lt;Product&gt;."***,
> states the rule in its DIRECT case, which was the only case that existed when
> it was written; it is not narrowed or widened here, it is read as what it
> always was — a requirement that a referent be DECLARED, not a requirement
> that it be declared in one hop.
> Ruled by Brett Heap, 2026-09-05T14:52Z, in session, verbatim: **"elect the
> shape for both, follow the pin chain, no family yet"**. A
> `<Domainx><Product>` name classifies as a domain descendant
> where its declared `neutral_product_pins` REACH the matching `open<Product>`
> through a CHAIN of declared neutral-product pins — `codexDox` declares
> `openXdox`, whose own manifest declares `openDox` — and a DIRECT pin remains
> sufficient. Every link stays an offline fact in a tree, so the check still
> asks no host anything, and the chain is RECORDED by the descendant rather than
> inferred, so a reader sees which links a classification relied on. The
> mechanics are `opensoft/openRepoShape`'s to state and are authored there as
> `opensoft/openRepoShape`#40; this doctrine only says the referent may be
> reached rather than only named. Ruling:
> `opensoft/openxFactory`#656 comment `5552614170`; the consuming amendment is
> `openspec/changes/split-opendox-two-layer-product/review/amendment-2026-09-05-repository-shape.md`.

## The double pin, and the lockstep invariant

Each non-assembly leg is pinned TWICE, in the same commit: by the GITLINK git
records for the submodule, and by `contracts/<role>-pin.yaml` carrying
`revision_kind: commit`, the exact commit and a digest. A tag may be recorded
beside the commit as a human-readable label, never as the thing being trusted, and
a pin never expresses a range. This is the ratified house form — the same-commit
rule from `domain-descendant-boundary` and the commit-and-digest rule from
`neutral-product-pin` — reused unchanged. No pin grammar is invented here.

Three things move together, in ONE commit:

1. the gitlink,
2. `commit:` in `contracts/<role>-pin.yaml`,
3. every workflow reference naming that leg at a sha.

The assembly root's own pull-request gate runs a validator that refuses when they
disagree, with a remediation string in the fail-closed form `neutral-product-pin`
already requires.

**This is a measured cost, not a hypothesis.** In the xFactory aggregation the
same invariant was practice for months and written down nowhere. Seven
consecutive pin-syncs from 2026-08-25 moved the gitlink alone and left `validate`
red on every aggregation pull request until 2026-08-26 (xFactory #146) —
unnoticed for a day because `validate` runs on pull requests only, so `main` never
reports it. The invariant is not aggregation-specific: any assembly root that both
pins a leg and dispatches a workflow at that leg's sha has it. Shipping the check
in the template turns a per-project tribal rule into a one-time scaffold cost.

### Why submodules and not a manifest of side-by-side clones

The pin is the product. A manifest gives the same directory layout with
independent clones and no shared commit — and without one commit naming both legs
there is no object for a gate to validate, and no way to say what "the project"
was at a point in time. The manifest's real advantage is ergonomic, and bootstrap
recovers it.

## The manifest is the source; a register row is derived

An electing project carries a self-describing manifest in its assembly root — the
project id, the elected schema, the reference the election followed, who elected
it and when, the project topic, each leg with its role and path, and the standard
revision it was scaffolded from.

**Where an aggregation register exists, the register row is DERIVABLE FROM that
manifest. The manifest is the SOURCE; the register is never the origin of the
election.** That direction is what lets an organisation with no aggregation, no
register and no openxFactory be conformant: a file inside the project is readable
by anyone who cloned it, which is exactly the population that needs it.

Three layers of grouping must agree — names carry the human eye, GitHub topics
carry the organisation's search, and the register is the only one of the three
that is REVIEWED. Where they disagree the register wins for navigation and the
others are reported as drift.

The register's fields are optional and additive:
`contracts/schemas/project-register.schema.yaml` gains a per-project `schema`, a
per-project `reference`, and a per-project `repository_roles` list assigning each
named repository a `role` of `spec`, `code` or `assembly`. `repositories` is
unchanged and remains the single membership answer. The requirement lives in the
`ideation-dashboard` capability, which owns the register today.

## Bootstrap: one command, schema-neutral, and it degrades

`git clone --recurse-submodules <Project>`, then ONE bootstrap command that

- **(a)** places each submodule on a tracking branch AT its pinned commit,
- **(b)** installs the project's neutral validators and hooks, and
- **(c)** reads any wallet review-authority register it can find and prints which
  objects the running engineer's grant lets them act on.

**The pin stays exact.** `.gitmodules` carries no `branch=` and no
`update=merge`: those buy the same ergonomics by making the declared pin advisory
for anyone running the remote form, which is the moving reference
`neutral-product-pin` already refuses in its own words. The convenience lives in a
COMMAND rather than in checked-in configuration, so there is exactly one
authoritative answer to "what commit is this project".

**The contract is SCHEMA-NEUTRAL.** A one-repository project runs the same
command and gets (b) and (c), the submodule step being a no-op. A bootstrap that
existed only for electing projects would make election worth something
operationally, which is exactly what the ratified doctrine forbids.
Schema-neutrality is how "confers nothing" survives contact with tooling.

**And it degrades rather than failing.** Where no wallet review-authority register
is found, step (c) prints exactly

```
authority is not wallet-carried in this org
```

and continues. An organisation that has not adopted wallet-carried authority is
not misconfigured, and a bootstrap that refused there would have made the layout
load-bearing again — the property this whole line of work exists to prevent. The
readout is REPORTING only: a required check in the repository that owns the
object is what confers.

## Overlays attach to a shape, never the reverse

A scaffolded project's own gate runs the NEUTRAL validators only — naming,
lockstep pin and manifest conformance. An engineering review lane, wallet-carried
authority and any domain CI are OPT-IN OVERLAYS an organisation adds later. **A
project holding none of them is FULLY conformant**, and it must be: the ratified
doctrine says election confers nothing, which is only true if a project with no
overlays is conformant. A shape that required its overlays would have made layout
load-bearing again.

## Who owns what

| plane | owner | holds |
|---|---|---|
| mechanics | `opensoft/openRepoShape` | naming policy as data, templates, scaffold, bootstrap, validators, agent instructions |
| doctrine | `openxFactory` | this document, the pin, the register-election delta |
| engineering overlay | `codexFactory` | the review-lane caller, engineering CI, and the act of RECOMMENDING the shape |
| organisation administration | `OpsxFactory` | organisation-level naming enforcement, repository-topic administration, any GitHub template repository |

**This NARROWS the ratified prose, and the narrowing is stated rather than
assumed.** `add-wallet-carried-review-authority` says *"codexFactory may recommend
— and scaffold — a three-repository shape"*. Read straight, that gives codexFactory
the scaffold. It is narrowed HERE in exactly one respect — **where the mechanics
LIVE** — because the convener's own case, a new organisation with no codexFactory,
cannot be served by a scaffold that is a directory of an engineering-domain
repository. **codexFactory keeps the recommending role in full**, keeps its
engineering overlay, and that change's task 8.4 is satisfied by
overlay-plus-offer rather than by codexFactory hosting the neutral shape.

## Starting a project in a new organisation

The convener's own question, answered literally: *"if I have a new org and in that
new org i want to make a new project… I think i need to fork the … repo from
opensoft and then tell my ai to scaffold a new project based on that."*

1. **FORK** `opensoft/openRepoShape` into the organisation — a fork, not a GitHub
   template, so the upstream link survives, shape updates pull, and the project's
   shape pin names a commit that still means something.
2. In the fork, run the setup entry point. It validates the three names against
   the naming policy, prints the plan, **asks once**, then creates the three
   repositories, adds the two legs as submodules with their digest pins, writes
   the shape pin recording the openRepoShape commit and digest the project was cut
   from, writes the self-describing manifest, and sets the GitHub topic on all
   three.
3. `git clone --recurse-submodules`, then the one bootstrap command.

The fork carries AGENT-READABLE instructions, because *"tell my ai to scaffold a
new project based on that"* is a requirement and not a figure of speech: without
them the flow depends on a prompt somebody remembers.

## A project may start before this is ratified

Yes — provided the project's manifest, and its register row where one exists,
record both the election and the REFERENCE it followed: the staged fragment's path
before ratification, this document after. Recording it is what makes a project
started ahead of ratification LEGIBLE rather than undeclared, and what lets a
later ratification reconcile drift instead of discovering it. The house already
works this way: the staging index's own draft-proposal workspace convention was
*"Adopted 2026-07-13 (Brett), first used by ideation-dashboard"* before any spec
carried it.

**A project scaffolded solely to exercise the standard is a TEMPORARY PILOT and
must say so.** It is not a product of the organisation that holds it, it is not
"the first project", and it may be deleted once the standard is ratified. The
evidence such a pilot produces is the RECORDED RUN — the commands, the commits,
the validator outcomes — which survives the pilot's deletion. Evidence that
depended on a temporary repository continuing to exist would be evidence with a
half-life.

### The pilot on record

**`MedxSoft/MedxScribe` is a TEMPORARY PILOT and not a real project.** Ruled by
Brett Heap, 2026-09-02: *"MedxScribe is only a temp pilot project right? it is not
a real project. make sure it noted as pilot to test the openRepoShape"*. It and
its two legs were scaffolded on 2026-09-02 for one purpose — to run
`opensoft/openRepoShape` end to end — and may be deleted once this document is
ratified. The three repositories carry `PILOT (temporary): …` descriptions and the
topics `pilot` and `openreposhape-pilot`; the assembly root's README carries a
banner saying the same.

The run it produced, against openRepoShape `deacbdc`, succeeded end to end: three
repositories created, the topic set on all three, the legs mounted, the shape pin
written, the election recorded with the staged fragment as its reference, both
legs left on `main` at their pins after `git clone --recurse-submodules` and
bootstrap, the naming, manifest and lockstep-pin validators green, the shape copy
pin green, and the degrade line printed verbatim. The full record — commands,
commits and outcomes — is in
[`add-project-repo-schema`'s proposal](../openspec/changes/add-project-repo-schema/proposal.md)
§ Realization evidence.

That run also fixed the standard. The FIRST pilot run found two defects — an
organisation misdetection that preferred the `upstream` remote over `origin` and
so refused a correct fork, and a descendant-shaped name read as a fact rather than
a claim — and both were fixed upstream the same day, at `7edd6bb` and `deacbdc`
respectively. **The commit this repository RATIFIED against is `deacbdc`, the one
carrying both fixes**, so the standard openxFactory ratified is the one the pilot
proved rather than the one it broke.

> Amended 2026-09-04. This first said "the commit this repository PINS is
> `deacbdc`". That was true when this document was ratified and is no longer:
> [`contracts/openreposhape-pin.yaml`](../contracts/openreposhape-pin.yaml) now
> pins `122d729bc0c2…` — openRepoShape `main` of 2026-09-04, twenty-seven
> digested and thirty-three path-only members over a sixty-file surface. Nothing
> in this doctrine moves with that bump: the pin advances within its own ratified
> grammar, and the PIN FILE rather than this sentence is where the commit in
> force is read. The ratification fact above is unchanged; only the present tense
> was wrong.

> Amended 2026-09-05. The note above said the pin "now pins `122d729bc0c2…` —
> openRepoShape `main` of 2026-09-04, twenty-seven digested and thirty-three
> path-only members over a sixty-file surface". That was true after PR #650 and
> is no longer:
> [`contracts/openreposhape-pin.yaml`](../contracts/openreposhape-pin.yaml) now
> pins `e9c4827b85f5…` — openRepoShape `main` of 2026-09-05, covering
> openRepoShape #42 (a descendant's referent reached through a declared pin
> chain) and #45 (a neutral product may elect the shape and be its own assembly
> root) — thirty-one digested and forty-five path-only members over a
> seventy-six-file surface. Nothing in this doctrine moves with this bump
> either: the pin advances within its own ratified grammar, and the PIN FILE
> rather than either sentence is where the commit in force is read. Both
> ratification facts above are unchanged; only the present tense was, again,
> wrong.

> Amended 2026-10-06. The note above said the pin "now pins `e9c4827b85f5…` —
> openRepoShape `main` of 2026-09-05 … thirty-one digested and forty-five
> path-only members over a seventy-six-file surface". That was true after PR
> #700 and is no longer:
> [`contracts/openreposhape-pin.yaml`](../contracts/openreposhape-pin.yaml) now
> pins `1a9fc537bcce…` — openRepoShape #164, the realization of
> `prefer-triad-project-shape` task 5.2 (the advisory and the optional
> `single-repository.yaml` named in § The Triad is PREFERRED above), fifty-seven
> commits on, and covering with it the compliance command
> `openRepoShape --doctor` (`shape-doctor.py`, openRepoShape #96), the native
> Windows flow `setup-project.py` that `setup.sh` now hands over to (#53, #60),
> and the `<user>-wip` workspace template (#154) — thirty-seven digested and
> sixty-seven path-only members over a hundred-and-four-file surface. Nothing in
> this doctrine moves with this bump either: the pin advances within its own
> ratified grammar, and the PIN FILE rather than any of these sentences is where
> the commit in force is read. The ratification facts above are unchanged; only
> the present tense was, a third time, wrong.

## See also

- [`contracts/openreposhape-pin.yaml`](../contracts/openreposhape-pin.yaml) — the pin
- [`scripts/validate-openreposhape-pin.py`](../scripts/validate-openreposhape-pin.py) — the running check
- [`contracts/schemas/project-register.schema.yaml`](../contracts/schemas/project-register.schema.yaml) — the register, with the election fields
- [`docs/roles-and-authority.md`](roles-and-authority.md) — who elects (`PA`, `CA`-constrained, `PM`-sequenced)
- [`docs/document-lifecycle.md`](document-lifecycle.md) — this document's own `Status:` header
- `https://github.com/opensoft/openRepoShape` — the standard
