# Tasks: add-dispatch-credential-contract

Contract tasks (section 1) come first; artifact and realization tasks
(sections 2-3, omnigent-install + operator provisioning) are marked as such and
are NOT done by authoring this change.

## 1. Contract (openxFactory)

- [x] 1.1 ADD the two requirements to `specs/credential-contracts` (this
      change's spec delta): dispatch-only least-privilege + serving-tier
      separation, and reference-delivered credential with operator-as-binding.
      Validate `--strict` and `--all --strict` green before commit.
- [x] 1.2 Ratify the openXdox naming on approval: flip
      `docs/openxdox-naming.md` `Status: draft -> ratified` and add
      `Ratified by: add-dispatch-credential-contract`; drop the interim
      "Ratification rides ..." note.
- [x] 1.3 Register the delta at realization (contracts manifest / CHANGELOG /
      README per the registration-at-realization precedent) and add the README
      "OpenSpec Records" entry for this change.
      Done — and the manifest/CHANGELOG half is ruled NOT OWED, 2026-08-25.
      The README half is discharged: the "OpenSpec Records" row for this change
      landed with PR `#168` (merge `4e4190cb`, 2026-08-13), where it sat at
      `README.md:263`; it stands today at `README.md:877` (line numbers drift as
      the block grows — cite the row, not the offset).
      There is NO manifest or CHANGELOG registration left to perform, because
      this change moves no bytes under `contracts/`. The credential-contracts
      family's registration was closed by a DIFFERENT change and deliberately
      so: `contracts/schemas/xfactory-credential-contracts.schema.yaml` was
      promoted at DTN-004 (`promote-credential-contracts`) without a manifest
      row, and `add-client-identity-roster` closed that gap at `contract-v1.33`
      (PR #190 / `71674ed`, 2026-08-15) — see `contracts/CHANGELOG.md:1295` and
      the `credential-contracts` manifest row's "FIRST registration at
      contract-v1.33" consumption rule. Routing that registration through THIS
      lane was considered and REJECTED: the amendment record
      `openspec/changes/archive/2026-08-15-add-client-identity-roster/review/amendment-record-2026-08-14.md`
      records, on its Decision B, that "Routing it through the active
      `add-dispatch-credential-contract` lane was rejected as cross-lane
      coupling". The examples and validator this change did ship are
      content-addressed by commit (`fceaf837`) rather than per-file digest,
      the same treatment `contract-v1.33` gives its own packaged corpus, so
      they own no manifest row either.

## 2. Neutral artifacts (openxFactory)

- [x] 2.1 Add example credential records validating against
      `contracts/schemas/xfactory-credential-contracts.schema.yaml`: a
      dispatch-only requirement + binding-template (Actions:write on one repo,
      reference-delivered, operator-bound) and the distinct content-write
      binding; negatives — dispatch with contents-write, dispatch reusing the
      content identity, a baked value, an operator fixed to one domain.
      THREE of the four negatives shipped as fixtures (`fceaf837`), each named
      by the rule it violates in `scripts/validate-credential-contracts.py`:
      `examples/credential-contracts/negative/dispatch-grants-contents.yaml`
      (`dispatch-scope-ceiling`), `.../dispatch-reuses-content-secret.yaml`
      (`shared-secret-identity`), `.../baked-secret-in-binding.yaml`
      (`baked-secret`).
      The FOURTH — "an operator fixed to one domain" — is DISPOSITIONED, not
      shipped, and this paragraph corrects the record rather than the tick.
      It cannot be written as a fixture because the record shape cannot express
      the violation. A binding names its operator in `owner` — that is the
      CONFORMANT case, and the shipped binding-template does exactly that
      (`owner: opensoft-platform` on both bindings). "Fixed to one domain" is a
      claim of EXCLUSIVITY, and no field in
      `contracts/schemas/xfactory-credential-contracts.schema.yaml` carries it
      (the binding requires exactly `provider, secret_ref, owner,
      rotation_policy`); inventing one so a negative could assert it would be a
      schema change, which would move bytes under `contracts/` and owe the very
      bundle this change is ruled not to owe.
      The requirement's own scenario text agrees. The two dispatch scenarios say
      "the validator MUST report an error" and duly got fixtures; the
      operator-fixing scenario says only "it MUST be rejected", naming no
      enforcer, and its sibling in the same requirement assigns rejection to
      "repository policy" rather than to the validator. So the invariant is
      enforced by repository policy and by Case B of
      `docs/openxdox-dispatch-credential-binding.md` — the self-hosted path in
      which the tenant's own IT channel operates the credential and no Opensoft
      identity performs the privileged change, plus the B4 tenant-provided
      scoped-credential fallback — and never by a validator fixture.
- [x] 2.2 Validator support where mechanizable (dispatch-scope ceiling and the
      distinct-binding / no-shared-identity check) in the credential-contracts
      family validator, each negative example naming its violated rule.

## 3. Operator-binding realization (omnigent-install + org provisioning) — downstream

- [x] 3.1 Create the org-owned **openXdox Intent Dispatch** GitHub App
      (`Actions: write` only; install on `opensoft/xFactory`). Org-admin action,
      not code.
      Done: App ID `4582547`, installation `153530982` on `opensoft/xFactory`,
      permissions exactly `{actions: write, metadata: read}`. Read back from the
      readiness result's `minted-token-is-dispatch-only` check (App ID and
      permission set, with repository-contents observed 403) and its
      `minter-cronjob-present-and-mint-succeeded` check, whose mint log printed
      "minted installation token for opensoft/xFactory (installation
      153530982)". The App is also named at seq 0 of the CIR transition ledger.
