# Tasks: OpenSpec repository casing compatibility

Status: draft

- [x] T001 [O] Record the bounded governance and selected baseline; files: openspec/changes/preserve-openspec-repository-casing/**, specs/042-openspec-repository-casing/**; verify: pinned strict change validation.
- [x] T002 [O] Add approved comparison keys without mutating reported identity or pin data; files: scripts/validate-openspec-cli-pin.py; verify: old/current scope matching and unchanged contract bytes.
- [x] T003 [S] Add rejection, duplicate and stale regressions; files: tests/openspec_cli_pin/test_openspec_cli_pin.py; verify: complete reader suite and actual consumer corpus.
- [ ] T004 [O] Record source/integration evidence and regenerate the owned corpus ledger; files: specs/042-openspec-repository-casing/evidence.md, tests/sequenced_after/corpus-ledger.yaml, README.md; verify: exact candidate checks and explicit Codex receipt, source-only boundary.

Consumer pin selection and qualification preparation remain with codeXfactory
feature 058. No owner-act box or live qualification is transcribed here.
