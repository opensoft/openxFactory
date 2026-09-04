# Contract Versioning Policy

Status: ratified
Ratified by: add-release-inventory-drift-check

This policy governs how openxFactory contracts change and how DomainxFactory
repos upgrade. It closes the gap where everything was `schema_version: 1`
pinned to a single commit with no defined upgrade path.

## Version Identity

A contract release is identified by five coordinated values:

1. `contract_schema_version` — an integer on each contract file and on the
   contract set as a whole. Incremented only for breaking changes.
2. `contract_bundle_version` in `contracts/manifest.yaml` — the aggregate
   release version allocated at realization after merge order is known.
3. An annotated git tag on openxFactory of the form
   `contract-v<major>.<minor>` (for example `contract-v1.0`). Minor increments
   are additive and non-breaking; major increments occur together with
   `contract_schema_version`.
4. The exact release commit plus per-file SHA-256 digests — the
   content-addressed identity consumers pin. A movable branch or tag alone is
   not a sufficient compatibility pin.
5. `contracts/CHANGELOG.md` — one entry per release listing every contract
   added, changed, or deprecated, with migration notes for breaking changes.

The manifest version, changelog heading, and annotated tag MUST match. The
manifest and changelog update SHALL be committed atomically with the contract
files; the tag SHALL point to that realized commit. A proposed change MUST NOT
reserve a minor number before merge order is known, and a bundle is not
published until its tag exists. Consumers record the human-readable bundle
tag while pinning the exact commit and required file digests.

### Untagged Bundles After Enforcement Began — DISCHARGED 2026-08-25, AND AGAIN 2026-08-31; INSTANCE SIX IS NOT DISCHARGEABLE

