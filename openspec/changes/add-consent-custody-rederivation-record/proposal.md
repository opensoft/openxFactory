---
code_surface: openxFactory — NOT `none`, and the distinction is load-bearing. This packet's own diff is spec text and bookkeeping, but its realization moves four openxFactory surfaces and the change MUST NOT archive until they are merged and green: (1) `contracts/schemas/consent-instrument.schema.yaml` — ONE new top-level sibling property, `custody_rederivations`, closed per entry, plus `contract_schema_version: 2 -> 3`; the `custody` object itself is not touched, gains no property, and keeps `additionalProperties: false`; (2) `scripts/validate-consent-instruments.py` — the canonical validator gains the INTERNAL-LINKAGE legs of the chain rule (first link equals the pin, each later link equals its predecessor's observed digest, declared order is chronological, no entry rewrites `custody.sha256`) and NOT the git re-derivation legs, which belong where the target lives; (3) `examples/consent-instrument/` and `examples/consent-instrument/negative/` — positive and negative fixtures, one per refusal the rule names; (4) the release surface — `contracts/manifest.yaml` (the `consent-instrument` row's `sha256`, today `13b0fe46…`, and its `consumption_rule`), `contracts/CHANGELOG.md`, `contracts/releases/<version>.digests.yaml` and the annotated tag. NO consumer file is written by this change: OpsxFactory's re-pin, its worker-enrollment-broker lockstep, and the three instruments' entries are named in § *Impact* as the CONSUMER'S owed acts and are outside this change's archive gate.
target_release: THE NEXT ADDITIVE MINOR, DELIBERATELY NOT NUMBERED HERE — allocated AT THE CUT by merge order per `docs/contract-versioning-policy.md` § *Bundle Realization Order* step 1, which forbids a proposal reserving a minor before merge order is known. The count was MEASURED at this branch's merge-base rather than remembered: `contracts/manifest.yaml:3` declares `contract_bundle_version: contract-v3.4` and `contracts/releases/` holds `contract-v3.4.digests.yaml` as its highest inventory, so the next additive minor is `contract-v3.5` **as things stand at authoring** and is neither reserved nor claimed by this text. The version number is a row-4 substrate on issue #630 and is claimed there AT CUT TIME, as its own task (§ 5.1), never here. Per `release-realization` a non-empty code surface archives on merged-plus-green realization evidence rather than on landing.
sequenced_after: [add-consent-instrument]
---

# Proposal: add-consent-custody-rederivation-record

Status: draft
Proposed: 2026-09-07
Awaiting ratification: Brett Heap (repository owner). **NOTHING IN THIS PACKET
IS RATIFIED.** The F.1 ruling below chose the repair FORM and ordered this
authoring; it did not approve a field name, an enum member, a closure posture,
a chain rule or a validator split. Those are design decisions C-1..C-8 and each
is a veto point.
Lane: opsXfactory-1

Origin: OpsxFactory PR **#248** (merged `40aaa93b`), ruling comment
[5571629298](https://github.com/opensoft/OpsxFactory/pull/248#issuecomment-5571629298)
— Brett Heap, 2026-09-07T13:51Z, in session, first-hand to lane opsXfactory-1.
Ruling **F.1**, verbatim: *"Bump the openxFactory instrument schema first"* —
*"a structured custody-history block is added to the consent-instrument
contract in openxFactory, a contract version is cut, OpsxFactory re-pins
(lockstep with the worker-enrollment-broker re-pin), and only then the three
instruments take their `amendments` entries plus the structured block."* The
ruling states its own exposure: *"F.1's repair now waits on a cross-repo
contract cut and re-pin; the sidecar-register and prose-sentence forms were
declined."*

Lane claims, posted before authoring under Lane Collision Protocol Amendment 1
Rule 7, both on openxFactory issue
[#630](https://github.com/opensoft/openxFactory/issues/630): the CHANGE claim at
[5571680046](https://github.com/opensoft/openxFactory/issues/630#issuecomment-5571680046)
and the row-3 README **SUBSTRATE CLAIMED** at
[5571680388](https://github.com/opensoft/openxFactory/issues/630#issuecomment-5571680388),
both 2026-09-07T13:55Z, lane opsXfactory-1. The row-4 CONTRACT-CUT substrate —
the version number — is **not** claimed by either and is claimed separately at
cut time (§ 5.1).

## Why

**Three of four executed OpsxFactory consent instruments carry a
`custody.sha256` that no longer proves its target, and the contract has no
place to say so.** The measurement is OpsxFactory's, taken 2026-09-06 at
`ddc03ad7` by `sha256sum` over each instrument's `custody.locator` target, and
recorded in
`openspec/changes/add-pre-archive-citation-gate/supporting-docs/owed-findings.md`
§ F.1 — **(archive in flight; the live path until then is
`openspec/changes/add-pre-archive-citation-gate/supporting-docs/owed-findings.md`
at OpsxFactory main `40aaa93b`.)** That packet archives 2026-09-07 by ruling,
landing before this one, after which the same register is cited at
`openspec/changes/archive/2026-09-07-add-pre-archive-citation-gate/supporting-docs/owed-findings.md`:

| Instrument | Pinned | At HEAD | Verdict |
| --- | --- | --- | --- |
| `opsx-farheap-node-inventory-reader-consent.yaml` | `55b97d77…` | `55b97d77…` | MATCH |
| `opensoft-exchange-monitor-reader-consent.yaml` | `bb8f89ea…` | `5c87d547…` | **BROKEN** |
| `opsx-farheap-service-discovery-reader-consent.yaml` | `b5d4ab55…` | `d9eecee3…` | **BROKEN** |
| `opsx-opensoft-node-inventory-reader-consent.yaml` | `31e4f889…` | `7fc4bb21…` | **BROKEN** |

**ALL THREE BROKE AT ONE COMMIT AND THE CAUSE IS RULED, WHICH IS WHY THIS IS A
CONTRACT PROBLEM AND NOT A REPAIR JOB.** OpsxFactory `57fd9fd2` (2026-08-24,
*"Discharge all 55 lifecycle-header defects in the OpenSpec scan set"*) wrote 16
files under `openspec/changes/archive/` and inserted ONE `Ratified:` line into
targets that were pinned. **The shape is corrected from an earlier draft of this
proposal, which said `Status:` header** — the commit's own message and
`git show 57fd9fd2 -- <target>` both read a single `+Ratified: 2026-07-10 — …`
line per file, derived from headers the page already carried. The finding is
unchanged and so are the enum members it grounds (`diff_class: header_only`,
`reason: lifecycle_header_edit`): the edit added a lifecycle header line and
changed no other byte. The edit was performed under a ratified convention —
OpsxFactory `docs/packet-lifecycle-headers.md` § *Editing an archived packet*
(Status: ratified, 2026-08-24, Brett Heap) — which requires only a bookkeeping
note. **The content did not change.** Re-derived at `57fd9fd2^` every one of the
three still hashes to its pin. And the correlation is with the header edit
rather than with archiving at 3 of 3: the one pin that still matches is the one
`57fd9fd2` did not touch, and one of the three broken targets sits in a change
directory that has **never been archived**.

**So a true instrument and a true ruling now contradict each other, and the
contract cannot represent the reconciliation.** The instrument says "this
digest proves that document". Git says the document's bytes moved. The ruling
says the move was authorized and the content is unchanged. Today the only
places to put that third fact are `amendments[].delta` — free prose, which no
checker can read — or nowhere.

**The repair the ruling chose needs a machine-checkable record, because the
gate that will consume it is already ruled.** The same session ruled **F.2
scope** — *"Every in-repo sha256 pointer to an in-repo target"* — one
custody-digest gate over all content-address pins OpsxFactory holds, each with
its family's re-derivation rule. A gate that must decide whether a divergence
is admitted cannot read a sentence. It needs the pin it started from, the
commit at which the bytes moved, the digest observed there, and the record that
authorized accepting it — each leg re-derivable from git history, so that the
record is an INDEX INTO THE EVIDENCE rather than a claim standing in place of
it.

## What Changes

**ONE new top-level property on `xfactory_consent_instrument`, closed per
entry, and a `contract_schema_version` bump.** Nothing else in the schema moves.

- **`custody` IS NOT TOUCHED.** It stays exactly `{locator, sha256}` with
  `additionalProperties: false`, by ruling **D9** (`add-consent-instrument`
  design.md § D9; the schema's own comment: *"CLOSED on purpose … there is no
  property the signed original's content could occupy"*). Growth goes to a
  SIBLING, because the argument for D9's closure is that no property may exist
  in which content could hide, and a history array inside `custody` would be
  exactly such a property.
- **`custody_rederivations`** — an array of closed entries, each carrying
  `at`, `commit`, `previous_locator`, `observed_locator`, `previous_sha256`,
  `observed_sha256`, `diff_class`, `reason`, `ruling_ref`, `recorded_by`. All
  TEN required; `additionalProperties: false` per entry; `diff_class` and
  `reason` closed enumerations.
- **A DECLARED CUSTODY STORE MAPPING is required of the consuming repository.**
  `custody.locator` is opaque and is NOT a path — every OpsxFactory locator
  carries an `opsx:opensoft/` scheme prefix, and three of the four targets
  resolve at NO ref under their literal path because they moved when their
  packets archived. The neutral contract states the obligation and refuses an
  unresolvable locator; the mapping itself is the consumer's declared policy
  (OpsxFactory's is `opsx:<tenant>/<repo-relative path>`).
- **NO `amendments` ENTRY IS WRITTEN.** A re-derivation is not an amendment and
  does not transition the instrument's status.
- **`contract_schema_version: 2 -> 3`**, ADDITIVE. An instrument that declares
  no `custody_rederivations` stays valid unchanged — which is the whole estate
  today, all four OpsxFactory instruments included. The RECORD envelope's
  `schema_version` stays `const: 1`, on the reasoning the schema already
  carries for the 1 -> 2 bump: changing it would invalidate every instrument in
  the estate, which is the opposite of additive.
- **A stated GATE RULE**, promoted as a requirement: custody is CURRENT iff the
  target hashes at HEAD to `custody.sha256`, or the declared chain from the pin
  to the last observed digest is unbroken in BOTH digest and locator, every link
  re-derives from git history AT BOTH PATHS (starting locator at `commit^`,
  observed locator at `commit`), and every commit is an ANCESTOR of the next and
  of HEAD. A chain that cannot be re-derived is a **REFUSAL, never an
  admission**, and a `diff_class: content` entry WITHHOLDS the verdict rather
  than buying currency — a moved referent is grounds for re-execution.
- **The canonical validator gains the INTERNAL legs and not the git legs.**
  `scripts/validate-consent-instruments.py` is network-free and reads ONE
  repository; the instrument's `custody.locator` target lives in the CONSUMER's
  repository. So the neutral validator checks the chain's internal consistency
  (linkage, order, no rewritten pin, closed enums) and the consumer's
  custody-digest gate performs the re-derivation where the bytes are. Both legs
  are named in the requirement; neither is left implicit.

## The shape proposed

**Example A — the bytes moved, the path did not.** The instrument is
`opsx-opensoft-node-inventory-reader-consent.yaml`, and its locator is quoted
VERBATIM from the record, scheme prefix included. Its target has never been
archived, so both locators are equal.

```yaml
custody:                      # UNCHANGED, still closed to exactly these two
  locator: "opsx:opensoft/openspec/changes/add-managed-node-inventory/review/ratification-2026-07-10-r2.md"
  sha256: "31e4f889…"         # THE PIN — never rewritten, ever

custody_rederivations:        # NEW sibling; absent on every existing instrument
  - at: "2026-09-07T14:00:00Z"
    commit: "57fd9fd2…"                 # 40 hex: where the target changed
    previous_locator: "opsx:opensoft/openspec/changes/add-managed-node-inventory/review/ratification-2026-07-10-r2.md"
    observed_locator: "opsx:opensoft/openspec/changes/add-managed-node-inventory/review/ratification-2026-07-10-r2.md"
    previous_sha256: "31e4f889…"        # == custody.sha256 (first entry)
    observed_sha256: "7fc4bb21…"        # the target AT that commit
    diff_class: header_only             # closed: header_only | content
    reason: lifecycle_header_edit       # closed: lifecycle_header_edit |
                                        #   archive_move | other_ruled_edit
    ruling_ref: "docs/packet-lifecycle-headers.md § Editing an archived packet"
    recorded_by: "lane opsXfactory-1, OpsxFactory PR #<n>"
```

**Example B — the path moved and the bytes did not**, which is the case a
single-locator rule can never admit. `opsx-farheap-node-inventory-reader-consent.yaml`
is the instrument whose pin still MATCHES by content, and whose target moved
when `add-managed-service-mapping` archived on 2026-08-26:

```yaml
custody:
  locator: "opsx:opensoft/openspec/changes/add-managed-service-mapping/proposal.md"
  sha256: "55b97d77…"

custody_rederivations:
  - at: "2026-09-07T14:00:00Z"
    commit: "<the archive commit>"
    previous_locator: "opsx:opensoft/openspec/changes/add-managed-service-mapping/proposal.md"
    observed_locator: "opsx:opensoft/openspec/changes/archive/2026-08-26-add-managed-service-mapping/proposal.md"
    previous_sha256: "55b97d77…"        # resolved at commit^, at the OLD path
    observed_sha256: "55b97d77…"        # resolved at commit, at the NEW path
    diff_class: header_only             # no byte changed; only the path did
    reason: archive_move
    ruling_ref: "<the archive act's record>"
    recorded_by: "lane opsXfactory-1, OpsxFactory PR #<n>"
```

## Readings not taken

Each with the measured reason it was refused, so a later reader does not
re-litigate a settled choice or mistake a refusal for an oversight.

1. **Grow `custody` itself** — refused by **D9**. The closure's argument is
   that no property may exist in which the signed original's content could sit,
   and the canonical validator enforces it by walking every string under
   `custody` for blob shapes (`check_custody`, `walk_strings`). An array of
   objects there would be new ground for that walk with no compensating gain:
   the sibling carries the same facts at the same level of the record.
2. **Prose in `amendments[].delta`** — **the form Brett declined.** It is the
   *"prose-sentence"* option named in the F.1 ruling as declined. It is not
   machine-checkable: a gate cannot read "the header edit of 2026-08-24 moved
   this target" and re-derive anything from it, so the divergence would be
   recorded and still unverifiable. The `amendments` entry is still owed by the
   consumer — the ruling asks for both — but it is the human-readable half.
3. **A sidecar register in the consumer repository** — **declined in the same
   ruling.** It splits one fact across two files with no contract binding them:
   an instrument could be copied, cited or cascaded without its register, and
   nothing in the neutral shape would notice. The record belongs on the record
   whose key it qualifies.
4. **Rewrite `custody.sha256` to the observed digest** — refused, and this is
   the one a hurried repair reaches for first. It rewrites an EXECUTED
   instrument's key: the pin is the half of the custody pair that proves the
   pointed-at original, and moving it destroys the only evidence that a
   divergence ever occurred while producing a record that verifies. It also
   contradicts `add-pre-archive-citation-gate`'s STOP-and-report discipline,
   which explicitly refused to write an assertion the mismatch would falsify.
5. **A neutral gate in openxFactory that re-derives the digests** — not taken
   HERE, and named so it is not read as forgotten. openxFactory holds no
   consent instruments; the targets live in consumer repositories. The neutral
   contract defines the RULE and the internal legs; F.2's gate is OpsxFactory's
   act under its own ruling.

## Impact

**Affected capability:** `consent-instrument` — one `## MODIFIED` requirement
(*The Signed Original Never Enters A Product Repo*) and one `## ADDED`
requirement (*Custody Currency Is Re-Derived From Git History Or Refused*).

**Affected contract:** `contracts/schemas/consent-instrument.schema.yaml`
(`contract_schema_version: 2 -> 3`, one added top-level property). The
`consent-instrument-class-registry` schema is NOT touched: nothing in this
change reaches class declarations, status aliases or evidence kinds.

**Affected release surface:** `contracts/manifest.yaml` (the `consent-instrument`
row's `sha256` and `consumption_rule`), `contracts/CHANGELOG.md`,
`contracts/releases/<version>.digests.yaml`, and the annotated tag.

**Consumers, named as THEIR owed acts and outside this change's archive gate:**

- **OpsxFactory** re-pins `stack.yaml` `contract_ref` (today the commit
  `724a2a4f…`) to the cut bundle's commit, **in lockstep with the
  worker-enrollment-broker's runtime-shape validation** — the `pin_gap_misdeclared`
  guard means an advance that moves the pin without re-validating the broker's
  declared shape fails closed. Then, and only then, the three broken instruments
  take a `custody_rederivations` entry each — **and NO `amendments` entry**: the
  structured record IS the record, and writing an amendment would transition
  three EXECUTED instruments to `amended` under the promoted requirement
  *Amendments Are Transitions, Never New Instruments* for a change in nothing
  the parties agreed. The fourth instrument is left alone because its content
  pin is not broken, though its locator DID move at archive and a future entry
  may record that.
- **F.2's custody-digest gate** (OpsxFactory, scope *"every in-repo sha256
  pointer to an in-repo target"*) consumes this record for the consent-custody
  family. This change does not build it and does not schedule it.
- **Every other domain** is unaffected: the growth is additive, no existing
  instrument declares the array, and no conformance declaration changes.

## Sequencing

This packet declares `sequenced_after: [add-consent-instrument]` — ONE parent,
archived 2026-08-06, and the declaration is MEASURED rather than chosen. An
explicit `[]` root claim was written first and then withdrawn: the corpus sweep
classifies this change as a **co-modifier**, and `add-sequenced-after-substrate`'s
scenario *A root claim is contradicted by a co-modifier* refuses exactly that
pairing. The co-modifier was then identified rather than assumed — a grep of the
whole change corpus for the requirement title returns `add-consent-instrument`'s
delta and nothing else — so the parent is named. **Depth 1** — the parent
declares nothing itself, so the chain is one hop, which is the ledger's own
definition and the figure its row carries.

`add-consent-instrument` is the right parent for the reason the field exists.
Its outcome IS the text this delta restates and grows: ruling D9's closure, the
promoted requirement *The Signed Original Never Enters A Product Repo*, and the
`contract_schema_version` discipline the bump follows.

**OpsxFactory's `add-pre-archive-citation-gate` is NOT a parent.** It RAISED the
finding and owns the register, and its own successor acts are DOWNSTREAM of this
contract rather than upstream of it. The ruling that ordered this authoring is an
authority, not a sequencing parent.

The cut is the serialization point, not this packet: § *Bundle Realization
Order* allocates the version LATE, at the final integration point, and
`release-tag-gate` refuses a cut standing on an earlier unpublished bundle. The
row-4 claim on issue #630 is therefore made by the cutting session (§ 5.1) and
not by this one.

## Ratification

Owed from Brett Heap, and the packet is inert until it arrives. Task 1.1. The
veto points are design decisions **C-1** (the sibling, not `custody`),
**C-2** (the name `custody_rederivations`), **C-3** (the eight fields, all
required), **C-4** (`diff_class` members), **C-5** (`reason` members),
**C-6** (the chain rule, the path pair, the ancestry leg and the refusal
posture), **C-6a** (locator resolution declared by the consumer, and the entry's
locator pair), **C-7** (the validator split — internal legs neutral, git legs at
the consumer, and the obligation to operate one), **C-8** (additive bump to
`contract_schema_version: 3` rather than a new record kind), **C-9** (a
`content` class withholds the verdict instead of buying currency), and **C-10**
(a re-derivation is not an amendment, so NO `amendments` entry is written).

**C-10 SUPERSEDES ONE CLAUSE OF THE F.1 RULING** — its *"their `amendments`
entries plus the structured block"* — and the supersession is named at the point
it is taken (`design.md` C-10) rather than quietly absorbed. The clause predates
the choice announced in the same sentence: the `amendments` entry was the prose
half of the form being replaced. Keeping it is Brett's to choose; the cost is a
false `executed → amended` transition on three instruments.

## What this proposal does NOT claim

- It does not claim the three broken pins are repaired. They are repaired by
  the consumer, after the cut and the re-pin, in OpsxFactory's own change.
- It does not claim `57fd9fd2` was wrong. It was ruled, and this contract's
  answer is to make the resulting divergence RECORDABLE and CHECKABLE rather
  than to relitigate the edit.
- It does not claim a version number. `contract-v3.5` is the measured next
  additive minor at authoring and is not reserved.
- It does not claim F.2's gate, F.3's archive-edit reconciliation, or the
  OpsxFactory-side half of the F.3 *"both at once"* ruling. Each is named
  where it is owed.
- It does not tick a box, move a schema byte, cut a release, or open a pull
  request in a consumer repository.
- It does not claim its first draft was right. An adversarial review found one
  BLOCKER (locator resolution was undefined, so `reason: archive_move` was
  unadmittable by construction and the worked example contradicted the finding)
  and four MAJOR defects (`diff_class: content` bought currency by omission; the
  instructed `amendments` entry would have transitioned three executed
  instruments; no ancestry leg; C-1's second leg argued backwards). Each is
  fixed above and each correction says what the earlier draft got wrong.
