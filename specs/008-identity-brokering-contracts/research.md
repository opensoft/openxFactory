# Research: identity-brokering neutral contracts

**Feature**: `008-identity-brokering-contracts`
**Governing change**: `add-identity-brokering` (ratified 2026-08-21, Brett Heap)

This file records the two settlements the ratified change assigned to this
feature (its task 2.3), the three further shape decisions the schemas rest on,
and the convention and dependency findings the implementation follows.

Both settlements were RECOMMENDED by the design and ADOPTED AS WRITTEN at
ratification ("all design decisions adopted as written, OQ-1 through OQ-4
recommendations adopted as the working recommendations at the settlement points
their tasks name"). They are recorded here as SETTLED, with the reasoning
carried, because change task 2.3 requires the resolution to live in this
feature's research rather than in a commit message.

## Settlement 1 — the `actor_subject` field shape (change task 2.3, design OQ-3)

### The question

Single opaque identifier, or a small structured object carrying issuer, subject
and display name?

### Settled: the STRUCTURED REFERENCE

Realized as `contracts/identity-brokering/actor-subject-reference.schema.yaml`
(`kind: actor_subject_reference`): `issuer.broker_instance_id`, `subject`,
`display_name_at_record`, and a `provenance` discriminator.

### Why

Three reasons, in the order they bind.

1. **A bare subject is ambiguous without its issuer**, and design D3 makes
   multiple broker instances an EXPECTED state rather than a hypothetical: the
   co-residence gate found a population (HealthLinc clinical patients) that must
   be served by a dedicated instance before the shared instance has its first
   client. A record carrying only `sub-8f2c…` cannot say which instance issued
   it, and the first migration or second instance makes every such record
   unresolvable.
2. **The display name has to travel with the record.** The requirement fixes
   that a record stays readable without a live broker, which a bare identifier
   cannot satisfy. Once the display name is in the object, the object exists;
   adding the issuer to it costs one field.
3. **The asymmetry of the two mistakes.** The cost of the structured reference
   is a wider field. The cost of guessing the other way is a schema major on a
   field embedded in every governed record that names a human — the most
   expensive kind of shape to change.

### What the settlement does NOT do

It does not settle how a specific consuming record family embeds the reference
(inline object, or a reference to a stored one). The gate-console binding —
change task 4.4 — is named as the change that confirms or overrides the shape
against a real record before the bundle cuts, and it can do so because this
schema is the vocabulary that record will use, not a field inside it.

## Settlement 2 — pre-broker history (change task 2.3, design OQ-1)

### The question

What happens to records written before the broker existed, which carry bare
usernames — a mapping table, a one-time backfill, or leave history as-is and
mark the boundary date?

### Settled: MARK THE BOUNDARY DATE, MAP ON DEMAND, NEVER BACKFILL

Realized as the three `provenance` classes, with the wrong combinations
unrepresentable:

| provenance | requires | forbids |
|---|---|---|
| `broker_asserted` | `issuer`, `subject` | `pre_broker` |
| `pre_broker_username` | `pre_broker` (username + `persona_boundary_date` + `presented_as_persona: false`) | `subject`, `issuer`, `mapping` |
| `mapped_historical_actor` | `issuer`, `subject`, `mapping` (mapped-from username, mapper, date, evidence) | `pre_broker` |

### Why

A blanket backfill asserts identity resolutions nobody verified. That is the
same false-audit failure the merge ruling (design D4) refuses — a record that
says the broker vouched for something it never saw is worse than a record that
says "this predates the broker", because the second is honest and the first is
not. And a mapping table that had to be complete before the broker was useful
would stall the whole adoption behind a data-cleanup exercise nobody has
budgeted.

Marking the boundary costs one date. Mapping costs one recorded act, taken only
where a specific record needs attribution, and the record of that act names who
mapped it and on what evidence.

### The structural half

The requirement's invariant — "SHALL NOT be presented as a broker-asserted
persona" — is not left to prose. `pre_broker.presented_as_persona` is a
REQUIRED CONSTANT `false`: the claim is always present and only one value is
legal, so a pre-broker record asserting itself a persona is not something the
shape can say. The validator closes the remaining route (a bare username pasted
into the `subject` field of a `broker_asserted` record) by refusing any subject
the corpus records as a pre-broker username.

## Decision 3 — the closed allow-list is DERIVED FROM THE SCHEMA

### What the design demands

Design D2's named risk states the requirement precisely: "The validator must
enforce the persona-assertion and organization property sets as a CLOSED
ALLOW-LIST rather than a denylist of forbidden names, because a denylist admits
every field nobody thought to forbid."

### The implementation, and why it is not a second list

The validator walks each document in parallel with its schema and computes the
legal property names AT EACH PATH from the schema itself — resolving local
`$ref`s and unioning `properties` across `allOf` / `anyOf` / `oneOf` / `if` /
`then` / `else`, so a property declared only inside a conditional branch (the
actor reference's `pre_broker`, for instance) is legal where the contract says
it is.

Writing the allow-list as a literal set in the validator would have been
simpler and wrong for the same reason a denylist is wrong: it would be a second
statement of the contract, free to drift from the first. The union across
branches is what makes the derivation faithful; a branch-blind walk would
report a conformant document's own property as unknown, and the pressure to fix
that would be to weaken the rule.

### Two codes, one walk

An undeclared property is reported as `closed-world-property` everywhere, and
ADDITIONALLY as `never-mirror-property` on `persona_assertion` and
`broker_organization`. Those are the two shapes the never-mirror rule governs
and the two where a tenancy projection actually arrives; the second code exists
so the refusal names the rule rather than the mechanism.

## Decision 4 — `served` bridges to the canonical `subject` layer

### The tension

The ratified change's task 1.2 fixes the company-role enumeration as
`` `tenant` | `served` — the ratified `layer-vocabulary` spelling ``.
`contracts/policies/layer-vocabulary.yaml` declares the canonical layer ids as
`subject`, `tenant` and `domain`; `served` is not one of them — it appears in
that policy as the ROLE TEXT of the subject layer ("The served party or work
subject"), and design D1 writes the pair as "**tenant** companies (the operator
layer) and **subject/served** companies".

### The resolution

The enumeration is `tenant | served`, as the ratified task text fixes it,
because a COMPANY BOUNDARY is not a Hermes layer: it is the company a persona
belongs to, and "served company" is what that boundary is called in the
requirement text. The family carries an explicit BRIDGE to the canonical layers
(`tenant` -> `tenant`, `served` -> `subject`), stated in the schema description
and enforced in the validator, and:

- the bridge's TARGETS are checked against the policy at run time, so renaming
  a canonical layer fails loudly here rather than leaving this family speaking a
  second spelling of the layer model;
- the policy's `reserved_layer_terms` (`customer`, `client`) are read from the
  same source and refused, so the retired spellings cannot re-enter through a
  company role;
- the governed-record pointer's `record_kind` is validated against the
  canonical layer ids directly, because THAT field does name a layer.

Restating the layer ids or the reserved list inside the validator would have
recreated exactly the drift `adopt-subject-tenant-domain-vocabulary` exists to
prevent. Reading them is the same technique `validate-openxwallet.py` uses for
the job envelope's approval-policy vocabulary.

## Decision 5 — the opaque subject carries a length floor

`opaque_subject` is `minLength: 16` with a pattern admitting no '@' and no
whitespace.

The pattern is uncontroversial: it makes an email address and any multi-word
display name unrepresentable in the identifier position, which is half of
requirement R5 enforced structurally rather than by review. The floor is the
interpretive call, and it is recorded here because it is the one place this
feature constrains a consumer beyond the ratified text.

A broker-issued subject is not a name. Every mechanism in use issues an opaque
value well over 16 characters (a UUID is 36), while the identifiers R5 refuses —
`bheap`, `jsmith`, `svc-1` — are short. Without the floor, a bare username in
the subject position is refused only by the corpus-based check (the validator
recognising it as a username it has seen marked pre-broker), which fails open
for a username the corpus has never seen. With the floor, the SHORT
substitutions are unrepresentable and the rest are validator-refused.

**Correction (review hardening, 2026-08-21).** This decision originally claimed
the substitution was "structurally impossible for the common case". That
over-states what a length floor can do, and the review's probes proved it: a
QUALIFIED username clears the floor without difficulty. `brett.heap.legacy` is
seventeen characters, admits no '@' and no whitespace, and is pattern-clean —
so `first.last` and `first.last.company`, which is how a large share of
directories spell usernames, walk straight through the structural guard. The
floor rules out `bheap`; it does not rule out a username.

The honest position is that the floor raises the cost of the substitution and
narrows it to spellings a reader is more likely to notice, and that the real
answer is a BROKER-ISSUED FORMAT the shape can require rather than a length
this shape can only hope means something. That is change task 4.4's business
(the gate-console binding, where the reference meets a real record): if the
issued format is regular — a prefix, a fixed width, a checksum — the floor
becomes a pattern and the substitution really does become unrepresentable.
Until then two validator rules carry it, and both are recorded as rules rather
than as structure: the pre-broker corpus check, and the mapping check added by
this hardening slice (a mapping resolving a username to itself, or to any
username the corpus records as pre-broker, is refused — `bare-username-as-persona`,
fixture `mapping-resolves-username-to-itself.yaml`).

**Accepted cost**: a broker that issued short opaque subjects would be
non-conformant on a field that is not really about length. The mitigation is
that the floor is stated in the schema description with this reasoning, so a
consumer meeting it can see why — and raising it to a real conflict would be a
one-line schema change with a recorded reason, not a rediscovery.

## Post-ratification dispositions (adversarial review, 2026-08-21)

An adversarial panel ran twenty-eight bypass probes against the ratified family
and the canonical validator. Fourteen findings were verified. Most were plain
bugs in checks that asked a slightly wrong question and are recorded in
`traceability.yaml` under `review_hardening`. **Three go further than bug
fixes**: they tighten the CONTRACT beyond what the ratified text spells out.
Each is recorded here rather than applied quietly, because a reader comparing
the ratified text with the shipped shape must be able to find the difference and
the argument for it. All three are architect rulings of 2026-08-21.

### Disposition 1 — a merge is not approved by one of its own parties (F5)

The ratified R4 says identities merge by a decision recorded as a
`governed_administration_approval`. It does NOT say "not by a party", and the
validator did not check it: probe P20 is a merge in which the surviving persona
is also the approving administrator, with every other obligation satisfied —
both parties named, both kept resolvable, an approval record referenced, a
timestamp. It passed.

**Ruled:** the refusal is the faithful reading, and the slice adopts it
(`merge-approved-by-a-party`, fixture
`merge-approved-by-one-of-its-own-parties.yaml`). A governed administration
approval given by the beneficiary is not a governed approval; it is the
paperwork of one. And a merge is the single act in this family that cannot be
undone from the audit record, so the argument for reading the requirement
strictly is strongest exactly here. The rule refuses an approver in `subjects`
or equal to `surviving_subject`, because both spellings are the same act.

**What could be said against it:** a one-person installation has nobody else to
approve with, and this makes a legitimate self-service merge unrepresentable
there. Accepted: the answer in that installation is that the merge is an
administrative act performed by the operator's own administrative persona, which
is a different subject from the persona being merged. If a real deployment
proves otherwise, the exception is a recorded change, not a rediscovery.

### Disposition 2 — `prior_shared_credential` is required (F11)

R7's retirement obligation was enforced only on records that VOLUNTEERED a
`replaced_credential` block. An adoption that named nothing was silently exempt
(probe P05), so the requirement bit on honesty and was inert against silence —
and the adoption most likely to leave a shared secret live is exactly the one
that never mentions it.

**Ruled:** `prior_shared_credential` is REQUIRED, `none | replaced`. This
realizes R7's retirement obligation STRUCTURALLY instead of conditionally:
`replaced` requires the block and the validator then requires the retirement and
its date; `none` is an AUDITABLE CLAIM — something a reader can later show to
have been false, which an omission never is. Two words, and the obligation stops
being satisfiable by leaving a field out. `none` additionally forbids the block,
so the claim and the record cannot disagree.

### Disposition 3 — `restriction_ref` is required for both answers (F12)

`co_residence_restriction: population_restricted` had to name the commitment it
consulted. `none` needed nothing — so the co-residence question could be
answered without anybody having asked it, `none` being what the field says by
default. Probe P16 is a clinical patient population on the shared instance
declaring `none` and referencing nothing; it passed.

**Ruled:** `restriction_ref` is required for BOTH values — the commitment that
imposes a restriction, or the WRITTEN FINDING that there is none. This applies
the OQ-5 co-residence finding's own rule to its own output: an unrecorded
restriction is indistinguishable from an unasked question, and so is an
unrecorded negative. The negative is also the finding most worth being able to
re-read, because it is the one revisited when the population changes.

### Also ruled: the decision-point locator walk, and its residue (F8)

`resolved_authorization.resolves_in` is a closed enumeration with one legal
value, and the refs beside it are 300 characters of free text. Probe P07
declares `governed_layer` and names the broker's own Keycloak admin API — the
organization's member collection — as the decision point. Every declaration in
the record is conformant; the decision is still "whoever is in the group may
act".

**Ruled:** the locator is walked BY SHAPE, using rule (e)'s technique on a
different class of value — broker-administration URI schemes, broker
administration paths, and a scheme-less ref whose first segment is the record's
own broker instance. Reported as `membership-as-authority`, because it is the
same invariant one field to the left.

**Two limits, recorded rather than implied.** First, a ref that merely CONTAINS
the instance id is deliberately not refused: the gate-console positive's
governed decision point is
`hermes://broker-opensoft-shared/authorization/gate-console`, where the instance
id is a legitimate scoping token on a governed-layer endpoint. Containment
cannot discriminate the two, so keying on it would have turned a ratified
positive red while proving nothing. Second — and this is the residue —
**an OPAQUE ref cannot be caught at all.** An internal id, a shortened URL or a
name meaningless outside one team, which in fact resolves to broker membership,
passes this walk completely. Like rule (e), it is a blocklist over the classes
it knows: it catches the honest mistake and the lazy shortcut, not a determined
one. Listed in the family README's limits section.

## Convention findings

- **Family layout** follows the `contracts/openxwallet/` shape:
  `contracts/identity-brokering/` holding `*.schema.yaml`, a `README.md`
  carrying a `Status:` header, and `examples/` with `examples/negative/`.
- **Schemas** are JSON Schema Draft 2020-12 written in YAML, each carrying
  `schema_version: 1`, a `kind:` (the family's schema kind) and a `name:` (the
  record kind), `$schema`, an absolute `$id` under
  `https://xforge.us/schemas/openxfactory/identity-brokering/v1/`,
  `contract_id`, and `contract_schema_version: 1`.
- **The validator** is standalone (no shared helper module), resolves its root
  as `Path(__file__).resolve().parents[1]`, collects findings through a
  `Findings` class emitting `ERROR [kebab-code] message`, runs a self-test layer
  over the packaged corpus plus an optional repo-scan layer, and exits 0 clean /
  1 findings / 2 harness error.
- **Dependency finding — `jsonschema` is the repository bar, not an extra.**
  Every canonical validator in this repository (`validate-openxwallet.py`,
  `validate-client-identity-roster.py`, `validate-credential-contracts.py`,
  `validate-worker-enrollment.py`, `validate-consent-instruments.py`) validates
  with `Draft202012Validator` plus a `FormatChecker`, and the dependency is
  pinned in `requirements/hermes-runtime-contracts.in`. A hand-rolled schema
  checker here would have been a second, weaker implementation of a bar the
  repository already meets uniformly — and `additionalProperties: false` at
  depth, conditional `if`/`then` requirements, `const` and `format` are exactly
  what a stock validator gets right and a hand-rolled one gets subtly wrong.
  The import is guarded and exits 2 with an install pointer, as its siblings do.
- **Negative fixtures** use the dominant repo dialect: `# expected_failure:`
  with an optional `# expected_failure_detail:` pin, plus a required
  `# requirement:` attribution and closed coverage checking in both directions.
  The detail pin matters more here than in most families because many fixtures
  also fail schema validation, and a generic `schema` finding would satisfy an
  unpinned probe while testing nothing.
- **The repo-scan layer indexes the SCANNED repository's own records** and
  excludes any vendored packaged corpus by path shape (`examples` +
  `identity-brokering`), not by this checkout's absolute paths — the failure
  `validate-openxwallet.py` recorded when domain repos began scanning vendored
  copies.

## Finding — the active support manifest is `supporting-docs/manifest.yaml`

Change task 3.2 asks for `supporting-docs.manifest.yaml`. The repository's
promotion tooling and the ratified `document-lifecycle` spine name the ACTIVE
change's manifest `openspec/changes/<change>/supporting-docs/manifest.yaml`
("Each active support folder owns `manifest.yaml`"), and reserve
`supporting-docs.manifest.yaml` for the ARCHIVED form written beside the
compressed bundle at archive time (`proposal-support.py archive`).

The promotion was therefore executed with the canonical tool —
`python3 scripts/proposal-support.py . transition add-identity-brokering
ideation/staging/identity-brokering-plane --apply` — which writes exactly the
fields task 3.2 enumerates (original staging path as `origin_path`, source
revision, transition date, per-file `sha256`, and the repeated
`origin.kind`/`origin.id`/`origin.path`, verified against `.openspec.yaml` and
refusing to proceed on any disagreement), moves the file with its history, adds
a byte-identical `source-snapshots/` copy, sets the promoted prose to
`Status: draft` naming this change, and removes the emptied staging folder.

Writing a second manifest under the archived filename would have created two
statements of the same facts in one change directory — the drift this feature
refuses everywhere else — and `proposal-support.py verify` reads only the
canonical one. The archived filename appears when the change archives, from
this manifest.
