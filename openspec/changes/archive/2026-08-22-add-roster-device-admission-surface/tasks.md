# Tasks: add-roster-device-admission-surface

Sections §1–§5 are the REALIZATION and ran ONLY AFTER Brett ratified this
change; nothing touched the schema, validator, examples, or bundle before
ratification. They are all discharged — the evidence is in §7. §6 is a
downstream boundary owned by another repository, and §7 is the bookkeeping and
archive-gate record, added at the archive rather than at authoring.

## 1. Admit `device` into the schema vocabulary

- [x] 1.1 Add the `device` `oneOf` const member to `$defs.admission_surface`
      in `contracts/schemas/xfactory-client-identity-roster.schema.yaml`,
      mirroring the shape of the existing `business_central` and `exchange`
      members: a `const: device` with a `description` that names the admission
      act and scoping mechanism per design Ruling 3 — admin consent for the
      application read roles `Device.Read.All`,
      `DeviceManagementManagedDevices.Read.All` and `CloudPC.Read.All` on ONE
      identity (Entra registered devices + Intune managed devices + Windows 365
      Cloud PCs read); scoping mechanism is TENANT-WIDE READ with
      `exact_effective_scopes` and NO narrower provider selector; read-only.
- [x] 1.2 Leave `contract_schema_version` at `1` (design Ruling 4: adding a
      `oneOf` const member is back-compatible — no existing roster is
      reinterpreted). Confirm the CLOSED-ON-PURPOSE header's "Growth takes a
      `contract_schema_version` bump" comment governs object-shape/key-space
      growth, not vocabulary-member admission (which the EXTENSION ROUTE text
      governs).
- [x] 1.3 Update the `admission_surface` `description` extension-route text so
      it no longer lists Windows 365 among the surfaces still to arrive (it is
      now part of the admitted `device` read surface). Keep endpoint-MUTATION
      (Intune write) and Entra-DIRECTORY listed as SEPARATE future surfaces
      each arriving with its own governing change.

## 2. Keep the validator refusal string in sync

- [x] 2.1 The canonical validator DERIVES the closed vocabulary from the
      schema (`Vocabularies.admission_surface = _consts(defs.get("admission_surface"))`
      in `scripts/validate-client-identity-roster.py`), so NO vocab-constant
      edit is needed — `device` becomes admissible automatically once §1 lands.
- [x] 2.2 Update ONLY the human-facing `EXTENSION_ROUTE["admission_surface"]`
      refusal string in that validator to match the schema's revised
      extension-route text (§1.3): drop Windows 365 from the "still to arrive"
      list, keep endpoint/Intune-mutation and Entra-directory. This string is
      descriptive text a refusal cites; it is not the source of the vocabulary.

## 3. Package a `device` example and confirm the negative stays valid

