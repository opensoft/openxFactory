# Staged: a project's repositories are named, pinned and cloned as one — and the layout still confers nothing

Status: staged
Kind: capability-proposal
Summary: GitHub has no folder that groups repositories, so a project spanning
several of them is held together by convention or by nothing. The ratified change
`add-wallet-carried-review-authority` already RECOMMENDS a three-repository shape
— SPEC, CODE, ASSEMBLY — as a human election that "changes no gate, no floor, no
grant, and no clearance eligibility", but it exists ONLY as proposal prose: no
spec text, no schema field, no validator, no scaffold, so a project manager who
elects it has nothing to elect against. This topic proposes the ERGONOMICS half
and nothing else: three agreeing layers of grouping with the project register
authoritative, a naming convention (`<Project>` for the assembly root you clone,
`<Project>-spec` / `<Project>-code` for the legs) that stays distinguishable from
the `open<Product>` and `<Domainx><Product>` families already owning the org,
spec and code as SUBMODULES under the double pin `neutral-product-pin` and
`domain-descendant-boundary` already ratify, and a one-command bootstrap after
`git clone --recurse-submodules`. The mechanics live in a standalone neutral
product, `opensoft/openRepoShape` — name, PUBLIC visibility and Apache-2.0
licence all ruled by Brett Heap 2026-09-02 and the repository CREATED the same
day, seeded at `65880cb` and still empty of the standard's content — so the shape
survives being forked into an org with no openxFactory, no codexFactory and no
wallet register. Every authority question is DEFERRED to the sibling topic
`wallet-carried-work-authority`, staged the same day and landed on `main` first; a
project that declines this schema is reviewed identically to one that elects it.
Topics: project-schema, repository-naming, submodules, bootstrap, onboarding,
project-register, assembly-root, lockstep-pin, github-topics, openreposhape,
scaffold, neutral-product-pin
Repository context: FOUR homes. `opensoft/openRepoShape`
(https://github.com/opensoft/openRepoShape — public, Apache-2.0, created
2026-09-02) owns the MECHANICS: naming policy data, assembly-root templates,
scaffold script, bootstrap, lockstep validator, agent instruction file.
openxFactory ratifies the DOCTRINE (`docs/project-repo-schema.md`), pins
openRepoShape under `neutral-product-pin`, and carries the register-election
delta. codexFactory realizes an ENGINEERING OVERLAY — review-lane caller,
engineering CI — which is the recommend-and-scaffold role the ratified prose
gives it, narrowed to the overlay. OpsxFactory realizes org-level naming
enforcement and repository topics, where GitHub administration was located by the
two exit changes of the superseded `github-administration-plane` topic
(openxFactory `archive/2026-07-14-add-github-app-identity-tiers`; OpsxFactory
`2026-07-15-add-github-administration-workflow`). The aggregation layer keeps the
`project-register.yaml` instance it already owns.
Staging ID: openxFactory:staging:project-repo-schema
Captured: 2026-09-02
Source: Brett Heap in session 2026-09-02, in four parts, quoted verbatim.
(1) "github does not have a folder setup to group repos. i think the best
practice would be a naming convention for this. would the spec and code repos be
submodules of the assembly? how can we make easy for engineer to clone it all
down and get started?" — then the ruling "stage the project-schema topic too."
(2) "where should we document this naming convention and the scaffold for new
projects. we might start a new project before codex is ready to support all this
or even outside codex and want to keep the same shape". (3) "so if I have a new
org and in that new org i want to make a new project. i will want that to use
this shape. how do I do that? I think i need to fork the 'codeXfactory-repo-shape'
repo from opensoft and then tell my ai to scaffold a new project based on that.
This way I can still take advantage of this shape even if i do not have
codeXfactory on this repo." (4) Two rulings on the recommendation that followed:
"name it openRepoShape and make it public", then "apache 2.0, create it". Origin
provenance is the ratified change `add-wallet-carried-review-authority`
(`proposal.md:600-617`), carrying his 2026-08-22 ruling, verbatim: "For our own
internal projects, we can have codeXfactory recommend and run a 3 repo project
schema. But let the human project manager decide." A fifth ruling followed
separately the same day, resolving Q2, quoted verbatim: "yes, assembly is per
project." A sixth ruling followed the first pilot run the same day, resolving
Q1, chosen from three options presented: "Descendant only if it pins
open<Product>."
Target capabilities: ADDED `project-repo-schema` (doctrine, naming convention,
assembly-root pin shape, bootstrap contract, lockstep obligation) and MODIFIED
`ideation-dashboard` (the register gains a per-project `schema` election and a
per-repository `role`, both still conferring nothing). The ADDED capability is
deliberately NOT fenced as an `xspec:candidate` target: it exists in neither
`openspec/specs/` nor an active change's `specs/`, so fencing it would emit
tag-hygiene unresolved-target findings — the convention `openxwallet-neutral-home`
and `treatment-options-engine` already follow. The one fenced block targets
`ideation-dashboard`, which owns the register requirement today.

