# Tasks: Neutralize Job Envelope

## 1. Canonical Schemas (openxFactory)

- [x] 1.1 Loosen envelope: repository/feature_id optional, job_type free
      string, add the seven neutral references.
- [x] 1.2 Loosen run/event schemas the same way (feature_id optional,
      engineering enums relaxed to strings where present).
- [x] 1.3 CHANGELOG contract-v1.5 (additive/loosening).

## 2. Engineering Overlay (cross-repo: codexFactory)

- [x] 2.1 Add schemas/engineering-job-envelope.overlay.schema.yaml
      re-tightening job_type enum and repository/feature requirements.
- [x] 2.2 Declare `specializes` in codexFactory stack.yaml.

## 3. Neutrality Test

- [x] 3.1 Validate every example envelope/run/event document in
      openxFactory against the loosened schemas (must pass unchanged) and
      the engineering examples against the overlay (must pass strictly).

## 4. Register

- [x] 4.1 DTN-003 -> openspec at proposal, -> adopted after 2.x and 3.x;
      staged topic exit recorded.

## 5. Validation

- [x] 5.1 openspec strict passes for this change and --all.
