# Clarifications

_Captured during alignment review and proposal council. These constrain the design._
_Two alignment reviewers (QA lead, stack architect) and three council seats
(product advocate, systems architect, adversary engineer), 2026-08-27._

**Verdicts:** Product Advocate PROCEED WITH CONSTRAINTS · Systems Architect
PROCEED WITH CONSTRAINTS · Adversary Engineer **RESTRUCTURE**.

**The RESTRUCTURE was TAKEN.** The packet as first authored relocated three
artifacts; it now relocates one. That is not a concession to tone — three
independent reviewers arrived at the same arithmetic from different directions,
and the arithmetic is in § Constraints below. Everything under
"Mooted by the restructure" was answered by narrowing rather than by prose, and
is recorded so the bench can see which objections were addressed by argument and
which by removing the thing objected to.

## Council- and review-identified constraints

### The relocation must survive openXwallet's nested-repository prune
**Raised by:** Adversary Engineer (V1), Systems Architect (V2)
**Concern:** openXwallet at `wallet-v1.1` prunes nested repositories from its
sweep by construction — `sweep_candidates()` (`scripts/validate-openxwallet.py:2063`)
exists because that sweep otherwise "walks into every repository nested below that
root and adjudicates its carried YAML as LIVE RECORDS of the consumer's tree", and
the prune is emitted as a note at `:2135-2142`. So any wallet-kind YAML placed
inside a nested `LedgerxWallet` is adjudicated by NOTHING. The prune arrived at
P2b of this same parent change.
**Design impact:** D3 makes this measurement M1 and withdraws the distinct-holder
constraint's relocation. `spec.md` requirement 4 makes it normative: an artifact
the pinned product's scan adjudicates SHALL NOT be relocated into the nested
descendant until a scan pass reaches it there. The relocation is a named
successor gated on that pass.

### A relocation that changes a count or a lookup must restate it in the same act
**Raised by:** Adversary Engineer (V1), Systems Architect (V1/V3), Stack Architect (F2/F3)
**Concern:** `check_real_estate()` asserts `elif int(m.group(1)) < 5: err(f"expected
>=5 wallet-family records validated …")` (`:721`, `:725-729`) — the five being two
wallet records, two grants and the distinct-holder constraint — and separately
does `dhc = constraints.get(EXPECTED_CONSTRAINT)` over records loaded from
`WALLET_DIR` alone (`:39`, `:735-746`, `:774-776`). Relocating the constraint
takes the count to four and the lookup to `None`. Both were measured in P5b's own
merged evidence one day before this packet was authored, and the first draft
promised "bar green" while doing exactly this.
**Design impact:** D3's measurements M2 and M3; `tasks.md` 4.2 and 6.3 make the
count an evidence line rather than an assumption. `spec.md` requirement 4 carries
the general rule.

### Rule 1 binds the RESOLUTION path, not the file's address
**Raised by:** Stack Architect (F2), Product Advocate (V4)
**Concern:** `tests/validate_wallet_estate.py` is LedgerxFactory-authored — its
header cites feature 016 and the 2026-08-08 ratification, and features 018/019
record it as unpinned LedgerxFactory code. Ratified rule 1 forbids integrating
THE PRODUCT'S validator. Moving the domain's own validator to close a rule-1
breach opens four seams for a fix the breach does not require: `REPO` (`:38`)
serves four referents — `WALLET_DIR` (`:39`), the pinned validator's scan target
with the floor (`:721`), `os.path.join(REPO, "stack.yaml")` (`:675-676`), and the
pin checker's positional argument (`:705`) — and `find_aggregation()` (`:560-595`)
is a SECOND five-level upward walk feeding a leg the parent's ratified `tasks.md`
6.2 makes this bar the only observer of.
**Design impact:** D4. The validator stays; only `VALIDATOR_CANDIDATES` and its
walk are replaced by one fixed path into the descendant. `find_aggregation()` and
`check_pin_reconciliation()` are untouched. The full move becomes a successor
shaped as a validator SPLIT.

### The parent's realization evidence must migrate, not die
**Raised by:** Adversary Engineer (V19)
**Concern:** Deleting `VALIDATOR_CANDIDATES` also deletes
`check_finder_candidates()` and its eight `FINDER_PROBES` (`:275-331`) — including
the ratified-order assertion and the `legacy-only` inversion the file calls "the
whole of what 10.1 changes observably" — `check_finder_loud_failure()`
(`:377-401`), and the constants `_NESTED`/`_AGGREGATION`/`_LEGACY`. These are the
RUNNING realization evidence of the parent's ratified tasks 2.1-2.3 and 10.1, and
the parent has NOT archived; its `tasks.md` 13.1 calls the evidence table "a gate,
not a report". P6 would close its parent's evidence before its parent's gate.
**Design impact:** D4a. The probes MIGRATE: the single descendant candidate
resolves, and `_NESTED`, `_AGGREGATION` and `_LEGACY` each resolve NOTHING,
retained as inverted probes for the reason P5b retained `_LEGACY`. `tasks.md`
5.3a cites the parent's task ids in the code so its table can be filled from this
run. The claim "every negative-probe corpus is byte-unchanged" is withdrawn as
false — `FINDER_PROBES` is one and cannot survive unchanged.

