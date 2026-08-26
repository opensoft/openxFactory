# Design: adopt-neutral-utility-pack

The small-sibling follow-on to `adopt-neutral-tooling-home`: the same
neutrality sweep, the same movement pattern, three register entries
(DTN-018/019/021) instead of three capabilities' runtimes.

## D1. History handling — copy with provenance, never graft

Same ruling as `adopt-neutral-tooling-home` design D1, for the same
open-sourcing reason: the files are plain-copied at a pinned codexFactory
commit (`main@1568c54b65e0de1dc63d9eef771f299ddbe60fcf`), the adopting
commit message carries `Provenance: adopted from codexFactory main@<sha>`,
and git filter-repo grafting is rejected — openxFactory is slated for
open-sourcing, and codexFactory's private commit history must not ride into
a public repo. The private history remains intact and citable in
codexFactory.

## D2. Original filenames retained — the shed is a path-only repoint

The four scripts keep their exact names (`check-inventory-consistency.py`,
`check-workflow-state-parity.py`, `check-openxfactory-pin.py`,
`proposal-support.py`) so codexFactory's `validate-docs.sh` sheds by
repointing `python3 scripts/<name>` to the already-resolved `$OPENX`
checkout's `scripts/<name>` — path-only edits, no argument or behavior
changes. Corollary on the CLI surface: the three checks' target-repo
positionals are retained but their self-repo DEFAULTS are dropped (target
now required) — in the publisher checkout, "this script's repo" is a
wrong-target default, and the known consumer already passes `"$REPO_ROOT"`
explicitly, so requiring the argument costs the repoint nothing.

## D3. check-openxfactory-pin.py lands AS-IS; the overlap merge is deferred

`check-openxfactory-pin.py` is adopted beside
`validate-domain-openxfactory-pins.py` even though the two overlap (the
register entry itself says "partially duplicates"). They are not the same
check: the pin checker classifies ancestry against the aggregation
submodule pointer (PASS/WARN-stale/ERROR-divergent/SKIP), the canonical
validator validates the declared pin block's shape and reachability.
Merging them needs its own design pass over both consumers' gates and is
deliberately deferred — recorded as a non-goal scenario in the
`domain-conformance-checks` delta, not attempted here.

## D4. The layer-template schema joins the hermes-domain-overlay family

`schemas/hermes-template.schema.json` lands at
`contracts/hermes-domain-overlay/hermes-layer-template.schema.json`: the
promoted `hermes-domain-overlay` capability (created by archiving
`add-hermes-domain-overlay-contract`) is what governs
`contracts/hermes-domain-overlay/`, so the ADDED requirement folds into
that capability — `domain-conformance-checks` would be the wrong altitude
for a contract-family membership rule. JSON format is retained (the family
is otherwise YAML; converting a draft-2020-12 schema buys nothing and
breaks byte-level comparability with the domain copies still in the wild).
The `$id` is neutralized to the openxfactory.local host; title/description
prose sheds the codexFactory naming; the `kind` enum values
(`subject_hermes_template`, `client_hermes_template`) and the
`role: client` const are frozen v1 machine spellings per
`contracts/policies/layer-vocabulary.yaml` and are NOT renamed.
`contracts/manifest.yaml` is untouched: bundle publication is additive and
rides the next contract release, per the family's versioned-publication
requirement — until a consumer re-pins, the domain-local copy stays
authoritative (document-lifecycle mid-promotion rule), which is also why
the register rows stop at `implemented`.
