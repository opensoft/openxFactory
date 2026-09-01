# Tasks: add-cpc-clearing-boundary

Status: draft
Proposed: 2026-09-01

Section 1 is THIS change — the neutral contract, authored and validated here.
Section 2 is the neutral artifact realization that follows ratification in THIS
repository. Sections 3–5 are DEPENDENT REALIZATIONS owned by other
repositories; they are listed so the sequencing, the ownership, and the exit
criteria are agreed here, and they are NOT executed by this change. Section 6
is the acceptance that closes the lane and spans them.

## 1. Contract (openxFactory — THIS CHANGE)

- [x] 1.1 `proposal.md` — why the refused shape fails, what the two new
      capabilities say, the impact map naming every dependent realization, and
      front-matter declaring `code_surface:` and `target_release:` per
      `release-realization`.
- [x] 1.2 `design.md` — decisions D1–D8 with the alternatives that were
      rejected, and open questions OQ1–OQ3 recorded as open rather than
      guessed. D1 is the register-home decision and carries its five grounds.
- [x] 1.3 `specs/clearing-boundary/spec.md` — eleven ADDED requirements: single
      admission point; the enumerated manifest; verification against platform
      truth rather than bundle contents; single-use, expiring, label-bound
      dispatch; the short-lived sealed job object; execution-target isolation
      with digest recomputation; hosted output-schema validation before any
      repository is touched; proven workspace wipe; sign-on-return attestation;
      audited decisions with one throttle and shutdown point; readiness as the
      lane's first operation with convergence to one authorization entry per
      execution group.
- [x] 1.4 `specs/factory-origin-identity/spec.md` — seven ADDED requirements:
      one registered Ed25519 origin identity per factory in a SIBLING register;
      public key references only; hosted-environment custody declared and
      attested; origin and review/seat acts distinct with refusal in both
      directions; revocation under the ratified lifecycle re-checked at
      clearing; conjunctive signature-plus-platform verification; the register
      as a permanently human-only surface entered into gate floors by name.
- [x] 1.5 README "OpenSpec Records" — Active-changes entry for this change.
- [x] 1.6 `OPENSPEC_TELEMETRY=0 openspec validate add-cpc-clearing-boundary
      --strict` and `--all --strict` green before commit.
- [ ] 1.7 Ratification: operator decision on the proposal, on D1 (sibling
      register) and on the OQ1/OQ2/OQ3 dispositions. Record the ruling in the
      front matter and flip `Status:`.

## 2. Neutral artifacts (openxFactory — after ratification, NOT authored here)

- [ ] 2.1 NEW `governance/factory-identity/register.yaml` — `register_version`,
      a declared `revocation_staleness_bound`, and `rows` carrying holder
      reference, wallet reference, act, authority tier, grant reference,
      expiry, and state. Deliberately kindless per design D2, mirroring the
      review-authority intake register; the reader is the shape. Record D2's
      rule-of-three trigger in the file header so the next register author
      finds it.
- [ ] 2.2 NEW `governance/factory-identity/wallets/<wallet>.yaml` — the wallet
      record for the first factory origin identity (`schema_version` + `kind`
      from the pinned neutral wallet vocabulary): holder, key reference with
      the Ed25519 public key and its algorithm, declared custody model, state.
      No private key material, no secret name resolvable to key material.
- [ ] 2.3 NEW `governance/factory-identity/grants/<grant>.yaml` — the grant
      conferring the ORIGIN act on that wallet (`schema_version` + `kind`),
      naming `issued_by` as the accountable human, its scope acts and objects,
      the authority tier the custody attestation licenses, and an expiry.
- [ ] 2.4 NEW `governance/factory-identity/attestations/<attestation>.yaml` —
      the custody attestation for the origin key's hosted-environment custody,
      naming the verifier, the verification basis, and the cap that applies in
      its absence.
- [ ] 2.5 Wire the factory-identity register READER into the REQUIRED
      wallet-validation check, with a POSITIVE log conjunction asserting the
      register was actually opened and its row count read — a green check that
      never opened the register must be impossible, exactly as the intake
      register's gate already asserts.
- [ ] 2.6 Enter `governance/factory-identity/` into the never-clearable gate
      floor BY NAME (not by path pattern), so no autonomous or council-cleared
      approval can land a change to the register or the records beside it.
- [ ] 2.7 Resolve OQ2 and act on it: either add a
      `contracts/clearing-boundary/` sealed-bounded-request manifest schema
      with packaged positive and negative examples and its canonical
      validator, registered in `contracts/manifest.yaml` and
      `contracts/CHANGELOG.md` at the next additive bundle cut, or record the
      decision that the manifest is referenced from the neutral job envelope
      rather than schema'd here.
