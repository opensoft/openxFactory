# openXdox — Capability Naming Record

Status: draft
Kind: reference
Repository context: openxFactory
Purpose: fix the name of the domain-neutral governed review-and-disposition
workbench so contracts, docs, and the forthcoming credential work all build on
one settled term.

Ratification: the naming is LOCKED as a direct ruling (below); formal
lifecycle ratification rides the forthcoming openXdox dispatch-credential
OpenSpec change (this record flips to `ratified` with `Ratified by:` on that
change landing).

## Decision (LOCKED — Brett, 2026-08-13)

The domain-neutral governed review-and-disposition workbench — the ideation
dashboard + intent plane + apply lane operating over a corpus of artifacts —
is named **openXdox**.

- **Capability name:** `openXdox` — house `openX<type>` capital-X form (the
  lowercase `openxFactory` / `openxWallet` spellings are the family
  exceptions, not the rule).
- **Short handle:** `dox` — already the Kubernetes namespace, the
  `dox-opensoft-qa.xforge.us` host, and the `doxbench_*` code-module prefix;
  all conform unchanged.
- **Surface / bench:** `doxBench` — the review workspace (and the existing
  acceptance rig), promoted from informal name to the capability's named
  surface.

## Why openXdox

- **Neutral artifact noun.** `dox` = documents + the `x` motif. Documents are
  the one artifact common to all five domains — engineering specs, clinical
  notes, ledger entries, ops runbooks, marketing briefs — so it is strictly
  more neutral than `specs` (engineering-only) or `notes` (leans informal /
  medical, and undersells a structured spec or a ledger entry).
- **On-convention and distinct.** `openX` + `dox` matches the house capital-X
  form, and the splitting `X` distinguishes it from the taken name `openDox`.
- **Zero rename.** The `dox` handle and the `doxbench_*` code family already
  exist; nothing in the namespace, host, or codebase has to move.

## Per-domain instances

One capability, one name; domains differ only in the corpus and in casual
reference:

- codexFactory — openXdox over *specs* (informally "the specs bench";
  `specsBench` is codex's instance label, never the capability name)
- MedxFactory — openXdox over *notes / cases*
- LedgerxFactory — openXdox over *entries*

## Alternative considered and rejected

**openXnotes** — cleaner connotation (no "doxxing" phonetic shadow) and a tidy
adjacency to the NotebookLM projection, but rejected as the primary name
because (a) "notes" is weak for engineering specs and ledger entries, (b) it
blurs against Google's *Notebook*LM, and (c) it would discard the embedded
`dox` namespace / host / code investment. Reconsider only if openXdox goes
market-facing, where the doxxing phonetic shadow — consciously accepted here
for an internal B2B governance tool — would warrant a brand review.

## Relationship to contracts

openXdox is realized by the `add-ideation-intent-plane` change. The
credentials it needs are named for it and follow the neutral-contract /
operator-as-binding principle
([hermes-stack-topology-per-client](../ideation/staging/hermes-stack-topology-per-client/hermes-stack-topology-per-client.md)):

- the **openXdox dispatch App** — `Actions: write` on the factory repo, held
  by the intent inbox as short-lived minted tokens; and
- the **content App** — `Contents: write` on the corpus, held in CI —

both to be contracted in `credential-contracts` as separate least-privilege
bindings (the dispatch credential MUST NOT reuse the content App's key: that
would give the credential-free serving tier a contents-write-capable key).
