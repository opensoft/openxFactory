# Research: `deliberation` — register entry two and its neutral return schema

**Feature**: [spec.md](./spec.md) | **Date**: 2026-09-04 | **Lane**: `hermes-wallet-exercise`

This file records WHERE EVERY AUTHORED VALUE CAME FROM, and — separately and
plainly — the handful of points the ratified text does not settle. **Nothing on
the second list was decided silently: each carries the most conservative reading
available, and each is flagged for the ratifier in the pull request.**

---

## R1. The realization is derivative by construction

No clarification round was run and none was needed. The ratified requirement
(`openspec/changes/admit-deliberation-clearing-operation/specs/clearing-dispatch-boundary/spec.md`)
fixes every fact of the entry, names the return's `kind`, names the three refusal
grounds AND the rule that renders them, and states WHICH COMPONENT EMITS WHICH.
`design.md` D4 rules the schema, D9 enumerates the five frozen copies and the
three pinned numerals, D13 supplies the emitter table. `tasks.md` Phase 2 is the
build list, each item stating the assertion it must satisfy.

Where this feature had a choice at all, it is on the second list below.

---

## R2. Where the return schema's fields come from

The ratified requirement's own words are the field list:

> emit the per-seat outputs as a STRUCTURED RETURN of evidence — seat identity,
> that seat's output, and the run identifiers that bind the return to the
> convening job id, the verified subject pin, and the inbound bundle digest it
> answers

and `tasks.md` 2.2 adds *"(inline payload or reference)"* and
*"`additionalProperties: false`"*, plus *"Declares no digest construction, no
handling vocabulary and no job envelope; it references the ones already in
force."*

**The producer-side grounding**, read at codexFactory PR #165 head
`b9714e2183d2e26a0f8023e47e3d00d8afc4245a`
(`openspec/changes/adopt-bundle-shaped-deliberation/`):

| neutral member | grounded in | quotation |
|---|---|---|
| the return exists at all, and is two artifacts on the producer side | design D3 | *"**Return members:** `seat_results.json` (UNSIGNED) and `return-manifest.json`."* |
| `binding.convening_job_id` | tasks 2.3 | *"Return manifest: per-file hashes, `convening_job_id`, `subject_pin`, `base_sha`, and the inbound `bundle_digest` it answers."* |
| `binding.verified_subject_pin` | tasks 2.3 (`subject_pin`); design D4 (the pin *"now taken from the admission stamp"*) | see R6 for the rename |
| `binding.inbound_bundle_digest` | design D1 leg 4 / tasks 5.3 | *"assert `return-manifest.bundle_digest` == the digest sealed at leg 1"* |
| `seats.<seat>.output` | design D6 | *"Leg 3 assembles `seat_results.json` … and stops."* — the per-seat material |
| the return is UNSIGNED and carries no signature member | design D6 | *"The host never holds a seat private half … No signature block, no runtime token exchanged on the host"* |
| `operation` | the ratified openxFactory entry | operation id `deliberation` |
| `lane` | the ratified openxFactory entry | ARTIFACT LANE ONLY |

**What was deliberately NOT lifted into the neutral shape.** #165 design D6 names
per-seat accounting members inside `seat_results.json` — `num_turns`,
`declared_turn_cap`, `model_usage`, `declared_model` — and return-level
`required_seats`, `base_sha`, `conditional_evidence`. None becomes a neutral
member. Two reasons, both from the ratified text: task 2.2 says **minimal**, and
D4's rejection of a producer-owned `output_schema_ref` is precisely a refusal to
let the producer author the shape its own return is checked against — a neutral
schema that enumerated the producer's accounting fields would be doing that from
the other side. They live INSIDE the seat's output, which this family carries
opaquely. (#165 design D14 separately places `base_sha` and `required_seats`
*"outside the signed payload"*, so lifting them would also have crossed a
producer-side signing boundary this entry has no business touching.)

---

## R3. `token_scopes: [actions:read]` — borrowed, not minted

