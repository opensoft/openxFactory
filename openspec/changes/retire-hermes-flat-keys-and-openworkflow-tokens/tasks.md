# Tasks: retire-hermes-flat-keys-and-openworkflow-tokens

**NOTHING BELOW SECTION 1 IS PERFORMED BY THIS PROPOSAL, AND RATIFICATION DOES
NOT CHANGE THAT.** The packet is `Status: ratified` — Brett Heap, 2026-09-01,
in session, at pull request #551 tip `64907604`; record
`review/ratification-2026-09-01.md` — and this is still the
OpenSpec-before-implementation stage: no retirement code, no policy row and no
changelog entry lands in the pull request that carries it. **Ratification
authorizes the requirement text and performs none of the work below.** Sections
2-5 are the realization, and § 7 is the archive gate that the realization must
clear before this change may archive at all.

## 1. Proposal (this pull request)

- [x] 1.1 Author the packet — `proposal.md`, `design.md`, `tasks.md`,
      `.openspec.yaml`, and the `contract-deprecation-execution` delta — off
      `origin/main`, citing issue #522, Brett's 2026-09-01 ruling comment on it,
      and the measurement memo.
- [x] 1.2 Re-verify the memo's facts against the tree rather than carrying them.
      Recorded in `proposal.md` § "What the measurement found": FIVE findings the
      memo did not carry — the fallback retirement being a REPLACEMENT and not a
      deletion (a bare deletion widens silently at a major); the `openworkflow`
      branch's SHADOWING (it widens one case as well as narrowing another);
      entry 2's entry under-declaring its own prefix by one character, raised in
      review of this PR; the `Owner layer constraint` canon/code severity
      divergence; and the `hermes.domain_overlay` vs `omnigent.domain_overlay`
      path collision.
- [x] 1.3 Validate: `OPENSPEC_TELEMETRY=0 openspec validate
      retire-hermes-flat-keys-and-openworkflow-tokens --strict` and
      `--all --strict`, both green.
- [x] 1.4 List the change in README § OpenSpec Records.
- [x] 1.5 **RATIFIED by the repository owner** — Brett Heap, 2026-09-01, in
      session ("ratify #551 and #552"), at pull request #551 tip `64907604`, on
      an orchestrator's report of the two packets read together. Record:
      `review/ratification-2026-09-01.md`. Ratification authorizes the
      requirement text and performs none of the realization below.
- [ ] 1.6 **Adversarial review to convergence — STILL OPEN, and the order this
      box originally stated was INVERTED by events rather than met.** It was
      written as "review to convergence, THEN ratification"; what happened is
      that six Copilot rounds ran and every finding was taken, while **every one
      of four `@codex review` requests returned a PROVIDER USAGE-LIMIT REFUSAL
      and no verdict**. The absence was disclosed to Brett and he ratified
      against it. **A CODEX PASS REMAINS OWED and is blocked by nothing in this
      packet**; whatever it returns routes to the amendment lane, not to doubt
      about the ratification.

## 2. Speckit F1 — the validator retirements

**One feature, both retirements, because they are one file and one class.**

- [ ] 2.1 `scripts/validate-domain-factory.py`: delete `LEGACY_HERMES_KEYS`
      (`:60-70`) and REPLACE the `else` arm of `check_hermes` (`:189-200`) —
      the warn line, the flat-key resolution loop, and the per-role
      `no overlay resolvable` check — **with an explicit error**.
      **DO NOT SIMPLY DELETE THE ARM.** The `hermes.layers missing required
      role` errors at `:186-188` sit INSIDE the `if isinstance(declared, list)`
      branch, so a bare deletion leaves a `layers`-less stack falling straight
      through to `for role, layer in layers.items()` with an EMPTY map and
      producing no finding at all — a silent WIDENING at a major, and the exact
      opposite of the retirement. The replacement is one error naming the
      missing or non-list `hermes.layers`.
- [ ] 2.2 `scripts/validate-domain-factory.py`: delete the
      `if token.startswith("openworkflow")` branch (`:309-311`), leaving
      `elif token not in allowed` (`:312-314`) as the only arm — which means
      converting it to an `if`. Delete the docstring line at `:26`.
- [ ] 2.3 Verify the widening at 2.2 rather than assuming it: a gate whose
      `owner_layer` normalizes to a DECLARED layer's display name and begins
      `openworkflow` validates silently after the change and warned before it.
      This is a real behaviour change and it goes in the Executed row.
- [ ] 2.4 `scripts/apply-domain-starter.py`: delete the comment at `:241` and
      the nine emitted flat keys at `:242-250` from the `stack.yaml` template.
      **Do not touch `omnigent.domain_overlay` at `:253`** — same key name,
      different block, not deprecated, and read by the validator at
      `scripts/validate-domain-factory.py:539-541`, which errors when the
      directory it names is missing.
- [ ] 2.5 Tests: the fallback branch has NO existing coverage (grep for
      `LEGACY_HERMES_KEYS` outside the validator returns nothing). The
      realization adds coverage for the post-removal behaviour in both
      directions — a `layers`-declaring stack unchanged, a `layers`-less stack
      refused, a co-resident stack still accepted with no new warning — plus the
      two `openworkflow` cases, plus a starter-output assertion that no
      deprecated flat key is emitted.
