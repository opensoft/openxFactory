# Realize `declare-spent-bundle-state`

Realizes `openspec/changes/declare-spent-bundle-state` § 2 (boxes **2.1–2.9**),
ratified 2026-09-02 by Brett Heap in two acts over OD-3 and OD-4; record
`review/ratification-2026-09-02.md`; packet merged as PR #578, squash
`f4fddf7c`, which is this branch's base. Spec Kit feature
[`specs/027-spent-bundle-state/`](../../specs/027-spent-bundle-state/) — the
packet says group 2 is ONE Spec Kit feature and this is it.

**Realizes #575's disposition. The issue stays open until the orchestrator
closes it with the green run id.**

---

## THE ONE THING TO READ FIRST: `pytest-suite` reports exactly 1 failed, and it goes green at the squash

`pytest-suite` reports **exactly 1 failed** —
`tests/doc-health/test_release_tag_publication.py::test_this_repository_reads_zero_and_the_probe_can_fire`,
which reads remote `main`'s `contracts/CHANGELOG.md` via `git ls-remote origin
refs/heads/main` and **cannot see this branch's declaration**; every other test
green; the failure set is **byte-identical to `main`'s since `ff9ed815`**; it
goes green at the squash.

That test is **not edited** — the packet requires it go green *"as a
CONSEQUENCE"* (2.9) — and the post-merge state is **measured, not predicted**:
a bare repository whose `main` IS this branch, cloned, with the unedited
self-gate run against it →

```text
1 passed in 2.02s
```

and the declaration then removed from that origin's `main` →

```text
FAILED …::test_this_repository_reads_zero_and_the_probe_can_fire
1 failed in 1.67s
```

Full transcript:
[`evidence/post-merge-proof.md`](../../specs/027-spent-bundle-state/evidence/post-merge-proof.md).
**`main` goes green because `contract-v2.6` is EXPLICITLY DECLARED spent, and
never because an undeclared bundle started passing** — which is what task 2.1
requires be verified rather than asserted.

## The declaration, exactly as committed (2.1)

ONE line, into the EXISTING `### \`contract-v2.6\` disposition — DECLARED,
NEVER VERIFIABLE, NEVER PUBLISHED, SUPERSEDED HERE` subsection under
`## contract-v3.0`. `contracts/CHANGELOG.md`: **+2 insertions, −0 deletions**.
`contracts/manifest.yaml`, `contracts/releases/contract-v2.6.digests.yaml` and
the `## contract-v2.6` entry are **untouched**.

```text
**SPENT BUNDLE:** `contract-v2.6` — SUPERSEDED BY `contract-v3.0` — CAUSE: it declares change class ADDITIVE (minor) over a tree that refuses three shapes `contract-v2.5` accepted, which no completion commit and no rebuilt inventory can cure, and it is never verifiable at `bbbbeda9`, its one declaring commit — RULED BY Brett Heap, 2026-09-02 — MEASUREMENT: PR #565 comment `5502452624`
```

`contract-v3.0`'s tag was **checked, not assumed**:
`git ls-remote origin refs/tags/contract-v3.0` → `59f4f51f…` peeling to
`ff9ed815…`, so the declaration lands in the `info` band and not OD-4's
`warning` band.

## The finding this buys, and its key

| | |
|---|---|
| severity | `info` |
| family | `release-tag-publication` |
| **path** | **`contracts/releases/contract-v2.6.digests.yaml`** |
| **match key** | `('release-tag-publication', 'openxFactory', 'contracts/releases/contract-v2.6.digests.yaml')` |
| class | `contested` |
| action | *no action is owed on this bundle — the obligation was not MET but EXTINGUISHED, by an owner act, at the cost of a version number, and the record is the reserved SPENT declaration in contracts/CHANGELOG.md; NEVER delete that declaration or this inventory to stop this finding being reported* |

Rule text, as emitted over the real repository at the simulated post-merge tip:

