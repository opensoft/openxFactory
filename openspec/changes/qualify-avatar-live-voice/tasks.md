# Tasks: qualify-avatar-live-voice

Governance-level and dependency-ordered. **§1 is authored by this change; §2
onwards are the realization plan and are NOT being executed now.** This change
carries a live code surface across two repositories, so it archives only on
merged code plus green internal-live realization evidence — never on landing
alone. The eight decisions RULED 2026-08-26 are locked inputs throughout: no
task below may re-open one, and a task that appears to require re-opening one
is mis-specified.

> **Amended 2026-08-27.** The proposal was ratified in-session that day, and §2
> and §3 were built in the ratifying round — the openxFactory contract slice:
> AVC-09 and AVC-10 published from their reserved shapes, the interface-lock
> unreservation of exactly those two, the validator's rules for them and for
> the two-tier latency posture, and the acceptance-map entries. §4 through §6
> remain unbuilt and unticked. The sentence above stands as the plan's original
> statement; this note records where the plan now actually is.
>
> **Amended again 2026-08-27, later the same day.** §7.1-§7.6 were RULED and
> are ticked; §7.7-§7.10 stay open, and 7.7 needs a person or rota named
> before the canary opens. Task 6.1.1 is DONE as a consequence — the custody
> pair the §7.1 and §7.3 rulings feed is authored, in its neutral half, with
> the concrete install-side binding named as a separate act in a repository
> this change does not touch. The rest of §4 through §6 remains unbuilt: 6.1.2
> is Brett's provisioning act, 6.1.3 and 6.1.4 are the wiring slice, and 6.1.5
> is deferred by ruling.
>
> **Amended a third time 2026-08-27.** §7.7-§7.10 were RULED in session and
> are ticked, so **§7 IS NOW FULLY RULED** — every authoring input the rulings
> deliberately left to proposal time carries a value, and the sentence above
> about 7.7 needing a person named is discharged: Brett Heap holds both kill
> switches, and the mechanism is the runbook at
> `docs/sops/avatar-internal-live-kill-switch.md`. The two cross-dependencies
> §7 was carrying against itself are closed with them: §7.4's page target is a
> named person rather than a role, and §7.2's metered per-tenant budget has a
> subject (tenant = cohort member, so two tenants, which is the denominator
> $150/month was sized against — no re-sizing needed). What did NOT change:
> §4 through §6 are still unbuilt apart from 6.1.1, 6.3.1 and 6.3.2, the
> AVC-09 descriptor is NOT authored — §7.9 pins the values it will declare,
> nothing more — and the ring's archive gate is unmoved.
>
> **Amended a fourth time 2026-08-27 — THE WIRING SLICE IS BUILT.** §6.1.3,
> §6.1.4 and §6.3.3-§6.3.5 are ticked. They are wired ONTO the landed
> reference runtime and invent nothing: the session hard-kill terminates
> through the kernel's existing duration-or-quota outcome with the same
> media-plane termination act the kill switch and the consent-withdraw path
> already perform (now factored out and shared by four callers rather than
> duplicated four times), the rollback act IS the existing two-switch kill
> switch, and ROLLBACK-A's abort reuses the consent-withdraw terminal exactly.
> The closed `OutcomeCode`, `AttemptStatus` and released `session-outcomes`
> registries are UNCHANGED — not one member added anywhere — and the frozen
> `contract-v1.7` conformance coordinates are undisturbed
> (`check_conformance.py` reports the same 106 required scenarios and 106 map
> entries as before, with the two pre-existing acr source-drift findings
> unchanged in number and kind). Every ruled number the wiring consumes is
> READ BACK from its own artifact by
> `tests/avatar_runtime/test_ruled_values_pinned.py` — the §7.2 ceilings and
> caps, the §7.4 channels, §7.5's declared n, ALV-SLO-001's materiality and
> gated set, the three-way split with its triggers and revoke flags, §7.7's
> operator surface, §7.8's tokens and §7.10's tenant count — so a drift in
> either the contract or the mirror fails a test rather than surfacing when
> the canary trips on the wrong number.
>
> WHAT REMAINS AFTER THIS SLICE, stated so no reader mistakes a built wiring
> for an opened ring: **6.1.2 is Brett's provisioning act** and everything
> install-side waits on it — the dedicated spend-capped provider project, its
> native budget notifications, and the scheduled job that actually invokes
> `gh issue create`, which is recorded rather than committed because a
> workflow with no input would be a fabricated procedure. **6.1.5 stays
> deferred** by ruling, and the provider-project cap remains the ring's only
> per-tenant hard stop. **§6.2 is unbuilt** — 6.2.1's synthetic corpus in
> particular, which is why 6.3.3's safety trip lands as a fail-closed INPUT
> SEAM rather than as a wired corpus. **6.4.4 is unbuilt.** **§4, §5 and §8
> are unbuilt**, so no evidence, no measured latency, no ring element and no
> archive gate has moved. §7.4's own condition — at least one alert observed
> DELIVERED end to end before the canary opens — is recorded
> `not_yet_delivered` rather than quietly satisfied by a unit test.
>
> **Amended a fifth time 2026-08-27 — §6.2 IS BUILT.** §6.2.1-§6.2.4 are
> ticked. Fork 4 Option C now has artifacts instead of prose: the SYNTHETIC
> evaluation corpus at
> `contracts/avatar-client/synthetic-evaluation-corpus.yaml` (35 scripted
> scenarios, all 15 class x domain cells, all EIGHT ROLLBACK-A triggers
> reachable) and the canary's ephemeral processing envelope at
> `contracts/avatar-client/canary-ephemeral-processing-envelope.yaml`, both
> machine-checked by two new fail-closed validator checks and 32 tests whose
> every negative is a MUTATION OF THE REAL ARTIFACT. The corpus CLOSES the
> hole §6.3.3 recorded in its own tick — "§6.2.1's CORPUS DOES NOT EXIST, so
> what is built is the INPUT SEAM" — and it closes it in the direction that
> matters: each scenario's trigger is resolved against the ROLLBACK-A list in
> the ratified policy artifact, not against a constant, so a corpus scenario
> that no ratified trigger covers fails rather than shipping as a failure that
> would never abort the ring.
>
> WHAT DID NOT MOVE, stated so no reader mistakes a built §6.2 for an opened
> ring: no schema, no registry and no interface lock is edited. The frozen
> consent-purpose count stays 3, the four reserved retention classes stay
> forbidden, `local_persistence` stays `const: false` — CONFIRMED BY
> INSPECTION at file and line in
> `review/reserved-surface-inspection-2026-08-27.md`, not by assertion and not
> by a test standing in for one. The non-shadowing guarantee is recorded as an
> OPERATIONAL control with `enforced_by_schema: false` in a field, because no
> schema forbids a second-model shadow today and the enforcing contract flag
> is `avatar-pilot-hardening` work. No AVC-09 descriptor is authored, no
> evidence register is touched, no audio is rendered or retained, and no ring
> element has moved.
>
> **WHAT REMAINS AFTER §6.2:** **6.1.2 is Brett's provisioning act** and
> everything install-side still waits on it. **6.1.5 stays deferred** by
> ruling. **6.4.4 is unbuilt.** **§4, §5 and §8 are unbuilt**, so no evidence,
> no measured latency and no archive gate has moved. §7.4's own
> at-least-one-alert-delivered condition still reads `not_yet_delivered`.
>
> **Amended a sixth time 2026-08-28 — §6.4.4 IS BUILT, AND IT REPORTS A
> BLOCKED RELEASE GATE.** The sentence "6.4.4 is unbuilt" above is superseded;
> the rest of that paragraph stands. The release evidence
> `repo-boundary-governance` "Avatar-client release evidence" obliges is
> standing up in `opensoft/openAvatar` (PR #6, branch
> `feat/release-evidence`), as `release_evidence.yaml` beside
> `contract_pin.yaml`. **It stays UNTICKED here** on 6.4.2's own rule for
> cross-repo tasks — and that rule is currently load-bearing rather than
> ceremonial, because 6.4.2 and 6.4.3 MERGED upstream on 2026-08-27 and are
> themselves still unticked here.
>
> WHAT MAKES IT EVIDENCE RATHER THAN A RECORD OF INTENT: the artifact is
> GENERATED, and every element carries the command that produced it, that
> command's exit code, its own verdict line verbatim, and a digest of its
> captured output. Eight of the nine elements are satisfied by a real run —
> the pin's 71 files recomputed offline, six conformance replays, 93 locked
> packages with ZERO unpinned sources, a real 13-pattern secret scan over 435
> files with ZERO findings, and `melos run ci` green end to end at 533 tests
> across 11 suites on a Linux bench, so the authoritative pixel goldens and the
> eleven accessibility capabilities executed rather than self-skipping. The
> rollback target is not asserted either: `text` and `human_handoff` are
> checked as members of the digest-pinned `fallback-modes` registry, and the
> closed set is checked to contain no member a reader could take for the model
> swap 6.3.4 forbids.
>
> **THE NINTH ELEMENT IS THE POINT.** RE-08 client integrity is
> `not_yet_satisfiable`, `blocks_release: true`, and the artifact's own
> verdict reads BLOCKED. That is scenario RBG-002-S02 being OBEYED, not missed:
> a client that cannot prove desktop signing or web deployment integrity for
> the code enforcing disclosure and local media gating must FAIL release
> validation, because the confidentiality trusted computing base is not
> established. Neither surface exists — the generator probes for both and
> records what it looked for, so the verdict is reproducible and flips by
> itself when material lands. **The desktop half is Brett's, install-side: it
> needs a code-signing certificate, the same class of act as 6.1.2. The web
> half has NO OWNER YET** — the production deployment home is routed by
> `repo-boundary-governance` to this change's live-qualification successor, and
> openAvatar's web CI leg is a smoke that ships nothing. Either surface
> discharges the element; the desktop path is the shorter one.
>
> WHAT DID NOT MOVE: no schema, registry, interface lock or acceptance-map
> entry is edited, no AVC-09 descriptor is promoted (it stays `candidate`, with
> zero latency evidence refs, exactly as §7.9 and §6.4.3 left it), no ring
> element is closed, and no archive gate has moved. RING-02 gains its CLIENT
> half only — the broker deployment's scan is install-side and untouched.
> **WHAT REMAINS: 6.1.2 (Brett), 6.1.5 (deferred by ruling), §4, §5 and §8
> (unbuilt), §7.4's `not_yet_delivered` alert condition, and now RE-08's
> client-integrity blocker with its two named owners.**

## 1. Spec deltas (THIS CHANGE)

- [x] 1.1 `avatar-live-voice` — NINE ADDED requirements: AVC-09 adapter
      descriptor; AVC-10 latency sample; the internal-live activation gate as
      the kernel's four-element ring with the eight conditions demoted to its
      mapped preflight/canary checklist; the neutral relative-regression
      latency SLO at the ratified threshold; the fresh client-side
      direct-provider reference baseline; broker-held custody with layered
      fail-closed spend containment; synthetic evaluation audio with an
      ephemeral single-model consented canary; the canary cohort and the
      recorded revoke-versus-block rollback policy; and the named deferrals
      the pilot-hardening successor carries.
- [x] 1.2 `avatar-client-runtime` — THREE MODIFIED requirements, each
      restating its promoted canon in full and amending only the sentences
      the rulings touch: "Versioned neutral avatar-client contract kernel"
      (AVC-09 and AVC-10 released from the reserved set, AVC-03 and AVC-05
      left reserved), "Server-owned model profiles and session-fixed persona"
      (approved promotion evidence qualifies `gpt-realtime-2.1` for the
      internal-live ring ONLY — latent decision 3), and "Redacted telemetry
      and latency evidence" (AVC-10 exists; internal-live latency evidence is
      judged by the neutral relative-regression rule against a same-platform
      client-side reference, never against F0's harness figures).
- [x] 1.3 `repo-boundary-governance` — ONE MODIFIED requirement, "Neutral
      avatar-client repository boundary": the named creator moves from
      `implement-avatar-client-lab` (which archived having ratified the
      codexFactory lab home instead) to this change, extracting at the
      internal-live gate. The sibling "Deferred aggregation and web-console
      integration" requirement is deliberately NOT touched — aggregation
      admission stays a separate reviewed change.
- [x] 1.4 `avatar-client-lab` — ONE MODIFIED requirement, "Repository and
      ownership boundary": the codexFactory home holds until the
      internal-live gate, where this change extracts it; openxFactory's
      ownership of contracts, fixtures and acceptance requirements is
      unchanged.
- [x] 1.5 Move the staged topic's two files into `supporting-docs/` with the
      staging origin preserved (`scripts/proposal-support.py transition`),
      and record the staged origin in `.openspec.yaml`.
- [x] 1.6 `OPENSPEC_TELEMETRY=0 openspec validate qualify-avatar-live-voice
      --strict` green and `--all --strict` green before commit.
- [x] 1.7 Staging bookkeeping: the topic promoted FULLY (no file remains
      staged), so its row and detail section leave
      `ideation/staging/INDEX.md` and the pointer moves to
      `ideation/README.md`'s "Active proposals promoted from staging" list
      per the INDEX maintenance rule. List the change in README's "OpenSpec
      Records" active block.

## 2. Contracts: AVC-09 and AVC-10 (openxFactory)

The RESERVED SHAPES ARE USED AS-IS. F2's Option C means AVC-09 gains NO
numeric latency-budget field; adding one would be the Option B that was not
ruled.

