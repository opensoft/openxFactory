# Public interface

Status: draft
Kind: implementation

Schemas: `contracts/factory-mcp/`. Implementation: `scripts/validate-factory-mcp.py`.

CLI accepts declaration path and explicit --snapshot repository@revision=path mappings; --json returns dimensions, stable located diagnostics and gaps. Exit 0 valid/valid-with-gaps, 1 invalid (including malformed or oversized input), 2 unreadable input/unavailable roots, output past its 256 KiB bound (output_size_limit, printed in place of the oversized report) or a usage error such as a malformed --snapshot. No network/dynamic imports or certification.

Outcome inventories may name an optional `discriminator` property for unions of object branches (2026-10-05 addendum in [tasks](../tasks.md)).

Additive opt-in. Exact projections and bounds are documented in the completed runbook; no adoption pin is changed.
