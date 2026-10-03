# NotebookLM hardening recovery realization evidence

Status: record
Recorded: 2026-10-03

## Identities and scope

The unpublished historical snapshot is
`702a93a4490cadf733d84c4ee88507943c6b6b6e` on
`fix/notebook-source-readiness-race`. Recovery starts from current main
`cc775fea08dab6ba64c27bb7aa3bb71ed607649b` on
`036-recover-notebooklm-hardening`; it does not replay the stale branch wholesale.
The old ref and worktree remain until the reviewed replacement lands.

Current main's settled rename/adoption, title disambiguation, hosting resolution,
root-product scope and workspace-record replacement are preserved. The old
package's provider/model/test boundaries are recovered and ported to current
pinned openDox/openXdox imports. There is no contract release or gitlink change.

## Deterministic local verification

Commands run in py-bench from the feature checkout with initialized pinned
openDox and openXdox legs. No live provider is used.

| Check | Result |
| --- | --- |
| Materialized-main NotebookLM baseline | 108 passed, 2 module skips, 30 subtests |
| Recovery pytest NotebookLM suite | 265 passed, 0 skipped, 42 subtests |
| Guarded unittest discovery | 265 tests, OK |
| Scoped Ruff 0.16.10 | zero findings |
| Scoped basedpyright 1.40.1, warnings fatal | zero errors and warnings |
| Original programming checker | zero violations across 89 files |
| Package dependency graph | 34 modules, zero cycles |
| Isolated Ruff unused-import probe | exit 1, F401 |
| Isolated programming-checker raw-dict probe | exit 1, raw-dict-return |
| Type-warning regression | reportUnusedCallResult makes the command fail |
| Explicit missing checker regression | refuses before any quality tool runs |
| Public CLI probes | help, hermetic dry run, malformed manifest and invalid target pass |
| Affected OpenSpec strict validation | pass |
| NotebookLM plus domain-profile regressions | 355 passed, 42 subtests |
| Doc-health and review-lane regressions | 2219 passed, 2 missing-core skips, 54 subtests |
| Hosting declaration validator | zero errors |
| Affected doc-health comparison | no introduced findings |
| Corrected NotebookLM/domain/boundary/manifest-name/release regressions | 363 passed, 42 subtests |
| Retained carve-path and test-floor regressions | 4 passed |
| Code-surface, target-release and sequenced-after declaration validators | pass |

The two main module skips were stale pre-shed names, rather than unavailable
features. Both now run. The pytest workflow moves `EXPECT_SKIPPED` from 6 to 4
with that reason; its other stand-downs and required named-verdict checks remain.
It supplies pinned uv tooling for the real type-checker failure regression.

The public hyphenated executable is a relative symlink to the canonical Python
module. The quality gate resolves the alias, checks the same implementation and
uses no naming/type suppression, baseline or rule exemption. Guarded unittest
adds the repository namespace root and registers the host as pytest already does.

## Checker provenance

The previously installed programming checker was absent. Its original bytes
were recovered from the local oh-my-opencode Git object store, blob
`4270ef321d4303ce90ed5afefe2460944458e9b6`, available in history at
`0913f1322b4c48052a78899bc85ae35179d6f6c5`.
The blob identity was independently checked with `git hash-object` before use.
Supply those unchanged bytes through `PROGRAMMING_CHECKER`; a missing checker
fails closed. Neither a replacement always-green checker nor a size opt-out is used.

## Publication and disposition are pending

Repository-wide strict validation: 111 passed, one unchanged baseline failure.
`add-chain-attestation` omits the canon's scenario “a tranche-two link does not
exist yet” from its modified hash-linked-chain requirement. The recovery does
not change that attestation decision. Constitution V requires the all-strict
gate before pushing; a baseline-exception decision was requested from Brett.

The initial full non-Postgres run at `49ce82dbf65abd60dc4c5e8931ade6faaa08037f`
reported 9070 passed, 16 failed, 2 skipped, 338 deselected and 426 subtests.
It exposed missing retained carve paths/counts, the neutral boundary import,
literal module lookups and target-release vocabulary. These recovery defects
are corrected and their focused checks pass. Four sequenced-after ledger cases
require the real moving PR identity; that ledger update remains a publication
step rather than an invented local PR number. The four schema-location cases
also fail on unchanged main with the same initialized pins under the same
directory ancestry: they find a validator in the older shared checkout, whose
openXdox spec leg is absent. A disposable main checkout away from that sibling
skips those four cases. No shared-checkout pin or peer-owned working file is
changed to conceal this environmental difference.
The full suite is not represented as green.

Exact-head PR review, required CI and landing remain pending. This file is local realization
evidence, not a claim of PR approval, landing, canon promotion or old-ref deletion.
The accepted backup/recovery inventory remains outside the repository under the
operator's local-state repo-cleanup directory. Exact old-tip restoration will be
verified independently before deleting the remaining old branch/worktree.

The verified code is commit `046a14c1e63e8cec04096972dcf027a8bf7db941`.
The prepared governance packet is a separate local commit so the first review
head can obtain a real PR identity before its ledger row is stamped. No push is
authorized merely by this sequencing; the recorded baseline decision remains
pending. Final review applies to the combined head after the ledger update.


## Discovery and adjacent baseline comparison

All 248 unique test names present on current main are retained. The recovered
suite has 262 unique scenario names across 265 collected methods. One historical
name, `test_the_committed_record_conforms`, became the current shipped-example
conformance test; its original live-record assumption is obsolete under configured
hosting identity. Collection is larger because formerly skipped modules now run.

Against materialized main, proposal-origin has the same one legacy warning and
ratified-provenance has the same 27 existing findings. Status-validity has no
recovery finding. None is silently rewritten or presented as a clean whole-repo
report. The affected recovery packet has no introduced finding in those families.
The old main test inventory and local checker outputs are preserved externally.

## Retained carve and discovery compatibility

The carve manifest retains `tests/notebooklm/test_sync_notebooklm_books.py` and
its 137-method floor. Keep that entry point as explicit typed forwarders to
scenario bodies in focused, non-collectable support modules. Each scenario keeps
its setup and cleanup and is discovered once; guarded unittest still runs 265
tests. The support classes are extensible case bases, and their scenario methods
do not override collected tests or use warning suppressions.

The public wrapper retains literal loader calls for the three pinned dashboard
modules through typed callbacks. This preserves both patchability and the carve
retirement audit. The neutral output boundary remains the sweep fixture's source;
a checked save protocol handles the pinned module's static class identity.
