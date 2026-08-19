# openxFactory Contract Changelog

Status: draft

Governed by [Contract Versioning Policy](../docs/contract-versioning-policy.md).

Legacy baseline note: versions `contract-v1.1` through `contract-v1.6`
predate mandatory annotated tags and carry none. Tag enforcement begins at
`contract-v1.7` — the first realized release published with an annotated tag —
without fabricating historical tags.

## contract-v1.34 — 2026-08-18 (additive + deprecating; the doxBench chat-turn widening)

Realizes `add-doxbench-editing-phase-b` §13, the contract release its ratified
"chat-turn contract release carries the bound buffer and the model" requirement
names. One CONTRACT changes —
`schemas/xfactory-workbench-chat-turn.schema.yaml` — and one normative document
moves with it: [`docs/contract-versioning-policy.md`](../docs/contract-versioning-policy.md)
records this cut's deprecation in its "Deprecations Currently In Force" list.
Both are release-surface members and both are digested in this cut's inventory.

**Change class: ADDITIVE (minor) plus a DEPRECATION (minor)**, both under
[`docs/contract-versioning-policy.md`](../docs/contract-versioning-policy.md)
lines 128-135. Nothing here is breaking: no required field is added to an
existing shape, no shape is removed, and no vocabulary is reinterpreted, so a
consumer on the same major version remains conformant WITHOUT CHANGES.

`xfactory-workbench-chat-turn.schema.yaml` gains a CO-RESIDENT SECOND ENVELOPE
FAMILY beside its existing one — `workbench-chat-turn-v2`,
`workbench-chat-turn-v2-success`, `workbench-chat-turn-v2-failure` — added to
the file's top-level `oneOf` and discriminated by `kind`, exactly as the three
v1 envelopes already discriminate each other. The widened family carries what
the v1 shape had no room for: the outline plus EVERY loaded document buffer
(`buffers` widens from `minItems: 2, maxItems: 2` to `minItems: 2, maxItems: 25`
— the surface's declared 24-document loaded-set bound plus the reserved
outline); the DECLARED `bound_buffer` key on both the request and the durable
record; `observed_hashes` keyed by BUFFER KEY rather than by the two fixed names
`outline` and `document`; `typed_proposal.target` as a buffer key rather than a
two-value enum, with the proposal list bounded by the buffer set rather than by
a literal 2; and `selected_model` metadata beside `model_id`, so a record states
both which model ANSWERED and which entry the human CHOSE (the two differ
exactly when the chosen entry is a routing rule). The v2 request carries no
`active_document_path`: the binding is DECLARED, never inferred from an adjacent
field that answers a different question.

**The v1 request, success and failure blocks are BYTE-IDENTICAL to their
contract-v1.31 bytes** and keep validating; a client that submits the previously
released shape is still served. That byte identity is asserted by a test against
a committed baseline, not by re-validation. The file's own
`contract_schema_version` stays `1`, and the envelope-level `schema_version`
stays `1` with it, because nothing previously valid becomes invalid.

**Deprecation, with its removal target recorded.** The whole v1 family
(`workbench-chat-turn`, `workbench-chat-turn-success`,
`workbench-chat-turn-failure`) is DEPRECATED as of this release. The record is
machine-readable in the schema's own top-level `deprecated_envelopes` block —
placed outside every envelope precisely so the deprecated bytes do not move.
Removal target: **contract-v2.0**, which is the next major and therefore the
earliest release at which a removal is legal; this deprecation starts the
"at least one full minor release where the old shape produced deprecation
warnings" clock the policy's breaking path requires. Migration: submit
`workbench-chat-turn-v2` instead of `workbench-chat-turn`; carry every loaded
buffer in `buffers` rather than exactly two; replace `active_document_path` with
`bound_buffer` (the key of the buffer the conversation is working ON, which must
name one of the buffers the same request supplies); read `observed_hashes` and a
proposal's `target` as buffer keys; and read the answering model from `model_id`
with the chosen entry from `selected_model`.

**What the deprecation does to your tooling.** The family's delegated validator
(`scripts/validate-ideation-dashboard-contracts.py`) reads the schema's own
`deprecated_envelopes` block and now emits ONE WARNING per validated v1 instance,
naming the superseding kind and the removal target — that warning is what the
deprecating change class requires, and the instance is still ACCEPTED, so the
default invocation still exits 0. The consequence to plan for: under the opt-in
`--strict` flag ("treat warnings as errors") a v1 instance now exits 1. That is
strict mode working as documented, and it is the intended way to find the shapes
that will not survive `contract-v2.0`; it is no longer the right command for
gating a corpus that legitimately still holds v1 instances.

## contract-v1.33 — 2026-08-15 (additive; the client-identity roster, and the credential-contracts registration gap closed)

Realizes `add-client-identity-roster` through Speckit feature
`007-client-identity-roster`: one new neutral contract family, one first-ever
registration of an already-promoted schema, and additive growth in two
existing capabilities. **Every change in this cut is ADDITIVE under
[`docs/contract-versioning-policy.md`](../docs/contract-versioning-policy.md)
lines 130-132** — the class is "new optional fields, new contracts, new
validator warnings", and its test is that a domain repo on the same major
version remains conformant WITHOUT CHANGES. Each item below is stated against
that test explicitly, because the cut touches capabilities domains already
consume.

`schemas/xfactory-client-identity-roster.schema.yaml` is the NEW family: the
record in which a domain factory declares every governed identity it holds
standing inside a paying client's provider tenant, and the report-only drift
finding that reports when observed state departs from that declaration. Two
kinds behind one top-level `oneOf`, because the fragment and the drift record
that cites it are produced and consumed by one lane and the five-element
uniqueness tuple — (domain, admission surface, authority class, blast-radius
unit, duty) — must be defined once and referenced by both. Entries carry
verified admission with achieved scope (a claimed-but-unevidenced verification
is unrepresentable, not merely discouraged), structural scoping preferred over
name-based scoping, declared provider-forced breadth where the provider offers
no narrower grant, and a fragment-scoped free-token legend. **Additive by the
policy test: it is a NEW contract, so no existing record is reinterpreted and
no domain repo needs an edit to stay conformant.** A domain that publishes no
fragment stays conformant and its checks report a notice, never a finding.

`schemas/xfactory-credential-contracts.schema.yaml` receives its **FIRST
manifest registration** in this cut. The schema was promoted at DTN-004
(`promote-credential-contracts`) without a manifest row, so the digest
cross-repo consumers are told to verify did not exist for the file they pin;
this cut closes that gap rather than refreshing anything. Registered together
with its one growth: the OPTIONAL `issuance_preconditions` object on a
credential requirement, a CLOSED vocabulary (`accepted_request_required`,
`registered_active_subject`, `roster_drift_clear_required`) in which every
value is `const: true`, because a precondition is DECLARED or NOT DECLARED —
`false` is not a second meaning, it is a declaration that reads as governance
while asserting nothing. **Additive by the policy test: the property is
OPTIONAL, so a requirement record that declares nothing at all remains valid,
and both live OpsxFactory records already carry `true`.**

`schemas/consent-instrument.schema.yaml` (`contract_schema_version` 1 → 2) and
`schemas/consent-instrument-class-registry.schema.yaml`
(`contract_schema_version` 1 → 2) grow so the termination cascade reaches a
standing identity in another party's tenant. The lifecycle enum gains
`withdrawn` as a SECOND TERMINAL state, reachable once the instrument is past
execution and a DISTINCT member — never an alias of `terminated`, because
withdrawal by the consenting party and termination are distinct events that
both raise the cascade obligation; the class registry's `status_aliases`
target enum tracks that six-state lifecycle. `dependent_refs` gains the NAMED
`governed_identity` kind with two evidence siblings
(`identity_removal_evidence`, `admission_withdrawal_evidence`), because a
credential revocation alone leaves the identity standing in the client's
tenant with its admission intact, and removing one of the two keys is a
half-cascade. **Additive by the policy test on both counts: an ADDED ENUM
MEMBER and OPTIONAL properties. No existing instrument becomes invalid, no
existing alias declaration becomes invalid, and no domain repo on the same
major version needs a change** — which is why the RECORD envelope's
`schema_version` stays `const: 1` in both schemas while the schema files'
`contract_schema_version` bumps: bumping the record envelope would invalidate
every instrument in the estate, the opposite of additive. The two manifest
digests are refreshed with the bump recorded in their `consumption_rule`.

