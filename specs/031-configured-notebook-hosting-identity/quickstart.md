# Quickstart: telling this install where its hosting declaration is

Two commands and one file. Everything below is the OPERATOR's, and none of it is
performed by an agent.

## 1. Write the one file

At the **workspace root** — for the aggregation layout that is
`~/projects/xFactory`, not `openxFactory`:

```yaml
# ~/projects/xFactory/.xfactory/notebook-hosting.yaml
# WHERE THIS MACHINE'S NOTEBOOK HOSTING DECLARATION IS. A PATH, AND NO SECRET.
declaration_path: installs/hermes-install/config/clients/opensoft/notebook-projection-hosting.yaml
```

The path may be workspace-relative (as above) or absolute. The file is
gitignored in openxFactory; **the aggregation repository wants the same
`.xfactory/` entry in its own `.gitignore`**, which this feature does not touch
because it is a third repository — noted so it is not discovered by surprise in
`git status`.

For a single run, skip the file:

```bash
export XFACTORY_NOTEBOOK_HOSTING_DECLARATION=/abs/path/to/notebook-projection-hosting.yaml
```

The environment variable wins over the file. Nothing configured at all is
**UNDECLARED** — a nonconforming transition state the ratified requirement
already defines, in which the sync runs under the CLI's default profile and says
plainly that the projection is not governed by a declared account. A fresh
public clone is in that state and works.

## 2. Prove the binding before any apply

```bash
cd ~/projects/xFactory
python3 openxFactory/scripts/validate-notebook-projection-hosting.py --resolved
#   expect: validate-notebook-projection-hosting: 0 error(s) over <the resolved path> (configuration)

python3 openxFactory/scripts/sync-notebooklm-books.py .          # preview, no --apply
#   expect a line beginning: hosting: operator_hosted — … (nlm profile 'company', verified active)
```

**That first green line is the live record's conformance evidence** and it is
packet task 5.2. It is what replaced a CI check: while the live record and the
committed example were one file, `test_the_committed_record_conforms` checked
the live declaration automatically; after the split this repository's CI cannot
reach the live record without publishing it. `--resolved` therefore refuses to
fall back to the committed example and refuses a record marked as one, so a
green line from it is evidence about the live record and nothing else.

## What you will see if something is wrong

| symptom | what it means |
| --- | --- |
| `NO DECLARED HOSTING IDENTITY … nothing is configured` | no environment variable and no `declaration_path:`. Step 1. |
| `NO DECLARED HOSTING IDENTITY … configuration names <path>, which is not a readable file` | the path is configured and the record is not there — most often a private submodule that is not initialized. Still non-breaking, and deliberately so. |
| `is the SHIPPED SYNTHETIC EXAMPLE` | configuration is pointing at `examples/notebook-projection-hosting.yaml` (or a copy of it). A fixture is no install's declaration; point it at the real one. |
| `EXISTS but no declaration could be read from it` | the record is valid YAML the narrow reader cannot parse — flow style, four-space indentation, tabs. Re-indent it to match the committed example. |
| `expected the 'company' profile but the CLI's active profile is …` | `nlm login switch company`. |
| `profile 'company' is signed in as <address>, but this install expects <declared>` | the profile name matches and the ACCOUNT does not — the exact mix-up a declared identity exists to catch. `nlm login --profile company`, as the declared account. |

## Where the live record is, and why it is not here

`installs/hermes-install/config/clients/opensoft/notebook-projection-hosting.yaml`
— ruled by Brett Heap on 2026-09-08 (OQ-A). It carries the declaration, the
custody reference, the approval designation, seven share grants and one recorded
denial. It is not in openxFactory because openxFactory becomes public and this
record's addresses are the values the sync compares against a live Google
account: a placeholder there would disarm a guard rather than redact a record,
and a placeholder in the roster would falsify a record of governed acts.
