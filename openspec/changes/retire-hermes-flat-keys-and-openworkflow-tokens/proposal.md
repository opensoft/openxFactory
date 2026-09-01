---
code_surface: openxFactory. (1) `scripts/validate-domain-factory.py` — the `LEGACY_HERMES_KEYS` nine-key map at `:60-70` and the `else` fallback branch of `check_hermes` at `:189-200` (the warn line, the flat-key resolution loop, and the per-role resolvability check that follows it) are REPLACED BY ONE EXPLICIT ERROR naming the missing or non-list `hermes.layers` -- **replaced, not merely deleted**, because the `hermes.layers missing required role` errors sit INSIDE the `layers`-declared branch and a bare deletion would let a `layers`-less stack pass with no finding at all; the `if token.startswith("openworkflow")` branch at `:309-311` is DELETED, so the `elif token not in allowed` arm at `:312-314` it shadows becomes the only arm; the docstring line at `:26` (`"openworkflow_*" tokens are flagged as deprecated naming.`) goes with it. (2) `scripts/apply-domain-starter.py` — the comment at `:241` naming a spent removal target and the nine emitted flat keys at `:242-250` leave the `stack.yaml` template, so a newly instantiated domain repository carries `hermes.layers` alone. (3) `docs/contract-versioning-policy.md` (RELEASE-SURFACE INVENTORY MEMBER) — the `openworkflow`-prefixed token entry moves to § Deprecations Executed, its declared shape CORRECTED to the prefix the code matches; the `hermes` flat-key entry SPLITS, an Executed row for the fallback read and a rewritten In Force entry for the keys themselves carrying the full refusal list, a restated removal target and the recorded reason it stays. (4) `contracts/CHANGELOG.md` (member) — the `contract-v3.0` BREAKING entry with its migration note and its discharge of all three Breaking-clause preconditions. (5) `contracts/manifest.yaml` (member) — `contract_bundle_version` and `contract_schema_version`. (6) A new `contracts/releases/contract-v3.0.digests.yaml`. NO consumer `stack.yaml` is edited by this change, in any of the five supported domain repositories: the half that would have required it is the half that is not executed. NO schema under `contracts/schemas/` changes, and no digested schema artifact moves. The sibling `retire-doxbench-chat-turn-v1` carries the schema-moving half of the same major and is a separate packet.
target_release: contract-v3.0 — a MAJOR, and naming it is not the reservation the policy forbids. `docs/contract-versioning-policy.md` § Version Identity forbids reserving a MINOR number before merge order is known; a major is deterministic from the declared bundle (`contract-v2.5`) and is already named as a forward target by the In Force entry `add-binding-consumer-identity` landed on 2026-08-31 ("The block is DECLARED at contract-v2.4 and CONSTRAINED at contract-v3.0"). THIS CHANGE HAS A CODE SURFACE, so under `release-realization` it archives ONLY on merged plus green realization evidence — never on landing — and its evidence includes the published annotated `contract-v3.0` tag verified from an independently refreshed checkout, because `docs/contract-versioning-policy.md` holds that a bundle is not published until its tag exists. The cut is a SEPARATE act from this proposal and from its realization; this packet neither performs it nor claims a place in its ordering beyond the class its retirements carry.
Status: draft
Proposed: 2026-09-01
Origin: openxFactory issue #522, filed against the three `contract-v2.0`-targeted deprecations that outlived their target; measured 2026-08-31 in a decision memo named `deprecations-522-memo-2026-08-31.md`, held on the operator's own machine and DELIBERATELY NOT COMMITTED anywhere in this repository (Principle IV forbids a host-absolute path in a committed file, so it is named and not located; the durable in-repo referents are issue #522 and its 2026-09-01 ruling comment, which carry the ruling this packet executes); RULED by Brett Heap 2026-09-01 in session and recorded as a comment on #522 — "execute all three retirements at contract-v3.0, as the memo recommends", entry 1 SPLIT, entry 2 EXECUTED, entry 3 executed as its own slice. The ruling authorizes the proposals; it does not ratify this text.
---

