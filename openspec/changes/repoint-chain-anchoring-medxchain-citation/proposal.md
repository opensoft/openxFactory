---
code_surface: none — this change edits only the PROVENANCE citation text inside
  three already-promoted `chain-anchoring` requirements (`openspec/specs/chain-anchoring/spec.md`);
  it adds, removes, and modifies no normative obligation, scenario, or code. No
  script, schema, or validator changes. Archives on landing (no code surface to
  realize).
target_release: none — a citation-text-only spec amendment; nothing to release
  or pin.
Status: draft
---

# Proposal: repoint-chain-anchoring-medxchain-citation

## Why

`openspec/specs/chain-anchoring/spec.md` is promoted canon. Four places across
three requirements cite the MedxChain design notes
(`ideation/brainstorm/medxchain-blockchain-medical-records.md`) as the named
source of a carried obligation, framed as **"the source is not in the tree
yet ... vendored by openxFactory pull request #509, which is IN FLIGHT at this
revision."** That framing is now doubly stale:

- Pull request #509 merged 2026-08-31, vendoring the file into openxFactory.
- Pull request #785 (merged 2026-09-08) then moved the file OUT of openxFactory
  permanently, to `MedxSoft/MedxFactory@74bed502`
  `ideation/brainstorm/medxchain-blockchain-medical-records.md` (2026-09-07
  ideation-split ruling, Q4[A]) — verified present at that path via the GitHub
  contents API at authoring time. `#785` deliberately left this spec file
  untouched: *"It is promoted canon; editing it outside an OpenSpec change
  would breach the ratification boundary ... Flagged for a future amendment"*
  (`#785`, judgement call 2; see also openxFactory issue #791).

So the citation no longer merely awaits a landing (which is what the current
text tells a reader) — it names a path that will never resolve inside this
repository again. The requirement text already anticipated an unresolvable
citation and said explicitly that *"the obligation does not depend on the
citation"* (it is provenance only, not a normative dependency), so this change
touches only that provenance framing: it repoints the citation to the note's
new, verified home and states plainly that it is cited as historical
provenance, never removing or altering any SHALL/SHALL NOT obligation, scenario,
or requirement title.

Governing issue: openxFactory #791.

## What Changes

- **MODIFIED** `chain-anchoring` requirement "Served verification and access
  decisions are logged leaves" — repoints its citation from "not in the tree
  yet / pull request #509 IN FLIGHT" to the verified MedxFactory destination,
  cited as historical provenance only.
- **MODIFIED** `chain-anchoring` requirement "The record and demographic
  planes are analyzable without the identity plane" — repoints its two
  citations (cross-plane join-key correction; meta-analysis consumer) the same
  way.
- **MODIFIED** `chain-anchoring` requirement "This capability is neutral and
  names no domain semantics" — repoints its citation (the MedxChain/HealthLinc/
  LedgerLinc domain-mapping proof) the same way.
- No requirement's SHALL/SHALL NOT text, scenario, or title changes. No code,
  schema, or validator is touched.

## Impact

- Affected spec: `chain-anchoring` (promoted, `openspec/specs/chain-anchoring/spec.md`).
- Affected code: none.
- Resolves the dead citation openxFactory #791 reports, closing the
  provenance-text gap `#785`'s judgement call 2 flagged for a future amendment.
