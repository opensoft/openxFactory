# D10 Hosted Refresh Marker

Status: record
Kind: report
Captured: 2026-07-31
Repository context: openxFactory
Summary: Content-neutral marker for the D10 Step C deliberate hosted-refresh observation — proves the hosted doxBench surface exposes a document published after its image was built, with no rebake.
Topics: doxbench, ideation-dashboard, runtime-refresh, acceptance-evidence

## Purpose

This record is the distinct `main`-landed document for Step C of the D10
combined real-corpus acceptance pass (`add-workbench-integrated-editor-chat`
task 1.3, runbook `d10-acceptance-runbook.md`). Its path and title are the
observable marker:

- `docs/d10-hosted-refresh-marker.md`
- `D10 Hosted Refresh Marker`

The deliberate human observation it supports: land this document on `main`
through an ordinary governed path, dispatch the publication lane, click
refresh on the hosted dashboard, and find this document — with the hosted
image digest identical before and after.

## Authority boundary

Identical to the 2026-07-29 predecessor marker
(`doxbench-runtime-refresh-dogfood.md`): the publication lane writes the
derived snapshot through its existing governed CI path; the hosted surface
only re-fetches published data. Nothing in this step builds an image,
rolls out a workload, or writes repository content from the dashboard.

## Immutability

This record is immutable evidence once captured. Per the predecessor's
erratum lesson, any future correction lands as a separate record, never as
an edit to this one.