- [x] 3.2 Token-minter delivering short-lived installation tokens by reference
      into the inbox's env-named dispatch secret (inbox stays stdlib-only,
      unchanged). Resolve the minter topology (CronJob / scheduled-Action /
      sidecar) here.
      Done, and the topology is RESOLVED as an in-cluster **CronJob** (not a
      scheduled Action, not a sidecar): `dox-token-minter`, shipped as
      `dispatch_token_minter` + `deploy/kubernetes/base/minter-*.yaml` in
      omnigent-install, pinned at `66ca33fd5a9556fe8edb022fbd7b18c4e80dab2d`
      (PR #97) — the release the CIR ledger re-pins to at seq 5 and applies at
      seq 6/7. It mints a ~1h installation token downscoped at issuance and
      writes it to the inbox's dispatch secret; the inbox reads the rotating
      token file unchanged and holds no key material, proven by the readiness
      result's `inbox-holds-no-app-key` check (only `/dispatch/token` is
      mounted; no PEM anywhere in the pod).
- [x] 3.3 Repoint the QA openXdox dispatch secret from the personal PAT to the
      minted App token; retire `dox-intent-inbox-qa-20260810`.
      Done: the readiness result's `dispatch-secret-holds-a-minted-token` check
      records `dox-intent-inbox-dispatch.token` at length 520, written by the
      minter, with the personal PAT no longer its source (length only, never the
      value), and the dox SecretProviderClass stopped syncing the PAT at CIR
      seq 7.
      The PAT DELETION RESTS ON BRETT'S RECORD, exactly as the readiness result
      itself states it: `personal-pat-retired` records that
      `dox-intent-inbox-qa-20260810` "was deleted by Brett via GitHub settings
      on 2026-08-15 (retired out-of-band: the CLI credential 404s on the PAT
      admin endpoint)". There is no API read-back for this one fact — a
      fine-grained PAT under an individual account is not enumerable by the
      automation, which is why the credential was fragile and why this change
      retired it. Recorded as an operator attestation, not as a machine probe.
- [x] 3.4 Self-hosted binding runbook: the domain repo's install docs pin the
      neutral contract and the tenant-installs-the-App / tenant-IT-provides-a-
      scoped-credential path (reachable by a domain licensed without the
      operator).
      Done 2026-08-14: docs/openxdox-dispatch-credential-binding.md — the
      operator-neutral binding runbook (Case A operator-hosted, Case B
      self-hosted App-in-tenant-org + the IT-provided-credential fallback),
      linked in the README doc index.
      RATIFIED IN THIS SLICE, 2026-08-25, per Brett's ruling: the runbook goes
      `Status: draft -> ratified` with `Ratified by:
      add-dispatch-credential-contract`. The primary spelling applies because an
      approving change exists to name — this one, the change the runbook
      realizes. It rides the same lifecycle act as `docs/openxdox-naming.md`
      (task 1.2), and lands in-window rather than owing a follow-up.

## 4. Records

- [x] 4.1 End-to-end: the inbox dispatches using a token minted from the App
      (not a personal PAT); token metadata proves `actions:write`-only on the
      one repo (openXdox readiness check 3); the content App remains a separate
      binding.
      Done, on a fresh passing readiness result and a completed CIR.
      **Readiness** — repo `installs/hermes-install` (in the aggregation
      checkout), path
      `config/clients/opensoft/readiness/dox-dispatch-minter-ready.result.yaml`,
      `result_id: ready-opensoft-dox-qa-dispatch-minter-20260815t013000z`,
      profile `dox-dispatch-minter-ready` v1, `status: ready`, observed
      2026-08-15T01:30:00Z, all SIX mandatory checks `pass` and
      `failed_checks: []`, over a non-privileged read-only walk that changed no
      governed state.
      **Dispatch** — check `inbox-dispatches-on-the-minted-token`: an authorized
      `brett` intent submitted through the ingress fired `intent-apply` run
      `31856312594` on `opensoft/xFactory` at 2026-08-15T01:22:04Z, outcome
      completed/success.
      **Scope** — check `minted-token-is-dispatch-only`: the minted installation
      token carries exactly `actions:write` on `opensoft/xFactory` and nothing
      else, with repository-contents observed 403; the content-write binding
      (`XFACTORY_APP`, `Contents: write`) stays a separate identity, as the
      shipped binding-template's two distinct `secret_ref`s declare.
      **Closeout** — the CIR transition ledger
      `config/clients/opensoft/requests/cir-opensoft-qa-dox-dispatch-minter.transitions.yaml`
      reaches `completed` at **seq 9**, 2026-08-15T01:35:00Z, actor
      `opensoft-hermes-qa-readiness-validator` in the `trusted_validator` role,
      citing that same result id (correlation
      `opensoft-dox-qa-dispatch-minter-001`).
- [x] 4.2 Keep the README "OpenSpec Records" entry current through
      ratification, realization, and archive.
      Done. The row no longer speaks in plan voice: its "realizes the dispatch
      binding ... retiring the personal PAT" promise is rewritten to the landed
      evidence — App `4582547`/installation `153530982`, the minter CronJob at
      omnigent-install `66ca33fd`, run `31856312594` green, readiness `ready`
      6/6 and the CIR completed, PAT `dox-intent-inbox-qa-20260810` deleted —
      and the row moves from Active to Archived changes in the same act.
