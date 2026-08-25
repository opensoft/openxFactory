## ADDED Requirements

### Requirement: The NotebookLM sync keeps its public CLI compatible
The implementation MUST preserve the executable path, documented flags, mode
precedence, and exit semantics of `scripts/sync-notebooklm-books.py` while its
internal responsibilities are split into focused modules.

#### Scenario: Existing automation invokes the split implementation
- **WHEN** an operator invokes the existing script path with a supported mode
- **THEN** the wrapper dispatches to the extracted implementation with the same observable output, provider operations, and exit status

#### Scenario: Invalid input remains fail-closed
- **WHEN** an operator supplies an invalid combination or missing required value
- **THEN** the CLI refuses through argparse or the existing explicit refusal path without contacting NotebookLM

### Requirement: Provider and mutable state boundaries are typed
The NotebookLM sync surface MUST pass its scoped basedpyright command with zero
errors and MUST NOT use casts, ignore directives, or unbounded `Any` values to
hide provider rows, manifest state, profile state, or session adapter contracts.

#### Scenario: Provider output enters business logic
- **WHEN** NotebookLM returns notebook or source JSON
- **THEN** the provider boundary parses required and optional fields into declared typed values before reconciliation code consumes them

#### Scenario: Profile state changes during a run
- **WHEN** the active NotebookLM profile differs from the profile bound at startup
- **THEN** the typed provider boundary refuses the next provider command before mutation

### Requirement: Scoped static quality gates start at zero debt
The repository MUST provide a reproducible scoped command that runs Ruff,
basedpyright, and the repository programming checker over the NotebookLM sync
implementation and tests, and every included checker MUST report zero findings.

#### Scenario: New scoped debt is introduced
- **WHEN** a changed NotebookLM sync file violates a configured lint, type, or programming rule
- **THEN** the scoped quality command exits nonzero and identifies the violating file and rule

#### Scenario: Unrelated repository debt exists
- **WHEN** code outside the declared NotebookLM sync surface has pre-existing findings
- **THEN** the scoped command does not broaden, baseline, suppress, or reclassify that unrelated debt

### Requirement: Module boundaries remain reviewable
Each newly extracted production or test module MUST remain below 250 pure lines
of code unless the repository programming checker defines a stricter applicable
limit, and modules MUST follow the acyclic dependency direction recorded in the
change design.

#### Scenario: A responsibility extraction is complete
- **WHEN** a production or test responsibility is moved out of the wrapper or monolithic test module
- **THEN** its destination is focused, below the applicable size ceiling, and introduces no import cycle

### Requirement: Test discovery and behavior are preserved
The split test suite MUST remain discoverable by pytest and unittest, MUST
retain the pre-split behavioral coverage, and MUST keep the real-`nlm`
hermeticity guard effective.

#### Scenario: The split suite is collected
- **WHEN** pytest collection and unittest discovery run over `tests/notebooklm`
- **THEN** all focused modules are collected without importing another `test_*.py` module and without reducing the pre-split test population

#### Scenario: A test reaches the provider boundary
- **WHEN** a NotebookLM sync test executes a provider operation
- **THEN** it uses an isolated fake or patched typed seam and never invokes the real `nlm` executable
