# Clarify Questions: 004-avatar-first-ui

**Spec**: [spec.md](./spec.md)
**Source**: OpenSpec change `align-avatar-first-ui-standard` (ratified-grade)
**Generated**: 2026-07-11
**Status**: Answered inline; `spec.md` remains unchanged for the track agent to update.

**Question count**: 8


## Accepted Answers

**Answered**: 2026-07-10 (America/Los_Angeles)

**Decision summary**: `Q1=A; Q2=A; Q3=A; Q4=A; Q5=Custom; Q6=A; Q7=A; Q8=A`.

### Q1: A

The UI profile carries only a persona reference: stable persona ID, version,
and an optional non-secret catalog locator. The persona-catalog schema and
instances remain domain/kernel-owned and out of scope. Resolution failures are
fail-closed and use an approved fallback; the UI never invents persona data.

### Q2: A

Publish a domain-neutral `confirmation-before-consequential-action` archetype
using neutral vocabulary. Ledgerx is inspiration only; no accounting-specific
fields or examples belong in openxFactory.

### Q3: A

Publish versioned YAML/JSON fixture files under
`examples/avatar-first-ui/fixtures/`, separate from profile examples. Each
fixture carries fixed clock/ID/font/locale/platform inputs, canonical
command/event/snapshot inputs, expected view-state/record shapes, and its AFU
evidence IDs. The offline validator checks them.

### Q4: A

The profile carries selected readiness, heartbeat, and lease values. Numeric
ceilings remain kernel-owned and are loaded read-only by the validator from the
parallel baseline during development and released registries at realization.
Do not hardcode duplicate maxima in the UI profile schema; missing or
unresolvable bounds fail closed.

### Q5: Custom - exact coordinates, no released ranges

During parallel work, runtime compatibility records the exact
`avatar-client-parallel-v1` baseline identity and required baseline digests. At
realization it records the released bundle tag, exact commit, and required
registry/interface-lock digests and validates every referenced ID against those
bytes. Do not permit a loose version range for a released profile. Profile
fields already declare the specific capabilities/outcomes/states they consume,
so a second hand-maintained capability list is not required.

### Q6: A

Require at least one negative fixture for each enforced rule class:
presentation-authored transition; out-of-range readiness/heartbeat/lease;
missing control fallback; unknown/invalid persona reference;
reserved/forbidden mode; unsafe rendering/HTML or URI; missing/invalid
consent-purpose mapping; and held-answer rendered as active. Each fixture must
fail one primary rule with a stable error/evidence ID.

### Q7: A

Represent accessibility as explicit structured capability declarations for
keyboard operation, stable/visible focus, screen-reader announcements,
captions, text-only mode, reduced motion, high contrast, non-color cues,
zoom/reflow, and pseudo-locale coverage. Every field has a closed default and is
individually validator-checkable.

### Q8: A

The retention overlay carries references to externally owned retention-policy
IDs plus presentation flags/labels needed to show resolved retention state. It
contains no inline durations, legal policy, consent evidence, or authority to
change retention. An unresolved policy reference fails closed.

The spec derives from a ratified OpenSpec change, so most decisions are settled.
The questions below are limited to **material** ambiguities that would change
planning or implementation, ranked by priority (scope → authority/security →
acceptance evidence → data model). Each has a recommended answer (row A).

---

## Q1: Persona catalog artifact scope

- **Category**: Scope

> FR-011: "every selectable persona presents a stable ID/version, role, display
> name, required disclosure, supported languages, and lifecycle status from the
> **domain-owned catalog**"; FR-013: "a persona catalog reference"; Key entity:
> "Persona reference: A pointer into the domain-owned persona catalog."

**Question**: Does this feature define a persona-catalog schema/contract, or does
the UI profile only carry a *reference* (ID + version) to a catalog owned and
schematized elsewhere?

| Option | Answer | Implications |
|--------|--------|--------------|
| A | Reference-only — the profile schema carries a persona reference (ID + version + optional catalog locator); the persona-catalog schema itself is out of scope. **(Recommended)** | Keeps the feature within its declared owned surface (Decision 1 lists no catalog schema); examples reference persona IDs; catalog schema deferred to a named domain/kernel owner. |
| B | This feature also defines a minimal domain-neutral persona-catalog schema alongside the profile. | Expands the owned surface beyond the five listed artifacts; adds a contract schema + validator checks + examples + manifest registration. |
| C | Reference-only, but the standard doc names the required persona-catalog fields normatively (ID, version, role, disclosure, languages, lifecycle) without shipping a schema file. | Standard prescribes the catalog shape as prose; successor/domain owns the schema; validator checks profile references only. |
| Custom | _Provide your own answer_ | — |

---

## Q2: Confirmation-before-action example neutrality

