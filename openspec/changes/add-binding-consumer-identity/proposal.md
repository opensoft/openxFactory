---
code_surface: openxFactory — A SCHEMA CHANGE PLUS PACKAGED FIXTURES PLUS A VALIDATOR CHANNEL THAT DOES NOT EXIST YET. `contracts/schemas/xfactory-credential-contracts.schema.yaml` gains ONE additive optional `consumer:` block on each entry of `credential_bindings` in the existing `xfactory_credential_binding_template` (`holder_ref`, `fetch_identity`, an optional QUALIFIED `requirement_ref` carrying a requirement id plus the requirements document declaring it, and an optional const-true `shared_credential_acknowledged`). THE BLOCK IS NOT CLOSED AT THIS CUT: `additionalProperties: false` on it lands at the MAJOR, because the binding object is open today and a domain may already hold a locally shaped `consumer:` object that the current major accepts — see § What Changes. `scripts/validate-credential-contracts.py` gains (a) a WARNING channel — it has none today, it prints `ERROR` and counts errors and nothing else, so the deprecation posture below is not merely unimplemented but currently unexpressible — and (b) four finding codes: `consumer-identity-undeclared` and `consumer-block-unknown-member` (both warning now, error at the next major), the sharpened `shared-secret-identity`, and the new `shared-authority-identity`. Packaged fixtures under the existing `examples/credential-contracts/` tree: the two-consumers-of-one-operated-identity POSITIVE that the custody change had to DECLINE because the current rule refuses it, and one negative per named refusal. `tests/credential_contracts/test_dispatch_credential_contract.py` asserts the self-test count string `"3 positive + 5 negative"` verbatim at `:35` and MUST move in the same commit as the fixtures. Registration in `contracts/manifest.yaml` (the `credential-contracts` row's `sha256` and `consumption_rule`) and `contracts/CHANGELOG.md` at the cut, a `Deprecations Currently In Force` entry in `docs/contract-versioning-policy.md`, and the invariant's prose home `docs/credential-access-model.md` (whose worked binding at `:219-225` is one of the artifacts below). AND THE THREE SHIPPED ARTIFACTS THAT ALREADY WRITE THIS SHAPE, swept for rather than assumed — a settled fact is chased to the whole repository including generators: `scripts/apply-domain-starter.py:2096-2102`, which EMITS `credentials/bindings.template.yaml` into every newly scaffolded domain repository and would otherwise seed each one with a binding the new validator warns about on its first run; `docs/domain-factory-starter-pack.md:804-810`, the same template in prose; and `docs/credential-access-model.md:219-225`, the worked example. A schema field whose own scaffolder does not emit it is a field every new consumer starts out of conformance with — BUT what the scaffolder emits is a STUB, so the validator exempts `.template.yaml` and `.example.yaml` from the omission warning rather than letting a placeholder satisfy it. NOT THIS CHANGE'S SURFACE, each for a stated reason: the LIVE binding instances (residency model — `contracts/manifest.yaml` records that "openxFactory ships no instance records"); the openXdox binding (its own repository's lane); the hosting record's singular `custody.binding_id` pointer (raised as OQ-3, not resolved here); and any cross-repository comparison of two consumers' bindings (named as an owed successor in § Honest reach).
target_release: THE NEXT ADDITIVE MINOR, DELIBERATELY NOT NUMBERED HERE — allocated AT REALIZATION by merge order per `docs/contract-versioning-policy.md`. `contract-v2.1` is the declared bundle (`contracts/manifest.yaml:3`). A number written here would be a number another packet is already spending: `add-credential-escrow-checkout` is ratified and owes an additive minor on THIS SAME FILE, and the `contract-v1.28` renumber sweep is the standing precedent for why a proposal must not spend a minor before merge order is known. THE CLASS IS ADDITIVE (MINOR) TODAY AND BREAKING (MAJOR) LATER, and the policy's own three-class definition (`docs/contract-versioning-policy.md:242-255`) is what makes that a sequence rather than a preference: "Additive (minor) — new optional fields, new contracts, new validator warnings" covers the block and the warning exactly; "Breaking (major) — a required field is added ... Requires: a CHANGELOG migration note, at least one full minor release where the old shape produced deprecation warnings, and an update to the conformance validator that accepts the new shape and rejects the old one only at the new major version" is what making `consumer:` REQUIRED costs, and the full minor of warnings that clause demands is the one THIS cut begins serving. So the required-at target is the next MAJOR (`contract-v3.0` at today's numbering) and it is named in the deprecation entry rather than executed here. A binding declaring no `consumer:` block stays VALID at this cut, a binding already carrying a locally shaped `consumer:` object stays VALID at this cut TOO (it warns), every consumer pinned at `contract-v2.1` stays conformant until it upgrades, and NOTHING NARROWS — which is a property this packet had to be corrected into: the first draft closed the block in the same minor, which would have refused an existing record the current major accepts. Both the requiredness AND the closure land at the major, for the same clause and the same reason.
---

