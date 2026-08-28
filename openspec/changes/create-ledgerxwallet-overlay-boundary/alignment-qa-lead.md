# Alignment review — QA lead

**Reviewed version.** `proposal.md` md5 `4fb7186a4365672510866b9cfd8ad1c0` (499 lines),
`specs/ledgerxwallet-overlay-boundary/spec.md` md5 `d5b254298ce935a3245392ad079ada23`
(180 lines), `.openspec.yaml` (49 lines), at worktree HEAD `90f7ed2c`. **The packet was
being edited while this review ran** — `proposal.md` went 455 → 470 → 499 lines and the
branch went ahead 3 → ahead 5 mid-pass; every finding below was re-verified against the
md5s named here. Two things the earlier draft got wrong have already been fixed by the
author and are NOT reported: the § 5 "divergence is REPORTED" claim that named no
reporter (now `:323-331`, and `spec.md:67-70` agrees), and the § Successors bullet that
read as deferring the whole three-way check.

**Headline:** The packet's citation work is unusually good — I byte-checked roughly sixty
anchored claims and the hard ones are right: `VALIDATOR_CANDIDATES` at `:53-78` with
exactly two tuples, `find_openxfactory()` at `:81-116`, `VALIDATOR` at `:119`, all 822
lines, all six named constants, the `stack.yaml` `openxwallet:` block at `:51-62` field
for field, the annotated-tag dereference `021cdeef…` → `63f5a1ad…` = openXwallet `main`
HEAD, `runsheet.md:23`'s relative link and `:174`'s by-ID reference, `docs/protected-surface.md:62`'s
glob verbatim, `.gitmodules`' `ledgerXavatar`/`LedgerxAvatar` mismatch, the 52
capabilities with neither of the two ratified ones among them, the eight/twenty-one
`policies/`/`docs/` counts, `gh repo view opensoft/LedgerxWallet` refusing, and every
negative claim I could construct a search for (no digest row, no protected directory, no
promoted requirement, no workflow, no sibling-domain profile artifact, no warrant entry).
**Three claims are outright wrong and all three are load-bearing arguments** — P3b is
merged not open, the newly added "EXACTLY SEVEN files" check returns eight when you run
it, and "MedxAvatar has been … for five months" is four days. **Two coordinates are
stale in the way this review was built to catch**: `models/protected-surface.yaml:438`
is the PRE-P5b line (it is `:455` on `origin/main`), and `quickstart.md:15` is the
```sh fence — the invocation is at `:19`, and it does not point at a relocating path at
all, which also opens a spec-coverage gap. `openspec validate --strict` is green and the
spec is structurally clean. Nothing here touches the argument's spine; all seventeen are
repairable by editing sentences, and five of them are one-token fixes.

## Verified accurate (no action)

`tests/validate_wallet_estate.py` on `origin/main` (822 lines, exactly as claimed):

- `:53` `VALIDATOR_CANDIDATES = (` through `:78` `)` — the span `:53-78` is exact.
- Exactly TWO candidate tuples, both byte-exact as quoted:
  `:64` `("openxFactory", "openXwallet", "scripts", "validate-openxwallet.py"),` and
  `:66` `("openXwallet", "scripts", "validate-openxwallet.py"),`. Both are paths in other
  repositories, as claimed.
- `:59` `#    aggregation's root gitlink is governed by nothing this repo pins.` and
  `:62-63` `Candidate order is what / breaks the tie` — both quotes exact (the second
  spans a comment wrap; the elision is honest).
- `:67-77` the removal note for the third candidate — "emphatic" is fair, and it does say
  restoring it would reintroduce a silent pass.
- `find_openxfactory()` `:81` (def) through `:116` (`return None`) — `:81-116` exact.
  The walk `:109-116` exact (`node = …` through `return None`).
- `:119` `VALIDATOR = find_openxfactory()` exact.
- `:88` `fail, not degrade to "empty" (repo law, 2026-08-07).` — the § 3 quote and its
  2026-08-07 attribution are exact.
- All six constants exist: `PIN_VERDICTS` `:139`, `ENVIRONMENT_EVIDENCING` `:142`,
  `PLATFORM_VERIFIABLE` `:146` (and `:143-145` does say BC 28.3 AL / RSA family /
  measured, so "the measured BC 28.3 RSA-only family" is right), `EXPECTED_WALLETS`
  `:147`, `EXPECTED_GRANTS` `:148-149`, `EXPECTED_CONSTRAINT` `:150`. The four hard-coded
  ids in § 4 are exactly the ones at `:147-149`.
- § 4's three estate-root reads: `:675` `os.path.join(REPO, "stack.yaml")` and `:676`
  `yaml.safe_load(fh)["xfactory"]["contract_ref"]`, both inside
  `check_pin_reconciliation()` (`:598`, no intervening `def`) — exact. `:688`
  `["git", "-C", openx, "show", f"{pin}:{PIN_CHECKER_PATH}"]` with
  `PIN_CHECKER_PATH = "scripts/check-openxfactory-pin.py"` at `:133` — exact.

LedgerxFactory `origin/main`, elsewhere:

