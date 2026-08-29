---
code_surface: openxFactory — A SCHEMA CHANGE PLUS PACKAGED FIXTURES PLUS A VALIDATOR CHANNEL THAT DOES NOT EXIST YET. `contracts/schemas/xfactory-credential-contracts.schema.yaml` gains ONE additive optional `consumer:` block on each entry of `credential_bindings` in the existing `xfactory_credential_binding_template`, DECLARED AT THIS MINOR AS AN ANNOTATION ONLY — no `type`, no member grammar, no `required:`, no `additionalProperties: false`. Its members (`holder_ref`, `fetch_identity`, a qualified `requirement_ref` of `requirement_id` + a repository-relative `requirements_document_ref`, a const-true `shared_credential_acknowledged`, and a const-true `instantiation_stub`) are described in the schema and enforced only at the MAJOR, where the breaking acts land together: requiredness, closure, the member grammar, the const-true token enforcement, the map-key grammar, the `access_mode` vocabulary and the `requirements_document_ref` grammar — one release, one deprecation window, eight codes serving it. The schema also gains a grammar on the `credential_bindings` MAP KEY and a closed `access_mode` vocabulary — both preconditions of the lift, not decoration. `scripts/validate-credential-contracts.py` gains (a) a WARNING channel — it has none today, it prints `ERROR` and counts errors and nothing else — and (b) EIGHT deprecation codes, one per shape the major will refuse — `consumer-identity-undeclared`, `consumer-block-incomplete`, `consumer-block-unknown-member`, `consumer-member-grammar`, `consumer-token-not-true`, `consumer-binding-key-grammar`, `consumer-access-mode-vocabulary` and `consumer-requirement-ref-grammar` (all eight WARN at this minor and ERROR at the major) — plus the sharpened `shared-secret-identity` and the new `shared-authority-identity`; it also extends `_looks_like_raw_secret` over `consumer.holder_ref` and `consumer.fetch_identity` under `baked-secret`, and REPLACES its first-against-rest `seen`-map with an every-pair comparison. Packaged fixtures under the existing `examples/credential-contracts/` tree — including a `warning/` directory and a `WARNING_EXPECTATIONS` map the self-test does not have today, without which the deprecation the major depends on ships with no probe — and every new fixture joins the by-name inventory at `tests/credential_contracts/test_dispatch_credential_contract.py:38-51` in the same commit. That file also asserts the self-test count string verbatim at `:35`; the count is DERIVED rather than asserted, in its own issue rather than here. Registration in `contracts/manifest.yaml` and `contracts/CHANGELOG.md` at the cut, a `Deprecations Currently In Force` entry in `docs/contract-versioning-policy.md` naming ALL of the acts that land at the major, and `docs/credential-access-model.md` — whose worked binding at `:219-225` is one of the artifacts below and whose `:228-229` no-raw-secret sentence is extended to the new fields in the same commit. AND THE SHIPPED ARTIFACTS THAT ALREADY WRITE THIS SHAPE, swept for rather than assumed: `scripts/apply-domain-starter.py:2096-2102`, which EMITS `credentials/bindings.template.yaml` into every newly scaffolded domain repository and which SHALL emit exactly `consumer: {instantiation_stub: true}` and nothing else — not a placeholder, which fails the identifier grammar, and not an omission, which a bot round proved cannot stay clean at the major because a missing block is an error there and the stub token is the only exemption; `docs/domain-factory-starter-pack.md:804-810`, the same template in prose; `docs/credential-access-model.md:219-225`, the worked example; and `contracts/avatar-client/broker-server-key-binding.template.yaml`, a SHIPPED record of this very kind carrying `resolution.fetch_identity` — named, reconciled and scoped rather than left unmentioned. The full sweep command returns THIRTEEN paths and each carries a stated in/out disposition. NOT THIS CHANGE'S SURFACE, each for a stated reason: the LIVE binding instances (residency model); the openXdox binding (its own repository's lane); the hosting record's singular `custody.binding_id` pointer (OQ-3); and any cross-repository comparison of two consumers' bindings (an owed successor in § Honest reach).
target_release: THE NEXT ADDITIVE MINOR, DELIBERATELY NOT NUMBERED HERE — allocated AT REALIZATION by merge order per `docs/contract-versioning-policy.md`. `contract-v2.1` is the bundle at this branch's merge-base and `origin/main` has since advanced to `contract-v2.2`; the figure is re-read at the ratification act, since the whole compatibility argument is indexed to a bundle. A number written here would be a number another packet is already spending: `add-credential-escrow-checkout` is ratified and owes an additive minor on THIS SAME FILE, and `contracts/manifest.yaml` now has THREE writers rather than two, main included. THE CLASS IS ADDITIVE (MINOR) TODAY AND BREAKING (MAJOR) LATER, and the policy's own three-class definition (`docs/contract-versioning-policy.md:242-255`) is what makes that a sequence rather than a preference: "Additive (minor) — new optional fields, new contracts, new validator warnings" covers an annotation-only declaration and its warnings exactly; "Breaking (major) — a required field is added, a shape is removed … Requires: a CHANGELOG migration note, at least one full minor release where the old shape produced deprecation warnings, and an update to the conformance validator that accepts the new shape and rejects the old one only at the new major version" is what EVERY act in this change that refuses a value the current major accepts costs — requiredness, the block's closure, the member grammar, the const-true token enforcement, the map-key grammar, the `access_mode` vocabulary and the `requirements_document_ref` grammar. SEVEN breaking acts, one release, one deprecation window, eight codes serving it. The count moved four times under review, which is why the packet now states the TEST rather than the tally: an act phases if the current major accepts the value it would refuse — regardless of whether it sits on the block, on the map, on a neighbouring record, in the schema or in the validator. NOTHING NARROWS AT THIS CUT, AND THAT IS NOW VERIFIED BY CONSTRUCTION RATHER THAN ASSERTED: the prescribed minor schema was built and driven against every shape a domain could already hold — a locally shaped object with neither declared member, a scalar, a list, placeholder-styled values, an undeclared extra member, and no block at all — and all six validate at the minor exactly as they validate today. The first draft of this packet claimed that property while prescribing a `required:` list that refused three of them; four council seats found it independently and it is repaired here. Every consumer pinned at the prior bundle stays conformant until it upgrades.
---

