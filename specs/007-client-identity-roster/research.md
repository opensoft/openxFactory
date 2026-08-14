# Research: client identity roster neutral contracts and conformance wiring

**Feature**: `007-client-identity-roster`
**Governing change**: `add-client-identity-roster` (ratified 2026-08-14, Brett
Heap; AMENDED the same day, Decisions A and B)
**Rulings**: [clarify-rulings-2026-08-14.md](clarify-rulings-2026-08-14.md) —
authoritative over this file wherever they touch the same ground.

This file records the decisions the ratified packet and the clarify rulings
left to the plan phase, the derivations behind them, and the convention and
tree findings the implementation rests on. Decisions the rulings already fixed
are NOT relitigated here; they are cited.

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
and whose values are booleans:

```yaml
issuance_preconditions:
  type: object
  minProperties: 1
  propertyNames:
    enum: [roster_drift_clear_required,
           accepted_request_required,
           registered_active_subject]
  additionalProperties: {type: boolean}
```

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
  `status not in ("terminated", "withdrawn")`; the existing
  `termination-without-cascade-evidence` code keeps firing for every
  dependent kind; a NEW code `identity-cascade-incomplete` fires when a
  `governed_identity` dependent on a terminated or withdrawn instrument
  lacks either new field.

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
  admission, achieved-vs-intended authority, residency obligations,
  lifecycle, attestation, both roots, the alias rule, `evidence_ref` SHAPE.
  Proven by the PACKAGED corpus (`examples/client-identity-roster/` plus
  `negative/`) in the self-test layer, in the dialect the tree already uses.
- **Repo-context rules** — decidable only against a target tree: the
  whole-repo misplacement sweep (FR-036), gate-obligation RESOLUTION against
  the target's `workflows/` records (FR-011), and the absence notice
  (FR-022). Proven by repo-shaped fixtures built in `tmp_path`, which is the
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

Corollary the sweep needs: the repo-scan layer must EXCLUDE
`<openxFactory>/examples/client-identity-roster/` when the target repo is the
openxFactory checkout itself, exactly as
`validate-consent-instruments.py:699` excludes `EXAMPLES_DIR` from its
`repo_scan`. Otherwise pointing the validator at its own repo reports its own
packaged corpus as misplaced.

Two negatives from FR-016 belong to OTHER corpora and are routed there rather
than duplicated:

- "cross-domain shared identity" is a CROSS-DOMAIN rule; it is proven in
  `tests/doc-health/fixtures/client-identity-composition/`, because the
  intra-repo validator must not carry it (FR-023, US5 acceptance scenario 2).
- the `issuance_preconditions` negative belongs to
  `examples/credential-contracts/negative/` and its
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
header — the shape of `examples/consent-instrument/` and
`examples/credential-contracts/`. Positives are
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
`app_access` — permissions that achieve MUTATION on an identity named
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
