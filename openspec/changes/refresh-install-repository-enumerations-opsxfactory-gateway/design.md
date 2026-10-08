# Design: refresh-install-repository-enumerations-opsxfactory-gateway

Status: draft
Kind: design
Lane: openxfactory-5 (openXfactory-5)

Seven decisions, **D1** through **D7**. Two of them put an open question to the
owner with a recommended answer (**D3**, **D4**), and each says what a different
ruling would change. Every figure below was read back from the repository or the
GitHub API on 2026-10-08, at openxFactory `main` `e83259b4` and opensoft/xFactory
`main` `651dd5c9`, not remembered. Brett Heap's word of 2026-10-08, *"Lane 5
indexes it now (Recommended)"*, admitted the work and chose the course; it
ratifies none of the text below.

## D0 — Convener brief

Eight lines, for the read that decides whether to ratify.

1. `opensoft/OpsxFactory-Gateway-Install` is mounted at
   `installs/opsxfactory-gateway-install` (opensoft/xFactory#567 → `651dd5c9`,
   gitlink `26f53c96`), and the promoted enumerations of install repositories name
   five repositories, not six.
2. **#1259 is the successor the index requirement asks an admitting change to name**,
   and the admitting change named it. This packet is the act it named.
3. **D1** measures every site in the three capabilities that names install
   repositories: five units are indexes and widen, one needs no edit, and the rest
   are not indexes.
4. **D2** measures the collision and there is none: no other active change writes
   any of the five requirement keys.
5. **D3 (OQ-2)**: no routing scenario for the gateway, because no requirement fixes
   what its repository owns and a scenario would confer that boundary through an
   index.
6. **D4 (OQ-1)**: the gateway joins `canonical-contract-migration`'s adapter trigger,
   recommended, as the family `Ops-gateway`; refusing it deletes one delta file.
7. **D5** leaves the index requirement's dated nine-against-five measurement alone and
   records today's, ten against six.
8. **D6**: the `## Purpose` widening cannot travel in a delta and is owed at the
   archive, with the sentence quoted.

## D1 — Which units widen: five, with one site needing no edit

The refresh's ratified method is kept: a unit widens when it is an INDEX of install
repositories, and a site that merely names one is left alone. Every site at `main`
`e83259b4` that names two or more of the five install repositories, or that lists
runtime adapter families, was found by script (the five names, case-sensitively,
across every promoted `spec.md`) and by reading the adapter bullet's neighbours:

| # | File : line | Unit as canon states it | Decision |
|---|---|---|---|
| 1 | `repo-boundary-governance:3-7` | `## Purpose` naming `openxFactory` and five installs | **Widens, as an OWED ARCHIVE ACT** (D6): a `## Purpose` in a delta is ignored on archive |
| 2 | `repo-boundary-governance:28` | *"Install repo needs policy context"* `WHEN` bullet, five names | **Widens** |
| 3 | `repo-boundary-governance:35-38` | *"Install repository scope"* list sentence, five names | **Widens** |
| 4 | `repo-boundary-governance:40-53` | the admission paragraph (Keycloak, OpenXPKI, OmniWorker records, the index sentence) | **Carried byte for byte; a paragraph is ADDED beside it** (D5) |
| 5 | `repo-boundary-governance:76` | *"Canonical policy exists in an install repo"* `WHEN` bullet, five names | **Widens** |
| 6 | `shared-contract-ownership:52` | *"Install repo consumes a contract"* `WHEN` bullet, five names | **Widens** |
| 7 | `shared-contract-ownership:88` | *"Submodule is proposed"* `WHEN` bullet, five names `or a later install repository` | **No edit**: the open tail covers it |
| 8 | `canonical-contract-migration:33` | *"Contract breaks an adapter"* `WHEN` bullet, five adapter families | **Widens, open question OQ-1** (D4) |
| — | `repo-boundary-governance:108-118` | *"Install repo scope links"*, per-repository README scenarios for Hermes and Omnigent | No: per-repository instances, not an index; the body is already general |
| — | `shared-contract-ownership:47`, `:91` | Gate G0 remote sentence; *"Hermes-Install remote is unresolved"* | No: one consumer's remote identity and one repository's condition |
| — | `canonical-contract-migration:5` | `## Purpose`, *"source repos (e.g. Omnigent-Install)"* | No: an `e.g.` list does not go stale |
| — | `repo-boundary-governance:120-141`, `:220-306` | *"Neutral installer repository integration"*; *"OmniWorker install repository boundary"* | No: each is one repository's own boundary |
| — | `repo-boundary-governance:309-` | the ADDED index requirement | No edit, and why: D5 |
| — | `contracts/README.md:18`, `docs/repo-boundary-pilot-plan.md:100` | an editorial release-inventory member; a dated pilot record | No: out of scope by class, as the refresh found |

