# project-repo-schema Specification

**ONE `## MODIFIED` REQUIREMENT AND THREE `## ADDED` REQUIREMENTS.** The
MODIFIED block restates *The project repository schema is elective and confers
nothing* as canon states it, and adds to it. Every body sentence and all three
promoted scenarios are carried VERBATIM, extracted by script from
`openspec/specs/project-repo-schema/spec.md` rather than retyped, so nothing
the promoted requirement says is removed, narrowed or reworded and no `Removed
from canon` marker is owed. What the block ADDS is the preference, the name
"Triad", the rule that the preference is never stated without the posture, and
two scenarios. No active change carries a delta on this capability (checked by
enumerating `openspec/changes/*/specs/` on `main` `92010d3e`), so there is no
ordering to declare and the block is written over canon as promoted.

**THE THREE ADDED REQUIREMENTS SAY WHERE THE PREFERENCE MAY BE SPOKEN AND WHERE
IT MAY NOT.** It is advised where a person starts work, once, and never stops
anyone; it is never a review input; and it is silent where the shape question
is already answered or does not arise. The title of the modified requirement
does not change: the schema is still elective and still confers nothing, and
that is the point of the whole packet.

## MODIFIED Requirements

### Requirement: The project repository schema is elective and confers nothing
A project's repository layout SHALL confer no gate, no floor, no grant, no
clearance eligibility and no lifecycle state, and a one-repository project and a
three-repository project SHALL be reviewed IDENTICALLY. Electing this schema is a
`PA` decision, `CA`-constrained and `PM`-sequenced
(`docs/roles-and-authority.md:67-74`), taken per project by a human, and it is
never a precondition of review. This restates rather than extends the ratified
doctrine of `add-wallet-carried-review-authority` — *"Electing the schema changes
no gate, no floor, no grant, and no clearance eligibility"* — and binds every
artifact this capability defines: a consumer that derives any permission from a
naming family, a leg role, a register field or a manifest field is DEFECTIVE, and
the defect is the consumer's rather than the declaration's.

The posture SHALL be restated wherever the schema is recorded — in the doctrine
document, in the register's schema description and requirement text, and in the
assembly root's own manifest — because a posture stated in one place is a posture
the second reader does not meet.

The three-repository shape is nonetheless the PREFERRED project shape, and
preferred SHALL NOT be read as required. It SHALL be the recommended default for
a new project and the recommended migration target for an existing
single-repository project. The recommendation is made TO the person deciding and
never in their place: electing remains the `PA` decision above, taken per
project by a human, and converting an existing repository remains
openRepoShape's `adopt-project.py`, run by a person deciding for that project.
The preference adds no gate, no floor, no grant, no clearance eligibility, no
lifecycle state and no review difference, so every sentence above holds
unchanged.

In human-facing text, including the advisory this capability defines, the shape
SHALL be called the Triad, with "three-leg project" and "three-repository
project" kept as accepted synonyms. The name is vocabulary only: no machine key,
`kind`, field, file name or naming family is renamed by it.

Wherever the preference is stated, the posture above SHALL be stated with it, so
that no reader meets "preferred" without also meeting "confers nothing". The
preference SHALL be restated beside the posture in the doctrine document, in the
register's schema description and in the assembly-root manifest template.

#### Scenario: A project declines the schema
- **WHEN** a project keeps all of its work in one repository and declares no schema election
- **THEN** it is reviewed identically to a project that elected the three-repository shape
- **AND** it is not less governed, is not reviewed more suspiciously, and owes no declaration

#### Scenario: A project elects the schema
- **WHEN** a `PA` elects the shape for a project and records the election
- **THEN** the project earns no additional clearance, grant, floor or gate standing
- **AND** the election is descriptive navigation, exactly as the project register's existing posture already states for grouping

#### Scenario: A consumer reads a permission out of the layout
- **WHEN** a tool treats a leg role, a naming family or a register election as evidence of authority over a repository
- **THEN** that consumer is defective and its reading MUST NOT be honoured
- **AND** the remedy is to read authority from the grants, which is where the authority travels

#### Scenario: A person creates a new project
- **WHEN** a person creates a new project through a tool or an agent
- **THEN** the Triad is offered first, as the recommended default
- **AND** a single repository chosen instead is accepted without a reason being asked, is reviewed identically, and owes no declaration

