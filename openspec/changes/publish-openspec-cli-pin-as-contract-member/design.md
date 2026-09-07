# Design: publish-openspec-cli-pin-as-contract-member

Status: draft (nothing here is ratified by being authored)

Every claim below about running code was read in a fresh clone of this
repository at `44d8fbaf` (openxFactory `main`, 2026-09-07) and is cited
`file:line`. Every number was produced by running the named code on that tree.

## D0 — The measurement, taken before the design

Three questions were asked of the tree before any option was written, because
the whole cut/defer decision turns on the answers and none of them is obvious
from reading prose.

**(a) Is the pin registered anywhere?** No.

```
git grep -c 'openspec-cli-pin' origin/main -- contracts/README.md         -> 0
git grep -c 'openspec-cli-pin' origin/main -- contracts/manifest.yaml     -> 0
git grep -c 'openspec-cli-pin' origin/main -- \
        contracts/releases/contract-v3.4.digests.yaml                     -> 0
```

**CORRECTED, AND THE CORRECTION IS THE POINT OF SHOWING THE COMMAND.** A first
draft of this section reported the manifest as carrying the string *"only inside
prose comments belonging to the `openxwallet-pin` rows (lines 2076-2685)"*.
Re-measured 2026-09-07, that is **ZERO OCCURRENCES**: the prose at those lines
carries `openxwallet-pin.yaml` and never `openspec-cli-pin`. The registration
gap is therefore total in all three registers rather than partial in one, which
is a stronger reading of the same finding and was worth correcting rather than
softening.

Its two siblings are in the same state: neither `contracts/openxwallet-pin.yaml`
nor `contracts/openreposhape-pin.yaml` is a registered row either. The pin class
as a whole has never been published.

**(b) What computes release membership?**
`scripts/hermes_runtime_validation/release.py::_collect_members` (`:532-745`),
from six sources and no others (`:38-103`):

| source | what it contributes |
| --- | --- |
| `contracts/hermes-runtime/contract-index.yaml` | every row with `release_member: true` |
| `contracts/hermes-runtime/fixtures/index.yaml` | every case input |
| `scripts/hermes_runtime_validation/**` | every module |
| `NAMED_VALIDATORS` (`:84-89`) | four literal paths |
| `AUXILIARY_MEMBERS` (`:90-98`) | seven literal paths, incl. the manifest, changelog and README |
| `NORMATIVE_DOCS` (`:99-103`) | three literal paths, when present |

`contracts/manifest.yaml` is read for exactly two things — `contract_bundle_version`
(`:587`) and the six intent-compliance registrations (`:601-616`). **The
`contracts:` list is never walked for membership.** A row added to it therefore
adds no member, and the fact is structural rather than incidental.

**(c) What does the membership actually read?**

```
python3 -c "from scripts.hermes_runtime_validation import release; ..."
release_membership(.)                             -> 283
contracts/openspec-cli-pin.yaml   in membership   -> False
scripts/validate-openspec-cli-pin.py in membership-> False
contracts/manifest.yaml           in membership   -> True
contracts/README.md               in membership   -> True
```

283 is also the entry count of `contracts/releases/contract-v3.4.digests.yaml`,
so the declared bundle and the derived membership agree at this commit.

## D1 — THE VETO POINT: A-defer against A-cut

**A-defer is DESIGNED.** Register the pin in `contracts/manifest.yaml` and
`contracts/README.md` in this pull request; cut no bundle; leave the pin's
arrival in a release inventory to whatever the next scheduled cut naturally
contains.

