# Recovery decisions

Status: record

## Compatibility baseline

Decision: preserve current main at `cc775fea08dab6ba64c27bb7aa3bb71ed607649b`.
Rationale: the old modular branch predates upload, hosting, corpus and session
fixes. Alternative: wholesale cherry-pick; rejected because it loses those fixes.

## Existing package

Decision: recover typed records, explicit provider boundary, isolated state,
focused tests and compatibility facades from `702a93a4490cadf733d84c4ee88507943c6b6b6e`.
Rationale: retain useful work rather than rewrite the whole CLI during cleanup.
Alternative: publish the old branch as-is; rejected for the same compatibility risk.

## Checker provenance

Decision: restore the original programming checker from local oh-my-opencode
blob `4270ef321d4303ce90ed5afefe2460944458e9b6` into operator-local storage
and pass PROGRAMMING_CHECKER explicitly. Rationale: the normal cached package
is unavailable; the gate must not skip a checker. No implementation unknowns
or new technology selections require external research.

## Historical evidence

Decision: retain the original snapshot in the verified external bundle and
replace its checked task ledger with one current Speckit handoff. Rationale:
old results do not prove current behavior, and implementation tasks have one owner.