# Proposal: retire-hermes-flat-keys-and-openworkflow-tokens

## Why

**`contract-v2.0` shipped, executed a deprecation through itself, and did not
look at the three deprecations that named it.** That is the finding issue #522
raises and the memo sharpens. On 2026-08-27 the major arrived and correctly
retired the eight openxWallet contracts deprecated one minor earlier at
`contract-v1.47`, writing the estate's one worked `Deprecations Executed` row.
Three older entries — the `hermes` flat keys, the `openworkflow_` layer/owner
tokens, and the doxBench chat-turn v1 family — all named `contract-v2.0` as
their removal target, and all three were simply not looked at. Five minors
later the declared bundle is `contract-v2.5` and all three still sit in
§ Deprecations Currently In Force naming a version that is one major and five
minors in the past.

**This packet carries the first two.** The third,
`retire-doxbench-chat-turn-v1`, is a separate proposal authored the same day
from the same ruling, on the memo's own recommendation that it be sliced
separately: it moves a digest-pinned schema's bytes, twelve packaged fixtures,
a byte-identity baseline test and a server fallback posture, where these two
move validator code and the policy rows that describe it.

**The mechanism's closing side is not unproven — it was exercised once and then
not used.** That distinction matters to the remedy. What is missing is not a
capability but an obligation: nothing in promoted canon says a deprecation must
be executed at the major it targets or restated, and nothing says an entry that
reaches its target and is deliberately NOT executed must record why. This change
promotes both, in the mechanism's own vocabulary, and then discharges them
against these two entries.

Cited in full: openxFactory issue **#522** and Brett Heap's ruling comment on it
of **2026-09-01**; the measurement memo
**`deprecations-522-memo-2026-08-31.md`**, measured against
main tip `4290cad2`. **That path is OPERATOR-LOCAL and the memo is deliberately
NOT committed to this repository**; it is cited because it is the measurement the
ruling adopted, and the DURABLE in-repo referents a later reader can resolve are
issue #522 and its 2026-09-01 ruling comment.

## What the measurement found, and where it did not survive re-verification

Re-measured on this branch against main tip `1a69b7cb`. **The memo's facts for
these two entries hold, and re-verification adds FIVE findings it did not
carry — one of them raised in review of this pull request.**

**Entry 1 — `hermes` flat keys. Confirmed.**

* `LEGACY_HERMES_KEYS` at `scripts/validate-domain-factory.py:60-70` carries
  **nine** keys — `subject_overlay`, `subject_layer_name`, `customer_overlay`,
  `customer_layer_name`, `client_overlay`, `client_layer_name`,
  `care_organization_overlay`, `domain_overlay`, `domain_layer_name`. The policy
  entry names **five**. `scripts/apply-domain-starter.py:242-250` emits **nine**,
  three of which (`domain_agent_mixes`, `client_agent_mixes_template`,
  `customer_agent_mixes_template`) appear in neither list. The entry
  under-declares its own scope, which is the exact failure
  `add-binding-consumer-identity`'s entry articulates and guards against.
* `check_hermes` reaches its warning ONLY in the `else` branch taken when
  `hermes.layers` is absent (`:189-200`). Every supported consumer declares
  `layers`, so the branch is dead for the whole supported population and the
  warning has never fired against any of them.
* `scripts/apply-domain-starter.py:241` still carries the comment
  `# Deprecated flat keys (removal at contract-v2.0); kept for older tooling.` —
  openxFactory's own generator writing the deprecated shape into every new
  domain, under a target that is spent.
* **Re-verified independently against all five supported consumers** (read-only,
  from the aggregation checkout, 2026-09-01): every one declares `hermes.layers`
  AND carries co-resident flat keys — codexFactory `domain_overlay`,
  `subject_layer_name`, `subject_overlay`; MedxFactory those plus
  `care_organization_overlay`; AdxFactory and LedgerxFactory the same three;
  OpsxFactory all six of `client_layer_name`, `client_overlay`,
  `customer_layer_name`, `customer_overlay`, `domain_layer_name`,
  `domain_overlay`. The memo's table reproduces exactly.
