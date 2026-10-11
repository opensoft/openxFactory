# codexFactory's sibling currency dispositions, retired ahead of their re-derivations: the runs

Status: record
Kind: report
Measured on: 2026-10-09, between 20:09Z and 20:16Z (UTC, `date -u` at each run)
Base: openxFactory branch `change/retire-codexfactory-sibling-currency-dispositions`,
merged up to openxFactory `main` `9a272c6d`. The pin on `main` is the blob at
`93d13d6c`, unchanged at `9a272c6d`.
Consuming tree: codeXfactory/codexFactory `main` at
`33b916c12a1dcccf882557d6edcf396c98824f31`, a fresh depth-1 clone whose push URL
was set to `no-push-scratch-clone`. Nothing was committed to it, and nothing
was pushed anywhere. No byte of codexFactory is written by this packet.
Measured by: lane `codexfactory-1` (display `codeXfactory-1`)
Word this packet is drafted under: Brett Heap, 2026-10-09T17:35:29Z, verbatim
**"This lane drafts it (Recommended)"**, recorded on
codeXfactory/codexFactory#549 (comment 6086047985).

Every block below is taken from the saved run output. Lines that are elided are
marked `…`. Nothing is elided from a totals line, a verdict line or an exit
code. The per-entry `why:` and `cited to:` continuation lines that the tool
prints under each applied disposition are elided throughout. Absolute scratch
paths are shortened to `<…>`. The pinned CLI is `@fission-ai/openspec@1.12.0`,
resolved by content address on every run:

```
openspec-cli-pin: @fission-ai/openspec@1.12.0 from pinned artifact (<…>/node_modules/.bin/openspec); integrity sha512-oFE2Lj7WVSc87nSi… verified
openspec-cli-pin: dependency closure openspec-cli-pin.1.12.0.package-lock.json (80 packages); lockfile_integrity sha512-aw5lIN45tQq2WZll… verified; installed with `npm ci --ignore-scripts`
```

**The two pins.**
- "The pin on `main`" is openxFactory `main`'s `contracts/openspec-cli-pin.yaml`,
  copied with its lockfile into a scratch directory (`sha256`
  `09dd2d634a95d447037a17f7e359eb24fd73c1edbabae800ad491a79569c877f`, 5
  entries). The lockfile resolves relative to the pin's own directory, so the
  copy carries it.
- "This packet's pin" is this branch's `contracts/openspec-cli-pin.yaml`, as
  committed (3 entries).

**The command**, in the form a consuming repository's gate issues it:

```
cd <openxFactory worktree at this branch>
OPENSPEC_TELEMETRY=0 python3 scripts/validate-openspec-cli-pin.py \
    --repo <codexFactory tree> --all --strict --pin <pin> </dev/null
```

**What is being proved.**
- The deletion is exactly two entries, and nothing else in the pin moved (§ 1).
- On codexFactory as it stands, the pin on `main` is green (§ 2), and this
  packet's pin leaves both findings UNDISPOSITIONED (§ 3). That is the
  constraint on codexFactory's next advance past this change.
- With both sibling blocks re-derived, the pin on `main` REFUSES stale (§ 4),
  and this packet's pin is green (§ 5). That is why the deletion has to come
  first.
- openxFactory's own gate is green with this packet in the tree (§ 6).
- The touched tests pass (§ 7).

---

## 1. The deletion, checked by parsing

Both pins were parsed with `yaml.safe_load` and compared by
`(repo, item, path)`:

