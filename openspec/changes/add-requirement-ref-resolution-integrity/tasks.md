# Tasks: add-requirement-ref-resolution-integrity

Governance-level and dependency-ordered. **This change is a DRAFT and is NOT
being implemented now.** § 1 is authored in this pull request; **§ 2 — Brett
Heap's ratification act — IS THE NEXT ACT AND IS OPEN**; § 3 onward are for the
implementer and belong to a separate realization pull request, on the pattern
this packet's own subject set established (proposal PR #497, realization PR
#516).

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
      of them these) and are ADDED by the ACTIVE, ratified, unarchived
      `add-binding-consumer-identity`. A MODIFIED block over either is exactly
      the shape `govern-sibling-added-modified-deltas` governs: a
      ``**Modified over `<basis>`'s addition by <change-id> (<date>):**`` marker
      plus an ARCHIVE-ORDER HOLD behind the sibling. A pure ADDED requirement
      serves, so this packet takes it, carries no marker and imposes no hold.
      Recorded in proposal.md § The sibling rule, measured.
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

## 2. Ratification — THE NEXT ACT, OPEN

- [ ] 2.1 **Brett Heap reads the packet and rules.** Ratification authorizes
      REALIZATION and performs none of it. Until it happens this packet stays
      `Status: draft` and nothing in § 3 onward may start.
- [ ] 2.2 Each of AD-1 … AD-6 carries a disposition (accept / veto / amend) and
      each of OQ-1 … OQ-4 a ruling or an explicit defer. **AD-1 is the one that
      changes the spec text**: one code or two. It is RULABLE IN ONE SENTENCE
      because the one-code branch is enumerated as a twelve-item AMENDMENT SET in
      AD-1 itself — which delta paragraph, which two scenarios, which
      `code_surface` sentences, which task rows and which README clause — so
      "one code" is executed mechanically in the ratifying commit rather than
      leaving a delta that requires two codes standing beside a ruling that
      permits one.
- [ ] 2.3 Whether a §7.4-shaped council sitting is convened for this packet at
      all is BRETT'S CALL and is not assumed here. The packet is small, its
      subject is a ruled successor rather than a new doctrine, and the
      `govern-sibling-added-modified-deltas` precedent — ratified by direct
      ruling with the sitting it prescribed for itself DECLINED — is the nearer
      one. If a sitting is convened, its record lands in `review/`; a `review/`
      directory is NOT created before then, an empty one asserting a sitting
      that did not happen.
- [ ] 2.4 On ratification: `Status: ratified` + `Ratified by:` on proposal.md,
      the README entry updated in the same commit, and the ratification record
      written to `review/ratification-<date>.md`.

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
