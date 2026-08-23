# Data Model — 011-council-feature-clearance

No persisted entities created. Logical entities the widened lane touches:

### CandidateClass (envelope entry — declared, not invented)

Fields per schema v1: `id`, `description`, `target_repos[]`, `expected_author`,
`expected_head_ref` (exact), `path_allowlist[]`. First-tranche entries name
feature-effort branches in `opensoft/xFactory` / `opensoft/openxFactory`.
Classification intent is NOT an envelope field — advisory posture emerges from
tier-2 state (research R2/R4).

### RefusalRecord (produced)

Named preflight outcomes (`parked_never_clearable`, stale-target, …) emitted in lane
runs for non-clearable classifications; idempotent per head SHA; no runtime job is
created behind a refusal.

### VerdictCheckRun (produced, unchanged shape)

`council-verdict/merge-readiness` on the candidate head SHA; `.app.id` must equal
`vars.COUNCIL_LANE_APP_ID`; conclusion reports transport conformance, never favorability.

Relationships: one CandidateClass entry ↔ many PR instances over time (per-effort);
RefusalRecord and VerdictCheckRun are mutually exclusive per classification outcome.
