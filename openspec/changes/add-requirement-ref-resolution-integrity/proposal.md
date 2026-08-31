---
code_surface: openxFactory — A VALIDATOR ARM, TWO CODES AND THREE FIXTURES; NO SCHEMA EDIT AT THIS MINOR. `scripts/validate-credential-contracts.py` gains a resolution-integrity pass over EVERY binding that declares a `consumer.requirement_ref`, reached from `_deprecation_warnings` (`:694-730`) beside the eight `consumer-*` arms rather than from `_lift_refusal_detail` (`:371-473`), which is the ONE caller of `resolve_requirement` (`:311-349`) in the file — at `:438`, inside a loop reached only for a pair sharing a `secret_ref` (`:540-546`, the bindings grouped into `by_secret` and every group of fewer than two skipped). The arm RE-USES `resolve_requirement` unchanged — the same four statuses, the same index built by `requirements_index` (`:294-309`), the same rule that the validator never opens a path taken from a record — and reports the `not-found` and `ambiguous` statuses that function already returns to a caller which consumes them only as a lift condition. `DEPRECATION_CODES` (`:157-166`) grows from EIGHT to TEN with two codes of a new family (proposed `requirement-ref-unresolved` and `requirement-ref-ambiguous`; the SPELLING is realization's, the FAMILY and the ZERO-versus-MANY split are the requirement's), and `WARNING_EXPECTATIONS` (`:169-180`) gains one entry per code — the self-test refusing a declared code that carries no packaged probe (`:826-838`). `examples/credential-contracts/warning/` gains two probes and `examples/credential-contracts/` one positive proving the SILENT direction (a resolving reference on bindings sharing no secret); the ambiguity probe resolves against the `support/ambiguous-requirement-ids.requirements.yaml` document that already ships, so the corpus needs no second support record. Every new fixture joins the by-name inventory at `tests/credential_contracts/test_dispatch_credential_contract.py:34-80`, which `test_the_inventory_is_the_whole_corpus_and_not_a_sample` (`:120-128`) holds EXHAUSTIVE against the glob; the self-test count string at `:103-104` is DERIVED from those tuples rather than written out, so it moves with them. `docs/contract-versioning-policy.md` § Deprecations Currently In Force — the `add-binding-consumer-identity` entry states "SEVEN acts that land together" and "EIGHT warning codes", and its own text claims to name EVERY act landing at contract-v3.0, so it is reconciled rather than left to contradict a ninth act; `contracts/manifest.yaml`'s `credential-contracts` row (`:2151-2210`) repeats the same "All seven acts … EIGHT warning codes" sentence and moves with it, which is what makes this realization owe a bundle cut even though the schema file itself does not move. NOT THIS CHANGE'S SURFACE, each for a stated reason: `contracts/schemas/xfactory-credential-contracts.schema.yaml` (the block is UNCONSTRAINED at this minor by ratified design, and resolution is not a shape a JSON Schema can check — it is a cross-document lookup); the six lift conditions and their every-pair arity (untouched, and the packaged dispatch-versus-content negative stays refused); `resolve_requirement`'s statuses, its index, its grammar and its never-open-a-path rule (re-used, not edited); and any cross-repository resolution (the residency model keeps consumers' bindings in their own trees, and this validator reads one repository).
target_release: THE NEXT ADDITIVE MINOR, DELIBERATELY NOT NUMBERED HERE — allocated AT REALIZATION by merge order per `docs/contract-versioning-policy.md`. Read at this branch's merge-base rather than remembered: `contracts/manifest.yaml:3` declares `contract_bundle_version: contract-v2.5` and `contracts/releases/contract-v2.5.digests.yaml` is a cut inventory in the tree, so the era is v2 and the next additive minor is whatever merge order allocates. A number written here would be a number another packet is already spending — `add-credential-escrow-checkout` is ratified and owes an additive minor on the SAME schema file, and `contracts/manifest.yaml` has had three writers before. THE CLASS AT THIS CUT IS ADDITIVE (MINOR): the policy's own definition (`docs/contract-versioning-policy.md:242-255`) reads "Additive (minor) — new optional fields, new contracts, NEW VALIDATOR WARNINGS", and two new validator warnings is exactly that. THE CLASS AT THE MAJOR IS BREAKING, and that is MEASURED rather than assumed — the reproduction below shows a record carrying both defects validating clean today, so refusing it later is "a shape is removed" and costs the policy's full ritual: a CHANGELOG migration note, at least one full minor of deprecation warnings, and a validator that refuses the old shape only at the new major. The removal target is contract-v3.0, the SAME major the consumer block's seven acts land at, so consumers serve ONE window rather than two.
---

# Proposal: add-requirement-ref-resolution-integrity

