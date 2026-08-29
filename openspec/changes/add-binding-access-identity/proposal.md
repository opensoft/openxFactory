---
code_surface: openxFactory — A SCHEMA CHANGE PLUS PACKAGED FIXTURES PLUS ONE VALIDATOR RULE. `contracts/schemas/xfactory-credential-contracts.schema.yaml` gains THREE ADDITIVE OPTIONAL FIELDS on each entry of `xfactory_credential_binding_template`'s `credential_bindings` map — `access_identity` (the principal the consuming system presents to the secret store), `operated_identity` (the shared operated identity this binding consumes, declared only where one exists) and `consumer` (the consuming system this binding serves; RESTORED in the bot round after Codex disproved the reasoning that omitted it — the map is keyed by REQUIREMENT ID, not by system). Each is constrained to a NON-BLANK principal reference rather than an unconstrained string, because `""` and `"  "` are pairwise distinct and name nobody. `scripts/validate-credential-contracts.py` gains the discrimination these fields make decidable: its existing `shared-secret-identity` refusal stops reading one fact and starts reading three, so that TWO CREDENTIALS COLLAPSED INTO ONE stays refused while TWO CONSUMERS OF ONE OPERATED IDENTITY — the shape this capability's own ratified requirement mandates — becomes recordable; and the `baked-secret` refusal is extended to the new fields AND its detector EXPANDED to the forms the requirement names — today `_looks_like_raw_secret` recognises six markers plus a wholly base64-like value, so a connection string, a `password=` assignment and a dotted JWT all pass it. PLUS packaged conformance fixtures under the existing `examples/credential-contracts/` tree: the conforming two-consumer binding template that could not be shipped when the operated-identity requirement landed, and negative fixtures for each named refusal (a shared reference with no operated-identity declaration; a shared reference declared by only one of the sharing bindings; two bindings declaring one operated identity and ONE access identity; a blank or whitespace-only declared identity; credential material placed in an access-identity field, in each enumerated form). The self-test count asserted at `tests/credential_contracts/test_dispatch_credential_contract.py:35` ("3 positive + 5 negative") moves in the same commit as the fixtures, exactly as the custody change's task 4.1 said it must. `contracts/manifest.yaml`'s `credential-contracts` row (`:2079-2084`) takes the new digest and its consumption rule records the growth. NO new record kind, NO change to any other kind, NO registry, NO change to the trust-anchor tree.
target_release: THE NEXT ADDITIVE MINOR AFTER `contract-v2.1`, DELIBERATELY NOT NUMBERED HERE — allocated AT REALIZATION by merge order per `docs/contract-versioning-policy.md`, on the precedent the sibling packet `add-credential-escrow-checkout` sets for a proposal in exactly this position. **THE `contract-v1.45` DESIGNATION THIS SUCCESSOR WAS QUEUED UNDER IS STALE AND IS FLAGGED RATHER THAN SILENTLY RENUMBERED.** Verified in the working checkout on 2026-08-29 by parse and not by memory: `contract-v1.45` WAS CUT on 2026-08-26 and is SPENT — `contracts/releases/contract-v1.45.digests.yaml` exists, `contracts/CHANGELOG.md:467` carries its entry ("additive; the `approve-model` gate action and the turn record's mid-turn re-mint"), and `openspec/changes/add-doxchat-model-intake/proposal.md:3` declares `target_release: contract-v1.45` as the packet that spent it. The declared bundle has since advanced twice past the 1.x line: `contracts/manifest.yaml:3` reads `contract_bundle_version: contract-v2.1`, whose CHANGELOG entry is dated 2026-08-28, and `contracts/releases/` holds inventories through `contract-v2.1`. So the reserved number is not merely taken, it is four cuts behind the head. WHY A NUMBER IS NOT WRITTEN HERE EITHER: `add-credential-escrow-checkout` is realizing an additive minor against the SAME schema file in parallel, a number written in a proposal is a number another packet is already spending, and the `contract-v1.28` renumber sweep is the standing precedent for why. THE CLASS IS ADDITIVE (MINOR) AND NOTHING NARROWS: three new optional fields on a registered bundle contract is the versioning policy's additive class verbatim, `contract_schema_version` is unchanged, a binding declaring none of the three fields stays valid, and every consumer pinned at `contract-v2.1` stays conformant until it upgrades. ONE COMPATIBILITY CLAIM THIS PROPOSAL ORIGINALLY MADE IS WITHDRAWN AS FALSE, on Codex's proof: the binding entry object sets no `additionalProperties: false` (`contracts/schemas/xfactory-credential-contracts.schema.yaml:138-146`), so a record can ALREADY carry these key names today as inert extra properties and this change gives them meaning — such a record MAY newly be refused. The population is MEASURED before the cut (tasks §4.6) instead of assumed empty, and whether a newly-meaningful open key keeps the ADDITIVE class is put to the council as OQ-4 rather than settled here. A CUT IS NEVERTHELESS OWED, and its mechanism is the versioning policy rather than release-inventory drift: `contracts/schemas/xfactory-credential-contracts.schema.yaml` is a REGISTERED bundle contract (`contracts/manifest.yaml:2079`, `id: credential-contracts`) but is NOT a member of the declared release digest inventory, so the drift family will not force the cut and the policy does.
---

