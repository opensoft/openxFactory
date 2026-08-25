# Design: add-projection-title-uniqueness

Status: draft

The decision this document exists for is **which title derivation replaces the
`README`-only special case**, and it was taken on measurement rather than on
taste. Everything numbered here was produced on 2026-08-25 by running the
sync's own `scan()` over a scratch assembly of the ten repositories at the live
mains the books mirror, then re-deriving titles with each candidate out of tree
and diffing the result against the current derivation. No apply-mode run and no
provider mutation; the live source counts come from a read-only listing.

## 1. The mechanism, stated exactly

`scan()` returns `{book: {relpath: title}}`. `sync_book()` then:

1. lists the book's live sources into `by_title`;
2. computes `wanted_titles = set(desired.values())` — **N path keys collapse to
   one title here**;
3. deletes, for every managed title, `sids` if unwanted and `sids[1:]` if
   wanted — **the book is actively held at one source per title**;
4. iterates `sorted(desired.items())` and writes `mf[rel]` for **every** path
   key — **the manifest records N documents as synced**.

On a fresh book, step 4 adds one source per document, because `by_title` is not
refreshed inside the loop; the NEXT run's step 3 deletes all but the first, and
from then on step 4 skips both (each document's own digest matches its own
manifest row). Steady state: one source, N manifest rows, and the surviving
source carries whichever document's content won the race.

That is the whole defect. It is not a provider limitation and not a race — it
is a derivation that is not injective, reconciled by a mechanism that assumes
it is.

## 2. Why the parity mode cannot see it

`parity_report()` computes `derived = set(items.values())` per book and
compares it against the set of live bracket-titled sources. A collapse leaves
the two sets equal. Parity reports OK on a book that is missing documents,
which is why this defect survived to be found by reading a sync report rather
than by any check.

The fix is not a new family: the mode already reads the desired map, which is
keyed by path. It needs to compare cardinalities, not just sets, and to name a
title that carries more than one path key. That is why the parity amendment is
in the same delta as the rule — a rule guaranteeing injectivity and a check
that cannot observe injectivity would ship the same silence somewhere new.

## 3. Census: what is collapsed today

| book | derived title | documents | absent |
| --- | --- | --- | --- |
| `ideation-medxfactory` | `[staged] MedxFactory: topic` | 4 | 3 |
| `drafts` | `[draft] openxFactory: requirements` | 2 | 1 |
| `ideation-opsxfactory` | `[staged] OpsxFactory: exchange-execution-bringup` | 2 | 1 |

Three collisions, eight documents, five displaced. 693 derived book slots
resolve to 688 distinct titles; the seven live books hold 695 sources
(688 + 7 charters) where the scan wants 700.

Three further same-repository stem pairs are LATENT — identical stems saved
today only by a status difference that puts different prefixes on their
titles: `memory-gateway/README` in openxFactory (contracts and examples — note
that this pair is created by the CURRENT `README` rule, which is therefore not
injective either), `company-provisioning` in LedgerxFactory, and
`codexfactory-domain-hermes-content` in openxFactory. Each is one `Status:`
edit away from a live collapse.

## 4. The candidates, measured

A renamed title is a delete plus an add on a book, so "ops" is twice the rename
count. "Sources" is the total across the seven books after the change (695
today). "Left" is the number of documents still sharing a title after the rule
is applied — the correctness column.

| candidate | renamed | ops | sources | left |
| --- | --- | --- | --- | --- |
| current (`README` only) | — | — | 695 | **5** |
| **(a) collision-triggered minimal suffix** | **14** | **28** | **700** | **0** |
| (b1) always `<parent>/<stem>` | 572 | 1144 | 699 | **1** |
| (b2) always the full repository-relative path | 611 | 1222 | 700 | 0 |
| (c) declared structural stems always qualified | 14 | 28 | 699 | **1** |

**(b1) is eliminated on correctness, not on cost.** Both checklist documents
live in a directory named `checklists`, so `checklists/requirements` collides
with itself. 572 renames and the defect survives. A one-level qualifier is not
a fix, it is a longer version of the same assumption.

