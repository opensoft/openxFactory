---
code_surface: opensoft/LedgerxWallet (new), LedgerxFactory, xFactory aggregation — THREE repositories: a NEW repository, one consumer, and the aggregation's placement record. (1) `opensoft/LedgerxWallet` created EMPTY and scaffolded (it is not a carve — there is no history to preserve, see § Why), holding `contracts/openxwallet-pin.yaml` (`kind: ledgerxwallet_openxwallet_pin`, `relationship: pinned_upstream_composition`), a nested `openXwallet/` gitlink at the SAME commit, `README.md`, `CLAUDE.md`/`AGENTS.md`, `.github/CODEOWNERS`, the relocated profile (`templates/wallet-exercise.template.yaml`, `profile/distinct-holder-constraints/dhc-lx-create-post-01.yaml`, `tests/validate_wallet_estate.py`), a NEW `profile/custody-posture.yaml` (new, not a move — see Impact), and a branch-protection ruleset. (2) LedgerxFactory: `.gitmodules` gains a `LedgerxWallet` entry and a gitlink; `stack.yaml`'s DECLARED `openxwallet:` block (`:51-62`, landed by P5b at `1a8ec62`) is re-sourced from `openxFactory-nested-submodule-pin` to `LedgerxWallet-nested-submodule-pin` with its `contract_ref` unchanged; three profile paths are deleted; `tests/validate_wallet_estate.py` is REPLACED by a delegating bar entry of the same path so the `tests/validate_*.py` glob bar keeps covering the estate, and its two-candidate finder (`:53-78`) narrows to LedgerxWallet's own nested gitlink; `tests/validate_document_estate_surface.py`'s allowed-kind registration for `ledgerx_wallet_exercise_template` is amended because the artifact leaves the tree; `specs/016-posting-segregation-of-duties/runsheet.md:23` and `quickstart.md:15` are repointed because that live window is PREPARED-BUT-UNEXECUTED; `README.md`, `.github/CODEOWNERS` and `models/protected-surface.yaml`'s prose reference. Tenant estate records under `tenants/ledgerxcorp/wallets/` DO NOT MOVE (Q2). (3) The xFactory aggregation: NO change in v1 — the RATIFIED nested placement is taken and the `xFactories/` placement is deliberately not, so `.gitmodules` at the aggregation is untouched and that is a stated decision rather than an omission. Per `release-realization` this change archives ONLY on merged plus green realization evidence, never on landing.
target_release: implemented — each affected repository's own main line. NO release identity is allocated here: LedgerxWallet's first tag is `lxw-v1.0` cut at scaffold time in its own repository, openXwallet is CONSUMED at the already-published `wallet-v1.1` and not re-cut, and openxFactory publishes NOTHING in this change — no contract bundle, no `contracts/releases/<tag>.digests.yaml`, because no openxFactory-registered artifact is added, changed or removed. The only openxFactory tree change is this packet plus one README Records entry.
Status: draft
---
# Proposal: create-ledgerxwallet-overlay-boundary

Status: draft
Proposed: 2026-08-27 — **P6 of the ratified `split-openxwallet-repo`**, named by
this id in that change's § Successors named and again as its `tasks.md` 12.1,
on Brett's in-session ruling of 2026-08-27 over the successor set: verbatim,
"approved. do all of these". The five descendant rules this change instantiates
were ratified 2026-08-26 (PR opensoft/openxFactory#391); this change does not
re-litigate them and does not amend them. Registered under DTN-026, whose
resolution names `LedgerxWallet` as the first descendant (R8).

## Constraints carried, not questions asked

`split-openxwallet-repo` ratified `domain-descendant-boundary` with FIVE
requirements. They are the specification this change is measured against, and
this proposal's job is to instantiate them for one domain — not to reopen them.
Stated here in the form this change must satisfy, each with the ratified text's
own words:

1. **Consume through the descendant, never by direct integration.** "A
   DomainxFactory SHALL consume a neutral `open*` product through a
   `<Domainx><Product>` DESCENDANT repository and SHALL NOT integrate that
   product's contracts, schemas, corpus or validator directly into its own
   tree." The name takes the `<Domainx><Product>` form (R7: `LedgerxWallet`).
2. **Pin by commit, TWICE, in ONE commit.** A nested gitlink AND
   `contracts/<product>-pin.yaml` carrying
   `kind: <descendant_repo_snake>_<product_snake>_pin` and, where the pin covers
   a whole tree, `relationship: pinned_upstream_composition`; both change in the
   SAME commit; a disagreement between them REFUSES rather than prefers either.
3. **Profile, never fork.** "ONLY profiles, overlays, branding, deploy
   configuration and domain validators over its own profile artifacts" — and
   anything the profile cannot express is an UPSTREAM change in openXwallet,
   released and re-pinned, never a local edit.
4. **One of exactly two placements, whose STANDING differs and must be stated
   rather than blended.** RATIFIED: nested into its DomainxFactory (MedxAvatar
   in MedxFactory, DTN-022, 2026-08-03). REALIZED BUT NOT YET RATIFIED: the
   aggregation's `xFactories/` (MedxChart, whose establishing act
   `create-medxchart-overlay-boundary` is still `Status: draft`). Both MAY be
   carried, and then the two gitlinks must name the same commit.
