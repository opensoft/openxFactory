# Private connectivity merge preparation

Status: draft

## Authority and scope

Brett Heap authorized this merge-preparation pass on 2026-11-12 UTC: update the domain
pull request from main, resolve the three verified fixed review threads, add
CI to both bootstrap repositories, rerun validation and record the landing
order. All six pull requests stay draft.

The CI realization is limited to .github/workflows/qualification.yml and its
README description in Headscale-Install and openXsoft-Hosted-Services. It runs
the existing approved owner qualification commands with read-only repository
permissions. The Hosted Services job installs its existing onboarding
requirements. The workflow reports validation evidence; branch protection and
review authority stay under their existing owners.

The domain update includes a compatibility repair to its validation and Sonar
self-checkout selectors. It retains the existing profile and qualified source history.
Original G0-G4 observations and five-role lab acceptance remain historical
records. This preparation records source and CI validation for the landing
candidate; it does not replace measured live pilot evidence.

## Landing order

This is the order for the six lab-candidate pull requests once the user
authorizes leaving draft and all applicable approvals and checks are satisfied.
Use merge commits to preserve the qualified source and evidence history.
The domain repository permits merge commits only.

| Order | Pull request | Dependency reason |
| --- | --- | --- |
| 1 | [Headscale-Install #1](https://github.com/opensoft/Headscale-Install/pull/1) | Package and recovery primitives consumed by Installer, Hosted Services and Ops. |
| 2 | [xFactory-Installer #2](https://github.com/opensoft/xFactory-Installer/pull/2) | Installation selection and lifecycle consumed by hosted onboarding. |
| 3 | [codeXfactory #578](https://github.com/codeXfactory/codeXfactory/pull/578) | Exact profile, schema, protected definition and synthetic workload consumed by the hosted pilot. |
| 4 | [openXsoft-Hosted-Services #1](https://github.com/opensoft/openXsoft-Hosted-Services/pull/1) | Hosted product and onboarding depend on the preceding package, installer and domain sources. |
| 5 | [OpsxFactory #622](https://github.com/opensoft/opsXfactory/pull/622) | Operational recovery composes the package with hosted authority and revocation state. |
| 6 | [openXfactory #1303](https://github.com/opensoft/openXfactory/pull/1303) | Land the coordination evidence and lab acceptance after the owner implementations. |

The shared neutral binding is already an immutable pilot candidate consumed by
the qualified implementations. This order does not allocate or publish a new
contract bundle. Commercial and profile-specific release decisions follow their
own qualification and authority.

Immediately before each authorized landing, refresh the PR head and main,
confirm the expected head and dependency pins, require passing checks for that
head and eligible approvals, and follow the applicable lane protocol before
moving main. If main or a candidate moves, repeat the affected validation.
After each merge, verify the resulting main and preservation of the qualified
commits before proceeding to its consumers. Preserve the historical evidence
references rather than rewriting them to a merge commit.

## Source and validation readback

The domain branch was updated from main with a merge commit. The approved
profile, schema, workload and protected definition remain identical to the
accepted runtime inventory. Both bootstrap updates contain only their
qualification workflow and README description.

All five owner runtime inventories match the accepted G4 packet, and every
listed source member matches its stored digest: 6 Headscale, 9 Installer,
15 Hosted Services, 3 Ops and 4 domain members. Their source pins remain intact.
The neutral binding candidate and historical five-role sign-offs remain
unchanged.

The preparation reran these owner checks:

| Owner | Command or check | Result |
| --- | --- | --- |
| Headscale-Install | Clean checkout and virtual environment; make validate and make test | 26 tests passed |
| xFactory-Installer | make validate and make test | 53 tests passed |
| Hosted Services | Clean checkout and virtual environment with the existing onboarding requirements; make validate and make test | 62 tests passed |
| OpsxFactory | pytest tests/private_connectivity | 25 tests passed |
| Domain | pytest tests/private_connectivity after the main update | 18 tests passed |
| Coordination | Binding, feature evidence, pin reachability and sentinel vocabulary suites | 167 tests and 52 subtests passed |

Both new workflows passed actionlint and use read-only contents permission,
pinned checkout/setup actions, Python 3.12 and the existing owner commands.
They trigger on pull requests, pushes to main and manual dispatch.
All 20 task evidence records passed verification. The owner inventory check
passed, all 310 unique immutable git file references resolved, and the
sequenced-after corpus and unchanged 244-row ledger passed. The pinned
OpenSpec full-corpus run reported zero undispositioned failures and printed
the existing authorized exception. The staged-tree sentinel suite passed
42 tests with its existing standing census.

The domain main update exposed an older canonical reader's case-sensitive
repository disposition matching. GitHub resolves both self-locator spellings
to repository ID 1281785369. A clean-clone probe using the unchanged stack-pinned
reader reproduced four undispositioned failures with the newly cased spelling
and zero with the existing verified spelling. The domain validation and Sonar
self-checkouts retain that compatible locator. The canonical reader,
CLI artifact, contract reference and disposition entries remain unchanged.
A later adoption of a case-aware canonical reader can remove this locator
compatibility requirement.

The two new hosted-runner owner-qualification checks passed:

- [Headscale qualification](https://github.com/opensoft/Headscale-Install/actions/runs/43148879890)
- [Hosted Services qualification](https://github.com/opensoft/openXsoft-Hosted-Services/actions/runs/43148889546)

The three fixed threads were verified against their regression and actual
qualification evidence and resolved:

- [Installer revoked-prior cleanup retry](https://github.com/opensoft/xFactory-Installer/pull/2#discussion_r4544202155): test_detach_retry_keeps_a_revoked_prior_out_of_pending_subjects.
- [Hosted interrupted tombstone cleanup](https://github.com/opensoft/openXsoft-Hosted-Services/pull/1#discussion_r4544193594): test_supervisor_recovers_tombstones_committed_before_pending_state and the recorded actual thread qualification.
- [Ops isolated recovering shadow authority](https://github.com/opensoft/opsXfactory/pull/622#discussion_r4544198389): test_shadow_qualification_copies_authority_without_changing_live_state and the recorded actual shadow qualification.

Original drill timings and live observations are retained at their measured
revisions. This preparation ran source/fixture checks and CI; it does not claim
a new full live drill or extend expired lab authority.

## Completion boundary

All six PRs remain draft. Current-head checks, main freshness, unresolved
threads and review decisions are read from GitHub at completion and must be
read again at landing. The new bootstrap CI reports evidence; it does not
change the required-check rulesets. Required human/code-owner approvals and
the instruction to leave draft are still outstanding. A GitHub Codex review
request is made after each meaningful push; quota refusals do not constitute
a fresh remote review.

## Subsequent landing authorization

Brett Heap subsequently authorized marking all six PRs ready for review,
requesting their required approvals and landing them in the recorded order
after checks and approvals pass. He then explicitly authorized a one-time
admin merge of codeXfactory #578 at head e6676356 after its required checks
pass. That exception is limited to #578; the other required approvals remain
in force, and Headscale-Install and Installer still land first.

During the landing recheck, main had advanced through the governed repository
casing maintenance in PR #1306. This branch adopted that canonical reader and
its canonical regression module byte for byte. Only the approved spelling
pairs receive compatibility; the earlier private-branch generic GitHub case
normalization is superseded by the upstream governed implementation.
The private-connectivity runtime inventories remain at their accepted bytes.

The draft boundary and validation counts in the preparation snapshot above
describe that historical snapshot. Current readiness, source head, checks,
review requests and merge results are recorded on the six PRs and must be
read again immediately before each landing.
