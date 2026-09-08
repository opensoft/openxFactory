---
code_surface: none — this packet's whole diff is governance text in openxFactory: one `document-lifecycle` spec delta (two `## ADDED` requirements and one `## MODIFIED`), this packet's own four files, one README "OpenSpec Records" row, and one `tests/sequenced_after/corpus-ledger.yaml` row. NO contract is added or changed — `contracts/manifest.yaml` is untouched, no digest inventory moves, no `contracts/CHANGELOG.md` line is owed and no release tag is owed. NO validator, workflow, script or test changes: in particular the rule this packet states is enforced by gates that ALREADY EXIST or are proposed ELSEWHERE (OpsxFactory's citation gate, live since its PR #248; OpsxFactory's `add-content-address-integrity-gate`, proposed), and this packet deliberately builds no checker of its own — a rule and its checker landing in one act is how the estate has repeatedly shipped a rule the checker's shape quietly narrowed. Realization is the merge itself.
target_release: implemented (the openxFactory main line; governance text only, so realization is the merge and no contract bundle is cut). Per `release-realization` an EMPTY code surface archives on landing rather than on merged-plus-green realization evidence.
sequenced_after: [govern-openspec-corpus-membership]
---

# Proposal: govern-archived-record-edits

Status: draft
Proposed: 2026-09-08
Awaiting ratification: Brett Heap
Lane: opsXfactory-1

