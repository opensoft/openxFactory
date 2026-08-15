# Fixture Corpus Sufficiency Checklist: Client Identity Roster

Status: draft

**Purpose**: Release-gate validation of the requirements governing the CORPUS — one
negative confirmation per rule, the killed-flaw positives, the discrimination pairs,
where each negative can physically live, and the registration that keeps a probe and
a file inseparable. A rule with no refusing probe is a sentence; a probe that refuses
for the wrong reason is worse than none.
**Created**: 2026-08-14
**Feature**: [spec.md](../spec.md)

## Per-rule coverage

- [x] CHK401 Is the corpus obligation stated as one negative per RULE, with the named list explicitly a minimum? [Completeness, Spec §FR-016]
- [x] CHK402 Are all sixteen named rules of FR-016 accounted for, with a named home for each? [Completeness, plan §Cluster C coverage table]
- [x] CHK403 Are the rules the named list does NOT enumerate also homed, so "at minimum" is honoured rather than cited? [Completeness, plan §Cluster C]
- [x] CHK404 Does every rule the requirements state have a refusing probe? [Coverage, Spec §FR-016] — FIXED: three stated rules had none — act-side undeclared reach, `per_unit_principal_available` coverage, and the drift record's closed `status`. Each now has a packaged negative (tasks §4.1, §4.3) and a rule in tasks §2.6 / plan §Cluster B.
- [x] CHK405 Does every registered negative have a refusal PREDICATE the requirements define, rather than a filename that implies one? [Gap, Spec §FR-016] — FIXED: `unverified-act-counted-as-access.yaml` named a rule whose only specified behaviour was EXCLUSION from effective reach — a behaviour, not a refusal — so the fixture would have validated clean and tripped FR-018's "negative that passes". FR-002/FR-003 now make the evidence/verification-time pair the predicate, and tasks §2.5 raises the named code.
- [x] CHK406 Are the counts of packaged negatives internally consistent across plan.md's structure listing, its Cluster C prose, and tasks.md's authoring tasks? [Consistency, plan §Cluster C, tasks §4.1–4.4] — FIXED: re-counted after the three additions — 31 packaged (19 + 8 + 3 + 1), 34 rule-homes, 36 refusing probes, ~35 packaged fixture files; the FR-016 table stays 16 named / 16 homed.
- [x] CHK407 Is each negative required to carry exactly one violation, so a refusal cannot be ambiguous about its cause? [Clarity, tasks §Phase 4 preamble]
- [x] CHK408 Is the negative header dialect fixed to one convention, with the sibling family that owns the other convention named? [Consistency, research §Examples layout]

## The killed-flaw positives and the discriminations

- [x] CHK409 Are the four mandated positive cases each required, and each required to validate with ZERO findings? [Completeness, Spec §FR-017, §SC-002]
- [x] CHK410 Is the genuine per-unit pair specified concretely enough to be authored (differing in `achieved_scope`), rather than as "a per-unit pair"? [Clarity, Spec §FR-017]
- [x] CHK411 Is the genuine duty pair specified with BOTH admissible qualifications (differing permissions OR a declared rationale)? [Clarity, Spec §FR-017, §FR-038]
- [x] CHK412 Is the alias-pair negative required to sit in the SAME corpus as the genuine pairs, so the measurement is a discrimination rather than a refusal? [Measurability, Spec §SC-002, tasks §4.6]
- [x] CHK413 Is the discrimination required to be a SINGLE run producing three verdicts, so a rule broad enough to catch all three cannot pass? [Measurability, tasks §4.6, §10.5]
- [x] CHK414 Does every packaged example that is a positive also serve as the discrimination partner of a specific negative, so each negative's refusal is proven non-incidental? [Measurability, plan §Cluster C, §Cluster D]
- [x] CHK415 Is a `retired` entry — the third member of the lifecycle set — instantiated anywhere in the corpus? [Coverage, Spec §FR-013] — FIXED: no fixture carried one, so FR-013's "a retired entry MUST retain its record" was a guarantee nothing exercised. tasks §3.5 now carries a `retired` entry in the ledgerx fragment, and plan §Cluster C names it as a coverage positive (not a killed-flaw one).
- [x] CHK416 Is the `planned` positive required to be checked against BOTH of its guarantees (validates, and is not reported as missing)? [Coverage, Spec §FR-013, §SC-013]

## Where a rule can physically be proven

- [x] CHK417 Is the two-layer split (record-internal vs repo-context) stated with a rule for deciding which layer a given rule belongs to? [Clarity, research §Decision 7]
- [x] CHK418 Are the rules that CANNOT be proven by a packaged file identified, with the forcing argument for each? [Completeness, research §Decision 7, plan §Cluster C]
- [x] CHK419 Is the misplacement rule's home argued (a packaged example is itself outside the declared placement) rather than asserted? [Clarity, research §Decision 7]
- [x] CHK420 Is FR-011's obligation-resolution negative homed, after the plan gate found it unhomed? [Completeness, ruling A-11, plan §Cluster C]
- [x] CHK421 Is FR-014's citation-resolution negative homed, given that it is not in FR-016's named list? [Completeness, plan §Cluster C fixture 6]
- [x] CHK422 Are the repo-shaped fixtures each required to carry a REAL instance of the thing being resolved, so a finding proves non-resolution rather than an empty tree? [Measurability, tasks §4.5]
- [x] CHK423 Is the conformant repo fixture required to be the discrimination partner of every refusing repo fixture? [Measurability, tasks §4.5]
- [x] CHK424 Does the repo corpus measure the SCOPE of the uniqueness comparison as well as its content? [Coverage, Spec §FR-006] — FIXED: fixture 1 now carries two fragments for two clients with an identical tuple and asserts exit 0 (tasks §4.5), which is the measurement the fragment-scope rule needs.
- [x] CHK425 Is the cross-domain negative routed to the doc-health corpus, with the requirement that the intra-repo validator must NOT carry it? [Consistency, Spec §FR-023, research §Decision 7]
- [x] CHK426 Are the doc-health fixture fragments required to be intra-repo CONFORMANT, so the cross-domain finding is provably composition-only? [Measurability, tasks §6.5, §6.7, ruling A-N4]

## Corpus integrity

- [x] CHK427 Is the registration table required to make a probe and a file inseparable in both directions? [Completeness, Spec §FR-018]
- [x] CHK428 Is `red_proven` defined in the 006 sense (suppress the code, watch the corpus go red), so "the probe is load-bearing" is measured? [Measurability, tasks §10.1]
- [x] CHK429 Is the reproduction procedure for `red_proven` named rather than left to invention? [Clarity, tasks §10.1, §2.2]
- [x] CHK430 Are the packaged examples required to validate clean as a set, so an example cannot drift from the schema it demonstrates? [Coverage, Spec §US2-AS4, tasks §2.2]
- [x] CHK431 Is every fixture required to be free of credentials, provider payloads and tenant secrets? [Security, plan §Constitution IV]
- [x] CHK432 Are the example `evidence_ref` pointers required to name real pinned content, given they are never resolved by the validator? [Traceability, Spec §Assumptions, tasks §3.2]

## Notes

- Four items carried a defect (CHK404, CHK405, CHK415, CHK424) and one bookkeeping item
  (CHK406) followed from them. CHK405 is the sharpest: a NAMED FR-016 negative whose
  requirement specified only a behaviour, so the fixture would have passed and the
  self-test would have reported `negative-should-fail` at implementation time.
