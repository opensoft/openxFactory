# Tasks: add-binding-consumer-identity

Status: ratified
Ratified: 2026-08-29 by Brett Heap (repository owner) — in-session via
question prompt, with the Codex-two-heads-back verification gap in view.
Record: `review/ratification-2026-08-29.md`. Council-reviewed the same day
(§7.4 sitting: split 2–2 on the word, unanimous 4/4 that the drafted text was
not ratifiable, fifteen blocking amendments) — his ruling was ACCEPT ALL
BLOCKING, one fix round, ratification read after; this text is that round.

**RATIFICATION HAS HAPPENED; REALIZATION HAS NOT.** The sequence Brett
authorized on 2026-08-29 ran in full: author the packet → a §7.4-shaped council
read it adversarially, convened OUTSIDE the clearance pipeline → Brett ruled
ACCEPT ALL BLOCKING → one fix round → the ratification read. **§1–§7 are now
AUTHORIZED and none of them has been performed.** They carry the contract-release
ritual, and the change stays ACTIVE until merged code, green evidence and the cut
exist.

**No task here creates, moves, or reads a live secret.** The block this change
adds holds identifiers; it holds no credential material, and its realization
touches no vault.

**EVERY TASK PRESCRIBING A SCHEMA SHAPE CARRIES A BUILT-AND-DRIVEN FIXTURE, NOT
A DESCRIPTION.** This is the round's own lesson, recorded as an obligation
because a prescription that a bench had to BUILD in order to find its defect is a
prescription that should have shipped with the build. Two Copilot reviews, three
author self-catches and a Codex P1 round all read §1 and missed what four seats
found by executing it.

## 0. The council round — DONE, and what it changed

- [x] 0.1 Council review of this packet, §7.4-shaped: independent seats,
  return-cited ballots, convener ballot, record filed with the 2026-08-28
  gate-rules convening's own. Commissioned outside the clearance pipeline BY
  DESIGN. **Held 2026-08-29 at `e6da07a4`. SPLIT 2–2 on the verdict word,
  UNANIMOUS 4/4 that the text as drafted was not ratifiable**; fifteen blocking
  amendments across four seats; `split_vote: park_for_liaison` engaged for the
  first time in that body's history.
- [x] 0.2 **Brett's ruling, 2026-08-29: ACCEPT ALL BLOCKING AMENDMENTS; one fix
  round; the ratification read follows.** Every blocking amendment is carried in
  this revision, every non-blocking one is taken or refuted from the record with
  a disposition, and the convener's own finding (#329/#330 closed, asserted open
  at four sites) is corrected with D-1's third ground re-derived. Reversals are
  recorded AS reversals: two seats re-aimed their own B12 answers mid-round and
  both are quoted rather than smoothed.
- [x] 0.3 Ratification act by Brett Heap, recorded under `review/` in this
  packet, naming what the citation covers and what it does not. **DONE
  2026-08-29** — `review/ratification-2026-08-29.md`. Ratified WITH the
  Codex-two-heads-back verification gap in view; he chose to ratify rather than
  wait for a bot whose usage limit had refused six requests. The record names the
  bundle drift and requires the figure re-read at realization, since the
  compatibility argument is indexed to a bundle and main has moved.

## 1. The schema — one block, DECLARED here and CONSTRAINED at the major

- [x] 1.1 Add `consumer:` to each entry of `credential_bindings` in
  `xfactory_credential_binding_template`
  (`contracts/schemas/xfactory-credential-contracts.schema.yaml`) as a
  **DESCRIBED, UNCONSTRAINED property**: no `type`, no `required:`, no
  `additionalProperties`, no member `pattern`. The description names the members
  and states that every constraint lands at the major. Members described:
  `holder_ref`, `fetch_identity`, `requirement_ref` (an object of
  `requirement_id` + `requirements_document_ref`), `shared_credential_acknowledged`,
  `instantiation_stub`.
- [x] 1.1a **DO NOT CONSTRAIN THE BLOCK AT THIS CUT — NOT ONE OF THE THREE
  ACTS.** The binding object is open today, so a domain may already hold a
  `consumer:` value of ANY shape. `required: [holder_ref, fetch_identity]`,
  `additionalProperties: false` and the identifier `pattern` are each a
  narrowing, and each therefore breaking. **The earlier draft of this task
  deferred only the second, and four council seats independently proved by
  construction that the other two refuse shapes the current major accepts** — a
  locally shaped object, a scalar, a list and the generator's own placeholder
  style — while `spec.md`'s scenario promised they stay valid. All three land
  TOGETHER at the major.