### The pin needs a verifier that reads the CHECKED-OUT tree
**Raised by:** Adversary Engineer (V3, V9), Stack Architect (F11)
**Concern:** Nothing compares the checked-out `openXwallet/` revision to the pin,
so a fork at another commit — or a stale or dirty checkout — EXECUTES while every
recorded declaration still agrees. The ratified rule's own scenarios say "the
descendant's OWN VALIDATOR REFUSES the tree", and the first scaffold shipped the
refusal declared and nothing that refuses. Separately, nothing declares WHICH
LedgerxWallet commit LedgerxFactory expects, so a stale descendant gitlink yields
a self-consistent GREEN.
**Design impact:** D5 adds `tests/validate_pin.py` with FOUR checks, the fourth
being `git -C openXwallet rev-parse HEAD` plus `git submodule status` `+`
detection, and `.github/workflows/pin-validation.yml` to run it — also the only
thing that lets the EVALUATE-mode ruleset be promoted. D6 adds the FOURTH READ on
the LedgerxFactory side: compare `git ls-tree HEAD LedgerxWallet` to the checkout
about to be read.

### `stack.yaml` is digest-pinned, so editing it owes a re-pin
**Raised by:** Stack Architect (F1), Adversary Engineer (V13), Product Advocate (V9)
**Concern:** The packet edits `stack.yaml` while asserting
`models/protected-surface.yaml` needs "a prose amendment only". That file PINS
`stack.yaml` by digest (`:384-385`), `docs/protected-surface.md:66-70` requires
the re-pin with an attributed reason, and the entry itself records the cost of
skipping (`:442-445`): "red on main for seventeen days".
**Design impact:** D7. `tasks.md` 5.5 makes the digest re-pin and its
`pinned_by:` reason part of the same commit, gated on
`tests/validate_onboarding_contracts.py`. The prose pointer is at `:455`, not the
`:438` cited against a pre-P5b tree.

### Fail-closed refusals name the runbook, and the init is recursive
**Raised by:** Adversary Engineer (V8), Product Advocate (V8)
**Concern:** `neutral-product-pin` requires a refusal to name the initializing
command AND the pin-resync runbook's path; the packet named only a command, and
that command was non-recursive while the reader sits two gitlinks down
(`LedgerxWallet`, then `openXwallet` inside it) — so it would appear to succeed
and leave the refusal standing.
**Design impact:** D4/D5. Every refusal names `git submodule update --init
--recursive <path>` plus `LedgerxWallet/docs/pin-resync-runbook.md`, and the
scaffold includes that runbook (`tasks.md` 3.2). The pin file carries
`verify_pin:` and `resync_runbook:` keys mirroring openxFactory's own.

### The repoint reaches beyond feature 016, and records keep their historical paths
**Raised by:** Adversary Engineer (V15, V16), Stack Architect (F8)
**Concern:** `specs/016/quickstart.md:19` invokes the neutral validator through
openxFactory's checkout and `:3-7` names that checkout as a prerequisite — a
rule-1 breach site in written procedure, not just a stale link. Beyond 016:
`specs/017/quickstart.md:36,49,97-98` imports the validator and calls
`check_finder_candidates()`; `specs/018/rollback.md:28` and
`specs/019/rollback.md:37` are rollback procedures for MERGED features that
operate on the narrowing finder; `tests/validate_document_estate_surface.py:1086-1098`
declares the old consumption path in prose its own text says was "Corrected at
P5b".
**Design impact:** D8 and `tasks.md` 5.6/5.8/5.9. Records of PERFORMED acts keep
their historical paths and gain DATED NOTES; live procedures are repointed in the
same commit; runsheet precondition P0.5 is added; and the task says explicitly
what happens to P5b's rollback.

### A nested descendant is outside every governed-repo enumeration
**Raised by:** Stack Architect (F5)
**Concern:** `scripts/sync-notebooklm-books.py:652-653` matches only
`^\s*path\s*=\s*(xFactories/\S+)\s*$`, its `in_nested_checkout()` (`:629-641`,
`:767`) excludes anything below a `.git`-carrying directory, and
`scripts/doc_health/ideation_routing.py:225-235` admits only `openxFactory` and
`xFactories/<Name>`. The parent's P4b widens exactly those sites by an allowlist
of ROOT-LEVEL neutral products, so a nested domain descendant is outside the set
before that widening and after it — and the ratified precedent (`MedxAvatar`,
`LedgerxAvatar`) is already in the hole.
**Design impact:** D2 names the price rather than discovering it later, and
§ Successors registers "governed-repo recognition for a NESTED descendant", which
would also finally cover the two existing nested descendants.