```
before 5
   ('openxFactory', 'add-chain-attestation', 'signed-execution-chain/spec.md')
   ('codexFactory', 'amend-composition-selector-labelling', 'domain-hermes-content/spec.md')
   ('codexFactory', 'relocate-review-authority-floor', 'repository-gate-floor/spec.md')
   ('codexFactory', 'extend-merge-master-envelope-to-floor-bot-lanes', 'merge-master-approval/spec.md')
   ('codexFactory', 'relocate-review-authority-floor', 'merge-master-approval/spec.md')
after 3
   ('openxFactory', 'add-chain-attestation', 'signed-execution-chain/spec.md')
   ('codexFactory', 'amend-composition-selector-labelling', 'domain-hermes-content/spec.md')
   ('codexFactory', 'relocate-review-authority-floor', 'repository-gate-floor/spec.md')
removed [('codexFactory', 'extend-merge-master-envelope-to-floor-bot-lanes', 'merge-master-approval/spec.md'), ('codexFactory', 'relocate-review-authority-floor', 'merge-master-approval/spec.md')]
survivor identical: add-chain-attestation signed-execution-chain/spec.md True
survivor identical: amend-composition-selector-labelling domain-hermes-content/spec.md True
survivor identical: relocate-review-authority-floor repository-gate-floor/spec.md True
top-level keys other than dispositions identical
```

The live pin's packet-referent count, read with
`scripts/validate-pin-registrations.py`'s own `citation_lines_in`,
`read_citation` and `packet_reference.resolve`: **5 referents in 4 active
packets** on the pin on `main`, and **3 referents in 3 active packets** on
this packet's pin. The two that left are both
`openspec/changes/disposition-codexfactory-regular-pr-council-clearance-archive/evidence/codexfactory-regular-pr-council-clearance-archive-2026-09-11.md`.
This is why `tests/pin_registrations/` moves its floor from 4 to 3.

---

## 2. codexFactory as it stands, the pin on `main`: exit 0, 4 applied

Tree: codexFactory `main` `33b916c1`, which declares `xfactory.contract_ref:
0992369ab7f9b4d81ca3099b02961181388c1726` (`stack.yaml:197`). Neither sibling
block is re-derived: each still carries *"A human-authored pull request is
never auto-approved"*. Canon (`openspec/specs/merge-master-approval/spec.md`)
carries the two retitled scenarios at lines 240 and 246.

```
$ … --repo <cxf@33b916c1> --all --strict --pin <pin on main>
…
Totals: 34 passed, 3 failed (37 items)
openspec-cli-pin: DISPOSITIONED FINDINGS in codexFactory (4 applied) — this run is NOT a clean tree:
  ✗→D amend-composition-selector-labelling / domain-hermes-content/spec.md
  ✗→D extend-merge-master-envelope-to-floor-bot-lanes / merge-master-approval/spec.md
  ✗→D relocate-review-authority-floor / merge-master-approval/spec.md
  ✗→D relocate-review-authority-floor / repository-gate-floor/spec.md
OK openspec-cli-pin: @fission-ai/openspec@1.12.0 verified against its content address; every target validated --strict with 0 UNDISPOSITIONED failures. THIS IS NOT A CLEAN TREE: 4 finding(s) are ACCEPTED EXCEPTIONS, named above.
exit 0
```

This is also the reading codexFactory #549's FIRST advance, to `93d13d6c`, gets.
That commit's pin is this same blob.

---

## 3. codexFactory as it stands, this packet's pin: exit 1, two UNDISPOSITIONED

```
$ … --repo <cxf@33b916c1> --all --strict --pin <this packet's pin>
…
Totals: 34 passed, 3 failed (37 items)
openspec-cli-pin: DISPOSITIONED FINDINGS in codexFactory (2 applied) — this run is NOT a clean tree:
  ✗→D amend-composition-selector-labelling / domain-hermes-content/spec.md
  ✗→D relocate-review-authority-floor / repository-gate-floor/spec.md
openspec-cli-pin: the pinned CLI reported 2 failure(s) this pin does not disposition. The PIN held — this is a finding about the deltas, not about which tool ran.
  ✗ extend-merge-master-envelope-to-floor-bot-lanes / merge-master-approval/spec.md: MODIFIED "Bounded autonomous surface" omits scenario(s) the current spec still has: "A human-authored pull request is never approved by tier 1 alone", "A gate-integrity path is never approved autonomously". Copy them into the MODIFIED block (a MODIFIED requirement replaces the whole block, so archive refuses to drop them).
  ✗ relocate-review-authority-floor / merge-master-approval/spec.md: MODIFIED "Bounded autonomous surface" omits scenario(s) the current spec still has: "A human-authored pull request is never approved by tier 1 alone", "A gate-integrity path is never approved autonomously". Copy them into the MODIFIED block (a MODIFIED requirement replaces the whole block, so archive refuses to drop them).
  Remedy for each: FIX IT, or DISPOSITION IT in contracts/openspec-cli-pin.yaml with a canon citation (`cited_to:`, non-empty) and an authority (`ratified_by:`). An undispositioned ERROR is not a tolerated one, and a disposition with no citation is refused rather than read as 'none needed'.
exit 1
```