- [x] 1.1b **THE BUILT-AND-DRIVEN FIXTURE FOR THIS TASK, written WITH the task
  and not deferred to realization.** Build the prescribed minor schema and drive
  every shape a domain could already hold: an object with neither declared
  member, a scalar, a list, placeholder-styled values, an undeclared extra
  member, and no block at all. **All six MUST validate at the minor**, and the
  same six MUST behave as §1.4 specifies at the major. This is the check whose
  absence let the defect through.
- [x] 1.2 The block stays OPTIONAL on the binding and the binding object stays
  UNCLOSED. Closing the binding object is a further breaking act and is NOT this
  change.
- [x] 1.3 **Constrain the `credential_bindings` MAP KEY** to the identity-brokering
  identifier grammar (`^[A-Za-z0-9][A-Za-z0-9._:/-]*$`, 1–200). This is not
  cosmetic: it is a precondition of §2.3's sixth lift condition, which requires a
  reference's `requirement_id` to EQUAL its binding's key. The answer to an
  unenforced convention is to enforce it, not to discard it and trust something
  weaker.
  **AND IT PHASES, LIKE EVERY OTHER NARROWING HERE — this task said nothing
  about phasing while its two neighbours did, and a bot round caught the
  asymmetry.** The map accepts arbitrary keys today. Measured: of five plausible
  existing keys, `corpus content write`, `m365-admin (legacy)`,
  `_leading_underscore` and `sync.lane#1` are all VALID today and all REFUSED by
  the grammar. Imposing it at the minor would refuse four shapes the current
  major accepts and falsify this packet's own nothing-narrows claim — **the
  fourth instance of the exact defect the council convened over, arriving inside
  the fix round for it.** So: `consumer-binding-key-grammar` WARNS at this minor,
  the grammar is enforced only at the major, and the deprecation entry names it
  with the others. **The sixth lift condition is unaffected at the minor**: it
  compares `requirement_id` to the key as a STRING, which needs no grammar to be
  equal — the grammar's job is to stop a key being a shape the comparison cannot
  express, and that job is a major-release job.
- [x] 1.4 **Close `access_mode` to a declared vocabulary** on
  `xfactory_credential_requirements`. It is `{type: string}` today with no
  `enum`, read by one line comparing to one exact spelling — so two ABSENT modes
  compare equal and a variant spelling compares equal to itself, and a security
  seat drove both into a granted lift. The vocabulary's initial members are the
  values already in the wild (`dispatch_only`, `contents_write`,
  `workload_identity`, `delegated_api`); adding one is its own additive act.
  **This is itself a narrowing of an existing field and therefore phases the same
  way**: a value outside the vocabulary WARNS at this minor and is refused at the
  major, and the deprecation entry names it with the others.
- [x] 1.5 **Give `requirements_document_ref` a grammar**: repository-relative,
  no leading `/`, no `..` segment, `.yaml`/`.yml` suffix, no foreign-repository
  prefix. Inherited from identity-brokering it is an unconstrained string that no
  script and no test in this repository resolves; promoting it to a resolution
  input feeding a security precondition without a grammar would rest that
  precondition on a second unenforced convention. Verified by construction:
  `../x.yaml`, `/etc/x.yaml` and `OpsxFactory:credentials/r.yaml` are refused by
  the pattern. Phases with the rest.
- [x] 1.6 **The stub exemption is the declared const-true `instantiation_stub`
  token**, never a `*.template.yaml` / `*.example.yaml` filename. A filename is
  author-chosen, invisible in the bytes a pinned consumer validates, and
  UNREACHABLE by a pinned schema — which is why the drafted validator-layer
  exemption could not have covered a schema-layer refusal. At the major the
  schema expresses it as `if not required(instantiation_stub) then
  required(holder_ref, fetch_identity)`; verified by construction to accept a
  token-bearing stub and refuse an incomplete non-stub.
- [x] 1.7 Write the block's `description` to carry its own reasoning, on this
  schema's established style: why the block is declared rather than left as the
  free key it already is, why the acknowledgment and the stub token are
  const-true, why a persona is not admissible in `holder_ref`, and **what lands
  at the major**.

## 2. The validator — a warning channel it does not have, and eight deprecation codes

- [x] 2.1 BUILD THE WARNING CHANNEL FIRST. `scripts/validate-credential-contracts.py`
  prints `ERROR` and counts errors; it has no warning severity at all, so the
  deprecation posture is currently inexpressible there. Eleven sibling
  validators have one — follow `scripts/validate-client-identity-roster.py`'s
  `warn(code, msg) -> "WARN  [{code}] {msg}"` shape rather than inventing a
  fourth.
