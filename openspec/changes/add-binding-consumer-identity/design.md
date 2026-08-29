# Design: add-binding-consumer-identity

Status: draft

The proposal states WHAT and WHY. This records what the repository's own
evidence said when each option was checked against it, including the two places
where the evidence chose the design rather than the author choosing it, and the
one place where it refused a shape that looked obviously right.

Everything below was read at `origin/main` on 2026-08-29 (bundle
`contract-v2.1`). Where a figure is stated it was executed, not remembered, and
the execution is named beside it.

SIX SECTIONS RECORD A CORRECTION RATHER THAN A CHOICE, from two rounds of
adversarial reading, and every one keeps the rejected draft visible beside the
fix — because a design document that shows only the position it ended at hides
the argument that moved it.

From the BOT round on pull request #497 (three P1s): §3's qualified requirement
reference, §5's deferred closure, §5b's template exemption. From the §7.4 COUNCIL
round of 2026-08-29 (fifteen blocking amendments across four seats, ruled by
Brett the same day as ACCEPT ALL): §1's rival-vocabulary correction, §3's
rebuilt lift, §5's UNIFORM phasing, §5b's re-keyed exemption, §6's fourth limit,
and §7's replaced grounds.

**In every one the packet already held the principle and had applied it one level
too shallow** — the shape of finding this estate keeps producing, which this
design named about its own predecessors before the bench found it three more
times in the document that named it. The bench's own sentence for the lesson is
the one worth carrying: **a prescribed fix applied without a verifier is an
unverified change, whatever its provenance.** Four seats found §5's residue by
BUILDING the prescribed schema and driving a record through it; two Copilot
reviews, three author self-catches and a Codex P1 round had all read it
instead.

## 1. The naming question, which the estate had already answered twice

The brief for this change asked what an access identity may reference — a
persona, a broker organization, a vault principal id — and warned against
inventing a second scheme. Checked against the repository, the question is
narrower than it looks, because two of the three candidate names are already
ratified vocabulary in capabilities this change must compose with, and the
third is FORBIDDEN.

**A consuming system is not a persona, and the prohibition is explicit.**
`add-identity-brokering` (ratified 2026-08-21) promotes "Workloads are not
personas":

> openxFactory SHALL keep non-human identity out of the persona population: a
> workload, agent, job, or service SHALL NOT be represented as a persona, and
> its authority SHALL continue to come from `credential-contracts` grants and
> `openxwallet` holders rather than from anything the broker holds.

So `actor-subject-reference` — that family's structured reference for a human
actor, with its `opaque_subject`, its issuer and its three provenance classes —
is the wrong shape for this field by that family's own rule, however tempting
its rigour. Using it would be the second-authority-copy defect that requirement
exists to close, arriving from the credential side.

**The right word is `holder_ref`, and it is already shipped.** The same family's
schemas define a shared `credential_reference` block:

```yaml
credential_reference:
  required: [requirement_id, requirements_document_ref, holder_ref, custody_declared_in]
```

— present in `contracts/identity-brokering/broker-client-declaration.schema.yaml:113-121`,
`broker-organization.schema.yaml:179-187` and `surface-adoption.schema.yaml:271-279`,
registered in `contracts/manifest.yaml` at `contract-v1.37`, and spelled in the
packaged examples as live values: `opsx:service-subject:aks-opensoft-qa`,
`opsx:service-subject:keycloak-opensoft-shared`.

That block points FROM a consuming declaration AT a credential requirement, and
names the holder on the way. What is missing is the return direction: the
BINDING — the record that actually resolves to a secret — says nothing about who
holds it. Adding `holder_ref` to the binding closes the loop with the word the
estate already uses, in the grammar it already uses, rather than with a
`consumer_id` that would mean the same thing under a different name and drift
from it within a release.

**The second word is `fetch_identity`, and `credential-contracts` supplied it
itself.** Two promoted requirements in this very capability name what a lane
receives:

> the consuming lane SHALL be identical in both cases, receiving only bindings:
> an opaque secret reference and a fetch-identity identifier

> A runtime credential an install materializes SHALL be delivered BY REFERENCE —
> a vault URI plus the runtime's own fetch identity

**The shape carries the first and not the second.** `secret_ref` is a required
property; the fetch identity appears nowhere in the SCHEMA. That is not a design
insight this packet contributes — it is canon's own two-item list, checked
against the shape that is supposed to carry it. It is also why the field is not
called `access_identity`, `vault_principal` or `service_principal`: three
plausible names for a thing canon has already named.

**CORRECTION, from a council seat: canon has named it TWICE, and the second
naming is not prose.** The first draft of this section said *"a thing canon has
already named once"*, and a shipped, digest-pinned machine key falsifies that.
`contracts/avatar-client/broker-server-key-binding.template.yaml` declares
`kind: xfactory_credential_binding_template` — the very kind this change extends
— and carries a top-level `resolution:` block with
`fetch_identity: install_federated_workload_identity`, plus a top-level
`requirement_id`, plus nine undeclared top-level keys, all validating against the
pinned schema with ZERO errors. Reproduced by this session before amending.

