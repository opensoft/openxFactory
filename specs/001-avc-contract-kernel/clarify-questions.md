# Clarify Questions: 001-avc-contract-kernel

**Feature spec**: `specs/001-avc-contract-kernel/spec.md`
**Source**: OpenSpec change `define-avatar-client-contract-kernel` (ratified-grade)
**Generated**: 2026-07-11
**Question count**: 7


## Accepted Answers

**Answered**: 2026-07-10 (America/Los_Angeles)

**Decision summary**: `Q1=A+; Q2=A; Q3=A; Q4=A; Q5=A; Q6=Custom; Q7=A+`.

### Q1: A, with the evidence/disposition register included

Digest and manifest-register the full consumed semantic and conformance set: the
8 schemas, shared definitions, all closed registries, the consent-purpose
registry, canonical fixtures, acceptance map, interface lock, and the
consolidated evidence/disposition register selected in Q4. The Python validator
ships at the release commit as reproducible reference tooling but is not a
pinned semantic artifact. Every manifest entry has its own SHA-256 digest.

### Q2: A

Ship AVC-07 and AVC-08 schemas plus conformance fixtures only. Do not ship live
persona or retention instances, extra examples, or domain templates. Domains
own concrete persona and retention content.

### Q3: A

Use both structural exclusion and a committed-content scan. Schemas must make
secret/SDP/raw-media fields structurally invalid where prohibited, and the
validator must scan fixtures and evidence for credential, SDP, raw payload,
transcript/media, and prohibited high-cardinality patterns. Synthetic test
sentinels must be explicitly bounded so they cannot become a bypass for real
secret patterns.

### Q4: A

Create one consolidated, content-addressed evidence/disposition register under
`contracts/avatar-client/`. Automated scenarios name fixture evidence; manual
scenarios contain a recorded result and reviewer/disposition fields; `live_f0`
and successor scenarios name the owning change and the fail-closed default that
remains active. The validator checks completeness, allowed status transitions,
and referenced artifact existence.

### Q5: A

Define conformance through language-neutral, self-describing fixtures. Each
fixture identifies its target schema/registry, expected valid or invalid result,
and stable scenario/evidence ID. Any draft-2020-12 implementation may execute
them. `scripts/validate-avatar-client.py` is the reference runner, not a required
consumer dependency.

### Q6: Custom - F0 owns; kernel pins and validates

`qualify-avatar-brokered-call-feasibility` owns and versions both
`f0-results.schema.yaml` and an `f0-interface-impact.schema.yaml`. The kernel
publication gate pins the exact F0 source commit and both schema digests,
validates the evidence instances against those pinned schemas, and only then
reads `PASS` or variance dispositions. It fails closed on a missing schema,
digest mismatch, validation failure, unknown status, or unknown variance field.
The kernel does not duplicate or co-own the F0 schemas.

### Q7: A, with two completion states

The Speckit implementation may reach **implementation complete, publication
pending F0** when all kernel artifacts and validators are merged and green and
the publication gate is enforced. The OpenSpec change remains active and its
publication/handoff tasks remain incomplete until F0 is `PASS`, all variances
are dispositioned, the annotated tag is published, and release digests are
recorded. Do not archive or call the release realized at the earlier milestone.

> These are **material** ambiguities only — each answer would change planning,
> task decomposition, the release/bundle definition, the validator, or acceptance
> evidence. Items already pinned by the ratified change, `docs/contract-versioning-policy.md`,
> the acceptance map, or the acceptance-traceability doc (release identity,
> compatibility classes, acceptance-map location under `contracts/avatar-client/`,
> the 17-requirement/72-scenario parity target) are **not** re-asked.
>
> The "(Recommended)" row is this author's analysis of the most defensible
> default from the source material. Accepted decisions are recorded below for the
> track agent to encode into `spec.md`.

Priority order below follows: scope > authority/security > acceptance evidence > sequencing.

---

## Q1: Released bundle file set and per-file digest scope

**Category**: Functional Scope & Constraints

**Context (spec.md)**: FR-022 — "each published bundle MUST have one matching
manifest version, changelog entry, annotated tag, exact release commit, and
per-file digests"; FR-023 — "Consumers MUST pin the exact openxFactory commit
plus per-file digests and prove conformance by executing the canonical fixtures
of the pinned release." The existing `contracts/manifest.yaml` registers only
`type: schema` files (no fixtures/validator), so the released file set for this
kernel is not established by convention.

**Question**: Which files constitute the content-addressed released bundle —
i.e., which get per-file SHA-256 digests and manifest entries that consumers pin?

