# Tasks: add-roster-directory-admission-surface

Sections §1–§5 are the REALIZATION and run ONLY AFTER Brett ratifies this
change; NOTHING touches the schema, validator, examples, or bundle before
ratification, and every box below is unchecked for that reason. §6 is a
downstream boundary owned by another repository and is listed for traceability
only.

## 1. Admit `directory` into the schema vocabulary

- [ ] 1.1 Add the `directory` `oneOf` const member to `$defs.admission_surface`
      in `contracts/schemas/xfactory-client-identity-roster.schema.yaml`,
      mirroring the shape of the existing `business_central`, `exchange` and
      `device` members: a `const: directory` with a `description` that names the
      admission act and scoping mechanism per design Ruling 4 — ADMIN CONSENT
      for the read-only directory and service-enumeration application roles on
      ONE Entra app registration (the realized reader class holds
      `Organization.Read.All`, `Application.Read.All` and `Domain.Read.All`:
      organization profile and subscribed service plans, service
      principals/applications, verified domains); scoping mechanism is
      TENANT-WIDE READ with `exact_effective_scopes` and NO narrower provider
      selector (unlike Exchange's per-group `RestrictAccess`, and exactly like
      `device`); read-only — no granted role confers creation, modification or
      deletion.
- [ ] 1.2 Leave `contract_schema_version` at `1` (design Ruling 5: adding a
      `oneOf` const member is back-compatible — no existing roster is
      reinterpreted). Confirm the CLOSED-ON-PURPOSE header's "Growth takes a
      `contract_schema_version` bump" comment governs object-shape/key-space
      growth, not vocabulary-member admission (which the EXTENSION ROUTE text
      governs).
- [ ] 1.3 Update the `admission_surface` `description` extension-route text:
      the closed vocabulary now reads "`business_central`, `exchange`,
      `device` and `directory`", and the "still to arrive" list drops
      Entra-directory READ (discharged here) while KEEPING endpoint MUTATION
      (Intune write) AND Entra-directory MUTATION (user/group/application
      administration) as SEPARATE future surfaces, each arriving with its own
      governing change (design Ruling 3). Do not drop the mutation half while
      editing the read half.

## 2. Keep the validator refusal string in sync

- [ ] 2.1 The canonical validator DERIVES the closed vocabulary from the schema
      (`self.admission_surface = _consts(defs.get("admission_surface"))` in
      `scripts/validate-client-identity-roster.py`), so NO vocab-constant edit
      is needed — `directory` becomes admissible automatically once §1 lands.
      Confirm this by reading the code, not by assuming it: the `device`
      admission relied on the same derivation and it is the reason this section
      is one line of text and not a vocabulary edit.
- [ ] 2.2 Update ONLY the human-facing `EXTENSION_ROUTE["admission_surface"]`
      refusal string in that validator to match the schema's revised
      extension-route text (§1.3): the "still to arrive" list becomes endpoint
      MUTATION / Intune write and Entra-directory MUTATION. This string is
      descriptive text a refusal cites; it is not the source of the vocabulary.
- [ ] 2.3 Confirm no other validator rule keys on the vocabulary's SIZE or on a
      hardcoded surface tuple (search the script for each existing surface
      const). A rule that enumerated surfaces by hand would silently exclude
      `directory`; the same class of defect was found and fixed on the
      OpsxFactory side as that change's adversarial finding F3.

## 3. Package a `directory` example and confirm the negative stays valid

- [ ] 3.1 Add a packaged positive example entry using
      `admission_surface: directory` under `examples/client-identity-roster/`
      (an entry in the existing OpsxFactory fragment, transcribed from the
      merged `microsoft_service_discovery_reader` evidence — OpsxFactory `main`
      `824f8ef`, `credentials/requirements.yaml` — and cited inline by
      repository, path and commit, per that directory's TRUTHFUL WORKED CASES
      rule). The example MUST use the governed-tenant-scope shape (design
      Ruling 2) so the roster validator self-test passes on it:
      - `exceeds_governed_unit: false` — the governed unit IS the tenant
        directory and service estate, so tenant-wide read is the governed
        scope, not excess;
      - NO `declared_excess` block, and `spanned_surfaces` empty/omitted — the
        provider areas read (organization profile, subscribed service plans,
        applications, domains) are NOT `admission_surface` consts, so they
        CANNOT appear in a structured breadth field (the schema would refuse
        them); they live only in the `directory` member's `description` prose;
      - `per_unit_principal_available: {directory: false}` — no per-unit
        principal; the governed unit is the whole tenant directory/service
        estate;
      - the single admission act `enforcement_mode: logic_enforced` — there is
        no provider scoping selector; the read is bounded by the exact
        read-only roles;
      - `blast_radius_unit` = the tenant directory and service estate (a clear
        free token such as `tenant_directory_estate`, bound in the fragment's
        `legend` — `blast_radius_unit` is a domain-declared token and a token
        with no legend entry is a finding);
      - `identity_kind: entra_app_registration`, `authority_class_intended` and
        `_achieved` both `observe`, `granted_permissions[]` each
        `achieves: observe` and `reaches: [directory]`;
      - `residency_model: client_tenant_single`, read-only, presented by
        reference through the `tenant-reader-grant-pipeline`.
      Decide and record whether the entry is `planned` (the discovery reader is
      a DOWNSTREAM OpsxFactory consumer not yet admitted, so the act is
      UNVERIFIED — no `evidence_ref`, no `verified_at`, `provider_object_ref`
      omitted) exactly as the `device` example did. Do NOT invent a
      verification timestamp or a provider object id. List the example in
      `examples/client-identity-roster/README.md`.
