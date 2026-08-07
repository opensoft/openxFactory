# Tasks: add-openxwallet

Governance-level only. The executable implementation list belongs to the
single Speckit feature this change hands off to; do not duplicate it here.

## 1. Spec deltas

- [x] 1.1 `openxwallet` (core) — eight ADDED requirements validate
      `--strict`: the wallet as a key reference with declared custody;
      authority as attenuated grants with monotonic narrowing; proof of
      possession rather than presentation; custody capping what a
      signature evidences; key-attributed audit; revocation propagating
      through derivation and checked at exercise; expressible
      distinct-holder constraints; and the non-substrate rule preserving
      MedxFactory's ratified wallet-neutrality.
- [x] 1.2 `openxwallet-agent-profile` — three ADDED requirements validate
      `--strict`: declared composition WITH its component set;
      declared-change revocation through the core's propagation rule; and
      agent authority as grant scope admitting `approval_policy` values.
- [ ] 1.3 `OPENSPEC_TELEMETRY=0 openspec validate --all --strict` green
      before commit and again at archive.

## 2. Ratification gate

- [ ] 2.1 Brett ratifies proposal, design and both spec deltas, together
      with the two decisions already carried (grants as the primitive;
      the core holder-class agnostic), and RULES the one still open:
      key custody DECLARED from a closed set and capping authority
      (recommended), versus mandated, versus unstated. Ratification
      authorizes exactly one Speckit feature and creates no key,
      credential, wallet, or runtime.

## 3. Handoff

- [ ] 3.1 Open the single Speckit feature: neutral schemas under
      `contracts/` for the wallet record, the custody enum with what each
      model evidences, the grant (audience, scope, expiry, parent), the
      distinct-holder constraint, and the agent profile's composition
      declaration; a validator under `scripts/`; and a fixture corpus with
      a NEGATIVE CONFIRMATION per requirement — key material in a record;
      a derived grant wider than its parent; a grant presented without
      proof of possession; a verification failure recorded as an
      unauthenticated request; authority exceeding its custody ceiling; a
      revoked parent whose derivation still exercises; a declared
      distinct-holder constraint satisfied by one holder; a wallet
      reference used as a subject identifier; a composition hash without
      its component set; and an authority term outside `approval_policy`.
- [ ] 3.2 Settle before the schema is authored, not after: WHAT THE
      COMPOSITION COMPONENT SET COVERS. Including a fast-changing
      retrieval corpus fires revocation constantly and gets routed
      around; excluding it lets behaviour change without identity
      changing. The profile requires the set to be declared, which makes
      the choice visible but does not make it for anyone.

## 4. Consumers and successors

- [ ] 4.1 Record the first consumer: LedgerxFactory's posting
      segregation-of-duties control needs the core's distinct-holder
      constraint plus the agent profile, and cannot be built until this
      lands. Its staged fragment cites this change.
- [ ] 4.2 Name the successors as successors, each gated on a consumer of
      its own and each a NEW profile capability over the same core rather
      than a modification of it: patient profile, practitioner profile,
      certification batteries and measured drift, qualification tiers,
      delegation policy beyond monotonic attenuation.
- [ ] 4.3 Record the `openxVault` boundary explicitly so it is not
      re-litigated: the vault owns custody and its gate CONSUMES these
      grants; this capability owns identity, keys and authority. Brett
      set that split 2026-07-16.

## 5. Docs and verification

- [ ] 5.1 README "OpenSpec Records" entry updated for the renamed change
      and moved when it archives.
- [ ] 5.2 Staging topic INDEX row and detail section updated — the topic
      folder is `agent-wallet-identity` while the change is
      `add-openxwallet`; record the relationship rather than leaving a
      reader to infer it.
- [ ] 5.3 Full bar green before commit and at archive: repository
      validators, `openspec validate --all --strict`, and doc-health clean
      against the change and the topic.
