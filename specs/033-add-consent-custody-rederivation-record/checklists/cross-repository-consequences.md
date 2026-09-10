# Checklist: Cross-Repository Consequences — 033-add-consent-custody-rederivation-record

**Purpose**: Release-gate audit of the boundary between this feature and
everything downstream of it — whether §§ 6 and 7 are correctly left
unperformed with dated NOT-OWED lines, whether this feature writes no
consumer (OpsxFactory) file, advances no pin, and builds no part of F.2's
gate, whether clarify A2's cross-repo consequence (landing DECLARES the
consent family's re-derivation rule, converting `govern-archived-record-edits`'
posture for that family from REPORTED to REFUSED once F.2's gate exists) is
RECORDED in two named places and armed in none, whether the three non-uniform
consumer prescriptions are described nowhere as performed, whether the
README amendment set (Q8) touches exactly three sites and leaves two as
true-when-written, and whether the row-3 substrate note blocker on Phase F is
respected. This interrogates the WRITTEN plan and the CURRENT state of the
worktree — no `openspec/changes/add-consent-custody-rederivation-record`
consumer act and no README edit has happened yet.

**Artifacts under review**: `spec.md`, `plan.md`, `tasks.md` (Speckit tree);
the packet's `tasks.md` §§ 6–7 and `proposal.md` § *Impact*; `README.md`
(lines 840-870, 2940-2960, 2980-3000, 3010-3030, 3090-3105); the current git
worktree status.

**Date**: 2026-09-09. No-argument invocation — maximum coverage, no item cap.

## §§ 6 and 7 — Left Unperformed, With Dated NOT-OWED Lines

- [x] CHK001 Are ALL EIGHT §6/§7 boxes (6.1, 6.2, 6.2b, 6.3, 6.4, 7.1, 7.2,
      7.3) individually named in the Speckit `tasks.md`'s NOT-OWED
      disposition (T075), rather than covered by a single blanket sentence
      that could be read as skipping one? MEASURED: T075 reads "Dated
      NOT-OWED lines on §§ 6.1, 6.2, 6.2b, 6.3, 6.4 and 7.1, 7.2, 7.3 —
      named as owed elsewhere, performed nowhere here," naming all eight.
      [Completeness, tasks.md T075]
- [x] CHK002 Is each NOT-OWED line required to be DATED, so a reader can tell
      when the disposition was recorded rather than reading it as an
      undated, potentially stale assertion? [Precision, spec.md FR-040,
      tasks.md T075]
- [x] CHK003 Does the packet's own `tasks.md` § 6 header ("Listed for
      completeness and explicitly OUTSIDE this change's archive gate...
      the items below are OpsxFactory's, in OpsxFactory's own change, under
      OpsxFactory's own gates") match this feature's framing of §6 as
      NOT-OWED rather than merely deferred or optional? [Consistency, packet
      tasks.md § 6 header, Speckit tasks.md T075/Out of scope]
- [x] CHK004 Does the packet's own `tasks.md` § 7 header ("Named as owed
      elsewhere, and deliberately not taken here") match this feature's NOT-
      OWED framing for §7.1–7.3 identically? [Consistency, packet tasks.md
      § 7 header, Speckit tasks.md T075/Out of scope]
- [x] CHK005 Is the distinction between §§ 5.1/5.5/5.6 (NOT-OWED-**HERE** —
      owed by the SAME lane, later) and §§ 6–7 (NOT-OWED — owed by a
      DIFFERENT repository/party entirely) maintained without slippage
      anywhere §§ 6–7 are discussed in the Speckit tree? MEASURED: `spec.md`
      Measured baseline table, Out of scope section, and `tasks.md` Box
      Accounting table each preserve the two-way split. [Clarity, spec.md/
      tasks.md]

## No Consumer File Written, No Pin Advanced, No F.2 Gate Built

- [x] CHK006 Does `plan.md`'s "Repository files this feature writes" list
      (Project Structure section) name ANY path outside the openxFactory
      repository tree (e.g. an OpsxFactory `stack.yaml`, an OpsxFactory
      consent-instrument file)? MEASURED: every listed path
      (`contracts/`, `scripts/`, `examples/`, `tests/`, `README.md`,
      `openspec/changes/add-consent-custody-rederivation-record/…`) is
      inside openxFactory. No OpsxFactory path appears. [Completeness,
      plan.md Project Structure]
- [x] CHK007 Is `spec.md`'s own Assumptions section explicit that "No
      consumer repository is touched by this feature," matching the file
      list's silence on any OpsxFactory path? [Consistency, spec.md
      Assumptions, plan.md Project Structure]
