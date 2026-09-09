---
code_surface: none — this packet's whole diff is governance text in openxFactory: the `## Purpose` block of 39 main specs under `openspec/specs/`, one missing group header plus a dated note in `openspec/changes/add-doxchat-model-intake/tasks.md`, four dated ordering notes in four other active changes' `tasks.md`, this packet's own five files, one README records row and one `tests/sequenced_after/corpus-ledger.yaml` row. NO contract is added or changed: `contracts/manifest.yaml` is untouched, no digest inventory moves, no `contracts/CHANGELOG.md` line is owed and no release tag is owed. NO validator, workflow, test or script changes — in particular `contracts/openspec-cli-pin.yaml` and `scripts/validate-openspec-cli-pin.py` are NOT TOUCHED, which is the point: the pin stays at `1.2.0` and this packet is what a later bump will cite, not the bump itself. No EXISTING requirement text, scenario, or lifecycle status anywhere is altered; a `## Purpose` is prose ABOUT a capability and carries no SHALL. The packet carries ONE `## ADDED Requirements` delta on `document-lifecycle`, written because strict validation REFUSES a change with no delta (`1.2.0`: *"Change must have at least one delta"*) and because the rule it states is the one this packet had to learn to do the work at all — that the archive act's placeholder Purpose can only be repaired in the promoted specification, a delta's `## Purpose` being read solely at capability creation.
target_release: implemented (the openxFactory main line; doc-only, so realization is the merge itself and no contract bundle is cut). The archive gate is merged-plus-green under `release-realization`, PLUS the disposition of the two recorded REFUSALS in § The two it does not fix — a packet that claims "1.12-ready" while two changes still fail must not archive on a silence.
Status: draft
---

# Proposal: prepare-openspec-1-12-readiness

Status: draft
Proposed: 2026-09-05
Origin: Operator instruction, Brett Heap, 2026-09-05, in session, verbatim:
*"start the 1.12 upgrade fixes"*. **That instruction ADMITTED this packet to
the queue and did not ratify its content.** In particular it did not settle
the two refusals recorded below, which are presented as the readings most
worth a veto.