# Proposal: add-binding-consumer-identity

Status: draft
**NOT YET RATIFIED** — the `Status:` header above carries the controlled
taxonomy value and cannot say so itself, so it is said here. (A first attempt
put the words in the header and `doc-health`'s `status-validity` family refused
it as a free-form status; the refusal was right and the fix is this line.)
Proposed: 2026-08-29, on Brett Heap's in-session lane authorization of the same
day. Council-reviewed 2026-08-29 (§7.4 sitting, split 2–2 on the word, unanimous
4/4 that the text as drafted was not ratifiable); **Brett ruled the same day:
accept all blocking amendments, one fix round, ratification read after.** This
revision is that round. **RATIFICATION HAS NOT HAPPENED.** Brett's authorization
covers AUTHORING this proposal and RULING on the council's amendments; it covers
none of this packet's own content, and the ratification act is still to come.

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
    requirement_id: <identifier>                     # MUST equal this binding's map key
    requirements_document_ref: <repository-relative path>
  shared_credential_acknowledged: true               # optional const true; see the lift below
  instantiation_stub: true                           # optional const true; a stub, declared not named
```

**The requirement reference is QUALIFIED, its document reference carries a
grammar, and its id is bound to the binding.** Each of those three is a repair
of a defect found by execution rather than by reading. A bare id resolves
ambiguously — this schema imposes no repository-wide uniqueness while the
validator scans a whole `credentials/` tree. A borrowed `requirements_document_ref`
carries no pattern, no resolution rule and no reader anywhere in this repository,
so promoting it to a security precondition without a grammar would rest that
precondition on an unenforced convention — the very objection this packet raises
against the map key. And a reference the author points wherever they like is not
a precondition at all: **the packaged dispatch-versus-content negative, this
capability's only red proof of serving-tier separation, is admitted by the
five-condition lift with four declarations added and its shared secret
untouched.** So the reference must name the binding it sits on, and the map key
it names must be constrained by the schema rather than trusted as a convention.

None of the three references invents a naming scheme, and that is deliberate:

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
  holders"* — so `holder_ref`, not a subject and not a persona reference. The
  IDENTIFIERS are reused; the two-member `requirement_ref` object is NOT that
  family's four-member block, and this packet claims only the former.
- **`fetch_identity` is promoted `credential-contracts`'s own words**, from the
  two requirements quoted above. The block adds no term the capability does not
  already use. It is not, however, this vocabulary's first appearance on this
  record kind — see § The rival that already ships.

**THE BLOCK IS DECLARED NOW AND CONSTRAINED AT THE MAJOR — ALL OF IT, NOT HALF
OF IT.** This is the packet's largest correction and it came from four council
seats reaching one finding independently. The binding object is OPEN today, so a
`consumer:` key of ANY shape validates. **Three** distinct acts would each refuse
a shape the current major accepts:

| act | what it refuses that validates today |
| --- | --- |
| `required: [holder_ref, fetch_identity]` | a locally shaped object carrying neither |
| `additionalProperties: false` | a locally shaped object carrying extra members |
| the identifier `pattern` | any value not matching the grammar, placeholders included |

The first draft phased only the second. Built and driven, the prescribed minor
schema **REFUSED** a locally shaped object, a scalar, a list and the generator's
own placeholder style — every one of them valid today — while `spec.md`'s own
scenario promised they *"stay VALID … and are warned rather than refused"*. A
ratifiable scenario falsified by its own build instruction is the silent-loss
shape this estate has issues open about, and the repair is to apply the packet's
own argument at the level it stopped short of: **at the minor the schema
constrains NOTHING about the block; every constraint lands together at the
major, with one deprecation window.** Verified by construction, not by a second
prose read.

**THE STUB EXEMPTION IS A DECLARED TOKEN, NOT A FILENAME.** `.template.yaml` and
`.example.yaml` stubs declare no consuming system because none exists yet — but
keying their exemption on the path is an exemption the author writes by naming,
invisible in the bytes a pinned consumer validates, and it would let a record
carrying live values escape a required field by what it is called. Worse, it
cannot reach the layer where the refusal lands: a filename is invisible to a
pinned schema, so a validator-layer exemption can never exempt a record from a
schema-layer error — which is why the drafted acceptance test *"a freshly
scaffolded repo validates clean"* could not have passed. A const-true
`instantiation_stub` token fixes both: the schema can condition on a property,
and the generator emits exactly **`consumer: {instantiation_stub: true}`** — so a
scaffolded repository validates clean at BOTH releases. Emitting nothing was the
draft in between, and it fails at the major: a missing block is an error there
and the token is the only exemption. The token is not a third sentinel — a
placeholder `holder_ref` asserts an identity that does not exist, while the token
asserts only that the record is a stub, which is exactly true of a file written
before any install exists.
Scaffolding that manufactures conformance is worse than scaffolding that omits
it, and this packet now takes its own advice.

**The refusal is sharpened, and the sharpening is honest about direction.**

- `shared-secret-identity` keeps its predicate and its refusal as the DEFAULT.
- **One narrow lift, SIX conditions, fail-closed on every one, over EVERY PAIR.**
  Two bindings sharing a `secret_ref` are permitted only when both declare a
  `consumer:` block, their `holder_ref`s differ, their `fetch_identity`s differ,
  both declare `shared_credential_acknowledged: true`, both name a qualified
  `requirement_ref` resolving to EXACTLY ONE requirement whose `access_mode` is a
  member of a CLOSED vocabulary, equal and not `dispatch_only` — and each
  reference's `requirement_id` EQUALS ITS OWN BINDING'S MAP KEY. The sixth
  condition is what makes the other five mean anything.
- **The arity is every pair.** The inherited predicate keeps the FIRST binding
  per secret and compares later ones against it, so with three bindings the
  second and third are never compared — and a record where those two share a
  fetch identity ships the authority collapse and is accepted. The shape is
  REPLACED, not extended.
- **An unreadable access mode is UNAVAILABLE, not satisfied.** Today the field is
  an unconstrained string compared to one exact spelling, so two absent modes
  compare equal and a variant spelling compares equal to itself — both lift. The
  vocabulary is closed and unreadable means unavailable, which is the rule this
  estate already learned from a fail-open drift check.
- **`shared-authority-identity` is NEW, and it is not scoped to a shared secret
  reference.** Two different holders declaring one fetch identity is the
  authority collapse whatever their `secret_ref`s; scoping the finding to the
  proxy would leave the same collapse unreported when two spellings name one
  secret. One holder reusing its own fetch identity across its own bindings is
  not the fault and is not reported.
- **EIGHT warning codes, ENUMERATED AGAINST THE REFUSALS rather than counted.**
  One per shape the major will refuse: no block; a block present but incomplete;
  an undeclared member; a member failing the grammar; a const-true token declared
  false; a map key outside the key grammar; an `access_mode` outside the
  vocabulary; a `requirements_document_ref` outside the path grammar. **FIVE of
  the eight were added by bot rounds on the fix round itself** — an empty
  `consumer: {}` matched none of the original three; the map-key grammar was
  prescribed with no phasing while its two neighbours had it; the false-token
  refusal was written as an immediate error though such a record validates today;
  and `access_mode` and the document reference both declared their phasing in
  prose and had no code to serve it. **Every one is the same defect the council
  convened over, recurring inside its own repair** — which is why the rule is now
  stated as a rule: *the warning set is derived from the list of things the major
  refuses, and a shape that no code names is a shape the deprecation does not
  serve.* This is the strongest argument the packet can make for why a verifier,
  not a reader, is what finds this class.
- **The two new fields are screened.** `holder_ref` and `fetch_identity` are free
  strings on the one record kind whose invariant is "never bake a secret", and
  the existing screen reads `secret_ref` and nothing else — a raw token in either
  new field produces zero findings today. Both join the `baked-secret` screen,
  with a registered negative per field.
- **AND WHAT THIS CUT ACTUALLY DOES TO THE REFUSAL SET IS STATED PLAINLY.**
  Enumerated, the validator's refusal set at this cut strictly SHRINKS: zero
  records are newly refused and one shape — the fully declared six-condition
  lift — is newly accepted. The tightening lands on the SCHEMA at the major and
  in the new warnings now. An earlier draft of this section read as though the
  refusal set grew; it does not, and the sentence is corrected rather than
  defended.

**The migration posture is declare-now / constrain-at-the-major**, and the
alternative was not available: `docs/contract-versioning-policy.md:250-254` makes
"a required field is added" and a removed shape the BREAKING class and conditions
both on "at least one full minor release where the old shape produced deprecation
warnings". The real questions put to the council were which major and whether the
warnings are registered as formal deprecations (OQ-1), and both are now settled
below.

## The rival that already ships, named rather than disclaimed

D-5's whole content is *"reuses vocabulary rather than creating a rival"*, and
that premise was false in shipped contract bytes when this packet first claimed
it. `contracts/avatar-client/broker-server-key-binding.template.yaml` declares
`kind: xfactory_credential_binding_template` — **this very kind** — and carries,
validating against the pinned schema with ZERO errors:

```
top-level keys : change_id, client, credential_bindings, kind, owning_task,
                 release_ring, requirement, requirement_id, resolution, ruled,
                 schema_version, source          (nine of them undeclared)