Consumers pin this release and run
`scripts/validate-client-identity-roster.py <domain-repo>` from the pinned
checkout, never a copy inside a domain repository; the packaged corpus is
`examples/client-identity-roster/` — 4 example YAMLs and a README, plus 31
registered negatives under `negative/`, each failing for its own registered
reason. The roster paths are content-addressed by commit and deliberately do
NOT enter the release digest inventory, whose membership is unchanged from
v1.30, v1.31 and v1.32. `scripts/validate-credential-contracts.py`'s
skip-with-notice over `credentials/client-identity-roster/` is EXPECTED and
BLESSED: the canonical roster validator claims exactly that path.

## contract-v1.32 — 2026-08-15 (additive; the Subject Hermes overlay kind)

Cuts the standing Unreleased items: the `hermes_subject_overlay` kind and
validator dispatch (add-subject-overlay-contract, ratified 2026-08-15,
PR #183 merged cb738ba5) and the openxwallet RSA signature-algorithm
widening. Also corrects the `omnigent-domain-overlay` manifest digest,
which drifted when df16f21 edited the schema without refreshing the
recorded digest.

- **Additive**: `contracts/hermes-domain-overlay/hermes-subject-overlay.schema.yaml`
  — the neutral `hermes_subject_overlay` kind for a Subject Hermes layer's
  seedable document (add-subject-overlay-contract, ratified 2026-08-15).
  Subject identity (`id`, not `ref` — a subject overlay DECLARES an identity
  that exists in no prior registry), a `policy_namespace`, a declared
  `relation_to_baseline` (single-value enum `additive_constraints_only`), and
  a non-empty `policies` mapping keyed by policy id whose entries restate
  their own `policy_id` and `policy_namespace` and keep an OPEN body — so a
  named policy is addressable as `<policy_namespace>/<policy_id>` without the
  neutral contract enumerating policy names, which is exactly what stopped the
  tenant-layer override contract from carrying one. The kind name is canonical
  (`subject`) while the runtime layer role key stays the frozen `customer`;
  the mapping is recorded in the schema header, and neither side is renamed.
  `scripts/validate-hermes-domain-overlay.py` gains the kind and now dispatches
  descriptor-declared paths BY KIND instead of skipping everything that was not
  a domain overlay, retaining the skip-with-notice for kinds owned by another
  canonical validator (`hermes_client_overlay` →
  `scripts/validate-client-content.py`); it adds address self-consistency and
  uniqueness, the prohibited-block list, and cross-document identity
  conformance against the domain's own `subject_hermes_template` (absent
  template = skip with notice, no new refusal class). One positive example and
  eleven negatives ship with it (eight document-shaped, three repo-shaped).
  Additive only: no released file's bytes change, so existing pins — including
  hermes-install's `contract-v1.18` pinned copies — resolve byte-identically
  until they choose to re-pin. Manifest entry added; the bundle minor number
  and annotated tag are allocated LATE at realization per the versioning
  policy.
- **Additive**: `openxwallet-record.schema.yaml` `signature_algorithm`
  enum widened with `rsa-2048-sha256` and `rsa-3072-sha256`
  (RSASSA-PKCS1-v1_5 over the named SHA-2 digest). Found by the first
  consumer, the LedgerxFactory posting segregation-of-duties control:
  its enforcement surface verifies proofs with Business Central's own
  crypto, and BC 28.3 AL exposes exactly RSA/DSA/RSASSA-PSS — no
  ed25519, no ECDSA (measured against the 28.3 System Application
  symbols, enum 1446 SignatureAlgorithm). The curve-only enum therefore
  admitted no algorithm the platform could verify locally, forcing
  verification off-platform against the consumer's local-decision rule.
  Existing records remain conformant; one positive example added
  (`wallet-agent-rsa-platform-verifiable.example.yaml`, corpus now 17
  positives); manifest digest for the schema refreshed with the
  amendment noted in its `consumption_rule`.

## contract-v1.31 — 2026-08-07 (additive; the openxWallet core and its first profile)

Realizes `add-openxwallet` tasks 3.1 and 3.2 through Speckit feature
`006-openxwallet-contracts`, registering two new neutral contract families and
modifying no existing capability.

`contracts/openxwallet/` is the HOLDER-AGNOSTIC core — a wallet is a signing
key anchored to a decentralized identifier and held by a person, practitioner,
organisation or agent. Six kinds: the wallet record (a key REFERENCE and a
declared custody model, never key material, with every object closing
`additionalProperties` so no key-shaped field can be added at any depth); the
closed custody registry; the attenuated capability grant (audience, scope,
expiry, parent, narrowing monotonically); the grant exercise record (proof of
possession, key attribution, revocation checked at use, distinct-holder
evaluation); the opt-in distinct-holder constraint; and the subject
attestation carrying the non-substrate rule that preserves MedxFactory's two
ratified wallet constraints.

The custody registry is where Brett's ruling of 2026-08-07 — custody is
DECLARED from a closed set and CAPS authority — becomes contract content
rather than an implementation detail. `evidences` is DERIVED from two declared
booleans and enforced, not asserted: a key readable by the holder's own
execution context evidences the ENVIRONMENT, and only isolation together with
an authorization that context cannot supply evidences the HOLDER. Three
invariants make the collapse the ruling closes structurally impossible rather
than discouraged — the derivation itself, a top-of-ladder ceiling that must be
earned (keyed on RANK, not on the tier's name, so renaming the top tier cannot
disable the rule), and a check that no model evidencing only the environment
sits at or above a model evidencing the holder.

`contracts/openxwallet-agent-profile/` is the FIRST profile over that core,
registered as a SIBLING family rather than an extension of it, so patient and
practitioner profiles arrive the same way. It settles the change's open task
3.2 — what the composition component set covers — by giving every component a
`binding_mode`: `content` digests the component itself, while `reference`
covers a corpus's identity and governing configuration but not its row-level
contents. Swapping a corpus or widening retrieval scope changes identity and
revokes; documents arriving in an already-governed corpus do not.

Consumers pin this release and run `scripts/validate-openxwallet.py` from the
pinned checkout. The validator enforces nineteen rules the shapes cannot
express and READS the legal approval-scope vocabulary out of
`contracts/schemas/hermes-job-envelope.schema.yaml` at run time rather than
restating it, because restating it would recreate the parallel authority
vocabulary the profile's third requirement forbids. The packaged corpus
comprises 16 valid examples and 33 intended-invalid negatives covering 11 of
11 ratified requirements, with coverage closed in both directions — a
requirement with no probe, and a probe naming no requirement, are both
validation failures. A red-proof harness recorded with the feature confirms
all 21 finding codes are load-bearing: suppressing any one turns the corpus
red.

No runtime, wallet infrastructure, key storage, issuance service, or signing
implementation lands with this release; no key, credential or wallet is
created; and no domain is obliged to adopt wallets. The `openxVault` boundary
Brett set on 2026-07-16 is preserved: the vault owns custody and its gate
consumes these grants.

## contract-v1.30 — 2026-08-06 (additive; cross-factory ideation routing and the consent-instrument family)

Realizes `add-cross-factory-ideation-routing` task 2.4 by registering the
four routing schemas: the canonical idea routing record, the reusable
structured repository-reference kernel, the central Idea-ID allocation
ledger, and the immutable organizer-recommendation evidence shape. Together
they define the governed cross-factory routing plane: one record per
unclassified, mixed, or claim-split idea, single-authority ID allocation,
controlled transitions with destination-owner acceptance, and non-mutating
organizer evidence. Consumers pin this release and run
`scripts/validate-ideation-routing.py` from the pinned checkout; the
packaged corpus comprises 8 valid and 8 intended-invalid examples (44
validator tests green at the cut).

Realizes `add-consent-instrument` task 1.6 (DTN-016 → `adopted`) by
registering the three consent-instrument schemas: the
`xfactory_consent_instrument` record kind (the authority-chain root that
credential grants cite, gates verify, and whose termination cascades
through declared dependent references), the domain-owned closed
instrument-class registry, and the domain-declared purpose model for the
neutral purpose-resolution check. Existing domain instances (the Ledgerx
engagement consent record, the Medx patient consent record) conform by
declaration, never by rewrite. Consumers pin this release and run
`scripts/validate-consent-instruments.py` from the pinned checkout; the
packaged corpus comprises 5 valid examples (including registry and purpose
model), 5 intended-invalid negatives, and 2 purpose-resolution probes.

