# Acceptance: the widened sweep, measured (§11.4)

**Status**: record

**Recorded**: 2026-08-27 · **Feature**: `024-root-governed-repo-recognition`

## The tree that was swept

The live aggregation `/home/brett/projects/xFactory` does **not** yet declare a
root-level `openXwallet` gitlink — that is P4, which has not landed — and the
shared checkout must never have submodules initialized in it. So the sweep ran
over a scratch workspace root assembled for the purpose:

| entry | contents |
| --- | --- |
| `openxFactory/` | this feature branch |
| `openXwallet/` | a full copy of `wallet-v1.1` (`63f5a1a`), initialized |
| `openAvatar/` | the live root-level checkout |
| `installs/hermes-install/` | present and pinned — the allowlist's counter-example |
| `.gitmodules` | declares all four at their real paths |

## Result 1 — the widening is real and measurable

The SAME tree, swept by `origin/main`'s script and by this branch's:

| | openXwallet documents projected | openAvatar documents projected |
| --- | --- | --- |
| `origin/main` | **0** | **0** |
| this branch | **4** | **2** |

The four: `openXwallet/contracts/CHANGELOG.md`,
`contracts/openxwallet-agent-profile/README.md`,
`contracts/openxwallet/README.md`, `docs/pin-resync-runbook.md`. The two:
`openAvatar/docs/README.md`, `docs/wcag-exception-register.md`. Before this
change both repositories were swept by nothing at all.

`installs/hermes-install` was projected by nothing, in both runs — the allowlist
holding, which is the whole reason D11 chose an allowlist over the rule.

## Result 2 — no `ideation-openxwallet` book derives, and the widening is not why

```
$ python3 scripts/sync-notebooklm-books.py <scratch-root> --book ideation-openxwallet
error: --book 'ideation-openxwallet' is not a book this scan derives;
       available: canon, drafts, ideation-openxfactory
```

Ideation-book membership is **STATUS-DERIVED ONLY**
(`split-ideation-book-per-repo`): a book exists exactly when its repository has
at least one `brainstorm` or `staged` document. Neither root product has one:

| repository | Status headers found |
| --- | --- |
| openXwallet @ `wallet-v1.1` | 3 ratified, 2 record, 2 standard — **0 brainstorm/staged** |
| openAvatar (live) | 2 draft, 1 record — **0 brainstorm/staged** |

So `xf-ideation-openavatar`'s absence had **two** causes, not one. Council
concern 4 named the recognition cause and was right about it; task 11.4 then
wrote an acceptance that assumes it was the only one. It is not. **This change
removes the recognition cause; the membership cause is a document nobody has
written yet.**

## Result 3 — the acceptance holds the moment the precondition does

One `Status: brainstorm` document added to the scratch openXwallet copy, same
widened script, same tree:

```
books: canon, drafts, ideation-openxfactory, ideation-openxwallet
  alias: xf-ideation-openxwallet
  title: xFactory Ideation — openXwallet
  openXwallet/ideation/brainstorm/wallet-review-authority.md
      -> [brainstorm] openXwallet: wallet-review-authority
  + the three [grounding] seeds
```

Alias and title are exactly what §11.4 asks for. The scratch document was removed
after the run; it exists in no repository.

## `--apply` was NOT run. What the operator owes, and in what order

`nlm notebook list` answers in this shell, so auth was not the blocker. Three
things were:

1. **There is no book to create.** The scan derives none, so `--apply` would
   create nothing for openXwallet either way.
2. **An apply from a scratch root is dangerous.** `sync_book` reconciles a live
   book against the scan, and the scratch root holds no `xFactories/*`; running
   `--apply` there would reconcile the REAL shared `canon` and `drafts` books
   against a partial tree.
3. **The live aggregation cannot yet be swept for openXwallet at all** — no root
   gitlink until P4.

The order, therefore:

1. **P4** lands the aggregation's root `openXwallet` gitlink.
2. openXwallet gains its first `brainstorm` or `staged` document. Until then
   §11.4's acceptance is not reachable and no widening can make it so.
3. `git submodule update --init openXwallet` in the aggregation, then `python3
   openxFactory/scripts/sync-notebooklm-books.py . --apply` — reviewing the plan
   first, because this change also adds openXwallet's 4 and openAvatar's 2
   documents to the shared `canon`/`drafts` books. Those books are subject to the
   300-source cap and the sync's own capacity guard; the plan names the adds.