- [x] CHK008 Does the current worktree's git status corroborate that no
      consumer file has been touched? MEASURED: `git status -sb` on this
      worktree shows only `specs/033-.../clarify-questions.md` and
      `specs/033-.../tasks.md` modified — no OpsxFactory path, no
      `contracts/` path, no `stack.yaml` (this feature has not yet executed
      §§ 2–5, consistent with the plan). [Measurability, git status]
- [x] CHK009 Is `stack.yaml`'s `contract_ref` re-pin (§ 6.1's
      "in lockstep with the worker-enrollment-broker's runtime-shape
      validation") named ONLY as OpsxFactory's owed act, with no task in
      this feature performing any part of it — not even a partial or
      preparatory edit? MEASURED: no Speckit task references editing
      `stack.yaml`; T075/Out of scope name § 6.1 as NOT-OWED wholesale.
      [Completeness, spec.md Out of scope § 6, tasks.md T075]
- [x] CHK010 Is F.2's custody-digest gate named as UNBUILT by this feature in
      terms strong enough to foreclose a partial implementation (a stub, a
      draft script) being read as progress toward it? MEASURED: packet
      `tasks.md` § 7.1 states "F.2's custody-digest gate is **NOT built
      here**... This packet supplies only the consent-custody family's
      re-derivation rule, which that gate consumes" — an unambiguous
      negative. [Precision, packet tasks.md § 7.1]
- [x] CHK011 Is the DECLARED CUSTODY STORE MAPPING (§ 6.2b, the
      `opsx:<tenant>/<repo-relative path>` resolution rule OpsxFactory must
      declare) distinguished from the NEUTRAL SCHEMA COMMENT this feature
      DOES write (T014, naming the MEASUREMENT that every OpsxFactory
      locator carries an `opsx:opensoft/` prefix), so that writing an
      in-file comment about a consumer's locator shape is not mistaken for
      declaring the consumer's mapping on its behalf? [Ambiguity, spec.md
      FR-005(c)/tasks.md T014, packet tasks.md § 6.2b]

## A2's Cross-Repo Consequence — Recorded in Two Places, Armed in None

- [x] CHK012 Are the TWO named places for A2's dated note identical between
      `spec.md` FR-047 and Speckit `tasks.md` T078 — "the realization
      evidence" and "the neighbourhood of § 7 in the packet's `tasks.md`"?
      MEASURED: both name the same two locations verbatim. [Consistency,
      spec.md FR-047, tasks.md T078]
- [x] CHK013 Is the CONTENT of A2's note specified precisely enough that an
      implementer could not under- or over-state the consequence — landing
      this realization DECLARES the consent family's re-derivation rule,
      which under `govern-archived-record-edits`' transition clause converts
      the posture for that family from REPORTED to REFUSED, but ONLY once
      F.2's gate exists (not immediately on landing)? MEASURED: FR-047, T078
      and `research.md` R14 all carry the "once F.2's gate exists"
      qualifier consistently — none states or implies an immediate REFUSED
      conversion. [Precision, spec.md FR-047/research.md R14/tasks.md T078]
- [x] CHK014 Is "RECORD IT; DO NOT ACT ON IT" (the clarify A2 ruling) carried
      through as an explicit prohibition in `spec.md`'s Out of scope section
      — "This feature RECORDS that and builds nothing for it" — not merely
      left implicit from the note's placement? [Traceability, spec.md Out of
      scope, clarify-questions.md A2]
- [x] CHK015 Does any task instruct building, scheduling, or ticking
      ANYTHING for A2's consequence — a stub gate, a placeholder check, a
      TODO issue filed against F.2 — which would constitute "arming" it
      contrary to the ruling? MEASURED: T078 explicitly states "Build
      nothing, schedule nothing, tick nothing" for A2; no other task
      references F.2 except to name it as NOT-OWED (§ 7.1/T075).
      [Completeness, tasks.md T078/T075]
- [x] CHK016 Is the PREMISE A2 falsifies — `README.md:2991-2993`'s "NO family
      anywhere has a declared re-derivation rule today — the consent
      family's is PROPOSED only (`contract_schema_version: 2`, no
      `custody_rederivations` property, `contract-v3.4`, 46/46 boxes
      unticked)" — quoted identically in `research.md` R14 and reflected in
      `spec.md`'s clarify A2 section, so the "converts... from REPORTED to
      REFUSED" claim is traceable to the exact sentence it falsifies rather
      than to a paraphrase? MEASURED: R14 and `README.md:2991-2993` match
      verbatim. [Traceability, research.md R14, README.md:2991-2993]
