---
code_surface: openxFactory — A VALIDATOR ARM, TWO CODES AND THREE FIXTURES; NO SCHEMA EDIT AT THIS MINOR. `scripts/validate-credential-contracts.py` gains a resolution-integrity pass over EVERY binding that declares a `consumer.requirement_ref`, reached from `_deprecation_warnings` (`:694-730`) beside the eight `consumer-*` arms rather than from `_lift_refusal_detail` (`:371-473`), which is the ONE caller of `resolve_requirement` (`:311-349`) in the file — at `:438`, inside a loop reached only for a pair sharing a `secret_ref` (`:540-546`, the bindings grouped into `by_secret` and every group of fewer than two skipped). The arm RE-USES `resolve_requirement` unchanged — the same four statuses, the same index built by `requirements_index` (`:294-309`), the same rule that the validator never opens a path taken from a record — and reports the `not-found` and `ambiguous` statuses that function already returns to a caller which consumes them only as a lift condition. `DEPRECATION_CODES` (`:157-166`) grows from EIGHT to TEN with two codes of a new family (proposed `requirement-ref-unresolved` and `requirement-ref-ambiguous`; the SPELLING is realization's, the FAMILY and the ZERO-versus-MANY split are the requirement's), and `WARNING_EXPECTATIONS` (`:169-180`) gains one entry per code — the self-test refusing a declared code that carries no packaged probe (`:826-838`). `examples/credential-contracts/warning/` gains two probes and `examples/credential-contracts/` one positive proving the SILENT direction (a resolving reference on bindings sharing no secret); the ambiguity probe resolves against the `support/ambiguous-requirement-ids.requirements.yaml` document that already ships, so the corpus needs no second support record. Every new fixture joins the by-name inventory at `tests/credential_contracts/test_dispatch_credential_contract.py:34-80`, which `test_the_inventory_is_the_whole_corpus_and_not_a_sample` (`:120-128`) holds EXHAUSTIVE against the glob; the self-test count string at `:103-104` is DERIVED from those tuples rather than written out, so it moves with them. `docs/contract-versioning-policy.md` § Deprecations Currently In Force — the `add-binding-consumer-identity` entry states "SEVEN acts that land together" and "EIGHT warning codes", and its own text claims to name EVERY act landing at contract-v3.0, so it is reconciled rather than left to contradict a ninth act; `contracts/manifest.yaml`'s `credential-contracts` row (`:2151-2210`) repeats the same "All seven acts … EIGHT warning codes" sentence and moves with it, which is what makes this realization owe a bundle cut even though the schema file itself does not move. NOT THIS CHANGE'S SURFACE, each for a stated reason: `contracts/schemas/xfactory-credential-contracts.schema.yaml` (the block is UNCONSTRAINED at this minor by ratified design, and resolution is not a shape a JSON Schema can check — it is a cross-document lookup); the six lift conditions and their every-pair arity (untouched, and the packaged dispatch-versus-content negative stays refused); `resolve_requirement`'s statuses, its index, its grammar and its never-open-a-path rule (re-used, not edited); and any cross-repository resolution (the residency model keeps consumers' bindings in their own trees, and this validator reads one repository).
target_release: THE NEXT ADDITIVE MINOR, DELIBERATELY NOT NUMBERED HERE — allocated AT REALIZATION by merge order per `docs/contract-versioning-policy.md`. Read at this branch's merge-base rather than remembered: `contracts/manifest.yaml:3` declares `contract_bundle_version: contract-v2.5` and `contracts/releases/contract-v2.5.digests.yaml` is a cut inventory in the tree, so the era is v2 and the next additive minor is whatever merge order allocates. A number written here would be a number another packet is already spending — `add-credential-escrow-checkout` is ratified and owes an additive minor on the SAME schema file, and `contracts/manifest.yaml` has had three writers before. THE CLASS AT THIS CUT IS MINOR ON EITHER OF THE POLICY'S TWO READINGS, and both are quoted rather than picked. `docs/contract-versioning-policy.md` § Change Classes (`:293-306`) reads "Additive (minor) — new optional fields, new contracts, NEW VALIDATOR WARNINGS" and, one bullet down, "Deprecating (minor) — a field or shape is marked deprecated; the conformance validator emits warnings but still accepts it. Deprecations must state the removal version and a migration path in the CHANGELOG." Two new validator warnings answering a refusal declared for the major is the SECOND of those exactly, which is the stricter reading and the one this packet takes: the removal version and the migration path are OWED IN THE CHANGELOG at the cut (tasks § 5, § 6) rather than optional. THE CLASS AT THE MAJOR IS BREAKING, and that is MEASURED rather than assumed — the reproduction below shows a record carrying both defects validating clean today, so refusing it later is "a shape is removed" and costs the policy's full ritual: a CHANGELOG migration note, at least one full minor of deprecation warnings, and a validator that refuses the old shape only at the new major. The removal target is contract-v3.0, the SAME major the consumer block's seven acts land at, so consumers serve ONE window rather than two.
---