- [x] 2.2 `consumer-identity-undeclared` — WARNING on a binding with no
  `consumer:` block, naming the release at which it becomes an error. ERROR only
  at that major. Does not fire on a record declaring `instantiation_stub: true`.
- [x] 2.2a `consumer-block-unknown-member` — WARNING on a member outside the
  declared set. Same phasing, same clause.
- [x] 2.2aa `consumer-block-incomplete` — WARNING on a `consumer:` block that
  EXISTS but omits `holder_ref` or `fetch_identity`. **This code was missing and
  a bot round found the hole by enumerating what `consumer: {}` matches: not
  2.2 (the block is present), not 2.2a (no unknown member), not 2.2b (no
  malformed value) — so an empty or half-filled block would have upgraded through
  the whole minor UNWARNED and then been refused at the major.** That is the
  requiredness change landing without the full warning release
  `docs/contract-versioning-policy.md:250-254` mandates, and it contradicted this
  packet's own delta text, which already promises a warning for exactly this
  shape. Does not fire on a record declaring `instantiation_stub: true`.
- [x] 2.2b `consumer-member-grammar` — WARNING on a `holder_ref` or
  `fetch_identity` whose value does not match the identifier grammar. Same
  phasing. **This code exists because the member grammar is one of the breaking
  acts deferred to the major**: without it the grammar would be unserved by any
  deprecation, and the major could not land on the policy's own precondition.
- [x] 2.2c `consumer-token-not-true` — WARNING on a const-true token
  (`shared_credential_acknowledged`, `instantiation_stub`) declared FALSE. The
  delta originally made this an immediate ERROR; a bot round pointed out that
  `consumer: {shared_credential_acknowledged: false}` VALIDATES on the current
  major (verified), so refusing it in a minor is a new refusal like any other.
  It warns now, errors at the major. **Withholding the LIFT from such a pair is
  a different act and needs no phasing** — the lift requires the token declared
  TRUE, and declining to grant an exemption is not refusing a record.
- [x] 2.2d `consumer-binding-key-grammar` — WARNING on a `credential_bindings`
  map key outside the key grammar (§1.3). Errors at the major.
- [x] 2.2e `consumer-access-mode-vocabulary` — WARNING on an `access_mode`
  outside §1.4's closed vocabulary. Errors at the major.
- [x] 2.2f `consumer-requirement-ref-grammar` — WARNING on a
  `requirements_document_ref` outside §1.5's path grammar. Errors at the major.
  **2.2e and 2.2f exist because a bot round found that §1.4 and §1.5 declared
  their phasing and then had no code to serve it** — a constraint that phases in
  prose but warns through nothing crosses the minor silently and fails at the
  major with the deprecation unserved. **EIGHT codes now, and the set is
  enumerated against the refusals rather than counted**: every shape the major
  refuses has exactly one warning that names it.
- [x] 2.3 `shared-secret-identity` — keep the predicate and the refusal as the
  DEFAULT, and add the SIX-condition lift exactly as the requirement states it,
  each condition failing closed. **The sixth condition — the resolved
  `requirement_id` EQUALS the binding's map key — is not optional and is not a
  refinement.** Without it the lift is satisfied by the author's own choice of
  where to point, and a security seat drove exactly that: the packaged negative
  `dispatch-reuses-content-secret.yaml`, this capability's only red proof of
  serving-tier separation, was LIFT GRANTED with its shared secret untouched by
  pointing both references at the content requirement. A test per condition, each
  proving the refusal STANDS when only that condition is missing.
- [x] 2.3a **The arity is EVERY PAIR, and the inherited shape is REPLACED not
  extended.** `validate-credential-contracts.py:116` keeps `seen[secret_ref] =
  FIRST binding name` and never rewrites it, so with three bindings on one
  secret the pair (b,c) is never examined — and a record where b and c share a
  fetch identity ships the authority collapse and is accepted on both examined
  pairs. Rewrite the loop to compare every pair. A test drives three bindings on
  one secret with the second and third sharing a fetch identity.
- [x] 2.3b **An unreadable access mode makes the lift UNAVAILABLE**, never "equal
  and not dispatch-only". Absent, non-string, or outside §1.4's vocabulary on
  EITHER resolved record. Tests for all three, including the two-absent case
  (which must NOT compare equal to itself) and the variant-spelling case.
