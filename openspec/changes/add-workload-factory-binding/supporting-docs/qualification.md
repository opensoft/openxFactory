# Isolated candidate realization

Date: 2026-11-11. Status: draft profile with locally qualified candidate source.

The sole implementation feature is `opensoft/openXwallet`,
`specs/016-factory-workload-binding/`, branch `016-factory-workload-binding`.
Local candidate commit: `ab49ea04bdd1f20b80e558969f93a2c58fe473fd`.
Its `evidence.md` records **405 passed**, including **124 binding tests**, with
zero failures/errors/skips in a fresh dependency environment.

This factory packet's code-surface/target-release suites passed **252 tests**.
The new proposal passes pinned strict OpenSpec cleanly. The wider factory corpus
retains its one existing accepted add-chain-attestation finding, with zero
undispositioned failures; no exception or floor changed.

The reference flow verifies real signatures over synthetic workload evidence,
independent observer-launched worker measurement, current wallet/grant chains,
durable replay refusal and real owning mutual-TLS custody. Worker resolve
succeeds while a valid canonical worker sign request refuses. An excess-permission
mutation proves that denial probe detects accidental permission. Success and
failure cleanup plus an independent audit found no owned process/key-state path.

Tested source/test/workflow/dependency snapshot SHA-256:
`ca76249382b2d2b8aa9212c26b1b4efede1e06f069358c1d17acb0864a07d659`.
The snapshot algorithm and owning neutral source identities are in the feature's
evidence record. No published contract, release or consumer pin advances.

Hosted CI, live GitHub issuer/environment assurance, deployed independent
supervisor and signer confinement, owner ratification, human approval and attended
pilot qualification remain separate. Same-user fixture processes do not establish
hostile operating-system isolation. No PR, release or activation occurred.
Feedback stays deferred and neither historically denied write was replayed.
