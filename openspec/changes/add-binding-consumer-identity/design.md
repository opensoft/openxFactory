# Design: add-binding-consumer-identity

Status: draft

The proposal states WHAT and WHY. This records what the repository's own
evidence said when each option was checked against it, including the two places
where the evidence chose the design rather than the author choosing it, and the
one place where it refused a shape that looked obviously right.

Everything below was read at `origin/main` on 2026-08-29 (bundle
`contract-v2.1`). Where a figure is stated it was executed, not remembered, and
the execution is named beside it.

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
property; the fetch identity appears nowhere in the schema. That is not a design
insight this packet contributes — it is canon's own two-item list, checked
against the shape that is supposed to carry it. It is also why the field is not
called `access_identity`, `vault_principal` or `service_principal`: three
plausible names for a thing canon has already named once.

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

**(c) A lift with independent, fail-closed preconditions — CHOSEN.** The
refusal is the default and stays the default. It lifts only when FIVE
conditions hold at once, each of which an adversary must satisfy separately:

| # | Condition | What it stops |
| --- | --- | --- |
| 1 | both bindings declare `consumer:` | silence buying an exemption |
| 2 | `holder_ref`s differ | one system wearing two hats |
| 3 | `fetch_identity`s differ | two systems on one authority — the custody invariant itself |
| 4 | both declare `shared_credential_acknowledged: true` | a one-sided declaration exempting a pair |
| 5 | both name a `requirement_ref` resolving in-repository to requirements with equal `access_mode`, not `dispatch_only` | the dispatch/content collapse laundering itself as intentional sharing |