- [x] 2.4 `shared-authority-identity` — NEW error: two bindings declaring
  DIFFERENT `holder_ref`s and the SAME `fetch_identity` in one document. The
  message names two systems on one authority and does not mention secret reuse,
  and where it applies it REPLACES the default finding for that pair rather than
  accompanying it. **It is NOT scoped to a shared `secret_ref`** — that predicate
  is a proxy the design already concedes is not the rule, and scoping to it
  leaves the same collapse unreported when two spellings name one secret. A test
  asserts the negative direction too: ONE holder reusing its own fetch identity
  across its own bindings produces nothing.
- [x] 2.5 **Resolution, constrained.** The QUALIFIED `requirement_ref` resolves
  ONLY against `xfactory_credential_requirements` records the validator itself
  discovered and schema-checked in the scanned tree. **The validator NEVER opens
  a path taken from a record.** ZERO matches AND MORE THAN ONE match both report
  and withhold the lift — never pass silently, never disambiguate by picking one:
  requirement ids carry no repository-wide uniqueness, two matches may differ in
  `access_mode`, and a rule whose outcome depends on traversal order is not a
  rule. Tests: the two-match case with DIFFERENT access modes; a document
  reference that resolves to nothing; and one that names a repository other than
  the one under validation.
- [x] 2.6 **Screen the two new sinks.** `_looks_like_raw_secret` reads
  `binding["secret_ref"]` and nothing else, so a raw token in
  `consumer.holder_ref` or `consumer.fetch_identity` produces ZERO findings
  today — two new unscreened free-string sinks on the one record kind whose
  invariant is "never bake a secret", and the borrowed identifier grammar admits
  `ghp_…` and `AKIA…` shapes. Extend the screen to both fields under the existing
  `baked-secret` code, with ONE REGISTERED NEGATIVE PER FIELD. Note while doing
  it that `_B64ISH` requires 40 characters, so a 38-character alphanumeric secret
  passes the screen even once applied — record that as a known limit rather than
  claiming coverage the check does not have.
- [x] 2.7 A mutation round over §2.3–§2.5, one mutant per condition, each
  mutant's death asserted by a NAMED test. **THE CONTROL IS A BASELINE, NOT A
  NAME.** Naming the killing test fixes attribution; it does NOT detect
  ANCHOR-MISSING, where the named test fails on the mutant because its fixture or
  assertion target is absent rather than because the mutation was caught. So per
  mutant, record BOTH: the named test PASSES against unmutated code, and FAILS
  against the mutant. **The mutant population is an explicit count** — nine: six
  lift conditions, the every-pair arity, the unreadable-access-mode arm, and the
  resolution-ambiguity arm.

## 3. Packaged fixtures — including the one the predecessor had to decline

- [x] 3.1 POSITIVE: two consuming systems reaching one operated identity in one
  template — the fixture the custody change DECLINED because the unsharpened rule
  refuses it. It carries all six lift conditions, including each reference's
  `requirement_id` equal to its own map key. **SYNTHETIC IDENTIFIERS, RULED BY
  BRETT 2026-08-29**: it MUST NOT name the live xFactory sync-lane or openXdox
  fetch identities. Those stay in the consuming installs' own `credentials/`
  trees. See §3.5.
- [x] 3.2 NEGATIVES, one per named refusal: same fetch identity with different
  holders; same holder reference; one-sided acknowledgment; acknowledgment valued
  false; stub token valued false; a dispatch/content pair declaring itself
  shared; a pair whose references do not equal their own map keys; a reference
  resolving to nothing; a reference resolving to TWO records with different
  access modes; a reference that is absolute, escaping, or foreign-repository; a
  resolved requirement with an absent access mode; three bindings on one secret
  with two sharing a fetch identity; a raw secret in `consumer.holder_ref`; a raw
  secret in `consumer.fetch_identity`. Each registered in `NEGATIVE_EXPECTATIONS`
  — an unregistered negative is reported by the self-test as having no
  expectation.
- [x] 3.2a **A RECORD WEARING A STUB NAME IS A NEGATIVE.** A binding carrying
  live values in a file named `*.template.yaml` and NOT declaring
  `instantiation_stub` must be treated as a record: it warns now and is refused
  at the major, exactly as if it were named anything else. This fixture is what
  proves the exemption moved off the filename.
- [x] 3.3 **WARNING FIXTURES NEED A HOME THAT DOES NOT EXIST YET, and building it
  is part of this change.** Measured: a warning fixture placed among the
  positives fails the self-test as *"unexpectedly invalid"*, and placed in
  `negative/` fails it as *"has no registered expectation"* — the corpus has no
  third channel. Add a `warning/` directory and a `WARNING_EXPECTATIONS` map so
  **all EIGHT codes** carry a packaged probe: `consumer-identity-undeclared`,
  `consumer-block-incomplete`, `consumer-block-unknown-member`,
  `consumer-member-grammar`, `consumer-token-not-true`,
  `consumer-binding-key-grammar`, `consumer-access-mode-vocabulary` and
  `consumer-requirement-ref-grammar`. **A deprecation the major depends on cannot
  be evidenced by a corpus with no place to hold its proof**, and a corpus that
  probes SOME of the codes is worse than one that probes none, because the
  major's preconditions then LOOK evidenced. A bot round caught this list at
  three of eight; the coverage rule is now stated as a rule — **one registered
  probe per warning code, checked by count against the code list itself**, so the
  next code added cannot silently ship unprobed.