Status: draft
Proposed: 2026-08-31, on Brett Heap's recorded ruling of 2026-08-30 — *"successor
change with its own resolution-integrity code"* — taken over the Codex finding on
PR #516 and anchored at openxFactory issue #523, which is this packet's origin
and its scope statement both.
**RATIFICATION HAS NOT HAPPENED AND IS NOT SOUGHT BY THIS PACKET'S LANDING.**
This is a PROPOSAL-ONLY pull request on the house pattern its own subject set:
`add-binding-consumer-identity` landed as a proposal (PR #497) and its
realization came separately (PR #516). No validator line, no fixture and no
policy row moves in this pull request. Every decision the authoring session took
is listed in § Authoring decisions, flagged for veto, rather than presented as
settled.

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

Measured on a fresh clone of `origin/main` at `3a6a16e9`, 2026-08-31, against the
validator exactly as it ships — not read out of the source and not remembered.

### 1. The defect reproduces, and it reproduces silently

A repository holding two files. `credentials/example.requirements.yaml` declares
three requirements: `alpha_lane`, and `dup_lane` TWICE — once
`workload_identity`, once `dispatch_only`, so the two matches differ in exactly
the field the lift turns on. `credentials/example.binding-template.yaml` declares
two bindings with DISTINCT secret references, each with a full consumer block:

- `zero_resolving_lane` -> `requirement_id: no_such_requirement` (resolves to ZERO)
- `multi_resolving_lane` -> `requirement_id: dup_lane` (resolves to TWO, with
  different access modes)

Both document references are grammatical and both name a document the validator
indexed. The run:

```text
self-test: 6 positive + 16 negative + 10 warning example(s) confirmed, 8 deprecation code(s) probed

repro: 2 contract(s) checked, 0 skipped, 0 warning(s), 0 error(s) -> PASS
```

**Zero warnings. Zero errors. PASS.**

### 2. One byte turns it into a finding

The same tree with `example-secret-two` changed to `example-secret-one` — the
two bindings now share a secret reference, and nothing else moves — plus the
acknowledgment both bindings need to reach the fifth lift condition:

```text
ERROR credentials/example.binding-template.yaml: shared-secret-identity: bindings
'zero_resolving_lane' and 'multi_resolving_lane' share secret_ref
'example-secret-one'; … The two-consumer lift is UNAVAILABLE here: binding
'zero_resolving_lane''s requirement_ref resolves to no requirement in the
repository under validation

control: 2 contract(s) checked, 0 skipped, 0 warning(s), 1 error(s) -> FAIL
```

The validator can see the dangling reference perfectly well. It looks only where
an exemption was being requested.

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

Measured on this branch's base:

- `openspec/specs/credential-contracts/spec.md` carries SEVEN requirement titles.
  Neither *"A credential binding declares the consuming system that holds it and
  the identity it fetches with"* nor *"Two bindings on one secret are refused
  unless every pair declares distinct consumers…"* is among them.
- Both are ADDED by `add-binding-consumer-identity`, which is ACTIVE
  (`openspec/changes/add-binding-consumer-identity/`), ratified 2026-08-29, and
  unarchived.

So a MODIFIED block over either of them would be exactly the governed shape: a
marker, and an archive-order hold putting this packet behind its sibling's
archive. **A pure ADDED requirement serves instead**, because the reporting duty
is a duty this capability does not yet state anywhere — the sibling states the
duty for the reference and this states where it is owed — and neither sibling
requirement's text has to change for both to be true. **CHOSEN: two ADDED
requirements, no MODIFIED block, no marker, no hold.** The reconciliation is
performed by the new requirement's own text rather than by editing the old one.

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

Every item here is the AUTHORING SESSION'S, taken to make the packet coherent,
and none is Brett's ruling. The ruling is the one sentence in issue #523.

- **AD-1 — Two codes rather than one.** Issue #523 says "a resolution-integrity
  code", singular. This packet asks for TWO — zero and more-than-one named apart
  — on the family's own "a refusal shall name the fault it found" rule and on the
  measured fact that their remedies live in different files. If the ruling meant
  one code carrying both statuses in its message, say so and the requirement's
  second scenario is struck.
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
- **Affected siblings:** `add-binding-consumer-identity` (ACTIVE, ratified) — this
  packet MODIFIES none of its requirements and imposes no archive-order hold on
  it; `add-credential-escrow-checkout` (ACTIVE, ratified) — the other writer on
  this family's schema, which this packet does not touch.
- **Risk if not done:** the ratified general SHALL stays unenforced, and a
  binding pointing at a requirement that does not exist keeps passing — the
  fail-open shape this family has already repaired twice, once in a drift check
  and once in the access-mode arm.
