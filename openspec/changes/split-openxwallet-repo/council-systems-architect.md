Reviewer role: Systems Architect (council review, read-only) — 2026-08-26
Subject proposal: openspec/changes/split-openxwallet-repo/proposal.md

# Systems Architect — `split-openxwallet-repo`

Four concerns. Each was checked against the tree rather than against the
proposal's description of the tree, which is where three of the four came from.

---

## Concern 1 — The deprecation minor is drafted as a VALIDATOR warning, and a validator warning reds the only live consumer (HIGH, raised jointly with the Adversary Engineer's #1)

**Concern.** P2.5 says the minor lands "with
`scripts/validate-openxwallet.py` emitting a deprecation warning naming
`opensoft/openXwallet`". That is the one implementation of the policy's
requirement that cannot be used here.

**Evidence.** `docs/contract-versioning-policy.md:246-248` describes a
deprecating minor as one where "the conformance validator emits warnings but
still accepts it", and `:250-255` makes a major require a prior minor of warnings
AND "an update to the conformance validator". But LedgerxFactory runs the
validator STRICT — `check_real_estate()` calls `run_validator(REPO, strict=True)`
and `err()`s on a non-zero exit (`tests/validate_wallet_estate.py:196-205`) — and
`scripts/validate-openxwallet.py:2107` returns `1` when `strict and f.warnings`.
So one new warning REDS the only live consumer. It would also edit the validator
inside a move whose entire safety argument is an empty diff, breaking both the
byte-identity floor and R6's proof. And it would be surfaced by no required check
in any case: openxFactory's own gate runs the validator without `--strict`
(`.github/workflows/wallet-validation.yml:34`).

**Verdict — VALID, HIGH. The marker is MANIFEST-carried, not validator-carried.**
A `relocating:` field on the eight rows at `contracts/manifest.yaml:1967-2082`
(target `opensoft/openXwallet`, successor tag) plus the CHANGELOG migration note,
read by manifest/release tooling — the domain-pin checkers warn when a domain
pins a bundle carrying `relocating:` rows. `scripts/validate-openxwallet.py` is
NOT edited in openxFactory by P2.5. The `:252-255` conformance-validator clause
is discharged by NAMING the pinned openXwallet validator as this family's
conformance validator from the major forward. P2.5 is a bundle cut and owes its
own `contracts/releases/<tag>.digests.yaml`. All byte-identity and R6 proofs are
restated against a NAMED CARVE COMMIT, never "HEAD".