- [x] 3.4 THE SELF-TEST COUNT STRING AND THE BY-NAME INVENTORY.
  `tests/credential_contracts/test_dispatch_credential_contract.py:35` asserts
  `"self-test: 3 positive + 5 negative example(s) confirmed"` verbatim. **Ruled:
  DERIVE the count**, in its own `credential-contracts` test-hygiene issue rather
  than here — the by-name inventory at `:38-51` already dominates it. **The
  condition is not optional: every fixture this change adds joins that by-name
  inventory in the SAME COMMIT**, including the new `warning/` members. Deriving
  the count without that is fail-open and would silently accept a shrinking
  corpus of security probes.
- [x] 3.5 **NO LIVE IDENTIFIER IN THE PACKAGED CORPUS — RULED, NOT PARKED.** The
  corpus is digest-pinned and distributed to every consumer that pins the
  contract, and a declared `fetch_identity` beside a `vault` and a `secret_ref`
  publishes which principal reaches which secret. **Brett ruled on 2026-08-29:
  packaged fixtures use SYNTHETIC identifiers.** A security seat had parked the
  question under its own escalation rule (P-2, LS-C1) because it turns on the
  repository's audience; the liaison has now decided it, so P-2 is DISCHARGED
  rather than open. The live xFactory sync-lane and openXdox fetch identities
  stay in the consuming installs' own `credentials/` trees — where the residency
  model already puts an estate fact, and where the readership is the install's
  rather than every pinning consumer. A grep of the packaged corpus for the live
  identifier strings rides with §6.4.
- [x] 3.6 The existing `dispatch-reuses-content-secret.yaml` negative KEEPS
  RAISING `shared-secret-identity`. Assert it EXPLICITLY and assert it the way
  the seat broke it: add the four declarations that granted the lift under the
  five-condition draft and prove condition 6 refuses them. The earlier task
  asserted this property against a fixture that declares no consumer at all,
  which is a non-test.

## 4. The artifacts that already write this shape — swept, not assumed

THE SWEEP IS ITS OWN SECTION because the lesson it discharges has cost this
estate repeatedly: a settled fact is chased to the WHOLE repository, generators
and shipped artifacts included. **The earlier draft of this section reported
THREE writers while its own prescribed command returns THIRTEEN paths** — an
incomplete sweep inside the section written to discharge the incomplete-sweep
lesson. All thirteen are listed below with a stated in/out disposition, because
the section's authority comes from being exhaustive.

- [x] 4.1 `scripts/apply-domain-starter.py:2096-2102` — **THE GENERATOR EMITS
  `consumer: {instantiation_stub: true}` AND NOTHING ELSE.** Not placeholders,
  not a bare comment. Three drafts converged here and the last two were both
  wrong for opposite reasons. Draft one emitted the block in the template's own
  `<placeholder>` style, which FAILS the identifier grammar. Draft two emitted no
  block at all — and a bot round showed **that cannot stay clean either**: §2.2
  makes a missing block an ERROR at the major, and the only exemption is the
  stub token, so a scaffolded repository would be refused the moment requiredness
  activates and §6.2's assertion would become impossible. Verified by
  construction: the token alone validates at the minor AND at the major, and a
  blockless template validates at the major's SCHEMA but is refused by its
  VALIDATOR.
  **The token is the honest emission, not a third sentinel.** A placeholder
  `holder_ref` claims an identity that does not exist; `instantiation_stub: true`
  claims only that this record is a stub, **which is exactly true of a file the
  generator writes before any install exists.** Scaffolding that manufactures
  conformance is worse than scaffolding that omits it — and scaffolding that
  DECLARES ITS OWN STATUS is better than either.
- [x] 4.2 `docs/domain-factory-starter-pack.md:804-810` — the same template in
  prose. Same treatment: the stub token, not a placeholder and not an omission,
  with the one-line explanation of what an instantiator replaces it with.