- [ ] 2.6 Run `python3 scripts/validate-domain-factory.py <repo>` against all
      five supported consumers from the candidate checkout and record the output.
      The expected result is that nothing changes for any of them; a changed
      line in any one of them is a finding about this retirement, not about that
      consumer.

## 3. Speckit F2 — the policy rows

**The record-why is HERE, and it is the mechanism's own section — not
`health/dispositions.yaml`, which lives at the aggregation root, suppresses
doc-health findings by path, and is unreachable by a consumer reading a pinned
policy document.**

- [ ] 3.1 `docs/contract-versioning-policy.md` § Deprecations Executed: add the
      `openworkflow`-prefixed token row, **with its declared shape CORRECTED to
      the prefix the code matches** — the entry and the validator docstring both
      write `openworkflow_`, the code writes
      `token.startswith("openworkflow")`, so `openworkflow`, `openworkflowx` and
      `openworkflow-legacy` are all refused and none is declared. Carry all six
      elements the one exemplar row
      establishes — the shape removed enumerated, REMOVED at `contract-v3.0`,
      `contract-v1.1` named as the release that served the warnings, the
      conformance-validator clause's discharge, the migration to `xfactory` with
      a reference a post-removal reader can still follow, and the closing
      `Deprecated at contract-v1.1, removed at contract-v3.0.` **Include the
      widening from 2.3**; a row that recorded only the narrowing would be
      accurate about the wrong half.
- [ ] 3.2 § Deprecations Executed: add the `hermes` flat-key FALLBACK READ row,
      with the same six elements, scoped explicitly to the fallback read and NOT
      to the keys.
- [ ] 3.3 § Deprecations Currently In Force: REWRITE the `hermes` flat-key entry.
      It (a) enumerates the refusal list by PATH — the nine keys under `hermes:`
      that `LEGACY_HERMES_KEYS` carries, plus the three the starter emitted
      (`domain_agent_mixes`, `client_agent_mixes_template`,
      `customer_agent_mixes_template`), explicitly excluding
      `omnigent.domain_overlay`; (b) records the reason it stays, in the
      mechanism's vocabulary and with the measurement behind it — the warning
      fires only when `hermes.layers` is absent, all five supported consumers
      declare `layers`, so the co-resident shape has never produced a warning
      and refusing it would be an unphased narrowing; (c) names the deprecating
      minor it owes; and (d) restates the removal target as
      `contract-v4.0`, preserving the section's `removal target contract-vX.Y`
      formula so a target still parses from the bullet.
- [ ] 3.4 § Deprecations Currently In Force: remove the `openworkflow_` bullet in
      the same cut that adds its Executed row. An entry MUST NOT sit in both.
- [ ] 3.5 Repair the stale `:250-254` citations in the existing Executed row and
      in the `contract-v2.0` changelog entry — cite the heading (§ Change
      Classes, *Breaking (major)*) rather than a line range. The clause now sits
      at `:301-305` and moved once already.

## 4. The `contract-v3.0` cut (a SEPARATE act, listed for completeness)

- [ ] 4.1 `contracts/CHANGELOG.md`: the `contract-v3.0` BREAKING entry —
      migration note, and the Breaking clause's three preconditions each
      discharged and each checkable, on the `contract-v2.0` entry's pattern.
- [ ] 4.2 `contracts/manifest.yaml`: `contract_bundle_version`, and
      `contract_schema_version` per OQ-2's answer at the cut.
- [ ] 4.3 `contracts/releases/contract-v3.0.digests.yaml`: the cut's inventory.
- [ ] 4.4 Follow § Bundle Realization Order exactly: allocate late, move every
      release surface atomically with the code, run every gate against the
      unchanged candidate, land the exact reviewed commit, publish the annotated
      tag, verify from an independently refreshed checkout.
- [ ] 4.5 Decide OQ-1 at the cut: whether this packet and
      `retire-doxbench-chat-turn-v1` ride the same major. Either is legal.

## 5. Post-cut verification

- [ ] 5.1 From a refreshed checkout at the tag, run the validator against all
      five supported consumers again. Expected: identical output to 2.6.
- [ ] 5.2 Instantiate a domain repository from the starter and assert its
      `stack.yaml` carries no deprecated flat key and no spent-target comment.

## 6. Rides along regardless of ratification

- [ ] 6.1 File the `Owner layer constraint` canon/code severity divergence as its
      own openxFactory issue — promoted canon says an unresolvable `owner_layer`
      is a WARNING, `scripts/validate-domain-factory.py:312-314` has made it an
      ERROR since `493fb33d` (2026-07-03), six days before the requirement was
      promoted at `a1a2802b` (2026-07-09). D4 keeps it out of this packet's
      scope; the issue is what keeps it from being lost.

## 7. Archive gate

**This change has a CODE SURFACE, so under `release-realization` it archives
ONLY on merged plus green realization evidence — never on landing.** The
evidence set:

- [ ] 7.1 §§ 2 and 3 merged on `openxFactory` `main`, `pytest-suite` green on
      the merge commit.
- [ ] 7.2 The `contract-v3.0` bundle declared, and its annotated tag PUBLISHED
      and verified from an independently refreshed checkout — a bundle is not
      published until its tag exists, and this packet's target release is that
      bundle.
- [ ] 7.3 `OPENSPEC_TELEMETRY=0 openspec validate --all --strict` green.
- [ ] 7.4 The five-consumer validator run of 5.1 recorded, showing no line moved.
