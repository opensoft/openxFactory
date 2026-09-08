---
code_surface: openxFactory, opensoft/openXwallet (new), xFactory, LedgerxFactory, OpsxFactory, codexFactory — SIX repositories: the publisher, a NEW repository, the aggregation, two consumers, and codexFactory (its merge-gate floor, P3b — added on council review; this change previously and wrongly claimed codexFactory needed none). (1) `opensoft/openXwallet` created from scratch by a `git filter-repo` path carve over exactly twelve path sets, scaffolded with its own `contracts/manifest.yaml` at `wallet-v1.0` (with `wallet-v1.1` following at P2b — the nested-repository sweep prune and the register-read note, and the tag openxFactory actually pins), `contracts/CHANGELOG.md`, `README.md`, `CLAUDE.md`/`AGENTS.md`, `.github/CODEOWNERS`, `.github/workflows/wallet-validation.yml` + `pytest-suite`, a `contract_pin.yaml` vendoring one openxFactory artifact (with an explicit digest-verify step in `wallet-validation`), `docs/pin-resync-runbook.md`, `docs/openxwallet-cutover-runbook.md` (the ordered, reversible cutover procedure — P2's own artifact, authored before the carve it describes), and a branch-protection ruleset created in EVALUATE mode and promoted to ACTIVE once `wallet-validation` has reported once. (2) openxFactory: a nested submodule gitlink `openXwallet/` plus `.gitmodules`; a new `contracts/openxwallet-pin.yaml`; deletion of `contracts/openxwallet/`, `contracts/openxwallet-agent-profile/`, `scripts/validate-openxwallet.py`, `scripts/wallet-yaml-syntax-gate.py`, `tests/wallet_yaml_syntax_gate/`, `specs/006-openxwallet-contracts/`, `specs/010-wallet-validator-ci/`, `specs/012-wallet-issuer-anchor/`; `.github/workflows/wallet-validation.yml` renamed to `.github/workflows/openxwallet-consumer-gate.yml` with `jobs: wallet-validation:` RETAINED, so the ruleset-pinned token survives the file rename; `.github/workflows/pytest-suite.yml` (its checkout at `:203-206` gains nested-submodule fetch — which is NOT one line: `.gitmodules` uses `git@github.com:`, so it needs the house app-token + `git config --global url."https://x-access-token:$TOKEN@github.com/".insteadOf "git@github.com:"` pattern of `doc-health-reusable.yml:143-158` before checkout, because `github.token` cannot clone a second private org repository; the pinned collection count at `:37` moves, and its three `wallet-validation.yml` references at `:5`, `:14`, `:148` are renamed); `.github/workflows/doc-health-reusable.yml` (the governed-submodule init filter `grep -E '^(openxFactory|xFactories/)'` at `:154-158` and `:815-819` is non-recursive, so the nested `openxFactory/openXwallet/` is never initialized in aggregation runs); `scripts/validate-trust-anchor.py` (`OPENXWALLET_REGISTRY_PATH` at `:322-323`, rule (f) at `:1146-1176`, the hard exit at `:2582-2586`) and `tests/trust-anchor/`; `.github/CODEOWNERS`; `contracts/manifest.yaml` (the eight rows gain a `relocating:` field at P2.5 and are deleted at P3), `contracts/CHANGELOG.md`, `contracts/README.md`, `contracts/releases/<tag>.digests.yaml` — **TWO of them, one per bundle cut: P2.5's deprecation minor owes its own release-surface digest file, not only P3's major** — `README.md`, `docs/openxdox-naming.md`, `docs/archive-record-discrepancies.md`; and the P4b tooling sites `scripts/sync-notebooklm-books.py` + `scripts/doc_health/ideation_routing.py`. (3) Branch-protection RULESET STATE in both repositories — a repository setting, not a tree fact, and therefore its own evidence line. (4) The xFactory aggregation: `.gitmodules`, a root gitlink, `README.md`, `CLAUDE.md`. (5) Consumer pull requests: LedgerxFactory (`tests/validate_wallet_estate.py`, `stack.yaml` — the P2.5 minor bump at P5a.2 and a DECLARED wallet pin at P5b, `specs/016-posting-segregation-of-duties/quickstart.md`, README, one ownership comment) and OpsxFactory (one supporting-doc path). (6) codexFactory: `scripts/merge_master/openxfactory-review-authority-floor.yaml` gains `contracts/openxwallet-pin.yaml` and `openXwallet` under `never_clearable_paths` (P3b). Per `release-realization` this change archives ONLY on merged plus green realization evidence, never on landing.
target_release: implemented — each affected repository's own main line, plus two release identities allocated AT THE CUT and deliberately NOT reserved here: `wallet-v1.0` in `opensoft/openXwallet` (its first bundle tag, cut only after byte-identity is proven; `wallet-v1.1` follows at P2b and is the tag openxFactory's pin records) and the next openxFactory contract bundle, whose number `docs/contract-versioning-policy.md` forbids this proposal from naming ("A proposed change MUST NOT reserve a minor number before merge order is known"). The extraction plan's `contract-v1.44` is NOT carried, for exactly that reason. That bundle also owes a `contracts/releases/<tag>.digests.yaml` over its own release surface under `release-surface-integrity` — an obligation discharged at the cut, not a capability amendment.
---

# Proposal: split-openxwallet-repo

Status: ratified
Ratified: 2026-08-26 by Brett Heap (openxFactory operator authority) — in-session
ruling on PR #391 after both required checks passed. Realization proceeds per
tasks.md through Speckit features, §1 and P5a.1 first.
Proposed: 2026-08-26 — the first and only exit of the staged topic
`ideation/staging/openxwallet-neutral-home/`
(`openxFactory:staging:openxwallet-neutral-home`, staged the same day), on Brett
Heap's in-session ruling of 2026-08-26, recorded verbatim in that topic: "approve
R1-R8 as recommended, stage the topic and propose". Registered as DTN-026
(`split`, P1, `staged`).

## Ratification record, 2026-08-26

Recorded verbatim from the convener's in-session ruling, taken after PR #391's
two required checks reported green: **"ratify as proposed and merge, then start
/opsx:apply"** — followed immediately by his standing correction, **"remember
that we build with speckit, not openspec"**. Four rulings, in the order they
bind:

1. **Ratified AS PROPOSED** — no restructure and no carve-back. The packet
   stands as authored: the **two ADDED** capabilities
   (`domain-descendant-boundary`, `neutral-product-pin` — the reusable half that
   outlives the wallet), the **two REMOVED** capability deltas (`openxwallet`
   and `openxwallet-agent-profile`, leaving this corpus with their successor
   location recorded — its first `## REMOVED Requirements` blocks and its first
   capability exit), the **three MODIFIED** deltas (`trust-anchor`,
   `review-authority-intake`, `shared-contract-ownership`), Amendment 2 to
   `docs/openxdox-naming.md` and the aggregation working-rule amendment. **The
   byte-identity floor is ratified with its ONE named prose carve-out** — the
   `openxFactory SHALL` → `openXwallet SHALL` subject in the eleven moved
   requirements, the only prose edit the floor permits — and it is proven
   against the NAMED CARVE COMMIT, never against "HEAD".
2. **R1–R8 stand unchanged.** They were LOCKED before this packet was authored
   and ratification does not reopen them; the LOCKED block below is neither
   renumbered nor edited by this record.
3. **Q1–Q5 are CARRIED at design.md's dispositions** (§ Open questions), not
   resolved by this ratification:
   - **Q1 — register as a wallet primitive, or the reader split back?** NOT
     decided here; it travels, as the proposal expects — both resolutions move a
     gated path or change code, converting a byte-identical extraction into a
     design change, and the pin already makes "which reader ran" an auditable
     digest. Revisit when a second consumer of authority registers exists.
   - **Q2 — do `tenants/ledgerxcorp/wallets/*` move?** Stays for
     `create-ledgerxwallet-overlay-boundary` (P6); the profile/instance line is
     the owning domain's call.
   - **Q3 — the `xfactory_wallet_*` → `openxwallet_*` window.** Stays for the
     openXwallet successor; this design adds only the price — the prefix sits in
     `pinned_by_commit_only` bytes, so the rename is a wallet MAJOR, an
     openxFactory pin bump and a LedgerxFactory re-pin.
   - **Q4 — `openXwallet-Install`.** DECIDED as far as design reaches: the NAME
     is registered in Amendment 2 and no repository is created, on rule (d)
     applied to an install repo. Whether Hermes is the issuer host stays with
     hermes-install's roadmap and is a precondition of nothing in this wave.
   - **Q5 — the bundle-tag scheme.** DECIDED: `wallet-vN.M`, major on a breaking
     key or schema change, minor on additive growth, and NO range expression in
     the pin — commit and sha256 are authoritative and the tag is a label beside
     them (`revision_kind: commit`, D1).
4. **The build path is SPECKIT, and `/opsx:apply` is NOT used.** On the
   convener's standing correction, given the same minute as the ratification:
   **OpenSpec ratifies the boundary; Speckit builds it.** Realization proceeds
   as **Speckit features, one per `tasks.md` group, in `design.md`'s Migration
   Plan order**. The first two are **§1 — this change's own packet
   bookkeeping**, which still owes Amendment 2 to `docs/openxdox-naming.md`
   (task 1.11) and the xFactory `CLAUDE.md` working-rule #1 amendment (task
   1.12) — and **§2 — P5a.1, the LedgerxFactory three-candidate finder**, which
   lands before P2 because `validate_wallet_estate.py::find_openxfactory()`
   fails loudly rather than skipping.

The merge of PR #391 is the convener's own act and is NOT performed by this
record, which lands on `change/split-openxwallet-repo` ahead of it.

## Rulings carried as LOCKED decisions

R1-R8 were ruled before this proposal was authored. **They are constraints on it,
not questions in it.** The bench may contest how this proposal constructs them; it
does not reopen them.

1. **R1 — the repo and brand are `opensoft/openXwallet`, prose `openXwallet`** —
   the ratified house `openX<type>` form. `docs/openxdox-naming.md` (LOCKED
   2026-08-13) names `openxWallet` as one of two family EXCEPTIONS to it, so the
   ruling removes an exception in a `ratified` record; that is why Amendment 2 is
   IN this change rather than a silent re-spelling.
2. **R2 — machine keys do not move in v1.** Paths stay `contracts/openxwallet/`;
   capability ids, the `xfactory_wallet_*` kind prefix, the envelope kind, finding
   codes and filenames are unchanged — LedgerxFactory pins five kinds and several
   finding-code strings by name, so a rename inside the move is unbisectable.
3. **R3 — the new repo owns the wallet's own standard; openxFactory keeps the
   seam.** openXwallet takes both families, the corpus, the validator, the syntax
   gate and its tests, the CI workflow, the two promoted specs, Speckit
   006/010/012 and the `2026-08-08-add-openxwallet` archive; openxFactory keeps
   `governance/review-authority/`, Speckit 013/014, the active
   `add-wallet-carried-review-authority` work, the trust-anchor /
   identity-brokering / roles-authority-model compositions and all ideation
   provenance. The primitives are non-substrate product; the review gate's USE of
   wallet authority is factory-layer.
4. **R4 — the dependency is pinned in both directions, and there is no cycle.**
   openxFactory pins openXwallet by commit plus per-file sha256 plus
   `pinned_by_commit_only`, via the `openXwallet/` gitlink and
   `contracts/openxwallet-pin.yaml`; openXwallet vendors exactly ONE openxFactory
   artifact at a digest pin, `contracts/schemas/hermes-job-envelope.schema.yaml`,
   which validator rule (g) reads (`scripts/validate-openxwallet.py:218`). Both
   directions are commit-pinned read-only consumption, so nothing builds in a
   loop. Rejected: making rule (g)'s vocabulary a CLI parameter with no default,
   which silently weakens the gate.
5. **R5 — placement is a root-level `openXwallet/` submodule** in the xFactory
   aggregation, sibling of `openxFactory/` and `openAvatar/`, on the DTN-022
   precedent that a neutral product pins at the aggregation's neutral root.
