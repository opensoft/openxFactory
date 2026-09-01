# Tasks: add-clearing-dispatch-boundary

The order matters and is not editorial. This packet ratifies FIRST; the
xFactory workflow merges SECOND; the operator's console act comes THIRD,
because an allowlist entry naming a workflow path that does not yet exist on
`main` is an entry nobody can verify; the neutral contract bytes land LAST,
at their own additive cut. Ratification authorizes realization and does not
perform it.

## 1. Spec delta (THIS CHANGE)

- [x] 1.1 `clearing-dispatch-boundary` — TEN ADDED requirements: the single
      door with its convergence model and grandfather enumeration; the sealed
      bounded request and its ten declared fields; API-side verification with
      the verifiable/policy-checked field split; the one sanctioned producer
      exit with the re-seal; hosted validation of returned output; the closed
      permitted-operations register; `readiness-diagnostic` as entry #1;
      route retirement; the authoring-time conformance guard; and the
      dispatch ledger with the periodic single-door attestation and its
      declared residual.
- [x] 1.2 `OPENSPEC_TELEMETRY=0 openspec validate add-clearing-dispatch-boundary --strict`
      and `--all --strict` both green.
- [x] 1.3 Listed in the openxFactory README "OpenSpec Records" block.
- [ ] 1.4 No `contracts/` file is created by this change. Confirm at review:
      `git diff --stat` against `main` touches only
      `openspec/changes/add-clearing-dispatch-boundary/` and `README.md`.

## 2. Ratification gate

