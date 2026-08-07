# Tasks: add-agent-wallet-identity

Governance-level only. The executable implementation list belongs to the
single Speckit feature this change hands off to; do not duplicate it here.

## 1. Spec delta

- [x] 1.1 Six ADDED requirements validate `--strict`: the governed identity
      record; proof of control (an asserted identifier is never identity);
      custody declared and capping authority; authority reusing the
      `approval_policy` vocabulary; declared-change decertification; and
      the non-substrate rule preserving MedxFactory's ratified
      wallet-neutrality.
- [ ] 1.2 `OPENSPEC_TELEMETRY=0 openspec validate --all --strict` green
      before commit and again at archive.

## 2. Ratification gate

- [ ] 2.1 Brett ratifies proposal, design and spec delta TOGETHER WITH the
      two recorded decisions, or corrects them:
      (a) proof of control REQUIRED at the neutral level, with any interim
      recorded as a dated exception in the consuming domain;
      (b) key custody DECLARED from a closed set and capping the authority
      an identity may hold, rather than mandated or unstated.
      Ratification authorizes exactly one Speckit feature and creates no
      key, credential, wallet, or runtime.

## 3. Handoff

- [ ] 3.1 Open the single Speckit feature: neutral schemas under
      `contracts/` (agent identity record, custody enum with what each
      model evidences, authority binding, decertification trigger), a
      validator under `scripts/`, and a fixture corpus with a NEGATIVE
      CONFIRMATION per requirement — an asserted identifier without proof;
      a signature that fails verification recorded distinctly from an
      unidentified request; authority exceeding its custody ceiling; an
      authority value outside `approval_policy`; a composition change that
      does not revoke; and a wallet reference used as a subject
      identifier.
- [ ] 3.2 Settle before the schema is authored, not after: WHAT THE
      COMPOSITION HASH COVERS. A hash including a fast-changing retrieval
      corpus fires revocation constantly and will be routed around; a hash
      excluding it lets behaviour change without identity changing. This is
      staging open question 3 and it is load-bearing for the schema.

## 4. Consumers and successors

- [ ] 4.1 Record the first consumer explicitly: LedgerxFactory's posting
      segregation-of-duties control cannot be built until this lands, and
      its staged fragment cites this change.
- [ ] 4.2 Name the successors as successors, each gated on a consumer of
      its own — certification batteries and measured drift; qualification
      levels and autonomous-authority tiers; delegation chains; patient
      and practitioner wallets. None is scheduled by this change.
- [ ] 4.3 Omnigent-install composition-hash attestation is a named
      successor in that repository, not part of this change: heartbeats
      already attest `worker_version`, `profile_versions` and
      `policy_version`.

## 5. Docs and verification

- [ ] 5.1 README "OpenSpec Records" active-changes entry added at proposal
      and moved when this archives.
- [ ] 5.2 Staging topic `agent-wallet-identity` INDEX row updated to
      proposed, per the staging maintenance rule.
- [ ] 5.3 Full bar green before commit and at archive: repository
      validators plus `openspec validate --all --strict`.
