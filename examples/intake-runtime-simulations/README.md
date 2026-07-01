# Intake Runtime Simulations

Status: generated examples
Repository context: openxFactory

This folder stores machine-readable outputs from the subtype install-readiness
simulator.

- [pass1.yaml](pass1.yaml) records the current local repo/catalog gaps for every
  factory type and subtype.
- [pass2.yaml](pass2.yaml) records the simulated state after generic starter
  scaffold fixes and the runtime gaps still left.

Regenerate from the openxFactory repo root:

```bash
python3 scripts/simulate-subtype-install-readiness.py
```