- [x] 2.1 Author `contracts/avatar-client/avc-09-voice-adapter-descriptor.schema.yaml`
      to the reserved shape: server/client adapter components, adapter id and
      version, provider, supported profiles, requested model alias or
      snapshot, provider-resolved model, prompt/policy/voice/turn
      configuration versions, capability and event mapper versions,
      authorization mode, sideband readiness, direct-media requirement,
      contract compatibility, region and data controls, and
      experimental/candidate/approved/retired status. `contract_id`,
      `contract_schema_version`, `$ref` into
      `shared-definitions.schema.yaml`. No budget field; no secret-shaped
      field.
      **Done 2026-08-27.** `avc-09-voice-adapter-descriptor.schema.yaml`,
      `contract_id: AVC-09`, `contract_schema_version: 1`, `$ref` into
      `shared-definitions.schema.yaml` through the session/media `$defs` its
      siblings share. Every field the reserved shape names is present and the
      component split is structural — `server_component` holds the
      prompt/policy/voice/turn configuration versions, `client_component` holds
      only mappers, and both are CLOSED shapes so a server provider
      configuration cannot appear on the client half. Option C is enforced, not
      merely honoured: the top-level `not` refuses ten spellings of a numeric
      latency budget and fifteen of secret or raw content, so an additive field
      cannot smuggle either back. `latency_evidence_refs` is the descriptor's
      only latency surface, and `status: approved` requires at least one
      reference — an approved adapter with no measured evidence behind it is
      invalid.
- [x] 2.2 Author `contracts/avatar-client/avc-10-voice-latency-sample.schema.yaml`
      to the reserved shape: sample/session/media-leg/turn identity, adapter
      and profile, platform, network, region, clock source and quality,
      monotonic markers (broker request, provider call, sideband ready, media
      connected, speech, first audio, playback, interruption, command, tool
      outcome, recovery, teardown), derived intervals, direct-or-brokered
      reference classification, reproducible fixture reference. No raw
      content, no secrets.
      **Done 2026-08-27.** `avc-10-voice-latency-sample.schema.yaml`,
      `contract_id: AVC-10`, `contract_schema_version: 1`, sharing
      `session_epoch` and `media_leg` through `shared-definitions`. The twelve
      markers are a closed `markers` object of raw monotonic offsets from a
      declared `monotonic_origin`; `derived_intervals` is a separate closed
      object so a reader can RECOMPUTE rather than trust. `platform`,
      `network_class`, `clock.source` and `clock.quality` are closed enums, and
      `reference_classification` is the required field that separates a
      direct-provider reference from a governed-adapter sample. A sample is one
      OBSERVATION: no percentile field, no budget field, and a `not` that
      refuses transcripts, captions, media, SDP, credentials and raw provider
      payloads.
- [x] 2.3 Packaged positive AND negative examples for both contracts,
      including the negatives that must fail: an AVC-09 carrying a numeric
      latency budget, an AVC-09 carrying secret material, an AVC-10 carrying
      transcript or SDP content, and a cross-platform regression comparison.
      **Done 2026-08-27**, packaged the way every other avatar-client contract
      packages fixtures — as self-describing cases in
      `contracts/avatar-client/fixtures/index.yaml`, executable by any
      conformant draft 2020-12 implementation without the Python validator.
      AVC-09: `avc09-valid` plus `avc09-latency-budget-refused`,
      `avc09-carries-secret`, `avc09-client-component-carries-provider-config`
      and `avc09-approved-without-latency-evidence`. AVC-10:
      `avc10-governed-adapter-valid` and `avc10-direct-reference-valid` plus
      `avc10-carries-transcript`, `avc10-carries-sdp` and
      `avc10-unknown-marker`. THE CROSS-PLATFORM COMPARISON COULD NOT BE A
      SCHEMA CASE: a refusal of a comparison is a property of a PAIR of sample
      sets, not of one instance, so it is packaged as a new self-describing
      `latency_comparison_cases` block — the same shape `release_pin_cases`
      already uses for the pinning rule — and executed by the §3.3 check.
      `slo-cross-platform-comparison-refused` is deliberately built so it WOULD
      HAVE PASSED on the arithmetic (900 ms reference against 910 ms adapter),
      which is what makes the structural refusal worth proving. The validator's
      per-schema coverage rule now demands a passing valid and a passing
      invalid case for both new contracts, so the fixtures cannot silently
      lapse.
- [x] 2.4 Register both in `contracts/manifest.yaml` and
      `contracts/CHANGELOG.md` at the next additive bundle cut; the bundle
      number is fresh-counted at realization, not allocated here.
      **Done 2026-08-27 at `contract-v1.46`**, fresh-counted as the policy
      requires rather than reserved in advance. COLLISION CHECK: `main` at
      `42662b70` declares `contract_bundle_version: contract-v1.45`, the
      CHANGELOG's newest entry is `contract-v1.45` (2026-08-26) and
      `contracts/releases/` holds no inventory above `contract-v1.45`, so 1.46
      was free; if a parallel bundle lands first this renumbers by the
      established sweep (manifest version, consumption-rule pins, CHANGELOG
      heading, README rows, inventory filename and `bundle_tag`). ADDITIVE:
      two new schemas, no existing shape narrowed, every
      `contract_schema_version` still `1`. Registered as
      `avatar-client-avc-09-voice-adapter-descriptor` and
      `avatar-client-avc-10-voice-latency-sample` with per-file sha256 and
      consumption rules; the four members whose bytes moved with the release —
      `interface-lock.yaml`, `acceptance-map.yaml`, `evidence-register.yaml`,
      `fixtures/index.yaml` — are RECOMPUTED in the same cut. Contract index
      updated in both places it lives: `contracts/README.md`'s
      `avatar-client/` row (8 -> 10 contracts, the SLO summarized) and
      `contracts/avatar-client/README.md`'s family table, conformance counts
      (17/72 -> 26/107) and digested-set sentence, plus the root README's
      document-index entry. `contracts/releases/contract-v1.46.digests.yaml`
      is built and committed IN this PR; membership is unchanged from
      `contract-v1.45` (192 entries) with four digests moving — CHANGELOG,
      `contracts/README.md`, `contracts/manifest.yaml`, and
      `scripts/validate-hermes-runtime-contracts.py`, that last one because
      main advanced it on 2026-08-27 after the v1.45 cut. The TAG is published
      post-merge by the orchestrator, per the policy's rule that a bundle is
      not published until its tag exists.

## 3. Unreservation and validator (openxFactory)

- [x] 3.1 `contracts/avatar-client/interface-lock.yaml` — move EXACTLY
      `AVC-09` and `AVC-10` from `frozen.reserved_identifiers` into
      `frozen.contracts`. `AVC-03` and `AVC-05` STAY reserved;
      `reserved_retention_classes: forbidden` and
      `registries.consent-purposes: 3` are NOT touched.
      **Done 2026-08-27.** `frozen.contracts` is now the ten
      `[AVC-01, AVC-02, AVC-04, AVC-06, AVC-07, AVC-08, AVC-09, AVC-10, AVC-11,
      AVC-12]` and `frozen.reserved_identifiers` is exactly `[AVC-03, AVC-05]`.
      Nothing else in the file moved: `reserved_retention_classes: forbidden`,
      `registries.consent-purposes: 3`, the timeouts, the ordering invariants,
      the F0 pin and the realized stamp are byte-identical. Because this is a
      baseline edit made by a change OTHER than the one the file's own header
      names, a comment records who moved the two ids and why exactly two, and
      §3.2's new `interface_lock_reserved_set` check now machine-checks both
      lists against the validator's constants so the pair can never drift apart
      again.
- [x] 3.2 `scripts/validate-avatar-client.py` — the constant at line 89
      (`RESERVED_IDS`) mirrors the interface lock by hand rather than reading
      it, and its guard at lines 300-303 fail-closes on the mere EXISTENCE of
      an `avc-09-*.schema.yaml` file. Remove the two ids from `RESERVED_IDS`
      and add the two filenames to `CONTRACT_FILES` (lines 79-88) in the SAME
      change that lands the schemas, or the repository goes red between
      commits. Update the stale "one of the 8 AVC ids" message at line 279.
      **Done 2026-08-27, in this one commit** — the constants and the schemas
      move together exactly as the task warns they must. `RESERVED_IDS` is now
      `{"AVC-03", "AVC-05"}`; `CONTRACT_FILES` gains the two filenames in id
      order. The line-279 message no longer hard-codes a count: it reads
      `len(CONTRACT_FILES)` and prints the sorted id set, so the next
      unreservation cannot re-stale it. Added `check_interface_lock` (evidence
      check `interface_lock_reserved_set`, discharging ACR-001-S04): it
      compares the lock's two lists against `CONTRACT_FILES` / `RESERVED_IDS`,
      requires them disjoint, and fails closed on a missing lock — the hand
      mirror the task names as the hazard now fails LOUDLY rather than
      silently.
- [x] 3.3 Add the validator rule that enforces the two-tier latency posture:
      exactly one neutral relative-regression SLO entry in the acceptance map,
      and a refusal of any per-profile numeric latency ceiling presented as a
      gating field.
      **Done 2026-08-27** as `check_latency_posture` (evidence check
      `latency_posture`). EXACTLY ONE: the check WALKS the acceptance map for
      mappings declaring `kind: neutral_relative_regression` rather than
      reading one known key, so a second entry hidden elsewhere is found —
      "exactly one" has to mean exactly one in the document, not one where we
      looked. Zero fails closed (an ungated ring); two fail (two rules say
      nothing about which binds); and the ratified threshold is compared, not
      defaulted — `greater_of`, 15 percent, 150 ms — so a drift in either
      direction is a finding. TWO TIERS: the gated set must be exactly p50+p95
      on the two setup intervals, Windows desktop and web canvas at nominal
      network; the recorded tier must name p99 and a teardown interval; the two
      tiers must be DISJOINT, because a percentile declared both ways makes the
      posture unreadable. NO CEILING: property names under any `properties`
      mapping in every avatar-client schema, and every key in the acceptance
      map, are matched against a ceiling-name pattern — the schema walk skips
      `not` blocks, since AVC-09 and AVC-10 name those very strings in order to
      FORBID them and a scan that could not tell a prohibition from a
      declaration would fail the schemas doing the prohibiting. Finally the ten
      `latency_comparison_cases` are executed against
      `adapter > reference + max(0.15 * reference, 150)` with refusal checked
      FIRST, and all four outcomes (`pass`, `fail`, `recorded`, `refused`) must
      be exercised or the posture is not proven end to end. Their evidence ids
      join the set the evidence register resolves against, so an automated
      entry may name a comparison case exactly as it may name a fixture.
- [x] 3.4 `contracts/avatar-client/acceptance-map.yaml` — an entry for every
      requirement and scenario this change adds or modifies, each naming its
      owning task, evidence identifier, release ring and status. Bump
      `expected_requirement_count` (17 today) and `expected_scenario_count`
      (72 today) by the amounts this change actually adds, measured rather
      than assumed. The map already lists `qualify-avatar-live-voice` in
      `owner_changes` for ACR-007, ACR-011, ACR-012, RBG-002 and SCO-002 —
      those entries are pre-authored for this change and must be discharged,
      not duplicated.
      **Done 2026-08-27.** Counts MEASURED off this change's own delta files,
      not assumed: `grep -c '^### Requirement:'` / `'^#### Scenario:'` gives
      `avatar-live-voice` 9/31, `avatar-client-runtime` 3/12 against 9 already
      mapped, `repo-boundary-governance` 1/3 against 2 already mapped. So +9
      requirements and +35 scenarios — 17 -> 26 and 72 -> 107 — and the
      provenance of those two numbers is written into the map itself. The nine
      ADDED requirements are ALV-001..ALV-009 under the new `avatar-live-voice`
      capability, each requirement and each scenario naming its owning task,
      evidence identifier, release ring (`internal_live` throughout) and
      status. The four MODIFIED requirements gained one scenario each in place
      — ACR-001-S04, ACR-007-S05, ACR-011-S03, RBG-001-S03 — rather than a
      duplicate requirement row, and ACR-001 and RBG-001 gained
      `qualify-avatar-live-voice` in `owner_changes`. ACR-012, RBG-002 and
      SCO-002 take no new scenario from this change, so they are DISCHARGED
      through an `owner_change_obligations` entry naming the owning task, ring
      and status — recorded rather than duplicated. `evidence-register.yaml`
      gains a matching entry for all 35 (107 total): fourteen automated against
      a packaged fixture or comparison case, ACR-001-S04 against the
      `interface_lock_reserved_set` check, and the rest DEFERRED with an
      explicit fail-closed default, because §4 through §6 have not run and
      claiming otherwise would be false. The new scenarios belong in this
      bundle's released register by the successor-register rule's own terms — a
      successor exists only to discharge, and a brand-new scenario belongs to a
      future bundle's map and released register, which is what this cut is.
      THE 3.4 / 5.4 SPLIT, followed exactly: this task writes the SLO ENTRY —
      `ALV-SLO-001`, at the ratified threshold, which is ratified canon
      available today and which §3.3's check fails closed without, and which
      §8.2 requires present in the same commit that unreserves the two ids.
      Task 5.4 owns the ENCODING AGAINST THE EVIDENCE RUN: the per-cell
      measured figures, carried under `measured_evidence` as
      `status: not_yet_measured` with §5 named as their owner and F0's
      distributions recorded as sanity checks that do not qualify as the
      reference. No §5 box is ticked.

## 4. The internal-live activation gate (F3 Option C)

The four-element ring is the binding exit contract; the eight conditions are
the checklist that produces its evidence.

