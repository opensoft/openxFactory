# Adversarial review round 1 — admit-deliberation-clearing-operation

Status: record
Filed: 2026-09-04
Filed by: adversarial review session, lane `hermes-wallet-exercise`
Reviewed head: `a47bdb6d0fea6f0fb1ea89a0fa092d5acfa9cca6` (PR #645)
Basis read: `add-clearing-dispatch-boundary` (unarchived, ratified 2026-09-01),
`add-cpc-clearing-boundary` (merged), promoted `doc-health`,
`release-realization`, `document-cataloging`, the realized `contracts/clearing/`
family, `scripts/validate-clearing-dispatch.py`, `tests/clearing/`,
`.github/workflows/clearing-dispatch-gate.yml`, `credential-contracts`,
`opensoft/xFactory`'s grandfather enumeration, and codexFactory PR #165 at
`b9714e21`.

**Nothing was refused.** Every finding is FIXED IN PLACE except the two that
only the operator can rule, which are stated as such. The packet still authors
NO contract byte: `git diff origin/main --stat` remains the packet directory,
`README.md`, and one `tests/sequenced_after/corpus-ledger.yaml` row.

## P1 — would have blocked ratification

### P1-1 — a closed enumeration was left for a realizer to widen

The scenario "The return does not validate against the declared neutral schema"
required the refusal ground to be "a member of the closed refusal enumeration,
added by a governed change rather than recorded as free text" — and named no
ground. Unnamed, that sentence instructs the realizer to add a member to a
closed enumeration on their own authority, which is the self-service widening
the closed register exists to end, moved one enumeration to the left.

The enumeration is `contracts/clearing/dispatch-record.schema.yaml`'s
`$defs.refusal_ground.enum` — **TWO members** today, snake_case and unprefixed
(`unregistered_operation`, `unknown_lane_selector`) — and NOT the validator's
hyphenated `clearing-…` `REFUSAL_CODES`. The two are different sets with
different spellings, which is how a realizer gets this wrong. The ratified sentence
that binds a refusal ("named FROM A CLOSED, NAMED ENUMERATION of refusal
grounds", with #560's "a ground absent from that enumeration MUST be added by a
governed change") is about the record's grounds.

**FIXED.** The requirement now admits **exactly three** grounds, in the record's
spelling, each one of the nine the record's own description says it awaits and
each made emittable by *this* entry's landing and no earlier one:
`lane_not_permitted` (entry one permits both lanes, so the refusal was
unreachable), `output_schema_failure` (entry one declares a report, not a
host-produced return), `origin_scoped_credential` (entry one's job carries no
token at all). The other six stay absent — seeding grounds no implementation
can emit is a closed enumeration in name only. New task 2.9 performs it and is
marked as the one task in the packet that widens a closed set. Reasoning:
design **D13**.

### P1-2 — the return's record kind was a realization choice, and it gates the verdict scan

`check_operation_report` — which carries the `VERDICT_WORDS` scan — is
dispatched on `kind == "xfactory_clearing_operation_report"`. The packet found
that (task 2.5) but left the new kind unnamed, so a realizer would have held the
choice of whether the verdict scan reaches this operation at all.

**FIXED.** The kind is ratified text: **`xfactory_clearing_deliberation_return`**,
in the family's existing `xfactory_clearing_*` form. The verdict scenario now
names the kind the scan must reach. Design D4/D13; tasks 2.2 and 2.5.

### P1-3 — no validator finding code may be minted, and the packet did not say so

Left as it stood, a realizer could reasonably have coined
`clearing-return-schema-invalid`. The closed finding-code set's own comment
refuses that: *"`schema` is the shape refusal and is not a member: it is not
this family's rule, it is JSON Schema's."*

**FIXED.** The requirement states that no finding code is minted, names the two
that already cover this entry's refusals (`clearing-lane-not-permitted`,
`clearing-report-carries-a-verdict`), and says a shape failure is reported as
the family's `schema` refusal. Task 2.5 carries the same, plus the assertion
`test_no_fixture_declares_a_code_outside_the_closed_set`.

## P2 — accuracy of ratified text

### P2-1 — `internal-governance` was attributed to the wrong family

The class name occurs **nowhere** in `document-cataloging`. That capability
types a document's handling as a free string
(`handling: {type: [string, "null"]}`), requires it to "remain mechanical
inventory fields and MUST NOT be semantically rewritten" — it COPIES the
source's word — and what it owns is the handling GATE that authorizes a host for
a class. The class name is a `Handling:` header value of the
`document-lifecycle` / doc-health header family, read by
`doc_health/inventory.py` and `doc_health/organizer_dispatch.py`, and it is the
handling authorization the doc-health worker dispatch requires by default
(`.github/workflows/doc-health-reusable.yml`, `worker-handling-class`).

**FIXED, without contradicting the shipped register.** The requirement now says
the `data_handling` FIELD borrows its vocabulary from `document-cataloging` as
the register's own schema and `composes_with` say, while the CLASS NAME is the
header value the estate's governance corpus already travels under. Design D7
carries the measurement. D7's `protected` sentence is also corrected: it is the
class the handling gate refuses to dispatch (`doc_health/cataloger.py`'s
protected-handling blocker), not a class `document-cataloging` "never
dispatches".

### P2-2 — the entry did not declare `lane_key`

The register's lane shape requires four members and none is optional. The
requirement named three.

**FIXED.** `lane_key` `artifact` is named in the requirement, the proposal's
fact table, and task 2.1.

### P2-3 — the basis scenario that reads against this packet was not named

`Routing a route through the clearing lane retires the old route` carries the
scenario *"WHEN a change adds a clearing operation for work an existing direct
route still performs THEN the change MUST be refused as leaving a dormant second
door."* On its face that reaches this change, and a ratifier finding it
unanswered would be right to stop.

**FIXED (the answer is now in the text), AND ESCALATED.** The requirement names
the scenario, states the test — whether a SECOND DOOR EXISTS, and a register
entry with no host job declared anywhere is not a route — and states the remedy
if the reading is refused: hold the admission until the retiring xFactory change
lands beside it. Design D10 flags the reading as the authoring session's and
vetoable. **This is one of the two items only Brett can rule.**

## P3 — completeness of the realization surface

### P3-1 — the member set is frozen in FIVE places, not four

The packet's own finding of a fourth copy was itself short by one.
`tests/clearing/test_clearing_gate_wiring.py::test_the_assertion_pins_the_registers_literal_member_count`
asserts `"1 registered operation" in assertion` — copy 4's literal, pinned from
a second file. Moving the workflow alone turns it red.

**FIXED** across design D9, tasks 2.3 and 2.6, the proposal's `code_surface`,
and the README block. D9 additionally records three pinned numerals the new
schema moves and the packet did not name:
`test_the_family_ships_five_schemas`' exact five-name list (→ six),
`test_the_family_registers_exactly_the_six_members` (→ seven), and
`test_the_row_digest_matches_the_artifact_on_disk` (the register instance's and
the dispatch record schema's manifest row digests both move with their bytes).

### P3-2 — `registry_version` was not scheduled to move

`test_the_registry_declares_its_own_identity` asserts only `>= 1`, so nothing
catches an unbumped version.

**FIXED.** Task 2.1 requires `registry_version` 1 → 2 and says why no test will
catch its absence.

### P3-3 — entry two would have shipped with no test of its own

`test_the_entry_declares_every_ratified_fact` and
`test_both_ratified_lanes_are_declared_with_literal_group_and_label` read entry
one. A malformed entry two would pass them in silence.

**FIXED.** Task 2.1 requires entry-two twins of both, the lane twin asserting
ONE lane.

### P3-4 — the re-pointed test kept a name that lies

`test_deliberation_is_refused_by_name` re-targeted to `coding` keeps a name that
says `deliberation` — the same defect as a fixture whose comment and bytes
disagree.

**FIXED.** Task 2.4 renames it `test_coding_is_refused_by_name`, and adds an
inspect-expecting-no-change item for
`examples/negative/dispatch-record-with-a-free-text-refusal-ground.yaml`, which
claims `deliberation` but is red for its free-text ground and survives
admission.

### P3-5 — the manifest's own bookkeeping was unscheduled

**FIXED** as new task 2.10: the clearing-family header comment's corpus counts
(and its already-stale negative count — the validator self-test reports 26 where
the comment says 24), the moved row digests, and the README corpus counts, with
`tests/clearing/test_clearing_manifest_rows.py` green in full as the assertion.

### P3-6 — the retirement makes four packaged attestation artifacts stale

`attestation-claiming-full-completeness-before-admission.yaml`,
`attestation-filing-a-dark-lane-as-a-widening.yaml`,
`attestation-with-one-estate-wide-expected-set.yaml` and the positive
`single-door-attestation.example.yaml` all carry
`council-deliberation-worker.yml` as a LIVE allowlisted member of
`xfactory-artifact-workers`. They are correct until the retirement and stale the
moment it lands.

**FIXED** as new task 4.2a — named so the staleness is scheduled rather than
discovered, with the follow-up owed by the retiring change.

## P4 — currency

- **P4-1 `.openspec.yaml` duplicate check.** Re-run a third time at
  `origin/main` `73b1b3c1`: 35 active change directories (the 34 recorded plus
  this one), NINE open pull requests (#640/#639/#638 merged in the interval,
  none touching `contracts/clearing/`), no `delib*`/`*permitted*` remote head,
  and the only merge since `963c5b77` is a single doc-health test file. Result
  unchanged. **RECORDED** in the origin reason.
- **P4-2 sequenced_after.** Re-measured, not re-read:
  `validate-sequenced-after.py . --sweep` on this branch returns **164 change
  ids (35 active + 129 archived), 113 co-modified, 51 sole, active 22 / 13**, 2
  declarations, 0 root claims, 3 prose headers, deepest chain 2 hops, and
  `--ledger-diff` reports *consistent with the corpus (164 rows)*. D11's figures
  are correct in every field. **FIXED:** D11 now carries the third reading at
  `73b1b3c1`.

## Verification at the fixed head

- `openspec validate admit-deliberation-clearing-operation --strict` — valid.
- `openspec validate --all --strict` — 90 passed, 0 failed.
- `python3 -m pytest tests/clearing tests/sequenced_after -q` — 334 passed.
- `python3 scripts/validate-clearing-dispatch.py .` — 0 errors, 0 warnings;
  *26/26 closed refusal codes red-proven*; *6 packaged record(s) validated, 26
  negative fixture(s) refused*.
- `scripts/doc-health.py --single-repo .` — **no finding names any path of this
  packet.** The four `record-immutability` criticals on `docs/*.md` were
  reproduced on a clean `origin/main` worktree and are PRE-EXISTING, not this
  packet's. Recorded because the family is FLAKY: an earlier run in this same
  session reported "No findings" for it, so a green reading of that family is
  not evidence.
- `.openspec.yaml` `code_surface:` / `target_release:` conform to
  `release-realization`, and `target_release:` reserves no minor, per
  `docs/contract-versioning-policy.md`.

## Checks that PASSED as authored, verified rather than assumed

- **The govern-sibling marker reading HELD.** The promoted requirement is
  *"A MODIFIED block over an active sibling's addition is evaluated for its
  pairing, not for its carriage"* and it scopes itself to "every `## MODIFIED
  Requirements` block". This packet's block is `## ADDED`. Confirmed
  EMPIRICALLY as well as textually: the `modified-block-currency` family emits
  nothing against this packet's delta, while emitting eleven findings against
  other active changes' MODIFIED blocks in the same run. The collision class
  reaches an ADDED block only where a second active change adds the same
  requirement title; no other change writes this title.
- **`actions:read` is the right spelling and is sufficient.** It is a member of
  `scripts/validate-credential-contracts.py`'s `DISPATCH_SCOPES`, so the entry
  borrows rather than mints; it satisfies the register schema's `identifier`
  pattern; and it is exactly what #165 tasks 7.3 fixes for the return-fetch job
  ("`actions: read` on the CLEARING repository's own run artifacts and nothing
  else"), which is the only read the host performs. `metadata:read`'s omission
  is correctly reasoned — on this provider it is a floor rather than a grant,
  and a register entry listing floors beside grants stops being a bound.
- **Every declared fact FITS the shipped schema.** `actions:read`,
  `council-deliberation-worker` and `internal-governance` all satisfy the
  `identifier` pattern `^[A-Za-z0-9][A-Za-z0-9._:/-]*$`; `data_handling` is an
  identifier, not a free string; `timeout_minutes` is bounded 1–1440; the lane
  shape is complete once `lane_key` is named (P2-2).
- **D9's claim of a literal gate grep is TRUE.**
  `.github/workflows/clearing-dispatch-gate.yml:113` greps
  `\(1 registered operation\)`.
- **The grandfather row is named correctly.** `opensoft/xFactory`'s
  `.github/clearing/grandfather-enumeration.yaml` carries
  `council-deliberation-worker.yml` on `xfactory-artifact-workers` with
  `cpc_jobs: [deliberate, smoke-seat]` and `allowlist_entry: present` — exactly
  what tasks 4.3 names. (#165's `smoke` is the codexFactory copy's job name; the
  xFactory copy's is `smoke-seat`, and the packet uses the right one.)
- **No collision with codexFactory #165.** #165 coins no worker-profile name, no
  data-handling class, no scope spelling and no output-record schema name; it
  names the return MEMBERS `seat_results.json` and `return-manifest.json`, which
  D4 already cites. Nothing in this packet re-coins anything #165 owns.
- **D10 agrees with #165 D17 and fills a gap in its Phase 7.** D17 rules the
  xFactory copy operative and scopes its RESHAPING to Phase 7; Phase 7.5 says
  the allowlist does not grow and the enumeration is shrink-only, but no Phase 7
  task actually strikes `council-deliberation-worker.yml`. This entry's
  forward clause is what binds it.
- **The honest limit is carried, not strengthened.** "A tripwire backed by
  review, not an unforgeable refusal" survives verbatim in substance in the
  requirement's third scenario and in D9.
- **No contract byte moves.** Verified against the merge base as well as
  `origin/main`.

## LEFT FOR BRETT — only the operator can rule these

1. **The route-retirement reading (P2-3, design D10).** Is admitting a register
   entry, with no host job declared anywhere, "adding a clearing operation for
   work an existing direct route still performs"? The packet says no, on the
   ground that no second door exists until a host job exists, and carries the
   retirement obligation forward onto the xFactory change that declares one. If
   you read it the other way, the remedy is to hold this admission until the
   retiring xFactory change is ready to land beside it — it costs the packet
   nothing but its landing window.
2. **The three refusal grounds (P1-1, design D13).** The spellings
   `lane_not_permitted`, `output_schema_failure` and `origin_scoped_credential`
   are the review session's, chosen to match the two seeded members' form; the
   CONCEPTS are the record schema's own awaited nine. Admitting three at once is
   also a judgement — the alternative is to admit only `lane_not_permitted` and
   `output_schema_failure` now (the two the packet's own scenarios force) and
   leave `origin_scoped_credential` to the change that declares the host job.
   Either is defensible; the packet takes the first because scenario six's
   refusal is otherwise unrecordable.

Beyond these two, the entry's substantive choices remain flagged for veto where
the packet already flagged them: D2, D3, D5, D6, D7, D8.
