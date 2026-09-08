# Staged: openXwallet's neutral home — its own repo, and domain descendants that pin and profile it

Status: staged
Kind: capability-proposal
Summary: openXwallet is today a set of features inside openxFactory — two
neutral contract families, a validator and a syntax gate, a CI workflow, two
promoted capabilities and a live governance estate — and no `opensoft/openXwallet`
repository exists. This topic settles where the wallet lives and how domains
reach it: the wallet moves to its own governed repo, openxFactory consumes it at
a commit-and-digest pin, and each domain gets a `<Domainx>Wallet` descendant that
pins and profiles the neutral product rather than integrating it directly. The
descendant pattern is not invented here — it is the existing house standard
(openChart, openPractice, openAvatar) ratified for the first time as a general
rule instead of one change per product. The first release is a byte-identical
pure move: zero key renames, zero capability-id renames, zero behaviour change.
Topics: openxwallet, openxwallet-agent-profile, repo-split, domain-descendant-boundary,
neutral-product-pin, submodule-pin, trust-anchor, review-authority-intake,
openxdox-naming, dtn-register, ledgerxwallet
Repository context: SPLIT across three homes on purpose. `opensoft/openXwallet`
(to be created) becomes the neutral product's home and owns both contract
families, the validator, the syntax gate, the corpus and the two promoted
capabilities. openxFactory keeps the SEAM — `governance/review-authority/`, the
trust-anchor / identity-brokering / roles-authority-model compositions, and all
ideation provenance — and consumes the product at a pin. The xFactory
aggregation gains a root-level `openXwallet/` submodule. `LedgerxWallet` is the
first domain descendant; LedgerxFactory is the only live consumer today.
Staging ID: openxFactory:staging:openxwallet-neutral-home
Captured: 2026-08-26
Source: Brett Heap's direction in session 2026-08-26, which asked two questions —
is openXwallet a repo-level project or features inside another repo, and do
domains integrate the neutral product directly or through a `<Domain>Wallet` repo
that pins it — and then, on the answer, ruled eight recommendations at once,
verbatim: "approve R1-R8 as recommended, stage the topic and propose". The
inventory those rulings rest on was measured against the live corpus the same
day. Origin provenance is the `agent-certification-wallets` brainstorm
(`ideation/brainstorm/agent-certification-wallets.md`, Brett 2026-07-15/16) and
the promoted change `openspec/changes/archive/2026-08-08-add-openxwallet/`.
Target capabilities: REMOVED `openxwallet` and REMOVED `openxwallet-agent-profile`
from the openxFactory corpus (moved, with the successor location recorded, to
`opensoft/openXwallet`); ADDED `domain-descendant-boundary` (the general standard
for how a domain consumes a neutral open* product); ADDED `neutral-product-pin`
(how openxFactory consumes an external neutral product — commit plus per-file
sha256 plus `pinned_by_commit_only`, tag-only refused, fail closed on an
uninitialized submodule or digest drift); MODIFIED `trust-anchor` (the custody
registry is resolved from the pin rather than from `ROOT/contracts/openxwallet/`);
MODIFIED `review-authority-intake` (the reader is the pinned tool, invoked by a
REQUIRED consumer check). The two ADDED capabilities are deliberately NOT fenced
as `xspec:candidate` targets below: neither exists yet in `openspec/specs/` or in
an active change's `specs/`, so fencing them would emit tag-hygiene
unresolved-target findings for prose this repo is otherwise the right home for.
The fenced blocks target `openxwallet`, which is the capability the REMOVED delta
acts on and the one this topic exists to relocate.

## Last proposal attempt (round-trip provenance)

Change ID: `split-openxwallet-repo` — proposed 2026-08-26, PR
opensoft/openxFactory#391
Raised: 2026-08-26
Status at demote: n/a — RATIFIED 2026-08-26 and never demoted
Demoted: n/a
Demote reason: n/a

## Claims

Eight rulings, given by Brett on 2026-08-26 as recommended, are settled context
and are not reopened by the open questions below.

1. **R1 — the repo and brand are `opensoft/openXwallet`, prose `openXwallet`.**
   This is the ratified house `openX<type>` capital-X form. `docs/openxdox-naming.md`
   (LOCKED 2026-08-13) currently names `openxWallet` as one of two family
   EXCEPTIONS to that form; the ruling removes the exception, which is why the
   change owes that record an Amendment 2 rather than a silent re-spelling.
