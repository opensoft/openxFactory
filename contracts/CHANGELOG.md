# openxFactory Contract Changelog

Status: draft

Governed by [Contract Versioning Policy](../docs/contract-versioning-policy.md).

Legacy baseline note: versions `contract-v1.1` through `contract-v1.6`
predate mandatory annotated tags and carry none. Tag enforcement begins at
`contract-v1.7` — the first realized release published with an annotated tag —
without fabricating historical tags.

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
lines 250-254: a shape is REMOVED. All three of that clause's requirements are
discharged, and each is checkable:

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
