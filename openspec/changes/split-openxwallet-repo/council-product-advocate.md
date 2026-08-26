Reviewer role: Product Advocate (council review, read-only) — 2026-08-26
Subject proposal: openspec/changes/split-openxwallet-repo/proposal.md

# Product Advocate — `split-openxwallet-repo`

Four concerns, ranked. R1–R8 were treated as LOCKED throughout; every concern
below is about how the proposal CONSTRUCTS a ruling, never about the ruling.

---

## Concern 1 — P3 is unmergeable as drafted: the required token is the JOB ID, and both drafted orderings deadlock (HIGH)

**Concern.** The proposal has P3 delete `.github/workflows/wallet-validation.yml`
and repoint ruleset 21538893 "WITH P3". Neither half can happen.

**Evidence.** `.github/workflows/wallet-validation.yml:6-9` states in its own
words that the check "must surface as exactly `wallet-validation` … the literal
token the ruleset pins", and `:19-20` shows that token IS the job id
(`jobs:` → `wallet-validation:`), not the filename. Ruleset 21538893 requires
that token on `main`. So deleting the workflow means the required check never
reports on P3's OWN pull request — blocked forever. And repointing first fails
because `openxwallet-consumer-gate` does not exist as a reportable token until
some workflow has reported under it once.

**Verdict — VALID, HIGH. Resolve by ALIAS, not repoint.**
`openxwallet-consumer-gate.yml` keeps `jobs: wallet-validation:`, so the token
survives the file rename, ruleset 21538893 is UNTOUCHED by P3, and no operator
act is needed to merge P3. Renaming the token is a named SUCCESSOR (add the new
token alongside the old, land one green pull request under both, drop the old).
The "no gate weakened, no bypass removed" claim is KEPT — it is now true.

**Disposition — APPLIED to `proposal.md`.** § "The REQUIRED check" rewritten to
the alias resolution, naming both unmergeable orderings so neither is
re-proposed; sequencing item 5 replaced with "No ruleset act gates P3"; the
realization row for 21538893 changed to **UNCHANGED**, post-act token
`wallet-validation`, evidence = the unchanged ruleset output PLUS the P3 pull
request's green `wallet-validation` run from the NEW workflow; the token rename
recorded as a successor; `code_surface` and the README `:217-228` note reworded
from "replaced"/"retiring token" to "renamed file, unchanged token"; the "No gate
is weakened" bullet restated as an UNCHANGED-STATE evidence row.

---

## Concern 2 — LedgerxFactory's pin authority is ambiguous the moment two checkouts exist, and the P3→P4 window has none (HIGH)

**Concern.** After P5b the Ledgerx finder resolves a wallet checkout by
filesystem walk-up. Two different gitlinks become reachable, only one of them
governed, and for part of the wave neither exists.

**Evidence.** Ledgerx `stack.yaml:13-14` pins openxFactory `39539fd4…` as a
DECLARED pin. `tests/validate_wallet_estate.py:47-63` (`find_openxfactory()`)
walks up five levels; after P5b it would find the AGGREGATION's root-level
`openXwallet/` gitlink — a different commit from openxFactory's nested
`openxFactory/openXwallet/`, and only the nested one is governed by
`contracts/openxwallet-pin.yaml`. Between P3's merge and P4-plus-`--init`, both
candidates are absent, and `find_openxfactory()` returning `None` is a loud
failure by design.

**Verdict — VALID, HIGH.** Three fixes: the finder resolves nested-first;
`neutral-product-pin` states pin authority and root/nested gitlink equality; P4
lands in the same wave as P3.

**Disposition — APPLIED.** P5a's finder becomes THREE ordered candidates
(`openxFactory/openXwallet/scripts/…` → `openXwallet/scripts/…` →
`openxFactory/scripts/…`); `neutral-product-pin` gains "the pin recorded in the
CONSUMING repository is authoritative and a resolver SHALL prefer it", plus "the
aggregation's root gitlink … SHALL equal openxFactory's nested gitlink commit,
checked in the aggregation"; sequencing item 7 puts P4 (and P3b) in P3's wave,
before LedgerxFactory's next estate run; P5b additionally records the wallet
commit and `wallet-vN.M` in Ledgerx `stack.yaml` so the consumer holds a DECLARED
wallet pin from the cut; P4's evidence row gains the gitlink-equality check.

---