* **The retirement is a REPLACEMENT, not a deletion, and the difference decides
  whether it narrows or widens.** The `hermes.layers missing required role`
  errors at `:186-188` sit INSIDE the `if isinstance(declared, list)` branch.
  Delete the `else` arm and nothing else, and a `layers`-less stack falls
  straight through to `for role, layer in layers.items()` with an EMPTY map,
  producing no finding at all — a SILENT WIDENING at a major, the exact opposite
  of the retirement. The removal therefore owes a stated replacement behaviour:
  one explicit error naming the missing or non-list `hermes.layers`. Neither the
  memo nor the issue named this, and it is the single easiest way to realize this
  entry wrongly.
* **A precision the memo did not state, and which the refusal list must carry.**
  `domain_overlay` is ALSO a live, non-deprecated key under the `omnigent:`
  block — every one of the five declares `omnigent.domain_overlay`, and the
  validator reads it at `scripts/validate-domain-factory.py:539-541`, erroring
  when the directory it names is missing. The deprecated key is `hermes.domain_overlay` and
  nothing else. A refusal list written by key NAME rather than by key PATH would
  refuse a shape every supported consumer legitimately carries, at a major, with
  no warning ever served for it. Named here so no realization discovers it.

**Entry 2 — `openworkflow`-prefixed tokens. Confirmed, with TWO properties the
memo did not name.**

* The surface is `scripts/validate-domain-factory.py:309-311` plus the docstring
  line at `:26`. It is an `if` that PRECEDES the general `elif token not in
  allowed` at `:312-314`, and therefore shadows it.
* **The shadowing cuts both ways, and this proposal states it.** Any token
  beginning `openworkflow` takes the branch — including one whose normalized
  form equals a declared Hermes layer's normalized display name, which the
  general rule would accept. Removing the branch therefore NARROWS the
  unresolvable case and WIDENS the resolvable one. The memo priced only the
  narrowing.
* **Entry 2's entry ALSO under-declares its own shape, by exactly one
  character** (raised in review of this PR, 2026-09-01). The policy entry reads
  *"Layer/owner tokens beginning `openworkflow_`"* and the validator docstring
  agrees; the code reads `token.startswith("openworkflow")`, with no trailing
  underscore. `openworkflow`, `openworkflowx` and `openworkflow-legacy` all take
  the branch today and are all refused by the removal, and none of them is the
  shape the entry declares. **This is the same defect as entry 1's seven
  undeclared keys, one character wide**, and it makes the refusal-list rule this
  packet promotes apply to BOTH of its entries rather than only to the flat keys.
* **A canon/code divergence the memo did not measure, and which this change
  records rather than resolves.** Promoted canon —
  `openspec/specs/workflow-gate-contract/spec.md:48`, "Owner layer constraint" —
  says an `owner_layer` matching neither a canonical role nor a declared layer id
  *"SHALL be reported as a validator warning"*. The shipped validator reports it
  as an **error**, and has since `493fb33d` (2026-07-03), six days BEFORE that
  requirement was promoted (`a1a2802b`, 2026-07-09). This change does not fix
  that: the fix moves every unresolvable token, not the retired prefix, and it is
  a different change's subject. See § Orchestrator Decisions D4.

**What no promoted capability owns.** Grepped across `openspec/specs/`: the
strings `Deprecations Currently In Force` and `Deprecations Executed` appear in
**zero** promoted requirements. No capability owns the deprecation lifecycle;
`docs/contract-versioning-policy.md` is a ratified governance document cited
piecemeal (once, by `neutral-product-pin`). Nothing in promoted canon names the
`hermes` flat keys, `LEGACY_HERMES_KEYS`, `hermes.layers`, or the `openworkflow`
token. That absence is why this packet ADDS a capability rather than modifying
one.