6. **R6 — the register STAYS in openxFactory; its READER moves with the
   validator.** The register is openxFactory's own review authority
   (`target_repo: opensoft/openxFactory`) and codexFactory's merge-gate floor pins
   its exact path under `never_clearable_paths` with a parser that refuses
   wildcards (verified on `origin/main`, 2026-08-26). **There is NO "generic
   authority-register mode" to build — the capability already exists.** `repo_scan`
   calls `check_register(f, target, repo_ctx)` with the SCAN TARGET
   (`scripts/validate-openxwallet.py:2091`), and `check_register` joins that
   `base_dir` with `REGISTER_DIR_PARTS` (`:1865`; `("governance",
   "review-authority")` at `:1780-1781`). So the literal invocation
   **`python3 openXwallet/scripts/validate-openxwallet.py .`, run from the
   openxFactory root**, already reads `governance/review-authority/` with **zero
   code change**; `main()` accepts one positional `path` plus `--strict` and nothing
   else (`:2110-2118`). The reader — rule (u), `check_register`,
   `_load_attestations`, the constants at `:1780-1787` — therefore travels
   unmodified, and openxFactory's consumer gate invokes the PINNED reader over its
   own tree by passing `.`. **Zero refactor, stated so it can fail:** the diff of
   `scripts/validate-openxwallet.py` between the NAMED CARVE COMMIT and openXwallet
   `wallet-v1.0` is **EMPTY** — not "touches only `ENVELOPE_SCHEMA_PATH`", because
   P2 requirement (i) places the vendored schema at the identical
   repository-relative path and `:218` is `ROOT`-relative, so even that line does
   not move.
7. **R7 — descendants are `MedxWallet`, `LedgerxWallet`, `codexWallet`,
   `OpsxWallet`, `AdxWallet`** — the `<Domainx><Product>` form all four existing
   descendants use. `medXwallet` would be a third casing scheme in the org; the
   cost of either choice is zero today because none of them exists.
8. **R8 — the first descendant is `LedgerxWallet`, at extraction time.**
   LedgerxFactory is the only live consumer — two wallet records, two grants, one
   distinct-holder constraint, an exercise template and
   `tests/validate_wallet_estate.py` — so it has descendant content on day one.
   `MedxWallet` follows on the Medx EMR thread's first profile; codex, Ops and Adx
   on demand.

## Why

**The wallet's contracts ARE a product, filed as features of a factory layer.**
`openxwallet` (8 promoted requirements) and `openxwallet-agent-profile` (3) are
ratified holder-agnostic and non-substrate — the core's eighth requirement is
literally "The capability is an authority control, never an identity substrate"
(`openspec/specs/openxwallet/spec.md:155`), which is the definition of content
belonging to no single layer's corpus. **What IS factory-layer sits in the same
repository with no boundary:** `governance/review-authority/` and the active
`add-wallet-carried-review-authority` describe how openxFactory's review gate USES
wallet authority, and today every wallet-primitive change and every review-gate
change share one blast radius, one workflow and one CODEOWNERS surface.

**The house standard for a neutral product with domain consumers is its own repo
plus pin-and-profile descendants — and it has exactly ONE ratified instance.**
Cited as what each precedent actually is, per the staged topic's own corpus
correction (checked 2026-08-26):

| Neutral product | Domain descendant | Standing of the establishing act |
| --- | --- | --- |
| `openAvatar` | `MedxAvatar` (nested in MedxFactory), `LedgerxAvatar` | **RATIFIED** — DTN-022, Brett 2026-08-03: own repo, and "domain descendants are pin-and-profile DISTRIBUTIONS … never code forks" |
| `openChart` | `MedxChart` | `create-medxchart-overlay-boundary` — `Status: draft`, a change IN FLIGHT (realized in the workspace, not ratified) |
| `openPractice` | `MedxPractice` | `create-medxpractice-overlay-boundary` — likewise `Status: draft`, in flight |

Calling all three ratified precedent would overstate the corpus. What is true and
load-bearing is narrower and enough: **no DomainxFactory consumes any open\*
product by direct integration, and there is no counter-example.** The only direct
consumer of neutral contracts is openxFactory-as-layer through `stack.yaml`, and
openxFactory is the neutral layer, not a domain.

**Stated plainly, because it is the honest weight of the precedent (V11): no
promoted capability has previously LEFT this corpus.** DTN-022 moved code, not
promoted requirements — this change is the corpus's first
`## REMOVED Requirements` block and its first capability exit. **The descendant
standard therefore rests on ONE ratified precedent**, DTN-022's openAvatar, and
rule (c)'s second placement rests on a `draft`. Both are enough to proceed and
neither is enough to be described as settled practice; the bench is reviewing a
first, and rule (c) now says which half is ratified and which is not.

**LedgerxFactory is a live consumer that fails loudly rather than skipping.**
`tests/validate_wallet_estate.py::find_openxfactory()` walks up five levels for
`openxFactory/scripts/validate-openxwallet.py` and returns `None` — "an absent
checkout is a loud failure, never a skip: an unreadable surface must fail, not
degrade to 'empty' (repo law, 2026-08-07)". Sequencing is therefore a correctness
property, not tidiness.

**Now is the moment because of what is still open elsewhere.** Slices S3 and S5 of
`add-wallet-carried-review-authority` are entirely open (15 of its 21 open tasks — §6 S3's eight plus §7 S5's seven)
and tagged `[hermes-install]`/`[codexFactory]`. If the extraction lands first, any
`openxwallet` core delta those slices need is authored once, in the right
repository, instead of being written in openxFactory and immediately migrated. That
is not an inference: `add-wallet-carried-review-authority/tasks.md` 8.1, **RULED
2026-08-26 by Brett Heap**, closes with "Cascade enforcement rides the named core
deltas at S5" over exits that "need `openxwallet` / `openxwallet-agent-profile` core
deltas" (`:317-330`). The core deltas S5 needs are named and dated; the only open
question is which repository they are authored in.
Every prior neutral product paid for its own bespoke boundary change; a fourth
would buy a fourth bespoke boundary instead of a standard.

**The cost is stated here rather than discovered at S5 (V12).** After the cut, an
`openxwallet` core delta — S5's ruled DRIFT cascade among them — costs **a wallet
release, an openxFactory pin bump, and a LedgerxFactory re-pin**, in that order.
`docs/pin-resync-runbook.md` is the path, and openXwallet's scaffold carries it from
day one for exactly this reason. The arc's owner should see that price before
ratification, because it is the price of the boundary and not a defect in it: the
same three steps are what make "which reader ran" an auditable digest instead of an
assumption.

## What Changes

Ordered by the extraction plan's phases, on the discipline
`add-wallet-carried-review-authority` set for S1-S5: **a physical act needs its own
realization evidence, so this change RATIFIES the standard and the obligations and
AUTHORIZES the acts as named successors.**

### What this change RATIFIES (its own diff)

1. **Two ADDED capabilities** — `domain-descendant-boundary` and
   `neutral-product-pin`. These are the reusable half and they outlive the wallet.
