# Tasks: add-trust-anchor

Governance-level and dependency-ordered. **This change is not being
implemented now**: §1 is authored here, §2 is time-critical and gated by
another change's ratification rather than by this one, and §3 onwards are
for the future implementer. The executable contract list belongs to the
single Speckit feature §5 hands off to; do not duplicate it there.

## 1. Spec deltas (THIS CHANGE)

- [x] 1.1 `trust-anchor` — eight ADDED requirements: anchors as governed
      records that systems trust (certificates only derivatively); issuance
      only under recorded authority with evidence stated as what it must
      ESTABLISH; declared chain custody deriving what a certificate
      evidences; renewal-as-rebind with the failure attributed to the
      issuing workflow; dependent bindings recorded against the
      certificate; revocation propagating to the authority the certificate
      supported within a declared window; authority material and issuance
      credentials as `credential-contracts` records with no QA exemption;
      and the declared-degraded-obligation rule.
- [x] 1.2 `repo-boundary-governance` — ONE ADDED requirement, "OpenXPKI
      install repository boundary", on the ratified avatar-client template.
      ADDED and not MODIFIED, per design D8 — the sibling
      `add-identity-brokering` needs the same admission in the same window
      and two MODIFIED deltas over one requirement race.
- [x] 1.3 `OPENSPEC_TELEMETRY=0 openspec validate add-trust-anchor
      --strict` green; `--all --strict` green before commit.

## 2. Time-critical: amend `add-openxpki-qa-image-pipeline` (OpsxFactory)

Not gated on this change's ratification. Gated by the OTHER change's
ratification, which it must precede (design D7).

