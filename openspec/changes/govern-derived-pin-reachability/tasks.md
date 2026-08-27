# Tasks: govern-derived-pin-reachability

**REALIZED 2026-08-27.** § 2 is implemented — `scripts/doc_health/pin_class.py`
(the declared class, Q1's ruled home), the reachability probe and the
reproduction check on the readiness surface in
`scripts/doc_health/ideation_readiness.py`, and 46 regressions at
`tests/doc-health/test_pin_reachability.py`. § 2.5's non-tool half and § 2.8's
landing obligation stay deliberately prose-only, and both say so in their own
words rather than being quietly ticked. § 3 grew from two orphans to FOUR: three
retained, one unrecoverable. § 4's gate is green except § 4.3, which is the merge
itself. § 5 carries five follow-ups, three of them raised by this realization.

**THE HEADER THIS FILE OPENED WITH, KEPT BECAUSE IT WAS TRUE WHEN WRITTEN.** As
authored: "**NO IMPLEMENTATION SURFACE is discharged here. This packet is a
PROPOSAL**: it carries the delta, the measurement, the inventory and the plan,
and it changes no code. § 1 records what the filing itself discharged, and § 1.5
is now discharged too. § 2 is the implementation plan, still entirely open, with
Q1's ruling folded into § 2.1 and § 2.2. § 4 is the archive gate. § 5 records two
adjacent gaps that are deliberately not this change." Every sentence of that is
now historical, and ONE OF THEM WAS WRONG EVEN THEN: the inventory it points at
reports 9 pins where measurement finds 63 sites. § 2's preamble carries the
correction and the four generator families the sweep missed.

**AND ONE THING THIS HEADER SAID IS NO LONGER TRUE, so it is corrected rather
than left standing.** As authored it read "and repairs no pin", and "§ 3 is the
live-orphan resolution, open and TIME-BOUND". **§ 3 IS DISCHARGED.** Brett ruled
Q2 on 2026-08-27 — publish the retention refs first, independently — and the
orchestrating session executed it the same day. Verified in this worktree rather
than taken on report: `git ls-remote origin 'refs/retention/*'` returns exactly
`refs/retention/pins/da9bf3b7d0ee1d86d2d437d42a715c238dddce4b` and
`refs/retention/pins/f13a3b6007736292e1e157febef1ac733e534de9`, each at the
commit its name states. The repair happened OUTSIDE this packet, which is
exactly what the recommendation asked for, and the packet still repairs no pin
because retention is not a pin edit — both records carry their original pins
UNEDITED and are now conforming. The garbage-collection window is CLOSED.

## 1. Filing and admission

- [x] 1.1 ORIGIN AND ADMISSION RECORDED. `.openspec.yaml` carries `kind: ad_hoc`
      with an `id`, a `reason`, and the approval pair filled from Brett's
      in-session commission of 2026-08-27, verbatim: "file the pin-governance
      follow-up change". The pair is filled rather than left blank because an
      instruction EXISTS here — this follows `fix-release-reachability-race`
      (whose `.openspec.yaml` records "in-session commissioning of the filing
      itself" as the approval act) and `add-family-enumeration-check`, and NOT
      the blank-pair shape `harden-ideation-readiness-check` was raised under,
      which had no instruction behind it. The distinction was judged, not
      assumed. THE APPROVAL SCOPE IS THE DECISION TO FILE: the five decisions in
      `proposal.md` § Orchestrator decisions and the three questions in § Open
      Questions are NOT covered by it and are flagged there.
- [x] 1.2 THE TWO DEFERRING RECORDS READ IN THE ARCHIVE AND CITED EXACTLY, with
      one correction to the commission's own description of them.
      `harden-ideation-readiness-check` defers the rule by name twice
      (`proposal.md` § Named follow-ups first bullet; `tasks.md` § 5.2, unticked
      at archive) and its OD-1 records the index-side requirement as CONSIDERED
      AND DECLINED "to avoid pre-empting the deferred governance packet".
      `fix-release-reachability-race` does NOT defer the rule by name: its
      § Named follow-ups carries three bullets and none is about pins. What it
      carries is § Family relation, whose table names the orphaned index pin as
      the family's stale operand. Established by absence-search over all four of
      its files: `defect in its own right`, `lands rebased`, `rebas`, `squash`,
      `orphan`, `unreachable from main` — no match. Recorded in `proposal.md`
      § The record that defers this rule, cited exactly.
- [x] 1.3 THE INVENTORY SWEPT AND EVERY PIN RESOLVED, not sampled. Nine pins
      across eight committed artifacts in scope, four generators, two of them
      ORPHANED; four schema-declared future members with no committed real pin
      yet; the cross-repository pin families named out of scope. Full table in
      `proposal.md` § The pin-carrying artifact inventory.
- [x] 1.4 COLLISION CHECK RUN BEFORE CHOOSING THE HOMES. No active change
      carries a delta for `ideation-cross-reference` or `release-realization` at
      all. Two active changes carry `doc-health` deltas —
      `add-family-enumeration-check` (`MODIFIED` on "Deterministic check
      families" plus one ADDED) and `add-nightly-dashboard-refresh` (seven
      ADDED) — and neither touches any requirement this packet adds. Every delta
      here is ADDED, so no archive order matters. `document-lifecycle` was
      considered as a cross-cutting home and declined partly because
      `add-ideation-intent-plane` carries a delta for it.
- [x] 1.5 THE FIVE FLAGGED DECISIONS CLEARED AND THE THREE OPEN QUESTIONS
      RULED, 2026-08-27. A four-question multi-choice was put to Brett by the
      orchestrating session and relayed the same day. **All five § Orchestrator
      decisions CLEARED AS AUTHORED, none vetoed** — OD-1 the three-capability
      all-ADDED shape, OD-2 the no-new-check-family enforcement home, OD-3
      re-pinning defined by reproduction, OD-4 record repair by retention, OD-5
      the change name. **All three questions RULED, each taking the packet's own
      recommendation**: Q1 the registry module beside
      `scripts/doc_health/families.py`; Q2 publish the retention refs first and
      independently, WHICH WAS THEN EXECUTED; Q3 formalize the namespace, and it
      is the one Q2's execution used, `refs/retention/pins/<full-sha>`. No
      verbatim wording of the ruling reached this session, so none is quoted —
      approver, date, mechanism and selected option are stated instead, the shape
      both sibling packets used. THE TWO ACTS ARE DISTINCT: the clearance closed
      the veto window and moved nothing, while the Q2 and Q3 rulings CHANGED the
      packet — Q3 edited two requirements and three scenarios and added the ref
      set to a third, Q2 discharged § 3 and § 4.5. Recorded in full at
      `proposal.md` § Orchestrator decisions and § Open Questions.
      `.openspec.yaml`'s origin block is deliberately NOT edited: a veto
      clearance is not origin provenance, and
      `release-realization`'s origin-retention rule makes rewriting a complete
      declaration a contested-class act. Verified unchanged at § 4.6.

## 2. Implementation (REALIZED 2026-08-27; § 2.8 stays deliberately prose-only)

**THE INVENTORY IN `proposal.md` § The pin-carrying artifact inventory IS
INCOMPLETE, AND THE REALIZATION MEASURED THE DIFFERENCE RATHER THAN INHERITING
IT.** That table reports 9 pins / 8 artifacts / 4 generators in scope, swept by
`git grep` over a list of key names. Re-measured at `origin/main` over committed
structured state — every standalone 40-hex token in every committed
`.yaml`/`.yml`/`.json`, resolved against the object database rather than matched
by key name — the repo-local class is **63 declared pin sites across 20 class
members**, of which 49 resolve, 13 are cross-repository and 1 is an
unrecoverable loss. Four generator families the packet never saw:

| family | sites | why the packet's sweep missed it |
| --- | --- | --- |
| proposal-support transition manifests (`openspec/changes/**/supporting-docs*manifest.yaml`) | 31 files | the largest member of the class, and swept by the same key (`source_revision`) the packet did search — it simply was not read out of the results |
| cross-factory ideation routing records (`ideation/brainstorm/**/routing.yaml`) | 11 | the key is `revision`, which the packet listed but whose hits it did not resolve |
| the avatar-client kernel, its lab register, and the F0 evidence | 7 | keys `f0_source_commit`, `openxfactory_commit`, `spec_delta_last_touched_commit`, `source_commit` |
| the hermes-runtime handoff/verification evidence and the neutrality-drift baseline | 11 | keys `commit`, `consumer_commit`, `expected_contract_ref`, `us3_baseline_commit` |

**AND IT FOUND TWO MORE ORPHANS THE PACKET DID NOT KNOW ABOUT.** The measured
table above is the argument for the declared class existing: a hand-swept
inventory is exactly the artifact that drifts. Both are recorded at § 3.5 and
§ 3.6.

- [x] 2.1 Q1 SETTLED FIRST, exactly as this task asked. **RULED 2026-08-27: a
      registry module beside `scripts/doc_health/families.py`**, taking the
      packet's recommendation, so the declaration is itself checked in the
      derived-not-restated shape `add-family-enumeration-check` establishes for
      the same problem one layer down. The two rejected homes are recorded with
      the ruling at `design.md` § 4: a contract artifact under
      `contracts/schemas/` (adds a schema, and would change § 4.4's
      no-bundle-owed answer) and a table in the promoted spec (prose a check must
      parse, which is the defect being designed away). THIS TASK IS THE RULING,
      NOT THE MODULE: writing the module is § 2.2, DONE.
- [x] 2.2 THE CLASS DECLARED at `scripts/doc_health/pin_class.py`, the home Q1
      ruled — `PIN_CLASS`, twenty `PinMember` rows, each carrying the path
      globs, the key, `key_form` (`field` or `prose`), the generator,
      `reproduction` (`tool-defined` or `measured`), `locality` (`repo-local` or
      `cross-repository`), `presence` (`current` or `future`) and a note. BOTH
      PROSE MEMBERS ARE DECLARED with their own patterns: the `.md` twin's
      `- Source revision:` line and the gate-action `notes:`/`recipe:` sentence.
      ALL FIVE FUTURE MEMBERS are declared — `ideation-dashboard-snapshot`,
      `-snapshot-index`, `ideation-workbench`,
      `xfactory-ideation-organizer-recommendations`, and
      `gate-intent.schema.yaml`'s `snapshot_rev_seen`, which the packet named
      only in passing — so the first committed instance is covered on arrival;
      `arrived_future_members` reports the arrival rather than waiting for
      somebody to notice. **A MEMBER IS A (PATH, KEY) PAIR, NOT A PATH**, forced
      by `capability-scenario-register.yaml` carrying two distinct pins, and by
      `hermes-install-g0-handoff.yaml` carrying ONE REPO-LOCAL AND ONE
      CROSS-REPOSITORY pin in the same file. `NON_MEMBERS` declares six
      exclusion rows WITH A REASON EACH (examples, negatives, fixtures and
      tests, schemas, markdown prose, `.openspec.yaml` origin narrative),
      because an exclusion nobody can read is a coverage gap in disguise.
- [x] 2.3 THE CLASS-WIDE REACHABILITY VERIFICATION implemented, riding the
      existing surface: `pin_class.verify()` is the engine and
      `ideation_readiness.verify_pin_reachability()` is the probe on the
      readiness-proof surface, returning `pass` / `fail` / `skip` so each caller
      turns it into its own surface's outcome. **JUDGED AGAINST REFS**:
      `merge-base --is-ancestor` against `main` plus
      `refs/retention/pins/<full-sha>` COMPUTED from the pin, and nothing else.
      The environment hazard this task named is pinned by test rather than
      merely avoided —
      `test_the_object_store_surviving_the_commit_is_not_a_defence` asserts that
      `cat-file -t` SUCCEEDS for a fixture orphan in the repository that made it
      while the probe reports the defect there and in a `--no-local` clone
      identically. FIVE STRAY-REF SHAPES ARE REFUSED by parametrized test,
      including the `refs/remotes/origin-retention/*` leftovers this checkout
      really carries from a since-deleted remote. **TWO MEASURED DECISIONS
      inside this task**, both recorded in the module and flagged in the
      realization report: (a) `main` resolves as `refs/remotes/origin/main`
      BEFORE `refs/heads/main`, because the shared checkout's local `main` sat
      at `26e1e021` while `origin/main` was at `0417e9b5` and consulting the
      local branch reported a pin that HAD landed as orphaned; (b) the retention
      namespace is consulted locally first and then by `git ls-remote origin`
      (no default refspec fetches `refs/retention/*`), and a remote that CANNOT
      be consulted yields INCONCLUSIVE rather than a pass or a defect — an
      unaskable question is not an affirmative answer.
- [x] 2.4 THE DECLARATION-COVERAGE CHECK implemented, both directions.
      `uncovered_sites` sweeps the declared scan roots for the pin-key
      vocabulary and reports any site no member covers, naming the artifact and
      the key; `vanished_members` reports a declared CURRENT row whose artifact
      no committed path matches. **THE COVERAGE HALF EARNED ITS KEEP ON ITS
      FIRST REAL RUN**: it reported `health/neutrality-drift/baseline/codexFactory.yaml`
      (`commit`), an artifact family nobody had declared, now a declared
      cross-repository member. The vanished direction is answered ONLY for the
      repository the declaration describes (`DECLARATION_SUBJECT_MARKERS`),
      because run anywhere else every row would "vanish" and the report would be
      noise a reader learns to ignore.
- [x] 2.5 THE REPRODUCTION CHECK implemented for the tool-defined members and
      HONESTLY BOUNDED for the rest. `ideation_readiness.index_reproduces_at()`
      reconstructs the corpus at a pin with a read-only `git archive`, re-runs
      the derivation and compares to the committed body; on the real repository
      the landed index REPRODUCES at its own pin (`4e57009c`, **290 entries,
      skeleton-identical**), and a fixture proves the refusal that matters —
      a pin HAND-MOVED to a perfectly reachable new tip with no regeneration is
      rejected, which is the exact act that produced `f13a3b60`. `cluster_skeleton`
      is now spelled ONCE and shared with the readiness proof, because two
      spellings of "the same skeleton" is how a reproduction claim quietly stops
      meaning anything. **THE NON-TOOL HALF IS FLAGGED, NOT FAKED**: this task
      asks the check to verify that a NAMED MEASUREMENT is recorded, and NO
      COMMITTED ARTIFACT RECORDS ONE — there is no measurement-record field,
      schema, or convention anywhere in the repository for a re-pin to write
      into. Inventing one would add a contract this packet explicitly declines
      to add. What is implemented instead is `repair_route()`, which states per
      member what a re-pin owes (bytes where a tool defines derivation, a named
      measurement where none does) at the moment a finding fires. A
      measurement-record format is a follow-up, recorded at § 5.3.
- [x] 2.6 REGRESSIONS at `tests/doc-health/test_pin_reachability.py` — 46 tests,
      all six minima covered and eight more besides. Reachable-but-stale gives
      no finding; an orphaned pin in a complete clone fails naming artifact, key
      and pin; a truncated clone skips naming the truncation OBSERVED (a real
      `--depth 1 --no-local` clone); an undeclared pin-carrying artifact is
      reported and the class is NOT reported fully verified; a hand-moved pin
      whose body does not reproduce is rejected; a pin reachable only through
      the computed retention ref passes, with the record's bytes asserted
      unchanged. Beyond the minima: the remote consult proved over a `file://`
      origin whose clone does not carry the ref; a retention ref pointing at the
      wrong commit refused; five stray ref names refused; declared-class drift in
      BOTH directions; the key-boundary defect the first real run exposed; per-
      site locality read out of the artifact; and the vocabulary's own coverage
      measured by resolving every committed 40-hex token against the object
      database rather than by trusting the key list.
- [x] 2.7 NO CHANGE to the deterministic check family registry, the family
      enumeration, or its numerals — and asserted STRUCTURALLY rather than
      promised. `scripts/doc_health/families.py` is untouched (`git diff` empty),
      `pin_class` defines no `fam_*` function and imports nothing from
      `families`, and `test_no_deterministic_check_family_is_added_by_this_verification`
      fails if `families.py` ever so much as mentions `pin_class` — so a later
      edit cannot register it as a family without deciding to. A count assertion
      was deliberately NOT used: it would break the day an unrelated change
      registers a family, which is the coupling this decision exists to avoid.
- [x] 2.8 THE LANDING-SIDE OBLIGATION IS STATED, NOT AUTOMATED, exactly as this
      task ruled, and the realization owes only that it be DISCOVERABLE where it
      binds. It is: `repair_route()` names, at the moment a finding fires, which
      route the artifact's own class allows — RETENTION for immutable evidence
      (`status: record`, or a machine-written manifest inside an archived
      packet), REPRODUCTION for a regenerable projection — and the probe's
      failure text carries those routes per orphan.
      `test_the_landing_obligation_is_discoverable_where_it_binds` pins it. NO
      WORKFLOW ENFORCES IT, and none is proposed: a branch-side check would have
      to run BEFORE the rewrite, because after it the state a regeneration would
      read is gone, and that is the engineering-lane question this packet does
      not answer.

**THE AUTHORED PLAN, KEPT VERBATIM** where the realization diverged from it,
because the plan is the argument for the shape that was built and a plan
rewritten to match what happened teaches nobody anything. Only § 2.2 and § 2.5
diverged, and both divergences are recorded against their own items above:

> **2.2 as authored** — "DECLARE THE CLASS in the registry module Q1 ruled, from
> `proposal.md` § The pin-carrying artifact inventory. **Nine pins, eight
> artifacts, four generators**, and per member: the path or path pattern, the
> key (including the two that are PROSE …), the generator that writes it, and
> whether reproduction is tool-defined. The four schema-declared future members
> … SHALL be declared as class members even though no committed instance holds a
> real pin today, so that the first one to land is covered on arrival rather
> than on discovery." — The FUTURE-member instruction was followed exactly (and
> a fifth added). The inventory was not, because it does not survive
> measurement: the class is 63 sites across 20 members, and the four generator
> families the packet's sweep missed are tabulated above.
>
> **2.5 as authored** — "For non-tool members, the check verifies that a NAMED
> measurement is recorded, not that bytes match." — Not implemented, and
> deliberately: nothing in this repository records such a measurement, and no
> field, schema or convention exists to record one in. The check cannot verify
> the presence of an artifact that has no form. `repair_route()` states the
> obligation instead, and § 5.3 carries the format as a follow-up.

## 3. The live orphaned pins — FOUR FOUND, THREE RETAINED, ONE LOST

**Q2 RULED AND EXECUTED, AND THE WINDOW IS CLOSED.** Brett ruled on 2026-08-27
that the retention refs publish FIRST, independently of this packet, taking the
recommendation § 3.3 offered; the orchestrating session executed it the same day.
Both refs are published on `origin` and were VERIFIED IN THIS WORKTREE rather
than taken on report. Q3's namespace ruling landed with it, so the refs are not
an ad-hoc choice — they are the namespace the requirements now name.

**AND THE COUNT WAS WRONG, WHICH IS THE POINT OF THE CHECK.** The packet knew of
two orphans. The realization's class-wide verification found FOUR: § 3.5 is a
third, retained the same day it was found; § 3.6 is a fourth that is
UNRECOVERABLE and is the first instance this repository has had to route through
requirement 2's other branch. The heading is corrected rather than left saying
two, and § 3.1 through § 3.4 are kept exactly as they were written about the two
the packet knew — a section rewritten to look prescient would erase the evidence
that a per-artifact sweep does not generalize.

- [x] 3.1 MEASURED AT AUTHORING AND RE-MEASURED BEFORE ACTING. Both records carry
      `status: record`:
      `health/ideation-readiness/2026-08-24/brainstorm-packet-migration-20260824.yaml:5`
      pins `da9bf3b7d0ee1d86d2d437d42a715c238dddce4b` and
      `…-final-20260824.yaml:5` pins
      `f13a3b6007736292e1e157febef1ac733e534de9`. For each, on 2026-08-27 at
      `origin/main` `42662b70`: `git branch -a --contains` EMPTY,
      `git ls-remote origin | grep -c` = `0`, `merge-base --is-ancestor
      origin/main` false, and `cat-file -t` = `commit` in a worktree of the
      shared checkout — so BOTH OBJECTS ARE STILL RECOVERABLE. That last fact is
      what makes retention possible and it expires without notice; re-measure it
      before choosing a route, which is what requirement 2 obliges.
      **RE-MEASURED 2026-08-27 IMMEDIATELY BEFORE RECORDING THE RULING**, and the
      answer had changed for the better: `git ls-remote origin | grep -c <pin>`
      now returns `1` for BOTH pins where it returned `0` at authoring, because
      the retention refs had landed. `merge-base --is-ancestor origin/main` is
      still false for both, and that is the intended end state rather than a
      residue — the pins resolve through the retention namespace, not through
      `main`, which is exactly the branch of requirement 1 that admits a
      retention ref.
- [x] 3.2 REPAIRED BY RETENTION, NOT BY RE-PIN. Both artifacts are `record`, so
      requirement 2 forbids editing their pins and `design.md` § 1 records the
      three rejected alternatives. **DONE 2026-08-27.** Published and verified by
      `git ls-remote origin 'refs/retention/*'`, which returns exactly two rows:
      `refs/retention/pins/da9bf3b7d0ee1d86d2d437d42a715c238dddce4b` at
      `da9bf3b7d0ee1d86d2d437d42a715c238dddce4b`, and
      `refs/retention/pins/f13a3b6007736292e1e157febef1ac733e534de9` at
      `f13a3b6007736292e1e157febef1ac733e534de9` — each ref pointing at the very
      commit its name states. **BOTH RECORDS ARE BYTE-IDENTICAL TO CAPTURE**;
      neither pin was touched, which is the claim requirement 2 makes,
      demonstrated on the two instances that forced it.
- [x] 3.3 THE ROUTE AND THE NAMING ARE RULED. **Q2: FIRST AND INDEPENDENTLY**,
      as recommended — a published ref is a remote-state act rather than a commit
      in a pull request, and the window was closing. **Q3: the namespace is
      `refs/retention/pins/<full-sha>`**, formalized and encoded in the delta
      rather than left as convention: requirement 1 names it and refuses any
      other name, requirement 2 obliges publishing it with the ref name COMPUTED
      from the pin, and requirement 4 states it as half the ref set a
      verification consults. The prediction in this task's authored text held
      exactly — the first two refs published DID set the convention, and the
      ruling declared it in the same act rather than leaving it implied.
      RETENTION LIFETIME remains deliberately unstated; see `proposal.md`
      § Open Questions Q3 for why.
- [x] 3.4 THE FALLBACK WAS NOT NEEDED, and the task closes as NOT-APPLICABLE
      rather than as done, because nothing was performed under it. As authored:
      if the window had closed by the time this was acted on, the route was the
      requirement's other branch — a SUPERSEDING record naming the loss and what
      is no longer verifiable, plus a disposition for the standing finding.
      Both objects were still present when § 3.2 ran, so both were retained and
      neither record was edited or deleted. The branch stays in the delta because
      the next orphaned record may not be caught in time. **AND THE BRANCH WAS
      NEEDED AFTER ALL, ONE ORPHAN LATER**: § 3.6 is the instance, found at
      realization, and it is the first time this repository has had to reach for
      the unrecoverable route. This task still closes NOT-APPLICABLE for the two
      records it was written about.
- [x] 3.5 **A THIRD ORPHAN, FOUND AT REALIZATION AND RETAINED THE SAME DAY.**
      Not in the packet's inventory, and not in any sweep this repository had
      ever run: `openspec/changes/archive/2026-08-22-add-doxbench-editing-phase-b/supporting-docs.manifest.yaml:31`
      pins `74022ea57354ab252abb0efa68c22474e4a2eb88` ("proposal-support: archive
      a change that has no supporting documents", 2026-08-21), and no ref reached
      it. MEASURED BEFORE ACTING, as requirement 2 obliges: `git cat-file -t` =
      `commit` in the shared object store, `git branch -a --contains` EMPTY,
      `git for-each-ref --contains` EMPTY, and the pin absent from ALL 566 refs
      `git ls-remote origin` advertises (403 of them `refs/pull/*`) — so the
      object was still recoverable and the window was open. **RETAINED
      2026-08-27**, by the route requirement 2 rules and the namespace Q3 named:
      `git push origin 74022ea5…:refs/retention/pins/74022ea5…`, verified by
      `git ls-remote origin 'refs/retention/pins/*'` now returning THREE rows,
      each at the commit its name states. THE MANIFEST WAS NOT EDITED: it sits
      inside an ARCHIVED packet, so the retention route applies for the same
      reason it applies to a `record` even though it carries no lifecycle
      header — which is why `repair_route()` keys on immutability rather than on
      a `Status:` line, and why a test pins that.
      **THIS IS A MEASURED DECISION TAKEN BY THE REALIZATION AND IS FLAGGED**:
      publishing a ref is a remote-state act. It was taken because the act is
      fully ruled (Q3 named the namespace, Q2's execution set the precedent, OD-4
      cleared the route), because it is purely additive and reversible by one
      command, and because the alternative was irreversible — an object nobody
      retains is gone when garbage collection reaches it, and this one had
      already survived five days by accident.
- [x] 3.6 **A FOURTH ORPHAN, AND THE FIRST UNRECOVERABLE ONE — THE BRANCH § 3.4
      HELD IN RESERVE.** `openspec/changes/archive/2026-08-27-add-hermes-customer-subject-runtime-contract/evidence/provider-verification.yaml:15`
      pins `66b14064bbd50d1af4e9585d10f8150f2bc352f0` under the key
      `us3_baseline_commit` — a key NO sweep vocabulary knew, which is exactly
      how a renamed key becomes a silent loss of coverage. It was found by
      enumerating every key name that carries a 40-hex value in committed
      structured state rather than by guessing which names a generator might
      pick, and that enumeration is now a test.
      MEASURED, and the answer is worse than § 3.5's: `git cat-file -t` FAILS,
      the pin is in NONE of the 566 advertised refs, the branch it was taken on
      (`005-customer-subject-runtime`) is gone from the remote, and
      `git fetch origin 66b14064…` is refused by the server with
      `upload-pack: not our ref` — the strongest available statement that the
      remote cannot reach it either. **RETENTION IS IMPOSSIBLE, not merely not
      yet performed.** Recorded in `pin_class.KNOWN_LOSSES` with the measurement
      and the act still OWED: a SUPERSEDING evidence record for
      `add-hermes-customer-subject-runtime-contract` naming the loss and what is
      no longer verifiable at that baseline, plus a disposition for the standing
      finding. **NEITHER IS PERFORMED HERE, DELIBERATELY**: both are governance
      acts with a named authority and neither is a code change, and a realization
      that wrote a superseding record for somebody else's archived evidence would
      be inventing provenance. The row is RE-MEASURED by test — the day the
      object turns out to be recoverable, retention is the route and the test
      fails saying so — and the class reports `fully_verified` FALSE while it
      stands, so the loss cannot quietly become background. **FLAGGED FOR
      BRETT.**

## 4. Archive gate

- [x] 4.1 `OPENSPEC_TELEMETRY=0 openspec validate govern-derived-pin-reachability
      --strict` and `--all --strict` both GREEN at realization:
      "Change 'govern-derived-pin-reachability' is valid" (exit 0), and
      `--all --strict` **76 passed / 0 failed (76 items)** (exit 0).
- [x] 4.2 `python3 -m pytest tests/doc-health -q` GREEN under `pipefail`, exit
      code read rather than inferred: **1123 passed / 0 failed / 0 skipped** in
      149s. The baseline this branch started from is **1077** (measured on the
      same tree with `--ignore=tests/doc-health/test_pin_reachability.py`), so
      the 46 new tests are the whole of the delta and none of them displaced an
      existing one. The full CI selection
      `python3 -m pytest tests/ -q -m "not postgres"` is recorded in the pull
      request body with its own numbers.
- [ ] 4.3 REALIZATION EVIDENCE per `release-realization`'s archive gate: this
      packet declares a non-empty `code_surface`, so it SHIPS ACTIVE and archives
      only on merged-plus-green on the openxFactory main line, in its own commit
      after the merge. **STILL OPEN BY DESIGN**: the realization pull request is
      open and is deliberately NOT merged or archived by the implementing
      session.
- [x] 4.4 NO CONTRACT BUNDLE IS OWED — RE-CHECKED AT REALIZATION as this task
      required, and by path rather than by `grep`. All 38
      `contracts/releases/*.digests.yaml` inventories were parsed into their
      **192 distinct inventoried paths**, and NONE of this change's four touched
      files is among them: `scripts/doc_health/pin_class.py` (new),
      `scripts/doc_health/ideation_readiness.py`,
      `tests/doc-health/test_pin_reachability.py`, and this packet's own
      `tasks.md`. A NAIVE `grep README.md` DOES hit 38 inventories and is a FALSE
      POSITIVE — the members are `contracts/README.md` and
      `contracts/hermes-runtime/README.md`, not the root file — which is why the
      check was done by parsing rather than by substring. Q1's ruling placed the
      declaration in `scripts/doc_health/`, NOT under `contracts/`, so the
      contingency this task named did not arise: no schema moved, no digest set
      changed, no release tag is owed, and no bundle is cut.
- [x] 4.5a **THE GATE'S OWN NOTE WAS RIGHT, AND TWO MORE ORPHANS TURNED UP.**
      § 4.5's note for the realization — "the verification in § 2.3 must consult
      the retention namespace, or it will report these two as orphans and red the
      gate this task just cleared" — was honoured: the namespace is half the ref
      set and the two records pass through it (`test_the_readiness_records_keep_the_pins_they_were_captured_with`).
      What the note could not anticipate is that the verification would find TWO
      MORE. § 3.5 was retained the same day and passes. § 3.6 is unrecoverable
      and CANNOT be repaired by code; it is declared in `KNOWN_LOSSES`, reported
      loudly, and holds `fully_verified` at FALSE while the superseding record it
      needs is still owed. **THE PYTEST GATE IS GREEN OVER IT, DELIBERATELY, AND
      THAT IS A MEASURED DECISION**: a standing governance obligation with no
      available code repair would otherwise red every unrelated change until the
      act lands, which is enforcement arriving through the back door — the exact
      reasoning four doc-health families launched advisory over a standing
      population under. `clean` excludes a declared, re-measured loss;
      `fully_verified` does not.
- [x] 4.5 THE TWO LIVE ORPHANS RESOLVED before the archive, by § 3 — and
      resolved before the MERGE rather than merely before the archive, which is
      more than this gate asked for. Requirement 4 turns an orphaned pin into a
      finding, so the change would otherwise have landed red on its own gate;
      both pins now resolve through `refs/retention/pins/<full-sha>` with both
      records unedited. Evidence at § 3.2. NOTE FOR THE REALIZATION: the
      verification in § 2.3 must consult the retention namespace, or it will
      report these two as orphans and red the gate this task just cleared.
- [x] 4.6 ORIGIN RETENTION VERIFIED at realization, and measured rather than
      asserted. `openspec/changes/govern-derived-pin-reachability/.openspec.yaml`
      is BYTE-IDENTICAL to its ratifying commit `f57287c7` ("The pin two packets
      deferred: an orphaned source_revision is a defect") — `git diff` against
      both that commit and `origin/main` is empty for that path. The realization
      touched no origin declaration: `release-realization`'s origin-retention
      rule makes any rewrite of it a contested-class act, so the veto clearance
      and the three question rulings stay recorded in `proposal.md`, and the two
      new orphans this realization found are recorded in THIS file rather than
      folded into the origin `reason` — the shape
      `harden-ideation-readiness-check` took for exactly this reason.
- [x] 4.7 README "OpenSpec Records" active entry PRESENT AND ACCURATE, verified
      at realization rather than assumed: `README.md:347` carries the
      `govern-derived-pin-reachability` row under "Active changes" with the
      ratification citation and its scope. The realization leaves it in the
      ACTIVE block, which is correct — the change ships active and the row moves
      to the archived block at archive, carrying the realization evidence. NOT
      EDITED HERE, deliberately: the row is accurate as written, and the pull
      request body carries the realization evidence until the archive commit
      moves it.

## 5. Named follow-ups, out of scope and deliberately not written

- [ ] 5.1 `git_generation()` pins `rev-parse HEAD` regardless of working-tree
      cleanliness (`scripts/bootstrap-ideation-cross-reference.py:144-154`), so
      an index can record a provenance claim about content no commit holds. This
      is `harden-ideation-readiness-check`'s own § 5.3, observed 2026-08-26 in
      the shared checkout, and it is a DISTINCT defect: it produces a pin that
      was never true, where this packet is about a pin that stopped being
      resolvable. Neither rule implies the other. Carried forward unticked so it
      does not fall out of the record on this packet's archive.
      **AND THE REALIZATION FOUND THE HONEST HALF OF THAT DEFECT ALREADY
      DEPLOYED, which sharpens the follow-up rather than closing it.** Of the 34
      committed proposal-support manifests, 24 carry a real forty-character pin
      and TEN DO NOT: six say `"source_revision": "uncommitted-worktree"`, one
      says `"not-applicable-ad-hoc"`, and three carry no `source_revision` at
      all. So THAT generator already refuses to write a pin it cannot mean,
      which is exactly the behaviour § 5.1 asks of `git_generation()` — the
      sentinel is a provenance claim a reader can check ("this was taken from a
      dirty tree") where a `rev-parse HEAD` on the same tree is a claim that
      looks true and is not. The class verification ignores the sentinels by
      construction, because it only reads full object names; the follow-up is
      whether the sentinel vocabulary should be shared, declared, and used by
      every generator rather than invented once per lane.
- [ ] 5.2 The cross-repository pin families — aggregation submodule gitlinks and
      the workflow-pin lockstep rule (xFactory `CLAUDE.md` working rule 2),
      `pinned_contract_manifest` and `neutral-product-pin`, release digest
      inventories, image digests. Different pin family, different remote,
      different authority, and for the gitlink rule a different repository.
      Named in `proposal.md` § The pin-carrying artifact inventory as out of
      scope rather than left to inference.
- [ ] 5.3 **A RECORDED-MEASUREMENT FORMAT FOR A RE-PIN**, raised by § 2.5's
      honest gap. Requirement 3 defines re-pinning by reproduction and admits a
      NAMED MEASUREMENT where no tool re-derives the artifact — and nothing in
      this repository records one. There is no field, schema, or convention for a
      re-pin to write the measurement into, so the check that would verify its
      presence has nothing to look for, and inventing a format here would add a
      contract this packet explicitly declines to add. What the realization does
      instead is state the obligation at the moment a finding fires
      (`pin_class.repair_route`). The follow-up is a small one: decide whether
      the measurement belongs in the artifact (a sibling `re_pin_measurement:`
      key), in the packet that performs the re-pin, or in a gate record — and
      whether it is checkable at all for an artifact nobody regenerates. Carried
      unticked so it does not fall out of the record on this packet's archive.
- [ ] 5.4 **MARKDOWN IS NOT SWEPT FOR COVERAGE, AND THAT IS A STATED TRADE.**
      `pin_class.NON_MEMBERS` excludes `**/*.md` because governance prose quotes
      pins constantly — a proposal narrating a landing, a migration-evidence file
      listing twelve manifests, an archive record naming a merge commit — and
      none of those is the quoting file's own derivation claim. A markdown file
      that genuinely carries its own pin is DECLARED
      (`ideation/cross-reference.md` is the one today) and verified like any
      other member, but a FUTURE markdown projection that pins its source and is
      never declared would go unswept where a `.yaml` one would be caught. The
      follow-up is whether a prose pin can be told from a prose QUOTATION of a
      pin mechanically at all; the honest answer today is no, which is why the
      class is a declaration. Carried unticked.
- [ ] 5.5 **THE SUPERSEDING RECORD § 3.6 OWES.** Not a follow-up this packet
      chose — a governance act it uncovered and cannot perform.
      `add-hermes-customer-subject-runtime-contract`'s archived
      `evidence/provider-verification.yaml` pins an UNRECOVERABLE commit, and
      requirement 2's second branch calls for a superseding record naming the
      loss plus a disposition for the standing finding. Recorded in
      `pin_class.KNOWN_LOSSES` with the full measurement, re-measured by test,
      and reported until it is discharged. **NEEDS BRETT** — the authority for
      that change's evidence, not this session.