**This is the hard constraint.** After this packet lands as D, codexFactory
must not advance its declared pin to D or later unless the same pull request
carries both re-derivations.

---

## 4. Both siblings re-derived, the pin on `main`: exit 2, both stale

The tree is a copy of the § 2 clone with both sibling blocks re-derived by a
MEASUREMENT SCAFFOLD. **It is not the proposed text.** The scaffold is the
lane's `tools/rederive_scenarios.py` (from the pre-stage), run under
`python3 -I`. It swaps the pre-archive scenario for canon's two current
scenarios, copied verbatim. The body rebase that the real re-derivation also
owes is content the checker does not read, so it was not attempted here. The
scaffold's whole diff:

```
$ python3 -I <…>/rederive_scenarios.py <cxf-sim> extend-merge-master-envelope-to-floor-bot-lanes
extend-merge-master-envelope-to-floor-bot-lanes: replaced 4 lines with 10
$ python3 -I <…>/rederive_scenarios.py <cxf-sim> relocate-review-authority-floor
relocate-review-authority-floor: replaced 4 lines with 10
$ git -C <cxf-sim> diff --stat
 .../specs/merge-master-approval/spec.md                        | 10 ++++++++--
 .../specs/merge-master-approval/spec.md                        | 10 ++++++++--
 2 files changed, 16 insertions(+), 4 deletions(-)
```

In each block, `#### Scenario: A human-authored pull request is never
auto-approved` and its two bullets become canon's `… never approved by tier 1
alone` (three bullets) and `A gate-integrity path is never approved
autonomously` (two bullets).

```
$ … --repo <cxf-sim> --all --strict --pin <pin on main>
…
Totals: 35 passed, 2 failed (37 items)
openspec-cli-pin: DISPOSITIONED FINDINGS in codexFactory (2 applied) — this run is NOT a clean tree:
  ✗→D amend-composition-selector-labelling / domain-hermes-content/spec.md
  ✗→D relocate-review-authority-floor / repository-gate-floor/spec.md
REFUSE pin-disposition-stale: the pin disposes findings this run did not produce:
  • extend-merge-master-envelope-to-floor-bot-lanes / merge-master-approval/spec.md (repo codexFactory)
  • relocate-review-authority-floor / merge-master-approval/spec.md (repo codexFactory)

The condition each was granted for no longer occurs — typically because the change archived out of the `--all` corpus, or because the pinned CLI now words the finding differently. A suppression that outlives its condition is a standing exemption nobody re-read, so it is REFUSED rather than tolerated: delete the entry from `dispositions:` in contracts/openspec-cli-pin.yaml, in a change that says the condition is gone
…
exit 2
```

This is the refusal both entries' `retires_when:` predicted. It is also why a
re-derivation cannot land in codexFactory first: codexFactory would read it
against a pin that still carries the entries.

---

## 5. Both siblings re-derived, this packet's pin: exit 0, 2 applied

```
$ … --repo <cxf-sim> --all --strict --pin <this packet's pin>
…
Totals: 35 passed, 2 failed (37 items)
openspec-cli-pin: DISPOSITIONED FINDINGS in codexFactory (2 applied) — this run is NOT a clean tree:
  ✗→D amend-composition-selector-labelling / domain-hermes-content/spec.md
  ✗→D relocate-review-authority-floor / repository-gate-floor/spec.md