Every one FAILS CLOSED, and the list is the whole five rather than a sample: an
absent block, a shared `holder_ref`, a shared `fetch_identity`, a one-sided or
missing acknowledgment, an unresolvable requirement reference and a mixed or
dispatch-only access mode each leave the original refusal standing. That direction is deliberate and it is the estate's own lesson, with
running code to cite. `scripts/doc_health/release_inventory.py:235-248` records
a fail-open the release-inventory-drift family shipped with and a bot round
caught: two comparisons written as `if recorded.get(field) and …`, so *"an
entry missing its `digest` skipped the byte check entirely — and if the mode
still matched, the family reported the member CLEAN while its bytes had
drifted. That is fail-open: the one failure mode a drift check must not have,
arriving through a field nobody thought could be absent (PR #324, Codex)."* The
repair is the rule this change adopts: an entry that cannot answer the question
is not a matching entry. Condition 5 is where that discipline earns its
keep: an unreadable requirement reference makes the lift UNAVAILABLE rather than
UNCHECKED.

**Condition 5 OVER-REFUSES ON PURPOSE, and the over-refusal is named rather than
left to be discovered.** It excludes `dispatch_only` on BOTH sides, so two
consumers of ONE dispatch-only credential cannot be lifted either — a shape
nothing in canon actually forbids. The choice is deliberate: the dispatch class
is where the serving-tier separation rule lives, the population of real
two-consumer dispatch cases is currently zero, and a rule that refuses a shape
nobody needs is cheaper to relax later than a rule that permits one nobody
checked. If such a case appears, relaxing this half is a successor with its own
evidence; a seat that thinks the exclusion should be narrower now should say so.

**Condition 5 is why `requirement_ref` exists at all**, and the alternative was
checked before it was rejected. The `credential_bindings` map key is the
requirement id BY CONVENTION — the packaged example's keys `intent_dispatch` and
`corpus_content_write` are exactly the requirement ids in its sibling
requirements example — but the schema declares `additionalProperties` with no
key grammar and no validator reads the key as an id. A safety precondition
resting on a convention nothing enforces is not a precondition, so the reference
is explicit. It is optional on the block, required only for the lift, and the
ordinary single-consumer binding pays nothing for it.

**The promoted dispatch requirement is NOT modified, and that was checked rather
than skipped.** "Dispatch-only credential least privilege and serving-tier
separation" carries the scenario *"WHEN a dispatch binding names the same App or
key identity as a content-write binding, THEN it MUST be rejected"*. Condition 5
exists so that scenario stays TRUE after the lift: the collapse is refused
however it is declared, and ADDED requirement 2 carries a scenario saying so in
those terms. Since no sentence of the promoted requirement becomes false, it is
left alone — the same test applied to "Canonical credential record shapes" in
§7. A seat may prefer it MODIFIED so the interaction is recorded in the
requirement's own text rather than in a neighbour's; that is a reasonable
ruling, and its cost is a second MODIFIED block with the ledger row it implies.

**`shared-authority-identity` is a new code and not a new message on an old
one.** Condition 3's failure is already refused by the default rule, so the code
adds no refusal — it adds a refusal that NAMES THE FAULT. A record with two
bindings, one secret and one fetch identity is not "two credentials collapsed";
it is the exact violation of "one identity MAY be shared; one AUTHORITY SHALL
NOT", and a reader who is told about secret reuse will fix the wrong thing. The
doc-health family's own rule applies — the failure message is a deliverable.

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

## 5. The closed block, and the hole it closes

`additionalProperties: false` goes ON THE BLOCK and is not proposed for the
binding object around it.

**On the block, because the hole is measured.** Executed on 2026-08-29 against
`contracts/schemas/xfactory-credential-contracts.schema.yaml`: a binding
carrying `consumer: {holder_ref: …, fetch_identity: …, totally: unchecked}`
validates with ZERO errors, because the binding object declares properties
without closing them. So the field this change adds already exists as an
unenforceable free-text hole, and any domain may be writing into it now,
invisibly to every consumer of the pinned contract. Declaring the block and
closing it is what converts that into a shape with a refusal.

**NOT on the binding object, and the restraint is the point.** Closing the
binding object would be a BREAKING change under the policy's own class
definition — it removes a shape (arbitrary extra keys) that pinned consumers may
be relying on — and it would do it silently, with no deprecation minor served.
The wider closure is named as a successor rather than smuggled in behind an
additive one, which is the same restraint the escrow packet exercised when it
kept its `escrow:` block optional.

## 6. What this makes provable — and the reach it does not have

Three limits, recorded here rather than left to be discovered, because the
predecessor change's ratification turned on exactly this kind of honesty and a
bot round caught the one place it had overclaimed.

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
the second modification also declines to create a third instance of a defect
class that is currently open twice over as issues #329 and #330. The proposal
records this as D-1 with the rejected alternative, so a seat can rule the other
way; the cost of ruling that way is a second live writer plus a ledger row in
the same commit.

**The requirement this change DOES modify is the custody change's**, and that
placement is chosen because it is the text this change makes stale. Its scenario
"The published binding shape cannot yet express the access identity" is FALSE
once the shape expresses it, and leaving a false scenario to promote into canon
would be worse than any ordering cost. Three facts make the placement safe
rather than merely defensible:

1. **`release-realization` governs it.** "Ordered deltas and branch vocabulary"
   requires the later proposal to reference the earlier change and declare its
   deltas relative to that change's outcome. The proposal does both, by name.
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
3. **The ordering is determinate in practice and stated as an obligation
   anyway.** The custody change carries `target_release: none` and its
   realization tasks §1–§3 are complete, so it archives on evidence that already
   exists; this change carries a contract cut and archives much later. The task
   list nonetheless states the inverse case and its remedy — convert the block
   to `ADDED` before archiving — because "the natural order will hold" is not a
   guarantee and the failure mode is a MODIFIED requirement promoting against
   canon that does not carry it.

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
string in the same commit or the suite fails. The escrow packet's design
recorded the identical hazard about the identical assertion; two packets tripping
over one string is a signal about the assertion, and whether the count should be
derived rather than asserted is worth a seat's opinion.

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
- **Not a second identity vocabulary.** Both identifiers are words this estate
  ratified before this packet existed.
- **Not a live secret act.** Nothing here creates, moves, or reads credential
  material; the block holds identifiers only.
