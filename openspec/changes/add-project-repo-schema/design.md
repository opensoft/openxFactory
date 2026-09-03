# Design: add-project-repo-schema

Status: draft

Every decision below is traceable to the staged fragment's twelve open questions
(`supporting-docs/project-repo-schema.md` § Open questions). Five of them the
convener RULED and they are recorded here as rulings with their dates, not
re-argued. The remaining seven are decided here on the fragment's recommended
answers, with the alternatives that were rejected named — a decision whose
alternative is not written down is a decision the next reader has to take again.

---

## D1 — The naming families, and what makes a descendant (Q1) — RULED

**Ruling: Brett Heap, 2026-09-02** — *"Descendant only if it pins
open&lt;Product&gt;."* Chosen from three options presented.

**Decision.** `<Project>` bare for the assembly root, `<Project>-spec` and
`<Project>-code` for the legs, suffixes fixed lowercase and hyphenated. A reader
disambiguates by SHAPE: leading `open` is a neutral product, trailing `-Install`
is an install, an `x`-terminated domain stem in front of a product name is a
descendant *only where the project declares a pin on that product*, and trailing
`-spec`/`-code` is a project leg. Where a `<Domainx><Product>`-shaped name
declares no such pin, the DECLARED ROLE wins and the manifest records
`also_matches`.

**Alternatives rejected.**

1. *Rename the pilot and keep the old precedence rule.* Rejected: it treats a
   CLAIM as a FACT. Every project in a `<Domainx>` family organisation hits the
   overlap, and `MedxSoft` holds three such names already; the rule would have
   made an ordinary project unscaffoldable in the one organisation shaped to
   have many.
2. *A live GitHub lookup to decide whether `open<Product>` exists.* Rejected:
   the check must run in an organisation that forked the standard once and may
   never speak to the upstream again. A rule needing the network is unrunnable
   exactly where this standard is meant to work.
3. *A second casing scheme to separate project legs from descendants.* Rejected:
   `<Domainx><Product>` was ratified with the explicit goal that *"one casing
   scheme covers the org rather than two"*. The pin-as-referent rule
   disambiguates without adding one.

**The residue this leaves, stated rather than hidden.** Two live repositories
fit no suffix rule at all (`xFactory-Installer`, `AgentTower`), so this is a
FORWARD rule. The spec says so: a repository predating the rule is not thereby
non-conformant.

## D2 — What ASSEMBLY means (Q2) — RULED

**Ruling: Brett Heap, 2026-09-02** — *"yes, assembly is per project."*

**Decision.** The ASSEMBLY leg IS the per-project ROOT repository the engineer
clones. It MAY pin the shared review-team assembly code as an OVERLAY, at a sha,
the way the aggregation already consumes `review-lane-reusable.yml@<sha>`.

**Alternative rejected.** *ASSEMBLY is the one shared review-team repository the
ratified prose describes* (`add-wallet-carried-review-authority`,
`proposal.md:608`). Rejected by the ruling, and it was the reading that could not
work: under it an electing project has SPEC and CODE and no root to clone, which
is precisely the question the convener asked. The chosen reading COSTS NOTHING
because the shared-code half is already how the family consumes review
machinery, so both sentences hold.

## D3 — Submodules, not a manifest of side-by-side clones (Q3)

**Decision.** The spec and code legs are SUBMODULES of the assembly root, pinned
by gitlink AND `contracts/<role>-pin.yaml` in the same commit, reusing the
ratified double pin unchanged. No pin grammar is invented.

**Alternative rejected.** *Side-by-side clones driven by a manifest.* It gives
the same directory layout with independent clones — and no shared commit. **The
pin is the product:** without one commit naming both legs there is no object for
a gate to validate and no way to say what "the project" was at a point in time.
The family's gates increasingly key on exactly that — the staged
`signed-execution-chain`'s merge gate validates a chain at a pull request, and
the sibling topic's `merge` act would be exercised at one. The manifest's real
advantage is ergonomic, and D4 recovers it.

## D4 — Detached HEAD is paid by bootstrap, not by `.gitmodules` (Q4)

**Decision.** The pin stays EXACT: `.gitmodules` carries no `branch=` and no
`update=merge`. Bootstrap checks each submodule out onto a tracking branch AT
the pinned commit, so the working state is branch-shaped while the recorded state
stays a pin. Advancing a pin remains an explicit assembly-root commit.

