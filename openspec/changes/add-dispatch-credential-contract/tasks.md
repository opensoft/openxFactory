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
- [ ] 1.3 Register the delta at realization (contracts manifest / CHANGELOG /
      README per the registration-at-realization precedent) and add the README
      "OpenSpec Records" entry for this change.

## 2. Neutral artifacts (openxFactory)

- [x] 2.1 Add example credential records validating against
      `contracts/schemas/xfactory-credential-contracts.schema.yaml`: a
      dispatch-only requirement + binding-template (Actions:write on one repo,
      reference-delivered, operator-bound) and the distinct content-write
      binding; negatives — dispatch with contents-write, dispatch reusing the
      content identity, a baked value, an operator fixed to one domain.
- [x] 2.2 Validator support where mechanizable (dispatch-scope ceiling and the
      distinct-binding / no-shared-identity check) in the credential-contracts
      family validator, each negative example naming its violated rule.

## 3. Operator-binding realization (omnigent-install + org provisioning) — downstream

- [ ] 3.1 Create the org-owned **openXdox Intent Dispatch** GitHub App
      (`Actions: write` only; install on `opensoft/xFactory`). Org-admin action,
      not code.
- [ ] 3.2 Token-minter delivering short-lived installation tokens by reference
      into the inbox's env-named dispatch secret (inbox stays stdlib-only,
      unchanged). Resolve the minter topology (CronJob / scheduled-Action /
      sidecar) here.
- [ ] 3.3 Repoint the QA openXdox dispatch secret from the personal PAT to the
      minted App token; retire `dox-intent-inbox-qa-20260810`.
- [x] 3.4 Self-hosted binding runbook: the domain repo's install docs pin the
      neutral contract and the tenant-installs-the-App / tenant-IT-provides-a-
      scoped-credential path (reachable by a domain licensed without the
      operator).
      Done 2026-08-14: docs/openxdox-dispatch-credential-binding.md — the
      operator-neutral binding runbook (Case A operator-hosted, Case B
      self-hosted App-in-tenant-org + the IT-provided-credential fallback),
      linked in the README doc index.

## 4. Records

- [ ] 4.1 End-to-end: the inbox dispatches using a token minted from the App
      (not a personal PAT); token metadata proves `actions:write`-only on the
      one repo (openXdox readiness check 3); the content App remains a separate
      binding.
- [ ] 4.2 Keep the README "OpenSpec Records" entry current through
      ratification, realization, and archive.
