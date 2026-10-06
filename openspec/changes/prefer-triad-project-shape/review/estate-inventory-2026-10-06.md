# Estate Inventory: prefer-triad-project-shape

Status: record
Kind: report
Lane: codeXfactory-5
Session: ed23f049-7e99-4601-8a6d-760b6aeb5f26
Captured: 2026-10-06, measured in one pass from 2026-10-06T18:57:19Z to 2026-10-06T19:01:23Z
Task: `tasks.md` § 5.7, *the estate inventory, a recommendation only* (`design.md` D7)
Authority: the realization of this RATIFIED change, on Brett Heap's in-session word of 2026-10-06T17:41:18Z, verbatim *"usage is fine, launch all four"*. The ratifying word was 2026-10-06T16:02:16Z, verbatim *"ratify 1249 as recommended"*, recorded at `review/ratification-2026-10-06.md`.
Inventory read: `scripts/estate-repository-inventory.yaml`, 37 rows, at openxFactory `main` `e63809650d39586134c4ec4fdb6e9effc87a7860`, blob `ce17309515898aec3b078ec2ea04492caef5e084`. The file was last changed by `1c6662e7862e2c1389d05a2bf78f3a4b54eb5157` (#1163), and the same blob stands at `c44c16105ef7f18202711ba75094754af8f0b58f`, this record's base.
Naming policy read: `opensoft/openRepoShape` `contracts/repository-naming.yaml` at `39d5c986fcfac1a160474bfe91c5f1c37fccc72c`, that repository's `main` when measured.

## What this record is, and what it is not

**A RECOMMENDATION ONLY, ADDRESSED TO EACH REPOSITORY'S OWNER.** For each of
the 37 repositories in the estate inventory, this record reports what that
repository is on its own `main`: a Triad, a leg, a family holder, a workspace
repository, or a single repository. For each single repository it also gives a
recommendation, either migrate or record staying single, to the person who
decides for that project. **The recommendations are not decisions.** They bind
nobody, and each owner may take one, take the other, or do nothing.

**It converts nothing and records nothing on any repository's behalf.** Every
read was an HTTP GET. No file was written to any of the 37 repositories, and no
issue, comment, branch or pull request was opened on any of them. No
`single-repository.yaml` or `project.yaml` was created anywhere.

**The preference is stated here with its posture, as the ratified requirement
says it must be.** The Triad is the PREFERRED project shape, and preferred is
not required. A project's repository layout confers no gate, no floor, no
grant, no clearance eligibility and no lifecycle state. A single repository is
reviewed IDENTICALLY to a Triad. A repository whose owner takes neither
recommendation, and records nothing, owes nothing.

**This record is not a review input.** Under the ratified requirement *A
project's shape is never a review input*, no review lane, required check,
validator, floor, merge gate, clearance or council may read this record, a row
of it, or a recommendation in it, in order to pass, fail, warn or change any
eligibility. It is a dated measurement for owners to read, and nothing more.

## 1. Method

**The rules are the ratified ones, applied in this order, and the first match
wins.**

1. **Triad.** A root `project.yaml` with `kind: project-manifest`, `schema:
   project-repo-schema`, and `legs:` entries for `role: spec` and `role: code`.
2. **Leg.** A name in the `spec` or `code` role form of openRepoShape's
   `project-leg` naming family (`^[A-Za-z][A-Za-z0-9]*-spec$`,
   `^[A-Za-z][A-Za-z0-9]*-code$`), or an `AGENTS.md` that says the repository
   is a leg. The leg templates' `AGENTS.md` opens "This is the **spec leg** of"
   or "This is the **code leg** of".
3. **Family holder.** A `family.yaml` with `kind: family-manifest` and no
   `project.yaml`.
4. **Workspace repository.** The `<user>-wip` form, which is the naming
   policy's `workspace` family.
5. **Single repository.** Everything else. Classes are not guessed (OQ-2,
   ruled). Where a single repository is an aggregation, a configuration
   repository or a fork, that is NOTED (§ 4, note A) to inform its
   recommendation, and the repository stays a single repository.

A `single-repository.yaml` at a repository's root would be reported as
"records staying single", beside its class.

**Every read was a GitHub REST GET made with `gh api`,** under an operator
token that can read every row, private ones included.

- `repos/{repo}` gave the default branch. For all 37 rows it is `main`, so
  "its default branch" and "its own `origin/main`" name the same branch.
  The same call gave `fork`, which is `false` for all 37.
- `repos/{repo}/commits/main` gave the head sha in the table's third column.
  **Every file below was read AT THAT SHA,** so each row stays fixed even after
  `main` moves.
- `repos/{repo}/contents/{path}?ref={sha}` read `project.yaml`, `family.yaml`,
  `single-repository.yaml` and `AGENTS.md`. An HTTP 404 means the file is
  absent.
- `repos/{repo}/git/trees/{sha}` gave the root listing, which was used only to
  inform a recommendation's reason. A private repository's reason draws on
  nothing beyond the inventory's own `role:` text, its class, and public
  sources.
- **Each name was classified by openRepoShape's own validator,** not by hand.
  The command was `python3 scripts/validate-repository-naming.py <the 37
  names>`, run in a read-only clone of `opensoft/openRepoShape` at
  `39d5c986`. Its verdict is the "name form" in the evidence column.

**openxFactory's own row is measured at `fc4fa0ff`, its `main` at that
moment.** `main` has since moved to `c44c1610` through #1253 and #1252. Neither
adds a root `project.yaml`, `family.yaml` or `single-repository.yaml`.

## 2. The inventory

Rows follow the inventory's own order. "Name form" is the naming validator's
verdict. A recommendation is given for single repositories only, and every
recommendation is a recommendation to the owner, never a decision (see above).

| # | repository | `main` head (measured) | class | evidence (path) | recommendation, for the owner — and why |
| ---: | --- | --- | --- | --- | --- |
| 1 | `opensoft/xFactory` | `1047586df1885146437c4dd461bc3f0b016a0dd1` | single repository | no `project.yaml`, `family.yaml` or `single-repository.yaml` at the root; name form `project-leg/assembly` | **record staying single** (`single-repository.yaml`) — an aggregation (inventory role: aggregation root; owns workspace assembly and pins only): it assembles other repositories by gitlink, and the shape question belongs to the repositories it mounts |
| 2 | `opensoft/openxFactory` | `fc4fa0ffc8726d7312e49aaa22316713c2ece641` | single repository | no `project.yaml`, `family.yaml` or `single-repository.yaml` at the root; name form `neutral-product` | **migrate** (`adopt-project.py`) — a product with code and specs: its specification and contract corpus (`openspec/`, `specs/`, `contracts/`) beside its validators, its reference runtime helpers and their tests (`scripts/`, `xfactory/`, `tests/`) |
| 3 | `codeXfactory/codexFactory` | `5ef09e3a0104acafc183c875a44429c47e13f510` | single repository | no `project.yaml`, `family.yaml` or `single-repository.yaml` at the root; name form `project-leg/assembly` | **migrate** (`adopt-project.py`) — a product with code and specs (inventory role: DomainxFactory, engineering) |
| 4 | `MedxSoft/MedxFactory` | `2dfde5b18a40280eaa8d815204f0e902e7743cb4` | single repository | no `project.yaml`, `family.yaml` or `single-repository.yaml` at the root; name form `project-leg/assembly` | **migrate** (`adopt-project.py`) — a product with code and specs (inventory role: DomainxFactory, medical) |
| 5 | `ledgerXfactory/LedgerxFactory` | `ba86f758b97f3a4fe0e38c86d10b152613e8c297` | single repository | no `project.yaml`, `family.yaml` or `single-repository.yaml` at the root; name form `project-leg/assembly` | **migrate** (`adopt-project.py`) — a product with code and specs (inventory role: DomainxFactory, accounting) |
| 6 | `opensoft/OpsxFactory` | `18623509c573ad2e297278e76a1d898510bb0bf5` | single repository | no `project.yaml`, `family.yaml` or `single-repository.yaml` at the root; name form `project-leg/assembly` | **migrate** (`adopt-project.py`) — a product with code and specs (inventory role: DomainxFactory, IT operations) |
| 7 | `opensoft/AdxFactory` | `e794dc2fc5094139f3eb2d3c78eff95d3bddaa99` | single repository | no `project.yaml`, `family.yaml` or `single-repository.yaml` at the root; name form `project-leg/assembly` | **migrate** (`adopt-project.py`) — a product with code and specs (inventory role: DomainxFactory, marketing) |
| 8 | `opensoft/MedxChart` | `9e05a88f3c944a2e9089c190a39ef2ba10632523` | single repository | no `project.yaml`, `family.yaml` or `single-repository.yaml` at the root; name form `project-leg/assembly` | **record staying single** (`single-repository.yaml`) — a composition boundary over `openChart`, which it mounts and pins (the inventory's header records both): the product it composes already has a repository of its own, where that product's shape question belongs |
| 9 | `opensoft/MedxPractice` | `f7fd8364e033df4a6c5b0f84080b7bde5d156fb4` | single repository | no `project.yaml`, `family.yaml` or `single-repository.yaml` at the root; name form `project-leg/assembly` | **record staying single** (`single-repository.yaml`) — a practice-operations boundary over `openPractice`, which it mounts and pins (the inventory's header records both): the product it composes already has a repository of its own, where that product's shape question belongs |
| 10 | `MedxSoft/MedxEHR` | `0e4a004438d0ce014904b6d047b769d877e06def` | Triad | `project.yaml`: `kind: project-manifest`, `schema: project-repo-schema`, `legs:` `spec` `MedxSoft/MedxEHR-spec` and `code` `MedxSoft/MedxEHR-code` | — elected; the advisory is silent here |
| 11 | `opensoft/HealthLinc` | `ce844c14f78b1147b0bfd3f5573f959229177f02` | single repository | no `project.yaml`, `family.yaml` or `single-repository.yaml` at the root; name form `project-leg/assembly` | **migrate** (`adopt-project.py`) — a product with code and specs (inventory role: Medx satellite); `MedxEHR`, the other Medx satellite, already elected the Triad |
| 12 | `opensoft/openXwallet` | `95669e98e4d707ccb9433114269924880cf54569` | single repository | no `project.yaml`, `family.yaml` or `single-repository.yaml` at the root; name form `neutral-product` | **migrate** (`adopt-project.py`) — a product with code and specs: the wallet standard's specification and contract corpus (`openspec/`, `specs/`, `contracts/`) beside its validators (`scripts/`, `tools/`, `tests/`); `openDox` and `openXdox`, neutral products pinned the same way, already elected |
| 13 | `opensoft/openDox` | `6a9f4902285029b4fb02753e2b79be0a137302c5` | Triad | `project.yaml`: `kind: project-manifest`, `schema: project-repo-schema`, `legs:` `spec` `opensoft/openDox-spec` and `code` `opensoft/openDox-code` | — elected; the advisory is silent here |
| 14 | `opensoft/openXdox` | `9564d5d9462ffd1a3155d9177206368e5061efa8` | Triad | `project.yaml`: `kind: project-manifest`, `schema: project-repo-schema`, `legs:` `spec` `opensoft/openXdox-spec` and `code` `opensoft/openXdox-code` | — elected; the advisory is silent here |
| 15 | `opensoft/openAvatar` | `31502eb26ad18e4cd5c861e6332f512a0da0387a` | single repository | no `project.yaml`, `family.yaml` or `single-repository.yaml` at the root; name form `neutral-product` | **migrate** (`adopt-project.py`) — a product with code and specs (inventory role: neutral product, avatar client) |
| 16 | `opensoft/openRepoShape` | `39d5c986fcfac1a160474bfe91c5f1c37fccc72c` | single repository | no `project.yaml`, `family.yaml` or `single-repository.yaml` at the root; name form `neutral-product` | **record staying single** (`single-repository.yaml`) — a tool: the shape's own scaffold, adopt and doctor tooling, which keeps no specification corpus at its root (no `openspec/`, no `specs/`) for a spec leg to carry, and which every elected project pins as one tree (`shape:` in its `project.yaml`, with `contracts/shape-pin.yaml`) |
| 17 | `opensoft/AgentTower` | `8a27d21613fc127681d4c5aa2c5b063618276545` | single repository | no `project.yaml`, `family.yaml` or `single-repository.yaml` at the root; name form `project-leg/assembly` | **migrate** (`adopt-project.py`) — a product with code and specs: `openspec/` and `specs/` beside `src/` and `tests/`; its name, unlike the `-Install` rows, is a valid assembly root |
| 18 | `opensoft/xFactory-Hermes-Install` | `763b61e1c60cde3c8a55019590580d3241106e0e` | single repository | no `project.yaml`, `family.yaml` or `single-repository.yaml` at the root; name form `install` | **record staying single** (`single-repository.yaml`) — its name is in the `install` form, which the naming policy admits into no role, so in-place adoption refuses it (note B) |
| 19 | `opensoft/Omnigent-Install` | `30c9e08270225b6dc20ee8a6477f157650c4a149` | single repository | no `project.yaml`, `family.yaml` or `single-repository.yaml` at the root; name form `install` | **record staying single** (`single-repository.yaml`) — its name is in the `install` form, which the naming policy admits into no role, so in-place adoption refuses it (note B) |
| 20 | `opensoft/OmniWorker-Install` | `125d9636d6fed5589d628b4f32d812c0968d7979` | single repository | no `project.yaml`, `family.yaml` or `single-repository.yaml` at the root; name form `install` | **record staying single** (`single-repository.yaml`) — its name is in the `install` form, which the naming policy admits into no role, so in-place adoption refuses it (note B) |
| 21 | `opensoft/CloudPC-Install` | `7a2b57745441c3089946235311b0a6748e351e56` | single repository | no `project.yaml`, `family.yaml` or `single-repository.yaml` at the root; name form `install` | **record staying single** (`single-repository.yaml`) — a configuration repository (inventory role: install, CloudPC); its name is in the `install` form, which the naming policy admits into no role, so in-place adoption refuses it (note B) |
| 22 | `opensoft/xFactory-Installer` | `4b3a14b954429166c6bb4c8144a24a58e8294dfd` | single repository | no `project.yaml`, `family.yaml` or `single-repository.yaml` at the root; name form `NO FAMILY` | **record staying single** (`single-repository.yaml`) — a tool (inventory role: install, workspace installer) whose hyphenated name matches no naming family (the naming policy lists it under `unclassified_examples`), so in-place adoption refuses it (note B) |
| 23 | `opensoft/xFactory-MedxRootTruth-Install` | `62ffdd2a6a4bbe4138726c1d04621d9646f50ee1` | single repository | no `project.yaml`, `family.yaml` or `single-repository.yaml` at the root; name form `install` | **record staying single** (`single-repository.yaml`) — its name is in the `install` form, which the naming policy admits into no role, so in-place adoption refuses it (note B) |
| 24 | `opensoft/Keycloak-Install` | `0f7228f35a61f499ab3f717ad887aa80968f179f` | single repository | no `project.yaml`, `family.yaml` or `single-repository.yaml` at the root; name form `install` | **record staying single** (`single-repository.yaml`) — a configuration repository (inventory role: install, Keycloak); its name is in the `install` form, which the naming policy admits into no role, so in-place adoption refuses it (note B) |
| 25 | `opensoft/OpenXPKI-Install` | `2469ce3d17b40099ea4f2c7e2a96dde4ebe1ca17` | single repository | no `project.yaml`, `family.yaml` or `single-repository.yaml` at the root; name form `install` | **record staying single** (`single-repository.yaml`) — a configuration repository (inventory role: install, OpenXPKI); its name is in the `install` form, which the naming policy admits into no role, so in-place adoption refuses it (note B) |
| 26 | `Fission-AI/OpenSpec` | `9111a7654d7800391459431fff4eaf66e33a3d2e` | single repository | no `project.yaml`, `family.yaml` or `single-repository.yaml` at the root; name form `project-leg/assembly` | **none made** — `governance: external`, a third-party CLI that this estate pins and authors none of; this record addresses no recommendation to a third party's owner |
| 27 | `opensoft/LedgerxWallet` | `0a0141cafc1fecd5d0e38b14e4f40a67a54a08d3` | single repository | no `project.yaml`, `family.yaml` or `single-repository.yaml` at the root; name form `project-leg/assembly` | **record staying single** (`single-repository.yaml`) — the Ledgerx overlay of `openXwallet` (inventory role; the naming policy's `example_chains` records `LedgerxWallet: [openXwallet, openWallet]`): the standard it overlays already has a repository of its own, where that standard's shape question belongs |
| 28 | `opensoft/openChart` | `aff1829cab68547437e725839afe9f702c5bea43` | single repository | no `project.yaml`, `family.yaml` or `single-repository.yaml` at the root; name form `neutral-product` | **migrate** (`adopt-project.py`) — a product with code and specs: `openspec/` and `specs/` beside `open_chart/` and `tests/` |
| 29 | `opensoft/openPractice` | `0ec9fca72ecf493e2520e676387f0c3f327cc6e6` | single repository | no `project.yaml`, `family.yaml` or `single-repository.yaml` at the root; name form `neutral-product` | **migrate** (`adopt-project.py`) — a product at specification only (`ideation/`, `openspec/`, no implementation yet): the doctrine makes the Triad the default for a new project, and adopting before any code lands moves the least (its empty code leg is seeded only on `--allow-empty-leg code`, a person's explicit act) |
| 30 | `opensoft/MedxAvatar` | `4ae4a71ca739050b0d1b74ca03975a3531309467` | single repository | no `project.yaml`, `family.yaml` or `single-repository.yaml` at the root; name form `project-leg/assembly` | **record staying single** (`single-repository.yaml`) — a configuration repository (inventory role: nested submodule of MedxSoft/MedxFactory), with no product of its own to split |
| 31 | `opensoft/LedgerxAvatar` | `c7bdd11b7748718630174a1d9bd844b5dea9d897` | single repository | no `project.yaml`, `family.yaml` or `single-repository.yaml` at the root; name form `project-leg/assembly` | **record staying single** (`single-repository.yaml`) — a configuration repository over `openAvatar`, which it mounts (the inventory's header records it), with no product of its own to split |
| 32 | `MedxSoft/MedxEHR-spec` | `7ea2583b69e3c118e29d98c4d0e644c412ec68d2` | leg | name form `project-leg/spec`; `AGENTS.md` opens as the spec leg; no `project.yaml` | — a leg of a Triad; the advisory is silent here |
| 33 | `MedxSoft/MedxEHR-code` | `2960743f3a138c800bb648da0ba04f3185ea1b05` | leg | name form `project-leg/code`; `AGENTS.md` opens as the code leg; no `project.yaml` | — a leg of a Triad; the advisory is silent here |
| 34 | `opensoft/openDox-spec` | `7db9438b4cc4446ab4e6ab5b552c220312deccc9` | leg | name form `project-leg/spec`; `AGENTS.md` opens as the spec leg; no `project.yaml` | — a leg of a Triad; the advisory is silent here |
| 35 | `opensoft/openDox-code` | `84f8ed8366ba1705305b48f962275c481faac882` | leg | name form `project-leg/code`; `AGENTS.md` opens as the code leg; no `project.yaml` | — a leg of a Triad; the advisory is silent here |
| 36 | `opensoft/openXdox-spec` | `f088b09732e236279898b53ab9fb0f5ebc89509a` | leg | name form `project-leg/spec`; `AGENTS.md` opens as the spec leg; no `project.yaml` | — a leg of a Triad; the advisory is silent here |
| 37 | `opensoft/openXdox-code` | `d45a0939c30ebbc2af60e16072ce4b3ae7205c3d` | leg | name form `project-leg/code`; `AGENTS.md` opens as the code leg; no `project.yaml` | — a leg of a Triad; the advisory is silent here |

## 3. Counts

| class | rows | repositories |
| --- | ---: | --- |
| Triad | 3 | `MedxSoft/MedxEHR`, `opensoft/openDox`, `opensoft/openXdox` |
| leg | 6 | `MedxSoft/MedxEHR-spec`, `MedxSoft/MedxEHR-code`, `opensoft/openDox-spec`, `opensoft/openDox-code`, `opensoft/openXdox-spec`, `opensoft/openXdox-code` |
| family holder | 0 | — |
| workspace repository | 0 | — |
| single repository | 28 | rows 1-9, 11, 12, 15-31 |
| **total** | **37** | |

**Records staying single: 0.** No row carries a `single-repository.yaml`.

**Recommendations, over the 28 single repositories:**

| recommendation | rows | repositories |
| --- | ---: | --- |
| migrate (`adopt-project.py`) | 12 | `openxFactory`, `codexFactory`, `MedxFactory`, `LedgerxFactory`, `OpsxFactory`, `AdxFactory`, `HealthLinc`, `openXwallet`, `openAvatar`, `AgentTower`, `openChart`, `openPractice` |
| record staying single (`single-repository.yaml`) | 15 | `xFactory`, `MedxChart`, `MedxPractice`, `openRepoShape`, `xFactory-Hermes-Install`, `Omnigent-Install`, `OmniWorker-Install`, `CloudPC-Install`, `xFactory-Installer`, `xFactory-MedxRootTruth-Install`, `Keycloak-Install`, `OpenXPKI-Install`, `LedgerxWallet`, `MedxAvatar`, `LedgerxAvatar` |
| none made | 1 | `OpenSpec` (`governance: external`) |

**The Triads agree with `design.md` D7.** D7 read the aggregation's local
checkouts and found three Triads: `openDox`, `openXdox` and `MedxEHR`. Read on
each repository's own `main`, those three are still the only Triads among the
inventory's 37 rows. The six legs are exactly the `spec` and `code` legs their
three `project.yaml` files name.

## 4. Notes that inform the recommendations

These notes are not classes.

**A. Noted kinds (OQ-2: noted, never guessed into a class).**

- Aggregation: `opensoft/xFactory`.
- Configuration repository: `CloudPC-Install`, `Keycloak-Install`,
  `OpenXPKI-Install`, `MedxAvatar`, `LedgerxAvatar`.
- Fork: none. GitHub reports `fork: false` for all 37 rows.

**B. Some names cannot be adopted in place.** `adopt-project.py` adopts a
repository IN PLACE. Its docstring records the ruling (Brett Heap, 2026-09-02)
that the adopted repository "KEEPS ITS NAME, ITS IDENTITY AND ITS FULL
HISTORY". Its `--project` argument is "the source repository's own name". It
checks that name against the naming policy, and two refusals apply here:

- `naming-role-mismatch` for the `install` form. Its remediation text reads "an
  `<X>-Install` may be no leg at all".
- `naming-unclassified` for a name that matches no family.

openRepoShape's validator at `39d5c986`, run over the 37 names, classifies
seven as `install`. They are rows 18-21 and 23-25. It classifies
`xFactory-Installer` (row 22) as `NO FAMILY`. For those eight, migrating would
first need a rename, which is a separate decision for the owner. Neither this
record nor the tool makes that decision, so the recommendation is to record
staying single. Nothing here stands against an owner who would rather rename
and then adopt.

**C. Acting on "record staying single" waits on `tasks.md` § 5.2.** OQ-1 was
ruled: the record is `single-repository.yaml` at the repository root, and its
schema belongs to openRepoShape. openRepoShape's `main` at `39d5c986` carries
neither that schema nor a template for it. Until § 5.2 lands, an owner who
takes this recommendation has nothing to write the record against. A
repository that records nothing owes nothing in the meantime.

**D. How each recommendation was chosen.** The doctrine makes the Triad "the
recommended migration target for an existing single-repository project". The
three outcomes follow from that:

- **Migrate** is recommended where the repository is a product with code and
  specs. `openPractice` is included as a product at specification only, where
  the doctrine's default for a new project applies.
- **Record staying single** is recommended in two cases. The first is where the
  repository is not such a product: an aggregation, a configuration repository,
  a tool, or a domain boundary or overlay whose product has a repository of its
  own. The second is where its name bars adoption in place (note B).
- **None** is made for the one `external` row, a third party's repository that
  this estate pins and authors none of.

## 5. Not measured

**None.** Every one of the 37 rows was read:

- `repos/{repo}` answered 200;
- the default branch was `main`;
- `commits/main` returned a head.

No row was skipped, and no class was inferred for a row that could not be read.

## 6. Re-running it

```sh
gh api repos/<owner>/<repo> --jq '.default_branch, .fork'
gh api repos/<owner>/<repo>/commits/main --jq .sha
gh api 'repos/<owner>/<repo>/contents/project.yaml?ref=<sha>'    # likewise family.yaml, single-repository.yaml, AGENTS.md
python3 scripts/validate-repository-naming.py <name> ...         # in an openRepoShape checkout at 39d5c986
```

A re-run on a later day reads later heads and belongs in a new dated record.
This one is a capture and is not edited (`Status: record`).