Ratified design D6: the spelling is `credential-contracts`' own, carried in
`scripts/validate-credential-contracts.py` as
`DISPATCH_SCOPES = {"actions:write", "actions:read", "metadata:read"}`.
`metadata:read` is deliberately NOT declared — D6 records that on this provider a
token carries metadata read implicitly, so declaring it would describe the
provider's floor rather than a grant. **Entry one's empty list is not touched.**

## R4. `data_handling: internal-governance` — the attribution is the ratified one

Ratified design D7, checked against the shipped text: the FIELD's vocabulary is
`document-cataloging`'s as the register's own schema says; the CLASS NAME is the
`Handling:` header value the estate's governance corpus already travels under
(`document-lifecycle` / doc-health header family), and the handling authorization
the doc-health worker dispatch requires by default. `protected` would make the
operation undispatchable by its own declaration; `restricted` would over-declare.

## R5. `worker_profile: council-deliberation-worker` — register-local, chosen

Ratified design D5: `worker_profile` is register-local vocabulary (entry one's
`cpc-readonly-probe` exists in this register and nowhere else). The name matches
the retiring grandfathered member `council-deliberation-worker.yml` so that D10's
retirement reads as a retirement rather than as a coincidence.

---

## OPEN POINTS — the conservative reading taken, and flagged

**None of these blocks the build. Each is a place the ratified text is silent,
and each is resolved here in the direction that claims the least.**

### O1. The spelling of seat identity — RESOLVED BY THIS FAMILY'S OWN PRECEDENT

**The gap.** #165 design D6 describes `seat_results.json` as carrying *"seat,
result, rationale, undispositioned conditions, `num_turns`, …"* — and *"seat"* is
the one item in that list NOT rendered as a code identifier. Neither #165 file
gives a confirmed machine key for seat identity, and the ratified openxFactory
requirement says only *"seat identity"*.

**Reading taken (most conservative): mint no key spelling at all.** `seats` is a
KEYED COLLECTION keyed by the seat's identity, exactly as
`operation-report.schema.yaml`'s `lanes` is keyed by the lane key the register
declares, with that schema's stated reason: *"An array of fragments would have
made 'one composed report' indistinguishable from 'several reports in one
file'."* Keying also makes a duplicate seat identity UNREPRESENTABLE rather than
merely wrong. So this feature introduces no `seat_id` / `seat_name` / `role`
identifier, and a producer maps its own spelling onto the key.

### O2. "The four bound values" — the requirement names THREE, and three is what binds

**The gap.** #165 design D6 twice references *"the four bound values"* as an
unchanged, pre-existing concept and never itemizes them; only three are named by
identifier anywhere in that packet (`bundle_digest`, `subject_pin`,
`convening_job_id`). The fourth is not discoverable from the packet.

**Reading taken: bind exactly the three the RATIFIED requirement names** — *"the
convening job id, the verified subject pin, and the inbound bundle digest it
answers"* — and nothing else. Inventing a fourth from a phrase that itemizes
nothing would be minting a field.

**LEFT FOR BRETT**: if the producer's fourth bound value must also travel in the
NEUTRAL return, that is an amendment to this entry's declared output schema and
owes its own governed change. It is not a fix-up in a realization diff.

### O3. `verified_subject_pin` rather than `subject_pin`

**The gap.** The ratified requirement says *"the verified subject pin"*; #165's
identifier is `subject_pin`.

**Reading taken: `verified_subject_pin`.** This family's stated naming discipline
is *"DECLARED IS NOT OBSERVED, AND THE MEMBER NAMES CARRY THE WORD"*
(`dispatch-record.schema.yaml`), realized as `declared_runner_group`,
`declared_dispatch_label`, `declared_data_handling` and the operation report's
`declared` block. A bare `subject_pin` in a neutral record would not say whose
word it is; `verified_subject_pin` carries the ratified adjective and cannot be
read as the producer's claim. The producer-side spelling is recorded here so the
mapping is one rename and not a mystery.

