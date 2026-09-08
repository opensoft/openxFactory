---
code_surface: opensoft/LedgerxWallet (new), LedgerxFactory, openxFactory — THREE repositories. (1) `opensoft/LedgerxWallet` created EMPTY and scaffolded (not a carve — there is no history to preserve): `contracts/openxwallet-pin.yaml` (`kind: ledgerxwallet_openxwallet_pin`, `relationship: pinned_upstream_composition`), a nested `openXwallet/` gitlink at the SAME commit in the SAME commit, `tests/validate_pin.py` (the refusing validator the ratified rule's own scenarios require), `README.md` with the relocated file's provenance, `CLAUDE.md`/`AGENTS.md`, `.github/CODEOWNERS`, `.github/workflows/pin-validation.yml`, a branch-protection ruleset, and the relocated `templates/wallet-exercise.template.yaml`. (2) LedgerxFactory: `.gitmodules` + a `LedgerxWallet` gitlink; `tests/validate_wallet_estate.py`'s two-candidate upward walk (`:53-78`, `:81-116`) REPLACED by one fixed relative path into the descendant — the validator STAYS; `stack.yaml`'s declared `openxwallet:` block (`:51-62`) re-sourced; `models/protected-surface.yaml`'s `stack.yaml` DIGEST re-pinned (`:384-388`) plus its prose pointer at `:455`; `templates/wallet-exercise.template.yaml` deleted; `tests/validate_document_estate_surface.py`'s kind registration (`:1116-1121`) and its resolution-path comment (`:1086-1098`) amended; `specs/016-posting-segregation-of-duties/{runsheet.md:22-23, quickstart.md:3-7 and :19}` repointed with a new P0.5 precondition; `README.md`; `.github/CODEOWNERS` gains `/.gitmodules` and `/LedgerxWallet`. The tenant estate and the distinct-holder constraint DO NOT MOVE (Q2, and § 2b). (3) openxFactory: this packet plus one README "OpenSpec Records" row — no contract, no schema, no manifest row, no release surface, no validator. The xFactory aggregation is deliberately UNTOUCHED (§ 6), which is a decision and not a surface. Per `release-realization` this change archives ONLY on merged plus green realization evidence, never on landing.
target_release: implemented — each affected repository's own main line. NO release identity is allocated here: LedgerxWallet's first tag `lxw-v1.0` is cut in its own repository, openXwallet is CONSUMED at the already-published `wallet-v1.1` and not re-cut, and openxFactory publishes NOTHING — no contract bundle and no `contracts/releases/<tag>.digests.yaml`, because no openxFactory-registered artifact is added, changed or removed.
Status: ratified
---
# Proposal: create-ledgerxwallet-overlay-boundary

Status: ratified
Ratified: 2026-08-28 by Brett Heap (openxFactory operator authority) — in-session
ruling ("ratify #449") on PR #449 with both checks green. Realization proceeds
per tasks.md through Speckit features, §3 (create and scaffold) first.
Proposed: 2026-08-27 — **P6 of the ratified `split-openxwallet-repo`**, named by
this id in that change's § Successors named and again as its `tasks.md` 12.1, on
Brett's in-session ruling of 2026-08-27 over the successor set: verbatim,
"approved. do all of these". The five descendant rules this change instantiates
were ratified 2026-08-26 (PR opensoft/openxFactory#391); this change does not
re-litigate and does not amend them. Registered under DTN-026, whose resolution
names `LedgerxWallet` as the first descendant (R8).

**This proposal was narrowed by its own alignment review.** As first authored it
relocated the estate validator and the distinct-holder constraint as well. Both
were withdrawn on findings that are arithmetic rather than aesthetic, and § 2b
records why — because the withdrawn version is the one a reader would otherwise
reinvent.

## Ratification record, 2026-08-28

Recorded from the convener's in-session ruling, taken after PR #449's required
checks reported green (`pytest-suite` 15m14s, `wallet-validation` 21s): verbatim,
**"ratify #449"**. Four things this record fixes, in the order they bind:

1. **RATIFIED AS PROPOSED — meaning the NARROWED v1, not the packet as first
   authored.** What is ratified is the version this file now describes: the
   descendant is created with **the pin declared twice in one commit**, **one
   profile artifact** (`templates/wallet-exercise.template.yaml`), and **a
   four-check pin validator plus its workflow** — where the fourth check reads the
   CHECKED-OUT `openXwallet/` revision and cleanliness, because a pin whose
   verifier reads only the recorded declarations lets a fork at another commit
   execute while all three agree. **The tenant estate, the distinct-holder
   constraint and `tests/validate_wallet_estate.py` STAY in LedgerxFactory.** Only
   the validator's RESOLUTION moves — `VALIDATOR_CANDIDATES` and its five-level
   walk collapse to one fixed path into the descendant — because ratified rule 1
   binds the resolution path and not the file's address, and that file is
   LedgerxFactory-authored rather than the product's. The RESTRUCTURE the
   adversary seat returned was TAKEN before this ratification, not argued down;
   ratifying "as proposed" ratifies the taken restructure.
2. **Q2 IS RULED: STAY.** `tenants/ledgerxcorp/wallets/*` remain in
   LedgerxFactory as tenant data. The parent carried this question forward
   explicitly to P6 as "the owning domain's call", and it is now made, on the
   three grounds § Open questions records: the records are instance-shaped on
   their own contents (holder ids, DIDs, key ids, `expires_at`, live `state:`); a
   nested descendant's YAML is PRUNED from openXwallet's own sweep
   (`sweep_candidates`, `validate-openxwallet.py:2063`), so relocating them would
   move them OUT of adjudication rather than into a boundary; and those five files
   are the commit target of the runsheet's **unexecuted Phase 3.4**, a procedure
   that mints real keys. **Q2 is closed and does not travel to another change.**
3. **The custody-posture cut STANDS.** No `profile/custody-posture.yaml` is
   authored here. It remains a named successor, which decides its reader and its
   home together — and under LedgerxFactory's own rules an ENFORCED posture
   belongs in the digest-protected `policies/` rather than an unprotected
   `profile/` tree.
4. **The nested-only placement's governed-enumeration gap STANDS, as a registered
   successor.** A nested descendant is outside every governed-repo enumeration in
   the corpus — `sync-notebooklm-books.py`'s `xFactories/<Name>` match and its
   `in_nested_checkout()` exclusion, and `ideation_routing.py`'s
   `_governed_repo_ids` — before the parent's P4b widening and after it. The
   ratified precedent (`MedxAvatar`, `LedgerxAvatar`) already sits in it. This
   ratification accepts the gap with its cost named rather than closing it, and
   the remedy stays a separate change.

The merge of PR #449 is the convener's own act and is NOT performed by this
record, which lands on `change/create-ledgerxwallet-overlay-boundary` ahead of it.
Realization — the repository creation, the nesting, the move — is Speckit work
that begins after this ratification, and per `release-realization` this change
archives only on merged plus green realization evidence, never on landing.

## Constraints carried, not questions asked

`split-openxwallet-repo` ratified `domain-descendant-boundary` with FIVE
requirements. They are the specification this change is measured against; its job
is to instantiate them for one domain.

1. **Consume through the descendant, never by direct integration.** "A
   DomainxFactory SHALL consume a neutral `open*` product through a
   `<Domainx><Product>` DESCENDANT repository and SHALL NOT integrate that
   product's contracts, schemas, corpus or validator directly into its own tree."
   Name form `<Domainx><Product>` (R7: `LedgerxWallet`).
2. **Pin by commit, TWICE, in ONE commit** — a nested gitlink AND
   `contracts/<product>-pin.yaml` with
   `kind: <descendant_repo_snake>_<product_snake>_pin` and
   `relationship: pinned_upstream_composition`; a disagreement REFUSES.
3. **Profile, never fork** — "ONLY profiles, overlays, branding, deploy
   configuration and domain validators over its own profile artifacts".
4. **One of exactly two placements, whose STANDING differs and must be stated
   rather than blended.** RATIFIED: nested in the DomainxFactory (MedxAvatar in
   MedxFactory, DTN-022). REALIZED BUT NOT YET RATIFIED: the aggregation's
   `xFactories/` (MedxChart, whose establishing act
   `create-medxchart-overlay-boundary` is `Status: draft`,
   `target_release: implementation_pending`).
5. **Created on its first profile, not before** — lazily, consumer-gated, "so
   that an empty boundary is never stood up as precedent."

## Why

**The breach rule 1 describes is a RESOLUTION PATH, and P5b narrowed it without
closing it.** `tests/validate_wallet_estate.py` reaches the neutral openXwallet
validator by walking UP OUT of its own checkout: `VALIDATOR_CANDIDATES`
(`:53-78`) holds path tuples, `find_openxfactory()` (`:81-116`, walk at
`:109-116`) tries each at five successive parents, and the result is frozen at
import (`VALIDATOR = find_openxfactory()`, `:119`). After P5b — merged 2026-08-27,
LedgerxFactory PR #30 at `b131286`, work commit `1a8ec62`, Speckit feature
`019-openxwallet-consumer-repoints` — exactly TWO candidates remain and BOTH are
paths in other repositories: `openxFactory/openXwallet/scripts/validate-openxwallet.py`
and the aggregation's root `openXwallet/scripts/validate-openxwallet.py` (which
the aggregation does not yet carry — P4 is open;
`/home/brett/projects/xFactory/.gitmodules` pins `openAvatar` at root and no
`openXwallet`). The third, the pre-carve home, was dropped BY P5b under a note
that restoring it would reintroduce a silent pass.

**A second breach site sits in the same repository and the first draft of this
proposal misread it.** `specs/016-posting-segregation-of-duties/quickstart.md:19`
invokes `python3 ../../openxFactory/openXwallet/scripts/validate-openxwallet.py . --strict`
— the NEUTRAL validator, by relative path, out of another repository's checkout —
and `:3-7` names "the pinned openxFactory checkout at the workspace root, with
its nested `openXwallet` gitlink initialized" as a prerequisite. That is the same
adjacency reach as the finder, written into a procedure a human follows.

So the surface is at its narrowest and is still adjacency, in two places. That is
"integrat[ing] that product's … validator directly into its own tree" in the only
form a validator can be integrated: as a resolution rule. The finder's own
comment concedes the stake — "the aggregation's root gitlink is governed by
nothing this repo pins" — and answers it with candidate ORDER, which the comment
itself calls a tie-break ("Candidate order is what breaks the tie"). **P5b took
candidate pruning as far as it goes; a descendant is what replaces the tie-break
with a pin.**

**This is not theoretical — the silent pass is observable in this workspace
today.** `openxFactory/openXwallet` does not exist here and the aggregation
carries no root `openXwallet`, so on the committed post-P5b finder
`find_openxfactory()` returns `None` and the bar exits 1, loudly and correctly.
But the local openxFactory checkout still carries the SHED
`scripts/validate-openxwallet.py` on disk, and the pre-P5b finder resolves it and
reports `WALLET ESTATE: PASS` — a green run against a contract version nothing
pins. After P6 that failure mode is unavailable by construction: there is exactly
ONE candidate, it lives inside the descendant, and its commit is declared twice.

**The rule 5 gate is satisfied and no other domain's is.** The profile-kind
artifact exists in LedgerxFactory now:
`templates/wallet-exercise.template.yaml`, `kind:
ledgerx_wallet_exercise_template`, `instantiates: xfactory_wallet_grant_exercise`
— the domain's own profile of a neutral product kind. `MedxWallet`,
`codexWallet`, `OpsxWallet` and `AdxWallet` have none, so rule 5 forbids creating
them; R7 already registers their names.

**The placement precedent is in this domain's own tree.** LedgerxFactory already
nests a descendant: `.gitmodules` carries one entry, `path = LedgerxAvatar`,
`url = git@github.com:opensoft/LedgerxAvatar.git`. MedxFactory nests `MedxAvatar`
the same way (`46f595c6`, 2026-08-23). Both are DTN-022 realizations — the ONE
ratified descendant precedent the corpus has — so this change need not rest its
placement on `create-medxchart-overlay-boundary`, which is `Status: draft` and
which this packet uses only as a SHAPE template.

## What Changes

### 1. `opensoft/LedgerxWallet` is created and scaffolded

Private, created EMPTY — no carve, no `filter-repo`, no history import — then
scaffolded on `main`:

- **`contracts/openxwallet-pin.yaml`** — `schema_version: 1`,
  `kind: ledgerxwallet_openxwallet_pin`, and a `pin:` mapping holding
  `repository: opensoft/openXwallet`,
  `remote: git@github.com:opensoft/openXwallet.git`, `revision: <40-hex>`,
  `revision_kind: commit`, `submodule_path: openXwallet`,
  `relationship: pinned_upstream_composition`, plus
  `contract_bundle_tag: wallet-v1.1` as a LABEL beside the commit.
  **Shape, stated precisely rather than by gesture.** `MedxChart/contracts/openchart-pin.yaml`
  nests its six fields under a `pin:` mapping (`:4-10`); this file follows that
  NESTING and carries five of MedxChart's six (`repository`, `remote`, `revision`,
  `submodule_path`, `relationship`), DROPS `source_path` because
  `relationship: pinned_upstream_composition` already says the pin covers the
  whole tree, and ADDS `revision_kind` and `contract_bundle_tag` because the
  ratified rule forbids a tag as the referent and a label needs to be marked as
  one. `MedxAvatar/pins/openavatar.yaml` is deliberately NOT followed — it lives
  at `pins/`, carries `source_repo`/`resolved_ref` and no `relationship:`, and
  the ratified rule settles the shape "FORWARD only" and says the live
  disagreement "SHALL NOT be read as retro-fitting them". The KIND takes
  `medxchart_openchart_pin`'s compressed form rather than
  `medx_avatar_openavatar_pin`'s underscored one; the rule names both, the corpus
  disagrees with itself, and the compressed form matches the directory the rule
  itself names.