Also riding this cut: the project-plane ADDITIVE deltas that landed on
`gate-intent`, `gate-action-record`, `ideation-dashboard-snapshot`, and
`xfactory-document-catalog-snapshot` after `contract-v1.29` — the
`create-project` / `edit-project` commissions with `target.project_id`,
multi-parent project membership (D8), and the project-first header fields
(`add-project-scoped-selection`, `add-project-merged-projection`,
`add-opendox-project-header`, each of whose own registration task realizes
against this release). Their per-file manifest digests are refreshed here
so the bundle describes main's actual bytes.

The growth is entirely additive: the pre-existing schema deltas above keep
`contract_schema_version: 1`, and no prior record is invalidated.

## contract-v1.29 — 2026-08-03 (additive; wheel action verbs, gate intents, and worker enrollment)

Realizes `add-wheel-action-verbs` tasks 1.5–1.6 and
`add-ideation-intent-plane` task 2.4. The existing
`gate-action-record.schema.yaml` adds the human-only commission actions
`promote-to-staging`, `derive-possibles`, and `research-brief`, the
`cluster_id` target, verb-specific target requirements, and a required
`workflow-job` companion for each new action. The previously unpublished
`gate-intent.schema.yaml` is registered at the same wheel-expanded shape, so
request and applied-record vocabularies remain in lockstep. The growth is
additive, keeps `contract_schema_version: 1`, and invalidates no prior intent
or action record.

Realizes `add-worker-enrollment-broker` task 1.11 by registering the seven
contract-first worker schemas: enrollment request, lease, enrollment grant,
lease renewal, policy, audit record, and removal grant. Together they define
one enrollment point for fleet and volunteer estates, lease-based authority,
the minimum-app-version renewal floor, estate-specific runner packaging,
trust-tier segregation, transient registration/remove tokens, and
redaction-by-shape audit evidence. Consumers pin this release and run
`scripts/validate-worker-enrollment.py` from the pinned checkout; packaged
fixtures comprise 11 valid and 27 intended-invalid examples.

This release also corrects a catalog defect present in `contract-v1.27` AND
republished unchanged by `contract-v1.28`, without moving or rewriting either
immutable tag. The two doxBench wire schemas were mistakenly typed as Hermes
semantic `schema` members even though they do not carry the Hermes-only root
annotations, causing the Hermes catalog loader to reject the published
catalog. They are now `release-schema` members with `semantic_member: false`:
still closed and digest-pinned in the release inventory, but correctly
excluded from the Hermes semantic registry. Migration is to pin
`contract-v1.29` (the first release whose catalog loads cleanly); the doxBench
wire-schema bytes are unchanged.

Per-file sha256 inventory:
`contracts/releases/contract-v1.29.digests.yaml`.

## contract-v1.28 — 2026-08-02 (additive; the chat-turn request's `active_document_path` is nullable)

Cut in response to codexFactory PR #63 re-verification finding **G-1**
(reviewer Brett Heap, 2026-08-02): measured against the real corpus with
the consumer's own scope authority, 16 of 21 staged topics have exactly
ONE editable path — the topic's own primary fragment, which doxBench loads
as the OUTLINE — so requiring a non-null `active_document_path` made a
legal turn impossible on ~76% of real topics and the chat surface refused
on all of them. Strictly widening: every instance valid before this cut is
still valid.

- **`xfactory-workbench-chat-turn` request: `active_document_path` is
  nullable** (additive; no `contract_schema_version` bump). The request key
  stays REQUIRED and its value becomes `oneOf: [null, confined_path]`,
  mirroring `buffer_state.path` exactly — the same shape, for the same reason:
  a path that does not exist yet is `null`, never a fabricated string. Growth
  source: **G-1**, the codexFactory PR #63 re-verification finding (2026-08-02,
  reviewer Brett Heap), measured against the real corpus with the consumer's
  own scope authority — 16 of 21 staged topics have exactly ONE editable path,
  the topic's own primary fragment, which doxBench loads as the OUTLINE. With a
  non-null value required, no legal turn existed on ~76% of real topics and the
  chat surface refused on all of them. Realizes part of
  `add-workbench-integrated-editor-chat` task 2.5's contract package (see that
  change's ledger note); the consumer contract is codexFactory
  `specs/010-doxbench-editor-chat/contracts/chat-turn.md`.
  - Compatibility: strictly widening. Every instance valid before this change
    is still valid; no producer must change; a consumer that already handles
    `buffer_state.path: null` handles the same fact here. Domain repos pinned
    to `contract-v1.27` are unaffected until they choose to advance.
  - Rides with it: a new packaged positive example
    (`examples/ideation-dashboard/workbench-chat-turn-outline-only.example.yaml`
    — the outline-only turn) and two delegated-validator tests (a null
    `active_document_path` validates; an ESCAPING one is still refused). The
    delegated family validator needed no change: its `_confined` helper already
    judges only paths that exist, which is how `buffer_state.path` nullability
    landed.
  - **Operator's cut still owes:** the `contracts/manifest.yaml` per-file
    sha256 refresh for the amended schema (`validate-manifest-digests.py`
    currently reports 1/109 failing, by design in this pending state), the
    version allocation, the realized digest inventory, and the annotated tag —
    none of which a proposal may reserve ahead of merge order (Contract
    Versioning Policy, "Bundle Realization Order").

## contract-v1.27 — 2026-07-30 (additive; doxBench model-catalog and chat-turn wire contracts)

Realizes `add-workbench-integrated-editor-chat` task 2.5: the doxBench
contract-first package lands as two NEW canonical schemas —
`xfactory-workbench-model-catalog.schema.yaml` (the GET
/workbench/model-catalog success envelope; public seven-field allowlist,
structurally closed, empty-catalog = editor-only posture) and
`xfactory-workbench-chat-turn.schema.yaml` (the POST
/actions/workbench/chat-turn family: request / validated success / fixed
redacted failure, exact-UTF-8 SHA-256 content identity, non-identity
`working_subject`, closed envelopes throughout). Instance kinds use the
retained `workbench-*` identifier family (`workbench-model-catalog`,
`workbench-chat-turn`, `-success`, `-failure`) per the compatibility ruling;
file names carry the manifest's `xfactory-` artifact prefix. Six positive and
eight single-violation negative examples land under
`examples/ideation-dashboard/` (plus the duplicate-turn-id pair), and the
delegated family validator grows the catalog/request/success/failure and
turn-id-sweep rules with its own pytest suite
(`tests/ideation_dashboard/`). Existing dashboard/session artifacts remain
valid; no pre-growth snapshot or gate record is invalidated (task 2.4).
Per-file sha256 inventory: `contracts/releases/contract-v1.27.digests.yaml`.

## contract-v1.26 — 2026-07-30 (additive; ideation-dashboard workbench family registration)

Realizes the four predecessor registration tasks — `add-staging-workbench`
1.7, `add-workbench-bullseye-and-create` 1.6, `add-dashboard-repo-selector`
1.6, and `add-workbench-branch-sessions` 1.6 — as the family's first
`contracts/manifest.yaml` registration beyond the README doc index (the
ideation-possibles-register precedent, contract-v1.14). Per-file sha256
entries for `ideation-dashboard-snapshot.schema.yaml` (staged-topic growth,
add-staging-workbench), `gate-action-record.schema.yaml` (create/document
action growth, add-workbench-bullseye-and-create; branch-session verb growth
plus the D23 `provenance` block, add-workbench-branch-sessions 1.1/1.2/1.8),
and the NEW `ideation-dashboard-snapshot-index.schema.yaml` locator
(add-dashboard-repo-selector). README contract index rows updated. No schema
bytes change at this cut — the growth landed additively with its owning
changes; this cut registers the family's content-addressed identity in the
manifest. No `contract_schema_version` bump; the delegated strict validator
(`scripts/validate-ideation-dashboard-contracts.py`) stays content-addressed
by commit. The four owning task checkboxes remain open until this exact
candidate lands on published `origin/main` and the annotated tag verifies.

## contract-v1.25 — 2026-07-30 (additive; the semantic kernel publishes — the bootstrap window closes)

Realizes **publish-semantic-kernel** (ratified 2026-07-30): the first
governed publication of the xFactory semantic kernel. `xf/core` releases
0.1.0 → 1.0.0 (additive, same compatibility line) through
`ontology-release.py`, decided by the accountable
`openxfactory-maintainers` council — every one of the 25 concepts and 9 relations published with evidenced adoption (two independent resolvable
adopters each), the per-term steward act explicit under the F18 gate, the
package-level adoption block carried through the faithful rewrite (the
F21 kernel scenario in production), and both retained snapshots born
`lifecycle_state: superseded`. Published digest `37090ba2…369038`; the
three kernel registrations refresh accordingly. Spec delta: the
`xfactory-semantic-kernel` bootstrap allowance CLOSES — the active kernel
line never regresses to pending adoption; new terms in future revisions
may record pending only while their revision is unpublished. Consumers:
MedxFactory d01ae62 + codexFactory de60c0c re-pin `kernel_import` to the
published digest. No term's meaning changed: publication moved lifecycle
and version, never label, definition, parents, domain, or range.