resolution     : fetch_identity          = install_federated_workload_identity
                 degraded_mode_permitted = true
requirement_id : ALV-006
```

So `fetch_identity` and `requirement_id` are not new names on this kind; they are
SECOND homes for facts an existing artifact already records at document level.
Three consequences, and none is discharged by a disclaimer:

1. **One kind, two homes for one fact, and nothing reconciles them.** After this
   change a document could declare `resolution.fetch_identity: A` and
   `credential_bindings.x.consumer.fetch_identity: B` and pass both validators.
   The estate has written the doctrine against exactly this, on the very family
   this packet borrows from: *"Composition, not a second custody vocabulary: this
   family states WHERE custody is declared and never restates the declaration, so
   the two cannot disagree."* **THE RULING THIS PACKET PUTS TO THE COUNCIL AND
   ADOPTS: the `consumer:` block is the ONE home for a fetch identity on a
   PER-BINDING basis, and `resolution.fetch_identity` is a DOCUMENT-LEVEL
   declaration of a different scope — one install's resolution posture, not one
   binding's holder.** They are not two spellings of one fact; they are two
   scopes, and the reconciliation is that a per-binding declaration, where
   present, is the operative one for that binding. That ruling is stated here so
   it can be refused; it was not stated at all before.
2. **The hole this packet measured already has a writer, and it is openxFactory's
   own `contracts/` tree.** The measurement found the hole; it did not ask who was
   using it. That artifact's `resolution:` block IS the hole, at document level,
   unprotected by a `consumer:`-scoped closure and — before this section —
   unmentioned.
3. **Two validators read one kind with divergent rules.**
   `scripts/validate-credential-contracts.py` scans only `<repo>/credentials/`
   and never sees the file; `scripts/validate-avatar-client.py` declares the same
   `BINDING_KIND` and enforces its own. **Scope ruling: `validate-avatar-client.py`
   is OUT of this change** — it is the avatar family's surface and this change
   adds no obligation to it — but the divergence is named as an owed successor
   rather than widened silently.

And the same artifact settles OQ-5's premise: it ships `degraded_mode_permitted:
true` beside a note citing the same canon sentence, so *"no machine-readable
home"* was false. The recommendation to keep the degraded mode out of this change
survives on capability-boundary and test-load grounds; its stated reason does not,
and is replaced.

## The other writer on this file, and how the two are ordered

`add-credential-escrow-checkout` is RATIFIED (2026-08-28) and ACTIVE, and it
adds an additive optional `escrow:` block to the SAME binding kind plus a sixth
record kind, owing its own additive minor on the same schema file. Two facts
follow and neither is left implicit:

1. **The blocks are orthogonal and neither narrows the other.** `escrow:`
   answers "who else can obtain this credential"; `consumer:` answers "who holds
   this binding and fetches with what". A binding may carry both, either, or
   neither. Realization order does not matter to the shapes; it matters only to
   which cut carries which row.
2. **The cut coordination binds only ONE of the two parties, and saying so is
   the honest form.** This packet's task 5.4 tells whichever cuts second to
   re-read the file. Escrow is RATIFIED and therefore frozen, makes no mention of
   this change, and carries no concurrent-writer re-read in any of its nine
   schema tasks — so if escrow cuts second, nothing in escrow's own governing
   list tells it to. The invariant currently depends on the second cutter having
   read a task in the other packet, which is a hope. **The remedy adopted here is
   to make it machine-checked rather than reciprocal**: a realization gate that
   recomputes the `credential-contracts` manifest digest from the file on disk at
   cut time and refuses a mismatch binds both parties without editing a frozen
   packet. Three further collisions are named with it: escrow places fixtures
   under a NEW `contracts/credentials/examples/` tree while this validator's
   `EXAMPLES_DIR` is one hard-coded path; both packets edit the same manifest
   row; and `contracts/manifest.yaml` now has a THIRD writer, main itself, which
   moved it 27/11 between this branch's merge-base and today.
3. **This change does NOT touch "Canonical credential record shapes", and that
   is a decision rather than an omission** — D-1 below.

**The requirement this change DOES modify is the custody change's**, and this
proposal names that change explicitly. **The citation is an EXTENSION, not an
application, and the earlier draft overstated it.** `release-realization`'s
"Ordered deltas and branch vocabulary" reads *"a proposal modifying a
requirement already MODIFIED by an active ratified change…"*, twice — in the body
and in its only scenario. The custody change **ADDS** this requirement; canon
does not carry it at all. So the rule is SILENT on this shape rather than
satisfied by it, and `document-lifecycle`'s restatement adds *"two active
RATIFIED writers"*, which this draft packet is not either. The delta is declared
relative to the custody change's outcome because that is the right thing to do
and because the estate has RULED this shape PENDING in running code, not because
a promoted requirement compels it. **The placement stands on the narrowness
argument, which is sound on its own.** The delta carries that requirement's body
in full with two named additions and ALL SIX of its scenarios, five
byte-identical and the sixth replaced — the scenario recording that the shape
cannot express the access identity, which this change makes false. The
dependency runs one way and is stated as a task: this change MUST NOT archive
before the custody change archives, and if the order ever inverted, the block
converts to `ADDED` before archiving rather than promoting a MODIFIED
requirement canon does not hold. **That obligation now carries a mechanical
backstop** — a pre-archive assertion that canon contains the requirement title —
because the checker that would otherwise catch it provably skips this block.

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
- **AND IT PUBLISHES SOMETHING, which an earlier draft's three limits all
  omitted.** Every limit above was an UNDER-claim — revocation is not eviction,
  the check is intra-document, the invariant is checkable not enforced — and none
  of them said what the record now carries. The binding already holds the vault,
  the secret reference and the owner; this block adds the principal that can
  fetch that secret and the system that holds it, in the same object. The
  defensive gain and the exposure are one fact read from two sides: "which grant
  do I revoke" becomes a lookup, and so does "which principal reaches this
  secret". The family this vocabulary is borrowed from already publishes live
  estate principal names in its packaged examples, and at the major the
  declaration becomes required, so the disclosure stops being opt-in. The
  residency model bounds it by keeping instance records in the consuming
  installs; the requirement now STATES it rather than legislating a "both halves"
  disclosure rule that omitted this half, and a packaged fixture uses fixture
  values rather than a live install's identifiers.
- **The two live consumers are named as consumers, not delivered.** The
  xFactory sync lane and openXdox are what this change makes checkable; their
  binding instances remain their own repositories' acts under the residency
  model, exactly as ratified on 2026-08-23. **Whether a packaged fixture may name
  their LIVE fetch identities was parked by a security seat and is now RULED**:
  Brett decided on 2026-08-29 that packaged fixtures use SYNTHETIC identifiers
  and the live ones stay in the consuming installs. P-2 is discharged; the
  conservative answer is the settled one rather than an interim.

## Impact

- **Affected specs.** `credential-contracts` — 1 MODIFIED requirement (the
  custody change's per-system-authority requirement, declared relative to its
  outcome, carriage re-measured after the amendment round: six scenarios in,
  six out, five byte-identical, title byte-identical, zero units lost) and
  3 ADDED requirements (the block; the sharpened refusal; the honest reach).
- **`contracts/` IS touched AT REALIZATION, and a cut IS owed then.** Unlike its
  predecessor, this change's realization moves schema bytes. THIS PACKET MOVES
  NONE: its own diff is the delta and these records, `contracts/` is untouched
  by it, and it cuts nothing — allocation is at realization by merge order.
- **No live secret is created, moved, or read by this change**, and none is by
  its realization either. The block names identifiers; it holds no material.
- **Affected code, at realization**: as enumerated in `code_surface`.
- **Every consumer pinned at the prior bundle stays conformant until it
  upgrades, and this is now a MEASUREMENT rather than a claim.** The block is
  declared and unconstrained, the warnings are warnings, and the compatibility
  direction (`docs/contract-versioning-policy.md:267-272`) forbids a new release
  retroactively invalidating an old pin. Six shapes a domain could already hold
  were built and driven against the prescribed minor schema; all six validate.
- **The bundle figure is re-read at ratification.** `contract-v2.1` is this
  branch's merge-base and `origin/main` has advanced to `contract-v2.2`; the
  drift was measured and does not reach any surface this change claims, but a
  compatibility argument indexed to a bundle is re-cited at the act that adopts
  it.

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
leaving alone the one whose text does not, is the narrower act.

**ITS THIRD GROUND WAS FALSE AND IS REPLACED.** The earlier draft argued at four
sites that the placement "declines to create a third instance of an open defect
class", citing issues #329 and #330. **Both were CLOSED on 2026-08-27** —
`#329` at 21:35:20Z and `#330` at 16:43:36Z, both `COMPLETED` — and the same
README this diff edits already records both closures, so the packet contradicted
its own repository in one file. No seat found it; the convener did. All four
sites are corrected, and the ground is re-derived rather than deleted, because
what replaces it is stronger and was MEASURED:

