---
code_surface: openxFactory (credential-contracts spec requirements; openXdox naming record draft->ratified; example dispatch/content credential records + validator support), omnigent-install (dispatch-App token-minter delivering short-lived tokens by reference into the inbox's env-named secret; QA dispatch-secret repoint), operator binding (org-owned "openXdox Intent Dispatch" GitHub App — org-admin provisioning, not code)
target_release: next additive contract bundle (allocated at realization per docs/contract-versioning-policy.md)
---

# Proposal: add-dispatch-credential-contract

## Why

The openXdox intent plane's dispatch credential — the token the intent inbox
carries to trigger the ONE apply workflow — was provisioned for the 2026-08-10
QA install as a **fine-grained personal access token under an individual's
GitHub account** (`dox-intent-inbox-qa-20260810`, never used). That is fragile
(it dies when that person rotates or leaves, and mis-attributes every automated
dispatch to them personally), but the deeper problem is that **nothing in the
contracts says how a dispatch credential must be held**, so the QA stopgap had
nothing to conform to. Two gaps:

1. **Least privilege and serving-tier separation are unwritten.** The whole
   intent-plane thesis — the serving surface holds *no* write authority — rests
   on the dispatch credential being dispatch-ONLY and never content-write
   capable. Yet the same capability also runs a *content* credential
   (`XFACTORY_APP`, `Contents: write`) inside CI, and nothing forbids reusing
   that App's key in the inbox. Reusing it would hand the internet-exposed,
   credential-"free" serving pod a key that can rewrite the corpus — silently
   collapsing the boundary the plane exists to enforce.

2. **Ownership and delivery must generalize to per-tenant installs.** xFactory
   installs per tenant, so the dispatch credential is a per-install concern, not
   a one-off. Brett's recorded **two-case worker-credential principle**
   (2026-08-11: neutral contract, operator as binding) already answers this for
   worker credentials — the contract is neutral (openxFactory), the vault
   operator is a per-install binding (OpsxFactory when licensed, the client's
   own IT channel when not). The dispatch credential is another face of the same
   fork and should inherit the same shape rather than reinvent it.

This change writes both invariants into `credential-contracts` and ratifies the
name of the capability whose credentials it contracts (**openXdox**).

## What Changes

- **ADD** (`credential-contracts`) the **dispatch-only least-privilege +
  serving-tier separation** requirement: a trigger-only credential is scoped to
  exactly its one named target (`actions: write` on the single workflow repo),
  carries no contents authority, is a DISTINCT binding from any content-write
  credential, and a zero-write-authority serving surface holding it MUST NOT
  hold — nor hold key material able to mint — a content-write credential.
- **ADD** (`credential-contracts`) the **reference-delivered, operator-as-
  binding** requirement: any install-materialized credential is delivered by
  vault reference + fetch identity, materialized ephemerally (never baked into
  image/config/log), with the vault OPERATOR a per-install binding and the
  neutral contract living in openxFactory (never an operator domain) so a domain
  licensed WITHOUT the operator can still realize it — the lane/serving code
  identical across bindings. This generalizes the worker-credential principle to
  any runtime credential.
- **RATIFY** the openXdox naming record (`docs/openxdox-naming.md`,
  `draft -> ratified`, `Ratified by: add-dispatch-credential-contract`).
- **Realize (downstream)** the openXdox dispatch binding as the recommended
  shape: an **org-owned GitHub App** (`Actions: write` on the factory repo)
  with a **token-minter** delivering short-lived installation tokens by
  reference into the inbox's env-named secret — which keeps the deliberately
  stdlib-only inbox unchanged (it still reads a token by name; the crypto never
  enters the credentialed serving component). The existing `XFACTORY_APP` stays
  the separate content-write binding. The neutral contract still permits a
  client-provided credential where a self-hosted tenant's policy forbids
  installing Apps.

## Impact

- **`credential-contracts` capability**: two ADDED requirements (+ example
  records and validator support at realization).
- **openXdox naming record**: `draft -> ratified`.
- **Enables**: moving the QA openXdox dispatch credential off the personal PAT
  onto the org-owned App binding; every future tenant install inherits the
  neutral contract with its own operator binding (operator-hosted or
  self-hosted).
- **Retires**: the personal-PAT stopgap `dox-intent-inbox-qa-20260810`.
- **Sibling, out of scope**: the worker/model-provider credential the two-case
  principle flagged for its own `credential-contracts` addition — the same
  reference-delivery requirement here covers its shape, but its family/broker
  records are a separate change.