## Last proposal attempt (round-trip provenance)

Change ID: none yet
Raised: n/a
Status at demote: n/a
Demoted: n/a
Demote reason: n/a

## Claims

Settled context the open questions below do NOT reopen.

- **The schema is elective and confers nothing.** `add-wallet-carried-review-authority`
  (ratified 2026-08-23): "Electing the schema changes no gate, no floor, no
  grant, and no clearance eligibility" (`proposal.md:617`); a one-repository and
  a three-repository project "are reviewed IDENTICALLY, because the authority
  travels in the grants rather than in the layout" (`:614-616`).
- **The election is a `PA` decision, `CA`-constrained and `PM`-sequenced**
  (`proposal.md:625-634`, against `docs/roles-and-authority.md:67-74`). This
  topic elects nothing for anyone.
- **The recommendation has NO spec text**, verified 2026-09-02: `openspec/specs/`
  carries no such capability; the ratified change's `specs/` deltas are exactly
  two (`review-authority-intake`, `roles-authority-model`); and greps for
  "recommended project schema", "three-repositor" and the governance sense of
  "ASSEMBLY" resolve only to that one proposal (`:81`, `:191`, `:193`, `:600`,
  `:606-608`, `:666`, `:1233`, `:1236`, `:1333`) plus `tasks.md:811-814`. The
  delta is ADDED — there is nothing yet to modify.
- **The register is the grouping instrument and it confers nothing.** The
  aggregation-root `project-register.yaml` (schema
  `contracts/schemas/project-register.schema.yaml`; requirement owned by
  `ideation-dashboard`, `spec.md:50`): "Grouping is descriptive navigation only:
  it confers no lifecycle state and no authority over the repositories it
  names." Split BY ROLE per Brett's 2026-08-06 D7 ruling on
  `dashboard-project-scoping`, multi-parent per D8, aggregation-owned, written
  only through a recorded `project-register-edit` commission (D2; `spec.md:1380`,
  `:1400`, `:1469`).