5. **Created on its first profile, not before.** Lazily and consumer-gated, "so
   that an empty boundary is never stood up as precedent."

Rule 5 is why this change exists NOW and only for Ledgerx: the profile artifacts
already exist, in LedgerxFactory, today.

## Why

**LedgerxFactory is, today, in breach of rule 1 — and P5b narrowed the breach
without closing it.** `tests/validate_wallet_estate.py` resolves the neutral
openXwallet validator by walking UP OUT of its own checkout:
`VALIDATOR_CANDIDATES` (`:53-78`) holds path tuples and `find_openxfactory()`
(`:81-116`, the walk at `:109-116`) tries each of them at each of five
successive parent directories, with the result frozen at import time
(`VALIDATOR = find_openxfactory()`, `:119`). **After P5b — merged 2026-08-27,
LedgerxFactory PR #30 at `b131286`, Speckit feature
`019-openxwallet-consumer-repoints` — exactly TWO candidates remain, and BOTH
are in other repositories.** Candidate 1 is
`openxFactory/openXwallet/scripts/validate-openxwallet.py` — openxFactory's
nested gitlink; candidate 2 is `openXwallet/scripts/validate-openxwallet.py` —
the aggregation's root gitlink, which the aggregation does not yet carry (P4 is
open: `/home/brett/projects/xFactory/.gitmodules` pins `openAvatar` at root and
no `openXwallet`). The third, the pre-carve home, was dropped BY P5b and its
removal note is emphatic that restoring it would reintroduce a silent pass.

So the surface is now at its narrowest and it is still A PATH IN SOMEBODY ELSE'S
REPOSITORY, reached by directory adjacency. That is precisely "integrat[ing]
that product's … validator directly into its own tree" in the only form a
validator can be integrated: as a resolution rule. The finder's own comment
concedes what is at stake — "the aggregation's root gitlink is governed by
nothing this repo pins" — and answers it with candidate ORDER, which the comment
itself calls a tie-break ("Candidate order is what breaks the tie"). **P5b took
the narrowing as far as candidate pruning can take it; a descendant is what
replaces the tie-break with a pin.**

**The rule 5 gate is satisfied and no other domain's is.** The profile-kind
artifacts exist in LedgerxFactory now, verified on `origin/main` 2026-08-27:
`templates/wallet-exercise.template.yaml` (`kind:
ledgerx_wallet_exercise_template`, `instantiates:
xfactory_wallet_grant_exercise`), the distinct-holder constraint
`tenants/ledgerxcorp/wallets/dhc-lx-create-post-01.yaml` (`kind:
xfactory_wallet_distinct_holder_constraint`), the 822-line domain validator
`tests/validate_wallet_estate.py`, and the two wallet records plus two grants
that are the estate it checks. `MedxWallet`, `codexWallet`, `OpsxWallet` and
`AdxWallet` have no profile artifact of any kind, so rule 5 forbids creating
them and R7 already registers their names. This change creates exactly one
repository and argues for exactly one.

**The descendant makes "which reader ran" answerable by a pin instead of by a
directory walk.** Inside LedgerxWallet the nested `openXwallet/` gitlink sits at
a FIXED relative path, governed by `contracts/openxwallet-pin.yaml` in the same
commit. The five-level, three-candidate walk collapses to one deterministic
candidate whose commit is declared, which is the property
`neutral-product-pin`'s own requirement asks for in openxFactory's direction
("The consuming repository's pin is authoritative among reachable checkouts").
This change buys that property for the domain direction, and it is the concrete
benefit — not tidiness.

