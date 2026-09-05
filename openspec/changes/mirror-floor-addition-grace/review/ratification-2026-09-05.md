# Proposal Ratification: mirror-floor-addition-grace

Status: ratified

Decision date: 2026-09-05

Ratifier: Brett Heap (openxFactory repository owner) — in session, recorded on
PR #676 (comment beginning "RULING — Brett Heap",
`https://github.com/opensoft/openxFactory/pull/676#issuecomment-5552450473`)
and on issue #675 (comment beginning "RATIFIED — Brett Heap",
`https://github.com/opensoft/openxFactory/issues/675#issuecomment-5552450611`).

Ratified verbatim: **"ratify the companion when green, then realize it"** — a
standing word given while this packet was being authored, applied at the FIRST
head where the condition held. The ruling comment records the application
time as 2026-09-05T14:24:10Z, over head `ce9a81ed`.

Ratified baseline: this change as committed in the ratification commit
carrying this record — `proposal.md`, `design.md`, `tasks.md`,
`.openspec.yaml`, this record, and the spec delta
`specs/review-lane-floor-mirror/spec.md` carrying SEVEN `## ADDED
Requirements` and 28 scenarios (measured by grep against the delta at this
commit: `grep -c '^### Requirement:'` → 7, `grep -c '^#### Scenario:'` → 28),
with no `## MODIFIED Requirements` block and no `## REMOVED Requirements`
block anywhere in the delta — the file carries exactly one `## ADDED
Requirements` heading.

**NOTHING IN THE PACKET'S SPEC DELTA CHANGES BETWEEN THE TIP THE RULING WAS
GIVEN OVER (`ce9a81ed`) AND THIS COMMIT**, and that is stated first rather
than left to a diff. Verified mechanically rather than asserted: `git diff
ce9a81ed -- openspec/changes/mirror-floor-addition-grace/specs/
openspec/changes/mirror-floor-addition-grace/design.md
openspec/changes/mirror-floor-addition-grace/tasks.md
openspec/changes/mirror-floor-addition-grace/.openspec.yaml` is EMPTY at this
commit — no requirement, no scenario, no design line and no task line moves
in the ratifying commit. Only `proposal.md`, `README.md` and this new record
change.

