# Design: split-openxwallet-repo

Companion to `proposal.md`. The proposal argues the doctrine, carries R1–R8 as
LOCKED constraints and names the wave; this document records the decisions the
council's clarifications demand (N1–N8), the alternatives rejected, the surviving
risks, and the ordered migration with a rollback per step. Every code fact was
re-verified in the tree on 2026-08-26 at openxFactory `c6656edd`.

## Context

**Current state.** The wallet is one product filed as features of a factory
layer: 55 files under `contracts/openxwallet/`, 8 under
`contracts/openxwallet-agent-profile/`, a 2175-line validator (21 rules
`(a)`–`(u)`), a 121-line syntax gate with one test module, three Speckit features
(`specs/006-openxwallet-contracts/`, `010-wallet-validator-ci/`,
`012-wallet-issuer-anchor/` — 25 files), a 6-file archive packet, two promoted
specs, a 34-line CI workflow. Eight artifacts carry per-file digests in
`contracts/manifest.yaml` (rows at `:1974`, `:1992`, `:2005`, `:2018`, `:2031`,
`:2044`, `:2057`, `:2070`; fields `id / path / source_path / type /
schema_version / sha256 / compatibility / adapter_owner / consumption_rule`);
everything else is content-addressed by commit (`:1968-1972`).

**The live consumer.** LedgerxFactory `tests/validate_wallet_estate.py`:
`find_openxfactory()` (`:47-63`) walks up five levels for
`openxFactory/scripts/validate-openxwallet.py` and returns `None` rather than
skipping; `run_validator()` (`:195-210`) invokes it `--strict`, requires exit 0,
and parses `repo scan: (\d+) openxWallet artifact` requiring a count ≥ 5.
`stack.yaml:10-16` pins openxFactory `39539fd4…` at `contract_ref_type: commit`.

**The live ruleset.** Org ruleset 21538893 has required `wallet-validation` on
`main` since 2026-08-26. The token is the JOB ID
(`.github/workflows/wallet-validation.yml:20`), not the filename, and the gate
runs the validator WITHOUT `--strict` (`:34`) — the two facts the rename-by-alias
resolution rests on.

**The wallet arc.** `add-wallet-carried-review-authority` task 2.5 is DONE (the
ruleset); 2.6 (the malformed-grant red-proof) is open; S3 and S5 are entirely
open — 15 of 21 open tasks — and `tasks.md` 8.1 (RULED 2026-08-26, `:317-330`)
puts `openxwallet` core deltas at S5. Those deltas are why the extraction goes
first.

**Constraints.** R1–R8 are constraints, not questions. The **byte-identity
floor** binds: for the eight digested artifacts `sha256sum` at openXwallet
`wallet-v1.0` equals the digest recorded at the NAMED CARVE COMMIT and the carved
subtree diffs empty against it — with one prose carve-out, the `openxFactory
SHALL` → `openXwallet SHALL` subject at `openspec/specs/openxwallet/spec.md:8`
and `openxwallet-agent-profile/spec.md:8`.
`docs/contract-versioning-policy.md:248-252` makes a removed shape BREAKING and
requires a preceding full minor of deprecation warnings; `:245-247` requires that
minor to state a removal version and migration path in the CHANGELOG; `:30-31`
forbids reserving a minor number before merge order is known. Shared-tree
discipline applies: `contracts/manifest.yaml` and the README Records block are
shared surfaces, and a freeze across P2.5 → P3 is unenforceable.

**Stakeholders.** The **openxFactory operator** merges every phase and owns both
rulesets. **LedgerxFactory** is the only live consumer and fails loudly by
design, so sequencing is a correctness property. The **codexFactory merge
master** governs whether a pull request touching the pin is council-clearable
(P3b). **hermes-install** is the future issuer host, a stakeholder in Q4 only.

## Goals

- Fix the shape of every artifact the proposal names but leaves unspecified: the
  pin file, both pin verifiers, the consumer gate, the `relocating:` marker, the
  declared consumer pin, the floor entries.
- Resolve N1–N8, each to running code or a named file, never prose.
- Keep the move bisectable: one provable empty diff, one named carve commit, one
  prose carve-out.
- Keep every gate at today's strength, with no operator act between P3 and merge.

## Non-goals

- Any runtime, issuer service or key-custody host (Q4).
- Any rename of a `kind:`, capability id, finding code, filename or path in v1
  (R2); the `xfactory_wallet_*` prefix ships knowingly stale.