> contract-v2.6 is SPENT: it was cut, was never publishable, and is declared
> spent by the reserved SPENT declaration at contracts/CHANGELOG.md line 374,
> inside the contract-v3.0 entry — contract-v3.0 superseded it and carries a
> published annotated tag on a commit that declares it. Ruled by Brett Heap,
> 2026-09-02; cause: …; measurement of record: … . This is NOT the tag
> obligation having been MET — it was EXTINGUISHED, by an owner act, at the
> cost of a version number

The `error` it replaces held
`('release-tag-publication', 'openxFactory', 'contracts/manifest.yaml')` and
was `auto-fixable`, so its disappearance raises no uncited-resolution; the key
that replaces it is `contested`, so **its** disappearance would.

## What landed, per box

* **2.2 — the reader.** `read_spent_declarations(bytes) -> {bundle:
  SpentDeclaration}`: one pure function, bytes in (the module's existing rule,
  because `blobs_at` answers raw blob bytes), parsing the reserved opener, the
  four elements, and the containing `## contract-vX.Y` entry. It **REJECTS
  rather than skips**: a line beginning with `**SPENT BUNDLE:**` is a
  declaration by construction, and one that does not complete the form comes
  back carrying `missing` or `defect`. Duplicates are **counted, not
  collapsed**.
* **2.3 — the ladder**, in `check_repo`, in the ABSENT arm **only** and
  **after** the `ok`/`lightweight`/`misplaced` branches, each of which
  `continue`s — so *"the SPENT state reaches the ABSENT-tag arm and nothing
  else"* holds **by construction rather than by care**. Seven pure refusals in
  order (duplicate, malformed, missing element, self-declaration, wrong
  containing entry, successor never cut, successor not STRICTLY LATER) in
  `spent_refusal`, then the one git question (is the successor published) in
  `check_repo`, which is also the only place that can turn an unlistable ref
  into a `Skip`.
* **2.4 — the emits.** Every finding of the state lands on
  `contracts/releases/<bundle>.digests.yaml` (OD-5 as amended on Codex's P1:
  `Finding.match_key()` ignores rule text, so the manifest would share one
  identity with everything and the changelog would share one identity between
  two spent bundles); the accepted `info` is `contested`; the orphan-subject
  `warning` keeps the changelog path, having no per-bundle inventory. **Four
  new action constants** beside the module's existing four. `_finding` gained
  `path=MANIFEST` as a **default**, so every pre-existing finding keeps its
  identity byte for byte.
* **2.5 — one read, one commit, one guard.** The changelog joins the manifest
  in the SAME `blobs_at` call at the SAME tip; a blob it cannot read is a
  **SKIP naming that read**, never "no declaration" — the #338 conflation one
  document over, which this family has already been caught by once.
* **2.6 / 2.7 — tests.** 19 → **51** in the family's file (+32: fourteen reader
  tests with no repository, fifteen ladder scenarios over real git fixtures,
  three report-integration proofs). All 13 new scenarios covered, each with the
  positive control the file's convention requires.
* **2.8 — `docs/doc-health.md`** gains the third state, the reserved form, the
  three outcomes, the path rule, the three action lines and the no-retrofit
  rule. **The family-count sentences are untouched** — this change adds no
  family — and `family-enumeration` reports `No findings.`
* **2.9 — `pytest tests/doc-health`**: **1415 passed, 1 failed**, the failure
  being the self-gate above and nothing else.

## The red-first proof (2.1, 2.6)

Not a one-off measurement but the **second half of a permanent test**
(`test_a_superseded_bundle_declared_SPENT_with_a_published_successor_is_an_info`):
the same fixture, declaration removed, must return the superseded `error` on
`contracts/manifest.yaml`. Re-taken over the REAL repository in
[`evidence/post-merge-proof.md`](../../specs/027-spent-bundle-state/evidence/post-merge-proof.md) § B.

