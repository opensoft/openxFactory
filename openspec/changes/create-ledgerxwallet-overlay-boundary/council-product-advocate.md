# Council — Product Advocate

**Verdict:** PROCEED WITH CONSTRAINTS — the benefit is real and the packet's four
hardest calls (D3's decidable test, D4's delegator, D7's refusal to claim a check
it does not have, D9's same-commit repoint) are right, so the boundary should be
ratified rather than restructured. But the packet materially understates the one
act that carries all its risk — it describes an 822-line validator's relocation
as "exactly three mechanical changes and no rule change" when five of that
file's seven checks are affected and two of them RED or CRASH as specified — and
two `[OPERATOR]` tasks cannot be executed as written, so the constraints below
are binding rather than advisory.

---

## V1. The benefit is real, but the packet argues the weaker half of it

**IMPACT: HIGH**

**EVIDENCE.** The breach is genuine and the code says so in its own words.
`LedgerxFactory/tests/validate_wallet_estate.py:57-63` (on `origin/main`):

> `#    openxFactory/contracts/openxwallet-pin.yaml governs; the`
> `#    aggregation's root gitlink is governed by nothing this repo pins.`
> `#    Resolving that one instead would validate our estate against an`
> `#    unpinned contract version while the bar reported green, and a`
> `#    silent pass is worse than a loud failure. Candidate order is what`
> `#    breaks the tie, so it may not be reordered.`

That is a correctness hazard, not tidiness, and the packet's diagnosis of it is
accurate. **But the hazard is LATENT, not felt.** Candidate 2 cannot resolve
today — the packet itself verifies the aggregation carries no root `openXwallet`
gitlink (`proposal.md:66-67`), so there is exactly one resolvable candidate and
no tie to break. The tie arrives with P4, which the packet correctly says does
not gate P6.

What an operator feels TODAY is different, and it is stronger:
`specs/016-posting-segregation-of-duties/quickstart.md:3-7` —
"Prerequisites: this worktree; **the pinned openxFactory checkout at the
workspace root, with its nested `openXwallet` gitlink initialized**" — and
`quickstart.md:19`:

```
python3 ../../openxFactory/openXwallet/scripts/validate-openxwallet.py . --strict
```

**A developer who clones LedgerxFactory alone cannot run its wallet bar.** The
descendant fixes that, because `git submodule update --init --recursive` inside
LedgerxFactory brings the profile and the product with it. That is a benefit a
person notices on their first afternoon; "in breach of rule 1" is a benefit only
a governance reader notices.

**REQUIRED CHANGE.** Lead `§ Why` with runnability-from-a-standalone-clone and
keep conformance second. It is the same change; it is a better reason, and it is
the reason that survives contact with the person who has to do the work. See V13
for the part of that benefit the packet does not actually deliver.

---

## V2. The moved validator crashes: it reads a `stack.yaml` that will not be there

**IMPACT: HIGH**

**EVIDENCE.** `tests/validate_wallet_estate.py:675-676`:

```python
    with open(os.path.join(REPO, "stack.yaml"), encoding="utf-8") as fh:
        pin = yaml.safe_load(fh)["xfactory"]["contract_ref"]
```

`REPO` is `os.path.dirname(os.path.dirname(os.path.abspath(__file__)))` (`:38`).
After the move, `REPO` is the LedgerxWallet checkout root, which has no
`stack.yaml` — LedgerxWallet is a profile repository and the packet never gives
it one. This is reached unconditionally from `main()` via
`check_pin_reconciliation()` (`:808`) whenever `find_aggregation()` returns a
root with an initialized openxFactory checkout, which is the normal workspace
shape.

The result is an unhandled `FileNotFoundError` — a traceback. The file's own
doctrine, twenty-five lines above the defect, forbids exactly that
(`:650-651`):

> `      * an exit code outside the emitter's documented {0, 1} -- a traceback`
> `        must never read as "observed nothing";`

`tasks.md:137-146` (task 4.3) enumerates "exactly three mechanical changes and no
rule change" — the finder, the estate root, the expected sets. None of the three
touches this line.

**REQUIRED CHANGE.** Either the three-way pin read stays in LedgerxFactory
(V4's split, which is the right answer) or task 4.3 gains a fourth named change:
the `stack.yaml` path becomes a declared input alongside the estate root, with
its own named refusal.

---

## V3. Relocating the DHC REDS the bar arithmetically, in two places

**IMPACT: HIGH**

**EVIDENCE.** `tenants/ledgerxcorp/wallets/` holds exactly five files
(`git ls-tree -r origin/main`): `dhc-lx-create-post-01.yaml`,
`grant-lx-create-01.yaml`, `grant-lx-post-01.yaml`, `wal-lx-creator-01.yaml`,
`wal-lx-poster-01.yaml`. The validator's floor, `:725-729`:

```python
    m = re.search(r"repo scan: (\d+) openxWallet artifact", proc.stdout)
    if not m:
        err("upstream validator output carried no repo-scan count")
    elif int(m.group(1)) < 5:
        err(f"expected >=5 wallet-family records validated, saw {m.group(1)}")
```

Move the DHC out of the scanned tree and the count becomes 4. **RED.**

Second hit, `:745-746` and `:774-776`:

```python
        elif kind == "xfactory_wallet_distinct_holder_constraint":
            constraints[doc.get("constraint_id")] = doc
...
    dhc = constraints.get(EXPECTED_CONSTRAINT)
    if dhc is None:
        err(f"missing distinct-holder constraint {EXPECTED_CONSTRAINT}")
```

`constraints` is built only from `WALLET_DIR` (`:735-746`). After the move the
DHC is not there, so `dhc is None`. **RED again.** And `tasks.md:145-146`
promises `EXPECTED_CONSTRAINT` is "BYTE-UNCHANGED", which is true of the literal
and false of the check that consumes it.

**REQUIRED CHANGE.** Task 4.3 names the scan floor and the constraint lookup as
changes it owns, with the new values stated: the floor becomes 4 (or per-tenant,
per V18) and the constraint is read from the profile's own
`profile/distinct-holder-constraints/` rather than from the estate. Withdraw
"no rule change" — this is a rule change, it is a correct one, and it is
cheaper to admit than to discover at task 6.2.

---

## V4. "Exactly three mechanical changes" is off by an order of magnitude; the honest act is a validator SPLIT

**IMPACT: HIGH**

**EVIDENCE.** `main()` runs seven checks (`:804-810`). Five are affected by a
change the packet describes as three mechanical edits.

*Orphaned by deleting the finder (D5 deletes `VALIDATOR_CANDIDATES` and the
walk):* `FINDER_PROBES`, eight probes at `:304-331`; `_finder_scratch` `:334-349`;
`check_finder_candidates` `:352-374`, whose first assertion is
`if declared != [_NESTED, _AGGREGATION]: err("VALIDATOR_CANDIDATES drifted from
ratified split-openxwallet-repo D9 …")` (`:362-366`);
`check_finder_loud_failure` `:377-401`, which copies `__file__` into a scratch
tree and asserts the string `"failure, not a skip"`; and `main()`'s guard
`:799-803`, the only consumer of module-level `VALIDATOR`.

*Untouched by the packet and broken by it:* `find_aggregation` `:560-595` — **a
SECOND five-level upward walk out of the repository, which the packet never
mentions once** —

```python
    node = REPO if start is None else start
    for _ in range(5):
        node = os.path.dirname(node)
```

plus `FIND_AGGREGATION_PROBES` / `check_find_aggregation_probes` (`:516-557`),
`read_pin_report` (`:404-`), `PIN_VERDICTS` (`:139`), and
`check_pin_reconciliation` (`:598-717`, see V2).

**REQUIRED CHANGE — and it is a cheaper design, not just a safer one.** Split
the file rather than moving it whole:

- **Stays in LedgerxFactory**, as its own `tests/validate_wallet_pin_*.py`:
  `find_aggregation`, `read_pin_report`, `PIN_VERDICTS`,
  `check_pin_reconciliation`, the `stack.yaml` read, and the three-way pin
  agreement. Every one of these is about **LedgerxFactory's** consumption of
  **openxFactory's** bundle — `stack.yaml`'s `xfactory.contract_ref`, not
  `openxwallet` — and reads LedgerxFactory's own files. It is the repository's
  governance surface, not the wallet profile.
- **Moves to LedgerxWallet:** the negative-probe corpora, the ratification pins
  (`ENVIRONMENT_EVIDENCING`, `PLATFORM_VERIFIABLE`), the domain vocabulary, and
  the estate checks.

This is cheaper on four counts: the `tests/validate_*.py` glob covers the
staying half with **no delegator logic for the pin agreement** (D4's entry
shrinks to submodule-resolution and exit-code propagation); V2's crash
disappears because `stack.yaml` is never read from a tree that lacks it; the
ratified 6.2 observation obligation (V6) stays where it can be discharged; and
the deleted finder probes have a home to be rewritten in rather than being
dropped. It also makes `tasks.md:154-156` (task 4.6, "every rule … appears in
EXACTLY ONE file") a property the packet can actually prove, because the split
is by owner rather than by file.

---

## V5. "Coverage is not reduced" is measured with an instrument that cannot see the loss

**IMPACT: HIGH**

**EVIDENCE.** The promise, `specs/ledgerxwallet-overlay-boundary/spec.md:113-114`:

> "The relocation of the Ledgerx wallet profile out of `LedgerxFactory` SHALL NOT
> reduce the coverage the estate had before it"

The instrument, `tasks.md:209-211` (task 6.2): "Baseline count recorded before
and after, so a silently-dropped validator is visible as a count delta."
LedgerxFactory has 17 files matching `tests/validate_*.py`
(`git ls-tree --name-only origin/main -- tests/`), and D4 keeps
`validate_wallet_estate.py` at its path. **The count is 17 before and 17 after.**
A file count cannot see a deleted check.

And checks ARE deleted. `check_finder_candidates` and
`check_finder_loud_failure` pin properties ratified by a DIFFERENT change —
`:385` cites "Ratified split-openxwallet-repo tasks.md 2.3 — 'a loud failure,
never a skip'", and `:360-366` pins the resolution order against "the ratified
spelling (tasks.md 2.1)". Deleting the mechanism does make some of those probes
meaningless; the packet never says which, or what replaces them.

**REQUIRED CHANGE.** Task 6.2's evidence becomes a CHECK-NAME inventory, not a
file count: every check function present before, and for each one either its
post-change name or an explicit "no longer meaningful because the mechanism it
pinned is gone", with the reason. That is a fifteen-minute table and it is the
only artifact that can substantiate spec.md:113.

---

## V6. A ratified observation obligation owed to another ACTIVE change is silently dropped

**IMPACT: HIGH**

**EVIDENCE.** `tests/validate_wallet_estate.py:126-131`:

> `# is the single live consumer of the wallet validator, so if this bar does`
> `# not run the emitter, the entire deprecation window is unobserved by`
> `# anyone and the versioning policy's "at least one full minor release"`
> `# precondition is a formality. This is that invocation.`

and `:601-603`: "Ratified split-openxwallet-repo tasks.md 6.2 — 'so the
relocation warning is OBSERVED by the one live consumer' — and 6.3, whose
evidence is 'the checker's OUTPUT, not the manifest rows'."

That invocation lives inside `check_pin_reconciliation`, which V2 shows crashes
after the move. So P6, as specified, breaks an observation that a ratified and
still-ACTIVE change requires — and the packet's `§ Out of scope` and `§ Impact`
sections do not mention it. The packet is scrupulous about P4, P3b and P5b
(`proposal.md:382-390`); this obligation is the one it misses, and it is the one
that belongs to somebody else.

**CONSTRAINT TO CARRY.** P6 SHALL NOT satisfy task 6.8's realization evidence
until the relocation-emitter observation demonstrably still runs, from whichever
repository owns it after V4's split, with its output in the evidence record.
`split-openxwallet-repo` archives on that observation; P6 must not be the change
that quietly removes it.

---

## V7. Task 6.1 is unsatisfiable: no check will ever report in LedgerxWallet

**IMPACT: HIGH**

**EVIDENCE.** `tasks.md:206-208` (task 6.1):

> `- [ ] 6.1 **[OPERATOR]** Promote the LedgerxWallet ruleset to ACTIVE once a check`
> `      has reported once; tag `lxw-v1.0`.`

Nothing in `tasks.md` §3 or §4 creates a workflow in LedgerxWallet. Task 3.3
scaffolds `README.md`, `CLAUDE.md`/`AGENTS.md` and `.github/CODEOWNERS` — no
`.github/workflows/`. Task 7.4 disclaims a workflow for LedgerxFactory only.
Task 4.6's fork-freedom proof is "A grep-based check, recorded as evidence" —
evidence in the packet, not a reporting check on a PR.

So Brett creates a ruleset in EVALUATE mode at 3.2, and the condition for
promoting it at 6.1 can never occur. He cannot execute this without asking
"which check?" — which is precisely the question this charge exists to catch.

**REQUIRED CHANGE.** Pick one and write it down: (a) add a task creating
LedgerxWallet's first workflow — the natural one is the moved validator plus task
4.6's grep, which would also give the descendant the CI its parent lacks; or
(b) restate 6.1 as "promote to ACTIVE after the first pull request merges", with
no check requirement and the absence recorded as a successor beside the one
already named at `proposal.md:407-415`. (a) is better and is small; (b) is
honest. Neither is what the packet says today.

---

## V8. The remediation string initializes one of the two levels it needs

**IMPACT: HIGH**

**EVIDENCE.** The same command appears three times, identically —
`proposal.md:243-244`, `design.md:184-185`, `tasks.md:173-175`, and normatively
in `spec.md:136`:

> `- **THEN** it REFUSES with a named exit and names `git submodule update --init LedgerxWallet``

That command initializes `LedgerxWallet` and **stops**. The nested
`LedgerxWallet/openXwallet` gitlink — the whole point of the descendant, and the
thing D5 resolves the neutral validator inside — is a second level, and
`--init` without `--recursive` does not touch it. An operator who runs the named
remediation gets: delegator satisfied, submodule present, and then a failure
from the moved validator about a missing
`openXwallet/scripts/validate-openxwallet.py` — a second, different message,
after doing exactly what the first message told them.

The packet's own spec makes this a defect of this capability, `spec.md:139-141`:

> `#### Scenario: A refusal carries no remediation`
> `- **WHEN** a fail-closed path added by this relocation emits a refusal that names no command`
> `- **THEN** the refusal is itself a defect of this capability`

**REQUIRED CHANGE.** `git submodule update --init --recursive LedgerxWallet`, in
all four places. Separately, the MOVED validator owes its own named refusal for
an uninitialized nested `openXwallet` with its own remediation
(`git submodule update --init openXwallet`, run from the LedgerxWallet root) —
task 6.6 proves that path refuses but neither 4.3 nor the spec requires it to
carry a remediation string.

---

## V9. Three cited line numbers are wrong, and one sends the operator to a code fence

**IMPACT: MEDIUM** (but it is the class of error that makes an operator distrust
the whole task list)

**EVIDENCE**, each verified by `git grep` on `origin/main`:

**(a)** `models/protected-surface.yaml:438`, asserted four times
(`proposal.md:371`, `:373` "the single wallet mention at `:438`",
`design.md:357-358`, `tasks.md:200`).
`git grep -n validate_wallet_estate origin/main -- models/` returns exactly one
hit: **`:455`** — `      RED-proven by validate_wallet_estate.py's`. Line 438
reads `      the digest in the same commit, which this surface's`. The
CONCLUSION is right (prose amendment, no digest row — I verified the
`pinned_files` block independently, V-sound item 5); the pointer is wrong.

**(b)** `quickstart.md:15`, asserted at `proposal.md:211-212`,
`design.md:324`, `tasks.md:185`. Line 15 is:

```
```sh
```

The relative validator invocation is **`:19`**
(`python3 ../../openxFactory/openXwallet/scripts/validate-openxwallet.py . --strict`),
and the same path appears again in PROSE at **`:3-7`** as a stated prerequisite.
So quickstart.md carries three references that the relocation changes; the
packet names one, at the line of the fence that opens the block. Task 5.6 is an
instruction to edit a line that contains nothing to edit.

**(c)** `tests/validate_document_estate_surface.py` carries **two** stale
references, not one. Task 5.8 names the allowed-kind registration (`:1121`).
Unnamed: `:1095-1096` —

```
    # (openxFactory/openXwallet/scripts/validate-openxwallet.py) — see
    # find_openxfactory() in tests/validate_wallet_estate.py for the
```

— a pointer to the function this change DELETES, in the same file the packet is
already opening.

**REQUIRED CHANGE.** Correct all three, and make the correcting grep the task's
own evidence: `git grep -n -e wallet-exercise.template -e validate_wallet_estate
-e dhc-lx-create-post-01` returns 28 files, of which the packet's §5 names five.
The other 23 are records and are correctly left alone — but that is a claim the
grep should support explicitly rather than a coincidence.

---

## V10. `profile/custody-posture.yaml` violates the packet's own fork-freedom property — CUT IT

**IMPACT: MEDIUM** · charge 6

**EVIDENCE.** The property, `tasks.md:154-156` (task 4.6):

> "Prove the fork-freedom property D4 names: every rule, threshold, expected set
> and probe corpus appears in EXACTLY ONE file across both repositories."

The posture's facts are ALREADY thresholds in the validator. `:141-142`:

```python
# Ratification pins (proposal Ratification section, 2026-08-08).
ENVIRONMENT_EVIDENCING = {"holder_readable", "isolated_invocable"}
```

and the authority ceiling, `:770-773`:

```python
        tier = ((doc.get("scope") or {}).get("authority_tier"))
        if tier != "act":
            err(f"{gid}: authority_tier {tier!r} exceeds the ratified "
                "environment-evidencing ceiling 'act'")
```

Task 4.4 declares the same two facts again as data, and task 4.5 adds a NEW
check against them — "The validator checks the tenant records against 4.4's
posture" — inside the same file task 4.3 promises has "**no rule change**". Two
declarations of one rule is exactly what 4.6 forbids, and the second one arrives
in the same act that promises to prove the property.

D8 is admirably candid that this is added scope
(`design.md:304`, "**It is a NEW ARTIFACT, not a relocation, and the packet does
not launder it**") and offers the cut in one line (`design.md:319-320`).

**REQUIRED CHANGE.** Take the cut. Move tasks 4.4 and 4.5 to a successor. If the
bench keeps it instead, then `:142` and `:770-773`'s literals MUST move INTO the
posture file and become its readers, and `tasks.md:145-146`'s byte-unchanged
claim must be withdrawn — a posture artifact that duplicates the thresholds it
describes is strictly worse than the comments it replaces, because comments
cannot disagree with code and a second YAML file can.

---

## V11. Task 5.7's notification has no artifact, and task 5.6 forbids the only durable form

**IMPACT: MEDIUM** · charge 3

**EVIDENCE.** `tasks.md:191-192`:

> `- [ ] 5.7 **[OPERATOR]** Tell the window's operator that the two references`
> `      moved, before the window runs. Not a file edit and therefore its own task.`

The window's operator is Brett. `runsheet.md:19-20`: "**BRETT** = authority for
every gate that changes what holds authority." So as written, 5.7 is Brett
telling Brett, with no record, on a procedure whose phases 1-6 have not run and
whose Phase 3 mints real RSA keypairs (`runsheet.md:119-134`). If the window runs
in three months, nothing in the runsheet records that its paths were moved
underneath it.

The runsheet has an established idiom for precisely this, used three times:
`:29` `- P0.1 **SATISFIED 2026-08-08** (Brett: "merge #130 and re-pin"):`;
`:38-40` `**REVISED 2026-08-09**`; and the Phase 1 heading itself, `:63`
`## Phase 1 — … (REVISED 2026-08-09 to the routed form; …)`.

But `tasks.md:189-190` forbids using it: "**LINKS ONLY**: no step, actor, abort
condition or evidence requirement is touched." A dated provenance note is none of
those four things, and the packet's own D9 rationale — "a prepared procedure with
a dead link is a broken procedure, and 'later' has no owner"
(`design.md:340`) — applies with equal force to an unrecorded notification.

**REQUIRED CHANGE.** Task 5.6 SHALL permit a dated `REVISED <date>` line beside
each repointed reference, naming this change; task 5.7 becomes "record the dated
note" rather than "tell". That is the runsheet's own idiom, it is not a step
change, and it is the difference between a notification and a fact.

---

## V12. Every LedgerxFactory Speckit worktree now needs a two-level recursive submodule init, and the packet never says the word "worktree"

**IMPACT: MEDIUM** · charge 4, journey (a)

**EVIDENCE.** The repository's normal working shape is a worktree, per the
validator's own docstring `:84-87`:

> `    The root checkout sits at <workspace>/xFactories/LedgerxFactory and a`
> `    Speckit worktree at <workspace>/xFactories/LedgerxFactory-worktrees/`
> `    <feature>, so the checkout is two or three levels up.`

And this repository has already been bitten once by a worktree path assumption —
`find_aggregation` exists BECAUSE of it, `:563-571`:

> `    pin.py defaults its aggregation root to `repo_root/../..`, which is`
> `    right for the shared checkout … and WRONG for every Speckit worktree`
> `    … where it lands on xFactories/ and the emitter SKIPs. An observation`
> `    silently switched off in exactly the trees where the work is done is`
> `    the failure this walk removes`

`git worktree add` does not populate submodules. After P6, every new
LedgerxFactory feature worktree needs `git submodule update --init --recursive
LedgerxWallet` before the wallet bar can run at all — a per-feature tax on the
repo's actual workflow, permanently, and the packet's `§ Impact` does not name
it. (I checked D5's `..` estate-root default against the worktree case: in
`LedgerxFactory-worktrees/<feature>/LedgerxWallet`, `..` is the worktree root,
which does hold `tenants/*/wallets/`. That default survives. Credited in
`§ What I checked and found sound`.)

**CONSTRAINT TO CARRY.** The delegator's refusal message SHALL name the worktree
case explicitly ("a new worktree does not inherit submodules; run …"), and the
bar block in `docs/protected-surface.md:62` and `quickstart.md:17` gains the
recursive init as a prerequisite line. One sentence each, and it is the
difference between a five-second fix and a twenty-minute puzzle in a tree where
the operator is mid-feature.

---

## V13. "Clone it and the bar goes green" is still false after the change, because of an inherited SKIP the packet never inventories

**IMPACT: MEDIUM**

**EVIDENCE.** `tests/validate_wallet_estate.py:661-666`:

```python
    aggregation, openx = find_aggregation()
    if aggregation is None:
        print("PIN RECONCILIATION: SKIP -- no aggregation checkout above "
              "this repository, so the recorded openxFactory submodule "
              "pointer cannot be read (the emitter's own SKIP case)")
        return
```

A standalone LedgerxFactory clone, with LedgerxWallet recursively initialized,
still has no aggregation root above it. So V1's benefit is delivered for the
wallet-estate half and **not** for the pin-observation half, which degrades to a
printed SKIP — the one outcome the repo's 2026-08-07 law and this packet's own
spec forbid (`spec.md:122-125`: "SHALL FAIL CLOSED with a named exit and a
REMEDIATION STRING … and SHALL NOT skip, pass, or degrade to 'empty'").

This SKIP is PRE-EXISTING, not caused by P6, and I say so plainly. But the
packet adds a fail-closed REQUIREMENT over a file that carries a live SKIP, and
does not mention it — so a reader of `spec.md:122-125` will believe the estate
bar has no skip path after this change, and it will.

**CONSTRAINT TO CARRY.** The packet SHALL inventory the SKIP at `:661-666` and
state which it is: inherited-and-out-of-scope (defensible, and then
`spec.md:122-125` must be scoped to "a fail-closed path **added by** this
relocation", which is in fact how `:140` already words the sibling scenario), or
closed here. Do not let the new requirement read as covering it. V4's split makes
this easy, because the SKIP moves to the half that stays beside the aggregation.

---

## V14. The pin this change introduces is the least-declared pin in the tree

**IMPACT: LOW**

**EVIDENCE.** After P6, openXwallet's commit is declared three ways and
cross-checked (`design.md:262-267`, `tasks.md:212-214`). LedgerxWallet's commit
is declared **once**, as a bare gitlink (`tasks.md:160-164`) — no pin manifest,
no `stack.yaml` block, no digest row, and LedgerxFactory has no CI to notice a
stale gitlink (`.github/` holds `CODEOWNERS` and `copilot-instructions.md`,
verified by `git ls-tree`).

Local precedent supports the packet here, and I checked it rather than assuming:
`git grep -l LedgerxAvatar origin/main` returns exactly one file, `.gitmodules`.
The existing descendant is gitlink-only too. So this is CONSISTENT and not a
breach — the ratified rule 2 governs descendant→product, not factory→descendant.

But for a change whose entire thesis is "a pin beats a walk", the pin it
introduces is the one nothing declares and nothing reads.

**CONSTRAINT TO CARRY.** Name it as a successor (a `contracts/ledgerxwallet-pin.yaml`
in LedgerxFactory, or a `stack.yaml` sibling block), and — cheap, now — have the
delegating entry PRINT the LedgerxWallet gitlink sha it resolved, beside the
three-way agreement it already prints at task 6.3. A stale descendant then shows
up in the bar's log instead of nowhere.

---

## V15. Changing a wallet rule goes from one commit to two repositories, with nothing enforcing the second

**IMPACT: MEDIUM** · charge 4, journey (b)

**EVIDENCE.** Today: edit `tests/validate_wallet_estate.py`, run
`docs/protected-surface.md:62` —
`for f in tests/validate_*.py; do python3 "$f" || echo "FAIL $f"; done` — commit.
One repository, one PR, one bar.

After: edit LedgerxWallet, PR it, merge it, then bump the LedgerxFactory gitlink
in a second PR. Since LedgerxFactory has no workflow, **nothing catches a merged
rule change that was never pinned in**, and the delegator will keep invoking the
old rule from the old gitlink while reporting green. The packet documents the
pin-bump procedure for the PRODUCT (`proposal.md:147-148`, README task 3.3) and
not for the descendant.

**CONSTRAINT TO CARRY.** LedgerxWallet's README pin-bump section SHALL document
the LedgerxFactory-side gitlink bump as the second half of one act, in the same
words the packet uses for the product pin — and V14's printed gitlink sha is what
makes a forgotten bump visible.

---

## V16. A third unbounded `os.walk(REPO)` gains a full product corpus, two levels deep

**IMPACT: LOW**

**EVIDENCE.** `tests/validate_realization_contracts.py:589-591`:

```python
    for dirpath, dirs, files in os.walk(REPO):
        dirs[:] = [d for d in dirs if d not in (".git", "node_modules",
                                                "__pycache__")]
```

No submodule exclusion. After P6 this descends into `LedgerxWallet/` and then
into `LedgerxWallet/openXwallet/` — the neutral product's whole YAML corpus —
loading and `yaml.safe_load`-ing every `.yaml`/`.yml` it finds.

Honest calibration: `LedgerxAvatar` is already nested, so the walk already
crosses one submodule boundary, and this check only errors on
`kind: ledgerx_probe_evidence` (`:600-603`), so the practical effect is bar
runtime and log volume rather than a false finding. I also checked the other
enumerators and they are safe: `validate_document_estate_surface.py:1223` uses
`git ls-files --cached --others --exclude-standard`, which lists a gitlink as one
entry and never its contents; `:618`/`:1527` and
`validate_protected_surface.py:113` walk declared roots.

**CONSTRAINT TO CARRY.** Record the bar's wall-clock before and after alongside
task 6.2's inventory. If it moves materially, add the submodule names to
`:590`'s exclusion list — a one-line change in a file the packet does not
otherwise touch, and better made deliberately than discovered by an operator
watching a bar that used to take seconds.

---

## V17. `/templates/` is the one directory of the new repo with no code owner — and it holds the artifact a prepared live window instantiates from

**IMPACT: LOW**

**EVIDENCE.** Task 3.3 scopes LedgerxWallet's CODEOWNERS to `/contracts/`,
`/profile/`, `/tests/` and `/.github/`. Task 4.1 puts
`templates/wallet-exercise.template.yaml` in a fifth directory. That template is
what `runsheet.md:22-23` tells the live-window operator to instantiate exercise
records from.

`opensoft` has an org-wide code-owner-review ruleset, and LedgerxFactory's own
CODEOWNERS exists because of exactly this shape
(`.github/CODEOWNERS:3-7`): "the org-wide `Require Code Owner Review` ruleset has
been active on this repository, and no CODEOWNERS file existed — so the rule
named nobody and therefore required nothing. A live gate with an empty owner set
reads as protection and provides none. Found 2026-08-26 across six repos in this
organization."

Calibration: LedgerxFactory does not own `/templates/`, `/tests/` or `/tenants/`
either (its CODEOWNERS covers `:20-29` only), so P6 is a net IMPROVEMENT — two of
the three moved paths GAIN an owner they lacked.

**REQUIRED CHANGE.** Add `/templates/` to task 3.3's list. One line, in the repo
where the org-wide finding of 2026-08-26 would otherwise reproduce itself for the
seventh time.

---

## V18. Adding a second Ledgerx tenant still requires editing the "cross-tenant" profile validator

**IMPACT: MEDIUM** · charge 4, journey (c)

**EVIDENCE.** D3's test is "IDENTICAL for a second Ledgerx tenant"
(`design.md:147-149`) and D6's argument against literal expected sets is that
"one tenant's wallet ids inside a cross-tenant profile is the same inversion"
(`proposal.md:258-260`). Both are right. But the file being moved has the tenant
compiled into it in three more places the packet does not name:

- `:39` `WALLET_DIR = os.path.join(REPO, "tenants", "ledgerxcorp", "wallets")`
  — a single literal path, while D5's estate-root refusal tests for the GLOB
  `tenants/*/wallets/` (`tasks.md:143-144`). The refusal and the reader disagree
  about how many tenants exist.
- `:728`'s `< 5` floor is a repo-wide scan count, not per-tenant (V3).
- `:774-776`'s constraint lookup assumes one estate directory.

So tenant 2 needs a second estate manifest (task 5.3 files it "beside the records
it enumerates", i.e. per-tenant — correct), plus three edits to the profile
validator. Q2's answer is right and the reusability it buys is currently partial.

**REQUIRED CHANGE.** Task 4.3 generalizes `WALLET_DIR` from the literal
`tenants/ledgerxcorp/wallets` to the `tenants/*/wallets/` glob the estate-root
refusal already tests for, with the floor and the constraint lookup following.
It is a small change now and a fork question later, and it is what makes D3's
test true in code rather than only in prose. This is the constraint I would least
like to see deferred.

---

## Q2 seat vote

**STAY.** The four records — `wal-lx-creator-01`, `wal-lx-poster-01`,
`grant-lx-create-01`, `grant-lx-post-01` — and their directory remain in
LedgerxFactory. I vote with the packet's recommendation, and with the parent's
(`split-openxwallet-repo/proposal.md:1158-1162`: "the profile artifacts move; the
tenant records stay put unless Ledgerx rules otherwise").

**My decisive reason is one the packet does not give.** These files are the
COMMIT TARGET of an unexecuted written procedure. `runsheet.md:132-134`:

> `- 3.4 Commit the wallet-record edits: `state: suspended` → `active`,`
> `  `key_id` confirmed, citing THIS runsheet execution and the 3.2`
> `  fingerprints. Wallet validator + full bar green before proceeding.`

and `README.md:107-108`: "the wallet identity estate at
`tenants/ledgerxcorp/wallets/` (suspended until the live window mints keys)".
Moving them would relocate the target of four written commit steps into a
repository that did not exist when the procedure was authored. That is precisely
the D9 hazard the packet already accepts, deliberately and correctly, for two
markdown links — multiplied to five files and four commit steps, inside a window
that mints real RSA keypairs (`runsheet.md:121-125`). The link repoint is a
sentence; this would be a rewrite of the phase.

**The content test agrees, and I verified it rather than taking it on trust.** The
records carry holder ids, DIDs, key ids and a mutable `state:`; the packet's
`proposal.md:169-175` characterization is accurate.

**I weigh the counter-case honestly.** STAY is what forces all three seams the
packet pays for: D4's delegator, D5's declared estate root, D6's manifest. Those
are real costs and V4 shows the packet has under-priced them. But each is a
fixed cost paid once, by code, in a change that is happening anyway. Moving the
estate would make the second Ledgerx tenant a fork question — an unbounded cost,
paid by whoever is unlucky enough to onboard tenant 2. Fixed-and-now beats
unbounded-and-later.

**One condition on my vote.** STAY is only true in code if V18 lands. As
specified, LedgerxWallet ships a "cross-tenant profile" with
`tenants/ledgerxcorp` compiled into line 39 of its own validator — Q2 answered
in prose and contradicted in the artifact. I vote STAY **with** V18 as a
condition, not as a suggestion.

---

## What I checked and found sound

Explicitly, so the record is calibrated. This is a strong packet and most of what
it claims survives checking.

1. **The rule-1 breach is real and the packet's best evidence is verbatim
   accurate.** `tests/validate_wallet_estate.py:57-63` really does concede "the
   aggregation's root gitlink is governed by nothing this repo pins" and answer it
   with "Candidate order is what breaks the tie". Quoting the code's own
   confession against itself is the right way to argue this, and it is not
   conformance-for-its-own-sake — a green bar that means "validated against an
   unpinned contract version" is a genuine defect. My quarrel in V1 is with which
   half of the benefit leads, not with whether there is one.

2. **D4's delegating bar entry is the right answer, and the rejected
   alternatives are the right ones to reject.** I verified every premise: the
   human-run glob at `docs/protected-surface.md:62` is real and is written down
   exactly as quoted; `.github/` holds `CODEOWNERS` and `copilot-instructions.md`
   and nothing else; there are 17 files matching `tests/validate_*.py`. A plain
   `git mv` WOULD silently remove the wallet estate from the only bar that checks
   it, and "quieter than a CI break, not safer" (`design.md:193-194`) is exactly
   right. The symlink and glob-widening rejections are correct. And D4 names the
   cheaper alternative the bench should weigh hardest (leave the validator behind)
   and defeats it on the correct ground — the validator IS the artifact whose
   resolution reaches outside the repository, so leaving it behind buys a smaller
   diff and keeps the breach. I agree, and V4 is a refinement of that answer
   rather than a reversal of it.

3. **D7 is the most honest paragraph in the packet and should be preserved
   verbatim.** Enumerating the fourth and fifth declarations of the same commit,
   declining to put them in the invariant, and stating flatly that "**Divergence
   is therefore not an error and is not checked**" — including the recorded
   self-correction from a weaker earlier draft that said divergence would be
   "REPORTED" and named no reporter — is the LS-A3 discipline working as
   intended. The same discipline appears at `proposal.md:407-415`, refusing to
   describe the three-way check as a required check when LedgerxFactory has no CI.
   That refusal is worth more than the check would have been.

4. **D9's same-commit repoint is the right call and the hazard is real.** Verified:
   `runsheet.md:3` `Status: prepared (this feature performs NONE of it)`;
   `runsheet.md:23` is exactly the relative link the packet quotes; Phase 3
   (`:119-134`) generates RSA keypairs and flips `suspended` → `active`;
   `README.md:117-119` confirms "What remains is the runsheet's live window
   (separately authorized; open preconditions P0.4 … then phases 1-6)". Waiting
   would indeed park P6 behind a decision it does not own. Both rejections
   (`design.md:337-340`) are correct.

5. **The `models/protected-surface.yaml` conclusion is right even though the
   pointer is not.** I checked the `pinned_files` block independently: it names
   `templates/coding-candidate.yaml`, `templates/correction-record.yaml` and five
   other templates (`:459-479`) plus the `tests/fixtures/intake-corpus/*` corpus,
   and carries **no** row for any of the three moved paths. `.gitmodules` is not
   pinned either, so task 5.1 owes no re-pin. "A prose amendment only" is correct
   and the packet was right to verify it rather than assume.

6. **`runsheet.md:174` really does reference the DHC by ID, not by path.** Verified:
   `` `refused_constraint` naming `dhc-lx-create-post-01` ``. So the DHC
   relocation genuinely needs no runsheet edit, and the packet distinguishes a
   surviving reference from a dangling one rather than repointing everything that
   mentions a moved file. That is a careful distinction and most packets get it
   wrong in the expensive direction.

7. **The nested-only placement and its stated price.** Choosing the RATIFIED
   placement over the one whose establishing act is `Status: draft` is right for
   a first-of-a-standard change, the `LedgerxAvatar` precedent is real (verified
   `.gitmodules`), and D2's governance-visibility cost — outside the notebook
   projection and ideation routing, as `MedxAvatar` has been for five months —
   is named as a price rather than discovered later. Rejecting both placements
   now ("two moving parts to solve a problem nobody has") is the right call.

8. **The annotated-tag dereference.** `wallet-v1.1` being a tag object whose
   commit must be resolved with `^{commit}` before it is written into a field
   declared `revision_kind: commit` is a real trap, and it is named as a task
   (`tasks.md:109-113`) rather than left to be discovered by whoever runs
   `rev-parse`. Small, and exactly the kind of thing that becomes a wrong
   precedent for three more domains.

9. **D5's `..` default survives the worktree case, which I checked because V12
   made me suspicious of it.** In
   `LedgerxFactory-worktrees/<feature>/LedgerxWallet`, `..` is the worktree root,
   which is a full checkout carrying `tenants/*/wallets/`. And D5 already names
   the one arrangement where the default breaks (`xFactories/LedgerxWallet`),
   shows the refusal fires loudly there, and records the "default becomes a
   required argument" consequence as a precondition on the change that would take
   that placement (`design.md:233-241`). That is the right way to handle a sharp
   edge you are not taking today.

10. **`.gitmodules` section naming.** Noticing that the existing entry is
    `[submodule "ledgerXavatar"]` against `path = LedgerxAvatar` (verified
    verbatim) and declining to propagate the mismatch is a small act of taste
    that saves someone a confused grep in two years.

11. **D3's decidable test, and D3a's named exception.** "An artifact belongs in
    LedgerxWallet if and only if it would be IDENTICAL for a second Ledgerx
    tenant" is the right instrument for a change that three more domains will
    copy, and naming the holder-registry seam as the ONE exception — because "an
    unnamed exception is how a test stops being one" (`design.md:171`) — is how a
    test stays usable. V18 is my complaint that the test is not yet true in the
    code, not that the test is wrong.

12. **Task 1.11's doc-health accounting.** Explaining the 64 → 64 baseline and the
    single rule-STRING rename caused by `_staged_exit_changes()` returning
    `sorted(...)`, so that nobody later reads it as a regression this packet
    caused, is the kind of pre-emptive bookkeeping that saves a future reviewer an
    hour. Credited.

13. **The bounded-scope claims all check out.** Two openxFactory files change and
    nothing else; no manifest row, no release surface; P4 and P3b are correctly
    identified as open and non-gating; P5b is correctly recorded as discharged at
    `b131286` / `1a8ec62`, and `stack.yaml:51-62` carries the declared
    `openxwallet:` block at `contract_ref: 63f5a1adac89f017e70bab9a4ffe7cf02d6e6705`
    with `contract_source: openxFactory-nested-submodule-pin`, exactly as
    described, preserve-this-block comment and all.
