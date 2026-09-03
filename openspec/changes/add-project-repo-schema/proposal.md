---
code_surface: openxFactory — FIVE artifacts, all NEW or ADDITIVE, and four of them land in this pull request. (1) `docs/project-repo-schema.md`, the ratifying home of the doctrine (`Status: draft` now; `ratified` when this packet is). (2) `contracts/openreposhape-pin.yaml`, openxFactory's consumption of `opensoft/openRepoShape` at commit `deacbdcce4f52af427bcb4edd075fcc992e3dabe`, in the `neutral-product-pin` shape and the `kind: pinned_contract_manifest` grammar reused unchanged. (3) `scripts/validate-openreposhape-pin.py`, the running code that checks that claim — standard library only, fail-closed, five named refusal codes and one fixed remediation trailer — wired into a new `.github/workflows/openreposhape-pin-gate.yml` on the `openxwallet-consumer-gate.yml` pattern. (4) `contracts/schemas/project-register.schema.yaml` gains an optional per-project `schema`/`reference` election and an optional `repository_roles` list, with the cross-field rules in `scripts/validate-ideation-dashboard-contracts.py` and tests in `tests/ideation-dashboard/` and `tests/openreposhape_pin/`. (5) NOT in this pull request and not owed by it: the codexFactory ENGINEERING OVERLAY and the OpsxFactory org-naming/topic administration, each a successor change in its own repository. The standard's own mechanics are NOT openxFactory's code surface at all — they live in `opensoft/openRepoShape`, which openxFactory consumes and does not author.
target_release: the next additive contract bundle after `contract-v3.0` — number ALLOCATED AT REALIZATION by merge order, never reserved here, per `docs/contract-versioning-policy.md` § Version Identity: "A proposed change MUST NOT reserve a minor number before merge order is known". ONE REGISTERED ARTIFACT MOVES, and it is not the one an earlier draft of this field named: `scripts/validate-ideation-dashboard-contracts.py` is row `scripts-validate-ideation-dashboard-contracts.py` of `contracts/releases/contract-v3.0.digests.yaml` (`:1417-1418`), and this change edits it. THE CLASS IS ADDITIVE: the validator only GAINS four cross-field rules over three new OPTIONAL register fields, no existing field changes, and no consumer pinned at `contract-v3.0` is made non-conformant. The other two artifacts are NOT registered rows and spend nothing — `contracts/schemas/project-register.schema.yaml` appears in neither `contracts/manifest.yaml` nor the v3.0 inventory (measured: zero occurrences in each), and `contracts/openreposhape-pin.yaml` is a CONSUMPTION pin in the shape of `contracts/openxwallet-pin.yaml`, likewise absent from the inventory. UNTIL THAT CUT, `doc-health`'s `release-inventory-drift` family reports the validator's bytes as differing from the digest `contract-v3.0` records. That is the EXPECTED between-cuts state its own action string describes — "cut a release through the bundle realization order" — and it MUST NOT be resolved by hand-editing the inventory or `contract_bundle_version`, which that same action string forbids in as many words.
Status: draft
---

# Proposal: add-project-repo-schema

Status: draft
Proposed: 2026-09-02 — the FULL promotion of the staged topic
`project-repo-schema` (`openxFactory:staging:project-repo-schema`, staged
2026-09-02), on Brett Heap's in-session instruction the same day: *"start the
add-project-repo-schema exit change"*. That instruction is ADMISSION INTO THE
PROPOSAL QUEUE AND NOT A RATIFICATION OF CONTENT. It supplies the origin and
approval pair the proposal-origin contract requires and nothing more: this
packet carries no ratification citation and none is owed, the promoted lifecycle
rule requiring one only for `Status: ratified`. **Ratification is the
convener's.**

## Why

`add-wallet-carried-review-authority` — ratified 2026-08-23 — already RECOMMENDS
a three-repository shape for a project, on the convener's 2026-08-22 ruling
quoted in it verbatim: *"For our own internal projects, we can have codeXfactory
recommend and run a 3 repo project schema. But let the human project manager
decide."* (`proposal.md:600-617`). It rules who elects it (a `PA` decision,
`CA`-constrained and `PM`-sequenced) and what electing it buys: **nothing** —
*"Electing the schema changes no gate, no floor, no grant, and no clearance
eligibility"*, and a one-repository and a three-repository project *"are reviewed
IDENTICALLY, because the authority travels in the grants rather than in the
layout"*.