2. **R2 — machine keys do not move in v1.** Paths stay `contracts/openxwallet/`,
   capability ids stay `openxwallet` and `openxwallet-agent-profile`, the kind
   prefix stays `xfactory_wallet_*`, the envelope kind stays
   `openxfactory-openxwallet-contract-schema`, and finding codes and filenames
   are unchanged. openxdox-naming's own rule is that brand and label differ by
   design — lowercase on the wire — and LedgerxFactory pins five kinds by name
   and pins finding-code strings, so a rename landing in the same change as the
   move would be unbisectable.
3. **R3 — the new repo owns the wallet's own standard; openxFactory keeps the
   seam.** openXwallet takes both contract families and the corpus, the
   validator, the syntax gate and its tests, the CI workflow, the two promoted
   specs, Speckit features 006/010/012, and the `2026-08-08-add-openxwallet`
   archive. openxFactory keeps `governance/review-authority/` (register, wallets,
   grants, attestations), Speckit 013/014, the active wallet-carried review
   authority work, the trust-anchor / identity-brokering / roles-authority-model
   compositions, and all ideation provenance. The wallet primitives are ratified
   holder-agnostic and non-substrate, so they are not factory-layer content; what
   IS factory-layer is how the review gate USES wallet authority.
4. **R4 — the dependency is pinned in both directions, and there is no cycle.**
   openxFactory pins openXwallet by commit plus per-file sha256 plus
   `pinned_by_commit_only` — the install-repo strictness — through a nested
   `openXwallet/` submodule and `contracts/openxwallet-pin.yaml`. openXwallet
   vendors exactly ONE openxFactory artifact at a digest pin,
   `contracts/schemas/hermes-job-envelope.schema.yaml`, because validator rule (g)
   ("one authority vocabulary") reads it. Both directions are commit-pinned
   read-only consumption, so nothing builds in a loop. The rejected alternative
   was making rule (g)'s vocabulary a CLI parameter with no default, which
   silently weakens the gate.
5. **R5 — workspace placement is a root-level `openXwallet/` submodule** in the
   xFactory aggregation, sibling of `openxFactory/` and `openAvatar/`, on the
   DTN-022 precedent: a neutral product is pinned at the aggregation's neutral
   root.
6. **R6 — the review-authority register stays in openxFactory; its READER moves
   with the validator.** The register is openxFactory's own review authority
   (`target_repo: opensoft/openxFactory`), and codexFactory's merge-gate floor
   pins the exact path `governance/review-authority/register.yaml` in
   `opensoft/openxFactory` with a parser that refuses wildcards. The reader —
   rule (u), `check_register`, `_load_attestations` — travels with the validator
   as a generic authority-register MODE, and openxFactory's consumer gate invokes
   the PINNED reader over its own tree. Zero refactor in the move, codexFactory
   unaffected, and "a grant with no reader in a required check confers nothing"
   is satisfied by a digest-pinned reader inside a required check.
7. **R7 — descendants are `MedxWallet`, `LedgerxWallet`, `codexWallet`,
   `OpsxWallet`, `AdxWallet`** — the `<Domainx><Product>` form all four existing
   descendants already use, not `medXwallet`, which would be a third casing
   scheme in the org. The cost of either choice is zero today because none of
   them exists.
8. **R8 — the first descendant is `LedgerxWallet`, created at extraction time.**
   LedgerxFactory is the only live consumer — two wallet records, two grants, one
   distinct-holder constraint, an exercise template and
   `tests/validate_wallet_estate.py` — so it has descendant content on day one.
   `MedxWallet` follows when the Medx EMR wallet thread stages its first profile;
   codex, Ops and Adx on demand.

9. **The house standard is the domain descendant repo, and there is no
   counter-example.** Every neutral open* product in the org is consumed by
   domains through a pin-and-profile descendant:

   | Neutral product | Domain descendant | How it was established |
   | --- | --- | --- |
   | `openChart` | `MedxChart` (`xFactories/MedxChart`) | `create-medxchart-overlay-boundary` |
   | `openPractice` | `MedxPractice` | `create-medxpractice-overlay-boundary` |
   | `openAvatar` (root-level submodule) | `MedxAvatar` (nested in MedxFactory), `LedgerxAvatar` | DTN-022, Brett 2026-08-03: own repo, and "domain descendants are pin-and-profile DISTRIBUTIONS … never code forks" |

   No DomainxFactory consumes any open* product by direct integration. The only
   direct consumer of neutral contracts is openxFactory-as-layer through
   `stack.yaml` — and openxFactory is the neutral layer, not a domain. So the
   wallet does not need a new pattern; it needs the existing one written down as
   a general standard.