- **Category**: Scope / Governance (Constitution Principle I — domain-neutral core)

> FR-019: "validated customer avatar-first, client hybrid, domain
> conventional-first, and **confirmation-before-action** profiles". The source
> task (tasks.md 2.2) calls this a "**Ledgerx-style** confirmation-before-action"
> profile, while Principle I forbids domain-specific content in openxFactory.

**Question**: Must the confirmation-before-action example be a domain-neutral
archetype rather than embedding Ledger/accounting specifics?

| Option | Answer | Implications |
|--------|--------|--------------|
| A | Domain-neutral archetype — a generic "confirmation-before-consequential-action" example in neutral vocabulary, no Ledger/accounting specifics. **(Recommended)** | Complies with Principle I; "Ledgerx-style" read as inspiration, not literal domain content; authorable now during parallel work. |
| B | Include Ledger-flavored fields, isolated in a clearly-marked `.example.yaml` instantiation stub. | Risks domain leakage into the neutral core; likely fails domain-neutrality review; needs explicit justification. |
| C | Drop the standalone confirmation-before-action example; fold confirmation coverage into the domain conventional-first example. | Fewer examples; reduces distinct positive coverage of the confirmation-before-action scenario; may weaken acceptance evidence. |
| Custom | _Provide your own answer_ | — |

---

## Q3: Deterministic UI fixture shapes — form and location

- **Category**: Scope / Acceptance evidence

> FR-023: "publish deterministic UI fixture shapes (fixed clocks, IDs, fonts,
> locale fixtures, platform capabilities, and canonical AVC commands/events/
> snapshots)"; SC-006: "declared canonical view-state, command, event, and
> record shapes."

**Question**: In what artifact form and location are the deterministic UI fixture
shapes published, as distinct from the profile examples under
`examples/avatar-first-ui/`?

| Option | Answer | Implications |
|--------|--------|--------------|
| A | Versioned YAML/JSON fixture files in a dedicated directory (e.g., `examples/avatar-first-ui/fixtures/`) carrying canonical command/event/snapshot inputs and expected view-state shapes, validated by the offline validator. **(Recommended)** | Clear separation of carrier profiles vs test shapes; validator parity-checks fixtures; no client code; reusable by successor. |
| B | Embed fixture shapes as annotated sections within the profile schema and examples. | Fewer files but conflates the carrier schema with test shapes; harder for the successor client to consume. |
| C | Define fixture shapes only as normative descriptions in the standard doc plus the acceptance map; concrete runnable fixtures deferred to `implement-avatar-client-lab`. | This feature ships shape contracts as prose; successor produces runnable fixtures; weaker offline determinism evidence here. |
| Custom | _Provide your own answer_ | — |

---

## Q4: Readiness/heartbeat/lease ceilings — schema-embedded vs kernel-referenced

- **Category**: Authority

> FR-013: "a readiness default/range, heartbeat and lease ceilings"; FR-021:
> "in final-realization mode, MUST load the exact released kernel registries
> read-only and fail closed on any drift"; Constitution Principle VII: closed
> registries are kernel-owned.

**Question**: Does the UI profile schema embed the concrete readiness/heartbeat/
lease ceiling constants, or carry per-profile selected values validated against
ceilings supplied read-only by the kernel state registry?

| Option | Answer | Implications |
|--------|--------|--------------|
| A | Reference/consume — the schema carries per-profile selections; the validator checks them against kernel-supplied ceilings (baseline IDs during parallel work, released registry at realization); no numeric maxima hardcoded in the UI schema. **(Recommended)** | Honors read-only kernel authority and the fail-closed drift check; the UI never owns the ceiling values. |
| B | The UI schema declares the ceiling constants itself as domain-neutral defaults. | Duplicates authority the kernel owns; risks drift the cross-check must catch; simpler offline validation but violates read-only consumption intent. |
| C | Hybrid — schema declares closed default *selections* but treats ceilings as kernel-owned symbolic bounds resolved at validation time. | Closed defaults present for existing-profile compatibility; bounds still resolved from the kernel; more validator logic. |
| Custom | _Provide your own answer_ | — |

---

## Q5: Runtime compatibility field semantics and cross-check basis

- **Category**: Authority / Integration

> FR-013: "carry runtime compatibility"; FR-017: "consumed read-only against the
> kernel's capability, outcome, consent-purpose, and state registries"; FR-021:
> final cross-check; Key entity: "Runtime compatibility (interface baseline
> reference)."

**Question**: What does the profile's "runtime compatibility" field encode, and
what does the final cross-check compare it against?