## contract-v1.24 — 2026-07-30 (additive; ontology stewardship hardening — guarantees move from procedure to tool)

Realizes **add-ontology-stewardship-hardening** (ratified 2026-07-30), the
stewardship pass closing the domain-ontology release review's
carried-forward findings. Schema bytes: `ontology-stewardship-policy`
(a required quality signal declares `min_value` OR `max_value` — rate
ceilings are expressible directly, vacuous signals fail; F26) and
`ontology-starter-provenance` (the optional `placeholders` block —
readiness blocks on the structural record, never a name; F24). Rides the
same change without schema bytes: the starter's `--ontology-only`
adoption mode (v14; mature repositories adopt without the whole-repo
scaffold), the inventoried STARTER marker (deleting it breaks the package
digest; F25), release-tool housekeeping (faithful manifest rewrite incl.
`adoption`/`notes`, evidence-path containment, retained snapshots born
`lifecycle_state: superseded`; F21), the cadence-deadline rule, and
EXECUTED memory-gateway semantic conformance fixtures (probes run through
the canonical preflight or resolution-verified delegates; F27). Ontology
negative corpus 55. **This cut also delivers the contract-v1.23 erratum
correction**: `contracts/hermes-domain-overlay/content-manifest.schema.yaml`
now records its true digest in `contracts/manifest.yaml`
(`d45a8c89…`, stale v1.18→v1.23), and `scripts/validate-manifest-digests.py`
guards the consumption contract so the class cannot recur. First
consumers: MedxFactory f4ca313 + codexFactory 11777a9 (inventoried
markers).

## contract-v1.23 — 2026-07-30 (additive; omnigent semantic wiring — the worker seam closes)

> **Erratum (2026-07-30, recorded per the release review):** the bundle at
> tag `contract-v1.23` ships a stale digest inside `contracts/manifest.yaml`
> for `contracts/hermes-domain-overlay/content-manifest.schema.yaml`
> (`9511794f…`, stale since 403c2b5 — the add-domain-ontology-layer §4 edit
> that added the `domain_ontology` content kind; the schema's true digest is
> `d45a8c89…`). The tag itself is internally honest (its digest inventory
> matches its own bytes); the defect predates the bundle (carried
> v1.18→v1.23 because nothing verified `contracts/manifest.yaml` digests).
> Corrected in main at commit 792afd2, which also adds
> `scripts/validate-manifest-digests.py` so the class cannot recur; the
> correction rides the next bundle cut. Consumers verifying that schema
> against the v1.23 bundle's manifest should use the corrected digest.
> Note: `contracts/releases/*.digests.yaml` files are TAG SNAPSHOTS —
> verify them against their tag, not against a later HEAD.

Realizes **add-omnigent-semantic-wiring** (ratified 2026-07-30), the
follow-up named at add-domain-ontology-layer task 6.7: the two omnigent
schemas gain the worker semantic seam. `omnigent-domain-overlay` — a
worker class MAY declare `semantic_context: {profile_id, package_id}`
(identity only, authority-free; repo-mode resolution against the domain's
inventoried `xfactory_semantic_context_profile` documents with
worker_scope archetype-or-class agreement). `omnigent-install-manifest` —
optional `semantic_contexts` section pinning exact kernel + domain
ontology digests and one compiled `xfactory_semantic_context` artifact
per declaring worker (both-direction completeness and per-artifact
digest/pin/scope agreement via the canonical `install_wiring_errors`,
exercised by `scripts/test-omnigent-semantic-wiring.py`). Seam hardening
rides the same change without schema bytes: the context compiler refuses
drifted package bytes (review F20) and itemizes truncation transitively
with a validator completeness rule (review F19; ontology negative corpus
50). Permission matrices and the constitutional
`execute_final_action`/`access_secrets` booleans are untouched. First
consumer: MedxFactory 80a81af (two profiles, declarations on
`data_reverification_agent` and `case_framing_agent`, overlay-manifest
re-pinned); codexFactory and install repositories adopt through their own
governed changes.

## contract-v1.22 — 2026-07-29 (additive; domain-ontology family — the semantic plane lands)

Realizes **add-domain-ontology-layer** (ratified 2026-07-28): the
eighteen-kind `contracts/domain-ontology/` meta-contract (package manifest,
concepts, relations, external mappings, source inventory, candidate/release
records, migration map, semantic context + worker profile, quality report,
stewardship policy, maintenance input/report, review fixtures, coverage-gap
report, starter provenance, consumer-impact report) and the `xf/core`
semantic kernel (24 concepts, 9 relation primitives; every term carries its
owning contract and evidenced adoption; DRAFT pending the governed
publication decision). Meaning never authority: closed shapes, reserved
authority-name rejection, and the memory-gateway preflight keep the
semantic plane descriptive; grants/consent/approvals are untouched.
Canonical validator `scripts/validate-domain-ontology.py` (self-test: 8
positive units incl. the retained MedxFactory/codexFactory pilots and the
published-kernel adoption pair, 43 indexed negatives, determinism,
readiness); tools
`apply-domain-starter.py` (v13 ontology generation),
`ontology-maintenance.py`, `ontology-release.py` (accountable-steward
gate, per-signal quality exceptions, consumer-impact evidence, byte-true
self-retention), `ontology-compile-context.py`. Memory-gateway packet
contracts gain the closed `semantic_context` block (this bundle refreshes
`context-packet` / `expert-context-packet` and the layer-vocabulary role
text). First consumer: MedxFactory `hermes/domain/ontology/` (kernel
digest-pinned); codexFactory / hermes-install / omnigent adoption recorded
as explicit deferrals in the change's 8.6 evidence.

## contract-v1.21 — 2026-07-30 (additive; capability-steward contracts — the crystallization flywheel closes)

Realizes **add-capability-steward** (exit 3, closing the
`recurrence-crystallization` staged topic; ratified 2026-07-29, archived
2026-07-30): the seven **capability-steward** record schemas —
`contracts/schemas/{crystallized-capability-registry,dispatch-record,adjudication-record,sentinel-policy,capability-health-report,savings-entry,calibration-score}.schema.yaml`
— the registry record (proof-gated status spine mirroring the document
lifecycle; artifacts digest-pinned while authority is live-read, D10;
digests-never-payloads), the path-invariant dispatch record (six-cause
fallback taxonomy, metered overhead, pure/idempotent admission per D11),
the shared parity/sentinel adjudication record (bidirectional
verdict↔consequence pairing), the strictly-positive-floor sentinel policy,
the capability-health report (auto vs contested findings, cost-ordered
drift responses), and the sentinel-anchored savings entry with the
maturity-graded calibration score. The canonical validator
`scripts/validate-capability-steward.py` (11 named policy rules;
self-testing 6 positives / 10 indexed negatives) and
`examples/capability-steward/` (completing the MVP packet-capture corpus:
the full flywheel now runs in fixtures) are commit-content-addressed
tools and fixtures, no per-file digest. With `contract-v1.19`
(pattern-ledger) and `contract-v1.20` (crystallizer), all three
crystallization waves are canon. Purely additive.

## contract-v1.20 — 2026-07-29 (additive; crystallizer contracts + omnigent crystallized-executor extension)

Realizes **add-crystallizer-contracts** (exit 2 of the
`recurrence-crystallization` staged topic; ratified and archived
2026-07-29): the four **crystallizer** record schemas —
`contracts/schemas/crystallization-{decision,spec,build,consent}.schema.yaml`
— the decision as the only path from candidate to spend
(ceilings-before-valuation, deflation + survival discounting,
shape-not-boolean outputs, the not-yet ledger, frozen L0–L6 rung
vocabulary), the episode-mined micro-spec (acceptance corpus with declared
equivalence predicates, scope fence, effect class), the governed build
record (gapless provenance, dry-run + leak-scan acceptance, declared
artifact residence per the rung→home lean), and the three-tier
default-deny consent grant. Also extends **`omnigent-domain-overlay`**
additively (manifest digest refreshed): the crystallized-executor binding
on the EXISTING five archetypes — so the constitutional matrix binds
verbatim — and per-category `rung_ceilings` with the conservative L3
default, enforced by the extended `scripts/validate-omnigent-contracts.py`
(authority-conservation subset rules: permissions and by_class credential
families never exceed the replaced configuration). The canonical validator
`scripts/validate-crystallizer-contracts.py` (12 named policy rules;
self-testing 4 positives / 9 indexed negatives) and
`examples/crystallizer/` are commit-content-addressed tools and fixtures,
no per-file digest. Purely additive.

