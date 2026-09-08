# Research: Trust-anchor neutral contracts

**Feature**: `009-trust-anchor-contracts`
**Governing change**: `add-trust-anchor` (ratified 2026-08-21, Brett Heap)

This file records the two settlements the ratified change requires BEFORE the
schema is authored (change tasks §4.1 and §4.2), the compatibility check the
ruling named, the settlements this feature made beyond them, and the convention
and dependency findings the implementation rests on.

Both §4 items are SETTLED, not open. The ratification ruled OQ1 and OQ2 as
recommended; what follows records the rulings as settled and works out what they
mean in the shape, which is the part that was left to this feature.

## Settlement 1 — the closed chain-custody enumeration (change tasks 4.1, OQ2)

### What the ratification fixed

> **OQ2** — the custody enumeration is CLOSED with `evidences` derived, and
> operator escrow is modelled as a relationship on the credential record rather
> than a custody tier, settled with the `client-credential-escrow-registry` topic
> in the room.

Two rulings, then: closed with derived `evidences`, and escrow is not a member.

### The lesson being carried

The `openxwallet` handoff states it exactly: a set that fails to distinguish a key
readable by its own host from one isolated from it lets the first claim the
second's authority — and it would all validate cleanly. The last clause is the
part that matters. The failure is not that someone writes down something false; it
is that the false thing passes every check, so nothing ever surfaces it.

### The members, and what each evidences

Three members, two declared booleans, `evidences` DERIVED and enforced:

| id | key readable by the using host | per-use authorization outside that host | evidences | assurance ceiling | openxWallet counterpart |
|---|---|---|---|---|---|
| `host_held` | yes | no | `using_host` | `host_attributed_act` | `holder_readable` |
| `host_isolated_invocable` | no | no | `using_host` | `host_attributed_act` | `isolated_invocable` |
| `host_isolated_per_use_authorized` | no | yes | `named_holder` | `holder_attributed_act` | `isolated_per_use_authorized` |

```
evidences = named_holder  iff  (not key_readable_by_using_host)
                               and use_requires_authorization_outside_using_host
            using_host    otherwise
```

The assurance ladder the ceilings point at is ordered and closed:
`channel_authentication` (0) — authenticate a channel, nothing attributed;
`host_attributed_act` (1) — an act attributed to the using host, reviewed before
effect; `holder_attributed_act` (2) — an act attributed to the named holder, with
nothing else in the way.

### Why the SUBJECT of the two questions changed and the questions did not

