# Tasks: add-roster-directory-admission-surface

Sections §1–§5 are the REALIZATION and run ONLY AFTER Brett ratifies this
change; NOTHING touches the schema, validator, examples, or bundle before
ratification, and every box below is unchecked for that reason. §6 is a
downstream boundary owned by another repository and is listed for traceability
only.

## 1. Admit `directory` into the schema vocabulary

- [x] 1.1 Add the `directory` `oneOf` const member to `$defs.admission_surface`
      in `contracts/schemas/xfactory-client-identity-roster.schema.yaml`,
      mirroring the shape of the existing `business_central`, `exchange` and
      `device` members: a `const: directory` with a `description` that names the
      admission act and scoping mechanism per design Ruling 4.
      HARD-ENUMERATE the admission act, in the `device` member's own
      enumeration style and matching the spec delta's added scenario word for
      word — ADMIN CONSENT for the read-only application roles
      `Organization.Read.All`, `Application.Read.All` and `Domain.Read.All` on
      ONE Entra app registration (the organization profile and its subscribed
      service plans, the tenant's service principals/applications, and its
      verified domains). Do NOT write a role FAMILY: the exact effective set is
      pinned at CLASS REALIZATION, and that realization is already MERGED
      (OpsxFactory `main` `824f8ef`, `microsoft_service_discovery_reader`
      `minimum_scopes` = exactly those three roles, with
      `exact_effective_scopes: true`), so there is no open pin left for loose
      prose to accommodate. Scoping mechanism is TENANT-WIDE READ with
      `exact_effective_scopes` and NO narrower provider selector (unlike
      Exchange's per-group `RestrictAccess`, and exactly like `device`);
      read-only — no granted role confers creation, modification or deletion.
      Then add ONE EXCLUSION CLAUSE: a broader directory-wide read role such as
      `Directory.Read.All` is NOT within this surface's admission act, because
      it also reads the ALREADY-ADMITTED `device` surface (Entra registered
      devices) and so would collapse two separately-consented, separately-scoped
      and separately-revocable surfaces onto one act — the very collapse the
      governing change rejected in its Decision 2 and design Ruling 2 rejects
      here. That clause MUST live in the member `description`, because the
      member description is the ONLY place the neutral layer can state it: the
      schema header rules that "THE NEUTRAL LAYER NEVER INFERS A PROVIDER FACT",
      so no validator can ever derive this boundary from the role tokens
      themselves.
- [x] 1.2 Leave `contract_schema_version` at `1` (design Ruling 5: adding a
      `oneOf` const member is back-compatible — no existing roster is
      reinterpreted). Confirm the CLOSED-ON-PURPOSE header's "Growth takes a
      `contract_schema_version` bump" comment governs object-shape/key-space
      growth, not vocabulary-member admission (which the EXTENSION ROUTE text
      governs).
- [x] 1.3 Update the `admission_surface` `description` extension-route text:
      the closed vocabulary now reads "`business_central`, `exchange`,
      `device` and `directory`", and the "still to arrive" list drops
      Entra-directory READ (discharged here) while KEEPING endpoint MUTATION
      (Intune write) AND Entra-directory MUTATION (user/group/application
      administration) as SEPARATE future surfaces, each arriving with its own
      governing change (design Ruling 3). Do not drop the mutation half while
      editing the read half.
      In the SAME edit, correct the GROUNDING of both the member set and the
      route from PROMOTED to RATIFIED. The text today grounds the vocabulary on
      promotion — "the client-tenant Entra-homed surfaces whose capabilities are
      PROMOTED", and "a surface enters with the promotion of the capability that
      governs it" — and that grounding has been FALSE since contract-v1.35:
      neither `managed-node-inventory` nor `managed-service-inventory` is
      promoted. Both are RATIFIED and still ACTIVE — unarchived, sitting in
      OpsxFactory `openspec/changes/` — so on the schema's literal wording
      `device` should never have been admitted either. Reword to the test the
      capability actually states and actually MEETS: the surfaces "whose
      governing change is RATIFIED", and "a surface enters with the ratified
      change that governs it". This is a SCHEMA-PROSE correction only: the
      promoted requirement's own normative sentence — "The closed surface
      vocabulary SHALL be extended only by the change that governs a new
      surface" — is already change-based, is satisfied here, and MUST NOT be
      touched; no spec delta in this change covers it.
      PRESERVE VERBATIM through the whole re-slice the route's non-Entra
      SUCCESSOR clause: "non-Entra providers, including a client-org GitHub App
      installation, are a NAMED SUCCESSOR routed by
      `client-infrastructure-liaison`". It is a separate named route with its
      own owner, wholly unaffected by this admission, and rewriting the prose
      around it is exactly how such a clause gets dropped by accident.
- [x] 1.4 Amend the SECOND site in the schema that carries the Entra-directory
      futures claim: the `device` member's OWN `description`, which today closes
      "Endpoint MUTATION (Intune write) and Entra DIRECTORY read remain SEPARATE
      future surfaces, each arriving with its own governing change." §1.3 covers
      only the vocabulary-level extension-route prose; THIS is a second,
      independent statement of the same claim, inside a sibling member. Amend it
      to: "Endpoint MUTATION (Intune write) and Entra-directory MUTATION remain
      SEPARATE future surfaces; Entra-directory READ is admitted as `directory`
      (contract-v1.39)." Without this edit the ratified contract file
      CONTRADICTS ITSELF — the `device` member announcing Entra directory read
      as a future surface while the vocabulary immediately above it already
      admits exactly that. Cite the bundle version §4.1 actually resolves, not
      `contract-v1.39` on faith.

## 2. Keep the validator refusal string in sync

- [x] 2.1 The canonical validator DERIVES the closed vocabulary from the schema
      (`self.admission_surface = _consts(defs.get("admission_surface"))` in
      `scripts/validate-client-identity-roster.py`), so NO vocab-constant edit
      is needed — `directory` becomes admissible automatically once §1 lands.
      Confirm this by reading the code, not by assuming it: the `device`
      admission relied on the same derivation and it is the reason this section
      is one line of text and not a vocabulary edit.
- [x] 2.2 Update ONLY the human-facing `EXTENSION_ROUTE["admission_surface"]`
      refusal string in that validator to match the schema's revised
      extension-route text (§1.3): the "still to arrive" list becomes endpoint
      MUTATION / Intune write and Entra-directory MUTATION. This string is
      descriptive text a refusal cites; it is not the source of the vocabulary.
- [x] 2.3 Confirm no other validator rule keys on the vocabulary's SIZE or on a
      hardcoded surface tuple (search the script for each existing surface
      const). A rule that enumerated surfaces by hand would silently exclude
      `directory`; the same class of defect was found and fixed on the
      OpsxFactory side as that change's adversarial finding F3.

## 3. Package a `directory` example and confirm the negative stays valid

- [x] 3.1 Add a packaged positive example entry using
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
- [x] 3.2 Confirm the `admission-surface-out-of-vocabulary` negative
      (`examples/client-identity-roster/negative/admission-surface-out-of-vocabulary.yaml`,
      which uses `sharepoint`) STAYS a valid negative — `sharepoint` is still
      outside the closed vocabulary, so the negative still fires. Do not change
      it. Note that `sharepoint` is one of the services DISCOVER may DETECT;
      detection is not admission, and the negative must keep firing.

## 4. Bundle bump contract-v1.38 → contract-v1.39 (digest refresh, additive)

- [x] 4.1 RE-READ `contracts/manifest.yaml` for the CURRENT
      `contract_bundle_version` before assuming the target. It reads
      `contract-v1.38` at authoring time (2026-08-22), so the target is
      contract-v1.39 — but bundles are cut frequently by other changes, and a
      cut landing between ratification and realization moves the target by one.
- [x] 4.2 Recompute the `client-identity-roster` schema-row `sha256` in
      `contracts/manifest.yaml` for the edited schema file; leave the row's
      `schema_version: 1` unchanged (design Ruling 5).
- [x] 4.3 Set `contract_bundle_version` to the target version in
      `contracts/manifest.yaml`.
- [x] 4.4 Add the corresponding entry to `contracts/CHANGELOG.md` in the
      established style: state it is ADDITIVE under
      `docs/contract-versioning-policy.md` (new vocabulary member; a domain on
      the same major version stays conformant without changes), and record the
      `directory` admission-surface admission with its governing evidence
      (OpsxFactory `add-managed-service-inventory` §1–§6, `main` `824f8ef`) and
      the read/mutate boundary the member preserves.
- [x] 4.5 Regenerate the release digests via the tooling — never hand-add:
      `python3 scripts/validate-contract-release.py build --tag <target>
      --output contracts/releases/<target>.digests.yaml` (and update the
      release README/index if the repo tracks one). Confirm the new inventory
      actually contains the roster schema row — the `contract-v1.37` cut was
      found to have OMITTED two new families, which is why this is a check and
      not a build step.

## 5. Validate green

- [x] 5.1 Run the roster validator self-test (its packaged-corpus pass over
      `examples/client-identity-roster/` including the new positive and the
      unchanged negatives) — green. Run it from a CLEAN path: `sweep_files`
      skips any path containing a `.git` segment, so a run from a linked
      worktree under `.git/modules/` silently measures less than it appears to.
- [x] 5.2 `OPENSPEC_TELEMETRY=0 openspec validate
      add-roster-directory-admission-surface --strict` and
      `OPENSPEC_TELEMETRY=0 openspec validate --all --strict` — both green,
      exit codes read directly and never through a pipe.
- [x] 5.3 Any repo-wide contract/manifest validator
      (`python3 scripts/validate-contract-release.py verify-commit --commit
      <realization commit>` and the manifest/digest checks) — green.
- [ ] 5.4 Re-verify the PROMOTED delta after archiving: the capability's
      requirement count is unchanged (a MODIFIED delta replaces), the three
      pre-existing scenarios of "Identities are enumerated by admission
      surface, not by product name" survive verbatim, and the promoted body
      diffs clean against this change's delta file apart from the delta's own
      scaffolding.
      STAYS UNTICKED ON PURPOSE — the act it names happens AT ARCHIVE, and this
      realization touches neither the delta nor the promoted spec. Its SUBSTANCE
      is nonetheless measured here so the archiver inherits a reading rather
      than a hope: the promoted requirement body (heading + prose + all three
      existing scenarios, 1882 bytes) is a VERBATIM PREFIX of the delta's 2584
      bytes, the only tail being the one added scenario "The directory
      (service-inventory) surface is admitted"; the promoted capability holds 13
      requirements and the delta names 1, so a MODIFIED replace leaves the count
      at 13.

## 5R. Realization record (what §1–§5 resolved, recorded where §3.1/§4.1/§4.5 ask)

Realization commit `5124fbcd` on `change/add-roster-directory-admission-surface`.

- **§4.1 resolved contract-v1.38 → contract-v1.39.** `contracts/manifest.yaml:3`
  read `contract-v1.38` at realization, on this branch and on `origin/main`. One
  caveat worth the ink: an UNLANDED branch,
  `origin/change/doxbench-turn-posture-release` (`97aa19a7`), has also cut a
  `contract-v1.39` in its own working state. It is not on `main`, and
  `contracts/CHANGELOG.md`'s own recorded allocation rule — the version is
  allocated AT REALIZATION against what is AVAILABLE, with CHANGELOG presence as
  the availability test (the v1.38 heading states it) — makes v1.39 unallocated
  when this ran. Whichever of the two lands SECOND re-cuts against the CHANGELOG
  it then finds. Recorded so the collision is not discovered at merge.
- **§3.1 decided `planned`.** No `evidence_ref`, no `verified_at`, no
  `provider_object_ref` — the discovery reader is a downstream OpsxFactory
  consumer not yet admitted, so the act is UNVERIFIED by derivation exactly as
  the `device` entry's was. `standing_credential_attestation.attested_at` is the
  commit timestamp of the merge that landed the reader class
  (`2026-08-22T11:11:27Z`, OpsxFactory `main` `824f8ef`) rather than an invented
  moment.
- **§4.5's inventory check answered, in the negative, by design.** The roster
  schema is NOT a release-inventory member: membership is the
  `contracts/hermes-runtime/contract-index.yaml` catalog's `release_member`
  entries plus the Decision-10 auxiliaries, and `contracts/schemas/
  xfactory-client-identity-roster.schema.yaml` is in neither. So
  `contract-v1.39.digests.yaml` holds 190 entries, the same count as v1.38, and
  differs from it in exactly TWO rows — `contracts/CHANGELOG.md` and
  `contracts/manifest.yaml`, both auxiliaries this cut edits. This is the same
  answer `contract-v1.35` recorded for `device`, and it is the answer the check
  was there to obtain; it is not the `contract-v1.37` omission class, which was
  about catalog families genuinely missing from their own inventory.
- **§2.2 mirrored the WHOLE revised route sentence, not only its futures list.**
  The task names the futures half; matching only that half would have left the
  validator saying "the promotion of the capability" while the schema says "the
  ratified change" — two declarations of one route, disagreeing, which is the
  defect F3 exists to remove. The string now tracks §1.3 verbatim.

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
- [ ] 6.2 RECORD, so no one mistakes landing this change for unblocking that
      one: this change alone does NOT make task 7.2 runnable. OpsxFactory pins
      contract-v1.35 (`stack.yaml` `contract_ref`
      `78f8e016fbddcf1125c11b7f11234fb2478b0415`) and carries its OWN local
      copy of the vocabulary —
      `ROSTER_ADMITTED_SURFACE_VOCAB = frozenset({"business_central",
      "exchange", "device"})` at `scripts/validate-domain-factory.py:1501`,
      enforced at :1670 with a refusal that names `directory` explicitly as
      riding its governing change. Until that repo re-pins, a `directory`
      roster entry FAILS its own local validator no matter what this
      vocabulary admits. So the FIRST downstream act is an OpsxFactory
      CONTRACT RE-PIN to the bundle this change's realization cuts, plus the
      matching `ROSTER_ADMITTED_SURFACE_VOCAB` / local-fence update — AHEAD of
      7.2, which then becomes possible. Precedent, exactly parallel: the
      `device` widening did not ride the openxFactory admission either, it
      landed separately in OpsxFactory as PR #45 (`77f4b82`, "Add device
      (node-inventory) planned roster entry + platform self-consent"), which
      re-pinned and widened the local fence to contract-v1.35 in one change.
      Also OpsxFactory's own work, listed here only so the ordering is not
      mis-stated on this side.
