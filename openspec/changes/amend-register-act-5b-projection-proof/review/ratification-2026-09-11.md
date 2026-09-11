# Proposal Ratification: amend-register-act-5b-projection-proof

Status: ratified
Kind: report
Decision date: 2026-09-11
Ratifier: Brett Heap (openxFactory operator authority)
Ratified: 2026-09-11T13:09:12Z by Brett Heap (openxFactory operator
authority), verbatim: *"accept all A on 960"* — given as a MULTIPLE-CHOICE
ruling over all seven decisions `proposal.md` § Open questions and
`design.md` D-1 through D-7 put for the owner, recorded as a comment on
openxFactory PR
[#960](https://github.com/opensoft/openxFactory/pull/960) and in full here.
**THE WORD TAKES THE RECOMMENDATION ON EVERY ONE OF THE SEVEN: OQ-1 = A,
OQ-2 = A, OQ-3 = A, OQ-4 = A, OQ-5 = A, OQ-6 = A, OQ-7 = A.** Each is the
option the packet already encoded, so **THE DELTA'S WORDING STANDS
UNCHANGED AND NOTHING WAS SUBSTITUTED, RESTORED OR DELETED.**

## 1. The word, and what it reaches

**"accept all A on 960" IS A SINGLE MULTIPLE-CHOICE RULING OVER SEVEN
DECISIONS, NOT SEVEN SEPARATE WORDS.** It was given at 2026-09-11T13:09:12Z
and is recorded verbatim, with that instant, on every document this
ratification touches — `proposal.md`, `design.md`, `tasks.md`,
`.openspec.yaml` (`approved_by`/`approved_on`, added beside the unmoved
`proposed_by`/`proposed_on` pair the `add-drafted-proposal-origin` (issue
#318) shape defined), and this record.

**THE RATIFICATION IS APPLIED BY LEAVING THE TEXT ALONE, AND THAT IS
VERIFIED BY DIFF RATHER THAN ASSERTED.** `git diff --stat -- openspec/changes/amend-register-act-5b-projection-proof/specs/`
between the pre-ratification head (`69a57fa2`) and the ratification commit
is **empty (0 files)** — the four `## ADDED` requirements and their twelve
scenarios are ratified exactly as the packet was authored and as PR #960's
ten checks ran green against.

## 2. The seven decisions, as put and as ruled

| OQ | `design.md` | Put | Ruled | Considered, not adopted |
| --- | --- | --- | --- | --- |
| **OQ-1** | D-1 | What step 5b's exit condition becomes | **A — a DIRECT OBSERVATION** of the published register projection's declared source revision, at or after the register act's landed commit | B, a reachable gate-side check (named as the successor; does not exist today — nothing in the repository can see cluster state); C, remove the exit condition and keep the projection as record evidence only; D, keep *"verify one convening admits"*, deferred until legs 3/4 exist |
| **OQ-2** | D-2 | How much the observation must read | **A — the declared source revision alone**, with the three row-level fields (`grant_ref`, `expires_at`, `staleness_bound`) named as OWED with an owner | B, mandate the row-level confirmations too, which would need an explicit sentence preserving the 2026-09-11 precedent; C, either, at the observer's discretion |
| **OQ-3** | D-3 | Where the concrete field name lives | **A — the requirement stays neutral**; the runbook names ConfigMap `hermes-register-projection`, annotation `hermes.opensoft.one/source-revision` | B, name the concrete annotation in the requirement too; C, neutral everywhere, leaving the walker to guess the field |
| **OQ-4** | D-4 | Whether the refresher cycle is a stated precondition | **A — stated as an EVENT**: a refresh cycle that COMPLETED after the act landed, evidenced by the refresher's own success record; §5.2 step 2's stale *"nothing refreshes the projection automatically"* corrected in the same edit | B, state it as a CLOCK (name the `0 */2 * * *` cadence, a deploy detail hermes-install owns); C, say nothing about timing, re-opening the exact 2026-09-11T02:5xZ failure |
| **OQ-5** | D-5 | Who may perform the observation | **A — a named human operator's word that NAMES the executing lane**; read-only verbs only; recorded with commands and values | B, any lane under a standing ceremony word given once; C, the operator personally, no lane |
| **OQ-6** | D-6 | Delta class and archive ordering | **A — `## ADDED`** on `review-authority-intake`; archive does NOT proceed before `add-wallet-carried-review-authority`, per `sequenced_after:` and `tasks.md` § 5 | B, `## ADDED` and archive whenever ready, risking a promoted file that misrepresents the capability until its parents land; C, hold the whole packet until a parent archives, then re-cut as `## MODIFIED` |
| **OQ-7** | D-7 | Home capability | **A — openxFactory `review-authority-intake`** | B, openxFactory `roles-authority-model` (owns the consequence, not the subject); C, codexFactory `domain-hermes-content` (a domain repository authoring a neutral contract, against working rule 1) |

**EVERY RULING IS THE RECOMMENDED OPTION.** No requirement text was
rewritten, no delta directory was renamed, and no `sequenced_after:` entry
moved.

## 3. What this word admits, and what it does not

**ADMITTED.** The four `## ADDED` requirements on `review-authority-intake`
exactly as authored and reviewed on PR #960 at head `69a57fa2`: the exit
condition as a direct observation of the published projection's declared
source revision (OQ-1/OQ-3); the observation as a read-only, named-operator,
named-lane act recorded with its values (OQ-5); the refresh-cycle
precondition stated as an event, with the runbook's stale sentence corrected
(OQ-4); and the stated-limit requirement naming the three row-level fields
as owed (OQ-2). The delta class is `## ADDED` and the archive ordering is
held behind the two parents (OQ-6).

**NOT ADMITTED, AND NOT BY THIS WORD.**

- **Nothing reaches `openspec/specs/`.** This ratification edits no promoted
  file. `review-authority-intake` has no promoted specification today
  (`add-wallet-carried-review-authority` and `register-gate-rules-council-seats`
  are both still ACTIVE), and this packet's own `tasks.md` § 5 holds its
  archive behind the first of those two, per OQ-6.
- **The two runbook sentences (three if OQ-4 = A, which it is) are not
  written.** `docs/governed-reissuance-runbook.md` keeps `Status: draft` and
  is realized at `tasks.md` § 3, a separate act after this one.
- **The walk record is not amended.**
  `openspec/changes/register-gate-rules-council-seats/walk-2026-09-11-register-act.md`
  is `Status: record`; this change is cited back into it as a dated append at
  `tasks.md` § 4, not performed here.
- **codexFactory is not touched.**
  `clarify-gate-rules-decline-position` § D4 step 5b keeps its ratified text
  and 2026-09-11 pointer annotation.
- **The gate-side check named under OQ-1 option B is not proposed.** No
  owner is assigned and no issue is filed by this ratification.

## 4. What is owed after this word

- **§ 2 (encode) is a no-op**, recorded rather than performed: every OQ was
  ruled at its recommendation, so the encoded wording IS the ratified
  wording (`tasks.md` task 2.1's own escape clause).
- **§ 3 (realize)** — the runbook sentences — is separate work, not part of
  this ratification.
- **§ 4 (cite back)** — the dated append into the walk record's disposition
  section — follows realization.
- **§ 5 (archive)** stays entirely open, held behind
  `add-wallet-carried-review-authority`, per OQ-6 and this packet's own
  `sequenced_after:` declaration.
- **The Rule 1 claim and Rule 6 landing window** are owed at landing (taking
  the pull request out of draft and merging it), not at this ratification —
  `tasks.md` task 6.5.

## 5. Provenance of this record

Written in the ratification commit itself, in the worktree
`~/projects/xFactory/openxFactory-worktrees/amend-5b`, by lane
`hermes-wallet-exercise`. It carries `Status: ratified` because
`document-lifecycle`'s *A review record records a ratification* governs a
`review/ratification-*` file. Its sibling `review/verification-2026-09-11.md`
keeps `Status: record`: that file's subject is the GATE RUN. Every path in
this file is repo-relative.