**There is no history to carve, and that is a material difference from P2.**
`split-openxwallet-repo`'s extraction was a `git filter-repo` path carve over
twelve path sets with a byte-identity floor, because eight registered
openxFactory artifacts and two promoted capabilities were moving out of a
governed corpus. Nothing of that kind moves here: the three relocating paths are
LedgerxFactory-authored, carry no openxFactory manifest row, appear in NO
`contracts/releases/*.digests.yaml`, and — verified — carry **no digest row in
`models/protected-surface.yaml`** (that file mentions
`validate_wallet_estate.py` once, at `:438`, in the PROSE of a `stack.yaml` pin
entry, and pins none of the three paths). So this is a plain `git mv` across a
repository boundary plus a scaffold, and the honesty obligation is a different
one: **preserve authorship provenance in prose**, because a fresh-repo scaffold
loses `git log`. Named as a task, not assumed.

**The precedent for the placement is the strongest one available and it is in
this domain's own tree.** LedgerxFactory already nests a descendant:
`.gitmodules` carries one entry, `path = LedgerxAvatar`, `url =
git@github.com:opensoft/LedgerxAvatar.git`. MedxFactory nests `MedxAvatar` the
same way. Both are DTN-022 realizations, and DTN-022 is the ONE ratified
descendant precedent the corpus has. Taking the ratified placement means this
change does not have to rest on `create-medxchart-overlay-boundary`, which is
`Status: draft` and which this packet uses only as a SHAPE template.

## What Changes

### 1. `opensoft/LedgerxWallet` is created and scaffolded

A new private repository under `opensoft`, created EMPTY (no carve, no
filter-repo, no history import), then scaffolded on `main` with:

- `contracts/openxwallet-pin.yaml` — `schema_version: 1`, `kind:
  ledgerxwallet_openxwallet_pin`, `relationship: pinned_upstream_composition`,
  `submodule_path: openXwallet`, `revision`/`revision_kind: commit`,
  `contract_bundle_tag: wallet-v1.1` as a LABEL beside the commit, and
  `repository: opensoft/openXwallet`. Shape follows the live descendant example
  `MedxChart/contracts/openchart-pin.yaml` (`kind: medxchart_openchart_pin`,
  the same six pin fields) because the ratified rule names it as one of the two
  it derives the kind form from. The other, `MedxAvatar/pins/openavatar.yaml`,
  is DELIBERATELY not followed: it lives at `pins/`, carries
  `source_repo`/`resolved_ref` and NO `relationship:`, and the ratified rule
  says the forward shape "SHALL NOT be read as retro-fitting" it.
- A nested `openXwallet/` submodule gitlink at the SAME commit as the pin
  file's `revision`, added in the SAME commit as the pin file.
- `README.md` (what the repository is, what it may and may not contain, the
  pin-bump procedure, and the authorship provenance of the relocated files),
  `CLAUDE.md` + `AGENTS.md` pointing at the user-global protocol per house
  style, `.github/CODEOWNERS` naming `@opensoft/xfactory` over
  `/contracts/`, `/profile/`, `/tests/` and `/.github/` (path-scoped, matching
  the style LedgerxFactory's own CODEOWNERS states and for the reason that file
  states: an org ruleset naming nobody requires nothing).
- A branch-protection ruleset created in EVALUATE mode and promoted to ACTIVE
  once its first check has reported, mirroring what P2 did for openXwallet.
- `lxw-v1.0` tagged after the profile lands and the estate run is green.

### 2. The profile relocates; the tenant estate does not

**MOVES into LedgerxWallet** — three paths, and the reason each is profile:

| From (LedgerxFactory) | To (LedgerxWallet) | Why it is profile |
| --- | --- | --- |
| `templates/wallet-exercise.template.yaml` | `templates/wallet-exercise.template.yaml` | A reusable INSTANTIATION STUB naming no tenant. Its own header states the domain rule set — presenting-key requirement, `custody_model_in_force` reading, `unattributed` for an unestablishable key, BC transport recorded as transport — which is the domain's interpretation of a neutral kind. |
| `tenants/ledgerxcorp/wallets/dhc-lx-create-post-01.yaml` | `profile/distinct-holder-constraints/dhc-lx-create-post-01.yaml` | Domain-wide policy MIS-FILED under a tenant path. It names no tenant, no wallet and no key: `declared_by: ledgerx:posting-segregation-of-duties`, `object_kind: purchase_invoice`, `comparison_basis: recorded_holder_of_prior_act`, `distinctness_floor: holder_id`. Creator≠poster holds for every Ledgerx estate, not for ledgerxcorp. The relocation CORRECTS the filing; it is not a re-scoping. |
| `tests/validate_wallet_estate.py` | `tests/validate_wallet_estate.py` | "A descendant adds a domain validator … that checks its own profile artifacts against the pinned product's schemas" is explicitly permitted by rule 3's third scenario. It carries the domain's own vocabulary as data — `ENVIRONMENT_EVIDENCING`, `PLATFORM_VERIFIABLE` (the measured BC 28.3 RSA-only family), `PIN_VERDICTS`, `EXPECTED_CONSTRAINT` — and the negative-probe corpora. |

**STAYS in LedgerxFactory** — and this is Q2's recommended disposition:

- `tenants/ledgerxcorp/wallets/{wal-lx-creator-01,wal-lx-poster-01}.yaml` and
  `{grant-lx-create-01,grant-lx-post-01}.yaml`. **Tenant data.** They carry
  holder ids (`agent:lx-ap-intake-creator`, `agent:lx-posting-agent`), DIDs
  (`did:web:xforge.us:wallets:lx-*`), key ids, `expires_at`, `issued_by`, and a
  `state:` that "is kept truthful by the session that closes each window". Their
  lifecycle is the tenant's live evidence window, not a pin bump. Moving them
  would put one tenant's identity estate inside a repository whose whole purpose
  is to be reusable across tenants — the exact inversion of the profile/instance
  line the descendant standard is built on.
- `schemas/holder-registry.schema.yaml` (`kind:
  ledgerx_wallet_holder_registry_contract`). **The platform seam.** Its
  counterparty is not openXwallet but Business Central: it declares the shape of
  LedgerLinc table 50200 "LL Wallet Holder Registry" and exists "so the repo and
  the client system state the same facts". This is R3's line applied one layer
  down — the product owns the standard, the factory keeps the seam.
- `specs/016-posting-segregation-of-duties/`,
  `specs/017-openxwallet-finder/`, `specs/018-openxwallet-pin-bump/`,
  `specs/019-openxwallet-consumer-repoints/`. **Records of acts LedgerxFactory
  performed.** Records are not relocated; the archive-record doctrine keeps a
  record where the act happened. Their PATH REFERENCES are a different matter —
  see the next sub-section.
- `models/protected-surface.yaml`, `tests/validate_document_estate_surface.py`,
  and the rest of the bar. LedgerxFactory's own governance surfaces.

**The enumeration is COMPLETE, and that is a checkable claim rather than a
hope.** `git grep '^kind:.*wallet'` over LedgerxFactory `origin/main` returns
EXACTLY SEVEN files: the exercise template
(`ledgerx_wallet_exercise_template`), the holder-registry contract
(`ledgerx_wallet_holder_registry_contract`), the distinct-holder constraint
(`xfactory_wallet_distinct_holder_constraint`), two grants
(`xfactory_wallet_grant`) and two wallet records (`xfactory_wallet_record`).
Two move, five stay, and the validator moves with them — nothing wallet-kinded in
that tree is unaccounted for above. Only two `ledgerx_wallet_*` kinds exist in
the whole repository, and both are named in this section.

### 2b. A PREPARED, UNEXECUTED live window points at a relocating path

`specs/016-posting-segregation-of-duties/runsheet.md` carries `Status: prepared
(this feature performs NONE of it)`, and its live window has NOT run: `## Phase 0
— preconditions` records P0.1 and P0.2 SATISFIED and the change's own README
entry says "What remains is the runsheet's live window (separately authorized;
open preconditions P0.4 … then phases 1-6)". The ratified change that owns it,
`modify-ledgerx-posting-authority-for-segregation-of-duties`, is still ACTIVE in
LedgerxFactory's OpenSpec instance and archives on that window's 6.3.

