# Tasks: align-doxbench-contract-pin-to-publisher

All three items land in `scripts/ideation_dashboard/doxbench_contracts.py`.
`serve.py` is not edited — the routes recover because the seam beneath them
starts succeeding.

## 1. Publisher-mode verification

- [x] 1.1 `is_publisher_checkout(root)` — true only when all three markers are
      present together: `contracts/manifest.yaml`, `contracts/schemas/`, and
      `scripts/validate-ideation-dashboard-contracts.py`. All three, because
      any one alone is satisfied by a directory that merely contains a
      similarly named file.
      Landed as `PUBLISHER_MARKERS` + `is_publisher_checkout`; the three
      constants already existed, so nothing new was named.
- [x] 1.2 `verify_stack_pin` returns the publisher verdict instead of raising
      when the hosting repo is a publisher checkout. Keep the consumer path —
      the missing-file, missing-`contract_ref` and drifted-ref refusals — byte
      for byte; this adds a branch above them and rewrites none of them.
      Two lines added above `stack = root / STACK_FILE`; every refusal below is
      untouched and still covered by its original test.
- [x] 1.3 Leave `_verified_bytes` completely alone. It is the whole fail-closed
      chain and the reason publisher mode is safe; a diff here would mean the
      design argument is wrong.
      Zero diff, as intended.
- [x] 1.4 Update the module docstring's three-things-verified list and the
      comment block above the pin: item 3 becomes conditional on the hosting
      repo being a consumer. The rest of both blocks stays true as written.
- [x] 1.5 **Design correction found while implementing.** The tighter same-tree
      rule floated during design (publisher mode only when the RESOLVED checkout
      is the hosting repo) is wrong and was NOT implemented: the declared-pin
      check never compared `stack.yaml` to the checkout, only to `CONTRACT_REF`,
      a module literal — so the digest chain already governs which release gets
      read from anywhere. The tighter rule adds no safety and would break the
      documented `OPENXFACTORY_ROOT=<other released checkout>` rung. Recorded in
      `verify_stack_pin`'s docstring and in design.md so it is not re-proposed.

## 2. Repin to the current release

- [x] 2.1 `CONTRACT_REF` → `e5554028e521d57c7501ef9bac206b20415281ef`,
      `CONTRACT_TAG` → `contract-v1.31`. Record the annotated tag object
      `fc66fa38b999ea15ce74bf00410afe189cc3a5d6` in the pin comment, matching
      how the v1.27 tag object is cited there today.
      The old comment still cited contract-v1.27/`fb912b9a…` beside v1.28
      literals — that staleness is corrected too.
- [x] 2.2 `SCHEMA_DIGESTS` unchanged — verify, do not edit. Both files are
      byte-identical v1.28 → v1.31, and v1.31's own manifest records exactly
      the two digests already pinned. A digest edit here would mean 2.1 was
      done against the wrong ref.
      Verified across all five points (v1.28/29/30/31/HEAD): zero diff.
- [x] 2.3 Note in the pin comment why codexFactory's `stack.yaml` declares
      contract-v1.30 and this does not: it no longer hosts the runtime, so the
      two pins are independent. A future reader will compare them.

## 3. Resolve the running checkout

- [x] 3.1 Insert the publisher rung into `resolve_root` between the
      `OPENXFACTORY_ROOT` override and the walk-up: explicit `root=`, then the
      env override, then the hosting repo when `is_publisher_checkout`, then
      the existing walk, then `ContractPinError`.
      `resolve_root()` now returns this worktree; before it returned the
      aggregation's submodule at `9fe29a2` on another session's branch.
- [x] 3.2 Keep `VALIDATOR_RELPATH` as-is for the walk-up rung — it is correct
      for the aggregation-relative search it was written for, and the
      consumer case still needs exactly that shape.
- [x] 3.3 Confirm the refusal message still names what to do when every rung
      misses; it currently cites `root=` and `OPENXFACTORY_ROOT` and should now
      also make sense from a non-publisher tree.
      Now names the absent publisher markers as well as the absent ancestor
      validator; pinned by `test_resolution_still_fails_closed_with_no_checkout_anywhere`.

## 4. Tests

- [x] 4.1 `test_doxbench_contracts.py`: publisher mode passes with no
      `stack.yaml`; a tree missing any one marker still requires the declared
      pin; a consumer tree with a drifted `contract_ref` still refuses.
      The marker test is parametrized over `PUBLISHER_MARKERS`, so a fourth
      marker cannot be added without gaining coverage.
- [x] 4.2 Resolution preference: with a publisher hosting repo AND a reachable
      aggregation-relative checkout, the hosting repo wins; explicit `root=`
      and `OPENXFACTORY_ROOT` still outrank it.
      The fixture reproduces the REAL layout
      (`aggregation/openxFactory` + `aggregation/openxFactory-worktrees/feature`)
      and asserts the walk-up genuinely would have found the sibling.
- [x] 4.3 The existing cache test that pins "the cache never shortcuts the byte
      verification" must stay green untouched — publisher mode must not have
      become a way past the digest chain.
      Green, zero diff. Two further tests were added for the same property
      (drifted digest, disagreeing manifest) under publisher mode specifically.
- [x] 4.4 A drifted digest under publisher mode still refuses, and the refusal
      text still reaches no response body.
- [x] 4.5 Make the `@released_only` rung runnable from a publisher checkout
      without `OPENXFACTORY_ROOT`, keeping the skip for trees that are neither
      a publisher nor pointed at one. This is the item that converts this whole
      class of break from a runtime 500 back into a test failure.
      Done in both suites. `test_doxbench_contracts.py`: 43 passed, 0 skipped
      (was 39 passed / 4 skipped). `test_doxbench_routes.py`: 130 passed,
      **0 skipped** (was 125 / 5) — see 4.6.