- [x] 2.1 **DONE 2026-09-01** — Brett ratified, in-session, on the recorded
      word *"merge #192 and ratify #555"* (ratified head `15b14bb3`; record
      `review/ratification-2026-09-01.md`). Brett ratifies proposal, design, and the spec delta, ruling or
      carrying the four open questions: **OQ1** when a signature becomes
      required for field 10 (recommendation: at the first cross-organization
      producer, expressed against `trust-anchor`'s certificate record);
      **OQ2** ledger record versus transparency-log entry (recommendation:
      own record kind, referencing a chain); **OQ3** where the grandfather
      enumeration lives — NO LONGER OPEN: SETTLED AT REALIZATION and carried
      for confirmation only, as the governed data file
      `.github/clearing/grandfather-enumeration.yaml` in `opensoft/xFactory`
      read by BOTH the L4 guard and the L5 attestation, each member carrying
      group attribution and allowlist-entry status, with the neutral contract
      requiring only that such an enumeration exist, be closed, carry those
      two fields, and shrink (design OQ3 keeps the question's history and its
      rejected candidates); **OQ4**
      attestation cadence and finding surface (recommendation: ride the
      existing nightly lane, emit a doc-health-shaped finding).
- [ ] 2.2 Record the rulings as a Ratification section in `proposal.md`, set
      `Status: ratified` with the ratifying commit named, and state that the
      change stays ACTIVE until the declared code surface is merged with
      green evidence and the contract cut exists.
- [ ] 2.3 **RATIFICATION IS GATED ON THE ORIGIN RECORD BEING MERGED.** The
      record has been written and pushed to `opensoft/xFactory` at the
      repository root as `cpc-clearing-boundary-ruling-2026-09-01.md`, as
      `opensoft/xFactory#192` (https://github.com/opensoft/xFactory/pull/192),
      via a pull request on branch `record/cpc-clearing-boundary-ruling`
      (head `5b6a9fdf`) — **MERGED 2026-09-01T11:47:21Z at
      `faee7a96ae6e06c15b6c2122947c62356e96f71d`.** Confirmed: the merge
      landed the same day as, and on the same recorded word as, this
      packet's own ratification (§2.1). THE REASON IS NOT
      BOOKKEEPING: requirements 1–7 trace to that record's text, while
      requirements 8–10 EXTEND it and trace to its APPEND-ONLY ADDENDUM
      capturing Brett's same-session instruction "fold 1-5 in and fan out".
      Until the record is on `main`, a reader cannot open the provenance of
      three of the ten requirements, and this packet would be asking for
      ratification of extensions on the strength of its own account of them.
- [ ] 2.4 **RATIFY THE THREE EXTENSIONS AS EXTENSIONS.** Requirements 8, 9 and
      10 are not encodings of the written ruling (proposal "Why" carries the
      per-requirement split): requirement 9, the authoring-time conformance
      guard, is WHOLLY ABSENT from the record and is the largest of the three;
      requirement 8 generalizes the single retirement the record names;
      requirement 10 adds the periodic attestation to the dispatch recording
      the record does state. Ratification should say so, so the record shows
      three requirements approved as NEW POLICY rather than as fidelity to a
      ruling that did not contain them.

## 3. The xFactory realization — authored IN PARALLEL with this packet

The realization PR against `opensoft/xFactory` is being authored beside this
one, against the fixed interface constants below. They are interface, not
suggestion: the workflow path is what the operator admits to the allowlist in
§4, and a rename after that act costs a second console act.

| constant | value |
|---|---|
| clearing workflow | `opensoft/xFactory` → `.github/workflows/clearing-dispatch.yml` |
| operation id | `readiness-diagnostic` |
| coding lane | group `xfactory-execution-lane-workers`, dispatch label `host-coding-cpc-brett01`, runner `xfactory-coding-cpc-brett01` |
| artifact lane | group `xfactory-artifact-workers`, dispatch label `host-rider-cpc-brett01`, runner `xfactory-artifact-cpc-brett01` |

- [ ] 3.1 `clearing-dispatch.yml` — the clearing lane, with BOTH host jobs
      declared PHYSICALLY IN THIS FILE (requirement 1 / design D2; no
      reusable-workflow indirection for a host job, ever), the group a
      literal and the label permitted to be an input expression (design D7),
      and the `readiness-diagnostic` operation as its only permitted
      operation at landing.
- [ ] 3.2 In the SAME pull request, DELETE
      `.github/workflows/runner-readiness-diagnostic.yml`
      (`opensoft/xFactory#188`, merged `4fffb6e5`, 2026-09-01). Its checks move into the operation verbatim in
      substance; the route-retirement requirement forbids landing the
      operation and leaving the workflow. It was never allowlisted and must
      never be.
- [ ] 3.3 The L4 conformance guard plus its test: STRUCTURAL resolution of
      `jobs.<id>.runs-on.group` over every workflow file, refusing any
      non-clearing, non-enumerated file that declares a governed group,
      refusing an unresolvable group expression, and — the case the estate
      already contains — NOT flagging the `concurrency: group:
      xfactory-artifact-worker` declarations in `doc-health-nightly.yml` and
      `review-lane.yml`, which differ from the runner group's name by one
      character. Wired as a REQUIRED check.
      **THE APPEND REFUSAL, and what it is worth.** The guard reads the
      enumeration from the data file in 3.4; its TEST holds the NINE FOUNDING
      NAMES as a frozen ORIGIN constant and asserts the data file's members
      are a SUBSET of that origin set — so a RETIREMENT (which only shrinks)
      passes and an ADDITION turns the suite red. Do NOT describe this as an
      unforgeable refusal in the guard, the test, or the pull request: the
      data file, the guard and the test share a repository with the changes
      they police, so one diff can edit both sides. What the mechanism
      guarantees is that an append cannot be SILENT — it is a red check plus a
      diff touching the enumeration or the guard — and REVIEW OF THAT DIFF is
      the declared backstop.
- [ ] 3.4 **THE GRANDFATHER ENUMERATION AS A GOVERNED DATA FILE** —
      `.github/clearing/grandfather-enumeration.yaml` in `opensoft/xFactory`,
      per §2.1 OQ3 (settled at realization). NOT a constant inside the
      guard's test module: the L5 attestation is a SECOND CONSUMER, and two
      copies of the closed set is the failure mode a closed set exists to
      prevent. Both the authoring-time guard (3.3) and the future L5
      attestation (§7.1) READ THIS FILE. Marked append-never in the file
      itself. **Each member declares FOUR fields**: the workflow filename;
      the GOVERNED RUNNER GROUP it targets; the governed-host JOB IDS it
      declares in that file; and its ALLOWLIST-ENTRY STATUS, `present` or
      `absent`. The last two are not bookkeeping — without the group the
      attestation cannot compute one group's expected set, and without the
      status a dark lane reads as a breach.
      **Seed it with exactly the NINE existing host-touching worker
      workflows, with the group and status MEASURED 2026-09-01 rather than
      assumed:**

      | member | group | allowlist entry |
      |---|---|---|
      | `execution-lane-coding-worker.yml` | `xfactory-execution-lane-workers` (7) | `present` |
      | `council-deliberation-worker.yml` | `xfactory-artifact-workers` (5) | `present` |
      | `dashboard-image-worker.yml` | `xfactory-artifact-workers` (5) | `present` |
      | `doc-health-analysis-worker.yml` | `xfactory-artifact-workers` (5) | `present` |
      | `doc-health-cataloger-worker.yml` | `xfactory-artifact-workers` (5) | `present` |
      | `doc-health-derive-possibles-worker.yml` | `xfactory-artifact-workers` (5) | `present` |
      | `doc-health-readiness-worker.yml` | `xfactory-artifact-workers` (5) | `present` |
      | `review-lane-worker.yml` | `xfactory-artifact-workers` (5) | **`absent`** |
      | `ideation-organizer-worker.yml` | `xfactory-artifact-workers` (5) | **`absent`** |

      Group 7 allowlists exactly ONE path
      (`execution-lane-coding-worker.yml`); group 5 allowlists exactly SIX
      (the six marked `present` above). The two `absent` members are the DARK
      LANES — they declare a group 5 job and hold no entry, so they already
      fail closed with nothing reporting it, and §8.3 carries their
      disposition. Re-measure before committing the seed rather than trusting
      this table.
- [ ] 3.5 The dispatch record written by the clearing lane — verified
      provenance plus claimed-where-different, refusals included. Shape
      follows §2.1 OQ2; until the neutral schema lands (§6) the record is
      written in the shape the ratified requirement describes and re-pointed
      at the schema when it exists. **THE R10 LEDGER FIELDS THE REALIZATION
      EMITS, verbatim on names** (`opensoft/xFactory#191`), so the neutral
      schema in §6.4 is authored against what actually exists:

      | field | value |
      |---|---|
      | `clearing.dispatch.group.<lane>=` | the lane's DECLARED runner group |
      | `clearing.dispatch.label.<lane>=` | the lane's DECLARED dispatch label |
      | `clearing.dispatch.handling=` | for a BUNDLE-LESS operation, the register entry's DECLARED data-handling class |
      | `clearing.dispatch.outcome=` | appended by `operation-report` |

      All three `dispatch.*` values are DECLARATIONS OF THE DISPATCH, not
      observations of the host — the provider exposes no runner-group context
      to a job, and observed group membership is what §7.1's attestation
      establishes. **REFUSAL GROUNDS ARE A CLOSED, NAMED ENUMERATION**,
      seeded now with exactly two: `unregistered_operation` and
      `unknown_lane_selector`. A new ground is a governed change (§6.4), not
      a new string in a workflow.
- [ ] 3.6 Merge gated on §2 — the workflow does not land before the packet
      that authorizes it.
- [ ] 3.7 **THE INTERIM REGISTER IS A WORKFLOW EDIT SURFACE, and saying so is
      the point of this item.** Until §6.2's
      `contracts/clearing/permitted-operations.registry.yaml` exists, the
      closed register has NO instance to validate against, so it is realized
      as the clearing workflow's own CLOSED CHOICE LIST for the operation
      input plus the guard's constant. That is EXACTLY the
      operation-set-extended-by-workflow-edit surface requirement 6
      ultimately forbids: in the interim, adding an operation is a YAML edit
      reviewed as workflow configuration, which is the condition the closed
      register exists to end. It is accepted only because the interim set has
      ONE member and the successor is scheduled. **Therefore: once §6.2
      lands, the clearing workflow MUST validate the dispatched operation id
      against the registry INSTANCE and stop relying on its own choice list
      as the authority.** Do not let the interim outlive §6.2 by treating a
      green workflow as a satisfied requirement 6.

## 4. The operator's acts — ONE console act per group, and one closure

- [x] 4.1 **DONE 2026-09-01** — verified against the provider API: `record
      review/readiness-evidence-2026-09-01.md` §1. Add
      `opensoft/xFactory/.github/workflows/clearing-dispatch.yml@refs/heads/main`
      to `selected_workflows` of group `xfactory-artifact-workers` (id 5) and
      group `xfactory-execution-lane-workers` (id 7). **ONE entry per group,
      once, ever** — this is the permanent entry the allowlist converges to.
      Perform AFTER §3 merges to `main`, so the path being admitted exists.
      **UNTIL THIS ACT LANDS, REQUIREMENT 1'S CONVERGENCE SCENARIO READS
      FALSE BY CONSTRUCTION** — the allowlist cannot contain a path the
      operator has not admitted — and that is the NOT-YET-CONVERGED state,
      NOT a single-door breach. The first §7.1 attestation run must not be
      misread as a finding on this account: it reports the absent clearing
      path as convergence not yet reached, and only an allowlist entry the
      expected set does not derive is a widening.
- [ ] 4.2 Do NOT add `runner-readiness-diagnostic.yml` to either group. This
      is Brett's option-1 ruling of 2026-09-01 and the reason the readiness
      test became an operation. Recorded as a task so a future operator does
      not "fix" a queued readiness run by adding the entry.
- [x] 4.3 **DONE 2026-09-01** — `opensoft/codexFactory` removed from group
      `xfactory-artifact-workers`'s repository admissions, verified against
      the provider API: `record review/readiness-evidence-2026-09-01.md` §1.
      **CLOSE THE RESIDUAL THE RULING NAMES.** Group
      `xfactory-artifact-workers` (id 5) currently admits TWO repositories —
      `opensoft/xFactory` AND `opensoft/codexFactory` (measured against the
      provider API 2026-09-01). The ruling holds runner-group access to
      xFactory only. Remove the codexFactory admission. It is why run
      `33381257642` could queue at all, and with the allowlist restricting
      workflow paths to xFactory files, no codexFactory job can be claimed
      through it today — so the removal takes nothing away that works. Group
      7 already admits xFactory alone; nothing to do there.
- [x] 4.4 **DONE 2026-09-01** — re-read and filed: both groups now admit
      `opensoft/xFactory` alone — zero widenings, the first green
      single-door reading. Filed as the §7 attestation baseline in `record
      review/readiness-evidence-2026-09-01.md` §1. Re-read both groups from
      the provider API after 4.1 and 4.3 and
      file the reading as the baseline the §7 attestation compares against.
- [x] 4.5 **DONE 2026-09-01** — new `opensoft/xFactory` ruleset `22015321`
      `"required-checks-main"` (active, default branch, required check
      `validate` pinned to the GitHub Actions integration `15368`), verified
      against the provider API: `record
      review/readiness-evidence-2026-09-01.md` §1. **CREATE THE REQUIRED
      STATUS CHECK THE L4 GUARD NEEDS TO BE A
      GATE.** Requirement 9 obliges a REQUIRED check, and the clearing
      repository has none: measured 2026-09-01, NONE of `opensoft/xFactory`'s
      five active rulesets declares `required_status_checks` — Tier-1 main
      protection (`18962101`) carries `pull_request`, `non_fast_forward`,
      `deletion`; "Require Code Owner Review" (`18834180`) and
      `merge-master-stale-approval-dismissal` (`19887057`) carry
      `pull_request`; "Copilot Auto-Review All PRs" (`8981805`) carries
      `copilot_code_review`; the bot-confinement ruleset (`19874574`) carries
      push rules only. So the guard as merged is a check that RUNS and GATES
      NOTHING. Add a `required_status_checks` rule on `opensoft/xFactory`
      `main` naming the `validate` check (the job the guard's test runs
      under). **RECORD THE RESIDUAL WITH IT**: ruleset `18962101`'s
      `bypass_actors` list is `OrganizationAdmin` with `bypass_mode:
      always`, so even a required check is OPERATOR-BYPASSABLE. That is the
      same residual class as the unversioned console — L4 buys authoring-time
      visibility, not an unbypassable gate — and the packet says so rather
      than presenting a required check as one.
- [ ] 4.6 **CLEAN UP THE MISLEADING RUNNER LABELS.** Both
      `xfactory-coding-cpc-brett01` (group 7) and
      `xfactory-artifact-cpc-brett01` (group 5) carry `artifact-only` and
      `rider` — neither label discriminates the lanes in either direction
      (measured 2026-09-01; `record review/readiness-evidence-2026-09-01.md`
      §2 Gap 3). The 2026-09-01 clearing dispatch confirmed group/label
      routing landed correctly on both lanes despite the stray labels, so
      this is not a live routing breach — but the labels remain a hazard on
      any future dispatch that requests `artifact-only` by name. An operator
      label-cleanup item: remove or correct `artifact-only`/`rider` on both
      runners, investigating both rather than "fixing" the coding host alone.
- [ ] 4.7 **DECIDE THE SAME-HOST TOPOLOGY.** The 2026-09-01 clearing dispatch
      found both lane runners reporting the same `hostname` /
      `COMPUTERNAME` / `compute.node` (`CPC-brett-TUBV0`,
      `NUMBER_OF_PROCESSORS=8`) — the coding and artifact lanes are two
      services (separate installs, separate service accounts
      `svc-omnicoder` / `svc-omniworker`) on ONE Cloud PC, not two machines
      (`record review/readiness-evidence-2026-09-01.md` §3). Lane isolation
      as provisioned today is service-account isolation, not machine
      isolation, and plausibly explains 4.6's copy-pasted labels. Operator
      decision owed: single-host-by-design, or an interim state pending a
      second host — and if interim, when the second host lands.

## 5. Dispatch readiness on both lanes, and file the evidence

**THE REPORT CARRIER, settled with `opensoft/xFactory#191`.** The lane jobs
do not each write a report. Each lane job FORWARDS its probed facts as JOB
OUTPUTS, and a downstream `operation-report` job COMPOSES the single
STRUCTURED OPERATION REPORT of record from them and appends
`clearing.dispatch.outcome=`. The evidence-filing steps below therefore
harvest the COMPOSED report — read it from the `operation-report` job's run
summary and log, not from the individual lane jobs — and §6.3's
`operation-report.schema.yaml` describes THAT composed artifact.

- [x] 5.1 **DONE 2026-09-01** — opensoft/xFactory run `33512287539`
      (https://github.com/opensoft/xFactory/actions/runs/33512287539),
      `lane=both`, dispatch ledger id `cd-33512287539-1`; composed report
      filed in `record review/readiness-evidence-2026-09-01.md`. Dispatch
      `readiness-diagnostic` through the clearing lane on the
      CODING lane (`xfactory-execution-lane-workers` /
      `host-coding-cpc-brett01`). File the COMPOSED structured operation
      report as emitted by the `operation-report` job.
- [x] 5.2 **DONE 2026-09-01** — same dispatch as 5.1 (run `33512287539`,
      `lane=both` covers both lanes in one run); composed report filed in
      `record review/readiness-evidence-2026-09-01.md`. Dispatch it on the
      ARTIFACT lane (`xfactory-artifact-workers` /
      `host-rider-cpc-brett01`). File the COMPOSED structured operation
      report from the same `operation-report` job.
- [x] 5.3 **DONE 2026-09-01** — read against run `33512287539`'s composed
      report and dispositioned in `record
      review/readiness-evidence-2026-09-01.md` §2: Gap 1 (coding lane round
      trip) CLOSED, Gap 2 (artifact lane service account) CLOSED, Gap 3
      (`artifact-only` label) STILL OPEN — carried forward as `tasks.md`
      §4.6. That same record also surfaces a fourth, unanticipated finding
      (both lanes share one Cloud PC host) not among the three named below —
      carried forward as `tasks.md` §4.7. **The three gaps these two runs are expected to close or expose**,
      recorded now so the reports are read against a question rather than
      skimmed:
      - **The coding lane has never completed a live round trip.** Every
        exercise of `xfactory-coding-cpc-brett01` to date has been as a child
        of real work. 5.1 is the first isolated confirmation that the host
        claims a job, executes, and returns.
      - **The artifact lane's service account is unconfirmed against the
        provisioning record.** The report's service-account field is the
        measurement. `design.md` DECLARES NO service account — nothing in
        this packet does — so compare the measurement against the document
        that actually declares one: `cloudpc-worker-handoff-prompt.md` at the
        root of `opensoft/xFactory`, which specifies the hidden local
        standard account `.\svc-omniworker` as the account the worker runs
        under. Record a divergence as a finding rather than adjusting the
        expectation, and do not cite this packet as the source of an
        expectation it never stated.
      - **The coding runner carries a suspicious `artifact-only` label — and
        the hazard is SYMMETRIC.** Runner `xfactory-coding-cpc-brett01`
        (group 7) reports labels `self-hosted, Windows, X64, omnigent,
        artifact-only, rider, coding-patch, host-coding-cpc-brett01` — this
        verbatim set stays as the measurement of record. A coding host
        labelled `artifact-only` is at best a leftover and at worst a routing
        hazard — a job requesting `artifact-only` can land on the coding
        host. **The symmetry, measured the same day**: the ARTIFACT runner
        `xfactory-artifact-cpc-brett01` (group 5) ALSO carries
        `artifact-only` AND `rider`. So neither label discriminates the lanes
        in EITHER direction; the labels that do are `coding-patch` (coding
        host only), the per-lane `host-coding-cpc-brett01` /
        `host-rider-cpc-brett01`, and the artifact host's task labels
        (`doc-analysis`, `document-cataloger`, `ideation-readiness`,
        `derive-possibles`, `dashboard-image`). Investigate BOTH runners, and
        do not "fix" the coding host alone as though the artifact host were
        clean; either way record the disposition.
- [x] 5.4 **DONE 2026-09-01** — filed as `record
      review/readiness-evidence-2026-09-01.md`. Note that this discharges
      §5.4's filing obligation only; §9.3's release-realization archiving
      still awaits §6.8's cut. File both reports plus the dispositions as the realization evidence
      this change's `code_surface` declaration owes (release-realization).

## 6. Neutral contract realization — POST-RATIFICATION, at its own cut

Deliberately not started before §2. Nothing here is authored by this packet.

- [ ] 6.1 `contracts/clearing/sealed-bundle-manifest.schema.yaml` — the ten
      declared fields, with expiration required, per-file hashes required
      alongside the file list, and the digest construction cited rather than
      redefined.
- [ ] 6.2 `contracts/clearing/permitted-operations.schema.yaml` plus the
      CLOSED registry INSTANCE
      `contracts/clearing/permitted-operations.registry.yaml`, on the
      `openxwallet-custody` schema-plus-instance pair convention. Entry #1 is
      `readiness-diagnostic` with its class constraints and
      `repository_affecting_output: false`.
- [ ] 6.3 `contracts/clearing/operation-report.schema.yaml` — the
      `readiness-diagnostic` report shape, and specifically THE COMPOSED
      REPORT: the artifact the `operation-report` job assembles from the lane
      jobs' forwarded outputs (§5), one report of record per dispatch across
      however many lanes were probed, carrying
      `clearing.dispatch.outcome=`. It is NOT a per-lane fragment schema, and
      it is not a log format. Per-lane facts appear as a keyed collection
      inside it. Each lane's `group` and `label` are typed as DECLARED values
      (§3.5), never as observed group membership. It carries probed FACTS and
      deliberately carries no eligibility verdict (design D9); a reviewer
      should refuse a field that turns it into a readiness decision.
- [ ] 6.4 `contracts/clearing/dispatch-record.schema.yaml` — resolved and
      claimed values, refusal grounds as a CLOSED NAMED ENUMERATION rather
      than free text, and the chain reference per §2.1 OQ2. **Seed the
      enumeration with exactly the two grounds the realization emits**
      (§3.5): `unregistered_operation` and `unknown_lane_selector`. The
      remaining named refusals in requirement text — expiry, hash mismatch,
      workflow-path contradiction, commit mismatch, unreadable API, lane not
      permitted, output-schema failure, origin-scoped credential,
      committed-data offer — become grounds as the operations that can
      produce them land; adding one is a governed change on this schema, not
      a new string in a workflow. Carry the DECLARED-vs-observed distinction
      into the field names so a declared lane cannot be read as an observed
      one.
- [ ] 6.5 `contracts/clearing/single-door-attestation.schema.yaml` — expected
      versus observed admitted repositories and allowlist entries per group,
      with the divergence direction carried.
- [ ] 6.6 Packaged POSITIVE examples plus a NEGATIVE fixture per named
      refusal: missing field, hash mismatch, expired handle, workflow-path
      contradiction, commit mismatch, unreadable API, unregistered operation,
      lane not permitted for the operation, output failing its declared
      schema, origin-scoped credential on the host, and a bundle offered as
      committed data.
- [ ] 6.7 Canonical `scripts/validate-clearing-dispatch.py` with the
      cross-shape rules the schemas cannot express, plus `tests/clearing/`
      under pytest on the per-family convention.
- [ ] 6.8 Register in `contracts/manifest.yaml` and `contracts/CHANGELOG.md`
      at the next additive bundle cut, the minor allocated AT REALIZATION
      after merge order is known. **Two cuts ahead are already claimed** —
      the in-flight `add-chain-attestation` realization takes the next, and
      `add-chain-anchoring` allocates after it — so read the manifest at the
      realization branch's tip rather than trusting any number written in
      this packet, and publish the annotated tag at the realized commit in
      the same act (the policy's recurring untagged-bundle gap,
      `opensoft/openxFactory#528`).

## 7. The single-door attestation realization (L5)

- [ ] 7.1 The attestation itself: read each governed group's admitted
      repositories and workflow allowlist from the provider API and compare
      against an expected set **COMPUTED PER GROUP** — the clearing
      workflow's path, UNION the members that §3.4's data file enumerates FOR
      THAT GROUP with allowlist status `present`. One estate-wide expected
      set is the wrong definition and cannot ever be green: it would report
      every group as diverging from every other group's members. Cadence and
      finding surface per §2.1 OQ4.
      **THE TWO DIVERGENCE DIRECTIONS ARE DIFFERENT OUTPUTS, not one
      finding:**
      - an OBSERVED entry the group's expected set does not derive is a
        WIDENING and a single-door breach — a finding naming the group, the
        entry, and the expected set. An admitted repository other than the
        clearing repository is a widening of the same class.
      - an ENUMERATED member with NO observed entry is ALREADY FAILING
        CLOSED. It is a DARK-LANE DISPOSITION ITEM (§8.3), NOT a breach.
      - the CLEARING PATH being absent before §4.1 is CONVERGENCE NOT YET
        REACHED, not a widening.
      **WHAT THE FIRST RUN IS EXPECTED TO REPORT, so it is read rather than
      panicked over** — measured 2026-09-01, and this is the seed to assert
      against: ZERO allowlist widenings on either group (group 7's one entry
      and group 5's six entries are all `present` members); TWO dark-lane
      items (`review-lane-worker.yml`, `ideation-organizer-worker.yml`); TWO
      not-yet-converged notices (the clearing path absent from both groups
      until §4.1); and EXACTLY ONE OPEN WIDENING — group 5's admission of
      `opensoft/codexFactory`, which §4.3 closes. So the allowlist axis is
      green on day one and the repository axis carries one known finding
      whose closure is already an operator task. Do not claim the attestation
      is green overall before §4.3.
- [ ] 7.2 State the residual where a reader of the finding sees it: the
      configuration being attested is not versioned, and the attestation is
      detection within one cycle rather than prevention.

## 8. Successor handoffs (named here, executed elsewhere)

- [ ] 8.1 `realize-factory-bundle-packaging` — the codexFactory hosted
      packaging workflow producing a conformant sealed bundle, plus the
      register entry for the CODING operation it feeds. Closes the ruling's
      cross-factory case end to end; blocked on nothing but §2 and its own
      authoring.
- [ ] 8.2 The HOSTED FINALIZER for patch-returning operations, gated on 8.1.
      `readiness-diagnostic` returns no repository-affecting output, so
      writing the finalizer now would be writing it against a guess.
- [ ] 8.3 The NINE grandfather retirements, one governed change each, each
      shrinking the enumeration and removing an allowlist entry in the same
      act. **THIS IS ALSO THE DARK-LANE DISPOSITION SURFACE §7.1 ROUTES TO.**
      Two members need a disposition before they need a migration:
      `ideation-organizer-worker.yml` and `review-lane-worker.yml` declare a
      job on group 5 and are enumerated `absent` (§3.4), so they are already
      failing closed with nothing reporting it. They are NOT single-door
      breaches and the attestation must not report them as such — nothing
      reaches the host through a lane with no allowlist entry, which is
      strictly safer than the expectation. Retire them into operations or
      remove the reference, but do not leave them undecided once the L4 guard
      and the L5 attestation make their state visible. A retirement of an
      `absent` member removes NO allowlist entry (there is none) and only
      shrinks the enumeration; a retirement of a `present` member does both,
      in the same act.
- [ ] 8.4 If and when the neutral INFRASTRUCTURE-READINESS RESULT that
      `document-cataloging` and `ideation-routing` both await is proposed,
      declare the `readiness-diagnostic` operation report a candidate INPUT
      to it and re-point the register entry's output schema. Do not grow the
      report into that contract (design D9).

## 9. Verification bar

- [ ] 9.1 `OPENSPEC_TELEMETRY=0 openspec validate --all --strict` green at
      every step, not only at authoring.
- [ ] 9.2 Repository validators and doc-health clean against THIS CHANGE'S
      OWN CONTENT — and the pytest suite is currently RED FOR A REASON THIS
      PACKET DID NOT CAUSE, recorded here so nobody reads a green tick that
      cannot exist yet.
      **THE INHERITED RED, named:**
      `tests/doc-health/test_modified_block_currency_self_gate.py::test_every_carriage_ledger_finding_over_the_real_tree_is_named`
      fails on ONE newly-unnamed carriage-ledger subject —
      `('add-chain-attestation', 'signed-execution-chain', 'A gate validates
      the short chain as a hash-linked chain')`. The self-gate names the
      subjects it expects; a new MODIFIED block over the tree makes it red
      until the module's named-subject list is updated.
      **IT IS INHERITED, and here is why that is not a convenience claim:**
      this packet's spec delta is ADDED-ONLY — it contains no `## MODIFIED
      Requirements` block at all — so it cannot contribute a carriage-ledger
      subject. The failing subject belongs to `add-chain-attestation`, and
      the failure REPRODUCES ON `origin/main` at `b7dc5909`. It is OWNED BY
      THE IN-FLIGHT `add-chain-attestation` REALIZATION LANE, which is where
      the named-subject list gets re-aimed, and NOT by this packet — fixing it
      here would edit another lane's gate out from under it.
      **CONSEQUENCE FOR THIS PULL REQUEST:** #555's required pytest-suite
      check is RED and MERGE WAITS ON THAT LANE'S RESOLUTION. Ratification
      (§2) is a separate act and is not blocked by it; merging is. Re-check
      before merge rather than assuming it has cleared.
- [ ] 9.3 Release-realization: this change declares a code surface, so it
      ARCHIVES only on merged realization plus green evidence — §5.4's filed
      reports and §6.8's cut — and stays ACTIVE until then, ratified or not.