openxWallet asks about the holder's own EXECUTION CONTEXT. A certificate is asked
about with respect to the USING HOST — the host presenting it. That is the same
question about the same hazard: a key the thing presenting it can read cannot
evidence who decided to present it. Renaming the subject and keeping the
discriminators is what lets the two sets map one-to-one instead of diverging into
two custody models, which the ratified text explicitly forbids ("composing with
`openxwallet`'s ratified rule … instead of restating a second custody model").

So the composition is made structural rather than asserted: every member declares
its `openxwallet_custody_model`, and the canonical validator RESOLVES that against
`contracts/openxwallet/openxwallet-custody.registry.yaml` AT RUN TIME and refuses
a member whose booleans or derived evidences disagree with the member it claims to
be. This is the same move `validate-openxwallet.py` makes when it reads the
approval-scope vocabulary out of the canonical job envelope instead of restating
it: a mapping nobody checks is how the second model arrives anyway.

### Why three members and not two

Same reading as `openxwallet`'s, one level down. "Only custody isolating the key
from that host evidences that the HOLDER acted" is a NECESSARY condition, not a
sufficient one; isolation is required for a holder claim and does not by itself
earn one. A two-member set (`readable` / `isolated`) would satisfy the ratified
wording while lumping a hardware-resident key the host can use at will together
with a key requiring a per-use authorization that host cannot supply — and the
first would then carry the second's authority.

That case is not hypothetical here. The live canary contains BOTH: a
per-use-attested broker certificate and non-exportable device keys usable at will.
A two-member set would have made those two indistinguishable, and the natural
label for the collapsed member would have been "hardware-backed" — which is why
`asserted_hardware_backing` is recorded as a deliberate NON-member. Where the key
physically lives is a fact about blast radius and belongs in `notes`.

### Why `host_held` reaches `host_attributed_act` rather than stopping below it

Capping software custody at channel authentication would make the contract
unusable for the service certificates both realizations actually run, and
`host_held` is also the FLOOR an undeclared certificate resolves to — so the
weakest member has to be one a real deployment can live inside. Review before
effect is the compensating control at that level; only the top level, where
nothing stands between the certificate and the effect, requires evidence that the
holder acted.

### The four enforced invariants

- **`custody-evidences-derivation`** — the derivation above, recomputed rather
  than trusted.
- **`custody-ceiling-unearned`** — the HIGHEST-ranked level a registry declares
  requires `evidences: named_holder`. Keyed on RANK, not on a level's name: the
  equivalent openxWallet rule was originally keyed on the literal id and was
  defeated by a registry that renamed its top tier. A probe attacks exactly that.
- **`custody-collapse`** — every member evidencing only the using host must rank
  STRICTLY BELOW every member evidencing the named holder. Keyed on what a member
  EVIDENCES rather than on readability, because readability is only one route to
  evidencing the host and keying on it leaves the middle member in neither list.
- **`custody-discriminator-duplicated`** — NEW here, and it is how the escrow
  ruling becomes structural. See below.

### Escrow: why a fourth member is refused, and how that stays compatible with the escrow topic

`ideation/staging/client-credential-escrow-registry/` (staged 2026-07-19) defines
a per-client, SOPS-encrypted credential escrow registry held OPERATOR-side, with
exactly one break-glass key, and makes escrow an explicit obligation of managed
installs. Its claim 1 is the load-bearing one for this settlement:

> **Escrow is a distinct layer, not a second runtime source.** The registry is
> written when a secret is created or rotated and read ONLY at break-glass.

That is precisely why escrow cannot be a custody tier. Custody answers a question
asked AT POINT OF USE — can the host presenting this certificate read the key? —
and escrow answers a question asked at creation and at disaster recovery: who else
can obtain a recoverable copy? An isolated key with an escrow copy is not the same
object as a host-readable key, and one axis carrying both facts makes both
unreadable.

The compatibility is therefore structural, not diplomatic. The escrow topic's
registry entries mirror `vaultref://` strings one-to-one on the CREDENTIAL record,
and every custody block in this family already references a
`credential-contracts` record and its vault binding. So when that topic lands, the
escrow relationship attaches to the object this family already points at, with no
change to any schema here and no change to what any certificate evidences. The
escrow topic's own open question 5 (what must be escrowed) and question 1 (whether
the delta is a MODIFIED `credential-contracts`) are untouched by this feature —
deliberately, because deciding them here would be deciding them in the wrong
place.

**The structural guard.** `evidences` derives from exactly two booleans, so a
member declaring the SAME pair as an existing member differs only in something
this axis cannot express. That is either a second axis smuggled in or a rename,
and both are refused. What makes this the right check rather than a denylist on
the word "escrow": an escrow member has no choice but to duplicate a pair, since
the escrow fact is invisible to both discriminators. The probe
`custody-registry-escrow-as-a-custody-tier.yaml` records that — its member is
internally impeccable and still refused.

### Settlement beyond the ratified text: the set is a REGISTRY document

The ratified text requires custody "from a defined set" whose members state what
they evidence, with `evidences` derived. That cannot be an inline enum: the set
would be duplicated in the anchor and certificate schemas, and the derivation —
which is a rule OVER members — would have nowhere to live. So the family carries
`chain-custody-registry.schema.yaml` plus the closed instance
`trust-anchor-chain-custody.registry.yaml`, mirroring the ratified
`openxwallet-custody-registry` pair exactly. Recorded here as a settlement rather
than left as an inference: it is two files the change's task list does not name
individually, and it is the mechanism the ratification pointed at.

### Settlement beyond the ratified text: the undeclared-custody FLOOR is declared