| Option | Answer | Implications |
|--------|--------|--------------|
| A | An interface/bundle pin or range (`avatar-client-parallel-v1` during parallel work, then the released contract bundle version/commit at realization) validated against the released kernel registries. **(Recommended)** | Matches the versioned, content-addressed release policy (Principle VI); enables fail-closed drift detection; requires updating the pin at realization. |
| B | A declared set of required kernel capabilities/outcomes/states the profile depends on, cross-checked for presence in the released registries. | Capability-set semantics; more granular drift detection; larger schema surface. |
| C | Both — a version pin plus a declared required-capability set. | Strongest compatibility guarantee; most validator/authoring work; largest schema. |
| Custom | _Provide your own answer_ | — |

---

## Q6: Negative fixture minimum coverage set

- **Category**: Acceptance evidence

> FR-019: "negative fixtures (each expected to fail on a specific rule)";
> FR-020 validator checks: state axes, safe outcomes, held-answer/media
> authorization, bounds, control fallbacks, purpose mappings, persona
> references, safe rendering, forbidden/reserved modes.

**Question**: What is the required minimum set of negative fixtures the validator
must reject?

| Option | Answer | Implications |
|--------|--------|--------------|
| A | One negative fixture per rule class the validator enforces (presentation-authored transition; out-of-range readiness/heartbeat/lease; missing control fallback; unknown/invalid persona reference; reserved/forbidden mode; unsafe-rendering/HTML; missing/invalid consent-purpose mapping; held-answer shown as active). **(Recommended)** | Full rule coverage (~8 fixtures); strongest acceptance evidence; more fixtures to maintain. |
| B | One negative fixture per AFU requirement family (up to 8, grouped by requirement). | Requirement-aligned coverage; may under-test multiple rules inside one requirement; fewer fixtures. |
| C | A representative subset covering the highest-risk rules (authority transitions, reserved modes, unsafe rendering), with the rest asserted by unit-level validator tests. | Fewer fixtures; some rules covered only by code tests; lighter maintenance, weaker fixture-level evidence. |
| Custom | _Provide your own answer_ | — |

---

## Q7: Accessibility baseline schema shape

- **Category**: Acceptance evidence / Data model

> FR-013: "an accessibility baseline"; FR-010 enumerates declarable a11y
> requirements; FR-020: validator "checks... accessibility fields"; Key entity:
> accessibility baseline.

**Question**: How is the accessibility baseline represented in the profile schema?

| Option | Answer | Implications |
|--------|--------|--------------|
| A | A structured set of explicit per-capability declarations (keyboard, stable/visible focus, screen-reader announcements, captions, text-only, reduced motion, high contrast, non-color cues, zoom/reflow, pseudo-locale), each with a closed default. **(Recommended)** | Validator checks each field; precise declared coverage; maps 1:1 to AFU-005; larger schema. |
| B | A single baseline-level enum/attestation (e.g., `baseline: standard`) with details only in the standard doc. | Compact schema; coarse validation; per-capability gaps not machine-checkable here. |
| C | A profile-referenced accessibility-baseline ID pointing at a named baseline definition, with per-profile overrides only. | Reuse across profiles; adds indirection; needs a baseline registry/definition owner. |
| Custom | _Provide your own answer_ | — |

---

## Q8: Retention overlay shape

- **Category**: Data model

> FR-013: "a retention overlay"; Decision 6 lists "retention overlay"; the
> standard requires showing the "resulting retention state" after consent
> withdrawal.

**Question**: What does the profile's retention overlay carry?

| Option | Answer | Implications |
|--------|--------|--------------|
| A | References to named retention-policy IDs (owned elsewhere) plus display/UX flags for showing retention state — no inline durations. **(Recommended)** | Keeps retention-policy authority outside the UI profile; UI only maps display; consistent with the no-consent-evidence rule. |
| B | Inline retention parameters (durations, categories) defined per profile. | Self-contained profiles; risks the UI owning retention policy that belongs to the Hermes/consent layer; possible authority conflict. |
| C | A minimal overlay of retention display states only (active/none/stopped), with all policy references external. | Smallest schema; UI purely presentational; policy binding handled entirely by consuming layers. |
| Custom | _Provide your own answer_ | — |

---

## Coverage note

Categories reviewed and judged **Clear** in the source (no question raised):
core scope and Hermes-layer defaults, presentation-mode vs authoritative-axis
separation, shell regions/controls, media-authorization/held-answer semantics,
AVC-02 denial/terminal rendering, control-loss vs media-loss, safe untrusted
rendering, handoff boundary and URL constraints, consent-purpose ID sourcing
(frozen `avatar-client-parallel-v1` baseline), serialized post-kernel release
sequencing (manifest/changelog/README atomic, version-at-realization), and the
successor-ownership split. Validator mode-selection mechanism was judged a
plan-level execution detail (not spec-blocking) and deliberately excluded.
