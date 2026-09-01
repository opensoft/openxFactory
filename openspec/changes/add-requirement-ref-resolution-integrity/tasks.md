# Tasks: add-requirement-ref-resolution-integrity

Governance-level and dependency-ordered. **This change is RATIFIED** (2026-09-01,
Brett Heap, by direct ruling — `review/ratification-2026-09-01.md`). § 1 was
authored in this pull request; **§ 2 CARRIES THE RATIFICATION and its dispositions,
two of its four boxes disposed rather than closed**; § 3 onward are for the
implementer and belong to a separate realization pull request, on the pattern this
packet's own subject set established (proposal PR #497, realization PR #516).

**NOTHING ELSE HAS MOVED.** § 3 – § 6 are the unbuilt realization slice, § 7's
verification gates are untouched, § 8's archive gate is untouched, and § 9 records
what this change deliberately does not close — **now including § 9.4, the one
review finding that is OPEN at the ratified tip and routed rather than repaired.**
Ratification authorizes realization and performs none of it.

Evidence convention, unchanged from the family's standard: a box closes on a
FACT that survives the session — a merged commit, a green run named by id, a
file path, a command and its output — never on an intention.

## 1. The packet (THIS PULL REQUEST)

- [x] 1.1 `credential-contracts` — **TWO ADDED requirements over TWELVE
      SCENARIOS**: the per-binding reporting duty (six scenarios, one of them the
      falsifiable reproduction), and the own-code-family phasing rule (six
      scenarios).
- [x] 1.2 **NO `## MODIFIED Requirements` block anywhere in this packet**, and
      the choice is MEASURED rather than preferred. The two requirements a
      reconciling MODIFIED block would have named — *"A credential binding
      declares the consuming system that holds it and the identity it fetches
      with"* and *"Two bindings on one secret are refused unless every pair
      declares distinct consumers…"* — are carried by NO promoted specification
      (`openspec/specs/credential-contracts/spec.md` holds seven titles, neither
      of them these) and are ADDED by the then-ACTIVE, ratified, unarchived
      `add-binding-consumer-identity`. A MODIFIED block over either would then
      have been exactly the shape `govern-sibling-added-modified-deltas` governs:
      a ``**Modified over `<basis>`'s addition by <change-id> (<date>):**``
      marker plus an ARCHIVE-ORDER HOLD behind the sibling. A pure ADDED
      requirement serves, so this packet takes it, carries no marker and imposes
      no hold.
      **RE-MEASURED 2026-09-01, AFTER THE CATCH-UP MERGE OF `origin/main`
      `1c1dcbbe`, AND THE BOX STILL TICKS.** PR #541 ARCHIVED
      `add-binding-consumer-identity` on 2026-08-31 (basis-first, with
      `add-notebook-hosting-credential-custody`), so the promoted spec now carries
      TWELVE titles and BOTH of the two named above ARE among them (`:278` and
      `:440`). A MODIFIED block over either would now be an ORDINARY block over
      promoted canon — no marker, no hold, the basis having archived. **The
      CHOICE is unchanged and only its REASON moved**: an all-ADDED delta served
      before because it avoided a marker and a hold, and serves now because the
      reporting duty is still a duty this capability states nowhere. Neither
      ADDED title collides with the twelve promoted ones — checked, not assumed.
      Both measurements are recorded in proposal.md § The sibling rule, measured
      and in `review/ratification-2026-09-01.md` § The catch-up merge.
- [x] 1.3 The reproduction is IN the packet as a falsifiable scenario
      (*"The shipped check is silent on both of them today"*), not only as
      prose in § What was measured — so a later reader can re-run it against
      whatever the validator has become.
- [x] 1.4 `.openspec.yaml` — `kind: ad_hoc`, origin id
      `openxFactory:adhoc:2026-08-31-add-requirement-ref-resolution-integrity`,
      `reason` naming issue #523 and the PR #516 review thread, `approved_by`
      recording Brett Heap's 2026-08-30 ruling AS A DECISION TO FILE and
      explicitly NOT as a ratification of content, `approved_on: 2026-08-30`.
- [x] 1.5 README "OpenSpec Records" active entry, stating the defect, the
      reproduction, the code-versus-narrowing choice as the ruling recorded it,
      the all-ADDED shape and the draft posture.