**And then it stops.** Verified at this branch's tip, and the fragment's claim
re-measured here: that change's own `specs/` deltas are exactly two
(`review-authority-intake`, `roles-authority-model`); no `project-repo-schema`
capability exists under `openspec/specs/`; and repository-wide greps for
"recommended project schema", "three-repositor" and the governance sense of
"ASSEMBLY" resolve only to that one proposal plus its `tasks.md:811-814`. There
is no name form, no schema field, no scaffold, no bootstrap and no validator.
**A `PA` who says yes has nothing to say yes to.** The delta is therefore ADDED
and not MODIFIED: there is nothing yet to modify.

The convener asked the ergonomics questions directly, in four parts on
2026-09-02, and each one has no answer in the corpus: GitHub has no folder that
groups repositories; are spec and code submodules of the assembly; how does an
engineer clone it all down and get started; where is this documented so a
project can start *"before codex is ready to support all this or even outside
codex"*; and *"if I have a new org … I think i need to fork the … repo from
opensoft and then tell my ai to scaffold a new project based on that."*

Layout is also now FREE to be optimized for humans, which is the second half of
why this is worth doing at all.
`add-wallet-carried-review-authority` demoted repository topology from the spine
of authority to an elective layout precisely so layout would carry no governance
weight; the sibling staged topic `wallet-carried-work-authority` — staged the
same day and landed on `main` first — removes the last hidden coupling by making
grants path-scoped rather than repository-granular. **This change takes that
freedom and does the ergonomics, only.** Every authority question is DEFERRED to
that sibling by name, and this packet answers none of them.

## What changes

