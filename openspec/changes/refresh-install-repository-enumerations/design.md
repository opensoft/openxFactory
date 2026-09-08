# Design: refresh-install-repository-enumerations

Status: draft
Lane: openxfactory-3 (openXfactory-3)

Six decisions, **D1** through **D6**. D1 is the one #796 asked for and the one
most worth a veto; D2 is the measurement that made D1 answerable at all. Every
figure below was read back from the repository or the GitHub API on 2026-09-08
at `main` `131adf11`, not remembered.

## D0 — Convener brief

Eight lines, for the read that decides whether to ratify.

1. A fifth install repository (`OmniWorker-Install`) exists, is mounted at
   `installs/omniworker-install`, and has a promoted boundary requirement.
   Four hand-written enumerations still describe an estate of two or four.
2. #796 offered two options: WIDEN the enumerations, or STOP enumerating and
   derive the list from the aggregation's `.gitmodules`.
3. **D1 recommends WIDEN**, because the two sets are not the same set: the
   aggregation mounts **nine** paths under `installs/` against an indexed set
   of **five**.
4. **D2 measured the collision #796 said to check for, and it does not
   exist.** Neither active packet writes *"Install repository scope"*; both are
   `class: co-modifier` for an unrelated reason.
5. So the widening can happen now. The ledger row still reads
   `class: co-modifier` — the ledger's corpus includes ARCHIVED changes and
   `admit-install-repos-to-aggregation` wrote the same key in August — which is
   why the packet DECLARES `sequenced_after: [admit-install-repos-to-aggregation]`
   rather than claiming there is nothing to sequence behind. `co-modifier` is a
   fact about history; the absence of a live collision is the separate fact D2
   measures.
6. Scope is SIX `## MODIFIED` requirements. Only **TWO** of the widened units
   are absent from #796's list (**D3**); one more is its item 2 under a
   CORRECTED reading, and the rest are its items 1 and 3. Every unit is
   measured and every one sits inside a capability the issue names.
7. ONE `## ADDED` requirement makes the index rule explicit so the sixth
   repository is a one-line edit (**D4**). **No generator is built** — that is
   the whole content of D1's refusal.
8. The `## Purpose` widening cannot travel in a delta and is booked as an
   owed archive act (**D6**), on a precedent eight days old.

## D1 — Widen the enumerations now, and state the index rule — NOT derive them

**RECOMMENDED. This is the veto point.**

#796 put the choice in one sentence: *"consider whether the right fix is to
widen the enumerations or to stop enumerating — a derived list (from the
aggregation `.gitmodules`, which OpsxFactory's
`code_surface_repository_registry` already re-derives) does not go stale on the
sixth repository."*

The derived option is attractive and it is wrong, for one measured reason:
**the aggregation's `installs/` mount list and the set these enumerations index
are DIFFERENT SETS.** Read back from `opensoft/xFactory`'s `.gitmodules` on
2026-09-08 — nine mounts:

| `installs/` mount | Remote | In the indexed set? |
|---|---|---|
| `agenttower` | `opensoft/AgentTower` | **No** — the string appears NOWHERE in `repo-boundary-governance`; it is named in `project-repo-schema` instead, so it is governed ELSEWHERE rather than ungoverned |
| `cloudpc-install` | `opensoft/CloudPC-Install` | **No** — likewise absent from this capability and named in `workstation-intake` instead, though it IS a named consumer in the OmniWorker split |
| `hermes-install` | `opensoft/xFactory-Hermes-Install` | Yes |
| `keycloak-install` | `opensoft/Keycloak-Install` | Yes |
| `medx-roottruth-install` | `opensoft/xFactory-MedxRootTruth-Install` | **No** — a Medx satellite install; the string appears in NO promoted specification at all |
| `omnigent-install` | `opensoft/Omnigent-Install` | Yes |
| `omniworker-install` | `opensoft/OmniWorker-Install` | Yes |
| `openxpki-install` | `opensoft/OpenXPKI-Install` | Yes |
| `xfactory-installer` | `opensoft/xFactory-Installer` | **No, and worse than absent** — it has its OWN requirement, *"Neutral installer repository integration"* |

