# Schema and Vocabulary Closedness Checklist: Client Identity Roster

Status: draft

**Purpose**: Release-gate validation of the requirements governing REPRESENTATION —
closed enumerations, refusal semantics, the two deliberately open tokens and what
bounds them, and the discipline that closure lives at the representation level
rather than in a denylist of bad values.
**Created**: 2026-08-14
**Feature**: [spec.md](../spec.md)
**Lens**: closed-world at the representation level. A rule that enumerates what is
FORBIDDEN is a detector; a rule that enumerates what is ADMISSIBLE is a contract.
Every item below asks which of the two a requirement actually specifies.

## Closed sets are enumerated, not described

- [x] CHK201 Is each closed set enumerated MEMBER BY MEMBER in the requirements, so the schema author has nothing to infer? [Completeness, Spec §FR-034]
- [x] CHK202 Is `admission_surface` closed to two named members with its extension route stated? [Closedness, Spec §FR-007]
- [x] CHK203 Is the authority class closed to two members with the destructive class unrepresentable rather than validated-against? [Closedness, Spec §FR-005]
- [x] CHK204 Is `residency_model` closed with both members named in token form, not only in prose form? [Closedness, Spec §FR-034]
- [x] CHK205 Is `enforcement_mode` closed with its two members named explicitly rather than left as a free string? [Closedness, Spec §FR-034]
- [x] CHK206 Is `lifecycle_state` closed to three members? [Closedness, Spec §FR-034]
- [x] CHK207 Is `identity_kind` closed, with its membership DERIVED by a stated rule rather than invented? [Closedness, Spec §FR-034, research §Decision 1]
- [x] CHK208 Is a one-member closed set argued for rather than treated as an oversight, so a later reader does not "fix" it by widening? [Clarity, research §Decision 1]
- [x] CHK209 Is the drift record's `status` set stated as closed and given a refusal probe like every other closed set? [Closedness, Spec §FR-035, §SC-014] — FIXED: `status` was closed in the schema but SC-014's measurement enumerated six sets and the corpus six negatives, leaving the seventh unprobed. SC-014 now names seven sets; `drift-finding-status-out-of-vocabulary.yaml` is added at tasks §4.3; plan §Cluster A, §Cluster C and the Constitution VII row are re-counted.
- [x] CHK210 Is the credential-side closed vocabulary (`issuance_preconditions`) stated as closed WITH a refusal that names the vocabulary? [Closedness, Spec §FR-028, §SC-008]
- [x] CHK211 Is the extension rule for every closed set the same one (the change that governs the new member adds it), so no set has a private growth path? [Consistency, Spec §FR-034]
- [x] CHK212 Are member spellings fixed to one dialect, with the prose forms explicitly declared NOT to be a second token spelling? [Clarity, Spec §FR-034]

## Refusal semantics

- [x] CHK213 Does every closed-set requirement say the refusal NAMES the closed vocabulary, rather than merely saying the value is invalid? [Clarity, Spec §FR-007, §FR-034, §SC-014]
- [x] CHK214 Does each closed-set refusal also name the EXTENSION ROUTE, so a refused author knows the legitimate path? [Completeness, Spec §FR-007, tasks §2.3]
- [x] CHK215 Is the refusal specified to survive the schema layer — i.e. does a requirement exist that the named message appears even when the schema alone would refuse the document? [Gap, Spec §SC-014, plan §Cluster B] — FIXED: nothing said the rule engine runs past a schema failure, so every schema-visible negative could have adjudicated as a generic `schema` finding that names neither vocabulary nor route. plan §Cluster B and tasks §2.2 now require record-internal rules to run to completion and raise their own kebab codes, with the expectations table pinning the NAMED one.
- [x] CHK216 Is "fail closed" stated for unrecognized values rather than "warn", anywhere a new value could appear? [Fail-closed, Spec §FR-034, plan §Constitution VII]
- [x] CHK217 Are the refusals expressed as ADMISSIBILITY rules (a value must be a member) rather than as denylists of known-bad values? [Closed-world, Spec §FR-034]
- [x] CHK218 Where the design does use a denylist-shaped rule, is that fact declared, bounded, and paired with the closed-world rule that carries the real guarantee? [Closed-world, Spec §FR-010] — FIXED: FR-010's name check matches a small closed list of observation-suggesting tokens — a detector whose blind spot (a name using an unlisted word) was nowhere stated. FR-010 now declares the blind spot, forbids growing the rule into an open-ended prose reading, and names FR-004's record-internal class check as the load-bearing closed-world rule beside it.

