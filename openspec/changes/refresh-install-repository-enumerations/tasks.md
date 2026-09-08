# Tasks: refresh-install-repository-enumerations

Status: draft
Lane: openxfactory-3 (openXfactory-3)

**EVERY BOX BELOW IS UNTICKED, AND THAT IS THE STATE OF THE PACKET RATHER THAN
AN OVERSIGHT.** This is a PROPOSAL. No promoted specification byte moves, no
`## Purpose` is edited, no issue is closed, no ledger row is claimed as final
and no repository is touched anywhere in the estate. The six `## MODIFIED`
blocks and the one `## ADDED` requirement under `specs/` are a proposal ABOUT
canon; canon is written by the archive act, which is § 4.

## 1. Ratification (Brett Heap's act, not this lane's)

- [ ] 1.1 Ratify this packet. Brett Heap's word on the pull request or on
      openxFactory#796; the packet is `Status: draft` until then. His word of
      2026-09-08 (*"do 794, 795 and 796"*, recorded on openxFactory#591)
      ADMITTED the work and ratifies no text: it names no option, no
      requirement wording and no scope.
- [ ] 1.2 The three veto points are put to him verbatim in the pull request
      body and stand or fall on their own:
      - **D1** — widen the enumerations and state the index rule
        (recommended), against replacing the hand lists with a list derived
        from the aggregation's `installs/` mount list. Refused on the
        nine-against-five measurement; the derived option is recorded as NOT
        TAKEN rather than foreclosed.
      - **D3** — the SIX-MODIFIED scope. **TWO** widened units are absent
        from #796's list, both `WHEN` bullets in `repo-boundary-governance`:
        *"Canonical workflow authority"* and *"Copy-first migration"*.
        Refusing it means deleting exactly those two MODIFIED blocks; the
        `canonical-contract-migration` delta STAYS, because that widening is
        #796's own item 2 under the corrected reading, not extra scope.
      - **D5** — the OPEN-ENDED widening of *"Submodule sequencing"*, the one
        place a closed five-name list would be wrong.
- [ ] 1.3 On ratification, flip `Status: draft` to `Status: ratified` in
      `proposal.md`, `design.md` and this file, add the `Ratified:` /
      `Ratified by:` lines naming the word and its date, and write
      `review/ratification-<date>.md` as `Status: record`. **Ratification
      performs no realization**: no delta is promoted, no Purpose is widened,
      no box in § 3 or § 4 ticks on it, and #796 stays open.

## 2. Authoring and validation (this lane's act, done before the pull request)

These boxes tick on the pull request, not at the archive, because they are the
evidence the packet is reviewable at all.

- [ ] 2.1 Three spec deltas authored, BUILT from the promoted text
      programmatically rather than retyped, so no unit is dropped by
      transcription: `specs/repo-boundary-governance/spec.md` (3 MODIFIED +
      1 ADDED), `specs/shared-contract-ownership/spec.md` (2 MODIFIED),
      `specs/canonical-contract-migration/spec.md` (1 MODIFIED).
- [ ] 2.2 Every MODIFIED block carries a
      `**Removed from canon by refresh-install-repository-enumerations
      (2026-09-08):**` marker naming the replaced sentence or bullet as a
      CommonMark code span, fenced with a longer backtick run where the unit
      itself contains backticks, and a reason beginning at the first ` — `
      standing outside every span. Verified by parsing each marker with
      `scripts/doc_health/modified_block_currency.py`'s own `parse_marker`, so
      the names the checker will read are the names the author intended.
- [ ] 2.3 `.openspec.yaml` carries the ad-hoc origin declaration written by
      `scripts/proposal-support.py . declare-adhoc` with DRAFTING provenance
      only (`proposed_by` + `proposed_on`, no `approved_by`, no `approved_on`)
      — the lawful unapproved shape `add-drafted-proposal-origin` defined.
- [ ] 2.4 One row added to README's *"OpenSpec Records"* active-changes block.
      That block is substrate-claimed on openxFactory#630 for THIS ONE ROW;
      nothing else in README is touched.
- [ ] 2.5 One row seeded into `tests/sequenced_after/corpus-ledger.yaml` by
      `scripts/validate-sequenced-after.py . --seed-ledger --moved-by '#<PR>'`.
      Measured shape: `{state: active, class: co-modifier, declares:
      [admit-install-repos-to-aggregation], depth: 1, prose: false}` —
      `co-modifier` because the ledger's corpus includes ARCHIVED changes and
      that one wrote the same key in August, NOT because a live change collides
      (D2). The diff is the check: any OTHER row that moves is a collision this
      packet did not predict and must be explained before merge.
- [ ] 2.6 Validation run and reported in the pull request body, every command
      and result: `openspec validate refresh-install-repository-enumerations
      --strict` and `--all --strict` (the two pre-existing failures,
      `add-chain-attestation` and `add-composed-view-authoring`, are unrelated
      and are named as the accepted baseline); `validate-openspec-cli-pin.py
      --all`; `proposal-support.py . verify refresh-install-repository-enumerations`;
      `validate-sequenced-after.py .` and `--ledger-diff`;
      `doc-health.py --single-repo . --fail-on error`; the
      `tests/sequenced_after` and `tests/proposal-support` suites;
      `git diff --check`.

## 3. What is NOT done by this packet, stated so no tick can claim it

- [ ] 3.1 **No promoted specification is edited.**
      `openspec/specs/repo-boundary-governance/spec.md`,
      `openspec/specs/shared-contract-ownership/spec.md` and
      `openspec/specs/canonical-contract-migration/spec.md` are UNTOUCHED by
      this packet's diff. Verified by `git diff --stat` naming no file under
      `openspec/specs/`.
- [ ] 3.2 **No generator, checker, script, workflow or test is written.** D1's
      refusal of the derived option is the reason, and D4 states it: a rule and
      its checker landing in one act is how this estate has shipped rules a
      checker's shape quietly narrowed. If a checker is ever wanted, its input
      is the ADDED requirement's declared-filter obligation.
- [ ] 3.3 **No contract is added, changed or cut.** `contracts/manifest.yaml`,
      `contracts/README.md` and `contracts/CHANGELOG.md` are untouched, no
      digest inventory moves, no `contract_bundle_version` is allocated or
      reserved, and no annotated tag is owed.
- [ ] 3.4 **No repository is created, admitted, renamed, re-pinned or
      retired**, and no submodule pointer moves in any repository. The fifth
      repository's creation and admission ALREADY HAPPENED —
      `opensoft/OmniWorker-Install` created 2026-09-05T16:15:48Z,
      admitted by opensoft/xFactory#274 → `648c8bd3` — and this packet only
      writes those facts into the index.
- [ ] 3.5 **The two sites named as candidates are NOT edited and no issue is
      filed for them by this packet**: `contracts/README.md` line 18 (an
      editorial release-inventory member, whose edit would put a
      `release-inventory-drift` finding on `main` until the next cut) and
      `docs/repo-boundary-pilot-plan.md` line 100 (a dated historical record).
      Both are listed in `proposal.md` § *What it does NOT change* as
      unclaimed.
- [ ] 3.6 **`Install repo scope links` is NOT widened.** It is D2's one real
      collision with `implement-keycloak-install-repo` and
      `implement-openxpki-install-repo`, both ACTIVE, and the fifth
      repository's equivalent obligation is already promoted in *"OmniWorker
      install repository boundary"*'s own first scenario.

## 4. Owed at the archive (the archive act, on a separate word)

`code_surface: none`, so per `release-realization` this change archives ON
LANDING rather than on merged-plus-green realization evidence. These three boxes
tick in the archive commit itself.

- [ ] 4.1 **THE `## Purpose` WIDENING — OWED HERE BECAUSE IT CANNOT TRAVEL IN A
      DELTA.** `openspec/specs/repo-boundary-governance/spec.md`'s `## Purpose`
      names `openxFactory`, `Hermes-Install` and `Omnigent-Install` and has not
      moved since `9ebceeff` (2026-06-26), while the capability now governs
      five install repository boundaries. A `## Purpose` in a change's spec
      delta is read ONLY at capability creation and is ignored on any later
      archive, so this edit is made in the PROMOTED specification, in the
      archive commit, in a hunk SEPARATE from the promotion — the shape
      `publish-openspec-cli-pin-as-contract-member` § 5.8 used at its own
      archive on 2026-09-08 (`d712ce29`) for the `neutral-product-pin`
      Purpose. The proposed sentence, so the edit is reviewable BEFORE it is
      taken rather than only in a diff:

      > Defines how `openxFactory`, `Hermes-Install`, `Omnigent-Install`,
      > `Keycloak-Install`, `OpenXPKI-Install`, and `OmniWorker-Install` assign
      > canonical workflow policy ownership, install repository scope,
      > copy-first migration rules, and guarded repo-boundary execution.

      **THE SERIAL COMMA IS CANON'S AND IS PRESERVED.** The promoted Purpose
      reads `` `Hermes-Install`, and `Omnigent-Install` `` — a comma before the
      final conjunction — so the widening keeps one before the fifth name
      rather than silently restyling the sentence it promises only to extend.
      **AND THE EDIT IS STATED EXACTLY, BECAUSE IT IS NOT A PURE INSERTION AND
      CANNOT BE.** Measured character by character against canon: three names
      are appended to the list AND the conjunction `and ` moves from before
      `Omnigent-Install` to before `OmniWorker-Install`, which is what
      extending a serial list requires — the conjunction belongs to the LAST
      item, whichever that is. Those two are the whole edit. Every other
      character of the sentence, the serial comma's position relative to the
      final `and` included, is byte-identical, and no other clause of the
      `## Purpose` block is touched.
      **NOTHING ELSE IN THE `## Purpose` BLOCK IS TOUCHED** — no clause is
      reworded, reordered or removed, only the enumeration widens — and **no
      promoted requirement's text is edited by it.** No `Removed from canon by`
      marker is owed: a Purpose is prose ABOUT the capability, carries no
      SHALL, and is not a canon unit. The tick MUST quote the sentence as
      written so the act is on the record.
- [ ] 4.2 **Close openxFactory#796** with the archive commit named, and record
      in the closing comment which of its four enumerations were widened
      (1, 2 corrected, 3 and the two unlisted bullets), which was taken as
      § 4.1's owed act (4), and the one correction to the issue's own text —
      `canonical-contract-migration` names `Hermes-Install` nowhere, so its
      in-scope unit is the *"Contract breaks an adapter"* runtime-adapter
      trigger rather than a repository pair. Closing it is an act on the
      recording: the issue closes because the enumerations moved, not because a
      successor was named.
- [ ] 4.3 Re-seed the sweep-ledger row at the archive (`state: active` →
      `state: archived`) and re-run `--ledger-diff` clean at the head the
      archive record cites.