A derivation over that group would do three separate wrong things. It would
enrol `AgentTower`, `CloudPC-Install` and `xFactory-MedxRootTruth-Install` into
a requirement no reviewed act placed them under — a silent widening of scope by
a script, which is the exact opposite of how every other boundary in this
capability was established, and two of the three are already governed by a
DIFFERENT capability whose scope a derivation here would silently overlap. It
would put `xFactory-Installer` under TWO requirements at once, one of which
fixes its scope differently (measured: `installs/xfactory-installer` and
`opensoft/xFactory-Installer` appear in `repo-boundary-governance` at its own
*"Neutral installer repository integration"* requirement). And it would
make the enumeration's contents depend on a file in ANOTHER repository at read
time, so `openxFactory`'s canon would say different things at different
aggregation commits with no reviewed act in between.

**The corpus has already counted this set and drawn the same line.**
`split-openxwallet-repo`'s design D11, quoted verbatim in
`scripts/sync-notebooklm-books.py`, keeps an explicit two-member allowlist
rather than reading the aggregation's pins precisely so as not to *"enrol the
nine `installs/*` runtime repositories as governed ideation repositories"*, and
the projection doc states its scope as skipping `installs/` outright. Nine is
the same nine.

**What the derived option gets right is kept anyway, as a requirement rather
than a script.** The complaint behind it is real: an index goes stale silently
and nobody notices. This one went THREE repositories and 74 days behind — the
`## Purpose` has not moved since `9ebceeff` (2026-06-26) while the capability
grew from two governed install repositories to five. D4's ADDED
requirement fixes that by naming the AUTHORITY the index answers to and by
requiring the next admission to refresh the index or name its successor — so
the failure mode becomes a missing citation, which this corpus already knows
how to catch, instead of a quiet omission.

**Rejected alternatives, stated so they are not re-litigated:**

- **D1-b, derive from `.gitmodules`.** Refused above. If it is ever wanted, the
  ADDED requirement's third scenario says what it would owe: a declared filter
  and the test that selects mounts. It is not foreclosed.
- **D1-c, derive from OpsxFactory's `code_surface_repository_registry`.**
  Refused on ownership, not on quality. That registry is a DomainxFactory
  artifact and its `aggregation_submodule` arm re-derives entries against the
  aggregation's `.gitmodules` — the same nine-member source, with the same
  filter problem, one repository further away. A neutral `openxFactory`
  requirement whose content is read from OpsxFactory inverts rule 1 of the
  workspace contract (domain repos never author neutral contracts).
- **D1-d, defer again.** `add-trust-anchor` § 8.1 booked the refresh as an
  owed task gated on two preconditions — both install repositories exist, and
  *"nothing else is replacing that requirement"*;
  `implement-keycloak-install-repo` declined to take it;
  `admit-install-repos-to-aggregation` discharged § 8.1 for two of four
  repositories and left the `## Purpose` behind; and
  `implement-omniworker-install-repo` deferred the next round to #796. **The
  precedent for taking it is therefore the SAME MEASUREMENT this design makes,
  by the same method:** § 8.1's tick records that *"the four active
  `repo-boundary-governance` deltas name only the two boundary requirements"* —
  a grep of the active deltas' requirement titles, which is D2 done in August
  with a smaller corpus. Both of § 8.1's preconditions hold again today, and
  D2 is the verification.

## D2 — The collision #796 said to check for, measured: it does not exist

#796 is explicit: *"`implement-keycloak-install-repo` and
`implement-openxpki-install-repo` are STILL ACTIVE in this repository (measured
2026-09-08 at main `9581ed9b`), so a change that MODIFIES 'Install repository
scope' may collide with whichever of them archives first. Check the sweep
ledger's `class:` for that requirement key before authoring."*

Checked, three ways, at `main` `131adf11`.

**1. What the two active packets actually write.** Each carries ONE spec delta
file and ONE `## MODIFIED` requirement, and neither names *"Install repository
scope"*:

| Active change | Delta file | Requirement written |
|---|---|---|
| `implement-keycloak-install-repo` | `specs/repo-boundary-governance/spec.md` | `### Requirement: Keycloak install repository boundary` |
| `implement-openxpki-install-repo` | `specs/repo-boundary-governance/spec.md` | `### Requirement: OpenXPKI install repository boundary` |