**And the runsheet reaches the relocating template by a RELATIVE LINK.** At
`runsheet.md:23`: "Record shapes: exercise records instantiate
[templates/wallet-exercise.template.yaml](../../templates/wallet-exercise.template.yaml)".
A `git mv` across the repository boundary makes that link dangle in an
operational procedure whose operator is Brett, whose actors include an ADMIN and
an OPSX lane, and whose steps mint real keys. `runsheet.md:174` also names
`dhc-lx-create-post-01`, but BY ID rather than by path, so that reference
survives the move; the template link does not. `quickstart.md:15` in feature 016
likewise invokes the validator by a relative path.

**This is a second sequencing constraint, and it is not P5b's.** The profile move
SHALL NOT interleave with an open live window: either the window has closed and
`modify-ledgerx-posting-authority-for-segregation-of-duties` has archived, OR the
runsheet's and quickstart's paths are repointed IN THE SAME COMMIT as the move
and the window's operator is told. This proposal recommends the second — waiting
on P0.4 would park P6 behind a decision it does not own — and makes the repoint a
task rather than an assumption. It is the one place where a topology change can
break something that is about to be *performed*, rather than something that is
merely read.

### 3. LedgerxFactory keeps the bar entry, delegating instead of duplicating

LedgerxFactory has **no GitHub Actions workflow at all** — `.github/` holds
`CODEOWNERS` and `copilot-instructions.md` and nothing else (verified on
`origin/main`). Its estate is enforced by a HUMAN-RUN GLOB, written down at
`docs/protected-surface.md:62`:

```sh
for f in tests/validate_*.py; do python3 "$f" || echo "FAIL $f"; done
```

**So a plain `git mv` of `tests/validate_wallet_estate.py` silently removes the
wallet estate from the only bar that ever checks it.** There is no required
check to repoint, which makes this quieter than a CI break, not safer. The
change therefore keeps `tests/validate_wallet_estate.py` AT ITS PATH as a THIN
DELEGATING ENTRY — not a copy — which resolves
`LedgerxWallet/tests/validate_wallet_estate.py` from the LedgerxFactory root,
invokes it with this tree as the declared estate root, and propagates its exit
code. If the `LedgerxWallet` submodule is uninitialized the entry REFUSES with a
named exit and a remediation string naming `git submodule update --init
LedgerxWallet` — never a skip, on LedgerxFactory's own 2026-08-07 repo law that
"an unreadable surface must fail, not degrade to 'empty'". One implementation
lives in LedgerxWallet; the bar's glob contract is unbroken; nothing is forked.

### 4. The moved validator gains a declared estate root

The validator's scan target — `tenants/ledgerxcorp/wallets/` — stays in
LedgerxFactory while the validator moves. This is R6's shape one layer down (the
register stayed in openxFactory; its READER travelled with the validator), and
it is handled the same way: by a declared scan target rather than by a walk. The
validator takes the estate root explicitly, defaults to `..` when it is nested
at `LedgerxFactory/LedgerxWallet`, and REFUSES with a named exit when the estate
root holds no `tenants/*/wallets/` directory.

**The estate root has THREE jobs, and naming only the first would have made this
move break silently.** Beyond the estate scan, the validator (a) opens
`os.path.join(REPO, "stack.yaml")` and reads
`yaml.safe_load(fh)["xfactory"]["contract_ref"]` inside
`check_pin_reconciliation()` — a file LedgerxWallet has no business owning — and
(b) runs a SECOND five-level upward walk, `find_aggregation()` (`:583-594`),
hunting a `.gitmodules` that mentions `openxFactory` so it can extract the
PINNED relocation emitter (`git -C <openx> show <pin>:scripts/check-openxfactory-pin.py`,
`:688`) and run it against this repository. That leg is not incidental: the
parent's ratified `tasks.md` 6.2 makes this bar the ONLY observer of the
deprecation window, so dropping it would un-observe an obligation another change
depends on. All three reads re-base on the declared estate root, the second walk
STARTS from it so nesting does not silently spend one of its five levels, and
each of the three gets its own refusal naming which surface was unreadable.
`design.md` D5 carries the enumeration.

Its `EXPECTED_WALLETS` and
`EXPECTED_GRANTS` sets — which today hard-code `wal-lx-creator-01`,
`wal-lx-poster-01`, `grant-lx-create-01`, `grant-lx-post-01` — move OUT of the
profile validator and into an estate-side declaration that the validator READS,
because one tenant's wallet ids inside a cross-tenant profile is the same
inversion § 2 refuses for the records themselves.

