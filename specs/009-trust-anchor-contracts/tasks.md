# Tasks: Trust-anchor neutral contracts

**Feature**: `009-trust-anchor-contracts` · **Change**: `add-trust-anchor`

Realizes the change's tasks §4.1, §4.2 and §5.1–5.9. The change's `tasks.md`
stays governance-level and is not duplicated here; §5.10 (registration at the
next additive bundle cut) is deliberately outside this feature.

## Phase 1 — settlements that gate the schema (change tasks 4.1, 4.2)

- [x] 1.1 Settle the closed chain-custody enumeration: three members, two
      declared booleans asked of the USING HOST, `evidences` DERIVED and
      enforced. Recorded in `research.md` with the ceilings, the assurance
      ladder, and the reasoning for three members rather than two.
- [x] 1.2 Settle escrow's place: NOT a custody tier, per the ratified OQ2 ruling.
      Read `ideation/staging/client-credential-escrow-registry/` and record in
      `research.md` how the enumeration stays compatible with that topic's
      direction — escrow attaches to the `credential-contracts` record every
      custody block already references, with one writer-moment and one
      reader-moment, neither of which changes what a certificate evidences at
      point of use.
- [x] 1.3 Make the escrow ruling STRUCTURAL rather than editorial: because
      `evidences` derives from exactly two booleans, a member declaring the same
      discriminator pair as another differs only in something this axis cannot
      express. Refused as a second axis or a rename.
- [x] 1.4 Settle the issuance-evidence floor: two establishment levels and
      nothing weaker representable; the floor requires BOTH halves and forbids
      the per-certificate provenance fields by shape; the conformance declaration
      carries the achieved level. Recorded in `research.md`.
- [x] 1.5 Settle the composition with `openxwallet`: per-member mapping, resolved
      against the canonical registry at run time rather than restated.

## Phase 2 — the closed set (change task 5.1's dependency)

- [x] 2.1 `chain-custody-registry.schema.yaml` — the mechanism: ordered assurance
      ladder, custody members with two booleans and derived `evidences`, the
      declared undeclared-custody floor, the openxWallet mapping, and the
      deliberate NON-members.
- [x] 2.2 `trust-anchor-chain-custody.registry.yaml` — THE closed set: three
      members, three assurance levels, four excluded models each with its reason.

## Phase 3 — anchors and certificates (User Story 1, P1)

- [x] 3.1 `trust-anchor.schema.yaml` (change task 5.1) — identity, chain
      position, validity, admitted issuance authorities, declared custody with
      its credential-record pairing or a declared shortfall, administration
      credentials brokered into ephemeral scope as a constant. Key material
      unrepresentable by shape.
- [x] 3.2 `certificate-record.schema.yaml` (change task 5.2) — anchor reference,
      subject, validity, key generation, declared chain custody, DERIVED
      `evidences` and assurance ceiling, issuance evidence or the honest absence,
      the dependent-binding enumeration, record defects, and the evaluation whose
      basis and standing check are constants.

## Phase 4 — issuance, dependents, renewal, revocation (User Story 2, P2)

- [x] 4.1 `issuance-evidence.schema.yaml` (change task 5.3) — anchor, admitted
      authority, request provenance, time, and the establishment level actually
      achieved, with the floor's conjunction and its forbidden fields.
- [x] 4.2 `dependent-binding.schema.yaml` (change task 5.4) — holding system
      inside or outside the family, what it binds, the key GENERATION referenced,
      required assurance and obligations, admission with its refusal shapes, and
      rebind status.
- [x] 4.3 `renewal-record.schema.yaml` (change task 5.5) — planning against the
      certificate's enumeration state, whether key material changed, the
      enumerated dependents, per-dependent rebind evidence, and a completion
      state that CANNOT read complete with an unevidenced dependent (schema
      `if/then`, not prose), with the failure attribution a constant.