- [x] 3.1 Add a packaged positive example entry using
      `admission_surface: device` under `examples/client-identity-roster/`
      (an entry, or a small fragment, transcribed from the node-inventory
      reader evidence). The example MUST use the governed-tenant-scope shape
      (design Ruling 2 + Adversarial fix F1) so the roster validator self-test
      passes on it:
      - `exceeds_governed_unit: false` — the governed unit IS the tenant-wide
        device estate, so tenant-wide read is the governed scope, not excess;
      - NO `declared_excess` block, and `spanned_surfaces` empty/omitted — the
        three provider areas (Entra / Intune / Windows 365) are NOT
        `admission_surface` consts, so they CANNOT appear in a structured
        breadth field (the schema would refuse them); they live only in the
        `device` member's `description` prose;
      - `per_unit_principal_available: {device: false}` — no per-unit
        principal; the governed unit is the whole tenant device estate;
      - each admission act `enforcement_mode: logic_enforced` — there is no
        provider scoping selector (unlike Exchange's `RestrictAccess`); the
        read is bounded by the exact read-only roles;
      - `blast_radius_unit` = the tenant-wide device estate (a clear token such
        as `tenant_device_estate`, described in the fragment legend);
      - read-only (`observe` only), transcribed from the ratified
        `microsoft_managed_node_inventory_reader` evidence.
      List it in `examples/client-identity-roster/README.md`.
- [x] 3.2 Confirm the `admission-surface-out-of-vocabulary` negative
      (`examples/client-identity-roster/negative/admission-surface-out-of-vocabulary.yaml`,
      which uses `sharepoint`) STAYS a valid negative — `sharepoint` is still
      outside the closed vocabulary, so the negative still fires. Do not change
      it.

## 4. Bundle bump contract-v1.34 → contract-v1.35 (digest refresh, additive)

- [x] 4.1 Recompute the `client-identity-roster` schema-row `sha256` in
      `contracts/manifest.yaml` for the edited schema file; leave the row's
      `schema_version: 1` unchanged (design Ruling 4).
- [x] 4.2 Set `contract_bundle_version: contract-v1.35` in
      `contracts/manifest.yaml`.
- [x] 4.3 Add a `contract-v1.35` entry to `contracts/CHANGELOG.md` in the
      established style: state it is ADDITIVE under
      `docs/contract-versioning-policy.md` (new vocabulary member; a domain on
      the same major version stays conformant without changes), and record the
      `device` admission-surface admission and its node-inventory evidence.
- [x] 4.4 Regenerate the release digests via the tooling — never hand-add:
      `python3 scripts/validate-contract-release.py build --tag contract-v1.35
      --output contracts/releases/contract-v1.35.digests.yaml` (and update the
      release README/index if the repo tracks one).

## 5. Validate green

- [x] 5.1 Run the roster validator self-test (its packaged-corpus pass over
      `examples/client-identity-roster/` including the new positive and the
      unchanged negatives) — green.
- [x] 5.2 `OPENSPEC_TELEMETRY=0 openspec validate --all --strict` — green.
- [x] 5.3 Any repo-wide contract/manifest validator
      (`scripts/validate-contract-release.py verify-commit …` and the
      manifest/digest checks) — green.

## 6. Downstream (NOT part of this change)

- [ ] 6.1 The OpsxFactory side — the `device` roster entry and node-inventory
      §6, which unblock `add-managed-node-inventory` task 5.x — is a DOWNSTREAM
      CONSUMER authored in the OpsxFactory repo under its own governance. It is
      out of scope here and does not land with this change. Listed for
      traceability only.
      STILL A RECORDED BOUNDARY AT ARCHIVE, not an open gap. This box stays
      unticked deliberately, the same way `refine-demote-round-trip-mechanics`
      archived with its §8 unticked by ruling: an unticked box here means "owned
      elsewhere", and ticking it would claim work this repository never did.

## 7. Bookkeeping and the archive gate

- [x] 7.1 README "OpenSpec Records" active block. The row was written at
      proposal time inside the realization pull request itself (#220 adds 14
      lines to `README.md`), then rewritten by the records sweep #241, which
      also corrected the row's claim that the change was still awaiting its
      implementation. On this archive the row moves from `Active changes:` to
      `Archived changes:` in date order, its link re-pointed at the archived
      folder, and the ratification rulings kept in the row rather than
      summarized away.
      ONE FALSEHOOD CARRIED IN THAT ROW IS CORRECTED ON THE MOVE. It read "the
      three provider areas ride the entry as declared provider-forced breadth"
      — which is exactly the framing adversarial finding F1 REJECTED before
      ratification. The ratified reading is the opposite: the governed unit IS
      the tenant device estate, so tenant-wide read is the GOVERNED scope
      (`exceeds_governed_unit: false`, no `declared_excess`, no
      `spanned_surfaces`), and the three provider areas live only in the
      member's `description` prose because the schema would refuse them
      anywhere structured. The row now says that.
- [x] 7.2 REALIZATION EVIDENCE, recorded at the archive gate, because
      `target_release: implementation_pending` archives only on merged code
      with green realization evidence.
      THE REALIZATION IS ONE PULL REQUEST, not a chain. Every commit that
      touches this change's folder or any surface §1–§4 names was enumerated
      (`git log -- openspec/changes/add-roster-device-admission-surface/`, and
      again over the schema, the validator, `examples/client-identity-roster/`
      and `contracts/releases/contract-v1.35.digests.yaml`), and the search for
      pull requests naming the roster, the device surface or the v1.35 cut
      returned only the roster capability's own two ancestors (#173, #190) and
      this one. The list below is that enumeration, not an inherited claim.
      • **PR #220** — "Extend roster admission_surface vocabulary: admit the
        device (node-inventory) surface", merged 2026-08-19T20:42:27Z as
        `78f8e01` (14 files, +1754/-8). FILES-TOUCHED TEST: it edits all six
        files of this change's own folder (`.openspec.yaml`, `proposal.md`,
        `design.md`, `tasks.md`, `review/ratification-2026-08-19.md`,
        `specs/client-identity-roster/spec.md`) AND every realization surface
        §1–§4 names, so it is this change's pull request on both halves of the
        test rather than a neighbour that happened to touch the same tree.
        SQUASH-MERGED, against this repository's rebase-merge habit, so the
        four branch commits are NOT individually reachable on `main` and must
        not be cited as if they were: `06d6875` (authoring), `6b158d9` (the F1
        fix), `52622d3` (ratification), `f69f61e` (realization) collapsed into
        the single-parent commit `78f8e01` (parent `ece236a`). Cite `78f8e01`.
      • **PR #241** — "README records sweep", merged 2026-08-22T00:17:30Z
        (`047d777`, branch tip `8924838`). NOT a realization pull request and
        not counted as one: it touches this change only through its
        `.openspec.yaml`, filling the absent `origin.approved_on: 2026-08-19`
        from the ratification record, and through the README row. Listed
        because the origin block it repaired is the block this archive is
        required to retain byte-for-byte.
      PER-TASK EVIDENCE, each read out of the tree at the archive tip rather
      than out of the pull-request description:
      • 1.1 — `- const: device` with its admission-act and scoping description
        at `contracts/schemas/xfactory-client-identity-roster.schema.yaml:122`.
      • 1.2 — `contract_schema_version` untouched; the manifest's roster row
        still reads `schema_version: 1` in the same diff that changed its hash.
      • 1.3 — the `$defs.admission_surface` header text was resliced exactly as
        specified: the closed vocabulary now reads "`business_central`,
        `exchange` and `device`", and the extension route's "still to arrive"
        list dropped Windows 365 while keeping "endpoint MUTATION / Intune
        write and Entra-directory".
      • 2.1 — no vocabulary constant exists to edit; the validator still
        derives the closed set from the schema at
        `scripts/validate-client-identity-roster.py:301`
        (`self.admission_surface = _consts(defs.get("admission_surface"))`).
      • 2.2 — the human-facing refusal string alone changed, one line, and now
        matches §1.3's schema text verbatim (`:317`).
      • 3.1 — the packaged positive is
        `examples/client-identity-roster/client-identity-roster-farheap-opsx.example.yaml:309`
        (`admission_surface: device`), listed in that folder's `README.md`.
      • 3.2 — the out-of-vocabulary negative is untouched by `78f8e01` and
        still carries `sharepoint`
        (`negative/admission-surface-out-of-vocabulary.yaml:26`), so it still
        fires.
      • 4.1 — the roster schema row's `sha256` moved `298bc37b…` → `5f21c727…`,
        and `sha256sum` over the schema file at the archive tip still returns
        `5f21c72724bfa2624a20c827b1ee3e68bbbb36746017883ab565e7f43fb23a6b`, so
        the manifest has not drifted from the file across the two bundle cuts
        since.
      • 4.2 — `contract_bundle_version: contract-v1.34` → `contract-v1.35`.
      • 4.3 — `contracts/CHANGELOG.md:271`, `## contract-v1.35 — 2026-08-19
        (additive; the `device` roster admission surface)`.
      • 4.4 — `contracts/releases/contract-v1.35.digests.yaml`, 1044 lines,
        generated by the tooling rather than hand-added.
      THE BUNDLE HAS MOVED ON and that is not drift: `contracts/manifest.yaml`
      reads `contract-v1.37` today, because `contract-v1.36` and
      `contract-v1.37` were cut after this one. `contract-v1.35` remains a
      released tag with its own digest inventory on disk; a later cut does not
      unmake it.
      GREEN RE-VERIFIED AT THE ARCHIVE TIP, not quoted from the merge run,
      exit codes read directly and never through a pipe:
      • 5.1 — the roster validator's packaged-corpus self-test: 4 positive
        examples confirmed clean and 31 negatives confirmed refused for their
        registered reason, `0 error(s) -> PASS`. Run from a clean path, because
        `sweep_files` skips any path with a `.git` segment and this archive was
        performed from a worktree under `.git/modules/`.
      • 5.2 — `OPENSPEC_TELEMETRY=0 openspec validate --all --strict`: 66
        passed / 0 failed before this archive, 65 after, both exit 0, the drop
        of exactly one being this change leaving the active set. Measured at
        the archive's FINAL base `c09fe68`, not at the branch's first: `main`
        moved under this slice three times mid-run
        (`34fb6ef` -> `433cb80` -> `58e4aec` -> `c09fe68`) and every reading
        was re-taken after each rebase rather than carried forward — the first
        pass read 65 -> 64 and was discarded, not reused. The base side was
        read from a separate checkout at `c09fe68` rather than inferred by
        subtraction.
      • 5.3 — `python3 scripts/validate-contract-release.py verify-commit
        --commit 78f8e01…` → `release verify-commit: pass`, exit 0, resolving
        `inventory=contracts/releases/contract-v1.35.digests.yaml`.