### 5. The pin agrees three ways, on a declaration P5b has already landed

**P5b IS MERGED** — LedgerxFactory PR #30, merge commit `b131286`, the work
commit `1a8ec62` "P5b: the dead finder candidate goes, and the wallet pin becomes
a declaration", Speckit feature `019-openxwallet-consumer-repoints`, 2026-08-27.
That was this change's one hard precondition and it is discharged: P6 now amends
a DECLARED pin rather than inventing one, and narrows a finder nobody else is
concurrently editing. What P5b left in `stack.yaml` is a sibling `openxwallet:`
block (`:51-62`) mirroring `xfactory:` field for field —
`contract_repo: github.com/opensoft/openXwallet`, `contract_ref_type: commit`,
`contract_ref: 63f5a1adac89f017e70bab9a4ffe7cf02d6e6705`,
`contract_bundle_tag: wallet-v1.1`, `contract_declared_at: "2026-08-27"`,
`contract_source: openxFactory-nested-submodule-pin` — under a comment block
that states its own derivation: "it is openxFactory's nested `openXwallet`
gitlink at contract-v2.0, which agrees with the `commit:` field of that
release's contracts/openxwallet-pin.yaml". **That derivation is exactly what this
change replaces**, because after P6 the domain consumes through its descendant
and not through openxFactory's gitlink. The invariant this change introduces and
owes a check:

> **LedgerxFactory's DECLARED `stack.yaml` `openxwallet.contract_ref` = LedgerxWallet's `contracts/openxwallet-pin.yaml` `revision` = LedgerxWallet's nested `openXwallet` gitlink commit.** Three declarations of one commit, and a disagreement REFUSES rather than picking a winner.

`contract_source:` moves from `openxFactory-nested-submodule-pin` to
`LedgerxWallet-nested-submodule-pin`, because after this change the descendant IS
how the domain consumes the product — that is rule 1 — and a `contract_source`
naming openxFactory's gitlink would describe a consumption path the tree no
longer takes. `contract_ref` itself does NOT change: openXwallet's `wallet-v1.1`
is an ANNOTATED tag (`021cdeef…`) dereferencing to commit
`63f5a1adac89f017e70bab9a4ffe7cf02d6e6705`, which is also openXwallet's `main`
HEAD and what openxFactory's own `contracts/openxwallet-pin.yaml` pins today —
so the pin task must resolve `wallet-v1.1^{commit}` and never the bare tag name.
Re-pointing the pin and re-homing it in the same act would make the change
unbisectable. **Agreement with openxFactory's pin is the STARTING state, not an
invariant:** LedgerxWallet and openxFactory are independent consumers of the
same product, governed by different pins, and may legitimately diverge later.
Such a divergence is NOT an error and is checked by nothing — stated that way
deliberately, because an earlier draft of this section said it would be
"REPORTED" and named no reporter, which is the LS-A3 shape. After this change
the commit that governs the Ledgerx estate is the one LedgerxWallet pins, and
that is the whole of the claim. What IS checked is the three-way agreement above,
by the delegating bar entry, before it invokes anything.

### 6. Placement: nested only, and the aggregation is untouched

LedgerxWallet is nested at `LedgerxFactory/LedgerxWallet` — the RATIFIED
placement, on the DTN-022 precedent this domain already realizes for
`LedgerxAvatar`. The aggregation's `xFactories/` placement is **deliberately not
taken in v1**: the descendant has no standalone-cloning need (its only consumer
is the tree it is nested in), and the `xFactories/` placement's standing is
REALIZED-BUT-NOT-YET-RATIFIED until `create-medxchart-overlay-boundary`
archives. If it is added later, the ratified rule already binds the follow-on:
both gitlinks must name the same commit. The new LedgerxFactory `.gitmodules`
section is named `LedgerxWallet`, matching its path — noted because the existing
entry's section name is `ledgerXavatar` against a path of `LedgerxAvatar`, and
this change does not propagate that mismatch.

## Capabilities

### New Capabilities

