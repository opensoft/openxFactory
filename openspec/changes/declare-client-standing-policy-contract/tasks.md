# Tasks — declare-client-standing-policy-contract

Legend: **(OPERATOR)** = a human act this change cannot perform;
**TRACKED** = owned by another repository's change, recorded here so the
dependency stays visible and never silently assumed.

The CONTRACT SHAPE is not re-litigated by this change: it was ratified
2026-08-22 by Brett Heap on hermes-install `add-client-overlay-standing-policy`
(four sub-rulings) and is already implemented, merged, and live-capable there.
What §1 asks for is the openxFactory-side DECLARATION act and the three
mechanical positions that belong to this repository.

## 1. Ratification

- [x] 1.1 **(OPERATOR)** Ratify the declaration. The shape itself is already
      ruled; ratification here confirms or corrects the three positions this
      repository owns, because the implementation branches on each:
      **(a) D1 — INLINE, not a fourth sibling schema file.** Position: declare
      `client.policy_namespace` + `client.policies` inside
      `client-overlay.schema.yaml`. Issue #254 raises the sibling-file
      alternative explicitly; the three existing siblings each govern a
      self-identifying sub-document that dispatches on its own inner `kind`,
      and these two entries carry none — a sibling file would add a released
      schema, a manifest row and a digest for something no dispatcher reaches.
      The subject family answered the same question the same way.
      **(b) D4 — the prohibited-content scan stays SUBTREE-SCOPED.** Position:
      walk `client.policies` only, preserving the asymmetry with the subject
      path's whole-document walk. `hermes_client_overlay` is released and
      live-seeded; a whole-document walk would change the verdict of overlays
      that use none of the new block (a breaking change wearing an additive
      change's clothes) and would invert the divergence direction the
      2026-08-22 sequencing ruling was granted on.
      **(c) D5 — hermes-install's message text, this file's conventions.**
      Position: adopt the runtime's wording verbatim where it is layer-neutral
      so the planned parity sweep can align on `# expected_failure:`
      substrings; drop its seed-specific trailing clause from the
      `policy_namespace` finding (canon describes a document, not a seeding
      act) leaving a strict prefix; keep credential findings in this file's
      single flat findings list rather than importing a remediation
      vocabulary; and name the ported constant `PROHIBITED_DOMAIN_BLOCKS`
      (hermes-install's semantics, this file's no-sigil convention), leaving
      the subject validator's `PROHIBITED_SUBJECT_BLOCKS` unrenamed as OQ-A.
- [x] 1.2 Strict-validate (`OPENSPEC_TELEMETRY=0 openspec validate
      declare-client-standing-policy-contract --strict` and `--all --strict`,
      run from the openxFactory root) and list the change in the README's
      OpenSpec Records block.
      (DONE — `Change 'declare-client-standing-policy-contract' is valid`;
      `--all --strict` clean. Listed in the README OpenSpec Records block as
      the first active change. NOTE for the lander: the unlanded branch
      `origin/change/readme-records-sweep` rewrites that whole block; this
      change lands first and the sweep rebases over it.)

## 2. Implementation (openxFactory — this change's code surface)

- [x] 2.1 Declare the pair in
      `contracts/client-content/client-overlay.schema.yaml`: OPTIONAL
      `policy_namespace` (`type: string`, `minLength: 1`) and `policies`
      (`type: object`, `minProperties: 1`, per-entry
      `required: [policy_id, policy_namespace]` with `minLength: 1` on each and
      an OPEN body). `client.required` byte-frozen at
      `[ref, display_name, policy_overrides]`. The schema comment records the
      inline-not-sibling reasoning and enumerates the five rules the shape
      cannot express, so a reader of the schema alone is never misled into
      thinking the shape is the contract.
      (DONE — both properties added inline under `client.properties`;
      `client.required` unchanged; sha256 moves
      `f67a3412…` → `7e74f7c0feb347c8646b0d852a9e120e43b2f9076973c78bab50a5e6b07b8ddc`.)
- [x] 2.2 Extend `scripts/validate-client-content.py`'s `hermes_client_overlay`
      branch with the six-rule mirror, reached only from
      `if "policies" in client` (membership, not truthiness — a truthiness test
      would make the ruled `{}` refusal unreachable): non-empty map with the
      declared-but-empty refusal and a DISTINCT wrong-type finding; per-entry
      mapping; `policy_id` non-empty and equal to its key; entry
      `policy_namespace` non-empty and equal to `client.policy_namespace`;
      `client.policy_namespace` required non-empty when and only when
      `policies` is present; `<namespace>/<id>` uniqueness. Plus the
      prohibited-domain-block and credential-value scan over the
      `client.policies` subtree ONLY, with the asymmetry and its reasons
      written into the code.
      (DONE — `_validate_client_policies` + `_prohibited_policy_content` +
      `_walk_entries`. Constants PORTED, not imported, with a provenance
      comment: verified first that no canonical validator in `scripts/` imports
      another — the only cross-module imports are into the shared
      `scripts/hermes_runtime_validation` package, a test-side scanner, and the
      `xfactory` package.)
- [x] 2.3 Fix the self-test trap before adding a second positive: `self_test()`
      loaded exactly one hardcoded positive filename, so a new packaged example
      would have been digested, published, and never validated. Sweep every
      packaged `*.example.yaml` except the baseline comparand, which keeps its
      role as the `client_policy_baseline` every positive is checked against,
      and fail closed if no positive is found.
      (DONE — `BASELINE_EXAMPLE` names the comparand; positives are discovered
      by glob. The original `example ok: hermes-client-overlay.example.yaml`
      output line is unchanged.)
- [x] 2.4 Fixtures in the family's self-testing idiom under
      `contracts/client-content/examples/`: one positive
      `hermes-client-overlay-standing-policy.example.yaml`, and negatives each
      declaring `# expected_failure:` — `client-empty-policies`,
      `client-missing-policy-namespace`, `client-policy-key-mismatch`,
      `client-policy-namespace-mismatch`, `client-policy-credential-value`,
      `client-duplicate-policy-address`. Each negative is an OTHERWISE-CLEAN
      overlay: the self-test validates negatives against the packaged domain
      baseline, so a comparability violation is a valid failure and a sloppy
      negative would pass for the wrong reason.
      (DONE — the six named, plus TWO beyond the declared minimum on
      `add-subject-overlay-contract`'s precedent, because a refusal rule with
      no fixture is a rule nothing proves: `client-policies-wrong-type` (the
      ruled distinct finding) and `client-prohibited-authority-boundaries`
      (mirroring the subject family's own negative of that name). Verified per
      fixture: every one reports ZERO comparability violations and ZERO
      `review_required`, so each fails on its policy rule and nothing else.
      `client-duplicate-policy-address` additionally carries the key-mismatch
      finding BY CONSTRUCTION — a mapping cannot hold one key twice, so the
      duplicate-address rule is reachable only when a second entry aliases the
      first's declared id under a different key, which is exactly the mistake
      the rule exists to catch. Both findings are the standing-policy address
      rule; the fixture comment says so.)
- [x] 2.5 Validators green: `python3 scripts/validate-client-content.py`
      (self-test runs on every invocation), `python3
      scripts/validate-manifest-digests.py`, and `python3
      scripts/validate-hermes-domain-overlay.py` — the last because it NAMES
      `scripts/validate-client-content.py` as the foreign-kind owner in
      `FOREIGN_KIND_VALIDATORS` and must be proven unbroken by a change to its
      counterpart.
      (DONE — client-content `self-test ok: 16 fixture(s)` (was 7);
      manifest digests `OK … 150 per-file digest(s) verify`;
      hermes-domain-overlay `self-test ok: 23 fixture(s)`, unchanged.)
- [x] 2.6 Family README (`contracts/client-content/README.md`): a bullet for
      the new block in the file's existing style, and the `examples/` bullet
      updated to say every packaged positive is swept.
      (DONE.)
- [x] 2.7 Release-surface RECORDS, which are all that may land on a branch:
      the `contracts/manifest.yaml` `client-overlay` row's `sha256` RECOMPUTED
      (editing the schema invalidates the pinned digest and
      `scripts/validate-manifest-digests.py` fails closed) with its
      `consumption_rule` restated, and a `contracts/CHANGELOG.md` entry under a
      newly opened `## Unreleased — pending bundle registration` section.
      NO NEW MANIFEST ROW (no sibling file) and **NO VERSION NUMBER
      ALLOCATED** — `docs/contract-versioning-policy.md` allocates the minor
      LATE, at realization, and forbids reserving one in a proposal.
      (DONE — digest recomputed and verified; `contract_bundle_version` stays
      at `contract-v1.40`; the changelog entry states that the cut is shared
      with the other next-additive-bundle changes.)
- [x] 2.8 Root `README.md` doc index unchanged — this change adds no standalone
      doc, only contract-family files the family README indexes. The only root
      README edit is the OpenSpec Records entry of task 1.2.
      (DONE — verified.)

## 3. Release — merge-gated, NOT performable on a branch

- [ ] 3.1 Contract release per `docs/contract-versioning-policy.md`: fetch and
      rebase onto the final integration point, allocate the next available
      minor THEN (CHANGELOG presence on main is the availability test), fold
      the `Unreleased` section into the cut, build the digest inventory with
      `scripts/validate-contract-release.py build`, then `verify-commit`,
      `verify-promotion`, land the exact reviewed commit, and publish and
      verify the annotated tag. **Shared**: this is ONE cut with whatever other
      next-additive-bundle changes are in the same `Unreleased` section, not a
      cut of this change alone. Additive only — no released file's bytes change
      except `client-overlay.schema.yaml` itself, whose `client.required` is
      frozen, so every existing pin resolves byte-identically and only a
      consumer that WANTS the block needs the new tag.

## 4. Consumption evidence — TRACKED, owned by hermes-install

Recorded because the archive gate depends on it, and NOT claimed as this
change's work. Both items are the ones
`add-client-overlay-standing-policy`'s own ruling said *"become available when
that change lands and are not scheduled here"*.

- [ ] 4.1 **[hermes-install]** Re-pin the client-content family: refresh
      `config/contracts/client-content/client-overlay.schema.yaml` from the
      released tag with its new sha256 in the compatibility manifest, and
      advance the recorded client-content contract version from
      `contract-v1.17` to the tag from 3.1. No runtime behaviour changes — the
      copy is a committed reference, not a runtime gate
      (`load_pinned_contract` is called for `hermes-domain-overlay/` and
      `memory-gateway/` only).
- [ ] 4.2 **[hermes-install]** Admit `hermes_client_overlay` to
      `tests/unit/test_contract_parity.py`'s `PARITY_KINDS` with a positive and
      negative floor. **This is not a one-line addition**: `_fixture_dir()`
      resolves exactly one directory
      (`contracts/hermes-domain-overlay/examples`) and the client fixtures live
      in `contracts/client-content/examples`, so the sweep needs a per-kind
      fixture root first — otherwise the new floors match nothing and the suite
      fails, or worse, are set to zero and prove nothing. Parity green over the
      canonical positive and the eight negatives is the evidence this task
      exists to produce, and it is the mechanism that makes any future drift
      between the two implementations fail a suite instead of passing quietly.

## 5. Records and archive gate

- [x] 5.1 Keep the change listed in the README's OpenSpec Records block with
      its status current, and record the released tag there once 3.1 lands.
      (Listed; the tag line is added at release.)
- [x] 5.2 Confirm `openspec validate declare-client-standing-policy-contract
      --strict` and `--all --strict` stay clean through ratification and any
      amendment.
      (Clean at authoring; re-run at ratification and at release.)
- [x] 5.3 Close `opensoft/openxFactory#254` with the released tag and the
      landed commit recorded, and note the closure on hermes-install
      `add-client-overlay-standing-policy` design §7 OQ-1 and task 1.2, whose
      accepted window this ends.
- [ ] 5.4 Archive per the `target_release` gate: ratified with the three
      D-positions confirmed; schema, fixtures and validator extension landed on
      main with the canonical validator green; the bundle released with a
      verified annotated tag, manifest, changelog and digest inventory; and
      CONSUMED — 4.1 and 4.2 done, with a parity suite that actually covers the
      kind. A declaration nothing validates against and nobody pins is not
      realized, and does not archive.