- [x] 7.3 THE ARCHIVE ACT, and why it used the bare CLI.
      `python3 scripts/proposal-support.py . verify
      add-roster-device-admission-surface` returned ok before the move, and the
      supporting-docs check that chooses the tool was run rather than assumed:
      this change owns NO `supporting-docs/` folder — its origin is `ad_hoc`
      and nothing was ever moved into it — so `document-lifecycle`'s promoted
      `Supporting-document archive retention` requirement, whose first clause
      is scoped to "an OpenSpec change WITH proposal supporting documents", has
      nothing to bind. The archive therefore used the bare
      `OPENSPEC_TELEMETRY=0 openspec archive add-roster-device-admission-surface
      --yes`, matching `refine-demote-round-trip-mechanics` (archived
      2026-08-21, same shape) rather than `add-staged-topic-outline-template`
      (same day, wrapper, because it DID own a folder). THE PREDICATE IS THE
      PRESENCE OF SUPPORTING DOCUMENTS, NOT THE ORIGIN KIND — the wrapper's own
      comment at `scripts/proposal-support.py:898-937` records that the
      bundle-less shape is the majority even among staged origins, and the
      wrapper now falls through to the same CLI call for it, so the two paths
      agree on this change and the bare one is simply the shorter of them.
      THE ARCHIVE FOLDER IS DATED 2026-08-22, not 2026-08-21, because the tool
      stamps the folder in UTC and the act fell just after midnight UTC on a
      machine reading 2026-08-21 locally. Recorded so the date is not later read
      as a backdating error. The archiver reported `Task status: 18/19 tasks`
      and continued under `--yes`: the single incomplete box is §6.1, the
      downstream boundary, unticked by design.
      ORIGIN RETENTION VERIFIED AGAINST PRE-ARCHIVE BYTES, because a check
      nobody performs is not a guarantee. `.openspec.yaml` hashes
      `76cb6f58d1246c0ea4eb8e96db189b4403e770acd120313a93646557e1c0c2f2`
      before the move and the same after it, still declaring `kind: ad_hoc`,
      the durable id `openxFactory:adhoc:2026-08-19-add-roster-device-admission-surface`,
      `approved_by: Brett` and the `approved_on: 2026-08-19` that #241 supplied.
      `proposal-support.py . verify` passes again on the archived shape.
