# Tasks: admit-code-leg-under-pinned-root

Status: draft

Lane: openxfactory-5 (openXfactory-5)
For: openxFactory [#1150](https://github.com/opensoft/openxFactory/issues/1150)

**WHAT IS OPEN AND WHAT IS CLOSED.** § 2 is CLOSED and was done in this pull
request. § 1 is Brett Heap's: his word of 2026-09-24 RULES D1 and ratifies the
packet on a condition this draft has not yet met, so § 1 stays unticked until
that condition is checked at a named head. §§ 3, 4, 5 and 6 stay OPEN. § 3 is a
LATER pull request, which the ratifying word authorizes to be authored. § 5 is
a SEPARATE act on a SEPARATE word.

## 1. Ratification — Brett Heap's and nobody else's

- [ ] 1.1 **(OPERATOR)** Ratify or refuse `proposal.md` § *The decision, put for
      a veto*, which puts THREE decisions with the recommendation first:
      **D1** the shape — (a) a `gitlink` whose carrier may be a `pinned` row
      admitted by exactly one `pin`, read at the commit that pin names; against
      (b) a sixth admission kind; (c) `run:` lines as workflow evidence,
      rejected; **D4** a row a pinned root's gitlink admits SHALL NOT declare
      `governance: governed` (against leaving the class to the author, and
      against requiring exactly `pinned`); **D6** one `## MODIFIED` block over
      the enumeration requirement alone (against also modifying the membership
      requirement). A BARE RATIFYING WORD takes the packet as encoded, which is
      the recommendation in all three.
      **WORD GIVEN, CONDITION NOT YET MET.** Brett Heap, 2026-09-24,
      approximately 16:52Z, verbatim *"(a) recommended for both, ratify when
      the draft is green"*, given in the lane's terminal to lane
      `openxfactory-5` (session `d7c51922`) BEFORE this pull request existed,
      and recorded as a `RULED` entry against `opensoft/openxFactory#1150` in
      `opensoft/brett-wip` `lanes/log/openXfactory-5.md` at commit `536b7ecf`.
      It names option (a) for D1 — encoded now at `design.md` D1 — and is
      otherwise bare, so D4 and D6 take the recommended option when it applies.
      Its ratifying clause applies only when § 1.4's condition is met.
- [ ] 1.2 **(OPERATOR)** The ratifying word authorizes the REALIZATION (§ 3) to be
      authored as a later pull request. It does not authorize the archive,
      which § 5 governs and which owes its own word on merged-plus-green
      evidence. No merge word is quoted anywhere in this packet: the landing of
      this pull request is a separate act performed by whoever holds it.
- [ ] 1.3 **(OPERATOR)** If D6 is vetoed toward also modifying the membership
      requirement, a second `## MODIFIED` block restating *A declared
      repository is judged for membership against the estate inventory* with
      the third NOT RE-CHECKED case named in its bound sentence and in *An
      inventory row nothing names* is added, and nothing else in the packet
      changes; `design.md` D6 states it so the veto is takeable without a
      re-author.
- [ ] 1.4 **(OPERATOR — THE CONDITION.)** "When the draft is green" is checked
      at a NAMED HEAD of this pull request, not asserted: every check-run on
      that head `completed` with no failure, Copilot's review present AT THAT
      HEAD, and zero unresolved review threads. Only then is the ratification
      applied — `Status: ratified` with a citation on `proposal.md`,
      `design.md` and this file, the approval pair ADDED to `.openspec.yaml`
      beside the unmoved drafting provenance, and the README bullet re-worded —
      naming the head the condition was met at.

## 2. Measurement (CLOSED in this pull request)

- [x] 2.1 **EVERY CARRIER THE WIDENED KIND CAN REACH, READ AT ITS PINNED COMMIT**
      (`design.md` D0.2): the four `pinned` rows admitted by a `pin`. Two carry
      submodules — `openDox` at `dc7aa08f` and `openXdox` at `2f3f857d`, each
      naming a `spec` and a `code` leg — and two carry none (`openXwallet` at
      `f3eb929b`, `openRepoShape` at `e9c4827b`). FOUR legs, none of them
      already a row.
- [x] 2.2 **THE PINNED COMMITS EQUAL openxFactory's OWN GITLINKS** for the same
      roots (`design.md` D0.1), so the supplied tree a caller most naturally
      holds — openxFactory's own initialized submodule — already carries the
      commit the evidence is read at.
- [x] 2.3 **THE REFUSAL REPRODUCED** (`design.md` D0.3): a scratch inventory
      carrying `opensoft/openDox-code` as a `pinned` row admitted by a `gitlink`
      in its root makes `validate-estate-inventory.py --inventory <scratch>`
      exit 2 at `scripts/estate_inventory.py` line 966.
- [x] 2.4 Existence of the four legs checked once (`design.md` D0.4): all four
      exist and are public. The gate never makes this call.
- [x] 2.5 **THE DECLARED POPULATION, THROUGH THE SHIPPED GATE** (`design.md`
      D0.5): 30 readable heads naming 8 distinct identifiers at `1d14fee6`, 31
      at this branch (the one more being this packet's own `openxFactory`), 8
      carried, 0 refused. No head names a leg yet.
- [x] 2.6 **THE ONE NEW HAZARD MEASURED** (`design.md` D0.6): on the git 2.43.0
      build measured, an unguarded object-store read in a `blob:none` partial
      clone fetched the blob from its promisor remote; `GIT_ALLOW_PROTOCOL=none`
      refused it even where the clone's own config allowed every transport —
      THIS IS THE GUARD RELIED ON. `GIT_NO_LAZY_FETCH=1` is a build-dependent
      extra. So the delta's "no network call" is a realization obligation
      with a named test (§ 3.1, § 3.4).
- [x] 2.7 **THE ONE-HOP BOUND MEASURED AT ZERO COST**: none of the four legs
      carries a submodule at the commit its root names (`design.md` D0.2).
- [x] 2.8 **THE DELTA GENERATED FROM CANON'S BYTES, AND ITS CARRIAGE MEASURED.**
      One `## MODIFIED` block over *The estate's repositories are enumerated in
      a governed inventory*, produced by a script that splices four insertions
      and one sentence into canon's block with every splice asserted unique. A
      line diff of canon's block against the delta's shows ONE canon line
      re-wrapped (where the sentence enters the `gitlink` bullet) and 70 lines
      added; all eight canon scenario titles and their bullets are carried. The
      replaced bullet is named in the block's own `Removed from canon by`
      marker. `modified-block-currency`'s verdict at this head is recorded in
      the pull request body's gate section.
- [x] 2.9 Sibling search taken before authoring (`design.md` D8): no active
      writer of either inventory key, no colliding change id, no staging topic.
- [x] 2.10 README "OpenSpec Records → Active changes" bullet added.
- [x] 2.11 Per-change sweep-ledger row seeded from the live corpus through the
      sanctioned command, never hand-written:
      `python3 scripts/validate-sequenced-after.py . --seed-ledger --moved-by '#<PR>'`,
      the diff read as the list of rows this change moved.
- [x] 2.12 Gate transcripts recorded in the pull request body.

## 3. Realization (OPEN; a LATER pull request on the ratifying word)

**NOT ONE BYTE OF § 3 MOVES IN THIS PULL REQUEST.** Each slice states the
FAILS-THEN-PASSES obligation: every new test is written to FAIL against the tree
without its arm, and is shown failing before it is shown passing.

- [ ] 3.1 `scripts/estate_inventory.py`:
      (i) THE CARRIER BOUND WIDENED at load (`design.md` D3): a `gitlink`
      carrier resolves to a `governed` row, OR to a `pinned` row admitted by
      EXACTLY ONE `pin`; an `external` carrier, a `pinned` carrier admitted by
      no `pin`, and a `pinned` carrier admitted by two or more are each REFUSED
      by name, the refusal saying which condition failed. THE ONE-HOP BOUND IS
      CHECKED DIRECTLY: a row already carried by this shape's `gitlink` is
      refused as a further carrier in its own right, whether or not that row
      also carries a `pin` of its own — the check is on the hop, not inferred
      from the pin-admission count above.
      (ii) THE CLASS BOUND (`design.md` D4): a row admitted by a pinned
      carrier's `gitlink` and declaring `governance: governed` is REFUSED at
      load, beside the existing refusal of a `governed` row admitted by a `pin`.
      (iii) THE PINNED COMMIT: read from the carrier row's one `pin` file in
      THIS checkout, through the strict loader, `revision_kind: commit` and 40
      hex or no revision at all (`verify-opendox-pin.py::_pinned_commit`'s
      shape), returned as a value or a reason and NEVER RAISED.
      (iv) THE PINNED-COMMIT READ (`design.md` D5): `<commit>:.gitmodules` out
      of a verified tree's own object store through the existing sanitized,
      time-bounded `_git`, with `GIT_ALLOW_PROTOCOL` set to name no protocol,
      normalized by the same `_GITMODULES_URL_RE` and `normalize_origin`, and
      `None` — never a fetch — where the commit or blob is not local.
- [ ] 3.2 `scripts/validate-estate-inventory.py`: its `--estate-tree` mode, for a
      row whose carrier row is `pinned`, verifies the tree exactly as today and
      then reads the carrier at its pinned commit through § 3.1 (iv), never the
      working-tree `.gitmodules`. A pin naming no commit and a tree that cannot
      produce the commit's `.gitmodules` locally are each NOT RE-CHECKED and
      COUNTED, the report naming the pin and the commit; a leg a verified tree
      does not carry at the pinned commit is a finding, exit 1. Governed
      carriers are read exactly as today.
- [ ] 3.3 `scripts/estate-repository-inventory.yaml`: FOUR rows, `design.md` D7 —
      `opensoft/openDox-spec`, `opensoft/openDox-code`, `opensoft/openXdox-spec`,
      `opensoft/openXdox-code` — each `governance: pinned` and admitted by a
      `gitlink` in its root. The header's `gitlink` definition says what the
      delta now says, and its population note is re-measured with a SIXTH
      command beside the five it records: each pin-admitted `pinned` row's
      `.gitmodules` at the commit its pin names.
- [ ] 3.4 `tests/estate_inventory/test_estate_inventory.py`, one case per new
      scenario class, each FAILING against the unwidened judge first:
      a leg row carried by a pin-admitted `pinned` root LOADS; a `pinned`
      carrier admitted by no `pin`, and one admitted by two, are REFUSED; a leg
      row declaring `governed` is REFUSED; a row carried by a leg (two hops) is
      REFUSED; a verified tree whose pinned commit names the leg is NAMED even
      while its checkout and working `.gitmodules` sit at another revision that
      does not, and a tree whose working `.gitmodules` names the leg while the
      pinned commit does not is a FINDING — together proving the working files
      are never read; a local `blob:none` clone missing the blob is NOT
      RE-CHECKED and the blob is STILL ABSENT afterwards (the D0.6 transcript as
      a test); a pin whose `revision_kind` is not `commit` leaves the leg NOT
      RE-CHECKED; and the live file carries the four rows as § 3.3 states.
      `test_a_gitlink_CARRIER_must_resolve_to_a_GOVERNED_row` keeps every
      assertion — its refused carrier is `external`, still refused — and its
      docstring's clause "or from one it carries as `pinned`" is corrected in
      the same commit, disclosed in the pull request body.
- [ ] 3.5 **NO OTHER FILE MOVES.** `scripts/validate-code-surface.py`, every
      contract member (the two pins are READ), every workflow, every other test
      and every promoted byte are untouched, verified in the realization pull
      request by its own diff.

## 4. Verification (OPEN; taken at the realization head)

- [ ] 4.1 `python3 -m pytest tests/estate_inventory tests/code_surface tests/scope_globs -q`
      green, with the fails-then-passes evidence for § 3.4 in the realization
      pull request body.
- [ ] 4.2 `python3 scripts/validate-estate-inventory.py .` and
      `python3 scripts/validate-code-surface.py .` both exit 0, the first
      reporting 37 rows (26 governed, 10 pinned, 1 external) and 34 `gitlink`
      rows NOT RE-CHECKED on a default run.
- [ ] 4.3 **RE-MEASURED AT THE REALIZATION HEAD, NOT CARRIED FROM THIS
      DRAFTING**: `design.md` D0.1 and D0.2 re-run (a root re-pinned between
      drafting and realization moves the commit the evidence is read at, and
      any leg that moved is DISCLOSED here), and one SUPPLIED-TREE run —
      `python3 scripts/validate-estate-inventory.py . --estate-tree
      opensoft/openDox=openDox --estate-tree opensoft/openXdox=openXdox` over
      openxFactory's own initialized submodules — reporting all four leg rows
      NAMED at their pinned commits.
- [ ] 4.4 `pytest-suite` green on the realization pull request at its merge head.

## 5. Archive (OPEN; a separate act on a separate word)

- [ ] 5.1 **(OPERATOR)** `code_surface` is NON-EMPTY, so under
      `release-realization` this packet archives on MERGED-PLUS-GREEN
      REALIZATION EVIDENCE and not on this landing. The archive is a separate
      pull request on a separate word, opened as a DRAFT and landed by MERGE
      COMMIT, never squash, so the archive directory's date keeps matching its
      adding commit.
- [ ] 5.2 **(OPERATOR)** Promote the `## MODIFIED` block onto
      `openspec/specs/release-realization/spec.md` at that archive and at that
      archive only, through the governed wrapper
      (`TZ=UTC python3 scripts/proposal-support.py . archive admit-code-leg-under-pinned-root --yes`),
      never a bare `openspec archive`, with the promoted block hashed on both
      sides.
- [ ] 5.3 **(OPERATOR)** Close openxFactory #1150 THERE, by a closing keyword
      written in the archive pull request's BODY and in no commit message on
      any branch of this change.

## 6. Measured and NOT taken (OPEN; successors, not work owed)

- [~] 6.1 **THE LEG RE-CHECK IS NOT WIRED INTO THE REQUIRED CHECK.**
      `pytest-suite.yml:425` already initializes `openDox` and `openXdox`
      recursively at their gitlinks, so a test could supply both trees and the
      four leg rows would be the first `gitlink` rows the required check
      actually re-checks. Not taken: it is new behaviour of the required check,
      beyond the admission question #1150 asks, and it couples the inventory
      gate to the submodule-init step's success. A successor.
- [~] 6.2 **THE GOVERNED CARRIER IS STILL READ FROM ITS WORKING TREE.**
      openxFactory consumes no governed carrier at a commit, so there is no
      revision to bind its evidence to; binding it to HEAD would only move the
      read from one unconsumed revision to another.
- [~] 6.3 **#1144's HEAD IS NOT RE-POINTED HERE.** `add-neutral-product-standalone-operability`
      names the roots on ruling `5804191141` and says it re-points at the legs
      once #1150 lands; that edit is its holder's act on its own packet, after
      § 3 lands. This lane posts the landing on #1150 and takes nothing in that
      packet.
- [~] 6.4 **A SIBLING READ CARRIES THE SAME LATENT REACH.**
      `scripts/verify-opendox-pin.py::_openxdox_derived_commit` reads a blob at
      a commit with `git show` and no transport refusal, so on a partial clone
      it could fetch (`design.md` D0.6). CI's submodule clones are full, so it
      has not bitten. A different capability's code; named, not taken.
- [~] 6.5 **THE `pin` KIND STILL DOES NOT JUDGE A COMMIT.** Its evidence check
      reads the pin's source field only, so a carrier pin that loses its commit
      leaves the leg NOT RE-CHECKED rather than refused. Widening the `pin`
      check would reach `contracts/openspec-cli-pin.yaml`, whose referent is a
      `package_integrity` and not a commit, and is not this packet's.
- [~] 6.6 **THE PROVIDER IS NEVER ASKED AT THE GATE.** Existence was checked
      once, at the measurement (`design.md` D0.4); every read the delta
      requires is local.