**(c) is eliminated for the same reason, and the reason generalizes.** A
declared list of structural filenames (`README`, `topic`, `requirements`,
`index`, `spec`, `tasks`, `design`, …) qualifies the MedxFactory four and the
checklist pair, and misses `exchange-execution-bringup` — a topic name, not a
structural one, that happens to appear as both a brainstorm document and its
staging fragment. No list would have contained it. This is the measured form of
the general objection: a fixed enumeration answers the instances known when it
was written, which is exactly what the `README` special case already was.

So the fork is **(a) versus (b2)**: 28 provider operations with titles that
depend on collision state, or 1222 with titles that never do.

**(b2) is genuinely stable** — a document's title is a function of its own path
and nothing else, so no document is ever renamed by another document's arrival
or departure. Its costs are one-time churn on 611 of 693 slots and title length
(longest 130 characters against 110 today; every title gains `ideation/staging/`
or `contracts/` or `docs/` whether or not anything is ambiguous). It also
discards the readability the current titles have: `[staged] MedxFactory:
treatment-plan-generation` is a better citation label than `[staged]
MedxFactory: ideation/staging/treatment-plan-generation/topic`, and titles are
what chat cites.

**(a) is recommended.** It leaves 679 of 693 titles exactly as they are, adds
the five missing sources, and closes all three latent pairs as a side effect of
its scope choice. Its cost is named plainly in § 5.

**RULED (2026-08-25, Brett, in-session multiple choice): recommendation
adopted — candidate (a) at repository scope.** `proposal.md` § Open Questions
OQ-1 rules this decision and folds in the scope sub-question (§ 7 below,
OQ-4): repository scope, 14 renames, 28 operations, zero collisions, closing
the three latent pairs as a side effect.

## 5. What (a) costs, and the variant that would remove it

Under (a) a title is a function of the document AND of its same-stem siblings.
Concretely: today `[staged] OpsxFactory: exchange-execution-bringup` becomes
`brainstorm/exchange-execution-bringup`; if the staging fragment were later
deleted, the survivor would revert to the bare stem — one more delete-plus-add.
Adding a second `topic.md` to a repository that had one renames the incumbent.

The exposure is small and it is measurable: across 675 distinct documents there
are 555 distinct stems, and only 13 stems are used by more than one document
anywhere in the corpus. Of those, `README` (50 documents) is already handled by
the floor, `document-catalog-adoption` (6), `packet-lifecycle-headers` (4),
`credentialing` (3), `omnigent-constitution` (2), `worker-enrollment-broker` (2)
and `INDEX` (2) each appear once per repository and so cannot collide under a
repository-scoped rule, and the remaining four are the three live collisions
plus one latent pair. The rate of new colliding stems is low, and each event
costs two operations on one book.

**Variant (a′), recorded and not proposed.** The manifest already stores a
`title` per document. Pinning a document's QUALIFICATION LEVEL there — allowed
to rise when a collision appears, never to fall when one disappears — makes
titles monotonic and removes the revert case entirely, at zero migration cost
beyond (a)'s 28 operations. It is not proposed because it turns
`.claude/nlm-sync-manifest.json` from a pure content cache (safe to delete;
deleting it today costs one re-upload pass and nothing else) into a store of
identity state whose loss silently changes titles. If Brett wants monotonic
titles, the honest form is (b2), which achieves it without state.

## 6. The exact migration (a) produces

Fourteen renames, 28 operations, five net new sources. Enumerated in advance so
the apply can be checked against a list rather than trusted:

| book | current title | new title |
| --- | --- | --- |
| `canon` | `[standard] openxFactory: memory-gateway/README` | `[standard] openxFactory: contracts/memory-gateway/README` |
| `canon` | `[ratified] LedgerxFactory: company-provisioning` | `[ratified] LedgerxFactory: docs/company-provisioning` |
| `drafts` | `[draft] openxFactory: memory-gateway/README` | `[draft] openxFactory: examples/memory-gateway/README` |
| `drafts` | `[draft] openxFactory: requirements` | `[draft] openxFactory: 005-customer-subject-runtime/checklists/requirements` |
| `drafts` | `[draft] openxFactory: requirements` | `[draft] openxFactory: 007-client-identity-roster/checklists/requirements` |
| `ideation-ledgerxfactory` | `[staged] LedgerxFactory: company-provisioning` | `[staged] LedgerxFactory: company-provisioning/company-provisioning` |
| `ideation-medxfactory` | `[staged] MedxFactory: topic` | `[staged] MedxFactory: root-truth-grounding/topic` |
| `ideation-medxfactory` | `[staged] MedxFactory: topic` | `[staged] MedxFactory: root-truth-target-claims/topic` |
| `ideation-medxfactory` | `[staged] MedxFactory: topic` | `[staged] MedxFactory: terminology-normalization/topic` |
| `ideation-medxfactory` | `[staged] MedxFactory: topic` | `[staged] MedxFactory: treatment-plan-generation/topic` |
| `ideation-openxfactory` | `[brainstorm] openxFactory: codexfactory-domain-hermes-content` | `[brainstorm] openxFactory: brainstorm/codexfactory-domain-hermes-content` |
| `ideation-openxfactory` | `[staged] openxFactory: codexfactory-domain-hermes-content` | `[staged] openxFactory: codexfactory-domain-hermes-content/codexfactory-domain-hermes-content` |
| `ideation-opsxfactory` | `[staged] OpsxFactory: exchange-execution-bringup` | `[staged] OpsxFactory: brainstorm/exchange-execution-bringup` |
| `ideation-opsxfactory` | `[staged] OpsxFactory: exchange-execution-bringup` | `[staged] OpsxFactory: exchange-execution-bringup/exchange-execution-bringup` |

The four `memory-gateway/README`, `company-provisioning` and
`codexfactory-domain-hermes-content` rows are the latent pairs of § 3: they are
not collapsed today, and they are qualified anyway because the uniqueness scope
is the repository. Under the tightest correct scope — (book, repository,
status) — they would not be, and the migration would be 8 renames instead of 14
while leaving those three pairs one status edit from a collapse.

## 7. Uniqueness scope, measured three ways

| scope | renamed | ops | left | immune to |
| --- | --- | --- | --- | --- |
| (book, repository, status) — tightest correct | 8 | 16 | 0 | nothing |
| (book, repository) | 10 | 20 | 0 | status change within one book |
| **repository — recommended** | **14** | **28** | **0** | any status change, any book move |

All three produce the same 700 sources and the same zero collisions; they
differ only in how much they qualify pre-emptively. The scope must include the
repository, and cannot be the book alone: `drafts` and `canon` carry documents
from every repository, and the repository name is already IN the title, so
grouping by book alone over-qualifies across repositories that never collide.

## 8. Capacity, checked

The capacity guard computes projected occupancy as `len(desired) + 1 +
unmanaged` — documents, plus charter, plus preserved strays. It has always
counted the collapsed documents, so **no candidate moves a single
guard-computed number**; what changes is that actual occupancy finally equals
it.

| book | guard today | live today | after (a) |
| --- | --- | --- | --- |
| `canon` | 114 | 114 | 114 |
| `drafts` | 189 | 188 | 189 |
| `ideation-openxfactory` | 247 | 247 | 247 |
| `ideation-ledgerxfactory` | 66 | 66 | 66 |
| `ideation-medxfactory` | 52 | 49 | 52 |
| `ideation-opsxfactory` | 17 | 16 | 17 |
| `ideation-codexfactory` | 15 | 15 | 15 |

The cap is 300 and the warn threshold fires at headroom of thirty or fewer,
i.e. at occupancy 270. The largest book is `ideation-openxfactory` at 247,
headroom 53, and it contains no collisions, so it does not move under ANY
candidate. Nothing trips the cap and nothing trips the warn.

## 9. Where the rule is written

The delta MODIFIES `Authority framing`, the requirement that already states
what a source title is, rather than adding a second requirement about titles.
The alternative would leave the title contract in two places and the injective
obligation in only one of them. The cost is a full byte-for-byte restatement of
the existing requirement and both of its scenarios, which the promotion-fidelity
family enforces and this packet's own gate run verifies.
