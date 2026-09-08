# openXdox — Capability Naming Record

Status: ratified
Ratified by: add-dispatch-credential-contract
Kind: reference
Repository context: openxFactory
Purpose: fix the name of the domain-neutral governed review-and-disposition
workbench so contracts, docs, and the credential work all build on one settled
term.

Ratified by `add-dispatch-credential-contract` (2026-08-13) — the change that
contracts openXdox's dispatch and content credentials (see its
`credential-contracts` spec delta). The name was locked as Brett's direct ruling
(below) when this record was authored; landing that change is its lifecycle
ratification.

## Decision (LOCKED — Brett, 2026-08-13)

The domain-neutral governed review-and-disposition workbench — the ideation
dashboard + intent plane + apply lane operating over a corpus of artifacts —
is named **openXdox**.

- **Capability name:** `openXdox` — house `openX<type>` capital-X form (the
  lowercase `openxFactory` spelling is the family exception, not the rule;
  `openXwallet` left this list in Amendment 2).
- **Short handle:** `dox` — already the Kubernetes namespace and the
  `doxbench_*` code-module prefix; both conform unchanged.
- **Public host:** `openxdox.opensoft.dev` (Amendment 1, below). LOWERCASE on
  the wire even though the capability is branded with a capital X: Gateway API
  hostnames, TLS SNI and certificate subjects are all lowercase, so `openXdox`
  cannot appear in a manifest or a certificate. The brand and the label differ
  by design; this is not a spelling to reconcile.
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

## Amendment 1 — the public host (2026-08-14)

**`openxdox.opensoft.dev` replaces `dox-opensoft-qa.xforge.us`.** Brett's direct
ruling, in session: one domain, and the legacy names are **cut dead at
switchover** — no dual-host period and no redirect, a deliberate departure from
the openemr precedent, which ran dual-host.

`opensoft.dev` was already the house domain on the same QA edge (`20.245.1.91`),
carrying `openchart-qa`, `openemr-qa` and `gatekeeper.dartwing`; openXdox was
the last service still published on `xforge.us`. TWO names retire, because there
were two routes: the openXdox route above, and `ideation-dashboard.xforge.us` —
the original 2026-07-14 read-only deployment in namespace `xfactory-control`,
superseded by the credential-free dashboard pod inside the `dox` namespace.

The record above is amended rather than rewritten: `dox-opensoft-qa.xforge.us`
was true when the name was locked on 2026-08-13, and the short-handle argument
that cited it still holds — `dox` remains the namespace and the code-module
prefix. Only the host moved.

Realization: Omnigent-Install PR #98 (the two route declarations, the retired
route, the host lists in the live validators). DNS `A 20.245.1.91 TTL 300` was
added and verified 2026-08-14; the zone carries no CAA record, so Let's Encrypt
issuance is unblocked. **Not yet done at the time of writing:** the shared
`opensoft-edge-public` Certificate in namespace `opsx-edge` must gain the new
subject — it lives outside every repository in this workspace, so the live-mode
edge validators fail until that reissue lands, by design.

## Amendment 2 — `openXwallet` leaves the exception list (2026-08-26)

**`openxWallet` becomes `openXwallet`, the house `openX<type>` capital-X
form.** Brett's ruling of 2026-08-26 (R1 of `split-openxwallet-repo`), taken
because the product is being given its own repository and brand at
`opensoft/openXwallet`, and a brand created under a spelling this record lists
as an exception would ratify the exception a second time.

The wire label stays LOWERCASE — `openxwallet` capability ids, the
`xfactory_wallet_*` kind prefix, paths and finding codes are untouched —
because that is this record's own rule: the brand and the label differ by
design; this is not a spelling to reconcile. `openXwallet-Install` is
registered as a NAME here and no repository is created (Q4).

The record above is amended rather than rewritten: `openxWallet` was genuinely
a family exception when the form was locked on 2026-08-13, and the
short-handle argument that cited it still holds. Only the brand moved.

## Amendment 3 — `openDox` is taken knowingly (2026-09-06)