- [x] 4.6 **A stale deferral this change's own repin released.**
      `test_the_outline_only_request_conforms_to_the_released_schema` carried
      `@pytest.mark.skip("DEFERRED until the pin advances…")` naming
      contract-v1.27 and waiting for the G-1 nullability amendment, with an
      explicit signal: "the pin advances to the bundle carrying the amendment —
      then delete this skip". The amendment landed AT contract-v1.28, so the
      signal fired before this change even started; nobody actioned it because
      the released rung the test belongs to was itself opt-in. A skip waiting on
      a signal no one could observe — which is the same failure mode as the 500
      this change exists to fix, one layer up.
      Verified before removing: the packaged outline-only positive carries
      `active_document_path: None` and `validate_instance` returns `[]` at the
      current pin. Skip deleted, assertion unchanged exactly as the deferral
      required; the routes suite now has NO skips at all.

## 5. Gates

- [x] 5.1 `OPENSPEC_TELEMETRY=0 openspec validate
      align-doxbench-contract-pin-to-publisher --strict`, then `--all
      --strict`, both from the `openxFactory/` root.
      Valid; `--all --strict` 58 passed, 0 failed.
- [x] 5.2 `python3 -m pytest tests/ideation-dashboard -q` — check the EXIT
      CODE, never a tailed pipeline. Expect the skip count to DROP by the four
      doxbench released-checkout probes recorded in
      `adopt-neutral-tooling-home` task 2.3; state the new count.
      **2850 passed, 5 skipped, exit code 0** (353s), re-run after 4.6 removed
      the stale deferral. Exit code read directly, not through a pipeline.
      Nine tests that previously skipped now execute: the eight doxbench
      released-checkout probes that wanted `OPENXFACTORY_ROOT` (four in
      `test_doxbench_contracts.py`, four in `test_doxbench_routes.py`), plus
      4.6's deferral.
      The five that remain are environmental and none belong to this change:
      four in `test_aggregation_register_instance.py` (this worktree's parent is
      not the aggregation root — the same four recorded in
      `adopt-neutral-tooling-home` task 2.3) and one empty-parameter-set in
      `test_doxbench_transport.py`. Enumerated with `-rs` rather than assumed.
- [x] 5.3 `python3 -m pytest tests/doc-health tests/notebooklm -q` — unchanged,
      confirming the shared pin module was not disturbed for its other
      consumers. 692 passed, exit 0.
- [x] 5.4 `scripts/validate-ideation-dashboard-contracts.py` over the contract
      family. Repo-tree mode (`--repo . --strict`): 26 family instances
      checked, 0 errors, 0 warnings, exit 0. The seven packaged workbench
      positives each validate (exit 0); under `--strict` two chat-turn
      instances warn "model context unavailable" because no catalog instance is
      paired with them — PRE-EXISTING, and `examples/` and the validator are
      both untouched by this change.
- [x] 5.5 **Live proof, from a browser, not curl:** start the serve from this
      worktree, load doxBench on a real tile, and confirm the model selector
      populates rather than reporting the catalog unavailable. The empty-catalog
      posture is a legitimate success, so the pass condition is "no
      `catalog_unavailable`", not "models are listed".
      Driven with Playwright/chromium against a serve on port 8799 (a second
      serve, so the session's existing one on 8765 was not disturbed).
      Result: `200 {schema_version: 1, kind: workbench-model-catalog,
      models: []}` — the conformant empty-catalog success, which also proves the
      released catalog schema resolved, since the route self-validates the
      envelope against it before sending.
      A/B on the same machine, same browser, same request: the serve whose
      module was loaded BEFORE the fix (port 8765) still answers
      `500 catalog_unavailable`. My serve was then stopped; 8765 verified
      still healthy.
- [x] 5.6 Confirm the aggregation's `openxFactory/` submodule checkout is NOT
      touched by any of this. If a step appears to need it moved, stop — that
      is another session's tree and the whole point of item 3 is that this
      runtime no longer depends on where it sits.
      Still `9fe29a2` on `staging/topology-handoff`, untouched. The diff is
      confined to four files in this worktree plus this change directory, and
      `resolve_root()` no longer reaches that tree at all.

## 6. Bookkeeping

- [x] 6.1 Add the change to the README "OpenSpec Records" active block.
- [ ] 6.2 ~~Mark `adopt-neutral-tooling-home` tasks.md 2.1's tranche-D open item
      resolved~~ — **not done deliberately.** Editing an archived change's task
      ledger rewrites the record of a landed change, and doc-health runs a
      `record-immutability` family. The resolution is instead recorded where a
      reader will actually meet it: this change's proposal, the README entry,
      and the note block in `test_doxbench_contracts.py` that previously carried
      the open item. Confirm this disposition is what Brett wants.
- [x] 6.3 Record the ruling in `docs/ideation-dashboard-session-runbook.md`.
      Landed as a NEW **§2c, "doxBench's two model routes have a FOURTH
      prerequisite"** — not in §0 as this ledger originally said. §0 turns out to
      be the openDox HEADER documented item by item, not a general rulings
      record; §2 is "Prerequisites for the live affordances", and the model
      routes' contract resolution is exactly a fourth prerequisite beside the
      three session conditions. It sits next to §2b, whose
      three-outcomes-not-two shape it follows.
      Carries: the publisher-versus-consumer verification table; that a
      contract failure is SILENT (`500` with no stderr reason) and the one
      command that makes it speak; that an empty catalog is a SUCCESS and
      `console_required` is a different gate; and the week it failed closed.
      The documented diagnostic was run as written — prints
      `contract-v1.31 -> <this worktree>`, exit 0.
      doc-health full run after the edit: **0 new regressions**.
