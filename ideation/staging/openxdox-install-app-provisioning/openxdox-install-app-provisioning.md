# Staged: openXdox install App provisioning — manifest-flow two-App bootstrap per tenant

Status: staged
Kind: architecture
Summary: How a DomainxFactory install (first case: a client running codexFactory)
provisions the intent plane's GitHub credentials with near-zero manual config,
tenant-owned and sovereign. The two Apps the intent plane needs — openxFactory
(content-write) and openXdox (dispatch) — are created in the TENANT's org via the
GitHub App Manifest flow (GitHub has no app-creates-app API), the apply workflow
lives in a small dedicated repo the install creates, and the tenant's only real
decision is which of their repos the content App may write.
Topics: install-provisioning, github-app-manifest, openxdox, dispatch-credential, content-app, tenant-sovereignty, codexfactory-install, two-app-separation, apply-workflow-repo, naming-convention
Repository context: openxFactory owns the neutral contract (a delta to `credential-contracts`, or a new `install-app-provisioning` capability — the two-App manifest-provisioning shape, the apply-workflow-repo home, the naming convention); the installer realization lands in `Omnigent-Install` (the domain install flow that drives the manifest flow + wires credentials); domain repos (codexFactory) ship the manifest files + the install-doc pointer; OpsxFactory operates the managed (`opsxfactory_executed`) case
Staging ID: openxFactory:staging:openxdox-install-app-provisioning
Source: named by Brett Heap 2026-08-14 during the openXdox dispatch-migration work, when the QA install's manual App setup (create the App, set permissions, add the repo, accept the permission update) surfaced "can we have the user install one app and use that to install the others" — resolved to the GitHub App Manifest flow; extends the self-hosted binding runbook (`docs/openxdox-dispatch-credential-binding.md`) from `add-dispatch-credential-contract`
Target capabilities: credential-contracts (MODIFIED — or a new `install-app-provisioning` capability); realization in Omnigent-Install (installer) + codexFactory (manifest files + install docs)

The intent plane needs **two** GitHub Apps per install, kept separate by
`add-dispatch-credential-contract`: the **content** App (`Contents: write` on the
governed doc repos, held in CI) and the **dispatch** App (`Actions: write` on the
one apply-workflow repo, held as short-lived minted tokens by the exposed inbox).
opensoft's QA install created both by hand, and hit every manual step — set
permissions, add the repo, accept the permission update — twice. Every tenant
running a DomainxFactory would repeat that toil unless the install provisions the
Apps for them — and it must do so without an opensoft identity ever holding a key
on the tenant's repos (the self-hosted sovereignty rule from the binding runbook).

## Claims

1. **Two Apps stay two — the separation is the security invariant, not toil to
   optimize away.** The exposed inbox must never hold a contents-write-capable
   key; content-write lives in CI. An install may not collapse them into one App.
2. **GitHub has no app-creates-app API; the App Manifest flow is the mechanism.**
   You cannot have one installed App create the others. But a shipped **manifest**
   (name, permissions, events, webhook pre-filled) lets the installer redirect the
   tenant to GitHub, where they name-and-confirm; GitHub creates the App in their
   org and returns a temp code the installer exchanges for the app-id + private
   key + secrets (within one hour). Near-one-click per App, no manual scope config.
3. **The Apps are tenant-owned.** The manifest-created App belongs to the tenant's
   org — which is exactly what sovereignty requires. An opensoft installer-App
   creating Apps (even if GitHub allowed it) would put an opensoft identity in the
   tenant's credential path; the manifest flow structurally avoids that.
4. **App names are globally unique → a naming convention, not identical names.** A
   GitHub App's name is its global slug (`github.com/apps/<slug>`), unique across
   all of GitHub. Every tenant cannot literally name an App `openXdox`; the
   convention is `openXdox — <tenant>` / `openxFactory — <tenant>` (manifest
   pre-fills a default). Support discovers a tenant's Apps by the `openXdox *` /
   `openxFactory *` pattern.
5. **The apply workflow lives in a small dedicated repo, created per install.** A
   tiny `openxdox-apply`-shaped repo holding the pinned `intent-apply.yml`, rather
   than parking the workflow in a large aggregation repo. The dispatch App then
   scopes to that one small repo (Actions:write on `openxdox-apply`, nothing else)
   — cleaner, more supportable, and it keeps the dispatch blast radius minimal.
6. **The tenant's only real config is the content App's repo scope.** With the
   manifest pre-filling permissions and the apply repo installer-created, the
   tenant's one decision is which of their repos hold the governed docs — the
   content App's selected-repositories list. Everything else is installer-driven.

## Open questions

1. **Contract home:** a MODIFIED delta to `credential-contracts` (the manifest
   provisioning shape as an extension of the dispatch/content binding contract),
   or a new `install-app-provisioning` capability that references it?
2. **Managed vs self-hosted flow:** in the `opsxfactory_executed` case does the
   operator drive the manifest flow on the tenant's behalf, or does the tenant
   always click through their own (keeping the App tenant-owned either way)?
3. **Apply-workflow-repo home:** created fresh per install, or a template repo the
   tenant forks? And does opensoft's own workflow stay in `xFactory` or migrate to
   the small-repo pattern for parity with tenant installs?
4. **Credential capture + hand-off:** the installer captures app-id + PEM from the
   manifest callback — where does it place them (the tenant's vault) and how does
   that hand to the minter without the installer becoming a credential custodian?
5. **Naming-convention grain:** `openXdox — <tenant-display>` vs
   `openxdox-<tenant-slug>`; how does opensoft support enumerate them across
   tenant orgs it may not directly see?

## Exit path

Proposal once the contract home (Q1) and the managed-vs-self-hosted flow (Q2) are
decided with Brett. Likely a MODIFIED `credential-contracts` delta (the two-App
manifest-provisioning shape + naming convention + apply-repo home) plus a named
`Omnigent-Install` realization change (the installer that drives the manifest flow
and wires credentials). Gated on the opensoft QA dispatch migration completing —
its readiness proves the two-App runtime shape the installer would provision.
