# Step B — Bullseye-motivated creation (`add-workbench-bullseye-and-create` 7.2)

Status: record · 2026-07-31 session · serve http://127.0.0.1:46129

## Scope reading (adapted route — see session-findings F5)

- The tile's own workbench lens could not form (F5: staging-only keywords
  absent from the corpus keyword index → empty rail), and the global lens
  tab is display-only by design (no `onActivate`). The scope READING
  happened on the global lens: checked {consent, party-ladder,
  credential-contracts, delegation} → 7 documents, ALL outer ring, empty
  centre — read live by Brett as the motivating gap: no corpus document
  spans the consent-instrument neighborhood; the authority chain has no
  root document.
- Motivated document (Brett's pick from three AI-proposed directions):
  the packet's decisions overview — the ranked record of the nine
  2026-07-31 rulings.

## Creation (workbench lens tab, "＋ new document from the checked set")

| Item | Value |
|---|---|
| Declared landing | `ideation/staging/consent-instrument-contract/` (topic folder) |
| Created document | `ideation/staging/consent-instrument-contract/consent-instrument-design-decisions.md` — found where declared |
| Gate-action record | `ideation/dashboard/gate-records/ideation-staging-consent-instrument-contract-consent-instrument-design-decisions/create-document-20260731T231323Z.gate-action.yaml` |
| Gate-action commit | `b280542b7c85b585e9c0039bc76814a86a068d91` (one commit: document + record) |
| Session | `draft/consent-instrument-contract` OPENED by the create (branch-sessions integration); worktree `d10-corpus-worktrees/sessions/draft__consent-instrument-contract`, clean after the commit |
| Served checkout | UNMOVED: `d10-corpus` still `d09d582…`, status clean (verified post-create) |

## Source line (verbatim, as displayed)

> Source: staging workbench scope: staged consent-instrument-contract ·
> keyword-lens recipe: checked none · pinned none · at source_revision
> d09d5820de5b63b9528f6baea884a6dccde9b158

Note: an honest LIVE derivation — it records the actual (empty) recipe and
the exact served source revision rather than a pasted membership list,
satisfying the "re-derives, not a static copy" clause. The recipe
emptiness is finding F5's fingerprint on the evidence; the source_revision
matches the served corpus HEAD exactly (while the session BRANCH based on
stale local main — that divergence is F9).

## Clause verdict

- Creation landed where the dialog declared: TRUE (topic folder).
- `Source:` re-derives membership: TRUE in mechanism (live recipe + scope +
  source_revision), with the recipe honestly empty per F5.
- Pass/Fail: Brett's sign-off cell; recommended PASS WITH FINDINGS
  (F5 adaptation + F9 base-revision mismatch recorded).

## Step-B-adjacent findings logged during creation

- F8: session NotebookLM notebook creation failed — the workbench invokes
  `nlm notebook create … --json`, and the installed nlm CLI has no
  `--json` option (CLI version drift). Session remains fully usable; the
  remedy path printed by the UI names FR-042/FR-040/D19 and
  `sync-notebooklm-books.py --session-ref`.
- F9: the session branch based on the repository's local `main` ref
  (`c782d6d`, 14 behind origin at open time), while the Source line claims
  the served `d09d582` — harmless here (ancestor of origin/main; topic
  folder byte-identical across the gap) but an honesty mismatch in any
  multi-session tree where local main lags.