The ratified scenario says an undeclared certificate "evidences the weakest member
of the defined set" and "may not hold authority above that member". Rather than
inferring the weakest member, the registry declares it
(`undeclared_custody_resolves_to`) and the validator checks the declaration is
honest: the named member must evidence the using host, have its key readable by
the using host, and sit at the minimum ceiling any MEMBER reaches. Keyed on the
weakest member rather than the ladder's lowest level, because a ladder may declare
a level no member caps at — `channel_authentication` is one — and keying on the
ladder would demand a member nothing declares. Without the check, moving the floor
up would invert the rule and make declaring nothing the way to obtain the
strongest assurance.

## Settlement 2 — the issuance-evidence floor (change tasks 4.2, OQ1)

### What the ratification fixed

> **OQ1** — issuance evidence remains an obligation on what the record must
> *establish*, with the declared floor (per-certificate record where the authority
> exposes it; per-policy attestation plus the authority's own log where it does
> not) fixed before schema authoring, refusing the weaker-form-in-requirement
> middle option.

### The floor in the shape

`establishment_level` has exactly two members and nothing weaker is
representable:

- `per_certificate_record` — REQUIRES `request_provenance.establishment:
  established`, and with it the requester, the request identity and the request
  time.
- `per_policy_attestation_with_authority_log` — REQUIRES both halves
  (`policy_attestation_ref` AND `authority_log_ref`; "plus" is a conjunction) and
  forces `establishment: not_established`, which in turn FORBIDS the requester,
  request id and request time by shape and requires a `declared_shortfall_ref`.

The mapping between level and provenance is one-to-one on purpose. If an authority
exposes per-certificate provenance, the strict level is the honest one, and
declaring the floor while filling in the strict fields is refused twice — by the
shape, and by a rule that names why (an asserted-but-unestablished record is worse
than a declared gap).

**What the ruling actually refused, restated correctly.** An earlier draft of this
section described the refused middle option as "declaring the floor while filling
in the strict fields". That is a different hazard — a real one, and the one the
shape closes — but it is not OQ1's. The ruling reads:

> Reject the tempting middle option of writing the weaker form INTO THE
> REQUIREMENT ITSELF: that would let the self-hosted authority, which can do
> better, stop at the floor.

So the refused option was making the weaker form the OBLIGATION, and the hazard it
carries is a family-operated authority stopping at the floor because the
requirement lets it. That hazard is not closed by the shape at all — the floor is
representable, and it has to be, for the authority the family does not run. It is
closed by a rule: an issuance record declaring the floor while recording
`issuing_authority.operated_by_family: true` is refused. Until the review of
2026-08-21 that field was required by the schema and read by nothing, so the
ruling was realized as prose describing a shape that did not implement it — the
drift this correction records rather than quietly fixes.

### Why the fields are forbidden rather than optional

"Records only what it can establish" is a shape obligation, not a habit. Optional
fields at the floor level would be filled in from a change ticket that happened to
be open, which is not the authority establishing anything — and a reader cannot
tell a reconstructed requester from an established one. The probe
`issuance-asserting-provenance-at-the-floor-level.yaml` is that record.

### The conformance declaration carries the difference

Per the ruling, the declaration states which form the realization achieves:
`achieved_establishment_level` is REQUIRED on the TA-R2 entry wherever it is
satisfied or partial. So a consumer reads the achieved level where it reads
everything else about the realization, rather than inferring it from a sample of
issuance records.

And the records are held to it. A record asserting `per_certificate_record` while
the declaration claims only the floor is refused
(`issuance-level-above-the-declared-achievement`), because otherwise the field is
a decoration: a consumer reads the floor, the records read stricter, and "the gap
is not closed by the realization asserting the evidence instead" has nothing
enforcing it. This too was a required-but-unread field before the 2026-08-21
review.

### Settlement beyond the ratified text: obligation entries need an address

