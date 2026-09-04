# Design — admit-deliberation-clearing-operation

Status: draft

Every decision below beyond D1's two ruled inputs was the authoring session's
and is flagged for the ratifier's veto.

## D1. What is ruled, and what is not

**RULED (a), 2026-09-01 — the boundary itself.** Brett Heap's clearing-boundary
ruling (operator workspace `cpc-clearing-boundary-ruling-2026-09-01.md`;
`opensoft/codexFactory` issue #156) produced `add-clearing-dispatch-boundary`
and `add-cpc-clearing-boundary`. It made the register CLOSED and made admission
a governed change. codexFactory PR #165 encodes its deliberation half and files
this packet as its task 1.6.

**RULED (b), 2026-09-04 — OQ1.** Verbatim: *"Ruling OQ1: new neutral
deliberation-return schema"*. Recorded as a Lane Collision Protocol Rule 2
ruling comment on codexFactory PR #165
(https://github.com/opensoft/codexFactory/pull/165#issuecomment-5535775096),
targeting lane `hermes-wallet-exercise`'s claim
(https://github.com/opensoft/codexFactory/pull/165#issuecomment-5535747335) on
the `deliberation` register member. See D4.

**NOT RULED:** everything else here — D2, D3, D5, D6, D7, D8, D9, D10, D11.

## D2. ONE requirement, and it mirrors entry number one

The basis writes entry number one as its OWN requirement — *"readiness-diagnostic
is register entry number one and is strictly read-only"* — separate from *"The
permitted-operations register is closed"*, which states the rule. That split is
worth keeping: the rule requirement says what an entry must declare and what
admission costs; a per-entry requirement says what THIS operation is, in one
place a reviewer can read whole and a later widening can be diffed against.

So entry number two is one requirement, titled in the same voice, declaring the
same fact list in the same order. The alternative — folding the entry into a
MODIFIED block over the closure requirement — was rejected for three reasons:
it would restate a ratified requirement to append a member (the exact
"re-authored the basis" defect adversarial review caught in
`add-cpc-clearing-boundary`'s withdrawn draft); it would need the reserved
`Modified over` marker and a currency warning while the basis is unarchived;
and it would put two entries' declarations in one requirement, so a future
widening of one could not be reviewed without re-reading the other.

## D3. ARTIFACT LANE ONLY

Entry number one declares BOTH lanes because a readiness probe is asked about
both hosts. Deliberation is asked about neither: it runs council seats, which is
artifact work, and the grandfathered lane it displaces —
`council-deliberation-worker.yml` — is enumerated on `xfactory-artifact-workers`
(group 5) and on no other group. Declaring the coding lane too would grant a
reach nothing asks for, and the register's whole containment argument is that
what bounds a compromised producer is "which operations exist at all and what
each one is permitted to do".

The lane constants are taken verbatim from entry number one's artifact lane, so
the register cannot come to disagree with the door it describes — the instance's
own `notes` field states that hazard for entry one and it applies identically
here.

## D4. RULED (OQ1) — the declared output schema is a NEW NEUTRAL schema

**Decision: `output_schema_ref: contracts/clearing/deliberation-return.schema.yaml`,
a new neutral schema authored in openxFactory and realized at this change's
realization cut.**

The register's schema says of `output_schema_ref`: *"A return is validated
against THIS value, never against a bundle's copy of it."* The return in
question is codexFactory #165's `seat_results.json` plus its
`return-manifest.json` — the UNSIGNED per-seat outputs that the originating
repository's hosted `council-seat-signing.yml` signs on return (#165 D6). No
neutral schema for that shape exists today: `operation-report.schema.yaml` is
`readiness-diagnostic`'s composed probe report and is the wrong subject.

**The alternative, and its cost, recorded as REJECTED.** Pointing
`output_schema_ref` at a codexFactory-owned path would break the estate's first
working rule — domain-neutral contracts live in `openxFactory`, and domain repos
never author neutral contracts. Worse, it would make the PRODUCER the author of
the shape its own return is checked against, which is the bundle-trust error
this boundary exists to refuse, moved one level up: the clearing side would be
validating a return against a schema the producer can edit. A third option —
leaving `output_schema_ref` pointing at the operation report — was rejected as
plainly false, since the operation report is a different document with different
required members.

**Its `kind` is `xfactory_clearing_deliberation_return`, named in the ratified
text and not left to realization.** The family routes a record to the schema it
is validated against by its top-level `kind`, and the verdict scan is dispatched
on that same routing (D13 and task 2.5). A realization free to pick the kind
would therefore be free to pick whether the scan reaches this operation at all,
which is a policy choice wearing the clothes of an identifier. The form follows
the five kinds already shipped (`xfactory_clearing_operation_report`,
`xfactory_clearing_dispatch_record`, …); no new naming convention is minted.

**What the schema must be, minimally** (authored at realization, task 2.2): the
per-seat outputs as STRUCTURED EVIDENCE — seat identity, that seat's output
(inline payload or reference), and the run identifiers that bind the return to
the convening job id, the verified subject pin, and the INBOUND bundle digest it
answers — with `additionalProperties: false` and NO verdict, eligibility,
decision, go/no-go, approval or recommendation member. It declares no digest
construction, no handling vocabulary and no job envelope; it references the ones
already in force.

## D5. `worker_profile: council-deliberation-worker`

`worker_profile` is register-local vocabulary: entry one's `cpc-readonly-probe`
exists in this register and nowhere else — the `worker-enrollment-broker`
family's `profiles` are label-shaped flags on an enrollment request, a different
subject. So the name is chosen, not looked up.

`council-deliberation-worker` names the WORK, and it names it with the same word
the retiring grandfathered member carries (`council-deliberation-worker.yml`),
so the retirement of D10 reads as a retirement rather than as a coincidence of
two unrelated names. The profile is not a workflow path and must not be read as
one; the register's convention is a descriptive hyphenated identifier, which
this is. Rejected: `cpc-deliberation-seat-runner` (parallel to
`cpc-readonly-probe`'s `cpc-` prefix, but the prefix on entry one describes a
PROBE of the CPC rather than a class, and copying it would suggest a taxonomy
the register does not have).

## D6. `token_scopes: [actions:read]`, and the spelling is borrowed

Entry one declares `token_scopes: []` and the emptiness is its statement. Entry
two cannot: leg 3 must DOWNLOAD the re-sealed bundle from the CLEARING run, and
#165 D1 fixes the shape — `permissions: {}` on every job except the
return-fetch job, which carries `actions: read` on the CLEARING repository's own
run artifacts.

**The estate DOES have a scope spelling and this entry borrows it rather than
minting one.** `scripts/validate-credential-contracts.py` carries
`DISPATCH_SCOPES = {"actions:write", "actions:read", "metadata:read"}` for the
`credential-contracts` family's least-privilege check, and the basis already
requires the admission credential to be expressed as a `credential-contracts`
record with declared custody. `actions:read` also satisfies the register
schema's `identifier` pattern. So the machine value is `actions:read` and the
requirement states the CONSTRAINT IN WORDS beside it: exactly the clearing
side's own scoped, short-lived, read-only admission credential, sufficient to
read the clearing repository's own run artifacts and no more.

**`metadata:read` is deliberately NOT declared**, and the reason is recorded so
a realizer does not add it silently: on this provider a token carries metadata
read implicitly, so declaring it would describe the provider's floor rather than
a grant this entry makes, and a register entry that lists floors alongside
grants stops being a bound. If realization finds the operation's token carries
it as a DISTINCT, grantable scope, adding it is an amendment to this entry by
governed change — not a fix-up in the realization diff.

**And the widening that is NOT happening.** Entry one's empty list is not
touched. The basis states this in as many words — those constraints "bind THIS
operation and its job, not the clearing workflow for all time … a later
bundle-carrying operation carries the clearing side's admission credential under
its OWN entry's constraints" — and the requirement quotes that reading so the
first conformant bundle-carrying operation is not read as a violation of a
requirement about a different operation.

## D7. `data_handling: internal-governance`

The registry instance promised this: *"A bundle-carrying operation will declare
a stricter class."*

**THE ATTRIBUTION WAS WRONG IN THE FIRST DRAFT AND IS CORRECTED HERE, MEASURED
RATHER THAN ASSUMED.** That draft said the class name is `document-cataloging`'s
vocabulary. It is not, and the distinction matters because a borrowed word
credited to the wrong family is a word nobody owns and nobody maintains. What is
true, checked against the shipped text:

- The register's own schema attributes the `data_handling` FIELD's vocabulary to
  `document-cataloging`, and the instance's `composes_with` repeats it. That
  attribution is about the FIELD, and this packet does not disturb it.
- `document-cataloging` defines NO controlled set of handling class names. Its
  catalog snapshot types the member as a free string
  (`handling: {type: [string, "null"]}`), its promoted requirement says a
  document's declared handling classification "SHALL remain mechanical inventory
  fields and MUST NOT be semantically rewritten" — i.e. it COPIES the source's
  word — and what it does own is the HANDLING GATE, which decides whether a host
  is authorized for a class. `protected` reaches it as a source-declared value
  that BLOCKS dispatch (`doc_health/cataloger.py`'s protected-handling blocker),
  which is why `protected` would make this operation undispatchable by its own
  declaration.
- The class name `internal-governance` occurs nowhere in `document-cataloging`.
  It is a `Handling:` header value — the `document-lifecycle` / doc-health
  header family's word, read by `doc_health/inventory.py` and
  `doc_health/organizer_dispatch.py` off the source document — and it is the
  handling authorization the doc-health worker dispatch requires by default
  (`.github/workflows/doc-health-reusable.yml`, `worker-handling-class`), for
  exactly this material on exactly these hosts.

So the sentence the requirement carries is: the FIELD borrows its vocabulary as
the register says, and the CLASS NAME is the header value the estate's
governance corpus already travels under. This entry mints neither.

So `internal-governance` is chosen because it is TRUE and ALREADY IN USE, not
because it is the strictest word available. `restricted` would over-declare —
this is governance material, not source-policy-restricted content — and
`protected` is the class the handling gate refuses to dispatch at all, which
would make the operation undispatchable by its own declaration. The step from
`public_log_only` is the real one: entry one reports facts already visible in a
public run log; entry two carries selected source files and a governance packet
across the boundary and returns the seats' reasoning about them.

## D8. The fixtures re-point to `coding`

Two packaged negative fixtures use `deliberation` as the honest unratified name,
and admitting it would silently turn both green for the wrong reason —
`register-carrying-an-unratified-operation.yaml` would stop being refused, and
`manifest-naming-an-unregistered-operation.yaml` would name a registered
operation. A closure refusal with no live probe is a refusal nobody tests, and
the clearing gate asserts `N/N closed refusal codes red-proven`, so it would go
red.

They re-point to **`coding`** — chosen because it is honest on the same terms
`deliberation` was: a REAL, WANTED, still-unratified operation. The basis's
design D11 names it as the next real later operation and the estate already has
the lane (`xfactory-execution-lane-workers`, `host-coding-cpc-brett01`) and the
grandfathered worker (`execution-lane-coding-worker.yml`, group 7) waiting for
it. The fixtures' comments must be rewritten to say so — a fixture whose comment
still argues about `deliberation` while its bytes say `coding` is worse than
either.

`examples/dispatch-record-refused.example.yaml` follows, because its whole
subject is a REFUSED CLAIM of `deliberation` with
`refusal.ground: unregistered_operation`; after admission that record would
document a refusal that could no longer happen. `tests/clearing/test_dispatch_record.py`'s
`test_a_refusal_records_what_was_asked_for` asserts the claimed value literally
and moves with it.

## D9. FIVE frozen copies move together — the brief said two, and the count is itself the finding

The register's member set is pinned in **five** places, not two, and all five
move in one reviewed diff or the change is red:

1. `scripts/validate-clearing-dispatch.py` — `RATIFIED_OPERATIONS = frozenset({"readiness-diagnostic"})`.
2. `tests/clearing/test_register_closure.py` — `RATIFIED = frozenset({"readiness-diagnostic"})`, an INDEPENDENT copy, deliberately: *"if the validator's set were the only one, a diff that widened it would widen the test in the same motion and nothing would go red."*
3. `contracts/clearing/permitted-operations.registry.yaml` — the instance itself.
4. **`.github/workflows/clearing-dispatch-gate.yml`** — a literal grep assertion
   `permitted-operations register read: … \(1 registered operation\)`, whose own
   comment says: *"THE LITERAL COUNT IS THE POINT … If this line has to move, the
   change that moved it is a GOVERNED CONTRACT CHANGE with a spec delta and a
   ratifier — not an edit to a grep."*
5. **`tests/clearing/test_clearing_gate_wiring.py`** —
   `test_the_assertion_pins_the_registers_literal_member_count` asserts
   `"1 registered operation" in assertion`, i.e. it pins copy 4's LITERAL from a
   second file. Moving copy 4 alone turns this test red; moving both is the
   whole move.

Copies 4 and 5 were not in this packet's brief and are recorded here so
realization does not discover them as red required-adjacent surfaces after the
fact. Copy 4 lives in CI configuration rather than in the contract tree, and
copy 5 is a test ABOUT the CI configuration — two hiding places, in neither of
which a reader of `contracts/clearing/` would look.

**AND THREE FURTHER PINNED LITERALS MOVE WITH THE NEW SCHEMA**, which are not
copies of the MEMBER SET but fail exactly as loudly, and each is a numeral
somebody wrote down on purpose:

- `tests/clearing/test_schemas.py::test_the_family_ships_five_schemas` pins the
  five schema filenames as an exact list, with the docstring *"A sixth arriving
  without a change to this line is a shape nobody ratified."* This change is
  that ratification, and the list becomes six.
- `tests/clearing/test_clearing_manifest_rows.py::test_the_family_registers_exactly_the_six_members`
  pins the family's `contracts/manifest.yaml` row count at six; the new schema
  makes it seven.
- `tests/clearing/test_clearing_manifest_rows.py::test_the_row_digest_matches_the_artifact_on_disk`
  pins a per-file digest for every registered artifact, so the register
  instance's row digest AND the dispatch record schema's row digest both move
  when their bytes do (D13). A realization that edits the files and not the
  manifest is red, which is the point.

`tests/clearing/test_register_closure.py::test_deliberation_is_refused_by_name`
is a fifth surface of the same fact: it builds an unratified member NAMED
`deliberation` in memory. It re-targets to `coding` with the fixtures (D8), and
its docstring's argument — *"the failure mode is never somebody adding an absurd
operation, it is somebody adding a REASONABLE one"* — survives the rename
unchanged, because that argument was never about the word.

**THE HONEST LIMIT, CARRIED FORWARD VERBATIM IN SUBSTANCE.** The register, the
validator that reads it, the tests that pin it and the gate that greps it all
live in the same repository as the changes they police, so ONE DIFF CAN EDIT
EVERY SIDE. What the refusal guarantees is that an addition cannot be made
SILENTLY: it is a red check plus a diff touching the register, the validator, the
tests or the gate, and REVIEW OF THAT DIFF is the declared backstop. **It is a
tripwire backed by review, not an unforgeable refusal, and this packet does not
describe it as one.**

## D10. The forward retirement obligation, and why it is stated HERE

The basis's requirement *"Routing a route through the clearing lane retires the
old route"* refuses a change that "adds a clearing operation for work an existing
direct route still performs" as leaving a dormant second door. The governed group
`xfactory-artifact-workers` today carries the grandfathered member
`council-deliberation-worker.yml`, whose `cpc_jobs` are `deliberate` and
`smoke-seat` with `allowlist_entry: present` — a live direct route performing
exactly this work.

**THE BASIS SCENARIO THAT COULD BE READ AGAINST THIS PACKET, NAMED RATHER THAN
LEFT FOR A RATIFIER TO FIND.** That requirement's second scenario reads: *"WHEN
a change adds a clearing operation for work an existing direct route still
performs THEN the change MUST be refused as leaving a dormant second door."* On
its face that sentence reaches this change. The packet's answer is that the test
is whether a SECOND DOOR EXISTS, and a register entry with no host job declared
anywhere is not a door: nothing can be dispatched through it, and the direct
route remains the only route. The act that opens the second door is the act that
declares the host job. **That reading is the authoring session's, it is not
ruled, and if Brett refuses it the remedy is plain: hold this admission until
the retiring xFactory change is ready to land beside it.** The requirement
itself states the answer and not the flag — a ratified sentence that reports its
own author's uncertainty is a sentence a later reader cannot rely on — so the
veto lives here, where every other unruled decision in this packet lives. The remedy is
available at any time and costs this packet nothing but its landing window,
which is why the reading is offered rather than argued for.

**And that member is in `opensoft/xFactory`, not here.** This packet cannot edit
xFactory's enumeration, its allowlist, or its clearing workflow. So the honest
reading, and the one the requirement encodes: **admitting the entry is not the
act the retirement requirement binds.** The act it binds is the change that
DECLARES THE HOST JOB — which is an xFactory change — and this packet carries the
obligation FORWARD to it, as a clause of the entry and as a scenario, so it is
checkable at the moment it can be violated. Admitting an entry with no host job
anywhere creates no second door; landing a host job beside a live grandfathered
one does.

Note also #165 design **D17**: the OPERATIVE deliberation lane is the xFactory
copy, not codexFactory's local one, and the codexFactory copy is what retires in
#165's own phase 6. This packet takes no position on that beyond naming which
enumeration member is the one this entry displaces.

## D11. RESOLVED (OQ2) — the `sequenced_after` live pin DOES move, by exactly one row

**Measured, not assumed, at `origin/main` `9ef151ad`.**

The pin the brief describes — five asserted totals in
`tests/sequenced_after/test_sweep.py` plus a MOVEMENT LOG — **is no longer the
live pin.** `add-per-change-sweep-ledger` (issue #618; realized by PR #623,
archived by PR #632, on `main` at `7ace2721`) replaced it: the live pin is
`tests/sequenced_after/corpus-ledger.yaml`, ONE ROW PER CHANGE ID over both
corpora, and every total the sweep reports is DERIVED from the rows and
cross-checked against the measurement. The openxFactory shared-substrate
register's row 2 still describes the old regime and is stale; that is recorded on
issue #630 as part of this packet's Rule 7 claim.

**Baseline** (`python3 scripts/validate-sequenced-after.py . --sweep`), at
`origin/main` **`9ef151ad`**: 163 change ids (34 active + 129 archived), 113
co-modified, 50 sole, active 22 / 12, 2 declarations, 0 root claims, 3 prose
headers (3 archived), deepest declared chain 2 hops. `--ledger-diff`:
*consistent with the corpus (163 rows)*. RE-TAKEN after merging `origin/main`
**`963c5b77`** (#640 and #638, two fix packets that add and archive no change
directory): **identical in every field**, which is why no re-derivation was
owed for that merge. RE-CHECKED A THIRD TIME at review round 1 against
`origin/main` **`73b1b3c1`** (#639, a merge whose only file is
`tests/doc-health/test_modified_block_currency_self_gate.py`): it adds and
archives no change directory, so the baseline is unmoved and no re-derivation
is owed for it either. Every reading here carries the sha it was taken at,
because a reading without one is the staleness the ledger exists to stop.

**What this packet moves: ONE ROW ADDED, no partner flipped.** The delta is
`## ADDED Requirements` only and carries ONE requirement title that no other
change in either corpus writes, so co-modification — which is measured at
REQUIREMENT granularity, not capability granularity — does not engage:
`add-clearing-dispatch-boundary` and `add-cpc-clearing-boundary` share this
capability but not this title, and both are already `co-modifier` from other
partners, so neither row moves.

**Post-state, MEASURED on this branch rather than predicted, and RE-MEASURED at
review round 1 with the identical result:** 164 change ids
(35 active + 129 archived), 113 co-modified, 51 sole, active **22 / 13**;
declarations, root claims, prose headers and the deepest chain all unchanged.
The whole movement is `sole_modifiers` 50 → 51 and `active_sole` 12 → 13, which
is the signature of one added SOLE row and nothing else — `co_modified` holding
flat is the check on that reading, since a partner flip would have moved it in
the opposite direction. (An earlier draft of this section PREDICTED
"active 23 / 12" and was wrong: it moved the co-modified half of the pair
instead of the sole half. The measurement is recorded here rather than the
prediction quietly corrected, because a pin whose author guessed and did not
re-measure is the staleness the ledger exists to stop.)

The new row sorts between `add-xfactory-installer-repository` and
`admit-install-repos-to-aggregation`; a concurrent lane inserting into that same
gap is the residual the ledger does not remove, and it is the landing window's
(Rule 6), not this packet's.

**THE ROW, AS SEEDED** — written by
`python3 scripts/validate-sequenced-after.py . --seed-ledger --moved-by '#645'`
rather than hand-edited, which reported *"164 rows, 1 moved by #645"* and named
exactly this change:

```yaml
  admit-deliberation-clearing-operation: {state: active, class: sole, declares: absent, prose: false, moved_by: "#645", moved_on: "2026-09-04"}
```

**NO MOVEMENT LOG ENTRY IS OWED.** The ledger's rule: an entry is owed only where
a move is NOT explained by the row diff itself. A row ADDED is the rule's
explicit no-entry case, and the diff here is one line.

## D12. What could go wrong, honestly

- **The register is now a set of two, and the second is the interesting one.**
  Entry one could be checked by reading it; entry two carries a bundle, a
  credential and a return. Every general rule in the basis has to actually hold
  for it, and this packet's scenarios assert only the ones specific to the entry
  — the rest are the basis's and are cited, not re-asserted here.
- **Five frozen copies (D9), plus three pinned numerals, is eight chances to
  move seven and miss one.** The mitigation is that each fails loudly and
  differently, and task 2.6 requires each to be seen red on a deliberately
  partial edit before the slice is called done. The count moved from two to four
  to five over this packet's authoring and its review round, which is the honest
  evidence that counting them by memory does not work.
- **The new neutral schema is a new surface with no consumer yet.** Nothing in
  this repository emits a deliberation return; the first real instance comes
  from a host job that does not exist. So its proof is the packaged corpus — one
  positive example and at least one negative fixture — and the schema must be
  minimal enough that the first real return does not immediately amend it.
- **The retirement (D10) is somebody else's commit.** The clause and the scenario
  make it checkable, but they do not make it happen; the estate's controls here
  are the authoring-time guard and the periodic attestation, both of which live
  in the clearing repository.

## D13. The refusal grounds and the return kind are NAMED IN RATIFIED TEXT, because both enumerations are closed

**Found in review round 1, and it is a ratification blocker cured in place
rather than a nicety.** The first draft's scenario said a return that fails its
declared schema "MUST be refused … and the ground MUST be a member of the closed
refusal enumeration, added by a governed change rather than recorded as free
text" — and then named no ground. That sentence, unnamed, instructs the
realizer to add a member to a closed enumeration on their own authority, which
is exactly the self-service widening the closed register exists to end, moved
one enumeration to the left.

**THE TWO ENUMERATIONS ARE DIFFERENT AND SO ARE THEIR SPELLINGS, WHICH IS HOW
A REALIZER GETS THIS WRONG.** Measured, not remembered:

| enumeration | where it lives | spelling | today |
|---|---|---|---|
| the RECORD'S REFUSAL GROUNDS | `contracts/clearing/dispatch-record.schema.yaml`, `$defs.refusal_ground.enum` | snake_case, unprefixed | TWO: `unregistered_operation`, `unknown_lane_selector` |
| the VALIDATOR'S FINDING CODES | `scripts/validate-clearing-dispatch.py`, `REFUSAL_CODES` | hyphenated, `clearing-` prefixed | TWENTY-SIX |

The ratified requirement that binds a refusal is about the FIRST of these: *"A
refusal SHALL be recorded with its ground named FROM A CLOSED, NAMED ENUMERATION
of refusal grounds"*, and `add-cpc-clearing-boundary`'s scenario adds *"a ground
absent from that enumeration MUST be added by a governed change rather than
recorded as free text"*. So the thing this packet owes is grounds, in the
record's spelling — not codes in the validator's.

**WHICH GROUNDS, AND THE TEST FOR IT.** The dispatch record's own description
sets the rule and lists the awaited members: *"The requirement text names nine
further grounds — expiry, hash mismatch, workflow-path contradiction, commit
mismatch, unreadable API, lane not permitted, output-schema failure,
origin-scoped credential, committed-data offer — and each becomes a member AS
THE OPERATION THAT CAN PRODUCE IT LANDS."* Three of those nine become emittable
at THIS entry's landing and no others do, so this change admits three and seeds
nothing else. **No concept is coined here — only the spelling, and it follows
the two seeded members' form.**

1. **`lane_not_permitted`.** Entry one declares BOTH lanes, so no sealed request
   can name a lane its operation does not permit; the refusal is unreachable
   today. Entry two declares ONE lane. It is the first entry that can produce
   the ground, and refusing a coding-lane request is its own scenario.
2. **`output_schema_failure`.** Entry two is the first entry to declare a return
   shape a host actually produces, and the scenario that refuses a
   non-validating return is its own.
3. **`origin_scoped_credential`.** Entry one's `token_scopes` is EMPTY — no
   credential of any kind reaches its job, so the condition is structurally
   impossible for it. Entry two is the first entry whose job carries a token at
   all, and refusing a producer-scoped credential in that job is its own
   scenario.

**WHAT IS DELIBERATELY NOT SEEDED, and why the restraint is the same rule.** The
other six awaited grounds stay absent. The schema's own warning is that
*"Seeding all eleven now would publish grounds no implementation can emit, which
is a closed enumeration in name only"*, and a packet that seeded them to be
helpful would be doing the widening it refuses in the register.

**NO VALIDATOR FINDING CODE IS MINTED EITHER, and that was measured too.** The
verdict refusal this entry's scenario names is `clearing-report-carries-a-verdict`,
already a member and already red-proven by
`examples/negative/operation-report-carrying-a-readiness-verdict.yaml`; the lane
refusal is `clearing-lane-not-permitted`, likewise already a member with its own
fixture. And a return that fails JSON Schema is NOT a member and must not become
one: the closed set's own comment says *"`schema` is the shape refusal and is
not a member: it is not this family's rule, it is JSON Schema's."* A realizer
inventing `clearing-return-schema-invalid` would be widening a closed set to
duplicate a refusal that already fires — so the requirement says so in as many
words.

**THE RETURN'S `kind`, for the same reason one enumeration to the left.**
`KIND_TO_SCHEMA` routes a record to the schema it is validated against, and
`check_operation_report` — which carries the `VERDICT_WORDS` scan — is dispatched
on `kind == "xfactory_clearing_operation_report"`. The scan therefore does not
reach a return of a new kind until the kind exists AND is routed. Leaving the
kind to realization would leave the realizer holding the choice of whether the
verdict scan reaches this operation at all, so the kind is ratified text:
**`xfactory_clearing_deliberation_return`**, in the family's existing
`xfactory_clearing_*` form.