SIX instances. **FIVE were discharged, in two discharges; the sixth cannot be**,
and the header says so rather than carrying a third date that would promise a
closure this section will never record. The first three and the 2026-08-25 ruling
are recorded immediately below; `contract-v2.3` and `contract-v2.4` are recorded
further down under their own dates; `contract-v2.6` — the one that no tag can
reach — is recorded last, under its own subsection. The header carries both
discharge dates because a single one would read as though the section closed once
— and **it has not closed, in the sense that matters**: the recurrence is caused
by the absence of a CHECK, filed as issue **#528**, and a record is not a check.
**The check has since landed** (the `release-tag-publication` doc-health family,
PR #563), which is why instance six was met by a machine rather than by a human
counting — and why it is also the instance that found the check's own missing
vocabulary, filed as issue **#575**.

Three bundles allocated AFTER mandatory tag publication began once carried a
changelog entry and a manifest version but NO published annotated tag:
`contract-v1.33`, `contract-v1.35` and `contract-v1.39`. Recorded here as an
undischarged gap when this policy was ratified, and **DISCHARGED on Brett's
ruling of 2026-08-25** by publishing each bundle's tag at the commit it was
actually realized at:

| bundle | realized commit | landed as |
|---|---|---|
| `contract-v1.33` | `71674ed58e338bf3f85a7b750b64f5f5ab6d02e1` | PR #190, 2026-08-15 |
| `contract-v1.35` | `78f8e016fbddcf1125c11b7f11234fb2478b0415` | PR #220, 2026-08-19 |
| `contract-v1.39` | `1f45e427bf7b2491aec09d2a9c9adeaaa5f99839` | PR #259, 2026-08-22 |

RETRO-PUBLISHED, NOT RE-DATED. Each tag names the commit its bundle was really
realized at; no release was reconstructed, re-cut, or altered, and no version
number was reused.

HOW THE REALIZED COMMIT WAS ESTABLISHED, recorded because the obvious method is
wrong. "The commit that introduced the bundle's changelog entry" reproduces only
five of the ten tags that already existed: where a release was COMPLETED by a
later commit — `contract-v1.31`, `contract-v1.36`, `contract-v1.37` — the tag
points at the completion, and where the work landed through a merge —
`contract-v1.32` — it points at the merge rather than at a branch-internal
commit. The rule actually used is:

> the EARLIEST FIRST-PARENT COMMIT on published `main` that DECLARES the bundle
> and at which `verify-commit` PASSES.

That rule reproduces **all ten** previously published tags exactly, including
`contract-v1.36`'s corrected target, which is why it was trusted for the three
that had none. `contract-v1.39` is the case that needed it: the commit
introducing its changelog entry is inside the change branch and is not a
landing, and tagging that commit would have named a target no other tag's shape
matches.

Every bundle from `contract-v1.7` — where mandatory publication begins — is now
tagged. The legacy `contract-v1.0`–`contract-v1.6` sequence remains untagged by
design, per the recovery recorded below.

**THE SENTENCE ABOVE WAS TRUE WHEN WRITTEN, BECAME FALSE, AND IS TRUE AGAIN —
`contract-v2.3` AND `contract-v2.4` WERE INSTANCES FOUR AND FIVE.** Recorded here
rather than left to be inferred from the sentence's present tense, because a
reader who takes that sentence as evidence the practice never lapsed again would
be reading a claim it does not make.

**AND IT WENT FALSE A THIRD TIME, AND THIS TIME IT STAYS FALSE.** `contract-v2.6`
is instance six, it is untagged, and — unlike all five above — **no discharge can
reach it**. The sentence is therefore left standing as the record of what was true
when it was written, on this document's own rule that a record is annotated and
never rewritten to match today; but a reader must not carry it forward as a
present-tense claim. The current, true statement is: *every bundle from
`contract-v1.7` is tagged EXCEPT `contract-v2.6`, which never can be.* See
§ *`contract-v2.6` — Instance Six* below.

| bundle | realized commit | landed as | declared-and-untagged for | discharged |
|---|---|---|---|---|
| `contract-v2.3` | `ec8be5aa62179713f37ee12dab53a948d791e147` | PR #514 merge, 2026-08-30 08:25 -0400 | about 19 hours — and it was CONSUMED as a spent number inside that window, by the `contract-v2.4` cut `afdf0e88` | tag `9fe9a742` published 2026-08-31 03:14 -0400 |
| `contract-v2.4` | `afdf0e88f329740150654d5ad67a1984a104e83b` | PR #526 squash, 2026-08-30 23:49 -0400 | about 3.5 hours | tag `3374ad2f` published 2026-08-31 03:14 -0400, in the same act |

`verify-tag --remote origin` passes for both and each peels to the commit named
above, which is *"the EARLIEST FIRST-PARENT COMMIT on published `main` that
DECLARES the bundle and at which `verify-commit` PASSES"*. RETRO-PUBLISHED, NOT
RE-DATED, on the same terms as the August discharge: no release was
reconstructed, re-cut or altered, and no version number was reused. **The
measurement of record is `contracts/CHANGELOG.md` § `contract-v2.4` tag
disposition — PUBLISHED 2026-08-31** (PR #532), which peels both tags, runs
`verify-commit` at both targets, and re-validates the targeting rule against a
live control (`contract-v2.2` → `8ccfb67b`, matching its already-published tag).
This table cites that measurement; it does not re-derive it, because two records
of one measurement is how they drift apart.

**THE DISCHARGE DOES NOT MAKE THE GAP ACCEPTABLE**, and the v2.3 case is the one
that shows why. For those nineteen hours *"a bundle is not published until its tag
exists"* was in force and unmet, and a later cut consumed the bundle as a spent
number anyway. That is evidence of the cost, never a precedent.

**WHY IT RECURRED, WHICH IS THE ONLY PART A FUTURE READER CAN ACT ON.** Nothing
in the estate checks this. `verify_tag` exists and is called only by unit tests
over synthetic repositories; no workflow calls the release validator at all;
`release-surface-integrity` deliberately does not anchor on tags; and
`tag-hygiene` is a different family entirely, over document prose markers. So the
gap is invisible until a human counts, which is exactly how it reached
`contract-v1.33`/`v1.35`/`v1.39` in August and then reached `contract-v2.3` and
`contract-v2.4` in the same week the August ruling was still being cited. **It is
filed as issue #528 and is OPEN.** Until a check lands, the sentence above can go
false a fourth time, and this section records rather than prevents that. A reader
finding it false again should add the gate, not another paragraph.

Every instance above is a breach of the rule, never an exception to it, and the
closing clause immediately below binds all six — the never-dischargeable sixth
most of all: no reader may cite this subsection, or the periods it narrates, to
treat an untagged bundle as released. **A bundle that can never be tagged is not
thereby released; it is permanently unreleased**, which is the whole content of
the `contract-v2.6` disposition below.

THE RULE WAS NEVER ADVISORY, INCLUDING WHILE IT WAS BEING BROKEN. For the weeks
these three went untagged, "a bundle is not published until its tag exists" was
in force and simply unmet: they were a breach of the rule, never an exception to
it, and their having been consumed anyway is evidence of the cost of the gap
rather than a precedent. No reader may cite this subsection, or the period it
narrates, to treat an untagged bundle as released.

RECORDS DESCRIBING THE FORMER GAP STAND AS HISTORY. `docs/archive-record-discrepancies.md`
(`Status: record`) states that `contract-v1.33` and `contract-v1.35` are not git
tags. That was true when written and is deliberately NOT edited: a record is
immutable, exactly as an archived change packet is, and rewriting one to match
today's state would destroy the evidence of what was true then.

### `contract-v2.6` — Instance Six: SPENT, NEVER VERIFIABLE, NEVER PUBLISHED, SUPERSEDED

**THE FIRST INSTANCE THAT IS NOT A LATE TAG BUT AN IMPOSSIBLE ONE.** The five
above were bundles whose tags nobody published; this is a bundle whose tag nobody
COULD publish. It is recorded in this document — and not only in the changelog —
because this policy is the artifact a consumer pins and reads, and a consumer who
reads the discharge tables above and stops would conclude that every allocated
number is either tagged or awaiting a tag. One is neither.

| bundle | declaring commit | disposition | authority |
|---|---|---|---|
| `contract-v2.6` | `bbbbeda984353ebaeb67d3e2bb1c73fcb7bac140` — the squash of PR **#565**, landed 2026-09-01 | **SPENT. Never verifiable, never published, SUPERSEDED by `contract-v3.0`.** No annotated tag exists or can exist; the number is never reused; the changelog entry and `contracts/releases/contract-v2.6.digests.yaml` are left exactly as written | Brett Heap, ruling in session 2026-09-02: *"Supersede: v3.0 is the completion."* Executed by the `contract-v3.0` cut, PR **#573**, squash `ff9ed815` |

**WHY NO TAG CAN REACH IT — TWO DEFECTS, AND THE SECOND IS THE ONE THAT SETTLES
IT.** The targeting rule this section established is *"the EARLIEST FIRST-PARENT
COMMIT on published `main` that DECLARES the bundle and at which `verify-commit`
PASSES."*

1. **NO COMMIT SATISFIES THE RULE.** Exactly one first-parent commit declares
   `contract-v2.6`, and `verify-commit` fails there with five
   `HGR-RELEASE-DIGEST-MISMATCH` findings — the cut branch forked at `518c670b`
   and was never rebased onto the final integration point, so a squash merge
   applied the PR diff onto a `main` that had moved under it (§ Bundle
   Realization Order **step 1**, omitted). Three of the five are NOT the
   editorial members § *What a red `verify-commit` at HEAD means* allows between
   cuts, and that allowance does not reach a tag in any case: *"a published
   bundle must verify at its own commit exactly."*
2. **AND A REBUILT INVENTORY WOULD NOT CURE IT.** `contract-v2.6` declares change
   class ADDITIVE (minor) on a tree that, from 2026-09-01T19:43Z, REFUSES three
   shapes `contract-v2.5` accepted. A minor asserts that consumers on the same
   major remain conformant without changes, and on that tree the assertion is
   false. A completion commit — the `contract-v1.31`/`-v1.36`/`-v1.37` shape that
   supplied a target for the earlier discharges — moves five digest lines and
   moves that not at all.

**THIS IS A SUPERSESSION, NOT A RETRO-PUBLICATION, and the distinction is the
whole record.** The 2026-08-25 and 2026-08-31 discharges published tags at the
commits their bundles were really realized at — RETRO-PUBLISHED, NOT RE-DATED. No
such act is available here. What discharges `contract-v2.6` instead is § Immutable
Tag Correction's remedy for a defective release, applied one step earlier in the
lifecycle: a superseding release carries the content forward under a number whose
class matches the tree, and *"its version number is never reused."* Everything
`contract-v2.6` was to have carried is carried at `contract-v3.0`.

**THE MEASUREMENT OF RECORD IS `contracts/CHANGELOG.md` § `contract-v3.0`, the
`contract-v2.6` disposition.** This table cites it and does not re-derive it,
because two records of one measurement is how they drift apart. The defect itself
is filed as issue **#574**; the raw measurement is PR #565 comment `5502452624`.

**WHAT THIS COSTS THE ESTATE, STATED PLAINLY RATHER THAN DISCOVERED.** The
`release-tag-publication` family reports `contract-v2.6` at **ERROR** —
*"cut and SUPERSEDED without ever being published"* — and **the finding will not
clear.** The family has no state between *published* and *owes a tag*, and the
action it prescribes is unperformable for this bundle for the two reasons above.
Publishing `contract-v3.0`'s tag did not clear it and could not: the family
inspects every bundle carrying a release inventory, not only the declared one.
**The finding is TRUE and the family is not wrong**, and it is deliberately NOT
weakened to fit this record — the owner's ruling supersedes a bundle, it does not
license a checker to stop objecting to abandoned ones, and a policy that relaxed
the one check standing between the estate and walked-away bundles would be
repeating the failure that check exists to catch. The missing vocabulary — what
record makes a bundle SPENT, who may declare it, at what severity, and the guard
that a bundle must never become spent merely by being ignored — is design work
owing its own change and its own review, filed as issue **#575**. **Until it
lands, this ERROR is a DECLARED permanent finding, not an undiscovered one**, and
no reader should quiet it by editing the manifest, the changelog or the inventory
to match the absence.

### Recovered Legacy Baseline

The historical `contract-v1.1` through `contract-v1.6` changelog entries were
created before tag enforcement and have no corresponding repository tags.
They are treated as an explicitly recovered, unpublished legacy sequence, and
`contract-v1.6` WAS the manifest baseline at the time of that recovery. (The
manifest baseline advances with every realized bundle and is whatever
`contracts/manifest.yaml` declares today; this sentence records the recovery,
not the current state.) The next realized contract change
allocates the next available minor version and begins mandatory annotated-tag
publication; historical tags MUST NOT be fabricated retroactively.

## Release Digest Inventory

The per-file digest identity (item 4 above) is realized as a canonical
release digest inventory at `contracts/releases/<bundle-tag>.digests.yaml`,
validated against `contracts/releases/release-digest-inventory.schema.yaml`.

- Every digest is the SHA-256 of the raw Git blob bytes at the release
  commit, encoded lowercase as `sha256:<64hex>`. Text canonicalization,
  checkout-filtered bytes, working-tree reads, symlinks, and submodule
  gitlinks are all invalid digest sources.
- Entries list unique repository-relative regular-file paths in bytewise
  UTF-8 order, each with an artifact ID, type, Git file mode, and optional
  schema ID and version.
- Membership is closed over the release surface: the Hermes runtime contract
  family, its indexed fixtures, the validators, the hash-locked requirements
  files, the PostgreSQL image lock, the inventory schema, the contracts
  manifest, changelog, and README, and every modified normative contract or
  versioning document. Missing, extra, duplicate, out-of-order, symlink,
  submodule, traversing, and host-absolute members all fail validation.
- The inventory excludes exactly itself and carries no commit field. Either
  would be circular; the annotated tag and the downstream compatibility
  manifest anchor the commit and the inventory digest instead.

`scripts/validate-contract-release.py` enforces this identity with four
subcommands: `build --tag <tag> --output <path>` writes a candidate
inventory from exact bytes; `verify-commit --commit <sha>` reproduces every
digest from the pinned commit's Git objects; `verify-promotion --commit
<sha> --remote <name> --tag <tag>` proves, before tagging, that the tag is
absent, the version is the next available, the reviewed candidate is
reachable from remote main, and no release-surface blob drifted; and
`verify-tag --remote <name> --tag <tag>` proves the published annotated tag
dereferences to the exact commit. Exit codes: 0 pass, 1 findings, 2
dependency/harness failure.

### What a red `verify-commit` at HEAD means

`verify-commit` resolves the inventory to check from `contract_bundle_version`
AT THE COMMIT, deliberately, so that historical inventories from earlier
releases are ignored. A consequence follows that every reader of a red result
needs, and that this policy did not previously state:

**Between cuts, `verify-commit` at `HEAD` is EXPECTED to report mismatches on
the editorial members** — `contracts/CHANGELOG.md`, `contracts/manifest.yaml`
and `contracts/README.md`. A change that touches no contract still records
itself in the changelog and may still update a consumption rule or a per-file
digest, and the declared bundle's inventory was written before those edits
existed. The next cut re-baselines the inventory as part of the realization
order. A red result confined to those three members is therefore a bounded,
expected state and NOT a defect.

A mismatch on any OTHER member is a defect: a normative contract's bytes moved
while the repository went on declaring a bundle that describes different bytes.

**THE REMEDY IS A RELEASE CUT, NEVER A HAND-EDIT.** An inventory is a record of
what a release contained; editing one so that a check passes destroys the only
evidence that the release surface moved, and converts a detectable defect into
an undetectable one. The same applies to the manifest's `contract_bundle_version`:
it is advanced by a cut, not adjusted to make a comparison succeed.

`verify-commit` at a TAG is a different question and has no such allowance:
a published bundle must verify at its own commit exactly.

## Bundle Realization Order

Contract-bundle realization is serialized and allocates versions late:

1. Fetch and rebase onto the final integration point, then immediately
   recheck bundle/tag availability and allocate the next available version.
2. Update every release surface — manifest, changelog, realized digest
   inventory — atomically with the contract files in one candidate commit.
3. Run every gate and independent review against that exact unchanged
   candidate commit.
4. Land the exact reviewed commit on published `origin/main`. If promotion
   creates a different commit, that commit becomes the new candidate and
   every gate and review reruns before tagging.
5. Publish the annotated tag pointing at the exact published commit and
   verify it from an independently refreshed checkout.

Release metadata rejects host-absolute paths, and the legacy
`local_source_path` field is removed only after a recorded
supported-consumer audit proves no supported consumer requires it.

## Immutable Tag Correction

A published annotated tag is immutable: it is never moved, deleted, or
re-tagged, not even for a defective release. A release found defective after
tagging is corrected by a superseding release — allocate the next available
version through the same realization order, record the defect and its
migration guidance in `contracts/CHANGELOG.md`, and let consumers upgrade by
pinning the new bundle. The defective tag and its digest inventory remain in
place as immutable provenance: nothing retroactively invalidates the
evidence of consumers that verified against it, and its version number is
never reused.

### contract-v1.36 Was Moved — a recorded breach, disposed of

`contract-v1.36` was published on 2026-08-21 at one commit and then deleted and
re-pushed to another, minutes later in the same session, to correct a cut whose
`contract_bundle_version` had been left at the previous release. That is a
breach of the rule immediately above, which forbids moving a published tag
**even for a defective release**. The tag today points at the corrected commit;
the superseded tag object and the reasoning are recorded in
`openspec/changes/add-release-inventory-drift-check/proposal.md` and in the
moving commit's own message.

**DISPOSITION — RECORD ONLY (Brett, 2026-08-24).** The breach stands recorded
and nothing further is owed.

TWO MOVES A LATER READER MUST NOT MAKE on discovering this:

1. **Do not move or re-point the tag again**, including to "restore" it to its
   original commit. A second move compounds the breach instead of repairing it,
   and the original commit does not carry a release that verifies.
2. **Do not cut a superseding release to "fix" it.** That is the sanctioned
   remedy for a DEFECTIVE RELEASE, and the release itself is not defective —
   it verifies at its tag. Spending a version number here would correct
   provenance that this record already carries accurately.

This subsection exists because the disposition would otherwise live only in a
change packet, which archives out of the path of anyone running `verify-tag`
and landing on the rule above (PR #319 review).

### The SPENT State — a Cut Number That Can Never Be Published

A bundle that was CUT and can NEVER be published is **SPENT**. It is a THIRD
state beside the two this policy otherwise knows, and the requirement that
checks it names the gap in those terms: *"Between published and owes a tag sits
a number that was cut, was never publishable, and never will be."* The remedy is
the one this section prescribes for a defective release, applied one step
earlier in the lifecycle — the content is carried forward under a superseding
number and the spent number is retired rather than repaired — and the sentence
governing the retirement is the same one: *"its version number is never
reused."* `contract-v2.6` is the estate's first instance and its record is
§ *`contract-v2.6` — Instance Six* above. **That section records the
supersession; this one DEFINES the state**, and neither restates the other.

**THE STATE IS ENTERED ONLY BY AN EXPLICIT DECLARATION, AND NEVER BY ANY
ABSENCE.** Silence is not a declaration, age is not a declaration, and a bundle
nobody got round to tagging is not spent — it owes a tag, and is reported as
owing one. The requirement states the fail-closed character without
qualification: *"A bundle MUST NOT become spent by being old, by being ignored,
by being inconvenient, or by any absence whatsoever."* An untagged superseded
bundle that no declaration names is reported exactly as it is today.

**THE DECLARATION LIVES IN `contracts/CHANGELOG.md`, INSIDE THE SUPERSEDING
BUNDLE'S OWN ENTRY, IN ONE RESERVED SINGLE-LINE FORM.** It is written into the
human disposition subsection the superseding cut writes anyway, so there is one
record and one place it can be read from. The form, whole, shown as a code block
so that no delimiter of the surrounding prose can be misread as part of it:

    **SPENT BUNDLE:** `<bundle>` — SUPERSEDED BY `<superseding bundle>` — CAUSE: <text> — RULED BY <author>, <YYYY-MM-DD> — MEASUREMENT: <citation>

Four elements are owed and each is checked for presence: the superseding bundle,
the cause, the ruling that disposed it — its author and its date — and the
measurement of record the cause cites. The opener is RESERVED, in the
requirement's own words: *"no other text in `contracts/CHANGELOG.md` may begin a
line with it, and a line beginning with it that does not complete the form is a
malformed declaration rather than prose to be ignored."* **AND A BUNDLE CANNOT
DECLARE ITSELF SPENT.** The declaring act is the LATER CUT that allocates the
replacement, so a declaration is accepted only inside the changelog entry of the
bundle it names as the superseding one — *"a bundle that could declare itself
spent could decline to be published"*, which is the state this rule refuses.

**THE SUPERSEDING BUNDLE MUST BE CUT, MUST BE PUBLISHED, AND MUST BE STRICTLY
LATER.** Cut and published, because *"the only way to retire a number is to
publish its replacement's tag"* — the obligation MOVES onto the successor rather
than being discharged by the declaration. Strictly later, because a guard
satisfied by an already-published EARLIER bundle would have been walked around
backwards rather than met: the superseding bundle's `(major, minor)` SHALL be
STRICTLY GREATER than the spent bundle's.

**WHAT THE REPORT SHOWS, AT THREE SEVERITIES AND NOT TWO.** The
`release-tag-publication` doc-health family reports an ACCEPTED declaration at
`info`, on the spent bundle's own `contracts/releases/<bundle>.digests.yaml` —
recorded rather than silent, because a reader who finds a release inventory with
no matching tag is owed the answer where they are looking. A PROVISIONAL
declaration — well formed in every element, its later successor CUT but NOT YET
PUBLISHED — is reported at `warning`, and is ONE finding rather than two, the
successor being graded on its own account. A REFUSED declaration is an `error`,
and the superseded-and-never-published `error` stands beside it, *"so that a bad
declaration removes nothing"*. The checking rule itself belongs to doc-health,
at `openspec/specs/doc-health/spec.md` § *Release-tag publication* and in
`docs/doc-health.md`; what belongs here is the obligation that family checks.

**AND WHAT IS OWED AFTERWARDS IS NOTHING.** The spent number is never reused.
`contracts/manifest.yaml`, the spent bundle's release inventory and its own
changelog entry are left EXACTLY AS WRITTEN — *"never edit the manifest, the
changelog or the inventory to match the absence"* — and the `info` is permanent.
It MUST NOT be read as the tag obligation having been MET: *"It was not met; it
was EXTINGUISHED, by an owner act, at the cost of a version number, and the
record says which."*

## Supported-Domain Regression Denominator

Publication is gated on a versioned regression inventory, never on an
implicit "all current domains" scan.
`contracts/hermes-runtime/fixtures/domain-regression-inventory.yaml` names
every supported DomainxFactory repository with an exact published commit,
`stack.yaml` path, raw-blob digest, and expected contract pin — currently
`opensoft/AdxFactory`, `opensoft/LedgerxFactory`, `opensoft/MedxFactory`,
`opensoft/OpsxFactory`, and `opensoft/codexFactory`, with
`opensoft/LegalxFactory` recorded as an explicit exclusion until it carries
a canonical `stack.yaml`. Before a bundle publishes, every inventoried pin
must revalidate from exact `commit:path` Git objects resolved through
deterministic mappings (`--domain-repo <canonical-repo>=<checkout>`, or
`--domain-repo-root` under which `owner/repo` resolves only to
`<root>/<owner>/<repo>` or `<root>/<owner>/<repo>.git`); missing objects are
dependency failures, not skips. The denominator is release evidence about
supported consumers; it does not invert the compatibility direction restated
below — openxFactory still never pins domain repos as a dependency.

## Change Classes

- **Additive (minor)** — new optional fields, new contracts, new validator
  warnings. Domain repos on the same major version remain conformant
  without changes.
- **Deprecating (minor)** — a field or shape is marked deprecated; the
  conformance validator emits warnings but still accepts it. Deprecations
  must state the removal version and a migration path in the CHANGELOG.
- **Breaking (major)** — a required field is added, a shape is removed, or
  role/vocabulary semantics change. Requires: a CHANGELOG migration note,
  at least one full minor release where the old shape produced deprecation
  warnings, and an update to the conformance validator that accepts the new
  shape and rejects the old one only at the new major version.

## Domain Upgrade Runbook

1. Read `contracts/CHANGELOG.md` between the pinned ref and the target ref.
2. Update `stack.yaml` `xfactory.contract_ref` (and `contract_schema_version`
   if major) to the exact target release commit, record the matching bundle
   tag, and update required per-file digests.
3. Run `openxFactory/scripts/validate-domain-factory.py <domain-repo> --strict`
   from the target checkout. Fix every error; triage every warning.
4. Record the upgrade in the domain repo (commit message referencing the
   contract tag), then update the tenant records that pin versions.

## Compatibility Direction (restated)

Compatibility flows from DomainxFactory to openxFactory. openxFactory never
pins domain repos. A domain repo remains valid against its pinned version
until it explicitly upgrades; nothing in a new openxFactory release may
retroactively invalidate an old pin.

## Deprecations Currently In Force

- **The `hermes` flat KEYS — the twelve, enumerated BY PATH, and the recorded
  reason the removal was NOT taken at contract-v3.0.** The fallback READ that
  resolved layer overlays and display names from these keys is gone; the keys
  themselves are not refused. **THE ENTRY IS WRITTEN FROM THE REFUSAL LIST**,
  because the shape a consumer must be able to check against its own bytes is
  the shape the removal would refuse, and this entry previously named five of
  the twelve:

  | key, under the `hermes:` block | previously named by the entry |
  | --- | --- |
  | `hermes.subject_overlay` | yes |
  | `hermes.subject_layer_name` | yes |
  | `hermes.customer_overlay` | yes |
  | `hermes.customer_layer_name` | no |
  | `hermes.client_overlay` | yes |
  | `hermes.client_layer_name` | no |
  | `hermes.care_organization_overlay` | yes |
  | `hermes.domain_overlay` | no |
  | `hermes.domain_layer_name` | no |
  | `hermes.domain_agent_mixes` | no |
  | `hermes.client_agent_mixes_template` | no |
  | `hermes.customer_agent_mixes_template` | no |

  **THE LIST IS BY PATH AND NOT BY NAME, AND THE DIFFERENCE IS LOAD-BEARING.**
  `omnigent.domain_overlay` is a LIVE, non-deprecated key that every supported
  consumer declares and that `scripts/validate-domain-factory.py` reads and
  errors on when the directory it names is missing. It is EXCLUDED from the list
  above. A refusal list written as bare key names would sweep it in and refuse,
  at a major and with no warning ever served, a shape the whole supported
  population legitimately carries. The deprecated key is `hermes.domain_overlay`
  and nothing else.

  Replaced by `hermes.layers`, whose role keys are `customer`/`client`/`domain`.
  THOSE KEYS ARE FROZEN MACHINE IDENTIFIERS, NOT THE CANONICAL VOCABULARY: the
  canonical Hermes layering has been Subject / Tenant / Domain since
  `adopt-subject-tenant-domain-vocabulary` was ratified 2026-07-23, and the
  machine keys survive unrenamed precisely so that pinned consumers keep
  validating. The mapping between them is
  `contracts/policies/layer-vocabulary.yaml`; interpret the keys through it and
  never rename them ad hoc.

  **THE RECORDED REASON THE REMOVAL WAS NOT TAKEN, AND IT IS A MEASUREMENT
  RATHER THAN A PREFERENCE.** The deprecation warning fired ONLY in the branch
  taken when `hermes.layers` was ABSENT. All five supported consumers —
  codexFactory, MedxFactory, AdxFactory, LedgerxFactory, OpsxFactory — declare
  `hermes.layers` AND carry flat keys alongside it, so that co-resident shape
  has never produced a warning against any of them: `python3
  scripts/validate-domain-factory.py <repo>` emits no legacy-flat-key line for
  any of the five, and the branch was dead code for the entire supported
  population. Refusing the keys would therefore be an UNPHASED narrowing — the
  Breaking class's "at least one full minor release where the old shape produced
  deprecation warnings" is unmet for the co-resident shape, and a warning that
  cannot fire is not a warning served.

  **THE DEPRECATING MINOR IT OWES**, stated so the successor is checkable rather
  than remembered: a minor in which the conformance validator warns on the
  co-resident shape *whether or not* `hermes.layers` is present, written from
  the full twelve-key refusal list above. Only after that minor has been cut and
  served may a major refuse these keys. A change that proposes refusing them
  without it is refused, and this paragraph is what makes the refusal citable.

  Migration, available now and unforced: delete the flat keys from `stack.yaml`;
  nothing reads them while `hermes.layers` is present, and no supported consumer
  is required to act before the deprecating minor lands.

  Warned since contract-v1.1; removal target RESTATED to contract-v4.0 — the
  co-resident shape has never been warned, so the removal is unphased and owes
  the deprecating minor named above first. If that minor has not been cut when
  contract-v4.0 is reached, this entry is RESTATED AGAIN rather than the removal
  taken unphased.
- **The undeclared `consumer:` block on a credential binding — and EIGHT acts
  that land together with it (`add-binding-consumer-identity`, extended by
  `add-consumer-identity-namespace`).** Each entry of
  `credential_bindings` in `xfactory_credential_binding_template` MAY declare a
  `consumer:` block naming the consuming system that holds the binding
  (`holder_ref`) and the identity that system authenticates to the secret store
  with (`fetch_identity`), optionally the issuing directory, account or tenant
  WITHIN the provider that minted that identity (`identity_namespace`),
  optionally a qualified `requirement_ref`
  (`requirement_id` + `requirements_document_ref`), and the const-true
  `shared_credential_acknowledged` and `instantiation_stub` tokens. **The block
  is DECLARED at contract-v2.4 and CONSTRAINED at contract-v4.0** — the target
  read `contract-v3.0` until that major was CUT without any of the eight acts
  and the entry was restated at that cut, per the tail of this bullet; from
  contract-v2.4 through contract-v3.0 the schema imposes no type, no member
  grammar, no requiredness and no closure on it, and
  `scripts/validate-credential-contracts.py` emits WARNINGS instead.

  **THIS ENTRY NAMES EVERY ACT THAT LANDS AT THAT MAJOR, because a reader
  learns from this entry alone that they are ONE act served by ONE deprecation
  window.** The entry is written from the REFUSAL LIST rather than from memory:
  every shape the current major accepts and the next one refuses owes its minor
  of warnings, and without that a reader at the major cannot demonstrate this
  section's own `:250-254` precondition was met and the requiredness becomes
  unauditable.

  **RECONCILED, NOT RESTATED: A FURTHER ACT LANDS AT THE SAME MAJOR AND IT IS
  NOT ONE OF THE EIGHT ABOVE.** `add-requirement-ref-resolution-integrity` declares
  that a `requirement_ref` resolving to zero requirements, or to more than one
  requirement of the document it names, is REFUSED at contract-v3.0 — a
  RESOLUTION fault rather than a SHAPE fault, carried by its own code family and
  its own entry, **the next entry in this section**. This paragraph exists
  because the completeness claim above would otherwise be FALSE, and an entry
  asserting completeness that is not complete is worse than one asserting
  nothing: a reader at the major uses it to demonstrate the deprecation
  precondition was met, and cannot tell an act that served its window from one
  that never had an entry. The claim now reads as scoped to the EIGHT SHAPE
  acts of the consumer block, with the further act named here and declared in
  full below.
  The two entries share ONE deprecation window and ONE major, so a consumer
  still upgrades once.

  | act, at contract-v4.0 (target restated from contract-v3.0) | the code that warns until then |
  | --- | --- |
  | a binding declares no `consumer:` block (requiredness) | `consumer-identity-undeclared` |
  | a block exists and omits `holder_ref` or `fetch_identity`, or is not an object | `consumer-block-incomplete` |
  | the block is CLOSED — an undeclared member is refused | `consumer-block-unknown-member` |
  | the member grammar — `holder_ref`, `fetch_identity` and `requirement_ref.requirement_id` carry identity-brokering's identifier pattern, and `requirement_ref` must be the qualified two-member object | `consumer-member-grammar` |
  | a const-true token declared `false` is refused | `consumer-token-not-true` |
  | the `credential_bindings` MAP KEY carries the identifier grammar | `consumer-binding-key-grammar` |
  | `access_mode` on `xfactory_credential_requirements` is closed to `{dispatch_only, contents_write, workload_identity, delegated_api}` | `consumer-access-mode-vocabulary` |
  | `requirements_document_ref` is repository-relative, non-escaping, non-foreign and YAML-suffixed | `consumer-requirement-ref-grammar` |
  | `identity_namespace` carries the same identifier pattern, and is a DECLARED member the block's closure does not refuse | `consumer-identity-namespace-grammar` |

  **THE NINTH ROW'S WINDOW OPENS AT ITS OWN MINOR AND NOT AT `contract-v2.4`,
  and the difference is the whole of what a deprecation window is.**
  `identity_namespace` did not exist before `add-consumer-identity-namespace`,
  so no release could have warned about a grammar on it and none did. Its window
  opens at the additive minor that DECLARES the member, and § Change Classes,
  *Breaking (major)* requires at least one FULL minor of warnings BEFORE the
  major that refuses — so if that minor turns out to be the last before
  `contract-v4.0`, this row waits for the one after rather than riding a window
  it did not serve. An entry warned and refused at the same bundle serves no
  window at all. Every other row above keeps `contract-v2.4` as its warned-since
  release; this one carries its own, and the two share the major without sharing
  the window.

  **IT IS A NINTH `consumer-*` CODE RATHER THAN A SECOND FAMILY — the opposite
  call from the entry below, made on the same rule.** The eight codes above are
  enumerated against refusals OF SHAPE, and an `identity_namespace` outside the
  identifier pattern IS one: a value that does not match a pattern, inside the
  declared member set, on the block. It carries its own code rather than joining
  `consumer-member-grammar` because its CONSEQUENCE differs — an unreadable
  namespace is SKIPPED by the shared-authority comparison, which then falls back
  to the bare fetch identity, so a reader told only that a member failed a
  grammar would repair a spelling while believing a scoping they declared is in
  force. Migration: none is owed by a record that declares no namespace, the
  member being optional at both releases; a record that declares one spells it
  in the identifier grammar, and declares it on BOTH bindings wherever two
  bindings name one fetch identity in two directories — a namespace on one side
  only falls back to the bare identity and still reports.

  Migration: declare `consumer: {holder_ref: …, fetch_identity: …}` on each
  binding; a record written before any install exists declares
  `consumer: {instantiation_stub: true}` instead, and **that TOKEN is the only
  exemption — a `*.template.yaml` filename exempts nothing**, because a filename
  is author-chosen, invisible in the bytes a pinned consumer validates, and
  unreachable by a pinned schema. Do NOT satisfy the field with a placeholder: a
  grammar-passing sentinel reads as an authority declaration while naming
  nothing. Every warning above carries a packaged probe under
  `examples/credential-contracts/warning/`, and the self-test refuses a code
  with no probe.

  **THE REQUIREDNESS IS GATED ON THE DEGRADED FETCH-IDENTITY MODE, AND SHALL
  NOT LAND WITHOUT IT.** At the major an install with no per-install fetch
  identity must write SOMETHING into a required field, and what it will write is
  the shared service identity, silently — precisely the grammar-passing
  placeholder this deprecation calls worse than omission, arriving through the
  front door of the field it adds. `contracts/avatar-client/broker-server-key-
  binding.template.yaml` already ships `degraded_mode_permitted: true` on this
  record kind, so the shape the successor is measured against exists. Until a
  degraded mode is declarable in this family, the OTHER seven acts may land and
  the requiredness may not.

  Nothing narrows at contract-v2.4, and that is a measurement rather
  than a claim: six shapes a domain could already hold — an object with neither
  declared member, a scalar, a list, placeholder-styled values, an undeclared
  extra member, and no block at all — were built and driven against the shipped
  schema, and all six validate. Every consumer pinned at the prior bundle stays
  conformant until it upgrades.

  **THE TARGET ARRIVED AND THE REMOVAL WAS NOT TAKEN — RESTATED AT
  `contract-v3.0`, WITH THE REASON.** `contract-v3.0` was CUT on 2026-09-02 —
  declared, not yet published, this section's own distinction, and the target
  arrives at the DECLARATION because that is when the removal would have had to
  be in the bytes — and **not one of the eight acts above landed** (the eight
  the table carried at that cut; a ninth was added afterwards by
  `add-consumer-identity-namespace` and carries a window of its own): `scripts/validate-credential-contracts.py`
  still emits all eight codes as WARNINGS, measured at that cut rather than
  assumed, and the schema still imposes no type, no member grammar, no
  requiredness and no closure on the block. **THE REASON IS THAT NOTHING
  AUTHORED IT, AND THAT IS SAID PLAINLY RATHER THAN DRESSED AS A DECISION**:
  no change proposed the constraining, no realization carried it, and the cut
  that reached the target had no ratified text to execute. This is NOT the
  flat-key case one entry above, where a measurement showed the removal would
  be unphased — the phasing here is intact and was served by `contract-v2.4`
  and every minor since, so a successor may take these acts at the restated
  major with **no new deprecation window owed**. The requiredness row alone
  carries its own separate precondition, unchanged and unmet: the degraded
  fetch-identity mode two paragraphs above, without which the OTHER SEVEN acts
  may land and the requiredness may not.

  Restated under § Deprecations Executed's own governing rule — a deprecation is
  EXECUTED at the major it targets, or its entry is RESTATED with the reason it
  stays — which `retire-hermes-flat-keys-and-openworkflow-tokens` promoted out
  of one entry's prose after three entries sat past `contract-v2.0` unexecuted
  and nothing said so. **A RESTATEMENT REFUSES NOBODY**: moving a removal target
  later can only widen what a major accepts, which is why the cut took it rather
  than leaving a spent target standing or, worse, executing eight unauthored
  acts to make a sentence true.

  Warned since contract-v2.4; removal target RESTATED to contract-v4.0 — the
  eight acts were not authored by the time `contract-v3.0` was cut, and an entry
  may not survive its own removal target unchanged. If they have still not
  landed when contract-v4.0 is reached, this entry is RESTATED AGAIN rather than
  the removal taken on text nobody wrote.
- **A `requirement_ref` that RESOLVES TO NOTHING, or to more than one requirement
  of the document it names (`add-requirement-ref-resolution-integrity`).**
  A `consumer.requirement_ref` on a credential binding is a
  QUALIFIED reference — `requirement_id` plus `requirements_document_ref` — and
  the entry above governs its SHAPE. This entry governs whether it ANSWERS. At
  contract-v4.0 a declared reference that resolves to ZERO requirements, or to
  MORE THAN ONE requirement OF THE ONE DOCUMENT IT NAMES, is REFUSED; until
  then `scripts/validate-credential-contracts.py` emits a WARNING and the
  record stays VALID. **THE TARGET READ `contract-v3.0` WHEN THIS ENTRY WAS
  WRITTEN AND IS RESTATED BY THE CUT THAT FILLED IN ITS `Warned since`, AND THE
  RESTATEMENT IS FORCED RATHER THAN CHOSEN**: these codes are PUBLISHED at
  `contract-v3.0`, so `contract-v3.0` is the release that first SERVES the
  warning, and § Change Classes, *Breaking (major)* requires *"at least one full
  minor release where the old shape produced deprecation warnings"* BEFORE the
  major that refuses. An entry warned and refused at the same bundle serves no
  window at all. The tail of this entry carries both versions.

  **IT IS A SECOND FAMILY AND NOT A NINTH `consumer-*` CODE, and the reason is
  the entry above's own enumeration rule.** Those eight codes are enumerated
  against REFUSALS OF SHAPE — a block that is missing, incomplete,
  closed-and-violated, ungrammatical, or carrying a token declared false. A
  reference that resolves to nothing is none of those: it is well-formed,
  inside the declared member set, grammatical in both members, and WRONG ABOUT
  THE WORLD. Filing it under a grammar code would make that code untrue in the
  other direction — a code meaning "this value does not match the pattern"
  would come to carry a record whose values match every pattern this family
  declares.

  | act, at contract-v4.0 (target restated from contract-v3.0 by the publishing cut) | the code that warns until then |
  | --- | --- |
  | a declared `requirement_ref` matches NO requirement record in the repository under validation | `requirement-ref-unresolved` |
  | a declared `requirement_ref` matches MORE THAN ONE requirement record of the ONE DOCUMENT IT NAMES | `requirement-ref-ambiguous` |

  **ZERO AND MORE-THAN-ONE ARE NAMED APART BECAUSE THEIR REMEDIES ARE IN
  DIFFERENT FILES**, and a reader told only "the reference did not resolve" has
  no way to know which file to open. Migration for
  `requirement-ref-unresolved`: repair the REFERENCE — the id is misspelled,
  the document moved, or the requirement was never written. Migration for
  `requirement-ref-ambiguous`: repair the REQUIREMENTS DOCUMENT THE REFERENCE
  NAMES, by making the ids that document declares unique; this is the more
  dangerous of the two, because nothing stops one document declaring one id
  twice and the matches may differ in `access_mode`. An implementation MUST NOT
  resolve the ambiguity by picking one. A binding that declares NO
  `requirement_ref` draws nothing from either code — the member is OPTIONAL at
  this release, and an omission is a different question from a wrong answer.

  **REPORTED PER BINDING, WHATEVER THE BINDING SHARES — which is the whole of
  the act.** Before this change the resolution was performed in exactly ONE
  place, the six-condition lift, reached only for a PAIR of bindings sharing a
  `secret_ref`, so a dangling reference on a binding whose secret was its own
  passed in silence. A sharing pair now keeps BOTH duties: the lift stays
  UNAVAILABLE and the `shared-secret-identity` refusal stands exactly as it
  does today, AND the reference is reported on the binding that declares it.
  The two answer different questions and are not one fault named twice.

  **THE AMBIGUITY IS PER-DOCUMENT, AND THE WIDER ARM IS FILED RATHER THAN
  CLAIMED.** `resolve_requirement` matches inside the one document a reference
  names, over an index keyed by document path, so the same requirement id
  declared in TWO schema-valid requirements documents resolves cleanly from a
  reference naming either and draws NOTHING from `requirement-ref-ambiguous`.
  That gap is INHERITED from the shipped validator rather than introduced here;
  it was ruled out of scope at this minor by Brett Heap on 2026-09-01 and is
  filed as **openxFactory issue #553**, which also carries the promoted
  scenario that already reaches across documents. If that arm is ever taken it
  lands as its OWN condition under this entry's own-family rule, never as a
  silent widening of `requirement-ref-ambiguous`.

  Nothing narrows at the minor that declares these codes, and that is a
  MEASUREMENT rather than a claim: a binding template declaring two bindings
  with DISTINCT secret references, one naming a requirement id no record
  carries and one naming an id TWO RECORDS OF THE ONE DOCUMENT IT NAMES carry
  with DIFFERENT access modes, validated with zero errors and zero warnings
  under the shipped validator — measured against
  `scripts/validate-credential-contracts.py` before the arm landed, and
  re-measured after, where the same tree reports both warnings and still
  returns `PASS`. Both codes carry a packaged probe under
  `examples/credential-contracts/warning/`, and the self-test refuses a code
  with no probe; the SILENT direction carries its own positive,
  `examples/credential-contracts/resolving-requirement-ref.binding-template.example.yaml`,
  because a corpus holding only the failing direction cannot tell a working
  check from one that fires on everything.

  **THE `Warned since` VERSION WAS DELIBERATELY UNWRITTEN HERE AND OWED BY THE
  CUT THAT PUBLISHES THESE CODES**, not by the realization that implements them:
  the bundle number is allocated by MERGE ORDER, `contracts/manifest.yaml` has
  had several writers, and a number written in advance is a number another
  packet is already spending. **THAT CUT IS `contract-v3.0` AND IT FILLS IT IN
  HERE.** The class is DEPRECATING (MINOR), which owes the removal version and
  the migration path in `contracts/CHANGELOG.md` rather than leaving them
  optional; both are stated above. An entry naming a warning release that was
  never cut would be the same defect as an entry claiming a completeness it does
  not have.

  **AND FILLING IT IN IS WHAT MOVED THE REMOVAL TARGET, WHICH THE ENTRY COULD
  NOT KNOW WHEN IT WAS WRITTEN.** It read *"Removal target contract-v3.0 — the
  SAME major the consumer block's seven acts land at, so a consumer serves ONE
  deprecation window rather than two."* The publishing cut turned out to BE
  `contract-v3.0` — the codes landed on `main` at `e01561c5` some ninety minutes
  after that cut's branch point and hours before its merge — so warning and
  refusal would have fallen on one bundle. The ONE-WINDOW property is preserved
  by moving BOTH entries together rather than by abandoning it: the consumer
  block's acts are restated to `contract-v4.0` above (none of them was authored
  by the time `contract-v3.0` was cut), and these two are restated to
  `contract-v4.0` here, so a consumer still serves ONE window and still upgrades
  once — one bundle later than either entry expected, and with the window
  actually served rather than merely declared.

  Warned since contract-v3.0; removal target RESTATED to contract-v4.0 — the
  publishing cut and the declared removal target collided on one bundle, and a
  warning that is first served at the bundle that refuses is not a window.

## Deprecations Executed

A deprecation leaves the list above when the removal it announced actually
lands. It is recorded HERE rather than deleted, because a consumer upgrading across
the removal needs the migration path to still be readable at the version it is
upgrading TO — and because a deprecation silently disappearing from a policy document
is indistinguishable from one that was never honoured.

- The eight openxWallet contracts (`openxwallet-record`,
  `openxwallet-custody-registry-schema`, `openxwallet-custody-registry`,
  `openxwallet-grant`, `openxwallet-grant-exercise`,
  `openxwallet-distinct-holder-constraint`, `openxwallet-subject-attestation`,
  and `openxwallet-agent-composition`) — **REMOVED at contract-v2.0**, the full
  minor of deprecation warnings having been served by contract-v1.47 as
  § Change Classes, *Breaking (major)* requires. Their canonical home is
  `opensoft/openXwallet` at tag `wallet-v1.1`.
  openxFactory now CONSUMES the family: `contracts/openxwallet-pin.yaml` pins the
  publisher by 40-hex COMMIT plus eight per-file `sha256` digests (the tag is a
  label beside them, never the referent) and records the NAMED CARVE COMMIT the
  digests were taken at; `scripts/verify-openxwallet-pin.py` checks it and fails
  closed with a named refusal code and a fixed remediation trailer. **The
  conformance-validator clause of § Change Classes, *Breaking (major)* is
  discharged by the move itself**: from contract-v2.0
  forward this family's conformance validator IS the pinned
  `openXwallet/scripts/validate-openxwallet.py` at the commit the pin records, run
  over openxFactory's own tree as the REQUIRED `wallet-validation` check. Migration:
  `contracts/CHANGELOG.md` § `contract-v2.0` and
  `openXwallet/docs/pin-resync-runbook.md`. Deprecated at contract-v1.47, removed at
  contract-v2.0.
- **The `openworkflow`-prefixed layer/owner token compatibility branch** — the
  branch in the canonical domain-factory conformance validator that gave any
  workflow-gate `owner_layer` whose normalized form BEGINS `openworkflow` its
  own deprecated-naming warning, together with the validator docstring line
  that advertised it. **REMOVED at contract-v3.0.** From that major such a token
  carries NO special handling and is evaluated by the same rule as any other
  `owner_layer` token.

  **THE SHAPE IS ENUMERATED AS THE CODE MATCHED IT, WHICH IS ONE CHARACTER
  WIDER THAN THIS ENTRY USED TO DECLARE.** The In Force entry and the validator
  docstring both wrote `openworkflow_`, with a trailing underscore; the code
  wrote `token.startswith("openworkflow")`, with none. So `openworkflow`,
  `openworkflowx` and `openworkflow-legacy` all took the branch and are all
  covered by this removal, and not one of them was the shape the entry declared.
  The correction is made here rather than carried forward, under the rule that a
  deprecation entry is written from the REFUSAL LIST.

  **IT NARROWS ONE CASE AND WIDENS ANOTHER, AND BOTH ARE RECORDED.** The removed
  branch was an `if` that PRECEDED the general `elif token not in allowed`, so
  it shadowed it. (1) NARROWING — a token carrying the prefix that resolves to
  no canonical role and no declared layer was WARNED and is now reported by the
  general undeclared-layer rule, at whatever severity that rule carries.
  (2) WIDENING — a token carrying the prefix whose normalized form EQUALS a
  declared Hermes layer's normalized display name was also warned, because the
  branch shadowed the general rule, and now validates SILENTLY. Both were
  measured on the two validators side by side before this row was written. No
  such gate exists in any reachable repository; the widening is recorded because
  it is real, not because it bites.

  The full minor of deprecation warnings required by § Change Classes,
  *Breaking (major)* was served by **contract-v1.1**, which introduced the
  replacement token and began warning on the prefix — forty-plus minors of
  warnings, and the refused shape is exactly the warned shape. **The
  conformance-validator clause of that section is discharged in the validator
  itself**: `scripts/validate-domain-factory.py` accepts the new shape — a
  canonical role, a declared layer's display name, `omnigent`,
  `<domain>_omnigent`, or `xfactory` — and rejects the old one only from
  contract-v3.0, through the general rule; a consumer pinned below the major
  reads the branch at its own pin, where it is still present and still warns.
  Migration: replace the token with `xfactory`, the replacement introduced by
  `contract-v1.1` (`contracts/CHANGELOG.md` § `contract-v1.1`); a
  post-removal reader recovers the original shape from this row and the
  migration target from that entry. Deprecated at contract-v1.1, removed at
  contract-v3.0.
- **The `hermes` flat-key FALLBACK READ — the READ, and not the keys** — the
  branch of the canonical domain-factory conformance validator that resolved
  layer overlays and display names from flat keys under `hermes:` when
  `hermes.layers` was absent, together with the `LEGACY_HERMES_KEYS` map it read
  them through, the per-role `no overlay resolvable for hermes role` check that
  followed it, and the domain-starter generator's emission of the deprecated
  keys into every newly instantiated domain repository. **REMOVED at
  contract-v3.0.**

  **THIS ROW IS SCOPED TO THE READ. THE KEYS ARE NOT REFUSED** and their entry
  stays in § Deprecations Currently In Force above, restated to contract-v4.0
  with the measurement behind it. An entry sitting in both sections would be a
  defect; these are two different shapes, and only one of them was removed.

  The full minor of deprecation warnings required by § Change Classes,
  *Breaking (major)* was served by **contract-v1.1**, which introduced
  `hermes.layers` and began warning on a stack that declared none. The refused
  shape is exactly the warned shape: the warning fired on a `hermes.layers`-less
  stack and nothing else, and a `hermes.layers`-less stack is precisely what is
  now refused. It refuses nobody — all five supported DomainxFactory consumers
  declare `hermes.layers`, verified by running the validator against each of
  them before and after the removal with no line moved.

  **The conformance-validator clause of that section is discharged by a
  REPLACEMENT and not by a deletion, and the distinction is the whole of it.**
  The `hermes.layers missing required role` errors sit INSIDE the branch taken
  when `hermes.layers` IS declared. Deleting the fallback arm alone would have
  left a `layers`-less stack falling through to an EMPTY layer map and producing
  no finding at all — a silent WIDENING at a major, the exact opposite of the
  retirement. In its place the validator emits ONE explicit error naming the
  missing or non-list `hermes.layers`, so the old shape is rejected, only at the
  new major, and visibly. Migration: declare `hermes.layers` with exactly one
  template for each canonical role `customer`, `client` and `domain`, each
  carrying `display_name` and `overlay` — the shape
  `contracts/schemas/xfactory-domain-stack.schema.yaml` requires and the
  domain-starter generator now emits alone. Deprecated at contract-v1.1, removed
  at contract-v3.0.
- **The doxBench chat-turn v1 envelope family** — `workbench-chat-turn`,
  `workbench-chat-turn-success` and `workbench-chat-turn-failure`, defined as
  `$defs/request`, `$defs/success` and `$defs/failure` in
  `contracts/schemas/xfactory-workbench-chat-turn.schema.yaml`, together with
  their three top-level `oneOf` refs, the file's machine-readable
  `deprecated_envelopes` block, the three kind→schema rows and three
  tag-dispatch arms in `scripts/validate-ideation-dashboard-contracts.py`, the
  v1 arm of `serve.py`'s kind discrimination, four positive and eight negative
  packaged fixtures, and the byte-identity baseline test that existed to prove
  the deprecated bytes never moved. **REMOVED at contract-v3.0.** The file's own
  `contract_schema_version` deliberately STAYS `1`: the envelopes this file no
  longer defines cannot be validated against it at all, so there is no shape
  left for a bumped integer to describe, and what changed is which release a
  consumer pins. The break is carried by the bundle version, by the per-file
  `sha256` a consumer verifies, and by this row — the realization pinned that
  decision in a test with its reasoning beside it, and the cut kept it.

  **THE ROW IS SCOPED TO THE THREE ENVELOPES AND THEIR OWN MACHINERY. FIVE
  SHARED `$defs` DID NOT LEAVE WITH THEM** — `content_hash`, `confined_path`,
  `scope_key`, `buffer_state` and `transcript_turn` — because the surviving
  family's measured reference closure reaches every one of them. A sixth,
  `typed_proposal`, is RETAINED AND UNREFERENCED: the closure computation put it
  OUTSIDE the surviving family (`keyed_typed_proposal` restates the shape with a
  buffer-key target rather than `$ref`-ing it), so the ratified text's premise
  that it is reachable is false, and removing it here would have been a
  narrowing no entry announced and no minor warned on. The measurement and that
  disposition are recorded at the definition's own site.

  The full minor of deprecation warnings required by § Change Classes,
  *Breaking (major)* was served by **contract-v1.34**, which introduced the
  co-resident widened `-v2` family and declared the v1 deprecation
  MACHINE-READABLY in the file's own `deprecated_envelopes` block. Unlike the
  two rows above, **these warnings were still firing at the removal and the
  count is on the record**: `python3 scripts/validate-ideation-dashboard-contracts.py`
  reported `0 error(s), 4 warning(s)` on `main` at `af746459`, one per packaged
  v1 fixture, and reports `0 error(s), 0 warning(s)` at contract-v3.0 — because
  their subjects are gone, not because the reader that emitted them was removed.
  The refused shape is exactly the warned shape: the warning named the three v1
  kinds and nothing else, and those three kinds are precisely what is now
  refused.

  **The conformance-validator clause of that section is discharged by the
  schema and the delegated validator together, and the deprecation READER is
  deliberately KEPT.** The new shape — a `workbench-chat-turn-v2` request and
  its two response envelopes — is accepted unchanged; the old one is refused
  only from contract-v3.0, by the closed `oneOf` that no longer admits it. The
  validator's general `deprecated_envelopes` reader survives with not one line
  of logic changed and now reports `{}`, which is the correct report and not a
  defect: deleting the estate's only machine-readable deprecation reader because
  its sole current subject had gone would have left the NEXT deprecation inert,
  which is the precise failure this whole retirement exists to correct.
  **A REFUSAL IS NOT SILENCE HERE**: `serve.py`'s v1 arm was REPLACED rather
  than deleted, so an unrecognized or absent `kind` — a retired v1 kind
  included — is answered in the surviving family's failure envelope carrying
  `unrecognized_turn_kind` (400) where a wire-valid `client_turn_id` exists, and
  in the pre-identity shape where it does not.
  Migration: send `workbench-chat-turn-v2` — `kind` replaced,
  `active_document_path` dropped in favour of the DECLARED `bound_buffer` key,
  `observed_hashes` keyed by buffer key, and `keyed_typed_proposal` in place of
  `typed_proposal` on the success envelope; the full note is
  `contracts/CHANGELOG.md` § `contract-v3.0`, and all SEVEN v1-only refusal
  classes are re-expressed as packaged `-v2` negatives, none lost. A consumer
  pinned below the major keeps the v1 bytes its pin names, by the immutability
  of those bytes rather than by their continued presence here. Deprecated at
  contract-v1.34, removed at contract-v3.0.

  **THE ENTRY NAMED contract-v2.0 AS ITS REMOVAL TARGET AND SURVIVED IT
  UNCHANGED FOR FIVE MINORS**, which is why openxFactory issue **#522** exists
  and why `contract-deprecation-execution` now requires an entry reaching its
  target to be executed or restated. This row is the first execution taken under
  that rule; the restatements taken beside it are in § Deprecations Currently In
  Force above.