> **The delta is provably loss-free, and the requirement it declined to touch
> already carries a lossy active writer.** Diffed rather than trusted: six
> scenarios in, six out, five byte-identical, the one changed body paragraph a
> strict prefix of its successor, the title byte-identical. Meanwhile the escrow
> sibling's block on "Canonical credential record shapes" is reported by
> doc-health as not carrying 3 of that requirement's 20 units — so the
> alternative target is the one with a live carriage finding against it. The
> class #329 closed is not open, but the mechanism that closed it — detection
> *"before an archive rather than at one"* — is exactly what makes the ordering
> obligation below worth anchoring in something that runs.

REJECTED ALTERNATIVE: modify both, on the symmetry argument that a block the
schema owns should be registered where the schema's owned shapes are listed. A
seat may reasonably prefer that; the cost is a second live writer on a
requirement that already has one, and a carriage-ledger row in
`tests/doc-health/test_modified_block_currency_self_gate.py` owed in the same
commit. **A council seat ACCEPTED the placement and REFUSED its stated grounds**,
which is the ruling this section now reflects: two of the three original grounds
did not hold, and the placement stands on the third.

**D-2. `requirement_ref` is in the block, it is QUALIFIED, its document
reference carries a grammar, and its id is BOUND TO THE BINDING.** It is the
field that makes the lift safe, and it took three passes to make it actually do
that. THREE REJECTED ALTERNATIVES, each rejected only after execution defeated
it: (a) rely on the convention that the `credential_bindings` map key IS the
requirement id — only a convention, since the schema enforces no key grammar,
and a safety precondition resting on an unenforced convention is not a
precondition; (b) a BARE requirement id, which the packet carried until a bot
round showed one id may match records with different access modes and the lift's
outcome would depend on traversal order; (c) a QUALIFIED reference the author
points wherever they like, which a council seat defeated by execution — the
packaged dispatch-versus-content negative, this capability's only red proof of
serving-tier separation, was **LIFT GRANTED** with its shared secret untouched
and four declarations added, simply by pointing both references at the content
requirement. **The severance from the key removed an unenforced convention and
put nothing in its place.** So the reference now names the binding it sits on
(`requirement_id` == map key) AND the schema constrains the key — enforcing the
convention rather than either trusting it or discarding it. The document
reference gains a repository-relative grammar for the same reason: it is
inherited as an unconstrained string that no code in this repository resolves,
and promoting it to a security precondition without one would rest the
precondition on a second unenforced convention.

