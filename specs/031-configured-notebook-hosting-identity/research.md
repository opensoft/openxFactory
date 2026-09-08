# Research: what the code does today, read rather than described

Measured on branch `031-configured-notebook-hosting-identity` at its base,
openxFactory main `e7c53012`. The packet's own § 1 measured the same surface at
`543d47a9`; this file re-measures at the realization head, which is packet task
0.3's obligation.

## 0.3 — the premises, re-checked at realization head

| premise | how it was checked | result |
| --- | --- | --- |
| Five files still carry forty lines | `git grep -cIE` over the four addresses at `origin/main` | `examples/notebook-projection-hosting.yaml` 18, `openspec/specs/lifecycle-notebook-projection/spec.md` 1, `tests/notebooklm/test_nlm_auth.py` 2, `tests/notebooklm/test_sync_notebooklm_books.py` 11, `tests/notebooklm/test_validate_hosting.py` 8 — **40, unchanged** |
| None has become a release-inventory member | `grep` of each path against `contracts/releases/contract-v3.4.digests.yaml` | not present; **no digest set moves** |
| The Q1/Q3 docs pull request has landed | `gh pr view 786` | MERGED 2026-09-08T12:28:32Z, main `e8021fed`; PR #785 merged 12:21:55Z |
| `openspec validate --all --strict` reads one pre-existing failure and no more | run at base | `100 passed, 1 failed` — the failure is `disposition-codexfactory-declared-renames`, a deltaless disposition packet unrelated to this work |

Two further baselines, taken so the realization can prove it added nothing:

- `python3 -m pytest tests/notebooklm tests/doc-health tests/sequenced_after -q`
  → **1997 passed, 37 subtests passed**.
- `python3 scripts/doc-health.py --single-repo .`
  → **10 critical, 9 error, 55 warning, 16 info. New regressions vs previous
  report: 0.** (The packet predicted `9/9/59/16` at its own head; the corpus has
  moved since, which is why the comparison that matters is this branch against
  THIS baseline and not against the packet's numbers.)

## 1. Who reads the record

| reader | path today | parse |
| --- | --- | --- |
| `scripts/sync-notebooklm-books.py` | `HOSTING_REL`, a module constant joined onto the WORKSPACE root | `read_hosting_declaration()`, a narrow scalar reader over the `hosting:` block's two-space scalars listed in `_HOSTING_SCALARS` plus its `migration:` sub-block at indent 4. No YAML dependency. |
| `scripts/validate-notebook-projection-hosting.py` | `DEFAULT_REL`, joined onto the REPO root, overridable by `argv[1]` | `yaml.safe_load`, authority on the whole record including the roster |

Nothing else consumes it. No contract registers it; no manifest pins it.

## 2. What the values DO

`enforce_hosting_profile(root)` runs five steps: read; pick the binding target
(`nlm_profile`, or `migration.from_nlm_profile` while `migration.state ==
"pending"`); compare the CLI's process-global active profile against it and refuse
on mismatch; **compare the ADDRESS** the CLI recorded in
`profiles/<name>/metadata.json` against `hosting.account` (or
`migration.from_account` while pending), case-insensitively, and refuse on
mismatch; bind, with `assert_still_bound()` re-reading the config before every
later invocation.

Step four is why redaction in place is unavailable: `hosting.account` is one side
of an equality test whose other side is a live Google account.

The roster's addresses are the identity of a RECORD: the validator's uniqueness key
is `(hosting_account, user, book_or_alias)`, so two rows differing only by a
redacted address collapse into one under that key.

## 3. What the tests do

`tests/notebooklm/test_sync_notebooklm_books.py` writes its own declaration text
into a temporary workspace through `_declare_hosting(root, text)`;
`tests/notebooklm/test_validate_hosting.py` writes its own into a temporary
directory through `_validate(text)`. Twenty of the twenty-one literals are
therefore fixture text and prove exactly as much when synthetic.

The twenty-first is `test_the_committed_record_conforms`, which validates
`REPO_ROOT / validator.DEFAULT_REL` and asserts "this install's own declaration
must pass". Its subject is the live record and its truth depends on the live
record and the committed file being ONE file. That is the one check the split
costs, and § 3.4 of the packet's design is how it is put back.

## 4. The eight questions the validator asks

Two-case vocabulary; the account is user-shaped (`@` present, no service-account
marker); an operator-hosted record names `account_type: google_workspace_user`;
the account's domain equals the declared domain; `nlm_profile` present; a pending
migration names both `from_account` and `from_nlm_profile`; the roster's six
fields, its uniqueness triple and its role vocabulary; `granted_by ==
approval.designated_actor`.

**Not one of the eight is about WHICH real account is named.** Every one is a
property of the record's shape or an equality between two of its own fields, which
is why the negative mutations keep their teeth over synthetic values.

## 5. The CI pins this work must not move

`.github/workflows/pytest-suite.yml` carries `MIN_SELECTED: "7090"`, `MIN_PASSED:
"7070"` (FLOORS — "may only rise") and `EXPECT_SKIPPED: "21"` (EXACT). The file's
own comment settles what a change like this one owes: *"(MIN_SELECTED and
MIN_PASSED are FLOORS and need no edit: the new module only raises the actuals,
which widens the printed margin.)"* This feature adds passing tests and no skipped
test, so **no pin moves and the workflow is not touched** — recorded here because
packet task 4.4 could be read as asking for a raise, and raising a floor to a
number measured on a developer machine is exactly what that file forbids.

`tests/doc-health/test_modified_block_currency_self_gate.py`'s `_LEDGER_SUBJECTS`
already carries this packet's row — added by PR #783, the packet's own landing,
line 752. Nothing is owed here.

## 6. Promotion happens at the archive act — measured, not assumed

`openspec/specs/lifecycle-notebook-projection/spec.md`'s history shows its last
substantive writer was `4290cad2 Archive add-notebook-projection-identity`, and
the two commits before it are likewise archive/promote acts. So this repository
promotes a delta into canon AT THE ARCHIVE COMMIT and never in the realization
pull request. **This feature therefore leaves the promoted spec untouched**, and
the one remaining address line in it is retired by the archive act — packet task
1.1, which says the same thing in the imperative.