# Proposal: add-requirement-ref-resolution-integrity

Status: ratified
Proposed: 2026-08-31, on Brett Heap's recorded ruling of 2026-08-30 — *"successor
change with its own resolution-integrity code"* — taken over the Codex finding on
PR #516 and anchored at openxFactory issue #523, which is this packet's origin
and its scope statement both.
Ratified: 2026-09-01 by Brett Heap (repository owner) — in-session via an explicit
multi-choice put, session `openxfactory-f5`; record at
`openspec/changes/add-requirement-ref-resolution-integrity/review/ratification-2026-09-01.md`.
The record-citing spelling is the one this citation's condition of use selects:
there is no approving OpenSpec change to name. **AD-1 IS RULED TWO CODES, AS
DRAFTED**, and the twelve-item one-code amendment set is DECLINED — left standing
in § Authoring decisions as the record of the alternative that was rulable, not
struck.

## Standing

**THIS PACKET IS RATIFIED — 2026-09-01, BY DIRECT RULING.** `Status: ratified`,
with the record-citing `Ratified:` line above; the record is
`review/ratification-2026-09-01.md`. Brett Heap ruled in session via an explicit
multi-choice put. **AD-1 IS RULED: TWO CODES**, exactly as this packet
recommends — zero-resolving and ambiguous reported apart, under distinct codes,
because their remedies live in different files. AD-2 … AD-6 stand as drafted.

**THE AD-1/ONE-CODE AMENDMENT SET IS DECLINED AND IS DELIBERATELY NOT DELETED.**
None of its twelve items is executed: the delta's *"ZERO AND MORE-THAN-ONE ARE
NAMED APART"* paragraph is unedited, the *"named apart"* scenario keeps its
DISTINCT-codes obligation, and `code_surface` still buys TWO CODES AND THREE
FIXTURES. The enumeration stays in AD-1 below as the record of what was rulable —
a ratifier offered a real alternative and taking the other one leaves a better
record by keeping the alternative legible than by deleting the evidence a choice
existed.

**NO §7.4 SITTING WAS CONVENED, AND NONE WAS PRESCRIBED.** `tasks.md` § 2.3 put
the question rather than the answer — whether to convene one was Brett's call —
and he took the DIRECT path, the #504/#497-family precedent's direct branch that
`add-notebook-projection-identity`, `add-standing-policy-compliance-contract` and
`govern-sibling-added-modified-deltas` each took. No seat sat, no ballot was cast,
and nothing in this packet may be cited as a council disposition.

**WHAT THE TWO AUTHORIZATIONS EACH COVER, KEPT APART.** What Brett authorized on
2026-08-30 was the DECISION TO FILE and the SHAPE OF THE FIX, the one sentence in
issue #523; `.openspec.yaml` records that and says plainly that it did not reach
this packet's content. The 2026-09-01 ruling is the separate, later act that does.

**THE FOUR OPEN QUESTIONS ARE UNTOUCHED BY IT.** OQ-1 … OQ-4 below remain OPEN,
each with its recommendation and no decision. The ruling reached AD-1 and did not
reach the questions.

