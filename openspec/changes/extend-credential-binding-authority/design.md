# Design: extend-credential-binding-authority

Status: draft

Task 4.5 of `add-notebook-hosting-credential-custody` names the deliverable in
one sentence: extend the published binding shape so the per-system authority is
REPRESENTABLE. This document records what the repository's own evidence said
when that sentence was worked out into a shape, including the two places where
the evidence overturned the obvious answer.

## The measured starting point

Read from the tree on 2026-08-29 rather than recalled:

- `xfactory_credential_binding_template` in
  `contracts/schemas/xfactory-credential-contracts.schema.yaml` puts each entry
  of `credential_bindings` under `required: [provider, secret_ref, owner,
  rotation_policy]` with `vault` optional and no other properties. There is no
  consumer field and no identity field.
- `scripts/validate-credential-contracts.py` runs three semantic checks over
  that kind — `baked-secret` and `shared-secret-identity` on bindings, and the
  issuance-precondition vocabulary on requirements. It compares no identities,
  and it has NO WARNING CHANNEL AT ALL: `_semantic_findings` returns strings
  that the caller counts as errors, and the self-test asserts positives produce
  none.
- The binding object does not set `additionalProperties: false`, so an
  undeclared key on a binding validates today.

That last fact is why the gap has been invisible rather than noisy: the record
has always ACCEPTED an authority field and never MEANT anything by one.

## The forcing fact: the key is already in the tree, unclaimed

`contracts/avatar-client/broker-server-key-binding.template.yaml` is
`kind: xfactory_credential_binding_template` and carries, at document level:

```yaml
resolution:
  resolved_by: broker_only
  fetch_identity: install_federated_workload_identity
  materialization: ephemeral_process_scope
```

An undeclared extra key on a neutral schema that neither declares nor forbids
it. That description is not this document's characterization — it is the
schema's own words about the last time this happened to it. The
`issuance_preconditions` block was added because *"the mechanism existed as a
domain-local extra key riding a neutral schema that neither declared nor forbade
it, so a refusal had no neutral home to be declared against."* Same schema, one
record family over, and this time the key is on the very kind being extended.

Two consequences are taken from it and one is deliberately not.

- It settles the SPELLING (below): the estate reached for `fetch_identity`
  unprompted.
- It settles that the field belongs on the RECORD rather than in guidance.
- It does NOT authorize migrating that file. `qualify-avatar-live-voice` is
  active and owns it, the document-level block stays valid because this change
  narrows nothing, and a packet that adds a field does not edit another active
  change's artifact to use it. Named as owed in the requirement and in the
  proposal's honest gaps.

There is a real shape difference worth stating rather than glossing: that record
carries ONE fetch identity for the whole document, and this change puts the
field on EACH BINDING. Per-binding is the general form and document-level is its
single-binding degenerate case — and per-binding is forced, because the whole
subject is two bindings differing in exactly this field. A document-level field
cannot express the thing the ratified requirement is about.

## Ruling: the spellings are the estate's, and there are no new ones

Three names, three pieces of evidence, no coinage.

**`fetch_identity`.** The promoted `credential-contracts` text says the lane
receives "an opaque secret reference and a fetch-identity identifier", and that
reference delivery is "a vault URI plus the runtime's own fetch identity", and
names "a per-install fetch identity" in the degraded-mode clause. Five
occurrences across three promoted requirements, plus the shipped record above.

**The competing spelling, handled rather than ignored.** "Access identity"
appears in the custody packet's ratified requirement text, in its tasks, and in
`docs/lifecycle-notebook-projection.md` — the doc that packet realized. It is
the newer word and the narrower one: it appears in exactly one thread, where
`fetch_identity` appears in promoted canon and in a contract artifact. The
decision is that the RECORD takes one spelling, `fetch_identity`, and the
requirement declares the synonymy so a reader of the ratified custody text is
never left wondering whether two fields are meant. **The ratified text is not
edited to match.** A ratified delta is a record; rewriting one for a successor's
convenience is the move this repository refuses elsewhere, most explicitly in
the versioning policy's insistence that a `Status: record` document stating a
since-changed fact is "deliberately NOT edited". The synonym costs a sentence;
the edit would cost the record.

**`requirement_id`, not `requirement_ref`.** The grant template already carries
`requirement_id` for exactly this relation — which credential requirement this
record resolves. `secret_ref` and `audit_ref` name REFERENCES INTO OTHER
SYSTEMS; a requirement is a sibling record in the same family, and the family
already spells that `requirement_id`. Matching the existing field is one fewer
vocabulary.

**`consumer`.** The custody requirement and the README both say "consuming
system". `consumer` is that noun; nothing else in the binding object claims the
word, and the manifest's `intended_consumers` is a different object describing
who consumes a CONTRACT, not who consumes a credential.

## Ruling: why three fields and not the two task 4.5 names

