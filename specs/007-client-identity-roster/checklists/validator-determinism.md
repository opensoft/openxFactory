# Validator Determinism and Hermeticity Checklist: Client Identity Roster

Status: draft

**Purpose**: Release-gate validation of the requirements governing HOW the canonical
validator and the cross-domain family may compute — determinism, network-freeness,
single-repo reach, consumption shape, exit codes, and the pointers they must not
follow. These are the requirements that make a finding reproducible and a check safe
to make blocking.
**Created**: 2026-08-14
**Feature**: [spec.md](../spec.md)

## Determinism

- [x] CHK301 Is determinism stated as a requirement of the canonical validator, not only of the doc-health family? [Completeness, Spec §FR-015, §SC-011]
- [x] CHK302 Is determinism given a measurable form (byte-identical findings across runs) rather than the word "deterministic"? [Measurability, Spec §SC-011]
- [x] CHK303 Is the determinism measurement for the new doc-health family required to be its OWN assertion, given that the existing suite's determinism test is family-specific? [Gap, plan §Cluster G, research §Decision 6]
- [x] CHK304 Is the vacuous-pass hazard for that assertion named (a context whose skip short-circuits the family satisfies "identical across runs" trivially)? [Edge Case, plan §Cluster G, ruling A-9]
- [x] CHK305 Are iteration orders specified where they affect output (sorted repo paths, sorted findings)? [Clarity, plan §Cluster G, research §Decision 6]
- [x] CHK306 Is "no model call" stated separately from "no network", since a model call could be local? [Completeness, Spec §FR-023, §SC-011]
- [x] CHK307 Is the drift-finding record forbidden from carrying anything a re-run would change other than the observed values and timestamps it is defined to carry? [Clarity, Spec §FR-027, §FR-035]

## Hermeticity and reach

- [x] CHK308 Is network-freeness stated as a property of the validator, its tests, and every artifact the feature ships? [Completeness, Spec §FR-029, §SC-011]
- [x] CHK309 Is the hermeticity guarantee anchored to a MECHANISM (the suite-wide guard) rather than to discipline? [Measurability, plan §Technical context, tasks §10.6]
- [x] CHK310 Is the single-repository reach of the canonical validator stated, so no rule can be written that reads a second tree? [Clarity, Spec §FR-015, §FR-037]
- [x] CHK311 Is `evidence_ref` explicitly excluded from resolution, with the reason (network-free, single-repo) rather than as an unexplained gap? [Clarity, Spec §FR-037]
- [x] CHK312 Is the consent dependent-ref's pointer given the SAME non-resolution posture, stated in the artifact so a later reader does not "fix" it with a cross-repo read? [Consistency, plan §Cluster I, ruling A-5]
- [x] CHK313 Are the pointers that DO resolve (gate obligation, consent citation) identified as intra-repo, with the argument for why that does not breach hermeticity? [Clarity, Spec §FR-011, §FR-014, plan §Cluster B]
- [x] CHK314 Is the cross-domain family's wider reach (pinned repos in an aggregation checkout) stated as the reason resolution belongs there instead? [Consistency, Spec §FR-037, §FR-023]
- [x] CHK315 Is a provider call, a credential mint, and a client-tenant act each forbidden by requirement — including inside tests? [Fail-closed, Spec §FR-029, §SC-012]
- [x] CHK316 Is the precondition task that needs provider FACTS constrained to offline sources, so the one research step cannot become a live call? [Coverage, tasks §0.1]

## Consumption shape

- [x] CHK317 Is the validator's invocation shape specified (one positional target-repo argument, run from the pinned checkout)? [Clarity, Spec §FR-015]
- [x] CHK318 Is the no-copy rule stated for the new check, matching the pack's existing rule? [Consistency, Spec §FR-015, §FR-022]
- [x] CHK319 Are the exit codes specified with their meanings (0 clean, 1 findings, 2 harness error) and tied to the pack's blocking semantics? [Clarity, Spec §FR-015, §FR-022]
- [x] CHK320 Is the no-argument behaviour specified (usage plus harness-error exit) rather than left undefined? [Edge Case, tasks §2.1]
- [x] CHK321 Is the absence behaviour specified as exit 0 WITH an explicit notice, rather than as silence? [Clarity, Spec §FR-022, §SC-013]
- [x] CHK322 Is the count of records checked required in the output, so a silent no-op run is distinguishable from a clean one? [Observability, Spec §US2-AS1, plan §Cluster B]
- [x] CHK323 Is the root-path derivation required to be relative to the module, so no host-absolute path is committed? [Clarity, plan §Constitution IV, tasks §2.1]

## Self-scan and fixture-corpus safety

- [x] CHK324 Is the whole-repo sweep's skip set specified rather than left to the implementer? [Clarity, Spec §FR-036, tasks §2.9]
- [x] CHK325 Are the self-scan exclusions (`examples/client-identity-roster/`, `tests/`) each justified by a stated fact, and bounded to the case where the target IS this checkout? [Clarity, plan §Cluster B, tasks §2.9]
- [x] CHK326 Is it stated that neither exclusion narrows the rule over a TARGET DOMAIN repo? [Clarity, Spec §FR-036, plan §Cluster B]
- [x] CHK327 Is the tree's own precedent for the rule cited (fixture corpora must never enter a real scan), so the exclusion is conventional rather than special-cased? [Traceability, plan §Cluster B, research §Decision 7]
- [x] CHK328 Is the case where a fixture repo is ITSELF the target dispositioned, so its fragments validate normally rather than being excluded? [Edge Case, plan §Cluster B, tasks §6.7]

## Rule-engine behaviour

- [x] CHK329 Is the behaviour of the rule engine on a schema-invalid document specified? [Gap, plan §Cluster B, tasks §2.2] — FIXED in this pass (see schema-vocabulary-closedness §CHK215): rules now run to completion and raise their own named codes, with defensive reads of missing or wrong-typed fields.
- [x] CHK330 Is the self-test's adjudication basis specified (registered code, plus a pinned detail where a generic schema finding would satisfy the code alone)? [Clarity, plan §Cluster B, tasks §2.2]
- [x] CHK331 Are all five self-test failure modes enumerated, so a corpus defect cannot pass as a green run? [Completeness, Spec §FR-018]
- [x] CHK332 Is the registration integrity rule two-directional (no probe without a file, no file without a probe)? [Completeness, Spec §FR-018]
- [x] CHK333 Is the "fails for the WRONG reason" failure mode required, so an incidental refusal cannot count as a negative confirmation? [Measurability, Spec §FR-018, §SC-001]

## Notes

- One item carried a defect (CHK329), fixed jointly with the closedness checklist's
  CHK215 — the same underlying gap seen from two lenses: a refusal that the harness
  cannot read is a refusal that does not exist.
- No item here required a ruling or packet change.
