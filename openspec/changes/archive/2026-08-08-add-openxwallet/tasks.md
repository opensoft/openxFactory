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
- [x] 1.3 `OPENSPEC_TELEMETRY=0 openspec validate --all --strict` green
      before commit and again at archive.

## 2. Ratification gate

- [x] 2.1 Brett ratified proposal, design and both spec deltas on
      2026-08-07, together with the two decisions already carried (grants
      as the primitive; the core holder-class agnostic), and RULED the one
      left open: key custody is DECLARED from a closed set and CAPS the
      authority a wallet may hold — neither mandated nor unstated.
      Ratification authorizes exactly one Speckit feature and creates no
      key, credential, wallet, or runtime.

## 3. Handoff

- [x] 3.1 REALIZED by Speckit feature `006-openxwallet-contracts`
      (contract-v1.31). Opened the single Speckit feature: neutral schemas under
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
- [x] 3.2 SETTLED by the feature before the schema was authored, and
      recorded in `specs/006-openxwallet-contracts/research.md`: every
      declared component carries a `binding_mode`. A retrieval corpus is
      bound by REFERENCE — its identity and governing configuration enter
      the hash, its row-level contents do not — so swapping the corpus or
      widening retrieval revokes while ordinary corpus churn does not.
      The original framing: WHAT THE
      COMPOSITION COMPONENT SET COVERS. Including a fast-changing
      retrieval corpus fires revocation constantly and gets routed
      around; excluding it lets behaviour change without identity
      changing. The profile requires the set to be declared, which makes
      the choice visible but does not make it for anyone.

## 4. Consumers and successors

- [x] 4.1 Record the first consumer: LedgerxFactory's posting
      segregation-of-duties control needs the core's distinct-holder
      constraint plus the agent profile, and cannot be built until this
      lands. Its staged fragment cites this change.
- [x] 4.2 Name the successors as successors, each gated on a consumer of
      its own and each a NEW profile capability over the same core rather
      than a modification of it: patient profile, practitioner profile,
      certification batteries and measured drift, qualification tiers,
      delegation policy beyond monotonic attenuation.
- [x] 4.3 Record the `openxVault` boundary explicitly so it is not
      re-litigated: the vault owns custody and its gate CONSUMES these
      grants; this capability owns identity, keys and authority. Brett
      set that split 2026-07-16.

## 5. Docs and verification

- [x] 5.1 README "OpenSpec Records" entry updated for the renamed change
      and moved when it archives.
- [x] 5.2 Staging topic INDEX row and detail section updated — the topic
      folder is `agent-wallet-identity` while the change is
      `add-openxwallet`; record the relationship rather than leaving a
      reader to infer it.
- [x] 5.3 Full bar green before commit and at archive: repository
      validators, `openspec validate --all --strict`, and doc-health clean
      against the change and the topic.

## Bookkeeping correction (2026-08-23, `govern-openspec-corpus-membership`)

`proposal.md` real line 5 was respelled `Ratified by:` to `Ratified:` by slice
5B of `govern-openspec-corpus-membership` — the prefix only. Every byte after
the colon is carried verbatim, asserted identical at the edit, so the original
line is recovered exactly by reading `Ratified by:` back in its place and
nothing else on the page moved. The ruling is OQ-4 (Brett Heap, in-session,
2026-08-23): a `Ratified by:` line that names a person and a date rather than
an approving OpenSpec change is substantively the record-citing form and takes
the record-citing prefix. This line was a live CRITICAL `ratified-provenance`
finding and the respell clears it. The record that justifies this line is
Brett Heap's 2026-08-07 ruling on the one open decision, quoted on the line —
"declared and capping authority" — recorded by commit `c5b41ca` of the same
day, "Ratify add-openxwallet: custody is declared and caps authority", whose
body opens "Brett Heap ratified proposal, design and both capability deltas".
An append on a single-valued header is mechanically impossible —
`doc_health.corpus.STATUS_RE` swallows any trailing annotation — so this is an
in-place overwrite and an extension of Brett's 2026-08-10 append ruling, named
as one, and it is entered in `docs/archive-record-discrepancies.md`.
