# doxBench Runtime Refresh Dogfood Record

Status: record
Kind: report
Captured: 2026-07-29
Repository context: openxFactory
Summary: A durable marker used to prove that doxBench can display a document published after its application image was built.
Topics: doxbench, ideation-dashboard, snapshot-source, runtime-refresh, doc-workflow

## Purpose

This small, content-neutral record is the post-image document for the
`add-dashboard-repo-selector` live acceptance pass. Its repository path and
title are the observable marker:

- `docs/doxbench-runtime-refresh-dogfood.md`
- `doxBench Runtime Refresh Dogfood Record`

After this record lands on `main`, the aggregation publication lane regenerates
the `openxFactory` snapshot. A hosted doxBench refresh must then fetch that
newer snapshot and expose this path without an application image rebuild or
workload rollout.

## Authority Boundary

The publication lane writes the derived snapshot through its existing governed
CI path. The hosted doxBench surface only re-fetches that published data. It
does not write repository content, dispatch publication, build an image, or
roll out a workload.

## Acceptance Observation

The acceptance pass is complete when the hosted snapshot:

1. names the `openxFactory` commit containing this record as its source
   revision;
2. lists this exact path in `documents`; and
3. makes the record available in the snapshot-backed document view.

The separately governed `/source` pass-through reads from the served checkout;
it is not the runtime snapshot-backed document view and is not an acceptance
criterion for this refresh pass.

The OpenSpec task ledger and deployment evidence carry the resulting revisions
and timestamps; this record remains durable evidence of the document used.