- **The double pin is ratified house form.** `domain-descendant-boundary` requires
  a gitlink AND `contracts/<product>-pin.yaml` moved in the SAME commit — "the
  same-commit rule is what makes the two pins one act" — and
  `neutral-product-pin` requires commit-and-digest, refusing a tag ("a tag can be
  moved") and a range, failing closed with a remediation string. Reused
  unchanged; no pin grammar is invented here.
- **Lockstep is a measured cost, not a hypothesis.** The aggregation's
  `.github/workflows/review-lane.yml:65` dispatches
  `review-lane-reusable.yml@dc21767…` and `tests/test_review_lane_workflow.py:13`
  pins the same string, so a pin-sync moves gitlink + caller ref + test PIN in
  ONE commit. Seven consecutive pin-syncs from 2026-08-25 moved the gitlink alone
  and left `validate` red on every aggregation PR until 2026-08-26 (xFactory
  #146), unnoticed because `validate` runs on pull requests only.
- **The shape repo is named, public, licensed and CREATED.** Brett Heap ruled
  2026-09-02: "name it openRepoShape and make it public", then "apache 2.0,
  create it". `opensoft/openRepoShape` exists — PUBLIC, Apache-2.0, default
  branch `main`, initial commit `228dd9f`, README seeded at `65880cb` carrying
  `Status: staged` and pointing back at this fragment. `65880cb` is the earliest
  pinnable ref; the standard's CONTENT is not in it yet.

## Why

The convener's questions are ergonomics questions with no answer in the corpus.
The family recommends a three-repository shape and has ruled who elects it, then
stops: no name form, no place to record the election, no way for one clone to
bring a project down, no scaffold for a project starting today — least of all in
a different org holding none of this machinery. The recommendation is
unactionable in the precise sense that a PA who says "yes" has nothing to say yes
to.

Layout is also now FREE to be optimized for humans.
`add-wallet-carried-review-authority` demoted repository topology from the spine
of authority to an elective layout so layout would carry no governance weight,
and the sibling topic
[wallet-carried-work-authority](../wallet-carried-work-authority/wallet-carried-work-authority.md),
staged the same day and landed on `main` first, removes the last hidden coupling
by making grants path-scoped rather than repository-granular. This topic takes that freedom and does the ergonomics, only.

## What changes

**Three layers of grouping that must agree, register authoritative.** A
`project-register.yaml` row lists the legs; each repository carries a GitHub
topic mirroring the project id, proposed form `xf-project-<id>`, so the org's own
search surfaces the group without a checkout; a naming convention carries the
human eye. Where they disagree the register wins and the others are reported as
drift — the register is the only one of the three that is reviewed.

**Naming.** `<Project>` for the assembly root and `<Project>-spec` /
`<Project>-code` for the legs. A reader disambiguates the four live families by
SHAPE: leading lowercase `open` means neutral product; trailing `-Install` means
install; an `x`-terminated domain stem in front of a live product name means
descendant (MedxChart pins openChart, MedxPractice pins openPractice); trailing
lowercase `-spec`/`-code` means project leg. The leg suffixes are lowercase and
hyphenated precisely so they sit in a different visual class from every existing
family, all of which are CamelCase words.

**Submodules, not a manifest.** The assembly root pins spec and code as
submodules — gitlink plus `contracts/<leg>-pin.yaml`, same commit — under the
ratified double pin. The consequence is the point: the assembly PR becomes the
SINGLE place where the staged `signed-execution-chain` merge gate can validate a
chain over the whole project, and the single place a wallet `merge` act (sibling
topic) would be exercised. Manifest-driven side-by-side clones are the rejected
alternative — same directories, no atomic pin, nothing for a gate to check.

**Onboarding.** `git clone --recurse-submodules <Project>`, then ONE bootstrap
command that (a) moves each submodule off its pinned detached HEAD onto a
tracking branch, (b) installs validators and hooks, and (c) reads the wallet
review-authority register and prints which objects this engineer's grant lets
them author or review. Step (c) depends on the sibling topic for `author` and
degrades to a stated line rather than failing. The contract is SCHEMA-NEUTRAL: a
one-repository project runs the same command and gets (b) and (c).

**The mechanics live in a forkable product.** `opensoft/openRepoShape` owns the
policy data, templates, `scaffold-project.py`, `bootstrap`, the lockstep
validator, and an `AGENTS.md`/`CLAUDE.md` describing the scaffold procedure so
"tell my AI to scaffold" works verbatim from a bare fork. openxFactory pins it by
commit and digest; its own validators consume the pinned copy. The doctrine —
elective, confers nothing, what ASSEMBLY means — stays ratified in openxFactory.

**The lockstep validator.** The assembly template ships a validator asserting
gitlink == pin-file commit == every workflow ref naming that leg, run in the
assembly's own PR gate: the aggregation's August defect written down as machinery
instead of as a working rule in a `CLAUDE.md`.

## The register election

<!-- xspec:candidate target=ideation-dashboard -->
The project register SHALL carry an optional per-project `schema` election and
an optional per-repository `role` of `spec`, `code` or `assembly`, so a human's
election is machine-readable by the instrument that already names the group.
Both fields SHALL be additive and optional: a project declaring neither is
legal, renders identically and is reviewed identically. Neither field SHALL
confer lifecycle state, authority, gate standing or clearance eligibility over
any repository, project or group it names — the register's existing posture
governs the new fields unchanged, and a consumer deriving any permission from
`schema` or `role` is defective. A project MAY additionally record the
`reference` its election followed — a staged fragment path before ratification,
the ratified document after — so a project started ahead of ratification is
legible rather than undeclared. Where an assembly root carries its own
`project.yaml` manifest, the register row SHALL be DERIVABLE from it and the
manifest is the source; the register stays descriptive. Register writes continue
to reach the file only through the recorded `project-register-edit` commission.
<!-- /xspec:candidate -->

## Impact

- Affected specs: ADDED `project-repo-schema`; MODIFIED `ideation-dashboard` (the
  additive register fields and the derivation rule above). No delta on
  `repo-boundary-governance` or `shared-contract-ownership` is declared —
  openRepoShape's CREATION is a separate act (Exit), and this topic moves no
  runtime code and advances no existing pin.
- Affected code: openRepoShape (new) — `contracts/repository-naming.yaml`,
  `templates/`, `scaffold-project.py`, `bootstrap`, the lockstep validator,
  `AGENTS.md`. openxFactory — `docs/project-repo-schema.md`,
  `contracts/openrepshape-pin.yaml`, the register schema's additive fields.
  codexFactory — the engineering overlay. OpsxFactory — org naming and topics.
  The xFactory aggregation — the register instance, when a project elects.
- Blast radius on adoption is zero by construction: every artifact is new, every
  field optional, no existing repository renamed.

## Idea notes (pre-document, non-documented)

- GitHub's missing folder is the whole problem, and every answer is a convention
  something must check. Three agreeing layers is not elegance, it is the minimum:
  humans read names, tools read topics, only the register is reviewed. —
  Added-by: Claude Fable 5.1 · 2026-09-02
- Naming the submodule tax beats selling the shape. Detached HEAD is what an
  engineer meets on day one and why people hate submodules; bootstrap exists
  mostly to pay it. — Added-by: Claude Fable 5.1 · 2026-09-02
- ASSEMBLY reads two ways in the ratified sentence and the topic cannot pick one
  without a ruling. Under the shared-repo reading a project has no root to clone,
  which defeats the question actually asked. — Added-by: Claude Fable 5.1 ·
  2026-09-02
- The register beats a file inside the project, because a file inside the project
  is only readable by someone who already cloned it — but a new org has no
  register at all, which is what forces the assembly-root `project.yaml` and makes
  the register a DERIVED view rather than the origin. — Added-by: Claude Fable
  5.1 · 2026-09-02
- Worth resisting: letting `role: spec` mean anything. The moment a tool reads it
  as "spec authority lives here" the register has quietly become a governance
  boundary, which the ratified prose forbids. — Added-by: Claude Fable 5.1 ·
  2026-09-02
- A project may need to start before ratification, and the corpus has a
  precedent: INDEX.md's own draft-proposal workspace convention was "Adopted
  2026-07-13 (Brett), first used by ideation-dashboard" before any spec carried
  it. — Added-by: Claude Fable 5.1 · 2026-09-02
- Brett's phrasing "tell my ai to scaffold a new project based on that" is a
  requirement, not a figure of speech: the fork must carry agent-readable
  instructions, or the flow depends on a prompt somebody remembers. — Added-by:
  Claude Fable 5.1 · 2026-09-02

## Conflicts

- **The ASSEMBLY wording is ambiguous and nothing resolves it.** The ratified
  prose defines ASSEMBLY as "the code that assembles a review team, shared across
  the family" (`proposal.md:608`) — one shared repository; this topic needs a
  PER-PROJECT root to clone. Both readings fit the rest of the document and the
  corpus has no third mention. Q2 is the ruling. — Added-by: Claude Fable 5.1 ·
  2026-09-02
- **The corpus PREFERS co-residence and this topic does not change that.** D1 of
  `add-wallet-carried-review-authority` rejected the three-repository topology as
  the spine partly because it would have had to overturn
  `shared-contract-ownership:113-137` and `adopt-neutral-tooling-home`, which
  moved tooling TOWARD the repository whose artifacts it reads; openxFactory is
  itself SPEC and CODE in one repository. Reconciliation: the schema stays
  ELECTIVE and the neutral layer keeps declining it. — Added-by: Claude Fable 5.1
  · 2026-09-02
- **Two naming families now end in a suffix and the corpus has no arbiter.**
  `<Domainx><Product>` is ratified with the explicit goal that "one casing scheme
  covers the org rather than two"; `-spec`/`-code` adds a second scheme. They do
  not collide today, but nothing prevents a future product named `Spec`. Q1
  proposes a disambiguation rule, which is a convention and not a proof. —
  Added-by: Claude Fable 5.1 · 2026-09-02
- **RESOLVED by Q1's ruling.** Brett Heap ruled 2026-09-02 that a
  `<Domainx><Product>`-shaped name is a domain descendant only when it pins the
  matching `open<Product>`, so a bare assembly-root name sharing that shape (the
  `MedxScribe` pilot, refused under the old precedence although no `openScribe`
  exists) is disambiguated from the descendant family without a second casing
  scheme. — Added-by: Claude Fable 5.1 · 2026-09-02
- **The register's "confers no authority" posture must survive two new fields.**
  `schema` and `role` are exactly the fields a later consumer reads as
  permission. The posture is stated in the schema description, the requirement
  text and the instance header, and all three must restate it for the new fields
  — an obligation this topic can name but not discharge. — Added-by: Claude Fable
  5.1 · 2026-09-02
- **The bootstrap's grant readout depends on an unratified sibling.** Step (c)
  reads what the engineer may AUTHOR, and `author` is proposed by
  `wallet-carried-work-authority`. Until that lands the readout reports review
  authority only, and must degrade rather than fail. — Added-by: Claude Fable 5.1
  · 2026-09-02
- **"codexFactory may recommend — and scaffold" reads as codexFactory owning the
  scaffold; Q9 puts the mechanics in a standalone neutral product.** The exit
  change must reconcile the wording explicitly. It is a NARROWING of where the
  scaffold LIVES, not of what codexFactory may recommend: codexFactory keeps the
  recommending role and its engineering overlay, and `tasks.md:811-814` (task
  8.4) is satisfied by overlay-plus-offer, not by codexFactory hosting the
  neutral shape. — Added-by: Claude Fable 5.1 · 2026-09-02
- **Visibility and licence were a live tension, are now RULED, and leave a
  ruleset residue.** The two private `open*` repos, openAvatar and openXwallet,
  carry NO licence and are pin-consumed inside the family; a repo meant to be
  FORKED into other orgs must be secret-free and licence-clear. Verified
  2026-09-02 via `gh repo view`: `openChart` and `openPractice` are PUBLIC under
  Apache-2.0 while `openAvatar` and `openXwallet` are PRIVATE with
  `licenseInfo: null`. Brett ruled both halves the same day — public, Apache-2.0
  — so the family now carries two deliberate postures for `open*` rather than a
  drift. BOOKKEEPING for the exit change: the seed push to `openRepoShape`'s
  `main` bypassed the org ruleset "Changes must be made through a pull request"
  under the operator's bypass right; the repo inherits that ruleset, so every
  later content commit lands by PR. — Added-by: Claude Fable 5.1 · 2026-09-02

## Open questions

### Q1. What is the name form for a project's repositories, and how does a reader tell it from the families that already own the org?

Context: the org carries `open<Product>` neutral products, `<Domainx><Product>`
descendants (ratified with the explicit goal of one casing scheme),
`<X>-Install` installs, and the bare aggregation root `xFactory`. Two live
repositories fit no suffix rule at all (`xFactory-Installer`, `AgentTower`), so
any convention is a forward rule, not a description.
Recommended answer: bare `<Project>` for the assembly root, `<Project>-spec` and
`<Project>-code` for the legs, suffixes fixed lowercase and hyphenated; a reader
disambiguates by shape (leading `open`, trailing `-Install`, embedded
`x`-terminated domain stem, trailing `-spec`/`-code`), and anything else is a
project root the register must name.
Explanation: the leg suffixes are the only part a human must learn, and
lowercase-hyphenated puts them in a different visual class from every existing
CamelCase family. Bare `<Project>` follows the precedent the aggregation itself
sets — the thing you clone has no suffix.
Disposition status: RULED — Brett Heap, 2026-09-02, choosing "Descendant only
if it pins open<Product>" from three options presented: a `<Domainx><Product>`
name is a domain descendant ONLY when the project declares a pin on the
matching `open<Product>`; otherwise the scaffold's declared role wins, the name
is a valid assembly root, and the manifest records that it also matches the
descendant form, keeping the policy checkable offline (the rejected
alternatives were renaming the pilot to keep the old rule, or a live GitHub
lookup). Evidence: the first pilot run, 2026-09-02, `MedxSoft/MedxScribe`
(private, forked from `opensoft/openRepoShape` at `0b1660a`), refused
`MedxScribe` as an assembly root under the old precedence although no
`openScribe` exists, and separately hit a `setup.sh` org-detection defect that
wrongly preferred the `upstream` remote over `origin` and refused a correct
fork (worked around with `--org MedxSoft`) — both fixes are an openRepoShape PR
in flight.
Added-by: Claude Fable 5.1 · 2026-09-02

### Q2. Does ASSEMBLY mean a per-project root repository, or the one shared review-team assembly repository the ratified prose describes?

Context: `proposal.md:608` defines ASSEMBLY as "the code that assembles a review
team, shared across the family". Read as one shared repository, an electing
project has SPEC and CODE and no root — and no answer to "how can we make easy
for engineer to clone it all down". Read as a per-project root, the sentence
describes the CONTENT such a root pins.
Recommended answer: the per-project root repository IS the assembly leg, and it
PINS the shared review-team assembly code from codexFactory at a sha — exactly
how the aggregation already consumes the review lane at
`review-lane-reusable.yml@dc21767…`. Both readings then hold.
Explanation: this is the only reading under which the convener's question has an
answer, and it costs nothing, because the shared-code half is already how the
family consumes review machinery. The alternative leaves a project with no front
door.
Disposition status: RULED — Brett Heap, 2026-09-02: "yes, assembly is per
project." Resolved: the ASSEMBLY leg is the per-project root repository the
engineer clones, not the shared family repository, and it may later pin the
shared review-team assembly code from codexFactory as an overlay. The exit
change's Q2 gate is satisfied.
Added-by: Claude Fable 5.1 · 2026-09-02

### Q3. Are the spec and code legs submodules of the assembly root, or side-by-side clones driven by a manifest?

Context: Brett asked directly. Submodules give one commit naming the whole
project; a manifest gives the same layout with independent clones and no shared
commit. The family's gates increasingly key on an atomic pin —
`signed-execution-chain`'s merge gate validates a chain at a PR, and the sibling
topic's `merge` act would be exercised at one.
Recommended answer: submodules, pinned by gitlink AND `contracts/<leg>-pin.yaml`
in the same commit, reusing the ratified double pin unchanged; the manifest is
the named rejected alternative.
Explanation: the pin is the product. Without one commit naming both legs there is
no object for a gate to validate and no way to say what "the project" was at a
point in time. The manifest's ergonomic advantage is recovered by bootstrap (Q4).
Disposition status: open
Added-by: Claude Fable 5.1 · 2026-09-02

### Q4. How is detached HEAD handled — bootstrap-driven tracking branches, or `.gitmodules` `branch=` with `update=merge`?

Context: a fresh `--recurse-submodules` clone leaves every submodule detached at
the pinned commit. `.gitmodules` can declare `branch=`/`update=merge` so
`git submodule update --remote` follows a branch, which makes the declared pin
advisory for anyone running the remote form.
Recommended answer: bootstrap-driven. The pin stays exact in `.gitmodules` with
no `branch=`; bootstrap checks each submodule out onto a tracking branch AT the
pinned commit, so the working state is branch-shaped while the recorded state
stays a pin. Advancing the pin remains an explicit assembly-root commit.
Explanation: `branch=`/`update=merge` buys the same ergonomics by weakening the
pin, and `neutral-product-pin` already refuses a moving reference in its own
words. Putting the convenience in a command rather than in checked-in
configuration keeps exactly one authoritative answer to "what commit is this
project".
Disposition status: open
Added-by: Claude Fable 5.1 · 2026-09-02

### Q5. Where is the election recorded, and which capability owns that field?

Context: the ratified prose says the register is "where it is recorded" and
leaves the field undesigned. The register SCHEMA is neutral openxFactory; the
INSTANCE is aggregation-owned; the REQUIREMENT lives in `ideation-dashboard`
(`spec.md:50`), an odd home for a project-layout election. A new org has neither
aggregation nor register (Q11).
Recommended answer: the assembly root's own `project.yaml` is the SOURCE; the
register row is DERIVED from it where an aggregation exists. Declare the register
delta as MODIFIED `ideation-dashboard`, because that capability owns the
requirement today; the new `project-repo-schema` capability defines the
VOCABULARY both carriers use and takes no ownership of the register.
Explanation: splitting vocabulary from carrier keeps one authoritative register
requirement instead of two capabilities claiming the same schema, and making the
manifest the source is what lets an org with no register still be conformant.
Moving the register requirement out of `ideation-dashboard` is a larger unrelated
change this topic should not pay for.
Disposition status: open
Added-by: Claude Fable 5.1 · 2026-09-02

### Q6. How is ownership split across openRepoShape, openxFactory, codexFactory and OpsxFactory?

Context: working rule 1 puts domain-neutral contracts in openxFactory; the
ratified prose gives codexFactory the recommend-and-scaffold role; GitHub
administration was located in OpsxFactory by two archived exit changes.
Recommended answer: openRepoShape owns the MECHANICS (policy data, templates,
scaffold, bootstrap, lockstep validator, agent instructions). openxFactory
ratifies the DOCTRINE, pins openRepoShape, and carries the register delta.
codexFactory owns the ENGINEERING OVERLAY and the act of recommending.
OpsxFactory owns org-level naming enforcement, repository topics, and any GitHub
template repository.
Explanation: four planes, three of them already established; the fourth exists
because the shape must survive being forked out of the family entirely (Q9,
Q11). The only genuine narrowing is codexFactory's, recorded as a conflict above
rather than assumed.
Disposition status: open
Added-by: Claude Fable 5.1 · 2026-09-02

### Q7. Does the assembly template ship a lockstep validator, and what must it assert?

Context: the aggregation's lockstep invariant — gitlink, the
`review-lane-reusable.yml@<sha>` caller ref, and `PIN` in
`tests/test_review_lane_workflow.py` move together or `validate` goes red — was
practice for months and written down nowhere. Seven pin-syncs from 2026-08-25
broke it, unnoticed for a day because `validate` runs on pull requests only.
Recommended answer: yes. The template ships a validator asserting gitlink ==
`contracts/<leg>-pin.yaml` commit == every workflow ref naming that leg, run in
the assembly's PR gate, refusing with a remediation string in the fail-closed
form `neutral-product-pin` already requires.
Explanation: the invariant is not specific to the aggregation — any assembly root
that both pins a leg and dispatches a workflow at that leg's sha has it. Shipping
it in the template makes the cost of the submodule answer a one-time scaffold
cost instead of a per-project tribal rule.
Disposition status: open
Added-by: Claude Fable 5.1 · 2026-09-02

### Q8. Does a one-repository project get the same bootstrap command?

Context: the schema is elective and a declining project must not be second-class.
Two of the three bootstrap steps have nothing to do with layout.
Recommended answer: yes. The bootstrap contract is schema-neutral — the same
command in any project root, with the submodule step a no-op where there are no
submodules.
Explanation: a bootstrap that existed only for electing projects would make
election worth something operationally, which is exactly what the ratified prose
forbids. Schema-neutrality is how "confers nothing" survives contact with
tooling.
Disposition status: open
Added-by: Claude Fable 5.1 · 2026-09-02

### Q9. Where do the naming convention and the scaffold live, and under what licence?

Context: Brett asked where to document this, then supplied the operating
constraint — a new org, no codexFactory — and then ruled the answer's name and
visibility: "name it openRepoShape and make it public". A directory inside
openxFactory cannot be forked into an org that has no openxFactory.
Recommended answer: a STANDALONE neutral product repository,
`opensoft/openRepoShape` (https://github.com/opensoft/openRepoShape — name,
PUBLIC visibility and Apache-2.0 licence all RULED 2026-09-02, repository created
the same day, seeded at `65880cb`), under the `open<Product>` convention. It owns `contracts/repository-naming.yaml` covering
all four naming families so one validator checks them, the assembly-root
templates, `scaffold-project.py`, `bootstrap`, the lockstep pin validator, and an
agent-facing `AGENTS.md`/`CLAUDE.md` describing the scaffold procedure so "tell
my AI to scaffold" works verbatim. openxFactory PINS it by commit and digest per
`neutral-product-pin`, exactly as it pins openXwallet, and openxFactory's own
validators consume the pinned copy. openxFactory keeps
`docs/project-repo-schema.md` as the ratifying home of the DOCTRINE — elective,
confers nothing, and what ASSEMBLY means. The licence question this
answer originally carried is RULED: Apache-2.0, matching the family's only
public-`open*` precedent. What remains open is the CONTENT — file layout, what
ships in v1, and the first digested release openxFactory can pin.
Explanation: Brett's earlier proposal `codeXfactory-repo-shape` is recommended
against and was superseded by his own ruling — a codex-prefixed name signals an
engineering-domain dependency in a repository whose whole purpose is to work
WITHOUT codexFactory. The product-owns-standard, openxFactory-pins-and-validates
relationship is the one openXwallet already has, so this invents no new
boundary. On licence: verified 2026-09-02 by `gh repo view`, `openChart` and
`openPractice` are PUBLIC under Apache-2.0 while `openAvatar` and `openXwallet`
are PRIVATE with no licence at all; Brett ruled Apache-2.0, whose patent grant is
the right posture for contract text and validators other orgs will fork and run.
Disposition status: RULED on the name, the visibility and the licence (Brett
Heap, 2026-09-02 — `opensoft/openRepoShape`, public, Apache-2.0), and the
repository is CREATED; OPEN on the remaining mechanics — file layout, what ships
in v1, and the first digested release openxFactory pins
Added-by: Claude Fable 5.1 · 2026-09-02

### Q10. May a project start before this is ratified, or outside codexFactory, and still keep the shape?

Context: Brett named both cases. The openRepoShape path has no codexFactory
dependency, so the second is a question about self-sufficiency; the first is
about what a pilot may cite.
Recommended answer: yes. A project MAY start against the STAGED fragment as its
reference, using the openRepoShape path directly, PROVIDED its assembly-root
`project.yaml` — and its register row where one exists — records both the
election and the reference followed (`schema: project-repo-schema` with a
`reference:` pointing at the staged fragment path before ratification, the
ratified doc after). The first such project is the PILOT and the exit change
cites it as realization evidence.
Explanation: the house already works this way — INDEX.md's draft-proposal
workspace convention was "Adopted 2026-07-13 (Brett), first used by
ideation-dashboard" before any spec carried it. The lifecycle permits a staged
reference as long as the pilot is recorded and the ratifying change reconciles
drift. A project outside codexFactory has no overlay to wait for, which makes
self-sufficiency a hard requirement on openRepoShape: plain Python, no package
install, no engineering-domain dependency.
Disposition status: open — needs Brett's confirmation that a staged fragment may
serve as a pilot's reference. The first pilot is `MedxSoft/MedxScribe`, elected
by brettheap 2026-09-02; its first run surfaced the two openRepoShape defects
recorded under Q1 (the `upstream`-remote org misdetection and the descendant
naming refusal). Both defects were fixed upstream and merged 2026-09-02:
openRepoShape PR #3 (org detected from the fork's own `origin`, `7edd6bb`) and
PR #4 (a descendant-shaped name is a claim that needs a declared pin; the
declared role wins otherwise, `deacbdc`). A second run, 2026-09-02, from the
MedxSoft fork synced to upstream `deacbdc`, command
`./setup.sh --project MedxScribe --visibility private --yes`, SUCCEEDED end to
end: it created private `MedxSoft/MedxScribe` (assembly root, `07060d4`),
`MedxSoft/MedxScribe-spec` (`52c96cb`) and `MedxSoft/MedxScribe-code`
(`023a27f`), topic `xf-project-medxscribe` on all three, legs mounted at
`spec/` and `code/`, shape pin `opensoft/openRepoShape @ deacbdc`, elected by
brettheap 2026-09-02 with this fragment's path recorded as reference; the
manifest records that `MedxScribe` also matches the descendant form with no
referent pin declared, so it is not a descendant unless
`contracts/openscribe-pin.yaml` is added. Bootstrap after
`git clone --recurse-submodules` left both legs on `main` at their pins, the
naming/manifest/lockstep-pin validators green, the shape copy pin (9 files)
green, and printed the degrade line verbatim: "authority is not
wallet-carried in this org". This is the realization evidence the exit change
`add-project-repo-schema` cites for "the first such project is the pilot".
Added-by: Claude Fable 5.1 · 2026-09-02

### Q11. What is the exact flow for starting a project in a NEW org?

Context: Brett's third question, verbatim, describes forking a shape repo and
telling an AI to scaffold from it. A new org has no aggregation repo, no
`project-register.yaml`, no wallet register and no codexFactory.
Recommended answer: as a concrete sequence — (1) FORK `opensoft/openRepoShape`
into the new org — a fork, not a GitHub "template", so the org keeps the upstream
link and can pull shape updates. (2) In the fork run
`scaffold-project.py --org <org> --project <Project>`, which creates
`<org>/<Project>`, `<Project>-spec` and `<Project>-code` via `gh repo create`,
pushes initial trees, adds the two legs as submodules of the assembly root with
`contracts/<leg>-pin.yaml` digest pins, writes `contracts/shape-pin.yaml`
recording the openRepoShape commit and digest the project was scaffolded from,
writes a self-describing `project.yaml` in the assembly root (id, schema, legs
with `role: spec|code|assembly`, shape reference), and sets the GitHub topic on
all three. (3) `gh repo clone <org>/<Project> -- --recurse-submodules`, then
`make bootstrap`.
Explanation: the assembly-root `project.yaml` is what an aggregation's
`project-register.yaml` can later be DERIVED from, so the register stays
descriptive and the manifest is the source — which is the only construction that
works for an org with no register (Q5). The shape pin lets `bootstrap --check`
report upstream drift the way neutral-product pins already do, and a fork rather
than a template is what keeps that comparison meaningful.
Disposition status: open
Added-by: Claude Fable 5.1 · 2026-09-02

### Q12. What does a scaffolded project do without the codexFactory and wallet overlays?

Context: an org forking the shape has neither the engineering review lane nor a
wallet review-authority register, and the doctrine says the schema confers
nothing.
Recommended answer: the scaffolded repositories' CI runs only the NEUTRAL
validators — naming, lockstep pin, manifest schema. The codexFactory engineering
review lane and wallet-carried authority are opt-in OVERLAYS an org adds later,
and `bootstrap` prints "authority is not wallet-carried in this org" when no
register is found rather than failing.
Explanation: the ratified doctrine says election confers nothing, so a project
with no overlays is FULLY conformant. Overlays attach to an existing shape, never
the reverse — a shape that required its overlays would have made layout
load-bearing again, which is the property this whole line of work exists to
prevent.
Disposition status: open
Added-by: Claude Fable 5.1 · 2026-09-02

## Exit

TWO acts in order, and the first is HALF DONE. FIRST, openRepoShape is created
and cut — the public Apache-2.0 repository EXISTS as of 2026-09-02 (seeded
`65880cb`); what remains is its CONTENT and a first release with per-file
digests: the naming policy data, the templates, the scaffold, the bootstrap, the
lockstep validator and the agent instruction file, all landing by PR under the
inherited org ruleset. This mirrors how `openxwallet-neutral-home` and its change
created openXwallet. SECOND, one openxFactory change (working name
`add-project-repo-schema`) that (a) ratifies the doctrine doc and the ASSEMBLY
clarification Q2 rules, (b) adds the openRepoShape pin under
`neutral-product-pin`, and (c) adds the register election fields and the
manifest-derivation rule. Two realizations follow: codexFactory ships the
ENGINEERING OVERLAY on the neutral scaffold (review-lane caller, engineering CI,
the offer named in task 8.4), and OpsxFactory ships org naming enforcement,
repository-topic administration, and any regenerated GitHub template repository.
Q2 is RULED (Brett Heap, 2026-09-02), so that precondition on proposing the
openxFactory change is satisfied; it still cannot pin openRepoShape until that
product cuts a digested release. Nothing in the exit elects the schema for any project — that stays a `PA`
decision, per project, conferring nothing.

Realization evidence for this exit change now exists: the pilot's second run,
2026-09-02, succeeded end to end against openRepoShape `deacbdc`, creating
`MedxSoft/MedxScribe`, `MedxSoft/MedxScribe-spec` and
`MedxSoft/MedxScribe-code`.
