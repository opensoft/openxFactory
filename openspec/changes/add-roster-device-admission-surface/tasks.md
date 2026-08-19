# Tasks: add-roster-device-admission-surface

ALL tasks below are the REALIZATION and run ONLY AFTER Brett ratifies this
change. Do not touch the schema, validator, examples, or bundle before
ratification. The change (proposal + design + spec delta) is authored now; the
edits below are the post-ratification implementation.

## 1. Admit `device` into the schema vocabulary

- [ ] 1.1 Add the `device` `oneOf` const member to `$defs.admission_surface`
      in `contracts/schemas/xfactory-client-identity-roster.schema.yaml`,
      mirroring the shape of the existing `business_central` and `exchange`
      members: a `const: device` with a `description` that names the admission
      act and scoping mechanism per design Ruling 3 — admin consent for the
      application read roles `Device.Read.All`,
      `DeviceManagementManagedDevices.Read.All` and `CloudPC.Read.All` on ONE
      identity (Entra registered devices + Intune managed devices + Windows 365
      Cloud PCs read); scoping mechanism is TENANT-WIDE READ with
      `exact_effective_scopes` and NO narrower provider selector; read-only.
- [ ] 1.2 Leave `contract_schema_version` at `1` (design Ruling 4: adding a
      `oneOf` const member is back-compatible — no existing roster is
      reinterpreted). Confirm the CLOSED-ON-PURPOSE header's "Growth takes a
      `contract_schema_version` bump" comment governs object-shape/key-space
      growth, not vocabulary-member admission (which the EXTENSION ROUTE text
      governs).
- [ ] 1.3 Update the `admission_surface` `description` extension-route text so
      it no longer lists Windows 365 among the surfaces still to arrive (it is
      now part of the admitted `device` read surface). Keep endpoint-MUTATION
      (Intune write) and Entra-DIRECTORY listed as SEPARATE future surfaces
      each arriving with its own governing change.

## 2. Keep the validator refusal string in sync

- [ ] 2.1 The canonical validator DERIVES the closed vocabulary from the
      schema (`Vocabularies.admission_surface = _consts(defs.get("admission_surface"))`
      in `scripts/validate-client-identity-roster.py`), so NO vocab-constant
      edit is needed — `device` becomes admissible automatically once §1 lands.
- [ ] 2.2 Update ONLY the human-facing `EXTENSION_ROUTE["admission_surface"]`
      refusal string in that validator to match the schema's revised
      extension-route text (§1.3): drop Windows 365 from the "still to arrive"
      list, keep endpoint/Intune-mutation and Entra-directory. This string is
      descriptive text a refusal cites; it is not the source of the vocabulary.

## 3. Package a `device` example and confirm the negative stays valid

- [ ] 3.1 Add a packaged positive example entry using
      `admission_surface: device` under `examples/client-identity-roster/`
      (an entry, or a small fragment, transcribed from the node-inventory
      reader evidence — read-only, tenant-wide, provider-forced breadth
      declared with its `spanned_surfaces` for the three provider areas and a
      gate obligation). List it in
      `examples/client-identity-roster/README.md`.
- [ ] 3.2 Confirm the `admission-surface-out-of-vocabulary` negative
      (`examples/client-identity-roster/negative/admission-surface-out-of-vocabulary.yaml`,
      which uses `sharepoint`) STAYS a valid negative — `sharepoint` is still
      outside the closed vocabulary, so the negative still fires. Do not change
      it.

## 4. Bundle bump contract-v1.34 → contract-v1.35 (digest refresh, additive)

- [ ] 4.1 Recompute the `client-identity-roster` schema-row `sha256` in
      `contracts/manifest.yaml` for the edited schema file; leave the row's
      `schema_version: 1` unchanged (design Ruling 4).
- [ ] 4.2 Set `contract_bundle_version: contract-v1.35` in
      `contracts/manifest.yaml`.
- [ ] 4.3 Add a `contract-v1.35` entry to `contracts/CHANGELOG.md` in the
      established style: state it is ADDITIVE under
      `docs/contract-versioning-policy.md` (new vocabulary member; a domain on
      the same major version stays conformant without changes), and record the
      `device` admission-surface admission and its node-inventory evidence.
- [ ] 4.4 Regenerate the release digests via the tooling — never hand-add:
      `python3 scripts/validate-contract-release.py build --tag contract-v1.35
      --output contracts/releases/contract-v1.35.digests.yaml` (and update the
      release README/index if the repo tracks one).

## 5. Validate green

- [ ] 5.1 Run the roster validator self-test (its packaged-corpus pass over
      `examples/client-identity-roster/` including the new positive and the
      unchanged negatives) — green.
- [ ] 5.2 `OPENSPEC_TELEMETRY=0 openspec validate --all --strict` — green.
- [ ] 5.3 Any repo-wide contract/manifest validator
      (`scripts/validate-contract-release.py verify-commit …` and the
      manifest/digest checks) — green.

## 6. Downstream (NOT part of this change)

- [ ] 6.1 The OpsxFactory side — the `device` roster entry and node-inventory
      §6, which unblock `add-managed-node-inventory` task 5.x — is a DOWNSTREAM
      CONSUMER authored in the OpsxFactory repo under its own governance. It is
      out of scope here and does not land with this change. Listed for
      traceability only.