That is a rival vocabulary in `contracts/`, and D-5's whole content is *"no rival
vocabulary"*, so a one-line disclaimer does not discharge it. Four things are
owed and all four are done. **(i) The artifact is NAMED**, here and in D-5.
**(ii) The "named it once" claim is corrected**, in this paragraph. **(iii) The
one-home-or-two question is RULED**, in the proposal's § The rival that already
ships: the two are not two spellings of one fact but two SCOPES — a document-level
resolution posture for one install, and a per-binding declaration of one
binding's holder — and where both are present the per-binding declaration is the
operative one for that binding. The estate's own doctrine, on the very family
this vocabulary is borrowed from, is *"Composition, not a second custody
vocabulary … so the two cannot disagree"*, and a scope rule is what makes them
unable to. **(iv) The second validator is SCOPED OUT**: two validators read this
one kind with divergent rules, `validate-credential-contracts.py` never seeing
the avatar file at all, and this change adds no obligation to
`validate-avatar-client.py`; the divergence is recorded as an owed successor
rather than widened in silence.

The same artifact also settles two other things the packet had wrong. It is a
FOURTH writer of the binding shape, checked-and-exempt, which §4 of the task list
had not named; and it ships `degraded_mode_permitted: true`, which falsifies
OQ-5's stated premise of *"no machine-readable home"* — see §9.

## 2. The wallet question, answered without creating a rival

`add-wallet-carried-review-authority` (ratified 2026-08-23) expresses review
authority as an `xfactory_wallet_grant` *"whose `audience.wallet_ref` names that
holder's wallet"*. The brief asked directly whether a wallet reference is the
right consumer-identity spelling for governed actors.

**Answer: a wallet reference is a legitimate VALUE of `holder_ref`, and MUST NOT
be its required type.** Three reasons, in descending order of force:

1. **Requiring one would invert a pin direction that was deliberately
   established three weeks ago.** Since `contract-v2.0`
   (`split-openxwallet-repo`, archived 2026-08-28) openxFactory does not OWN the
   openxWallet family — `contracts/openxwallet/` does not exist here. It
   CONSUMES it: `contracts/openxwallet-pin.yaml` pins `opensoft/openXwallet` by
   40-hex commit plus eight per-file `sha256` digests, and
   `docs/contract-versioning-policy.md` § Deprecations Executed records the
   removal. A required field in a core openxFactory schema whose type is owned
   by a pinned downstream product would make every openxFactory cut depend on a
   shape openxFactory no longer publishes. The pin file's own design note
   refuses a weaker version of the same coupling.
2. **Most consumers of a credential binding carry no wallet and need none.** A
   sync lane, a CI job, a serving tier: `identity-brokering` routes exactly
   these to *"`credential-contracts` grants and `openxwallet` holders"* — a
   disjunction, not a requirement of both.
3. **`holder_ref` is a bare identifier, so a wallet-carrying governed actor can
   simply BE named by its wallet's identifier.** Nothing is foreclosed and no
   second vocabulary is created; the two families meet at the word "holder",
   which is what both already say.

REJECTED, and worth naming because it is the attractive wrong turn: a typed
`holder:` block with a `kind: wallet | service_subject | …` discriminator. It
would import the wallet family's shape questions into a schema that does not
need them, and the discriminator would have to be closed — a closed vocabulary
of holder classes is a governance object of its own, with its own growth
procedure, argued in the wrong packet.

## 3. The check design, and the exemption hazard it had to avoid

The custody change handed this decision forward in terms (its tasks §4.1): a
later change *"must first decide whether `shared-secret-identity` should
distinguish 'two credentials collapsed into one' from 'two consumers of one
credential'"*.

**What the check does today, verified by reading it rather than its
description.** `scripts/validate-credential-contracts.py:115-129` walks one
document's `credential_bindings`, keeps a `{secret_ref: first_binding_name}`
map, and raises on the second occurrence. It reads no other field, and its
message names the dispatch/content fault: *"dispatch and content credentials
must be distinct bindings so the serving tier holds no content-write key
material."* The packaged negative `dispatch-reuses-content-secret.yaml` is
exactly that shape — two bindings, one `secret_ref: xfactory-content-app`, same
`owner`.

**The predicate is a PROXY for the rule it enforces, and the two are not the
same statement.** Promoted `credential-contracts` refuses a dispatch binding
that *"names the same App or key identity as a content-write binding"*. The
implementation refuses a duplicate `secret_ref`. That proxy is sound for the
fault it was built for and unsound for the fault this change introduces a
vocabulary for: two consumers of ONE deliberately shared identity are a
duplicate `secret_ref` and are not a collapse of two credentials into one.

**Three candidate designs were considered.**

**(a) Leave the check absolute.** Cost: the shape the family has RATIFIED — two
consuming systems, one operated identity — remains inexpressible in one
document, which is precisely why the custody change had to decline its packaged
fixture and say so in its proposal, its design and its task list. A rule that
cannot express a ratified shape is worked around, not obeyed. This remains a
buildable option (D-3 in the proposal): delete one clause.

**(b) Exempt a declared pair.** REJECTED on a defect this estate has already
paid for once, in a shipped schema, on the identical shape. `contracts/identity-brokering/actor-subject-reference.schema.yaml`
records why its provenance classes had to be made mutually exclusive:

> `broker_asserted` plus a mapping block was the one combination the
> conditionals left representable, and it is the useful one to an attacker: the
> mapping's evidence goes unchecked because no rule governing mappings applies,
> so an unverified resolution travels inside a record that reads as a
> first-party broker assertion.

An exemption keyed on "the author says this pair is fine" is that shape exactly:
a declaration that suppresses a check while satisfying no rule of its own, so an
unverified claim travels inside a record that reads as validated. What that
schema did about it — make the wrong combinations UNREPRESENTABLE by requiring
independent conditions per class — is what (c) does here.