### The moved template is not tenant-free, and the rule is narrowed to fit the artifact
**Raised by:** Stack Architect (F3/F6), QA Lead
**Concern:** The template names `grant_ref` (`:24`), `presenting_key_ref` (`:34`),
`wallet_ref` (`:38`), `holder_ref` (`:39`) and `constraint_ref` (`:48`), and
points instances at `tenants/ledgerxcorp/ledger-estates/` (`:4`). The packet
claimed it named no tenant, and its own estate-refusal scenario would have
refused it.
**Design impact:** D3 drops the claim. `spec.md` requirement 3's refusal is scoped
to RECORDS, with an explicit scenario admitting a template that shows which ids to
substitute. The ids are not generalized (`tasks.md` 7.7) — that is a separate act.

### The creation gate is Ledgerx's own, not four other domains'
**Raised by:** Stack Architect (F12)
**Concern:** A Ledgerx-scoped capability carrying a SHALL over `MedxWallet`,
`codexWallet`, `OpsxWallet` and `AdxWallet` creates two sources for one
obligation the ratified rule already binds generally — and the packet's own
§ Modified Capabilities says it issues no delta, so the restatement would not move
if the neutral rule were amended.
**Design impact:** `spec.md` requirement 5 is scoped to LedgerxWallet's own
creation and CITES `domain-descendant-boundary` for the siblings, with a scenario
saying a citation of this capability does not carry.

### The pin's fork-detector is not the ratified one, and the difference is declared
**Raised by:** Adversary Engineer (V5), Stack Architect (F10)
**Concern:** `domain-descendant-boundary`'s fork scenario names "the pin's
DIGESTS" as the detector. This pin carries a commit and no digests, so restating
the scenario with "the recorded commit" silently swaps a ratified detector while
claiming to issue no delta.
**Design impact:** `spec.md` requirement 3's scenario says exactly what detects a
fork here — the descendant's validator comparing the checked-out revision and
cleanliness — and states that the digest detector is deliberately not carried, as
a reduction in effect rather than an amendment. § Impact carries the reduction:
the Ledgerx reader becomes gitlink-verified where it was reached through
openxFactory's digest-verified gitlink.

### Every "REFUSED" in normative text names its enforcer, or is not written
**Raised by:** Adversary Engineer (V6, and the LS-A3 group), Stack Architect (F4)
**Concern:** The spec's THENs asserted refusals and reports that nothing emits —
including "an empty boundary … is REPORTED", and a pin divergence described as
"REPORTED" with no reporter. The proposal itself names LS-A3 while the spec
committed its shape.
**Design impact:** Each unwired THEN is either built (the descendant's pin
validator; the estate bar's three-way check) or softened to an observation with a
stated owner. The openxFactory-divergence case now says plainly that it is not an
error and is checked by nothing. `spec.md` requirement 2 adds a scenario saying
the third reachable checkout falls OUTSIDE `neutral-product-pin`'s
root-equals-nested rule, and that the rule's illustrative "resolves the NESTED
checkout" sentence stops describing this consumer without being amended by this
capability.

### The operator's path must be executable end to end
**Raised by:** Product Advocate (V7, V8)
**Concern:** "Promote the ruleset to ACTIVE once a check has reported" was
unsatisfiable — nothing in the change created a workflow in LedgerxWallet.
**Design impact:** D5 adds `.github/workflows/pin-validation.yml`; `tasks.md` 3.7
and 6.10 order it before promotion. Green-run tasks name the initialized checkout
they depend on (`tasks.md` 6.1), because the bar is red-by-construction without it.

## Q2 — the one carried question

**Do `tenants/ledgerxcorp/wallets/*` move into LedgerxWallet, or stay?**
Recommendation: **STAY.** The Product Advocate seat voted STAY independently and
supplied the reason the packet had not: **those five files are the commit target
of the runsheet's unexecuted Phase 3.4**, a procedure that mints real keys and
flips wallet state. That is now the third and strongest of the three grounds in
§ Open questions, after the records' own instance-shaped contents and the
nested-repository prune.

## Findings MOOTED by the restructure

Recorded so the bench can distinguish what was answered from what was removed.
All concerned the withdrawn relocation of the estate validator or the
distinct-holder constraint: the declared estate root and its three re-based reads;
the estate root's `..` default and the trees where it is wrong; the delegating bar
entry and whether a delegator is a fork under rule 3 (judged NOT a fork, and the
alternatives — widening the glob at `docs/protected-surface.md:62`, or a symlink
that `os.path.abspath(__file__)` does not resolve — judged worse); the
expected-set relocation; the descendant reading LedgerxFactory's `stack.yaml`;
`find_aggregation()`'s deepened walk; the profile-root/estate-root split; and the
custody-posture artifact. Each is preserved in the retained review records, and
the first two successors in § Successors carry the ones that must be solved when
the relocation is attempted again.

## Calibration retained from the reviews

Three points the reviewers checked and found sound, recorded because a review
record that only lists defects mis-states the packet: the **placement section**
is the best treatment of ratified rule 4 in the corpus (states both standings,
takes the ratified one, gives a real criterion, carries the both-placements rule
forward); authoring this capability in **openxFactory's** OpenSpec instance rather
than LedgerxFactory's is correct on house precedent and breaches no aggregation
working rule; and the **wallet-kind sweep is complete** — eight `git grep` hits,
seven committed YAML artifacts and the validator's embedded probe corpora, with
nothing missed.
