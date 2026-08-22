# Consent Cascade Checklist: Client Identity Roster

Status: draft

**Purpose**: Release-gate validation of the requirements for the `consent-instrument`
MODIFIED capability — the governed-identity dependent kind, the cascade evidence
obligation, the `withdrawn` status growth, and the guarantee that every existing
instrument keeps its verdict.
**Created**: 2026-08-14
**Feature**: [spec.md](../spec.md)

## The dependent kind

- [x] CHK701 Is the governed identity required to be a NAMED member of the closed dependent-kind enumeration rather than the `other` escape? [Closedness, Spec §FR-026]
- [x] CHK702 Is the token itself named, given the packet settles none? [Clarity, research §Decision 5]
- [x] CHK703 Is the reason a new dependent kind cannot ride an extra property stated (the item object closes `additionalProperties`)? [Clarity, research §Decision 5]
- [x] CHK704 Is the dependent-ref's pointer CONVENTION specified (fragment path plus the entry's `identity_ref`)? [Clarity, ruling A-5, plan §Cluster I]
- [x] CHK705 Is the non-resolution posture of that pointer stated IN the artifact, so a later reader does not file it as a coverage gap? [Clarity, ruling A-5]
- [x] CHK706 Is the consent validator's obligation for a `governed_identity` dependent bounded explicitly (non-empty ref and nothing more)? [Scope, plan §Cluster I]

## The cascade obligation

- [x] CHK707 Is the evidence obligation stated to cover identity removal or retirement AND withdrawal of provider-side admission, not merely credential revocation? [Completeness, Spec §FR-026]
- [x] CHK708 Is the coverage made STRUCTURAL (two declared evidence properties) rather than a keyword scan of free text? [Measurability, research §Decision 5]
- [x] CHK709 Is the reason a free-text coverage claim was rejected stated (unmeasurable and trivially gamed)? [Clarity, research §Decision 5]
- [x] CHK710 Are the two new properties required to be OPTIONAL, so no existing instrument becomes invalid? [Consistency, Spec §FR-030, plan §Cluster I]
- [x] CHK711 Is the obligation placed where the family's own precedent puts it (the validator, per the schema's own comment), rather than in a root-level conditional? [Consistency, research §Decision 5]
- [x] CHK712 Is the new finding code named, and distinguished from the existing cascade code? [Clarity, plan §Cluster I, tasks §8.4]
- [x] CHK713 Is the ATTRIBUTION rule (the finding lands against the instrument, not the identity) carried, and identified as the already-promoted rule rather than a new discovery mechanism? [Traceability, Spec §US4-AS3, research §Decision 5]
- [x] CHK714 Is the measurement of attribution specified (the negative's finding names the instrument path)? [Measurability, tasks §8.5]

## The `withdrawn` growth

- [x] CHK715 Is the reason the enum must grow stated (the delta requires behaviour on "terminated or withdrawn" while the set admits only one)? [Traceability, Spec §FR-039]
- [x] CHK716 Is `withdrawn` required to be a DISTINCT member, with aliasing onto `terminated` explicitly forbidden? [Clarity, Spec §FR-039]
- [x] CHK717 Are ALL normative declaration sites of the closed set enumerated, so they grow together? [Completeness, Spec §FR-039, research §Decision 5]
- [x] CHK718 Is the Python copy of the set (`NEUTRAL_STATUSES`) included among those sites, with the consequence of omitting it? [Completeness, research §Decision 5]
- [x] CHK719 Is the DIRECTION of that change stated correctly (growing the tuple NARROWS an alias check rather than widening one)? [Clarity, ruling A-7, plan §Cluster I]
- [x] CHK720 Is the precondition that makes the narrowing safe recorded as a MEASURED sweep with a date and a reach, not as an assumption? [Measurability, ruling A-7, tasks §0.2]
- [x] CHK721 Is the sweep's reach required to be recorded honestly when the estate is only partly visible? [Honesty, tasks §0.2]
- [x] CHK722 Is the lifecycle-skip set (`PAST_SIGNATURE_STATUSES`) grown too, with the argument for why `withdrawn` belongs in it? [Completeness, plan §decision 7, research §Decision 5]
- [x] CHK723 Is the cascade gate's widening declared as a BEHAVIOUR CHANGE rather than described as unchanged in meaning? [Honesty, ruling A-6, plan §Cluster I]
- [x] CHK724 Is the code-spelling continuity decision stated separately from the behaviour change, so the two are not conflated? [Clarity, ruling A-6]
- [x] CHK725 Is the behaviour change reconciled with FR-030's "unmodified in behaviour" boundary? [Consistency, Spec §FR-030] — FIXED: FR-030's additivity argument covered the optional property and the enum member but not this widening; it now names it and states the narrow argument (the widened reach can only bind a state that could not exist before this change).
- [x] CHK726 Is the schema-version discipline specified (file `contract_schema_version` bumps; record envelope const does not)? [Clarity, Spec §FR-039, research §A registration gap]

## Existing-corpus safety

- [x] CHK727 Is the guarantee stated as verdicts AND finding codes preserved, rather than "the run still exits 0"? [Measurability, tasks §8.6]
- [x] CHK728 Is the baseline that makes that measurable required to be captured BEFORE the first edit? [Dependency, tasks §0.3, §8.6]
- [x] CHK729 Is the fact that this family has no pytest suite stated plainly, so the validator's self-test is understood as the suite? [Honesty, plan §Verification story]
- [x] CHK730 Are the fixtures for the new behaviour required to prove the obligation fires IDENTICALLY on both terminating events? [Measurability, tasks §8.5]
- [x] CHK731 Is the positive fixture required to exercise the new status AND the new dependent kind together? [Coverage, tasks §8.5]
- [x] CHK732 Is the promoted consent spec text excluded from edits, by the same rule as doc-health's? [Consistency, plan §decision 15, research §Decision 5]
- [x] CHK733 Is the roster side's use of the consent lifecycle ("in force" = executed or amended) consistent with the grown set — excluding `withdrawn` for every entry the in-force test APPLIES to, and exempting `retired` entries from that test entirely? [Consistency, Spec §FR-014, §FR-039] — AMENDED by gate ruling G1: the in-force test is now lifecycle-scoped. Resolution binds every entry; the in-force condition binds `planned` and `enrolled` only, because the ratified cascade drives withdrawal or termination through to identity retirement while FR-013 keeps the retired record, so an ended instrument is the EXPECTED citation of a `retired` entry. The item's original unscoped reading would have held the gate permanently red on the cascade's own correct end state.

## Notes

- One item carried a defect (CHK725), fixed in FR-030 and cross-listed on the
  scope-containment and ratified-fidelity checklists.
- CHK733 is the item most at risk of silent staleness later: the roster validator hard-codes
  the in-force set, so a future growth of the consent lifecycle must revisit it. It passes
  today because FR-014 names all four excluded states including `withdrawn` — and, after
  gate ruling G1, because it also names WHICH entries the in-force test binds. A future
  lifecycle growth must revisit both halves: the excluded-state list AND the lifecycle
  scoping.
