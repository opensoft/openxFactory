# Avatar F0 Brokered-Call Feasibility — Results (live run)

Change: qualify-avatar-brokered-call-feasibility

## Overall: PASS

| Group | planned | completed | passed | failed |
| --- | --- | --- | --- | --- |
| F0-A | 20 | 20 | 20 | 0 |
| F0-B | 10 | 10 | 10 | 0 |
| F0-C | 10 | 10 | 10 | 0 |
| F0-D | 10 | 10 | 10 | 0 |
| F0-E | 10 | 10 | 10 | 0 |
| F0-F | 10 | 10 | 10 | 0 |

## Assertions

- `F0-A-ORDERING`: PASS (passed 20, failed 0)
- `F0-A-SINGLE_CALL`: PASS (passed 20, failed 0)
- `F0-B-ORDERING`: PASS (passed 10, failed 0)
- `F0-B-WITHIN_CEILING`: PASS (passed 10, failed 0)
- `F0-C-NO_MEDIA`: PASS (passed 10, failed 0)
- `F0-C-READINESS_TIMEOUT`: PASS (passed 5, failed 0)
- `F0-D-TERMINAL_5S`: PASS (passed 10, failed 0)
- `F0-D-NO_LATE_IO`: PASS (passed 10, failed 0)
- `F0-E-SINGLE_CALL`: PASS (passed 10, failed 0)
- `F0-F-IDEMPOTENCY`: PASS (passed 10, failed 0)
- `F0-D-INTERRUPTED`: PASS (passed 0, failed 0)
- `F0-D-BOUNDED_CLEANUP`: PASS (passed 0, failed 0)

## Redaction / threat-model disposition

Evidence carries only hashes, bounded reason codes, and monotonic offsets — no SDP, credential, raw call id, transcript, media, or high-cardinality identifier. The record is re-scanned before writing and a finding fails the run closed.

## Reviewer decision

Terminal `PASS` record from the supervised live lab run.