- **`ledgerxwallet-overlay-boundary`** — the repository, pin and profile
  contract for the FIRST domain descendant created under
  `domain-descendant-boundary`: that LedgerxWallet is the only path by which
  the Ledgerx domain consumes openXwallet; that the pin is declared twice and
  agrees three ways with the domain's `stack.yaml`; that the profile relocates
  while the tenant estate stays; and that the estate's coverage by
  LedgerxFactory's glob bar survives the move by delegation rather than by
  duplication.

### Modified Capabilities

- None. `domain-descendant-boundary` and `neutral-product-pin` are ratified by
  `split-openxwallet-repo` and **not yet promoted into `openspec/specs/`** —
  verified 2026-08-27: `openspec/specs/` holds 52 capabilities and neither of
  those two is among them, because that change archives only on merged plus
  green realization evidence. This change therefore cites them as
  RATIFIED-IN-CHANGE and issues no delta against them. It does not amend them,
  and if the bench wants one of its rules changed, that is an amendment to
  `split-openxwallet-repo`, not a requirement here.

## Impact

- **A new repository exists that did not.** `opensoft/LedgerxWallet` does not
  exist today (verified 2026-08-27: `gh repo view opensoft/LedgerxWallet` →
  "Could not resolve to a Repository"). Creating it, its ruleset, and its first
  tag are `[OPERATOR]` acts and are marked as such.
- **`profile/custody-posture.yaml` is NEW, not a move, and is named as such.**
  The Ledgerx wallet custody posture — `custody.model: holder_readable`,
  environment-evidencing, authority ceiling `act`, "the audit record says
  'environment', never 'holder'" — exists today ONLY in YAML COMMENTS inside the
  two wallet records and in the ratification prose of
  `modify-ledgerx-posting-authority-for-segregation-of-duties` (2026-08-08).
  There is no custody policy artifact in LedgerxFactory: `policies/` holds eight
  files and none is wallet custody; `docs/` holds twenty-one and none is either.
  Declaring the posture as a profile artifact is permitted (it is profile, not
  fork) and is worth doing in the same act that creates the profile's home — but
  it is a NEW ARTIFACT and this proposal does not launder it as a relocation.
  The bench may cut it to a successor with no other consequence.
