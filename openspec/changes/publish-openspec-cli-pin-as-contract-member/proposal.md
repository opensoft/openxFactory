---
code_surface: openxFactory — TWO EDITORIAL FILES AND NOTHING ELSE. (1) `contracts/manifest.yaml` gains ONE row, `id: openspec-cli-pin`, `path: contracts/openspec-cli-pin.yaml`, `type: pin`, `adapter_owner: openxFactory`, `compatibility: canonical_openxfactory_contract`, `intended_consumers`, and a `consumption_rule` written on `domain-factory-conformance-validator`'s precedent (`contracts/manifest.yaml:184-199`) — check openxFactory out at `stack.yaml`'s `xfactory.contract_ref` and invoke the entrypoint from that checkout; copying is a conformance violation. (2) `contracts/README.md` gains the matching Native-contract-index row and ONE new consumer-facing section, *Gating archives on the pinned CLI from a consumer repository*, carrying the checkout-at-`contract_ref` recipe as codexFactory and OpsxFactory already run it plus the declared copy-in fallback for a repository with no stack pin. NOT THIS CHANGE'S SURFACE, each for a stated reason: `contracts/openspec-cli-pin.yaml` itself is NOT EDITED — no version moves, no digest moves, no disposition is added or retired, and this packet must not be read as approving a bump; `scripts/validate-openspec-cli-pin.py`, `scripts/install-pinned-openspec-cli.py`, `scripts/proposal-support.py` and every workflow are UNTOUCHED, because the gate they implement is already ratified and running and this packet publishes the pin rather than changing what it does; no consuming repository is wired from here (B of #754 and every sibling's adoption belong to their own lanes and their own pull requests); and NO release bundle is cut, no `contracts/releases/**` file is written and no tag is pushed.
target_release: none — MEASURED, NOT ASSUMED. (`none` is HOUSE PRACTICE and not an enumerated value: `release-realization` § *Realization axis declaration* enumerates `implemented` or a named aggregation-repo release, and eleven active changes in this corpus spell the no-bundle case `none`. It is used here in that established sense — no contract bundle is cut by this packet — and the reading is measured below rather than left to the word.) The derived release membership reads **283 members before this diff and 283 after**, with `contracts/openspec-cli-pin.yaml` absent from it in both readings (`scripts/hermes_runtime_validation/release.py::release_membership`, taken on this branch on 2026-09-07). Membership is a CLOSED set computed from the hermes-runtime contract index, the fixture index, `scripts/hermes_runtime_validation/**`, four `NAMED_VALIDATORS`, seven `AUXILIARY_MEMBERS` and three `NORMATIVE_DOCS` (`release.py:38-103,532-745`) — it does NOT read `contracts/manifest.yaml`'s `contracts:` list — so a row added there moves no member. Both files this packet edits are EDITORIAL members (`release_inventory.py:57-67`; `release-surface-integrity` names exactly the three), whose movement between cuts is a declared expected state reported at `info`, never a defect. Therefore no digest set moves, no `contract_bundle_version` is spent and no release tag is owed; `release-tag-gate` runs (the diff touches `contracts/manifest.yaml`) and is expected to PASS, `contract-v3.4` being published as an annotated tag peeling to `807a4f47`. Under `release-realization` the code surface is non-empty, so this packet archives on merged-plus-green realization evidence rather than on landing.
sequenced_after: [add-openspec-cli-pin]
Status: draft
Proposed: 2026-09-07
Origin: openxFactory issue **#754**, the governing record of Brett Heap's two rulings of 2026-09-07 — rollout **"Hybrid A+B"** and lane scope **"openxFactory only; siblings via their lanes"** — and of the read-only survey those rulings were taken on. THE ORIGIN IS NOT A RATIFICATION: the rulings choose a ROLLOUT SHAPE and a LANE SCOPE and decide no wording, no requirement and no design option here. `.openspec.yaml` carries drafting provenance only — no `approved_by`, no `approved_on` — and every document in this packet carries `Status: draft` to match. The decision most worth a veto is `design.md` **D1**: **A-defer** (register now, cut later) against **A-cut** (register and cut `contract-v3.5` in this pull request).
---

# Proposal: publish-openspec-cli-pin-as-contract-member