**D-3. The lift exists at all.** REJECTED ALTERNATIVE: keep
`shared-secret-identity` absolute, express the two-consumer shape only across
documents, and ship no positive fixture — which is what the custody change did,
under protest, when it DECLINED its packaged example for exactly this reason.
Reasoning for lifting: the custody packet's own task §4.1 hands this decision
forward in terms — *"it must first decide whether `shared-secret-identity`
should distinguish 'two credentials collapsed into one' from 'two consumers of
one credential'"* — and a rule that cannot express a shape the family has
ratified will be worked around rather than obeyed. **A security seat ruled the
lift AS DRAFTED unacceptable and AS AMENDED acceptable**, and the amendments are
carried: the sixth conjunct, the closed access-mode vocabulary, the constrained
resolution target and the every-pair arity. The packet's own fallback stands if
any of them cannot be built: it is buildable without the lift by deleting one
clause.

**D-4. `shared_credential_acknowledged` is a const-true declaration rather than
a boolean.** Following `issuance_preconditions` verbatim: *"a precondition is
DECLARED or NOT DECLARED — `false` is not a second meaning, it is a declaration
that reads as governance while asserting nothing."* REJECTED ALTERNATIVE: a
plain boolean, which admits a record asserting `false` beside a shared secret.
**Unanimous on the bench, and the one decision a security seat said it would not
touch.** The same mechanism now also carries the stub exemption.

