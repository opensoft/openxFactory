# Proposal Ratification: add-project-repo-schema

Status: ratified
Decision date: 2026-09-02
Ratifier: Brett Heap (openxFactory convener) — in the working session
Ratified: 2026-09-02 by Brett Heap (openxFactory convener) — in the working
session, verbatim: *"ratify it"*.
Ratified baseline: the packet as it stands on `main` after PR #605 landed at
squash `642ac147` with five checks green — `proposal.md`, `design.md`,
`tasks.md`, `.openspec.yaml`, `supporting-docs/`,
`specs/project-repo-schema/spec.md` (ELEVEN ADDED requirements over 28
scenarios) and `specs/ideation-dashboard/spec.md` (ONE MODIFIED requirement,
"Project grouping hierarchy") as they stood at that commit.

## Decision

**RATIFY.** One word, given on the packet as landed, and it decides the
CONTENT — which is the act the proposing pull request deliberately did not
perform. Brett Heap's earlier instruction of 2026-09-02, *"start the
add-project-repo-schema exit change"*, is the `.openspec.yaml` origin pair:
permission to AUTHOR, recorded as `approved_by` / `approved_on`, and explicitly
"ADMISSION INTO THE PROPOSAL QUEUE AND NOT A RATIFICATION OF CONTENT". The two
acts are separate and this record keeps them separate.

## What is ratified

**One ADDED capability and one MODIFIED capability.**

- ADDED `project-repo-schema` — eleven requirements: the shape is ELECTIVE and
  CONFERS NOTHING, a one-repository project being reviewed identically; the
  ASSEMBLY leg is the per-project ROOT an engineer clones (R2); the
  `<Project>` / `<Project>-spec` / `<Project>-code` naming families with a
  `<Domainx><Product>` form read as a CLAIM needing a declared `open<Product>`
  pin (R3); the double pin and its one-commit lockstep invariant; the
  assembly-root manifest as the SOURCE a register row derives from; the
  schema-neutral bootstrap and its verbatim `authority is not wallet-carried in
  this org` degrade line; overlays that attach to a shape and never the
  reverse; the standard living in the public Apache-2.0 `opensoft/openRepoShape`
  (R4, R5), consumed by fork and pinned by openxFactory under
  `neutral-product-pin`; the four-way ownership split; and the
  pre-ratification election rule with the pilot on record (R7).
- MODIFIED `ideation-dashboard` — "Project grouping hierarchy" gains an optional
  per-project `schema`, an optional `reference` and an optional
  `repository_roles` list, all additive, `repositories` unchanged as the single
  membership answer, canon's body carried verbatim and all five original
  scenarios retained.

**The narrowing is ratified as stated and no further.**
`add-wallet-carried-review-authority`'s *"codexFactory may recommend — and
scaffold"* is narrowed in WHERE THE MECHANICS LIVE and in nothing else;
codexFactory keeps the recommending role and its engineering overlay in full.
That change's two spec deltas are untouched, and no `## MODIFIED Requirements`
block is declared over them.

## What ratification does NOT do

**It authorizes realization; it does not perform it.** `code_surface` is
non-empty and `target_release` names the next additive contract bundle after
`contract-v3.0`, UNNUMBERED because `docs/contract-versioning-policy.md` forbids
reserving a minor before merge order is known. Under `release-realization`'s
realization archive gate this change stays ACTIVE — approved-but-unrealized
intent — and the archive decision taken with this ratification is recorded
below.

**It decides no authority question.** Every one is deferred by name to the
sibling staged topic `wallet-carried-work-authority`. This packet declares no
grant, no clearance, no gate standing and no floor, and a consumer deriving any
permission from `schema`, `role` or a naming family is DEFECTIVE.

**It does not promote the doctrine document to `standard`.**
`docs/project-repo-schema.md` moves to `Status: ratified` +
`Ratified by: add-project-repo-schema`, which is what the lifecycle allows a
document backed by an approved change to claim. `standard` requires a PROMOTED
spec, and nothing is promoted until this change archives.

**It does not tick the successors.** `tasks.md` slices 7 (the codexFactory
engineering overlay) and 8 (OpsxFactory organisation administration) are
successor changes in their own repositories, named rather than implied, and none
is a precondition of this packet. 4.6 — making the `openreposhape-pin` check
REQUIRED on the default branch — is an operator act on an organisation ruleset.
6.2 — deleting the temporary pilot — is the convener's option and retracts
nothing.

## Archive decision at ratification: DO NOT ARCHIVE

`release-realization` § Realization archive gate:

> A change with a non-empty code surface SHALL NOT archive until realization
> evidence exists: its code merged on the implemented target through the owning
> domain's engineering gates, and — where the surface is runnable — a green run
> of that surface. … Until then the change remains active as
> approved-but-unrealized intent, preserving the invariant that promoted specs
> describe what the code does.

The merge half and the green-run half are both satisfied. The RELEASE half is
not: `target_release` is a named additive contract bundle, not `implemented`,
and that bundle is not cut. The repository's own check says so — `doc-health`
reports `release-inventory-drift` at ERROR on
`scripts/validate-ideation-dashboard-contracts.py`, "bytes differ from the
digest 'contract-v3.0' records", whose action string is *"cut a release through
the bundle realization order"*. `tasks.md` 9.3 owns that cut and is UNTICKED; it
is an act this packet owes, not a deferral by design, unlike 4.6, 6.2, 7.x and
8.x which name their owners elsewhere. Two further archive-preflight tasks are
also open: 9.2 (re-verify the pin and re-run the slice 4 and 5 validators
against the tree the archive would promote deltas over) and 9.4 (package
`supporting-docs/` into the deterministic bundle the same capability's proposal
support archive gate requires).

The precedent is exact and recent. `add-signed-execution-chain` was ratified
2026-08-29 and archived only on 2026-08-31, after its task 4.7 took the
`contract-v2.5` cut; `add-binding-consumer-identity`'s own ratified text says
the change "stays ACTIVE until merged code, green evidence and the contract cut
exist, per `release-realization`".

**So: ratified and ACTIVE.** The archive act is a later one, and the between-cuts
`release-inventory-drift` finding is the EXPECTED state until it happens — never
to be silenced by hand-editing an inventory or `contract_bundle_version`, which
that finding's own action string forbids in as many words.

## Realization evidence read at this ratification

| # | evidence | state |
| --- | --- | --- |
| E1 | The packet and its four landing artifacts merged on `main` — PR #605, squash `642ac147`, five checks green | MET |
| E2 | `openreposhape-pin` gate green on that pull request | MET |
| E3 | `scripts/validate-openreposhape-pin.py` green against the real `opensoft/openRepoShape` bytes at `deacbdcce4f52af427bcb4edd075fcc992e3dabe`, through both resolvers (`--checkout` and `--from-gh`), and refusing `pin-unresolvable` with neither | MET |
| E4 | `tests/openreposhape_pin` (21) and `tests/ideation_dashboard` register-election tests (13 of the 95) green; `scripts/validate-ideation-dashboard-contracts.py` → 0 errors, 0 warnings over 42 valid and 80 negative examples | MET |
| E5 | The `MedxSoft/MedxScribe` end-to-end run of 2026-09-02 against upstream `deacbdc` — RECORDED in `proposal.md` § Realization evidence and `tasks.md` 6.1, and independent of the pilot repositories continuing to exist (R7) | MET, and deletion-proof |
| E6 | The additive contract bundle carrying the moved registered validator (`tasks.md` 9.3) | **NOT MET** — the archive blocker |
| E7 | Pre-archive re-verification (9.2) and the `supporting-docs/` bundle (9.4) | NOT MET — archive-time preflight |

E5 is deliberately constructed so that the pilot's deletion retracts nothing:
the evidence is the RUN, the commands and the commits are written down here and
in the packet, and openRepoShape's own `tests/test_scaffold_e2e.py` re-runs the
same path into bare repositories on every pull request there. Evidence that
required a temporary repository to stay alive would be evidence with a
half-life.

## Verification at the ratified head

- `OPENSPEC_TELEMETRY=0 openspec validate --all --strict` → `Totals: 86 passed, 0 failed (86 items)`
- `python3 scripts/doc-health.py --single-repo .` → `6 critical, 6 error, 29 warning, 14 info. New regressions vs previous report: 0` — unchanged from the pre-ratification baseline
- `python3 scripts/validate-ideation-routing.py` → green
- `python3 -m pytest tests/openreposhape_pin tests/ideation_dashboard tests/proposal-support -q -m "not postgres"` → green
- `python3 scripts/validate-openreposhape-pin.py --checkout <openRepoShape@deacbdc>` → `OK openreposhape-pin verified`

## Rulings carried, not re-litigated

R1 (2026-08-22, the elective shape, ratified inside
`add-wallet-carried-review-authority`), R2–R5 and R7 (2026-09-02: assembly is
per project; descendant only if it pins `open<Product>`; name it openRepoShape
and make it public; Apache-2.0, create it; MedxScribe is a temporary pilot), and
R6 (2026-09-02, admission of this packet into the proposal queue — authoring,
not ratification). This record adds none and amends none.