10. **The four descendant-repo rules, generalized from those three precedents.**
    (a) A descendant pins the neutral product BY COMMIT, TWICE — nested submodule
    gitlink plus `contracts/<product>-pin.yaml` (`kind: <domain><product>_pin`,
    `relationship: pinned_upstream_composition`) — with both changed in the same
    commit. (b) It carries ONLY profiles, overlays, branding, deploy config and
    domain validators: pin and profile, never fork, and anything the profile
    cannot express is an upstream change. (c) It is nested into its
    DomainxFactory as a submodule (the MedxAvatar placement, being the more
    recent ruling) and may ALSO be aggregated at `xFactories/` (the MedxChart
    placement) if it needs to be cloned standalone. (d) It is created LAZILY and
    CONSUMER-GATED: the repo appears when the domain has its first profile, not
    before — which matches the wallet arc's own discipline, where every successor
    is gated on a consumer.

11. **The first release is a byte-identical pure move.** The eight artifact
    sha256s in openXwallet's own `contracts/manifest.yaml` must equal
    openxFactory HEAD's manifest rows before `wallet-v1.0` is tagged. Zero key
    renames, zero capability-id renames, zero corpus edits. Any content change
    the extraction wants is a separate, later change in the new repo, because a
    move whose diff is not provably empty cannot be bisected against.

## Evidence and inventory (measured against the live corpus, 2026-08-26)