- `stack.yaml` `openxwallet:` `:51` through `:62` (the preserve comment) — `:51-62` exact.
  Every quoted value verified: `contract_repo`, `contract_ref_type: commit`,
  `contract_ref: 63f5a1adac89f017e70bab9a4ffe7cf02d6e6705`,
  `contract_bundle_tag: wallet-v1.1`, `contract_declared_at: "2026-08-27"`,
  `contract_source: openxFactory-nested-submodule-pin`. The derivation comment at
  `:48-50` is quoted verbatim.
- P5b: PR #30 merged `b131286`, work commit `1a8ec62` with exactly that subject line,
  feature `019-openxwallet-consumer-repoints`, and `1a8ec62` is the commit that added the
  `stack.yaml` block (+32) — all exact.
- `templates/wallet-exercise.template.yaml`: `:20` `kind: ledgerx_wallet_exercise_template`,
  `:21` `instantiates: xfactory_wallet_grant_exercise`; the header rule set quoted in § 2
  (presenting-key, `custody_model_in_force`, `unattributed`, BC transport) is at `:9-18`.
- `tenants/ledgerxcorp/wallets/` holds exactly FIVE files. `dhc-lx-create-post-01.yaml`:
  `declared_by: ledgerx:posting-segregation-of-duties` `:15`, `object_kind: purchase_invoice`
  `:16`, `comparison_basis: recorded_holder_of_prior_act` `:20`,
  `distinctness_floor: holder_id` `:21` — all exact, and it does name no tenant, no wallet
  and no key. Holder ids `agent:lx-ap-intake-creator` / `agent:lx-posting-agent`, DIDs
  `did:web:xforge.us:wallets:lx-creator-01` / `…lx-poster-01`, `expires_at`, `issued_by`
  all present; the `state:` quote is `grant-lx-create-01.yaml:11-12` verbatim.
- `runsheet.md:3` `Status: prepared (this feature performs NONE of it)` exact;
  `:23` carries the relative link `../../templates/wallet-exercise.template.yaml`;
  `:174` names `dhc-lx-create-post-01` by ID, not by path — exact.
  `README.md:117-119` carries the live-window quote verbatim.
- `modify-ledgerx-posting-authority-for-segregation-of-duties` IS still unarchived in
  `openspec/changes/`; P0.4 (`runsheet.md:50`) carries no SATISFIED marker and phases 1-6
  carry no execution markers — the window is genuinely unexecuted.
- `.gitmodules` is one entry, section `[submodule "ledgerXavatar"]` against
  `path = LedgerxAvatar` — the mismatch is real. `MedxFactory/.gitmodules` nests
  `MedxAvatar` the same way.
- `.github/` holds exactly `CODEOWNERS` and `copilot-instructions.md`. There is no
  `.github/workflows/` anywhere in the tree — the "no GitHub Actions workflow at all"
  claim is exact.
- `docs/protected-surface.md:62` is byte-identical to the fenced one-liner in § 3.
- `models/protected-surface.yaml`: 137 `path:` rows, none of them any of the three moved
  paths (`templates/` pins seven files, none the wallet template; `tests/` pins only the
  intake corpus plus two intake scripts). `protected_directories:` (`:29-78`) is
  credentials, adapters, policies, openspec/specs, conformance — so `templates/`, `tests/`
  and `tenants/` are not protected directories either. **The negative claim holds
  completely**; only its line number is wrong (F4).
- `tests/validate_document_estate_surface.py:1121` registers
  `ledgerx_wallet_exercise_template`, with the CHK002 note at `:1119-1120` exactly as
  quoted. The anti-rot check (`check_warrant_declaration()`, `:1204`) is on the feature
  warrant, not the kind registry — so "a stale registration" rather than a red bar is the
  correct characterization.
- `schemas/holder-registry.schema.yaml:11` `kind: ledgerx_wallet_holder_registry_contract`;
  `:7-9` "Realized in the LedgerLinc extension as table 50200 / "LL Wallet Holder
  Registry""; `:1-2` "so the repo and the / client system state the same facts" — all exact.
- `policies/` holds exactly 8 files and `docs/` exactly 21; grepping both for `custody`
  returns only DOCUMENT custody (`custody_position`, retention, catalog custody) — no
  wallet custody artifact. `holder_readable` appears in no file under either directory.
- **Extra negative I ran that the packet does not claim:** the active feature warrant
  `specs/001-document-estate-read/warrant.yaml` declares none of the three moved paths
  (its `templates/` entries are `document-*` / `fact-*` / three named files; its `tests/`
  entry is `validate_document_estate_*.py`), so the `git mv` cannot trip the warrant's
  anti-rot. Worth stating in the packet — a bench member will ask.
- No PROMOTED LedgerxFactory requirement names any of the three moved paths (12 specs
  under `openspec/specs/`, grep clean). `specs/017-openxwallet-finder/`,
  `018-openxwallet-pin-bump/`, `019-openxwallet-consumer-repoints/` all exist.
- Every one of feature 016's 29 tasks is ticked (`[X]`), so `tasks.md:215`'s path
  reference to the moving template is a RECORD, not an instruction — the packet's decision
  to leave it alone is correct and matches P5b's own stated rule ("an unticked task is an
  instruction, not a record"). Same for `plan.md:104` and `tasks.md:77`'s DHC references.

Authority side:

- openxFactory `openspec/specs/` holds exactly **52** capabilities and neither
  `domain-descendant-boundary` nor `neutral-product-pin` is among them — exact.