OK openspec-cli-pin: @fission-ai/openspec@1.12.0 verified against its content address; every target validated --strict with 0 UNDISPOSITIONED failures. THIS IS NOT A CLEAN TREE: 2 finding(s) are ACCEPTED EXCEPTIONS, named above.
exit 0
```

**This is the end state codexFactory #549's second advance must reach.**
`relocate-review-authority-floor`'s `repository-gate-floor/spec.md` entry is
still matched and applied. Re-deriving the `merge-master-approval` block does
not retire it.

These four runs agree with the lane's pre-stage measurement of 2026-10-09 over
codexFactory `2bc5015d` (its E0, E1 and E2). That measurement used a pin
derived from `93d13d6c` by deleting the same two entries. The runs here use
this branch's own pin over the newer codexFactory `main`.

---

## 6. openxFactory's own tree: the gate is green with this packet in it

The gate's literal invocation (`.github/workflows/openspec-cli-pin-gate.yml`):

```
$ python3 scripts/validate-openspec-cli-pin.py --all --no-cache
…
change/retire-codexfactory-sibling-currency-dispositions
  ℹ [INFO] file: skip_specs is set in .openspec.yaml: change declares no spec-level behavior changes, zero deltas accepted
…
Totals: 114 passed, 1 failed (115 items)
openspec-cli-pin: DISPOSITIONED FINDINGS in openxFactory (1 applied) — this run is NOT a clean tree:
  ✗→D add-chain-attestation / signed-execution-chain/spec.md
OK openspec-cli-pin: @fission-ai/openspec@1.12.0 verified against its content address; every target validated --strict with 0 UNDISPOSITIONED failures. THIS IS NOT A CLEAN TREE: 1 finding(s) are ACCEPTED EXCEPTIONS, named above.
exit 0
```

`--all --strict` (cached install) prints the same `Totals: 114 passed, 1 failed
(115 items)` and exit 0. None of the three codexFactory entries is applied or
stale here, which is the out-of-scope property this packet relies on to land
first.

This packet on its own, with `skip_specs: true` and no `specs/` directory:

```
$ python3 scripts/validate-openspec-cli-pin.py --change retire-codexfactory-sibling-currency-dispositions
…
change/retire-codexfactory-sibling-currency-dispositions
  ℹ [INFO] file: skip_specs is set in .openspec.yaml: change declares no spec-level behavior changes, zero deltas accepted
Totals: 1 passed, 0 failed (1 items)
OK openspec-cli-pin: @fission-ai/openspec@1.12.0 verified against its content address and every target validated --strict clean
exit 0
```

---

## 7. The touched tests

```
$ python3 -m pytest tests/openspec_cli_pin tests/doc-health/test_pin_shape_adapter.py tests/pin_registrations -q -p no:cacheprovider
…
316 passed in 23.80s
```

The whole suite, as `pytest-suite` selects it (`tests/ -m "not postgres"`,
9,532 collected), was run as eight directory shards in parallel, because the
host was shared with another lane's suite. Together the shards cover all 49
top-level entries: **9,511 passed, 23 skipped, 5 failed.** All five failures
reproduce identically on a clean detached checkout of openxFactory `main`
`9a272c6d`, with this packet absent, so none is caused by it:

* four in `tests/factory-mcp/test_factory_mcp_conformance.py` (three
  `test_local_fragments_may_carry_uri_characters` subtests and
  `test_nul_bytes_are_refused_not_raised`);
* one in `tests/hermes_runtime_contracts/test_validator_cli.py`
  (`test_release_mode_field_is_preserved_on_the_real_repository[--require-realization-realization]`),
  a 30-second subprocess timeout. It also times out on the clean checkout,
  with the host load average at 25.

---

## 8. What was NOT measured, said plainly

* **The honest re-derived text.** The § 4 and § 5 scaffold proves the checker's
  reading only. The real re-derivations (the body rebase, the kept `Merged
  into` marker paragraph, relocate- derived from extend-) are codexFactory
  #549's second advance, each on its own owner word.
* **codexFactory's `validate` job** at any advance. That is a codexFactory
  verdict on a codexFactory tree. What is measured here is the
  `openspec-cli-pin` leg, through the same entrypoint that job calls.
* **Any codexFactory commit other than `main` `33b916c1`.**