- **A registered kind loses its artifact.**
  `tests/validate_document_estate_surface.py` maintains an allowed-kinds list
  that registers `ledgerx_wallet_exercise_template` with a CHK002 note
  ("RED-confirmed 2026-08-08 … on the staged
  `templates/wallet-exercise.template.yaml`"). When the template leaves the
  tree, that registration names an artifact that is gone. Amending it is a task
  in this change; leaving it would be a stale registration in a surface gate,
  and the surrounding entries show that file treats its registrations as
  load-bearing.
- **`models/protected-surface.yaml` needs a prose amendment only.** Verified: it
  carries NO digest row for any of the three moved paths; the single wallet
  mention at `:438` is inside the narrative of a `stack.yaml` pin entry
  ("RED-proven by `validate_wallet_estate.py`'s platform-verifiability pin
  before the flip"). That sentence stays TRUE as history; what changes is where
  the named file lives, so the amendment is a pointer, not a re-pin.
- **Authorship provenance is lost by `git log` and must be kept in prose.** The
  three moved files were authored under
  `modify-ledgerx-posting-authority-for-segregation-of-duties` (ratified
  2026-08-08) and amended by Speckit features 016/017/018. A fresh-repo scaffold
  carries none of that history. LedgerxWallet's `README.md` records the origin
  repository, the authoring change, the Speckit features, and the commit each
  file came from.
- **P5b, this change's one precondition on another packet, is DISCHARGED**
  (LedgerxFactory PR #30, `b131286`, 2026-08-27). The remaining precondition is
  LedgerxFactory's OWN: the feature-016 live window, handled by § 2b as a
  same-commit repoint rather than by waiting.
- **Two other wave items are open and neither gates P6.** P4 — the aggregation's
  root `openXwallet` gitlink — is not landed (`/home/brett/projects/xFactory/.gitmodules`
  carries `openAvatar` at root and no `openXwallet`), and P3b — codexFactory's
  merge-gate floor — is codexFactory's. P6 touches neither surface. Stated so the
  bench does not have to check.
- **Two openxFactory files change and nothing else.** This packet and one
  README "OpenSpec Records" entry. No contract, no schema, no manifest row, no
  release surface, no validator.

## Successors named

- **`MedxWallet`, `codexWallet`, `OpsxWallet`, `AdxWallet`** — each lazily, on
  its domain's first wallet profile artifact (R7/R8 and rule 5). None has one
  today; the names are registered and no repository is created.
- **The `xFactories/LedgerxWallet` aggregation placement** — if and when
  standalone cloning is actually needed, and on the ratified both-placements
  rule that the two gitlinks then name the same commit.
- **The `xfactory_wallet_*` → `openxwallet_*` kind-prefix rename** (Q3 of the
  parent, owned by openXwallet). LedgerxWallet's profile pins those kind
  strings by name, so it becomes a second re-pin site. Recorded so the
  successor's blast radius is known, not owned here.
- **A REQUIRED check for the three-way pin agreement.** LedgerxFactory has no
  GitHub Actions workflow at all, so what this change builds is RUNNING CODE in a
  HUMAN-RUN bar — the delegating entry reads all three declarations and refuses
  on any disagreement before invoking anything — and NOT a required check. The
  distinction is stated rather than blurred: a control described but not wired is
  the failure LS-A3 exists to forbid, and the honest form of this claim is "a bar
  anyone can run, that fails loudly, whose absence from CI is a successor".
  Giving LedgerxFactory its first workflow is that successor and is bigger than
  this change.
- **Governed-repo recognition for a NESTED descendant.** openxFactory's
  enumerations key on `xFactories/<Name>`, and the parent's P4b widens them by an
  allowlist of ROOT-LEVEL neutral products — neither admits a nested gitlink. So
  a nested-only `LedgerxWallet` is outside the notebook projection and the
  ideation routing, exactly as `MedxAvatar` has been for five months under the
  same ratified placement. Accepted here because the descendant carries no
  ideation corpus; the remedy, if it ever does, is the `xFactories/` gitlink or a
  nested-descendant widening, and either is a separate change.

## Out of scope, deliberately

- **Moving `tenants/ledgerxcorp/wallets/{wal-*,grant-*}`.** Q2's recommended
  disposition is that they stay; the bench decides.
- **Any content change to the moved files beyond the mechanical three:** the
  DHC's new path, the validator's declared estate root, and the expected-set
  extraction. No rule is added, removed or re-worded, and the negative-probe
  corpora are byte-unchanged.
- **Any change to openXwallet.** It is consumed at the published `wallet-v1.1`
  and not re-cut. Anything the profile cannot express is an upstream change
  there — rule 3 — and this change finds nothing of the kind.
- **Any change to the aggregation.** § 6.
- **The LedgerLinc / BC enforcement half.** The extension's posting surface,
  table 50200 and the holder registry are the platform seam and stay.
- **Re-widening the finder.** P5b narrowed it to two candidates and its removal
  note forbids restoring the third. This change narrows it further — to
  LedgerxWallet's own nested gitlink, one deterministic candidate, no upward walk
  — and adds no candidate back.
- **Promoting `domain-descendant-boundary` into `openspec/specs/`.** That
  happens when `split-openxwallet-repo` archives, on its own realization
  evidence.

## Open questions

**Q2 (carried from the parent, its one open question) — do
`tenants/ledgerxcorp/wallets/*` move into LedgerxWallet, or stay as tenant
data?** `split-openxwallet-repo`'s ratification record carries Q2 forward
explicitly: "Stays for `create-ledgerxwallet-overlay-boundary` (P6); the
profile/instance line is the owning domain's call."

**Recommendation: STAY in LedgerxFactory as tenant data, while LedgerxWallet
carries the PROFILE** — the exercise template, the distinct-holder constraint
set, the estate validator, and the declared custody posture. The line is
profile-versus-instance, and the four estate records fall on the instance side
on their own contents: holder ids, DIDs, key ids, `expires_at`, `issued_by`, and
a `state:` field whose truthfulness is maintained per live evidence window.
A profile repository holding one tenant's identity estate would be reusable by
construction and un-reusable in fact. The counter-case is real and worth stating:
keeping them apart means the validator and its scan target live in two
repositories, which § 4 pays for with a declared estate root and § 3 pays for
with a delegating bar entry. That is two seams accepted to keep the
profile/instance line clean — and the alternative (move everything) buys one
repository at the cost of making the second Ledgerx tenant a fork question.

**This is the one question this proposal carries.** Everything else is either a
ratified constraint or a decision this packet takes and defends.