**And the order is recorded as taken, not as prescribed.** The module and the
tests were authored in one pass, module first; the red was then demonstrated by
reverting the module against the landed tests, where **not one of the 32 new
tests can even be COLLECTED** (`AttributeError: module
'doc_health.release_tag_publication' has no attribute 'CHANGELOG'`). That is
weaker than a true test-first order and is disclosed rather than smoothed over:
[`evidence/red-log.md`](../../specs/027-spent-bundle-state/evidence/red-log.md).
The packet's § 4.1 baseline was **re-taken rather than quoted** in the same
worktree: **18 passed, 1 failed**, the same test.

## OQ-3 — PROVED, not inherited. It behaves as OD-5 assumed.

`report.plan_line` writes `class="{resolution}"` for **every** finding and
`render` writes a ranked-plan row for every severity; `parse_previous` adds to
`contested` on the class alone, with **no severity test** (the severity test
gates only the regression `keys` set). So a contested `info` joins
`previous_contested` and its disappearance raises an `uncited-resolution`
ERROR. Measured:

```text
contested == {('release-tag-publication','alphaFactory',
               'contracts/releases/contract-v2.6.digests.yaml')}
uncited_resolutions([], contested, dispositions=set())
    -> ['uncited-resolution'] on contracts/releases/contract-v2.6.digests.yaml
```

**OD-5's class choice stands and does NOT return to the owner as a question.**
The complement is pinned too — a CITED disposition silences it — so the proof
cannot be read as "a spent state can never be retired".

## The two-bundle proof — Codex's other P1

Two accepted declarations → **two `info`s, two DIFFERENT match keys**, on
`contract-v2.6`'s and `contract-v2.8`'s own inventories. Withdrawing ONE
declaration raises **exactly one** uncited-resolution, for that bundle alone,
and that bundle is reported again by the superseded arm while the other's
`info` stands. A single-bundle test cannot see the defect Codex found, which is
why this one is written with two.

## verify-commit — exactly two members, and they are different kinds of fact

```text
$ python3 scripts/validate-contract-release.py verify-commit --commit HEAD
HGR-RELEASE-DIGEST-MISMATCH error path=contracts/CHANGELOG.md: …
HGR-RELEASE-DIGEST-MISMATCH error path=docs/contract-versioning-policy.md: …
exit=1
```

| member | whose | class |
|---|---|---|
| `contracts/CHANGELOG.md` | **THIS PR** | **EDITORIAL** — one of the three members the versioning policy allows to move between cuts, so `release-inventory-drift` reports it at `info`, *editorial member — expected between cuts* |
| `docs/contract-versioning-policy.md` | **INHERITED** — PR #577, `2898b104`, already red on `main` | NON-editorial: an unconditional `error` |

The same command at `origin/main` reports the **second one alone**, exit 1 — so
this PR adds exactly one mismatch, on an editorial member, and inherits the
other. **The TAG is unaffected**: `verify-tag --remote origin --tag
contract-v3.0` → `release verify-tag: pass`, exit 0, because the tag verifies
the bundle at `ff9ed815` where nothing moved. That distinction is the whole of
what OD-6 turns on and it is measured here rather than argued.
[`evidence/gates.md`](../../specs/027-spent-bundle-state/evidence/gates.md)

## doc-health before/after — exactly ONE new row

`--single-repo`, same clock, BASE a detached worktree at `f4fddf7c`, HEAD this
branch committed:

| | critical | error | warning | info |
|---|---|---|---|---|
| base | 6 | 6 | 29 | 12 |
| head | 6 | 6 | 29 | **13** |

Ranked-plan rows diffed row by row with the repo-identity string normalized, 53
→ 54 rows, **one addition and nothing else**:

```diff
> - severity=info family=release-inventory-drift path=contracts/CHANGELOG.md rule="bytes differ from the digest 'contract-v3.0' records (editorial member — expected between cuts)" …
```