- [x] 4.3 `docs/credential-access-model.md:219-225` — the worked binding example,
  plus the invariant's prose home. **AND `:228-229`'s sentence — "It must not
  include the raw secret value" — is extended to the new fields in the SAME
  commit**, because this change doubles the record's free-string surface and that
  sentence is the record's only content discipline. Note in passing that this
  document is itself `Status: draft`, so "prose home" is not a claim of settled
  standing.
- [x] 4.4 `contracts/avatar-client/broker-server-key-binding.template.yaml` —
  **A FOURTH WRITER, of the exact record kind, CHECKED AND EXEMPT.** It declares
  `kind: xfactory_credential_binding_template`, carries
  `resolution.fetch_identity` and a top-level `requirement_id`, validates against
  the pinned schema with zero errors, and carries no `consumer:` key. It is
  exempt because it is a `.template.yaml` under a tree
  `validate-credential-contracts.py` never scans, and because
  `validate-avatar-client.py` refuses a second binding in it so the lift can
  never reach it. **On the record as checked-and-exempt rather than unmentioned**,
  and the second validator reading one kind with divergent rules is named as an
  owed successor, not scoped in.
- [x] 4.5 IN/OUT for the remaining nine paths the command returns:
  `README.md` (OUT — index prose, already edited by this change);
  `contracts/avatar-client/README.md` and
  `contracts/avatar-client/broker-server-key-rotation-policy.yaml` (OUT — avatar
  family surface, not this kind's shape);
  `contracts/schemas/xfactory-credential-contracts.schema.yaml` (IN — §1);
  `examples/credential-contracts/openxdox-dispatch.binding-template.example.yaml`
  and the two `examples/credential-contracts/negative/` binding records (IN — the
  packaged corpus, §3, and they are what the self-test counts);
  `scripts/validate-avatar-client.py` and
  `tests/avatar_client_validator/test_section7_pinned_values.py` (OUT — the
  second validator and its pin, scoped out with §4.4).
- [x] 4.6 RE-RUN THE SWEEP AT REALIZATION rather than trusting this list. The
  command, reproducible as written rather than as described:
  `git grep -l "rotation_policy" -- '*.md' '*.yaml' '*.py'
  ':(exclude)openspec/changes/**'`. Broaden it once with `credential_bindings`
  too, which returns eighteen, and dispose of the difference.

## 5. The release ritual

- [x] 5.1 `docs/contract-versioning-policy.md` § Deprecations Currently In Force
  — **UNCONDITIONAL, not "subject to the council's ruling": the council ruled
  YES, unanimously, and two seats escalated it to load-bearing.** The entry names
  the removal version, the migration path, and **EVERY act that lands there** —
  all EIGHT deprecation codes
  (`consumer-identity-undeclared`, `consumer-block-incomplete`,
  `consumer-block-unknown-member`, `consumer-member-grammar`,
  `consumer-token-not-true`, `consumer-binding-key-grammar`,
  `consumer-access-mode-vocabulary`, `consumer-requirement-ref-grammar`) and the
  acts they serve — the member requiredness, the block's closure, the member
  grammar, the const-true token enforcement, the `credential_bindings` map-key
  grammar, the `access_mode` vocabulary and the `requirements_document_ref`
  grammar. **The entry is written from the refusal list, not from memory**: every
  shape the current major accepts and the next one refuses owes its minor of
  warnings, and the entry is the only place a reader learns they are one act.
  Without it, at the major nothing can demonstrate the policy's own precondition
  was met and the requiredness becomes unauditable.
- [x] 5.1a **THE ENTRY GATES THE MAJOR ON THE DEGRADED MODE.** It states that
  the requiredness does not land until the degraded fetch-identity mode is
  declarable. A security seat ruled against keeping OQ-5 out: at the major an
  install with no per-install fetch identity must write SOMETHING into a required
  field, and what it will write is the shared service identity, silently — the
  grammar-passing placeholder this packet itself calls worse than omission,
  arriving through the front door of the field it adds. This is that seat's own
  second branch, taken.
- [x] 5.1b **FIRST CHECK WHETHER THE MECHANISM IS TRUSTWORTHY.** Three entries in
  that same section still carry `removal target contract-v2.0` while the bundle
  is past it, with no matching § Deprecations Executed rows. Whoever writes 5.1
  checks whether they are overdue-and-forgotten, because that is the same
  mechanism this new entry will rely on to retire itself. Not a condition on this
  packet; a condition on trusting what it is about to lean on.
- [ ] 5.2 `contracts/CHANGELOG.md` and the `credential-contracts` row in
  `contracts/manifest.yaml` — new `sha256`, `consumption_rule` extended with the
  block and its phasing.
  **HALF DONE IN THE REALIZATION COMMIT, HALF OWED TO THE CUT, and the split is
  stated rather than left to be inferred.** The manifest row is DONE: its
  `sha256` is recomputed over the moved schema bytes and its `consumption_rule`
  now carries the block, the seven acts and the deprecation pointer — that half
  cannot wait, because a row whose digest does not match the file it registers
  publishes a promise about bytes nobody shipped, and §5.4's gate reds on it.
  The `contracts/CHANGELOG.md` entry is NOT written, because it is written
  UNDER the bundle heading the cut allocates and writing it earlier would spend
  a number this packet deliberately does not number. It lands with §5.3.
- [ ] 5.3 THE CUT. Additive minor, allocated AT REALIZATION by merge order, not
  numbered in this packet. Bundle bumped in-cut, inventory built last, tag
  verified from an independent clone.
  **NOT PERFORMED BY THE REALIZATION COMMIT, DELIBERATELY.** Allocation is by
  MERGE ORDER, and this branch is not merged; a number written before the merge
  is a number the next packet to land would have to renumber. Until the cut, the
  `release-inventory-drift` family reports the moved members of the standing
  bundle — the schema, the manifest, the policy — which is the family working as
  designed rather than a defect, and is what the cut discharges.
- [x] 5.4 **COORDINATE WITH THE OTHER WRITERS — MACHINE-CHECKED, BECAUSE A
  ONE-SIDED OBLIGATION IS NOT COORDINATION.** `add-credential-escrow-checkout`
  owes an additive minor on this same file, is RATIFIED and therefore frozen,
  makes no mention of this change, and carries no concurrent-writer re-read in
  any of its nine schema tasks — so telling "whichever cuts second" to re-read
  binds only this packet. **Build the invariant instead**: a realization gate
  that recomputes the `credential-contracts` row digest from the file on disk at
  cut time and refuses a mismatch. It binds both parties without editing a frozen
  packet. **And there are THREE writers, not two** — main moved
  `contracts/manifest.yaml` 27/11 between this branch's merge-base and today.
  Reconcile the two fixture trees before either cut: `EXAMPLES_DIR` is one
  hard-coded path and escrow places its fixtures under a new
  `contracts/credentials/examples/`.

## 6. Gates

- [x] 6.1 `OPENSPEC_TELEMETRY=0 openspec validate add-binding-consumer-identity --strict`
  and `--all --strict`, counted fresh against an independently reconciled
  baseline.
- [x] 6.2 `python3 -m pytest tests/ -q -m "not postgres"` — what CI runs — with
  `tests/credential_contracts` and `tests/doc-health` named explicitly. **Includes
  the scaffolded-repo assertion**: generate a repo with
  `apply-domain-starter.py`, run the validator over it, and require CLEAN **at
  BOTH releases — the introducing minor and the major** — because a scaffold that
  is clean only until requiredness activates is a scaffold that breaks every new
  domain repository on the upgrade. Under §4.1 that passes because the generator
  emits the stub token; under the first draft it could not pass at the minor
  (the placeholder fails the grammar) and under the second it could not pass at
  the major (a missing block is an error there). The two-release form of this
  assertion is what makes the difference visible, and the test is RUN, not
  asserted.
- [ ] 6.3 doc-health zero-new against a same-clock `origin/main` baseline.
  **MEASURED AND NOT ZERO, AND THE TWO IT IS NOT ARE BOTH THE CUT'S.** Run
  same-clock against `origin/main` from an identically-named checkout (the
  identity is `(family, repo, path)` and the repo is the basename, so a
  differently-named baseline manufactures phantoms): baseline 4 critical /
  4 error / 28 warning / 12 info; branch 4 critical / 5 error / 28 warning /
  13 info. The delta is exactly TWO findings, both `release-inventory-drift`
  against the standing `contract-v2.3` inventory — `docs/contract-versioning-
  policy.md` (error) and `contracts/manifest.yaml` (info, editorial band) —
  and the family's own remedy line is *"cut a release through the bundle
  realization order; never hand-edit an inventory or `contract_bundle_version`
  to make this comparison pass."* So this box is UNTICKED rather than ticked
  with an excuse: it is discharged BY §5.3, in the same act, and hand-editing
  it green now is the one thing the family forbids. Every other family is
  unmoved. (`contracts/schemas/xfactory-credential-contracts.schema.yaml` is
  not an inventory member, so the schema edit drifts nothing.)
- [x] 6.4 `python3 scripts/validate-credential-contracts.py .` clean, self-test
  included. Note it reports `0 contract(s) checked` against openxFactory's own
  root, because the repository ships no `credentials/` tree — so this gate is
  satisfied almost entirely by the SELF-TEST, which is what puts the whole weight
  on §3's packaged corpus.
- [ ] 6.5 `python3 scripts/verify-openxwallet-pin.py` and the release
  `verify-commit` green at the cut.
  **FIRST HALF DONE, SECOND HALF IS THE CUT'S BY ITS OWN WORDING.**
  `verify-openxwallet-pin.py` passes on this branch —
  `openXwallet@6b248d40` (tag label `wallet-v1.3`), gitlink read from HEAD,
  8 digests recomputed. `verify-commit` is GREEN on `origin/main` and reports
  the same two members §6.3 names on this branch; "green AT THE CUT" is
  satisfied when §5.3 rebuilds the inventory, not before.

## 7. Bookkeeping and the ordering obligation

- [ ] 7.1 README OpenSpec Records: this change moves from active to archived when
  it archives.
- [ ] 7.2 **THE ORDERING OBLIGATION, AND THE BACKSTOP THAT RUNS.** This change's
  MODIFIED block is declared relative to `add-notebook-hosting-credential-custody`'s
  outcome, and that change is ACTIVE. This change SHALL NOT archive before it
  does; if the order ever inverts, the block CONVERTS TO `ADDED` first, because a
  MODIFIED requirement promoting against canon that does not carry it is a silent
  loss. **A prose task in a class the checker provably cannot see is not a
  control**, and it was measured that the checker cannot: this block's group has
  size ONE and always will, since `_arm_ordering` needs two RATIFIED *MODIFIED*
  blocks and the custody block is ADDED. In the safe order the carriage arms run;
  in the unsafe order nothing checks anything. **So the archive checklist carries
  a mechanical assertion** that `openspec/specs/credential-contracts/spec.md`
  contains the requirement title before this change archives — one `grep`, which
  fails loudly in exactly the inverted order.
- [ ] 7.3 Reconcile with `add-notebook-projection-identity` at ITS archive: the
  operated-identity generalization all three changes presume promotes then.
- [ ] 7.4 **RE-RUN THE CARRIAGE DIFF IF THE MODIFIED BLOCK IS TOUCHED AGAIN.** A
  losslessness measurement does not survive an edit; verify-then-regress is a
  shape this estate has already paid for. It was re-run after this amendment
  round — six scenarios in, six out, five byte-identical, one changed body
  paragraph a strict prefix of its successor, title byte-identical, zero units
  lost — and it is re-run after any later edit to that block.

## 8. NOT part of this change

- **Closing the binding object.** Breaking, deserves its own deprecation minor,
  named as a successor in design §5.
- **Constraining the `consumer:` block at this release.** Declared here; all
  three constraining acts execute at the major, in one window.
- **Cross-repository reconciliation of two consumers' bindings.** No
  per-repository validator can perform it; named as a successor in design §6(ii).
- **Reconciling the two validators that read `xfactory_credential_binding_template`.**
  `validate-avatar-client.py` is the avatar family's surface; the divergence is
  an owed successor, named in design §1 rather than widened in silence.
- **A home for the MODIFIED-over-a-sibling's-ADDED gap — FILED AS ISSUE #502.**
  No governing requirement, no evaluating arm, no marker; FOUR live PENDING pairs
  measured on `origin/main` `3b342561` (the seats' "eight" is the cumulative
  figure, being the family docstring's historical seven plus this block). Two
  seats raised it as owed a home of its own and both said this change must
  neither close it nor be delayed for it; **Brett ruled on 2026-08-29 that the
  successor be filed now**, and #502 is that filing. This change carries only its
  own local stopgap — §7.2's pre-archive assertion — and does not wait on #502.
- **The self-test count derivation.** Ruled DERIVE; filed as its own
  `credential-contracts` test-hygiene issue.
- **Live binding instances.** The residency model holds: they live in the
  consuming installs, and the xFactory sync-lane and openXdox bindings remain
  their own repositories' acts.
- **The hosting record's singular custody pointer.** OQ-3; ruled leave-singular
  and route out, WITH a named home as an owed successor, carrying the seat's
  caution that a singular pointer beside a multi-consumer record lets an operator
  evict one of two consumers believing they evicted the access.
- **Reconciling a declared fetch identity against the store's actual grants.**
  A live-estate act with its own home; the requirement says the store governs.
- **~~Whether the packaged corpus may name LIVE fetch identities.~~ RULED
  2026-08-29 — SYNTHETIC identifiers, and the live ones stay in the installs.
  No longer parked; see §3.5.**
- **Any change to `shared-secret-identity`'s behaviour on records that declare
  no consumer.** They are refused today and are refused after this change.