## contract-v1.19 — 2026-07-29 (additive; pattern-ledger sensing contracts + derived-model registration catch-up)

Realizes **add-pattern-ledger** (exit 1 of the `recurrence-crystallization`
staged topic; ratified and archived 2026-07-29): the five **pattern-ledger**
record schemas —
`contracts/schemas/pattern-ledger-{episode,outcome-label,recurrence-family,recurrence-forecast,crystallization-candidate}.schema.yaml`
— episodes as derived projections over existing audit/run/metering/label
streams with explicit default-deny consent tiers; append-only outcome
labels (quality is a fold, never a stored verdict); tenant-scoped
recurrence families with recorded merge/split transitions; maturity-dated,
scored forecasts with declared cost-regime assumptions; and the
nominate-never-spend crystallization candidate. The canonical validator
`scripts/validate-pattern-ledger.py` (nine named policy rules; self-testing
7 positives / 7 indexed negatives) and `examples/pattern-ledger/` (incl.
the MVP packet-capture fixture corpus hand-derived from the real
2026-07-28/29 runs) are commit-content-addressed tools and fixtures, no
per-file digest. Purely additive.

Also registers **`xfactory-derived-model-conformance`**
(`contracts/schemas/xfactory-derived-model-conformance.schema.yaml`),
realized 2026-07-23 by archived `add-governed-derived-model` but missed by
the v1.16–v1.18 cuts — the standing Unreleased note is discharged by this
cut. DTN-014 flips `implemented` → `adopted` in the candidate register as
domain pins advance past this registering ref.

## contract-v1.18 — 2026-07-24 (additive; domain content manifest + memory binding)

Realizes **add-hermes-domain-content-manifest** (seeding increment 4b's
contract half; convention-then-contract): the optional
**`hermes_domain_content_manifest`**
(`contracts/hermes-domain-overlay/content-manifest.schema.yaml`) — a domain
repo declares its seedable content set per ratified `content_kind` (exactly
one of `path`/`directory`; absent manifest, consumers keep the documented
increment-4a convention; an undeclared kind never loads silently) — and the
**`hermes_memory_binding`** record shape
(`contracts/memory-gateway/memory-binding.schema.yaml`), formalizing the
derived binding hermes-install increment 3 materializes: rails input in the
ratified gateway vocabulary (promotion gateway constitutionally
`customer_memory_gateway`, `accepted_authority_level` drawn from
`authority_levels`), never a provider binding — any provider/credential
surface fails the canonical validator. Realization anchors: the codexFactory
conventional set declared verbatim; the two LIVE-derived opensoft bindings
as the packaged example. Purely additive.

## contract-v1.17 — 2026-07-23 (additive; client-content tuning surface)

Realizes **add-client-layer-tuning-contracts** (phase 2a of the layer
activation path): the neutral tenant-layer contract set — three client
content kinds (`client_policy_overrides` with stricter_only + budget
envelopes + tracking granularity + the human-ratified auto-clear envelope,
`client_memory_boundaries` with the tenant_isolated invariant,
`client_integration_boundaries` reference-only) and the seedable
**`hermes_client_overlay`** (canonical path
`config/clients/<client_ref>/overlay.yaml`, descriptor-declared,
`client_overlays[]`-pinned). Canonical validator
`scripts/validate-client-content.py` implements the stricter-only
comparability spec with a `review_required` fallback and self-testing
fixtures. Also in this bundle: the neutral house-team roster
(`templates/client-layer/roles/` — 10 deciders incl. the Finance &
Accounting Officer + the liaison capability, voice floor locked) and the
scaffold's `cost_reporting_steward`. Purely additive.

## contract-v1.16 — 2026-07-23 (additive; omnigent contract family + layer vocabulary)