- `contracts/openxwallet-pin.yaml`: `contract_bundle_tag: wallet-v1.1` `:34`,
  `submodule_path: openXwallet` `:41`, `commit: "63f5a1adac89f017e70bab9a4ffe7cf02d6e6705"`
  `:44`; the `openXwallet` gitlink on `origin/main` is that same commit. openxFactory
  `.gitmodules:5-7` carries `openXwallet` at root.
- `gh api …/git/ref/tags/wallet-v1.1` → `type: tag`, `021cdeefbae50127946f147c23edf98c653aa4a5`;
  dereferenced → commit `63f5a1adac89f017e70bab9a4ffe7cf02d6e6705`; `refs/heads/main` →
  the same commit. The ANNOTATED-tag claim and the `wallet-v1.1^{commit}` instruction are
  both correct and non-obvious — good catch by the author.
- `gh repo view opensoft/LedgerxWallet` → `Could not resolve to a Repository with the
  name 'opensoft/LedgerxWallet'` — the quoted phrase is exact.
- `/home/brett/projects/xFactory/.gitmodules:41-43` pins `openAvatar` at root; no
  `openXwallet` entry exists. P4 is genuinely open.
- The `.openspec.yaml` quote of the parent's § Successors is **byte-exact** against
  `split-openxwallet-repo/proposal.md:1195-1197`, and the Q2 quote is byte-exact against
  its ratification record `:50-52`. `tasks.md` 12.1 exists, is unticked, and is group 12
  "P6 — the first domain descendant" (see F16 for the truncation).
- All five rule restatements are faithful: rule 1's quote = ratified `spec.md:6-8`;
  rule 3's = `:55-56`; rule 5's = `:105-106`; rules 2 and 4 are accurate paraphrases,
  including the `Status: draft` standing of `create-medxchart-overlay-boundary` (confirmed:
  its `proposal.md:4` is `Status: draft`).
- `neutral-product-pin` requirement title at `:57` is exactly "The consuming repository's
  pin is authoritative among reachable checkouts".
- R7 (`:137-140`) and R8 (`:141-144`) say what the packet says they say. DTN-026's register
  row (`docs/domain-neutralization-candidate-register.md:56`) does name `LedgerxWallet` first.
- Parent carve claims: "twelve path sets" (parent `:286-287`, `:610-611`), "eight
  registered … artifacts" (`:394`), two promoted capabilities (`:28-33`) — all accurate.
- `MedxAvatar/pins/openavatar.yaml` does live at `pins/`, does carry `source_repo` `:7` /
  `resolved_ref` `:8`, and has NO `relationship:` — the "deliberately not followed"
  paragraph is accurate on every particular.
- `target_release: implemented` is a legal value (`openspec/specs/release-realization/spec.md:9`),
  and openxFactory README carries `## OpenSpec Records` at `:379`.
- `MedxWallet`/`codexWallet`/`OpsxWallet`/`AdxWallet`: grepping all four domain trees on
  `origin/main` for `kind: xfactory_wallet*` / `kind: openxwallet_*` / wallet template or
  constraint kinds returns NOTHING. MedxFactory carries eight `ideation/brainstorm/medx-repo-wallet-emr-*.md`
  files, but those are ideation prose, not artifacts of the product's profile kind — the
  rule-5 test is unmet in all four, exactly as claimed. (Worth naming the brainstorm files
  pre-emptively; a bench member will grep "wallet" and find them.)
- `pinned_factory_paths()` (`scripts/sync-notebooklm-books.py:644-663`) matches
  `^\s*path\s*=\s*(xFactories/\S+)$` and `:767` explicitly skips nested checkouts;
  `_governed_repo_ids()` (`scripts/doc_health/ideation_routing.py:225-235`) builds
  `xFactories/<Name>`. The new § Successors bullet's mechanism is exactly right (only its
  duration is wrong — F3).

Structural conformance:

- `openspec validate create-ledgerxwallet-overlay-boundary --strict`, run from
  `/home/brett/projects/xFactory/openxFactory-worktrees/P6-ledgerxwallet`, verbatim:
  `Change 'create-ledgerxwallet-overlay-boundary' is valid` (exit 0). Re-run after the
  concurrent edits: identical.
- Sole delta header is `## ADDED Requirements` (`spec.md:3`). All five requirements carry
  SHALL on the FIRST body line (`:6`, `:46`, `:77`, `:113`, `:161`). Scenario counts
  5 / 4 / 5 / 7 / 3 — every requirement has at least one.
- `code_surface:` and `target_release:` both present; `Status: draft` appears in BOTH the
  front matter (`:4`) and the body (`:8`).
- `.openspec.yaml` origin: `kind: ad_hoc` is one of only two legal kinds
  (`openspec/specs/document-lifecycle/spec.md:349-353`), and the id
  `openxFactory:adhoc:2026-08-27-create-ledgerxwallet-overlay-boundary` conforms exactly
  to the required `<repo>:adhoc:<date>-<sequence-or-slug>` form, with `reason`,
  `approved_by` and `approved_on` all present. The kind choice is right (see F13 for the
  one sentence that overstates it).

---

## F1 — codexFactory P3b is MERGED, not open

**CLASS: MISMATCH**

**Evidence.** `proposal.md:415-419`: "**Two other wave items are open and neither gates
P6.** P4 … is not landed …, and P3b — codexFactory's merge-gate floor — is codexFactory's.
P6 touches neither surface. **Stated so the bench does not have to check.**"

