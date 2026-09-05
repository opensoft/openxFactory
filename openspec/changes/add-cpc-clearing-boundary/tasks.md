# Tasks: add-cpc-clearing-boundary

Status: draft
Proposed: 2026-09-01

Section 1 is THIS change. Section 2 is the neutral artifact realization that
follows ratification in THIS repository. Sections 3–5 are DEPENDENT
REALIZATIONS owned by other repositories, listed so sequencing and ownership are
agreed here and NOT executed by this change. Section 6 closes the lane.

**ORDERING.** This packet's `## MODIFIED Requirements` block is written over an
active sibling's addition, so it archives AFTER `add-clearing-dispatch-boundary`
archives, per `release-realization` and the `Modified over` marker this delta
carries.

## 1. Contract (openxFactory — THIS CHANGE)

- [x] 1.1 `proposal.md` — the extension delta, its standing beside the ratified
      basis, and an impact map naming every dependent realization. Front matter
      declares `code_surface:` and `target_release:`, and records the ordering
      obligation.
- [x] 1.2 `design.md` — D1 … D11 with the alternatives rejected, including D11's
      record of a requirement deliberately NOT written because the basis already
      carries it. OQ1 and OQ3 open; OQ2 resolved to REFERENCE.
- [x] 1.3 `specs/clearing-dispatch-boundary/spec.md` — THREE MODIFIED
      requirements carried VERBATIM from the ratified basis with additions marked
      in place and every original scenario retained (177 basis units, none lost),
      EACH carrying its OWN `Modified over` marker IN ITS REQUIREMENT BODY —
      per requirement, never per section, a section-level paragraph leaving every
      requirement in the block declaring nothing — naming
      `add-clearing-dispatch-boundary` as basis with the nonempty reason tail the
      form requires. The third MODIFIED block is the basis's dispatch-record and
      single-door attestation requirement, widened by ONE FIELD in what the
      attestation reads (§ 1.11). Plus THREE ADDED requirements the basis has no
      counterpart to: sign-on-return, inbound re-seal of the return, and
      workspace-disposal evidence.
- [x] 1.4 `specs/factory-origin-identity/spec.md` — six ADDED requirements: one
      registered Ed25519 identity per originating repository in the sibling
      register with `holder_class: organisation` and no seat spelling; public key
      references only; hosted-environment custody with the unattested cap; the
      checked disjointness rule with the read-time refusal declared not in force;
      the register's own staleness bound with at-clearing revocation declared
      unrealizable; and the human-only surface with the exact-set floor
      obligation.
- [x] 1.5 `.openspec.yaml` — ad-hoc origin recording the ruling, the extension,
      and a duplicate check run against ACTIVE CHANGES AND RECENT RATIFICATIONS
      rather than the promoted specs alone.
- [x] 1.6 README "OpenSpec Records" — Active-changes entry.
- [x] 1.7 `openspec validate add-cpc-clearing-boundary --strict` and
      `--all --strict` green; `proposal-support.py . verify` ok; doc-health
      families green.