**2. Who writes *"Install repository scope"* anywhere in the corpus.** A grep
for `### Requirement: Install repository scope` across all 41 active and 144
archived change directories returns exactly two hits, both ARCHIVED:
`2026-06-26-restructure-factory-repo-boundaries` (which created it) and
`2026-08-25-admit-install-repos-to-aggregation` (which widened it to four). **No
active change writes that key at all.**

**3. Why the ledger nevertheless says `co-modifier`, which is the trap.** The
sweep ledger rows read:

```yaml
implement-keycloak-install-repo: {state: active, class: co-modifier, declares: absent, prose: false, moved_by: "#623", moved_on: "2026-09-03"}
implement-openxpki-install-repo: {state: active, class: co-modifier, declares: absent, prose: false, moved_by: "#623", moved_on: "2026-09-03"}
```

`class:` is BOOLEAN over every key a change writes, as the ledger's own header
says — *"whether ANY requirement key this change writes … is also written by
another change in the corpus"*. It does not say WHICH key. Both rows are
`co-modifier` because each shares its OWN sibling boundary requirement with an
active partner: `add-identity-brokering` `## ADDED` *"Keycloak install
repository boundary"*, and `add-trust-anchor` `## ADDED` *"OpenXPKI install
repository boundary"*. Reading the `co-modifier` flag as being ABOUT the
enumeration is the mistake this design exists to avoid making a fourth time.

**Consequence for this packet.** Grepping all 41 other active change
directories for each of the SEVEN requirement titles this packet writes — the
six it MODIFIES plus the one it ADDS — returns ZERO hits. So no requirement
here is *"already modified by an active RATIFIED change"*,
`release-realization`'s ordered-deltas rule is not engaged, and there is no
archive-time race with either packet #796 named.

**AND THE LEDGER ROW IS `co-modifier` ANYWAY, WHICH IS NOT A CONTRADICTION —
IT IS THE SAME TRAP READ THE OTHER WAY ROUND.** The ledger's corpus is active
PLUS archived (*"also written by another change in the corpus"*), and
`2026-08-25-admit-install-repos-to-aggregation` — archived — writes *"Install
repository scope"*. Measured by seeding the row:

```yaml
refresh-install-repository-enumerations: {state: active, class: co-modifier, declares: [admit-install-repos-to-aggregation], depth: 1, prose: false, moved_by: "#<PR>", moved_on: "2026-09-08"}
```

So `class:` says *"somebody else has written one of these keys"*, which is
TRUE and is a statement about history; it does NOT say *"a live change will
collide with you at archive time"*, which is what a reader looking for a
collision wants and is FALSE here. Exactly one row moves — this change's own —
and `admit-install-repos-to-aggregation`'s row does not flip, because it was
already `co-modifier`.

**Which is why this packet DECLARES the sequence rather than leaving it
absent**: `sequenced_after: [admit-install-repos-to-aggregation]`, resolving at
depth 1. That change wrote the four-name enumeration this one widens, so this
packet's deltas ARE relative to its outcome and saying so is a positive,
resolvable claim about ordering rather than a silence a later reader has to
reconstruct. `scripts/validate-sequenced-after.py . --seed-ledger --moved-by '#<PR>'`
writes the row and its diff is the check: any OTHER row that moves is a
collision this design did not predict.

**What DOES still collide, and is therefore left alone.**
*"Install repo scope links"* carries per-repository README scenarios for
`Hermes-Install` and `Omnigent-Install`. The equivalent obligation for
`Keycloak-Install` and `OpenXPKI-Install` is inside the two active packets'
boundary requirements. Widening that requirement here is the one edit in this
capability that would genuinely race them, so it is out of scope — see
`proposal.md` § *What it does NOT change*, item 3. #796's warning was sound
about the capability; it was aimed one requirement to the left.

## D3 — Scope: SIX MODIFIED requirements — the two extra units, and one corrected reading, are measured

**RECOMMENDED. Second veto point.**

#796's list is four enumerations. Measured against `main`, the same defect
class appears at SIX units in the three capabilities, and the fourth item on
the issue's list (the `## Purpose`) is not a requirement at all. The full
measurement, so the scope is auditable rather than asserted:

