# Design: add-dispatch-credential-contract

## Context

The intent inbox (Omnigent-Install `intent_inbox/server.py`) already reads its
dispatch token by env-var NAME at call time — "manifests name, never carry it"
— and its container is deliberately **stdlib-only, no pip dependencies** (the
one credentialed serving component, kept minimal on purpose). That indirection
is what makes the serving tier binding-neutral for free: the contract can swap
what backs the referenced secret without touching inbox code.

## Decisions

### D1 — Two invariants, not a mechanism
The spec adds INVARIANTS (least-privilege + separation; reference-delivery +
operator-binding), not a chosen credential technology. A bot-account PAT, a
client-provided scoped token, and an org-owned App can all satisfy the
contract. This keeps the neutral contract honest across the two install cases.

### D2 — GitHub App is the recommended binding, but not mandated
For the operator-hosted case (and as the shape opensoft ships), the dispatch
binding is an **org-owned GitHub App** — GitHub's multi-tenant primitive: one
registration, N per-tenant installations, per-installation short-lived tokens,
no personal account, org-revocable. A per-tenant bot account or PAT does not
scale as a product (N accounts × N hand-minted tokens). The contract stays
neutral so a self-hosted tenant whose policy forbids third-party Apps may
supply a scoped credential through their own IT channel instead.

### D3 — The minter lives in the binding, never in the inbox
A GitHub App authenticates by RS256-signing a JWT, which Python's stdlib cannot
do — so minting an App token inside the inbox would force a crypto dependency
into the stdlib-only credentialed component AND place the App private key (which
can mint tokens indefinitely) in the long-running, internet-exposed pod. Both
are rejected. Instead a **token-minter** (operator platform minter, or an
in-estate CronJob for self-hosted) turns the App key into short-lived
installation tokens and writes them to the vault by reference; the inbox reads
the token by env-name, unchanged. This mirrors the worker-credential pattern
(vault-reference, ephemeral materialization) beat for beat. The exact minter
topology (CronJob vs scheduled-Action vs sidecar) is resolved at realization.

### D4 — Dispatch and content are separate bindings
The dispatch App (`Actions: write` on the factory repo, held by the inbox) and
the content App (`XFACTORY_APP`, `Contents: write` on the corpus, held in CI)
are DISTINCT identities on different repos with disjoint permissions. Token
downscoping does not substitute for separation: an App private key in the pod
retains the App's full capability regardless of how narrowly a given token is
requested, so only a separately-permissioned identity enforces "dispatch-only"
at the key level.

## Relationship to prior records

- The reference-delivery / operator-as-binding requirement generalizes the
  **two-case worker-credential principle** (Brett, 2026-08-11) from worker
  credentials to any install-materialized credential.
- This change is the lifecycle **ratification vehicle** for
  `docs/openxdox-naming.md` (the capability whose credentials it contracts).
