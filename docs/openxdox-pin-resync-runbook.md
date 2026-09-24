# openXdox pin resync runbook — advancing openxFactory's consumption of opensoft/openXdox

Status: draft
Kind: runbook
Repository context: openxFactory
Backed by: `contracts/openxdox-pin.yaml`, whose `resync_runbook:` names this
  document, and its verifier `scripts/verify-openxdox-pin.py`, under the
  promoted [`neutral-product-pin`](../openspec/specs/neutral-product-pin/spec.md)
  capability. Authored on RULED `5815412869` (Brett Heap,
  `opensoft/openxFactory#656`, 2026-09-24, item 3 C4: *"the openXdox-pin resync
  runbook lands as one small PR after review"*), claimed at `5815620605`.

**Why this document is `draft`.** It was authored on a ruling, not ratified by
an OpenSpec change. What it describes is enforced by the two verifiers it names,
not by this text. Where this text and a verifier disagree, the verifier is right
and this document is stale.

This is the resync runbook for openxFactory's OWN consumption of the openXdox
pin. Until it existed, the pin's `resync_runbook:` named
`openXdox/README.md#the-lockstep-invariant` as a stand-in. That section is
openXdox's procedure for pinning ITS legs, not openxFactory's procedure for
pinning openXdox.

## 1. What this governs, and what it does not

`contracts/openxdox-pin.yaml` pins `opensoft/openXdox`, the ASSEMBLY ROOT
mounted as the `openXdox/` submodule, by `commit:` plus one whole-tree digest,
`digests.tree_sha256` (`digest_definition: sorted-ls-tree-r-v1`). It never pins
a leg. `opensoft/openXdox-code` and `opensoft/openXdox-spec` are pinned by the
assembly root's own `contracts/code-pin.yaml` and `contracts/spec-pin.yaml`, and
openxFactory never mounts either (the pin's own comment, on
`split-opendox-two-layer-product` task 5.1). The digest still covers them,
because `git ls-tree -r` records each nested gitlink as `160000 commit <oid>`,
so a leg pin moving inside openXdox changes this digest.

**The sibling pin is related, but it is NOT this procedure.** RULED Q7 (Brett
Heap, `#656` comment `5626248666`, 2026-09-10) gave openxFactory a SECOND direct
pin, `contracts/opendox-pin.yaml`, for `opensoft/openDox`. RULED `5799494355`
(2026-09-23, *"keep the direct arrow, revisit after phase 1"*) kept it. That pin
has its own verifier, `scripts/verify-opendox-pin.py`, whose fifth check holds
it in LOCKSTEP with openXdox's own reading of openDox. § 4 is where the two
interact.

**The carve-time record is elsewhere.** `docs/opendox-cutover-runbook.md` § 7
records how this pin came to exist, once, at the carve. This document is the
procedure for every advance after that.

## 2. What the verifier checks

`scripts/verify-openxdox-pin.py` is the pin's own `verify_pin:`, and
`.github/workflows/openxdox-consumer-gate.yml` runs it on every pull request.
Its `verify()` raises `PinRefusal` on the FIRST failure and never continues past
it. The order matters: a digest recomputed over the wrong revision would report
drift when the real defect is a stale checkout.

- **The pin must be readable** (`load_pin`). An absent file, a parse failure, a
  missing PyYAML, a `digest_algorithm` other than `sha256` or a
  `digest_definition` other than `sorted-ls-tree-r-v1` is `pin-unreadable`. That
  is an environment failure rather than a finding, so it sits outside the
  five-code vocabulary. It still exits 2.
- **The shape guards run before any comparison.** `_pinned_commit` refuses
  `openxdox-pin-tag-only` unless `revision_kind: commit` and `commit` is exactly
  40 hex. A tag, a branch or an abbreviated oid is not a compatibility pin.
  `_pinned_tree_digest` refuses a `tree_sha256` that is not 64 hex.
- **Check 1: the submodule is initialized.** `openXdox/.git` must exist
  (`.exists()`, because a submodule's `.git` is a FILE).
  `openxdox-pin-submodule-uninitialized`.
- **Check 2: the RECORDED gitlink equals `commit`.** `_recorded_gitlink` reads
  the `160000` entry from the INDEX when it has been staged, and from HEAD
  otherwise. `openxdox-pin-gitlink-mismatch`.
- **Check 3: the CHECKED-OUT revision equals `commit`.** This is
  `git -C openXdox rev-parse HEAD`. `openxdox-pin-checkout-mismatch`.
- **Check 4: the tree digest recomputes.** `tree_digest` hashes
  `git ls-tree -r -z <commit>`, split on NUL with empties dropped, sorted
  bytewise, each record followed by `\n`. `openxdox-pin-digest-mismatch`.

Success prints one line, `OK openxdox-pin verified: openXdox@<commit>, gitlink
read from <HEAD|index>, sorted-ls-tree-r-v1 tree digest recomputed (<digest>)`,
and exits 0. Every refusal prints the reason and the REMEDIATION trailer to
stderr and exits 2. There is no exit 1.

The verifier reads the pin, the gitlink and the submodule's object store, and
nothing else: never the network, never openXdox's own `contracts/manifest.yaml`,
never its `contracts/opendox-pin.yaml`. Under RULING F it has no openDox check
and must never grow one. The lockstep in § 4 belongs to the OTHER verifier.

## 3. The advance, step by step

Write the new openXdox assembly-root commit as `NEW_SHA`.

1. **Confirm the upstream is landed.** `NEW_SHA` must be on
   `opensoft/openXdox` `main`. When the bump carries a change to a leg, the
   order is FORCED:
   - the leg pull request lands first (openXdox-code squash-lands, so the landed
     sha is NOT the PR head);
   - then the openXdox root bump lands (its `code` gitlink, `contracts/code-pin.yaml`
     `commit:` and `tree_sha256`, `contracts/manifest.yaml` and
     `contracts/CHANGELOG.md`), pointing at the LANDED leg sha;
   - only then does this pin move.
   openXdox#18 is the precedent: it re-pointed from the PR head `39d8937e` to the
   landed `626f2c8d` before it landed.
2. **Work in a fresh full clone whose directory is named `openxFactory`**, on a
   new branch off `origin/main`. The directory name is not cosmetic: see the
   last point of § 5.
3. **Move the submodule to `NEW_SHA`.**

   ```sh
   git submodule update --init openXdox openDox
   git -C openXdox fetch origin
   git -C openXdox checkout --detach NEW_SHA
   git -C openXdox rev-parse HEAD        # must print NEW_SHA
   ```

4. **Recompute the digest with a second implementation**, independent of the
   verifier's code. `test_the_shipped_digest_is_recomputed_by_an_independent_implementation`
   rests on the same principle:

   ```sh
   git -C openXdox ls-tree -r -z NEW_SHA | python3 -c 'import sys, hashlib
   records = sorted(r for r in sys.stdin.buffer.read().split(b"\0") if r)
   print(hashlib.sha256(b"".join(r + b"\n" for r in records)).hexdigest())'
   ```

   At `2f3f857d` (the pin on 2026-09-24) this prints
   `149dc2cd6701abbacb635718713b01cb172e6eadb2f6a29607212016aa23d1c5`, the
   recorded value.
5. **Edit `contracts/openxdox-pin.yaml`: `commit:` and `digests.tree_sha256:`
   only.**
   - Grep the file for the OLD sha first. A header sentence that names it is
     now false and moves too; #1146 had to correct *"this re-pin advances the
     gitlink … to `646f1dc0`"*.
   - **Keep the file's line count and every line's position.** Other documents
     cite it BY LINE: the promoted `openspec/specs/document-lifecycle/spec.md`
     cites `:76-79,92-94`, and the active `add-neutral-product-standalone-operability`
     design cites `:106-108`. #1146 and #1148 both kept it at 154 lines.
   - `scripts/verify-openxdox-pin.py` is cited by line the same way, from the
     same promoted spec and from `scripts/doc_health/pin_shapes.py`, so a bump
     that also edits the verifier keeps its line numbers too.
6. **Stage the gitlink deliberately**, with explicit paths, never `git add -A`:

   ```sh
   git add openXdox contracts/openxdox-pin.yaml
   git diff --cached --stat               # exactly the paths you mean
   python3 scripts/verify-openxdox-pin.py # "gitlink read from index"
   ```

   `git add openXdox` is the act that records the new `160000` gitlink. It is
   also the act to AVOID after an ordinary `git merge`, where it would stage
   whatever the submodule happens to be checked out at.
7. **Check the lockstep consequence (§ 4) before committing.**
8. **Commit the gitlink and the pin file in ONE commit**, with explicit
   pathspecs. The consumer code the bump makes due goes in the same pull request
   (#1146 and #1148 each carried `scripts/profile_openxfactory.py` and its test).
   Then run § 5.

## 4. The one cross-file consequence: openDox's lockstep check

`scripts/verify-opendox-pin.py` has a fifth check with no analogue in the
openXdox verifier. `_openxdox_derived_commit` reads openXdox's OWN
`contracts/opendox-pin.yaml` as a git BLOB (`git -C openXdox show
<openXdox gitlink>:contracts/opendox-pin.yaml`, the index entry when staged,
HEAD otherwise), never the working tree. It then compares that file's `commit:`
with openxFactory's own `contracts/opendox-pin.yaml` `commit:`. If they
disagree, it refuses `opendox-pin-lockstep-mismatch`.

**So advancing THIS pin can break the SIBLING pin's check without touching the
sibling's file.** If openXdox's derived openDox reading changed between the old
commit and `NEW_SHA`, the refusal fires as soon as the new gitlink is recorded.
Compare the two before committing:

```sh
git -C openXdox show NEW_SHA:contracts/opendox-pin.yaml | grep '^commit:'
grep '^commit:' contracts/opendox-pin.yaml
```

If they differ, the openDox side moves in the SAME commit. That means the
`openDox` gitlink, `contracts/opendox-pin.yaml` `commit:` and `tree_sha256`, and
its `migration:` triple when the openDox bump crosses a migration, following
`openDox/README.md#the-lockstep-invariant` and `docs/opendox-cutover-runbook.md`
§ 7 (*"whichever side is stale is re-pinned in one commit"*).

**Measured history.** openXdox `646f1dc0`, `cd2596a2` and `2f3f857d` all derive
openDox `dc7aa08f`, which equals openxFactory's own pin. That is why #1146 and
#1148 could move this pin alone.

## 5. The gates to run before opening the pull request

Two workflows read this pin on every pull request.

- `.github/workflows/openxdox-consumer-gate.yml` does four things:
  - it runs `git submodule update --init --recursive openDox openXdox`. This is
    RECURSIVE, unlike the verifiers' own remediation, because
    `tests/ideation-dashboard` reaches the legs through `scripts/carved_reach.py`;
  - it runs both verifiers;
  - it runs `pytest tests/opendox_pin tests/openxdox_pin`, whose floors are 105
    selected, 105 passed and 0 skipped, plus four named verdicts, among them
    `test_ruling_q7_two_direct_upstreams_in_lockstep` and
    `test_the_real_pin_is_in_lockstep_with_openxdox_own_derived_reading`;
  - it runs `pytest tests/ideation-dashboard`, whose floors are 1137, 1137 and 0.
- `.github/workflows/pytest-suite.yml` runs the whole suite with `openXdox` and
  `openDox` initialized recursively. Its floors are 7050 selected, 7044 passed
  and exactly 6 skipped.

Measured at openxFactory `main` `dd2466ad`, 2026-09-24, in a checkout whose
directory is named `openxFactory`:
- both verifiers print `OK`, openXdox@`2f3f857d` and openDox@`dc7aa08f`;
- the pin suites pass 105 of 105;
- `tests/ideation-dashboard` passes 1137 of 1137.

**Run the gates from a checkout named `openxFactory`.** In a checkout under any
other directory name, 13 `tests/ideation-dashboard` tests SKIP ("pinned
openxFactory validator(s) not reachable"). The cause is that
`find_cross_reference_validator` walks up the tree looking for
`openxFactory/scripts/...`. The consumer gate then reads red locally against its
`EXPECT_SKIPPED: 0` while CI, which checks out to `openxFactory/`, is green.
Measured the same day.

Every refusal either verifier prints ends with a REMEDIATION trailer. This
pin's trailer names this document.

## 6. The migration triple

The `neutral-product-pin` requirement, as modified by
`split-opendox-two-layer-product`, applies to a pinned product that carries a
database schema and ordered migrations. It requires that product's pin to
declare the migration RANGE a bump crosses, whether the bump is reversible, and
the runbook that performs it. `contracts/opendox-pin.yaml` carries the filled
form:

```yaml
range: "0001..0002"
reversible: false
runbook: "opensoft/openDox-code docs/runtime.md sections 5-6, …"
```

`contracts/openxdox-pin.yaml` carries NO `migration:` field.

On 2026-09-24, `git ls-tree -r --name-only` finds no path containing `migrat`
at openXdox `2f3f857d`, openXdox-code `626f2c8d` or openXdox-spec `f088b097`.
So this pin has nothing to declare yet.

**UNCONFIRMED:** whether the first advance that DOES cross an openXdox migration
is expected to ADD the field here, filled on the sibling's pattern. The trigger
to watch for is the same command returning a hit for the first time:
`git ls-tree -r --name-only <tree> | grep -i migrat`. The openDox pin's own
header records exactly that before/after measurement at its `dc7aa08f` bump.

## 7. Worked examples

- **#1146** moved openXdox `646f1dc0` → `cd2596a2`. It was the upstream root
  bump openXdox#17, of code `195276b7` (openXdox-code #26).
- **#1148** moved openXdox `cd2596a2` → `2f3f857d`. It was the upstream root
  bump openXdox#18, of code `626f2c8d` (openXdox-code #27).
- Each one changed the `openXdox` gitlink, `commit:` and `tree_sha256` in one
  commit, beside the consumer code the bump made due.
- Neither one touched `contracts/opendox-pin.yaml`, because the derived openDox
  reading held at `dc7aa08f` (§ 4).

## 8. The rule in one sentence

**Three things name one commit and move in one commit**: the `openXdox`
gitlink, and this pin's `commit:` and `digests.tree_sha256`. Add openDox's
gitlink and `contracts/opendox-pin.yaml` to that same commit whenever the
advance changes what `openXdox/contracts/opendox-pin.yaml` derives.
`scripts/verify-openxdox-pin.py` holds the first invariant.
`scripts/verify-opendox-pin.py`'s check 5 alone holds the second.