Origin: Brett Heap's **F.3** ruling, in session, first-hand to lane
`opsXfactory-1`, given on OpsxFactory PR #248 in **TWO comments on two days**,
and both are named because each carries one of the two verbatim selections. The
rule's SHAPE — comment
[5563099832](https://github.com/opensoft/OpsxFactory/pull/248#issuecomment-5563099832),
**2026-09-06T23:42Z** — is *"Header/bookkeeping edits only + re-derive pins"*.
Its HOME — comment
[5571629298](https://github.com/opensoft/OpsxFactory/pull/248#issuecomment-5571629298),
**2026-09-07T13:51Z** — is
*"Both at once"* — *"an OpsxFactory change (dated amendment to
`docs/packet-lifecycle-headers.md` + an ADDED requirement: header/bookkeeping
edits only under a recorded ruling, and every edit of a pinned target
re-derives dependent pins in the same change) AND an openxFactory change
amending the promoted document-lifecycle capability, with the OpsxFactory
re-pin."* The ruling states its own exposure: *"two claims in two repos."*

**THAT RULING IS AN ADMISSION TO THE QUEUE, NOT A RATIFICATION OF THIS TEXT.**
It settles what the rule says and where it lives. Whether these words say it
correctly is Brett Heap's to decide, and until he does this packet is `draft`
and every box in `tasks.md` stays unticked.

Lane claim: openxFactory issue
[#630 comment 5578961492](https://github.com/opensoft/openxFactory/issues/630#issuecomment-5578961492)
(2026-09-08T03:59Z), substrate claim
[…#issuecomment-5578961805](https://github.com/opensoft/openxFactory/issues/630#issuecomment-5578961805)
(README Records block row 3 + the sequenced-after ledger row).

This is the ESTATE-NEUTRAL half of a matched pair. The domain half is
OpsxFactory's `govern-archived-record-edits` — the same working id, claimed at
OpsxFactory issue
[#207 comment 5578960955](https://github.com/opensoft/OpsxFactory/issues/207#issuecomment-5578960955),
with its substrate claim
[…#issuecomment-5578961206](https://github.com/opensoft/OpsxFactory/issues/207#issuecomment-5578961206)
(that repository's `openspec/README.md` Records block) —
— which states the same rule at that repository's own altitude, over that
repository's archive tree and its own gates, and carries the dated amendment to
`docs/packet-lifecycle-headers.md` that the ruling names. Neither half is the
other's summary: this one states the rule for every repository the
`document-lifecycle` capability governs, and that one states what OpsxFactory's
archive tree, its citation gate and its content-address register do about it.

## Why

**A permissive convention was the whole of the governance, and it was measured
failing.** OpsxFactory's `docs/packet-lifecycle-headers.md` § *Editing an
archived packet* — a convention ratified 2026-08-24 — permitted an edit to an
archived packet on a BOOKKEEPING NOTE ALONE. On that same day, commit
`57fd9fd2` ("Discharge all 55 lifecycle-header defects in the OpenSpec scan
set", 63 files) wrote SIXTEEN files under that repository's
`openspec/changes/archive/` tree under that convention, inserting one
`Ratified:` line per target. It broke THREE executed consent instruments'
`custody.sha256`. The content of the targets did not change — re-derived at
`57fd9fd2^` each still matches — and the one pin that still verifies is the one
that commit did not touch: 3 of 3. One of the three broken targets sits in a
change directory that HAS NEVER BEEN ARCHIVED, which is why the class is
pinned-target integrity rather than archiving. **Thirteen days passed before
anything noticed.**

These facts are CITED, not re-derived here. They were measured by OpsxFactory's
citation sweep on 2026-09-06 at `ddc03ad7` and are recorded in that
repository's owed-findings register, § F.3. **THAT REGISTER IS MID-ARCHIVE AND
ITS PATH IS NOT YET A FACT.** At OpsxFactory `main` today it is the LIVE path
`openspec/changes/add-pre-archive-citation-gate/supporting-docs/owed-findings.md`;
its archive PR is in flight (OpsxFactory #273, still OPEN at this writing) and
on merge the register files at
`openspec/changes/archive/2026-09-07-add-pre-archive-citation-gate/supporting-docs/owed-findings.md`.
Both are named here rather than one asserted, because a citation of the archive
path written before the archive lands is a claim about a file that does not yet
exist — which is the class of defect the citing repository's own gate was built
to refuse. The same register's § F.1 carries the custody half, ADDRESSED BY —
not discharged by — `add-consent-custody-rederivation-record`, merged 2026-09-08
as `543d47a9`: that packet is a ratified PROPOSAL whose 46 boxes are all
unticked, so the three broken pins are still broken and the contract still reads
`contract_schema_version: 2`. "Discharged" would claim a repair nobody has
performed, which is the class of overstatement this packet exists to refuse.

**There was no general rule to break.** Two OpsxFactory packets had cited
`FR-072` as forbidding archive writes. That reading was wrong: `FR-072` is
feature 010's CLOSE-TIME FENCE for one feature, not an estate rule. So on
2026-09-07 the corpus stood in this position — a widely believed prohibition
that does not exist, and a written convention that permits more than anyone
intended. This packet supplies the rule the belief was reaching for.

**The archive is load-bearing in two independent ways, and this capability
already knows both.** *Ratified spec deltas reach the promoted specification*
makes "the MOST RECENT archived delta that touches it, and that one alone" the
AUTHORITY for a promoted requirement — an edit to an archived delta edits the
standard canon is checked against, with no proposal and no ratification in the
act. And archived files are content-address TARGETS named by locator and
`sha256` from elsewhere in the corpus.

**And this capability already names the missing route without stating it.**
*Proposal packets carry the lifecycle header* ends its discharge clause with
"Backfilling a header onto an archived packet is an archived-record edit and
**takes the route archived-record edits take**." That sentence points at a route
that does not exist. It was written 2026-08-24 by
`govern-openspec-corpus-membership` — the same day as `57fd9fd2`, and the
dangling reference and the breakage are the same gap seen from two sides. The
`## MODIFIED` block in this packet closes it.

## What Changes

One `document-lifecycle` spec delta, three requirement blocks.

**`## MODIFIED` — *Proposal packets carry the lifecycle header*.** The block
restates the promoted requirement as canon states it and the restatement was
VERIFIED rather than asserted: extracted programmatically from
`openspec/specs/document-lifecycle/spec.md` and diffed against it. **Canon's
block is 5,815 characters; the delta block is 7,186; the difference of 1,371 is
entirely INSERTED** (measured over the slice from the requirement heading to the
next one, trailing newlines stripped on both sides). EVERY canon byte is carried
verbatim, all six promoted scenarios are restated, and there are exactly two
hunks of difference, **both PURE INSERTIONS**. The
dangling sentence "takes the route archived-record edits take" is left
UNTOUCHED and a paragraph after it names the route and says that where the
backfilled file is also a pinned target the second requirement attaches as well,
the two obligations being independent. And one scenario is added, *A header
defect is discharged on an archived packet*, which is the `57fd9fd2` act stated
as a rule. Nothing is reworded and nothing is deleted, so no `Removed from
canon` marker is owed.

**`## ADDED` — *An archived record is edited only as a bookkeeping correction
under a recorded ruling*.** The route. A file under `openspec/changes/archive/`
may be edited ONLY as a lifecycle-header or bookkeeping correction, under a
ruling RECORDED BEFORE THE EDIT, carrying a bookkeeping note; every other edit
of an archived byte is refused. **The note has a NEUTRAL MINIMUM** — a dated
`Edited (bookkeeping): <UTC date> by <change-id> — <edit class>` line in the
edited file's own lifecycle-header block — because an earlier spelling
delegated the note to "the editing repository's own convention" and
**openxFactory, the repository promoting this capability, HAS NONE**; only
OpsxFactory has written one down, so the delegation left the obligation absent
in the loosest repository in the estate. A local convention MAY be stricter and
MUST NOT be absent, and the note sits in the lifecycle header on purpose: that
block is the one part of an archived file this rule already permits the edit to
touch, so recording the edit cannot itself be an edit the rule forbids. The bookkeeping class is defined BY EFFECT ("does the edit
change what the record asserts?") rather than by a list of filenames, because
`proposal.md` carries both classes and a path-keyed rule would license a
substantive rewrite inside a file the list called safe. And the note is
explicitly NOT the authorization: a convention satisfied by the note alone
authorizes every edit its author believed was bookkeeping, which is the same
thing as authorizing every edit. A repository's local convention may be
STRICTER and may not be LOOSER.

**`## ADDED` — *A change that edits a pinned target re-derives every dependent
pin in the same change*.** A change that edits a file any in-repo
content-address pin names — ARCHIVED OR LIVE — must re-derive every dependent
pin and record it IN THE SAME CHANGE, by the rule the pin's own family
declares. Stated separately from its neighbour because the two failures are
invisible to each other, and because one of the three measured breakages was
never in the archive tree at all: a rule scoped to `archive/` would have left
it broken while reporting itself satisfied. Re-derivation is PER FAMILY: for
consent instruments the rule is the structured `custody_rederivations[]` entry
proposed by `add-consent-custody-rederivation-record` — a CONTRACT home; for
every other family the rule is declared either in the declaring repository's
content-address register OR in the neutral contract that owns the family, and
OpsxFactory's `add-content-address-integrity-gate` proposes the estate's first
REGISTER home. **A family that declares no rule has not earned a pin — and the
consequence arrives WITH THE DECLARATION, not with this requirement**: until a
family declares, an edit of its pinned target is REPORTED, naming the family,
the target and the home that owes the rule, and it becomes a REFUSAL for that
family the day that family declares. That transition is not a softening; it is
what keeps the rule from refusing every pinned-target edit in the estate on the
day it lands, no family having declared one yet (measured in § *Impact*).

## What This Change Does NOT Do

- **It writes no checker.** Enforcement is by gates that already run or are
  separately proposed. The obligation this packet creates is the RECORDING.
- **It repairs no pin.** The three broken OpsxFactory custody pins are F.1's
  object, and their repair waits on the contract cut and re-pin that
  `add-consent-custody-rederivation-record` sequences.
- **It edits no archived byte** — including under the rule it states.
- **It does not amend OpsxFactory's convention.** The dated amendment to
  `docs/packet-lifecycle-headers.md` is the OpsxFactory half's, scheduled there
  as a realization task and not performed at proposal time.

## Impact

- Affected capability: `document-lifecycle` (openxFactory, promoted).
- Affected repositories: every repository the capability governs — openxFactory
  and every DomainxFactory. The first domain realization is OpsxFactory's
  `govern-archived-record-edits`.
- Owed acts, named and NOT performed here. **openxFactory — THIS repository —
  owes one too, and it was missed for two drafts**: it has NO archived-packet
  convention of its own, so a rule delegating the note obligation to local
  conventions was absent exactly in the repository promoting it. The requirement
  now states a NEUTRAL MINIMUM, and task 3.4 adopts it in
  `docs/document-lifecycle.md` at realization. Then: OpsxFactory's amendment of
  its own convention; OpsxFactory's `add-content-address-integrity-gate`
  register naming a re-derivation rule per family; every other DomainxFactory
  reading its local archived-packet convention against this rule and amending
  what is looser or absent.
- Archive gate: `code_surface: none`, so this change archives on landing per
  `release-realization`.

**THE TRANSITION CLAUSE EXISTS BECAUSE OF A MEASUREMENT, AND THE MEASUREMENT IS
THIS.** On the day this packet is authored, **NO family anywhere in the estate
has a declared re-derivation rule**, in either home. The consent family's is
PROPOSED and not declared: `contracts/schemas/consent-instrument.schema.yaml`
still reads `contract_schema_version: 2`, the schema carries no
`custody_rederivations` property, `contracts/manifest.yaml` still declares
`contract-v3.4`, and all **46 boxes** of `add-consent-custody-rederivation-record`
are unticked — ratification performed no realization and said so. The register
home does not exist at all: `models/content-address-families.yaml` is absent
from OpsxFactory's `main` AND from `change/add-content-address-integrity-gate`,
the branch that proposes it, where authoring it is task 2.1.

**And this change has nothing to sequence behind.** `code_surface: none` means
it archives ON LANDING, so its requirements reach canon the day it merges,
before either home exists. A refuse-on-landing reading of "a family that
declares no rule has not earned a pin" would therefore refuse EVERY
pinned-target edit in the estate from that moment — including the routine
lifecycle-header discharge that the neighbouring ADDED requirement and
*Proposal packets carry the lifecycle header* both require to be performed, and
including the very repairs F.1 and F.2 are sequenced to make. The requirement
therefore REPORTS an edit whose family has declared no rule, naming the family
and the home that owes it, and becomes a REFUSAL for that family the day it
declares. **The refuse-outright reading is recorded in `design.md` D-7 as
Brett Heap's veto point**: taking it is coherent and it freezes the corrective
work until the first family declares.