## What Changes

- **ADD the capability `contract-deprecation-execution`** — four requirements:
  the execute-or-restate rule; the refusal-list rule with its unwarned-shape
  corollary; and one requirement per retirement, each carrying scenarios in BOTH
  directions (the shape now refused or absent, and the previously-warned path).
- **EXECUTE, at `contract-v3.0`, the phased half of entry 1** — delete the
  fallback read in `check_hermes` and the `LEGACY_HERMES_KEYS` map it uses, and
  stop `apply-domain-starter.py` emitting the deprecated keys.
- **RECORD-WHY the refusing half of entry 1** — the co-resident flat keys stay
  In Force, in the mechanism's own section, with the full refusal list, a
  restated removal target, and the measured reason: the warning has been dead
  code for the entire supported population, so refusing the keys would be an
  unphased narrowing that owes its own deprecating minor first.
- **EXECUTE, at `contract-v3.0`, entry 2** — delete the `openworkflow` branch
  and the docstring line, and move the entry to § Deprecations Executed.
- **Repair the two entries' stale line-number citations** (`:250-254`, now at
  `:301-305`) by citing the heading, per the memo's ride-along.

## What this change does NOT do

- **It does not cut `contract-v3.0`.** The cut is its own act under
  § Bundle Realization Order, with the version allocated at realization, every
  gate run against an unchanged candidate, and the annotated tag published and
  verified from a refreshed checkout. This packet declares the class and the
  target; it performs neither.
- **It does not edit any consumer `stack.yaml`.** Nothing it executes refuses
  what the five supported consumers carry.
- **It does not touch the doxBench chat-turn family.** That is the sibling.
- **It does not propose the `deprecation-target-currency` doc-health family.**
  The memo designs one and sequences it behind PR #544 and behind these
  retirements; commissioning it is a separate proposal, and the memo's own
  calibration argument ("a check that lands red teaches readers to ignore it")
  is why it follows rather than leads.
- **It does not resolve the `Owner layer constraint` severity divergence.**
  See D4.

## Capabilities

### New Capabilities

- `contract-deprecation-execution`: the obligation that a deprecation is
  executed at the major it targets or restated with the reason it stays; the
  rule that an entry is written from the refusal list and that a shape whose
  warning never fired is not phased; and the two retirements this change takes,
  each with its both-direction behaviour at the major.

### Modified Capabilities

**None, and the absence is measured rather than assumed.** No promoted
requirement names either shape, so there is no canon this change falsifies and
no `## MODIFIED Requirements` block to write. It follows that #538's
base-declaration convention (`govern-sibling-added-modified-deltas`, ratified
2026-08-31) does not apply here: that convention governs a MODIFIED block whose
requirement exists only as an active sibling's ADDED, and this packet carries no
MODIFIED block at all. The sibling `retire-doxbench-chat-turn-v1` DOES carry one,
over promoted canon, and declares its own basis accordingly.

## Impact

- **Refuses nobody at the major.** All five supported DomainxFactory
  consumers — codexFactory, MedxFactory, AdxFactory, LedgerxFactory,
  OpsxFactory — declare `hermes.layers`, so none exercises the removed fallback;
  none carries an `openworkflow`-prefixed `owner_layer` in any workflow gate.
  Both facts were re-verified read-only on 2026-09-01: `openworkflow` occurs in
  openxFactory in exactly TWO code positions, the docstring line and the branch
  itself, and in ZERO positions across the five consumer repositories. Four of
  the five are pinned below `contract-v2.0` and, under § Compatibility Direction,
  stay valid at their pins regardless.
- **Widens one case.** A gate whose `owner_layer` begins `openworkflow` AND
  resolves to a declared layer stops being warned. No such gate exists today in
  any reachable repository; the widening is stated because it is real, not
  because it bites.
- **Release surface.** Four inventory members move
  (`docs/contract-versioning-policy.md`, `contracts/CHANGELOG.md`,
  `contracts/manifest.yaml`, and the new
  `contracts/releases/contract-v3.0.digests.yaml`). No schema's bytes move, so
  no digested schema artifact's `sha256` changes on account of this packet.
