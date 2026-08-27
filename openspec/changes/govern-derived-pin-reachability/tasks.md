# Tasks: govern-derived-pin-reachability

**NO IMPLEMENTATION is discharged here. This packet is a PROPOSAL**: it carries
the delta, the measurement, the inventory and the plan, and it changes no code
and repairs no pin. § 1 records what the filing itself discharged. § 2 is the
implementation plan, entirely open. § 3 is the live-orphan resolution, open and
TIME-BOUND. § 4 is the archive gate. § 5 records two adjacent gaps that are
deliberately not this change.

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
- [ ] 1.5 THE FIVE FLAGGED DECISIONS AND THE THREE OPEN QUESTIONS DISPOSED.
      Open. The veto window on § Orchestrator decisions 1–5 stays open until a
      ruling closes it, and Q1 (where the declared class lives), Q2 (whether the
      live-orphan repair rides this change) and Q3 (whether a retention-ref
      namespace is owed) each carry a recommendation and NO decision. A ruling
      that clears them SHALL be recorded here and at § Orchestrator decisions,
      so that a closed window is legibly closed rather than merely unexercised —
      the shape both sibling packets used.

## 2. Implementation plan (open — nothing here is done)

- [ ] 2.1 SETTLE Q1 FIRST, because everything else in § 2 depends on it. The
      declared pin class needs a home: a registry module beside
      `scripts/doc_health/families.py` (recommended), a contract artifact under
      `contracts/schemas/`, or a table in the promoted `doc-health` spec. Do not
      write the check before this is ruled; a check whose class declaration
      moves is a check rewritten twice.
- [ ] 2.2 DECLARE THE CLASS from `proposal.md` § The pin-carrying artifact
      inventory. Nine pins, eight artifacts, four generators, and per member:
      the path or path pattern, the key (including the two that are PROSE — the
      `.md` twin's `- Source revision:` line and the gate-action `recipe:`
      string), the generator that writes it, and whether reproduction is
      tool-defined. The four schema-declared future members
      (`ideation-dashboard-snapshot`, `-snapshot-index`, `ideation-workbench`,
      `xfactory-ideation-organizer-recommendations`) SHALL be declared as class
      members even though no committed instance holds a real pin today, so that
      the first one to land is covered on arrival rather than on discovery.
- [ ] 2.3 IMPLEMENT THE CLASS-WIDE REACHABILITY VERIFICATION beside the existing
      probe in `scripts/doc_health/ideation_readiness.py`, reusing the
      complete-clone / truncated-clone distinction the sibling's promoted
      requirement already defines rather than spelling a second one. Judge
      reachability against REFS (`merge-base --is-ancestor` against `main`, plus
      any declared retained ref), NOT against the local object store — a
      `cat-file -t` that succeeds because the object survives locally is exactly
      the false pass requirement 1 forbids. NOTE THE ENVIRONMENT HAZARD: in an
      agent worktree sharing an object store, both live orphans resolve with
      `cat-file` and neither is an ancestor of `main`; a probe written against
      `cat-file` would report this repository clean.
- [ ] 2.4 IMPLEMENT THE DECLARATION-COVERAGE CHECK: an artifact carrying a
      repo-local commit pin that no declared member covers is reported, naming
      the artifact and the key. This is the half of requirement 4 that a
      pattern-scanner cannot provide, and `design.md` § 4 records why.
- [ ] 2.5 IMPLEMENT THE REPRODUCTION CHECK for the tool-defined members: the
      committed body regenerates byte-for-byte at the pin. For the index this is
      `scripts/bootstrap-ideation-cross-reference.py` plus the strict index
      validator, which is the mechanism `harden-ideation-readiness-check`
      already used to prove its own re-pin at three revisions. For non-tool
      members, the check verifies that a NAMED measurement is recorded, not that
      bytes match.
- [ ] 2.6 REGRESSIONS under `tests/doc-health/`, at minimum: reachable-but-stale
      pin gives no finding; orphaned pin in a complete clone fails, naming
      artifact and pin; truncated clone skips, naming the truncation observed;
      an undeclared pin-carrying artifact is reported; a hand-moved pin whose
      body does not reproduce at the new pin is rejected; and a pin reachable
      only through a declared retained ref passes. Use bare `--no-local` clones
      for the reachability cases — the sibling's realization proved the
      shared-object-store hazard is real and that isolated clones are the only
      honest venue.
- [ ] 2.7 NO CHANGE to the deterministic check family registry
      (`scripts/doc_health/families.py`), the family enumeration, or its
      numerals. If an implementation finds itself adding a family id, § 3 of
      `design.md` has been contradicted and the packet needs re-ruling, not a
      quiet enumeration edit.
