# Adversarial review round 2 — admit-deliberation-clearing-operation

Status: record
Filed: 2026-09-04
Filed by: adversarial review session, lane `hermes-wallet-exercise`
Reviewed head at entry: `47f3e2f52ddda13b068ef723485af5ddab40a173` (PR #645)
Catch-up merge: `ef65be6c`, merging `origin/main` `342bee51`
Round 1's record: `review/adversarial-round-1-2026-09-04.md`

**Round 2's subject is what round 1 ADDED.** Round 1 cured three ratification
blockers by writing new ratified text — three refusal grounds, a record kind, a
no-code-is-minted sentence — and new ratified text is exactly what a second pair
of eyes owes attention. **Nothing was refused.** Every finding is fixed in place
except the two the operator must rule, which are unchanged in substance and are
now PUT as questions rather than only flagged. The packet still authors NO
contract byte: `git diff origin/main --stat` is the packet directory, the
README's records block, and one `tests/sequenced_after/corpus-ledger.yaml` row.

## Part A — the catch-up merge

`mergeStateStatus` was **DIRTY**. `origin/main` had advanced by ONE commit,
`342bee51` (#644), which archives `add-drafted-proposal-origin`. **It touches
none of the five surfaces that would force a fact re-check** — `contracts/clearing/`,
`scripts/validate-clearing-dispatch.py`, `tests/clearing/`,
`.github/workflows/clearing-dispatch-gate.yml`,
`openspec/changes/add-clearing-dispatch-boundary/` — so no frozen-copy count, no
pinned numeral, no register member-count literal and no refusal enumeration moved
under the packet. Each was nevertheless re-measured on the merged tree (below)
rather than carried over.

- **`README.md` — CONFLICT, resolved by keeping both sides' intent.** Main
  REMOVED `add-drafted-proposal-origin`'s active entry (and added its archived
  entry further down, which auto-merged); this branch had added its own entry
  above it. Resolution: this packet's active entry stays at the top of the block
  in the block's newest-first convention, main's removal is taken, main's
  archived entry stands.
- **`tests/sequenced_after/corpus-ledger.yaml` — auto-merged cleanly**, both rows
  present: main's `add-drafted-proposal-origin` flipped `active` → `archived`
  `moved_by: "#644"`, this branch's `admit-deliberation-clearing-operation` row
  untouched.
- **The "246-line phantom revert" round 1 saw before ITS merge did not survive
  this one.** After the merge `git diff origin/main` is PURELY ADDITIVE — the
  packet directory, the README block, one ledger row, 1556 insertions and ZERO
  deletions — and `git diff origin/main` over main's newer
  `openspec/specs/doc-health/spec.md`,
  `openspec/specs/document-lifecycle/spec.md` and
  `tests/doc-health/test_modified_block_currency_self_gate.py` is EMPTY. The
  merged tree carries main's newer bytes.

**THE LEDGER RE-MEASUREMENT, and the baseline genuinely moved this time.**
`342bee51` is the first main commit since this branch was cut that moves a change
DIRECTORY, so `--sweep`'s split figures move with it and its totals do not.
Measured on an extracted `origin/main` tree, not inferred: baseline **163 change
ids (33 active + 130 archived), 113 co-modified, 50 sole, active 21 / 12**,
`--ledger-diff` *consistent with the corpus (163 rows)*. On the merged branch:
**164 (34 active + 130 archived), 113, 51, active 21 / 13**, *consistent with the
corpus (164 rows)*. **This packet's own signature is unchanged** — `sole`
50 → 51, `active_sole` 12 → 13, `co_modified` flat — which is why the correction
is a correction of the BASELINE and not of the packet's claim. Round 1's reading
("35 active + 129 archived, active 22 / 13") was right at its baseline `73b1b3c1`
and is superseded, not contradicted. **FIXED:** design D11 carries the fourth
reading, both halves, each with the sha it was taken at.

## P1 — findings against round 1's own additions

### P1-1 — the three spellings' provenance was understated, and it is the whole defence of the act

Round 1 recorded the spellings as "the review session's" and left it in LEFT FOR
BRETT as a judgement. **Measured byte-for-byte, that undersells what happened and
leaves the weaker argument in the packet.** The record's awaited nine are named
IN PROSE and in no identifier anywhere: the phrases *"lane not permitted"*,
*"output-schema failure"* and *"origin-scoped credential"* appear VERBATIM in the
shipped `contracts/clearing/dispatch-record.schema.yaml` description (line 65)
and, in the same words, in the ratified basis's own `tasks.md` 6.4 and 6.6. The
schema's `enum` holds two members and neither is one of the nine, so there was
never an identifier to copy — only a name to render.

**FIXED.** The requirement and design D13 now state that the three ENGLISH NAMES
are the record's own, verbatim; that the three IDENTIFIERS are this change's; and
that the rendering follows THE ONE RULE the two seeded members already follow
(`unregistered_operation` ← "unregistered operation", `unknown_lane_selector` ←
"unknown lane selector") — lower case, words joined by underscores, no
`clearing-` prefix, a compound's hyphen becoming an underscore. The rule is
written down so the remaining six render the same way and so the enumeration
moves at realization BY THIS TEXT rather than by a realizer's ear (task 2.9 now
requires the rule to be carried into the schema's own description). The sentence
that applying the rule is not authorization to seed the six is in the ratified
text.

**Ground-to-scenario mapping, checked:** `lane_not_permitted` → scenario 2 only;
`output_schema_failure` → scenario 5 only; `origin_scoped_credential` → scenario
6 only. One each, no ground without a scenario and no scenario reaching for a
ground it does not name.

### P1-2 — the `origin_scoped_credential` collision hypothesis: CHECKED, and it does not hold

The challenge was that `origin_*` in this estate reads as #560's origin-IDENTITY
family (`origin_signature`, `clearing-origin-signature-missing`,
`clearing-origin-row-expired`, the factory ORIGIN SIGNING KEY), so
`origin_scoped_credential` could be read as "the origin key's credential" rather
than "a credential scoped to the ORIGINATING REPOSITORY".

**It does not hold, measured inside the file the member lands in.** That schema's
own provider-verified field list is `origin_repository`, `origin_workflow_path`,
`source_commit`, `dispatching_identity`, `sealed_object_run` — `origin` in this
shape ALREADY means the originating repository — and `origin_signature` reads the
same way, as *the originating repository's* signature. The two uses share a
referent; they do not collide over one. The proposed alternative
`originating_repository_credential` was considered and **REFUSED**: it departs
from the record's own awaited-list name, which is the entire basis of the
rendering rule, and it would be the only member not derived from that list —
the ear-over-text drift the rule exists to stop. **FIXED anyway, in the direction
the challenge earns:** the requirement now fixes the reading in a sentence, so
the question is answered where a later reader meets it.

### P1-3 — scenario six folds a seat key into a credential ground, and nothing said so

Scenario six's WHEN covers a seat key, ANY other signing key, AND any credential
scoped to the originating repository; its THEN names ONE ground. A seat key is
not, in ordinary speech, a credential. Left unsaid, a ratifier finds a conflation
and cannot tell it from an oversight.

**FIXED, as a stated choice.** The ground covers the whole class of MATERIAL
SCOPED TO THE ORIGINATING REPOSITORY THAT MUST NEVER BE ON THE HOST, a seat key
included. The alternative — a fourth member such as `signing_key_on_host` — is
refused in the record: the awaited nine names no such ground, and minting one
would be coining a CONCEPT where every other member is the rendering of a name
the record already carries. A later change that needs them apart splits them on
the same governed terms.

### P1-4 — "no validator finding code is minted" was true and INCOMPLETE, and the gap is a realization decision nobody should hold

Round 1's sentence was verified true — `REFUSAL_CODES`' own comment says
*"`schema` is the shape refusal and is not a member: it is not this family's
rule, it is JSON Schema's"* — but it ran FOUR mechanisms together, and a realizer
holding all four at once is how a code gets minted by accident. Two measured
facts the packet did not state:

1. **A shape failure does not surface at all until the kind is ROUTED.**
   `validate-clearing-dispatch.py:879` is `KIND_TO_SCHEMA.get(kind)` followed by
   `if schema_name is None: return`. An unrouted kind is not validated LOOSELY,
   it is not validated. The packet's claim that a shape failure appears as
   `schema` is FALSE until task 2.5's routing row exists.
2. **The record GROUND `output_schema_failure` is not the validator's to write.**
   The basis says so in as many words (`tasks.md` 6.6): *"OUTPUT FAILING ITS
   DECLARED SCHEMA belongs to the hosted finalizer, which this slice deliberately
   does not ship."* The neutral validator never writes a dispatch record at all.
   The same item puts `origin_scoped_credential` and the committed-data offer
   outside every packaged shape — *"properties of a dispatch attempt rather than
   of a record"* — so no fixture is owed for it and none can exist.

**FIXED, and it is NOT "the realization decides".** The requirement now carries a
four-way statement of which component emits which, and design D13 carries the
same as a measured table: `schema` from the canonical validator, once routed;
`output_schema_failure` from the clearing workflow's hosted finalizer;
`origin_scoped_credential` from the clearing workflow at dispatch, owing no
fixture; and `clearing-record-refusal-ground-unknown` unchanged, since
`_refusal_grounds(schema)` reads the enumeration OUT OF THE SCHEMA at run time —
so admitting three members needs no validator code and grants no new refusal.
**Assigning an existing refusal to an existing component is not a widening**, and
the requirement says that too. The `26/26 red-proven` rule is untouched: it binds
`REFUSAL_CODES`, not this enumeration's members, whose proof is that a packaged
record naming them validates clean.

## P2 — accuracy of ratified text

### P2-1 — the requirement carried a count its OWN realization falsifies

*"That enumeration holds TWO members today"* is a standing statement in text
destined for canon, and task 2.9 takes the enumeration to five. Promoted, it
would read false, and it would read false because of this very packet.

**FIXED.** *"That enumeration HELD TWO MEMBERS AT THIS CHANGE'S AUTHORING … so
this change ADMITS EXACTLY THREE FURTHER GROUNDS — carrying the enumeration to
FIVE"*, with the reason written in: a reading taken at a moment is not a standing
fact, and a ratified sentence its own realization falsifies is one a later reader
cannot rely on. The same treatment is applied to the retirement clause's *"today
carries the grandfathered member"* → *"carries, AT THIS CHANGE'S RATIFICATION"*,
whose falsification is the POINT of the clause.

### P2-2 — design D1's NOT-RULED list had gone stale against `.openspec.yaml`

`.openspec.yaml`'s `approved_by` flags D13 for veto; design D1's own NOT-RULED
line still read "D2, D3, D5, D6, D7, D8, D9, D10, D11". Two governance records
of the same packet disagreeing about what is ruled is the kind of small
divergence a ratifier is entitled to stop on.

**FIXED.** D1 names D13, and points at the two `THE QUESTION, PUT FOR RULING`
headings.

## P3 — the two operator questions, made rulable (positions UNCHANGED)

### P3-1 — D10, the route-retirement reading

**FIXED as a rulable paragraph**, not as a change of position. `THE QUESTION, PUT
FOR RULING` states Reading A (the packet's: no second door exists until a host
job exists; the obligation binds forward) with its cost — an interval in which
the estate holds a ratified entry with no route, enforced by a scenario in a
repository that cannot execute it — and Reading B (hold the admission until the
retiring xFactory change lands beside it) with its cost. **Round 2 adds the fact
that makes B answerable:** #165 design D13 says leg 3 "has no legal home" until
this entry exists, so the xFactory change that declares the host job cannot
lawfully be authored ahead of the admission it depends on. **Reading B is
therefore coherent only as ONE ACT across two repositories in one reviewed
window** — a real option, and a refusal of A should be read as choosing it rather
than as an accident of refusing.

### P3-2 — D13, three grounds or two

**FIXED as a rulable paragraph.** Reading A (the packet's, three) with its cost:
two of the three are emitted by a component that does not exist yet, so the
enumeration briefly carries members nothing can emit — the schema's own "closed in
name only" defect, admitted at three-ninths scale. Reading B (two, deferring
`origin_scoped_credential`) with its cost: scenario six then ratifies a refusal
whose ground is unnamed until a later change, a milder form of the P1-1 defect
round 1 caught. **The execution of a ruling for B is named so it costs nothing to
choose:** strike one bullet from the requirement, one member from task 2.9, one
row from the proposal's fact table; nothing else moves.

## P4 — currency

- **P4-1 `.openspec.yaml` duplicate check — RE-RUN A FOURTH TIME at `342bee51`
  and RECORDED IN THE ORIGIN REASON.** Round 1's record says its third re-check
  was "RECORDED in the origin reason"; **it was not** — it lives in design D11
  and in round 1's own record. The origin reason now carries both, and the round-2
  run in full, because this is the run under which the surface counts MOVED.
  (1) 34 active changes — 33 main's plus this packet, main's #644 having archived
  one. (2) NINE other open pull requests (#648, #647, #646, #643, #641, #594,
  #548, #518, #176), with #644/#642/#640/#639/#638 merged and #646/#647/#648
  opened in the interval; **every one of the nine was checked FILE BY FILE**
  (`gh pr view --json files`) against the five clearing surfaces and NONE touches
  any of them. (3) No `delib*` or `*permitted*` remote head; the only other
  `admit-` head is the unrelated `change/admit-install-repos`. (4) The five merges
  above, none touching a clearing artifact. **Result unchanged: no sibling, no
  successor, no duplicate.**
- **P4-2 — the PR body was STALE in five places and is rewritten.** It said the
  member set is frozen in **FOUR** places (round 1 found the fifth); it carried
  none of round 1's ratified text (the three grounds, the kind
  `xfactory_clearing_deliberation_return`); its OQ2 figures were the pre-merge
  baseline (163/164, 35 + 129, active 22 / 13); its duplicate check was the
  `963c5b77` run; and its verification block said `90 passed` where the corpus is
  now 89 items. Rewritten at this head, first line `Lane: hermes-wallet-exercise`.
- **P4-3 — every numeral round 1's tasks name, re-verified against the MERGED
  tree, not carried over.** `test_the_family_ships_five_schemas` pins an exact
  five-name list (→ six); `test_the_family_registers_exactly_the_six_members`'
  `EXPECTED_ROWS` holds six (→ seven); `contracts/manifest.yaml`'s clearing header
  says *"6 positive examples + 24 intended-invalid"* while the corpus on disk is
  **6 positives and 26 negatives** and the validator's self-test reports *"6
  packaged record(s) validated, 26 negative fixture(s) refused"* — so task 2.10's
  "already stale on main, correct it to the measured count" is CONFIRMED, not
  inherited; `test_the_registry_declares_its_own_identity` asserts only
  `registry_version >= 1`, so task 2.1's bump is genuinely uncaught by any test;
  `test_the_assertion_pins_the_registers_literal_member_count` asserts
  `"1 registered operation"`, the fifth copy, and the gate's own grep at
  `clearing-dispatch-gate.yml:113` is the fourth. **All fifteen test names the
  packet's tasks cite exist at the paths cited.** Task 2.9's arithmetic (two
  members → five; nine awaited → six) is right.

## P5 — one addition to the realization surface

**Task 2.2's negative fixture had a trap in it.** The task asks for "AT LEAST ONE
negative fixture" for a new schema whose only refusal is a shape failure — and a
realizer who reads that a shape failure is reported as `schema`, then finds that
every packaged negative fixture must declare an `# expected_failure:` code, is
one step from minting `clearing-return-schema-invalid` to give the fixture
something to declare. **FIXED**: the task now records that
`test_no_fixture_declares_a_code_outside_the_closed_set` **excepts `schema` by
name** from the closed-set membership check (`code != "schema"`), so a
`schema`-declaring fixture is lawful and adds nothing to the probed set, leaving
`26/26` arithmetically untouched — measured, not assumed.

## Checks that PASSED as authored, verified rather than assumed

- **No requirement-title collision.** `register entry number two` occurs in this
  packet only. Two other active changes write `clearing-dispatch-boundary`
  deltas (`add-clearing-dispatch-boundary`, `add-cpc-clearing-boundary`) and
  neither writes this title, so the govern-sibling ADDED-block reading round 1
  established still holds, and `modified-block-currency` emits **10 findings on
  the branch and 10 on `origin/main`** — identical, none naming this packet.
- **`registry_version`, the five copies, the three pinned numerals, the lane
  shape, `actions:read`, the grandfather row** — all re-measured on the merged
  tree, all as round 1 recorded them.
- **The honest limit is carried, not softened.** *"a tripwire backed by review,
  not an unforgeable refusal"* survives in the requirement's third scenario and
  in D9, untouched by this round.
- **`Seven scenarios`** is still seven, and the seven are the seven the proposal
  lists.
- **No contract byte moves.** `git diff origin/main --stat` after the merge and
  after this round's edits: the packet directory, `README.md`, one ledger row.

## Verification at the round-2 head

- `openspec validate admit-deliberation-clearing-operation --strict` — valid.
- `openspec validate --all --strict` — **89 passed, 0 failed** (90 at round 1;
  main archived one change).
- `python3 -m pytest tests/clearing tests/sequenced_after -q` — **334 passed**.
- `python3 scripts/validate-clearing-dispatch.py .` — 0 errors, 0 warnings;
  *26/26 closed refusal codes red-proven*; *6 packaged record(s) validated, 26
  negative fixture(s) refused*; register still reads *1 registered operation*.
- `python3 scripts/proposal-support.py . verify` — ok.
- `python3 scripts/validate-sequenced-after.py . --ledger-diff` — *consistent with
  the corpus (164 rows)*.
- `scripts/doc-health.py --single-repo .` — **no finding names any path of this
  packet** (0 of 53). RUN TWICE per round 1's flakiness warning, byte-identical
  both times: 6 critical / 4 error / 27 warning / 16 info. The four
  `record-immutability` criticals are on `docs/*.md`, which this packet does not
  touch, and round 1 reproduced them on a clean `origin/main` worktree. A
  same-run comparison against an extracted `origin/main` tree matches family for
  family where the family can run there (`staged-topic-template` 25/25,
  `modified-block-currency` 10/10, `tag-hygiene` 4/4, `ratified-provenance` 2/2);
  `record-immutability`, `release-inventory-drift`, `release-tag-publication` and
  `staged-candidate-aging` cannot run on an extracted tree because version control
  cannot be consulted, and that limitation is recorded here rather than reported
  as a clean comparison.

## LEFT FOR BRETT — still exactly two, and still the two round 1 named

1. **D10 — the route-retirement reading.** Reading A (the packet's) or Reading B
   (hold the admission), with the costs of each stated in design D10 under
   `THE QUESTION, PUT FOR RULING`, and with round 2's addition that B is coherent
   only as one act across two repositories.
2. **D13 — three refusal grounds now, or two.** Both readings, both costs, and
   the exact edit a ruling for B requires, in design D13 under the same heading.

Round 2 found no third. Beyond these two, the entry's substantive choices remain
flagged for veto where the packet already flags them: D2, D3, D5, D6, D7, D8, D9.
