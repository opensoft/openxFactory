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

- [x] 2.1 DONE 2026-08-21 — all three sites amended (Impact split into the tenant-owned image-custody surface and the xFactory-OpenXPKI-Install topology home; What-Changes bullet 3 re-pointed; tasks gained a 3.4 migration obligation, since the change's QA tasks were already executed with the manifests authored in Opensoft-Tenant during bring-up — the amendment records that location as transitional, not governed). In the OpsxFactory repo, amend the active change
      `add-openxpki-qa-image-pipeline` in three places that today home the
      QA deployment manifests in `opensoft/Opensoft-Tenant`: its **Impact**
      section, its **"What Changes" bullet 3**, and its **tasks §3**.
      Re-point the deployment-manifest scope to
      `xFactory-OpenXPKI-Install`; leave the image-custody scope (build,
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

## 4. Settle before the schema is authored

Both items are contract content, not implementation detail, and both are
cheap now and expensive after a bundle ships.

- [ ] 4.1 OQ2 — the custody enumeration and what each member EVIDENCES,
      settled with the `client-credential-escrow-registry` topic in the
      room. Carry the `openxwallet` lesson: a set that fails to distinguish
      a key readable by its own host from one isolated from it lets the
      first claim the second's authority.
- [ ] 4.2 OQ1 — the declared floor for issuance evidence (per-certificate
      record where the authority exposes it; per-policy attestation plus
      the authority's own log as the declared floor where it does not), and
      the shape of the conformance declaration that carries the difference.

## 5. Contract realization (one Speckit feature)

- [ ] 5.1 NEW `contracts/trust-anchor/trust-anchor.schema.yaml`
      (`schema_version`, `kind`): anchor identity, chain position, validity
      window, admitted issuance authorities, declared custody. Key
      material is unrepresentable by shape.
- [ ] 5.2 NEW `contracts/trust-anchor/certificate-record.schema.yaml`:
      anchor reference, subject, validity, declared chain custody, derived
      `evidences`, and the dependent-binding set (§5.4).
- [ ] 5.3 NEW `contracts/trust-anchor/issuance-evidence.schema.yaml`:
      anchor, admitted authority reference, request provenance, time, and
      the establishment level actually achieved (per §4.2).
- [ ] 5.4 NEW `contracts/trust-anchor/dependent-binding.schema.yaml`: the
      system holding the binding, what it binds, the key material
      referenced, and rebind status — the record that makes the rebind set
      computable before a renewal (design D4).
- [ ] 5.5 NEW `contracts/trust-anchor/renewal-record.schema.yaml`: whether
      key material changed, the enumerated dependents, per-dependent
      rebind evidence, and a completion state that cannot read
      "successful" with an unevidenced dependent.
- [ ] 5.6 NEW `contracts/trust-anchor/revocation-propagation.schema.yaml`:
      what was revoked, the declared bounded window, the downstream
      authority reached, propagation evidence, and the
      escalated-open-exposure state for a window that closed unevidenced.
- [ ] 5.7 NEW
      `contracts/trust-anchor/conformance-declaration.schema.yaml`: per
      obligation — satisfied / partial / cannot, with a reason — the
      artifact D6 depends on.
- [ ] 5.8 Packaged positive examples plus a NEGATIVE CONFIRMATION per
      requirement: key material in an anchor record; a certificate trusted
      with no held anchor; issuance with no admitted authority; asserted
      provenance the authority cannot establish; a host-held certificate
      claiming hardware-bound assurance; a renewal reported successful with
      an unevidenced dependent; a renewal planned against an incomplete
      dependent set; a revocation window closed with no propagation
      evidence; authority key material in a repository (including a
      reversible encoding) with "QA only" as the reason; and an
      undeclared unsatisfied obligation.
- [ ] 5.9 NEW canonical `scripts/validate-trust-anchor.py`, wired into the
      repository validator bar, green on the whole example corpus.
- [ ] 5.10 Register the family in `contracts/manifest.yaml` and
      `contracts/CHANGELOG.md` at the next additive bundle cut, allocating
      the version per `docs/contract-versioning-policy.md`. Consumers pin
      the released bundle rather than copying a shape.

## 6. Promotion bookkeeping

- [ ] 6.1 Move the staged topic fragment
      `ideation/staging/pki-trust-anchor-plane/pki-trust-anchor-plane.md`
      into this change's `supporting-docs/`, preserving its `Status:`
      header per `document-lifecycle`.
- [ ] 6.2 Retire the `pki-trust-anchor-plane` row in
      `ideation/staging/INDEX.md` and update its detail section to record
      the exit — including the one deliberate divergence from the topic
      (R1's MODIFIED enumeration became an ADDED requirement; design D8),
      so a reader is not left to infer it.
- [ ] 6.3 List this change in the openxFactory README "OpenSpec Records"
      block, and move the entry when it archives.
- [ ] 6.4 Note the shared-topic relationship: the topic folder is
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
- [ ] 7.2 **`xFactory-OpenXPKI-Install` creation** — the named successor
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
      matching boundary requirement for `xFactory-Keycloak-Install`.
      Confirm before either ratifies that the two
      `repo-boundary-governance` deltas are both ADDED and therefore do not
      collide.

## 8. Deferred bookkeeping over ratified text

- [ ] 8.1 After BOTH install repositories exist, one change refreshes the
      `repo-boundary-governance` "Install repository scope" requirement so
      the admitted install repos are enumerated in one place — a MODIFIED
      delta restating all its scenarios, run when nothing else is
      replacing that requirement (design D8).

## 9. Verification bar

- [ ] 9.1 `OPENSPEC_TELEMETRY=0 openspec validate --all --strict` green
      before commit and again at archive.
- [ ] 9.2 Repository validators and doc-health clean against this change,
      its `supporting-docs/`, and the retired INDEX row.
- [ ] 9.3 Release-realization evidence: this change declares a code
      surface, so it archives only on merged realization with green
      evidence — the validator and example corpus passing, and the bundle
      registered.
