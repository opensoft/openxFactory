# Tasks: Ideation Cross-Reference Readiness Index

## 1. Sequencing And Contract Baseline

- [ ] 1.1 Follow the declared delta order (semantic sweep, cataloging, routing, proposal origin); before realization, verify the promoted doc-health wording matches what this change's enumeration delta was declared against, rebase if needed, and re-run strict OpenSpec validation.
- [ ] 1.2 Verify this change's staged-origin `.openspec.yaml`, support-manifest origin repetition, and staging-header linkage.

## 2. Index Contract (openxFactory)

- [ ] 2.1 Define the cross-reference index schema: topic entry with stage column, member documents with repository/path/stage, tag sources (`Topics:`, `Target capabilities:`, later catalog tags), extension-fit note, per-tier scores with evidence references, conflict flags, and recommendation state.
- [ ] 2.2 Add valid and invalid examples: multi-stage cluster, promoted-fit citation, explicit no-promoted-fit entry, archive-pointer-only fit note (invalid), score out of range, missing tier with reason, spread conflict, and a gated recommendation.
- [ ] 2.3 Implement a strict `validate-ideation-cross-reference.py` validator (schema, stage vocabulary, score ranges, evidence-reference completeness, fit-citation resolution against promoted specs) and wire it into the per-repo validator preflight.
- [ ] 2.4 Bootstrap the initial `ideation/cross-reference.md` from the current headers and update ideation guidance to reference the promoted requirements without duplicating them.

## 3. Readiness Worker (codexFactory)

- [ ] 3.1 Add the readiness-scorer module with a versioned prompt contract producing three independent tier scores (domain, company, project/buildability) per topic cluster.
- [ ] 3.2 Reuse the organizer/cataloger evidence contract verbatim for every score — committed source revision, passage hash and section reference, rationale, confidence, alternatives, `pending_review` disposition — and validate worker output against it before persistence.
- [ ] 3.3 Implement cluster membership from the header tag sources with deterministic tie-breaks, and the additive catalog-tag fold-in path guarded off until `document-cataloging` realizes.
- [ ] 3.4 Implement the minimum-score gate, the unscoreable-tier block, the spread-conflict flag, and the extension-fit citation check emitting `ideation-readiness` findings.
- [ ] 3.5 Enforce the non-mutating bound: the pass writes only the index and evidence artifacts; add tests proving any other write path is rejected.

## 4. Nightly Lane (xFactory aggregation, omnigent-install)

- [ ] 4.1 Wire the readiness lane into the nightly run after the deterministic pass, consuming its inventory snapshot; a skipped or failed lane is reported as skipped and never affects deterministic results.
- [ ] 4.2 Add the bounded read-only readiness-scorer profile in omnigent-install reusing the existing document-analysis host pattern, with workload-specific readiness assertions and no repository credentials in the worker environment.
- [ ] 4.3 Link the index and evidence artifacts from the dated report; recommendations appear in the ranked plan as `contested`, at most `warning`, report-only items.

## 5. Tests And Records

- [ ] 5.1 Add tests: gate fires only at minimum >= 8; one low tier blocks despite two 10s; spread conflict flagged below threshold; recommendation performs no state transition; tag bootstrap reads both header fields; evidence contract validates against the existing organizer/cataloger schema; absent findings from a skipped lane are not treated as resolved.
- [ ] 5.2 Keep the openxFactory README "OpenSpec Records" entry current through ratification, realization, and archive.
