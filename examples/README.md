# Reference Examples

This directory contains canonical, static reference examples for the
Hermes/Omnigent/OpenSpec/Spec Kit/GitHub workflow.

These examples are not runtime state and are not proof harness replacements.
They illustrate contract shapes, traceability, stage gates, PR admission, merge
council output, and Merge Master decisions.

## Source Provenance

Reviewed and copied sources:

- `/home/brett/projects/Agents/Omnigent-Install/examples/project-alfa-decomposition/`
- `/home/brett/projects/Agents/Omnigent-Install/examples/project-alfa-speckit/`
- `/home/brett/projects/Agents/Omnigent-Install/examples/project-alfa-pr-admission/`
- `/home/brett/projects/Agents/Omnigent-Install/examples/project-alfa-merge-council/`
- `/home/brett/projects/Agents/Omnigent-Install/examples/project-alfa-next-non-doc/`
- `/home/brett/projects/Agents/Omnigent-Install/examples/merge-master/`

Reviewed but not copied in this feature:

- `/home/brett/projects/Agents/Omnigent-Install/examples/live-pilot/`
- `/home/brett/projects/Agents/Omnigent-Install/pilot-flows/`
- `/home/brett/projects/Agents/Omnigent-Install/live-pilot/`

Live pilot and pilot-flow materials remain in `Omnigent-Install` until a later
feature approves either a replacement validation path in `openxFactory` or a
separate `factory-lab` repository.

## Placement Decision

```yaml
reference_example_policy:
  canonical_static_examples: openxFactory/examples
  executable_install_proofs: Omnigent-Install
  future_executable_lab: factory-lab
```

`openxFactory/examples` is the right home for static examples that define the
factory workflow contract. `Omnigent-Install` remains the right home for
runtime proof fixtures, local scripts, worker harnesses, generated run state,
and install-specific examples that may change with Omnigent implementation.

## Included Examples

```text
examples/
  avatar-first-ui/
  merge-master/
  project-alfa/
    decomposition/
    speckit/
    pr-admission/
    merge-council/
    end-to-end-reference/
```

## Exclusions

Do not place these in `openxFactory/examples`:

- credentials or auth profiles;
- generated state;
- local workspaces;
- runtime logs;
- databases;
- live worker outputs;
- secrets;
- install-specific paths that must execute on a Cloud PC or AKS node.

If an example becomes executable, either keep it in the install repo or move it
to a future `factory-lab` repo with its own validation path.