- [ ] 3.2 Confirm the `admission-surface-out-of-vocabulary` negative
      (`examples/client-identity-roster/negative/admission-surface-out-of-vocabulary.yaml`,
      which uses `sharepoint`) STAYS a valid negative — `sharepoint` is still
      outside the closed vocabulary, so the negative still fires. Do not change
      it. Note that `sharepoint` is one of the services DISCOVER may DETECT;
      detection is not admission, and the negative must keep firing.

## 4. Bundle bump contract-v1.38 → contract-v1.39 (digest refresh, additive)

- [ ] 4.1 RE-READ `contracts/manifest.yaml` for the CURRENT
      `contract_bundle_version` before assuming the target. It reads
      `contract-v1.38` at authoring time (2026-08-22), so the target is
      contract-v1.39 — but bundles are cut frequently by other changes, and a
      cut landing between ratification and realization moves the target by one.
- [ ] 4.2 Recompute the `client-identity-roster` schema-row `sha256` in
      `contracts/manifest.yaml` for the edited schema file; leave the row's
      `schema_version: 1` unchanged (design Ruling 5).
- [ ] 4.3 Set `contract_bundle_version` to the target version in
      `contracts/manifest.yaml`.
- [ ] 4.4 Add the corresponding entry to `contracts/CHANGELOG.md` in the
      established style: state it is ADDITIVE under
      `docs/contract-versioning-policy.md` (new vocabulary member; a domain on
      the same major version stays conformant without changes), and record the
      `directory` admission-surface admission with its governing evidence
      (OpsxFactory `add-managed-service-inventory` §1–§6, `main` `824f8ef`) and
      the read/mutate boundary the member preserves.
- [ ] 4.5 Regenerate the release digests via the tooling — never hand-add:
      `python3 scripts/validate-contract-release.py build --tag <target>
      --output contracts/releases/<target>.digests.yaml` (and update the
      release README/index if the repo tracks one). Confirm the new inventory
      actually contains the roster schema row — the `contract-v1.37` cut was
      found to have OMITTED two new families, which is why this is a check and
      not a build step.

## 5. Validate green

- [ ] 5.1 Run the roster validator self-test (its packaged-corpus pass over
      `examples/client-identity-roster/` including the new positive and the
      unchanged negatives) — green. Run it from a CLEAN path: `sweep_files`
      skips any path containing a `.git` segment, so a run from a linked
      worktree under `.git/modules/` silently measures less than it appears to.
- [ ] 5.2 `OPENSPEC_TELEMETRY=0 openspec validate
      add-roster-directory-admission-surface --strict` and
      `OPENSPEC_TELEMETRY=0 openspec validate --all --strict` — both green,
      exit codes read directly and never through a pipe.
- [ ] 5.3 Any repo-wide contract/manifest validator
      (`python3 scripts/validate-contract-release.py verify-commit --commit
      <realization commit>` and the manifest/digest checks) — green.
- [ ] 5.4 Re-verify the PROMOTED delta after archiving: the capability's
      requirement count is unchanged (a MODIFIED delta replaces), the three
      pre-existing scenarios of "Identities are enumerated by admission
      surface, not by product name" survive verbatim, and the promoted body
      diffs clean against this change's delta file apart from the delta's own
      scaffolding.

## 6. Downstream (NOT part of this change)

- [ ] 6.1 The OpsxFactory side — the FarHeap `directory` roster entry
      (`add-managed-service-inventory` task 7.2) and everything its §7 gates
      behind that entry: the consent ceremony (7.3), the grant mint (7.4), the
      authorized live sweep (7.5), snapshot acceptance and revocation proof
      (7.6), and the MAP hand-off (7.7) — is a DOWNSTREAM CONSUMER authored in
      the OpsxFactory repo under its own governance. It is out of scope here,
      does not land with this change, and is authorized by nothing here. This
      box stays unticked deliberately: an unticked box here means "owned
      elsewhere", and ticking it would claim work this repository never did.
