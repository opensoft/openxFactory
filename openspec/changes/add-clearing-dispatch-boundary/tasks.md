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

- [ ] 2.1 Brett ratifies proposal, design, and the spec delta, ruling or
      carrying the four open questions: **OQ1** when a signature becomes
      required for field 10 (recommendation: at the first cross-organization
      producer, expressed against `trust-anchor`'s certificate record);
      **OQ2** ledger record versus transparency-log entry (recommendation:
      own record kind, referencing a chain); **OQ3** where the grandfather
      enumeration lives (recommendation: an xFactory-side declaration the
      guard and the attestation both read, with the neutral contract
      requiring only that it exist, be closed, and shrink); **OQ4**
      attestation cadence and finding surface (recommendation: ride the
      existing nightly lane, emit a doc-health-shaped finding).
- [ ] 2.2 Record the rulings as a Ratification section in `proposal.md`, set
      `Status: ratified` with the ratifying commit named, and state that the
      change stays ACTIVE until the declared code surface is merged with
      green evidence and the contract cut exists.

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
      `.github/workflows/runner-readiness-diagnostic.yml` (PR #188, merged
      `4fffb6e5`, 2026-09-01). Its checks move into the operation verbatim in
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
- [ ] 3.4 The grandfather enumeration, per §2.1 OQ3, declared where the guard
      and the attestation both read it, seeded with exactly the NINE existing
      host-touching worker workflows: `execution-lane-coding-worker`,
      `council-deliberation-worker`, `review-lane-worker`,
      `ideation-organizer-worker`, `dashboard-image-worker`,
      `doc-health-analysis-worker`, `doc-health-readiness-worker`,
      `doc-health-cataloger-worker`, `doc-health-derive-possibles-worker`.
      Marked append-never in the file itself.
- [ ] 3.5 The dispatch record written by the clearing lane — verified
      provenance plus claimed-where-different, refusals included. Shape
      follows §2.1 OQ2; until the neutral schema lands (§6) the record is
      written in the shape the ratified requirement describes and re-pointed
      at the schema when it exists.
- [ ] 3.6 Merge gated on §2 — the workflow does not land before the packet
      that authorizes it.

## 4. The operator's acts — ONE console act per group, and one closure

- [ ] 4.1 Add `opensoft/xFactory/.github/workflows/clearing-dispatch.yml@refs/heads/main`
      to `selected_workflows` of group `xfactory-artifact-workers` (id 5) and
      group `xfactory-execution-lane-workers` (id 7). **ONE entry per group,
      once, ever** — this is the permanent entry the allowlist converges to.
      Perform AFTER §3 merges to `main`, so the path being admitted exists.
- [ ] 4.2 Do NOT add `runner-readiness-diagnostic.yml` to either group. This
      is Brett's option-1 ruling of 2026-09-01 and the reason the readiness
      test became an operation. Recorded as a task so a future operator does
      not "fix" a queued readiness run by adding the entry.
- [ ] 4.3 **CLOSE THE RESIDUAL THE RULING NAMES.** Group
      `xfactory-artifact-workers` (id 5) currently admits TWO repositories —
      `opensoft/xFactory` AND `opensoft/codexFactory` (measured against the
      provider API 2026-09-01). The ruling holds runner-group access to
      xFactory only. Remove the codexFactory admission. It is why run
      `33381257642` could queue at all, and with the allowlist restricting
      workflow paths to xFactory files, no codexFactory job can be claimed
      through it today — so the removal takes nothing away that works. Group
      7 already admits xFactory alone; nothing to do there.
- [ ] 4.4 Re-read both groups from the provider API after 4.1 and 4.3 and
      file the reading as the baseline the §7 attestation compares against.

## 5. Dispatch readiness on both lanes, and file the evidence

- [ ] 5.1 Dispatch `readiness-diagnostic` through the clearing lane on the
      CODING lane (`xfactory-execution-lane-workers` /
      `host-coding-cpc-brett01`). File the structured operation report.
- [ ] 5.2 Dispatch it on the ARTIFACT lane (`xfactory-artifact-workers` /
      `host-rider-cpc-brett01`). File the structured operation report.
- [ ] 5.3 **The three gaps these two runs are expected to close or expose**,
      recorded now so the reports are read against a question rather than
      skimmed:
      - **The coding lane has never completed a live round trip.** Every
        exercise of `xfactory-coding-cpc-brett01` to date has been as a child
        of real work. 5.1 is the first isolated confirmation that the host
        claims a job, executes, and returns.
      - **The artifact lane's service account is unconfirmed against the
        design.** The report's service-account field is the measurement;
        compare it with the design's declared `svc-omniworker` and record a
        divergence as a finding rather than adjusting the expectation.
      - **The coding runner carries a suspicious `artifact-only` label.**
        Runner `xfactory-coding-cpc-brett01` (group 7) reports labels
        `self-hosted, Windows, X64, omnigent, artifact-only, rider,
        coding-patch, host-coding-cpc-brett01`. A coding host labelled
        `artifact-only` is at best a leftover and at worst a routing hazard —
        a job requesting `artifact-only` can land on the coding host.
        Investigate and, if it is a leftover, remove it; either way record
        the disposition.
- [ ] 5.4 File both reports plus the dispositions as the realization evidence
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
      `readiness-diagnostic` report shape. It carries probed FACTS and
      deliberately carries no eligibility verdict (design D9); a reviewer
      should refuse a field that turns it into a readiness decision.
- [ ] 6.4 `contracts/clearing/dispatch-record.schema.yaml` — resolved and
      claimed values, refusal grounds as a named enumeration rather than free
      text, and the chain reference per §2.1 OQ2.
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
      the same act (the policy's recurring untagged-bundle gap, issue #528).

## 7. The single-door attestation realization (L5)

- [ ] 7.1 The attestation itself: read each governed group's admitted
      repositories and workflow allowlist from the provider API, compare
      against the clearing path plus the current grandfather enumeration and
      the clearing repository alone, emit a finding on any divergence in
      either direction. Cadence and finding surface per §2.1 OQ4.
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
      act. **Two need a disposition before they need a migration**:
      `ideation-organizer-worker.yml` and `review-lane-worker.yml` declare a
      job on group 5 and are NOT allowlisted, so they are already failing
      closed with nothing reporting it — retire them into operations or
      remove the reference, but do not leave them undecided once the L4 guard
      makes their state visible.
- [ ] 8.4 If and when the neutral INFRASTRUCTURE-READINESS RESULT that
      `document-cataloging` and `ideation-routing` both await is proposed,
      declare the `readiness-diagnostic` operation report a candidate INPUT
      to it and re-point the register entry's output schema. Do not grow the
      report into that contract (design D9).

## 9. Verification bar

- [ ] 9.1 `OPENSPEC_TELEMETRY=0 openspec validate --all --strict` green at
      every step, not only at authoring.
- [ ] 9.2 Repository validators and doc-health clean against this change.
- [ ] 9.3 Release-realization: this change declares a code surface, so it
      ARCHIVES only on merged realization plus green evidence — §5.4's filed
      reports and §6.8's cut — and stays ACTIVE until then, ratified or not.