# Proposal: add-binding-access-identity

Status: draft
Proposed: 2026-08-29
Origin: THE NAMED SUCCESSOR OWED BY A RATIFIED CHANGE. Brett Heap ratified
`add-notebook-hosting-credential-custody` on 2026-08-23
(`openspec/changes/add-notebook-hosting-credential-custody/review/ratification-2026-08-23.md`,
"Ratifier: Brett Heap (repository owner) — in-session via question prompts"),
and that ratification's Decision item 3 records the enforcement gap this packet
closes and names its successor by task number. See `.openspec.yaml` for the
durable origin record and for exactly what that citation does and does not
cover.

Review path: **this change is the first subject of the §7.4 council-reviewed
but human-approved path** — the continuation of the 2026-08-28 gate-rules
ruling. Council review PRECEDES ratification; Brett's approve is the merge act.
Nothing in this packet is ratified by its authoring, by its bot round, or by
the council read. See "The review path this packet is the first subject of"
below.

## Why

A ratified requirement of this capability is enforced by nobody, and the
capability said so in its own promoted text rather than papering over it.

`add-notebook-hosting-credential-custody` promoted the rule that where more than
one system authenticates as the SAME operated identity, each SHALL reach that
identity's credential through its OWN binding — its own access identity, its own
grant, its own rotation visibility, its own audit trail. Its governing sentence:
**"One identity MAY be shared; one AUTHORITY SHALL NOT."**

The published record cannot express that. Quoting the ratification record's third
flagged item, which was before the ratifier at the read
(`openspec/changes/add-notebook-hosting-credential-custody/review/ratification-2026-08-23.md:49-60`):

> **The enforcement gap, admitted rather than papered over.** Per-system
> authority is NOT machine-provable today: the published
> `xfactory_credential_binding_template` requires only `[provider, secret_ref,
> owner, rotation_policy]` with optional `vault`, carries no consumer or
> access-identity field, and `scripts/validate-credential-contracts.py`
> compares no authorities — so two bindings naming the same vault principal
> validate cleanly. The invariant is held TODAY by review and by estate
> wiring. Making it provable means extending `contracts/schemas/`, which
> carries the full contract-release ritual, and is named as an owed successor
> (tasks §4.5) rather than folded in here.

The obligation is also carried in the PROMOTED spec text, so it is not merely a
task note. The custody change's ADDED requirement ships this scenario
(`openspec/changes/add-notebook-hosting-credential-custody/specs/credential-contracts/spec.md:60-63`):

> **Scenario: The published binding shape cannot yet express the access identity**
> — **WHEN** two bindings for one operated identity are recorded in the promoted
> binding-template shape — **THEN** the shape carries no consumer or
> access-identity field, so the per-system authority is asserted by the binding's
> owner and its estate wiring rather than proven by the record — **AND** the gap
> is recorded as owed to a successor that extends the shape, not left implied as
> enforced.