- [x] CHK017 Is it stated that the conversion is CONDITIONAL on an act
      OUTSIDE this feature's control (F.2's gate existing) and not a fixed
      future date, so a later reader cannot mistake A2's note for a
      commitment this feature or its lane can unilaterally fulfil?
      [Clarity, spec.md FR-047, packet tasks.md § 7.1]

## The Three Non-Uniform Consumer Prescriptions — Described, Not Performed

- [x] CHK018 Are the three prescriptions (the TWO-entry chains for
      `opensoft-exchange-monitor` and `opsx-farheap-service-discovery`, the
      ONE-entry chain for `opsx-opensoft-node-inventory`) named in `spec.md`/
      `research.md` ONLY as consumer-owed content — descriptive of what
      OpsxFactory must eventually write — never as a task this feature
      executes? MEASURED: the packet's `tasks.md` § 6.2 carries the full
      prescription text and is listed under the `[OpsxFactory]` tag,
      NOT-OWED in this feature's accounting (T075); no Speckit `T###`
      writes any instrument file. [Completeness, packet tasks.md § 6.2,
      Speckit tasks.md T075]
- [x] CHK019 Is the NON-UNIFORMITY itself (two targets need a two-entry
      chain because they archived BEFORE `57fd9fd2`; one target is uniform
      because it never archived) preserved accurately wherever this feature
      restates it, matching the packet's own § 6.2 and the ratification
      record's "What this ratification authorizes" section digest-for-digest
      (`bb8f89ea…`→`5c87d547…`, `b5d4ab55…`→`d9eecee3…`,
      `31e4f889…`→`7fc4bb21…`)? MEASURED: consistent across
      `proposal.md` Example A/B, packet `tasks.md` § 6.2, and the
      ratification record. [Consistency, packet tasks.md § 6.2/proposal.md/
      ratification record]