### O4. `lane` is typed as an identifier, not pinned to `artifact`

**The gap.** The entry permits one lane. Should the schema pin it?

**Reading taken: no.** `permitted-operations.schema.yaml` states the family's own
rule — *"CLOSURE ITSELF IS NOT EXPRESSIBLE HERE: a schema constrains a document,
not a decision"* — and the register is the authority on which lanes an operation
may use. A `const: artifact` in the return schema would be a second copy of a
decision the register owns, and a sixth frozen copy nobody counted.

### O5. The negative fixture's failure code

**Reading taken:** the shape fixture declares the family's SHAPE refusal
`schema`. Verified against the shipped test:
`tests/clearing/test_validator_refusals.py::test_no_fixture_declares_a_code_outside_the_closed_set`
excludes `code != "schema"` from the closed-set membership check, exactly as task
2.2 says. **No `clearing-…` code is minted**, and the probed set — and therefore
the gate's `N/N` line — is arithmetically untouched at 26.

### O6. The re-pointed register fixture stays a TWO-entry document

**The gap.** `examples/negative/register-carrying-an-unratified-operation.yaml`
is "the shipped register plus one unratified member". After this change the
shipped register has two members.

**Reading taken: re-point the second entry to `coding` and stop there.** Ratified
task 2.4 asks for a re-point and a comment rewrite, nothing more; CLOSURE SHRINKS
lawfully (`test_removing_a_member_does_not_refuse`), so a fixture carrying fewer
ratified members than the instance is well-formed. Growing the fixture into a
three-entry mirror of the instance would add a maintenance surface no ratified
text asks for.

### O7. THE CONTRACT MINOR IS NOT TAKEN BY THIS FEATURE — `contract-v3.4` IS ALREADY CLAIMED

**MEASURED, and it changed the answer.** `git tag -l 'contract-v3.*'` returns
`contract-v3.0 … contract-v3.3`; `contracts/manifest.yaml` on `main` still
declares `contract-v3.3`; no later cut has landed. On merge order alone the next
number would be `contract-v3.4`.

**IT IS SPOKEN FOR.** openxFactory issue #630 (the pinned *Shared substrates —
claims* register) carries, at **2026-09-04T12:40:25Z**, comment
`#issuecomment-5540561424`:

> **SUBSTRATE CLAIMED — lane repo-shape** … Substrate: **row 4** (Contract cuts)
> — version number **`contract-v3.4`** … Brett Heap's word 2026-09-04, in
> session, lane repo-shape, verbatim: *"cut contract-v3.4"*.

Lane Collision Protocol **Amendment 1 rule 7** makes contract cuts a claimable
shared substrate and serializes claims **FIFO**. That claim is 25 minutes older
than this lane's realization claim, it names the repository owner's word, and its
object (the openRepoShape consumption pin) has since landed on `main` as **#650**
with the cut itself still to come.

**READING TAKEN, and it is the conservative one: THIS FEATURE DOES NOT CUT.**

- `contract_bundle_version` is **NOT MOVED**. It still reads `contract-v3.3`.
- **NO `contracts/CHANGELOG.md` ENTRY IS WRITTEN.** The policy allows one entry
  per RELEASE, and this feature allocates no release.
- **NO `contracts/releases/<tag>.digests.yaml` IS BUILT.** An inventory names a
  bundle, and naming one would reserve it.
- The new manifest row is **REGISTERED AT REALIZATION** and says so in its own
  `consumption_rule`: *"Registered at realization by
  `admit-deliberation-clearing-operation` … the bundle number is the cutting
  session's and is not reserved here."*

