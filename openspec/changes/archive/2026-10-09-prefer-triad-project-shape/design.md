# Design: prefer-triad-project-shape

Status: ratified
Ratified by: prefer-triad-project-shape — 2026-10-06, Brett Heap, "ratify 1249 as recommended" (PR #1249 comment 6020300563), over PR #1249's head `8f9c5855` (record `review/ratification-2026-10-06.md`)
Kind: design

**RATIFIED 2026-10-06T16:02:16Z, as recommended.** Every decision below was
ratified as written, and OQ-1, OQ-2 and OQ-3 were each RULED to their
recommendation (marked where each is put). The paragraph that follows is kept
as filed.

Every decision below is PROPOSED for Brett Heap's ratification. His two
sentences of 2026-10-06 are the direction and the authority to author and open
this packet; they rule on no design point here, and nothing below says they do.
Each decision is stated with what it costs and how a different ruling would
change the text.

## D1 — Preferred is not required, so the elective requirement is kept whole and added to

The direction is *"the triad should be the prefered structure and should prompt
or warn the user if working on a non Triad repo."* The promoted requirement it
meets reads, at first glance, as its opposite: *"A project's repository
layout SHALL confer no gate, no floor, no grant, no clearance eligibility and no
lifecycle state, and a one-repository project and a three-repository project
SHALL be reviewed IDENTICALLY."* Those two statements are compatible only if
"preferred" is a recommendation to the person deciding and never a property of
the project. That is the reading this packet encodes.

So the MODIFIED block carries EVERY body sentence and all three promoted
scenarios verbatim, extracted by script and diffed against canon (`tasks.md`
§ 3.1), and ADDS: the preference, the name, the rule that the preference is
never stated without the posture, and two scenarios. The scenario *A project
declines the schema* keeps its bullet *"it is not less governed, is not reviewed
more suspiciously, and owes no declaration"* word for word, because that bullet
is the test of this whole packet: if a reader can find a way the preference
makes a decliner owe something, the packet has failed.

**The requirement's title does not change and no `## RENAMED` block is
written.** "Elective" and "confers nothing" are both still true after this
change, and renaming the requirement to lead with the preference would make the
first thing a reader meets the part that matters least to authority.

**Why the preference is in the MODIFIED requirement and not a fourth ADDED
one.** The canon requirement already says the posture must be restated wherever
the schema is recorded, "because a posture stated in one place is a posture the
second reader does not meet." A preference stated in a separate requirement is
exactly a preference a reader can meet without the posture. Putting it inside
the requirement that carries the posture, and adding the rule *"Wherever the
preference is stated, the posture above SHALL be stated with it"*, makes the two
travel together.

**The restatement rule is deliberately one-directional.** The posture may still
be stated alone: the register's REQUIREMENT TEXT in `ideation-dashboard`, which
canon lists among the places the posture is restated, is not touched, and a
posture without the preference misleads nobody. The preference may never be
stated alone. The places it IS restated are the three this capability's
realization already owns: the doctrine document, the register's schema
DESCRIPTION, and openRepoShape's assembly-root manifest template. That keeps
this packet to one capability.

## D2 — The advisory is given where a person starts work, once, at three surfaces

"Prompt or warn" needs a place. The place proposed is the moment a person STARTS
WORK on a repository, and only there:

| surface | form | why this form |
| --- | --- | --- |
| an agent session addressing a person | says it ONCE per session, then carries on | an agent that asked a question here would be interrupting a person for something that is neither a decision needing their authority nor a containment failure (`docs/roles-and-authority.md` § Parked decisions and § Interrupts); a statement costs one line and asks for nothing |
| a subagent, a delegated worker, an unattended run | says nothing | it addresses no person, so the advisory would reach nobody, and an unattended run that printed it would put shape text into output a review might read (D3) |
| the workstation bootstrap (`setup-openspeckit` in this estate), non-interactive | prints a warning; exit status unchanged | its tests and any scripted use see the same result they see today |
| the same bootstrap, interactive terminal | asks before continuing; continuing is the default | the person is already at the terminal running the command, so one question with Enter meaning "carry on" is the "prompt" the direction names, at the one moment it costs nothing extra |
| openRepoShape's scaffold, adopt and doctor | MAY report it beside what they already report; no exit status changes | these are the tools a person runs when the shape question is already in front of them |

**Once per session, and never a blocking prompt** — see A4 below.

**The interactive answer "no" is the person's own stop.** Taking the default
gives the run the person would have had without the advisory. Answering no ends
the run before it writes anything; that is the person choosing to stop, not the
advisory refusing, and the realization owner picks the exit status for it with
the rule that nothing reads that status as a verdict about the repository.

**What "offer the Triad first" means at creation.** In an interactive creation
the Triad is listed first and is the pre-selected answer. A non-interactive
invocation does what its flags say, and prints the recommendation when it
creates a single repository. No surface creates three repositories on a default:
openRepoShape's `setup.sh` keeps its own typed confirmation, which its AGENTS.md
already makes an agent unable to answer on a person's behalf.

**openRepoShape's PROJECT bootstrap is deliberately NOT an advisory surface.**
The promoted requirement *One bootstrap command follows a recursive clone, and
it degrades rather than fails* makes that command SCHEMA-NEUTRAL, and its
scenario *A one-repository project is bootstrapped* says the one-repository run
"is not second-class for having declined". A prompt there would make it
second-class. The workstation bootstrap that installs agent-workflow pointers is
a different tool, run when a person starts work, and is where the advisory
belongs.

**The advisory names two exits and takes neither.** It says how to convert
(openRepoShape's `adopt-project.py`, run by a person deciding for that project)
and how to stop meeting it (the staying-single record, D4). It converts nothing,
creates nothing, writes nothing, and records nothing about having been given,
so no later act can read "was advised" as a fact about the project.

## D3 — Never a review input, as its own requirement

The direction says to prompt or warn THE USER. A user is a person starting
work. A review lane, a required check, a council and a clearance are not users,
and the canon requirement forbids layout from being an input to any of them.
That is why the prohibition is its own requirement with its own scenarios rather
than a clause: it is the requirement a future proposer is most likely to argue
around ("it's only a warning in CI"), so it is written to be cited.

**What it does not forbid, stated so it is not over-read.** An electing
project's own conformance gate — the naming, lockstep-pin and manifest
validators the canon requirements give an assembly root, and the doctor run over
that root — checks the shape that project ELECTED against what it declared. It
never reaches a repository that did not elect, so it is not a shape reading in
this requirement's sense, and its scenario says so.

**The doctor's `NOT A SHAPE ROOT` verdict is named because it is the obvious
thing to wire into CI.** openRepoShape's `shape-doctor.py` already exits
non-zero for a directory with neither manifest, and its AGENTS.md already calls
that verdict "a question for the human, not a task". This packet changes nothing
about the doctor's exits. It forbids building a required check, review lane or
merge gate on that verdict, which is the one step that would turn the doctor
into the review warning A1 rejects.

**This also keeps a staged claim true rather than contradicting it.**
`ideation/staging/wallet-carried-work-authority/` claim 6 says the schema
"stays human-elected" and is falsifiable by "any gate, floor, grant or clearance
rule that reads a project's repository count after this lands". The requirement
that a project's shape is never a review input refuses that falsifier in
advance.

## D4 — The advisory's scope, the optional record, and two open questions

The advisory is silent in five places, each read from a declared fact rather
than inferred:

1. **An elected Triad assembly root** — the existing detector: `project.yaml`
   with `kind: project-manifest`, `schema: project-repo-schema` and `legs:`
   naming a `spec` and a `code` leg.
2. **A leg clone** — recognized by the `AGENTS.md` every leg ships from
   openRepoShape's `templates/spec-root/` and `templates/code-root/`, which
   names the leg's assembly root; the existing instruction to work from that
   root applies instead. The leg IS part of a Triad, so the advisory would be
   false there.
3. **A family holder** — `family.yaml` with `kind: family-manifest` and no
   `project.yaml`. It pins member projects and is not itself a project that
   could elect.
4. **A `<user>-wip` workspace repository** — openRepoShape's README classifies
   it as a naming family of its own in `contracts/repository-naming.yaml`, and
   openRepoShape's AGENTS.md says it "holds no code, elects nothing and is
   membership of nothing". It is identified by that declared naming family or
   because the person's own workspace configuration names it.
5. **A project that has recorded staying single.**

**The record is OPTIONAL, which is what keeps "owes no declaration" true.** A
project that declines and records nothing owes nothing and is reviewed
identically; the only difference is that it meets one line once per session. A
project that would rather not meet it can write the record. Its only reader is
the advisory; it confers nothing and restates that where it is recorded; and
its schema is openRepoShape's, as mechanics.

### OPEN QUESTION OQ-1 — the record's file name, location and schema — RULED 2026-10-06T16:02:16Z

**RULED, as recommended.** Brett Heap, verbatim *"ratify 1249 as
recommended"*: the optional staying-single record is `single-repository.yaml`
at the repository root, and openRepoShape owns its schema. The recommendation
and its reasoning below are kept as filed.

**Recommendation:** a file of its own at the repository root,
`single-repository.yaml`, carrying `schema_version: 1`,
`kind: single-repository-record`, `decided_by` (the person who decided for the
project, as for an election), `decided_on`, `reason`, and an optional
`revisit_on`, with a header comment restating that it confers nothing and that
only the advisory reads it. Its schema and template live in openRepoShape beside
the other manifest templates, and openRepoShape's doctor may recognize it. The
project register gains no field for it: the register is navigation, and a
staying-single marker there would be a second reader.

**Why at the root:** the same root read that looks for `project.yaml` finds it,
so detection costs no second walk, and the two can never be confused because
their file names and their `kind`s differ.

**Why overloading `project.yaml` is rejected:** `project.yaml` carrying
`kind: project-manifest` with spec and code legs IS the Triad detector — in the
shared agent protocol's "Detecting the shape", in `setup-openspeckit`'s
`resolve_project_shape()`, and in openRepoShape's doctor, whose `NOT A SHAPE
ROOT` verdict keys on that file's absence. A single repository carrying a
`project.yaml` would turn every one of those readers from a presence test into a
content test, would make the doctor find a manifest where today it finds none
and judge a repository that never elected as a malformed shape root, and would
put a staying-single fact into the file the canon
requirement makes "the SOURCE" from which a register row is derived, where a
register derivation could read it as an election. A separate file has none of
those costs.

**What a different ruling changes:** the record's sentences in the third ADDED
requirement name no file, so a different name, location or schema is a change to
`tasks.md` § 5.2's handoff and to this section, not to the spec. A ruling that
there should be NO record at all would delete the fifth bullet and the
record paragraph from that requirement, and every decliner would then meet the
advisory for good.

### OPEN QUESTION OQ-2 — aggregations, configuration repositories and vendored forks — RULED 2026-10-06T16:02:16Z

**RULED, as recommended.** Brett Heap, verbatim *"ratify 1249 as
recommended"*: no class-guessing. Aggregations, configuration and dotfile
repositories, and vendored forks get the advisory until they migrate or record
staying single. The recommendation and its reasoning below are kept as filed.

**Recommendation: no class-guessing.** An aggregation repository such as
`opensoft/xFactory`, a configuration or dotfile repository, and a vendored fork
receive the advisory like any other single repository until they migrate or
record staying single. For most of them the expected outcome is a one-line
record, written once.

**Why not exempt them by class:** none of the three carries a declared fact that
says what it is. An exemption would have to infer the class from a name, a
file layout or a remote, and every such inference is a rule that is right for
the repositories its author had in mind and wrong for the next one. The five
exemptions in D4 are each a declared fact; adding inferred ones would make the
list unbounded and the advisory unpredictable. The record already gives any
such repository a one-step way out.

**What a different ruling changes:** if ratification wants a class exempt, the
remedy is to give that class a declared fact (a naming family in openRepoShape's
naming policy, as `<user>-wip` already has) and add it to the list, not to guess.

## D5 — The name "Triad"

"Triad" is already the estate's word for the openRepoShape three-repository
shape: the shared agent protocol's section "Triad Feature Amendments" (adopted
2026-10-04) uses it, `opensoft/workBenches#135` lands that adopted change, and
Brett Heap's direction uses it. No openRepoShape document does yet. The two
changes do not overlap: workBenches#135 governs how a project that is already a
Triad amends its features, and its Copilot thread `4194811387` asks for the
2026-10-06 direction to be recorded as a deferred follow-up. This packet is
where that direction is governed. The proposal makes it the human-facing name, including in the
advisory, keeps "three-leg project" and "three-repository project" as accepted
synonyms so no existing document becomes wrong, and renames no machine key,
`kind`, field, file name or naming family: `project-manifest`,
`project-repo-schema`, `legs[].role` and every other key a reader parses stay
exactly as they are.

## D6 — Ownership, and a third open question

The promoted requirement *codexFactory carries the engineering overlay and
OpsxFactory carries organisation naming and topic administration* splits
ownership four ways — openRepoShape the mechanics, openxFactory the doctrine,
codexFactory the engineering overlay "and the act of RECOMMENDING the shape",
OpsxFactory organisation administration — and says the split "SHALL NOT be
re-concentrated".

This packet puts the PREFERENCE in the doctrine (openxFactory's plane) and the
ADVISORY in openRepoShape's mechanics, in the workstation bootstrap and in the
shared agent protocol. None of those is codexFactory.

### OPEN QUESTION OQ-3 — does the advisory re-home codexFactory's recommending act? — RULED 2026-10-06T16:02:16Z

**RULED, as recommended.** Brett Heap, verbatim *"ratify 1249 as
recommended"*: the advisory restates the doctrine's preference and is not
codexFactory's "act of RECOMMENDING the shape", so no `## MODIFIED` block is
written on the ownership requirement. The recommendation and its reasoning
below are kept as filed.

**Recommendation: no, and no block is written on that requirement.** That
requirement's own scenario describes the recommending act as codexFactory
recommending the shape TO A PROJECT, after which "the human project manager
still decides, the election being theirs". The advisory is the doctrine's preference restated to whoever is at
the keyboard when work starts, through tooling that is not engineering-domain.
codexFactory keeps its recommending role and its engineering overlay in full
and unchanged, and nothing is concentrated: the advisory is spread across three
surfaces that are none of the four owners' exclusive property.

**What a different ruling changes:** if ratification reads the advisory as that
act, this packet gains a `## MODIFIED` block on that requirement naming the
advisory's surfaces beside codexFactory's role. That is one more block and it
changes no other sentence here.

## D7 — Estate impact, stated rather than discovered

**Nearly every repository in this estate is a single repository today.**
Measured on 2026-10-06 over the aggregation's own submodule checkouts: of the 22
checked out, THREE carry a `project.yaml` with `kind: project-manifest` and
`schema: project-repo-schema` — `opensoft/openDox`, `opensoft/openXdox` and
`MedxSoft/MedxEHR` — and those are the Triads; the other 19 carry neither a
`project.yaml` nor a `family.yaml`. So **every lane will meet the advisory once
per session** in nearly every repository it works in, until that repository
migrates or records staying single. (The measurement read local checkouts, not
each repository's `origin/main`; the inventory below re-measures on origin.)

That is the intended effect of the direction, and the once-per-session,
non-blocking form keeps its cost to one line per session. It is also why the
optional record exists: a repository that has decided to stay single should be
able to say so once and stop hearing about it.

**An estate inventory is recommended as a realization task and is NOT performed
here** (`tasks.md` § 5.7): for each repository in
`scripts/estate-repository-inventory.yaml`, whether it is a Triad, a leg, a
family holder, a workspace repository, or a single repository, and for each
single repository a recommendation — migrate, or record staying single — for its
owner to decide. The inventory recommends; it converts and records nothing.

## D8 — The doctrine document is not edited in this pull request

**Precedent followed:** `amend-register-act-5b-projection-proof`, the closest
recent change that amended ratified text and its governing document. It was
proposed with no document edit (`07b72078`), ratified (`5daa96ec`), and the
governing document was then realized under its own `tasks.md` § 3 with an
`Amended by:` header line naming the change (`0446dece`). The same order holds
for `split-ideation-book-per-repo` against the `Status: standard`
`docs/lifecycle-notebook-projection.md`: propose (`95ba14c3`), ratify
(`201e5bc5`), realize the document (`d2fcae43`). No recent amending change
edited its ratified document in the proposal commit.

So `docs/project-repo-schema.md` and the description in
`contracts/schemas/project-register.schema.yaml` are NOT edited here. After
ratification, the realization adds the preference beside the posture in both,
and the doctrine document gains an `Amended by: prefer-triad-project-shape
(ratified <date>)` header line (`tasks.md` § 5.1). Editing ratified doctrine
text before its amendment is ratified would put an unratified sentence into a
document whose header says `Status: ratified`.

## D9 — Why the code-surface head names two repositories when the realization reaches five

The head is `openxFactory, opensoft/openRepoShape`, and those are the only two
surfaces that `scripts/estate-repository-inventory.yaml` carries.
`opensoft/workBenches`, `opensoft/openRepoProject` and the private repository
that is the shared agent protocol's source are not in the inventory. The
inventory's own header says a row records an admission and performs none — a
repository joins the estate when a governed tree names it — so writing rows here
to make the head pass would be inventing an admission. The membership arm of
`scripts/validate-code-surface.py` fails an identifier the inventory does not
carry.

They are therefore named in the gloss as HANDOFFS to their owners, each with a
`tasks.md` box that this packet's archive waits on. The two repositories in the
head are the ones the house validators can resolve; for the other three, the
archiving actor checks the boxes and cites each one's evidence in the archive
record.

## D10 — No `sequenced_after:` declaration

The only other change that writes this requirement is `add-project-repo-schema`,
archived 2026-09-03, which ADDED it. No active change carries a delta on
`project-repo-schema`, so there is no ordering for `release-realization`'s
"Ordered deltas" rule to settle, and the field is left absent, which is the
lawful default. The per-change sweep ledger reads this packet as a CO-MODIFIER
(`declares: absent`), because it writes a requirement key the archived change
also wrote; seeding moved this packet's row and no other (`tasks.md` § 2.4).

## Alternatives considered and rejected

**A1 — Warn inside review or CI.** A required check, a review-lane comment or a
council note saying "this repository is not a Triad" is the most visible form of
"warn", and it is rejected because it makes layout a review input. The canon
requirement says a one-repository and a three-repository project "SHALL be
reviewed IDENTICALLY"; a review that says something about one and not the other
is not identical, even when it does not fail. And it would undo "confers
nothing" in practice: a warning in review output is a cost a project carries for
its layout, and the next consumer reads it as a signal. Wanting it would need a
deliberate amendment of the doctrine itself, which the second ADDED requirement
says in so many words.

**A2 — Make the Triad mandatory.** Rejected. It contradicts every SHALL of the
canon requirement, and the direction says "preferred", not "required". A
mandatory shape would also make the openRepoShape fork-and-run case, an
organisation with no openxFactory, owe something to a doctrine it never adopted.

**A3 — Per-person suppression in the person's workspace manifest.** A person
could switch the advisory off for themselves in their own workspace
configuration. Rejected because whether a project stays single is the project's
`PA` decision, not a viewer's preference: a suppression held by one person would
leave every other person working in that repository meeting the advisory for a
decision that had already been made, and would let one person silence the
preference for a project they do not decide for. The project-level record puts
the decision where the election would have been. The once-per-session form
already keeps the per-person cost to one line.

**A4 — A blocking prompt.** An agent that stopped and asked, or a bootstrap that
refused until the person answered a shape question, is rejected under Brett
Heap's interrupt bar, codified in `docs/roles-and-authority.md`: decisions that
need a human park and "never interrupt", and an interrupt is legal only on
containment failure. A non-Triad repository is neither a decision the person
must make before working nor a containment failure. The interactive bootstrap
question survives only because the person is already at that terminal running
that command, and its default is to continue.
