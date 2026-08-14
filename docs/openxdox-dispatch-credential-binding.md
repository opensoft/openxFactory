# openXdox Dispatch-Credential Binding Runbook

Status: draft
Kind: reference
Repository context: openxFactory
Purpose: bind the openXdox intent-plane dispatch credential to a real provider
per install, in either operating case, without an Opensoft identity performing
the privileged change on a self-hosted tenant's estate.

This is the operator-neutral realization of the
[`credential-contracts`](../openspec/specs/credential-contracts/spec.md)
dispatch requirement for **openXdox** (see the
[naming record](openxdox-naming.md) and `add-dispatch-credential-contract`). The
serving inbox is identical in every case: it reads a short-lived dispatch token
from a mounted, rotating file — it never holds an App key or a long-lived PAT.
Only the **binding** (who owns the credential and who mints the token) differs,
exactly per the [two-case worker-credential principle](../ideation/staging/hermes-stack-topology-per-client/hermes-stack-topology-per-client.md):
the vault operator is a per-install execution binding.

## The neutral contract (what every binding must satisfy)

- A **dispatch-only** credential: exactly `actions: write` on the single factory
  repository that owns the apply workflow, **no repository-contents authority**,
  a **distinct** binding from the content-write credential (never the same key).
- Delivered **by reference** (vault → the inbox's env-named secret), materialized
  as a **short-lived** token the inbox reads from a file, rotated in place.
- The token-minter (which turns any org-owned GitHub App key into a ~1h
  installation token) lives in the **binding**, never in the stdlib-only inbox.

## Case A — operator-hosted (the tenant licenses OpsxFactory)

The operator (Opensoft) owns and operates the credential, applied through the
deployment-handoff boundary (CIR → intake → approval → grant-held apply). The
operator creates the openXdox Intent Dispatch App, stores its key in the
operator's vault, and runs the minter in the tenant's cluster. This is what the
opensoft QA install does (`cir-opensoft-qa-dox-dispatch-minter`).

## Case B — self-hosted (a domain licensed WITHOUT OpsxFactory)

The tenant's own IT channel operates the credential; **no Opensoft identity
performs the privileged change**. The tenant stands up its OWN App from the
recipe below — it does not install an Opensoft-owned App on its repo.

### B1. Create the dispatch App in the tenant's org

In the tenant's GitHub org → Settings → Developer settings → GitHub Apps → New:

- **Name:** `openXdox Intent Dispatch` (tenant-scoped; any unique name is fine)
- **Repository permissions:** **Actions → Read and write**, and nothing else
  (Metadata: Read is auto-added).
- **Where can this App be installed:** Only this account (the tenant's org).
- **Install it on:** only the tenant's factory repository.
- Generate a **private key** (`.pem`) and note the **App ID**.

The App is owned by the tenant's org — its key can only ever mint
`actions:write` tokens on the tenant's own repo. There is no cross-tenant shared
App and no Opensoft-owned key on the tenant's estate.

### B2. Store the key in the tenant's vault (never in git)

Put the PEM into the tenant's approved secret provider under the `secret_ref` the
binding names (the openXdox example uses `openxdox-intent-dispatch-app`). Follow
the tenant's own secure-handoff process — the key never travels through chat,
tickets, or a repository. (See the operator-hosted key handoff for the shape of
a safe vault write: read the PEM from file, suppress the tool's echo, shred the
local copy.)

### B3. Run the minter in the tenant's estate

Deploy the same minter the operator uses (`dispatch_token_minter` +
`deploy/kubernetes/base/minter-*.yaml`), pointing its config at the tenant's
values:

- `MINTER_APP_ID` — the tenant's App ID
- `MINTER_APP_KEY_FILE` — the tenant's vault-mounted PEM
- `MINTER_DISPATCH_REPO` — the tenant's `owner/factory-repo`
- `MINTER_TARGET_SECRET` — the inbox's dispatch secret

The CronJob mints a ~1h token, downscoped at issuance to `actions:write` on the
one repo, and writes it to the inbox's secret. The inbox reads the rotating file
unchanged.

### B4. Alternative — a tenant-provided scoped credential

If the tenant's policy forbids GitHub Apps, the neutral contract still holds: the
tenant's IT channel provisions a **fine-grained token** (Actions:write on the one
repo, nothing else) through their own process and points the inbox's dispatch
secret at it. There is no minter in this variant (no App key to mint from), so
the token is long-lived — the tenant owns its rotation. This is a policy
fallback, not the default; the App path is preferred because its tokens are
short-lived and org-owned.

## What stays constant

In all cases the **serving inbox holds no write-capable key material**, the
dispatch credential is **distinct** from the content-write credential, and the
credential is **reference-delivered**. Those are the invariants the
`credential-contracts` validator enforces; this runbook is how a given install
satisfies them.