P3b is landed. `git -C xFactories/codexFactory show origin/main:scripts/merge_master/openxfactory-review-authority-floor.yaml`
carries both P3b entries under `never_clearable_paths` (`:34`):
`:37` `- contracts/openxwallet-pin.yaml` and `:41` `- openXwallet`, landed by
`5a46628` "Realize P3b of split-openxwallet-repo: widen the review-authority floor".
`gh pr view 117 --repo opensoft/codexFactory` → `{"mergedAt":"2026-08-27T21:53:01Z","state":"MERGED"}`.
Only P4 remains open of the two.

**Remedy.** Rewrite `:415-419` as a ONE-item bullet: "**One other wave item is open and
it does not gate P6.** P4 — the aggregation's root `openXwallet` gitlink — is not landed
(`/home/brett/projects/xFactory/.gitmodules` carries `openAvatar` at root and no
`openXwallet`). P3b — codexFactory's merge-gate floor — MERGED 2026-08-27 (PR
opensoft/codexFactory#117, `5a46628`), and P6 touches neither surface." A sentence that
ends "stated so the bench does not have to check" has to be right; this one sends a
reviewer to a green surface expecting red.

## F2 — the newly added "EXACTLY SEVEN files" check returns EIGHT when you run it

**CLASS: MISMATCH**

**Evidence.** `proposal.md:193-196`: "**The enumeration is COMPLETE, and that is a
checkable claim rather than a hope.** `git grep '^kind:.*wallet'` over LedgerxFactory
`origin/main` returns EXACTLY SEVEN files".

Run it. `git grep -l '^kind:.*wallet' origin/main` returns **EIGHT**: the seven named
artifacts PLUS `tests/validate_wallet_estate.py`, whose embedded probe corpora
(`_WALLET` `:153`, `_GRANT` `:165`, `_EXERCISE` `:180`, `_DHC_PROBE` `:200`) carry
column-zero `kind:` lines inside their triple-quoted YAML. The `^kind:` LINE count is 11,
not 7: `xfactory_wallet_record` ×3, `xfactory_wallet_grant` ×3,
`xfactory_wallet_distinct_holder_constraint` ×2, `xfactory_wallet_grant_exercise` ×1
(probe only — no real exercise record exists yet), plus the two `ledgerx_wallet_*` ×1 each.

The seven ARTIFACTS are correctly enumerated, and "two move, five stay" is right. It is
only the offered command that misreports — which is worse than no command, because the
paragraph invites the bench to run it.

**Remedy.** Replace `:194-200` with a command that produces the stated number, and name
the eighth hit rather than hiding it: "`git grep -l '^kind:.*wallet' origin/main -- ':!tests/'`
returns EXACTLY SEVEN files … The same grep without the exclusion returns an eighth,
`tests/validate_wallet_estate.py`, whose probe corpora carry synthetic wallet-kind YAML;
those are fixtures, not artifacts, and they move with the validator."

## F3 — "MedxAvatar has been … for five months" is four days

**CLASS: MISMATCH**

**Evidence.** `proposal.md:448-450`: "a nested-only `LedgerxWallet` is outside the
notebook projection and the ideation routing, **exactly as `MedxAvatar` has been for five
months** under the same ratified placement."

`git -C xFactories/MedxFactory log --reverse -S'MedxAvatar' -- .gitmodules` → the gitlink
was added by `46f595c6` "add MedxAvatar distribution submodule (private; pins openAvatar
@ a5c5448)", dated **2026-08-23**. Today is 2026-08-27. That is FOUR DAYS. (DTN-022 itself
is 2026-08-03, so even the ratification is 24 days old, not five months.)

This is not cosmetic: the bullet's whole argument is "accept this gap because a precedent
has lived with it", and a four-day precedent does not carry that weight.

**Remedy.** Change the clause to "exactly as `MedxAvatar` has been since its own nesting
on 2026-08-23 (`46f595c6`) under the same ratified placement" and drop the appeal to
duration — the mechanism argument (`pinned_factory_paths` keys on `xFactories/`) is
sufficient on its own and is fully accurate.

## F4 — `models/protected-surface.yaml:438` is a PRE-P5b coordinate; it is `:455`

**CLASS: DRIFT**

**Evidence.** `proposal.md:110-112` "(that file mentions `validate_wallet_estate.py`
once, at `:438` …)" and `:399-400` "the single wallet mention at `:438`".

On `origin/main` the mention is at **`:455`**: `      RED-proven by validate_wallet_estate.py's`.
`:438` is `      the digest in the same commit, which this surface's` — an unrelated
sentence in the `instantiate-hermes-authority` entry. Proof of the cause:
`git show 1a8ec62~1:models/protected-surface.yaml | grep -n validate_wallet_estate` → `438`.
P5b added 23 lines to that file and pushed the mention down 17 lines. This is a surviving
pre-P5b coordinate.

Propagates: `design.md:357` and `tasks.md:201` carry `:438` too.

