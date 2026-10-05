# Public interface

Status: draft
Kind: implementation

Schemas: `contracts/factory-mcp/`. Implementation: `scripts/validate-factory-mcp.py`.

CLI accepts declaration path and explicit --snapshot repository@revision=path mappings; --json returns dimensions, stable diagnostics and gaps. Exit 0 valid/valid-with-gaps, 1 invalid, 2 unreadable input/unavailable roots. No network/dynamic imports or certification.

Additive opt-in. Exact projections and bounds are documented in the completed runbook; no adoption pin is changed.