And the successor's own scope is written out, at
`openspec/changes/add-notebook-hosting-credential-custody/tasks.md:81-90`:

> **4.5 NAMED SUCCESSOR, owed:** extend the published binding shape so the
> per-system authority is REPRESENTABLE. Today `xfactory_credential_binding_template`
> requires only `[provider, secret_ref, owner, rotation_policy]` with optional
> `vault`, carries no consumer or access-identity field, and the validator compares
> no authorities — so two bindings using the same vault principal validate cleanly
> and the invariant is held by review rather than by the record. Adding that field
> is a `contracts/schemas/` change and therefore DOES carry the contract-release
> ritual (CHANGELOG allocation, manifest digest, `contract_bundle_version` bump,
> inventory rebuild, verify-commit, tag) — which is precisely why it is a successor
> and not smuggled into this change.

That is the whole scope of this packet, and it is quoted rather than composed.

## The second half the same change told this successor to decide first

The gap has a twin, and the custody change was explicit that the successor must
settle it BEFORE shipping a fixture. At
`openspec/changes/add-notebook-hosting-credential-custody/tasks.md:53-66`, recording why its own
planned conformance fixture was DECLINED:

> ...a fixture would TRIP the validator: `shared-secret-identity` fires whenever
> two bindings in one template share a `secret_ref`
> (`scripts/validate-credential-contracts.py`), and two systems reaching ONE
> account's password is exactly that shape. Giving them distinct `secret_ref`s to
> satisfy the rule would misrepresent the estate (there is one secret), and
> relaxing the rule is a change to a check that exists to keep the dispatch and
> content credentials apart. So the requirement text carries the shape and no
> fixture is added. **If a later change wants one, it must first decide whether
> `shared-secret-identity` should distinguish "two credentials collapsed into
> one" from "two consumers of one credential"** — and updating the self-test
> count asserted in `tests/credential_contracts/` ("3 positive + 5 negative")
> rides with it.

So the capability is currently in a state where **its own mandated shape cannot
be written down**: the record has no way to say "these two bindings are two
consumers of one operated identity", and every attempt to say it is refused by a
check that reads one fact. The requirement stands, the fixture is absent, and
the absence is not an oversight — it is recorded, with its reasoning, in the
change that ratified the requirement.

This packet takes that decision. **`shared-secret-identity` SHALL
discriminate, and the discriminator is a DECLARATION and not an inference.**

## What this changes

**One field makes the authority representable; a second makes the refusal
decidable; a third says whose authority it is.** All three are additive and
optional.

- `access_identity` — the principal the consuming system presents to the secret
  store. This is the field task 4.5 names, and it makes per-system authority a
  fact in the record.
- `operated_identity` — WHICH shared operated identity this binding consumes,
  declared only where one exists.
- `consumer` — the consuming system this binding serves. **Restored in the bot
  round after its omission was DISPROVEN.** It was originally left out on the
  reasoning that "the binding's map key already names the system"; Codex showed
  that reasoning is factually wrong — `credential_bindings` is keyed by
  REQUIREMENT ID, stated in terms by the custody change's own design
  (`openspec/changes/add-notebook-hosting-credential-custody/design.md:121-125`,
  "a `credential_bindings` map keyed by requirement id"), and the shipped
  example uses keys like `intent_dispatch` and `corpus_content_write` — purposes,
  not systems. Without it, two requirement-keyed bindings could carry distinct
  access identities while leaving unstated WHICH system holds each, so the
  attribution the capability asks the store's access log to deliver stayed
  unprovable. Task 4.5 names "no consumer or access-identity field" — **two**
  things — so the field was inside the quoted scope all along and its omission
  was the deviation.

**Why the second field is structurally necessary rather than decorative.**
Suppose the discrimination keyed on `access_identity` distinctness alone: two
bindings sharing a `secret_ref` would become conforming whenever they named two
different principals. But the DEFECT the existing check catches has exactly that
shape too — the openXdox dispatch binding and the content-write binding are
served by different workload identities and would collapse onto one App key with
the refusal silently satisfied
(`examples/credential-contracts/negative/dispatch-reuses-content-secret.yaml`).
Keying on access identity alone would therefore REGRESS the check it is meant to
refine. What separates the two cases is INTENT, and intent has to be declared:
two credentials collapsed into one declare no operated identity, **because
there is no one identity to declare**.

