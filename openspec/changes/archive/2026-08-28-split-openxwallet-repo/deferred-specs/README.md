# Deltas held back from this archive's spec apply

Status: record
Kind: record
Repository context: openxFactory
Ratified by: split-openxwallet-repo

These two delta directories were authored by `split-openxwallet-repo` and are
ratified. They were **NOT applied at this archive**, and they sit here rather
than under `specs/` so the packet says which of its deltas landed and which did
not, in the tree rather than only in prose.

## Why they could not be applied

Both are `## MODIFIED Requirements` deltas whose target capability is **not in
`openspec/specs/`**:

| Delta | Target capability | Host change (ACTIVE) |
| --- | --- | --- |
| `trust-anchor/spec.md` | `trust-anchor` | `add-trust-anchor` |
| `review-authority-intake/spec.md` | `review-authority-intake` | `add-wallet-carried-review-authority` |

`openspec archive` refuses that shape. Measured 2026-08-28 on a scratch copy of
the corpus, verbatim:

```
review-authority-intake: target spec does not exist; only ADDED requirements are
allowed for new specs. MODIFIED and RENAMED operations require an existing spec.
Aborted. No files were changed.
```

This is not a defect in the packet. Both deltas were **declared relative to the
OUTCOME of their host change** rather than against a promoted spec — the
proposal's `### Modified Capabilities` block says so explicitly, and each delta
file restates its target requirement's full text as the host change will promote
it. That is `release-realization`'s ordered-delta rule
(`openspec/specs/release-realization/spec.md:64-79`) applied by **parity**: the
rule's letter covers a requirement already MODIFIED by an active ratified change,
and these requirements are ADDED, so the parity is declared rather than implied.
A delta declared against an outcome cannot land before that outcome exists.

## Where the obligation lives now

Recorded ON each host change's own tasks ledger, so it falls due where the work
will be done:

- [`../../../add-trust-anchor/tasks.md`](../../../add-trust-anchor/tasks.md) — task 8.2
- [`../../../add-wallet-carried-review-authority/tasks.md`](../../../add-wallet-carried-review-authority/tasks.md) — task 9.1

At each host change's promotion, the ADDED text of the named requirements MUST
carry the amendment recorded here. See this packet's `tasks.md` § 14.

## Why not under `specs/`

`scripts/doc_health/promotion_fidelity.py` reads `archive/<change>/specs/*/spec.md`
and treats every writer there as a promotion obligation that is due NOW. Left
under `specs/`, these four requirements raise four `error`-severity findings
reading "targets capability …, which has no promoted spec" — measured, not
assumed. That family's own remedy line offers two routes: "apply the ratified
delta to the promoted spec through an OpenSpec change, **or record the
non-promotion as deliberate**." This directory, § 14 of `tasks.md`, and the two
host-change ledger tasks are that record.

Nothing was forced and nothing was discarded: the delta text is intact, byte for
byte, in the files beside this one.