- **`scripts/validate-domain-factory.py` is a manifest artifact
  (`domain-factory-conformance-validator`) and is NOT currently an inventory
  member.** Stated so the cut does not discover it late.

## Orchestrator Decisions

**D1 — the split is executed as ruled, and both halves land in one cut.**
Brett's ruling of 2026-09-01 splits entry 1: execute the fallback read's
retirement, record why the keys stay. Both halves are written into
`docs/contract-versioning-policy.md` by the SAME cut, because a cut that
executed half an entry and left the other half naming `contract-v2.0` would
reproduce the defect #522 was filed about, one entry smaller.
*Alternative not taken:* record-why in a following minor. Rejected — the entry
would name a spent target across the major.

**D2 — the restated removal target is `contract-v4.0`, conditioned on the
deprecating minor it owes.** The refusing half needs a target that parses and
that lies ahead of the declared bundle; leaving it targetless makes the
deprecation unenforceable, which the *Deprecating (minor)* class forbids on its
own terms. `contract-v4.0` is the next major after the one this change lands at,
and the restatement names the precondition explicitly: a deprecating minor in
which `check_hermes` warns on the co-resident shape *whether or not* `layers` is
present, written from the full refusal list. If that minor has not been cut when
`contract-v4.0` is reached, the entry is restated AGAIN rather than the removal
taken unphased — which is exactly the rule R1 promotes.
*Alternative not taken:* declaring the keys permanently tolerated vestigial and
retiring the entry. The memo names it a legitimate ruling; Brett did not take it,
ruling "not this, not yet" rather than "not ever", and this packet does not
convert his ruling into a broader one.

**D3 — the entry is rewritten from the refusal list in the same cut, whichever
half executes.** Nine keys in `LEGACY_HERMES_KEYS`, three more emitted by the
starter, five named in the policy. The under-declaration is a defect of the
entry, not of the cut, and it is repaired regardless of the split.

**D4 — the `Owner layer constraint` canon/code severity divergence is RECORDED
AND NOT RESOLVED here.** Canon says warning; the shipped validator has errored
since before the requirement was promoted. Resolving it means moving every
unresolvable `owner_layer` token, in every domain repository, at whatever
severity is ruled — a strictly larger subject than a four-line retirement, and
one whose answer this packet has no measurement to support. The retirement's
Breaking class does not depend on it: the policy's Breaking clause is *"a shape
is removed"*, and the `openworkflow`-prefixed token is removed from the
validator's accepted vocabulary whatever the fall-through's severity turns out
to be. The requirement this packet adds therefore names no severity for that
fall-through and defers to whatever the general rule carries.
*Task:* file the divergence as its own issue at proposal time (§ 6.1), so the
record exists whether or not this packet is ratified.

**D5 — no doc-health family is proposed.** Following the memo's sequencing and
#544's own calibration principle. The three findings such a family would emit on
the day it lands are the subject of these two packets and the sibling; a check
authored ahead of them lands red on work already commissioned.

## Open Questions

- **OQ-1 — does `contract-v3.0` carry both retirement packets, or one?** They
  are independent by construction: neither is a precondition of the other, and
  the cut may carry either alone. Sequencing is the cutting session's, not this
  proposal's.
- **OQ-2 — is `contract_schema_version` incremented?** § Version Identity says
  major increments occur together with it. Whether a validator-only removal that
  moves no schema byte increments the per-file integer, or only the bundle's, is
  a question for the cut; it is named here so the cut does not have to discover
  it. The sibling packet, which DOES move schema bytes, meets the same question
  from the other side.
- **OQ-3 — does the restated entry's `contract-v4.0` target survive review?**
  D2 picks it as the honest default. A reviewer who prefers "no numeric target
  until the phasing minor is cut" is arguing against the *Deprecating (minor)*
  class's own requirement to state one, and should say so explicitly.