**(c) A lift with independent, fail-closed preconditions — CHOSEN, and then
DEFEATED BY EXECUTION AND REBUILT.** The refusal is the default and stays the
default. The first cut lifted on five conditions:

| # | Condition | What it stops |
| --- | --- | --- |
| 1 | both bindings declare `consumer:` | silence buying an exemption |
| 2 | `holder_ref`s differ | one system wearing two hats |
| 3 | `fetch_identity`s differ | two systems on one authority — the custody invariant itself |
| 4 | both declare `shared_credential_acknowledged: true` | a one-sided declaration exempting a pair |
| 5 | both name a QUALIFIED `requirement_ref` resolving in-repository to EXACTLY ONE requirement, with equal `access_mode`, not `dispatch_only` | the dispatch/content collapse laundering itself as intentional sharing |

**A security seat drove that lift and it failed three ways on the one fixture it
exists to protect.** The subject was
`examples/credential-contracts/negative/dispatch-reuses-content-secret.yaml` —
this capability's ONLY red proof of serving-tier separation — byte-unchanged in
its secret sharing, with four declarations added:

```
L1  HONEST refs: the two requirements the map keys name   -> refusal stands   (modes differ)
L2  BOTH refs point at the CONTENT requirement            -> LIFT GRANTED
L3  both refs point at a doc carrying NO access_mode      -> LIFT GRANTED     (None == None)
L4  both refs point at 'Dispatch_Only'                    -> LIFT GRANTED     (spelling variant)
```

**L2 is the one that matters.** Condition 5 severed the lift from the map key —
correctly, because the key was an unenforced convention — and put NOTHING in its
place. The author chooses where the reference points, so the condition is
satisfied by the author's own word about which requirement this binding serves.
That is candidate (b) again at one remove: the declaration now has five parts
instead of one, and the fifth is still an unverified assertion. **A precondition
an author can satisfy by choosing where to point is not a precondition** — the
same sentence this design already uses against the map key, arriving at its own
replacement.

**A fourth defeat came from arity.** The inherited predicate keeps the FIRST
binding seen per `secret_ref` and compares later ones against it, so with three
bindings the pair (b,c) is never examined — and a record where b and c share a
fetch identity lifts on both examined pairs and ships the exact fault
`shared-authority-identity` exists to name.

**So the lift now has SIX conditions, an every-pair arity, and a closed
discriminator:**

- **Condition 6 — the reference names its own binding.** `requirement_id` MUST
  equal the `credential_bindings` map key, **and the schema constrains the key**
  to the identifier grammar so the key stops being a convention. That is the
  repair the rejection of candidate (a) implied but did not perform: the answer
  to an unenforced convention is to enforce it, not to discard it and trust
  something weaker. L2 is refused by condition 6.
- **`access_mode` is closed to a declared vocabulary, and unreadable means
  UNAVAILABLE.** Today it is `{type: string}` with no `enum`, read by one line
  comparing to one exact spelling — so two absent modes compare equal (L3) and a
  variant spelling compares equal to itself (L4). Both now make the lift
  unavailable. This is the `release_inventory.py` fail-open rule this design
  already cites, applied to the field the lift turns on rather than only to the
  reference that reaches it.
- **The resolution target is constrained.** References resolve ONLY against
  requirement records the validator itself discovered and schema-checked in the
  scanned tree; the document reference is repository-relative, non-escaping and
  non-foreign by grammar; **the validator never opens a path taken from a
  record.** Verified by construction: `../x.yaml`, `/etc/x.yaml` and
  `OpsxFactory:credentials/r.yaml` are all refused by the pattern.
- **The arity is every pair**, and the inherited first-against-rest shape is
  REPLACED rather than extended.