| Option | Answer | Implications |
|--------|--------|--------------|
| A | Digest + manifest-register the full **consumed** set: the 8 schemas, `shared-definitions`, the closed registries, the consent-purpose registry, the canonical fixtures, the acceptance map, and the interface-lock. Ship `scripts/validate-avatar-client.py` in the release commit as reproducible tooling but treat it as **not** a pinned semantic artifact. **(Recommended)** | Consumers can pin and re-run the exact fixtures/registries; the validator stays a tool, not a versioned contract. Largest manifest surface; clear "run these exact fixtures" guarantee (satisfies SC-009). |
| B | Digest + register only the semantic schemas, `shared-definitions`, and registries. Ship fixtures + acceptance map in the commit but do **not** give them per-file digests. | Smaller pinned surface; but consumers cannot cryptographically prove which fixture bytes they ran, weakening FR-023/SC-009. |
| C | Digest **everything** in `contracts/avatar-client/`, including the validator script. | Strongest reproducibility; but couples consumers to a Python tool version and forces re-release on any validator edit. |
| Custom | Provide your own file-set / digest boundary | — |

---

## Q2: AVC-07 / AVC-08 profile artifacts — schemas only or instances too?

**Category**: Domain & Data Model / Scope

**Context (spec.md)**: FR-001 lists "AVC-07 retention profile" and "AVC-08
persona profile" among the eight contracts; Assumptions state this feature owns
"the neutral contracts, shared definitions, registries, consent purposes,
fixtures, the validator, the acceptance map, and the release metadata." Constitution
Principle IV treats `.template.yaml` / `.example.yaml` as instantiation stubs.
The persona catalog is domain-owned.

**Question**: For AVC-07 and AVC-08, does the kernel ship only the JSON Schema
(plus conformance fixtures), or also concrete profile instances?

| Option | Answer | Implications |
|--------|--------|--------------|
| A | Schemas + conformance fixtures only; the canonical fixtures serve as the illustrative examples. No separate live profile instances. **(Recommended)** | Keeps domain-owned persona/retention content out of the neutral kernel; smallest surface; consistent with "contracts + fixtures" scope. |
| B | Schemas + one non-live reference `.example.yaml` for each, clearly marked as illustration. | Gives implementers a worked example beyond fixtures; adds files that must be kept in sync and validated. |
| C | Schemas + `.template.yaml` instantiation stubs for domains to fill. | Eases domain adoption; risks the kernel implying a specific instantiation shape the domain layer should own. |
| Custom | Provide your own artifact boundary | — |

---

## Q3: Secret-exclusion / redaction enforcement method

**Category**: Security & Privacy

**Context (spec.md)**: FR-018 — "any artifact containing a credential, SDP, raw
transcript, raw media, or a prohibited high-cardinality identifier fails
validation"; SC-008 — "0 committed contract, fixture, or evidence files contain
credentials, raw provider payloads, SDP, or prohibited high-cardinality
identifiers." The detection mechanism is not specified.

**Question**: How does the validator enforce redaction / secret-exclusion over
committed contract, fixture, and evidence files?

| Option | Answer | Implications |
|--------|--------|--------------|
| A | Both layers: (1) **structural** — schemas forbid secrets/SDP/credentials as required or permitted fields (validated by construction); (2) **content scan** — a denylist of credential/SDP/high-cardinality-identifier patterns run over committed fixtures and evidence. **(Recommended)** | Defense in depth; the structural layer proves the contract can't carry secrets, the scan catches accidental leakage in example bytes. Most work; strongest guarantee. |
| B | Structural only — rely on schema shape to make secret-carrying results invalid. | Simple; but a fixture author could still paste a real secret into an otherwise-valid example and it would pass. |
| C | Content scan only — pattern denylist over all committed files. | Catches pasted secrets; but does not prove the contract structurally excludes them (weaker than the FR-007/FR-018 intent). |
| Custom | Provide your own enforcement model | — |

---

## Q4: Evidence representation for manual / live_f0 / successor scenarios

**Category**: Completion Signals / Acceptance Evidence

**Context (spec.md)**: FR-021 requires the acceptance map to name each scenario's
"fixture or manual evidence ID, release ring, and status"; SC-003 — "Every
normative requirement and scenario ... has exactly one acceptance-map entry with
an evidence identifier." The acceptance map's `evidence_types` include `manual`,
`live_f0`, and `successor`, which cannot be satisfied by a contract fixture, yet
the validator must not report them as "evidence-free."

**Question**: For non-automatable scenarios, what committed artifact makes the
validator's evidence-presence check pass without a fixture?

| Option | Answer | Implications |
|--------|--------|--------------|
| A | A single consolidated evidence/disposition register under `contracts/avatar-client/`: automated → fixture ID; `manual` → a register entry with a recorded result; `live_f0` / `successor` → a named owning change **plus** the fail-closed default that holds until the owner lands. Validator checks the register for presence + disposition. **(Recommended)** | One auditable file ties every scenario to evidence or a named deferral; matches the traceability doc ("named owner and fail-closed default"). Consumers/reviewers read one register. |
| B | One evidence-record file per manual/successor scenario. | Fine-grained; but many small files to maintain and digest. |
| C | The acceptance-map fields alone (owner_change + status) are sufficient; no separate evidence artifact. | Least work; but "status" is not the same as recorded evidence — weakens the "not evidence-free" guarantee for manual scenarios. |
| Custom | Provide your own evidence model | — |