Added-by: Claude Opus 5 (session, Brett's direction) · 2026-08-26

- **Footprint.** Two neutral contract families (`contracts/openxwallet/` core,
  `contracts/openxwallet-agent-profile/` as a structural sibling), one validator
  (`scripts/validate-openxwallet.py`) plus a syntax gate
  (`scripts/wallet-yaml-syntax-gate.py`, `tests/wallet_yaml_syntax_gate/`), one CI
  workflow (`.github/workflows/wallet-validation.yml`), two promoted OpenSpec
  capabilities (`openxwallet` at 8 requirements, `openxwallet-agent-profile` at 3,
  registered at `contract-v1.31`), five Speckit features (006, 010, 012, 013,
  014), and a live governance estate under `governance/review-authority/`. The
  conformance corpus stands at 17 positives and 36 negative confirmations.
  `opensoft/openXwallet` does not exist yet.
- **Rule (g) reads an openxFactory schema.** The validator resolves
  `contracts/schemas/hermes-job-envelope.schema.yaml` for its
  one-authority-vocabulary rule, so a moved validator with no vendored copy fails
  on EVERY run — which is why the pin is bidirectional (R4) rather than one-way.
- **trust-anchor hard-exits on a missing registry.** `scripts/validate-trust-anchor.py`
  exits hard when `contracts/openxwallet/openxwallet-custody.registry.yaml` is
  absent (around lines 2582-2591). Consumer repoint and shed must therefore land
  in ONE atomic pull request; a two-step move leaves a broken intermediate commit.
- **LedgerxFactory fails loudly, never skips.** Its
  `tests/validate_wallet_estate.py::find_openxfactory()` walks up the tree for
  `openxFactory/scripts/validate-openxwallet.py` and fails when it is not there.
  A forward-compatible finder — look for `openXwallet/scripts/…` first, fall back
  to `openxFactory/scripts/…` — must land in LedgerxFactory BEFORE openxFactory
  sheds anything.
- **codexFactory's merge-gate floor pins the register path exactly.** It names
  `governance/review-authority/register.yaml` in `opensoft/openxFactory` and its
  parser refuses wildcards, so the register cannot move without breaking a gate
  in another repository. (Separately, lead-security's 2026-08-26 finding that the
  floor path is unreachable in the checked tree is a PRE-EXISTING codexFactory
  issue, independent of this topic.)
- **hermes-install reseed is untouched.** Wallet content is NOT in `CONTENT_KINDS`
  and is not domain-overlay content, so the reseed path is unaffected by the
  extraction. The reseed-drift fix is therefore NOT a precondition, which an
  earlier reading of the sequencing assumed it was.
- **The release digests never indexed the family.** `contracts/releases/*.digests.yaml`
  has no wallet rows, so there is nothing to carry across — a gap to RECORD, not
  to backfill inside a move that must stay byte-identical.
- **Bookkeeping surface.** `contracts/manifest.yaml` rows 1967-2082 are the wallet
  artifact rows to remove, and seven incoming citations must be reworded to the
  pin: lines 2089, 2146, 2251, 2287, 2423, 2473-2475 and 2494-2495. The
  supporting edits are `contracts/CHANGELOG.md` (a `contract-v1.44` entry),
  `contracts/README.md` rows 106-108 collapsing to one "consumed at pin" row,
  root `README.md` (the gate section, the index, the active-change ledger and the
  archive record), `.github/CODEOWNERS` (drop the two validator lines, add the pin
  and the gitlink), `docs/openxdox-naming.md` Amendment 2, and
  `docs/archive-record-discrepancies.md` row 7 gaining a "carried to openXwallet"
  note.
- **Immutable provenance, annotate never rewrite.** `health/document-catalog/runs/**`
  snapshots, archived changes, the `cl-openxwallet` cluster in
  `ideation/cross-reference.yaml`, and `docs/archive-record-discrepancies.md` are
  records. The extraction annotates them; it does not edit them into agreement.

## Why

<!-- xspec:candidate target=openxwallet -->
The wallet's contracts ARE a product, and they are currently filed as features
of a factory layer. `openxwallet` and `openxwallet-agent-profile` are ratified
holder-agnostic and non-substrate — the core deliberately says nothing about
agents, patients, practitioners or ledgers — which is precisely the definition of
content that does not belong to any one layer's corpus. Meanwhile the thing that
IS factory-layer, how openxFactory's review gate uses wallet authority, sits in
the same repository with no boundary between them, so every wallet-primitive
change and every review-gate change land in one blast radius and one CODEOWNERS
surface. The pressure is now concrete rather than aesthetic: a second domain is
about to want wallet content, and the only pattern the org has for that —
domains reach a neutral product through a pin-and-profile descendant repo — is
established three times over (openChart, openPractice, openAvatar) and written
down nowhere as a general rule. Every prior instance paid for its own ratifying
change. Doing that a fourth time buys a fourth bespoke boundary instead of a
standard.
<!-- /xspec:candidate -->

## What changes

<!-- xspec:candidate target=openxwallet -->
Both wallet contract families, their validator and syntax gate, their conformance
corpus, their CI workflow and their two promoted capabilities leave the
openxFactory corpus for `opensoft/openXwallet`, carved with full path history and
tagged `wallet-v1.0` before anything in openxFactory changes. openxFactory then
consumes the product at a pin — a nested `openXwallet/` submodule at that commit
plus a `contracts/openxwallet-pin.yaml` carrying the commit, the bundle tag and a
per-file sha256 for each of the eight artifacts — and sheds the moved paths in
one atomic pull request, because the trust-anchor validator hard-exits without
the custody registry and cannot survive a two-step move. openXwallet vendors
exactly one openxFactory artifact in return, the Hermes job-envelope schema its
one-authority-vocabulary rule reads, at a digest pin with a resync runbook. The
existing `wallet-validation` workflow in openxFactory is replaced by an
`openxwallet-consumer-gate` that checks out submodules, verifies the pin digests,
and runs the PINNED syntax gate and the PINNED validator in authority-register
mode over `governance/review-authority/` — which is what keeps the register in
openxFactory (codexFactory's merge-gate floor pins its exact path and refuses
wildcards) while the reader that gives a grant force travels with the validator.
Machine keys do not move: paths, capability ids, the `xfactory_wallet_*` kind
prefix, the envelope kind, finding codes and filenames are all unchanged, and the
eight artifact digests must match openxFactory HEAD before the tag is cut.
<!-- /xspec:candidate -->

Two capabilities are ADDED alongside the move, and they are the reusable half of
this topic. `domain-descendant-boundary` ratifies the house standard: a domain
consumes a neutral open* product through a `<Domainx><Product>` descendant repo
that pins the product by commit TWICE (gitlink plus pin file, same commit),
carries only profiles and overlays and branding and deploy config and domain
validators, nests into its DomainxFactory as a submodule and may also be
aggregated at `xFactories/`, and is created lazily when the domain has its first
profile. `neutral-product-pin` ratifies the consumption strictness openxFactory
itself now needs: commit plus per-file sha256 plus `pinned_by_commit_only`, a
tag-only pin REFUSED, and fail-closed behaviour on an uninitialized submodule or
a digest that disagrees with the pin. Neither capability is fenced above, for the
reason the header states — they do not resolve yet.

## Impact

<!-- xspec:candidate target=openxwallet -->
- Affected specs: `openxwallet` (REMOVED — both promoted capabilities leave the
  openxFactory corpus with their successor location recorded),
  `openxwallet-agent-profile` (REMOVED — same), `domain-descendant-boundary`
  (ADDED — the general descendant standard), `neutral-product-pin` (ADDED — the
  consumption strictness), `trust-anchor` (MODIFIED — the custody registry
  resolves from the pin, and the check fails closed on an uninitialized submodule
  or digest drift), `review-authority-intake` (MODIFIED — the reader is the
  pinned tool inside a REQUIRED consumer check).
- Affected code: openxFactory (`contracts/openxwallet*/`, `scripts/validate-openxwallet.py`,
  `scripts/wallet-yaml-syntax-gate.py`, `scripts/validate-trust-anchor.py`,
  `tests/wallet_yaml_syntax_gate/`, `tests/trust-anchor/`,
  `.github/workflows/wallet-validation.yml`, `.github/CODEOWNERS`,
  `contracts/manifest.yaml`, `contracts/README.md`, `contracts/CHANGELOG.md`,
  `README.md`, `docs/openxdox-naming.md`, `docs/archive-record-discrepancies.md`);
  the new `opensoft/openXwallet` repository in full; the xFactory aggregation
  (`.gitmodules`, the root gitlink, README layout and Terms, `CLAUDE.md`);
  LedgerxFactory (`tests/validate_wallet_estate.py`, a quickstart path, an
  ownership comment, README); OpsxFactory (one doc path).
- Not affected, verified: hermes-install (wallet content is not in `CONTENT_KINDS`,
  so reseed is untouched); codexFactory (the register does not move);
  MedxFactory brainstorm links (they point at the openxFactory brainstorm, which
  stays); keycloak-install and openxpki-install citations (doctrinal prose).
- Working-rule blast radius: the aggregation's working rule #1, "domain-neutral
  contracts live ONLY in openxFactory", becomes false as written the moment this
  lands and must be amended in the same wave to "…or in a neutral open* product
  repo that openxFactory pins; domain repos never author neutral contracts".
- Branch protection: `wallet-validation` becomes REQUIRED in the new repo from
  day one, and `openxwallet-consumer-gate` becomes REQUIRED in openxFactory —
  which is where the wallet arc's outstanding "the check is not yet required"
  task discharges, in the new topology rather than before the move.
<!-- /xspec:candidate -->

## Sequencing constraints

Added-by: Claude Opus 5 (session, Brett's direction) · 2026-08-26

1. **The LedgerxFactory forward-compatible finder lands FIRST.** Phase 5a — the
   `find_openxfactory()` change that looks for `openXwallet/scripts/validate-openxwallet.py`
   first and falls back to `openxFactory/scripts/…` — must merge BEFORE
   openxFactory sheds the validator, because Ledgerx CI fails loudly rather than
   skipping. It is forward-compatible by construction, so it can land any time.
2. **`wallet-v1.0` exists before openxFactory changes.** The tag in the new repo
   is a precondition of the consume-and-shed pull request, which keeps every
   commit on openxFactory's main bisectable.
3. **Consume and shed are ONE atomic pull request.** The trust-anchor validator
   hard-exits without the custody registry, so no ordering of two commits leaves
   a green intermediate state.
4. **The not-yet-REQUIRED check resolves in the NEW topology.** The wallet arc's
   open "mark the check required" task is discharged by requiring
   `wallet-validation` in openXwallet from day one and requiring
   `openxwallet-consumer-gate` in openxFactory — not by marking the old workflow
   required and then moving it.
5. **The active wallet-carried review-authority change authors its `openxwallet`
   core deltas AFTER the split.** Its slices S3 and S5 are entirely open and
   tagged for hermes-install and codexFactory; if the extraction lands first,
   those deltas are authored once, in the right repository, instead of being
   written in openxFactory and immediately migrated.
6. **Kindless files have their shape only in the validator.** The register and
   the custody attestation carry no `kind`, so the pinned reader is their only
   reader — and the pin manifest's digest is what makes "which reader ran" an
   auditable fact rather than an assumption.
7. **Shared tree discipline.** Every commit in this arc stages explicit paths and
   commits with pathspecs, and checks `git status -sb` for the current branch
   before any submodule commit.

## Idea notes (pre-document, non-documented)

- The wallet is the first open* product whose CONTRACTS are the product. openAvatar
  moved CODE and left the contracts in openxFactory; here the contract families
  are the thing being shipped, which is why R3 splits along a seam (product vs.
  how a gate uses the product) rather than along a file type. Worth watching
  whether that seam generalizes to the next extraction or is wallet-specific. —
  Added-by: Claude Opus 5 (session, Brett's direction) · 2026-08-26
- `openXwallet-Install` is a real eventual repo and has zero footprint today: no
  runtime, no issuer service, no key custody host. Hermes is the likely issuer
  host, and it currently has no wallet footprint at all. Registering the name now
  and building nothing is probably right, but naming a repo before a consumer
  exists is exactly what the lazy-descendant rule (claim 10d) says not to do. —
  Added-by: Claude Opus 5 (session, Brett's direction) · 2026-08-26
- The bidirectional pin is a small cycle in the DEPENDENCY GRAPH even though it
  is not one in the BUILD graph. Two repos each holding a digest of the other's
  file means a resync runbook is load-bearing documentation, not a nicety, and
  the failure mode (a stale vendored envelope schema silently passing rule (g)
  against last month's vocabulary) is quiet rather than loud. — Added-by: Claude
  Opus 5 (session, Brett's direction) · 2026-08-26
- Five descendant repos named (R7) and one built (R8) means four names sitting
  unused. That is deliberate under the lazy rule, but a named-and-absent repo is
  also a thing people create by hand at 2am. The naming record is worth more than
  the reservation. — Added-by: Claude Opus 5 (session, Brett's direction) ·
  2026-08-26
- The NotebookLM projection derives `xf-ideation-openxwallet` automatically once
  the repo exists, because books resolve by title. Nothing to design; just a sync
  run after the aggregation lands. — Added-by: Claude Opus 5 (session, Brett's
  direction) · 2026-08-26

## Conflicts

- **Working rule #1 is contradicted the moment this lands.** The aggregation's
  standing rule says domain-neutral contracts live ONLY in openxFactory. This
  topic moves two neutral contract families out of it. The reconciliation is an
  amendment in the same wave — "…or in a neutral open* product repo that
  openxFactory pins; domain repos never author neutral contracts" — but until
  that amendment exists the rule and this topic are flatly inconsistent, and the
  rule is the one currently in force. — Added-by: Claude Opus 5 (session,
  Brett's direction) · 2026-08-26
- **`docs/openxdox-naming.md` names `openxWallet` as a ratified family
  exception.** That record is `Status: ratified` and LOCKED 2026-08-13, and R1
  contradicts it directly. Amendment 2 is the resolution; until it is written,
  the ratified naming record says the opposite of the ruling. — Added-by: Claude
  Opus 5 (session, Brett's direction) · 2026-08-26
- **Two of the three descendant precedents are not ratified in this repo.**
  Checked 2026-08-26: `openspec/changes/create-medxchart-overlay-boundary/proposal.md`
  and `openspec/changes/create-medxpractice-overlay-boundary/proposal.md` both
  stand `Status: draft`. So the precedent table in claim 9 has ONE ratified
  member — DTN-022's openAvatar ruling of 2026-08-03 — and two changes in flight.
  The pattern is still the only pattern in the org and no counter-example exists,
  but a proposal that calls all three "ratified precedent" overstates the corpus.
  Noted, deferred: the `domain-descendant-boundary` delta should cite what each
  precedent actually IS. — Added-by: Claude Opus 5 (session, Brett's direction) ·
  2026-08-26
- **R2 freezes a name the org has decided is wrong.** The kind prefix stays
  `xfactory_wallet_*` in a repository that is no longer xFactory. That is
  deliberate — a rename in the move is unbisectable — but it ships a known-stale
  vocabulary into a brand-new repo's first release, and the deprecation window
  for the successor rename is not designed yet (see Q3). — Added-by: Claude Opus
  5 (session, Brett's direction) · 2026-08-26
- **The reader and the register end up in different repositories.** R6 keeps the
  register in openxFactory and moves its reader to openXwallet. This is the
  cheapest move and it satisfies "a grant with no reader in a required check
  confers nothing" — but it does split one contract's shape (the register is
  kindless; its schema exists only in the validator) across a repository
  boundary, which is the tension Q1 exists to resolve rather than a settled
  design. — Added-by: Claude Opus 5 (session, Brett's direction) · 2026-08-26

## Open questions

### Q1. Should the review-authority register be promoted to a wallet primitive, or should the reader be split back into openxFactory?

Context: R6 settles WHERE both live for the move — register in openxFactory,
reader travelling with the validator — but it explicitly leaves the durable shape
open as a council question. The register is kindless: its structure exists only
inside the validator's rule (u), `check_register` and `_load_attestations`. So
after the split, one repository holds the data and another holds its only schema.
Promoting the register to a wallet primitive would reunite them at the cost of
moving a file codexFactory's merge-gate floor pins by exact path. Splitting the
reader back would keep the data and its schema together in openxFactory at the
cost of a real refactor inside the validator and a second wallet-aware toolchain.
Recommended answer: neither, yet — carry the split as ruled, and put the question
to the council in the proposal rather than resolving it inside a move that must
stay byte-identical. If the council must lean, lean toward promoting the register
as a wallet primitive in a LATER change, once a second consumer of authority
registers exists; the reader-split option pays a refactor to avoid a boundary the
pin already makes auditable.
Explanation: the move's whole safety property is that its diff is provably empty.
Either resolution changes code or moves a gated path, so either one converts a
byte-identical extraction into a design change and loses the bisect guarantee.
And the argument for promotion gets stronger with a second consumer and weaker
without one, which is exactly the shape of a question that should wait.
Disposition status: open
Added-by: Claude Opus 5 (session, Brett's direction) · 2026-08-26

### Q2. Do the `tenants/ledgerxcorp/wallets/*` records move into `LedgerxWallet`, or stay in LedgerxFactory as tenant data?

Context: LedgerxFactory holds two wallet records, two grants, one distinct-holder
constraint and an exercise template. The template and the constraint sets are
plainly profile content and belong in the descendant under claim 10b. The RECORDS
are less clear: they are instances under a tenant path, and tenant data has its
own home conventions in Ledgerx that this topic does not know.
Recommended answer: the profile artifacts move; the tenant records stay put
unless Ledgerx rules otherwise. Either way this is Ledgerx's own ruling, made
inside the `LedgerxWallet` boundary change and not decided here.
Explanation: a descendant repo carries profiles, not instances — "pin and
profile, never fork" is about the SHAPE a domain declares, and a tenant's actual
wallet records are operating data. But the distinction between a profile and a
long-lived instance is exactly the kind of call the owning domain makes better
than the neutral layer, and getting it wrong from outside would relocate live
tenant data on an aesthetic argument.
Disposition status: open
Added-by: Claude Opus 5 (session, Brett's direction) · 2026-08-26

### Q3. What is the deprecation window for renaming the kind prefix `xfactory_wallet_*` to `openxwallet_*`?

Context: R2 freezes machine keys for v1, and names the prefix rename as a
successor. The rename touches every wallet artifact, LedgerxFactory pins five
kinds by name, and the validator's finding codes are pinned as strings elsewhere.
Nothing in the rulings says how long both spellings are accepted, whether the
validator accepts the old prefix with a warning or refuses it, or whether the
window is measured in releases or in consumers-migrated.
Recommended answer: a successor change in openXwallet that accepts BOTH prefixes
for exactly one bundle release — `wallet-v1.1` accepts either and warns on the
old, `wallet-v2.0` refuses the old — with the window closing on
consumers-migrated rather than on a date, since there is exactly one consumer and
"all consumers migrated" is a checkable fact here in a way a calendar is not.
Explanation: a dual-accept window is the only shape that lets a consumer
repository migrate on its own schedule without a synchronized cut, and pinning
the close to consumer count rather than a date avoids the failure where the
window expires while the single consumer is mid-review. The cost is one release
carrying two spellings, which is cheap while the consumer set is one.
Disposition status: open
Added-by: Claude Opus 5 (session, Brett's direction) · 2026-08-26

### Q4. When does `openXwallet-Install` become a real repository, and is Hermes its issuer host?

Context: the wallet has no runtime today — no issuer service, no key-custody
host, no deployment surface anywhere. Hermes is the natural issuer host and
currently carries zero wallet footprint. The lazy-descendant rule (claim 10d)
says a repository appears when it has content, not when it has a name.
Recommended answer: register the NAME in the naming record and create nothing.
`openXwallet-Install` becomes a repository on the day a runtime has an owner and
a first consumer — most likely when Hermes needs to issue rather than merely
verify — and not before.
Explanation: naming is cheap and prevents a second casing scheme appearing later
under time pressure; an empty install repo is a maintenance surface with a CI
budget and a CODEOWNERS entry and no content to protect. The whole wallet arc has
gated every successor on a consumer, and this is the same rule applied to a repo
instead of a capability.
Disposition status: open
Added-by: Claude Opus 5 (session, Brett's direction) · 2026-08-26

### Q5. What is openXwallet's own bundle-tag scheme?

Context: openxFactory versions its contract bundles `contract-vN.M` and the
wallet families were registered at `contract-v1.31`. Once the families live in
their own repository they need their own release identity, and the extraction
plan proposes `wallet-v1.0` for the first tag. Nothing settles what the numbers
MEAN — whether the major moves on a breaking key change, whether the minor tracks
requirement additions, or how a consumer's pin file expresses an acceptable range
(it currently expresses none: `pinned_by_commit_only` is the whole strictness).
Recommended answer: `wallet-vN.M` with the same semantics openxFactory's bundle
tags already carry — major on any breaking key or schema change, minor on
additive contract growth — and NO range expression in the pin: the pin stays
commit-and-digest, with the tag recorded as a human-readable label beside it
rather than as the thing being trusted.
Explanation: reusing the bundle-tag semantics the org already reads correctly is
worth more than a scheme that fits the wallet better in isolation. And keeping
the tag advisory while the digest is authoritative is the point of R4's
`pinned_by_commit_only` — a tag can be moved, a commit and a sha256 cannot, and
the moment a pin trusts a range the fail-closed property is gone.
Disposition status: open
Added-by: Claude Opus 5 (session, Brett's direction) · 2026-08-26

## Exit

One OpenSpec change, `split-openxwallet-repo`, declaring a code surface of
scripts, CI workflows, pin files and submodule gitlinks — so it archives only on
merged plus green realization evidence, never on landing alone. It carries the
two REMOVED capability deltas with their successor location recorded, the two
ADDED capabilities (the general descendant standard and the neutral-product-pin
strictness), the two MODIFIED deltas (custody registry resolved from the pin, and
the pinned reader inside a required consumer check), Amendment 2 to the naming
record, and the aggregation working-rule amendment. Speckit features follow per
phase: carve and scaffold the new repository and prove byte-identity before
tagging; consume and shed in one atomic pull request; aggregate the root
submodule; repoint consumers. The first domain descendant is `LedgerxWallet`, via
`create-ledgerxwallet-overlay-boundary`, on the descendant standard this change
ratifies. What must be true first: the eight rulings are recorded (done,
2026-08-26), the forward-compatible consumer finder has landed in LedgerxFactory,
and every open question above either carries a disposition other than `open` or
is explicitly carried into the change as a council question — Q1 is the one
expected to travel rather than resolve.

Exit TAKEN 2026-08-26. Proposed the same day as `split-openxwallet-repo`
(PR opensoft/openxFactory#391) and RATIFIED 2026-08-26 by Brett Heap, in session,
after both required checks on that pull request reported green — ratified AS
PROPOSED, with R1-R8 standing unchanged and Q1-Q5 carried at the change's design
dispositions (Q1, Q2 and Q3 travel; Q4 and Q5 decided). Realization proceeds
through Speckit features, one per `tasks.md` group in the design's Migration Plan
order, on the convener's standing rule that this house builds with Speckit rather
than `/opsx:apply`: OpenSpec ratified the boundary and Speckit builds it. The
first two features are the change's own remaining packet bookkeeping (Amendment 2
to `docs/openxdox-naming.md` and the xFactory working-rule #1 amendment) and
P5a.1, LedgerxFactory's three-candidate finder, which lands before the carve.