Every one FAILS CLOSED, and the list is the whole set rather than a sample: an
absent block, a shared `holder_ref`, a shared `fetch_identity`, a one-sided or
missing acknowledgment, a reference resolving to zero or to more than one record,
a reference whose id does not equal its binding's key, an ungrammatical or
escaping document reference, and an access mode that is absent, unrecognised,
mixed or dispatch-only each leave the original refusal standing. That direction
is the estate's own lesson, with running code to cite:
`scripts/doc_health/release_inventory.py:235-248` records a fail-open the
release-inventory-drift family shipped with and a bot round caught — two
comparisons written as `if recorded.get(field) and …`, so *"an entry missing its
`digest` skipped the byte check entirely … That is fail-open: the one failure
mode a drift check must not have, arriving through a field nobody thought could
be absent (PR #324, Codex)."* The repair is the rule this change adopts: an entry
that cannot answer the question is not a matching entry.

**The access-mode exclusion OVER-REFUSES ON PURPOSE, and the over-refusal is
named rather than left to be discovered.** It excludes `dispatch_only` on BOTH
sides, so two consumers of ONE dispatch-only credential cannot be lifted either —
a shape nothing in canon actually forbids. The choice is deliberate: the dispatch
class is where the serving-tier separation rule lives, the population of real
two-consumer dispatch cases is currently zero, and a rule that refuses a shape
nobody needs is cheaper to relax later than a rule that permits one nobody
checked.

**The promoted dispatch requirement is NOT modified, and that was checked rather
than skipped — but the reason had to be repaired first.** "Dispatch-only
credential least privilege and serving-tier separation" carries the scenario
*"WHEN a dispatch binding names the same App or key identity as a content-write
binding, THEN it MUST be rejected"* — unconditional in canon, no lift, no
acknowledgment. The first draft said condition 5 kept that scenario true; L2
falsified that by execution. **Condition 6 is what actually keeps it true**, and
a security seat's adjacent ruling is taken with it: because a promoted
unconditional refusal now has a conditional exemption declared in a neighbouring
requirement, the reader of canon must be able to see that. The exemption's
conditions are stated in the ADDED requirement in full, and the packaged negative
is asserted to STAY refused however many declarations are added to it — the
assertion the earlier task list made and could not have kept.

**`shared-authority-identity` is a new code and not a new message on an old
one.** Condition 3's failure is already refused by the default rule, so the code
adds no refusal — it adds a refusal that NAMES THE FAULT. A record with two
bindings, one secret and one fetch identity is not "two credentials collapsed";
it is the exact violation of "one identity MAY be shared; one AUTHORITY SHALL
NOT", and a reader who is told about secret reuse will fix the wrong thing. **And
its scope is no longer the `secret_ref` proxy.** Two different holders declaring
one fetch identity is the collapse whatever their `secret_ref`s; scoping the
finding to a shared reference leaves the same fault unreported when two spellings
name one secret. The subtraction that matters was performed before widening it:
one holder legitimately reuses its fetch identity across its own bindings, so the
check keys on DIFFERENT holders sharing ONE fetch identity, never on the fetch
identity alone.

## 4. The const-true declaration, following a precedent in the same file

`shared_credential_acknowledged` takes `const: true` and never `false`, on the
reasoning `issuance_preconditions` states in this very schema
(`contracts/schemas/xfactory-credential-contracts.schema.yaml:57-68`):

> Every value is `const: true` because a precondition is DECLARED or NOT
> DECLARED — `false` is not a second meaning, it is a declaration that reads as
> governance while asserting nothing.

A `shared_credential_acknowledged: false` beside a shared secret would be the
same false comfort, and the family has a registered negative fixture for that
exact shape one record kind over
(`examples/credential-contracts/negative/issuance-precondition-valued-false.yaml`).

## 5. The block is DECLARED at the minor and CONSTRAINED at the major — all of it

> **RULED BY BRETT HEAP, 2026-08-29 (in session): Decision 2, ROUTE (i).** The
> council put two routes and left the choice to `lead-architect`: **(i) PHASE
> IT** — the block's `required:` list moves to the major with the closure — or
> **(ii) DELETE THE PROMISE** — declare that a pre-existing locally shaped
> `consumer:` object is a shape the estate declines to protect, and strike the
> scenario that says otherwise from `spec.md`, `proposal.md`, `design.md` and the
> README. The bench was unanimous that one of the two was required before
> ratification and expressed no preference between them. **Brett confirmed route
> (i)**, which is what this section builds: the promise is kept and the
> narrowing is phased, rather than the promise being withdrawn to match a
> narrowing.
>
> The ruling is recorded here because it is an `architecture_direction` decision
> the council explicitly routed to a decision-maker, not an authoring choice —
> and because route (ii) remains a coherent design that a later reader might
> otherwise assume was never considered. It was; it was ruled against. The
> convening record cross-reference is in `.openspec.yaml`'s `council_review`
> block under `rulings`.

`additionalProperties: false` goes on the block, is NOT proposed for the binding
object around it, and does not land at the same release as the block. Nor does
`required:`. Nor does the identifier `pattern`. **All three are the breaking
class and all three wait for the major**, and getting there took two corrections
that are both kept visible below, because this is the section whose incomplete
first two drafts a bench of four then found in a third place.

**The hole is measured.** Executed against
`contracts/schemas/xfactory-credential-contracts.schema.yaml`: a binding carrying
`consumer: {holder_ref: …, fetch_identity: …, totally: unchecked}` validates with
ZERO errors, because the binding object declares properties without closing them.
The field this change adds already exists as an unenforceable free-text hole.

**CORRECTION ONE, from a bot round.** The first draft said: declare the block and
close it, in one additive minor. But the measurement's own premise defeats that.
If the key is writable today, a domain may ALREADY hold a locally shaped
`consumer:` object that the current major accepts, and closing the block in a
minor refuses it — a NARROWING wearing an additive label, and what
§ Compatibility Direction forbids outright. The packet had the argument in hand
and stopped one level out: it already said closing the BINDING OBJECT would be
breaking *"because it removes a shape (arbitrary extra keys) that pinned
consumers may be relying on"*. So `additionalProperties: false` moved to the
major.

**CORRECTION TWO, from four council seats at once, and it is the decisive one.**
The same argument condemns two further acts that the corrected draft still landed
in the minor. `required: [holder_ref, fetch_identity]` removes shapes the object
could previously take — over a strictly LARGER set than the closure, because it
also refuses `consumer: {holder_ref: x}`, which the closure would have accepted.
And the identifier `pattern` removes every value that does not match it,
including the generator's own placeholder style. Built and driven against the
prescribed minor schema:

| shape a domain could already hold | today | as first prescribed | as corrected |
| --- | --- | --- | --- |
| object with neither declared member | VALID | **REFUSED** | VALID |
| a scalar `consumer:` value | VALID | **REFUSED** | VALID |
| a list `consumer:` value | VALID | **REFUSED** | VALID |
| declared members, placeholder values | VALID | **REFUSED** | VALID |
| declared members + an undeclared extra | VALID | VALID | VALID |
| no block at all | VALID | VALID | VALID |

**And the first prescription falsified a scenario that would have promoted into
canon** — `spec.md`'s own *"it stays VALID across this addition and is warned
rather than refused"*. A ratifiable promise contradicted by its own build
instruction is the silent-loss shape this estate has paid for before.

**THE LESSON, THIRD TIME IN ONE PACKET.** `design.md`'s own diagnosis of the
drafts it replaced — *"a settled fact was chased to the enclosing object and
stopped there"* — describes correction one's own residue exactly. The analysis
was chased from the binding object down to the block and stopped there; it did
not reach the members WITHIN the block. Four seats reached it independently, and
none of them reached it by reading: **every one built the schema and drove a
record through it.** Two Copilot reviews, three author self-catches and a Codex
P1 round had all read the prescription instead of executing it.

**So the phasing is now uniform and the rule is one sentence:** at the
introducing minor the schema constrains NOTHING about `consumer:` — it declares
the property, describes its members, and stops. Every constraint arrives together
at the major, behind one deprecation window and EIGHT warning codes — one per
shape the major refuses, derived from that list rather than counted. That also
dissolves the layer problem §5b had, because at the minor every consumer check
lives in the validator, which is the layer the stub exemption can reach.

**CORRECTION THREE, from a bot round on the fix round itself, and it is the
reason this section now says "wherever it sits" rather than "about the block".**
Two narrowings escaped the uniform rule because they were written down somewhere
other than the block. `consumer: {}` — a block that exists and declares neither
identifier — matched NONE of the three warning codes then defined, so it would have crossed
the whole minor in silence and been refused at the major, leaving the
requiredness change without the warning release the policy requires. And the
`credential_bindings` MAP-KEY grammar was prescribed with no phasing at all while
its two immediate neighbours in the same task list, the `access_mode` vocabulary
and the `requirements_document_ref` grammar, both had it. Measured: of five
plausible existing keys, four are VALID today and REFUSED by the grammar.

**That is the fourth and fifth instance of one defect, and the last two arrived
inside the repair for the first three.** The generalisation the section had been
missing, now written where it cannot be missed: *every* act that refuses a value
the current major accepts phases, whether it sits on the block, on the map, or on
a neighbouring record — and the warning set is ENUMERATED against the refusals it
must cover, never summarised. Nothing about this was hard to see once someone
enumerated what an empty block matches; nobody had.

**Still NOT the binding object.** That closure is a further breaking act with a
much wider blast radius, and it stays a named successor.

## 5b. Templates are not instances — and the exemption must be a TOKEN, not a name

A bot round hit the sweep's own remedy: task §4.1 asked the domain-starter
generator to emit the `consumer:` block, on the reasoning that a field its own
scaffolder does not emit is a field every new domain starts out of conformance
with. That reasoning is sound about INSTANCES and wrong about this artifact — the
generator emits a TEMPLATE, written before any install, vault or fetch identity
exists. Its placeholder style FAILS the identifier grammar, and the obvious
repair, a grammar-passing sentinel, is worse: it suppresses the warning and reads
as the record fact the change exists to establish while naming nothing.

**Two council seats then showed the adopted remedy could not work, on two
independent grounds, and both are taken.**

**(i) A filename is not a declaration.** The exemption was keyed on
`*.template.yaml` / `*.example.yaml` — a property of the PATH, chosen by the
author, invisible in the record's bytes. The generator emits exactly
`credentials/bindings.template.yaml` into every scaffolded repo; an install that
fills it in and does not rename it is permanently exempt from the omission
warning and, at the major, from the requirement itself. A real binding record
named `prod.template.yaml` escapes a required field by what it is called. That is
the "declared exemption" shape §3 rejects, degraded — *a declaration is at least
visible as a declaration.* **The packet already held the right mechanism** and
used it one field over: the declared-or-absent const-true token. So the exemption
is `instantiation_stub: true`, and a record carrying live values must not declare
it.

**(ii) The exemption sat in the wrong LAYER, and the token is what moves it.**
This is the sharper of the two. `spec.md` exempted a stub from *"the omission
warning"* and *"the major's refusal"* — both validator behaviours — while the
placeholder's failure was a **jsonschema error against the pinned contract**. A
pinned schema cannot carry a filename-conditional branch, because cross-repository
consumers validate against it by digest. So the exemption could never reach the
case it was adopted for, and the acceptance test *"a freshly scaffolded repo
validates clean"* **could not have passed as drafted** — proven by running the
real validator over the generator's own emitted bytes.

The token fixes the layer as well as the key: a schema CAN condition on a
property, so `if: not required(instantiation_stub) then: required(holder_ref,
fetch_identity)` is expressible at the major and was verified by construction.
And at the minor the question does not arise, because §5's correction leaves the
schema constraining nothing.

**The generator emits `consumer: {instantiation_stub: true}` — the token alone.**
That is the third draft of this instruction, and the second was wrong in a way
worth keeping visible. Draft two said *emit no block at all, a named comment
instead*, on the principle that *scaffolding which manufactures conformance is
worse than scaffolding that omits it.* The principle is right; the application
was not. A bot round showed that a blockless template **cannot stay clean at the
major either**: a missing block is an ERROR there, the stub token is the ONLY
exemption, and the generator was emitting neither — so the
scaffolded-repo-validates-clean assertion would have become impossible the moment
requiredness activated, which is the same class of defect as the placeholder it
replaced, one release later.

**The token is the resolution, and it is not a third sentinel.** A placeholder
`holder_ref` asserts an identity that does not exist; `instantiation_stub: true`
asserts only that the record is a stub, **which is true of a file written before
any install exists.** Verified by construction: the token alone validates at the
minor and at the major, while a blockless template validates at the major's
schema and is refused by its validator. So the rule generalises past this
packet: *scaffolding that manufactures conformance is worse than scaffolding that
omits it — and scaffolding that DECLARES ITS OWN STATUS is better than either.*

## 6. What this makes provable — and the reach it does not have

FOUR limits — three under-claims and one DISCLOSURE — recorded here rather than
left to be discovered. The first three were in the earlier draft; the fourth was
not, and a security seat's finding is that its absence was itself the defect,
because a requirement that legislates a "both halves" disclosure rule for
adopting documents and then defines the halves as two under-claims is a
requirement with a hole in it.

**(i) Revocation of ACCESS becomes readable and actionable. Eviction does not.**
With `fetch_identity` on the record, "revoke this consumer" resolves to a
specific grant at the store and its effect is bounded and attributable. But the
credential is a shared BEARER secret: revoking a fetch identity stops future
fetches and nothing else — it cannot un-disclose a password already read or end
a session already established with it. Evicting a consumer that HOLDS the secret
still requires ROTATION, and rotation still reaches every consumer of that
identity. The custody requirement says this; this change changes none of it and
restates it so a new field cannot read as new containment.

**(ii) The check is intra-document. The estate is not.**
`scripts/validate-credential-contracts.py` takes a `<domain-repo-path>` and
scans that repository's `credentials/` tree; its cross-binding comparison is
within one document. The live two-consumer case is not in one document or even
one repository: the xFactory sync-lane binding belongs in the install's
`credentials/` tree and openXdox declares its own in its own repository, under
the residency model ratified on 2026-08-23. **No per-repository validator can
compare them.** What this change delivers there is READABILITY at every site —
each binding states who holds it and what it fetches with, wherever it lives —
and an estate-level sweep that reconciles bindings across repositories is named
as an owed successor. That is the same admission, in the same form, that the
custody change made about this change.

**(iii) The invariant becomes checkable, not enforced.** A record that declares
a fetch identity has not proved that the store's grant matches it. Reconciling a
declaration against the provider's actual grants is a live-estate act with its
own family (`client-identity-roster`'s drift finding is the model), and it is
out of scope here. The claim this packet makes is bounded and exact: the
authority moves from held-by-review to stated-in-the-record.

**(iv) AND THE RECORD NOW PUBLISHES WHICH PRINCIPAL REACHES WHICH SECRET.** The
three limits above are all under-claims; none of them says what the declaration
ADDS to the record's information surface. The binding already carries `vault`,
`secret_ref` and `owner`. This block adds the principal that can fetch that
secret and the system that holds it, in the same object. The defensive gain is
stated exactly right elsewhere — *"which grant to revoke … is a lookup rather
than an inference"* — and the symmetry is exact: for anyone who can read the
record, "which principal do I take over to reach this secret" becomes a lookup
too. This is not speculative. The family this vocabulary is borrowed from already
ships live estate principal names in its packaged examples
(`opsx:service-subject:keycloak-opensoft-shared`,
`opsx:service-subject:aks-opensoft-qa`). Two aggravations were named with it: a
proposed positive fixture would have put the LIVE xFactory sync-lane and openXdox
fetch identities into the digest-pinned, distributed corpus, and at the major the
declaration becomes REQUIRED so the disclosure stops being opt-in.

**The finding is not "do not do this."** The declaration is worth having, and the
residency model bounds it by keeping instance records in the consuming installs.
The repair is that the requirement STATES it — as a third half of the disclosure
obligation, with its own scenario — and that packaged fixtures use fixture values
rather than live identifiers. **RULED BY BRETT HEAP, 2026-08-29: the packaged fixtures use SYNTHETIC
IDENTIFIERS.** A security seat parked this question under its own escalation
rule (P-2, LS-C1) rather than resolving it — it turns on the repository's
audience and on whether those identifiers are already public — and the liaison
has now ruled it. **The positive two-consumer fixture MUST NOT name the live
xFactory sync-lane or openXdox fetch identities.** Those stay where the residency
model already puts them: in the consuming installs' own `credentials/` trees,
which is where a live estate fact belongs and where its readership is the
install's rather than every consumer that pins the contract. The fixture
demonstrates the SHAPE, which is all a fixture owes; naming the real principals
would buy illustrative realism with a permanent, digest-pinned widening of who
knows which principal reaches which secret. **P-2 is discharged, not still
parked**, and the packaged corpus is synthetic by rule rather than by
convention.

**A note on who found this, because it bears on the record.** This is precisely
the client-security-compliance reading, and that seat was NOT seated at the
convening on a disputed convener act; a domain seat carried the question and
produced the finding. Its provenance is recorded rather than smoothed over: the
mitigation worked, and it is not the same thing as the seat having been present.

## 7. Delta placement, and the two active writers on this capability

Two active changes already write `credential-contracts` deltas, and this change
touches one of them deliberately and the other not at all.

**`add-credential-escrow-checkout` (ratified 2026-08-28) MODIFIES "Canonical
credential record shapes"** because a sixth record kind falsifies three of that
requirement's sentences the moment it exists — its body's enumeration and two
scenario bullets that say "the five kinds". Its `escrow:` block is registered
there in the same breath. That is a FORCED modification, and it is registered in
the doc-health carriage ledger
(`tests/doc-health/test_modified_block_currency_self_gate.py`) as the audit
trail for it.

**This change adds no record kind, so no sentence of that requirement becomes
false, and it does not modify it.** The substance is carried by ADDED
requirements — which is exactly how the escrow packet carries ITS substance too
("The escrow relationship rides the credential binding, never a custody tier"
is an ADDED requirement declaring a block on the binding template). Declining
the second modification was also argued as declining a third instance of an OPEN
defect class — **and that ground was false: #329 and #330 both closed on
2026-08-27, which the same README this diff edits already records.** It is
replaced by a measured one: this delta is provably loss-free, while the escrow
sibling's block on the alternative target is currently REPORTED lossy on this
very branch, missing 3 of that requirement's 20 units. The proposal records this
as D-1 with the rejected alternative, so a seat can rule the other way; the cost
of ruling that way is a second live writer plus a ledger row in the same commit.
A council seat ACCEPTED the placement and REFUSED its stated grounds, which is
what this section now reflects.

**The requirement this change DOES modify is the custody change's**, and that
placement is chosen because it is the text this change makes stale. Its scenario
"The published binding shape cannot yet express the access identity" is FALSE
once the shape expresses it, and leaving a false scenario to promote into canon
would be worse than any ordering cost. Three facts make the placement safe
rather than merely defensible:

1. **`release-realization` does NOT govern it, and the earlier draft said it
   did.** Read in its own text, the rule's antecedent is a requirement *"already
   MODIFIED by an active ratified change"* — twice, in the body and in its only
   scenario — and the custody change **ADDS** this requirement; canon carries it
   nowhere. `document-lifecycle`'s restatement adds *"two active RATIFIED
   writers"*, and this packet is `draft`. So the rule is SILENT on this shape
   rather than satisfied by it, and citing it as settled authority would leave a
   later reader with a citation that does not carry. **The honest statement:** no
   promoted requirement governs MODIFIED-over-a-sibling's-ADDED; the estate has
   RULED the shape PENDING in running code
   (`modified_block_currency.py:1149-1155`); the proposal declares its delta
   relative to the custody change's outcome because that is the right thing to
   do; and the placement stands on the NARROWNESS argument, which is sound on its
   own and is the ground of record.
2. **The doc-health family already anticipates this shape and reports
   nothing.** `scripts/doc_health/modified_block_currency.py:1176-1201`
   (`resolve`) returns PENDING for a MODIFIED block whose title an active
   sibling ADDS, and `:1149-1155` records the ruling and the population:
   *"pending means there is nothing to compare: the promoted requirement does
   not exist yet, so no basis is synthesized from the sibling's ADDED text.
   RULED 2026-08-27 — the earlier reading, which built a basis from the
   addition, would have measured all seven of this corpus's
   MODIFIED-over-a-sibling's-ADDED pairs against text no promoted requirement
   carries."* Measured on this branch rather than inferred: the family reports
   8 info findings, exactly the 8 the self-gate names, and none of them is this
   change's block. `_arm_ordering` is silent for a second reason too — it scopes
   to active RATIFIED writers, and this packet is `draft`.
   **BUT THAT SILENCE IS NOT EVIDENCE OF SAFETY, and offering it as one was the
   error the earlier draft made.** The block is dropped at
   `modified_block_currency.py:1374-1375`'s `if status == "pending": continue`
   BEFORE any arm runs; the family's own docstring says *"there is nothing to
   compare"*. **The family DECLINES TO MEASURE this shape, so its silence neither
   supports nor opposes the placement** — and this estate has the doctrine in
   running code, in the very repository that convened the review:
   *"Unevaluable NEVER means absent … It must never be read as 'the condition
   does not hold'."* The actual evidence for losslessness is the DIFF, re-run
   after this amendment round: six scenarios in, six out, five byte-identical,
   the one changed body paragraph a strict prefix of its successor, the title
   byte-identical, zero units lost.
3. **The ordering is determinate in practice and stated as an obligation
   anyway.** The custody change carries `target_release: none` and its
   realization tasks §1–§3 are complete, so it archives on evidence that already
   exists; this change carries a contract cut and archives much later. The task
   list nonetheless states the inverse case and its remedy — convert the block
   to `ADDED` before archiving — because "the natural order will hold" is not a
   guarantee and the failure mode is a MODIFIED requirement promoting against
   canon that does not carry it. **AND THE OBLIGATION NOW HAS A BACKSTOP THAT
   RUNS**, because a prose task in a class the checker provably cannot see is not
   a control. Measured: the group for this block has size ONE and always will —
   `_arm_ordering` needs two RATIFIED *MODIFIED* blocks and the custody change's
   block is ADDED, so it is structurally ineligible for the group. In the SAFE
   order the requirement enters canon, `resolve` returns `canon`, and the
   carriage arms run; in the UNSAFE order nothing checks anything. **The one case
   the obligation exists to guard is the one case with no guard**, so the archive
   checklist gains a mechanical assertion that
   `openspec/specs/credential-contracts/spec.md` contains the requirement title
   before this change archives — a one-line check that fails loudly in exactly
   the inverted order.

4. **And the estate-level gap under all of this is FILED, as the estate's and
   not this packet's — issue #502.** MODIFIED-over-a-sibling's-ADDED is governed
   by no promoted requirement, evaluated by no arm, and declared by no marker.
   Two seats raised it as owed a home of its own (LA-C2, LQ-C5) and both said
   this change must neither close it nor be delayed for it. **Brett ruled on
   2026-08-29 that the successor be filed now**, and it is: openxFactory
   **#502**, carrying the three holes with their line citations, the four
   settlement questions a successor must answer, and the measured population.
   **On that population, a precision the seats' figure needs:** they cited
   EIGHT, which is the family docstring's historical seven (counted at the
   2026-08-27 ruling) plus this packet's own block. Measured live on
   `origin/main` `3b342561` with the family's own `resolve`, the corpus carries
   **FOUR** PENDING pairs, zero markers between them — this change,
   `add-wallet-carried-review-authority`, `implement-keycloak-install-repo` and
   `implement-openxpki-install-repo`. Four is the live number; eight is the
   cumulative one. That the two differ, and that nothing tracks the turnover, is
   itself part of what #502 exists for.

## 8. The contracts-and-release decision

**`contracts/` IS touched and a cut IS owed** — the first difference of
substance between this change and its predecessor, which moved no contract bytes
and cut nothing. The ownership test that kept the custody obligations out of
`contracts/` points the other way here: a schema shape that cross-repository
consumers pin by digest is exactly `contracts/` territory, and the custody
packet said so when it named this successor as the one that *"DOES carry the
contract-release ritual"*.

**The number is not spent here, and the reason is concrete rather than
procedural.** `add-credential-escrow-checkout` is ratified and owes an additive
minor on THIS SAME FILE; writing a number in this proposal would spend one
another packet is already spending, which is the `contract-v1.28` renumber
sweep's standing lesson. Allocation happens at realization by merge order.

**One realization consequence is named now because it is a same-commit
obligation, not a follow-up.** `tests/credential_contracts/test_dispatch_credential_contract.py:35`
asserts the validator's self-test line verbatim — `"self-test: 3 positive + 5
negative example(s) confirmed"` — and the packaged corpus currently holds
exactly 3 positives and 5 negatives. Any fixture this change adds moves that
string in the same commit or the suite fails. **ATTRIBUTION CORRECTED:** the
packet that recorded the identical hazard about this identical assertion is
`add-notebook-hosting-credential-custody`, NOT the escrow packet — escrow
contains zero occurrences of "self-test", "3 positive" or
`test_dispatch_credential_contract` across all four of its files. The
substantive claim survives (two packets HAD tripped over the string; with this
one, three), and the seat ruled: **DERIVE the count.** The evidence is stronger
than "two packets tripped" — the verbatim assertion is already REDUNDANT, because
`test_the_example_files_are_present` at `:38-51` enumerates all three positives
and all five negatives BY NAME, which strictly dominates a count: it catches
every drop AND says which. Deriving is safe on ONE condition, and the condition
is the actual control: **every fixture this change adds joins that by-name
inventory in the same commit.** Deriving without that is the fail-open version
and would silently accept a shrinking corpus of security probes. The derivation
is filed as its own `credential-contracts` test-hygiene issue rather than folded
in here.

**And one that is genuinely missing rather than merely owed.**
`scripts/validate-credential-contracts.py` has NO warning channel. It prints
`ERROR` lines, counts them, and exits non-zero; `skip … with notice` is the only
non-error output it can produce, and it is not a finding. ELEVEN sibling
validators in `scripts/` have one, including
`scripts/validate-client-identity-roster.py` — the other validator that reads
records this same schema owns. So the deprecation posture this change adopts — warn
now, error at the next major, which is the policy's stated precondition for ever
making the field required — is not merely unimplemented in this validator, it is
currently INEXPRESSIBLE there. Building the channel is part of the realization
surface and is listed as such.

## 9. What this change is not

- **Not a live binding instance.** The residency model holds unchanged;
  `contracts/manifest.yaml` still records that "openxFactory ships no instance
  records". The xFactory sync-lane binding and the openXdox binding are named
  as the consumers this change makes checkable, and remain their own
  repositories' acts.
- **Not a cross-repository reconciliation.** Named as a successor in §6(ii).
- **Not a change to the hosting record.** Its singular `custody.binding_id` is
  raised as OQ-3 and left to its owning capability.
- **Not a closure of the binding object.** Named as a successor in §5.
- **Not a constraint of any kind on the `consumer:` block at this release.**
  Declared here; requiredness, closure AND the member grammar all execute at the
  major, in one window — §5.
- **Not a reconciliation of the two validators that read this record kind.**
  `validate-avatar-client.py` is the avatar family's surface and is scoped OUT;
  the divergence is an owed successor — §1.
- **Not a home for the MODIFIED-over-a-sibling's-ADDED gap — FILED as issue
  #502** on Brett's ruling of 2026-08-29. Four live PENDING pairs measured, no
  governing requirement, no evaluating arm, no marker; two seats said this change
  must neither close it nor be delayed for it, and it does neither — §7.
- **Not the self-test count derivation.** Ruled DERIVE, filed as its own issue —
  §8.
- **Not a second identity vocabulary.** Both identifiers are words this estate
  ratified before this packet existed.
- **Not a live secret act.** Nothing here creates, moves, or reads credential
  material; the block holds identifiers only.