Task 4.5 names two — "no consumer or access-identity field". Two are enough to
make the authority WRITABLE. They are not enough to make the shared-secret
question ANSWERABLE, and that question is a precondition of the fixture task 4.1
declined. `requirement_id` is this packet's addition, it is the whole of decision
4, and its consequence is stated plainly: **cut it and the recommended position
on 4.1 is unavailable, because the alternative discriminator is the one shown
below to be wrong.**

## Ruling: the 4.1 question, and why the obvious discriminator fails

Task 4.1: should `shared-secret-identity` distinguish "two credentials collapsed
into one" from "two consumers of one credential"?

**Recommended: YES, and the discriminator is the SAME `requirement_id`.**

The obvious answer is "two consumers of one credential is fine if the consumers
are distinct" — exempt on distinct `consumer` values, perhaps also on distinct
`fetch_identity` values. **The repository contains the counterexample, packaged
as a test fixture.**

`examples/credential-contracts/negative/dispatch-reuses-content-secret.yaml`
holds the fault the check exists to catch: the openXdox dispatch credential and
the content-write credential resolved to one `secret_ref`. Now ask what those
two bindings look like under the new fields:

- Their consumers are DIFFERENT. One is the zero-write serving tier, the other
  the privileged CI apply lane — the promoted requirement's own words are that
  "a zero-write-authority serving surface holding a dispatch-only credential
  MUST NOT hold — nor hold key material capable of minting — a content-write
  credential." Two surfaces, two consumers.
- Their fetch identities MUST be different, by that same requirement: "a
  dispatch binding names the same App or key identity as a content-write
  binding … MUST be rejected".

So the naive exemption is satisfied EXACTLY by the record it must refuse. It
would turn a packaged negative green. That is not a close call, and it is the
reason the recommendation is not the obvious one.

What actually separates the two cases is PURPOSE, and purpose is the credential
requirement. The dispatch fault is one key serving TWO requirements. The
notebook estate is one key serving ONE requirement — the hosting account's
credential — reached by two consumers. `requirement_id` is that fact, and it is
a fact the record would carry anyway.

Three further properties, each checked rather than assumed:

- **Nothing previously refused becomes conforming by default.** Every condition
  is a positive declaration, and no existing record makes any of them. The
  packaged negative stays red because it declares no `requirement_id` at all.
- **The dispatch-only separation requirement is not modified, in text or in
  force.** Its bindings resolve two requirements; the exemption's first
  condition can never hold for them.
- **The exemption is unanimous, not majority.** EVERY binding sharing the
  `secret_ref` must satisfy all three conditions. Three bindings where two
  conform and one does not is a refusal, because a shared key with one
  unaccounted consumer is the fault regardless of its better-behaved neighbours.

### The alternative, and its honest cost

**Leave `shared-secret-identity` unconditional.** The council may prefer a check
with no exemption at all; simplicity is a real argument and the fault class is
serious.

Its cost is not that the estate becomes non-conforming — it is that the estate
becomes UNREPRESENTED, and the unrepresented shape has somewhere silent to go.
The rule compares bindings within ONE document (`seen` is a per-document dict).
Two consumers of one operated identity split across two template files trip
nothing, today and under the unconditional rule alike. So the unconditional rule
does not prevent the shape; it prevents the shape being written down where a
check can see it. That is the cost to weigh: a rule that refuses the honest
record and permits the split one.

## What was considered and declined

**One binding carrying a list of consumers.** Represents "one credential, N
authorities" with no exemption needed, because there is only one binding and
`shared-secret-identity` never fires. DECLINED: the ratified custody requirement
says each consuming system reaches the credential "through its OWN binding" and
that "each binding SHALL therefore be revocable on its own, and revoking one
SHALL NOT disturb the other's ability to fetch." A list inside one binding makes
revocation-independence a property of list entries rather than of bindings,
which is a different contract from the one that was ratified.

**A marker whose only effect is to silence the check** — `shared_identity: true`
or similar. DECLINED on two of this family's own precedents. The
`issuance_preconditions` design refuses a declaration that "reads as governance
while asserting nothing", to the point of making every member `const: true` so
that a false value cannot exist. And Brett's ratified trust-anchor ruling
refuses an escrow discriminator on a custody axis, on the grounds that a member
existing only to encode what the axis cannot say makes both unreadable. A
boolean that turns a refusal off is that species. The discriminator must be a
fact the record would carry anyway — which `requirement_id` is and a silence
flag is not.

**Making the fields required now.** DECLINED by the versioning policy, not by
preference: "a required field is added" is its BREAKING (major) class, requiring
"at least one full minor release where the old shape produced deprecation
warnings". The warning IS the migration path, and it is served first.