| # | File : line | Text as canon states it | In scope? |
|---|---|---|---|
| 1 | `repo-boundary-governance:32` | body: *"`Hermes-Install`, `Omnigent-Install`, `Keycloak-Install`, and `OpenXPKI-Install` SHALL be scoped to…"* | **Yes** — #796 item 3 |
| 2 | `repo-boundary-governance:27` | bullet: *"WHEN `Hermes-Install` or `Omnigent-Install` needs to implement a factory policy"* | **Yes** — same class, same capability, not on the issue's list |
| 3 | `repo-boundary-governance:62` | bullet: *"WHEN policy currently lives in `Hermes-Install` or `Omnigent-Install`"* | **Yes** — same |
| 4 | `shared-contract-ownership:50` | bullet: *"WHEN `Hermes-Install` or `Omnigent-Install` consumes a shared contract"* | **Yes** — #796 item 1 |
| 5 | `shared-contract-ownership:84` | bullet: *"WHEN a change proposes adding `Hermes-Install` or `Omnigent-Install` as a submodule"* | **Yes** — #796 item 1, second site |
| 6 | `canonical-contract-migration:31` | bullet: *"WHEN a contract change would break Hermes or Omnigent runtime adapters"* | **Yes** — #796 item 2, corrected: see below |
| 7 | `repo-boundary-governance:4` | `## Purpose` naming three repositories | **Yes, but as an OWED ARCHIVE ACT** — #796 item 4, and D6 |
| — | `shared-contract-ownership:46` | Gate G0 receipt requiring `opensoft/xFactory-Hermes-Install` | No — one consumer's remote-identity rule |
| — | `shared-contract-ownership:88` | *"Hermes-Install remote is unresolved"* | No — one repository's condition |
| — | `repo-boundary-governance:92`+ | *"Install repo scope links"* scenarios | No — D2's real collision |
| — | `canonical-contract-migration:5` | `## Purpose`, *"source repos (e.g. Omnigent-Install)"* | No — an `e.g.` list does not go stale |
| — | `contracts/README.md:18` | *"Hermes-Install and Omnigent-Install"* | No — release-inventory editorial member |
| — | `docs/repo-boundary-pilot-plan.md:100` | pilot acceptance criteria | No — a dated historical record |

**#796's item 2 is misdescribed and the correction is part of this design.**
The issue says `canonical-contract-migration` *"names `Hermes-Install` and
`Omnigent-Install` by hand — likewise"*. It does not. Measured: that
capability names `Hermes-Install` NOWHERE; it names `Omnigent-Install` exactly
once, inside a hedged `e.g.` in its `## Purpose`; and the one unit a fifth
install repository made incomplete is the *"Contract breaks an adapter"*
bullet, which enumerates two RUNTIME ADAPTER FAMILIES rather than two
repositories. That bullet is in scope because five install repositories now
hold adapters over `openxFactory` contracts and the trigger names two. The
`## Purpose` there is out of scope because `e.g.` already says the list is
open. Stating this rather than quietly widening whatever was nearest is what
lets a reviewer check the claim.

**EXACTLY TWO UNITS ARE ABSENT FROM #796's LIST, and the count is derived from
the table above rather than asserted.** They are rows 2 and 3 — the
*"Canonical workflow authority"* and *"Copy-first migration"* `WHEN` bullets in
`repo-boundary-governance`. Row 5 is #796's item 1 at its second site (the
issue names the capability, not one line in it); row 6 is #796's item 2 under
the corrected reading; rows 1 and 7 are its items 3 and 4.

**Why those two are in scope rather than a second issue.** The issue's own
2026-09-08 addendum makes the argument: `admit-install-repos-to-aggregation`
widened the requirement, left the `## Purpose`, and the Purpose went three
repositories behind. A packet whose stated purpose is *"the enumerations are
stale"* that widens one bullet in a requirement and leaves the bullet two
requirements below it reproduces that failure inside its own diff. Each of the
two is a single `WHEN` line in a requirement this packet must restate in full
anyway, so the marginal review cost is two lines and the marginal risk is zero.

**Veto shape, stated exactly.** Refusing D3 means dropping **rows 2 and 3**
from the table — those two MODIFIED blocks in the `repo-boundary-governance`
delta — and keeping 1, 4, 5, 6 and 7, which is #796's list. **Row 6 is NOT
part of this veto**: the `canonical-contract-migration` widening IS #796's item
2, so refusing the extra scope leaves that delta standing. The packet is
coherent either way; the deltas are per-requirement blocks and two of them can
be deleted without touching the rest.