- [x] 4.4 `revocation-propagation.schema.yaml` (change task 5.6) — the mechanism
      constant, what was revoked, the declared bounded window, subordinate
      certificates reached, per-authority propagation evidence, and the
      escalated-open-exposure state.

## Phase 5 — the conformance declaration (User Story 3, P3)

- [x] 5.1 `conformance-declaration.schema.yaml` (change task 5.7) — per
      obligation: satisfied / partial / cannot with a reason, closed over all
      eight, with addressable and dated entries so the two ratified guards are
      enforceable across records.

## Phase 6 — the validator

- [x] 6.1 `scripts/validate-trust-anchor.py` (change task 5.9) following the
      repo's `validate-*.py` shape: standalone, runtime-resolved root, `Findings`
      with kebab-case codes, self-test plus optional repo scan, exit 0/1/2.
- [x] 6.2 Thirty-four lettered rules the shapes cannot express, each citing the
      requirement it enforces. Twenty-seven at first landing; (bb) through (hh)
      were added by the 2026-08-21 adversarial review (see Phase 10).
- [x] 6.3 Read the openxWallet custody registry at run time and hold every
      chain-custody member to the member it claims to be.
- [x] 6.4 Wire into the repository validator bar the way `validate-openxwallet.py`
      is: family self-test with no arguments, repo mode against an explicit
      target, `--strict`, and the invocations documented in the family README.
      CORRECTED 2026-08-21: there is no single bar script in this repository —
      the convention is a per-family canonical validator plus a `tests/<family>/`
      suite CI runs under pytest, so the wiring is `tests/trust-anchor/`
      (`python3 -m pytest tests/trust-anchor/`) beside the README invocations.
- [x] 6.5 Design the repo-scan layer closed over the scanned repository from the
      start (index before validate; packaged corpus excluded by family path, not
      by this checkout's absolute paths; unresolved references refused
      unconditionally rather than guarded by empty-collection checks). Verified
      against a scratch consumer corpus.

## Phase 7 — the negative-confirmation corpus (change task 5.8)

- [x] 7.1 The TEN named violations, one probe each.
- [x] 7.2 Seven further probes for the custody enumeration itself — the ruling's
      sharp edge: the derivation, the unearned top level, the renamed top level
      (proving the rule keys on RANK), the collapse, escrow as a tier, a
      disagreeing openxWallet mapping, and a floor above the weakest member.
- [x] 7.3 Further probes for the clauses that would otherwise go unproven: a
      certificate outliving its anchor, trust under a revoked anchor, an
      unresolvable parent, an over-claimed `evidences`, a ceiling above the
      floor, a custody model outside the closed set, an unexplained certificate
      recorded as trusted, a certificate trusted on an unauthorized issuance, an
      unattended renewal reported complete, a failure blamed on the dependent, a
      failure naming the wrong dependents, a rebind claimed at the superseded
      generation, an unenumerated binding, an outage-discovered dependent with no
      defect, a defect closed without correcting the record, incomplete anchor
      transitivity, a revoked certificate trusted, window arithmetic, a hex
      encoding, a JWK exponent, a readable key with no credential record, an
      anchor below the strictest tier, a declaration omitting an obligation, an
      admitted binding over a declared gap, and a shortfall declared after the
      claim.
- [x] 7.4 `# requirement:` attribution plus closed coverage checking in both
      directions, so a requirement cannot silently lose its probe.
- [x] 7.5 34 positive examples forming ONE coherent story across two
      realizations, so every cross-record rule is exercised by records that agree
      with each other. (32 at first landing; the hardening added a host-readable
      partner root and the dependent binding that gives the certificate-side
      revocation closure something to be checked against.)
- [x] 7.6 Red-proof harness (`evidence/red-proof.py`) and its recorded output:
      all 50 non-`schema` finding codes load-bearing. The harness derives its
      code list from the fixture headers, so the hardening's twelve new codes are
      covered without editing it — which is the property that makes it a harness
      rather than a list.