- [x] 7.4 PROMOTED DELTA VERIFIED, requirement by requirement, rather than
      trusting the archiver's exit code.
      This change carries exactly ONE spec folder, `specs/client-identity-roster/`,
      holding exactly ONE `## MODIFIED Requirements` block and no ADDED or
      REMOVED block — so the whole promotion is one requirement moving, and the
      capability's requirement count must be unchanged by it.
      • `client-identity-roster` → `Identities are enumerated by admission
        surface, not by product name`, the FIRST requirement of the capability
        at `openspec/specs/client-identity-roster/spec.md:6`. The capability
        held 13 requirements before this archive and holds 13 after: a MODIFIED
        delta replaces, and no requirement was added, dropped or duplicated.
      • The scenario the delta exists for landed: `The device (node-inventory)
        surface is admitted` is now the requirement's THIRD scenario, after the
        two that were already promoted (`Two product names share one admission
        act`, `One product name has two admission acts`), and both of those
        survive verbatim — the ratification record's archive-fidelity claim
        held through the promotion, not merely through the delta.
      • The promoted body was DIFFED against the delta file rather than
        eyeballed: from the requirement heading to the end of the delta against
        the same span of the promoted spec, `diff` reports ONE line — the blank
        line the promoted file needs before `Identity uniqueness is keyed on
        surface, class, blast-radius unit and duty`. Every other byte,
        including all three scenarios, is identical. What did not promote is
        only the delta's own scaffolding: its `# client-identity-roster (delta)`
        title and the `## MODIFIED Requirements` header.
      • A repository-wide search for the requirement heading returns exactly
        ONE promoted location, `openspec/specs/client-identity-roster/spec.md:6`.
        The two other hits are both archived spec deltas — the original ADDED in
        `archive/2026-08-15-add-client-identity-roster/` and this change's
        MODIFIED — which is the expected shape for a requirement amended once,
        not a double promotion.