Tenth annotated-tag release. Realizes **add-omnigent-domain-overlay** (the
Omnigent execution layer's domain-tier contracts) and registers
**adopt-subject-tenant-domain-vocabulary**'s policy artifact:

- `contracts/omnigent/omnigent-domain-overlay.schema.yaml` — per-domain
  overlay payload: worker classes mapped to the five neutral archetypes
  (frame/generate/verify/challenge/assemble_for_admission), the generalized
  six-boolean permission matrix with constitutional
  `execute_final_action`/`access_secrets` `const: false`, four credential
  tiers including `never_assignable`, domain-level permission aliases,
  whole-document `worker_profiles` payload, `stricter_rule_wins`
  composition under the `domain_installation_overlay` operations.
- `contracts/omnigent/omnigent-install-manifest.schema.yaml` — the install
  manifest: hermes-install rendered runtime manifest digest-pinned as the
  single stack identity (no parallel identity by construction), exactly one
  domain overlay, the authoritative subject-workload registry, pre-rendered
  effective-profile provenance. First family with canonical
  Subject/Tenant/Domain machine spellings from birth.
- `contracts/policies/layer-vocabulary.yaml` — the ratified canonical layer
  vocabulary: names + roles, the customer→subject / client→tenant legacy
  mapping, reserved layer terms, the frozen-identifier inventory (migration
  staged dormant at `ideation/staging/layer-vocabulary-machine-migration/`),
  and the per-domain alias table.

Canonical validator `scripts/validate-omnigent-contracts.py` with packaged
examples and marked negative fixtures (commit-content-addressed tools, no
per-file digest). Realization evidence: canonical domain overlays in
codexFactory (`engineering-omnigent-overlay`) and MedxFactory
(`medical-omnigent-overlay`); Omnigent-Install's live manifest with
fail-closed compose/verify, byte-equivalent rendered coding-patch-worker
binding, and the MedxFactory second-domain params fixture. All additive:
every released path from `contract-v1.7` through `contract-v1.15` is
byte-identical.

## contract-v1.15 — 2026-07-23 (additive; hermes-domain-overlay contract surface)

Ninth annotated-tag release. Realizes **add-hermes-domain-overlay-contract**:
the neutral `hermes_domain_overlay` schema (domain identity, non-empty
approval scopes and required fields, authority boundaries with the
canonical-validator-enforced `<domain.id>_owns` naming and no-overlap rules)
and the `hermes_overlay_descriptor` role→path declaration (runtime layer
roles domain/client/customer as keys — deliberately not directory names —
with a documented-convention fallback when absent and fail-closed dangling
paths). New canonical validator `scripts/validate-hermes-domain-overlay.py`
with self-testing packaged examples/negatives under
`contracts/hermes-domain-overlay/examples/`. Realization proof: codexFactory's
live 37-authority `hermes/domain/overlay.yaml` passes unmodified via the
convention fallback. Replaces the hermes-install seeding runtime's minimal
structural check at its materialization increment (which pins this release).
Purely additive; no existing contract touched.

## contract-v1.14 — 2026-07-22 (additive; possibles-register AI-derivation intake)

Eighth annotated-tag release. Realizes the **possibles-derivation lane's
contract surface** (`add-possibles-derivation-lane`, task 2.6 registration at
the realization commit): the ADDITIVE AI-derivation intake delta on the
`ideation-possibles-register` kernel — optional `register_entry.origin`
(enum `[human-authored, ai-derived]`; absent defaults to human-authored),
optional `register_entry.derivation` (worker-run identity: correlation id /
worker profile / prompt-contract version, plus machine
`disposition: pending_review` and the `derivation_human_disposition` local
mirror of the index's `human_disposition`), and the `allOf` conditional that
requires `derivation` when `origin: ai-derived`. Modelled one-for-one on the
index topic entry's `origin` + `human_seen` intake pair; the conditional
never fires on an origin-absent entry, so `contract_schema_version` stays 1
per the kernel's additive-growth rule and every released path from prior
bundles is byte-identical.

Registered — `contracts/schemas/ideation-possibles-register.schema.yaml`
(per-file SHA-256 recorded in `contracts/manifest.yaml`; the kernel's first
manifest registration — the ideation-dashboard family was previously
registered in `contracts/README.md`'s doc index only). Packaged examples:
`examples/ideation-dashboard/derived-possible-register.example.yaml` plus
the derived negatives and one-way-disposition transition pairs, all enforced
by the delegated strict register validator
(`scripts/validate-ideation-dashboard-contracts.py`, extended at task 2.4).

Realization evidence: codexFactory `specs/004-derive-possibles` — the
derive-possibles worker (PR #25), the nightly lane + watchdog + rolling-PR
register commit-back (PR #27), and the omnigent-install `derive-possibles`
worker profile (Omnigent-Install PR #22, contract-only until host
deployment). The nightly lane reports SKIPPED until a host advertises the
profile — the readiness-scorer precedent's valid landed state.

## contract-v1.13 — 2026-07-17 (additive; client-infrastructure-request contract family)

Seventh annotated-tag release. Realizes the neutral **client-infrastructure
contract family** (`add-client-infrastructure-liaison`): the durable
`client_infrastructure_request` coordination record, the signed/traceable
`infrastructure_readiness_result` artifact, and their strict openxFactory
validator, promoted at this change's archival (task 5.1) out of the "Contracts
Pending Realization" holding area that task 2.5 added to `contracts/README.md`.
All additive: every `contract-v1.7` / `v1.8` / `v1.11` / `v1.12` released path
is byte-identical and `contract_schema_version` is unchanged.

Added — two `contracts/schemas/xfactory-*.schema.yaml` contracts
(YAML-serialized JSON Schema draft 2020-12, `contract_schema_version: 1`;
per-file SHA-256 recorded in `contracts/manifest.yaml`):

- `xfactory-client-infrastructure-request.schema.yaml` — the
  `client_infrastructure_request` durable coordination record (never a Hermes job
  envelope): six never-conflated identity-reference `$defs`, the three-mode
  `execution_binding` (`client_managed|managed_host|opsxfactory_executed`, design
  D1), the closed 13-state `status` enum, orthogonal `conditions[]`, the embedded
  `handoff` acceptance record, digest-bearing `package_refs`, cancellation
  `child_acks`, and `supersedes_request_ref`.
- `xfactory-infrastructure-readiness-result.schema.yaml` — the
  `infrastructure_readiness_result` signed/traceable readiness artifact, never a
  bare boolean: status `ready|degraded|not_ready|unknown|maintenance`,
  `valid_until` freshness, non-privileged validator + trust refs, per-check
  `mandatory`/`outcome`/evidence, and `evidence_digest`.

Also added — `scripts/validate-client-infrastructure.py`: strict validator for
both kinds — schema conformance, embedded-secret rejection (shared avatar-client
denylist), transition legality including terminal immutability and
readiness-gated completion, identity-class separation (actor ≠ authority ≠
creating liaison; a subject id never in a typed field), idempotency/supersedes
integrity, and cancellation-acknowledgment presence — self-testing the packaged
reference examples (`examples/client-infrastructure/`: 4 valid + 9
one-violation-each negatives). Registered as a tool and content-addressed by
commit; not a pinned semantic artifact, so excluded from the per-file digest set.

Governance:

- The liaison and no domain agent ever holds tenant-administration authority; an
  `infrastructure_readiness_result` is never a bare boolean and gates a
  `client_infrastructure_request` completion only when fresh (used before
  `valid_until`), overall `ready`, and every mandatory check passes. The governing
  role doc `docs/client-infrastructure-liaison.md` is ratified alongside this
  change (`Status: ratified`; `Ratified by: add-client-infrastructure-liaison`),
  with product-owner sign-off on design D1 (execution-binding tokens) and D5
  (roles-authority wording) recorded by Brett 2026-07-16 (task 4.1). It is prose
  governed by this changelog, not a per-file manifest member.
- Fail-closed validation: `scripts/validate-client-infrastructure.py` self-test
  confirms 4 valid examples and 9 negatives each failing for its intended reason;
  `OPENSPEC_TELEMETRY=0 openspec validate add-client-infrastructure-liaison
  --strict` is green. The reference validator is content-addressed by commit and
  carries no per-file digest.

Also added — `contracts/releases/contract-v1.13.digests.yaml`: the raw-Git-blob
SHA-256 release digest inventory for this bundle (built by
`scripts/validate-contract-release.py`), refreshing the closed hermes-runtime
release surface plus the `manifest.yaml` / `CHANGELOG.md` / `README.md`
auxiliaries; the client-infrastructure family is outside that closure and is
content-addressed via `manifest.yaml` per-file digests instead.

Consumers: the per-domain adoption successors (OpsxFactory binding/readiness
producer first, then the Medx/Ledger/Ad/codex aliases) pin this bundle at the
`contract-v1.13` tag and verify the per-file SHA-256 in `manifest.yaml` before
treating a copy as current; openxFactory ships no instance records (they live in
client installs, credential-contracts residency model).

## contract-v1.12 — 2026-07-15 (additive; avatar-client-lab evidence surface / P-row adoption)

Sixth annotated-tag release. Realizes the neutral **avatar-client-lab evidence
surface** (`adopt-avatar-client-lab-candidates`), the P1/P10 owning change that
adopts the panel-confirmed layer-2 evidence candidates from codexFactory
`002-avatar-client-lab` @ `3a8fbd5` (7/7 confirmed; provenance in that feature's
`upstream-drafts/STATUS.md`). All additive: every `contract-v1.7` / `v1.8` /
`v1.11` released path is byte-identical and `contract_schema_version` is unchanged.

Added — two neutral, content-addressed client-lab artifacts under
`contracts/avatar-client-lab/` (per-file SHA-256 recorded in
`contracts/manifest.yaml`):

- `avatar-state-derivation-table.yaml` — the P1 total avatar-state derivation
  table (design D3): the precedence-ordered R0..R6 derivation plus the enumerated
  healthy-control matrix mapping the four authoritative runtime axes onto the six
  FR-019 avatar presentation states, embedding the normative invariants, with
  OQ-1..OQ-6 ratified (product-owner sign-off Brett 2026-07-15). Gate
  (vi)/(ix)(a) source. Its normative `.md` companion
  (`avatar-state-derivation-table.md`) and `README.md` are prose governed by this
  changelog, not per-file manifest members.
- `capability-scenario-register.yaml` — the P10 capability-scenario register
  (9 requirements / 22 scenarios; Option B, design D2): stable `ACL-*` ids and
  verbatim `#### Scenario:` titles machine-checked fail-closed in document order
  against the `implement-avatar-client-lab` capability spec. Gate (ix)(b) source.

Added — the 20 adopted deterministic fixtures under
`examples/avatar-first-ui/fixtures/deterministic/` (per-file SHA-256 in
`manifest.yaml`), closing the state-reachability denominator via AVC-12 kernel
fields only: P7 intake breadth (5), P8 lease/epoch takeover + snapshot-barrier
recovery (4), P11 `interrupted`/`handoff` (2), and P12/P13 the eight non-control
closed `media.states` + `control_degraded` (9). The five pre-existing released
seeds already in that directory stay unregistered (not this change's members).

Added — `contracts/avatar-client/evidence-register.implement-avatar-client-lab.yaml`,
the SCO-001-S05 successor deferral-discharge register (locked decision 7 of
`implement-avatar-client-lab`, task 4.4). Registering it here — the release-time
manifest convention first used at `contract-v1.9` (bundle members join
`manifest.yaml` only when the next additive version is cut, never mid-change) —
makes the `deferred → evidenced` discharge effective WITHOUT mutating the
released, byte-identical `evidence-register.yaml` (a contract-v1.9 member).

Governance:

- Settled law L2 (the app never self-serves neutral artifacts): all candidates
  land at their upstream openxFactory source; the codexFactory
  `apps/avatar-client-lab/` app consumes them read-only as
  `vendored_evidence_inputs` at its `contract-v1.12` pin resync (this change's
  codexFactory realization surface).
- Fail-closed validation: `scripts/validate-avatar-client.py` carries
  `check_avatar_state_derivation_table` and `check_capability_scenario_register`
  (both fail-closed, with negative coverage); with the successor register now
  manifest-listed, `--require-realization` passes (0 errors).
  `scripts/validate-avatar-first-ui.py` (baseline + realization) stays green. The
  reference validators are content-addressed by commit and carry no per-file digest.

Also added — `contracts/releases/contract-v1.12.digests.yaml`: the raw-Git-blob
SHA-256 release digest inventory for this bundle (built by
`scripts/validate-contract-release.py`), refreshing the closed hermes-runtime
release surface plus the `manifest.yaml` / `CHANGELOG.md` / `README.md`
auxiliaries; the avatar-client-lab surface is outside that closure and is
content-addressed via `manifest.yaml` per-file digests instead.

Consumers: the codexFactory `apps/avatar-client-lab/` lab pins this bundle at
the `contract-v1.12` tag and verifies the per-file SHA-256 in `manifest.yaml`
before treating a vendored copy as current.

## contract-v1.11 — 2026-07-14 (additive; document-cataloging contract surface)

Fifth annotated-tag release. Realizes the neutral **document-cataloging
contract surface** (`add-document-cataloging`): six domain-neutral JSON-Schema
contracts plus their strict openxFactory validator, promoted at this change's
archival (task 8.7) out of the "Contracts Pending Realization" holding area
that task 2.4 added to `contracts/README.md`. All additive: no existing
contract path changes and `contract_schema_version` is unchanged.

Added — six `contracts/schemas/xfactory-document-*.schema.yaml` contracts
(YAML-serialized JSON Schema draft 2020-12; per-file SHA-256 recorded in
`contracts/manifest.yaml`):

- `xfactory-document-catalog-snapshot.schema.yaml` — immutable per-repository
  document-catalog snapshot.
- `xfactory-document-cataloger-recommendation.schema.yaml` — immutable,
  non-authoritative cataloger-recommendation evidence.
- `xfactory-document-tag-registry.schema.yaml` — namespaced topic-tag registry.
- `xfactory-document-tag-overrides.schema.yaml` — owner override / disposition
  file.
- `xfactory-document-opaque-locator.schema.yaml` — reusable canonical/opaque
  document-locator `$defs` kernel.
- `xfactory-document-handling-gate.schema.yaml` — reusable dispatch/handling-gate
  decision `$defs` kernel.

Also added — `scripts/validate-document-catalog.py`: strict validator over the
packaged reference examples (`examples/document-cataloging/`) and the
deterministic cross-cutting invariants JSON Schema alone cannot express
(complete coverage, unique per-snapshot identity, source and review freshness,
taxonomy resolution, override standing, immutable path layout, and the
disclosed baseline-mode coverage exception). Registered as a tool and
content-addressed by commit; not a pinned semantic artifact, so excluded from
the per-file digest set.

Governance:

- Catalog facets are descriptive discovery metadata only: they never set a
  document's lifecycle `Status:`/`Kind:`, ownership, routing state, `xspec:`
  markers, sensitivity approval, or lifecycle changes (see
  `docs/document-lifecycle.md` "Catalog Tags Are Not Lifecycle State" and the
  `document-catalog` family in `docs/doc-health.md`). The adoption guide
  `docs/document-catalog-adoption.md` is ratified alongside this change.
- Realization evidence: the deterministic mechanical baseline covers 225/225
  governed v1 documents across six repositories (xFactory aggregation
  `800a572`), byte-equal to the freshly built extended inventory with zero
  source edits and reproduced identically across two from-scratch runs; strict
  `validate-document-catalog.py` reports 0 errors / 0 warnings against the real
  artifacts and 661/661 codexFactory tests pass at the merged SHA; the
  codexFactory `document-catalog` doc-health family and the non-authoritative
  document-cataloger lane landed in codexFactory PR #4 / PR #6, and the bounded
  read-only cataloger worker profile in omnigent-install `b836a24`.

- Nightly evidence (workflow runs 29328943314 and 29330008234, 2026-07-14):
  the first post-baseline nightly produced the dated report
  `health/reports/2026-07-14.md` (xFactory aggregation `97c4754`) with a
  rendered "Document Catalog" section — 225 of 225 docs cataloged, facet
  states pending=1350 (all other states 0), changes 225 new / 0 changed /
  0 deleted / 0 stale / 0 rejected, classifier `document-cataloger/1`
  prompt contract v1, cataloger skipped fail-closed with
  `runner_labels_missing` (the document-cataloger profile is not yet
  deployed to the artifact-worker host) — and the immutable snapshot at
  `health/document-catalog/runs/2026-07-14/ee0b0ab6…/`. The
  `document-catalog` family contributed zero findings at static pins
  (run 29328943314); run 29330008234's 32 auto-fixable stale-entry
  findings were the ratified freshness contract firing on an unrelated
  mid-window codexFactory pin move, self-healed by the landed snapshot.
  No catalog recommendation entered the Ranked Plan and no catalog-caused
  critical/error regression was introduced.

Consumers: every DomainxFactory pins this bundle at the `contract-v1.11` tag
and verifies the per-file SHA-256 in `manifest.yaml` before treating a copy as
current; the codexFactory `document-catalog` doc-health family and the
document-cataloger worker consume the schemas and validator from their pinned
openxFactory checkout.

## contract-v1.10 — 2026-07-14 (additive; superseding hardening of the neutral Hermes customer-subject runtime, provider side)

Fourth annotated-tag release. A **superseding additive re-realization** of the
provider-side neutral Hermes customer-subject runtime family first cut at
`contract-v1.9`. Per the Immutable Tag Correction policy, the `contract-v1.9`
annotated tag and its digest inventory
(`contracts/releases/contract-v1.9.digests.yaml`) remain in place as immutable
provenance; this bundle carries the corrected bytes under the next available
version. No contract shape changes: `contract_schema_version` is unchanged,
every v1 contract path is untouched, and any consumer that pinned
`contract-v1.9` remains conformant until it deliberately upgrades.

Why a superseding release: after `contract-v1.9` was tagged, two governed
review findings hardened release-surface members, so the frozen v1.9 digest
inventory no longer reproduced the current tree (expected drift, not a defect):

- **F-U3** (`Harden release membership closure`) made the Decision-10 mandatory
  release auxiliaries unconditional members of the closed bundle (no
  `exists()` gate) and repaired two release-fragile tests, changing
  `scripts/hermes_runtime_validation/release.py` and the six
  `contracts/hermes-runtime/fixtures/release/*.yaml` inventory fixtures.
- **F-4 / F-7..F-9** (`Harden migration digest surface`) changed
  `contracts/hermes-runtime/hermes-operational-postgres-v2.sql`.

This release refreshes the raw-Git-blob release digest inventory over the
current bytes and re-establishes manifest/changelog/tag/inventory agreement.

Host-local metadata removal (FR-042): `contracts/manifest.yaml`
`source_compatibility_ref.local_source_path` — a host-absolute developer path
(`/home/brett/...`) — is removed in this additive bundle after the recorded
repository-wide supported-consumer audit
(`openspec/changes/add-hermes-customer-subject-runtime-contract/evidence/legacy-source-path-consumer-audit.md`,
`Status: record`) proved no supported consumer requires it. Canonical source
repository and source-commit provenance are retained; no consumer, validator,
or DomainxFactory `stack.yaml` resolved the removed field.

Gate G0 remains OPEN: the exact downstream `opensoft/xFactory-Hermes-Install`
consumer pin and its reproduced digests are required to close it and are owned
by that repository's own feature.

Changed:

- `contracts/manifest.yaml` — `contract_bundle_version` -> `contract-v1.10`;
  `source_compatibility_ref.local_source_path` removed (audited; provenance
  `repo`/`source_commit` retained).
- `contracts/releases/contract-v1.10.digests.yaml` — new realized release
  digest inventory (raw Git blob SHA-256; bytewise-`utf8` path order;
  self-excluded and commit-free) for this bundle.
- The `contracts/hermes-runtime/` family,
  `scripts/hermes_runtime_validation/`,
  `scripts/validate-hermes-runtime-contracts.py`,
  `scripts/validate-contract-release.py`, and the hermes-runtime docs are the
  realized surface (governed by `contracts/hermes-runtime/contract-index.yaml`;
  not tracked per-file in `manifest.yaml`), carrying the F-U3 and
  F-4/F-7..F-9 hardening above.

## contract-v1.9 — 2026-07-14 (additive; neutral Hermes customer-subject runtime, provider side)

Third annotated-tag release. Realizes the **provider side** of the neutral
Hermes customer-subject runtime contract family
(`add-hermes-customer-subject-runtime-contract`, feature
`005-customer-subject-runtime`): the domain-neutral customer-subject topology,
trusted-scope authority/binding/approval/traceability records, the PostgreSQL
15/16 operational contract with the governed v1-to-v2 migration and quarantine,
the scoped v2 job/run/event lifecycle, the supported-DomainxFactory regression
denominator, and this bundle's own raw-Git-blob release digest inventory plus
the consumer handoff receipt. All additive: existing v1 contract paths and
pinned consumers are unchanged.

This is the first release to carry a canonical release digest inventory
(`contracts/releases/contract-v1.9.digests.yaml`, schema
`contracts/releases/release-digest-inventory.schema.yaml`): raw Git blob
SHA-256 over every required semantic member, bytewise-`utf8` path order, the
inventory self-excluded and carrying no commit (the annotated tag anchors the
commit; a downstream consumer manifest pins the inventory digest externally).

Gate G0 remains OPEN: the exact downstream `opensoft/xFactory-Hermes-Install`
consumer pin and its reproduced digests are required to close it and are owned
by that repository's own feature.

Changed:

- `contracts/manifest.yaml` — `contract_bundle_version` -> `contract-v1.9`.
- `contracts/releases/contract-v1.9.digests.yaml` — new realized release digest
  inventory for this bundle.
- The `contracts/hermes-runtime/` family, `scripts/hermes_runtime_validation/`,
  `scripts/validate-hermes-runtime-contracts.py`,
  `scripts/validate-contract-release.py`, and the hermes-runtime docs are the
  realized surface (governed by `contracts/hermes-runtime/contract-index.yaml`;
  not tracked per-file in `manifest.yaml`).

## contract-v1.8 — 2026-07-13 (additive; avatar-first UI profile-schema alignment)

Second annotated-tag release. Realizes the **avatar-first UI standard alignment**
(`align-avatar-first-ui-standard`), aligning the domain-neutral
`avatar-first-ui-profile` schema to the released avatar-client (AVC) contract
kernel. This release consumes the `contract-v1.7` kernel **read-only** — each
profile's `runtime_compatibility` pins the kernel bundle tag, exact commit
`ddff475`, and per-file registry/interface-lock SHA-256 digests; no kernel file
is changed.

Changed:

- `contracts/schemas/avatar-first-ui-profile.schema.yaml` — AVC-aligned additive
  OPTIONAL blocks with closed (fail-closed) defaults (`runtime_compatibility`,
  `presentation`, `media`, `outcome_slots`, `fallback_slots`, `interaction_mode`,
  `speech_gate`, `timing`, `consent_purpose_mappings`, `persona_reference`,
  `retention_overlay`, `accessibility_baseline`, `handoff`). Top-level `required`
  keys unchanged; backward compatible. Per-file SHA-256 recorded in
  `contracts/manifest.yaml`.

Governance:

- Offline realization gate `scripts/validate-avatar-first-ui.py --mode realization`
  loads the released kernel registries read-only and fails closed
  (`AFUV-RUNTIME-DRIFT`) on any baseline drift or `runtime_compatibility`
  digest/tag/commit mismatch. The standard doc is ratified
  (`docs/avatar-first-ui-standard.md`; `Ratified by: align-avatar-first-ui-standard`).

Consumers: DomainxFactory repos pin this bundle at the `contract-v1.8` tag and
verify the profile-schema SHA-256 in `manifest.yaml` before treating a copy as
current.

## contract-v1.7 — 2026-07-12 (additive; first annotated-tag release)

First contract release published under mandatory annotated-tag enforcement
(Contract Versioning Policy). Realizes the neutral **avatar-client (AVC)
contract kernel** (`define-avatar-client-contract-kernel`) after the F0
brokered-call feasibility gate passed — 70/70 live trials, client-enforced
revocation (`qualify-avatar-brokered-call-feasibility`, harness commit
`5142065`).

Added — `contracts/avatar-client/` (23-file semantic set; per-file SHA-256
recorded in `contracts/manifest.yaml`):

- `shared-definitions.schema.yaml` plus eight `avc-*.schema.yaml` contracts
  (AVC-01/02/04/06/07/08/11/12) — YAML-serialized JSON Schema draft 2020-12.
- Nine closed registries under `registries/` (session-result-reasons = 15,
  consent-purposes = 3, events, commands, capabilities, fallback-modes,
  interaction-modes, retention-classes, session-outcomes).
- `acceptance-map.yaml`, `interface-lock.yaml` (frozen
  `avatar-client-parallel-v1` baseline + fail-closed F0 publication-gate pin),
  `evidence-register.yaml`, and the `fixtures/` conformance set
  (`index.yaml`, `f0-gate-cases.yaml`).
- `scripts/validate-avatar-client.py` — reference validator carrying the
  fail-closed F0 publication gate (content-addressed by commit; not a pinned
  semantic artifact, so excluded from the digest set).

Governance:

- ACR-005 revocation clarified to **client-enforced within the 5 s bound**
  (`change/clarify-avatar-revocation-client-enforced`); provider-side settle is
  recorded informationally. The registered avatar-client threat model is
  accepted.

Consumers: the avatar-client reference runtime (003) and avatar-first UI
standard (004) siblings pin this bundle at the `contract-v1.7` tag and verify
the per-file digests before treating a copy as current.

## contract-v1.6 — 2026-07-09 (additive)

Added:

- `contracts/schemas/xfactory-credential-contracts.schema.yaml` — the five
  credential record shapes promoted from OpsxFactory evidence
  (promote-credential-contracts change; DTN-004).
- `scripts/validate-credential-contracts.py` — canonical credential
  contract validator.

## contract-v1.5 — 2026-07-09 (loosening, backward compatible)

Changed:

- `contracts/schemas/hermes-job-envelope.schema.yaml` — neutralized
  (neutralize-job-envelope change; DTN-003): `repository` and `feature_id`
  now optional, `job_type` a domain-owned string, new optional neutral
  references (`domain`, `subject_ref`, `client_ref`, `workflow_ref`,
  `focal_item_ref`, `gate_ref`, `artifact_refs`). Engineering strictness
  moves to codexFactory's engineering-job-envelope overlay.
- `contracts/schemas/hermes-job-run.schema.yaml` — `feature_id` optional.
- `contracts/schemas/hermes-job-event.schema.yaml` — unchanged (already
  neutral; lifecycle enums are domain-neutral vocabulary).

## contract-v1.4 — 2026-07-09 (additive)

Added:

- `contracts/schemas/xfactory-workflow.schema.yaml` — neutral workflow
  contract and gate record/blocking vocabulary promoted from four-domain
  evidence (promote-workflow-gate-contract change; DTN-001, DTN-002).
- `scripts/validate-workflow-contracts.py` — canonical workflow contract
  validator (errors for structure, warnings for undeclared owner layers,
  out-of-scope kinds skipped with notice).

## contract-v1.3 — 2026-07-09 (additive)

Added:

- `contracts/schemas/xfactory-domain-stack.schema.yaml` — optional
  `xfactory.promoted_from` and `xfactory.specializes` promotion-provenance
  fields (refine-promotion-provenance change). Backward compatible; existing
  stacks remain valid.

## contract-v1.2 — 2026-07-03 (additive)

Added:

- `contracts/memory-gateway/` — canonical xFactory Memory Gateway contract
  surface for Customer Hermes memory and Domain Omnigent expert
  memory/knowledge access. Includes vocabularies, consent profile, gateway
  request/response, provider profile, binding, mapping, subject safety,
  context packet, expert context packet, expert source, promotion, migration,
  usage, revocation, erasure, break-glass, and audit event schemas.
- `scripts/validate-memory-gateway.py` — canonical validation for gateway
  contracts, provider profiles, conformance fixtures, domain examples, and the
  first local runtime smoke path.

## contract-v1.1 — 2026-07-03 (additive + deprecating)

Added:

- `contracts/schemas/xfactory-domain-stack.schema.yaml` — canonical
  stack.yaml shape. Introduces `hermes.layers`: an ordered list of authority
  layers each bound to a canonical role (`customer` = served subject,
  `client` = tenant/operator organization, `domain` = reusable expert
  domain, `extension` = declared intermediate layer with authority_scope).
  Fixes the cross-domain vocabulary collision where "Client Hermes" meant
  the subject layer in some domains and the tenant layer in others.
- `scripts/validate-domain-factory.py` — canonical conformance validator,
  consumed (not copied) by domain repos. Replaces per-domain hand-rolled
  validators as the conformance baseline; domain validators may extend it.
- `docs/contract-versioning-policy.md` and this changelog.

Deprecated (warnings, removal at contract-v2.0):

- `hermes` flat keys (`subject_overlay`, `subject_layer_name`,
  `care_organization_overlay`, flat `client_overlay`/`customer_overlay`
  styles) in favor of `hermes.layers`.
- `openworkflow_*` owner/layer tokens in workflow gates in favor of
  `xfactory`.

## contract-v1.0 — 2026-06-26 (baseline)

- Initial canonical contract set migrated from install repos: job
  envelope/event/run schemas, clarification packets, avatar-first UI
  profile, domain installation overlay, governance and merge-risk
  policies, hermes operational Postgres DDL.
