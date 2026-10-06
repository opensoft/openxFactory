---
code_surface: openxFactory, opensoft/openRepoShape — THIS PACKET AUTHORS NO CODE BYTE, AND IT DECLARES A REAL SURFACE. Landing it is corpus text only: its five files (`proposal.md`, `design.md`, `tasks.md`, `.openspec.yaml` and one spec delta) plus its ratification record under `review/`, one README *Active changes* bullet, and the machine-seeded row in `tests/sequenced_after/corpus-ledger.yaml` that every filing owes. The REALIZATION runs after ratification. In `opensoft/openRepoShape`: the advisory in `scaffold-project.py`, `adopt-project.py` and `shape-doctor.py`, the optional staying-single record's schema and template, and the posture text in `README.md`, `AGENTS.md` and `templates/assembly-root/project.yaml`. In openxFactory: `docs/project-repo-schema.md` and the description of `contracts/schemas/project-register.schema.yaml` restated, and `contracts/openreposhape-pin.yaml` advanced onto the realized standard. THREE FURTHER SURFACES ARE NOT IN THE HEAD BECAUSE THE ESTATE INVENTORY DOES NOT CARRY THEM, and they are named here so no reader takes them to be out of scope: `opensoft/workBenches` (the `setup-openspeckit` bootstrap, its tests, and its embedded fallback protocol), `opensoft/openRepoProject` (new-project creation, reached through workBenches' `project-command` change), and the shared agent protocol, whose source is a private repository named in `tasks.md` § 5.5. `scripts/estate-repository-inventory.yaml` carries none of the three, its own header says a row records an admission and performs none, and the membership arm of `scripts/validate-code-surface.py` fails an identifier the inventory does not carry, so each is a HANDOFF to its owner with a `tasks.md` box this packet's archive waits on (`design.md` D9).
target_release: implemented — the affected repositories' main lines: openxFactory and opensoft/openRepoShape, plus the three handoff surfaces named under `code_surface:`. No contract bundle is cut and no release tag is owed. Neither openxFactory file the realization edits is a bundle member: `contracts/openreposhape-pin.yaml` is registered in no bundle (the manifest's openXwallet-pin note says that registration "covers one pin and not both"), and `contracts/schemas/project-register.schema.yaml` appears in neither `contracts/manifest.yaml` nor any `contracts/releases/` inventory. Because the code surface is NOT empty, under `release-realization` this packet archives only on merged plus green realization evidence on every surface `tasks.md` § 5 names, and not on landing (`tasks.md` § 6).
---

# Proposal: prefer-triad-project-shape