**The core is the `opensoft/openDox` PROJECT, and the collision is accepted
rather than absent.** Brett's ruling of 2026-09-04 (RULING C1 on
`opensoft/openxFactory` issue #656, 17:46Z), taken because the
document-and-ideation workbench becomes two open-source layers and the neutral
core needs the neutral name.

**The facts, as measured on 2026-09-04 rather than asserted.** A GitHub
ORGANIZATION named `opendox` EXISTS — created 2026-03-20, holding one public
repository `opendox/dox` ("Rethinking Amazon Product Performance
Intelligence", 357 KB, last pushed 2026-05-31) on an unrelated subject. GitHub
search returns SIX repositories named `opendox`: `noitran/opendox` (22 stars, a
Laravel/Lumen OpenAPI package, last pushed 2022-02-10 — the largest and
dormant), `fum4/opendox` (0 stars, pushed 2026-07-16, "Spec + CLI + skill for
agent-written repo docs" — an ACTIVE 2026 project in the ADJACENT
agent-written-docs space), `dibinraj2003/opendox` (0 stars, 2026-08-10),
`andymadson/opendox` (1 star, 2025-08-27), `mfbmina/opendox` (2023-01-04) and
`ritskush1/opendox` (2017-05-22). GitHub namespaces repositories PER OWNER, so
none of these blocks `opensoft/openDox`; the ORGANIZATION name is unavailable
and **no claim is made on it**. The brand lives under `opensoft`.

**What is accepted.** The adjacent-subject overlap with `fum4/opendox` is known
and accepted; which specific abandoned repository originally prompted the word
"dead" is immaterial to this record. `openXnotes` stays documented as the
considered alternative and remains unused.

**The record above is amended rather than rewritten.** The sentence "the
splitting `X` distinguishes it from the taken name `openDox`" was written on
2026-08-13 against a one-word claim that nobody had measured; the measurement
is above and the distinction it drew is now a deliberate two-layer
relationship rather than an avoidance. `openXdox` keeps its name, its
lowercase wire label, its `dox` handle and its host; what changed is that the
neutral layer below it is now also named.

**SIX REPOSITORY NAMES, AND THE ELECTION THAT PRODUCED THEM.** Brett's ruling
of 2026-09-05T14:52Z (`opensoft/openxFactory` issue #656, comment
`5552614170`), verbatim *"elect the shape for both, follow the pin chain, no
family yet"*, ELECTS the `openRepoShape` three-repository shape for both
layers. The names this record registers are therefore six:
`openDox`, `openDox-spec`, `openDox-code`, `openXdox`, `openXdox-spec` and
`openXdox-code`. The election is recorded where the doctrine says it lives —
each assembly root's `project.yaml`, `elected_by: Brett Heap`,
`elected_on: 2026-09-05`, `reference: openxFactory docs/project-repo-schema.md` — and this
record only registers the NAMES.

**The leg suffixes are not new brands.** `-spec` and `-code` are lowercase and
hyphenated precisely so they sit in a different naming family from every
CamelCase product name this record governs: `openDox-code` is a LEG of the
openDox project, not a product called "openDox-code", and the `openX` + `dox`
reasoning above does not apply to it. **Electing the shape confers nothing** —
no gate, no floor, no grant, no authority — so nothing else in this record
moves with it. `openXdox-Install` keeps its own form and its own rule: it is
an INSTALL name, not a leg, and it is still registered with no repository
created.

**The descendant spelling is unaffected.** The transcript spells the
descendants `medXdox` and `CodeXdox`; the ratified `<Domainx><Product>` form
governs, so they are `MedxDox`, `codexDox`, `LedgerxDox`, `AdxDox` and
`OpsxDox` — registered as NAMES here with no repository created, on the same
rule that registered `openXwallet-Install`. A descendant scaffolded the same
way carries the same two legs, so its leg names are registered beside it —
`codexDox-spec`, `codexDox-code`, `MedxDox-spec`, `MedxDox-code`, and so on
for `LedgerxDox`, `AdxDox` and `OpsxDox` — and, again, no repository is
created for any of them.