**THIS IS THE REPOSITORY'S OWN ESTABLISHED FORM, not an invention.** The twelve
`contracts/chain-anchoring/` rows already on `main` carry the identical sentence,
under a manifest comment that states the rule: *"NO BUNDLE NUMBER IS RESERVED BY
THIS REGISTRATION … the next additive number is fresh-counted at the tip the cut
is taken from … because a proposed change MUST NOT reserve a minor number before
merge order is known."* `add-chain-attestation` split the same way — rows in the
realization (#556), version bump and changelog in the cut (#565).
`docs/contract-versioning-policy.md` says it in as many words.

**LEFT FOR BRETT.** The realization's own `tasks.md` Phase 3 (3.1 – 3.4) is
therefore UNDISCHARGED and its item 3.1 — *"claim the version number, not the
files, on openxFactory issue #630 row 4"* — cannot be performed by this lane
while row 4 is held. The cut that carries these bytes will be whichever cut
follows `contract-v3.4`, and it must, when it comes:

1. advance `contract_bundle_version`;
2. write ONE changelog entry, class **ADDITIVE (minor)**, MEASURED — see the
   measurement already taken in § O9 below, which a cutting session can use
   rather than re-deriving;
3. build `contracts/releases/<tag>.digests.yaml` with
   `scripts/validate-contract-release.py build`;
4. move `tests/clearing/test_clearing_manifest_rows.py`'s `REGISTRATION` map
   entry for `clearing-deliberation-return` from the change name to the number,
   and `tests/intent-compliance/test_release_boundary.py`'s `ReleaseState` enum
   to admit the new value — both of which this feature deliberately did NOT
   touch, because touching them is cutting.

### O8. What a later cut will be carrying — MEASURED NOW so it is not re-derived

`git diff --name-status contract-v3.3 <this branch> -- contracts/` reports **119
additions and 6 modifications**. Only NINE of them are this feature's:

| this feature's | |
|---|---|
| A | `contracts/clearing/deliberation-return.schema.yaml` |
| A | `contracts/clearing/examples/deliberation-return.example.yaml` |
| A | `contracts/clearing/examples/negative/deliberation-return-carrying-a-verdict.yaml` |
| A | `contracts/clearing/examples/negative/deliberation-return-that-does-not-match-its-shape.yaml` |
| M | `contracts/clearing/permitted-operations.registry.yaml` |
| M | `contracts/clearing/dispatch-record.schema.yaml` |
| M | `contracts/clearing/examples/dispatch-record-refused.example.yaml` |
| M | `contracts/clearing/examples/negative/register-carrying-an-unratified-operation.yaml` |
| M | `contracts/clearing/examples/negative/manifest-naming-an-unregistered-operation.yaml` |

plus this feature's share of `contracts/manifest.yaml` and `contracts/README.md`.

**THE OTHER 110 ARE NOT THIS FEATURE'S, and are named here for the same reason
the `contract-v3.3` entry named the two review-lane files it did not own — so a
reader intersecting the diff with an entry does not attribute them to the wrong
change.** They moved on `main` between the `contract-v3.3` tag (which peels to
`16b85614`) and this branch's base `3cf917b7`:

- **`contracts/chain-anchoring/` — the whole tranche-three family, 110 new
  files**, registered at realization by `add-chain-anchoring` with its rows
  already in `contracts/manifest.yaml` and its changelog entry expressly left, in
  that manifest's own words, as *"the cutting session's act, unwritten at this
  commit"*.
- `contracts/signed-execution-chain/digest-construction.schema.yaml`,
  `transparency-log-leaf.schema.yaml` and that family's `README.md` — the same
  tranche-three work.
- `contracts/review-lane-pin.yaml` and `contracts/review-lane-floor-snapshot.yaml`.

**NO RELEASE-INVENTORY DRIFT IS CREATED BY THIS FEATURE, and that was measured
rather than assumed.** Every one of the 283 members of
`contracts/releases/contract-v3.3.digests.yaml` was re-hashed at this branch's
head: one drifts, `contracts/manifest.yaml`, which
`scripts/doc_health/release_inventory.py` classes as EDITORIAL and reports at
INFO. `contracts/clearing/` is not in that inventory at all, so no member of it
moved. The count is identical at the base commit, so this feature adds nothing to
it.