**Why it is lawful, in the policy's own words.** `contracts/manifest.yaml` and
`contracts/README.md` are two of the exactly three EDITORIAL members
(`scripts/doc_health/release_inventory.py:57-67`, and `release-surface-integrity`
§ *The declared bundle describes the release surface*: *"THE EDITORIAL MEMBERS
are `contracts/CHANGELOG.md`, `contracts/manifest.yaml` and
`contracts/README.md` … Drift confined to them is an EXPECTED, BOUNDED state
that the next cut re-baselines, and it SHALL NOT be reported as a defect."*).
`docs/contract-versioning-policy.md` § *What a red `verify-commit` at HEAD means*
says the same thing in the runbook's voice. And by D0(b) the diff adds no
member, so there is nothing for a cut to re-baseline beyond the two editorial
files a cut re-baselines anyway.

**What the checks will say, stated in advance rather than discovered.**

| check | expected reading, and why |
| --- | --- |
| `release-inventory-drift` | **no new `error`.** Both changed files are editorial; the family grades editorial drift `INFO` and non-editorial drift `ERROR` (`release_inventory.py`, the five-arm taxonomy in its docstring). |
| `release-tag-gate` | **PASS, and it does run** — the diff touches `contracts/manifest.yaml`, which is one of its two trigger paths. `gate-findings` needs a stale unpublished bundle: `contract-v3.4` is published, an annotated tag peeling to `807a4f47`. `gate-version-reuse` needs the declaration to MOVE: this packet does not touch `contract_bundle_version`. |
| `validate-contract-release.py verify-commit` | unchanged in kind: the two editorial members will read as mismatched at `HEAD`, which the policy names an expected bounded state between cuts, and which they already read as on `main` for any landing that touches them. |
| `validate-manifest-digests.py` | unchanged count: the new row carries no `sha256` (D2), so the walk over digest-bearing entries is the same set it was. |
| the STANDING `release-inventory-drift` **error** on `docs/contract-versioning-policy.md` | **pre-existing, and named so it is not mistaken for this packet's.** That file is a NORMATIVE member (`release.py` `NORMATIVE_DOCS`), not an editorial one, so its drift from `contract-v3.4` grades `error` and not `info`. It reads identically on `origin/main` and on this branch — measured `python3 scripts/doc-health.py --single-repo . --family release-inventory-drift` — because this packet does not touch that file. It is the standing debt the next cut re-baselines, and A-defer neither creates nor discharges it. |

**A-cut, written out because a veto has to have somewhere to land.** Register
AND cut `contract-v3.5` in this pull request: allocate the version, write the
`contracts/CHANGELOG.md` § `contract-v3.5` entry, build
`contracts/releases/contract-v3.5.digests.yaml`, advance
`contract_bundle_version`, and leave the annotated tag OWED on whoever lands it.
Its costs, in the order they bite:

1. **It buys nothing this packet needs.** By D0(b) the pin does not become an
   inventory member by being registered; a cut would re-baseline 283 members of
   which none is the pin. The consumer adoption this packet exists to enable is
   by COMMIT — codexFactory and OpsxFactory both resolve
   `stack.yaml['xfactory']['contract_ref']` and check openxFactory out AT THAT
   COMMIT — so a bundle number is not on the path from this row to a consumer.
2. **It spends a version number that cannot be unspent.** `contract-v2.6` is the
   estate's standing record of what that costs: cut, never published, superseded,
   and permanently reported (`doc-health` `release-tag-publication`, class
   `contested`). The Immutable Tag Correction rule makes a number unreusable.
3. **It creates a tag obligation this lane cannot discharge.** Step 5 of the
   bundle realization order is a second act by an actor with tag rights, after
   the merge. Until it is met, `release-tag-gate` REFUSES the next pull request
   that touches the release surface (`gate-findings`), which is the estate-wide
   red PR #628 caused on 2026-09-03 and `add-release-tag-gate` was written to
   bound.
4. **It is not this lane's act to take.** A cut is a contract act taken on Brett
   Heap's word. This packet does not cut, does not allocate, and must not be read
   as authorising one. If A-cut is chosen, the cut becomes a REALIZATION TASK of
   this packet — ticked when it is done, by whoever is told to do it — and not a
   thing this pull request performs.

**WHAT `docs/contract-versioning-policy.md` SAYS ABOUT THIS, ENGAGED RATHER THAN
STEPPED AROUND.** Two of its texts reach a registration, and neither was
answered in the first draft.

* § *Change Classes* grades **"new optional fields, new contracts, new validator
  warnings"** as **Additive (minor)**. A registered row IS a new contract in the
  consumption register's sense, so this packet's content is additive-minor
  MATERIAL. That is a statement about the class of the NEXT CUT, not a statement
  that a register edit is itself a cut: the class says what kind of version
  number will eventually carry it, and D0(b) says the membership it would
  re-baseline does not move.
* § *Version Identity* item 5 requires `contracts/CHANGELOG.md` to hold **"one
  entry per release listing every contract added, changed, or deprecated"**, and
  the section closes: *"The manifest and changelog update SHALL be committed
  atomically with the contract files."*

**THE HONEST ANSWER TO THE SECOND, WITH NOTHING GLOSSED.** The atomicity clause
binds a MANIFEST + CHANGELOG + CONTRACT-FILE triple at a release. This diff adds
no contract FILE: `contracts/openspec-cli-pin.yaml` already exists in the tree at
`main`, is UNTOUCHED here (D7), and only its REGISTER ROW is new. And this
repository writes no `Unreleased` block by practice — the changelog is headed at
`contract-v3.4` and every cut record in it states *"there is no `Unreleased`
block pending in this file"* — so there is no place a changelog entry could
lawfully be written today without allocating a version, which is A-cut and is
not this lane's act. **So the CHANGELOG entry naming this registered contract is
OWED AT THE NEXT CUT**, where § *Version Identity* item 5 requires the release
entry to list it. It is recorded as owed at `tasks.md` § 5.7 rather than left
implicit, and the membership/digest accounting above is unmoved by it: an
inventory member is what a digest set contains, and a changelog line is what a
release entry says.

**A third option, recorded as not taken rather than foreclosed: A-member.** Make
the pin a genuine member of the derived release inventory by adding
`contracts/openspec-cli-pin.yaml` to `AUXILIARY_MEMBERS` (and its entrypoint to
`NAMED_VALIDATORS`) in `scripts/hermes_runtime_validation/release.py`. That
WOULD move the membership from 283 to 285, would require the bundle realization
order under R2's own second scenario, and is a change to the release machinery
rather than to a register — a different packet with a different risk profile.
It is named here so that "the pin is not in the inventory" is visibly a
DECISION rather than an oversight.

## D2 — The manifest row carries NO `sha256`

**Designed: no digest**, matching `domain-factory-conformance-validator`
(`contracts/manifest.yaml:184-199`), the row this packet is modelled on: a
`type: tool` artifact with `intended_consumers`, `compatibility`,
`adapter_owner` and a `consumption_rule`, and no per-file digest.

**Why.** `scripts/validate-manifest-digests.py` walks every entry carrying a
`sha256` and fails closed on any mismatch, inside the required `pytest-suite`.
That is a good property for a file that moves at a cut. `contracts/openspec-cli-pin.yaml`
is not that kind of file: it moves on THREE distinct events, only one of which is
a version bump —

* a version bump (`bump-openspec-cli-pin-to-1.12` is the worked example);
* a DISPOSITION ADDED (`disposition-codexfactory-declared-renames` added two,
  from a different repository's readiness measurement);
* a DISPOSITION RETIRED, which is forced from outside: the verifier refuses
  `pin-disposition-stale` the moment a dispositioned finding stops occurring,
  and the pin's own header says an entry goes stale *"the day"* its change
  archives — including changes that archive in codexFactory.

A digest here would make each of those a two-file edit whose omission turns the
required suite red on `main`, and the third class of event is triggered by a
merge in another repository. The property a digest would buy — detecting a
hand-edit of the pin — is already bought twice over: the merge-gate floor names
the pin as a never-clearable path (`neutral-product-pin` § *Repointing the
reader and editing what it reads is one human-only act*), and a version move is
human-only with target-version evidence owed in the same change.

**The alternative, with its cost, so a veto lands somewhere.** Record
`sha256: 834b51a90d858a30d63b3252cc2126c4eb2407fbc9c8651a087e4bc8ce872856` (the
pin file's digest at `44d8fbaf`). It buys a checked coupling — a pin edit that
forgets the manifest reds the required suite — at the price of the three-event
coupling above, and it puts a digest of a live governance surface in a file that
is re-baselined only at cuts. Both readings are defensible; the packet designs
the quieter one and says which.

**AND THE RESIDUAL COUPLING D2 DOES LEAVE, NAMED RATHER THAN LEFT TO BE FOUND.**
Declining the digest does not make the row coupling-free. The row's
`consumption_rule` QUOTES a path — `scripts/validate-openspec-cli-pin.py` — and
the pin file names that same path in its own `consumer_entrypoint:` field, and
**nothing compares the two**. A rename of the entrypoint that updated the pin and
not the manifest would leave the register quoting a path that does not exist,
and no check in this repository would say so. That is a smaller coupling than a
byte digest (one string, moving only on a rename, rather than a whole file
moving on three event classes) and it is a real one. It is recorded as part of
§ 5.4's owed checker — the same checker that would assert a read pin IS
registered would naturally assert that the row's quoted entrypoint EQUALS the
pin's `consumer_entrypoint:` — and it is not written here.

## D3 — `type: pin`, a new descriptive value

The manifest's `type` vocabulary is descriptive and open: 14 distinct values
across 205 rows, **SEVEN of them used exactly once** — `sql_schema`,
`interface_lock`, `fixture_index`, `derivation_table`, `contract_family`,
`capability_scenario_register` and `acceptance_map` (re-measured 2026-09-07 over
`origin/main`; a first draft of this line said five and omitted `fixture_index`
and `sql_schema`). The seven sit against `schema` 153, `fixture` 21, `registry`
11, `tool` 5, `semantic_kernel` 3, `policy` 3 and `evidence_register` 2, so
half the vocabulary is singletons and a new descriptive value is the file's
ordinary habit rather than an exception argued for here. Nothing enumerates it: every reader of the manifest resolves
rows by `id` or by `path` (`scripts/check-openxfactory-pin.py:96`,
`scripts/validate-avatar-first-ui.py:656`,
`scripts/ideation_dashboard/doxbench_contracts.py:589-616`), and
`validate-manifest-digests.py` keys on `sha256` + `path`. So `type: pin` names
the artifact for a human without moving any machine.

Rejected: `type: tool` (the pin is not executable — the tool is the entrypoint
it names), `type: policy` (a policy states what may be done; a pin states which
bytes are trusted), `type: registry` (a registry enumerates members; this pin
deliberately carries no member list, and its header argues at length why).

## D4 — Two ADDED requirements, no `## MODIFIED`

The natural host for a modification is *An external neutral product is pinned by
commit and digest, never by tag* — and it is already carried in an ACTIVE
`## MODIFIED` block by `add-openspec-cli-pin`, which has not archived. A second
`## MODIFIED` over that title would make this packet a CO-MODIFIER, and the
`modified-block-currency` family judges a block against the CURRENTLY PROMOTED
requirement — which does not carry `add-openspec-cli-pin`'s pending
published-artifact clauses. The block would have to restate either the promoted
text (contradicting the pending block a reader would compare it to) or the
pending text (restating canon this repository does not hold yet). Both are worse
than not needing the block at all.

Two ADDED requirements need no such reconciliation, and
`sequenced_after: [add-openspec-cli-pin]` records the ordering claim explicitly:
R1 and R2 stand on the pin file that change lands. The corpus ledger reads this
packet's class from the requirement keys it writes; both titles are new, so no
partner row flips.

**THE SECOND ENTRY IS UNWRITEABLE, AND THAT IS A FINDING.** This packet also
stands behind `bump-openspec-cli-pin-to-1.12`, and that entry cannot be
declared: `scripts/validate-sequenced-after.py` refuses any entry whose
change-id half does not match `^[a-z0-9][a-z0-9-]*$` —

```
sequenced_after of publish-openspec-cli-pin-as-contract-member entry
'bump-openspec-cli-pin-to-1.12' has change-id half
'bump-openspec-cli-pin-to-1.12', which does not match ^[a-z0-9][a-z0-9-]*$
```

— and that sibling's own directory name carries a `.`. So NO change in this
repository can order itself behind that one, by any spelling. It was found by
writing the entry and reading the refusal rather than by reading the grammar,
and it is recorded as an owed successor (`tasks.md` § 5.6) with its three honest
exits named — widen the grammar, rename the change, or accept that the ordering
is prose no machine reads — and none of them taken here.

## D5 — The consumer doc section lives in `contracts/README.md`

**`docs/` carries no page about the pin at all** — the load-bearing measurement,
and the one that survives re-measurement: `git grep -l 'openspec-cli-pin'
origin/main -- 'docs/*'` returns **zero** files. (A first draft over-narrowed the
surrounding claim, saying the only files naming the string outside `openspec/`
and `scripts/` were the root `README.md` and two workflows. Re-measured, there
are **TEN**: those three, plus `contracts/openspec-cli-pin.yaml` itself,
`specs/021-modified-block-currency-self-gate/contracts/self-gate-contract.md`,
and five under `tests/`. None of them is a doc page, so the conclusion below is
unchanged and the count is corrected rather than the argument.) Three homes were
considered:

* **a new `docs/openspec-cli-pin-adoption.md`** — a fourth place to keep in step,
  reachable only from a doc index, and the section is eight lines of recipe;
* **the root `README.md`** — already 5,800 lines and organised around this
  repository's own governance rather than around a consumer's task;
* **`contracts/README.md` — DESIGNED.** It is the file the registration row goes
  into, so registration and instructions arrive together and cannot drift apart;
  it is where `docs/contract-versioning-policy.md` § *Domain Upgrade Runbook*
  already sends a consumer ("read `contracts/CHANGELOG.md` between the pinned
  ref and the target ref"); and it is an editorial member, so the section costs
  no cut for the same reason the row does.

## D6 — The pin is registered; the entrypoint and the installer are not

`scripts/validate-openspec-cli-pin.py` and
`scripts/install-pinned-openspec-cli.py` are NOT given rows. A consumer reaches
them by checking the whole `openxFactory` tree out at its pinned
`contract_ref` — codexFactory and OpsxFactory both do exactly that — so a row
would publish nothing that the checkout does not already deliver, and it would
put two more paths in a register that must then track every rename. The pin's
own `consumer_entrypoint:` field NAMES the entrypoint, and the registered row's
`consumption_rule` quotes that path, so the register does point at the
entrypoint — by reference, through the artifact whose job it is to name it,
rather than by a second registration that could come to disagree.

## D7 — This packet does not touch the pin file

`contracts/openspec-cli-pin.yaml` is not edited: no version, no digest, no
`rollback:`, no `dispositions:` entry. Publishing a pin and moving a pin are
different acts with different authorities — the second is human-only and owes
target-version evidence in the same change (`add-openspec-cli-pin`, requirement
3) — and a packet that did both would be asking for one word to cover two
decisions. Nothing here may be read as approving a bump.