- [x] 1.6 `OPENSPEC_TELEMETRY=0 openspec validate
      add-requirement-ref-resolution-integrity --strict` and `--all --strict`
      both green.
- [x] 1.7 `python3 -m pytest tests/doc-health -q` green, and a same-clock
      doc-health run against an `origin/main` baseline in an identically named
      directory shows ZERO NEW FINDINGS. Docs-only, so the suite's pinned skip
      count MUST NOT move.
- [x] 1.8 § Authoring decisions AD-1 … AD-6 and § Open questions OQ-1 … OQ-4
      are stated as the AUTHORING SESSION'S and are flagged for veto. None is
      presented as ruled.
- [x] 1.9 **The Codex round on PR #542, both findings repaired in the packet.**
      (a) The reproduction's Control A claimed a ONE-BYTE edit over
      `example-secret-one` -> `example-secret-two`, which is THREE bytes. The
      reproduction was REBUILT on `example-secret-a` / `example-secret-b` and
      RE-RUN against `scripts/validate-credential-contracts.py` at this branch's
      merge-base; the templates are now the same length and differ at one offset,
      the recorded outputs are that run's, and the delta scenario *"The shipped
      check is silent on both of them today"* states the single-byte spacing in
      its WHEN so the claim is checkable rather than asserted; § What was
      measured § 6 now carries BOTH REPRODUCTION FILES IN FULL, so the run is
      re-executable from this packet alone rather than from a description of a
      tree nobody kept. (b) AD-1 offered a one-code branch that struck ONE
      scenario while the delta still obliged "NAMED APART" and the tasks and
      `code_surface` still bought two codes — a packet that would have ratified a
      permission and a prohibition together. AD-1 now carries the COMPLETE
      twelve-item AD-1/ONE-CODE AMENDMENT SET, and § 2.2 and § 3.3 point at it.
      The recommendation stands UNCHANGED at TWO codes.

## 2. Ratification — DONE 2026-09-01, BY DIRECT RULING

**RATIFIED 2026-09-01 BY DIRECT RULING** — Brett Heap (repository owner), in
session via an explicit multi-choice put, session `openxfactory-f5`; record
`review/ratification-2026-09-01.md`. **AD-1 IS RULED TWO CODES, AS DRAFTED**, and
the twelve-item AD-1/ONE-CODE AMENDMENT SET is DECLINED — none of its items
executed, and it is left standing in the proposal rather than struck. **NO §7.4
SITTING WAS CONVENED**, § 2.3 having left that question to Brett rather than
prescribing one. Each box below therefore carries its MEASURED disposition, and
TWO OF THE FOUR DO NOT TICK: a box that routes every open question to a ruling
cannot be ticked by a ruling that reached the decisions and not the questions, and
a box that puts a live question cannot be ticked by the act that answered it.

- [x] 2.1 **DONE.** Brett Heap read the packet and ruled: RATIFY, by direct
      ruling of the repository owner, over tip `deb72c8e`. Ratification authorizes
      REALIZATION and performs none of it; `proposal.md` now carries
      `Status: ratified` with the record-citing `Ratified:` line, and § 3 onward
      may start in a SEPARATE pull request.
- [ ] 2.2 **PARTLY ANSWERED, AND THEREFORE NOT TICKED.** This box asks for TWO
      things and got one. **THE AD SIDE IS DISCHARGED IN FULL**: AD-1 is RULED
      TWO CODES — the decision the box names as "the one that changes the spec
      text" — and AD-2 … AD-6 stand ACCEPTED AS DRAFTED. The box's own prediction
      held exactly: the ruling took ONE SENTENCE and executed as ZERO EDITS,
      because the one-code branch was enumerated as a mechanical amendment set,
      so no delta requiring two codes was ever left standing beside a ruling
      permitting one. **THE OQ SIDE IS NOT**: OQ-1 … OQ-4 received neither a
      ruling nor an explicit defer. They REMAIN OPEN exactly as
      `proposal.md` § Open questions leaves them, each with its recommendation
      and no decision, and they travel with § 4, § 9.1 and § 9.2. Ticking this
      box would assert four dispositions that were never taken.