## Concern 3 — Rule (c) calls a `draft` placement "ratified", and the Why never says this is a first (MEDIUM)

**Concern.** `domain-descendant-boundary` rule (c) says a descendant is
aggregated "at one of two RATIFIED placements" and cites `MedxChart`
(2026-08-23) as one of them. The proposal's own ## Why table says
`create-medxchart-overlay-boundary` is `Status: draft`, "a change IN FLIGHT".
The proposal contradicts itself two hundred lines apart, and the contradiction
runs in the direction that overstates the corpus.

**Evidence.** `create-medxchart-overlay-boundary/proposal.md:4` reads
`Status: draft`. DTN-022 (openAvatar/`MedxAvatar`, 2026-08-03) is the only
ratified placement act. Separately: no promoted capability has previously left
this corpus — DTN-022 moved CODE, and this change's own § Removed says its
`## REMOVED Requirements` block is the first in `openspec/`.

**Verdict — VALID, MEDIUM.** Rule (c) must state the standing of each placement
rather than blending them, and the Why must say out loud that the descendant
standard rests on one ratified precedent and rule (c)'s second placement on a
draft.

**Disposition — APPLIED.** Rule (c) rewritten to "two placements, whose STANDING
differs and is stated rather than blended — **RATIFIED:** nested … (DTN-022) …
**REALIZED BUT NOT YET RATIFIED:** the aggregation's `xFactories/` (`MedxChart`
… still `Status: draft`) — permitted here, and confirmed as ratified precedent
when that change archives." ## Why gains the first-of-its-kind paragraph and the
one-ratified-precedent statement, and cites
`add-wallet-carried-review-authority/tasks.md` 8.1 (RULED 2026-08-26; "Cascade
enforcement rides the named core deltas at S5") as the timing evidence the Why
previously only inferred.

---

## Concern 4 — The arc this change unblocks has dangling wallet paths the change does not fix, and the S5 price is never stated (MEDIUM)

**Concern.** The proposal declares ONE `review-authority-intake` modification (a
single scenario's WHEN clause) and leaves the arc's other wallet-path citations
to resolve themselves. They do not. And nowhere does the proposal say what an
`openxwallet` core delta will COST after the cut — which is the one number the
arc's owner needs before ratifying.

**Evidence.** `add-wallet-carried-review-authority/specs/review-authority-intake/spec.md:10`
cites `contracts/openxwallet/openxwallet-custody.registry.yaml:15-37` for the
closed tier ladder; `:15` cites `openspec/specs/openxwallet-agent-profile/spec.md:50-69`
and `:208` cites `:27-48` of the same file — all three resolve into paths that
leave this repository. Its `tasks.md:81`, `:100`, `:134` and `:204` each name
`scripts/validate-openxwallet.py` inside an ACTIVE change. And `tasks.md` 8.1
(RULED 2026-08-26) confirms S5 needs `openxwallet` / `openxwallet-agent-profile`
CORE deltas.

**Verdict — VALID, MEDIUM.** Extend the delta to all three citations, treat the
four `tasks.md` lines as live-change edits, and state the cost.

**Disposition — APPLIED.** The `review-authority-intake` MODIFIED delta now
covers `:10` (registry path → the pin plus the pinned checkout), `:15` and `:208`
(→ openXwallet's own OpenSpec instance at the recorded pin). ## Impact gains a
bullet naming `tasks.md:81`, `:100`, `:134`, `:204` as LIVE-CHANGE edits rather
than record annotations. ## Why gains: "after the cut, an `openxwallet` core
delta … costs a wallet release, an openxFactory pin bump, and a LedgerxFactory
re-pin"; `docs/pin-resync-runbook.md` is the path, and the arc's owner sees the
price before ratification.

---

**Also raised jointly with the Adversary Engineer (his #5):** the wave has no
cutover runbook and the new repository's ruleset cannot be REQUIRED on day one.
Verdict VALID, MEDIUM — see `council-adversary-engineer.md` § Concern 5; applied
as `docs/openxwallet-cutover-runbook.md` in P2's scaffold, plus the register-expiry
and rebase-and-re-verify sequencing items.

**Bottom line.** The doctrine is sound and the boundary is the right one. What
was not sound was the mergeability of P3, the resolver's authority once two
checkouts exist, one overstated precedent, and an unpriced successor. All four
are now written into the proposal, and the second-strongest outcome of this
review is that the change no longer claims codexFactory needs nothing.