`family-enumeration`: `No findings.` `modified-block-currency`:
scenario-title completeness `0`, carriage ledger `8` — both unmoved.
**`release-tag-publication` at head still reports the `error`, and that is
correct**: the family reads the published tip, which is `f4fddf7c`. The
`error` → `info` conversion is a **merge-time** event, measured post-merge.
[`evidence/doc-health-delta.md`](../../specs/027-spent-bundle-state/evidence/doc-health-delta.md)

## Other gates

* `OPENSPEC_TELEMETRY=0 openspec validate --all --strict` → **85 passed, 0
  failed**. The packet keeps `Status: ratified` and is **not archived** —
  § 5 follows the merge.
* `proposal-support.py . verify declare-spent-bundle-state` → **ok**.
* `validate-sequenced-after.py .` → **passed (32 active, 1 declaring)**;
  `pytest tests/sequenced_after` → **118 passed**. **No pin moved**, and
  structurally so: this PR adds no OpenSpec change directory, moves none, and
  authors no MODIFIED block (the block it realizes was authored by #578 and is
  already counted on `main`). The `32` against the packet's `31` is #555's
  landing, already accounted for by whoever landed it.

## One consequence stated rather than hidden

A repository that declares a contract bundle and holds **no**
`contracts/CHANGELOG.md` now **SKIPS** where it previously reported. That is
the ratified fail-closed rule (*"not fetched is not an answer, in either
direction"*) and it is why the test file's `_declare` now seeds a changelog
into every fixture: a fixture with no changelog is one the family declines to
judge, which would have made every other assertion in that file vacuous. Two
smaller residues are named in
[`plan.md`](../../specs/027-spent-bundle-state/plan.md) § D6.

## OpenSpec § 3.1 — ROUTED, not discharged, and left unticked

`docs/contract-versioning-policy.md` is **NOT edited by this PR.** It is a
non-editorial member of `contracts/releases/contract-v3.0.digests.yaml`, and
**the repository owner ruled on 2026-09-02 that #577's existing drift on that
file CARRIES TO THE NEXT CUT and that this realization's pre-authorized scope
is "editorial member; no drift."** The obligation-side paragraph — the
versioning policy naming SPENT as a state and its reserved declaration form, so
a consumer reading the pinned policy can find the state without reading
doc-health — **stays owed at the next contract cut**. Box 3.1 is left open with
a dated one-sentence note recording that routing.

OD-6's zero-incremental-cost arithmetic is **accepted as arithmetic and
declined as authority**: it says the edit would cost nothing, not that this
realization was authorized to make it. What #577 already discharges — a
consumer of the pinned policy learns `contract-v2.6` is superseded and not
dischargeable — is **not re-authored** here: *"two records of one measurement
is how they drift apart."*

## Nothing else relaxed

Threshold still **five**. Floor still **`contract-v1.7`**. MISPLACED and
LIGHTWEIGHT untouched and explicitly beyond the state's reach (two tests).
The declared bundle's distance grading untouched (and a declaration naming it
is an `error` that does not stop the grading). The five bundles under
§ *Untagged Bundles After Enforcement Began* not retrofitted, nor any bundle
below the floor (one test asserting `findings == []`). No new family, no change
to `Finding`, `report.render`, the finding or ranked-plan grammars,
`health/dispositions.yaml` or its readers, `release-inventory-drift`,
`verify_tag`, or any other family.

---

Files: `contracts/CHANGELOG.md` (+2/−0),
`scripts/doc_health/release_tag_publication.py`,
`tests/doc-health/test_release_tag_publication.py`, `docs/doc-health.md`,
`openspec/changes/declare-spent-bundle-state/tasks.md` (boxes 2.1–2.9 ticked;
3.1 left open with its routing note), and the Spec Kit feature under
`specs/027-spent-bundle-state/`.
