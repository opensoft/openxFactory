# Implementation Plan: Factory MCP advisory conformance

Status: draft
Kind: implementation

Branch: 030-factory-mcp-conformance | Date: 2026-09-07 | [Spec](spec.md)

## Summary

Draft 2020-12 JSON Schema; Python jsonschema plus an offline reference resolver and deterministic semantic passes. Synthetic fixtures exercise all three repetition modes. Codex mapping cites immutable source without shipping domain behavior.

## Technical Context

Python 3.11+, installed jsonschema and existing repository modules; unittest, fake clocks and synthetic fixtures in py-bench. Local Linux CLI/callable. No durable storage or deployed service. Bounds: input 256 KiB, artifact/observation 1 MiB, output 256 KiB, collections 256 items, bounded strings. Host may tighten callable bounds. No remote resolution. Synchronous injected readers must cooperate with deadlines; no enforced cancellation claim.

## Constitution Check

Pre-research and post-design PASS. Recorded ratification governs behavior. Domain ownership preserved. Closed schemas and failing tests precede behavior. Legacy contracts unchanged. Redacted deterministic evidence. Unreleased opt-in artifacts allocate no release version; release and pins are later realization. Existing unrelated validator failures are recorded and prevent a green merge claim. No exceptions.

## Project Structure

- contracts/factory-mcp/: schemas and synthetic examples.
- scripts/validate-factory-mcp.py: validator/callable.
- tests/factory-mcp: deterministic tests.
- docs/factory-mcp-conformance.md: integration runbook.
- This feature: research, data-model, contracts, checklists, tasks, verification.

## Strategy

Schemas → failing tests → trusted resolution → semantic evaluation → mapping → verification. No deployment, live reader, acceptance or pin update. Archive only after merged green evidence.
