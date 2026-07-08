# TUI Spec Questionnaire

Status: draft
Kind: template
Progress: awaiting answers
Created: 2026-07-01
Repository context: `openxFactory`
Purpose: capture the context and unanswered decisions needed to write a
buildable OpenSpec change for the xFactory TUI.

## How To Use This Document

Answer the questions in the Answer Sheet section, then tell Codex that this
document is complete. A fresh Codex session should read this file first, then
create an OpenSpec proposal, design, tasks, and spec deltas for the TUI.

Recommended next command after answers are complete:

```bash
openspec list --json
```

At the time this document was created, `openspec list --json` showed no active
changes.

## Current Repo Facts

The old canonical name was `openWorkflow`; the new canonical name is
`openxFactory`. The workspace was swept for old-name text and filenames outside
`.git`, and no old-name matches remained at the end of the rename pass.

`openxFactory` currently documents planned installer commands and stages, but it
does not contain an implemented TUI or CLI package. A search found no
`package.json`, `pyproject.toml`, `go.mod`, `Cargo.toml`, TUI source package,
CLI source package, Dockerfile, or Compose file in the repo paths checked.

Existing planning docs relevant to the TUI:

- `docs/intake-and-installer-plan.md`
- `docs/self-hosted-runtime-binding-plan.md`
- `docs/runtime-services-plan.md`
- `docs/deploy-artifacts-plan.md`
- `templates/intake/README.md`
- `templates/intake/subtypes/README.md`

Planned command names already appearing in docs:

```bash
xfactory intake
xfactory install --answers examples/instantiation-answers.generated.yaml
xfactory bind-runtime
xfactory validate-runtime
xfactory dry-run --workflow <workflow-id>
xfactory readiness
```

## Related Runtime Context

The expected high-level TUI flow is:

```text
┌────────┐   ┌─────────┐   ┌──────────────┐   ┌──────────┐   ┌───────────┐
│ intake │ ->│ install │ ->│ bind runtime │ ->│ validate │ ->│ readiness │
└────────┘   └─────────┘   └──────────────┘   └──────────┘   └───────────┘
                                                      │
                                                      v
                                                dry-run proof
```

Runtime services are not implemented yet. The runtime-services plan defines the
minimum service set as Hermes API, openxFactory control API, job scheduler and
queue, Omnigent worker gateway, credential broker, adapter registry and runner,
Postgres, artifact store, audit/event stream, and readiness service.

Deploy artifacts are not implemented yet. The deploy-artifacts plan calls for
service Dockerfiles, Compose, `.env.example`, dev scripts, runtime binding
examples, database migrations, CI, observability, and a first production target.

## Install Repo Context

`Omnigent-Install` is registered as a submodule at:

```text
installs/omnigent-install -> git@github.com:opensoft/Omnigent-Install.git
```

During LedgerxFactory development, the decision record allows Omnigent to track
its active development branch. `.gitmodules` is configured with:

```text
branch = main
```

Important Git behavior: submodules do not store "latest" in the parent repo.
The parent repo always records an exact commit. Pre-release "latest" means
running:

```bash
git submodule sync installs/omnigent-install
git submodule update --init --remote installs/omnigent-install
git add .gitmodules installs/omnigent-install
git commit -m "Advance Omnigent install to latest development head"
```

At LedgerxFactory release, Omnigent should be frozen to an approved commit or
tag and treated as a release dependency.

`Hermes-Install` is not yet a submodule. The canonical remote decision remains
open between:

```text
git@github.com:FarHeap/Hermes-Install.git
git@github.com:opensoft/Hermes-Install.git
```

The TUI spec must decide whether missing Hermes install support blocks full
installation or allows a contract/dry-run-only mode.

## LedgerxFactory Context

`LedgerxFactory` was expanded from a generic scaffold into a domain-ready
contract surface. It now includes Ledgerx credential requirements, adapter
contracts, workflows, runtime binding template, schemas, golden-path examples,
blocked-path examples, and a stricter validator.

Relevant Ledgerx files:

- `/home/brett/projects/xFactory/LedgerxFactory/stack.yaml`
- `/home/brett/projects/xFactory/LedgerxFactory/credentials/requirements.yaml`
- `/home/brett/projects/xFactory/LedgerxFactory/runtime/runtime-binding.template.yaml`
- `/home/brett/projects/xFactory/LedgerxFactory/scripts/validate-domain-factory.py`
- `/home/brett/projects/xFactory/LedgerxFactory/workflows/bank_feed_review.yaml`

Ledgerx validation passed with:

```bash
cd /home/brett/projects/xFactory/LedgerxFactory
make validate
```

The first practical TUI proof path may use Ledgerx as the initial supported
domain.

## Validation Environment Note

