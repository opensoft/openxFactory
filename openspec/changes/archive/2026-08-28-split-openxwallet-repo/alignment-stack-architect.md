Status: record
Reviewer role: Stack Architect (alignment review, read-only) — 2026-08-26
Subject proposal: openspec/changes/split-openxwallet-repo/proposal.md
Dispositions ruled by: the change lead, 2026-08-26 — all MISMATCH and DRIFT findings
APPLIED; all GAP findings APPLIED as additions inside the declared scope; the
missing-`specs/` finding DEFERRED to the specs phase.

# Stack Architect review — `split-openxwallet-repo`

Worktree `split-openxwallet-repo`, branch `change/split-openxwallet-repo`. The change
is untracked; contents are `proposal.md` only (514 lines at review time, 778 after
these fixes landed).

**Headline:** the proposal's construction of R1–R8 holds and its citation density is
unusually high, but fifteen citations or claims do not survive checking against the
tree — one of them load-bearing (`shared-contract-ownership` IS engaged), two of them
inverted precedents, one an entire omitted REQUIRED check, and four wrong README
ranges.

---

## 1. `shared-contract-ownership` IS engaged

**Finding (verbatim).** MISMATCH — `shared-contract-ownership` IS engaged, by "Tooling
hosted in the publisher verifies released bytes, not a declared pin"
(`openspec/specs/shared-contract-ownership/spec.md:139-165`). "Canonical contract home"
(`:8-31`) reading holds (the `or referenced` limb, `:17-19`). But `:139-165`'s
publisher test ("a checkout SHALL be treated as a publisher release only when it
carries all of contracts/manifest.yaml, contracts/schemas/, and the contract family's
own validator… A tree missing any marker is NOT a publisher and SHALL take the consumer
path with its declared pin intact") means shedding the validator demotes openxFactory
to consumer for that family, and the consumer path is written only for stack.yaml-
declared openxFactory releases. FIX: replace proposal ~260-266 parenthetical and
~339-350 with: "`shared-contract-ownership` — one MODIFIED delta declared, on *Tooling
hosted in the publisher verifies released bytes, not a declared pin* (`:139-165`).
Shedding the wallet validator removes a publisher marker for that family, and the
requirement's consumer path assumes the publisher is openxFactory. The delta states the
third case: where openxFactory is the CONSUMER of an external neutral product, the
declared pin is `contracts/<product>-pin.yaml` rather than `stack.yaml`, and the byte
chain, fail-closed rule and manifest-parity obligation run unchanged. *Canonical
contract home* (`:8-31`) needs no delta — the pin is the scenario's `or referenced`
limb." Also add `shared-contract-ownership` to ## Capabilities → Modified.

**Disposition: APPLIED.** Union with QA #2 taken. A `shared-contract-ownership` bullet
now stands in ## Modified Capabilities; the ## Declared NOT modified bullet was
rewritten to a "DECLARED, not omitted" cross-reference; RATIFIES item 3 became "Three
MODIFIED deltas"; the "why new capabilities" paragraph no longer claims the capability
is unengaged. **Note on application:** the `or referenced` limb is at `:18`, inside the
scenario spanning `:16-18`, not `:17-19`; the proposal cites `:18`. The requirement plus
all six scenarios runs `:139-170` (QA #2's range); `:139-165` covers the requirement and
the first five scenarios and is the range the proposal carries, as ruled.

## 2. The pin grammar is not new

**Finding (verbatim).** MISMATCH — pin grammar is not new: `kind:
pinned_contract_manifest` exists in
`/home/brett/projects/xFactory/installs/keycloak-install/config/contracts/identity-brokering/manifest.yaml:1-20,45-58`
and `installs/openxpki-install/config/contracts/trust-anchor/manifest.yaml:55`
(contract_bundle_tag + source_repository + commit + revision_kind + per-file sha256 +
pinned_by_commit_only; "A tag-only pin is refused: a tag can be moved"). FIX at
~250-258: "…which it has never done in this DIRECTION. The pin GRAMMAR is the ratified
`pinned_contract_manifest` shape (keycloak-install identity-brokering manifest,
openxpki-install trust-anchor manifest): commit + `revision_kind` + per-file sha256 +
`pinned_by_commit_only`, tag-only refused. `contracts/openxwallet-pin.yaml` REUSES
`kind: pinned_contract_manifest` unchanged; what is new is only that openxFactory is
the consumer." Adjust the repo-boundary-governance non-declaration (~356-358) to cite
those two realized instances.

**Disposition: APPLIED.** Verified in the tree: both manifests carry
`kind: pinned_contract_manifest` and the refusal sentence verbatim. Both the
`neutral-product-pin` bullet and the `repo-boundary-governance` non-declaration now
carry it.

## 3. Rule (c) inverts both placement precedents

**Finding (verbatim).** MISMATCH — rule (c) inverts both placement precedents:
MedxFactory/.gitmodules carries ONLY MedxAvatar; MedxChart exists only at
xFactories/MedxChart; MedxChart's placement (created 2026-08-23) is the LATER act vs
DTN-022/MedxAvatar 2026-08-03. FIX rule (c) at ~246-248: "(c) a descendant is
aggregated at one of two ratified placements — nested into its DomainxFactory as a
submodule (`MedxAvatar` in `MedxFactory`, DTN-022, 2026-08-03) or at the aggregation's
`xFactories/` (`MedxChart`, 2026-08-23, the more recent act) — and the choice is the
owning domain's, on whether the descendant needs standalone cloning; it MAY carry
both."

**Disposition: APPLIED,** verbatim, plus the two corpus facts stated inline
(`MedxFactory/.gitmodules` carries only `MedxAvatar`; `MedxChart` exists only at
`xFactories/MedxChart`) so the rule is checkable against the tree.

## 4. Rule (a)'s kind template matches no pin file

**Finding (verbatim).** MISMATCH — rule (a)'s kind template matches no pin file
(`medxchart_openchart_pin` at contracts/; `medx_avatar_openavatar_pin` at pins/ with
source_repo/resolved_ref and no relationship:; openAvatar
`avatar-client-lab-contract-pin`). FIX rule (a) at ~240-243: "(a) a descendant pins the
product BY COMMIT, TWICE — the nested gitlink and a pin manifest at
`contracts/<product>-pin.yaml` (`kind: <descendant_repo_snake>_<product_snake>_pin`,
following `medxchart_openchart_pin` / `medx_avatar_openavatar_pin`; `relationship:
pinned_upstream_composition` where the pin covers a whole tree) — both changed in the
SAME commit. The three live pin files disagree on directory and kind form; this rule
settles the shape forward and does not retro-fit the existing two."

**Disposition: APPLIED,** verbatim, with the original clause "so a gitlink can never
silently disagree with a declared pin" preserved (it is the rule's rationale and no
finding contested it) and the three divergent files named inline.

## 5. The byte-identity floor would forbid fixing the requirement subject

**Finding (verbatim).** MISMATCH — the 11 moved requirements read "openxFactory SHALL …"
(`openspec/specs/openxwallet/spec.md:7`, `openxwallet-agent-profile/spec.md:7`); the
byte-identity floor ("zero corpus edits", ~174-183) would forbid fixing it. FIX add to
the floor §: "One carve-out, named: the 11 requirements read `openxFactory SHALL …`.
The floor covers `contracts/` BYTES — schemas, registry, corpus, validator — and NOT
the spec prose. The subject is rewritten to `openXwallet SHALL` in the same move, as
the only prose edit the floor permits, because a requirement naming the wrong
repository is not a pure move either."

**Disposition: APPLIED.** **Note on application:** the `openxFactory SHALL` sentence
begins at `:8` in both specs (`:7` is blank); the proposal cites `:8`.

## 6. `.github/workflows/pytest-suite.yml` omitted

**Finding (verbatim).** MISMATCH — `.github/workflows/pytest-suite.yml` omitted: its
checkout (`:203-206`) has `path: openxFactory`, `fetch-depth: 0`, NO `submodules:
true`; runs `pytest tests/` incl. `tests/trust-anchor/` (`test_negative_corpus.py:60,68`
use `ctx.openxwallet`) and `tests/wallet_yaml_syntax_gate/`; header names
`wallet-validation.yml` at `:5`, `:14`, `:148`; it is a required check. FIX add to
code_surface and Impact: "`.github/workflows/pytest-suite.yml` — the checkout gains
`submodules: true` (the repointed `tests/trust-anchor/` reads the wallet registry
through the `openXwallet/` gitlink), the deleted `tests/wallet_yaml_syntax_gate/` drops
from collection so the pinned collection count in its header moves, and its three
references to `wallet-validation.yml` (`:5`, `:14`, `:148`) become
`openxwallet-consumer-gate.yml`."

**Disposition: APPLIED,** to both `code_surface` and the openxFactory Impact bullet.
The pinned collection count is at `:37` (`5877 + 17 + 338 = 6232`) and the proposal now
names that line, so the move is checkable.

## 7. Wrong README block for the archive-ledger entry

**Finding (verbatim).** MISMATCH — `README.md:2254-2265` is the wrong block
(align-demote-to-round-trip-rule); the add-openxwallet archive-ledger entry is
`:2523-2536`. FIX.

**Disposition: APPLIED.** Both ranges verified; the proposal now cites `:2523-2536` and
says explicitly that `:2254-2265` is `align-demote-to-round-trip-rule`, so the error is
not re-made.

## 8. Wrong README block for the contract index

**Finding (verbatim).** MISMATCH — `README.md:290-297` wrong; wallet contract-index
entry is `:286-293`; `:310` is the identity-brokering entry's citation of openxwallet's
custody rule (reword to the pin). FIX.

**Disposition: APPLIED.** **Note on application:** `:310` sits inside the **Trust
anchors** contract-index entry (which begins at `:305`), not the identity-brokering
entry (`:294-304`); the proposal describes it accordingly. Union with QA #5 taken.

## 9. Wrong README range for the active-change ledger

**Finding (verbatim).** MISMATCH — `README.md:836-891` wrong;
add-wallet-carried-review-authority ledger entry runs `:873-927`; `:909-912` "advisory
until an operator marks it required" is stale vs ruleset 21538893; `:920-921` names the
retiring workflow + both scripts. FIX (QA reviewer reads the same region as `:836-921`
— use `:873-927` and name `:896`, `:909-912`, `:920-921`).

**Disposition: APPLIED,** union with QA #5. **Note on application:** the "advisory
until an operator marks it required" phrase is at `:896-897`, not `:909-912`; `:909-912`
carries the declined-floor / precondition prose, which the split does not touch. The
proposal names all three sub-citations with those accurate readings.

## 10. No spec deltas — `openspec validate --strict` fails

**Finding (verbatim).** MISMATCH — no deltas; `openspec validate --strict` fails.
DEFERRED to specs phase (record only).

**Disposition: DEFERRED to the specs phase.** Confirmed still the only strict error
after this pass: `OPENSPEC_TELEMETRY=0 openspec validate split-openxwallet-repo
--strict` reports exactly `[ERROR] file: Change must have at least one delta.` The
specs author owes seven capability folders — two ADDED (`domain-descendant-boundary`,
`neutral-product-pin`), three MODIFIED (`trust-anchor`, `review-authority-intake`,
`shared-contract-ownership`) and two REMOVED (`openxwallet`,
`openxwallet-agent-profile`) — the last two naming the eleven titles recorded in
`alignment-qa-lead.md` § 1.

## 11. A removed shape is a breaking major, and a major has a precondition

**Finding (verbatim).** MISMATCH — `docs/contract-versioning-policy.md:250-255`:
"Breaking (major) — a required field is added, a shape is removed, or role/vocabulary
semantics change. Requires: a CHANGELOG migration note, at least one full minor release
where the old shape produced deprecation warnings, and an update to the conformance
validator". Shedding eight registered artifacts removes shapes → major → a prior
deprecation minor is a precondition. FIX replace the Out-of-scope bullet (~511-514)
with: "Allocating the openxFactory bundle number — but NOT the class.
`docs/contract-versioning-policy.md:250` makes a removed shape BREAKING (major), and a
major requires one full prior minor of deprecation warnings. The cut therefore owes a
preceding deprecation minor that keeps the eight rows registered and marks them
relocating (the validator emitting a deprecation warning naming
`opensoft/openXwallet`), with the major following it; the numbers are allocated at
merge order per `:30-31`." ALSO add this as a new successor "P2.5 — the deprecation
minor" in the AUTHORIZES list (it can land any time before P3; P3 is the major) and as
item in "Sequencing that is not negotiable".

**Disposition: APPLIED** in all three places — the rewritten Out-of-scope bullet, a new
`P2.5` bullet in the AUTHORIZES list, and sequencing item 3 (the list renumbered to
seven items). P2.5 also has its own row in the new ## Realization evidence table.

## 12. Impact omits prose-only surfaces

**Finding (verbatim).** DRIFT — Impact omits prose-only surfaces. FIX append to Impact:
"Prose-only citations, reworded to the pin and not deleted:
`scripts/validate-identity-brokering.py:118,165,748`, `contracts/CHANGELOG.md:20` (its
additive-minor worked example names a path that leaves), `README.md:805`, `:2612`,
`scripts/proposal-support.py:978`. `health/` and `scripts/doc_health/` carry no wallet
reference at all — verified by grep — which is what makes the `doc-health`
non-declaration safe."

**Disposition: APPLIED.** Every citation re-verified, including the negative: `grep -rli
openxwallet health/ scripts/doc_health/` returns nothing.

## 13. Front matter should open with a parseable value

**Finding (verbatim).** DRIFT — front matter should open with a parseable value per
`docs/release-realization-flow.md:22-23`. FIX: `code_surface: openxFactory,
opensoft/openXwallet (new), xFactory, LedgerxFactory, OpsxFactory — ` + existing prose;
`target_release: implemented — ` + existing prose.

**Disposition: APPLIED for `code_surface`.** `target_release` already opened with
`implemented — `, so no edit was owed there; recorded rather than silently skipped.

## 14. The Purpose placeholder is in both promoted specs, not the archive

**Finding (verbatim).** DRIFT — the Purpose placeholder is in BOTH promoted specs
(`openspec/specs/openxwallet/spec.md:4`, `openxwallet-agent-profile/spec.md:4`: "TBD -
created by archiving change add-openxwallet"), not the archive. FIX ~386-387
accordingly ("both are written while they are being moved").

**Disposition: APPLIED,** with the placeholder quoted in full so the claim is
checkable.

## 15. Overshooting ranges, and two supporting facts

**Finding (verbatim).** DRIFT — ranges overshoot: document-lifecycle requirement is
`:520-598`; trust-anchor hard exit is `scripts/validate-trust-anchor.py:2582-2586`;
README wallet-gate section is `:217-229` (QA says `:217-228`; use `:217-228`). FIX
everywhere cited (~299, ~158/278/368, ~379, and front matter). Also add one sentence in
the Removed Capabilities §: `scripts/doc_health/promotion_fidelity.py:144,820-824`
already implements `CHECKED_OPS = ("ADDED","MODIFIED","REMOVED")` and the "ratified
REMOVED requirement still present" finding — the exit is tooling-supported, not merely
legal. And in P3, cite that openxFactory already nests a gitlink
(`installs/omnigent-install` in its `.gitmodules`).

**Disposition: APPLIED,** all of it. `:2582-2591` → `:2582-2586` in all four places
(front matter, P3, the trust-anchor delta, the Impact bullet); `:520-599` → `:520-598`;
`:217-231` → `:217-228` (QA's range, as ruled). Both supporting facts verified in the
tree and added: `promotion_fidelity.py:144` and `:820-824`, and the
`installs/omnigent-install` gitlink in openxFactory's own `.gitmodules`.

---

## Disposition summary

| # | Dimension | Severity | Disposition |
|---|---|---|---|
| 1 | `shared-contract-ownership` IS engaged (`:139-165`) | MISMATCH | APPLIED |
| 2 | pin grammar already ratified as `pinned_contract_manifest` | MISMATCH | APPLIED |
| 3 | rule (c) inverts both placement precedents | MISMATCH | APPLIED |
| 4 | rule (a)'s kind template matches no live pin file | MISMATCH | APPLIED |
| 5 | floor would forbid fixing `openxFactory SHALL` | MISMATCH | APPLIED |
| 6 | `pytest-suite.yml` omitted — a REQUIRED check | MISMATCH | APPLIED |
| 7 | README `:2254-2265` is the wrong block (`:2523-2536`) | MISMATCH | APPLIED |
| 8 | README `:290-297` wrong (`:286-293`); `:310` | MISMATCH | APPLIED |
| 9 | README `:836-891` wrong (`:873-927`) | MISMATCH | APPLIED |
| 10 | no spec deltas — strict validation fails | MISMATCH | **DEFERRED to specs phase** |
| 11 | removed shape = major; deprecation minor is a precondition | MISMATCH | APPLIED (P2.5) |
| 12 | Impact omits prose-only surfaces | DRIFT | APPLIED |
| 13 | front matter must open with a parseable value | DRIFT | APPLIED (`code_surface`) |
| 14 | Purpose placeholder is in both promoted specs | DRIFT | APPLIED |
| 15 | three overshooting ranges + two supporting facts | DRIFT | APPLIED |

**Blocking before ratification:** none remain in this reviewer's set. **Blocking before
circulation for validation:** #10 only, and it is a specs-phase obligation by ruling,
not a defect in the proposal's reasoning.