**Alternative rejected.** *`branch=` plus `update=merge`, so
`git submodule update --remote` follows a branch.* Rejected: it buys the same
ergonomics by WEAKENING the pin — the declared commit becomes advisory for
anyone running the remote form, which is the moving reference
`neutral-product-pin` already refuses in its own words. Putting the convenience
in a COMMAND rather than in checked-in configuration keeps exactly one
authoritative answer to "what commit is this project".

## D5 — Where the election is recorded, and which capability owns the field (Q5)

**Decision.** The assembly root's own manifest is the SOURCE; the register row is
DERIVED from it where an aggregation exists. The register delta is declared as
MODIFIED `ideation-dashboard`, because that capability owns the
`kind: project-register` requirement today; the new `project-repo-schema`
capability defines the VOCABULARY both carriers use and takes no ownership of the
register.

**Alternatives rejected.**

1. *Move the register requirement into `project-repo-schema`.* Rejected: two
   capabilities claiming one schema is two answers to one question, and moving
   the requirement out of `ideation-dashboard` is a larger unrelated change this
   packet should not pay for.
2. *The register is the origin of the election.* Rejected: a new organisation has
   no aggregation and no register. Making the manifest the source is the only
   construction under which such an organisation is conformant — and a file
   inside the project is readable by exactly the population that needs it.

## D6 — The register's field shape (new; forced by D5)

**Decision.** Three ADDITIVE, optional fields: per-project `schema` and
`reference`, and a per-project `repository_roles` list of
`{repository, role}` where `role` is `spec | code | assembly`. `repositories`
is UNCHANGED and remains the single membership answer; a repository named in
`repository_roles` must also appear in `repositories`; at most one `assembly` per
project.

**Alternatives rejected.**

1. *Retype `repositories[]` items from strings to `{id, role}` objects.*
   Rejected as consumer-breaking: `scripts/ideation_dashboard/register.py`'s
   `_repo_to_project` and `projects_of` read those items as strings, and so does
   every renderer downstream of the snapshot. Widening the schema does not widen
   the readers, and a schema change that silently breaks the one live consumer is
   not additive.
2. *Name the field `legs:`, matching the assembly manifest exactly.* Rejected:
   "leg" is SHAPE vocabulary, and a project that declines the schema has no legs.
   The register must read identically for an electing and a declining project, so
   the field is named for what it holds — repository roles — rather than for the
   shape that happens to have produced them.
3. *A bare `role:` map keyed by repository id.* Rejected as less checkable: a
   list of records gives the validator a place to stand for the duplicate,
   unknown-repository and multiple-assembly rules without inventing key-order
   semantics.

**The obligation this field creates, and how it is discharged.** `schema` and
`role` are exactly the fields a later consumer reads as permission. The fragment
named this as an obligation it could not discharge. It is discharged here in FOUR
places, deliberately: the ADDED capability's first requirement, the MODIFIED
register requirement's own text, the schema file's `description`, and the
assembly-root manifest template's header comment.

## D7 — The lockstep validator ships in the template (Q7)

**Decision.** Yes. The assembly template ships a validator asserting gitlink ==
`contracts/<role>-pin.yaml` `commit:` == every workflow reference naming that leg,
run in the assembly root's own pull-request gate, refusing with a remediation
string in the fail-closed form `neutral-product-pin` already requires.