# Proposal: add-binding-consumer-identity

Status: draft
Proposed: 2026-08-29, on Brett Heap's in-session lane authorization of the same
day. **RATIFICATION HAS NOT HAPPENED AND IS NOT SOUGHT BY THIS PACKET'S
LANDING.** This packet is authored to be read adversarially by a §7.4-shaped
council convened OUTSIDE the clearance pipeline — proposals are
never-convenable through it, unanimously, 2026-08-28 — and every decision the
authoring session took is listed in § Authoring decisions put to the council
rather than presented as settled. Brett's authorization covers AUTHORING this
proposal; it covers none of its content.

## Why

**A ratified requirement in this repository makes a claim its own record cannot
show, and the packet that ratified it said so five times — in its requirement's
own scenario, its Impact section, its design, its task list §4.5 and its
ratification record — rather than letting the claim stand.**

`add-notebook-hosting-credential-custody` (ratified 2026-08-23) established
one-identity / per-system-authority for a shared operated identity. Its
requirement text is unambiguous:

> Where more than one system authenticates as the SAME operated identity, each
> consuming system SHALL reach that identity's credential through its OWN
> binding: its own access identity against the secret store, its own grant, its
> own rotation visibility, and its own audit trail. One identity MAY be shared;
> one AUTHORITY SHALL NOT.

And the same packet recorded, in its own scenario, that the record cannot carry
what makes two bindings two AUTHORITIES:

> **WHEN** two bindings for one operated identity are recorded in the promoted
> binding-template shape
> **THEN** the shape carries no consumer or access-identity field, so the
> per-system authority is asserted by the binding's owner and its estate wiring
> rather than proven by the record
> **AND** the gap is recorded as owed to a successor that extends the shape, not
> left implied as enforced

The gap is not abstract, and the claim it undermines is already in a shipped
document. `docs/lifecycle-notebook-projection.md:576-579` states as realized
fact: *"The xFactory sync lane and openXdox each hold their own access identity
against the store, their own grant, their own rotation visibility, and their own
audit trail."* Nothing in any binding record says which system a binding belongs
to, and nothing says which identity it fetches with. A reader who wants to know
which of the two the sentence is about has no record to consult.

**Three facts were MEASURED in the working checkout on 2026-08-29 rather than
carried from the ratified packet's description of them.**

1. `xfactory_credential_binding_template` requires `[provider, secret_ref,
   owner, rotation_policy]` per binding with `vault` optional, and declares no
   other properties
   (`contracts/schemas/xfactory-credential-contracts.schema.yaml:135-147`).
2. `scripts/validate-credential-contracts.py` compares no authorities. Its one
   cross-binding check, `shared-secret-identity` (`:115-129`), fires on a
   duplicate `secret_ref` **within one document** and reads nothing else.
3. **The binding object carries no `additionalProperties: false`, so a
   `consumer:` key with arbitrary contents VALIDATES AGAINST THE PINNED SCHEMA
   TODAY.** Executed against the schema on 2026-08-29: a binding carrying
   `consumer: {holder_ref: …, fetch_identity: …, totally: unchecked}` produced
   zero errors. This is not a missing field; it is a field-shaped hole. It is
   the same defect this schema's own `issuance_preconditions` design names one
   record kind over — *"the mechanism existed as a domain-local extra key riding
   a neutral schema that neither declared nor forbade it, so a refusal had no
   neutral home to be declared against"* (`:57-68`) — and the remedy taken there
   is the remedy taken here.