## D4 — One ADDED requirement, no generator

The ADDED requirement *"Install-repository enumerations are an index with a
named authority"* does three things and deliberately not a fourth.

- **It fixes the READING.** An enumeration is an index; the authority for
  existence is the aggregation's `installs/` mount list; the authority for
  scope is each repository's own boundary requirement; an omission is an index
  defect and changes no repository's obligations. This is the sentence
  `admit-install-repos-to-aggregation` already wrote inside *"Install
  repository scope"* (*"This enumeration is an index of admitted install
  repositories; it neither widens nor narrows the scope…"*), lifted to a
  requirement of its own so it covers the other capabilities' lists too.
- **It fixes the MAINTENANCE.** The next admitting change either refreshes
  every enumeration or names the successor, and the naming must be a citation.
  This is the `owed-successor-tick-on-the-recording` doctrine applied to an
  index, and it is what #796 itself did well: the box ticked on a named issue.
- **It records the NINE-AGAINST-FIVE measurement in canon**, with the date, so
  the derivation question is answerable by reading the requirement instead of
  re-deriving the argument. A future change may still derive — the third
  scenario says what it owes.
- **It does NOT build a checker.** No script greps the specs against
  `.gitmodules`, and none is proposed. A rule and its checker landing in one
  act is how this estate has repeatedly shipped a rule the checker's shape
  quietly narrowed; and here the checker would have to encode the very filter
  D1 refuses to guess. If a checker is ever wanted, its input is the ADDED
  requirement's declared-filter obligation, not the mount list.

## D5 — One widening is open-ended, and only one

**Third veto point.** *"Submodule sequencing"*'s scenario is *"Submodule is
proposed"* — it governs the act of ADMITTING a repository as a submodule. A
repository being admitted is by definition not yet in any index, so a closed
five-name trigger there would exempt the sixth admission from the decision
record the scenario exists to require, which is the reverse of this packet's
purpose. It reads *"an install repository — `Hermes-Install`,
`Omnigent-Install`, `Keycloak-Install`, `OpenXPKI-Install`, `OmniWorker-Install`
or a later one — as a submodule"*, and its marker says why in the same words.

Every other widening is a CLOSED five-name list, on purpose. The five names are
the reviewed facts; *"any install repository"* in a scope or ownership
requirement would be a standing grant to a repository nobody has reviewed, and
D1's whole argument is that the set is not derivable.

## D6 — The `## Purpose` widening is OWED, not delta-carried

`repo-boundary-governance`'s `## Purpose` is the fourth enumeration and the
only one this packet cannot carry in a delta.

**The rule, and it is promoted-adjacent rather than assumed.**
`prepare-openspec-1.12-readiness`'s `document-lifecycle` delta states it in
terms — a `## Purpose` in a change's spec delta *"is read ONLY when the
capability is created; on any later archive it is ignored"*, so *"an author who
follows the corpus's ordinary reflex … produces a packet that validates, that
archives, and that changes nothing"*. That change is ACTIVE, so it is cited as
reasoning rather than as canon. The LANDED authority is the act itself:
`publish-openspec-cli-pin-as-contract-member` (archived 2026-09-08,
`d712ce29`) declared a `neutral-product-pin` Purpose widening owed in its own
ratified `tasks.md` § 5.8 and TOOK it in the archive commit, *"as ONE SENTENCE
… IN A HUNK SEPARATE FROM THE PROMOTION"*, after `proposal-support.py …
archive` had written the deltas into canon. Confirmed mechanically here: a grep
for `^## Purpose` across every archived change's `specs/*/spec.md` returns
NOTHING, so no packet in this corpus has ever shipped a Purpose through a
delta.

**So `tasks.md` § 4.1 books it**: one sentence appended to the Purpose naming
all five install repositories, taken in the archive commit, in a hunk of its
own, with the sentence quoted in the tick so the edit is on the record and not
only in a diff. Nothing else in the Purpose block is touched, no requirement
text is edited by it, and no `Removed from canon by` marker is owed — a Purpose
carries no SHALL and is not a canon unit.

**What this packet does NOT do about the Purpose.** It does not edit
`openspec/specs/repo-boundary-governance/spec.md` now. #803 declined exactly
that edit for exactly the right reason — no owed act in its ratified packet —
and doing it here before ratification would be the same unratified edit with a
different author.