Status: draft
Proposed: 2026-09-07, in lane `openxfactory-1`.
Origin: openxFactory issue
[#754](https://github.com/opensoft/openxFactory/issues/754). The origin admits
the work and fixes its scope; it ratifies no text here. § Ratification records
what is owed.

## Why

**The pin governs a fleet and the fleet's own contract register does not
mention it.**

`contracts/openspec-cli-pin.yaml` is the estate's claim about WHICH TOOL
adjudicates canon: `openspec validate --strict` is the gate every spec delta
passes and `openspec archive` is the act that writes a ratified delta into
canon. Two repositories already gate on it, and both reach it the same way —
they check `openxFactory` out at their own `stack.yaml` `xfactory.contract_ref`
and run `scripts/validate-openspec-cli-pin.py` from that checkout, copying
nothing.

And yet, measured on this branch on 2026-09-07:

| register | carries the pin? |
| --- | --- |
| `contracts/manifest.yaml` (205 rows) | **no** — **zero occurrences** of the string `openspec-cli-pin`, re-measured 2026-09-07 (`git grep -c 'openspec-cli-pin' origin/main -- contracts/manifest.yaml` → `0`). An earlier draft of this row said the string appeared inside the `openxwallet-pin` prose comments; it does not, and those comments carry `openxwallet-pin.yaml` |
| `contracts/README.md` | **no** — zero occurrences |
| `contracts/releases/contract-v3.4.digests.yaml` (283 members) | no (and this packet does not change that) |

So the one file that says which tool decides what canon is, is absent from the
register `scripts/validate-manifest-digests.py`'s own docstring calls *"what
cross-repo consumers read to verify the bytes they pin"*. A consumer finds the
pin today only by already knowing its path.

**The survey behind #754 says what that costs, in two lines.** Of 26 repositories
carrying `openspec/`, exactly TWO gate on the pin (openxFactory; codexFactory,
required since its #227) and one more consumes it with a shadow-only gate
(OpsxFactory); **twenty repositories have zero pin awareness**, three of them
archiving this week on whatever `openspec` is on PATH — Omnigent-Install
(2026-09-07), openXwallet (2026-09-06), xFactory-Hermes-Install (2026-08-27) —
and no archive commit anywhere in the estate names the CLI version that produced
it.

## What this packet does and does not claim

**IT DOES NOT CHANGE THE GATE.** The gate is ratified and running.
`add-openspec-cli-pin` already requires that a consuming repository *"invokes the
pinned entrypoint from the pinned `openxFactory` checkout rather than copying
the entrypoint or installing the CLI itself"* and that it *"names in its
`stack.yaml` the `openxFactory` version whose pin it is consuming"*
(`openspec/changes/add-openspec-cli-pin/specs/neutral-product-pin/spec.md`,
requirement 2, scenario *A consuming repository wires its own gate*). Nothing
here restates that, weakens it or extends it.

**WHAT IS MISSING IS PUBLICATION.** The ratified requirement tells a consumer
what to DO once it knows about the pin. It does not make the pin FINDABLE, and
it does not make adoption ride the pin-sync a consumer already performs. That
gap is what `add-openspec-cli-pin` itself declared rather than hid: its
`code_surface` front matter names four new artifacts, *"none of them a registered
contract row"*, and its `target_release: none` records that *"neither of those
appears in `contracts/manifest.yaml` nor in any `contracts/releases/*.digests.yaml`
inventory"*. The pin was never modelled as publishable, and the reason it was not
is written into the pin's own header: **openxFactory does not OWN the OpenSpec
CLI, it CONSUMES it.**

**THAT REASON IS SOUND AND IT DOES NOT REACH THIS CONCLUSION.** openxFactory
does not publish the CLI. It publishes ITS OWN CLAIM ABOUT WHICH ARTIFACT
ADJUDICATES — a file it authors, versions, disposes exceptions in, and gates its
whole corpus on. That claim is exactly the kind of thing the contract register
exists to carry, and registering it transfers no ownership of the product: the
row's `adapter_owner` and `compatibility` describe the PIN, and the delta says
so in canon rather than leaving it to be inferred.

## What changes

### 1. The delta — two ADDED requirements in `neutral-product-pin`

**No `## MODIFIED` and no `## REMOVED`.** The requirement a modification would
naturally land on — *An external neutral product is pinned by commit and digest,
never by tag* — is under an ACTIVE `## MODIFIED` block held by
`add-openspec-cli-pin`, which has not archived. Writing a second block over the
same title would make this packet a co-modifier of a requirement whose promoted
text does not yet carry the pending clauses, so the block would have to restate
either the promoted text (contradicting the pending one) or the pending text
(restating canon this repository does not yet hold). Two ADDED requirements
avoid the collision entirely and are ordered behind both CLI-pin packets by
`sequenced_after`.

**R1 — a consumption pin another repository reads is a PUBLISHED contract
member, adopted by pin-sync.** Registration in `contracts/manifest.yaml` and
`contracts/README.md`; adoption rides the consumer's ordinary pin-sync;
publishing the pin is not publishing the pinned product; a consumer gates by
reading from the pinned checkout and never by copying; and ONE admitted
fallback, for a repository with no stack pin, which must DECLARE the commit it
copied from, the digest of what it copied and the divergence it accepts, and
must retire the copy when it adopts a stack pin. R1 also carries the
PRECONDITION on the normal case — the consumer's `contract_ref` must be at or
after the commit that introduced the entrypoint, or the read is unavailable and
a pin-sync is owed — and the clause reconciling the fallback with this
capability's promoted requirement *A required check runs the pinned tool, at the
pinned digest*: a required check wired off a declared copy leaves that
requirement's enforcement claim UNMET until the copy is retired.

**WHOSE FALLBACK IT IS, CORRECTED AGAINST THE TREE.** An earlier draft of this
packet cited OpsxFactory's `contracts/openspec-cli-pin-consumption.yaml` as the
fallback's worked example. **That citation was wrong and is withdrawn.**
OpsxFactory carries an `xfactory:` stack pin (`contract_ref: 724a2a4f`), copies
NOTHING (neither the pin nor the entrypoint exists in its tree), records
`commit_source: stack.yaml xfactory.contract_ref` — a POINTER, asserted
statically by `scripts/opsx_validation_gate.py` — and states no divergence from
openxFactory; the *"DECLARED DIVERGENCE"* in its workflow header is a divergence
from OPSXFACTORY'S OWN ratified `design.md` § 4/§ 6 (an `npm ci` install of
`@fission-ai/openspec@1.2.0`) TOWARD this pin, and
`advance-openxfactory-pin-and-fold-cli-pin` went in the RETIRE-THE-COPY
direction. OpsxFactory is the NORMAL case in its hardened form — a
digest-verified read from the pinned checkout, proving the entrypoint that RAN
is the entrypoint that was REVIEWED — and it is re-cited there.

**The fallback's first realized instance is elsewhere, and it landed today.**
xFactory-Hermes-Install PR
[#72](https://github.com/opensoft/xFactory-Hermes-Install/pull/72), merged
`06c9083d` on 2026-09-07 as B of #754, is a declared copy: three vendoring
headers naming openxFactory `44d8fbaf`, and a stated divergence (three `uses:`
commit-SHA pins in the adapted workflow, governed archive routing deferred). It
satisfies TWO of R1's three fields; **the digest of what it copied is not
recorded** — byte-identity is asserted below the header, with a `diff` recipe in
place of a per-file `sha256` — so that field is OWED on that repository and is
named as owed here rather than counted as met.

**ONE ORDERING CLAIM COULD NOT BE DECLARED, AND THE REASON IS A FINDING RATHER
THAN A CHOICE.** `sequenced_after: [add-openspec-cli-pin]` is what this packet
declares. It would also stand behind `bump-openspec-cli-pin-to-1.12`, and that
entry is UNWRITEABLE: `scripts/validate-sequenced-after.py` refuses any entry
whose change-id half does not match `^[a-z0-9][a-z0-9-]*$`, and that sibling's
own directory name carries a `.`. So a change in this repository cannot be
sequenced behind the bump by any spelling — measured, not inferred, by writing
the entry and reading the refusal. It is recorded as an owed successor at
`tasks.md` § 5.6 rather than worked around here.

**R2 — registering a pin in the consumption register is not a bundle cut unless
it moves the release membership.** This is D1 written into canon so that the next
author does not have to re-derive it, and it carries an obligation on the
registering author: RECORD THE DERIVED MEMBERSHIP BEFORE AND AFTER, because a
membership that is computed cannot be eyeballed and silence about it is not
evidence it did not move.

### 2. The realization — one manifest row, one README row, one README section

In this pull request, per `release-realization`'s decomposition rule.

The manifest row is written on the precedent already in the file:
`domain-factory-conformance-validator` (`contracts/manifest.yaml:184-199`),
`type: tool`, whose `consumption_rule` reads *"Domain repos must invoke this
validator from their pinned openxFactory checkout … Copying the validator into a
domain repo is a conformance violation"*. That sentence is the never-copy rule
this packet needs, already ratified in the register's own voice, for a
neighbouring artifact.

The README section is written FOR A CONSUMING REPOSITORY rather than for this
one: three steps, the exact shape codexFactory's `validate.yml` and OpsxFactory's
`opsx-validation.yml` already run, plus the declared copy-in fallback.

## The cut question, and why it is D1 rather than an assumption

**MEASURED ON THIS BRANCH, 2026-09-07.** The derived release membership is a
CLOSED SET computed by `scripts/hermes_runtime_validation/release.py::_collect_members`
(`:532-745`) from: the hermes-runtime contract index's `release_member: true`
rows, the fixture index, every module under `scripts/hermes_runtime_validation/`,
four `NAMED_VALIDATORS`, seven `AUXILIARY_MEMBERS` and three `NORMATIVE_DOCS`
(`:38-103`). **It does not read `contracts/manifest.yaml`'s `contracts:` list at
all** — the manifest is consulted only for `contract_bundle_version` and for the
six intent-compliance registrations. So:

```
release_membership(.)  before this diff : 283 members
release_membership(.)  after  this diff : 283 members
contracts/openspec-cli-pin.yaml in membership : False (both readings)
contracts/manifest.yaml         in membership : True  (editorial)
contracts/README.md             in membership : True  (editorial)
```

`contracts/manifest.yaml`, `contracts/CHANGELOG.md` and `contracts/README.md` are
exactly the three EDITORIAL members (`scripts/doc_health/release_inventory.py:57-67`;
`release-surface-integrity` § *The declared bundle describes the release
surface*), and drift confined to them *"is an EXPECTED, BOUNDED state that the
next cut re-baselines, and it SHALL NOT be reported as a defect"*.

**Therefore A-defer is lawful as policy stands, and it is what is designed.** No
bundle is spent, no digest set moves, no tag is owed, and `release-inventory-drift`
gains no `error` from this diff. The alternative, A-cut, is written out in
`design.md` D1 with its costs — and it is also **not available to this lane**: a
cut is a contract act taken on Brett Heap's word, and this packet neither cuts
one nor asks to be read as authorising one.

**`release-tag-gate` DOES run on this pull request**, because the diff touches
`contracts/manifest.yaml`, and it is expected to PASS. Its two substantive
refusals are `gate-findings` (a stale bundle cut earlier and still unpublished)
and `gate-version-reuse` (the declaration moved onto an already-published tag).
`contract-v3.4` is published — an annotated tag peeling to `807a4f47` — and this
packet does not move `contract_bundle_version` at all, so neither refusal has a
condition to fire on. Its verdict is reported verbatim in the pull request body,
whatever it is.

## Impact

**No consuming repository is wired from here.** #754's ruling *"openxFactory
only; siblings via their lanes"* is a scope, and this packet respects it: B (the
three no-lane repositories) is separate work with its own pull requests, every
OpsxFactory, Medx, Adx, Ledgerx and openDox-family adoption belongs to that
repository's own lane, and none is claimed by this change.

| what | where it belongs |
| --- | --- |
| the three no-lane repositories' copy-in (B of #754) | plain pull requests in Omnigent-Install, openXwallet, xFactory-Hermes-Install, each claimed on that repository's governing issue |
| OpsxFactory's shadow gate becoming required | OpsxFactory's own lanes (four live) |
| MedxFactory / AdxFactory / LedgerxFactory adoption | those repositories' owners |
| the openDox family | lane `openXfactory-4` |
| the next bundle cut absorbing nothing from this packet | the next scheduled cut; this packet spends no version |

## Ratification

**RATIFICATION HAS NOT HAPPENED AND IS NOT SOUGHT BY THIS PACKET'S LANDING.**
Brett Heap's two rulings on #754 admit the work and fix its scope. They decide no
wording here and take no design decision. Every judgment this authoring session
took is listed in `design.md` as a numbered decision with the alternative beside
it, and D1 is the one most worth a veto.

**THE VETO POINTS, NAMED HERE AS WELL AS IN `design.md` AND `tasks.md`, so a
reader who reads only this file finds them.** **D1** — A-defer (register in the
two editorial files, cut no bundle) against **A-cut** (register AND cut
`contract-v3.5` here, with the annotated tag owed after the merge). **A-member**
— a third option recorded as NOT TAKEN rather than foreclosed: add
`contracts/openspec-cli-pin.yaml` to `AUXILIARY_MEMBERS` (and its entrypoint to
`NAMED_VALIDATORS`) in `scripts/hermes_runtime_validation/release.py`, which
would move the derived membership 283 → 285 and would then require the bundle
realization order under R2's own second scenario; it is a change to the release
machinery rather than to a register, and belongs in its own packet. And **D2**,
the second and smaller veto point: the manifest row carries NO `sha256`, on
`domain-factory-conformance-validator`'s precedent, with the digest-bearing
alternative and its cost written out beside it in `design.md`. A veto on any of
the three lands on a written alternative rather than on a blank.
