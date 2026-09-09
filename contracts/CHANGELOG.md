# openxFactory Contract Changelog

Status: draft

Governed by [Contract Versioning Policy](../docs/contract-versioning-policy.md).

Legacy baseline note: versions `contract-v1.1` through `contract-v1.6`
predate mandatory annotated tags and carry none. Tag enforcement begins at
`contract-v1.7` — the first realized release published with an annotated tag —
without fabricating historical tags.

## contract-v3.6 — 2026-09-09 (additive; the consent instrument gains a re-derivable custody record — `contract_schema_version` 2 → 3 for ONE closed optional array — RE-CUT at the next minor after a sibling lane took `contract-v3.5`)

Cut under § 5 of the RATIFIED change
[`add-consent-custody-rederivation-record`](../openspec/changes/add-consent-custody-rederivation-record/proposal.md)
(ratified 2026-09-08 by Brett Heap, reviewer of record, verbatim *"ratify 774,
merge it and land it"*; the ratification PR is **#774**, merged by him at
2026-09-08T03:48:44Z as `543d47a9`), realized by lane `opsXfactory-1` under
issue **#630** row-4 realization claim
[`5602971301`](https://github.com/opensoft/openxFactory/issues/630#issuecomment-5602971301).
**The version number is claimed on row 4 AT CUT TIME and not before**, which is
row 4's own rule (*"Claim the version number, not the files"*) and
[`docs/contract-versioning-policy.md`](../docs/contract-versioning-policy.md)
§ *Bundle Realization Order* step 1: the claim for THIS number is
[`5609660878`](https://github.com/opensoft/openxFactory/issues/630#issuecomment-5609660878),
posted 2026-09-09T22:34:39Z at the integration point below.

**THE WHOLE RELEASE SURFACE MOVES IN ONE CANDIDATE COMMIT OVER ONE INTEGRATION
POINT**, per § *Bundle Realization Order* step 2. The integration point is the
merge commit `fee36588` — `origin/main` at **`17167481`** merged INTO the
cutting branch, never a rebase, because opensoft org ruleset **8981805** forbids
non-fast-forward updates and a candidate therefore only ever advances forward.
The candidate is its own DECLARING commit and the branch tip, so the release-tag
gate's first-parent declaring distance is **zero**.

### Why this bundle is `contract-v3.6` and not `contract-v3.5`

Two lanes held cut candidates for the same number on 2026-09-09. Lane
`provenance-autonomous-merge` cut `contract-v3.5` for
`adopt-codexfactory-repository-identity` (**#866**), and the repository owner
ORDERED the sequence. Brett Heap, 2026-09-09T22:11Z, selected option verbatim:

> *"#866 first, I re-cut as v3.6 (Recommended)"*

**#866 landed on `main` as `a37ae0cd` at 21:47:48Z and Brett Heap published the
annotated tag `contract-v3.5` (`6c602f3c` → `a37ae0cd`).** That number is
therefore SPENT by another bundle, this lane's `contract-v3.5` claim was
RELEASED on the ordering ruling's own record (issue #630 comments
[`5609050869`](https://github.com/opensoft/openxFactory/issues/630#issuecomment-5609050869)
and
[`5609442856`](https://github.com/opensoft/openxFactory/issues/630#issuecomment-5609442856)),
and this cut is re-taken at the next free minor.

**THE TWO EARLIER CANDIDATES DECLARED `contract-v3.5`, WERE NEVER PUBLISHED, AND
ARE WITHDRAWN.** `d54d89ca` (the first cut) and `e9a688d3` (its forward-only
remake) carried a `## contract-v3.5` entry that never reached `main` and never
reached a tag; both are superseded by this entry, and a later audit found THREE
defects in the remake, each recorded here rather than left to the branch's
history: **(a)** `scripts/validate-release-tag-gate.py` exited **2, REFUSED**
over that tree — *"contract-v3.5 is declared and has no published annotated tag
more than 5 first-parent landings after the commit that declared it — under the
versioning policy it is NOT PUBLISHED, and its presence in the manifest is not a
release"* — because the DECLARING commit was `d54d89ca`, by then six to seven
first-parent landings back, and the readings that had called the gate green were
misreads of a transcript whose header looks clean and whose exit code sits at
the tail; **(b)** its § *What moved OUTSIDE `contracts/`* claimed *"Two inventory
members live outside `contracts/`"* when FOUR had moved, leaving
`docs/terminology-and-repo-topology.md` and `docs/xfactory-domain-factory-model.md`
(both moved by `44fc8063`) unattributed; **(c)** it carried only
`contracts/CHANGELOG.md` and the rebuilt inventory while `contracts/manifest.yaml`,
`contracts/README.md` and the cut-coupled tripwire stayed behind at `d54d89ca`,
which is not the ONE atomic candidate that § *Bundle Realization Order* step 2
and this packet's **FR-034a** require. **All three are moot at this candidate
rather than argued away**: the declaring distance is zero, the attribution below
is taken from an inventory diff over all 283 members, and every release surface
moves in this one commit.

### What forced the cut, and what moved: the INVENTORY DIFF over all 283 members

**Counted from the DIGEST INVENTORY, not from `git diff -- contracts/`.** A cut's
subject is the release inventory's 283 members wherever they live, and a diff
scoped to `contracts/` cannot see the 91 members that do not. Measured with
[`releases/contract-v3.5.digests.yaml`](releases/contract-v3.5.digests.yaml)
against this candidate's own bytes: **283 entries at both ends, ZERO added, ZERO
removed, no `git_mode` and no non-digest field changed, and FOUR digests
re-baselined.** Every one of the four, by exact path, with what moved it:

| member | `contract-v3.5` digest | `contract-v3.6` digest | moved by |
| --- | --- | --- | --- |
| `contracts/manifest.yaml` | `sha256:93564e191379…` | *(this candidate)* | `f59a587d` — § 2's own commit, which re-derived the `consent-instrument` row's `sha256` `13b0fe46…` → `2b834492…` in the same act that moved the schema, so no commit on this branch was ever left carrying a stale digest; `fee36588` — the merge, which re-applied that ONE key onto `main`'s manifest; and **THIS CUT** (the `contract_bundle_version` line, the row's new `contract-v3.6` `consumption_rule` paragraph, and the family comment's re-measured corpus counts) |
| `contracts/README.md` | `sha256:f3a959fa223d…` | *(this candidate)* | `f420cd50` — §§ 3–4, the validator-and-corpus row rewritten for THREE buckets; `d54d89ca` — the consent-schema row's amendment sentence, authored at the withdrawn candidate and carried forward on this branch; and **THIS CUT** (both rows respelled `contract-v3.5` → `contract-v3.6`) |
| `contracts/CHANGELOG.md` | `sha256:a2b65ff30b9c…` | *(this candidate)* | **THIS CUT** — this entry |
| `tests/intent-compliance/test_release_boundary.py` | `sha256:a235e1c55947…` | *(this candidate)* | **THIS CUT** — the cut-coupled tripwire |

The three `contract-v3.6` columns above read *(this candidate)* rather than a
literal digest for the reason `contract-v3.4`'s entry gives when it names its own
self-referential members as *"THIS CUT — this entry and the rebuilt inventory"*:
this file is itself an inventory member, so its digest is fixed only by the build
that runs AFTER this sentence is final, and quoting a value here would be quoting
a byte this text had not yet produced. The authoritative values are in
[`releases/contract-v3.6.digests.yaml`](releases/contract-v3.6.digests.yaml),
which is built by the tool from the candidate's own bytes and never hand-edited.

**ONE OF THE FOUR LIVES OUTSIDE `contracts/`, AND IT IS NAMED RATHER THAN LEFT TO
THE DIFF**: `tests/intent-compliance/test_release_boundary.py`, this cut's own
tripwire. Ninety-one inventory members live outside `contracts/` in total — the
three `NORMATIVE_DOCS`, the two hash-locked `requirements/` files, the PostgreSQL
image lock, the four `NAMED_VALIDATORS`, the `scripts/hermes_runtime_validation/`
and `scripts/intent_compliance/` implementation and the
`tests/intent-compliance/` suite — and **ninety of them are byte-unchanged
between `contract-v3.5` and this candidate**, measured by exact path. In
particular all three normative documents
(`docs/contract-versioning-policy.md`, `docs/terminology-and-repo-topology.md`,
`docs/xfactory-domain-factory-model.md`) were re-baselined by `contract-v3.5`
itself and move nothing here — which is the direct repair of defect **(b)**
above.

`tests/intent-compliance/test_release_boundary.py` moves because
`_release_state()` FAILS LOUDLY on a bundle its enum does not name, so a
`contract_bundle_version` that advanced without it would red the required suite.
Three edits, the pattern `contract-v3.4` and `contract-v3.5` both used:
`FEATURE_SUCCESSOR_10 = "contract-v3.6"`, the member added to **BOTH** match arms
(there are two, and missing either hits `assert_never`), and the hand-written
boundary paragraph that every cut past the intent-compliance floor owes. That
paragraph's claim is MEASURED: `git diff --name-status contract-v3.5 <candidate>`
over `contracts/intent-compliance/`, `scripts/intent_compliance/`,
`tests/intent-compliance/` and `scripts/validate-intent-compliance.py` reports
exactly ONE path — that file, for this advance and nothing else — so no other
member of the family moved a byte between the two cuts and the membership the
file asserts is again UNCHANGED.

`tests/clearing/test_clearing_manifest_rows.py` takes **NO EDIT**, and that is a
measurement too rather than an assumption: run at the candidate it passes, and
its only failure before the build was the ABSENT inventory, which `build` then
created. `807a4f47` engineered exactly that outcome when it repaired the file's
bundle-version equality instead of re-pinning a number that would fail again at
the next cut.

### The substance is ONE SCHEMA; every other moved member is cut bookkeeping

**`contracts/schemas/consent-instrument.schema.yaml`** (`f59a587d`) grows ONE
closed optional top-level array, `custody_rederivations[]`, a **SIBLING of
`custody` rather than a member of it**, and its `contract_schema_version` moves
**2 → 3**. Each entry is closed at TEN REQUIRED FIELDS — `at`, `commit`,
`previous_locator`, `observed_locator`, `previous_sha256`, `observed_sha256`,
`diff_class`, `reason`, `ruling_ref`, `recorded_by` — under TWO CLOSED
ENUMERATIONS: `diff_class` `[path_only, header_only, content]` and `reason`
`[lifecycle_header_edit, archive_move, other_ruled_edit]`. It makes an
AUTHORIZED act that moves a pinned custody target's bytes or its path
RECORDABLE, so a custody pin that no longer resolves can be RE-DERIVED from the
record rather than rewritten to match whatever it now finds.

**That schema is a registered manifest row and NOT a release-inventory member**,
so it moves no digest of its own here — membership is closed over the surface
[`scripts/hermes_runtime_validation/release.py`](../scripts/hermes_runtime_validation/release.py)
enumerates, and `contracts/schemas/` is not in it. Its identity travels by the
manifest row's per-file `sha256`, verified by
`scripts/validate-manifest-digests.py` (189 rows, green at this candidate). The
divergence between that membership surface and the policy's *"every modified
normative contract"* is PRE-EXISTING — it held at every earlier bundle that
carried this schema — and is **NOT repaired here**, because hand-adding a row to
a BUILT inventory is precisely the edit the policy forbids; it is recorded as an
owed finding beside the packet's § 7.

The bundle also carries, since `contract-v3.5`, the change's other realization
bytes, none of which is an inventory member:
`scripts/validate-consent-instruments.py` (`f420cd50`) with the chain's internal
legs and the third outcome; EIGHTEEN new fixtures under
`examples/consent-instrument/` (`f420cd50`), including the new `withheld/`
bucket; and the new `tests/consent_instruments/` package (`f420cd50`, hardened
by `0cbd022a`'s refutation-panel finding R7).

### Change class: ADDITIVE (minor), argued over the WHOLE bundle

The additions are additive by construction — a member that did not exist cannot
have narrowed. Each MODIFICATION is checked individually, because "the bundle is
additive" is a claim about every row in it:

* **The consent schema is the ONLY `*.schema.yaml` this bundle moves** —
  measured, not assumed: `git diff --name-status contract-v3.5 <candidate> --
  contracts/` returns five paths and exactly one ends in `.schema.yaml`. Its
  growth adds one OPTIONAL top-level property. Nothing is removed, no
  enumeration is narrowed, no existing property becomes required, and the RECORD
  envelope's `schema_version` stays `const: 1` for the same reason it did at
  `contract-v1.33`. Every instrument already in the estate validates unchanged
  and none declares the new array — proven by the packaged corpus, where all six
  pre-existing valid examples are byte-unedited and still pass.
* **`contracts/manifest.yaml` and `contracts/README.md` are EDITORIAL members** —
  rows, digests and prose, carrying no consumer-visible shape, and moved by every
  cut. So are this entry and the built inventory, this cut's own two.
* **`tests/intent-compliance/test_release_boundary.py` is a TRIPWIRE**, not a
  contract: it names the bundle so that a version bump cannot pass unnoticed.

**NOTHING IN THIS BUNDLE IS BREAKING, AND NOTHING IS DEPRECATED.** There is no
command-line migration and no shape work.

### The bundle number, FRESH-COUNTED at the candidate

Measured at the integration point rather than trusted, and re-measured after
`contract-v3.5` landed and was tagged:

- [`manifest.yaml`](manifest.yaml) declared `contract_bundle_version:
  contract-v3.5` before this edit.
- [`releases/`](releases/) held inventories through
  [`contract-v3.5.digests.yaml`](releases/contract-v3.5.digests.yaml); there was
  no `contract-v3.6.digests.yaml`.
- `git ls-remote --tags origin 'contract-v*'` publishes annotated tags through
  `contract-v3.5`, and `refs/tags/contract-v3.6` is ABSENT — so no earlier
  bundle owes a tag, and this number is not a reuse.
- There is no `Unreleased` block pending in this file.

`contract-v3.6` is taken HERE and was reserved nowhere: the packet's own task
5.1 measures the number and says in terms that the CLAIM is the lane's act at
cut time, which is § *Version Identity*'s rule that a proposed change MUST NOT
reserve a minor before merge order is known. **The measurement recorded in that
task's text — `contract-v3.4` on all three surfaces — is stale by two bundles and
is superseded by this section**, which is exactly why the rule says re-measure.

### What this bundle does NOT do

The consent family's re-derivation rule is DECLARED here and ENFORCED nowhere.
The neutral validator published with this bundle takes only the legs derivable
from a record's own bytes — anchor and linkage in both digest and locator,
declared order, the unrewritten pin, `path_only` digest equality, closed
enumerations and entry closure — and a pass by it is **NOT a currency claim**. A
`content`-class divergence yields a THIRD OUTCOME, `WITHHELD`, and exit `3`,
"needs a human decision", rather than a pass. The GIT re-derivation legs, the
declared custody-store mapping that resolves an OPAQUE locator, and the operated
custody-digest check are the CONSUMING repository's; no consumer file is written
by this release, no consumer pin advances, and **no custody pin is repaired by
this bundle**.

### `contract-v3.5` remains valid provenance

Its tag and [its inventory](releases/contract-v3.5.digests.yaml) are untouched by
this cut and stay exactly as published. A consumer pinned at `contract-v3.5`
remains conformant without changes, that number is never reused, and this bundle
supersedes nothing and declares nothing spent.

### Migration guidance

* **A consumer pinned at `contract-v3.5` re-pins to `contract-v3.6`** by moving
  `xfactory.contract_ref` to this bundle's published commit, recording the tag,
  and re-running the per-file digest checks under § *Domain Upgrade Runbook*.
  **There is no shape work**: nothing here refuses a record `contract-v3.5`
  accepted.
* **A consumer that intends to WRITE a custody re-derivation reads THIS bundle.**
  The ten fields are all required together, the two enumerations are closed, and
  an entry whose locators or digests do not chain to the one before it is
  refused.
* **A consumer must not read a neutral pass as a currency claim.** The GIT legs
  and the custody-store mapping are the consuming repository's own, and the
  neutral validator says so by withholding rather than by passing.

### The annotated tag is published at the LANDED commit, not from this branch

§ *Bundle Realization Order* step 4: *"Land the exact reviewed commit on
published `main`. If promotion creates a different commit, that commit becomes
the new candidate and every gate and review reruns before tagging."* Step 5 then
publishes the tag at that exact published commit. **SKIPPING THE RE-VERIFICATION
AT STEP 4 IS WHAT MADE `contract-v3.1` DEFECTIVE** — a squash merge ALWAYS
creates a different commit. Box 5.6 is an **[OPERATOR]** act at the landed merge
commit and is NOT performed by this cutting session; `TAG OWED` is the expected
state at this candidate, not a finding.

## contract-v3.5 — 2026-09-09 (additive; the eight inventoried members are re-issued under `codeXfactory/codexFactory`, so the release surface stops describing a repository identity that no longer resolves)

Cut as task **7.2–7.3** of the RATIFIED change
[`adopt-codexfactory-repository-identity`](../openspec/changes/adopt-codexfactory-repository-identity/proposal.md),
whose realization moved `opensoft/codexFactory` to `codeXfactory/codexFactory`
across this repository's governed content. **The cut is owed, not elective**, and
its own § 5 (*Version treatment, derived rather than assumed*) says by which
rule: eight members of the declared `contract-v3.4` digest inventory changed
bytes, and
[`docs/contract-versioning-policy.md`](../docs/contract-versioning-policy.md)
§ *What a red `verify-commit` at HEAD means* calls a mismatch on a non-editorial
member *"a defect: a normative contract's bytes moved while the repository went
on declaring a bundle that describes different bytes"*, whose *"remedy is a
release cut, never a hand-edit"*. No inventory row and no
`contract_bundle_version` was adjusted to make a comparison pass; the inventory
below is built by the tool from the candidate's own bytes.

**THE WHOLE RELEASE SURFACE IS DERIVED IN ONE ACT OVER ONE INTEGRATION POINT**,
per § *Bundle Realization Order* step 2. The integration point is `origin/main`
at `95e67ab0` — the merge of PR **#806**, the LAST of the change's four gated
realization slices, committed 2026-09-09T20:44:00Z. **The candidate was first
derived at `00d368a4` (#805, 20:00:16Z) and then RE-DERIVED here when `main`
moved**, per step 1's *"fetch and rebase onto the final integration point, then
immediately recheck bundle/tag availability"*; availability was re-checked at
this tip rather than carried forward from the first derivation. See § *The
bundle number, FRESH-COUNTED at the candidate* below. Re-measured across the
move: neither #806 nor #864, the two pull requests that landed in between,
touches a single release-inventory member — checked by exact path against the
inventory's 283 entries — so the re-derivation moved no digest that the first
derivation had not already moved.

### What forced the cut: the eight inventoried members, old digest → new digest

Measured with `validate-contract-release.py verify-commit --commit 00d368a4`,
which reported exactly ten `HGR-RELEASE-DIGEST-MISMATCH` findings — these eight
plus the two editorial members § *What a red `verify-commit` at HEAD means*
allows between cuts (`contracts/manifest.yaml`, `contracts/README.md`).

| member | `contract-v3.4` digest | `contract-v3.5` digest |
| --- | --- | --- |
| `contracts/hermes-runtime/README.md` | `sha256:c14f1d6d4f38…` | `sha256:376f970ec9bc…` |
| `contracts/hermes-runtime/fixtures/domain-regression-inventory.yaml` | `sha256:5d5d9815c7cb…` | `sha256:33e5e8fad6e0…` |
| `contracts/hermes-runtime/fixtures/regression/digest-mismatch.yaml` | `sha256:26df927b6647…` | `sha256:3b442833740f…` |
| `contracts/hermes-runtime/fixtures/regression/duplicate-repository.yaml` | `sha256:03bcfb439bad…` | `sha256:8df7ab81f947…` |
| `contracts/hermes-runtime/fixtures/regression/missing-exclusion-reason.yaml` | `sha256:7587549d7fca…` | `sha256:3b31231a6eee…` |
| `docs/contract-versioning-policy.md` | `sha256:9c5cf8989234…` | `sha256:d4b9402c5916…` |
| `docs/terminology-and-repo-topology.md` | `sha256:56d7e3c0da4b…` | `sha256:07a337f76cb0…` |
| `docs/xfactory-domain-factory-model.md` | `sha256:91b7f9914643…` | `sha256:fba5ac5f1e2f…` |

**THE SUBSTANCE IS ONE OWNER SEGMENT AND NOTHING ELSE.** The supported-domain
regression denominator
([`contracts/hermes-runtime/fixtures/domain-regression-inventory.yaml`](hermes-runtime/fixtures/domain-regression-inventory.yaml))
now keys its codex row on `codeXfactory/codexFactory`; the row's `commit`
(`7bfa492f`), `stack_path`, `stack_digest`, `domain_id`, `expected_contract_ref`
and `expected_result` are byte-unchanged, and the row moved to the head of the
list only because entries are held in bytewise repository order. Its three
negative fixtures and the family README's denominator paragraph follow the same
one-segment rule. The three normative documents restate the denominator's
membership in prose. **A transfer moves the OWNER SEGMENT ONLY** — bare names,
commits, repository-relative paths and blob digests are untouched — which is
`repository-identity.yaml`'s `owner_segment_rule`, and it is why this is an
additive cut and not a compatibility event.

**The root `README.md` is NOT a member and owes nothing here**, although a
substring search says otherwise: the inventory carries `contracts/README.md` and
`contracts/hermes-runtime/README.md`, and matching `README.md` as a substring
finds both. Membership was re-measured by EXACT path; the count is eight, not
nine.

### The mapping row is the resolver, and this is the bundle that publishes it

[`contracts/policies/repository-identity.yaml`](policies/repository-identity.yaml)
is NEW in this bundle and registered in
[`manifest.yaml`](manifest.yaml) as `id: repository-identity`. It carries the
`opensoft/codexFactory → codeXfactory/codexFactory` row with
`transfer_state: complete`, and the estate resolves a FORMER repository identity
**through that file, by lookup, and never through a provider redirect** — a
redirect lapses the moment the former owner reuses the name. The row also
records the derived, tool-imposed GHCR lowercasing (`codexfactory`) as a
spelling and not a second identity, per OQ-6 (ruled 2026-09-08T03:51Z: canonical
`codeXfactory/codexFactory`).

**NOTHING IMMUTABLE WAS RESPELLED TO MATCH THE ROW.** Archived OpenSpec packets,
dated verification tables, and signature- or digest-covered artifacts stay
verbatim: in particular the 34 files under
`contracts/signed-execution-chain/examples/`, whose `ground_ref` sits inside a
signature the fixture key cannot re-issue, are byte-unchanged in this bundle and
`scripts/validate-signed-execution-chain.py` is the check that proves it.

### The origin identity is re-issued in this bundle's tree

`governance/factory-identity/` is not a release-inventory member, so it moves no
digest here, but the re-issuance is part of the same act and this entry names it
so that a reader of the tag can find it: PR **#802** (`20298c64`) re-issued
`grant-origin-codexfactory-0001` and `wal-origin-codexfactory-0001` against the
new repository identity, re-pointed `register.yaml`, and updated
`governance/review-authority/grants/grant-grc-0001.yaml`. **Until that
re-issuance is live, codexFactory clearing dispatches are REFUSED** — that is
the transfer revoking the origin identity, working as designed rather than
failing.

### `--domain-repo` KEY MIGRATION — the one command-line break in this release

The domain-regression denominator is resolved by exact `commit:path` Git objects
through deterministic mappings, and **the mapping key is the inventoried
repository identity**. So every release-time and CI invocation of
`scripts/validate-hermes-runtime-contracts.py` that named the codex checkout by
hand must change its key:

```sh
# contract-v3.4 and earlier
--domain-repo opensoft/codexFactory=/path/to/codexFactory
# contract-v3.5 onward
--domain-repo codeXfactory/codexFactory=/path/to/codexFactory
```

`--domain-repo-root <root>` callers resolve the same rename by directory: the
checkout must be reachable at `<root>/codeXfactory/codexFactory` or
`<root>/codeXfactory/codexFactory.git`. **A stale key is a dependency failure,
never a skip** — the validator refuses a missing object rather than passing the
denominator with one supported consumer silently unmeasured, which is the whole
reason the denominator is versioned.

### Also carried into this cut, MEASURED rather than intended

A bundle is a commit's whole tree, not a session's intention. Measured with
`git diff --name-status contract-v3.4 HEAD -- contracts/`: **four additions and
twenty-seven modifications**, every path attributed.

**Four additions.** `contracts/policies/repository-identity.yaml` (above; #799 /
#815, registered in the manifest). `contracts/openspec-cli-pin.yaml` and
`contracts/openspec-cli-pin.1.12.0.package-lock.json` — the OpenSpec CLI
consumption pin and its vendored dependency closure, published as a contract
member by `publish-openspec-cli-pin-as-contract-member` (#754, #757, #780) with
the pin's own registration row and no `sha256` for the stated reason that the
pin legitimately moves on three distinct events.
`contracts/review-lane-repin-binding.template.yaml` — the re-pin lane's
operator-facing binding template (#715, #726, #801), whose
`identity_namespace` reads `github:codeXfactory` by the convener's ruling of
2026-09-09 rather than being left at `github:opensoft`.

**Twenty-seven modifications, in four groups.** (1) The eight inventoried
members above, plus `contracts/manifest.yaml` (two new registration rows and
this cut's version line) and `contracts/README.md` (the contract-index rows for
the pin, its lockfile and the mapping row) — both editorial. (2) Sixteen
identity respells that are NOT inventory members and therefore drift nothing:
eight `contracts/clearing/examples/**` files and
`contracts/hermes-domain-overlay/examples/**` ×2 plus
`contracts/omnigent/examples/**` ×6 (#799 `edbc2621`, #802). (3) Three
consumption pins advanced by their own gates: `openreposhape-pin.yaml` to
`e9c4827b` (#700), `openxwallet-pin.yaml` to `wallet-v1.5` / `f3eb929b` (#740,
eight digests reverified unchanged). (4) `review-lane-pin.yaml` and
`review-lane-floor-snapshot.yaml`, the decision-core re-pins of #686, #689,
#702, #732, #747, #764 and #801 — **NOT this cut's act**, recorded here only
because the bundle contains them.

### Change class: ADDITIVE (minor), measured

No required field is added, no shape is removed, no `contract_schema_version`
moves, and no role or vocabulary SEMANTICS change. Every edit to a published
member replaces one owner segment with another inside a value that was already a
free-form repository string. Nothing this bundle carries refuses a record
`contract-v3.4` accepted, with the single exception named above, which is a
COMMAND-LINE key and not a record shape.

### The bundle number, FRESH-COUNTED at the candidate

Measured at the integration point rather than trusted:

- [`manifest.yaml`](manifest.yaml) declared `contract_bundle_version:
  contract-v3.4` before this edit.
- [`releases/`](releases/) held inventories through
  [`contract-v3.4.digests.yaml`](releases/contract-v3.4.digests.yaml); there was
  no `contract-v3.5.digests.yaml`.
- `git ls-remote --tags origin 'refs/tags/contract-v*'` publishes annotated tags
  through `contract-v3.4` (`807a4f47`), and
  `refs/tags/contract-v3.5` is ABSENT — so no earlier bundle owes a tag, and
  this number is not a reuse.
- There is no `Unreleased` block pending in this file.

`contract-v3.5` is taken HERE and was reserved nowhere. The change's own task
7.2 says so in terms — *"no number is reserved by this packet, and this packet
has a live ordering dependency besides"* — which is § *Version Identity*'s rule
that a proposed change MUST NOT reserve a minor before merge order is known.

### Inventory: 283 members, membership UNCHANGED, twelve re-baselined

[`releases/contract-v3.5.digests.yaml`](releases/contract-v3.5.digests.yaml) is
built LAST by `validate-contract-release.py build --tag contract-v3.5` from the
candidate's own bytes and is never hand-edited. Measured against
`contract-v3.4`'s 283 entries: **no member added, none removed, no `git_mode`
changed**, and TWELVE digests re-baselined — the eight above; the three
editorial members (`contracts/manifest.yaml`, `contracts/README.md`, and this
file); and `tests/intent-compliance/test_release_boundary.py`, which is a
release member and carries the by-hand boundary statement every cut past the
intent-compliance floor is required to write. That statement is the twelfth
mover and is what it says: `FEATURE_SUCCESSOR_9 = "contract-v3.5"` is added to
the enum and to both match arms, and the docstring records the MEASUREMENT that
this cut moves NO intent-compliance member — `git diff --name-status
contract-v3.4 HEAD` over `contracts/intent-compliance/`,
`scripts/intent_compliance/`, `tests/intent-compliance/` and
`scripts/validate-intent-compliance.py` reports ZERO paths. The library floor is
an at-or-after comparison and would not have noticed the bump on its own, which
is why the statement is a hand act and not an inference.

None of the four newly added `contracts/` paths is a release-inventory member:
membership is closed over the surface
`scripts/hermes_runtime_validation/release.py` enumerates, and a manifest
registration row does not by itself confer it.

`contract-v3.4`'s tag and inventory are untouched and remain valid provenance.

### The cut lands after ALL FOUR realization slices, and the recorded disagreement is moot

The change realized in four gated slices, sequenced by the ceremony merge order
that the lane added to the operator runbook
(`~/session-prompts/runbook-codexfactory-org-transfer.md` § *Ceremony merge
order*, outside this repository) over the packet's
[`tasks.md`](../openspec/changes/adopt-codexfactory-repository-identity/tasks.md)
§ 7: #801 (machine surfaces, `e86eca35`), #802 (origin identity, `20298c64`, a
HUMAN merge word), #805 (the eight inventoried members, `00d368a4`) and #806
(prose and README, `95e67ab0`).

**That order put the cut at row 5 and #806 at row 6, and one recorded
disagreement said the cut belonged after all four**, on the letter of tasks 7.1
and 6.5. #806 landed at 20:44:00Z, forty-four minutes after #805 and BEFORE this
candidate was re-derived — **so the cut is after all four and the disagreement
is settled by events rather than by argument**. It is also settled on the
measurement either reading needed: not one of #806's sixteen files is a member
of the `contract-v3.4` inventory, checked by exact path against its 283 entries,
so neither this cut's inputs nor task 7.1's condition could have changed across
it in either order.

### Migration guidance

* **A consumer pinned at `contract-v3.4` re-pins to `contract-v3.5`** by moving
  `xfactory.contract_ref` to this bundle's published commit, recording the tag,
  and re-running the per-file digest checks under § *Domain Upgrade Runbook*.
  **There is no shape work.**
* **A consumer that names the codex repository on a command line or in CI
  changes the key**, per § *`--domain-repo` KEY MIGRATION* above. This is the
  only break in the release.
* **A consumer that resolves a FORMER identity reads
  `contracts/policies/repository-identity.yaml`**, never a provider redirect,
  and NEVER respells an immutable or dated record to match a row.
* **A codexFactory clearing producer re-reads the origin register.** A sealed
  request whose `origin.repository` still names `opensoft/codexFactory` is
  refused by `scripts/validate-clearing-dispatch.py` against the re-issued
  register, and that refusal is correct.

### The annotated tag is published at the LANDED commit, not from this branch

§ *Bundle Realization Order* step 4: *"Land the exact reviewed commit on
published `main`. If promotion creates a different commit, that commit becomes
the new candidate and every gate and review reruns before tagging."* Step 5 then
publishes the tag at that exact published commit. **SKIPPING THE
RE-VERIFICATION AT STEP 4 IS WHAT MADE `contract-v3.1` DEFECTIVE** — a squash
merge ALWAYS creates a different commit.

**Task 7.4 IS AN OPERATOR ACT AND IS NOT PERFORMED BY THE CUTTING LANE.**
`verify-promotion` and the annotated tag are RELEASE SURFACES; the ceremony
runbook's own legend does not cover them and assigns them to the operator. The
exact sequence, run from a freshly refreshed openxFactory checkout AFTER this
cut lands on `main`:

```sh
git -C <openxFactory> fetch origin --tags
LANDED="$(git -C <openxFactory> rev-parse origin/main)"   # the landed merge/squash sha of this cut

# 1. re-verify the inventory at the LANDED commit (step 4)
python3 scripts/validate-contract-release.py verify-commit --commit "$LANDED"

# 2. prove the tag is absent, the version is next, the candidate is reachable
#    from remote main, and no release-surface blob drifted (step 5 precondition)
python3 scripts/validate-contract-release.py verify-promotion \
    --commit "$LANDED" --remote origin --tag contract-v3.5

# 3. publish the annotated tag at that exact commit
git -C <openxFactory> tag -a contract-v3.5 -m contract-v3.5 "$LANDED"
git -C <openxFactory> push origin contract-v3.5

# 4. verify the published tag from an INDEPENDENTLY refreshed checkout
python3 scripts/validate-contract-release.py verify-tag --remote origin --tag contract-v3.5
```

The tag message is the tag name and nothing else, matching `contract-v3.3` and
`contract-v3.4`. **If step 1 or step 2 reports a finding, STOP and do not
tag**: the landed commit is then a new candidate, and every gate and review
reruns before step 3.

## contract-v3.4 — 2026-09-04 (additive; the chain-anchoring family reaches its first bundle WITH the ratified readiness-and-durability amendment already realized in it, `deliberation` becomes clearing register entry two, and the openRepoShape consumption pin advances to `122d729b`)

Cut on the repository owner's word — Brett Heap, 2026-09-04, in session, lane
repo-shape, verbatim: *"cut contract-v3.4"* — and cut a second time, at a later
tip, on the owner's RULING of 2026-09-04T14:50Z that HELD the first candidate
until one named change had landed. **The whole release surface is derived in ONE
act over ONE integration point**, per
[`docs/contract-versioning-policy.md`](../docs/contract-versioning-policy.md)
§ *Bundle Realization Order* step 2, at the final integration point required by
step 1 and RE-MEASURED there rather than re-asserted. The integration is a MERGE
of `main` into the cutting branch rather than a rebase of the branch: opensoft
org ruleset **8981805** forbids non-fast-forward updates on every branch, so a
held candidate can only be advanced by integrating forward. The resulting tree is
byte-identical to the rebase that ruleset refuses, and step 4 re-verifies at the
landed commit in either case.

**THE CUT WAS ORDERED FOR THE PIN AND MEASURED TO CARRY FAR MORE, AND THE
MEASUREMENT GOVERNS.** The bump that occasioned it is
`contracts/openreposhape-pin.yaml`'s advance (PR **#650**, squash
`48dc9b67c87377cdad31d2840666c7028a212cf7`, issue **#649**). But a bundle is a
commit's whole tree, not a session's intention, and `contract-v3.3` peels to
`16b85614` — a commit that PREDATES `add-chain-anchoring`'s realization
(`11feff75`, PR **#629**) by twenty minutes. So an entire neutral contract
family, its amendment's realization and a second clearing register entry are
inside this bundle whether or not the cutting session went looking for them, and
this entry names them first for that reason. § *Version Identity* requires one
entry per release *"listing every contract added, changed, or deprecated"*; an
entry naming only the pin would have been a false record of what the tag points
at.

### The ordering constraint the owner set, and how this bundle satisfies it

`amend-chain-anchoring-readiness-and-durability` was **ratified 2026-09-04** by
Brett Heap (repository owner) — requirements 2 and 3 as written, requirement 1
withdrawn — and merged as PR **#548** (`471d3361`). The owner queued its
realization in the same breath, verbatim:

> *"Queued as the realization cost, ahead of the next contract cut … must land
> BEFORE those schemas ship in a tagged bundle, or the enum change becomes a
> breaking change on a published bundle."*

**THAT REALIZATION HAS LANDED, AND IT LANDED FIRST.** PR **#657**
(`e65dcc48`, lane `openxfactory-1d`) merged to `main` at 2026-09-04T18:25:33Z,
realizing requirements 2 and 3 against the schemas `add-chain-anchoring` had
landed. The first candidate for this cut (`422474eb`, 14:06Z) was HELD on the
owner's ruling precisely so that this ordering would hold — *"this PR stays open
and unmerged; `contract-v3.4` is cut only after
`amend-chain-anchoring-readiness-and-durability`'s follow-on pass is on `main`,
and then carries both"* — and this candidate is the re-cut at the tip that
carries both.

**So the sentence the owner was protecting against never comes due.** The
per-witness `status` enumeration of `anchor-state.schema.yaml` is REPLACED in
these bytes rather than widened later against them: `[in_flight, landed,
terminally_failed]` becomes `[pending, submitted, confirmed, invalid,
unevaluable, terminally_failed]`, because `in_flight` had one word for "no
accepted submission evidence" and "submission accepted, the approved confirmation
condition unmet", and one word for both is what lets interface acceptance read as
progress toward confirmation. **Replacing a closed enumeration is free before
publication and a compatibility break after it, and this is before.** Measured,
not assumed: `git tag --contains 11feff75` is empty, and
[`contract-v3.3.digests.yaml`](releases/contract-v3.3.digests.yaml) carries zero
rows for any path under `contracts/chain-anchoring/`. **`contract-v3.4` is the
FIRST tagged bundle to carry this family, and the shape it carries is the amended
one.** No published bundle ever carried the retired spelling, so no consumer can
have written a record against it, and the amendment's own `tasks.md` § 2.4
stop-condition — *"verify … that no bundle cut the family in between"* — is
answered in the affirmative direction: none did.

### Change class: ADDITIVE (minor)

MEASURED at this candidate, not claimed. `git diff --name-status contract-v3.3
HEAD -- contracts/` reports **187 additions and 15 modifications**. Every path,
with the pull request and lane that moved it:

| path(s) | moved by |
|---|---|
| 113 A — `contracts/chain-anchoring/` as first landed (12 schemas, the family README, 21 positive examples, 75 indexed negatives) | **#629** `11feff75`, lane `openxfactory-1d` — `add-chain-anchoring`'s realization |
| M `contracts/signed-execution-chain/digest-construction.schema.yaml`, `transparency-log-leaf.schema.yaml`, `README.md` | **#629**, same commit |
| 73 A + 66 M inside `contracts/chain-anchoring/` — SIX further schemas (`confirmation-profile`, `confirmation-profile-registry`, `daily-merkle-profile`, `durability-eligibility-registry`, `durability-batch-admission`, `durability-batch-manifest`), 15 new positives, 52 new negatives, and the amendment's edits to five of the original schemas plus the family README | **#657** `e65dcc48`, lane `openxfactory-1d` — `amend-chain-anchoring-readiness-and-durability` requirements 2 and 3, **the change this cut was held for** |
| M `contracts/signed-execution-chain/digest-construction.schema.yaml`, `README.md` (again) | **#657**, same commit — six further digest subjects under the ONE construction |
| 10 files under `contracts/clearing/` (A `deliberation-return.schema.yaml` + its example and two negative fixtures; M `permitted-operations.registry.yaml`, `dispatch-record.schema.yaml`, three re-pointed fixtures, the family README) | **#652** `0df522eb`, lane `hermes-wallet-exercise` — `admit-deliberation-clearing-operation`'s realization |
| M `contracts/manifest.yaml` | **#629** (twelve registration rows plus two moved signed-execution-chain digests), **#652** (the `clearing-deliberation-return` row and a count fix), **#657** (six chain-anchoring rows), **#658** `2ba666ee`, lane `repo-shape` (a stale registration comment corrected), AND **THIS CUT** (the `contract_bundle_version` line, and nothing else) |
| M `contracts/README.md` | **#652** (the clearing family's two contract-index rows rewritten for entry two) AND **THIS CUT** (the two chain-anchoring contract-index rows appended) |
| M `contracts/CHANGELOG.md`, A `contracts/releases/contract-v3.4.digests.yaml` | **THIS CUT** — this entry and the rebuilt inventory |
| M `contracts/openreposhape-pin.yaml` | **#650** `48dc9b67`, lane `repo-shape` |
| M `contracts/review-lane-pin.yaml`, `contracts/review-lane-floor-snapshot.yaml` | **#647** `e4ff4fb3`, **#654** `bc1bd4ee` and **#660** `dda5bd3a` — three archive-driven decision-core re-pins, net `8f770afb` → `6d35c4fe`, floor 63 → 66. **NOT this cut's**, named here so a reader intersecting the diff with this entry does not attribute them to any family above |

Under § *Change Classes*, *"Additive (minor) — new optional fields, new contracts,
new validator warnings. Domain repos on the same major version remain conformant
without changes."* Argued against that text, clause by clause, and **every edit to
a schema that WAS published at `contract-v3.3` was checked for narrowing
individually**:

* **The eighteen `chain-anchoring` schemas are NEW contracts.** Nothing existed at
  `contract-v3.3` that they replace, and none of them appears in that bundle's
  inventory or in its manifest rows.
* **THE ONE REPLACEMENT IS INSIDE THE NEW FAMILY AND THEREFORE FREE.**
  `anchor-state.schema.yaml`'s per-witness `status` enumeration is replaced, not
  widened (section above). It narrows nothing published, because the schema
  carrying it is published for the FIRST TIME here. Had this cut been taken before
  #657 landed, the identical edit would have been breaking against a published
  bundle — which is exactly why the owner's ruling held it.
* **Every edit to a SHIPPED schema WIDENS.** `digest_subject` in
  `digest-construction.schema.yaml` gains eleven subjects from #629 and six more
  from #657 — seventeen in total, on that file's own written invitation that a
  later tranche add its subjects there rather than declare a second construction.
  `transparency-log-leaf.schema.yaml`'s `leaf_type` gains twelve members and the
  shape gains **ONE OPTIONAL member**, `anchor_event`. `dispatch-record.schema.yaml`'s
  closed `refusal_ground` enumeration goes from two members to five
  (`lane_not_permitted`, `output_schema_failure`, `origin_scoped_credential`), and
  `permitted-operations.registry.yaml` gains a second member with
  `registry_version` advancing 1 → 2. **No enumeration published at
  `contract-v3.3` lost a member, no required field was added to a published
  schema, no shape was removed, and no `contract_schema_version` moved.**
* **The one movement in the refusing direction refuses nothing that was ever
  valid.** `transparency-log-leaf.schema.yaml`'s `anchor_event` complement — the
  conditional refusing an anchoring block on a NON-anchoring leaf — widens to
  cover tranche two's seven kinds; **it can refuse no record that was valid at
  `contract-v3.3`, because `anchor_event` did not exist there**.
* **No role or vocabulary semantics change.** The anchoring kinds are settled
  inside tranche one's ratified leaf grammar, and the six new digest subjects are
  taken under the ONE construction, precisely so that no second vocabulary is
  minted.

**AND A CONSUMPTION PIN ADVANCED — a movement § *Change Classes* does not name.**
Said plainly rather than argued into a class it does not mention: the three
classes are written about what a release does to the shapes a DOMAIN REPO must
conform to, and `contracts/openreposhape-pin.yaml` is openxFactory's own
consumption of a neutral product, not a shape any consumer validates against. It
is classified here by the definition's own test — *"Domain repos on the same
major version remain conformant without changes"* — which it passes trivially,
since no domain repo reads it. The class is **ADDITIVE** and the number advances
the minor.

### Inventory note: this cut re-baselines the EDITORIAL members only

**MEASURED against `contract-v3.3`'s own inventory**, whose 283 entries were
searched for each moved path: `contracts/chain-anchoring/*` (zero hits),
`contracts/clearing/*` (zero hits), `contracts/openreposhape-pin.yaml`,
`contracts/review-lane-pin.yaml`, `contracts/review-lane-floor-snapshot.yaml` and
all three `contracts/signed-execution-chain/` paths are **not release-inventory
members**. Membership is closed over the surface
[`scripts/hermes_runtime_validation/release.py`](../scripts/hermes_runtime_validation/release.py)
enumerates — the `contracts/hermes-runtime/` family and its indexed fixtures, the
intent-compliance contracts, implementation, tests and validator, the four
`NAMED_VALIDATORS`, the `AUXILIARY_MEMBERS` (the two hash-locked requirements
files, the PostgreSQL image lock, the inventory schema, and the manifest,
changelog and README) and the three `NORMATIVE_DOCS` — and a new neutral family
belongs to none of them, exactly as `clearing/` did not at `contract-v3.3` and
`signed-execution-chain/` did not at `contract-v2.5`. Their identity travels by
manifest-row `sha256`, verified by `scripts/validate-manifest-digests.py`:
**169 rows at `contract-v3.3`, 188 here** — twelve from #629, six from #657, one
from #652.

So [`contract-v3.4.digests.yaml`](releases/contract-v3.4.digests.yaml) carries the
same **283 members** and re-baselines four of them, all editorial:
[`manifest.yaml`](manifest.yaml), [`CHANGELOG.md`](CHANGELOG.md),
[`README.md`](README.md) and
`tests/intent-compliance/test_release_boundary.py`. Two of those four had already
moved on `main` before this cut touched them — `README.md` by #652 and
`manifest.yaml` by four separate pull requests — which is the whole content of the
red measured at the pre-cut tip below.

**The pin is verified by its own gate, not by this inventory.**
`openreposhape-pin-gate` checks out `opensoft/openRepoShape` at the commit read
out of the pin file and re-verifies every digest against the real bytes — run
**33874963034** on #650, green: *"27 digest(s) recomputed, 33 member(s) present,
60 file(s) declared with none undeclared"*.

### The pre-cut measurement, recorded verbatim

`python3 scripts/validate-contract-release.py verify-commit --commit origin/main`
at `a858e5b0` — the final integration point this candidate is built over, and
the tip AFTER #657, #652, #658 and the three archive re-pins had all landed —
reports exactly two findings and no others:

```text
HGR-RELEASE-DIGEST-MISMATCH error path=contracts/README.md: digest does not match the raw Git blob at the pinned commit
HGR-RELEASE-DIGEST-MISMATCH error path=contracts/manifest.yaml: digest does not match the raw Git blob at the pinned commit
```

That is the bounded, expected state § *Release Digest Inventory* → *What a red
`verify-commit` at HEAD means* describes: a red confined to the EDITORIAL members
between cuts is **NOT a defect**, and *"THE REMEDY IS A RELEASE CUT, NEVER A
HAND-EDIT."* Two members and no other moved, which is the whole content of the
claim above that nothing outside the editorial set is a registered row — an entire
contract family, its amendment and a clearing register entry landed between the
two cuts and moved no inventory member at all. No digest in any file under
[`releases/`](releases/) was edited by hand; this cut's inventory is BUILT by
[`scripts/validate-contract-release.py`](../scripts/validate-contract-release.py)
`build`, last, after every other edit was final.

### `contract-v3.3` remains valid provenance

Its tag and [its inventory](releases/contract-v3.3.digests.yaml) are untouched by
this cut and stay exactly as published. Nothing here retroactively invalidates the
evidence of a consumer that verified against them, a consumer pinned at
`contract-v3.3` remains conformant without changes, and that number is never
reused. This bundle supersedes nothing and declares nothing spent.

### What this release adds

**A new neutral contract family, `contracts/chain-anchoring/`** — tranche three of
the signed execution chain, realizing the RATIFIED `add-chain-anchoring` (ratified
2026-08-30 by Brett Heap, repository owner, record
[`openspec/changes/add-chain-anchoring/review/ratification-2026-08-30.md`](../openspec/changes/add-chain-anchoring/review/ratification-2026-08-30.md),
realized by PR #629) **AS AMENDED by the RATIFIED
`amend-chain-anchoring-readiness-and-durability` requirements 2 and 3** (ratified
2026-09-04, PR #548, realized by PR #657). **Eighteen schemas** carry a per-file
`sha256` in [`manifest.yaml`](manifest.yaml); the family README, the packaged
corpus, the canonical reader `scripts/validate-chain-anchoring.py` and its pytest
wiring are content-addressed BY COMMIT, on tranche one's and tranche two's
precedent.

- **`anchoring-definitions.schema.yaml`** — the shared vocabulary declaring NO
  record kind: two witness roles, three plane names, the custody reference, the
  per-chain accepted-time rule, and THE CLOSED REFUSAL ENUMERATION in one place,
  so no sibling schema can mint a code the reader does not know.
- **`anchor-receipt.schema.yaml`** — the chain-agnostic MULTI-ANCHOR receipt, with
  the format defined first and the targets in a list inside it, so adding or
  dropping a chain moves nothing else. It carries no state member.
- **`anchor-state.schema.yaml`** — per-witness state. **SUBMITTED IS NOT
  CONFIRMED**: `pending` and `submitted` split what one word used to cover,
  `confirmed` is bound to a NAMED PROFILE's objective condition rather than to a
  word, `invalid` and `unevaluable` are reportable because the amendment's refusal
  scenario obliges a verifier to report them, and `terminally_failed` is
  unchanged. A missing witness is a declared, fail-closed state; the aggregate
  `anchored` boolean is refused by name.
- **`confirmation-profile.schema.yaml`** and
  **`confirmation-profile-registry.schema.yaml`** — an operator-approved
  confirmation condition, and the APPEND-ONLY registry that binds each version's
  terms to a canonical digest, so a `confirmed` label always names the rule it was
  confirmed under and a profile cannot be silently substituted beneath a receipt
  already minted.
- **`daily-merkle-profile.schema.yaml`**,
  **`durability-eligibility-registry.schema.yaml`**,
  **`durability-batch-admission.schema.yaml`** and
  **`durability-batch-manifest.schema.yaml`** — the FIXED-UTC durability batch:
  an immutable released Merkle construction (leaf encoding, algorithm, two domain
  separators, ordering, tree shape, odd-node handling, deterministic empty root)
  bound by digest to every admission and manifest; an append-only eligibility
  register; atomic per-window admission that cannot select by event; and a
  day-linked manifest whose continuity link is over the previous item's anchored
  digest, so two consecutive empty windows cannot be confused for one.
- **`verification-result.schema.yaml`** — one verification's answer with its
  MANDATORY verification mode, so the answer says what knowledge stands behind it.
- **`anchor-bound-commitment.schema.yaml`** — the only value this capability puts
  on a chain: keyed and salted, with both custody references, and carrying **no
  free-text member at all** — a structural refusal rather than a policed one.
- **`log-checkpoint-anchor.schema.yaml`** — a checkpoint anchor and its `const`
  never-read-as-validation disclaimer, a member of the record rather than a note
  beside it.
- **`consent-checkpoint-commitment.schema.yaml`**,
  **`plane-separation-declaration.schema.yaml`**,
  **`linkage-derivation-issuance.schema.yaml`**,
  **`linkage-derivation-use.schema.yaml`** and **`analysis-result.schema.yaml`** —
  the consent plane stays where it can be erased, keys and salts are per plane,
  the ONE lawful cross-plane correlation path is minted in the identity plane
  against an anchored consent checkpoint and bounded in time, and a silently
  partial analysis result is the failure the outcome discriminator exists to
  refuse.
- **`conformance-declaration.schema.yaml`** — where a realization says what it has
  NOT done, over `CA-R1 … CA-R9`, on `add-trust-anchor`'s ratified
  declared-shortfall pattern.
- **The packaged corpus and its canonical reader** — 41 positive examples and 127
  intended-invalid negatives, each declaring its own expected refusal, read by
  `scripts/validate-chain-anchoring.py`. Measured at this tree: *"41 packaged
  record(s) validated as ONE coherent corpus, 127 negative fixture(s) confirmed
  invalid for their intended reason, 118/118 closed refusal codes red-proven"*,
  exit 0, with two standing warnings that are DECLARED shortfalls rather than
  defects — `reader-not-required` and `archival-node-undeclared`.
- **The tranche-three widenings of tranche one's grammar**, described under the
  class above: `digest_subject` by seventeen subjects across two commits,
  `leaf_type` by twelve members and one optional `anchor_event` block. **No second
  grammar and no second digest construction** — `add-chain-anchoring` `tasks.md`
  5.3's own rule, kept by the amendment's realization as well as by the basis.

**`deliberation` becomes clearing register ENTRY NUMBER TWO** — the realization of
the RATIFIED `admit-deliberation-clearing-operation` (ratified 2026-09-04 by
Brett Heap, proposal merged `3cf917b7` as PR #645, realized by PR **#652**,
`0df522eb`, lane `hermes-wallet-exercise`). A bundle-carrying, EVIDENCE-ONLY
operation on the ARTIFACT LANE ONLY, with `checks_out_code`, `writes`,
`may_reference_secrets` and `repository_affecting_output` all false, `token_scopes`
exactly `[actions:read]`, and NO key of any kind, because the return is signed ON
RETURN by the originating repository. It brings the neutral
[`deliberation-return.schema.yaml`](clearing/deliberation-return.schema.yaml)
(kind `xfactory_clearing_deliberation_return`) as the family's SEVENTH registered
row, carries `dispatch-record.schema.yaml`'s closed `refusal_ground` enumeration
from two members to five, and advances the register instance's `registry_version`
1 → 2 in the same act, because a governed change to a closed set that left the
version alone would make two different registers indistinguishable by their own
declaration. **Those rows reserved no bundle number** — they were registered at
realization and left the minor to this cutting session, which is § *Version
Identity*'s rule; lane `hermes-wallet-exercise` said so in its row-4 notice on
issue #630 and asked only that this entry name the change, which it does here.

**The `openRepoShape` consumption pin advances**
`deacbdcce4f52af427bcb4edd075fcc992e3dabe` → `122d729bc0c2f2e0ded0bb61b6b97f49512f613e`
(#650, issue #649, on the owner's word *"bump the openRepoShape pin in
openxFactory"*). The pin's grammar makes that a **re-enumeration rather than a
one-line edit**: its two lists must cover exactly the files present at the pinned
commit or the verifier reports `pin-surface-undeclared`, and the new commit
carries **60 files where `deacbdcc` carried 34** — a **27 digested / 33 path-only**
split, from 16 / 18. Upstream, those eighteen commits are the standard's v0.2
(`adopt-project.py`), v0.3 (`update-shape.py`) and v0.4 (the FAMILY shape and
spec-only adoption), the App-token leg credential, `setup.sh` self-bootstrap, the
`openapi`→spec classification, the ratified-reference default (#19) and the
`recorded_gitlink()` index-first fix (#25) — **the shape every project carrying
the standard had already taken through `update-shape`** (MedxEHR, MedxGlass, IRRS,
IRSS and the InkRouter holder), which is what made openxFactory's pin the last
reader still at the ratification commit. Every new file was classified by the
pin header's own rule rather than by the release it arrived in, and **no member
declared at `deacbdcc` changed list**. `deacbdcc` stays the commit
`add-project-repo-schema` was RATIFIED against — a historical fact that does not
move with the pin, and
[`docs/project-repo-schema.md`](../docs/project-repo-schema.md) carries a dated
amendment note saying exactly that.

**The editorial re-baseline** — [`manifest.yaml`](manifest.yaml),
[`README.md`](README.md), this file, and
[`contracts/releases/contract-v3.4.digests.yaml`](releases/contract-v3.4.digests.yaml).

### WHAT THIS RELEASE DOES NOT CONFER

**REGISTRATION IS NOT ENFORCEMENT, AND THE PACKAGED DECLARATION SAYS SO.**
`contracts/chain-anchoring/`'s conformance declaration records
`is_required_in_ruleset: false`. Until a named reader runs as a REQUIRED check on
the repository holding these records, everything registered here confers and
refuses exactly nothing — tranche one's own distinction, which took it from
realization on 2026-08-29 to a required check on 2026-08-31 (opensoft org ruleset
**21957695**). Making a check required is an operator act on a ruleset and no
cut performs it. The same is true of `clearing-dispatch-gate`, which REPORTS
rather than GATES until an operator makes it required.

**NOTHING IS ANCHORED BY THIS BUNDLE.** No witness is configured, no receipt is
captured, no confirmation profile is approved, no durability window is opened,
nothing is placed on any chain, and this repository operates no anchoring
subsystem. What ships is the EVENT-RECORDING grammar for those acts.
`add-chain-anchoring`'s operator conditions — its tasks 4.9 and 4.10, and its § 5
settlements — are UNGATED AND UNTICKED, `SEC-R6` stays declared and open until an
anchor actually lands, and neither `add-chain-anchoring` nor its amendment
archives with this cut.

**ADMITTING `deliberation` AUTHORIZES NO HOST JOB.** The register entry is the
shape and the permission grammar; the act that declares a host job must, in the
same act, retire the grandfathered `council-deliberation-worker.yml` route, and
that act is `opensoft/xFactory`'s, not this bundle's.

### A guard repaired by this cut, because this cut is where it could first fire

`tests/clearing/test_clearing_manifest_rows.py` carried
`test_the_declared_bundle_version_is_the_one_the_rows_name`, written at
`contract-v3.3` and asserting `doc["contract_bundle_version"] == "contract-v3.3"`
against the LIVE manifest. **That equality could only hold until the next cut.**
The clearing rows' `Registered at contract-v3.3` is HISTORY — the bundle whose
bytes first carried that family, which never moves — while
`contract_bundle_version` names what the repository declares TODAY and advances
at every cut. The two were the same number for exactly one release and the test
pinned them to each other, so it reds the REQUIRED `pytest-suite` here.

**Repaired rather than re-pinned**, because re-pinning it to `contract-v3.4`
would only move the failure to `contract-v3.5`. The guard's stated purpose — *"a
cut that moved one and not the other would publish rows claiming a release the
bundle does not declare"* — survives whole: the test now reads the registering
release OUT OF the rows, requires them to name ONE release, requires an inventory
beside both that release and the declared bundle, and requires the declared bundle
never to be BEHIND the release the rows advertise. Renamed to
`test_the_declared_bundle_has_an_inventory_and_is_not_behind_the_rows` to say
what it checks. **It composes with #652's own edit to the same file** — that PR
added a per-row `REGISTRATION` map so `clearing-deliberation-return`, registered
at realization rather than at a cut, names its CHANGE instead of a bundle
number — and both intents survive together: the row registered at realization
names no release, so the "one registering release" set stays a singleton, and the
per-row provenance check is untouched. The file is not a release-inventory member
(measured: no `tests/clearing/` path appears in either inventory), so this repair
moves no digest of its own.

### The bundle number, FRESH-COUNTED at the re-cut

Measured at the rebased tip rather than trusted:

- [`manifest.yaml`](manifest.yaml) declared `contract_bundle_version:
  contract-v3.3` before this edit.
- [`releases/`](releases/) held inventories through
  [`contract-v3.3.digests.yaml`](releases/contract-v3.3.digests.yaml).
- `git ls-remote --tags origin` publishes annotated tags through
  `contract-v3.3`; `contract-v3.4` is free, and `verify-promotion` reports no
  `HGR-RELEASE-TAG-EXISTS` and no version-not-next finding.
- There is no `Unreleased` block pending in this file.

`contract-v3.4` is taken here. No proposal reserved it: `add-chain-anchoring`'s
`tasks.md` 4.11, the eighteen chain-anchoring manifest rows and
`admit-deliberation-clearing-operation`'s seventh clearing row all say in terms
that **no bundle number is taken or reserved by that registration**, which is
§ *Version Identity*'s rule that a proposed change MUST NOT reserve a minor
before merge order is known.

### Also carried into this cut: `add-chain-anchoring`'s cut half (task 4.12)

The owner overruled 4.11's timing — Brett Heap, 2026-09-04, verbatim: *"merge
629, register now"* — so the twelve manifest rows and the family README's
registration paragraph landed at realization, on the TRANCHE-TWO PRECEDENT where
`add-chain-attestation` added its eight rows in #556 (`518c670b`) and left the
number and the changelog entry to the cut (#565, `bbbbeda9`). **4.12 is the half
that was carried forward and this cut discharges it**: this entry, the
`contract_bundle_version` bump, the two durable
[`contracts/README.md`](README.md) contract-index rows, and the rebuilt digest
inventory. What 4.12 also asks — `verify-commit` and `verify-tag` green from an
independently refreshed clone — belongs to steps 4 and 5 below and is not
claimed here.

### Migration guidance

* **A consumer pinned at `contract-v3.3` re-pins to `contract-v3.4`** by moving
  `xfactory.contract_ref` to this bundle's published commit, recording the tag,
  and re-running the per-file digest checks under § *Domain Upgrade Runbook*.
  **There is no shape work.** Nothing this bundle carries refuses anything
  `contract-v3.3` accepted; every edit to a published schema only widens; and the
  eighteen new chain-anchoring schemas plus the new clearing return shape describe
  records no existing consumer writes.
* **A consumer intending to WRITE `chain-anchoring` records reads THIS bundle and
  no earlier draft of the family.** The per-witness `status` vocabulary published
  here is `[pending, submitted, confirmed, invalid, unevaluable,
  terminally_failed]`; `in_flight` and `landed` were never published in any tagged
  bundle and must not be written. A `confirmed` row without the named profile and
  the condition it satisfied is refused.
* **A clearing producer may now emit three further refusal grounds**
  (`lane_not_permitted`, `output_schema_failure`, `origin_scoped_credential`) and
  a `deliberation` operation id. Nothing already emitted becomes invalid.
* **The `openRepoShape` pin is not a consumer-facing surface.** A domain repo
  neither reads nor pins `contracts/openreposhape-pin.yaml`, and no upgrade work
  follows from its advance.

### The annotated tag is published at the LANDED commit, not from this branch

§ *Bundle Realization Order* step 4: *"Land the exact reviewed commit on published
`main`. If promotion creates a different commit, that commit becomes the new
candidate and every gate and review reruns before tagging."* Step 5 then publishes
the tag at that exact published commit. **SKIPPING THE RE-VERIFICATION AT STEP 4
IS WHAT MADE `contract-v3.1` DEFECTIVE** — a squash merge ALWAYS creates a
different commit. So the tag for this release is NOT pushed from the cutting
branch: after this cut lands on `main`, `verify-commit --commit <landed sha>` is
re-run at the landed commit, and only then is the annotated tag published there
and verified from an independently refreshed checkout.

## contract-v3.3 — 2026-09-03 (additive; the neutral clearing-dispatch boundary becomes contract bytes)

Realizes the RATIFIED change **`add-clearing-dispatch-boundary`** — ratified
2026-09-01 by Brett Heap (repository owner), record at
[`openspec/changes/add-clearing-dispatch-boundary/review/ratification-2026-09-01.md`](../openspec/changes/add-clearing-dispatch-boundary/review/ratification-2026-09-01.md),
merged as PR **#555**, squash `ab0bb2dd2e642fce43bee3d02128bafd664d3be3`, on
2026-09-02 — as MODIFIED by **`add-cpc-clearing-boundary`**, ratified 2026-09-02
and merged at `c0270d28`.

**THE PACKET AUTHORED NO CONTRACT BYTE, AND SAID SO.** Its `code_surface`
paragraph is explicit: *"The neutral openxFactory artifacts are DECLARED here and
REALIZED POST-RATIFICATION at their own additive cut, because ratification
authorizes realization and does not perform it."* Its `tasks.md` §6 is the
artifact list, and §6.8 defers the number: *"the minor allocated AT REALIZATION
after merge order is known."* This is that cut.

### Change class: ADDITIVE (minor)

MEASURED, not claimed. `git diff --name-status contract-v3.2 HEAD -- contracts/`
at this cut reports **39 additions and 5 modifications**. Of the five, two —
`contracts/review-lane-pin.yaml` and `contracts/review-lane-floor-snapshot.yaml`
— are NOT this cut's: they moved on `main` in `c271caa2` (#615), between the
`contract-v3.2` tag (which peels to `9a773a31`) and this branch's base
`6a39d2ab`, and they are named here so a reader intersecting the diff with this
entry does not attribute them to the clearing family. **The three this cut owns
are `contracts/manifest.yaml` (registration and the version line),
`contracts/README.md` (two index rows), and
`contracts/signed-execution-chain/digest-construction.schema.yaml`**, whose
`digest_subject` enumeration gains ONE member.

Under [`docs/contract-versioning-policy.md`](../docs/contract-versioning-policy.md)
§ *Change Classes*, *"Additive (minor) — new optional fields, new contracts, new
validator warnings. Domain repos on the same major version remain conformant
without changes."* Every artifact here is NEW. The single edit to a shipped
schema ADDS an enum member, which widens what validates and narrows nothing: no
record conformant at `contract-v3.2` becomes non-conformant, no required field is
added to an existing shape, no `contract_schema_version` moves, and no role or
vocabulary semantics change. The class is **ADDITIVE** and the number advances
the minor.

### What this release adds

**A new neutral contract family, `contracts/clearing/`** — the machine-readable
half of the ratified `clearing-dispatch-boundary` capability. Six artifacts carry
per-file `sha256` in [`manifest.yaml`](manifest.yaml); the validator, the family
README, the packaged corpus and the tests are content-addressed by commit, on the
openxWallet / client-identity-roster / identity-brokering / trust-anchor /
signed-execution-chain precedent.

- **`sealed-bundle-manifest.schema.yaml`** — the SEALED BOUNDED REQUEST: exactly
  the TEN declared fields, `expires_at` required (an expiring object is a
  REQUEST; a committed copy is a MIRROR that outlives the work), a byte-tagged
  hash per selected file, and field (10) as a TAGGED UNION. Field (10) is where
  `add-cpc-clearing-boundary` tightens the basis: an ORIGIN SIGNATURE is REQUIRED
  where the originating repository holds an active row in
  [`governance/factory-identity/`](../governance/factory-identity/README.md), and
  trusted hosted-workflow provenance satisfies it only where no identity is
  registered — so registering an identity TIGHTENS a producer and never loosens
  one, and the boundary stays usable by a producer not yet issued a key.
- **`permitted-operations.schema.yaml` + `permitted-operations.registry.yaml`** —
  the CLOSED register, as a schema-plus-instance pair on the convention
  `trust-anchor`'s chain-custody registry already uses against
  `openxwallet-custody`. **THE INSTANCE HOLDS EXACTLY ONE MEMBER**,
  `readiness-diagnostic`, the ratified entry number one, with its permitted
  semantics in both directions, its class constraints (no checkout, no writes, no
  secret reference, an EMPTY token-scope list, a five-minute bound), its worker
  profile, both lanes with literal groups and labels, its output schema, its
  handling class, and `repository_affecting_output: false`.
- **`operation-report.schema.yaml`** — the COMPOSED report of record: one per
  dispatch across however many lanes were probed, per-lane facts as a keyed
  collection, each lane's group and label typed as DECLARED, the environment echo
  restricted by `propertyNames` to the ratified NAME ALLOWLIST so a wholesale
  dump is unrepresentable, and NO eligibility verdict.
- **`dispatch-record.schema.yaml`** — the ledger, written for cleared dispatches
  AND refusals in ONE shape, with resolved values beside claimed ones, THREE
  verification classes kept apart, refusal grounds from a CLOSED enumeration
  seeded with exactly the two the current realization emits, and workspace
  disposal as a required field.
- **`single-door-attestation.schema.yaml`** — the per-group comparison that keeps
  the ledger's completeness claim honest, with a WIDENING, a DARK LANE and
  CONVERGENCE-NOT-YET-REACHED as three distinct findings and the completeness
  claim carrying its own strength.
- **`scripts/validate-clearing-dispatch.py`** — the canonical validator. 26
  closed refusal codes, ALL 26 red-proven by a packaged fixture; a code with no
  probe is itself a finding. Two of the twenty-six answer questions the shapes
  cannot ask: `clearing-origin-row-expired` refuses a producer whose origin row
  is recorded `state: active` but whose declared expiry has PASSED — in BOTH
  directions, since skipping the row would let an expiry LOOSEN what field (10)
  may carry — and `clearing-artifact-unparseable` refuses a file that names one
  of the family's kinds and does not parse, because an artifact the sweep could
  not read is not an artifact the sweep cleared.
- **The packaged corpus** — `contracts/clearing/examples/`: 6 positive examples
  and 26 intended-invalid negatives, one per closed refusal code, each declaring
  its own `# expected_failure:` header and naming the ratified sentence it
  violates.
- **`.github/workflows/clearing-dispatch-gate.yml`** — job id
  `clearing-dispatch-gate`, no display name, with a POSITIVE log assertion.
- **`tests/clearing/`** — the per-family pytest wiring, including
  `test_clearing_manifest_rows.py` closed in BOTH directions and
  `test_clearing_gate_wiring.py` pinning the CI invocation inside the required
  `pytest-suite` job. Both carry the family in the filename because
  `tests/signed_execution_chain/` already claims those bare module names and
  neither directory is a Python package, so collection would fail with an
  import-file mismatch the moment both are collected.
- **The tranche-3 `digest_subject` widening** — `sealed_bundle_manifest` added to
  `contracts/signed-execution-chain/digest-construction.schema.yaml` and to
  `scripts/signed_execution_chain/canonical.py`'s frozen `SUBJECTS`. That file's
  own header declares this the one way it may move: *"A LATER TRANCHE ADDS NO
  SECOND RULE. Any digest a later tranche introduces is computed under this
  construction, with its subject added to the enumeration below."*
- **The editorial re-baseline** — `manifest.yaml`, `README.md`, this file, and
  [`contracts/releases/contract-v3.3.digests.yaml`](releases/contract-v3.3.digests.yaml).

**NO SECOND VOCABULARY.** Digests are `signed-execution-chain`'s one
construction; runner groups, labels and trust tiers are
`worker-enrollment-broker`'s; scoped credentials are `credential-contracts`';
job scope references are `neutral-job-envelope`'s; handling classes are
`document-cataloging`'s; and the origin identity a field-(10) signature resolves
to is `factory-origin-identity`'s. Per-file content hashes stay OUTSIDE the
canonical-JSON construction and are plain algorithm-tagged SHA-256 over file
BYTES, because a canonicalization has nothing to canonicalize in a byte stream.

### WHAT THIS RELEASE DOES NOT CONFER

**REGISTRATION IS NOT ENFORCEMENT.** These are the shapes a clearing
implementation validates, records and attests with. The boundary is enforced by
the clearing repository's own workflow — `opensoft/xFactory`'s
`clearing-dispatch.yml` (PR #191, squash `95f1a9c6`), which today validates its
dispatched operation against its own literal choice list. The ratified packet's
`tasks.md` §3.7 states the consequence in its own words: *"once §6.2 lands, the
clearing workflow MUST validate the dispatched operation id against the registry
INSTANCE and stop relying on its own choice list as the authority."* That is a
task of the clearing repository, and this cut does not discharge it.

**THE GATE IS NOT YET A REQUIRED CHECK.** `clearing-dispatch-gate` runs on every
pull request and on `main`, and making it REQUIRED is an operator act on a
ruleset — as `wallet-validation` (opensoft ruleset 21538893) and
`signed-execution-chain-gate` (21957695) each needed. Until that act it REPORTS
rather than GATES, and where a protection rule admits bypass actors a required
check is bypassable by those actors.

**THE CLOSURE REFUSAL IS A TRIPWIRE, NOT AN UNFORGEABLE REFUSAL.** The register,
the validator that reads it and the test that pins it share a repository with the
changes they police, so one diff can edit every side. What it guarantees is that
an addition cannot be made SILENTLY — a red check plus a diff touching the
register or the validator — and REVIEW OF THAT DIFF is the declared backstop.
This is the same honesty the ratified authoring-time guard requires of its own
mechanism.

**MEMBERSHIP ASYMMETRY, which a reviewer will ask about.** The six clearing
artifacts are registered in [`manifest.yaml`](manifest.yaml) and are NOT members
of [`contract-v3.3.digests.yaml`](releases/contract-v3.3.digests.yaml). The
release inventory's membership is CLOSED over the release surface — the Hermes
runtime contract family and its indexed fixtures, the named validators, the
hash-locked requirements files, the PostgreSQL image lock, the inventory schema,
the contracts manifest, changelog and README, and every modified normative
contract or versioning document. A new neutral family belongs to none of them,
exactly as `signed-execution-chain` did at `contract-v2.5` and
`xfactory-credential-contracts.schema.yaml` did at `contract-v2.4`. Its identity
travels by manifest-row `sha256`, verified by
`scripts/validate-manifest-digests.py` and by the family's own scoped test.

**NOT THIS RELEASE'S SURFACE**, each named by the ratified `code_surface`
paragraph as a successor or as somebody else's artifact:
`realize-factory-bundle-packaging` (the codexFactory hosted packaging workflow
and the CODING operation's entry); the HOSTED FINALIZER for patch-returning
operations, gated on it because `readiness-diagnostic` returns nothing a
finalizer would validate; the grandfather retirements; any runner, group, label,
host or credential; the L4 authoring-time guard and the L5 attestation
IMPLEMENTATIONS in `opensoft/xFactory`; the `deliberation` register member
(codexFactory #165, a LATER governed change, and the fixture that proves the
closure refusal fires); and the `sealed_return` digest subject that
`add-cpc-clearing-boundary` `tasks.md` §2.9 names beside the manifest subject —
nothing here computes a digest over a return, and an admitted subject with no
consumer is a widening no shape exercises.

### The bundle number, FRESH-COUNTED at the cut

Measured at this branch's tip rather than trusted:

- [`manifest.yaml`](manifest.yaml) declared `contract_bundle_version:
  contract-v3.2` before this edit.
- [`releases/`](releases/) held inventories through
  [`contract-v3.2.digests.yaml`](releases/contract-v3.2.digests.yaml).
- `git ls-remote --tags origin` publishes annotated tags through
  `contract-v3.2`; `contract-v3.3` is free.
- No open pull request cuts a bundle (`gh pr list --state open`, 10 open, none a
  cut).
- There is no `Unreleased` block pending in this file.

**THE TWO CUTS THE PACKET NAMED AS AHEAD OF IT HAVE RESOLVED, WHICH IS WHY THIS
NUMBER IS AVAILABLE.** `add-clearing-dispatch-boundary`'s front matter reads:
*"the in-flight realization of `add-chain-attestation` takes the next additive
cut, and the in-flight realization of `add-chain-anchoring` allocates after
it."* Since then `add-chain-attestation` tranche two landed and was CARRIED at
[`contract-v3.0`](#contract-v30--2026-09-02-breaking-three-retirements-execute-chain-attestations-content-is-carried-and-contract-v26-is-superseded-unpublished)
(PR #556, squash `518c670b`), and `add-chain-anchoring`'s realization has NOT
landed — no `contract-v*` entry names it. Neither claim stands ahead of this one
now. The packet's own front matter, which recorded `contract-v2.5` at authoring
time, is stale BY DESIGN: § *Version Identity* forbids a proposal reserving a
minor before merge order is known, and this cut read the manifest at its own tip
as that section requires.

### The annotated tag is published at the LANDED commit, not from this branch

[`docs/contract-versioning-policy.md`](../docs/contract-versioning-policy.md)
§ *Bundle Realization Order* step 4: *"Land the exact reviewed commit on
published `main`. If promotion creates a different commit, that commit becomes
the new candidate and every gate and review reruns before tagging."* Step 5 then
publishes the tag at that exact published commit.

**SKIPPING THE RE-VERIFICATION AT STEP 4 IS WHAT MADE `contract-v3.1`
DEFECTIVE** — a squash merge ALWAYS creates a different commit, and
`verify-commit` was not re-run there before the tag was pushed. So the tag for
this release is NOT pushed from the realization branch. After this cut lands on
`main`, `python3 scripts/validate-contract-release.py verify-commit --commit
<landed sha>` is re-run at the landed commit, and only then is the annotated tag
published there and verified from an independently refreshed checkout.

### Also realized in this cut: `add-consumer-identity-namespace` (#622)

**THE BYTES WERE ALREADY IN THIS RELEASE'S TREE AND THIS ENTRY DID NOT NAME
THEM.** `add-consumer-identity-namespace` — ratified 2026-09-03 by Brett Heap,
the convener, verbatim *"implement your recommendations on all these"* — merged
as PR **#622**, squash `95c2cf6ae530e6cd0570dd766dd98269d06a75fa`, BEFORE this
cut's branch point, so its schema, validator and documentation bytes ship inside
`contract-v3.3`. Its ruling **excluded the cut in terms**, leaving the changelog
entry to whoever cut next; two lanes then measured the same free number at the
same hour and **`contract-v3.3` is #628's by merge order**, which is what
[`docs/contract-versioning-policy.md`](../docs/contract-versioning-policy.md)
§ *Version Identity* means by allocating late. **This block is folded into the
already-allocated entry BEFORE the annotated tag is published** — § *Bundle
Realization Order* step 4, the step that treats a promoted commit as a new
candidate every gate reruns against — rather than spending `contract-v3.4` on a
release whose bytes are already here, and the sections above it are untouched.

`add-consumer-identity-namespace`'s `tasks.md` § 5.3 prescribes what a changelog
entry realizing it must say, so that no cutting session invents it. **VERBATIM,
as that task states it:**

> **THE CHANGELOG ENTRY IS PRESCRIBED SO THE CUT INVENTS NOTHING**: class
> ADDITIVE (minor); the entry states that `consumer.identity_namespace` is
> declared and unconstrained at this release; that the shared-authority
> comparison reads the PAIR where both sides declare a grammatical namespace and
> the BARE identity everywhere else, so absence and malformedness REPORT rather
> than clear; that one predicate serves both the named finding and the lift's
> third condition; that the block's SHAPE codes go from EIGHT to NINE with
> `consumer-identity-namespace-grammar`, whose deprecation window OPENS AT THIS
> RELEASE rather than at `contract-v2.4`; that the one narrowing is
> `baked-secret` over the third free string, under § 2.6's precedent; and that
> nothing else narrows — the member being optional, the schema constraining
> nothing about the block, and the comparison only ceasing to refuse.

Discharged clause by clause, and **the class this packet contributes is ADDITIVE
(minor)**, which is the class this release already carries:

* **`consumer.identity_namespace` is DECLARED AND UNCONSTRAINED at this
  release.** It joins the `consumer:` block's DESCRIBED member set in
  [`contracts/schemas/xfactory-credential-contracts.schema.yaml`](schemas/xfactory-credential-contracts.schema.yaml)
  exactly as every other member of that block stands at this minor: no `type`,
  no `pattern`, no `required:`, no `additionalProperties: false`. The
  constraining acts are queued at the major and are NOT taken here.
* **The shared-authority comparison reads the PAIR where both sides declare a
  grammatical namespace, and the BARE identity everywhere else, so absence and
  malformedness REPORT rather than clear.** `shared-authority-identity` compares
  `(identity_namespace, fetch_identity)` only when BOTH bindings declare a
  namespace matching the identifier grammar; in every other case — neither
  declares one, one declares one, a declared value is ungrammatical, a declared
  value is null — the comparison falls back to the bare fetch identity and
  behaves exactly as the shipped validator behaves. An estate able to silence a
  real shared authority by OMITTING a member on one side would hold a rule it
  could switch off without writing anything false; this release does not give it
  one.
* **ONE predicate serves BOTH the named finding and the lift's third
  condition.** `_same_fetch_authority` in
  `scripts/validate-credential-contracts.py` is called from both places the
  promoted text states the comparison, because two implementations of one
  sentence drift.
* **The `consumer:` block's SHAPE codes go from EIGHT to NINE**, the ninth being
  `consumer-identity-namespace-grammar`, a WARNING over a declared value outside
  the identifier grammar. **Its deprecation window OPENS AT THIS RELEASE rather
  than at `contract-v2.4`** — stated in
  [`docs/contract-versioning-policy.md`](../docs/contract-versioning-policy.md)
  § *Deprecations Currently In Force*'s ninth row and in a paragraph of its own
  there, because a row that borrowed a window it never served is exactly the
  defect that entry exists to prevent.
* **THE ONE NARROWING IS `baked-secret` OVER THE THIRD FREE STRING**, taken
  deliberately under `add-binding-consumer-identity` § 2.6's own precedent: that
  task extended this error-level screen to the two free-string members it
  declared, in the release that declared them, on the ground that a new
  free-string sink on the record kind whose invariant is *"never bake a secret"*
  is a gap rather than a permission.
* **NOTHING ELSE NARROWS.** The member is optional; the schema constrains
  nothing about the block; and the comparison only ceases to refuse — it can
  make a pair that is reported today go silent, and only when both sides declare
  a grammatical namespace and the two differ. `identity_namespace` joining
  `CONSUMER_MEMBERS` likewise only REMOVES a warning: a block carrying that key
  draws `consumer-block-unknown-member` today and stops. No consumer pinned at
  `contract-v3.2` is made non-conformant by this packet's bytes.

**What #622 moved over the registered release surface**, measured by
intersecting `git diff --name-only contract-v3.2 95c2cf6a` with the 283
registered members of
[`contract-v3.2.digests.yaml`](releases/contract-v3.2.digests.yaml) —
**exactly two**, both #622's alone:

* [`contracts/manifest.yaml`](manifest.yaml) — the `credential-contracts` row's
  `sha256` recomputed from the schema bytes on disk (`d0e936fc7377…` →
  `b8aa4c77e937…`) and its `consumption_rule` extended with the member and the
  comparison. FORCED rather than chosen: `test_manifest_row_digest.py` reds at
  the commit on any schema move that leaves the row behind, so a consumer never
  verifies a digest for bytes nobody shipped.
* [`docs/contract-versioning-policy.md`](../docs/contract-versioning-policy.md)
  — a `NORMATIVE_DOCS` release member: § *Deprecations Currently In Force* gains
  the ninth table row, the member in the entry's own enumeration, the act count
  SEVEN → EIGHT, the reconciliation paragraph's corrected ordinal, and the new
  paragraph opening the ninth row's window at its own minor.

**#622's schema and validator are NOT registered inventory rows** — measured,
zero occurrences of either path in
[`contract-v3.2.digests.yaml`](releases/contract-v3.2.digests.yaml).
`contracts/schemas/xfactory-credential-contracts.schema.yaml` is pinned instead
by its `contracts/manifest.yaml` row's `sha256`, which IS registered and moved
with it; `scripts/validate-credential-contracts.py` is not one of the four
`NAMED_VALIDATORS`; the five packaged fixtures under
`examples/credential-contracts/` and the two governance documents
[`docs/credential-access-model.md`](../docs/credential-access-model.md) and
[`docs/domain-factory-starter-pack.md`](../docs/domain-factory-starter-pack.md)
are likewise unregistered. **This fold changes no inventory membership**: the
inventory is rebuilt at the amended tree by the repository's own builder, and
the only digest that moves is this file's own.

**Migration guidance for this packet's half of the release.** A consumer
re-pinning to `contract-v3.3` owes no shape work for it: the member is optional
and unconstrained, and a binding that declares nothing is accepted exactly as
before. An estate that DOES declare `consumer.identity_namespace` should declare
it on BOTH sides of any pair it expects the comparison to distinguish — one-sided
and ungrammatical declarations fall back to the bare fetch identity and keep
reporting, which is the designed behaviour and not a defect to work around.
`consumer-identity-namespace-grammar` is a WARNING and reddens nothing at this
release. The one new refusal is `baked-secret` over `identity_namespace`.

## contract-v3.2 — 2026-09-03 (additive; the SUPERSEDING release for defective `contract-v3.1`, whose published inventory records two stale digests)

**THIS CUT EXISTS TO CORRECT A DEFECTIVE PUBLISHED RELEASE AND DOES NOTHING
ELSE.** `contract-v3.1` was cut by PR **#616** (squash
`19d008723e10b2e19d96bc217292564c941e9f93`) and its annotated tag was pushed at
that commit. The bundle does not verify there. Both
`python3 scripts/validate-contract-release.py verify-commit --commit 19d00872`
and `verify-tag --remote origin --tag contract-v3.1` report, verbatim:

```text
HGR-RELEASE-DIGEST-MISMATCH error path=requirements/hermes-runtime-contracts.in: digest does not match the raw Git blob at the pinned commit
HGR-RELEASE-DIGEST-MISMATCH error path=requirements/hermes-runtime-contracts.lock: digest does not match the raw Git blob at the pinned commit
```

[`docs/contract-versioning-policy.md`](../docs/contract-versioning-policy.md)
§ *Immutable Tag Correction* governs exactly this case: *"A published annotated
tag is immutable: it is never moved, deleted, or re-tagged, not even for a
defective release. A release found defective after tagging is corrected by a
superseding release — allocate the next available version through the same
realization order, record the defect and its migration guidance in
`contracts/CHANGELOG.md`, and let consumers upgrade by pinning the new
bundle."* **THIS IS THAT SUPERSEDING RELEASE**, cut on the convener's ruling —
Brett Heap, 2026-09-03, verbatim: *"cut 3.2"*.

### The measured cause, and whose error it was

MEASURED RATHER THAN INFERRED. The `contract-v3.1` inventory was built LAST at
#616's branch head `a981c988`, where it verified. The branch forked at
`0bf37d14`, and THREE first-parent landings reached `main` between that fork and
the squash: `ea117d4e` (#610), `4fc7b94c` (#566) and `995c0ad5` — the merge of
`11db75ee` (#621, *"The mint script's Ed25519 dependency is declared where the
suite installs it"*).
Intersecting the eighteen paths `git diff --name-only a981c988 19d00872` reports
with the 283 registered members of
[`contract-v3.1.digests.yaml`](releases/contract-v3.1.digests.yaml) leaves
EXACTLY TWO, and both are #621's alone:
`requirements/hermes-runtime-contracts.in` and
`requirements/hermes-runtime-contracts.lock` — inventory rows
`requirements-hermes-runtime-contracts.in` and
`requirements-hermes-runtime-contracts.lock`. The squash carried #621's bytes
into the tagged tree while the inventory kept its pre-#621 digests.

**THE DEFECT IS NOT #621's.** That pull request is an ordinary landing on `main`
doing exactly what a landing does. § *Bundle Realization Order* step 4 is the
step that was skipped: *"Land the exact reviewed commit on published `main`. If
promotion creates a different commit, that commit becomes the new candidate and
every gate and review reruns before tagging."* A squash merge ALWAYS creates a
different commit, and `verify-commit` was not re-run at that commit before step
5 published the tag. **That was lane repo-shape's error**, in the cutting
session itself, and it is recorded here in those terms rather than attributed to
the merge mechanism or to the unrelated pull request whose bytes it carried.
This is the same omission — a cut branch not reconciled with the integration
point — that made `contract-v2.6` unpublishable, arriving at a different step of
the same order.

### Change class: ADDITIVE (minor)

MEASURED. `git diff --name-status contract-v3.1 HEAD` at this cut's branch point
is **EMPTY**: the published tag peels to `19d00872`, which is `origin/main`'s
tip, so this bundle's content is `contract-v3.1`'s realized surface exactly —
with the two requirements files as they now stand on `main`, and with this cut's
own release-surface edits on top. Under
[`docs/contract-versioning-policy.md`](../docs/contract-versioning-policy.md)
§ *Change Classes* the only movement over any registered member is #621's
`cryptography==50.0.0` declaration in `requirements/hermes-runtime-contracts.in`
and the lock closure it pins — a build dependency ADDED, with no required field
added, no shape removed, and no role or vocabulary semantics changed. Nothing a
consumer pinned at `contract-v3.1` declares becomes non-conformant, so the class
is **ADDITIVE (minor)** and the number advances the minor. NOT
`contract-v3.1.1` OR ANY OTHER SUB-MINOR: § *Version Identity*'s tag form is
`contract-v<major>.<minor>` exactly, with no third component.

### The number, fresh-counted at the cut

`contracts/manifest.yaml:3` declared `contract-v3.1`; `contracts/releases/` held
inventories through `contract-v3.1.digests.yaml`; the annotated tag
`contract-v3.1` is published, and stays published; this changelog headed at
`contract-v3.1` with no `Unreleased` block pending. The next available number is
**`contract-v3.2`**, taken here. `contract-v3.1` is not re-cut, not re-tagged
and not reused.

### No new capability is realized by this cut

Nothing beyond what `contract-v3.1` already named is realized here. No OpenSpec
change archives with this cut, no schema, validator or governance document gains
behaviour, and no deprecation entry moves in either direction.
`add-project-repo-schema` was and remains realized by `contract-v3.1` — that
realization is not repeated, undone or re-attributed, and a reader asking what
this family added must read the `contract-v3.1` entry below. What this cut moves
is the release surface and nothing else: the manifest bump, this entry, the
rebuilt inventory [`contract-v3.2.digests.yaml`](releases/contract-v3.2.digests.yaml),
and the by-hand statement `tests/intent-compliance/test_release_boundary.py`'s
`ReleaseState` tripwire requires of every cut past the floor — recording, as
every advance above it does, that this bundle touches NO intent-compliance
member and that the membership that file asserts is UNCHANGED.

### Migration guidance

* **A consumer pinned at `contract-v3.1` re-pins to `contract-v3.2`.** Move
  `xfactory.contract_ref` to this bundle's published commit, record the tag
  `contract-v3.2`, and re-run the per-file digest checks under § *Domain Upgrade
  Runbook*. There is no shape work: nothing this bundle carries refuses anything
  `contract-v3.1` accepted, and the two files whose digests move are build
  requirements, not contracts.
* **`contract-v3.1`'s tag and its inventory remain exactly as published**, as
  immutable provenance. Neither is moved, deleted, re-tagged nor edited, and
  nothing retroactively invalidates the evidence of a consumer that verified
  against it. `verify-commit` at `19d00872` will keep reporting the two lines
  quoted above; that is the record OF the defect, not a thing to repair.
* **The number `contract-v3.1` is never reused.**
* **NOTHING IS DECLARED SPENT BY THIS CUT, and `contract-v3.1` is not in that
  state.** That state is reserved for a number that was cut and can NEVER be
  published; `contract-v3.1` WAS published, tag and all. It is DEFECTIVE and
  SUPERSEDED — the state § *Immutable Tag Correction* describes — and this cut
  writes no declaration of the other one.

### Publication

The annotated tag `contract-v3.2` is published at the exact commit this cut
lands on `origin/main`, and NOT before `verify-commit --commit <merge-sha>`
passes there. That is § *Bundle Realization Order* step 5 preceded by step 4,
which is the pair whose separation produced the defect this entry records.

## contract-v3.1 — 2026-09-03 (additive; add-project-repo-schema's project-register election and its openRepoShape consumption pin are realized)

Realizes `add-project-repo-schema` **`tasks.md` 9.3** — *"Cut the next additive
contract bundle carrying `scripts/validate-ideation-dashboard-contracts.py`'s
new bytes … Until it is cut, `release-inventory-drift` reporting that validator
is the EXPECTED between-cuts state"* — the archive blocker that packet's own
realization left to the cutting session, exactly as `contract-v2.5`'s cut left
`add-signed-execution-chain`'s tranche-one registration to its own. The packet
was ratified 2026-09-02 by Brett Heap, the convener, in the working session,
verbatim *"ratify it"* (record:
`openspec/changes/archive/2026-09-03-add-project-repo-schema/review/ratification-2026-09-02.md`,
the change having archived alongside this cut in the same pull request).

**Change class: ADDITIVE (minor)** under
[`docs/contract-versioning-policy.md`](../docs/contract-versioning-policy.md) §
Change Classes. MEASURED RATHER THAN CLAIMED: `git diff --name-status
contract-v3.0 HEAD -- contracts/schemas/project-register.schema.yaml
scripts/validate-ideation-dashboard-contracts.py` shows the schema gaining
three OPTIONAL fields (`schema`, `reference`, `repository_roles`) with
`repositories` items unchanged as strings, and the validator gaining four new
WARNING/ERROR rules over those new fields alone
(`check_project_schema_election`) with no existing rule's behaviour altered. A
project declaring nothing is accepted exactly as before — packaged in
`tests/ideation_dashboard/test_project_schema_election.py`'s own assertion of
it — so no consumer pinned at `contract-v3.0` is made non-conformant by this
release.

### The number, fresh-counted at the cut

`contracts/manifest.yaml:3` declared `contract-v3.0`; `contracts/releases/`
held inventories through `contract-v3.0.digests.yaml`; the annotated tag
`contract-v3.0` is published; this changelog headed at `contract-v3.0` with no
`Unreleased` block pending. `grep -rl project-repo-schema
contracts/releases/contract-v3.0.digests.yaml` finds nothing, so `contract-v3.0`
covers none of this family. The next available additive number is
**`contract-v3.1`**, taken here. **NOT `contract-v3.0.1` OR ANY OTHER
SUB-MINOR**: § Version Identity's tag form is `contract-v<major>.<minor>`
exactly, with no third component, and every prior additive release under a
major has advanced the minor (`contract-v2.0` → `contract-v2.1` … →
`contract-v2.5`) rather than a component this scheme does not declare.

### What this release adds, atomically with the manifest bump

The four artifacts `add-project-repo-schema` §*What this change realizes IN
THIS PULL REQUEST* names, of which exactly ONE is a registered release member
and the other three are measured NOT to be (proposal `target_release`, and
re-measured identically here: zero occurrences of either file in
`contracts/manifest.yaml` or in `contracts/releases/contract-v3.0.digests.yaml`):

* [`docs/project-repo-schema.md`](../docs/project-repo-schema.md) — the
  doctrine: the project/spec/code/assembly shape is ELECTIVE and CONFERS
  NOTHING, the four naming families, the double pin and its lockstep
  invariant, the manifest-is-the-source rule, the bootstrap contract and its
  degrade line, and the ownership split between this document, the neutral
  `opensoft/openRepoShape` standard, and codexFactory's engineering overlay.
  Not a registered contract; a governance document.
* [`contracts/openreposhape-pin.yaml`](openreposhape-pin.yaml) — openxFactory's
  consumption of `opensoft/openRepoShape` at commit
  `deacbdcce4f52af427bcb4edd075fcc992e3dabe`, in the
  `kind: pinned_contract_manifest` grammar `openxwallet-pin.yaml` already
  established: sixteen per-file `sha256` digests plus eighteen
  `pinned_by_commit_only:` members, covering all thirty-four files present at
  the pinned commit so none is an undeclared consumption. Not a registered
  release member, on the same terms as `openxwallet-pin.yaml`: a pin file
  records a CONSUMPTION, not a contract this repository authors.
* `scripts/validate-openreposhape-pin.py` +
  `.github/workflows/openreposhape-pin-gate.yml` — the running check, on the
  `openxwallet-consumer-gate.yml` pattern: five ordered checks (shape,
  revision, digests, presence, surface completeness), six named refusal
  codes, one fixed remediation trailer, no gitlink comparison because
  openxFactory cites the standard rather than mounting it. RE-VERIFIED at this
  cut against the real bytes via `--from-gh`:
  `OK openreposhape-pin verified: opensoft/openRepoShape@deacbdcce4f5…, 16
  digest(s) recomputed, 18 member(s) present, 34 file(s) declared with none
  undeclared`, exit 0.
* **`scripts/validate-ideation-dashboard-contracts.py`** — the ONE registered
  row this bundle moves (`artifact_id: scripts-validate-ideation-dashboard-
  contracts.py`, `contracts/releases/contract-v3.0.digests.yaml:1417`), for
  `check_project_schema_election` and the four rules it adds over
  `contracts/schemas/project-register.schema.yaml`'s new fields:
  `project-role-unknown-repository`, `project-duplicate-repository-role`,
  `project-multiple-assembly-roles`, `project-reference-without-schema`. The
  schema file itself is NOT a registered row (measured above) so its own bytes
  moving raises no digest obligation independent of the validator's.

**Also re-baselined at this cut, and disclosed rather than left implicit:**
[`docs/contract-versioning-policy.md`](../docs/contract-versioning-policy.md)
is a NORMATIVE_DOCS release member and its bytes moved since `contract-v3.0`
— PR #577 (`2898b10`), recording the `contract-v2.6` "Instance Six" disposition
in the pinned policy document itself. That edit is UNRELATED to
`add-project-repo-schema`; it is exactly the "known and accepted cost" #577's
own commit message names — a non-editorial member drifting between cuts,
carried forward unchanged and re-baselined by whichever cut comes next. This
one does. No content is altered by the re-baseline; the digest simply now
matches what has been on `main` since 2026-09-02.

**AND THAT DOCUMENT MOVES A SECOND TIME AT THIS CUT, FOR A REASON OF ITS OWN.**
[`docs/contract-versioning-policy.md`](../docs/contract-versioning-policy.md)
gains a new subsection, *The SPENT State — a Cut Number That Can Never Be
Published*, under § *Immutable Tag Correction*. That is
`declare-spent-bundle-state`'s task **3.1**: the obligation-side DEFINITION of
the SPENT state — the third state between published and owes-a-tag, its
reserved single-line declaration form and the entry that must contain it, the
successor guard in all three of its conjuncts, and the three severities the
`release-tag-publication` family reports it at. OD-6 routed that paragraph to
*"the next contract cut"* and Brett Heap affirmed the routing on PR **#587**
(2026-09-03T02:49:08Z): *"Task 3.1 (policy-side SPENT paragraph in
`docs/contract-versioning-policy.md`) deferred to the next cut per OD-6's shape
argument: affirmed."* **THIS IS THAT CUT.** The consumer-facing half is NOT
re-authored here: #577 recorded the supersession as Instance Six and the new
subsection cites it rather than restating it, *"two records of one measurement
is how they drift apart"*.

**THE TWO MOVEMENTS IN THIS ONE FILE ARE DISTINCT, AND THE PARAGRAPH ABOVE IS
ABOUT THE FIRST.** #577's bytes are carried forward with no content altered;
this cut's bytes are content deliberately ADDED. ONE rebuilt inventory
re-baselines both, which is why `docs-contract-versioning-policy.md`'s digest
in [`contract-v3.1.digests.yaml`](releases/contract-v3.1.digests.yaml) records
the policy document's bytes AS CUT rather than as `contract-v3.0` recorded
them — and that re-baseline is what discharges `declare-spent-bundle-state`
§ 3.2, under which this changelog's editorial drift `info` and the policy
document's `release-inventory-drift` ERROR *"both clear on their own when the
inventory re-baselines"*.

**NOTHING IS DECLARED SPENT BY THIS CUT.** `contract-v2.6`'s declaration stands
exactly where it was written, inside § `contract-v3.0`'s own entry below, and
this cut neither adds a declaration nor edits one. DEFINING the state and
PERFORMING it are different acts, and only the first happens here.

### Realization evidence

`MedxSoft/MedxScribe` (2026-09-02, against openRepoShape `deacbdc`) is a
TEMPORARY PILOT — Brett Heap, 2026-09-02: *"MedxScribe is only a temp pilot
project right? it is not a real project. make sure it noted as pilot to test
the openRepoShape"* — and is not counted as an adoption. The adoptions counted
are real, dated 2026-09-03 and post the pin's `update-shape` re-sync at
`opensoft/openRepoShape@51836ba` (`v0.3`): `MedxSoft/MedxEHR` converted in
place (legs `MedxEHR-spec`, `MedxEHR-code`; assembly root `f1e07bd`) and
`MedxSoft/MedxGlass` scaffolded as a declared descendant of `openGlass`
(assembly root `a0e1897`), both bootstrap-verified. Full evidence:
`openspec/changes/archive/2026-09-03-add-project-repo-schema/tasks.md` § 9.3.

### Not part of this bundle

`docs/project-repo-schema.md`'s own `Status: ratified` (not `standard`, not
owed until the capability promotes) is unchanged by this cut. The successor
work `add-project-repo-schema` §*What is PENDING* names — the codexFactory
engineering overlay, OpsxFactory organisation/topic administration, and any
aggregation `project-register.yaml` row for an electing project — is each a
change in its own repository and none is realized here.

**Superseded by `contract-v3.2` (defective inventory: two digests stale at
the tag) — see the v3.2 entry above.** Nothing in this entry is rewritten and
nothing it describes is withdrawn: the release it records was published, its
tag stands as immutable provenance, and its number is never reused.

## contract-v3.0 — 2026-09-02 (BREAKING; three retirements execute, chain-attestation's content is carried, and `contract-v2.6` is superseded unpublished)

**THIS ENTRY NAMES EVERY ACT THAT LANDS AT THIS MAJOR**, in the words
[`docs/contract-versioning-policy.md`](../docs/contract-versioning-policy.md)
§ Deprecations Currently In Force uses of its own major-bound entry, because a
reader at `contract-v3.0` must be able to learn from ONE place what this major
refuses that `contract-v2.5` accepted. The list is written in both directions:
what landed, and what named this major and did NOT.

| # | act | where it landed | class |
|---|---|---|---|
| 1 | The `hermes` flat-key FALLBACK READ leaves the canonical domain-factory conformance validator, `LEGACY_HERMES_KEYS` with it, and the domain-starter generator stops EMITTING the deprecated keys | PR **#562**, squash `a951be76` | REMOVAL (Breaking) |
| 2 | The `openworkflow`-prefixed `owner_layer` compatibility branch leaves the same validator, with its docstring line | PR **#562**, squash `a951be76` | REMOVAL (Breaking) |
| 3 | The doxBench chat-turn **v1** envelope family (`workbench-chat-turn`, `-success`, `-failure`) leaves `contracts/schemas/xfactory-workbench-chat-turn.schema.yaml`, with its `deprecated_envelopes` block, the runtime and validator dispatch, twelve packaged fixtures and the byte-identity baseline test | PR **#564**, squash `6856f502` | REMOVAL (Breaking) |
| 4 | `add-chain-attestation` tranche two — eight new schemas, four shipped schemas extended additively, the tranche-two corpus and the extended reader | PR **#556**, squash `518c670b` | ADDITIVE, carried from the never-published `contract-v2.6` |
| 5 | The three deprecation-section moves: Executed rows for acts 1–3, and the flat KEYS' In Force entry restated to `contract-v4.0` with the recorded reason | PR **#562** (acts 1, 2 and the restatement) and THIS CUT (act 3) | policy record |
| 6 | NO `contract_schema_version` moves at this major — set, manifest rows and contract files alike (OQ-2, answered by measurement below) | THIS CUT, as a recorded decision | metadata |
| 7 | The doxBench consumer pin's `CONTRACT_TAG` off its knowingly stale `contract-v2.2` | THIS CUT | consumer pin |
| 8 | `contract-v2.6` recorded as a SPENT, never-verifiable, never-published number, SUPERSEDED here | THIS CUT | release record |
| 9 | `add-requirement-ref-resolution-integrity` — the two `requirement-ref-*` WARNING codes and their packaged probes, PUBLISHED at this bundle (its entry's owed `Warned since`, filled in here) | PR **#570**, squash `e01561c5` | DEPRECATING (minor) |

**AND ONE ACT THAT NAMED THIS MAJOR AND DID NOT LAND**, recorded here because
the sentence above is worthless if it is only true of the things that
succeeded: the `add-binding-consumer-identity` `consumer:` block's EIGHT
constraining acts, whose In Force entry read *"DECLARED at contract-v2.4 and
CONSTRAINED at contract-v3.0"* and *"Warned since contract-v2.4; removal target
contract-v3.0"*. Not one of them was authored — `scripts/validate-credential-contracts.py`
still emits all eight codes as WARNINGS, measured at this tip — and the
requiredness among them is additionally gated, by that entry's own text, on a
degraded fetch-identity mode this contract family cannot yet declare. So the
entry is **RESTATED to `contract-v4.0`** in this cut with that reason recorded,
under the ratified requirement *"A deprecation is EXECUTED at the major it
targets, or its entry is RESTATED with the reason it stays"*
(`retire-hermes-flat-keys-and-openworkflow-tokens`,
`specs/contract-deprecation-execution/spec.md`), whose scenario *"The target
arrives and the removal is not taken"* makes leaving the spent target *"a
defect of that cut rather than a neutral omission"*. Restating a removal
target LATER can only widen what is accepted; it refuses nobody, and the
warning window it re-serves is the same window.

**AND A SECOND ENTRY MOVES WITH IT, FOR A DIFFERENT AND STRICTER REASON.**
`add-requirement-ref-resolution-integrity` landed on `main` at `e01561c5`
NINETY MINUTES AFTER THIS CUT'S FIRST BRANCH POINT and hours before its merge,
declaring two more acts *"at contract-v3.0"*: a `consumer.requirement_ref` that
resolves to ZERO requirements (`requirement-ref-unresolved`) or to MORE THAN ONE
requirement of the one document it names (`requirement-ref-ambiguous`) is
REFUSED at that major. **Its own entry left `Warned since` deliberately blank
and owed to *"THE CUT THAT PUBLISHES THESE CODES"* — and that cut is this one.**
So the two versions collide on one bundle: `contract-v3.0` is the release that
first SERVES these warnings, and § Change Classes, *Breaking (major)* requires
*"at least one full minor release where the old shape produced deprecation
warnings"* BEFORE the major that refuses. **A warning first served at the bundle
that refuses is not a window at all**, so this is not a judgment the cut
exercised but an arithmetic it could not avoid. The entry is filled in as
`Warned since contract-v3.0` and its removal target RESTATED to
`contract-v4.0`.

**THE TWO RESTATEMENTS ARE ONE ACT, and separating them would have broken a
property that entry just bought.** It states that its removal target is *"the
SAME major the consumer block's seven acts land at, so a consumer serves ONE
deprecation window rather than two."* Moving one entry and not the other would
split that window in two. Both move to `contract-v4.0`, so a consumer still
serves ONE window and still upgrades once — one bundle later than either entry
expected, and with the window actually served rather than merely declared.
`scripts/validate-credential-contracts.py` is UNCHANGED by this cut in either
family: all ten codes remain warnings, exactly as they were at `e01561c5`.

### The number, FRESH-COUNTED at the cut, and why it is a MAJOR rather than `contract-v2.7`

Counted at the FINAL integration point `e01561c588d99c3b55b0304d584878a8cc890c7e`
(`origin/main` tip), not inherited. **THE COUNT WAS TAKEN TWICE, and the second
time is the one that governs**: the cut first branched at `bbbbeda9`, `main`
then moved under it (PR #570, `e01561c5`), and § Bundle Realization Order step 1
was performed rather than skipped — REBASE onto the final integration point,
then recheck. That is precisely the step whose omission made `contract-v2.6`
unpublishable, and the recheck found a real change rather than a formality (see
the act that did not land, above). Both readings agree on the number:

* `contracts/manifest.yaml:3` declared `contract-v2.6`.
* `contracts/releases/` held inventory files through `contract-v2.6`.
* `git ls-remote --tags origin 'refs/tags/contract-v*'` publishes
  `contract-v1.7` … `contract-v2.5` and **NO `contract-v2.6`**.
* This changelog headed at `contract-v2.6`. No Unreleased block is pending.
* `git ls-remote origin 'refs/tags/contract-v3.0'` is **empty** — the name is
  free.
* The only first-parent commit between the two readings is `e01561c5`, which
  moves no `contract_bundle_version`, writes no inventory and publishes no tag;
  it is a DEPRECATING (minor) code surface whose own entry hands its bundle
  number to this cut. So it changes the count's inputs not at all and its
  content substantially, which is the difference between rebasing and merely
  re-reading.

**THE CLASS RULE, NOT PREFERENCE, PICKS THE MAJOR.** § Change Classes,
*Breaking (major)* is entered when *"a shape is removed"*, and three shapes were
removed on `main` at 2026-09-01T19:43Z by `a951be76` and `6856f502` — a
`layers`-less `stack.yaml` (refused where it resolved), an
`openworkflow`-prefixed unresolvable `owner_layer` (refused where it warned),
and the three v1 chat-turn envelopes (refused where they validated). From that
moment no MINOR number can honestly be declared on this tree: a minor asserts
that *"domain repos on the same major version remain conformant without
changes"*, and this tree refuses shapes `contract-v2.5` accepted. `contract-v2.7`
would carry the same defect `contract-v2.6` carries. The next available number
of the class the tree actually requires is **`contract-v3.0`**, and this cut
takes it.

### Change class: BREAKING (major) — the three preconditions, each discharged and each checkable

§ Change Classes, *Breaking (major)* requires three things of every removal.
They are discharged per removal rather than in aggregate, because the three
removals served their warnings at three different releases.

| removal | (a) migration note | (b) a full minor in which the OLD SHAPE PRODUCED warnings | (c) the conformance validator accepts the new shape and rejects the old one ONLY at the new major |
|---|---|---|---|
| the `hermes` flat-key FALLBACK READ | § *What is removed* below, and `docs/contract-versioning-policy.md` § Deprecations Executed | **`contract-v1.1`**, which introduced `hermes.layers` and began warning on a stack declaring none — forty-plus minors, and the refused shape IS the warned shape: the warning fired on a `hermes.layers`-less stack and nothing else | discharged by a REPLACEMENT and not a deletion — `scripts/validate-domain-factory.py` emits ONE explicit error naming the missing or non-list `hermes.layers`, because deleting the fallback arm alone would have let a `layers`-less stack fall through to an EMPTY layer map and produce no finding at all, a silent WIDENING at a major |
| the `openworkflow`-prefixed token branch | § *What is removed* below, and the Executed row | **`contract-v1.1`**, which introduced the replacement token `xfactory` and began warning on the prefix | discharged in the validator itself: it accepts a canonical role, a declared layer's display name, `omnigent`, `<domain>_omnigent` or `xfactory`, and rejects the old token only from `contract-v3.0`, through the general undeclared-layer rule |
| the doxBench chat-turn **v1** family | § *What is removed* below, and the Executed row | **`contract-v1.34`**, which deprecated the family MACHINE-READABLY in a top-level `deprecated_envelopes` block; the warnings were real and were still firing at the removal — `python3 scripts/validate-ideation-dashboard-contracts.py` reported **`0 error(s), 4 warning(s)`** on `main` at `af746459`, one per packaged v1 fixture, and reports **`0 error(s), 0 warning(s)`** at this cut | discharged by the schema and the delegated validator together: the surviving `-v2` family is accepted unchanged, a v1 instance is refused only from `contract-v3.0`, and the machine-readable deprecation READER is KEPT (it now reports `{}`, which is the correct report and not a defect) so the NEXT deprecation is not inert |

**A PINNED CONSUMER IS UNTOUCHED, and that is § Compatibility Direction rather
than a courtesy.** A domain repository pinned at or below `contract-v2.5` reads
the validator, the schema and the branch AT ITS OWN PIN, where all three are
still present and still warn. Nothing in this release reaches backwards.

**WHO THIS MAJOR ACTUALLY REFUSES, MEASURED.** All five supported
DomainxFactory consumers — codexFactory, MedxFactory, AdxFactory,
LedgerxFactory, OpsxFactory — declare `hermes.layers`, so removal 1 refuses
none of them; there is not one `openworkflow`-prefixed `owner_layer` token in a
workflow gate across ten reachable repositories, so removal 2 refuses none of
them; and the only v1 chat-turn instances that existed were openxFactory's own
four packaged fixtures, so removal 3 refuses no consumer either. **This major
refuses shapes, not repositories** — which is why it may be taken, and is not a
reason to have taken it silently.

### What is removed

* **The `hermes` flat-key FALLBACK READ — the READ, and NOT the keys.** The
  branch of `scripts/validate-domain-factory.py` that resolved layer overlays
  and display names from flat keys under `hermes:` when `hermes.layers` was
  absent, the `LEGACY_HERMES_KEYS` map it read them through, the per-role
  `no overlay resolvable for hermes role` check that followed it, and
  `scripts/apply-domain-starter.py`'s emission of the deprecated keys into
  every newly instantiated domain repository. **Migration**: declare
  `hermes.layers` with exactly one template for each canonical role
  `customer`, `client` and `domain`, each carrying `display_name` and
  `overlay` — the shape
  `contracts/schemas/xfactory-domain-stack.schema.yaml` requires and the
  domain-starter generator now emits alone. **THE CO-RESIDENT KEYS ARE NOT
  REFUSED**; their entry stays in § Deprecations Currently In Force, restated
  to `contract-v4.0`, because the warning fired ONLY in the `layers`-absent
  branch and all five supported consumers carry the keys ALONGSIDE
  `hermes.layers` — a shape that has never produced a warning against any of
  them, so refusing it would be an UNPHASED narrowing. That measurement, and
  the deprecating minor it owes, are in the entry itself.
* **The `openworkflow`-prefixed layer/owner token compatibility branch**, with
  the validator docstring line that advertised it. **The removal is ONE
  CHARACTER WIDER than the entry used to declare**: the entry and the docstring
  both wrote `openworkflow_`, the code wrote `token.startswith("openworkflow")`,
  so `openworkflow`, `openworkflowx` and `openworkflow-legacy` all took the
  branch and are all covered. **It NARROWS one case and WIDENS another**,
  because the removed `if` PRECEDED and shadowed the general
  `elif token not in allowed`: a prefixed token resolving to nothing was warned
  and is now reported by the general undeclared-layer rule; a prefixed token
  whose normalized form EQUALS a declared layer's normalized display name was
  also warned and now validates SILENTLY. Both were measured on the two
  validators side by side. **Migration**: replace the token with `xfactory`,
  the replacement `contract-v1.1` introduced.
* **The doxBench chat-turn v1 envelope family** — `$defs/request`,
  `$defs/success`, `$defs/failure` and their three `oneOf` refs in
  `contracts/schemas/xfactory-workbench-chat-turn.schema.yaml`, the top-level
  `deprecated_envelopes` block and its comment, the three kind→schema rows and
  three tag-dispatch arms in `scripts/validate-ideation-dashboard-contracts.py`,
  the v1 arm of `serve.py`'s kind discrimination, four positive and eight
  negative packaged fixtures, and the byte-identity baseline test.
  **Migration**: send `workbench-chat-turn-v2`; the conversion applied uniformly
  to this repository's own corpus is `kind` → `workbench-chat-turn-v2`,
  `active_document_path` DROPPED and `bound_buffer` declared in its place per
  design D17's *"stated, never inferred"*, with `observed_hashes` keyed by
  buffer key and `typed_proposal` replaced by `keyed_typed_proposal` on the
  success envelope. Every one of the SEVEN v1-only refusal classes was
  re-expressed as a `-v2` negative and NONE was lost — escaping path, hash
  mismatch, identity subject, over budget, unknown model, untyped proposal and
  duplicate turn pair, each run through `validate_instance` individually and
  each refusing for the INTENDED reason.
  **THE `serve.py` FALLBACK IS REDESIGNED, NOT DELETED**: an unrecognized or
  absent `kind` is refused in the SURVIVING family's failure envelope carrying
  the new `unrecognized_turn_kind` code (400) where a wire-valid
  `client_turn_id` exists, and in the existing pre-identity shape where it does
  not. A retired v1 kind takes exactly that path, which is the ruled
  consequence: after the removal a retired kind and a kind that never existed
  are the same fact about the wire.
  **THE BASELINE TEST'S RETIREMENT IS NAMED RATHER THAN ABSORBED**, as the
  packet's D4 requires. `test_the_v1_envelope_bytes_are_unchanged_by_the_release`
  and its `chat-turn-v1-envelopes.baseline.yaml` fixture existed to prove the
  deprecated bytes never moved. They end because the shape they protect leaves
  the published surface and the assertion has no subject — `_v1_ref_closure`
  would raise `KeyError` on its own seed rather than fail an assertion. A
  consumer pinned below `contract-v3.0` keeps the promise it was given, and
  keeps it by the IMMUTABILITY OF THE BYTES ITS PIN NAMES rather than by their
  continued presence here.

### What is carried forward from the never-published `contract-v2.6`

`add-chain-attestation` tranche two landed on `main` as PR #556, squash
`518c670b`, and was registered in `contracts/manifest.yaml` there — thirteen
rows, eight new and four refreshed — because that family's own required
manifest-row digest test refuses a moved schema whose row did not move in the
SAME commit. The NUMBER was claimed by `contract-v2.6`, which is never
published (below). **The CONTENT is carried here unchanged; only the number it
is registered under moves.** Not one of the eight new schemas, the four
extensions, the tranche-two corpus or the extended reader is re-cut, re-signed
or edited by this cut.

* **Four shipped schemas extended, additively** —
  `digest-construction.schema.yaml` gains ELEVEN digest subjects and NO second
  construction; `chain-inception.schema.yaml` gains the OPTIONAL
  `amendment_lineage` block inside the signed bytes, REQUIRED BY THE READER for
  any chain carrying tranche-two records; `transparency-log-leaf.schema.yaml`
  gains seven leaf types and the extended closed refusal enumeration;
  `conformance-declaration.schema.yaml` gains SEC-R10..SEC-R18 and the
  `attestation_design` block.
* `contracts/signed-execution-chain/` — **eight NEW schemas, links 4–6 and
  10**, each with a per-file `sha256` row: `attestation-common.schema.yaml`,
  `setup-attestation.schema.yaml`, `commitment-extension.schema.yaml`,
  `signed-chain-binding.schema.yaml`, `runner-attestation.schema.yaml`,
  `pr-open-decision.schema.yaml`, `closure-record.schema.yaml` and
  `remediation-declaration.schema.yaml`.
* `scripts/signed_execution_chain/attestation.py` — the tranche-two walk of THE
  SAME NAMED READER: links 1–6 as eleven ordered checks in the ONE walk (org
  ruleset **21957695** unchanged), **ninety-five closed refusal codes, every one
  red-proven** over two packaged corpora, 74 tranche-two negatives and four
  positive chains.
* **What it does NOT operate**: no certificate authority, no minted tier-2
  identity, no held private key, no running omnigent layer. SEC-R18 stays
  declared UNMET (`execution_layer_ordering: not_enforced`), and the packet's
  §5.1–5.3 machinery gates and its §5.8 canary pair stay OPEN.

**THE ADDITIVE CLAIM IS RE-MEASURED OVER THE LANDED TREE, AND IT IS NOW TWO
CLAIMS RATHER THAN ONE.** The `contract-v2.6` entry measured *"ADDITIVE
(minor) … nothing narrows"* with `git diff --name-status contract-v2.5
518c670b -- contracts/` — a tree in which `6856f502` had not yet removed the v1
chat-turn schema. Re-measured here against what actually landed, the two facts
are ATTRIBUTED SEPARATELY and never merged:

1. **Chain-attestation's own content is additive and narrows nothing**, and
   that survives the re-measurement intact, because its surface and the
   retirements' surface are DISJOINT: `518c670b` touched
   `contracts/signed-execution-chain/**` plus four editorial registration
   files; `a951be76` and `6856f502` touched neither. No member any of the four
   extended schemas published was removed, renamed or narrowed; the shipped
   tranche-one corpus validates green under the extended schemas in the same
   required check that walks the new corpus; the shipped nine-entry conformance
   declaration stays valid because the obligations enumeration widened as
   `minItems: 9, maxItems: 18`.
2. **The NARROWING at this bundle is the three retirements' and theirs alone.**
   It is what makes this a major. Attributing it to chain-attestation would be
   false; folding it into a single "additive" verdict for the bundle would be
   worse, because it would make the major's own reason invisible.

A consumer that pinned `contract-v2.5` for the signed-execution-chain family
and nothing else can adopt every byte of item 1 by upgrading, and pays for the
retirements only if it holds one of the three refused shapes.

### `contract-v2.6` disposition — DECLARED, NEVER VERIFIABLE, NEVER PUBLISHED, SUPERSEDED HERE

Modelled on this changelog's § `contract-v2.3` disposition, which recorded a
declared-but-untagged bundle honestly and left the tag to its owner. **The fact
here is stronger and the disposition is therefore different**: `contract-v2.3`
was untagged but VERIFIABLE, and its tag was published four days later at the
commit the targeting rule names. `contract-v2.6` can never be.

* **DECLARED** at `bbbbeda984353ebaeb67d3e2bb1c73fcb7bac140` — the squash of PR
  **#565**, `add-chain-attestation` task 5.9's cut half — by three artifacts:
  `contracts/manifest.yaml`'s `contract_bundle_version`, its changelog entry
  above, and `contracts/releases/contract-v2.6.digests.yaml`.
* **NEVER VERIFIABLE.** `python3 scripts/validate-contract-release.py
  verify-commit --commit bbbbeda9…` returns FIVE
  `HGR-RELEASE-DIGEST-MISMATCH` findings, exit 1 —
  `contracts/CHANGELOG.md`, `contracts/manifest.yaml`,
  `contracts/schemas/xfactory-workbench-chat-turn.schema.yaml`,
  `docs/contract-versioning-policy.md` and
  `scripts/validate-ideation-dashboard-contracts.py`. **The CAUSE is
  § Bundle Realization Order step 1**: the branch `cut/contract-v2.6` forked at
  `518c670b` and was never rebased onto the final integration point, and a
  squash merge takes `main`'s tree and applies the PR diff — so the landed
  commit carries five release-surface members the reviewed candidate `07986003`
  never saw, moved by `a951be76` (#562) and `6856f502` (#564), both merged
  four hours BEFORE that candidate was committed. Two of the five are the
  editorial members § *What a red `verify-commit` at HEAD means* allows between
  cuts; **three are not** — a normative schema, this policy's own versioning
  document, and a validator — and the allowance does not reach a tag in any
  case: *"a published bundle must verify at its own commit exactly."*
* **NEVER PUBLISHED, and the name is still free.** No annotated tag object was
  ever created and none was pushed; `git ls-remote origin refs/tags/contract-v2.6`
  is empty. The post-merge checklist was run in order from an independent clone
  and **STOPPED at step 2**, which is the release machinery doing exactly the
  job it exists for. The full measurement is PR #565 comment `5502452624`; this
  entry cites it and does not re-derive it, because two records of one
  measurement is how they drift apart.
* **NO COMMIT CAN CARRY THE TAG, EVEN AFTER A REBUILD.** The targeting rule is
  *"the EARLIEST FIRST-PARENT COMMIT on published `main` that DECLARES the
  bundle and at which `verify-commit` PASSES."* Exactly one first-parent commit
  declares `contract-v2.6` and `verify-commit` fails there; `07986003` is not
  reachable from `origin/main`. A completion commit — the
  `contract-v1.31`/`-v1.36`/`-v1.37` shape — could have supplied a target for a
  digest rebuild, and would still not have cured the second defect.
* **THE SECOND DEFECT NO COMPLETION COMMIT CAN CURE, and it is the one that
  settles the disposition.** `contract-v2.6` declares change class **ADDITIVE
  (minor)**. From 2026-09-01T19:43Z the tree it declares on REFUSES three shapes
  `contract-v2.5` accepted. A minor asserts that consumers on the same major
  remain conformant without changes, and on that tree the assertion is false. A
  rebuilt inventory moves five digest lines and moves that not at all.
* **SUPERSEDED, at the same surface, by this bundle.** Everything
  `contract-v2.6` was to have carried is carried here under a number whose class
  matches the tree. **The number is SPENT and is never reused**, on the terms
  § Immutable Tag Correction sets for a version number: *"its version number is
  never reused."* `contracts/releases/contract-v2.6.digests.yaml` and the
  `contract-v2.6` entry above are **left exactly as written and are not
  edited** — they are the record of what was declared and of what was true when
  it was written, on the same footing as
  `docs/archive-record-discrepancies.md` and as the `contract-v2.3` PENDING
  heading. A reader who arrives at that entry should read on to here.
* **THIS IS INSTANCE SIX of the shape #528 tracks**, and it is a different
  shape from the first five: those were bundles whose tags nobody published;
  this is a bundle whose tag nobody COULD publish. The step this cut takes to
  avoid repeating it is the one whose omission killed `contract-v2.6`:
  § Bundle Realization Order **step 4**, rerun on the promoted commit BEFORE any
  tag.

**AND THE CHECK #528 ASKED FOR NOW EXISTS, READS THIS BUNDLE, AND HAS NO
VOCABULARY FOR IT — WHICH THIS ENTRY DECLARES RATHER THAN LEAVES TO BE HIT.**
The `release-tag-publication` doc-health family
(`scripts/doc_health/release_tag_publication.py`) inspects EVERY bundle with a
release inventory, not only the declared one. Today it reports `contract-v2.6`
at **WARNING** — *"declared and has no published annotated tag, 1 first-parent
landing(s) after the commit that declared it"* — and
`tests/doc-health/test_release_tag_publication.py::test_this_repository_reads_zero_and_the_probe_can_fire`
is consequently **RED ON `main` ALREADY**, before and independently of this cut,
which reads `origin/main` rather than any branch. **What this cut changes is the
SEVERITY, permanently**: once the manifest declares `contract-v3.0`,
`contract-v2.6` becomes a SUPERSEDED bundle and the family reports it at
**ERROR** without grading — *"cut and SUPERSEDED without ever being published"* —
and the action it prescribes, *"publish the annotated tag at the commit the
versioning policy's rule identifies"*, is UNPERFORMABLE for this bundle for the
two reasons above. Its closing clause, *"never edit the manifest, the changelog
or the inventory to match the absence"*, is exactly right and is obeyed here:
nothing was deleted to quiet it.

**THE FINDING IS TRUE. THE FAMILY IS NOT WRONG. IT SIMPLY HAS NO THIRD STATE**
between *published* and *owes a tag*, and a spent-never-publishable number is
that third state. **This cut does NOT weaken the family to fit the ruling**, and
the reason is the ruling's own scope: Brett Heap ruled that `contract-v3.0`
supersedes `contract-v2.6`, not that a checker should stop objecting to
abandoned bundles — the shape of any such vocabulary (what record counts as a
supersession, who may declare one, whether it is `contested` and needs a
disposition entry) is design work that owes its own change and its own review,
and a release cut quietly relaxing the one check that exists to stop bundles
being walked away from is precisely the failure that check was built for. It is
filed as **openxFactory issue #575**, which carries the measurement, why the cut
declined to take it, and the five things a disposition owes — including the
guard against the obvious abuse, that a bundle must never become spent by being
ignored. It is named here so a reader meeting the ERROR knows it is DECLARED
rather than undiscovered.

**AND THE STATE NOW EXISTS, SO THIS RECORD CARRIES ITS MACHINE-READABLE HANDLE.**
`declare-spent-bundle-state` was ratified on 2026-09-02 by Brett Heap and
realized in the PR that adds the line below (openxFactory **#575**). That line is
the reserved single-line form the `release-tag-publication` family reads, and it
is a **HANDLE ON THIS RECORD AND NOT A SECOND RECORD** — written inside the
disposition subsection this cut wrote anyway, in the pattern
`document-lifecycle`'s reserved `Modified over` marker already sets. Nothing
above it is edited: the ERROR is not silenced by an absence but answered by a
declaration, and what it becomes is ONE `info`, classed `contested`, on
`contracts/releases/contract-v2.6.digests.yaml`. **`contract-v3.0`'s own
annotated tag is what makes it quiet** — `git ls-remote origin
refs/tags/contract-v3.0` answers `59f4f51f…` peeling to `ff9ed815…` — so the
only way this number was retired was by publishing its replacement, which is the
act this family exists to compel.

**SPENT BUNDLE:** `contract-v2.6` — SUPERSEDED BY `contract-v3.0` — CAUSE: `contract-v2.6` declares change class ADDITIVE (minor) on a tree that refuses three shapes `contract-v2.5` accepted, and is never verifiable (five HGR-RELEASE-DIGEST-MISMATCH findings at `bbbbeda9`, the only first-parent commit that declares it), so the targeting rule has no legal target and no completion commit or rebuilt inventory can cure it — RULED BY Brett Heap, 2026-09-02 — MEASUREMENT: PR #565 comment `5502452624`

### OQ-1 and OQ-2, answered at the cut

Both retirement packets named these for the cutting session and neither
proposal answered them.

**OQ-1 — does `contract-v3.0` carry both retirement packets, or one?
BOTH.** They are independent by construction and either was legal alone. They
ride together because they landed together on `main` — `a951be76` and
`6856f502` merged in the same minute — so any bundle declared after that point
carries both narrowings whether it names them or not, and a cut that named one
would have under-declared its own refusal list.

**OQ-2 — is `contract_schema_version` incremented? NO — NOT the contract set's,
NOT any manifest row's, and NOT the one contract file whose shape narrowed. The
answer is three measurements, and the third is the one the cut got wrong first
and is recorded rather than smoothed over.**

* **The contract SET's integer does NOT move.** `contract-v2.0`, the only
  previous major, moved none. More decisively,
  `scripts/validate-domain-openxfactory-pins.py:92` HARD-CODES
  `"contract_schema_version": 1` as the value every domain `stack.yaml` must
  declare and ERRORS on any other, and all five supported consumers declare
  `1`. Moving it would ERROR all five at the major with no warning minor ever
  served — the exact unphased narrowing § Change Classes forbids and this
  bundle restated two entries to avoid. The Domain Upgrade Runbook's
  *"`contract_schema_version` if major"* is guidance to a consumer performing an
  upgrade, not a licence for the publisher to refuse the population.
* **No manifest ROW's `schema_version` moves**, and the estate's precedent shows
  the row and the file are independent: `contracts/schemas/consent-instrument.schema.yaml`
  carries `contract_schema_version: 2` while its manifest row still records
  `schema_version: 1`.
* **`contracts/schemas/xfactory-workbench-chat-turn.schema.yaml`'s own
  `contract_schema_version` STAYS 1 — AND THE ANSWER WAS ALREADY IN THE TREE,
  ARGUED, BEFORE THIS CUT ASKED THE QUESTION.** The realization (#564) wrote it
  into `tests/ideation-dashboard/test_doxbench_contracts.py` as an assertion
  with its reasoning beside it: *"The file's own version does NOT move. It did
  not move at contract-v1.34 because nothing previously valid became invalid
  (D16); it does not move here for the opposite reason — the envelopes this file
  no longer defines cannot be validated against it AT ALL, so there is no shape
  left for a bumped `contract_schema_version` to describe. What changed is which
  release a consumer pins, which is the major's own job."*
  `tests/ideation-dashboard/test_doxchat_model_intake.py` pins the same value.
  **THE CUT FIRST BUMPED IT TO 2 AND WAS REFUSED BY THOSE TWO TESTS, and that
  is recorded here rather than quietly reverted**, because the packet filed
  `contract_schema_version` to the cut *"per OQ-2's answer"* and the honest
  finding is that the realization had already answered it — in executable form,
  which is the strongest place an answer can sit. A cut is not the place to
  overturn a ratified realization's reasoned decision, and the measurement that
  would have justified doing so was itself wrong: the cut's claim that *"nothing
  in the repository reads it as a refusal input"* was made from a truncated grep
  and two tests read it.
  **SO NO INTEGER MOVES AT THIS MAJOR, AND WHAT CARRIES THE BREAK INSTEAD IS
  WHAT ALWAYS CARRIED IT**: the bundle version, the per-file `sha256` a consumer
  verifies, and this entry. The record ENVELOPES' `schema_version: { const: 1 }`
  are untouched in every surviving definition, as they must be — bumping those
  would invalidate every instance in the estate, the opposite of what this
  removal did.

### The consumer pin: `CONTRACT_TAG`, and the sentinel this cut deliberately re-introduces

`scripts/ideation_dashboard/doxbench_contracts.py` pinned
`CONTRACT_TAG = "contract-v2.2"` / `CONTRACT_REF = "8ccfb67b…"`, left knowingly
stale by the realization and owed to this cut. **It was already incoherent
before this cut touched it, which is the fact that decides the disposition**:
`6856f502` moved `SCHEMA_DIGESTS[CHAT_TURN_SCHEMA_FILE]` to the post-removal
bytes, so the module pinned bytes that belong to NO published release while
naming `contract-v2.2` as the release they came from. **This cut moves no
schema byte and re-derives no digest**: OQ-2 above answers that no
`contract_schema_version` moves, so `SCHEMA_DIGESTS` keeps the realization's
`350bfedc…` and what this cut changes is the LABEL beside it — which is the
whole of the repair, the label having been the incoherent half.

`CONTRACT_TAG` becomes **`contract-v3.0`** — the release these bytes actually
belong to — and `CONTRACT_REF` becomes **`unpublished:contract-v3.0`**, this
module's own established sentinel, used across the `contract-v1.34`,
`contract-v1.38`, `contract-v1.40` and `contract-v2.2` realization branches for
exactly this moment and for exactly this reason: the policy allocates the
version and builds the inventory AT REALIZATION and publishes the annotated tag
against the commit that actually LANDS, so until that commit exists there is
nothing honest to name. It is spelled so a consumer comparing against it REFUSES
rather than matching by accident, and the mechanism is the PIN VALIDATOR rather
than YAML: a repository can write the string, but
`scripts/validate-domain-openxfactory-pins.py` requires a 40-character
lowercase SHA for `contract_ref_type: commit`, so a stack carrying the sentinel
fails its own pin check and one carrying anything else fails the module's
equality check. The older comments in that module put this as *"a value no
`stack.yaml` can declare"*; that overclaims, and the correction is made here
rather than inherited.
**THE RESIDUE THAT MECHANISM ONCE LEFT IS NAMED SO IT IS NOT REPEATED**: the
`contract-v1.45` repin left `unpublished:contract-v1.45` standing for three days
after the tag was published. **Resolving this sentinel to the commit
`contract-v3.0` dereferences to is a POST-TAG act and is owed**, and it is
listed in this cut's pull request as a post-merge step rather than left to be
remembered.

### The `typed_proposal` disposition — RETAINED, and the false premise not carried forward

`retire-doxbench-chat-turn-v1` task 2.1 computed the SURVIVING family's
reference closure rather than inspecting it, and the computation returned a
surprise: the v1-only set is `request`, `success`, `failure` **and
`typed_proposal`**. `keyed_typed_proposal` RESTATES the shape with a buffer-key
target instead of `$ref`-ing `typed_proposal`, so the widened family never
points at it. The ratified requirement names `typed_proposal` among the shared
definitions that *"do NOT leave with the envelopes"* on the premise that it is
*"reachable from the surviving family"*, **and that premise is false**.

**DISPOSITION AT THE CUT: RETAINED, unreferenced, with the reason stated — and
the reason is a rule rather than caution.** Removing it here would be a
narrowing of a published contract file that NO deprecation entry ever
announced and NO minor ever warned on, which § Change Classes, *Breaking
(major)* forbids at this major as squarely as it forbids refusing the
co-resident flat keys. A removal of `typed_proposal` owes its own deprecating
minor first. The definition therefore stays, carrying at its own site the
measurement and this disposition, so the false reachability claim is not what a
reader finds standing at the major.

### Release surface, and the deprecation-section moves

* `contracts/manifest.yaml` — `contract_bundle_version: contract-v3.0`; the
  `xfactory-workbench-chat-turn` row's `sha256` unchanged from the realization's
  `350bfedc…` (OQ-2 moves no byte in that file) and its `consumption_rule` prose
  dropped of the v1 clauses it still carried
  (it described *"SIX closed envelopes"*, false the moment the v1 `$defs`
  left — raised by Copilot against the realization, filed to the cut at that
  packet's 6.1/6.2 rather than crossed twice).
* `contracts/README.md` — the `xfactory-workbench-chat-turn` row, which still
  described the v1 envelopes as byte-identical, still validating, and DEPRECATED
  with removal target `contract-v2.0`.
* `docs/contract-versioning-policy.md` — the doxBench chat-turn v1 entry LEAVES
  § Deprecations Currently In Force and arrives in § Deprecations Executed
  carrying all six elements the exemplar row establishes, closing *"Deprecated
  at contract-v1.34, removed at contract-v3.0."*; and the
  `add-binding-consumer-identity` `consumer:` entry is RESTATED to
  `contract-v4.0` with its reason, per the act that did not land, above, and
  `add-requirement-ref-resolution-integrity`'s entry has its owed `Warned since`
  filled in as `contract-v3.0` with its removal target restated to
  `contract-v4.0` beside it. **§ Deprecations Currently In Force now holds THREE
  bullets and not one of them names a spent target**; § Deprecations Executed
  holds FOUR rows. The
  Executed rows for the fallback read and the `openworkflow` branch, and the
  flat KEYS' restatement to `contract-v4.0`, landed in `a951be76` ahead of this
  cut — verified unchanged here, and § Deprecations Currently In Force now
  holds exactly two bullets, neither of which names a spent target.
* `tests/intent-compliance/test_release_boundary.py` — the release boundary is
  pinned by an ENUM OF NAMED BUNDLE VALUES and fails loudly on a bundle it has
  not been told how to classify. It fired on this bump, correctly.
  `contract-v3.0` is classified BY HAND and on the record: past the floor,
  family registered, family present, and the membership this file asserts is
  UNCHANGED — the three retirements touch no intent-compliance member. The enum
  gains ONE named member handled by the SAME match arms; no test is added,
  removed, renamed or weakened, and the next bundle trips it again.
* `contracts/releases/contract-v3.0.digests.yaml` — this cut's inventory, built
  by the canonical `build --tag contract-v3.0` AFTER every other member above,
  and never hand-edited. `contracts/releases/contract-v2.6.digests.yaml` and
  every earlier inventory are untouched.

### What this release does NOT confer

**The bundle is not published until its tag exists**, and at this entry it does
not. This cut declares `contract-v3.0`; the annotated tag is a separate act on
the commit that actually lands, taken only after § Bundle Realization Order
step 4 — every gate and review rerun against the promoted commit — has been
performed and verified from an independently refreshed checkout. That is the
step whose omission produced the disposition three sections above, and this
entry may not be cited as evidence that `contract-v3.0` is released.

`add-chain-attestation`'s §5.1–5.3 machinery gates and its **§5.8 canary pair**
remain OPEN and are honestly unticked; the canary needs the published tag and a
real pull request, and is not the cutting session's to close. Neither retirement
packet may archive on this cut alone: both carry a code surface, and under
`release-realization` they archive on merged plus green realization evidence
plus the published tag.

## contract-v2.6 — 2026-09-01 (additive; what actually ran, said by the chain itself)

Realizes `add-chain-attestation` **tranche two**, ratified 2026-09-01 by the
repository owner at `f54cb5bc` and RE-RATIFIED at `6d7ef17b` after the amendments
that head's own verdict forced
(`openspec/changes/add-chain-attestation/review/`). The code surface — the eight
new schemas, the additive extension of four shipped ones, the tranche-two
packaged corpus and the extended reader — landed as PR #556, squash `518c670b`.
THIS ENTRY IS `tasks.md` 5.9's cut half. The registration half (the thirteen
manifest rows) rode in #556 itself, because the family's own required
manifest-row digest test refuses a moved schema whose row did not move in the
SAME commit; the NUMBER stayed out of every contract byte until this cut, per
[`docs/contract-versioning-policy.md`](../docs/contract-versioning-policy.md).
THE NUMBER, FRESH-COUNTED AT THE CUT: at this tip `contracts/manifest.yaml:3`
declared `contract-v2.5`, `contracts/releases/` held inventories through v2.5,
`git ls-remote` published tags through contract-v2.5, the CHANGELOG headed at
v2.5, and the v2.5 inventory carries ZERO tranche-two rows — the two
`contract-v3.0` ratifications of #551/#552 are PROPOSAL-ONLY retirement packets
whose major waits behind its own deprecation window and reserves nothing here.
The next additive number available at that tip was therefore `contract-v2.6`,
and **`contract-v2.6` IS THE NUMBER THIS CUT TAKES** — the number counted here,
not one reserved for a later release.

**Change class: ADDITIVE (minor)** under
[`docs/contract-versioning-policy.md`](../docs/contract-versioning-policy.md).
`git diff --name-status contract-v2.5 518c670b -- contracts/` reports
**eighty-eight additions and nine modifications**, and the nine are measured
rather than waved at: FOUR are the editorial registration surfaces (this
changelog, `contracts/README.md`, `contracts/manifest.yaml`, the family README);
ONE is the packaged tranche-one conformance-declaration example, moved by the
already-landed #550 (`is_required_in_ruleset: true` — the declaration stopped
saying the reader is unrequired because it is required, a truth update and not a
shape change); and FOUR are the additive schema extensions this release is for.
NO MEMBER ANY OF THE FOUR PUBLISHED WAS REMOVED, RENAMED OR NARROWED, and the
non-refusal of prior instances is PROVED rather than argued: the shipped
tranche-one corpus — every positive of it byte-identical since v2.5 except the
#550 example — validates green under the extended schemas in the same required
check that walks the new corpus, and the shipped nine-entry conformance
declaration stays valid because the obligations enumeration widened as
`minItems: 9, maxItems: 18` with the eighteen-entry closure enforced by the
READER only for a declaration naming a tranche-two obligation. Every consumer
pinned at `contract-v2.5` stays conformant until it deliberately upgrades, and
`contract_schema_version` is unchanged.

### What this release adds

* **Four shipped schemas extended, additively** —
  `digest-construction.schema.yaml` gains ELEVEN digest subjects and NO second
  construction (the one way that file is meant to move, said in the file);
  `chain-inception.schema.yaml` gains the OPTIONAL `amendment_lineage` block
  (reviewed digest, ratified subject digest, review-record digest, amendment
  record reference) inside the signed bytes, REQUIRED BY THE READER for any
  chain carrying tranche-two records — optional in the shape because `required`
  would have refused every inception the v2.5 bundle accepts, which this
  policy classes BREAKING; the residual is DECLARED at the packaged
  declaration's SEC-R16 entry; `transparency-log-leaf.schema.yaml` gains seven
  leaf types and the extended closed refusal enumeration (a second digest
  construction has no code because it has no representation);
  `conformance-declaration.schema.yaml` gains SEC-R10..SEC-R18 and the
  `attestation_design` block carrying the three obligations a gate cannot see.
* `contracts/signed-execution-chain/` — **eight NEW schemas, links 4–6 and 10**,
  each with a per-file `sha256` row: `attestation-common.schema.yaml` (shared
  definitions by `$ref` — the signature block with THE SIGNER'S PUBLIC KEY
  CARRIED BESIDE IT, the predecessor hash link, the CLOSED three-member
  evidence class composing with the ratified trust-anchor chain-custody
  registry in D2's declared ORDER, and the signing request as a REQUIRED
  member, so an unattributable signature is unrepresentable);
  `setup-attestation.schema.yaml` (link 4 — the controller attests the
  environment IT PREPARED and COMMITS to the expected attestation set inside
  the same signed bytes); `commitment-extension.schema.yaml` (the same
  commitment written later, deadline at DISPATCH);
  `signed-chain-binding.schema.yaml` (the seventh record kind and the third leg
  of a tier-2 identity's COMPOSED issuance — subject scope, closed record-kind
  enumeration, the chain identity served — consuming the canonical
  `certificate-record` and `issuance-evidence` at `contract-v1.37` and
  redefining NEITHER); `runner-attestation.schema.yaml` (link 5 — signed AT the
  controller on a recorded, attributed request; corroborated against link 4 and
  never notarized); `pr-open-decision.schema.yaml` (link 6 — the enumeration
  EQUALS the committed expectation in both directions, the pull request and
  head revision inside the signed bytes; PROPOSING IS NOT PERMITTING);
  `closure-record.schema.yaml` (link 10 — the governed post-merge test the
  RATIFIED SUBJECT names, controller-dispatched on exactly the merge commit,
  authenticated and PASSING, the three lineage limbs verified; a
  merged-but-unclosed chain is a REFUSING state);
  `remediation-declaration.schema.yaml` (the ONE admitted consumer of an
  unclosed chain — itself a full chain, its exemption non-inheritable, its own
  closure owed).
* `scripts/signed_execution_chain/attestation.py` — the tranche-two walk of THE
  SAME NAMED READER, content-addressed by commit like the rest of the reader:
  links 1–6 as ELEVEN ordered checks in the ONE walk (org ruleset **21957695**
  unchanged — the same required check reading further, never a second gate),
  the horizon rules, the composed tier-2 issuance verified FINGERPRINT-FIRST,
  the custody ceiling read from the ratified registry's own file, and the
  remediation exemption's four refusals. **Ninety-five closed refusal codes,
  every one red-proven** by the self-test over TWO packaged corpora
  (`examples/` and `examples/tranche-two/` — the split forced by the log's
  append-only rule), 74 tranche-two negatives, four positive chains including
  the interleaved fan-out and the unamended zero-length lineage.
* **What this release does NOT operate**: no certificate authority, no minted
  tier-2 identity, no held private key, no running omnigent layer. SEC-R18 is
  declared UNMET (`execution_layer_ordering: not_enforced`) until a running
  layer REFUSES, and the packet's §5.1–5.3 machinery gates stay open — the
  packaged fixture keys exist as public halves, digests and signatures only.

## contract-v2.5 — 2026-08-31 (additive; a validated chain is not an audit trail, it is a permission)

Realizes `add-signed-execution-chain` **tranche one**, ratified 2026-08-29 by the
repository owner
(`openspec/changes/add-signed-execution-chain/review/ratification-2026-08-29.md`)
after all seven of the staged topic's questions were ruled the same day (#499,
squash `9c501df6`), **Q4** fixing tranche one at links 1–3 plus the signed
transparency log plus the short-chain gate. The packet landed as PR #495, squash
`91cf0a46`; the code surface — the five schemas, the packaged corpus, the named
reader and the running gate — landed as PR #524, squash `9af98c4d`. THIS ENTRY IS
`tasks.md` 4.7, the cut-dependent box that realization deliberately left to the
cutting session: registration in `contracts/manifest.yaml` and here, plus the
additive bundle, because a proposed change MUST NOT reserve a minor number before
merge order is known and this one had already been re-counted twice.

**Change class: ADDITIVE (minor)** under
[`docs/contract-versioning-policy.md`](../docs/contract-versioning-policy.md).
NOTHING NARROWS AT THIS RELEASE, AND THAT IS A MEASUREMENT RATHER THAN A CLAIM.
`git diff --name-status contract-v2.4 9af98c4d -- contracts/` reports **forty-seven
additions and exactly one modification**, and the one modification is
`contracts/README.md` — the editorial contract index, not a schema. Not one
schema, template, example or registry this repository already published moved a
byte. A release whose whole contract surface is NEW FILES and which changes no
existing shape cannot refuse an instance the prior bundle accepted, and the
refusal is not merely unlikely: there is no shared file for it to happen in. The
five schemas are one new family, and a new family is this policy's *"new
contracts"* case verbatim. Every consumer pinned at
`contract-v2.4` stays conformant until it deliberately upgrades, and
`contract_schema_version` is unchanged.

### What this release adds

* `contracts/signed-execution-chain/` — a NEW neutral contract family, tranche
  one, registered here with per-file `sha256` on all five schemas:
  * `digest-construction.schema.yaml` — **THE ONE CONSTRUCTION IN FORCE**,
    `xfc-jcs-sha256-1` (RFC 8785 JCS over the admitted value classes, then
    SHA-256, algorithm-tagged), declared ONCE and taken by `$ref` everywhere
    else. It declares NO record kind, deliberately, so the family cannot grow a
    second construction rule beside the first. A non-integer number, an integer
    outside ±(2\*\*53 − 1) and an unpaired surrogate are REFUSED rather than
    serialized, because a digest two conforming readers compute differently is
    worse than a digest one of them refuses.
  * `chain-inception.schema.yaml` — links 1 and 2 as ONE signed act.
    `signed_ratification` is the exact byte range the ratifying signature covers,
    and the actor binding, the presentation reference, the per-act value and the
    out-of-pipeline ground all sit INSIDE it, because a fact attachable after the
    signature is a fact anyone can attach.
  * `traveling-contract.schema.yaml` — link 3, the signed ratification carried
    WITH the work and checkable at the point of use with no live service in
    reach. It establishes internal consistency only; a question that requires the
    log still refuses while the log is unreachable.
  * `transparency-log-leaf.schema.yaml` — one signed, hash-linked leaf of the
    append-only log that is this capability's PRIMARY chain of custody, on the
    RFC 6962 / Certificate Transparency and Sigstore Rekor pattern taken as a
    hash-linked signed leaf sequence. THE HEAD IS THE NEWEST LEAF, so no separate
    tree-head record exists.
  * `conformance-declaration.schema.yaml` — a realization's obligation-by-
    obligation declaration over the capability's NINE obligations
    (SEC-R1..SEC-R9), closed in both directions, on `add-trust-anchor`'s ratified
    declared-shortfall pattern.
* NO SECOND IDENTITY, GRANT OR PROOF-OF-POSSESSION VOCABULARY. The presentation
  is the shipped `xfactory_wallet_grant_exercise` and the signing wallet the
  shipped `xfactory_wallet_record`, carried VERBATIM inside the signed bytes and
  validated against the schemas pinned at [`openxwallet-pin.yaml`](openxwallet-pin.yaml)
  (tag label `wallet-v1.3`); the actor is `identity-brokering`'s
  `actor_subject_reference` carrying an `xfactory_wallet_subject_attestation`.
  This bundle registers no openxFactory-owned copy of a pinned wallet shape.
* `scripts/validate-signed-execution-chain.py` + `scripts/signed_execution_chain/`
  — the NAMED READER, walking EIGHT ordered checks over links 1–3 plus the four
  scope rules a gate cannot see (atomicity, per-act uniqueness, the log's
  append-only property, the declaration). It VERIFIES the ratifying signature
  rather than reading a claim about it — `ed25519` per RFC 8032, pinned by that
  RFC's published vectors and their mutations, with the small-order public-key
  class refused by `[8]P == identity` — and refuses `ecdsa-p256` and
  `ecdsa-secp256k1` as UNEVALUABLE rather than accepting a signature it did not
  check. Content-addressed by commit, no per-file digest (the openxWallet,
  client-identity-roster, identity-brokering and trust-anchor precedent).
* `contracts/signed-execution-chain/examples/` — 7 positives composing ONE whole
  chain and 34 indexed negatives, with all 24 closed refusal codes red-proven and
  a self-test that REFUSES A CODE WITH NO PROBE. Two further obligations are
  refused BY SHAPE instead, because unrepresentable is stronger than refused. A
  negative is adjudicated IN THE POSITIVE CORPUS'S SCOPE, because a refusal of a
  CHAIN is a property of a SET of records.
* `.github/workflows/signed-execution-chain-gate.yml`, job id
  `signed-execution-chain-gate` — it verifies the openXwallet pin BEFORE trusting
  it, walks the tree with `--require-pinned-wallet-vocabulary` so an unreachable
  pin REFUSES instead of silently checking less, and asserts POSITIVELY that the
  walk happened. Its invocation is pinned by
  `tests/signed_execution_chain/test_gate_wiring.py` inside the required
  `pytest-suite` job, because a comment in a workflow protects nothing.
* `tests/signed_execution_chain/test_manifest_row_digests.py` — the five rows this
  bundle adds are recomputed FROM THE FILES ON DISK.
  `scripts/validate-manifest-digests.py` sweeps all 155 rows and is the right
  tool for the estate, but it is wired into no workflow and no test, so a row
  could go stale exactly as the one that rode through three bundle cuts
  undetected did. This test is scoped to the rows this family owns, so it reds
  for THIS capability's reason and cannot be greened by an unrelated row.
* `contracts/manifest.yaml`, `contracts/README.md`, `contracts/CHANGELOG.md`,
  `docs/contract-versioning-policy.md` — the editorial and ERROR-band members,
  re-baselined. The two contract-index rows the realization wrote as **REALIZED
  and NOT YET REGISTERED** are resolved to the literal `contract-v2.5`, and so is
  the family README's own front-matter, which said the same thing in the same
  words.
* `tests/intent-compliance/test_release_boundary.py` — the intent-compliance
  family's release boundary is pinned by an ENUM OF NAMED BUNDLE VALUES and fails
  loudly on a bundle it has not been told how to classify. That tripwire fired on
  this bump, correctly, and is what it is for: the library floor
  (`INTENT_RELEASE_FLOOR`) is an at-or-after comparison that would never have
  noticed. `contract-v2.5` is classified BY HAND and on the record with the
  introducing release — past the floor, family registered, family present — and
  asserts the same membership. The enum gains ONE named member handled by the
  SAME match arm; no test is added, removed, renamed or weakened, and the next
  bundle trips it again.
* `contracts/releases/contract-v2.5.digests.yaml` — this cut's inventory, built
  AFTER the `contract_bundle_version` bump and after every other member above,
  and never hand-edited.

### WHAT THIS RELEASE DOES NOT CONFER, in the present tense

**A registered contract family is not an enforced one, and this bundle is the
wrong artifact to read as evidence that it is.** Requirement 9 of this capability
is that nothing it defines confers or refuses anything until the named reader
runs as a REQUIRED check in the branch ruleset. It does NOT.
`add-signed-execution-chain` tasks **4.5** (make the check required — an operator
act, whose evidence is the live ruleset state and never a merged workflow file)
and **4.6** (its canary evidence, blocked on 4.5 by construction) are OPEN at
this cut and are not the cutting session's to close. Accordingly the packaged
conformance declaration records `is_required_in_ruleset: false`, the reader emits
a standing `reader-not-required` warning on every run, and a test refuses a
declaration that records SEC-R9 `satisfied` while the reader is unrequired. A
manifest row is a consumption contract for BYTES. Nothing here may be cited as
evidence that a chain is being walked before a terminal act.

> **ADDENDUM, 2026-08-31 (after this cut, and not part of it): 4.5 and 4.6 are
> PERFORMED.** `signed-execution-chain-gate` is REQUIRED on `main` through
> opensoft org ruleset **21957695**, and canary PR **#549** put a deliberately
> broken chain in front of it — run `33455808456`, one named refusal, the pull
> request reported BLOCKED, closed unmerged. The packaged conformance declaration
> now records `is_required_in_ruleset: true` and the standing warning no longer
> fires. **The paragraph above is left standing rather than rewritten**, because
> it is the record of what `contract-v2.5` shipped and every sentence of it was
> true at the cut — and because its point survives the flip intact: a registered
> contract family is still not an enforced one, this bundle is still the wrong
> artifact to read as evidence, and a consumer pinning these rows in ITS
> repository gets the shapes and not the enforcement.

**Two residuals are STRUCTURAL at this tranche and are refused the word
`satisfied` by the reader** rather than left to an author's care: SEC-R1's — the
pinned exercise record carries no field holding the SIGNED digest value, so the
record alone cannot prove the signed request included `object_ref`, and the
durable repair is an additive optional field belonging to `opensoft/openXwallet`
— and SEC-R6's unobserved suffix truncation, which tranche-three anchoring
closes. **No live log instance exists**: inception is a human act with a
wallet-held key, this bundle mints no chain, and the reader's repo scan says so
rather than reporting an empty sweep as a pass.

**MEMBERSHIP IS AN ASYMMETRY A REVIEWER WILL ASK ABOUT, and it is deliberate.**
The five schemas are registered in `contracts/manifest.yaml` and are **NOT**
release-inventory members: inventory membership is driven by
`contracts/hermes-runtime/contract-index.yaml`, the intent-compliance surface and
the named auxiliaries, and this family belongs to none of them — exactly as
`contracts/schemas/xfactory-credential-contracts.schema.yaml` did at
`contract-v2.4`. Their identity travels by manifest row `sha256`, verified by
`scripts/validate-manifest-digests.py` and recomputed from disk by the scoped
test above.

### The bundle number, FRESH-COUNTED at the cut

Counted at the branch tip rather than inherited, as `tasks.md` 4.7 requires and
as this number's own history earns — it has now moved twice:

* `contracts/manifest.yaml:3` declared `contract-v2.4`.
* `contracts/releases/` holds inventory files through `contract-v2.4`.
* `git ls-remote --tags origin 'refs/tags/contract-v2*'` publishes
  `contract-v2.0`, `contract-v2.1`, `contract-v2.2`, `contract-v2.3` AND
  `contract-v2.4`.
* No Unreleased block is pending.

`contract-v2.4` is SPENT — declared, tagged, and carrying **ZERO**
`signed-execution-chain` members, verified by grep over
`contracts/releases/contract-v2.4.digests.yaml` rather than assumed. So it covers
none of this family, the next available additive number is **`contract-v2.5`**,
and this cut takes it. THE FIRST COUNT, TAKEN AT THE REALIZATION TIP, READ
`contract-v2.4`; `add-binding-consumer-identity` then cut and tagged that number
alone (#526, `afdf0e88`). The realization had written the re-count instruction
into `tasks.md` rather than a number into a contract byte, which is the only
reason nothing had to be renumbered.

### The predecessor tags, as the fresh count found them — RECORDED BY #532, NOT RE-DERIVED HERE

The fresh count above reads `contract-v2.3` AND `contract-v2.4` as published, and
that is a change from what the `contract-v2.4` entry below could say: it recorded
v2.3's tag as PENDING an owner act and said nothing about its own. Both were
published by the repository owner on 2026-08-31, and **the measurement of record
is that entry's own § `contract-v2.4` tag disposition — PUBLISHED 2026-08-31**
(PR #532, `96b8a616`), which peels both tags, runs `verify-commit` at both
targets, and re-validates the targeting rule against a live control. **THIS ENTRY
DOES NOT RE-DERIVE IT.** Two records of one measurement is how they drift apart;
the count here needed only the tag list, and it reads `contract-v2.5` as the next
available number because of it.

WHAT THIS CUT ADDS INSTEAD IS THE HALF #532 ARGUED FOR AND DID NOT TAKE. That
entry names the structural cause — filed as **#528**, that no gate anywhere
asserts a declared bundle has a published tag — and observes that the policy's
sentence *"every bundle from `contract-v1.7` … is now tagged"* **has now been
false twice while nothing noticed**. It then, correctly, declines to correct the
prose again. So `docs/contract-versioning-policy.md` § Untagged Bundles After
Enforcement Began now carries both instances beside the three the 2026-08-25
ruling discharged, in the section a reader of `verify-tag` actually lands on,
where the changelog entry that records them archives out of nobody's path but is
also nobody's first stop. **A record is not a check**, and this cut does not
pretend otherwise: #528 stays open, and until it lands the sentence can go false a
third time.

`contracts/releases/contract-v2.3.digests.yaml` and
`contracts/releases/contract-v2.4.digests.yaml` are untouched by this cut.

## contract-v2.4 — 2026-08-31 (additive; a credential binding declares who holds it and what it fetches with)

Realizes `add-binding-consumer-identity`, ratified 2026-08-29 by the repository
owner after a §7.4-shaped council round read the packet adversarially, split 2–2
on the verdict word, agreed 4/4 that the drafted text was not ratifiable, and
returned fifteen blocking amendments — his ruling was ACCEPT ALL BLOCKING, one
fix round, the ratification read after
(`openspec/changes/add-binding-consumer-identity/review/ratification-2026-08-29.md`).
The schema, the validator's warning channel, the packaged corpus and the
generator sweep landed as PR #516, squash `5e8a33cf`. THIS ENTRY IS THE OTHER
HALF: §5.2's changelog half and §5.3, the cut that allocates the number the
packet deliberately declined to write in advance, because allocation is by merge
order and a number written before the merge is a number the next packet to land
would have to renumber.

**Change class: ADDITIVE (minor)** under
[`docs/contract-versioning-policy.md`](../docs/contract-versioning-policy.md).
NOTHING NARROWS AT THIS RELEASE, AND THAT IS A MEASUREMENT RATHER THAN A CLAIM.
The binding object has never been closed, so a `consumer:` key of ANY shape
already validated at `contract-v2.3`; the growth therefore cannot refuse an
instance the prior bundle accepted. Six shapes a domain could already hold — an
object with neither declared member, a scalar, a list, placeholder-styled values,
an undeclared extra member, and no block at all — were built and driven against
the shipped schema in
`tests/credential_contracts/test_consumer_block_phasing.py`
(`test_all_six_shapes_validate_at_the_introducing_minor`), and all six validate.
Five of the six are refused at `contract-v3.0`, which is exactly why the
narrowing is deferred to the major behind a served minor of warnings. A consumer
pinned at `contract-v2.3` stays conformant until it deliberately upgrades, and
`contract_schema_version` is unchanged.

### What this release adds

* `contracts/schemas/xfactory-credential-contracts.schema.yaml` — each entry of
  `credential_bindings` in `xfactory_credential_binding_template` MAY declare an
  OPTIONAL `consumer:` block: the consuming system that holds the binding
  (`holder_ref`), the identity that system authenticates to the secret store with
  (`fetch_identity`), an optional QUALIFIED `requirement_ref` (`requirement_id` +
  `requirements_document_ref`), and the const-true `shared_credential_acknowledged`
  and `instantiation_stub` tokens. THE BLOCK IS DECLARED HERE AND CONSTRAINED AT
  `contract-v3.0`: at this release the schema imposes no type, no member grammar,
  no requiredness and no closure on it.
* EIGHT deprecation codes, emitted as WARNINGS by
  `scripts/validate-credential-contracts.py` and enumerated with their migration
  path in `docs/contract-versioning-policy.md` § Deprecations Currently In Force:
  `consumer-identity-undeclared`, `consumer-block-incomplete`,
  `consumer-block-unknown-member`, `consumer-member-grammar`,
  `consumer-token-not-true`, `consumer-binding-key-grammar`,
  `consumer-access-mode-vocabulary` and `consumer-requirement-ref-grammar`. They
  serve SEVEN acts that land together at `contract-v3.0` behind ONE window — the
  member requiredness, the block's closure, the member grammar, the const-true
  token enforcement, and the three narrowings that sit OUTSIDE the block and are
  not exempt for it (the `credential_bindings` MAP KEY grammar, the closed
  `access_mode` vocabulary, and the repository-relative
  `requirements_document_ref` grammar). The requiredness is additionally GATED on
  a declarable degraded fetch-identity mode and shall not land without it.
* A packaged probe per code under `examples/credential-contracts/warning/` — ten
  fixture files across the eight codes, two codes carrying a second probe — and a
  self-test that REFUSES a code with no probe, so the next code added cannot
  silently ship unprobed.
* `consumer: {instantiation_stub: true}` is what a record written before any
  install exists declares, and THAT TOKEN IS THE ONLY EXEMPTION. A
  `*.template.yaml` FILENAME exempts nothing, being author-chosen, invisible in
  the bytes a pinned consumer validates, and unreachable by a pinned schema; a
  stub-named file carrying live values is a packaged NEGATIVE.
* `scripts/validate-credential-contracts.py` — the shared-secret refusal's
  first-against-rest arity is REPLACED by an EVERY-PAIR comparison, with a
  six-condition fail-closed lift for two consuming systems reaching one
  deliberately shared operated identity, and a new `shared-authority-identity`
  error. Both are enforced here and never re-implemented by consumers.
* `contracts/manifest.yaml`, `contracts/README.md`, `contracts/CHANGELOG.md`,
  `docs/contract-versioning-policy.md` — the editorial and ERROR-band members,
  re-baselined, with the deictic "the release that introduces it" / "at THIS
  release" phrasing resolved to the literal `contract-v2.4` at every occurrence —
  once in the manifest row's `consumption_rule` and three times in the policy
  entry — and the terminal audit line the section's other entries carry
  (`Warned since contract-v2.4; removal target contract-v3.0.`) added to the one
  that lacked it.
* `tests/intent-compliance/test_release_boundary.py` — the intent-compliance
  family's release boundary is pinned by an ENUM OF NAMED BUNDLE VALUES, and a
  bundle it has not been told how to classify fails loudly rather than being
  classified by inference. That tripwire fired on this bump and is what it is
  for: the library floor (`INTENT_RELEASE_FLOOR`) is an at-or-after comparison
  that would never have noticed, and the file exists to hold the family's
  membership and its manifest registration together. `contract-v2.4` is
  classified BY HAND and on the record with the introducing release — past the
  floor, family registered, family present — and asserts the same membership.
  No test is added, removed or weakened; the pin is advanced. A future bundle
  will trip it again, which is the design.
* `contracts/releases/contract-v2.4.digests.yaml` — this cut's inventory, built
  AFTER the `contract_bundle_version` bump and after every other member above,
  and never hand-edited.

**THE BUNDLE NUMBER WAS FRESH-COUNTED AT THE CUT**, as §5.3 requires and as this
repository's own renumbering history earns. Counted at the branch tip:
`contracts/CHANGELOG.md`'s top entry was `contract-v2.3` (2026-08-29);
`contracts/releases/` holds inventory files through `contract-v2.3`; `git tag`
publishes `contract-v2.0`, `contract-v2.1` and `contract-v2.2` and NOT
`contract-v2.3`; and no Unreleased block is pending (`grep -i unreleased` over
the changelog returns only historical prose in older entries). `contract-v2.3` is
therefore SPENT — declared and consumed as a number — but untagged, so the next
available additive number is **`contract-v2.4`**, and this cut takes it.

### `contract-v2.3` disposition — measured, and PENDING an owner act

`contract-v2.3` is DECLARED by three artifacts on `main` — the manifest's
`contract_bundle_version` (until this cut moved it), its changelog entry above,
and `contracts/releases/contract-v2.3.digests.yaml` — and its annotated tag was
NEVER PUBLISHED. Under this policy's own § Untagged Bundles After Enforcement
Began — DISCHARGED 2026-08-25, the remedy class for exactly this shape is
RETRO-PUBLICATION, NOT RE-DATING: publish the tag at *"the EARLIEST FIRST-PARENT
COMMIT on published `main` that DECLARES the bundle and at which `verify-commit`
PASSES."* Both halves were measured at this cut rather than asserted. The
earliest first-parent commit on `main` declaring `contract-v2.3` is
`ec8be5aa62179713f37ee12dab53a948d791e147` (the PR #514 merge); the three
first-parent commits above it — `698073f7`, `5e8a33cf`, `1d7e9bd2` — all declare
it too and none precedes it. `python3 scripts/validate-contract-release.py
verify-commit --commit ec8be5aa62179713f37ee12dab53a948d791e147` returns
`release verify-commit: pass` against
`contracts/releases/contract-v2.3.digests.yaml`, exit 0, no findings. So the
candidate satisfies the rule as written.

TAG PUBLICATION IS THE REPOSITORY OWNER'S ACT AND IS RECORDED HERE AS PENDING.
This entry measures; it does not publish, and it does not treat the measurement
as the act. Nothing in this release consumes `contract-v2.3` as a published
bundle, and this subsection may not be cited to treat an untagged bundle as
released — the same clause the discharged subsection binds every later reader
with. `contracts/releases/contract-v2.3.digests.yaml` is untouched by this cut.

### `contract-v2.4` tag disposition — PUBLISHED 2026-08-31

This entry did not originally say anything about its own tag, and the obligation
binds it the moment the bundle is declared: *"a bundle is not published until its
tag exists"*, and the manifest version, changelog heading and annotated tag *"MUST
match"*. The subsection immediately above measured the PREVIOUS bundle's missing
tag with care and left this one's unmentioned — recorded here plainly, because a
cut that documents its predecessor's gap and not its own is evidence that nothing
in the process is positioned to notice. That structural gap is filed as **#528**:
no gate anywhere asserts that a declared bundle has a published tag, which is why
the same shape reached `contract-v1.33`/`v1.35`/`v1.39` in August and needed a
ruling to discharge.

**Both tags are now published, by the repository owner, on 2026-08-31.** Annotated
tag objects, each peeling to the commit the ratified rule names:

| bundle | annotated tag | peels to | rule satisfied |
|---|---|---|---|
| `contract-v2.3` | `9fe9a742` | `ec8be5aa62179713f37ee12dab53a948d791e147` (the PR #514 merge) | `verify-commit` passes against `contracts/releases/contract-v2.3.digests.yaml`, exit 0 |
| `contract-v2.4` | `3374ad2f` | `afdf0e88f329740150654d5ad67a1984a104e83b` (the PR #526 squash) | `verify-commit` passes against `contracts/releases/contract-v2.4.digests.yaml`, exit 0 |

Each target is *"the EARLIEST FIRST-PARENT COMMIT on published `main` that DECLARES
the bundle and at which `verify-commit` PASSES"* — the rule this policy established
for the 2026-08-25 discharge, applied here rather than asserted. The rule was
re-validated against a live control before being trusted for these two: it returns
`8ccfb67b` for `contract-v2.2`, and that bundle's already-published tag peels to
exactly that commit. RETRO-PUBLISHED, NOT RE-DATED, on the same terms as the
August discharge: no release was reconstructed, re-cut or altered, and no version
number was reused.

**The subsection above is left exactly as written.** Its heading still says PENDING
an owner act, and that was true when it was written; the act has since been
performed and is recorded here rather than by editing the earlier text. This
follows the handling this policy already requires of `docs/archive-record-discrepancies.md`,
which states that `contract-v1.33` and `contract-v1.35` are not git tags and is
deliberately not corrected — rewriting a statement to match today's state destroys
the evidence of what was true then. A reader who arrives at the PENDING heading
should read on to here; a reader who cites it as evidence that `contract-v2.3` is
untagged today has misread it.

With these two published, every bundle from `contract-v1.7` — where mandatory
publication begins — carries an annotated tag again. That sentence has now been
false twice while nothing noticed, which is the argument #528 makes for a check
rather than for another correction of the prose.

## contract-v2.3 — 2026-08-29 (additive; standing-policy intent compliance with review-closed trust and outcome semantics)

Realizes `add-standing-policy-compliance-contract` through Speckit feature
`015-intent-compliance-contract`. The release was reallocated from the collided
v2.2 candidate only after the published `contract-v2.2` tag and inventory were
preserved from `main` and the `contract-v2.3` name was verified free.

**Change class: ADDITIVE (minor)** under
[`docs/contract-versioning-policy.md`](../docs/contract-versioning-policy.md).
The five new record kinds and their canonical validator are additive; no
existing contract shape is narrowed, and consumers may remain pinned until
they adopt standing-policy compliance gates.

### What this release adds

* The five-record `contracts/intent-compliance/` family: an authority-bound veto
  vocabulary, immutable allowance approval, separate authenticated revocation,
  append-only allowance registry, and closed, bounded, redacted compliance
  decision.
* Canonical digest closure, trusted-snapshot authority resolution,
  lifetime-unique allowance identifiers, deterministic outcome precedence,
  neutral scope verdicts, bounded fail-closed classifier evidence, identical
  cross-gate bindings, and registry-head-conditioned dispatch authorization.
* `scripts/validate-intent-compliance.py`, positive scenarios, indexed
  single-fault negatives, focused pytest coverage, and fail-closed release
  membership for both partial and absent family registration.
* Hardened static pytest/PostgreSQL realization evidence, including exact test
  identity and cardinality, stable collection semantics, cumulative budgets,
  and deterministic local-origin release tests rather than live-remote timing.

### Review repairs carried by the cut

Authority trust is content-bound, not inferred from Git object existence. Each
issuer, revoker, and policy-approval principal cites one bounded authority
document from the caller-supplied trusted snapshot; the validator verifies the
blob bytes, digest, repository and ancestor revision, then requires the exact
principal/role tuple and, for an approval, the exact approval id. Inherited Git
repository-redirection variables, including `GIT_COMMON_DIR`, cannot redirect
that lookup.

Registry state is a tagged outcome. `resolved` carries the uniquely derived
registry revision id and digest; `unresolved` carries exactly
`registry_not_found` or `registry_head_ambiguous`. The declared decision state,
every unresolved resolution reason, and deterministic evidence must agree with
the derived tag. A terminal decision binds the current unique head; an
intermediate decision binds the applicable historical head at evaluation time.

A deterministic veto is pure: it is sufficient for `block` with no fabricated
allowance reference or resolution. Allowance evidence may satisfy a
deterministic finding, but it cannot erase or downgrade a deterministic block;
classifier and Hermes layers may only preserve the block or escalate another
outcome to review. Composition remains
`block > needs_human_review > allow`.

### Superseding digest correction and immutable history

Both published `contract-v2.1` and published `contract-v2.2` carried the stale
ideation-dashboard snapshot digest
`6a3b496c59cea9cfb232e35d21b4864a928287c7b98b5436aac0c83d9c14e9b3`
in their manifest bytes. The schema bytes themselves were unchanged and hash to
`9c44da235e8b4771b721b3ea0f88e0f6adcdaf4854cac045924abd9981c9ea9c`.
This release supersedes the stale manifest claim. Both published inventories
and annotated tags remain immutable, including their historical manifest bytes;
neither inventory is rewritten to make the old release describe a later tree.

### Release obligation still open at this entry

`contracts/releases/contract-v2.3.digests.yaml` is committed with 283 entries.
It must be regenerated after the current review-repair bytes stabilize, then
verified against the exact final candidate commit. Merge, tagging, and
publication remain pending. The downstream first conformer remains
codexFactory's `add-intent-compliance-gate` realization.

## contract-v2.2 — 2026-08-29 (additive; a catalog entry may say WHAT KIND of input it accepts, and the type stops being weaker than its own wire)

Realizes `add-model-capability-vocabulary`, ratified 2026-08-24 with TWO rulings
in one read (`openspec/changes/add-model-capability-vocabulary/review/ratification-2026-08-24.md`):
ratify the requirement set, and **the parity scope is ALL FIVE** — every string
bound the released schema declares gets type-side enforcement in THIS release,
with no residue and no named follow-up. Ruling 2 overrode the proposal's own
recommendation, which had closed two bounds and recorded three as a follow-up.

**Change class: ADDITIVE (minor)** under
[`docs/contract-versioning-policy.md`](../docs/contract-versioning-policy.md).
ONE OPTIONAL PROPERTY is added to one `$defs`; nothing is required, deprecated,
removed or narrowed, and no instance valid at `contract-v2.1` becomes invalid.
A consumer pinned at `contract-v2.1` remains conformant until it deliberately
upgrades, and a consumer that never reads the new key stays correct against
every catalog it could already read. `contract_schema_version` is unchanged.

**THE BUNDLE NUMBER WAS FRESH-COUNTED AT REALIZATION, twice** — at the branch
base and again before the landing squash — as the proposal, the design's
non-decision and the ratification's third acceptance note all insist, because
this repository has renumbered mid-flight more than once. It is `contract-v2.2`
and NOT the `contract-v1.41` the packet speculated about: v1.41 through v1.47,
v2.0 and v2.1 were all allocated between ratification and realization, no
Unreleased block was pending, and `contract-v2.1` is the published tip.

### What moved

* `contracts/schemas/xfactory-workbench-model-catalog.schema.yaml` —
  `$defs/model_entry` gains OPTIONAL `modalities`: an array,
  `uniqueItems: true`, `minItems: 1`, `items.enum` exactly `text` and `image`,
  and `contains: {const: text}`. It is NOT in `required`, so absence stays valid
  and every catalog released before this one still validates.
* `scripts/ideation_dashboard/doxbench_model.py` — the type reads, validates and
  PROJECTS the declaration, and closes the six bound gaps below.
* `scripts/validate-ideation-dashboard-contracts.py` — `check_model_catalog`
  now records, in the place a later reader looks for a delegated rule, that the
  three modality refusals are deliberately NOT delegated.
* `examples/ideation-dashboard/` — one positive declaring `[text, image]`, three
  negatives (one per refusal), the absence case named on the existing local
  example, and the index rows for all four.
* `contracts/manifest.yaml`, `contracts/README.md`, `contracts/CHANGELOG.md` —
  the editorial members, re-baselined; the manifest's `consumption_rule` states
  the absence rule and the closed-vocabulary extension route.
* `contracts/releases/contract-v2.2.digests.yaml` — this cut's inventory, built
  AFTER the `contract_bundle_version` bump.

### `contains: {const: text}` is load-bearing, and that is a review finding

`minItems` plus an item enum does NOT encode required `text` membership. Without
the `contains` clause the shape would have accepted `modalities: [image]` — an
instance the catalog TYPE refuses — so a schema-only consumer would have treated
as conformant a catalog the type rejects. THE WIRE GATE MUST NOT BE THE WEAKEST
ONE, which is the very divergence class this release's second requirement closes
pointing the other way.

**THE TYPE IS THE ONLY OTHER GATE**, stated precisely because the obvious
phrasing overstates it. The ratified task says such an instance is one "the type
and the standalone validator both refuse"; that is not so, and this release's own
measurement is what shows it. The delegated validator does not restate the
modality rules — all three are expressible in the shape — so it refuses
`modalities: [image]` BY APPLYING THESE BYTES, and the revert that removes
`contains` sends the packaged validator to `1 error(s)` precisely because the
image-only negative STOPS being refused. So in the counterfactual the type
refuses alone, which is reason enough for the clause and is the honest reason.

### Absence is not a claim, in either direction

An entry that declares nothing is a PRODUCER THAT PREDATES THE FIELD, not a
model that rejects images. A reader treats it as text-only FOR ROUTING — the
safe reading — while recording that no declaration was made, so a conservative
default stays distinguishable from a stated capability. The type carries both
facts (`declares_modalities`, `routing_modalities`) and keeps `None` and `()`
DIFFERENT VALUES, exactly as the wire does: no key versus `minItems: 1`.

This is not invented here. The chat-turn family already uses this idiom for
`context_posture`, where absence means "a producer older than contract-v1.40"
rather than a posture claim, and reusing it keeps one rule in a reader's head.

### The declaration REACHES THE WIRE, and that was not automatic

`ModelCatalogEntry.as_public_dict()` emits an EXPLICIT key list rather than
serializing the dataclass, so a declared set would have been validated in
process and then silently dropped by `GET /workbench/model-catalog` — leaving
consumers and the routing successor with nothing to read, which is the entire
purpose of the field. The pre-ratification bot round found this; the projection
is deliberate, follows the present-only-when-declared idiom the routing fields
already use, and is proved AT THE ROUTE (a real request through the real
released-schema validation) rather than only at the projection. An undeclared
entry emits no key, so its served bytes are byte-identical across this boundary.

### THE PARITY HALF: six gaps, all reproduced, all closed, no residue

The catalog type refused less than its own released schema. Every gap below was
REPRODUCED by construction before it was closed, at the ratification commit and
again at this branch's base:

| field | released bound | probe | before | after |
| --- | --- | --- | --- | --- |
| `model_id` | `maxLength: 128` | 129 chars | accepted | refused |
| `model_id` | pattern | `'has space'` | accepted | refused |
| `label` | `maxLength: 200` | 201 chars | accepted | refused |
| `provider_class` | `maxLength: 64` | 65 chars | accepted | refused |
| `data_handling` | `maxLength: 500` | 501 chars | accepted | refused |
| `models` | `maxItems: 64` | 65 entries | accepted | refused |
| `resolved_model_id` | `maxLength: 128` + pattern | 129 chars, `'has space'` | already refused | unchanged |

`resolved_model_id` is the fifth string-bounded field and was ALREADY enforced
through `_require_model_reference`. That is what made the widening cheap: the
pattern existed, worked, and is REUSED for `model_id` rather than respelled.

**N7's deferral is discharged by name.** The code said tightening `model_id`
"would be a behaviour change belonging to no release". This is that release: it
opens `$defs/model_entry` and the same construction gate anyway, and the fix
moves no schema byte, so it rides at no additional release surface. The test
that pinned the laxity said in as many words that a release closing the gap
should make it fail and be rewritten; it did, and it was.

**TWO BEHAVIOUR CHANGES, stated plainly.** Constructions that succeed today will
fail after this lands: a 65-entry catalog, and an out-of-bounds `model_id`,
`label`, `provider_class` or `data_handling`. ALL WERE ALREADY UNSERVABLE — the
catalog route validates the projected envelope against these bytes — so what
changes is WHERE they fail, not whether. The existing corpus and fixtures were
checked before landing rather than discovered in a gate: no packaged example, no
fixture and no in-repo catalog carries a value any of the six now refuses.

The entry-count cap takes its OWN exception class, `CatalogEntryCountError`. No
single entry is wrong, so `InvalidCatalogEntryError` — whose docstring says a
single field failed — would be a false statement about what happened, and an
over-large catalog of plain entries is not a routing inconsistency, so
`InvalidRoutingRuleError` is wrong for the opposite reason. The split this
module keeps is by HOW MUCH CONTEXT A REFUSAL NEEDS.

**NO-RESIDUE IS PROVED FROM THE SCHEMA, not from a list.** The ratified
requirement's last scenario says a field the schema bounds but the type does not
is a DEFECT IN THE REQUIREMENT rather than an accepted residue. A test that
enumerated four names could not see a fifth bound added later, so the proof
walks the released `$defs/model_entry`, collects every string property carrying
a `maxLength` or `pattern`, and drives a violating value through the real
construction gate for each.

ITS REACH, STATED EXACTLY rather than rounded up: it walks the TOP-LEVEL string
properties of the entry, and it holds the set of them to a hard equality — so a
future release that adds a bounded top-level string and forgets the type fails
there. A bound added under an ARRAY'S `items` (the shape `routes_to` already
has) or inside a nested object is outside its walk and would still need a
reader. That is the honest boundary of the guarantee.

**ONE PLACE THE TWO GATES DIFFER, and it is the type being STRICTER.** The
requirement asks that the type refuse everything the schema refuses; it does.
The reverse does not quite hold: `label`, `provider_class` and `data_handling`
keep the blankness refusal they have always had, so a whitespace-only value is
refused at construction while the released schema — `minLength: 1`, no pattern —
accepts it. That predates this release and is deliberately not softened: the
length bound is ADDED to the blankness check rather than substituted for it, and
a tightening removed to make a symmetry claim tidier would be a regression
dressed as parity. Recorded so "exact parity" is read as the requirement states
it, in one direction.

### What this release does NOT do

It does not READ `modalities` to choose a destination. Fit-aware routing is
exit (b) of the staged topic `doxchat-auto-fit-routing` and CONSUMES this
vocabulary; compress-to-fit disclosure is exit (c). No route, selector or
browser file changes here, which is why this exit was sequenced first: it
deliberately avoids the ratified-but-unbuilt intake lane that (b) must be
sequenced against.

No second capability dimension enters. Audio, video, tool-calling, structured
output, latency class and cost class are each plausible and none has a consumer;
a member enters with the ratified change that governs it, on the roster's
`admission_surface` rule.

The three modality refusals are NOT delegated to
`scripts/validate-ideation-dashboard-contracts.py`. All three are expressible in
the shape, so the released schema that validator already applies refuses them,
and a fourth spelling would be a second gate to keep in step with no rule to
enforce. The three packaged negatives prove the refusal happens.

### RECONCILIATION with `add-doxchat-model-intake`

That change's proposal describes the catalog entry as "the closed seven-field
shape" and promises its proposed-versus-approved distinction "does NOT widen"
it. Both remain true of THAT change: its packet is another lane's and IS NOT
EDITED HERE, its descriptions were accurate when ratified, and its no-widening
promise is about its own delta. What changes is the REFERENT — the closed entry
is now the v2.2 shape: seven required base fields, plus `modalities`, plus the
three routing-declaration fields. This is exactly the reconciliation
`contract-v1.38` recorded for the same packet and the same sentence, and it is
recorded the same way, in this entry rather than by editing a ratified record.

Its realized module `scripts/ideation_dashboard/doxbench_intake.py` carried the
count in a docstring, where the sentence had become false rather than merely
dated; it now names `DECLARABLE_ENTRY_FIELDS` instead of a number, so the claim
it actually makes — that THIS module widens nothing — survives the next growth.

### The consumer re-pin

codexFactory pins this schema by digest. The growth is additive and a consumer
may ignore the field entirely, but the digest moves from
`sha256:dff513fa…` to `sha256:e563cc9f…` and the pin moves with it. Updating it
is codexFactory's own governed act under the domain upgrade runbook; no file in
that repository is touched here, and this entry is the notice.

The in-repo consumer pin moves in this cut:
`scripts/ideation_dashboard/doxbench_contracts.py` and its companion test carry
the new catalog digest and the `unpublished:contract-v2.2` REF SENTINEL across
the realization branch, on the v1.34/v1.38/v1.40/v1.45 precedent — the policy
publishes the annotated tag against the commit that LANDS, so until that commit
exists there is nothing honest to name, and the sentinel is spelled as a value
no `stack.yaml` can declare so a consumer comparing against it REFUSES rather
than matching by accident.

RECORDED, because a reader will find it: the `contract-v1.45` repin left
`unpublished:contract-v1.45` standing after that tag was published, so its own
task 4.2 went undischarged. This cut SUPERSEDES that sentinel rather than
repairing it — there is no honest way to resolve a sentinel for a bundle these
bytes no longer belong to.

### Release obligation still open at this entry

Per the versioning policy, CHANGELOG presence is the availability test and the
annotated tag is cut at the realization squash against the commit that actually
lands. `releases/contract-v2.2.digests.yaml` ships INSIDE this cut, built after
the version bump, and `verify-commit` passes on the candidate.

Realized by `add-model-capability-vocabulary`. The change itself does NOT archive
with this cut: it carries a code surface, and the archive gate wants the merge
and a green run first.

## contract-v2.1 — 2026-08-28 (additive; the release verifier tells the one content condition it can act on from the fourteen it cannot)

**Change class: ADDITIVE (minor)** under
[`docs/contract-versioning-policy.md`](../docs/contract-versioning-policy.md).
NO SCHEMA BYTES CHANGE: nothing under `contracts/schemas/` moves,
`contract_schema_version` is unchanged, no field is added, deprecated or
removed, and no instance valid at `contract-v2.0` is narrowed or invalidated. A
consumer pinned at `contract-v2.0` remains conformant until it deliberately
upgrades. NO FINDING CODE is added, removed, renamed or re-severitied:
`HGR-RELEASE-SURFACE-DRIFT`, `HGR-RELEASE-MEMBER-MISSING` and
`HGR-RELEASE-PATH-UNRESOLVABLE` fire on exactly the population they fired on
before, and the refusals this cut introduces take the EXISTING
`HGR-RELEASE-DEPENDENCY` class. The inventory schema, the membership closure,
the digest rule, the mode comparison and the CLI exit codes are untouched.

WHY THIS CUT EXISTS, stated as membership rather than as preference. Both edited
validators are NON-EDITORIAL members of the declared bundle's own digest
inventory (`contracts/releases/contract-v2.0.digests.yaml`, established by
PARSE: the document loaded and its 192 entries walked, not grepped).
`scripts/hermes_runtime_validation/release.py` is present as `type: validator`
at `sha256:660e55ca…` and `scripts/hermes_runtime_validation/content.py` on the
same terms, each exactly what the tree carried before this change;
`contracts/hermes-runtime/evidence-register.yaml` is present as
`type: evidence-register` and moves too, because the new proofs are bound in it.
The editorial set is exactly three files — `contracts/CHANGELOG.md`,
`contracts/manifest.yaml` and `contracts/README.md`
(`scripts/doc_health/release_inventory.py:62-66`) — and none of the three moved
members is in it. Editing them without cutting would leave the declared
inventory describing bytes the repository no longer holds, which
`release-surface-integrity` names a defect, whose prescribed remedy is a release
cut and NEVER a hand-edit of an inventory to match a tree, and which doc-health's
release-inventory-drift family reports at `error` rather than at a warning.
TOUCHING THREE MEMBERS OWES ONE CUT, NOT THREE: the inventory is rebuilt
wholesale from the manifest plus the contract index, so one build re-baselines
every moved member at once. THE PRECEDENT IS THE SAME FILE FOR THE SAME CAUSE:
`contract-v1.44` was cut two days ago as an additive re-realization because
`fix-release-reachability-race` changed this very file, and `contract-v1.10`
before it for the same reason.

WHAT MOVED:

* `scripts/hermes_runtime_validation/content.py` — the resolver now DECLARES
  which condition it observed. `resolve_git_object` reaches fifteen refusals
  carrying fourteen distinct messages, and exactly ONE of them is a fact about
  the release: `ls-tree` resolved the commit AND its tree, and the path was not
  in it. That site alone raises with `code=CONTENT_PATH_ABSENT`
  (`HRC-CONTENT-PATH-ABSENT`); every other site keeps the default
  `HRC-CONTENT-DEPENDENCY`, whose spelling and value are unchanged. Purely
  additive, and measured rather than assumed: nothing in this repository reads
  `ContentResolutionError.code` — the four `.code` readers that exist read
  `MigrationContractError`, `DomainRegressionDependencyError`,
  `ReleaseDependencyError` and `ConsumerHandoffDependencyError` — so no observed
  surface changes for any consumer that never asked.
* `scripts/hermes_runtime_validation/release.py` — `_blob_object_id` converted
  EVERY `ContentResolutionError` into `None`, and `_CommitSource.exists`
  converted every one into `False`. Both answers are then consumed as DATA: the
  first is one side of `_surface_drift`'s comparison, the second decides release
  membership and whether `contracts/manifest.yaml` is present at the commit.
  So a fact about the MACHINE became a verdict about the RELEASE, and it failed
  in both directions with the quiet one worse — a failure on ONE side
  manufactured a drift finding out of an environment fact, and a failure on BOTH
  sides made two identical non-answers compare EQUAL and reported the surface
  UNDRIFTED having read neither side of it, emitting nothing a reader could
  notice. Measured against this repository before the fix: seven distinct
  conditions — the path absent, the commit absent, the repository absent, the
  directory that is not a repository, a path that is a directory, a path that is
  not canonical, a revision that is not a full object id — all produced the same
  `None` and the same `False`, carrying the same code. Now a single
  `_resolution_established_absence` reads the resolver's declared code: the one
  data condition still yields `None` / `False` unchanged, and every other
  condition becomes a fail-closed `ReleaseDependencyError` whose reason NAMES THE
  CONDITION OBSERVED (`release content could not be resolved at <commit>:
  <path>: <the resolver's own refusal>`) rather than a conclusion about the
  release, with the original chained by `from`.
* **The distinction is carried by a DECLARED CODE and never by matching the
  message.** A message is prose, prose is edited for clarity, and a near-miss
  match would then silently reclassify a safety refusal as release data — the
  same hazard the sentinel vocabulary refuses near-miss spellings for. Pinned at
  SOURCE level rather than behaviourally, because the rejected mechanism passes
  every behavioural test on the day it is written: substituting a message match
  for the code comparison left all nine behavioural proofs green and was caught
  only by the structural assertion.
* **THE SAFETY REFUSALS STAY REFUSALS.** A release-surface path that is a
  directory or a nested repository link at one commit takes the resolver's
  deliberate "not a supported regular file" refusal, and it is no longer read as
  absence. That is reachable from COMMITTED DATA rather than only from a broken
  environment, and it is not softened because the same path resolves cleanly at
  the other commit under comparison.
* **`HGR-RELEASE-PATH-UNRESOLVABLE` at the inventory-path read is deliberately
  NOT changed.** It already emits a NAMED FINDING rather than a silent value, and
  changing what a published finding code means to consumers reading verifier
  output is a contract question rather than a defect fix. The obligation is
  scoped to resolutions reduced to presence or identity, so leaving that site is
  conforming rather than a self-violation.
* `tests/hermes_runtime_contracts/test_release_inventory.py` and
  `test_content_resolution.py` — twelve new proofs over the module's established
  `_bare_origin` / `_repo_with_committed_inventory` fixture pair, which DRIVE
  each condition by argument or by committed data rather than by a real store
  timeout: the absent path in both directions, the unavailable store, the quiet
  direction with both sides failing, and the unsafe object at one commit only.
  Ten of the twelve fail against the committed module. Mutation-pinned at source
  level in three directions: flattening every refusal back to absence fails all
  seven refusal proofs while both absent-path proofs still pass; flattening
  absence into a refusal fails both absent-path proofs; and substituting a
  message match for the declared code fails the structural proof alone.
* `contracts/hermes-runtime/evidence-register.yaml` — the twelve proofs are
  bound under the `SCO-002` scenarios they serve (`S03` pinned-file drift, `S04`
  verification without a usable network). Test node ids added to existing
  scenarios; no scenario id added.
* `contracts/CHANGELOG.md` and `contracts/manifest.yaml` — the editorial
  members, re-baselined.

THE SAME FORTUNATE PROPERTY `contract-v1.44` recorded holds again: the cut runs
the NEW code, so `verify-promotion` exercises the fix before the release that
carries it is tagged.

Realized by `fix-content-resolution-conflation`.

## contract-v2.0 — 2026-08-27 (BREAKING; the eight openxWallet contracts are REMOVED and the family is consumed at a pin)

Realizes `split-openxwallet-repo` **P3** (`tasks.md` §7), the atomic
consume-and-shed that design decisions **D1**, **D2**, **D3**, **D4** and **D6**
specify, through Speckit feature `023-openxwallet-consume-shed`.

**Change class: BREAKING (major)** under
[`docs/contract-versioning-policy.md`](../docs/contract-versioning-policy.md)
§ Change Classes, *Breaking (major)*: a shape is REMOVED. All three of that
clause's requirements are discharged, and each is checkable:

1. **A CHANGELOG migration note** — below.
2. **At least one full minor release where the old shape produced deprecation
   warnings** — `contract-v1.47`, whose eight `relocating:` rows and
   `scripts/check-openxfactory-pin.py` WARN-tier notice served exactly that
   purpose. This cut could not legally precede it.
3. **An update to the conformance validator** — discharged by the MOVE ITSELF.
   From this major forward this family's conformance validator IS the pinned
   `openXwallet/scripts/validate-openxwallet.py`, at the commit and digest
   [`openxwallet-pin.yaml`](openxwallet-pin.yaml) records. There is no second
   validator that accepts a new shape and rejects the old one, because there is
   no new shape: the BYTES are identical and the PUBLISHER changed.

### What is removed

The eight digested openxWallet rows leave [`manifest.yaml`](manifest.yaml):
`openxwallet-record`, `openxwallet-custody-registry-schema`,
`openxwallet-custody-registry`, `openxwallet-grant`,
`openxwallet-grant-exercise`, `openxwallet-distinct-holder-constraint`,
`openxwallet-subject-attestation` and `openxwallet-agent-composition`. With them
go `contracts/openxwallet/`, `contracts/openxwallet-agent-profile/`,
`scripts/validate-openxwallet.py`, `scripts/wallet-yaml-syntax-gate.py`,
`tests/wallet_yaml_syntax_gate/` and `.github/workflows/wallet-validation.yml`.

**NO BYTES OF ANY CONTRACT CHANGED.** Every one of the eight artifacts carries at
`opensoft/openXwallet` `wallet-v1.1` exactly the `sha256` this manifest recorded
for it at `contract-v1.47`, and exactly the bytes it had at `contract-v1.31`.
That is not a courtesy: a move whose diff is not provably empty cannot be
bisected against, and this atomic cut rests on that property.

### The migration path

1. **Read the artifacts from `opensoft/openXwallet`**, tag `wallet-v1.1`.
2. **Pin them through [`openxwallet-pin.yaml`](openxwallet-pin.yaml)**, which
   arrives in THIS cut: `kind: pinned_contract_manifest`, `revision_kind:
   commit`, a 40-hex `commit`, `submodule_path: openXwallet`, eight `files:`
   members each with its `sha256`, and `pinned_by_commit_only:` for the
   validator, the syntax gate, both `examples/` corpora and both family READMEs.
   `contract_bundle_tag: wallet-v1.1` is a LABEL beside the commit and never the
   trusted referent; a tag-only pin is REFUSED (`pin-tag-only`).
3. **Verify the pin before trusting anything it names** —
   `python3 scripts/verify-openxwallet-pin.py`. Six ordered checks, exit 2 with a
   NAMED code (`pin-submodule-uninitialized`, `pin-gitlink-mismatch`,
   `pin-checkout-mismatch`, `pin-digest-mismatch`, `pin-member-missing`,
   `pin-tag-only`), and one fixed remediation trailer on every refusal.
4. **Run the PINNED reader**, not a local copy:
   `python3 openXwallet/scripts/validate-openxwallet.py <checkout>`. openxFactory
   runs exactly that as its REQUIRED `wallet-validation` check, over its own
   tree, from `.github/workflows/openxwallet-consumer-gate.yml`.
5. **Re-pinning** is `openXwallet/docs/pin-resync-runbook.md`.

The pin also records `carve_commit:
30565e48ffe3d8a9773e10af33425701845e10f6` — the NAMED CARVE COMMIT the eight
digests were taken at. "HEAD" is not a stable referent across a
multi-pull-request wave, so the referent is in the FILE and not only in the
runbook.

### What did NOT move, and why

`governance/review-authority/` STAYS — all four files. The reader travels; the
DATA stays. codexFactory's
`scripts/merge_master/openxfactory-review-authority-floor.yaml` names
`governance/review-authority/register.yaml` in `opensoft/openxFactory` under
`never_clearable_paths`, and a floor cannot be satisfied by a path in another
repository. The consumer gate therefore runs the pinned reader over
openxFactory's OWN tree, which is what keeps the intake register readable at all.

The `openxwallet` capability ids, the `xfactory_wallet_*` kind prefix, every
finding code, every filename and every path are UNCHANGED (R2). The brand became
`openXwallet`; the wire label did not.
`openxwallet_revocation_through_derivation` in the trust-anchor family is a
frozen machine key and is not renamed here.

### The REQUIRED check survives by ALIAS, not by repoint

Org ruleset 21538893 requires the check `wallet-validation` on `main`. That token
is the JOB ID, never the filename, so `openxwallet-consumer-gate.yml` retains
`jobs: wallet-validation:` verbatim and **ruleset 21538893 is edited by nothing
in this wave**. Renaming the TOKEN is a named successor and a precondition of
nothing here.

### Release surface

[`releases/contract-v2.0.digests.yaml`](releases/contract-v2.0.digests.yaml) is
this cut's inventory, over a surface that no longer carries the eight artifacts —
transitively, since inventory membership is catalog-driven from
`contracts/hermes-runtime/contract-index.yaml` and the eight FILES were never
inventory members: what changes is that `manifest.yaml` IS a digested member and
the digest recorded is now an eight-row-lighter manifest's.

### Rollback posture

`git revert` of this cut restores every path — the carve COPIED and deleted
nothing — and removes the pin file and the gitlink; `wallet-validation.yml`
returns as a filename. Ruleset 21538893 is unchanged throughout, so there is
nothing to roll back there. A published bundle is not unpublished: if the
DOCTRINE were reversed the honest reversal would be a following major, not a
revert of the cut.

## contract-v1.47 — 2026-08-27 (deprecating; the eight openxWallet contracts are marked relocating)

Realizes `split-openxwallet-repo` **P2.5** (`tasks.md` §5), the deprecating minor
that design decisions **D5** and **D6** specify, through Speckit feature
`018-openxwallet-deprecation-minor`. **NO CONTRACT FILE CHANGES IN THIS CUT.**
Every one of the eight openxWallet artifacts keeps the exact bytes it had at
`contract-v1.45`, keeps its per-file `sha256` in [`manifest.yaml`](manifest.yaml),
keeps its `schema_version: 1`, and keeps validating. What changes is what the
manifest SAYS ABOUT THEIR FUTURE.

**Change class: DEPRECATING (minor)** under
[`docs/contract-versioning-policy.md`](../docs/contract-versioning-policy.md)
lines 246-248. Nothing previously valid becomes invalid; no required field is
added; no shape is removed; no vocabulary is reinterpreted. A domain repo on the
same major version remains conformant WITHOUT CHANGES — which is the entire
purpose of this release existing separately from the one that follows it.

**Why this cut exists at all.** The successor change deletes these eight rows from
the manifest. `:250-252` classes a removed shape as BREAKING and requires, before
it, "at least one full minor release where the old shape produced deprecation
warnings". This IS that release. Without it the removal is an illegal cut. One
normative document moves with the cut for the same reason it did at
`contract-v1.34`: [`docs/contract-versioning-policy.md`](../docs/contract-versioning-policy.md)
records this deprecation in its "Deprecations Currently In Force" list. Both it
and this changelog are release-surface members and both are digested in this
cut's inventory.

**On the number.** This cut was authored as `contract-v1.46` and renumbered to
`contract-v1.47` at merge order: while it waited for review, the additive
avatar-client cut (`qualify-avatar-live-voice`, AVC-09 and AVC-10) landed and
published `contract-v1.46` first. That is exactly the case
[`docs/contract-versioning-policy.md`](../docs/contract-versioning-policy.md)
lines 30-31 exist for — "a proposed change MUST NOT reserve a minor number before
merge order is known" — so the four places that carry the number (the manifest's
`contract_bundle_version`, the eight rows' `since:`, this heading, and the
inventory filename) moved together rather than the earlier cut being asked to wait.

### What is deprecated, and what it is deprecated IN FAVOUR OF

The eight artifacts whose canonical home becomes `opensoft/openXwallet` — seven
under `contracts/openxwallet/` and one under
`contracts/openxwallet-agent-profile/`:

| manifest `id` | path |
|---|---|
| `openxwallet-record` | `contracts/openxwallet/openxwallet-record.schema.yaml` |
| `openxwallet-custody-registry-schema` | `contracts/openxwallet/openxwallet-custody-registry.schema.yaml` |
| `openxwallet-custody-registry` | `contracts/openxwallet/openxwallet-custody.registry.yaml` |
| `openxwallet-grant` | `contracts/openxwallet/openxwallet-grant.schema.yaml` |
| `openxwallet-grant-exercise` | `contracts/openxwallet/openxwallet-grant-exercise.schema.yaml` |
| `openxwallet-distinct-holder-constraint` | `contracts/openxwallet/openxwallet-distinct-holder-constraint.schema.yaml` |
| `openxwallet-subject-attestation` | `contracts/openxwallet/openxwallet-subject-attestation.schema.yaml` |
| `openxwallet-agent-composition` | `contracts/openxwallet-agent-profile/openxwallet-agent-composition.schema.yaml` |

Each row gains ONE added key and nothing else — the marker D5 chose, as a nested
mapping, placed last so no existing line moves:

```yaml
    relocating:
      to: opensoft/openXwallet
      tag: wallet-v1.1
      since: contract-v1.47
```

`to` is the repository that becomes the artifact's canonical home. `tag` is the
tag in that repository a consumer migrates TO — `wallet-v1.1`, which is the tag
openxFactory itself pins when the move completes, not the earlier `wallet-v1.0`
against which the carve's byte-identity floor was proven. `since` is this bundle.

**There is deliberately NO removal-version key on the row.** `:246-248` puts the
removal version and the migration path HERE, in the changelog, and naming the next
MAJOR is permitted where naming the next MINOR is not: `:30-31` forbids reserving
a minor before merge order is known, and there is exactly one next major.

### Removal version

**`contract-v2.0`** — the next major bundle, and therefore the earliest release at
which a removal is legal. This release starts the one-full-minor deprecation
window `:250-252` requires. The eight rows and their bytes are unchanged and keep
validating until then.

### Migration path

1. **Read the artifacts from `opensoft/openXwallet` at `wallet-v1.1`** rather than
   from this repository. The bytes are identical; the byte-identity floor was
   proven once against the named carve commit at `wallet-v1.0`, and `wallet-v1.1`
   is one auditable additive-minor diff on top that touches none of the eight
   digested artifacts.
2. **Pin them through `contracts/openxwallet-pin.yaml`**, which arrives in this
   repository at the major. Until it lands, a consumer that pins this bundle
   continues to consume the eight artifacts from here exactly as before — no
   consumer action is required BY THIS RELEASE.
3. **Resync a pin using `openXwallet/docs/pin-resync-runbook.md`** in the target
   repository, which is the procedure for moving a recorded wallet pin forward.
4. **The conformance validator moves with the contracts.** From the major forward,
   this family's conformance validator is the pinned openXwallet
   `scripts/validate-openxwallet.py` at the digest
   `contracts/openxwallet-pin.yaml` records. The `:251-252` "update to the
   conformance validator" obligation is discharged by that move — the move IS the
   update. `scripts/validate-openxwallet.py` in THIS repository is not edited by
   this release.

### How a consumer actually finds out

`scripts/check-openxfactory-pin.py` — the one domain-pin checker with a warning
tier — now reads the manifest AT THE COMMIT A CONSUMER PINS and emits a WARN-tier
notice naming every relocating artifact with its target repository and tag. **It
stays green**: WARN exits 0, exactly as it did before, and the notice is additive
to the pin verdict rather than a replacement for it. A consumer pinned to
`contract-v1.45` or earlier sees nothing new.

The sibling checker `scripts/validate-domain-openxfactory-pins.py` is deliberately
NOT the emitter: it has no warning tier, so a relocation notice there would be an
ERROR and would red every domain that pinned this perfectly legal bundle — the
precise failure the manifest-carried marker was chosen to avoid.

LedgerxFactory bumps `stack.yaml` `xfactory.contract_ref` to this minor and adds
that checker to its estate run, so the one live consumer OBSERVES the warning
inside the deprecation window rather than after it.

### Rollback posture, recorded before the fact

A published bundle is not unpublished. The honest reversal of this release is a
FOLLOWING minor that removes the marker — never a revert of the cut.
## contract-v1.46 — 2026-08-27 (additive; AVC-09 and AVC-10 leave the reserved set)

Realizes `qualify-avatar-live-voice` §2 and §3 — the change ratified 2026-08-27
that turns on real voice — by publishing the two avatar-client identifiers the
kernel deliberately RESERVED at `contract-v1.7` and named this change as the
owner of. TWO CONTRACTS ARE ADDED:
[`avatar-client/avc-09-voice-adapter-descriptor.schema.yaml`](avatar-client/avc-09-voice-adapter-descriptor.schema.yaml)
and
[`avatar-client/avc-10-voice-latency-sample.schema.yaml`](avatar-client/avc-10-voice-latency-sample.schema.yaml),
both content-addressed by their per-file `sha256` in
[`manifest.yaml`](manifest.yaml). Four existing avatar-client members are
RECOMPUTED in this cut because their bytes moved with the release:
`interface-lock.yaml`, `acceptance-map.yaml`, `evidence-register.yaml`, and
`fixtures/index.yaml`.

**Change class: ADDITIVE (minor)** under
[`docs/contract-versioning-policy.md`](../docs/contract-versioning-policy.md).
Two NEW schemas are added and no existing shape changes: no property is
removed, no required field is added to any existing contract, no enum member is
withdrawn, and no instance valid at `contract-v1.45` is narrowed or
invalidated. A consumer pinned at `contract-v1.45` stays conformant until it
deliberately reads AVC-09 or AVC-10. Every avatar-client
`contract_schema_version` stays `1`, and the new rows' `schema_version` is `1`
with them.

### The reserved shapes, used AS-IS

Both schemas are the shapes the kernel's neutral-contracts note reserved,
published unchanged. AVC-09 distinguishes SERVER and CLIENT adapter components
and records adapter identity and version, provider, supported profiles, the
requested model alias or snapshot, the provider-resolved model,
prompt/policy/voice/turn configuration versions, capability and event mapper
versions, authorization mode, sideband readiness, the direct-media requirement,
contract compatibility, region and data controls, and
experimental/candidate/approved/retired status. AVC-10 carries sample, session,
media-leg and turn identity, adapter and profile, platform, network class,
region, clock source and quality, the twelve RAW monotonic markers, the DERIVED
intervals, the direct-or-brokered reference classification, and a reproducible
fixture reference.

**AVC-09 CARRIES NO NUMERIC LATENCY-BUDGET FIELD, and its `not` refuses one
however it is spelled.** That is Fork 2's ruled Option C. Latency gating is the
neutral relative-regression SLO — more than 15 percent relative OR more than 150
milliseconds absolute, whichever is GREATER — which lives in
`avatar-client/acceptance-map.yaml` as exactly one entry, and the measured
numbers live in AVC-10 samples the descriptor merely REFERENCES. A per-profile
absolute ceiling frozen into a neutral contract is the Option B that was not
ruled, and freezing one here would have made the contract, rather than the
evidence, the thing a profile is judged against.

Neither schema can carry secret material or raw content: provider keys,
ephemeral client secrets, SDP, transcripts, captions, media and raw provider
payloads are all structurally excluded by `not` rather than by convention, so
additive evolution cannot reintroduce them.

### The unreservation, and what stayed reserved

`avatar-client/interface-lock.yaml` moves EXACTLY `AVC-09` and `AVC-10` from
`frozen.reserved_identifiers` into `frozen.contracts`. `AVC-03` (absorbed inline
on the AVC-02 grant) and `AVC-05` (a registered AVC-04 event payload) STAY
reserved; `reserved_retention_classes: forbidden` and the frozen
`consent-purposes: 3` are untouched, and no identifier is reused.

`scripts/validate-avatar-client.py` moved in the SAME commit, because it had to:
its reserved-id guard fail-closes on the mere EXISTENCE of an
`avc-09-*.schema.yaml` file, so a schema landing one commit ahead of the
constant would have redded the repository between commits. It gains two new
fail-closed rules with the move — `interface_lock_reserved_set`, which
machine-checks the lock's two lists against the validator's own constants so the
hand-mirroring cannot drift again, and `latency_posture`, which enforces exactly
one relative-regression SLO entry at the ratified threshold, the disjointness of
the gated tier (p50 and p95 on the two setup intervals, Windows desktop and web
canvas at nominal network) from the recorded tier (p99, teardown, degraded and
jittered network), and the refusal of any per-profile numeric latency ceiling
presented as a gating field.

### Packaged fixtures

Ten cases join `avatar-client/fixtures/index.yaml`. AVC-09: one valid
internal-live descriptor plus four negatives — a descriptor carrying a numeric
latency budget, one carrying secret material, one whose closed client component
carries a server provider configuration, and an `approved` status claimed with
no latency evidence behind it. AVC-10: two valid samples (one governed, one
direct-provider reference) plus three negatives — a sample carrying a
transcript, one carrying SDP, and one carrying an unrecognized marker.

A refusal of a COMPARISON cannot be expressed as a single-instance schema case,
so the two-tier posture is proved by a new self-describing
`latency_comparison_cases` block executed by the validator, the way
`release_pin_cases` proves the pinning rule: ten comparisons covering a material
regression that fails, a small absolute regression on a fast interval that
PASSES because materiality takes the greater threshold, a gated pass on the
second interval, p99 and teardown recorded rather than gated, and five refusals
— cross-platform, degraded-network, Linux-CI, region-mismatch, and
adapter-versus-adapter.

RELEASE OBLIGATION STILL OPEN AT THIS ENTRY: per the versioning policy,
CHANGELOG presence is the availability test and the annotated tag is cut at the
realization merge. The release DIGEST INVENTORY
(`releases/contract-v1.46.digests.yaml`) ships INSIDE this cut, as
`contract-v1.34` through `contract-v1.45` all did. `qualify-avatar-live-voice`
itself archives only on merged plus green internal-live realization evidence —
never on this cut landing.

## contract-v1.45 — 2026-08-26 (additive; the `approve-model` gate action and the turn record's mid-turn re-mint)

Realizes `add-doxchat-model-intake` §3 (tasks 3.3 and 3.6) — the ratified
requirements *"Intake proposes a model; approval stays a recorded human act"*
and Brett's ruling of 2026-08-26 that a mid-turn re-mint and the paid retry it
buys are visibly recorded in the turn record. TWO CONTRACTS change:
`schemas/gate-action-record.schema.yaml` and
`schemas/xfactory-workbench-chat-turn.schema.yaml`. Both are content-addressed
by their per-file `sha256` in [`manifest.yaml`](manifest.yaml); both rows'
digests are RECOMPUTED in this cut, and both `consumption_rule`s name what
arrived.

**Change class: ADDITIVE (minor)** under
[`docs/contract-versioning-policy.md`](../docs/contract-versioning-policy.md).
Every addition is an OPTIONAL property or a new enum member constrained by a
conditional that fires on that member alone. Nothing previously valid becomes
invalid, no required field is added to any existing shape, no shape is removed,
and no existing record is reinterpreted. Both schemas' `contract_schema_version`
stays `1`, and both manifest rows' `schema_version` stays `1` with them.

### `gate-action-record`: the act that makes an added model available

`action` gains **`approve-model`**, and it exists because "approved" was
previously NOT A RECORD AT ALL. Availability was the conjunction of three
runtime facts — the entry sits in the `ModelCatalog` the install handed to its
model port, its `available` flag is true, and the console passed the loopback
local-human verdict — with no approver, no instrument, and nothing written down.
That is defensible while the only way to add a model is to edit a settings
document, since whoever can do that IS the operator by definition. **A wizard
breaks the implication**: if completing an intake flow set `available`, then
supplying a payment credential would be the same act as approving a provider to
process governed corpus material, and the control the human is looking at
already says "approved model". Those are two decisions and this action is the
second one.

Two OPTIONAL properties arrive with it, and both are required BY THE
CONDITIONAL rather than unconditionally, which is what keeps the cut additive:

* `target.model_declaration` — the declaration this action approved, named by
  the model-provider BINDING id it carries. That identifier is also the catalog
  handle a turn selects, so one string resolves the whole chain: this record,
  the declaration in the install's settings document, the binding that names the
  broker and the credential reference, and the menu entry the human picks. It is
  deliberately NOT the credential reference and NOT a provider account
  identifier: a governance record names the thing that was decided about.
* `model_approval` — the grant accountability, in
  `credential-contracts`' own field names rather than a second vocabulary:
  `issued_by`, `approved_by`, `expires_at`, `audit_ref`, plus `install_posture`.
  That family already holds that a grant template lacking the first four is
  invalid, and a model reached through a credential broker is a
  credential-bearing capability answerable in exactly those terms. `audit_ref`
  is the reference the broker returned when it took custody; it is disclosable
  by construction, because the broker's declaration records no token material
  against an audit reference.

`install_posture` is the one field with no precedent, and it encodes **Brett's
OQ-3 ruling of 2026-08-21**, which splits BY INSTALL: a recorded gate action
suffices on a single-operator loopback console — the human is spending their own
subscription on their own corpus, and requiring a consent instrument there is
ceremony without a second party — while a tenant or shared install, or a turn
that will process another party's material, REQUIRES a consent instrument. Two
conditionals inside the block enforce both halves: `consent_ref` is REQUIRED on
`shared` and REFUSED on `single-operator`. The refusal half is deliberate and is
not the inverse of the first: a single-operator record carrying a consent
reference would claim a second party that does not exist, and the ruling's words
are that ONLY the shared case carries one. The posture is STATED rather than
inferred from which fields happen to be present, because a record whose rule has
to be reconstructed from its own shape cannot be read back against the ruling it
was made under.

The new conditional requires NO artifact kind, and that is a decision rather
than an omission, on the `abandon-session` and `share-session` precedent: this
action produces no commit, no document, no pull request and no workflow-job.
Its own artifact IS the record, and the settings document it unblocks is written
after the record exists — that ORDER is a runtime obligation, not a schema one,
and it is the safe order: a crash between the two leaves an audit record for an
approval that did not take effect, which is readable and recoverable, rather
than an available model no record accounts for.

### `xfactory-workbench-chat-turn`: what the turn cost beyond one call

`success_v2` gains the OPTIONAL **`provider_retry`**, and the v1 success
envelope does NOT — the v1 family is deprecated at contract-v1.34 with removal
target contract-v2.0, and its promise is byte-identical stability.

`add-model-provider-broker` built the behaviour: when a minted token expires
part-way through a turn the port re-mints and retries ONCE, and a second expiry
in the same turn refuses rather than buying a third call. Brett's ruling of
2026-08-26 attached a condition to that behaviour — the re-mint and the paid
retry are **visibly recorded in the turn record** — and that change could not
discharge it. Recorded here because the reason is a property of these contracts:
`workbench-chat-turn-success` and `workbench-chat-turn-v2-success` are RELEASED,
digest-pinned, `additionalProperties: false`, and self-validated by the route
before an envelope is stored or sent, so the fact could not reach the browser
without a release act — and that change declares `target_release: none` while
this one owns the turn-record surface and pays for a schema cut. What it built
instead was three real records — the port's content-free mint ledger, the
console's stderr notice, and the broker's own `broker-audit.jsonl` correlated by
`--retry-of` — none of which a browser can read. This field is how the fact
reaches the person paying for it.

The shape carries the REDACTED fact and nothing more: `retried` and
`at_most_once`, both `const: true`, plus the re-mint's `audit_ref`. There is no
`retried: false` spelling, on purpose — a turn that did not retry omits the
whole object, and a second, weaker way to say an absence that is already
unambiguous is how a consumer comes to read the wrong one. `at_most_once`
records that the ruling's BOUND held, which a reader would otherwise have to
know the port's internals to infer. The object is `additionalProperties: false`
because this record is stored, mirrored into a thread sidecar on a session
branch, and rendered in a page: a key nobody declared is a key nobody redacted,
and the one thing a re-mint must never carry is the token it minted.

ABSENCE IS NOT A CLAIM, exactly as it is not for `context_packet` at
contract-v1.40: a record without the key means its producer predates
contract-v1.45 or had nothing to report, never that no retry occurred. A
consumer that reports what a turn cost MUST read this key; one that does not may
ignore it, and every pre-existing v2 record stays valid — which is what makes
this half of the cut additive too.

### Packaged fixtures

Two valid instances and three negatives join `examples/ideation-dashboard/`:
`gate-action-record-approve-model` and
`workbench-chat-turn-v2-provider-retry`; `gate-action-approve-model-without-approval-block`,
`gate-action-approve-model-shared-install-without-consent`, and
`workbench-chat-turn-v2-provider-retry-carries-a-token`. The validator
self-tests them (valid pass, each negative fails for its intended reason).

RELEASE OBLIGATION STILL OPEN AT THIS ENTRY: per the versioning policy,
CHANGELOG presence is the availability test and the annotated tag is cut at the
realization merge. `add-doxchat-model-intake` task 4.2 carries the tag +
submodule-pin half, and that change archives only on merged plus green. The
release DIGEST INVENTORY (`releases/contract-v1.45.digests.yaml`) ships INSIDE
this cut, as `contract-v1.34` through `contract-v1.44` all did — it is part of
the cut, not part of the tagging.

## contract-v1.44 — 2026-08-26 (additive; the release verifier resolves its remote operand before it compares)

**Change class: ADDITIVE (minor)** under
[`docs/contract-versioning-policy.md`](../docs/contract-versioning-policy.md).
NO SCHEMA BYTES CHANGE: nothing under `contracts/schemas/` moves,
`contract_schema_version` is unchanged, no field is added, deprecated or
removed, and no instance valid at `contract-v1.43` is narrowed or invalidated.
A consumer pinned at `contract-v1.43` remains conformant until it deliberately
upgrades. No finding code is added, removed, renamed or re-severitied, and
`HGR-RELEASE-CANDIDATE-UNREACHABLE` / `HGR-RELEASE-TAG-UNREACHABLE` fire on
exactly the population they fired on before.

WHY THIS CUT EXISTS, stated as membership rather than as preference:
`scripts/hermes_runtime_validation/release.py` is a NON-EDITORIAL member of
`contract-v1.43`'s own digest inventory
(`contracts/releases/contract-v1.43.digests.yaml`, `type: validator`, recorded
digest `sha256:d149a34b...`, which is exactly what the tree carried before this
change). Editing it would leave that declared inventory describing bytes the
repository no longer holds — the state `release-surface-integrity` names a
defect for any member outside the editorial three, that `doc-health`'s
release-inventory drift family reports at `error`, and whose prescribed remedy
is a release cut and never a hand-edit of an inventory to match a tree. THE
PRECEDENT IS THE SAME FILE FOR THE SAME CAUSE: `contract-v1.10` was cut as a
superseding additive re-realization because finding F-U3 hardened release
membership and thereby changed this very file, so the frozen `contract-v1.9`
inventory stopped reproducing the tree.

WHAT MOVED:

* `scripts/hermes_runtime_validation/release.py` — the release verifier asked
  the canonical remote a LIVE question (`git ls-remote refs/heads/main`, and the
  tag advertisement) and answered it out of a STATIC local object store (`git
  merge-base --is-ancestor`, `git ls-tree`, blob reads). A clone is fixed at the
  moment it was taken; the remote's refs are not. When `main` advanced after the
  clone, the advertised object was simply absent locally, `merge-base` exited 128
  rather than 0 or 1, and the verifier refused with "commit reachability could
  not be determined" — a fail-closed refusal produced by somebody else's merge
  rather than by anything about the candidate. MEASURED on openxFactory PR #372,
  a doc-only change: one tree, three attempts, two failures and one pass, with a
  merge landing on `main` inside each failing window and none inside the passing
  one. The fix puts the obligation on the OPERAND rather than on the comparison:
  a new `_resolve_remote_object` probes with `git cat-file -e`, so an
  already-current clone spends nothing, and otherwise fetches THE SINGLE NAMED
  OBJECT (`--no-tags --no-write-fetch-head`, leaving the clone's refs and
  `FETCH_HEAD` untouched) from the remote that just named it. It is called where
  each remote-derived object id ENTERS the local world, which covers all four of
  its readers by construction: the candidate ancestor check, the
  release-surface comparison and its per-member blob reads, the published-tag
  ancestor check, and the tag's tree walk in `_verify_release_at`.
  `_is_ancestor`'s 128-branch refusal is DELIBERATELY UNCHANGED as the last line
  of defence, and a mutation proof depends on it still being there.
* Three outcomes are now told apart and named. A candidate genuinely not on
  published `main` keeps its existing refusal finding, unchanged. Transient skew
  resolves in the fetch and produces no finding at all. An object that cannot be
  made available stays a fail-closed dependency refusal — never a finding, never
  a pass, never a "not reachable" verdict invented from an absence — but its
  reason now NAMES THE RETRIEVAL (`remote object fetch failed: <remote> <oid>
  (git exit <n>)`) instead of announcing that reachability could not be
  determined, because the reader's next action differs completely between
  checking a candidate and checking a network or a credential. It claims NO
  cause beyond the failed fetch and its exit status: a fetch can fail for a
  refused credential, an unreachable host, a timeout or a remote that declines
  the object, and naming one of them unobserved would be the same failure of
  diagnosis the message replaces (openxFactory pull request #390, Copilot
  review, accepted).
* `tests/hermes_runtime_contracts/test_release_inventory.py` — six new proofs
  over the module's established `_bare_origin` fixture pattern, which DRIVE the
  condition rather than describing it: a second clone advances the bare origin's
  `main` so the verifying repository genuinely lacks the advertised object. Two
  skew proofs (`verify_promotion`; and `verify_tag` with BOTH its operands
  absent, tag and main tip alike), one release-surface proof asserting the drift
  verdict the surface actually warrants rather than the false drift an
  unresolved object would produce on every surface path, one unavailable-object
  proof asserting the refusal and its reason, and a two-case mutation proof
  demonstrating that removing the resolution step alone reproduces the original
  128 refusal.
* **A negative ancestry verdict is no longer trusted in a truncated history.**
  Resolving the operand makes the OBJECT present; it does not make the ANCESTRY
  present. A shallow clone's graft boundary declares its oldest commits
  parentless, so `git merge-base --is-ancestor` returns a definite 1 for a commit
  that is reachable on the real history — which would have turned this cut's own
  fix into a FALSE `HGR-RELEASE-TAG-UNREACHABLE`. Measured against the canonical
  remote in a `--depth 1` clone, and raised independently in review.
  `_refuse_unreachable_in_a_shallow_clone` runs `git rev-parse
  --is-shallow-repository` on the FALSE branch of each ancestor check only, and
  in a truncated store raises `ancestry cannot be judged in a shallow clone`
  instead of emitting the unreachable finding. THE ASYMMETRY IS THE RULE: a
  positive answer is honoured in any store, because a path git found is a path
  that exists, so only the negative is re-examined — one local `rev-parse`, never
  on the ordinary path, no network. A shallow clone holding a genuinely
  unreachable candidate takes the refusal as well, which is deliberate: the
  verifier cannot tell an earned negative from an artefact of its own store, and
  a fail-closed refusal naming the truncation is honest about both. Ruled by
  Brett 2026-08-26 (openxFactory pull request #390).
* `contracts/hermes-runtime/evidence-register.yaml` — the new proofs are bound
  in place under the `SCO-002` scenarios they serve (`S02` published-tag verify,
  `S03` pinned-file drift, `S04` verification without a usable network). Test
  node ids added to existing scenarios; no scenario id added.
* `contracts/CHANGELOG.md` and `contracts/manifest.yaml` — the editorial
  members, re-baselined.

A FORTUNATE PROPERTY, worth stating rather than discovering: the verifier's fix
is verified BY the verifier as part of the cut that carries it.
`verify-promotion` runs before the tag, so if the fix were wrong the release
carrying it would be the first thing it failed.

Realized by `fix-release-reachability-race`.

## contract-v1.43 — 2026-08-25 (additive; cleanup retention evidence becomes exact and transactional)

**Change class: ADDITIVE (minor)** under
[`docs/contract-versioning-policy.md`](../docs/contract-versioning-policy.md).
The cleanup action and demotion receipt are new contract shapes; no instance
valid at `contract-v1.42` is narrowed or invalidated. Existing consumers may
remain pinned until they adopt abandoned-session cleanup or demotion evidence.

- **Additive (minor)**: `contracts/openxwallet/openxwallet-grant.schema.yaml`
  gains an `issuer_identifier` def and `issued_by` moves to it — the issuer
  grammar is the identifier grammar plus `@`, so a review-authority root grant
  can record its issuer as the responsible OPERATOR's email address
  (`Brett.Heap@opensoft.one`), anchored outside the register under the Human
  Escalation Contract. Every other identifier field keeps the strict
  machine-id grammar unchanged (`012-wallet-issuer-anchor`, S2 of
  `add-wallet-carried-review-authority`; convener-authorized schema widening
  2026-08-24, overriding that substrate item's initial no-schema-edit
  posture, with the manifest entry's sha256 refreshed to match).
  **Annotation (contract-v2.0, `split-openxwallet-repo` P3):** the path
  named in this published entry left openxFactory at `contract-v2.0`. The
  artifact is unchanged and now lives at `opensoft/openXwallet`, consumed
  here through [`openxwallet-pin.yaml`](openxwallet-pin.yaml). The record
  above is annotated rather than rewritten: at `contract-v1.43` the path
  was correct.
- **Additive (minor)**: `contracts/client-content/client-overlay.schema.yaml`
  — `hermes_client_overlay` gains the OPTIONAL `client.policy_namespace` +
  `client.policies` pair, so a **Tenant** layer may carry FREESTANDING
  company-wide standing policy and not only deviations from the domain
  baseline (`declare-client-standing-policy-contract`, closing
  `opensoft/openxFactory#254`). `policies` is a non-empty mapping keyed by
  policy id whose entries restate their own `policy_id` and `policy_namespace`
  and keep an OPEN body, so a named tenant policy is addressable as
  `<policy_namespace>/<policy_id>` and materializes to `policy_position` — the
  same content kind, and therefore the same row shape, that the Domain and
  Subject seats already use, which is the entire point of a namespaced
  address. A faithful mirror of `subject.policy_namespace` +
  `subject.policies` in
  `contracts/hermes-domain-overlay/hermes-subject-overlay.schema.yaml` one
  layer up, with ONE deliberate difference: **no `relation_to_*` field**. A
  tenant's standing policy is a POSITION, not a deviation, so there is no
  baseline for it to declare a relation to.
- **Declared INLINE, no new file, no new manifest row.** The three sibling
  `client-*.schema.yaml` files each govern a self-identifying sub-document
  that dispatches on its own inner `kind:`; these two entries carry no `kind`
  and are not documents, so a fourth sibling would add a schema nothing
  dispatches to. The subject family answered the same question the same way.
- **`client.required` is byte-frozen** at `[ref, display_name,
  policy_overrides]`. An overlay that declares neither key takes exactly the
  verdict it took before the block existed, and no consumer is forced to
  re-pin; only a consumer that wants to USE the block needs the new tag.
  `contracts/manifest.yaml`'s `client-overlay` row digest is RECOMPUTED in
  this cut (the schema file's bytes changed) and its `consumption_rule` states
  what a consumer must now read and what it may still ignore.
- **`scripts/validate-client-content.py`** learns the six rules the shape
  cannot express — non-empty map with a DECLARED-BUT-EMPTY REFUSAL and a
  distinct wrong-type finding; per-entry mapping; `policy_id` non-empty and
  equal to its key; entry `policy_namespace` non-empty and equal to
  `client.policy_namespace`; `client.policy_namespace` required non-empty
  WHEN AND ONLY WHEN `policies` is present; `<namespace>/<id>` uniqueness —
  plus a prohibited-domain-block and credential-value scan **scoped to the
  `client.policies` subtree only**, deliberately narrower than the subject
  path's whole-document walk so an ADDITIVE change cannot re-decide the
  verdict of an overlay that uses none of it. Its self-test now sweeps EVERY
  packaged positive rather than one hardcoded filename; one new positive and
  eight new negatives ship with it.
- **Additive (minor)**: `contracts/schemas/gate-action-record.schema.yaml`
  registers `cleanup-abandoned-branch` with an exact tile/ref/head, correlated
  abandonment and retention-release evidence, and a `prepared`/`completed`
  transaction status. Machine evidence requires the preserving change id,
  nonempty references, and a durable recording time; explicit release keeps
  its separately recorded human reason.
- **Additive (minor)**:
  `contracts/schemas/demotion-execution-receipt.schema.yaml` is registered for
  the first time. An executed receipt now accounts for every exact from/to
  move, asserts source-folder removal, and restricts its manifest and returned
  artifact references to repository-relative paths. Runtime validation joins
  it to the exact transition manifest and verifies the returned artifacts
  still exist before cleanup accepts it.
- **Validator and examples**: the ideation-dashboard validator enforces exact
  cleanup target/scope equality, complete machine evidence, matching explicit
  reasons, exact demotion destinations, and safe repository paths. Packaged
  negatives cover empty machine evidence, mismatched cleanup scope, mismatched
  demotion destination, and traversal.
- **Release identity**: the delegated ideation-dashboard validator joins the
  closed release inventory's named-validator set, so the validator referenced
  by these schema consumption rules is pinned by raw-blob digest with the
  contract instead of being named but unaddressed.
- **Realization**: `contract-v1.43` was allocated only after rebasing and
  confirming the tag was available. The manifest, changelog, contract index,
  schema digests, and candidate release inventory move atomically in this cut;
  the annotated tag is published only after this exact reviewed commit lands
  on `origin/main` and passes `verify-promotion`.

## contract-v1.42 — 2026-08-25 (additive; the untagged-bundle gap is discharged)

Cut on Brett's ruling of 2026-08-25, alongside the retro-publication of the
three bundles this policy had recorded as an undischarged gap.

**Change class: ADDITIVE (minor)** under
[`docs/contract-versioning-policy.md`](../docs/contract-versioning-policy.md).
NO SCHEMA BYTES CHANGE: nothing under `contracts/schemas/` moves, no
`contract_schema_version` advances, no field is added, deprecated or removed,
and no existing instance changes meaning. A domain repo on the same major
version remains conformant without doing anything.

WHAT MOVED, and why it owed a cut:

* `docs/contract-versioning-policy.md` — a release-surface member (the
  membership clause covers "every modified normative contract **or versioning
  document**"). Its § *Untagged Bundles After Enforcement Began* is rewritten
  from a recorded GAP to a recorded DISCHARGE, naming each bundle's realized
  commit and the rule by which that commit was established.
* `contracts/CHANGELOG.md` and `contracts/manifest.yaml` — the editorial
  members, re-baselined.

THE THREE TAGS PUBLISHED WITH THIS CUT, each at the commit its bundle was really
realized at, each verified from the remote:

| bundle | realized commit | landed as |
|---|---|---|
| `contract-v1.33` | `71674ed58e338bf3f85a7b750b64f5f5ab6d02e1` | PR #190, 2026-08-15 |
| `contract-v1.35` | `78f8e016fbddcf1125c11b7f11234fb2478b0415` | PR #220, 2026-08-19 |
| `contract-v1.39` | `1f45e427bf7b2491aec09d2a9c9adeaaa5f99839` | PR #259, 2026-08-22 |

Retro-published, not re-dated: no release was reconstructed or re-cut, and no
version number was reused. Every bundle from `contract-v1.7` — where mandatory
tag publication begins — now carries a tag.

THAT THIS CUT EXISTS AT ALL is the `release-inventory-drift` family working as
designed for the second time: editing the policy drifted a member of
`contract-v1.41`'s inventory, the family reported it as a non-editorial `error`,
and the remedy the taxonomy prescribes is a release cut rather than an edit to
make the check pass.

## contract-v1.41 — 2026-08-25 (additive; the ratified versioning policy joins the release surface)

Cut on Brett's ruling of 2026-08-25, in response to the first finding the
`release-inventory-drift` check family ever reported — which was against the
change that commissioned the family.

**Change class: ADDITIVE (minor)** under
[`docs/contract-versioning-policy.md`](../docs/contract-versioning-policy.md).
NO SCHEMA BYTES CHANGE IN THIS CUT: no file under `contracts/schemas/` moves, no
`contract_schema_version` advances, no field is added, deprecated or removed, and
no existing instance changes meaning. A domain repo on the same major version
remains conformant without doing anything. What this bundle does is RE-BASELINE
the release surface's recorded identity.

WHAT MOVED, and why each was already true before the cut:

* `docs/contract-versioning-policy.md` — a release-surface member (the
  membership clause covers "every modified normative contract **or versioning
  document**"). It was RATIFIED by `add-release-inventory-drift-check`
  (`Status: draft` → `ratified`), and that ratification corrected five defects
  the read-through found: three modern bundles published with no annotated tag
  (recorded as an undischarged gap, the rule NOT relaxed), a stale present-tense
  baseline claim, a superseded layer vocabulary called "canonical", the
  undocumented meaning of a red `verify-commit` at HEAD, and the record-only
  disposition of the `contract-v1.36` tag move. This bundle records the policy
  at its ratified state.
* `contracts/CHANGELOG.md` and `contracts/manifest.yaml` — the editorial members,
  re-baselined. They had drifted from `contract-v1.40`'s inventory across several
  commits, which is the expected bounded state between cuts that the policy now
  documents in as many words.

WHY THIS CUT EXISTS AT ALL, recorded because it is the useful part. The
`release-inventory-drift` family reported one `error` at `origin/main`:
`docs/contract-versioning-policy.md` differed from the digest `contract-v1.40`
records. That was a TRUE POSITIVE, proven both directions — run at the
`contract-v1.40` tag the family reports zero findings, and run at main it named
exactly the one member that had moved. Two remedies were available and one was
refused: reclassifying the policy into the editorial set would have been the
"hand-edit to make the check pass" that this very policy now forbids in writing.
The other is this cut, which is what the taxonomy prescribes.

The structural question the finding raised is recorded and NOT answered here:
ratifying a versioning document is itself a release-surface edit, so under the
membership clause as written, governing the policy drifts the surface the policy
governs. Either such edits owe a cut — as this one does — or the membership
clause wants revisiting. That is a separate change.

## contract-v1.40 — 2026-08-22 (additive; the doxBench chat-turn record states its assembled context's posture)

Realizes tasks.md §10.7 of `add-doxbench-editing-phase-b` — the ratified
scenario *"The knowledge service is unavailable"* and the requirement sentence
it belongs to: *"Where the knowledge service is unavailable the turn SHALL
degrade to a declared reduced packet — the selected thread and the loaded
buffers, with the reduced posture STATED — and MUST NOT bypass a rail to reach a
provider, MUST NOT silently substitute an unbounded context, and MUST NOT fail an
editor that does not need it."* One CONTRACT changes:
`schemas/xfactory-workbench-chat-turn.schema.yaml`. That schema is
content-addressed by its per-file `sha256` in [`manifest.yaml`](manifest.yaml);
that row's digest is RECOMPUTED in this cut, and its `consumption_rule` states
what a consumer must now read and what it may still ignore.

WHAT WAS ALREADY TRUE, AND WHAT WAS NOT. The packet half of §10.7 shipped with
§10 itself (PR #216): a `ContextPacket` cannot be REDUCED without
stating its reason and cannot be FULL while carrying one — enforced at
construction, not by convention — and the reduced posture is written into the
prompt's own declaration section, which is where the ratified sentence puts it.
The turn also SUCCEEDS: a live model with no knowledge service answers on the
reduced packet rather than refusing. What was NOT true is that any reader could
consult the posture. `workbench-chat-turn-v2-success` is a CLOSED envelope
(`additionalProperties: false`) with no field for one, so no conformant success
body could carry it, and the delta's own rule forbids carrying it as a
server-side value nobody can read. §10.7 therefore stayed open with its
obligation recorded against ITSELF, naming the release that would carry it.
This is that release.

VERSION ALLOCATION, RE-CUT — this release was `contract-v1.39` until the number
was taken out from under it. At this slice's branch base (`66140613`) the
CHANGELOG's newest heading and `contract_bundle_version` both read
`contract-v1.38`, so v1.39 was the next available number and this cut took it.
While it was in review, `add-roster-directory-admission-surface` landed on main
(PR #259, `5124fbcd`, merged at `1f45e427`) and ALLOCATED `contract-v1.39` for
the `directory` roster admission surface. Under
[`docs/contract-versioning-policy.md`](../docs/contract-versioning-policy.md)
the version is allocated AT REALIZATION against what is available, and CHANGELOG
PRESENCE ON MAIN is the availability test — so v1.39 is theirs and this release
is `contract-v1.40`.

BOTH SIDES SAW IT COMING, which is what makes this an orderly re-cut rather than
a collision. That entry names this branch and says so in as many words: *"an
UNLANDED branch (`change/doxbench-turn-posture-release`, `97aa19a7`) has also cut
a `contract-v1.39` in its own working state … Whichever of the two lands second
re-cuts against the CHANGELOG it then finds."* This is that re-cut. The two
releases are INDEPENDENT — theirs grows
`xfactory-client-identity-roster.schema.yaml`, this one grows
`xfactory-workbench-chat-turn.schema.yaml`, and neither touches the other's file
— so only the shared release surface merged, and their v1.39 digest inventory
ships beside this one's v1.40 untouched.

THE SAME SHAPE AS `contract-v1.38`, which was briefed as v1.37 until PR #235 took
that number mid-flight, and the difference is worth recording. v1.37 was
allocated by a cut whose own squash message still said v1.36 and which shipped NO
digest inventory, so it had to be discovered and left a red release surface
behind it. Here the taking release announced itself in its own entry and shipped
`releases/contract-v1.39.digests.yaml` complete — verified present at
`1f45e427` before this renumber — so there is no `HGR-RELEASE-INVENTORY-MISSING`
landmine on the preceding surface this time. The habit that caught it is
unchanged and has now paid three times: recheck bundle availability against the
CHANGELOG at the moment you allocate, and again at the moment you land.

THE PRECEDING RELEASE SURFACE IS GREEN, checked rather than assumed (the other
half of that habit) — and the preceding release is now v1.39 rather than v1.38,
because of the re-cut above. `validate-contract-release.py verify-commit --commit
1f45e427` PASSES against `contracts/releases/contract-v1.39.digests.yaml`.
Recorded because a preceding surface has been broken when a release got there
twice in this family's recent history (`6cbb4495`, missing inventory; and from
`e11a057b`, an inventory member edited without a rebuild), so "it verified last
time" is not the test in either direction — including this one, where it
verifies. Nothing here depends on it either way:
`resolve_committed_inventory` reads `contract_bundle_version` AT THE COMMIT, so
this cut resolves v1.40 and checks against the v1.40 inventory that ships inside
it, and their v1.39 inventory is untouched beside it.

MAIN MOVED UNDER THIS SLICE FIVE TIMES, and each time it was merged in rather
than rebased over, with availability rechecked at the merge rather than trusted
from the allocation: `2c69e743`, `0f9e14b4`, `ede82ef9` and `135d52d6` touched no
`contracts/` file and left the number free; `1f45e427` took it, which is what
this entry's allocation note is about. `verify-commit` passes at every merge.

**Change class: ADDITIVE (minor)** under
[`docs/contract-versioning-policy.md`](../docs/contract-versioning-policy.md).
ONE OPTIONAL property is added to `$defs/success_v2`, referencing ONE new closed
`$def`. Nothing previously valid becomes invalid, no required field is added to
any existing shape, no shape is removed, and no existing record is reinterpreted:
a record that carries no `context_packet` is judged exactly as it was before. The
schema's `contract_schema_version` stays `1`, and the manifest row's
`schema_version` stays `1` with it. Verified case by case against the released
bytes, including the pre-release record shape and each malformed posture.

`$defs/success_v2` gains:

* `context_packet` (optional) — an object stating the POSTURE the turn's bounded
  context packet was assembled under, and why it was reduced when it was.

`$defs/context_packet` is that object, CLOSED, with two members:

* `posture` (required) — `full` or `reduced`. Exactly two values, because
  `ContextPacket` has exactly two: the wire does not get a third spelling of a
  fact the assembler already owns.
* `reduced_reason` (`minLength` 1, `maxLength` 500 — JSON Schema counts those in
  CODE POINTS, and the shipped-reason guard below checks the stricter UTF-8 BYTE
  count against the same number, so a reason that passes the guard passes the
  shape) — present IFF the posture is `reduced`. Free prose about the ASSEMBLY,
  never about content; in the two reasons this
  capability ships it says in as many words that nothing unbounded was
  substituted and no rail was bypassed, which is the ratified sentence's own
  second and third clauses.

THE TRUTH-PAIRING IS ENFORCED, not documented. Two `allOf` conditionals, and
they are NOT each other's inverse — they guard different instances and each has
its own packaged negative and its own revert-test. `posture: reduced` requires
`reduced_reason`; `posture: full` refuses it. A posture outside the vocabulary
matches NEITHER conditional (both require `posture` to equal a named constant)
and is refused by the `enum` underneath them — the same lesson `contract-v1.38`
learned about `dependentRequired` versus `if`-conditionals guarding different
paths, read on this shape. No `dependentRequired` block is used here, and that
is deliberate: `posture` is REQUIRED, so `dependentRequired: {reduced_reason:
[posture]}` could never fire, and a clause no revert-test can make fail is a
clause that documents rather than enforces.

WHY ONE OBJECT AND NOT TWO SIBLING KEYS — a judgement call, flagged. The
`selected_model` $def one line above set the precedent for exactly this shape:
one fact about one thing, grouped. Three consequences decided it. The
present-iff rule stays LOCAL to the object that owns it rather than becoming a
cross-field rule on a ten-key envelope. The ENVELOPE's key set is then identical
for a full turn and a reduced one, so a consumer's presence check is on ONE key
— which is the ratified independence claim (*"MUST NOT ... make the editors
unusable"*) read on the wire: the two turns differ in what the record SAYS, not
in the shape it arrives in. That is asserted rather than described, by a
route-level test that drives the SAME widened request with and without a
knowledge service and requires the two records' key sets to be equal — a test
that could not have been written at all under two sibling keys, because a
reduced record would then carry one key more than a full one. (The pre-existing
key-set test on the DEPRECATED v1 lane is untouched and says nothing about this:
that envelope gains no key at all.) And a reader who wants the posture reads one
object rather than correlating two keys that could disagree.

OMISSION IS NOT A POSTURE CLAIM, and this is the consumer note that matters
most. An absent `context_packet` means the producer predates `contract-v1.40`.
It does NOT mean the context was full. A consumer that needs the posture must
read the key and treat its absence as UNKNOWN. This is the mirror image of
`contract-v1.38`'s disclosure call and the opposite conclusion, reached for the
opposite reason: there, omission and explicit-`false` had to be read as the SAME
fact, because a plain catalog entry is not a routing rule whether or not it says
so. Here they are DIFFERENT facts, because a turn always ran under some posture
and the question is only whether the producer stated it. Both packaged: the
pre-release record (`workbench-chat-turn-v2-success.example.yaml`, whose
INSTANCE is unchanged and states nothing — only its header comment gained a
paragraph saying so) sits beside `workbench-chat-turn-v2-full-context`, which
states `full` explicitly, and both are valid.

JUDGEMENT CALL — THIS PRODUCER ALWAYS STATES THE POSTURE, INCLUDING `full`.
`doxbench_turn_v2_success_body` takes the posture as a REQUIRED argument, so no
v2 record this repository builds can silently omit it, and a full turn's record
says `full` rather than saying nothing. Always-emitting was REJECTED for
`contract-v1.38`'s catalog projection and is ADOPTED here, and the difference is
what the omission would mean. There, omitting kept every existing catalog
response byte-identical and cost a reader nothing, because absence and
explicit-false were the same fact. Here, omitting on a full turn would make the
posture inferable only by absence — which is precisely the reading this release
forbids — and would leave a reader unable to distinguish "assembled full" from
"nobody checked". The cost is stated rather than hidden: every v2 success body
this server produces now carries one more key than it did at `contract-v1.38`,
as does the copy the idempotency store replays. NOTHING DURABLY STORES A v2
BODY (adversarial review N6, which caught this entry calling that store
durable): `TurnStore` is per-process, in-memory and bounded, so a replayed
record outlives the request and not the process. The durable record of a turn is
the THREAD SIDECAR on disk, and it does not carry the wire body at all — the
same boundary the sidecar gap below is about.

THE DERIVATION IS ONE FUNCTION, AND IT READS THE PACKET. `serve.py`
`doxbench_context_packet` sits beside `doxbench_selected_model` and re-states the
packet's OWN `posture` and `reduced_reason`, verbatim. It is deliberately NOT a
re-derivation from "did this serve have a knowledge service?", which would be a
second authority able to disagree with the first: a packet also reduces when a
DECLARED backend REFUSES a retrieval, and only the packet knows which of the two
happened. A route-level test drives a refusing backend and asserts the record
carries `REDUCED_RETRIEVAL_REFUSED` rather than the absent-service reason — the
case the re-derived implementation would get exactly backwards.

FAIL-CLOSED, NEVER A GUESSED POSTURE. The derivation runs INSIDE the route's
existing packet boundary, so a packet that contradicts itself about its own
posture — which `ContextPacket` cannot construct, but the INJECTED, duck-typed
`packet_assembler` seam could hand back — is a `PacketError` mapped to the fixed
`invalid_turn_request`, with nothing dispatched. Four such cases are tested
through the real seam. A defaulting derivation (`getattr(packet, "posture",
"full")`) would have shipped a record claiming a full context for every one of
them.

TWO DELEGATED RULES, in `scripts/validate-ideation-dashboard-contracts.py`
(`check_context_packet`), the family's declared owner. The first — the pairing —
the SHAPE also expresses, and it is restated on purpose: it is this release's
whole truth-claim, and `contract-v1.38`'s review found a file gate that had grown
strictly weaker than the type gate beside it while its own docstring claimed
parity. THREE gates now assert this one rule (the two conditionals,
`ContextPacket.__post_init__`, and the validator), and a test asserts they AGREE
on the packaged corpus rather than leaving it to prose. The second — that
`reduced_reason` is LINTED for credential and endpoint spellings exactly as a
failure's `message` is — the shape CANNOT express, and this is the only place it
lives; it is the one new free-prose field the release adds, and the
leak-through-an-allowed-field class the failure lane already watches applies to
it unchanged.

THAT SECOND RULE IS A LINT AND THE ENTRY SAYS SO. It is a spelling heuristic
over free prose, with misses in both directions: it refuses innocent text that
happens to say `api_key`, and it passes a real token whose shape it does not
know. It raises the cost of a careless paste; it does NOT establish that a
reason is secret-free, and a consumer must not read a clean scan as if it did.
What is structural here is the producer, not the scan: the reasons this
capability emits are MODULE CONSTANTS rather than formatted provider errors, so
no value flows into the field for a scan to have to catch.

THE RESTATED PAIRING IS A DIAGNOSTIC, NOT AN INDEPENDENT GUARD — found by
revert-testing, recorded rather than dressed up. Disabling both pairing arms in
the delegated validator leaves its own packaged self-test GREEN, because the
SHAPE refuses the same two instances anyway. That is the same class
`contract-v1.38`'s revert-testing found for its separator-collision and
self-reference arms, and it is handled the same way: the arms are pinned on
their finding CODE by a test, which is the only guard that fails when they are
deleted. They earn their place as defence in depth and as the diagnostic a
consumer reading validator output actually gets — not as a second refusal.

A THIRD RULE WAS CONSIDERED AND REJECTED: requiring the reason to SAY that
nothing unbounded was substituted and no rail was bypassed. Both shipped reasons
do say it, and a rule to that effect would be prose-matching a contract — it
would refuse a conformant producer whose honest reason is worded differently and
pass a dishonest one that quoted the sentence. What the wire can check is that a
reduction is STATED; whether the statement is TRUE is the assembler's rail,
enforced where the rails run.

THE CEILING IS ENFORCED BY THE PRODUCER, PRE-DISPATCH, and an earlier draft of
this entry claimed a guard that did not exist. The route self-validates every
success body against the released schema and answers `response_invalid` if it
refuses — so without a producer-side bound a reduction reason past the ceiling
turned a degraded-but-successful turn into a 502 AFTER a provider dispatch had
been paid for, on the one path nobody exercises by hand. Measured, not supposed.
`serve.doxbench_context_packet` now refuses an over-long reason where the reason
is carried onto the record, in CODE POINTS so it refuses exactly what this shape
refuses and no conformant record more; its constant is pinned to this file's
`maxLength` by a test. A second test holds every shipped `REDUCED_*` constant to
the STRICTER UTF-8 byte count — a rule about text this repository authors, not
one the wire imposes. The reason is never truncated to fit; truncating a
statement about a degradation is how a degradation goes quiet.

THE SURFACE HALF, which is why this release exists rather than being a
record-only growth. §10.7's gap was never that the posture was unknown — it was
that the human whose answer had quietly changed could not see it. The rail now
renders one live-announced note under the transcript, `reduced context: <the
reason>`, for a turn that ran reduced, and NOTHING for a full one — un-hidden
BEFORE its text is written, because a `hidden` node is out of the accessibility
tree and text written into one is announced by nothing (the `aria-live`
attribute reads the same either way, so the ORDER is what a probe has to pin),
and written only when its text CHANGES, because re-writing a live region with
the same sentence re-announces it on every keystroke: a standing
"full context" badge is a line every operator learns to stop reading, which is
exactly how the reduced one would stop being noticed. A node probe mounts the
SHIPPED `doxbench-chat.js` bytes and drives real turns through it — reduced
renders the note and the reason, full renders nothing, a record with no posture
renders no phantom badge, and both self-contradicting records render silence
rather than half a statement.

JUDGEMENT CALL — THE NOTE IS RAIL-LEVEL AND DESCRIBES THE TRANSCRIPT'S LAST
ASSISTANT ANSWER, not a per-turn badge in the transcript. Per-turn was designed
and rejected: the browser transcript is restored from the SERVER'S THREAD SIDECAR
when a human switches documents, and the sidecar records no posture, so per-turn
badges would be present on a lived-through turn and absent on the byte-identical
restored one — a difference the reader would have to explain away. The note
therefore changes exactly when that answer changes, and every path that replaces
the answer already replaces the posture beside it — FOUR of them:
`settleTurnSuccess`, `adoptThreadTranscript`, `rekeyChatState`, and
`restoreChatState`, which adopts the posture the browser-local chat SNAPSHOT now
carries so the disclosure survives a tile being closed and reopened. That
snapshot field is optional and needs no version bump: an older blob lacks it and
restores to posture-unknown, which renders no note and is the pre-release
behaviour exactly. A flight STARTING replaces no
answer and moves nothing: an earlier draft cleared the note there, and a reduced
answer followed by a FAILED follow-up then lost its disclosure while still
holding the transcript — the same lost-badge defect the per-turn rejection was
about, at rail level.

JUDGEMENT CALL, FLAGGED — THE THREAD SIDECAR IS NOT EXTENDED. The durable
transcript on disk names the turn id, the model and the bound buffer, and it does
not name the posture. Extending it was considered and REJECTED on the format, not
on the merit: `doxbench_threads._parse_turn` refuses any turn header that does not
split into EXACTLY three fields, so a fourth would make every sidecar already on
disk unreadable by the new parser and every new sidecar unreadable by the old
one — a breaking change to a durable record, inside an additive release. This is
recorded as a GAP rather than papered over, and it is the honest counterpart to
`contract-v1.38`'s F3 finding (which caught the sidecar naming the wrong model):
a reader of a thread file can learn WHICH MODEL answered and cannot learn WHAT
CONTEXT it answered on. Closing it needs a sidecar format migration, which is a
successor change's act.

THE DEPRECATED v1 SUCCESS ENVELOPE IS NOT WIDENED, and this is the second
recorded v1 limitation of this family (the first was `contract-v1.38`'s, about
the requested versus the answering model). `workbench-chat-turn-success` has no
`context_packet` and gains none, so a v1 turn that ran on a reduced context
SUCCEEDS — the ratified *"MUST NOT ... make the editors unusable"* half — and
cannot say so on the wire. The reduction is still stated where it always was,
inside the assembled packet. Widening a deprecated closed shape whose whole
promise is byte-identical stability is precisely what `contract-v1.34`'s
deprecation forbids; the migration path is the v2 envelope, which exists.
Recorded at the v1 arm in `serve.py` and pinned by a test that fails if the v1
record ever grows the key.

OWED CROSS-REPO FOLLOW-UP (recorded, not performed). This schema's description
names `codexFactory specs/010-doxbench-editor-chat/contracts/chat-turn.md` as its
consumer contract. That document is NOT in this checkout and was NOT read here,
so this entry does not assert what it says — what it asserts is the obligation:
if it enumerates the v2 success envelope's fields, it is now short by one, in the
same way `contract-v1.38`'s entry recorded for the model-catalog document.
Either way it remains CORRECT while codexFactory pins `contract-v1.27`, which is
the pin it declares, so nothing there is wrong today. It becomes wrong the moment that repository
re-pins. Updating it is codexFactory's own governed act under the domain upgrade
runbook; no file in that repository is touched here, and this entry is the notice.

RELEASE OBLIGATION STILL OPEN AT THIS ENTRY: per the versioning policy, CHANGELOG
presence is the availability test and the annotated tag is cut at the realization
squash against the commit that actually lands. The release DIGEST INVENTORY
(`releases/contract-v1.40.digests.yaml`) ships INSIDE this cut, as
`contract-v1.34`, `contract-v1.35`, `contract-v1.36` and `contract-v1.38` did —
and as `contract-v1.37` did NOT, which is the defect this file records against
it and the reason the habit is written down. The consuming runtime repin
ships with it and carries the `unpublished:contract-v1.40` sentinel for its ref,
on `contract-v1.34`'s own precedent: until the release commit exists there is
nothing honest to name, and the sentinel is spelled as a value no `stack.yaml`
can declare, so a consumer comparing against it refuses rather than matching by
accident. A follow-up commit resolves it.
## contract-v1.39 — 2026-08-22 (additive; the `directory` roster admission surface)

Realizes `add-roster-directory-admission-surface` §1–§5, the ratified extension
of the client-identity-roster closed `admission_surface` vocabulary. One
CONTRACT changes — `schemas/xfactory-client-identity-roster.schema.yaml` — and
the change adds a packaged `directory` example to
`examples/client-identity-roster/`. The roster schema is content-addressed by
its per-file `sha256` in [`manifest.yaml`](manifest.yaml); that row's digest is
RECOMPUTED in this cut. (The roster schema is not a release-inventory member —
inventory membership is the `contracts/hermes-runtime/contract-index.yaml`
catalog plus the Decision-10 auxiliaries — so this cut's digest inventory
changes only where `manifest.yaml` and this changelog change. Checked, not
assumed, per task 4.5.)

VERSION ALLOCATION. `contracts/manifest.yaml` read `contract-v1.38` at
realization, so this cut allocates `contract-v1.39`. Noted because an UNLANDED
branch (`change/doxbench-turn-posture-release`, `97aa19a7`) has also cut a
`contract-v1.39` in its own working state; under the availability test this
changelog itself records at v1.38 — the version is allocated AT REALIZATION
against what is AVAILABLE, and CHANGELOG PRESENCE on `main` is the availability
test — v1.39 was unallocated when this ran. Whichever of the two lands second
re-cuts against the CHANGELOG it then finds.

**Change class: ADDITIVE (minor)** under
[`docs/contract-versioning-policy.md`](../docs/contract-versioning-policy.md).
A `oneOf` const member is added to `$defs.admission_surface`; nothing
previously valid becomes invalid, no required field is added to any existing
shape, no shape is removed, and no existing roster is reinterpreted, so a
domain on the same major version stays conformant WITHOUT CHANGES. The one
coupling is NAMED rather than denied: `per_unit_principal_available` closes its
key space with `propertyNames: {$ref: "#/$defs/admission_surface"}`, so
admitting `directory` DOES widen that closed key space — but purely
PERMISSIVELY and purely by DERIVATION. A record can only meet the widening by
CHOOSING to write a `directory` key it had no reason to write before; every
fragment naming `business_central`, `exchange` or `device` validates
byte-identically. `legend.*`'s sub-maps close on `free_token`, not on
`admission_surface`, and are untouched. The schema's own
`contract_schema_version` stays `1`, and the roster row's `schema_version`
stays `1` with it — vocabulary-member admission is governed by the schema's
EXTENSION ROUTE text, not by the object-shape/key-space growth that would take
a `contract_schema_version` bump.

`$defs.admission_surface` gains a fourth member, `directory`: the Microsoft
tenant DIRECTORY AND SERVICE ESTATE — the organization profile and its
subscribed service plans, the tenant's service principals/applications, and its
verified domains — admitted as ONE tenant-wide READ surface. Its admission act
is admin consent for the read-only application roles `Organization.Read.All`,
`Application.Read.All` and `Domain.Read.All` on ONE Entra app registration;
its scoping mechanism is tenant-wide read with exact effective scopes and no
narrower provider selector (`enforcement_mode: logic_enforced`, no per-unit
principal available); it is read-only. Because the governed unit IS the tenant
directory and service estate — a complete tenant service-surface inventory is
what read-only DISCOVER is for — tenant-wide read is the GOVERNED scope, not
excess.

THE READ/MUTATE BOUNDARY THE MEMBER PRESERVES, in two parts. First, an
EXCLUSION inside the read half: a broader directory-wide read role such as
`Directory.Read.All` is NOT within this surface's admission act, because it
also reads the ALREADY-ADMITTED `device` surface (Entra registered devices are
directory objects) and would therefore collapse two separately-consented,
separately-scoped and separately-revocable surfaces onto one act. The neutral
layer NEVER INFERS A PROVIDER FACT, so no validator can derive that boundary
from the role tokens; the member `description` is the only place it can be
stated, and it is stated there. Second, the mutation half stays out: the
extension-route prose is resliced so `directory` is the READ surface for the
tenant directory and service estate, while endpoint MUTATION (Intune write) and
Entra-directory MUTATION (user, group and application administration) remain
SEPARATE future surfaces, each arriving with its own governing change. The
`device` member's own closing sentence is amended in the same cut so the
contract file cannot contradict itself — it announced Entra-directory READ as a
future surface, and now records it as admitted here.

Also corrected in the same edit, and PROSE ONLY: the vocabulary's grounding
moves from PROMOTED to RATIFIED. The text grounded both the member set and the
extension route on capability PROMOTION, and that has been false since
`contract-v1.35` — neither `managed-node-inventory` nor
`managed-service-inventory` is promoted; both are RATIFIED and still active in
OpsxFactory `openspec/changes/`, so on the old literal wording `device` should
never have been admitted either. The vocabulary now names the surfaces "whose
governing change is RATIFIED", and a surface "enters with the ratified change
that governs it". The promoted requirement's own normative sentence — "The
closed surface vocabulary SHALL be extended only by the change that governs a
new surface" — is already change-based, is satisfied here, and is UNTOUCHED.
`scripts/validate-client-identity-roster.py`'s human-facing
`EXTENSION_ROUTE["admission_surface"]` refusal string is resynced to the
revised schema text; the VOCABULARY itself needs no validator edit, because
that validator DERIVES the closed set from the schema
(`_consts(defs.get("admission_surface"))`) rather than restating it.

GOVERNING EVIDENCE. OpsxFactory `add-managed-service-inventory` (read-only
tenant service-surface DISCOVER, ratified 2026-08-21), §1–§6 realized and
MERGED at OpsxFactory `main` `824f8ef`. The realized
`microsoft_service_discovery_reader` credential requirement there
(`credentials/requirements.yaml`) carries `admission_surface: directory` with
`minimum_scopes` exactly those three roles under `exact_effective_scopes: true`
and `reject_write_or_destructive_scopes: true` — which is why the member
HARD-ENUMERATES the act instead of naming a role family. Per that change's
ratified F1 ordering this extension is grounded on the DETERMINISTIC §1–§6
contract, never on a live snapshot, and it authorizes no provider act.

The packaged positive example (`opsx-farheap-service-discovery-reader`, a
`planned` entry in
`examples/client-identity-roster/client-identity-roster-farheap-opsx.example.yaml`)
demonstrates the shape: `admission_surface: directory`,
`authority_class_intended`/`_achieved: observe`, the three read roles each
`achieves: observe` and `reaches: [directory]`, `exceeds_governed_unit: false`,
NO `declared_excess`, no `spanned_surfaces`,
`per_unit_principal_available: {directory: false}`, and a single
`logic_enforced` act that is UNVERIFIED by derivation (no `evidence_ref`, no
`verified_at`, `provider_object_ref` omitted) because the discovery reader is a
DOWNSTREAM OpsxFactory consumer not yet admitted. The
`admission-surface-out-of-vocabulary` negative (which uses `sharepoint`) still
fires — `directory` is now in-vocabulary, `sharepoint` is not, and `sharepoint`
being a service DISCOVER may DETECT is not admission.

DOWNSTREAM, so the ordering is not overclaimed: landing this cut is NECESSARY
but NOT SUFFICIENT for the OpsxFactory live sweep. OpsxFactory pins
`contract-v1.35` and keeps its own local `ROSTER_ADMITTED_SURFACE_VOCAB`
(`scripts/validate-domain-factory.py`), so a `directory` roster entry is
refused by that repository's own validator until it RE-PINS to this bundle and
widens that fence — the precedent being OpsxFactory PR #45 (`77f4b82`) for
`device`.

## contract-v1.38 — 2026-08-21 (additive; the doxBench model-catalog routing rule)

Realizes tasks.md §11.7 of `add-doxbench-editing-phase-b` — the ratified
scenario *"The menu offers a routing rule"*. One CONTRACT changes:
`schemas/xfactory-workbench-model-catalog.schema.yaml`. That schema is
content-addressed by its per-file `sha256` in [`manifest.yaml`](manifest.yaml);
that row's digest is RECOMPUTED in this cut, and its `consumption_rule` states
what a consumer must now read and what it may still ignore.

VERSION ALLOCATION, stated because it moved mid-flight. This slice was briefed
as `contract-v1.37`. While it was in flight, `6cbb4495` (PR #235,
identity-brokering + trust-anchor) landed on main and ALLOCATED v1.37 — a
CHANGELOG heading plus `contract_bundle_version: contract-v1.37` — although its
own squash message still says "at contract-v1.36". Under
[`docs/contract-versioning-policy.md`](../docs/contract-versioning-policy.md)
the version is allocated AT REALIZATION against what is available, and CHANGELOG
presence is the availability test, so this release is `contract-v1.38`.

A DEFECT ON THE PRECEDING RELEASE SURFACE, found here, repaired by its own lane,
AND BACK. At `6cbb4495`, `scripts/validate-contract-release.py verify-commit`
reported `HGR-RELEASE-INVENTORY-MISSING` and exited 1: that cut bumped the bundle
to v1.37 without shipping `releases/contract-v1.37.digests.yaml`, the same class
of miss `contract-v1.36`'s first tag hit, one step earlier. It was recorded here
rather than fixed, because a release surface belongs to the release that cut it —
and `c1ffa0fd` (PR #238, "Complete the contract-v1.37 cut: release digest
inventory") shipped that inventory, at which commit `verify-commit` PASSED.

IT IS RED AGAIN AT `8924838d`, and by the same habit: `e11a057b` (PR #242,
install-repo naming) edited `contracts/CHANGELOG.md` — a v1.37 INVENTORY MEMBER —
without rebuilding v1.37's inventory, so `verify-commit --commit origin/main`
now exits 1 with `HGR-RELEASE-DIGEST-MISMATCH` on that file. Bisected: green at
`c1ffa0fd`, red from `e11a057b` onward. That is the v1.37 lane's to repair, and
it is exactly the habit this note names — recheck bundle availability against
the CHANGELOG at the moment you allocate, and do not assume the preceding
release surface verifies, including when it verified an hour ago.

THIS CUT IS UNAFFECTED THROUGHOUT, in every one of those states:
`resolve_committed_inventory` reads `contract_bundle_version` AT THE COMMIT, so
it resolves v1.38 and checks against the v1.38 inventory that ships inside it —
and this branch's own `verify-commit` passes.

**Change class: ADDITIVE (minor)** under
[`docs/contract-versioning-policy.md`](../docs/contract-versioning-policy.md).
Three OPTIONAL properties are added to `$defs/model_entry`, together with one
`dependentRequired` block and two `allOf` conditionals that constrain ONLY those
three. Nothing previously valid becomes invalid, no required field is added to
any existing shape, no shape is removed, and no existing catalog is
reinterpreted: BOTH conditionals require `routing_rule` to be PRESENT, so an
entry that declares no routing rule matches neither and is judged exactly as it
was before, and `dependentRequired` cannot fire on keys that are absent. The
schema's `contract_schema_version` stays `1`, and the manifest row's
`schema_version` stays `1` with it. Verified case by case against the released
bytes, including the pre-release entry shape and each malformed declaration.

`$defs/model_entry` gains, all optional and all three travelling together:

* `routing_rule` (boolean) — present-and-true means this entry is a ROUTING RULE
  this capability owns, an `auto` entry that maps a turn to a model by role,
  rather than a directly answering provider model. Absent means what absence has
  always meant, and a plain entry acquires no new obligation of any kind.
* `routes_to` — every model the rule MAY route to, as a non-empty, unique array
  of `model_id` REFERENCES into the same catalog (same pattern and length bounds
  as `model_id`, up to 64 members).
* `resolved_model_id` — the model the rule CURRENTLY resolves to: the one that
  ANSWERS, recorded as the turn's `model_id` beside the requested id in the
  `workbench-chat-turn-v2-success` record's `selected_model`.

They carry NO provider surface, and that is what keeps PUBLIC-ONLY BY
CONSTRUCTION intact: both reference fields hold opaque catalog handles drawn
from this catalog's own `model_id` values, so a routing declaration can name
nothing a plain entry could not already name. §11.6's ruling that the harness
provider id lives on `LaunchConfig.provider_id` and NOT on the catalog entry is
untouched — the entry is still closed, `provider_id` on it is still refused
structurally, and a companion test asserts that against these exact bytes.

WHERE THE CREDENTIAL COMES FROM, named here because this is the release at which
an operator can declare an API-backed routing entry and therefore has to know
(§11.7's P3-23 sentence). An API-backed entry's credential is provisioned into
the `doxbench-bridge` harness PROFILE by the ratified broker lane
(`add-model-provider-broker`). The adapter neither holds nor fetches a raw
secret: its child environment is an ALLOWLIST no credential-shaped variable can
pass, which is why an empty profile makes the harness refuse ("no models
available") rather than reach for an ambient key. A self-hosted, keyless
provider needs no credential at all. Nothing in this release moves that
boundary; it states it.

SEVEN RULES THE SHAPE CANNOT EXPRESS are delegated to
`scripts/validate-ideation-dashboard-contracts.py`, the family's declared owner,
and enforced at catalog construction in
`scripts/ideation_dashboard/doxbench_model.py` (an in-process catalog never
becomes a validated file, and a file is never constructed through that type, so
neither place substitutes for the other). That the two gates AGREE is asserted by
a test over the packaged corpus, not claimed here: an earlier draft of this entry
said "enforced identically" while rules 6 and 7 below existed only on the type,
and the release's own adversarial review walked a catalog past the file gate to
prove it:

1. NO DANGLING TARGET — every `routes_to` id must name an entry in the same
   catalog. A rule that routes somewhere the catalog does not offer has a badge
   nobody can check.
2. NO CHAINED RULE — a target must not itself be a routing rule, because
   `resolved_model_id` is recorded as the model that ANSWERED and must therefore
   name something that answers rather than another indirection.
3. AN AVAILABLE RULE RESOLVES TO AN AVAILABLE MODEL. The turn gate checks
   availability on the SELECTED entry, and the adapter then sets the harness to
   the RESOLVED id; without this rule an available `auto` could dispatch to a
   model the catalog itself calls unavailable. An unavailable rule is exempt —
   nothing can select it.
4. THE BADGE COVERING — the ratified THEN, as SEGMENT MEMBERSHIP over the
   declared `" / "` separator: each target's `data_handling` must be one segment
   of the rule's own, compared with whitespace collapsed, case folded and
   trailing `.;,` dropped, and with interior characters never rewritten. Extra
   segments are permitted; a routed badge that itself holds the separator is
   refused as ill-formed, because it could never be one segment. See the
   judgement call below for why this replaced substring containment.
5. A RULE PROMISES NO MORE HEADROOM THAN THE MODEL THAT ANSWERS — the
   effective turn limit is computed from the selected entry, which for a routed
   turn is the rule, so an AVAILABLE rule's declared limits must not exceed
   those of `resolved_model_id`'s entry. The bound is the RESOLVED model's
   alone, deliberately NOT the minimum across `routes_to`; unavailable rules are
   exempt, as they are from rule 3. See the judgement call below — this shape
   was ruled after the release's adversarial review.
6. `resolved_model_id` MUST BE A MEMBER OF `routes_to` — otherwise the model
   that actually answers is the one model no covering check ever looked at,
   since they all iterate `routes_to`.
7. A RULE MUST NOT NAME ITSELF in `routes_to`.

Every rule has a packaged negative that fails for exactly its own reason — ten
of them — beside one positive (`workbench-model-catalog-routing-rule`) and a
structural negative for a plain entry carrying a routing field. Four of the ten
came from this release's adversarial review, packaged verbatim from the
reviewer's own instances.

JUDGEMENT CALL — THE BADGE COVERING IS SEGMENT MEMBERSHIP, AND THE MENU IS WHY.
The requirement says a routing entry must "carry the handling badge of every
model it may route to", *"because an entry that hid a routing decision behind a
model-shaped id would report a handling posture it does not control"*. The
entry's own `data_handling` is the ONE badge string the selector shows for it, so
the covering rule has to be about that string.

An earlier draft of this release enforced it as raw substring containment. THAT
WAS WRONG, and this release's adversarial review broke it twice on these very
bytes: a rule badged *"Routes to a non-tenant endpoint."* was accepted as
carrying a target badged *"on-tenant"* — `"on-tenant" in "non-tenant"` is True,
so the menu would have shown the INVERSE of the posture the rule routes to — and
a rule ending *"...retain nothing."* was accepted as carrying a target badged
*"retain"*. The same review found the predicate simultaneously OVER-strict in the
harmless direction, refusing a badge that differed only by a trailing full stop,
a capital, or a line wrap.

The rule is therefore SEGMENT MEMBERSHIP, and the separator is DECLARED here and
in the schema: `" / "` (space, slash, space). A routing rule's `data_handling` is
a list of segments joined by it, and each routed model's own badge must be one of
them. Comparison collapses whitespace, folds case, and ignores trailing `.;,`;
it NEVER rewrites interior characters, which is the load-bearing part, because
that is exactly where `on-tenant` and `non-tenant` differ. Extra segments are
permitted, so a rule may carry its own lead-in beside the badges it must carry.
The separator is `" / "` because a badge is free prose and any separator can
collide with one — `;`, `.` and `,` all occur in the packaged badges and `/` does
not — and the residual collision is refused rather than hoped away: a routed
entry whose badge itself contains the separator could never be one segment, so
that catalog is ill-formed.

CONSUMER NOTE: a consumer that RENDERS a routing entry's badge may split it on
`" / "` to show the routed postures separately, and one that does not may show
the string whole; both are correct, and the string is authored to read as prose
either way.

The alternative considered and rejected was per-target badge OBJECTS on the wire
(`{model_id, data_handling}` pairs) plus a view that composes them — rejected
because it duplicates authored text that then drifts from the target's own entry.
The consequence, stated rather than hidden: `data_handling`'s pre-existing
500-byte ceiling is UNCHANGED and therefore bounds how many segments one rule can
carry. A rule whose list does not fit must be split, or its members' badges
written more tightly. Widening that ceiling was rejected as a consumer-visible
change to an existing field, which this release's additive posture does not
permit.

JUDGEMENT CALL — RULE 5' BOUNDS AGAINST THE RESOLVED MODEL, RULED BY BRETT.
This release first shipped rule 5 as a MINIMUM over every member of
`routes_to`. Its adversarial review upheld it only WITH RESERVATION: it
permanently caps an `auto` entry's declared limits at its narrowest destination
in order to compensate for the runtime computing budgets from the SELECTED
entry. Brett ruled on 2026-08-21 — "Swap to rule 5'" — and the bound is now the
RESOLVED model's alone. Three reasons, recorded because the shape of a
conformance rule is a design commitment:

* under this release's STATIC resolution, the promise that matters is that the
  menu's declared limits are honoured by the model that ACTUALLY ANSWERS, which
  is exactly what the resolved-bound form checks;
* the un-resolved destinations are not load-bearing — no turn reaches them while
  the rule resolves elsewhere — so capping against them constrains a promise
  nobody can call in;
* min-capping would BAKE IN semantics contradicting the sanctioned future
  direction: a per-turn, FIT-AWARE router that picks a destination by the
  assembled packet's size and by other capability dimensions, staged as
  `ideation/staging/doxchat-auto-fit-routing/`. Under that design a rule's
  declared ceiling is the WIDEST thing it can serve, not the narrowest, and a
  min-cap would have had to be undone to reach it.

A packaged POSITIVE carries the difference rather than leaving it to prose:
`workbench-model-catalog-routing-rule-wider-than-a-non-resolved-member` declares
800,000 bytes while a routable — but not resolved — member accepts 2,048, and is
VALID. The first form of the rule would have refused it. Its mirror-image
negative is `routing-rule-wider-than-its-resolution`.

JUDGEMENT CALL — DISCLOSED ONLY WHEN DECLARED. This repository's projection
(`ModelCatalogEntry.as_public_dict`) emits the three keys only for an entry that
IS a routing rule, so a plain entry's public dict is byte-identical across the
release boundary. Always emitting them with plain-model defaults was rejected: it
would change the bytes of every catalog response that exists, hand every
consumer a `resolved_model_id: null` it never asked for, and put `routes_to: []`
on entries this schema forbids to carry it. The WIRE, being additive, tolerates
BOTH producers — an explicit `routing_rule: false` with no siblings is valid,
it is simply not what this projection emits — so a consumer must not treat
omission and explicit-false as different facts.

WHERE THE RESOLVED MODEL IS RECORDED, and a v1 LIMITATION that goes with it.
The scenario's second THEN is that "the resolved model MUST be recorded on the
turn, so a transcript names the model that actually answered", and there are TWO
readers of that fact. The `workbench-chat-turn-v2-success` record carries it in
`model_id`, beside `selected_model.requested_model_id` and
`selected_model.routing_rule`. The turn's THREAD SIDECAR — the durable transcript
on disk — carries it in the turn header. This release's adversarial review found
the second one naming the RULE rather than the answering model (the derivation
sat after the sidecar was written), which is now fixed: one derivation, above
both readers.

THE DEPRECATED v1 SUCCESS ENVELOPE CANNOT STATE BOTH FACTS, and is not changed to.
`workbench-chat-turn-success` has one `model_id` field and no `selected_model`,
so on a routed turn it carries the REQUESTED id — what every v1 consumer already
reads and revalidates. Widening a deprecated closed shape whose whole promise is
byte-identical stability is precisely what `contract-v1.34`'s deprecation
forbids; the migration path is the v2 envelope, which exists and is where a
routed turn should be recorded. The SIDECAR on the v1 lane does name the
answering model, because it is not part of the v1 wire.

NO VIEW CHANGE, and the reason is the covering rule. `doxbench-chat.js` already
renders each option as `label — data_handling` and `sendDisclosure` already
names the selected entry's `data_handling`, so for a conformant rule both
already show every routed model's badge. A node probe mounts the SHIPPED rail
over the packaged routing catalog and asserts exactly that, so the claim is
evidence rather than argument; if a future release moved the badges off
`data_handling`, that probe fails and a view change is then owed.
`staging-workbench-model.js` reads only an approved-model COUNT and is untouched.

RECONCILIATION with `add-doxchat-model-intake` (ratified 2026-08-21, UNBUILT).
That change's proposal repeatedly describes the catalog entry as "the closed
seven-field shape" and promises its own proposed-versus-approved distinction
"does NOT widen" it. Both remain true of THAT change: its packet is another
lane's and is not edited here, its descriptions were accurate when ratified, and
its no-widening promise is about its own delta. What changes is the referent —
the closed entry is now the v1.38 shape: seven required base fields plus the
three optional routing-declaration fields. Its task 3.5 ("the closed seven-field
public catalog entry does NOT widen") should be read against this shape when
that lane builds; a proposed-versus-approved distinction is still not a widening
of it.

OWED CROSS-REPO FOLLOW-UP (recorded, not performed). This schema's description
names `codexFactory specs/010-doxbench-editor-chat/contracts/model-catalog.md`
as its consumer contract, and that document's Reconciliation section claims an
exact match with the seven-field entry shape. That claim is STALE against this
release — though it remains CORRECT while codexFactory pins `contract-v1.27`,
which is the pin it declares, so nothing there is wrong today. It becomes wrong
the moment that repository re-pins. Updating it is codexFactory's own governed act
under the domain upgrade runbook; no file in that repository is touched here, and
this entry is the notice.

RELEASE OBLIGATION STILL OPEN AT THIS ENTRY: per the versioning policy,
CHANGELOG presence is the availability test and the annotated tag is cut at the
realization squash against the commit that actually lands. The release DIGEST
INVENTORY (`releases/contract-v1.38.digests.yaml`) ships INSIDE this cut, as
`contract-v1.34`, `contract-v1.35` and `contract-v1.36` all did. The consuming
runtime repin ships with it and carries the `unpublished:contract-v1.38`
sentinel for its ref, on `contract-v1.34`'s own precedent: until the release
commit exists there is nothing honest to name, and the sentinel is spelled as a
value no `stack.yaml` can declare, so a consumer comparing against it refuses
rather than matching by accident. A follow-up commit resolves it.

## contract-v1.37 — 2026-08-21 (additive; two new neutral families — identity brokering and trust anchors)

Realizes the two ratified sibling changes of 2026-08-21 —
`add-identity-brokering` through Speckit feature
`008-identity-brokering-contracts`, and `add-trust-anchor` through
`009-trust-anchor-contracts` — as TWO new neutral contract families. Fifteen
NEW contract files land; **no existing released file's bytes change**, so
every existing pin resolves byte-identically until it chooses to re-pin.

**Change class: ADDITIVE (minor)** under
[`docs/contract-versioning-policy.md`](../docs/contract-versioning-policy.md)
lines 130-132 ("new optional fields, new contracts, new validator warnings").
The test is that a domain repo on the same major version remains conformant
WITHOUT CHANGES, and it holds trivially here: both families are entirely new,
no existing shape gains a required field, no shape is removed, and no existing
vocabulary is reinterpreted. Every new file declares
`contract_schema_version: 1`, and NO `contract_schema_version` anywhere in the
bundle is bumped. Both families are OPT-IN: a domain that records no persona,
adoption, anchor or certificate publishes nothing and stays conformant, and
each family's canonical validator exits 0 with a notice over a repository that
holds none of its artifacts.

**Nothing was pending.** The standing Unreleased items were cut at
`contract-v1.32` (the `hermes_subject_overlay` kind and the openxWallet RSA
signature-algorithm widening), and no Unreleased block accumulated between
that cut and this one, so this entry folds no deferred item.

### `contracts/identity-brokering/` — the neutral identity-brokering family (`add-identity-brokering`)

The neutral contract for what any identity broker must assert about a human,
what a governed record may store about an actor, and what a broker must never
become. Keycloak is the realization being adopted and it appears in no schema,
no enumeration and no requirement. SIX schemas, each with a per-file `sha256`
in [`manifest.yaml`](manifest.yaml):

- `persona-assertion.schema.yaml` — what a conformant broker asserts about an
  authenticated human: issuing broker INSTANCE, stable opaque subject, display
  name, federated upstreams, organization memberships, and nothing else. The
  property set is a CLOSED ALLOW-LIST AT EVERY DEPTH, so a role, group, grant,
  project, stack, layer or entitlement has nowhere to go — the never-mirror
  rule enforced by the shape rather than by review. The membership's
  `organization_id` uses a narrower pattern than the family's general
  identifier (no `:` and no `/`), which was the rule's last doorway.
- `broker-organization.schema.yaml` — a company boundary as the broker holds
  it. `company_role` is `tenant` or `served`; the two are the SAME KIND of
  record. A company boundary is NOT a Hermes layer, so the family carries an
  explicit bridge (`tenant` -> `tenant`, `served` -> `subject`) whose targets
  the canonical validator READS from
  [`policies/layer-vocabulary.yaml`](policies/layer-vocabulary.yaml) at run
  time, reserved terms included. `governed_record_refs` is bounded at ONE
  closed item: the pointer-not-projection line.
- `actor-subject-reference.schema.yaml` — the STRUCTURED reference a governed
  record embeds when it names a human actor (issuer, opaque subject, display
  name as it stood, provenance discriminator). Three provenance classes whose
  wrong combinations are UNREPRESENTABLE, including a `pre_broker_username`
  that admits no issuer or subject and carries a required constant
  `presented_as_persona: false`.
- `identity-link-record.schema.yaml` — a federated identity joining an
  existing persona. EXACTLY TWO MODES, each requiring its actor by shape;
  attribute-match auto-linking cannot be written at all; every pre-merge
  subject is carried with the survivor it remains resolvable to.
- `broker-client-declaration.schema.yaml` — a broker service client declared
  as TRANSPORT, with three REQUIRED CONSTANTS (`is_transport: true`,
  `actor_of_governed_acts: false`,
  `organization_membership_as_authority: false`) and no property in which an
  actor role or authority could be written. Non-human authority stays on
  `credential-contracts` grants and `openxwallet` holders.
- `surface-adoption.schema.yaml` — a surface's declared authorization posture,
  the instance it authenticates against, the shared secret the adoption
  retires, and the isolation its population requires. A write action cannot
  hide under the weak posture (schema conditional both ways), `resolves_in`
  has one legal value `governed_layer`, and isolation escalates by broker
  INSTANCE while the contract stays SILENT on instance count.

`contracts/identity-brokering/README.md` (`Status: ratified`) and the packaged
corpus at `contracts/identity-brokering/examples/` — 14 positive examples and
41 intended-invalid negatives, coverage closed in both directions at 9/9
requirements — are content-addressed by commit, no per-file digest, per the
openxWallet and client-identity-roster precedent. So is the canonical
validator `scripts/validate-identity-brokering.py`: fourteen lettered rules
(a)-(n) the shapes cannot express, with the closed allow-list DERIVED FROM THE
SCHEMA (local `$ref`s resolved, branches unioned) rather than written as a
second list, and the admissible linking bases, the authorization-resolution
target and the layer vocabulary all READ AT RUN TIME from the contract or the
policy so a check cannot drift from the thing it enforces.

### `contracts/trust-anchor/` — the neutral trust-anchor family (`add-trust-anchor`)

The neutral contract for what a governed system may assume about a certificate
it trusts — product-agnostic, because the family runs two certificate
authorities from two vendors for two populations (live Intune Cloud PKI;
OpenXPKI planned). SEVEN schemas plus the chain-custody registry PAIR, each
with a per-file `sha256` in [`manifest.yaml`](manifest.yaml):

- `trust-anchor.schema.yaml` — the governed record a system TRUSTS; a
  certificate is trusted only derivatively, through an anchor the evaluating
  system already holds. Chain position is coherent or the record is refused,
  an anchor's window BOUNDS its subordinates, and authority key material is a
  `credential-contracts` record with its vault binding or a declared
  obligation that neither can be produced.
- `certificate-record.schema.yaml` — a certificate as a governed record.
  `trust_evaluation.basis` is the constant `held_anchor_record` and the
  standing check's basis is the constant `checked_at_use`, so trust cannot be
  recorded on a certificate's own strength nor on issuance-time validity;
  `evidences` is DERIVED from declared custody and recomputed.
- `issuance-evidence.schema.yaml` — what an issuance record must ESTABLISH,
  never the mechanism. Two `establishment_level` members and nothing weaker is
  representable; the floor
  (`per_policy_attestation_with_authority_log`) requires BOTH halves; asserted
  provenance at `not_established` is forbidden by shape and requires a
  resolvable `declared_shortfall_ref`.
- `dependent-binding.schema.yaml` — one authority binding against a
  certificate's key material, recorded so a renewal's rebind set is computable
  BEFORE the renewal. The key GENERATION is the join, compared against the
  CERTIFICATE with no renewal record in the way.
- `renewal-record.schema.yaml` — a renewal and the rebind obligation it
  creates. "Successful with an unevidenced dependent" is unrepresentable as a
  SCHEMA constraint; `failure.attribution` is the constant
  `issuing_workflow`; no rule anywhere keys on `renewal_mode`.
- `revocation-propagation.schema.yaml` — revocation reaching the authority the
  certificate supported, within a declared window whose arithmetic is
  recomputed. `mechanism.realized_through` is the constant
  `openxwallet_revocation_through_derivation` — one revocation vocabulary, not
  two — and an unevidenced closed window must be recorded
  `incomplete_open_exposure` with the escalation.
- `conformance-declaration.schema.yaml` — obligation by obligation, what a
  realization satisfies, partially satisfies, and cannot; CLOSED over the
  capability's eight obligations with coverage checked in both directions and
  a per-entry `declared_at`, so a gap declared afterwards does not validate
  the claims made while the realization was silent.
- `chain-custody-registry.schema.yaml` + `trust-anchor-chain-custody.registry.yaml`
  — the CLOSED chain-custody enumeration and the ordered assurance ladder it
  caps, as a schema plus its closed instance (the `openxwallet-custody`
  registry pattern). `evidences` is DERIVED from two declared booleans and
  never independently asserted, and each member declares the `openxwallet`
  custody member it corresponds to, which the canonical validator RESOLVES
  against [`openxwallet/openxwallet-custody.registry.yaml`](openxwallet/openxwallet-custody.registry.yaml)
  at run time — so "composes with rather than restates" is structural rather
  than a promise, and the two registries cannot drift into two custody
  models. Operator escrow is a deliberate NON-MEMBER, modelled as a
  relationship on the credential record rather than a custody tier (OQ2, ruled
  as recommended).

`contracts/trust-anchor/README.md` (`Status: ratified`) and the packaged
corpus at `contracts/trust-anchor/examples/` — 34 positive examples and 65
intended-invalid negatives, coverage closed in both directions at 8/8
requirements — are content-addressed by commit, no per-file digest. So are the
canonical validator `scripts/validate-trust-anchor.py` (34 lettered rules, a
self-test layer and a repo-scan layer, exit 0/1/2) and its pytest wiring
`tests/trust-anchor/` (validator exit code and reported corpus counts; every
negative fixture adjudicated independently; the declaration-perimeter rules
whose cases need two records that disagree).

### Realization provenance and the review hardening in this cut

Both families were ratified by Brett Heap on 2026-08-21 — identity brokering
with its recommendations adopted as written and the OQ-5 co-residence gate
discharged, trust anchors with OQ1 and OQ2 ruled as recommended — and both
were realized the same day.

**Each family was then hardened by an adversarial review panel independent of
its author, and the hardening is IN the bytes this cut registers.** Identity
brokering: 28 bypass probes, 14 verified findings, 14 new negative fixtures
(negative corpus 27 -> 41), the validator's rule set (a)-(m) -> (a)-(n), and
22 distinct finding codes red-proven; three findings tightened the CONTRACT
rather than a check (a merge is not approved by one of its own parties;
`prior_shared_credential` required; `restriction_ref` required for both
answers) and are disclosed in
`specs/008-identity-brokering-contracts/research.md`. Trust anchors: 52
probes, 14 findings, all 14 closed, two new positives and twenty-two new
negatives (32/43 -> 34/65), 27 -> 34 validator rules, and 50 non-`schema`
finding codes red-proven. Zero ratified-corpus regressions on either side. The
per-finding dispositions live in each feature's `traceability.yaml` under
`review_hardening`.

Both changes also ADD one requirement each to `repo-boundary-governance` — the
`Keycloak-Install` (amended 2026-08-21: Opensoft-level naming ruling — see the
changes' Ratification sections) and `OpenXPKI-Install` repository
boundaries — as TWO DISTINCT ADDED requirements rather than one shared
MODIFIED enumeration delta, so the sibling changes cannot collide on one
requirement at archive time. Those are governance deltas, not contract files,
and nothing in this cut depends on them.

Per [`docs/contract-versioning-policy.md`](../docs/contract-versioning-policy.md)
"Bundle Realization Order", the minor number is allocated LATE: this entry,
the manifest bump to `contract-v1.37` and the fifteen new contract files land
atomically in one candidate commit, and the annotated tag `contract-v1.37` is
applied POST-MERGE to the exact realized commit on published `origin/main` —
never reserved ahead of merge order, and never moved once published.

## contract-v1.36 — 2026-08-21 (additive; the `share-session` gate action)

Realizes tasks.md §12 of `add-doxbench-editing-phase-b` — the ratified
requirement *"Share-session hands a live session to a colleague"*. One CONTRACT
changes: `schemas/gate-action-record.schema.yaml`. That schema is
content-addressed by its per-file `sha256` in [`manifest.yaml`](manifest.yaml);
that row's digest is RECOMPUTED in this cut, and its `consumption_rule` names
the new action.

**Change class: ADDITIVE (minor)** under
[`docs/contract-versioning-policy.md`](../docs/contract-versioning-policy.md).
An enum member is added to `action`, and one `allOf` conditional is added that
constrains ONLY that new member. Nothing previously valid becomes invalid, no
required field is added to any existing shape, no shape is removed, and no
existing record is reinterpreted. This is the schema's own stated additive
route — "no record has ever carried that action, so nothing pre-existing is
narrowed" — the same posture under which `edit-document`, `open-pr`,
`abandon-session` and the three wheel commissions landed. The schema's
`contract_schema_version` stays `1`, and the manifest row's `schema_version`
stays `1` with it.

`action` gains `share-session`: the doxBench workbench verb that commits a
session's DIRTY thread sidecars and PUSHES the session branch, so a colleague
can resume the same session from the fetched branch. It is deliberately
STRICTLY LESS than `open-pr` — it reuses that verb's existing remote-write path
(`session_pr.PullRequestPort.push`), opens no pull request, requests no review,
and holds no approval or merge authority. It exists because threads are LOCAL
until a human says otherwise: a working note that leaves the machine without an
explicit act is a disclosure nobody chose, so no Save, turn, compaction or
scheduled task may push one.

The new conditional requires `target.ref` and NO artifact kind. That is a
decision, not an omission, and it is the one genuinely novel shape in this cut:
`share-session` has TWO RECORD RESIDENCIES, because FR-006's one-commit-per-
gate-action guard explicitly refuses an empty declared document set.

* With dirty sidecars to publish, the action commits them WITH its record as
  exactly one commit on the session branch, so the record is BRANCH-RESIDENT
  and carries a `commit` artifact — and rides to the colleague, who can then
  see why those threads landed.
* With nothing dirty but commits the remote has not seen — the ordinary state
  after a run of Saves, precisely because nothing pushes implicitly — the
  action commits nothing, so its record is MAIN-RESIDENT exactly as `open-pr`'s
  is.

Requiring `commit` would therefore invalidate the second and commoner case, and
requiring `pull-request` would assert a pull request this verb never opens.

A FAMILY-WIDE NOTE, recorded here because it is a property of the whole
per-action conditional family and not of this cut alone: a conditional of the
form `if action then artifacts contains kind` requires a companion artifact; it
does NOT forbid the others. So this schema does not prevent a `share-session`
record from carrying a `pull-request` artifact — it simply never requires one.
`abandon-session` has the identical hole and has had it since
`add-workbench-branch-sessions`. What forbids it is the RUNTIME: the share verb
reaches exactly one port member and a test asserts that against the port's own
call log, so no path exists that could build such a record. Closing the hole
schema-side would mean adding a `not`/`contains` clause to several pre-existing
actions at once, which narrows shapes that already have valid records in the
corpus — the one thing this schema's additive posture forbids. It is therefore
recorded as a known, runtime-enforced boundary rather than fixed here.

RELEASE OBLIGATION STILL OPEN AT THIS ENTRY: per the versioning policy,
CHANGELOG presence is the availability test and the annotated tag is cut at the
realization squash. Task 12.7 carries the tag + submodule-pin half. The release
DIGEST INVENTORY (`releases/contract-v1.36.digests.yaml`) ships INSIDE this cut,
as `contract-v1.34` and `contract-v1.35` both did — it is part of the cut, not
part of the tagging.

## contract-v1.35 — 2026-08-19 (additive; the `device` roster admission surface)

Realizes `add-roster-device-admission-surface`, the ratified extension of the
client-identity-roster closed `admission_surface` vocabulary. One CONTRACT
changes — `schemas/xfactory-client-identity-roster.schema.yaml` — and the
change adds a packaged `device` example to
`examples/client-identity-roster/`. The roster schema is content-addressed by
its per-file `sha256` in [`manifest.yaml`](manifest.yaml); that row's digest is
RECOMPUTED in this cut. (The roster schema is not a release-inventory member,
so this cut's digest inventory changes only where `manifest.yaml` and this
changelog change.)

**Change class: ADDITIVE (minor)** under
[`docs/contract-versioning-policy.md`](../docs/contract-versioning-policy.md).
A `oneOf` const member is added to `$defs.admission_surface`; nothing
previously valid becomes invalid, no required field is added to any existing
shape, no shape is removed, and no existing roster is reinterpreted, so a
domain on the same major version stays conformant WITHOUT CHANGES. The
schema's own `contract_schema_version` stays `1`, and the roster row's
`schema_version` stays `1` with it — vocabulary-member admission is governed by
the schema's EXTENSION ROUTE text, not by the object-shape/key-space growth
that would take a `contract_schema_version` bump.

`$defs.admission_surface` gains a third member, `device`: the Microsoft tenant
DEVICE ESTATE — Entra registered devices, Intune managed devices and Windows
365 Cloud PCs — admitted as ONE tenant-wide READ surface. Its admission act is
admin consent for the read-only application roles `Device.Read.All`,
`DeviceManagementManagedDevices.Read.All` and `CloudPC.Read.All` on ONE Entra
app registration; its scoping mechanism is tenant-wide read with exact
effective scopes and no narrower provider selector (`enforcement_mode:
logic_enforced`); it is read-only. Because the governed unit IS the tenant
device estate, tenant-wide read is the GOVERNED scope, not excess. The
extension-route prose is resliced so `device` is the READ surface for those
three provider areas, while endpoint MUTATION (Intune write) and Entra
DIRECTORY read remain SEPARATE future surfaces, each arriving with its own
governing change. Evidence: the OpsxFactory node-inventory reader (a downstream
consumer authored under OpsxFactory governance).

The packaged positive example (`opsx-farheap-node-inventory-reader`, a
`planned` entry in
`examples/client-identity-roster/client-identity-roster-farheap-opsx.example.yaml`)
demonstrates the shape: `admission_surface: device`,
`authority_class_intended`/`_achieved: observe`, the three read roles each
`achieves: observe`, `exceeds_governed_unit: false`, NO `declared_excess`,
`per_unit_principal_available: {device: false}`, and a single
`logic_enforced` act. The `admission-surface-out-of-vocabulary` negative
(which uses `sharepoint`) still fires — `device` is now in-vocabulary,
`sharepoint` is not.

## contract-v1.34 — 2026-08-18 (additive + deprecating; the doxBench chat-turn widening)

Realizes `add-doxbench-editing-phase-b` §13, the contract release its ratified
"chat-turn contract release carries the bound buffer and the model" requirement
names. One CONTRACT changes —
`schemas/xfactory-workbench-chat-turn.schema.yaml` — and one normative document
moves with it: [`docs/contract-versioning-policy.md`](../docs/contract-versioning-policy.md)
records this cut's deprecation in its "Deprecations Currently In Force" list.
Both are release-surface members and both are digested in this cut's inventory.

**Change class: ADDITIVE (minor) plus a DEPRECATION (minor)**, both under
[`docs/contract-versioning-policy.md`](../docs/contract-versioning-policy.md)
lines 128-135. Nothing here is breaking: no required field is added to an
existing shape, no shape is removed, and no vocabulary is reinterpreted, so a
consumer on the same major version remains conformant WITHOUT CHANGES.

`xfactory-workbench-chat-turn.schema.yaml` gains a CO-RESIDENT SECOND ENVELOPE
FAMILY beside its existing one — `workbench-chat-turn-v2`,
`workbench-chat-turn-v2-success`, `workbench-chat-turn-v2-failure` — added to
the file's top-level `oneOf` and discriminated by `kind`, exactly as the three
v1 envelopes already discriminate each other. The widened family carries what
the v1 shape had no room for: the outline plus EVERY loaded document buffer
(`buffers` widens from `minItems: 2, maxItems: 2` to `minItems: 2, maxItems: 25`
— the surface's declared 24-document loaded-set bound plus the reserved
outline); the DECLARED `bound_buffer` key on both the request and the durable
record; `observed_hashes` keyed by BUFFER KEY rather than by the two fixed names
`outline` and `document`; `typed_proposal.target` as a buffer key rather than a
two-value enum, with the proposal list bounded by the buffer set rather than by
a literal 2; and `selected_model` metadata beside `model_id`, so a record states
both which model ANSWERED and which entry the human CHOSE (the two differ
exactly when the chosen entry is a routing rule). The v2 request carries no
`active_document_path`: the binding is DECLARED, never inferred from an adjacent
field that answers a different question.

**The v1 request, success and failure blocks are BYTE-IDENTICAL to their
contract-v1.31 bytes** and keep validating; a client that submits the previously
released shape is still served. That byte identity is asserted by a test against
a committed baseline, not by re-validation. The file's own
`contract_schema_version` stays `1`, and the envelope-level `schema_version`
stays `1` with it, because nothing previously valid becomes invalid.

**Deprecation, with its removal target recorded.** The whole v1 family
(`workbench-chat-turn`, `workbench-chat-turn-success`,
`workbench-chat-turn-failure`) is DEPRECATED as of this release. The record is
machine-readable in the schema's own top-level `deprecated_envelopes` block —
placed outside every envelope precisely so the deprecated bytes do not move.
Removal target: **contract-v2.0**, which is the next major and therefore the
earliest release at which a removal is legal; this deprecation starts the
"at least one full minor release where the old shape produced deprecation
warnings" clock the policy's breaking path requires. Migration: submit
`workbench-chat-turn-v2` instead of `workbench-chat-turn`; carry every loaded
buffer in `buffers` rather than exactly two; replace `active_document_path` with
`bound_buffer` (the key of the buffer the conversation is working ON, which must
name one of the buffers the same request supplies); read `observed_hashes` and a
proposal's `target` as buffer keys; and read the answering model from `model_id`
with the chosen entry from `selected_model`.

**What the deprecation does to your tooling.** The family's delegated validator
(`scripts/validate-ideation-dashboard-contracts.py`) reads the schema's own
`deprecated_envelopes` block and now emits ONE WARNING per validated v1 instance,
naming the superseding kind and the removal target — that warning is what the
deprecating change class requires, and the instance is still ACCEPTED, so the
default invocation still exits 0. The consequence to plan for: under the opt-in
`--strict` flag ("treat warnings as errors") a v1 instance now exits 1. That is
strict mode working as documented, and it is the intended way to find the shapes
that will not survive `contract-v2.0`; it is no longer the right command for
gating a corpus that legitimately still holds v1 instances.

## contract-v1.33 — 2026-08-15 (additive; the client-identity roster, and the credential-contracts registration gap closed)

Realizes `add-client-identity-roster` through Speckit feature
`007-client-identity-roster`: one new neutral contract family, one first-ever
registration of an already-promoted schema, and additive growth in two
existing capabilities. **Every change in this cut is ADDITIVE under
[`docs/contract-versioning-policy.md`](../docs/contract-versioning-policy.md)
lines 130-132** — the class is "new optional fields, new contracts, new
validator warnings", and its test is that a domain repo on the same major
version remains conformant WITHOUT CHANGES. Each item below is stated against
that test explicitly, because the cut touches capabilities domains already
consume.

`schemas/xfactory-client-identity-roster.schema.yaml` is the NEW family: the
record in which a domain factory declares every governed identity it holds
standing inside a paying client's provider tenant, and the report-only drift
finding that reports when observed state departs from that declaration. Two
kinds behind one top-level `oneOf`, because the fragment and the drift record
that cites it are produced and consumed by one lane and the five-element
uniqueness tuple — (domain, admission surface, authority class, blast-radius
unit, duty) — must be defined once and referenced by both. Entries carry
verified admission with achieved scope (a claimed-but-unevidenced verification
is unrepresentable, not merely discouraged), structural scoping preferred over
name-based scoping, declared provider-forced breadth where the provider offers
no narrower grant, and a fragment-scoped free-token legend. **Additive by the
policy test: it is a NEW contract, so no existing record is reinterpreted and
no domain repo needs an edit to stay conformant.** A domain that publishes no
fragment stays conformant and its checks report a notice, never a finding.

`schemas/xfactory-credential-contracts.schema.yaml` receives its **FIRST
manifest registration** in this cut. The schema was promoted at DTN-004
(`promote-credential-contracts`) without a manifest row, so the digest
cross-repo consumers are told to verify did not exist for the file they pin;
this cut closes that gap rather than refreshing anything. Registered together
with its one growth: the OPTIONAL `issuance_preconditions` object on a
credential requirement, a CLOSED vocabulary (`accepted_request_required`,
`registered_active_subject`, `roster_drift_clear_required`) in which every
value is `const: true`, because a precondition is DECLARED or NOT DECLARED —
`false` is not a second meaning, it is a declaration that reads as governance
while asserting nothing. **Additive by the policy test: the property is
OPTIONAL, so a requirement record that declares nothing at all remains valid,
and both live OpsxFactory records already carry `true`.**

`schemas/consent-instrument.schema.yaml` (`contract_schema_version` 1 → 2) and
`schemas/consent-instrument-class-registry.schema.yaml`
(`contract_schema_version` 1 → 2) grow so the termination cascade reaches a
standing identity in another party's tenant. The lifecycle enum gains
`withdrawn` as a SECOND TERMINAL state, reachable once the instrument is past
execution and a DISTINCT member — never an alias of `terminated`, because
withdrawal by the consenting party and termination are distinct events that
both raise the cascade obligation; the class registry's `status_aliases`
target enum tracks that six-state lifecycle. `dependent_refs` gains the NAMED
`governed_identity` kind with two evidence siblings
(`identity_removal_evidence`, `admission_withdrawal_evidence`), because a
credential revocation alone leaves the identity standing in the client's
tenant with its admission intact, and removing one of the two keys is a
half-cascade. **Additive by the policy test on both counts: an ADDED ENUM
MEMBER and OPTIONAL properties. No existing instrument becomes invalid, no
existing alias declaration becomes invalid, and no domain repo on the same
major version needs a change** — which is why the RECORD envelope's
`schema_version` stays `const: 1` in both schemas while the schema files'
`contract_schema_version` bumps: bumping the record envelope would invalidate
every instrument in the estate, the opposite of additive. The two manifest
digests are refreshed with the bump recorded in their `consumption_rule`.

Consumers pin this release and run
`scripts/validate-client-identity-roster.py <domain-repo>` from the pinned
checkout, never a copy inside a domain repository; the packaged corpus is
`examples/client-identity-roster/` — 4 example YAMLs and a README, plus 31
registered negatives under `negative/`, each failing for its own registered
reason. The roster paths are content-addressed by commit and deliberately do
NOT enter the release digest inventory, whose membership is unchanged from
v1.30, v1.31 and v1.32. `scripts/validate-credential-contracts.py`'s
skip-with-notice over `credentials/client-identity-roster/` is EXPECTED and
BLESSED: the canonical roster validator claims exactly that path.

## contract-v1.32 — 2026-08-15 (additive; the Subject Hermes overlay kind)

Cuts the standing Unreleased items: the `hermes_subject_overlay` kind and
validator dispatch (add-subject-overlay-contract, ratified 2026-08-15,
PR #183 merged cb738ba5) and the openxwallet RSA signature-algorithm
widening. Also corrects the `omnigent-domain-overlay` manifest digest,
which drifted when df16f21 edited the schema without refreshing the
recorded digest.

- **Additive**: `contracts/hermes-domain-overlay/hermes-subject-overlay.schema.yaml`
  — the neutral `hermes_subject_overlay` kind for a Subject Hermes layer's
  seedable document (add-subject-overlay-contract, ratified 2026-08-15).
  Subject identity (`id`, not `ref` — a subject overlay DECLARES an identity
  that exists in no prior registry), a `policy_namespace`, a declared
  `relation_to_baseline` (single-value enum `additive_constraints_only`), and
  a non-empty `policies` mapping keyed by policy id whose entries restate
  their own `policy_id` and `policy_namespace` and keep an OPEN body — so a
  named policy is addressable as `<policy_namespace>/<policy_id>` without the
  neutral contract enumerating policy names, which is exactly what stopped the
  tenant-layer override contract from carrying one. The kind name is canonical
  (`subject`) while the runtime layer role key stays the frozen `customer`;
  the mapping is recorded in the schema header, and neither side is renamed.
  `scripts/validate-hermes-domain-overlay.py` gains the kind and now dispatches
  descriptor-declared paths BY KIND instead of skipping everything that was not
  a domain overlay, retaining the skip-with-notice for kinds owned by another
  canonical validator (`hermes_client_overlay` →
  `scripts/validate-client-content.py`); it adds address self-consistency and
  uniqueness, the prohibited-block list, and cross-document identity
  conformance against the domain's own `subject_hermes_template` (absent
  template = skip with notice, no new refusal class). One positive example and
  eleven negatives ship with it (eight document-shaped, three repo-shaped).
  Additive only: no released file's bytes change, so existing pins — including
  hermes-install's `contract-v1.18` pinned copies — resolve byte-identically
  until they choose to re-pin. Manifest entry added; the bundle minor number
  and annotated tag are allocated LATE at realization per the versioning
  policy.
- **Additive**: `openxwallet-record.schema.yaml` `signature_algorithm`
  enum widened with `rsa-2048-sha256` and `rsa-3072-sha256`
  (RSASSA-PKCS1-v1_5 over the named SHA-2 digest). Found by the first
  consumer, the LedgerxFactory posting segregation-of-duties control:
  its enforcement surface verifies proofs with Business Central's own
  crypto, and BC 28.3 AL exposes exactly RSA/DSA/RSASSA-PSS — no
  ed25519, no ECDSA (measured against the 28.3 System Application
  symbols, enum 1446 SignatureAlgorithm). The curve-only enum therefore
  admitted no algorithm the platform could verify locally, forcing
  verification off-platform against the consumer's local-decision rule.
  Existing records remain conformant; one positive example added
  (`wallet-agent-rsa-platform-verifiable.example.yaml`, corpus now 17
  positives); manifest digest for the schema refreshed with the
  amendment noted in its `consumption_rule`.

## contract-v1.31 — 2026-08-07 (additive; the openxWallet core and its first profile)

Realizes `add-openxwallet` tasks 3.1 and 3.2 through Speckit feature
`006-openxwallet-contracts`, registering two new neutral contract families and
modifying no existing capability.

`contracts/openxwallet/` is the HOLDER-AGNOSTIC core — a wallet is a signing
key anchored to a decentralized identifier and held by a person, practitioner,
organisation or agent. Six kinds: the wallet record (a key REFERENCE and a
declared custody model, never key material, with every object closing
`additionalProperties` so no key-shaped field can be added at any depth); the
closed custody registry; the attenuated capability grant (audience, scope,
expiry, parent, narrowing monotonically); the grant exercise record (proof of
possession, key attribution, revocation checked at use, distinct-holder
evaluation); the opt-in distinct-holder constraint; and the subject
attestation carrying the non-substrate rule that preserves MedxFactory's two
ratified wallet constraints.

The custody registry is where Brett's ruling of 2026-08-07 — custody is
DECLARED from a closed set and CAPS authority — becomes contract content
rather than an implementation detail. `evidences` is DERIVED from two declared
booleans and enforced, not asserted: a key readable by the holder's own
execution context evidences the ENVIRONMENT, and only isolation together with
an authorization that context cannot supply evidences the HOLDER. Three
invariants make the collapse the ruling closes structurally impossible rather
than discouraged — the derivation itself, a top-of-ladder ceiling that must be
earned (keyed on RANK, not on the tier's name, so renaming the top tier cannot
disable the rule), and a check that no model evidencing only the environment
sits at or above a model evidencing the holder.

`contracts/openxwallet-agent-profile/` is the FIRST profile over that core,
registered as a SIBLING family rather than an extension of it, so patient and
practitioner profiles arrive the same way. It settles the change's open task
3.2 — what the composition component set covers — by giving every component a
`binding_mode`: `content` digests the component itself, while `reference`
covers a corpus's identity and governing configuration but not its row-level
contents. Swapping a corpus or widening retrieval scope changes identity and
revokes; documents arriving in an already-governed corpus do not.

Consumers pin this release and run `scripts/validate-openxwallet.py` from the
pinned checkout. The validator enforces nineteen rules the shapes cannot
express and READS the legal approval-scope vocabulary out of
`contracts/schemas/hermes-job-envelope.schema.yaml` at run time rather than
restating it, because restating it would recreate the parallel authority
vocabulary the profile's third requirement forbids. The packaged corpus
comprises 16 valid examples and 33 intended-invalid negatives covering 11 of
11 ratified requirements, with coverage closed in both directions — a
requirement with no probe, and a probe naming no requirement, are both
validation failures. A red-proof harness recorded with the feature confirms
all 21 finding codes are load-bearing: suppressing any one turns the corpus
red.

No runtime, wallet infrastructure, key storage, issuance service, or signing
implementation lands with this release; no key, credential or wallet is
created; and no domain is obliged to adopt wallets. The `openxVault` boundary
Brett set on 2026-07-16 is preserved: the vault owns custody and its gate
consumes these grants.

## contract-v1.30 — 2026-08-06 (additive; cross-factory ideation routing and the consent-instrument family)

Realizes `add-cross-factory-ideation-routing` task 2.4 by registering the
four routing schemas: the canonical idea routing record, the reusable
structured repository-reference kernel, the central Idea-ID allocation
ledger, and the immutable organizer-recommendation evidence shape. Together
they define the governed cross-factory routing plane: one record per
unclassified, mixed, or claim-split idea, single-authority ID allocation,
controlled transitions with destination-owner acceptance, and non-mutating
organizer evidence. Consumers pin this release and run
`scripts/validate-ideation-routing.py` from the pinned checkout; the
packaged corpus comprises 8 valid and 8 intended-invalid examples (44
validator tests green at the cut).

Realizes `add-consent-instrument` task 1.6 (DTN-016 → `adopted`) by
registering the three consent-instrument schemas: the
`xfactory_consent_instrument` record kind (the authority-chain root that
credential grants cite, gates verify, and whose termination cascades
through declared dependent references), the domain-owned closed
instrument-class registry, and the domain-declared purpose model for the
neutral purpose-resolution check. Existing domain instances (the Ledgerx
engagement consent record, the Medx patient consent record) conform by
declaration, never by rewrite. Consumers pin this release and run
`scripts/validate-consent-instruments.py` from the pinned checkout; the
packaged corpus comprises 5 valid examples (including registry and purpose
model), 5 intended-invalid negatives, and 2 purpose-resolution probes.

Also riding this cut: the project-plane ADDITIVE deltas that landed on
`gate-intent`, `gate-action-record`, `ideation-dashboard-snapshot`, and
`xfactory-document-catalog-snapshot` after `contract-v1.29` — the
`create-project` / `edit-project` commissions with `target.project_id`,
multi-parent project membership (D8), and the project-first header fields
(`add-project-scoped-selection`, `add-project-merged-projection`,
`add-opendox-project-header`, each of whose own registration task realizes
against this release). Their per-file manifest digests are refreshed here
so the bundle describes main's actual bytes.

The growth is entirely additive: the pre-existing schema deltas above keep
`contract_schema_version: 1`, and no prior record is invalidated.

## contract-v1.29 — 2026-08-03 (additive; wheel action verbs, gate intents, and worker enrollment)

Realizes `add-wheel-action-verbs` tasks 1.5–1.6 and
`add-ideation-intent-plane` task 2.4. The existing
`gate-action-record.schema.yaml` adds the human-only commission actions
`promote-to-staging`, `derive-possibles`, and `research-brief`, the
`cluster_id` target, verb-specific target requirements, and a required
`workflow-job` companion for each new action. The previously unpublished
`gate-intent.schema.yaml` is registered at the same wheel-expanded shape, so
request and applied-record vocabularies remain in lockstep. The growth is
additive, keeps `contract_schema_version: 1`, and invalidates no prior intent
or action record.

Realizes `add-worker-enrollment-broker` task 1.11 by registering the seven
contract-first worker schemas: enrollment request, lease, enrollment grant,
lease renewal, policy, audit record, and removal grant. Together they define
one enrollment point for fleet and volunteer estates, lease-based authority,
the minimum-app-version renewal floor, estate-specific runner packaging,
trust-tier segregation, transient registration/remove tokens, and
redaction-by-shape audit evidence. Consumers pin this release and run
`scripts/validate-worker-enrollment.py` from the pinned checkout; packaged
fixtures comprise 11 valid and 27 intended-invalid examples.

This release also corrects a catalog defect present in `contract-v1.27` AND
republished unchanged by `contract-v1.28`, without moving or rewriting either
immutable tag. The two doxBench wire schemas were mistakenly typed as Hermes
semantic `schema` members even though they do not carry the Hermes-only root
annotations, causing the Hermes catalog loader to reject the published
catalog. They are now `release-schema` members with `semantic_member: false`:
still closed and digest-pinned in the release inventory, but correctly
excluded from the Hermes semantic registry. Migration is to pin
`contract-v1.29` (the first release whose catalog loads cleanly); the doxBench
wire-schema bytes are unchanged.

Per-file sha256 inventory:
`contracts/releases/contract-v1.29.digests.yaml`.

## contract-v1.28 — 2026-08-02 (additive; the chat-turn request's `active_document_path` is nullable)

Cut in response to codexFactory PR #63 re-verification finding **G-1**
(reviewer Brett Heap, 2026-08-02): measured against the real corpus with
the consumer's own scope authority, 16 of 21 staged topics have exactly
ONE editable path — the topic's own primary fragment, which doxBench loads
as the OUTLINE — so requiring a non-null `active_document_path` made a
legal turn impossible on ~76% of real topics and the chat surface refused
on all of them. Strictly widening: every instance valid before this cut is
still valid.

- **`xfactory-workbench-chat-turn` request: `active_document_path` is
  nullable** (additive; no `contract_schema_version` bump). The request key
  stays REQUIRED and its value becomes `oneOf: [null, confined_path]`,
  mirroring `buffer_state.path` exactly — the same shape, for the same reason:
  a path that does not exist yet is `null`, never a fabricated string. Growth
  source: **G-1**, the codexFactory PR #63 re-verification finding (2026-08-02,
  reviewer Brett Heap), measured against the real corpus with the consumer's
  own scope authority — 16 of 21 staged topics have exactly ONE editable path,
  the topic's own primary fragment, which doxBench loads as the OUTLINE. With a
  non-null value required, no legal turn existed on ~76% of real topics and the
  chat surface refused on all of them. Realizes part of
  `add-workbench-integrated-editor-chat` task 2.5's contract package (see that
  change's ledger note); the consumer contract is codexFactory
  `specs/010-doxbench-editor-chat/contracts/chat-turn.md`.
  - Compatibility: strictly widening. Every instance valid before this change
    is still valid; no producer must change; a consumer that already handles
    `buffer_state.path: null` handles the same fact here. Domain repos pinned
    to `contract-v1.27` are unaffected until they choose to advance.
  - Rides with it: a new packaged positive example
    (`examples/ideation-dashboard/workbench-chat-turn-outline-only.example.yaml`
    — the outline-only turn) and two delegated-validator tests (a null
    `active_document_path` validates; an ESCAPING one is still refused). The
    delegated family validator needed no change: its `_confined` helper already
    judges only paths that exist, which is how `buffer_state.path` nullability
    landed.
  - **Operator's cut still owes:** the `contracts/manifest.yaml` per-file
    sha256 refresh for the amended schema (`validate-manifest-digests.py`
    currently reports 1/109 failing, by design in this pending state), the
    version allocation, the realized digest inventory, and the annotated tag —
    none of which a proposal may reserve ahead of merge order (Contract
    Versioning Policy, "Bundle Realization Order").

## contract-v1.27 — 2026-07-30 (additive; doxBench model-catalog and chat-turn wire contracts)

Realizes `add-workbench-integrated-editor-chat` task 2.5: the doxBench
contract-first package lands as two NEW canonical schemas —
`xfactory-workbench-model-catalog.schema.yaml` (the GET
/workbench/model-catalog success envelope; public seven-field allowlist,
structurally closed, empty-catalog = editor-only posture) and
`xfactory-workbench-chat-turn.schema.yaml` (the POST
/actions/workbench/chat-turn family: request / validated success / fixed
redacted failure, exact-UTF-8 SHA-256 content identity, non-identity
`working_subject`, closed envelopes throughout). Instance kinds use the
retained `workbench-*` identifier family (`workbench-model-catalog`,
`workbench-chat-turn`, `-success`, `-failure`) per the compatibility ruling;
file names carry the manifest's `xfactory-` artifact prefix. Six positive and
eight single-violation negative examples land under
`examples/ideation-dashboard/` (plus the duplicate-turn-id pair), and the
delegated family validator grows the catalog/request/success/failure and
turn-id-sweep rules with its own pytest suite
(`tests/ideation_dashboard/`). Existing dashboard/session artifacts remain
valid; no pre-growth snapshot or gate record is invalidated (task 2.4).
Per-file sha256 inventory: `contracts/releases/contract-v1.27.digests.yaml`.

## contract-v1.26 — 2026-07-30 (additive; ideation-dashboard workbench family registration)

Realizes the four predecessor registration tasks — `add-staging-workbench`
1.7, `add-workbench-bullseye-and-create` 1.6, `add-dashboard-repo-selector`
1.6, and `add-workbench-branch-sessions` 1.6 — as the family's first
`contracts/manifest.yaml` registration beyond the README doc index (the
ideation-possibles-register precedent, contract-v1.14). Per-file sha256
entries for `ideation-dashboard-snapshot.schema.yaml` (staged-topic growth,
add-staging-workbench), `gate-action-record.schema.yaml` (create/document
action growth, add-workbench-bullseye-and-create; branch-session verb growth
plus the D23 `provenance` block, add-workbench-branch-sessions 1.1/1.2/1.8),
and the NEW `ideation-dashboard-snapshot-index.schema.yaml` locator
(add-dashboard-repo-selector). README contract index rows updated. No schema
bytes change at this cut — the growth landed additively with its owning
changes; this cut registers the family's content-addressed identity in the
manifest. No `contract_schema_version` bump; the delegated strict validator
(`scripts/validate-ideation-dashboard-contracts.py`) stays content-addressed
by commit. The four owning task checkboxes remain open until this exact
candidate lands on published `origin/main` and the annotated tag verifies.

## contract-v1.25 — 2026-07-30 (additive; the semantic kernel publishes — the bootstrap window closes)

Realizes **publish-semantic-kernel** (ratified 2026-07-30): the first
governed publication of the xFactory semantic kernel. `xf/core` releases
0.1.0 → 1.0.0 (additive, same compatibility line) through
`ontology-release.py`, decided by the accountable
`openxfactory-maintainers` council — every one of the 25 concepts and 9 relations published with evidenced adoption (two independent resolvable
adopters each), the per-term steward act explicit under the F18 gate, the
package-level adoption block carried through the faithful rewrite (the
F21 kernel scenario in production), and both retained snapshots born
`lifecycle_state: superseded`. Published digest `37090ba2…369038`; the
three kernel registrations refresh accordingly. Spec delta: the
`xfactory-semantic-kernel` bootstrap allowance CLOSES — the active kernel
line never regresses to pending adoption; new terms in future revisions
may record pending only while their revision is unpublished. Consumers:
MedxFactory d01ae62 + codexFactory de60c0c re-pin `kernel_import` to the
published digest. No term's meaning changed: publication moved lifecycle
and version, never label, definition, parents, domain, or range.

## contract-v1.24 — 2026-07-30 (additive; ontology stewardship hardening — guarantees move from procedure to tool)

Realizes **add-ontology-stewardship-hardening** (ratified 2026-07-30), the
stewardship pass closing the domain-ontology release review's
carried-forward findings. Schema bytes: `ontology-stewardship-policy`
(a required quality signal declares `min_value` OR `max_value` — rate
ceilings are expressible directly, vacuous signals fail; F26) and
`ontology-starter-provenance` (the optional `placeholders` block —
readiness blocks on the structural record, never a name; F24). Rides the
same change without schema bytes: the starter's `--ontology-only`
adoption mode (v14; mature repositories adopt without the whole-repo
scaffold), the inventoried STARTER marker (deleting it breaks the package
digest; F25), release-tool housekeeping (faithful manifest rewrite incl.
`adoption`/`notes`, evidence-path containment, retained snapshots born
`lifecycle_state: superseded`; F21), the cadence-deadline rule, and
EXECUTED memory-gateway semantic conformance fixtures (probes run through
the canonical preflight or resolution-verified delegates; F27). Ontology
negative corpus 55. **This cut also delivers the contract-v1.23 erratum
correction**: `contracts/hermes-domain-overlay/content-manifest.schema.yaml`
now records its true digest in `contracts/manifest.yaml`
(`d45a8c89…`, stale v1.18→v1.23), and `scripts/validate-manifest-digests.py`
guards the consumption contract so the class cannot recur. First
consumers: MedxFactory f4ca313 + codexFactory 11777a9 (inventoried
markers).

## contract-v1.23 — 2026-07-30 (additive; omnigent semantic wiring — the worker seam closes)

> **Erratum (2026-07-30, recorded per the release review):** the bundle at
> tag `contract-v1.23` ships a stale digest inside `contracts/manifest.yaml`
> for `contracts/hermes-domain-overlay/content-manifest.schema.yaml`
> (`9511794f…`, stale since 403c2b5 — the add-domain-ontology-layer §4 edit
> that added the `domain_ontology` content kind; the schema's true digest is
> `d45a8c89…`). The tag itself is internally honest (its digest inventory
> matches its own bytes); the defect predates the bundle (carried
> v1.18→v1.23 because nothing verified `contracts/manifest.yaml` digests).
> Corrected in main at commit 792afd2, which also adds
> `scripts/validate-manifest-digests.py` so the class cannot recur; the
> correction rides the next bundle cut. Consumers verifying that schema
> against the v1.23 bundle's manifest should use the corrected digest.
> Note: `contracts/releases/*.digests.yaml` files are TAG SNAPSHOTS —
> verify them against their tag, not against a later HEAD.

Realizes **add-omnigent-semantic-wiring** (ratified 2026-07-30), the
follow-up named at add-domain-ontology-layer task 6.7: the two omnigent
schemas gain the worker semantic seam. `omnigent-domain-overlay` — a
worker class MAY declare `semantic_context: {profile_id, package_id}`
(identity only, authority-free; repo-mode resolution against the domain's
inventoried `xfactory_semantic_context_profile` documents with
worker_scope archetype-or-class agreement). `omnigent-install-manifest` —
optional `semantic_contexts` section pinning exact kernel + domain
ontology digests and one compiled `xfactory_semantic_context` artifact
per declaring worker (both-direction completeness and per-artifact
digest/pin/scope agreement via the canonical `install_wiring_errors`,
exercised by `scripts/test-omnigent-semantic-wiring.py`). Seam hardening
rides the same change without schema bytes: the context compiler refuses
drifted package bytes (review F20) and itemizes truncation transitively
with a validator completeness rule (review F19; ontology negative corpus
50). Permission matrices and the constitutional
`execute_final_action`/`access_secrets` booleans are untouched. First
consumer: MedxFactory 80a81af (two profiles, declarations on
`data_reverification_agent` and `case_framing_agent`, overlay-manifest
re-pinned); codexFactory and install repositories adopt through their own
governed changes.

## contract-v1.22 — 2026-07-29 (additive; domain-ontology family — the semantic plane lands)

Realizes **add-domain-ontology-layer** (ratified 2026-07-28): the
eighteen-kind `contracts/domain-ontology/` meta-contract (package manifest,
concepts, relations, external mappings, source inventory, candidate/release
records, migration map, semantic context + worker profile, quality report,
stewardship policy, maintenance input/report, review fixtures, coverage-gap
report, starter provenance, consumer-impact report) and the `xf/core`
semantic kernel (24 concepts, 9 relation primitives; every term carries its
owning contract and evidenced adoption; DRAFT pending the governed
publication decision). Meaning never authority: closed shapes, reserved
authority-name rejection, and the memory-gateway preflight keep the
semantic plane descriptive; grants/consent/approvals are untouched.
Canonical validator `scripts/validate-domain-ontology.py` (self-test: 8
positive units incl. the retained MedxFactory/codexFactory pilots and the
published-kernel adoption pair, 43 indexed negatives, determinism,
readiness); tools
`apply-domain-starter.py` (v13 ontology generation),
`ontology-maintenance.py`, `ontology-release.py` (accountable-steward
gate, per-signal quality exceptions, consumer-impact evidence, byte-true
self-retention), `ontology-compile-context.py`. Memory-gateway packet
contracts gain the closed `semantic_context` block (this bundle refreshes
`context-packet` / `expert-context-packet` and the layer-vocabulary role
text). First consumer: MedxFactory `hermes/domain/ontology/` (kernel
digest-pinned); codexFactory / hermes-install / omnigent adoption recorded
as explicit deferrals in the change's 8.6 evidence.

## contract-v1.21 — 2026-07-30 (additive; capability-steward contracts — the crystallization flywheel closes)

Realizes **add-capability-steward** (exit 3, closing the
`recurrence-crystallization` staged topic; ratified 2026-07-29, archived
2026-07-30): the seven **capability-steward** record schemas —
`contracts/schemas/{crystallized-capability-registry,dispatch-record,adjudication-record,sentinel-policy,capability-health-report,savings-entry,calibration-score}.schema.yaml`
— the registry record (proof-gated status spine mirroring the document
lifecycle; artifacts digest-pinned while authority is live-read, D10;
digests-never-payloads), the path-invariant dispatch record (six-cause
fallback taxonomy, metered overhead, pure/idempotent admission per D11),
the shared parity/sentinel adjudication record (bidirectional
verdict↔consequence pairing), the strictly-positive-floor sentinel policy,
the capability-health report (auto vs contested findings, cost-ordered
drift responses), and the sentinel-anchored savings entry with the
maturity-graded calibration score. The canonical validator
`scripts/validate-capability-steward.py` (11 named policy rules;
self-testing 6 positives / 10 indexed negatives) and
`examples/capability-steward/` (completing the MVP packet-capture corpus:
the full flywheel now runs in fixtures) are commit-content-addressed
tools and fixtures, no per-file digest. With `contract-v1.19`
(pattern-ledger) and `contract-v1.20` (crystallizer), all three
crystallization waves are canon. Purely additive.

## contract-v1.20 — 2026-07-29 (additive; crystallizer contracts + omnigent crystallized-executor extension)

Realizes **add-crystallizer-contracts** (exit 2 of the
`recurrence-crystallization` staged topic; ratified and archived
2026-07-29): the four **crystallizer** record schemas —
`contracts/schemas/crystallization-{decision,spec,build,consent}.schema.yaml`
— the decision as the only path from candidate to spend
(ceilings-before-valuation, deflation + survival discounting,
shape-not-boolean outputs, the not-yet ledger, frozen L0–L6 rung
vocabulary), the episode-mined micro-spec (acceptance corpus with declared
equivalence predicates, scope fence, effect class), the governed build
record (gapless provenance, dry-run + leak-scan acceptance, declared
artifact residence per the rung→home lean), and the three-tier
default-deny consent grant. Also extends **`omnigent-domain-overlay`**
additively (manifest digest refreshed): the crystallized-executor binding
on the EXISTING five archetypes — so the constitutional matrix binds
verbatim — and per-category `rung_ceilings` with the conservative L3
default, enforced by the extended `scripts/validate-omnigent-contracts.py`
(authority-conservation subset rules: permissions and by_class credential
families never exceed the replaced configuration). The canonical validator
`scripts/validate-crystallizer-contracts.py` (12 named policy rules;
self-testing 4 positives / 9 indexed negatives) and
`examples/crystallizer/` are commit-content-addressed tools and fixtures,
no per-file digest. Purely additive.

## contract-v1.19 — 2026-07-29 (additive; pattern-ledger sensing contracts + derived-model registration catch-up)

Realizes **add-pattern-ledger** (exit 1 of the `recurrence-crystallization`
staged topic; ratified and archived 2026-07-29): the five **pattern-ledger**
record schemas —
`contracts/schemas/pattern-ledger-{episode,outcome-label,recurrence-family,recurrence-forecast,crystallization-candidate}.schema.yaml`
— episodes as derived projections over existing audit/run/metering/label
streams with explicit default-deny consent tiers; append-only outcome
labels (quality is a fold, never a stored verdict); tenant-scoped
recurrence families with recorded merge/split transitions; maturity-dated,
scored forecasts with declared cost-regime assumptions; and the
nominate-never-spend crystallization candidate. The canonical validator
`scripts/validate-pattern-ledger.py` (nine named policy rules; self-testing
7 positives / 7 indexed negatives) and `examples/pattern-ledger/` (incl.
the MVP packet-capture fixture corpus hand-derived from the real
2026-07-28/29 runs) are commit-content-addressed tools and fixtures, no
per-file digest. Purely additive.

Also registers **`xfactory-derived-model-conformance`**
(`contracts/schemas/xfactory-derived-model-conformance.schema.yaml`),
realized 2026-07-23 by archived `add-governed-derived-model` but missed by
the v1.16–v1.18 cuts — the standing Unreleased note is discharged by this
cut. DTN-014 flips `implemented` → `adopted` in the candidate register as
domain pins advance past this registering ref.

## contract-v1.18 — 2026-07-24 (additive; domain content manifest + memory binding)

Realizes **add-hermes-domain-content-manifest** (seeding increment 4b's
contract half; convention-then-contract): the optional
**`hermes_domain_content_manifest`**
(`contracts/hermes-domain-overlay/content-manifest.schema.yaml`) — a domain
repo declares its seedable content set per ratified `content_kind` (exactly
one of `path`/`directory`; absent manifest, consumers keep the documented
increment-4a convention; an undeclared kind never loads silently) — and the
**`hermes_memory_binding`** record shape
(`contracts/memory-gateway/memory-binding.schema.yaml`), formalizing the
derived binding hermes-install increment 3 materializes: rails input in the
ratified gateway vocabulary (promotion gateway constitutionally
`customer_memory_gateway`, `accepted_authority_level` drawn from
`authority_levels`), never a provider binding — any provider/credential
surface fails the canonical validator. Realization anchors: the codexFactory
conventional set declared verbatim; the two LIVE-derived opensoft bindings
as the packaged example. Purely additive.

## contract-v1.17 — 2026-07-23 (additive; client-content tuning surface)

Realizes **add-client-layer-tuning-contracts** (phase 2a of the layer
activation path): the neutral tenant-layer contract set — three client
content kinds (`client_policy_overrides` with stricter_only + budget
envelopes + tracking granularity + the human-ratified auto-clear envelope,
`client_memory_boundaries` with the tenant_isolated invariant,
`client_integration_boundaries` reference-only) and the seedable
**`hermes_client_overlay`** (canonical path
`config/clients/<client_ref>/overlay.yaml`, descriptor-declared,
`client_overlays[]`-pinned). Canonical validator
`scripts/validate-client-content.py` implements the stricter-only
comparability spec with a `review_required` fallback and self-testing
fixtures. Also in this bundle: the neutral house-team roster
(`templates/client-layer/roles/` — 10 deciders incl. the Finance &
Accounting Officer + the liaison capability, voice floor locked) and the
scaffold's `cost_reporting_steward`. Purely additive.

## contract-v1.16 — 2026-07-23 (additive; omnigent contract family + layer vocabulary)

Tenth annotated-tag release. Realizes **add-omnigent-domain-overlay** (the
Omnigent execution layer's domain-tier contracts) and registers
**adopt-subject-tenant-domain-vocabulary**'s policy artifact:

- `contracts/omnigent/omnigent-domain-overlay.schema.yaml` — per-domain
  overlay payload: worker classes mapped to the five neutral archetypes
  (frame/generate/verify/challenge/assemble_for_admission), the generalized
  six-boolean permission matrix with constitutional
  `execute_final_action`/`access_secrets` `const: false`, four credential
  tiers including `never_assignable`, domain-level permission aliases,
  whole-document `worker_profiles` payload, `stricter_rule_wins`
  composition under the `domain_installation_overlay` operations.
- `contracts/omnigent/omnigent-install-manifest.schema.yaml` — the install
  manifest: hermes-install rendered runtime manifest digest-pinned as the
  single stack identity (no parallel identity by construction), exactly one
  domain overlay, the authoritative subject-workload registry, pre-rendered
  effective-profile provenance. First family with canonical
  Subject/Tenant/Domain machine spellings from birth.
- `contracts/policies/layer-vocabulary.yaml` — the ratified canonical layer
  vocabulary: names + roles, the customer→subject / client→tenant legacy
  mapping, reserved layer terms, the frozen-identifier inventory (migration
  staged dormant at `ideation/staging/layer-vocabulary-machine-migration/`),
  and the per-domain alias table.

Canonical validator `scripts/validate-omnigent-contracts.py` with packaged
examples and marked negative fixtures (commit-content-addressed tools, no
per-file digest). Realization evidence: canonical domain overlays in
codexFactory (`engineering-omnigent-overlay`) and MedxFactory
(`medical-omnigent-overlay`); Omnigent-Install's live manifest with
fail-closed compose/verify, byte-equivalent rendered coding-patch-worker
binding, and the MedxFactory second-domain params fixture. All additive:
every released path from `contract-v1.7` through `contract-v1.15` is
byte-identical.

## contract-v1.15 — 2026-07-23 (additive; hermes-domain-overlay contract surface)

Ninth annotated-tag release. Realizes **add-hermes-domain-overlay-contract**:
the neutral `hermes_domain_overlay` schema (domain identity, non-empty
approval scopes and required fields, authority boundaries with the
canonical-validator-enforced `<domain.id>_owns` naming and no-overlap rules)
and the `hermes_overlay_descriptor` role→path declaration (runtime layer
roles domain/client/customer as keys — deliberately not directory names —
with a documented-convention fallback when absent and fail-closed dangling
paths). New canonical validator `scripts/validate-hermes-domain-overlay.py`
with self-testing packaged examples/negatives under
`contracts/hermes-domain-overlay/examples/`. Realization proof: codexFactory's
live 37-authority `hermes/domain/overlay.yaml` passes unmodified via the
convention fallback. Replaces the hermes-install seeding runtime's minimal
structural check at its materialization increment (which pins this release).
Purely additive; no existing contract touched.

## contract-v1.14 — 2026-07-22 (additive; possibles-register AI-derivation intake)

Eighth annotated-tag release. Realizes the **possibles-derivation lane's
contract surface** (`add-possibles-derivation-lane`, task 2.6 registration at
the realization commit): the ADDITIVE AI-derivation intake delta on the
`ideation-possibles-register` kernel — optional `register_entry.origin`
(enum `[human-authored, ai-derived]`; absent defaults to human-authored),
optional `register_entry.derivation` (worker-run identity: correlation id /
worker profile / prompt-contract version, plus machine
`disposition: pending_review` and the `derivation_human_disposition` local
mirror of the index's `human_disposition`), and the `allOf` conditional that
requires `derivation` when `origin: ai-derived`. Modelled one-for-one on the
index topic entry's `origin` + `human_seen` intake pair; the conditional
never fires on an origin-absent entry, so `contract_schema_version` stays 1
per the kernel's additive-growth rule and every released path from prior
bundles is byte-identical.

Registered — `contracts/schemas/ideation-possibles-register.schema.yaml`
(per-file SHA-256 recorded in `contracts/manifest.yaml`; the kernel's first
manifest registration — the ideation-dashboard family was previously
registered in `contracts/README.md`'s doc index only). Packaged examples:
`examples/ideation-dashboard/derived-possible-register.example.yaml` plus
the derived negatives and one-way-disposition transition pairs, all enforced
by the delegated strict register validator
(`scripts/validate-ideation-dashboard-contracts.py`, extended at task 2.4).

Realization evidence: codexFactory `specs/004-derive-possibles` — the
derive-possibles worker (PR #25), the nightly lane + watchdog + rolling-PR
register commit-back (PR #27), and the omnigent-install `derive-possibles`
worker profile (Omnigent-Install PR #22, contract-only until host
deployment). The nightly lane reports SKIPPED until a host advertises the
profile — the readiness-scorer precedent's valid landed state.

## contract-v1.13 — 2026-07-17 (additive; client-infrastructure-request contract family)

Seventh annotated-tag release. Realizes the neutral **client-infrastructure
contract family** (`add-client-infrastructure-liaison`): the durable
`client_infrastructure_request` coordination record, the signed/traceable
`infrastructure_readiness_result` artifact, and their strict openxFactory
validator, promoted at this change's archival (task 5.1) out of the "Contracts
Pending Realization" holding area that task 2.5 added to `contracts/README.md`.
All additive: every `contract-v1.7` / `v1.8` / `v1.11` / `v1.12` released path
is byte-identical and `contract_schema_version` is unchanged.

Added — two `contracts/schemas/xfactory-*.schema.yaml` contracts
(YAML-serialized JSON Schema draft 2020-12, `contract_schema_version: 1`;
per-file SHA-256 recorded in `contracts/manifest.yaml`):

- `xfactory-client-infrastructure-request.schema.yaml` — the
  `client_infrastructure_request` durable coordination record (never a Hermes job
  envelope): six never-conflated identity-reference `$defs`, the three-mode
  `execution_binding` (`client_managed|managed_host|opsxfactory_executed`, design
  D1), the closed 13-state `status` enum, orthogonal `conditions[]`, the embedded
  `handoff` acceptance record, digest-bearing `package_refs`, cancellation
  `child_acks`, and `supersedes_request_ref`.
- `xfactory-infrastructure-readiness-result.schema.yaml` — the
  `infrastructure_readiness_result` signed/traceable readiness artifact, never a
  bare boolean: status `ready|degraded|not_ready|unknown|maintenance`,
  `valid_until` freshness, non-privileged validator + trust refs, per-check
  `mandatory`/`outcome`/evidence, and `evidence_digest`.

Also added — `scripts/validate-client-infrastructure.py`: strict validator for
both kinds — schema conformance, embedded-secret rejection (shared avatar-client
denylist), transition legality including terminal immutability and
readiness-gated completion, identity-class separation (actor ≠ authority ≠
creating liaison; a subject id never in a typed field), idempotency/supersedes
integrity, and cancellation-acknowledgment presence — self-testing the packaged
reference examples (`examples/client-infrastructure/`: 4 valid + 9
one-violation-each negatives). Registered as a tool and content-addressed by
commit; not a pinned semantic artifact, so excluded from the per-file digest set.

Governance:

- The liaison and no domain agent ever holds tenant-administration authority; an
  `infrastructure_readiness_result` is never a bare boolean and gates a
  `client_infrastructure_request` completion only when fresh (used before
  `valid_until`), overall `ready`, and every mandatory check passes. The governing
  role doc `docs/client-infrastructure-liaison.md` is ratified alongside this
  change (`Status: ratified`; `Ratified by: add-client-infrastructure-liaison`),
  with product-owner sign-off on design D1 (execution-binding tokens) and D5
  (roles-authority wording) recorded by Brett 2026-07-16 (task 4.1). It is prose
  governed by this changelog, not a per-file manifest member.
- Fail-closed validation: `scripts/validate-client-infrastructure.py` self-test
  confirms 4 valid examples and 9 negatives each failing for its intended reason;
  `OPENSPEC_TELEMETRY=0 openspec validate add-client-infrastructure-liaison
  --strict` is green. The reference validator is content-addressed by commit and
  carries no per-file digest.

Also added — `contracts/releases/contract-v1.13.digests.yaml`: the raw-Git-blob
SHA-256 release digest inventory for this bundle (built by
`scripts/validate-contract-release.py`), refreshing the closed hermes-runtime
release surface plus the `manifest.yaml` / `CHANGELOG.md` / `README.md`
auxiliaries; the client-infrastructure family is outside that closure and is
content-addressed via `manifest.yaml` per-file digests instead.

Consumers: the per-domain adoption successors (OpsxFactory binding/readiness
producer first, then the Medx/Ledger/Ad/codex aliases) pin this bundle at the
`contract-v1.13` tag and verify the per-file SHA-256 in `manifest.yaml` before
treating a copy as current; openxFactory ships no instance records (they live in
client installs, credential-contracts residency model).

## contract-v1.12 — 2026-07-15 (additive; avatar-client-lab evidence surface / P-row adoption)

Sixth annotated-tag release. Realizes the neutral **avatar-client-lab evidence
surface** (`adopt-avatar-client-lab-candidates`), the P1/P10 owning change that
adopts the panel-confirmed layer-2 evidence candidates from codexFactory
`002-avatar-client-lab` @ `3a8fbd5` (7/7 confirmed; provenance in that feature's
`upstream-drafts/STATUS.md`). All additive: every `contract-v1.7` / `v1.8` /
`v1.11` released path is byte-identical and `contract_schema_version` is unchanged.

Added — two neutral, content-addressed client-lab artifacts under
`contracts/avatar-client-lab/` (per-file SHA-256 recorded in
`contracts/manifest.yaml`):

- `avatar-state-derivation-table.yaml` — the P1 total avatar-state derivation
  table (design D3): the precedence-ordered R0..R6 derivation plus the enumerated
  healthy-control matrix mapping the four authoritative runtime axes onto the six
  FR-019 avatar presentation states, embedding the normative invariants, with
  OQ-1..OQ-6 ratified (product-owner sign-off Brett 2026-07-15). Gate
  (vi)/(ix)(a) source. Its normative `.md` companion
  (`avatar-state-derivation-table.md`) and `README.md` are prose governed by this
  changelog, not per-file manifest members.
- `capability-scenario-register.yaml` — the P10 capability-scenario register
  (9 requirements / 22 scenarios; Option B, design D2): stable `ACL-*` ids and
  verbatim `#### Scenario:` titles machine-checked fail-closed in document order
  against the `implement-avatar-client-lab` capability spec. Gate (ix)(b) source.

Added — the 20 adopted deterministic fixtures under
`examples/avatar-first-ui/fixtures/deterministic/` (per-file SHA-256 in
`manifest.yaml`), closing the state-reachability denominator via AVC-12 kernel
fields only: P7 intake breadth (5), P8 lease/epoch takeover + snapshot-barrier
recovery (4), P11 `interrupted`/`handoff` (2), and P12/P13 the eight non-control
closed `media.states` + `control_degraded` (9). The five pre-existing released
seeds already in that directory stay unregistered (not this change's members).

Added — `contracts/avatar-client/evidence-register.implement-avatar-client-lab.yaml`,
the SCO-001-S05 successor deferral-discharge register (locked decision 7 of
`implement-avatar-client-lab`, task 4.4). Registering it here — the release-time
manifest convention first used at `contract-v1.9` (bundle members join
`manifest.yaml` only when the next additive version is cut, never mid-change) —
makes the `deferred → evidenced` discharge effective WITHOUT mutating the
released, byte-identical `evidence-register.yaml` (a contract-v1.9 member).

Governance:

- Settled law L2 (the app never self-serves neutral artifacts): all candidates
  land at their upstream openxFactory source; the codexFactory
  `apps/avatar-client-lab/` app consumes them read-only as
  `vendored_evidence_inputs` at its `contract-v1.12` pin resync (this change's
  codexFactory realization surface).
- Fail-closed validation: `scripts/validate-avatar-client.py` carries
  `check_avatar_state_derivation_table` and `check_capability_scenario_register`
  (both fail-closed, with negative coverage); with the successor register now
  manifest-listed, `--require-realization` passes (0 errors).
  `scripts/validate-avatar-first-ui.py` (baseline + realization) stays green. The
  reference validators are content-addressed by commit and carry no per-file digest.

Also added — `contracts/releases/contract-v1.12.digests.yaml`: the raw-Git-blob
SHA-256 release digest inventory for this bundle (built by
`scripts/validate-contract-release.py`), refreshing the closed hermes-runtime
release surface plus the `manifest.yaml` / `CHANGELOG.md` / `README.md`
auxiliaries; the avatar-client-lab surface is outside that closure and is
content-addressed via `manifest.yaml` per-file digests instead.

Consumers: the codexFactory `apps/avatar-client-lab/` lab pins this bundle at
the `contract-v1.12` tag and verifies the per-file SHA-256 in `manifest.yaml`
before treating a vendored copy as current.

## contract-v1.11 — 2026-07-14 (additive; document-cataloging contract surface)

Fifth annotated-tag release. Realizes the neutral **document-cataloging
contract surface** (`add-document-cataloging`): six domain-neutral JSON-Schema
contracts plus their strict openxFactory validator, promoted at this change's
archival (task 8.7) out of the "Contracts Pending Realization" holding area
that task 2.4 added to `contracts/README.md`. All additive: no existing
contract path changes and `contract_schema_version` is unchanged.

Added — six `contracts/schemas/xfactory-document-*.schema.yaml` contracts
(YAML-serialized JSON Schema draft 2020-12; per-file SHA-256 recorded in
`contracts/manifest.yaml`):

- `xfactory-document-catalog-snapshot.schema.yaml` — immutable per-repository
  document-catalog snapshot.
- `xfactory-document-cataloger-recommendation.schema.yaml` — immutable,
  non-authoritative cataloger-recommendation evidence.
- `xfactory-document-tag-registry.schema.yaml` — namespaced topic-tag registry.
- `xfactory-document-tag-overrides.schema.yaml` — owner override / disposition
  file.
- `xfactory-document-opaque-locator.schema.yaml` — reusable canonical/opaque
  document-locator `$defs` kernel.
- `xfactory-document-handling-gate.schema.yaml` — reusable dispatch/handling-gate
  decision `$defs` kernel.

Also added — `scripts/validate-document-catalog.py`: strict validator over the
packaged reference examples (`examples/document-cataloging/`) and the
deterministic cross-cutting invariants JSON Schema alone cannot express
(complete coverage, unique per-snapshot identity, source and review freshness,
taxonomy resolution, override standing, immutable path layout, and the
disclosed baseline-mode coverage exception). Registered as a tool and
content-addressed by commit; not a pinned semantic artifact, so excluded from
the per-file digest set.

Governance:

- Catalog facets are descriptive discovery metadata only: they never set a
  document's lifecycle `Status:`/`Kind:`, ownership, routing state, `xspec:`
  markers, sensitivity approval, or lifecycle changes (see
  `docs/document-lifecycle.md` "Catalog Tags Are Not Lifecycle State" and the
  `document-catalog` family in `docs/doc-health.md`). The adoption guide
  `docs/document-catalog-adoption.md` is ratified alongside this change.
- Realization evidence: the deterministic mechanical baseline covers 225/225
  governed v1 documents across six repositories (xFactory aggregation
  `800a572`), byte-equal to the freshly built extended inventory with zero
  source edits and reproduced identically across two from-scratch runs; strict
  `validate-document-catalog.py` reports 0 errors / 0 warnings against the real
  artifacts and 661/661 codexFactory tests pass at the merged SHA; the
  codexFactory `document-catalog` doc-health family and the non-authoritative
  document-cataloger lane landed in codexFactory PR #4 / PR #6, and the bounded
  read-only cataloger worker profile in omnigent-install `b836a24`.

- Nightly evidence (workflow runs 29328943314 and 29330008234, 2026-07-14):
  the first post-baseline nightly produced the dated report
  `health/reports/2026-07-14.md` (xFactory aggregation `97c4754`) with a
  rendered "Document Catalog" section — 225 of 225 docs cataloged, facet
  states pending=1350 (all other states 0), changes 225 new / 0 changed /
  0 deleted / 0 stale / 0 rejected, classifier `document-cataloger/1`
  prompt contract v1, cataloger skipped fail-closed with
  `runner_labels_missing` (the document-cataloger profile is not yet
  deployed to the artifact-worker host) — and the immutable snapshot at
  `health/document-catalog/runs/2026-07-14/ee0b0ab6…/`. The
  `document-catalog` family contributed zero findings at static pins
  (run 29328943314); run 29330008234's 32 auto-fixable stale-entry
  findings were the ratified freshness contract firing on an unrelated
  mid-window codexFactory pin move, self-healed by the landed snapshot.
  No catalog recommendation entered the Ranked Plan and no catalog-caused
  critical/error regression was introduced.

Consumers: every DomainxFactory pins this bundle at the `contract-v1.11` tag
and verifies the per-file SHA-256 in `manifest.yaml` before treating a copy as
current; the codexFactory `document-catalog` doc-health family and the
document-cataloger worker consume the schemas and validator from their pinned
openxFactory checkout.

## contract-v1.10 — 2026-07-14 (additive; superseding hardening of the neutral Hermes customer-subject runtime, provider side)

Fourth annotated-tag release. A **superseding additive re-realization** of the
provider-side neutral Hermes customer-subject runtime family first cut at
`contract-v1.9`. Per the Immutable Tag Correction policy, the `contract-v1.9`
annotated tag and its digest inventory
(`contracts/releases/contract-v1.9.digests.yaml`) remain in place as immutable
provenance; this bundle carries the corrected bytes under the next available
version. No contract shape changes: `contract_schema_version` is unchanged,
every v1 contract path is untouched, and any consumer that pinned
`contract-v1.9` remains conformant until it deliberately upgrades.

Why a superseding release: after `contract-v1.9` was tagged, two governed
review findings hardened release-surface members, so the frozen v1.9 digest
inventory no longer reproduced the current tree (expected drift, not a defect):

- **F-U3** (`Harden release membership closure`) made the Decision-10 mandatory
  release auxiliaries unconditional members of the closed bundle (no
  `exists()` gate) and repaired two release-fragile tests, changing
  `scripts/hermes_runtime_validation/release.py` and the six
  `contracts/hermes-runtime/fixtures/release/*.yaml` inventory fixtures.
- **F-4 / F-7..F-9** (`Harden migration digest surface`) changed
  `contracts/hermes-runtime/hermes-operational-postgres-v2.sql`.

This release refreshes the raw-Git-blob release digest inventory over the
current bytes and re-establishes manifest/changelog/tag/inventory agreement.

Host-local metadata removal (FR-042): `contracts/manifest.yaml`
`source_compatibility_ref.local_source_path` — a host-absolute developer path
(`/home/brett/...`) — is removed in this additive bundle after the recorded
repository-wide supported-consumer audit
(`openspec/changes/archive/2026-08-27-add-hermes-customer-subject-runtime-contract/evidence/legacy-source-path-consumer-audit.md`,
`Status: record`) proved no supported consumer requires it. Canonical source
repository and source-commit provenance are retained; no consumer, validator,
or DomainxFactory `stack.yaml` resolved the removed field.

Gate G0 remains OPEN: the exact downstream `opensoft/xFactory-Hermes-Install`
consumer pin and its reproduced digests are required to close it and are owned
by that repository's own feature.

Changed:

- `contracts/manifest.yaml` — `contract_bundle_version` -> `contract-v1.10`;
  `source_compatibility_ref.local_source_path` removed (audited; provenance
  `repo`/`source_commit` retained).
- `contracts/releases/contract-v1.10.digests.yaml` — new realized release
  digest inventory (raw Git blob SHA-256; bytewise-`utf8` path order;
  self-excluded and commit-free) for this bundle.
- The `contracts/hermes-runtime/` family,
  `scripts/hermes_runtime_validation/`,
  `scripts/validate-hermes-runtime-contracts.py`,
  `scripts/validate-contract-release.py`, and the hermes-runtime docs are the
  realized surface (governed by `contracts/hermes-runtime/contract-index.yaml`;
  not tracked per-file in `manifest.yaml`), carrying the F-U3 and
  F-4/F-7..F-9 hardening above.

## contract-v1.9 — 2026-07-14 (additive; neutral Hermes customer-subject runtime, provider side)

Third annotated-tag release. Realizes the **provider side** of the neutral
Hermes customer-subject runtime contract family
(`add-hermes-customer-subject-runtime-contract`, feature
`005-customer-subject-runtime`): the domain-neutral customer-subject topology,
trusted-scope authority/binding/approval/traceability records, the PostgreSQL
15/16 operational contract with the governed v1-to-v2 migration and quarantine,
the scoped v2 job/run/event lifecycle, the supported-DomainxFactory regression
denominator, and this bundle's own raw-Git-blob release digest inventory plus
the consumer handoff receipt. All additive: existing v1 contract paths and
pinned consumers are unchanged.

This is the first release to carry a canonical release digest inventory
(`contracts/releases/contract-v1.9.digests.yaml`, schema
`contracts/releases/release-digest-inventory.schema.yaml`): raw Git blob
SHA-256 over every required semantic member, bytewise-`utf8` path order, the
inventory self-excluded and carrying no commit (the annotated tag anchors the
commit; a downstream consumer manifest pins the inventory digest externally).

Gate G0 remains OPEN: the exact downstream `opensoft/xFactory-Hermes-Install`
consumer pin and its reproduced digests are required to close it and are owned
by that repository's own feature.

Changed:

- `contracts/manifest.yaml` — `contract_bundle_version` -> `contract-v1.9`.
- `contracts/releases/contract-v1.9.digests.yaml` — new realized release digest
  inventory for this bundle.
- The `contracts/hermes-runtime/` family, `scripts/hermes_runtime_validation/`,
  `scripts/validate-hermes-runtime-contracts.py`,
  `scripts/validate-contract-release.py`, and the hermes-runtime docs are the
  realized surface (governed by `contracts/hermes-runtime/contract-index.yaml`;
  not tracked per-file in `manifest.yaml`).

## contract-v1.8 — 2026-07-13 (additive; avatar-first UI profile-schema alignment)

Second annotated-tag release. Realizes the **avatar-first UI standard alignment**
(`align-avatar-first-ui-standard`), aligning the domain-neutral
`avatar-first-ui-profile` schema to the released avatar-client (AVC) contract
kernel. This release consumes the `contract-v1.7` kernel **read-only** — each
profile's `runtime_compatibility` pins the kernel bundle tag, exact commit
`ddff475`, and per-file registry/interface-lock SHA-256 digests; no kernel file
is changed.

Changed:

- `contracts/schemas/avatar-first-ui-profile.schema.yaml` — AVC-aligned additive
  OPTIONAL blocks with closed (fail-closed) defaults (`runtime_compatibility`,
  `presentation`, `media`, `outcome_slots`, `fallback_slots`, `interaction_mode`,
  `speech_gate`, `timing`, `consent_purpose_mappings`, `persona_reference`,
  `retention_overlay`, `accessibility_baseline`, `handoff`). Top-level `required`
  keys unchanged; backward compatible. Per-file SHA-256 recorded in
  `contracts/manifest.yaml`.

Governance:

- Offline realization gate `scripts/validate-avatar-first-ui.py --mode realization`
  loads the released kernel registries read-only and fails closed
  (`AFUV-RUNTIME-DRIFT`) on any baseline drift or `runtime_compatibility`
  digest/tag/commit mismatch. The standard doc is ratified
  (`docs/avatar-first-ui-standard.md`; `Ratified by: align-avatar-first-ui-standard`).

Consumers: DomainxFactory repos pin this bundle at the `contract-v1.8` tag and
verify the profile-schema SHA-256 in `manifest.yaml` before treating a copy as
current.

## contract-v1.7 — 2026-07-12 (additive; first annotated-tag release)

First contract release published under mandatory annotated-tag enforcement
(Contract Versioning Policy). Realizes the neutral **avatar-client (AVC)
contract kernel** (`define-avatar-client-contract-kernel`) after the F0
brokered-call feasibility gate passed — 70/70 live trials, client-enforced
revocation (`qualify-avatar-brokered-call-feasibility`, harness commit
`5142065`).

Added — `contracts/avatar-client/` (23-file semantic set; per-file SHA-256
recorded in `contracts/manifest.yaml`):

- `shared-definitions.schema.yaml` plus eight `avc-*.schema.yaml` contracts
  (AVC-01/02/04/06/07/08/11/12) — YAML-serialized JSON Schema draft 2020-12.
- Nine closed registries under `registries/` (session-result-reasons = 15,
  consent-purposes = 3, events, commands, capabilities, fallback-modes,
  interaction-modes, retention-classes, session-outcomes).
- `acceptance-map.yaml`, `interface-lock.yaml` (frozen
  `avatar-client-parallel-v1` baseline + fail-closed F0 publication-gate pin),
  `evidence-register.yaml`, and the `fixtures/` conformance set
  (`index.yaml`, `f0-gate-cases.yaml`).
- `scripts/validate-avatar-client.py` — reference validator carrying the
  fail-closed F0 publication gate (content-addressed by commit; not a pinned
  semantic artifact, so excluded from the digest set).

Governance:

- ACR-005 revocation clarified to **client-enforced within the 5 s bound**
  (`change/clarify-avatar-revocation-client-enforced`); provider-side settle is
  recorded informationally. The registered avatar-client threat model is
  accepted.

Consumers: the avatar-client reference runtime (003) and avatar-first UI
standard (004) siblings pin this bundle at the `contract-v1.7` tag and verify
the per-file digests before treating a copy as current.

## contract-v1.6 — 2026-07-09 (additive)

Added:

- `contracts/schemas/xfactory-credential-contracts.schema.yaml` — the five
  credential record shapes promoted from OpsxFactory evidence
  (promote-credential-contracts change; DTN-004).
- `scripts/validate-credential-contracts.py` — canonical credential
  contract validator.

## contract-v1.5 — 2026-07-09 (loosening, backward compatible)

Changed:

- `contracts/schemas/hermes-job-envelope.schema.yaml` — neutralized
  (neutralize-job-envelope change; DTN-003): `repository` and `feature_id`
  now optional, `job_type` a domain-owned string, new optional neutral
  references (`domain`, `subject_ref`, `client_ref`, `workflow_ref`,
  `focal_item_ref`, `gate_ref`, `artifact_refs`). Engineering strictness
  moves to codexFactory's engineering-job-envelope overlay.
- `contracts/schemas/hermes-job-run.schema.yaml` — `feature_id` optional.
- `contracts/schemas/hermes-job-event.schema.yaml` — unchanged (already
  neutral; lifecycle enums are domain-neutral vocabulary).

## contract-v1.4 — 2026-07-09 (additive)

Added:

- `contracts/schemas/xfactory-workflow.schema.yaml` — neutral workflow
  contract and gate record/blocking vocabulary promoted from four-domain
  evidence (promote-workflow-gate-contract change; DTN-001, DTN-002).
- `scripts/validate-workflow-contracts.py` — canonical workflow contract
  validator (errors for structure, warnings for undeclared owner layers,
  out-of-scope kinds skipped with notice).

## contract-v1.3 — 2026-07-09 (additive)

Added:

- `contracts/schemas/xfactory-domain-stack.schema.yaml` — optional
  `xfactory.promoted_from` and `xfactory.specializes` promotion-provenance
  fields (refine-promotion-provenance change). Backward compatible; existing
  stacks remain valid.

## contract-v1.2 — 2026-07-03 (additive)

Added:

- `contracts/memory-gateway/` — canonical xFactory Memory Gateway contract
  surface for Customer Hermes memory and Domain Omnigent expert
  memory/knowledge access. Includes vocabularies, consent profile, gateway
  request/response, provider profile, binding, mapping, subject safety,
  context packet, expert context packet, expert source, promotion, migration,
  usage, revocation, erasure, break-glass, and audit event schemas.
- `scripts/validate-memory-gateway.py` — canonical validation for gateway
  contracts, provider profiles, conformance fixtures, domain examples, and the
  first local runtime smoke path.

## contract-v1.1 — 2026-07-03 (additive + deprecating)

Added:

- `contracts/schemas/xfactory-domain-stack.schema.yaml` — canonical
  stack.yaml shape. Introduces `hermes.layers`: an ordered list of authority
  layers each bound to a canonical role (`customer` = served subject,
  `client` = tenant/operator organization, `domain` = reusable expert
  domain, `extension` = declared intermediate layer with authority_scope).
  Fixes the cross-domain vocabulary collision where "Client Hermes" meant
  the subject layer in some domains and the tenant layer in others.
- `scripts/validate-domain-factory.py` — canonical conformance validator,
  consumed (not copied) by domain repos. Replaces per-domain hand-rolled
  validators as the conformance baseline; domain validators may extend it.
- `docs/contract-versioning-policy.md` and this changelog.

Deprecated (warnings, removal at contract-v2.0):

- `hermes` flat keys (`subject_overlay`, `subject_layer_name`,
  `care_organization_overlay`, flat `client_overlay`/`customer_overlay`
  styles) in favor of `hermes.layers`.
- `openworkflow_*` owner/layer tokens in workflow gates in favor of
  `xfactory`.

## contract-v1.0 — 2026-06-26 (baseline)

- Initial canonical contract set migrated from install repos: job
  envelope/event/run schemas, clarification packets, avatar-first UI
  profile, domain installation overlay, governance and merge-risk
  policies, hermes operational Postgres DDL.
