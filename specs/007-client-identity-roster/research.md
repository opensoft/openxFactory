# Research: client identity roster neutral contracts and conformance wiring

**Feature**: `007-client-identity-roster`
**Governing change**: `add-client-identity-roster` (ratified 2026-08-14, Brett
Heap; AMENDED the same day, Decisions A and B)
**Rulings**: [clarify-rulings-2026-08-14.md](clarify-rulings-2026-08-14.md) —
authoritative over this file wherever they touch the same ground.
**Plan-gate rulings**:
[plan-gate-rulings-2026-08-14.md](plan-gate-rulings-2026-08-14.md) — the
architect's rulings on the cross-model adversarial review of this file and
plan.md at `913c3ca`, likewise authoritative. The decisions below carry their
amendments inline, marked with the ruling id: Decision 3 (A-3a, A-3b),
Decision 5 (A-5, A-6, A-7), Decision 6 (A-9), Decision 7 (A-11), Decision 8
(A-16). Ruling R-N1 is recorded first, immediately below, because it settles
an element of the uniqueness key that every other decision references.

This file records the decisions the ratified packet and the clarify rulings
left to the plan phase, the derivations behind them, and the convention and
tree findings the implementation rests on. Decisions the rulings already fixed
are NOT relitigated here; they are cited.

---

## Ruling R-N1 — the uniqueness key's third element is `authority_class_intended`

### Why a choice existed at all

The five-element key is ratified, but its third element is named
"authority class" in every ratified statement of it, while the roster ENTRY
carries two authority-class fields (`authority_class_intended` and
`authority_class_achieved`, FR-001). The key's element 3 therefore had to be
bound to one of them before `$defs.identity_key` could be written.

### The verification sweep (performed before encoding, per the ruling)

Every ratified mention of the key was read in full, hunting for any text
implying the ACHIEVED class participates in uniqueness:

| Source | Text |
|---|---|
| spec.md constraint 6 | "Uniqueness is keyed on (domain, admission surface, **authority class**, blast-radius unit, duty)" |
| spec.md FR-006 | "keyed on the tuple (owning domain, admission surface, **authority class**, blast-radius unit, duty)" |
| spec.md FR-035 | "`identity_ref` (the five-element uniqueness tuple that identifies the entry)" |
| spec.md Key Entities, "Roster entry" | "identified by the uniqueness tuple (domain, admission surface, **authority class**, blast-radius unit, duty)" |
| roster delta, requirement heading | "Identity uniqueness is keyed on surface, class, blast-radius unit and duty" |
| roster delta, requirement body | "keyed on the tuple (owning domain, admission surface, **authority class**, blast-radius unit, duty). Authority class SHALL be one of `observe` or `mutate`." |
| roster delta, "A genuine duplicate" scenario | "two entries share owning domain, admission surface, **authority class**, blast-radius unit and duty" |
| design.md Decision 2 | "Adopted: uniqueness on (domain, admission surface, **authority class**, blast-radius unit, duty)" |
| proposal.md item 2 | "**Uniqueness on (domain, surface, class, blast-radius unit, duty).** Classes are `observe` and `mutate`." |
| seed handoff, killed-flaw block | "Uniqueness is now **(domain, admission surface, authority class, blast-radius unit, duty)**; classes are **`observe\|mutate`** only." |

Two near-misses were read in context and are NOT counterexamples:

- `review/decision-review-2026-08-14.md` — "`authority_class_intended` vs
  `_achieved` derived from granted permissions" appears under *Non-blocking
  findings adopted* and concerns the FIELD PAIR's existence, not the key; and
  "Both are elements of the uniqueness tuple" appears under *Not adopted*,
  where "both" refers to the per-surface and per-blast-radius-unit AXES the
  reviewer had framed as exclusive — not to the two class fields.
- roster delta line 67 — "spanned admission surfaces or the achieved authority
  class" is the DECLARED-EXCESS rule (FR-009/FR-010), a rule about a stable
  identity, not about how it is keyed.

**Sweep result: CLEAN.** No ratified text implies the achieved class
participates in uniqueness. The choice is the plan's to make.

### The choice, and why

**Element 3 is `authority_class_intended`.**

A key must be DECLARATIVE and STABLE. `authority_class_intended` is a
declaration the owning domain makes, and only a deliberate record change moves
it. `authority_class_achieved` is OBSERVATIONAL: it is derived from
`granted_permissions[]` and therefore moves whenever provider state moves.

Keying on the observational field would mean an identity's IDENTITY changes at
the moment its permissions drift — which is incoherent, because drift is
exactly what FR-009 and FR-010 report ABOUT a stable identity, not what
re-keys it. It would also break the drift record's whole purpose: a drift
finding is raised precisely when observed authority departs from the recorded
authority, so an achieved-keyed `identity_ref` would name a tuple that no
longer matches the entry the finding is about — the join would fail exactly
when it was needed.

The intended-keyed reading also keeps FR-006 and FR-004 as the two distinct
rules they are. Two entries sharing all five elements are an FR-006 duplicate
even where their achieved classes differ; that achieved difference is its own
finding (FR-004: an achieved class the permissions contradict; FR-010:
achieved above intended, undeclared), never a licence to declare two entries
distinct.

### Consequence for the drift record

The drift finding's `identity_ref` OBJECT carries the same
`authority_class_intended` value as the entry it cites — the stable join key.
Observed values, including an observed authority class, ride `roster_value` /
`observed_value` like every other drifted field. A drift finding about an
authority-class change is therefore fully expressible without the key moving
underneath it. This is stated in the schema description of kind 2 so a reader
of the contract alone can see why the two `identity_ref` shapes differ and why
element 3 is the intended field.

---

## Decision 1 — the `identity_kind` closed set (FR-034, the plan's headline
open item)

### What constrains the answer

FR-034 is a derivation rule, not a vocabulary:

> `identity_kind`'s members MUST be taken VERBATIM from the ratified delta or
> OpenSpec task 2.1 where those enumerate them; they do NOT (task 2.1 names
> the field only), so its members MUST be exactly the kinds the four mandated
> example cases require, closed at that set for this release, and the builder
> MUST NOT invent an unratified kind vocabulary.

So the input set is: the four mandated example cases of FR-019, plus (per the
progress handoff) the vendor-homed negative of FR-016 if it forces a second
kind. Nothing else may contribute a member.

### The derivation, case by case