**Row 7 is the one a reader will look for.** *"Submodule is proposed"* reads
*"… `OpenXPKI-Install`, `OmniWorker-Install`, or a later install repository as a
submodule"* at `shared-contract-ownership:88`. The archived refresh made it
open-ended on purpose (its D5): the scenario governs the act of ADMITTING a
repository, which by definition is not yet in any index, so a closed list would
exempt the next admission from the decision record. The gateway was exactly such a
repository on 2026-10-06 and is covered by the same tail now, as is the next one.
Naming it would close a list the refresh chose to leave open, so it is not named.

**The five widenings are list extensions and nothing else.** Canon's grammar and
order are kept, the sixth name is appended, and canon's own `or` (the list sentence
in row 3 has `and`) moves to stand before the last name, so the serial comma canon
already uses is preserved. The same movement was the edit to the `## Purpose` when
the fifth name was added. No widened unit adds a phrase canon does not use.

**What stays unindexed, and is not touched.** Of the TEN `installs/` mounts at
xFactory `main`, six are indexed after this packet. `agenttower`, `cloudpc-install`,
`medx-roottruth-install` and `xfactory-installer` stay unindexed, for the reasons the
archived refresh measured in its D1: no reviewed act placed them under these
enumerations. `cloudpc-install` is governed by another capability
(`workstation-intake`), `xfactory-installer` by its own requirement (*"Neutral installer
repository integration"*), and `agenttower` and `medx-roottruth-install` by neither.
The gateway differs from all four in the respect that matters: Brett Heap's word chose
to index it, and its admitting change named this packet.

**Rejected, so it is not re-litigated: record it as mounted but unindexed.** That is
what the refresh did for `cloudpc-install` and `medx-roottruth-install`, and it was
the second option put to the owner on 2026-10-08. It was not chosen. The facts also
cut against it here: an omission from an enumeration is an index defect under the
index requirement's own second scenario, and the admitting change named a successor
precisely so the repository would be indexed.

## D2 — The collision, measured: none

`release-realization`'s ordered-deltas rule binds a proposal that modifies a
requirement an active ratified change already modifies. Measured at `main`
`e83259b4` over every active change directory but this one (47):

1. **Delta files in the three capabilities.** Five active changes carry a
   `repo-boundary-governance` delta and each writes one requirement of the
   repository-boundary kind:

   | Active change | Requirement written |
   |---|---|
   | `add-identity-brokering` | `Keycloak install repository boundary` (ADDED) |
   | `add-trust-anchor` | `OpenXPKI install repository boundary` (ADDED) |
   | `implement-keycloak-install-repo` | `Keycloak install repository boundary` (MODIFIED) |
   | `implement-openxpki-install-repo` | `OpenXPKI install repository boundary` (MODIFIED) |
   | `qualify-avatar-live-voice` | `Neutral avatar-client repository boundary` (MODIFIED) |

   No active change carries a `shared-contract-ownership` or a
   `canonical-contract-migration` delta.
2. **The requirement titles themselves.** A script read every `### Requirement:`
   heading of every active change's `specs/*/spec.md` against the eight titles this
   packet writes or reasons about (the five it MODIFIES, *"Submodule sequencing"*,
   *"Install repo scope links"* and the index requirement). **Zero hits.**
3. **Prose.** Five active packets mention *"Install repository scope"* in prose.
   Four (`add-trust-anchor`, `add-identity-brokering`, `implement-keycloak-install-repo`,
   `implement-openxpki-install-repo`) record that the enumeration's refresh was
   executed elsewhere (2026-08-21, `admit-install-repos-to-aggregation`) or was decided
   against by them in favour of an ADDED per-repository requirement; none books a
   pending change to it. The fifth, `add-wallet-carried-review-authority`, cites it only
   to say it is not the template for a non-install repository's boundary.

So no requirement here is already modified by an active ratified change, the
ordered-deltas rule is not engaged, and there is no archive-time race. The check
is repeated at the pull request's head (`tasks.md` § 2.6).

**The ledger row reads `class: co-modifier` all the same, and that is not a
contradiction.** `class:` is boolean over every key a change writes and the ledger's
corpus is active PLUS archived, and the archived `refresh-install-repository-enumerations`
and `amend-repo-boundary-governance-scope-first-line` wrote the same keys. The row
seeded by `scripts/validate-sequenced-after.py . --seed-ledger --moved-by '#<PR>'`
reads `{state: active, class: co-modifier, declares:
[refresh-install-repository-enumerations,
amend-repo-boundary-governance-scope-first-line], depth: 2, prose: false}`, and
EXACTLY ONE row moves, this change's own. Which is why the packet DECLARES the
sequence: `refresh-install-repository-enumerations` wrote every list this packet
extends, and `amend-repo-boundary-governance-scope-first-line` wrote the form
*"Install repository scope"* now has, so these deltas ARE relative to their
outcome, and saying so is a positive, resolvable claim. The diff is the check: any
other row that moved would be a collision this design did not predict.

## D3 — OQ-2: no routing scenario for the gateway (recommended)

*"Install repository scope"* carries three routing scenarios, each of the form
*"WHEN a change installs, restores, backs up, upgrades, or verifies X runtime
behavior THEN the implementation detail MUST live in `X-Install`"*. The record of how
each came to exist:

| Repository | Scenario | Entered canon | Basis |
|---|---|---|---|
| `Hermes-Install` | yes | 2026-06-26, `7c4dacb9` | the capability's creation |
| `Omnigent-Install` | yes | 2026-06-26, `7c4dacb9` | the capability's creation |
| `OmniWorker-Install` | yes | 2026-09-08, `ca4a1558` (the refresh's archive) | its own boundary requirement, promoted 2026-09-08, fixes "the worker-host product" |
| `Keycloak-Install`, `OpenXPKI-Install` | **none** | — | each has its own boundary requirement and the list names it without a scenario |

**A routing scenario is a further obligation about WHERE procedures live, and it
presupposes that something fixes WHAT the repository is.** For the gateway nothing
does. Measured at xFactory `main`, no `repo-boundary-governance` requirement names
`OpsxFactory-Gateway-Install` (the aggregation's own admission record says so in
terms), and the repository's README says *"Once admitted (task 2.4 (a)), the
gateway's runtime and install material. The admitting change says exactly what that
is; nothing is authored here before it."* with *"gateway_realization: HELD"*. A
scenario saying gateway runtime procedures MUST live there would settle that
question through an index. The index requirement says the opposite is the rule:
*"the enumeration indexes them and does not confer them"*.

**What listing the repository DOES say**, stated so a reader does not mistake the
absence for a gap: the list sentence applies one scope to every name in it. The
gateway is scoped to install, operations, backup, restore, upgrade, verification and
disaster recovery, as each of the five is. The listing says that and nothing about
what the gateway is.

**What a different ruling would change.** If the owner wants the scenario, ONE
scenario is added to the *"Install repository scope"* block, after the three it
carries, and nothing else in the packet moves:

```
#### Scenario: Gateway runtime procedure is changed
- **WHEN** a change installs, restores, backs up, upgrades, or verifies task-bound gateway runtime behavior
- **THEN** the implementation detail MUST live in `OpsxFactory-Gateway-Install`
```

The recommendation is the answer that leaves the next, still-open question (what the
gateway's repository owns) with the act that should answer it.

## D4 — OQ-1: the gateway joins "Contract breaks an adapter" (recommended)

The bullet reads *"WHEN a contract change would break Hermes, Omnigent, Keycloak,
OpenXPKI, or worker-host runtime adapters"*. It lists adapter FAMILIES, not
repositories, and the archived refresh widened it because five install repositories
held adapters over `openxFactory` contracts while it named two.

**The facts do not settle this on their own.** For joining: the gateway is an
admitted install repository, and under the index requirement's second scenario an
admitted repository missing from an enumeration is an index defect, repaired
wherever it is found. Against joining: the repository holds no adapter today. Its
README reads `implementation_status: repository-seed. No runtime and no manifests`,
the admission record counts 105 tracked files with no runtime source, and the
gateway's realization is HELD.

**Why the recommendation is to join:**

1. **The trigger is conditional.** It reads *"WHEN a contract change would break
   …"*. Listing a family binds nothing until an adapter of that family exists, so the
   absence of an adapter today is no reason to leave the family out.
2. **The obligation exists either way.** *"Contract changes incompatibly"* in
   `shared-contract-ownership` requires a shared contract change that would break
   *"an install repo adapter or smoke test"* to be split from the adapter migration
   or explicitly approved as breaking. That reaches the gateway's adapter whether or
   not this bullet names it, so the choice moves one sentence's completeness and no
   obligation.
3. **Cost.** Joining costs one word and one delta file. Not joining leaves the
   enumeration known to be short by one and needs a later refresh when the first
   adapter exists.
4. **What the gateway will work against** is already stated by the repository: its
   README's ownership table names `openxFactory`'s neutral MCP conformance
   declaration (`factory-mcp-conformance`) and `xFactory-Hermes-Install`'s
   wallet-exercise verification as the contracts it serves under and consumes.

**The name.** The adapter family is `Ops-gateway`, hyphenated as `worker-host` is, and
named for what the repository runs in the Ops domain rather than for the repository.
The alternatives are `gateway` alone, which is ambiguous in a neutral capability, and
a longer `Ops task-bound-gateway`, which names a design still under HOLD. A different
name changes one word in one delta and nothing else.

**What a different ruling would change.** Refusing OQ-1 deletes
`specs/canonical-contract-migration/spec.md`. Nothing in the other two deltas depends
on it, and `canonical-contract-migration` is then left untouched, one adapter family
short, with its omission recorded here as a deliberate decision rather than a miss.

## D5 — The admission paragraph, and the index requirement left alone

**The paragraph.** The existing admission paragraph in *"Install repository scope"*
records the Keycloak and OpenXPKI admissions, the OmniWorker admission, and ends with
the index sentence. The gateway's own record is added as a SEPARATE paragraph after
it, so the existing paragraph is carried byte for byte instead of being re-wrapped
around an insertion. The paragraph states, and only states:

- the path `installs/opsxfactory-gateway-install` and the remote
  `opensoft/OpsxFactory-Gateway-Install`;
- the date, 2026-10-06, and the admitting change, opensoft/xFactory#567, by merge
  commit `651dd5c9450646a1d6e4a55ef04ddc5d53823cb4`, with the pinned commit
  `26f53c96965336819ac3d852db935e89ea7ec143`;
- that the change recorded the eight admission fields (path, remote, visibility,
  exact validated commit, checkout, compatibility, update, rollback) and is distinct
  from the repository's creation, which the capability requires: *"repository
  creation SHALL NOT be treated as aggregation admission"*;
- that the change named opensoft/openxFactory#1259 as the successor that refreshes
  the enumeration, as the index requirement asks of an admitting change.

It makes no claim about what the repository owns, which is D3's point, and no claim
that the repository has a boundary requirement. A sentence saying it has none would
be true today and false the day one is added, which is the maintenance burden the
index requirement exists to remove; that fact is recorded here, where staleness is
harmless, and not in canon.

**The index requirement is not edited.** *"Install-repository enumerations are an
index with a named authority"* carries a measurement, *"Measured on 2026-09-08, the
aggregation mounts NINE paths under `installs/` … while the install repositories
this capability's 'Install repository scope' requirement indexes number FIVE"*, and a
scenario repeating it, dated the same day. Both are dated measurements and remain
true as such. Re-measured on 2026-10-08, the aggregation mounts TEN paths
(the nine, plus `opsxfactory-gateway-install`) and, after this packet, the enumeration
indexes SIX. The surplus is the same four repositories, so the requirement's argument
(the two sets are different sets, and a derivation needs a declared filter) holds
unchanged. Editing a dated measurement to a newer date is a ratified-text edit with no
obligation behind it, and the requirement already says *"the measurement is the reason,
not the rule"*.

**The index requirement worked as written.** Its first scenario requires a change that
records the admission of a further install repository either to refresh every
enumeration or to name the issue or packet that will, as a citation. opensoft/xFactory#567
named #1259, and this packet is what #1259 names. That is recorded here as evidence the
rule is satisfiable, not as a new rule.

## D6 — The `## Purpose` widening is OWED at the archive, not carried in a delta

`repo-boundary-governance`'s `## Purpose` is the one enumeration this packet cannot
carry in a delta. A `## Purpose` in a change's spec delta is read only when the
capability is created and is ignored on any later archive, so a packet that put one
in a delta would validate, archive, and change nothing. The archived deltas that carry a
`## Purpose` are measured at `main` `e83259b4`: exactly two, and each CREATED its
capability (`repromote-engineering-vocabulary` → `openxfactory-engineering-adapter`,
2026-09-18, and `add-factory-mcp-conformance` → `factory-mcp-conformance`, 2026-10-06).
None has widened an existing capability's Purpose through a delta. The landed authority
for taking such a widening at the archive is the archived
`refresh-install-repository-enumerations` § 4.1 (and
`publish-openspec-cli-pin-as-contract-member` § 5.8, `d712ce29`).

`tasks.md` § 4.1 therefore books it, as one sentence appended in a hunk of its own in
the archive commit, after the promotion. Promoted, the `## Purpose` reads:

> Defines how `openxFactory`, `Hermes-Install`, `Omnigent-Install`,
> `Keycloak-Install`, `OpenXPKI-Install`, `OmniWorker-Install`, and
> `OpsxFactory-Gateway-Install` assign canonical workflow policy ownership,
> install repository scope, copy-first migration rules, and guarded
> repo-boundary execution.

The edit is the same two things the archived refresh's § 4.1 made: a sixth name
appended to the list, and canon's own `and` standing before the last name with the
serial comma kept. Every other word of the sentence is canon's. Nothing else in the
Purpose block is touched, no promoted requirement's text is edited by it, and no
`Removed from canon` marker is owed, a Purpose carrying no `SHALL` and not being a
canon unit. This packet does not edit `openspec/specs/` now, for the reason the
archived refresh gave: doing it before ratification would be an unratified edit with
a different author.

## D7 — No generator, no checker

The archived refresh refused to derive the enumerations from the aggregation's mount
list (its D1) and built no checker for the index rule (its D4), on a measurement that
the two sets differ and a checker would have to encode the filter nobody has ruled.
D5 re-measures the same fact. This packet builds none either, and changes no script,
workflow or test, which is what `code_surface: none` states.