**And canon already names the two things a lane receives; the schema carries
one of them.** Promoted `credential-contracts` says the consuming lane receives
*"only bindings: an opaque secret reference and a fetch-identity identifier"*,
and its sibling requirement says a credential is *"delivered BY REFERENCE — a
vault URI plus the runtime's own fetch identity"*. `secret_ref` is in the shape.
The fetch identity is not in the shape at all. That is the sharpest statement of
the gap available, and it comes from canon rather than from this packet.

## What Changes

**One additive optional block, in vocabulary this estate has already ratified
and shipped.** Each entry of `credential_bindings` MAY declare:

```yaml
consumer:
  holder_ref: opsx:service-subject:aks-opensoft-qa   # WHO holds this binding
  fetch_identity: <identifier>                       # the identity it authenticates to the store with
  requirement_ref:                                   # optional; QUALIFIED, never a bare id
    requirement_id: <identifier>
    requirements_document_ref: <path>
  shared_credential_acknowledged: true               # optional const true; see the lift below
```

**The requirement reference is QUALIFIED, and a bare id was rejected for a
reason a bot found before the council did.** This schema requires only a string
`id` on a requirement and imposes no repository-wide uniqueness, while
`scripts/validate-credential-contracts.py` scans a whole `credentials/` tree —
so one id may match records in several documents whose `access_mode` DIFFERS. A
rule resolving a bare id could lift the refusal on a non-dispatch match while a
dispatch-only match stood beside it, and which it found would depend on
traversal order. The qualified shape is `identity-brokering`'s own
`credential_reference` pair (`requirement_id` + `requirements_document_ref`),
which is the second half of the composition this change is already making.

Neither identifier invents a naming scheme, and that is deliberate:

- **`holder_ref` is `identity-brokering`'s own spelling, already shipped and
  digest-pinned at `contract-v1.37`** — `contracts/identity-brokering/broker-client-declaration.schema.yaml:113-121`
  and two sibling schemas define a `credential_reference` whose members are
  `[requirement_id, requirements_document_ref, holder_ref, custody_declared_in]`,
  and the packaged examples spell live values `opsx:service-subject:aks-opensoft-qa`.
  That family points from a CONSUMER's declaration at a credential requirement
  and names the holder; this change points from the BINDING back and names the
  same holder with the same word. A consuming system is emphatically NOT a
  persona — `identity-brokering`'s "Workloads are not personas" forbids it and
  routes non-human authority to *"`credential-contracts` grants and `openxwallet`
  holders"* — so `holder_ref`, not a subject and not a persona reference.
- **`fetch_identity` is promoted `credential-contracts`'s own words**, from the
  two requirements quoted above. The block adds no term the capability does not
  already use.

**THE BLOCK IS DECLARED NOW AND CLOSED AT THE MAJOR, and the two-step is not
tidiness.** The binding object is open TODAY, so a domain may already hold a
binding carrying a locally shaped `consumer:` object that the current major
accepts. Declaring the members AND refusing every other member in one minor
would refuse that record — a NARROWING wearing an additive label, and the one
thing `docs/contract-versioning-policy.md` § Compatibility Direction forbids
outright. So the closure serves the same deprecation the requiredness does:
`consumer-block-unknown-member` WARNS at this cut and becomes an error at the
major, alongside `consumer-identity-undeclared`. Same clause, same reason, same
release.

**A TEMPLATE IS EXEMPT, because a conforming placeholder is worse than an
absent field.** `.template.yaml` and `.example.yaml` instantiation stubs declare
no consuming system because none exists when they are written. Forcing the field
onto them yields either a `<placeholder>` that fails the identifier grammar or a
grammar-passing sentinel that suppresses the warning and reads as an authority
fact while naming nothing. Neither warning nor major refusal applies to a stub.

