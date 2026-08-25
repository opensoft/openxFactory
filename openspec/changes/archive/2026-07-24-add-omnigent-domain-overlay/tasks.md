# Tasks: add-omnigent-domain-overlay

## 1. Contract schemas (openxFactory)

- [x] 1.1 Author the Omnigent domain-overlay payload schema alongside
      `contracts/hermes-runtime/` (v2 family; consumes
      `overlay-manifest.schema.yaml` for the file-inventory + sha256 +
      `git_overlay_pin` shape): worker-class declarations with archetype
      mapping, the six-boolean generalized permission matrix (constitutional
      `execute_final_action`/`access_secrets` false enforced in-schema),
      credential tiers incl. `never_assignable`, prompt-pack / toolchain /
      validator / preseed / lane-delta sections, and the
      `domain_installation_overlay` operation envelope with
      `stricter_rule_wins`.
- [x] 1.2 Author the Omnigent install-manifest schema: digest pin of the
      Hermes runtime manifest as stack identity, tenant/domain cardinality,
      subject-workload registry entries (identity ref, activation state,
      validator mode), and compose/verify evidence-record references.
      Canonical `subject`/`tenant`/`domain` spellings throughout.
- [x] 1.3 Positive and negative fixtures: a conforming overlay + manifest
      pair; rejections for archetype-less worker class, constitutional
      boolean true, loosening overlay, dual domain overlay, identity drift,
      unrendered-profile launch, `never_assignable` grant.
- [x] 1.4 Validator: extend or add a `scripts/validate-*.py` covering 1.3;
      register new files per the contract versioning policy (holding area
      until the allocated additive release).

## 2. Documentation

- [x] 2.1 MODIFY `docs/xfactory-domain-factory-model.md`: prescribe the
      DomainxFactory `omnigent/` tree shape (sibling of `hermes/domain/`),
      its payload inventory, and the pin-consumption mechanism; cite this
      change as the ratification record.
- [x] 2.2 Record the worker archetype vocabulary and permission-matrix
      semantics in the domain-factory model's Omnigent overlay section
      (with the codex and Medx alias examples).
- [x] 2.3 Link this change in the README OpenSpec Records block; keep the
      staging INDEX row current (done at proposal authoring). Doc-index
      link to `contracts/omnigent/README.md` and the contracts README
      holding-area rows added at realization.

## 3. Gated follow-up changes (filed, not executed in this change)

- [x] 3.1 `installs/omnigent-install`: manifest quartet +
      `domain_overlays[]` digest pins + cardinality validation + read-only
      compose/verify increment emitting seeding-vocabulary evidence
      (first realization increment; worker-host mutation verbs deferred).
      REALIZED 2026-07-23: omnigent-install `add-omnigent-install-manifest`
      (3f31270) — manifest with hermes identity pin + codex overlay pin,
      fail-closed verify with deterministic evidence, skew findings
      surfaced. Effective-profile rendering + byte-equivalence deferred to
      its follow-up increment (overlays carry no profile deltas yet).
- [x] 3.2 `installs/hermes-install`: worker-readiness API port and pilot
      `hermes_service/` retirement (cutover shape per the design record's
      open question).
      AUTHORED + LANDED 2026-07-23: hermes-install
      `port-worker-readiness-surface` (09af670) — wire+auth-compatible
      endpoints outside /api/v1, pilot validation ported, additive
      migration 0010, sanitized read view, 15 API tests, all gates green.
      Cutover decision recorded: hard hostname repoint, no data migration
      (300s freshness), no dual-serve. REMAINING (human-gated): Brett's
      deployment window — deploy, repoint hermes-readiness.xforge.us,
      verify a consumer freshness gate, retire the pilot. This task and
      the parent change complete at that evidence.
      COMPLETE 2026-07-24: cutover Phases 1-4 executed and evidenced
      (hermes-install port-worker-readiness-surface, ratified + archived
      2026-07-24, canonical spec worker-readiness-surface; pilot workload
      pruned via Omnigent-Install PRs #29/#30; doc-health readiness gates
      green end-to-end; pilot code retirement filed as omnigent-install
      retire-pilot-readiness-service).
- [x] 3.3 `xFactories/codexFactory`: author the first `omnigent/` overlay;
      the live coding-patch-worker binding becomes a rendered consequence
      of overlay + params, byte-equivalence proven.
      PROGRESS 2026-07-23: overlay authored, conforming, and archived
      (codexFactory `align-omnigent-overlay-to-neutral-contract`, canonical
      spec `engineering-omnigent-overlay`; digest-pinnable
      `omnigent/overlay-manifest.yaml` landed).
      COMPLETE 2026-07-23 (rendering increment): codexFactory
      `author-execution-lane-profile-in-overlay` (469322b) made the live
      coding-patch-worker profile overlay-authored; omnigent-install
      `render-effective-profiles` (def6a56) renders it byte-verbatim with
      provenance sidecars and proves rendered == pinned source == live
      binding (sha256 f2f70eb2..., render-verify evidence green). The live
      execution-lane binding is a rendered consequence of overlay + params.
- [x] 3.4 `xFactories/MedxFactory`: second-domain params fixture rendered
      from the staged overlay draft
      (`ideation/staging/medical-omnigent-overlay/domain-overlay.draft.yaml`)
      without touching core — the pattern-is-real gate for archiving the
      staging topic.
      PROGRESS 2026-07-23: the fixture's content source is landed and
      canonical — MedxFactory `adopt-neutral-omnigent-overlay` ratified +
      archived (canonical spec `medical-omnigent-overlay`; conforming
      `omnigent/domain-overlay.yaml` + pinnable overlay manifest at
      cadeaa2).
      REALIZED (manifest level) 2026-07-23: omnigent-install
      `config/fixtures/medx-second-domain.manifest.yaml` — params-only
      delta over the same schema + verify step, zero core edits, verified
      green with evidence. With task 3.3 complete (rendering increment), both
      halves of the staging topic's archive gate are satisfied; the topic
      archives when the rendering-increment changes ratify.

## Bookkeeping correction (2026-08-23, `govern-openspec-corpus-membership`)

`proposal.md` real line 4 was respelled `Ratified by:` to `Ratified:` by slice
5B of `govern-openspec-corpus-membership` — the prefix only. Every byte after
the colon is carried verbatim, asserted identical at the edit, so the original
line is recovered exactly by reading `Ratified by:` back in its place and
nothing else on the page moved. The ruling is OQ-4's RULED extension of
2026-08-23 (Brett Heap, in-session), which widens the class to the sixteen
lines whose named change id is the DOCUMENT'S OWN. A change is not its own
approving change, and such a line passed `fam_ratified_provenance` only by
self-reference. This one emitted NO finding, so the respell is corrective
rather than a discharge and clears nothing from the census. The record that
justifies this line is the user approval of 2026-07-22 named on the line,
recorded by commit `aa636e1` of that same 2026-07-22, "Record ratification of
add-omnigent-domain-overlay (2026-07-22)" — two days before the archive
folder's date, which is why the two dates differ. An append on a single-valued
header is mechanically impossible — `doc_health.corpus.STATUS_RE` swallows any
trailing annotation — so this is an in-place overwrite and an extension of
Brett's 2026-08-10 append ruling, named as one, and it is entered in
`docs/archive-record-discrepancies.md`.
