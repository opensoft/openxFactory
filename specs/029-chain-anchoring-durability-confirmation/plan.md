# Plan: 029-chain-anchoring-durability-confirmation

Status: draft
Kind: implementation plan

## The vertical slice, in the order it was built and committed

Each step was pushed before the next began, so a termination mid-feature loses a
step and never the feature.

1. **Shapes.** Six new schemas; eighteen shared `$defs` in
   `anchoring-definitions.schema.yaml`; the refusal enumeration widened by 48;
   the per-witness `status` enumeration REPLACED, with the migration written
   into the `$def` itself; six subjects added to
   `signed-execution-chain/digest-construction.schema.yaml` and its frozen
   `canonical.py` mirror moved with it. (`e4ee7994`)
2. **Corpus.** Fifteen new positive example files carrying three consecutive
   fixed-UTC windows, and the basis realization's sixty corpus files migrated
   uniformly onto the amended shapes with anchored digests recomputed ONLY where
   they already recomputed. (`f4689754`)
3. **Reader.** Eight new check layers, run last because every rule of this
   profile is a property of a SET; the released Merkle construction RESOLVED and
   every leaf, path and root recomputed under it; manifests reconciled against
   their own window's admissions. (`8626bacd`)
4. **Negatives.** Fifty-two single-fault fixtures — 48 closed codes plus 4
   semantic findings whose codes live outside the enumeration. (`32531421`)
5. **Tests and registration.** One test per scenario, 34 of them; six manifest
   rows with per-file digests and six moved files re-pinned. (`80c038f7`)
6. **Documentation.** The family README's migration table, the pre-publication
   measurement, and what the operator still owes in the present tense.
   (`3c266b5b`)
7. **Governance.** The amendment's realization tasks ticked with evidence, and
   this feature.

## Three design decisions worth stating, because each had a live alternative

**The Merkle tree composes under the estate's ONE digest construction.** A leaf
node is `xfc-jcs-sha256-1` over `{domain, leaf}` and an internal node over
`{domain, left, right}`, so the domain separators travel INSIDE the canonical
JSON. The alternative — raw-bytes `SHA-256(separator || child || child)` — would
have produced values that are not `xfc-jcs-sha256-1` while being tagged as such,
which is exactly the defect `digest-construction.schema.yaml`'s header names when
it forbids a second construction. Cost: the tree is not interoperable with a
generic RFC 6962 implementation, and the released profile says so by DECLARING
`leaf_encoding: xfc_jcs_sha256_1_canonical_json` rather than implying it.

**`canonical_digest`, not `content_digest`.** The amendment calls this the
"canonical content digest". This family's structural payload sweep refuses ANY
member whose NAME carries a content-bearing token, and that sweep is blind to
what the content is about on purpose. Earning an exemption for a legitimately
named digest would weaken a structural refusal to buy a spelling, so the spelling
gave way instead — noted at the `$def`.

**No leaf-grammar widening.** The amendment names five kinds of control leaf.
Every record in this family references leaves BY IDENTIFIER and defines none, so
the recursion refusal is grounded on a DECLARED `leaf_class` on the admission
rather than on a leaf discriminator. Adding five `leaf_type` members would have
pulled in `transparency-log-leaf.schema.yaml`, the tranche-one reader and its
settlement tests for no refusal this realization needs.

## Test strategy

Two modules. `test_anchoring_reader.py` adjudicates the READER and runs the full
41-positive / 126-negative self-test.
`test_durability_and_confirmation_scenarios.py` adjudicates the RATIFIED DELTA
over a MINIMAL scope — the durability subset — because the self-test already
proves the whole corpus coherent and repeating it per scenario would multiply a
quadratic cost for no further evidence. 59 tests, 138s.