**Alternative rejected.** *Leave it as a working rule in a `CLAUDE.md`.*
Rejected, and the rejection is MEASURED rather than argued: that is exactly what
the xFactory aggregation did. The invariant was practice for months and written
down nowhere; seven consecutive pin-syncs from 2026-08-25 moved the gitlink alone
and left `validate` red on every aggregation pull request until 2026-08-26
(xFactory #146), unnoticed for a day because `validate` runs on pull requests
only, so `main` never reports it. The invariant is not aggregation-specific — any
assembly root that both pins a leg and dispatches a workflow at that leg's sha has
it — so shipping the check in the template turns a per-project tribal rule into a
one-time scaffold cost.

## D8 — The bootstrap contract is schema-neutral, and degrades (Q8, Q12)

**Decision.** One command, the same command in any project root, with the
submodule step a no-op where there are no submodules. Where no wallet
review-authority register is found it prints exactly `authority is not
wallet-carried in this org` and CONTINUES.

**Alternatives rejected.**

1. *A bootstrap that exists only for electing projects.* Rejected: it would make
   election worth something operationally, which is what the ratified doctrine
   forbids. Schema-neutrality is how "confers nothing" survives contact with
   tooling.
2. *Fail when no wallet register is found.* Rejected: an organisation that has
   not adopted wallet-carried authority is not misconfigured, and a bootstrap
   that refused there would have made the layout load-bearing again — the exact
   property this line of work exists to prevent.

**The dependency this leaves, stated.** Step (c) reports what the engineer may
AUTHOR as well as review, and `author` is proposed by the sibling topic
`wallet-carried-work-authority`. Until that lands the readout reports REVIEW
authority only, and degrades rather than failing. This packet declares nothing
about `author` and defers it by name.

## D9 — The ownership split, and the two capabilities checked and left alone (Q6)

**Decision.** Four planes: openRepoShape owns the MECHANICS; openxFactory
ratifies the DOCTRINE, pins the standard and carries the register delta;
codexFactory owns the ENGINEERING OVERLAY and the act of recommending; OpsxFactory
owns organisation-level naming enforcement and repository-topic administration,
where GitHub administration was located by the two exit changes of the superseded
`github-administration-plane` topic (openxFactory
`archive/2026-07-14-add-github-app-identity-tiers`; OpsxFactory
`2026-07-15-add-github-administration-workflow`).

**Three capabilities were read requirement by requirement to see whether the new
repository kind contradicts one. None does, so none is modified — and the reading
is recorded because "we checked" is only a claim if it names what was checked.**

- **`neutral-product-pin`** (nine requirements). It enumerates NO products: its
  first requirement is written as a general rule over "an EXTERNAL neutral
  product", and the pin this change adds SATISFIES it as written — commit,
  `revision_kind`, per-file `sha256` for every artifact digested per file, and
  `pinned_by_commit_only:` for the rest, with a tag refused and no range
  expressed. Adding a second pinned product needs no spec-level statement; that
  a general rule absorbs a new instance without amendment is the rule working.
  **NOT MODIFIED.**
- **`domain-descendant-boundary`** (five requirements). All five govern a
  DomainxFactory consuming a neutral product THROUGH a `<Domainx><Product>`
  descendant. A project leg is not a descendant and does not consume a neutral
  product; D1's ruling keeps the descendant family's membership rule intact by
  requiring the pin those requirements already require, rather than widening
  membership to anything shaped like a descendant. **NOT MODIFIED.**
- **`repo-boundary-governance`** (nine requirements) and
  **`shared-contract-ownership`** (twelve). Their scoping requirements are about
  canonical workflow authority, install-repo scope, copy-first migration, the
  canonical contract home and contract-version pinning. The one that comes
  closest is *Canonical contract home* — "openxFactory SHALL define the canonical
  home for shared factory contracts that govern behavior between factory
  subsystems or across DomainxFactories". The doctrine document and the register
  delta land IN openxFactory and satisfy it; the standard's mechanics are not a
  shared factory contract governing behaviour between factory subsystems, they
  are a forkable repository-layout standard consumed by organisations that hold
  no factory at all, and openxFactory consumes them through the pin the same
  capability's sibling already ratifies. **NEITHER MODIFIED.**

**The narrowing that IS declared** is codexFactory's, and it is stated in the
spec text and in the proposal rather than assumed: it is a narrowing of where the
scaffold LIVES, never of what codexFactory may recommend.

## D10 — The standard is a standalone public product (Q9) — RULED

**Ruling: Brett Heap, 2026-09-02** — *"name it openRepoShape and make it
public"*, then *"apache 2.0, create it"*. `opensoft/openRepoShape` exists,
PUBLIC, Apache-2.0.

**Decision.** The mechanics live in that repository; openxFactory pins it by
commit and digest under `neutral-product-pin`, exactly as it pins openXwallet,
and keeps `docs/project-repo-schema.md` as the ratifying home of the doctrine.

**Alternatives rejected.**

1. *A directory inside openxFactory.* Rejected by the convener's own operating
   constraint: it cannot be forked into an organisation that has no openxFactory.
2. *`codeXfactory-repo-shape`, the convener's own earlier working name.*
   Superseded by his own ruling, and it was the wrong name on the merits: a
   codex-prefixed name signals an engineering-domain dependency in a repository
   whose entire purpose is to work WITHOUT codexFactory.
3. *Private, or unlicensed, matching openAvatar and openXwallet.* Rejected by the
   ruling. Verified 2026-09-02 by `gh repo view`: `openChart` and `openPractice`
   are PUBLIC under Apache-2.0 while `openAvatar` and `openXwallet` are PRIVATE
   with `licenseInfo: null`. The family now carries two DELIBERATE postures for
   `open*` rather than a drift — a repository meant to be forked into other
   organisations must be secret-free and licence-clear, and Apache-2.0's patent
   grant is the right posture for contract text and validators other
   organisations will fork and run.
4. *A GitHub template repository rather than a fork.* Rejected: a template copy
   severs the upstream link, and `contracts/shape-pin.yaml`'s drift comparison
   stops meaning anything. A fork keeps shape updates pullable.

## D11 — What openxFactory's pin covers, and how it is verified (new)

**Decision.** `contracts/openreposhape-pin.yaml` pins commit
`deacbdcce4f52af427bcb4edd075fcc992e3dabe` with SIXTEEN per-file `sha256`
digests — the standard's normative surface: the naming policy, the four
assembly-root contract and manifest templates, the scaffold, the setup entry
point, the bootstrap, the four shipped validators and the shared library, the
agent instruction file, the README and the LICENCE — and `pinned_by_commit_only:`
for the remaining EIGHTEEN members. Together the two lists cover all 34 files at
that commit, so no artifact appears in neither, which
`neutral-product-pin`'s own scenario calls *"an undeclared consumption, not a
permitted omission"*. `scripts/validate-openreposhape-pin.py` recomputes every
digest, asserts presence for every path-only member, and additionally asserts
SURFACE COMPLETENESS: a file present at the pinned commit and named by neither
list is a refusal.

**Alternatives rejected.**

1. *Pin the whole tree with a single `tree_sha256` and no per-file rows.*
   Rejected: the standard's own copy pin uses per-file digests for exactly the
   artifacts a consumer HOLDS, and openxFactory's verifier needs to say WHICH
   file drifted. A single tree digest reports that something changed.
2. *A submodule gitlink, as openXwallet has.* Rejected: openxFactory does not
   MOUNT the standard, it CITES it. There is nothing openxFactory runs out of an
   openRepoShape checkout, so a gitlink would add a working-tree obligation to
   every clone of this repository in exchange for nothing. The verifier therefore
   resolves bytes from a `--checkout` a caller supplies or from the host API, and
   REFUSES rather than passing when it can resolve neither.
3. *PyYAML, as `scripts/verify-openxwallet-pin.py` uses.* Rejected for this one
   tool: the pin's grammar is a fixed, small subset this repository authors, and
   a standard-library-only verifier can run in the same bare environment the
   standard itself insists on. The reader refuses anything outside that subset
   rather than guessing, so the narrowness is fail-closed rather than fragile.

**Deliberately NOT done: no release tag is cut.** The fragment's exit path said
openxFactory *"cannot pin openRepoShape until that product cuts a digested
release"*. That precondition is met differently and more strictly than a tag
would meet it: `revision_kind: commit` with per-file digests IS the digested
identity, and `neutral-product-pin` refuses a tag as a referent in its own words.
A tag may still be recorded beside the commit as a label when openRepoShape cuts
one; this pin does not wait for it and does not trust it.

## D12 — A project may start against a staged reference, and a pilot says so (Q10)

**Decision.** Yes. A project MAY elect against the STAGED fragment as its
reference, provided the manifest — and the register row where one exists —
records both the election and the reference followed. The house precedent is its
own: the staging index's draft-proposal workspace convention was *"Adopted
2026-07-13 (Brett), first used by ideation-dashboard"* before any spec carried it.

**AND THE PILOT IS TEMPORARY, which is a ruling and not a nuance.** Brett Heap,
2026-09-02: *"MedxScribe is only a temp pilot project right? it is not a real
project. make sure it noted as pilot to test the openRepoShape"*.
`MedxSoft/MedxScribe` and its two legs were scaffolded on 2026-09-02 SOLELY to
test `opensoft/openRepoShape` end to end. It is not a MedxSoft product, it is not
"the first project", and it may be deleted once this standard is ratified. The
three repositories carry `PILOT (temporary): …` descriptions and the topics
`pilot` and `openreposhape-pilot`, and the assembly root's README carries a
banner.

**Alternative rejected.** *Cite the pilot repositories as the realization
evidence.* Rejected because it would make the evidence depend on temporary
repositories continuing to exist. The evidence is the RECORDED RUN — the
commands, the three commits, the validator outcomes and the degrade line, all
written into `proposal.md` § Realization evidence and into `tasks.md` — plus the
standard's own `tests/test_scaffold_e2e.py`, which re-runs the same path into
bare repositories on every openRepoShape pull request. Evidence with a half-life
is not evidence, and the spec says so in its own requirement.

## D13 — The new-organisation flow (Q11)

**Decision.** The concrete sequence, which is the convener's own third question
answered literally: (1) FORK `opensoft/openRepoShape` into the new organisation —
a fork, not a template, so the upstream link survives and shape updates pull.
(2) In the fork, run the setup entry point, which validates the three names
against the naming policy, prints the plan, ASKS ONCE, then creates the three
repositories, adds the two legs as submodules with their digest pins, writes the
shape pin recording the openRepoShape commit and digest the project was
scaffolded from, writes the self-describing manifest, and sets the GitHub topic on
all three. (3) `git clone --recurse-submodules`, then the one bootstrap command.

**Alternative rejected.** *A GitHub template repository.* Same rejection as D10.4,
for the additional reason that the shape pin's drift comparison is only
meaningful against an upstream the fork can still see.

**The requirement hidden in the convener's phrasing.** *"tell my ai to scaffold a
new project based on that"* is a requirement, not a figure of speech: the fork
must carry AGENT-READABLE instructions, or the flow depends on a prompt somebody
remembers. The standard carries them.

## The two defects the pilot found, and how the standard now handles them

Both were found by the FIRST pilot run on 2026-09-02, both were fixed upstream
the same day, and **the pin this change carries is at `deacbdc`, the commit that
carries both fixes.** The pilot is therefore not merely evidence that the
standard works; it is the reason the standard the corpus ratifies is the fixed
one.

1. **Organisation misdetection preferred `upstream` over `origin`.** The setup
   entry point detected the organisation from the `upstream` remote, so a
   correctly-made fork was refused as an attempt to scaffold into `opensoft`
   (worked around on the day with `--org MedxSoft`). **Fixed:** openRepoShape
   PR #3, `7edd6bb` — the organisation is detected from the fork's OWN `origin`.
   The refusal it was guarding remains, because cloning the upstream instead of
   forking it looks identical from inside the directory: scaffolding into
   `opensoft` still requires an explicit flag, and the standard's agent
   instructions forbid an assistant from passing it on its own initiative.
2. **A descendant-shaped name was read as a fact rather than a claim.** The
   scaffold refused `MedxScribe` as *"domain-descendant, not the assembly form of
   a project leg"* — for a name that descends from nothing, no `openScribe`
   existing. **Fixed:** openRepoShape PR #4, `deacbdc` — a descendant form is a
   CLAIM that needs a declared referent pin, the declared role wins otherwise,
   and the overlap is RECORDED in the manifest's `also_matches` rather than
   discarded. This is D1's ruling, and the naming policy carries `MedxScribe`
   in its own data as a `claim_without_referent_examples` row so the rule is
   testable from the contract rather than from memory.

## Open items the convener may still wish to rule

Neither blocks this packet; both are recorded so they are not discovered later.

- **OI-1 — the GitHub topic's administration.** The topic form `xf-project-<id>`
  is fixed by the standard's naming policy and set by the scaffold. WHO enforces
  it organisation-wide, and what happens to a repository whose topic drifts from
  its register row, is OpsxFactory's GitHub administration plane's question and
  is left to its successor change. This packet states the drift RULE (the
  register wins, the others are reported) and no enforcement mechanism.
- **OI-2 — whether the register's `schema` value set is ever closed.** Today
  `project-repo-schema` is the only defined value and the schema constrains the
  field only to a non-empty string, deliberately: closing an enumeration in the
  first change that opens it forecloses a second schema nobody has proposed. If
  the convener would rather it be closed now, that is a one-line schema edit.