- [x] 7.7 `traceability.yaml` — one row per ratified requirement with its
      artifact, its enforcing check, its probes, and its red-proof.

## Phase 8 — the family README and the change's task list

- [x] 8.1 `contracts/trust-anchor/README.md` with a `Status:` header naming the
      ratifying change, the kinds table, the closed custody set, the issuance
      floor, the validator invocations, and what the family deliberately does
      not do — including what no validator can check.
- [x] 8.2 Tick the change's own tasks 4.1, 4.2 and 5.1–5.9 with a DONE note each.
- [x] 8.3 Promotion bookkeeping (change task 6.1): move
      `ideation/staging/pki-trust-anchor-plane/` into the change's
      `supporting-docs/` per `document-lifecycle`, with the manifest recording the
      original staging path, the source revision, the transition date, per-file
      sha256 digests, and the origin block matching `.openspec.yaml` exactly.

## Phase 9 — the green bar

- [x] 9.1 `python3 scripts/validate-trust-anchor.py` — 0 errors, 0 warnings.
- [x] 9.2 `python3 scripts/validate-trust-anchor.py . --strict` — repo scan
      clean.
- [x] 9.3 `OPENSPEC_TELEMETRY=0 openspec validate --all --strict` green.
- [x] 9.4 `python3 specs/009-trust-anchor-contracts/evidence/red-proof.py` — all
      codes load-bearing.
- [ ] 9.5 NOT THIS FEATURE (change task 5.10): register the family in
      `contracts/manifest.yaml` and `contracts/CHANGELOG.md` at the next additive
      bundle cut, add the `contracts/README.md` index rows and the root README
      entries, and retire the staging INDEX row.

## Phase 10 — adversarial-review hardening (2026-08-21)

A cross-model adversarial review ran 52 constructed corpora against the landed
family and demonstrated fourteen bypasses. All fourteen are closed, each with a
new negative fixture so the corpus reaches the case forever. The full record —
what each was, what closed it, which fixture keeps it, and the five probes that
correctly still pass — is `traceability.yaml` under `review_hardening`.

- [x] 10.1 The declaration perimeter (findings 1, 2, 4): three fields the schemas
      required and nothing read — `authority_operated_by_family`,
      `operated_by_family`, `achieved_establishment_level` — plus the lateness
      guard that skipped rather than refused when a timestamp was absent.
- [x] 10.2 The key-material scan made ARMOR-INDEPENDENT (finding 3): decoded
      bytes tested for DER private-key structure, two decode layers, both base64
      alphabets, segment recovery from a polluted run, and the document's strings
      joined before the armor match. Five demonstrated evasions closed, each with
      its own fixture.
- [x] 10.3 `key_change.changed` verified against the certificate record, and a
      binding's generation compared without a renewal record in the way
      (finding 5).
- [x] 10.4 Revocation transitivity for CERTIFICATE targets (finding 6), and
      FR-017's wording corrected — it had narrowed the ratified R6 to anchors.
- [x] 10.5 Window-timed propagation evidence (finding 7), validity checked at use
      (finding 11), registry pointers resolved and a diverging registry claiming
      the canonical id refused (finding 9), the floor resolved in the document's
      own members (finding 10), duplicate obligation entry ids reported
      (finding 12).
- [x] 10.6 The point-of-use cost of a declared `cannot` (finding 8):
      `required_obligations` required and non-empty, a broad `cannot` set
      reported, and a binding requiring a `partial` obligation reported — with
      the error/warning split documented in the README (finding 14).
- [x] 10.7 `tests/trust-anchor/` (finding 13), which is what task 6.4's "wired
      into the repository validator bar" now means: 87 tests across three files.
- [x] 10.8 The green bar re-run: validator 0/0 with 34 positives and 65
      negatives, `. --strict` clean, red-proof OK at 50 codes, the new suite
      green, `openspec validate --all --strict` green, and
      `validate-openxwallet.py` green (the composition is unchanged).
