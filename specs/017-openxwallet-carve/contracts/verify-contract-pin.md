# Contract: `scripts/verify-contract-pin.py`

**Feature**: `017-openxwallet-carve` · **Authority**: task 3.17, design D7,
clarification N1, proposal § P2 requirement (iii)

## CLI

```
python3 scripts/verify-contract-pin.py
```

No arguments. No options. The pin file is found relative to the script's parent
directory, so the tool works from any working directory inside the repository.

## Reads

- `contract_pin.yaml`
- every path listed under its `files:`

**Nothing else.** No network. No upstream tree. No `contracts/manifest.yaml` — the
live cross-check is a SYNC-TIME obligation, never a CI read (the offline law).

## Exit codes

| Code | Condition |
| --- | --- |
| `0` | every named file present AND its recomputed sha256 equals the recorded one |
| `1` | drift; a named file missing; a recorded digest missing or empty; `commit` missing, empty, or not 40-hex; the pin unparseable |
| `2` | environment: `contract_pin.yaml` absent, or PyYAML unavailable |

## Fail-closed pre-sync

Adopted from openAvatar's doctrine and asserted as behaviour, not prose:

1. An empty or absent `commit` is **not content-addressed** → reject.
2. A recomputed digest **can never equal an empty recorded digest** → drift →
   fail before any test runs.

## Refusal contract (N1)

Every non-zero exit prints the finding and then, on its own lines:

```
  remediation: git submodule update --init openXwallet
  remediation: see docs/pin-resync-runbook.md
```

Both strings are required. A refusal that names what is wrong without naming what
to run puts the exit in tribal memory instead of in the message.

## Position in CI

FIRST step of the `wallet-validation` job, before the syntax gate and before the
validator — because the validator checks only
`ENVELOPE_SCHEMA_PATH.is_file()` (presence, not identity) while rule (g) reads the
approval-scope vocabulary out of that same file.

## Proof obligation (V8)

Two runs are evidence, not one:

- a GREEN run whose log shows the verification happened before the validator step
  started;
- a RED run against a deliberately mutated vendored copy.

A verifier that has never refused is not known to refuse.
