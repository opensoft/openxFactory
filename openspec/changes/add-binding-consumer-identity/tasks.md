# Tasks: add-binding-consumer-identity

Status: draft

**NOTHING BELOW RUNS BEFORE RATIFICATION, and ratification is not what landing
this packet seeks.** This change's own diff is the spec delta and these records.
The sequence Brett authorized on 2026-08-29 is: author the packet → a
§7.4-shaped council reads it adversarially, convened OUTSIDE the clearance
pipeline → Brett rules → only then does anything in §1–§7 begin.

**No task here creates, moves, or reads a live secret.** The block this change
adds holds identifiers; it holds no credential material, and its realization
touches no vault.

## 0. Before anything is built — the council round and its consequences

- [ ] 0.1 Council review of this packet, §7.4-shaped: independent seats, return-cited
  ballots, convener ruling, record filed where the 2026-08-28 gate-rules convening
  filed its own. Commissioned outside the clearance pipeline BY DESIGN — proposals
  are never-convenable through it on the 2026-08-28 unanimous ruling.
- [ ] 0.2 Carry every ballot disposition back into the packet BEFORE ratification,
  including reversals, and record a reversal as a reversal rather than smoothing it
  into agreement. D-1 through D-5 in `proposal.md` and OQ-1 through OQ-5 are the
  named targets; a seat ruling against D-1 or D-3 changes the delta's shape and
  §1 below must be re-scoped before it is executed.
- [ ] 0.3 Ratification act by Brett Heap, recorded under `review/` in this packet,
  naming what the citation covers and what it does not.

## 1. The schema — one additive optional block

- [ ] 1.1 Add `consumer:` to each entry of `credential_bindings` in
  `xfactory_credential_binding_template`
  (`contracts/schemas/xfactory-credential-contracts.schema.yaml`): `holder_ref`
  and `fetch_identity` REQUIRED WITHIN THE BLOCK, `requirement_ref` optional,
  `shared_credential_acknowledged` optional with `const: true`.
  `additionalProperties: false` ON THE BLOCK.
- [ ] 1.2 The block itself stays OPTIONAL on the binding, and the binding object
  stays UNCLOSED. Closing the binding object is a breaking act and is NOT this
  change — see design §5. A test asserts the un-narrowing: a binding template
  carrying no `consumer:` block validates unchanged.
- [ ] 1.3 Identifier grammar reuses the shipped one rather than inventing a
  third: `identity-brokering`'s `identifier` pattern
  (`^[A-Za-z0-9][A-Za-z0-9._:/-]*$`, 1–200) is what its own `holder_ref` uses,
  and a divergent pattern for the same word in the same estate is how two
  spellings begin.
- [ ] 1.4 Write the block's `description` to carry its own reasoning, on this
  schema's established style: why the block is declared rather than left as the
  free key it already is, why the acknowledgment is const-true, and why a
  persona is not admissible in `holder_ref`.

## 2. The validator — a warning channel it does not have, and three codes

- [ ] 2.1 BUILD THE WARNING CHANNEL FIRST. `scripts/validate-credential-contracts.py`
  prints `ERROR` and counts errors; it has no warning severity at all, so the
  deprecation posture is currently inexpressible there. Eleven sibling
  validators have one — follow the nearest
  (`scripts/validate-client-identity-roster.py`, which reads records this same
  schema owns) rather than inventing a fourth shape.
- [ ] 2.2 `consumer-identity-undeclared` — WARNING on a binding with no
  `consumer:` block, naming the release at which it becomes an error. It is an
  ERROR only at that major and MUST NOT be one before.
- [ ] 2.3 `shared-secret-identity` — keep the predicate and the refusal as the
  DEFAULT, and add the five-condition lift exactly as the requirement states it,
  each condition failing closed. A test per condition, each proving the
  refusal STANDS when only that condition is missing.
- [ ] 2.4 `shared-authority-identity` — NEW error: two bindings on one
  `secret_ref` declaring the same `fetch_identity`. The message names two
  systems on one authority and does not mention secret reuse.
- [ ] 2.5 The fifth condition's resolution: `requirement_ref` resolves against
  the `xfactory_credential_requirements` records in the repository under
  validation. UNRESOLVABLE MUST REPORT AND WITHHOLD THE LIFT — never pass
  silently, never treat what could not be read as satisfied.
- [ ] 2.6 A mutation round over §2.3–§2.5, one mutant per condition, and each
  mutant's death asserted by a NAMED test rather than by a count. A harness has
  a fourth state: a mutant that dies because its anchor is missing has proved
  nothing.

## 3. Packaged fixtures — including the one the predecessor had to decline

- [ ] 3.1 POSITIVE: two consuming systems reaching one operated identity in one
  template — the fixture `add-notebook-hosting-credential-custody` §4.1 DECLINED
  because the unsharpened rule refuses it. Landing it is this change's own
  evidence that the decision handed forward has been taken.
- [ ] 3.2 NEGATIVES, one per named refusal: same fetch identity; one-sided
  acknowledgment; acknowledgment valued false; a member outside the closed
  block; a dispatch/content pair declaring itself shared; an unresolvable
  requirement reference. Each registered in the validator's
  `NEGATIVE_EXPECTATIONS` map, because an unregistered negative is reported by
  the self-test as having no expectation.
- [ ] 3.3 UPDATE THE SELF-TEST COUNT STRING IN THE SAME COMMIT.
  `tests/credential_contracts/test_dispatch_credential_contract.py:35` asserts
  `"self-test: 3 positive + 5 negative example(s) confirmed"` verbatim. Any
  fixture added here moves it or the suite fails. (Two packets have now recorded
  this same hazard about this same assertion; whether the count should be
  derived rather than asserted is OQ material, not a silent fix.)