- [ ] 2.8 THE LANDING-SIDE OBLIGATION (requirement 3) IS STATED, NOT AUTOMATED,
      and that is deliberate. A landing is performed by humans and merge buttons.
      Whether a branch-side check can discharge it — and it would have to run
      BEFORE the rewrite, because after it the state a regeneration would read is
      gone — is an engineering-lane question this packet does not answer. What
      the realization owes is that the obligation is discoverable at the moment
      it binds, not a workflow that enforces it.

## 3. The two live orphaned pins (open, and TIME-BOUND)

- [ ] 3.1 MEASURED AT AUTHORING, RE-MEASURE BEFORE ACTING. Both records carry
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
- [ ] 3.2 REPAIR BY RETENTION, NOT BY RE-PIN. Both artifacts are `record`, so
      requirement 2 forbids editing their pins and `design.md` § 1 records the
      three rejected alternatives. The repair publishes refs reaching
      `da9bf3b7` and `f13a3b60`, leaving both records byte-identical.
- [ ] 3.3 THE ROUTE AND THE NAMING ARE Q2 AND Q3, UNRULED. Q2: whether the
      retention rides this change or lands first — recommendation is FIRST,
      independently of this packet's fate, because a published ref is a
      remote-state act rather than a commit in a pull request and the window is
      closing. Q3: what the refs are called and how long they live — the first
      two published will set the convention whether or not anyone declares one.
- [ ] 3.4 IF THE WINDOW HAS CLOSED by the time this is acted on, the route is
      the requirement's other branch: a SUPERSEDING record naming the loss and
      what is no longer verifiable, plus a disposition for the standing finding.
      Neither record may be edited or deleted to make the finding disappear.

## 4. Archive gate

- [ ] 4.1 `OPENSPEC_TELEMETRY=0 openspec validate govern-derived-pin-reachability
      --strict` and `--all --strict` both green.
- [ ] 4.2 `python3 -m pytest tests/doc-health -q` green, with the shell running
      `pipefail` — a piped pytest hides a red suite, and this repository has
      merged two pull requests red that way.
- [ ] 4.3 REALIZATION EVIDENCE per `release-realization`'s archive gate: this
      packet declares a non-empty `code_surface`, so it SHIPS ACTIVE and archives
      only on merged-plus-green on the openxFactory main line, in its own commit
      after the merge.
- [ ] 4.4 NO CONTRACT BUNDLE IS OWED — checked, not assumed: no file this change
      would edit appears in any `contracts/releases/*.digests.yaml` inventory.
      RE-CHECK at realization, because Q1 may place the class declaration under
      `contracts/`, and a new schema there changes this answer.
- [ ] 4.5 THE TWO LIVE ORPHANS RESOLVED before the archive, by § 3. Requirement 4
      turns both of them into findings, so the change would otherwise land red on
      its own gate — the same reason the sibling's OD-4 rode its repair.
- [ ] 4.6 ORIGIN RETENTION VERIFIED: `.openspec.yaml`'s origin declaration
      byte-identical to the ratifying commit. `release-realization`'s
      origin-retention rule makes any rewrite of it a contested-class act, so a
      veto clearance or a question ruling is recorded in `proposal.md`, NOT by
      editing the origin block — the shape `harden-ideation-readiness-check`
      took for exactly this reason.
- [ ] 4.7 README "OpenSpec Records" active entry present and accurate at
      authoring; MOVED to the archived block at archive, carrying the realization
      evidence.

## 5. Named follow-ups, out of scope and deliberately not written

- [ ] 5.1 `git_generation()` pins `rev-parse HEAD` regardless of working-tree
      cleanliness (`scripts/bootstrap-ideation-cross-reference.py:144-154`), so
      an index can record a provenance claim about content no commit holds. This
      is `harden-ideation-readiness-check`'s own § 5.3, observed 2026-08-26 in
      the shared checkout, and it is a DISTINCT defect: it produces a pin that
      was never true, where this packet is about a pin that stopped being
      resolvable. Neither rule implies the other. Carried forward unticked so it
      does not fall out of the record on this packet's archive.
- [ ] 5.2 The cross-repository pin families — aggregation submodule gitlinks and
      the workflow-pin lockstep rule (xFactory `CLAUDE.md` working rule 2),
      `pinned_contract_manifest` and `neutral-product-pin`, release digest
      inventories, image digests. Different pin family, different remote,
      different authority, and for the gitlink rule a different repository.
      Named in `proposal.md` § The pin-carrying artifact inventory as out of
      scope rather than left to inference.
