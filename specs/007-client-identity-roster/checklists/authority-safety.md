# Authority and Safety Checklist: Client Identity Roster

Status: draft

**Purpose**: Release-gate validation of the requirements that carry the authority
argument — consent as the root, no secrets in the tree, fail-closed defaults, the
identity axis's blast-radius reasoning, and the guarantee that nothing here can widen
anyone's access.
**Created**: 2026-08-14
**Feature**: [spec.md](../spec.md)

## Authority roots

- [x] CHK1601 Is BOTH roots required on every entry (the ratified capability AND the consent instrument)? [Completeness, Spec §FR-014]
- [x] CHK1602 Is the principle stated that our own ratification never by itself justifies standing in another party's tenant? [Clarity, Spec §FR-014, proposal §item 11]
- [x] CHK1603 Is the consent citation required to RESOLVE, with presence explicitly insufficient? [Fail-closed, Spec §FR-014]
- [x] CHK1604 Is "in force" defined against a closed lifecycle rather than by the existence of a record? [Clarity, Spec §FR-014]
- [x] CHK1605 Is a `mutate` entry with no ratified capability required to BLOCK rather than report? [Fail-closed, Spec §FR-014]
- [x] CHK1606 Is the asymmetry between the two citations (instrument resolves; capability does not, in this release) recorded as a reading with its reason? [Honesty, Spec §FR-014, plan §decision 19]
- [x] CHK1607 Is consent withdrawal required to reach the identity and its provider-side admission rather than only its credentials? [Completeness, Spec §FR-026]
- [x] CHK1608 Is the reason that matters stated (revoking a credential leaves the identity registered and still admitted)? [Clarity, Spec §US4, proposal §consent-instrument]

## Blast radius and the axis

- [x] CHK1609 Is the axis's rationale carried (the identity is the unit of grant for every provider-side scoping mechanism)? [Traceability, proposal §item 3]
- [x] CHK1610 Is structural enforcement preferred over logical, with logical admissible only where no per-unit principal exists? [Fail-closed, Spec §FR-008]
- [x] CHK1611 Is the conversion of a structural bound into a logical one required to be declared, checkable and tested rather than merely noted? [Measurability, Spec §FR-002, §FR-010]
- [x] CHK1612 Is the gate obligation required to RESOLVE and to name a refusal test, so an obligation cannot be decorative? [Fail-closed, Spec §FR-011]
- [x] CHK1613 Is the reason stated (an unenforced obligation converts an undetected widening into a documented one)? [Clarity, Spec §FR-011, §Edge Cases]
- [x] CHK1614 Is residency required to distinguish the registration's home tenant from the tenants its principals occupy? [Completeness, Spec §FR-012]
- [x] CHK1615 Are the vendor-tenant-multi obligations required in full, including a consent amendment per affected client? [Completeness, Spec §FR-012]
- [x] CHK1616 Is the "vendor-homed but principal appears in the client tenant" evasion explicitly refused? [Fail-closed, Spec §FR-012]
- [x] CHK1617 Is per-domain identity separation protected as the thing that preserves provider-side attribution and independent revocation? [Constraint fidelity, Spec §FR-024]

## Secrets, credentials and standing access

- [x] CHK1618 Is credential minting forbidden by requirement, including inside tests? [Fail-closed, Spec §FR-029, §SC-012]
- [x] CHK1619 Is the tree required to carry no credential, provider payload or tenant secret, including in the packaged worked case? [Security, plan §Constitution IV]
- [x] CHK1620 Is the standing-credential attestation required on every entry, with a defined falsification? [Completeness, Spec §FR-013]
- [x] CHK1621 Is that falsification required to be record-internal, so no check can be tempted to read a credential store? [Fail-closed, Spec §FR-013, plan §Cluster A]
- [x] CHK1622 Is the refusal lever (withhold OUR credential) distinguished from remediation (mutate THEIR tenant), with the reason the second is unacceptable? [Clarity, Spec §FR-027, §FR-028]
- [x] CHK1623 Is the refusal's predicate deterministic and stated, so issuance cannot be refused or allowed by judgement? [Clarity, Spec §FR-035]
- [x] CHK1624 Is the JIT discipline and the existing credential record shape explicitly unchanged? [Scope, Spec §FR-030]

## Fail-closed defaults

- [x] CHK1625 Does every closed set refuse an unrecognized value rather than warning? [Fail-closed, Spec §FR-034]
- [x] CHK1626 Is a free-text precondition explicitly refused, with the reason it is unenforceable? [Fail-closed, Spec §FR-028]
- [x] CHK1627 Is an unverified admission act excluded from effective reach by default rather than counted until disproven? [Fail-closed, Spec §FR-003]
- [x] CHK1628 Is a claimed verification with no evidence refused rather than downgraded silently? [Fail-closed, Spec §FR-002] — FIXED this pass.
- [x] CHK1629 Is a harness error required to exit distinctly from a clean run, so a broken check cannot read as a pass? [Fail-closed, Spec §FR-015]
- [x] CHK1630 Is a nonzero exit required to FAIL the domain gate rather than to warn? [Fail-closed, Spec §FR-022]
- [x] CHK1631 Is the pack's absence behaviour prevented from becoming a fail-open hole (exit 0 WITH a notice, and only for absence)? [Fail-closed, Spec §FR-022, §SC-013]
- [x] CHK1632 Is the one deliberately permissive area (the enrollment axis) bounded by requirements that keep it from becoming a coverage claim? [Clarity, Spec §FR-032, §SC-013]

## Notes

- One item carried a defect (CHK1628), fixed with the verification-pair rule.
- The authority argument survives the pass intact: consent is the root, both citations
  are required, the drift lever mutates nothing in the client's estate, and no artifact
  or test in the feature can widen access anywhere.
