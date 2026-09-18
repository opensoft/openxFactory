# Proposal Ratification: repromote-engineering-vocabulary

Status: ratified
Decision date: 2026-09-18
Ratifier: Brett Heap (openxFactory operator authority) — in-session, by INTERACTIVE
MULTI-CHOICE over four questions, the recommended option taken each time
Ratified: 2026-09-18 by Brett Heap — recorded at openxFactory issue #656, comment
[`5728607038`](https://github.com/opensoft/openxFactory/issues/656#issuecomment-5728607038),
ruling **R-A**; record: this file
Ratified baseline: the LANDED filing, openxFactory PR
[#1071](https://github.com/opensoft/openxFactory/pull/1071) →
`e83f8cd77159c414177068cc11dc38f896541aad`, 2026-09-17T14:43:45Z — the packet
exactly as it stands, with no amendment at ratification

## Decision

**RATIFY.** § 5.2a's successor capability and the fifteen carried into it stand as
filed. R-A, verbatim:

> **R-A. § 5.2a — `repromote-engineering-vocabulary` is RATIFIED** (filed by #1071
> → `e83f8cd7`; `code_surface: none`, `target_release: implemented`, so it
> archives on landing with no build). Its archive PR is prepared now and lands in
> a Rule 6 window AFTER #1066 (§ 6.5 still edits
> `openspec/specs/ideation-dashboard/spec.md` content). § 5.2a ticks in amendment
> #6 on this word.

**THE WORD IS NOT A BARE "ratify", AND THE FORM IS RECORDED RATHER THAN SMOOTHED
OVER.** It was given as the recommended option of a multi-choice question put with
three others; the same ruling's R-B, R-C and R-D settle § 5.6 (arc F, the
codexFactory de-floor) and belong to that box, not to this packet. What this
record claims is R-A and nothing beside it.

## The two judgments this packet declared, and how they were answered

`tasks.md` § 1.4 and § 1.5 refused to resolve two judgments silently and put both
to the ratifier. Both were carried into the word in the LANDED-and-gate comment
[`5716296239`](https://github.com/opensoft/openxFactory/issues/656#issuecomment-5716296239),
verbatim: *"Two judgments for Brett Heap at RATIFICATION, declared in the packet
rather than resolved silently: (1) no second `## REMOVED` block on
`ideation-dashboard` — the split packet's ratified map is the removal's single
writer; (2) `repromote-engineering-vocabulary` ARCHIVES BEFORE the split packet,
so the fifteen are never in no capability at all."*

R-A ratifies the packet **carrying both**, so both are ACCEPTED as filed:

1. **§ D3 — no second `## REMOVED Requirements` block on `ideation-dashboard`.**
   The removal keeps its single ratified writer, the split packet's
   per-requirement map. Mechanically corroborated at the archive: see below.
2. **§ D4 — this packet archives BEFORE `split-opendox-two-layer-product`.**
   Re-promotion first; the fifteen are never in no capability at all.

## What ratification authorizes, and what it does not

**It authorizes the archive, and the archive is the whole of the remaining act.**
`code_surface: none` and `target_release: implemented` are the doc-only pair
`release-realization` names, so there is nothing to build, no merged-plus-green
realization evidence to wait for, no contract bundle cut and no number allocated.
No byte of `contracts/`, `scripts/` or `tests/` (other than the machine-seeded
sweep-ledger row every filing owes) moves with it.

**It does not tick § 5.2a.** That tick rides the packet bookkeeper's own
`tasks.md` amendment #6, on R-A's own words — `tasks.md` § 4.1, unchanged.

## The archive-time proof of § D3, taken rather than asserted

Run on a throwaway copy of `openspec/` at main `9c817545` with the pinned OpenSpec
CLI **1.12.0**, a sha256 manifest of `openspec/specs/` taken before and after. The
CLI's own output:

```
Specs to update:
  openxfactory-engineering-adapter: create
Applying changes to openspec/specs/openxfactory-engineering-adapter/spec.md:
  + 15 added
Totals: + 15, ~ 0, - 0, → 0
```

`- 0` — zero removals, stated by the tool. The manifest diff across all of
`openspec/specs/` is ONE added line, `openxfactory-engineering-adapter/spec.md`;
capability directories go **62 → 63**; and
`openspec/specs/ideation-dashboard/spec.md` carries sha256
`e7e86bf0dcd22ad373c8ea8c7f1448eea7a2a4068650c0202b3c26829d092f6c` **before and
after**, unchanged to the byte. That is `tasks.md` § 2.9's predicted check and
`design.md` § D3's claim, discharged mechanically.

## Carry fidelity at the ratified baseline

`review/build-delta.py` re-run from the ACTIVE path against main `9c817545`
(`tasks.md` § 3.3, deliberately BEFORE the move): **CHECK PASSED** — fifteen
requirements, 84 scenarios, 49,829 source bytes lifted, delta **53,118 bytes,
sha256 `c3b985aedb7cc9be…`**, byte-identical to the committed delta, with the
reversal proof asserting every byte outside the two declared `resolve` edits is
carried identical. The promoted text of the fifteen has not moved since filing.

## Provenance

`.openspec.yaml` gains `approved_by` / `approved_on` as a pure ADDITION beside an
unmoved `kind`, `id` and drafting pair — the shape `add-drafted-proposal-origin`
(issue #318) defined for this transition.