## The two open tokens, and what bounds them

- [x] CHK219 Are `blast_radius_unit` and `duty` stated as domain-declared tokens with a pattern, rather than as neutral enumerations? [Clarity, Spec §FR-034]
- [x] CHK220 Is the legend required as the binding between a free token and its provider-native identifier, so provider fidelity has a declared home? [Completeness, Spec §FR-034, §Key Entities]
- [x] CHK221 Are the legend's findings enumerated EXHAUSTIVELY (used-without-entry, declared-twice) with a statement that there is no third legend rule? [Completeness, Spec §FR-034, plan §Cluster A]
- [x] CHK222 Is the deliberate NON-finding (a legend entry no entry uses) stated with its reason, so it is not added later as a "strictness improvement"? [Coverage, plan §Cluster A]
- [x] CHK223 Is the legend's scope (per fragment) stated, given that the same token spelling may legitimately recur in another fragment? [Clarity, Spec §FR-034, §FR-006]
- [x] CHK224 Is the alias rule stated as the bound on free-token invention, with its own probe? [Coverage, Spec §FR-038, §SC-014]

## Record shape and internal checkability

- [x] CHK225 Is `granted_permissions[]` specified as objects carrying the declared class and reach, so no rule needs to read a provider identifier's spelling? [Clarity, Spec §FR-004, plan §Cluster A]
- [x] CHK226 Is the prohibition on inferring provider semantics from an identifier stated as a requirement, not only as a design note? [Clarity, Spec §FR-004, §Assumptions]
- [x] CHK227 Is `achieved_scope` kept provider-native, with the one fact a check needs about it DECLARED (`exceeds_governed_unit`) rather than parsed out of the token? [Clarity, Spec §FR-002]
- [x] CHK228 Is `per_unit_principal_available` specified as a per-surface mapping rather than a boolean, and is its required KEY SET specified? [Completeness, Spec §FR-008] — FIXED: the coverage obligation lived only in tasks §1.5's prose; nothing enforced it and nothing probed it, so a fragment could omit the awkward surface and pass while an absent key and a declared `false` stayed indistinguishable. FR-008 now states the required key set and the finding, tasks §2.6 carries the rule, and `per-unit-principal-undeclared.yaml` (tasks §4.1) is its negative. An EXTRA key is explicitly NOT a finding — the key space is already closed by the enum.
- [x] CHK229 Is `standing_credential_attestation` given a shape that makes FR-013's falsification a record-internal contradiction rather than an observation of a credential store? [Clarity, Spec §FR-013, plan §Cluster A]
- [x] CHK230 Is `evidence_ref` specified as a pointer with a shape and an explicit non-resolution posture? [Clarity, Spec §FR-037]
- [x] CHK231 Are the two `identity_ref` shapes (entry string, drift object) both ratified names, with the divergence documented rather than renamed away? [Consistency, Spec §FR-001, §FR-035]
- [x] CHK232 Is `additionalProperties: false` required at every depth, so an unknown property is refused rather than carried? [Closed-world, tasks §1.1]
- [x] CHK233 Are conditional obligations that a schema CAN express required to live there (the vendor-tenant-multi `if/then`), so a validator refactor cannot lose them? [Completeness, Spec §FR-012, tasks §1.8]
- [x] CHK234 Where an obligation CANNOT be expressed in schema (a key set depending on another field's value), is that stated with the reason, so its absence from the schema is not read as an oversight? [Clarity, tasks §1.7] — FIXED as part of CHK228.
- [x] CHK235 Is the drift record's disposition citation's POPULATION specified, given that an `open` finding cannot have been dispositioned? [Ambiguity, Spec §FR-035] — FIXED: `disposition_ref` is now optional and required only under `status: disposed`; the packaged example (tasks §3.6) is an `open` finding and carries none, where the pre-checklist draft listed both together.
- [x] CHK236 Do both record kinds declare the same envelope `schema_version` const, so the single manifest row is unambiguous? [Consistency, plan §Cluster A, ruling A-2]

## Notes

- Five items carried a defect (CHK209, CHK215, CHK218, CHK228/CHK234, CHK235). Every fix
  is an admissibility rule or a declared limitation — none adds a denylist.
- The one denylist-shaped rule in the feature (FR-010's name-token list) is now declared
  as a detector with a named blind spot, standing beside a closed-world rule that carries
  the guarantee. That is the disposition this lens exists to force.