- [x] 7.5 WHAT THIS SLICE DELIBERATELY DID NOT EDIT, named rather than left for
      a later reader to wonder about. The proposal's `## What Changes` and
      `## Impact` bodies still speak of the realization in the future tense
      ("The realization (post-ratification, tasks §1–§5): add the `device`
      `oneOf` const member …", "ALL of this waits until ratification"). That is
      the RATIFIED BASELINE — the ratification record pins it as "this change as
      committed in the ratification commit" — and rewriting a ratified body to
      match later events would make the record describe a plan nobody approved.
      The banner is the sanctioned place to say the plan was executed, and it
      now does, so the two read correctly together: a ratified plan, followed by
      a realization block reporting that it happened. Only the front matter's
      `target_release`, the banner, and the `Ratified:` framing sentence were
      rewritten, because those three are status claims about the present rather
      than the approved content.
- [x] 7.6 THE ARCHIVE SLICE'S OWN GATES, exit codes read directly and never
      through a pipe, because a piped exit code reports the pipe.
      • `python3 -m pytest tests/ideation-dashboard -q` — exit 0, 3853 passed /
        14 skipped, re-run at the final base after `add-dashboard-account-menu`
        landed 431 tests into that suite mid-slice; the earlier 3761-passed run
        is superseded, not averaged.
      • `python3 -m pytest tests/doc-health -q` from the agent worktree — exit
        1, 4 failed / 687 passed, and the four are EXACTLY the known
        `.git`-segment location artifacts, enumerated rather than counted:
        `test_client_identity_composition.py::test_every_cross_domain_fixture_repo_passes_the_blocking_domain_gate`
        at `[alphaxFactory]`, `[betaxFactory]`, `[deltaxFactory]` and
        `[gammaxFactory]`. Nothing else failed.
      • THE SAME SUITE FROM A CLEAN PATH — exit 0, 691 passed, ZERO skips, so
        all 691 items are green and the four are a property of the path, not of
        the corpus. This suite was run there deliberately and not by rote:
        this change's whole subject matter IS client-identity roster
        admission, so the one family whose worktree failures are excused is
        the family it would break, and excusing them without the clean-path
        run would be excusing the only test that could catch it.
      • `python3 scripts/proposal-support.py . verify
        add-roster-device-admission-surface` on the ARCHIVED shape — exit 0,
        `proposal support verification ok`.
      • DOC-HEALTH, two full runs from IDENTICALLY-NAMED clean-path `git
        clone`s (never `git archive`, which drops the git-dependent
        `record-immutability` family), one at the base `58e4aec` and one at
        this branch tip, both `python3 scripts/doc-health.py --single-repo .`
        and both exit 0, the second given the first as `--previous-report`
        with `--new-findings-out`. The new-findings file is literally `[]`,
        and because an empty list proves little alone the two reports were
        also diffed RAW: findings identical at
        `3 critical, 7 error, 78 warning, 3 info`, the whole "Findings By
        Family" body byte-identical, and every Per-Stage row — docs AND words
        — unchanged.
        EXACTLY TWO LINES DIFFER IN THE WHOLE REPORT, both the same arithmetic
        and both accounted for to the word rather than accepted:
        (1) `(promoted specs)` 107388 -> 107466 words, and
        (2) canon share 156842 -> 156920 canon words of 508696 -> 508774
        governance words, the same +78 landing on the canon side of the same
        ratio, which stays 30.8%.
        (The pair was re-measured after each of the two rebases; an earlier
        pair against base `433cb80` gave the identical +78 on both lines at a
        governance total of 501489 -> 501567 and a ratio of 31.3%. The absolute
        totals moved because `contract-v1.38` landed in `contracts/` on main
        between the two bases; the delta attributable to THIS change did not.
        The third rebase, onto `c09fe68`, was NOT re-measured for doc-health
        and does not need to be: that commit touches only
        `scripts/ideation_dashboard/`, `tests/` and one active change's
        `tasks.md`, none of which is inside `GOVERNED_ROOTS` or
        `openspec/specs/`, so the corpus it reports on is byte-identical to
        the `58e4aec` pair's.)
        +78 IS THE PROMOTION ITSELF, counted: the four lines this archive added
        to `openspec/specs/client-identity-roster/spec.md` — the device
        scenario's heading and its WHEN/THEN/AND — are 78 words by `wc -w`.
        NOTHING MOVED FOR THE ARCHIVE MOVE ITSELF, nor for this slice's edits
        to `proposal.md` and `tasks.md`, and that is not luck: `corpus.py`'s
        `GOVERNED_ROOTS` is `contracts`, `docs`, `examples`, `ideation`,
        `templates`, so `openspec/changes/` is outside the staged corpus
        entirely and only `openspec/specs/` is counted, separately, as
        promoted specs. No location, aging, origin, immutability or
        register-consistency family reacted to the change folder relocating
        under `archive/`.
        ONE FALSE START RECORDED so it is not repeated: the first pair of runs
        used `--repo-root .` against the clone, which makes doc-health look for
        an AGGREGATION layout, find no `openxFactory/` inside it, and report
        `0 canon words / 0 governance words` with four families skipped as "not
        in scope". Those two reports were byte-identical, which would have
        looked like a clean result while measuring almost nothing. `--single-repo`
        is the flag for a lone repository checkout, and the numbers above are
        from that.