- A **nested `openXwallet/` gitlink** at the same commit, in the SAME commit.
- **`tests/validate_pin.py`** — the refusing validator rule 2's own scenarios
  require ("the descendant's OWN VALIDATOR REFUSES the tree rather than
  preferring either"). It asserts `git ls-tree HEAD openXwallet` equals the pin's
  `revision`, that `revision` is 40 hex and no bare tag stands in for it, and
  fails closed with a named exit and the remediation string. Without it the
  descendant would ship the refusal DECLARED and nothing that refuses.
- **`.github/workflows/pin-validation.yml`** running it — because a
  branch-protection ruleset cannot be promoted from EVALUATE to ACTIVE until some
  check has reported, and nothing else in this change creates one.
- `README.md` (what the repository may and may not contain, the pin-bump
  procedure, and the relocated file's provenance), `CLAUDE.md`/`AGENTS.md` per
  house style, `.github/CODEOWNERS` naming `@opensoft/xfactory` path-scoped over
  `/contracts/`, `/templates/`, `/tests/` and `/.github/`.
- `lxw-v1.0` tagged after the template lands and `validate_pin.py` is green.

### 2. What moves: the exercise template, and nothing else

`templates/wallet-exercise.template.yaml` relocates to LedgerxWallet at the same
relative path. It is the domain's reusable instantiation stub for a neutral kind,
it is the artifact that satisfies rule 5's creation gate, and — decisively — it
is the ONE wallet-adjacent artifact whose move breaks nothing, for a reason its
own header states: it "deliberately carries a template kind instead, because the
wallet validator's repo scan adjudicates any wallet-kind YAML as a live record
and a placeholder record must not be one." Not being adjudicated is its design,
so relocating it removes nothing from adjudication.

**It is not tenant-free, and the first draft wrongly said it was.** The template
enumerates this tenant's live ids as placeholder GUIDANCE inside angle brackets —
`grant_ref` at `:24`, `presenting_key_ref` at `:34`, `wallet_ref` at `:38`,
`holder_ref` at `:39`, `constraint_ref: dhc-lx-create-post-01` at `:48` — and
`:4` points instances at `tenants/ledgerxcorp/ledger-estates/`. Those are strings
in a stub, not declared facts, and this proposal says so rather than claiming a
tenant-freedom the file does not have. The spec's refusal is scoped to RECORDS
accordingly.

### 2b. What does NOT move, and the two withdrawn relocations

**The tenant estate stays** —
`tenants/ledgerxcorp/wallets/{wal-lx-creator-01,wal-lx-poster-01,grant-lx-create-01,grant-lx-post-01}.yaml`.
That is Q2's recommended disposition and § Open questions carries it.

**The distinct-holder constraint stays, and the first draft was wrong to move
it.** `tenants/ledgerxcorp/wallets/dhc-lx-create-post-01.yaml` names no tenant,
no wallet and no key, so on a profile/instance test it reads as domain policy
mis-filed under a tenant path — which is why the first draft relocated it. Two
measured consequences withdraw that:

- `check_real_estate()` loads all three record kinds from `WALLET_DIR` alone
  (`:39`, `:735-746`) and then does `dhc = constraints.get(EXPECTED_CONSTRAINT)`
  → `err(f"missing distinct-holder constraint …")` (`:774-776`). Move the file and
  the lookup returns `None` and the bar REDS.
- `check_real_estate()` also runs the pinned validator over the repository and
  asserts a floor: `elif int(m.group(1)) < 5: err(f"expected >=5 wallet-family
  records validated …")` (`:721`, `:725-729`). The five are the two wallets, the
  two grants and this constraint. Move it and the count is four.

**And relocating it would not merely red the bar — it would put the file beyond
every scan.** openXwallet's validator at `wallet-v1.1` PRUNES NESTED
REPOSITORIES from its sweep by construction: `sweep_candidates()`
(`scripts/validate-openxwallet.py:2063`) exists because "that sweep then walks
into every repository nested below that root and adjudicates its carried YAML as
LIVE RECORDS of the consumer's tree", and the prune is reported as a note
(`:2135-2142`, "nested repositories pruned (not adjudicated)"). So any wallet-kind
YAML placed inside a nested `LedgerxWallet` is adjudicated by NOTHING. The prune
was added at P2b of this very parent change, for the openxFactory case; it
applies here unchanged.

**The estate validator stays, and that is the largest correction.** The first
draft moved `tests/validate_wallet_estate.py` and paid for it with a delegating
bar entry, a declared estate root, an expected-set relocation and a restated
artifact floor — four seams. The review established that none of them is
necessary, because **rule 1 forbids integrating THE PRODUCT'S validator, and this
file is not the product's.** It is LedgerxFactory-authored (its header cites
feature 016 and the 2026-08-08 Ledgerx ratification; features 018 and 019 record
it as unpinned LedgerxFactory code). What breaches rule 1 is where it RESOLVES
the product's validator — and that is fixed by replacing the two-candidate
upward walk with one fixed relative path into the descendant. The breach closes
either way; this way opens no seams.

It also avoids four concrete breakages the move would have caused, each measured
rather than argued: `REPO` (`:38`) is used as four different referents — the
wallet directory (`:39`), the pinned validator's repo-scan target with the `>= 5`
floor (`:721`, `:725-729`), `os.path.join(REPO, "stack.yaml")` →
`yaml.safe_load(fh)["xfactory"]["contract_ref"]` (`:675-676`, a file LedgerxWallet
has no business owning), and the pin checker's positional argument (`:705`); and
`find_aggregation()` (`:560-595`) is a SECOND five-level upward walk, hunting a
`.gitmodules` that names `openxFactory` so `check_pin_reconciliation()` can
extract the PINNED relocation emitter (`git -C <openx> show
<pin>:scripts/check-openxfactory-pin.py`, `:687-689`) and run it — a leg the
parent's ratified `tasks.md` 6.2 makes this bar the ONLY observer of. One
declared root cannot serve four referents in two repositories.

**Both relocations are named successors**, each with the precondition it needs: a
descendant-side scan pass that survives the nested prune, and an artifact floor
restated per root.

**The platform seam stays.** `schemas/holder-registry.schema.yaml`
(`kind: ledgerx_wallet_holder_registry_contract`) declares the shape of LedgerLinc
table 50200 "LL Wallet Holder Registry" so "the repo and the client system state
the same facts". Its counterparty is Business Central, not the pinned product —
R3 of the parent one layer down: the product owns the standard, the factory keeps
the seam.

**Records stay.** `specs/016-posting-segregation-of-duties/`,
`specs/017-openxwallet-finder/`, `specs/018-openxwallet-pin-bump/`,
`specs/019-openxwallet-consumer-repoints/` — records of acts this repository
performed. Their PATH REFERENCES are a different matter (§ 4).

**The enumeration is complete, and checkably so.**
`git grep -l '^kind:.*wallet'` over LedgerxFactory `origin/main` returns EIGHT
files. Seven are committed YAML artifacts: the exercise template
(`ledgerx_wallet_exercise_template`), the holder-registry contract
(`ledgerx_wallet_holder_registry_contract`), the distinct-holder constraint, two
grants and two wallet records. The eighth is
`tests/validate_wallet_estate.py`, which matches because its NEGATIVE-PROBE
CORPORA are embedded as Python string literals — not an artifact, and named here
so the count is not quietly seven. ONE of the seven moves. Only two
`ledgerx_wallet_*` kinds exist in the repository and both are named above.

### 3. The resolution path becomes a pin, in one repository

In `tests/validate_wallet_estate.py`, `VALIDATOR_CANDIDATES` (`:53-78`) and the
five-level walk in `find_openxfactory()` (`:81-116`) are replaced by the single
fixed relative path `LedgerxWallet/openXwallet/scripts/validate-openxwallet.py`,
resolved from `REPO`, with the upward walk DELETED. There is then nothing to
break a tie between, and the commit that governs the reader is declared twice in
`LedgerxWallet` and once in `stack.yaml`.

`find_aggregation()` and `check_pin_reconciliation()` are UNTOUCHED — they
concern the openxFactory BUNDLE pin (`xfactory.contract_ref`), a different pin,
and the parent's ratified `tasks.md` 6.2 requires that leg to keep running.
Leaving them alone is the point of not moving the file.

Refusals gain the remediation string, and it is **`git submodule update --init
--recursive LedgerxWallet`** — recursive, because the reader is two levels down
(`LedgerxWallet`, then `openXwallet` inside it) and a non-recursive init
initializes one of the two.

### 4. `stack.yaml`, its digest, and a prepared live window

**`stack.yaml`** — `openxwallet.contract_source` re-sourced from
`openxFactory-nested-submodule-pin` to `LedgerxWallet-nested-submodule-pin`,
because after this change the descendant IS how the domain consumes the product,
and a `contract_source` naming openxFactory's gitlink would describe a path the
tree no longer takes. `contract_ref` is UNCHANGED (`63f5a1ad…`), so the re-homing
is bisectable against a re-pin. The parent's design D9 specified the value being
replaced; D9 is a DESIGN DECISION rather than a spec requirement, so no delta is
owed against `split-openxwallet-repo` — the substitution is what rule 1 compels
once the descendant exists.

**`models/protected-surface.yaml` needs a DIGEST RE-PIN, not just prose — and the
first draft got this backwards.** That file PINS `stack.yaml` by digest
(`:384-385`), and `docs/protected-surface.md:66-70` requires "edit it, recompute
its digest, and update the entry with the reason recorded beside it. An
unattributed re-pin defeats the point of pinning." The same entry records the
cost of skipping it (`:442-445`): "The unpinned window showed as `[baseline]
stack.yaml diverges from its pinned digest` in `validate_onboarding_contracts.py`,
red on main for seventeen days." P5b re-pinned in the same commit (`:387-388`);
so does this change. Separately the prose pointer at `:455` is amended — and
`:455` is the correct coordinate, not the `:438` the first draft cited against a
pre-P5b tree. Verified: NO digest row exists for the moved template, and
`templates/` is not among `protected_directories` (exactly `credentials`,
`adapters`, `policies`, `openspec/specs`, `conformance`).

**A PREPARED, UNEXECUTED live window points at both changing things.**
`specs/016-posting-segregation-of-duties/runsheet.md` carries `Status: prepared
(this feature performs NONE of it)`; Phase 0 records P0.1–P0.3 SATISFIED and P0.4
OPEN; the README confirms "What remains is the runsheet's live window". It links
the relocating template relatively at `:22-23`, and `quickstart.md:19` invokes
the neutral validator through openxFactory's checkout with `:3-7` naming that
checkout as the prerequisite. All are repointed IN THE SAME COMMIT as the move,
and a **P0.5 precondition is added** naming `git submodule update --init
--recursive LedgerxWallet` — otherwise the operator inherits a procedure that
cannot read its own template. LINKS AND PREREQUISITES ONLY: no step, actor, abort
condition or evidence requirement is touched.

*Rejected: waiting for the window to close.* It parks P6 behind P0.4, a decision
this change does not own.

### 5. The pin agrees three ways, on a declaration P5b has landed

**P5b IS MERGED**, so P6 amends a declared pin rather than inventing one. The
block (`stack.yaml:51-62`) mirrors `xfactory:` field for field at
`contract_ref: 63f5a1adac89f017e70bab9a4ffe7cf02d6e6705`,
`contract_bundle_tag: wallet-v1.1`, `contract_source: openxFactory-nested-submodule-pin`,
under a comment stating its own derivation — "openxFactory's nested `openXwallet`
gitlink at contract-v2.0". That derivation is what this change replaces.

> **LedgerxWallet's `openXwallet` gitlink = LedgerxWallet's `contracts/openxwallet-pin.yaml` `revision` = LedgerxFactory's `stack.yaml` `openxwallet.contract_ref`.** Three declarations of one commit.

`wallet-v1.1` is an ANNOTATED tag (object `021cdeef…`) dereferencing to
`63f5a1adac89f017e70bab9a4ffe7cf02d6e6705`, also openXwallet's `main` HEAD and
what openxFactory's own pin records — so the pin task resolves
`wallet-v1.1^{commit}`, never the bare tag.

**What checks it, and what does not.** `LedgerxWallet/tests/validate_pin.py`
checks (1) against (2) in the descendant, where the ratified rule puts it, and
its workflow makes that a real check. Whether (3) agrees is checked by the
estate validator when the bar is run — running code, in a HUMAN-RUN bar, because
LedgerxFactory has no GitHub Actions workflow at all (`.github/` holds
`CODEOWNERS` and `copilot-instructions.md`). **That is the honest form of the
claim, and this change does not dress it as a required check.**

**Three further declarations exist and are deliberately outside the invariant:**
openxFactory's own pin manifest and nested gitlink, and the aggregation's root
gitlink when P4 lands. `neutral-product-pin`'s "consuming repository's pin is
authoritative" requirement binds the aggregation-root ↔ openxFactory-nested pair.
A THIRD reachable checkout at `LedgerxFactory/LedgerxWallet/openXwallet`
therefore neither breaks nor widens that rule — **it falls OUTSIDE it, and
nothing in the corpus will ever compare the descendant's gitlink to either of the
two the rule covers.** That is accepted rather than overlooked: LedgerxWallet and
openxFactory are independent consumers of one product, may legitimately pin
different commits, and such a divergence is NOT an error and is checked by
nothing. Said plainly because an earlier draft called it "REPORTED" and named no
reporter, which is the LS-A3 shape this corpus knows by name.

### 6. Placement: nested only, and the price named

LedgerxWallet is nested at `LedgerxFactory/LedgerxWallet` — the RATIFIED
placement, the one this domain already realizes for `LedgerxAvatar`. The
aggregation's `xFactories/` placement is NOT taken: the descendant has no
standalone-cloning need (its only consumer is the tree it is nested in, which is
the criterion the ratified rule itself names), and that placement's standing is
REALIZED-BUT-NOT-YET-RATIFIED. If it is added later, the ratified rule binds the
follow-on — both gitlinks name the same commit. The new `.gitmodules` section is
named `LedgerxWallet`, matching its path; the existing entry is
`[submodule "ledgerXavatar"]` against `path = LedgerxAvatar`, and this change
does not propagate that mismatch.

## Capabilities

### New Capabilities

- **`ledgerxwallet-overlay-boundary`** — the repository, pin and profile contract
  for the FIRST domain descendant created under `domain-descendant-boundary`:
  that LedgerxWallet is the only path by which the Ledgerx domain RESOLVES
  openXwallet; that the pin is declared twice in one commit and checked by the
  descendant's own validator; that the descendant carries profile and never the
  tenant estate or a fork; and that a relocation reduces no coverage.

### Modified Capabilities

- None. `domain-descendant-boundary` and `neutral-product-pin` are RATIFIED-IN-CHANGE
  and **not yet promoted into `openspec/specs/`** — verified: it holds 52
  capabilities and neither is among them, because that change archives only on
  merged plus green realization evidence. This change cites them as ratified and
  issues no delta; a wanted rule change is an amendment to
  `split-openxwallet-repo`, not a requirement here.

## Impact

- **A new repository exists that did not.** `opensoft/LedgerxWallet` does not
  resolve today. Creating it, its ruleset and its first tag are `[OPERATOR]` acts.
- **The Ledgerx reader becomes gitlink-verified rather than digest-verified.**
  openxFactory's pin carries eight per-file `sha256` (`:70-86`), a
  `pinned_by_commit_only:` set (`:95-101`) and `verify_pin:
  scripts/verify-openxwallet-pin.py` (`:64`). The descendant's pin carries a
  commit and no digests. This CONFORMS — rule 2 requires only commit-twice of a
  descendant, and `neutral-product-pin` is scoped to openxFactory and to REQUIRED
  checks, of which LedgerxFactory has none — but it is a reduction in EFFECT and
  is stated rather than discovered. Digest verification of openXwallet remains
  openxFactory's.
- **A nested-only descendant is outside EVERY governed-repo enumeration in the
  corpus.** `scripts/sync-notebooklm-books.py:652-653` matches only
  `^\s*path\s*=\s*(xFactories/\S+)\s*$`, and its `in_nested_checkout()`
  (`:629-641`, skipped at `:767`) excludes any path below a `.git`-carrying
  directory — so `xFactories/LedgerxFactory/LedgerxWallet/**` is excluded from
  LedgerxFactory's OWN book walk by construction.
  `scripts/doc_health/ideation_routing.py:225-235` admits only `openxFactory` and
  `xFactories/<Name>`. And the parent's P4b widens exactly these two sites by an
  allowlist of ROOT-LEVEL neutral products — a nested domain descendant is
  outside the set before that widening and after it. **The ratified precedent is
  already in this hole:** the aggregation `.gitmodules` carries no `MedxAvatar`
  and no `LedgerxAvatar` entry. Accepted here because the descendant carries no
  ideation corpus; registered as a successor rather than left to be found.
- **A registered kind loses its artifact, and a maintained comment goes false.**
  `tests/validate_document_estate_surface.py` registers
  `ledgerx_wallet_exercise_template` with a CHK002 note (`:1116-1121`), and its
  comment block at `:1086-1098` says the validator "runs from openxFactory's
  nested gitlink … see `find_openxfactory()` in `tests/validate_wallet_estate.py`
  for the ordered candidates. Corrected at P5b". Both become false; that
  "Corrected at P5b" is proof the prose is maintained and load-bearing, not stale.
- **P5b and P3b are both DISCHARGED.** P5b as above; P3b — codexFactory's
  merge-gate floor — merged 2026-08-27T21:53 as PR opensoft/codexFactory#117,
  merge commit `58bd3cf7`. **P4 remains open** (the aggregation's root
  `openXwallet` gitlink) and P6 touches no aggregation path, so it does not gate
  this change. The first draft wrongly listed P3b as open.
- **Green-run tasks need an initialized checkout as a stated precondition.** In a
  workspace where `LedgerxWallet/openXwallet` is uninitialized the bar refuses —
  correctly — so every "the bar is green" claim names the initialization it
  depended on.
- **Provenance moves to prose.** The relocated template was authored under
  `modify-ledgerx-posting-authority-for-segregation-of-duties` (ratified
  2026-08-08). A fresh-repo scaffold carries no `git log`, so LedgerxWallet's
  `README.md` records the origin repository, the authoring change, and the commit
  the file came from. Prose provenance is weaker than history; naming it as weaker
  is the point.

## Successors named

- **The estate validator's relocation** — as a validator SPLIT (the governance
  half, which reads `stack.yaml` and runs the pinned relocation emitter, stays in
  LedgerxFactory; the profile half moves), with the four measured breakages in
  § 2b as its work list.
- **The distinct-holder constraint's relocation** — gated on a descendant-side
  scan pass that survives openXwallet's nested-repository prune, plus the `>= 5`
  artifact floor restated per root.
- **A declared Ledgerx wallet custody posture.** The posture exists today only in
  YAML comments in the two wallet records and in the 2026-08-08 ratification
  prose; a first draft authored it here. Withdrawn: nothing would read it (the
  validator keeps its thresholds at `:141-142` and `:770-773`), and a repo-level
  posture beside per-record `custody.model` is a second declaration of one fact
  with no reconciliation rule. The successor decides its reader and its home
  together — and under LedgerxFactory's own rules an ENFORCED posture belongs in
  the digest-protected `policies/`, not an unprotected `profile/` tree.
- **Governed-repo recognition for a NESTED descendant** — which would also
  finally cover `MedxAvatar` and `LedgerxAvatar`.
- **A REQUIRED check in LedgerxFactory.** It has no workflow at all; giving it its
  first one is bigger than this change.
- **`MedxWallet`, `codexWallet`, `OpsxWallet`, `AdxWallet`** — each lazily, on its
  domain's first wallet profile artifact.
- **The `xFactories/LedgerxWallet` placement**, if standalone cloning is ever
  needed, on the both-gitlinks-one-commit rule.
- **The `xfactory_wallet_*` → `openxwallet_*` kind-prefix rename** (parent Q3).
  The relocated template pins those strings by name, so LedgerxWallet becomes a
  re-pin site.

## Out of scope, deliberately

- **Moving the tenant estate** (Q2), **the distinct-holder constraint** or **the
  estate validator** (§ 2b). All three are successors with stated preconditions.
- **Any content change to the moved template.** Its placeholder ids stay as they
  are; generalizing them is a separate act.
- **Any change to `opensoft/openXwallet`.** Consumed at `wallet-v1.1`, not
  re-cut. Rule 3 routes anything the profile cannot express upstream, and this
  change finds nothing of the kind.
- **Any change to the xFactory aggregation** (§ 6).
- **The LedgerLinc / Business Central enforcement half.**
- **Re-widening the finder.** P5b narrowed it to two and forbade restoring the
  third; this change narrows it to one and adds none back.
- **Promoting `domain-descendant-boundary` into `openspec/specs/`.**

## Open questions — none remaining; Q2 was RULED at ratification

**Q2 — RULED 2026-08-28: STAY** (see § Ratification record, item 2). It is
recorded below in the form it was carried and recommended, because the grounds
are what the ruling adopted and a reader tracing the parent's carry-forward needs
to find them here rather than in a review record.

**Q2 (carried from the parent, its one open question) — do
`tenants/ledgerxcorp/wallets/*` move into LedgerxWallet, or stay as tenant data?**
The parent's ratification carries it forward explicitly: "Stays for
`create-ledgerxwallet-overlay-boundary` (P6); the profile/instance line is the
owning domain's call."

**Recommendation: STAY in LedgerxFactory as tenant data.** Three reasons, in
increasing force. (1) The records fall on the instance side on their own
contents — holder ids, DIDs, key ids, `expires_at`, `issued_by`, and a `state:`
"kept truthful by the session that closes each window". (2) A nested descendant's
YAML is pruned from openXwallet's own sweep (`sweep_candidates`, `:2063`,
`:2135-2142`), so moving the estate would move it OUT of adjudication — the
opposite of what a boundary is for. (3) **Those five files are the commit target
of the runsheet's unexecuted Phase 3.4** — a procedure that mints real keys and
flips wallet state. Relocating the write target of a prepared live window is a
risk with no offsetting benefit.

LedgerxWallet therefore carries the PIN and the profile artifact whose move costs
nothing, and grows the rest of the profile through the two named successors as
each earns its preconditions.

**This was the one question this proposal carried, and it is now CLOSED** — ruled
STAY on 2026-08-28, so it does not travel to a further change. Everything else
above is a ratified constraint, a decision this packet takes and defends, or a
correction it made to itself.
