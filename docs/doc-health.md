# xFactory Doc-Health Contract

Status: standard
Kind: process
Repository context: openxFactory
Backed by: [openspec/specs/doc-health/spec.md](../openspec/specs/doc-health/spec.md) (promoted from the archived add-doc-health-contract change)
Purpose: define the deterministic health-check contract for the factory
family's governance corpus — the check families, the report and ranked-plan
schema, finding severities, aging thresholds, and the ownership split.

Companion contracts: [Document Lifecycle](document-lifecycle.md) (the states,
taxonomy, and `xspec:` marker grammar the checks enforce) and
[Lifecycle Notebook Projection](lifecycle-notebook-projection.md) (whose
sync dry-run is one of the drift checks).

## Scope

This contract covers the **deterministic pass only**: same inputs, same
findings, no model calls. The agentic/semantic sweep (untagged normative
prose, prose-vs-spec contradiction) is a separate active change
(`openspec/changes/add-doc-health-semantic-sweep/`). Implementation lives in
this repository (`scripts/doc_health/`, adopted from codexFactory by
`adopt-neutral-tooling-home`); the nightly runner is hosted by the xFactory
aggregation repo; this document and the `doc-health` spec own the contract.

## Check Families

Every run executes twenty-three families over every family repo the aggregation
repo pins, after running each repo's own validators as a preflight. A
family that cannot run is reported as skipped, never silently omitted.

**The table below is knowingly incomplete.** It carries the original twelve
plus the eighteenth, `promotion-fidelity`, whose spec delta is one of the
deltas that raised the count above. Families 13 through 17, and the
nineteenth through twenty-third (`release-inventory-drift`,
`duplicate-packet`, `family-enumeration`, `modified-block-currency`,
`release-tag-publication`), each
reached the `doc-health` spec by delta and never reached this table — which
is also why the two paragraphs after it still describe families 13 and 14,
and the notes further below describe families 20 through 23, by the
changes that added them rather than by a table row. Repairing that backlog
belongs to a change that owns those families; it is a named standing gap,
recorded in the archived `add-promotion-fidelity-check` §5.2, not an
oversight here.