Checks at `ce9a81ed`, the head the ruling was given over — all TEN green:
`pytest-suite` run `33970371971`; `merge-master-approval` run `33970371308`;
`lane-line` run `33970371973`; `openspec-cli-pin` run `33970371982`;
`openreposhape-pin` run `33970371959`; `wallet-validation` run `33970371986`;
`signed-execution-chain-gate` run `33970371987`; `clearing-dispatch-gate` run
`33970371977`; `release-tag-gate` run `33970371960`; and the
`copilot-pull-request-reviewer` check run (check-run id `101317698310`),
which is the same head's Copilot review producing the 🟢 verdict quoted
below. `OPENSPEC_TELEMETRY=0 openspec validate mirror-floor-addition-grace
--strict` is VALID and `--all --strict` reports **92 passed / 0 failed** at
this commit (measured after the ratifying commit; the spec delta itself is
unchanged from `ce9a81ed`, so this is the same result the ruled head would
report). `python3 scripts/proposal-support.py . verify` reports "proposal
support verification ok". `python3 -m pytest tests/sequenced_after
tests/review_lane_pin -q` reports **217 passed, 1 skipped, 18 subtests
passed**. `python3 scripts/validate-sequenced-after.py . --ledger-diff`
reports "per-change sweep ledger consistent with the corpus (170 rows)" —
this change is one of the four active changes declaring `sequenced_after:`,
and the ledger needed no seeding for this commit.

Bot state at the ruling: **three Copilot review threads, all resolved.** Two
were fixed together in commit `23de2283` — a real defect in the pin-window
`git log` invocation on `proposal.md` § What Changes and `tasks.md` § 2.2 (as
written, missing `--name-only`/`--pretty=format:`, the command would emit
commit headers rather than a path list); the fix copied the pinned core's own
`specs_floor_block.paths_added_after_pin` invocation argument for argument,
and corrected a third site Copilot had not flagged, `design.md` § 3, which
carried half the same fault (`--name-only` present, `--pretty=format:`
absent). The third thread — a request to spell the lane token
`openxfactory-2` instead of `openXfactory-2` in `proposal.md`'s `Authored:`
line — was **refused, with a measurement**: both spellings are deliberate,
the lowercase token is the greppable one and is present on every
machine-read surface (every commit trailer, the PR body, every comment's
first line, and the `lane-line` check itself, which passed on exactly that
string), while `openXfactory-2` is the lane's owner-set NAME, which the
provenance line records. Copilot's final verdict on the ratified head
`ce9a81ed`, 2026-09-05T13:59:44Z — 🟢 *Approval recommended*, 0 new comments,
7/7 files reviewed, Lite effort: *"The changes are confined to OpenSpec
authoring/docs plus the derived sequencing ledger/index updates, with no
realization code paths or CI-critical workflows/tests modified."* Codex was
quota-refused twice on this PR (`chatgpt-codex-connector`, 2026-09-05T13:33:05Z
and 2026-09-05T14:22:20Z, both verbatim *"You have reached your Codex usage
limits for code reviews... "* / *"...usage limits..."*) — **no Codex verdict
exists on this packet**, disclosed rather than read as a clean bill. Sourcery
is an upsell stub on this repository and reviewed nothing (*"Your private
repo does not have access to Sourcery"*, posted twice).

## Decision

**RATIFY, BY DIRECT RULING OF THE REPOSITORY OWNER**, the SEVEN `## ADDED
Requirements` and 28 scenarios this change adds to the NEW capability
`review-lane-floor-mirror` — **as written**, unamended.

**Because the word preceded the authoring's completion, AUTHORING DECISIONS
A–F STAND AS RECOMMENDED and none is separately ruled.** The owner may veto
any of them by follow-up; this record does not elevate any one of them above
the others, and none was singled out the way codexFactory's companion
ratification singled out B1.

| | Decision | Alternative it beat | Disposition |
|---|---|---|---|
| **A** | The required assertion RE-IMPLEMENTS the rule and REPLAYS the pinned core's 16 exported vectors plus 5 refused ones; the advisory lane IMPORTS `evaluate_floor_completeness` directly. | Have the required assertion import the core too. | **STANDS AS RECOMMENDED** — the pinned core checkout carries `continue-on-error: true` in `pytest-suite.yml` by design, so an importing blocking assertion could only skip (a CSC-F16 silent-false-green) or fail for a cause no candidate can fix; the mirror stays local so an outage never wedges the repository. |
| **B** | A NEW capability, `review-lane-floor-mirror`, rather than an existing one. | File under `neutral-product-pin` or `release-surface-integrity`. | **STANDS AS RECOMMENDED** — `contracts/review-lane-pin.yaml` is deliberately `kind: pinned_workflow`, not `pinned_contract_manifest`, on its own stated ground; nothing here touches a bundle, inventory or cut. |
| **C** | The advisory lane's base checkout moves to `fetch-depth: 0`. | A targeted fetch deepened only to the declared `generated_at`. | **STANDS AS RECOMMENDED** — measured cost 2,025 commits / 29.6 MiB on this branch; the targeted alternative is strictly more fragile (a depth sufficient last week can silently fail-safe this week). |
| **D** | `sequenced_after: [codexFactory:add-floor-addition-grace]` — the corpus's first CROSS-REPOSITORY declaration. | State the dependency in prose plus `.openspec.yaml` `related:` only. | **STANDS AS RECOMMENDED** — `scripts/sequenced_after.py` checks a qualified foreign entry for well-formedness only and the consumer's disposition refuses it under a named identifier; the ledger sweep above confirms it resolves and the corpus stays consistent. |
| **E** | The two negative controls MOVE onto the graced expression rather than being deleted or exempted. | Delete or exempt the controls under the grace. | **STANDS AS RECOMMENDED** — both controls call the module's shared `uncovered()` and fail by construction whenever the coverage assertion fails; a control that never runs proves nothing. |
| **F** | This packet performs NO regeneration and proposes NO D-3 tolerance value. | Propose a tolerance number or perform the first regeneration here. | **STANDS AS RECOMMENDED** — both are later, separately claimed acts; the D-3 number is codexFactory's own CODEOWNERS-routed value (shipped as `3`, put for veto there), and this repository reads the field through the core rather than declaring one of its own. |

**Ratification authorizes promotion of the spec delta and performs no
realization.** No code lands by this act.

## What ratification does NOT authorize

1. **No code lands here.** Not one line of `.github/workflows/pytest-suite.yml`,
   not one line of `.github/workflows/merge-master-approval.yml`, not one test.
   The realization is the NEXT act, claimed on the same word.
2. **The pin advance is not performed.** `contracts/review-lane-pin.yaml` and
   the other four pin sites are untouched by this commit; requirement 6's
   five-site lockstep advance past codexFactory `712fc8ca` is realization work.
3. **No floor regeneration is performed.** The obligation that ONE
   regeneration happen after the grace is in force, at a landed openxFactory
   commit, is stated in the packet and discharged by nobody here.
4. **The D-3 tolerance number is not proposed, endorsed or set here.** It
   lives in codexFactory's own CODEOWNERS-routed floor document (shipped as
   `3`, put for veto there); this repository reads the field through the
   pinned core and declares no value of its own.
5. **This record does not merge PR #676.** Merge is the orchestrator's act,
   on the owner's word, and this packet's own `Status: ratified` front matter
   plus `target_release`'s stated evidence (five pin sites advanced in
   lockstep, the assertion and its two negative controls moved with the
   vector replay green, `merge-master-approval` reporting
   `pending_floor_extension` distinct from `floor_incomplete`, one landed
   regeneration, and one observed `pending_floor_extension` outcome quoted in
   the archive record) govern when this change may archive — none of that
   evidence exists yet.
6. **The ratified `add-floor-addition-grace` capability (codexFactory,
   `repository-gate-floor`) is not reopened, extended or re-argued.** This
   record ratifies only the openxFactory-side mirror; the core rule's home
   stays codexFactory's, per this packet's own § "What this deliberately does
   not do".