2. **Two REMOVED capability deltas** — `openxwallet` and
   `openxwallet-agent-profile` leave the openxFactory corpus with the successor
   location recorded (## Capabilities → Removed).
3. **Three MODIFIED deltas** — `trust-anchor`, `review-authority-intake` and
   `shared-contract-ownership` (the last one added on alignment review: shedding the
   validator removes a publisher marker, and that requirement's consumer path assumes
   the publisher is openxFactory).
4. **Amendment 2 to `docs/openxdox-naming.md`**, in Amendment 1's shape (`:84-100`):
   the record is amended, never rewritten. TWO edits, both quoted so the bench
   reviews text rather than intent.

   The new section, appended after Amendment 1:

   > ## Amendment 2 — `openXwallet` leaves the exception list (2026-08-26)
   >
   > **`openxWallet` becomes `openXwallet`, the house `openX<type>` capital-X
   > form.** Brett's ruling of 2026-08-26 (R1 of `split-openxwallet-repo`), taken
   > because the product is being given its own repository and brand at
   > `opensoft/openXwallet`, and a brand created under a spelling this record lists
   > as an exception would ratify the exception a second time.
   >
   > The wire label stays LOWERCASE — `openxwallet` capability ids, the
   > `xfactory_wallet_*` kind prefix, paths and finding codes are untouched —
   > because that is this record's own rule: the brand and the label differ by
   > design; this is not a spelling to reconcile. `openXwallet-Install` is
   > registered as a NAME here and no repository is created (Q4).
   >
   > The record above is amended rather than rewritten: `openxWallet` was genuinely
   > a family exception when the form was locked on 2026-08-13, and the
   > short-handle argument that cited it still holds. Only the brand moved.

   And the inline pointer at `:23-25`, whose sentence names TWO exceptions and must
   stay grammatical when one of them leaves:

   > **before:** (the lowercase `openxFactory` / `openxWallet` spellings are the
   > family exceptions, not the rule).
   >
   > **after:** (the lowercase `openxFactory` spelling is the family exception, not
   > the rule; `openXwallet` left this list in Amendment 2).
5. **The aggregation working-rule amendment**, quoted in both directions so the
   diff is checkable rather than described. xFactory `CLAUDE.md` § "Working rules"
   item 1 reads today, verbatim:

   > 1. Domain-neutral contracts live ONLY in `openxFactory`; domain repos pin the
   >    openxFactory version they consume in their `stack.yaml`.

   It becomes FALSE AS WRITTEN the moment the shed lands. The replacement text,
   verbatim:

   > 1. Domain-neutral contracts live in `openxFactory` or in a neutral `open*`
   >    product repository that `openxFactory` pins by commit and digest; domain
   >    repos never author neutral contracts, and every consumer pins the
   >    openxFactory version it consumes in its `stack.yaml`.

   Until P4 lands, the rule as written is the one in force and this change
   contradicts it; stated here rather than discovered later.

### What this change AUTHORIZES as successors, each with its own evidence

- **P2 — carve and scaffold `opensoft/openXwallet`.** `git filter-repo` over the
  twelve path sets named in `code_surface`, full path history (the openAvatar
  subtree-split precedent); governed-repo scaffold; **`docs/openxwallet-cutover-runbook.md`,
  authored BEFORE the carve it describes** (§ The cutover runbook, below);
  `contract_pin.yaml` vendoring the job-envelope schema. **Three P2 REQUIREMENTS,
  not preferences:**

  **(i) the vendored copy sits at exactly `contracts/schemas/hermes-job-envelope.schema.yaml`**
  — the same repository-relative path it holds in openxFactory — because
  `ENVELOPE_SCHEMA_PATH` is `ROOT / "contracts" / "schemas" /
  "hermes-job-envelope.schema.yaml"` (`scripts/validate-openxwallet.py:218`) and
  `:2156` prints `ENVELOPE_SCHEMA_PATH.relative_to(ROOT)`, so an identical relative
  path means **no source edit at all**, and R6's empty-diff proof survives. Every
  other `ROOT`-relative constant (`:213-218`) is likewise unchanged.

  **(ii) the carve PRESERVES the `contracts/openxwallet*/examples/` path prefixes.**
  `repo_scan`'s corpus exclusion (`:2050-2053`) keys on `"examples" in path.parts`
  AND a part in `("openxwallet", "openxwallet-agent-profile")`. A carve that
  flattens or renames those prefixes causes the 36 intended-invalid negatives to be
  re-adjudicated as LIVE records — inside openxFactory's own REQUIRED check, since
  the consumer gate sweeps this tree. An acceptance line, not a hope.

  **(iii) `wallet-validation` gains an explicit digest-VERIFY step for the vendored
  schema, ahead of the validator.** `main()` checks only
  `ENVELOPE_SCHEMA_PATH.is_file()` (`:2124`) — presence, not identity. openAvatar's
  `contract_pin.yaml:15-21` shows the house shape: a named `verify_pin` that FAILS
  CLOSED pre-sync ("a recomputed digest can never equal an empty recorded digest →
  drift → fail before any test"); openXwallet's `contract_pin.yaml` was given no
  such verifier and now gets one. In the same act, openXwallet's
  `contracts/manifest.yaml` registers the vendored file as a **CONSUMED member**
  (`compatibility: canonical_openxfactory_contract`, `adapter_owner: openxFactory`,
  digest equal to the pinned openxFactory row's), so
  `shared-contract-ownership:142`'s all-markers-together publisher test is met
  without openXwallet claiming ownership of an openxFactory contract.

  Then the byte-identity proof, stated so it can fail: **against a NAMED CARVE
  COMMIT — openxFactory `<sha>`, recorded in the cutover runbook and in
  `contracts/openxwallet-pin.yaml`, never "HEAD" — for each of the eight rows at
  `contracts/manifest.yaml:1967-2082`, `sha256sum` at openXwallet `wallet-v1.0`
  equals the recorded `sha256:`, and a diff of the carved subtree against that
  commit's `contracts/openxwallet*/`, `scripts/validate-openxwallet.py`,
  `scripts/wallet-yaml-syntax-gate.py` and `tests/wallet_yaml_syntax_gate/` is
  empty** (spec prose excepted, per the named carve-out below); then tag
  `wallet-v1.0`.
- **P2b — `wallet-v1.1`, and openxFactory's first pin is THAT tag, not
  `wallet-v1.0`.** Two additive-minor changes in openXwallet, landing as ONE
  auditable diff on top of the byte-identical first release: (i) `repo_scan` prunes
  any file descending from a directory OTHER than the scan root that carries a
  `.git` entry, file or directory — the nested-repository exclusion P3's REQUIRED
  sweep depends on, made in the product's own code instead of as an openxFactory
  edit to a pinned artifact, and closing the same pre-existing hole for
  `installs/omnigent-install`, which the sweep walks into today; and (ii) the
  register-read `f.note` D3's positive proof rests on. **`wallet-v1.0` stays the
  byte-identical pure move and the floor is proven against IT**, at the named carve
  commit; P2b is the one diff on top, none of the eight digested artifacts is
  touched by it, so `contracts/openxwallet-pin.yaml` records
  `contract_bundle_tag: wallet-v1.1` with those eight sha256s still equal to the
  carve commit's rows. **P2b lands BEFORE P3**, because the sweep hazard sits inside
  a REQUIRED check and a hazard inside a required check is closed before the check
  starts running, not after.
- **P2.5 — the deprecation minor, and it is a precondition of P3's class. The
  marker is MANIFEST-CARRIED, never validator-carried.**
  `docs/contract-versioning-policy.md:250-255` makes a REMOVED shape BREAKING
  (major), and a major "requires … at least one full minor release where the old
  shape produced deprecation warnings" plus "an update to the conformance
  validator". So the cut owes a PRECEDING openxFactory minor.

  **What it must NOT do is make `scripts/validate-openxwallet.py` emit that
  warning.** An earlier reading of this proposal said it should; that reading is
  WITHDRAWN, for three independent reasons. LedgerxFactory runs the validator
  `--strict` — `check_real_estate()` calls `run_validator(REPO, strict=True)` and
  `err()`s on any non-zero exit (`tests/validate_wallet_estate.py:196-205`) — and
  `scripts/validate-openxwallet.py:2107` returns `1` when `strict and f.warnings`,
  so one new warning REDS the only live consumer. It would edit the validator inside
  a move whose safety rests on an empty diff, breaking both the byte-identity floor
  and R6's proof. And it would be surfaced by no required check anyway, because
  openxFactory's own gate runs the validator WITHOUT `--strict`
  (`.github/workflows/wallet-validation.yml:34`).

  **The marker is therefore a `relocating:` field on the eight rows at
  `contracts/manifest.yaml:1967-2082`** — naming target repository
  `opensoft/openXwallet` and the successor tag — **plus the CHANGELOG migration
  note the deprecating-minor clause requires** (`:246-249`: "the conformance
  validator emits warnings but still accepts it. Deprecations must state the removal
  version and a migration path in the CHANGELOG"). It is **READ BY MANIFEST /
  RELEASE TOOLING**: the domain-pin checkers
  (`scripts/check-openxfactory-pin.py`, `scripts/validate-domain-openxfactory-pins.py`)
  warn when a domain pins a bundle carrying `relocating:` rows. Which of those
  emits, and the field's exact shape, is design's call — carried as an open design
  item, not decided here. **`scripts/validate-openxwallet.py` is NOT edited in
  openxFactory by P2.5.**

  **The `:252-255` conformance-validator obligation is discharged explicitly, not
  implied:** from the major (P3) forward, **the pinned openXwallet
  `scripts/validate-openxwallet.py` at the digest recorded in
  `contracts/openxwallet-pin.yaml` IS this contract family's conformance
  validator**, invoked by openxFactory's consumer gate. The policy's required
  "update to the conformance validator that accepts the new shape and rejects the
  old one only at the new major version" is satisfied by the validator MOVING to
  the repository that owns the shape from the major forward — that move IS the
  update, and naming it here is what keeps the major conformant.

  **P2.5 is a bundle cut and owes its own `contracts/releases/<tag>.digests.yaml`**
  over its release surface under `release-surface-integrity` — carried in
  `code_surface`, because a minor that skips it is a non-conformant release.

  P2.5 may land any time before P3; P3 is the major.
- **P3 — openxFactory consumes and sheds, in ONE atomic pull request. BREAKING.**
  Paths move out of this repository; the manifest loses eight registered artifact
  rows; and the trust-anchor validator's registry path changes — falsifiably:
  **`scripts/validate-trust-anchor.py` resolves `OPENXWALLET_REGISTRY_PATH` from
  `contracts/openxwallet-pin.yaml` and exits `2` with a named refusal on an
  uninitialized submodule or a digest disagreement, and `tests/trust-anchor/` covers
  both cases.** It is one PR because `scripts/validate-trust-anchor.py:2582-2586`
  exits `2` when `contracts/openxwallet/openxwallet-custody.registry.yaml` is absent,
  so no ordering of two commits leaves a green intermediate state. The nested gitlink
  is not a new shape for this repository: openxFactory already carries one,
  `installs/omnigent-install` in its own `.gitmodules`.

  **P3's CI half is not one line of YAML** (V9). `.gitmodules` uses
  `git@github.com:`, and `github.token` cannot clone a second private org
  repository, so both `openxwallet-consumer-gate.yml` and
  `.github/workflows/pytest-suite.yml` need the house pattern
  `doc-health-reusable.yml:143-158` already carries — `create-github-app-token@v2`,
  then `git config --global url."https://x-access-token:$TOKEN@github.com/".insteadOf
  "git@github.com:"` BEFORE checkout, then a scoped `git submodule update --init`.
  `pytest-suite.yml:203-206` has none of it today. Design chooses between that
  pattern and declaring the nested `.gitmodules` URL as
  `https://github.com/opensoft/openXwallet.git`; what P3 may NOT do is add
  `submodules: true` and call it done. Two further CI facts, each verified:
  **doc-health's init filter is non-recursive** — `grep -E
  '^(openxFactory|xFactories/)'` at `doc-health-reusable.yml:154-158` and
  `:815-819`, so `openxFactory/openXwallet/` is never initialized in aggregation
  runs and must be added explicitly or the init made `--recursive`; and **the
  repointed `OPENXWALLET_REGISTRY_PATH` stays a real `Path` at MODULE scope**,
  because `tests/trust-anchor/test_negative_corpus.py:47` and
  `test_declaration_perimeter.py:55` both call
  `MODULE.load_yaml(MODULE.OPENXWALLET_REGISTRY_PATH)` at setup — the pin and digest
  check happens in `main()`, never at import, or every trust-anchor test dies at
  collection.

  **P3 also owes two negative properties** (V5, V7), and the first of them is
  discharged UPSTREAM rather than by an openxFactory edit: the pinned sweep must
  SKIP the `openXwallet/` gitlink directory (a submodule's `.git` is a FILE, so the
  existing `.git` skip does not fire) — and because the sweep is the PRODUCT's own
  code, that exclusion is an openXwallet change cut as **`wallet-v1.1`** ahead of
  P3, successor **P2b** below, never an edit to a byte-identical `wallet-v1.0`.
  Second, **the exact invocation string is pinned in a test**, because `main()` runs
  `repo_scan` — and hence `check_register` — only `if args.path is not None`
  (`scripts/validate-openxwallet.py:2160`). Point the pinned validator at
  `openXwallet` or omit the argument and the REQUIRED check goes GREEN with the
  register never opened. `grep -rn "wallet-validation.yml" tests/` returns nothing
  today, so nothing currently stops that.

  **And the proof that the register was READ is POSITIVE — it is not a log line
  naming the register file.** An earlier reading of this proposal promised such a
  line; that reading is WITHDRAWN, because the pinned reader does not produce one.
  On the happy path `check_register` emits NOTHING that names
  `governance/review-authority/register.yaml`: the only lines carrying that path are
  its failure findings, and the absent-register note names no path at all. What the
  reader DOES produce is a conjunction, and that conjunction is the evidence — the
  `repo scan: N openxWallet artifact` note (the sweep ran, over a directory target)
  TOGETHER WITH the absence of `no intake register at this tree` and of any
  `register-*` finding code (the register existed and parsed AT the scan target). A
  durable positive line lands upstream at `wallet-v1.1` (P2b) as an `f.note` naming
  the resolved register path when the register IS read — a NOTE and never a warning,
  because `scripts/validate-openxwallet.py:2107` reds a `--strict` run on warnings
  and LedgerxFactory runs `--strict`. The pinned test asserts both forms, so it does
  not go stale across the tag.
- **P3b — codexFactory floor widening. LANDS IN THE SAME WAVE AS P3.** Reversing an
  earlier claim in this proposal that codexFactory needs no change (V6).
  `scripts/merge_master/openxfactory-review-authority-floor.yaml` lists exactly ONE
  `never_clearable_paths` entry, `governance/review-authority/register.yaml`, and
  `repository_floor.py::matching_paths` is exact set membership
  (`path in protected`). Nothing covers `contracts/openxwallet-pin.yaml` or the
  `openXwallet` gitlink, so after P3 **a single pull request could bump the gitlink
  to a neutered reader AND edit a grant while matching no floor path** — clearable
  by council, no human required. P3b adds `contracts/openxwallet-pin.yaml` and
  `openXwallet` (gitlink form, no trailing slash: `_parse_exact_path` rejects a
  leading or trailing `/` and accepts the bare name) to `never_clearable_paths`. Its
  own realization-evidence row: the floor-file diff plus the merged pull request.
- **P4 — aggregation. LANDS IN THE SAME WAVE AS P3.** Root `openXwallet/` gitlink and
  `.gitmodules`, README Terms and layout, `CLAUDE.md` orientation and working rule
  #1. Same wave and before LedgerxFactory's next estate run, because between P3's
  merge and P4-plus-`--init` NEITHER gitlink candidate exists in any checkout
  (V3).
- **P5a.1 — LedgerxFactory forward-compatible finder. LANDS FIRST, before P2.**
  `find_openxfactory()` (`tests/validate_wallet_estate.py:47-63`) resolves in
  **three** ordered candidates, not two (V3): first
  `openxFactory/openXwallet/scripts/validate-openxwallet.py`, then
  `openXwallet/scripts/validate-openxwallet.py`, then
  `openxFactory/scripts/validate-openxwallet.py`. The nested candidate leads because
  the finder walks UP the tree and would otherwise resolve the AGGREGATION's
  root-level gitlink — a DIFFERENT gitlink from openxFactory's nested
  `openxFactory/openXwallet/`, which is the one `contracts/openxwallet-pin.yaml`
  governs. Forward-compatible by construction — candidate three is today's
  behaviour — so it can land any time, and it MUST land first.
- **P5a.2 — LedgerxFactory `stack.yaml` bump to the P2.5 minor. LANDS AFTER P2.5 IS
  CUT, BEFORE P3.** It bumps `xfactory.contract_ref` from openxFactory `39539fd4…`
  (`:13-14` today) to the deprecation minor, and adds one invocation of the pinned
  checker to LedgerxFactory's estate run, so the one live consumer actually OBSERVES
  the `relocating:` marker; without both halves the deprecating-minor warning window
  is unobserved by anyone and the policy's precondition is a formality. **This is a
  SECOND pull request, not a second paragraph of P5a.1**, and the split is forced
  arithmetic rather than a revision: one pull request cannot both precede P2 and pin
  a bundle P2.5 has not yet published. Both of this proposal's constraints — the
  forward-compatible finder before P3, the consumer observing the marker before the
  major — are satisfied by the split and by nothing else.
- **P5b — post-move repoints.** Drop the Ledgerx fallback; **record the wallet
  commit and `wallet-vN.M` in LedgerxFactory's `stack.yaml`**, in the shape its
  `xfactory:` block already uses, so the consumer holds a DECLARED wallet pin from
  the cut rather than inheriting one transitively (V3; field shape carried to
  design); Ledgerx quickstart path
  (`specs/016-posting-segregation-of-duties/quickstart.md:15`), README and one
  ownership comment; OpsxFactory's single prose path
  (`add-keycloak-administration-workflow/supporting-docs/identity-pki-administration.md:417`).
- **P6 — `LedgerxWallet`** via `create-ledgerxwallet-overlay-boundary`, on the
  descendant standard this change ratifies.
- **P7 — close.** Archive on realization evidence; DTN-026 → `implemented`;
  NotebookLM sync `--apply`.

### The byte-identity floor (R2, and why it is a floor)

**The first release is a byte-identical pure move:** zero renames of `kind:`
values, capability ids, finding codes or filenames, zero corpus edits. The eight
artifact sha256s in openXwallet's own `contracts/manifest.yaml` MUST equal the rows
at the **NAMED CARVE COMMIT** — openxFactory `<sha>`, recorded in
`docs/openxwallet-cutover-runbook.md` and in `contracts/openxwallet-pin.yaml`, and
**never "HEAD"**, which is not a stable referent across a multi-pull-request wave
(`contracts/manifest.yaml:1967-2082`) — before `wallet-v1.0` is tagged. Any content change the extraction wants is a separate,
later change in the new repo, **because a move whose diff is not provably empty
cannot be bisected against** — and that property is what makes an atomic
consume-and-shed safe to merge at all.

**One carve-out, named.** The eleven moved requirements read `openxFactory SHALL …`
(`openspec/specs/openxwallet/spec.md:8`, `openxwallet-agent-profile/spec.md:8`). The
floor covers `contracts/` BYTES — schemas, registry, packaged corpus, validator — and
NOT the spec prose. The subject is rewritten to `openXwallet SHALL` in the same move,
as the only prose edit the floor permits, because a requirement naming the wrong
repository is not a pure move either.

One precision the plan's shorthand loses: the manifest carries per-file digests for
the eight SCHEMA and REGISTRY artifacts only; the validator, the syntax gate, the
packaged corpus and the family READMEs are "content-addressed by commit; no
per-file digest" (`contracts/manifest.yaml:1968-1972`). The pin file therefore
carries per-file sha256 for the eight and `pinned_by_commit_only:` for the rest —
which is exactly the strictness `neutral-product-pin` ratifies, not a weaker
special case.

### The register stays; only its reader moves (R6)

All four files under `governance/review-authority/` stay.
codexFactory's `scripts/merge_master/openxfactory-review-authority-floor.yaml`
names `governance/review-authority/register.yaml` in `opensoft/openxFactory`
under `never_clearable_paths`, and that floor cannot be satisfied by a path in
another repository. The reader travels; the data stays; the consumer gate runs
the PINNED reader over openxFactory's own tree.

**codexFactory DOES need a change, and this reverses an earlier claim in this
proposal that it did not** (V6). The floor's single entry protects the register
FILE; it protects nothing about the tool that reads it. `matching_paths` is exact
set membership (`repository_floor.py:30-32`: `path in protected`), so after P3 a
pull request that bumps the `openXwallet` gitlink to a neutered reader AND edits a
grant under `governance/review-authority/` matches no floor path at all — a
candidate could repoint its own checker and clear the result by council. **P3b
widens the floor** to `contracts/openxwallet-pin.yaml` and `openXwallet`, in the
same wave as P3, and `neutral-product-pin` carries the general rule as a scenario.

### The REQUIRED check: a live requirement is being REPLACED, not created

**Correction to the extraction plan, carried because it turns an obligation into a
risk.** `add-wallet-carried-review-authority` task 2.5 is **DONE**, not open: org
ruleset **21538893** ("openxFactory wallet-gate (require wallet-validation)") has
been ACTIVE on this repository's default branch since 2026-08-26, verified through
`GET repos/opensoft/openxFactory/rules/branches/main`. The open task is **2.6** —
the red-proof that a deliberately malformed grant fails a pull request, with
ruleset state as evidence.

So the extraction is not marking a check required for the first time; it is
**renaming the workflow FILE behind a token a live ruleset pins**. The token is the
JOB ID, never the filename — `.github/workflows/wallet-validation.yml:6-9` says so
in its own words ("the status check must surface as exactly `wallet-validation`
(FR-007), the literal token the ruleset pins; a distinct job display name silently
de-advises the gate"), and `:19-20` carries `jobs:` → `wallet-validation:`.

**P3 therefore resolves this by ALIAS, not by repoint.**
`.github/workflows/openxwallet-consumer-gate.yml` keeps `jobs: wallet-validation:`
unchanged, so the required token survives the file rename; ruleset 21538893 is
UNTOUCHED by P3; and **no operator act stands between P3 and merge** — the new
workflow runs on P3's own pull-request head, so the required token reports there
and the pull request is mergeable. Both alternatives are unmergeable and are named
so neither is re-proposed: deleting the workflow first means the required token
never reports on P3's own pull request, and repointing the ruleset first fails
because the new token does not exist until a workflow has reported under it once.

**Renaming the TOKEN to `openxwallet-consumer-gate` is a named SUCCESSOR**, not
part of P3: add the new token ALONGSIDE `wallet-validation` in ruleset 21538893,
land one green pull request reporting under both, then drop the old one. Out of
this change's scope, and a precondition of nothing here.

Two obligations do travel with the wave, or the gate lapses silently:
`wallet-validation` becomes REQUIRED in `opensoft/openXwallet` (bootstrapped per
`docs/openxwallet-cutover-runbook.md` — EVALUATE mode, one trivial pull request so
the check reports and becomes selectable, then ACTIVE; **day-one REQUIRED is
impossible**, because GitHub cannot require a check that has never reported), and
**task 2.6's red-proof discharges in openxFactory, retargeted at the consumer
gate** — not in the new repository. `review-authority-intake/spec.md:30-33` confers
authority only where the reader "runs as a REQUIRED check on the repository that
holds the register", and R6 keeps the register here; openXwallet's tree has no
`governance/review-authority/` for a malformed row to sit in. The red-proof is
therefore a deliberately malformed row under openxFactory's
`governance/review-authority/` turning an openxFactory pull request red.

### The cutover runbook, and it is P2's own artifact

`docs/openxwallet-cutover-runbook.md` lands in openXwallet's scaffold (code_surface,
and AUTHORIZED as part of P2) because a wave of this shape cannot be carried in a
proposal's prose. **Ordered and REVERSIBLE, with a rollback per phase.** Its
contents, named so the bench reviews a procedure rather than an intention:

1. **A case-variant repository-name check BEFORE the carve.** GitHub repository
   names are case-insensitive-unique, so `openxwallet` and `OpenXWallet` in the org
   — and in any fork — collide with `openXwallet`. Checked and recorded first,
   because discovering it after a carve costs the carve.
2. **Repository creation**, then the `git filter-repo` carve over the twelve path
   sets, with a **completeness check**: every file under the twelve paths is present
   in the carved tree. Two path sets are named explicitly because a shorthand loses
   them — `specs/006-openxwallet-contracts/evidence/` and
   `contracts/openxwallet/examples/negative/`.
3. **CODEOWNERS**, then the new repository's **ruleset in EVALUATE mode** → one
   trivial pull request so `wallet-validation` reports once and becomes selectable →
   **promote to ACTIVE**. Stated plainly in the runbook: **day-one REQUIRED is
   impossible**, because GitHub cannot require a check that has never reported.
4. **Tag `wallet-v1.0`** only after the byte-identity proof against the named carve
   commit.
5. **Submodule init in openxFactory and in the xFactory aggregation**, then the
   byte-identity proof re-run from each consuming checkout.
6. **Rollback per phase**, each written before the phase is taken.

### Sequencing that is not negotiable

1. P5a.1 merges before P3 — before P2, in fact (Ledgerx fails loudly) — and P5a.2,
   the `stack.yaml` bump to the P2.5 minor, merges AFTER P2.5 is cut and before P3,
   because one pull request cannot both precede P2 and pin a bundle P2.5 has not
   published.
2. `wallet-v1.0` exists before P3 merges (keeps openxFactory main bisectable), and
   **`wallet-v1.1` exists before P3 merges too**, because openxFactory's pin at P3
   is `wallet-v1.1`: the nested-repository prune P3's REQUIRED sweep depends on is
   the product's code, cut as P2b, and the byte-identity floor is proven against
   `wallet-v1.0` at the named carve commit either way.
3. P2.5's deprecation minor is PUBLISHED before P3's major
   (`docs/contract-versioning-policy.md:250-254` requires one full minor release in
   which the old shape produced deprecation warnings, ahead of a breaking removal).
4. P3 is one atomic pull request (the trust-anchor hard exit).
5. **No ruleset act gates P3.** The required token `wallet-validation` survives
   P3 as the new workflow's job id (§ The REQUIRED check), so ruleset 21538893 is
   edited in this wave by nothing; openXwallet's own ruleset is bootstrapped in
   EVALUATE mode and promoted to ACTIVE after its first report, per
   `docs/openxwallet-cutover-runbook.md`.
6. S3/S5 of `add-wallet-carried-review-authority` author any `openxwallet` core
   delta after the split, in openXwallet.
7. **P3b and P4 land in the SAME WAVE as P3.** P3b because the floor gap it closes
   opens the moment the gitlink exists (V6); P4 because between P3's merge and
   P4-plus-`--init` neither gitlink candidate exists in any checkout, and it must be
   done before LedgerxFactory's next estate run (V3).
8. **The register row's expiry is a hard clock on this wave.**
   `governance/review-authority/register.yaml:37` carries
   `expires_at: "2026-11-23T12:00:00Z"`, and `check_register` raises
   `register-row-expired` as an **error** once that instant passes
   (`scripts/validate-openxwallet.py:1961-1965`), which reds the REQUIRED gate on
   every pull request thereafter. So either **the row is re-issued before
   2026-11-23**, or **P3 is not scheduled after 2026-11-01**: a wave that lands into
   an expired register cannot produce a green consumer gate, and the wave's own
   evidence rows would be unfillable.
9. **The declared manifest freeze is UNENFORCEABLE, so P3 re-verifies.** A freeze on
   `contracts/manifest.yaml` and the README Records block across P2.5 → P3 cannot be
   enforced across sessions in a shared checkout. **P3 therefore REBASES and
   RE-VERIFIES the eight digests immediately before merge**, and that
   re-verification — not a P2-era artifact reused — is what P3's evidence row
   carries.
10. **NOT a precondition, contrary to an earlier reading:** the hermes-install
   reseed-drift fix. Wallet content is not in `CONTENT_KINDS` and is not
   domain-overlay content, so the reseed path is untouched.

## Capabilities

### New Capabilities

- **`domain-descendant-boundary`** — the general standard for how a domain consumes
  a neutral open\* product, generalized from the three precedents and citing each as
  what it actually is (## Why). Four rules: **(a)** a descendant pins the product BY
  COMMIT, TWICE — the nested gitlink and a pin manifest at
  `contracts/<product>-pin.yaml`
  (`kind: <descendant_repo_snake>_<product_snake>_pin`, following
  `medxchart_openchart_pin` / `medx_avatar_openavatar_pin`;
  `relationship: pinned_upstream_composition` where the pin covers a whole tree) —
  both changed in the SAME commit, so a gitlink can never silently disagree with a
  declared pin. The three live pin files disagree on directory and kind form
  (`MedxChart/contracts/openchart-pin.yaml`; `MedxAvatar/pins/openavatar.yaml`, which
  carries `source_repo`/`resolved_ref` and no `relationship:`; openAvatar's
  `avatar-client-lab-contract-pin`); this rule settles the shape FORWARD and does not
  retro-fit the existing two; **(b)** it carries ONLY profiles, overlays, branding,
  deploy config and domain validators — **pin and profile, never fork** — and anything
  the profile cannot express is an upstream change; **(c)** a descendant is aggregated
  at one of two placements, whose STANDING differs and is stated rather than blended
  — **RATIFIED:** nested into its DomainxFactory as a submodule (`MedxAvatar` in
  `MedxFactory`, DTN-022, 2026-08-03). **REALIZED BUT NOT YET RATIFIED:** the
  aggregation's `xFactories/` (`MedxChart`, 2026-08-23, whose establishing act
  `create-medxchart-overlay-boundary` is still `Status: draft`) — permitted here, and
  confirmed as ratified precedent when that change archives. The choice between them
  is the owning domain's, on whether the descendant needs standalone cloning; it MAY
  carry both. (Corpus fact behind the rule: `MedxFactory/.gitmodules` carries ONLY
  `MedxAvatar`, and `MedxChart` exists only at `xFactories/MedxChart`.) **(d)** it is
  created LAZILY and CONSUMER-GATED: **a `<Domainx><Product>` repository SHALL NOT be
  created before the domain tree carries at least one artifact of the product's
  profile kind.**
- **`neutral-product-pin`** — how openxFactory consumes an EXTERNAL neutral product,
  which it has never done in this DIRECTION. The pin GRAMMAR is not new: it is the
  ratified `pinned_contract_manifest` shape (keycloak-install's `identity-brokering`
  manifest, openxpki-install's `trust-anchor` manifest) — commit + `revision_kind` +
  per-file sha256 + `pinned_by_commit_only`, with a tag-only pin already refused in
  that shape's own words ("A tag-only pin is refused: a tag can be moved").
  `contracts/openxwallet-pin.yaml` REUSES `kind: pinned_contract_manifest` unchanged;
  what is new is only that openxFactory is the consumer. What this capability
  therefore ADDS, because nothing states it in this direction: **fail closed** on an
  uninitialized submodule or a digest disagreeing with the pin — an unanswerable
  question is never an implicit pass; **the PINNED validator and the PINNED reader
  are what a REQUIRED check runs**, so "which reader ran" is an auditable digest
  rather than an assumption; **the declared pin for an external neutral product is
  `contracts/<product>-pin.yaml`, not `stack.yaml`** — a reverse-direction pin that
  `shared-contract-ownership:146`'s stack.yaml rule does not reach; and **a neutral
  product repository MAY keep a digest-pinned copy of one openxFactory contract, and
  MUST identify the openxFactory contract version it pins** — mirroring
  `shared-contract-ownership:27`, which is scoped to INSTALL repos and so does not
  license the reverse vendoring on its own. openXwallet carries that vendored copy at
  `contracts/schemas/hermes-job-envelope.schema.yaml`, which is also why the `:142`
  publisher-marker test is satisfied in the new repository.

  **Four further rules this capability carries, each added on council evidence:**

  **Pin authority when several checkouts are reachable** (V3). Where more than one
  checkout of the product is reachable from a consuming tree, **the pin recorded in
  the CONSUMING repository is authoritative and a resolver SHALL prefer it**; and
  **the aggregation's root gitlink for a product openxFactory pins SHALL equal
  openxFactory's nested gitlink commit**, checked in the aggregation. Without this,
  a walk-up resolver in a consumer repository silently reads whichever checkout it
  meets first — the aggregation root or openxFactory's nested one — and only the
  latter is governed by `contracts/openxwallet-pin.yaml`.

  **The vendored foreign contract is digest-verified before it is read** (V8). A
  neutral product repository that keeps a digest-pinned copy of an openxFactory
  contract SHALL verify that copy against its own `contract_pin.yaml` before reading
  it, and **an unverifiable copy refuses the run**. Presence is not identity:
  `scripts/validate-openxwallet.py:2124` checks only
  `ENVELOPE_SCHEMA_PATH.is_file()` today, while openAvatar's
  `contract_pin.yaml:15-21` shows the house fail-closed shape.

  #### Scenario: One pull request changes both the pin and the register (V6)
  - **WHEN** one pull request changes the product pin or its gitlink AND any file
    under the review-authority register's directory
  - **THEN** the pull request is human-only, because a candidate could otherwise
    repoint the very reader that judges its own change

  #### Scenario: A required check invokes the pinned validator with no scan target (V7)
  - **WHEN** a required check invokes a pinned validator without a scan target
  - **THEN** the check REFUSES rather than self-tests, because a self-test that
    reads no register is a green check that verified nothing

**Why new capabilities and not deltas on `repo-boundary-governance`.** It carries the
org's boundary requirements one product at a time — "Neutral installer repository
integration", "Neutral avatar-client repository boundary", "Avatar-client contract
ownership and consumer pinning". That per-product shape is precisely the cost ## Why
identifies; a general standard authored as a fourth product-named requirement would be
the fourth bespoke boundary wearing a general name. `shared-contract-ownership` is a
different case and IS engaged — one MODIFIED delta, declared below.

### Modified Capabilities

- **`trust-anchor`** — **declared relative to the active change `add-trust-anchor`,
  not against a promoted spec.** `trust-anchor` is NOT in `openspec/specs/`; its 8
  requirements are ADDED by that change (ratified 2026-08-21, code surface
  unrealized). Per `release-realization`'s ordered-delta rule (`:64-79`) the delta
  references that change AND declares itself relative to its OUTCOME, restating the
  target requirement's full text as that change will promote it. **One honesty note on
  that rule: its letter covers a requirement already MODIFIED by an active ratified
  change; these requirements are ADDED, so this proposal applies the rule by PARITY
  and declares the parity rather than implying the letter.**

  **The modification is a dangling cross-corpus reference, not a code change.** The
  target requirement *Declared chain custody bounds what a certificate evidences*
  (`openspec/changes/add-trust-anchor/specs/trust-anchor/spec.md:69-99`) says only
  "composing with `openxwallet`'s ratified rule that custody caps what a signature
  evidences instead of restating a second custody model" — which, after the shed,
  names a capability this corpus no longer holds and supplies no resolution path. The
  delta rewrites that clause to "…composing with the `openxwallet` capability's
  ratified rule, consumed from `opensoft/openXwallet` at the pin recorded in
  `contracts/openxwallet-pin.yaml`, that custody caps what a signature evidences…"
  and ADDS one scenario: **WHEN the pinned openXwallet checkout is uninitialized or
  its custody-registry digest disagrees with the pin THEN the custody question is
  refused rather than resolved.**

  The code that realizes it is P3's surface, not the requirement's text: the
  chain-custody set's openxWallet counterpart resolves from the PIN rather than from
  `ROOT/contracts/openxwallet/` (`scripts/validate-trust-anchor.py:322-323`), and rule
  (f) (`:1146-1176`) fails closed on an uninitialized submodule or a digest
  disagreeing with the pin — replacing today's bare file-absent exit at `:2582-2586`.
  The composition is otherwise unchanged: two registries, one custody question, still
  checked at run time.
- **`shared-contract-ownership`** — one MODIFIED delta declared, on *Tooling hosted in
  the publisher verifies released bytes, not a declared pin* (`:139-165`). Shedding
  the wallet validator removes a publisher marker for that family — the requirement's
  own test is that "a checkout SHALL be treated as a publisher release only when it
  carries all of `contracts/manifest.yaml`, `contracts/schemas/`, and the contract
  family's own validator… A tree missing any marker is NOT a publisher and SHALL take
  the consumer path with its declared pin intact" — and the consumer path it names is
  written only for a `stack.yaml`-declared openxFactory release. The delta states the
  THIRD case: where openxFactory is the CONSUMER of an external neutral product, the
  declared pin is `contracts/<product>-pin.yaml` rather than `stack.yaml`, and the
  byte chain, the fail-closed rule and the manifest-parity obligation run unchanged.
  *Canonical contract home* (`:8-31`) needs no delta — the pin is the scenario's `or
  referenced` limb.
- **`review-authority-intake`** — **declared relative to
  `add-wallet-carried-review-authority`**, for the same reason: not promoted, existing
  only as that change's 12 ADDED requirements, and by the same parity reading of the
  ordered-delta rule. The modification is to the requirement titled, verbatim, **"A
  grant with no reader in a required check confers nothing"**
  (`openspec/changes/add-wallet-carried-review-authority/specs/review-authority-intake/spec.md:30-40`:
  "A review-authority grant SHALL confer no authority until a named validator that
  reads it runs as a REQUIRED check on the repository that holds the register"). Its
  scenario at `:38-39` — "WHEN `scripts/validate-openxwallet.py` (or the register's
  own validator) is present in the repository but appears in no workflow that is a
  required check" — becomes UNSATISFIABLE after P3, because the validator is no longer
  present in this repository at all. The delta rewrites the WHEN to "…is **reachable**
  in the repository, in-tree or through a digest-pinned submodule, but appears in no
  workflow that is a required check". After the split the reader is a DIGEST-PINNED
  TOOL invoked by a required consumer check in the repository holding the register,
  and the pin's digest is what makes "which reader ran" auditable. This STRENGTHENS
  the rule rather than narrowing it. What does not change: the register's location,
  its human-only floor, or the fact that it is openxFactory's own review authority.

  **The delta extends to every dangling wallet path the arc holds, not only that one
  scenario** (V12). Three citations in `review-authority-intake/spec.md` resolve into
  paths that leave this repository, and each is repointed in the same delta:
  **`:10`** cites `contracts/openxwallet/openxwallet-custody.registry.yaml:15-37` for
  the closed `authority_tiers` ladder — repointed to the PIN plus the pinned
  checkout, since the tiers themselves (`attest`, `request`, `act`,
  `act_unsupervised`) are unchanged bytes at the carve commit; **`:15`** cites
  `openspec/specs/openxwallet-agent-profile/spec.md:50-69` and **`:208`** cites
  `:27-48` of the same file — both repointed to **openXwallet's own OpenSpec instance
  at the recorded pin**, which is where those promoted specs live after the exit.
  Left unrepointed, the arc's own authority-vocabulary rule and its composition-drift
  rule would each cite a corpus member openxFactory no longer holds.

### Removed Capabilities — and exactly how the corpus exit is expressed

**`openxwallet`** (8 requirements) and **`openxwallet-agent-profile`** (3) leave the
openxFactory corpus for **`opensoft/openXwallet`**.

**The mechanism, with the rule cited.** `document-lifecycle`'s requirement
"Ratified spec deltas reach the promoted specification"
(`openspec/specs/document-lifecycle/spec.md:520-598`) is the only rule in this
corpus stating how a promoted requirement legitimately stops being promoted: "a
requirement it REMOVED SHALL be absent", with the scenario *A ratified delta removes
a requirement* — "the promoted spec MUST NOT carry that requirement thereafter"
**AND** "a requirement still present after its ratified removal MUST be reported".
The same requirement supplies the authority rule: "The authority for a requirement
is the MOST RECENT archived delta that touches it, and that one alone."

So the exit is **two `## REMOVED Requirements` deltas naming all eleven requirement
titles verbatim.** They are listed here, not merely described, because the titles ARE
the join key. The eight of `openxwallet`:

1. A wallet is a key, never a record of a key
2. Authority travels as attenuated grants, never as keys
3. Use requires proof of possession, not presentation
4. Custody is declared and bounds what a signature evidences
5. Every exercise is key-attributed
6. Revocation propagates through the chain
7. Distinct-holder constraints are expressible
8. The capability is an authority control, never an identity substrate

and the three of `openxwallet-agent-profile`:

9. An agent holder declares its composition
10. A composition change revokes the agent's grants immediately
11. Agent authority is grant scope, not a parallel vocabulary

All eleven verified byte-identical against both promoted specs and the archived
`2026-08-08-add-openxwallet` delta. **`scripts/doc_health/promotion_fidelity.py` keys
on (capability, normalized title)**, so ONE character of drift in a title leaves the
2026-08-08 `ADDED` writer authoritative and the removal invisible to the checker.

`openspec archive` applies them, the promoted specs empty, and the two capability
directories go with their last requirement. **This is the first
`## REMOVED Requirements` block in this corpus** — a grep across `openspec/` returns
none today — stated so the bench reviews a first use knowingly rather than assuming a
precedent. The exit is nevertheless TOOLING-SUPPORTED and not merely legal:
`scripts/doc_health/promotion_fidelity.py:144` already carries
`CHECKED_OPS = ("ADDED", "MODIFIED", "REMOVED")`, and `:820-824` already emits the
"ratified REMOVED requirement … is still present" finding.

**Three things this deliberately does NOT do.** No `superseded` header on a spec
file: the controlled taxonomy governs governance DOCUMENTS, and borrowing a document
status to express a capability move would invent a mechanism. No emptied stub spec
left as a signpost: a requirement-less `openspec/specs/openxwallet/spec.md` is a
corpus member asserting a capability openxFactory no longer owns, which is worse
than absence because it reads as canon. No archived-record edits:
`openspec/changes/archive/2026-08-08-add-openxwallet/` and
`docs/archive-record-discrepancies.md` row 7 are records, ANNOTATED with the
carry-forward and never rewritten into agreement.

**The successor location is recorded in three places that survive the archive:** each
REMOVED delta's header prose; `contracts/openxwallet-pin.yaml`, the live
machine-readable pointer; and `contracts/README.md` (rows 106-108 collapsing to one
"consumed at pin" row) plus the CHANGELOG entry for the cut.

**Ordering, stated so the window is not a surprise.** Both promoted specs stay in
canon until this change ARCHIVES, and archiving is gated on merged-plus-green
evidence. Between P3's merge and the archive, canon describes contracts openxFactory
no longer holds — exactly the realization window `release-realization` defines
("active changes describe approved intent not yet realized") — and it must be closed
in the same wave rather than left open.

### Declared NOT modified, with the reason

- **`shared-contract-ownership` — DECLARED, not omitted; it was the closest call in
  the change and it resolved the other way.** *Canonical contract home* (`:8-31`)
  needs no delta — `contracts/openxwallet-pin.yaml` is the scenario's `or referenced`
  limb (`:18`). But *Tooling hosted in the publisher verifies released bytes, not a
  declared pin* (`:139-165`) IS engaged, and the one MODIFIED delta lands there; see
  ## Modified Capabilities above. Two corrections that go with it: the reverse
  vendoring is **not** licensed by *Subsystem adapter needs a contract* (`:25-27`),
  whose text is scoped to an INSTALL repo ("an install repo needs a runtime adapter,
  generated client, smoke fixture, or pinned schema copy"), so the permission is
  stated in `neutral-product-pin` instead; and the consumer path at `:146` is written
  only for a `stack.yaml`-declared openxFactory release, which is exactly the gap the
  delta closes.
- **`identity-brokering` — NOT declared.** Its two `openxwallet` references
  (`openspec/changes/add-identity-brokering/specs/identity-brokering/spec.md:196`,
  `:211`) name the capability, not a path or a corpus member; after the split they
  resolve to `opensoft/openXwallet` through `contracts/openxwallet-pin.yaml`.
- **`neutral-job-envelope` — NOT declared.** A new external consumer appears at a
  digest pin; the schema, its kind and its vocabulary are untouched.
- **`release-surface-integrity` — NOT declared.** The cut owes a
  `contracts/releases/<tag>.digests.yaml` over its own release surface: an existing
  obligation discharged, not amended.
- **`repo-boundary-governance` — NOT declared.** Its neutral-repo requirements are
  per-product and none is the wallet's; the general standard lands as
  `domain-descendant-boundary`. Nor is the PIN GRAMMAR new to it: the
  `pinned_contract_manifest` shape this change reuses is already realized twice under
  its per-product requirements —
  `installs/keycloak-install/config/contracts/identity-brokering/manifest.yaml:1-20,45-58`
  and `installs/openxpki-install/config/contracts/trust-anchor/manifest.yaml:55` — so
  the DIRECTION is the delta, never the shape.
- **`doc-health` — NOT declared.** No finding class, family or severity changes; the
  corpus shrinks by two capabilities, which every family already handles.

## Impact

- **openxFactory.** `contracts/openxwallet/` and
  `contracts/openxwallet-agent-profile/` deleted; `scripts/validate-openxwallet.py`
  (path constants `:213-218`, register reader `:1780-1787`),
  `scripts/wallet-yaml-syntax-gate.py` and `tests/wallet_yaml_syntax_gate/` deleted;
  `scripts/validate-trust-anchor.py` (`:322-323`, `:1146-1176`, `:2582-2586`) and
  `tests/trust-anchor/` repointed to the pin;
  `.github/workflows/wallet-validation.yml` → `openxwallet-consumer-gate.yml`
  (nested-submodule checkout with the app-token + `insteadOf` pattern, verify pin
  digests, then run the pinned gate and the pinned validator by the LITERAL
  invocation `python3 openXwallet/scripts/validate-openxwallet.py .` from the
  openxFactory root — which is what reads `governance/review-authority/`, per R6;
  there is no "authority-register mode" to build, and the sweep's skip of the
  `openXwallet/` gitlink directory is upstream code at `wallet-v1.1`, not an
  openxFactory edit — P2b);
  **`.github/workflows/pytest-suite.yml` — omitted from the extraction plan and a
  REQUIRED check.** Its checkout (`:203-206`) carries `path: openxFactory` and
  `fetch-depth: 0` and NO `submodules: true`, so it gains one; it runs `pytest tests/`
  including `tests/trust-anchor/` (whose `test_negative_corpus.py:60,68` read
  `ctx.openxwallet`, repointed to read the wallet registry through the `openXwallet/`
  gitlink) and the DELETED `tests/wallet_yaml_syntax_gate/`, so the pinned collection
  count in its header (`:37`, `5877 + 17 + 338 = 6232`) moves; and its three
  references to `wallet-validation.yml` (`:5`, `:14`, `:148`) become
  `openxwallet-consumer-gate.yml`;
  `.github/CODEOWNERS` drops the two validator lines (`:3-4`) and gains the pin and
  the gitlink; `contracts/manifest.yaml` loses the eight rows at `:1967-2082` and
  rewords the seven incoming citations at `:2089`, `:2146`, `:2251`, `:2287`,
  `:2423`, `:2473-2475`, `:2494-2495` (each an "…and openxWallet precedent" or a
  custody-correspondence reference — reworded to the pin, never deleted, because the
  precedent they cite still holds); `contracts/README.md:106-108` → one row;
  `contracts/CHANGELOG.md` gains the cut's entry; `README.md` at `:217-228` (the
  Wallet validation gate section, which names the workflow FILE that is renamed while
  the ruleset TOKEN is deliberately unchanged), `:286-293`
  (the openxWallet contract-index entry), `:310` (the trust-anchor index entry's
  citation of openxwallet's custody rule — reworded to the pin, not deleted), `:805`
  (the same custody-composition citation in the `add-trust-anchor` ledger entry),
  `:873-927` (the `add-wallet-carried-review-authority` ledger entry — `:896`'s
  "advisory until an operator marks it required" is already STALE against ruleset
  21538893 and is corrected in this wave; `:909-912`'s declined-floor prose stands
  unchanged; `:920-921` names the retiring workflow AND both departing scripts),
  `:2523-2536` (the `add-openxwallet` archive-ledger entry — **not** `:2254-2265`,
  which is `align-demote-to-round-trip-rule`) and `:2612`;
  `docs/openxdox-naming.md` Amendment 2; `docs/archive-record-discrepancies.md` row 7
  gains a "carried to openXwallet" note. **`governance/review-authority/` STAYS —
  all four files.**
- **`opensoft/openXwallet` (new).** Everything in `code_surface` (1). Its own OpenSpec
  instance receives the two promoted specs. The `## Purpose` placeholder is in BOTH
  PROMOTED SPECS, not in the archive: `openspec/specs/openxwallet/spec.md:4` and
  `openxwallet-agent-profile/spec.md:4` each read "TBD - created by archiving change
  add-openxwallet. Update Purpose after archive." Both are written while they are
  being moved.
- **xFactory aggregation.** `.gitmodules` and a root `openXwallet/` gitlink; README
  Terms and the layout block; `CLAUDE.md` orientation line **and working rule #1**,
  which this change makes false as written.
- **LedgerxFactory — larger than the plan counted, and it is THREE pull requests.**
  P5a.1's forward-compatible finder and P5b's fallback drop are both in
  `tests/validate_wallet_estate.py:47-66` (`find_openxfactory()` at `:47-63`,
  `VALIDATOR = find_openxfactory()` at `:66`); P5a.1 lands before P2, and P5a.2 —
  the `stack.yaml` bump to the P2.5 minor plus the pinned-checker invocation that
  makes the `relocating:` warning observed — lands between P2.5's cut and P3. P5b
  then repoints, each verified present:
  `specs/016-posting-segregation-of-duties/quickstart.md:15`, `plan.md:27`,
  `spec.md:63`, `README.md:220` (**not** `:112-135`, which is concept prose with no
  wallet path), and the ownership comment at
  `tests/validate_document_estate_surface.py:1046-1075`. **Two items are distinct
  kinds of work, not path edits.** (i)
  `specs/016-posting-segregation-of-duties/data-model.md:5` is a COMMIT pin —
  "`openxFactory/contracts/openxwallet/*.schema.yaml` at `e5554028`" — which needs a
  NEW repository and a NEW commit, not a rewritten path (the same commit also appears
  at `plan.md:26`, `quickstart.md:4` and `spec.md:376`). (ii)
  `openspec/changes/modify-ledgerx-posting-authority-for-segregation-of-duties/tasks.md:81`
  is inside an ACTIVE change, so its repoint is a live-change edit rather than a
  record annotation.
- **OpsxFactory — six references, exactly one of them path-bearing.** Enumerated with
  the full prefix, because the plan's shorthand loses it. Inside
  `openspec/changes/add-keycloak-administration-workflow/`:
  `supporting-docs/identity-pki-administration.md:59`, `:294` and `:417`, and
  `specs/keycloak-administration/spec.md:150`. At the repository root:
  `credentials/requirements.yaml:514` and `workflows/keycloak-administration.yaml:56`.
  **`supporting-docs/identity-pki-administration.md:417` is the ONLY path-bearing one**
  — it names `openspec/specs/openxwallet/spec.md`, which after the split lives in
  openXwallet's own OpenSpec instance — and it is what P5b repoints. The other five
  name `openxwallet` as a CONCEPT (grants, holders) with no path and **need
  nothing**.
- **codexFactory — ONE required change, P3b.** Reversing this proposal's earlier
  "NO change" claim (V6). The register stays, so the floor's pinned path still
  resolves — but the floor protects only
  `governance/review-authority/register.yaml`, and `matching_paths` is exact set
  membership, so after P3 the pin and the gitlink that determine WHICH READER RUNS
  are outside the floor entirely. P3b adds `contracts/openxwallet-pin.yaml` and
  `openXwallet` to `never_clearable_paths`, in the same wave as P3, with its own
  realization-evidence row.
  **Recorded as PRE-EXISTING and explicitly NOT this change's scope:** the same
  floor file omits `governance/review-authority/grants/`, `…/wallets/` and
  `…/attestations/`, so today a grant, wallet or attestation file can be edited
  outside the floor while only the register index is protected. That is a finding for
  the owner of `add-wallet-carried-review-authority`, which created those
  directories; this change neither fixes it nor depends on it. Likewise
  lead-security's 2026-08-26 finding that the floor path is unreachable in the
  checked tree remains a pre-existing codexFactory issue, neither fixed nor depended
  upon here.
- **`add-wallet-carried-review-authority` — four LIVE-CHANGE edits, not record
  annotations** (V12). `tasks.md:81` (`python3 scripts/validate-openxwallet.py
  <checkout> --strict`), `:100` (`validate-openxwallet.py .`), `:134`
  (`scripts/validate-openxwallet.py`) and `:204` (the wallet-validation check named
  by the same script path) each name the departing script inside an ACTIVE change,
  so each is edited rather than annotated — the same treatment
  `modify-ledgerx-posting-authority-for-segregation-of-duties/tasks.md:81` gets in
  LedgerxFactory. Its `tasks.md` 8.1 ruling (`:317-330`) needs no edit; it is cited
  in ## Why as this change's timing evidence.
- **MedxFactory — no change.** Its brainstorm links point at
  `openxFactory/ideation/brainstorm/agent-certification-wallets.md`, which stays.
- **hermes-install — no change.** Wallet content is not in `CONTENT_KINDS` and is not
  domain-overlay content; the reseed path is untouched and S3/S5's hermes-install
  work is unaffected.
- **keycloak-install / openxpki-install — no change.** Doctrinal citations only.
- **NotebookLM and doc-health: aggregation tooling does NOT see a root-level repo,
  so nothing derives automatically** (V10, replacing this proposal's earlier
  "derives automatically … nothing to design"). Two code sites, both verified:
  `scripts/sync-notebooklm-books.py:761` builds its repository set as
  `["openxFactory", *pinned_factory_paths(root)]`, and `pinned_factory_paths`
  (`:644-663`) matches only `^\s*path\s*=\s*(xFactories/\S+)\s*$` — a root-level
  `openXwallet` pin is invisible to it. `scripts/doc_health/ideation_routing.py`
  `_governed_repo_ids` (`:225-235`) admits only `openxFactory` and
  `xFactories/<Name>`, so a root-level `openXwallet` is classed **EXTERNAL** and its
  references fall under the nightly-skip / strict-materialization path. The living
  proof is that **there is no `xf-ideation-openavatar` book today**, five months into
  the ratified openAvatar precedent. Carried as successor **P4b**.
- **`contracts/releases/*.digests.yaml` never indexed the wallet family.** Nothing to
  carry across. **Recorded as a gap, deliberately NOT backfilled** — a backfill
  inside a move that must stay byte-identical would destroy the one property the move
  is safe on.
- **Immutable records are annotated, never rewritten:**
  `health/document-catalog/runs/**` snapshots, the archived
  `2026-08-08-add-openxwallet` packet, the `cl-openxwallet` cluster in
  `ideation/cross-reference.yaml`, and `docs/archive-record-discrepancies.md`.
- **Prose-only citations, reworded to the pin and NOT deleted.**
  `scripts/validate-identity-brokering.py:118`, `:165`, `:748`;
  `contracts/CHANGELOG.md:20`, whose additive-minor worked example names a path that
  leaves the repository; `README.md:805` and `:2612`; and
  `scripts/proposal-support.py:978`, which names `add-openxwallet` in a
  staged-origin-shape comment. **`health/` and `scripts/doc_health/` carry no wallet
  reference at all** — verified by grep, and that is what makes the `doc-health`
  non-declaration safe rather than merely plausible.
- **Carried STALE, deliberately NOT corrected.** `contracts/manifest.yaml:1968-1969`
  says "16 valid + 33 intended-invalid" and `contracts/README.md:108` says "nineteen
  rules" over "16 positives and 33 intended-invalid negatives"; the tree is **17
  positives, 36 negatives and 21 rules `(a)`–`(u)`**. Correcting them INSIDE a
  byte-identical move would destroy the one property the move is safe on. The
  correction is a successor in openXwallet, named below.
- **No gate is weakened and no bypass removed.** The one live requirement in play
  (ruleset 21538893) is not touched at all: its token `wallet-validation` survives P3
  as the renamed workflow's job id, so the check reports on P3's own pull request and
  no operator act stands between P3 and merge. The ruleset appears in realization
  evidence as an UNCHANGED-STATE row, which is what makes the claim checkable rather
  than asserted.

## Realization evidence

Required by `release-realization`'s *Realization archive gate*
(`openspec/specs/release-realization/spec.md:22-46`): a code-surface change archives
only on merge evidence plus, where the surface is runnable, a green run of it. **One
row per surface, and the table is a gate, not a report** — every cell filled before
this change may archive.

| # | Surface | Repository | PR | Merge commit | Green check + run id |
| --- | --- | --- | --- | --- | --- |
| P2 | carve + scaffold | `opensoft/openXwallet` | [#1](https://github.com/opensoft/openXwallet/pull/1) | `936ceb2066705d82fa60b333bea3babe6297a1b7` | first green `wallet-validation`, plus the carve-completeness check over the twelve path sets (`specs/006-openxwallet-contracts/evidence/` and `contracts/openxwallet/examples/negative/` named explicitly) — run **33024308629**, job **98361927764**; the completeness diff of the two sorted listings is EMPTY at 100 files (tasks §3.5–3.6) |
| P2 | runnable half | `opensoft/openXwallet` | [#1](https://github.com/opensoft/openXwallet/pull/1) | `936ceb2066705d82fa60b333bea3babe6297a1b7` | first green `pytest-suite`, plus the byte-identity proof of the eight rows **against the NAMED CARVE COMMIT** `30565e48ffe3d8a9773e10af33425701845e10f6` — run **33024308567**, job **98361927209**; part one 8/8 three-way, part two 100/100 at the carve layer and 97/100 after the scaffold (tasks §3.23–3.24) |
| P2 | vendored-schema verify (V8) | `opensoft/openXwallet` | [#1](https://github.com/opensoft/openXwallet/pull/1) | `936ceb2066705d82fa60b333bea3babe6297a1b7` | the `wallet-validation` log line showing the vendored `contracts/schemas/hermes-job-envelope.schema.yaml` digest-verified against `contract_pin.yaml` BEFORE the validator ran, plus a red run with a mutated copy — `wallet-validation` run **33024308629**, job **98361927764**, whose log shows the digest verified 253 ms before the validator started; the refusal on a mutated copy was observed locally (exit 1, both remediation strings) and is recorded at tasks §3.30, with no separate CI run id |
| P2b | `wallet-v1.1` — nested-repository prune + register-read note | `opensoft/openXwallet` | [#2](https://github.com/opensoft/openXwallet/pull/2) | `63f5a1adac89f017e70bab9a4ffe7cf02d6e6705` | the one auditable additive-minor diff, green `wallet-validation` and `pytest-suite` at the tag, a run proving a YAML file inside a nested repository is no longer swept, AND a green LedgerxFactory estate run on the v1.1 reader (its `--strict` invocation must stay green, and the register-read line must be a NOTE) — `wallet-validation` run **33035937510**, job **98398510254**; `pytest-suite` run **33035937545**, job **98398510215**; the prune tests are `tests/nested_repo_prune/test_prune_and_register_note.py` (tasks §4.4); the estate run is recorded at tasks §4.9 — candidate 1 resolved against a live rival, `repo scan: 5`, `0 error(s), 0 warning(s)` under `--strict`, the register read emitted as a NOTE |
| P2.5 | deprecation minor | `opensoft/openxFactory` | [#417](https://github.com/opensoft/openxFactory/pull/417) | `af7ac0fa4d31ffeec45524a0fe74524ba5b5b22c` | the eight `relocating:` rows, the CHANGELOG migration note, the emitting checker's warning output, AND the minor's own `contracts/releases/<tag>.digests.yaml` — `wallet-validation` run **33086366248**, job **98566978151**; `pytest-suite` run **33086366020**, job **98566975887**; the tag is `contract-v1.47` (renumbered from the proposed v1.46 at merge order) and its `contracts/releases/contract-v1.47.digests.yaml` carries 192 members; the checker's WARN output is the one quoted in LedgerxFactory [#29](https://github.com/opensoft/LedgerxFactory/pull/29) |
| P3 | consume + shed (major) | `opensoft/openxFactory` | [#431](https://github.com/opensoft/openxFactory/pull/431) | `c9a1500e1a960be827cd714d8024d9aacb40aeb2` | green `wallet-validation` (the token, from the renamed `openxwallet-consumer-gate.yml`) on P3's own head; the digests RE-VERIFIED post-rebase immediately before merge — post-rebase head `746fe3f9`, `wallet-validation` run **33115267228**, job **98668176860** (24s); the post-merge re-verify printed `OK openxwallet-pin verified: openXwallet@63f5a1adac89f017e70bab9a4ffe7cf02d6e6705 (tag label wallet-v1.1), gitlink read from HEAD, 8 digest(s) recomputed`. `c9a1500e` is the commit tag `contract-v2.0` resolves to |
| P3 | the reader actually RAN (V7) | `opensoft/openxFactory` | [#431](https://github.com/opensoft/openxFactory/pull/431) | `c9a1500e1a960be827cd714d8024d9aacb40aeb2` | the consumer gate's log carrying the `repo scan: N openxWallet artifact` note AND carrying neither `no intake register at this tree` nor any `register-*` finding code — the positive conjunction the pinned reader actually produces, since `check_register` names the register path on failure only — plus the `wallet-v1.1` register-read NOTE naming the resolved path, **plus the task-2.6 red-proof run id**. A green check that proves no register was opened is a vacuous pass. The green half is `wallet-validation` run **33115267228**, job **98668176860**, whose log carries `intake register read: governance/review-authority/register.yaml (1 row(s))` and no `register-*` code. The **red-proof is run 33109857156, job 98649492960** (21s, `[register-row-malformed]` naming the full path), on draft pull request [#432](https://github.com/opensoft/openxFactory/pull/432) — branched from #431 so the gate under test is the one P3 installs, **CLOSED and never merged, by design**, which is why it is not its own surface row |
| P3 | `pytest-suite` under nested submodules (V9) | `opensoft/openxFactory` | [#431](https://github.com/opensoft/openxFactory/pull/431) | `c9a1500e1a960be827cd714d8024d9aacb40aeb2` | the pinned **PASS / SKIP counts**, not collection alone, so a silently skipped `tests/trust-anchor/` is distinguishable from a passing one — `pytest-suite` run **33115267254**, job **98668260667** (14m39s) on the post-rebase head; the pinned counts are read from run **33111235491**: `selected=7090 passed=7070 skipped=20 failures=0 errors=0` |
| P3b | codexFactory floor widening (V6) | `opensoft/codexFactory` | [#117](https://github.com/opensoft/codexFactory/pull/117) | `58bd3cf79b91da26aced95c2000576981d9445c8` | the `openxfactory-review-authority-floor.yaml` diff adding `contracts/openxwallet-pin.yaml` and `openXwallet`, plus the merged pull request — `validate` run **33107711955**, `merge-master-approval` run **33107712097**, `sonar` run **33107711992**, all success. The floor's own OpenSpec change `widen-review-authority-floor` was ratified by codexFactory [#118](https://github.com/opensoft/codexFactory/pull/118), merged `7d776bbd7972cd959d9e59b78941aaa57d12e09d` |
| P4 | aggregation | `opensoft/xFactory` | [#161](https://github.com/opensoft/xFactory/pull/161) | `0893f0db1d40602c074c0ed905037ad62b6d166f` | plus the root-gitlink-equals-nested-gitlink check (V3) — `validate` run **33117801366**, job **98676831966**; `merge-master-approval` run **33117800992**, both success. The parity check is confirmed on both sides: `tests/test_openxwallet_gitlink_parity.py` went SKIP → PASS once the `openxFactory` pointer moved to `c9a1500e`, and `verify-openxwallet-pin.py --aggregation-root` agreed from the openxFactory implementation. In `validate` itself the assertion still SKIPS by construction (that lane checks out without submodules), which is why §9.4 wires the check into the doc-health lane instead |
| P4b | root-level governed-repo recognition (V10) | `opensoft/openxFactory` | [#440](https://github.com/opensoft/openxFactory/pull/440) | `86212300362755e05dea8885397fdf9ae24a17d1` | `xf-ideation-openxwallet` exists after one `sync-notebooklm-books.py . --apply` — `wallet-validation` run **33126031126**, job **98704281076**; `pytest-suite` run **33126031118**, job **98704281172**. The CODE half is realized and measured: openXwallet goes 0 → 4 projected documents and openAvatar 0 → 2, with `installs/*` never admitted. **The acceptance as worded is NOT satisfied and the widening is not why** — ideation-book membership is status-derived, and openXwallet carries zero brainstorm-or-staged documents, so no book can derive. Recorded at tasks §11.4, which stays OPEN pending openXwallet's first brainstorm/staged document |
| P5a.1 | forward-compatible finder (before P2) | `opensoft/LedgerxFactory` | [#25](https://github.com/opensoft/LedgerxFactory/pull/25) | `e2cedb683019ae8bfee5a520f60cdbbc85ef90fd` | green estate run resolving through the THREE-candidate finder, on a tree where only candidate three exists — LedgerxFactory runs no CI gate other than the Copilot reviewer (run **33018077104**), so the estate-run evidence is the local `validate_wallet_estate.py` output quoted in the pull request: `WALLET ESTATE: PASS`, resolving `…/openxFactory/scripts/validate-openxwallet.py` (candidate three, the "only candidate three exists" tree §2.4 asks for) with `repo scan: 5` satisfying its `>= 5`, and `openspec validate --all --strict` 16 passed / 0 failed |
| P5a.2 | `stack.yaml` bump to the P2.5 minor (after P2.5, before P3) | `opensoft/LedgerxFactory` | [#29](https://github.com/opensoft/LedgerxFactory/pull/29) | `e09902d7c6a5cd9abfe3cdeda6599496833c3b09` | green estate run with the `relocating:` warning OBSERVED — the pinned checker's output in the run log, not the manifest rows. Copilot reviewer run **33108631778**; the estate run is again local, and its captured output names all eight rows under `WARN: the pinned openxFactory bundle contract-v1.47 carries 8 relocating contract row(s)`, inside `WALLET ESTATE: PASS`, exit 0. The checker is extracted from the commit `stack.yaml` pins, so the reader is read at the pin as well as the manifest |
| P5b | post-move repoints + declared wallet pin | `opensoft/LedgerxFactory` | [#30](https://github.com/opensoft/LedgerxFactory/pull/30) | `b1312869127e530ae062dee509845199588735a8` | Copilot reviewer run **33124866596** — LedgerxFactory has no other CI gate. The runnable evidence is the green estate run recorded at tasks §4.9 and §10.10, taken on a purpose-made aggregation clone with BOTH gitlinks initialized so candidate 1 won against a live rival: `repo scan: 5 openxWallet artifact(s) validated`, `0 error(s), 0 warning(s)` under `--strict`, exit 0, resolving through the TWO-candidate finder this pull request leaves behind |
| P5b | supporting-doc repoint | `opensoft/OpsxFactory` | [#129](https://github.com/opensoft/OpsxFactory/pull/129) | `f63c7cd2c76f067ae6a70bc05e92ee0fa44d5f55` | SonarCloud success; Copilot reviewer run **33124268817**. The repoint's own proof is local and recorded at tasks §10.8: `make validate` exit 0 and `openspec validate --all --strict` 36/36, measured before the edit and again after it, with the target verified present in `opensoft/openXwallet` at `wallet-v1.1` and verified to be the copy carrying D12's two prose edits |

**RULESET STATES are their own evidence rows**, because a repository setting is
not a tree fact and no merge commit records it. For each, the evidence is the
`GET repos/<owner>/<repo>/rules/branches/main` output showing
`required_status_checks → [<token>]`. The table was written with two rows; P6
landed after it and its ruleset is the same class of fact, so it is recorded here
as a third:

| Ruleset | Repository | Required token after the act |
| --- | --- | --- |
| 21607344 — "openXwallet wallet-gate (require wallet-validation + pytest-suite)" | `opensoft/openXwallet` | `wallet-validation` — created in EVALUATE mode, promoted to ACTIVE after the bootstrap pull request's first report. Day-one ACTIVE is impossible: a check must have reported once before it is selectable, so "required from day one" is recorded here as unachievable and the bootstrap sequence replaces it. Re-fetched 2026-08-28: enforcement **active**, `rules/branches/main` → `required_status_checks = [wallet-validation, pytest-suite]`. Both tokens are required, which satisfies the named minimum and matches the 21538893 shape D8 says to mirror |
| 21538893 (**UNCHANGED**) | `opensoft/openxFactory` | `wallet-validation` — unchanged, because the token is the job id and P3 retains it in `openxwallet-consumer-gate.yml`. Evidence is TWO artifacts: the ruleset output showing the same tokens as before the wave, AND the P3 pull request's own green `wallet-validation` run, produced by the NEW workflow file (run **33115267228**, job **98668176860**). Re-fetched 2026-08-28: `rules/branches/main` → `required_status_checks = [wallet-validation, pytest-suite]`. **This row asks for ONE token and the ruleset carries TWO** — the same two as the before-picture recorded at tasks §7.31, where `pytest-suite` was made required by an operator act OUTSIDE this wave. The mismatch is stated rather than papered over: it is a row that expects one token and is handed two. What the row actually asserts is nonetheless true — `wallet-validation` is present, now reporting from `.github/workflows/openxwallet-consumer-gate.yml` by retained job id, and **no ruleset edit occurred anywhere in the wave** |
| 21701436 — "LedgerxWallet pin-gate (require pin-validation)" | `opensoft/LedgerxWallet` | `pin-validation` — the descendant repository was created 2026-08-28T02:57:39Z, PRIVATE; re-fetched 2026-08-28 the ruleset's enforcement is **active** and `rules/branches/main` → `required_status_checks = [pin-validation]`. First green `pin-validation` run **33137519688**, job **98740745732**, on LedgerxWallet [#1](https://github.com/opensoft/LedgerxWallet/pull/1), merged `0a0141cafc1fecd5d0e38b14e4f40a67a54a08d3` (= tag `lxw-v1.0`). P6 is the DESCENDANT realization and not this change's own surface — it landed after this table was written — so the row is recorded here for completeness and the P6 change `create-ledgerxwallet-overlay-boundary` carries it too |

## Open questions

Carried from the staged topic with its recommended answer and its destination.
**Q1 is the one expected to travel rather than resolve.**

### Q1. Should the review-authority register be promoted to a wallet primitive, or should the reader be split back into openxFactory?

R6 settles WHERE both live for the move and explicitly leaves the durable shape
open. The register is kindless: its structure exists only inside the validator's
rule (u), `check_register` and `_load_attestations`, so after the split one
repository holds the data and another holds its only schema. **Recommended answer:**
neither, yet — carry the split as ruled and put the question to the council here; if
the council must lean, lean toward promoting the register as a wallet primitive in a
LATER change once a second consumer of authority registers exists, because the
reader-split option pays a real refactor to avoid a boundary the pin already makes
auditable. Both resolutions change code or move a gated path, so either converts a
byte-identical extraction into a design change. **Carried to the council, in this
proposal.**

### Q2. Do the `tenants/ledgerxcorp/wallets/*` records move into `LedgerxWallet`, or stay in LedgerxFactory as tenant data?

**Recommended answer:** the profile artifacts move; the tenant records stay put
unless Ledgerx rules otherwise. A descendant carries profiles, not instances — but
the profile/long-lived-instance line is the owning domain's call, and getting it
wrong from outside relocates live tenant data on an aesthetic argument. **Carried to
the successor `create-ledgerxwallet-overlay-boundary`.**

### Q3. What is the deprecation window for renaming the kind prefix `xfactory_wallet_*` to `openxwallet_*`?

R2 freezes machine keys for v1 and names the rename a successor; nothing says how
long both spellings are accepted. **Recommended answer:** a successor change in
openXwallet accepting BOTH prefixes for exactly one bundle release — `wallet-v1.1`
accepts either and warns on the old, `wallet-v2.0` refuses the old — with the window
closing on **consumers-migrated**, not a date, since there is exactly one consumer
and "all consumers migrated" is a checkable fact where a calendar is not. **Carried
to that successor's design.**

### Q4. When does `openXwallet-Install` become a real repository, and is Hermes its issuer host?

The wallet has no runtime today: no issuer service, no key-custody host, no
deployment surface anywhere. **Recommended answer:** register the NAME in the naming
record and create nothing. The repo appears the day a runtime has an owner and a
first consumer — most likely when Hermes needs to ISSUE rather than merely verify.
This is rule (d) of `domain-descendant-boundary` applied to an install repo. **Carried
to design; the naming half lands in Amendment 2.**

### Q5. What is openXwallet's own bundle-tag scheme?

**Recommended answer:** `wallet-vN.M` with the semantics openxFactory's bundle tags
already carry — major on any breaking key or schema change, minor on additive
contract growth — and **no range expression in the pin**: commit and digest stay
authoritative, with the tag recorded beside them as a human-readable label rather
than as the thing being trusted. A tag can be moved; a commit and a sha256 cannot,
and the moment a pin trusts a range the fail-closed property is gone. **Carried to
P2's design, where the first tag is cut.**

## Successors named

- **`create-ledgerxwallet-overlay-boundary`** — the first domain descendant, on the
  standard this change ratifies (template: `create-medxchart-overlay-boundary`, cited
  as a draft-in-flight shape and not as ratified precedent). Carries Q2.
- **The kind-prefix rename** `xfactory_wallet_*` → `openxwallet_*`, in openXwallet,
  on Q3's dual-accept window. R2 ships a knowingly stale prefix into a brand-new
  repo's first release; that cost is accepted for bisectability and discharged here,
  not forgotten.
- **`MedxWallet`, `codexWallet`, `OpsxWallet`, `AdxWallet`** — each lazily, on its
  domain's first profile (R7/R8, rule (d)).
- **The stale corpus counts** — `contracts/manifest.yaml:1968-1969` and
  `contracts/README.md:108` (16/33 and "nineteen rules" against a tree of 17
  positives, 36 negatives and 21 rules), corrected in openXwallet AFTER
  `wallet-v1.0`, because correcting them inside the move would break byte-identity.
- **P4b — root-level governed-repo recognition** (V10). Both code sites are
  openxFactory's, so it is an openxFactory pull request:
  `scripts/sync-notebooklm-books.py` (`pinned_factory_paths` at `:644-663` and the
  repository set at `:761`) and `scripts/doc_health/ideation_routing.py`
  (`_governed_repo_ids` at `:225-235`). **Acceptance:
  `xf-ideation-openxwallet` exists and carries openXwallet's ideation** — and the
  same widening is what would finally produce `xf-ideation-openavatar`, absent
  today.
- **`openXwallet-Install`** — name registered, repository not created, per Q4.
- **Register-as-primitive** — only if Q1 resolves that way AND a second consumer of
  authority registers exists.

**Amendment 2 to `docs/openxdox-naming.md` is IN this change, not a successor.** R1
contradicts a `ratified` record; leaving that contradiction standing while the repo
is created under the new spelling is the exact defect `document-lifecycle`'s
explicit-delta rule exists to prevent.

## Out of scope, deliberately

- Any runtime, issuer service or key-custody host. The wallet has none and this
  change builds none.
- Any rename of a `kind:` value, capability id, finding code, filename or path in v1
  (R2). Successor, named above.
- Moving `governance/review-authority/` (R6). **NOT** "any change to codexFactory" —
  that earlier exclusion is withdrawn: P3b widens codexFactory's merge-gate floor,
  and it is in scope (V6).
- Widening codexFactory's floor to
  `governance/review-authority/{grants,wallets,attestations}/`. Real, pre-existing,
  and the arc owner's — recorded under ## Impact.
- Fixing lead-security's floor-reachability finding in codexFactory. Real,
  independent, not this change's.
- Backfilling the wallet family into `contracts/releases/*.digests.yaml`.
- Any content change to the moved families. The first release is byte-identical or it
  is not this change.
- Allocating the openxFactory bundle NUMBER — but **not** the class, which is settled.
  `docs/contract-versioning-policy.md:250` makes a removed shape BREAKING (major):
  "a required field is added, **a shape is removed**, or role/vocabulary semantics
  change. Requires: a CHANGELOG migration note, at least one full minor release where
  the old shape produced deprecation warnings, and an update to the conformance
  validator." Shedding eight registered artifacts removes shapes, so the cut is a
  major — and a major has a PRECONDITION. The cut therefore owes a preceding
  deprecation minor that keeps the eight rows registered and marks them relocating —
  by a MANIFEST-carried `relocating:` field plus the CHANGELOG migration note, NOT
  by a validator warning (see P2.5: a validator warning reds LedgerxFactory's strict
  run and is surfaced by no required check) — with the major following it, and the
  "update to the conformance validator" clause discharged by the validator's move
  to openXwallet. Both NUMBERS are allocated at merge order per `:30-31`
  ("A proposed change MUST NOT reserve a minor number before merge order is known").
  Carried as successor **P2.5** above.
