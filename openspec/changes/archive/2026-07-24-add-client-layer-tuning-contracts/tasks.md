# Tasks — add-client-layer-tuning-contracts

## 1. Roster
- [x] 1.1 `templates/client-layer/roles/house-style.yaml` (locked floor,
      tunable ranges).
- [x] 1.2 Eleven persona/capability objects per the ratified roster draft
      (v1 trait scale; FAO + cost-reporting; liaison as capability).
- [x] 1.3 Scaffold delta: `cost_reporting_steward` + roles/ reference.

## 2. Contracts
- [x] 2.1 Schemas: client_policy_overrides, client_memory_boundaries,
      client_integration_boundaries, hermes_client_overlay.
- [x] 2.2 Examples + intended-reason negatives.
- [x] 2.3 contracts/client-content/README.md.

## 3. Validator
- [x] 3.1 `scripts/validate-client-content.py`: schema checks + the
      comparability spec (subset/superset/ceiling/floor/add-only/ordered;
      review_required fallback) + self-test.

## 4. Close out
- [x] 4.1 Manifest registration + bundle allocation at realization;
      contracts README row; CHANGELOG.
- [x] 4.2 Strict validate + repo validator suite green; staging INDEX
      updated (first client-layer-tuning exit raised).

## Bookkeeping correction (2026-08-23, `govern-openspec-corpus-membership`)

`proposal.md` real line 5 was respelled `Ratified by:` to `Ratified:` by slice
5B of `govern-openspec-corpus-membership` — the prefix only. Every byte after
the colon is carried verbatim, asserted identical at the edit, so the original
line is recovered exactly by reading `Ratified by:` back in its place and
nothing else on the page moved. The ruling is OQ-4's RULED extension of
2026-08-23 (Brett Heap, in-session), which widens the class to the sixteen
lines whose named change id is the DOCUMENT'S OWN. A change is not its own
approving change, and such a line passed `fam_ratified_provenance` only by
self-reference. This one emitted NO finding, so the respell is corrective
rather than a discharge and clears nothing from the census. The record that
justifies this line is the user approval of 2026-07-24 named on the line,
carried into the record by commit `95ac6dd` of the same day, "Archive
add-client-layer-tuning-contracts (ratified 2026-07-24, live-proven)". An
append on a single-valued header is mechanically impossible —
`doc_health.corpus.STATUS_RE` swallows any trailing annotation — so this is an
in-place overwrite and an extension of Brett's 2026-08-10 append ruling, named
as one, and it is entered in `docs/archive-record-discrepancies.md`.
