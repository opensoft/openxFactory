---
code_surface: openxFactory — ONE file, `scripts/doc_health/families.py`, whose `_resolve_capability` (line 1317) and `fam_tag_hygiene` (line 1331) gain a second resolution arm for a pinned target, plus that arm's tests under `tests/doc-health/` (hyphen: the tests directory is `tests/doc-health/`, while the package under test is `scripts/doc_health/`). NO BYTE OF EITHER MOVES IN THIS PULL REQUEST. This pull request carries the PACKET ONLY — `proposal.md`, `design.md`, `tasks.md`, `.openspec.yaml`, two `## MODIFIED` spec deltas, one README "Active changes" bullet, and the machine-seeded per-change sweep-ledger row in `tests/sequenced_after/corpus-ledger.yaml` (a derived bookkeeping file, not test implementation). THE REALIZATION IS A LATER PULL REQUEST in this same repository, authored after ratification, and it is FOUR surfaces and not more: (1) the resolver arm and its tests; (2) the four affected markers retargeted from `target=openxwallet` to the pinned form; (3) `docs/document-lifecycle.md`'s Prose Tagging Markers section carrying the new form and the stale-target rule; (4) the stale sentence at `ideation/staging/INDEX.md:2262-2265`, which still calls three `openxwallet` blocks "all resolving" and has been false since 2026-08-28. NOT THIS PACKET'S SURFACE, each for a stated reason: no marker regex changes, because the existing `_CAND_OPEN` and `_ATTR` patterns already accept the proposed value unchanged (design D-1, measured); no pin record is edited and no pin schema member is added — D-2 RESERVES the member name `capabilities:` as the trigger for its dormant conditional arm, so that the arm has a deterministic input contract rather than an intention, but it NAMES it and does not add it: no pin record gains that member here, no schema admits it here, and whether a real pin record may carry it is a `neutral-product-pin` question with the publisher (design D-2); no capability is created, deleted or renamed; no `openspec/specs/` directory moves; no contract byte, pin byte or digest moves; no contract bundle is cut.
target_release: implemented
---

# Proposal: extend-prose-tagging-target-to-pinned-capabilities

Status: draft

Proposed: 2026-09-12 at approximately 01:55Z by Brett Heap (openxFactory
repository owner), first-hand, in session to lane `openxfactory-2` (display
`openXfactory-2`) — **a SELECTION, not a typed sentence**: presented with the
lane's multi-select question, he chose the option ***"#992 grammar-extension
OpenSpec change (Recommended)"***. Recorded on openxFactory #745. That word
commissioned the FILING of the change openxFactory issue #992 asks for, and
nothing further: **no ratification, no realization and no archive is claimed
by this packet**, and every document in it carries `Status: draft`.

## Why

### The four findings, and why no edit can clear them honestly

`python3 scripts/doc-health.py --single-repo . --family tag-hygiene` reports
FOUR `error`-band, `auto-fixable`-labelled findings on `origin/main`, all one
shape:

```text
[error] oxf:ideation/staging/notebook-access-wallet-governance/notebook-access-wallet-governance.md — unresolved target=openxwallet at line 107
[error] oxf:ideation/staging/openxwallet-neutral-home/openxwallet-neutral-home.md — unresolved target=openxwallet at line 222
[error] oxf:ideation/staging/openxwallet-neutral-home/openxwallet-neutral-home.md — unresolved target=openxwallet at line 242
[error] oxf:ideation/staging/openxwallet-neutral-home/openxwallet-neutral-home.md — unresolved target=openxwallet at line 280
```

The archived change that produced them,
`openspec/changes/archive/2026-08-28-split-openxwallet-repo/`, already reasoned
through both mechanical fixes and rejected both, in its own
`tasks.md:1770-1786`:

> "**The cause is this archive and nothing else.** `document-lifecycle`'s
> prose-tagging grammar resolves an `<!-- xspec:candidate target=… -->` marker
> through `families.py::_resolve_capability`, which admits a name only if it is
> a capability under `openspec/specs/` or an active change id, searched in this
> repository and then in `openxFactory`. Deleting `openspec/specs/openxwallet/`
> removed the only referent those four markers had.
>
> **They are NOT fixed here, deliberately.** The band says `auto-fixable`, but
> no mechanical fix is truthful: retargeting a marker to
> `domain-descendant-boundary` or `neutral-product-pin` would make the marker
> name a capability the tagged prose is not about, and deleting the markers
> would silently drop four blocks out of the conversion queue. The honest fix
> is a GRAMMAR EXTENSION — a target form that can name a capability which now
> lives in a pinned neutral product — and that is a change, not an edit."

### The grammar is silent, not merely unhelpful

`docs/document-lifecycle.md:183-185` defines only what a valid target IS:

> "`<capability>` is a spec capability id under `openspec/specs/` (or in an
> active change's `specs/` while the capability is pre-promotion)"

Neither that bullet nor any other sentence of that document addresses a target
that USED TO resolve and no longer does. The corpus's first capability EXIT
found the rule missing, and the checker's single fixed remedy string
(`families.py:1367-1368`) inherits the silence: it tells an author what a valid
target looks like, and cannot tell them which capability is faithful to any one
of these four blocks — because the capability those blocks are about is not in
this repository at all.

### The owed successor has been on the register since the archive, unopened

`README.md:6828-6832` carries it as numbered item (7) of the
`split-openxwallet-repo` archived-ledger entry:

> "(7) **A prose-tagging target form for a capability that has left the
> corpus** — added at the archive itself, because the act produced it: deleting
> `openspec/specs/openxwallet/` left four `<!-- xspec:candidate
> target=openxwallet -->` markers in `ideation/staging/` with no referent,
> since `families.py::_resolve_capability` admits only an in-tree capability or
> an active change id."