- [ ] 2.3 **ANSWERED, NOT PERFORMED — AND THEREFORE NOT TICKED.** This box put a
      QUESTION rather than an obligation: whether to convene a §7.4-shaped sitting
      was Brett's call and was not assumed. **HE TOOK THE DIRECT PATH.** No
      sitting was convened, no seat sat, no ballot was cast, and nothing in this
      packet may be cited as a council disposition. The box named the
      `govern-sibling-added-modified-deltas` precedent as the nearer one and it
      was: that packet was ratified 2026-08-31 by direct ruling with the sitting
      it had PRESCRIBED for itself declined, and this one never prescribed a
      sitting at all. The box's `review/` condition is honoured in its own terms —
      the directory was created only when there was a record to put in it, and
      what it holds is a RATIFICATION record, not a sitting record. A box asking
      "shall we convene?" cannot be ticked by the answer "no".
- [x] 2.4 **DONE in the ratification commit.** `proposal.md` carries
      `Status: ratified` plus the RECORD-CITING `Ratified:` spelling — the branch
      of this box that applies, there being no approving OpenSpec change to name,
      so `Ratified by:` would mean naming a change that does not exist; the
      citation names an approver, a date AND a resolvable record path, all three
      of the three-way floor rather than the one it needs. The record is
      `review/ratification-2026-09-01.md`. Swept in the SAME commit, on the rule
      that any edit changing what a packet asserts about itself owes a sweep of
      every site asserting the same thing: `proposal.md`'s new § Standing, its
      § Authoring decisions preamble, AD-1's heading and its amendment-set
      heading, § The sibling rule measured, § Impact's sibling states,
      `.openspec.yaml`'s `approved_by` and three `related:` rows, this file's
      header and § 1.2, and the README active-changes entry.

## 3. Realization — the validator arm (SEPARATE PULL REQUEST)

- [ ] 3.1 **Re-measure before editing.** Re-run the reproduction of § What was
      measured against the tree as it then stands and paste the output. If it no
      longer reproduces, STOP and dispose of the packet rather than implementing
      against a defect that has moved.
- [ ] 3.2 A per-binding resolution pass reached from `_deprecation_warnings`,
      running for every binding whose consumer block declares a
      `requirement_ref` that is a well-formed qualified reference with a
      grammatical document reference — the two shapes the existing
      `consumer-member-grammar` and `consumer-requirement-ref-grammar` arms
      already report are NOT reported twice, one fault keeping one finding.
- [ ] 3.3 Two codes, one per status: `not-found` and `ambiguous` reported apart.
      Proposed spellings `requirement-ref-unresolved` and
      `requirement-ref-ambiguous`; both join `DEPRECATION_CODES` (8 -> 10) and
      `WARNING_EXPECTATIONS`. **Subject to AD-1**, and if the ratifier rules ONE
      code this row is not the only thing that moves: the whole edit is the
      AD-1/ONE-CODE AMENDMENT SET enumerated in proposal.md § Authoring
      decisions, applied ENTIRE in the ratifying commit — this row is its item 8.
      Reaching realization with a one-code ruling and a two-code delta still
      standing is the failure this cross-reference exists to prevent.
- [ ] 3.4 `resolve_requirement` is CALLED, not edited: same statuses, same
      index, same grammar, same never-open-a-path rule. A diff touching that
      function's body is out of scope and should be justified or reverted.
      **BUT SEE § 9.4 BEFORE TREATING THIS ROW AS COMPLETE.** The third Codex
      round (2026-08-31, on the ratified tip `deb72c8e`) found that this freeze,
      as written, would carry an INHERITED gap forward silently: the resolver
      matches `index.get(requirements_document_ref)`, so one requirement id
      sitting in TWO schema-valid documents resolves `ok` from either, leaving the
      CROSS-DOCUMENT arm of the promoted ambiguity scenario unmet. That finding is
      OPEN and routed to § 9.4. The implementer must BROADEN the lookup or
      EXPLICITLY AMEND that promoted scenario, and must not do neither — this row
      is the freeze, not a licence to leave the gap unnamed.
- [ ] 3.5 The lift path is untouched. A sharing pair whose reference does not
      resolve still gets the `shared-secret-identity` ERROR naming the condition
      that stood, AND now also the per-binding warning. A test asserts BOTH are
      present and that neither replaced the other.