#### Scenario: An existing single-repository project has not elected the Triad
- **WHEN** an existing single-repository project has not elected the Triad
- **THEN** the Triad is its recommended migration target, and it is converted only when a person deciding for that project runs openRepoShape's `adopt-project.py`
- **AND** nothing converts it automatically, and until a person decides it is reviewed identically to a project that elected

## ADDED Requirements

### Requirement: A person starting work outside a Triad is advised once, and is never stopped for it
A surface where a person starts work SHALL advise a project that has not elected
the Triad that the Triad is the preferred project shape, and the advisory SHALL
be given only at such surfaces and only in these forms:

- an agent session addressing a person SHALL say it once per session and then carry on with the work it was asked to do; a subagent, a delegated worker and an unattended run address no person and SHALL NOT say it;
- the workstation bootstrap that installs a repository's agent-workflow pointers SHALL print it as a warning in a non-interactive run, with its exit status unchanged, and in an interactive terminal SHALL ask before continuing, with continuing as the default answer;
- openRepoShape's scaffold, adopt and doctor surfaces MAY report it beside what they already report, and SHALL NOT change an exit status on its account.

Where a person creates a new project, the creating tool or agent SHALL offer the
Triad first, as the recommended default, and SHALL create no repository the
person has not confirmed.

The advisory SHALL name the way to convert — openRepoShape's `adopt-project.py`,
run by a person deciding for that project — and the way to stop meeting it — the
optional staying-single record — and SHALL convert nothing. No surface converts a
repository, creates one, or writes a manifest or a record on the advisory's
account. The advisory is a sentence said to a person and not a state: it records
nothing, and no later act reads whether it was given.

#### Scenario: An agent session starts work in a single repository
- **WHEN** an agent session addressing a person starts work in a repository that has not elected the Triad and carries no staying-single record
- **THEN** it says once that the Triad is the preferred project shape, naming how to convert and how to record staying single
- **AND** it does not say it again in that session, and it carries on with the work it was asked to do

#### Scenario: A subagent or an unattended run starts in the same repository
- **WHEN** a subagent, a delegated worker or an unattended run starts work in that repository
- **THEN** it gives no advisory, because it addresses no person

#### Scenario: The bootstrap runs without an interactive terminal
- **WHEN** the workstation bootstrap runs non-interactively in a repository that has not elected the Triad
- **THEN** it prints the advisory as a warning
- **AND** it writes what it would have written without the advisory and exits with the status it would have exited with

#### Scenario: The bootstrap runs in an interactive terminal
- **WHEN** the workstation bootstrap runs in an interactive terminal in a repository that has not elected the Triad
- **THEN** it asks before continuing, with continuing as the default answer
- **AND** a person who takes the default gets exactly the run they would have had without the advisory

#### Scenario: Nothing converts on the advisory's account
- **WHEN** the advisory is given on any surface
- **THEN** no repository is converted, created or rewritten because of it
- **AND** nothing records that it was given

### Requirement: A project's shape is never a review input
No review lane, required check, validator, floor, merge gate, clearance, council
or other review surface SHALL read whether a project elected the Triad, whether
it recorded staying single, or whether the advisory was given, in order to pass,
fail, warn in review output or change any eligibility. The preference lives at
the surfaces where a person starts work and review never meets it, which is what
keeps a one-repository project and a three-repository project reviewed
IDENTICALLY now that one of them is preferred.

An electing project's own conformance gate is not such a reading. The validators
the requirements above give an assembly root — naming, the lockstep pin and
manifest conformance — check the shape a project ELECTED against what it
declared, and none of them fails, warns or changes eligibility because a
repository did not elect. openRepoShape's doctor answers a person's question
about one repository, and its `NOT A SHAPE ROOT` verdict is an answer to that
person: no required check, review lane or merge gate SHALL be built on it, or on
any other reading of whether a repository is a Triad.

A shape warning placed inside review — a required check, a review comment, a
council finding — would make layout a review input, which the requirement *The
project repository schema is elective and confers nothing* forbids. It is
therefore not a realization of this capability but an amendment of that
doctrine, and SHALL be proposed as one if it is ever wanted.