Some validators require PyYAML. In this workspace, `/home/brett/bin/python3`
lacked `yaml`, while `/usr/bin/python3` had PyYAML available. Successful
validation commands used `/usr/bin/python3` where needed:

```bash
cd /home/brett/projects/xFactory/openxFactory
/usr/bin/python3 scripts/validate-intake-templates.py
/usr/bin/python3 scripts/simulate-subtype-install-readiness.py

cd /home/brett/projects/xFactory/MedxFactory
/usr/bin/python3 scripts/validate.py
```

The TUI spec should decide whether v1 creates a repo-local virtual environment,
uses a packaged binary, or documents host prerequisites.

## Answer Sheet

Fill in the answers below.

### 1. Primary User

Who is the first TUI for: internal FarHeap/OpenSoft operators, technical
customers self-hosting, or nontechnical customers guided by support?

Answer:

```text
TBD
```

### 2. MVP Boundary

Should v1 handle the full flow, or only `intake + generate files + readiness
report`?

Answer:

```text
TBD
```

### 3. First Domain

Should the first supported path be `LedgerxFactory` only, with other domains
later, or should it support every `openxFactory` intake template from day one?

Answer:

```text
TBD
```

### 4. Runtime Target

Should v1 deploy to local Docker Compose, an existing remote Linux host, Azure
Container Apps, Kubernetes, or just generate deploy artifacts without running
them?

Answer:

```text
TBD
```

### 5. Submodules

Should the TUI initialize and update `Omnigent-Install` automatically using
`git submodule update --remote`, or only warn and show the command?

Answer:

```text
TBD
```

### 6. Hermes Handling

Since `Hermes-Install` is still deferred, should the TUI block full install
until Hermes is configured, or allow a contract/dry-run-only mode?

Answer:

```text
TBD
```

### 7. Credentials

Should the TUI collect only secret references, never raw secrets? Which provider
should v1 support first: local dev env refs, Azure Key Vault, 1Password,
Bitwarden, AWS Secrets Manager, or GCP Secret Manager?

Answer:

```text
TBD
```

### 8. Installer Behavior

Should the TUI actually run commands like `docker compose up`, migrations, and
dry-runs, or should it produce a runbook plus generated config for an operator
to execute?

Answer:

```text
TBD
```

### 9. State And Output Paths

Where should it write outputs: `examples/instantiation-answers.generated.yaml`,
`runtime/runtime-binding.generated.yaml`, a `.openxfactory/` workspace folder,
or a user-selected path?

Answer:

```text
TBD
```

### 10. UX Shape

Should it be a guided wizard, a dashboard with resumable sections, or both?

Answer:

```text
TBD
```

### 11. Noninteractive Mode

Do we need the same binary to support CI/scripted usage, for example:

```bash
xfactory install --answers file.yaml --non-interactive
```

Answer:

```text
TBD
```

### 12. Readiness Levels

Should the TUI expose the L0-L8 readiness model directly, or translate that into
simpler states like `schema ready`, `runtime ready`, `workflow ready`, and
`live ready`?

Answer:

```text
TBD
```

### 13. First Dry-Run

For Ledgerx, should the first proof workflow be `bank_feed_review`, or a safer
synthetic workflow that requires no adapter endpoint?

Answer:

```text
TBD
```

### 14. Implementation Stack

Preferred implementation stack: Python Textual, Go Bubble Tea, Node Ink, Rust
Ratatui, or whichever best fits packaging?

Answer:

```text
TBD
```

### 15. Acceptance Test

What means v1 is done? Example:

```text
fresh checkout, run one command, answer wizard, generate runtime binding,
initialize Omnigent, validate Ledgerx, run dry-run, produce readiness report
```

Answer:

```text
TBD
```

## Candidate Spec Shape After Answers

When this document is complete, create an OpenSpec change with a name similar
to:

```text
add-openxfactory-tui-installer
```

Likely artifacts:

- `openspec/changes/add-openxfactory-tui-installer/proposal.md`
- `openspec/changes/add-openxfactory-tui-installer/design.md`
- `openspec/changes/add-openxfactory-tui-installer/tasks.md`
- `openspec/changes/add-openxfactory-tui-installer/specs/tui-installer/spec.md`

Likely requirements to capture:

- TUI can run intake from existing `templates/intake` data.
- TUI can generate an answers file without raw secrets.
- TUI can generate or validate a runtime binding manifest.
- TUI can initialize or report submodule state according to the selected policy.
- TUI can distinguish contract-only, dry-run-ready, workflow-ready, and
  live-ready states.
- TUI can run noninteractive mode if Question 11 says yes.
- TUI writes resumable state to the selected output location.
- TUI never stores raw secrets in repo files, logs, support bundles, or
  generated artifacts.