**The refusal is sharpened, and it is sharpened by TIGHTENING FIRST.** Nothing
that validates today becomes invalid at this cut, and nothing that is refused
today becomes accepted by default:

- `shared-secret-identity` keeps its predicate and its refusal as the DEFAULT.
- **One narrow lift, fail-closed on every precondition.** Two bindings sharing a
  `secret_ref` are permitted ONLY when BOTH declare a `consumer:` block, their
  `holder_ref`s differ, their `fetch_identity`s differ, BOTH declare
  `shared_credential_acknowledged: true`, and BOTH name a QUALIFIED
  `requirement_ref` resolving in the same repository to EXACTLY ONE requirement,
  with equal `access_mode` that is not `dispatch_only`. Silence, a shared
  `holder_ref`, a shared `fetch_identity`, a one-sided acknowledgment, a
  reference resolving to zero OR to more than one record, and a mixed or
  dispatch-only access mode each leave the refusal standing — ambiguity is
  treated as unreadability, never resolved by picking one match. This is what closes the laundering route the
  lift would otherwise open: the dispatch/content collapse the rule exists to
  refuse cannot buy its way past by declaring itself intentional.
- **`shared-authority-identity` is NEW and it is a tightening.** Two bindings on
  one `secret_ref` whose `fetch_identity` is the SAME are refused under a code
  that names the actual fault — two systems, one authority — rather than under a
  code about secret reuse. Today that record validates cleanly whenever the two
  bindings are the estate's real shape; making it a named refusal is the whole
  of "the invariant is held by review" becoming "the invariant is held by the
  record".
- `consumer-identity-undeclared` warns on a binding that declares no block, and
  `consumer-block-unknown-member` warns on a member outside the declared set;
  both become errors at the next major. See the front-matter for why the policy
  makes that a sequence rather than a choice.

**The migration posture is additive-optional-first, required-at-next-major**,
and the alternative was not available: `docs/contract-versioning-policy.md:250-254`
makes "a required field is added" the BREAKING class and conditions it on "at
least one full minor release where the old shape produced deprecation
warnings". Requiring `consumer:` at this cut would skip a precondition the
policy states, so the real question put to the council is not whether to phase
but which major and whether the warnings are registered as formal deprecations
(OQ-1). The same clause governs the CLOSURE, which is why both halves phase
together rather than the block arriving closed.

## The other writer on this file, and how the two are ordered

`add-credential-escrow-checkout` is RATIFIED (2026-08-28) and ACTIVE, and it
adds an additive optional `escrow:` block to the SAME binding kind plus a sixth
record kind, owing its own additive minor on the same schema file. Two facts
follow and neither is left implicit:

1. **The blocks are orthogonal and neither narrows the other.** `escrow:`
   answers "who else can obtain this credential"; `consumer:` answers "who holds
   this binding and fetches with what". A binding may carry both, either, or
   neither. Realization order does not matter to the shapes; it matters only to
   which cut carries which row, and both are allocated at realization.
2. **This change does NOT touch "Canonical credential record shapes", and that
   is a decision rather than an omission** — D-1 below.

**The requirement this change DOES modify is the custody change's**, and this
proposal names that change explicitly for the reason
`release-realization`'s "Ordered deltas and branch vocabulary" requires: *"a
proposal modifying a requirement already modified by an active ratified change
references that change and declares its deltas relative to that change's
outcome."* The delta here is declared relative to
`add-notebook-hosting-credential-custody`'s outcome, carries that requirement's
body and five of its six scenarios verbatim, and replaces exactly the sixth —
the scenario recording that the shape cannot express the access identity, which
this change makes false. The dependency runs one way and is stated as a task:
this change MUST NOT archive before the custody change archives, and if the
order ever inverted, the block converts to `ADDED` before archiving rather than
promoting a MODIFIED requirement canon does not hold.

## Honest reach — what this makes provable, and what it does not

Recorded here rather than discovered later, on the custody packet's own
precedent of naming the gap instead of implying enforcement.

