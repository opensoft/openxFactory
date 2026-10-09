# project-repo-schema Specification

## Purpose
Defines the neutral, ELECTIVE project repository shape — SPEC / CODE / ASSEMBLY,
one per-project root an engineer clones — that a project MAY adopt for
ergonomics: the naming families, the double pin (gitlink plus a pin file plus
every workflow `@<sha>` moving in one commit), the manifest-is-the-source rule
with a derived register row, the bootstrap contract and its schema-neutral
degrade line, and the ownership split between this doctrine, the neutral
public `opensoft/openRepoShape` standard the mechanics live in, and
codexFactory's engineering overlay on it. Electing the shape CONFERS NOTHING —
no gate, no floor, no grant, no clearance eligibility — and a project that
declines it is reviewed identically to one that elects it; every authority
question is deferred by name to `wallet-carried-work-authority`.

## Requirements

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

### Requirement: The assembly leg is the per-project root, and it may pin shared assembly code as an overlay
A project electing this schema SHALL have exactly one ASSEMBLY leg, and that leg
SHALL BE the per-project ROOT repository an engineer clones — the repository that
carries the project manifest, mounts the other legs and runs the project's own
gate. Ruled by Brett Heap, 2026-09-02, verbatim: *"yes, assembly is per
project."* The assembly root MAY additionally PIN shared review-team assembly
code — from codexFactory or from anywhere else — at a commit, as an OVERLAY, in
the way the xFactory aggregation already consumes its review lane at
`review-lane-reusable.yml@<sha>`; that pin is optional and its absence is
conformant.

This resolves the ratified sentence *"ASSEMBLY (the code that assembles a review
team, shared across the family)"* (`add-wallet-carried-review-authority`,
`proposal.md:608`) WITHOUT contradicting it: the per-project root is the leg, and
the shared code is content that root may pin. Under the alternative reading an
electing project has a SPEC leg and a CODE leg and no front door, which answers
none of the questions this capability exists to answer.

#### Scenario: An engineer clones an electing project
- **WHEN** an engineer is given a project that has elected the schema
- **THEN** the assembly root is the one repository they clone, and it brings the other legs with it
- **AND** they need no list of repositories held anywhere else

#### Scenario: A project pins shared review-team assembly code
- **WHEN** an assembly root pins shared review-team code at a commit as an overlay
- **THEN** both readings of the ratified sentence hold — the leg is the root and the shared code is what it pins
- **AND** a project that pins no such code is fully conformant

### Requirement: A project's repositories are named `<Project>`, `<Project>-spec` and `<Project>-code`
An electing project's repositories SHALL be named `<Project>` for the assembly
root, `<Project>-spec` for the spec leg and `<Project>-code` for the code leg,
where `<Project>` is ONE CamelCase token carrying no hyphen, underscore, dot or
space, and the two suffixes are fixed LOWERCASE and hyphenated. Every repository
of the project SHALL also carry the GitHub topic `xf-project-<id>`, where `<id>`
is the project's lowercase id.

The suffixes are lowercase and hyphenated precisely so they sit in a different
visual class from every family the pinned standard's naming policy spells as a
CamelCase word, and the assembly root is BARE because the thing you clone has no
suffix — the precedent the aggregation root already sets. A name matching no
family at all is REFUSED rather than accepted as a residual, which is the check
that earns its keep: this is a FORWARD rule, and two live repositories
(`xFactory-Installer`, `AgentTower`) fit no suffix rule, so the rule describes
what may be created and never retroactively condemns what exists.