---

## Q5: Cross-language consumer conformance mechanism

**Category**: Integration & Acceptance Evidence

**Context (spec.md)**: SC-009 — "A consumer pinned to the released kernel can
validate its own models against the canonical fixtures using only the published
commit and per-file digests, with 0 additional coordination required." FR-020
names `scripts/validate-avatar-client.py` (Python), but the first real consumer
(the Flutter client) is Dart, and the reference runtime is Python.

**Question**: How is consumer conformance defined so a non-Python consumer can
prove it "with 0 additional coordination"?

| Option | Answer | Implications |
|--------|--------|--------------|
| A | Fixtures are **language-neutral and self-describing** — each declares its target schema and expected valid/invalid outcome — so any conformant draft-2020-12 validator (incl. Dart) can execute them. The Python validator is the reference runner, not a required dependency for consumers. **(Recommended)** | Truly portable conformance; satisfies SC-009 for Dart/other consumers. Requires a small fixture-metadata convention. |
| B | Conformance is defined as running `scripts/validate-avatar-client.py`; consumers invoke the kernel's Python tool in their CI. | Simplest to author; but forces every consumer (Dart client) to carry a Python toolchain — contradicts "0 additional coordination." |
| C | Ship both a self-describing fixture manifest **and** the Python validator, and require consumers to match the Python reference results. | Maximal rigor; heaviest consumer burden and cross-language drift risk. |
| Custom | Provide your own conformance definition | — |

---

## Q6: Ownership of the consumed F0 evidence schema

**Category**: Integration & External Dependencies

**Context (spec.md)**: Dependencies — "the annotated contract tag depends on
`qualify-avatar-brokered-call-feasibility` producing `PASS` evidence and a
disposition for every reported interface variance." FR-029 gates the tag on that
evidence. The gate reads `f0-results.json` / `f0-interface-impact.yaml`, but
which change owns the **schema** of those consumed artifacts is unstated.

**Question**: Who defines and validates the shape of the F0 evidence artifacts
the kernel's publication gate consumes?

| Option | Answer | Implications |
|--------|--------|--------------|
| A | The kernel defines and versions the **minimal consumed schema** for `f0-results.json` and `f0-interface-impact.yaml` (the gate's input contract) and validates their shape before honoring `PASS`; the F0 sibling produces conforming instances. **(Recommended)** | The consumer of the gate owns the interface it depends on; robust, fail-closed gate. Adds two small schemas to this change. |
| B | The F0 sibling (`qualify-avatar-brokered-call-feasibility`) owns the schemas; the kernel reads named fields opaquely and trusts them. | Less coupling into this change; but the gate can silently misread a malformed evidence file (weaker fail-closed posture). |
| C | A shared evidence schema is authored here but its evolution is owned by the F0 sibling. | Balances ownership; but split ownership invites drift over who may change the shape. |
| Custom | Provide your own ownership split | — |

---

## Q7: Definition of Done — is tag publication inside this feature's scope?

**Category**: Sequencing / Completion Signals

**Context (spec.md)**: FR-024 — "The contract bundle version MUST be allocated
only at realization ... and the annotated tag published from the realized release
commit"; FR-029 blocks the tag until F0 is `PASS`. The F0 sibling may not have
produced `PASS` during this feature's implementation window.

**Question**: Does completing this Speckit feature include publishing the
annotated tag + digests, or does the feature complete "release-ready" with tag
publication deferred behind the F0 gate?

| Option | Answer | Implications |
|--------|--------|--------------|
| A | Feature reaches "**implementation complete, publication pending F0**": all schemas/registries/fixtures/validator/acceptance-map authored and green, the gate enforced; the tag + digests are published as the final realization step **when** F0 `PASS` exists (possibly after this feature's coding window). **(Recommended)** | Lets the feature finish without blocking on a sibling; honors `target_release: implemented` (archives on merged + green realization evidence). Tasks 3.3/4.2 have a clearly gated final step. |
| B | The feature is **not done** until the tag is published; it blocks on F0 `PASS` within this feature. | Single clean endpoint; but stalls the feature on an external sibling and couples two workstreams' timelines. |
| C | Move tag publication + digest handoff entirely to a **separate release change**; this feature ends at release-ready artifacts. | Clean separation; but adds governance overhead and a second change to author/track. |
| Custom | Provide your own DoD / publication boundary | — |

---

*End of block — 7 questions. Accepted answers are recorded above for the track agent to apply to `spec.md`.*