**D-5. `holder_ref` reuses identity-brokering's spelling rather than defining a
consumer id of its own, and does NOT require a wallet reference.** The wallet
half is sound and its facts are exact. **The REUSE half was refused as argued** —
its premise, that canon had named this thing once, was false in shipped contract
bytes — and § The rival that already ships is the re-argument: the artifact is
named, the "named it once" claim is corrected, the one-home-or-two question is
RULED (per-binding versus document-level scope), and the second validator is
scoped OUT with the divergence recorded as an owed successor. See design.md
§ The wallet question for the wallet half's full reasoning.

**D-6. The self-test count string is DERIVED, in its own issue rather than
here.** The verbatim assertion is already redundant: the by-name fixture
inventory beside it enumerates every positive and negative and strictly
dominates a count, catching every drop *and* saying which. Deriving it is safe
**provided every fixture this change adds joins that by-name inventory in the
same commit** — deriving without that is the fail-open version and would silently
accept a shrinking corpus of security probes. Three packets have now met this
assertion, which is why it is filed rather than patched in place.

## Open questions — RULED by the council round, no longer open

The bench answered all five and reversed the author on one. Each is recorded
with what moved it.

**OQ-1. Is the omission warning registered as a formal deprecation? RULED YES,
unanimously, and NOT optional.** All four seats agreed and two escalated it: the
versioning policy conditions the entire breaking class on *"at least one full
minor release where the old shape produced deprecation warnings"*, so a
deprecation that was never registered cannot be shown to have been served, and
the major's requiredness becomes unauditable. **The entry names ALL of the acts
that land at the major** — requiredness, closure and the member grammar, with
their codes — because a reader learns from that entry alone that they are one
act. Task 5.1 is therefore UNCONDITIONAL, not "subject to the council's ruling".
A seat also asks that whoever writes it first check whether the three
pre-existing `removal target contract-v2.0` entries are themselves overdue
against the now-current bundle — carried as a condition on trusting the
mechanism, not on this packet.