**Removed from canon by correct-naming-families-count (2026-10-07):** ``The suffixes are lowercase and hyphenated precisely so they sit in a different visual class from every other live family, all of which are CamelCase words, and the assembly root is BARE because the thing you clone has no suffix — the precedent the aggregation root already sets.`` — REPLACED, not dropped: the paragraph above restates it with one clause changed. Its claim that every other family is a CamelCase word has been false at the pin in force since openxFactory's openRepoShape pin moved to `1a9fc537` (openxFactory PR #1260, 2026-10-06), because that commit's naming policy declares the `workspace` form `<user>-wip`, which is lowercase and hyphenated (openRepoShape PR #86). The replacement keeps what the sentence is for, that the leg suffixes are told apart from the CamelCase forms, and states no property of the whole set of families. The removed unit carries no SHALL, and its clause about the bare assembly root is carried word for word.

#### Scenario: A project is scaffolded
- **WHEN** a project named `Atlas` elects the schema
- **THEN** its repositories are `Atlas`, `Atlas-spec` and `Atlas-code`, and each carries the topic `xf-project-atlas`

#### Scenario: A leg name uses the wrong case or separator
- **WHEN** a proposed leg name is `Atlas-SPEC`, `Atlas_spec` or `Atlas-tests`
- **THEN** it is refused before anything is created
- **AND** the refusal names the form that would have been accepted

#### Scenario: An existing repository fits no family
- **WHEN** a repository that predates this rule matches no naming family
- **THEN** it is not thereby non-conformant, this being a forward rule over what may be created

### Requirement: The naming families are governed by the pinned standard, and a descendant form is a claim that needs a declared pin
The naming families SHALL be those the naming policy of the pinned openRepoShape
standard (`contracts/repository-naming.yaml`) declares, governed there as DATA
rather than by prose and restated here by neither their number nor their full
list — among them `open<Product>` neutral products, `<X>-Install` installs,
`<Domainx><Product>` domain descendants, and the project legs above — and a
`<Domainx><Product>`-shaped name SHALL be classified as a domain descendant
ONLY where the project DECLARES a pin on the matching `open<Product>`. Ruled by
Brett Heap, 2026-09-02, choosing from three options presented: *"Descendant only
if it pins open&lt;Product&gt;."* Absent that declared pin the project's DECLARED
ROLE wins, the name is a valid assembly root, and the project manifest SHALL
RECORD that the name ALSO MATCHES the descendant form rather than discarding the
overlap.

A family the pinned policy adds or retires at a later pin owes this capability
no amendment for its count or its listing: how many naming families there are,
and which, is read from the policy at the pin in force and not from this
specification. A count or a closed list restated here would be a second
statement of a fact the pinned data owns, and it would go stale at the first pin
that moved it — which is what this requirement's promoted text did twice, at
openxFactory's openRepoShape pin advances of 2026-09-04 and 2026-10-06.

**Removed from canon by correct-naming-families-count (2026-10-07):** ``The four live naming families SHALL be governed as DATA by the naming policy of the pinned openRepoShape standard (`contracts/repository-naming.yaml`) rather than by prose — `open<Product>` neutral products, `<X>-Install` installs, `<Domainx><Product>` domain descendants, and the project legs above — and a `<Domainx><Product>`-shaped name SHALL be classified as a domain descendant ONLY where the project DECLARES a pin on the matching `open<Product>`.`` — REPLACED, not dropped, and the replacement is this change's whole object. The promoted sentence was true at the pin in force when it was promoted on 2026-09-03, `deacbdc`, whose naming policy declared four families. openxFactory's pin moved to `122d729b` on 2026-09-04 (openxFactory PR #650), whose policy declares five, the `family` holder having been added by openRepoShape PR #16; and to `1a9fc537` on 2026-10-06 (openxFactory PR #1260), whose policy declares six, the `workspace` form `<user>-wip` having been added by openRepoShape PR #86. The paragraph above restates the sentence with its count and its closed list removed and with the four forms it named kept as named members, and carries its descendant clause word for word. Every SHALL the removed unit stated is carried: the families stay governed as DATA by the pinned policy, and a descendant-shaped name is still a descendant only on a declared pin.

The classification SHALL be decided OFFLINE, from facts in the project's own
tree, and SHALL NOT ask any host whether `open<Product>` exists — a rule needing
the network is unrunnable in the fork-and-run case this capability exists for.
`open<Product>` and `<X>-Install` are unambiguous in their own characters and
keep their precedence unchanged; `<Domainx><Product>` is not, its form being a
CLAIM of descent that the characters alone cannot settle, which is why it
carries a referent. This narrows NOTHING in
`domain-descendant-boundary`: a descendant is still a descendant because it pins
the product, which is what that capability already requires.

**Removed from canon by correct-naming-families-count (2026-10-07):** `` `open<Product>` and `<X>-Install` are unambiguous in their own characters and keep their precedence unchanged; `<Domainx><Product>` is the one family whose membership is not decided by the characters alone, which is why it is the one family carrying a referent. `` — REPLACED, not dropped: the paragraph above restates it with its second clause changed. `<Domainx><Product>` stopped being the ONLY family whose membership the characters alone do not decide when openxFactory's pin moved to `122d729b` (openxFactory PR #650, 2026-09-04), because that commit's naming policy declares the `family` holder form DECLARED-ONLY, the characters of a holder's name being those of an assembly root (openRepoShape PR #16). The replacement keeps the sentence's point, that the descendant form is a claim and carries a referent for that reason, and makes no claim about the rest of the set. Its first clause, on `open<Product>` and `<X>-Install`, is carried word for word.

#### Scenario: A descendant-shaped name declares the matching pin
- **WHEN** a repository named `MedxChart` declares a pin on `openChart`
- **THEN** it classifies as a domain descendant, on the strength of the pin rather than the spelling

#### Scenario: A descendant-shaped name declares no matching pin
- **WHEN** a repository named `MedxScribe` is declared as an assembly root and no `openScribe` pin is declared
- **THEN** the declared role wins and the name is a valid assembly root
- **AND** the manifest records that it also matches the descendant form, so a resolved overlap stays visible to the next reader

#### Scenario: The classifier is asked to reach the network
- **WHEN** classification would require asking a host whether a neutral product repository exists
- **THEN** the classification MUST instead be decided from the project's declared pins
- **AND** a rule that reached the network would be unrunnable in an organisation that forked the standard and never speaks upstream

#### Scenario: The pinned policy declares a family no requirement here names
- **WHEN** openxFactory's openRepoShape pin advances to a naming policy that declares a family no requirement of this capability names
- **THEN** that family is a naming family from that pin on, governed as data by the pinned policy
- **AND** no requirement of this capability is amended to restate how many families there are or which, the pinned policy being where both are read

### Requirement: Each leg is pinned twice, and the pins and every workflow reference move in one commit
An assembly root SHALL pin each non-assembly leg TWICE — by the GITLINK git
records for the submodule, and by `contracts/<role>-pin.yaml` carrying
`revision_kind: commit`, the exact commit and a digest — and the gitlink, the
pin file's `commit:`, and EVERY workflow reference naming that leg at a sha SHALL
move in ONE commit. A tag MAY be recorded beside the commit as a human-readable
label, never as the thing being trusted, and a pin SHALL NOT express a range.
The assembly root's own pull-request gate SHALL run a validator that refuses when
the three disagree, and the refusal SHALL name what to run.

The pin grammar is REUSED and not invented: this is `domain-descendant-boundary`'s
same-commit rule and `neutral-product-pin`'s commit-and-digest rule, applied to a
consumer that is new. **The lockstep invariant is a MEASURED cost and not a
hypothesis.** In the xFactory aggregation the same invariant was practice for
months and written down nowhere; seven consecutive pin-syncs from 2026-08-25
moved the gitlink alone and left `validate` red on every aggregation pull request
until 2026-08-26 (xFactory #146), unnoticed for a day because `validate` runs on
pull requests only, so `main` never reports it. Shipping the validator in the
template makes that a one-time scaffold cost instead of a per-project rule
somebody has to remember.

#### Scenario: A leg's pin is advanced
- **WHEN** an assembly root advances a leg to a new commit
- **THEN** the gitlink, `contracts/<role>-pin.yaml` and every workflow reference at that leg's sha move in the same commit
- **AND** a commit moving fewer than all three is refused by the assembly root's own gate

#### Scenario: A pin names a tag rather than a commit
- **WHEN** a leg pin declares a tag, a branch or a range as its referent
- **THEN** the pin is refused, because a tag can be moved and a commit cannot

#### Scenario: The gate refuses without saying what to run
- **WHEN** a lockstep refusal names what is wrong and does not name the command that repairs it
- **THEN** the refusal is itself a defect, the exit belonging in the message rather than in tribal memory

### Requirement: The assembly root's manifest is the source, and a register row is derived from it
An electing project SHALL carry a self-describing manifest in its assembly root
recording at least the project id, the elected schema, the reference the election
followed, who elected it and when, the project topic, each leg with its role and
path, and the standard revision the project was scaffolded from; and where an
aggregation register exists, that register's row for the project SHALL be
DERIVABLE FROM the manifest, the manifest being the SOURCE and the register
remaining descriptive. The manifest SHALL NOT be derived from the register.

The direction is what makes an organisation with no aggregation, no register and
no openxFactory conformant: a file inside the project is readable by anyone who
cloned it, which is exactly the population that needs it, whereas a register is
readable only by somebody who already has the aggregation. Where the two
disagree, the register is the one that is REVIEWED and therefore the one that
wins for navigation, and the disagreement SHALL be reported as drift rather than
silently reconciled.

#### Scenario: An organisation has no aggregation register
- **WHEN** a project is scaffolded in an organisation that holds no `project-register.yaml`
- **THEN** the project is fully conformant on the strength of its own manifest
- **AND** nothing is owed to a register that does not exist

#### Scenario: A register row and a manifest disagree
- **WHEN** an aggregation's register row for a project disagrees with that project's manifest
- **THEN** the disagreement is reported as drift
- **AND** the register wins for navigation, being the only one of the grouping layers that is reviewed

### Requirement: One bootstrap command follows a recursive clone, and it degrades rather than fails
An electing project SHALL be startable with `git clone --recurse-submodules`
followed by exactly ONE bootstrap command, and that command SHALL (a) place each
submodule on a tracking branch AT its pinned commit without moving or weakening
the pin, (b) install the project's neutral validators and hooks, and (c) read any
wallet review-authority register it can find and print which objects the running
engineer's grant lets them act on. The bootstrap contract SHALL be
SCHEMA-NEUTRAL: the same command runs in a one-repository project, where the
submodule step is a no-op. Where no register is found, step (c) SHALL print
exactly `authority is not wallet-carried in this org` and CONTINUE; it SHALL NOT
fail.

The pin stays exact and `.gitmodules` carries no `branch=`: the convenience lives
in a COMMAND rather than in checked-in configuration, so there is exactly one
authoritative answer to "what commit is this project". `branch=`/`update=merge`
would buy the same ergonomics by making the declared pin advisory for anyone
running the remote form, which is the moving reference `neutral-product-pin`
already refuses in its own words. A bootstrap that existed only for electing
projects would make election worth something operationally, which is exactly what
the ratified doctrine forbids; and a bootstrap that FAILED where no wallet
register exists would have made the layout load-bearing again, which is the
property this whole line of work exists to prevent. The readout is REPORTING
only: a required check in the repository that owns the object is what confers.

#### Scenario: A fresh recursive clone is bootstrapped
- **WHEN** an engineer clones an electing project with `--recurse-submodules` and runs the bootstrap command
- **THEN** each leg is left on its tracking branch AT its pinned commit, and the recorded pin is unchanged

#### Scenario: The organisation has no wallet register
- **WHEN** bootstrap finds no wallet review-authority register
- **THEN** it prints exactly `authority is not wallet-carried in this org` and continues
- **AND** the absence is a report and not a fault, an organisation that has not adopted wallet-carried authority not being misconfigured

#### Scenario: A one-repository project is bootstrapped
- **WHEN** a project that declined the schema runs the same bootstrap command
- **THEN** it gets the validator and authority steps and the submodule step is a no-op
- **AND** it is not second-class for having declined

### Requirement: Review lanes and wallet-carried authority are overlays that attach to an existing shape
A scaffolded project's own gate SHALL run the NEUTRAL validators only — naming,
lockstep pin and manifest conformance — and an engineering review lane,
wallet-carried authority, and any domain CI SHALL be OPT-IN OVERLAYS an
organisation adds to an existing shape. A project holding none of them SHALL be
FULLY CONFORMANT. An overlay SHALL NOT be a precondition of the shape, and the
shape SHALL NOT be a precondition of an overlay.

Overlays attach to a shape and never the reverse. A shape that required its
overlays would have made layout load-bearing, and the ratified doctrine says
election confers nothing — which is only true if a project with no overlays is
conformant.

#### Scenario: An organisation holds no engineering overlay
- **WHEN** a project is scaffolded in an organisation with no codexFactory and no wallet register
- **THEN** its gate runs the neutral validators and the project is fully conformant

#### Scenario: An overlay is added later
- **WHEN** an organisation later adds a review lane or wallet-carried authority to an existing project
- **THEN** the overlay attaches to the shape already present
- **AND** the shape is not re-scaffolded and nothing about its conformance changes

### Requirement: The standard lives in `opensoft/openRepoShape`, is consumed by fork, and openxFactory pins it by commit and digest
The mechanics of this schema SHALL live in the standalone neutral product
`opensoft/openRepoShape` — the naming policy as data, the assembly-root
templates, the scaffold, the bootstrap, the validators and the agent-facing
instruction file — that product being PUBLIC and Apache-2.0, both ruled by Brett Heap on
2026-09-02 (*"name it openRepoShape and make it public"*, then *"apache 2.0,
create it"*). An organisation outside this family SHALL consume it by FORK rather
than by template copy, so the upstream link survives and shape drift stays
comparable, and the fork SHALL carry agent-readable scaffold instructions so that
"tell my AI to scaffold a new project based on that" works from a bare fork.
`openxFactory` SHALL consume it under `neutral-product-pin` — declaring
`contracts/openreposhape-pin.yaml` in the ratified `kind: pinned_contract_manifest`
grammar with `revision_kind: commit`, the exact commit, a per-file `sha256` for
every artifact it digests per file and `pinned_by_commit_only:` for the rest —
and SHALL verify that pin with running code that fails closed and names its
remedy. The standard SHALL be standard-library-only, so it runs where nothing can
be installed.

openxFactory ratifies the DOCTRINE and pins the MECHANICS; it does not author
them. A directory inside openxFactory cannot be forked into an organisation that
has no openxFactory, which is the convener's own operating constraint and the
whole reason the standard is a separate product. The
product-owns-standard / openxFactory-pins-and-validates relationship is the one
`openXwallet` already has, so this invents no boundary.

#### Scenario: An organisation outside the family starts a project
- **WHEN** an organisation with no openxFactory, no codexFactory and no wallet register forks the standard and scaffolds a project
- **THEN** the project is conformant on the strength of the fork alone
- **AND** it depends on no artifact of this family at run time

#### Scenario: openxFactory's pin is checked
- **WHEN** openxFactory's gate verifies its openRepoShape pin
- **THEN** a tag-only pin, an absent digested member, or a digest that disagrees with the recorded bytes each produces a named refusal carrying its remediation
- **AND** the refusal MUST NOT resolve to an implicit pass, to "empty" or to a skip

#### Scenario: The standard grows a dependency
- **WHEN** the standard would require a package install to run its scaffold, bootstrap or validators
- **THEN** that dependency is refused, the standard having to run in an organisation where nothing can be installed

### Requirement: codexFactory carries the engineering overlay and OpsxFactory carries organisation naming and topic administration
Ownership of this schema SHALL be split four ways and SHALL NOT be
re-concentrated: `opensoft/openRepoShape` owns the MECHANICS; `openxFactory`
ratifies the DOCTRINE, pins the standard and carries the register-election delta;
`codexFactory` owns the ENGINEERING OVERLAY on the neutral scaffold and the act
of RECOMMENDING the shape; and `OpsxFactory` owns organisation-level naming
enforcement, repository-topic administration and any GitHub template repository,
GitHub administration having been located there by the two exit changes of the
`github-administration-plane` topic.

**THIS NARROWS THE RATIFIED PROSE, and the narrowing is stated rather than
assumed.** `add-wallet-carried-review-authority` (`proposal.md:606-608`) says
*"codexFactory may recommend — and scaffold — a three-repository shape."* Read
straight, that gives codexFactory the scaffold. It is narrowed HERE in exactly
one respect — where the mechanics LIVE — because the convener's own case, a new
organisation with no codexFactory, cannot be served by a scaffold that is a
directory of an engineering-domain repository. codexFactory KEEPS the
recommending role in full, keeps its engineering overlay, and that change's
`tasks.md:811-814` (task 8.4) is satisfied by overlay-plus-offer rather than by
codexFactory hosting the neutral shape. Nothing else in that ratified change is
narrowed by this requirement.

#### Scenario: codexFactory offers the shape to a project
- **WHEN** codexFactory recommends the three-repository shape to a project
- **THEN** the recommendation is unchanged from the ratified prose, and the scaffold it points at is the neutral one
- **AND** the human project manager still decides, the election being theirs

#### Scenario: An organisation enforces the naming families
- **WHEN** organisation-level naming enforcement or repository-topic administration is realized
- **THEN** it is realized in OpsxFactory's GitHub administration plane
- **AND** neither openxFactory nor the neutral standard acquires an administration surface

### Requirement: A project may elect the schema against a staged or a ratified reference, and a pilot is recorded as such
A project electing this schema BEFORE the doctrine is ratified SHALL record both
the election and the REFERENCE it followed — the staged fragment's path before
ratification, the ratified document after — in its assembly-root manifest and in
its register row where one exists; such an election is otherwise permitted and
MUST NOT be treated as premature. A project electing against a
pre-ratification reference SHALL be recorded as a PILOT, and where a pilot exists
only to exercise the standard it SHALL be declared TEMPORARY and MUST NOT be
represented as a product of the organisation that holds it. The realization
evidence a change cites SHALL be the RECORDED RUN, and SHALL NOT depend on a
temporary pilot's repositories continuing to exist.

The house already works this way: the staging index's own draft-proposal
workspace convention was *"Adopted 2026-07-13 (Brett), first used by
ideation-dashboard"* before any spec carried it. Recording the reference is what
makes a project started ahead of ratification LEGIBLE rather than undeclared, and
what lets a later ratification reconcile drift instead of discovering it.

#### Scenario: A project elects before ratification
- **WHEN** a project elects the schema while the doctrine is still staged
- **THEN** its manifest records the staged fragment's path as the reference the election followed
- **AND** the election is legible rather than undeclared, and is reconciled at ratification

#### Scenario: A pilot exercises the standard
- **WHEN** a project is scaffolded solely to test the standard end to end
- **THEN** it is declared a TEMPORARY PILOT, is not represented as a product, and may be deleted once the standard is ratified
- **AND** the evidence it produced is the recorded run, which survives the pilot's deletion

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