**One ADDED capability, `project-repo-schema`, and one MODIFIED capability,
`ideation-dashboard`.** The ADDED capability is the neutral contract: the
doctrine (elective, confers nothing), what ASSEMBLY means, the naming families,
the double pin and its lockstep invariant, the manifest-is-the-source rule, the
bootstrap contract and its degrade line, the overlay rule, where the standard
lives and how openxFactory consumes it, the ownership split, and the pilot rule.
The MODIFIED capability is the register: `ideation-dashboard` owns the
`kind: project-register` requirement today (`spec.md`, "Project grouping
hierarchy"), so the election fields are declared there rather than claimed by a
second capability.

**The mechanics are NOT authored here.** They live in
`opensoft/openRepoShape` — PUBLIC, Apache-2.0, both ruled by Brett Heap on
2026-09-02 (*"name it openRepoShape and make it public"*, then *"apache 2.0,
create it"*) — and openxFactory CONSUMES that standard at a commit and a set of
digests under `neutral-product-pin`, exactly as it consumes `openXwallet`. The
reason is the convener's own operating constraint: a directory inside
openxFactory cannot be forked into an organisation that has no openxFactory,
and the shape must survive being forked into an org with no openxFactory, no
codexFactory and no wallet register.

**What this change realizes IN THIS PULL REQUEST** (each ticked in `tasks.md`,
and nothing else is ticked):

1. `docs/project-repo-schema.md` — the doctrine document, `Status: draft`.
2. `contracts/openreposhape-pin.yaml` — the pin, `revision_kind: commit`,
   commit `deacbdcce4f52af427bcb4edd075fcc992e3dabe`, sixteen per-file `sha256`
   digests computed from the real bytes at that commit and
   `pinned_by_commit_only:` for the remaining eighteen members, so no artifact
   appears in neither list.
3. `scripts/validate-openreposhape-pin.py` + `.github/workflows/openreposhape-pin-gate.yml`
   — the running check, green against the real openRepoShape bytes.
4. The register schema's additive fields, their cross-field validator rules, and
   tests for both.

**What is PENDING, and named rather than implied:** the codexFactory engineering
overlay, the OpsxFactory org naming and topic administration, and the aggregation
`project-register.yaml` row for any project that elects. Each is a successor
change in its own repository; none is owed by this packet, and none is a
precondition of it.

## The rulings this change carries

Fixed by the convener, cited rather than re-argued. This packet does not
re-litigate any of them.

| # | ruling | date | what it settles |
|---|---|---|---|
| R1 | *"For our own internal projects, we can have codeXfactory recommend and run a 3 repo project schema. But let the human project manager decide."* | 2026-08-22 | the shape is ELECTIVE and human-elected; ratified inside `add-wallet-carried-review-authority` |
| R2 | *"yes, assembly is per project"* | 2026-09-02 | the ASSEMBLY leg IS the per-project root repository the engineer clones (Q2) |
| R3 | *"Descendant only if it pins open&lt;Product&gt;"* | 2026-09-02 | a `<Domainx><Product>`-shaped name is a domain descendant only where the project declares a pin on the matching `open<Product>`; otherwise the declared role wins and the manifest records `also_matches` (Q1) |
| R4 | *"name it openRepoShape and make it public"* | 2026-09-02 | the standard's name and PUBLIC visibility (Q9) |
| R5 | *"apache 2.0, create it"* | 2026-09-02 | the licence, and the act of creating the repository (Q9) |
| R6 | *"start the add-project-repo-schema exit change"* | 2026-09-02 | admission of THIS packet into the proposal queue — authoring, not ratification |
| R7 | *"MedxScribe is only a temp pilot project right? it is not a real project. make sure it noted as pilot to test the openRepoShape"* | 2026-09-02 | the pilot is TEMPORARY and exists only to test openRepoShape; the evidence is the recorded run, not the repositories' continued existence |

## What this change supersedes, and exactly how far

**The ratified prose reads as codexFactory owning the scaffold, and this change
NARROWS that — in where the mechanics LIVE, and in nothing else.**
`add-wallet-carried-review-authority` says, at `proposal.md:606-608`,
*"codexFactory may recommend — and scaffold — a three-repository shape for a
project: SPEC (the governing specs and contracts), CODE (the implementations),
and ASSEMBLY (the code that assembles a review team, shared across the family)."*

Two clauses of that sentence are narrowed and one is not:

1. **"and scaffold" is narrowed.** The neutral scaffold lives in
   `opensoft/openRepoShape`, not in codexFactory, because the convener's own
   case — a new org with no codexFactory — cannot be served by a scaffold that
   is a directory of an engineering-domain repository. codexFactory keeps an
   ENGINEERING OVERLAY on the neutral scaffold, and
   `add-wallet-carried-review-authority`'s `tasks.md:811-814` (task 8.4) is
   satisfied by overlay-plus-offer rather than by codexFactory hosting the
   neutral shape.
2. **"ASSEMBLY (the code that assembles a review team, shared across the
   family)" is narrowed by R2.** Read as ONE shared repository, an electing
   project has SPEC and CODE and no root to clone, and the convener's actual
   question has no answer. Under R2 the ASSEMBLY leg is the PER-PROJECT ROOT,
   and the shared review-team code is something that root MAY PIN as an overlay
   — which is how the aggregation already consumes the review lane at
   `review-lane-reusable.yml@<sha>`. Both readings then hold, and no ratified
   sentence is contradicted.
3. **"codexFactory may recommend" is NOT narrowed.** codexFactory keeps the
   recommending role in full. What moved is where the mechanics are hosted.

**Nothing else in that change is touched.** Its two spec deltas are untouched,
its election-confers-nothing doctrine is carried forward verbatim as this
capability's first requirement, and no `## MODIFIED Requirements` block is
declared over it — the narrowing lands as new text in a new capability that
cites the sentence it narrows, which is the smaller act.

## What is deferred, and to what

**Every authority question is deferred to `wallet-carried-work-authority`**, the
sibling staged topic, by name and without exception. This packet declares no
grant, no clearance, no gate standing and no floor. The bootstrap's authority
readout (below) reports what a register already says and confers nothing by
reporting it; where the sibling's `author` verb does not exist, the readout
reports review authority only.

**And the layout confers nothing.** That sentence is not a courtesy — it is the
first requirement of the ADDED capability, it is restated in the register's
schema description, in its requirement text, in the doctrine document and in the
manifest template, and a consumer deriving any permission from `schema`, `role`
or a naming family is DEFECTIVE. A project that declines this schema is reviewed
identically to one that elects it.

## Realization evidence, and why it survives the pilot's deletion

**`MedxSoft/MedxScribe` is a TEMPORARY PILOT and not a real project.** Ruled by
Brett Heap on 2026-09-02: *"MedxScribe is only a temp pilot project right? it is
not a real project. make sure it noted as pilot to test the openRepoShape"*. It
was scaffolded on 2026-09-02 for one purpose — to run `opensoft/openRepoShape`
end to end — it is not a MedxSoft product, it is not "the first project", and it
MAY BE DELETED once this standard is ratified. Its three repositories carry the
description prefix `PILOT (temporary): …` and the topics `pilot` and
`openreposhape-pilot`, and the assembly root's README carries a banner saying so.

**The evidence is the RUN, and the run is recorded here.** On 2026-09-02, from a
MedxSoft fork synced to upstream `deacbdc`, the command
`./setup.sh --project MedxScribe --visibility private --yes` succeeded end to
end: it created `MedxSoft/MedxScribe` (assembly root, `07060d4`),
`MedxSoft/MedxScribe-spec` (`52c96cb`) and `MedxSoft/MedxScribe-code`
(`023a27f`); set the topic `xf-project-medxscribe` on all three; mounted the
legs at `spec/` and `code/`; wrote the shape pin `opensoft/openRepoShape @
deacbdc`; and recorded the election by `brettheap` on 2026-09-02 with the staged
fragment's path as its `reference:`. The manifest recorded that `MedxScribe`
ALSO matches the descendant form with no referent pin declared, so it is not a
descendant unless `contracts/openscribe-pin.yaml` is added — R3 exercised on the
case that forced it. `git clone --recurse-submodules` followed by `make
bootstrap` left both legs on `main` AT their pins, the naming, manifest and
lockstep-pin validators green, the shape copy pin (9 files) green, and printed
the degrade line verbatim: `authority is not wallet-carried in this org`.

**That record does not depend on the pilot repositories continuing to exist.**
The realization step in `tasks.md` cites this paragraph and the commits named in
it; deleting the pilot does not retract the run, and the standard's own
`tests/test_scaffold_e2e.py` re-runs the same path into bare repositories on
every openRepoShape pull request. A realization step that required a temporary
repository to stay alive would be evidence with a half-life, which is not
evidence.

**Two defects the pilot found, both fixed upstream before this packet was
written.** The first run refused `MedxScribe` as an assembly root under the old
precedence rule although no `openScribe` exists, and separately hit a `setup.sh`
org-detection defect that preferred the `upstream` remote over `origin` and so
refused a correct fork (worked around with `--org MedxSoft`). openRepoShape PR
#3 (`7edd6bb`) detects the org from the fork's own `origin`; PR #4 (`deacbdc`)
makes a descendant form a CLAIM that needs a declared pin. **The pin this change
carries is at `deacbdc` — the commit that carries both fixes** — so the standard
openxFactory ratifies is the one the pilot proved, not the one it broke.

## Impact

- **Affected specs.** ADDED `project-repo-schema` (eleven requirements).
  MODIFIED `ideation-dashboard` (one requirement, "Project grouping hierarchy",
  carried verbatim with the additions marked in place and every original
  scenario retained).
- **NOT modified, and each checked rather than assumed.**
  `neutral-product-pin` — its nine requirements enumerate no products, so
  adding openRepoShape as a pinned product needs no spec-level statement; the
  pin CONFORMS to the requirement as written and that is the whole point of a
  general rule. `domain-descendant-boundary` — its five requirements govern a
  DomainxFactory consuming a neutral product through a descendant; a project leg
  is not a descendant, and R3 keeps the descendant family's membership rule
  intact rather than widening it. `repo-boundary-governance` and
  `shared-contract-ownership` — read requirement by requirement in `design.md`
  § D9; nothing this change adds contradicts one, so neither is touched.
- **Affected code.** Listed in `code_surface` above.
- **Blast radius on adoption is zero by construction:** every artifact is new,
  every register field is optional, no existing repository is renamed, and no
  project is elected into anything. Electing the schema stays a `PA` decision,
  per project, conferring nothing.

## Ratification

**Ratification is the convener's.** This packet is `Status: draft`. Brett Heap's
instruction of 2026-09-02 authorized AUTHORING it and recorded the rulings above
as locked constraints; it decided nothing about the content, which is declared
here and not accepted.