- [ ] 3.4 The existing `dispatch-reuses-content-secret.yaml` negative KEEPS
  RAISING `shared-secret-identity` unchanged. Assert it explicitly: the lift
  must not have moved the fixture the original rule exists for.

## 4. The artifacts that already write this shape — swept, not assumed

THE SWEEP IS ITS OWN SECTION because the lesson it discharges has cost this
estate repeatedly: a settled fact is chased to the WHOLE repository, generators
and shipped artifacts included. Three writers of the binding shape were found by
grep on 2026-08-29, and one of them is executable.

- [ ] 4.1 `scripts/apply-domain-starter.py:2096-2102` — THE GENERATOR, and the
  one that matters. It emits `credentials/bindings.template.yaml` into every
  newly scaffolded domain repository. If it does not emit the `consumer:` block,
  every new domain repo is seeded with a binding the new validator warns about on
  its first run, and the field's own scaffolder is its first non-conformant
  consumer.
- [ ] 4.2 `docs/domain-factory-starter-pack.md:804-810` — the same template in
  prose, and the document that already says "Bindings belong to client or tenant
  deployments, not the domain repo. Domain repos provide templates only." The
  template it provides gains the block and the guidance beneath it gains the
  phasing.
- [ ] 4.3 `docs/credential-access-model.md:219-225` — the worked binding example,
  plus the invariant's prose home: what a declared consumer buys and the bearer
  limit that survives it, stated together as the requirement demands.
- [ ] 4.4 RE-RUN THE SWEEP AT REALIZATION rather than trusting this list. It was
  taken at one commit; `grep -rln "rotation_policy"` over tracked `*.md`,
  `*.yaml` and `*.py` is the command, and the frozen records under
  `openspec/changes/**` are correctly excluded — an active packet's own text is a
  record of what was true when it was written.

## 5. The release ritual

- [ ] 5.1 `docs/contract-versioning-policy.md` § Deprecations Currently In Force
  — an entry for the undeclared-consumer shape naming the removal version and
  the migration path, per OQ-1's recommendation. Subject to the council's ruling
  on OQ-1 and OQ-2.
- [ ] 5.2 `contracts/CHANGELOG.md` and the `credential-contracts` row in
  `contracts/manifest.yaml` — new `sha256`, `consumption_rule` extended with the
  block and its phasing.
- [ ] 5.3 THE CUT. Additive minor, allocated AT REALIZATION by merge order, not
  numbered in this packet. Bundle bumped in-cut, inventory built last, tag
  verified from an independent clone — the defect-free tag ritual, not an
  improvised one.
- [ ] 5.4 COORDINATE WITH THE OTHER WRITER ON THIS FILE.
  `add-credential-escrow-checkout` owes an additive minor on
  `contracts/schemas/xfactory-credential-contracts.schema.yaml` too. Whichever
  cuts second re-reads the file it is cutting: two additive blocks, two rows,
  one digest, and a digest computed against a stale read is a broken pin.

## 6. Gates

- [ ] 6.1 `OPENSPEC_TELEMETRY=0 openspec validate add-binding-consumer-identity --strict`
  and `--all --strict`, counted fresh.
- [ ] 6.2 `python3 -m pytest tests/ -q -m "not postgres"` — what CI runs — with
  `tests/credential_contracts` and `tests/doc-health` named explicitly because
  this change touches what they measure.
- [ ] 6.3 doc-health zero-new against a same-clock `origin/main` baseline.
- [ ] 6.4 `python3 scripts/validate-credential-contracts.py .` clean, self-test
  included.
- [ ] 6.5 `python3 scripts/verify-openxwallet-pin.py` and the release
  `verify-commit` green at the cut.

## 7. Bookkeeping and the ordering obligation

- [ ] 7.1 README OpenSpec Records: this change moves from active to archived when
  it archives.
- [ ] 7.2 **THE ORDERING OBLIGATION, AND ITS INVERSE.** This change's MODIFIED
  block is declared relative to `add-notebook-hosting-credential-custody`'s
  outcome, and that change is ACTIVE. This change SHALL NOT archive before it
  does. If the order ever inverts, the MODIFIED block CONVERTS TO `ADDED` before
  this change archives — a MODIFIED requirement promoting against canon that
  does not carry it is a silent loss, and the two open issues in that class
  (#329, #330) are why this is a stated obligation rather than an assumption
  about merge order.
- [ ] 7.3 Reconcile with `add-notebook-projection-identity` at ITS archive: the
  operated-identity generalization all three changes presume promotes then.

## 8. NOT part of this change

- **Closing the binding object.** Breaking, deserves its own deprecation minor,
  named as a successor in design §5.
- **Cross-repository reconciliation of two consumers' bindings.** No
  per-repository validator can perform it; named as a successor in design §6(ii).
- **Live binding instances.** The residency model holds: they live in the
  consuming installs, and the xFactory sync-lane and openXdox bindings remain
  their own repositories' acts.
- **The hosting record's singular custody pointer.** OQ-3; a
  `lifecycle-notebook-projection` act, not a `credential-contracts` one.
- **Reconciling a declared fetch identity against the store's actual grants.**
  A live-estate act with its own home; the requirement says the store governs.
- **Any change to `shared-secret-identity`'s behaviour on records that declare
  no consumer.** They are refused today and are refused after this change.