- Moving `governance/review-authority/` (R6), or resolving Q1's durable shape.
- Widening codexFactory's floor to `governance/review-authority/{grants,wallets,
  attestations}/` — real, pre-existing, the arc owner's.
- Backfilling the wallet family into `contracts/releases/*.digests.yaml`, or
  correcting the stale 16/33 and "nineteen rules" counts.
- Allocating the openxFactory minor number for P2.5.

## Decisions

### D1 — `contracts/openxwallet-pin.yaml` reuses `kind: pinned_contract_manifest`

**Decision.** Mirror the realized keycloak-install shape
(`installs/keycloak-install/config/contracts/identity-brokering/manifest.yaml:1-20`)
field for field, plus two additions:

```yaml
schema_version: 1
kind: pinned_contract_manifest
contract_bundle_tag: wallet-v1.1     # label only; never the trusted referent
source_repository: opensoft/openXwallet
submodule_path: openXwallet          # ADDED: the gitlink this pin governs
commit: <40-hex openXwallet commit>
revision_kind: commit                # a tag-only pin is refused
digest_algorithm: sha256
digest_source: contracts/manifest.yaml       # openXwallet's own manifest
carve_commit: <40-hex openxFactory sha>      # ADDED: byte-identity referent
resync_runbook: openXwallet/docs/pin-resync-runbook.md
files:                   # path + sha256, one per digested member
pinned_by_commit_only:   # path only
```

The eight `files:` members are the eight digested manifest rows: seven under
`contracts/openxwallet/` (record, custody-registry-schema, custody-registry,
grant, grant-exercise, distinct-holder-constraint, subject-attestation) plus
`openxwallet-agent-profile/openxwallet-agent-composition.schema.yaml`.
`pinned_by_commit_only:` carries `scripts/validate-openxwallet.py`,
`scripts/wallet-yaml-syntax-gate.py`, both `examples/` directories and both family
READMEs.

**Rationale.** The grammar is ratified and realized twice; only the DIRECTION is
new, so reusing the kind unchanged keeps `neutral-product-pin` a statement about
direction rather than a new shape. `submodule_path` is borrowed from the one live
descendant pin carrying it (`MedxChart/contracts/openchart-pin.yaml:8`) because a
pin with no path cannot be checked against a gitlink. `carve_commit` is in the
file, not only the runbook, because the byte-identity referent must survive into
the tree the gate reads — "HEAD" is no referent across a multi-PR wave.

**Rejected.** *A new `kind: openxfactory_openxwallet_pin`* on rule (a)'s
`<consumer>_<product>_pin` template: rule (a) governs DESCENDANTS, and one
grammar stretched over both relationships would make it claim openxFactory is a
wallet descendant. *Declaring the pin in `stack.yaml`*:
`shared-contract-ownership:146` is written for consuming an openxFactory release,
and this is the reverse direction — exactly what that capability's MODIFIED delta
states. *Per-file digests for the validator, gate and corpus*: the publisher's own
manifest declares them "content-addressed by commit; no per-file digest"
(`:1968-1972`), and inventing digests inside a byte-identical move would add rows
the publisher never published; the gitlink commit fixes those bytes as strongly.

### D2 — `scripts/verify-openxwallet-pin.py`, and every refusal carries the remediation (N1)

**Decision.** A new openxFactory script checks, in order: (1) the submodule is
initialized — `openXwallet/.git` **exists** rather than `is_dir()`, because a
submodule's `.git` is a FILE; (2) the RECORDED gitlink (`git ls-tree HEAD --
openXwallet`) equals `commit`; (3) the CHECKED-OUT revision (`git -C openXwallet
rev-parse HEAD`) equals `commit` — both, because a detached checkout can differ
from the recorded gitlink and only one comparison catches each case; (4) each of
the eight `files:` members recomputes to its `sha256`; (5) every
`pinned_by_commit_only:` path exists (presence only — identity comes from (2) and
(3)); (6) `revision_kind` is `commit` and `commit` is 40 hex. Exit 0, or exit 2
with a named code: `pin-submodule-uninitialized`, `pin-gitlink-mismatch`,
`pin-checkout-mismatch`, `pin-digest-mismatch`, `pin-member-missing`,
`pin-tag-only`.

Every fail-closed refusal — here, `validate-trust-anchor.py` rule (f), and
openXwallet's vendored-schema verify — prints one fixed trailer: *Remediation:
`git submodule update --init --recursive openXwallet`; if the pin itself is
stale, follow `openXwallet/docs/pin-resync-runbook.md`.*

**Where it runs.** First step of `openxwallet-consumer-gate.yml`, before anything
pinned is trusted; and inside `scripts/validate-trust-anchor.py`'s `main()`,
never at import. `OPENXWALLET_REGISTRY_PATH` (today `:323-324`) stays a
module-scope plain `Path`, rebased onto the pin's `submodule_path` as a pure
string join with no I/O, because `tests/trust-anchor/test_negative_corpus.py:47`
and `test_declaration_perimeter.py:55` both call
`MODULE.load_yaml(MODULE.OPENXWALLET_REGISTRY_PATH)` at setup — any resolution
that can fail at import kills every trust-anchor test at collection. The
file-absent exit at `:2581-2585` is replaced by the verifier's call, so the
refusal gains identity where it had only presence.

**Rejected.** *Inline shell in the workflow* — not runnable locally, not
testable, and the refusal strings would exist in three copies that drift.
*Folding the check into `validate-openxwallet.py`* — that file is the pinned
artifact, editing it breaks R6's empty diff, and a verifier living inside the
thing it verifies is not a verifier.

### D3 — The consumer gate: SSH stays, the app token rewrites it; the invocation is pinned by a positive test (N5, N7)

**Decision on auth.** `.gitmodules` keeps `git@github.com:` and CI uses the house
pattern of `doc-health-reusable.yml:154-158`: `create-github-app-token@v2`, then
`git config --global url."https://x-access-token:$TOKEN@github.com/".insteadOf
"git@github.com:"` BEFORE checkout, then a scoped `git submodule update --init
openXwallet`. Applied identically to `pytest-suite.yml` (whose checkout at
`:203-206` has none of it) and to both non-recursive init filters in
`doc-health-reusable.yml` (`:154-158`, `:815-819`), which gain a second scoped
init for `openxFactory/openXwallet`. *Rejected: declaring the nested URL as
`https://github.com/opensoft/openXwallet.git`* — openXwallet is PRIVATE, so an
anonymous HTTPS clone fails and a token is still required; the URL change only
moves which credential helper needs it, while making every human clone prompt for
HTTPS credentials instead of using the operator's key, and openxFactory's
`.gitmodules` is already `git@github.com:opensoft/Omnigent-Install.git`.
*Rejected: `--recursive`* — it would pull `installs/omnigent-install` and every
domain's nested submodules into every aggregation doc-health run.

**Steps.** app token → `insteadOf` → checkout → `verify-openxwallet-pin.py` →
`python3 openXwallet/scripts/wallet-yaml-syntax-gate.py .` → `python3
openXwallet/scripts/validate-openxwallet.py . | tee wallet-gate.log` (no
`--strict`, unchanged from `wallet-validation.yml:34`) → the register-read
assertion. `jobs:` keeps the key `wallet-validation`.

**Decision on the pinned invocation.** One test file,
`tests/openxwallet_consumer_gate/test_gate_invocation.py`, collected by the
REQUIRED `pytest-suite`. It loads the workflow YAML, asserts `jobs` contains
`wallet-validation`, and asserts one step's `run` is exactly `python3
openXwallet/scripts/validate-openxwallet.py .` — the argument present AND equal
to `.`, because `main()` runs `repo_scan` only `if args.path is not None`
(`:2157`) and `repo_scan` reads the register only `if sweep`, where `sweep =
target.is_dir()` (`:2039`, `:2090-2091`). A missing or file-valued argument is a
green check that opened no register.

**The assertion is POSITIVE and needs no edit to the pinned code.** On the happy
path `check_register` emits nothing: the only lines naming
`governance/review-authority/register.yaml` are its failure findings
(`:1873-1877`, `:1884-1904`, `:1962-1966`), and the absent-register note
(`:1878`) names no path. The test asserts the conjunction the validator DOES
produce — the output carries the `repo scan:` note (`:2092-2093`, sweep proven)
AND carries neither `no intake register at this tree` nor any `register-*` code,
so `reg_path.exists()` was true AT the scan target. That pair positively proves
the register at the openxFactory root was opened. The negative half is task 2.6's
red-proof: a malformed row emits `register-row-malformed` naming the full path. A
durable positive line lands upstream at `wallet-v1.1` (D4) as an `f.note` naming
`reg_path` when the register IS read — a NOTE, never a warning, because `:2107`
reds a `--strict` run on warnings and LedgerxFactory runs `--strict`. The test
asserts both forms so it does not go stale across the tag.

### D4 — The sweep skips nested repositories by construction, upstream, at `wallet-v1.1` (N4)

**Decision.** `repo_scan` prunes any file whose path descends from a directory
other than the scan root that carries a `.git` entry, file or directory. The
change is made in openXwallet and published as `wallet-v1.1`, and **openxFactory's
first pin is `wallet-v1.1`**, not `wallet-v1.0`.

**Rationale.** The existing filter is `set(path.parts) & SKIP_DIR_NAMES` over
`target.rglob("*.y*ml")` (`:2040`, `:2044-2045`) with `SKIP_DIR_NAMES = {".git",
"node_modules", "__pycache__", ".venv"}` (`:295`), so a submodule directory is
never skipped and its `.git` FILE is all the set catches. The corpus exclusion at
`:2050-2053` keys on path PARTS, so the 36 negatives and 17 positives stay
excluded inside the submodule — the real hazard is the non-`examples/` YAML the
carve brings along (`specs/006-openxwallet-contracts/evidence/`,
`tests/wallet_yaml_syntax_gate/`, openXwallet's own OpenSpec instance) plus the
canonical custody registry being re-indexed as a live record of the scanned repo.
That hazard sits inside a REQUIRED check, so it closes BEFORE P3, not after. The
prune also closes the same pre-existing hole for `installs/omnigent-install`,
which the sweep walks into today, so the rule is not wallet-shaped. Byte-identity
is untouched: it is proven for `wallet-v1.0` against the carve commit, and
`wallet-v1.1` is one auditable additive-minor diff on top (`:242-244`).

**Rejected.** *Adding `openXwallet` to `SKIP_DIR_NAMES`* — it hard-codes one
consumer's directory name into the product's validator, the exact coupling the
split removes, and misses every other nested repository. *Narrowing the scan
scope* — `check_register` joins the SCAN TARGET with `("governance",
"review-authority")` (`:1865`, `:1780-1781`), so any target below the root
silently disables the register read. *A `--exclude` CLI flag* — it edits
`main()`'s argparse (`:2113-2118`), which both R6's zero-refactor proof and D3's
test key on, and an exclusion the caller supplies is one the caller can omit, the
same vacuous-pass class as N7. *Deinit or relocate the checkout in CI* — it
contradicts R6's literal invocation, a LOCKED ruling.

### D5 — `relocating:` on the eight rows; `check-openxfactory-pin.py` is the emitter (N2)

**Decision.** Each of the eight rows gains one sibling key — `relocating: {to:
opensoft/openXwallet, tag: wallet-v1.0, since: contract-v<the P2.5 minor>}`, as a
nested mapping. **No `removed_at` on the row.**
`docs/contract-versioning-policy.md:245-247` puts the removal version and
migration path in the **CHANGELOG**, and the CHANGELOG entry states them: removal
at the next MAJOR bundle, migration via `contracts/openxwallet-pin.yaml` and
`openXwallet/docs/pin-resync-runbook.md`. Naming the major is permitted where
naming the minor is not — `:30-31` prohibits reserving a MINOR before merge order
is known, and there is exactly one next major where the next minor depends on
merge order. P2.5's own number stays unnamed here.

**The emitter is `scripts/check-openxfactory-pin.py`.** It is the only candidate
with a warning tier — `PASS, WARN, ERROR, SKIP` at `:35`, returned by
`classify()` at `:43` — while `scripts/validate-domain-openxfactory-pins.py`
carries no `warn` token in its 138 lines, so making it emit would force a
relocation notice to be an ERROR and red every domain pinning the deprecation
minor: precisely the failure the manifest-carried marker was chosen to avoid.
**How it reaches LedgerxFactory:** P5a bumps `stack.yaml`
`xfactory.contract_ref` to the P2.5 minor AND adds one invocation of the pinned
checker to LedgerxFactory's estate run, so the warning is observed by the one live
consumer; without that second half the deprecation window is unobserved and the
policy precondition is a formality.

**Rejected.** *A validator-emitted warning* — withdrawn in the proposal, all three
reasons re-verified: `validate_wallet_estate.py:195-210` runs `--strict`, `:2107`
reds on `strict and f.warnings`, and openxFactory's gate runs without `--strict`
so nothing required would surface it. *The release-inventory tooling* — it runs at
cut time in the publisher, and the audience for a relocation notice is the
consumer.

### D6 — Two distinct published bundles, each with its own digests file

**Decision.** P2.5 is a deprecating minor: the eight `relocating:` fields, the
CHANGELOG migration note, and its own `contracts/releases/<minor>.digests.yaml`
over a release surface that still CONTAINS the eight artifacts. P3 is the major:
the eight rows deleted, the CHANGELOG removal entry, and its own
`contracts/releases/<major>.digests.yaml` over a surface that no longer contains
them. They must be separately published tags — `:250-251` requires "at least one
full minor release", so P3 cannot fold into P2.5's cut, and `:31-32` says a bundle
is not published until its tag exists. The `:251-252` "update to the conformance
validator" clause is discharged by naming, from the major forward, the pinned
openXwallet `scripts/validate-openxwallet.py` at the digest in
`contracts/openxwallet-pin.yaml` as this family's conformance validator: the move
IS the update. The validator is not edited in openxFactory by P2.5 at all.

### D7 — The carve: twelve path sets, no renames, provenance in three places

**Decision.** `git filter-repo` with one `--path` per set, exact paths, no globs,
no `--path-rename`:

```
contracts/openxwallet/                    openspec/specs/openxwallet/
contracts/openxwallet-agent-profile/      openspec/specs/openxwallet-agent-profile/
scripts/validate-openxwallet.py           openspec/changes/archive/2026-08-08-add-openxwallet/
scripts/wallet-yaml-syntax-gate.py        specs/006-openxwallet-contracts/
tests/wallet_yaml_syntax_gate/            specs/010-wallet-validator-ci/
.github/workflows/wallet-validation.yml   specs/012-wallet-issuer-anchor/
```

The carve COPIES; it deletes nothing from openxFactory. P3's eight deletions are
its own commit, and three of the twelve sets are deliberately NOT deleted there:
the two promoted specs empty when `openspec archive` applies the REMOVED deltas,
and the archive packet is a record that is annotated, never removed.

**Completeness check.** `git ls-tree -r --name-only <carve_commit> --` over the
twelve paths, sorted, equals the same listing at `wallet-v1.0` filtered to those
prefixes — with two explicit non-empty counts, because a shorthand loses them: 7
files under `specs/006-openxwallet-contracts/` (its `evidence/` included) and 36
under `contracts/openxwallet/examples/negative/`. **Examples-prefix preservation**
is an acceptance line: both `examples/` directories exist at identical relative
paths in the carved tree, because `:2050-2053` keys on `"examples" in path.parts`
AND an `openxwallet*` part, so a rename re-adjudicates 36 intended-invalid
negatives as LIVE records inside a REQUIRED check.

**The vendored envelope schema** is added by the scaffold commit, not the carve,
at exactly `contracts/schemas/hermes-job-envelope.schema.yaml` — the identical
relative path, so `ENVELOPE_SCHEMA_PATH` (`:218`) and its `.relative_to(ROOT)`
print need no edit and R6's empty diff survives. `contract_pin.yaml` records it on
openAvatar's model (`openAvatar/contract_pin.yaml`) with a named `verify_pin` that
fails closed pre-sync, invoked in `wallet-validation` BEFORE the validator:
`main()` checks only `.is_file()` (`:2123`), presence and not identity, while rule
(g) reads the approval-scope vocabulary out of that file.

**The CONSUMED-member row (N8)** in openXwallet's `contracts/manifest.yaml` keeps
the publisher's nine fields — `compatibility: canonical_openxfactory_contract`,
`adapter_owner: openxFactory`, `sha256` equal to the pinned openxFactory row's —
and adds three: `member_class: consumed`, `release_surface: false`,
`pinned_openxfactory_bundle: contract-v<pinned>`. Those declared fields are how
the wallet's release tooling excludes it: `wallet-vN.M.digests.yaml` selects
`member_class: owned` only. Exclusion by DECLARED FIELD, not by path heuristic — a
`contracts/schemas/` heuristic breaks the day openXwallet publishes a schema of
its own there. The row satisfies `shared-contract-ownership:142`'s
all-markers-together test without claiming ownership of an openxFactory contract.

**Carve-commit provenance** is recorded in three places, one machine-read:
`carved_from: {repository, commit}` in openXwallet's `contracts/manifest.yaml`;
`carve_commit:` in openxFactory's pin file; and the procedure in the cutover
runbook. *Rejected: a bare `CARVE_COMMIT` file* — an unschema'd file nothing reads
is the failure class of a governance floor whose source of truth is loose
markdown.

### D8 — openXwallet bootstrap

**Decision.** In order: the case-variant repository-name check; repository
creation; the carve; `.github/CODEOWNERS`; the ruleset created in **EVALUATE**
mode; one trivial pull request so `wallet-validation` reports once and becomes
selectable; promote to **ACTIVE**. Day-one REQUIRED is impossible and is recorded
as unachievable, not promised. Two workflows: `wallet-validation.yml` (job id
`wallet-validation`, deliberately the same token name as openxFactory's — the
token names the check's function and the repositories are distinct namespaces; a
different name would need its own runbook language and its own rename successor)
and `pytest-suite`. Two docs: `docs/openxwallet-cutover-runbook.md`, authored
before the carve it describes with a rollback written before each phase is taken;
and `docs/pin-resync-runbook.md` on openAvatar's shape
(`openAvatar/docs/pin-resync-runbook.md`: Preconditions, Checklist, re-verify the
pin offline, re-run the offline gate suite). `wallet-v1.0` is tagged only after
the byte-identity proof.

### D9 — LedgerxFactory: three candidates, and a sibling declared pin (N6)

**Decision.** `find_openxfactory()` resolves in three ordered candidates —
`openxFactory/openXwallet/scripts/validate-openxwallet.py`, then
`openXwallet/scripts/validate-openxwallet.py`, then
`openxFactory/scripts/validate-openxwallet.py`. Nested leads because the finder
walks UP and would otherwise resolve the AGGREGATION's root gitlink, a different
commit that `contracts/openxwallet-pin.yaml` does not govern. The third keeps
pre-P3 checkouts working and is dropped at P5b.

The declared pin is a SIBLING block in `stack.yaml` mirroring `xfactory:`
(`:10-16`) field for field: `contract_repo: github.com/opensoft/openXwallet`,
`contract_name: openXwallet`, `contract_ref_type: commit`, `contract_ref:
<40-hex>`, `contract_bundle_tag: wallet-v1.1`, `contract_schema_version: 1`,
`contract_declared_at`, `contract_source: openxFactory-nested-submodule-pin`,
plus the preserve comment `stack.yaml:18-19` already carries ("re-pin tooling must
preserve this block; regenerating it away is a health finding"). Sibling, not
nested under `xfactory:`, because nesting would assert openXwallet is a component
of the openxFactory release; it is a separate product openxFactory itself pins.
`contract_ref_type: commit` is carried, matching `:12`, so the tag stays a label.
P5a bumps `xfactory.contract_ref` to the P2.5 minor.
`specs/016-posting-segregation-of-duties/data-model.md:5` — and `plan.md:26`,
`quickstart.md:4`, `spec.md:376` — are COMMIT pins to `e5554028`, re-pinned to the
openXwallet commit at `wallet-v1.0` rather than path-rewritten.

### D10 — codexFactory P3b: two entries, and why `.gitmodules` is not a third

**Decision.** `never_clearable_paths` gains exactly
`contracts/openxwallet-pin.yaml` and `openXwallet`. The bare gitlink name is what
`git diff --name-only` reports and what `_parse_exact_path` accepts — it rejects a
leading or trailing `/` and any of `*?[]` (`repository_floor.py:47-59`) — and
`matching_paths` is exact set membership (`:30-32`, `path in protected`).

**`.gitmodules` is deliberately not added.** A URL swap alone cannot change what
runs: D2 checks the recorded gitlink, the checked-out revision and the eight
digests against the pin, so a fork at the same commit and bytes is inert and a
fork at any other commit fails. Any pull request that actually changes which
reader runs must edit the pin file, which IS floored. One chokepoint, chosen over
a fence around every adjacent file.

### D11 — P4 gitlink equality is a mode of the openxFactory verifier; P4b widens by allowlist

**Decision.** The root-equals-nested check is `verify-openxwallet-pin.py
--aggregation-root <path>`: one implementation and one refusal vocabulary, living
in openxFactory, INVOKED from the aggregation's doc-health run — the only CI that
initializes both gitlinks. *Rejected: a second script in xFactory*, which has no
validator convention of its own and would drift a duplicate refusal set.

P4b widens two openxFactory sites by an explicit ALLOWLIST of root-level neutral
products (`openXwallet`, `openAvatar`), not by admitting every root-level
`.gitmodules` pin: `pinned_factory_paths` matches only
`^\s*path\s*=\s*(xFactories/\S+)\s*$` (`sync-notebooklm-books.py:652-653`) and the
repository set at `:761` is `["openxFactory", *pinned_factory_paths(root)]`;
`_governed_repo_ids` (`ideation_routing.py:224-235`) admits only `openxFactory`
and `xFactories/<Name>`. Admitting every root pin would enrol `installs/*` as
governed ideation repositories. Acceptance: `xf-ideation-openxwallet` exists after
one `--apply` — and the same widening finally produces `xf-ideation-openavatar`,
absent today five months into the ratified precedent.

### D12 — Two prose edits, and the proof's declared scope

**Decision.** The move carries exactly two prose edits, both outside the byte
floor, both enumerated so the diff is checkable: the `openxFactory SHALL` →
`openXwallet SHALL` subject at `openspec/specs/openxwallet/spec.md:8` and
`openxwallet-agent-profile/spec.md:8`, and the `## Purpose` placeholder at `:4` of
each ("TBD - created by archiving change add-openxwallet…"), written in the move
because a moved spec whose Purpose names another repository's archiving change is
not a pure move either. The floor covers `contracts/` BYTES and does not reach
spec prose at all, which is why one carve-out permits both.

**The proof is a two-part table** in the runbook and in P2's evidence row. Part
one: eight rows, `sha256sum` at `wallet-v1.0` against the digest recorded at the
carve commit. Part two: `git diff` EMPTY over `contracts/openxwallet/`,
`contracts/openxwallet-agent-profile/`, `scripts/validate-openxwallet.py`,
`scripts/wallet-yaml-syntax-gate.py`, `tests/wallet_yaml_syntax_gate/`, the three
Speckit sets and the archive packet; and diff-limited-to-two-lines over each
promoted spec, asserted line by line at `:4` and `:8`.

### D13 — The corpus exit needs no checker change, and the window it opens has no checker

**Decision.** Two `## REMOVED Requirements` blocks naming all eleven titles
verbatim; no `superseded` header, no emptied stub spec, no archived-record
rewrite; the two capability directories go with their last requirement.
`promotion_fidelity.py` already carries `CHECKED_OPS = ("ADDED", "MODIFIED",
"REMOVED")` and already emits "ratified REMOVED requirement … is still present",
so the exit is tooling-supported with zero checker change and that finding must
read zero after `openspec archive`. The eleven titles are the join key — it keys
on (capability, normalized title), so one character of drift leaves the 2026-08-08
ADDED writer authoritative and the removal invisible.

**What the checker cannot do, stated.** Between P3's merge and this change's
archive, canon describes contracts openxFactory no longer holds, and
`promotion_fidelity.py` does NOT fire there — the deltas are not yet archived. The
window is a doc-health silence rather than a finding, so the wave's own sequencing
is its only control.

### D14 — The token survives by alias; the rename is a successor

**Decision.** `openxwallet-consumer-gate.yml` keeps `jobs: wallet-validation:`.
Ruleset 21538893 is edited by nothing in this wave, the token reports on P3's own
pull-request head from the new file, and no operator act stands between P3 and
merge. Both alternatives are unmergeable and are named so neither is
re-proposed: delete-first means the required token never reports on P3's own pull
request; repoint-first fails because the new token is not selectable until a
workflow has reported under it once. The rename — add
`openxwallet-consumer-gate` alongside, land one green pull request reporting under
both, drop the old — is a SUCCESSOR and a precondition of nothing here.

## Risks and trade-offs

- **[The register row expires 2026-11-23]** → `register.yaml:37` carries
  `expires_at: "2026-11-23T12:00:00Z"` and `check_register` raises
  `register-row-expired` as an ERROR past that instant (`:1962-1966`), reddening
  the REQUIRED gate on every later pull request, the wave's own included, so its
  evidence rows become unfillable. *Mitigation:* re-issue the row before
  2026-11-23, or do not schedule P3 after 2026-11-01. There is no third option.
- **[Shared-tree collisions: the manifest, the README Records block, the
  validator]** → P2.5's eight `relocating:` fields and P3's eight deletions sit in
  a file other sessions edit, the README ledger is likewise shared, and both are
  surfaces S3/S5 may touch; a freeze is unenforceable. *Mitigation:* P3 rebases
  and RE-VERIFIES the eight digests immediately before merge, and that
  re-verification — not a P2-era artifact — is what its evidence row carries;
  commits use explicit pathspecs; after the cut the validator is not an
  openxFactory file to collide on at all.
- **[Stale checkouts]** → a pre-P3 checkout has the validator in-tree and no
  gitlink. *Mitigation:* the finder's third candidate keeps LedgerxFactory
  resolving until P5b, and the verifier refuses with D2's remediation trailer
  rather than falling back — an unanswerable question is never an implicit pass.
- **[The grants/wallets/attestations floor gap]** → codexFactory's floor omits
  `governance/review-authority/{grants,wallets,attestations}/`, so those files are
  editable outside the floor with only the register index protected. Named,
  pre-existing, the arc owner's; neither fixed nor depended on here, and the same
  goes for lead-security's 2026-08-26 floor-reachability finding.
- **[The P3→P4 window]** → between P3's merge and P4-plus-`--init` NEITHER gitlink
  candidate exists in any checkout, and `find_openxfactory()` returning `None` is a
  loud failure by design. *Mitigation:* P3, P3b and P4 land in one wave, before
  LedgerxFactory's next estate run.
- **[`wallet-v1.1` adds a step, and the prune changes consumer behavior]** → D4's
  fix must precede P3, and it stops LedgerxFactory adjudicating files inside any
  nested repository of its own. *Mitigation:* Ledgerx wallet records live at
  `tenants/ledgerxcorp/wallets/*`, not in a submodule, so `run_validator()`'s ≥5
  assertion is unaffected; P2b's evidence is a green Ledgerx run on the v1.1 reader.
- **[The vacuous-pass class]** → every control here has a shape that passes while
  checking nothing: a pinned validator invoked with no target, a presence check
  standing in for a digest check, a gate whose log names no register, a silently
  skipped `tests/trust-anchor/`. *Mitigation:* D3's positive assertion, D2's
  fail-closed refusals, and `pytest-suite.yml`'s pinned header count at `:37`
  becoming a pinned TRIPLE — collected, passed, skipped — read from the JUnit XML
  attributes rather than grepped from the human summary, so a skip moves a pinned
  number and fails.
- **[Case-variant repository name]** → GitHub names are case-insensitive-unique,
  so `openxwallet` or `OpenXWallet` anywhere in the org or a fork collides.
  *Mitigation:* checked and recorded BEFORE the carve, the runbook's first step.

## Migration plan

Ordered; each step's rollback is written before the step is taken.

1. **P5a.1 — LedgerxFactory finder.** The three-candidate order alone,
   forward-compatible, lands any time. *Rollback:* revert; candidate three is
   today's behavior.
2. **P2 — carve, scaffold, prove, tag `wallet-v1.0`** from the NAMED CARVE COMMIT.
   *Rollback:* nothing pins openXwallet yet — delete the repository or leave it
   unpinned; openxFactory is untouched.
3. **P2b — `wallet-v1.1`.** The nested-repository prune and the register-read
   note: two additive-minor changes, one auditable diff. *Rollback:* openxFactory
   pins `wallet-v1.0` and P3 is blocked until the prune lands, because the sweep
   hazard sits inside a REQUIRED check.
4. **P2.5 — the openxFactory deprecating minor.** Eight `relocating:` fields, the
   CHANGELOG note, its own digests file, its tag. *Rollback:* a published bundle
   is not unpublished — the honest reversal is a FOLLOWING minor that removes the
   marker, never a revert of the cut.
5. **P5a.2 — LedgerxFactory `stack.yaml` bump to the P2.5 minor**, plus the
   pinned-checker invocation that makes the relocation warning observed.
   *Rollback:* revert to `39539fd4…`.
6. **P3 + P3b + P4, one wave.** P3 is one atomic pull request — the trust-anchor
   guard at `:2581-2585` leaves no green intermediate. *Rollback:* `git revert` P3
   restores every path (the carve copied and deleted nothing) and removes the pin
   file and the gitlink; `wallet-validation.yml` returns as a filename. **Ruleset
   21538893 is unchanged throughout, so there is nothing to roll back there.** P4
   reverts WITH P3 or the aggregation pins a product openxFactory does not; P3b
   reverts only with P3, since reverting it alone re-opens the floor gap.
7. **P5b — post-move repoints and the declared wallet pin.** *Rollback:* coupled
   to P3's; dropping the fallback is safe only while the gitlink exists.
8. **P4b — root-level governed-repo recognition.** *Rollback:* revert; the books
   are derived and a removed repository id simply stops deriving.
9. **P6 — `LedgerxWallet`** via `create-ledgerxwallet-overlay-boundary`.
10. **P7 — close.** Archive on realization evidence; DTN-026 → `implemented`;
    NotebookLM sync `--apply`.

Splitting the proposal's P5a into 5a.1 and 5a.2 is forced arithmetic, not a
revision: one pull request cannot both precede P2 and pin a bundle P2.5 has not
cut. Both of the proposal's constraints — forward-compatible finder before P3,
consumer observing the marker before the major — are satisfied by the split and
by nothing else.

## Open questions

- **Q1 — register as a wallet primitive, or the reader split back?** NOT decided
  here; it travels, as the proposal expects. Both resolutions move a gated path or
  change code, converting a byte-identical extraction into a design change, and
  the pin already makes "which reader ran" an auditable digest — the property the
  reader-split would pay a refactor to obtain. Revisit when a second consumer of
  authority registers exists.
- **Q2 — do `tenants/ledgerxcorp/wallets/*` move?** Stays for
  `create-ledgerxwallet-overlay-boundary` (P6); the profile/instance line is the
  owning domain's call.
- **Q3 — the `xfactory_wallet_*` → `openxwallet_*` window.** Stays for the
  openXwallet successor. This design adds only the price: the prefix sits in
  `pinned_by_commit_only` bytes, so the rename is a wallet MAJOR, an openxFactory
  pin bump and a LedgerxFactory re-pin — the three steps
  `docs/pin-resync-runbook.md` exists for.
- **Q4 — `openXwallet-Install`.** DECIDED as far as design reaches: the NAME is
  registered in Amendment 2 and no repository is created, on rule (d) applied to
  an install repo. Whether Hermes is the issuer host stays with hermes-install's
  roadmap and is a precondition of nothing in this wave.
- **Q5 — the bundle-tag scheme.** DECIDED: `wallet-vN.M`, major on a breaking key
  or schema change, minor on additive growth, and NO range expression in the pin —
  commit and sha256 are authoritative and the tag is a label beside them
  (`revision_kind: commit`, D1). D4 is the first application: `wallet-v1.1` is
  additive growth, and openxFactory pins it by commit while recording the tag.