- [x] 1.9 **Known transient doc-health condition, cited rather than waived.**
      `modified-block-currency` emits THREE `warning`-severity, `contested`-class
      findings against this delta: the MODIFIED blocks "resolve to no promoted
      requirement, no rename of its own, and no active sibling's addition —
      capability `clearing-dispatch-boundary` has no promoted spec at all". That
      is CORRECT and expected: the basis is `add-clearing-dispatch-boundary`,
      which is RATIFIED but UNMERGED (PR #555), so its `## ADDED Requirements`
      block is not in this tree for the pairing arm to resolve against. The
      condition cleared: #555 merged 2026-09-02, and the `Modified over`
      marker this delta already carries is what the arm reads. No `error` or
      `critical` finding is emitted and `--fail-on error` is green. Recorded here
      as the cited change rather than dispositioned away.
- [x] 1.11 **The attestation extension is DECLARED, not implicit.** The ADDED
      workspace-disposal requirement makes disposal evidence a field of the
      dispatch record and then has the periodic attestation read it — an
      extension of a ratified requirement written from outside it, which is the
      undeclared coupling `govern-sibling-added-modified-deltas` exists to catch.
      The basis's attestation requirement therefore carries its own MODIFIED
      block with its own marker (design D14), adding one field to what the
      attestation READS and nothing to what it AUTHORIZES.
- [ ] 1.10 **MERGE ORDER, AND THE DISPOSITION ROWS THAT COVER IT.**
      `add-clearing-dispatch-boundary` (#555) MERGED 2026-09-02, FIRST as required. If this packet
      merged first, its three contested `modified-block-currency` warnings would
      enter the nightly baseline, and #555 landing would resolve them — a
      contested finding vanishing without a citation, which `report.py`'s
      uncited-resolution rule re-emits as three ERRORs. Prose in § 1.9 is NOT a
      recorded disposition: the matcher keys on `(family, repo, path)` in
      `health/dispositions.yaml`. **That file lives at the AGGREGATION ROOT and
      is tracked in the `opensoft/xFactory` aggregation repo, not here**, so the
      three rows are a cross-repo act that cannot land in this PR: family
      `modified-block-currency`, repo `openxFactory`, path
      `openspec/changes/add-cpc-clearing-boundary/specs/clearing-dispatch-boundary/spec.md`,
      one per MODIFIED requirement title, each citing `add-clearing-dispatch-boundary`
      as the resolving change. Tracked as the aggregation-side task in § 5.3.
- [x] 1.8 **DONE 2026-09-02** — Brett ratified, in-session, on the recorded
      word *"Ratify + merge openxFactory #560"* (ratified head `33fa2b54`;
      record `review/ratification-2026-09-02.md`). Ratification: operator
      decision on the re-scoped packet, on D2/D4/D8/D9/D10/D11, and on the
      OQ1/OQ3 dispositions.

## 2. Neutral artifacts (openxFactory — after ratification, NOT authored here)

- [ ] 2.1 NEW `governance/factory-identity/register.yaml` — `register_version`,
      its OWN declared revocation staleness bound and ceiling, and `rows`
      carrying holder reference, wallet reference, act, grant reference, expiry,
      and state — the six the spec's row enumeration names, and no `authority
      tier` field, the authority cap being a property of the grant and its
      custody attestation rather than a column of the register. Deliberately kindless per D3; record D3's
      rule-of-three trigger in the file header.
- [ ] 2.2 NEW `governance/factory-identity/wallets/<wallet>.yaml` — the wallet
      record for the first origin identity (`schema_version` + `kind` from the
      pinned neutral vocabulary), `holder_class: organisation`, Ed25519 public
      key with its `did` and `key_id`, declared custody model, state. NO
      seat-key block and no agent-holder prefix (D2). No private key material.
- [ ] 2.3 NEW `governance/factory-identity/grants/<grant>.yaml` — the grant
      conferring the ORIGIN act, naming `issued_by` as the accountable human,
      its scope, the tier the custody attestation licenses, and an expiry.
- [ ] 2.4 NEW `governance/factory-identity/attestations/<attestation>.yaml` —
      the custody attestation for hosted-environment custody, naming the
      verifier, the basis, and the cap applying in its absence.
- [ ] 2.5 The DISJOINTNESS VALIDATOR: assert that no `key_id`, `did`, or
      public-key fingerprint appears in both the factory-identity and
      review-authority record trees; fail naming the shared value; not waivable
      by declaring different acts. This is the enforceable half of act
      distinctness (D8) and ships with the register, not after it.
- [ ] 2.6 Wire the factory-identity register READER into the REQUIRED
      wallet-validation check with a POSITIVE log conjunction — a green check
      that never opened the register must be impossible.
- [ ] 2.7 Enter `governance/factory-identity/` into the never-clearable floor BY
      NAME. **Cross-repo, same governed act:** codexFactory's
      `scripts/merge_master/openxfactory-review-authority-floor.yaml` is compared
      as an EXACT SET, so it must be updated in the same act — an exact-set
      comparison against a floor that does not name the new register fails closed
      on every candidate.
- [ ] 2.9 **Tranche-3 `digest_subject` widening (blocks the origin signature).**
      `contracts/signed-execution-chain/digest-construction.schema.yaml` closes
      `digest_subject` at seventeen members and none of them is a request,
      return, or bundle manifest, so an origin signature over the manifest has
      no admitted subject today. Widen the enumeration with the manifest
      subjects this contract needs — the sealed bounded request manifest and the
      sealed return — as a TRANCHE ADDITION OF SUBJECTS, never a second
      construction, which is the one way that file is meant to move and what its
      own header says. Until it lands, the spec reports the requirement
      unrealizable rather than satisfied. NOT a task of this change; named here
      because the realization cannot proceed without it.
- [ ] 2.10 Confirm the byte-hash carve-out needs no contract change: per-file
      content hashes are plain algorithm-tagged SHA-256 over file bytes and use
      no canonical-JSON construction, so nothing under
      `contracts/signed-execution-chain/` moves for them.
- [ ] 2.8 Confirm no `contracts/` artifact moves: OQ2 is resolved to REFERENCE,
      no manifest schema is added, no bundle is cut, no digest set moves.

## 3. Dependent realization — the clearing lane (xFactory, its own change)

- [ ] 3.1 Origin-signature verification in the live clearing workflow, against
      the register projection, CONJUNCTIVE with the provider checks and reported
      as its own dispatch-record outcome — never folded into the provider-verified
      set.
- [ ] 3.2 Field (10) enforced as a required signature for a registered
      originator, and unchanged for an unregistered one.
- [ ] 3.3 The operation's class constraints, worker profile, lanes, and output
      schema RESOLVED FROM the permitted-operations register entry; the bundle's
      copies compared as claims; disagreement refuses and is recorded.
- [ ] 3.4 Workspace disposal evidence written as a field of the dispatch record
      on every terminal state, and read by the periodic attestation.
- [ ] 3.5 Register-view staleness enforced: a view older than the declared bound,
      unreadable, or absent refuses, with unreachable diagnosed distinctly from
      absent.

## 4. Dependent realization — packaging and sign-on-return (codexFactory, its own change)

- [ ] 4.1 The HOSTED packaging workflow signs the manifest with the origin key
      held in that hosted environment, over all ten declared fields including the
      per-file hashes, using the digest construction already in force.
- [ ] 4.2 The origin key provisioned into that hosted environment only, custody
      declaration and attestation matching task 2.4.
- [ ] 4.3 The HOSTED sign-on-return workflow verifies the sealed return's digest
      and provenance against the dispatch record BEFORE signing, using the
      existing seat signing keys where they already live — no re-mint, no
      relocation, nothing signed on an unverified return.
- [ ] 4.4 The codexFactory floor-file exact-set update of task 2.7, landed in the
      same governed act as the register.
- [ ] 4.5 A GOVERNED REGISTER CHANGE adding a `deliberation` operation to the
      closed permitted-operations register — with its class constraints, worker
      profile, lanes, output schema, and repository-affecting-output declaration.
      It does not exist today; draft PR #165 (`adopt-bundle-shaped-deliberation`)
      depends on it, and its OQ-A is closed by the ruling in favour of the
      clearing repository as the single door.
- [ ] 4.6 Retirement of the codexFactory worker jobs that reached the host
      directly — unclaimable by design — retired with the clearing slice, each
      routed through the basis's retire-the-old-route requirement.

## 5. Dependent realization — the reader scoping (openXwallet, its own change)

- [ ] 5.1 Scope the review-authority reader's wallet and grant resolution to its
      OWN register, so a wallet record in a sibling tree is not resolvable as a
      review row's `wallet_ref` (OQ3, D8's fail-open direction).
- [ ] 5.2 Only when 5.1 lands may the read-time refusal be described as in force;
      until then the disjointness rule of task 2.5 is the whole enforcement, and
      documents saying otherwise are refused by the spec's own scenario.

- [ ] 5.3 **xFactory aggregation repo** — add the three
      `modified-block-currency` disposition rows described in § 1.10 to
      `health/dispositions.yaml`, citing `add-clearing-dispatch-boundary`.
      Landed before or with this packet's merge, never after.

## 6. Records and acceptance

- [ ] 6.1 Keep the README entry current through ratification, realization, and
      archive.
- [ ] 6.2 Archive ONLY after `add-clearing-dispatch-boundary` archives, and only
      on merged-plus-green realization evidence per `release-realization`.
- [ ] 6.3 Acceptance: a sealed bounded request from a REGISTERED originator
      clears with the origin signature verified as its own outcome beside the
      provider checks, runs an operation whose constraints came from the register
      rather than from the bundle, returns a result validated by the hosted
      finalizer and attested on the originating repository's hosted
      infrastructure, and leaves a dispatch record carrying disposal evidence.

## Archive-ordering note (2026-09-05)

Under `@fission-ai/openspec@1.12.0`, `openspec archive` would REFUSE this
change's `clearing-dispatch-boundary` delta: the TARGET SPEC DOES NOT EXIST,
and only `ADDED` requirements are permitted for a new spec. **This is an
ordering dependency, not a wrong delta shape.** `add-clearing-dispatch-boundary`
CREATES that spec and is still ACTIVE and unarchived; it archives FIRST, and
the refusal ends there. The control that proves the shape is
`admit-deliberation-clearing-operation`, which targets the SAME absent spec
and validates clean, because its block is `## ADDED Requirements` — so the
refusal is about MODIFIED-before-creation and nothing else.

Recorded by `prepare-openspec-1.12-readiness`, which measured this corpus
under `@fission-ai/openspec@1.12.0` while the fleet pin stays at `1.2.0`
(#667). **NOTHING IN THIS PACKET WAS CHANGED:** the delta is correct as
written, the finding is `[INFO]` rather than a validation failure, and the
remedy is archive ORDER, which no other packet may take on this one's behalf.
**A `sequenced_after:` declaration is OWED here and was deliberately not
added** — that would edit this ratified proposal's front matter from outside,
and `add-sequenced-after-substrate`, which builds the validator that reads the
field, is itself still active and unrealized.