**OQ-2. Which major requires the block AND closes it? RULED TOGETHER,
unanimously.** There are now THREE breaking halves owed at the major, not two,
so separating them would triple the deprecation bookkeeping and produce
partially-migrated shapes for one field. One seat adds the ordering rule that
matters if they are ever separated anyway: **the CLOSURE lands FIRST**, because
requiredness before closure would make an open-membered block mandatory — every
binding compelled to carry a security-relevant declaration whose member set
nothing constrains, which is the worst of the four orderings.

**OQ-3. Does the hosting record's custody pointer become plural? RULED: leave
singular, route out — AND record it as an owed successor with a named home**,
which the earlier draft did not do (it listed the question only under "NOT part
of this change"). A security seat attaches a caution to carry with it: at
eviction time a singular pointer beside a deliberately multi-consumer record
resolves to one binding, and an operator who follows it evicts one of two
consumers believing they evicted the access — part of the eviction-readability
gain this change sells, undone by the record that consumes it.

**OQ-4. Should `fetch_identity` resolve to a client-identity-roster entry?
RULED NO requirement now, unanimously — with the successor named in RATIFIED
text rather than only in an open question**, because a successor named only in a
proposal's open questions archives with the proposal. Two independent grounds
were added by the bench: the shipped `install_federated_workload_identity` is a
class-level value with no roster entry by construction, which is evidence FOR the
recommendation and is now cited; and adopting a roster obligation would create a
SECOND unresolvable-reference class on top of the one being repaired here.

**OQ-5. Is the degraded fetch-identity mode declarable? RULED OUT — and the
author's stated reason was FALSE and is replaced, and a security seat ruled
AGAINST the recommendation.** The premise *"no machine-readable home"* is false:
`contracts/avatar-client/broker-server-key-binding.template.yaml:115` ships
`degraded_mode_permitted: true` on this very record kind, beside a note citing
the same canon sentence. The recommendation survives on capability-boundary and
test-load grounds, not on absence of prior art, and that prior art is the shape
the successor is measured against rather than a greenfield design. **The
dissent is real and it is answered rather than out-voted**: at the major
`fetch_identity` becomes required, so a degraded-mode install must write
SOMETHING into a required field, and what it will write is the shared service
identity, silently — *"precisely the grammar-passing placeholder"* this packet
itself calls worse than omission, *"arriving through the front door of the very
field this change adds."* **So the major is GATED on it**: the deprecation entry
SHALL state that the requiredness does not land until the degraded mode is
declarable. That is the dissenting seat's own second branch, taken.

## Three rulings the bench routed to the liaison, and how they came back

The council answered what it could and deliberately left three questions to
Brett. All three were ruled on 2026-08-29, in session, and all three are encoded
in this revision rather than noted for later.

**Decision 2 — which route.** The four-seat convergent amendment offered two:
**(i)** phase the block's `required:` list to the major with the closure, or
**(ii)** delete the promise that a pre-existing locally shaped `consumer:` object
stays valid, striking the scenario from every document that repeats it. The bench
was unanimous that one was required and expressed no preference. **RULED: route
(i).** The promise is kept and the narrowing is phased, rather than the promise
being withdrawn to match a narrowing. Route (ii) is preserved in design.md §5 as
a coherent design that was considered and ruled against, so a later reader does
not have to guess whether it was seen.

**P-2 — may the packaged corpus name live identifiers?** Parked by
`lead-security` under its own escalation rule, because it turns on the
repository's audience and on whether those identifiers are already public.
**RULED: SYNTHETIC IDENTIFIERS.** The positive two-consumer fixture MUST NOT name
the live xFactory sync-lane or openXdox fetch identities; they stay in the
consuming installs' own `credentials/` trees, where the residency model already
puts an estate fact and where the readership is the install's rather than every
consumer that pins the contract. A fixture owes the SHAPE, and naming the real
principals would buy illustrative realism with a permanent, digest-pinned
widening of who knows which principal reaches which secret. **P-2 is discharged,
not still parked.**

**P-3 — the estate-level delta-pair gap.** Raised by `lead-architect` under
`cross_cutting_design` and concurred by `lead-quality`; both said this change
must neither close it nor be delayed for it. **RULED: file the successor now** —
openxFactory **[#502](https://github.com/opensoft/openxFactory/issues/502)**,
carrying the three holes with their line citations, the four questions a
successor must settle, and the measured population. **A precision on that
population**, since the packet is obliged to reproduce a figure before repeating
it: the seats cited EIGHT, which is the family docstring's historical seven plus
this block. Measured live, the corpus carries **FOUR** PENDING pairs with zero
markers between them. Four is the live number, eight the cumulative one, and the
fact that nothing tracks the difference is part of what #502 is for. This change
carries only its own local stopgap and does not wait on it.

## The §7.4 council round, and what it changed

**Convened 2026-08-29 on this packet at `e6da07a4`. SPLIT 2–2 on the verdict
word; UNANIMOUS 4/4 that the text as drafted was not ratifiable.** Two seats
returned REFUSE AS DEFINED and two ACCEPT AS AMENDED, and both accepting seats
said in terms that the word was the only thing separating them. Fifteen blocking
amendments across four seats. **Brett ruled on 2026-08-29: ACCEPT ALL BLOCKING
AMENDMENTS; one fix round; the ratification read follows.** This revision is that
round.

**Four seats independently reached ONE amendment** — that the block's
`required:` list was an unphased narrowing at the minor while the closure
correctly deferred to the major, falsifying a scenario that would have promoted
into canon. It was found by building the prescribed schema and driving a record
through it. It had survived two Copilot reviews, three author self-catches, a
Codex P1 round and a full independent seat pass, **because every one of those
read the prescription instead of executing it.** The sentence the bench asked to
be quotable is the right one to end on:

> **A prescribed fix applied without a verifier is an unverified change, whatever
> its provenance.**

Two further facts the round produced, recorded because they bear on how this
packet should be read rather than on its content. The convening's own finding —
that #329 and #330 were closed and the packet said otherwise at four sites — was
found by no seat. And the security seat's exposure finding (LS-F8, now the third
limb of § Honest reach) is precisely the reading the client-security-compliance
seat would have carried had it been seated; that seat was not, on a disputed
convener act, and its absence is recorded as load-bearing rather than harmless.