The ratified guards on the degraded-obligation rule ("a declared gap is NOT
permission to assert the missing evidence"; "declaring a gap afterwards does not
validate the claims made while it was silent") are only enforceable if a record
can NAME the entry it relies on and the entry can be resolved. So each obligation
entry carries an `entry_id` and its own `declared_at`, and three rules run over the
citation: the entry must belong to the same realization, must declare the
obligation the citation claims, must record `partial` or `cannot` rather than
`satisfied`, and must not be dated after the record citing it. Without per-entry
dates a late declaration is indistinguishable from a timely one, and the ratified
guard would have nothing to bite on.

### Settlement beyond the ratified text: the anchor-custody pairing is CONDITIONED

The custody block on an anchor admits exactly two shapes — the credential record
WITH its vault binding, or the obligation entry where the realization declared
that neither can be produced. The justification for the second shape is specific
and it is worth stating as the condition it is, because the earlier wording stated
it as a general permission:

> An anchor for an authority the family does not operate has no credential record
> for its key, and requiring one unconditionally would have made the live
> realization non-conformant for a reason unrelated to trust.

The second shape is therefore for the UN-OPERATED case. Where the realization
declares `authority_operated_by_family: true`, nothing stands between it and a
credential record with a vault binding, so there is no shortfall to declare and
the shape is being used as an exemption. The validator now refuses that, at both
places the claim appears: on the declaration (a family-operated realization
recording TA-R7 as `partial` or `cannot`) and at the citation (an anchor naming
such an entry). Before the 2026-08-21 review the field was required and unread,
and a self-hosted realization could excuse its own readable root key by declaring
that it could not do better.

### Settlement beyond the ratified text: a readable anchor key caps what is beneath it

The ratified derivation is record-local: what a certificate evidences comes from
ITS declared custody. That leaves a chain whose ROOT key is a readable file with a
leaf that reads `named_holder` at the top of the ladder — every record-local rule
passes, and anything with read access to the authority's host could have obtained
the same certificate for the same subject. So a certificate (and a subordinate
anchor) may not carry a ceiling above the ceiling of any anchor in its chain whose
key is readable by the using host.

**Why keyed on readability rather than on rank alone.** The unconditioned form —
a certificate may never exceed the weakest anchor ceiling in its chain — is a
simpler invariant and was considered. It was not adopted, and the reason is the
same D6 hazard the pairing above turns on: every anchor of an authority the family
does not operate sits below the strictest tier BY DECLARATION, so the
unconditioned rule would make a declared R7 shortfall a bar to any
holder-attributed certificate anywhere beneath it — a live realization
non-conformant for a reason it already declared honestly, and a ruling for the
ratifier rather than for a hardening pass. Readability is the case where the bound
genuinely disappears: a readable key can be copied off the host and used anywhere,
by anyone who ever had read access, indefinitely, where an isolated key confines
minting to a compromised host while it is compromised.

### The `key_change` premise, verified

The renewal schema binds `rebind_obligation.arises` to `key_change.changed` and,
where `changed` is false, FORBIDS the generation references and forces the rebind
list empty. That implication is sound and it inherited an unverified premise:
`changed` was a self-assertion, and every rule downstream is guarded on the
obligation arising, so a renewal that did change the key could declare that it did
not and owe nothing. The certificate record is the witness — it carries
`supersedes_generation_ref` — so a supersession NO renewal record accounts for is
now refused, from the renewal's side and from the certificate's. The escape is
deliberate and load-bearing: a certificate whose current generation supersedes an
earlier one may be renewed again with the key preserved, so the rule asks whether
ANY renewal owns the supersession rather than refusing `changed: false` outright.

## Design decision carried into the shape: what is unrepresentable rather than checked

The change's design leans on structure repeatedly ("structural, not prose").
Where a guarantee could be expressed in the shape, it is — because a schema
constraint cannot be neutered by editing a validator, and a record that cannot be
authored is stronger than one that is authored and then refused:

| Guarantee | How |
|---|---|
| A certificate accepted on its own strength | `trust_evaluation.basis` is a constant; the refusal vocabulary has no member for well-formedness |
| Trust from issuance-time validity | `revocation_standing_check.basis` is a constant `checked_at_use`, and `outcome: trusted` forces the check performed and active |
| A renewal "successful" with a recorded-but-unevidenced dependent | `completion_state: complete` forces every rebind entry to carry succeeded evidence (schema `if/then`) |
| A renewal blamed on the dependent | `failure.attribution` is a constant naming the issuing workflow |
| A key-preserving renewal with rebind evidence | `arises: false` forces the rebind list empty |
| A renewal proceeding against a known-incomplete enumeration | `known_incomplete` forces the planning outcome to `refused` |
| An absent issuance record read as approval | `question_answered_as` and `disposition` are constants |
| An unevidenced revocation window closed administratively | `escalated_as` is a constant `open_exposure`; `complete` forces every authority propagated |
| A credential held in a workflow's own storage | `brokered_into_ephemeral_scope` is `const: true`, not a boolean |
| A second revocation vocabulary | `mechanism.realized_through` is a constant naming openxWallet's rule |
| A root anchor with a parent, or a subordinate without one | `chain_position` `if/then` on `role` |

The validator then closes what a shape cannot see: everything cross-record, every
derivation, and every set comparison.

## Convention findings

- **Family layout** follows `contracts/openxwallet/`: `contracts/trust-anchor/`
  holding `*.schema.yaml` plus the closed registry instance, a `README.md`
  carrying a `Status:` header, and `examples/` with `examples/negative/`.
- **Schemas** are JSON Schema Draft 2020-12 written in YAML, each carrying
  `schema_version: 1`, a `kind:`/`name:` line, `$schema`, an absolute `$id` under
  `https://xforge.us/schemas/openxfactory/trust-anchor/v1/`, `contract_id`, and
  `contract_schema_version: 1`. Every object closes `additionalProperties` at
  every depth.
- **The validator** is standalone (no shared helper module), resolves its root as
  `Path(__file__).resolve().parents[1]`, collects findings through a `Findings`
  class emitting `ERROR [kebab-code] message`, runs a self-test layer plus an
  optional repo-scan layer, and exits 0 clean / 1 findings / 2 harness error. Only
  the standard library plus `pyyaml` and `jsonschema` (with `rfc3339-validator`
  for `format: date-time`) — all already pinned in
  `requirements/hermes-runtime-contracts.in`. No new dependency.
- **Negative fixtures** use the dominant repo dialect: a first-line
  `# expected_failure: <code>` header with an optional
  `# expected_failure_detail: <substring>` pin, plus `# requirement: <REQ-ID>`
  for coverage closure in both directions.
- **The detail pin matters more in this family than in most**, because so many
  guarantees are expressed in the shape: `schema` is satisfied by any schema error
  whatsoever, so a probe pinned only to it can be mutated into testing nothing
  while its self-test stays green. Exactly two fixtures pin `schema`
  (`renewal-attributing-failure-to-the-dependent.yaml`, where the guarantee IS the
  constant, and `dependent-binding-declaring-no-required-obligations.yaml`, where
  it is the required field), and each pins the message as its detail.
- **The repo-scan context is closed over the scanned repository** plus the
  canonical registries, never the packaged positives — the fail-open family of
  defects that openxWallet's adversarial review found (inert layer 2, vendored
  fixtures re-adjudicated as live records, empty-index guards) is designed out
  from the start rather than fixed later. Verified by scanning a scratch consumer
  corpus: a complete set validates clean, and a certificate alone fires both
  `trusted-without-held-anchor` and `issuance-evidence-unresolved`.

## Dependency finding — the openxWallet registry is read, not restated

`contracts/openxwallet/openxwallet-custody.registry.yaml` declares three custody
members with two booleans and a derived `evidences` of `environment` | `holder`.
The mapping this family enforces is:

- `key_readable_by_using_host` ↔ `key_readable_by_holder_execution_context`
- `use_requires_authorization_outside_using_host` ↔
  `use_requires_authorization_outside_holder_execution_context`
- `using_host` ↔ `environment`, `named_holder` ↔ `holder`

The validator refuses to run without that registry present (exit 2), because the
composition is not optional: without it there is no way to tell whether this set
is one model or two.

## What the validator cannot check, recorded rather than implied

It does not contact a certificate authority, parse a certificate, verify a
signature, check a revocation list, or confirm that a DECLARED custody model or a
DECLARED conformance state is the real one. Declaration is what keeps this contract
honest, and it works only if realizations declare truthfully. A false declaration
is a governance finding rather than a misconfiguration — the same disposition
`openxwallet` recorded for the same reason.
