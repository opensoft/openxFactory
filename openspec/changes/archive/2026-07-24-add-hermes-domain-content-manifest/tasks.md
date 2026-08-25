# Tasks — add-hermes-domain-content-manifest

- [x] 1.1 `contracts/hermes-domain-overlay/content-manifest.schema.yaml` +
      example (the codexFactory conventional set declared) + negative
      fixtures (unknown kind, ambiguous location).
- [x] 1.2 `contracts/memory-gateway/memory-binding.schema.yaml` + example
      (the two LIVE-derived opensoft bindings); provider/credential-surface
      prohibition enforced by the canonical validator.
- [x] 1.3 Validator extensions: `validate-hermes-domain-overlay.py` covers a
      present content manifest (self-test 10 fixtures + real codexFactory
      repo pass); `validate-memory-gateway.py` covers the binding shape,
      vocabulary cross-checks, and the no-provider-surface rule; both green.
- [x] 1.4 Contract release: manifest.yaml entry + CHANGELOG + contract-v1.18
      allocated (v1.17 verified current) + digest inventory built (179
      entries) + annotated tag published and verified.
- [x] 1.5 README doc-index (both contract-family READMEs) + OpenSpec Records
      block updated.

## Bookkeeping correction (2026-08-23, `govern-openspec-corpus-membership`)

`proposal.md` real line 5 was respelled `Ratified by:` to `Ratified:` by slice
5B of `govern-openspec-corpus-membership` — the prefix only. Every byte after
the colon is carried verbatim, asserted identical at the edit, so the original
line is recovered exactly by reading `Ratified by:` back in its place and
nothing else on the page moved. The ruling is OQ-4's RULED extension of
2026-08-23 (Brett Heap, in-session), which widens the class to the sixteen
lines whose named change id is the DOCUMENT'S OWN. A change is not its own
approving change, and such a line passed `fam_ratified_provenance` only by
self-reference. This one emitted NO finding, so the respell is corrective
rather than a discharge and clears nothing from the census. The record that
justifies this line is the user approval of 2026-07-24 named on the line,
carried into the record by commit `6785435` of the same day, "Archive
add-hermes-domain-content-manifest (ratified 2026-07-24)". An append on a
single-valued header is mechanically impossible —
`doc_health.corpus.STATUS_RE` swallows any trailing annotation — so this is an
in-place overwrite and an extension of Brett's 2026-08-10 append ruling, named
as one, and it is entered in `docs/archive-record-discrepancies.md`.
