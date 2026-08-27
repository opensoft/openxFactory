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

- [ ] 6.1.1 Author the broker server-key credential binding under the
      promoted `xfactory_credential_binding_template` shape — provider,
      vault, secret_ref, owner, rotation_policy — resolved only by the
      broker. No plaintext key in any repository; the age-encrypted registry
      copy is supervised recovery material, never a deployment source.
- [ ] 6.1.2 Provision the DEDICATED spend-capped internal-live provider
      project, distinct from the F0 lab project, with its project budget and
      rate controls set BEFORE any live trial (the F0-proven pattern).
- [ ] 6.1.3 Wire the session hard-kill onto the EXISTING duration/quota
      terminal outcome plus kill switch plus lease revocation — no new
      terminal is invented — and give a cost-triggered kill an auditable
      reason distinguishable from an ordinary duration or quota terminal.
- [ ] 6.1.4 Wire asynchronous usage metering and threshold alerting for
      per-tenant visibility.
- [ ] 6.1.5 DEFERRED, NOT BUILT: the durable synchronous per-tenant
      cumulative-spend counter. Record it as `avatar-pilot-hardening`'s work
      and record the resulting limit — the provider-project cap is the only
      per-tenant hard stop until it lands — as a stated property of this ring.

### 6.2 Consent and evaluation audio (F4 Option C)

- [ ] 6.2.1 Build the SYNTHETIC evaluation corpus for the model-versus-model
      safety, exact-value, consent, handoff and blocked-state scenarios across
      generic, MedxFactory and LedgerxFactory.
- [ ] 6.2.2 Define the canary's ephemeral processing envelope: consent rides
      the existing `avatar.media_capture` and `avatar.provider_processing`
      purposes plus an optional stricter domain purpose reference; captions
      and deltas are `ephemeral_presentation`; decisions, consent versions and
      outcomes are `structured_record`; withdrawal maps to the existing
      revoked outcome and stays reachable mid-session.
- [ ] 6.2.3 CONFIRM UNTOUCHED, by inspection rather than assertion: the four
      reserved retention classes stay forbidden, `local_persistence` stays
      const false, and the frozen consent-purpose count stays 3.
- [ ] 6.2.4 Record the non-shadowing guarantee as an OPERATIONAL control with
      the enforcing contract flag named as pilot-hardening work — no schema
      field forbids a second-model shadow today, and claiming otherwise would
      be false.

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
      6.3.3's auto-detection wiring is NOT built by this task and is left
      unticked; the policy names §6.3.3 as its `detection_wiring_owner`.
- [ ] 6.3.3 Build the auto-detection wiring the policy needs — the latency
      trip off §5's SLO and the safety-eval trip off §6.2.1 — since Option B
      was chosen precisely for this rehearsal value.
- [ ] 6.3.4 Implement rollback as disable-voice into text or human handoff.
      `gpt-realtime-2.1` is the FIRST qualified profile, so no model fallback
      exists and none may be implied in copy or code.
- [ ] 6.3.5 Prove that an abort ends the media plane only: the logical
      session's authority-owned workflow projection and its policy-required
      records survive, reusing the landed consent-withdraw-mid-speech terminal
      path.

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
>    it held no code. Under R3 it was deleted 2026-08-27; `gh api
>    repos/opensoft/xfactory-avatar-client` now returns 404.
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
- [ ] 6.4.5 NOT THIS CHANGE: admitting `openAvatar` to the
      xFactory aggregation. That is a separate reviewed change recording path,
      remote, visibility, exact validated commit, checkout, compatibility,
      update and rollback behavior. Do not open it here.
      **ALREADY EXISTS — verified 2026-08-27.** The xFactory aggregation's
      `.gitmodules` already carries `[submodule "openAvatar"]` at path
      `openAvatar` with remote `git@github.com:opensoft/openAvatar.git`,
      admitted by a separate act outside this change. The not-this-change
      clause therefore stands satisfied by that prior act rather than
      forbidding work that still needs doing.

## 7. Authoring inputs to pin (unvalued in the memo, not reopened forks)

Each of these is a value the rulings deliberately left to proposal and
realization time. None reopens a ruled fork; leaving any unset opens the ring
on an unstated assumption.

- [ ] 7.1 The concrete vault for the internal-live server key. F0's mode-600
      local file plus age escrow is explicitly NOT a deployment source.
- [ ] 7.2 Numeric ceilings: per-session duration and billable-unit limits, the
      per-tenant budget, and the configured provider-project cap amount.
- [ ] 7.3 Rotation cadence and trigger for the server key, written into the
      binding's `rotation_policy`; the SOP gives the procedure but no
      interval.
- [ ] 7.4 The alerting channel, thresholds and page targets for the usage
      meter.
- [ ] 7.5 Minimum sample count per gated latency cell (feeds §5.2).
- [ ] 7.6 Canary exit criteria: soak duration, minimum session count, and
      tolerated error rate.
- [ ] 7.7 The operator surface that fires the kill switches — the web console
      is a kernel non-goal, so the holder and the mechanism must be named
      before the canary opens.
- [ ] 7.8 The session-outcome token each rollback path emits (`revoked` versus
      `abandoned` for a drained leg versus a force-terminated leg); only
      consent/lease revocation is fixture-bound today.
- [ ] 7.9 The declared region and data-control values recorded in the AVC-09
      descriptor, and the retention window for any canary-derived
      `structured_record` as a domain-owned policy reference.
- [ ] 7.10 The definition of "tenant" for this ring, which must agree with
      §6.3.1's cohort or the per-tenant dimension has no subject.

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