- [ ] 3.6 **The negative direction is asserted by a NAMED test**: a binding whose
      reference resolves to exactly one requirement, and a binding declaring no
      `requirement_ref` at all, each produce NOTHING from the new arm.
- [ ] 3.7 A mutation round over § 3.2 – § 3.6, one mutant per arm (drop the
      per-binding call; merge the two codes; report on an undeclared member;
      scope the new arm back to `by_secret`), each mutant's death asserted by a
      named test.

## 4. Realization — the packaged corpus

- [ ] 4.1 `examples/credential-contracts/warning/requirement-ref-unresolved.yaml`
      — a binding whose reference names an id no record carries, with NO shared
      `secret_ref`, schema-VALID and drawing no ERROR (a fixture that is refused
      belongs in `negative/`).
- [ ] 4.2 `examples/credential-contracts/warning/requirement-ref-ambiguous.yaml`
      — resolving against the shipped
      `support/ambiguous-requirement-ids.requirements.yaml`, per OQ-1, with the
      re-use recorded in the fixture header so a later edit to that support
      record cannot silently defang two probes.
- [ ] 4.3 A POSITIVE proving the silent direction — a resolving reference on
      bindings that share no secret — as its own file per OQ-4, so a regression
      in the silent direction names itself.
- [ ] 4.4 All three join the by-name inventory tuples in
      `tests/credential_contracts/test_dispatch_credential_contract.py` IN THE
      SAME COMMIT; `test_the_inventory_is_the_whole_corpus_and_not_a_sample`
      holds them exhaustive against the glob, and the self-test count string is
      derived from those tuples rather than written out.

## 5. Realization — the declared deprecation

- [ ] 5.1 `docs/contract-versioning-policy.md` § Deprecations Currently In Force
      — the act, its two codes, its migration and its removal target
      (contract-v3.0) are declared. **The `add-binding-consumer-identity` entry
      claims to name EVERY act landing at that major**, so it is reconciled in
      the same commit: either it carries the new rows or it names the entry that
      does. An entry asserting completeness that is not complete is a defect of
      the entry.
- [ ] 5.2 `contracts/manifest.yaml`'s `credential-contracts` `consumption_rule`
      repeats "All seven acts … EIGHT warning codes"; it moves with § 5.1. The
      row's `sha256` is the SCHEMA file's digest and does not move, the schema
      not being edited — state that explicitly rather than letting a reader
      infer it from an unchanged hash.
- [ ] 5.3 `docs/credential-access-model.md` — checked for a sentence that
      describes the reference as resolved-only-in-a-pair; edited if one exists,
      and recorded as "checked, none found" if not.

## 6. Realization — the contract cut

- [ ] 6.1 **Allocate the bundle number AT REALIZATION, not here.** Re-read
      `contracts/manifest.yaml:3` at that moment; `contract-v2.5` is the bundle
      at this packet's merge-base and other packets are queued on the same file.
- [ ] 6.2 `contracts/manifest.yaml` — advance `contract_bundle_version`.
- [ ] 6.3 `contracts/CHANGELOG.md` — an entry stating the class and naming the
      act that lands at the major. **The class is DEPRECATING (MINOR)** on the
      policy's own bullet — "a field or shape is marked deprecated; the
      conformance validator emits warnings but still accepts it" — which is
      stricter than the Additive reading the same section would also allow, and
      which OWES the removal version and the migration path in the CHANGELOG
      rather than leaving them optional.
- [ ] 6.4 The release build / digest inventory / tag steps the family's cut
      ritual requires, and `verify-commit --commit HEAD` after committing.

## 7. Verification gates

- [ ] 7.1 `set -o pipefail; python3 -m pytest tests/credential_contracts -q`
      green.
- [ ] 7.2 `set -o pipefail; python3 -m pytest tests/ -q -m "not postgres"`
      green: zero failures, zero errors, and the SKIPPED count EXACTLY the pin
      `.github/workflows/pytest-suite.yml` carries — the pin moving is a finding,
      not a nuisance.
- [ ] 7.3 `python3 scripts/validate-credential-contracts.py <a domain repo>`
      self-test green, reporting the grown counts.
- [ ] 7.4 `OPENSPEC_TELEMETRY=0 openspec validate --all --strict` green.
- [ ] 7.5 Same-clock doc-health against an `origin/main` baseline: zero new
      findings.