So the licit condition is a conjunction of three facts, not one:

| bindings share a `secret_ref` | all declare the same `operated_identity` | each declares a distinct NON-BLANK `access_identity` | outcome |
| --- | --- | --- | --- |
| yes | no (none declare) | — | **REFUSED** — unchanged, the collapsed-credential defect |
| yes | partially | — | **REFUSED** — an unexplained share is an unexplained share |
| yes | yes | no (same principal) | **REFUSED** — one identity shared, one authority shared |
| yes | yes | blank / whitespace-only | **REFUSED** — a blank value names no principal |
| yes | yes | yes | **VALID** — the shape the capability mandates |
| no | — | — | untouched *(blankness still refused on its own terms)* |

**Distinctness is not a string comparison alone.** `""` and `"  "` are pairwise
distinct and name nobody, so unconstrained strings would let the conjunction be
satisfied by records identifying no authority at all. Every declared identity
must be a non-blank principal reference BEFORE distinctness is considered, and
blankness is refused on its own terms — including on a binding that shares no
reference, which the grouping check never reaches. Codex found this; the
repository already has the precedent in the doxBench admission-form predicate
(issue #263), where a blank-class refusal was made explicit rather than left to
a truthiness test.

**Default-refuse is preserved — and the compatibility claim is now the WEAKER,
TRUE one.** As authored this proposal claimed that "every new refusal is
reachable only through a field no earlier record could carry, because the field
did not exist." **That was false, and Codex proved it against the schema.** The
binding entry object sets no `additionalProperties: false`
(`contracts/schemas/xfactory-credential-contracts.schema.yaml:138-146`; the only
`additionalProperties: false` in the file is at `:56`, on a different object), so
a record valid at `contract-v2.1` can ALREADY carry a key called
`access_identity` today as an inert extra property. This extension gives that key
MEANING, so such a record could newly be refused. What is true is narrower and is
what the packet now claims: **a record that declares none of the three fields is
unaffected**, and the population that declares any of them is **MEASURED before
the cut rather than assumed empty** (tasks §4.6). The class question this raises
— whether a newly-meaningful open key keeps the ADDITIVE (MINOR) classification —
is **flagged for the council rather than settled here** (OQ-4).

**The core rule follows the field, and its reach is stated honestly.**
`baked-secret` reads `secret_ref` alone today, via a detector that recognises six
markers plus a wholly base64-like value
(`scripts/validate-credential-contracts.py:38-40,60-62`). Codex showed that
reusing it as-is would NOT implement the prohibition this packet writes:
`postgresql://user:password@host/db`, `password=hunter2` and a dotted JWT all
pass it, while the requirement forbids passwords, tokens and connection strings
by name. The detector is therefore EXPANDED with the enumerated forms and their
fixtures (tasks §3.3), and the requirement now says what a detector can and
cannot deliver: passing is evidence that no ENUMERATED form was found, never
evidence that the value is not credential material.

**The fixture that could not be written gets written.** With the discrimination
settled, the conforming two-consumer template becomes recordable, and the
self-test count moves with it in the same commit, as instructed.

## What this deliberately does not change

- **No new record kind.** Five kinds today, six once
  `add-credential-escrow-checkout` archives; this packet adds none.
- **No `## MODIFIED Requirements` block, and the omission is deliberate rather
  than convenient.** See "The requirement this packet may not touch" below.
- **No change to `contracts/trust-anchor/`.**
- **No registry, no inventory obligation, no drift audit** — those belong to the
  escrow line and are not touched from here.
- **One access identity presenting for two bindings with DIFFERENT secret
  references is NOT legislated.** That is privilege aggregation, a real question
  and a different one. It is named in Open Questions rather than decided quietly.
- **No claim that the estate was verified.** The record proves a CLAIM of
  distinct authorities exists and is refusable when self-contradictory. Whether
  the two named principals really exist, really differ, and really carry
  different grants is the store's fact and the operator's, and the requirement
  text says so in its own paragraph. This packet does not read a live directory.

## The requirement this packet may not touch

The sentence naming which kinds and which fields the canonical schema owns lives
in `Canonical credential record shapes`. **`add-credential-escrow-checkout` is
holding a LIVE `MODIFIED` block on exactly that requirement right now**
(`openspec/changes/add-credential-escrow-checkout/specs/credential-contracts/spec.md:5`),
carrying the sixth record kind and the optional `escrow:` block.

The custody change refused this collision explicitly, and its ratification record
states the discipline (`openspec/changes/add-notebook-hosting-credential-custody/review/ratification-2026-08-23.md:46-48`): *"no
requirement is MODIFIED here precisely so that two active changes never hold two
live deltas on one requirement text."* OpenSpec's `MODIFIED` REPLACES wholesale;
two live blocks on one requirement is the exact machinery that produced the
silent-scenario-loss class of issues #329 and #330, and `--strict` sees none of
it.

This packet therefore carries **ADDED requirements only**, and records the
shape-ownership sentence as an OWED sequencing obligation rather than dropping
it: tasks §2.3 puts it on whichever of the two packets archives SECOND, with the
scenario-complete restatement that requires. This is OD-3 below, flagged for
veto — the alternative (this packet takes the MODIFIED block and the escrow
packet drops it) reverses a ruled decision on a ratified packet and is not the
authoring session's to take.

## The review path this packet is the first subject of

The 2026-08-28 gate-rules convening ruled a class of gate rule never convenable
at the code-level floor and established, in continuation, a §7.4-shaped path in
which a proposal is **council-reviewed but human-approved**. This packet is that
path's designated first subject.

What that means concretely, and what it does not:

1. Authoring, the bot round, and the council read are all PRE-ratification. None
   of them ratifies anything.
2. The council review happens OUTSIDE the pipeline, on the 2026-08-28 procedure.
3. **Brett Heap's approve is the merge act and the ratification act.** Until it
   happens this packet stands at `Status: draft`, carries no ratification
   citation, and none is owed — the promoted lifecycle rule requires one only
   for `Status: ratified`.
4. Every decision below marked OD is the AUTHORING SESSION's and is flagged for
   veto. The origin citation covers admission and scope, not this text.

## Orchestrator decisions — flagged for veto

- **OD-1 — THREE FIELDS (was two).** Task 4.5 names "no consumer or
  access-identity field", naming two things without specifying either.
  `operated_identity` is the third and is structurally forced (see the regression
  argument above). *Recommendation: accept.* The alternative — one field and an
  inference — regresses an existing refusal, which is the one outcome the custody
  change said must not happen.
- **OD-2 — THE FIELD NAMES. CORRECTED IN THE BOT ROUND; THE ORIGINAL REASONING
  WAS DISPROVEN.** `access_identity` is task 4.5's own phrase. `operated_identity`
  takes the ratified vocabulary of the custody requirement. `consumer` names the
  consuming system. As authored this packet OMITTED the consumer field, arguing
  that "the word consumer is ambiguous between the SYSTEM and the IDENTITY, and
  the binding's map key already names the system." **The second half of that is
  false**: the map is keyed by REQUIREMENT ID, per the custody change's own
  design
  (`openspec/changes/add-notebook-hosting-credential-custody/design.md:121-125`)
  and per the shipped example's `intent_dispatch` / `corpus_content_write` keys.
  The field is restored, the ambiguity is resolved by NAMING it (`consumer` is
  the system; `operated_identity` is the identity), and the disproof is recorded
  rather than the conclusion quietly swapped. *Recommendation: accept the
  correction.*
- **OD-3 — ADDED-ONLY, WITH THE SHAPE SENTENCE OWED.** Stated in full above.
  *Recommendation: accept*, with tasks §2.3 as the discharge.
- **OD-4 — THE REFUSAL FOR A SHARED ACCESS IDENTITY IS AN ERROR, NOT A WARNING.**
  Two bindings declaring one operated identity and one access identity contradict
  the ratified requirement in the record itself. *Recommendation: accept.* A
  warning would let the record assert a separation it denies in the same breath.
- **OD-5 — PRIVILEGE AGGREGATION IS LEFT OPEN.** See Open Questions OQ-1.
  *Recommendation: accept the deferral*; deciding it here widens a packet whose
  scope is quoted from a ratified successor note.
- **OD-6 — NO DOMAIN REPOSITORY IS ASKED TO MOVE.** All three fields are
  optional, so no consumer owes an upgrade. The live per-system bindings the
  custody change routed to the installs (its tasks §4.2/§4.3) MAY adopt the
  fields when they are authored; this packet neither requires nor schedules that.
  *Recommendation: accept.*
- **OD-7 — BLANKNESS IS REFUSED EVERYWHERE, NOT ONLY UNDER A SHARED REFERENCE.**
  A blank identity on a binding that shares nothing would never reach the
  grouping check, so the refusal is stated on the field itself. *Recommendation:
  accept.* A value that names no principal is not a weaker declaration; it is a
  declaration that asserts nothing while looking like governance.

## Open Questions

- **OQ-1 — Should one access identity presenting for two bindings with DIFFERENT
  secret references be refused, warned, or ignored?** It is privilege aggregation:
  one principal able to fetch two distinct credentials. There is a real argument
  it belongs to the same invariant and a real argument it is a separate one.
  *Recommendation: leave it for a named follow-up.* Nothing in the quoted
  successor note reaches it, and this packet's scope is quoted, not composed.
- **OQ-2 — Should `operated_identity` be constrained to a vocabulary, or free
  text?** The roster and the identity line hold real subject records that a
  future change could bind it to. *Recommendation: free text at this cut*, on
  the same ground the escrow block took its shape from running prior art rather
  than inventing a registry; binding it to a roster record is a follow-up with
  its own resolution question.
- **OQ-3 — Does the conforming fixture name the real `xFactor001@opensoft.one`
  account, or a neutral placeholder?** The custody requirement says naming a
  concrete estate fact in a per-client BINDING INSTANCE is correct, but
  `contracts/manifest.yaml` records that *"openxFactory ships no instance
  records"*, and a packaged fixture is neither exactly. *Recommendation: a
  neutral placeholder*, because the fixture's job is to exercise the shape and a
  real account name in a neutral repository invites the residency question the
  custody ratification just settled in the other direction.
- **OQ-4 — NEW, RAISED BY THE BOT ROUND. Does a newly-meaningful open key keep
  the ADDITIVE (MINOR) classification?** The binding object accepts unknown
  properties, so `access_identity` is not a NEW key — it is an EXISTING inert one
  this change gives meaning to, and a record already carrying it could newly be
  refused. That is not the textbook additive case ("new optional fields") and it
  is not a narrowing of any DECLARED shape either. *Recommendation: keep ADDITIVE,
  conditional on the §4.6 measurement returning an empty population, and record
  the reasoning in the CHANGELOG entry rather than leaving the class implied.*
  This is a versioning-policy judgement and is put to the council rather than
  taken here.

## Impact

- **Capability:** `credential-contracts` — 3 ADDED requirements, 15 scenarios,
  no requirement modified.
- **Contract surface:** three additive optional fields on one existing record
  kind, each constrained to a non-blank principal reference; one registered
  bundle contract's digest moves; an additive minor is owed at realization.
- **Consumers:** none obliged to move. Every record that declares none of the
  three fields is unaffected; the population declaring any of them is measured
  before the cut (tasks §4.6) rather than assumed empty.
- **Discharges:** `add-notebook-hosting-credential-custody` tasks §4.5 (the named
  successor) and the decision its §4.1 required before a fixture could ship.
- **Coordinates with:** `add-credential-escrow-checkout`, which edits the same
  schema file and holds the MODIFIED block on the requirement this packet may not
  touch. Merge order matters and is handled in tasks §2.3 and §3.
