# roles-authority-model

## MODIFIED Requirements

### Requirement: An enrolled autonomous lane carries a one-edit kill switch

The model SHALL ensure that every enrolled candidate class can be returned to the human merge gate by A SINGLE REVIEWED EDIT TO THE ENROLMENT DECLARATION TOGETHER WITH ITS DECLARED TEST COMPANION — the set of conformance assertions that pin that enrolment, named beside the declaration in the reviewed declaration itself, so that the withdrawing pull request is landable against the repository's required checks — and that the withdrawal takes effect on the next evaluation, without redeploying, reconfiguring or otherwise touching any lane.

The declaration SHALL remain the switch. The enrolment SHALL be held in a reviewed, diff-visible declaration read from the base branch, and the model SHALL NOT accept a kill switch held in a value that does not appear in a reviewable diff: not a repository or organization variable, not a secret, not an environment setting, not a platform toggle, and not any store whose change leaves no reviewable record. A withdrawal SHALL therefore be visible in the declaration's history forever, and SHALL be a code-owner-reviewed act by construction.

The companion SHALL be declared, and the declaration SHALL be kept honest by a test. Where a class is enrolled, the assertions that pin that enrolment — every conformance assertion that fails when the class is withdrawn, INCLUDING any golden or snapshot artefact whose recorded value moves with the withdrawal — SHALL be named beside the enrolment in the same reviewed declaration; and a conformance test SHALL assert that the declared companion ASSERTIONS equal the set that actually pin the enrolment, and that every declared artefact exists, so that a stale declaration is a failing check rather than a discovery made at the moment the switch is thrown.

The model SHALL NOT accept an enrolment whose withdrawal, WITH THE DECLARED COMPANION APPLIED AND NOTHING ELSE, is not landable against the repository's required checks. An enrolment that cannot be withdrawn by a landable pull request is not enrolled under a kill switch, however the declaration describes itself.

WHAT THIS REQUIREMENT DOES NOT DO IS LOOSEN THE PINNING, and that is the point of stating the companion rather than removing the assertions. The conformance assertions that pin an enrolment SHALL keep the property that the enrolment's departure is NOTICED: the model SHALL NOT accept, as a means of satisfying this requirement, a suite that derives the enrolled set from the enrolment declaration itself and therefore passes unchanged whether the class is present or absent. The companion is a DECLARATION of what must move, never a licence for nothing to move.

**Modified over `extend-merge-master-envelope-to-floor-bot-lanes`'s addition by amend-kill-switch-to-declared-test-companion (2026-09-11):** — the requirement this block restates is not in canon. It is ADDED by the ACTIVE change `extend-merge-master-envelope-to-floor-bot-lanes`, which is ratified (2026-09-07, PR #746) but not yet archived, so the basis is a sibling's addition rather than a promoted specification, and the target text is that change's own delta at `specs/roles-authority-model/spec.md` lines 53–65. The pairing is declared here per requirement, as `govern-sibling-added-modified-deltas` requires, and the archive order follows from it: this packet SHALL NOT archive until that change promotes, which the `sequenced_after` front matter and `.openspec.yaml`'s `related` entry already record. THE AMENDMENT IS TO DECISION N-4's ACCOUNT OF THE ACT'S SHAPE — measured 2026-09-11 as one edit plus 29 required-check assertion failures across five test files, plus a sixth file (the golden digest) that moves with them — AND TO NOTHING ELSE N-4 decided: the switch is still the candidate entry, a boolean `active:` member is still refused as a schema change that would let a disabled entry read as enrolled, and a repository variable is still refused as invisible in the diff.

#### Scenario: Withdrawing an enrolment
- **WHEN** the owner removes a candidate class from the enrolment declaration AND applies exactly the companion declared beside that class, and nothing else
- **THEN** the repository's required checks pass on that pull request and the removal lands
- **AND** the next evaluation of a pull request of that class reaches no envelope decision at all — it is not a candidate, the evaluation exits as not-a-candidate, no approval is offered and no sticky comment is posted
- **AND** that pull request stays at the human merge gate, exactly as it would had the class never been enrolled
- **AND** the withdrawal is visible in the enrolment declaration's history forever

#### Scenario: A kill switch outside the diff
- **WHEN** an enrolment is proposed whose disabling is a repository variable, a secret, an environment setting or any other value that does not appear in a reviewable diff
- **THEN** the enrolment is refused
- **AND** the refusal names the reviewability of the switch as the ground

#### Scenario: The companion is declared beside the declaration
- **WHEN** a candidate class is enrolled
- **THEN** the conformance assertions that pin that enrolment are named beside it in the same reviewed declaration, including any golden or snapshot artefact whose recorded value moves on withdrawal
- **AND** a conformance test asserts that the declared companion ASSERTIONS equal the set that actually pin the enrolment, and that every declared artefact exists
- **AND** a declaration that has gone stale is a failing check rather than a discovery made when the switch is thrown

#### Scenario: An undeclared companion is a finding against the enrolment
- **WHEN** a withdrawal is proposed with the declared companion applied and nothing else, and a required check goes red through an assertion that the companion does not name
- **THEN** the enrolment is non-conformant with this requirement
- **AND** the finding is recorded against the enrolment and its declaration, never against the suite that caught it
- **AND** the remedy is to complete the declaration, never to relax the assertion that noticed