A corpus-wide search for that item's own wording returns only the one README
passage. No proposal, staged topic, or active or archived change anywhere else
picks it up. **This packet is that successor, and it is the first.**

### The house has already been working around the gap

A later staged topic, `wallet-carried-work-authority` (2026-09-02, after the
archive landed), declined to fence new wallet-topic prose as a candidate at
all, citing this exact precedent (`ideation/staging/INDEX.md:2362-2366`):

> "`openxwallet` and `work-authority-intake` are deliberately NOT fenced, on
> `openxwallet-neutral-home`'s recorded precedent: neither resolves as a
> capability in this repository, so fencing them would emit tag-hygiene
> unresolved-target findings."

That is a precedent for NOT FENCING NEW PROSE. It is not a rule, it is not
written anywhere a checker can read, and it costs the conversion queue every
block it touches. A grammar that can NAME the absent referent lets the prose be
fenced and queued truthfully instead.

## What Changes

**One grammar extension, in three parts, none of them realized here.**

1. **A target form that can name a capability in a pinned neutral product.**
   `target=pinned:<pin-id>/<capability>`, in an `xspec:candidate` marker's
   `target=` attribute and there only (design D-1.1 closes the
   `xspec:supersedes` `spec=` case explicitly rather than leaving it silent),
   where `<pin-id>` is the stem of a
   `contracts/<pin-id>-pin.yaml` record this repository already carries and
   `<capability>` is the capability name as the pinned product holds it. For
   the four affected markers that is `target=pinned:openxwallet/openxwallet`.
   The form is chosen because it is the ONLY candidate the existing marker
   regexes accept with no regex change at all — `_CAND_OPEN`'s attribute value
   class is `[^\s>]+` and `_ATTR`'s is `\S+`, both of which already admit `:`
   and `/`, and `spec=<capability>/<requirement-slug>` is the standing
   precedent for a `/` inside an attribute value (design D-1).

2. **A resolution rule that rests on the pin, and says so.** The `<pin-id>`
   MUST resolve to a NEUTRAL-PRODUCT pin record in this repository's pin
   registry — `kind: pinned_contract_manifest`, the shape `neutral-product-pin`
   requires; a `pinned_workflow` record pins executable governance code and is
   excluded, since it has no capability set for a name to be about. The
   `<capability>` segment is NOT resolved further, because **no pin record in
   this tree enumerates capabilities** — measured over all six at `323c7adf`.
   What each record addresses INSTEAD differs, and the differences matter
   enough to state rather than average: two enumerate files (`files:` beside
   `pinned_by_commit_only:`), two carry tree `digests:`, one carries workflow
   `pinned_members:`, and `contracts/openspec-cli-pin.yaml` enumerates NOTHING
   — it carries ONE whole-artifact `integrity:` digest over a published tarball
   plus a lockfile referent, and its own comment at
   `contracts/openspec-cli-pin.yaml:69-76` states why it has neither a `files:`
   nor a `pinned_by_commit_only:` list ("ONE digest covers ALL 389 files, so
   the completeness question the two lists answer is answered here by
   construction"). The invariant this resolution rule rests on is the one that
   holds across all six: the absence of a CAPABILITY enumeration. A rule
   requiring one would therefore refuse every marker it exists to admit. The
   requirement is written so that a pin record which LATER enumerates
   capabilities tightens resolution automatically, without a further grammar
   delta. The enumeration is ONE NAMED MEMBER and not a search — a top-level
   `capabilities:` sequence on the pin record — so the dormant arm is
   deterministic; naming it adds it to nothing (design D-2).

3. **A stale-target rule, which `document-lifecycle` does not have today.**
   When a marker's target capability exits the corpus, the marker either takes
   the pinned form or the block is unfenced — never silently retargeted to a
   different capability, and never silently deleted (design D-3). This is the
   sentence issue #992 § 4's third bullet asks for, and it codifies the
   `wallet-carried-work-authority` precedent as a rule a reader and a checker
   can both apply.

**Spec deltas.** `## MODIFIED Requirements` against `document-lifecycle`'s
"Prose tagging marker hygiene" and `doc-health`'s "Tag hygiene enforced by
reference" — the second because the tag-hygiene family enforces the grammar BY
REFERENCE and its requirement enumerates what the family covers, an enumeration
the new arm extends.

**Not in scope, deliberately.** This packet does not retarget the four markers,
does not delete them, does not move a byte of the resolver, and does not correct
`ideation/staging/INDEX.md:2262-2265`. Those are the realization, and the
realization is a later pull request after ratification.

## Impact

- **Affected specs:** `document-lifecycle` (one MODIFIED requirement),
  `doc-health` (one MODIFIED requirement).
- **Affected code at realization, not here:** `scripts/doc_health/families.py`
  (`_resolve_capability`, `fam_tag_hygiene`) and its tests.
- **Affected documents at realization, not here:**
  `docs/document-lifecycle.md` (Prose Tagging Markers section), the four
  markers in `ideation/staging/`, and `ideation/staging/INDEX.md:2262-2265`.
- **Findings:** the four `tag-hygiene` findings stay OPEN until realization
  lands green. This packet changes their count by zero.
- **Release:** `target_release: implemented` and `code_surface` is non-empty,
  so per `release-realization` this packet archives ONLY on merged-plus-green
  realization evidence. No contract bundle is cut, nothing under `contracts/`
  moves, no `contract_bundle_version` is spent and no release tag is owed.
- **Other repositories:** none. The grammar is openxFactory's, the resolver is
  openxFactory's, and the four affected documents are openxFactory's. Sibling
  repositories inherit the extension when they next read the grammar; none is
  edited by this packet or by its realization.

refs #992 · refs #745
