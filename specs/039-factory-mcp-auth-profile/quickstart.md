# Quickstart: Factory MCP authorization profile

Status: draft
Kind: runbook

Run from the repository root, in a Python environment built from CI's lock
(`research.md` R-11), kept outside the repository tree:

```sh
VENV="$HOME/.venvs/factory-mcp"
python3 -m venv "$VENV"
"$VENV/bin/pip" install --require-hashes -r requirements/hermes-runtime-contracts.lock
```

## Validate the two synthetic examples

```sh
"$VENV/bin/python" scripts/validate-factory-mcp.py \
  contracts/factory-mcp/examples/declaration.example.json \
  --snapshot synthetic@aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa=contracts/factory-mcp/examples \
  --json
"$VENV/bin/python" scripts/validate-factory-mcp.py \
  contracts/factory-mcp/examples/declaration-deployed.example.json \
  --snapshot synthetic@aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa=contracts/factory-mcp/examples \
  --json
```

Expected for both: exit 0, `valid-with-gaps`, no diagnostic,
`verified_conformance: false`. The not-deployed example reports the gap
`audit-gap`. The deployed one reports `audit-gap` and `auth-gap`, because its
block is supported by a gap and not by an observed server.

## Run the tests

```sh
"$VENV/bin/python" -m pytest tests/factory-mcp -q
```

## Reproduce the red-first and mutant runs

The commands, their trees and their results are recorded in
[`verification.md`](verification.md): the test commit run against `main`'s
validator, and the two classification tests run against a mutant whose
classification comparison is removed (`research.md` R-14).

## Validate the governance records

```sh
python3 scripts/validate-openspec-cli-pin.py --all --strict
```

This validates through the repository's pinned OpenSpec CLI, never a bare
`openspec` on `PATH`.
