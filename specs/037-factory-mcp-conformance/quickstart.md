# Quickstart

Status: draft
Kind: implementation

Run from the repository root inside py-bench:

```sh
python3 -m unittest discover -s tests/factory-mcp -p 'test_*.py' -v
python3 -m pytest tests/factory-mcp -q
python3 scripts/validate-openspec-cli-pin.py --all --strict
```

The third line validates through the repository's PINNED OpenSpec CLI. A bare
`openspec` on PATH is unpinned; the 2026-09-07 records used one and its result
agreed with the pinned run (2026-10-05 addendum in [tasks](tasks.md)).
The change archived on 2026-10-06, so `--change add-factory-mcp-conformance`
no longer resolves; `--all` validates its requirements as the promoted
[`factory-mcp-conformance`](../../openspec/specs/factory-mcp-conformance/spec.md)
specification.

Runbook: docs/factory-mcp-conformance.md. Synthetic inputs require no live credentials.