#### Scenario: A single-repository project reaches review
- **WHEN** a project that has not elected the Triad opens a pull request where review lanes and required checks run
- **THEN** none of them reads its shape, and its review output carries no shape warning
- **AND** it is reviewed identically to a project that elected the Triad

#### Scenario: A check is proposed that warns on a non-Triad repository
- **WHEN** a required check, review lane or merge gate is proposed that would pass, fail or warn according to whether a repository is a Triad
- **THEN** it is refused as a realization of this capability
- **AND** it can be proposed only as an amendment of the doctrine that the shape confers nothing

#### Scenario: An electing project's own gate runs
- **WHEN** an assembly root's own gate runs its naming, lockstep-pin and manifest validators, or the doctor over its own root
- **THEN** they check the shape that project elected, as the requirements above already require
- **AND** none of them is a shape reading in the sense of this requirement, because none of them reaches a repository that did not elect

#### Scenario: A workflow gates a merge on the doctor's verdict
- **WHEN** a workflow fails or blocks a merge because the doctor answered `NOT A SHAPE ROOT`
- **THEN** that workflow is defective, as a consumer deriving a permission from layout is defective
- **AND** the verdict remains an answer to the person who asked

### Requirement: The advisory is silent where the shape question is answered or does not arise
The advisory SHALL NOT be given in any of the following, each read from a
declared fact — the repository's own tree, the pinned naming policy, or the
person's own configuration — and never inferred:

- an elected Triad assembly root: `project.yaml` carrying `kind: project-manifest`, `schema: project-repo-schema` and `legs:` naming a `spec` and a `code` leg;
- a leg clone, where the existing instruction to move to the assembly root applies instead;
- a family holder: `family.yaml` carrying `kind: family-manifest`, with no `project.yaml`, which pins member projects and is not itself a project;
- a `<user>-wip` workspace repository, which holds no code and elects nothing, identified by the naming family openRepoShape's naming policy declares for it or because the person's own workspace configuration names it;
- a project that has recorded that it is staying a single repository.

The staying-single record SHALL be OPTIONAL, so a project that declines the
Triad still owes no declaration: one that records nothing is reviewed
identically and meets only the advisory. Where a project records it, the record
SHALL be a small project-level file of its own, carrying `schema_version`,
`kind`, and who decided, when and why. It SHALL NOT be `project.yaml` or a field
of it, because `project.yaml` with `kind: project-manifest` and a spec and a
code leg is how every surface detects a Triad. Its only reader SHALL be the
advisory. It SHALL confer nothing — no gate, no floor, no grant, no clearance
eligibility, no lifecycle state and no review difference — and SHALL restate
that posture where it is recorded. Its schema SHALL be owned by openRepoShape as
mechanics, as the rest of this schema's mechanics are.

Every other repository — an aggregation, a configuration or dotfile repository,
a vendored fork, or any class a tool might infer — SHALL receive the advisory
until it migrates or records staying single. No surface SHALL exempt a
repository by guessing its class: the list above is the whole list.

#### Scenario: Work starts in an elected Triad
- **WHEN** a person starts work in an assembly root whose `project.yaml` declares the schema with a spec and a code leg
- **THEN** no advisory is given

#### Scenario: Work starts in a leg clone
- **WHEN** a person starts work in a clone of a Triad's spec or code leg
- **THEN** no advisory is given
- **AND** the instruction to move to the assembly root is given instead

#### Scenario: Work starts in a family holder or a workspace repository
- **WHEN** a person starts work in a family holder, or in a `<user>-wip` workspace repository
- **THEN** no advisory is given, neither being a project that could elect

#### Scenario: A project has recorded staying single
- **WHEN** a single-repository project carries the staying-single record
- **THEN** the advisory is not given for it
- **AND** the record gains it nothing else — no gate, no floor, no grant, no clearance eligibility and no review difference

#### Scenario: A project declines without recording anything
- **WHEN** a single-repository project declines the Triad and records nothing
- **THEN** it owes nothing and is reviewed identically
- **AND** it meets the advisory once per session wherever a person starts work in it

#### Scenario: A repository whose class a tool could guess
- **WHEN** a person starts work in an aggregation, a configuration repository or a vendored fork that has neither elected the Triad nor recorded staying single
- **THEN** the advisory is given, as for any other single repository
- **AND** no surface exempts it by inferring what class of repository it is