- [ ] 7.6 The reproduction re-run on the realized tree now REPORTS, and the
      control (the ONE BYTE that makes the two `secret_ref`s equal —
      `example-secret-b` -> `example-secret-a`) still reports its own
      `shared-secret-identity` error — both pasted into the realization evidence.
      The reproduction's `dispatch_only` record carries TRIGGER-ONLY scopes; give
      it a content scope and `dispatch-scope-ceiling` fires and the tree stops
      being a silent one.

## 8. Archive gate

- [ ] 8.1 Merged to `origin/main` with the required checks green, the merge
      commit named.
- [ ] 8.2 The cut complete: manifest, changelog, digest inventory, verified tag.
- [ ] 8.3 **No archive-order hold applies to this packet** — it carries no
      MODIFIED block over any sibling's addition (§ 1.2). Re-verify that by
      `grep` at archive time rather than trusting this line, the packet having
      been authored before its siblings archived.
- [ ] 8.4 Every § 9 item carries a disposition rather than a blank box.

## 9. Open — deliberately not closed by this change

- [ ] 9.1 **The identity-brokering `requirements_document_ref`**, per OQ-3. The
      packet that introduced that pointer recorded that "no script and no test
      resolves" it. The same class of gap, a different family; a successor issue,
      not a fold-in.
- [ ] 9.2 **The other two conditions of the general SHALL**, per OQ-2 —
      ungrammatical and foreign-repository. Both ARE reported per-binding today
      by `consumer-requirement-ref-grammar`; the finding is that this was checked
      rather than assumed, and the check should be written down where the next
      reader looks.
- [ ] 9.3 **Whether the major should refuse an UNDECLARED `requirement_ref`**
      — i.e. whether the reference becomes required alongside the two
      identifiers. Out of scope: that is a requiredness act on the block, which
      is the sibling's territory and its degraded-mode gate.
- [ ] 9.4 **CROSS-DOCUMENT AMBIGUITY IS NOT RESOLVED BY THE FROZEN RESOLVER.**
      **OPEN AT THE RATIFIED TIP, ROUTED RATHER THAN REPAIRED — the one review
      finding this packet ratifies over.** Raised by Codex on 2026-08-31 23:54
      UTC against `deb72c8e`, the tip that was ratified: *"Resolve ambiguity
      across all indexed requirement documents."* `resolve_requirement` matches
      `[r for r in index.get(doc_ref, []) if r.get("id") == rid]` — scoped to the
      ONE document the reference names — so where the same requirement id sits in
      TWO schema-valid documents, a binding pointing at either resolves `ok`, and
      the per-binding arm § 3.2 buys would stay SILENT on that case.
      **WHAT IT MEASURES AGAINST IS PROMOTED CANON**, not this packet:
      `openspec/specs/credential-contracts/spec.md`'s scenario *"The requirement
      reference resolves to more than one record"* reads *"a named requirement
      reference matches requirement records in MORE THAN ONE DOCUMENT, or more
      than one record in a document"* — promoted when PR #541 archived
      `add-binding-consumer-identity` on 2026-08-31. The shipped resolver already
      fails its first arm.
      **WHY IT IS ROUTED AND NOT REPAIRED HERE.** It falsifies nothing this packet
      ratifies — this delta's ambiguity scenario says *"matching more than one
      requirement record"* and says nothing about document count, so it stays true
      whether or not the lookup is later broadened. It lands on a REALIZATION row
      (§ 3.4), and ratification realizes nothing. And the gap is INHERITED, not
      introduced: this packet neither created it nor closes it.
      **WHAT IS OWED, AND BY WHOM.** Before § 3 may be called complete the
      implementer MUST either BROADEN the resolution lookup across indexed
      documents or EXPLICITLY AMEND that promoted scenario — and MUST NOT do
      neither. Whether the broadening belongs to this change or to a successor is
      itself undecided and is part of what this box carries.
      **THE BENCH HAS NOT SEEN THIS ANSWER.** No review round has read the packet
      since the finding was routed; the four hourly retries after it were all
      provider-refused. Recorded in `review/ratification-2026-09-01.md`
      § "The review evidence" and § "The provider refusal, recorded honestly".