- **A consumer identity makes revocation of ACCESS attributable and actionable
  from the record.** Which grant to revoke, and whose future fetches stop, is a
  lookup rather than an inference, and the store's access log becomes
  reconcilable against a declaration.
- **It does NOT un-share a bearer secret already fetched.** Revoking a
  `fetch_identity`'s grant stops future fetches and nothing more; it cannot
  un-disclose a password already read or end a session already established with
  it. Evicting a consumer that holds the secret still requires ROTATION, and
  rotation still reaches every consumer of that identity. That is a property of
  the credential class, it is unchanged by this change, and the custody
  requirement already says so — this packet restates it rather than letting a
  new field read as new containment.
- **The CHECK is intra-document; the ESTATE is not.** Every rule above compares
  bindings within one template, because `scripts/validate-credential-contracts.py`
  is a per-repository validator run against one domain repo's `credentials/`
  tree. The live two-consumer case spans repositories: the xFactory sync-lane
  binding lives in the install's `credentials/` tree, and openXdox declares its
  own in its own repository. **No per-repository validator can compare them, and
  this change does not claim to.** What it delivers there is READABILITY — each
  binding says who holds it and what it fetches with, wherever it lives — and
  the cross-repository comparison is named as an owed successor, in the same
  form and for the same reason the custody change named this one.
- **The two live consumers are named as consumers, not delivered.** The
  xFactory sync lane and openXdox are what this change makes checkable; their
  binding instances remain their own repositories' acts under the residency
  model, exactly as ratified on 2026-08-23.

## Impact

- **Affected specs.** `credential-contracts` — 1 MODIFIED requirement (the
  custody change's per-system-authority requirement, declared relative to its
  outcome) and 3 ADDED requirements (the block; the sharpened refusal; the
  honest reach).
- **Affected code, at realization**: as enumerated in `code_surface`.
- **`contracts/` IS touched AT REALIZATION, and a cut IS owed then.** Unlike its
  predecessor, this change's realization moves schema bytes. THIS PACKET MOVES
  NONE: its own diff is the delta and these records, `contracts/` is untouched
  by it, and it cuts nothing — allocation is at realization by merge order.
- **No live secret is created, moved, or read by this change**, and none is by
  its realization either. The block names identifiers; it holds no material.
- **Every consumer pinned at `contract-v2.1` stays conformant until it
  upgrades.** The block is optional, the warning is a warning, and the
  compatibility direction (`docs/contract-versioning-policy.md:267-272`) forbids
  a new release retroactively invalidating an old pin.

## Authoring decisions put to the council

Every one of these was taken by the authoring session. None is Brett's, none is
ratified, and each is stated with the alternative that was rejected so a seat
can rule the other way on the record.

**D-1. The delta modifies the CUSTODY requirement and deliberately does NOT
modify "Canonical credential record shapes".** `add-credential-escrow-checkout`
modified that requirement, so the sibling precedent points the other way.
Reasoning for the split: escrow's modification was FORCED — canon's requirement
ENUMERATES the record kinds, and a sixth kind falsifies three sentences the
moment it exists. This change adds no kind, so no sentence of that requirement
becomes false, while the custody requirement contains a scenario that this
change DOES falsify. Modifying the requirement whose text goes stale, and
leaving alone the one whose text does not, is the narrower act. It also declines
to create a third instance of an open defect class: two lossy sibling deltas are
already filed as issues #329 and #330. REJECTED ALTERNATIVE: modify both, on the
symmetry argument that a block the schema owns should be registered where the
schema's owned shapes are listed. A seat may reasonably prefer that; the cost is
a second live writer on a requirement that already has one, and a
carriage-ledger row in `tests/doc-health/test_modified_block_currency_self_gate.py`
owed in the same commit.