- [x] 4.1 Record the per-condition classification as a checklist artifact
      alongside the acceptance map, exactly per the memo's mapping:
      conditions 1, 2, 3-topology, 4, and the deterministic halves of 5 and 7
      are HARD PREFLIGHT; the live domain-voice eval (5), the live
      cross-domain safety/exact-value/consent/handoff/blocked-state evals (7),
      the measured latency figure (3), and the opt-in canary (8) are
      CANARY-TIME; the kill switches and rollback machinery under 8 are HARD
      PREFLIGHT. Condition 6 is recorded in its reinterpreted form only.
      **Done 2026-08-27.**
      `contracts/avatar-client/internal-live-activation-checklist.yaml`,
      beside `acceptance-map.yaml` as the task requires. The eight conditions
      carry the memo's Fork 3 mapping exactly, and FOUR of them are recorded as
      SPLITS rather than collapsed to one class — 3 (topology hard preflight /
      measured figure canary), 5 (deterministic UI hard / live domain-voice
      canary), 7 (deterministic blocked-state and exact-value hard / live
      cross-domain evals canary) and 8 (kill switches and rollback machinery
      HARD PREFLIGHT / opt-in canary canary-time). Collapsing 8 to a single
      canary class is the specific error that would let a canary open on
      unproven kill switches, so it is the mutation the check is built around.
      Condition 6 is recorded in its REINTERPRETED form only
      (`recorded_form: reinterpreted_only`); the as-written comparative string
      is carried solely to name what was reserved to the GPT-Live adoption
      change, flagged `as_written_form_is_reserved: true`, and is never a
      second classification. The four ring elements each cross-reference the
      acceptance-map entries that own their evidence — RING-02 to RBG-001 and
      ALV-001-S03, RING-03 to ACR-011-S01, RING-04 to ACR-012-S04 and
      ALV-003-S02, RING-05 to ALV-004 and ALV-SLO-001 — and `gate_confers`
      states the ring yields a selectable internal-live profile and NO
      production default (latent decision 3, task 4.6's constraint binding this
      artifact's copy in advance of 4.6's own box).
      VALIDATOR EXTENDED, per how §3's rules were added: `check_activation_
      checklist` mirrors the ratified classification in validator constants
      (`CHECKLIST_RULED`, `CHECKLIST_RULED_HALVES`, `CHECKLIST_RING_ELEMENTS`)
      and machine-compares the artifact against them, exactly the discipline
      `check_interface_lock` applies to the frozen identifier lists — a ruling
      copied by hand drifts, and one that is machine-compared drifts loudly.
      `_check_map_refs` resolves every `acceptance_map_refs` entry against the
      map so a renamed scenario is a finding rather than a decoration. THE
      RELEASED REGISTER IS NOT TOUCHED: `acceptance-map.yaml` and
      `evidence-register.yaml` were cut at `contract-v1.46` and stay
      byte-identical, so the new check is deliberately NOT registered as an
      evidence-check id and no `deferred` status is flipped — the enforcement
      is the fail-closed check itself, and discharging ALV-003's scenarios is
      §4.2-§4.6's work against real evidence.
      MUTATION CHECK: 18 mutations across both §4.1 and §6.3 artifacts, 18
      caught, 0 missed — including the four that matter most (condition 8
      collapsed to canary-time, the kill-switch half reclassified, a condition
      deleted, and the ring widened by a sixth element).
- [ ] 4.2 RING ELEMENT — secret scan: a green scan across the extracted
      client repository and the broker deployment, with the release-evidence
      obligations of `repo-boundary-governance` "Avatar-client release
      evidence" active from this gate.
- [ ] 4.3 RING ELEMENT — telemetry-redaction verification: prove that no log,
      trace, metric, crash report or support bundle carries a credential,
      SDP, raw transcript, raw media, or prohibited identifier.
- [ ] 4.4 RING ELEMENT — kill-switch proof: both server kill switches
      (all-new-session-creation and per-model-profile) exercised for real,
      each in both block-new and revoke-active modes, BEFORE any canary
      traffic.
- [ ] 4.5 RING ELEMENT — measured latency evidence: §5's baseline and gated
      cells, green against the SLO.
- [ ] 4.6 Record explicitly that passing this gate confers a selectable
      internal-live profile and NO production default (latent decision 3), so
      a later reader cannot infer promotion from the gate's closure.

## 5. Latency: baseline, SLO, and evidence (F2 Option C)

- [ ] 5.1 MEASURE A FRESH CLIENT-SIDE DIRECT-PROVIDER BASELINE on the real
      Flutter client. F0's numbers — first-playable p50 603.63 / p95 643.488
      ms, sideband p50 772.37 / p95 1642.119 ms — came from a single
      Python/aiortc harness with `region: null` on neither gated platform,
      and the memo is explicit that they DO NOT QUALIFY as the reference.
      They may be cited as sanity checks only.
- [ ] 5.2 Declare the minimum sample count per gated cell BEFORE measuring,
      and record it with the evidence (§7.5).
- [ ] 5.3 Produce the gated cells: Windows desktop and web canvas at nominal
      network, p50 and p95, on first-playable-after-authorized and
      sideband-ready, for both the direct reference and the governed adapter,
      recorded as AVC-10 samples with the direct-or-brokered classification.
      Linux CI is reference-generation only and is never a gated delivery
      platform.
- [ ] 5.4 Encode the acceptance-map SLO entry at the RATIFIED threshold:
      material regression = more than 15% relative OR more than 150 ms
      absolute, whichever is GREATER. The "whichever is greater" clause is
      load-bearing — a percentage-only or milliseconds-only reading fails
      differently on fast and slow intervals.
- [ ] 5.5 RECORD, do not gate: p99, teardown / hangup-to-terminal,
      degraded-network runs, and steady-state per-turn speech-to-first-audio.
      The five-second revocation bound stays pass/fail, not a percentile.

## 6. Custody, spend, consent, canary, and the client repository

### 6.1 Credential custody and spend (F1 Option C)

- [x] 6.1.1 Author the broker server-key credential binding under the
      promoted `xfactory_credential_binding_template` shape — provider,
      vault, secret_ref, owner, rotation_policy — resolved only by the
      broker. No plaintext key in any repository; the age-encrypted registry
      copy is supervised recovery material, never a deployment source.
      **Done 2026-08-27**, as a PAIR, because the ruling splits across two
      repositories and the published shape cannot hold half of it.
      `contracts/avatar-client/broker-server-key-binding.template.yaml` is the
      binding, under the promoted shape exactly and with no invented field:
      all five members present, `secret_ref:
      avatar-broker-openai-internal-live` (a NEW reference — 6.1.2 requires a
      dedicated project distinct from the F0 lab, so a distinct key follows),
      `owner: opensoft-platform` carried forward from the F0 Credential
      Record, `rotation_policy: operator_managed`, and a `resolution` block
      pinning `resolved_by: broker_only` with ephemeral process-scope
      materialization. `provider` and `vault` are PER-INSTALL PLACEHOLDERS by
      canon, not by omission: `credential-contracts` says "Contract
      artifacts, lane definitions, and domain repositories SHALL NOT hard-code
      a vault operator, a vault product, or any secret value", and this
      repository is a contract-artifact tree. §7.3's cadence rides
      `broker-server-key-rotation-policy.yaml` beside it, because the
      published schema types `rotation_policy` as a plain string and every
      corpus instance uses it as an accountability label; the two files name
      each other, and the validator fails if that pointer drifts. THE §7.2
      CEILINGS ARE DELIBERATELY NOT HERE: the template shape carries no
      spend, duration or budget field, and inventing one would have put a
      number in a record no reader resolves.
      **THE NAMED INSTALL-SIDE ACT, left for the install's own PR.** The
      concrete binding — `provider: azure_key_vault`, `vault:
      kv-opensoft-xfactory-qa`, resolved by the broker's own AKS workload
      identity through the Secrets Store CSI driver — belongs at
      `installs/hermes-install/credentials/avatar-broker-bindings.yaml` in
      `opensoft/xFactory-Hermes-Install`, with the matching
      `SecretProviderClass` entry naming
      `avatar-broker-openai-internal-live` in the broker's
      `deploy/kubernetes/overlays/aks-qa/` overlay beside the two that
      already serve the live stack. That repository is NOT touched by this
      change and no file in it is written here. Its own PR carries the
      binding, the `SecretProviderClass`, a no-secret scan over the rendered
      manifest, and the §7.3 override installed into
      `credentials/policies/rotation-policy.yaml`.
      **VERIFIED:** `scripts/validate-avatar-client.py --strict` green with
      the new `check_broker_credential_binding` rule, and the binding
      validates against
      `contracts/schemas/xfactory-credential-contracts.schema.yaml` with zero
      errors.
- [ ] 6.1.2 Provision the DEDICATED spend-capped internal-live provider
      project, distinct from the F0 lab project, with its project budget and
      rate controls set BEFORE any live trial (the F0-proven pattern).
- [x] 6.1.3 Wire the session hard-kill onto the EXISTING duration/quota
      terminal outcome plus kill switch plus lease revocation — no new
      terminal is invented — and give a cost-triggered kill an auditable
      reason distinguishable from an ordinary duration or quota terminal.
      **Done 2026-08-27** in the reference runtime:
      `xfactory/avatar_runtime/spend.py` plus the wiring on
      `runtime.enforce_session_ceilings`, proven by
      `tests/avatar_runtime/test_session_hard_kill.py` (16 tests).
      NOTHING WAS INVENTED AT EITHER END. The three ruled ceilings are read
      back from `canary-cohort-and-rollback-policy.yaml` ROLLBACK-B
      `elevated_quota_condition` by
      `tests/avatar_runtime/test_ruled_values_pinned.py`, so 900 s, 300
      billable units, $3.00 and `uncountable_is: exhausted` are a checked
      mirror rather than a second source. The terminal is the kernel's own:
      `REASON_OUTCOMES` maps every ceiling reason onto `QUOTA_EXCEEDED` or
      `DURATION_EXCEEDED` and onto nothing else, and the closed `OutcomeCode`
      and `AttemptStatus` registries are UNCHANGED — not one member added.
      The act is the LANDED consent-withdraw-mid-speech path, now factored out
      as `AvatarRuntime._terminate_media_leg` and shared by four callers (the
      kill switch, the lease-expiry terminal, this hard-kill and ROLLBACK-A)
      rather than four lookalikes: lease revoked, idempotent provider hangup,
      terminal attempt status, credential-free grant-cache terminal.
      **THE AUDITABLE REASON, and where it had to live.** The closed
      `OutcomeCode` registry has no reason slot and widening it would widen a
      released closed registry, so the reason rides the two shapes the runtime
      already had for one: `TelemetryRecord.reason` (`reason` is an
      allowlisted stable telemetry key, so the record passes redaction and is
      published rather than dropped) and the new credential-free
      `SessionSpendRecord`. A cost kill reads `cost_ceiling_exceeded` or
      `cost_uncountable`; the ORDINARY cap terminal in the broker now publishes
      `ordinary_quota_exceeded` / `ordinary_duration_exceeded` on the same
      shape, so the test asserts the same `OutcomeCode` carrying two different
      reasons — which is the whole of what "distinguishable" means here.
      `uncountable_is: exhausted` is treated as COST-triggered by ruling: a
      broker that refuses because it cannot count is containing spend, not
      enforcing a quota. Precedence is stated rather than left to evaluation
      order (uncountable, then cost, then duration).
- [x] 6.1.4 Wire asynchronous usage metering and threshold alerting for
      per-tenant visibility.
      **NOW DONE 2026-08-27** — `xfactory/avatar_runtime/metering.py`,
      `scripts/avatar-metering-alert.py`,
      `contracts/avatar-client/usage-metering-and-alerting.yaml`, proven by
      `tests/avatar_runtime/test_usage_metering.py` (25 tests). The note below
      records what this task no longer had to decide when it was built; it is
      kept because it is the reason the wiring needed no invention.
      **ASYNCHRONOUS BY CONSTRUCTION, NOT BY PROMISE.** Every counter is a
      pure function over CLOSED `SessionSpendRecord`s, and neither `broker.py`
      nor `runtime.py` imports the metering module — a metering call cannot
      appear in the dispatch path of a module that cannot see it. The test
      parses both dispatch modules with `ast` and asserts the absent import
      rather than trusting a docstring. The per-SESSION ceilings stay
      synchronous in the broker, as §7.2 ruled; only the per-TENANT view is
      asynchronous.
      **THE MARKS AND THEIR CHANNELS.** Both figures are evaluated at 50%,
      80% and the budget itself. The project's 50%/80% ($375/$600) route to
      the provider's own native notifications and the cap to the provider's
      hard stop — both RECORDED as install-side halves owned by 6.1.2 and
      neither faked here; nothing in this repository emits them. The
      per-tenant crossing of $150 and ANY cost-triggered session kill route to
      `gh issue create` on the doc-health pattern. The tenant 50%/80% marks are
      computed and RECORDED but not paged: §7.4 rules the gh-issue channel at
      the budget itself, and firing at 50% would be a trigger nobody ratified.
      They are still computed because they are the telemetry ROLLBACK-C's
      `cost_concern` judgment is read off.
      **THE PATTERN IS MIRRORED, NOT APPROXIMATED.** One issue per run, title
      `avatar internal-live metering <YYYY-MM-DD>`, superseded by a STRICTLY
      OLDER date comparison so a run can never close its own issue — the
      doc-health rule verbatim, and the split is doc-health's too: the Python
      half computes and writes the body, a job step runs
      `gh issue create --body-file`. THE JOB STEP IS DELIBERATELY NOT
      COMMITTED. The metering job has no input until 6.1.2 provisions the
      serving install, and a scheduled workflow reading nothing would be the
      fabricated procedure the §7.7 runbook refuses to write for the
      kill-switch command. Recorded as the outstanding half, with §7.4's
      "at least one alert observed DELIVERED end to end" left
      `not_yet_delivered` rather than quietly satisfied by a unit test.
      **THE RECIPIENT IS READ, NEVER COPIED.** `build_alert` takes the
      recipient and the runbook as arguments and RAISES
      `AlertRecipientUnresolved` without them; the script reads both from
      `canary-cohort-and-rollback-policy.yaml` `operator_surface.holder` and
      `mechanism_ref` at run time. The holder's name appears nowhere in
      `xfactory/avatar_runtime/`, in code or in prose, and a test greps the
      whole package for it — an alert with no named recipient and a kill
      switch with no named holder were one gap seen twice, and a second copy
      of the name is how it would re-open.
      **What it no longer had to decide:** §7.4 was RULED 2026-08-27, so this
      task had its channel,
      its thresholds and its page target rather than having to invent them
      while building. Two channels, neither of which builds new
      infrastructure: the provider project's own native budget notifications
      at 50% and 80% of the §7.2 project cap, and `gh issue create` from the
      metering job following the doc-health pattern verbatim (one issue per
      run, supersede-and-close the prior) on a per-tenant metered crossing of
      $150/month or any cost-triggered session kill. The page target is the
      §7.7 kill-switch holder, and §7.7 was RULED later the same day, so this
      task inherits a NAMED PERSON rather than the role §7.4 first recorded:
      read the recipient from
      `canary-cohort-and-rollback-policy.yaml` `operator_surface.holder`,
      never from a copy. The metered per-tenant crossing also has its subject
      now — §7.10 rules tenant = cohort member, so this job meters two
      tenants — and the runbook the alert escalates into is
      `docs/sops/avatar-internal-live-kill-switch.md`.
- [ ] 6.1.5 DEFERRED, NOT BUILT: the durable synchronous per-tenant
      cumulative-spend counter. Record it as `avatar-pilot-hardening`'s work
      and record the resulting limit — the provider-project cap is the only
      per-tenant hard stop until it lands — as a stated property of this ring.

### 6.2 Consent and evaluation audio (F4 Option C)

- [x] 6.2.1 Build the SYNTHETIC evaluation corpus for the model-versus-model
      safety, exact-value, consent, handoff and blocked-state scenarios across
      generic, MedxFactory and LedgerxFactory.
      **Done 2026-08-27** in
      `contracts/avatar-client/synthetic-evaluation-corpus.yaml`, machine-checked
      by `check_synthetic_evaluation_corpus`. THIS IS THE CORPUS §6.3.3 NAMED
      AND DID NOT HAVE: `detection.py` records
      `SAFETY_CORPUS_OWNER = "qualify-avatar-live-voice 6.2.1"` beside a
      `SafetyEvalSignal` seam wired fail-closed BECAUSE no corpus existed, and
      every scenario here declares the signal its FAILURE emits.
      **35 SCENARIOS, AND THE COUNT IS DERIVED RATHER THAN CHOSEN.** Floor:
      every one of the 5 x 3 = 15 class x domain cells carries at least one
      scenario, because a cell with none is a condition-7 claim with no
      evidence. SAFETY takes four per domain (12) because ROLLBACK-A gives that
      class FOUR distinct triggers and no umbrella one — there is no
      `failed_safety_evaluation`, so `revocation_bound_violation`,
      `redaction_finding`, `secret_scan_finding` and
      `media_authorization_ordering_violation` ARE the safety class, and
      probing one per domain would leave three ratified triggers unreachable
      from that domain. CONSENT takes the kernel's own pair per domain —
      consent absent at request time, and withdrawal DURING an active media leg
      — plus one each for the two DomainxFactories probing the optional
      stricter domain purpose reference, which the generic domain has nothing
      to be stricter about (8). EXACT-VALUE and BLOCKED-STATE take two per
      domain (6 each): a character-exact readback plus the kernel-named
      supersede-correction edge, and entering a blocked state plus the
      denial-versus-failure distinction in the FALSE-POSITIVE direction.
      HANDOFF takes ONE per domain (3), deliberately — one trigger, one
      kernel-named fixture, and the handoff-carries-no-secret failure it would
      otherwise duplicate is already the safety class's `secret_scan_finding`
      scenario per domain. The asymmetry is recorded rather than levelled by
      inventing a scenario.
      **§7.6's "15 classes x 3 = 45" IS SESSIONS, NOT SCENARIOS**, and the 15
      it counts are exactly these cells — so the corpus's structure IS the
      denominator §7.6 already assumed and its session floor is satisfiable
      against it. Nothing was padded to 45.
      **EVERY FAILURE MAPS TO A RATIFIED TRIGGER, READ FROM THE POLICY.** The
      check resolves each scenario's trigger against
      `canary-cohort-and-rollback-policy.yaml`'s own ROLLBACK-A list rather
      than a constant in the validator, so narrowing the policy invalidates the
      corpus rather than the two copies agreeing with each other. All EIGHT
      triggers are reachable; an unreachable one fails, because §6.3.3 proved
      the trip for all eight. An invented trigger would be answered by
      `evaluate_safety_signal` with `REFUSED_UNKNOWN_TRIGGER` — a NON-tripping
      verdict — so a mis-specified scenario would report a failure and NOT
      abort the ring, which is why the check refuses one rather than warning.
      **SYNTHETIC IS A FIELD, NOT A PROMISE:** `content_origin: scripted`,
      `tenant_data: none`, `real_utterances: none`, all compared. The exchanges
      are TEXT-LEVEL and say so — rendering a script to audio is a §5-time and
      canary-time act of the RUN, and committing rendered audio would commit
      media into a ring whose `audio` retention class stays forbidden.
      **ONE HONEST LIMIT RECORDED IN THE ARTIFACT:** no MedxFactory or
      LedgerxFactory avatar profile exists in this repository — the kernel's
      overlay material is domain-NEUTRAL by design (`domain_factory_repo:
      DomainxFactory`) and the archived `adopt-avatar-client-lab-candidates`
      records the patient-intake demo pack as "its own change". The domain
      framing is therefore drawn from the RECORDED Hermes layer names in
      `examples/pre-run-simulations/{medx,ledgerx}.yaml` and the kernel's own
      generic intake fixture family, with `domain_grounding_caveat` saying so,
      so a landed domain profile refines these scripts rather than discovering
      they pre-empted it.
- [x] 6.2.2 Define the canary's ephemeral processing envelope: consent rides
      the existing `avatar.media_capture` and `avatar.provider_processing`
      purposes plus an optional stricter domain purpose reference; captions
      and deltas are `ephemeral_presentation`; decisions, consent versions and
      outcomes are `structured_record`; withdrawal maps to the existing
      revoked outcome and stays reachable mid-session.
      **Done 2026-08-27** in
      `contracts/avatar-client/canary-ephemeral-processing-envelope.yaml`,
      beside the canary policy and on its conventions, machine-checked by
      `check_ephemeral_processing_envelope`. Fork 4 Option C's sentence has
      lived as prose in a memo and as three ruled fields on checklist condition
      2; this is the envelope itself — which consent the canary rides, which
      data class each ARTIFACT of a live leg falls into, how long the one
      retained class lives, and how a person gets out mid-session.
      **THE TWO TRUE SENTENCES ABOUT THE PURPOSES ARE RECONCILED, NOT CHOSEN
      BETWEEN.** This task names TWO purposes; the promoted requirement names
      THREE. Both are right about different things and the envelope records
      which: the MEDIA LEG rides `avatar.media_capture` and
      `avatar.provider_processing`, and a produced `structured_record` rides
      `avatar.structured_record`. All three are pre-existing frozen members,
      `new_purposes_introduced: 0`, and the count is RECOMPUTED from the
      registry rather than mirrored — growing the registry makes the envelope's
      number wrong.
      **THE OPTIONAL STRICTER REFERENCE IS OPTIONAL TO DECLARE AND NEVER
      OPTIONAL TO SATISFY.** An unresolved one DENIES; it is never downgraded
      to the neutral pair, because a request that asked for a stricter term and
      could not get it has not obtained the consent it asked for. A reference
      is not a registry member, which is exactly why the ruling admits one
      rather than a fourth purpose — the frozen count is untouched by it.
      **RETENTION IS CITED, NOT RESTATED.** The 90-day window and the named
      reference `avatar.internal_live.canary.structured_record.retention.v1`
      are READ from the checklist's §7.9 `ruled_values.retention` and compared,
      so the two artifacts cannot drift; `ephemeral_presentation` carries no
      window because it carries no retention.
      **WITHDRAWAL'S MID-SESSION REACHABILITY IS PROVED, NOT ASSERTED.** It
      maps onto the EXISTING `revoked` outcome (`new_outcome_tokens_introduced:
      0`, resolved against the closed registry), and the reachability proof is
      the landed fixture
      `examples/avatar-first-ui/fixtures/deterministic/consent-withdraw-mid-speech.yaml`
      (`det-consent-withdraw-mid-speech`, AFU-006-S03), which delivers the
      authoritative `revocation` AFTER `transcript_segment` — i.e. while the
      avatar is SPEAKING — and expects `media_state: revoked`,
      `capture_active: false`, `governed_commands_enabled: false` with
      `control_state: healthy`. The validator RESOLVES that fixture on disk and
      compares its `fixture_id`, so the citation cannot become a filename
      nobody wrote. `control_state: healthy` is load-bearing: a withdrawal is a
      clean authored terminal, not a `blocked` safety trip, so a subject who
      withdraws is not shown a failure they did not cause.
- [x] 6.2.3 CONFIRM UNTOUCHED, by inspection rather than assertion: the four
      reserved retention classes stay forbidden, `local_persistence` stays
      const false, and the frozen consent-purpose count stays 3.
      **Done 2026-08-27** in
      `openspec/changes/qualify-avatar-live-voice/review/reserved-surface-inspection-2026-08-27.md`
      — a dated `Status: record` review-style record where this change keeps
      evidence, with file-and-line citations at this branch's tree.
      **"BY INSPECTION RATHER THAN ASSERTION" RULES OUT BOTH EASY
      DISCHARGES** — writing "confirmed" in a tick, and adding a test and
      calling the test the confirmation. A test proves the state at the moment
      it runs; what 6.2.3 asks is whether THIS CHANGE TOUCHED these surfaces,
      which is a question about a diff and is answered by looking. So the
      record walks each claim to its line: the four reserved classes at
      `registries/retention-classes.registry.yaml:13-17`, the closed active
      enum at `avc-07-retention-profile.schema.yaml:13-17`, the freeze at
      `interface-lock.yaml:39`; `local_persistence: {const: false}` at
      `avc-07-retention-profile.schema.yaml:21` — `const`, not `default`, and
      this change authors no AVC-07 instance at all; the three frozen purposes
      at `registries/consent-purposes.registry.yaml:9-12` and
      `shared-definitions.schema.yaml:37-43`, pinned twice independently at
      `interface-lock.yaml:21` and `validate-avatar-client.py:133`. Every one
      of those files is UNMODIFIED by this branch.
      **ONE OBSERVATION RECORDED RATHER THAN SMOOTHED OVER.** §7.9's
      `classes_never_instantiated` names THREE, not four — `video` is absent —
      and the validator's own comment says so. That is not a defect: the §7.9
      list is the ring's canary-audio DATA CLASSES and `video` is absent
      because the ring has no video capability, while the RESERVATION of
      `video` is intact at the registry and the enum, which is the level this
      task asks about. The two lists are deliberately not merged and neither is
      edited; the envelope names all four because the promoted requirement
      does, and its check compares that block against the REGISTRY's reserved
      set.
      **BELT-AND-BRACES WENT WHERE A CHECK DID NOT ALREADY EXIST.** The count
      freeze (`EXACT_COUNTS`) and the registry/schema parity already run, so
      nothing was added there. What did not exist is a guard on the two NEW
      artifacts re-stating these facts wrongly, and that is what
      `check_ephemeral_processing_envelope` adds: the purpose count recomputed
      from the registry, the never-instantiated list compared to the registry's
      reserved set, a permitted-reserved class refused.
- [x] 6.2.4 Record the non-shadowing guarantee as an OPERATIONAL control with
      the enforcing contract flag named as pilot-hardening work — no schema
      field forbids a second-model shadow today, and claiming otherwise would
      be false.
      **Done 2026-08-27** as `OPC-01` in
      `canary-ephemeral-processing-envelope.yaml` `operational_controls`.
      Exactly ONE model processes live canary audio and consented audio is
      never shadowed, mirrored, teed, forked or replayed to a second model —
      recorded with `enforced_by_schema: false` in a FIELD, `enforcement:
      operational`, and `enforcing_contract_flag: {status: deferred,
      owner_change: avatar-pilot-hardening}`.
      **THE FALSE CLAIM IS NAMED SO IT CANNOT BE MADE BY ACCIDENT.** AVC-09
      carries ONE `requested_model` and ONE `provider_resolved_model`, which
      describes the adapter's own resolution and does not — cannot, as written
      — forbid a broker opening a second provider leg beside the first. A
      reader inferring enforcement from the singular field would be inferring
      something the schema does not say, so the control says it instead.
      **AND THE CLAIM IS MUTATION-GUARDED**, because flipping
      `enforced_by_schema` to `true` is the kind of edit that looks like an
      improvement: `test_claiming_the_schema_forbids_a_shadow_is_caught` fails
      on it, and two siblings fail on an unnamed or already-built enforcing
      flag. `OPC-02` records the out-of-class retention control on the same
      discipline, and is honest that it is only PARTIALLY structural — the
      AVC-07 enum refuses a reserved class in a retention profile, but no
      schema forbids a component retaining audio without authoring a profile
      at all.
      The corpus does NOT claim to prove this: no corpus scenario can prove a
      negative about infrastructure it does not observe, and
      `not_this_corpus.second_model_shadow` says so and leaves the guarantee
      where it honestly sits.

### 6.3 Canary and rollback (F5 Option B)

- [x] 6.3.1 Define the cohort: vendor-organization internal accounts plus
      exactly ONE internally-staffed domain sandbox, synthetic or
      internally-consented audio only, no real external tenant. Opt-in is
      server-side capability resolution against an allowlist with the
      per-session opt-in recorded in the AVC-01 request context — not a
      client-visible toggle.
      **Done 2026-08-27** in
      `contracts/avatar-client/canary-cohort-and-rollback-policy.yaml`
      (`cohort:`). Two members: COHORT-01 the vendor organization's internal
      accounts, COHORT-02 the internally-staffed domain sandbox carrying
      `cardinality: exactly_one` as a checked field rather than as prose,
      because "exactly one" is the ruled boundary and not a starting point a
      canary operator may widen. Audio is synthetic or internally-consented
      only; `external_tenants.admitted: false` with the refusal routed to the
      pilot ring, which owns data-handling review and real-tenant scale
      (ALV-008-S05). Opt-in is `server_side_capability_resolution` against the
      internal allowlist with the per-session record in the AVC-01 request
      context and `client_visible_toggle: false` — a client toggle would move
      cohort membership to the client where it can be neither enforced nor
      audited. The §7.10 "tenant" definition is recorded `status: unset` with
      the note that it MUST agree with this cohort or the per-tenant spend and
      metering dimensions have no subject; recorded open rather than assumed.
      **§7.10 RULED later the same day**, and it agrees with this cohort by
      construction: TENANT = COHORT MEMBER, so the two members above ARE the
      two tenants. `tenant_definition_ref` now reads `status: set`, and the
      validator recomputes its `tenant_count` from `cohort.members` rather
      than trusting the recorded 2 — if this cohort ever widened by ruling,
      the tenant count could not quietly stay behind.
- [x] 6.3.2 WRITE the revoke-versus-block policy the kernel requires and has
      never had, in its ratified three-way split: safety/integrity breaches
      auto-abort WITH active-lease revocation; latency-budget and elevated
      error/quota breaches auto-block-new and let in-flight legs drain;
      quality/cost breaches are operator-triggered.
      **Done 2026-08-27**, same artifact (`rollback_policy:`). This is the
      document `avatar-client-runtime`'s kill-switch scenario has pointed at
      since the kernel was written — "revoke affected active leases ACCORDING
      TO THE RECORDED POLICY" — and which Fork 5 recorded as never actually
      written; until now "optional revocation" had no rule selecting the
      option, leaving revoke-everything and revoke-nothing equally defensible.
      The three-way split is encoded with its triggers: ROLLBACK-A (automatic,
      abort, `revoke_active_leases: true`) on a revocation-bound violation, a
      failed blocked-state / exact-value / consent / handoff evaluation, a
      redaction or secret-scan finding, or a media-authorization ordering
      violation — reusing the landed consent-withdraw-mid-speech terminal path
      rather than inventing a terminal; ROLLBACK-B (automatic, block_new,
      `revoke_active_leases: false`) on a material regression against
      ALV-SLO-001 or an elevated error or quota condition, letting in-flight
      legs drain; ROLLBACK-C operator-triggered for quality and cost judgment.
      ROLLBACK TARGET, per 6.3.4's constraint binding this copy even though
      6.3.4's implementation is later: `disable_voice_to_text_or_human_handoff`
      with `model_fallback_exists: false` and an explicit binding note that no
      sentence here may let a reader infer a hot-swap — `gpt-realtime-2.1` is
      the first qualified profile and there is nothing to swap to.
      `abort_scope.ends: media_plane_only` with the authority-owned workflow
      projection and policy-required records surviving (ALV-008-S04). The
      §7.7 operator surface is recorded `status: unnamed` and the §7.8 outcome
      tokens `partially_bound` — only consent and lease revocation is
      fixture-bound to `revoked` today, so the drained-leg and
      force-terminated-leg tokens are left OPEN rather than guessed.
      `check_canary_rollback_policy` machine-checks the split and its revoke
      flags; the mutation that flips ROLLBACK-B's flag to true — which would
      cut people off mid-conversation on a performance regression and spend the
      safety mechanism on a latency problem — is caught.
      **BOTH OPEN RECORDS CLOSED later the same day** by §7.7 and §7.8, so
      this artifact no longer carries an open field: `operator_surface` reads
      `status: named` with Brett Heap as holder and the runbook at
      `docs/sops/avatar-internal-live-kill-switch.md` as `mechanism_ref`, and
      `session_outcome_tokens` reads `status: bound` with all three paths
      mapped — drained leg `abandoned` (or `completed` on a natural terminal),
      force-terminated leg `revoked` on the same consent-withdraw path
      ROLLBACK-A's `mechanism` already names. ROLLBACK-A and ROLLBACK-B carry
      their own `session_outcome` and the validator compares the two copies,
      so a class cannot promise one terminal while the policy binds another.
      6.3.3's auto-detection wiring is NOT built by this task and is left
      unticked; the policy names §6.3.3 as its `detection_wiring_owner`.
- [x] 6.3.3 Build the auto-detection wiring the policy needs — the latency
      trip off §5's SLO and the safety-eval trip off §6.2.1 — since Option B
      was chosen precisely for this rehearsal value.
      **Done 2026-08-27** in `xfactory/avatar_runtime/detection.py`, fired
      through `runtime.latency_detection` and `runtime.safety_detection`,
      proven by `tests/avatar_runtime/test_rollback_detection.py` (36 tests).
      This is the wiring the policy names itself as waiting for:
      `detection_wiring_owner: qualify-avatar-live-voice 6.3.3` on both
      automatic classes.
      **THE LATENCY TRIP fires ROLLBACK-B** — auto-block-new, in-flight legs
      drain — on a material regression against ALV-SLO-001, evaluated at p50
      AND p95, using the ruled `greater_of` rule unchanged (`adapter >
      reference + max(0.15 x reference, 150)`). THREE REFUSALS STACK, and each
      one means "does not trip": a cell outside the gated set (platform,
      `network_class: nominal`, the two gated intervals) is
      `refused_not_a_gated_cell` with its numbers still recorded — the refusal
      attaches to the CLAIM of the gated tier, not to the cell, exactly as the
      map's own note requires; a cell holding fewer than the DECLARED n>=100
      is `recorded_not_gated_under_minimum` and NEVER trips, on either side of
      the comparison, because at n=30 a p95 estimate is a maximum wearing a
      percentile's name and auto-blocking a ring on one would be auto-blocking
      on noise; an incomplete or cross-region comparison is refused rather
      than pooled. The percentile is nearest-rank and non-interpolating, so
      two readers cannot disagree about whether a gate tripped.
      **THE SAFETY-EVAL TRIP fires ROLLBACK-A** — auto-abort WITH active-lease
      revocation through the landed consent-withdraw terminal path, proven for
      all EIGHT recorded triggers.
      **§6.2.1's CORPUS DOES NOT EXIST, so what is built is the INPUT SEAM.**
      `SafetyEvalSignal` is the shape a §6.2.1 run will feed — `run_id`,
      `corpus_ref`, `scenario_class`, `trigger`, `verdict` — and the module
      names `SAFETY_CORPUS_OWNER` rather than implying a corpus is there. The
      seam is wired FAIL-CLOSED IN THE DETECTOR'S DIRECTION: an absent signal,
      a malformed one, a foreign object, an unparseable verdict and an
      unrecognised trigger each return a distinct NON-tripping verdict, and a
      parametrised test drives all six cases and asserts that no lease was
      revoked and no new session was blocked. `REFUSED_ABSENT` is deliberately
      a different value from `NO_TRIP_PASSED`: "no evaluation arrived" is a
      canary gate condition, not a green light, and collapsing the two would
      let an unrun evaluation read as a passed one. Revoking live leases on a
      parse error would spend the safety mechanism on a data problem.
- [x] 6.3.4 Implement rollback as disable-voice into text or human handoff.
      `gpt-realtime-2.1` is the FIRST qualified profile, so no model fallback
      exists and none may be implied in copy or code.
      **Done 2026-08-27** in `xfactory/avatar_runtime/rollback.py`, proven by
      `tests/avatar_runtime/test_rollback_target.py` (16 tests). The act is the
      EXISTING kill switch and nothing else: a `RollbackDecision` resolves to a
      `KillSwitchState`, and the scope follows the runbook's own selection rule
      — `SWITCH-PROFILE` unless the condition is not specific to the candidate
      profile, `SWITCH-ALL-NEW` being the wider blast radius. The mode is the
      policy, not the operator's mood: A and B carry their ruled flags and
      refuse an override, and ROLLBACK-C REFUSES TO DEFAULT — the operator must
      state the choice, because revoke-everything and revoke-nothing were the
      two equally defensible readings this policy exists to settle. The
      session-creation path answers a withdrawn profile with a credential-free
      `killed` terminal plus a `RollbackPosture`: `voice_enabled: false`,
      offered modes `text` and `human_handoff` (both released `fallback-modes`
      registry members), `model_fallback_exists: false` and
      `qualified_profiles_remaining: ()`.
      **THE COPY CONSTRAINT IS ENFORCED ON THIS CHANGE'S OWN SOURCE.** A test
      greps every `.py` in `xfactory/avatar_runtime/` for the phrasings that
      would leave a reader expecting a swap — a fall-back-to-another-model
      sentence, a truthy `model_fallback`, a hot-swap, a "previously qualified
      profile". It caught one occurrence in this slice's own prose and that
      line was rewritten, which is the only evidence worth having that the
      guard is live rather than decorative. `qualified_profiles_remaining` is
      empty because there is no other qualified profile in existence, not
      because one is switched off, and the posture says so in a shape a caller
      can read rather than only in prose.
- [x] 6.3.5 Prove that an abort ends the media plane only: the logical
      session's authority-owned workflow projection and its policy-required
      records survive, reusing the landed consent-withdraw-mid-speech terminal
      path.
      **Done 2026-08-27** — `xfactory/avatar_runtime/projection.py` makes the
      two planes separately addressable, and
      `tests/avatar_runtime/test_abort_scope.py` (7 tests) is the proof.
      **THE CLAIM IS TURNED INTO BYTES.** A session is driven to authorization
      (appending the authoritative `media_authorized`), given an accepted
      governed command so its projection carries real state, then aborted
      under ROLLBACK-A. The assertion is not "the projection still exists" but
      `serialize()` and `digest()` IDENTICAL either side of the abort, with a
      negative control appending one authoritative event and asserting the
      digest moves — so the byte-intactness claim is not vacuous. The event
      log is asserted untouched, a second session's projection is asserted
      byte-intact across another leg's abort, and the logical session is shown
      still `ACTIVE` with its epoch, revision, policy version and consent
      version unmoved.
      **IT HOLDS STRUCTURALLY, NOT BY PROMISE.** The shared termination act
      touches media state only — lease, provider call, attempt status, grant
      cache — and appends nothing to the event log, so there is no path from
      an abort to the projection to test for. That is why the audit reason
      rides telemetry and the spend record rather than an authoritative event:
      an abort that wrote its own reason into the workflow projection would
      have falsified `abort_scope.ends: media_plane_only` in the act of
      recording itself.
      **THE RECORDS ARE APPEND-ONLY ACROSS AN ABORT**, so the test asserts the
      pre-abort authoritative events are UNCHANGED and the pre-abort terminals
      and spend records are a SUBSET of the post-abort set — retention, not
      byte-freezing, which is the honest reading of "policy-required records
      survive".
      **BOTH RULED MAPPINGS ARE EXERCISED.** ROLLBACK-A emits `revoked` on the
      force-terminated path — media revoked, capture stopped, credential-free
      terminal, held answer and control descriptor erased, control channel
      healthy — reusing the consent-withdraw path exactly. ROLLBACK-B leaves
      the in-flight leg alone (not terminal, lease active, provider still
      live) while refusing new work, and then: `abandoned` when the drain
      window closes on a leg still in flight, `completed` when the leg reached
      its own natural terminal inside the drain, with a closing window
      refusing to relabel a finished leg. Every token emitted is a member of
      the released closed `session-outcomes` registry — a test enumerates the
      whole terminal cross-product and checks membership — and `TIMED_OUT` and
      an unqualified `TERMINATED` map to None rather than to a guess, because
      a token inferred after the fact is how two readers count the same event
      differently.

### 6.4 The `openAvatar` extraction (latent decision 1)

> **RULED 2026-08-27 by Brett Heap (in-session, via AskUserQuestion) — option
> (a): recognize `openAvatar` as the extracted client.** §6.4.1 and §6.4.2 had
> been raised as MIS-SPECIFIED AGAINST THE WORLD and were not executed pending
> that ruling. The three rulings recorded here:
>
> * **R1.** The Flutter client repo KEEPS the name **openAvatar** — it already
>   IS the extracted client. Canon's `xfactory-avatar-client` name predates
>   openAvatar becoming a first-class product and is AMENDED to `openAvatar`
>   throughout `repo-boundary-governance`, `avatar-client-lab`, and this
>   change's deltas.
> * **R2.** **`openAvatar-server`** is RECORDED AS THE NAMED FUTURE HOME for
>   deployable avatar server code. The repository is created only by whichever
>   change first ships deployable server code — not now.
> * **R3.** The parked empty `opensoft/xfactory-avatar-client` repository was
>   DELETED 2026-08-27; nothing referenced it.
>
> **Two live occurrences of the old name are deliberately NOT renamed here.**
> `contracts/manifest.yaml` and `contracts/avatar-client/evidence-register.yaml`
> each carry `xfactory-avatar-client` in prose, and both are published,
> digest-bearing release artifacts — the evidence register is additionally a
> `manifest_cross_checked` member of openAvatar's `contract_pin.yaml`. Renaming
> their bytes outside a bundle cut would invalidate the published
> `contract-v1.46`/`contract-v1.47` digest inventories and the client pin. They
> are renamed when this change's realization cuts the next additive bundle
> (§2). Separately, the archived
> `2026-07-13-define-avatar-client-contract-kernel` change, this change's
> `.openspec.yaml` origin record, `supporting-docs/source-snapshots/`, the body
> of `supporting-docs/fork-decision-memo.md`, and
> `specs/001-avc-contract-kernel/` are dated RECORDS: they keep the name they
> were written with and carry dated amendment notes instead.
>
> The facts the ruling was made on, verified against the live remotes rather
> than inferred:
>
> 1. **codexFactory `apps/avatar-client-lab/` does not exist.** It was deleted
>    in full on 2026-08-03 by codexFactory `2b79da35` ("Shed the avatar client
>    lab to opensoft/openAvatar (DTN-022)", PR #74) — 240 files, ~22.9k lines
>    of Dart, and `apps/` went with it. codexFactory `main` today contains
>    ZERO `.dart` files and no `pubspec`. There is nothing at that path to
>    extract. What remains is `specs/002-avatar-client-lab/`, deliberately kept
>    as frozen Speckit evidence.
> 2. **The extraction §6.4.1 describes has already happened**, under Brett's
>    own DTN-022 ruling of 2026-08-03 — but to a DIFFERENTLY NAMED repository.
>    `opensoft/openAvatar` (private) carries the lab with FULL subtree-split
>    history (codexFactory `main@25e46fd1` -> openAvatar `main@1998dcf8`), is
>    actively developed (154 Dart files, melos packages `app`, `avatar_view`,
>    `avc_contracts`, `avc_session`, `avc_adapters_fixture`, `ui_kit`,
>    `golden_config`), and is ALREADY pinned into the xFactory aggregation at
>    `xFactory@6a2f418`. The DTN register records this as `adopted`:
>    "DTN-022 | Avatar client lab neutral home | own repo `opensoft/openAvatar`
>    (ruled 2026-08-03); domain descendants are pin-and-profile distributions".
> 3. **`opensoft/xfactory-avatar-client` existed and was PARKED — and is now
>    DELETED.** It was created 2026-07-14 as task 1.1 of
>    `implement-avatar-client-lab`, then parked the same day when Brett
>    redirected the lab's code surface to codexFactory. Its README said so, and
>    it held no code. Under R3 it was deleted 2026-08-27;
>    `gh api repos/opensoft/xfactory-avatar-client` now returns 404.
>
> **Why this was not worked around.** Creating a fresh repo and copying
> openAvatar's tree into it would FORK a live product line — precisely what
> this change's own `avatar-client-lab` delta forbids in the scenario it added
> (pre-amendment wording): "the application and its generated bindings MUST
> move to `xfactory-avatar-client` RATHER THAN BEING FORKED". It would orphan the
> history DTN-022 deliberately preserved, duplicate a repository already
> admitted to the aggregation, and strand `MedxAvatar` and `LedgerxAvatar`,
> which are pin-and-profile distributions OF openAvatar. The tasks preamble is
> explicit that "a task that appears to require re-opening [a ruled decision]
> is mis-specified" — and §6.4.1 as written cannot be executed without
> re-opening DTN-022.
>
> **The substance of latent decision 1 is already satisfied.** openAvatar is
> private, independently releasable, holds no provider key, no server tool
> handler and no server provider configuration, and consumes neutral contracts
> read-only through a digest pin. What `repo-boundary-governance` "Neutral
> avatar-client repository boundary" requires of the client repository is true
> of openAvatar today; what is false is only the NAME the requirement records.
>
> **The ruling was needed** (Brett's, not an implementer's) on which of these
> the canon should say — a naming and governance question with no code in it
> either way. The two options put to him on 2026-08-27 were:
>
> * **(a) Recognize openAvatar as the extracted client.** Amend
>   `repo-boundary-governance` and this change's §6.4 to name
>   `opensoft/openAvatar`, record DTN-022 as the act that performed the
>   extraction, and archive or re-point the parked `xfactory-avatar-client`.
>   §6.4.2's pin work then lands in openAvatar as a resync (see below). This
>   matches the world and needs no repository surgery.
> * **(b) Rename `opensoft/openAvatar` to `xfactory-avatar-client`**, keeping
>   history, and re-point the aggregation pin and the two descendant repos.
>   Preserves the canon's chosen name at the cost of a rename touching three
>   other repositories.
>
> **Brett ruled (a).** The canon is amended, DTN-022 is recorded as the act
> that performed the extraction, and the parked repository was deleted rather
> than re-pointed (R3). `MedxAvatar` and `LedgerxAvatar` remain
> pin-and-profile distributions OF openAvatar, untouched.
>
> §6.4.5 was also implicated: it forbade admitting the client repository to the
> aggregation in this change, but openAvatar is ALREADY admitted under its own
> name by a separate act — consistent with §6.4.5's intent, inconsistent with
> its pre-ruling letter. §6.4.5 below is re-worded to state the existing
> membership as fact.
>
> **§6.4.2 was blocked only on which repo it targets, not on how — and is now
> unblocked.** openAvatar
> already carries the exact mechanism the task asks for: a committed
> `contract_pin.yaml` (`schema_version: 1`,
> `kind: avatar-client-lab-contract-pin`) recording bundle, exact 40-hex
> openxFactory commit and per-file sha256 per member, a `verify_pin` gate that
> fails closed on an empty or commit-less pin, a `sync_contracts.dart` baker
> and `docs/pin-resync-runbook.md`. It currently pins `contract-v1.7` and
> `contract-v1.8` at openxFactory `01960b13`, verified against
> `contract-v1.12`. The real §6.4.2 work is a RESYNC of that existing pin up to
> `contract-v1.46` at commit `046466a05590eff13819194f6ce4489798edd815`, taking
> the per-file digests from `contracts/manifest.yaml` at that pinned commit —
> the source the runbook mandates; the release inventory
> `contract-v1.46.digests.yaml` is a Hermes-runtime inventory covering none of
> the pinned client paths — executed through the runbook's sole sanctioned
> baker and landed as a PR on `opensoft/openAvatar`,
> the repo ruling (a) picked. That is a contained, well-understood follow-up.

- [x] 6.4.1 Create the private, independently releasable
      `openAvatar` repository and EXTRACT the app and its
      generated bindings from codexFactory `apps/avatar-client-lab/`. It
      holds no provider key, no server tool handler, no server provider
      configuration, and no unpinned copy of a neutral schema.
      **SATISFIED-BY-DTN-022 — RECORDED, NOT RE-DONE.** Provenance: Brett
      Heap's ruling R1 of 2026-08-27, made in-session via AskUserQuestion. The
      extraction was performed on 2026-08-03 by DTN-022 as a subtree split of
      codexFactory `apps/avatar-client-lab/` carrying full history
      (codexFactory `main@25e46fd1` → openAvatar `main@1998dcf8`) into the
      private `opensoft/openAvatar`. Verified against the live remote
      2026-08-27: the repository is private, its `main` is at
      `bc6462330b1c512c13b46eb49d821ab1f91e5137`, it holds no provider key, no
      server tool handler and no server provider configuration, and it
      consumes neutral contracts read-only through the digest-pinned
      `contract_pin.yaml`. Under ruling R3 the parked, empty
      `opensoft/xfactory-avatar-client` was DELETED 2026-08-27 — nothing
      referenced it, and the name now returns 404.
- [ ] 6.4.2 Resync `openAvatar`'s `contract_pin.yaml` to `contract-v1.46` at
      openxFactory commit `046466a05590eff13819194f6ce4489798edd815` — pinning
      the compatible openxFactory bundle tag plus exact contract
      commit and per-file digests; the co-checkout path reference allowed
      before this gate stops being sufficient at it.
      **RE-SCOPED 2026-08-27 under ruling R1** from "create a pin" to "resync
      the existing one": the mechanism already exists in
      `openAvatar/contract_pin.yaml` (today `contract-v1.7` + `contract-v1.8`
      at openxFactory `01960b13`, verified against `contract-v1.12`), so the
      work runs through `openAvatar/docs/pin-resync-runbook.md` and its
      `sync_contracts.dart` baker.
      **CROSS-REPO DEPENDENCY — this task is discharged by a PR in
      `opensoft/openAvatar`, not by anything in openxFactory.** It stays
      UNTICKED here until that PR merges.
- [ ] 6.4.3 Realize the live `avc_adapters_live` transport behind the
      existing fail-closed `SessionTransport` port with ZERO reducer or UI
      change, and instrument AVC-10 markers on the gated platforms.
- [ ] 6.4.4 Stand up release evidence per `repo-boundary-governance`
      "Avatar-client release evidence" — source revision, Flutter and platform
      versions, pinned bundle and digests, fixture conformance, dependency
      lock, secret scan, test evidence, client integrity (desktop signing or
      web deployment integrity/CSP), and rollback target.
      **BUILT 2026-08-28 in `opensoft/openAvatar` PR #6, branch
      `feat/release-evidence`. CROSS-REPO DEPENDENCY — discharged by that PR,
      not by anything in openxFactory, so it STAYS UNTICKED here until the PR
      merges**, on 6.4.2's own stated rule. That rule is load-bearing rather
      than ceremonial right now: 6.4.2 and 6.4.3 both MERGED upstream on
      2026-08-27 (openAvatar PRs #4 and #5) and are still unticked here, so
      ticking 6.4.4 off an unmerged branch would claim more for it than two
      landed siblings claim for themselves.
      The artifact is `openAvatar/release_evidence.yaml` (`schema_version: 1`,
      `kind: avatar-client-release-evidence`), standing beside
      `contract_pin.yaml` because it answers the same kind of question. It is
      GENERATED by `packages/avc_contracts/tool/gen_release_evidence.dart
      --generated-at=<ISO-8601>` and never hand-edited: every element carries
      the command that produced it, that command's exit code, its own verdict
      line verbatim, and a SHA-256 of its captured output. Generated against
      openAvatar `b7e89f2d`; `tree_facts_sha256`
      `656e2bb44409f7446069ed4258412234a7ef8e31a8217e7f9ad7bde74cf22550`.
      **EIGHT OF THE NINE ELEMENTS ARE SATISFIED BY A REAL RUN**, none by
      assertion: RE-01 source revision (git, worktree clean); RE-02 Flutter
      3.44.4 / Dart 3.12.2 / framework `ad70ec4617…`, declared in
      `toolchain.lock.json` + `.fvmrc` and confirmed by `flutter --version
      --machine` and `verify_toolchain`; RE-03 the pin — `contract-v1.7` +
      `contract-v1.8`, both at openxFactory
      `046466a05590eff13819194f6ce4489798edd815`, 68 bundle members + 3
      vendored evidence inputs = the 71 files `verify_pin` recomputes offline;
      RE-04 fixture conformance across six replays (36 schema cases / 12 AFUV
      negatives / 17 loader cases / 5 intake seeds / 4 AVC-09+AVC-10 documents
      / gate ix), gate ix recorded as `GREEN-WITH-TRACKED-GAPS` rather than
      rounded up; RE-05 dependency lock (93 packages, **0 unpinned sources**,
      7 sdk-sourced, enforced by CI's `flutter pub get --enforce-lockfile`);
      RE-06 secret scan — a REAL scan, 13 key-shape patterns over 435 files,
      **0 findings**; RE-07 test evidence — `melos run ci` green end to end on
      a Linux bench, **533 tests across 11 suites**, so the authoritative pixel
      goldens and the eleven accessibility capabilities EXECUTED rather than
      self-skipping; RE-09 rollback target machine-checked against the pinned
      `fallback-modes` registry — `text` and `human_handoff` are members and
      the closed set contains NO model-fallback member, matching 6.3.4's
      ruling that `gpt-realtime-2.1` is the first qualified profile and no
      swap exists or may be implied.
      **THE NINTH ELEMENT IS A NAMED BLOCKER, NOT A TRACKED GAP.** RE-08
      client integrity is recorded `not_yet_satisfiable` with
      `blocks_release: true`, and the artifact's own `verdict.release_gate`
      reads **BLOCKED**. This is what scenario RBG-002-S02 demands rather than
      a shortfall against it: when an internal-live client cannot prove desktop
      signing or web deployment integrity for the code enforcing disclosure and
      local media gating, release validation MUST FAIL, because the
      confidentiality trusted computing base is not established. The generator
      PROBES for both surfaces and records the probe list, so the finding is
      reproducible and the element flips automatically when material lands —
      both sets are empty today. **Desktop half: no code-signing certificate
      exists; owner Brett Heap, install-side, the same class of provisioning
      act as 6.1.2.** **Web half: no web deployment exists and its owner is not
      yet appointed** — `repo-boundary-governance` "Deferred aggregation and
      web-console integration" routes the production deployment home to this
      change's live-qualification successor, and openAvatar's web CI leg is a
      headless-Chrome SMOKE that ships nothing. Either surface discharges the
      element; the desktop path is the shorter one, needing a certificate
      rather than a decision about where the product lives.
      Two gates were added to `melos run ci` AND `ci-agnostic`, appended after
      the existing gates so no pre-existing guard, gate or test changes
      semantics or order — no gate was faked to have something to cite:
      `gate-secret-scan` (proven live rather than decorative on eight
      credential shapes and both fail-closed paths, 16 tests) and
      `gate-release-evidence-freshness`, which re-derives the TREE-DERIVED half
      of the artifact and fails when the committed record stops describing the
      tree or when any dependency resolves from a git or path source. The
      secret scan's exemption set is not a local decision: it READS the
      permitted bounded forms from the vendored digest-pinned
      `contracts/avatar-client/redaction/sentinels.yaml`, whose own text
      instructs the content scan to permit those exact strings and flag
      everything else, so widening it means moving a pinned digest.
      RING-02 note: this discharges the CLIENT half only. The broker
      deployment's secret scan is install-side and is not touched here.
      Out of scope by the requirement's own carve-out, and correctly absent:
      SBOM, dependency-license review and the formal accessibility audit are
      pilot-gate obligations, not per-release ones.
- [ ] 6.4.5 NOT THIS CHANGE: admitting `openAvatar` to the
      xFactory aggregation. That is a separate reviewed change recording path,
      remote, visibility, exact validated commit, checkout, compatibility,
      update and rollback behavior. Do not open it here.
      **THE ADMISSION ALREADY HAPPENED — NO WORK REMAINS. The unticked box is
      a SCOPE STATEMENT, not a pending item.** House precedent keeps
      NOT-THIS-CHANGE clauses unticked: there is nothing here for this change
      to do, and ticking would falsely claim this change did it. The admitting
      act, verified against the live remote 2026-08-27: xFactory aggregation
      commit `6a2f418fdc5e` of 2026-08-04, "Pin openAvatar at the neutral root
      (DTN-022 ruled: own repo)" — the only `.gitmodules` commit that touches
      this submodule. `.gitmodules` on the `opensoft/xFactory` aggregation
      repo's `main` today carries
      `[submodule "openAvatar"]` at path `openAvatar` with remote
      `git@github.com:opensoft/openAvatar.git`. That was a separate reviewed
      act outside this change, exactly as this clause and
      `repo-boundary-governance` "Deferred aggregation and web-console
      integration" require. Nothing in this change opens, re-opens, or depends
      on it.

## 7. Authoring inputs to pin (unvalued in the memo, not reopened forks)

Each of these is a value the rulings deliberately left to proposal and
realization time. None reopens a ruled fork; leaving any unset opens the ring
on an unstated assumption.

> **§7 IS FULLY RULED as of 2026-08-27.** All ten entries carry a value, a
> provenance and a grounding line; none is left to be decided at realization
> time, which is what this section's own preamble says the hazard would be.
>
> **7.1-7.6 RULED 2026-08-27** by Brett Heap, in session, on the research in
> `supporting-docs/section-7-authoring-inputs-memo.md` — every recommendation
> that memo carried, adopted as written.
>
> **7.7-7.10 RULED 2026-08-27**, later the same day, by Brett Heap in session.
> These four were NOT memo recommendations and could not have been: 7.7 needed
> a person named, which is Brett's act and not a value research can propose,
> and the other three were held open behind it or behind each other. Ruling
> them closed the last two cross-dependencies §7 was carrying against itself —
> §7.4's page target had no named recipient until 7.7 named the holder, and
> §7.2's metered per-tenant budget had no subject until 7.10 defined "tenant" —
> so no entry in this section now depends on an unruled one.

- [x] 7.1 The concrete vault for the internal-live server key. F0's mode-600
      local file plus age escrow is explicitly NOT a deployment source.
      **RULED 2026-08-27: Azure Key Vault `kv-opensoft-xfactory-qa`, fetched
      by the broker's own AKS workload identity through the Secrets Store CSI
      driver.** GROUNDING: this is not a new pattern for this org — the review
      lane already fetches a MODEL-PROVIDER TOKEN, the same credential class,
      from that vault by reference using the runner's own federated workload
      identity, which is the shipped realization of `credential-contracts`
      "Worker credentials are distributed by reference into ephemeral job
      scope"; the vault is live in the AKS QA estate the broker deploys into,
      so the ruling adds ONE SECRET to an operated estate rather than a
      custody mechanism (memo §7.1, "The decisive precedent").
      **THE RULING SPLITS ACROSS TWO REPOSITORIES, by canon.**
      `credential-contracts` says contract artifacts "SHALL NOT hard-code a
      vault operator, a vault product, or any secret value", so the two names
      above appear HERE — in a change packet — and never in
      `contracts/`. The neutral half is
      `contracts/avatar-client/broker-server-key-binding.template.yaml` (a
      credential reference, an owner, a rotation policy, and per-install
      placeholders for provider and vault); the concrete half is the named
      install-side act recorded at 6.1.1, left for that repository's own PR.
      The mode-600 local file and the age-escrow copy stay exactly what the
      SOP makes them — developer-local convenience and supervised recovery
      material — which is what this task's own sentence demands.
      **Recorded as a deliberate NOT NOW:** openProfiler, ratified 2026-08-26
      as this org's model-provider credential broker, is the freshest
      on-point precedent, but on the `api_key` path "the minted token IS the
      stored key verbatim", so minting buys no scope reduction here, and it is
      a per-operator local custody surface rather than a server-side vault —
      using it would mean deploying it into AKS as a sidecar, which is
      net-new infrastructure and out of scope of the change that introduced
      it. The two custody stories should converge later; they do not converge
      in this ring.
- [x] 7.2 Numeric ceilings: per-session duration and billable-unit limits, the
      per-tenant budget, and the configured provider-project cap amount.
      **RULED 2026-08-27: per-session 15 minutes (900 s) AND 300 billable
      units where one unit is one US cent of provider-attributed spend
      ($3.00) — both HARD and broker-enforced; per-tenant $150 per calendar
      month, METERED AND ALERTED ONLY; provider-project cap $750 per calendar
      month, HARD at the provider, with notifications at 50% ($375) and 80%
      ($600).** GROUNDING: F0 recorded ~183 short billed calls and NO dollar
      figure and no cap amount, so the anchor is the provider's published rate
      card, not a measurement — at audio rates and 1 token per 100 ms in / 50
      ms out, a well-cached 15-minute session costs about $0.84 and a
      poorly-cached one about $10.40, because the whole conversation is re-sent
      on every response and caching is best-effort; $3.00 is ~3.5x the
      expected case, so a normal session never trips it while the runaway is
      caught at under a third of its course, and $750 is ~2.4x the modelled
      ~$310 of total ring consumption, so ordinary work never halts the
      qualification (memo §7.2). The unit is CENTS, not tokens: audio-output
      tokens cost 160x cached audio-input tokens, so a token count is a bad
      cost proxy across modalities. The broker reads real per-response usage
      off the provider's own `usage` block, so this is accumulated actual
      cost, not an estimate. FAIL CLOSED ON AN UNCOUNTABLE VALUE — a broker
      that cannot determine its accumulated cost refuses the session rather
      than proceeding blind, following the org's other real ceiling.
      **THE PER-TENANT NUMBER IS METERED-ONLY, AND ITS READER IS §7.4.**
      Fork 1 Option C defers the durable synchronous per-tenant counter (task
      6.1.5), so nothing can hard-stop a single tenant and recording $150 as
      hard would be false. A metered-only threshold with no alert wired to it
      is the `budget_envelopes: {}` artifact a council reviewer has already
      flagged in this org — "no reader, no `spend_over_envelope` consumer, and
      no FAO seated" — so the $150 threshold's reader is named in §7.4's
      `gh issue create` path, and the two rulings are one arrangement.
      LANDED: the trip points are in
      `contracts/avatar-client/canary-cohort-and-rollback-policy.yaml` at
      ROLLBACK-B `elevated_quota_condition` (per-session ceilings, project
      cap, `uncountable_is: exhausted`) and ROLLBACK-C `cost_concern` (the
      metered per-tenant budget, `hard_stop_exists: false`, and its alert
      reader).
- [x] 7.3 Rotation cadence and trigger for the server key, written into the
      binding's `rotation_policy`; the SOP gives the procedure but no
      interval.
      **RULED 2026-08-27: `max_key_age_days: 90` as an
      `xfactory_credential_rotation_policy` override on
      `avatar_broker_openai_internal_live`, inheriting the global
      `require_rotation_on` list UNCHANGED (`client_offboarding`,
      `suspected_exposure`, `provider_policy_change`,
      `privileged_scope_change`) and adding three:
      `avatar_platform_maintainer_change`, `canary_cohort_change`,
      `release_ring_promotion`.** GROUNDING: 90 days is not invented here —
      it is the org's ONLY enforced key-age cadence, applied to exactly three
      vault-held credentials in the same custody shape §7.1 rules for this
      key, and independently described as the family's strictest existing
      tier; adopting it makes this a constrained instance of an existing tier
      rather than a new policy, and the three added triggers follow the same
      `additional_require_rotation_on` idiom those overrides already use
      (memo §7.3). It also does not churn the evidence: against the ruled
      14-day soak (§7.6), a 90-day cadence means AT MOST one rotation inside
      the ring and most likely zero, where 30 days would risk a rotation
      landing mid-soak and muddying the latency and error-rate evidence for no
      security gain at this blast radius — one dedicated spend-capped provider
      project, synthetic or internally-consented audio only.
      **A WORDING TENSION RULED WITH EYES OPEN:** `credential-contracts` calls
      the vault-held worker credential a "LONG-LIVED, NON-ROTATING headless
      token", and the same sentence continues "Rotation SHALL be a vault write
      (effective the next job, no host administration)". NON-ROTATING MEANS
      NOT SELF-REFRESHING — the phrase exists to refuse the refreshable
      session-state class — and it does not forbid a cadence. Stated here so a
      later reader does not find the two clauses contradictory.
      LANDED: `contracts/avatar-client/broker-server-key-rotation-policy.yaml`;
      the binding keeps `rotation_policy: operator_managed` because the
      published schema types that field as a string.
- [x] 7.4 The alerting channel, thresholds and page targets for the usage
      meter.
      **RULED 2026-08-27: two channels, neither of which builds new
      infrastructure — (1) the provider project's own native budget
      notifications on the dedicated internal-live project, at 50% and 80% of
      the §7.2 cap, with the cap itself as the hard stop; (2) `gh issue
      create` from the metering job following the doc-health pattern verbatim
      (one issue per run, supersede-and-close the prior), on a per-tenant
      metered crossing of $150/month or any cost-triggered session kill.
      Azure Monitor is named as PILOT-HARDENING work, not ring work.**
      GROUNDING: a full survey of the aggregation tree found NO alerting plane
      of any kind — no Prometheus, Grafana, Alertmanager, PagerDuty, Opsgenie,
      Azure Monitor action group, App Insights, SMTP alert or Slack webhook in
      any running code path; the one live service exposes only Kubernetes
      probes and notifies no human, OpsxFactory's monitoring material is
      explicitly `Status: brainstorm`, and the Flux notification controller
      present in the QA cluster has zero `Provider`/`Alert` resources and in
      any case reports GitOps reconciliation, not application spend. The ONLY
      wired path that reaches a human is `gh issue create` from CI, proven
      twice — the nightly doc-health regression issue with its
      supersede-and-close semantics, and merge-master's `@`-mention issue — so
      the ruling reuses it rather than building a plane on the critical path
      of a qualification ring (memo §7.4, the one ⚠️ NEW CAPABILITY flag,
      routed around rather than through).
      **PAGE TARGET — RECORDED AS A ROLE, AND THIS IS AN OPEN EDGE.** The
      target is the human who also holds the §7.7 kill switch, so the person
      who learns about the spend is the person who can stop it. §7.7 is still
      OPEN and does not yet say HOW that holder is recorded, so this ruling
      records the ROLE — the openxFactory avatar platform maintainers, as
      credential owner, in the person who holds the §7.7 kill switch — and
      NOT a personal name. §7.7 must name a person or rota before the canary
      opens; an alert with no named recipient and a kill switch with no named
      holder are the same gap seen twice.
      **EDGE CLOSED LATER THE SAME DAY, by §7.7.** The clause above stands as
      written because it records what this ruling could and could not decide
      on its own. It is now discharged: §7.7 names BRETT HEAP as the holder of
      both kill switches, so the page target is a PERSON and no longer a role,
      and the metering alert has a named recipient. The name is written down
      in exactly one place —
      `canary-cohort-and-rollback-policy.yaml` `operator_surface.holder` — and
      ROLLBACK-C's `cost_concern` points at it as `alert_recipient_ref` rather
      than repeating it, because a second copy is how the alert's recipient
      drifts away from the switch's holder, which is the one coupling these
      two rulings exist to guarantee.
      **AN UNTESTED ALERT PATH IS INDISTINGUISHABLE FROM NO ALERT PATH:** at
      least one alert must be observed DELIVERED end to end — a threshold
      deliberately tripped low, or a test issue filed — before the canary
      opens. That is the §7.4 analogue of RING-04's "exercised for real"
      discipline, and it belongs to 6.1.4's wiring slice.
- [x] 7.5 Minimum sample count per gated latency cell (feeds §5.2).
      **RULED 2026-08-27: n >= 100 completed, schema-valid AVC-10 samples per
      gated cell — declared BEFORE measuring; a cell with n < 100 is RECORDED
      but MUST NOT GATE; and per cell the samples must span at least 3
      distinct measurement runs on at least 2 distinct days.** GROUNDING: the
      count above the true p95 is Binomial(n, 0.05), so at F0's n=30 the p95
      estimate is essentially the second-largest of thirty — a maximum wearing
      a percentile's name, whose nonparametric interval plausibly swings as
      wide as the 246 ms threshold it is meant to test, because that
      `sideband_ready` distribution spans 870 ms between its p50 and its p95;
      at n=100 the estimate is an interior order statistic and sits stably
      inside the 150-246 ms materiality floor, and 4 cells x 100 setup-only
      sessions is a small fraction of §7.2's cap, so the defensible number and
      the affordable one are the same number (memo §7.5). The run-and-day
      spread exists because F0's whole dataset came from one harness, one
      configuration, `region: null`, in one sitting — a minimum n taken all at
      once would repeat that with a bigger number, which is worse, because a
      bigger number looks like rigor. RECORDED NOW to prevent a live
      misreading: at n=100 p99 IS effectively the maximum, so gating it would
      need ~500 samples per cell and it stays `recorded_not_gated`.
      LANDED: `contracts/avatar-client/latency-sample-minimum.yaml`, a sibling
      of the acceptance map rather than a block inside it, because
      `acceptance-map.yaml` is a published digest-pinned bundle member and an
      authoring input does not earn a contract-release cut. §5.2's ordering
      requirement is satisfied by construction: the declaration lands while
      the SLO entry still reads `measured_evidence.status: not_yet_measured`,
      which is exactly now.
- [x] 7.6 Canary exit criteria: soak duration, minimum session count, and
      tolerated error rate.
      **RULED 2026-08-27: soak = 14 consecutive calendar days with canary
      sessions on >= 10 distinct days; minimum = 200 completed canary sessions
      with sub-floors of >= 50 from COHORT-02 and >= 3 per §6.2.1 evaluation
      scenario class; tolerated error rate = <= 2% abnormal-session rate over
      the full soak AND <= 5% over any trailing 50-session window. Plus two
      criteria beyond the three this task names: >= 1 live ROLLBACK-B
      auto-trip proven end to end through the §6.3.3 detection wiring
      (injected if it does not occur naturally), and zero unresolved
      ROLLBACK-A trips at exit.** GROUNDING: 200 is set by MEASURABILITY, not
      by feel — the §6.2.1 coverage floor alone is 15 classes x 3 = 45, but a
      "<= 2%" criterion cannot be evaluated at n=50, where one failure is
      already 2%, whereas at n=200 the two thresholds are 4 and 10 sessions
      and the criterion can actually distinguish a good ring from a marginal
      one; 14 days covers two business weeks for a weekday-shaped internal
      cohort and spans a provider deploy cadence, and the 10-distinct-day
      floor stops 200 sessions being run in two frantic afternoons; 2%/5% is
      anchored to observed behavior, since across ~183 F0 calls no
      provider-side failure class was recorded and the one failed smoke was a
      client-harness defect (memo §7.6).
      **THE TRAILING-WINDOW RATE IS ALSO ROLLBACK-B's `elevated_error_rate`
      TRIP — one number, not two.** Ruled apart, the canary could pass its
      exit criterion while its auto-blocker was tripping, or the reverse; the
      validator now compares the two and fails on drift.
      **ABNORMAL IS DEFINED, or the rate is unfalsifiable:** a session that
      fails to reach `first_playable_after_authorized`, or terminates to a
      non-clean terminal that is not a deliberate test action — consent
      withdrawal drills, injected rollback rehearsals and operator-fired
      ROLLBACK-C are excluded and counted separately.
      **THE REHEARSAL CRITERION IS NOT A DUPLICATE OF RING-04.** RING-04 is a
      PRE-canary gate on the kill SWITCHES, exercised for real in both
      block-new and revoke-active modes. Nothing else proves the DETECTION,
      and Option B was chosen over Option A precisely for that rehearsal
      value; an untripped detector is an unrehearsed detector.
      LANDED: `contracts/avatar-client/canary-cohort-and-rollback-policy.yaml`
      `canary_exit_criteria`, moved from `status: unset` to `status: ruled`
      BEFORE the canary opened — which that block's own statement says is the
      point, so the ordering is itself the evidence.
- [x] 7.7 The operator surface that fires the kill switches — the web console
      is a kernel non-goal, so the holder and the mechanism must be named
      before the canary opens.
      **RULED 2026-08-27 by Brett Heap, in session: BRETT HEAP holds BOTH kill
      switches for the internal-live ring; the mechanism is a DOCUMENTED
      RUNBOOK ACT on the serving install — flipping the two server-side
      kill-switch flags; and the ROTA question is DEFERRED to
      `avatar-pilot-hardening`.** This is the one §7 entry that could not be
      closed by research: it needed a person named, which is Brett's act and
      not a value any memo can recommend, and the memo said so.
      **IT CLOSES TWO GAPS, WHICH WERE ALWAYS ONE GAP.** (1) The policy's
      `operator_surface.status: unnamed`, whose own note read "a canary opened
      without a named holder has an unfireable kill switch, which would make
      ROLLBACK-C undeliverable and ROLLBACK-A dependent on automation alone" —
      now `status: named` with the holder, the mechanism and the two switches
      recorded. (2) §7.4's ALERT RECIPIENT. That ruling recorded its page
      target as a ROLE only because this task was open; the ruling names the
      person both ends were waiting for, so the metering alert now has a named
      recipient and §7.4's open edge is closed. An alert with no named
      recipient and a kill switch with no named holder were the same gap seen
      twice; one ruling closes both, which is why they were recorded as one.
      LANDED, in two places: `docs/sops/avatar-internal-live-kill-switch.md` —
      the runbook, in this repository's SOP home beside the F0 lab-credential
      SOP, carrying the two switch scopes (`SWITCH-ALL-NEW` for all new
      session creation, `SWITCH-PROFILE` for `gpt-realtime-2.1`), the
      `block_new` and `revoke_active` modes each carries, which mode each
      rollback class selects, the rollback target's no-model-fallback fact,
      the escalation path, and RING-04's pre-canary obligation; and
      `canary-cohort-and-rollback-policy.yaml` `operator_surface`, which
      points at it as `mechanism_ref`. The validator requires that reference
      to RESOLVE ON DISK — a mechanism that IS a document is unfireable if the
      document does not exist, which is the same defect wearing a filename.
      **THE MECHANISM SPLITS ACROSS TWO REPOSITORIES, exactly as §7.1's does.**
      The runbook states the two scopes, the two modes and the selection rule;
      it does NOT state a flag name or a command, because the serving install
      does not exist yet — task 6.1.2 is unticked — and a procedure written
      for a system nobody has run is a fabricated procedure. The concrete half
      lands in the consuming install's own PR, and the runbook says so in
      those words rather than leaving the gap to be discovered.
      **THE ROTA DEFERRAL IS PART OF THE RULING, not an omission.** One named
      human is proportionate to a cohort of internal staff plus one
      internally-staffed sandbox. It is not proportionate to a pilot admitting
      real tenants, and `avatar-pilot-hardening` owns that widening.
- [x] 7.8 The session-outcome token each rollback path emits (`revoked` versus
      `abandoned` for a drained leg versus a force-terminated leg); only
      consent/lease revocation is fixture-bound today.
      **RULED 2026-08-27 by Brett Heap, in session: a ROLLBACK-B DRAINED leg
      ends `abandoned` — or `completed` if it reached its natural terminal
      first; a ROLLBACK-A FORCE-TERMINATED leg emits `revoked`, reusing the
      fixture-bound consent-withdraw terminal path EXACTLY. NO NEW OUTCOME
      TOKEN.** GROUNDING: every token is already a member of the closed
      `session-outcomes` registry, and the ruling is deliberately the reading
      that keeps the two facts DISTINGUISHABLE. A drained leg was given up
      when the drain window closed — it was not revoked, and spending
      `revoked` on it would hide real revocations among performance rollbacks,
      which is the one place the revocation evidence has to stay legible. A
      force-terminated leg was cut, not given up, and it is cut by the very
      terminal path ROLLBACK-A's own `mechanism` already says it reuses, so
      emitting anything but `revoked` would contradict the class one line
      above it. The `completed` alternative is not a hedge: a leg that reached
      its own terminal inside the drain IS a completed session that happened
      to be in flight when new work was blocked, and recording it as
      `abandoned` would be false.
      **THE TOKENS ARE WHAT MAKES §7.6's ERROR RATE READABLE.** The
      abnormal-session rate counts terminals, so a path whose token was
      inferred after the fact would let one event be counted two ways by two
      readers — which is why this block always said the outcome SHALL be
      "DECLARED IN ADVANCE rather than inferred".
      LANDED: `canary-cohort-and-rollback-policy.yaml`
      `session_outcome_tokens` moves from `partially_bound` to `bound` with
      all three paths mapped and `unbound` emptied, and the token is ALSO
      carried on the ROLLBACK-A and ROLLBACK-B class blocks
      (`session_outcome`, `session_outcome_path`) so the class a reader lands
      on states its own terminal. The two copies are machine-compared, on the
      same discipline as §7.6's error rate. ROLLBACK-C carries
      `session_outcome: operator_selected`, in that class's existing idiom:
      the operator picks the scope and the scope binds the token. The
      validator resolves every declared token against the REGISTRY rather than
      against a list mirrored in the validator, so the "no new token" ruling
      cannot be satisfied by a copy that agrees only with itself.
- [x] 7.9 The declared region and data-control values recorded in the AVC-09
      descriptor, and the retention window for any canary-derived
      `structured_record` as a domain-owned policy reference.
      **RULED 2026-08-27 by Brett Heap, in session: REGION = the provider
      project's US default, declared HONESTLY in the AVC-09 descriptor when it
      is authored; DATA-CONTROL = exactly the F4 Option C classes
      (`ephemeral_presentation` + `structured_record`), with no `audio`,
      `full_transcript` or `independent_transcription` instance ever created;
      RETENTION = 90 days for canary-derived `structured_record`, carried by a
      NAMED DOMAIN-OWNED policy reference the descriptor cites.** GROUNDING:
      F0 recorded `region: null` from one harness in one sitting and the
      dedicated internal-live provider project is unprovisioned (task 6.1.2),
      so the only truthful declaration is the default the project will
      actually run under — a descriptor claiming a pinned region the project
      does not enforce would be false in the single field the ring points at
      for locality, and the honesty is the ruling rather than a caveat on it.
      The data classes are Fork 4 Option C unchanged, which is what keeps the
      four reserved retention classes forbidden and the consent-purpose count
      frozen at 3. Ninety days outlives the ring — §7.6's soak is 14
      consecutive days — so a record survives long enough to answer a question
      asked after the canary closes, which is when such questions are actually
      asked, without a qualification ring accruing a standing retention
      obligation it never justified.
      **THE VALUES ARE PINNED; THE DESCRIPTOR IS NOT AUTHORED.** AVC-09's
      `region_and_data_controls` is their single home and no descriptor
      instance exists yet, so what this ruling fixes is what the descriptor
      SHALL declare — descriptor authoring consumes a ruling instead of making
      one. LANDED on `internal-live-activation-checklist.yaml` condition 2,
      which is the condition that APPROVES the regional, retention and
      data-control terms, is HARD PREFLIGHT, and already named §7.9 as an
      owning task. Recorded there as `ruled_values`, machine-checked: the
      permitted class set is compared SET-EQUAL, because the failure mode is a
      class quietly ADDED — `audio` appearing there would unreserve by
      checklist edit what the kernel says only a successor change may
      unreserve.
      **TWO THINGS RECORDED SO SILENCE IS NOT READ AS A RULING.** AVC-09's
      three OPTIONAL fields (`data_residency`, `provider_retention`,
      `provider_training_opt_out`) are NOT pinned here and are authored from
      the provider's actual terms at descriptor time. And the data-control
      guarantee is OPERATIONAL: no schema field forbids an out-of-class
      instance or a second-model shadow today, the enforcing contract flag is
      pilot-hardening work (task 6.2.4), and claiming otherwise would be
      false. Also stated in the artifact: §7.3's `max_key_age_days: 90` and
      this 90-day retention window are two unrelated numbers that happen to
      share a value; nothing couples them.
- [x] 7.10 The definition of "tenant" for this ring, which must agree with
      §6.3.1's cohort or the per-tenant dimension has no subject.
      **RULED 2026-08-27 by Brett Heap, in session: TENANT = COHORT MEMBER —
      exactly §6.3.1's cohort, so the vendor-organization internal cohort and
      the one internally-staffed domain sandbox are TWO TENANTS.**
      **THIS IS WHAT GIVES §7.2's METERED BUDGET ITS SUBJECT.** The ruled
      $150-per-calendar-month per-tenant budget had no subject at all until
      now — a metered figure with an undefined denominator is not a budget, it
      is a number — and §7.2 explicitly recorded that it was SIZED on the
      assumption that tenant = cohort member, i.e. two tenants, so that the
      pair sits comfortably under the $750 provider-project cap. This ruling
      makes the assumed denominator explicit rather than replacing it, so
      §7.2's figure stands unchanged and needs no re-sizing: two budgeted
      subjects, $300 of metered per-tenant exposure against a $750 hard cap.
      The alternatives were both worse and are recorded as refused. A
      per-session participant would have made $150 meaningless at this scale;
      a whole DomainxFactory would have collapsed COHORT-02 into a unit larger
      than the sandbox actually admitted to the ring, which would have widened
      the ring by arithmetic rather than by ruling.
      LANDED: `canary-cohort-and-rollback-policy.yaml`
      `cohort.tenant_definition_ref` moves from `status: unset` to `status:
      set` with `tenant_is: cohort_member`, the two tenant ids, the count, and
      `sizing_still_valid: true`; and ROLLBACK-C's `cost_concern` gains
      `budget_subject: cohort_member` so the metered number names its
      denominator at the point of use. The validator RECOMPUTES `tenant_count`
      from `cohort.members` rather than reading it — a count that outlives the
      membership it summarises is exactly how a budget silently starts
      metering against a denominator that no longer exists.

## 8. Realization gate

- [ ] 8.1 Preconditions consumed, not re-proven: the released, code-signed
      Flutter client with its fail-closed `SessionTransport` seam; the
      contract kernel pinned at exact commit, per-file digest and
      interface-lock digest; and the recorded F0 overall PASS with its
      accepted threat model.
- [ ] 8.2 `python3 scripts/validate-avatar-client.py` green, and the repo's
      own validators green, in the SAME commit that unreserves the two ids.
- [ ] 8.3 The four ring elements closed with real evidence (§4.2-§4.5) — a
      dry run is not evidence.
- [ ] 8.4 ARCHIVE GATE: merged on both target surfaces plus green
      internal-live realization evidence. This change stays ACTIVE as
      approved-but-unrealized intent until then, per `release-realization`.