**Remedy.** `:438` → `:455` in all four places (`proposal.md:111`, `proposal.md:400`,
`design.md:357`, `tasks.md:201`). The quoted sentence at `:401-402` is byte-correct and
needs no change (`:455-456` "RED-proven by validate_wallet_estate.py's /
platform-verifiability pin before the flip").

## F5 — `quickstart.md:15` is wrong twice: wrong line, and wrong referent

**CLASS: MISMATCH**

**Evidence.** `proposal.md:221-222`: "`quickstart.md:15` in feature 016 likewise invokes
the validator by a relative path", inside § 2b, whose subject is paths the profile
relocation breaks. Front matter `:2` gives the reason: "`runsheet.md:23` and
`quickstart.md:15` are repointed **because that live window is PREPARED-BUT-UNEXECUTED**".

`specs/016-posting-segregation-of-duties/quickstart.md:15` is the opening fence,
"```sh". The relative invocation is at **`:19`**:
`python3 ../../openxFactory/openXwallet/scripts/validate-openxwallet.py . --strict`.

And that path is the NEUTRAL openXwallet validator inside openxFactory's nested gitlink —
already repointed by P5b, which touched this very file (`quickstart.md | 8 +-` in
`1a8ec62`). It is **not** one of the three relocating paths. `git grep` confirms
`quickstart.md` references neither `validate_wallet_estate` nor `wallet-exercise.template`
at all; its only relocation-relevant line is `:17`'s `tests/validate_*.py` glob, which the
delegating entry already covers. So the `git mv` does not break `quickstart.md` — P6's
rule 1 does, which is a different and later-binding reason.

The gap this opens: `spec.md:156-158`'s covering scenario fires only "**WHEN** an
un-executed runsheet or quickstart … references **a profile artifact by a path this
relocation changes**". The quickstart references neither a profile artifact nor a path this
relocation changes, so the requirement as written does not compel the repoint the proposal
promises, and a later phase could satisfy the spec while leaving `:19` pointing outside the
descendant — the exact breach rule 1 forbids.

**Remedy.** Two edits. (1) `proposal.md:221-222`: "`quickstart.md:19` invokes the NEUTRAL
openXwallet validator by a relative path into openxFactory's nested gitlink
(`../../openxFactory/openXwallet/scripts/validate-openxwallet.py`, its P5b value). That
path is not broken by the `git mv` — it is forbidden by rule 1 once the domain consumes
through the descendant — so it is repointed to
`LedgerxWallet/openXwallet/scripts/validate-openxwallet.py` in the same act, for that
reason." Fix `:2` and `tasks.md:185` / `design.md:325`, `:413` to `:19` likewise.
(2) Widen `spec.md:157` to "references a relocating profile artifact by path, OR resolves
the pinned product outside `LedgerxWallet/`" so the requirement actually reaches `:19`.

## F6 — the custody posture is NOT comment-only; it is declared data in three places

**CLASS: MISMATCH**

**Evidence.** `proposal.md:377-382`: "The Ledgerx wallet custody posture —
`custody.model: holder_readable`, environment-evidencing, authority ceiling `act`, "the
audit record says 'environment', never 'holder'" — **exists today ONLY in YAML COMMENTS**
inside the two wallet records and in the ratification prose of
`modify-ledgerx-posting-authority-for-segregation-of-duties`".

Three counter-examples, all structured data:

- `tenants/ledgerxcorp/wallets/wal-lx-creator-01.yaml:27-31` —
  `custody:` / `  model: holder_readable` / `  registry_version: 1` /
  `  declared_at: "2026-08-08T00:00:00Z"` / `  declared_by: opensoft`. Same block in
  `wal-lx-poster-01.yaml`. The very string the sentence quotes is a declared field.
- `grant-lx-create-01.yaml:22` `  authority_tier: act` (and the same in
  `grant-lx-post-01.yaml`) — the "authority ceiling `act`" is declared, not narrated.
- `tests/validate_wallet_estate.py:142`
  `ENVIRONMENT_EVIDENCING = {"holder_readable", "isolated_invocable"}` — enforced data.
  The proposal's own § 2 table (`:165`) cites `ENVIRONMENT_EVIDENCING` as "the domain's own
  vocabulary as data", which contradicts `:380` two hundred lines later.

Only the quoted PROSE ("the audit record says 'environment', never 'holder'",
`wal-lx-creator-01.yaml:5-6`) is comment-only. The sentence the bullet actually needs —
"there is no custody POLICY ARTIFACT in LedgerxFactory" — is at `:383` and is **true**:
verified across `policies/` (8 files) and `docs/` (21 files), where `holder_readable`
appears zero times.

**Remedy.** Replace `:378-382` with: "The Ledgerx wallet custody posture is declared today
only as per-record FIELDS and comments — `custody.model: holder_readable` plus
`registry_version`/`declared_at`/`declared_by` in each of the two wallet records,
`authority_tier: act` in each grant, `ENVIRONMENT_EVIDENCING` in the validator, and the
prose rule "the audit record says 'environment', never 'holder'" in a YAML comment and in
the 2026-08-08 ratification. There is no custody POLICY ARTIFACT that states the posture
once for the domain: …". This is a stronger argument for `custody-posture.yaml` than the
current one, because it shows the posture is real and enforced but has no single home.

## F7 — "the single wallet mention" — the file has about sixteen

**CLASS: OVERCLAIM**

**Evidence.** `proposal.md:399-400`: "the **single wallet mention** at `:438`".

`git grep -n -i wallet` in `models/protected-surface.yaml` on `origin/main` returns lines
`389`, `391`, `392`, `393`, `394`, `395`, `397`, `408`, `411`, `413`, `414`, `415`, `427`,
`454`, `455` — fifteen lines across two narrative entries (the P5b `stack.yaml` pin entry
and the 018 pin-bump entry), several of them mentioning `openxwallet:` and `wallet-v1.1`
directly. What IS single is the mention of `validate_wallet_estate.py` — which is exactly
how `:110-111` words it. The Impact bullet drops the qualifier and the claim goes false.

**Remedy.** `:399-400` → "the file's single mention of `validate_wallet_estate.py`, at
`:455`, is inside the narrative of a `stack.yaml` pin entry". (Fixes F4 in the same edit.)

## F8 — "the same six pin fields" is not MedxChart's six, and the nesting is dropped

**CLASS: OVERCLAIM**

**Evidence.** `proposal.md:133-139` lists the LedgerxWallet pin as `schema_version`,
`kind`, `relationship`, `submodule_path`, `revision`/`revision_kind: commit`,
`contract_bundle_tag`, `repository` — then: "Shape follows the live descendant example
`MedxChart/contracts/openchart-pin.yaml` (`kind: medxchart_openchart_pin`, **the same six
pin fields**)".

`xFactories/MedxChart/contracts/openchart-pin.yaml` in full is ten lines. Its six pin
fields are nested under a `pin:` mapping (`:4`):
`:5` `repository: opensoft/openChart`, `:6` `remote: git@github.com:opensoft/openChart.git`,
`:7` `revision: d2376a31…`, `:8` `submodule_path: openChart`, `:9` `source_path: .`,
`:10` `relationship: pinned_upstream_composition`. It carries **no** `revision_kind:` and
**no** `contract_bundle_tag:`. So the proposal's list swaps two fields in, drops
`remote:` and `source_path:`, and presents everything FLAT rather than under `pin:`.
Four of six overlap; "the same six" is not one of the things this file says.

(`revision_kind: commit` comes from openxFactory's own pin
`contracts/openxwallet-pin.yaml:45`, and `contract_bundle_tag` from `:34` — both good
choices, just not MedxChart's.)

**Remedy.** `:137-139` → "Shape follows the live descendant example
`MedxChart/contracts/openchart-pin.yaml` for its `kind:` form and its `relationship:`,
`submodule_path:` and `revision:` fields, and adds `revision_kind: commit` plus
`contract_bundle_tag:` from openxFactory's own `contracts/openxwallet-pin.yaml` (`:45`,
`:34`) so a tag-only pin is refusable. MedxChart nests its fields under a `pin:` key;
state whether LedgerxWallet does the same." Then say which, because a later phase cannot
guess it (F9).

## F9 — nothing in the packet names the field that carries the 40-hex commit

**CLASS: GAP**

**Evidence.** `spec.md:8-12` requires the pin manifest to carry `schema_version: 1`,
`kind: ledgerxwallet_openxwallet_pin`, `submodule_path: openXwallet`,
`revision_kind: commit` and `relationship: pinned_upstream_composition` — five named keys,
none of which holds the commit. `spec.md:36-38`'s scenario refuses "`wallet-vN.M` but no
40-hex commit", and `proposal.md:135` writes the field as `revision`/`revision_kind: commit`
while `:145` says "the SAME commit as the pin file's `revision`" and `:311` says
"`contracts/openxwallet-pin.yaml` `revision`". The two live precedents disagree:
MedxChart uses `revision:` (`:7`), openxFactory uses `commit:` (`:44`) alongside
`revision_kind:`. Whether the keys sit at the top level or under `pin:` is also unstated.

A later phase can satisfy the spec's letter with either key name and either nesting, and
the three-way invariant at `:311` names `revision` — so a tasks author who follows
openxFactory's `commit:` would break the invariant's own wording.

**Remedy.** Add `revision:` to the spec's required-key list at `:11` — "…,
`revision: <40-hex commit>`, `revision_kind: commit` …" — and add one sentence to
`proposal.md:133-143` stating whether the keys are top-level (openxFactory's shape) or
nested under `pin:` (MedxChart's). One clause each; it removes the only ambiguity in the
change's central artifact.

## F10 — `code_surface:` declares THREE repositories; only two change

**CLASS: OVERCLAIM**

**Evidence.** `proposal.md:2`: "opensoft/LedgerxWallet (new), LedgerxFactory, xFactory
aggregation — **THREE repositories**: a NEW repository, one consumer, and the aggregation's
placement record. … (3) The xFactory aggregation: **NO change in v1** … so `.gitmodules`
at the aggregation is untouched".

`code_surface:` declares the code this change touches. A repository that receives no
commit is not a code surface, and the front matter says so itself two clauses later.
`Out of scope` `:465` already carries "Any change to the aggregation. § 6", which is the
right home for it. Compare the parent, whose `code_surface:` names six repositories every
one of which receives a commit.

**Remedy.** `:2` → "opensoft/LedgerxWallet (new), LedgerxFactory — TWO repositories: a NEW
repository and one consumer. The xFactory aggregation is DELIBERATELY not a surface here
(§ 6): the ratified nested placement is taken and the `xFactories/` placement is not, so
`.gitmodules` at the aggregation is untouched — a stated decision rather than an omission."
Keep item (3)'s prose, just move it out of the repository count.

## F11 — "Two openxFactory files change" — the packet alone is five files

**CLASS: MISMATCH**

**Evidence.** `proposal.md:420-421`: "**Two openxFactory files change and nothing else.**
This packet and one README "OpenSpec Records" entry."

The packet is five files on disk: `proposal.md`, `.openspec.yaml`,
`specs/ledgerxwallet-overlay-boundary/spec.md`, `design.md`, `tasks.md`. Plus `README.md`
= six. The front matter's own version of the claim (`:3`, "The only openxFactory tree
change is this packet plus one README Records entry") is honest because it counts the
packet as a packet; the Impact bullet converts it to a file count and the count is wrong.

**Remedy.** `:420` → "**Nothing in openxFactory changes but this packet and one README
line.**" Drop the number; the point is the absence of contract/schema/manifest/release
surface, which `:421-422` already makes and which I verified.

## F12 — Phase 0's enumeration omits P0.3 SATISFIED

**CLASS: DRIFT**

**Evidence.** `proposal.md:207-208`: "`## Phase 0 — preconditions` records **P0.1 and
P0.2** SATISFIED".

`runsheet.md` records THREE: `:29` "P0.1 **SATISFIED 2026-08-08**", `:38` "P0.2
**SATISFIED 2026-08-08**", `:47` "P0.3 **SATISFIED 2026-08-08**: LedgerxFactory#19 merged
as merge…". Only `:50`'s P0.4 lacks the marker — which is what the README quote at
`:209-210` says, so the packet's conclusion is right and only the enumeration is short.

**Remedy.** `:208` → "records P0.1, P0.2 and P0.3 SATISFIED, with only P0.4 open".

## F13 — "NO STAGING ORIGIN IS CLAIMED: none exists" — the staged topic is still on `main`

**CLASS: DRIFT**

**Evidence.** `.openspec.yaml:17-21`: "NO STAGING ORIGIN IS CLAIMED: **none exists**, and
none is needed. The staged topic `ideation/staging/openxwallet-neutral-home/` exited ONCE,
into `split-openxwallet-repo`, which is that topic's "first and only exit"".

`ideation/staging/openxwallet-neutral-home/openxwallet-neutral-home.md` is present on
openxFactory `origin/main` — 552 lines, `:3` `Status: staged` — and its own `## Exit`
(`:534-535`) names this change by id: "The first domain descendant is `LedgerxWallet`, via
`create-ledgerxwallet-overlay-boundary`". So organized source material for this subject
demonstrably exists, and it points here. That matters because the governing rule
(`openspec/specs/document-lifecycle/spec.md:351-353`) is "Ad-hoc status is an explicit,
approved exception — it MUST NOT substitute for staging **when organized source material
exists**".

The `ad_hoc` choice is still correct — the topic's exit is TAKEN (`:542` "Exit TAKEN
2026-08-26") and an exit is single-use, which is precisely the packet's argument — and the
quoted phrase "first and only exit" is genuine (`split-openxwallet-repo/proposal.md:12`,
openxFactory `README.md:385`). It is the two words "none exists" that are false as written
and that hand a reviewer an easy objection.

**Remedy.** `:17-18` → "NO STAGING ORIGIN IS CLAIMED, and none is available: the topic
`ideation/staging/openxwallet-neutral-home/` still stands on `main` but its single exit is
TAKEN (`:542`), into `split-openxwallet-repo` — that change's own words, "the first and
only exit of the staged topic". A successor named inside a ratified change draws its
authority from the ratification, not from a second trip through a spent exit." Keep the
rest verbatim.

## F14 — LedgerxFactory's `.github/CODEOWNERS` is declared as changing, with no stated change

**CLASS: GAP**

**Evidence.** `proposal.md:2` item (2) ends: "`README.md`, `.github/CODEOWNERS` and
`models/protected-surface.yaml`'s prose reference." `README.md` has a named reason
(`:109` carries `tests/validate_wallet_estate.py` "in the bar" — verified) and
`protected-surface.yaml` has one (`:398-403`). `.github/CODEOWNERS` has none: no § in the
body, no Impact bullet, and no spec requirement mentions it.

Nor is one obvious. LedgerxFactory's CODEOWNERS (verified on `origin/main`) is path-scoped
over `/adapters/`, `/credentials/`, `/catalog/`, `/conformance/`, `/hermes/`, `/omnigent/`,
`/openspec/`, `/policies/`, `/.github/`, `/stack.yaml` — it covers **none** of the three
moved paths, and it does not cover `.gitmodules` either. So either a `/LedgerxWallet` or
`/.gitmodules` entry is intended (say so), or the entry is a copy-paste from the
LedgerxWallet scaffold list at `:149-152` and should come out. As it stands a tasks author
has to invent the edit.

**Remedy.** Either add one clause to `:2` — e.g. "`.github/CODEOWNERS` gains `/.gitmodules`
and `/LedgerxWallet`, because the gitlink is now a governed surface" — plus a matching
Impact bullet, or strike `.github/CODEOWNERS` from LedgerxFactory's list in `:2`.

## F15 — `find_aggregation()` (`:583-594`) cites the walk body, one line short, against the packet's own convention

**CLASS: DRIFT**

**Evidence.** `proposal.md:273`: "runs a SECOND five-level upward walk,
`find_aggregation()` (`:583-594`)".

`find_aggregation` is defined at `:560`; its docstring runs to `:582`; the walk is
`:583` (`node = REPO if start is None else start`) through `:595` (`return None, None`).
So `:583-594` names the walk but stops one line before its terminal return. The packet's
own convention for the first finder gives BOTH coordinates and includes the return —
`find_openxfactory()` (`:81-116`, the walk at `:109-116`), where `:116` IS `return None`.

**Remedy.** `:273` → "`find_aggregation()` (`:560-595`, the walk at `:583-595`)".

## F16 — two quotes presented as verbatim are composites

**CLASS: NOTED**

**Evidence.** Two, both minor, both in a packet whose credibility rests on quoting:

1. `.openspec.yaml:16-17`: "as `tasks.md` group 12, task 12.1, **whose text is**
   "**[GOVERNANCE]** Open `create-ledgerxwallet-overlay-boundary` — the named successor,
   on the descendant standard this change ratifies"". The actual 12.1 continues:
   "… ratifies (template: `create-medxchart-overlay-boundary`, cited as a draft-in-flight
   shape and NOT as ratified precedent). It carries Q2 (whether …". "Whose text is" plus a
   truncation with no ellipsis reads as a full quote.
2. `proposal.md:165`: ""A descendant adds a domain validator … that checks its own profile
   artifacts against the pinned product's schemas" is explicitly permitted by rule 3's
   third scenario." It is rule 3's third scenario (verified: ratified `spec.md:71-73`), but
   the quote splices the scenario HEADING ("A descendant adds a domain validator") to its
   WHEN clause ("a descendant adds **a validator** that checks its own profile artifacts
   against the pinned product's schemas") — the word "domain" appears only in the heading.

**Remedy.** (1) Change "whose text is" to "which opens" and append "…" after "ratifies".
(2) Quote the WHEN clause alone: ""a descendant adds a validator that checks its own
profile artifacts against the pinned product's schemas" is permitted by rule 3's third
scenario, headed "A descendant adds a domain validator"."

## F17 — the packet is being written concurrently, and two bad coordinates are in all four files

**CLASS: NOTED**

**Evidence.** `design.md` (440 lines) and `tasks.md` (242 lines) already exist and are
substantive — the "later phases, not yet expected" framing this review was given is
superseded. During the pass `proposal.md` went 455 → 470 → 499 lines (mtimes 19:34-19:35,
commits `4255b206`, `90f7ed2c`) and the branch moved from ahead 3 to ahead 5. Two of the
findings above are already replicated downstream: `:438` in `design.md:357` and
`tasks.md:201` (F4); `quickstart.md:15` in `design.md:325`, `design.md:413` and
`tasks.md:185` (F5).

Also worth noting for the record: the concurrent edits FIXED two real defects an earlier
draft carried — § 5 now says a divergence from openxFactory's pin "is NOT an error and is
checked by nothing … because an earlier draft … said it would be "REPORTED" and named no
reporter" (`:326-328`), and `spec.md:67-70` was rewritten to agree ("no tool is required
to reconcile them and none SHALL claim to"). That resolves what would otherwise have been
a described-but-unwired control. I re-ran `openspec validate --strict` after the edits:
still green.

**Remedy.** Apply F4 and F5 as four-file edits, not two, and re-run
`OPENSPEC_TELEMETRY=0 openspec validate create-ledgerxwallet-overlay-boundary --strict`
after. If any further alignment pass is commissioned, freeze the packet first — a review
that quotes line numbers against a moving file produces findings that expire.

---

## Blocking before circulation

Every one of these is a factual claim a bench member will check first, and each currently
fails the check:

- **F1** — P3b is merged; the sentence tells the bench not to verify it. One-line fix.
- **F2** — the offered `git grep` returns eight files, not seven. The paragraph invites
  the run, so it will be run.
- **F3** — "five months" is four days, and the duration is the bullet's argument.
- **F4** — `:438` is a pre-P5b coordinate (`:455` now), in two places in `proposal.md`
  and two more downstream. This is the exact drift class this pass exists to catch.
- **F5** — `quickstart.md:15` is the wrong line AND the wrong referent, and § 2b's stated
  reason for the repoint is wrong.
- **F6** — the custody posture is declared data in three places, contradicting the
  proposal's own § 2 table.
- **F7** — "the single wallet mention" (fifteen lines mention wallet).
- **F11** — "Two openxFactory files" (the packet alone is five).

## Blocking before ratification

Structural or normative gaps a tasks/design phase cannot close by guessing:

- **F9** — the spec never names the key carrying the 40-hex commit, and the three-way
  invariant names `revision` while openxFactory's precedent uses `commit:`. Fix in the
  spec, not in tasks.
- **F5 (spec half)** — `spec.md:156-158`'s trigger does not reach the reference the
  proposal promises to repoint, so the spec is satisfiable while rule 1 stays breached.
- **F8** — "the same six pin fields" misdescribes the precedent the pin's shape is
  derived from; the derivation is the ratified rule's own test.
- **F10** — `code_surface:` declares a repository that receives no commit.
- **F13** — `.openspec.yaml`'s "none exists" is false on `origin/main` and undercuts the
  `ad_hoc` justification the origin contract requires.
- **F14** — a declared code surface (`LedgerxFactory/.github/CODEOWNERS`) with no stated
  change; either specify it or strike it.

## Not blocking

**F12**, **F15**, **F16** are precision repairs (one enumeration, one line span, two quote
forms). **F17** is process: apply F4/F5 in all four files and freeze the packet before the
next review pass.