**Disposition — APPLIED.** P2.5 rewritten end to end with the withdrawal stated
("An earlier reading of this proposal said it should; that reading is
WITHDRAWN") and all three reasons cited; § Out of scope's tail corrected the same
way; the byte-identity floor now reads "the rows at the **NAMED CARVE COMMIT** …
and **never 'HEAD'**, which is not a stable referent across a
multi-pull-request wave"; `code_surface` records TWO `contracts/releases/*.digests.yaml`
files, one per bundle cut; P2.5's evidence row lists the `relocating:` rows, the
CHANGELOG note, the emitting checker's output and its own digests file; P5a
additionally bumps LedgerxFactory `stack.yaml` to the P2.5 minor so the one live
consumer actually OBSERVES the relocation marker.

---

## Concern 2 — `submodules: true` is not one line, and three separate CI facts make it not work (HIGH)

**Concern.** The proposal treats the nested-submodule CI change as a checkout
flag. It is an authentication change, a non-recursive filter, and an import-time
path, in three different files.

**Evidence.** (a) `.gitmodules` uses `git@github.com:`, and `github.token` cannot
clone a second private org repository; the house pattern is
`doc-health-reusable.yml:143-158` and `:805-819` — `create-github-app-token@v2`,
then `git config --global url."https://x-access-token:$TOKEN@github.com/".insteadOf
"git@github.com:"` BEFORE checkout, then a scoped `git submodule update --init`.
`pytest-suite.yml:203-206` has none of it. (b) doc-health's init filter
`grep -E '^(openxFactory|xFactories/)'` (`:154-158`, `:815-819`) is
non-recursive, so `openxFactory/openXwallet/` is never initialized in aggregation
runs. (c) `tests/trust-anchor/test_negative_corpus.py:47` and
`test_declaration_perimeter.py:55` both call
`MODULE.load_yaml(MODULE.OPENXWALLET_REGISTRY_PATH)` at setup, so a repointed
constant that is anything other than a real `Path` at module scope kills every
trust-anchor test at collection.

**Verdict — VALID, HIGH.** All three go into `code_surface` and P3. Design chooses
between the app-token + `insteadOf` pattern and declaring the nested `.gitmodules`
URL as `https://github.com/opensoft/openXwallet.git`. The evidence row must pin
PASS/SKIP counts, not collection alone, so a silent skip is distinguishable from
a pass.

**Disposition — APPLIED.** `code_surface` now spells out that the checkout change
"is NOT one line", names the house pattern and cites it, and adds
`.github/workflows/doc-health-reusable.yml` as a surface with both filter sites.
P3 gains a "CI half is not one line of YAML" block covering all three facts, and
states that P3 may NOT "add `submodules: true` and call it done". A dedicated
evidence row pins the **PASS / SKIP counts**.

---

## Concern 3 — There is no "authority-register mode" to build, the `ENVELOPE_SCHEMA_PATH` edit is a no-op, and two real gaps hide behind those two non-problems (MEDIUM, third limb raised jointly with the Adversary Engineer's LS-A3)

**Concern.** The proposal describes work that does not exist and omits work that
does.

**Evidence.** `repo_scan` calls `check_register(f, target, repo_ctx)` with the
SCAN TARGET (`scripts/validate-openxwallet.py:2091`), and `check_register` joins
that `base_dir` with `REGISTER_DIR_PARTS` (`:1865`; `("governance",
"review-authority")` at `:1780-1781`). So
`python3 openXwallet/scripts/validate-openxwallet.py .` from the openxFactory
root already reads the register with ZERO code change; `main()` takes one
positional `path` plus `--strict` and nothing else. Likewise
`ENVELOPE_SCHEMA_PATH = ROOT/"contracts"/"schemas"/"hermes-job-envelope.schema.yaml"`
(`:218`) needs no edit at all if the vendored copy sits at the identical relative
path, since `:2156` prints `.relative_to(ROOT)`. Behind those: `repo_scan`'s
corpus exclusion keys on the `examples` path prefix AND an `openxwallet*` part
(`:2050-2053`), so a carve that changes those prefixes re-adjudicates the 36
intended-invalid negatives as LIVE records inside openxFactory's REQUIRED check;
and the consumer gate's sweep will walk INTO the `openXwallet/` gitlink, whose
`.git` is a FILE, so the existing `.git` skip does not fire.

**Verdict — VALID, MEDIUM.** Replace the invented mode with the literal
invocation; restate R6/R2 as an EMPTY diff; make the vendored path a P2
REQUIREMENT; add the examples-prefix acceptance line and the sweep exclusion.

**Disposition — APPLIED.** The R6 rulings item now says "**There is NO 'generic
authority-register mode' to build — the capability already exists**", cites
`:2091`/`:1865`/`:1780-1781`/`:2110-2118`, and restates the proof as "the diff …
is **EMPTY** — not 'touches only `ENVELOPE_SCHEMA_PATH`'". P2 requirement (i) is
the exact vendored path; requirement (ii) is the examples-prefix acceptance line.
P3 carries the sweep exclusion (mechanism for design), and ## Impact's workflow
bullet is reworded from "authority-register mode" to the literal invocation.

---

## Concern 4 — Aggregation tooling cannot see a root-level repository, so "derives automatically … nothing to design" is false (MEDIUM)

**Concern.** The NotebookLM Impact bullet asserts that
`xf-ideation-openxwallet` derives automatically once the repository exists. Two
code sites say otherwise, and the openAvatar precedent proves it empirically.

**Evidence.** `scripts/sync-notebooklm-books.py:761` builds the repository set as
`["openxFactory", *pinned_factory_paths(root)]`, and `pinned_factory_paths`
(`:644-663`) matches only `^\s*path\s*=\s*(xFactories/\S+)\s*$`.
`scripts/doc_health/ideation_routing.py` `_governed_repo_ids` (`:225-235`) admits
only `openxFactory` and `xFactories/<Name>`, so a root-level product is classed
EXTERNAL and falls under the nightly-skip / strict-materialization path. The
proof: **there is no `xf-ideation-openavatar` book today**, months into the
ratified openAvatar precedent.

**Verdict — VALID, MEDIUM.** State the gap and add a successor naming both code
sites, with `xf-ideation-openxwallet` as its acceptance.

**Disposition — APPLIED.** The Impact bullet replaced with the stated gap and
both citations; successor **P4b — root-level governed-repo recognition** added
(an openxFactory pull request, since both sites are openxFactory's), with its own
realization-evidence row and `xf-ideation-openxwallet` as acceptance;
`code_surface` gains both script paths.

---

**Architecturally, the boundary is right and the pin direction is the interesting
half.** `neutral-product-pin` is doing real work that
`repo-boundary-governance` could not: it is the first statement in this corpus of
how openxFactory behaves as a CONSUMER. My four concerns were all about the
proposal describing the tree from the extraction plan rather than from the tree.