**THIS PACKET BUMPS NOTHING.** `contracts/openspec-cli-pin.yaml` stays at
`@fission-ai/openspec@1.2.0` (#667) and is not in this diff. The bump is a
separate, later, human-ratified change that must land its own target-version
evidence. What this packet buys that change is a tree the successor tool
already accepts.

## Why

**The tool that decides what canon is has been pinned, and the corpus has
never been measured against the tool it will be pinned to next.**

`openspec validate --strict` is the gate every spec delta passes and
`openspec archive` is the act that writes a ratified delta into canon. #667
pinned that tool at `1.2.0` and made `scripts/validate-openspec-cli-pin.py`
the one entrypoint through which strict validation runs. Under that
entrypoint this corpus reads, on main `26d0a43d`:

```
Totals: 89 passed, 0 failed (89 items)
OK openspec-cli-pin: @fission-ai/openspec@1.2.0 verified against its content
address and every target validated --strict clean
```

Run the SAME TREE under `1.12.0`:

```
Totals: 47 passed, 42 failed (89 items)
```

**Not one of those 42 is a defect the pinned tool can see, and not one was
introduced by any lane.** 1.12.0 carries checks 1.2.0 does not:

- a **placeholder-`## Purpose`** check over MAIN specs — 39 specs still carry
  the sentence `openspec archive` itself writes when it creates a capability,
  `TBD - created by archiving change <X>. Update Purpose after archive.`,
  and nobody went back to replace it. The 1.12 message states the rule that
  makes this a MAIN-spec edit and not a delta: *a `## Purpose` in a delta is
  read only when the capability is created, so it cannot replace this one.*
- a **task-group numbering** check — `add-doxchat-model-intake` carries tasks
  `4.1` and `4.2` physically under `## 3.`, because the `## 4.` header was
  never written.
- a **scenario-currency** check over an active change's MODIFIED blocks —
  which is where this packet stops, and § The two it does not fix says why.

A bump proposed against an unmeasured corpus is a bump that discovers 42
failures on the pull request that performs it, in the one check every other
lane's work also has to pass. **Measuring first, and fixing what is genuinely
stale, is the cheap half; it is done here so the bump can be a bump.**

## What changes

**Nothing normative.** Concretely:

1. **39 real Purposes**, written into the main specs directly. Each derived
   from that spec's own `### Requirement` headers and from the CREATING
   change's `proposal.md` under `openspec/changes/archive/`. A Purpose is
   prose ABOUT a capability: it carries no SHALL, adds no scope, and is not a
   restatement of the requirement list.
2. **One missing group header** in `add-doxchat-model-intake/tasks.md`, with
   a dated note in that packet's own Amendment Record. Nothing is renumbered:
   `4.1` and `4.2` are already cited by those numbers in five places, one of
   them a dated amendment, so renumbering would have falsified a record.
3. **Four dated ordering notes**, one in each of the four active changes whose
   MODIFIED delta targets a requirement a DIFFERENT active change has not
   archived yet. **No delta is repointed and no intent is rewritten** — see
   § The four orderings.
4. **ONE `## ADDED Requirements` delta on `document-lifecycle`** — *A promoted
   specification carries a written Purpose, repaired in the promoted
   specification*. It sits beside that capability's existing promotion rules
   (*Ratified spec deltas reach the promoted specification*; *A MODIFIED
   requirement block restates the requirement as canon currently states it*)
   and states the rule this packet had to discover before it could act. It is
   written because strict validation REFUSES a delta-less change, and it
   invents nothing: the tool's own 1.12 message states the delta-is-read-only-
   at-creation rule, and 39 undischarged placeholders are the measurement.
5. **This packet's own five files**, one README records row, one ledger row.

## The four orderings

The 1.12 run reports four `[INFO]` lines of the form *"Archive would refuse
this delta"*. **They are INFO, not failures: they do not count against the
0-failed target, and no one of them is a broken pointer.** Read rather than
assumed, all four are the SAME shape — a MODIFIED delta on a requirement (or
a whole spec) that another change ADDS, where the adding change is ALSO still
active:

| MODIFYING change (active) | target | ADDED by (active, not yet archived) |
| --- | --- | --- |
| `add-wallet-carried-review-authority` | `roles-authority-model` § *Pilot repository and reviewing domain* | `add-substantive-review-lane` |
| `implement-keycloak-install-repo` | `repo-boundary-governance` § *Keycloak install repository boundary* | `add-identity-brokering` |
| `implement-openxpki-install-repo` | `repo-boundary-governance` § *OpenXPKI install repository boundary* | `add-trust-anchor` |
| `add-cpc-clearing-boundary` | the whole `clearing-dispatch-boundary` spec | `add-clearing-dispatch-boundary` |

The first of these says so IN ITS OWN DELTA, in a marker written on
2026-08-31: *"the lane change adds this requirement and this change was
authored the day that change ratified"*. The other three are the same fact
without the marker. **Every one of the four deltas is correct as written; the
corpus simply has not archived the predecessor yet.** The remedy is archive
ORDER, which no packet may take on another packet's behalf, so this one
records the dependency where the next reader of each change will meet it and
claims nothing further.

**What is genuinely OWED, and is not taken here:** all four modifying changes
read `declares: absent` in `tests/sequenced_after/corpus-ledger.yaml`, and
this repository already has the machine-readable instrument for exactly this
— the `sequenced_after:` front-matter field. Declaring it on four other
ratified packets would move four ledger rows beyond this packet's own and
would edit four proposals this packet has no mandate over, and
`add-sequenced-after-substrate` — the change that builds the validator which
would read them — is itself still active and unrealized. Recorded as owed.

**And a second owed act, sharper:** promoted canon already governs this exact
shape — `document-lifecycle` § *A MODIFIED block over a requirement no promoted
specification carries declares its basis by marker* — and says the shape is
LAWFUL, the declaration being what makes it so.
`add-wallet-carried-review-authority` carries its marker; the other three do
not, and owe one. Supplying a marker means writing inside another packet's
MODIFIED block, where it is a unit that packet's own currency reader counts, so
it is left to those packets and recorded here.

## The two it does not fix

**THIS IS THE PACKET'S VETO POINT, AND ITS MOST IMPORTANT FINDING.**

Two changes fail 1.12.0 at ERROR level and **this packet refuses to fix
them**, because the only available fix is to revert two ratified decisions:

- `add-chain-attestation` :: `signed-execution-chain` MODIFIED *"A gate
  validates the short chain as a hash-linked chain"* omits canon's scenario
  *"a tranche-two link does not exist yet"*.
- `add-composed-view-authoring` :: `ideation-dashboard` MODIFIED *"Composed
  views are read-only with a repository jump"* omits canon's scenario *"Gate
  verbs hide on a composed view"*.

Neither omission is an accident. **Both blocks carry the house's RESERVED
MARKER declaring the omission deliberate**, in the exact form
``**Merged into `<destination>` by <change-id> (<date>):**``, and in both
cases the scenario was RENAMED AND NARROWED rather than dropped:

- the tranche-two scenario's antecedent had become *a permission for exactly
  the chain this tranche refuses*, which is the contradiction the council's
  LA-A1 was raised to close; its successor carries the same rule scoped to a
  link **no ratified tranche has yet put in force**.
- *"Gate verbs hide on a composed view"* became *"Tile-bound gate verbs hide
  on a composed view"*, because the same change deliberately admits document
  CREATION on a composed view. Restoring the unqualified title would
  contradict the very scenario beside it.

**openxFactory has already ruled on this exact case, and 1.12.0 contradicts
the ruling.** The promoted `doc-health` requirement *"Currency of an active
change's MODIFIED requirement blocks"* defines these two marker forms, states
that ``a `Merged into` marker names titles only``, and names `Merged into` as
*"the author's instrument for a retitle"*. Its own worked example, written
into canon, is:

```
**Merged into `Tile-bound gate verbs hide on a composed view` by add-example-change (2026-08-27):** `Gate verbs hide on a composed view`
```

— which is, byte for byte, the rename in `add-composed-view-authoring`. That
rename was declared by its own landed change (#444, *"Declare
add-composed-view-authoring's rename with a Merged-into marker"*).

**1.12.0's scenario-currency check is marker-blind.** It compares scenario
title sets and cannot read the declaration this house requires, so it
re-reports as an ERROR precisely the two blocks canon holds up as correct.

**The consequence for the bump, stated plainly so nobody discovers it later:**
while these two changes are active, openxFactory cannot read 0 failed under
`1.12.0`, and `openspec archive` at 1.12.0 would REFUSE both. Both findings
disappear on their own when the two changes archive, since archived changes
are outside the `--all` corpus. The bump therefore has three honest exits, and
this packet takes none of them: sequence the bump after both archive; carry a
dispositioned exception; or take it upstream so the check learns the markers.

## Impact

- **Affected specs:** 39, `## Purpose` block only, plus ONE ADDED requirement on `document-lifecycle`. No requirement, scenario,
  or status is touched, so no promotion fidelity or canon-unit movement
  arises and no `Removed from canon by` marker is owed anywhere.
- **Affected changes:** 5 `tasks.md` files, additive text only; no delta body,
  no front matter, no lifecycle header.
- **Contract surface:** none. No bundle, no digest, no tag.
- **Corpus counts:** the ledger gains ONE row, this packet's own.