**Case 1 — the Business Central worked case.** Measured, not assumed: the
governing evidence is `tenants/farheap-bc-observer-identity-evidence-v1.yaml`
on OpsxFactory `origin/main`. Its `identity_evidence.entra` block records a
`tenant_guid` (the CLIENT's tenant, `96d3fa6b-…`), a `display_name`
(`opsx-farheap-bc-observer`), an `app_id`, an `object_id` (the application
registration object) and an `sp_id` (the service principal). Its
`business_central` block records an `environment` (`Sandbox1`), a
`user_security_id` / `user_name` (the BC **application user**), permission
sets, and `production_application_user: absent`.

The record therefore contains exactly ONE identity object — an Entra
application registration with its service principal, homed in the client
tenant — and TWO admission acts over it:

1. the per-environment BC application user in Sandbox1 (provider-enforced,
   scope = one environment, and demonstrably absent in Production), and
2. the admin-center Entra-app authorization with no scope selector
   (tenant-wide).

**Both acts belong to ONE admission surface, and the packet says so.** The
roster delta's scenario "One product name has two admission acts → each act is
its own admission surface" is not a licence to split Business Central into two
surfaces: packet task 2.2 binds both acts to the single `business_central`
member verbatim ("BC: the per-environment application user AND the admin-center
Entra-app authorization, which is the two-act worked case"), and ratified
answer 5 closes the first-release vocabulary at two members, so a split is
unrepresentable. The measured reason the two are not INDEPENDENT admission acts
in the delta's sense is the investigation that motivated this change: four
admin-consented permissions held for six days still returned `401` until the
admin-center act landed, so neither act admits alone — they are jointly
required keys to one surface. The delta's scenario governs acts that admit
independently, through separate administrative surfaces. Recorded here because
an implementer authoring the packaged case would otherwise have to resolve the
apparent conflict alone, and either split (unrepresentable, breaking SC-003) or
quietly drop the second act (the exact fiction FR-003 exists to refuse).

The BC application user is **admission, not identity**. This is settled by the
spec itself, which places both acts inside one entry's `admission[]` list
(FR-019 "a provider-enforced per-environment application user in Sandbox1 …
PLUS the admin-center Entra-app authorization"; acceptance scenario 3, "both
acts appear with their own achieved scopes and enforcement modes and the
effective reach is their union"). A record that made the application user a
second identity would need two entries sharing every element of the
uniqueness tuple — a duplicate finding under FR-006. The case therefore
contributes ONE kind: an Entra application registration with service
principal.

**Case 2 — the provider-forced multi-surface reader.** The reach is carried
by `granted_permissions[]` (application permissions and/or a directory role
assigned to a service principal). The object holding them is again an Entra
application registration. Contributes no new kind.

**Case 3 — the duty-separated pair.** The estate precedent is
LedgerxFactory's `ledgerx-farheap-bc-poster` / `-provisioner`. Both are Entra
application registrations differing in `duty`. Contributes no new kind.

**Case 4 — the `planned` entry.** An identity not yet created. Its kind is
declared as intent; the intent is an Entra application registration.
Contributes no new kind.

**The vendor-homed negative (FR-016).** This is the case the handoff flagged
as possibly forcing a second member. It does not, and the reason is
structural: FR-012 and design Decision 5 deliberately split residency into
FOUR separate declarations — `identity_kind`, `home_tenant`,
`principal_locations[]`, and `residency_model`. A vendor-homed registration
consented by many clients is the SAME object class as a client-resident one;
what differs is where the registration is homed and where its principals
land. Encoding vendor-homedness as a second `identity_kind` would create two
fields that can disagree about the same fact — precisely the failure design
Decision 5 rejected ("an implementer could declare client-residency for a
vendor-homed app and pass"). The negative fixture fails on
`home_tenant` ≠ client tenant while `residency_model` claims client-resident;
it needs no second kind, and giving it one would weaken the check.

### The derived set

```
identity_kind: [ entra_app_registration ]      # ONE member, closed for v1
```

`entra_app_registration` denotes the Entra application registration together
with the service principal(s) it instantiates. `home_tenant` says where the
registration lives; `principal_locations[]` says where the principals land;
`residency_model` says which governed model that combination is.

**Why a provider-named member is neutral enough.** The same contract already
carries a closed, provider-named vocabulary by ratification —
`admission_surface: [business_central, exchange]` (FR-007) — and the ratified
scope is Entra-homed surfaces with a named successor for non-Entra providers
(proposal, "Out of scope, deliberately"). A member named for the object class
the first-release surfaces actually admit is consistent with that, and it
keeps the extension route identical: a new kind arrives with the change that
governs the surface or provider that needs it.

**Why a one-member enum is the right outcome and not a smell.** A closed
one-member set is falsifiable (any other value is refused, naming the
extension route), forces the successor path rather than a free string, and is
exactly what FR-034's derivation rule produces. Widening it now would be the
invention FR-034 forbids.

### Alternatives considered and rejected

- **Two members splitting registration from principal**
  (`entra_app_registration` / `entra_service_principal`). Rejected: no
  mandated case needs an entry whose subject is a principal with no
  registration in the roster's scope, and the split would duplicate the
  `home_tenant`/`principal_locations[]` pair as a kind, re-opening design
  Decision 5's ambiguity.
- **Members encoding residency** (`client_resident_app` /
  `vendor_multi_tenant_app`). Rejected for the same reason, more sharply: it
  makes `identity_kind` and `residency_model` two spellings of one fact.
- **Members for managed identity, workload-identity federation, or a service
  user account.** Rejected: no mandated case requires them, and FR-034
  forbids inventing an unratified vocabulary. They enter with the change that
  governs the surface that needs them.
- **Leaving `identity_kind` an open pattern-bound token like
  `blast_radius_unit`.** Rejected: FR-034 lists `identity_kind` among the
  CLOSED sets explicitly.

**Verdict: not ambiguous.** The four mandated cases and the vendor-homed
negative converge on one object class, and every candidate second member
either duplicates another declared field or has no mandated case behind it.
No `[ARCHITECT RULING NEEDED]` block is raised for the SET. The member's
SPELLING is a naming choice and is listed among the plan's reviewable
decisions.

---

## Decision 2 — where the drift-finding record lives (FR-035)

FR-035 leaves the home to implementation but binds the consequences: either
way it registers under FR-021 (manifest row with sha256 and consumption rule,
CHANGELOG entry, same `contract-v1.32` bundle) and carries at least one
packaged example and one negative.

**Chosen: a SECOND `kind` inside
`contracts/schemas/xfactory-client-identity-roster.schema.yaml`**, expressed
as a top-level `oneOf` over `xfactory_client_identity_roster` and
`xfactory_client_identity_drift_finding`.

### Why

1. **Sibling-family precedent, in the same directory.**
   `contracts/schemas/xfactory-credential-contracts.schema.yaml` owns FIVE
   record kinds in one file behind a top-level `oneOf` with per-branch
   `required` lists. That is the established shape for "one contract family,
   several record kinds" in `contracts/schemas/`, and this family is exactly
   that: a roster fragment and the drift record that cites it.
2. **It keeps FR-021's singular language literally true.** FR-021 says "The
   new schema MUST be registered in `contracts/manifest.yaml` with `path`,
   `source_path`, … and a `consumption_rule`". One file is one row, one
   `sha256`, one consumption rule, one CHANGELOG line at `contract-v1.32`.
   The reconciliation the progress handoff asked for is therefore not a
   strained reading — the singular is preserved by construction, and no
   sentence of FR-021 needs to be read distributively.
   **Consequence, ruling A-2: BOTH kinds declare `schema_version: const: 1`.**
   The manifest row's `schema_version` mirrors the RECORD envelope's const
   (see "A registration gap FR-021 assumes away" below for that distinction),
   and a single row can mirror only one value. Two kinds sharing a file, a
   digest and a consumption rule must therefore share an envelope version; a
   later divergence between them is a signal the two kinds have outgrown one
   file, not a thing to paper over in the row.
3. **The tuple cannot drift from its definition.** The drift record's
   `identity_ref` IS the five-element uniqueness tuple of FR-006. In one file
   the tuple is defined once and referenced by both kinds through `$defs`; in
   two files it is two definitions behind two digests that a consumer can pin
   independently and at different versions.
4. **The consumption rule is one statement.** The declared placement
   (FR-020) attaches to the roster kind only — a drift record has no domain
   placement in this release, because no producer exists (FR-035, SC-008).
   One consumption rule can say both things once; two rows would have to say
   "and the other kind's placement is elsewhere" twice.

### The counter-case, and why it loses

`consent-instrument` splits across three schema files
(`consent-instrument`, `consent-instrument-class-registry`,
`consent-purpose-model`). That precedent does not transfer: those three are
independently consumable records with independent lifecycles and separate
manifest rows, authored by different parties (a domain owns its class
registry). The roster fragment and its drift record are produced and consumed
by the same lane; separating them buys independent versioning nobody needs
and costs the tuple's single definition.

### Consequence recorded

The whole-repo kind sweep of FR-036 targets `kind:
xfactory_client_identity_roster` ONLY. The drift kind carries no placement
rule in this release and is therefore not swept; its conformance is proven by
the packaged example and negatives. When a producer lands (a named domain
follow-up), its placement enters with that change.

---

## Decision 3 — the `issuance_preconditions` shape (FR-028) — a live-breakage
finding

### What the tree actually holds

The amendment record states that `issuance_preconditions` "is a domain-local
extra key in OpsxFactory's `credentials/requirements.yaml`, riding a neutral
schema that neither declares nor forbids extra keys". Measured, the key's
SHAPE matters and it is not a list of tokens:

`xFactories/OpsxFactory/credentials/requirements.yaml` (lines 232-234 and
263-265, on `aks_workload_administration` and `deployment_operator`):

```yaml
    issuance_preconditions:
      accepted_request_required: true
      registered_active_subject: true
```

It is an OBJECT — a map of precondition token to boolean. The same shape
appears on the workflow record at
`xFactories/OpsxFactory/workflows/deployment.yaml:75` (with a third, STRING
member `subject_registry`), enforced by that domain's own
`scripts/validate-domain-factory.py:953-956`.

Confirmed independently: `contracts/schemas/xfactory-credential-contracts.schema.yaml`
declares `additionalProperties` exactly once (line 98, inside an unrelated
branch); the `xfactory_credential_requirements` requirement item does NOT
close it, which is why the extra key rides today.

### The collision

If the neutral schema declares `issuance_preconditions` as an ARRAY of closed
tokens, OpsxFactory's existing, currently-conformant records become invalid
against the pinned neutral schema at the next
`scripts/validate-credential-contracts.py <domain-repo>` run. That is not a
hypothetical: it is the canonical validator for a promoted capability, and
this feature is simultaneously making a sibling check BLOCKING in the same
pack.

That outcome is forbidden three times over:

- **FR-030**: "no domain repository file MUST be edited by this feature" —
  and it would force exactly such an edit.
- **FR-028**: "this feature MUST NOT edit the domain-local instance on
  OpsxFactory's `deployment_operator` / `aks_workload_administration`, whose
  extra-key precedent this vocabulary **regularizes rather than replaces in
  place**."
- **`docs/contract-versioning-policy.md:130-132`**, the tree's own definition
  of the change class this bundle claims: "**Additive (minor)** — new
  optional fields, new contracts, new validator warnings. **Domain repos on
  the same major version remain conformant without changes.**" A shape that
  invalidates a conformant domain record is not additive-minor, and
  `contract-v1.32` is a minor bump.

### The resolution

Declare `issuance_preconditions` on the `xfactory_credential_requirements`
requirement item as an OBJECT whose PROPERTY NAMES are the closed vocabulary
and whose values are `const: true` (ruling A-3a, argued below — the pre-gate
draft said `type: boolean` here and the narrowing is the ruling's, not a
restatement):

```yaml
issuance_preconditions:
  type: object
  minProperties: 1
  additionalProperties: false
  properties:
    roster_drift_clear_required:
      const: true
      description: >-
        Grant issuance is refused while an open
        xfactory_client_identity_drift_finding covers the roster entry for the
        identity this requirement names (add-client-identity-roster).
    accepted_request_required:
      const: true
      description: >-
        Grant issuance requires an accepted deployment request
        (adopt-deployment-handoff-boundary).
    registered_active_subject:
      const: true
      description: >-
        Grant issuance requires a registered, active subject
        (adopt-deployment-handoff-boundary).
```

Two amendments the plan gate made to this shape:

**Values are `const: true`, not `type: boolean` (ruling A-3a).** A precondition
is a REQUIREMENT that is either declared or not declared. `false` is not a
second meaning — it is a declaration that reads as governance while asserting
nothing, precisely the false-comfort shape a closed vocabulary exists to
refuse. Both live OpsxFactory records declare `true`, so the narrowing breaks
no existing record and the additive-minor claim of the section above is
untouched.

**Each member carries a one-line schema `description` naming its governed
condition, and the two precedent members cite `adopt-deployment-handoff-boundary`
(ruling A-3b).** This is what makes "regularizes rather than replaces in place"
legible in the artifact itself rather than only in this file: a reader of the
schema can see that two of the three members are admitted because they are
already governed elsewhere, and that only the roster-drift member is minted
here.

(The enumeration is written as explicit `properties` with
`additionalProperties: false` rather than `propertyNames.enum`, because
per-member `description` and `const` have nowhere to live under
`propertyNames`. The refusal semantics are identical; the naming of the
vocabulary in the refusal message is Decision 4's `_semantic_findings` branch
either way.)

The closed set has three members, and each is derived rather than invented:

- `roster_drift_clear_required` — the ratified roster-drift member (Decision
  B, FR-028, the credential-contracts delta). Its meaning: a grant naming
  this identity is refused while an `open` drift finding covers the roster
  entry.
- `accepted_request_required`, `registered_active_subject` — the two tokens
  the precedent this vocabulary is chartered to REGULARIZE already declares,
  ratified in their own domain lane by `adopt-deployment-handoff-boundary`.

Reading "regularize rather than replace in place" as "admit what the
precedent declares, without touching the file" is what makes the sentence
operative; a one-member closed set would replace the precedent by
invalidating it, which is the reading the sentence rules out.

"Its first member is the roster-drift precondition" (the delta) is honoured
by ordering: the roster-drift token is the vocabulary's first member and the
only one this change ratifies as neutral meaning; the other two are admitted
because they already exist and are already governed elsewhere.

### Scope fence

The neutral property is declared on the CREDENTIAL REQUIREMENT record only.
The workflow-record occurrence at `workflows/deployment.yaml:75` is a
different record kind, owned by the domain's own validator, and is NOT
governed by this vocabulary. The plan says so explicitly so a later reader
does not extend the neutral vocabulary onto a record it never claimed.

### Rejected alternatives

- **Array of tokens.** Cleanest expression; breaks a live domain gate. See
  above.
- **Single-member closed set.** Same breakage, and it makes the word
  "regularizes" inoperative.
- **Leave the object open (`additionalProperties: true`).** Fails FR-028's
  "A member outside the closed vocabulary MUST be refused" and SC-008's
  negative.
- **A different property name to avoid the collision.** Forbidden: the delta
  and FR-028 name `issuance_preconditions` verbatim, and a second parallel
  mechanism is explicitly ruled out ("never a second parallel one").

---

## Decision 4 — how the closed vocabulary NAMES itself in a refusal (FR-028,
SC-008)

`propertyNames.enum` refuses an out-of-vocabulary member, but the
`jsonschema` message for a `propertyNames` failure does not name the allowed
set, and SC-008 requires the refusal to name the closed vocabulary.

`scripts/validate-credential-contracts.py` already carries the idiom for
exactly this: `_semantic_findings(doc)` returns `code: message` strings for
invariants "the shape schema cannot express", and each packaged negative is
registered in `NEGATIVE_EXPECTATIONS` keyed by filename to the code it must
raise.

Decision: the schema constrains the shape; a new `_semantic_findings` branch
emits `issuance-precondition-unknown: requirement <id> declares
<token>, which is not a member of the closed issuance_preconditions
vocabulary (allowed: [...])`. Both fire on the negative; the semantic one is
what names the vocabulary.

**The branch fires on BOTH failure shapes — an out-of-vocabulary member AND a
false-valued member — and the semantic mirror is STRUCTURALLY REQUIRED, not a
presentation nicety (ruling A-3a).** The reason is a measured fact about this
validator's self-test: it adjudicates its registered negatives against
`_semantic_findings` ONLY —

```python
# scripts/validate-credential-contracts.py:108
findings = _semantic_findings(yaml.safe_load(path.read_text()))
```

— so a negative fixture whose only defect is a SCHEMA violation raises no
semantic finding at all and is reported as `negative-should-fail`. A
schema-only implementation of this vocabulary would therefore make its own
negatives unregisterable, and SC-008's "refused naming the closed vocabulary"
would have no probe. Every closed-vocabulary refusal this cluster ships must
exist in both layers: the schema constrains, the semantic branch names, and
the semantic branch is the one the harness reads. This is why the fixture set
includes a false-valued negative alongside the out-of-vocabulary one — the
`const: true` narrowing of Decision 3 is only measurable through the semantic
mirror.

---

## Decision 5 — consent-instrument growth (FR-026, FR-039)

### The declaration sites, measured

The closed `status` set is declared in FOUR normative places, and FR-039
requires all of them to grow together:

| Site | What it is |
|---|---|
| `contracts/schemas/consent-instrument.schema.yaml:194` | the record's own `status` enum |
| `contracts/schemas/consent-instrument.schema.yaml:209` | the `status_history[].status` enum (a second declaration in the same file) |
| `contracts/schemas/consent-instrument-class-registry.schema.yaml:77` | the `status_aliases` value constraint |
| `scripts/validate-consent-instruments.py:129-130` | `NEUTRAL_STATUSES`, the Python copy the alias-target check adjudicates against (`check_registry`, lines 344-357) |

A fifth site is `PAST_SIGNATURE_STATUSES` (`validate-consent-instruments.py:133`,
`{executed, amended, terminated}`) — the states that lie past the signature
phase. `withdrawn` belongs in it: an instrument can only be withdrawn after
it was executed, so a `withdrawn` instrument under a `signature_phase: true`
class must still show `pending_signatures` in its trace. Omitting it would
open a lifecycle-skip hole through the new member. The addition is additive
by construction — it can only bind records in a state that could not exist
before this change.

**Verified precondition on the `NEUTRAL_STATUSES` growth (ruling A-7): no
consent class registry anywhere in the estate aliases a key spelled
`withdrawn`** (swept 2026-08-14). This matters because growing
`NEUTRAL_STATUSES` NARROWS a check rather than widening one: the alias-target
check (`check_registry`, lines 344-357) raises
`alias-remaps-neutral-status` (line 348) when a domain's `status_aliases` KEY
is itself a neutral status — remapping a status the neutral layer already
owns. Adding `withdrawn` to the tuple makes that spelling newly capable of
tripping the check. The sweep establishes that no registry uses it, so the
narrowing fires nowhere and no existing registry or instrument changes verdict
— which is what keeps FR-030's "existing suites unaffected" true through this
edit. Recorded as a precondition, not an assumption: if this cluster is
rebased onto a materially later estate, re-run the sweep before growing the
tuple.

The promoted requirement text at `openspec/specs/consent-instrument/spec.md:69-74`
("the closed five-state lifecycle") is PROMOTED text and is **not** edited by
this feature, by the same rule FR-025 states for doc-health: the OpenSpec
archive step rewrites promoted spec text after this feature lands.

### The dependent-kind member

`contracts/schemas/consent-instrument.schema.yaml:244` closes the enum to
`[consent_profile, credential_grant, adapter_activation, other]`, and the
item object closes `additionalProperties: false` (line 239) — so a new
dependent kind cannot ride an extra property; it must be an enum member, as
FR-026 requires ("not the `other` escape"). No token is settled anywhere in
the packet; it is minted here as **`governed_identity`**, matching the
siblings' `noun_noun` snake_case and the spec's own Key Entity name
("Governed-identity dependent reference").

**What the dependent-ref's `ref` names, and what nothing resolves (ruling
A-5).** For a `governed_identity` dependent, `ref` names the roster FRAGMENT
PATH plus the entry's `identity_ref` — the fragment at
`credentials/client-identity-roster/<client_ref>.yaml` and the identity
within it. The field itself stays a bare `{type: string, minLength: 1}`
(line 248); what this change adds is a schema `description` stating the
convention AND the posture: **the consent validator does NOT resolve it.** It
checks that a `governed_identity` dependent carries a non-empty `ref` and
nothing further — it does not open the fragment, does not confirm the entry
exists, and does not cross a repository boundary.

That is the same posture FR-037 fixes for the roster validator's
`evidence_ref`, adopted here for the same reason: both validators are
network-free and read one repository (ruling D8 makes the consent validator
standalone), so a pointer they cannot follow must be declared as a pointer
rather than implied to be a link. Stating it in the schema is what stops a
later reader from filing the non-resolution as a coverage gap and "fixing" it
with a cross-repo read that would break hermeticity. Resolution, here as with
`evidence_ref`, belongs to a pass that assembles pinned repositories.

### The cascade-evidence obligation

`cascade_evidence` is a bare `{type: string, minLength: 1}` (lines 253-255),
and `check_termination_cascade` (lines 494-505) checks PRESENCE only, gated
on `status == "terminated"`. FR-026 requires evidence covering identity
removal or retirement AND withdrawal of provider-side admission — a coverage
claim no free-text string can be checked for without a keyword heuristic,
which would fail SC-011's byte-identical-findings standard in spirit and be
trivially gamed.

Decision: make the coverage STRUCTURAL and additive. Two new OPTIONAL sibling
properties on the dependent-ref item — `identity_removal_evidence` and
`admission_withdrawal_evidence`, each `{type: string, minLength: 1}` — and a
Python obligation, not a schema one:

- schema: enum member + two optional properties. Nothing becomes required;
  every existing instrument and fixture stays valid unchanged (SC-007, FR-030).
- `check_termination_cascade`: gate widens from `status != "terminated"` to
  `status not in ("terminated", "withdrawn")`. **The REACH of the existing
  `termination-without-cascade-evidence` code widens to `withdrawn`
  instruments — that is a behaviour change, and it is declared as one; what
  is retained is the code's SPELLING, for continuity with the corpus and the
  registered negatives** (ruling A-6; the pre-gate draft's claim that the
  code was "unchanged in meaning" was false and is deleted). The widening is
  additive in the sense FR-030 requires — it can only bind instruments in a
  state that could not exist before this change, so no existing instrument
  acquires a finding — but it is not a no-op, and calling it one would have
  hidden the one place this cluster changes an existing check's behaviour. A
  NEW code `identity-cascade-incomplete` fires when a `governed_identity`
  dependent on a terminated or withdrawn instrument lacks either new field.

Putting the obligation in Python rather than in a root-level
`if status … then dependent_refs.items.if kind …` follows the family's own
precedent: the schema comment at lines 256-259 says cascade evidence is
"Optional while the instrument lives; the VALIDATOR requires it on every
reference once status is terminated". The obligation has always lived in the
validator; this grows it rather than moving it.

US4 acceptance scenario 3 ("a governed identity discovered as an undeclared
dependent … the finding lands against the instrument, not against the
identity") is the ALREADY-PROMOTED attribution rule of the same requirement,
not a new discovery mechanism: the consent validator is standalone by ruling
D8 and reads one repo, so it cannot discover an undeclared dependent by
cross-referencing roster fragments. It is measured by the negative fixture's
finding naming the instrument path.

---

## Decision 6 — the sixteenth doc-health family (FR-023, FR-025)

### Registration mechanics, measured

- Families are a plain module-level dict, `scripts/doc_health/families.py:674-690`
  (`FAMILIES = { "status-validity": fam_status_validity, … }`); late families
  are defined in their own module and merely registered here, e.g.
  `"proposal-origin": proposal_origin.fam_proposal_origin` (line 689). The
  import list is line 25.
- The entry-point contract is stated in the module docstring, line 3:
  `fam_<id>(ctx) -> list[Finding] | Skip`.
- `Finding` is `scripts/doc_health/__init__.py:73-82`
  (`severity, family, repo, path, rule, action, resolution="auto-fixable",
  disposer=None`); `Skip` is lines 93-96 (`family, reason`).
- `runner.py`'s `--family` / `--skip-family` choices are `sorted(FAMILIES)`,
  so a new key is picked up with no runner edit.
- `FAMILY_RESOLUTION` (`families.py:44-51`) assigns ONE blanket resolution
  class per family. The three late families do not use it; they set
  `resolution=CONTESTED` per `Finding` (e.g.
  `proposal_origin.py:196-201`). This family needs mixed classes (FR-023
  requires contested only for findings contradicting a ratified capability),
  so it follows that precedent and stays OUT of `FAMILY_RESOLUTION`.
- Determinism is proven by running the family twice over one fixture context
  and comparing `__dict__`s — `tests/doc-health/test_suite.py:15-19`. That
  test is family-specific (`tag-hygiene`), so the new family needs its own
  equivalent assertion (SC-011).
- Fixtures live at `tests/doc-health/fixtures/<family-id>/<repo-name>/…`;
  `tests/doc-health/conftest.py` supplies `make_ctx(family, …)` and a
  `FakeGit` with canned facts.
- **The trap in that helper (ruling A-9): `make_ctx(family, git=None,
  agg_root=None, …)` defaults `agg_root=None`** (`conftest.py:66`, feeding
  `agg_root=agg_root` at line 80). This family's FIRST branch is
  `ctx.agg_root is None → Skip("single-repo run")`. So a fixture test that
  calls `make_ctx` without passing `agg_root` explicitly never reaches the
  family's logic — it short-circuits into the skip and passes vacuously,
  green while measuring nothing. **Every fixture test for this family MUST
  pass `agg_root` explicitly**, and the one test that exercises the
  single-repo skip must pass `agg_root=None` in the call rather than relying
  on the default, so the omission can never be mistaken for intent. The
  determinism assertion (SC-011) and both finding-class tests are the most
  exposed, because a vacuous skip satisfies "identical findings across runs"
  trivially and would let SC-011 be claimed on a family that never ran.

### Cross-repo assembly

The family must assemble fragments "published by pinned domain repositories".
The mechanism already exists and needs nothing new:
`corpus.discover_repos(repo_root)` (`scripts/doc_health/corpus.py:38-50`)
returns `openxFactory` plus every `xFactories/<name>` in the aggregation
checkout; `runner.build_context` turns it into `ctx.repo_paths`
(`name -> Path`) with `ctx.agg_root` set. The family iterates
`sorted(ctx.repo_paths.items())` — the same loop `fam_proposal_origin` uses
at `proposal_origin.py:331` — and reads
`<repo>/credentials/client-identity-roster/*.yaml` from each.

Skip semantics, mapped to the two ratified cases:

- `ctx.agg_root is None` (single-repo run): `Skip("client-identity-composition",
  "single-repo run: no aggregation checkout")` — the exact pattern of
  `fam_submodule_pin_drift` (`families.py:606-610`).
- an aggregation run in which NO client has two or more fragments:
  `Skip(…, "no client is held by two or more domains: nothing to compose")`
  — US5 acceptance scenario 3, worded as "a corpus with NO client having two
  or more fragments". Where at least one client qualifies, the family returns
  findings (possibly an empty list); clients with a single fragment simply
  contribute nothing. Returning `Skip` in that mixed case would suppress real
  findings, so the skip is corpus-level, not per-client.

### The two finding classes, defined precisely

The ratified delta names them in prose only, so the plan fixes their
predicates:

- **`shared-identity-material`** — two fragments for one `client_ref` from
  DIFFERENT `domain` values whose entries name the same identity MATERIAL:
  the same `identity_ref`, or the same provider-native application identifier
  in `principal_locations[]`. Keyed on material, NEVER on (surface, class)
  collocation — FR-024 makes two domains each holding their own separate
  identity on one surface and class conformant at every level, and a fixture
  proves the discrimination.
- **`undeclared-cross-domain-reach`** — an admission act or `declared_excess`
  in domain A's fragment achieves scope over an admission surface for which A
  publishes no entry, while another domain's fragment for the same client
  declares that surface. Composition is what makes it visible; the intra-repo
  undeclared-reach rule (FR-009) fires on A's own declared permissions and is
  NOT duplicated here (FR-023, US5 acceptance scenario 2).

`resolution=CONTESTED` on any finding that contradicts a ratified capability
(US5 acceptance scenario 5); everything else takes the dataclass default.

### The count-bearing prose this feature owns

FR-025 restricts the feature to the prose sites it owns and forbids editing
`openspec/specs/doc-health/spec.md`. Measured, there are exactly two COUNT
statements in the tree:

| Path:line | Text | Disposition |
|---|---|---|
| `openspec/specs/doc-health/spec.md:11` | "SHALL implement fifteen check families" | **NOT edited** — the archive step rewrites it (FR-025) |
| `scripts/doc_health/families.py:1` | `"""The fifteen contract check families.` | **edited** → sixteen |

plus the ownership note in the same docstring (`families.py:7-11`), which
names which module owns which late family and must name the sixteenth.

ORDINAL statements are left untouched, per FR-025 ("an ordinal is not a
count"): `README.md:488`, `docs/document-lifecycle.md:132`,
`scripts/doc_health/proposal_origin.py:1`, and `families.py:10` (the
"fifteenth (add-proposal-origin-contract)" clause inside the note, which
stays true).

### A pre-existing gap this family must not silently inherit

`scripts/doc_health/__init__.py:52-70` defines `FAMILY_IDS`, used by
`report.py:251` to render the report's per-family sections. The list stops at
`"ideation-routing"` and does NOT contain `"proposal-origin"` — the fifteenth
family has no report section, although its archived task record claims the
registration touched "the registry, runner, configuration, and report
output".

Decision: this feature ADDS `"client-identity-composition"` to `FAMILY_IDS`,
so the new family renders a report section and SC-009's "reporting or
skipping with an explicit reason" is observable in the report as well as in
the run. It does NOT fix the `proposal-origin` omission — that is an
unrelated defect in another capability's realization and belongs to its own
change. The observation is recorded here so the next reader does not mistake
the asymmetry for a mistake in this feature.

### The collision check FR-023 demands

`scripts/doc_health/shared_identity.py` is NOT a doc-health family: it is not
imported in `families.py:25`, has no key in `FAMILIES`, and declares no
`FAMILY = "…"` constant at all. It is the deterministic detector behind the
ideation dashboard's repository lens (`add-shared-identity-seeds`), consumed
by `scripts/ideation_dashboard/serve.py:2168` and tested at
`tests/ideation-dashboard/test_shared_identity.py`. Family id
`client-identity-composition` and module `client_identity_composition.py`
therefore collide with nothing, and "shared identity material" stays a
FINDING CLASS inside the new family, never its name.

---

## Decision 7 — the two-layer validator and where each rule is proven

`scripts/validate-credential-contracts.py` is the closest sibling in shape
and consumption (canonical, pinned checkout, one positional domain-repo
argument, self-test over packaged examples, then a repo scan). The roster
validator follows it, with the layers doing different work because the
roster's rules split into two classes:

- **Record-internal rules** — everything decidable from one fragment: closed
  vocabularies, the uniqueness tuple, the legend, verified-vs-unverified
  admission, achieved-vs-intended authority, **the scope-excess rule** (a
  verified act declaring `exceeds_governed_unit` requires a `declared_excess`,
  and the entry's effective reach is the union of verified acts'
  `(surface, achieved_scope)` pairs plus the OR of their exceedance flags),
  residency obligations, lifecycle, attestation, both roots, the alias rule,
  `evidence_ref` SHAPE.
  Proven by the PACKAGED corpus (`examples/client-identity-roster/` plus
  `negative/`) in the self-test layer, in the dialect the tree already uses.
- **Repo-context rules** — decidable only against a target tree: the
  whole-repo misplacement sweep (FR-036), gate-obligation RESOLUTION against
  the target's `workflows/` records (FR-011), **`consent_ref` RESOLUTION
  against the target repo's own consent-instrument records (FR-014's second
  clause) — by kind sweep for `xfactory_consent_instrument`
  (`consent-instrument.schema.yaml:62`) matched on `instrument_id` (`:63`),
  the mechanism `validate-consent-instruments.py`'s `repo_scan` already uses,
  because that family declares no domain placement to cite the way FR-011
  cites `workflows/`** — and the absence notice (FR-022). The consent citation
  resolves intra-repo by the same argument as the gate obligation — a domain's
  consent instruments live in the domain repo
  (`OpsxFactory:tenants/farheap-bc-administration-consent.yaml` is the worked
  example) — which is the opposite posture from `evidence_ref` (FR-037), a
  pointer into ANOTHER repo that this validator may only shape-check. Presence
  alone does not satisfy FR-014: a citation resolving to nothing is the failure
  the change's central claim (consent, not our own ratification, authorizes
  standing) depends on catching. `ratified_by` is NOT resolved — the ratified
  clause attaches resolution to the instrument citation alone and the delta's
  capability scenario is an absence test, so the capability check stays
  presence plus domain-qualification.
  Proven by repo-shaped fixtures built in `tmp_path`, which is the
  idiom the conformance pack already uses
  (`tests/conformance-gate/test_conformance_checks.py` builds fixture domain
  repos from inline templates).

The misplacement rule is the forcing case for the split: a packaged negative
fixture cannot express it, because every packaged example sits outside
`credentials/client-identity-roster/` by construction and would itself be a
misplacement. FR-016 lists "a roster instance outside the declared placement"
among the corpus's negatives; the plan satisfies it as a repo-shaped fixture
and says so, rather than fabricating a packaged file that cannot mean what it
claims.

Corollary the sweep needs: the repo-scan layer must EXCLUDE this feature's own
fixture corpora when the target repo is the openxFactory checkout itself —
`<openxFactory>/examples/client-identity-roster/` AND `<openxFactory>/tests/`
— the first exactly as `validate-consent-instruments.py:699` excludes
`EXAMPLES_DIR` from its `repo_scan`, the second because Decision 6's family
fixtures put REAL roster fragments at
`tests/doc-health/fixtures/client-identity-composition/<repo>/credentials/client-identity-roster/*.yaml`.
Those are at each FIXTURE repo's declared placement and are validated normally
when a fixture repo is the target (the A-N4 run), but they are NOT at the
openxFactory checkout's own `credentials/client-identity-roster/`, so without
the `tests/` exclusion a self-scan reports every one as misplaced. The tree
states the rule for its sibling scanner and tests it:
`tests/doc-health/test_suite.py:23-27`, "fixture corpora must never enter a
real scan". Neither exclusion narrows FR-036 or ruling R1 over a TARGET DOMAIN
repo, which carries no such trees.

**The same forcing argument applies to FR-011's gate-obligation negative, and
the pre-gate draft missed it (ruling A-11, the plan gate's one BROKEN
verdict).** Obligation RESOLUTION reads the TARGET repo's `workflows/`
records, so it is a repo-context rule by this section's own classification — a
packaged fixture has no `workflows/` tree to resolve against and cannot
express the rule any more than it can express misplacement. The pre-gate
fixture plan carried `missing-enforcement-test.yaml` (FR-011's OTHER half,
which is record-internal and correctly packaged) and routed nothing for
"unresolvable gate obligation", leaving that named FR-016 rule with no
negative home in ANY corpus. The fix is a repo-shaped fixture whose entry's
`declared_excess.gate_obligation` names a gate ABSENT from that fixture's
`workflows/`, while the repo carries at least one real gate so the finding
proves non-resolution rather than an empty tree. Its discrimination partner is
the conformant repo fixture, whose obligation DOES resolve.

**A second addition from the same ruling: FR-004 gains
`negative/achieved-class-contradicted-by-permissions.yaml`** — an entry
declaring `authority_class_achieved: observe` while a `granted_permissions[]`
member DECLARES `achieves: mutate`. (The pre-analyze wording said "while its
permissions carry a write- or delete-capable permission", which an implementer
could only evaluate by reading the identifier's spelling — the inference the
object member form exists to forbid; the contradiction is between two
declarations in the record.) FR-016's
named list is a MINIMUM ("one NEGATIVE CONFIRMATION per rule — at minimum"),
and FR-004 is a rule of its own: it forbids ASSERTING an achieved class the
permissions contradict, which is distinct from
`achieved-exceeds-intended-undeclared.yaml`'s rule that achieved-above-intended
must be DECLARED. Neither fixture substitutes for the other, and before this
addition the first rule had no probe.

The re-counted per-rule coverage table lives in plan.md, Cluster C: 16 named
FR-016 rules, 16 homed, 0 unhomed (13 packaged, 2 repo-shaped, 1 doc-health).

THREE negatives from FR-016 belong to OTHER corpora and are routed there
rather than duplicated:

- "cross-domain shared identity" is a CROSS-DOMAIN rule; it is proven in
  `tests/doc-health/fixtures/client-identity-composition/`, because the
  intra-repo validator must not carry it (FR-023, US5 acceptance scenario 2).
- "a roster instance outside the declared placement" is the misplacement rule
  argued above — a repo-shaped fixture.
- "an unresolvable gate obligation" is the FR-011 rule argued above — a
  repo-shaped fixture (ruling A-11).

And separately from FR-016's list, the `issuance_preconditions` negatives
belong to `examples/credential-contracts/negative/` and its
`NEGATIVE_EXPECTATIONS` table.

---

## Decision 8 — the packaged multi-surface reader (FR-019) and its provider
fact

FR-019 mandates "a provider-forced multi-surface reader" among the packaged
cases. FR-007 closes `admission_surface` to `business_central` and
`exchange`, and FR-031 forbids adding a surface. So the packaged
multi-surface reader must span exactly those two.

The ratified precedent the proposal cites for this case —
`microsoft_managed_node_inventory_reader`, holding Entra, Intune and Windows
365 read scopes on one identity — spans surfaces that are OUT of the
first-release vocabulary and therefore cannot be transcribed into the
example.

The conformant realization is a service principal holding a directory role
whose narrowest available form reaches both the Business Central admin centre
and Exchange Online read surfaces, declared with:

- `granted_permissions[]` in provider-native identifiers (the role, plus
  `Exchange.ManageAsApp` where the surface requires it),
- `declared_excess.provider_reason` stating that the provider offers no
  read-only role scoped to one of the two surfaces,
- the gate obligation and enforcement-test reference FR-010 requires.

**Constraint on the builder, stated as a rule rather than a hope:** the
`provider_reason` must cite the provider's own documentation or a record in
the OpsxFactory evidence chain. A packaged example may not assert a provider
fact the builder cannot cite. If no citable spanning permission is found, the
case is ESCALATED (the example cannot be softened into a single-surface
reader without under-delivering FR-019), not invented.

**That constraint is mechanized as a PRECONDITION, not left as a discovery
(ruling A-16).** The provider fact is verified BEFORE the packaged-examples
cluster begins — before any example file is authored — because the difference
between the two orderings is the difference between escalating cheaply and
escalating after a corpus has been built around an assumption. The fact to
establish: that one provider-native permission or directory role, in its
narrowest available form, reaches BOTH the `business_central` and the
`exchange` read surfaces, and that no read-only role scoped to just one of the
two exists.

- Citable fact found → the cluster proceeds; the citation is transcribed into
  `declared_excess.provider_reason`.
- No in-vocabulary citation → **STOP and escalate to the architect**, listing
  the candidates examined and why each failed. The builder does not synthesize
  a provider fact and does not soften the case into a single-surface reader;
  either would under-deliver FR-019 and silently drop SC-002's fourth
  positive.

The escalation path existed and had not triggered as of the plan gate.

---

## Convention and tree findings the implementation rests on

### Validator shape (from `scripts/validate-credential-contracts.py`)

- `SCHEMA = Path(__file__).resolve().parents[1] / "contracts/schemas/…"`;
  no host-absolute paths (constitution IV).
- `Draft202012Validator(yaml.safe_load(SCHEMA.read_text()))`.
- One positional argument, the target domain repo; `print(__doc__)` and
  `raise SystemExit(2)` on wrong argc.
- Self-test first, then the scan; a closing verdict line
  (`N checked, M skipped, K errors -> PASS|FAIL`); `SystemExit(0 if not
  errors else 1)`.
- Findings printed as `ERROR <rel-path>: <code>: <message>`;
  `oneOf` sub-error noise is filtered so the reported message is the
  branch-specific one.
- Negatives registered by filename in a module-level expectations table so a
  probe cannot exist without a file or a file without a probe (FR-018).

`scripts/validate-consent-instruments.py` supplies the richer variant this
family also needs: a `Findings` class emitting `ERROR [kebab-code] message`
(lines 167-182), an `EXPECTED_NEGATIVE_FINDINGS` table mapping filename to
`(code, optional detail substring)` (lines 149-155) with five distinct
self-test failure modes (`negative-missing`, `negative-unregistered`,
`negative-should-fail`, `negative-wrong-reason`, and the detail-substring
mismatch), and `SKIP_DIR_NAMES = {".git", "node_modules", "__pycache__",
".venv"}` for the repo walk (line 687). The roster validator adopts the
kebab-code `Findings` class and the two-part expectations table, because
FR-018 requires refusing a negative that fails for the WRONG reason and
several roster negatives would otherwise collapse into a generic `schema`
finding.

### Examples layout

`examples/<family>/` with `negative/` and a `README.md` carrying a `Status:`
header — the shape of `examples/consent-instrument/` (measured: README with
`Status: draft`, five positives, a `negative/` directory). The sibling
`examples/credential-contracts/` carries the positives and the `negative/`
directory but NO README at all, so the README half of the convention rests on
the consent family and on the 006 header precedent cited below, not on both
siblings. Positives are
`<family>-<tag>.example.yaml` directly in the family directory; negatives are
`<violation-description>.yaml` under `negative/`, with no `.example` infix,
one violation per file, each opening with the tree's comment dialect:

```
# INVALID <record noun> — violates <requirement> (<rule>): <what is wrong>
# … (finding <finding-code>).
```

The tree carries TWO negative-header dialects: the consent family's `# INVALID
… (finding <code>)` and the credential family's terser `# NEGATIVE (expect:
<code>). …` (`examples/credential-contracts/negative/dispatch-grants-contents.yaml:1`).
This family takes the CONSENT dialect, because it also takes the consent
validator's two-part expectations table (code plus optional detail substring),
and a header that states the requirement and the rule it violates is what
makes FR-018's "fails for the wrong reason" reviewable by a human as well as
by the harness. The one negative this feature adds to
`examples/credential-contracts/negative/` keeps THAT directory's dialect.

Family README headers follow the 006 precedent —
`contracts/openxwallet/README.md:3-6` carries `Status: ratified` plus a
`Ratified by:` line naming the change and the bundle it registered at — rather
than the older sibling READMEs' `Status: draft`.

C3 already ruled the rival `contracts/<family>/examples/` convention (feature
006) out for this family.

### Registration mechanics

- `contracts/manifest.yaml` — `contract_bundle_version` at the top (today
  `contract-v1.31`); rows carry `id, path, source_path, type, schema_version,
  sha256, compatibility: canonical_openxfactory_contract, adapter_owner:
  openxFactory, consumption_rule`. The v1.31 rows (openxWallet) are the shape
  to copy, including the closing sentence "Registered at contract-v1.NN;
  consumed through the pinned openxFactory checkout with per-file sha256
  verified before any copy is treated as current."
- `scripts/validate-manifest-digests.py` recomputes every row's `sha256`
  against the file on disk and fails closed — this is the check FR-021's
  "digest verification passes" names.
- `contracts/releases/contract-v1.NN.digests.yaml` is a DIFFERENT and
  narrower artifact: it is built by
  `scripts/validate-contract-release.py build --tag … --output …` and its
  membership is closed over the Hermes-runtime release surface plus
  `contracts/manifest.yaml`, `contracts/CHANGELOG.md`,
  `contracts/README.md`, `contracts/hermes-runtime/README.md` and
  `docs/contract-versioning-policy.md`
  (`scripts/hermes_runtime_validation/release.py:64-70`). Measured: the path
  membership of `contract-v1.30.digests.yaml` and
  `contract-v1.31.digests.yaml` is IDENTICAL (190 entries), and neither
  contains an openxwallet, consent-instrument or credential-contracts path,
  even though v1.31 registered the openxWallet families. So cutting v1.32
  regenerates the inventory because the manifest and changelog digests
  change, NOT because roster files enter it. The plan states this so nobody
  hand-adds roster paths to the inventory.
- `contracts/CHANGELOG.md` carries an `## Unreleased — pending bundle
  registration (fold into the next cut)` block holding one additive
  openxwallet enum widening whose manifest digest is already refreshed. This
  feature cuts the next bundle, so that block folds into the
  `## contract-v1.32` entry rather than surviving alongside it.

### A registration gap FR-021 assumes away

FR-021 requires that every OTHER schema this feature edits "have its manifest
row REFRESHED". Measured: `contracts/schemas/xfactory-credential-contracts.schema.yaml`
**has no row in `contracts/manifest.yaml`** (grep for `credential` over the
manifest returns only unrelated prose) and no row in the
`contracts/README.md` registration table, though it is linked from
`README.md:226` and `docs/credential-access-model.md:11`.

Decision: for that schema, FR-021's "refresh" is a FIRST REGISTRATION —
a new row at `contract-v1.32` in the shape the v1.31 rows use. Recorded
rather than silently performed, because the requirement's wording assumes a
row that does not exist.

Related trap: the manifest's per-row `schema_version` mirrors the RECORD
envelope's `schema_version` const, not the schema file's
`contract_schema_version`. The consent-instrument records' envelope const
stays `1` (changing it would invalidate every existing instrument); what
bumps is the schema FILE's `contract_schema_version` (1 → 2 in
`consent-instrument.schema.yaml:9` and in
`consent-instrument-class-registry.schema.yaml:7`). The bump is recorded in
the row's `consumption_rule` prose, which is exactly what the pending
`Unreleased` changelog entry did for the openxwallet widening.