| # | Family | What it verifies |
| --- | --- | --- |
| 1 | Status validity | Every governance doc carries a `Status:` header, and carries one drawn from the controlled taxonomy — a missing header and a free-form value are separate `error` findings, because they name different repairs. One of the four families that read the declared lifecycle scan set as well as the governed corpus |
| 2 | Standard backing | Every `Status: standard` header carries a `Backed by:` line, in the lifecycle header, whose target resolves — an existing local path, or any `http(s)` URL taken on trust, neither one opened to confirm it IS a promoted spec or canonical contract — `critical` where nothing resolves at all. The deterministic arm reads the HEADER; the prose half of `document-lifecycle`'s status-claim rule is not what this family measures. One of the four families that read the declared lifecycle scan set as well as the governed corpus |
| 3 | Ratified provenance | Five arms across both sanctioned citation spellings, each `critical`: a `ratified` header carrying more than one citation line, counted as one total across the two spellings; a `Ratified by:` naming no existing active or archived change and resolving to no path — except a citation naming `openxFactory` itself, accepted outright as cross-repo provenance a run with no `openxFactory` checkout in scope (a single-repo run) cannot verify; a record-citing `Ratified:` naming none of an approver, a date, or a resolvable record path; a `ratified` header carrying no citation in either spelling; and a `review/` record whose SUBJECT is a ratification while its status is not `ratified`. A LAST PASS then downgrades to `info`, quoting the citation, any finding whose family/repo/path carries a dated, cited entry in the aggregation's `health/dispositions.yaml` AND whose path is under `openspec/changes/archive/` — a downgrade rather than a suppression, because an archived record is beyond the plain repair every other arm asks for. One of the four families that read the declared lifecycle scan set as well as the governed corpus |
| 4 | Succession integrity | `superseded` docs carry a `Superseded by:` line whose target resolves — the same existing-path-or-`http(s)`-URL test as standard backing above, never a check that the target IS the successor; `retired` docs carry a `Retired:` or `Reason:` line — the prefix's bare presence, an empty line after it still passes — each an `error`. One of the four families that read the declared lifecycle scan set as well as the governed corpus |
| 5 | Location conformance | Lifecycle locations (a `brainstorm` doc outside `ideation/brainstorm/`; a `staged` doc outside `ideation/` that is not a candidate register); staged material whose own exit-statement line — one of `Proposed by:`, `Proposal:`, `Exit:`, `Exits via:`, or a stated exit inside a recognized Exit heading, never a bare dependency or evidence citation — names an ACTIVE proposal, the move being the remedy; active proposal support without a valid `manifest.yaml`, carrying `staged` status below it (`source-snapshots/` excepted BY PATH ALONE — not itself confirmed listed or hash-matched there, though a separate arm checksums whatever the manifest's own file list does name), or disagreeing with its manifest's per-file checksums; archived support missing its readable manifest or its bundle, failing the bundle checksum, or disagreeing with the member inventory the manifest records; and no historical bundle under `openspec/specs/`. Every arm `error` |
| 6 | Record immutability | `record` docs unchanged after capture (link fixes excepted) |
| 7 | Staged/candidate aging | Staged topics, open candidate blocks, `xspec:supersedes` markers still without `change=`, and draft ages against the thresholds below, plus one `info` draft-age distribution per repo that carries at least one `draft` — a repo with none gets no such finding. A staged topic carrying a RECORDED OUTCOME does not age at all — its primary fragment `superseded` or `retired`, or an `Exit taken:` line in that fragment or in the repository's staging INDEX naming a change that has ARCHIVED; a citation of an ACTIVE change silences nothing, that topic's staged material being the move another family is already reporting |
| 8 | Register-lifecycle consistency | Every `DTN-` row of the candidate register carries at least six cells — more are accepted, not enforced away — and a status from the documented alias set — each an `error` — and an `adopted` entry points at an artifact that resolves — the same bare existing-path-or-`http(s)`-URL test, not a check that the target IS the promoted artifact (`warning`) |
| 9 | Tag hygiene | Live `xspec:` markers obey the canonical grammar — as defined by [Document Lifecycle](document-lifecycle.md#prose-tagging-markers), which owns every syntactic detail; this contract never restates it |
| 10 | Submodule pin drift | Aggregation-repo gitlink pins vs each submodule's remote main — `warning` where they differ, and `info` naming the pin whose remote could not be read, so a pin that was not checked is never reported as a clean one |
| 11 | Contract-copy drift | Each pinned consumer's `stack.yaml` `contract_ref:` — a 40-character commit hex only; a tag-form pin is invisible to this family — against openxFactory's own HEAD — `warning` where the declared pin differs at all, a plain inequality that a lag, a lead, and an unrelated commit trip alike. What it compares is the DECLARED PIN; the token-set comparison of the copies themselves is this family generalized, and it belongs to the neutrality-drift lane below |
| 12 | Notebook projection drift | The lifecycle notebook sync dry-run reports zero add/update/delete operations |
| 18 | Promotion fidelity | Every archived spec delta reached the promoted spec it was ratified to reach — the requirement title, every scenario stated under it, a ratified removal actually removed, and, for an `ADDED` or `MODIFIED` writer only (the `REMOVED` branch returns before this check and is never subject to it), a target capability carrying a promoted spec to reach at all. The most recent archived delta is the authority, a later `RENAMED` writer legitimately retires the earlier title and is checked no further, and only a packet whose own `proposal.md` declares `draft` or a lower standing is exempt, and so is a writer whose `(repo, path)` or `(repo, path, title)` carries a cited `health/dispositions.yaml` entry — read here too, and skipped before any comparison runs; a `--single-repo` run has no aggregation root to read one from at all. Findings are `error`, classified `contested`, and reported against the archived delta's own path |

**Rows re-derived at** `8015d45fdf68` (2026-09-11, issue #967). Every row above
states its family's arms as `scripts/doc_health/` and the promoted
[`doc-health` spec](../openspec/specs/doc-health/spec.md) carry them at that commit —
except row 7's RECORDED OUTCOME exemption, whose textual authority is
`openspec/changes/settle-aging-staging-topics/`, `Status: ratified` but still active,
not yet archived into the promoted spec —
rather than the one arm several of them were first summarised by; rows 6, 9 and 12
already did and are unchanged. This refreshes no ROSTER — the table stays knowingly
incomplete for the reason given above — and a later sweep refreshes this line with the
commit it measured at.

The archived `add-document-cataloging` change added a thirteenth
deterministic family, `document-catalog`, plus a separate, non-deterministic
`document-cataloger` worker lane that never participates in this pass; see
its
[doc-health spec delta](../openspec/changes/archive/2026-07-14-add-document-cataloging/specs/doc-health/spec.md)
for the owned check scope. Its table registration never landed — see the
disclosure paragraph above — and any catalog classification stays
descriptive discovery metadata — never lifecycle, ownership, or approval
authority (see
[Document Lifecycle](document-lifecycle.md#catalog-tags-are-not-lifecycle-state)).

A second archived change, `add-cross-factory-ideation-routing`, added a
fourteenth deterministic family, `ideation-routing` (sequenced after
`add-document-cataloging`, per that change's own tasks), covering routing
schema and controlled-vocabulary conformance, central Idea-ID and Claim-ID
allocation and uniqueness, legal routing/claim transitions, destination-owner
acceptance, structured repository/path/revision reference resolution, and
routing aging; see its
[doc-health spec delta](../openspec/changes/archive/2026-08-06-add-cross-factory-ideation-routing/specs/doc-health/spec.md)
for the owned check scope. Its table registration never landed either, and
routing metadata stays descriptive coordination — never lifecycle,
ownership, or approval authority (see
[Document Lifecycle](document-lifecycle.md#cross-factory-ideation-routing)).

The archived
[`2026-08-25-add-duplicate-packet-check`](../openspec/changes/archive/2026-08-25-add-duplicate-packet-check/specs/doc-health/spec.md)
change added a twentieth deterministic family, `duplicate-packet`, comparing
every repository's archived spec deltas against each other for the same
ruling recorded twice, per the canon `Requirement: One ruling, one discharge,
across archived packets` in
[`openspec/specs/doc-health/spec.md`](../openspec/specs/doc-health/spec.md).

The archived
[`2026-08-27-add-family-enumeration-check`](../openspec/changes/archive/2026-08-27-add-family-enumeration-check/specs/doc-health/spec.md)
change added a twenty-first deterministic family, `family-enumeration`,
verifying this very section's family count and roster against the code
registry rather than trusting either on prose alone, per the canon
`Requirement: The family enumeration is derived, not restated on trust` in
[`openspec/specs/doc-health/spec.md`](../openspec/specs/doc-health/spec.md).

The archived
[`2026-08-27-add-modified-block-currency-check`](../openspec/changes/archive/2026-08-27-add-modified-block-currency-check/specs/doc-health/spec.md)
change added a twenty-second deterministic family, `modified-block-currency`
(launched ADVISORY; the gate-bearing scenario-title arm flipped to `error`
and the family joined `FAMILY_RESOLUTION` on 2026-08-31, issue #357, once the
measured population read zero), comparing an active change's `MODIFIED
Requirements` blocks against the promoted requirements they replace across
three arms plus a marker-defect class, per the canon `Requirement: Currency
of an active change's MODIFIED requirement blocks` in
[`openspec/specs/doc-health/spec.md`](../openspec/specs/doc-health/spec.md);
the archived
[`2026-08-28-add-unclassified-finding-class`](../openspec/changes/archive/2026-08-28-add-unclassified-finding-class/specs/doc-health/spec.md)
change then added a fifth `unplaced` class for findings its own arms/
marker-defect map cannot place, per the canon `Requirement: A
modified-block-currency finding its own class map cannot place is itself a
finding`. The archived
[`2026-09-02-govern-sibling-added-modified-deltas`](../openspec/changes/archive/2026-09-02-govern-sibling-added-modified-deltas/proposal.md)
change adds a SIXTH and a SEVENTH class, both `warning` at launch and both
inserted BEFORE `unplaced` so that the gate-bearing arm still reads first and
the drift class still reads last: `sibling-pairing`, which evaluates the
PAIRING — never the carriage — of a MODIFIED block whose title only an active
sibling's `ADDED` (or a rename's `TO:` half) supplies, in four reported states
(self-referential, undeclared, misdeclared, undisclosed) and silent on a
correctly declared pair, per the canon `Requirement: A MODIFIED block over an
active sibling's addition is evaluated for its pairing, not for its carriage`;
and `added-over-canon`, the archive-ordering backstop, which reports an active
`## ADDED Requirements` block — or an active rename's `TO:` title — naming a
requirement the promoted specification ALREADY carries, per the canon
`Requirement: An active block writing a title the promoted specification
already carries is reported`. The three comparison arms still do NOT run
against a pending block: the pairing class reads a delta's own markers and the
set of active additions, and compares no requirement text at all. The declaring
marker is `document-lifecycle`'s third reserved form,
``**Modified over `<basis change-id>`'s addition by <change-id>
(<YYYY-MM-DD>):**`` followed by ` — <reason>`, which names no units and is
therefore never a suppression, never a marker defect and never a carriage unit.
Issue #627 then generalized the ordering arm from a pair to a chain: where
three or more active ratified changes carry a MODIFIED block for one
requirement, their declarations resolve the order whenever they state a single
linear chain — one starting point, no fork and no cycle — and every later block
is then measured against its predecessor's block rather than against canon,
while a group whose declarations state no such chain is still reported and now
names the defect (`forked`, `unanchored`, `cycle`, or a declaration anchored on
a writer outside the ratified group).

[`2026-09-01-add-release-tag-publication-check`](../openspec/changes/archive/2026-09-01-add-release-tag-publication-check/proposal.md)
added a twenty-third deterministic family, `release-tag-publication`, per the
canon `Requirement: Release-tag publication`. It asks the one question
`docs/contract-versioning-policy.md` states absolutely and nothing checked —
"a bundle is not published until its tag exists" — for every repository in
scope declaring a bundle at or above the `contract-v1.7` enforcement line:
does that bundle have a PUBLISHED ANNOTATED tag, and does it peel to a commit
that declares the bundle? It is DISTANCE-GRADED in first-parent landings on
published `main` (silent while the declaring commit is still the tip, since
the owner's tag act legitimately follows the cut; `warning` after that;
`error` past **five**, ruled 2026-08-31), and it splits an ABSENT tag from a
MISPLACED one — a tag on a non-declaring commit satisfies every check that
asks only whether a tag exists, and is what consumers pin. Its action line:
*publish the annotated tag at the commit the versioning policy's rule
identifies — the earliest first-parent commit on published main that declares
the bundle and at which verify-commit passes — never edit the manifest, the
changelog or the inventory to match the absence*. The gap it closes reached
`contract-v1.33`/`v1.35`/`v1.39` in August and recurred on `contract-v2.3`
and `contract-v2.4`; a human found it both times (issue #528). Because it reads at the PUBLISHED tip, the family first asks whether that commit is in the local object store and FETCHES exactly it — bounded, at the distance window's depth, and `--depth` only where the clone is already shallow — before it will read a missing `contracts/manifest.yaml` as anything at all: a tip it holds that carries no manifest is answered as *no bundle declared*, and only a tip it could neither find nor fetch keeps the fail-closed *could not be read at the published tip* skip (issue #612, which had nine governed repositories reported in the second sentence's words every nightly while the first was true).

The archived
[`2026-09-03-declare-spent-bundle-state`](../openspec/changes/archive/2026-09-03-declare-spent-bundle-state/proposal.md)
change gave that family a **THIRD STATE — SPENT** (ratified 2026-09-02, realized
PR #587 squash `3fa222f3`, archived 2026-09-03, issue #575),
between *published* and *owes a tag*. It adds **no family** and moves no family
count. A bundle that was cut, superseded, and can never carry a legal tag —
`contract-v2.6` is the first and so far only instance in this estate — may be
declared spent by ONE reserved single-line form in `contracts/CHANGELOG.md` at
the published tip, written inside the changelog entry of the bundle that
superseded it:

    **SPENT BUNDLE:** `<bundle>` — SUPERSEDED BY `<superseding bundle>` — CAUSE: <text> — RULED BY <author>, <YYYY-MM-DD> — MEASUREMENT: <citation>

**Silence is never a declaration.** An untagged superseded bundle that no
declaration names is reported exactly as before, at `error` and in the same
words; a bundle never becomes spent by being old, ignored, or inconvenient.
There are **three outcomes and the middle one is not a refusal**. ACCEPTED —
every element present, the line inside its superseding bundle's own entry, and
that bundle itself cut, itself carrying a published annotated tag on a declaring
commit, and **strictly later** — emits exactly one `info`, classed `contested`,
on the spent bundle's OWN release inventory
(`contracts/releases/<bundle>.digests.yaml`, never the manifest and never the
changelog, because a finding's identity is family + repo + path). PROVISIONAL —
well formed, successor cut but not yet published — emits one `warning` and
suppresses the superseded `error`, the successor being graded on its own account.
REFUSED — successor never cut, successor not later, an element missing, two
declarations naming one bundle, a declaration outside its successor's entry, or
one naming the bundle the manifest still declares — is an `error` that accepts
nothing, and the superseded `error` stands alongside it so a bad declaration
removes nothing. A declaration whose SUBJECT was never cut disposes nothing and
is a `warning` on `contracts/CHANGELOG.md`, the one finding of this state with no
per-bundle inventory to land on. Its action line for the accepted state: *no
action, and this is NOT the tag obligation having been met — it was
EXTINGUISHED, by an owner act, at the cost of a version number*. **The successor
guard is what makes the state unabusable**: the only way to retire a number is to
publish its replacement's tag, which is the act this family exists to compel. The
state reaches the ABSENT-tag arm and nothing else — it never quiets a MISPLACED
tag, a LIGHTWEIGHT ref, or the distance grading of the bundle the manifest
currently declares — and it is not read backwards onto the five bundles the
versioning policy records under § *Untagged Bundles After Enforcement Began*, all
of which were publishable and were published.

**What "inside the entry" means, since containment is the guard the state leans
on hardest.** An entry runs from its `## <bundle>` heading to the next
STRUCTURAL BOUNDARY, and every boundary closes it while only a `##` heading
whose first token is a COMPLETE bundle name opens one — so a declaration under a
non-release section, under a level-one heading, under an empty or Setext
heading, or under `## contract-v3.0.1` sits inside NO entry and is REFUSED
rather than inheriting the previous release's authority. Level THREE and deeper
do not close (this repository's own reserved line lives inside a
``### `contract-v2.6` disposition`` subsection of the `contract-v3.0` entry),
and up to three leading spaces are a heading while four is an indented code
block. **Fenced blocks are opaque** — to headings and to the reserved opener
alike — so the form may be DOCUMENTED inside a fence without being PERFORMED,
which is fail-closed in both directions: an example cannot spend a bundle, and a
declaration hidden in a fence does not count, leaving the superseded `error`
standing. Over-closing is the safe error and under-closing is not, which is what
picks each of these readings.

**Raw HTML is not read at all — it is REFUSED, and a fence is the only opaque
region.** The family reads `contracts/CHANGELOG.md` as CommonMark PROSE and
models no HTML block, so a raw-HTML block opener outside a fence (any of
CommonMark's seven start conditions, at up to three leading spaces) produces one
`contested` `error` naming the line, and NO SPENT declaration below that line is
read — declarations above it stand, and any bundle a declaration below it would
have quieted goes on being reported. A construct this reader cannot parse must
never be able to quiet a finding, whatever a renderer makes of the lines below
it; the repair is to remove the HTML or to move the declaration above it. An
opener shown as an EXAMPLE inside a fence is not an opener.

## Finding Severities

| Severity | Meaning | Examples |
| --- | --- | --- |
| `critical` | Governance integrity broken | Unbacked `standard` claim; dangling provenance; `record` mutation |
| `error` | Contract violation | Malformed/unresolved marker; free-form status; aging past escalation; a ratified spec delta that never reached its promoted spec |
| `warning` | Drift or first-stage aging | Pin drift; copy drift; projection drift; 30-day staged item |
| `info` | Inventory, metrics, and RECORDED STATES | Canon share; per-stage counts; age distributions; a bundle declared SPENT, which is recorded rather than silent because a reader who finds a release inventory with no matching tag is owed the answer in the report (ruled 2026-09-02) |

**Regression rule:** any `critical` or `error` finding not present in the
previous report (matched by family + path) opens one issue per run in the
aggregation repo listing all new findings. Persistent findings do not
re-open issues. A headline-metric decline is trend data, not a regression.

**Identity check (issue #342):** a report is stamped with the repo(s) the
run covered (`Repo-Identity:` header line); `--previous-report` REFUSES a
stamped baseline whose identity does not cover this run's scope, with a
nonzero exit — otherwise every finding key misses by construction and a
benign path/scope slip reports as mass regressions and uncited-resolution
errors. A baseline written before this stamp existed is still accepted
(with a warning), so the check phases in without breaking an in-flight
nightly.

## Aging Threshold Defaults

| What ages | Warning | Error |
| --- | --- | --- |
| Staged topic untouched | 30 days | 90 days |
| `xspec:candidate` block untouched | 30 days | 90 days |
| `xspec:supersedes` without `change=` | 14 days | 45 days |
| `draft` doc without transition | 60 days | — (age always reported as `info`) |

Defaults are contract surface so reports stay comparable; a run using
non-default thresholds or scope must say so in its report.

## Report Contract

Each run commits a dated Markdown report at `health/reports/YYYY-MM-DD.md`
in the xFactory aggregation repo, carrying `Status: record` +
`Kind: report`, plus a `Repo-Identity:` line naming the repo(s) the run
covered (generated evidence, per the lifecycle taxonomy; see "Identity
check" above). Contents:

- **Headline metric** — canon share by words: ratified + standard +
  promoted spec words over total governance words.
- **Per-stage counts** and age distributions.
- **Per-family finding sections** for every family the run executed.
- **The promotion fidelity measurement basis**, stated in that family's own
  section on every run and whether or not it found anything: the pinned
  checkout by default — the same tree every other family measures — or each
  repository's own live `main` where the run is configured for it, naming
  any repository whose live `main` could not be read and was measured from
  its checkout instead.
- **Ranked plan** — every finding as a ready-to-stage work item stating
  severity, repo, path, and suggested action, so report output feeds the
  ideation pipeline's input.

Plain Markdown is v1 by decision (diffable, greppable, zero infrastructure,
flows into the notebook projection); the plan-item shape is
machine-parseable so a later dashboard consumes the same files.

## Ownership

```text
openxFactory      owns the CONTRACT (this document, the doc-health spec,
                  the report schema) AND the IMPLEMENTATION: checker
                  scripts, report generator, reusable workflow
xFactory (root)   HOSTS the nightly runner and health/reports/ (the only
                  repo pinning every submodule)
each domain repo  owns APPROVAL of its own content: the pipeline reports
                  and stages, it never approves or merges
```

Changes to check families, schema, severities, or thresholds are OpenSpec
deltas to the `doc-health` capability here; the implementation follows.

Proposal-support integrity is part of location conformance rather than a
thirteenth family. It reports staged documents that already cite a proposal,
active support folders without valid manifests, `staged` status below an
active proposal, unverifiable archived bundles, and bundles misplaced below
`openspec/specs/`.

## Neutrality-Drift Lane

Ratified by `add-neutrality-drift-lane` (2026-08-04) as a MODIFIED
`doc-health` requirement: a nightly, incremental, model-driven lane beside
the deterministic families — the standing scout for domain-factory content
that belongs in openxFactory. Families/lanes overview row:

| Lane | Scope | Stage 1 (deterministic) | Stage 2 (model) | Output |
| --- | --- | --- | --- | --- |
| `neutrality-drift` | pinned `xFactories/*` domain repos only (never openxFactory, openAvatar, or installs in v1) | near-duplicate of a neutral artifact (token-set similarity, `contract-copy-drift` generalized), zero domain-lexicon hits in a schema/script (lexicon from the repo's own identity + ontology), cross-repo consumers, stack.yaml-uninventoried `scripts/` tooling | bounded batch of new/changed survivors judged under `scripts/doc_health/neutrality-prompt.md` ("would another domain need this essentially unchanged?") | drafted DTN-register seed (row + detail section, the register's own format) + ranked-plan items |

**Approval flow** (nothing moves automatically — ever): candidates land in
the rolling health PR as drafted register-seed text (persisted under
`health/neutrality-drift/seeds/` in this repo) plus contested WARNING
ranked-plan items. Brett's approval of a seed is his merge of the register
addition; movement then follows the
[Domain-To-Neutral Promotion Process](domain-to-neutral-promotion-process.md)
(staged topic → OpenSpec change → tranche moves), never the nightly. The
lane's write surface is exactly its own `health/neutrality-drift/` tree
(state, baseline markers, drafted seeds) plus the dated report — it never
edits a domain repo, the register, or any contract.

**Dispositions keying**: a rejected candidate gets an entry in the
aggregation repo's existing `health/dispositions.yaml` — the same
vocabulary every contested resolution uses, extended for this lane with a
content digest — keyed `family: neutrality-drift`, `repo`, `path`,
`content_sha256`, plus the required `cite`. Suppression holds while the
content is unchanged; a changed digest re-files the candidate.

**Incremental state**: `health/neutrality-drift/state.yaml` records each
repo's last-run commit and judged content digests;
`health/neutrality-drift/baseline/<repo>.yaml` is the recorded baseline
marker for a completed full sweep (codexFactory's cites the 2026-08-03
manual sweep). The reusable nightly exposes `neutrality-drift` (opt-out,
default on) and `neutrality-baseline` (manual full-sweep repo) inputs; with
no omnigent worker host the lane records a skip note and stage-1 counts
only, never an error.

## Related Documents

- [Document Lifecycle](document-lifecycle.md) — states, taxonomy, marker
  grammar.
- [Lifecycle Notebook Projection](lifecycle-notebook-projection.md) —
  drift-check target and report distribution surface.
- [Domain Neutralization Candidate Register](domain-neutralization-candidate-register.md)
  — register the consistency family checks.
- Implementation history is retained with the archived doc-health OpenSpec
  changes and their supporting-document manifests.