- [x] 2.1 DONE 2026-08-21 — all three sites amended (Impact split into the tenant-owned image-custody surface and the OpenXPKI-Install topology home; What-Changes bullet 3 re-pointed; tasks gained a 3.4 migration obligation, since the change's QA tasks were already executed with the manifests authored in Opensoft-Tenant during bring-up — the amendment records that location as transitional, not governed). In the OpsxFactory repo, amend the active change
      `add-openxpki-qa-image-pipeline` in three places that today home the
      QA deployment manifests in `opensoft/Opensoft-Tenant`: its **Impact**
      section, its **"What Changes" bullet 3**, and its **tasks §3**.
      Re-point the deployment-manifest scope to
      `OpenXPKI-Install`; leave the image-custody scope (build,
      release / package / configuration / base-image pins, offline and
      integration harness, ACR digest) exactly where it is.
- [x] 2.2 DONE 2026-08-21 — `openspec validate add-openxpki-qa-image-pipeline --strict` green post-amendment; the cross-reference to this proposal is recorded in its Impact. Re-validate that change `--strict` after the amendment and record
      the cross-reference to this proposal in its Impact section, so a
      reviewer reading either one finds the other.
- [ ] 2.3 STATUS 2026-08-21: on the good branch — the amendment is in the change's draft text BEFORE ratification (the change is still an uncommitted working-tree draft owned by its authoring session; it was found already implemented through its QA gate, tasks 3.x/4.x checked, but unratified). Close this box when that change ratifies with the amendment aboard. Confirm the amendment landed BEFORE that change is ratified. If
      it ratifies first, the correction becomes a follow-up change against
      ratified text rather than an edit to a draft — record which happened.

## 3. Ratification gate

- [x] 3.1 DONE 2026-08-21 — ratified with OQ1 and OQ2 ruled per their recommendations (see the proposal's Ratification section). Brett ratifies proposal, design, and both spec deltas, ruling
      OQ1 (issuance-evidence strictness for an authority we do not operate)
      and OQ2 (chain-custody tiers closed or open; whether operator escrow
      is a tier at all) — the two the staged topic flags as hardest.
- [x] 3.2 DONE 2026-08-21. Record the rulings in `proposal.md` as a Ratification section and
      set the front-matter `Status:` to `ratified` with `Ratified by:`.
      Ratification authorizes exactly one Speckit contract feature and
      creates no authority, anchor, key, or runtime.
      **Respelled 2026-08-23** by `govern-openspec-corpus-membership` slice
      5A.1 under OQ-4's ruling: real line 5's prefix became `Ratified:`, the
      bytes after the colon carried verbatim, because the line names an
      approver and a date rather than an approving OpenSpec change. The record
      that justifies it is Brett Heap's 2026-08-21 in-session ruling, quoted on
      the line itself — "ratify both proposals" — with OQ1 and OQ2 both ruled
      as recommended, which is what 3.1 above records.

## 4. Settle before the schema is authored

Both items are contract content, not implementation detail, and both are
cheap now and expensive after a bundle ships.

- [x] 4.1 DONE 2026-08-21 — SETTLED and recorded in `specs/009-trust-anchor-contracts/research.md`: three members, two declared booleans asked of the USING HOST, `evidences` DERIVED (`host_held` / `host_isolated_invocable` -> using_host; `host_isolated_per_use_authorized` -> named_holder), with the assurance ladder each caps. Escrow is NOT a member per the ruling, and that is now STRUCTURAL rather than editorial: because `evidences` derives from exactly two booleans, a member declaring the same discriminator pair as another differs only in a fact the axis cannot express, and an escrow member has no choice but to duplicate a pair. Compatibility with `client-credential-escrow-registry` is recorded — escrow attaches to the `credential-contracts` record every custody block already references, one writer-moment and one reader-moment, neither changing what a certificate evidences at use. OQ2 — the custody enumeration and what each member EVIDENCES,
      settled with the `client-credential-escrow-registry` topic in the
      room. Carry the `openxwallet` lesson: a set that fails to distinguish
      a key readable by its own host from one isolated from it lets the
      first claim the second's authority.
- [x] 4.2 DONE 2026-08-21 — SETTLED and recorded in `research.md`: two establishment levels and nothing weaker representable. `per_certificate_record` requires established provenance (requester, request id, time); `per_policy_attestation_with_authority_log` requires BOTH halves and FORBIDS the per-certificate fields by shape, so asserting what the authority cannot establish is unrepresentable rather than discouraged. The conformance declaration carries `achieved_establishment_level` on the issuance obligation wherever it is satisfied or partial. Obligation entries gained an `entry_id` and their own `declared_at` so the two ratified guards (a declared gap is not permission; late declaration does not validate earlier claims) are enforceable across records. OQ1 — the declared floor for issuance evidence (per-certificate
      record where the authority exposes it; per-policy attestation plus
      the authority's own log as the declared floor where it does not), and
      the shape of the conformance declaration that carries the difference.

## 5. Contract realization (one Speckit feature)

REALIZED 2026-08-21 by Speckit feature `009-trust-anchor-contracts`
(`specs/009-trust-anchor-contracts/`). One settlement beyond the list below,
recorded in that feature's `research.md`: the closed custody set needs a
REGISTRY document, not an inline enum — an enum duplicated across two schemas
cannot carry a rule OVER its members, and the derivation is exactly such a rule.
So the family adds `chain-custody-registry.schema.yaml` plus the closed instance
`trust-anchor-chain-custody.registry.yaml`, mirroring the ratified
`openxwallet-custody-registry` pair that OQ2's ruling pointed at.

- [x] 5.1 DONE 2026-08-21 — `contracts/trust-anchor/trust-anchor.schema.yaml`. Key material unrepresentable by shape (closed objects at every depth; the only key-adjacent value is a pattern-restricted digest), custody paired with a credential record + vault binding OR a declared shortfall, administration credentials brokered into ephemeral scope as a `const: true`. NEW `contracts/trust-anchor/trust-anchor.schema.yaml`
      (`schema_version`, `kind`): anchor identity, chain position, validity
      window, admitted issuance authorities, declared custody. Key
      material is unrepresentable by shape.
- [x] 5.2 DONE 2026-08-21 — `contracts/trust-anchor/certificate-record.schema.yaml`, with `trust_evaluation.basis` and the standing check's basis as CONSTANTS, `evidences`/`assurance_ceiling` derived and recomputed, and the dependent-binding enumeration carrying its own completeness state. NEW `contracts/trust-anchor/certificate-record.schema.yaml`:
      anchor reference, subject, validity, declared chain custody, derived
      `evidences`, and the dependent-binding set (§5.4).
- [x] 5.3 DONE 2026-08-21 — `contracts/trust-anchor/issuance-evidence.schema.yaml`, carrying the §4.2 floor: two levels, the conjunction at the floor, and the per-certificate provenance fields forbidden there. NEW `contracts/trust-anchor/issuance-evidence.schema.yaml`:
      anchor, admitted authority reference, request provenance, time, and
      the establishment level actually achieved (per §4.2).
- [x] 5.4 DONE 2026-08-21 — `contracts/trust-anchor/dependent-binding.schema.yaml`. The key GENERATION is the join, so "still pointing at superseded material" is a comparison rather than an intuition; `inside_family` is required because the obligation reaches outside. NEW `contracts/trust-anchor/dependent-binding.schema.yaml`: the
      system holding the binding, what it binds, the key material
      referenced, and rebind status — the record that makes the rebind set
      computable before a renewal (design D4).
- [x] 5.5 DONE 2026-08-21 — `contracts/trust-anchor/renewal-record.schema.yaml`. STRUCTURAL, not prose: `completion_state: complete` forces every rebind entry to carry succeeded evidence (schema `if/then`), `failure.attribution` is a constant naming the issuing workflow, `arises: false` forces the rebind list empty, and no rule anywhere keys on `renewal_mode`. NEW `contracts/trust-anchor/renewal-record.schema.yaml`: whether
      key material changed, the enumerated dependents, per-dependent
      rebind evidence, and a completion state that cannot read
      "successful" with an unevidenced dependent.
- [x] 5.6 DONE 2026-08-21 — `contracts/trust-anchor/revocation-propagation.schema.yaml`. The window's arithmetic is recomputed, `mechanism.realized_through` is a constant naming openxWallet's derivation rule, and the open-exposure escalation is timed against the record's own `assessed_at` rather than the wall clock. NEW `contracts/trust-anchor/revocation-propagation.schema.yaml`:
      what was revoked, the declared bounded window, the downstream
      authority reached, propagation evidence, and the
      escalated-open-exposure state for a window that closed unevidenced.
- [x] 5.7 DONE 2026-08-21 — `contracts/trust-anchor/conformance-declaration.schema.yaml`, closed over all eight obligations with a reason and a date on each. NEW
      `contracts/trust-anchor/conformance-declaration.schema.yaml`: per
      obligation — satisfied / partial / cannot, with a reason — the
      artifact D6 depends on.
- [x] 5.8 DONE 2026-08-21 — 34 positive examples forming one coherent story across two realizations, plus 65 intended-invalid fixtures (32 + 43 at first landing; the adversarial review of the same day added two positives and twenty-two negatives, one per demonstrated bypass — see `traceability.yaml` `review_hardening`). All TEN named negative confirmations are present (the mapping is listed in `specs/009-trust-anchor-contracts/traceability.yaml` under `named_negatives`), with 8/8 requirements covered and coverage closed in both directions. Packaged positive examples plus a NEGATIVE CONFIRMATION per
      requirement: key material in an anchor record; a certificate trusted
      with no held anchor; issuance with no admitted authority; asserted
      provenance the authority cannot establish; a host-held certificate
      claiming hardware-bound assurance; a renewal reported successful with
      an unevidenced dependent; a renewal planned against an incomplete
      dependent set; a revocation window closed with no propagation
      evidence; authority key material in a repository (including a
      reversible encoding) with "QA only" as the reason; and an
      undeclared unsatisfied obligation.
- [x] 5.9 DONE 2026-08-21 — `scripts/validate-trust-anchor.py`: 34 lettered rules the shapes cannot express (27 at first landing, seven added by the same day's adversarial review), self-test plus repo-scan layers, exit 0/1/2, green on the whole corpus (0 errors, 0 warnings, `--strict`). It READS `contracts/openxwallet/openxwallet-custody.registry.yaml` at run time and holds every chain-custody member to the openxWallet member it claims to be, which is how the ratified "composes with rather than restates" clause became structural. Red-proof recorded: all 50 non-`schema` finding codes are load-bearing. WIRED IN, corrected: this repository has no single "validator bar" script — the convention is a per-family canonical validator plus a `tests/<family>/` suite that CI runs under pytest. So the wiring is `tests/trust-anchor/` (three files: the validator's exit code and reported corpus counts; every negative fixture adjudicated independently; and the declaration-perimeter rules whose cases need two records that disagree), run with `python3 -m pytest tests/trust-anchor/`, alongside the invocations documented in the family README. The earlier note's "wired into the repository validator bar" named nothing that existed. NEW canonical `scripts/validate-trust-anchor.py`, wired into the
      repository validator bar, green on the whole example corpus.
- [x] 5.10 DONE 2026-08-21 — registered at **`contract-v1.37`** (bundle bumped from `contract-v1.35`), the minor number allocated AT realization per `docs/contract-versioning-policy.md` § "Bundle Realization Order" — never reserved ahead of merge order — with the annotated tag applied post-merge to the exact realized commit. NINE files carry a per-file `sha256` in `contracts/manifest.yaml` under a `contract-v1.37` registration block, each with a distilled `consumption_rule`: the seven schemas plus the chain-custody registry SCHEMA and its closed registry INSTANCE (the `openxwallet-custody` pair convention that §5's settlement pointed at). `scripts/validate-manifest-digests.py` verifies 150 digests (was 135; +15 across both sibling families). The `contract-v1.37` CHANGELOG entry lists every file, states the additive class against the no-changes-required test, records that no `contract_schema_version` is bumped, and carries the realization plus adversarial-review-hardening provenance. Index rows added to `contracts/README.md` (family + validator/corpus/pytest wiring) and a conformance bullet to the root `README.md`. Per the openxWallet precedent the packaged corpus, the family README, `scripts/validate-trust-anchor.py` and `tests/trust-anchor/` are content-addressed by commit with NO per-file digest, so consumers pin the released bundle rather than copying a shape. Register the family in `contracts/manifest.yaml` and
      `contracts/CHANGELOG.md` at the next additive bundle cut, allocating
      the version per `docs/contract-versioning-policy.md`. Consumers pin
      the released bundle rather than copying a shape.

## 6. Promotion bookkeeping

- [x] 6.1 DONE 2026-08-21 — moved with the canonical tool (`scripts/proposal-support.py . transition add-trust-anchor ideation/staging/pki-trust-anchor-plane --apply`), which moved the file to `openspec/changes/add-trust-anchor/supporting-docs/pki-trust-anchor-plane.md`, wrote a byte-identical `source-snapshots/` copy, set the promoted prose's `Status:` header per `document-lifecycle`, rewrote its relative links, wrote `supporting-docs/manifest.yaml` (origin path, source revision, transition date, per-file `sha256` plus the source hash and snapshot path), and removed the emptied staging folder. `python3 scripts/proposal-support.py . verify add-trust-anchor` reports ok. Move the staged topic fragment
      `ideation/staging/pki-trust-anchor-plane/pki-trust-anchor-plane.md`
      into this change's `supporting-docs/`, preserving its `Status:`
      header per `document-lifecycle`.
- [x] 6.2 DONE 2026-08-21 — FULL promotion, so the INDEX maintenance rule's full-promotion branch governs and OVERRIDES this task's "update its detail section" phrasing: no staged file remains, so the row AND the detail section are DELETED from `ideation/staging/INDEX.md`, and the pointer — carrying the exit record this task asked for — moves to `ideation/README.md`'s "Active proposals promoted from staging" list. THE ONE DELIBERATE DIVERGENCE IS STATED THERE EXPLICITLY rather than left to inference: the topic's R1 called for the `repo-boundary-governance` install-repository enumeration to be MODIFIED, and the change instead ADDS a per-repo requirement for the `OpenXPKI-Install` boundary (design D8), which is the sibling-collision avoidance `add-identity-brokering` mirrors. Row/section parity re-verified: 33/33 -> 31/31, with neither retired slug present in either list. Retire the `pki-trust-anchor-plane` row in
      `ideation/staging/INDEX.md` and update its detail section to record
      the exit — including the one deliberate divergence from the topic
      (R1's MODIFIED enumeration became an ADDED requirement; design D8),
      so a reader is not left to infer it.
- [x] 6.3 DONE 2026-08-21 — the entry was already listed under "Active changes" in the openxFactory README "OpenSpec Records" block; this pass APPENDS the realization to it — REALIZED 2026-08-21 by Speckit feature `009-trust-anchor-contracts`, the schemas/registry-pair/validator/pytest-wiring/corpus named, hardened by the two-panel adversarial review, registered at `contract-v1.37` — and adds a trust-anchor conformance bullet to the README's validator list beside `validate-openxwallet.py`. The second clause — moving the entry out of "Active changes" when the change archives — remains OPEN by design. List this change in the openxFactory README "OpenSpec Records"
      block, and move the entry when it archives.
- [x] 6.4 DONE 2026-08-21 — noted where a reader reaches it, now that the INDEX detail section is gone: the `ideation/README.md` promoted-list pointer for this change states outright that the topic folder is `pki-trust-anchor-plane` while the change is `add-trust-anchor`, and that R1/R7 were ruled ONCE across this topic and `identity-brokering-plane`; the sibling pointer says the same from the other side; both README "OpenSpec Records" entries name each other as siblings; and the appended realization note in `ideation/brainstorm/keycloak-identity-brokering.md` records that the PKI side it did not anticipate realized in the same `contract-v1.37` cut. Note the shared-topic relationship: the topic folder is
      `pki-trust-anchor-plane` while the change is `add-trust-anchor`, and
      R1/R7 were ruled once across this topic and
      `identity-brokering-plane`.

## 7. Successor handoffs (named here, executed elsewhere)

Each pins the released contract bundle rather than restating its shapes.

- [ ] 7.1 **OpsxFactory `pki-administration`** — a workflow capability,
      SIBLING of `exchange-administration`,
      `aks-administration-workflow`, `github-administration-workflow`, and
      `business-central-administration`, not a profile of one of them
      (R7). The certificate-authority service-subject kind registers in
      lockstep: `customer-kinds` **and** the Hermes template **and**
      `stack.yaml` in the same change, with grant ceilings in
      `credentials/requirements.yaml`. Developed in
      `OpsxFactory:staging:identity-pki-administration`.
- [ ] 7.2 **`OpenXPKI-Install` creation** — the named successor
      the `repo-boundary-governance` requirement points at: create the
      private repository, move the QA deployment topology (server /
      client / web) per the custody split, and land the first
      `config/clients/<tenant>/runtime-manifest.yaml` (generated, never
      hand-edited). No build sources, secrets, or key material.
- [ ] 7.3 **Aggregation admission** — a SEPARATE reviewed change pinning
      `installs/openxpki-install`, recording path, remote, visibility,
      exact validated commit, recursive checkout, compatibility, update,
      and rollback. Repository creation is not admission.
- [ ] 7.4 **The cloud-PKI canary's governed record** — scoped only after
      the seam with `add-cloudpc-worker-fleet-management` and the
      worker-enrollment broker's device identity is checked (OQ5). The
      OpsxFactory `incident-diagnostics-and-intervention` topic's question
      about how TPM-backed keys are issued, attested, and rotated is
      answered from this contract, not twice.
- [ ] 7.5 **Sibling coordination** — `add-identity-brokering` carries the
      matching boundary requirement for `Keycloak-Install`.
      Confirm before either ratifies that the two
      `repo-boundary-governance` deltas are both ADDED and therefore do not
      collide.

## 8. Deferred bookkeeping over ratified text

- [x] 8.1 After BOTH install repositories exist, one change refreshes the
      `repo-boundary-governance` "Install repository scope" requirement so
      the admitted install repos are enumerated in one place — a MODIFIED
      delta restating all its scenarios, run when nothing else is
      replacing that requirement (design D8).
      **DONE 2026-08-21 by
      [`admit-install-repos-to-aggregation`](../admit-install-repos-to-aggregation/specs/repo-boundary-governance/spec.md).**
      Both preconditions held and were verified rather than assumed: both
      install repositories exist and are seeded
      (`opensoft/Keycloak-Install` at
      `1aa184e891d4ba6e641a31260d3f64d2b335f175`,
      `opensoft/OpenXPKI-Install` at
      `05f440444d9091206778e838454ed9b5bb7bff60`), and **nothing else is
      replacing that requirement** — the four active
      `repo-boundary-governance` deltas name only the two boundary
      requirements (ADDED by this change and `add-identity-brokering`,
      MODIFIED by the two `implement-*` changes), and every other
      non-archive mention of "Install repository scope" is prose. The
      refresh is ONE MODIFIED delta: both scenarios restated verbatim, the
      enumeration extended with `installs/keycloak-install` and
      `installs/openxpki-install` as admitted 2026-08-21, and an explicit
      statement that the enumeration is an index rather than a second
      boundary. Grep evidence and reasoning:
      [that change's design D-enumeration](../admit-install-repos-to-aggregation/design.md).
- [ ] 8.2 **Carried in from `split-openxwallet-repo` (archived 2026-08-28).**
      That change authored ONE `## MODIFIED Requirements` delta against
      `trust-anchor` — *Declared chain custody bounds what a certificate
      evidences* — declared relative to the OUTCOME of THIS change rather
      than against a promoted spec, because `trust-anchor` is not in
      `openspec/specs/` and the requirement is one of this change's own
      ADDED eight. It could not be applied at that change's archive:
      `openspec archive` aborts on a MODIFIED delta whose target
      capability does not yet exist (`target spec does not exist; only
      ADDED requirements are allowed for new specs`), so the delta
      travelled into the archived packet UNAPPLIED and the obligation
      falls due HERE. **At this change's promotion the ADDED text of that
      requirement MUST carry the amendment**: the composition clause reads
      "composing with the `openxwallet` capability's ratified rule,
      consumed from `opensoft/openXwallet` at the pin recorded in
      `contracts/openxwallet-pin.yaml`, that custody caps what a signature
      evidences" — because after `contract-v2.0` this corpus no longer
      holds `openxwallet` and the unamended clause is a dangling
      cross-corpus reference with no resolution path — plus ONE added
      scenario: WHEN the pinned openXwallet checkout is uninitialized or
      its custody-registry digest disagrees with the pin THEN the custody
      question is REFUSED rather than resolved. Verbatim source, including
      every scenario:
      [`../archive/2026-08-28-split-openxwallet-repo/deferred-specs/trust-anchor/spec.md`](../archive/2026-08-28-split-openxwallet-repo/deferred-specs/trust-anchor/spec.md).
      This is `release-realization`'s ordered-delta rule
      (`openspec/specs/release-realization/spec.md:64-79`) applied by
      PARITY — its letter covers a requirement already MODIFIED by an
      active ratified change and this one is ADDED — recorded rather than
      forced, exactly as that proposal's § Modified Capabilities declared.
      The realizing code already landed at P3
      (`scripts/validate-trust-anchor.py` resolving the registry from the
      pin, and rule (f) failing closed in place of the bare file-absent
      exit), so only the requirement's TEXT is outstanding.

## 9. Verification bar

- [ ] 9.1 `OPENSPEC_TELEMETRY=0 openspec validate --all --strict` green
      before commit and again at archive.
- [ ] 9.2 Repository validators and doc-health clean against this change,
      its `supporting-docs/`, and the retired INDEX row.
- [ ] 9.3 Release-realization evidence: this change declares a code
      surface, so it archives only on merged realization with green
      evidence — the validator and example corpus passing, and the bundle
      registered.