### The BC evidence chain (corrects the seed handoff, confirms the spec)

Verified in `opensoft/OpsxFactory`: `tenants/farheap-bc-sandbox1-verify-probe-evidence-v3.yaml`
through `-v7.yaml`, plus `farheap-bc-observer-identity-evidence-v1.yaml`,
`farheap-bc-sandbox1-registration.yaml` and
`farheap-bc-administration-consent.yaml`, are all present on `origin/main`.
Packaged-example `evidence_ref` pointers therefore aim at real pinned content
— while remaining UNRESOLVED pointers at the canonical validator, which
checks their shape only (FR-037).

`granted_permissions[]` for the worked case, verbatim from that record:
`API.ReadWrite.All`, `Automation.ReadWrite.All`, `AdminCenter.ReadWrite.All`,
`app_access` — each transcribed as the `id` of a `granted_permissions[]` member
whose `achieves` and `reaches[]` the record declares (plan.md Cluster A: the
neutral layer never infers a class from an identifier's spelling), permissions
that achieve MUTATION on an identity named
`opsx-farheap-bc-observer`, which is the name/purpose mismatch acceptance
scenario 4 exists for, and which the packaged example expresses through
`declared_excess` rather than by renaming anything in a domain repo.

### Record immutability

`openspec/changes/add-client-identity-roster/review/decision-review-2026-08-14.md`
and `review/amendment-record-2026-08-14.md` both carry `Status: record`. The
doc-health `record-immutability` family treats a change to a record as
CRITICAL. The amendment record is itself the precedent: it is a SIBLING file
that says "Companion to: `decision-review-2026-08-14.md` … appended to here
rather than edited, per the record-immutability rule". Any further amendment
this feature provokes lands as a new sibling record file, never as an append
or an edit.