Status: ratified
Ratified: 2026-10-06T16:02:16Z by Brett Heap (openxFactory operator authority) — in session, verbatim "ratify 1249 as recommended" (PR #1249 comment 6020300563), over PR #1249's head `8f9c5855`; record at review/ratification-2026-10-06.md
Kind: proposal
Proposed: 2026-10-06, in lane `codeXfactory-5`, session
`ed23f049-7e99-4601-8a6d-760b6aeb5f26`.
Origin: Brett Heap's in-session direction of 2026-10-06, quoted verbatim below
and recorded in `.openspec.yaml` (`kind: ad_hoc`, unapproved).

**RATIFIED ON 2026-10-06. The next paragraph is kept verbatim as the filing's
record.** It was true at filing and is superseded by the ratification cited
above and recorded under § Ratification record. That ratification settles the
design, and each open question as recommended. It is not a merge word and not a
word to realize anything, so this pull request stays held for Brett Heap's merge
word.

**NOTHING HERE IS RATIFIED BY THE AUTHORING LANE, AND NOTHING HERE IS BRETT
HEAP'S RULING BEYOND HIS TWO SENTENCES.** This packet proposes how to carry out
his direction without breaking the doctrine it meets. The advisory-only form,
the exemptions, the optional record and every other design choice are put to
him for ratification. Held for Brett Heap's ratification and merge words.

## The direction, verbatim

- **2026-10-06T10:20:12Z**, Brett Heap, in session: *"the triad should be the
  prefered structure and should prompt or warn the user if working on a non
  Triad repo."*
- **2026-10-06T11:28:19Z**, Brett Heap, after the lane answered with the reading
  this packet encodes and a plan to author it: *"usage is fine, launch both"*.

The second sentence authorized AUTHORING and OPENING this proposal. It is not a
ratification and it rules on no design point.

"Triad" is the estate's name for the openRepoShape three-repository shape: an
assembly root with a spec leg and a code leg mounted as submodules. The shared
agent protocol has used the word since its "Triad Feature Amendments" section
was adopted on 2026-10-04. No openRepoShape document uses it yet.

**The sibling.** `opensoft/workBenches#135` lands the adopted Triad Feature
Amendments change, which governs how a project that is ALREADY a Triad amends
its features. Copilot's review there (thread `4194811387`) observed that that
change carries no preference for the Triad and no non-Triad warning, and asked
for Brett Heap's 2026-10-06 direction to be recorded as a deferred follow-up.
THIS change is where that direction is governed; the two do not overlap.

## Why a change, and not a sentence somewhere

The direction meets a promoted requirement head on.
`openspec/specs/project-repo-schema/spec.md`, *The project repository schema is
elective and confers nothing*, says a repository's layout SHALL confer no gate,
no floor, no grant, no clearance eligibility and no lifecycle state; that a
one-repository and a three-repository project SHALL be reviewed IDENTICALLY;
that electing is a `PA` decision, `CA`-constrained and `PM`-sequenced, taken per
project by a human and never a precondition of review; that a consumer deriving
permission from layout is DEFECTIVE; and that the posture SHALL be restated
wherever the schema is recorded. Its scenario *A project declines the schema*
says the decliner "owes no declaration". The ratified doctrine document
`docs/project-repo-schema.md` says *"The shape is ELECTIVE and it confers
NOTHING"*, and openRepoShape's README and AGENTS.md say the same.

A preference stated anywhere outside that requirement would read, to the next
consumer, as layout mattering after all. A warning placed in review would make
the two shapes reviewed differently, which that requirement forbids outright.
So the preference has to be stated INSIDE the requirement, with rules for where
it may be spoken and where it may not. That is this packet.

## What changes

**`project-repo-schema`, ONE `## MODIFIED` requirement** — *The project
repository schema is elective and confers nothing*, title unchanged. Every body
sentence and all three promoted scenarios are carried byte-identically (`tasks.md`
§ 3.1). Added:

- **The preference.** The Triad is the PREFERRED project shape: the recommended
  default for a new project and the recommended migration target for an
  existing single repository. Preferred SHALL NOT be read as required. The
  election stays the `PA` decision; conversion stays openRepoShape's
  `adopt-project.py`, run by a person deciding for that project.
- **The name.** "Triad" in human-facing text, with "three-leg project" and
  "three-repository project" kept as synonyms. No machine key is renamed.
- **The posture travels with the preference.** Wherever the preference is
  stated, "confers nothing" is stated with it; and it is restated beside the
  posture in the doctrine document, the register's schema description and the
  assembly-root manifest template.
- **Two scenarios:** a person creating a new project is offered the Triad first
  and may choose a single repository without being asked why; an existing single
  repository's recommended target is the Triad, and nothing converts it
  automatically.

**THREE `## ADDED` requirements:**

1. **A person starting work outside a Triad is advised once, and is never
   stopped for it.** An agent session addressing a person says it once per
   session and carries on (subagents and unattended runs say nothing); the
   workstation bootstrap warns in a non-interactive run with its exit status
   unchanged, and in an interactive terminal asks before continuing with
   "continue" as the default; openRepoShape's scaffold, adopt and doctor may
   report it. Creation offers the Triad first. Nothing converts, creates or
   records anything on the advisory's account.
2. **A project's shape is never a review input.** No review lane, required
   check, validator, floor, merge gate, clearance or council reads the shape to
   pass, fail, warn in review output or change eligibility. An electing
   project's own conformance gate is not such a reading. A gate built on the
   doctor's `NOT A SHAPE ROOT` verdict is defective. A shape warning in review
   would be an amendment of the doctrine, not a realization of this capability.
3. **The advisory is silent where the shape question is answered or does not
   arise:** an elected Triad assembly root, a leg clone, a family holder, a
   `<user>-wip` workspace repository, and a project that has recorded staying
   single. The record is OPTIONAL, so a decliner still owes no declaration. Its
   only reader is the advisory, it confers nothing, and its schema is
   openRepoShape's. Every other repository receives the advisory, with no
   exemption by guessing its class.

## What does not change

- Every SHALL of the elective requirement. A project that never elects is
  reviewed identically, is not less governed, and owes no declaration.
- Who decides: the `PA`, per project, a human. Nothing converts a repository
  automatically.
- Every machine key, `kind`, field, file name and naming family.
- openRepoShape's PROJECT bootstrap, which stays schema-neutral and silent: a
  one-repository run "is not second-class for having declined" (`design.md` D2).
- codexFactory's recommending role and engineering overlay (OQ-3 below).
- The project register's fields. The staying-single record is not registered.

## What ratification decides

Each item below was RULED on 2026-10-06T16:02:16Z by Brett Heap's *"ratify 1249
as recommended"*, which took every recommendation as written. The items are
kept as filed, with the ruling marked on each.

1. **The reading itself** (`tasks.md` 1.1): preferred, not required; advised at
   work start, once; never in review. **RULED: ratified as written.**
2. **OQ-1, the staying-single record** (`design.md` D4). **RULED, as
   recommended: `single-repository.yaml` at the repository root, schema owned by
   openRepoShape.** Recommendation: its own
   file at the repository root, `single-repository.yaml`, with `schema_version`,
   `kind: single-repository-record`, who decided, when and why, and an optional
   revisit date; schema owned by openRepoShape. Overloading `project.yaml` is
   rejected because `project.yaml` with `kind: project-manifest` and spec and
   code legs IS the Triad detector for the shared protocol, `setup-openspeckit`
   and openRepoShape's doctor.
3. **OQ-2, aggregations, configuration repositories and vendored forks**
   (`design.md` D4). **RULED, as recommended: no class-guessing.**
   Recommendation: no class-guessing. They receive the advisory until they
   migrate or record staying single.
4. **OQ-3, ownership** (`design.md` D6). **RULED, as recommended: the advisory
   is not codexFactory's act of recommending the shape, and no block is
   written on the ownership requirement.** The promoted ownership requirement
   gives codexFactory "the act of RECOMMENDING the shape". Recommendation: the
   advisory restates the doctrine's preference at work start and is not that
   act, so no block is written on that requirement. If ratification reads it
   otherwise, the packet gains one `## MODIFIED` block there.

## Ratification record

**RATIFIED on 2026-10-06T16:02:16Z by Brett Heap**, in session, first-hand to
lane `codeXfactory-5`, verbatim: *"ratify 1249 as recommended"*. It is recorded
on PR #1249 (comment 6020300563) and in full at
[`review/ratification-2026-10-06.md`](review/ratification-2026-10-06.md). The
ratified text is the packet at PR #1249's head `8f9c5855`.

| question | decision | ruled | considered, not adopted |
| --- | --- | --- | --- |
| the reading (`tasks.md` 1.1) | preferred, not required; advised at work start, once; never in review | 2026-10-06T16:02:16Z | a warning in review or CI (A1); a mandatory Triad (A2); per-person suppression (A3); a blocking prompt (A4) |
| OQ-1 | `single-repository.yaml` at the repository root, schema owned by openRepoShape | 2026-10-06T16:02:16Z | a field or variant of `project.yaml`; a register field |
| OQ-2 | no class-guessing; such repositories get the advisory until they migrate or record staying single | 2026-10-06T16:02:16Z | exempting a class by inference |
| OQ-3 | the advisory restates doctrine and is not codexFactory's act of recommending; no block on the ownership requirement | 2026-10-06T16:02:16Z | a `## MODIFIED` block on the ownership requirement |

**Every ruling is the recommended option, so no delta byte moves.**
`specs/project-repo-schema/spec.md` is byte-identical to the text that was put
to ratification. Its third ADDED requirement already describes the record
without naming a file, which is what OQ-1 decides. It already refuses
class-guessing, which is OQ-2. And it carries no block on the ownership
requirement, which is OQ-3.

**The word ratifies and authorizes nothing further.** It is not a merge word:
this pull request stays held for Brett Heap's merge word. It is not a word to
realize anything: each `tasks.md` § 5 handoff waits on its own owner's act.
Nothing is promoted until the archive, which waits for merged, green realization
evidence (`tasks.md` § 6).

## Realization routing — handoffs, not performed here

Each of these is its owner's act after ratification, in its own repository and
under its own claims (`tasks.md` § 5):

- **openxFactory:** `docs/project-repo-schema.md` restated, with an `Amended by:`
  header line; the description of `contracts/schemas/project-register.schema.yaml`
  restated; `contracts/openreposhape-pin.yaml` advanced after openRepoShape
  realizes. The doctrine document is NOT edited in this pull request, following
  `amend-register-act-5b-projection-proof` (propose, ratify, then realize the
  document) — `design.md` D8.
- **`opensoft/openRepoShape`:** the README posture box; AGENTS.md § "What you
  must not tell them", still forbidding "confers anything" and gaining "the
  Triad is preferred"; the `templates/` manifest posture comment; the optional
  record's schema; the advisory in `scaffold-project.py`, `adopt-project.py` and
  `shape-doctor.py`.
- **`opensoft/workBenches`:** `setup-openspeckit`'s `resolve_project_shape()`
  advisory, its interactive question and its tests; then the embedded fallback
  protocol `openspec_speckit_protocol()` re-synced byte-identical to the shared
  protocol. Existing governing record: workBenches #22.
- **New-project creation:** workBenches' `project-command` change, held by lane
  `project-command`, which forwards to `opensoft/openRepoProject`'s `project
  new`. The Triad-first offer routes through that lane's claim, never around it.
- **The shared agent protocol:** source in the private repository
  `brettheap/new-workstation`, under `home/.agents/` — `AGENTS.md` (the shape
  bullet), `protocols/openspec-speckit-workflow.md` § "Repository Shape" /
  "Detecting the shape", and `protocols/project-agent-bootstrap.md`.
- **An estate inventory**, recommended and not performed: per repository,
  Triad / leg / family holder / workspace / single, and for each single
  repository a recommendation for its owner.

## Estate impact

Of the 22 submodule repositories the aggregation has checked out, three are
Triads (`openDox`, `openXdox`, `MedxEHR`) and 19 carry neither a project nor a
family manifest (`design.md` D7). So nearly every lane will meet the advisory
once per session until its repository migrates or records staying single. That
is the intended effect of the direction. The once-per-session, never-blocking
form keeps its cost to one line, and the optional record lets a repository that
has decided say so once.

## Alternatives rejected

`design.md` § Alternatives: a warning inside review or CI (it would break
"reviewed identically" and undo "confers nothing", so it needs a deliberate
amendment of the doctrine itself); a mandatory Triad; per-person suppression in
the person's workspace manifest (staying single is the project's `PA` decision,
not a viewer's preference); and a blocking prompt (Brett Heap's interrupt bar,
`docs/roles-and-authority.md`: the default must be to continue).

## Boundaries this packet holds

- No ratified document, schema description, template or pin is edited here;
  each is a § 5 handoff after ratification.
- No pin, gitlink, contract bundle or release tag moves.
- No act is taken in openRepoShape, workBenches, openRepoProject or the private
  protocol source.
- The lane register is not written by this packet.