- [x] CHK020 Is it stated that these digests are to be RE-MEASURED at write
      time rather than copied from the packet (packet § 6.2: "Re-measure
      each digest at write time rather than copying these; they were taken
      at the OpsxFactory tree on 2026-09-07"), and does this feature's own
      documentation avoid presenting the packet's cited digests as
      authoritative for a future write? [Precision, packet tasks.md § 6.2]
- [x] CHK021 Is the "NO `amendments` entry anywhere" instruction (C-10,
      design.md) carried into this feature's description of § 6.2 without
      this feature itself writing or testing an `amendments`-entry-absent
      instrument as a CONSUMER artifact (as opposed to a NEUTRAL fixture
      demonstrating the schema permits it)? [Ambiguity, packet tasks.md
      § 6.2, ratified delta "A re-derivation does not amend the instrument"]

## README Amendment Set (Q8) — Exactly Three Sites, Two True-When-Written

- [x] CHK022 Are the THREE sites FR-046 names for amendment
      (`README.md:856-857`'s "all 46 boxes... stay unticked";
      `README.md:3022-3023`'s present-tense box count keeping "the three
      pins are still broken"; `README.md:2993`'s "46/46 boxes unticked"
      inside the `govern-archived-record-edits` row) each located at the
      line number FR-046/Q8 states? MEASURED: `grep -n` over `README.md`
      confirms "stay unticked" at line 857, "the three pins are still
      broken" at line 3023, and "46/46 boxes unticked" at line 2993 —
      matching FR-046/Q8 exactly. [Precision, spec.md FR-046,
      clarify-questions.md Q8, README.md]
- [x] CHK023 Are the TWO sites left as true-when-written
      (`README.md:2949-2950`'s past-tense "left its 46";
      `README.md:3098-3100`'s dated "measured 2026-09-09 UTC at `main`
      `6cc06288`... still carries all 46 boxes unticked") each located at
      the line FR-046/Q8 states, and does Q8's ruling explicitly justify
      NOT amending them (past tense survives; a dated measurement is true
      as of its date)? MEASURED: `grep -n` confirms "left its 46" at line
      2950 and "6cc06288" at line 3099 — matching. [Precision, spec.md
      FR-046, clarify-questions.md Q8, README.md]
- [x] CHK024 Does the set of five sites (three amended + two left) account
      for EVERY README sentence clarify Q8 originally surveyed, with no
      sixth site introduced later without a corresponding ruling? MEASURED:
      Q8's own text enumerates four numbered statements plus "a FIFTH site
      the reviewer found" (`README.md:2993`) — five total, matching FR-046's
      three-amend/two-leave split exactly. [Completeness, clarify-questions.md
      Q8]
- [x] CHK025 Is "KEEP 'the three pins are still broken'" (FR-046) precise
      about WHICH clause of `README.md:3022-3023`'s sentence survives the
      amendment and which does not, so an implementer amending that sentence
      could not also strike the surviving half by mistake? MEASURED: FR-046
      states the amendment targets "the present-tense box count" while
      explicitly preserving "the three pins are still broken... because that
      half stays true (the repair is § 6, the consumer's)." [Precision,
      spec.md FR-046]
- [x] CHK026 Has ANY of the three amendment sites been edited in this
      worktree yet, which would make CHK022's "planned" framing stale?
      MEASURED: `git status -sb` shows `README.md` unmodified — Phase F
      (T055-T059) has not executed. [Measurability, git status]

## The Row-3 Substrate Note Blocker

- [x] CHK027 Is Phase F (T055-T059) stated as BLOCKED on the lane's
      row-3 substrate note for the two sibling-row sentences (README.md:3022
      and README.md:2993), with this packet's own row (README.md:856-857)
      explicitly exempted via its standing row-3 claim (`5571680388`,
      2026-09-07)? MEASURED: T055/FR-046 both draw this exact distinction.
      [Precision, spec.md FR-046, tasks.md T055]
- [x] CHK028 Does the Dependencies graph correctly show Phase F as a
      standalone branch off Phase E that does NOT feed into Phase G or H —
      so a substrate note that never arrives blocks ONLY T057/T058, never
      the cut or the bookkeeping? MEASURED: the graph shows `E -> {F, G}`
      with F annotated "BLOCKED on the lane's substrate note" and G
      annotated "LAST; must not wait on F" — H depends only on G.
      [Consistency, tasks.md Dependencies graph]
- [x] CHK029 Is a CHANNEL or MECHANISM named by which "the LANE... post[s]
      the row-3 substrate note," and a stated cadence for RE-CHECKING whether
      it has arrived? **RE-VERIFIED, RESOLVED.** T055 now carries "CHANNEL
      AND CADENCE, stated rather than left to inference. Posting is a LANE
      act, exactly as § 5.1's version claim is — this seat opens no pull
      request and posts no comment. The orchestrator does NOT poll: it
      RE-CHECKS whether the note has arrived at **each merge-from-main**, the
      same cadence the version re-measurement runs on (T060), and reports the
      state each time." This draws the exact §5.1 parallel this item asked
      for, explicitly rather than by inference. [Gap-closure, tasks.md
      T055, spec.md FR-046/Out of scope]
- [x] CHK030 Is it explicit that Phase F's non-arrival does NOT gate the
      feature's "Definition of done"? MEASURED: `tasks.md`'s Definition of
      done lists "All 35 in-scope packet boxes ticked," "11 boxes carrying
      dated NOT-OWED / NOT-OWED-HERE lines," `SC-001`..`SC-010`,
      `speckit-analyze` zero findings, and "the branch is pushed" — none of
      T055-T059 (which correspond to no packet box at all; the README sites
      are additional realization acts per FR-046/A1, not packet boxes)
      appears in this list, so a substrate note that never arrives leaves
      T057/T058 open without blocking completion. [Consistency, tasks.md
      Definition of done vs Phase F]

## False-Record Class

- [x] CHK031 Does any artifact in the Speckit tree state or imply that the
      consumer handoff (§ 6), F.2's gate (§ 7.1), F.3's settlement (§ 7.2),
      or any other content-address family's re-derivation record (§ 7.3) has
      been performed, scheduled with a date, or built in any part, which
      would be a false record of an act this feature does not own? MEASURED:
      every reference found (`spec.md` Out of scope, `plan.md` Constitution
      Check, `tasks.md` T075/T078) uses NOT-OWED / "builds nothing" /
      "performed nowhere here" language with no qualifying claim of partial
      completion. [Completeness, spec.md/plan.md/tasks.md]
- [x] CHK032 Does any artifact claim the README amendments (Q8) are already
      applied, or that the substrate note has already been posted, ahead of
      either actually occurring? MEASURED: `tasks.md` frames T056-T058 in
      future/imperative tense ("Amend..."), T055 as an open BLOCKER, and
      `git status` confirms `README.md` is unmodified — no artifact asserts
      completion. [Completeness, tasks.md Phase F, git status]
