# Validator CLI Contract

## Commands

```text
python3 scripts/validate-intent-compliance.py
python3 scripts/validate-intent-compliance.py --trusted-repository <checkout> --trusted-repository-id <owner/name> --trusted-commit <commit> <candidate-records>
python3 scripts/validate-intent-compliance.py --strict --trusted-repository <checkout> --trusted-repository-id <owner/name> --trusted-commit <commit> <candidate-records>
```

The default command validates all schemas and runs the complete packaged
positive and negative static conformance corpus. A target argument requires an
out-of-band trusted Git checkout, canonical repository ID, and full commit,
runs self-test first, loads
the complete authoritative family from that exact tree, and validates submitted
decisions against it. Strict mode treats absence of applicable decisions as a
finding.

## Exit codes

- `0`: schemas, packaged corpus, and requested repository are conforming.
- `1`: one or more deterministic contract findings were emitted.
- `2`: validator harness, schema, dependency, or fixture metadata is invalid.

## Finding contract

Each finding renders a stable machine code, source path, and bounded message.
Negative fixtures declare their expected code and governing requirement in
header comments; the self-test fails if the intended finding is absent, a
requirement has no negative probe, or a fixture claims an unknown requirement.

## Runtime boundary

The validator checks static dispatch-evidence identity and digest bindings. It
does not issue credentials or claim replay prevention, atomic consumption, or
worker invocation. Consuming domain runtimes own and test those guarantees.