- [ ] 2.8 Resolve OQ3 and act on it: make the review-authority reader refuse a
      key registered for the origin act, by whichever of the three routes the
      ruling picks (pinned-vocabulary change, consumer-side check beside the
      reader invocation, or a validator rule asserting the two registers share
      no key).
- [ ] 2.9 Resolve OQ1 and act on it: the projection path by which the
      factory-identity register reaches a clearing workflow, with the staleness
      bound it honours and the fail-closed behaviour on a stale, unreadable, or
      absent projection.

## 3. Dependent realization — the clearing lane (xFactory, its own change)

Not this change's surface. Exit criteria for the slice:

- [ ] 3.1 A clearing workflow that accepts a sealed bounded request, verifies
      every enumerated manifest field against the hosting platform's
      authoritative API, verifies the origin signature against the register
      projection, and refuses on any single failure — with the refusal audited.
- [ ] 3.2 Single-use, expiring, label-bound dispatch: a job id that clears
      once, an expired request refused, and the dispatch bound to its unique
      dispatch label so exactly one execution target can claim it.
- [ ] 3.3 The sealed bundle carried as a short-lived sealed job object; no
      committed folder of copied data anywhere in the path.
- [ ] 3.4 The execution-target side: stage the bundle only, no clone and no
      credential, recompute the bundle digest and every per-file hash before
      execution, confine execution to the permitted operation, and prove the
      workspace wipe on every terminal state including failure and timeout.
- [ ] 3.5 The hosted finalizer: validate the sealed return against the declared
      output schema and run the operation's required tests before anything may
      affect a repository.
- [ ] 3.6 Readiness expressed as the clearing lane's FIRST operation, and the
      standalone read-only dual-lane runner readiness diagnostic (xFactory
      PR #188) retired into it rather than kept alongside.
- [ ] 3.7 Authorization convergence: ONE permanent entry per execution group —
      the clearing workflow — added by the operator once, when this slice
      lands. No per-path additions.
- [ ] 3.8 Audit, rate limiting, and an emergency stop exercised at the boundary,
      demonstrated: halting the clearing workflow halts all cross-boundary
      execution in the estate.

## 4. Dependent realization — packaging and sign-on-return (codexFactory, its own change)

Not this change's surface. Exit criteria for the slice:

- [ ] 4.1 A HOSTED packaging workflow that selects source files, computes
      per-file hashes and the bundle digest, builds the enumerated manifest,
      and signs it with the factory origin key held in that hosted
      environment — no repository credential and no key of any other kind in
      the bundle.
- [ ] 4.2 The origin key provisioned into that hosted environment only, with
      its custody declaration and attestation matching what task 2.4 records.
- [ ] 4.3 A HOSTED sign-on-return workflow that verifies the sealed return's
      provenance and digest FIRST and only then signs the results, using the
      existing seat signing keys where they already live — no re-mint, no key
      relocation, and nothing signed on an unverified return.
- [ ] 4.4 Completion proceeds through the factory's normal reusable completion
      path once results are attested.
- [ ] 4.5 codexFactory draft PR #165 (`adopt-bundle-shaped-deliberation`)
      revised to DEPEND on this change: its bundle shape conforms to the
      manifest this contract enumerates rather than declaring its own, and its
      OQ-A is closed by the ruling in favour of the estate's clearing boundary.

## 5. Dependent realization — retirements (codexFactory + estate, their own changes)

Not this change's surface. Exit criteria:

- [ ] 5.1 The codexFactory worker jobs that reached the execution surface
      directly — unclaimable by design under the ruling — retired with the
      clearing slice, not before it and not left dormant after it.
- [ ] 5.2 Any remaining direct-origination path removed; if a narrow direct
      path is ever granted, it is ONE exact workflow path on a protected
      branch, recorded as its own governed decision.
- [ ] 5.3 The superseded per-path readiness approach removed from all live
      documents, with the supersession recorded rather than silently dropped.

## 6. Records and acceptance

- [ ] 6.1 Keep the README "OpenSpec Records" entry current through
      ratification, realization, and archive; the row moves from Active to
      Archived changes in the same act as archiving.
- [ ] 6.2 Record the ruling of 2026-09-01 and its extension as this change's
      origin in the archived packet, so the incident stays findable from the
      contract.
- [ ] 6.3 Acceptance: one sealed bounded request originates in a factory,
      clears at the boundary with both verifications passing, executes a
      permitted operation on an execution target that never saw a repository
      or a credential, returns a result that validates on hosted infrastructure
      and is attested on the factory's hosted infrastructure — and the
      execution group's authorization list shows exactly one permanent entry
      throughout.
- [ ] 6.4 Archive only on merged-plus-green realization evidence for the
      declared code surface, per `release-realization`.
