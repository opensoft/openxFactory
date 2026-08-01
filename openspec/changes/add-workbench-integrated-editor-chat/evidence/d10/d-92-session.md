# Step D — Real branch session end to end (`add-workbench-branch-sessions` 9.2)

Status: record · 2026-07-31 → 2026-08-01 session (times UTC-4 unless noted)

## The session

| Item | Value |
|---|---|
| Session branch | `draft/consent-instrument-contract`, auto-opened by the Step B create (branch-sessions integration) |
| Session worktree | `openxFactory-worktrees/d10-corpus-worktrees/sessions/draft__consent-instrument-contract`, created beside the served checkout |
| Create gate action | `b280542` — `consent-instrument-design-decisions.md` + its gate-action record (shared evidence with Step B: one real action satisfying both clauses' create elements, recorded transparently) |
| Edit gate action 1 | `8599f60` — packet doc `consent-instrument-contract.md`: nine `RESOLVED (Brett, 2026-07-31)` rulings + header fix (Topics single-line, inside the 15-line scan window) |
| Edit gate action 2 | `9674dc8` — decisions doc filled with the ranked nine-rulings record; template `TODO` replaced by the real possible feat (`add-consent-instrument`) |
| Gate effect on readiness | Topic went 0.458 / 2 blockers → **ready / 0 blockers / both docs 0.925** in the session snapshot — an HONEST gate pass earned by resolving the questions, not by moving the bar |
| Panels follow the worktree | TRUE — after selector rekey to `openxFactory @ draft/consent-instrument-contract`, the docs strip showed both session docs; the session snapshot regenerated at each gate action (`b280542` → `8599f60` → `9674dc8` entries observed in `/snapshot-index.json`) |
| Wheel shows no draft | TRUE, two planes — local `openxFactory @ main` view showed only the packet doc throughout; the HOSTED selector carries no session refs at all (non-main refused by design, observed live) |
| Session notebook | NOT EXERCISED, two recorded causes: F8 (`nlm … --json` CLI drift broke auto-creation at session open) and the remedy script's session-worktree discovery not covering the dedicated `d10-corpus` serve layout (environmental, a D10-setup consequence). Sign-off matrix carries this as not-exercised-with-cause |
| Pull request | opensoft/openxFactory#47 — title `Session draft/consent-instrument-contract: consent-instrument-contract`; body carried the D18 merge-commit-never-squash notice verbatim |
| Merge | MERGE COMMIT `52153ce` (admin merge under Brett's live "merge it"); all three gate-action commits preserved individually on main |
| Docs on main (separate read path) | `git fetch` + `ls-tree origin/main` in the EVIDENCE worktree (never the served checkout): both documents present under `52153ce` |
| Next published snapshot | Aggregation pointer-sync `fac1af5` → lane run `30677000612` → rolling PR opensoft/xFactory#68 merged `a4d7b68`: published `openxFactory-snapshot.json` at source `52153cedb09e` lists BOTH merged documents |
| Session teardown | Merge-ending observation was ENVIRONMENTALLY BLOCKED: the engine's fail-closed base check resolves the shared `refs/heads/main` (held at `c782d6d` by another live session's dirty primary checkout; advancing it would sweep their work). The engine's refusal (twice, deterministic, with remedy text) is preserved in the transcript. Resolution per the propose refusal's own guidance: `abandon-session` with a durable reason naming the merge — engine report: `torn_down: [worktree, registry-entry]`, `branch_retained: true`, record `ideation/dashboard/gate-records/draft-consent-instrument-contract/abandon-session-20260801T012037Z.gate-action.yaml`; branch deletable via `cleanup-abandoned-branch` once the proposal exists (it now does) |

## Fingerprints (served checkout: branch + HEAD + porcelain)

| # | When | Result |
|---|---|---|
| 1 | before session work | `d10/corpus-baseline` @ `d09d582`, clean |
| 2 | after create + 2 edits + PR open | branch/HEAD identical; porcelain gained ONE untracked dir — `ideation/dashboard/gate-records/draft-consent-instrument-contract/` (the `open-pr` verb's own dispatch record; see F10 note) |
| 3 | across the PR merge | identical to 2 |
| 4 | after publication of the merged docs | branch/HEAD identical (now reads `[behind 5]` origin — origin ADVANCED with the merges; the checkout itself never moved); porcelain identical to 2 |

F10 note (for the sign-off matrix): the save verb writes its `open-pr`
gate-action record UNTRACKED into the served checkout, so "porcelain
unchanged" holds for fingerprints 2→4 but not 1→2. The tracked state,
branch, and HEAD never moved at any point. Whether record placement
belongs in the served checkout is a product question filed with the
session findings.

## Clause verdict (for Brett's sign-off)

Every observable element TRUE except: session notebook (not exercised,
two named causes) and the strict porcelain reading (F10). Recommended:
PASS WITH FINDINGS.