**RATIFICATION AUTHORIZES REALIZATION AND PERFORMS NONE OF IT.** This is still a
PROPOSAL-ONLY pull request on the house pattern its own subject set established:
`add-binding-consumer-identity` landed as a proposal (PR #497) and its realization
came separately (PR #516). No validator line, no fixture, no bundle number and no
policy row moves here. `tasks.md` § 3 – § 6 are the realization slice and belong
to a separate pull request; the change stays ACTIVE until § 8's
merged-and-green evidence exists.

**ONE REVIEW FINDING IS OPEN AT THE RATIFIED TIP AND IS ROUTED, NOT REPAIRED.**
The third Codex round read `deb72c8e` and found that `resolve_requirement`'s
lookup is scoped to the ONE document a reference names, so the cross-document arm
of the promoted ambiguity scenario stays unmet while `tasks.md` § 3.4 freezes that
resolver. It falsifies nothing ratified here — this delta's ambiguity scenario
says *"more than one requirement record"* and nothing about document count — and
it is carried in the open at `tasks.md` § 9.4 with a pointer at § 3.4. See
`review/ratification-2026-09-01.md` § "The review evidence".

## Why

**A reference that resolves to nothing is reported only when the binding beside
it happens to name the same secret.** That is not a rule about references. It is
a rule about pairs, doing duty for a rule about references, and the packet that
introduced the reference said the general thing in its requirement text while
its implementation said the narrow one.

The ratified block requirement states the duty with no predicate at all:

> A reference that is ungrammatical, that names a repository other than the one
> under validation, or that resolves to zero or to more than one requirement
> SHALL be reported and SHALL NOT be treated as resolved.

The shipped check answers to a different sentence. `resolve_requirement` is
called from exactly ONE place — `_lift_refusal_detail`, the six-condition lift —
and that function is only reached for a PAIR OF BINDINGS THAT SHARE A
`secret_ref`. A binding that declares a well-formed, grammatical reference to a
requirement that does not exist, and whose secret reference is its own, is
resolved by nobody and reported by nothing.

**Codex found this on PR #516; the realization confirmed it and deliberately did
not fix it**, because neither repair available inside that packet was honest:

- an ERROR would have been an UNPHASED NARROWING — a shape valid on the current
  major would start refusing with no deprecation window, which is the exact act
  the whole consumer-block packet exists to phase;
- a WARNING would have needed a NINTH code, and the ratified rule is that the
  warning set is *"ENUMERATED against the refusals"* — an unresolvable reference
  is not a shape the coming major refuses, so a ninth code would have been a
  warning with no deprecation to serve.

**Brett ruled the successor on 2026-08-30**: a small change carrying its own
resolution-integrity code. Issue #523 is that ruling's anchor and states the
scope in three parts — a code of its own family rather than a widening of an
existing one; phased per the deprecation pattern if any today-valid shape starts
refusing; and the three split packet clauses reconciled so that the general SHALL
and the scenario's scope agree. This packet is those three parts and nothing
wider.

## What was measured

Measured 2026-08-31 against the validator exactly as it ships at this branch's
merge-base `3a6a16e9` — not read out of the source and not remembered — and
RE-MEASURED the same day, after review, once the control was rebuilt on secret
references that genuinely differ by one byte. The branch's own diff moves no
validator line, no fixture and no test, so the tree run against here and the
merge-base tree are the same validator.

### 1. The defect reproduces, and it reproduces silently

A repository holding two files. `credentials/example.requirements.yaml` declares
three requirements: `alpha_lane`, and `dup_lane` TWICE — once
`workload_identity`, once `dispatch_only` carrying TRIGGER-ONLY scopes so the
`dispatch-scope-ceiling` arm has nothing to say — leaving the two matches
differing in exactly the field the lift turns on and in nothing else.
`credentials/example.binding-template.yaml` declares two bindings whose secret
references DIFFER BY ONE BYTE (`example-secret-a` and `example-secret-b`), each
with a consumer block carrying `holder_ref`, `fetch_identity` and
`requirement_ref` and NO acknowledgment:

- `zero_resolving_lane` (`secret_ref: example-secret-a`) ->
  `requirement_id: no_such_requirement` (resolves to ZERO)
- `multi_resolving_lane` (`secret_ref: example-secret-b`) ->
  `requirement_id: dup_lane` (resolves to TWO, with different access modes)

THE ONE-BYTE SPACING IS DELIBERATE AND IS WHAT MAKES THE CONTROL BELOW RERUNNABLE
AS STATED. An earlier draft of this section spaced them `example-secret-one` /
`example-secret-two` and called the control a one-byte edit; that edit is THREE
bytes, and a reader rerunning it would have been measuring something the text did
not describe.

Both document references are grammatical and both name a document the validator
indexed. The run:

```text
self-test: 6 positive + 16 negative + 10 warning example(s) confirmed, 8 deprecation code(s) probed

repro: 2 contract(s) checked, 0 skipped, 0 warning(s), 0 error(s) -> PASS
```

**Zero warnings. Zero errors. PASS.**

### 2. One byte turns it into a finding, and a second edit names the fault

TWO CONTROLS, KEPT APART, because they say different things.

**Control A — one byte, COUNTED rather than claimed.** The same tree with
`example-secret-b` changed to `example-secret-a`, and NOTHING else touched. The
two binding templates are the SAME LENGTH (1318 bytes) and differ at EXACTLY ONE
OFFSET (byte 980); the requirements document is byte-identical between the two
trees. Output below, reflowed to this column and otherwise verbatim:

```text
ERROR credentials/example.binding-template.yaml: shared-secret-identity:
bindings 'zero_resolving_lane' and 'multi_resolving_lane' share secret_ref
'example-secret-a'; dispatch and content credentials must be distinct bindings
so the serving tier holds no content-write key material. The two-consumer lift
is UNAVAILABLE here: binding 'zero_resolving_lane' does not declare
shared_credential_acknowledged: true — a one-sided declaration exempts a pair
on one party's word

control: 2 contract(s) checked, 0 skipped, 0 warning(s), 1 error(s) -> FAIL
```

A record that was silent is now refused, and ONE BYTE of `secret_ref` is the
whole difference. But the refusal names the FOURTH lift condition, not the
reference — the pair is refused before resolution is ever consulted.

**Control B — that same byte PLUS the acknowledgment** on both bindings, so the
pair reaches the fifth condition and resolution is actually asked:

```text
ERROR credentials/example.binding-template.yaml: shared-secret-identity:
bindings 'zero_resolving_lane' and 'multi_resolving_lane' share secret_ref
'example-secret-a'; dispatch and content credentials must be distinct bindings
so the serving tier holds no content-write key material. The two-consumer lift
is UNAVAILABLE here: binding 'zero_resolving_lane''s requirement_ref resolves to
no requirement in the repository under validation

control: 2 contract(s) checked, 0 skipped, 0 warning(s), 1 error(s) -> FAIL
```

*"resolves to no requirement in the repository under validation"* — the exact
sentence the silent tree never produced, about the exact same bytes of
`requirement_ref`. The validator can see the dangling reference perfectly well.
It looks only where an exemption was being requested, and only after four other
conditions have passed.

### 3. The call graph says the same thing

`resolve_requirement` (`scripts/validate-credential-contracts.py:311-349`) has
ONE caller in the file: `_lift_refusal_detail` at `:438`, inside the loop over a
pair. That function is reached from `_lift_refusal` -> `_binding_findings`, whose
default-refusal block (`:540-546`) groups the bindings into `by_secret` and
`continue`s past every group of fewer than two:

```python
    for ref, sharers in by_secret.items():
        if len(sharers) < 2:
            continue
```

The per-binding deprecation arm `_consumer_block_warnings` (`:590-691`) checks
the reference's SHAPE (`consumer-member-grammar`) and its document reference's
GRAMMAR (`consumer-requirement-ref-grammar`) and never resolves it — correctly,
since grammar is not resolution, but that is the whole per-binding coverage there
is.

### 4. Three clauses of one packet, split

| clause | what it says | scope |
| --- | --- | --- |
| block requirement | "resolves to zero or to more than one … SHALL be reported" | none stated |
| lift requirement, scenario *The requirement reference cannot be resolved* | "**WHEN** two bindings share a `secret_ref` and a named requirement reference resolves to nothing" | a sharing pair |
| lift requirement, scenario *The requirement reference resolves to more than one record* | "**WHEN** a named requirement reference matches requirement records in more than one document" | none stated |
| tasks § 2.5 | "ZERO matches AND MORE THAN ONE match both report and withhold the lift" | a conjunction |

Note the third row: the AMBIGUITY scenario in the ratified text already carries
NO sharing predicate, while the implementation scopes it to one — so the split is
not merely between prose and code, it is inside the promoted scenario set.

### 5. Nothing narrows at this cut, and the major's window is shared

Two new WARNING codes. A record that draws them stays VALID and the verdict does
not redden, exactly as the eight `consumer-*` codes behave today. The refusal
lands at contract-v3.0, the same major the block's seven acts land at, so a
consumer serves one deprecation window rather than two.

### 6. The reproduction tree, in full

Written out rather than described, so § 1 and § 2 are RE-RUNNABLE by anyone
holding this file and a checkout — the two files below under a `credentials/`
directory, then `python3 scripts/validate-credential-contracts.py <that repo>`.

`credentials/example.requirements.yaml`:

```yaml
# Reproduction support for add-requirement-ref-resolution-integrity.
# Three requirement records: one unambiguous, and one id declared TWICE with
# DIFFERENT access modes so a reference to it resolves to MORE THAN ONE.
schema_version: 1
kind: xfactory_credential_requirements
domain:
  id: example-projection
  product_name: Example Projection Lane
requirements:
  - id: alpha_lane
    purpose: the unambiguous sibling, present so the document is a real requirements record
    access_mode: workload_identity
    minimum_scopes:
      - projection:write
    requires_domain_approval: true
    requires_human_approval: false
    max_grant_minutes: 60
    audit_required: true
  - id: dup_lane
    purpose: the first record carrying this id
    access_mode: workload_identity
    minimum_scopes:
      - projection:write
    requires_domain_approval: true
    requires_human_approval: false
    max_grant_minutes: 60
    audit_required: true
  - id: dup_lane
    purpose: the SECOND record carrying the same id, with a different access mode
    access_mode: dispatch_only
    minimum_scopes:
      - actions:read
    requires_domain_approval: true
    requires_human_approval: false
    max_grant_minutes: 60
    audit_required: true
```

`credentials/example.binding-template.yaml`:

```yaml
# Reproduction for add-requirement-ref-resolution-integrity: TWO defective
# references on bindings whose secret references DIFFER BY ONE BYTE
# (`example-secret-a` / `example-secret-b`), so the shipped validator never
# reaches resolution.
schema_version: 1
kind: xfactory_credential_binding_template
client:
  id: example-client
  display_name: Example Client (reproduction)
credential_bindings:
  zero_resolving_lane:
    provider: azure_key_vault
    vault: kv-example-projection
    secret_ref: example-secret-a
    owner: example-platform
    rotation_policy: operator_managed
    consumer:
      holder_ref: example:service-subject:zero-resolving-lane
      fetch_identity: example-zero-resolving-workload-identity
      requirement_ref:
        requirement_id: no_such_requirement
        requirements_document_ref: credentials/example.requirements.yaml
  multi_resolving_lane:
    provider: azure_key_vault
    vault: kv-example-projection
    secret_ref: example-secret-b
    owner: example-platform
    rotation_policy: operator_managed
    consumer:
      holder_ref: example:service-subject:multi-resolving-lane
      fetch_identity: example-multi-resolving-workload-identity
      requirement_ref:
        requirement_id: dup_lane
        requirements_document_ref: credentials/example.requirements.yaml
```

Control A is that second file with `example-secret-b` -> `example-secret-a` and
nothing else. Control B is Control A with
`      shared_credential_acknowledged: true` added to BOTH consumer blocks,
immediately after each `requirement_ref` mapping.

## What this changes

**Two ADDED requirements on `credential-contracts`, no MODIFIED block anywhere.**

1. **A declared requirement reference is resolved on its own binding, whatever
   that binding shares.** The reporting duty is per-binding and independent of
   `secret_ref`, on the same reasoning this capability already applied to the
   shared-authority finding — the shared secret is a proxy for a rule, not the
   rule. It reconciles the three split clauses by SPLITTING the conjunction:
   reporting is owed by every binding that declares a reference; withholding the
   lift is owed by the pair asking for the exemption. Six scenarios, including
   the falsifiable one that the shipped check reports NEITHER defect today and
   that one byte is enough to make it report.
2. **Resolution integrity carries its own code and phases like every other
   narrowing.** Its own family, not a widening; zero and more-than-one named
   apart because their remedies differ; WARNING for a full minor and ERROR at
   contract-v3.0; the entry that claims to name every act at that major
   reconciled; and the corpus probing BOTH directions, the silent one being what
   distinguishes a working check from one that fires on everything. Six
   scenarios.

**The delta is ALL-ADDED BY MEASUREMENT, not by preference** — see § The sibling
rule, measured.

## The sibling rule, measured

`govern-sibling-added-modified-deltas` was ratified 2026-08-31: a
`## MODIFIED Requirements` block over a requirement that no PROMOTED
specification carries, where an ACTIVE change ADDS it, must carry a
``**Modified over `<basis>`'s addition by <change-id> (<date>):**`` marker AND
falls under an ARCHIVE-ORDER HOLD — the basis change ratifying and archiving
first.

**MEASURED TWICE, AND THE SECOND MEASUREMENT IS THE ONE THAT NOW HOLDS.** The
first was taken at this branch's merge-base `3a6a16e9`; a catch-up merge of
`origin/main` (`1c1dcbbe`) then falsified it, and it is re-measured here rather
than ratified as written.

**AS MEASURED AT MERGE-BASE `3a6a16e9` (TRUE WHEN WRITTEN, NO LONGER TRUE):**

- `openspec/specs/credential-contracts/spec.md` carried SEVEN requirement titles.
  Neither *"A credential binding declares the consuming system that holds it and
  the identity it fetches with"* nor *"Two bindings on one secret are refused
  unless every pair declares distinct consumers…"* was among them.
- Both were ADDED by `add-binding-consumer-identity`, then ACTIVE, ratified
  2026-08-29, and unarchived.

So a MODIFIED block over either of them would then have been exactly the governed
shape: a marker, and an archive-order hold putting this packet behind its
sibling's archive.

**AS RE-MEASURED AFTER THE CATCH-UP MERGE, AT `origin/main` `1c1dcbbe`:**

- **PR #541 ARCHIVED `add-binding-consumer-identity`** on 2026-08-31 (basis-first,
  together with `add-notebook-hosting-credential-custody`), promoting its
  requirements. The packet now lives at
  `openspec/changes/archive/2026-08-31-add-binding-consumer-identity/`.
- `openspec/specs/credential-contracts/spec.md` now carries TWELVE requirement
  titles, and **BOTH of the two named above ARE among them** — at `:278` and
  `:440` respectively.
- So a MODIFIED block over either would now be an ORDINARY MODIFIED block over
  PROMOTED CANON: no `Modified over` marker, and no archive-order hold, the basis
  having already archived.

**THE CHOICE IS UNCHANGED BY THE RE-MEASUREMENT, AND THAT IS WHY IT IS RE-MEASURED
RATHER THAN DELETED.** Under BOTH measurements **a pure ADDED requirement
serves**, because the reporting duty is a duty this capability states nowhere —
the sibling states the duty for the reference and this states where it is owed —
and neither sibling requirement's text has to change for both to be true. What
moved is only the REASON the marker rule does not apply: first because a marker
plus a hold would have been owed and an ADDED delta avoided both, now because the
basis has archived and neither would be owed at all. **CHOSEN, AND RATIFIED: two
ADDED requirements, no MODIFIED block, no marker, no hold.** The reconciliation is
performed by the new requirement's own text rather than by editing the old one.

**CHECKED WITH IT, AND NOT ASSUMED:** neither ADDED title — *"A declared
requirement reference is resolved on its own binding, whatever that binding
shares"* nor *"Resolution integrity carries its own code and phases like every
other narrowing"* — appears among the twelve promoted titles, so the all-ADDED
delta raises no ADDED-over-canon collision against the newly promoted text.

## What this deliberately does not change

- **The schema.** The `consumer:` block stays UNCONSTRAINED at this minor by
  ratified design, and resolution is not a shape JSON Schema can check: it is a
  cross-document lookup against records the validator discovered.
- **The lift and its six conditions.** Same conditions, same every-pair arity,
  same fail-closed behaviour. The packaged dispatch-versus-content negative stays
  refused.
- **`resolve_requirement` itself.** Same four statuses, same index, same grammar,
  same rule that the validator never opens a path taken from a record. This
  change reports what that function already returns.
- **The `consumer-*` codes.** None is widened, renamed, re-severitied or
  re-probed. `consumer-requirement-ref-grammar` keeps meaning "the document
  reference is not a repository-relative YAML path", which is a different fault
  from "the reference resolved to nothing".
- **Cross-repository resolution.** The residency model keeps consumers' bindings
  in their own trees; this validator reads one repository and this change does
  not make it read two.

## Authoring decisions, flagged for veto

**RULED 2026-09-01 — see § Standing and `review/ratification-2026-09-01.md`.**
Every item here was the AUTHORING SESSION'S when written, taken to make the packet
coherent, and none was Brett's 2026-08-30 ruling — that ruling is the one sentence
in issue #523 and covers the decision to file and the shape of the fix. **AD-1 …
AD-6 ARE NOW DISPOSED BY THE SEPARATE 2026-09-01 RATIFICATION: AD-1 is RULED TWO
CODES, as drafted, and AD-2 … AD-6 stand as drafted.** The veto flags are kept
below as authored, because what each decision cost to veto is why the ruling that
declined to veto it means something.

- **AD-1 — RULED: TWO CODES, 2026-09-01.** *Two codes rather than one, with the
  ONE-CODE BRANCH WRITTEN OUT so it can be RULED rather than merely gestured at.*
  **THE RULING TOOK THE RECOMMENDATION AS DRAFTED**, so the amendment set below is
  DECLINED AND NOT EXECUTED — not one of its twelve items is applied — and it is
  left standing as the record of the alternative that was rulable rather than
  struck from the packet. `tasks.md` § 3.3's *"Subject to AD-1"* cross-reference is
  DISCHARGED by this ruling, not deleted. Issue #523 says "a
  resolution-integrity code", singular. This packet asks for TWO — zero and
  more-than-one named apart — on the family's own "a refusal shall name the fault
  it found" rule and on the measured fact that their remedies live in different
  files: a reference resolving to NOTHING is repaired at the reference, a
  reference resolving to SEVERAL is repaired in the requirements document.

  **THE PACKET AS DRAFTED CARRIES THE TWO-CODE SHAPE AS NORMATIVE.** The delta
  obliges the two faults to be NAMED APART, the task list buys two codes and
  three fixtures, and `code_surface` says `DEPRECATION_CODES` grows from EIGHT to
  TEN. A one-code ruling is therefore NOT the strike of a single scenario — an
  earlier draft of this item said it was, which would have ratified a packet that
  simultaneously permitted and forbade a single-code implementation. It is the
  amendment set below, EXECUTED IN THE RATIFYING COMMIT if ruled, enumerated here
  so a one-line ruling can be carried out mechanically and so no reader has to
  reconstruct it.

  **AD-1/ONE-CODE AMENDMENT SET — applied ENTIRE or not at all. DECLINED BY THE
  2026-09-01 RULING; NONE OF THE TWELVE ITEMS IS EXECUTED. It is retained verbatim
  as the record of the branch that was on offer:**

  1. `specs/credential-contracts/spec.md`, FIRST requirement, the paragraph
     opening *"ZERO AND MORE-THAN-ONE ARE NAMED APART, because their remedies are
     different"*: REPLACED by a paragraph that keeps the remedy analysis and
     drops the naming-apart obligation — *"ZERO AND MORE-THAN-ONE HAVE DIFFERENT
     REMEDIES, AND THE REPORT SHALL SAY WHICH IT FOUND"*, retaining the two
     remedy sentences and the "more dangerous of the two" reasoning verbatim, and
     closing: *"Under a single code the distinction MOVES INTO THE MESSAGE: the
     finding SHALL state whether ZERO or MORE THAN ONE requirement answered, and
     SHALL NOT report the one as the other."*
  2. `specs/credential-contracts/spec.md`, SECOND requirement, scenario
     *"Zero and more-than-one are named apart"*: RETITLED *"Zero and
     more-than-one are told apart"* and its THEN bullet REPLACED — "the two MUST
     be reported under DISTINCT codes, their remedies being at the reference and
     in the requirements document respectively" becomes "the finding MUST STATE
     WHICH OF THE TWO it found, their remedies being at the reference and in the
     requirements document respectively". The AND bullet ("neither MUST be
     reported as the other") STANDS UNCHANGED — it is the half that does the
     work under either shape. **The scenario is REWRITTEN, NOT STRUCK**, so the
     promoted scenario set keeps its arity and tasks § 1.1's TWELVE stands.
  3. `specs/credential-contracts/spec.md`, SECOND requirement, scenario *"Both
     directions are packaged"*: TEXT UNCHANGED — it is written per DECLARED CODE
     and is count-neutral — but its consequence becomes ONE registered probe
     rather than two. No edit; listed so the ratifier can see it was checked.
  4. `proposal.md` front-matter `code_surface`, four sentences: "A VALIDATOR ARM,
     TWO CODES AND THREE FIXTURES" -> "A VALIDATOR ARM, ONE CODE AND TWO
     FIXTURES"; "`DEPRECATION_CODES` (`:157-166`) grows from EIGHT to TEN with
     two codes of a new family (proposed `requirement-ref-unresolved` and
     `requirement-ref-ambiguous`; …)" -> "grows from EIGHT to NINE with ONE code
     of a new family (proposed `requirement-ref-unresolved`, its MESSAGE carrying
     the zero-versus-many status; the SPELLING is realization's, the FAMILY is
     the requirement's)"; "`examples/credential-contracts/warning/` gains two
     probes and `examples/credential-contracts/` one positive" -> "gains ONE
     probe and `examples/credential-contracts/` one positive"; and the clause
     re-using `support/ambiguous-requirement-ids.requirements.yaml` becomes
     PERMISSIVE rather than owed, the single probe being free to probe either
     status.
  5. `proposal.md` § What was measured § 5 ("Two new WARNING codes") and
     § Impact ("Two new warnings") -> "ONE new WARNING code" / "One new warning".
     Nothing else in either passage moves; the phasing argument is code-count
     independent.
  6. `proposal.md` § What this changes, item 2: "zero and more-than-one named
     apart because their remedies differ" -> "zero and more-than-one
     DISTINGUISHED IN THE MESSAGE, their remedies differing".
  7. `tasks.md` § 1.1: UNCHANGED. "TWO ADDED requirements over TWELVE SCENARIOS"
     survives because item 2 rewrites rather than strikes.
  8. `tasks.md` § 3.3: "Two codes, one per status: `not-found` and `ambiguous`
     reported apart. Proposed spellings … both join `DEPRECATION_CODES` (8 ->
     10) and `WARNING_EXPECTATIONS`" -> "ONE code carrying both statuses in its
     message, `not-found` and `ambiguous` told apart in the text of the finding.
     Proposed spelling `requirement-ref-unresolved`; it joins `DEPRECATION_CODES`
     (8 -> 9) and `WARNING_EXPECTATIONS`." The trailing "**Subject to AD-1**"
     sentence is DELETED, the ruling having discharged it.
  9. `tasks.md` § 3.7: the mutant "merge the two codes" -> "report the WRONG
     STATUS in the message (zero reported as many)", so the mutation round still
     kills the fault the second code was buying.
  10. `tasks.md` § 4.1 and § 4.2: the two `warning/` fixtures collapse to ONE
      REGISTERED probe. § 4.2's ambiguity fixture either ships UNREGISTERED (kept
      as an assertion target of a named test, since `WARNING_EXPECTATIONS` holds
      one entry per file and the self-test refuses a stray) or is dropped and its
      case folded into § 4.1's file as a second binding. § 4.4's "All three join
      the by-name inventory tuples" reads "BOTH join" or "All three join",
      matching whichever of the two is taken — and the count string stays
      DERIVED, so it moves either way.
  11. `tasks.md` § 5.1: "the act, its two codes, its migration and its removal
      target" -> "the act, its code, its migration and its removal target".
  12. `README.md`'s active entry for this change: "a separate change owing two
      codes, three fixtures, a reconciled `Deprecations Currently In Force` entry
      and a bundle cut" -> "one code, two fixtures, a reconciled … entry and a
      bundle cut". The entry's "a code of its OWN FAMILY (not a widening of any
      of the eight `consumer-*` codes)" is already singular and does not move.

  **THE RECOMMENDATION IS UNCHANGED BY THE ENUMERATION: TWO CODES — AND IT IS
  WHAT WAS RULED.** Writing the
  branch out did not weaken the case — it showed that the one-code shape survives
  only by moving the fault's name from the CODE into the MESSAGE, which is
  exactly what this family's "a refusal shall name the fault it found" rule was
  written against, and it costs a machine-readable distinction a consumer's
  tooling can act on. But the branch is now a branch, and one sentence takes it.
- **AD-2 — The removal target is contract-v3.0**, shared with the consumer
  block's seven acts, rather than a major of its own. Cheaper for consumers; it
  also means this act must be written INTO the sibling's completeness claim,
  which is AD-3.
- **AD-3 — The sibling's deprecation entry is reconciled rather than duplicated.**
  `docs/contract-versioning-policy.md`'s entry says it names EVERY act landing at
  contract-v3.0. The alternative — a separate entry naming the same major — is
  coherent but leaves the first entry's completeness claim false unless it
  gains a pointer, so the reconciliation is owed either way.
- **AD-4 — The code family spelling is left to realization.** The requirement
  fixes the FAMILY (its own, not a widening) and the SPLIT (zero apart from
  many); `requirement-ref-unresolved` / `requirement-ref-ambiguous` are proposed
  in `code_surface` and in tasks § 3, not prescribed in the spec, on the
  precedent that the promoted text enumerates shapes and the policy document
  carries spellings.
- **AD-5 — Proposal-only landing.** No code in this pull request, on the
  #497 -> #516 pattern this packet's own subject set. An implementer could argue
  the fix is small enough to bundle; the counter is that a bundled realization
  spends a contract bundle number before a ratifier has read the text.
- **AD-6 — `credential-contracts` is the owning capability**, not a new one. The
  requirement is about this validator's reading of this family's records.

## Open questions

- **OQ-1 — Does the ambiguity arm need a support fixture of its own?**
  `examples/credential-contracts/support/ambiguous-requirement-ids.requirements.yaml`
  already ships and is indexed by the self-test; the probe can resolve against it.
  Recommendation: re-use it, and record the re-use in the fixture's header so a
  later edit to that support record cannot silently defang two probes.
- **OQ-2 — Should the ungrammatical and foreign-repository statuses move too?**
  The block requirement's general SHALL names THREE conditions —
  ungrammatical, foreign-repository, and zero-or-many. The first two are already
  reported per-binding by `consumer-requirement-ref-grammar`, so only the third
  is homeless. Recommendation: leave them where they are, and say so in the
  requirement rather than leaving a reader to check.
- **OQ-3 — Does the same gap exist in the sibling families?** `resolve` /
  `requirements_document_ref` also appear in the identity-brokering family, where
  the introducing packet recorded that *"no script and no test resolves"* the
  pointer at all. Recommendation: out of scope here, filed as a successor issue
  rather than folded in.
- **OQ-4 — Should the positive silent-direction fixture be a THIRD binding on an
  existing positive, or its own file?** Recommendation: its own file, so that a
  regression in the silent direction names itself.

## Impact

- **Affected capability:** `credential-contracts` (two ADDED requirements).
- **Affected code at realization:** `scripts/validate-credential-contracts.py`,
  `examples/credential-contracts/**`, `tests/credential_contracts/**`,
  `docs/contract-versioning-policy.md`, `contracts/manifest.yaml`,
  `contracts/CHANGELOG.md`.
- **Affected consumers:** none at this cut. Two new warnings; every record valid
  today stays valid, and a domain repo pinned at the prior bundle is untouched
  until it upgrades.
- **Affected siblings:** `add-binding-consumer-identity` — **ARCHIVED 2026-08-31
  by PR #541**, its requirements now promoted canon; this packet MODIFIES none of
  them and imposes no archive-order hold on anything.
  `add-credential-escrow-checkout` (ACTIVE, ratified) — the other writer on this
  family's schema, which this packet does not touch.
- **Risk if not done:** the ratified general SHALL stays unenforced, and a
  binding pointing at a requirement that does not exist keeps passing — the
  fail-open shape this family has already repaired twice, once in a drift check
  and once in the access-mode arm.
