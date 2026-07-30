# doxBench Runtime Refresh Dogfood Acceptance Erratum

Status: record
Kind: report
Captured: 2026-07-29
Repository context: openxFactory
Corrects: `docs/doxbench-runtime-refresh-dogfood.md`, Acceptance Observation item 3
Summary: Records the governing interpretation of the doxBench runtime-refresh acceptance pass without mutating its original evidence marker.
Topics: doxbench, ideation-dashboard, snapshot-source, runtime-refresh, doc-workflow

## Correction

The original dogfood marker included an over-strict third observation: serving
the post-image file through `/source`. That route is a separately governed
pass-through bound to the served checkout, not the runtime snapshot-backed
document view exercised by `add-dashboard-repo-selector` task 6.2.

The governing pass condition is therefore:

1. the refreshed hosted snapshot names the source revision containing the
   marker;
2. the snapshot lists the marker path in `documents`; and
3. the snapshot-backed document view makes the marker available without an
   application image rebuild or workload rollout.

The 2026-07-29/30 live pass satisfied those conditions. The same experiment
also confirmed that `/source` does not expose a file added after the image's
served checkout was baked. That known plane boundary is recorded openly but is
not evidence for, or a blocker to, the runtime snapshot-refresh task.

This erratum leaves the original `Status: record` document byte-for-byte
unchanged and supplies the correction as a new immutable evidence record.