**D-2. `requirement_ref` is in the block at all, and it is QUALIFIED.** It is
the field that makes the lift safe: without a resolvable requirement on both
sides, the validator cannot see that a dispatch-only credential and a
content-write credential are being declared "one shared credential", and the
lift becomes the laundering route for the exact collapse `shared-secret-identity`
exists to refuse. It is optional on the block and REQUIRED for the lift, so the
ordinary binding pays nothing. TWO REJECTED ALTERNATIVES, and the second was
rejected only after a bot round found it: (a) rely on the convention that the
`credential_bindings` map key IS the requirement id — only a convention, since
the schema says `additionalProperties` and enforces no key grammar, and a safety
precondition resting on an unenforced convention is not a precondition; (b) a
BARE requirement id, which the packet carried until Codex pointed out that this
schema imposes no repository-wide uniqueness on requirement ids while the
validator scans a whole tree, so one id may match records with different access
modes and the lift's outcome would depend on traversal order.

**D-3. The lift exists at all.** REJECTED ALTERNATIVE: keep
`shared-secret-identity` absolute, express the two-consumer shape only across
documents, and ship no positive fixture — which is what the custody change did,
under protest, when it DECLINED its packaged example for exactly this reason.
Reasoning for lifting: the custody packet's own task §4.1 hands this decision
forward in terms — *"it must first decide whether `shared-secret-identity`
should distinguish 'two credentials collapsed into one' from 'two consumers of
one credential'"* — and a rule that cannot express a shape the family has
ratified will be worked around rather than obeyed. A seat that thinks the
laundering risk outweighs the expressiveness should say so; the packet is
buildable without the lift by deleting one clause.

**D-4. `shared_credential_acknowledged` is a const-true declaration rather than
a boolean.** Following `issuance_preconditions` verbatim: *"a precondition is
DECLARED or NOT DECLARED — `false` is not a second meaning, it is a declaration
that reads as governance while asserting nothing."* REJECTED ALTERNATIVE: a
plain boolean, which admits a record asserting `false` beside a shared secret.

**D-5. `holder_ref` reuses identity-brokering's spelling rather than defining a
consumer id of its own, and does NOT require a wallet reference.** See design.md
§ The wallet question for the full reasoning and the rejected alternatives.

## Open questions carrying recommendations, not decisions

**OQ-1. Is the omission warning registered as a formal deprecation?**
Recommendation: YES — add an entry to `docs/contract-versioning-policy.md`
§ Deprecations Currently In Force naming the removal version, because that
section is where a consumer upgrading across the removal looks, and the policy's
own § Deprecations Executed says a deprecation that never appeared there is
indistinguishable from one that was never honoured.

**OQ-2. Which major requires the block AND closes it?** Both breaking halves
land together. Recommendation: the next major after this change's minor
(`contract-v3.0` at today's numbering), named in the deprecation entries rather
than in the schema. A seat may want them separated — closure at one major,
requiredness at a later one — on the argument that a domain can adopt the
declared members long before it can name a consumer for every binding.

**OQ-3. Does the hosting record's custody pointer become plural?**
`examples/notebook-projection-hosting.yaml` names a SINGLE `custody.binding_id`,
while the requirement it discharges says each consuming system has its own
binding. With consumers on the binding, which consumer the pointer resolves to
becomes readable — but the pointer is still one. Recommendation: leave it
singular in this change and raise the question with the record's owning
capability, because widening it is a `lifecycle-notebook-projection` act and
this packet is a `credential-contracts` one.

**OQ-4. Should `fetch_identity` resolve to a client-identity-roster entry where
one exists?** The roster already reaches into this capability through the
`roster_drift_clear_required` issuance precondition, so the composition is not
novel. Recommendation: NO requirement in this change — the roster's population
is identities standing in a CLIENT's provider tenant, and a lane's vault fetch
identity may or may not be one — but the identifier grammar admits a roster
reference, and the tightening is named as a successor rather than foreclosed.

**OQ-5. Is the degraded fetch-identity mode declarable?** Promoted
`credential-contracts` permits service-scoped materialization "where a per-install
fetch identity does not yet exist" and requires the rotation cost to "be recorded
as a gap" — with no machine-readable home for that record. Recommendation: OUT
of this change (it is a second field with its own vocabulary question), named
as a successor. A seat may rule it belongs here, since the field it would ride
is the one this change adds.
