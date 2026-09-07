# Quickstart

Status: draft
Kind: implementation

Run in the feature worktree inside py-bench:

```sh
python3 -m unittest discover -s tests/factory-mcp -p 'test_*.py' -v
OPENSPEC_TELEMETRY=0 openspec validate add-factory-mcp-conformance --strict
```

Runbook: docs/factory-mcp-conformance.md. Synthetic inputs require no live credentials.