**Modifying a promoted requirement to hang this on.** DECLINED after checking
which requirements are already spoken for. `add-credential-escrow-checkout`
carries a live MODIFIED block on "Canonical credential record shapes";
`add-notebook-projection-identity` carries one on "The credential vault operator
is an execution binding". Those are the two a shape change would most naturally
attach to, and both would put a second live delta on one requirement — the exact
hazard the custody packet's design refused for its own text. Three ADDED
requirements avoid it, and the obligations are genuinely additive: the ability of
a record to STATE an authority is not a refinement of the shapes requirement.

## The validator, precisely

Three changes to `scripts/validate-credential-contracts.py`, specified here so
realization is mechanical.

1. **`shared-fetch-identity` (ERROR).** Within one document, two bindings
   declaring equal `fetch_identity` and both declaring `consumer`, where the
   consumers differ. Not raised when either side omits `consumer` — see 3.
2. **`shared-secret-identity` (ERROR, refined).** Group bindings by
   `secret_ref`. A group of size > 1 raises unless EVERY member declares
   `requirement_id`, all equal; and every member declares `consumer` and
   `fetch_identity`, each pairwise distinct across the group. The existing
   message is kept for the unexempted case, because it is the same finding.
3. **`binding-authority-undeclared` (WARNING).** A binding declaring neither
   `consumer` nor `fetch_identity`. This requires the validator's FIRST warning
   channel: warnings print with a `WARN` prefix, do not increment `errors`, and
   do not change the exit code. Two consequences to get right — the self-test
   must assert positives raise no ERRORS while REPORTING their warning count, so
   that a positive silently acquiring a warning is visible rather than absorbed;
   and the existing packaged positives WILL warn, which is correct and is the
   deprecation working, not a fixture defect.

**The fail-open is deliberate and bounded.** Rule 1 stays silent when a consumer
is undeclared because the record genuinely cannot distinguish one consumer from
two, and inventing a verdict from an absent field is how a check earns
distrust. The silence is not a clearance: rule 3's warning is already standing
on that binding, saying the record does not yet answer. This is the same
posture the family took when it declined to fabricate origin history for
pre-contract changes — report the absence, never infer the fact.

## Fixtures and the count string

`examples/credential-contracts/` gains one positive and two negatives; the
self-test line moves from "3 positive + 5 negative" to "4 positive + 7
negative", and `tests/credential_contracts/test_dispatch_credential_contract.py`
asserts that string and lists the fixture filenames, so it moves in the same
commit. The custody packet's task 4.1 warned about exactly this coupling.

- **Positive — the two-consumer shape task 4.1 could not package.** Two
  bindings, one `secret_ref`, one shared `requirement_id`, distinct `consumer`
  and distinct `fetch_identity`. This is the ratified custody shape becoming
  packageable, which is the clearest single proof the change did its job.
- **Negative — `shared-fetch-identity`.** Two consumers, one fetch identity.
- **Negative — the naive exemption's counterexample.** Two bindings sharing a
  `secret_ref` with distinct consumers and distinct fetch identities but
  DIFFERENT requirements, expecting `shared-secret-identity`. This fixture is
  the executable form of the 4.1 argument: it is green under the rejected
  discriminator and red under the recommended one, so the decision cannot be
  silently reversed later without a test going red.
- The existing `dispatch-reuses-content-secret.yaml` is UNCHANGED and stays
  red, which is the backward-compatibility proof.

Fixture residency is unchanged and needs no ruling: `examples/` is packaged
fixture territory, is not a release-inventory member, and is not registered in
`contracts/manifest.yaml` — so adding these three moves no bundle member.

## The release ritual, and the packet it must not collide with

The cut is owed by the versioning policy rather than by inventory drift, and the
measurement is in the proposal's front-matter: the credential schema is not one
of `contract-v2.1.digests.yaml`'s 192 entries. The number is allocated at
realization by merge order; `contract-v2.2` is expected and is not reserved.

**`add-credential-escrow-checkout` is the coupling, and it is stated here rather
than met at a merge conflict.** It is active, ratified 2026-08-28, and its own
code surface adds an optional `escrow:` block to THIS binding template and a
sixth record kind to THIS schema, teaches THIS validator both, and owes THE SAME
next additive minor. The two are compositionally independent — different keys,
different rules, neither reading the other's fields — so this is a sequencing
question, not a conflict of substance:

- Whichever lands second rebases onto the first. Both touch
  `contracts/schemas/xfactory-credential-contracts.schema.yaml` and
  `scripts/validate-credential-contracts.py`.
- Whether the two ship ONE combined additive cut or TWO sequential ones is put to
  the review as decision 7. One cut is fewer rituals and one changelog entry
  describing two unrelated additions; two cuts keep each packet's evidence with
  its own bundle. This packet has no stake in the answer and will take the
  ruling.
- Its self-test fixtures live under `contracts/credentials/examples/`, a
  different tree from `examples/credential-contracts/`, so the count string this
  packet moves is not one that packet also moves. Verified rather than assumed.
